/* Dev-only: Playwright + installed Edge; no page runtime dependencies. */
const {chromium}=require('playwright'),assert=require('node:assert/strict'),path=require('node:path'),fs=require('node:fs'),http=require('node:http'),{pathToFileURL}=require('node:url');
(async()=>{
 const root=path.resolve(__dirname,'../..'),out=path.join(root,'tmp/population-verification');fs.mkdirSync(out,{recursive:true});
 const server=http.createServer((req,res)=>{const file=path.resolve(root,'.'+decodeURIComponent(req.url.split('?')[0]));if(!file.startsWith(root+path.sep)){res.writeHead(403).end();return;}fs.readFile(file,(err,bytes)=>{if(err){res.writeHead(404).end();return;}const ext=path.extname(file);res.setHeader('Content-Type',({'.html':'text/html','.css':'text/css','.js':'text/javascript','.svg':'image/svg+xml'})[ext]||'application/octet-stream');res.end(bytes);});});
 await new Promise(resolve=>server.listen(0,'127.0.0.1',resolve));let browser;
 try{
 browser=await chromium.launch({channel:'msedge',headless:true});
 const page=await browser.newPage({viewport:{width:1440,height:1000},reducedMotion:'reduce'}),errors=[],requests=[];
 page.on('pageerror',e=>errors.push(e.message));page.on('console',m=>{if(m.type()==='error')errors.push(m.text());});page.on('request',r=>requests.push(r.url()));
 const fileURL=pathToFileURL(path.join(root,'general_fundamentals/population_sample_simulation.html')).href;
 const base=`http://127.0.0.1:${server.address().port}`;
 const snapshot=()=>page.evaluate(()=>({step:state.step,n:state.students.length,labels:state.students.map(s=>s.name),selected:[...selected],studies:state.studies.length,mu:MU,sigma:SIGMA}));
 for(const url of [fileURL,base+'/general_fundamentals/population_sample_simulation.html']){
  // Storage failure or survey lockout cannot prevent opening the public lesson.
  await page.addInitScript(()=>{Storage.prototype.getItem=()=>{throw Error('disabled');};Storage.prototype.setItem=()=>{throw Error('disabled');};});
  await page.goto(url);assert.equal(await page.locator('#lesson-password,#variable,#grade,#group').count(),0);assert.equal((await snapshot()).n,0);
  await page.locator('#add-one').focus();await page.keyboard.press('Enter');assert.equal((await snapshot()).n,1);assert.match(await page.locator('#student-detail').textContent(),/Generated 1/);
  await page.locator('#add-one').press('Space');assert.equal((await snapshot()).n,2);
  await page.locator('#options-titlebar').focus();await page.keyboard.press('Escape');assert.equal(await page.locator('#options-open').evaluate(el=>el===document.activeElement),true);
  await page.locator('#next').click();await page.locator('#options-open').click();
  for(const count of [1,10,100,1000])await page.locator(`[data-add="${count}"]`).click();assert.equal((await snapshot()).n,1113);
  assert.equal(new Set((await snapshot()).labels).size,1113);
  await page.locator('#histogram').click();await page.locator('#options-close').click();const bin=page.locator('.bin:visible').first();await bin.focus();await bin.press('Enter');assert.match(await bin.getAttribute('aria-label'),/students/);await bin.press('Escape');
  await page.locator('[data-step="3"]').click();await page.locator('#window').focus();const start=await page.evaluate(()=>state.sampling.start);await page.keyboard.press('ArrowRight');assert.equal(await page.evaluate(()=>state.sampling.start),start+1);
  const end=await page.evaluate(()=>state.sampling.end);await page.keyboard.press('Shift+ArrowRight');assert.equal(await page.evaluate(()=>state.sampling.end),end+1);await page.keyboard.press('Alt+ArrowRight');
  await page.locator('#chart').focus();await page.keyboard.press('ArrowRight');assert.equal(await page.locator('#inspect').inputValue(),'2');
  await page.locator('#options-open').click();await page.locator('#mode-random').click();await page.locator('#sample-number').fill('30');await page.locator('#sample-number').dispatchEvent('input');assert.equal((await snapshot()).selected.length,30);
  await page.locator('#redraw').click();assert.equal(new Set((await snapshot()).selected).size,30);
  await page.locator('[data-step="4"]').click();await page.locator('#sample-number').fill('30');await page.locator('#sample-number').dispatchEvent('input');await page.locator('#options-close').click();
  const ci=await page.evaluate(()=>interval());assert.ok(Math.abs(ci.se-8/Math.sqrt(30))<1e-12);assert.ok(Math.abs(ci.moe-ci.z*ci.se)<1e-12);assert.ok(!/NaN|Infinity/.test(await page.locator('#formulas').textContent()));
  await page.locator('#why > summary').click();const before=await snapshot();await page.locator('[data-studies="10"]').click();await page.waitForFunction(()=>state.studies.length===10);assert.deepEqual((await snapshot()).selected,before.selected);assert.deepEqual((await snapshot()).labels,before.labels);
  await page.locator('#options-open').click();await page.locator('[data-confidence="99"]').click();assert.equal((await snapshot()).studies,0);const wide=await page.evaluate(()=>interval());assert.ok(wide.W>ci.W);
  await page.locator('#options-close').click();await page.locator('[data-studies="1"]').click();await page.locator('#options-open').click();await page.locator('#sample-number').fill('20');await page.locator('#sample-number').dispatchEvent('input');assert.equal((await snapshot()).studies,0);await page.locator('#options-close').click();
  await page.locator('[data-studies="1"]').click();await page.locator('#clear-studies').click();assert.equal((await snapshot()).studies,0);
  const identity=await snapshot();await page.locator('#population-mu').fill('160');await page.locator('#population-sigma').fill('6');await page.locator('#population-settings button').click();const changed=await snapshot();assert.equal(changed.mu,160);assert.equal(changed.sigma,6);assert.deepEqual(changed.labels,identity.labels);assert.deepEqual(changed.selected,identity.selected);
  await page.locator('#population-sigma').fill('0');await page.locator('#population-settings button').click();assert.equal(await page.locator('#population-sigma').evaluate(el=>el===document.activeElement),true);assert.equal((await snapshot()).sigma,6);
  await page.locator('#reset').click();assert.deepEqual(await snapshot(),{step:1,n:0,labels:[],selected:[],studies:0,mu:170,sigma:8});assert.equal(await page.locator('#tooltip').isHidden(),true);assert.equal(await page.locator('#why').getAttribute('open'),null);
  await page.locator('[data-step="4"]').click();assert.equal((await snapshot()).n,20);assert.equal(await page.locator('#confidence').inputValue(),'95');
 }
 for(const width of [1440,390,320]){
  await page.setViewportSize({width,height:1000});
  for(const step of [1,2,3,4]){
   await page.locator(`[data-step="${step}"]`).click();assert.equal(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth),true);
   await page.screenshot({path:path.join(out,`simulation-${width}-step${step}.png`),fullPage:true});
  }
  await page.locator('[data-step="3"]').click();await page.locator('#options-open').click();await page.locator('#mode-window').click();
  assert.equal(await page.locator('#options-panel').evaluate(el=>el.scrollWidth<=el.clientWidth),true);
  await page.screenshot({path:path.join(out,`simulation-options-${width}.png`),fullPage:true});
  await page.locator('#options-titlebar').focus();await page.keyboard.press('Home');await page.keyboard.press('ArrowLeft');await page.keyboard.press('Escape');assert.equal(await page.locator('#options-open').evaluate(el=>el===document.activeElement),true);
 }
 assert.deepEqual(requests.filter(u=>/survey|workbook|student|population-lesson-gate|population-simulation\.js|\.xlsx/i.test(u)),[]);
 // Hosted restricted page still defers its assets until password entry.
 const restricted=await browser.newPage(),restrictedRequests=[];restricted.on('request',r=>restrictedRequests.push(r.url()));
 await restricted.goto(base+'/general_fundamentals/population_sample_simulation_restricted.html');assert.equal(await restricted.locator('#lesson').isHidden(),true);assert.equal(restrictedRequests.some(u=>u.includes('survey_data')),false);
 await restricted.locator('#lesson-password').fill('321654');await restricted.locator('#lesson-password').press('Enter');await restricted.locator('#lesson').waitFor({state:'visible'});assert.ok(restrictedRequests.some(u=>u.includes('survey_data_extended.js')));await restricted.close();
 assert.deepEqual(errors,[]);console.log('Simulation browser checks passed: file + HTTP, no gate or survey/student requests, generated labels, all steps, keyboard/focus, sampling, known-sigma CI, studies, parameters, Reset, 1440/390/320px; hosted survey gate retained.');
 }finally{if(browser)await browser.close();await new Promise(resolve=>server.close(resolve));}
})().catch(e=>{console.error(e);process.exitCode=1;});
