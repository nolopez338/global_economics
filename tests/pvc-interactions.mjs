import {Design, validate, vec, quat, rectangle, port} from '../assets/js/pvc-model.mjs';
const iframe=document.querySelector('#app'), results=document.querySelector('#results');
let w,d,c,api;
const assert=(ok,message)=>{if(!ok)throw Error(message);};
const near=(a,b,t=1e-6)=>Math.abs(a-b)<t;
const same=(a,b)=>JSON.stringify(a)===JSON.stringify(b);
const tick=()=>new Promise(resolve=>requestAnimationFrame(()=>requestAnimationFrame(resolve)));
async function load(model=new Design()){
  localStorage.setItem('pvc-studio-browser-test',JSON.stringify(model.data()));
  iframe.src='/tests/.pvc-browser/pvc_design.html'+'?test='+Math.random();
  await new Promise(resolve=>iframe.onload=resolve);
  w=iframe.contentWindow;d=w.document;
  for(let i=0;i<120&&!w.pvcTest;i++)await tick();
  assert(w.pvcTest,'App did not initialize');api=w.pvcTest;c=d.querySelector('canvas');await tick();
}
const state=()=>api.read();
function click(selector){d.querySelector(selector).click();}
function change(selector,value){const el=d.querySelector(selector);el.value=value;el.dispatchEvent(new w.Event('change',{bubbles:true}));}
function key(key,target=c,extra={}){target.dispatchEvent(new w.KeyboardEvent('keydown',{key,bubbles:true,cancelable:true,...extra}));}
function pointer(type,p,extra={}){c.dispatchEvent(new w.PointerEvent(type,{clientX:p.x,clientY:p.y,pointerId:1,pointerType:'mouse',button:0,buttons:type==='pointerup'?0:1,bubbles:true,cancelable:true,...extra}));}
function tap(p,extra={}){pointer('pointerdown',p,extra);pointer('pointerup',p,extra);}
function double(p){tap(p);tap(p);c.dispatchEvent(new w.MouseEvent('dblclick',{clientX:p.x,clientY:p.y,button:0,bubbles:true}));}
async function drag(a,b,extra={}){pointer('pointerdown',a,extra);for(let i=1;i<=6;i++){pointer('pointermove',{x:a.x+(b.x-a.x)*i/6,y:a.y+(b.y-a.y)*i/6},extra);await tick();}pointer('pointerup',b,extra);await tick();}
const screen=p=>api.screen(p);
async function test(name,fn){const li=document.createElement('li');results.append(li);try{await fn();li.textContent='PASS · '+name;}catch(e){li.className='fail';li.textContent='FAIL · '+name+': '+e.message;console.error(e);}}
function connectedPair(){const m=new Design(),t=m.add('tube',[0,120,0]),e=m.add('elbow90');m.connect({id:e.id,port:0},{id:t.id,port:1});return m;}

localStorage.removeItem('pvc-studio-browser-test-increment');
await test('Q/E preview world axes; default 90°; placement creates one history entry',async()=>{
  await load();click('[data-type="corner"]');key('q');key('e');
  const q=quat([0,0,0,1]).setFromAxisAngle(vec([1,0,0]),Math.PI/2).multiply(quat([0,0,0,1]).setFromAxisAngle(vec([0,1,0]),Math.PI/2));
  assert(near(Math.abs(quat(state().placement.q).dot(q)),1),'Preview rotation axes');
  assert(state().undo===0,'Preview modified history');tap(screen([0,0,0]));assert(state().data.pieces.length===1&&state().undo===1,'Placement history');
});
await test('Presets and custom positive increment; labels, world Q/E selection, one undo each, persistence',async()=>{
  for(const v of ['15','30','45','90']){change('#rotation-increment',v);assert(state().rotationIncrement===Number(v),'Preset '+v);}
  change('#rotation-increment','custom');change('#rotation-custom','22.5');
  assert(d.querySelector('[data-rotation-label="Horizontal"]').textContent.includes('22.5°'),'Label');
  const before=state();key('q');key('e');assert(state().undo===before.undo+2,'Discrete history count');
  const q=quat([0,0,0,1]).setFromAxisAngle(vec([1,0,0]),Math.PI/8).multiply(quat([0,0,0,1]).setFromAxisAngle(vec([0,1,0]),Math.PI/8)).multiply(quat(before.data.pieces[0].q));
  assert(near(Math.abs(quat(state().data.pieces[0].q).dot(q)),1),'Selected Q/E world axes');
  key('z',c,{ctrlKey:true});key('z',c,{ctrlKey:true});assert(same(state().data,before.data),'Undo rotations');
  key('z',c,{ctrlKey:true,shiftKey:true});key('z',c,{ctrlKey:true,shiftKey:true});
  change('#rotation-custom','0');assert(state().rotationIncrement===22.5,'Accepted zero');
  change('#rotation-custom','-10');assert(state().rotationIncrement===22.5,'Accepted negative');
  await load();assert(state().rotationIncrement===22.5,'Preference reload');
});
await test('Rigid connected assembly and disconnected multiselection rotations retain joints and relative arrangement',async()=>{
  const m=connectedPair();m.add('tee',[0,120,350]);await load(m);click('#select-all');
  const before=state();key('q');key('e');const after=state();validate(after.data);
  const distances=data=>data.pieces.flatMap((p,i)=>data.pieces.slice(i+1).map(o=>vec(p.p).distanceTo(vec(o.p))));
  assert(distances(before.data).every((v,i)=>near(v,distances(after.data)[i])),'Relative spacing');
  for(let i=1;i<before.data.pieces.length;i++){
    const rel=s=>quat(s.data.pieces[0].q).invert().multiply(quat(s.data.pieces[i].q));
    assert(near(Math.abs(rel(before).dot(rel(after))),1),'Relative orientation');
  }
  assert(after.data.connections.length===1&&after.undo===2,'Connections/history');
});
await test('Normal left drag pans over a piece without selection or geometry changes; small motion clicks; right drag orbits; wheel zooms',async()=>{
  await load(connectedPair());const before=state(),p=screen(before.data.pieces[0].p);
  await drag(p,{x:p.x+60,y:p.y+40});assert(!same(state().target,before.target),'No pan');assert(same(state().data,before.data)&&!state().selected.length&&state().undo===0,'Pan edited/selected pieces');
  const at=screen(state().data.pieces[0].p);pointer('pointerdown',at);pointer('pointermove',{x:at.x+2,y:at.y+1});pointer('pointerup',{x:at.x+2,y:at.y+1});assert(state().selected.length===1,'Small-motion click');
  const b=state();await drag(at,{x:at.x+70,y:at.y+20},{button:2,buttons:2});assert(!same(state().cameraQ,b.cameraQ),'No right orbit');assert(same(state().data,b.data),'Orbit edited geometry');
  const pos=state().camera;c.dispatchEvent(new w.WheelEvent('wheel',{deltaY:120,bubbles:true,cancelable:true}));await tick();assert(!same(state().camera,pos),'No zoom');
});
await test('Click, Shift-click toggle, and explicit marquee preserve selection semantics',async()=>{
  const m=new Design();m.add('tube',[-300,100,0]);m.add('tube',[300,100,0]);await load(m);change('#camera','top');await tick();
  tap(screen(m.pieces[0].p));assert(state().selected.length===1,'Click');tap(screen(m.pieces[1].p),{shiftKey:true});assert(state().selected.length===2,'Shift add');tap(screen(m.pieces[0].p),{shiftKey:true});assert(state().selected.length===1,'Shift remove');
  click('[data-tool="marquee"]');const r=c.getBoundingClientRect();await drag({x:r.left+5,y:r.top+5},{x:r.right-5,y:r.bottom-5});assert(state().selected.length===2,'Marquee');
});
await test('Double-click mode; rigid no-jump plane drag with remote offset; persistent mode; single undo/redo',async()=>{
  await load(connectedPair());change('#camera','top');change('#plane-offset','900');await tick();
  const start=state(),p=screen(start.data.pieces[0].p);double(p);assert(state().tool==='move-piece'&&!d.querySelector('#movement-bar').hidden,'No movement mode');
  assert(d.querySelector('#assembly-note').textContent.includes('2 pieces will move'),'Companion highlight count');
  const a={x:p.x-70,y:p.y}; // Away from the pivot / translation handles, on the tube.
  await drag(a,{x:a.x+40,y:a.y+25});const after=state();validate(after.data);
  assert(after.undo===1&&after.tool==='move-piece','Drag history / mode');
  assert(same(after.camera,start.camera)&&same(after.target,start.target),'Camera competed with piece movement');
  assert(after.data.pieces.every((piece,i)=>near(piece.p[1],start.data.pieces[i].p[1])),'Jumped to plane offset');
  const delta=vec(after.data.pieces[0].p).sub(vec(start.data.pieces[0].p));assert(delta.length()>1,'No movement');assert(vec(after.data.pieces[1].p).sub(vec(start.data.pieces[1].p)).distanceTo(delta)<1e-6,'Nonrigid movement');
  key('z',c,{ctrlKey:true});assert(same(state().data,start.data),'Undo drag');key('z',c,{ctrlKey:true,shiftKey:true});assert(same(state().data,after.data),'Redo drag');
  click('[data-tool="select"]');assert(state().tool==='select'&&d.querySelector('#movement-bar').hidden,'Select exit');
});
await test('Escape during piece drag restores geometry, exits mode, and creates no history on release',async()=>{
  await load(connectedPair());change('#camera','top');await tick();double(screen(state().data.pieces[0].p));const before=state(),p=screen(before.data.pieces[0].p),a={x:p.x-70,y:p.y};
  pointer('pointerdown',a);pointer('pointermove',{x:a.x+70,y:a.y+40});assert(!same(state().data,before.data),'Drag did not start');key('Escape');pointer('pointermove',{x:a.x+90,y:a.y+40});pointer('pointerup',{x:a.x+90,y:a.y+40});assert(same(state().data,before.data)&&state().undo===0&&state().tool==='select','Cancel failed');
});
await test('Compatible-port preview and release create a persistent joint in the same drag history entry',async()=>{
  const m=new Design(),t=m.add('tube',[0,100,0]),e=m.add('elbow90',[300,100,0]);await load(m);change('#camera','top');await tick();double(screen(t.p));
  const from=screen([-100,100,0]),to=screen([-50,100,0]);pointer('pointerdown',from);pointer('pointermove',to);assert(state().candidate,'No snap preview');pointer('pointerup',to);const after=state();assert(after.data.connections.length===1&&after.undo===1,'Snap connection/history');validate(after.data);
  key('z',c,{ctrlKey:true});assert(same(state().data,m.data()),'Undo snap');key('z',c,{ctrlKey:true,shiftKey:true});assert(state().data.connections.length===1,'Redo snap');
});
await test('Keyboard shortcuts ignore number, select, textarea and editable text while typing',async()=>{
  await load(connectedPair());click('#select-all');const before=state();
  for(const target of [d.querySelector('#plane-offset'),d.querySelector('#rotation-increment'),...['textarea','div'].map(tag=>{const el=d.createElement(tag);if(tag==='div')el.contentEditable='true';d.body.append(el);return el;})]){
    for(const k of ['q','e','g','r','v','Delete','Escape'])key(k,target);
    key('z',target,{ctrlKey:true});key('a',target,{ctrlKey:true});
  }
  assert(same(state().data,before.data)&&same(state().selected,before.selected)&&state().tool===before.tool&&state().undo===0,'Typing triggered shortcuts');
});
await test('Translation gizmo remains available and Escape restores a gizmo drag without an undo entry',async()=>{
  await load(connectedPair());click('#select-all');click('[data-tool="translate"]');await tick();
  // Find the actual visible gizmo axis by hovering along world X from its pivot.
  const p=state().data.pieces.reduce((a,p)=>a.map((v,i)=>v+p.p[i]/2),[0,0,0]);
  let hit=false;
  for(let offset=40;offset<180&&!hit;offset+=10){const a=screen([p[0]+offset,p[1],p[2]]);pointer('pointermove',a,{buttons:0});pointer('pointerdown',a);if(state().gizmoDragging){hit=true;const before=state().data;pointer('pointermove',{x:a.x+50,y:a.y});key('Escape');pointer('pointerup',{x:a.x+50,y:a.y});assert(same(state().data,before)&&state().undo===0,'Gizmo cancellation');}else pointer('pointerup',a);}
  assert(hit,'Could not pick translation handle');
});
await test('Front and side movement planes pass through the piece, ignoring the offset; grid movement has no initial jump',async()=>{
  for(const [plane,view,fixed] of [['front','front',2],['side','side',0]]){
    const m=new Design();m.add('tube',[13,113,37],400,plane==='side'?[0,Math.SQRT1_2,0,Math.SQRT1_2]:[0,0,0,1]);
    await load(m);change('#plane',plane);change('#camera',view);change('#plane-offset','800');await tick();
    double(screen(m.pieces[0].p));d.querySelector('#grid-snap').checked=true;
    const p=screen(m.pieces[0].p),a={x:p.x-80,y:p.y};pointer('pointerdown',a);pointer('pointermove',{x:a.x+2,y:a.y+1});assert(same(state().data,m.data()),'Subthreshold jump');
    pointer('pointermove',{x:a.x+42,y:a.y+35});pointer('pointerup',{x:a.x+42,y:a.y+35});
    const after=state().data.pieces[0];assert(near(after.p[fixed],m.pieces[0].p[fixed]),'Wrong plane');assert(!same(after.p,m.pieces[0].p),'No plane movement');assert(state().undo===1,'Grid drag history');
  }
});
await test('Discrete on-screen buttons share the custom increment for previews and selections',async()=>{
  await load();change('#rotation-increment','custom');change('#rotation-custom','12.5');click('[data-type="corner"]');
  click('[data-rotation-label="Horizontal"]');click('[data-rotation-label="Vertical"]');
  const preview=state().placement.q;assert(!same(preview,[0,0,0,1])&&state().undo===0,'Preview buttons');
  tap(screen([0,0,0]));const before=state();click('.rotate-buttons [data-turn="z"]');assert(state().undo===before.undo+1,'Axis button transaction');
  const q=quat([0,0,0,1]).setFromAxisAngle(vec([0,0,1]),12.5*Math.PI/180).multiply(quat(before.data.pieces[0].q));assert(near(Math.abs(quat(state().data.pieces[0].q).dot(q)),1),'Axis button increment');
});
await test('Length units cycle globally without changing geometry, history or fractional dimensions',async()=>{
  const m=new Design();m.add('tube',[123.456789,120,-80.123456],456.789123);m.add('tube',[600,120,0],1000);
  await load(m);tap(screen(m.pieces[0].p));change('#plane-offset','123.456789');
  const before=state();
  for(let cycle=0;cycle<20;cycle++)for(const [unit,factor] of [['cm',10],['m',1000],['mm',1]]){
    click('#length-unit');
    assert(d.querySelector('#length-unit').textContent===unit,'Cycle order');
    assert(near(Number(d.querySelector('#length').value),456.789123/factor,.001/factor),'Cut input');
    assert(near(Number(d.querySelector('#position-x').value),123.456789/factor,.001/factor),'Position input');
    assert(near(Number(d.querySelector('#plane-offset').value),123.456789/factor,.001/factor),'Plane input');
    assert(Number(d.querySelector('#length').min)===80/factor&&Number(d.querySelector('#length-slider').max)===3000/factor,'Bounds');
    assert(Number(d.querySelector('#length-slider').step)===1/factor,'Slider step');
    for(const selector of ['.spec','.panel-note','.workspace-tag','#transform-section h3','#summary','#total-length','.footer-spec','#help']){
      const text=d.querySelector(selector).textContent;
      assert(text.includes(unit),'Missing selected unit in '+selector);
      if(unit!=='mm')assert(!/\bmm\b|millimetres/.test(text),'Stale millimetres in '+selector);
    }
    assert(same(state().data,before.data)&&state().undo===before.undo,'Toggle changed canonical data/history');
    // Unchanged rounded inputs must never be written back into geometry.
    change('#length',d.querySelector('#length').value);change('#position-x',d.querySelector('#position-x').value);
    assert(same(state().data,before.data),'Rounded display written back');
  }
});
await test('Length, slider, position and plane edits use the current unit; undo and limits retain millimetres',async()=>{
  for(const [unit,factor,clicks] of [['mm',1,0],['cm',10,1],['m',1000,2]]){
    const m=new Design();m.add('tube',[0,120,0]);await load(m);click('#select-all');
    for(let i=0;i<clicks;i++)click('#length-unit');
    change('#length',String(725.125/factor));assert(near(state().data.pieces[0].length,725.125),'Length edit in '+unit);
    assert(d.querySelector('#summary').textContent.includes(unit),'Cut list label');
    change('#position-x',String(-321.5/factor));assert(near(state().data.pieces[0].p[0],-321.5),'Position edit');
    change('#plane-offset',String(250/factor));
    const slider=d.querySelector('#length-slider');slider.value=String(900/factor);slider.dispatchEvent(new w.Event('input',{bubbles:true}));slider.dispatchEvent(new w.Event('change',{bubbles:true}));
    assert(near(state().data.pieces[0].length,900)&&near(Number(d.querySelector('#length').value),900/factor),'Slider edit');
    click('#undo');assert(near(state().data.pieces[0].length,725.125),'Undo canonical length');click('#redo');
    const before=state();change('#length',String(79/factor));assert(same(state().data,before.data),'Accepted invalid cut length');
    assert(d.querySelector('#status').textContent.includes(unit),'Error unit');
    change('#position-x',String(100001/factor));assert(same(state().data,before.data),'Position limit changed');
    // A newly placed tube uses the selected-unit offset without scaling its geometry.
    change('#plane','front');change('#camera','front');click('[data-type="tube"]');
    pointer('pointermove',screen([0,0,250]),{buttons:0});
    assert(near(state().placement.p[2],250),'Plane offset converted incorrectly');key('Escape');
  }
});
await test('Converted length edits preserve connected joints and closed-loop locking',async()=>{
  await load(connectedPair());tap(screen(state().data.pieces[0].p));click('#length-unit');click('#length-unit');
  change('#length','0.875');validate(state().data);assert(near(state().data.pieces[0].length,875),'Connected resize');
  await load(rectangle());tap(screen(state().data.pieces.find(p=>p.type==='tube').p));click('#length-unit');
  assert(d.querySelector('#length').disabled&&d.querySelector('#length-slider').disabled,'Closed-loop lock lost');
});

await test('Catalog click and drag placement: every fitting and tube, all cameras, exact preview commit and history',async()=>{
  for(const [index,type] of ['tube','coupling','elbow90','elbow45','tee','cross','corner'].entries()){
    const m=new Design(),target=m.add(type==='tube'?'tee':'tube',[0,120,0]);await load(m);
    change('#camera',['perspective','top','front','side'][index%4]);await tick();
    const dragEvent=(name,p)=>d.querySelector('#workspace').dispatchEvent(new w.DragEvent(name,{clientX:p.x,clientY:p.y,bubbles:true,cancelable:true,dataTransfer:new w.DataTransfer()}));
    const button=d.querySelector(`[data-type="${type}"]`);
    if(index%2)button.dispatchEvent(new w.DragEvent('dragstart',{bubbles:true,dataTransfer:new w.DataTransfer()}));else button.click();
    // Rotate before the first pointer update, including catalog drag mode.
    key('q',button);key('e',button);
    assert(!same(state().placement.intentQ,[0,0,0,1]),'Initial orientation input ignored '+type);
    const at=screen(port(target,type==='tube'?2:1).position.toArray());
    if(index%2)dragEvent('dragover',at);else pointer('pointermove',at,{buttons:0});
    const mesh=state().previewMesh,preview=state().placement;assert(preview.connection,'No connection preview: '+type);
    assert(same(state().data,m.data())&&state().undo===0,'Preview mutated model');
    for(let step=0;step<4;step++){key(step%2?'e':'q');const before=state().placement;pointer('pointermove',at,{buttons:0});assert(same(state().placement.q,before.q),'Pointer undid rotation '+type);}
    assert(state().previewMesh===mesh,'Preview mesh rebuilt during movement/rotation');
    const final=state().placement;
    if(index%2){dragEvent('drop',at);button.dispatchEvent(new w.DragEvent('dragend',{bubbles:true}));}else tap(at);
    const after=state(),added=after.data.pieces.at(-1);validate(after.data);
    assert(same(added.p,final.p)&&same(added.q,final.q),'Preview jumped on placement '+type);
    const joint=after.data.connections.at(-1);
    assert(joint.a.id===added.id&&joint.a.port===final.connection.source&&same(joint.b,final.connection.target),'Preview port pairing changed '+type);
    const a=port(added,joint.a.port),b=port(after.data.pieces.find(p=>p.id===joint.b.id),joint.b.port),socket=a.type==='socket'?a:b;
    assert(a.position.distanceTo(b.position)<1e-8&&a.direction.dot(b.direction)<-.999999,'Committed joint alignment '+type);
    assert(near(socket.mouth.distanceTo(socket.position),20),'Insertion depth changed '+type);
    assert(after.data.connections.length===1&&after.undo===1&&after.selected[0]===added.id&&!after.placement,'Commit/selection '+type);
    click('#undo');assert(same(state().data,m.data()),'Undo '+type);click('#redo');assert(same(state().data,after.data),'Redo '+type);
  }
});
await test('192 CSS-pixel acquisition and strict release in every camera, zoomed views and free rotation',async()=>{
  for(const view of ['front','side','top','perspective'])for(const zoomed of [false,true]){
    const m=new Design(),target=m.add('coupling',[0,120,0]);await load(m);
    change('#camera',view);change('#plane',view==='side'?'side':view==='front'?'front':'ground');await tick();
    if(zoomed){c.dispatchEvent(new w.WheelEvent('wheel',{deltaY:-240,bubbles:true,cancelable:true}));await tick();}
    click('[data-type="tube"]');key('q');const initial=state().placement.intentQ;
    const at=[0,1].map(i=>screen(port(target,i).position.toArray())).sort((a,b)=>b.y-a.y)[0],mesh=state().previewMesh;
    for(const distance of [128,191.75,192]){
      pointer('pointermove',{x:at.x,y:at.y+distance},{buttons:0});
      assert(state().placement.connection?.target.id===target.id,`${view} ${zoomed} did not acquire at ${distance}px`);
      const guide=d.querySelector('#placement-guide'),circle=guide.querySelector('circle'),r=c.getBoundingClientRect();
      const chosen=screen(port(target,state().placement.connection.target.port).position.toArray());
      assert(!guide.hasAttribute('hidden')&&near(Number(circle.getAttribute('cx')),chosen.x-r.left)&&near(Number(circle.getAttribute('cy')),chosen.y-r.top),'Connection guide target '+view);
    }
    pointer('pointermove',{x:at.x,y:at.y+192.25},{buttons:0});
    assert(!state().placement.connection,'Target retained outside 192px '+view);
    assert(d.querySelector('#placement-guide').hasAttribute('hidden'),'Free placement retained connection guide '+view);
    assert(same(state().placement.q,initial),'Automatic alignment contaminated free orientation '+view);
    key('e');const free=state().placement;
    pointer('pointermove',{x:at.x,y:at.y+200},{buttons:0});
    assert(same(state().placement.q,free.q),'Free pointer movement undid E '+view);
    assert(state().previewMesh===mesh&&same(state().data,m.data())&&state().undo===0,'Query allocated mesh or changed model/history '+view);
    key('Escape');assert(!state().placement&&same(state().data,m.data())&&d.querySelector('#placement-guide').hasAttribute('hidden'),'Escape changed design or retained guide '+view);
  }
});
await test('Placement switches by pointer, stays stable near competitors, moves away, disables snap and cancels',async()=>{
  const m=new Design();m.add('coupling',[-20,120,0]);m.add('coupling',[20,120,0]);await load(m);change('#camera','front');change('#plane','front');await tick();click('[data-type="tube"]');
  const {port}=await import('../assets/js/pvc-model.mjs');
  const a=screen(port(m.pieces[0],0).position.toArray()),b=screen(port(m.pieces[1],0).position.toArray());
  pointer('pointermove',a,{buttons:0});const first=state().placement.connection;assert(first,'First target');
  const mid={x:(a.x+b.x)/2+2,y:a.y};pointer('pointermove',mid,{buttons:0});assert(state().placement.connection.target.id===first.target.id,'Hysteresis');
  pointer('pointermove',b,{buttons:0});assert(state().placement.connection.target.id!==first.target.id,'Did not switch');
  const r=c.getBoundingClientRect(),far={x:r.left+10,y:r.bottom-10};pointer('pointermove',far,{buttons:0});assert(!state().placement.connection,'Far snap');
  pointer('pointermove',b,{buttons:0});const check=d.querySelector('#port-snap');check.checked=false;check.dispatchEvent(new w.Event('change'));assert(!state().placement.connection&&d.querySelector('#placement-guide').hasAttribute('hidden'),'Disabled snap / guide');
  const free=state().placement;tap(b);assert(same(state().data.pieces.at(-1).p,free.p)&&!state().data.connections.length,'Disabled free commit');click('#undo');click('[data-type="tube"]');pointer('pointermove',b,{buttons:0});
  check.checked=true;check.dispatchEvent(new w.Event('change'));assert(state().placement.connection,'Reenabled snap');key('Escape');assert(!state().placement&&same(state().data,m.data())&&state().undo===0,'Escape mutated design');
});
await test('Occupied placement targets excluded and orthographic zoom remains targetable on edge-on plane',async()=>{
  const m=connectedPair();await load(m);change('#camera','front');await tick();click('[data-type="tee"]');
  const {port}=await import('../assets/js/pvc-model.mjs');const t=m.pieces[0],free=screen(port(t,0).position.toArray());
  pointer('pointermove',free,{buttons:0});assert(state().placement.connection?.target.port===0,'Edge-on plane blocked connection');
  c.dispatchEvent(new w.WheelEvent('wheel',{deltaY:-300,bubbles:true,cancelable:true}));await tick();
  pointer('pointermove',screen(port(t,0).position.toArray()),{buttons:0});assert(state().placement.connection,'Zoom targeting');
  const occupied=screen(port(t,1).position.toArray());pointer('pointermove',occupied,{buttons:0});assert(!state().placement.connection,'Occupied target selected');key('Escape');
});

document.title=results.querySelector('.fail')?'FAIL · PVC interaction tests':'PASS · PVC interaction tests';
