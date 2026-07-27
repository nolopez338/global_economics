# Repository Structure

This inventory describes the tracked files in the current checkout. Paths are
repository-relative. Where the repository does not establish a lifecycle,
publication target, or build contract, that status is recorded as
**unconfirmed** rather than inferred from a directory name.

## 1. Repository Overview

This repository collects statistics and global-economics teaching resources in
four principal forms:

1. static, browser-delivered Grade 10 and Grade 11 study hubs;
2. teacher schedule pages, schedule data, and browser-based authoring tools;
3. independent academic-year LaTeX collections for activities, assessments,
   solutions, catch-up work, and olympiad material; and
4. standalone dashboards, manual quiz experiments, and small data utilities.

The web areas use HTML, CSS, and unbundled JavaScript. They have no application
framework, package manifest, backend, or repository-level build step. Some
features use browser globals and remotely hosted libraries. The print areas use
LaTeX with year-local preambles, TikZ/PGFPlots resources, images, and CSV data.
One Node.js script validates a dashboard dataset, and one Python/pandas command
normalizes externally supplied assessment workbooks.

The main functional boundaries are:

| Area | Kind | Purpose |
| --- | --- | --- |
| `index.html`, `grade10/`, `grade11/` | Static website | Student navigation, term summaries, practice, formulas, and interactive topic pages. |
| `assets/` | Shared web assets and browser authoring | Site CSS/JavaScript, reference templates, and a configurable assessment runtime. |
| `teacher/` | Static teacher website, data, and utilities | Weekly/class schedules, calendar views, schedule authoring prototype, and result processing. |
| `book2025-2026/`, `book2026-2027/` | LaTeX authoring sources | Year-specific printable teaching and enrichment material. |
| `other/` | Standalone and experimental projects | Cambridge heatmap, manual quiz comparisons, and an independent Grade 9 page. |

No repository evidence connects the LaTeX sources to automatic generation of
the HTML study pages.

## 2. Top-Level Structure

The following selective tree includes every meaningful top-level path and
expands the areas needed for navigation. Repetitive curriculum documents are
grouped rather than listed individually.

```text
.
├── .gitignore                         # Ignored LaTeX PDFs and compiler auxiliaries
├── README.md                          # General navigation and workflow notes
├── REPOSITORY_STRUCTURE.md            # This verified structural inventory
├── index.html                         # Root student navigation page
├── assets/
│   ├── css/                           # Shared site, schedule, graph, and topic styles
│   ├── js/                            # Collapsible UI and MathJax/SVG graph helpers
│   ├── html/                          # Unlinked reference/template HTML pages
│   └── interactive/
│       ├── index.html                 # Assessment-settings authoring page
│       ├── shared/interactive.css
│       ├── template/                  # Assessment runtime, settings, and question data
│       └── tools/                     # Image-question and spreadsheet import tools
├── grade10/
│   ├── index.html                     # Grade 10 hub
│   └── src/
│       ├── G10_T1.html … G10_T3.html  # Term hubs
│       └── pages/                     # Topic, practice, formula, and explorer pages
├── grade11/
│   ├── index.html                     # Grade 11 hub
│   └── src/
│       ├── G11_T1.html … G11_T3.html  # Term hubs
│       └── pages/                     # Topic, practice, formula, and distribution pages
├── teacher/
│   ├── README.md                      # Schedule contracts and known baseline gaps
│   ├── schedule.html                  # Main weekly schedule
│   ├── schedule-teacher.html          # Teacher-mode weekly schedule
│   ├── authoring/schedule.csv         # Claimed source; current generator contract is incomplete
│   ├── assets/
│   │   ├── css/principal-schedule.css
│   │   ├── html/general_calendar.html # Standalone year-calendar view
│   │   └── js/                        # Schedule globals, renderers, controllers, and theme
│   ├── pages/
│   │   ├── class.html                 # Shared class-page implementation
│   │   ├── class_schedules/           # Thin wrappers for 10A–10E and 11A–11E
│   │   ├── full_schedule.html          # Combined dated schedule
│   │   ├── schedule_prototype_generated.html
│   │   ├── magis.html                 # Standalone supplementary page
│   │   └── sum_symbol.html             # Lesson linked from both grade hubs
│   └── tools/
│       ├── schedule_authoring_tool.html # Browser CSV validator/generator prototype
│       └── 2026-02-19-results/         # Python normalizer, README, and ten input workbooks
├── book2025-2026/
│   ├── README.md
│   ├── clean-latex.bat
│   ├── grade9/                         # One Term 3 source
│   ├── grade10/{term_2,term_3}/        # Activities, evidence, catch-ups, extras, and CSVs
│   ├── grade11/{term_2,term_3}/        # Same broad organization; Term 3 also has exams
│   ├── olympiad/                       # One grades 8–9 source
│   └── preamble/                       # Shared year-local preambles, templates, graphs, images
├── book2026-2027/
│   ├── README.md
│   ├── clean-latex.bat
│   ├── grade9/                         # One Term 3 source
│   ├── grade10/{term_1,term_3}/        # Term 1 contains many G10_T2-labelled files
│   ├── grade11/{term_2,term_3}/
│   ├── olympiad/                       # Enrichment, Cambridge, diploma, and workbook material
│   └── preamble/                       # Separate year-local TeX resources and images
└── other/
    ├── README.md
    ├── cambridge/                      # Grade 3 heatmap dashboard, data, and Node validator
    ├── Test Basic/                     # Three manual browser quiz experiments
    ├── Test Codex/                     # Two manual browser quiz experiments
    └── src/pages/                      # Standalone Grade 9 correlation page
```

The checkout contains no tracked top-level `tools/` directory, CI definition,
deployment manifest, dependency lockfile, container definition, or test-runner
configuration.

## 3. Main Entry Points

### Browser and authoring entry points

All browser pages can be served as static files. Pages that call `fetch()` need
an HTTP origin rather than a reliable `file:` workflow.

| Path | Verified role | Requirements and incoming navigation |
| --- | --- | --- |
| `index.html` | Root student navigation. | Links to both grade hubs and `teacher/schedule.html`; loads `assets/css/base.css`, `components.css`, and `theme.css`. |
| `grade10/index.html` | Grade 10 hub. | Links to `src/G10_T1.html`, `G10_T2.html`, and `G10_T3.html`; linked from the root page. |
| `grade11/index.html` | Grade 11 hub. | Links to `src/G11_T1.html`, `G11_T2.html`, and `G11_T3.html`; linked from the root page. |
| `teacher/schedule.html` | Main weekly teacher schedule/navigation shell. | Loads the weekly-table renderer before its inline invocation, then `principal-schedule.js` and `theme-toggle.js`; linked from `index.html`. |
| `teacher/schedule-teacher.html` | Teacher-mode variant of the weekly shell. | Uses the same renderer/controller sequence; it is linked from schedule UI code rather than the root landing page. |
| `teacher/pages/full_schedule.html` | Combined dated schedule view. | Requires, in deferred order, class globals/controller, `schedule-data.js`, renderers, and theme logic. |
| `teacher/pages/class.html` | Shared implementation for one class schedule. | The wrappers in `teacher/pages/class_schedules/` redirect or configure this page; it consumes the same deferred globals and renderers as the full view. |
| `teacher/assets/html/general_calendar.html` | Standalone year-calendar view. | Loads `year-calendar-data.js` before inline rendering and also loads the theme toggle. |
| `assets/interactive/index.html` | Interactive-assessment settings editor and launcher. | Browser-only; loads existing settings and downloads a replacement `settings.js`. |
| `assets/interactive/template/template.html` | Configurable assessment runtime. | Loads jsPDF from a CDN, then settings and question-data globals before `template.js`. |
| `assets/interactive/tools/image-questions.html` | Image-question data authoring/import. | Browser-only; downloads `image-questions-settings.js`. |
| `assets/interactive/tools/multiple_choice_questions.html` | Multiple-choice spreadsheet importer. | Browser-only; SheetJS is loaded remotely; downloads `multiple-choice-database.js`. |
| `other/cambridge/grade3_heatmap_dashboard.html` | Standalone Cambridge Grade 3 heatmap. | Loads its colocated data script before dashboard logic. Publication status is unconfirmed. |
| `other/Test Basic/*.html`, `other/Test Codex/*.html` | Manual quiz experiments. | Standalone browser pages; no automated runner references them. |
| `other/src/pages/g9-t3-correlation-coefficient.html` | Standalone Grade 9 statistics page. | Not linked from the root/grade hubs; publication status is unconfirmed. |

`assets/html/Gn_Tm.html`, `assets/html/template_practice.html`, and
`assets/html/decision_tree.html` are reference or standalone HTML sources with
no verified root navigation. Their external consumers and publication status
are unconfirmed.

### Command-line and document entry points

| Path or family | Role | Verified requirement |
| --- | --- | --- |
| `other/cambridge/validate_grade3_heatmap_data.js` | Validates the Cambridge data schema, aggregates, and required dashboard safeguards. | Node.js; run from the repository root or `other/cambridge/` as documented below. |
| `teacher/tools/2026-02-19-results/results.py` | Normalizes four-row student records from adjacent Excel exports. | Python 3, pandas, a compatible Excel reader, and optional `tabulate`. |
| `book2025-2026/**/*.tex`, `book2026-2027/**/*.tex` | Printable activities, exams, solutions, summaries, and enrichment documents. | Many files contain `\documentclass` and are plausible principal documents; others are inputs/templates. A canonical engine, complete entry-point list, and supported invocation directory are unconfirmed. |
| `book*/preamble/main.tex` | Small year-local sample/principal document importing `preamble`. | LaTeX environment with the packages used by the same-year preamble; no supported command is declared. |
| `book*/clean-latex.bat` | Recursive Windows cleanup of common TeX auxiliaries. | Windows `cmd.exe`; it pauses after deleting files. |

## 4. Shared Assets and Dependencies

### Shared website resources

- `assets/css/base.css`, `components.css`, and `theme.css` form the common
  visual base for the root, grade hubs, term pages, and many practice pages.
- `assets/css/schedule.css` is shared by teacher schedule, full-schedule, and
  class pages. `teacher/assets/css/principal-schedule.css` augments the two
  weekly shells.
- `assets/css/decision-tree.css`, `graphs.css`,
  `components_extra_resources.css`, and `youtube-links.css` are loaded only by
  pages that need those components.
- `assets/js/collapsible.js` adds collapsible-section behavior. Many longer
  term/practice pages load it after their markup.
- `assets/js/math-render.js` configures MathJax and exposes graph helpers through
  `window.MathRender`; pages that call those helpers must load it before use.
- The assessment runtime has its own CSS boundary at
  `assets/interactive/shared/interactive.css` and
  `assets/interactive/template/src/template.css`.

### Browser globals and load order

The repository uses classic scripts rather than modules:

- `assets/interactive/template/src/settings.js` defines
  `window.InteractiveTemplateSettings`;
  `databases/multiple-choice-database.js` and
  `image-questions-settings.js` define their corresponding question globals.
  `template.js` reads all three, so `template.html` loads them first.
- `teacher/assets/js/class-data.js` defines `window.CLASS_STUDENT_LISTS` and
  `window.CLASS_NOTES`. `schedule-data.js` defines `window.SCHEDULE_DATA`.
  Class and full-schedule controllers read these names; script order is part of
  the runtime contract.
- `teacher/assets/js/render-weekly-schedule-table.js` exports
  `window.renderWeeklyScheduleTable`, which the two weekly shells invoke before
  `principal-schedule.js` enhances the resulting page.
- `teacher/assets/js/year-calendar-data.js` is a separate calendar dataset used
  by `teacher/assets/html/general_calendar.html`.

### Remote dependencies and offline behavior

Individual pages load MathJax, D3, jsPDF, QRCode.js, or SheetJS from public
CDNs. There is no vendored fallback or centralized dependency manifest.
Consequently, formulas, graphs, PDF/QR generation, or spreadsheet import can be
incomplete offline unless the browser already has the resource cached.
Curriculum pages also link to external video, design, and document services;
availability and access permissions are outside this repository.

### LaTeX resources

Each academic-year tree deliberately contains its own `preamble/` directory:
`preamble.tex`, `preamble_exams.tex`, exam/solution templates, reusable graph
definitions, logos, and other images. Representative documents use relative
`\input` and `\includegraphics` paths into the same year. The duplicated trees
must therefore be treated as separate dependency sets; no cross-year import or
shared package workspace is declared.

## 5. Grade 10 and Grade 11 Web Areas

Both grades follow the convention `gradeNN/index.html` →
`gradeNN/src/GNN_T1.html` through `GNN_T3.html` → topic pages in
`gradeNN/src/pages/`. Practice filenames usually encode grade, term, learning
evidence/lesson, and criterion identifiers (for example,
`g10-t2-le2-c6-practice.html`). This convention is common but not universal:
generic names such as `formulas.html`, `main_examples.html`, and
`practice_activity3_1.html` also exist.

### Grade 10

- `grade10/index.html` is the navigational hub for all three term pages.
- `G10_T2.html` connects economics/statistics material to practice pages,
  formula and expected-value resources, a payoff builder, and
  `teacher/pages/sum_symbol.html?origin=grade10`.
- `G10_T3.html` links discrete/continuous probability explorers and the Term 3
  practice series.
- Grade-specific content remains under `grade10/src/pages/`, while layout,
  collapsible behavior, MathJax setup, and graph styles are drawn from
  `assets/`.

### Grade 11

- `grade11/index.html` is the navigational hub for all three term pages.
- Its topic collection includes distributions, normal-distribution material,
  formulas, Term 2 practice, and Term 3 practice.
- `G11_T2.html` also links to `teacher/pages/sum_symbol.html?origin=grade11`.
- Like Grade 10, grade-local pages use shared root assets through relative
  paths; there is no copied grade-local asset bundle.

The web term organization does not mirror the academic-year LaTeX term trees
exactly, and no generator connects the two. The root page links the public
weekly teacher schedule, but grade pages do not directly consume schedule data.

## 6. Teacher Area

### Pages and schedule consumers

- `teacher/schedule.html` and `schedule-teacher.html` render the same weekly
  timetable structure in public and teacher modes. `principal-schedule.js`
  detects the pathname to select the mode and fetches class wrapper pages when
  building its UI.
- `teacher/pages/full_schedule.html` combines schedule entries across classes.
- `teacher/pages/class_schedules/10A.html` through `10E.html` and `11A.html`
  through `11E.html` are thin class-specific entry points that route into the
  shared `teacher/pages/class.html` implementation.
- `teacher/pages/schedule_prototype_generated.html` reads the retained
  `window.SCHEDULE_DATA` artifact, but is not linked from main navigation. Its
  support and publication status are unconfirmed.
- `teacher/assets/html/general_calendar.html` is an independent calendar
  consumer of `year-calendar-data.js`.
- `teacher/pages/magis.html` and `sum_symbol.html` are supplementary pages;
  `sum_symbol.html` has verified incoming links from both grade term hubs.

### Authoring inputs and generated artifacts

`teacher/authoring/schedule.csv` is labelled as the source by the headers of
both `teacher/assets/js/schedule-data.js` and `schedule-data-base.js`. Those two
JavaScript files declare generated schedule data and should not be manually
edited. However, the current source-to-artifact contract is not reproducible:

- `schedule.csv` contains 115 data records with nine display-oriented columns;
- `schedule-data.js` contains 383 records and additional `Term` and
  `Material teacher` fields;
- `schedule_authoring_tool.html` expects normalized columns such as
  `class_id`, `date`, and `slot`, not the current CSV header;
- the tool fetches `teacher/authoring/slots.csv`, which is absent; and
- `schedule-data-base.js` has a different, undated record shape and has no
  tracked HTML consumer.

Accordingly, `schedule.csv` is a **claimed canonical authoring source**, not a
verified lossless source for the retained runtime data. The exact canonical
dataset, slot definitions, adapter contract, and role of
`schedule-data-base.js` remain unconfirmed. The browser tool can validate
loaded CSV and download flat, normalized, and adapter JavaScript, but its
default workflow must not be treated as verified equivalence with the current
runtime artifact.

### Results processing and data caution

`teacher/tools/2026-02-19-results/` contains `results.py`, usage instructions,
and dated `.xls` inputs for classes 10A–10E and 11A–11E. The script detects
student and C1–C10 columns, collapses four-row records, normalizes yes/no values,
and can print or export cleaned tables. These workbooks appear externally
supplied and may contain student-level information. Their provenance,
retention period, and authorization are not documented; this map intentionally
does not reproduce their contents. Run the tool only in an authorized local
environment and avoid shared logs or derived commits.

## 7. Academic-Year LaTeX Books

The year directories are source collections, not declared packages or
automated builds. Many documents are self-contained via `\documentclass`;
others import a same-year preamble/template. PDFs are generated outputs, while
the `.tex`, `.csv`, image, and spreadsheet files are authoring inputs.

### `book2025-2026/`

- **Grades and terms:** Grade 9 has one `G9_T3` source. Grade 10 has `term_2`
  and `term_3`; Grade 11 has `term_2` and `term_3`.
- **Organization:** term directories use numbered groups for
  `1-practice_activities`, `2-learning_evidences`, `3-catch_ups`, and, where
  present, `4-extra_material`. Grade 11 Term 3 additionally has `3-exams`.
- **Data:** Term 3 learning-evidence areas contain CSV datasets used as activity
  data or companion inputs. Provenance is not stated.
- **Shared resources:** `preamble/` contains the year-local standard and exam
  preambles, templates, three graph-definition inputs, a logo, and principal
  navigation images.
- **Olympiad:** `olympiad/2026-03_grades_8-9.tex` is the sole olympiad source.
- **Status:** active/archive lifecycle is unconfirmed; the directory name alone
  does not establish it.

### `book2026-2027/`

- **Grades and terms:** Grade 9 again has one `G9_T3` source. Grade 10 has
  `term_1` and `term_3`; Grade 11 has `term_2` and `term_3`.
- **Organization:** the same numbered activity/evidence/catch-up/extra pattern
  is used, with Grade 11 Term 3 also containing `3-exams`.
- **Data:** Grade 10 and Grade 11 Term 3 include CSV datasets. Several
  Grade-10-prefixed datasets also reside in the Grade 11 tree; whether this is
  intentional reuse or a naming anomaly is unconfirmed.
- **Shared resources:** this year's `preamble/` is separate and includes the
  common graph/template set plus Cambridge, Icontec, IHS, and Urraca images.
- **Olympiad and related material:** `olympiad/` contains a grades 8–9 source,
  standalone probability/statistics/pedagogy sources, four diploma documents,
  and `Cambridge/` Paper 1/Paper 2 question/solution documents with an `.xlsx`
  workbook.
- **Naming anomaly:** many `G10_T2_*` sources are located below
  `grade10/term_1/`; repository evidence does not say whether the path or label
  is erroneous. Copy-named, `proyect`, `soution`, and `suplementary` filenames
  also remain as-is.
- **Status:** lifecycle is unconfirmed; a newer year name is not proof that the
  tree is the active or published collection.

There is substantial byte-identical and near-identical content across the two
years, consistent with copy-forward authoring. No policy specifies which copy
is canonical, whether corrections should be backported, or whether one tree is
archived. The exact TeX distribution, engine, invocation directory, shell
escape requirements, and complete set of compilable roots are unconfirmed.

## 8. Other Projects and Experiments

`other/` is explicitly separate from root student navigation, and its README
marks publication status as unconfirmed.

- `other/cambridge/` contains a standalone Cambridge Grade 3 heatmap. The HTML
  loads `grade3_heatmap_dashboard_data.js` before
  `grade3_heatmap_dashboard.js`, with sibling CSS. The validator executes the
  data in a Node VM, checks row/value/aggregate invariants, and verifies that
  dashboard safeguards remain present.
- `other/Test Basic/` holds biology, history, and template quiz examples.
  `other/Test Codex/` holds biology and history variants. These are manual
  browser experiments: no test framework, runner, or CI configuration consumes
  them.
- `other/src/pages/g9-t3-correlation-coefficient.html` is a standalone Grade 9
  lesson using CDN resources. It has no verified incoming link from the root or
  grade hubs.

No additional current subproject exists below `other/` in this checkout.

## 9. Validation and Maintenance Workflows

Only commands supported by files in the current checkout are listed. Unless a
row says otherwise, commands are run from the repository root.

| Command | Working directory | Dependencies and verified scope |
| --- | --- | --- |
| `python3 -m http.server 8000` | Repository root | Python 3 standard library. Serves relative web paths and gives `fetch()` an HTTP origin; this is a local preview, not evidence of production deployment. |
| `node other/cambridge/validate_grade3_heatmap_data.js` | Repository root | Node.js. Validates the Cambridge dataset/aggregate/dashboard contract. |
| `node validate_grade3_heatmap_data.js` | `other/cambridge/` | Equivalent validator invocation from its own directory. |
| `python teacher/tools/2026-02-19-results/results.py --help` | Repository root | Python 3 and pandas (imported before CLI parsing). Displays the current CLI. |
| `python teacher/tools/2026-02-19-results/results.py --file 10A.xls` | Repository root | pandas plus an `.xls` reader such as compatible `xlrd`; may expose sensitive data. The script resolves the named file beside itself. |
| `python teacher/tools/2026-02-19-results/results.py --all` | Repository root | Same dependencies/caution; processes every adjacent `.xls`/`.xlsx` input. |
| `clean-latex.bat` | Either academic-year directory, in Windows `cmd.exe` | Recursively deletes `*.aux`, `*.synctex.gz`, `*.log`, `*.out`, and `*.toc`, then pauses. |

The current checkout has **no** `tools/validate_local_references.py`, despite a
reference to that path in `README.md`; therefore no local-reference validation
command is documented as runnable. Schedule source/artifact drift or
equivalence likewise has no committed passing command. The schedule authoring
page provides interactive validation only, and its missing `slots.csv` and CSV
schema mismatch are baseline limitations.

No canonical LaTeX compilation command is declared. Running an assumed
`pdflatex`, `xelatex`, `latexmk`, or other command is therefore not presented as
a verified workflow.

## 10. Generated, Ignored, and External Content

### Generated or download-produced artifacts

- `teacher/assets/js/schedule-data.js` and `schedule-data-base.js` carry
  generated/source headers. Do not edit them manually; the exact reproducible
  generator for their current contents is unresolved.
- `teacher/tools/schedule_authoring_tool.html` downloads
  `schedule-flat.generated.js`, `schedule-norm.generated.js`, and
  `schedule-adapter.generated.js`. No automated installation step maps those
  downloads into the runtime tree.
- The interactive assessment authoring pages download `settings.js`,
  `image-questions-settings.js`, and `multiple-choice-database.js` for manual
  placement in `assets/interactive/template/`.
- Compiled PDFs and LaTeX auxiliaries are outputs, not source. The root
  `.gitignore` excludes `*.pdf`, `*.aux`, `*.log`, `*.synctex.gz`, `*.toc`,
  `*.out`, `*.lof`, and `*.lot`.

### External or potentially sensitive inputs

- `teacher/tools/2026-02-19-results/*.xls` are dated external assessment
  exports and may contain student-level information. Provenance, authorization,
  retention, and deletion policy are unconfirmed.
- `book2026-2027/olympiad/Cambridge/2026-cambridge-stage4.xlsx` is a tracked
  workbook colocated with Cambridge question/solution sources. Its provenance
  and whether it is an input to those documents are unconfirmed.
- Curriculum CSV datasets are tracked authoring inputs. Some LaTeX files refer
  to same-area datasets, but repository-wide provenance and retention rules are
  not documented.
- External web links and CDN libraries are dependencies, not vendored content.
  This document omits private-looking query strings and does not assert that
  linked resources are publicly accessible.

Transient dependencies, editor metadata, Git internals, and ignored compiler
outputs are intentionally absent from the tree above.

## 11. Known Structural Limitations and Unconfirmed Areas

1. **Broken documentation references:** `README.md` names the absent
   `tools/validate_local_references.py` and absent
   `REPOSITORY_RESTRUCTURING_PROPOSAL.md`. Their intended retention or removal
   is unconfirmed.
2. **Schedule generation contract:** the claimed CSV source, retained runtime
   datasets, and browser generator differ in record count and schema; required
   `teacher/authoring/slots.csv` is missing. Canonical data and artifact mapping
   are unconfirmed.
3. **Unused schedule data:** `teacher/assets/js/schedule-data-base.js` declares
   the same global as the primary data file but has no tracked HTML consumer.
   Its lifecycle and ownership are unconfirmed.
4. **Publication and deployment:** no hosting/deployment configuration defines
   public URLs or identifies which standalone, teacher, experimental, or
   academic-year paths are published.
5. **LaTeX build contract:** supported engine, distribution, working directory,
   entry-point inventory, and build flags are not documented. Relative imports
   demonstrate same-year dependencies but do not establish a universal command.
6. **Academic-year lifecycle:** neither year README identifies its tree as
   active or archived, and no copy-forward/backport policy exists.
7. **Naming and placement ambiguities:** `book2026-2027/grade10/term_1/`
   contains many Term 2 labels; Grade 10 datasets occur under the Grade 11 Term
   3 evidence directory; and spelling/copy suffix anomalies occur throughout.
   Intent is unconfirmed.
8. **External dependencies:** CDN-dependent browser features and externally
   hosted teaching links may be unavailable offline or access-controlled.
9. **External data governance:** provenance and retention rules for the dated
   results workbooks, Cambridge workbook, and curriculum datasets are not
   recorded.
10. **Reference/experiment consumers:** incoming external links, publication
    status, and ownership for `assets/html/`, the schedule prototype, and most
    of `other/` are unconfirmed.
