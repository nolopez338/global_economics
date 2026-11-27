// Shared, unpainted component geometry for the workspace and isolated exports.
import * as THREE from '../vendor/three-0.170.0/three.module.js';
import {RADIUS,INNER_RADIUS,localPorts,vec} from './pvc-model.mjs';
import {personProperties} from './pvc-person.mjs';

export const PERSON_COLOR=0x71818b;
// Volumetric, low-poly silhouettes. The canonical figure spans y=0..1;
// one uniform scale changes every dimension, with the soles at local y=0.
function personGeometry(p){
  const {height,variant,category}=personProperties(p),woman=variant==='woman';
  const g=new THREE.Group(),mat=new THREE.MeshStandardMaterial({color:PERSON_COLOR,roughness:.85,metalness:0});
  function ellipsoid(position,size){const m=mesh(new THREE.SphereGeometry(1,16,12),mat,g);m.position.set(...position);m.scale.set(...size);}
  function limb(a,b,r1,r2){const start=vec(a),end=vec(b);const m=mesh(new THREE.CylinderGeometry(r2,r1,start.distanceTo(end),12),mat,g);m.position.copy(start).add(end).multiplyScalar(.5);m.quaternion.setFromUnitVectors(vec([0,1,0]),end.sub(start).normalize());}
  ellipsoid([0,.93,0],[.052,.07,.055]);
  limb([0,.82,0],[0,.88,0],.031,.028);
  const shape=new THREE.Shape();
  const outline=woman?[[-.085,.47],[-.104,.53],[-.067,.64],[-.102,.79],[-.062,.83],[.062,.83],[.102,.79],[.067,.64],[.104,.53],[.085,.47]]:[[-.084,.47],[-.091,.57],[-.119,.79],[-.064,.83],[.064,.83],[.119,.79],[.091,.57],[.084,.47]];
  outline.forEach(([x,y],i)=>i?shape.lineTo(x,y):shape.moveTo(x,y));shape.closePath();
  const torso=mesh(new THREE.ExtrudeGeometry(shape,{depth:.105,bevelEnabled:false,steps:1}),mat,g);torso.position.z=-.0525;
  for(const s of [-1,1]){
    const shoulder=[s*(woman?.101:.116),.785,0],elbow=[s*.144,.64,0],wrist=[s*.164,.505,.012];
    ellipsoid(shoulder,[.033,.036,.037]);limb(shoulder,elbow,.03,.024);ellipsoid(elbow,[.024,.024,.025]);limb(elbow,wrist,.024,.018);ellipsoid([s*.165,.488,.012],[.021,.033,.023]);
    const hip=[s*.055,.49,0],knee=[s*.061,.265,0],ankle=[s*.067,.045,0];
    limb(hip,knee,woman?.046:.044,.032);ellipsoid(knee,[.032,.034,.034]);limb(knee,ankle,.032,.022);
    const foot=mesh(new THREE.BoxGeometry(.058,.05,.12),mat,g);foot.position.set(s*.067,.025,.025);
  }
  g.scale.setScalar(height);Object.assign(g.userData,{id:p.id,type:p.type,height,variant,category});return g;
}

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
export function geometry(p){
  localPorts(p); // Reject unsupported types and socket overrides before allocating geometry.
  if(p.type==='person')return personGeometry(p);
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
    }
  }
  g.userData.id=p.id;g.userData.type=p.type;g.userData.length=p.length;return g;
}
export function dispose(group){const geometries=new Set(),materials=new Set();group.traverse(o=>{if(o.geometry)geometries.add(o.geometry);if(o.material)for(const m of Array.isArray(o.material)?o.material:[o.material])materials.add(m);});geometries.forEach(g=>g.dispose());materials.forEach(m=>m.dispose());group.clear();}
