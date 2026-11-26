import test from 'node:test';
import assert from 'node:assert/strict';
import {Design,CATALOG,port,vec,quat,validate} from '../assets/js/pvc-model.mjs';
import {PerspectiveCamera,OrthographicCamera} from '../assets/vendor/three-0.170.0/three.module.js';
import {placementTargets,choosePlacement,projectPort} from '../assets/js/pvc-placement.mjs';
const piece=(type='tube',q=[0,0,0,1])=>({id:'preview',type,p:[0,0,0],q,length:400});
const flat=p=>({x:p.x,y:p.y,depth:100-p.z});
const query=(m,pointer,extra={})=>choosePlacement({piece:piece(),targets:placementTargets(m),pointer,project:flat,...extra});
test('screen proximity, hysteresis and strict release radius',()=>{
  const m=new Design(),a=m.add('cap',[0,0,0]),b=m.add('cap',[40,0,0]);
  const initial=query(m,{x:25,y:0});assert.equal(initial.target.id,a.id);
  assert.equal(query(m,{x:48,y:0},{previous:initial}).target.id,a.id);
  assert.equal(query(m,{x:55,y:0},{previous:initial}).target.id,b.id);
  assert.equal(query(m,{x:130,y:0},{previous:initial}),null);
  assert.equal(query(m,{x:25,y:65}),null);
});
test('occupied and incompatible targets excluded, query does not mutate model',()=>{
  const m=new Design(),cap=m.add('cap'),tube=m.add('tube');m.connect({id:tube.id,port:0},{id:cap.id,port:0});
  const before=m.data();assert.equal(query(m,{x:0,y:0}),null);assert.deepEqual(m.data(),before);
});
test('every fitting port aligns at the insertion stop; preview commits without realignment',()=>{
  for(const type of Object.keys(CATALOG))for(const q of [[0,0,0,1],[0,.7071067811865475,0,.7071067811865476]]){
    const m=new Design(),target=m.add(type==='tube'?'tee':'tube',[0,0,0]);
    for(const endpoint of placementTargets(m)){
      const before=m.data(),pointer=flat(endpoint.position);
      const preview=query(m,pointer,{piece:piece(type,q),targets:[endpoint]});assert(preview,type);
      assert.deepEqual(m.data(),before);
      const shifted=query(m,pointer,{piece:{...piece(type,q),p:[123.456789,987.654321,-113.257]},targets:[endpoint]});
      assert.deepEqual(shifted.p,preview.p,'Aligned position depends on free-plane coordinates');
      assert.deepEqual(shifted.q,preview.q);
      const added=m.add(type,preview.p,400,preview.q);m.connect({id:added.id,port:preview.source},preview.target,false);validate(m.data());
      assert.deepEqual(added.p,preview.p);assert.deepEqual(added.q,preview.q);
      const a=port(added,preview.source),b=port(target,endpoint.target.port);
      assert(a.position.distanceTo(b.position)<1e-8);assert(a.direction.dot(b.direction)<-.999999);
      const socket=a.type==='socket'?a:b;assert(Math.abs(socket.mouth.distanceTo(socket.position)-20)<1e-8);
      m.remove(new Set([added.id]));
    }
  }
});
test('orientation alternatives use prospective ports and retain roll after pointer updates',()=>{
  const m=new Design();m.add('tube',[-200,0,0]);const target=placementTargets(m).find(t=>t.target.port===1);
  const pointer=flat(target.position),targets=[target];
  const a=query(m,pointer,{piece:piece('corner'),targets});
  const intended=quat([0,0,0,1]).setFromAxisAngle(vec([1,0,0]),Math.PI/2).multiply(quat(a.q)).toArray();
  const b=query(m,pointer,{piece:piece('corner',intended),targets,previous:a});
  assert(Math.abs(quat(b.q).dot(quat(intended)))>1-1e-8);
  const c=query(m,{x:pointer.x+1,y:pointer.y},{piece:piece('corner',intended),targets,previous:b});assert.deepEqual(c.q,b.q);
  const flip=quat([0,0,0,1]).setFromAxisAngle(vec([0,1,0]),Math.PI).toArray();
  const d=query(m,pointer,{piece:piece('tee',flip),targets});assert(Math.abs(quat(d.q).dot(quat(flip)))>1-1e-8);
});
test('overlaps prefer visibility, depth and deterministic endpoint order',()=>{
  const m=new Design();const back=m.add('cap',[0,0,-200]),front=m.add('cap',[0,0,0]);
  assert.equal(query(m,{x:25,y:0}).target.id,front.id);
  assert.equal(query(m,{x:25,y:0},{visible:t=>t.target.id===back.id}).target.id,back.id);
  const targets=placementTargets(m);targets[1].position.copy(targets[0].position);
  const opts={targets,visible:()=>true};assert.deepEqual(query(m,{x:25,y:0},opts),query(m,{x:25,y:0},{...opts,targets:targets.toReversed()}));
});
test('front, side, top, perspective and zoom project in CSS pixels; reject behind/clipped/nonfinite',()=>{
  const rect={left:10,top:20,width:800,height:600};
  for(const Camera of [PerspectiveCamera,OrthographicCamera])for(const direction of [[0,0,1],[1,0,0],[0,1,0],[1,1,1]])for(const zoom of [.5,3]){
    const camera=Camera===PerspectiveCamera?new Camera(42,4/3,1,10000):new Camera(-400,400,300,-300,1,10000);
    camera.position.copy(vec(direction).normalize().multiplyScalar(1000));if(direction[1]===1&&direction[0]===0)camera.up.set(0,0,-1);camera.lookAt(0,0,0);camera.zoom=zoom;camera.updateProjectionMatrix();camera.updateMatrixWorld(true);
    const project=p=>projectPort(p,camera,rect),m=new Design();m.add('cap',[-25,0,0]);
    assert.equal(project(vec([NaN,0,0])),null);assert.equal(project(camera.position.clone().multiplyScalar(2)),null);
    const target=project(vec([0,0,0]));assert(Math.abs(target.x-410)<1e-8);assert(Math.abs(target.y-320)<1e-8);
    assert(query(m,target,{project}));assert.equal(query(m,{x:target.x+65,y:target.y},{project}),null);
  }
});

test('nonfinite prospective transforms never produce a candidate',()=>{
  const m=new Design();m.add('cap');
  assert.equal(query(m,{x:25,y:0},{piece:piece('tube',[NaN,0,0,1])}),null);
});
