// Real Chrome/WebGL UI verification. Generate fixtures with pvc-browser-fixtures.py.
// Test hooks only observe private state; edits use the actual UI and input events.
const assert=require('node:assert/strict'),fs=require('node:fs'),path=require('node:path'),http=require('node:http');
const {chromium}=require('playwright');
const root=process.cwd(),out=path.join(root,'tmp/pvc-bounds');fs.mkdirSync(out,{recursive:true});
const mime={'.html':'text/html','.js':'text/javascript','.mjs':'text/javascript','.css':'text/css','.svg':'image/svg+xml'};
const server=http.createServer((req,res)=>{const file=path.resolve(root,'.'+decodeURIComponent(req.url.split('?')[0]));if(!file.startsWith(root+path.sep)){res.writeHead(403);res.end();return;}fs.readFile(file,(e,b)=>{res.writeHead(e?404:200,{'Content-Type':mime[path.extname(file)]||'application/octet-stream'});res.end(e?'Not found':b);});});
(async()=>{
  await new Promise(r=>server.listen(0,'127.0.0.1',r));
  const browser=await chromium.launch({...(process.env.PVC_BROWSER?{executablePath:process.env.PVC_BROWSER}:{channel:'chrome'}),headless:true,args:['--use-angle=swiftshader','--enable-unsafe-swiftshader']});
  const page=await browser.newPage({viewport:{width:1440,height:1000},acceptDownloads:true}),errors=[];page.on('pageerror',e=>errors.push(e.message));page.on('dialog',d=>d.accept());page.setDefaultTimeout(30000);
  const origin=`http://127.0.0.1:${server.address().port}`,read=()=>page.evaluate(()=>pvcTest.read()),bounds=()=>page.evaluate(()=>pvcTest.bounds());
  const settled=()=>page.waitForFunction(()=>pvcTest.bounds().mode!==2||!pvcTest.bounds().visible||pvcTest.bounds().state==='approximate');
  const contained=async()=>assert((await bounds()).excess<1e-6,'every current selected vertex is contained');
  async function labels(){
    await page.waitForFunction(()=>[...document.querySelectorAll('.bounds-dimension')].every(e=>!e.hidden&&e.textContent.endsWith(' '+pvcTest.read().lengthUnit)&&e.style.transform&&e.offsetWidth));
    const result=await page.evaluate(()=>{
      const wr=document.querySelector('#workspace').getBoundingClientRect(),nodes=[...document.querySelectorAll('.bounds-dimension')];
      return nodes.map(n=>{const r=n.getBoundingClientRect(),style=getComputedStyle(n);return {text:n.textContent,x:r.x-wr.x,y:r.y-wr.y,w:r.width,h:r.height,font:style.fontSize,pointer:document.elementFromPoint(r.x+r.width/2,r.y+r.height/2)?.tagName,workspace:{w:wr.width,h:wr.height}};});
    });
    assert.equal(result.length,3);for(const r of result){assert(r.x>=7&&r.y>=7&&r.x+r.w<=r.workspace.w-7&&r.y+r.h<=r.workspace.h-7,JSON.stringify(r));assert.equal(r.font,'12px');assert.equal(r.pointer,'CANVAS');}
    for(let a=0;a<3;a++)for(let b=0;b<a;b++){const x=result[a],y=result[b];assert(x.x+x.w<=y.x||y.x+y.w<=x.x||x.y+x.h<=y.y||y.y+y.h<=x.y,'labels must not collide');}return result;
  }
  async function loadData(data){await page.locator('#file').setInputFiles({name:'bounds-fixture.json',mimeType:'application/json',buffer:Buffer.from(JSON.stringify(data))});await page.waitForFunction(n=>pvcTest.read().data.pieces.length===n,data.pieces.length);}
  async function pick(piece,shift=false){const p=await page.evaluate(p=>pvcTest.screen(p.p),piece);if(shift)await page.keyboard.down('Shift');await page.mouse.click(p.x,p.y);if(shift)await page.keyboard.up('Shift');}
  try{
    // Smoke the uninstrumented production page first, including native buttons.
    await page.goto(origin+'/general_fundamentals/pvc_design.html');await page.waitForSelector('#catalog button');
    const button=page.locator('#selection-bounds');assert.equal(await button.getAttribute('data-mode'),'0');assert.equal(await button.getAttribute('aria-pressed'),null);
    const size=await button.boundingBox();assert(size.width>=24&&size.height>=24);await button.focus();
    assert.equal(await button.evaluate(e=>getComputedStyle(e).outlineStyle),'solid');
    await page.keyboard.press('Enter');assert.equal(await button.getAttribute('data-mode'),'1');await page.keyboard.press('Space');assert.equal(await button.getAttribute('data-mode'),'2');
    assert.match(await button.getAttribute('aria-label'),/approximate.*Next: Off/);assert.match(await page.locator('#bounds-announcement').textContent(),/approximate/);
    assert(await page.locator('.bounds-overlay').isHidden());await page.keyboard.press('Space');assert.equal(await button.getAttribute('data-mode'),'0');
    assert.equal(await page.evaluate(()=>localStorage.getItem('pvc-studio-v1')),null);
    console.log('PASS production page, three states, Enter/Space, focus, 28px target, accessible names/announcement and empty selection');

    await page.goto(origin+'/tests/.pvc-browser/pvc_design.html');await page.waitForFunction(()=>globalThis.pvcTest);
    const data=await page.evaluate(async()=>{const {Design}=await import('/assets/js/pvc-model.mjs'),{Quaternion,Euler}=await import('/assets/vendor/three-0.170.0/three.module.js');const m=new Design();m.add('tube',[-200,150,0],500);m.add('tube',[250,380,-100],300,new Quaternion().setFromEuler(new Euler(.37,.61,.23)).toArray());m.add('elbow45',[0,500,180]);return m.data();});
    await loadData(data);await pick(data.pieces[0]);assert.deepEqual((await read()).selected,[data.pieces[0].id]);let before=await read();
    await button.click();await contained();assert.equal((await bounds()).positionCount,24);assert.equal((await bounds()).mode,1);
    let ls=await labels();assert(ls.every((r,i)=>r.text.startsWith('XYZ'[i])&&r.text.endsWith(' mm')));const world=(await bounds()).box;world.size.forEach((v,i)=>assert(Math.abs(v-[500,32,32][i])<1e-6));
    for(const view of ['top','front','side']){await page.selectOption('#camera',view);await page.waitForTimeout(120);await labels();await page.screenshot({path:path.join(out,'world-'+view+'.png')});}
    await page.selectOption('#camera','perspective');
    await button.click();await settled();await contained();await labels();assert((await bounds()).box.volume<=world.volume);assert.equal((await read()).undo,before.undo);assert.equal((await read()).autosave,before.autosave);assert.deepEqual((await read()).data,before.data);assert.equal((await read()).exported,before.exported);
    console.log('PASS explicitly selected tube, actual geometry dimensions, worker refinement and no history/autosave/model changes');

    await page.locator('#clear').click();await page.locator('#frame').click();await pick(data.pieces[0]);
    await pick(data.pieces[1],true);assert.equal((await read()).selected.length,2);assert.equal((await bounds()).mode,2);await contained();await settled();await contained();
    await pick(data.pieces[2],true);assert.equal((await read()).selected.length,3);await settled();await contained();await labels();
    await page.screenshot({path:path.join(out,'mixed-oriented.png')});
    const stable=await bounds();
    // Actual right drag, pan and wheel with OrbitControls damping.
    await page.locator('#workspace').scrollIntoViewIfNeeded();const wr=await page.locator('#workspace').boundingBox();
    await page.mouse.move(wr.x+wr.width*.6,wr.y+wr.height*.6);await page.mouse.down({button:'right'});await page.mouse.move(wr.x+wr.width*.6+80,wr.y+wr.height*.6+45,{steps:12});await page.mouse.up({button:'right'});await page.waitForTimeout(400);await labels();
    await page.mouse.wheel(0,-140);await page.waitForTimeout(400);await labels();
    await page.mouse.move(wr.x+wr.width*.5,wr.y+wr.height*.8);await page.mouse.down();await page.mouse.move(wr.x+wr.width*.5+20,wr.y+wr.height*.8+12,{steps:6});await page.mouse.up();await page.waitForTimeout(400);
    let after=await bounds();assert.deepEqual(after.box,stable.box);assert.equal(after.computations,stable.computations);assert.deepEqual((await read()).data,before.data);
    for(const view of ['top','front','side','perspective']){await page.selectOption('#camera',view);await page.waitForTimeout(250);await labels();assert.deepEqual((await bounds()).box,stable.box);assert.equal((await bounds()).computations,stable.computations);await page.screenshot({path:path.join(out,view+'.png')});}
    console.log('PASS Shift union with mixed rotations, actual orbit/pan/zoom, damping and top/front/side views; no camera-triggered geometry optimization');

    await page.setViewportSize({width:600,height:1000});await page.locator('#frame').click();await page.waitForTimeout(200);await labels();await page.screenshot({path:path.join(out,'narrow.png')});
    await page.setViewportSize({width:320,height:1000});await page.locator('#frame').click();await page.waitForTimeout(200);await labels();await page.screenshot({path:path.join(out,'minimum-width.png')});
    await page.setViewportSize({width:1440,height:1000});await page.locator('#frame').click();await page.waitForTimeout(200);
    // Every edit goes through existing controls, including a live length preview.
    await page.locator('#clear').click();assert(!(await bounds()).visible);assert.equal((await bounds()).mode,2);
    await pick(data.pieces[0]);await settled();before=await read();
    await page.locator('#length-slider').evaluate(e=>{e.value='700';e.dispatchEvent(new Event('input',{bubbles:true}));});await contained();assert.equal((await bounds()).state,'refining');assert.equal((await read()).undo,before.undo);assert(Math.max(...(await bounds()).box.size)>=700-1e-6);
    await page.locator('#length-slider').evaluate(e=>e.dispatchEvent(new Event('change',{bubbles:true})));await settled();assert.equal((await read()).undo,before.undo+1);
    await page.locator('#undo').click();await contained();assert.equal((await read()).data.pieces[0].length,500);await page.locator('#redo').click();await contained();assert.equal((await read()).data.pieces[0].length,700);
    for(const [id,value] of [['position-x','-100'],['rotation-z','37']]){await page.locator('#'+id).fill(value);await page.locator('#'+id).press('Enter');await contained();await settled();}
    await page.locator('[data-turn="y"]').first().click();await contained();await settled();
    // Movement mode's actual pointer preview + commit, containing at each step.
    await page.selectOption('#camera','top');await page.locator('#frame').click();const current=(await read()).data.pieces[0],screen=await page.evaluate(p=>pvcTest.screen(p.p),current);
    await page.mouse.dblclick(screen.x,screen.y);assert.equal((await read()).tool,'move-piece');await labels();before=await read();
    await page.mouse.move(screen.x-20,screen.y);await page.mouse.down();for(const d of [15,30,45]){await page.mouse.move(screen.x-20+d,screen.y+30,{steps:2});await contained();}await page.mouse.up();await settled();assert.equal((await read()).undo,before.undo+1);
    await page.keyboard.press('Escape');await page.locator('[data-tool="rotate"]').click();assert.equal((await read()).tool,'rotate');await contained();await page.locator('[data-tool="select"]').click();
    console.log('PASS live tube length and pointer translation, numeric position/rotation, discrete rotation, gizmo attachment and undo/redo');

    before=await read();const count=(await bounds()).computations;for(const unit of ['cm','m','mm']){await page.locator('#length-unit').click();assert((await labels()).every(r=>r.text.endsWith(' '+unit)));assert.deepEqual((await read()).data,before.data);assert.equal((await read()).autosave,before.autosave);assert.equal((await read()).undo,before.undo);assert.equal((await bounds()).computations,count);}
    const downloadEvent=page.waitForEvent('download');await page.locator('#export').click();const download=await downloadEvent;await download.saveAs(path.join(out,'design.json'));assert.deepEqual(JSON.parse(fs.readFileSync(path.join(out,'design.json'),'utf8')),before.data);
    const pdfEvent=page.waitForEvent('download');await page.locator('#download-pdf').click();const pdf=await pdfEvent;await pdf.saveAs(path.join(out,'design.pdf'));assert(fs.statSync(path.join(out,'design.pdf')).size>20000);
    await page.locator('#copy').click();await page.locator('#paste').click();await contained();assert.equal((await read()).data.pieces.length,4);await page.locator('#delete').click();assert(!(await bounds()).visible);assert.equal((await bounds()).mode,2);await page.locator('#undo').click();await contained();
    await page.locator('#new').click();assert(!(await bounds()).visible);assert.equal((await bounds()).mode,2);await page.locator('#undo').click();await contained();
    console.log('PASS units, unchanged autosave/history, JSON and PDF downloads, paste/deletion/New and undo');

    await page.selectOption('#template','ground');await page.locator('#load-template').click();assert(!(await bounds()).visible);
    await page.locator('#select-all').click();await settled();await contained();const all=await bounds();await page.locator('#frame').click();await page.waitForTimeout(200);await labels();
    await page.locator('#clear').click();const assembly=(await read()).data;await pick(assembly.pieces.find(p=>p.type==='tube'));assert.equal((await read()).selected.length,1);await contained();assert((await bounds()).box.volume<all.box.volume);
    await page.locator('#select-assembly').click();await settled();await contained();assert.equal((await read()).selected.length,assembly.pieces.length);assert(Math.abs((await bounds()).box.volume-all.box.volume)<1e-4);
    // Marquee native input (rectangle includes the full framed design).
    await page.locator('#clear').click();await page.locator('[data-tool="marquee"]').click();const rect=await page.locator('#workspace').boundingBox();await page.mouse.move(rect.x+5,rect.y+5);await page.mouse.down();await page.mouse.move(rect.x+rect.width-5,rect.y+rect.height-5,{steps:8});await page.mouse.up();assert.equal((await read()).selected.length,assembly.pieces.length);await contained();await settled();
    await page.screenshot({path:path.join(out,'assembly.png')});
    // Live coordinated resize while oriented bounds are enabled.
    await page.selectOption('#camera','perspective');await page.selectOption('#template','bridge');await page.locator('#load-template').click();
    const bridge=(await read()).data,rails=bridge.pieces.filter(p=>p.type==='tube'&&Math.abs(p.p[0]+350)<1e-6);
    for(const p of rails)await pick(p,true);assert.equal((await read()).selected.length,4);await settled();before=await read();
    await page.locator('#group-length').fill('100');await contained();assert.equal((await read()).undo,before.undo);await page.locator('#group-length').press('Enter');await settled();await contained();assert.equal((await read()).undo,before.undo+1);
    await page.locator('#undo').click();await contained();await page.locator('#redo').click();await contained();await settled();
    // Real rotation-ring pointer drag; test-only screen coordinates locate the
    // existing gizmo, rather than substituting a transform implementation.
    await page.locator('[data-tool="rotate"]').click();let grabbed=false;
    const handles=await page.evaluate(()=>pvcTest.rotationHandles('Y'));
    for(let i=0;i<handles.length;i+=3){const p=handles[i];await page.mouse.move(p.x,p.y);if((await read()).gizmoAxis!=='Y')continue;await page.mouse.down();if((await read()).gizmoDragging){grabbed=true;break;}await page.mouse.up();}
    assert(grabbed,'locate actual Y rotation ring');before=await read();
    for(const angle of [12,28,47]){const p=await page.evaluate(angle=>pvcTest.rotationPointer(angle),angle);await page.mouse.move(p.x,p.y);await contained();assert.equal((await read()).undo,before.undo);}
    await page.mouse.up();await settled();await contained();assert.equal((await read()).undo,before.undo+1);
    console.log('PASS active overlay during live coordinated tube resize and real rotation-ring previews/commit');
    await button.click();assert.equal((await bounds()).mode,0);assert(!(await bounds()).visible);assert.equal((await bounds()).workers,0);assert.equal((await bounds()).timer,0);
    assert.deepEqual(errors,[]);console.log('PASS template replacement, explicit vs connected selection, select-all, marquee, resource cancellation and no browser errors');
  }finally{await browser.close();}
})().then(()=>server.close()).catch(error=>{console.error(error);server.close();process.exitCode=1;});
