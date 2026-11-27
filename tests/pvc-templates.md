# PVC Studio standard-component templates

The dropdown contains **Empty** and **Ground footprint study**. The former nine
elevated furniture templates were removed because their junction layouts and
brace reaches require components outside the seven-part catalog. Their IDs
now fail explicitly; they are never silently mapped to another template.

The floor-level example uses four 90° elbows, two 550 mm tubes and two 350 mm
tubes, with all eight tube/socket joints aligned and recorded. Centerline
spans are 600 × 400 mm; the footprint is approximately 64 × 44 cm. The rails
span between four floor-contact elbows on a level supporting surface. There are no legs, unsupported
branches, elevated surfaces, crossing tubes, or overlapping fittings.

This is a footprint study, not a furniture support. It is unbraced and can rack;
unglued sockets are not assumed rigid. It supplies no lateral restraint for an
elevated structure in either horizontal direction. Performance depends on PVC
dimensions and properties, connection methods, assembly quality and use
conditions. No load rating, certified analysis or guaranteed stability is given.

Template selection previews only. Load validates before changing current state,
asks before replacing unexported work, and creates one undoable, autosaved edit.
Tests check the exact allowlist, fixed and immutable socket geometry, rejected
component types and overrides, atomic imports and paste, constructor/history
validation, real JSON/PDF exports, physical connection alignment, connected
components and unintended intersections.

Run from the repository root:

```powershell
node --test --test-isolation=none tests/pvc-model.test.mjs tests/pvc-placement.test.mjs tests/pvc-templates.test.mjs tests/pvc-standard.test.mjs
python tests/pvc-browser-fixtures.py
node tests/pvc-templates.browser.cjs
node tests/pvc-standard.browser.cjs
node tests/pvc-placement.browser.cjs
node tests/pvc-pdf.browser.cjs
```

Browser checks require Playwright and Chrome; set NODE_PATH to the local bundled
dependencies if necessary. Generated fixtures use isolated storage keys. Results
and screenshots are written under tmp/.
