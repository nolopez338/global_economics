// Real UI imports/exports and atomic rejection through instrumented test-only buffers.
const assert=require('node:assert/strict'),fs=require('node:fs'),path=require('node:path'),http=require('node:http');
const {chromium}=require('playwright');
const root=process.cwd(),out=path.join(root,'tmp/pvc-standard');fs.mkdirSync(out,{recursive:true});
const mime={'.html':'text/html','.js':'text/javascript','.mjs':'text/javascript','.css':'text/css','.svg':'image/svg+xml'};
const server=http.createServer((req,res)=>{const file=path.resolve(root,'.'+decodeURIComponent(req.url.split('?')[0]));if(!file.startsWith(root+path.sep)){res.writeHead(403);res.end();return;}fs.readFile(file,(e,b)=>{res.writeHead(e?404:200,{'Content-Type':mime[path.extname(file)]||'application/octet-stream'});res.end(e?'Not found':b);});});
(async()=>{
 await new Promise(r=>server.listen(0,'127.0.0.1',r));
 const browser=await chromium.launch({channel:'chrome',headless:true,args:['--use-angle=swiftshader','--enable-unsafe-swiftshader']});
 try{
 const page=await browser.newPage({viewport:{width:1440,height:1000},acceptDownloads:true});page.setDefaultTimeout(30000);const errors=[];page.on('pageerror',e=>errors.push(e.message));
 const url=`http://127.0.0.1:${server.address().port}/tests/.pvc-browser/pvc_design.html`;
 const read=()=>page.evaluate(()=>pvcTest.read());
 await page.goto(`http://127.0.0.1:${server.address().port}/general_fundamentals/pvc_design.html`);
 await page.waitForSelector('#catalog button');assert.equal(await page.locator('#catalog button').count(),8);
 assert.equal(await page.locator('#template option').count(),10);
 await page.selectOption('#template','ground');await page.locator('#load-template').click();
 await page.locator('.materials').evaluate(e=>e.scrollTop=0);await page.screenshot({path:path.join(out,'production.png')});
 console.log('PASS production page catalog and standard-only template');
 await page.goto(url);await page.waitForFunction(()=>globalThis.pvcTest);
 assert.deepEqual(await page.locator('#catalog button').evaluateAll(a=>a.map(b=>b.dataset.type)),['tube','coupling','elbow90','elbow45','tee','cross','corner','person']);
 assert.equal(await page.locator('.materials .count').innerText(),'8');
 await page.selectOption('#template','ground');await page.locator('#load-template').click();
 await page.locator('[data-type="corner"]').click();
 const base=await read(),invalid=[];
 for(const type of ['multiway','cap','custom']){const d=structuredClone(base.data);d.pieces.at(-1).type=type;invalid.push(d);}
 for(const key of ['sockets','ports','socketCount','directions','positions','insertion','compatibility','scale']){const d=structuredClone(base.data);d.pieces[0][key]=[];invalid.push(d);}
 for(const data of invalid){
   const before=await read();await page.locator('#file').setInputFiles({name:'invalid.json',mimeType:'application/json',buffer:Buffer.from(JSON.stringify(data))});
   await page.waitForFunction(()=>document.querySelector('#status').textContent.startsWith('Could not load design:'));
   assert.deepEqual(await read(),before,'Rejected import changed design, preview, history or storage');
   await page.evaluate(data=>pvcTest.setClipboard(data),data);const pasteBefore=await read();await page.locator('#paste').click();assert.deepEqual(await read(),pasteBefore,'Rejected paste changed design');assert.equal(await page.locator('#status').getAttribute('data-error'),'true');
   for(const direction of ['undo','redo']){await page.evaluate(({direction,data})=>pvcTest.setHistory(direction,data),{direction,data});const historyBefore=await read();await page.locator('#'+direction).click();assert.deepEqual(await read(),historyBefore,'Rejected history changed state');assert.match(await page.locator('#status').innerText(),/Could not restore history/);}
 }
 console.log('PASS eight-item catalog (seven PVC components and Person) and atomic rejection of custom types/socket overrides in file imports, paste, undo and redo');
 await page.keyboard.press('Escape');
 let event=page.waitForEvent('download');await page.locator('#export').click();let download=await event;const file=path.join(out,'standard.json');await download.saveAs(file);assert.deepEqual(JSON.parse(fs.readFileSync(file,'utf8')),base.data);
 const pdf=await page.evaluate(async()=>{const {createDesignPDF}=await import('/assets/js/pvc-pdf.mjs');const {Design,CATALOG}=await import('/assets/js/pvc-model.mjs');const m=new Design();for(const [i,type] of Object.keys(CATALOG).entries())m.add(type,[i*160,100,0]);const blob=await createDesignPDF(m.data());return {pages:blob.pageCount,size:blob.size};});assert.equal(pdf.pages,3);assert(pdf.size>50000);
 await page.screenshot({path:path.join(out,'catalog-ground.png')});
 console.log('PASS real JSON download and PDF creation with all seven PVC components and Person');
 // Exercise the unique-socket bridge path with real mouse and keyboard events,
 // then round-trip the new tube and joints through the actual download/import UI.
 await page.evaluate(async()=>{
   const {Design}=await import('/assets/js/pvc-model.mjs');const m=new Design(),a=m.add('coupling',[0,100,0]),b=m.add('coupling',[600,100,0]);
   for(const [fitting,socket] of [[a,0],[b,1]]){const t=m.add('tube');m.connect({id:t.id,port:0},{id:fitting.id,port:socket});}
   localStorage.setItem('pvc-studio-browser-test',JSON.stringify(m.data()));
 });
 await page.reload();await page.waitForFunction(()=>globalThis.pvcTest);await page.selectOption('#camera','top');
 const bridgeBase=await read(),fittings=bridgeBase.data.pieces.filter(p=>p.type==='coupling');
 for(let i=0;i<fittings.length;i++){const at=await page.evaluate(p=>pvcTest.screen(p),fittings[i].p);if(i)await page.keyboard.down('Shift');await page.mouse.click(at.x,at.y);if(i)await page.keyboard.up('Shift');}
 assert.equal((await read()).data.connections.length,2,'Native Shift-click detached a joint');
 await page.locator('#connect').click();const bridge=await read();assert.equal(bridge.data.pieces.length,5);assert.equal(bridge.data.connections.length,4);assert.equal(bridge.undo,1);assert.deepEqual(JSON.parse(bridge.autosave),bridge.data);
 await page.locator('#undo').click();assert.deepEqual((await read()).data,bridgeBase.data);await page.locator('#redo').click();assert.deepEqual((await read()).data,bridge.data);
 await page.screenshot({path:path.join(out,'fitting-bridge.png')});
 event=page.waitForEvent('download');await page.locator('#export').click();download=await event;const bridgeFile=path.join(out,'fitting-bridge.json');await download.saveAs(bridgeFile);assert.deepEqual(JSON.parse(fs.readFileSync(bridgeFile,'utf8')),bridge.data);
 await page.locator('#new').click();assert.equal((await read()).data.pieces.length,0);
 await page.locator('#file').setInputFiles(bridgeFile);await page.waitForFunction(()=>document.querySelector('#status').textContent.startsWith('Loaded 5 pieces'));
 assert.deepEqual((await read()).data,bridge.data);await page.reload();await page.waitForFunction(()=>globalThis.pvcTest);assert.deepEqual((await read()).data,bridge.data);
 console.log('PASS native fitting selection, Shift-click, unique-socket tube bridge, undo/redo, JSON download/import and autosave reload');
 for(const data of invalid){await page.evaluate(data=>localStorage.setItem('pvc-studio-browser-test',JSON.stringify(data)),data);await page.reload();await page.waitForFunction(()=>globalThis.pvcTest);const state=await read();assert.equal(state.data.pieces.length,0);assert.equal(state.undo,0);assert.deepEqual(JSON.parse(state.autosave),data);assert.match(await page.locator('#status').innerText(),/Saved work could not be restored/);}
 console.log('PASS invalid autosave rejected without partial restoration or overwriting stored data');assert.deepEqual(errors,[]);
 }finally{await browser.close();}
})().then(()=>server.close()).catch(e=>{console.error(e);server.close();process.exitCode=1;});
