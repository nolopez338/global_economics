import test from 'node:test';
import assert from 'node:assert/strict';
import {TEMPLATES,buildTemplate} from '../assets/js/pvc-templates.mjs';
import {validate,port,vec,clone} from '../assets/js/pvc-model.mjs';
import {geometry,dispose} from '../assets/js/pvc-geometry.mjs';
import {Box3,Group} from '../assets/vendor/three-0.170.0/three.module.js';

test('exactly ten uniquely named templates, including Empty',()=>{
  assert.equal(TEMPLATES.length,10);assert.equal(new Set(TEMPLATES.map(t=>t.id)).size,10);
  assert.equal(TEMPLATES[0].name,'Empty');assert.equal(buildTemplate('empty').pieces.length,0);
  assert.throws(()=>buildTemplate('unknown'));
});
for(const t of TEMPLATES.slice(1))test(`${t.name}: seated connected assembly, round trip and materials`,()=>{
  assert(t.description&&t.dimensions);const m=buildTemplate(t.id),data=m.data();
  assert.equal(m.connected([m.pieces[0].id]).size,m.pieces.length);
  assert.equal(new Set([...m.pieces,...m.connections].map(p=>p.id)).size,m.pieces.length+m.connections.length);
  const used=new Set();for(const c of m.connections){
    for(const e of [c.a,c.b]){const key=e.id+':'+e.port;assert(!used.has(key));used.add(key);}
    const a=port(m.get(c.a.id),c.a.port),b=port(m.get(c.b.id),c.b.port);
    assert(a.position.distanceTo(b.position)<1e-8);assert(Math.abs(a.direction.dot(b.direction)+1)<1e-8);assert.notEqual(a.type,b.type);
  }
  for(const p of m.pieces){if(p.type==='tube'){
    assert(p.length>=80&&p.length<=3000);assert.equal(p.length,Math.round(p.length));
    assert(used.has(p.id+':0')&&used.has(p.id+':1'));
    const d=port(p,1).direction.toArray().filter(v=>Math.abs(v)>1e-7);
    if(d.length===1)assert.equal(p.length%100,0,'axial cuts use 100 mm increments');
  }}
  const restored=validate(JSON.parse(JSON.stringify(data)));assert.deepEqual(restored.data(),data);assert.deepEqual(restored.materials(),m.materials());
  assert.equal(m.materials().rows.reduce((n,r)=>n+r.count,0),m.pieces.length);
  assert.equal(m.materials().total,m.pieces.filter(p=>p.type==='tube').reduce((n,p)=>n+p.length,0));
  // Copy and rigid editing retain every configured socket and joint.
  const copy=m.copy(new Set(m.pieces.map(p=>p.id))),fresh=m.paste(copy);m.transform(fresh,undefined,undefined,vec([3000,0,0]));validate(m.data());
});
test('window front opening, sill, rear / side bracing and physical bounds',()=>{
  const m=buildTemplate('window'),group=new Group();
  for(const p of m.pieces){const g=geometry(p);g.position.fromArray(p.p);g.quaternion.fromArray(p.q);group.add(g);}
  group.updateMatrixWorld(true);const box=new Box3().setFromObject(group,true);console.log('Window full rendered bounds mm:',box.min.toArray(),box.max.toArray(),box.getSize(vec([0,0,0])).toArray());
  const frontTubes=m.pieces.filter(p=>p.type==='tube'&&Math.abs(p.p[2]-175)<1e-8);
  for(const p of frontTubes){const ends=[port(p,0).position,port(p,1).position];assert(!ends.some(v=>v.y>1142&&v.y<2200&&Math.abs(v.x)<729));}
  assert(frontTubes.some(p=>Math.abs(p.p[1]-1121)<1e-8));
  assert(m.pieces.some(p=>p.type==='tube'&&p.p[2]>175));assert(m.pieces.some(p=>p.type==='tube'&&p.p[2]<-175));dispose(group);
});
test('custom junction import rejects malformed, colliding and off-axis sockets',()=>{
  const data=buildTemplate('window').data(),p=data.pieces.find(p=>p.type==='multiway');
  for(const mutate of [p=>p.sockets=[],p=>p.sockets[1]=clone(p.sockets[0]),p=>p.sockets[0].insertion=0,p=>p.sockets[0].direction=[2,0,0],p=>p.sockets[0].position=[999,0,0]]){const d=clone(data);mutate(d.pieces.find(q=>q.id===p.id));assert.throws(()=>validate(d));}
});

function segmentDistance(p1,q1,p2,q2){
  const d1=q1.clone().sub(p1),d2=q2.clone().sub(p2),r=p1.clone().sub(p2),a=d1.dot(d1),e=d2.dot(d2),b=d1.dot(d2),c=d1.dot(r),f=d2.dot(r),denom=a*e-b*b;
  const clamp=x=>Math.max(0,Math.min(1,x));let s=denom?clamp((b*f-c*e)/denom):0,t=(b*s+f)/e;
  if(t<0){t=0;s=clamp(-c/a);}else if(t>1){t=1;s=clamp((b-c)/a);}
  return p1.clone().addScaledVector(d1,s).distanceTo(p2.clone().addScaledVector(d2,t));
}
for(const template of TEMPLATES.slice(1))test(`${template.id}: unrelated tubes do not intersect`,()=>{
  const m=buildTemplate(template.id),tubes=m.pieces.filter(p=>p.type==='tube');
  const neighbors=p=>new Set(m.connections.filter(c=>c.a.id===p.id||c.b.id===p.id).map(c=>c.a.id===p.id?c.b.id:c.a.id));
  for(let i=0;i<tubes.length;i++)for(let j=0;j<i;j++){
    const a=tubes[i],b=tubes[j],na=neighbors(a),nb=neighbors(b);if([...na].some(id=>nb.has(id)))continue;
    assert(segmentDistance(port(a,0).position,port(a,1).position,port(b,0).position,port(b,1).position)>32,`Unintended intersection ${a.id} / ${b.id}`);
  }
});
