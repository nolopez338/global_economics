# Global Economics Study Resources

This repository contains a static browser-based study hub, teacher schedule
pages and authoring utilities, and year-specific LaTeX teaching materials.
There is no repository-wide build step.

## Entry points

- `index.html` is the student-facing navigation root. Grade hubs are
  `grade10/index.html` and `grade11/index.html`.
- `teacher/schedule.html` is the main teacher schedule page. See
  [`teacher/README.md`](teacher/README.md) before editing schedule data.
- `assets/interactive/index.html` opens the browser-only interactive assessment
  authoring tools.
- `book2025-2026/` and `book2026-2027/` contain independent LaTeX source
  collections. Their status and known contents are documented in their local
  README files.
- [`other/README.md`](other/README.md) identifies standalone and experimental
  pages that are not linked from the student hub.

Serve the checkout from its root when using tools that call `fetch()`:

```bash
python3 -m http.server 8000
```

Then open `http://localhost:8000/`. The production host and deployment process
are not documented in this repository.

## Deterministic validation

```bash
python3 tools/validate_local_references.py --self-test
node other/cambridge/validate_grade3_heatmap_data.js
```

The first command validates static local `href`, `src`, CSS `url()`, and CSS
`@import` targets without accessing the network. The second validates the
colocated Cambridge heatmap data and dashboard safeguards. Schedule source/data
equivalence does not yet have a passing automated check; see the blocked
workflow described in `teacher/README.md`.

## Content and dependency boundaries

- `assets/`, `grade10/`, `grade11/`, and the HTML below `teacher/` are published
  or publishable static files. No bundler is required.
- `teacher/authoring/` and the LaTeX year trees are source areas. Files under
  `teacher/assets/js/` that carry an `AUTO-GENERATED FILE` header are generated
  runtime inputs and should not be edited manually.
- PDFs and LaTeX auxiliary output are generated and ignored by `.gitignore`.
- The academic-year trees keep their preambles, images, and activity datasets
  year-local. Do not introduce cross-year imports.
- Workbooks under `teacher/tools/2026-02-19-results/` are externally supplied
  inputs. Their retention and privacy status is not documented; do not move,
  delete, or expose their contents without authorization.
- `other/Test Basic/` and `other/Test Codex/` are manual browser experiments,
  not automated tests. Their publication status is unconfirmed.

Browser pages load selected third-party libraries from CDNs, including MathJax,
D3, jsPDF, QRCode.js, and SheetJS. Those features require network access unless
the browser has cached the dependency. Teaching-resource links may also point
to access-controlled external services; deterministic validation intentionally
does not request them.

For the verified architectural inventory, see
[`REPOSITORY_STRUCTURE.md`](REPOSITORY_STRUCTURE.md). For the evidence and
phased rationale behind these maintenance changes, see
[`REPOSITORY_RESTRUCTURING_PROPOSAL.md`](REPOSITORY_RESTRUCTURING_PROPOSAL.md).
