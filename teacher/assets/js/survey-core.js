/* Survey analysis primitives. Browser + Node, no DOM or network dependencies. */
(function (root, factory) {
  const api = factory();
  if (typeof module === 'object' && module.exports) module.exports = api;
  else root.SurveyCore = api;
})(typeof globalThis !== 'undefined' ? globalThis : this, function () {
  'use strict';
  const unavailable = new Set(['missing', 'corrupted', 'not_applicable', 'not_collected', 'unresolved_evidence']);
  const blank = v => v === null || v === undefined || (typeof v === 'string' && !v.trim());
  const numeric = v => blank(v) || typeof v === 'boolean' || v instanceof Date ? null : (Number.isFinite(Number(v)) ? Number(v) : null);
  const weekdays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'];
  function measurement(field, v) {
    if (field !== 'q01_birth_weekday') return numeric(v);
    const day = weekdays.findIndex(day => day.toLowerCase() === String(v ?? '').trim().toLowerCase());
    if (day >= 0) return day + 1;
    const code = numeric(v);
    return Number.isInteger(code) && code >= 1 && code <= 7 ? code : null;
  }
  const title = s => s.replace(/^q\d+_/, '').replace(/_/g, ' ').replace(/\best\b/g, 'estimated').replace(/\bapprox\b/g, 'approximate').replace(/^./, c => c.toUpperCase());
  const originals = {
    q02_siblings: ['Number of siblings', 'count', 1, true], q03_pets: ['Number of pets', 'count', 1, true],
    q04_commute_minutes: ['Home-to-school commute', 'minutes', 10], q05_sleep_hours: ['Sleep on a school night', 'hours', .5],
    q06_phone_hours: ['Recreational phone use', 'hours/day', .5], q07_exercise_days: ['Days with ≥30 minutes of exercise', 'days/week', 1, true, [0, 7]],
    q08_study_minutes: ['Weekday study / homework', 'minutes', 30], q09_math_enjoyment: ['Math enjoyment', 'score (−10 to +10)', 1, false, [-10, 10]],
    q10_countries: ['Countries visited', 'count', 1, true], q11_height_cm: ['Height', 'cm', 5], q12_books: ['Books read (period unspecified)', 'count', 20],
    q13_first_phone_age: ['Age at first phone', 'years', 1], q14_phone_free_days: ['Longest phone break', 'days', 30], q15_daily_apps: ['Different apps used per day', 'count', 1, true]
  };
  const topic = field => {
    const q = Number((field.match(/^q(\d+)/) || [])[1]);
    return q === 1 ? 'Age & birthdays' : [2,3].includes(q) ? 'Household' : [4,11].includes(q) ? 'Travel & height' : [5,7].includes(q) ? 'Sleep & exercise' : [6,13,14,15].includes(q) ? 'Phone & technology' : [8,9].includes(q) ? 'Learning & study' : [10,12].includes(q) ? 'Experiences & reading' : 'Phone & homework';
  };
  function sheetRows(sheet, XLSX) {
    // Recover actual populated extents, including files without <dimension>.
    const cells = Object.keys(sheet).filter(k => /^[A-Z]+[1-9]\d*$/.test(k));
    if (!cells.length) return [];
    let maxR = 0, maxC = 0;
    cells.forEach(k => { const p = XLSX.utils.decode_cell(k); maxR = Math.max(maxR,p.r); maxC = Math.max(maxC,p.c); });
    const range={s:{r:0,c:0},e:{r:maxR,c:maxC}};
    return XLSX.utils.sheet_to_json({...sheet,'!ref':XLSX.utils.encode_range(range)}, {header:1, raw:true, defval:null, range, blankrows:false});
  }
  function table(rows, required, name) {
    const index = rows.findIndex(r => required.every(h => r.includes(h)));
    if (index < 0) throw new Error(`${name}: missing required headers: ${required.join(', ')}`);
    const headers = rows[index].map(v => String(v ?? '').trim());
    if (new Set(headers.filter(Boolean)).size !== headers.filter(Boolean).length) throw new Error(`${name}: duplicate column headers.`);
    return {headers, rows:rows.slice(index+1).filter(r => r.some(v=>!blank(v))).map(r => Object.fromEntries(headers.filter(Boolean).map(h=>[h,r[headers.indexOf(h)] ?? null])))};
  }
  function parseWorkbook(wb, XLSX) {
    const specs = {
      'Clean answers':['questionnaire_id','grade','group_section',...Object.keys(originals)],
      'Answer status':['questionnaire_id','answer_column','original_condition','final_status','transformation_method'],
      'Audit':['questionnaire_id','field','original_value','result','reason','source_reference'],
      'Derivation config':['Setting','Value','Meaning'],
      'Derived dictionary':['Field','Source questions','Units','Classification','Calculation and assumptions'],
      'Derived issues':['Questionnaire ID','Field','Issue','Recorded value','Handling'],
      'Data dictionary':['Column','Answer / option','Data type','Unit / encoding','Allowed values / meaning']
    };
    const sheets = {};
    for (const [name, headers] of Object.entries(specs)) {
      if (!wb.Sheets[name]) throw new Error(`Required worksheet missing: ${name}`);
      sheets[name] = table(sheetRows(wb.Sheets[name],XLSX),headers,name);
    }
    const rows = sheets['Clean answers'].rows, headers=sheets['Clean answers'].headers;
    const ids = new Set();
    rows.forEach(r=>{ if(blank(r.questionnaire_id) || ids.has(String(r.questionnaire_id))) throw new Error('Questionnaire IDs must be nonblank and unique.'); r.questionnaire_id=String(r.questionnaire_id); ids.add(r.questionnaire_id); r.class_label=`${r.grade}${r.group_section}`; });
    const dict = new Map(sheets['Data dictionary'].rows.filter(r=>/^q\d{2}_/.test(r.Column)).map(r=>[r.Column,r]));
    const derived = new Map(sheets['Derived dictionary'].rows.map(r=>[r.Field,r]));
    const requiredFields = [...dict.keys(),...derived.keys()];
    const absent=requiredFields.filter(f=>!headers.includes(f));
    if(absent.length) throw new Error(`Clean answers is missing dictionary fields: ${absent.join(', ')}`);
    const noDefinition=headers.filter(f=>(Object.hasOwn(originals,f)||f==='q01_date_of_birth'||f.endsWith('_rank'))&&!dict.has(f));
    if(noDefinition.length)throw new Error(`Data dictionary is missing original question definitions: ${noDefinition.join(', ')}`);
    const status = new Map(), audit = new Map(), issues=new Map(), warnings=[];
    const key=(id,f)=>`${id}\u0000${f}`;
    for(const s of sheets['Answer status'].rows) {
      const k=key(s.questionnaire_id,s.answer_column);
      if(status.has(k)) throw new Error(`Duplicate Answer status key: ${s.questionnaire_id} / ${s.answer_column}`);
      status.set(k,s);
    }
    for(const [name,map,idField,field] of [['Audit',audit,'questionnaire_id','field'],['Derived issues',issues,'Questionnaire ID','Field']]) {
      for(const r of sheets[name].rows) { const k=key(r[idField],r[field]); if(!map.has(k))map.set(k,[]); map.get(k).push(r); }
    }
    for(const name of ['Answer status','Audit','Derived issues']) {
      const idField=name==='Derived issues'?'Questionnaire ID':'questionnaire_id';
      const orphans=sheets[name].rows.filter(r=>!ids.has(String(r[idField]))).length;
      if(orphans) warnings.push(`${name}: ${orphans} supplementary rows have unknown questionnaire IDs.`);
    }
    const questionFields=q=>[...dict.keys()].filter(f=>new RegExp(`^q${String(q).padStart(2,'0')}_`).test(f)&&!f.endsWith('_text'));
    const meta=[];
    for(const [field,v] of Object.entries(originals)) meta.push({field,label:v[0],unit:v[1],width:v[2],integer:!!v[3],domain:v[4],kind:'numeric',topic:topic(field),dependencies:[field],classification:'Original measurement',description:dict.get(field)?.['Allowed values / meaning']||''});
    const excluded = new Set(['q01_age_years_months_days','q01_next_birthday','q11_height_feet','q11_height_remaining_inches','q13_first_phone_year_earliest','q13_first_phone_year_latest']);
    const numericUnits=new Set(['years','days','weeks','months','day of year','hours','minutes/day','hours/5 school days','minutes/night','percentage','hours/5 nights','hours/week','hours/365 days','24-hour days/365 days','days/week','minimum minutes/week','hours/weekday','hours/5 weekdays','score 0–100','meters','inches','approximate years','ratio','minutes']);
    for(const [field,d] of derived) {
      if(/^q1[678]_/.test(field)||excluded.has(field))continue;
      const unit=d.Units, category=['category','weekday','quarter','0/1'].includes(unit);
      if(!category&&!numericUnits.has(unit))continue;
      const dependencies=[...String(d['Source questions']).matchAll(/Q(\d+)/g)].flatMap(m=>questionFields(Number(m[1])));
      const percent=unit==='percentage';
      const completedAge=['q01_age_completed_years','q01_age_at_next_birthday'].includes(field);
      meta.push({field,label:title(field)+(d.Classification==='estimated'?' (estimate / projection)':''),unit:percent?'%':unit,width:completedAge||field==='q07_nonqualifying_days'?1:null,integer:/completed|days_lived|days_until|age_at_next/.test(field)||field==='q07_nonqualifying_days',domain:field==='q07_nonqualifying_days'?[0,7]:null,kind:category?'categorical':'numeric',topic:topic(field),dependencies,scale:percent?100:1,classification:d.Classification,description:d['Calculation and assumptions']});
      if (field === 'q01_birth_weekday') Object.assign(meta[meta.length - 1], {
        kind:'numeric', width:1, integer:true, domain:[1,7],
        description:'Birth weekday encoded as Monday=1, Tuesday=2, Wednesday=3, Thursday=4, Friday=5, Saturday=6, Sunday=7. Weekday codes repeat cyclically each week.'
      });
    }
    const config=sheets['Derivation config'].rows;
    if(!config.some(r=>r.Setting==='Survey reference date'))throw new Error('Derivation config: reference date missing.');
    const model={rows,headers,dict,derived,meta,status,audit,issues,config,key,warnings,questionFields};
    model.statuses=[...new Set([...status.values()].map(s=>s.final_status).filter(s=>!blank(s)))].sort();
    model.classes=[...new Set(rows.map(r=>r.class_label))].sort(); model.grades=[...new Set(rows.map(r=>String(r.grade)))].sort();
    return model;
  }
  function sourceStatuses(model,row,field) {
    const direct=model.status.get(model.key(row.questionnaire_id,field));
    if(direct)return [{field,...direct}];
    const m=model.meta.find(m=>m.field===field);
    return (m?.dependencies||[]).map(f=>{const s=model.status.get(model.key(row.questionnaire_id,f));return s?{field:f,...s}:null;}).filter(Boolean);
  }
  function qualityPass(model,row,field,allowed) {
    const ss=sourceStatuses(model,row,field);
    return ss.every(s=>!unavailable.has(s.final_status) && (!allowed || allowed.has(s.final_status)));
  }
  function value(model,row,field,allowed) {
    if(!qualityPass(model,row,field,allowed))return null;
    if(field==='phone_to_homework_minutes_ratio' && numeric(row.q08_study_minutes)===0)return null;
    const v=measurement(field,row[field]); return v===null?null:v*(model.meta.find(m=>m.field===field)?.scale||1);
  }
  function filterRows(rows, f) {
    return rows.filter(r=>(!f.grades || f.grades.has(String(r.grade))) && (!f.classes || f.classes.has(r.class_label)) && (!f.ranges || f.ranges.every(a=>{const v=measurement(a.field,r[a.field]);return v!==null&&(a.min===null||v>=a.min)&&(a.max===null||v<=a.max);})) && (!f.categories || f.categories.every(a=>a.values.has(String(r[a.field])))));
  }
  function quantile(sorted,p) { if(!sorted.length)return null; const i=(sorted.length-1)*p,j=Math.floor(i);return sorted[j]+(sorted[Math.ceil(i)]-sorted[j])*(i-j); }
  function stats(values) {
    const a=[...values].sort((a,b)=>a-b), n=a.length;
    const mean=n?a.reduce((s,x)=>s+x,0)/n:null;
    return {n,mean,median:quantile(a,.5),min:n?a[0]:null,max:n?a[n-1]:null,q1:quantile(a,.25),q3:quantile(a,.75),sd:n>1?Math.sqrt(a.reduce((s,x)=>s+(x-mean)**2,0)/(n-1)):null};
  }
  function binEdges(values, opts={}) {
    if(!values.length)return [];
    const s=stats(values), lo=opts.domain?Math.min(opts.domain[0],s.min):s.min, hi=opts.domain?Math.max(opts.domain[1],s.max):s.max;
    let width=opts.width;
    if(opts.mode==='auto') { const fd=2*(s.q3-s.q1)/Math.cbrt(s.n); width=s.n>=4 && fd>0?fd:(hi-lo)/(Math.ceil(Math.log2(s.n)+1)||1); }
    if(opts.mode==='count')width=(hi-lo)/(Math.max(1,Math.min(200,opts.count||10)));
    if(!(width>0) || !Number.isFinite(width))width=1;
    let start=numeric(opts.origin);
    if(start===null)start=opts.mode==='count'?lo:opts.integer&&width===1?Math.floor(lo)-.5:Math.floor(lo/width)*width;
    if(start>lo)start-=Math.ceil((start-lo)/width)*width;
    let n=Math.max(1,Math.ceil((hi-start)/width-1e-10));
    if(n>2000)throw new Error('This width creates more than 2,000 bins. Increase the width.');
    const edges=Array.from({length:n+1},(_,i)=>Number((start+i*width).toPrecision(14)));
    if(edges[edges.length-1]<hi)edges[edges.length-1]=hi;
    return edges;
  }
  function binIndex(v,edges) {
    if(v<edges[0]||v>edges[edges.length-1]||edges.length<2)return -1;
    let lo=0,hi=edges.length-1;
    while(lo+1<hi){const mid=(lo+hi)>>1;if(v<edges[mid])hi=mid;else lo=mid;}
    return Math.min(lo,edges.length-2);
  }
  function histogram(values,edges) {
    const bins=edges.slice(0,-1).map((lo,i)=>({lo,hi:edges[i+1],count:0,percent:0,final:i===edges.length-2}));
    values.forEach(v=>{const i=binIndex(v,edges);if(i>=0)bins[i].count++;});
    bins.forEach(b=>b.percent=values.length?100*b.count/values.length:0);return bins;
  }
  function ranking(row,fields) {
    const choices=[null,null,null], seen=new Set(); let invalid=false;
    for(const f of fields){if(blank(row[f]))continue;const v=numeric(row[f]);if(v===null||!Number.isInteger(v)||v<0||v>3){invalid=true;continue;}if(v>0){if(seen.has(v))invalid=true;seen.add(v);choices[v-1]=f;}}
    if(invalid||!seen.size)return {state:'unavailable',choices:[null,null,null]};
    return {state:seen.size===3?'complete':'partial',choices};
  }
  function rankingSeries(model,rows,q,mode,completeness,allowed) {
    const fields=model.questionFields(q).filter(f=>f.endsWith('_rank'));
    const states={complete:0,partial:0,unavailable:0};
    const eligible=[];
    rows.forEach(row=>{
      const rank=ranking(row,fields);states[rank.state]++;
      const relevant=['1','2','3'].includes(mode)?[rank.choices[Number(mode)-1]].filter(Boolean):rank.choices.filter(Boolean);
      if(rank.state!=='unavailable'&&(completeness==='all'||rank.state===completeness)&&relevant.every(f=>qualityPass(model,row,f,allowed)))eligible.push({row,rank});
    });
    const rankNum=Number(mode), denom=[1,2,3].includes(rankNum)?eligible.filter(x=>x.rank.choices[rankNum-1]).length:eligible.length;
    const data=fields.map(field=>{
      const split=[1,2,3].map(i=>eligible.filter(x=>x.rank.choices[i-1]===field).length);
      const base=field.replace(/_rank$/,'');
      const count=mode==='points'?eligible.reduce((s,x)=>s+(numeric(x.row[`${base}_points`])??0),0):mode==='top'?eligible.filter(x=>numeric(x.row[`${base}_selected`])===1).length:mode==='split'?split.reduce((a,b)=>a+b,0):split[rankNum-1];
      return {field,label:model.dict.get(field)?.['Answer / option']||title(field),count,split,percent:denom?count/denom*100:0};
    });
    return {data,denom,states,eligible};
  }
  return {blank,numeric,title,originals,topic,sheetRows,parseWorkbook,sourceStatuses,qualityPass,value,filterRows,quantile,stats,binEdges,binIndex,histogram,ranking,rankingSeries,unavailable};
});
