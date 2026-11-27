import * as THREE from '../vendor/three-0.170.0/three.module.js';
import {GeometryVertices,fitBox,boxCorners,BOX_EDGES} from './pvc-bounds.mjs';

const MODES=['Off','World-aligned box','Minimum-volume oriented box (approximate)'];
const overlap=(a,b)=>Math.max(0,Math.min(a.x+a.w,b.x+b.w)-Math.max(a.x,b.x))*Math.max(0,Math.min(a.y+a.h,b.y+b.h)-Math.max(a.y,b.y));
const clamp=(v,a,b)=>Math.max(a,Math.min(b,v));

export function projectBoundsPoint(point,camera,width,height){
  const v=new THREE.Vector3(...point).project(camera),view=new THREE.Vector3(...point).applyMatrix4(camera.matrixWorldInverse);
  return [v.x,v.y,v.z].every(Number.isFinite)&&view.z<-camera.near&&v.z>=-1&&v.z<=1?{x:(v.x+1)*width/2,y:(1-v.y)*height/2}:null;
}

export class BoundsOverlay {
  constructor({scene,workspace,button,announcement,format}){
    Object.assign(this,{scene,workspace,button,announcement,format});
    this.mode=0;this.cache=new GeometryVertices();this.key='';this.revision=0;this.edgeChoice=[];this.computations=0;
    this.geometry=new THREE.BufferGeometry();this.geometry.setAttribute('position',new THREE.BufferAttribute(new Float32Array(72),3));
    this.geometry.setAttribute('lineDistance',new THREE.BufferAttribute(new Float32Array(24),1));
    this.material=new THREE.LineDashedMaterial({color:0x376c78,dashSize:12,gapSize:8,transparent:true,opacity:.95,depthTest:false,depthWrite:false});
    this.lines=new THREE.LineSegments(this.geometry,this.material);this.lines.frustumCulled=false;this.lines.renderOrder=4;this.lines.visible=false;
    this.lines.raycast=()=>{};scene.add(this.lines);
    this.layer=document.createElement('div');this.layer.className='bounds-overlay';this.layer.hidden=true;this.layer.setAttribute('aria-hidden','true');
    this.leaders=document.createElementNS('http://www.w3.org/2000/svg','svg');this.layer.append(this.leaders);
    this.labels=Array.from({length:3},()=>{const node=document.createElement('span');node.className='bounds-dimension';this.layer.append(node);const line=document.createElementNS(this.leaders.namespaceURI,'line');this.leaders.append(line);return {node,line};});workspace.append(this.layer);
    this.cycle=()=>{this.mode=(this.mode+1)%3;this.updateControl();this.announcement.textContent=`Selection bounds: ${MODES[this.mode]}.`;this.key='';this.sync(this.selected,this.meshes);};
    button.addEventListener('click',this.cycle);this.updateControl();
  }
  updateControl(){
    const detail=this.mode!==2?'':this.state==='refining'?' Containing preview; refining.':this.state==='unavailable'?' Refinement unavailable; showing containing preview.':this.box?.converged===false?' Search iteration limit reached; no global error guarantee.':' Numerical search; no global error guarantee.';
    const text=`Selection bounds: ${MODES[this.mode]}. Next: ${MODES[(this.mode+1)%3]}.${detail}`;
    this.button.title=text;this.button.setAttribute('aria-label',text);this.button.dataset.mode=String(this.mode);
  }
  cancel(){clearTimeout(this.timer);this.timer=null;this.worker?.terminate();this.worker=null;}
  sync(selected=new Set(),meshes=new Map()){
    this.selected=selected;this.meshes=meshes;
    const groups=[...selected].sort().map(id=>meshes.get(id)).filter(Boolean);
    const key=this.mode+':'+groups.map(g=>g.uuid+':'+g.matrixWorld.elements.join(',')).join('|');
    if(key===this.key)return;this.key=key;this.cancel();this.revision++;this.projectionKey='';
    if(!this.mode||!groups.length){this.box=null;this.state=null;this.lines.visible=false;this.layer.hidden=true;this.points=null;this.updateControl();return;}
    const {points,seeds}=this.cache.collect(groups);this.points=points;
    const world=fitBox(points);if(!world)return;
    // Every live preview contains the CURRENT vertices. A previous orientation
    // is reusable, but its old center/extents are never reused.
    const previous=this.mode===2&&this.box?fitBox(points,this.box.axes):null;
    this.setBox(previous&&previous.volume<world.volume?previous:world,this.mode===2?'refining':'world');
    if(this.mode===2){const revision=this.revision;
      this.timer=setTimeout(()=>{
        this.timer=null;
        try{
          const worker=new Worker(new URL('./pvc-bounds-worker.mjs',import.meta.url),{type:'module'});this.worker=worker;this.computations++;
          worker.onmessage=({data})=>{if(revision!==this.revision)return;worker.terminate();this.worker=null;
            if(data.error){this.setBox(this.box,'unavailable');console.error('Bounds refinement:',data.error);return;}
            // A previous fitted orientation can occasionally beat this search.
            const previous=this.box,box=previous.volume<=data.box.volume*(1+1e-9)?{...data.box,center:previous.center,axes:previous.axes,size:previous.size,volume:previous.volume}:data.box;this.setBox(box,'approximate');
          };
          worker.onerror=()=>{if(revision!==this.revision)return;worker.terminate();this.worker=null;this.setBox(this.box,'unavailable');};
          const copy=points.slice();worker.postMessage({points:copy,seeds},[copy.buffer]);
        }catch{this.setBox(this.box,'unavailable');}
      },140);
    }
  }
  setBox(box,state){
    this.box=box;this.state=state;this.lines.visible=true;this.layer.hidden=false;this.projectionKey='';this.edgeChoice=[];
    this.updateControl();
    if(state==='unavailable')this.announcement.textContent='Oriented refinement unavailable. Showing containing selection bounds.';
    this.layer.dataset.state=state;
    const corners=boxCorners(box),position=this.geometry.getAttribute('position'),distance=this.geometry.getAttribute('lineDistance');
    // Center the Float32 line coordinates to avoid precision loss far from 0.
    this.lines.position.fromArray(box.center);
    BOX_EDGES.forEach(({a,b},i)=>{for(const [n,corner] of [[i*2,corners[a]],[i*2+1,corners[b]]])position.setXYZ(n,...corner.map((v,j)=>v-box.center[j]));distance.setX(i*2,0);distance.setX(i*2+1,new THREE.Vector3(...corners[a]).distanceTo(new THREE.Vector3(...corners[b])));});
    position.needsUpdate=true;distance.needsUpdate=true;this.material.dashSize=Math.max(...box.size)/55||1;this.material.gapSize=this.material.dashSize*.65;
  }
  project(camera){
    if(!this.box||!this.mode)return;
    camera.updateMatrixWorld(true);
    const w=this.workspace.clientWidth,h=this.workspace.clientHeight,text=this.box.size.map(this.format),key=[this.revision,this.state,w,h,this.workspace.dataset.mode,this.workspace.querySelector('#movement-bar')?.hidden,this.workspace.querySelector('#placement-bar')?.hidden,...camera.matrixWorld.elements,...camera.projectionMatrix.elements,...text].join(',');
    if(key===this.projectionKey)return;this.projectionKey=key;
    const corners=boxCorners(this.box),project=p=>projectBoundsPoint(p,camera,w,h);
    const projected=corners.map(project),valid=projected.filter(Boolean);
    if(!valid.length||valid.every(p=>p.x<0)||valid.every(p=>p.x>w)||valid.every(p=>p.y<0)||valid.every(p=>p.y>h)){this.layer.hidden=true;return;}this.layer.hidden=false;
    const center=project(this.box.center)||{x:w/2,y:h/2},eye=camera.isPerspectiveCamera?camera.position.clone().sub(new THREE.Vector3(...this.box.center)).normalize():camera.getWorldDirection(new THREE.Vector3()).negate();
    const anchors=[];
    for(let axis=0;axis<3;axis++){
      const candidates=BOX_EDGES.map((edge,index)=>({...edge,index})).filter(e=>e.axis===axis).flatMap(e=>{
        const mid=corners[e.a].map((v,j)=>(v+corners[e.b][j])/2),p=project(mid);if(!p)return [];
        const a=projected[e.a],b=projected[e.b],length=a&&b?Math.hypot(b.x-a.x,b.y-a.y):0;
        // Exterior edges border two faces. Favor front-facing faces, radial
        // separation, and non-collapsed projected edges; keep near ties stable.
        const faces=[];for(let j=0;j<3;j++)if(j!==axis)faces.push(new THREE.Vector3(...this.box.axes[j]).dot(eye)*((e.a>>j)&1?1:-1));
        const silhouette=faces[0]*faces[1]<=1e-8&&Math.max(...faces)>=-1e-8;
        const score=(silhouette?60:0)+(faces[0]+faces[1])*8+Math.max(...faces)*10+Math.hypot(p.x-center.x,p.y-center.y)*.25+Math.min(length,80)*.2;
        return [{...p,index:e.index,score,length}];
      }).sort((a,b)=>b.score-a.score||a.index-b.index);
      const old=candidates.find(c=>c.index===this.edgeChoice[axis]),chosen=old&&old.score>=candidates[0]?.score-15?old:candidates[0];
      this.edgeChoice[axis]=chosen?.index;anchors.push(chosen);
      const {node}=this.labels[axis];node.hidden=!chosen;node.textContent=`${(this.mode===1?'XYZ':'LWH')[axis]} ${text[axis]}`;
      node.title=this.mode===2?`Approximate oriented bounds · ${this.state==='refining'?'containing preview, refining':this.state==='unavailable'?'refinement unavailable':this.box.converged===false?'iteration limit reached; no global error guarantee':'target search resolution 0.000573°, no global error guarantee'}`:'World-axis extent';
    }
    const wr=this.workspace.getBoundingClientRect(),obstacles=[];
    for(const selector of ['.viewport-top','.viewport-bottom','#orientation','#movement-bar','#placement-bar']){
      const node=this.workspace.querySelector(selector);if(!node||node.hidden)continue;const r=node.getBoundingClientRect();if(r.width&&r.height)obstacles.push({x:r.left-wr.left-4,y:r.top-wr.top-4,w:r.width+8,h:r.height+8});
    }
    const options=anchors.map((anchor,i)=>{
      if(!anchor)return [];const node=this.labels[i].node,width=node.offsetWidth,height=node.offsetHeight;
      let dx=anchor.x-center.x,dy=anchor.y-center.y,n=Math.hypot(dx,dy);if(n<1){dx=0;dy=-1;n=1;}
      const directions=[[dx/n,dy/n],[0,-1],[1,0],[0,1],[-1,0]];
      return directions.flatMap(([x,y],j)=>[18,40,68,96].map(offset=>{
        const rawX=anchor.x+x*(offset+width*.25)-width/2,rawY=anchor.y+y*offset-height/2;
        const rect={x:clamp(rawX,8,w-width-8),y:clamp(rawY,38,h-height-42),w:width,h:height};
        return {...rect,cost:offset+j*4+Math.hypot(rect.x-rawX,rect.y-rawY)*2+obstacles.reduce((sum,o)=>sum+overlap(rect,o)*1000,0)};
      }));
    });
    // Only three labels: test all placement combinations rather than let an
    // early greedy choice force a collision in an orthographic/narrow view.
    let best=null;const search=(axis,rects,cost)=>{if(best&&cost>=best.cost)return;if(axis===3){best={rects,cost};return;}
      if(!options[axis].length){search(axis+1,[...rects,null],cost);return;}
      for(const r of options[axis])search(axis+1,[...rects,r],cost+r.cost+rects.reduce((sum,o)=>sum+(o?overlap({...r,x:r.x-3,y:r.y-3,w:r.w+6,h:r.h+6},o)*10000:0),0));
    };search(0,[],0);
    this.labels.forEach(({node,line},i)=>{const r=best?.rects[i],anchor=anchors[i];line.style.display=r?'':'none';if(!r)return;
      node.style.transform=`translate(${r.x}px,${r.y}px)`;
      const end={x:clamp(anchor.x,r.x,r.x+r.w),y:clamp(anchor.y,r.y,r.y+r.h)};
      for(const [name,value] of Object.entries({x1:anchor.x,y1:anchor.y,x2:end.x,y2:end.y}))line.setAttribute(name,value);
    });
  }
  dispose(){this.cancel();this.button.removeEventListener('click',this.cycle);this.scene.remove(this.lines);this.geometry.dispose();this.material.dispose();this.layer.remove();}
}
