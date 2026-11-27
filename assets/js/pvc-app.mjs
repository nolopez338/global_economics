import * as THREE from '../vendor/three-0.170.0/three.module.js';
import {OrbitControls} from '../vendor/three-0.170.0/OrbitControls.js';
import {TransformControls} from '../vendor/three-0.170.0/TransformControls.js';
import {Design,CATALOG,RADIUS,localPorts,port,vec,quat,clone,validate,materialName} from './pvc-model.mjs';

import {TEMPLATES,buildTemplate} from './pvc-templates.mjs';
import {geometry,dispose} from './pvc-geometry.mjs';
import {placementTargets,choosePlacement,projectPort,SNAP_PIXELS} from './pvc-placement.mjs';
import {MagneticRotation} from './pvc-rotation.mjs';

const $=s=>document.querySelector(s), $$=s=>[...document.querySelectorAll(s)];
const STORAGE='pvc-studio-v1', ROTATION_STORAGE='pvc-studio-rotation-increment', MAX_HISTORY=80, DRAG_THRESHOLD=4;
// Geometry, history and portable designs always remain in millimetres.
const LENGTH_UNITS=['mm','cm','m'], LENGTH_SCALES={mm:1,cm:10,m:1000};
let pdfExporting=false;
let lengthUnit='mm', planeOffset=0, statusSource='Ready. Choose a component to start building.';
const scale=()=>LENGTH_SCALES[lengthUnit];
const displayLength=n=>Number((n/scale()).toFixed({mm:3,cm:4,m:6}[lengthUnit]));
const lengthText=n=>`${displayLength(n).toLocaleString('en-US',{maximumFractionDigits:6})} ${lengthUnit}`;
const lengthTemplates=[];
function unitText(text){return text.replace(/(\d[\d,]*(?:\.\d+)?)[–−](\d[\d,]*(?:\.\d+)?) mm\b/g,(_,a,b)=>`${displayLength(Number(a.replaceAll(',','')))}–${lengthText(Number(b.replaceAll(',','')))}`).replace(/(-?\d[\d,]*(?:\.\d+)?) mm\b/g,(_,n)=>lengthText(Number(n.replaceAll(',','')))).replace(/\bmm\b/g,lengthUnit).replace('millimetres',({mm:'millimetres',cm:'centimetres',m:'metres'})[lengthUnit]);}
function showLengthInput(input,value){input.value=displayLength(value);input.dataset.displayValue=input.value;}
function updateLengthUnits(){
  for(const [node,text] of lengthTemplates)node.textContent=unitText(text);
  const next=LENGTH_UNITS[(LENGTH_UNITS.indexOf(lengthUnit)+1)%3];
  for(const button of [$('#length-unit'),$('#group-length-unit')]){button.textContent=lengthUnit;button.setAttribute('aria-label',`Length unit: ${lengthUnit}. Switch to ${next}`);}
  for(const id of ['length','length-slider']){const input=$('#'+id);input.min=80/scale();input.max=3000/scale();input.step=1/scale();input.setAttribute('aria-label',`Tube cut length${id==='length-slider'?' slider':''} in ${lengthUnit}`);}
  for(const axis of ['x','y','z']){const input=$('#position-'+axis);input.step=1/scale();input.setAttribute('aria-label',`position ${axis.toUpperCase()} in ${lengthUnit}`);}
  $('#plane-offset').setAttribute('aria-label',`Plane offset in ${lengthUnit}`);$('#plane-offset').step=25/scale();showLengthInput($('#plane-offset'),planeOffset);
  $('[data-type="tube"] small').textContent=`${displayLength(80)}–${displayLength(3000).toLocaleString('en-US')} ${lengthUnit} cut length`;
  $('#status').textContent=unitText(statusSource);
}
let rotationIncrement=90, pointerGesture=null, doubleClickEligible=false;
let model=new Design(), selected=new Set(), selectedJoint=null, tool='select', clipboard=null;
let undo=[],redo=[],transaction=null,exported=JSON.stringify(model.data()), storageOK=true;
let placementPointer=null, placementPorts=[], placementMesh=null;
let placement=null, candidate=null, pickedPorts=[], hovered=null, directDrag=null, marquee=null, cancelledGesture=false;
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
orbit.mouseButtons={LEFT:THREE.MOUSE.PAN,MIDDLE:THREE.MOUSE.PAN,RIGHT:THREE.MOUSE.ROTATE};orbit.update();
const pivot=new THREE.Object3D();scene.add(pivot);
const gizmo=new TransformControls(camera,canvas);gizmo.setSize(.8);gizmo.setSpace('world');scene.add(gizmo.getHelper());
const ray=new THREE.Raycaster(), pointer=new THREE.Vector2();
let baseTransform=null, activeIds=new Set(), rotationDrag=null, sliderBase=null, groupEdit=null, groupCancelled=false, groupRangeKey=null, groupRangePointer=null;

function status(text,error=false){statusSource=text;$('#status').textContent=unitText(text);$('#status').dataset.error=error;}
function snapshot(){return {data:model.data(),selected:[...selected],joint:selectedJoint};}
function restore(s){model=validate(s.data);selected=new Set(s.selected.filter(id=>model.pieces.some(p=>p.id===id)));selectedJoint=s.joint;candidate=null;pickedPorts=[];}
function begin(){if(!transaction)transaction=snapshot();}
function persist(){try{localStorage.setItem(STORAGE,JSON.stringify(model.data()));storageOK=true;}catch{storageOK=false;status('Browser storage is unavailable or full. Use Save JSON to keep your work.',true);}}
function commit(message){if(transaction&&JSON.stringify(transaction.data)!==JSON.stringify(model.data())){undo.push(transaction);if(undo.length>MAX_HISTORY)undo.shift();redo=[];persist();}transaction=null;refresh();if(message)status(message);}
function action(fn,message){begin();try{fn();commit(message);}catch(e){restore(transaction);transaction=null;refresh();status(e.message,true);}}
function history(direction){const from=direction==='undo'?undo:redo,to=direction==='undo'?redo:undo;if(!from.length)return;try{validate(from.at(-1).data);}catch(error){status('Could not restore history: '+error.message,true);return;}cancelInteraction();if(placement)cancelPlacement();to.push(snapshot());restore(from.pop());persist();refresh();status(direction==='undo'?'Undid construction change.':'Redid construction change.');}

// Geometry: hollow tube walls, annular rims, recessed fitting sockets. No mesh scaling changes diameter.
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
  if(placement?.connection){const c=placement.connection;marker(port(model.get(c.target.id),c.target.port).position,0x00dce0,9,{candidate:true});marker(port({...placement,id:'preview'},c.source).mouth,0x00dce0,6,{candidate:true});}
  if(candidate){for(const e of [candidate.a,candidate.b])marker(port(model.get(e.id),e.port).position,0x00dce0,9,{candidate:true});}
}
function clearGhost(){clearGroup(ghost);placementMesh=null;ghost.visible=true;}
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
function setSelection(ids,joint=null){finishLengthEdits();selected=new Set(ids);selectedJoint=joint;pickedPorts=[];refresh();}
function attach(){gizmo.detach();if(selected.size&&(tool==='translate'||tool==='move-piece'||tool==='rotate')){pivot.position.copy(center(selected));pivot.quaternion.identity();pivot.updateMatrixWorld(true);gizmo.setMode(tool==='move-piece'?'translate':tool);gizmo.setTranslationSnap($('#grid-snap').checked?25:null);gizmo.setRotationSnap(null);gizmo.attach(pivot);}}
function fields(container,prefix){for(const axis of ['x','y','z']){const label=document.createElement('label');label.textContent=axis.toUpperCase();const input=document.createElement('input');input.type='number';input.step=prefix==='position'?'1':'5';input.id=`${prefix}-${axis}`;input.setAttribute('aria-label',`${prefix} ${axis.toUpperCase()}`);label.append(input);$(container).append(label);input.addEventListener('change',()=>numericTransform(prefix,axis,input));}}
fields('#position-fields','position');fields('#rotation-fields','rotation');
function showSelectedPieces(list,joint){
  $('#selection-content').replaceChildren();if(!list.length)$('#selection-content').textContent=joint?'Detach to separate the two ports.':'Nothing selected';
  for(const p of list.slice(0,8)){const chip=document.createElement('span');chip.className='piece-chip';chip.textContent=CATALOG[p.type].name+(p.type==='tube'?` · ${lengthText(p.length)}`:'');$('#selection-content').append(chip);}if(list.length>8)$('#selection-content').append(`+ ${list.length-8} more`);
}
function inspector(){
  const list=model.pieces.filter(p=>selected.has(p.id)),single=list.length===1?list[0]:null,joint=model.connections.find(c=>c.id===selectedJoint),moves=expanded();
  $('#selection-title').textContent=joint?'Selected joint':single?CATALOG[single.type].name:list.length?`${list.length} selected`:'Your design';
  $('#selection-note').textContent=joint?`Joint ${joint.id.slice(0,8)} · tube to socket`:single?`Piece ${single.id.slice(0,8)} · Ø ${lengthText(32)}`:list.length?'Edit a selection or its connected assemblies.':'Select a piece to refine it.';
  showSelectedPieces(list,joint);
  $('#select-assembly').hidden=!list.length;$('#transform-section').hidden=!list.length;
  if(list.length){const p=list[0],e=new THREE.Euler().setFromQuaternion(quat(p.q),'XYZ');['x','y','z'].forEach((a,i)=>{showLengthInput($(`#position-${a}`),p.p[i]);$(`#rotation-${a}`).value=round(THREE.MathUtils.radToDeg(e[a]));});$('#assembly-note').textContent=`${moves.size} pieces will move${moves.size>list.length?` · ${moves.size-list.length} connected companions highlighted in amber`:''}. Fields refer to the first selected piece.`;}
  $('#length-section').hidden=single?.type!=='tube';
  if(single?.type==='tube'){const plan=model.lengthPlan(single.id);showLengthInput($('#length'),single.length);$('#length-slider').value=single.length/scale();$('#length').disabled=$('#length-slider').disabled=!!plan.locked;$('#length-note').textContent=plan.locked?plan.reason:plan.fixed===null?'Physical cut length. Free tube resizes about its centre.':plan.side.size?'End 1 stays fixed. The assembly on end 2 translates with the new length.':`Connected end ${plan.fixed+1} stays fixed. The free end moves.`;$('#detach-blocking').hidden=!plan.locked;$('#detach-blocking').onclick=()=>{selectedJoint=plan.joint;setTool('joints');inspector();$('#detach').scrollIntoView({block:'nearest'});};}
  $('#group-length-section').hidden=list.length<2;
  if(list.length>1){
    const plan=groupEdit?.plan??model.coordinatedLengthPlan(selected),min=plan.locked?0:Math.ceil(plan.minDelta*1000)/1000,max=plan.locked?0:Math.floor(plan.maxDelta*1000)/1000;
    for(const id of ['group-length','group-length-slider']){const input=$('#'+id);input.disabled=plan.locked;input.min=min/scale();input.max=max/scale();input.step=.001/scale();input.setAttribute('aria-label',`Change selected tube lengths${id.endsWith('slider')?' slider':''} in ${lengthUnit}`);input.removeAttribute('aria-invalid');showLengthInput(input,groupEdit?.delta??0);}
    $('#group-length-unit-label').textContent=lengthUnit;$('#group-length-min').textContent=lengthText(min);$('#group-length-max').textContent=lengthText(max);
    $('#group-length-slider').setAttribute('aria-valuetext',`${lengthText(groupEdit?.delta??0)} adjustment`);
    $('#group-length-note').textContent=plan.locked?unitText(plan.reason):`Same signed adjustment to each starting cut; unequal lengths stay unequal. ${plan.anchors.length?`In each connected group, the attached section with the lowest endpoint along the tube axis toward positive ${plan.axisLabel} stays fixed (ties: stable piece ID). Anchor section${plan.anchors.length>1?'s':''}: ${plan.anchors.map(id=>id.slice(0,8)).join(', ')}. Other sections translate rigidly.`:''} Free tubes keep their centres. Escape cancels; release, Enter or blur completes one undoable edit.`;
  }
  $('#ports-section').hidden=!list.length&&!joint;$('#ports').replaceChildren();
  for(const p of list) localPorts(p).forEach((def,i)=>{
    const connection=model.connections.find(c=>[c.a,c.b].some(e=>e.id===p.id&&e.port===i));const row=document.createElement('div');row.className='port-row';const button=document.createElement('button');button.textContent=`${list.length>1?CATALOG[p.type].name+' · ':''}End ${i+1} · ${def.type}${connection?' · joined':''}`;button.setAttribute('aria-pressed',pickedPorts.some(e=>e.id===p.id&&e.port===i));button.onclick=()=>{if(connection){selectedJoint=connection.id;inspector();showOverlays();}else pickPort({id:p.id,port:i});};row.append(button);$('#ports').append(row);
  });
  if(joint){const text=document.createElement('p');text.className='muted';text.textContent=`Joint ${joint.id.slice(0,8)} · ${CATALOG[model.get(joint.a.id).type].name} / ${CATALOG[model.get(joint.b.id).type].name}`;$('#ports').append(text);}
  $('#connect').hidden=pickedPorts.length!==2;$('#detach').hidden=!joint;
}
function pickPort(endpoint){if(model.occupied(endpoint.id,endpoint.port)){status('This port is occupied. Select and detach its joint first.',true);return;}selectedJoint=null;const i=pickedPorts.findIndex(e=>e.id===endpoint.id&&e.port===endpoint.port);if(i>=0)pickedPorts.splice(i,1);else{if(pickedPorts.length===2)pickedPorts=[];pickedPorts.push(endpoint);}inspector();showOverlays();status(pickedPorts.length===2?'Connect selected ports to align the assemblies.':'Port selected. Shift-select another piece, or choose a second port in Joints mode.');}
function round(n){return Math.round(n*1000)/1000;}
function summary(){const {rows,total}=model.materials();$('#summary').replaceChildren();if(!rows.length)$('#summary').textContent='Your cut list will appear here.';for(const rowData of rows){const {type,length,count}=rowData;const row=document.createElement('div');row.className='summary-row';const label=document.createElement('span'),value=document.createElement('b');label.textContent=type==='tube'?`Tube · ${lengthText(length)}`:materialName(rowData);value.textContent=`× ${count}`;row.append(label,value);$('#summary').append(row);}$('#total-length').textContent=lengthText(total);$('#summary-count').textContent=`${model.pieces.length} pieces`;$('#download-pdf').disabled=pdfExporting||!model.pieces.length;}
function refresh(){if(placement)placementPorts=placementTargets(model);updateInstructions();sync();inspector();summary();attach();showOverlays();$('#undo').disabled=!undo.length;$('#redo').disabled=!redo.length;$('#paste').disabled=!clipboard;$('#copy').disabled=!selected.size;$('#delete').disabled=!selected.size&&!selectedJoint;$('#save-state').textContent=storageOK?'Saved on this device':'Save JSON to keep your work';}
function updateInstructions(){
  const degrees=`${rotationIncrement}°`;
  $$('[data-turn]').forEach(b=>{const axis=b.dataset.turn;b.textContent=b.dataset.rotationLabel?`${b.dataset.rotationLabel} +${degrees} (${axis==='y'?'Q':'E'})`:`${axis.toUpperCase()} +${degrees}`;b.title=`Rotate around world ${axis.toUpperCase()} by ${degrees}`;b.disabled=!placement&&!selected.size;});
  $('#placement-bar').textContent=`Aim within ${SNAP_PIXELS} screen px of a free port · move away to place freely · Q/E: rotate ${degrees} · Esc: cancel`;
  $('#movement-bar').hidden=tool!=='move-piece'||!!placement;
  workspace.dataset.mode=placement?'placement':tool;
}
function setTool(next){cancelInteraction();if(placement)cancelPlacement();tool=next;$$('[data-tool]').forEach(b=>b.setAttribute('aria-pressed',b.dataset.tool===tool||(tool==='move-piece'&&b.dataset.tool==='translate')));attach();showOverlays();updateInstructions();canvas.style.cursor=tool==='marquee'?'crosshair':tool==='move-piece'?'grab':'default';status(({select:'Click selects · Shift-click toggles · left drag pans · right drag orbits · double-click a piece to move.',translate:'Drag an axis handle to move. Double-click a piece for plane movement. Q/E rotate.', 'move-piece':'Piece movement mode · drag a highlighted piece on the working plane · Q/E rotate · Esc or Select exits.',rotate:'Drag a world-axis ring: magnetic angles catch within 3° and hold through 5°. Keep dragging beyond the catch for free rotation. Q/E use Rotation increment; connected pieces rotate together.',marquee:'Left drag selects pieces whose centres are inside the rectangle. Shift adds to selection.',joints:'Click cyan joint markers to inspect and detach. Free port markers can be paired.'})[tool]);}
function rotateDiscrete(axis){
  if(transaction||pointerGesture&&!placement||gizmo.dragging)return;
  const rotation=new THREE.Quaternion().setFromAxisAngle(vec(axis==='x'?[1,0,0]:axis==='y'?[0,1,0]:[0,0,1]),THREE.MathUtils.degToRad(rotationIncrement));
  if(placement){
    // Intent is never fed back from automatic alignment. Reproject the requested
    // orientation onto the joint constraint independently on every update.
    placement.intentQ=rotation.multiply(quat(placement.intentQ)).normalize().toArray();
    placement.q=[...placement.intentQ];
    if(placementPointer)updatePlacement(placementPointer,false);else{previewPlacement();showOverlays();}
    return;
  }
  if(selected.size)action(()=>model.transform(expanded(),rotation,center(selected)),`Rotated the connected selection around world ${axis.toUpperCase()} by ${rotationIncrement}°.`);
}
function setRotationIncrement(value){
  if(!Number.isFinite(value)||value<=0){status('Rotation increment must be a positive finite number.',true);$('#rotation-custom').value=rotationIncrement;return;}
  rotationIncrement=value;$('#rotation-increment').value=[15,30,45,90].includes(value)?String(value):'custom';$('#rotation-custom-label').hidden=$('#rotation-increment').value!=='custom';$('#rotation-custom').value=value;
  try{localStorage.setItem(ROTATION_STORAGE,String(value));}catch{status('Rotation preference could not be saved on this browser.',true);}updateInstructions();
}
function numericTransform(prefix,axis,input){if(prefix==='position'&&input.value===input.dataset.displayValue)return;const value=input.valueAsNumber*(prefix==='position'?scale():1);if(!Number.isFinite(value)||Math.abs(value)>100000){inspector();status(prefix==='position'?'Enter a finite position between −100,000 mm and 100,000 mm.':'Enter a finite value between −100,000 and 100,000.',true);return;}const anchor=model.pieces.find(p=>selected.has(p.id));if(!anchor)return;action(()=>{if(prefix==='position'){const delta=new THREE.Vector3();delta[axis]=value-anchor.p[['x','y','z'].indexOf(axis)];model.transform(expanded(),undefined,undefined,delta);}else{const e=new THREE.Euler().setFromQuaternion(quat(anchor.q),'XYZ');e[axis]=THREE.MathUtils.degToRad(input.valueAsNumber);const q=new THREE.Quaternion().setFromEuler(e).multiply(quat(anchor.q).invert());model.transform(expanded(),q,vec(anchor.p));}},'Transform applied to the connected selection.');}

// Gizmo gestures are one transaction, even though the state and snap preview update every frame.
gizmo.addEventListener('dragging-changed',e=>{
  orbit.enabled=!e.value;if(e.value){
    begin();baseTransform=clone(model.data());activeIds=expanded();cancelledGesture=false;
    // Match TransformControls' in-plane fallback exactly. Its ordinary world
    // X/Y/Z handles already supply continuous, unbounded raw angles.
    const axis=({X:[1,0,0],Y:[0,1,0],Z:[0,0,1]})[gizmo.axis];
    rotationDrag=tool==='rotate'&&gizmo.axis!=='XYZE'?new MagneticRotation({wrapped:gizmo.axis==='E'||!!axis&&vec(axis).cross(gizmo.eye).lengthSq()===0}):null;
  }
  else{
    rotationDrag=null;
    if(transaction){if(cancelledGesture){restore(transaction);transaction=null;}else{try{finishSnap();commit();}catch(error){restore(transaction);transaction=null;refresh();status(error.message,true);}}}
    baseTransform=null;refresh();
  }
});
gizmo.addEventListener('objectChange',()=>{
  if(!baseTransform||!transaction||cancelledGesture)return;
  if(rotationDrag){
    const angle=rotationDrag.update(gizmo.rotationAngle);
    // Read raw input before changing the displayed pivot. TransformControls
    // recomputes its next raw angle from the original pointer and drag start.
    pivot.quaternion.setFromAxisAngle(gizmo.rotationAxis,angle);
    gizmo.rotationAngle=angle;
  }
  const base=new Design(baseTransform),origin=centerFrom(base,selected);model=base;model.transform(activeIds,pivot.quaternion,origin,pivot.position.clone().sub(origin));sync();findCandidate(activeIds);
});
function centerFrom(m,ids){const a=new THREE.Vector3();let n=0;for(const p of m.pieces)if(ids.has(p.id)){a.add(vec(p.p));n++;}return a.divideScalar(n||1);}

// Placement uses an explicit working plane and an actual hollow-geometry preview.
function workPlane(through=null){const mode=$('#plane').value,normal=mode==='front'?vec([0,0,1]):mode==='side'?vec([1,0,0]):vec([0,1,0]);const value=planeOffset;return new THREE.Plane(normal,through?-normal.dot(through):-value);}
function setRay(event){const r=canvas.getBoundingClientRect();pointer.set((event.clientX-r.left)/r.width*2-1,-(event.clientY-r.top)/r.height*2+1);ray.setFromCamera(pointer,camera);}
function planePoint(event,plane=workPlane(),snap=true){setRay(event);const hit=ray.ray.intersectPlane(plane,new THREE.Vector3());if(!hit)return null;if(snap&&$('#grid-snap').checked)hit.toArray().forEach((v,i)=>hit.setComponent(i,Math.round(v/25)*25));return hit;}
function startPlacement(type){if(!Object.hasOwn(CATALOG,type)){status('Unsupported component type. Only standard PVC components are allowed.',true);return;}cancelInteraction();cancelPlacement();selectedJoint=null;placement={type,p:[0,60,0],freeP:[0,60,0],q:[0,0,0,1],intentQ:[0,0,0,1],length:400};placementPorts=placementTargets(model);orbit.enabled=false;gizmo.detach();$('#placement-bar').hidden=false;$('#empty').hidden=true;canvas.style.cursor='crosshair';previewPlacement();updateInstructions();status(`Placing ${CATALOG[type].name}. Aim within ${SNAP_PIXELS} screen px of a free compatible port to connect; move away for free placement. Click or release the catalog drag to commit. Q/E rotate immediately; Escape cancels.`);}
function previewPlacement(){
  if(!placement)return;
  if(!placementMesh){clearGhost();placementMesh=geometry({...placement,id:'preview'});placementMesh.traverse(o=>{if(o.isMesh){o.material.transparent=true;o.material.opacity=.55;o.material.color.set(0x2aadaf);o.material.depthWrite=false;o.castShadow=false;}});ghost.add(placementMesh);}
  ghost.visible=true;placementMesh.position.copy(vec(placement.p));placementMesh.quaternion.copy(quat(placement.q));
  workspace.dataset.connection=placement.connection?'ready':'free';
  const guide=$('#placement-guide'),connection=placement.connection;
  guide.toggleAttribute('hidden',!connection);
  if(connection&&placementPointer){
    const rect=canvas.getBoundingClientRect(),x=connection.screen.x-rect.left,y=connection.screen.y-rect.top;
    const line=guide.querySelector('line'),circle=guide.querySelector('circle');
    for(const [name,value] of Object.entries({x1:placementPointer.clientX-rect.left,y1:placementPointer.clientY-rect.top,x2:x,y2:y}))line.setAttribute(name,value);
    circle.setAttribute('cx',x);circle.setAttribute('cy',y);
  }
}
function updatePlacement(event,retainSource=true){
  placementPointer={clientX:event.clientX,clientY:event.clientY};
  camera.updateMatrixWorld(true);
  let point=planePoint(event);
  if(point){if($('#plane').value==='ground')point.y+=placement.type==='tube'?RADIUS:22;if(point.toArray().every(n=>Number.isFinite(n)&&Math.abs(n)<1e7))placement.freeP=point.toArray();else point=null;}
  const prospective={...placement,id:'preview',p:placement.freeP,q:placement.intentQ};
  const rect=canvas.getBoundingClientRect();
  const previous=retainSource?placement.connection:placement.connection&&{target:placement.connection.target};
  const connection=$('#port-snap').checked?choosePlacement({piece:prospective,targets:placementPorts,pointer:{x:event.clientX,y:event.clientY},project:p=>projectPort(p,camera,rect),previous,
    visible:target=>{
      const s=projectPort(target.mouth,camera,rect);if(!s)return false;
      const visibilityRay=new THREE.Raycaster();visibilityRay.setFromCamera(new THREE.Vector2((s.x-rect.left)/rect.width*2-1,1-(s.y-rect.top)/rect.height*2),camera);
      const hit=visibilityRay.intersectObjects(parts.children,true)[0];
      return !hit||hit.distance>=visibilityRay.ray.origin.distanceTo(target.mouth)-24;
    }}):null;
  placement.connection=connection;
  if(!connection&&!point){ghost.visible=false;$('#placement-guide').setAttribute('hidden','');workspace.dataset.connection='free';showOverlays();status('Working plane is edge-on or out of range. Aim near a connection or choose a different plane.',true);return false;}
  placement.p=connection?[...connection.p]:[...placement.freeP];placement.q=connection?[...connection.q]:[...placement.intentQ];
  previewPlacement();showOverlays();status(connection?'Connection preview · click or release to connect exactly as shown · Q/E: change orientation.':'Free placement · aim near a compatible connection to snap · click or release to place.');return true;
}
function commitPlacement(){const spec=clone(placement);cancelPlacement();action(()=>{const piece=model.add(spec.type,spec.p,spec.length,spec.q);if(spec.connection)model.connect({id:piece.id,port:spec.connection.source},spec.connection.target,false);selected=new Set([piece.id]);selectedJoint=null;},spec.connection?'Placed and connected.':'Piece placed. Double-click it for movement mode; Q/E rotate the selection.');}

function cancelPlacement(){placement=null;placementPointer=null;placementPorts=[];placementMesh=null;ghost.visible=true;delete workspace.dataset.connection;candidate=null;clearGhost();$('#placement-bar').hidden=true;$('#placement-guide').setAttribute('hidden','');orbit.enabled=true;canvas.style.cursor='default';showOverlays();$('#empty').hidden=!!model.pieces.length;attach();updateInstructions();}
function hitPiece(event){setRay(event);const hit=ray.intersectObjects(parts.children,true)[0];if(!hit)return null;let o=hit.object;while(o&&!o.userData.id)o=o.parent;return o?.userData.id||null;}
function hitOverlay(event){setRay(event);return ray.intersectObjects(overlays.children,false).find(h=>!h.object.userData.candidate)?.object.userData;}

// Capture assigns one owner before OrbitControls / TransformControls see a gesture.
// Camera input stays with OrbitControls, but sub-threshold motion never reaches it.
function cancelInteraction(){
  if(pointerGesture)pointerGesture.cancelled=true;
  cancelledGesture=true;baseTransform=null;rotationDrag=null;sliderBase=null;groupEdit=null;groupCancelled=true;groupRangeKey=null;groupRangePointer=null;
  if(transaction){restore(transaction);transaction=null;}
  if(gizmo.dragging)gizmo.pointerUp({button:0});
  directDrag=null;marquee=null;$('#marquee-box').hidden=true;candidate=null;clearGhost();orbit.enabled=!placement;refresh();
}
function clickSelection(e){const id=hitPiece(e);if(id){const next=e.shiftKey?new Set(selected):new Set();if(e.shiftKey&&next.has(id))next.delete(id);else next.add(id);setSelection(next);}else if(!e.shiftKey)setSelection([]);}
canvas.addEventListener('contextmenu',e=>e.preventDefault());
canvas.addEventListener('pointerdown',e=>{
  if(pointerGesture){e.stopImmediatePropagation();return;}
  if(e.button!==0)return;
  canvas.focus();cancelledGesture=false;
  const owner=placement?'placement':gizmo.axis&&gizmo.object?'gizmo':tool==='marquee'?'marquee':tool==='joints'?'joint':tool==='move-piece'&&!e.shiftKey&&hitPiece(e)?'piece':e.shiftKey?'click':'camera';
  pointerGesture={owner,id:e.pointerId,x:e.clientX,y:e.clientY,moved:false,cancelled:false};
  if(owner==='camera'||owner==='gizmo')return;
  orbit.enabled=false;
  e.stopImmediatePropagation();canvas.setPointerCapture(e.pointerId);
  if(owner==='marquee'){const r=canvas.getBoundingClientRect();marquee={x:e.clientX-r.left,y:e.clientY-r.top,shift:e.shiftKey};}
  if(owner==='piece'){
    const id=hitPiece(e);if(!expanded().has(id))setSelection([id]);
    const plane=workPlane(vec(model.get(id).p)),start=planePoint(e,plane,false);
    if(start)directDrag={plane,start,base:clone(model.data()),ids:expanded(),moved:false};
    else status('Working plane is edge-on. Choose a different plane or camera view.',true);
  }
},true);
canvas.addEventListener('pointermove',e=>{
  const g=pointerGesture;
  if(g&&g.id===e.pointerId){
    g.moved ||= Math.hypot(e.clientX-g.x,e.clientY-g.y)>=DRAG_THRESHOLD;
    if(g.owner!=='camera'&&g.owner!=='gizmo'||!g.moved)e.stopImmediatePropagation();
    if(g.cancelled)return;
    if(g.owner==='camera'||g.owner==='gizmo'||!g.moved)return;
    if(marquee){const r=canvas.getBoundingClientRect(),x=e.clientX-r.left,y=e.clientY-r.top,b=$('#marquee-box');b.hidden=false;Object.assign(b.style,{left:Math.min(x,marquee.x)+'px',top:Math.min(y,marquee.y)+'px',width:Math.abs(x-marquee.x)+'px',height:Math.abs(y-marquee.y)+'px'});return;}
    if(directDrag){const point=planePoint(e,directDrag.plane,false);if(point){begin();const delta=point.sub(directDrag.start);if($('#grid-snap').checked)delta.toArray().forEach((v,i)=>delta.setComponent(i,Math.round(v/25)*25));directDrag.moved=true;model=new Design(directDrag.base);model.transform(directDrag.ids,undefined,undefined,delta);sync();findCandidate(directDrag.ids);}return;}
  }
  if(placement){updatePlacement(e);return;}
  if(gizmo.dragging)return;const id=hitPiece(e);if(id!==hovered){hovered=id;paint();}
},true);
canvas.addEventListener('pointerleave',()=>{hovered=null;paint();});
canvas.addEventListener('pointerup',e=>{
  const g=pointerGesture;if(e.button!==0||!g||g.id!==e.pointerId)return;
  pointerGesture=null;
  doubleClickEligible=!g.cancelled&&!g.moved&&['camera','click','piece'].includes(g.owner);
  const owned=g.owner!=='camera'&&g.owner!=='gizmo';if(owned)e.stopImmediatePropagation();
  if(!g.cancelled){
    if(g.owner==='placement'&&placement){if(!g.moved&&updatePlacement(e))commitPlacement();}
    else if(marquee){const r=canvas.getBoundingClientRect(),x=e.clientX-r.left,y=e.clientY-r.top,next=marquee.shift?new Set(selected):new Set();if(g.moved)for(const p of model.pieces){const v=vec(p.p).project(camera),sx=(v.x+1)/2*r.width,sy=(1-v.y)/2*r.height;if(v.z>=-1&&v.z<=1&&sx>=Math.min(x,marquee.x)&&sx<=Math.max(x,marquee.x)&&sy>=Math.min(y,marquee.y)&&sy<=Math.max(y,marquee.y))next.add(p.id);}marquee=null;$('#marquee-box').hidden=true;setSelection(next);}
    else if(directDrag){try{if(directDrag.moved){finishSnap();commit('Moved the connected selection. Piece movement mode remains active.');}}catch(error){restore(transaction);transaction=null;refresh();status(error.message,true);}directDrag=null;}
    else if(!g.moved&&g.owner!=='gizmo'){
      const overlay=g.owner==='joint'?hitOverlay(e):null;
      if(overlay?.joint){selectedJoint=overlay.joint;selected.clear();refresh();}else if(overlay?.endpoint)pickPort(overlay.endpoint);else clickSelection(e);
    }
  }
  if(owned&&canvas.hasPointerCapture(e.pointerId))canvas.releasePointerCapture(e.pointerId);
  if(owned)orbit.enabled=!placement;
},true);
canvas.addEventListener('dblclick',e=>{if(!doubleClickEligible||e.button!==0||placement||pointerGesture||tool==='marquee'||tool==='joints'||gizmo.dragging)return;const id=hitPiece(e);if(id){setSelection([id]);setTool('move-piece');}});
canvas.addEventListener('pointercancel',()=>{cancelInteraction();pointerGesture=null;});
canvas.addEventListener('lostpointercapture',()=>{if(pointerGesture){cancelInteraction();pointerGesture=null;}});
workspace.addEventListener('dragover',e=>{if(placement){e.preventDefault();e.dataTransfer.dropEffect='copy';updatePlacement(e);}});
workspace.addEventListener('drop',e=>{e.preventDefault();if(placement&&updatePlacement(e))commitPlacement();});

// Catalog is generated from the same definitions as geometry and port compatibility.
function thumbnail(type){const paths={tube:'M14 47 L65 17',coupling:'M20 44 L59 22',elbow90:'M16 45 Q45 47 45 18',elbow45:'M14 45 L35 34 Q40 30 61 30',tee:'M12 47 L65 17 M38 32 L56 53',cross:'M12 47 L65 17 M20 12 L57 53',corner:'M12 47 L38 32 L65 47 M38 32 L38 9'};return `<svg viewBox="0 0 78 64" aria-hidden="true"><defs><filter id="shadow-${type}"><feDropShadow dx="1" dy="3" stdDeviation="2" flood-color="#69888f" flood-opacity=".25"/></filter></defs><path d="${paths[type]}" stroke="#aec3c6" stroke-width="${type==='tube'?12:17}" fill="none" stroke-linecap="butt" filter="url(#shadow-${type})"/><path d="${paths[type]}" stroke="#f3f8f7" stroke-width="${type==='tube'?9:13}" fill="none"/><path d="${paths[type]}" stroke="#ffffff" stroke-width="3" opacity=".9" fill="none"/>${type==='tube'?'<ellipse cx="65" cy="17" rx="5" ry="6" fill="#6f9298" transform="rotate(48 65 17)"/><ellipse cx="65" cy="17" rx="3" ry="4" fill="#35575f" transform="rotate(48 65 17)"/>':''}</svg>`;}
for(const [type,def] of Object.entries(CATALOG)){const b=document.createElement('button');b.className='material';b.draggable=true;b.dataset.type=type;b.innerHTML=thumbnail(type);const name=document.createElement('strong'),note=document.createElement('small');name.textContent=def.name;note.textContent=def.note;b.append(name,note);b.onclick=()=>startPlacement(type);b.addEventListener('dragstart',e=>{e.dataTransfer.setData('text/plain',type);e.dataTransfer.effectAllowed='copy';startPlacement(type);});b.addEventListener('dragend',()=>{if(placement)cancelPlacement();});$('#catalog').append(b);}
$('.materials .count').textContent=Object.keys(CATALOG).length;

function editLength(value){const p=model.pieces.find(p=>selected.has(p.id));if(!p)return;if(!sliderBase){begin();sliderBase=clone(transaction.data);}try{const next=new Design(sliderBase);next.resize(p.id,Number(value)*scale());model=next;sync();summary();showOverlays();showLengthInput($('#length'),Number(value)*scale());$('#length-slider').value=value;}catch(e){status(e.message,true);}}
function finishLengthEdits(){
  if(groupEdit){groupEdit=null;groupRangeKey=null;commit('Selected tube lengths updated together; all joints and other cuts preserved.');}
  if(sliderBase){sliderBase=null;commit('Tube cut length updated; valid joints preserved.');}
}
function editGroupLength(input){
  if(groupCancelled)return;
  if(!groupEdit){const plan=model.coordinatedLengthPlan(selected);if(plan.locked){status(plan.reason,true);return;}begin();groupEdit={base:clone(transaction.data),ids:[...selected],plan,delta:0};}
  try{
    const delta=input.valueAsNumber*scale();
    if(!input.value.trim()||!Number.isFinite(delta))throw Error('Enter a finite signed length adjustment.');
    // Publish only a fully solved and validated candidate. Every preview starts
    // from the same snapshot; invalid input leaves the last valid preview live.
    const next=new Design(groupEdit.base);next.resizeTogether(groupEdit.ids,delta);model=next;groupEdit.delta=delta;
    const other=input.id==='group-length'?$('#group-length-slider'):$('#group-length');showLengthInput(other,delta);
    input.removeAttribute('aria-invalid');other.removeAttribute('aria-invalid');$('#group-length-slider').setAttribute('aria-valuetext',`${lengthText(delta)} adjustment`);
    showSelectedPieces(model.pieces.filter(p=>selected.has(p.id)),null);sync();summary();showOverlays();attach();
    status(`Selected tubes: ${delta>=0?'+':''}${lengthText(delta)} each. Escape restores the starting geometry.`);
  }catch(error){input.setAttribute('aria-invalid','true');status(error.message,true);}
}
for(const id of ['group-length','group-length-slider']){
  const input=$('#'+id),range=input.type==='range';
  input.addEventListener('focus',()=>{groupCancelled=false;});
  input.addEventListener('pointerdown',e=>{if(document.activeElement!==input)finishLengthEdits();groupCancelled=false;if(range)groupRangePointer=e.pointerId;});
  input.addEventListener('input',()=>{if(!range)groupCancelled=false;editGroupLength(input);});
  input.addEventListener('change',()=>{if(!range||!groupRangeKey&&groupRangePointer===null)finishLengthEdits();});
  // Chromium may emit the range's first input before blurring the numeric
  // field. That blur belongs to the previous focus, not the new slider drag.
  input.addEventListener('blur',e=>{if(!(groupRangePointer!==null&&e.relatedTarget===$('#group-length-slider')))finishLengthEdits();});
  input.addEventListener('pointercancel',()=>{cancelInteraction();status('Tube length adjustment cancelled.');});
  input.addEventListener('keydown',e=>{
    if(e.key==='Escape'){e.preventDefault();e.stopPropagation();cancelInteraction();status('Tube length adjustment cancelled; starting geometry restored.');}
    else if(e.key==='Enter'){e.preventDefault();finishLengthEdits();}
    else if(range&&['ArrowLeft','ArrowRight','ArrowUp','ArrowDown','Home','End','PageUp','PageDown'].includes(e.key)){groupCancelled=false;groupRangeKey=e.key;}
  });
  input.addEventListener('keyup',e=>{if(e.key===groupRangeKey){groupRangeKey=null;finishLengthEdits();}});
}
window.addEventListener('pointerup',e=>{if(e.pointerId===groupRangePointer){groupRangePointer=null;finishLengthEdits();}});
$('#length').addEventListener('change',e=>{const p=model.pieces.find(p=>selected.has(p.id));if(p&&e.target.value!==e.target.dataset.displayValue)action(()=>model.resize(p.id,e.target.valueAsNumber*scale()),'Tube cut length updated; valid joints preserved.');});
for(const button of [$('#length-unit'),$('#group-length-unit')])button.onclick=()=>{finishLengthEdits();lengthUnit=LENGTH_UNITS[(LENGTH_UNITS.indexOf(lengthUnit)+1)%3];updateLengthUnits();inspector();summary();};
$('#plane-offset').onchange=e=>{if(e.target.value===e.target.dataset.displayValue)return;const value=e.target.valueAsNumber*scale();if(Number.isFinite(value))planeOffset=value;else status('Enter a finite plane offset.',true);showLengthInput(e.target,planeOffset);};
$('#length-slider').addEventListener('input',e=>editLength(e.target.value));
$('#length-slider').addEventListener('change',()=>{sliderBase=null;commit('Tube cut length updated; valid joints preserved.');});
$('#length-slider').addEventListener('blur',()=>{if(sliderBase){sliderBase=null;commit();}});
$$('[data-tool]').forEach(b=>b.onclick=()=>setTool(b.dataset.tool));
$$('[data-turn]').forEach(b=>b.onclick=()=>rotateDiscrete(b.dataset.turn));
$('#rotation-increment').onchange=e=>{const custom=e.target.value==='custom';$('#rotation-custom-label').hidden=!custom;if(custom){$('#rotation-custom').focus();}else setRotationIncrement(Number(e.target.value));};
$('#rotation-custom').onchange=e=>setRotationIncrement(e.target.valueAsNumber);
try{const saved=Number(localStorage.getItem(ROTATION_STORAGE));if(saved>0&&Number.isFinite(saved))rotationIncrement=saved;}catch{}
setRotationIncrement(rotationIncrement);
$('#undo').onclick=()=>history('undo');$('#redo').onclick=()=>history('redo');
$('#copy').onclick=()=>{if(selected.size){clipboard=model.copy(selected);$('#paste').disabled=false;status(`Copied ${clipboard.pieces.length} pieces and ${clipboard.connections.length} internal joints.`);}};
$('#paste').onclick=()=>{if(clipboard)action(()=>{selected=model.paste(clipboard);selectedJoint=null;},'Pasted with fresh IDs, preserved internal joints, and an 80 mm offset.');};
$('#delete').onclick=()=>{if(selectedJoint)detach();else if(selected.size)action(()=>{model.remove(selected);selected.clear();},'Deleted selected pieces and their incident joints.');};
function detach(){if(selectedJoint)action(()=>{model.disconnect(selectedJoint);selectedJoint=null;},'Joint detached. Pieces stay in place; connected assemblies recalculated.');}
$('#detach').onclick=detach;$('#connect').onclick=()=>{if(pickedPorts.length===2)action(()=>{model.connect(...pickedPorts);pickedPorts=[];},'Ports connected. The assemblies now move together.');};
$('#select-all').onclick=()=>setSelection(model.pieces.map(p=>p.id));$('#clear').onclick=()=>setSelection([]);$('#select-assembly').onclick=()=>setSelection(expanded());
$('#start').onclick=()=>startPlacement('tube');$('#grid-snap').onchange=attach;$('#port-snap').onchange=()=>{candidate=null;if(placement){if(placementPointer)updatePlacement(placementPointer);else previewPlacement();}else{clearGhost();showOverlays();}};
$('#help-toggle').onclick=()=>{$('#help').showModal();$('#help-toggle').setAttribute('aria-expanded','true');};$('#help-close').onclick=()=>$('#help').close();$('#help').addEventListener('close',()=>$('#help-toggle').setAttribute('aria-expanded','false'));

// Persistence is versioned and strictly validated before replacement.
function mayReplace(){return JSON.stringify(model.data())===exported||!model.pieces.length||confirm('Replace this design? Changes are saved on this browser, but will be overwritten. Save JSON first if you need a separate copy.');}
$('#new').onclick=()=>{if(mayReplace()){cancelPlacement();action(()=>{model=new Design();selected.clear();selectedJoint=null;},'Started a new design. Undo can restore the previous design.');exported=JSON.stringify(model.data());}};
for(const t of TEMPLATES){const option=document.createElement('option');option.value=t.id;option.textContent=t.name;$('#template').append(option);}
function previewTemplate(){const t=TEMPLATES.find(t=>t.id===$('#template').value);$('#template-description').textContent=t.description;$('#template-dimensions').textContent=t.dimensions;}
$('#template').onchange=previewTemplate;previewTemplate();
$('#load-template').onclick=()=>{
  const t=TEMPLATES.find(t=>t.id===$('#template').value);let incoming;
  try{incoming=validate(buildTemplate(t?.id).data());}catch(error){status('Could not load template: '+error.message,true);return;}
  if(!mayReplace())return;
  // Roll back pending gestures before taking the single replacement snapshot.
  cancelInteraction();cancelPlacement();setTool('select');
  action(()=>{model=incoming;selected.clear();selectedJoint=null;pickedPorts=[];hovered=null;placementPointer=null;pointerGesture=null;doubleClickEligible=false;},`Loaded ${t.name}. ${t.dimensions} Undo restores the previous design.`);
  frame();
};
$('#export').onclick=()=>{try{const data=JSON.stringify(model.data(),null,2),blob=new Blob([data],{type:'application/json'}),url=URL.createObjectURL(blob),a=document.createElement('a');a.href=url;a.download='pvc-design.json';a.click();setTimeout(()=>URL.revokeObjectURL(url),2000);exported=JSON.stringify(model.data());status('Design exported as pvc-design.json.');}catch(error){status('Could not export JSON: '+error.message,true);}};
// Read only the committed snapshot during an in-progress transform. Placement lives outside it.
$('#download-pdf').onclick=async()=>{
  if(pdfExporting)return;
  let data;const unit=lengthUnit;
  try{data=validate(clone(transaction?.data??model.data())).data();}catch(error){status('Could not export PDF: '+error.message,true);return;}
  if(!data.pieces.length)return;
  pdfExporting=true;const button=$('#download-pdf');button.disabled=true;button.setAttribute('aria-busy','true');
  status('PDF: preparing materials and eight views…');
  try{
    const {createDesignPDF,downloadPDF}=await import('./pvc-pdf.mjs');
    const blob=await createDesignPDF(data,{unit,title:$('.document-title').firstChild.textContent.trim(),onProgress:message=>status(message)});
    downloadPDF(blob);status(`Downloaded pvc-design.pdf · ${blob.pageCount} pages, materials and 8 views.`);
  }catch(error){status('Could not export PDF: '+error.message,true);}
  finally{pdfExporting=false;button.removeAttribute('aria-busy');button.disabled=!model.pieces.length;}
};
$('#import').onclick=()=>$('#file').click();$('#file').onchange=async e=>{const file=e.target.files[0];if(!file)return;try{if(file.size>5e6)throw Error('Design file exceeds the 5 MB limit.');const incoming=validate(JSON.parse(await file.text()));if(!mayReplace())return;cancelPlacement();action(()=>{model=incoming;selected.clear();selectedJoint=null;},`Loaded ${incoming.pieces.length} pieces and ${incoming.connections.length} valid joints.`);exported=JSON.stringify(model.data());frame();}catch(error){status('Could not load design: '+error.message,true);}finally{e.target.value='';}};
try{const saved=localStorage.getItem(STORAGE);if(saved){model=validate(JSON.parse(saved));status(`Restored ${model.pieces.length} pieces from this browser.`);}}catch(error){status('Saved work could not be restored: '+error.message+'. Load a JSON backup to recover it.',true);}

// Cameras, resize and world-axis indicator.
function resize(){const w=workspace.clientWidth,h=workspace.clientHeight;renderer.setSize(w,h,false);cameraPerspective.aspect=w/h;cameraPerspective.updateProjectionMatrix();const vertical=(cameraOrtho.top-cameraOrtho.bottom)/2;cameraOrtho.left=-vertical*w/h;cameraOrtho.right=vertical*w/h;cameraOrtho.updateProjectionMatrix();if(placement&&placementPointer)updatePlacement(placementPointer);}
const observer=new ResizeObserver(resize);observer.observe(workspace);
orbit.addEventListener('change',()=>{if(placement&&placementPointer)updatePlacement(placementPointer);});
function frame(){const ids=selected.size?expanded():new Set(model.pieces.map(p=>p.id));if(!ids.size)return;sync();const box=new THREE.Box3();for(const id of ids)box.expandByObject(meshes.get(id));const size=box.getSize(new THREE.Vector3()),target=box.getCenter(new THREE.Vector3()),radius=Math.max(size.length()/2,100),aspect=workspace.clientWidth/workspace.clientHeight;
  const dir=camera.position.clone().sub(orbit.target).normalize();orbit.target.copy(target);
  if(camera.isPerspectiveCamera)camera.position.copy(target).addScaledVector(dir,radius/Math.sin(THREE.MathUtils.degToRad(camera.fov/2))*1.25/Math.min(aspect,1));
  else{camera.position.copy(target).addScaledVector(dir,5000);const half=radius*1.3/Math.min(aspect,1);camera.top=half;camera.bottom=-half;camera.left=-half*aspect;camera.right=half*aspect;camera.zoom=1;camera.updateProjectionMatrix();}orbit.update();}
$('#frame').onclick=frame;
$('#camera').onchange=e=>{const view=e.target.value,target=orbit.target.clone();camera=view==='perspective'?cameraPerspective:cameraOrtho;orbit.object=camera;gizmo.camera=camera;orbit.enableRotate=view==='perspective';camera.up.set(0,1,0);if(view==='top')camera.up.set(0,0,-1);const d=({perspective:[1,.8,1],top:[0,1,0],front:[0,0,1],side:[1,0,0]})[view];camera.position.copy(target).addScaledVector(vec(d).normalize(),2000);camera.lookAt(target);resize();orbit.update();frame();$('#view-label').textContent=e.target.selectedOptions[0].textContent;};
function orientation(){const inverse=camera.quaternion.clone().invert(),lines=$('#axis-lines');lines.replaceChildren();for(const [axis,label,color] of [[[1,0,0],'X','#c45b55'],[[0,1,0],'Y','#479a69'],[[0,0,1],'Z','#558dc7']]){const v=vec(axis).applyQuaternion(inverse),x=42+v.x*27,y=42-v.y*27;const line=document.createElementNS('http://www.w3.org/2000/svg','line');for(const [k,val] of Object.entries({x1:42,y1:42,x2:x,y2:y,stroke:color,'stroke-width':2}))line.setAttribute(k,val);const text=document.createElementNS(line.namespaceURI,'text');text.setAttribute('x',x-4);text.setAttribute('y',y-5);text.setAttribute('fill',color);text.setAttribute('font-size',11);text.textContent=label;lines.append(line,text);}}
// Capture static labels once; always convert their original millimetre text.
const walker=document.createTreeWalker(document.body,NodeFilter.SHOW_TEXT);
while(walker.nextNode()){const node=walker.currentNode;if(!node.parentElement.closest('script,#catalog,#length-unit,#status')&&/\bmm\b|millimetres/.test(node.textContent))lengthTemplates.push([node,node.textContent]);}
updateLengthUnits();
let animation;function render(){animation=requestAnimationFrame(render);if(orbit.enabled)orbit.update();orientation();renderer.render(scene,camera);}resize();refresh();render();
window.addEventListener('keydown',e=>{
  if((e.target.closest?.('input,textarea,select')||e.target.isContentEditable)||$('#help').open)return;const key=e.key.toLowerCase(),mod=e.ctrlKey||e.metaKey;
  if((pointerGesture||gizmo.dragging)&&key!=='escape'&&!(placement&&!mod&&['q','e'].includes(key))){e.preventDefault();return;}
  if(mod&&['c','v','z','y','a'].includes(key)){e.preventDefault();if(key==='c')$('#copy').click();if(key==='v')$('#paste').click();if(key==='z')history(e.shiftKey?'redo':'undo');if(key==='y')history('redo');if(key==='a')$('#select-all').click();return;}
  if(key==='escape'){e.preventDefault();const moving=tool==='move-piece';if(placement){cancelInteraction();cancelPlacement();status('Placement cancelled.');}else if(transaction||pointerGesture||moving){cancelInteraction();if(moving)setTool('select');status('Transform cancelled; piece movement mode exited.');}else{setSelection([]);pickedPorts=[];showOverlays();}return;}
  if(!mod&&(key==='q'||key==='e')){e.preventDefault();if(!e.repeat)rotateDiscrete(key==='q'?'y':'x');return;}
  if(placement)return;if(key==='delete'||key==='backspace'){e.preventDefault();$('#delete').click();}if(key==='f')frame();if(key==='g')setTool('translate');if(key==='r')setTool('rotate');if(key==='v')setTool('select');
});
window.addEventListener('pagehide',event=>{if(event.persisted)return;cancelAnimationFrame(animation);observer.disconnect();gizmo.dispose();orbit.dispose();clearGroup(parts);clearGroup(overlays);clearGroup(ghost);grid.geometry.dispose();grid.material.dispose();floor.geometry.dispose();floor.material.dispose();renderer.dispose();});
