/* Classroom convenience only: inspectable password and bypassable local lockout.
   The data file is independently downloadable; this is not data authorization. */
(function(){
 'use strict';
 const key='population-lesson-password-failures',limit=5;
 const form=document.getElementById('password-form'),input=document.getElementById('lesson-password'),button=document.getElementById('gate-enter'),feedback=document.getElementById('gate-feedback');
 let busy=false,unavailable=false;
 function readFailures(){
  const raw=localStorage.getItem(key);
  if(raw!==null&&!/^[0-5]$/.test(raw))throw Error('Invalid stored attempt count');
  const count=raw===null?0:Number(raw);
  // Verify writes as well as reads before allowing any authentication.
  localStorage.setItem(key,String(count));
  if(localStorage.getItem(key)!==String(count))throw Error('Storage write failed');
  return count;
 }
 function writeFailures(count){localStorage.setItem(key,String(count));if(localStorage.getItem(key)!==String(count))throw Error('Storage write failed');}
 function closed(count){
  const blocked=count>=limit;
  input.disabled=button.disabled=blocked;
  feedback.textContent=blocked?'Access blocked after five incorrect attempts.':`${limit-count} attempts remaining.`;
 }
 function storageError(){
  unavailable=true;input.disabled=button.disabled=true;
  feedback.textContent='Persistent browser storage is unavailable or invalid. Access remains closed. Use a browser that allows persistent storage for this page.';
 }
 function loadScript(src){return new Promise((resolve,reject)=>{const s=document.createElement('script');s.src=src;s.onload=resolve;s.onerror=()=>reject(Error('Lesson load failed'));document.body.append(s);});}
 try{closed(readFailures());if(!input.disabled)input.focus();}catch{storageError();}
 // Keep another open tab's gate in sync. Reset simulation never touches this key.
 window.addEventListener('storage',e=>{if(e.key===key&&!busy&&!unavailable){try{closed(readFailures());}catch{storageError();}}});
 form.addEventListener('submit',async e=>{
  e.preventDefault();if(busy||unavailable)return;
  try{
   const failures=readFailures();if(failures>=limit){closed(failures);return;}
   if(input.value!=='321654'){
    writeFailures(failures+1);closed(failures+1);input.value='';
    if(!input.disabled){feedback.textContent='Incorrect password. '+feedback.textContent;input.focus();}
    return;
   }
   writeFailures(0);
  }catch{storageError();return;}
  busy=true;input.value='';input.disabled=button.disabled=true;feedback.textContent='Opening lesson…';
  try{
   await loadScript('../assets/data/survey_data_extended.js');
   await loadScript('../assets/js/survey-simulation-core.js');
   // Initialization measures the visible chart; reveal and initialize in one task.
   // Load source first, then let it reveal the lesson immediately before reset.
   await loadScript('../assets/js/population-simulation.js');
   document.getElementById('lesson-gate').hidden=true;
   document.getElementById('step-title').focus();
  }catch{
   document.getElementById('lesson').hidden=true;
   feedback.textContent='The lesson could not be loaded. Reload the page and enter the password again.';
  }
 });
})();
