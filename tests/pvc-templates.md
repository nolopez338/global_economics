# PVC Studio standard-component structural templates

The dropdown contains exactly ten nonempty structural patterns. **New** clears
the workspace. Selection previews only; Load validates before changing current
state, asks before replacing unexported work, and creates one undoable,
autosaved edit. Each assembly consists of ordinary editable pieces and joints.

| # | Pattern | Structural distinction and limitation |
| --- | --- | --- |
| 1 | Perimeter loop | A closed floor-level footprint; short rails bear at corner elbows. Its unbraced rectangle can rack. |
| 2 | Ladder frame | Three rungs distribute transverse support along two side rails. Rectangular bays remain unbraced; not a climbing ladder. |
| 3 | Two-axis grillage | A central cross joins intersecting rails into four bays, providing paths in both horizontal directions. No deck or diagonal restraint is assumed. |
| 4 | Wide-base portal | Two uprights and one overhead beam transfer reactions into a broad ground perimeter. Portal sway and socket rotation remain possible. |
| 5 | Closed space cell | Two rectangular perimeters and four columns form a basic eight-corner spatial cell. Its faces remain unbraced. |
| 6 | Braced rectangular tower | Six direct diagonals and staggered intermediate ties address three-dimensional deformation within the exact requested envelope. See below. |
| 7 | Two-bay supported frame | Six columns divide continuous upper and lower beams; mid-height transverse ties link front and rear. Central supports shorten spans, but the bays remain unbraced. |
| 8 | Gabled prism | Closed five-sided ends use inclined roof rails, 45° eaves and 90° ridges. Transverse purlins connect slope/post tees; longitudinal sway remains possible. |
| 9 | Re-entrant space frame | Six columns follow an L-shaped top and base. Noncrossing plan chords connect outline vertices 1–3 and 0–4; its vertical faces remain unbraced. |
| 10 | Polygonal ring cell | Octagonal hoops, eight columns and four radial ties meeting a cross distribute perimeter reactions. Radial ties couple opposite supports; vertical bays remain unbraced. |

All patterns use only straight tubes, couplings, 90° and 45° elbows, tees,
crosses and three-way corners. No component dimensions, socket angles,
functionality or compatibility rules are changed. A graph junction must match
a rigid rotation of one complete catalog fitting. Every tube end is seated
20 mm into a socket and recorded in the connection graph. Physical cuts can be
fractional millimetres; values are not rounded to force a loop closure.

## Template 6: exact outer envelope and reinforcement

World X is width, Y is height and Z is depth. Rendered bounds are
`[-650, 0, -200]` through `[650, 2200, 200]` mm: exactly **1,300 × 400 × 2,200 mm
(W × D × H)**. Corner centers are at X = ±629 mm, Y = 21/2179 mm and
Z = ±179 mm. The unchanged 21 mm fitting radius accounts for the outside
surfaces; these are not centerline dimensions.

Standard tees host six straight braces. Their run remains on a transverse
frame rail, and the whole fitting rolls so its fixed perpendicular branch
points at the opposite brace endpoint. No arbitrary socket definitions or
elbow chains are needed.

| Brace | Fitting center A (mm) | Fitting center B (mm) | Physical tube cut (mm, shown approximately) |
| --- | --- | --- | ---: |
| Width-height 1 | (−629, 21, −49) | (629, 2179, −49) | 2447.904721962 |
| Width-height 2 | (629, 21, 49) | (−629, 2179, 49) | 2447.904721962 |
| Depth-height left | (−429, 21, 179) | (−429, 2179, −179) | 2137.493542848 |
| Depth-height right | (429, 21, −179) | (429, 2179, 179) | 2137.493542848 |
| Lower plan | (−629, 200, −179) | (629, 200, 179) | 1257.948011199 |
| Upper plan | (−629, 2000, 179) | (629, 2000, −179) | 1257.948011199 |

Each cut is the fitting-center distance minus 50 mm, retaining the exact numeric
value in the design. The width-height diagonals lie in planes 98 mm apart;
the apparent X has no coincident, unconnected crossing. Opposite depth-height
braces distribute restraint across the width. Lower and upper plan diagonals
couple opposite columns and oppose plan distortion and twisting. Width ties at
Y = 970 mm and depth ties at Y = 1100 mm shorten column segments without asking
one junction to provide unavailable noncoplanar sockets. The 130 mm stagger
leaves a valid 80 mm connecting tube cut.

These are qualitative geometric improvements, not measured stiffness or
certified structural analysis. Long braces can flex or buckle; socket rotation,
slip and pullout depend on the connection method and assembly. The 400 mm depth
still limits resistance to overturning, especially under asymmetric or elevated
loading. Bracing does not enlarge the support polygon. No safe load rating or
guaranteed stability is claimed. PVC dimensions/properties, assembly quality,
connection methods, support conditions and use govern actual performance.

A seated final graph does not simulate the assembly path. Dry-fit partial,
unfixed subassemblies with the braces already in place before closing or fixing
loops; a brace cannot simply be inserted between two sockets of an already
rigid box. Check practical assembly order, insertion clearances, cut tolerances
and actual vendor fitting dimensions before fabrication. The exact Template 6
envelope describes this app's unchanged schematic geometry, not vendor CAD or
a guaranteed manufactured dimension.

## Verification

Model checks cover all ten IDs, fixed socket definitions, compatible ports used
once, fully seated tube ends, connected graphs, serialization/materials,
copying and rigid transforms, tube-wall clearance, exact rendered Template 6
bounds, its six brace paths and the staggered intermediate ties. Browser checks
exercise all template loads, camera framing, undo/redo, replacement prompts,
autosave, JSON export/import, PDF generation and responsive controls. Generated
fixtures use isolated storage keys; artifacts are written under `tmp/`.

Run from the repository root:

```powershell
node --test --test-isolation=none tests/pvc-model.test.mjs tests/pvc-placement.test.mjs tests/pvc-templates.test.mjs tests/pvc-standard.test.mjs
python tests/pvc-browser-fixtures.py
node tests/pvc-templates.browser.cjs
node tests/pvc-standard.browser.cjs
node tests/pvc-placement.browser.cjs
node tests/pvc-pdf.browser.cjs
```

Set `PVC_EDITS_ONLY=1` for the shorter load/rotate/undo/autosave browser pass.
The default pass also captures three views and exercises JSON and PDF exports.

Browser checks require Playwright and Chrome; set `NODE_PATH` to the local
bundled dependencies when needed. Template collision checks do not add general
collision detection or engineering analysis to the interactive application.
