/* Regenerate from repository root: node teacher/tools/export-survey-simulation.cjs */
const fs = require('node:fs');
const path = require('node:path');
const crypto = require('node:crypto');
const X = require('../assets/vendor/sheetjs/xlsx.full.min.js');
const C = require('../assets/js/survey-core.js');
const root = path.resolve(__dirname, '../..');
function convert(bytes) {
  const m = C.parseWorkbook(X.read(bytes, {type:'buffer', cellDates:true}), X);
  const domains = {
    q04_commute_minutes:[0,1440], q05_sleep_hours:[0,24], q06_phone_hours:[0,24], q07_exercise_days:[0,7], q08_study_minutes:[0,1440], q09_math_enjoyment:[-10,10],
    q04_one_way_hours:[0,24],q04_daily_round_trip_minutes_est:[0,2880],q04_weekly_travel_hours_est:[0,240],
    q05_sleep_minutes_school_night:[0,1440],q05_sleep_share_of_24_hours:[0,1],q05_five_school_nights_hours_est:[0,120],
    q06_phone_daily_minutes:[0,1440],q06_phone_weekly_hours_est:[0,168],q06_phone_annual_hours_est:[0,8760],q06_phone_annual_equivalent_24h_days_est:[0,365],
    q07_qualifying_days_share:[0,1],q07_nonqualifying_days:[0,7],q07_minimum_weekly_exercise_minutes:[0,210],
    q08_homework_hours_weekday:[0,24],q08_homework_five_weekdays_hours_est:[0,120],q09_math_enjoyment_0_100:[0,100],
    phone_minus_homework_minutes:[-1440,1440]
  };
  const unsupported = /birth_weekday|birth_day_of_year|days_until_next|math_enjoyment|qualifying_days_share|minimum_weekly_exercise/;
  const labels={q01_age_completed_years:'Completed age',q01_calendar_days_lived:'Days lived',q01_completed_weeks_lived:'Completed weeks lived',q01_completed_months_lived:'Completed months lived',q01_age_at_next_birthday:'Age at next birthday',q04_one_way_hours:'One-way commute',q04_daily_round_trip_minutes_est:'Daily return commute (estimate)',q04_weekly_travel_hours_est:'Weekly commute (estimate)',q05_sleep_minutes_school_night:'Sleep per school night',q05_sleep_share_of_24_hours:'Sleep share of a day',q05_five_school_nights_hours_est:'Five nights of sleep (estimate)',q06_phone_daily_minutes:'Daily phone use',q06_phone_weekly_hours_est:'Weekly phone use (estimate)',q06_phone_annual_hours_est:'Annual phone use (estimate)',q06_phone_annual_equivalent_24h_days_est:'Annual phone use in days (estimate)',q07_nonqualifying_days:'Days below exercise threshold',q08_homework_hours_weekday:'Weekday homework',q08_homework_five_weekdays_hours_est:'Weekly homework (estimate)',q11_height_meters:'Height in meters',q11_height_total_inches:'Height in inches',q13_years_since_first_phone_approx:'Years since first phone (estimate)',q14_longest_phone_break_hours:'Longest phone break in hours',q14_longest_phone_break_weeks:'Longest phone break in weeks',phone_to_homework_minutes_ratio:'Phone / homework time ratio',phone_minus_homework_minutes:'Phone minus homework time'};
  // Explicit semantic classification: numeric storage does not imply continuous measurement.
  const fields = m.headers.filter(k=>!['student_id','student_name','q16_other_text'].includes(k)).map(key=>{
    const a=m.meta.find(x=>x.field===key), d=m.dict.get(key), derived=m.derived.get(key);
    const quantitative=!!a && a.kind==='numeric' && !unsupported.test(key);
    const integer= d?.['Data type']==='integer' || /age_completed|calendar_days_lived|completed_weeks|completed_months|age_at_next|nonqualifying_days|_rank$|_selected$|_points$|_has_positive_count$|_is_leap$|is_feb29/.test(key);
    let type=quantitative?(integer?'count':'continuous'): /_rank$/.test(key)?'ordinal': /_selected$|_has_positive_count$|_is_leap$|is_feb29/.test(key)?'binary': /date|birthday$/.test(key)?'date': /points|enjoyment/.test(key)?'score':'categorical';
    if(key==='questionnaire_id')type='identifier';
    const domain=quantitative?(domains[key] || [0,null]):type==='binary'?[0,1]:type==='ordinal'||/_points$/.test(key)?[0,3]:null;
    const positive=/^q11_height/.test(key);
    const workbookUnit=derived?.Units||d?.['Unit / encoding']||'';
    return {key,label:labels[key]||a?.label||d?.['Answer / option']||C.title(key),unit:workbookUnit==='percentage'?'fraction of 1':workbookUnit,workbookUnit,measurementType:type,domain,validDomain:domain||d?.['Allowed values / meaning']||derived?.['Calculation and assumptions']||'Recorded categories',exclusiveMinimum:positive,integer:!!integer,precision:integer?1:'continuous; retain workbook precision',normalModeling:quantitative?'approximation':'unsupported',topic:a?.topic||'Other',origin:derived?(derived.Classification==='estimated'?'workbook estimate':'derived'):'source',dependencies:a?.dependencies||[key],description:derived?.['Calculation and assumptions']||d?.['Allowed values / meaning']||''};
  });
  const valid=(v,f)=>typeof v==='number'&&Number.isFinite(v)&&(!f.domain||((f.exclusiveMinimum?v>f.domain[0]:v>=f.domain[0])&&(f.domain[1]===null||v<=f.domain[1])))&&(!f.integer||Number.isInteger(v));
  // Identity is joined exclusively by the unique questionnaire key, never student ID or value.
  const names = new Map(m.rows.map(r=>[r.questionnaire_id,typeof r.student_name==='string'?r.student_name.trim():null]));
  const records=m.rows.map((r,i)=>{
    const values={},statuses={};
    for(const f of fields){
      const raw=r[f.key], usable=C.qualityPass(m,r,f.key,null);
      values[f.key]=C.blank(raw)||!usable?null:raw instanceof Date?raw.toISOString().slice(0,10):raw;
      if(f.normalModeling!=='unsupported'&&!valid(values[f.key],f))values[f.key]=null;
      const ss=C.sourceStatuses(m,r,f.key);
      if(ss.length)statuses[f.key]=ss.map(s=>({field:s.field,status:s.final_status,condition:s.original_condition,method:s.transformation_method}));
    }
    if(C.numeric(r.q08_study_minutes)===0)values.phone_to_homework_minutes_ratio=null;
    return {questionnaire_id:r.questionnaire_id,student_name:names.get(r.questionnaire_id)||null,label:`Questionnaire ${String(i+1).padStart(3,'0')}`,grade:r.grade,group_section:r.group_section,values,statuses};
  });
  return {schemaVersion:2,source:'survey_data_extended.xlsx',sha256:crypto.createHash('sha256').update(bytes).digest('hex'),referenceDate:m.config.find(r=>r.Setting==='Survey reference date').Value.toISOString().slice(0,10),reconciliation:'Populated Clean answers headers and cells override obsolete blank-template prose. Student names are exported for step 1 only; student identification numbers and free-text answers are excluded. Dates and derivations remain workbook snapshots. Fractions remain fractions, not percentages.',config:m.config.map(r=>({...r,Value:r.Value instanceof Date?r.Value.toISOString():r.Value})).filter(r=>!['Transfer identity','Transfer method'].includes(r.Setting)),fields,records,issues:[...m.issues.values()].flat().map(r=>({questionnaire_id:r['Questionnaire ID'],field:r.Field,issue:r.Issue,handling:r.Handling}))};
}
function serialize(data){return '/* Generated by teacher/tools/export-survey-simulation.cjs; do not edit. */\n(function(root){const data='+JSON.stringify(data).replace(/</g,'\\u003c')+';if(typeof module==="object"&&module.exports)module.exports=data;else root.SurveyData=data;})(globalThis);\n';}
if(require.main===module){const data=convert(fs.readFileSync(path.join(root,'assets/data/survey_data_extended.xlsx')));fs.writeFileSync(path.join(root,'assets/data/survey_data_extended.js'),serialize(data));console.log(`Exported ${data.records.length} questionnaires with step-1 names, reference ${data.referenceDate}`);}
module.exports={convert,serialize};

