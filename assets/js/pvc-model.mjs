// PVC Studio's independent, millimetre-based construction model.
import {Vector3, Quaternion} from '../vendor/three-0.170.0/three.module.js';
export const RADIUS = 16, INNER_RADIUS = 13, INSERTION = 20, MIN_LENGTH = 80, MAX_LENGTH = 3000;
const socket = (direction) => ({position: direction.map(x => x * 45), direction, type: 'socket', insertion: INSERTION});
export const CATALOG = Object.freeze({
  tube: {name: 'Straight tube', note: '80–3,000 mm cut length', ports: null, icon: 'tube'},
  coupling: {name: 'Straight coupling', note: '2 sockets · inline', ports: [socket([-1,0,0]),socket([1,0,0])]},
  elbow90: {name: '90° elbow', note: '2 sockets · right angle', ports: [socket([1,0,0]),socket([0,0,1])]},
  elbow45: {name: '45° elbow', note: '2 sockets · gentle turn', ports: [socket([-1,0,0]),socket([Math.SQRT1_2,0,Math.SQRT1_2])]},
  tee: {name: 'Three-port tee', note: '3 sockets · branch', ports: [socket([-1,0,0]),socket([1,0,0]),socket([0,0,1])]},
  cross: {name: 'Four-port cross', note: '4 sockets · flat junction', ports: [socket([-1,0,0]),socket([1,0,0]),socket([0,0,-1]),socket([0,0,1])]},
  corner: {name: 'Three-way corner', note: '3 sockets · furniture corner', ports: [socket([1,0,0]),socket([0,1,0]),socket([0,0,1])]},
  cap: {name: 'End cap', note: '1 socket · closed end', ports: [socket([1,0,0])]}
});
export const uid = () => crypto.randomUUID();
export const vec = a => new Vector3(...a);
export const quat = a => new Quaternion(...a);
export const clone = a => JSON.parse(JSON.stringify(a));
export function localPorts(piece) {
  return piece.type === 'tube' ? [-1,1].map(s => ({position:[s*piece.length/2,0,0],direction:[s,0,0],type:'tube',insertion:0})) : CATALOG[piece.type].ports;
}
export function port(piece, index) {
  const p = localPorts(piece)[index];
  if (!p) throw Error('Unknown connection port.');
  const direction = vec(p.direction).applyQuaternion(quat(piece.q));
  const mouth = vec(p.position).applyQuaternion(quat(piece.q)).add(vec(piece.p));
  // Socket's mating datum is its internal stop. A physical tube end seats 20 mm inside the mouth.
  return {...p, direction, mouth, position: mouth.clone().addScaledVector(direction,-p.insertion)};
}
export class Design {
  constructor(data = {pieces:[],connections:[]}) { this.pieces=clone(data.pieces); this.connections=clone(data.connections); }
  data() {return {format:'pvc-studio',version:1,catalog:'pvc-32-v1',units:'mm',radius:RADIUS,pieces:clone(this.pieces),connections:clone(this.connections)};}
  get(id) {const p=this.pieces.find(p=>p.id===id); if(!p) throw Error('Piece no longer exists.'); return p;}
  add(type,p=[0,60,0],length=400,q=[0,0,0,1]) {
    if(!Object.hasOwn(CATALOG,type)) throw Error('Unknown component type.');
    const piece={id:uid(),type,p:[...p],q:[...q],...(type==='tube'?{length}: {})}; this.pieces.push(piece); return piece;
  }
  occupied(id,index) {return this.connections.some(c=>[c.a,c.b].some(e=>e.id===id&&e.port===index));}
  connected(ids,excluded=new Set()) {
    const found=new Set([...ids].filter(id=>!excluded.has(id))), queue=[...found];
    while(queue.length){const id=queue.pop(); for(const c of this.connections){const next=c.a.id===id?c.b.id:c.b.id===id?c.a.id:null;
      if(next&&!excluded.has(next)&&!found.has(next)){found.add(next);queue.push(next);}}} return found;
  }
  transform(ids,rotation=new Quaternion(),pivot=new Vector3(),translation=new Vector3()) {
    for(const p of this.pieces) if(ids.has(p.id)) {p.p=vec(p.p).sub(pivot).applyQuaternion(rotation).add(pivot).add(translation).toArray();p.q=rotation.clone().multiply(quat(p.q)).normalize().toArray();}
  }
  check(a,b,geometry=true) {
    if(a.id===b.id) throw Error('A piece cannot connect to itself.');
    const pa=port(this.get(a.id),a.port),pb=port(this.get(b.id),b.port);
    if(pa.type===pb.type) throw Error('Connect a tube end to a fitting socket. Tube-to-tube and socket-to-socket joints are incompatible.');
    if(this.occupied(a.id,a.port)||this.occupied(b.id,b.port)) throw Error('This port is occupied. Detach its joint first.');
    if(geometry&&(pa.position.distanceTo(pb.position)>.05||pa.direction.dot(pb.direction)>-.99999)) throw Error('This joint would distort the assembly. Align both ports exactly or detach an existing joint.');
    return [pa,pb];
  }
  alignment(a,b) {
    const [pa,pb]=this.check(a,b,false);
    return {rotation:new Quaternion().setFromUnitVectors(pa.direction,pb.direction.clone().negate()),pivot:pa.position,translation:pb.position.clone().sub(pa.position)};
  }
  connect(a,b,align=true) {
    this.check(a,b,false);
    const moving=this.connected([a.id]);
    if(!moving.has(b.id)&&align){const t=this.alignment(a,b);this.transform(moving,t.rotation,t.pivot,t.translation);}
    this.check(a,b); const c={id:uid(),a:{...a},b:{...b}};this.connections.push(c);return c;
  }
  disconnect(id) {this.connections=this.connections.filter(c=>c.id!==id);}
  remove(ids) {this.pieces=this.pieces.filter(p=>!ids.has(p.id));this.connections=this.connections.filter(c=>!ids.has(c.a.id)&&!ids.has(c.b.id));}
  lengthPlan(id) {
    const p=this.get(id), ends=[0,1].map(i=>this.connections.find(c=>[c.a,c.b].some(e=>e.id===id&&e.port===i)));
    const other=c=>c.a.id===id?c.b.id:c.a.id;
    if(ends.every(Boolean)) {const side=this.connected([other(ends[1])],new Set([id]));if(side.has(other(ends[0])))return {locked:true,reason:`Closed frame: detach joint ${ends[1].id.slice(0,8)} at tube end 2, or another joint on its alternate path, before resizing.`,joint:ends[1].id};return {fixed:0,side};}
    return {fixed:ends[0]?0:ends[1]?1:null,side:new Set()};
  }
  resize(id,length) {
    if(!Number.isFinite(length)||length<MIN_LENGTH||length>MAX_LENGTH)throw Error(`Cut length must be ${MIN_LENGTH}–${MAX_LENGTH} mm.`);
    const p=this.get(id);if(p.type!=='tube')throw Error('Only tubes have cut lengths.');
    const plan=this.lengthPlan(id);if(plan.locked)throw Error(plan.reason);
    const delta=length-p.length, axis=vec([1,0,0]).applyQuaternion(quat(p.q));
    if(plan.fixed!==null)p.p=vec(p.p).addScaledVector(axis,(plan.fixed===0?1:-1)*delta/2).toArray();
    this.transform(plan.side,new Quaternion(),new Vector3(),axis.multiplyScalar(delta));p.length=length;
  }
  copy(ids) {return {pieces:clone(this.pieces.filter(p=>ids.has(p.id))),connections:clone(this.connections.filter(c=>ids.has(c.a.id)&&ids.has(c.b.id)))};}
  paste(data,offset=[80,0,80]) {
    const map=new Map(data.pieces.map(p=>[p.id,uid()]));
    this.pieces.push(...data.pieces.map(p=>({...clone(p),id:map.get(p.id),p:vec(p.p).add(vec(offset)).toArray()})));
    this.connections.push(...data.connections.map(c=>({id:uid(),a:{id:map.get(c.a.id),port:c.a.port},b:{id:map.get(c.b.id),port:c.b.port}})));
    return new Set(map.values());
  }
  summary() {const rows=new Map();let total=0;for(const p of this.pieces){const name=p.type==='tube'?`Tube · ${Number(p.length.toFixed(3))} mm`:CATALOG[p.type].name;rows.set(name,(rows.get(name)||0)+1);if(p.type==='tube')total+=p.length;}return {rows:[...rows],total};}
}
export function validate(data) {
  if(!data||data.format!=='pvc-studio'||data.version!==1||data.catalog!=='pvc-32-v1'||data.units!=='mm'||data.radius!==RADIUS)throw Error('Unsupported design. Expected PVC Studio v1, pvc-32-v1 catalog, millimetres and 32 mm tubes.');
  if(!Array.isArray(data.pieces)||!Array.isArray(data.connections)||data.pieces.length>2000||data.connections.length>6000)throw Error('Invalid design arrays or design exceeds 2,000 pieces / 6,000 joints.');
  const ids=new Set(), array=(a,n)=>Array.isArray(a)&&a.length===n&&a.every(x=>Number.isFinite(x)&&Math.abs(x)<1e7);
  for(const p of data.pieces){if(typeof p.id!=='string'||!p.id||p.id.length>100||ids.has(p.id))throw Error('Missing or duplicate piece ID.');ids.add(p.id);
    if(!Object.hasOwn(CATALOG,p.type)||!array(p.p,3)||!array(p.q,4)||Math.abs(quat(p.q).length()-1)>.00001)throw Error('Invalid component or transform.');
    if(p.type==='tube'&&(!Number.isFinite(p.length)||p.length<MIN_LENGTH||p.length>MAX_LENGTH))throw Error('Invalid tube cut length.');}
  const model=new Design({pieces:data.pieces,connections:[]}), jointIds=new Set();
  for(const c of data.connections){if(typeof c.id!=='string'||!c.id||c.id.length>100||jointIds.has(c.id)||ids.has(c.id))throw Error('Missing or duplicate joint ID.');jointIds.add(c.id);
    for(const e of [c.a,c.b])if(!e||!ids.has(e.id)||!Number.isInteger(e.port)||e.port<0||e.port>=localPorts(model.get(e.id)).length)throw Error('Joint refers to an invalid piece or port.');
    model.check(c.a,c.b);model.connections.push(clone(c));}
  // Normalize to supported fields only; arbitrary imported properties never reach the UI.
  model.pieces=model.pieces.map(p=>({id:p.id,type:p.type,p:[...p.p],q:[...p.q],...(p.type==='tube'?{length:p.length}:{})}));return model;
}
export function rectangle() {
  const m=new Design(), elbows=[];
  for(const [x,z,angle] of [[-300,-200,0],[300,-200,-Math.PI/2],[300,200,Math.PI],[-300,200,Math.PI/2]])elbows.push(m.add('elbow90',[x,60,z],400,new Quaternion().setFromAxisAngle(vec([0,1,0]),angle).toArray()));
  for(let i=0;i<4;i++){const a=elbows[i],b=elbows[(i+1)%4];const dir=vec(b.p).sub(vec(a.p)).normalize();const t=m.add('tube',vec(a.p).add(vec(b.p)).multiplyScalar(.5).toArray(),vec(a.p).distanceTo(vec(b.p))-50,new Quaternion().setFromUnitVectors(vec([1,0,0]),dir).toArray());
    const ai=localPorts(a).findIndex((_,j)=>port(a,j).direction.dot(dir)>.999),bi=localPorts(b).findIndex((_,j)=>port(b,j).direction.dot(dir)<-.999);
    m.connect({id:t.id,port:0},{id:a.id,port:ai},false);m.connect({id:t.id,port:1},{id:b.id,port:bi},false);}
  return m;
}
