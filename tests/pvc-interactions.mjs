import {Design, validate, vec, quat} from '../assets/js/pvc-model.mjs';
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
document.title=results.querySelector('.fail')?'FAIL · PVC interaction tests':'PASS · PVC interaction tests';
