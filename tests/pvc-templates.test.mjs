import test from 'node:test';
import assert from 'node:assert/strict';
import {TEMPLATES,buildTemplate} from '../assets/js/pvc-templates.mjs';
import {CATALOG,validate,port,vec,localPorts,MIN_LENGTH,MAX_LENGTH} from '../assets/js/pvc-model.mjs';
import {geometry,dispose} from '../assets/js/pvc-geometry.mjs';
import {Box3,Group,Quaternion} from '../assets/vendor/three-0.170.0/three.module.js';

const ids=['ground','ladder','grid','portal','box','tower','bridge','gable','lframe','octagon'];
const near=(a,b,tolerance=1e-7)=>assert(Math.abs(a-b)<tolerance,`${a} != ${b}`);
const vectorNear=(a,b,tolerance=1e-7)=>assert(vec(a).distanceTo(vec(b))<tolerance,`${a} != ${b}`);

test('exactly ten distinct, nonempty structural patterns in the documented order',()=>{
  assert.deepEqual(TEMPLATES.map(t=>t.id),ids);
  assert.equal(new Set(TEMPLATES.map(t=>t.name)).size,10);
  assert.equal(new Set(TEMPLATES.map(t=>t.description)).size,10);
  for(const t of TEMPLATES){assert(t.name&&t.description&&t.dimensions);assert(buildTemplate(t.id).pieces.length>0);}
  assert.throws(()=>buildTemplate('unknown'));
  assert.throws(()=>buildTemplate('empty'));
});

for(const template of TEMPLATES)test(`${template.id}: standard components, seated connected graph, editable round trip`,()=>{
  const m=buildTemplate(template.id),data=m.data();
  assert.equal(m.connected([m.pieces[0].id]).size,m.pieces.length,'Template has a disconnected member');
  assert.equal(new Set([...m.pieces,...m.connections].map(p=>p.id)).size,m.pieces.length+m.connections.length);
  const used=new Set();
  for(const c of m.connections){
    for(const e of [c.a,c.b]){const key=e.id+':'+e.port;assert(!used.has(key),'A socket is used twice');used.add(key);}
    const a=port(m.get(c.a.id),c.a.port),b=port(m.get(c.b.id),c.b.port);
    assert(a.position.distanceTo(b.position)<1e-7,'Unseated joint');
    near(a.direction.dot(b.direction),-1);assert.notEqual(a.type,b.type);
  }
  for(const p of m.pieces){
    assert(Object.hasOwn(CATALOG,p.type),'Unsupported component');
    assert(!Object.hasOwn(p,'sockets')&&!Object.hasOwn(p,'ports'),'Per-piece socket override');
    if(p.type==='tube'){
      assert(p.length>=MIN_LENGTH&&p.length<=MAX_LENGTH);
      assert(used.has(p.id+':0')&&used.has(p.id+':1'),'An unconnected tube end appears structural');
    }else assert.equal(localPorts(p),CATALOG[p.type].ports,'Fitting does not use fixed catalog sockets');
  }
  const restored=validate(JSON.parse(JSON.stringify(data)));
  assert.deepEqual(restored.data(),data);assert.deepEqual(restored.materials(),m.materials());
  assert.equal(m.materials().rows.reduce((n,r)=>n+r.count,0),m.pieces.length);
  near(m.materials().total,m.pieces.filter(p=>p.type==='tube').reduce((n,p)=>n+p.length,0),1e-6);
  const copy=m.copy(new Set(m.pieces.map(p=>p.id))),fresh=m.paste(copy);
  const rotation=new Quaternion().setFromAxisAngle(vec([1,2,3]).normalize(),.47);
  m.transform(fresh,rotation,vec([10,20,30]),vec([4000,100,200]));validate(m.data());
  assert.equal(fresh.size,data.pieces.length);
});

for(const template of TEMPLATES)test(`${template.id}: detach a joint and edit a tube cut without distorting retained joints`,()=>{
  const m=buildTemplate(template.id),tube=m.pieces.find(p=>p.type==='tube'&&p.length+10<=MAX_LENGTH);
  assert(tube,'Template has no tube available for the editability exercise');
  const joint=m.connections.find(c=>c.a.id===tube.id||c.b.id===tube.id),oldLength=tube.length,oldJointCount=m.connections.length;
  assert(joint,'Editable tube is not connected');
  m.disconnect(joint.id);assert(!m.lengthPlan(tube.id).locked,'Detaching one incident joint should free the cut');
  m.resize(tube.id,oldLength+10);
  near(m.get(tube.id).length,oldLength+10);assert.equal(m.connections.length,oldJointCount-1);
  validate(m.data()); // All retained joints must still be fully seated and aligned.
});

// Physical tube ends stop 25 mm from fitting centers. The intended overlap with
// each own socket is excluded here; distinct tube walls must never intersect.
function segmentDistance(p1,q1,p2,q2){
  const d1=q1.clone().sub(p1),d2=q2.clone().sub(p2),r=p1.clone().sub(p2);
  const a=d1.dot(d1),e=d2.dot(d2),b=d1.dot(d2),c=d1.dot(r),f=d2.dot(r),denom=a*e-b*b;
  const clamp=x=>Math.max(0,Math.min(1,x));let s=denom?clamp((b*f-c*e)/denom):0,t=(b*s+f)/e;
  if(t<0){t=0;s=clamp(-c/a);}else if(t>1){t=1;s=clamp((b-c)/a);}
  return p1.clone().addScaledVector(d1,s).distanceTo(p2.clone().addScaledVector(d2,t));
}
for(const template of TEMPLATES)test(`${template.id}: distinct tube walls do not intersect`,()=>{
  const m=buildTemplate(template.id),tubes=m.pieces.filter(p=>p.type==='tube');
  for(let i=0;i<tubes.length;i++)for(let j=0;j<i;j++){
    const a=tubes[i],b=tubes[j];
    const distance=segmentDistance(port(a,0).position,port(a,1).position,port(b,0).position,port(b,1).position);
    assert(distance>32+1e-7,`Unintended tube intersection: ${a.p} / ${b.p}; clearance ${distance} mm`);
  }
});

// A fitting fits inside a 64 mm radius ball: elbow center curves stay within
// 45 mm and have 19 mm walls; straight socket cylinders reach 45 mm with
// radial extent at most 22 mm (sqrt(45² + 22²) < 64). This deliberately larger
// envelope protects curved cores as well as the exact straight socket axes.
const FITTING_ENVELOPE=64,TUBE_RADIUS=16,SOCKET_RADIUS=22;
function pointSegmentDistance(point,start,end){
  const direction=end.clone().sub(start),lengthSquared=direction.lengthSq();
  const parameter=Math.max(0,Math.min(1,point.clone().sub(start).dot(direction)/lengthSquared));
  return point.distanceTo(start.clone().addScaledVector(direction,parameter));
}
for(const template of TEMPLATES)test(`${template.id}: fitting envelopes clear unrelated tubes and other fittings`,()=>{
  const m=buildTemplate(template.id),fittings=m.pieces.filter(p=>p.type!=='tube'),tubes=m.pieces.filter(p=>p.type==='tube');
  for(const tube of tubes){
    const ends=[port(tube,0).position,port(tube,1).position];
    const ownFittings=new Set(m.connections.filter(c=>c.a.id===tube.id||c.b.id===tube.id).map(c=>c.a.id===tube.id?c.b.id:c.a.id));
    for(const fitting of fittings){
      if(ownFittings.has(fitting.id))continue; // Its own 20 mm socket insertion is intentional.
      const core=vec(fitting.p),envelopeDistance=pointSegmentDistance(core,...ends);
      assert(envelopeDistance>TUBE_RADIUS+FITTING_ENVELOPE+1e-7,
        `Tube ${tube.p} enters an unrelated fitting envelope at ${fitting.p}: ${envelopeDistance} mm`);
      for(let index=0;index<localPorts(fitting).length;index++){
        const mouth=port(fitting,index).mouth,distance=segmentDistance(...ends,core,mouth);
        assert(distance>TUBE_RADIUS+SOCKET_RADIUS+1e-7,
          `Tube ${tube.p} intersects an unrelated socket at ${fitting.p}: ${distance} mm`);
      }
    }
  }
  for(let i=0;i<fittings.length;i++)for(let j=0;j<i;j++){
    const a=fittings[i],b=fittings[j],distance=vec(a.p).distanceTo(vec(b.p));
    assert(distance>2*FITTING_ENVELOPE+1e-7,
      `Fitting envelopes overlap at ${a.p} / ${b.p}: ${distance} mm`);
  }
});

test('Template 6 outer geometry is exactly 1300 × 400 × 2200 mm and rests at y=0',()=>{
  assert.equal(TEMPLATES[5].id,'tower');
  const m=buildTemplate('tower'),group=new Group();
  try{
    for(const p of m.pieces){const g=geometry(p);g.position.fromArray(p.p);g.quaternion.fromArray(p.q);group.add(g);}
    group.updateMatrixWorld(true);const bounds=new Box3().setFromObject(group,true);
    vectorNear(bounds.min.toArray(),[-650,0,-200],1e-6);
    vectorNear(bounds.max.toArray(),[650,2200,200],1e-6);
    vectorNear(bounds.getSize(vec([0,0,0])).toArray(),[1300,2200,400],1e-6);
  }finally{dispose(group);}
});

test('Template 6 has six collision-free diagonal load paths in three planes, with standard rolled tees',()=>{
  const m=buildTemplate('tower');
  const braces=m.pieces.filter(p=>p.type==='tube'&&port(p,1).direction.toArray().filter(v=>Math.abs(v)>1e-7).length===2);
  assert.equal(braces.length,6,'Each width, depth and plan pair must have two distinct braces');
  const expected=[
    [[-629,21,-49],[629,2179,-49]],[[629,21,49],[-629,2179,49]],
    [[-429,21,179],[-429,2179,-179]],[[429,21,-179],[429,2179,179]],
    [[-629,200,-179],[629,200,179]],[[-629,2000,179],[629,2000,-179]]
  ];
  for(const brace of braces){
    const fittingEnds=[0,1].map(i=>{
      const c=m.connections.find(c=>[c.a,c.b].some(e=>e.id===brace.id&&e.port===i));
      const e=c.a.id===brace.id?c.b:c.a,fit=m.get(e.id);assert.equal(fit.type,'tee');
      const defs=localPorts(fit);assert.equal(e.port,2,'Brace must use the radial branch of a standard tee');
      near(vec(defs[0].direction).dot(vec(defs[2].direction)),0);
      return fit.p;
    });
    const index=expected.findIndex(([a,b])=>
      (vec(a).distanceTo(vec(fittingEnds[0]))<1e-7&&vec(b).distanceTo(vec(fittingEnds[1]))<1e-7)||
      (vec(b).distanceTo(vec(fittingEnds[0]))<1e-7&&vec(a).distanceTo(vec(fittingEnds[1]))<1e-7));
    assert(index>=0,`Unexpected brace endpoints ${fittingEnds}`);
    const [a,b]=expected.splice(index,1)[0];near(brace.length,vec(a).distanceTo(vec(b))-50);
  }
  assert.equal(expected.length,0);
  // Width/depth ties use separate stations so a forbidden four-socket spatial
  // junction is never needed where continuous columns meet the two rail sets.
  for(const y of [970,1100])assert(m.pieces.some(p=>p.type==='tee'&&Math.abs(p.p[1]-y)<1e-7));
});
