const assert = require('node:assert/strict');
const fs = require('node:fs');
const { chromium } = require('C:/Users/orlan.ORLANDO/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
(async () => {
 const browser = await chromium.launch({headless:true, executablePath:'C:/Program Files/Google/Chrome/Application/chrome.exe'});
 const page = await browser.newPage();
 const errors = [];
 page.on('pageerror', e => errors.push(e.message));
 const base = 'file:///' + process.cwd().replaceAll('\\','/') + '/teacher/';
 await page.clock.install({ time: new Date('2026-11-10T07:30:00') });
 await page.goto(base + 'pages/exam_instructions.html');
 async function fit() {
  const result = await page.evaluate(() => {
   const elements = [...document.querySelectorAll('h1,.class-timer,.desk-column,.important,.footer,li')];
   return {inner:[innerWidth,innerHeight],scroll:[document.documentElement.scrollWidth,document.documentElement.scrollHeight],
    visible:elements.every(e => {const r=e.getBoundingClientRect();return r.top>=0 && r.left>=0 && r.bottom<=innerHeight && r.right<=innerWidth;}),
    overlap:document.querySelector('h1').getBoundingClientRect().right > document.querySelector('.header-tools').getBoundingClientRect().left};
  });
  assert.deepEqual(result.scroll,result.inner);
  assert.equal(result.visible,true);
  assert.equal(result.overlap,false);
  return result;
 }
 for (const [width,height] of [[1280,720],[1366,768],[1440,900],[1920,1080]]) {
  await page.setViewportSize({width,height});
  console.log('normal',width,height,await fit());
  await page.screenshot({path:`tmp/exam-validation/${width}x${height}.png`});
  await page.getByRole('button',{name:'Fullscreen',exact:true}).click();
  assert.equal(await page.evaluate(()=>document.fullscreenElement?.id),'exam-page');
  assert.equal(await page.getByRole('button',{name:'Exit fullscreen'}).getAttribute('aria-pressed'),'true');
  console.log('fullscreen',width,height,await fit());
  if (width === 1280) {
   await page.keyboard.press('Escape');
   console.log('native Escape exited fullscreen:',await page.evaluate(()=>!document.fullscreenElement));
  }
  await page.evaluate(()=>document.fullscreenElement ? document.exitFullscreen() : undefined);
  await page.waitForFunction(()=>document.querySelector('#fullscreen-toggle').getAttribute('aria-pressed')==='false');
 }
 for (const [time,label,value] of [
  ['06:30:00','Contact starts in','15:00'],['06:45:00','Contact ends in','15:00'],
  ['07:00:00','1st Hour starts in','5:00'],['07:30:00','1st Hour ends in','25:00'],
  ['07:55:00','2nd Hour starts in','5:00'],['08:00:00','2nd Hour ends in','50:00'],
  ['09:45:00','Break ends in','30:00'],['12:55:00','Lunch ends in','1:00:00'],
  ['14:45:00','Pause ends in','15:00'],['16:00:00','School day ended','']]) {
  await page.clock.setSystemTime(new Date('2026-11-10T'+time));
  await page.evaluate(()=>window.dispatchEvent(new Event('focus')));
  assert.equal(await page.locator('#timer-label').textContent(),label);
  assert.equal(await page.locator('#timer-value').textContent(),value);
 }
 await page.clock.setSystemTime(new Date('2026-11-10T07:54:59'));
 await page.evaluate(()=>document.dispatchEvent(new Event('visibilitychange')));
 assert.equal(await page.locator('#timer-value').textContent(),'0:01');
 await page.clock.runFor(1250);
 console.log('automatic boundary',await page.evaluate(()=>({now:new Date().toString(),label:document.querySelector('#timer-label').textContent,value:document.querySelector('#timer-value').textContent})));
 assert.equal(await page.locator('#timer-label').textContent(),'2nd Hour starts in');
 for(const [date,label] of [['2026-11-14','Weekend · no school'],['2026-11-16','School holiday'],['2026-12-24','Not a school day'],['2028-01-03','Calendar unavailable']]) {
  await page.clock.setSystemTime(new Date(date+'T08:00:00'));
  await page.evaluate(()=>window.dispatchEvent(new Event('focus')));
  assert.equal(await page.locator('#timer-label').textContent(),label);
  assert.equal(await page.locator('#timer-value').isVisible(),false);
 }
 await page.clock.setSystemTime(new Date('2026-11-10T08:00:00'));
 await page.evaluate(()=>{window.academicCalendar=undefined; window.dispatchEvent(new Event('focus'));});
 assert.equal(await page.locator('#timer-label').textContent(),'Calendar unavailable');
 // Text enlargement must grow naturally; no clipped content or horizontal scrolling.
 await page.setViewportSize({width:1280,height:720});
 await page.addStyleTag({content:'html {font-size:200% !important}'});
 const zoom = await page.evaluate(()=>({width:innerWidth,scroll:document.documentElement.scrollWidth,height:innerHeight,scrollHeight:document.documentElement.scrollHeight}));
 assert.equal(zoom.width,zoom.scroll);
 assert.ok(zoom.scrollHeight>zoom.height);
 console.log('200% text',zoom);
 await page.reload();
 await page.setViewportSize({width:390,height:844});
 const narrow=await page.evaluate(()=>({width:innerWidth,scroll:document.documentElement.scrollWidth,height:innerHeight,scrollHeight:document.documentElement.scrollHeight}));
 assert.equal(narrow.width,narrow.scroll);
 assert.ok(narrow.scrollHeight>narrow.height);
 console.log('narrow',narrow);
 // API rejection is caught and shown without breaking the countdown.
 await page.evaluate(()=>{document.querySelector('#exam-page').requestFullscreen=()=>Promise.reject(Error('denied'));});
 await page.getByRole('button',{name:'Fullscreen',exact:true}).click();
 assert.equal(await page.locator('#fullscreen-message').isVisible(),true);
 assert.equal(await page.locator('#fullscreen-toggle').isEnabled(),true);
 await page.addInitScript(()=>Object.defineProperty(document,'fullscreenEnabled',{get:()=>false}));
 await page.reload();
 assert.equal(await page.locator('#fullscreen-toggle').isVisible(),false);
 // Existing timer view retains its own presentation using the shared formatter.
 await page.setViewportSize({width:1280,height:720});
 await page.goto(base+'timer_view.html');
 for (const [time,title,countdown] of [
  ['06:30:00','School day begins soon','15:00 until Contact'],
  ['07:30:00','1st Hour','25:00 remaining'],
  ['07:55:00','Between periods','5:00 until 2nd Hour'],
  ['09:45:00','Break','30:00 remaining'],
  ['12:55:00','Lunch','1:00:00 remaining'],
  ['14:45:00','Pause','15:00 remaining'],
  ['16:00:00','School schedule ended','']]) {
  await page.clock.setSystemTime(new Date('2026-11-10T'+time));
  await page.evaluate(()=>window.dispatchEvent(new Event('focus')));
  assert.equal(await page.locator('#period-title').textContent(),title);
  assert.equal(await page.locator('#countdown').textContent(),countdown);
 }
 assert.deepEqual(errors,[]);
 console.log('PASS: layout, fullscreen API, timer states, restoration, text zoom, narrow screen, API failure, unsupported fullscreen, existing timer view; no JS errors');
 await browser.close();
})().catch(e=>{console.error(e);process.exit(1);});

