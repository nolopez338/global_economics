// PVC Studio's independent, millimetre-based construction model.
import {Vector3, Quaternion} from '../vendor/three-0.170.0/three.module.js';
import {personProperties,personCategoryChange} from './pvc-person.mjs';
export const RADIUS = 16, INNER_RADIUS = 13, INSERTION = 20, MIN_LENGTH = 80, MAX_LENGTH = 3000;
export const PARALLEL_TOLERANCE = 1e-7;
const socket = (direction) => ({position: direction.map(x => x * 45), direction, type: 'socket', insertion: INSERTION});
const deepFreeze = value => {if(value && typeof value==='object'){Object.values(value).forEach(deepFreeze);Object.freeze(value);}return value;};
export const CATALOG = deepFreeze({
  tube: {name: 'Straight tube', note: '80–3,000 mm cut length', ports: null, icon: 'tube'},
  coupling: {name: 'Straight coupling', note: '2 sockets · inline', ports: [socket([-1,0,0]),socket([1,0,0])]},
  elbow90: {name: '90° elbow', note: '2 sockets · right angle', ports: [socket([1,0,0]),socket([0,0,1])]},
  elbow45: {name: '45° elbow', note: '2 sockets · gentle turn', ports: [socket([-1,0,0]),socket([Math.SQRT1_2,0,Math.SQRT1_2])]},
  tee: {name: 'Three-port tee', note: '3 sockets · branch', ports: [socket([-1,0,0]),socket([1,0,0]),socket([0,0,1])]},
  cross: {name: 'Four-port cross', note: '4 sockets · flat junction', ports: [socket([-1,0,0]),socket([1,0,0]),socket([0,0,-1]),socket([0,0,1])]},
  corner: {name: 'Three-way corner', note: '3 sockets · furniture corner', ports: [socket([1,0,0]),socket([0,1,0]),socket([0,0,1])]},
  person: {name: 'Person', note: 'Scale reference · no connections', reference:true, ports:[]}
});
export const uid = () => crypto.randomUUID();
export const vec = a => new Vector3(...a);
export const quat = a => new Quaternion(...a);
export const clone = a => JSON.parse(JSON.stringify(a));
const header = {format:'pvc-studio',version:1,catalog:'pvc-32-v1',units:'mm',radius:RADIUS};
const array = (a,n) => Array.isArray(a)&&a.length===n&&a.every(x=>Number.isFinite(x)&&Math.abs(x)<1e7);
function standardType(piece) {
  if(!piece || !Object.hasOwn(CATALOG,piece.type))throw Error('Unsupported component type. Use a standard PVC component or Person scale reference.');
  const overrides=['sockets','ports','socketCount','directions','positions','direction','position','insertion','compatibility'];
  if(overrides.some(key=>Object.hasOwn(piece,key)))throw Error('Socket overrides and arbitrary ports are not allowed. Standard fitting sockets are fixed.');
}
function validatePiece(p) {
  standardType(p);
  const fields=['id','type','p','q',...(p.type==='tube'?['length']:p.type==='person'?['height','category','variant']:[])];
  if(Object.keys(p).some(key=>!fields.includes(key)))throw Error('Unsupported per-piece override. Use identity, transforms and the size properties defined for this type.');
  if(!array(p.p,3)||!array(p.q,4)||Math.abs(quat(p.q).length()-1)>.00001)throw Error('Invalid component transform.');
  if(p.type==='tube'&&(!Number.isFinite(p.length)||p.length<MIN_LENGTH||p.length>MAX_LENGTH))throw Error('Invalid tube cut length.');
  if(p.type==='person')personProperties(p);
}
export function localPorts(piece) {
  standardType(piece);
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
export const compatiblePorts = (a,b) => (a.type==='tube'&&b.type==='socket')||(a.type==='socket'&&b.type==='tube');
export function portAlignment(pa,pb) {
  return {rotation:new Quaternion().setFromUnitVectors(pa.direction,pb.direction.clone().negate()),pivot:pa.position,translation:pb.position.clone().sub(pa.position)};
}
export class Design {
  constructor(data = {pieces:[],connections:[]}) { const checked=validate({...header,...data});this.pieces=checked.pieces;this.connections=checked.connections; }
  data() {const checked=validate({...header,pieces:this.pieces,connections:this.connections});return {...header,pieces:checked.pieces,connections:checked.connections};}
  get(id) {const p=this.pieces.find(p=>p.id===id); if(!p) throw Error('Piece no longer exists.'); return p;}
  add(type,p=[0,60,0],length=400,q=[0,0,0,1],...overrides) {
    if(overrides.length)throw Error('Socket overrides and arbitrary ports are not allowed.');
    const piece={id:uid(),type,p:[...p],q:[...q],...(type==='tube'?{length}:type==='person'?personProperties({}):{})};
    validatePiece(piece);this.pieces.push(piece);return piece;
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
    for(const e of [a,b])if(!e||typeof e.id!=='string'||!Number.isInteger(e.port)||e.port<0||Object.keys(e).some(k=>!['id','port'].includes(k)))throw Error('Invalid connection endpoint. Use a piece ID and fixed standard port index; port overrides are not allowed.');
    if(a.id===b.id) throw Error('A piece cannot connect to itself.');
    const pa=port(this.get(a.id),a.port),pb=port(this.get(b.id),b.port);
    if(!compatiblePorts(pa,pb)) throw Error('Connect a tube end to a fitting socket. Tube-to-tube and socket-to-socket joints are incompatible.');
    if(this.occupied(a.id,a.port)||this.occupied(b.id,b.port)) throw Error('This port is occupied. Detach its joint first.');
    if(geometry&&(pa.position.distanceTo(pb.position)>.05||pa.direction.dot(pb.direction)>-.99999)) throw Error('This joint would distort the assembly. Align both ports exactly or detach an existing joint.');
    return [pa,pb];
  }
  alignment(a,b) {
    const [pa,pb]=this.check(a,b,false);
    return portAlignment(pa,pb);
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
  // Height changes only the reference's uniformly scaled local geometry.
  updatePerson(id,changes) {
    const p=this.get(id);if(p.type!=='person')throw Error('Select one Person to edit height or silhouette.');
    if(Object.keys(changes).some(k=>!['height','category','variant'].includes(k)))throw Error('Unsupported Person override.');
    const next={...p,...changes};validatePiece(next);Object.assign(p,personProperties(next));
  }
  setPersonCategory(id,category) {
    const p=this.get(id);if(p.type!=='person')throw Error('Select one Person to change category.');
    this.updatePerson(id,personCategoryChange(p,category));return p.height;
  }
  // Remove every selected tube at once. Each remaining connected component is
  // rigid and may only translate. For a unit cut adjustment, its end velocities
  // must satisfy v(end 2) - v(end 1) = the tube's actual world-space axis.
  // Consistent vector potentials solve loops without invoking single resize().
  coordinatedLengthPlan(ids) {
    const selected=new Set(ids), blocked=reason=>({locked:true,reason});
    if(selected.size<2)return blocked('Select at least two tubes to change their lengths together.');
    const tubes=[...selected].map(id=>this.get(id)).sort((a,b)=>a.id.localeCompare(b.id));
    if(tubes.some(p=>p.type!=='tube'))return blocked('The selection includes fittings or scale references. Select only tubes; every selected piece must participate.');
    const axes=new Map(tubes.map(p=>[p.id,vec([1,0,0]).applyQuaternion(quat(p.q))]));
    const axis=axes.get(tubes[0].id).clone().normalize();
    if(tubes.some(p=>axes.get(p.id).clone().normalize().cross(axis).length()>PARALLEL_TOLERANCE))return blocked('Selected tubes are not parallel in world space (including reversed directions).');
    const dominant=[0,1,2].sort((a,b)=>Math.abs(axis.getComponent(b))-Math.abs(axis.getComponent(a)))[0];
    if(axis.getComponent(dominant)<0)axis.negate();
    const neighbors=new Map(this.pieces.filter(p=>!selected.has(p.id)).map(p=>[p.id,[]]));
    for(const {a,b} of this.connections)if(neighbors.has(a.id)&&neighbors.has(b.id)){neighbors.get(a.id).push(b.id);neighbors.get(b.id).push(a.id);}
    const components=new Map(), nodes=[];
    for(const id of [...neighbors.keys()].sort())if(!components.has(id)){
      const node={key:id,ids:[],edges:[],rank:Infinity},queue=[id];nodes.push(node);components.set(id,node);
      while(queue.length){const next=queue.pop();node.ids.push(next);for(const other of neighbors.get(next))if(!components.has(other)){components.set(other,node);queue.push(other);}}
    }
    const attached=new Map();
    for(const {a,b} of this.connections)for(const [end,other] of [[a,b],[b,a]])if(selected.has(end.id))attached.set(`${end.id}:${end.port}`,components.get(other.id));
    const ends=new Map();
    for(const p of tubes){
      const pair=[0,1].map(i=>{
        let node=attached.get(`${p.id}:${i}`);
        if(!node){node={key:`${p.id}:${i}`,ids:[],edges:[],rank:Infinity};nodes.push(node);}
        node.rank=Math.min(node.rank,port(p,i).position.dot(axis));return node;
      });
      if(pair[0]===pair[1])return blocked(`Tube ${p.id.slice(0,8)} has both ends joined through an unselected rigid section. Include the parallel tubes on that alternate path; resizing would otherwise change an unselected tube or joint.`);
      const difference=axes.get(p.id);
      pair[0].edges.push({node:pair[1],difference});pair[1].edges.push({node:pair[0],difference:difference.clone().negate()});ends.set(p.id,pair);
    }
    // Prefer an attached rigid section over a free end. Rank by the lowest
    // mating endpoint along the positive dominant world axis, then stable ID.
    const ordered=nodes.filter(n=>n.edges.length).sort((a,b)=>Number(!a.ids.length)-Number(!b.ids.length)||a.rank-b.rank||a.key.localeCompare(b.key));
    const velocities=new Map(),anchors=[];
    for(const root of ordered)if(!velocities.has(root)){
      const free=!root.ids.length,queue=[root];
      velocities.set(root,free?root.edges[0].difference.clone().multiplyScalar(-.5):vec([0,0,0]));
      if(!free)anchors.push(root.key);
      while(queue.length){const node=queue.pop();for(const edge of node.edges){
        const expected=velocities.get(node).clone().add(edge.difference),existing=velocities.get(edge.node);
        if(existing&&existing.distanceTo(expected)>PARALLEL_TOLERANCE)return blocked(`Conflicting resize paths near rigid section ${edge.node.key.slice(0,8)}: the selected tubes require different translations of the same connected geometry.`);
        if(!existing){velocities.set(edge.node,expected);queue.push(edge.node);}
      }}
    }
    const minDelta=Math.max(...tubes.map(p=>MIN_LENGTH-p.length)),maxDelta=Math.min(...tubes.map(p=>MAX_LENGTH-p.length));
    if(minDelta===maxDelta)return blocked(`Cut-length limits leave no nonzero shared adjustment: selected cuts already span ${MIN_LENGTH}–${MAX_LENGTH} mm.`);
    return {locked:false,minDelta,maxDelta,axis:axis.toArray(),axisLabel:'XYZ'[dominant],anchors,
      tubes:tubes.map(p=>({id:p.id,velocity:velocities.get(ends.get(p.id)[0]).clone().addScaledVector(axes.get(p.id),.5).toArray()})),
      sections:nodes.filter(n=>n.ids.length&&velocities.has(n)).map(n=>({ids:n.ids,velocity:velocities.get(n).toArray()}))};
  }
  resizeTogether(ids,delta) {
    const plan=this.coordinatedLengthPlan(ids);
    if(plan.locked)throw Error(plan.reason);
    if(!Number.isFinite(delta)||delta<plan.minDelta||delta>plan.maxDelta)throw Error(`Shared adjustment must be ${plan.minDelta}–${plan.maxDelta} mm so every cut stays ${MIN_LENGTH}–${MAX_LENGTH} mm.`);
    if(delta===0)return;
    const next=clone(this.data()),pieces=new Map(next.pieces.map(p=>[p.id,p]));
    for(const section of plan.sections)for(const id of section.ids){const p=pieces.get(id);p.p=vec(p.p).addScaledVector(vec(section.velocity),delta).toArray();}
    for(const tube of plan.tubes){const p=pieces.get(tube.id);p.p=vec(p.p).addScaledVector(vec(tube.velocity),delta).toArray();p.length+=delta;}
    // Validate every socket stop, direction and cut before publishing anything.
    const checked=validate(next);this.pieces=checked.pieces;this.connections=checked.connections;
  }
  copy(ids) {this.data();return {pieces:clone(this.pieces.filter(p=>ids.has(p.id))),connections:clone(this.connections.filter(c=>ids.has(c.a.id)&&ids.has(c.b.id)))};}
  paste(data,offset=[80,0,80]) {
    data=new Design(data).data();
    const map=new Map(data.pieces.map(p=>[p.id,uid()]));
    const pieces=data.pieces.map(p=>({...clone(p),id:map.get(p.id),p:vec(p.p).add(vec(offset)).toArray()}));
    const connections=data.connections.map(c=>({id:uid(),a:{id:map.get(c.a.id),port:c.a.port},b:{id:map.get(c.b.id),port:c.b.port}}));
    const checked=new Design({pieces:[...this.pieces,...pieces],connections:[...this.connections,...connections]});
    this.pieces=checked.pieces;this.connections=checked.connections;
    return new Set(map.values());
  }
  materials() {return materialsSummary(this.pieces);}
  summary() {const {rows,total}=this.materials();return {rows:rows.map(p=>[p.type==='tube'?`Tube · ${p.length} mm`:materialName(p),p.count]),total};}
}
// Exact numeric cut lengths are the grouping key; presentation never changes identity.
export function materialName(row) {standardType(row);return CATALOG[row.type].name;}
export function materialsSummary(pieces) {
  const rows=new Map(),cuts=[];let references=0;
  for(const p of pieces){
    validatePiece(p);
    if(p.type==='person'){references++;continue;}
    const key=p.type==='tube'?`tube:${p.length}`:p.type;
    if(!rows.has(key))rows.set(key,{type:p.type,...(p.type==='tube'?{length:p.length}:{}),count:0});
    rows.get(key).count++;if(p.type==='tube')cuts.push(String(p.length));
  }
  // Valid physical cuts (80-3000 mm) have decimal, non-exponential strings.
  // Sum their decimal digits so repeated fractional cuts do not accumulate binary noise.
  const places=Math.max(0,...cuts.map(n=>(n.split('.')[1]||'').length));
  const digits=cuts.reduce((sum,n)=>{const [whole,fraction='']=n.split('.');return sum+BigInt(whole+fraction.padEnd(places,'0'));},0n).toString().padStart(places+1,'0');
  const total=Number(places?digits.slice(0,-places)+'.'+digits.slice(-places):digits);
  return {rows:[...rows.values()],total,count:pieces.length-references,references};
}
export function validate(data) {
  if(!data||data.format!=='pvc-studio'||data.version!==1||data.catalog!=='pvc-32-v1'||data.units!=='mm'||data.radius!==RADIUS)throw Error('Unsupported design. Expected PVC Studio v1, pvc-32-v1 catalog, millimetres and 32 mm tubes.');
  if(!Array.isArray(data.pieces)||!Array.isArray(data.connections)||data.pieces.length>2000||data.connections.length>6000)throw Error('Invalid design arrays or design exceeds 2,000 pieces / 6,000 joints.');
  const ids=new Set();
  for(const p of data.pieces){validatePiece(p);if(typeof p.id!=='string'||!p.id||p.id.length>100||ids.has(p.id))throw Error('Missing or duplicate piece ID.');ids.add(p.id);}
  const model=Object.create(Design.prototype),jointIds=new Set();model.pieces=clone(data.pieces).map(p=>p.type==='person'?{...p,...personProperties(p)}:p);model.connections=[];
  for(const c of data.connections){if(!c||typeof c.id!=='string'||!c.id||c.id.length>100||jointIds.has(c.id)||ids.has(c.id))throw Error('Missing or duplicate joint ID.');jointIds.add(c.id);
    if(Object.keys(c).some(k=>!['id','a','b'].includes(k)))throw Error('Unsupported joint override.');
    for(const e of [c.a,c.b])if(!e||!ids.has(e.id)||!Number.isInteger(e.port)||e.port<0||e.port>=localPorts(model.get(e.id)).length)throw Error('Joint refers to an invalid piece or port.');
    model.check(c.a,c.b);model.connections.push(clone(c));}
  return model;
}
export function rectangle() {
  const m=new Design(), elbows=[];
  for(const [x,z,angle] of [[-300,-200,0],[300,-200,-Math.PI/2],[300,200,Math.PI],[-300,200,Math.PI/2]])elbows.push(m.add('elbow90',[x,60,z],400,new Quaternion().setFromAxisAngle(vec([0,1,0]),angle).toArray()));
  for(let i=0;i<4;i++){const a=elbows[i],b=elbows[(i+1)%4];const dir=vec(b.p).sub(vec(a.p)).normalize();const t=m.add('tube',vec(a.p).add(vec(b.p)).multiplyScalar(.5).toArray(),vec(a.p).distanceTo(vec(b.p))-50,new Quaternion().setFromUnitVectors(vec([1,0,0]),dir).toArray());
    const ai=localPorts(a).findIndex((_,j)=>port(a,j).direction.dot(dir)>.999),bi=localPorts(b).findIndex((_,j)=>port(b,j).direction.dot(dir)<-.999);
    m.connect({id:t.id,port:0},{id:a.id,port:ai},false);m.connect({id:t.id,port:1},{id:b.id,port:bi},false);}
  return m;
}
