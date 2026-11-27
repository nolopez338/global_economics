# Person reference checks

From the repository root:

```powershell
node --test tests/pvc-person.test.mjs tests/pvc-model.test.mjs tests/pvc-standard.test.mjs tests/pvc-placement.test.mjs tests/pvc-coordinated-resize.test.mjs tests/pvc-rotation.test.mjs tests/pvc-templates.test.mjs tests/pvc-bounds.test.mjs
python tests/pvc-browser-fixtures.py
node tests/pvc-person.browser.cjs
python tests/pvc-person-pdf-check.py
```

The browser suite requires Playwright and installed Chrome. An existing package
installation can be supplied through `NODE_PATH`; `PVC_BROWSER` can select another
Chromium executable. It serves this repository on localhost and uses actual Chrome
with software WebGL. It first checks the shipped page, then the generated fixture
with separate test storage. Fixture hooks observe state and geometry; edits run
through UI controls, file inputs, native catalog dragging, and pointer/keyboard
events. No application dependencies are added.

Model tests cover both silhouettes and categories; actual 1800 mm bounds;
inclusive limits and strict invalid-data rejection; proportional scaling and fixed
soles/transforms; category preservation/clamping; missing-property defaults;
independent instances; copy/paste and snapshots; older PVC-only designs; absence of
ports, snapping and joints; free overlap and coherent explicit mixed transforms;
PVC-only quantities; unchanged templates; and all-corner PDF camera containment.

The browser suite covers numeric/slider synchronization and live bounds; one-step
history; Escape, blur, selection changes, arrows and Home/End; all display units and
fine numeric precision; category/variant changes; actual click/drag placement;
overlap, individual and mixed transforms; autosave/reload; JSON downloads/import;
camera presets, Frame, narrow 600/320px layouts; and mixed/reference-only PDF
downloads. Outputs and screenshots are written under ignored `tmp/pvc-person/`.

The PDF checker verifies three A4 pages, eight complete images and labels,
construction-only totals and a separate reference count. Render the downloaded
PDFs and inspect the pages as well as browser screenshots. Automated assertions
and visual inspection are separate checks; neither establishes behavior on every
browser/GPU or confirms a screen reader's spoken delivery.
