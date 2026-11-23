/* Shared nonmodal Options panel. Dimensions are preferred expanded dimensions;
   viewport constraints never overwrite them unless the user resizes a corner. */
window.initializeOptionsPanel=function(){
 'use strict';
 const panel=document.getElementById('options-panel'),bar=document.getElementById('options-titlebar'),body=document.getElementById('options-body'),toggle=document.getElementById('options-toggle'),launcher=document.getElementById('options-open');
 const handles=[...panel.querySelectorAll('.options-resize')];
 let collapsed=false,gesture=null;
 const initial=getComputedStyle(panel);
 let expanded={width:parseFloat(initial.width),height:parseFloat(initial.getPropertyValue('--options-initial-height'))};
 const clamp=(n,min,max)=>Math.max(min,Math.min(n,max));
 function bounds(){return{width:Math.max(0,document.documentElement.clientWidth-16),height:Math.max(0,window.innerHeight-16)}}
 function minimum(){const b=bounds();return{width:Math.min(160,b.width),height:Math.min(80,b.height)}}
 function position(left,top){
  const r=panel.getBoundingClientRect(),b=bounds();
  panel.style.left=clamp(left,8,8+b.width-r.width)+'px';
  panel.style.top=clamp(top,8,8+b.height-r.height)+'px';
 }
 function fit(){
  if(panel.hidden)return;
  const r=panel.getBoundingClientRect(),b=bounds(),m=minimum();
  panel.style.width=clamp(expanded.width,m.width,b.width)+'px';
  panel.style.height=collapsed?'auto':clamp(expanded.height,m.height,b.height)+'px';
  position(r.left,r.top);
 }
 function stopGesture(){
  const old=gesture;gesture=null;
  if(old?.target.hasPointerCapture(old.id))old.target.releasePointerCapture(old.id);
 }
 function resetPosition(){position(document.documentElement.clientWidth-panel.offsetWidth-16,document.getElementById('plot').getBoundingClientRect().top)}
 function visibility(open){
  stopGesture();panel.hidden=!open;launcher.hidden=open;launcher.setAttribute('aria-expanded',String(open));
  if(open){fit();bar.focus()}else launcher.focus();
 }
 toggle.onclick=()=>{
  stopGesture();
  if(!collapsed&&body.contains(document.activeElement))toggle.focus();
  collapsed=!collapsed;body.hidden=collapsed;panel.classList.toggle('is-collapsed',collapsed);
  handles.forEach(handle=>handle.hidden=collapsed);
  const label=collapsed?'Expand Options':'Collapse Options';
  toggle.setAttribute('aria-label',label);toggle.title=label;toggle.setAttribute('aria-expanded',String(!collapsed));
  fit();
 };
 launcher.onclick=()=>visibility(true);
 document.getElementById('options-close').onclick=()=>visibility(false);
 function start(e,corner){
  if(e.button!==0||gesture||panel.hidden||(corner&&collapsed))return;
  const r=panel.getBoundingClientRect();
  gesture={id:e.pointerId,target:e.currentTarget,corner,x:e.clientX,y:e.clientY,left:r.left,top:r.top,right:r.right,bottom:r.bottom};
  e.currentTarget.setPointerCapture(e.pointerId);e.currentTarget.focus();e.preventDefault();e.stopPropagation();
 }
 function resize(g,dx,dy){
  const west=g.corner.includes('w'),north=g.corner.includes('n'),b=bounds(),m=minimum();
  const left=west?clamp(g.left+dx,8,g.right-m.width):g.left;
  const right=west?g.right:clamp(g.right+dx,g.left+m.width,8+b.width);
  const top=north?clamp(g.top+dy,8,g.bottom-m.height):g.top;
  const bottom=north?g.bottom:clamp(g.bottom+dy,g.top+m.height,8+b.height);
  expanded={width:right-left,height:bottom-top};
  // Set the complete rectangle together; no observer repositions its fixed corner.
  Object.assign(panel.style,{left:left+'px',top:top+'px',width:expanded.width+'px',height:expanded.height+'px'});
 }
 function move(e){
  if(gesture?.id!==e.pointerId)return;
  const dx=e.clientX-gesture.x,dy=e.clientY-gesture.y;
  if(gesture.corner)resize(gesture,dx,dy);else position(gesture.left+dx,gesture.top+dy);
 }
 for(const target of [bar,...handles]){
  target.addEventListener('pointermove',move);
  for(const event of ['pointerup','pointercancel','lostpointercapture'])target.addEventListener(event,e=>{if(gesture?.id===e.pointerId)stopGesture()});
 }
 bar.onpointerdown=e=>{if(!e.target.closest('button,input,a,select,textarea'))start(e,null)};
 const arrows=['ArrowLeft','ArrowRight','ArrowUp','ArrowDown'];
 bar.onkeydown=e=>{
  if(e.target!==bar)return;
  const r=panel.getBoundingClientRect(),step=e.shiftKey?40:10;
  if(e.key==='Home'){e.preventDefault();resetPosition()}
  else if(arrows.includes(e.key)){e.preventDefault();position(r.left+(e.key==='ArrowRight'?step:e.key==='ArrowLeft'?-step:0),r.top+(e.key==='ArrowDown'?step:e.key==='ArrowUp'?-step:0))}
 };
 for(const handle of handles){
  handle.onpointerdown=e=>start(e,handle.dataset.corner);
  handle.onkeydown=e=>{
   if(!arrows.includes(e.key)||collapsed)return;
   e.preventDefault();const r=panel.getBoundingClientRect(),step=e.shiftKey?40:10;
   resize({corner:handle.dataset.corner,left:r.left,top:r.top,right:r.right,bottom:r.bottom},e.key==='ArrowRight'?step:e.key==='ArrowLeft'?-step:0,e.key==='ArrowDown'?step:e.key==='ArrowUp'?-step:0);
  };
 }
 document.addEventListener('keydown',e=>{if(e.key==='Escape'&&!panel.hidden){e.preventDefault();visibility(false)}});
 // Only the window changes available space. Content changes scroll internally;
 // observing the panel itself would interfere with opposite-corner anchoring.
 window.addEventListener('resize',()=>{stopGesture();fit()});
 launcher.hidden=true;fit();resetPosition();
};
