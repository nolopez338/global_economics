import test from 'node:test';
import assert from 'node:assert/strict';
import {Box3,Vector3,Quaternion} from '../assets/vendor/three-0.170.0/three.module.js';
import {Design,CATALOG,validate,localPorts,port,clone,rectangle,vec} from '../assets/js/pvc-model.mjs';
import {PERSON_LIMITS,PERSON_DEFAULTS,personProperties} from '../assets/js/pvc-person.mjs';
import {geometry,dispose} from '../assets/js/pvc-geometry.mjs';
import {placementTargets,choosePlacement,alignPlacement} from '../assets/js/pvc-placement.mjs';
import {PDF_VIEWS,frameExportCamera} from '../assets/js/pvc-pdf.mjs';
import {buildTemplate,TEMPLATES} from '../assets/js/pvc-templates.mjs';

const bounds=p=>{const g=geometry(p);try{return new Box3().setFromObject(g,true);}finally{dispose(g);}};
const close=(a,b)=>assert(Math.abs(a-b)<1e-5,`${a} != ${b}`);

test('Person defaults, independent instances and actual 1800 mm sole-to-crown geometry',()=>{
  const m=new Design(),a=m.add('person',[0,0,0]),b=m.add('person',[0,0,0]);
  assert.deepEqual(personProperties(a),PERSON_DEFAULTS);assert.notEqual(a.id,b.id);
  const box=bounds(a);close(box.min.y,0);close(box.max.y,1800);assert(box.max.z-box.min.z>150);
  m.updatePerson(a.id,{height:1900,variant:'woman'});assert.equal(b.height,1800);assert.equal(b.variant,'man');
  assert.equal(CATALOG.person.reference,true);assert.deepEqual(localPorts(a),[]);
});

for(const category of ['adult','child'])for(const variant of ['man','woman'])test(`${category}/${variant}: inclusive limits, proportional geometry and fixed local soles`,()=>{
  const m=new Design(),p=m.add('person',[35,70,-100],undefined,new Quaternion().setFromAxisAngle(vec([1,2,3]).normalize(),.8).toArray());
  m.setPersonCategory(p.id,category);m.updatePerson(p.id,{variant});const {min,max}=PERSON_LIMITS[category],transform=clone({p:p.p,q:p.q});
  m.updatePerson(p.id,{height:min});const low=bounds(p),size=low.getSize(new Vector3());
  m.updatePerson(p.id,{height:max});const high=bounds(p),larger=high.getSize(new Vector3());
  close(low.min.y,0);close(high.min.y,0);close(low.max.y,min);close(high.max.y,max);
  for(let i=0;i<3;i++)close(larger.getComponent(i)/size.getComponent(i),max/min);
  assert.deepEqual({p:p.p,q:p.q},transform);validate(m.data());
  for(const height of [min-.001,max+.001,0,-1,NaN,Infinity,'1800',null]){
    const before=m.data();assert.throws(()=>m.updatePerson(p.id,{height}),/height/);assert.deepEqual(m.data(),before);
  }
});

test('silhouettes differ in geometry without changing height, category or transforms',()=>{
  const m=new Design(),p=m.add('person',[10,20,30]),before=clone(p),man=geometry(p);
  m.updatePerson(p.id,{variant:'woman'});const woman=bounds(p);
  const other=geometry(p);assert.notDeepEqual(man.children[2].geometry.attributes.position.array,other.children[2].geometry.attributes.position.array);
  dispose(man);dispose(other);
  assert.deepEqual({...p,variant:'man'},before);close(woman.max.y,1800);
});

test('category switching preserves overlap heights and clamps only when required',()=>{
  const m=new Design(),p=m.add('person');
  m.setPersonCategory(p.id,'child');assert.equal(p.height,1700);
  m.updatePerson(p.id,{height:1500});m.setPersonCategory(p.id,'adult');assert.equal(p.height,1500);
  m.setPersonCategory(p.id,'child');assert.equal(p.height,1500);
  m.updatePerson(p.id,{height:600});m.setPersonCategory(p.id,'adult');assert.equal(p.height,1400);
  m.updatePerson(p.id,{height:2200});m.setPersonCategory(p.id,'child');assert.equal(p.height,1700);
});

test('documented missing-property defaults; invalid supplied values and overrides rejected atomically',()=>{
  const m=new Design();m.add('person');const data=m.data();
  const missing=clone(data);for(const key of ['category','variant','height'])delete missing.pieces[0][key];
  assert.deepEqual(personProperties(validate(missing).pieces[0]),PERSON_DEFAULTS);
  missing.pieces[0].category='child';assert.equal(validate(missing).pieces[0].height,1200);
  const bad=[{category:'teen'},{category:null},{category:['adult']},{category:'constructor'},{variant:'other'},{variant:['man']},{variant:null},{height:null},{height:'1800'},{height:NaN},{height:Infinity},{height:1399},{height:2201},{length:400},{scale:1},{ports:[]},{insertion:0},{sockets:[]},{p:[NaN,0,0]},{q:[0,0,0,Infinity]},{q:[0,0,0,2]}];
  for(const changes of bad){const incoming=clone(data);Object.assign(incoming.pieces[0],changes);const before=m.data();
    for(const check of [()=>validate(incoming),()=>new Design(incoming),()=>m.paste(incoming)])assert.throws(check,undefined,JSON.stringify(changes));
    assert.deepEqual(m.data(),before);
  }
  const undefinedHeight=clone(data);undefinedHeight.pieces[0].height=undefined;assert.throws(()=>validate(undefinedHeight),/height/);
  // Person-specific fields remain forbidden on every construction component.
  for(const type of Object.keys(CATALOG).filter(t=>t!=='person'))for(const key of ['height','category','variant']){
    const pvc=new Design();pvc.add(type);const incoming=pvc.data();incoming.pieces[0][key]=data.pieces[0][key];assert.throws(()=>validate(incoming),/override/);
  }
});

test('no ports, snap sources/targets or joints; overlapping references never join or restrict PVC',()=>{
  const m=rectangle(),reference=m.add('person',m.pieces[0].p),other=m.add('person',reference.p),tube=m.pieces.find(p=>p.type==='tube');
  const before=m.data(),targets=placementTargets(m);assert(targets.every(t=>t.target.id!==reference.id&&t.target.id!==other.id));
  assert.equal(choosePlacement({piece:reference,targets,pointer:{x:0,y:0},project:()=>{throw Error('Reference snapping must bypass projection');}}),null);
  assert.throws(()=>port(reference,0),/port/);assert.throws(()=>alignPlacement(reference,0,targets[0]||{position:vec([0,0,0]),direction:vec([1,0,0])}),/port/);
  for(const [a,b] of [[reference,tube],[tube,reference],[reference,other]]){
    assert.throws(()=>m.connect({id:a.id,port:0},{id:b.id,port:0}));assert.deepEqual(m.data(),before);
    const incoming=clone(before);incoming.connections.push({id:'bad-person-joint',a:{id:a.id,port:0},b:{id:b.id,port:0}});assert.throws(()=>validate(incoming),/port/);
  }
  const assembly=m.connected([tube.id]);assert(!assembly.has(reference.id));m.transform(assembly,undefined,undefined,vec([100,0,0]));
  assert.deepEqual(reference.p,before.pieces.find(p=>p.id===reference.id).p);validate(m.data());
  const explicit=m.connected([tube.id,reference.id]);assert(explicit.has(reference.id));assert(!explicit.has(other.id));
  const delta=vec([50,30,-10]);m.transform(explicit,new Quaternion().setFromAxisAngle(vec([0,1,0]),.7),undefined,delta);validate(m.data());
  m.updatePerson(reference.id,{height:2200});m.setPersonCategory(reference.id,'child');validate(m.data());
  assert.equal(m.connections.length,before.connections.length);assert(m.coordinatedLengthPlan(new Set([tube.id,reference.id])).locked);
});

test('copy/paste, snapshots, deletion, round trip and old PVC-only compatibility',()=>{
  const m=rectangle(),old=m.data(),p=m.add('person');m.setPersonCategory(p.id,'child');m.updatePerson(p.id,{height:1234.56,variant:'woman'});
  const snapshot=m.data();m.updatePerson(p.id,{height:1400});assert.equal(new Design(snapshot).get(p.id).height,1234.56);
  const copied=m.copy(new Set(m.pieces.map(p=>p.id))),ids=m.paste(copied),pasted=m.pieces.filter(p=>ids.has(p.id));
  assert.equal(pasted.filter(p=>p.type==='person').length,1);assert.equal(m.connections.length,snapshot.connections.length*2);
  const ref=pasted.find(p=>p.type==='person');assert.equal(ref.height,1400);assert.equal(ref.variant,'woman');assert.equal(ref.category,'child');assert.deepEqual(ref.p,vec(p.p).add(vec([80,0,80])).toArray());
  assert.deepEqual(validate(JSON.parse(JSON.stringify(m.data()))).data(),m.data());m.remove(ids);assert.equal(m.pieces.length,snapshot.pieces.length);
  assert.deepEqual(validate(old).data(),old);
});

test('references excluded from every PVC quantity and all structural templates',()=>{
  const m=rectangle(),summary=m.materials();m.add('person');m.add('person');
  assert.deepEqual(m.materials(),{...summary,references:2});assert.equal(m.summary().total,summary.total);
  for(const template of TEMPLATES)assert(buildTemplate(template.id).pieces.every(p=>p.type!=='person'));
});

test('PDF camera framing contains full reference geometry in all eight views',()=>{
  const m=new Design(),p=m.add('person');m.updatePerson(p.id,{height:2200,variant:'woman'});const box=bounds(p);
  for(const view of PDF_VIEWS){const camera=frameExportCamera(box,view,86/96);
    for(const x of [box.min.x,box.max.x])for(const y of [box.min.y,box.max.y])for(const z of [box.min.z,box.max.z]){
      const v=new Vector3(x,y,z).project(camera);assert(Math.abs(v.x)<1&&Math.abs(v.y)<1&&Math.abs(v.z)<1,view.label);
    }
  }
});
