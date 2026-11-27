// Placement is a pure query: no temporary pieces, IDs, history or mesh allocation.
import {localPorts,port,quat,compatiblePorts,portAlignment} from './pvc-model.mjs';
// CSS screen pixels, never world units or drawing-buffer/device pixels.
export const SNAP_PIXELS=192, SWITCH_MARGIN=12;
const ANGLE_EPSILON=1e-8;
const finiteVector=v=>v&&[v.x,v.y,v.z].every(Number.isFinite);
export function placementTargets(model) {
  const occupied=new Set(model.connections.flatMap(c=>[c.a,c.b].map(e=>JSON.stringify([e.id,e.port]))));
  return model.pieces.flatMap(p=>localPorts(p).flatMap((_,i)=>occupied.has(JSON.stringify([p.id,i]))?[]:[{target:{id:p.id,port:i},...port(p,i)}]));
}
export function alignPlacement(piece,source,target) {
  if(!Array.isArray(piece.p)||piece.p.length!==3||!piece.p.every(Number.isFinite)||
    !Array.isArray(piece.q)||piece.q.length!==4||!piece.q.every(Number.isFinite)||
    !finiteVector(target.position)||!finiteVector(target.direction))return null;
  const intended=quat(piece.q),orientationLength=intended.length(),directionLength=target.direction.length();
  if(!Number.isFinite(orientationLength)||orientationLength<1e-12||Math.abs(directionLength-1)>1e-8)return null;
  intended.normalize();
  // The shortest swing is the closest quaternion to the user's independent
  // intent that makes this source oppose the target. It preserves axial roll;
  // Three.js chooses a deterministic perpendicular axis for a 180-degree swing.
  const originPiece={...piece,p:[0,0,0],q:intended.toArray()};
  const t=portAlignment(port(originPiece,source),target);
  const q=t.rotation.clone().multiply(intended).normalize().toArray();
  // Compute from the mating datum, independent of the free-plane position. This
  // also avoids rounding drift when a native drop rounds pointer coordinates.
  const p=target.position.clone().sub(port({...originPiece,q},source).position).toArray();
  return [...p,...q].every(Number.isFinite)&&p.every(n=>Math.abs(n)<1e7)?{p,q,turn:t.rotation.angleTo(quat([0,0,0,1]))}:null;
}
// Coordinates and distances are CSS pixels, independent of DPR, zoom and projection.
export function projectPort(position,camera,rect) {
  if(![rect.left,rect.top,rect.width,rect.height].every(Number.isFinite)||rect.width<=0||rect.height<=0)return null;
  const view=position.clone().applyMatrix4(camera.matrixWorldInverse);
  const ndc=position.clone().project(camera);
  if(![view.x,view.y,view.z,ndc.x,ndc.y,ndc.z].every(Number.isFinite)||view.z>=0||ndc.z < -1||ndc.z > 1)return null;
  const x=rect.left+(ndc.x+1)*rect.width/2,y=rect.top+(1-ndc.y)*rect.height/2;
  return [x,y].every(Number.isFinite)?{x,y,depth:-view.z}:null;
}
const sameTarget=(a,b)=>a?.id===b?.id&&a?.port===b?.port;
export function choosePlacement({piece,targets,pointer,project,previous=null,visible=()=>true}) {
  if(!pointer||![pointer.x,pointer.y].every(Number.isFinite))return null;
  const sources=localPorts(piece).map((definition,i)=>({i,...definition}));
  const choices=[];
  for(const target of targets){
    const screen=project(target.position);if(!screen)continue;
    if(![screen.x,screen.y,screen.depth].every(Number.isFinite)||screen.depth<=0)continue;
    const distance=Math.hypot(screen.x-pointer.x,screen.y-pointer.y);
    if(distance>SNAP_PIXELS+1e-9)continue;
    // Evaluate every compatible source, even when it initially points away.
    // Free-plane position must not affect orientation ties as the pointer moves.
    const variants=sources.filter(source=>compatiblePorts(source,target)).map(source=>{
      const aligned=alignPlacement(piece,source.i,target);if(!aligned)return null;
      return {...aligned,source:source.i};
    }).filter(Boolean);
    if(!variants.length)continue;
    const minimum=Math.min(...variants.map(v=>v.turn));
    const closest=variants.filter(v=>v.turn<=minimum+ANGLE_EPSILON);
    const retained=closest.find(v=>sameTarget(previous?.target,target.target)&&v.source===previous.source);
    const variant=retained||closest[0];
    choices.push({...variant,target:target.target,distance,screen,depth:screen.depth,visible:visible(target)});
  }
  // Distance dominates, including subpixel neighbours. Numerically equal
  // distances prefer visible/frontmost ports and stable endpoint IDs.
  choices.sort((a,b)=>Math.round(a.distance*1e6)-Math.round(b.distance*1e6)||Number(b.visible)-Number(a.visible)||a.depth-b.depth||a.target.id.localeCompare(b.target.id)||a.target.port-b.target.port);
  const best=choices[0];if(!best)return null;
  const current=choices.find(c=>sameTarget(c.target,previous?.target));
  if(!current)return best;
  const separation=Math.hypot(current.screen.x-best.screen.x,current.screen.y-best.screen.y);
  // Close ports remain switchable. Exact overlaps use visibility/depth/ID order,
  // rather than allowing history to hide the preferred coincident endpoint.
  const margin=Math.min(SWITCH_MARGIN,separation/2);
  return separation>1e-6&&(current.visible||!best.visible)&&current.distance<=best.distance+margin?current:best;
}
