// Isolated client-side PDF export. No live scene, controls, storage or history access.
import * as THREE from '../vendor/three-0.170.0/three.module.js';
import {validate,CATALOG,vec,quat,materialName} from './pvc-model.mjs';
import {geometry,dispose} from './pvc-geometry.mjs';

export const PDF_VIEWS=Object.freeze([
  {label:'Front',direction:[0,0,1],up:[0,1,0],axis:'+Z'},
  {label:'Back',direction:[0,0,-1],up:[0,1,0],axis:'-Z'},
  {label:'Left',direction:[-1,0,0],up:[0,1,0],axis:'-X'},
  {label:'Right',direction:[1,0,0],up:[0,1,0],axis:'+X'},
  {label:'Top',direction:[0,1,0],up:[0,0,-1],axis:'+Y; up = -Z'},
  {label:'Bottom',direction:[0,-1,0],up:[0,0,1],axis:'-Y; up = +Z'},
  {label:'Isometric front-right',direction:[1,1,1],up:[0,1,0],perspective:true},
  {label:'Isometric rear-left',direction:[-1,1,-1],up:[0,1,0],perspective:true}
]);
const pause=()=>new Promise(resolve=>setTimeout(resolve,0));
const lengths={mm:1,cm:10,m:1000};
export function pdfLength(n,unit){
  const [whole,fraction='']=String(n).split('.'),shift={mm:0,cm:1,m:3}[unit];
  const digits=(whole+fraction).padStart(whole.length+fraction.length+shift,'0'),point=digits.length-fraction.length-shift;
  const value=(digits.slice(0,point)||'0')+'.'+digits.slice(point);
  return `${value.replace(/^0+(?=\d)/,'').replace(/0+$/,'').replace(/\.$/,'')||'0'} ${unit}`;
}

// Fit all eight corners of world bounds in camera space, including perspective depth.
export function frameExportCamera(box,view,aspect){
  const center=box.getCenter(new THREE.Vector3()),radius=Math.max(box.getSize(new THREE.Vector3()).length()/2,1);
  const camera=view.perspective?new THREE.PerspectiveCamera(35,aspect,1,10000):new THREE.OrthographicCamera(-1,1,1,-1,1,10000);
  const direction=vec(view.direction).normalize();camera.up.copy(vec(view.up));camera.position.copy(center).add(direction);camera.lookAt(center);camera.updateMatrixWorld(true);
  const inverse=camera.quaternion.clone().invert(),corners=[];
  for(const x of [box.min.x,box.max.x])for(const y of [box.min.y,box.max.y])for(const z of [box.min.z,box.max.z])corners.push(new THREE.Vector3(x,y,z).sub(center).applyQuaternion(inverse));
  let distance=radius*3;
  if(view.perspective){const tangent=Math.tan(THREE.MathUtils.degToRad(camera.fov/2));distance=Math.max(...corners.flatMap(p=>[p.z+Math.abs(p.x)*1.18/(tangent*aspect),p.z+Math.abs(p.y)*1.18/tangent]),radius*1.2);}
  else{const half=Math.max(...corners.flatMap(p=>[Math.abs(p.y),Math.abs(p.x)/aspect]),1)*1.18;Object.assign(camera,{left:-half*aspect,right:half*aspect,top:half,bottom:-half});}
  camera.near=Math.max(.01,distance-radius*1.1);camera.far=distance+radius*1.5;
  camera.position.copy(center).addScaledVector(direction,distance);camera.lookAt(center);camera.updateProjectionMatrix();camera.updateMatrixWorld(true);return camera;
}

function exportRenderer(){
  const renderer=new THREE.WebGLRenderer({antialias:true,preserveDrawingBuffer:true});
  renderer.setPixelRatio(1);renderer.setClearColor(0xf1f5f5);renderer.outputColorSpace=THREE.SRGBColorSpace;
  renderer.toneMapping=THREE.ACESFilmicToneMapping;renderer.toneMappingExposure=1.05;
  return renderer;
}
function exportScene(){
  const scene=new THREE.Scene();scene.add(new THREE.HemisphereLight(0xffffff,0x718b91,2.4));
  const light=new THREE.DirectionalLight(0xffffff,3.2);light.position.set(500,1000,650);scene.add(light);
  const fill=new THREE.DirectionalLight(0xc9e2e8,1);fill.position.set(-500,-600,-400);scene.add(fill);
  return scene;
}
function capture(renderer,scene,group,view,width,height){
  renderer.setSize(width,height,false);group.updateWorldMatrix(true,true);
  const box=new THREE.Box3().setFromObject(group,true),camera=frameExportCamera(box,view,width/height);
  renderer.render(scene,camera);
  if(renderer.getContext().isContextLost())throw Error('The export graphics context was lost. Try again.');
  return renderer.domElement.toDataURL('image/png');
}
function text(doc,value,x,y,size=10,bold=false){doc.setFont('helvetica',bold?'bold':'normal');doc.setFontSize(size);doc.setTextColor(32,58,65);doc.text(value,x,y);}
function heading(doc,title,section,page,total=3){
  text(doc,'PVC STUDIO / DESIGN',12,14,9,true);text(doc,title,12,25,18,true);text(doc,section,12,36,11,true);
  doc.setDrawColor(209,223,225);doc.line(12,41,198,41);doc.setFontSize(9);doc.text(`${page} / ${total}`,198,289,{align:'right'});
}

// Fixed readable type and thumbnail sizes; measure wrapping before allocating any GPU resources.
export function materialsLayout(doc,rows,unit){
  for(const columns of [1,2]){
    const width=(186-(columns-1)*6)/columns,ref=22,name=columns===1?57:27,spec=width-ref-name-12;
    doc.setFont('helvetica','normal');doc.setFontSize(9);
    const measured=rows.map(row=>{
      const nameLines=doc.splitTextToSize(materialName(row),name-3);
      const specification=row.type==='tube'?`Cut ${pdfLength(row.length,unit)}\nOD ${pdfLength(32,unit)}`:`${CATALOG[row.type].ports.length} socket${CATALOG[row.type].ports.length===1?'':'s'}\nFor OD ${pdfLength(32,unit)}`;
      const specLines=doc.splitTextToSize(specification,spec-3);
      return {...row,nameLines,specLines,height:Math.max(16,Math.max(nameLines.length,specLines.length)*3.8+5)};
    });
    const groups=[[]];let height=0;
    for(const row of measured){if(height+row.height>204){groups.push([]);height=0;}groups.at(-1).push(row);height+=row.height;}
    if(groups.length<=columns)return {groups,width,ref,name,spec,columns};
  }
  throw Error(`The ${rows.length}-row materials list cannot fit legibly on one A4 page, even in two columns. Reduce the number of distinct cut lengths or export smaller designs separately. No PDF was downloaded.`);
}
function drawMaterials(doc,layout,thumbnails,summary,unit){
  for(const [column,rows] of layout.groups.entries()){
    const x=12+column*(layout.width+6),nameX=x+layout.ref,specX=nameX+layout.name,quantityX=x+layout.width-10;
    doc.setFillColor(227,240,239);doc.rect(x,46,layout.width,10,'F');
    text(doc,'Reference',x+2,52,8,true);text(doc,'Component',nameX,52,8,true);text(doc,'Spec / cut',specX,52,8,true);text(doc,'Qty',quantityX,52,8,true);
    let y=56;
    for(const row of rows){
      doc.setFillColor(248,250,250);doc.rect(x,y,layout.width,row.height,'F');
      doc.addImage(thumbnails.get(row.type),'PNG',x+2,y+(row.height-12)/2,18,12,`reference-${row.type}`);
      text(doc,row.nameLines,nameX,y+5,9);text(doc,row.specLines,specX,y+5,9);text(doc,String(row.count),quantityX,y+5,9,true);
      y+=row.height;doc.setDrawColor(221,230,232);doc.line(x,y,x+layout.width,y);
    }
  }
  text(doc,`Total pieces: ${summary.count}${summary.references?`   |   Scale references: ${summary.references}`:''}`,12,267,11,true);text(doc,`Total tube cut length: ${pdfLength(summary.total,unit)}`,12,274,11,true);
  text(doc,'Cut lengths include the tube inserted into fitting sockets. Fittings are counted separately.',12,281,9);
}
export async function createDesignPDF(data,{unit='mm',title='Untitled design',onProgress=()=>{}}={}){
  const model=validate(data);if(!model.pieces.length)throw Error('Add a component before exporting.');
  if(!Object.hasOwn(lengths,unit))throw Error('Unsupported length unit.');
  await import('../vendor/jspdf-3.0.3/jspdf.umd.min.js');
  const doc=new globalThis.jspdf.jsPDF({orientation:'portrait',unit:'mm',format:'a4',compress:true});
  doc.setProperties({title:`${title} - PVC design`,subject:'Materials and eight design views',creator:'PVC Studio'});
  const summary=model.materials(),layout=materialsLayout(doc,summary.rows,unit);
  const materialPages=Math.ceil(layout.groups.length/layout.columns),totalPages=materialPages+2;
  let renderer;const scene=exportScene(),parts=new THREE.Group(),reference=new THREE.Group();scene.add(parts,reference);
  try{
    renderer=exportRenderer();parts.visible=false;
    const thumbnails=new Map();
    for(const row of summary.rows.filter((r,i,a)=>a.findIndex(t=>t.type===r.type)===i)){
      const {type}=row;
      onProgress(`PDF: rendering reference for ${CATALOG[type].name}…`);await pause();
      reference.add(geometry({type,length:120,id:'reference'}));
      thumbnails.set(type,capture(renderer,scene,reference,{direction:[1,.9,1.3],up:[0,1,0]},450,300));dispose(reference);
    }
    for(let page=0;page<materialPages;page++){
      if(page)doc.addPage('a4','portrait');
      heading(doc,title,'Materials list',page+1,totalPages);
      drawMaterials(doc,{...layout,groups:layout.groups.slice(page*layout.columns,(page+1)*layout.columns)},thumbnails,summary,unit);
    }
    parts.visible=true;reference.visible=false;
    for(const p of model.pieces){const g=geometry(p);g.position.copy(vec(p.p));g.quaternion.copy(quat(p.q));parts.add(g);}
    for(const [index,view] of PDF_VIEWS.entries()){
      onProgress(`PDF: rendering ${view.label} (${index+1} / 8)…`);await pause();
      if(index%4===0){doc.addPage('a4','portrait');heading(doc,title,index===0?'Directional views':'Top, bottom and perspective views',materialPages+1+Math.floor(index/4),totalPages);}
      const cell=index%4,x=12+(cell%2)*96,y=48+Math.floor(cell/2)*117;
      text(doc,view.label,x,y,11,true);text(doc,view.perspective?'Perspective':`Orthographic / from ${view.axis}`,x,y+6,8);
      const image=capture(renderer,scene,parts,view,1092,1218);
      doc.addImage(image,'PNG',x,y+10,86,86*1218/1092,`view-${index}`);
    }
    onProgress(`PDF: assembling ${totalPages} pages…`);await pause();const blob=doc.output('blob');blob.pageCount=totalPages;return blob;
  }finally{
    dispose(parts);dispose(reference);scene.clear();
    if(renderer){renderer.dispose();renderer.forceContextLoss();renderer.domElement.width=renderer.domElement.height=1;}
  }
}
export function downloadPDF(blob){
  const url=URL.createObjectURL(blob),a=document.createElement('a');
  try{a.href=url;a.download='pvc-design.pdf';document.body.append(a);a.click();}
  finally{a.remove();setTimeout(()=>URL.revokeObjectURL(url),2000);}
}
