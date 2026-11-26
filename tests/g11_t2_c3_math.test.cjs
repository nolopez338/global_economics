'use strict';
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const {model,cdf,invCdf} = require('../assets/js/g11_t2_c3_math.js');
const close=(a,b,tol=1e-12)=>assert.ok(Math.abs(a-b)<tol,`${a} differs from ${b}`);
const fixed=v=>v.toFixed(3);
// Original displayed examples, independently transcribed from the LaTeX source.
for(const [n,se,moe,l,u] of [
  [25,'6.000','11.760','72.240','95.760'],
  [400,'1.500','2.940','81.060','86.940'],
  [1600,'0.750','1.470','82.530','85.470']
]){
  const q=model(n,1.960);
  assert.deepEqual([q.se,q.moe,q.l,q.u].map(fixed),[se,moe,l,u]);
}
assert.equal(fixed(model(800,1.960).moe),'2.079');
assert.equal(fixed(model(800,1.960).se),'1.061');
const z=[1.282,1.645,1.960,2.576,3.291];
assert.deepEqual(z.map(v=>fixed(model(100,v).moe)),['3.846','4.935','5.880','7.728','9.873']);
assert.deepEqual(z.map(v=>model(100,v).coverage.toFixed(5)),['80.01574','90.00302','95.00042','99.00049','99.90017']);
let previous=Infinity;
for(let n=25;n<=1600;n++){
  const q=model(n,1.960);
  close((q.l+q.u)/2,84);close(84-q.l,q.u-84);
  assert.ok(q.moe<previous);previous=q.moe;
  if(n*4<=1600)close(model(n*4,1.960).se,q.se/2);
}
// Independent standard-normal reference values and inverse round trips.
for(const [x,p] of [[0,.5],[1,.8413447460685429],[1.96,.9750021048517795],[3,.9986501019683699],[4,.9999683287581669]]){
  close(cdf(x),p,3e-14);close(cdf(-x),1-p,3e-14);
}
for(let c=.8;c<=.999;c+=.0001)close(2*cdf(invCdf((1+c)/2))-1,c,2e-14);
assert.throws(()=>model(25.5,1.960),RangeError);
console.log('PASS: source checkpoints, all 1576 integer interval states, fixed centre, monotonic width, quadrupling, normal CDF and inverse.');
// Compile the actual content definitions without a browser. Check that overlays
// remain reveals within the 26 original frames, and compare the source order.
const root=path.resolve(__dirname,'..');
const source=fs.readFileSync(path.join(root,'assets/js/g11_t2_c3_slides.js'),'utf8');
const context={window:{G11C3Math:{model,cdf,invCdf}}};
vm.createContext(context);
vm.runInContext(source.slice(0,source.indexOf('  const state='))+'globalThis.lesson={slides,legend};})();',context);
const tex=fs.readFileSync(path.join(root,'book/grade11/term_2/3-slides/G11_T2_L1_C3_slides.tex'),'utf8');
const originalTitles=[...tex.matchAll(/\\begin\{frame\}(?:\[t\])?(?:\{([^}]+)\})?/g)].map((match,i)=>i===0?'Anatomy of a confidence interval':match[1]);
assert.equal(context.lesson.slides.length,26);
assert.deepEqual(Array.from(context.lesson.slides,s=>s.title),originalTitles);
assert.equal(context.lesson.legend.length,13);
for(const slide of context.lesson.slides){
  const revealLevels=[...slide.body.matchAll(/data-step="(\d+)"/g)].map(match=>+match[1]);
  assert.ok(revealLevels.every(level=>level<=slide.steps),`${slide.title}: inaccessible reveal`);
  for(let i=1;i<=slide.steps;i++)assert.ok(revealLevels.includes(i),`${slide.title}: missing step ${i}`);
}
const htmlPath=path.join(root,'grade11/src/pages/term2/g11-t2-C3-slides.html');
for(const match of fs.readFileSync(htmlPath,'utf8').matchAll(/(?:src|href)="([^"]+)"/g)){
  assert.ok(fs.existsSync(path.resolve(path.dirname(htmlPath),match[1])),`Missing dependency ${match[1]}`);
}
console.log('PASS: 26 source frame titles in order, 13 legend entries, all reveal levels reachable, local dependencies present.');
