// Placement is a pure query: no temporary pieces, IDs, history or mesh allocation.
import {localPorts,port,quat,compatiblePorts,portAlignment} from './pvc-model.mjs';
export const SNAP_PIXELS=64, SWITCH_MARGIN=12;
export function placementTargets(model) {
  const occupied=new Set(model.connections.flatMap(c=>[c.a,c.b].map(e=>JSON.stringify([e.id,e.port]))));
  return model.pieces.flatMap(p=>localPorts(p).flatMap((_,i)=>occupied.has(JSON.stringify([p.id,i]))?[]:[{target:{id:p.id,port:i},...port(p,i)}]));
}
export function alignPlacement(piece,source,target) {
  const t=portAlignment(port(piece,source),target);
  const q=t.rotation.clone().multiply(quat(piece.q)).normalize().toArray();
  // Compute from the mating datum, independent of the free-plane position. This
  // also avoids rounding drift when a native drop rounds pointer coordinates.
  const p=target.position.clone().sub(port({...piece,p:[0,0,0],q},source).position).toArray();
  return [...p,...q].every(Number.isFinite)?{p,q,turn:t.rotation.angleTo(quat([0,0,0,1]))}:null;
}
// Coordinates and distances are CSS pixels, independent of DPR, zoom and projection.
export function projectPort(position,camera,rect) {
  const view=position.clone().applyMatrix4(camera.matrixWorldInverse);
  const ndc=position.clone().project(camera);
  if(![view.x,view.y,view.z,ndc.x,ndc.y,ndc.z].every(Number.isFinite)||view.z>=0||ndc.z < -1||ndc.z > 1)return null;
  return {x:rect.left+(ndc.x+1)*rect.width/2,y:rect.top+(1-ndc.y)*rect.height/2,depth:-view.z};
}
const sameTarget=(a,b)=>a?.id===b?.id&&a?.port===b?.port;
export function choosePlacement({piece,targets,pointer,project,previous=null,visible=()=>true}) {
  const sources=localPorts(piece).map((_,i)=>({i,...port(piece,i)}));
  const choices=[];
  for(const target of targets){
    if(!compatiblePorts(sources[0],target))continue;
    const screen=project(target.position);if(!screen)continue;
    const distance=Math.hypot(screen.x-pointer.x,screen.y-pointer.y);
    if(distance>SNAP_PIXELS)continue;
    // At one target, prefer the port requiring the least change of intended orientation.
    // Prospective port distance resolves equal rotations, never the component centre.
    const variants=sources.map(source=>{
      const aligned=alignPlacement(piece,source.i,target);if(!aligned)return null;
      const s=project(source.position),reach=s?Math.hypot(s.x-screen.x,s.y-screen.y):Infinity;
      return {...aligned,source:source.i,reach};
    }).filter(Boolean).sort((a,b)=>a.turn-b.turn||a.reach-b.reach||a.source-b.source);
    if(!variants.length)continue;
    let variant=variants[0];
    const retained=variants.find(v=>sameTarget(previous?.target,target.target)&&v.source===previous.source);
    if(retained&&retained.turn<=variant.turn+1e-6)variant=retained;
    choices.push({...variant,target:target.target,distance,depth:screen.depth,visible:visible(target)});
  }
  // Distance dominates; subpixel overlaps prefer visible/frontmost ports and stable IDs.
  choices.sort((a,b)=>Math.round(a.distance)-Math.round(b.distance)||Number(b.visible)-Number(a.visible)||a.depth-b.depth||a.target.id.localeCompare(b.target.id)||a.target.port-b.target.port);
  const best=choices[0];if(!best)return null;
  const current=choices.find(c=>sameTarget(c.target,previous?.target));
  return current&&(current.visible||!best.visible)&&current.distance<=best.distance+SWITCH_MARGIN?current:best;
}
