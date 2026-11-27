// Actual Chrome/WebGL verification. Edits use UI; fixture hooks only observe state.
// Run python tests/pvc-browser-fixtures.py first. Supply Playwright via NODE_PATH.
const assert=require('node:assert/strict'),fs=require('node:fs'),path=require('node:path'),http=require('node:http');
const {pathToFileURL}=require('node:url'),{chromium}=require('playwright');
const root=process.cwd(),out=path.join(root,'tmp/pvc-person');fs.mkdirSync(out,{recursive:true});
const mime={'.html':'text/html','.mjs':'text/javascript','.js':'text/javascript','.css':'text/css','.svg':'image/svg+xml'};
const server=http.createServer((req,res)=>{const file=path.resolve(root,'.'+decodeURIComponent(req.url.split('?')[0]));if(!file.startsWith(root+path.sep)){res.writeHead(403);res.end();return;}fs.readFile(file,(e,b)=>{res.writeHead(e?404:200,{'Content-Type':mime[path.extname(file)]||'application/octet-stream'});res.end(e?'Not found':b);});});
(async()=>{
  await new Promise(r=>server.listen(0,'127.0.0.1',r));const origin=`http://127.0.0.1:${server.address().port}`;
  const browser=await chromium.launch({...(process.env.PVC_BROWSER?{executablePath:process.env.PVC_BROWSER}:{channel:'chrome'}),headless:true,args:['--use-angle=swiftshader','--enable-unsafe-swiftshader']});
  try{
    const page=await browser.newPage({viewport:{width:1440,height:1050},acceptDownloads:true}),errors=[];
    page.on('pageerror',e=>errors.push(e.message));page.on('dialog',d=>d.accept());page.setDefaultTimeout(30000);
    const read=()=>page.evaluate(()=>pvcTest.read()),screen=p=>page.evaluate(p=>pvcTest.screen(p),p);
    const {Design,rectangle,validate,vec,quat}=await import(pathToFileURL(path.join(root,'assets/js/pvc-model.mjs')));
    const load=async data=>{await page.locator('#file').setInputFiles({name:'person.json',mimeType:'application/json',buffer:Buffer.from(JSON.stringify(data))});assert.deepEqual((await read()).data,data);};
    const pick=async(p,shift=false)=>{const local=p.type==='person'?[0,p.height*.93,0]:p.type==='tube'?[p.length*.35,0,0]:[0,0,0];const v=await screen(vec(local).applyQuaternion(quat(p.q)).add(vec(p.p)).toArray());if(shift)await page.keyboard.down('Shift');await page.mouse.click(v.x,v.y);if(shift)await page.keyboard.up('Shift');};
    const number=async(id,value)=>{await page.locator(id).fill(String(value));await page.locator(id).press('Enter');};
    async function download(button,name){const event=page.waitForEvent('download',{timeout:120000});await page.locator(button).click();const item=await event;await item.saveAs(path.join(out,name));return path.join(out,name);}

    // Smoke the actual shipped page, with its real model, storage and controls.
    await page.goto(origin+'/general_fundamentals/pvc_design.html');await page.waitForSelector('[data-type="person"]');
    assert.equal(await page.locator('#catalog button').count(),8);await page.locator('[data-type="person"]').click();
    let wr=await page.locator('#workspace canvas').boundingBox();await page.mouse.click(wr.x+wr.width*.5,wr.y+wr.height*.65);
    assert(await page.locator('#person-section').isVisible());assert.equal(await page.locator('#person-height').inputValue(),'1800');
    await page.locator('#frame').click();await number('#person-height',1900);await page.selectOption('#person-variant','woman');
    await page.screenshot({path:path.join(out,'production.png')});console.log('PASS production page: catalog, placement, height and silhouette controls');

    await page.goto(origin+'/tests/.pvc-browser/pvc_design.html');await page.waitForFunction(()=>globalThis.pvcTest);
    await page.locator('[data-type="person"]').click();let target=await screen([0,0,0]);await page.mouse.click(target.x,target.y);
    let state=await read(),p=state.data.pieces[0];assert.equal(p.height,1800);assert.equal(p.p[1],0);assert.equal(p.variant,'man');assert.equal(state.undo,1);await page.locator('#frame').click();
    // Native HTML catalog drag/drop, placing another independent reference.
    target=await screen([450,0,0]);wr=await page.locator('#workspace canvas').boundingBox();
    await page.locator('[data-type="person"]').dragTo(page.locator('#workspace canvas'),{targetPosition:{x:target.x-wr.x,y:target.y-wr.y}});
    state=await read();assert.equal(state.data.pieces.length,2);assert.equal(state.data.connections.length,0);assert.notEqual(state.data.pieces[0].id,state.data.pieces[1].id);
    console.log('PASS click and native catalog drag/drop create independent people with anchored feet');

    const single=new Design();single.add('person',[0,0,0]);await load(single.data());await page.locator('#select-all').click();await page.locator('#frame').click();
    assert(await page.locator('#ports-section').isHidden());assert(await page.locator('#length-section').isHidden());assert(await page.locator('#group-length-section').isHidden());
    await page.locator('#selection-bounds').click();let b=await page.evaluate(()=>pvcTest.bounds());assert(Math.abs(b.box.size[1]-1800)<1e-5);assert(b.excess<1e-6);
    let before=await read();await page.locator('#person-height').fill('1950');state=await read();assert.equal(state.data.pieces[0].height,1950);assert.equal(state.undo,before.undo);assert(state.transaction);
    assert.equal(await page.locator('#person-height-slider').inputValue(),'1950');b=await page.evaluate(()=>pvcTest.bounds());assert(Math.abs(b.box.size[1]-1950)<1e-5);
    await page.locator('#person-height').press('Escape');assert.deepEqual((await read()).data,before.data);assert.equal((await read()).undo,before.undo);
    await number('#person-height',1900);assert.equal((await read()).undo,before.undo+1);await page.locator('#undo').click();assert.equal((await read()).data.pieces[0].height,1800);await page.locator('#redo').click();assert.equal((await read()).data.pieces[0].height,1900);
    for(const invalid of ['2300','0','-10','']){before=await read();await page.locator('#person-height').fill(invalid);assert.equal(await page.locator('#person-height').getAttribute('aria-invalid'),'true');assert.deepEqual((await read()).data,before.data);await page.locator('#person-height').press('Enter');assert.match(await page.locator('#person-feedback').innerText(),/finite|1,?400.*2,?200/);}
    console.log('PASS live numeric preview, synchronized range and bounds, Escape, one undo/redo and invalid input feedback');

    // Real pointer slider drag: several previews, exactly one completed action.
    const slider=page.locator('#person-height-slider');await slider.scrollIntoViewIfNeeded();let r=await slider.boundingBox();before=await read();
    await page.mouse.move(r.x+r.width*.25,r.y+r.height/2);await page.mouse.down();await page.mouse.move(r.x+r.width*.7,r.y+r.height/2,{steps:14});
    state=await read();assert.equal(state.undo,before.undo);assert(state.transaction);assert.equal(Number(await page.locator('#person-height').inputValue()),state.data.pieces[0].height);
    await page.mouse.up();assert.equal((await read()).undo,before.undo+1);
    before=await read();r=await slider.boundingBox();await page.mouse.move(r.x+r.width*.5,r.y+r.height/2);await page.mouse.down();await page.mouse.move(r.x+r.width*.3,r.y+r.height/2,{steps:5});await page.keyboard.press('Escape');await page.mouse.up();assert.deepEqual((await read()).data,before.data);assert.equal((await read()).undo,before.undo);
    await slider.focus();await slider.press('Home');assert.equal((await read()).data.pieces[0].height,1400);await slider.press('ArrowRight');assert.equal((await read()).data.pieces[0].height,1410);await slider.press('End');assert.equal((await read()).data.pieces[0].height,2200);
    console.log('PASS real slider drags, cancellation, native keyboard focus, 10 mm arrows and inclusive Home/End');

    before=await read();await page.selectOption('#person-category','child');state=await read();assert.equal(state.data.pieces[0].height,1700);assert.equal(state.undo,before.undo+1);assert.match(await page.locator('#person-feedback').innerText(),/2200|2,200/);
    assert.equal(await slider.getAttribute('min'),'600');assert.equal(await slider.getAttribute('max'),'1700');assert.equal(await page.locator('#person-height').inputValue(),'1700');assert.match(await page.locator('#person-min').innerText(),/600/);
    await number('#person-height',1500);await page.selectOption('#person-category','adult');assert.equal((await read()).data.pieces[0].height,1500);await page.selectOption('#person-category','child');assert.equal((await read()).data.pieces[0].height,1500);
    await number('#person-height',600);await page.selectOption('#person-category','adult');assert.equal((await read()).data.pieces[0].height,1400);
    before=await read();await page.selectOption('#person-variant','woman');state=await read();assert.deepEqual({...state.data.pieces[0],variant:'man'},before.data.pieces[0]);await page.locator('#undo').click();assert.equal((await read()).data.pieces[0].variant,'man');await page.locator('#redo').click();assert.equal((await read()).data.pieces[0].variant,'woman');
    await page.selectOption('#person-category','child');await number('#person-height',1200);
    for(const [unit,height,step,min,max] of [['cm','120','1','60','170'],['m','1.2','0.01','0.6','1.7'],['mm','1200','10','600','1700']]){
      before=await read();await page.locator('#person-unit').click();assert.equal(await page.locator('#person-height').inputValue(),height);assert.equal(await slider.inputValue(),height);assert.equal(await slider.getAttribute('step'),step);assert.equal(await slider.getAttribute('min'),min);assert.equal(await slider.getAttribute('max'),max);assert.deepEqual((await read()).data,before.data);
      await slider.focus();await slider.press('ArrowRight');assert.equal((await read()).data.pieces[0].height,1210);await slider.press('ArrowLeft');assert.equal((await read()).data.pieces[0].height,1200);
    }
    // Preserve typed/imported precision even off the slider's base grid.
    await number('#person-height',1234.56);assert.equal(await slider.inputValue(),'1234.56');await slider.press('ArrowRight');assert.equal((await read()).data.pieces[0].height,1244.56);
    await page.locator('#person-height').fill('1300');await page.locator('#clear').click();assert.equal((await read()).data.pieces[0].height,1300);assert.equal((await read()).transaction,null);
    await page.locator('#select-all').click();before=await read();await page.locator('#copy').click();await page.locator('#paste').click();state=await read();assert.equal(state.data.pieces.length,2);assert.equal(state.data.pieces[1].height,1300);assert.equal(state.data.pieces[1].variant,'woman');assert.equal(state.data.pieces[1].category,'child');
    await page.locator('#delete').click();assert.equal((await read()).data.pieces.length,1);await page.locator('#undo').click();assert.equal((await read()).data.pieces.length,2);
    const saved=(await read()).data,json=await download('#export','people.json');assert.deepEqual(JSON.parse(fs.readFileSync(json,'utf8')),saved);await page.reload();await page.waitForFunction(()=>globalThis.pvcTest);assert.deepEqual((await read()).data,saved);
    await load(JSON.parse(fs.readFileSync(json,'utf8')));
    console.log('PASS category preservation/clamping, variants/history, all units and precision, blur/selection commits, copy/delete, JSON and autosave reload');

    // Coincident references and PVC have no collision restrictions or inferred joints.
    const mixed=rectangle(),tube=mixed.pieces.find(p=>p.type==='tube'),ref=mixed.add('person',[tube.p[0],0,tube.p[2]]),ref2=mixed.add('person',[tube.p[0],0,tube.p[2]]);mixed.updatePerson(ref2.id,{variant:'woman'});
    await load(mixed.data());await page.locator('#clear').click();await page.locator('#frame').click();await pick(ref);assert.deepEqual((await read()).selected,[ref.id]);
    before=await read();await number('#position-x',tube.p[0]+120);assert.deepEqual((await read()).data.connections,before.data.connections);assert.deepEqual((await read()).data.pieces.find(p=>p.id===tube.id),tube);
    await number('#rotation-y',45);await number('#person-height',2200);validate((await read()).data);
    await page.locator('#clear').click();await page.locator('#frame').click();await pick(tube);await page.locator('#select-assembly').click();state=await read();assert(!state.selected.includes(ref.id));assert(!state.selected.includes(ref2.id));
    before=await read();await page.locator('[data-turn="y"]').first().click();state=await read();assert.deepEqual(state.data.pieces.filter(p=>p.type==='person'),before.data.pieces.filter(p=>p.type==='person'));validate(state.data);
    // Explicit mixed multi-selection transforms rigidly, preserving existing joints.
    await page.locator('#select-all').click();assert(await page.locator('#group-length-section').isHidden());assert(await page.locator('#person-section').isHidden());before=await read();
    await number('#position-y',180);await page.locator('[data-turn="y"]').first().click();await number('#rotation-z',20);state=await read();validate(state.data);assert.equal(state.data.connections.length,mixed.connections.length);
    for(const piece of state.data.pieces)for(const other of state.data.pieces){const distance=(a,b)=>Math.hypot(...a.map((v,i)=>v-b[i]));assert(Math.abs(distance(piece.p,other.p)-distance(before.data.pieces.find(p=>p.id===piece.id).p,before.data.pieces.find(p=>p.id===other.id).p))<1e-6);}
    assert.equal(await page.locator('#summary-count').innerText(),'8 pieces');assert.match(await page.locator('#reference-count').innerText(),/2/);assert.equal(await page.locator('#total-length').innerText(),'1,800 mm');assert(!await page.locator('#summary').innerText().then(t=>t.includes('Person')));
    console.log('PASS overlapping references/PVC, independent movement/rotation/height, no companions, explicit mixed transforms with intact joints and PVC-only totals');

    // Pointer-based individual movement and rotation buttons.
    await page.locator('#clear').click();await page.selectOption('#camera','front');await page.selectOption('#plane','front');await page.locator('#frame').click();
    let person=(await read()).data.pieces.find(p=>p.id===ref2.id);await pick(person);await number('#rotation-x',0);await number('#rotation-y',0);await number('#rotation-z',0);await page.locator('#frame').click();person=(await read()).data.pieces.find(p=>p.id===ref2.id);
    let pt=await screen([person.p[0],person.p[1]+person.height*.93,person.p[2]]);await page.mouse.dblclick(pt.x,pt.y);assert.equal((await read()).tool,'move-piece');before=await read();
    await page.mouse.move(pt.x,pt.y);await page.mouse.down();await page.mouse.move(pt.x+35,pt.y+15,{steps:10});assert.equal((await read()).candidate,null);await page.mouse.up();assert.equal((await read()).undo,before.undo+1);assert.deepEqual((await read()).data.connections,before.data.connections);await page.keyboard.press('Escape');
    before=await read();await page.locator('[data-turn="y"]').first().click();assert.equal((await read()).undo,before.undo+1);validate((await read()).data);
    await page.locator('#clear').click();await page.locator('#select-all').click();before=await read();
    for(const view of ['front','side','top','perspective']){await page.selectOption('#camera',view);await page.locator('#frame').click();await page.waitForTimeout(180);assert.deepEqual((await read()).data,before.data);assert((await page.evaluate(()=>pvcTest.bounds())).excess<1e-5);await page.screenshot({path:path.join(out,view+'.png')});}
    for(const width of [600,320]){await page.setViewportSize({width,height:1050});await page.locator('#clear').click();await page.locator('#frame').click();await page.screenshot({path:path.join(out,'narrow-'+width+'.png'),fullPage:true});assert(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth));}
    await page.setViewportSize({width:1440,height:1050});await page.locator('#select-all').click();await page.locator('#frame').click();
    before=await read();const pdf=await download('#download-pdf','mixed.pdf');assert(fs.statSync(pdf).size>25000);assert.deepEqual((await read()).data,before.data);assert.match(await page.locator('#status').innerText(),/3 pages/);
    // Reference-only documents keep the same materials + eight-view PDF structure.
    const refs=new Design();refs.add('person',[0,0,0]);const woman=refs.add('person',[500,0,0]);refs.setPersonCategory(woman.id,'child');refs.updatePerson(woman.id,{variant:'woman',height:1200});await load(refs.data());await download('#download-pdf','references-only.pdf');
    console.log('PASS real pointer movement, rotations, camera presets/Frame, live selection dimensions, 600/320px layouts and mixed/reference-only PDF downloads');
    assert.deepEqual(errors,[]);console.log('PASS no browser JavaScript errors');
  }finally{await browser.close();}
})().then(()=>server.close()).catch(error=>{console.error(error);server.close();process.exitCode=1;});
