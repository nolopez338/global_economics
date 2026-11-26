/* Grade 11 C3. Native HTML equations are rendered once; SVG and numerical text
   update without typesetting. No shared presentation scripts are modified. */
(() => {
  'use strict';
  const $ = s => document.querySelector(s);
  const colors = {mean:'#ff765c',point:'#9bdd36',sd:'#e42134',size:'#173b17',se:'#f4d94b',confidence:'#55c8f0',critical:'#2648bb',tail:'#408ed8',margin:'#f28a18',bounds:'#f9ca97',width:'#6d3e0b',normal:'#43a5c9'};
  const h = (role, text) => `<mark data-role="${role}" style="--role:${colors[role]}">${text}</mark>`;
  const sym = {mean:'μ',point:'x̄',sd:'σ',size:'n',se:'SE',confidence:'C',critical:'z<sup>*</sup>',tail:'α',margin:'MoE',bounds:'CI',width:'W',normal:'Φ'};
  const m = r => h(r,sym[r]);
  const frac = (a,b) => `<span class="frac"><span>${a}</span><span>${b}</span></span>`;
  const eq = text => `<div class="equation">${text}</div>`;
  const p = text => `<p>${text}</p>`;
  const step = (i,text) => `<div class="reveal" data-step="${i}">${text}</div>`;
  const ns = [25,100,400,800,1600], zs=[1.282,1.645,1.960,2.576,3.291], cs=[80,90,95,99,99.9], ids=['A','B','C','D','E'];
  const f = (v,d=3) => Number(v).toFixed(d);
  const {model,cdf,invCdf}=window.G11C3Math;
  const legend = [
    ['mean','μ','Population mean',"Fixed mean of the defined population, in the response’s units."],
    ['point','x̄','Sample mean and point estimate','Average of one sample; estimates its population mean.'],
    ['sd','σ','Population or model standard deviation','Spread of individual values, in original units.'],
    ['size','n','Observation count','Fixed trial count or sample size; a positive integer.'],
    ['se','SE','Standard error','Spread of a statistic across samples, or its estimate.'],
    ['confidence','C','Confidence level','Chosen nominal long-run coverage under the model; decimal in formulas.'],
    ['tail','α, α/2','Significance level and tail area','Total excluded area and each equal tail in a two-sided procedure.'],
    ['critical','z<sup>*</sup>','Critical value','Positive unitless reference cutoff selected by confidence and model.'],
    ['margin','MoE','Margin of error','Centre-to-bound distance, or its precision target.'],
    ['bounds','L, U; CI = [L, U]','Bounds and confidence interval','Lower and upper limits; the range they delimit for the parameter.'],
    ['width',`W = ${h('bounds','U')} − ${h('bounds','L')}; W = 2${h('margin','MoE')}`,'Full interval width','Total distance between bounds, in the parameter’s units.'],
    ['normal',`Φ(z), ${h('critical','Φ<sup>−1</sup>')}(u)`,'Normal cumulative area and inverse','Left-tail standard normal area; the cutoff with that area.'],
    ['normal','C<sub>normal</sub>','Theoretical normal coverage','Model area from a rounded cutoff; may differ slightly from nominal confidence.']
  ];
  const legendEntry = (e) => `<button class="legend-entry" data-focus-role="${e[0]}"><strong><span class="legend-symbol">${h(e[0],e[1])}</span> ${h(e[0],e[2])}</strong><span class="meaning">${e[3]}</span></button>`;
  const caseButton = (i,task) => `<button class="case-button" data-case="${i}" data-task="${task}" aria-label="Select Task ${task} case ${ids[i]}" aria-pressed="false">${ids[i]}</button>`;
  function table(headers, rows, cls=''){return `<table class="${cls}"><thead><tr>${headers.map(v=>`<th scope="col">${v}</th>`).join('')}</tr></thead><tbody>${rows.join('')}</tbody></table>`;}
  const task1Rows = ns.map((n,i)=>{
    const q=model(n,1.960),approx=i===3?'≈':'=';
    return `<tr class="reveal" data-step="${i+1}" data-row="${i}" data-task="1"><td>${caseButton(i,1)}</td><td>${h('size',n)}</td><td>${h('sd','30')}/√${h('size',n)} ${approx} ${h('se',f(q.se))}</td><td>${h('critical','1.960')}(${i===3?`${h('sd','30')}/√${h('size',n)}`:h('se',f(q.se))}) ${approx} ${h('margin',f(q.moe))}</td></tr>`;
  });
  const task2Rows = zs.map((z,i)=>`<tr class="reveal" data-step="${i+1}" data-row="${i}" data-task="2"><td>${caseButton(i,2)}</td><td>${h('confidence',cs[i])}</td><td>${h('critical',f(z))}</td><td>${h('critical',f(z))}(${h('se','3.000')}) = ${h('margin',f(z*3))}</td></tr>`);
  const intervalExamples = table(['Sample size','Centre ± margin','Interval (thousand COP)'],[0,2,4].map((i,k)=>{const q=model(ns[i],1.960);return `<tr class="reveal" data-step="${k+2}" data-example="${ns[i]}"><td>${h('size',ns[i])}</td><td>${h('point','84')} ± ${h('margin',f(q.moe))}</td><td>${h('bounds',`[${f(q.l)}, ${f(q.u)}]`)}</td></tr>`;}));
  const slides = [];
  const add = (title,chapter,body,steps,mode,caption) => slides.push({title,chapter,body,steps,mode,caption});
  add('Anatomy of a confidence interval','C3 · Components and connections',`<p class="eyebrow">Grade 11 · Term 2 · Lesson 1 · 2026–2027</p><h1>Anatomy of a confidence interval</h1><div class="criterion">${p('<strong>C3.</strong> Identifies the components of a confidence interval, including point estimate, critical value, standard error, and margin of error, explaining how each component affects precision and reliability.')}</div>${step(1,eq(`${m('point')} ± ${m('critical')} × ${m('se')}`))}`,1,'interval','A point estimate supplies the centre. The margin reaches equally far in both directions.');
  [[0,4],[4,7],[7,10],[10,13]].forEach(([a,b],i)=>add(`Highlight legend (${i+1}/4)`,'Notation · A shared visual language',legend.slice(a,b).map((e,k)=>step(k,legendEntry(e))).join(''),b-a-1,'legend','Focus a legend entry to connect its symbol, meaning, and visual. This reference remains available throughout the lesson.'));
  add('Problem 1: Weekly household grocery spending','Problem 1 · What is unknown?',p(`An analyst estimates the district mean weekly household grocery bill, ${m('mean')}.`)+p(`The common ${h('point','point estimate')} is ${m('point')} = ${h('point','84')} thousand COP; known population SD is ${m('sd')} = ${h('sd','30')} thousand COP.`)+step(1,p('<strong>Question.</strong> How do sample size and confidence affect the interval’s precision and reliability?'))+step(2,p('<strong>Model assumptions.</strong> A simple random sample of independent observations (or a negligible fraction of a much larger population); known population SD; a normal population or a well approximated normal sample mean.')),2,'interval','μ is the unknown, fixed population mean. The sample estimate x̄ = 84 is not a known value of μ.');
  add('Task 1: Vary sample size','Task 1 · Change the input n',p(`Fix ${m('sd')} = ${h('sd','30')} thousand COP and ${m('confidence')} = ${h('confidence','95%')}, with ${m('critical')} = ${h('critical','1.960')}.`)+table(['ID',...ids],['<tr><th scope="row">'+m('size')+'</th>'+ns.map(n=>`<td>${h('size',n)}</td>`).join('')+'</tr>'])+p(`<strong>Calculate</strong> SE and MoE for every case.<br><strong>Draw</strong> SE vs ${m('size')}, MoE vs ${m('size')}, and MoE vs SE, with A–E coordinates.`)+step(1,p(`<strong>Relevant concepts.</strong> ${h('se','Standard error')} measures variation of sample means; ${h('margin','margin of error')} is the distance from the estimate to either interval endpoint.`)),1,'interval','Only the sample size changes. The shared estimate remains 84 thousand COP.');
  add('Task 1: From formula to case A','Task 1 · σ → SE → MoE',p(`How much uncertainty remains when ${m('size')} = ${h('size','25')}?`)+step(1,eq(`${m('se')} = ${frac(m('sd'),`√${m('size')}`)}`))+step(2,eq(`= ${frac(h('sd','30'),`√${h('size','25')}`)} = <span id="se-output">${h('se','6.000')}</span>`))+step(3,eq(`${m('margin')} = ${m('critical')} × <span id="se-input">${m('se')}</span>`))+step(4,eq(`= ${h('critical','1.960')} × ${h('se','6.000')} = ${h('margin','11.760')}`))+step(5,p('Both SE and MoE are in thousand COP. The critical value is unitless; population SD describes individual bills, while SE describes sample means.')),5,'interval','Carry the standard error into the margin: 6.000 thousand COP × 1.960 = 11.760 thousand COP.');
  add('Task 1: Calculate all five cases','Task 1 · One model, five inputs',table(['ID',m('size'),`${m('se')} = 30/√n`,`${m('margin')} = 1.960 SE`],task1Rows,'calculation-table')+p('SE and MoE: thousand COP; n: sampled households.'),5,'interval','Select a revealed case to link its calculation to the interval. Internal calculations retain unrounded values, including case D.');
  add('Standard error vs sample size','Task 1 · A diminishing return',eq(`${m('se')} = ${frac(h('sd','30'),`√${m('size')}`)}`)+p('As sample size increases, SE decreases as 1/√n.')+step(1,p(`<strong>Quadrupling ${m('size')} halves ${m('se')}.</strong>`))+step(2,eq(`${h('size','25 → 100 → 400 → 1600')}<br>${h('se','6.000 → 3.000 → 1.500 → 0.750')}`)),2,'se','Fixed axes throughout: n from 0 to 1700 households; SE from 0 to 7 thousand COP.');
  add('Margin of error vs sample size','Task 1 · Apply the fixed multiplier',eq(`${m('margin')} = ${h('critical','1.960')} × ${m('se')}`)+eq(`${m('se')} = ${frac(h('sd','30'),`√${m('size')}`)}`)+p('Larger samples give narrower intervals and greater precision at the same 95% confidence.'),0,'moe','Axis update: y now measures MoE, from 0 to 14 thousand COP. The n axis and selected sample size carry forward.');
  add('Margin of error vs standard error','Task 1 · The same cases, new coordinates',eq(`${m('margin')} = ${h('critical','1.960')} × ${m('se')}`)+p('A line through the origin: the fixed critical value is its slope.')+p('SE and MoE decrease together as 1/√n.'),0,'semoe','Coordinate change: x is now SE (thousand COP), not n. Each case becomes (SE, MoE); the slope is 1.960.');
  add('The confidence interval stays centred at 84','Task 1 · Build outward from the centre',p(`The ${h('point','point estimate')} centres the interval for the district mean ${m('mean')}.`)+eq(`${m('bounds')} = [${m('point')} − ${m('margin')}, ${m('point')} + ${m('margin')}]`)+step(1,p(`At 95% confidence: ${h('point','84')} ± ${h('critical','1.960')}(${h('sd','30')}/√${m('size')}).`))+intervalExamples,4,'interval','The same margin subtracts from and adds to 84. The endpoints change symmetrically; the estimate stays fixed.');
  add('Explanatory confidence-interval comparison','Task 1 · More households, a tighter interval',eq(`${m('se')}(${m('size')}) = ${h('sd','30')}/√${m('size')}<br>${m('margin')}(${m('size')}) = ${h('critical','1.960')} × ${m('se')}(${m('size')})<br>${h('bounds','L')}(${m('size')}) = ${h('point','84')} − ${m('margin')}(${m('size')})<br>${h('bounds','U')}(${m('size')}) = ${h('point','84')} + ${m('margin')}(${m('size')})`)+p('Same estimate and 95% confidence; larger samples reduce SE and MoE, producing narrower intervals and greater precision.')+p('<strong>Read the motion:</strong> leftward means more households. The vertical spending estimate remains at 84.')+p('Use the slider, checkpoints, or Play to follow one interval. Playback pauses at n = 25, 400, and 1600.'),0,'interval','Fixed vertical spending axis: 70–100 thousand COP/week. Sample size increases from right to left; this is a sample-size position, not a decrease in spending.');
  add('Task 2: Vary confidence','Task 2 · A–E now name confidence cases',p(`Keep ${m('size')} = ${h('size','100')} and ${m('sd')} = ${h('sd','30')} thousand COP fixed.`)+table(['ID',...ids],[`<tr><th>${m('confidence')} (%)</th>${cs.map(v=>`<td>${h('confidence',v)}</td>`).join('')}</tr>`,`<tr><th>${m('critical')}</th>${zs.map(v=>`<td>${h('critical',f(v))}</td>`).join('')}</tr>`])+p('<strong>Calculate</strong> fixed SE and the MoE for each supplied pair.<br><strong>Draw</strong> confidence vs MoE, critical value vs MoE, and confidence vs critical value; label A–E with coordinates.')+step(1,p(`The ${h('critical','critical value')} is a unitless normal cutoff. ${h('confidence','Confidence')} is the nominal long-run percentage of intervals covering ${m('mean')} under the model.`)),1,'interval','New changing input: confidence and its critical value. Locked: n = 100, σ = 30, SE = 3.000 thousand COP.');
  add('Task 2: Fixed SE, changing multiplier','Task 2 · A stable SE',eq(`${m('se')} = ${frac(m('sd'),`√${m('size')}`)}`)+step(1,eq(`= ${frac(h('sd','30'),`√${h('size','100')}`)} = ${h('se','3.000')}`))+step(2,eq(`${m('margin')} = ${m('critical')} × ${m('se')} = ${m('critical')}(${h('se','3.000')})`))+step(3,p(`For A: ${m('margin')} = ${h('critical','1.282')}(${h('se','3.000')}) = ${h('margin','3.846')} thousand COP.`))+step(4,p('SE stays fixed because neither population SD nor sample size changes. The confidence choice changes the multiplier and therefore the margin.')),4,'interval','The SE remains 3.000. Moving the critical value changes the margin, not the SE.');
  add('Task 2: Calculate all five margins','Task 2 · A multiplier controls width',table(['ID',`${m('confidence')} (%)`,m('critical'),`${m('margin')} = z* (3.000)`],task2Rows)+p('MoE: thousand COP; critical values: unitless.'),5,'interval','Choose a revealed row: larger z* produces a wider interval at the same SE and centre.');
  add('Confidence level vs margin of error','Task 2 · Coverage and precision',eq(`${m('se')} = ${h('se','3.000')} (fixed)`)+p('Higher confidence requires a larger margin: intervals widen and precision decreases.')+p('Curve: theoretical normal coverage. A–E: nominal confidence.'),0,'coverageMoe','x = MoE (thousand COP); y = confidence (%). The continuous curve uses 100[2Φ(MoE/3) − 1]. A–E use supplied nominal percentages.');
  add('Critical value vs margin of error','Task 2 · The same case, new axes',eq(`${m('critical')} = ${frac(m('margin'),h('se','3.000'))}`)+p('At fixed SE, MoE increases with z*. The relationship is linear through the origin.'),0,'zmoe','Axis update: y now measures the unitless critical value, from 0 to 3.6. x remains MoE in thousand COP. SE stays 3.000.');
  add('Confidence level vs critical value','Task 2 · Move the cutoffs, expand the area',p(`Higher confidence requires a larger ${m('critical')}.`)+p('Both normal cutoffs move outward, enclosing a larger central area.')+p('Curve: theoretical coverage. A–E: nominal confidence.'),0,'coverageZ','New x axis: unitless z*. The inset uses fixed standard-normal axes; changing confidence changes its cutoffs and enclosed area.');
  add('Reading the confidence curves','Normal coverage · From left area to centre',p(`The supplied ${m('critical')} values are rounded to three decimals.`)+eq(`${h('normal','C<sub>normal</sub>')} = 2${h('normal','Φ')}(${m('critical')}) − 1`)+step(1,p(`${h('normal','Φ(z*)')} is the area to the left of +z*.`))+step(2,p(`${h('tail','1 − Φ(z*)')} is the right tail; symmetry gives the same area in the left tail.`))+step(3,p(`Central area = 1 − 2[1 − Φ(z*)] = 2Φ(z*) − 1. With ${h('tail','α = 1 − C')}, each excluded tail is ${h('tail','α/2')}; use C as a decimal.`))+step(4,p('The curves use normal coverage; the plotted markers use nominal percentages. The small differences come from rounding the cutoffs.')),4,'normalArea','Follow the shading: left cumulative area, then symmetric tails, then the central region. Rounded cutoffs yield theoretical coverage slightly different from nominal labels.');
  add('Nominal confidence and theoretical normal coverage','Normal coverage · Rounding, made explicit',p(`The supplied ${m('critical')} values are rounded to three decimals.`)+table(['ID',`Nominal ${m('confidence')}`,m('critical'),'100[2Φ(z*) − 1]'],zs.map((z,i)=>`<tr class="reveal" data-step="${i+1}" data-row="${i}" data-task="2"><td>${caseButton(i,2)}</td><td>${h('confidence',`${cs[i]}%`)}</td><td>${h('critical',f(z))}</td><td>${h('normal',`${f(model(100,z).coverage,5)}%`)}</td></tr>`))+p('The theoretical column uses the supplied rounded cutoff, not an inverse calculation from the nominal percentage.'),5,'normal','The distribution and its axes stay fixed. All five differences are rounding effects; no magnified area scale is used.');
  [0,2,4].forEach(i=>add(`Standard normal illustration: case ${ids[i]}`,'Normal coverage · One persistent distribution',p('Z ∼ N(0, 1): the cutoffs enclose the central region.')+eq(`${h('critical',`−${f(zs[i])}`)} ≤ Z ≤ ${h('critical',`+${f(zs[i])}`)}`)+p(`Nominal ${m('confidence')} = ${h('confidence',`${cs[i]}%`)}; shaded theoretical normal coverage ${h('normal','C<sub>normal</sub>')} ≈ ${h('normal',`${f(model(100,zs[i]).coverage,5)}%`)}.`)+p('Play the transition or scrub between checkpoints. The curve’s shape and axes remain fixed.'),0,'normal',`Case ${ids[i]} checkpoint: nominal ${cs[i]}%, theoretical ${f(model(100,zs[i]).coverage,5)}%. Live readouts follow the current cutoffs during a transition.`));
  add('What changes, and what stays fixed?','Synthesis · Two dependency chains',p('<strong>Task 1: same confidence, more observations.</strong>')+eq(`${m('se')} ∼ ${m('margin')} ∼ 1/√${m('size')}`)+p('Larger samples give narrower intervals and greater precision at the same 95% confidence.')+step(1,p(`<strong>Task 2: same SE, greater confidence.</strong><br>Higher ${m('confidence')} requires a larger ${m('critical')}, producing a larger ${m('margin')}, wider intervals, and lower precision.`))+step(2,p(`<strong>The components work together.</strong><br>The ${h('point','84')} thousand COP point estimate supplies the centre; critical value and SE determine the margin. Confidence describes the procedure’s long-run reliability under the model assumptions.`))+step(2,p('Across repeated samples, the stated percentage of intervals constructed by this procedure cover the fixed population mean. It does not assign a probability to μ in this one realized interval.')),2,'interval','Play a short recap. Step 1 varies n at 95% confidence; step 2 varies z* at SE = 3.000. The point estimate always supplies the centre.');

  const state={index:0,steps:Array(26).fill(0),n:25,z:1.282,raf:0,playing:false,elapsed:0,normalZ:1.282,focusRole:'point',schedule:null,build:1};
  const reducedQuery=matchMedia('(prefers-reduced-motion: reduce)');
  const reduced=()=>$('#reduce-motion').checked;
  $('#reduce-motion').checked=reducedQuery.matches;
  const active=()=>slides[state.index];
  $('#slides').innerHTML=slides.map((s,i)=>`<section class="slide" id="slide-${i+1}" aria-labelledby="title-${i+1}" ${i?'hidden':''}>${i?`<p class="eyebrow">${s.chapter}</p><h2 id="title-${i+1}" tabindex="-1">${s.title}</h2>`:''}${s.body}</section>`).join('');
  $('#slide-1 h1').id='title-1';$('#slide-1 h1').tabIndex=-1;
  $('#slide-select').innerHTML=slides.map((s,i)=>`<option value="${i}">${i+1} / 26 · ${s.title}</option>`).join('');
  $('#reference-entries').innerHTML=legend.map(legendEntry).join('');
  function task2(){return state.index>=14&&state.index<=24 || state.index===25&&state.steps[25]>=1;}
  function current(){return model(task2()?100:state.n,task2()?(active().mode.startsWith('normal')?state.normalZ:state.z):1.960);}
  function stop(){cancelAnimationFrame(state.raf);state.raf=0;state.playing=false;state.build=1;$('#play').textContent='Play';$('#play').setAttribute('aria-pressed','false');$('#play-status').textContent='Paused';document.querySelectorAll('.flow-token').forEach(e=>e.remove());}
  function applyReveal(){
    const slide=$(`#slide-${state.index+1}`),level=state.steps[state.index];
    slide.querySelectorAll('[data-step]').forEach(el=>{const show=+el.dataset.step<=level;el.hidden=!show;el.classList.toggle('is-new',show&&+el.dataset.step===level);});
    $('#step-progress').textContent=`Slide ${state.index+1} / 26 · Reveal ${level+1} / ${active().steps+1}`;
    $('#next').textContent=level<active().steps?'Reveal next':state.index===25?'Lesson complete':'Next slide';
    $('#next').disabled=state.index===25&&level===active().steps;
    $('#previous').disabled=state.index===0&&level===0;
    if(state.index===7)state.n=25;
    if(state.index===8&&level>0)state.n=ns[level-1];
    if(state.index===12&&level>=2)state.n=[25,400,1600][level-2];
    if((state.index===16||state.index===21)&&level>0){state.z=zs[level-1];state.normalZ=state.z;}
    if(state.index===15)state.z=1.282;
  }
  function flySE(){
    if(reduced())return;
    const from=$('#se-output').getBoundingClientRect(),to=$('#se-input').getBoundingClientRect();
    const token=document.createElement('span');token.className='flow-token';token.textContent='6.000';token.style.left=`${from.left}px`;token.style.top=`${from.top}px`;document.body.append(token);
    const anim=token.animate([{transform:'translate(0,0)'},{transform:`translate(${to.left-from.left}px,${to.top-from.top}px)`}],{duration:900,easing:'ease-in-out',fill:'forwards'});anim.finished.then(()=>token.remove()).catch(()=>{});
  }
  function reveal(direction){
    stop();state.schedule=null;state.elapsed=0;const index=state.index;
    if(direction>0){if(state.steps[index]<active().steps){state.steps[index]++;applyReveal();configure();draw();if(index===7&&state.steps[index]===3)flySE();if(index===12&&state.steps[index]===1)buildInterval();}else go(index+1);}
    else if(state.steps[index]>0){state.steps[index]--;applyReveal();configure();draw();}else go(index-1,true);
  }
  function buildInterval(){
    if(reduced())return;
    const began=performance.now();
    function tick(now){const t=Math.min(1,(now-began)/1200);state.build=t*t*(3-2*t);draw();if(t<1)state.raf=requestAnimationFrame(tick);else state.raf=0;}
    state.raf=requestAnimationFrame(tick);
  }
  function go(index,back=false){
    if(index<0||index>=slides.length)return;
    stop();const old=state.index;state.index=index;
    document.querySelectorAll('.slide').forEach((el,i)=>el.hidden=i!==index);
    if(back)state.steps[index]=slides[index].steps;
    if(index===14&&old<14){state.z=1.282;state.normalZ=1.282;}
    if(index===22&&!(old>=22&&old<=24))state.normalZ=zs[0];
    if(index===23&&!(old>=22&&old<=24))state.normalZ=zs[2];
    if(index===24&&!(old>=22&&old<=24))state.normalZ=zs[4];
    state.elapsed=0;state.schedule=null;
    $('#chapter').textContent=active().chapter;$('#slide-select').value=index;
    $('#progress').style.width=`${100*(index+1)/26}%`;
    $('#stage-caption').textContent=active().caption;
    $('#navigation-status').textContent=`Slide ${index+1} of 26. ${active().title}`;
    history.replaceState(null,'',`#slide-${index+1}`);
    applyReveal();configure();draw();
    if(innerWidth<901)window.scrollTo({top:0,behavior:'instant'});
  }
  function config(){
    if(task2())return {min:1.282,max:3.291,step:.001,label:'Critical value z* (unitless)',value:active().mode.startsWith('normal')?state.normalZ:state.z,values:zs,labels:ids.map((id,i)=>`${id}: ${cs[i]}% · ${f(zs[i])}`)};
    return {min:25,max:1600,step:1,label:'Sample size n (households)',value:state.n,values:ns,labels:ids.map((id,i)=>`${id}: n = ${ns[i]}`)};
  }
  function configure(){
    const c=config(),slider=$('#scrubber');Object.assign(slider,{min:c.min,max:c.max,step:c.step,value:c.value});$('#slider-label').textContent=c.label;slider.style.accentColor=task2()?colors.critical:colors.size;
    $('#demo-controls').hidden=active().mode==='legend'||state.index===0||state.index===5;
    $('#checkpoints').innerHTML=c.values.map((v,i)=>`<button data-checkpoint="${v}" aria-pressed="false">${c.labels[i]}</button>`).join('');
    $('#locks').innerHTML=task2()?`Locked: ${m('size')} = 100 · ${m('sd')} = 30 · ${m('se')} = 3.000`:`Locked: ${m('sd')} = 30 · ${m('confidence')} = 95% · ${m('critical')} = 1.960`;
    if(state.index<6)$('#locks').textContent=state.index===5?'Weekly spending · thousand COP':'A shared semantic color map';
    $('#play-status').textContent=reduced()?'Reduced motion: use checkpoints or scrub.':'Ready · teacher controlled';
  }
  function setInput(value){if(task2()){state.z=value;state.normalZ=value;}else state.n=Math.round(value);draw();}
  function timeline(){
    if(task2()){
      if(state.index>=22&&state.index<=24){const target=zs[[0,2,4][state.index-22]];return [{v:state.normalZ,hold:400},{v:target,hold:1200}];}
      return zs.map(v=>({v,hold:650}));
    }
    return (state.index===13?[25,400,1600]:ns).map(v=>({v,hold:state.index===13?1200:650}));
  }
  function play(restart=false){
    if(state.playing&&!restart){stop();return;}
    stop();
    if(reduced()){setInput(timeline().at(-1).v);$('#play-status').textContent='Final checkpoint · reduced motion';return;}
    const frames=timeline();
    if(restart){state.elapsed=0;if(state.index>=22&&state.index<=24)frames[0].v=state.index===22?zs[0]:zs[state.index===23?0:2];}
    if(restart)state.schedule=null;
    let segments,total;
    if(state.schedule){({segments,total}=state.schedule);}else{
      segments=[];total=0;
      frames.forEach((frame,i)=>{if(i){segments.push({start:total,end:total+2200,a:frames[i-1].v,b:frame.v,moving:true});total+=2200;}segments.push({start:total,end:total+frame.hold,a:frame.v,b:frame.v,moving:false});total+=frame.hold;});
      state.schedule={segments,total};
    }
    const t=total;
    if(state.elapsed>=t)state.elapsed=0;
    const began=performance.now()-state.elapsed;state.playing=true;$('#play').textContent='Pause';$('#play').setAttribute('aria-pressed','true');
    function tick(now){
      if(!state.playing)return;
      state.elapsed=Math.min(now-began,t);const seg=segments.find(s=>state.elapsed<=s.end)||segments.at(-1),u=Math.max(0,Math.min(1,(state.elapsed-seg.start)/(seg.end-seg.start))),ease=u*u*(3-2*u);
      let value=seg.a+(seg.b-seg.a)*ease;
      // In confidence mode move uniformly in exact theoretical coverage, then invert.
      if(task2()&&seg.moving){const coverage=(2*cdf(seg.a)-1)+(2*cdf(seg.b)-2*cdf(seg.a))*ease;value=invCdf((1+coverage)/2);}
      setInput(value);$('#play-status').textContent=seg.moving?'Playing':'Checkpoint';
      if(state.elapsed<t)state.raf=requestAnimationFrame(tick);else{stop();$('#play-status').textContent='Complete · replay available';}
    }
    state.raf=requestAnimationFrame(tick);
  }

  const svgNS='http://www.w3.org/2000/svg';
  function element(tag,attrs={},text=''){const el=document.createElementNS(svgNS,tag);Object.entries(attrs).forEach(([k,v])=>el.setAttribute(k,v));el.textContent=text;return el;}
  function text(parent,x,y,value,cls='',anchor='start'){
    const label=element('text',{x,y,class:cls,'text-anchor':anchor},value);
    if(cls==='axis-title'){
      if(value.startsWith('SE '))label.style.fill='#867729';
      else if(value.startsWith('MoE '))label.style.fill='#b66812';
      else if(value.startsWith('n '))label.style.fill=colors.size;
      else if(value.startsWith('z* '))label.style.fill=colors.critical;
      else if(value.startsWith('Confidence'))label.style.fill='#2b6478';
    }
    parent.append(label);
  }
  function path(points){return points.map((pt,i)=>`${i?'L':'M'}${pt[0].toFixed(3)},${pt[1].toFixed(3)}`).join(' ');}
  let chartKey='';let chart=null;
  function axes(key,xmax,ymin,ymax,xlabel,ylabel,xTicks,yTicks){
    const x=v=>90+v/xmax*620,y=v=>355-(v-ymin)/(ymax-ymin)*285;
    if(chartKey===key)return {x,y};
    chartKey=key;const a=$('#axes');a.replaceChildren();$('#points').replaceChildren();$('#guide').replaceChildren();
    xTicks.forEach(v=>{a.append(element('path',{d:`M${x(v)} 70V355`,class:'grid'}));text(a,x(v),382,v,'tick','middle');});
    yTicks.forEach(v=>{a.append(element('path',{d:`M90 ${y(v)}H710`,class:'grid'}));text(a,78,y(v)+6,v,'tick','end');});
    a.append(element('path',{d:'M90 60V355H720',class:'axis'}));text(a,400,420,xlabel,'axis-title','middle');text(a,90,35,ylabel,'axis-title');
    return {x,y};
  }
  function normalPath(z,offset={x:0,y:0,scale:1}){
    const x=v=>offset.x+(90+(v+4)/8*620)*offset.scale,y=v=>offset.y+(355-v/.46*285)*offset.scale;
    const pdf=v=>Math.exp(-v*v/2)/Math.sqrt(2*Math.PI);
    const points=Array.from({length:241},(_,i)=>{const v=-4+i/30;return [x(v),y(pdf(v))];});
    return {curve:path(points),area:path([[x(-z),y(0)],...Array.from({length:161},(_,i)=>{const v=-z+2*z*i/160;return [x(v),y(pdf(v))];}),[x(z),y(0)]])+'Z',x,y,pdf};
  }
  function drawNormal(q,areaMode=false){
    const key=areaMode?'normalArea':'normal';
    if(chartKey!==key){chartKey=key;$('#axes').replaceChildren();$('#points').replaceChildren();$('#guide').replaceChildren();const a=$('#axes');
      const x=v=>90+(v+4)/8*620,y=v=>355-v/.46*285;
      a.append(element('path',{d:'M90 65V355H720',class:'axis'}));[-4,-3,-2,-1,0,1,2,3,4].forEach(v=>text(a,x(v),382,v,'tick','middle'));[0,.2,.4].forEach(v=>text(a,78,y(v)+5,v,'tick','end'));
      text(a,400,425,'z (unitless)','axis-title','middle');text(a,90,35,'Standard normal density · Z ∼ N(0, 1)','axis-title');
    }
    const n=normalPath(q.z);$('#curve').setAttribute('d',n.curve);$('#curve').style.stroke='#132a3e';$('#area').setAttribute('d',n.area);$('#area').style.fill='#c8edf9';
    const x=n.x,y=n.y;
    if(areaMode){const level=state.steps[20];if(level===1){const pts=Array.from({length:181},(_,i)=>{const v=-4+(q.z+4)*i/180;return [x(v),y(n.pdf(v))];});$('#area').setAttribute('d',path([[x(-4),y(0)],...pts,[x(q.z),y(0)]])+'Z');$('#area').style.fill='#a8d8e9';}else if(level===2){const tail=(a,b)=>path([[x(a),y(0)],...Array.from({length:101},(_,i)=>{const v=a+(b-a)*i/100;return [x(v),y(n.pdf(v))];}),[x(b),y(0)]])+'Z';$('#area').setAttribute('d',tail(-4,-q.z)+' '+tail(q.z,4));$('#area').style.fill='#408ed8';}}
    $('#cutoffs').setAttribute('d',`M${x(-q.z)} 355V${y(.36)} M${x(q.z)} 355V${y(.36)}`);
    $('#marker').setAttribute('cx',x(q.z));$('#marker').setAttribute('cy',355);
    setText($('#upper'),x(-q.z),y(.39),`−${f(q.z)}`,'middle');setText($('#lower'),x(q.z),y(.39),`+${f(q.z)}`,'middle');
    const g=$('#guide');g.replaceChildren();
    const label=areaMode&&state.steps[20]===1?`Φ(z*) = ${f(cdf(q.z),7)}`:areaMode&&state.steps[20]===2?`Each tail = ${f((1-cdf(q.z))*100,5)}%`:`Central area = ${f(q.coverage,5)}%`;
    text(g,400,240,label,'axis-title','middle');
  }
  function setText(el,x,y,value,anchor='start'){el.setAttribute('x',x);el.setAttribute('y',y);el.setAttribute('text-anchor',anchor);el.textContent=value;}
  function drawInterval(q){
    $('#curve').setAttribute('d','');
    const axis=axes('interval',1,70,100,'Larger sample size  ⟵  smaller sample size','Spending (1000 COP/week)',[],[70,75,80,84,90,95,100]);
    const y=axis.y,x=state.index===13?650-(q.n-25)/1575*510:400;
    if(!$('#axes .reference-line')){const a=$('#axes');a.append(element('path',{d:`M90 ${y(84)}H710`,class:'reference-line'}));text(a,400,58,'Shared estimate x̄ = 84 · C = 95%','axis-title','middle');}
    const titles=$('#axes').querySelectorAll('.axis-title');
    titles[0].textContent=state.index===13?'Larger sample size  ⟵  smaller sample size':'The estimate stays at 84 thousand COP';
    titles[titles.length-1].textContent=`Shared estimate x̄ = 84 · ${task2()?'SE = 3.000':'C = 95%'}`;
    const r=state.index===12?(state.steps[12]===0?0:state.build):1;
    const uy=y(84+(q.u-84)*r),ly=y(84+(q.l-84)*r);
    $('#interval').setAttribute('d',`M${x} ${uy}V${ly} M${x-16} ${uy}H${x+16} M${x-16} ${ly}H${x+16}`);
    $('#marker').setAttribute('cx',x);$('#marker').setAttribute('cy',y(84));
    setText($('#upper'),x+23,uy-8,r===1?f(q.u):'84 + MoE');setText($('#lower'),x+23,ly+24,r===1?f(q.l):'84 − MoE');
    const g=$('#guide');g.replaceChildren();
    if(state.index===13){[[25,650],[400,650-375/1575*510],[1600,140]].forEach(([v,px])=>text(g,px,382,`n=${v}`,'tick','middle'));}
    else {text(g,400,382,`x̄ − MoE       84       x̄ + MoE`,'tick','middle');}
  }
  function drawRelation(q,mode){
    const definitions={
      se:{xmax:1700,ymin:0,ymax:7,xlabel:'n (sampled households)',ylabel:'SE (thousand COP)',xt:[0,425,850,1275,1700],yt:[0,1,2,3,4,5,6,7],fn:n=>30/Math.sqrt(n),lo:25,hi:1600,c:'#867729',coord:v=>[v.n,v.se]},
      moe:{xmax:1700,ymin:0,ymax:14,xlabel:'n (sampled households)',ylabel:'MoE (thousand COP)',xt:[0,425,850,1275,1700],yt:[0,2,4,6,8,10,12,14],fn:n=>58.8/Math.sqrt(n),lo:25,hi:1600,c:'#b66812',coord:v=>[v.n,v.moe]},
      semoe:{xmax:7,ymin:0,ymax:14,xlabel:'SE (thousand COP)',ylabel:'MoE (thousand COP)',xt:[0,1,2,3,4,5,6,7],yt:[0,2,4,6,8,10,12,14],fn:x=>1.960*x,lo:0,hi:6,c:'#b66812',coord:v=>[v.se,v.moe]},
      coverageMoe:{xmax:11,ymin:79,ymax:101,xlabel:'MoE (thousand COP)',ylabel:'Confidence (%)',xt:[0,2,4,6,8,10],yt:[80,85,90,95,99.9],fn:x=>100*(2*cdf(x/3)-1),lo:3.82,hi:10.2,c:'#2b6478',coord:v=>[v.moe,v.coverage]},
      zmoe:{xmax:11,ymin:0,ymax:3.6,xlabel:'MoE (thousand COP)',ylabel:'z* (unitless)',xt:[0,2,4,6,8,10],yt:[0,1,2,3],fn:x=>x/3,lo:0,hi:9.873,c:'#2648bb',coord:v=>[v.moe,v.z]},
      coverageZ:{xmax:3.6,ymin:79,ymax:101,xlabel:'z* (unitless)',ylabel:'Confidence (%)',xt:[0,1,2,3],yt:[80,85,90,95,99.9],fn:x=>100*(2*cdf(x)-1),lo:1.274,hi:3.4,c:'#2b6478',coord:v=>[v.z,v.coverage]}
    };
    const d=definitions[mode],isNew=chartKey!==mode,a=axes(mode,d.xmax,d.ymin,d.ymax,d.xlabel,d.ylabel,d.xt,d.yt);
    if(isNew){
      $('#curve').setAttribute('d',path(Array.from({length:241},(_,i)=>{const v=d.lo+(d.hi-d.lo)*i/240;return [a.x(v),a.y(d.fn(v))];})));$('#curve').style.stroke=d.c;
      (task2()?zs.map(z=>model(100,z)):ns.map(n=>model(n,1.960))).forEach((v,i)=>{let [px,py]=d.coord(v);if(mode.startsWith('coverage'))py=cs[i];const g=$('#points');g.append(element('circle',{cx:a.x(px),cy:a.y(py),r:5}));text(g,a.x(px)+9,a.y(py)-9,ids[i],'coordinate');});
    }
    const [cx,cy]=d.coord(q);$('#marker').setAttribute('cx',a.x(cx));$('#marker').setAttribute('cy',a.y(cy));
    const g=$('#guide');g.replaceChildren();g.append(element('path',{d:`M${a.x(cx)} 355V${a.y(cy)}H90`}));
    const coordinateText=mode==='se'||mode==='moe'?`(${q.n}, ${f(cy)})`:`(${f(cx)}, ${f(cy,mode.startsWith('coverage')?5:3)})`;
    text(g,400,58,`Selected coordinates: ${coordinateText}`,'axis-title','middle');
    if(mode==='coverageMoe'||mode==='zmoe'){
      // Small horizontal interval uses its own explicitly labeled spending axis.
      const y=315,xx=v=>360+(v-70)/30*330;
      g.append(element('path',{d:`M360 ${y}H690`,class:'axis'}));text(g,525,300,'Spending 70–100 (thousand COP)','tick','middle');
      g.append(element('path',{d:`M${xx(q.l)} ${y-12}V${y+12} M${xx(q.l)} ${y}H${xx(q.u)} M${xx(q.u)} ${y-12}V${y+12}`,stroke:'#b56812','stroke-width':4}));g.append(element('circle',{cx:xx(84),cy:y,r:5,fill:'#56791e',stroke:'none'}));
    }
    if(mode==='coverageZ'){
      const n=normalPath(q.z,{x:260,y:210,scale:.53});const inset=element('g');inset.append(element('rect',{x:290,y:235,width:400,height:110,fill:'#f6f9fa',stroke:'none'}));inset.append(element('path',{d:n.area,fill:'#c8edf9',stroke:'none'}));inset.append(element('path',{d:n.curve,fill:'none',stroke:'#132a3e','stroke-width':2}));inset.append(element('path',{d:`M${n.x(-q.z)} ${n.y(0)}V${n.y(.34)} M${n.x(q.z)} ${n.y(0)}V${n.y(.34)}`,stroke:'#2648bb','stroke-width':2}));text(inset,475,330,'Fixed N(0,1) · z from −4 to 4','tick','middle');g.append(inset);
    }
    // All source coordinates stay readable outside the dense plot labels.
    $('#stage-caption').innerHTML=active().caption+'<br><span class="small">'+(task2()?zs.map(z=>model(100,z)):ns.map(n=>model(n,1.960))).map((v,i)=>{let [x,y]=d.coord(v);if(mode.startsWith('coverage'))y=cs[i];return `${ids[i]}: (${mode==='se'||mode==='moe'?x:f(x)}, ${mode.startsWith('coverage')?y:f(y)})`;}).join(' · ')+'</span>';
  }
  function drawLegend(){
    const role=state.focusRole||'point';
    if(['critical','confidence','tail','normal'].includes(role)){drawNormal(model(100,1.960));}
    else drawInterval(model(25,1.960));
    const found=legend.find(e=>e[0]===role);$('#stage-label').textContent=found?found[2]:'A shared visual language';
    if(role==='mean'){$('#upper').textContent='μ remains unknown';$('#lower').textContent='x̄ = 84 estimates μ';}
    if(role==='sd'){$('#upper').textContent='σ = 30: individual bills';$('#lower').textContent='SE = 6: sample means';}
    if(role==='size'){$('#upper').textContent='n = 25 households';}
    if(role==='width'){$('#upper').textContent='W = 2MoE = 23.520';}
  }
  function draw(){
    const q=current(),mode=active().mode;
    $('#area').setAttribute('d','');$('#cutoffs').setAttribute('d','');$('#interval').setAttribute('d','');$('#upper').textContent='';$('#lower').textContent='';
    if(!mode.startsWith('normal')&&mode!=='legend'&&mode==='interval')$('#curve').setAttribute('d','');
    $('#stage-label').textContent=mode.startsWith('normal')?'Fixed standard normal distribution':task2()?'Task 2 · Confidence changes the multiplier':'Task 1 · Sample size changes the standard error';
    if(mode==='legend')drawLegend();else if(mode.startsWith('normal'))drawNormal(q,mode==='normalArea');else if(mode==='interval')drawInterval(q);else drawRelation(q,mode);
    $('#diagram-title').textContent=active().title;
    $('#diagram-description').textContent=mode.startsWith('normal')?`Fixed standard normal curve. Cutoffs minus and plus ${f(q.z)} enclose ${f(q.coverage,5)} percent of the theoretical area.`:mode==='interval'?`One interval on a fixed spending axis, centred at 84. Sample size ${q.n}, lower limit ${f(q.l)}, upper limit ${f(q.u)} thousand COP.`:active().caption;
    const nominalIndex=zs.findIndex(z=>Math.abs(q.z-z)<1e-8);
    if(task2())$('#stage-label').textContent=nominalIndex>=0?`Nominal C = ${cs[nominalIndex]}% · normal coverage = ${f(q.coverage,5)}%`:`Continuous theoretical coverage = ${f(q.coverage,5)}%`;
    const readouts=mode.startsWith('normal')?[
      ['critical','z*',f(q.z)],['confidence','Nominal C',nominalIndex>=0?`${cs[nominalIndex]}%`:'—'],['normal','Normal coverage',`${f(q.coverage,5)}%`],['normal','Φ(z*)',f(cdf(q.z),7)],['tail','Each tail',`${f((1-cdf(q.z))*100,5)}%`],['point','Estimate x̄','84']
    ]:[task2()?['critical','z*',f(q.z)]:['size','n',q.n],['se','SE',f(q.se)],['margin','MoE',f(q.moe)],['bounds','L',f(q.l)],['point','Centre x̄','84'],['bounds','U',f(q.u)]];
    $('#readouts').innerHTML=readouts.map(([r,label,value])=>`<div style="--role:${colors[r]}"><dt>${label}</dt><dd>${value}</dd></div>`).join('');
    if(mode==='legend')$('#readouts').hidden=true;else $('#readouts').hidden=false;
    const c=config();$('#scrubber').value=c.value;$('#scrubber').setAttribute('aria-valuetext',task2()?`Critical value ${f(c.value)}, theoretical normal coverage ${f(q.coverage,5)} percent`:`${q.n} households; standard error ${f(q.se)}; margin ${f(q.moe)} thousand COP`);
    $('#checkpoints').querySelectorAll('button').forEach(b=>b.setAttribute('aria-pressed',Math.abs(+b.dataset.checkpoint-c.value)<1e-8));
    const caseIndex=task2()?zs.findIndex(z=>Math.abs(z-q.z)<1e-8):ns.indexOf(q.n);
    $(`#slide-${state.index+1}`).querySelectorAll('[data-row]').forEach(row=>row.classList.toggle('active-row',+row.dataset.row===caseIndex));
    document.querySelectorAll('[data-case]').forEach(b=>b.setAttribute('aria-pressed',+b.dataset.case===caseIndex&&+b.dataset.task===(task2()?2:1)));
    $('#locks').querySelectorAll('mark').forEach(el=>el.classList.toggle('focus-match',el.dataset.role===state.focusRole));
  }
  $('#next').addEventListener('click',()=>reveal(1));$('#previous').addEventListener('click',()=>reveal(-1));
  $('#slide-select').addEventListener('change',e=>go(+e.target.value));
  $('#scrubber').addEventListener('input',e=>{stop();state.elapsed=0;state.schedule=null;setInput(+e.target.value);});
  $('#play').addEventListener('click',()=>play());$('#replay').addEventListener('click',()=>play(true));
  $('#checkpoints').addEventListener('click',e=>{const b=e.target.closest('[data-checkpoint]');if(b){stop();state.elapsed=0;state.schedule=null;setInput(+b.dataset.checkpoint);$('#play-status').textContent='Checkpoint selected';}});
  document.addEventListener('click',e=>{const b=e.target.closest('[data-case]');if(b){stop();state.schedule=null;state.elapsed=0;const i=+b.dataset.case;if(+b.dataset.task===1)state.n=ns[i];else {state.z=zs[i];state.normalZ=zs[i];}draw();}});
  function focusRole(e){const b=e.target.closest('[data-focus-role]');if(!b)return;state.focusRole=b.dataset.focusRole;document.querySelectorAll('mark').forEach(mark=>mark.classList.toggle('focus-match',mark.dataset.role===state.focusRole));if(active().mode==='legend')draw();}
  document.addEventListener('focusin',focusRole);document.addEventListener('pointerover',focusRole);
  $('#reference-open').addEventListener('click',()=>{stop();$('#reference').showModal();});$('#reference-close').addEventListener('click',()=>$('#reference').close());
  async function fullscreen(){try{if(document.fullscreenElement)await document.exitFullscreen();else await $('#presentation').requestFullscreen();}catch{$('#navigation-status').textContent='Fullscreen is unavailable in this browser. Use the browser fullscreen command.';}}
  $('#fullscreen').addEventListener('click',fullscreen);
  document.addEventListener('fullscreenchange',()=>{const full=!!document.fullscreenElement;$('#fullscreen').setAttribute('aria-pressed',full);$('#fullscreen').textContent=full?'Exit fullscreen':'Enter fullscreen';});
  function motionChange(){stop();$('#presentation').classList.toggle('reduced-motion',reduced());configure();}
  $('#reduce-motion').addEventListener('change',motionChange);reducedQuery.addEventListener('change',e=>{$('#reduce-motion').checked=e.matches;motionChange();});
  document.addEventListener('keydown',e=>{
    if($('#reference').open||e.target.closest('input,select,textarea,[contenteditable],[role="slider"],[role="spinbutton"],[role="combobox"]')||e.altKey||e.ctrlKey||e.metaKey)return;
    if(e.key===' '&&e.target.closest('button,a'))return;
    if(['ArrowRight','PageDown',' ','ArrowLeft','PageUp','Home','End','f','F','r','R'].includes(e.key))e.preventDefault();
    if(['ArrowRight','PageDown',' '].includes(e.key))reveal(1);if(['ArrowLeft','PageUp'].includes(e.key))reveal(-1);
    if(e.key==='Home')go(0);if(e.key==='End')go(25);if(e.key.toLowerCase()==='f')fullscreen();if(e.key.toLowerCase()==='r')play(true);
  });
  document.addEventListener('visibilitychange',()=>{if(document.hidden)stop();});
  window.addEventListener('pagehide',stop);
  const initial=/^#slide-(\d+)$/.exec(location.hash);go(initial?Math.max(0,Math.min(25,+initial[1]-1)):0);
})();
