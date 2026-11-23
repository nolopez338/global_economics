/* Pure browser/Node model and reveal primitives. See teacher/tools/population-simulation.md. */
(function(root,factory){const api=factory();if(typeof module==='object'&&module.exports)module.exports=api;else root.SurveySimulation=api;})(globalThis,function(){
'use strict';
function seeded(seed){let s=2166136261;for(const c of String(seed))s=Math.imul(s^c.charCodeAt(0),16777619);return()=>{s+=0x6D2B79F5;let t=s;t=Math.imul(t^t>>>15,t|1);t^=t+Math.imul(t^t>>>7,t|61);return((t^t>>>14)>>>0)/4294967296;};}
function shuffle(a,rng){for(let i=a.length-1;i>0;i--){const j=Math.floor(rng()*(i+1));[a[i],a[j]]=[a[j],a[i]];}return a;}
function filter(data,key,grade='',group=''){const matching=data.records.filter(r=>(!grade||String(r.grade)===String(grade))&&(!group||r.group_section===group));return {matching,usable:matching.filter(r=>typeof r.values[key]==='number'&&Number.isFinite(r.values[key]))};}
const phi=z=>Math.exp(-z*z/2)/Math.sqrt(2*Math.PI);
function cdf(z){if(z===Infinity)return 1;if(z===-Infinity)return 0;const x=Math.abs(z),t=1/(1+.2316419*x),p=1-phi(x)*t*(.319381530+t*(-.356563782+t*(1.781477937+t*(-1.821255978+t*1.330274429))));return z<0?1-p:p;}
function logDensity(x,c){return Math.log(c.w)-.5*Math.log(2*Math.PI*c.v)-(x-c.m)**2/(2*c.v);}
function likelihood(a,cs){return a.reduce((s,x)=>{const logs=cs.map(c=>logDensity(x,c)),max=Math.max(...logs);return s+max+Math.log(logs.reduce((t,l)=>t+Math.exp(l-max),0));},0);}
function fit(values){
 const n=values.length;if(!n)return {n,kind:'empty',components:[],mean:0,sd:0,note:'No usable values. Addition and studies are disabled.'};
 const mean=values.reduce((s,x)=>s+x,0)/n,v=values.reduce((s,x)=>s+(x-mean)**2,0)/n;
 if(v===0)return {n,kind:'constant',components:[{w:1,m:mean,v:0}],mean,sd:0,note:'Singleton or constant data: deterministic generator, no invented variation; nominal coverage is not applicable.'};
 const single=[{w:1,m:mean,v}],bic1=2*Math.log(n)-2*likelihood(values,single),floor=Math.max(v*1e-4,(Math.abs(mean)*Number.EPSILON*32)**2),sorted=[...values].sort((a,b)=>a-b);
 let best=null;
 if(n>=30)for(const [p,q] of [[.2,.8],[.3,.7],[.1,.6],[.4,.9],[.15,.85]]){
  let cs=[{w:.5,m:sorted[Math.floor((n-1)*p)],v},{w:.5,m:sorted[Math.floor((n-1)*q)],v}],old=-Infinity,converged=false,valid=true;
  for(let iter=0;iter<400;iter++){
   const sums=[0,0],means=[0,0],rs=[];
   for(const x of values){const l=cs.map(c=>logDensity(x,c)),mx=Math.max(...l),a=Math.exp(l[0]-mx),b=Math.exp(l[1]-mx),r=a/(a+b);rs.push(r);sums[0]+=r;sums[1]+=1-r;means[0]+=r*x;means[1]+=(1-r)*x;}
   if(sums.some(s=>s<Math.max(5,n*.05))){valid=false;break;}
   const next=cs.map((c,k)=>({w:sums[k]/n,m:means[k]/sums[k],v:0}));
   values.forEach((x,i)=>next.forEach((c,k)=>c.v+=(k?1-rs[i]:rs[i])*(x-c.m)**2/sums[k]));
   if(next.some(c=>c.v<=floor||!Number.isFinite(c.v))){valid=false;break;}
   cs=next;const ll=likelihood(values,cs);if(ll<old-1e-7){valid=false;break;}if(Math.abs(ll-old)<1e-8*(1+Math.abs(ll))){converged=true;break;}old=ll;
  }
  if(valid&&converged){const bic=5*Math.log(n)-2*likelihood(values,cs);if(!best||bic<best.bic)best={bic,cs};}
 }
 const mixture=best&&best.bic+6<bic1,cs=mixture?best.cs.sort((a,b)=>a.m-b.m):single;
 const overall=cs.reduce((s,c)=>s+c.w*c.m,0),variance=cs.reduce((s,c)=>s+c.w*(c.v+(c.m-overall)**2),0);
 return {n,kind:mixture?'two-component normal mixture':'single Gaussian',components:cs,mean:overall,sd:Math.sqrt(variance),bicSingle:bic1,bicMixture:best?.bic??null,note:n<30?'Fewer than 30 values: single Gaussian only.':mixture?'Mixture improves BIC by more than 6; converged components each have at least 5 values and 5% weight.':'Single Gaussian preferred: mixture unstable or BIC improvement ≤ 6.'};
}
function generator(model,field,rng=Math.random){
 const cs=model.components,domain=field.domain||[null,null],lo=domain[0]??-Infinity,hi=domain[1]??Infinity,integer=field.integer;
 if(model.kind==='empty')return {mean:0,sd:0,draw:()=>null,note:model.note};
 if(model.sd===0)return {mean:model.mean,sd:0,draw:()=>model.mean,note:model.note};
 const lower=integer?lo-.5:lo,upper=integer?hi+.5:hi;
 const masses=cs.map(c=>{const sd=Math.sqrt(c.v),a=(lower-c.m)/sd,b=(upper-c.m)/sd;return {c,sd,a,b,z:cdf(b)-cdf(a)};});
 const z=masses.reduce((s,t)=>s+t.c.w*t.z,0);
 let mean=0,second=0;
 if(integer){
  const min=Math.max(lo,Math.floor(Math.min(...cs.map(c=>c.m-10*Math.sqrt(c.v))))),max=Math.min(hi,Math.ceil(Math.max(...cs.map(c=>c.m+10*Math.sqrt(c.v)))));
  for(let x=min;x<=max;x++){const p=cs.reduce((s,c)=>s+c.w*(cdf((x+.5-c.m)/Math.sqrt(c.v))-cdf((x-.5-c.m)/Math.sqrt(c.v))),0)/z;mean+=x*p;second+=x*x*p;}
 }else for(const t of masses){const {c,sd,a,b}=t,pa=phi(a),pb=phi(b),az=Number.isFinite(a)?a*pa:0,bz=Number.isFinite(b)?b*pb:0;mean+=c.w*(c.m*t.z+sd*(pa-pb))/z;second+=c.w*((c.m*c.m+c.v)*t.z+2*c.m*sd*(pa-pb)+c.v*(az-bz))/z;}
 function draw(){for(;;){const u=rng();let cumulative=0,c=cs[cs.length-1];for(const candidate of cs){cumulative+=candidate.w;if(u<cumulative){c=candidate;break;}}const x=c.m+Math.sqrt(c.v)*Math.sqrt(-2*Math.log(Math.max(Number.MIN_VALUE,rng())))*Math.cos(2*Math.PI*rng());if(x<lower||x>upper)continue;const result=integer?Math.round(x):x;if(field.exclusiveMinimum&&result<=lo)continue;return result;}}
 return {mean,sd:Math.sqrt(Math.max(0,second-mean*mean)),draw,note:`Rejection outside ${lo} to ${hi}${field.exclusiveMinimum?' (lower bound excluded)':''}; ${integer?'round to nearest integer after rejection at half-integer limits':'continuous precision retained'}. Generator moments account for this transformation.`};
}
function queue(records,key,seed){const a=shuffle([...records],seeded(seed));let cursor=0;return {get used(){return cursor;},get length(){return a.length;},rewind(count){if(Number.isFinite(count))cursor=Math.max(0,cursor-Math.max(0,Math.floor(count)));},take(count,gen){if(!a.length)return [];return Array.from({length:count},()=>cursor<a.length?{source:'actual',record:a[cursor++],value:a[cursor-1].values[key]}:{source:'synthetic',record:null,value:gen.draw()});}};}
return {seeded,shuffle,filter,fit,generator,queue,cdf};
});
