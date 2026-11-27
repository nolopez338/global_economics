// Run from the repository root: python tests/pvc-browser-fixtures.py &&
// node tests/pvc-placement.browser.cjs. Requires Playwright and Chrome.
// PVC_BROWSER optionally supplies an alternative Chromium executable.
const assert=require('node:assert/strict');
const fs=require('node:fs');
const path=require('node:path');
const http=require('node:http');
const {chromium}=require('playwright');
const root=process.cwd(),out=path.join(root,'tmp/pvc-placement');
fs.mkdirSync(out,{recursive:true});
const mime={'.html':'text/html','.js':'text/javascript','.mjs':'text/javascript','.css':'text/css','.svg':'image/svg+xml'};
const server=http.createServer((req,res)=>{
  const file=path.resolve(root,'.'+decodeURIComponent(req.url.split('?')[0]));
  if(!file.startsWith(root+path.sep)){res.writeHead(403);res.end();return;}
  fs.readFile(file,(error,body)=>{res.writeHead(error?404:200,{'Content-Type':mime[path.extname(file)]||'application/octet-stream'});res.end(error?'Not found':body);});
});
(async()=>{
  await new Promise(resolve=>server.listen(0,'127.0.0.1',resolve));
  const origin=`http://127.0.0.1:${server.address().port}`;
  const browser=await chromium.launch({...(process.env.PVC_BROWSER?{executablePath:process.env.PVC_BROWSER}:{channel:'chrome'}),headless:true,args:['--use-angle=swiftshader','--enable-unsafe-swiftshader']});
  try{
    if(!process.env.PVC_SKIP_INTERACTIONS&&!process.env.PVC_ONLY_STATIONARY){
    const page=await browser.newPage({viewport:{width:1440,height:1100}}),errors=[];
    page.setDefaultTimeout(120000);page.on('pageerror',error=>errors.push(error.message));
    await page.exposeFunction('reportPVCResult',text=>console.log(text));
    await page.goto(origin+'/tests/pvc-interactions.html');
    await page.evaluate(()=>{
      const seen=new Set();new MutationObserver(()=>{
        for(const li of document.querySelectorAll('#results li'))if(li.textContent&&!seen.has(li)){
          seen.add(li);reportPVCResult(li.textContent);
        }
      }).observe(document.querySelector('#results'),{childList:true,subtree:true});
    });
    await page.waitForFunction(()=>/^(PASS|FAIL)/.test(document.title),{},{timeout:240000});
    const interactions=await page.locator('#results').innerText();
    assert(!interactions.includes('FAIL'),'DOM interaction suite failed');assert.deepEqual(errors,[]);
    await page.close();
    }
    if(process.env.PVC_ONLY_INTERACTIONS)return;
    for(const dpr of [1,2]){
      const context=await browser.newContext({viewport:{width:1440,height:1100},deviceScaleFactor:dpr});
      const page=await context.newPage(),errors=[];
      page.on('pageerror',error=>errors.push(error.message));page.setDefaultTimeout(120000);
      const read=()=>page.evaluate(()=>pvcTest.read());
      const load=async type=>{
        await page.goto(origin+'/tests/.pvc-browser/pvc_design.html');await page.waitForFunction(()=>globalThis.pvcTest);
        await page.evaluate(async type=>{
          const {Design}=await import('/assets/js/pvc-model.mjs');const m=new Design();m.add(type,[0,120,0]);
          localStorage.setItem('pvc-studio-browser-test',JSON.stringify(m.data()));localStorage.setItem('pvc-studio-browser-test-increment','90');
        },type);
        await page.reload();await page.waitForFunction(()=>globalThis.pvcTest);
      };
      const target=async()=>page.evaluate(async()=>{
        const {Design}=await import('/assets/js/pvc-model.mjs');const {placementTargets}=await import('/assets/js/pvc-placement.mjs');
        const t=placementTargets(new Design(pvcTest.read().data))[0];return pvcTest.screen(t.position.toArray());
      });
      if(!process.env.PVC_ONLY_STATIONARY){
      await load('cap');
      for(const view of ['front','side','top','perspective']){
        await page.selectOption('#camera',view);await page.selectOption('#plane',view==='side'?'side':view==='front'?'front':'ground');
        // Zoom while camera controls are enabled, before catalog selection.
        const canvas=page.locator('#workspace canvas'),box=await canvas.boundingBox();
        await page.mouse.move(box.x+box.width/2,box.y+box.height/2);await page.mouse.wheel(0,-180);
        await page.locator('[data-type="tube"]').click();const at=await target();
        for(const distance of [128,191.75]){await page.mouse.move(at.x,at.y+distance);assert((await read()).placement.connection,`DPR ${dpr}, ${view}, ${distance}px acquisition`);assert(await page.locator('#placement-guide').isVisible());}
        await page.mouse.move(at.x,at.y+192.25);assert.equal((await read()).placement.connection,null,`DPR ${dpr}, ${view} release`);assert(await page.locator('#placement-guide').isHidden());
        await page.keyboard.press('Escape');
      }
      console.log(`PASS real mouse 192 CSS-pixel targeting at DPR ${dpr}, four cameras and zoom`);
      }
      await load('cap');await page.selectOption('#camera','front');await page.selectOption('#plane','front');
      await page.locator('[data-type="tube"]').click();const stationary=await target();await page.mouse.move(stationary.x,stationary.y+40);
      assert((await read()).placement.connection);
      const guideMatches=()=>page.evaluate(()=>{
        const s=pvcTest.read(),connection=s.placement?.connection;if(!connection)return false;
        const canvas=document.querySelector('#workspace canvas'),r=canvas.getBoundingClientRect(),guide=document.querySelector('#placement-guide'),circle=guide.querySelector('circle');
        const target=s.data.pieces.find(p=>p.id===connection.target.id);
        return import('/assets/js/pvc-model.mjs').then(({port})=>{
          const projected=pvcTest.screen(port(target,connection.target.port).position.toArray());
          return !guide.hasAttribute('hidden')&&Math.abs(Number(circle.getAttribute('cx'))-(projected.x-r.left))<1e-6&&Math.abs(Number(circle.getAttribute('cy'))-(projected.y-r.top))<1e-6;
        });
      });
      await page.selectOption('#camera','top');assert(await guideMatches(),'Camera switch left stationary preview guide at old projection');
      await page.setViewportSize({width:1520,height:1140});
      await page.waitForFunction(()=>document.querySelector('#workspace canvas').width===Math.round(document.querySelector('#workspace').clientWidth*Math.min(devicePixelRatio,2)));
      assert(await guideMatches(),'Resize left stationary preview guide at old projection');
      await page.keyboard.press('Escape');assert(await page.locator('#placement-guide').isHidden());
      await page.setViewportSize({width:1440,height:1100});
      console.log(`PASS stationary pointer camera/resize retargeting and guide visibility at DPR ${dpr}`);
      if(process.env.PVC_ONLY_STATIONARY){assert.deepEqual(errors,[]);await context.close();continue;}
      await load('tube');await page.selectOption('#camera','front');
      const at=await target(),button=page.locator('[data-type="corner"]'),box=await button.boundingBox();
      const base=await read();
      await page.mouse.move(box.x+box.width/2,box.y+box.height/2);await page.mouse.down();
      await page.mouse.move(at.x,at.y+128,{steps:20});
      await page.waitForFunction(()=>pvcTest.read().placement?.connection);
      const mesh=(await read()).previewMesh;
      // Chromium may suppress hardware key events during native HTML dragging.
      // Check delivered keys, and also exercise the browser-delivered DOM path.
      await page.evaluate(()=>{globalThis.deliveredRotationKeys=0;addEventListener('keydown',e=>{if(e.key==='q')deliveredRotationKeys++;});});
      const beforeKey=(await read()).placement;
      await page.keyboard.press('q');
      const delivered=await page.evaluate(()=>deliveredRotationKeys);
      if(!delivered)await page.evaluate(()=>document.querySelector('canvas').dispatchEvent(new KeyboardEvent('keydown',{key:'q',bubbles:true,cancelable:true})));
      const rotated=(await read()).placement;
      assert.notDeepEqual(rotated.intentQ,beforeKey.intentQ,'Rotation during native drag was ignored');
      await page.mouse.move(at.x+2,at.y+127);
      await page.waitForFunction(()=>pvcTest.read().placement?.connection);
      const preview=(await read()).placement;
      assert.deepEqual(preview.q,rotated.q,'Native drag pointer update undid orientation');
      assert.equal((await read()).previewMesh,mesh);assert.deepEqual((await read()).data,base.data);
      await page.locator('#workspace').screenshot({path:path.join(out,`native-drag-dpr${dpr}.png`)});
      await page.mouse.up();await page.waitForFunction(()=>!pvcTest.read().placement);
      const placed=await read(),added=placed.data.pieces.at(-1),joint=placed.data.connections.at(-1);
      assert.deepEqual(added.p,preview.p);assert.deepEqual(added.q,preview.q);
      assert.equal(joint.a.port,preview.connection.source);assert.deepEqual(joint.b,preview.connection.target);
      assert.equal(placed.undo,1);assert.deepEqual(JSON.parse(placed.autosave),placed.data);
      await page.locator('#undo').click();assert.deepEqual((await read()).data,base.data);
      await page.locator('#redo').click();assert.deepEqual((await read()).data,placed.data);
      console.log(`PASS native drag exact commit, rotation (${delivered?'hardware key delivered':'Chromium suppressed hardware key; DOM key delivered'}), mesh reuse, autosave and undo/redo at DPR ${dpr}`);
      await load('cap');await page.selectOption('#camera','front');await page.selectOption('#plane','front');
      await page.locator('#port-snap').uncheck();
      const freeAt=await target(),tubeBox=await page.locator('[data-type="tube"]').boundingBox();
      await page.mouse.move(tubeBox.x+tubeBox.width/2,tubeBox.y+tubeBox.height/2);await page.mouse.down();
      await page.mouse.move(freeAt.x,freeAt.y,{steps:20});await page.waitForFunction(()=>pvcTest.read().placement);
      const free=(await read()).placement;assert.equal(free.connection,null);
      assert(await page.locator('#placement-guide').isHidden());
      await page.mouse.up();await page.waitForFunction(()=>!pvcTest.read().placement);
      assert.equal((await read()).data.connections.length,0);assert.deepEqual((await read()).data.pieces.at(-1).p,free.p);
      await page.locator('#undo').click();await page.locator('#port-snap').check();
      const cancelBase=await read(),cancelAt=await target(),cancelBox=await page.locator('[data-type="tube"]').boundingBox();
      await page.mouse.move(cancelBox.x+cancelBox.width/2,cancelBox.y+cancelBox.height/2);await page.mouse.down();
      await page.mouse.move(cancelAt.x,cancelAt.y,{steps:20});await page.waitForFunction(()=>pvcTest.read().placement?.connection);
      await page.keyboard.press('Escape');await page.mouse.up();await page.waitForFunction(()=>!pvcTest.read().placement);
      assert.deepEqual((await read()).data,cancelBase.data);assert.equal((await read()).undo,cancelBase.undo);
      assert(await page.locator('#placement-guide').isHidden());
      console.log(`PASS native drag snapping disabled and Escape cancellation at DPR ${dpr}`);
      assert.deepEqual(errors,[]);await context.close();
    }
  }finally{await browser.close();}
})().then(()=>server.close()).catch(error=>{console.error(error);server.close();process.exitCode=1;});
