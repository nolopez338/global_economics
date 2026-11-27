# Selection bounds

The compact box button next to Frame cycles **Off → World-aligned → Approximate
minimum-volume oriented → Off**. It starts Off and retains its mode as selection
changes. Its native button supports Enter/Space, visible focus, a 28 × 28 CSS-pixel
target, dynamic name/title, and a polite status announcement. A hollow dot,
filled square, and filled diamond distinguish the three states without using
boolean `aria-pressed` for a three-state value. Hover the button for the current
mode and next action; `≈` on oriented dimensions discloses the approximation.

## Geometry and accuracy

Only explicitly selected piece groups contribute. Traversal takes the rendered
mesh position vertices, including nested cylinder/ring/shell/body transforms;
piece world matrices include all ancestors. Ports, joint markers, ghosts,
grid/floor, and gizmos live outside these groups. Local deduplicated vertices are
cached in WeakMaps keyed by the immutable piece group; changing a cut replaces
that group. World-transformed vertices are reused while its world matrix is
unchanged. `pvc-geometry.mjs` and `pvc-model.mjs` need no modifications.

World mode takes exact coordinate minima/maxima over these vertices. Oriented
mode minimizes the product of the three support-plane widths over a freely
rotating orthonormal basis:

1. Normalize coordinates by the largest world extent and center them for
   numerical conditioning. Reduce to a deterministic QuickHull vertex set.
   Hull visibility tolerance is `1e-10` of the largest world extent. Very thin
   initial simplices fall back to all points, avoiding unstable hull topology.
2. Seed with world axes, every distinct selected-piece frame, PCA, and 96
   deterministic uniform SO(3) samples. PCA is only an initial candidate.
3. Refine the best 12 seeds, world axes, and up to 16 supplied piece frames using
   pattern search with 26 local rotation directions. Start at 15°, halve after
   an unsuccessful sweep, and stop below `1e-5` radians (about **0.000573°**).
   A 450-sweep cap per start bounds work. A regularized width product adds
   `1e-10` to normalized extents so planar/linear inputs have a useful objective.
4. Canonicalize equivalent signed/permuted bases to the right-handed frame
   closest to world XYZ. Retain world axes on equivalent volume solutions;
   subsequent previews retain a previous basis within a `1e-9` volume tie to
   avoid unnecessary flips. Local names L/W/H identify this canonical basis;
   they do not mean world-axis extents or sorted largest-to-smallest dimensions.
5. Refit each refined candidate against **every original selected vertex**.
   Choose it only if it improves on the world solution (volume tie tolerance
   `1e-10` of world volume). Thus hull tolerance cannot exclude a vertex from
   the final box, and the final volume never exceeds the world volume. A previous
   containing orientation may be retained if it beats the new search.

This is a **deterministic numerical approximation, not a proven global minimum**.
The angular stopping resolution is not a bound on global volume error. Caps,
local minima, ill conditioning, and hull tolerance can affect the candidate
found. If a start reaches the cap, its metadata records `converged: false`.
Reported dimensions are the actual full-geometry support widths, with only the
existing unit formatter's rounding. They have no visual padding. In particular,
the rendered 32-segment tube is polygonal: a 400 mm tube's optimal enclosing
square section is approximately `31.845911 × 31.845911 mm`, rather than the
continuous-cylinder diameter of 32 mm.

Accuracy evidence in `pvc-bounds.test.mjs`:

| Fixture | Reference / assertion |
| --- | --- |
| Aligned and arbitrarily rotated 400 mm tube | Analytic regular 32-gon result `400 × (32 cos(π/32))²`; volume within 0.02 mm³ |
| Rotated `400 × 120 × 32` cuboid, without supplied orientation | Volume within 0.02% of analytic 1,536,000 mm³; observed relative error `4.19e-12` on the verification run |
| World-aligned cuboid and cube | Exact world axes and dimensions retained; repeated results identical |
| Asymmetric elbow, mixed rotations, disconnected pieces, connected assembly | Every vertex contained and oriented volume ≤ world volume |
| Mixed rendered tube/elbow | Candidate beats an independent seeded scan of 1,024 uniform orientations |
| Random hull support directions | Widths match original vertices within `1e-9` normalized units |
| Coincident, linear, planar and nearly degenerate points | Finite orthonormal frames, containment, deterministic repeated results |

These fixtures support correctness and practical accuracy; they do not establish
a global approximation ratio for arbitrary selections.

## Integration and rendering

`sync()` observes selection, group replacement and world-matrix changes. It
immediately refits a containing world or previous-oriented preview. After 140 ms
without geometry changes, one module worker refines the oriented candidate.
New changes, empty selection, Off, and disposal cancel timers and terminate
obsolete workers. Revision checks reject stale results. Optimization runs off
the UI thread; camera movement never invalidates geometry bounds. First-time
mesh extraction and live support fits remain linear in selected vertex count;
very large selections can still cost time on the main thread. For reference,
the 70-piece tower fixture had 43,675 cached vertices and 545 hull vertices;
one local Node run took about 55 ms for initial collection and 352 ms for search.
Those timings are observations, not performance guarantees.

One reused `LineSegments` buffer draws 12 thin dashed edges, with no faces.
Depth writes/tests are disabled so coplanar meshes do not flicker. The independent
DOM layer contains exactly three upright 12px labels and three SVG leader lines;
it has `pointer-events: none`. Lines are outside piece/joint picking groups and
also have a no-op raycast. Label placement uses camera-dependent exterior-edge
scoring, 15-point edge-selection hysteresis, screen-space offsets, viewport
clamping, control avoidance, and joint collision minimization of three label
rectangles. End-on edges retain true dimensions and use leader lines. Invalid,
behind-camera and wholly offscreen projections are hidden. Projection is updated
after camera damping in the existing loop and skipped when camera/text/size are
unchanged. Projection never invokes the geometry optimizer.

The overlay has no model, history, persistence, or export dependency. JSON
contains only the existing model data; PDF builds its own scene from that data.
Page disposal releases buffers, material, labels, listener, timers and worker.
No new Three.js installation, CDN, package or build step is needed.

## Verification

From the repository root, with Node, Python, Playwright and Chrome available:

```powershell
node --test tests/pvc-bounds.test.mjs
python tests/pvc-browser-fixtures.py
node tests/pvc-bounds.browser.cjs
node tests/pvc-coordinated-resize.browser.cjs
node tests/pvc-placement.browser.cjs
```

`PVC_BROWSER` can specify a different Chromium binary; `NODE_PATH` can point to
an existing Playwright installation. The browser scripts start their own local
HTTP server. No runtime dependency installation is needed by the application.

The new browser suite runs real Chrome/WebGL: it first opens the production
page for keyboard/accessibility/empty-selection checks, then a disposable copy
instrumented with read-only observations. Geometry fixtures enter through Load
JSON. Selection, marquee, assembly selection, translation and ring dragging,
numeric/discrete transforms, single/group length previews, undo/redo, units,
copy/paste, deletion, New, template loading, JSON and PDF downloads use existing
controls and actual pointer/keyboard input. The containment observer independently
traverses the current rendered meshes, rather than trusting the bounds cache.
Camera checks use native orbit/pan/wheel input and presets. Layout checks assert
three non-colliding, non-clipped, 12px labels with canvas hit-through, including
600px and 320px page widths and end-on orthographic views. Screenshots and real
downloads are saved under ignored `tmp/pvc-bounds/` for visual inspection.

Remaining scope: automated checks exercise Chromium with software WebGL, not
every browser/GPU or assistive technology. A screen reader's spoken delivery is
not manually audited. Large-selection timing and global-optimality guarantees
are not established by these tests.
