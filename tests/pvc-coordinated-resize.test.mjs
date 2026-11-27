import test from 'node:test';
import assert from 'node:assert/strict';
import {Design,rectangle,validate,port,vec,quat,PARALLEL_TOLERANCE} from '../assets/js/pvc-model.mjs';
import {buildTemplate} from '../assets/js/pvc-templates.mjs';
import {Quaternion} from '../assets/vendor/three-0.170.0/three.module.js';

const leftBay=m=>m.pieces.filter(p=>p.type==='tube'&&Math.abs(p.p[0]+350)<1e-6);
const ids=ps=>new Set(ps.map(p=>p.id));
const near=(a,b)=>assert.ok(vec(a).distanceTo(vec(b))<1e-7,`${a} != ${b}`);
function intact(m,before,selected,delta){
  validate(m.data());assert.deepEqual(m.connections,before.connections);
  for(const p of m.pieces){const old=before.pieces.find(o=>o.id===p.id);assert.deepEqual(p.q,old.q);if(p.type==='tube')assert.equal(p.length,old.length+(selected.has(p.id)?delta:0));}
  for(const c of m.connections){const a=port(m.get(c.a.id),c.a.port),b=port(m.get(c.b.id),c.b.port);assert.ok(a.position.distanceTo(b.position)<1e-7);assert.ok(a.direction.dot(b.direction)<-.999999);const socket=a.type==='socket'?a:b,tube=a.type==='tube'?a:b;assert.ok(Math.abs(socket.mouth.distanceTo(tube.position)-20)<1e-7);}
}
test('Template 7: four left-bay rails solve together even though each single cut is locked',()=>{
  for(const delta of [100,-100,-570,2350]){
    const m=buildTemplate('bridge'),tubes=leftBay(m),selection=ids(tubes),before=m.data();assert.equal(tubes.length,4);
    assert.ok(tubes.every(p=>m.lengthPlan(p.id).locked));assert.equal(m.coordinatedLengthPlan(selection).locked,false);
    // Prove the coordinated solver never calls the single-tube operation.
    m.resize=()=>{throw Error('single resize invoked');};m.resizeTogether(selection,delta);intact(m,before,selection,delta);
    for(const p of m.pieces){const old=before.pieces.find(o=>o.id===p.id);near(p.p,vec(old.p).add(vec([selection.has(p.id)?delta/2:old.p[0]>-699?delta:0,0,0])).toArray());}
    assert.equal(m.materials().total,before.pieces.filter(p=>p.type==='tube').reduce((s,p)=>s+p.length,0)+4*delta);
  }
});
test('parallelism alone is insufficient: an unselected closed path blocks the entire atomic resize',()=>{
  const m=buildTemplate('bridge'),selection=ids(leftBay(m).slice(0,3)),before=m.data();
  assert.match(m.coordinatedLengthPlan(selection).reason,/unselected rigid section/);assert.throws(()=>m.resizeTogether(selection,100),/unselected/);assert.deepEqual(m.data(),before);
});
test('conflicting paths with two selected cuts versus one are rejected without distortion',()=>{
  const m=rectangle(),old=m.pieces.find(p=>p.type==='tube'),axis=vec([1,0,0]).applyQuaternion(quat(old.q)),joints=m.connections.filter(c=>c.a.id===old.id||c.b.id===old.id);
  const opposite=m.pieces.find(p=>p.type==='tube'&&p.id!==old.id&&Math.abs(vec([1,0,0]).applyQuaternion(quat(p.q)).dot(axis))>.999);
  m.remove(new Set([old.id]));
  const coupling=m.add('coupling',old.p,400,old.q),short=[];
  for(const end of [0,1]){
    const sign=end===0?-1:1,t=m.add('tube',vec(old.p).addScaledVector(axis,sign*(old.length+50)/4).toArray(),(old.length-50)/2,old.q);short.push(t);
    m.connect({id:t.id,port:1-end},{id:coupling.id,port:end},false);
    const joint=joints.find(c=>[c.a,c.b].some(e=>e.id===old.id&&e.port===end)),other=joint.a.id===old.id?joint.b:joint.a;
    m.connect({id:t.id,port:end},other,false);
  }
  const selection=ids([...short,opposite]),before=m.data();assert.match(m.coordinatedLengthPlan(selection).reason,/Conflicting resize paths/);assert.throws(()=>m.resizeTogether(selection,100),/Conflicting/);assert.deepEqual(m.data(),before);
});
test('reversed endpoint directions and global rotation preserve constraints and anchoring',()=>{
  const original=buildTemplate('bridge'),selection=ids(leftBay(original));
  for(const p of leftBay(original).slice(0,2)){p.q=quat(p.q).multiply(new Quaternion().setFromAxisAngle(vec([0,1,0]),Math.PI)).toArray();for(const c of original.connections)for(const e of [c.a,c.b])if(e.id===p.id)e.port=1-e.port;}
  validate(original.data());const normal=new Design(original.data()),reordered=new Design(original.data());normal.resizeTogether(selection,125);reordered.resizeTogether([...selection].reverse(),125);assert.deepEqual(normal.data(),reordered.data());
  original.transform(new Set(original.pieces.map(p=>p.id)),new Quaternion().setFromAxisAngle(vec([1,2,3]).normalize(),.73));const before=original.data();original.resizeTogether(selection,-50);intact(original,before,selection,-50);
});
test('unequal starting lengths get an equal absolute adjustment, connected and free',()=>{
  for(const connected of [false,true]){const m=new Design(),a=m.add('tube',[0,0,0],500),b=m.add('tube',[0,0,100],700),selection=ids([a,b]);
    if(connected){const tee=m.add('tee');m.connect({id:a.id,port:0},{id:tee.id,port:0});m.connect({id:b.id,port:0},{id:tee.id,port:1});}
    const before=m.data();m.resizeTogether(selection,100);assert.deepEqual([m.get(a.id).length,m.get(b.id).length],[600,800]);intact(m,before,selection,100);
    if(!connected){near(m.get(a.id).p,a.p);near(m.get(b.id).p,b.p);}
  }
});
test('shared limits intersect every starting cut; invalid adjustments are atomic',()=>{
  const m=new Design(),a=m.add('tube',[0,0,0],100),b=m.add('tube',[0,0,100],2900),selection=ids([a,b]);
  const plan=m.coordinatedLengthPlan(selection);assert.equal(plan.minDelta,-20);assert.equal(plan.maxDelta,100);
  for(const delta of [NaN,Infinity,-20.001,100.001]){const before=m.data();assert.throws(()=>m.resizeTogether(selection,delta),/Shared adjustment/);assert.deepEqual(m.data(),before);}
  for(const delta of [-20,100]){const copy=new Design(m.data());copy.resizeTogether(selection,delta);intact(copy,m.data(),selection,delta);}
  const exhausted=new Design();exhausted.add('tube',[0,0,0],80);exhausted.add('tube',[0,0,100],3000);assert.match(exhausted.coordinatedLengthPlan(ids(exhausted.pieces)).reason,/no nonzero shared adjustment/);
});
test('mixed and nonparallel selections explain all selected pieces; tolerance accepts near parallel axes',()=>{
  const m=rectangle(),tubes=m.pieces.filter(p=>p.type==='tube'),fitting=m.pieces.find(p=>p.type!=='tube');
  assert.match(m.coordinatedLengthPlan(ids([tubes[0],fitting])).reason,/includes fittings/);
  assert.match(m.coordinatedLengthPlan(ids(tubes.slice(0,2))).reason,/not parallel in world space/);
  const free=new Design(),a=free.add('tube'),b=free.add('tube');
  b.q=new Quaternion().setFromAxisAngle(vec([0,1,0]),PARALLEL_TOLERANCE/2).toArray();assert.equal(free.coordinatedLengthPlan(ids([a,b])).locked,false);
  b.q=new Quaternion().setFromAxisAngle(vec([0,1,0]),PARALLEL_TOLERANCE*2).toArray();assert.equal(free.coordinatedLengthPlan(ids([a,b])).locked,true);
});
test('snapshot-based previews retain exact starting geometry and fractional cut differences',()=>{
  const m=new Design();m.add('tube',[0,0,0],500.123);m.add('tube',[0,0,100],700.456);const before=m.data(),selection=ids(m.pieces);
  for(const delta of [123.456,-200.001,1.234,0]){const preview=new Design(before);preview.resizeTogether(selection,delta);intact(preview,before,selection,delta);if(!delta)assert.deepEqual(preview.data(),before);}
});
