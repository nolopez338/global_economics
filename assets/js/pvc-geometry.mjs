// Shared, unpainted component geometry for the workspace and isolated exports.
import * as THREE from '../vendor/three-0.170.0/three.module.js';
import {RADIUS,INNER_RADIUS,localPorts,vec} from './pvc-model.mjs';

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
export function dispose(group){const geometries=new Set(),materials=new Set();group.traverse(o=>{if(o.geometry)geometries.add(o.geometry);if(o.material)for(const m of Array.isArray(o.material)?o.material:[o.material])materials.add(m);});geometries.forEach(g=>g.dispose());materials.forEach(m=>m.dispose());group.clear();}
