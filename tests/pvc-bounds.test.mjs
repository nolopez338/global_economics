import test from 'node:test';
import assert from 'node:assert/strict';
import * as THREE from '../assets/vendor/three-0.170.0/three.module.js';
import {Design} from '../assets/js/pvc-model.mjs';
import {buildTemplate} from '../assets/js/pvc-templates.mjs';
import {geometry,dispose} from '../assets/js/pvc-geometry.mjs';
import {GeometryVertices,fitBox,orientedBox,hullVertices,boxCorners,WORLD_AXES} from '../assets/js/pvc-bounds.mjs';
import {projectBoundsPoint} from '../assets/js/pvc-bounds-overlay.mjs';

const rotation=new THREE.Quaternion().setFromEuler(new THREE.Euler(.37,.61,.23));
const axes=q=>WORLD_AXES.map(a=>new THREE.Vector3(...a).applyQuaternion(q).toArray());
const near=(a,b,tolerance=1e-5)=>assert(Math.abs(a-b)<=tolerance,`${a} != ${b} ± ${tolerance}`);
function contains(points,box,tolerance=1e-6){
  assert(box.axes.flat().every(Number.isFinite));
  const basis=box.axes.map(a=>new THREE.Vector3(...a));
  for(let a=0;a<3;a++){near(basis[a].length(),1,1e-10);for(let b=0;b<a;b++)near(basis[a].dot(basis[b]),0,1e-10);}
  for(let i=0;i<points.length;i+=3)for(let a=0;a<3;a++){
    const p=new THREE.Vector3().fromArray(points,i).sub(new THREE.Vector3(...box.center));
    assert(Math.abs(p.dot(basis[a]))<=box.size[a]/2+tolerance,`vertex ${i/3} outside axis ${a}`);
  }
}
function measured(pieces,check){const groups=pieces.map(p=>{const g=geometry(p);g.position.fromArray(p.p);g.quaternion.fromArray(p.q);return g;});try{const data=new GeometryVertices().collect(groups);return check(data,groups);}finally{groups.forEach(dispose);}}
function verify(points,seeds=[]){const world=fitBox(points),box=orientedBox(points,seeds);contains(points,world);contains(points,box);assert(box.volume<=world.volume+Math.max(1e-7,world.volume*1e-10));return box;}

test('single aligned and arbitrarily rotated rendered tube, including its wall thickness',()=>{
  for(const q of [[0,0,0,1],rotation.toArray()]){const m=new Design();m.add('tube',[75,80,-50],400,q);
    measured(m.pieces,({points,seeds})=>{const box=verify(points,seeds);const dims=[...box.size].sort((a,b)=>b-a);near(dims[0],400);
      // Geometry has a regular 32-gon cross-section: the minimum square touches
      // facets, not the ideal continuous cylinder. This is an analytic fixture.
      near(dims[1],32*Math.cos(Math.PI/32),1e-5);near(dims[2],dims[1],1e-5);near(box.volume,400*(32*Math.cos(Math.PI/32))**2,.02);
      if(q[3]===1)fitBox(points).size.forEach((v,i)=>near(v,[400,32,32][i]));
    });
  }
});

test('unknown rotated cuboid: multi-start optimization, not rotating a world AABB',()=>{
  const source={center:[1e6,17,-2e6],size:[400,120,32],axes:axes(rotation)},points=Float64Array.from(boxCorners(source).flat());
  const box=verify(points);near(box.volume,400*120*32,400*120*32*2e-4);assert(box.volume<fitBox(points).volume*.25);
});

test('world optimum is allowed; exact known dimensions and symmetric tie breaking',()=>{
  for(const size of [[1300,400,2200],[100,100,100]]){const points=Float64Array.from(boxCorners({center:[0,0,0],size,axes:WORLD_AXES}).flat());
    const result=verify(points);assert.deepEqual(result.axes,WORLD_AXES);assert.deepEqual(result.size,size);assert.deepEqual(orientedBox(points),result);
  }
});

test('asymmetric fitting includes curved body, socket rims and nested transforms',()=>{
  const m=new Design();m.add('elbow45',[200,100,-500],undefined,rotation.toArray());
  measured(m.pieces,({points,seeds},groups)=>{const box=verify(points,seeds),direct=[];
    groups[0].traverse(o=>{if(o.isMesh){const p=o.geometry.getAttribute('position');for(let i=0;i<p.count;i++)direct.push(...new THREE.Vector3().fromBufferAttribute(p,i).applyMatrix4(o.matrixWorld).toArray());}});
    contains(direct,box);assert(points.length>1000);assert(box.volume<fitBox(points).volume*.8);
  });
});

test('disconnected pieces with different rotations are optimized as a union',()=>{
  const m=new Design();m.add('tube',[-120,75,40],500,rotation.toArray());m.add('tee',[270,90,-80],undefined,new THREE.Quaternion().setFromEuler(new THREE.Euler(.9,-.3,.72)).toArray());m.add('corner',[0,250,130]);
  measured(m.pieces,({points,seeds})=>{verify(points,seeds);});
});

test('explicit selection excludes connected companions; assembly selection uses the union',()=>{
  const m=buildTemplate('ground'),single=m.pieces.find(p=>p.type==='tube'),connected=m.connected([single.id]);assert(connected.size>1);
  let singleVolume;measured([single],({points,seeds})=>{singleVolume=verify(points,seeds).volume;});
  measured(m.pieces.filter(p=>connected.has(p.id)),({points,seeds})=>{assert(verify(points,seeds).volume>singleVolume);});
});

test('exact and nearly planar/linear geometry, repeated points and empty selections',()=>{
  assert.equal(fitBox([]),null);assert.equal(orientedBox([]),null);
  for(const size of [[0,0,0],[800,0,0],[800,1e-7,2e-7],[800,300,0],[800,300,1e-7]]){
    for(const q of [new THREE.Quaternion(),rotation]){const points=Float64Array.from(boxCorners({center:[5,60,90],size,axes:axes(q)}).flat());const box=verify(points,[axes(q)]);
      assert(box.size.every(Number.isFinite));contains(points,box);assert.deepEqual(orientedBox(points,[axes(q)]),box);
    }
  }
});

test('cached nested vertices follow all parent/world transforms without mutating source data',()=>{
  const cache=new GeometryVertices(),parent=new THREE.Group(),piece=new THREE.Group(),nested=new THREE.Group(),mesh=new THREE.Mesh(new THREE.BoxGeometry(40,20,10));
  parent.position.set(300,-80,19);parent.quaternion.copy(rotation);parent.scale.set(1.2,.8,1.6);nested.position.set(17,23,-11);nested.rotation.set(.2,.4,.8);nested.scale.set(1,2,.7);nested.add(mesh);piece.add(nested);parent.add(piece);
  const before=mesh.geometry.getAttribute('position').array.slice(),first=cache.collect([piece]),local=cache.local.get(piece),world=cache.world.get(piece);
  cache.collect([piece]);assert.equal(cache.local.get(piece),local);assert.equal(cache.world.get(piece),world);
  parent.position.x+=500;piece.rotation.y=.56;const next=cache.collect([piece]);assert.equal(cache.local.get(piece),local);assert.notDeepEqual(next.points,first.points);
  const direct=[];const p=mesh.geometry.getAttribute('position');for(let i=0;i<p.count;i++)direct.push(...new THREE.Vector3().fromBufferAttribute(p,i).applyMatrix4(mesh.matrixWorld).toArray());
  contains(direct,verify(next.points,next.seeds));assert.deepEqual(p.array,before);dispose(parent);
});

test('hull reduction retains support planes across deterministic random directions',()=>{
  let seed=17;const random=()=>((seed=(Math.imul(seed,1664525)+1013904223)>>>0)/2**32);
  const points=Float64Array.from({length:1800},()=>random()-.5),hull=hullVertices(points);assert(hull.length<points.length);
  for(let i=0;i<100;i++){const q=new THREE.Quaternion().setFromEuler(new THREE.Euler(random()*6,random()*6,random()*6)),a=fitBox(points,axes(q)),b=fitBox(hull,axes(q));for(let j=0;j<3;j++)near(a.size[j],b.size[j],1e-9);}
});

test('mixed rendered geometry beats an independent 1024-orientation reference scan',()=>{
  const m=new Design();m.add('tube',[-120,75,40],500,rotation.toArray());m.add('elbow45',[200,110,-30],undefined,new THREE.Quaternion().setFromEuler(new THREE.Euler(.9,-.3,.72)).toArray());
  measured(m.pieces,({points,seeds})=>{const result=verify(points,seeds);let reference=Infinity,state=711;
    const random=()=>((state=(Math.imul(state,1664525)+1013904223)>>>0)/2**32);
    for(let i=0;i<1024;i++){const q=new THREE.Quaternion();
      const u=random(),a=2*Math.PI*random(),b=2*Math.PI*random();q.set(Math.sqrt(1-u)*Math.sin(a),Math.sqrt(1-u)*Math.cos(a),Math.sqrt(u)*Math.sin(b),Math.sqrt(u)*Math.cos(b));
      reference=Math.min(reference,fitBox(points,axes(q)).volume);
    }
    assert(result.volume<=reference*(1+1e-8));
  });
});

test('label projection rejects behind-camera, near/far-clipped and invalid points',()=>{
  for(const camera of [new THREE.PerspectiveCamera(42,1,1,1000),new THREE.OrthographicCamera(-100,100,100,-100,1,1000)]){
    camera.position.set(0,0,500);camera.lookAt(0,0,0);camera.updateMatrixWorld(true);
    assert.deepEqual(projectBoundsPoint([0,0,0],camera,800,800),{x:400,y:400});
    for(const point of [[0,0,501],[0,0,499.5],[0,0,-501],[NaN,0,0],[0,Infinity,0]])assert.equal(projectBoundsPoint(point,camera,800,800),null);
  }
});
