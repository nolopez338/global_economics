const assert=require('node:assert/strict'),fs=require('node:fs'),path=require('node:path'),http=require('node:http');
const {chromium}=require('playwright');
const root=process.cwd(),out=path.join(root,'tmp/pvc-templates');fs.mkdirSync(out,{recursive:true});
const mime={'.html':'text/html','.js':'text/javascript','.mjs':'text/javascript','.css':'text/css','.svg':'image/svg+xml'};
const server=http.createServer((req,res)=>fs.readFile(path.join(root,decodeURIComponent(req.url.split('?')[0])),(err,body)=>{res.writeHead(err?404:200,{'Content-Type':mime[path.extname(req.url)]||'application/octet-stream'});res.end(err?'Not found':body)}));
(async()=>{
 await new Promise(r=>server.listen(0,'127.0.0.1',r));
 const browser=await chromium.launch({channel:'chrome',headless:true,args:['--use-angle=swiftshader','--enable-unsafe-swiftshader']});
 try{
 const page=await browser.newPage({viewport:{width:1440,height:1000},acceptDownloads:true});page.setDefaultTimeout(180000);const errors=[];page.on('pageerror',e=>errors.push(e.message));
 await page.goto(`http://127.0.0.1:${server.address().port}/tests/.pvc-browser/pvc_design.html`);await page.waitForFunction(()=>globalThis.pvcTest);
 const read=()=>page.evaluate(()=>pvcTest.read());
 const options=await page.locator('#template option').evaluateAll(a=>a.map(o=>({id:o.value,name:o.textContent})));assert.equal(options.length,10);assert.equal(options[0].name,'Empty');
 let before=await read();await page.selectOption('#template','window');assert.deepEqual((await read()).data,before.data,'preview mutated design');
 await page.locator('#load-template').click();let windowState=await read();assert.equal(windowState.undo,1);assert.equal(windowState.selected.length,0);assert.equal(windowState.tool,'select');assert.deepEqual(JSON.parse(windowState.autosave),windowState.data);
 // Reject both nonempty and Empty replacement without affecting model, history or placement.
 await page.locator('[data-type="tube"]').click();before=await read();
 for(const id of ['empty','desk']){await page.selectOption('#template',id);page.once('dialog',d=>d.dismiss());await page.locator('#load-template').click();assert.deepEqual(await read(),before);}
 await page.selectOption('#template','empty');page.once('dialog',d=>d.accept());await page.locator('#load-template').click();let empty=await read();assert.equal(empty.data.pieces.length,0);assert.equal(empty.placement,null);assert.equal(empty.undo,2);assert(await page.locator('#download-pdf').isDisabled());
 await page.locator('#undo').click();assert.deepEqual((await read()).data,windowState.data);await page.locator('#redo').click();assert.equal((await read()).data.pieces.length,0);
 console.log('PASS preview, rejected replacements, Empty, placement reset, one-step undo / redo and autosave');
 page.on('dialog',d=>d.accept());
 for(const {id,name} of options.slice(1)){
   await page.selectOption('#template',id);const previous=await read();await page.locator('#load-template').click();const state=await read();assert.equal(state.undo,previous.undo+1);assert.equal(state.data.pieces.length,new Set(state.data.pieces.map(p=>p.id)).size);assert.deepEqual(JSON.parse(state.autosave),state.data);
   assert.equal(await page.locator('#selection-content').innerText(),'Nothing selected');
   for(const view of ['front','side','perspective']){await page.selectOption('#camera',view);await page.waitForTimeout(150);await page.locator('#workspace').screenshot({path:path.join(out,`${id}-${view}.png`)});}
   const data=state.data;
   // Download actual portable JSON, import it through the file input, then restore autosave.
   let event=page.waitForEvent('download');await page.locator('#export').click();let file=await event;const json=path.join(out,id+'.json');await file.saveAs(json);assert.deepEqual(JSON.parse(fs.readFileSync(json,'utf8')),data);
   await page.locator('#new').click();await page.locator('#file').setInputFiles(json);await page.waitForFunction(()=>pvcTest.read().data.pieces.length>0);assert.deepEqual((await read()).data,data);
   await page.reload();await page.waitForFunction(()=>globalThis.pvcTest);assert.deepEqual((await read()).data,data);
   const result=await page.evaluate(async()=>{const {createDesignPDF}=await import('/assets/js/pvc-pdf.mjs');const blob=await createDesignPDF(pvcTest.read().data);return {pages:blob.pageCount,size:blob.size};});assert(result.size>50000&&result.pages>=3);
   // Also exercise the actual download button on the most complex template.
   if(id==='window'){event=page.waitForEvent('download');await page.locator('#download-pdf').click();file=await event;await file.saveAs(path.join(out,id+'.pdf'));await page.waitForFunction(()=>!document.querySelector('#download-pdf').disabled);}
   console.log(`PASS ${name}: rendered three views, JSON download/import, autosave reload, PDF ${result.pages} pages / ${result.size} bytes`);
 }
 await page.setViewportSize({width:360,height:850});await page.locator('#template').scrollIntoViewIfNeeded();const bounds=await page.locator('#template').boundingBox();assert(bounds.width<=140);await page.screenshot({path:path.join(out,'mobile.png')});assert.deepEqual(errors,[]);console.log('PASS responsive dropdown and no browser errors');
 }finally{await browser.close();}
})().then(()=>server.close()).catch(e=>{console.error(e);server.close();process.exitCode=1});
