# Survey dashboard

Open `teacher/pages/survey_visualization.html` using the repository's normal static hosting. There is no backend, installation, or build step. For a local preview, run this from the repository root:

```powershell
python -m http.server 8765 --bind 127.0.0.1
```

Then visit `http://127.0.0.1:8765/teacher/pages/survey_visualization.html`.

The page automatically fetches `../../assets/data/survey_data_extended.xlsx`. The file picker is always available and processes XLSX files locally. On `file://`, the page explicitly skips automatic fetch and asks for a local file. All runtime scripts, including SheetJS CE 0.20.3, are bundled locally. Nothing is sent to an external service.

## Implementation

- `teacher/assets/js/survey-core.js`: header-based parsing, sheet/key validation, explicit measurement classification, metadata dependencies, filtering, statistics, binning, and ranking logic. Exposes the same API to the browser and Node tests.
- `teacher/assets/js/survey-dashboard.js`: local loading, controls, inline SVG charts, linked details, quality/audit evidence, and CSV/SVG downloads.
- `teacher/assets/css/survey-visualization.css`: responsive styles layered over the teacher pages' shared `assets/css/schedule.css`.
- `teacher/assets/vendor/sheetjs/`: pinned SheetJS browser distribution and Apache 2.0 license. Source: https://cdn.sheetjs.com/xlsx-0.20.3/package/dist/xlsx.full.min.js; documentation: https://docs.sheetjs.com/docs/api/parse-options/.

Derived values are the workbook's stored snapshots. Reference date and assumptions come from Derivation config. Shares stored as fractions are displayed as percentages in charts. Additional numeric range filters explicitly use stored units. Original statuses and source dependencies govern quality selection; derived fields are not assigned invented statuses. Supplemental rows are indexed by questionnaire ID and field and never expand the respondent table.

Default analysis CSVs exclude questionnaire IDs, student IDs, and names. Enabling the teacher identity control explicitly includes them. CSVs export all globally filtered respondents using the displayed analysis fields, independently of chart selections and table searches. Charts export as vector SVG images, including their titles, units, filters, denominators, and reference date; no raster-image library is required.

## Verification

Run the focused tests from the repository root:

```powershell
node --test teacher/tools/survey-core.test.cjs
```

In environments that prohibit spawning a test-runner child process, Node 22+ supports:

```powershell
node --test --test-isolation=none teacher/tools/survey-core.test.cjs
```

Tests read the actual workbook without modifying it. They cover all numeric-variable count/percentage reconciliation, shared class edges, questionnaire and class benchmarks, sleep/height/math counts, nulls/zeros/fractional negatives, empty and one-record filters, ranking completeness and denominators, zero-denominator ratios, source quality dependencies, missing worksheet dimensions, reordered columns, and validation errors.

Browser checks performed with static HTTP hosting: automatic load, local-file chooser, desktop and 390-pixel layouts, no page-wide horizontal overflow at the narrow width, sleep/height/math benchmarks, empty class selection, a one-person histogram selection, ranking selections, partial rankings, class percentage comparisons, box plots, scatterplot paired n, default CSV privacy, and console errors. The phone-hours vs sleep-hours preset has paired n=197 in this source. Q16 has 167 complete, 18 partial, and 21 unavailable rankings; Q17 has 172/17/17; Q18 has 172/15/19.

The browser automation environment blocks the `file://` protocol, so direct file opening could not be visually tested. The HTTP file-picker flow was tested successfully. Large files are parsed synchronously in the browser; this dashboard is designed for classroom-scale workbooks. Histogram settings are capped at 2,000 bins, and manually requested bin counts at 200. An explicit origin can add leading bins to retain every value. Overlaid class bars may obscure one another; small multiples and the frequency table provide alternatives.
