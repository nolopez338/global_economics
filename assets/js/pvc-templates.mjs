// Geometric planning assemblies. Coordinates, sockets and physical cuts are mm.
import {Quaternion} from '../vendor/three-0.170.0/three.module.js';
import {Design,CATALOG,vec,port,validate} from './pvc-model.mjs';

export const TEMPLATES=Object.freeze([
  {id:'empty',name:'Empty',description:'Clear the workspace.',dimensions:''},
  {id:'window',name:'Window-ready box frame',description:'Upper half of the front stays clear for a future lightweight window panel. Mid-height sill, lower rails, back / side diagonals and four braced outriggers.',dimensions:'Main box ≈154 × 224 × 39 cm (W × H × D). Full footprint ≈154 × 109 cm; clear front opening ≈146 × 106 cm.'},
  {id:'shelving',name:'Reinforced shelving frame',description:'Four rail levels with central supports and triangulated back and sides. Add shelf panels separately.',dimensions:'≈134 × 169 × 59 cm (W × H × D).'},
  {id:'worktable',name:'Worktable frame',description:'Wide top perimeter with central support, lower rails and diagonals on the back and sides. Add a worktop separately.',dimensions:'≈134 × 94 × 69 cm (W × H × D).'},
  {id:'desk',name:'Compact desk frame',description:'Compact top frame with a clear front knee opening; rear and side reinforcement. Add a desktop separately.',dimensions:'≈114 × 74 × 59 cm (W × H × D).'},
  {id:'clothes',name:'Freestanding clothes rack',description:'Hanging rail, intermediate rear supports and braced base outriggers. No front intermediate crossbars.',dimensions:'≈114 × 169 × 59 cm body; full footprint ≈114 × 149 cm.'},
  {id:'shoes',name:'Shoe rack',description:'Three open rail tiers with center supports and back / side triangulation. Add shelf surfaces separately.',dimensions:'≈114 × 74 × 39 cm (W × H × D).'},
  {id:'plant',name:'Plant stand',description:'Two raised rail levels, lower rails, center supports, braced back / sides and outriggers for the narrow upright shape. Add trays separately.',dimensions:'≈74 × 114 × 59 cm body; full footprint ≈74 × 129 cm.'},
  {id:'hamper',name:'Laundry hamper frame',description:'Twin open top bays for removable fabric liners; lower support rails and back / side diagonals.',dimensions:'≈74 × 94 × 59 cm (W × H × D).'},
  {id:'display',name:'Freestanding display frame',description:'Clear upper front display area, mid-height rail, back / side triangulation and braced outriggers. Add a lightweight display panel separately.',dimensions:'≈134 × 199 × 49 cm body; full footprint ≈134 × 139 cm.'}
]);

// Match a junction to an existing catalog fitting whenever its socket layout permits.
function catalogFit(sockets) {
  if(sockets.some(s=>Math.abs(vec(s.position).length()-45)>1e-7))return null;
  const directions=sockets.map(s=>vec(s.direction));
  for(const [type,def] of Object.entries(CATALOG)) {
    if(type==='tube'||type==='multiway'||def.ports.length!==sockets.length)continue;
    for(const a of directions)for(const b of directions){
      const q=new Quaternion().setFromUnitVectors(vec(def.ports[0].direction),a);
      if(sockets.length>1){
        const source=vec(def.ports[1].direction).applyQuaternion(q);
        const u=source.clone().addScaledVector(a,-source.dot(a)),v=b.clone().addScaledVector(a,-b.dot(a));
        if(u.length()>1e-6&&v.length()>1e-6){u.normalize();v.normalize();const angle=Math.atan2(a.dot(u.clone().cross(v)),u.dot(v));q.premultiply(new Quaternion().setFromAxisAngle(a,angle));}
      }
      if(def.ports.every(s=>directions.some(d=>vec(s.direction).applyQuaternion(q).distanceTo(d)<1e-7)))return {type,q:q.toArray()};
    }
  }
  return null;
}

export function buildTemplate(id) {
  if(!TEMPLATES.some(t=>t.id===id))throw Error('Unknown template.');
  if(id==='empty')return new Design();
  const configs={window:[750,350,[0,550,1100,1650,2200],350],shelving:[650,550,[0,550,1100,1650],0],worktable:[650,650,[0,450,900],0],desk:[550,550,[0,350,700],0],clothes:[550,550,[0,550,1100,1650],450],shoes:[550,350,[0,350,700],0],plant:[350,550,[0,550,1100],350],hamper:[350,550,[0,450,900],0],display:[650,450,[0,650,1300,1950],450]};
  const [bay,depth,levels,feet]=configs[id],nodes=new Map(),edges=[];
  const front=depth/2,back=-front,xs=[-bay,0,bay],top=levels.at(-1);
  const node=p=>{const key=p.join(',');if(!nodes.has(key))nodes.set(key,{p:[p[0],p[1]+21,p[2]],edges:[]});return nodes.get(key);};
  const edge=(a,b,diagonal=false)=>{const na=node(a),nb=node(b);if(edges.some(e=>e.a===na&&e.b===nb||e.a===nb&&e.b===na))return;const e={a:na,b:nb,diagonal};edges.push(e);na.edges.push(e);nb.edges.push(e);};
  const open=['window','desk','clothes','display'].includes(id);
  const sill=id==='window'?1100:id==='display'?650:0;
  for(const z of [back,front]){
    for(const x of xs){
      // Upper front opening is uninterrupted; its center has no vertical post.
      if(z===front&&x===0&&open){if(sill)for(let i=1;i<levels.length&&levels[i]<=sill;i++)edge([x,levels[i-1],z],[x,levels[i],z]);continue;}
      for(let i=1;i<levels.length;i++)edge([x,levels[i-1],z],[x,levels[i],z]);
    }
    for(const y of levels){
      if(z===front&&open&&y!==0&&y!==top&&y!==sill)continue;
      for(let i=1;i<xs.length;i++)edge([xs[i-1],y,z],[xs[i],y,z]);
    }
  }
  for(const x of xs)for(const y of levels){
    if(x===0&&open&&y!==0&&y!==top&&y!==sill)continue;
    edge([x,y,back],[x,y,front]);
  }
  // Triangulate every rear bay and each side bay; never brace the front opening.
  for(let i=1;i<levels.length;i++){
    for(let j=1;j<xs.length;j++)edge([xs[j-1],levels[i-1],back],[xs[j],levels[i],back],true);
    for(const x of [-bay,bay])edge([x,levels[i-1],back],[x,levels[i],front],true);
  }
  if(feet)for(const x of [-bay,bay])for(const z of [back,front]){
    const tip=z+Math.sign(z)*feet;
    edge([x,0,z],[x,0,tip]);edge([x,0,tip],[x,levels[1],z],true);
  }
  // Diagonals use whole-mm cuts. Their socket necks absorb <0.25 mm rounding
  // at each end, preserving exact seating and 20 mm insertion, rather than gaps.
  for(const e of edges){const distance=vec(e.a.p).distanceTo(vec(e.b.p));e.length=e.diagonal?Math.round(distance-170):distance-50;e.stop=(distance-e.length)/2;}
  const m=new Design();
  for(const n of nodes.values()){
    n.sockets=n.edges.map(e=>{const other=e.a===n?e.b:e.a,dir=vec(other.p).sub(vec(n.p)).normalize().toArray();return {direction:dir,position:dir.map(v=>v*(e.stop+20)),type:'socket',insertion:20};});
    const fit=catalogFit(n.sockets);
    n.piece=fit?m.add(fit.type,n.p,400,fit.q):m.add('multiway',n.p,400,[0,0,0,1],n.sockets);
  }
  for(const e of edges){
    const direction=vec(e.b.p).sub(vec(e.a.p)).normalize(),mid=vec(e.a.p).add(vec(e.b.p)).multiplyScalar(.5);
    const t=m.add('tube',mid.toArray(),e.length,new Quaternion().setFromUnitVectors(vec([1,0,0]),direction).toArray());
    for(const [end,n,dir] of [[0,e.a,direction],[1,e.b,direction.clone().negate()]]){
      const index=n.piece.type==='multiway'?n.edges.indexOf(e):CATALOG[n.piece.type].ports.findIndex((_,i)=>port(n.piece,i).direction.distanceTo(dir)<1e-7);
      m.connect({id:t.id,port:end},{id:n.piece.id,port:index},false);
    }
  }
  return validate(m.data());
}
