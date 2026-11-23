/* node --test teacher/tools/population-simulation.test.cjs */
const test=require('node:test'),assert=require('node:assert/strict'),fs=require('node:fs');
const {convert,serialize}=require('./export-survey-simulation.cjs');
const D=require('../../assets/data/survey_data_extended.js'),E=require('../../assets/js/survey-simulation-core.js');
const X=require('../assets/vendor/sheetjs/xlsx.full.min.js'),C=require('../assets/js/survey-core.js');
const bytes=fs.readFileSync(require('node:path').join(__dirname,'../../assets/data/survey_data_extended.xlsx'));
const workbook=C.parseWorkbook(X.read(bytes,{type:'buffer',cellDates:true}),X);
test('export is reproducible, keyed by questionnaire, names joined by questionnaire and reconciled against every workbook value',()=>{
 assert.deepEqual(convert(bytes),D);assert.equal(D.records.length,206);assert.equal(D.referenceDate,'2026-11-01');assert.equal(new Set(D.records.map(r=>r.questionnaire_id)).size,206);
 for(const r of D.records){const row=workbook.rows.find(x=>x.questionnaire_id===r.questionnaire_id);assert.equal(r.student_name,typeof row.student_name==='string'?row.student_name.trim()||null:null);assert.equal(r.grade,row.grade);assert.equal(r.group_section,row.group_section);for(const f of D.fields){const v=r.values[f.key];if(v!==null)assert.deepEqual(v,row[f.key] instanceof Date?row[f.key].toISOString().slice(0,10):row[f.key]);}}
 const text=serialize(D);assert.ok(text.includes('student_name'));assert.ok(!text.includes('student_id'));
 for(const r of workbook.rows){if(r.student_id)assert.ok(!text.includes('"'+r.student_id+'"'));}
 assert.equal(D.records[0].values.q02_siblings,0);assert.equal(D.records[0].values.q11_height_cm,null);assert.equal(D.records[1].values.q11_height_cm,172);assert.equal(D.records[1].values.q04_one_way_hours,1/3);
 assert.equal(D.records[1].values.q05_sleep_share_of_24_hours,1/3);assert.equal(D.fields.find(f=>f.key==='q05_sleep_share_of_24_hours').unit,'fraction of 1');
 assert.ok(D.fields.filter(f=>/_rank$|_selected$|birth_weekday|enjoyment/.test(f.key)).every(f=>f.normalModeling==='unsupported'));
});
test('grade/group counts match source, group letters span both grades, filters independently fit actuals',()=>{
 for(const key of D.fields.filter(f=>f.normalModeling!=='unsupported').map(f=>f.key))for(const grade of ['',10,11])for(const group of ['','A','B','C','D','E','Z']){
  const a=E.filter(D,key,grade,group),expected=workbook.rows.filter(r=>(!grade||r.grade===grade)&&(!group||r.group_section===group));assert.equal(a.matching.length,expected.length);
  const fit=E.fit(a.usable.map(r=>r.values[key]));assert.equal(fit.n,a.usable.length);if(fit.n)assert.ok(Math.abs(fit.mean-a.usable.reduce((s,r)=>s+r.values[key],0)/fit.n)<1e-7);
 }
 assert.equal(E.filter(D,'q11_height_cm').usable.length,109);assert.equal(E.filter(D,'q05_sleep_hours').usable.length,201);
 assert.deepEqual([...new Set(E.filter(D,'q11_height_cm','','A').matching.map(r=>r.grade))].sort(),[10,11]);
});
test('seeded queue preserves equal-valued records, crossing batches, reset, and independence from studies',()=>{
 const a=E.filter(D,'q02_siblings').usable,g={draw:()=>42},q=E.queue(a,'q02_siblings','seed'),first=q.take(10,g);
 assert.ok(first.every(x=>x.source==='actual'));const used=q.used;for(let i=0;i<100;i++)g.draw();assert.equal(q.used,used);
 const batch=q.take(a.length-10+17,g),all=[...first,...batch];assert.equal(all.filter(x=>x.source==='actual').length,a.length);assert.equal(all.filter(x=>x.source==='synthetic').length,17);assert.ok(all.slice(0,a.length).every(x=>x.source==='actual'));assert.equal(new Set(all.slice(0,a.length).map(x=>x.record.questionnaire_id)).size,a.length);
 assert.deepEqual(E.queue(a,'q02_siblings','seed').take(10,g),first);assert.notDeepEqual(E.queue(a,'q02_siblings','different').take(10,g),first);assert.deepEqual(E.queue([],'x','seed').take(10,g),[]);
});
test('empty, singleton, constants, tiny samples and stable deterministic mixture selection',()=>{
 assert.equal(E.fit([]).kind,'empty');for(const a of [[0],[7],[0,0,0],[7,7]]){const m=E.fit(a),g=E.generator(m,{domain:[0,null],integer:true});assert.equal(m.sd,0);assert.equal(g.draw(),a[0]);assert.equal(g.sd,0);}
 assert.equal(E.fit([1,2,3]).kind,'single Gaussian');
 const rng=E.seeded('two modes'),values=Array.from({length:300},(_,i)=>(i%2?10:-10)+Math.sqrt(-2*Math.log(rng()))*Math.cos(2*Math.PI*rng()));const m=E.fit(values);assert.equal(m.kind,'two-component normal mixture');assert.deepEqual(m,E.fit(values));assert.ok(m.components.every(c=>c.w>.05&&c.v>0));
});
test('transformed generator moments match independent draws for normal, mixture, bounded, integer variables',()=>{
 for(const key of ['q11_height_cm','q02_siblings','q05_sleep_hours','q07_exercise_days','q04_commute_minutes','q14_phone_free_days']){
  const f=D.fields.find(f=>f.key===key),fit=E.fit(E.filter(D,key).usable.map(r=>r.values[key])),g=E.generator(fit,f,E.seeded(key));let s=0,s2=0,n=80000;
  for(let i=0;i<n;i++){const x=g.draw();assert.ok(x>=f.domain[0]&&(f.domain[1]===null||x<=f.domain[1]));if(f.integer)assert.ok(Number.isInteger(x));s+=x;s2+=x*x;}
  const mean=s/n,sd=Math.sqrt(s2/n-mean*mean);assert.ok(Math.abs(mean-g.mean)<6*g.sd/Math.sqrt(n)+1e-7,key+' mean');assert.ok(Math.abs(sd-g.sd)<g.sd*.035+1e-7,key+' sd');
 }
 const model={kind:'single Gaussian',components:[{w:1,m:0,v:1}],mean:0,sd:1},g=E.generator(model,{domain:[0,1],integer:false},E.seeded('truncated'));assert.ok(Math.abs(g.mean-.459862)<1e-5);assert.ok(Math.abs(g.sd-.282227)<1e-5);
});

test('rewinding actual reveals restores the seeded suffix before synthetic generation',()=>{
 const records=E.filter(D,'q11_height_cm').usable,g={draw:()=>42},q=E.queue(records,'q11_height_cm','rewind');
 const original=q.take(records.length+3,g);q.rewind(0);assert.equal(q.used,records.length);
 q.rewind(7);assert.equal(q.used,records.length-7);
 const again=q.take(10,g);assert.deepEqual(again.slice(0,7),original.slice(records.length-7,records.length));assert.ok(again.slice(7).every(x=>x.source==='synthetic'));
 q.rewind(10000);assert.equal(q.used,0);assert.deepEqual(q.take(records.length,g),original.slice(0,records.length));
 q.rewind(-1);q.rewind(NaN);assert.equal(q.used,records.length);
 const empty=E.queue([],'x','empty');empty.rewind(100);assert.equal(empty.used,0);assert.deepEqual(empty.take(10,g),[]);
});

// Reorder source records, including equal values and incomplete student IDs.
// Missing and hostile names must survive conversion as data, never markup.
test('name join survives reordered questionnaire rows and missing names without student IDs',()=>{
 const wb=X.read(bytes,{type:'buffer',cellDates:true});
 const rows=C.sheetRows(wb.Sheets['Clean answers'],X),headers=rows[0],id=headers.indexOf('questionnaire_id'),name=headers.indexOf('student_name'),studentId=headers.indexOf('student_id');
 const original=rows.slice(1),target=original[3][id],missing=original[4][id];
 const reordered=original.reverse().map(r=>{r[studentId]=null;if(r[id]===target)r[name]='Ángela <img src=x onerror=alert(1)>';if(r[id]===missing)r[name]=' ';return r;});
 wb.Sheets['Clean answers']=X.utils.aoa_to_sheet([headers,...reordered]);
 const out=convert(X.write(wb,{type:'buffer',bookType:'xlsx'}));
 for(const r of out.records){const row=reordered.find(x=>x[id]===r.questionnaire_id);assert.equal(r.student_name,String(row[name]||'').trim()||null);}
 assert.equal(out.records.find(r=>r.questionnaire_id===target).student_name,'Ángela <img src=x onerror=alert(1)>');
 assert.equal(out.records.find(r=>r.questionnaire_id===missing).student_name,null);
 assert.ok(serialize(out).includes('\\u003cimg'));assert.ok(!serialize(out).includes('<img'));
});
