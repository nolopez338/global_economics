// Bounds of rendered vertices only. No construction/model or camera dependencies.
import {Vector3, Matrix4, Quaternion} from '../vendor/three-0.170.0/three.module.js';

export const WORLD_AXES=[[1,0,0],[0,1,0],[0,0,1]];
export const ANGULAR_TOLERANCE=1e-5; // radians; numerical search resolution, NOT a global error bound
const dot=(a,b)=>a[0]*b[0]+a[1]*b[1]+a[2]*b[2];
const sub=(a,b)=>a.map((v,i)=>v-b[i]);
const cross=(a,b)=>[a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0]];
const norm=a=>{const n=Math.hypot(...a);return n>1e-14?a.map(v=>v/n):null;};

// Group geometry is immutable in PVC Studio; length edits replace the group.
// Cache vertices AFTER nested transforms, BEFORE the piece's world transform.
export class GeometryVertices {
  constructor(){this.local=new WeakMap();this.world=new WeakMap();}
  collect(groups){
    const chunks=[],seeds=[];let count=0;
    for(const group of groups){
      group.updateWorldMatrix(true,true);
      let local=this.local.get(group);
      if(!local){
        const inverse=group.matrixWorld.clone().invert(),unique=new Map(),v=new Vector3();
        group.traverseVisible(o=>{if(!o.isMesh)return;const p=o.geometry.getAttribute('position'),m=new Matrix4().multiplyMatrices(inverse,o.matrixWorld);
          for(let i=0;i<p.count;i++){v.fromBufferAttribute(p,i).applyMatrix4(m);unique.set(v.toArray().join(','),v.toArray());}
        });
        local=new Float64Array([...unique.values()].flat());this.local.set(group,local);
      }
      const key=group.matrixWorld.elements.join(',');let cached=this.world.get(group);
      if(cached?.key!==key){const points=new Float64Array(local.length),v=new Vector3();
        for(let i=0;i<local.length;i+=3){v.fromArray(local,i).applyMatrix4(group.matrixWorld).toArray(points,i);}cached={key,points};this.world.set(group,cached);
      }
      chunks.push(cached.points);count+=cached.points.length;
      const q=group.getWorldQuaternion(new Quaternion()).normalize();seeds.push(WORLD_AXES.map(a=>new Vector3(...a).applyQuaternion(q).toArray()));
    }
    const points=new Float64Array(count);let offset=0;for(const chunk of chunks){points.set(chunk,offset);offset+=chunk.length;}
    return {points,seeds};
  }
}

export function fitBox(points,axes=WORLD_AXES){
  if(!points.length)return null;
  const origin=Array.from(points.slice(0,3)),lo=[Infinity,Infinity,Infinity],hi=[-Infinity,-Infinity,-Infinity];
  for(let i=0;i<points.length;i+=3){const x=points[i]-origin[0],y=points[i+1]-origin[1],z=points[i+2]-origin[2];
    for(let a=0;a<3;a++){const d=x*axes[a][0]+y*axes[a][1]+z*axes[a][2];lo[a]=Math.min(lo[a],d);hi[a]=Math.max(hi[a],d);}}
  const size=hi.map((n,i)=>Math.max(0,n-lo[i])),center=[...origin];
  for(let a=0;a<3;a++)for(let j=0;j<3;j++)center[j]+=axes[a][j]*(lo[a]+hi[a])/2;
  return {center,axes:axes.map(a=>[...a]),size,volume:size[0]*size[1]*size[2]};
}

// Deterministic QuickHull reduction. Near-coplanar points within 1e-10 of the
// normalized diameter can be dropped here; final fits ALWAYS use every vertex.
export function hullVertices(flat){
  const unique=new Map();for(let i=0;i<flat.length;i+=3){const p=Array.from(flat.slice(i,i+3));unique.set(p.join(','),p);}
  const p=[...unique.values()],eps=1e-10;if(p.length<5)return p.flat();
  const a=p.reduce((a,v,i)=>v[0]<p[a][0]?i:a,0);
  const far=distance=>p.reduce((best,v,i)=>distance(v)>best.d?{i,d:distance(v)}:best,{i:a,d:-1});
  const b=far(v=>dot(sub(v,p[a]),sub(v,p[a]))).i,line=sub(p[b],p[a]);
  if(Math.hypot(...line)<eps)return [...p[a]];
  const c=far(v=>Math.hypot(...cross(line,sub(v,p[a])))).i,n=norm(cross(line,sub(p[c],p[a])));
  if(!n)return p.flat(); // linear: retain original points, no fragile hull
  const d=far(v=>Math.abs(dot(n,sub(v,p[a])))).i;
  if(Math.abs(dot(n,sub(p[d],p[a])))<eps)return p.flat();
  const inside=[0,1,2].map(j=>(p[a][j]+p[b][j]+p[c][j]+p[d][j])/4);
  const face=(a,b,c)=>{let normal=norm(cross(sub(p[b],p[a]),sub(p[c],p[a])));if(!normal)return null;
    if(dot(normal,sub(inside,p[a]))>0){[b,c]=[c,b];normal=normal.map(v=>-v);}return {v:[a,b,c],n:normal,out:[]};};
  let faces=[[a,b,c],[a,d,b],[b,d,c],[c,d,a]].map(v=>face(...v));
  if(faces.some(f=>!f))return p.flat(); // extremely thin tetrahedron
  const assign=(ids,to)=>{for(const id of ids){let best=null,distance=eps;for(const f of to){const v=dot(f.n,sub(p[id],p[f.v[0]]));if(v>distance){best=f;distance=v;}}if(best)best.out.push(id);}};
  assign(p.map((_,i)=>i).filter(i=>![a,b,c,d].includes(i)),faces);
  for(let f;(f=faces.find(f=>f.out.length));){
    const eye=f.out.reduce((best,i)=>dot(f.n,sub(p[i],p[f.v[0]]))>dot(f.n,sub(p[best],p[f.v[0]]))?i:best,f.out[0]);
    const visible=faces.filter(f=>dot(f.n,sub(p[eye],p[f.v[0]]))>eps),edges=new Map(),outside=new Set();
    for(const f of visible){for(const id of f.out)if(id!==eye)outside.add(id);for(let i=0;i<3;i++){const a=f.v[i],b=f.v[(i+1)%3],reverse=`${b},${a}`;if(edges.has(reverse))edges.delete(reverse);else edges.set(`${a},${b}`,[a,b]);}}
    const added=[...edges.values()].map(([a,b])=>face(a,b,eye)).filter(Boolean);
    faces=faces.filter(f=>!visible.includes(f));assign(outside,added);faces.push(...added);
  }
  return [...new Set(faces.flatMap(f=>f.v))].sort((a,b)=>a-b).flatMap(i=>p[i]);
}

function principalAxes(points){
  const mean=[0,0,0],n=points.length/3;for(let i=0;i<points.length;i++)mean[i%3]+=points[i]/n;
  const m=Array.from({length:3},()=>[0,0,0]),v=WORLD_AXES.map(a=>[...a]);
  for(let i=0;i<points.length;i+=3)for(let a=0;a<3;a++)for(let b=0;b<3;b++)m[a][b]+=(points[i+a]-mean[a])*(points[i+b]-mean[b]);
  for(let k=0;k<32;k++){let a=0,b=1;for(const [i,j] of [[0,2],[1,2]])if(Math.abs(m[i][j])>Math.abs(m[a][b])){a=i;b=j;}if(Math.abs(m[a][b])<1e-15)break;
    const t=.5*Math.atan2(2*m[a][b],m[b][b]-m[a][a]),c=Math.cos(t),s=Math.sin(t);
    for(let j=0;j<3;j++){const x=m[a][j],y=m[b][j];m[a][j]=c*x-s*y;m[b][j]=s*x+c*y;}
    for(let i=0;i<3;i++){const x=m[i][a],y=m[i][b];m[i][a]=c*x-s*y;m[i][b]=s*x+c*y;const u=v[i][a],w=v[i][b];v[i][a]=c*u-s*w;v[i][b]=s*u+c*w;}
  }
  return [0,1,2].map(j=>v.map(row=>row[j]));
}
const matrix=axes=>new Matrix4().makeBasis(...axes.map(a=>new Vector3(...a)));
const qAxes=q=>WORLD_AXES.map(a=>new Vector3(...a).applyQuaternion(q).toArray());
function canonical(axes){
  // Box axes may be signed/permuted without changing the box. Pick the
  // right-handed equivalent closest to world XYZ; lexicographic ties are fixed.
  let best=null,score=-Infinity;
  for(const order of [[0,1,2],[0,2,1],[1,0,2],[1,2,0],[2,0,1],[2,1,0]])for(const x of [-1,1])for(const y of [-1,1]){
    const a=axes[order[0]].map(v=>v*x),b=axes[order[1]].map(v=>v*y),c=cross(a,b),candidate=[a,b,c],s=a[0]+b[1]+c[2];
    if(s>score+1e-12){score=s;best=candidate;}
  }return best;
}

export function orientedBox(points,seeds=[]){
  const world=fitBox(points);if(!world)return null;
  const scale=Math.max(...world.size);if(scale<1e-12)return {...world,approximate:true};
  const normalized=Array.from(points,(v,i)=>(v-world.center[i%3])/scale),hull=hullVertices(normalized);
  // Full geometry is represented by its hull during search, then checked/refit
  // against every original vertex. PCA is one seed, never a minimum claim.
  const candidates=[],keys=new Set();
  const add=axes=>{axes=canonical(axes);const key=axes.flat().map(v=>v.toFixed(7)).join(',');if(keys.has(key))return;keys.add(key);const q=new Quaternion().setFromRotationMatrix(matrix(axes)).normalize();candidates.push({q,box:fitBox(hull,axes)});};
  add(WORLD_AXES);for(const axes of seeds)add(axes);add(principalAxes(normalized));
  // Uniform deterministic SO(3) coverage, plus all supplied piece frames.
  for(let i=0;i<96;i++){const u=(i+.5)/96,a=2*Math.PI*((i*.618033988749895)%1),b=2*Math.PI*((i*.414213562373095)%1);add(qAxes(new Quaternion(Math.sqrt(1-u)*Math.sin(a),Math.sqrt(1-u)*Math.cos(a),Math.sqrt(u)*Math.sin(b),Math.sqrt(u)*Math.cos(b))));}
  // Regularized volume provides a useful objective even for exactly planar or
  // linear inputs. Epsilon is 1e-10 of the world's largest extent.
  const objective=box=>box.size.reduce((p,v)=>p*(v+1e-10),1);
  candidates.sort((a,b)=>objective(a.box)-objective(b.box));
  const directions=[];for(let x=-1;x<=1;x++)for(let y=-1;y<=1;y++)for(let z=-1;z<=1;z++)if(x||y||z)directions.push(new Vector3(x,y,z).normalize());
  let best=world,evaluations=candidates.length,converged=true;
  const starts=candidates.slice(0,12);
  // Always refine the world and each distinct piece orientation as well.
  for(const axes of [WORLD_AXES,...seeds.slice(0,16)]){const q=new Quaternion().setFromRotationMatrix(matrix(axes));if(!starts.some(s=>Math.abs(s.q.dot(q))>1-1e-9))starts.push({q,box:fitBox(hull,axes)});}
  for(const start of starts){let q=start.q.clone(),box=start.box,score=objective(box),iterations=0;
    for(let step=Math.PI/12;step>=ANGULAR_TOLERANCE;){
      let next=null;for(const axis of directions){const trial=q.clone().multiply(new Quaternion().setFromAxisAngle(axis,step)).normalize(),b=fitBox(hull,qAxes(trial)),s=objective(b);evaluations++;if(s<score-1e-15&&(!next||s<next.score))next={q:trial,box:b,score:s};}
      if(next){q=next.q;box=next.box;score=next.score;}else step/=2;
      if(++iterations>450){converged=false;break;}
    }
    const full=fitBox(points,canonical(qAxes(q)));
    // Keep exact world axes on equivalent results; never return a larger box.
    if(full.volume<best.volume-Math.max(1e-12,world.volume*1e-10)||
      (world.volume<1e-12&&objective(full)<objective(best)-1e-14))best=full;
  }
  return {...best,approximate:true,angularTolerance:ANGULAR_TOLERANCE,converged,evaluations,hullPoints:hull.length/3};
}

export function boxCorners(box){return Array.from({length:8},(_,i)=>box.center.map((v,j)=>v+box.axes.reduce((sum,a,k)=>sum+a[j]*box.size[k]*((i>>k)&1?.5:-.5),0)));}
export const BOX_EDGES=Array.from({length:3},(_,axis)=>Array.from({length:8},(_,i)=>i).filter(i=>!((i>>axis)&1)).map(i=>({axis,a:i,b:i|(1<<axis)}))).flat();
