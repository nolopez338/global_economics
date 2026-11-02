/* Static, local-only survey dashboard. Workbook contents never leave the browser. */
(() => {
  'use strict';
  const C = window.SurveyCore, $ = id => document.getElementById(id);
  const palette=['#24766b','#b56b37','#557db0','#8966a5','#a34966','#477f94','#79772d','#a65735','#5968aa','#357950'];
  const rankColors=['#24766b','#598bb0','#c68a43'];
  let model, filtered=[], selection=null, frequency=[], rankFrequency=[], sortField='Questionnaire ID', ascending=true, sourceName='', reference='', requestVersion=0;
  const state={grades:new Set(),classes:new Set(),quality:new Set(),ranges:[],categories:[]};
  const fmt=v=>v===null||v===undefined||!Number.isFinite(Number(v))?'Unavailable':Number(v).toLocaleString('en-US',{maximumFractionDigits:3});
  const txt=v=>v instanceof Date?v.toISOString().slice(0,10):C.blank(v)?'Unavailable':String(v);
  function el(tag,text,attrs={}){const n=document.createElement(tag);if(text!==undefined)n.textContent=text;for(const [k,v]of Object.entries(attrs))n.setAttribute(k,v);return n;}
  function empty(host,message){host.replaceChildren(el('p',message,{class:'empty'}));}
  function options(host,values,selected){host.replaceChildren();values.forEach(v=>{const o=el('option',typeof v==='string'?v:v.label,{value:typeof v==='string'?v:v.value});o.selected=o.value===selected;host.append(o);});}
  function table(host,headers,rows,caption,sortable=false){
    host.replaceChildren();const t=el('table');t.append(el('caption',caption));const head=el('thead'),tr=el('tr');
    headers.forEach(h=>{const th=el('th',undefined,{scope:'col'});if(sortable){const b=el('button',h+(sortField===h?(ascending?' ↑':' ↓'):''));b.onclick=()=>{ascending=sortField===h?!ascending:true;sortField=h;renderDetails();};th.setAttribute('aria-sort',sortField===h?(ascending?'ascending':'descending'):'none');th.append(b);}else th.textContent=h;tr.append(th);});
    head.append(tr);t.append(head);const body=el('tbody');rows.forEach(row=>{const tr=el('tr');row.forEach(v=>tr.append(el('td',txt(v))));body.append(tr);});
    if(!rows.length){const tr=el('tr');tr.append(el('td','No matching records.',{colspan:headers.length}));body.append(tr);}t.append(body);host.append(t);
  }
  function checks(host,values,key){host.replaceChildren();values.forEach(v=>{const lab=el('label'),input=el('input',undefined,{type:'checkbox',value:v});input.checked=state[key].has(v);input.onchange=()=>{input.checked?state[key].add(v):state[key].delete(v);refresh();};lab.append(input,document.createTextNode(v.replace(/_/g,' ')));host.append(lab);});}
  function populateVariables(){
    const select=$('variable'),current=select.value||'q05_sleep_hours',search=$('variable-search').value.toLowerCase();select.replaceChildren();
    const all=model.meta.filter(m=>m.kind==='numeric');const matching=all.filter(m=>(m.label+' '+m.field+' '+m.topic).toLowerCase().includes(search)||m.field===current);
    [...new Set(matching.map(m=>m.topic))].forEach(topic=>{const g=el('optgroup',undefined,{label:topic});matching.filter(m=>m.topic===topic).forEach(m=>g.append(el('option',`${m.label} · ${m.unit}`,{value:m.field})));select.append(g);});select.value=current;
  }
  function meta(){return model.meta.find(m=>m.field===$('variable').value);}
  function activeFilters(){
    const parts=[];if(state.grades.size!==model.grades.length)parts.push(`Grades: ${[...state.grades].join(', ')||'none'}`);
    if(state.classes.size!==model.classes.length)parts.push(`Classes: ${[...state.classes].join(', ')||'none'}`);
    if(state.quality.size!==model.statuses.length)parts.push(`Quality: ${[...state.quality].join(', ')||'none'}`);
    state.ranges.forEach(r=>parts.push(`${model.meta.find(m=>m.field===r.field)?.label}: ${r.min??'−∞'} to ${r.max??'∞'} (stored units)`));
    state.categories.forEach(r=>parts.push(`${fieldLabel(r.field)}: ${[...r.values].map(v=>categoryLabel(r.field,v)).join(', ')}`));return parts.length?parts.join('; '):'All grades, classes, and answer statuses';
  }
  function fieldLabel(f){return model.meta.find(m=>m.field===f)?.label||C.title(f);}
  function categoryLabel(field,v){
    const m=model.meta.find(m=>m.field===field);
    if(m?.unit==='0/1')return Number(v)===1?'Yes':'No';
    if(m?.unit==='quarter')return 'Q'+v;
    return String(v);
  }
  function categoryChoices(field){
    const a=[...new Set(model.rows.map(r=>r[field]).filter(v=>!C.blank(v)).map(String))];
    const weekdays=['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday'];
    if(field==='q01_birth_weekday')return a.sort((x,y)=>weekdays.indexOf(x)-weekdays.indexOf(y));
    if(field==='q09_math_enjoyment_category')return a.sort((x,y)=>['Negative','Neutral','Positive'].indexOf(x)-['Negative','Neutral','Positive'].indexOf(y));
    return a.sort((x,y)=>{const p=parseFloat(x),q=parseFloat(y);return Number.isFinite(p)&&Number.isFinite(q)?p-q:x.localeCompare(y);});
  }
  function populateCategoryValues(){const f=$('category-field').value;options($('category-values'),categoryChoices(f).map(v=>({value:v,label:categoryLabel(f,v)})));}
  function resetFilters(){state.grades=new Set(model.grades);state.classes=new Set(model.classes);state.quality=new Set(model.statuses);state.ranges=[];state.categories=[];checks($('grade-options'),model.grades,'grades');checks($('class-options'),model.classes,'classes');checks($('quality-options'),model.statuses,'quality');refresh();}
  function resetChart(){const m=meta();$('bin-mode').value=m.width?'width':'auto';$('bin-width').value=m.width||1;$('bin-count').value=10;$('bin-origin').value='';$('measure').value='count';$('compare').value='pooled';$('compare-layout').value='overlay';$('mean-marker').checked=false;$('median-marker').checked=false;selection=null;refresh();}
  function buildChips(){
    const host=$('filter-chips');host.replaceChildren();host.append(el('span',activeFilters(),{class:'chip'}));
    state.ranges.forEach((r,i)=>{const b=el('button',`Remove ${fieldLabel(r.field)} range ×`);b.onclick=()=>{state.ranges.splice(i,1);refresh();};host.append(b);});
    state.categories.forEach((r,i)=>{const b=el('button',`Remove ${fieldLabel(r.field)} category ×`);b.onclick=()=>{state.categories.splice(i,1);refresh();};host.append(b);});
  }
  function grouped(rows,key){if(key==='pooled')return [{name:'All respondents',rows}];const names=key==='grade'?model.grades:model.classes;return names.map(name=>({name,rows:rows.filter(r=>String(r[key])===name)}));}
  function sv(tag,attrs={},text){const n=document.createElementNS('http://www.w3.org/2000/svg',tag);Object.entries(attrs).forEach(([k,v])=>n.setAttribute(k,v));if(text!==undefined)n.textContent=text;return n;}
  function wrap(s,limit=115){const lines=[];let line='';String(s).split(/\s+/).forEach(w=>{if((line+' '+w).length>limit){lines.push(line);line='';}line+=(line?' ':'')+w;});if(line)lines.push(line);return lines;}
  function makeSvg(host,title,caption,height,width=900){
    const lines=wrap(caption),top=48+lines.length*16;
    const svg=sv('svg',{viewBox:`0 0 ${width} ${height+top}`,role:'group','aria-label':`${title}. ${caption}`,xmlns:'http://www.w3.org/2000/svg'});
    svg.append(sv('title',{},title),sv('desc',{},caption),sv('rect',{width:'100%',height:'100%',fill:'#fff'}));
    svg.append(sv('text',{x:18,y:25,style:'font-size:16px;font-weight:700;fill:#203c52'},title));
    lines.forEach((line,i)=>svg.append(sv('text',{x:18,y:45+i*16,style:'font-size:11px;fill:#536476'},line)));
    const g=sv('g',{transform:`translate(0,${top})`});svg.append(g);host.replaceChildren(svg);return {svg,g,top};
  }
  function tooltip(node,text){node.append(sv('title',{},text));}
  function clickable(node,text,handler){node.classList.add('bar');node.setAttribute('tabindex','0');node.setAttribute('role','button');node.setAttribute('aria-label',text);tooltip(node,text);node.onclick=handler;node.onkeydown=e=>{if(e.key==='Enter'||e.key===' '){e.preventDefault();handler();}};}
  function numericRows(rows,field){return rows.map(row=>({row,v:C.value(model,row,field,state.quality)})).filter(x=>x.v!==null);}
  function chartCaption(m,n){return `${m.label} (${m.unit}) · ${activeFilters()} · usable n=${n} · reference ${reference}`;}
  function renderHistogram(){
    const m=meta(), data=numericRows(filtered,m.field),values=data.map(x=>x.v),s=C.stats(values);
    const intrinsic=filtered.filter(r=>C.value(model,r,m.field,null)!==null).length;
    $('total-n').textContent=model.rows.length;$('filtered-n').textContent=filtered.length;$('usable-n').textContent=s.n;$('missing-n').textContent=filtered.length-s.n;
    $('usable-note').textContent=`${m.label} · ${m.unit}`;$('missing-note').textContent=`${filtered.length-intrinsic} unavailable; ${intrinsic-s.n} quality-excluded`;
    $('variable-description').textContent=`${m.classification} · ${m.description} [${m.field}]`;
    $('chart-title').textContent=`${m.label} (${m.unit})`;
    const caption=chartCaption(m,s.n);$('chart-caption').textContent=caption;
    const st=$('stats');st.replaceChildren();for(const [label,v]of [['Usable n',s.n],['Mean',s.mean],['Median',s.median],['Minimum',s.min],['Maximum',s.max],['First quartile',s.q1],['Third quartile',s.q3],['Sample standard deviation',s.sd]]){const d=el('div',label,{class:'stat'});d.append(el('strong',fmt(v)));st.append(d);}
    frequency=[];
    $('bin-width').disabled=$('bin-mode').value!=='width';$('bin-count').disabled=$('bin-mode').value!=='count';
    if(!values.length){empty($('histogram'),'No usable values for this variable and these filters.');table($('frequency-table'),['Group','Interval','Count','Percent','Usable n'],[],'Histogram frequencies');return;}
    let edges;
    try{edges=C.binEdges(values,{mode:$('bin-mode').value,width:C.numeric($('bin-width').value),count:C.numeric($('bin-count').value),origin:$('bin-origin').value,integer:m.integer,domain:m.domain});}catch(e){empty($('histogram'),e.message);table($('frequency-table'),['Message'],[[e.message]],'Chart settings');return;}
    const groups=grouped(filtered,$('compare').value).map(g=>{const values=numericRows(g.rows,m.field).map(x=>x.v);return {...g,values,stats:C.stats(values),bins:C.histogram(values,edges)};});
    const percent=$('measure').value==='percent',small=$('compare-layout').value==='small'&&groups.length>1;
    const max=Math.max(1,...groups.flatMap(g=>g.bins.map(b=>percent?b.percent:b.count)))*1.08;
    const panelH=small?215:335,{g}=makeSvg($('histogram'),`${m.label} (${m.unit}) · ${percent?'Percentage':'Frequency'}`,caption,panelH*(small?groups.length:1)+65);
    const left=62,right=870,plotW=right-left;
    const draw=(group,gi,panel)=>{
      const top=panel*panelH+30,bottom=top+panelH-85,plotH=bottom-top;
      if(small||gi===0){
        for(let tick=0;tick<=4;tick++){const v=max*tick/4,y=bottom-v/max*plotH;g.append(sv('line',{x1:left,x2:right,y1:y,y2:y,stroke:'#dfe7ec'}),sv('text',{x:53,y:y+4,'text-anchor':'end'},fmt(v)+(percent?'%':'')));}
        g.append(sv('line',{x1:left,x2:right,y1:bottom,y2:bottom,stroke:'#63778a'}));
        const step=Math.max(1,Math.ceil((edges.length-1)/12));edges.forEach((v,i)=>{if(i%step===0||i===edges.length-1){const x=left+i/(edges.length-1)*plotW;g.append(sv('text',{x,y:bottom+22,'text-anchor':'middle'},fmt(v)));}});
      }
      group.bins.forEach((b,i)=>{
        const x=left+i/(edges.length-1)*plotW,w=plotW/(edges.length-1),h=(percent?b.percent:b.count)/max*plotH;
        const chosen=selection?.type==='bin'&&selection.index===i&&(!selection.group||selection.group===group.name);
        const rect=sv('rect',{x,y:bottom-h,width:Math.max(.2,w-.6),height:Math.max(1,h),fill:palette[gi%palette.length],'fill-opacity':small||groups.length===1?.86:.48,class:chosen?'chosen':''});
        const interval=`[${fmt(b.lo)}, ${fmt(b.hi)}${b.final?']':')'}`;
        clickable(rect,`${group.name}: ${interval} ${m.unit}; ${b.count} observations; ${fmt(b.percent)}%; usable n=${group.values.length}`,()=>{selection={type:'bin',index:i,group:$('compare').value==='pooled'?null:group.name,groupKey:$('compare').value,ids:new Set(data.filter(x=>C.binIndex(x.v,edges)===i&&($('compare').value==='pooled'||String(x.row[$('compare').value])===group.name)).map(x=>x.row.questionnaire_id)),label:`Bin ${interval} ${m.unit} · ${group.name}`};renderHistogram();renderRanking();renderDetails();});g.append(rect);
        frequency.push([group.name,interval,b.count,b.percent,group.values.length]);
      });
      for(const [id,k,color]of [['mean-marker','mean','#a13735'],['median-marker','median','#5b3d8b']])if($(id).checked&&group.stats[k]!==null){const x=left+(group.stats[k]-edges[0])/(edges.at(-1)-edges[0])*plotW;const line=sv('line',{x1:x,x2:x,y1:top,y2:bottom,stroke:color,'stroke-width':2,'stroke-dasharray':k==='median'?'3 3':'7 3'});tooltip(line,`${group.name} ${k}: ${fmt(group.stats[k])}`);g.append(line);}
      if(small)g.append(sv('text',{x:left,y:top-12,style:'font-weight:700'},`${group.name} · usable n=${group.values.length} · unavailable/excluded ${group.rows.length-group.values.length}`));
    };
    groups.forEach((group,i)=>draw(group,i,small?i:0));
    if(!small)groups.forEach((group,i)=>{const x=62+(i%3)*275,y=panelH+Math.floor(i/3)*17;g.append(sv('rect',{x,y:y-9,width:10,height:10,fill:palette[i%palette.length]}),sv('text',{x:x+15,y},`${group.name}: usable n=${group.values.length}; other=${group.rows.length-group.values.length}`));});
    const note=el('p',`Intervals: [lower, upper); the final upper endpoint is included. Shared ${edges.length-1} bins; width ${fmt(edges[1]-edges[0])} ${m.unit}. ${$('mean-marker').checked?'Mean: red dashed line. ':''}${$('median-marker').checked?'Median: purple dotted line.':''}`,{class:'hint'});$('histogram').append(note);
    table($('frequency-table'),['Group','Interval','Count','Percent of usable n','Usable n'],frequency.map(r=>[r[0],r[1],r[2],fmt(r[3])+'%',r[4]]),'Histogram frequencies · '+m.label);
  }
  function horizontalChart(host,title,caption,groups,{percent=false,points=false,split=false,onSelect=null}={}){
    const rowH=34,left=330,right=835,groupHeights=groups.map(s=>45+s.data.length*rowH),height=groupHeights.reduce((a,b)=>a+b,0)+25;
    const {g}=makeSvg(host,title,caption,height);
    const max=Math.max(1,...groups.flatMap(s=>s.data.map(d=>percent?d.percent:d.count)))*1.08;
    let offset=0;
    groups.forEach((group,gi)=>{
      g.append(sv('text',{x:16,y:offset+18,style:'font-weight:700'},`${group.name} · denominator n=${group.denom}`));
      group.data.forEach((d,i)=>{
        const y=offset+33+i*rowH,v=percent?d.percent:d.count,w=v/max*(right-left);
        const label=d.label.length>43?d.label.slice(0,40)+'…':d.label;
        const labelNode=sv('text',{x:left-12,y:y+16,'text-anchor':'end'},label);tooltip(labelNode,d.label);g.append(labelNode);
        const selected=selection?.type==='rank'&&selection.field===d.field&&(!selection.group||selection.group===group.name);
        const hit=sv('rect',{x:left,y,width:Math.max(5,w),height:23,fill:palette[i%palette.length],class:selected?'chosen':''});
        const info=`${group.name}: ${d.label}; ${d.count} ${points?'points':'count'}; ${points?'':fmt(d.percent)+'%; '}denominator n=${group.denom}${split?'; ranks 1, 2, 3: '+d.split.join(', '):''}`;
        if(onSelect)clickable(hit,info,()=>onSelect(d,group));else tooltip(hit,info);g.append(hit);
        if(split&&d.count>0){let x=left;d.split.forEach((count,j)=>{const width=(percent?(group.denom?100*count/group.denom:0):count)/max*(right-left),rect=sv('rect',{x,y,width,height:23,fill:rankColors[j],'pointer-events':'none'});g.append(rect);x+=width;});if(selected)g.append(sv('rect',{x:left,y,width:w,height:23,fill:'none',stroke:'#142e48','stroke-width':3,'pointer-events':'none'}));}
        g.append(sv('text',{x:left+w+8,y:y+16},percent?fmt(d.percent)+'%':fmt(d.count)));
      });offset+=groupHeights[gi];
    });
    if(split)rankColors.forEach((color,i)=>{g.append(sv('rect',{x:330+i*150,y:offset-2,width:10,height:10,fill:color}),sv('text',{x:345+i*150,y:offset+8},`Rank ${i+1}`));});
  }
  function rankingResult(rows){return C.rankingSeries(model,rows,Number($('rank-question').value),$('rank-mode').value,$('rank-completeness').value,state.quality);}
  function renderRanking(){
    const q=Number($('rank-question').value),mode=$('rank-mode').value,overall=rankingResult(filtered),groupKey=$('rank-compare').value;
    const groups=grouped(filtered,groupKey).map(g=>({...rankingResult(g.rows),name:g.name}));
    $('rank-measure').disabled=mode==='points';
    const percent=mode!=='points'&&$('rank-measure').value==='percent',states=overall.states;
    const caption=`Q${q} · ${$('rank-mode').selectedOptions[0].textContent} · complete ${states.complete}, partial ${states.partial}, unavailable ${states.unavailable} (before completeness/quality selection). Eligible n=${overall.eligible.length}; denominator n=${overall.denom}. ${mode==='points'?'Points: rank 1=3, rank 2=2, rank 3=1; not probabilities.':mode==='top'||mode==='split'?'Percent denominator: eligible respondents; totals may exceed 100%.':'Denominator: usable choice at this rank.'} · ${activeFilters()} · reference ${reference}`;
    $('ranking-caption').textContent=caption;
    horizontalChart($('ranking-chart'),`Q${q} · ${$('rank-mode').selectedOptions[0].textContent}`,caption,groups,{percent,points:mode==='points',split:mode==='split',onSelect:(d,g)=>{
      const ids=g.eligible.filter(x=>{if(['1','2','3'].includes(mode))return x.rank.choices[Number(mode)-1]===d.field;return C.numeric(x.row[d.field.replace(/_rank$/,'_selected')])===1;}).map(x=>x.row.questionnaire_id);
      selection={type:'rank',field:d.field,group:groupKey==='pooled'?null:g.name,ids:new Set(ids),label:`Q${q}: ${d.label} · ${$('rank-mode').selectedOptions[0].textContent} · ${g.name}`};renderHistogram();renderRanking();renderDetails();
    }});
    rankFrequency=groups.flatMap(g=>g.data.map(d=>[g.name,d.label,...d.split,d.count,mode==='points'?'Points':percent?'% of eligible respondents':'Count',mode==='points'?null:d.percent,g.denom]));
    table($('ranking-table'),['Group','Option','Rank 1','Rank 2','Rank 3','Displayed total','Measure','Percent','Denominator n'],rankFrequency.map(r=>r.map((v,i)=>i===7?(v===null?'Not applicable':fmt(v)+'%'):v)),`Q${q} preference frequencies`);
    renderOther();
  }
  function renderOther(){const search=$('other-search').value.toLowerCase(),names=$('show-identities').checked;const rows=filtered.filter(r=>!C.blank(r.q16_other_text)&&String(r.q16_other_text).toLowerCase().includes(search));table($('other-table'),['Questionnaire ID','Class',...(names?['Name']:[]),'Original Q16 Other wording'],rows.map(r=>[r.questionnaire_id,r.class_label,...(names?[r.student_name]:[]),r.q16_other_text]),`${rows.length} matching original responses (no normalization)`);}
  function renderSecondary(){
    const mode=$('secondary-mode').value;
    $('secondary-category-label').hidden=mode!=='category';$('box-group-label').hidden=mode!=='box';$('scatter-controls').hidden=mode!=='scatter';
    if(mode==='category'){
      const field=$('secondary-category').value,eligible=filtered.filter(r=>!C.blank(r[field])&&C.qualityPass(model,r,field,state.quality)),denom=eligible.length;
      const data=categoryChoices(field).map(v=>({label:categoryLabel(field,v),count:eligible.filter(r=>String(r[field])===v).length}));data.forEach(d=>d.percent=denom?d.count/denom*100:0);
      const cap=`${fieldLabel(field)} · usable n=${denom}; unavailable/excluded ${filtered.length-denom} · ${activeFilters()} · reference ${reference}`;$('secondary-caption').textContent=cap;
      horizontalChart($('secondary-chart'),fieldLabel(field),cap,[{name:'All filtered respondents',denom,data}]);table($('secondary-table'),['Category','Count','Percent of usable n','Usable n'],data.map(d=>[d.label,d.count,fmt(d.percent)+'%',denom]),'Categorical frequencies');
    }else if(mode==='box'){
      const m=meta(),groups=grouped(filtered,$('box-group').value).map(g=>({...g,...C.stats(numericRows(g.rows,m.field).map(x=>x.v))})),values=numericRows(filtered,m.field).map(x=>x.v);
      const cap=`${chartCaption(m,values.length)} · boxes Q1–Q3, line median, diamond mean; whiskers minimum–maximum (all observations).`;$('secondary-caption').textContent=cap;
      if(!values.length)empty($('secondary-chart'),'No usable values.');else{
        const all=C.stats(values),min=all.min,max=all.max===min?min+1:all.max,x=v=>145+(v-min)/(max-min)*680;
        const {g}=makeSvg($('secondary-chart'),`${m.label} by ${$('box-group').value==='grade'?'grade':'class'} (${m.unit})`,cap,groups.length*57+55);
        groups.forEach((s,i)=>{const y=30+i*57;g.append(sv('text',{x:15,y:y+4},`${s.name} · n=${s.n}`));if(!s.n){g.append(sv('text',{x:150,y:y+4},'Unavailable'));return;}g.append(sv('line',{x1:x(s.min),x2:x(s.max),y1:y,y2:y,stroke:'#4c667b'}),sv('rect',{x:x(s.q1),y:y-12,width:Math.max(1,x(s.q3)-x(s.q1)),height:24,fill:palette[i%palette.length],'fill-opacity':.5,stroke:'#3a5367'}),sv('line',{x1:x(s.median),x2:x(s.median),y1:y-12,y2:y+12,stroke:'#152e44','stroke-width':2}));[s.min,s.max].forEach(v=>g.append(sv('line',{x1:x(v),x2:x(v),y1:y-8,y2:y+8,stroke:'#3a5367'})));const diamond=sv('path',{d:`M ${x(s.mean)} ${y-5} l 5 5 -5 5 -5 -5 Z`,fill:'#a13735'});tooltip(diamond,`${s.name}: mean ${fmt(s.mean)}, median ${fmt(s.median)}, Q1 ${fmt(s.q1)}, Q3 ${fmt(s.q3)}, min ${fmt(s.min)}, max ${fmt(s.max)}`);g.append(diamond);});
        for(let i=0;i<=5;i++){const v=min+(max-min)*i/5;g.append(sv('text',{x:x(v),y:groups.length*57+20,'text-anchor':'middle'},fmt(v)));}
      }
      table($('secondary-table'),['Group','Usable n','Unavailable / excluded','Minimum','Q1','Median','Q3','Maximum','Mean','Sample SD'],groups.map(s=>[s.name,s.n,s.rows.length-s.n,...[s.min,s.q1,s.median,s.q3,s.max,s.mean,s.sd].map(fmt)]),'Box plot summary');
    }else{
      const xf=$('scatter-x').value,yf=$('scatter-y').value,xm=model.meta.find(m=>m.field===xf),ym=model.meta.find(m=>m.field===yf);
      const pairs=filtered.map(row=>({row,x:C.value(model,row,xf,state.quality),y:C.value(model,row,yf,state.quality)})).filter(p=>p.x!==null&&p.y!==null);
      const xs=C.stats(pairs.map(p=>p.x)),ys=C.stats(pairs.map(p=>p.y));let r=null;if(pairs.length>1&&xs.sd>0&&ys.sd>0)r=pairs.reduce((s,p)=>s+(p.x-xs.mean)*(p.y-ys.mean),0)/((pairs.length-1)*xs.sd*ys.sd);
      const cap=`X: ${xm.label} (${xm.unit}); Y: ${ym.label} (${ym.unit}) · paired n=${pairs.length}; unpaired/excluded ${filtered.length-pairs.length}; Pearson r=${fmt(r)}. Association does not imply causation. · ${activeFilters()} · reference ${reference}`;$('secondary-caption').textContent=cap;
      if(!pairs.length)empty($('secondary-chart'),'No pairwise-complete observations.');else{
        const {g}=makeSvg($('secondary-chart'),`${xm.label} versus ${ym.label}`,cap,370),x=v=>80+(v-xs.min)/(xs.max-xs.min||1)*760,y=v=>300-(v-ys.min)/(ys.max-ys.min||1)*270;
        for(let i=0;i<=5;i++){let vx=xs.min+(xs.max-xs.min)*i/5,vy=ys.min+(ys.max-ys.min)*i/5;g.append(sv('text',{x:x(vx),y:321,'text-anchor':'middle'},fmt(vx)),sv('text',{x:67,y:y(vy)+4,'text-anchor':'end'},fmt(vy)),sv('line',{x1:80,x2:840,y1:y(vy),y2:y(vy),stroke:'#e1e8ed'}));}
        pairs.forEach(p=>{const dot=sv('circle',{cx:x(p.x),cy:y(p.y),r:4,fill:palette[model.grades.indexOf(String(p.row.grade))%palette.length],'fill-opacity':.65});tooltip(dot,`${p.row.questionnaire_id} · ${p.row.class_label}: ${xm.label} ${fmt(p.x)} ${xm.unit}; ${ym.label} ${fmt(p.y)} ${ym.unit}`);g.append(dot);});g.append(sv('text',{x:450,y:352,'text-anchor':'middle'},`${xm.label} (${xm.unit})`),sv('text',{transform:'translate(17 165) rotate(-90)','text-anchor':'middle'},`${ym.label} (${ym.unit})`));
      }
      table($('secondary-table'),['Questionnaire ID','Class',`${xm.label} (${xm.unit})`,`${ym.label} (${ym.unit})`],pairs.map(p=>[p.row.questionnaire_id,p.row.class_label,fmt(p.x),fmt(p.y)]),'Pairwise-complete scatterplot observations');
    }
  }
  function relatedFields(){const m=meta(),q=Number($('rank-question').value);return [...new Set([m.field,...m.dependencies,...model.questionFields(q)])];}
  function statusText(row){const field=meta().field,ss=C.sourceStatuses(model,row,field);return ss.length?ss.map(s=>`${s.field}: ${s.final_status} (${s.transformation_method||s.original_condition||'no method supplied'})`).join('; '):'No answer-level status recorded';}
  function issueText(row){return relatedFields().flatMap(f=>(model.issues.get(model.key(row.questionnaire_id,f))||[]).map(i=>`${i.Field}: ${i.Issue}; recorded ${txt(i['Recorded value'])}; ${i.Handling}`)).join(' | ')||'None recorded for these fields';}
  function detailData(rows,exporting=false){
    const reveal=$('show-identities').checked,m=meta(),q=$('rank-question').value;
    const headers=[...(!exporting||reveal?['Questionnaire ID']:[]),'Class',`${m.label} (${m.unit})`,'Answer / source quality','Issues',`Q${q} completeness`,`Q${q} first choice`,`Q${q} second choice`,`Q${q} third choice`,`Q${q} known-choice quality`,...(!$('secondary-mode').value.includes('scatter')?[]:[fieldLabel($('scatter-x').value),fieldLabel($('scatter-y').value)]),...(reveal?['Student ID','Student name']:[])];
    const data=rows.map(r=>{const rank=C.ranking(r,model.questionFields(Number(q)).filter(f=>f.endsWith('_rank')));const rankQuality=rank.choices.filter(Boolean).map(f=>`${model.dict.get(f)?.['Answer / option']}: ${model.status.get(model.key(r.questionnaire_id,f))?.final_status||'No answer-level status recorded'}`).join('; ')||'No usable choices';return [...(!exporting||reveal?[r.questionnaire_id]:[]),r.class_label,C.value(model,r,m.field,state.quality),statusText(r),issueText(r),rank.state,...[1,2,3].map(i=>r[`q${q}_choice_${i}`]),rankQuality,...(!$('secondary-mode').value.includes('scatter')?[]:[C.value(model,r,$('scatter-x').value,state.quality),C.value(model,r,$('scatter-y').value,state.quality)]),...(reveal?[r.student_id,r.student_name]:[])];});return {headers,data};
  }
  function renderDetails(){
    const rows=selection?filtered.filter(r=>selection.ids.has(r.questionnaire_id)):filtered;
    $('selection-status').textContent=selection?`Chart selection: ${selection.label} · ${rows.length} selected questionnaires`:`No chart selection · ${rows.length} filtered questionnaires`;
    const d=detailData(rows),search=$('detail-search').value.toLowerCase();let data=d.data.filter(r=>r.some(v=>txt(v).toLowerCase().includes(search)));
    const index=d.headers.indexOf(sortField);if(index>=0)data.sort((a,b)=>{const av=a[index],bv=b[index];if(C.blank(av))return C.blank(bv)?0:1;if(C.blank(bv))return -1;const sign=ascending?1:-1;return sign*(typeof av==='number'&&typeof bv==='number'?av-bv:String(av).localeCompare(String(bv),undefined,{numeric:true}));});
    table($('detail-table'),d.headers,data,`${data.length} displayed respondents`,true);renderEvidence(rows);
  }
  function renderEvidence(rows){
    const fields=relatedFields(),out=[];
    rows.forEach(r=>fields.forEach(f=>{(model.audit.get(model.key(r.questionnaire_id,f))||[]).forEach(a=>out.push([r.questionnaire_id,f,'Audit',a.original_value,a.result,a.reason,a.source_reference]));(model.issues.get(model.key(r.questionnaire_id,f))||[]).forEach(i=>out.push([r.questionnaire_id,f,i.Issue,i['Recorded value'],null,i.Handling,'Derived issues']));}));
    table($('evidence-table'),['Questionnaire ID','Field','Kind','Original / recorded','Result','Reason / handling','Source reference'],out,`${out.length} relevant audit and issue entries`);
  }
  function renderCompleteness(){
    const fields=['q01_date_of_birth',...Object.keys(C.originals)],rows=fields.map(f=>{const n=filtered.filter(r=>!C.blank(r[f])&&C.qualityPass(model,r,f,null)).length;return [model.dict.get(f)?.['Answer / option']||fieldLabel(f),n,filtered.length-n,filtered.length];});
    [16,17,18].forEach(q=>{const ranks=filtered.map(r=>C.ranking(r,model.questionFields(q).filter(f=>f.endsWith('_rank')))),n=ranks.filter(r=>r.state!=='unavailable').length;rows.push([`Q${q} · at least one consistent known rank`,n,filtered.length-n,filtered.length]);});
    const {g}=makeSvg($('completeness-chart'),'Completeness by original question',`Global filters · n=${filtered.length}; independent of active-variable quality selection. Green = nonblank / usable; amber = unavailable. Reference ${reference}`,rows.length*32+55);
    rows.forEach((r,i)=>{const y=15+i*32,label=sv('text',{x:315,y:y+15,'text-anchor':'end'},r[0].length>43?r[0].slice(0,40)+'…':r[0]);tooltip(label,r[0]);g.append(label);let x=330;[r[1],r[2]].forEach((n,j)=>{const width=filtered.length?n/filtered.length*390:0,rect=sv('rect',{x,y,width,height:22,fill:j?'#c58d56':'#24766b'});tooltip(rect,`${r[0]}: ${r[1]} nonblank / usable; ${r[2]} unavailable; filtered n=${filtered.length}`);g.append(rect);x+=width;});g.append(sv('text',{x:735,y:y+15},`${r[1]} usable | ${r[2]} unavailable`));});
    table($('completeness-table'),['Question','Nonblank / usable','Unavailable','Filtered n'],rows,'Question completeness');
  }
  function refresh(clear=true){if(!model)return;if(clear)selection=null;filtered=C.filterRows(model.rows,state);buildChips();renderHistogram();renderRanking();renderSecondary();renderDetails();renderCompleteness();}
  function download(blob,name){const url=URL.createObjectURL(blob),a=el('a',undefined,{href:url,download:name});document.body.append(a);a.click();a.remove();setTimeout(()=>URL.revokeObjectURL(url),1000);}
  function csv(headers,rows,name){
    const cell=v=>{let s=C.blank(v)?'':v instanceof Date?v.toISOString().slice(0,10):String(v);if(typeof v==='string'&&/^[\s]*[=+@\-]/.test(s))s="'"+s;return '"'+s.replace(/"/g,'""')+'"';};
    download(new Blob(['\ufeff'+[headers,...rows].map(row=>row.map(cell).join(',')).join('\r\n')],{type:'text/csv;charset=utf-8'}),name);
  }
  function image(host){const original=$(host).querySelector('svg');if(!original)return;const svg=original.cloneNode(true);svg.querySelectorAll('text').forEach(n=>{n.style.fontFamily='system-ui, sans-serif';if(!n.style.fontSize)n.style.fontSize='12px';if(!n.style.fill)n.style.fill='#35485b';});svg.querySelectorAll('.chosen').forEach(n=>{n.setAttribute('fill','#dfaa53');n.setAttribute('stroke','#142e48');n.setAttribute('stroke-width','3');});download(new Blob([new XMLSerializer().serializeToString(svg)],{type:'image/svg+xml;charset=utf-8'}),`survey-${host}.svg`);}
  function verify(){
    const expected={'10A':17,'10B':22,'10C':22,'10D':19,'10E':22,'11A':20,'11B':19,'11C':20,'11D':23,'11E':22};
    const failures=[];if(model.rows.length!==206)failures.push(`records ${model.rows.length}, benchmark 206`);
    for(const [cl,n]of Object.entries(expected)){const actual=model.rows.filter(r=>r.class_label===cl).length;if(actual!==n)failures.push(`${cl}: ${actual}, benchmark ${n}`);}
    for(const [f,n]of [['q05_sleep_hours',201],['q11_height_cm',109],['q09_math_enjoyment',200]]){const count=model.rows.filter(r=>C.value(model,r,f,null)!==null).length;if(count!==n)failures.push(`${f}: ${count} usable, benchmark ${n}`);}
    const math=C.stats(model.rows.map(r=>C.value(model,r,'q09_math_enjoyment',null)).filter(v=>v!==null));if(math.min!==-10||math.max!==10)failures.push(`math range ${math.min} to ${math.max}`);
    $('verification').textContent=(failures.length?`Benchmark differences (file still loaded): ${failures.join('; ')}.`:'Current-source benchmarks pass: 206 unique questionnaires; all ten class sizes; sleep 201 usable / 5 unavailable; height 109 / 97; math enjoyment 200 / 6, range −10 to +10.')+' '+model.warnings.join(' ');
  }
  async function load(buffer,name,token){
    try{
      if(!window.XLSX)throw new Error('The local SheetJS dependency did not load. Restore teacher/assets/vendor/sheetjs/xlsx.full.min.js and reload the page.');
      const wb=XLSX.read(buffer,{type:'array',cellDates:true,nodim:true,cellHTML:false});
      const next=C.parseWorkbook(wb,XLSX);if(token!==requestVersion)return;model=next;sourceName=name;selection=null;
      const ref=model.config.find(r=>r.Setting==='Survey reference date').Value;
      reference=ref instanceof Date?ref.toLocaleDateString('en-US',{timeZone:'UTC',year:'numeric',month:'long',day:'numeric'}):txt(ref);
      $('source').textContent='Source: '+sourceName;$('reference').textContent='Reference date: '+reference;
      $('variable-search').value='';$('variable').replaceChildren();populateVariables();
      const nums=model.meta.filter(m=>m.kind==='numeric').map(m=>({value:m.field,label:`${m.label} (${m.unit})`}));
      for(const id of ['range-field','scatter-x','scatter-y'])options($(id),nums);
      $('scatter-x').value='q06_phone_hours';$('scatter-y').value='q05_sleep_hours';
      const cats=model.meta.filter(m=>m.kind==='categorical').map(m=>({value:m.field,label:m.label}));
      options($('secondary-category'),cats,'q09_math_enjoyment_category');
      options($('category-field'),[...cats,...[16,17,18].flatMap(q=>[1,2,3].map(i=>({value:`q${q}_choice_${i}`,label:`Q${q} · choice ${i}`})))]);populateCategoryValues();
      $('show-identities').checked=false;verify();table($('config-table'),['Setting','Value','Meaning'],model.config.map(r=>[r.Setting,txt(r.Value),r.Meaning]),'Workbook derivation configuration');
      $('dashboard').hidden=false;state.grades=new Set(model.grades);state.classes=new Set(model.classes);state.quality=new Set(model.statuses);state.ranges=[];state.categories=[];
      checks($('grade-options'),model.grades,'grades');checks($('class-options'),model.classes,'classes');checks($('quality-options'),model.statuses,'quality');resetChart();
      $('load-status').classList.remove('error');$('load-status').textContent=`Ready · ${model.rows.length} questionnaires · ${model.headers.length} source columns · processed locally in your browser.`;
    }catch(e){if(token!==requestVersion)return;loadingError(e);}
  }
  function loadingError(e){$('load-status').classList.add('error');$('load-status').textContent=`Could not load workbook: ${e.message} Choose a compatible local XLSX file above to retry.${model?' The previous successfully loaded workbook remains displayed.':''}`;$('reference').textContent=model?'Reference date: '+reference:'Reference date: unavailable until a workbook is loaded';}
  $('workbook-file').addEventListener('change',async e=>{const file=e.target.files[0];if(!file)return;const token=++requestVersion;$('load-status').textContent='Reading local file…';try{await load(await file.arrayBuffer(),file.name,token);}catch(e){if(token===requestVersion)loadingError(e);}});
  $('variable-search').oninput=()=>model&&populateVariables();$('variable').onchange=()=>resetChart();$('reset-chart').onclick=()=>resetChart();$('clear-filters').onclick=()=>resetFilters();
  document.querySelectorAll('[data-select]').forEach(b=>b.onclick=()=>{if(!model)return;const [key,action]=b.dataset.select.split(':'),values=key==='quality'?model.statuses:model[key];state[key]=new Set(action==='all'?values:[]);checks($(key==='grades'?'grade-options':key==='classes'?'class-options':'quality-options'),values,key);refresh();});
  $('add-range').onclick=()=>{if(!model)return;const min=C.numeric($('range-min').value),max=C.numeric($('range-max').value);if(min===null&&max===null)return;if(min!==null&&max!==null&&min>max){$('range-min').setCustomValidity('Minimum must not exceed maximum.');$('range-min').reportValidity();return;}$('range-min').setCustomValidity('');const field=$('range-field').value;state.ranges=state.ranges.filter(r=>r.field!==field);state.ranges.push({field,min,max});refresh();};$('range-min').oninput=()=>$('range-min').setCustomValidity('');
  $('category-field').onchange=()=>model&&populateCategoryValues();$('add-category').onclick=()=>{if(!model)return;const field=$('category-field').value,values=new Set([...$('category-values').selectedOptions].map(o=>o.value));state.categories=state.categories.filter(r=>r.field!==field);state.categories.push({field,values});refresh();};
  for(const id of ['bin-mode','bin-width','bin-count','bin-origin','measure','compare','compare-layout','mean-marker','median-marker','rank-question','rank-mode','rank-completeness','rank-measure','rank-compare','secondary-mode','secondary-category','box-group','scatter-x','scatter-y'])$(id).addEventListener('change',()=>refresh());
  $('scatter-preset').onchange=()=>{const [x,y]=$('scatter-preset').value.split(',');$('scatter-x').value=x;$('scatter-y').value=y;refresh();};
  $('other-search').oninput=()=>model&&renderOther();$('detail-search').oninput=()=>model&&renderDetails();$('show-identities').onchange=()=>{if(model){renderDetails();renderOther();}};
  $('clear-selection').onclick=()=>{selection=null;renderHistogram();renderRanking();renderDetails();};
  $('frequency-export').onclick=()=>csv(['Group','Interval','Count','Percent of usable n','Usable n'],frequency,'survey-histogram.csv');
  $('ranking-export').onclick=()=>csv(['Group','Option','Rank 1','Rank 2','Rank 3','Displayed total','Measure','Percent','Denominator n'],rankFrequency,'survey-preferences.csv');
  $('analysis-export').onclick=()=>{const d=detailData(filtered,true);csv(d.headers,d.data,'survey-filtered-analysis.csv');};
  document.querySelectorAll('[data-image]').forEach(b=>b.onclick=()=>image(b.dataset.image));
  async function autoLoad(){
    const token=++requestVersion;
    if(!C){loadingError(new Error('The dashboard analysis script failed to load. Check the local survey-core.js path and reload.'));return;}
    if(!window.XLSX){loadingError(new Error('The local SheetJS dependency failed to load. Restore teacher/assets/vendor/sheetjs/xlsx.full.min.js and reload.'));return;}
    if(location.protocol==='file:'){loadingError(new Error('Automatic loading is unavailable on file://. Use the local file picker, or serve the repository root over HTTP.'));return;}
    const controller=new AbortController(),timeout=setTimeout(()=>controller.abort(),20000);
    try{const response=await fetch('../../assets/data/survey_data_extended.xlsx',{signal:controller.signal});if(!response.ok)throw new Error(`HTTP ${response.status} at ../../assets/data/survey_data_extended.xlsx`);await load(await response.arrayBuffer(),'survey_data_extended.xlsx',token);}catch(e){if(token===requestVersion)loadingError(e);}finally{clearTimeout(timeout);}
  }
  autoLoad();
})();
