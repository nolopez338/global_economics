/* Dev-only: requires Playwright. Uses installed Edge, no page runtime dependencies.
   node teacher/tools/population-simulation.browser.cjs */
const {chromium}=require('playwright'),assert=require('node:assert/strict'),path=require('node:path'),{pathToFileURL}=require('node:url'),fs=require('node:fs');
(async()=>{
 const browser=await chromium.launch({channel:'msedge',headless:true});
 const page=await browser.newPage({viewport:{width:1440,height:1000},reducedMotion:'reduce'}),errors=[];
 page.on('pageerror',e=>errors.push(e.message));page.on('console',m=>{if(m.type()==='error')errors.push(m.text());});
 const url=pathToFileURL(path.resolve(__dirname,'../../general_fundamentals/population_sample_simulation_restricted.html')).href;
 fs.mkdirSync(path.resolve('tmp/population-verification'),{recursive:true});
 const key='population-lesson-password-failures';
 const unlock=async p=>{await p.locator('#lesson-password').fill('321654');await p.locator('#lesson-password').press('Enter');await p.locator('#lesson').waitFor({state:'visible'});await p.waitForFunction(()=>typeof state!=='undefined');};
 const closed=async p=>{assert.equal(await p.locator('#lesson').isHidden(),true);assert.equal(await p.evaluate(()=>typeof SurveyData),'undefined');assert.equal(await p.evaluate(()=>typeof state),'undefined');assert.equal(await p.locator('script[src*="survey_data_extended"]').count(),0);};
 await page.goto(url);await closed(page);
 assert.equal(await page.locator('#lesson-password').evaluate(el=>el===document.activeElement),true);
 await page.keyboard.press('Tab');assert.equal(await page.locator('#gate-enter').evaluate(el=>el===document.activeElement),true);
 for(const width of [1440,390,320]){await page.setViewportSize({width,height:1000});assert.equal(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth),true);await page.screenshot({path:path.resolve(`tmp/population-verification/gate-${width}.png`),fullPage:true});}
 await page.setViewportSize({width:1440,height:1000});
 for(const [i,value] of ['321','321654 ','x321654',''].entries()){
  await page.locator('#lesson-password').fill(value);
  if(i%2)await page.locator('#lesson-password').press('Enter');else await page.locator('#gate-enter').click();
  assert.match(await page.locator('#gate-feedback').textContent(),new RegExp(`${4-i} attempts remaining`));await closed(page);
  await page.reload();assert.match(await page.locator('#gate-feedback').textContent(),new RegExp(`${4-i} attempts remaining`));
 }
 // Correct entry clears four failures and focuses the lesson. Success is never persisted.
 await unlock(page);assert.equal(await page.evaluate(k=>localStorage.getItem(k),key),'0');assert.equal(await page.locator('#step-title').evaluate(el=>el===document.activeElement),true);
 await page.reload();await closed(page);await unlock(page);
 // A separate profile exercises durable fifth-attempt lockout, reopening, and storage errors.
 const lockedContext=await browser.newContext(),locked=await lockedContext.newPage();await locked.goto(url);
 for(let i=1;i<=5;i++){await locked.locator('#lesson-password').fill('wrong');await locked.locator('#gate-enter').click();if(i<5)assert.match(await locked.locator('#gate-feedback').textContent(),new RegExp(`${5-i} attempts remaining`));}
 const checkLock=async p=>{await closed(p);assert.equal(await p.locator('#gate-feedback').textContent(),'Access blocked after five incorrect attempts.');assert.equal(await p.locator('#gate-enter').isDisabled(),true);assert.equal(await p.locator('#lesson-password').isDisabled(),true);};
 await checkLock(locked);await locked.reload();await checkLock(locked);await locked.close();const reopened=await lockedContext.newPage();await reopened.goto(url);await checkLock(reopened);
 await reopened.evaluate(()=>{document.querySelector('#lesson-password').value='321654';document.querySelector('#password-form').requestSubmit();});await checkLock(reopened);await lockedContext.close();
 for(const method of ['getItem','setItem']){const context=await browser.newContext();await context.addInitScript(method=>{Storage.prototype[method]=()=>{throw new Error('Storage disabled');};},method);const p=await context.newPage();await p.goto(url);await closed(p);assert.match(await p.locator('#gate-feedback').textContent(),/Persistent browser storage is unavailable/);assert.equal(await p.locator('#gate-enter').isDisabled(),true);await context.close();}
 await page.waitForFunction(()=>document.querySelector('#dataset-counts').textContent.includes('Usable Height: 109'));
 const snapshot=()=>page.evaluate(()=>({n:state.students.length,actual:state.students.filter(s=>s.source==='actual').length,synthetic:state.students.filter(s=>s.source==='synthetic').length,ids:state.students.map(s=>s.questionnaire_id),used:reveal.used,fitN:fit.n,selected:selected.size,studies:state.studies.length,step:state.step,mean:MU,sd:SIGMA}));
 // Names appear only for actual observations in step 1, through text-safe sinks.
 for(let i=0;i<3;i++)await page.locator('#add-one').click();await page.evaluate(()=>inspectStudent(2));
 const first=await page.evaluate(()=>{const s=state.students[2],r=data.records.find(r=>r.questionnaire_id===s.questionnaire_id);return {name:r.student_name,label:r.label,display:observationLabel(s)};});
 assert.ok(first.name);assert.equal(first.display,first.name);assert.equal(await page.evaluate(label=>{const seen=[],original=ctx.fillText;ctx.fillText=function(t,...args){seen.push(t);return original.call(this,t,...args);};try{draw();}finally{ctx.fillText=original;}return seen.some(t=>t.includes(label));},first.display),true);assert.ok((await page.locator('#student-detail').textContent()).includes(first.display));
 // Exercise the real canvas pointer tooltip, then repeat with hostile and missing names.
 const hoverFirst=async()=>{await page.locator('#chart').scrollIntoViewIfNeeded();await page.evaluate(()=>new Promise(requestAnimationFrame));const point=await page.evaluate(()=>{const r=canvas.getBoundingClientRect(),s=state.students[2];return {x:r.x+x(s.order),y:r.y+y(s.height)};});await page.mouse.move(point.x,point.y);};
 await page.locator('#options-close').click();await hoverFirst();assert.ok((await page.locator('#tooltip').textContent()).includes(first.display));await page.screenshot({path:path.resolve('tmp/population-verification/names-step1.png'),fullPage:true});
 await page.evaluate(()=>{state.students[2].studentName='Ángela <img src=x onerror=alert(1)>';inspectStudent(2);});await hoverFirst();
 assert.match(await page.locator('#student-detail').textContent(),/Ángela <img/);assert.match(await page.locator('#tooltip').textContent(),/Ángela <img/);assert.equal(await page.locator('#student-detail img,#tooltip img').count(),0);
 await page.evaluate(()=>{state.students[2].studentName=null;inspectStudent(2);});assert.ok((await page.locator('#student-detail').textContent()).includes(first.label));
 await page.evaluate(()=>{state.students[2].studentName='Ángela';go(2);inspectStudent(2);});await hoverFirst();assert.ok((await page.locator('#student-detail').textContent()).includes(first.label));assert.ok(!(await page.locator('#tooltip').textContent()).includes('Ángela'));
 for(const step of [3,4]){await page.evaluate(step=>{go(step);inspectStudent(2);},step);assert.ok((await page.locator('#student-detail').textContent()).includes(first.label));}
 await page.locator('#reset').click();await page.locator('#options-open').click();assert.equal(await page.evaluate(k=>localStorage.getItem(k),key),'0');
 await page.evaluate(k=>{localStorage.setItem(k,'2');reset();},key);assert.equal(await page.evaluate(k=>localStorage.getItem(k),key),'2');
 await page.evaluate(k=>{localStorage.setItem(k,'5');reset();},key);assert.equal(await page.evaluate(k=>localStorage.getItem(k),key),'5');await page.reload();await checkLock(page);
 // Clear this isolated test profile explicitly; lesson Reset cannot clear lockout.
 await page.evaluate(k=>localStorage.removeItem(k),key);await page.reload();await unlock(page);
 // Synthetic observations never inherit a real name, even in step 1.
 await page.evaluate(()=>{data.records=[{questionnaire_id:'fixture',student_name:'Actual Ángela',label:'Questionnaire fixture',grade:10,group_section:'A',values:{q11_height_cm:170},statuses:{}}];reset();go(2);go(1);inspectStudent(1);});
 assert.match(await page.locator('#student-detail').textContent(),/Generated 2/);assert.equal(await page.evaluate(()=>state.students.slice(1).every(s=>s.source==='synthetic'&&!s.studentName)),true);
 await page.reload();await unlock(page);
 // Shared navigation and focused removal regression checks.
 for(const id of ['next','options-next']){assert.equal(await page.locator('#'+id).isVisible(),true);assert.equal(await page.locator('#'+id).isDisabled(),true);}
 assert.equal(await page.locator('#options-help').count(),0);assert.equal(await page.locator('#options-titlebar').getAttribute('aria-describedby'),null);assert.equal(await page.getByText('Window instructions',{exact:true}).count(),0);
 await page.locator('#add-one').click();await page.locator('#options-next').click();assert.equal((await snapshot()).step,2);
 await page.locator('[data-add="100"]').click();await page.locator('[data-add="10"]').click(); // 109 actual + 2 synthetic
 const original=await page.evaluate(()=>state.students.map(s=>({id:s.questionnaire_id,height:s.height,source:s.source}))),model=await page.evaluate(()=>JSON.stringify(fit));
 await page.locator('[data-remove="1"]').click();assert.equal((await snapshot()).used,109);assert.equal((await snapshot()).synthetic,1);
 await page.locator('[data-remove="10"]').click();assert.equal((await snapshot()).n,100);assert.equal((await snapshot()).used,100);
 assert.deepEqual(await page.evaluate(()=>state.students.map(s=>({id:s.questionnaire_id,height:s.height,source:s.source}))),original.slice(0,100));
 await page.locator('[data-add="10"]').click();assert.deepEqual(await page.evaluate(()=>state.students.slice(100,109).map(s=>({id:s.questionnaire_id,height:s.height,source:s.source}))),original.slice(100,109));assert.equal((await snapshot()).synthetic,1);
 await page.locator('#histogram').click();await page.evaluate(()=>{inspectStudent(109);showTip('stale',{clientX:100,clientY:100});});
 await page.locator('[data-remove="100"]').click();assert.equal(await page.evaluate(()=>bins.reduce((n,b)=>n+b.count,0)),10);assert.equal(await page.locator('#inspect').inputValue(),'10');assert.equal(await page.locator('#tooltip').isHidden(),true);
 await page.evaluate(()=>remove(10000));assert.equal((await snapshot()).step,2);assert.equal((await snapshot()).n,0);assert.equal((await snapshot()).used,0);assert.equal(await page.locator('.bin').count(),0);
 for(const id of ['next','options-next'])assert.equal(await page.locator('#'+id).isDisabled(),true);
 assert.equal(await page.locator('[data-remove="1"]').isDisabled(),true);assert.match(await page.locator('#student-detail').textContent(),/No observations/);
 await page.locator('[data-add="10"]').click();await page.locator('#options-close').click();await page.locator('#next').click();assert.equal((await snapshot()).step,3);await page.locator('#options-open').click();assert.equal(await page.locator('#selection-help').isVisible(),true);
 const bounds=()=>page.evaluate(()=>{const N=state.students.length;return [state.sampling,state.ci].filter(Boolean).every(q=>q.size>=0&&q.size<=N&&q.start>=0&&q.start<=q.end&&q.end<=N&&(N===0?q.size===0&&q.end===0:q.size>=1&&q.start<q.end))&&[...selected].every(id=>state.students.some(s=>s.id===id));});
 await page.evaluate(()=>changeWindow(7,10));await page.locator('[data-remove="1"]').click();assert.equal(await bounds(),true);assert.equal(await page.evaluate(()=>state.sampling.end),9);
 await page.locator('[data-remove="100"]').click();assert.equal((await snapshot()).step,3);assert.equal((await snapshot()).selected,0);assert.equal(await bounds(),true);assert.equal(await page.locator('#window').isHidden(),true);assert.equal(await page.locator('#window-start').isDisabled(),true);
 await page.locator('#mode-random').click();await page.locator('[data-add="10"]').click();await page.locator('#sample-number').fill('10');await page.locator('#sample-number').dispatchEvent('input');await page.locator('[data-remove="1"]').click();assert.equal((await snapshot()).selected,9);assert.equal(await bounds(),true);
 await page.locator('#options-next').click();assert.equal((await snapshot()).step,4);for(const id of ['next','options-next','selection-help','remove-controls'])assert.equal(await page.locator('#'+id).isHidden(),true);
 await page.locator('[data-step="3"]').click();await page.locator('[data-remove="100"]').click();assert.equal(await bounds(),true);await page.locator('[data-add="1"]').click();assert.equal(await bounds(),true);assert.equal((await snapshot()).selected,1);assert.equal(await page.evaluate(()=>JSON.stringify(fit)),model);
 await page.locator('#options-close').click();await page.locator('#reset').click();await page.locator('#options-open').click();
 for(let i=0;i<20;i++)await page.locator('#add-one').click();assert.equal((await snapshot()).actual,20);assert.equal((await snapshot()).synthetic,0);
 await page.locator('[data-step="2"]').click();await page.locator('[data-add="100"]').click();let a=await snapshot();assert.equal(a.actual,109);assert.equal(a.synthetic,11);assert.match(await page.locator('#status').textContent(),/Source exhausted/);
 await page.locator('[data-add="1"]').click();await page.locator('[data-add="10"]').click();await page.locator('[data-add="1000"]').click();assert.equal((await snapshot()).n,1131);
 await page.locator('#histogram').click();await page.locator('#options-close').click();const bin=page.locator('.bin').filter({visible:true}).first();await bin.focus();await bin.press('Enter');assert.match(await bin.getAttribute('aria-label'),/actual.*generated/);assert.match(await bin.getAttribute('style'),/linear-gradient/);await bin.press('Escape');
 await page.screenshot({path:path.resolve('tmp/population-verification/histogram.png'),fullPage:true});
 await page.locator('[data-step="3"]').click();await page.locator('#window').focus();const windowBefore=await page.evaluate(()=>state.sampling.start);await page.locator('#window').press('ArrowRight');assert.equal(await page.evaluate(()=>state.sampling.start),windowBefore+1);await page.locator('#window').press('Shift+ArrowRight');
 const rect=await page.locator('#window').boundingBox();await page.mouse.move(rect.x+rect.width/2,rect.y+30);await page.mouse.down();await page.mouse.move(rect.x+rect.width/2+50,rect.y+30,{steps:5});await page.mouse.up();assert.ok(await page.evaluate(()=>state.sampling.start>1));
 await page.locator('#inspect').fill('1');await page.locator('#inspect').dispatchEvent('input');assert.match(await page.locator('#student-detail').textContent(),/actual/);await page.locator('#inspect').fill('110');await page.locator('#inspect').dispatchEvent('input');assert.match(await page.locator('#student-detail').textContent(),/synthetic/);await page.locator('#chart').focus();await page.locator('#chart').press('ArrowRight');assert.equal(await page.locator('#inspect').inputValue(),'111');
 await page.screenshot({path:path.resolve('tmp/population-verification/selection.png'),fullPage:true});
 await page.locator('#options-open').click();await page.locator('#mode-random').click();await page.locator('#sample-number').fill('30');await page.locator('#sample-number').dispatchEvent('input');assert.equal((await snapshot()).selected,30);assert.equal(await page.evaluate(()=>new Set(config().order.slice(0,config().size)).size),30);
 await page.locator('#redraw').click();await page.locator('[data-step="4"]').click();await page.locator('#why').evaluate(el=>el.open=true);await page.locator('#options-close').click();const before=await snapshot();await page.locator('[data-studies="10"]').click();await page.waitForFunction(()=>state.studies.length===10);const after=await snapshot();assert.deepEqual(after.ids,before.ids);assert.equal(after.used,before.used);assert.equal(after.fitN,before.fitN);
 await page.locator('#clear-studies').click();assert.equal((await snapshot()).studies,0);await page.locator('[data-studies="1"]').click();assert.equal((await snapshot()).studies,1);
 await page.locator('#options-open').click();await page.locator('[data-confidence="99"]').click();assert.equal((await snapshot()).studies,0);await page.locator('#options-close').click();await page.locator('[data-studies="1"]').click();await page.locator('#options-open').click();await page.locator('#sample-number').fill('20');await page.locator('#sample-number').dispatchEvent('input');assert.equal((await snapshot()).studies,0);assert.equal((await snapshot()).selected,20);await page.locator('#options-close').click();assert.ok(!/NaN|Infinity/.test(await page.locator('#formulas').textContent()));
 await page.locator('#variable').selectOption('q02_siblings');assert.equal((await snapshot()).n,0);assert.equal((await snapshot()).studies,0);await page.locator('#grade').selectOption('10');await page.locator('#group').selectOption('A');assert.equal((await snapshot()).fitN,await page.evaluate(()=>filtered.usable.length));assert.equal(await page.locator('#tooltip').isHidden(),true);
 await page.locator('[data-step="2"]').click();const ids=(await snapshot()).ids;await page.locator('#reset').click();await page.locator('[data-step="2"]').click();assert.deepEqual((await snapshot()).ids,ids);
 // Fixture datasets exercise UI degeneracy without modifying the workbook or exported asset.
 for(const values of [[],[5],[0,0,0],[1,2]]){
  await page.evaluate(values=>{data.records=values.map((v,i)=>({questionnaire_id:'fixture-'+i,label:'Anonymous '+i,grade:10,group_section:'A',values:{q02_siblings:v},statuses:{}}));reset();},values);
  if(!values.length){assert.equal(await page.locator('#add-one').isDisabled(),true);assert.match(await page.locator('#model-summary').textContent(),/No model fitted/);await page.locator('[data-step="4"]').click();assert.equal((await snapshot()).step,1);}
  else {await page.locator('[data-step="4"]').click();assert.equal((await snapshot()).actual,values.length);assert.equal((await snapshot()).synthetic,20-values.length);assert.ok(!/NaN|Infinity/.test(await page.locator('#formulas').textContent()));await page.locator('#why').evaluate(el=>el.open=true);await page.locator('[data-studies="1"]').click();assert.ok(!/NaN|Infinity/.test(await page.locator('#studies').getAttribute('viewBox')));}
 }
 await page.reload();await closed(page);await unlock(page);
 fs.mkdirSync(path.resolve('tmp/population-verification'),{recursive:true});
 for(const width of [1440,390,320]){
  await page.setViewportSize({width,height:1000});await page.locator('#variable').selectOption('q06_phone_annual_equivalent_24h_days_est');await page.locator('[data-step="4"]').click();if(await page.locator('#options-close').isVisible())await page.locator('#options-close').click();
  assert.equal(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth),true);
  const clipped=await page.locator('select').evaluateAll(els=>els.filter(el=>el.getBoundingClientRect().right>innerWidth).map(el=>el.id));assert.deepEqual(clipped,[]);
  await page.screenshot({path:path.resolve(`tmp/population-verification/${width}.png`),fullPage:true});
  await page.locator('[data-step="3"]').click();await page.locator('#options-open').click();await page.locator('#mode-window').click();
  const boxes=await page.locator('#window-controls > *').evaluateAll(els=>els.map(el=>{const r=el.getBoundingClientRect();return {x:r.x,y:r.y,right:r.right,bottom:r.bottom};}));
  assert.equal(await page.locator('#options-panel').evaluate(el=>el.scrollWidth<=el.clientWidth),true);assert.equal(await page.locator('.options-body').evaluate(el=>el.scrollWidth<=el.clientWidth),true);
  if(width===1440)assert.ok(boxes.every(b=>Math.abs((b.y+b.bottom)-(boxes[0].y+boxes[0].bottom))<2));
  assert.ok(boxes.every(b=>b.x>=0&&b.right<=width));
  await page.screenshot({path:path.resolve(`tmp/population-verification/options-${width}.png`),fullPage:true});
  await page.locator('#options-titlebar').focus();await page.locator('#options-titlebar').press('Home');await page.locator('#options-titlebar').press('ArrowLeft');await page.locator('#options-titlebar').press('Escape');assert.equal(await page.locator('#options-panel').isHidden(),true);assert.equal(await page.locator('#options-open').evaluate(el=>el===document.activeElement),true);
 }
 assert.deepEqual(errors,[]);console.log('Browser checks passed: password exactness, remaining attempts, durable lockout, reload/reopen, storage errors, deferred data/initialization, focus/keyboard, names/fallback/injection/synthetic/later anonymity, file://, all four steps, shared Next navigation, removal and queue rewind, empty/recovered selections, additions, exhaustion, bins, window controls, random samples, CIs, studies, filters, reset, edge fixtures, 1440/390/320px, no console errors.');await browser.close();
})().catch(e=>{console.error(e);process.exit(1);});
