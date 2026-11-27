import test from 'node:test';
import assert from 'node:assert/strict';
import {TEMPLATES,buildTemplate} from '../assets/js/pvc-templates.mjs';
import {validate,port,vec} from '../assets/js/pvc-model.mjs';

test('only Empty and the floor-level layout remain; elevated templates are unavailable',()=>{
  assert.deepEqual(TEMPLATES.map(t=>t.id),['empty','ground']);
  assert.equal(buildTemplate('empty').pieces.length,0);
  for(const id of ['unknown','window','shelving','worktable','desk','clothes','shoes','plant','hamper','display'])assert.throws(()=>buildTemplate(id),/Unavailable/);
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
    assert([350,550].includes(p.length));
  }}
  const restored=validate(JSON.parse(JSON.stringify(data)));assert.deepEqual(restored.data(),data);assert.deepEqual(restored.materials(),m.materials());
  assert.equal(m.materials().rows.reduce((n,r)=>n+r.count,0),m.pieces.length);
  assert.equal(m.materials().total,m.pieces.filter(p=>p.type==='tube').reduce((n,p)=>n+p.length,0));
  // Copy and rigid editing retain fixed sockets and joint.
  const copy=m.copy(new Set(m.pieces.map(p=>p.id))),fresh=m.paste(copy);m.transform(fresh,undefined,undefined,vec([3000,0,0]));validate(m.data());
});
test('floor layout has no elevated branches and no overlapping fitting bodies',()=>{
  const m=buildTemplate('ground'),fittings=m.pieces.filter(p=>p.type!=='tube');
  for(const p of m.pieces)assert.equal(p.p[1],22);
  for(const a of fittings)for(const b of fittings)if(a!==b)assert(vec(a.p).distanceTo(vec(b.p))>90);
  assert.match(TEMPLATES[1].description,/unbraced rectangle can rack/);
});

function segmentDistance(p1,q1,p2,q2){
  const d1=q1.clone().sub(p1),d2=q2.clone().sub(p2),r=p1.clone().sub(p2),a=d1.dot(d1),e=d2.dot(d2),b=d1.dot(d2),c=d1.dot(r),f=d2.dot(r),denom=a*e-b*b;
  const clamp=x=>Math.max(0,Math.min(1,x));let s=denom?clamp((b*f-c*e)/denom):0,t=(b*s+f)/e;
  if(t<0){t=0;s=clamp(-c/a);}else if(t>1){t=1;s=clamp((b-c)/a);}
  return p1.clone().addScaledVector(d1,s).distanceTo(p2.clone().addScaledVector(d2,t));
}
for(const template of TEMPLATES.slice(1))test(`${template.id}: tube walls do not intersect`,()=>{
  const m=buildTemplate(template.id),tubes=m.pieces.filter(p=>p.type==='tube');
  for(let i=0;i<tubes.length;i++)for(let j=0;j<i;j++){
    const a=tubes[i],b=tubes[j];
    assert(segmentDistance(port(a,0).position,port(a,1).position,port(b,0).position,port(b,1).position)>32,`Unintended intersection ${a.id} / ${b.id}`);
  }
});
