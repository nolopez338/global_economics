import test from 'node:test';
import assert from 'node:assert/strict';
import {Design,port,vec,quat,rectangle} from '../assets/js/pvc-model.mjs';
const end=(p,port)=>({id:p.id,port});
test('bridge seats both ends 20 mm inside mouths; JSON retains all geometry',()=>{
  const m=new Design(),a=m.add('tee',[0,100,0]),b=m.add('corner',[500,170,90]);
  const before=structuredClone(a),t=m.connectFittings(end(a,1),end(b,0),[100,10]);
  assert.deepEqual(m.get(a.id),before);assert.equal(t.length,500);
  assert.equal(m.connections.length,2);assert.equal(m.pieces.length,3);
  for(const c of m.connections){const x=port(m.get(c.a.id),c.a.port),y=port(m.get(c.b.id),c.b.port);assert(x.position.distanceTo(y.position)<1e-8);assert(Math.abs(y.mouth.distanceTo(x.position)-20)<1e-8);}
  assert.deepEqual(new Design(JSON.parse(JSON.stringify(m.data()))).data(),m.data());
});
test('larger second assembly fixed; smaller moves rigidly; equal areas fix first',()=>{
  for(const areas of [[1,10],[10,1],[10,10],[10,10+1e-12]]){
    const m=new Design(),a=m.add('coupling',[0,100,0]),b=m.add('coupling',[500,170,90]);
    const t=m.add('tube');m.connect(end(t,1),end(a,0));
    const before=m.data(),distance=vec(a.p).distanceTo(vec(t.p)),rel=quat(a.q).invert().multiply(quat(t.q));
    m.connectFittings(end(a,1),end(b,0),areas);
    const fixed=areas[0]>=areas[1]-1e-9?a:b;
    assert.deepEqual(m.get(fixed.id),before.pieces.find(p=>p.id===fixed.id));
    assert(Math.abs(vec(m.get(a.id).p).distanceTo(vec(m.get(t.id).p))-distance)<1e-8);
    assert(Math.abs(quat(m.get(a.id).q).invert().multiply(quat(m.get(t.id).q)).dot(rel))>1-1e-10);
    m.data();
  }
});
test('occupied, same-piece, incompatible and unsupported bridge lengths reject atomically',()=>{
  for(const separation of [40,3100,-500]){
    const m=new Design(),a=m.add('coupling',[0,0,0]),b=m.add('coupling',[separation,30,0]);const before=m.data();
    assert.throws(()=>m.connectFittings(end(a,1),end(b,0)),/length/);assert.deepEqual(m.data(),before);
  }
  const m=new Design(),a=m.add('tee'),b=m.add('tee',[500,60,0]),t=m.add('tube');m.connect(end(t,0),end(a,0));const before=m.data();
  for(const pair of [[end(a,0),end(b,0)],[end(t,1),end(b,0)],[end(a,1),end(a,2)]]){assert.throws(()=>m.connectFittings(...pair));assert.deepEqual(m.data(),before);}
});
test('same assembly accepts exact straight closure and rejects misalignment atomically',()=>{
  const m=rectangle(),tube=m.pieces.find(p=>p.type==='tube'),joints=m.connections.filter(c=>c.a.id===tube.id||c.b.id===tube.id),ends=joints.map(c=>c.a.id===tube.id?c.b:c.a);
  m.remove(new Set([tube.id]));assert(m.connected([ends[0].id]).has(ends[1].id));
  const before=m.data();const added=m.connectFittings(...ends);assert(Math.abs(added.length-tube.length)<1e-8);m.data();
  m.remove(new Set([added.id]));const wrong={id:ends[1].id,port:1-ends[1].port};assert.throws(()=>m.connectFittings(ends[0],wrong));assert.deepEqual(m.data(),before);
});
test('detachment removes only boundary joints, preserving internal joints and transforms',()=>{
  const m=rectangle(),ids=new Set(m.pieces.slice(0,2).map(p=>p.id));ids.add(m.pieces.find(p=>p.type==='tube').id);
  const before=m.data(),expected=before.connections.filter(c=>ids.has(c.a.id)===ids.has(c.b.id));
  m.detachSelection(ids);assert.deepEqual(m.data().pieces,before.pieces);assert.deepEqual(m.connections,expected);m.data();
});

test('same-assembly noncollinear free sockets reject without distorting a closed path',()=>{
  const m=rectangle(),tube=m.pieces.find(p=>p.type==='tube'),joints=m.connections.filter(c=>c.a.id===tube.id||c.b.id===tube.id),ends=joints.map(c=>c.a.id===tube.id?c.b:c.a);
  m.remove(new Set([tube.id]));
  const corner=m.get(ends[1].id);corner.type='corner';
  for(const c of m.connections)for(const e of [c.a,c.b])if(e.id===corner.id&&e.port===1)e.port=2;
  if(ends[1].port===1)ends[1].port=2;
  const before=m.data();
  assert.throws(()=>m.connectFittings(ends[0],{id:corner.id,port:1}),/same assembly/);
  assert.deepEqual(m.data(),before);
});
test('bridge accepts exact supported cut-length limits without clamping',()=>{
  for(const length of [80,3000]){
    const m=new Design(),a=m.add('coupling',[0,0,0]),b=m.add('coupling',[length+50,90,0]);
    const tube=m.connectFittings(end(a,1),end(b,0));assert.equal(tube.length,length);m.data();
  }
});
