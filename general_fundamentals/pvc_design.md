# PVC Studio

Open `general_fundamentals/pvc_design.html` through the repository's normal
static server (`start-project.bat`, or `python -m http.server 8000` at the root).
No build, backend, npm installation, or runtime CDN is required.

## Files and geometry contract

- `assets/js/pvc-model.mjs`: structured catalog, local ports, graph traversal,
  rigid transforms, cut-length editing, copying, materials and import validation.
- `assets/js/pvc-templates.mjs`: ten structural pattern studies made from
  fixed standard fittings, with dimensions and explicit structural limitations.
- `assets/js/pvc-app.mjs`: hollow geometry, Three.js scene and controls,
  selection, snap preview, gesture transactions, persistence and inspector.
- `assets/css/pvc-design.css`: scoped application styling and responsive panels.
- `assets/vendor/three-0.170.0/`: pinned Three.js modules and MIT license.
- `tests/pvc-model.test.mjs`: independent construction-model regression tests.

Coordinates and dimensions use millimetres. All tubes have a 16 mm outer
radius and 13 mm inner radius. Tube length is the physical cut length,
including inserted material; allowed lengths are 80–3,000 mm. Tube local X
is its longitudinal axis; end 1 is −X and end 2 is +X. Standard fitting socket mouths
are 45 mm from the local origin, and their internal mating stops are 20 mm
inside their mouths. The tube end aligns with that stop, with opposing outward
directions. Socket walls are thicker than tube walls.

Only seven components are supported: straight tube, straight coupling, 90° elbow,
45° elbow, three-port tee, four-port cross and three-way corner (three mutually
perpendicular sockets). The deeply frozen catalog defines every socket count,
position, direction, insertion and compatibility. Piece records permit only
`id`, `type`, `p`, `q`, and `length` for tubes. Socket arrays, port definitions
and every other per-piece override are rejected, even if they match a standard
fitting. Removed components are never converted to standard parts.

The Template dropdown offers exactly ten nonempty structural patterns, ordered
from perimeter, ladder and grillage layouts through portal and box frames to
braced, multi-bay, pitched, re-entrant and polygonal arrangements. Use **New** to
clear the workspace. Template selection previews only; Load template validates
the complete graph before replacement, records one undoable, autosaved action,
and frames the view. All templates remain ordinary editable pieces and joints.
See [template geometry and verification](../tests/pvc-templates.md).

Template 6 is a rectangular tower with an exact rendered outer envelope of
1,300 mm width × 400 mm depth × 2,200 mm height. Six straight diagonal members
address width-height sway, depth-height sway and horizontal plan distortion.
Their endpoint tees rotate around transverse rails so the catalog's fixed
perpendicular branch points along the brace; no socket geometry changes.
The apparent width-height X uses two planes 98 mm apart, avoiding an
unconnected crossing. Intermediate width and depth ties use staggered heights
to keep every junction compatible with the available fittings.

These are geometric planning considerations, not certified structural analysis.
Rectangular bays and unglued sockets are not assumed rigid. Template 6 improves
the arrangement of axial load paths qualitatively; long-brace flexure and
buckling, socket rotation/slip/pullout and the shallow 400 mm tipping footprint
remain limitations. Bracing does not widen the support polygon. No safe load
ratings, guaranteed stability or quantitative stiffness claims are provided.
Actual performance depends on PVC dimensions and properties, connection methods,
assembly quality, support conditions and loading, including asymmetric or
elevated loads. Other templates identify their unbraced deformation mechanisms.

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

### Coordinated parallel-tube resizing

Select two or more tubes with Shift-click or Marquee to reveal **Change selected
tube lengths**. Its slider and numeric field show a signed adjustment, initially
zero, in the current mm/cm/m units. Every preview adds the same adjustment to
each starting cut; 500 and 700 mm become 600 and 800 mm with +100 mm. The shared
range is `[max(80 − startingLength), min(3000 − startingLength)]` mm, displayed
at the existing 0.001 mm precision. Reversed tube directions are supported.
Mixed tube/fitting and nonparallel selections retain all selected pieces and
show a specific disabled-state explanation.

`Design.coordinatedLengthPlan(ids)` checks world-axis parallelism with a cross
product tolerance of `1e-7` (unit directions, approximately radians), then removes
all selected tubes together from the connection graph. Each remaining connected
section is rigid and may only translate. For each selected tube, the translation
velocity at end 2 minus that at end 1 must equal its actual world direction, per
millimetre of shared adjustment. A graph potential solve enforces these equations
simultaneously. A tube whose ends remain in the same rigid section, or conflicting
translations around alternate selected paths, blocks the entire operation.
The solver never calls the single-tube resize method.

For each independent connected group, an attached rigid section stays fixed:
choose the section with the lowest selected mating endpoint projected onto the
tube axis, orienting that axis so its largest absolute world component is
positive (X/Y/Z breaks equal component ties). Equal projections use stable piece
IDs. Free ends have lower anchor priority than attached sections; completely
free tubes keep their centres. Selection order and reversed endpoint numbering
do not change the result. The inspector identifies the axis and anchor section
IDs. Other sections translate rigidly; fitting rotations, socket geometry, joint
identities and all unselected cuts remain unchanged.

`Design.resizeTogether(ids, delta)` builds and validates a complete candidate
before publishing it. Live UI previews always rebuild from the edit's fixed
starting snapshot. Invalid or empty input retains the last valid geometry.
Release a slider, press Enter or leave the numeric field to complete one undoable
edit and autosave it; the adjustment then resets to zero. Arrow/Home/End keys
operate the slider. Escape inside either control restores the starting snapshot
without history or autosave changes, including during a pointer drag. Changing
selection finishes the valid preview before updating the inspector.

**Template 7 verification selection:** load **Two-bay supported frame** and
Shift-click the four horizontal rails in its left bay. Their tube centres in mm
are `(-350, 21, -300)`, `(-350, 21, 300)`, `(-350, 821, -300)` and
`(-350, 821, 300)`; all four cut lengths are 650 mm. Each is individually locked
by a closed loop, while selecting all four permits coordinated resizing. With
+100 mm, all four become 750 mm, the left support section stays fixed and the
centre/right section translates +100 mm along X. With −100 mm, all four become
550 mm and that section translates −100 mm. The original shared range is
−570 to +2350 mm. Selecting only three of these rails is blocked by the remaining
unselected path.

The JSON contract is `format: pvc-studio`, `version: 1`, `catalog: pvc-32-v1`,
`units: mm`, `radius: 16`, plus pieces and connections. Import checks transforms,
normalized quaternions, ID uniqueness, port compatibility and occupancy, tube
lengths, endpoint references and all joint geometry before replacement. The same
validation protects constructors, manual creation, paste, autosave, history,
JSON exports and PDF materials. Invalid input leaves the current design intact
and reports an error. Invalid autosave remains in storage for manual recovery.
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

A seated final graph does not simulate the assembly path. Dry-fit partial,
unfixed subassemblies with the braces already in place before closing or fixing
loops; a brace cannot simply be inserted between two sockets of an already
rigid box. Check practical assembly order, insertion clearances, cut tolerances
and actual vendor fitting dimensions before fabrication. The exact Template 6
envelope describes this app's unchanged schematic geometry, not vendor CAD or
a guaranteed manufactured dimension.

## Verification

Run the model suites from the repository root:

```powershell
node --test --test-isolation=none tests/pvc-model.test.mjs tests/pvc-placement.test.mjs tests/pvc-templates.test.mjs tests/pvc-standard.test.mjs tests/pvc-coordinated-resize.test.mjs
```

The model suites cover the exact component allowlist, immutable socket geometry,
rejection of custom types and per-piece or endpoint overrides, atomic paste,
JSON/PDF input validation, connected templates, insertion, rigid transforms,
cut-length editing, graph constraints, materials and serialization.

Generate browser fixtures with `python tests/pvc-browser-fixtures.py`. These copy
the production implementation into ignored `tests/.pvc-browser/` files and add
observation and invalid-buffer injection hooks only to that test copy. Separate
storage keys protect ordinary autosaves and placement preferences. Regenerate
after changing production sources.

`tests/pvc-standard.browser.cjs` checks the seven-item catalog, invalid JSON,
paste, undo/redo and autosave rejection with unchanged state, JSON download and
all-seven-component PDF creation. `tests/pvc-templates.browser.cjs` covers all
ten template options, replacement prompts, history, autosave, JSON round trips,
PDF output, camera framing and responsive layout.

`tests/pvc-placement.browser.cjs` exercises DOM controls and real mouse/native
drag input, camera and working-plane modes, custom rotation increments, rigid
assembly edits, cut lengths and units, exact snap commits, copy/history and
Escape cancellation. Its native-input checks use device pixel ratios 1 and 2.
`tests/pvc-coordinated-resize.test.mjs` covers valid/blocked connected groups,
conflicting paths, reversed directions, rotated assemblies, unequal cuts, limits,
parallelism tolerance and fixed-snapshot fractional previews.
`tests/pvc-coordinated-resize.browser.cjs` checks the concrete Template 7 selection
with real Shift-clicks, numeric and mouse previews, every joint's alignment and
20 mm insertion throughout, shared limits, units, cancellation, atomic invalid
input, selection changes, undo/redo, totals and autosave. It saves before/preview/
after screenshots in ignored `tmp/pvc-coordinated-resize/`.
`tests/pvc-pdf.browser.cjs` checks real downloads, committed snapshots, export
state preservation, eight camera views, compact lists, overflow and rendering
errors. `tests/pvc-pdf-check.py` inspects downloaded PDF pages, materials,
quantities, exact cuts and embedded images using pypdf. Browser tests require
Playwright and Chrome. Cross-browser and touch-device QA remain outside scope.

## Deliberate scope

This is a geometric furniture planner, not a structural or manufacturing
certification tool. Fittings use schematic hollow socket geometry rather than
vendor-specific CAD/CSG solids. The tool does not perform collision detection,
load/strength calculations, stock-length nesting or manufacturing-tolerance
analysis. Marquee selection tests piece centres. Camera views use mouse
controls; touch-specific multi-finger camera gestures are not provided.
Autosave belongs to this browser and origin; JSON is the portable backup.
