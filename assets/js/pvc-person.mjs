// Configurable application limits, not medical or demographic definitions.
// All persisted dimensions are millimetres; both silhouettes share these limits.
export const PERSON_LIMITS=Object.freeze({
  adult:Object.freeze({label:'Adult',min:1400,max:2200,default:1800}),
  child:Object.freeze({label:'Child',min:600,max:1700,default:1200})
});
export const PERSON_VARIANTS=Object.freeze({man:'Man',woman:'Woman'});
export const PERSON_DEFAULTS=Object.freeze({category:'adult',variant:'man',height:PERSON_LIMITS.adult.default});
export const PERSON_STEP=10;
// Only absent properties receive defaults. Invalid supplied values are errors.
// A missing height uses the chosen category's default (Adult 1800 / Child 1200).
export function personProperties(piece){
  const category=Object.hasOwn(piece,'category')?piece.category:PERSON_DEFAULTS.category;
  const variant=Object.hasOwn(piece,'variant')?piece.variant:PERSON_DEFAULTS.variant;
  if(typeof category!=='string'||!Object.hasOwn(PERSON_LIMITS,category))throw Error('Unsupported Person category. Choose Adult or Child.');
  if(typeof variant!=='string'||!Object.hasOwn(PERSON_VARIANTS,variant))throw Error('Unsupported Person silhouette. Choose Man or Woman.');
  const limits=PERSON_LIMITS[category],height=Object.hasOwn(piece,'height')?piece.height:limits.default;
  if(!Number.isFinite(height)||height<limits.min||height>limits.max)throw Error(`Person height must be ${limits.min}–${limits.max} mm for ${limits.label}.`);
  return {category,variant,height};
}
export function personCategoryChange(piece,category){
  if(typeof category!=='string'||!Object.hasOwn(PERSON_LIMITS,category))throw Error('Unsupported Person category. Choose Adult or Child.');
  const current=personProperties(piece),limits=PERSON_LIMITS[category];
  return {...current,category,height:Math.min(limits.max,Math.max(limits.min,current.height))};
}
