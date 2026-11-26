import * as THREE from '../vendor/three-0.170.0/three.module.js';
import {OrbitControls} from '../vendor/three-0.170.0/OrbitControls.js';
import {TransformControls} from '../vendor/three-0.170.0/TransformControls.js';
import {Design,CATALOG,RADIUS,INNER_RADIUS,INSERTION,localPorts,port,vec,quat,clone,validate,rectangle} from './pvc-model.mjs';

const $=s=>document.querySelector(s), $$=s=>[...document.querySelectorAll(s)];
const STORAGE='pvc-studio-v1', MAX_HISTORY=80;
let model=new Design(), selected=new Set(), selectedJoint=null, tool='select', clipboard=null;
let undo=[],redo=[],transaction=null,exported=JSON.stringify(model.data()), storageOK=true;
let placement=null, candidate=null, pickedPorts=[], hovered=null, directDrag=null, marquee=null, gesture=false, cancelledGesture=false;
const meshes=new Map(), scene=new THREE.Scene(), parts=new THREE.Group(), overlays=new THREE.Group(), ghost=new THREE.Group();
const workspace=$('#workspace'), canvas=document.createElement('canvas');canvas.setAttribute('aria-label','Interactive PVC construction canvas');canvas.tabIndex=0;
const renderer=new THREE.WebGLRenderer({canvas,antialias:true});
renderer.setPixelRatio(Math.min(devicePixelRatio,2));renderer.shadowMap.enabled=true;renderer.shadowMap.type=THREE.PCFSoftShadowMap;
renderer.setClearColor(0xedf2f3);renderer.outputColorSpace=THREE.SRGBColorSpace;workspace.append(canvas);
renderer.toneMapping=THREE.ACESFilmicToneMapping;renderer.toneMappingExposure=1.05;
canvas.addEventListener('webglcontextlost',()=>{$('#fatal').hidden=false;$('#fatal').textContent='The graphics context was lost. Your completed edits are saved on this device. Wait for recovery, or reload this page.';});
canvas.addEventListener('webglcontextrestored',()=>{$('#fatal').hidden=true;status('Graphics context restored.');});
scene.add(parts,overlays,ghost);scene.add(new THREE.HemisphereLight(0xffffff,0x9aacb0,2.4));
const light=new THREE.DirectionalLight(0xffffff,3.2);light.position.set(500,1000,650);light.castShadow=true;
light.shadow.mapSize.set(2048,2048);Object.assign(light.shadow.camera,{left:-2500,right:2500,top:2500,bottom:-2500,near:1,far:5000});light.shadow.bias=-.0004;light.shadow.normalBias=1;scene.add(light);
const floor=new THREE.Mesh(new THREE.PlaneGeometry(20000,20000),new THREE.ShadowMaterial({opacity:.13}));floor.rotation.x=-Math.PI/2;floor.position.y=-.6;floor.receiveShadow=true;scene.add(floor);
const grid=new THREE.GridHelper(10000,400,0xaabfc3,0xd7e1e3);grid.material.transparent=true;grid.material.opacity=.5;scene.add(grid);
const cameraPerspective=new THREE.PerspectiveCamera(42,1,1,100000), cameraOrtho=new THREE.OrthographicCamera(-600,600,600,-600,1,100000);
let camera=cameraPerspective;camera.position.set(1000,850,1100);
const orbit=new OrbitControls(camera,canvas);orbit.target.set(0,80,0);orbit.enableDamping=true;orbit.dampingFactor=.12;orbit.maxDistance=30000;orbit.minDistance=80;
orbit.mouseButtons={LEFT:null,MIDDLE:THREE.MOUSE.PAN,RIGHT:THREE.MOUSE.ROTATE};orbit.update();
const pivot=new THREE.Object3D();scene.add(pivot);
const gizmo=new TransformControls(camera,canvas);gizmo.setSize(.8);gizmo.setSpace('world');scene.add(gizmo.getHelper());
const ray=new THREE.Raycaster(), pointer=new THREE.Vector2();
let baseTransform=null, activeIds=new Set(), sliderBase=null;

function status(text,error=false){$('#status').textContent=text;$('#status').dataset.error=error;}
function snapshot(){return {data:model.data(),selected:[...selected],joint:selectedJoint};}
function restore(s){model=new Design(s.data);selected=new Set(s.selected.filter(id=>model.pieces.some(p=>p.id===id)));selectedJoint=s.joint;candidate=null;pickedPorts=[];}
function begin(){if(!transaction)transaction=snapshot();}
function persist(){try{localStorage.setItem(STORAGE,JSON.stringify(model.data()));storageOK=true;}catch{storageOK=false;status('Browser storage is unavailable or full. Use Save JSON to keep your work.',true);}}
function commit(message){if(transaction&&JSON.stringify(transaction.data)!==JSON.stringify(model.data())){undo.push(transaction);if(undo.length>MAX_HISTORY)undo.shift();redo=[];persist();}transaction=null;refresh();if(message)status(message);}
function action(fn,message){begin();try{fn();commit(message);}catch(e){restore(transaction);transaction=null;refresh();status(e.message,true);}}
function history(direction){if(placement)cancelPlacement();const from=direction==='undo'?undo:redo,to=direction==='undo'?redo:undo;if(!from.length)return;to.push(snapshot());restore(from.pop());persist();refresh();status(direction==='undo'?'Undid construction change.':'Redid construction change.');}

// Geometry: hollow tube walls, annular rims, recessed fitting sockets. No mesh scaling changes diameter.
function material(color=0xf9fcfb){return new THREE.MeshStandardMaterial({color,roughness:.32,metalness:.04});}
function mesh(geometry,mat,group){const m=new THREE.Mesh(geometry,mat);m.castShadow=true;m.receiveShadow=true;group.add(m);return m;}
function hollow(group,start,end,outer,inner,mat){
  const a=vec(start),b=vec(end),length=a.distanceTo(b),direction=b.clone().sub(a).normalize();
  const shell=new THREE.Group();shell.position.copy(a).add(b).multiplyScalar(.5);shell.quaternion.setFromUnitVectors(vec([0,1,0]),direction);group.add(shell);
  mesh(new THREE.CylinderGeometry(outer,outer,length,32,1,true),mat,shell);
  const inside=mat.clone();inside.side=THREE.BackSide;inside.color.multiplyScalar(.72);
  mesh(new THREE.CylinderGeometry(inner,inner,length,32,1,true),inside,shell);
  for(const sign of [-1,1]){const rim=mesh(new THREE.RingGeometry(inner,outer,32),mat,shell);rim.rotation.x=sign===1?-Math.PI/2:Math.PI/2;rim.position.y=sign*length/2;}
}
function geometry(p){
  const g=new THREE.Group(),mat=material(p.type==='tube'?0xeaf3f1:0xffffff);
  if(p.type==='tube')hollow(g,[-p.length/2,0,0],[p.length/2,0,0],RADIUS,INNER_RADIUS,mat);
  else {
    const defs=localPorts(p);
    if(p.type==='elbow90'||p.type==='elbow45'){
      const a=vec(defs[0].position),b=vec(defs[1].position);
      const curve=new THREE.QuadraticBezierCurve3(a,new THREE.Vector3(),b);
      mesh(new THREE.TubeGeometry(curve,24,19,24,false),mat,g);
      const inside=mat.clone();inside.side=THREE.BackSide;inside.color.set(0x9aafb0);mesh(new THREE.TubeGeometry(curve,24,RADIUS+.25,24,false),inside,g);
      for(const d of defs)hollow(g,d.direction.map(x=>x*24),d.position,22,RADIUS+.25,mat);
    } else {
      if(p.type!=='coupling')mesh(new THREE.SphereGeometry(19,24,16),mat,g);
      for(const d of defs)hollow(g,p.type==='coupling'?d.direction.map(x=>-x*3):[0,0,0],d.position,21,RADIUS+.25,mat);
      if(p.type==='cap'){const cap=mesh(new THREE.CylinderGeometry(21,21,8,32),mat,g);cap.rotation.z=Math.PI/2;cap.position.x=3;}
    }
  }
  g.userData.id=p.id;g.userData.type=p.type;g.userData.length=p.length;return g;
}
function dispose(group){const geometries=new Set(),materials=new Set();group.traverse(o=>{if(o.geometry)geometries.add(o.geometry);if(o.material)for(const m of Array.isArray(o.material)?o.material:[o.material])materials.add(m);});geometries.forEach(g=>g.dispose());materials.forEach(m=>m.dispose());group.clear();}
function clearGroup(group){dispose(group);}
function expanded(){return model.connected(selected);}
function center(ids){const result=new THREE.Vector3();let n=0;for(const p of model.pieces)if(ids.has(p.id)){result.add(vec(p.p));n++;}return n?result.divideScalar(n):result;}
function paint(){const companions=expanded();for(const [id,g] of meshes){const color=selected.has(id)?0x219da5:companions.has(id)?0xd29c36:id===hovered?0x8abcc4:g.userData.type==='tube'?0xeaf3f1:0xffffff;g.traverse(o=>{if(o.isMesh){o.material.color.setHex(color);if(o.material.side===THREE.BackSide)o.material.color.multiplyScalar(.65);o.material.emissive.setHex(0);o.material.emissiveIntensity=0;}});}}
function sync(){
  const existing=new Set(model.pieces.map(p=>p.id));
  for(const [id,g] of meshes)if(!existing.has(id)){parts.remove(g);dispose(g);meshes.delete(id);}
  for(const p of model.pieces){let g=meshes.get(p.id);if(g&&(g.userData.length!==p.length||g.userData.type!==p.type)){parts.remove(g);dispose(g);meshes.delete(p.id);g=null;}
    if(!g){g=geometry(p);parts.add(g);meshes.set(p.id,g);}g.position.copy(vec(p.p));g.quaternion.copy(quat(p.q));}
  paint();scene.updateMatrixWorld(true);$('#empty').hidden=!!model.pieces.length||!!placement;
  $('#scene-count').textContent=`${model.pieces.length} pieces · ${model.connections.length} joints`;
}
function marker(position,color,radius,data){const mat=new THREE.MeshBasicMaterial({color,depthTest:false,transparent:true,opacity:.9});const m=new THREE.Mesh(new THREE.SphereGeometry(radius,12,8),mat);m.position.copy(position);m.renderOrder=5;m.userData=data;overlays.add(m);return m;}
function showOverlays(){
  clearGroup(overlays);
  if(tool==='joints'||selected.size||pickedPorts.length)for(const p of model.pieces){if(tool!=='joints'&&!selected.has(p.id)&&!pickedPorts.some(e=>e.id===p.id))continue;
    localPorts(p).forEach((_,i)=>{if(!model.occupied(p.id,i))marker(port(p,i).position,pickedPorts.some(e=>e.id===p.id&&e.port===i)?0xe4aa32:0x5d9da8,5,{endpoint:{id:p.id,port:i}});});}
  for(const c of model.connections)if(tool==='joints'||selectedJoint===c.id||selected.has(c.a.id)||selected.has(c.b.id))marker(port(model.get(c.a.id),c.a.port).position,c.id===selectedJoint?0xf4ad32:0x00a7af,8,{joint:c.id});
  if(candidate){for(const e of [candidate.a,candidate.b])marker(port(model.get(e.id),e.port).position,0x00dce0,9,{candidate:true});}
}
function clearGhost(){clearGroup(ghost);}
function showGhost(ids,t){clearGhost();for(const id of ids){const p=clone(model.get(id));if(t){p.p=vec(p.p).sub(t.pivot).applyQuaternion(t.rotation).add(t.pivot).add(t.translation).toArray();p.q=t.rotation.clone().multiply(quat(p.q)).toArray();}const g=geometry(p);g.position.copy(vec(p.p));g.quaternion.copy(quat(p.q));g.traverse(o=>{if(o.isMesh){o.material.transparent=true;o.material.opacity=.35;o.material.depthWrite=false;o.material.color.setHex(0x04b0b4);o.castShadow=false;}});ghost.add(g);}}
function findCandidate(ids){
  if(!$('#port-snap').checked){candidate=null;clearGhost();showOverlays();return;}
  let best=null,score=Infinity;
  for(const p of model.pieces)if(ids.has(p.id))for(let i=0;i<localPorts(p).length;i++){
    if(model.occupied(p.id,i))continue;const a={id:p.id,port:i},pa=port(p,i);
    for(const other of model.pieces){if(other.id===p.id||other.type===p.type)continue;
      for(let j=0;j<localPorts(other).length;j++){if(model.occupied(other.id,j))continue;const b={id:other.id,port:j},pb=port(other,j);if(pa.type===pb.type)continue;
        const internal=ids.has(other.id);if(internal&&(pa.position.distanceTo(pb.position)>.05||pa.direction.dot(pb.direction)>-.99999))continue;
        const distance=pa.position.distanceTo(pb.position),stable=candidate?.a.id===a.id&&candidate.a.port===i&&candidate.b.id===b.id&&candidate.b.port===j;
        const weight=distance-(stable?18:0);if(distance<(stable?90:65)&&weight<score){score=weight;best={a,b,internal,moving:[...ids]};}
      }
    }
  }
  candidate=best;clearGhost();if(best){const t=best.internal?null:model.alignment(best.a,best.b);if(!best.internal)showGhost(ids,t);status('Snap ready · release to seat the tube 20 mm into the socket.');}showOverlays();
}
function finishSnap(){if(candidate){const c=candidate;if(!c.internal){const t=model.alignment(c.a,c.b);model.transform(new Set(c.moving),t.rotation,t.pivot,t.translation);}model.connect(c.a,c.b,false);status('Joint connected. Transforming either piece moves its connected assembly.');}candidate=null;clearGhost();}

// Inspector and selection state are independent of rendered geometry.
function setSelection(ids,joint=null){selected=new Set(ids);selectedJoint=joint;pickedPorts=[];refresh();}
function attach(){gizmo.detach();if(selected.size&&(tool==='translate'||tool==='rotate')){pivot.position.copy(center(selected));pivot.quaternion.identity();pivot.updateMatrixWorld(true);gizmo.setMode(tool);gizmo.setTranslationSnap($('#grid-snap').checked?25:null);gizmo.setRotationSnap($('#grid-snap').checked?Math.PI/12:null);gizmo.attach(pivot);}}
function fields(container,prefix){for(const axis of ['x','y','z']){const label=document.createElement('label');label.textContent=axis.toUpperCase();const input=document.createElement('input');input.type='number';input.step=prefix==='position'?'1':'5';input.id=`${prefix}-${axis}`;input.setAttribute('aria-label',`${prefix} ${axis.toUpperCase()}`);label.append(input);$(container).append(label);input.addEventListener('change',()=>numericTransform(prefix,axis,input));}}
fields('#position-fields','position');fields('#rotation-fields','rotation');
function inspector(){
  const list=model.pieces.filter(p=>selected.has(p.id)),single=list.length===1?list[0]:null,joint=model.connections.find(c=>c.id===selectedJoint),moves=expanded();
  $('#selection-title').textContent=joint?'Selected joint':single?CATALOG[single.type].name:list.length?`${list.length} selected`:'Your design';
  $('#selection-note').textContent=joint?`Joint ${joint.id.slice(0,8)} · tube to socket`:single?`Piece ${single.id.slice(0,8)} · Ø 32 mm`:list.length?'Edit a selection or its connected assemblies.':'Select a piece to refine it.';
  $('#selection-content').replaceChildren();if(!list.length)$('#selection-content').textContent=joint?'Detach to separate the two ports.':'Nothing selected';
  for(const p of list.slice(0,8)){const chip=document.createElement('span');chip.className='piece-chip';chip.textContent=CATALOG[p.type].name+(p.type==='tube'?` · ${fmt(p.length)} mm`:'');$('#selection-content').append(chip);}if(list.length>8)$('#selection-content').append(`+ ${list.length-8} more`);
  $('#select-assembly').hidden=!list.length;$('#transform-section').hidden=!list.length;
  if(list.length){const p=list[0],e=new THREE.Euler().setFromQuaternion(quat(p.q),'XYZ');['x','y','z'].forEach((a,i)=>{$(`#position-${a}`).value=round(p.p[i]);$(`#rotation-${a}`).value=round(THREE.MathUtils.radToDeg(e[a]));});$('#assembly-note').textContent=`${moves.size} pieces will move${moves.size>list.length?` · ${moves.size-list.length} connected companions highlighted in amber`:''}. Fields refer to the first selected piece.`;}
  $('#length-section').hidden=single?.type!=='tube';
  if(single?.type==='tube'){const plan=model.lengthPlan(single.id);$('#length').value=round(single.length);$('#length-slider').value=single.length;$('#length').disabled=$('#length-slider').disabled=!!plan.locked;$('#length-note').textContent=plan.locked?plan.reason:plan.fixed===null?'Physical cut length. Free tube resizes about its centre.':plan.side.size?'End 1 stays fixed. The assembly on end 2 translates with the new length.':`Connected end ${plan.fixed+1} stays fixed. The free end moves.`;$('#detach-blocking').hidden=!plan.locked;$('#detach-blocking').onclick=()=>{selectedJoint=plan.joint;setTool('joints');inspector();$('#detach').scrollIntoView({block:'nearest'});};}
  $('#ports-section').hidden=!list.length&&!joint;$('#ports').replaceChildren();
  for(const p of list) localPorts(p).forEach((def,i)=>{
    const connection=model.connections.find(c=>[c.a,c.b].some(e=>e.id===p.id&&e.port===i));const row=document.createElement('div');row.className='port-row';const button=document.createElement('button');button.textContent=`${list.length>1?CATALOG[p.type].name+' · ':''}End ${i+1} · ${def.type}${connection?' · joined':''}`;button.setAttribute('aria-pressed',pickedPorts.some(e=>e.id===p.id&&e.port===i));button.onclick=()=>{if(connection){selectedJoint=connection.id;inspector();showOverlays();}else pickPort({id:p.id,port:i});};row.append(button);$('#ports').append(row);
  });
  if(joint){const text=document.createElement('p');text.className='muted';text.textContent=`Joint ${joint.id.slice(0,8)} · ${CATALOG[model.get(joint.a.id).type].name} / ${CATALOG[model.get(joint.b.id).type].name}`;$('#ports').append(text);}
  $('#connect').hidden=pickedPorts.length!==2;$('#detach').hidden=!joint;
}
function pickPort(endpoint){if(model.occupied(endpoint.id,endpoint.port)){status('This port is occupied. Select and detach its joint first.',true);return;}selectedJoint=null;const i=pickedPorts.findIndex(e=>e.id===endpoint.id&&e.port===endpoint.port);if(i>=0)pickedPorts.splice(i,1);else{if(pickedPorts.length===2)pickedPorts=[];pickedPorts.push(endpoint);}inspector();showOverlays();status(pickedPorts.length===2?'Connect selected ports to align the assemblies.':'Port selected. Shift-select another piece, or choose a second port in Joints mode.');}
function fmt(n){return Number(n.toFixed(3)).toLocaleString('en-US',{maximumFractionDigits:3});}function round(n){return Math.round(n*1000)/1000;}
function summary(){const data=model.summary();$('#summary').replaceChildren();if(!data.rows.length)$('#summary').textContent='Your cut list will appear here.';for(const [name,count] of data.rows){const row=document.createElement('div');row.className='summary-row';const label=document.createElement('span'),value=document.createElement('b');label.textContent=name;value.textContent=`× ${count}`;row.append(label,value);$('#summary').append(row);}$('#total-length').textContent=`${fmt(data.total)} mm`;$('#summary-count').textContent=`${model.pieces.length} pieces`;}
function refresh(){sync();inspector();summary();attach();showOverlays();$('#undo').disabled=!undo.length;$('#redo').disabled=!redo.length;$('#paste').disabled=!clipboard;$('#copy').disabled=!selected.size;$('#delete').disabled=!selected.size&&!selectedJoint;$('#save-state').textContent=storageOK?'Saved on this device':'Save JSON to keep your work';}
function setTool(next){if(placement)cancelPlacement();tool=next;$$('[data-tool]').forEach(b=>b.setAttribute('aria-pressed',b.dataset.tool===tool));attach();showOverlays();canvas.style.cursor=tool==='marquee'?'crosshair':'default';status(({select:'Click to select · Shift-click toggles · right drag orbits.',translate:'Drag an axis handle or a piece to move. Nearby compatible ports preview a snap.',rotate:'Drag a rotation ring. Connected pieces rotate together.',marquee:'Left drag selects pieces whose centres are inside the rectangle. Shift adds to selection.',joints:'Click cyan joint markers to inspect and detach. Free port markers can be paired.'})[tool]);}
function numericTransform(prefix,axis,input){if(!Number.isFinite(input.valueAsNumber)||Math.abs(input.valueAsNumber)>100000){inspector();status('Enter a finite value between −100,000 and 100,000.',true);return;}const anchor=model.pieces.find(p=>selected.has(p.id));if(!anchor)return;action(()=>{if(prefix==='position'){const delta=new THREE.Vector3();delta[axis]=input.valueAsNumber-anchor.p[['x','y','z'].indexOf(axis)];model.transform(expanded(),undefined,undefined,delta);}else{const e=new THREE.Euler().setFromQuaternion(quat(anchor.q),'XYZ');e[axis]=THREE.MathUtils.degToRad(input.valueAsNumber);const q=new THREE.Quaternion().setFromEuler(e).multiply(quat(anchor.q).invert());model.transform(expanded(),q,vec(anchor.p));}},'Transform applied to the connected selection.');}

// Gizmo gestures are one transaction, even though the state and snap preview update every frame.
gizmo.addEventListener('dragging-changed',e=>{
  orbit.enabled=!e.value;if(e.value){begin();baseTransform=clone(model.data());activeIds=expanded();gesture=true;cancelledGesture=false;}
  else if(transaction){if(cancelledGesture){restore(transaction);transaction=null;}else{try{finishSnap();commit();}catch(error){restore(transaction);transaction=null;refresh();status(error.message,true);}}baseTransform=null;refresh();}
});
gizmo.addEventListener('objectChange',()=>{
  if(!baseTransform||!transaction||cancelledGesture)return;
  const base=new Design(baseTransform),origin=centerFrom(base,selected);model=base;model.transform(activeIds,pivot.quaternion,origin,pivot.position.clone().sub(origin));sync();findCandidate(activeIds);
});
function centerFrom(m,ids){const a=new THREE.Vector3();let n=0;for(const p of m.pieces)if(ids.has(p.id)){a.add(vec(p.p));n++;}return a.divideScalar(n||1);}

// Placement uses an explicit working plane and an actual hollow-geometry preview.
function workPlane(through=null){const mode=$('#plane').value,normal=mode==='front'?vec([0,0,1]):mode==='side'?vec([1,0,0]):vec([0,1,0]);const value=Number($('#plane-offset').value)||0;return new THREE.Plane(normal,through?-normal.dot(through):-value);}
function setRay(event){const r=canvas.getBoundingClientRect();pointer.set((event.clientX-r.left)/r.width*2-1,-(event.clientY-r.top)/r.height*2+1);ray.setFromCamera(pointer,camera);}
function planePoint(event,plane=workPlane()){setRay(event);const hit=ray.ray.intersectPlane(plane,new THREE.Vector3());if(!hit)return null;if($('#grid-snap').checked)hit.toArray().forEach((v,i)=>hit.setComponent(i,Math.round(v/25)*25));return hit;}
function startPlacement(type){cancelPlacement();selectedJoint=null;placement={type,p:[0,60,0],q:[0,0,0,1],length:400};orbit.enabled=false;gizmo.detach();$('#placement-bar').hidden=false;$('#empty').hidden=true;canvas.style.cursor='crosshair';previewPlacement();status(`Placing ${CATALOG[type].name}. Move into the workspace; click to commit. Q rotates.`);}
function previewPlacement(){clearGhost();if(!placement)return;const g=geometry({...placement,id:'preview'});g.position.copy(vec(placement.p));g.quaternion.copy(quat(placement.q));g.traverse(o=>{if(o.isMesh){o.material.transparent=true;o.material.opacity=.55;o.material.color.set(0x2aadaf);o.material.depthWrite=false;o.castShadow=false;}});ghost.add(g);}
function updatePlacement(event){const point=planePoint(event);if(!point){status('Working plane is edge-on. Choose a different plane or camera view.',true);return false;}if($('#plane').value==='ground')point.y+=placement.type==='tube'?RADIUS:22;placement.p=point.toArray();
  const temp=model.add(placement.type,placement.p,placement.length,placement.q);findCandidate(new Set([temp.id]));if(candidate){const t=model.alignment(candidate.a,candidate.b);placement.p=vec(temp.p).sub(t.pivot).applyQuaternion(t.rotation).add(t.pivot).add(t.translation).toArray();placement.q=t.rotation.multiply(quat(temp.q)).toArray();placement.target={...candidate.b};}else delete placement.target;model.pieces.pop();candidate=null;previewPlacement();showOverlays();if(placement.target){marker(port(model.get(placement.target.id),placement.target.port).position,0x00dce0,9,{candidate:true});const p={...placement,id:'preview'},idx=localPorts(p).findIndex((_,i)=>port(p,i).position.distanceTo(port(model.get(placement.target.id),placement.target.port).position)<.05);if(idx>=0)marker(port(p,idx).position,0x00dce0,9,{candidate:true});}return true;}
function commitPlacement(){const spec=clone(placement);cancelPlacement();action(()=>{const piece=model.add(spec.type,spec.p,spec.length,spec.q);if(spec.target){const target=port(model.get(spec.target.id),spec.target.port);const i=localPorts(piece).findIndex((_,i)=>port(piece,i).position.distanceTo(target.position)<.05);if(i<0)throw Error('Snap target changed; place the piece again.');model.connect({id:piece.id,port:i},spec.target,false);}selected=new Set([piece.id]);selectedJoint=null;},spec.target?'Placed and connected.':'Piece placed. Select Move to position it precisely.');}
function cancelPlacement(){placement=null;candidate=null;clearGhost();$('#placement-bar').hidden=true;orbit.enabled=true;canvas.style.cursor='default';showOverlays();$('#empty').hidden=!!model.pieces.length;attach();}
function hitPiece(event){setRay(event);const hit=ray.intersectObjects(parts.children,true)[0];if(!hit)return null;let o=hit.object;while(o&&!o.userData.id)o=o.parent;return o?.userData.id||null;}
function hitOverlay(event){setRay(event);return ray.intersectObjects(overlays.children,false).find(h=>!h.object.userData.candidate)?.object.userData;}

canvas.addEventListener('contextmenu',e=>e.preventDefault());
canvas.addEventListener('pointerdown',e=>{
  if(e.button!==0)return;gesture=gizmo.dragging;cancelledGesture=false;if(placement||gizmo.dragging||gizmo.axis)return;
  const overlay=hitOverlay(e);if(tool==='joints'&&overlay){if(overlay.joint){selectedJoint=overlay.joint;selected.clear();inspector();sync();attach();showOverlays();}else if(overlay.endpoint)pickPort(overlay.endpoint);gesture=true;return;}
  if(tool==='marquee'){const r=canvas.getBoundingClientRect();marquee={x:e.clientX-r.left,y:e.clientY-r.top,shift:e.shiftKey};orbit.enabled=false;canvas.setPointerCapture(e.pointerId);gesture=true;return;}
  const id=hitPiece(e);if(id){if(e.shiftKey){const next=new Set(selected);next.has(id)?next.delete(id):next.add(id);setSelection(next);}else if(!selected.has(id))setSelection([id]);
    if(tool==='translate'&&!e.shiftKey&&selected.has(id)){const plane=workPlane(vec(model.get(id).p)),start=planePoint(e,plane);if(start){begin();directDrag={plane,start,base:clone(model.data()),ids:expanded(),moved:false};orbit.enabled=false;canvas.setPointerCapture(e.pointerId);}}}
  else if(!e.shiftKey)setSelection([]);
});
canvas.addEventListener('pointermove',e=>{
  if(placement){updatePlacement(e);return;}
  if(marquee){const r=canvas.getBoundingClientRect(),x=e.clientX-r.left,y=e.clientY-r.top,b=$('#marquee-box');b.hidden=false;Object.assign(b.style,{left:Math.min(x,marquee.x)+'px',top:Math.min(y,marquee.y)+'px',width:Math.abs(x-marquee.x)+'px',height:Math.abs(y-marquee.y)+'px'});return;}
  if(directDrag){const point=planePoint(e,directDrag.plane);if(point){const delta=point.sub(directDrag.start);directDrag.moved=delta.length()>.1;model=new Design(directDrag.base);model.transform(directDrag.ids,undefined,undefined,delta);sync();findCandidate(directDrag.ids);}return;}
  if(gizmo.dragging)return;const id=hitPiece(e);if(id!==hovered){hovered=id;paint();}
});
canvas.addEventListener('pointerleave',()=>{hovered=null;paint();});
canvas.addEventListener('pointerup',e=>{
  if(e.button!==0)return;
  if(placement){if(updatePlacement(e))commitPlacement();return;}
  if(marquee){const r=canvas.getBoundingClientRect(),x=e.clientX-r.left,y=e.clientY-r.top,next=marquee.shift?new Set(selected):new Set();for(const p of model.pieces){const v=vec(p.p).project(camera),sx=(v.x+1)/2*r.width,sy=(1-v.y)/2*r.height;if(v.z>=-1&&v.z<=1&&sx>=Math.min(x,marquee.x)&&sx<=Math.max(x,marquee.x)&&sy>=Math.min(y,marquee.y)&&sy<=Math.max(y,marquee.y))next.add(p.id);}marquee=null;$('#marquee-box').hidden=true;orbit.enabled=true;setSelection(next);}
  if(directDrag){try{if(directDrag.moved)finishSnap();commit();}catch(error){restore(transaction);transaction=null;refresh();status(error.message,true);}directDrag=null;orbit.enabled=true;}
  if(canvas.hasPointerCapture(e.pointerId))canvas.releasePointerCapture(e.pointerId);
});
canvas.addEventListener('pointercancel',()=>{if(transaction){restore(transaction);transaction=null;}directDrag=null;marquee=null;$('#marquee-box').hidden=true;orbit.enabled=true;candidate=null;clearGhost();refresh();});
workspace.addEventListener('dragover',e=>{if(placement){e.preventDefault();e.dataTransfer.dropEffect='copy';updatePlacement(e);}});
workspace.addEventListener('drop',e=>{e.preventDefault();if(placement&&updatePlacement(e))commitPlacement();});

// Catalog is generated from the same definitions as geometry and port compatibility.
function thumbnail(type){const paths={tube:'M14 47 L65 17',coupling:'M20 44 L59 22',elbow90:'M16 45 Q45 47 45 18',elbow45:'M14 45 L35 34 Q40 30 61 30',tee:'M12 47 L65 17 M38 32 L56 53',cross:'M12 47 L65 17 M20 12 L57 53',corner:'M12 47 L38 32 L65 47 M38 32 L38 9',cap:'M27 39 L53 24'};return `<svg viewBox="0 0 78 64" aria-hidden="true"><defs><filter id="shadow-${type}"><feDropShadow dx="1" dy="3" stdDeviation="2" flood-color="#69888f" flood-opacity=".25"/></filter></defs><path d="${paths[type]}" stroke="#aec3c6" stroke-width="${type==='tube'?12:17}" fill="none" stroke-linecap="${type==='cap'?'round':'butt'}" filter="url(#shadow-${type})"/><path d="${paths[type]}" stroke="#f3f8f7" stroke-width="${type==='tube'?9:13}" fill="none"/><path d="${paths[type]}" stroke="#ffffff" stroke-width="3" opacity=".9" fill="none"/>${type==='tube'?'<ellipse cx="65" cy="17" rx="5" ry="6" fill="#6f9298" transform="rotate(48 65 17)"/><ellipse cx="65" cy="17" rx="3" ry="4" fill="#35575f" transform="rotate(48 65 17)"/>':''}</svg>`;}
for(const [type,def] of Object.entries(CATALOG)){const b=document.createElement('button');b.className='material';b.draggable=true;b.dataset.type=type;b.innerHTML=thumbnail(type);const name=document.createElement('strong'),note=document.createElement('small');name.textContent=def.name;note.textContent=def.note;b.append(name,note);b.onclick=()=>startPlacement(type);b.addEventListener('dragstart',e=>{e.dataTransfer.setData('text/plain',type);e.dataTransfer.effectAllowed='copy';startPlacement(type);});b.addEventListener('dragend',()=>{if(placement)cancelPlacement();});$('#catalog').append(b);}

function editLength(value){const p=model.pieces.find(p=>selected.has(p.id));if(!p)return;if(!sliderBase){begin();sliderBase=clone(transaction.data);}try{model=new Design(sliderBase);model.resize(p.id,Number(value));sync();summary();showOverlays();$('#length').value=round(Number(value));$('#length-slider').value=value;}catch(e){status(e.message,true);}}
$('#length').addEventListener('change',e=>{const p=model.pieces.find(p=>selected.has(p.id));if(p)action(()=>model.resize(p.id,e.target.valueAsNumber),'Tube cut length updated; valid joints preserved.');});
$('#length-slider').addEventListener('input',e=>editLength(e.target.value));
$('#length-slider').addEventListener('change',()=>{sliderBase=null;commit('Tube cut length updated; valid joints preserved.');});
$('#length-slider').addEventListener('blur',()=>{if(sliderBase){sliderBase=null;commit();}});
$$('[data-tool]').forEach(b=>b.onclick=()=>setTool(b.dataset.tool));
$$('[data-turn]').forEach(b=>b.onclick=()=>{if(selected.size)action(()=>model.transform(expanded(),new THREE.Quaternion().setFromAxisAngle(vec(b.dataset.turn==='x'?[1,0,0]:b.dataset.turn==='y'?[0,1,0]:[0,0,1]),Math.PI/2),center(selected)),'Rotated the connected selection by 90°.');});
$('#undo').onclick=()=>history('undo');$('#redo').onclick=()=>history('redo');
$('#copy').onclick=()=>{if(selected.size){clipboard=model.copy(selected);$('#paste').disabled=false;status(`Copied ${clipboard.pieces.length} pieces and ${clipboard.connections.length} internal joints.`);}};
$('#paste').onclick=()=>{if(clipboard)action(()=>{selected=model.paste(clipboard);selectedJoint=null;},'Pasted with fresh IDs, preserved internal joints, and an 80 mm offset.');};
$('#delete').onclick=()=>{if(selectedJoint)detach();else if(selected.size)action(()=>{model.remove(selected);selected.clear();},'Deleted selected pieces and their incident joints.');};
function detach(){if(selectedJoint)action(()=>{model.disconnect(selectedJoint);selectedJoint=null;},'Joint detached. Pieces stay in place; connected assemblies recalculated.');}
$('#detach').onclick=detach;$('#connect').onclick=()=>{if(pickedPorts.length===2)action(()=>{model.connect(...pickedPorts);pickedPorts=[];},'Ports connected. The assemblies now move together.');};
$('#select-all').onclick=()=>setSelection(model.pieces.map(p=>p.id));$('#clear').onclick=()=>setSelection([]);$('#select-assembly').onclick=()=>setSelection(expanded());
$('#start').onclick=()=>startPlacement('tube');$('#grid-snap').onchange=attach;$('#port-snap').onchange=()=>{candidate=null;clearGhost();showOverlays();};
$('#help-toggle').onclick=()=>{$('#help').showModal();$('#help-toggle').setAttribute('aria-expanded','true');};$('#help-close').onclick=()=>$('#help').close();$('#help').addEventListener('close',()=>$('#help-toggle').setAttribute('aria-expanded','false'));

// Persistence is versioned and strictly validated before replacement.
function mayReplace(){return JSON.stringify(model.data())===exported||!model.pieces.length||confirm('Replace this design? Changes are saved on this browser, but will be overwritten. Save JSON first if you need a separate copy.');}
$('#new').onclick=()=>{if(mayReplace()){cancelPlacement();action(()=>{model=new Design();selected.clear();selectedJoint=null;},'Started a new design. Undo can restore the previous design.');exported=JSON.stringify(model.data());}};
$('#sample').onclick=()=>{if(mayReplace()){cancelPlacement();action(()=>{model=rectangle();selected=new Set();selectedJoint=null;},'Rectangular frame: 4 elbows, 4 cut tubes, 8 joints. Select a tube to inspect the closed-loop length lock.');frame();}};
$('#export').onclick=()=>{const data=JSON.stringify(model.data(),null,2),blob=new Blob([data],{type:'application/json'}),url=URL.createObjectURL(blob),a=document.createElement('a');a.href=url;a.download='pvc-design.json';a.click();setTimeout(()=>URL.revokeObjectURL(url),2000);exported=JSON.stringify(model.data());status('Design exported as pvc-design.json.');};
$('#import').onclick=()=>$('#file').click();$('#file').onchange=async e=>{const file=e.target.files[0];if(!file)return;try{if(file.size>5e6)throw Error('Design file exceeds the 5 MB limit.');const incoming=validate(JSON.parse(await file.text()));if(!mayReplace())return;cancelPlacement();action(()=>{model=incoming;selected.clear();selectedJoint=null;},`Loaded ${incoming.pieces.length} pieces and ${incoming.connections.length} valid joints.`);exported=JSON.stringify(model.data());frame();}catch(error){status('Could not load design: '+error.message,true);}finally{e.target.value='';}};
try{const saved=localStorage.getItem(STORAGE);if(saved){model=validate(JSON.parse(saved));status(`Restored ${model.pieces.length} pieces from this browser.`);}}catch(error){status('Saved work could not be restored: '+error.message+'. Load a JSON backup to recover it.',true);}

// Cameras, resize and world-axis indicator.
function resize(){const w=workspace.clientWidth,h=workspace.clientHeight;renderer.setSize(w,h,false);cameraPerspective.aspect=w/h;cameraPerspective.updateProjectionMatrix();const vertical=(cameraOrtho.top-cameraOrtho.bottom)/2;cameraOrtho.left=-vertical*w/h;cameraOrtho.right=vertical*w/h;cameraOrtho.updateProjectionMatrix();}
const observer=new ResizeObserver(resize);observer.observe(workspace);
function frame(){const ids=selected.size?expanded():new Set(model.pieces.map(p=>p.id));if(!ids.size)return;sync();const box=new THREE.Box3();for(const id of ids)box.expandByObject(meshes.get(id));const size=box.getSize(new THREE.Vector3()),target=box.getCenter(new THREE.Vector3()),radius=Math.max(size.length()/2,100),aspect=workspace.clientWidth/workspace.clientHeight;
  const dir=camera.position.clone().sub(orbit.target).normalize();orbit.target.copy(target);
  if(camera.isPerspectiveCamera)camera.position.copy(target).addScaledVector(dir,radius/Math.sin(THREE.MathUtils.degToRad(camera.fov/2))*1.25/Math.min(aspect,1));
  else{camera.position.copy(target).addScaledVector(dir,5000);const half=radius*1.3/Math.min(aspect,1);camera.top=half;camera.bottom=-half;camera.left=-half*aspect;camera.right=half*aspect;camera.zoom=1;camera.updateProjectionMatrix();}orbit.update();}
$('#frame').onclick=frame;
$('#camera').onchange=e=>{const view=e.target.value,target=orbit.target.clone();camera=view==='perspective'?cameraPerspective:cameraOrtho;orbit.object=camera;gizmo.camera=camera;orbit.enableRotate=view==='perspective';camera.up.set(0,1,0);if(view==='top')camera.up.set(0,0,-1);const d=({perspective:[1,.8,1],top:[0,1,0],front:[0,0,1],side:[1,0,0]})[view];camera.position.copy(target).addScaledVector(vec(d).normalize(),2000);camera.lookAt(target);resize();orbit.update();frame();$('#view-label').textContent=e.target.selectedOptions[0].textContent;};
function orientation(){const inverse=camera.quaternion.clone().invert(),lines=$('#axis-lines');lines.replaceChildren();for(const [axis,label,color] of [[[1,0,0],'X','#c45b55'],[[0,1,0],'Y','#479a69'],[[0,0,1],'Z','#558dc7']]){const v=vec(axis).applyQuaternion(inverse),x=42+v.x*27,y=42-v.y*27;const line=document.createElementNS('http://www.w3.org/2000/svg','line');for(const [k,val] of Object.entries({x1:42,y1:42,x2:x,y2:y,stroke:color,'stroke-width':2}))line.setAttribute(k,val);const text=document.createElementNS(line.namespaceURI,'text');text.setAttribute('x',x-4);text.setAttribute('y',y-5);text.setAttribute('fill',color);text.setAttribute('font-size',11);text.textContent=label;lines.append(line,text);}}
let animation;function render(){animation=requestAnimationFrame(render);orbit.update();orientation();renderer.render(scene,camera);}resize();refresh();render();
window.addEventListener('keydown',e=>{
  if(e.target.closest('input,textarea,select,[contenteditable=true]')||$('#help').open)return;const key=e.key.toLowerCase(),mod=e.ctrlKey||e.metaKey;
  if(mod&&['c','v','z','y','a'].includes(key)){e.preventDefault();if(key==='c')$('#copy').click();if(key==='v')$('#paste').click();if(key==='z')history(e.shiftKey?'redo':'undo');if(key==='y')history('redo');if(key==='a')$('#select-all').click();return;}
  if(key==='escape'){e.preventDefault();if(placement){cancelPlacement();status('Placement cancelled.');}else if(transaction){cancelledGesture=true;restore(transaction);transaction=null;baseTransform=null;directDrag=null;sliderBase=null;candidate=null;clearGhost();orbit.enabled=true;refresh();status('Transform cancelled.');}else{setSelection([]);pickedPorts=[];showOverlays();}return;}
  if(placement&&key==='q'){placement.q=new THREE.Quaternion().setFromAxisAngle(vec([0,1,0]),Math.PI/2).multiply(quat(placement.q)).toArray();delete placement.target;previewPlacement();return;}
  if(placement)return;if(key==='delete'||key==='backspace'){e.preventDefault();$('#delete').click();}if(key==='f')frame();if(key==='g')setTool('translate');if(key==='r')setTool('rotate');if(key==='v')setTool('select');
});
window.addEventListener('pagehide',event=>{if(event.persisted)return;cancelAnimationFrame(animation);observer.disconnect();gizmo.dispose();orbit.dispose();clearGroup(parts);clearGroup(overlays);clearGroup(ghost);grid.geometry.dispose();grid.material.dispose();floor.geometry.dispose();floor.material.dispose();renderer.dispose();});
