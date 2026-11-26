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

 await page.goto(origin+'/tests/.pvc-browser/pvc_design.html');await page.waitForFunction(()=>globalThis.pvcTest);
 await page.evaluate(async()=>{const {Design}=await import('/assets/js/pvc-model.mjs');const m=new Design();m.add('cap',[0,120,0]);localStorage.setItem('pvc-studio-browser-test',JSON.stringify(m.data()));});
 await page.reload();await page.waitForFunction(()=>globalThis.pvcTest);
 const target=async type=>page.evaluate(async type=>{const {Design}=await import('/assets/js/pvc-model.mjs');const {placementTargets}=await import('/assets/js/pvc-placement.mjs');const m=new Design(pvcTest.read().data);const t=placementTargets(m).find(t=>t.type===type);return pvcTest.screen(t.position.toArray());},type);
 await page.locator('[data-type="tube"]').click();const at=await target('socket');await page.mouse.move(at.x,at.y);await page.waitForTimeout(100);
 let before=await page.evaluate(()=>pvcTest.read().placement);assert(before.connection);await page.screenshot({path:path.join(out,'connection-preview.png')});await page.mouse.click(at.x,at.y);
 let after=await page.evaluate(()=>pvcTest.read());assert.deepEqual(after.data.pieces.at(-1).p,before.p);assert.deepEqual(after.data.pieces.at(-1).q,before.q);console.log('PASS real mouse click preview/commit');
 await page.locator('#frame').click();const to=await target('tube'),box=await page.locator('[data-type="elbow90"]').boundingBox();await page.mouse.move(box.x+box.width/2,box.y+box.height/2);await page.mouse.down();await page.mouse.move(to.x,to.y,{steps:15});await page.waitForTimeout(200);
 before=await page.evaluate(()=>pvcTest.read().placement);assert(before?.connection,'No real native drag preview');await page.screenshot({path:path.join(out,'drag-connection-preview.png')});await page.mouse.up();await page.waitForTimeout(100);
 after=await page.evaluate(()=>pvcTest.read());assert(!after.placement);assert.deepEqual(after.data.pieces.at(-1).p,before.p);assert.deepEqual(after.data.pieces.at(-1).q,before.q);assert.equal(after.data.connections.length,2);console.log('PASS real native catalog drag preview/commit');
 assert.deepEqual(errors,[]);console.log('PASS no page errors');
 }finally{await browser.close();}
})().then(()=>server.close()).catch(error=>{console.error(error);server.close();process.exitCode=1;});
