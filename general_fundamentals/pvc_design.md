# PVC Studio

Open `general_fundamentals/pvc_design.html` through the repository's normal
static server (`start-project.bat`, or `python -m http.server 8000` at the root).
No build, backend, npm installation, or runtime CDN is required.

## Files and geometry contract

- `assets/js/pvc-model.mjs`: structured catalog, local ports, graph traversal,
  rigid transforms, cut-length editing, copying, materials and import validation.
- `assets/js/pvc-app.mjs`: hollow geometry, Three.js scene and controls,
  selection, snap preview, gesture transactions, persistence and inspector.
- `assets/css/pvc-design.css`: scoped application styling and responsive panels.
- `assets/vendor/three-0.170.0/`: pinned Three.js modules and MIT license.
- `tests/pvc-model.test.mjs`: independent construction-model regression tests.

Coordinates and dimensions use millimetres. All tubes have a 16 mm outer
radius and 13 mm inner radius. Tube length is the physical cut length,
including inserted material; allowed lengths are 80–3,000 mm. Tube local X
is its longitudinal axis; end 1 is −X and end 2 is +X. Fitting socket mouths
are 45 mm from the local origin, and their internal mating stops are 20 mm
inside their mouths. The tube end aligns with that stop, with opposing outward
directions. Socket walls are thicker than tube walls.

Joints are graph edges with stable IDs and explicit piece/port endpoints.
Proximity only proposes a new joint; existing joints never depend on mesh
positions or ongoing proximity. The rigid transform includes all selected
pieces and their connected companions. A snap applies the same correction to
that entire moving selection, including disconnected selected assemblies.
Closing a loop requires matching mating datums within 0.05 mm and opposing
directions within the model's dot-product tolerance. No component is scaled
or bent to satisfy a joint.

Both-end length editing traverses the graph with the selected tube excluded.
If the two branches are independent, end 1 stays fixed and the end 2 branch
translates. If an alternate path still joins the branches, length editing is
disabled and a specific incident joint is identified for detachment. Detaching
one edge never moves pieces or automatically breaks other edges.

The JSON contract is `format: pvc-studio`, `version: 1`, `catalog: pvc-32-v1`,
`units: mm`, `radius: 16`, plus pieces and connections. Import checks transforms,
normalized quaternions, ID uniqueness, port compatibility and occupancy, tube
lengths, endpoint references and all joint geometry before replacement.
Import limits are 5 MB, 2,000 pieces and 6,000 joints. Browser autosave uses
`pvc-studio-v1` in local storage. Undo/redo retains up to 80 completed actions
in the current session; history and the copy buffer are not persisted.

## Interaction controls

Q rotates horizontally about world Y; E rotates vertically about world X.
The toolbar has corresponding labeled buttons. Options includes a rotation
increment, defaulting to 90°, with 15°, 30°, 45°, 90° and custom positive values.
All discrete rotation buttons use the same increment and update their labels.
The preference is stored separately as `pvc-studio-rotation-increment`; exported
design JSON remains version 1 with no preference fields. Placement rotations
edit the preview; selection rotations transform the selected pieces and every
connected companion as one rigid group about the selection centre.

In normal Select mode, left drag pans, right drag orbits and scroll zooms.
Middle drag can also pan. A four CSS-pixel threshold separates clicks from
drags; selection is resolved on release, so camera panning over a piece neither
selects nor moves it. Shift-click toggles pieces; the explicit Marquee tool
selects piece centres within its rectangle.

Double-click a piece to select it and enter Piece movement mode. A persistent
banner identifies this mode, selected pieces are teal, and connected companions
are amber. Drag a piece to translate the entire highlighted group on a plane
parallel to the chosen working plane, through that piece's current position.
The grab-point offset is preserved. Grid snapping rounds the translation delta,
so enabling the grid does not first relocate an off-grid piece. The configured
plane offset still controls placement but does not relocate existing pieces.
Translation gizmos and numeric controls remain available.

Compatible free ports show a cyan snap preview; releasing commits the rigid
alignment and new persistent joint in the same undo action as the drag.
Movement mode remains active after release. Escape or Select exits; Escape
during a piece or gizmo drag restores its starting geometry without recording
an action. Gesture ownership prevents camera, placement, marquee, direct piece
movement and gizmos from processing the same left drag. Keyboard shortcuts are
ignored in inputs, selects, textareas and editable text; active gestures accept
Escape and defer other shortcuts until release.

## Verification

Run `node --test tests/pvc-model.test.mjs` from the repository root.
All 11 model tests pass, covering insertion, rigid movement, independent pieces
after detachment, free/one-ended/two-ended resizing, rotated branches,
alternate paths, rectangular closed loops, rejected inconsistent closure,
copy/paste with fresh IDs, materials, JSON round trips and malformed imports.

For repeatable browser regression tests, run
`python tests/pvc-browser-fixtures.py`, serve the repository normally, and open
`tests/pvc-interactions.html`. The generator copies the current implementation
into ignored `tests/.pvc-browser/` files, adding read-only observation hooks
only to that test copy. Separate test storage keys protect ordinary autosaves
and preferences. Regenerate after changing production sources.

All 12 browser scenarios pass in Chromium with WebGL: Q/E during placement
and selection, world axes, presets/custom increments and local persistence,
on-screen rotations, rigid connected and disconnected selections, left pan,
right orbit, wheel zoom, the click threshold, click/Shift-click, marquee,
double-click movement, all three working planes, no offset/grid jump, snapping,
Escape cancellation, typing protection, gizmo availability and cancellation,
and exact drag/discrete-rotation undo/redo counts. The suite sends DOM keyboard
and pointer events through the real controls and validates resulting joints.
Native browser input also verified preview Q/E, double-click mode entry,
translation, Q/E on a connected selection, undo and Escape exit. Desktop and
narrow layouts were visually inspected. Cross-browser and touch-device QA
remain outside this verification.

Browser QA used the working page in the in-app Chromium browser:

1. Placed a hollow tube, placed an elbow near its end, and confirmed automatic
   snap and one committed joint. Also tested inspector-based port connection.
2. Moved the connected pair with the translation gizmo and rotated it with a
   rotation ring; the connection remained intact.
3. Detached a selected joint, undid and redid the detachment, and moved the
   detached tube independently while its elbow stayed in place.
4. Changed length with the numeric control and the synchronized range control.
   Tested one attached end, then a tube between an elbow and a tee: both joints
   remained intact while the opposite branch translated.
5. Copied and pasted a two-piece selection; counts changed from two pieces /
   one joint to four pieces / two joints, with the pasted pieces selected.
6. Opened the eight-piece rectangular frame. Confirmed its length lock, used
   Show blocking joint and Detach, resized the open tube, then attempted to
   reconnect the loop: the inconsistent closure was rejected without mutation.
7. Exported JSON and imported that actual downloaded file; the four pieces,
   one remaining joint and 1,400 mm cut total matched the export. Reload also
   restored the autosaved design.
8. Checked materials quantities and changing cut totals throughout construction.
9. Tested all four camera presets, marquee selection, Shift-click add/remove,
   catalog drag-and-drop, placement cancellation, and dismissible help.
10. Inspected the three-panel layout at 1280×720 and 1366×768, and the stacked
    layout at 390×844. Narrow-screen properties are below the workspace; panels
    scroll independently on desktop. No browser console errors were reported.
11. Moved two disconnected selected tubes into snapping range of an elbow.
    Both tubes received the same rigid snap correction, retaining their
    spacing and relative rotation; only the mating tube gained a joint.

## Deliberate scope

This is a geometric furniture planner, not a structural or manufacturing
certification tool. Fittings use schematic hollow socket geometry rather than
vendor-specific CAD/CSG solids. The tool does not perform collision detection,
load/strength calculations, stock-length nesting or manufacturing-tolerance
analysis. Marquee selection tests piece centres. Camera views use mouse
controls; touch-specific multi-finger camera gestures are not provided.
Autosave belongs to this browser and origin; JSON is the portable backup.
