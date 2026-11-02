/* Run from the repository root: node --test teacher/tools/survey-core.test.cjs */
const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const C = require('../assets/js/survey-core.js');
const XLSX = require('../assets/vendor/sheetjs/xlsx.full.min.js');
const source = path.resolve(__dirname, '../../assets/data/survey_data_extended.xlsx');
const bytes = fs.readFileSync(source);
const read = () => XLSX.read(bytes, {type:'buffer',cellDates:true,nodim:true});
const model = C.parseWorkbook(read(),XLSX);
const values = field => model.rows.map(r=>C.value(model,r,field,null)).filter(v=>v!==null);

test('null handling retains zero and negative fractional measurements',()=>{
  for(const v of [null,undefined,'','  ',NaN,Infinity,true,new Date()]) assert.equal(C.numeric(v),null);
  assert.equal(C.numeric(0),0); assert.equal(C.numeric('0'),0); assert.equal(C.numeric(-4.75),-4.75);
  assert.equal(C.stats([]).mean,null); assert.equal(C.stats([7]).sd,null);
  assert.equal(C.stats([7,7]).sd,0);
});
test('lower inclusive, upper exclusive, final upper inclusive; empty bins remain',()=>{
  const bins=C.histogram([0,1,1.5,3,4],[0,1,2,3,4]);
  assert.deepEqual(bins.map(b=>b.count),[1,2,0,2]);
  assert.equal(C.binIndex(1,[0,1,2]),1); assert.equal(C.binIndex(2,[0,1,2]),1);
  assert.equal(C.binIndex(-1,[0,1,2]),-1);
  assert.ok(Math.abs(bins.reduce((s,b)=>s+b.percent,0)-100)<1e-10);
});
test('integer-centered bins and exercise domain retain zero and seven',()=>{
  const edges=C.binEdges([0,3,7],{width:1,integer:true,domain:[0,7]});
  assert.deepEqual(edges,[-.5,.5,1.5,2.5,3.5,4.5,5.5,6.5,7.5]);
  assert.equal(C.histogram([0,3,7],edges).reduce((s,b)=>s+b.count,0),3);
});
test('automatic fallback handles small, constant, zero-IQR and fractional data',()=>{
  for(const v of [[3],[3,3,3],[0,0,0,0,9],[-10,-4.75,0,10]]){
    const edges=C.binEdges(v,{mode:'auto'});assert.ok(edges.length>=2);
    assert.equal(C.histogram(v,edges).reduce((s,b)=>s+b.count,0),v.length);
    for(let i=1;i<edges.length;i++)assert.ok(edges[i]>edges[i-1]);
  }
  assert.deepEqual(C.binEdges([],{mode:'auto'}),[]);
  assert.throws(()=>C.binEdges([0,100],{width:.0001}),/2,000/);
});
test('origin expands backward rather than dropping observations',()=>{
  const values=[-10,-2,0,10],edges=C.binEdges(values,{width:2,origin:3});
  assert.ok(edges[0]<=-10); assert.equal(C.histogram(values,edges).reduce((s,b)=>s+b.count,0),4);
});
test('requested bin count is exact without an explicit origin',()=>{
  const edges=C.binEdges([3,3.5,7,11],{mode:'count',count:7});
  assert.equal(edges.length,8);assert.equal(edges[0],3);assert.equal(edges.at(-1),11);
});
test('OR within groups; AND across dimensions; empty means empty',()=>{
  const all=new Set(model.classes);
  assert.equal(C.filterRows(model.rows,{classes:new Set()}).length,0);
  assert.equal(C.filterRows(model.rows,{grades:new Set()}).length,0);
  assert.equal(C.filterRows(model.rows,{classes:new Set(['10A','10B'])}).length,39);
  assert.equal(C.filterRows(model.rows,{grades:new Set(['11']),classes:new Set(['10A'])}).length,0);
  assert.equal(C.filterRows(model.rows,{classes:all}).length,206);
  assert.equal(C.filterRows(model.rows,{categories:[{field:'grade',values:new Set()}]}).length,0);
  assert.ok(C.filterRows(model.rows,{ranges:[{field:'q02_siblings',min:0,max:0}]}).length>0);
});
test('one-record filters work; statistics have no fabricated sample deviation',()=>{
  const r=model.rows[0];const rows=C.filterRows(model.rows,{categories:[{field:'questionnaire_id',values:new Set([r.questionnaire_id])}]});
  assert.equal(rows.length,1);assert.equal(C.stats([r.q05_sleep_hours]).sd,null);
});
test('complete rankings allow unknown unselected options; partial choices are retained',()=>{
  const fields=['a','b','c','d'];
  assert.equal(C.ranking({a:1,b:2,c:3,d:null},fields).state,'complete');
  assert.deepEqual(C.ranking({a:0,b:2,c:null,d:null},fields),{state:'partial',choices:[null,'b',null]});
  for(const row of [{a:1,b:1},{a:4},{a:1,b:1.5},{a:null},{a:0,b:0},{a:'garbled'}])assert.equal(C.ranking(row,fields).state,'unavailable');
});
test('actual source matches unique questionnaire and class benchmarks',()=>{
  assert.equal(model.rows.length,206);assert.equal(model.headers.length,158);
  assert.equal(new Set(model.rows.map(r=>r.questionnaire_id)).size,206);
  assert.deepEqual(Object.fromEntries(model.classes.map(cl=>[cl,model.rows.filter(r=>r.class_label===cl).length])),{'10A':17,'10B':22,'10C':22,'10D':19,'10E':22,'11A':20,'11B':19,'11C':20,'11D':23,'11E':22});
  assert.equal(values('q05_sleep_hours').length,201);assert.equal(values('q11_height_cm').length,109);
  assert.equal(values('q09_math_enjoyment').length,200);assert.equal(Math.min(...values('q09_math_enjoyment')),-10);assert.equal(Math.max(...values('q09_math_enjoyment')),10);
});
test('all numeric variables and shared comparison bins reconcile counts and percentages',()=>{
  for(const m of model.meta.filter(m=>m.kind==='numeric')){
    const vs=values(m.field),edges=C.binEdges(vs,{mode:m.width?'width':'auto',width:m.width,integer:m.integer,domain:m.domain});
    const bins=C.histogram(vs,edges);assert.equal(bins.reduce((s,b)=>s+b.count,0),vs.length,m.field);
    if(vs.length)assert.ok(Math.abs(bins.reduce((s,b)=>s+b.percent,0)-100)<1e-9,m.field);
    for(const cl of model.classes){const v=model.rows.filter(r=>r.class_label===cl).map(r=>C.value(model,r,m.field,null)).filter(v=>v!==null),b=C.histogram(v,edges);assert.deepEqual(b.map(b=>[b.lo,b.hi]),bins.map(b=>[b.lo,b.hi]));assert.equal(b.reduce((s,b)=>s+b.count,0),v.length);if(v.length)assert.ok(Math.abs(b.reduce((s,b)=>s+b.percent,0)-100)<1e-9);}
  }
});
test('source zeros, anomalous age, and zero-denominator ratio are preserved correctly',()=>{
  assert.ok(values('q02_siblings').includes(0));assert.ok(values('q09_math_enjoyment').includes(0));assert.ok(values('q01_age_completed_years').includes(0));
  const zeros=model.rows.filter(r=>C.numeric(r.q08_study_minutes)===0);assert.ok(zeros.length>0);
  zeros.forEach(r=>{assert.equal(C.value(model,r,'phone_to_homework_minutes_ratio',null),null);if(C.numeric(r.q06_phone_hours)!==null)assert.notEqual(C.value(model,r,'phone_minus_homework_minutes',null),null);});
});
test('quality applies to active field and documented dependencies, not unrelated answers',()=>{
  const row=model.rows.find(r=>C.numeric(r.q05_sleep_hours)!==null&&C.numeric(r.q11_height_cm)===null);
  assert.notEqual(C.value(model,row,'q05_sleep_hours',new Set(model.statuses)),null);
  assert.equal(C.value(model,row,'q05_sleep_hours',new Set()),null);
  assert.equal(C.sourceStatuses(model,row,'q05_sleep_minutes_school_night')[0].field,'q05_sleep_hours');
  assert.equal(C.sourceStatuses(model,row,'phone_minus_homework_minutes').length,2);
});
test('first-choice quality does not filter unrelated second-choice answers',()=>{
  const fields=['a_rank','b_rank','c_rank'];
  const r={questionnaire_id:'one',a_rank:1,b_rank:2,c_rank:3};
  const key=(id,f)=>id+'\u0000'+f;
  const m={questionFields:()=>fields,key,meta:[],dict:new Map(fields.map(f=>[f,{'Answer / option':f}])),status:new Map(fields.map((f,i)=>[key('one',f),{final_status:i===1?'corrected':'observed'}]))};
  assert.equal(C.rankingSeries(m,[r],16,'1','all',new Set(['observed'])).denom,1);
  assert.equal(C.rankingSeries(m,[r],16,'2','all',new Set(['observed'])).denom,0);
});
test('ranking denominators are specific to rank and eligibility; points remain points',()=>{
  for(const q of [16,17,18]){
    for(const mode of ['1','2','3','top','split','points']){
      const s=C.rankingSeries(model,model.rows,q,mode,'all',null);
      assert.equal(s.states.complete+s.states.partial+s.states.unavailable,206);assert.ok(s.states.partial>0);
      if(['1','2','3'].includes(mode)){assert.equal(s.data.reduce((a,b)=>a+b.count,0),s.denom);assert.ok(Math.abs(s.data.reduce((a,b)=>a+b.percent,0)-100)<1e-9);}
      if(mode==='top'||mode==='split'){assert.equal(s.denom,s.eligible.length);assert.ok(s.data.reduce((a,b)=>a+b.percent,0)>100);}
      if(mode==='points')assert.equal(s.data.reduce((a,b)=>a+b.count,0),s.eligible.reduce((sum,x)=>sum+x.rank.choices.reduce((s,f,i)=>s+(f?3-i:0),0),0));
    }
    const complete=C.rankingSeries(model,model.rows,q,'1','complete',null),partial=C.rankingSeries(model,model.rows,q,'1','partial',null);
    assert.equal(complete.eligible.length,complete.states.complete);assert.equal(partial.eligible.length,partial.states.partial);
  }
});
test('worksheet dimension metadata is optional and headers need not be at fixed positions',()=>{
  const wb=read();for(const s of Object.values(wb.Sheets))delete s['!ref'];
  assert.equal(C.parseWorkbook(wb,XLSX).rows.length,206);
  const rows=C.sheetRows(wb.Sheets['Clean answers'],XLSX).map(r=>[...r].reverse());wb.Sheets['Clean answers']=XLSX.utils.aoa_to_sheet(rows);
  const reordered=C.parseWorkbook(wb,XLSX);assert.equal(reordered.rows[0].questionnaire_id,model.rows[0].questionnaire_id);assert.equal(reordered.rows[0].q05_sleep_hours,model.rows[0].q05_sleep_hours);
});
test('missing sheets, required headers, duplicate questionnaire and status keys fail clearly',()=>{
  let wb=read();delete wb.Sheets.Audit;assert.throws(()=>C.parseWorkbook(wb,XLSX),/worksheet missing: Audit/);
  wb=read();wb.Sheets['Clean answers'].A1.v='wrong';assert.throws(()=>C.parseWorkbook(wb,XLSX),/missing required headers/);
  wb=read();wb.Sheets['Clean answers'].A3.v=wb.Sheets['Clean answers'].A2.v;assert.throws(()=>C.parseWorkbook(wb,XLSX),/unique/);
  wb=read();wb.Sheets['Answer status'].B3.v=wb.Sheets['Answer status'].B2.v;assert.throws(()=>C.parseWorkbook(wb,XLSX),/Duplicate Answer status key/);
});
