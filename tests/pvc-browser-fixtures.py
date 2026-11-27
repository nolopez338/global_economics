"""Generate disposable, instrumented fixtures for PVC browser regression tests.

Run python tests/pvc-browser-fixtures.py, serve the repository normally, then
open /tests/pvc-interactions.html. Production files have no observation hooks.
The generated app uses separate local-storage keys and is ignored by Git.
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HOOKS = '''
globalThis.pvcTest = {
  bounds: () => {
    let excess=0;
    if(boundsOverlay.box){const b=boundsOverlay.box;scene.updateMatrixWorld(true);
      for(const id of selected)meshes.get(id)?.traverse(o=>{if(!o.isMesh)return;
        const positions=o.geometry.getAttribute('position'),v=new THREE.Vector3();
        for(let i=0;i<positions.count;i++){v.fromBufferAttribute(positions,i).applyMatrix4(o.matrixWorld);
          for(let a=0;a<3;a++){let d=0;for(let j=0;j<3;j++)d+=(v.getComponent(j)-b.center[j])*b.axes[a][j];excess=Math.max(excess,Math.abs(d)-b.size[a]/2);}
        }
      });
    }
    return {mode:boundsOverlay.mode,box:clone(boundsOverlay.box),state:boundsOverlay.state,
      visible:boundsOverlay.lines.visible,excess,computations:boundsOverlay.computations,
      positionCount:boundsOverlay.geometry.getAttribute('position').count,
      points:boundsOverlay.points?.length/3,workers:Number(!!boundsOverlay.worker),timer:Number(!!boundsOverlay.timer)};
  },
  setClipboard: data => {clipboard=clone(data);$("#paste").disabled=false;},
  setHistory: (direction,data) => {(direction==='undo'?undo:redo).push({data:clone(data),selected:[],joint:null});refresh();},
  read: () => ({data:model.data(),selected:[...selected],tool,
    undo:undo.length,redo:redo.length,placement:clone(placement),
    candidate:clone(candidate),rotationIncrement,selectedJoint,
    previewMesh:placementMesh?.uuid,
    pickedPorts:clone(pickedPorts),transaction:clone(transaction),exported,
    autosave:localStorage.getItem(STORAGE),lengthUnit,
    history:clone({undo,redo}),
    camera:camera.position.toArray(),target:orbit.target.toArray(),
    cameraQ:camera.quaternion.toArray(),gizmoDragging:gizmo.dragging,
    gizmoAxis:gizmo.axis,rotationDrag:rotationDrag&&{raw:rotationDrag.raw,held:rotationDrag.held,angle:gizmo.rotationAngle}}),
  rotationHandles: axis => {
    scene.updateMatrixWorld(true);
    return gizmo._gizmo.picker.rotate.children.filter(o=>o.name===axis).flatMap(o=>{
      const positions=o.geometry.getAttribute('position'),points=[];
      for(let i=0;i<positions.count;i++)points.push(pvcTest.screen(new THREE.Vector3().fromBufferAttribute(positions,i).applyMatrix4(o.matrixWorld).toArray()));
      return points;
    });
  },
  rotationPointer: degrees => {
    const angle=THREE.MathUtils.degToRad(degrees),axis=({X:[1,0,0],Y:[0,1,0],Z:[0,0,1]})[gizmo.axis];
    const tangent=axis&&vec(axis).cross(gizmo.eye),point=gizmo.pointStart.clone();
    if(!tangent||tangent.lengthSq()===0)point.applyAxisAngle(gizmo.eye,angle);
    else{
      // The drag plane faces the camera, while eye points from the pivot to
      // the camera. They differ when the selection is away from orbit.target.
      tangent.normalize();const normal=camera.getWorldDirection(new THREE.Vector3());
      const direction=tangent.clone().addScaledVector(normal,-normal.dot(tangent));
      point.addScaledVector(direction,angle*gizmo.worldPosition.distanceTo(camera.position)/(20*direction.dot(tangent)));
    }
    return pvcTest.screen(point.add(gizmo.worldPositionStart).toArray());
  },
  screen: p => {const v=vec(p).project(camera),r=canvas.getBoundingClientRect();
    return {x:r.left+(v.x+1)*r.width/2,y:r.top+(1-v.y)*r.height/2};}
};
'''

fixture = ROOT / 'tests/.pvc-browser'
fixture.mkdir(exist_ok=True)
source = (ROOT / 'assets/js/pvc-app.mjs').read_text(encoding='utf-8')
source = source.replace("'../vendor/", "'../../assets/vendor/").replace("'./pvc-", "'../../assets/js/pvc-")
source = source.replace("'pvc-studio-v1'", "'pvc-studio-browser-test'").replace("'pvc-studio-rotation-increment'", "'pvc-studio-browser-test-increment'")
(fixture / 'pvc-app.mjs').write_text(source + HOOKS, encoding='utf-8')
html = (ROOT / 'general_fundamentals/pvc_design.html').read_text(encoding='utf-8')
html = html.replace('../assets/', '../../assets/').replace('../../assets/js/pvc-app.mjs', './pvc-app.mjs')
(fixture / 'pvc_design.html').write_text(html, encoding='utf-8')
print('Open /tests/pvc-interactions.html on your normal static server.')
