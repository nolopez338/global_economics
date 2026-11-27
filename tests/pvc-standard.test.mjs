import test from 'node:test';
import assert from 'node:assert/strict';
import {Design,CATALOG,validate,localPorts,materialsSummary,rectangle,clone,compatiblePorts} from '../assets/js/pvc-model.mjs';
import {geometry,dispose} from '../assets/js/pvc-geometry.mjs';
import {createDesignPDF} from '../assets/js/pvc-pdf.mjs';
const allowed=['tube','coupling','elbow90','elbow45','tee','cross','corner','person'];
const invalidTypes=['multiway','cap','custom','junction','constructor','__proto__'];
const overrides={sockets:[],ports:[],socketCount:8,directions:[[1,0,0]],positions:[[0,0,0]],direction:[1,0,0],position:[0,0,0],insertion:0,compatibility:'any',radius:100,scale:2};
test('exact allowlist; standard socket arrays are deeply immutable',()=>{
  assert.deepEqual(Object.keys(CATALOG),allowed);
  for(const [type,count] of Object.entries({coupling:2,elbow90:2,elbow45:2,tee:3,cross:4,corner:3})){
    assert.equal(CATALOG[type].ports.length,count);
    assert.throws(()=>CATALOG[type].ports.push({}),TypeError);
    assert.throws(()=>CATALOG[type].ports[0].direction[0]=99,TypeError);
    assert.throws(()=>CATALOG[type].ports[0].position[0]=99,TypeError);
    assert.throws(()=>CATALOG[type].ports[0].insertion=0,TypeError);
  }
  const dirs=CATALOG.corner.ports.map(p=>p.direction);
  for(let i=0;i<3;i++)for(let j=i+1;j<3;j++)assert.equal(dirs[i].reduce((n,v,k)=>n+v*dirs[j][k],0),0);
  assert(!compatiblePorts({type:'custom'},{type:'socket'}));
});
test('every allowed component can be manually created, rendered and exported',()=>{
  const m=new Design();for(const type of allowed){const p=m.add(type);const g=geometry(p);assert(g.children.length);dispose(g);}
  const d=validate(JSON.parse(JSON.stringify(m.data())));assert.deepEqual(d.data(),m.data());assert.equal(d.materials().rows.length,7);
});
for(const type of invalidTypes)test(`reject ${type} in creation, construction, validation, paste, geometry and exports`,async()=>{
  const m=rectangle(),before=m.data(),incoming=clone(before);incoming.pieces.at(-1).type=type;
  assert.throws(()=>m.add(type),/Unsupported/);assert.deepEqual(m.data(),before);
  for(const check of [()=>new Design(incoming),()=>validate(incoming),()=>m.paste(incoming),()=>geometry(incoming.pieces.at(-1)),()=>materialsSummary(incoming.pieces)])assert.throws(check,/Unsupported/);
  await assert.rejects(createDesignPDF(incoming),/Unsupported/);assert.deepEqual(m.data(),before);
});
for(const [key,value] of Object.entries(overrides))test(`reject per-piece ${key} overrides atomically on every type`,()=>{
  for(const type of allowed){const m=new Design();m.add(type);const before=m.data(),data=clone(before);data.pieces[0][key]=value;
    for(const check of [()=>new Design(data),()=>validate(data),()=>m.paste(data),()=>materialsSummary(data.pieces)])assert.throws(check,/override|arbitrary/i);
    assert.deepEqual(m.data(),before);
  }
});
test('reject even identical socket definitions; no silent standard fitting conversion',()=>{
  const m=new Design(),p=m.add('tee'),before=m.data();
  assert.throws(()=>m.add('tee',[0,0,0],400,[0,0,0,1],clone(CATALOG.tee.ports)),/overrides/);
  assert.deepEqual(m.data(),before);p.sockets=clone(CATALOG.tee.ports);
  assert.throws(()=>localPorts(p),/overrides/);assert.throws(()=>m.data(),/overrides/);assert.throws(()=>m.copy(new Set([p.id])),/overrides/);
});
test('paste validates the complete graph and shifted geometry before mutation',()=>{
  const m=rectangle(),before=m.data();
  for(const mutate of [d=>d.connections.at(-1).b.port=99,d=>d.pieces.at(-1).p[0]+=20]){
    const d=clone(before);mutate(d);assert.throws(()=>m.paste(d));assert.deepEqual(m.data(),before);
  }
  assert.throws(()=>m.paste(m.copy(new Set(m.pieces.map(p=>p.id))),[NaN,0,0]));assert.deepEqual(m.data(),before);
});

test('arbitrary endpoint port definitions are rejected in manual joints and imports',()=>{
  const m=new Design(),t=m.add('tube'),f=m.add('tee'),before=m.data();
  assert.throws(()=>m.connect({id:t.id,port:0,sockets:[]},{id:f.id,port:0}),/overrides/);assert.deepEqual(m.data(),before);
  const data=rectangle().data();data.connections[0].a.direction=[0,1,0];assert.throws(()=>validate(data),/overrides/);
});
