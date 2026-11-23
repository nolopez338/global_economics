/* node --test --test-isolation=none teacher/tools/population-simulation-only.test.cjs */
const test=require('node:test'),assert=require('node:assert/strict'),fs=require('node:fs'),path=require('node:path'),vm=require('node:vm');
const root=path.resolve(__dirname,'../..'),read=p=>fs.readFileSync(path.join(root,p),'utf8');
const html=read('general_fundamentals/population_sample_simulation.html');
const script=html.match(/<script>([\s\S]*?)<\/script>/)[1];
test('both pages use the same Options controller while the public page stays self-contained',()=>{
 const controller=read('assets/js/options-panel.js').replace(/\r\n/g,'\n').trim();
 assert.ok(script.replace(/\r\n/g,'\n').includes(controller),'Keep the inline public controller synchronized with options-panel.js');
 assert.match(read('general_fundamentals/population_sample_simulation_restricted.html'),/<script src="\.\.\/assets\/js\/options-panel\.js"><\/script>/);
 assert.match(read('assets/js/population-simulation.js'),/initializeOptionsPanel\(\)/);
});
test('public simulation is self-contained, generated, and independent of survey assets and gate',()=>{
 assert.doesNotMatch(html,/survey|workbook|student_name|student_id|questionnaire|password|localStorage|fetch\s*\(|XMLHttpRequest|NAMES\s*=/i);
 assert.doesNotMatch(html,/<script[^>]+src=/i);
 assert.match(script,/name:`Generated \$\{order\+1\}`/);
 assert.match(html,/artificial population/);
 for(const match of html.matchAll(/(?:href|src)="([^"#]+)"/g))assert.ok(fs.existsSync(path.resolve(root,'general_fundamentals',match[1])),match[1]);
 new vm.Script(script);
});
test('restored normal generator has the declared moments and uses independent untruncated draws',()=>{
 const normal=script.match(/function normal\(\)\{[^\n]+/)[0];
 let seed=42;const math=Object.create(Math);math.random=()=>((seed=(1664525*seed+1013904223)>>>0)+.5)/4294967296;
 const context=vm.createContext({Math:math});vm.runInContext(`let MU=170,SIGMA=8;${normal};this.draw=normal;`,context);
 const values=Array.from({length:80000},()=>context.draw()),mean=values.reduce((a,b)=>a+b)/values.length,sd=Math.sqrt(values.reduce((s,x)=>s+(x-mean)**2,0)/values.length);
 assert.ok(Math.abs(mean-170)<.15);assert.ok(Math.abs(sd-8)<.12);
 vm.runInContext('MU=0;SIGMA=1',context);const draws=Array.from({length:100},()=>context.draw());assert.ok(draws.some(x=>x<0)&&draws.some(x=>x>0));
});
test('inverse normal critical values match confidence presets',()=>{
 const inverse=script.match(/function invNormal\(p\)\{[^\n]+/)[0],context=vm.createContext({});vm.runInContext(inverse,context);
 for(const [p,z] of [[.95,1.644853627],[.975,1.959963985],[.995,2.575829304],[.9995,3.290526731]])assert.ok(Math.abs(context.invNormal(p)-z)<1e-7);
});
test('restricted page retains deferred survey loading and local links resolve',()=>{
 const restricted=read('general_fundamentals/population_sample_simulation_restricted.html');
 assert.match(restricted,/<div id="lesson" hidden>/);assert.match(restricted,/id="password-form"/);
 assert.match(restricted,/src="\.\.\/assets\/js\/population-lesson-gate.js"/);
 assert.doesNotMatch(restricted,/<script[^>]+src="[^"]*survey_data/);
 for(const match of restricted.matchAll(/(?:href|src)="([^"#]+)"/g))assert.ok(fs.existsSync(path.resolve(root,'general_fundamentals',match[1])),match[1]);
 const gate=read('assets/js/population-lesson-gate.js');for(const match of gate.matchAll(/loadScript\('([^']+)'\)/g))assert.ok(fs.existsSync(path.resolve(root,'general_fundamentals',match[1])),match[1]);
 for(const file of ['grade11/src/G11_T2.html','grade11/src/G11_T3.html']){
  const links=[...read(file).matchAll(/href="([^"]*population_sample_simulation[^"#]*)"/g)];assert.equal(links.length,3);
  for(const [,href] of links){assert.ok(href.endsWith('/population_sample_simulation.html'));assert.ok(fs.existsSync(path.resolve(root,path.dirname(file),href)));}
 }
});
