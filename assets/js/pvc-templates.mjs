// Structural pattern studies built entirely from unchanged catalog sockets.
import {Quaternion} from '../vendor/three-0.170.0/three.module.js';
import {Design,CATALOG,validate,vec,port} from './pvc-model.mjs';

export const TEMPLATES=Object.freeze([
  {id:'ground',name:'1 · Perimeter loop',description:'A four-corner floor-level footprint with short rails supported at the elbows. A basic closed load path; the unbraced rectangle can rack and supplies no elevated support.',dimensions:'Approximately 64 × 44 cm footprint.'},
  {id:'ladder',name:'2 · Ladder frame',description:'Parallel side rails and three transverse rungs distribute support along a long footprint and shorten crosswise spans. The open rectangular bays can still rack; this is not a climbing ladder.',dimensions:'Approximately 124 × 54 cm footprint.'},
  {id:'grid',name:'3 · Two-axis grillage',description:'A central four-port cross joins intersecting rails into four bays. Loads have paths in both horizontal directions and shorter spans; no deck or diagonal restraint is assumed.',dimensions:'Approximately 104 × 84 cm footprint.'},
  {id:'portal',name:'4 · Wide-base portal',description:'Two uprights carry one overhead rail into a closed ground perimeter. Fore-and-aft feet distribute the upright reactions. The open portal and base are unbraced, so socket rotation and lateral sway remain possible.',dimensions:'Approximately 84 × 64 × 94 cm (W × D × H).'},
  {id:'box',name:'5 · Closed space cell',description:'Eight three-way corners connect top and bottom perimeters through four columns. The spatial loop distributes reactions to four corners; its rectangular faces have no diagonal restraint.',dimensions:'Approximately 104 × 64 × 84 cm (W × D × H).'},
  {id:'tower',name:'6 · Braced rectangular tower',description:'Exactly 1.30 × 0.40 × 2.20 m outside the rendered fittings. Rolled standard tees carry two separated width-height diagonals, opposing side diagonals, and lower/upper plan diagonals. Staggered intermediate ties shorten column spans. This geometry addresses sway and twisting, but long-brace flexure, socket slip and the narrow tipping footprint remain limitations; no stiffness or stability rating is implied.',dimensions:'Exact model envelope: 1.30 m W × 0.40 m D × 2.20 m H. Width-diagonal planes are 98 mm apart.'},
  {id:'bridge',name:'7 · Two-bay supported frame',description:'Six columns divide continuous upper and lower beams into two bays; transverse ties at mid-height link front and rear supports. Central reactions reduce beam spans, but the unbraced bays do not prevent sway.',dimensions:'Approximately 144 × 64 × 84 cm (W × D × H).'},
  {id:'gable',name:'8 · Gabled prism',description:'Two closed five-sided end frames carry inclined roof rails through 45° eaves and 90° ridges. Transverse purlins connect tees on the slopes and posts. This demonstrates pitched load paths; purlins alone do not brace longitudinal sway or socket rotation.',dimensions:'Approximately 124 × 84 × 112 cm (W × D × H). No roof covering is included.'},
  {id:'lframe',name:'9 · Re-entrant space frame',description:'An L-shaped top and base follow a re-entrant footprint with six columns. Two noncrossing horizontal diagonal ties couple its wings in plan. Uneven loading can twist the inner corner; vertical faces remain unbraced.',dimensions:'Approximately 124 × 104 × 84 cm (W × D × H).'},
  {id:'octagon',name:'10 · Polygonal ring cell',description:'Two octagonal hoops connect through eight columns attached to straight rail tees. Four radial ties meet a standard cross at mid-height, linking opposite supports without unconnected crossings. Distributed perimeter reactions and radial ties restrain plan distortion; the vertical bays remain unbraced.',dimensions:'Approximately 132 × 132 × 94 cm (W × D × H).'}
].map(Object.freeze));

// Match a rigid rotation of a complete standard fitting, never a port override.
// A tee's run can remain on a rail while its perpendicular branch rolls into
// any plane through that rail: diagonals need no altered socket angles.
function fitting(directions) {
  for(const [type,def] of Object.entries(CATALOG)) {
    if(!def.ports||def.ports.length!==directions.length)continue;
    const source=def.ports.map(p=>vec(p.direction));
    for(const a of directions)for(const b of directions){
      const q=new Quaternion().setFromUnitVectors(source[0],a);
      const second=source.find(s=>Math.abs(s.dot(source[0]))<.9999)||source[1];
      const u=second.clone().applyQuaternion(q);u.addScaledVector(a,-u.dot(a));
      const v=b.clone().addScaledVector(a,-b.dot(a));
      if(u.length()>1e-7&&v.length()>1e-7){
        u.normalize();v.normalize();q.premultiply(new Quaternion().setFromAxisAngle(a,Math.atan2(a.dot(u.clone().cross(v)),u.dot(v))));
      }
      if(source.every(s=>directions.some(d=>s.clone().applyQuaternion(q).distanceTo(d)<1e-7)))return {type,q:q.normalize().toArray()};
    }
  }
  throw Error('Template junction cannot be assembled with a standard fitting.');
}
class Frame {
  constructor(){this.nodes=new Map();this.edges=[];}
  node(p){const key=p.map(n=>n.toFixed(7)).join(',');if(!this.nodes.has(key))this.nodes.set(key,{p:[...p],neighbors:[]});return this.nodes.get(key);}
  line(points){for(let i=1;i<points.length;i++){
    const a=this.node(points[i-1]),b=this.node(points[i]);
    if(a===b||a.neighbors.includes(b))throw Error('Duplicate template member.');
    a.neighbors.push(b);b.neighbors.push(a);this.edges.push([a,b]);
  }}
  build(){
    const m=new Design();
    for(const n of this.nodes.values()){
      const fit=fitting(n.neighbors.map(b=>vec(b.p).sub(vec(n.p)).normalize()));n.piece=m.add(fit.type,n.p,400,fit.q);
    }
    for(const [a,b] of this.edges){
      const axis=vec(b.p).sub(vec(a.p)).normalize(),length=vec(a.p).distanceTo(vec(b.p))-50;
      const t=m.add('tube',vec(a.p).add(vec(b.p)).multiplyScalar(.5).toArray(),length,new Quaternion().setFromUnitVectors(vec([1,0,0]),axis).toArray());
      for(const [end,n,dir] of [[0,a,axis],[1,b,axis.clone().negate()]]){
        const index=CATALOG[n.piece.type].ports.findIndex((_,i)=>port(n.piece,i).direction.distanceTo(dir)<1e-7);
        m.connect({id:t.id,port:end},{id:n.piece.id,port:index},false);
      }
    }
    return validate(m.data());
  }
}
function perimeter(f,xs,zs,y=22){
  for(const z of [zs[0],zs.at(-1)])f.line(xs.map(x=>[x,y,z]));
  for(const x of [xs[0],xs.at(-1)])f.line(zs.map(z=>[x,y,z]));
}
function cell(f,xs,zs,ys){
  for(const y of ys)perimeter(f,xs,zs,y);
  for(const x of [xs[0],xs.at(-1)])for(const z of [zs[0],zs.at(-1)])f.line(ys.map(y=>[x,y,z]));
}
function ground(f){perimeter(f,[-300,300],[-200,200]);}
function ladder(f){
  const xs=[-600,-300,0,300,600],zs=[-250,250];perimeter(f,xs,zs);
  for(const x of xs.slice(1,-1))f.line(zs.map(z=>[x,22,z]));
}
function grid(f){
  const xs=[-500,0,500],zs=[-400,0,400];perimeter(f,xs,zs);
  f.line(xs.map(x=>[x,22,0]));f.line(zs.map(z=>[0,22,z]));
}
function portal(f){
  perimeter(f,[-400,400],[-300,0,300]);
  for(const x of [-400,400])f.line([[x,22,0],[x,922,0]]);
  f.line([[-400,922,0],[400,922,0]]);
}
function box(f){cell(f,[-500,500],[-300,300],[21,821]);}
function tower(f){
  const x=629,z=179,lo=21,hi=2179;
  // One brace tee on each depth rail; their two XY planes are 98 mm apart.
  for(const y of [lo,hi]){
    for(const a of [-x,x]){
      const braceZ=(y===lo?(a<0?-49:49):(a<0?49:-49));
      f.line([[a,y,-z],[a,y,braceZ],[a,y,z]]);
    }
    for(const b of [-z,z]){
      const braceX=(y===lo?(b<0?429:-429):(b<0?-429:429));
      f.line([[-x,y,b],[braceX,y,b],[x,y,b]]);
    }
  }
  for(const a of [-x,x])for(const b of [-z,z]){
    const levels=[lo,970,1100,hi];
    if((a<0&&b<0)||(a>0&&b>0))levels.push(200);
    if((a<0&&b>0)||(a>0&&b<0))levels.push(2000);
    f.line(levels.sort((a,b)=>a-b).map(y=>[a,y,b]));
  }
  for(const b of [-z,z])f.line([[-x,970,b],[x,970,b]]);
  for(const a of [-x,x])f.line([[a,1100,-z],[a,1100,z]]);
  for(const [a,b] of [
    [[-x,lo,-49],[x,hi,-49]],[[x,lo,49],[-x,hi,49]],
    [[-429,lo,z],[-429,hi,-z]],[[429,lo,-z],[429,hi,z]],
    [[-x,200,-z],[x,200,z]],[[-x,2000,z],[x,2000,-z]]
  ])f.line([a,b]);
}
function bridge(f){
  const xs=[-700,0,700],zs=[-300,300],ys=[21,821];
  for(const y of ys){for(const z of zs)f.line(xs.map(x=>[x,y,z]));for(const x of [-700,700])f.line(zs.map(z=>[x,y,z]));}
  for(const x of xs){for(const z of zs)f.line([21,421,821].map(y=>[x,y,z]));f.line(zs.map(z=>[x,421,z]));}
}
function gable(f){
  for(const z of [-400,400]){
    f.line([[-600,21,z],[600,21,z]]);
    for(const x of [-600,600])f.line([[x,21,z],[x,321,z],[x,521,z]]);
    f.line([[-600,521,z],[-300,821,z],[0,1121,z],[300,821,z],[600,521,z]]);
  }
  for(const x of [-600,600])for(const y of [21,321])f.line([[x,y,-400],[x,y,400]]);
  for(const x of [-300,300])f.line([[x,821,-400],[x,821,400]]);
}
function lframe(f){
  const outline=[[-600,-500],[600,-500],[600,0],[0,0],[0,500],[-600,500]];
  for(const y of [21,821])for(let i=0;i<outline.length;i++){
    const a=outline[i],b=outline[(i+1)%outline.length];f.line([[a[0],y,a[1]],[b[0],y,b[1]]]);
  }
  for(const [i,[x,z]] of outline.entries())f.line(([0,1,3,4].includes(i)?[21,421,821]:[21,821]).map(y=>[x,y,z]));
  // Noncrossing chords in the two wings. Each vertex uses one rolled tee.
  for(const [i,j] of [[1,3],[0,4]]){const a=outline[i],b=outline[j];f.line([[a[0],421,a[1]],[b[0],421,b[1]]]);}
}
function octagon(f){
  const r=650,h=r*Math.SQRT1_2,vertices=[[r,0],[h,h],[0,r],[-h,h],[-r,0],[-h,-h],[0,-r],[h,-h]],mid=[];
  for(let i=0;i<8;i++){const a=vertices[i],b=vertices[(i+1)%8];mid.push([(a[0]+b[0])/2,(a[1]+b[1])/2]);}
  for(const y of [22,922])for(let i=0;i<8;i++){
    const a=vertices[i],b=vertices[(i+1)%8],c=mid[i];f.line([[a[0],y,a[1]],[c[0],y,c[1]],[b[0],y,b[1]]]);
  }
  for(let i=0;i<8;i++){const [x,z]=mid[i];f.line((i%2===0?[22,472,922]:[22,922]).map(y=>[x,y,z]));}
  for(const i of [0,2,4,6]){const [x,z]=mid[i];f.line([[x,472,z],[0,472,0]]);}
}
const builders={ground,ladder,grid,portal,box,tower,bridge,gable,lframe,octagon};
export function buildTemplate(id){
  if(!Object.hasOwn(builders,id))throw Error('Unavailable template. Choose one of the ten structural patterns.');
  const f=new Frame();builders[id](f);return f.build();
}
