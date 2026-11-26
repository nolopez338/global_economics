# PVC PDF export checks

From the repository root:

1. `python tests/pvc-browser-fixtures.py`
2. `node tests/pvc-model.test.mjs`
3. `node tests/pvc-pdf.browser.cjs` (requires Playwright and installed Chrome)
4. `python tests/pvc-pdf-check.py` (requires pypdf)
5. Render the PDFs in `tmp/pdfs/pvc-export/` with `pdftoppm -png`, then inspect all pages.

The browser runner serves only local files, runs the existing interaction suite,
and downloads the real sample, mixed disconnected, compact and pending-edit
exports. It checks state preservation, orientations, camera bounds, projection
types, empty/busy controls, capture and overflow errors, and narrow headers.
The PDF checker verifies A4 page sizes, page/view counts, image resolution,
material quantities, exact cuts, selected units, totals and compact-list completeness.

`PVC_BROWSER` can select another Chromium binary. `PVC_SKIP_INTERACTIONS=1`
reruns only export checks; `PVC_ONLY_INTERACTIONS=1` reruns only interactions.
Playwright may be provided through `NODE_PATH` instead of a local installation.
Generated fixtures use separate browser storage and must not be deployed.
