// Generate fixtures first: python tests/pvc-browser-fixtures.py
// Requires Playwright and Chrome (PVC_BROWSER can override the executable).
const assert=require('node:assert/strict'),fs=require('node:fs'),path=require('node:path'),http=require('node:http');
const {chromium}=require('playwright');
const root=process.cwd(),out=path.join(root,'tmp/pvc-coordinated-resize');fs.mkdirSync(out,{recursive:true});
const mime={'.html':'text/html','.js':'text/javascript','.mjs':'text/javascript','.css':'text/css','.svg':'image/svg+xml'};
const server=http.createServer((req,res)=>{const file=path.resolve(root,'.'+decodeURIComponent(req.url.split('?')[0]));if(!file.startsWith(root+path.sep)){res.writeHead(403);res.end();return;}fs.readFile(file,(e,b)=>{res.writeHead(e?404:200,{'Content-Type':mime[path.extname(file)]||'application/octet-stream'});res.end(e?'Not found':b);});});
(async()=>{
  await new Promise(r=>server.listen(0,'127.0.0.1',r));
  const browser=await chromium.launch({...(process.env.PVC_BROWSER?{executablePath:process.env.PVC_BROWSER}:{channel:'chrome'}),headless:true,args:['--use-angle=swiftshader','--enable-unsafe-swiftshader']});
  try{
    const page=await browser.newPage({viewport:{width:1440,height:1100}}),errors=[];page.on('pageerror',e=>errors.push(e.message));page.setDefaultTimeout(30000);
    const url=`http://127.0.0.1:${server.address().port}/tests/.pvc-browser/pvc_design.html`,read=()=>page.evaluate(()=>pvcTest.read());
    await page.goto(url);await page.waitForFunction(()=>globalThis.pvcTest);await page.selectOption('#template','bridge');await page.locator('#load-template').click();
    const start=await read(),rails=start.data.pieces.filter(p=>p.type==='tube'&&Math.abs(p.p[0]+350)<1e-6),selection=rails.map(p=>p.id);assert.equal(selection.length,4);
    async function selectPieces(pieces){
      await page.locator('#clear').click();
      for(const p of pieces){const point=await page.evaluate(p=>pvcTest.screen(p.p),p);await page.keyboard.down('Shift');await page.mouse.click(point.x,point.y);await page.keyboard.up('Shift');}
      assert.deepEqual(new Set((await read()).selected),new Set(pieces.map(p=>p.id)),'real Shift-click selection');
    }
    async function aligned(){
      const report=await page.evaluate(async()=>{const {validate,port}=await import('/assets/js/pvc-model.mjs');const m=validate(pvcTest.read().data);let gap=0,insertionError=0;for(const c of m.connections){const a=port(m.get(c.a.id),c.a.port),b=port(m.get(c.b.id),c.b.port);gap=Math.max(gap,a.position.distanceTo(b.position));const socket=a.type==='socket'?a:b,tube=a.type==='tube'?a:b;insertionError=Math.max(insertionError,Math.abs(socket.mouth.distanceTo(tube.position)-20));}return {gap,insertionError,joints:m.connections.length};});
      assert(report.gap<1e-7);assert(report.insertionError<1e-7);assert.equal(report.joints,start.data.connections.length);
    }
    async function preview(value,id='group-length'){
      await page.locator('#'+id).focus();await page.locator('#'+id).evaluate((e,value)=>{e.value=String(value);e.dispatchEvent(new Event('input',{bubbles:true}));},value);await aligned();
    }
    await selectPieces(rails);assert(await page.locator('#group-length').isEnabled());assert.equal(await page.locator('#group-length').inputValue(),'0');assert.match(await page.locator('#group-length-note').innerText(),/positive X stays fixed/);
    await page.locator('#group-length-section').scrollIntoViewIfNeeded();await page.screenshot({path:path.join(out,'template7-before.png')});
    await preview(100);const plus100=(await read()).data;for(const p of plus100.pieces){const old=start.data.pieces.find(o=>o.id===p.id);assert.deepEqual(p.q,old.q);if(p.type==='tube')assert.equal(p.length,old.length+(selection.includes(p.id)?100:0));}
    assert.deepEqual(plus100.connections,start.data.connections);assert.equal(await page.locator('#group-length-slider').inputValue(),'100');assert.equal((await read()).undo,start.undo);
    assert.match(await page.locator('#selection-content').innerText(),/750 mm/);assert.equal(await page.locator('#total-length').innerText(),`${plus100.pieces.filter(p=>p.type==='tube').reduce((sum,p)=>sum+p.length,0).toLocaleString('en-US')} mm`);
    await preview(700);await preview(-100);await preview(100);assert.deepEqual((await read()).data,plus100,'previews accumulate no drift');
    await page.screenshot({path:path.join(out,'template7-preview.png')});
    await page.keyboard.press('Enter');const committed=await read();assert.equal(committed.undo,start.undo+1);assert.deepEqual(JSON.parse(committed.autosave),plus100);assert.equal(await page.locator('#group-length').inputValue(),'0');
    await page.locator('#undo').click();assert.deepEqual((await read()).data,start.data);await page.locator('#redo').click();assert.deepEqual((await read()).data,plus100);await aligned();
    console.log('PASS Template 7 real four-tube selection, fixed-snapshot ± previews, unchanged fittings/cuts, exact joints/insertion, one-step undo/redo and autosave');
    // Cancellation inside a focused numeric input, without adding an undo entry.
    let before=await read();await preview(123.456);await page.keyboard.press('Escape');assert.deepEqual((await read()).data,before.data);assert.equal((await read()).undo,before.undo);assert.equal((await read()).autosave,before.autosave);
    // Invalid numeric input retains the last valid preview atomically.
    await preview(50);const valid=(await read()).data;
    await page.locator('#group-length').fill('99999');assert.deepEqual((await read()).data,valid);assert.equal(await page.locator('#group-length').getAttribute('aria-invalid'),'true');
    await page.locator('#group-length').fill('');assert.deepEqual((await read()).data,valid);await page.keyboard.press('Escape');assert.deepEqual((await read()).data,before.data);
    // Selection changes complete the current valid preview, then reset delta.
    await preview(25);const changed=(await read()).data;await page.locator('#select-all').click();assert.deepEqual((await read()).data,changed);assert.equal((await read()).undo,before.undo+1);assert(await page.locator('#group-length').isDisabled());assert.match(await page.locator('#group-length-note').innerText(),/includes fittings/);await page.locator('#undo').click();
    console.log('PASS numeric cancellation, invalid/empty input atomicity and clean selection changes');
    // Unit changes affect only presentation. Numeric adjustment precision is .001 mm.
    await selectPieces(rails);before=await read();
    const expected100=await page.evaluate(async({data,selection})=>{const {Design}=await import('/assets/js/pvc-model.mjs');const m=new Design(data);m.resizeTogether(selection,100);return m.data();},{data:before.data,selection});
    for(const [unit,value] of [['cm',10],['m',.1],['mm',100]]){
      await page.locator('#group-length-unit').click();assert.equal((await read()).lengthUnit,unit);assert.deepEqual((await read()).data,before.data);
      await preview(value);assert.deepEqual((await read()).data,expected100);
      await page.keyboard.press('Escape');assert.deepEqual((await read()).data,before.data);
    }
    await preview(.123);for(const p of (await read()).data.pieces.filter(p=>selection.includes(p.id)))assert.equal(p.length,before.data.pieces.find(o=>o.id===p.id).length+.123);await page.keyboard.press('Escape');
    console.log('PASS mm/cm/m conversion, synchronized controls and fractional precision');
    // Real pointer drag is one undoable gesture, checked at every sampled step.
    const slider=page.locator('#group-length-slider');await slider.scrollIntoViewIfNeeded();const box=await slider.boundingBox();before=await read();
    await page.mouse.move(box.x+box.width*.3,box.y+box.height/2);await page.mouse.down();
    for(const fraction of [.35,.4,.5,.25]){await page.mouse.move(box.x+box.width*fraction,box.y+box.height/2);await aligned();assert.equal((await read()).undo,before.undo);}
    await page.mouse.up();const dragged=await read();assert.equal(dragged.undo,before.undo+1);await page.locator('#undo').click();assert.deepEqual((await read()).data,before.data);await page.locator('#redo').click();assert.deepEqual((await read()).data,dragged.data);
    // Escape also cancels a real pointer gesture and ignores subsequent movement.
    before=await read();await slider.scrollIntoViewIfNeeded();await page.mouse.move(box.x+box.width*.4,box.y+box.height/2);await page.mouse.down();await page.keyboard.press('Escape');await page.mouse.move(box.x+box.width*.5,box.y+box.height/2);await page.mouse.up();assert.deepEqual((await read()).data,before.data);assert.equal((await read()).undo,before.undo);
    // Keyboard Home/End obey shared cut limits; one key gesture creates one action.
    await slider.focus();before=await read();await page.keyboard.press('Home');await aligned();assert.equal(Math.min(...(await read()).data.pieces.filter(p=>selection.includes(p.id)).map(p=>p.length)),80);assert.equal((await read()).undo,before.undo+1);await page.locator('#undo').click();
    await slider.focus();await page.keyboard.press('End');await aligned();assert.equal(Math.max(...(await read()).data.pieces.filter(p=>selection.includes(p.id)).map(p=>p.length)),3000);await page.locator('#undo').click();
    console.log('PASS live mouse gesture, Escape during dragging, keyboard shared limits and gesture history');
    // Blocked parallel selection, mixed pieces and nonparallel tubes stay visible.
    const current=(await read()).data;await selectPieces(current.pieces.filter(p=>selection.includes(p.id)).slice(0,3));assert(await page.locator('#group-length').isDisabled());assert.match(await page.locator('#group-length-note').innerText(),/unselected rigid section/);
    const nonparallel=[current.pieces.find(p=>selection.includes(p.id)),current.pieces.find(p=>p.type==='tube'&&Math.abs(p.p[0]+700)<1e-6&&p.length===350)];await selectPieces(nonparallel);assert(await page.locator('#group-length-slider').isDisabled());assert.match(await page.locator('#group-length-note').innerText(),/not parallel/);
    // Restore the documented example for the final screenshot and verify single editing.
    await selectPieces(current.pieces.filter(p=>selection.includes(p.id)));await page.locator('#group-length-section').scrollIntoViewIfNeeded();await page.screenshot({path:path.join(out,'template7-after.png')});
    await selectPieces([current.pieces.find(p=>selection.includes(p.id))]);assert(await page.locator('#length-section').isVisible());assert(await page.locator('#length').isDisabled());assert(await page.locator('#group-length-section').isHidden());
    // Unequal free cuts and a reversed direction use the same UI and preserve centres.
    await page.evaluate(async()=>{const {Design}=await import('/assets/js/pvc-model.mjs');const m=new Design();m.add('tube',[0,1600,0],500);m.add('tube',[0,2000,0],700,[0,1,0,0]);pvcTest.setClipboard(m.data());});
    await page.locator('#paste').click();before=await read();const freeIds=before.selected;
    await preview(100);let free=(await read()).data.pieces.filter(p=>freeIds.includes(p.id));assert.deepEqual(free.map(p=>p.length),[600,800]);for(const p of free)assert.deepEqual(p.p,before.data.pieces.find(o=>o.id===p.id).p);
    await page.keyboard.press('Enter');const freeCommit=await read();assert.equal(freeCommit.undo,before.undo+1);await page.locator('#undo').click();assert.deepEqual((await read()).data,before.data);await page.locator('#redo').click();assert.deepEqual((await read()).data,freeCommit.data);
    await page.locator('#frame').click();await selectPieces([free[0]]);assert(await page.locator('#length').isEnabled());await page.locator('#length').fill('900');await page.locator('#length').press('Enter');assert.equal((await read()).data.pieces.find(p=>p.id===free[0].id).length,900);
    console.log('PASS unequal 500/700 cuts become 600/800 with reversed direction, free centres, history and existing single-tube editing');
    await page.evaluate(async()=>{const {Design}=await import('/assets/js/pvc-model.mjs');const m=new Design();m.add('tube',[0,2500,0],80);m.add('tube',[0,2700,0],3000);pvcTest.setClipboard(m.data());});await page.locator('#paste').click();
    assert(await page.locator('#group-length').isDisabled());assert(await page.locator('#group-length-slider').isDisabled());assert.match(await page.locator('#group-length-note').innerText(),/no nonzero shared adjustment/);
    before=await read();await page.locator('#group-length-unit').click();assert.match(await page.locator('#group-length-note').innerText(),/8–300 cm/);assert.deepEqual((await read()).data,before.data);assert.equal((await read()).undo,before.undo);
    assert.deepEqual(errors,[]);console.log('PASS blocked/mixed/nonparallel explanations, single-tube inspector and no browser errors');
  }finally{await browser.close();}
})().then(()=>server.close()).catch(error=>{console.error(error);server.close();process.exitCode=1;});
