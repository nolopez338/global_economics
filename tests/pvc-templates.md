# PVC Studio planning templates

The Materials panel offers exactly ten options. Changing the option only previews its description and dimensions; **Load template** uses the existing replacement prompt, creates one history entry, clears temporary editing state, autosaves, updates materials, and frames the assembly. Empty uses the same replacement path. The original rectangular fixture remains available to model regression tests.

All nonempty assemblies are tube-and-fitting graphs with a joint at both ends of every tube. They use rear and side triangles, lower rails and intermediate supports. Tall narrow shapes also have braced outriggers. Front is +Z. The window template has no brace or intermediate post across the upper front opening; rear reinforcement remains visible through it.

These are geometric planning templates without load ratings or certified strength. Tops, shelves, liners and panels are not included. Custom junctions require compatible sourcing or fabrication.

## Window dimensions and cut list

Dimensions include fitting geometry and 20 mm insertion at each tube end:

- Main box: **1542 W × 2242 H × 392 D mm**; centerline box 1500 × 2200 × 350 mm.
- Complete footprint with four outriggers: **1542 × 1088 mm**.
- Sill center: 1121 mm above the floor, exactly halfway between the lower and upper rail centerlines.
- Clear upper front opening between the perimeter sleeves: approximately **1458 W × 1058 H mm**.
- 108 pieces, 150 recorded joints, 75 tubes; total physical tube cuts **39164 mm**.
- Straight cuts: 300 mm × 17, 500 mm × 22, 700 mm × 16.
- Diagonal cuts: **482 mm × 12**, **760 mm × 8**.

Every axial cut in all nine templates is a multiple of 100 mm. The following whole-mm diagonal cuts are the only exceptions:

| Template | Diagonal cuts (mm) |
| --- | --- |
| Window-ready box frame | 482, 760 |
| Reinforced shelving frame | 608, 681 |
| Worktable frame | 621 |
| Compact desk frame | 482 |
| Freestanding clothes rack | 541, 608 |
| Shoe rack | 325, 482 |
| Plant stand | 482, 608 |
| Laundry hamper frame | 541 |
| Freestanding display frame | 621, 749 |

## Custom junction representation

Existing catalog fittings are used whenever their directions and reaches match. Other junctions use the `multiway` catalog entry with 2–8 serialized local `sockets`. Each socket has a normalized direction, a collinear mouth position, `type: "socket"`, and `insertion: 20`. Import validation restricts mouth reach to 44–106 mm and socket separation to at least 30 degrees. Geometry uses these same ports; connections still go through `Design.connect` and `Design.check`.

Axial socket mouths are 45 mm from the node center (25 mm internal stop). Diagonal mouths are approximately 105 mm from the center; rounding the physical diagonal cut to the nearest whole millimetre adjusts each neck by less than 0.25 mm. This gives exact seating without hidden gaps or a different insertion depth. Rotations, copying, undo/redo, JSON and autosave retain the socket array. Materials and PDFs count each distinct local socket configuration separately with an identifier; JSON carries the full socket layout. PDF materials overflow continues onto additional pages, followed by all eight views.

## Repeatable verification

Run from the repository root:

```powershell
node --test --test-isolation=none tests/pvc-model.test.mjs tests/pvc-placement.test.mjs tests/pvc-templates.test.mjs
python tests/pvc-browser-fixtures.py
node tests/pvc-templates.browser.cjs
```

The browser test requires Playwright and installed Chrome (set `NODE_PATH` to the bundled Node dependencies when needed). Its fixture uses separate browser-storage keys. It writes screenshots, portable JSON and the window PDF to `tmp/pvc-templates/`.

Model checks cover all ten options, unique IDs, cut limits and increments, compatible ports used once, alignment within 1e-8 mm, a single connected component, occupied tube ends, serialization, materials totals, copied / transformed assemblies, invalid custom sockets, unintended tube intersections, the window opening and rendered bounds. Browser checks load all nine nonempty options, capture front / side / perspective views, exercise rejected replacements and Empty, one-step undo/redo, placement reset, actual JSON downloads and imports, autosave reload, materials and PDF generation, and the narrow dropdown. Inspect the saved images for the visual checks.
