import test from 'node:test';
import assert from 'node:assert/strict';
import {Design,validate,rectangle,port,vec,quat,CATALOG} from '../assets/js/pvc-model.mjs';
import {Quaternion} from '../assets/vendor/three-0.170.0/three.module.js';
const end=(p,i)=>({id:p.id,port:i});
function valid(m){validate(m.data());}
function near(a,b){assert.ok(vec(a).distanceTo(vec(b))<.00001,`${a} != ${b}`);}
test('tube + elbow seat at socket stop and move rigidly, then detach independently',()=>{
  const m=new Design(),t=m.add('tube'),e=m.add('elbow90',[240,60,0]);const c=m.connect(end(t,1),end(e,0));
  near(port(t,1).position.toArray(),port(e,0).position.toArray());assert.equal(port(t,1).position.distanceTo(port(e,0).mouth),20);valid(m);
  const old=[...e.p];m.transform(m.connected([t.id]),undefined,undefined,vec([50,10,30]));near(e.p,vec(old).add(vec([50,10,30])).toArray());valid(m);
  m.disconnect(c.id);const fixed=[...e.p];m.transform(m.connected([t.id]),undefined,undefined,vec([100,0,0]));near(e.p,fixed);valid(m);
});
test('free tube resizes about centre, each single attached end stays fixed',()=>{
  const free=new Design(),f=free.add('tube');free.resize(f.id,600);near(f.p,[0,60,0]);
  for(const i of [0,1]){const m=new Design(),t=m.add('tube'),e=m.add('coupling');m.connect(end(e,0),end(t,i));const point=port(t,i).position.toArray(),fixed=[...e.p];m.resize(t.id,700);near(port(t,i).position.toArray(),point);near(e.p,fixed);valid(m);}
});
test('two-ended tube translates only the free branch and retains every joint',()=>{
  const m=new Design(),t=m.add('tube'),a=m.add('tee'),b=m.add('elbow90');m.connect(end(a,1),end(t,0));m.connect(end(b,0),end(t,1));
  const fixed=[...a.p],before=[...b.p],axis=vec([1,0,0]).applyQuaternion(quat(t.q));m.resize(t.id,650);near(a.p,fixed);near(b.p,vec(before).addScaledVector(axis,250).toArray());assert.equal(m.connections.length,2);valid(m);
});
test('closed rectangular frame locks length; removing one edge permits adjustment',()=>{
  const m=rectangle(),t=m.pieces.find(p=>p.type==='tube');assert.equal(m.connections.length,8);valid(m);assert.equal(m.lengthPlan(t.id).locked,true);assert.throws(()=>m.resize(t.id,600),/Closed frame/);
  const c=m.connections.find(c=>c.a.id===t.id||c.b.id===t.id);m.disconnect(c.id);assert.equal(m.connected([t.id]).size,8);m.resize(t.id,650);valid(m);
});
test('inconsistent loop closure is rejected without moving geometry',()=>{
  const m=rectangle(),c=m.connections.pop();const t=m.get(c.a.id);m.resize(t.id,t.length+25);const before=JSON.stringify(m.data());assert.throws(()=>m.connect(c.a,c.b),/distort/);assert.equal(JSON.stringify(m.data()),before);
});
test('copy/paste preserves only internal joints, relative transforms and fresh IDs',()=>{
  const m=rectangle(),old=new Set(m.pieces.map(p=>p.id)),all=m.copy(old),fresh=m.paste(all);assert.equal(fresh.size,8);assert.equal(m.connections.length,16);assert.ok([...fresh].every(id=>!old.has(id)));valid(m);
  const tube=m.pieces.find(p=>p.type==='tube'),partial=m.copy(new Set([tube.id]));assert.equal(partial.connections.length,0);const copied=m.get([...m.paste(partial)][0]);assert.equal(copied.length,tube.length);near(copied.p,vec(tube.p).add(vec([80,0,80])).toArray());valid(m);
});
test('compatibility, occupied ports, self joints and impossible connections are rejected',()=>{
  const m=new Design(),a=m.add('tube'),b=m.add('tube'),e=m.add('elbow90');assert.throws(()=>m.connect(end(a,0),end(b,0)),/tube end/);assert.throws(()=>m.connect(end(a,0),end(a,1)),/itself/);m.connect(end(a,0),end(e,0));assert.throws(()=>m.connect(end(b,0),end(e,0)),/occupied/);valid(m);
});
test('rotated assemblies retain constraints and length-edit axes',()=>{
  const m=new Design(),t=m.add('tube'),a=m.add('coupling'),b=m.add('corner');m.connect(end(a,0),end(t,0));m.connect(end(b,0),end(t,1));m.transform(m.connected([t.id]),new Quaternion().setFromAxisAngle(vec([0,0,1]),Math.PI/2),vec([10,30,0]));m.resize(t.id,900);valid(m);
});
test('JSON round trip retains geometry, graph and materials',()=>{
  const m=rectangle(),round=validate(JSON.parse(JSON.stringify(m.data())));assert.deepEqual(round.data(),m.data());assert.deepEqual(round.summary(),m.summary());assert.equal(round.summary().total,1800);assert.deepEqual(round.summary().rows,[['90° elbow',4],['Tube · 550 mm',2],['Tube · 350 mm',2]]);
});
test('imports reject corrupt values, duplicate IDs, occupied ports, mismatches and malformed references',()=>{
  for(const mutate of [d=>d.version=2,d=>d.radius=20,d=>d.pieces[0].p[0]=null,d=>d.pieces[0].q=[0,0,0,0],d=>d.pieces[1].id=d.pieces[0].id,d=>d.connections[0].b.id='missing',d=>d.connections[0].b.port=1.5,d=>d.connections[0].b.port=99,d=>d.pieces.find(p=>p.type==='tube').length=1,d=>d.pieces[0].p[0]+=10,d=>d.connections.push({...d.connections[0],id:'unique'}),d=>d.pieces[0].type='__proto__']){const d=rectangle().data();mutate(d);assert.throws(()=>validate(d));}
});
test('every fitting has explicit normalized socket definitions',()=>{for(const [type,def] of Object.entries(CATALOG)){if(type==='tube'||def.reference)continue;assert.ok(def.ports.length);for(const p of def.ports){assert.equal(p.type,'socket');assert.equal(p.insertion,20);assert.ok(Math.abs(vec(p.direction).length()-1)<1e-10);}}});

test('materials group exact cuts and fitting types, with decimal totals',()=>{
  const m=new Design();m.add('tube',[0,0,0],123.456);m.add('tube',[0,0,0],123.4560001);
  m.add('tube',[0,0,0],650);m.add('tube',[0,0,0],650);m.add('tee');m.add('tee');
  assert.deepEqual(m.materials(),{rows:[{type:'tube',length:123.456,count:1},{type:'tube',length:123.4560001,count:1},{type:'tube',length:650,count:2},{type:'tee',count:2}],total:1546.9120001,count:6,references:0});
  assert.deepEqual(new Design().materials(),{rows:[],total:0,count:0,references:0});
});
