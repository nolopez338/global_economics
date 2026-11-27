import test from 'node:test';
import assert from 'node:assert/strict';
import {Design,CATALOG,localPorts,port,vec,quat,validate} from '../assets/js/pvc-model.mjs';
import {PerspectiveCamera,OrthographicCamera} from '../assets/vendor/three-0.170.0/three.module.js';
import {SNAP_PIXELS,SWITCH_MARGIN,placementTargets,alignPlacement,choosePlacement,projectPort} from '../assets/js/pvc-placement.mjs';
const piece=(type='tube',q=[0,0,0,1])=>({id:'preview',type,p:[0,0,0],q,length:400});
const flat=p=>({x:p.x,y:p.y,depth:100-p.z});
const query=(m,pointer,extra={})=>choosePlacement({piece:piece(),targets:placementTargets(m),pointer,project:flat,...extra});
test('192 CSS pixel acquisition includes the boundary and releases strictly outside it',()=>{
  assert.equal(SNAP_PIXELS,192);assert.equal(SWITCH_MARGIN,12);
  const m=new Design();m.add('coupling',[-25,0,0]);
  for(const distance of [0,64.01,128,191.99,192]){
    const preview=query(m,{x:distance,y:0});assert(preview,`No acquisition at ${distance}px`);
    assert(Math.abs(preview.distance-distance)<1e-8);
  }
  const previous=query(m,{x:192,y:0});
  for(const pointer of [{x:192.001,y:0},{x:0,y:-192.001},{x:136,y:136}])
    assert.equal(query(m,pointer,{previous}),null,'Hysteresis extended the release radius');
  assert(query(m,{x:115.2,y:153.6}),'Diagonal point on the acquisition boundary');
});

test('hysteresis retains competitors within 12px but lets pointer movement switch naturally',()=>{
  const m=new Design(),a=m.add('coupling',[0,0,0]),b=m.add('coupling',[40,0,0]);
  const initial=query(m,{x:25,y:0});assert.equal(initial.target.id,a.id);
  assert.equal(query(m,{x:48,y:0},{previous:initial}).target.id,a.id);
  assert.equal(query(m,{x:55,y:0},{previous:initial}).target.id,b.id);
  assert.equal(query(m,{x:51,y:0},{previous:initial}).target.id,a.id,'12px advantage must retain target');
  assert.equal(query(m,{x:51.01,y:0},{previous:initial}).target.id,b.id,'Larger advantage must switch target');
  assert.equal(query(m,{x:65,y:0},{previous:initial}).target.id,b.id);
  const switched=query(m,{x:65,y:0},{previous:initial});
  assert.equal(query(m,{x:42,y:0},{previous:switched}).target.id,b.id,'Reverse hysteresis');
  assert.equal(query(m,{x:35,y:0},{previous:switched}).target.id,a.id,'Reverse switch');
});

test('close targets cap hysteresis by separation, so either port remains reachable',()=>{
  for(const separation of [.1,2,8,20]){
    const m=new Design(),a=m.add('coupling',[-25,0,0]),b=m.add('coupling',[-25+separation,0,0]);
    const previous=query(m,{x:0,y:0});assert.equal(previous.target.id,a.id);
    const retained=query(m,{x:separation*.6,y:0},{previous});
    assert.equal(retained.target.id,a.id,`Unstable competition at ${separation}px`);
    const switched=query(m,{x:separation,y:0},{previous:retained});
    assert.equal(switched.target.id,b.id,`Cannot reach the second port at ${separation}px`);
    assert.equal(query(m,{x:0,y:0},{previous:switched}).target.id,a.id);
  }
});
test('occupied and incompatible targets excluded, query does not mutate model',()=>{
  const m=new Design(),cap=m.add('coupling'),tube=m.add('tube');m.connect({id:tube.id,port:0},{id:cap.id,port:0});
  const before=m.data();assert.equal(query(m,{x:0,y:0}).target.port,1);assert.deepEqual(m.data(),before);
  const endpoints=placementTargets(m);
  assert(!endpoints.some(e=>e.target.id===cap.id&&e.target.port===0||e.target.id===tube.id&&e.target.port===0));
  const tubeTargets=endpoints.filter(e=>e.type==='tube');
  assert.equal(query(m,flat(tubeTargets[0].position),{targets:tubeTargets}),null,'A tube cannot target a tube end');
  assert(query(m,flat(tubeTargets[0].position),{piece:piece('tee'),targets:tubeTargets}),'Free compatible tube end excluded');
  assert.deepEqual(m.data(),before);
});
test('every fitting port aligns at the insertion stop; preview commits without realignment',()=>{
  const rotations=[[0,0,0,1],[0,.7071067811865475,0,.7071067811865476],
    quat([0,0,0,1]).setFromAxisAngle(vec([1,2,3]).normalize(),2.4).toArray(),
    quat([0,0,0,1]).setFromAxisAngle(vec([0,0,1]),Math.PI).toArray()];
  for(const type of Object.keys(CATALOG).filter(type=>!CATALOG[type].reference))for(const q of rotations){
    const m=new Design(),target=m.add(type==='tube'?'tee':'tube',[0,0,0]);
    for(const endpoint of placementTargets(m)){
      const before=m.data(),pointer=flat(endpoint.position);
      const preview=query(m,pointer,{piece:piece(type,q),targets:[endpoint]});assert(preview,type);
      assert.deepEqual(m.data(),before);
      const shifted=query(m,pointer,{piece:{...piece(type,q),p:[123.456789,987.654321,-113.257]},targets:[endpoint]});
      assert.deepEqual(shifted.p,preview.p,'Aligned position depends on free-plane coordinates');
      assert.deepEqual(shifted.q,preview.q);
      const wanted=endpoint.direction.clone().negate(),nearest=Math.min(...localPorts(piece(type,q)).map((_,i)=>
        Math.acos(Math.max(-1,Math.min(1,port(piece(type,q),i).direction.dot(wanted))))));
      assert(Math.abs(quat(preview.q).angleTo(quat(q))-nearest)<1e-7,'Did not choose the closest aligned orientation: '+type);
      const added=m.add(type,preview.p,400,preview.q);m.connect({id:added.id,port:preview.source},preview.target,false);validate(m.data());
      assert.deepEqual(added.p,preview.p);assert.deepEqual(added.q,preview.q);
      const a=port(added,preview.source),b=port(target,endpoint.target.port);
      assert(a.position.distanceTo(b.position)<1e-8);assert(a.direction.dot(b.direction)<-.999999);
      const socket=a.type==='socket'?a:b;assert(Math.abs(socket.mouth.distanceTo(socket.position)-20)<1e-8);
      m.remove(new Set([added.id]));
    }
  }
});

test('every applicable source port can be selected, including ports initially facing away',()=>{
  for(const type of Object.keys(CATALOG)){
    const m=new Design();m.add(type==='tube'?'coupling':'tube',[0,0,0]);
    const target=placementTargets(m)[0],wanted=target.direction.clone().negate();
    for(const [source,definition] of localPorts(piece(type)).entries()){
      const facing=quat([0,0,0,1]).setFromUnitVectors(vec(definition.direction),wanted);
      const roll=quat([0,0,0,1]).setFromAxisAngle(wanted,.731).multiply(facing).toArray();
      const preview=query(m,flat(target.position),{piece:piece(type,roll),targets:[target]});
      assert.equal(preview.source,source,`${type}: source port ${source} was not evaluated`);
      assert(Math.abs(quat(preview.q).dot(quat(roll)))>1-1e-12,'An already aligned roll was changed');
      const opposite=quat([0,0,0,1]).setFromUnitVectors(vec(definition.direction),target.direction).toArray();
      const aligned=alignPlacement(piece(type,opposite),source,target);assert(aligned,`${type}: cannot turn a port through 180°`);
      const actual=port({...piece(type),p:aligned.p,q:aligned.q},source);
      assert(actual.position.distanceTo(target.position)<1e-8&&actual.direction.dot(target.direction)<-1+1e-10);
      assert(Math.abs(quat(aligned.q).length()-1)<1e-12);
      assert.deepEqual(alignPlacement(piece(type,opposite),source,target),aligned,'Antiparallel tie was not deterministic');
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
  let previous=b;
  for(let i=0;i<100;i++){
    const next=query(m,{x:pointer.x+Math.sin(i)*40,y:pointer.y+Math.cos(i)*40},{piece:{...piece('corner',intended),p:[i*20,-i,i*13]},targets,previous});
    assert.deepEqual(next.q,b.q,'Repeated alignment drifted or discarded roll');
    assert.equal(next.source,b.source);previous=next;
  }
});

test('source orientation ties do not depend on free-plane position or target projection',()=>{
  const m=new Design();m.add('tube',[-200,0,0]);const targets=[placementTargets(m).find(t=>t.target.port===1)];
  const intended=quat([0,0,0,1]).setFromAxisAngle(vec([0,1,0]),Math.PI/4).toArray();
  const baseline=query(m,{x:0,y:0},{piece:piece('elbow90',intended),targets});
  for(const p of [[1000,0,0],[-1000,900,1000],[0,-100,0]]){
    const other=query(m,{x:0,y:0},{piece:{...piece('elbow90',intended),p},targets});
    assert.equal(other.source,baseline.source);assert.deepEqual(other.q,baseline.q);assert.deepEqual(other.p,baseline.p);
  }
});
test('overlaps prefer visibility, depth and deterministic endpoint order',()=>{
  const m=new Design();const back=m.add('coupling',[0,0,-200]),front=m.add('coupling',[0,0,0]);
  assert.equal(query(m,{x:25,y:0}).target.id,front.id);
  assert.equal(query(m,{x:25,y:0},{visible:t=>t.target.id===back.id}).target.id,back.id);
  const backChoice=query(m,{x:25,y:0},{visible:t=>t.target.id===back.id});
  assert.equal(query(m,{x:25,y:0},{previous:backChoice}).target.id,front.id,'Coincident target hysteresis hid the frontmost port');
  const targets=placementTargets(m);targets[1].position.copy(targets[0].position);
  const opts={targets,visible:()=>true};assert.deepEqual(query(m,{x:25,y:0},opts),query(m,{x:25,y:0},{...opts,targets:targets.toReversed()}));
  const first=query(m,{x:25,y:0},opts),other=targets.find(t=>t.target.id!==first.target.id);
  assert.deepEqual(query(m,{x:25,y:0},{...opts,previous:{target:other.target,source:0}}),first,'Coincident target tie retained a worse endpoint');
  const nearer=placementTargets(m);nearer[0].position.x=27;
  assert.equal(query(m,{x:27,y:0},{targets:nearer,visible:t=>t.target.id===front.id}).target.id,back.id,'Visibility outranked a closer target');
});
test('front, side, top, perspective and zoom project in CSS pixels; reject behind/clipped/nonfinite',()=>{
  const rect={left:10,top:20,width:800,height:600};
  for(const Camera of [PerspectiveCamera,OrthographicCamera])for(const direction of [[0,0,1],[1,0,0],[0,1,0],[1,1,1]])for(const zoom of [.5,3]){
    const camera=Camera===PerspectiveCamera?new Camera(42,4/3,1,10000):new Camera(-400,400,300,-300,1,10000);
    camera.position.copy(vec(direction).normalize().multiplyScalar(1000));if(direction[1]===1&&direction[0]===0)camera.up.set(0,0,-1);camera.lookAt(0,0,0);camera.zoom=zoom;camera.updateProjectionMatrix();camera.updateMatrixWorld(true);
    const project=p=>projectPort(p,camera,rect),m=new Design();m.add('coupling',[-25,0,0]);
    assert.equal(project(vec([NaN,0,0])),null);assert.equal(project(camera.position.clone().multiplyScalar(2)),null);
    const target=project(vec([0,0,0]));assert(Math.abs(target.x-410)<1e-8);assert(Math.abs(target.y-320)<1e-8);
    for(const distance of [64.1,128,191.9,192])assert(query(m,{x:target.x+distance,y:target.y},{project}),`Missing ${distance}px acquisition at zoom ${zoom}`);
    const previous=query(m,target,{project});
    assert.equal(query(m,{x:target.x+192.01,y:target.y},{project,previous}),null);
    // A renderer's drawing buffer may be scaled by DPR; only its CSS rectangle is used.
    for(const dpr of [1,1.25,2,3]){
      const cssRect={...rect,drawingBufferWidth:rect.width*dpr,drawingBufferHeight:rect.height*dpr};
      assert.deepEqual(projectPort(vec([0,0,0]),camera,cssRect),target);
    }
  }
});

test('nonfinite prospective transforms never produce a candidate',()=>{
  const m=new Design();m.add('coupling');
  assert.equal(query(m,{x:25,y:0},{piece:piece('tube',[NaN,0,0,1])}),null);
  assert.equal(query(m,{x:25,y:0},{piece:piece('tube',[Infinity,0,0,1])}),null);
  assert.equal(query(m,{x:25,y:0},{piece:piece('tube',[0,0,0,0])}),null);
  for(const pointer of [{x:NaN,y:0},{x:0,y:Infinity}])assert.equal(query(m,pointer),null);
  for(const project of [()=>({x:NaN,y:0,depth:1}),()=>({x:25,y:0,depth:Infinity})])
    assert.equal(query(m,{x:25,y:0},{project}),null);
});
