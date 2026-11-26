// Run from the repository root after python tests/pvc-browser-fixtures.py.
// Requires Playwright and Chrome; PVC_BROWSER optionally selects a browser binary.
const assert=require('node:assert/strict');
const fs=require('node:fs');
const path=require('node:path');
const http=require('node:http');
const {pathToFileURL}=require('node:url');
const {chromium}=require('playwright');
const root=process.cwd(),out=path.join(root,'tmp/pdfs/pvc-export');fs.mkdirSync(out,{recursive:true});
const mime={'.html':'text/html','.js':'text/javascript','.mjs':'text/javascript','.css':'text/css','.svg':'image/svg+xml'};
const server=http.createServer((req,res)=>{const file=path.join(root,decodeURIComponent(req.url.split('?')[0]));fs.readFile(file,(error,body)=>{res.writeHead(error?404:200,{'Content-Type':mime[path.extname(file)]||'application/octet-stream'});res.end(error?'Not found':body);});});
(async()=>{
 await new Promise(r=>server.listen(0,'127.0.0.1',r));const origin=`http://127.0.0.1:${server.address().port}`;
 const browser=await chromium.launch({...(process.env.PVC_BROWSER?{executablePath:process.env.PVC_BROWSER}:{channel:'chrome'}),headless:true,args:['--use-angle=swiftshader','--enable-unsafe-swiftshader']});
 try{
 const page=await browser.newPage({viewport:{width:1440,height:1100},acceptDownloads:true});page.setDefaultTimeout(120000);const errors=[];page.on('pageerror',e=>errors.push(e.message));
 const requests=[];page.on('request',r=>requests.push(r.url()));
 if(!process.env.PVC_SKIP_INTERACTIONS){await page.goto(origin+'/tests/pvc-interactions.html');await page.waitForFunction(()=>/^(PASS|FAIL)/.test(document.title),{},{timeout:120000});
 const interactions=await page.locator('#results').innerText();console.log(interactions);assert(!interactions.includes('FAIL'));}
 if(process.env.PVC_ONLY_INTERACTIONS)return;
 const load=async data=>{await page.goto(origin+'/tests/.pvc-browser/pvc_design.html');await page.waitForFunction(()=>globalThis.pvcTest);await page.evaluate(data=>{localStorage.setItem('pvc-studio-browser-test',JSON.stringify(data));},data);await page.reload();await page.waitForFunction(()=>globalThis.pvcTest);await page.waitForTimeout(300);};
 const {Design,rectangle}=await import(pathToFileURL(path.join(root,'assets/js/pvc-model.mjs')));
 await load(new Design().data());assert(await page.locator('#download-pdf').isDisabled());
 async function download(name,direct=false){
   const before=await page.evaluate(()=>pvcTest.read());
   const downloadEvent=page.waitForEvent('download');if(direct)await page.evaluate(()=>document.querySelector('#download-pdf').click());else await page.locator('#download-pdf').click();assert(await page.locator('#download-pdf').isDisabled());
   const download=await downloadEvent;assert.equal(download.suggestedFilename(),'pvc-design.pdf');await download.saveAs(path.join(out,name+'.pdf'));
   await page.waitForFunction(()=>!document.querySelector('#download-pdf').disabled);assert.match(await page.locator('#status').innerText(),/Downloaded.*3 pages/);
   const after=await page.evaluate(()=>pvcTest.read());assert.deepEqual(after,before,'Export changed workspace');console.log('PASS download and unchanged state: '+name);
 }
 await load(rectangle().data());await page.locator('#select-all').click();await page.locator('[data-tool="rotate"]').click();await page.locator('[data-type="tee"]').click();
 await download('frame'); // selected, transform tool, joints, pending placement and ghosts retained
 const mixed=new Design();mixed.add('tube',[-330,130,90],123.456);mixed.add('tube',[240,330,-100],650);mixed.add('tube',[240,330,300],650);mixed.add('tube',[1200,-200,-750],123.4560001);
 for(const [i,type] of ['coupling','elbow90','elbow45','tee','cross','corner','cap'].entries())mixed.add(type,[i*145-400,i*48,-400],400,[0,0,Math.sin(i*.12),Math.cos(i*.12)]);
 await load(mixed.data());await page.locator('#select-all').click();await page.evaluate(()=>document.querySelector('#length-unit').click());assert.equal(await page.evaluate(()=>pvcTest.read().lengthUnit),'cm');await download('mixed-cm');
 await page.screenshot({path:path.join(out,'workspace.png')});
 // A pending cut-length gesture exports its committed snapshot without completing it.
 const pending=new Design();pending.add('tube',[0,120,0],500);await load(pending.data());await page.locator('#select-all').click();
 await page.evaluate(()=>{const input=document.querySelector('#length-slider');input.value=800;input.dispatchEvent(new Event('input',{bubbles:true}));});
 await download('committed',true);
 // A rendering failure must restore the button and retain all application state.
 await load(rectangle().data());const failureState=await page.evaluate(()=>pvcTest.read());
 await page.evaluate(()=>{globalThis.savedDataURL=HTMLCanvasElement.prototype.toDataURL;HTMLCanvasElement.prototype.toDataURL=()=>{throw Error('Injected capture failure');};document.querySelector('#download-pdf').click();});
 await page.waitForFunction(()=>document.querySelector('#status').textContent.includes('Injected capture failure'));
 assert(!await page.locator('#download-pdf').isDisabled());assert.deepEqual(await page.evaluate(()=>pvcTest.read()),failureState);
 await page.evaluate(()=>HTMLCanvasElement.prototype.toDataURL=globalThis.savedDataURL);console.log('PASS rendering failure restores controls and workspace');
 // Exact grouping, projection, all-corner framing, layout, failure cleanup.
 const unitChecks=await page.evaluate(async()=>{
  const {PDF_VIEWS,frameExportCamera,materialsLayout,createDesignPDF,pdfLength}=await import('/assets/js/pvc-pdf.mjs');
  const THREE=await import('/assets/vendor/three-0.170.0/three.module.js');const {Design}=await import('/assets/js/pvc-model.mjs');
  if(pdfLength(123.4560001,'cm')!=='12.34560001 cm'||pdfLength(1800,'mm')!=='1800 mm'||pdfLength(32,'m')!=='0.032 m'||pdfLength(0,'cm')!=='0 cm')throw Error('Unit formatting');
  const box=new THREE.Box3(new THREE.Vector3(-14000,-500,-300),new THREE.Vector3(400,8000,3000));
  for(const view of PDF_VIEWS){const c=frameExportCamera(box,view,1092/1218);if(!!c.isPerspectiveCamera!==!!view.perspective)throw Error('Projection '+view.label);
   const target=box.getCenter(new THREE.Vector3()),direction=c.position.clone().sub(target).normalize();if(direction.distanceTo(new THREE.Vector3(...view.direction).normalize())>1e-8)throw Error('Orientation '+view.label);
   for(const x of [box.min.x,box.max.x])for(const y of [box.min.y,box.max.y])for(const z of [box.min.z,box.max.z]){const p=new THREE.Vector3(x,y,z).project(c);if(Math.abs(p.x)>.86||Math.abs(p.y)>.86||Math.abs(p.z)>1)throw Error('Clipping '+view.label);}}
  const m=new Design();for(let i=0;i<20;i++)m.add('tube',[i*30,0,0],80+i);const doc=new jspdf.jsPDF();const layout=materialsLayout(doc,m.materials().rows,'m');if(layout.columns!==2||layout.groups.flat().length!==20)throw Error('Compact layout');
  let failed=false;try{await createDesignPDF(m.data(),{onProgress:()=>{throw Error('Injected render failure');}});}catch(e){failed=e.message==='Injected render failure';}if(!failed)throw Error('Failure injection');
  return 'PASS eight projections/orientations, bounds, compact columns and render-failure cleanup';
 });console.log(unitChecks);
 const compact=new Design();for(let i=0;i<20;i++)compact.add('tube',[i%5*130,Math.floor(i/5)*100,0],80+i);await load(compact.data());await download('compact');
 const huge=new Design();for(let i=0;i<100;i++)huge.add('tube',[i*10,0,0],80+i);await load(huge.data());const before=await page.evaluate(()=>pvcTest.read());let unexpected=false;const unexpectedDownload=()=>unexpected=true;page.on('download',unexpectedDownload);
 await page.locator('#download-pdf').click();await page.waitForFunction(()=>document.querySelector('#status').dataset.error==='true');assert.match(await page.locator('#status').innerText(),/100-row.*cannot fit legibly/);assert(!await page.locator('#download-pdf').isDisabled());assert.deepEqual(await page.evaluate(()=>pvcTest.read()),before);assert(!unexpected);page.off('download',unexpectedDownload);console.log('PASS oversize failure, no partial download and controls restored');
 await page.setViewportSize({width:360,height:850});const header=await page.locator('.app-header').evaluate(el=>({width:el.scrollWidth,viewport:innerWidth,buttons:[...el.querySelectorAll('button')].map(b=>({x:b.getBoundingClientRect().x,right:b.getBoundingClientRect().right}))}));assert(header.width<=header.viewport);assert(header.buttons.every(b=>b.x>=0&&b.right<=360));await page.screenshot({path:path.join(out,'narrow.png')});console.log('PASS narrow header');
 await page.waitForTimeout(2100);
 assert(requests.every(url=>url.startsWith(origin)||url.startsWith('blob:')||url.startsWith('data:')),'External request');assert.deepEqual(errors,[]);console.log('PASS no page errors or external network requests');
 }finally{await browser.close();}
})().then(()=>server.close()).catch(error=>{console.error(error);server.close();process.exitCode=1;});
