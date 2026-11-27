// Floor-level geometry example; no elevated furniture or structural claims.
import {rectangle,Design,validate,vec} from './pvc-model.mjs';
export const TEMPLATES=Object.freeze([
  {id:'empty',name:'Empty',description:'Clear the workspace.',dimensions:''},
  {id:'ground',name:'Ground footprint study',description:'Four floor-contact elbows distribute support across a broad, low footprint; short rails span between them. Use a level surface, with no legs, elevated loads or cantilevers. This unbraced rectangle can rack in either horizontal direction and is not a furniture support.',dimensions:'Approximately 64 × 44 cm footprint; 550 and 350 mm cuts.'}
]);
export function buildTemplate(id) {
  if(id==='empty')return new Design();
  if(id!=='ground')throw Error('Unavailable template. Elevated furniture templates were removed because their support and bracing require unavailable junctions.');
  const m=rectangle();m.transform(new Set(m.pieces.map(p=>p.id)),undefined,undefined,vec([0,-38,0]));
  return validate(m.data());
}
