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
 await page.goto(origin+'/tests/.pvc-browser/pvc_design.html');await page.waitForFunction(()=>globalThis.pvcTest);
 await page.locator('[data-type="tube"]').click();
 await page.screenshot({path:path.join(out,'connection-preview.png')});
 assert.deepEqual(errors,[]);console.log('PASS no browser errors');
 }finally{await browser.close();}
})().then(()=>server.close()).catch(error=>{console.error(error);server.close();process.exitCode=1;});
