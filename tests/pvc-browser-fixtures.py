"""Generate disposable, instrumented fixtures for PVC browser regression tests.

Run python tests/pvc-browser-fixtures.py, serve the repository normally, then
open /tests/pvc-interactions.html. Production files have no observation hooks.
The generated app uses separate local-storage keys and is ignored by Git.
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HOOKS = '''
globalThis.pvcTest = {
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
    cameraQ:camera.quaternion.toArray(),gizmoDragging:gizmo.dragging}),
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
