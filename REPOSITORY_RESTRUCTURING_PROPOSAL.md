# Repository Restructuring Proposal

## 1. Executive Assessment

**Assessment: limited, incremental restructuring is warranted; a repository-wide redesign is not.** The existing top-level separation between the student site, shared web assets, teacher material, year-specific LaTeX collections, and miscellaneous work is understandable and appropriate for a 485-file, build-free repository. The root `index.html` is a clear published entry point, and the grade hubs, teacher schedule, and LaTeX year boundaries already express real delivery and maintenance boundaries.

The most important improvements are narrower:

1. **High — restore and continuously check local references.** A verified local-reference scan found five missing browser resources. Four student pages request the nonexistent `assets/css/decision-tree.css`, and `teacher/pages/schedule_prototype_generated.html` requests a nonexistent generated artifact. These are current defects, not stylistic concerns.
2. **High — make schedule generation reproducible.** `teacher/tools/schedule_authoring_tool.html` requires a missing `teacher/authoring/slots.csv`; its download names do not directly match the runtime files, while two runtime files say they are generated from the canonical CSV. The source/generated boundary therefore exists but cannot be reliably followed from a clean checkout.
3. **Medium — document contributor entry points and dependencies.** The only Markdown guide is the architectural inventory `REPOSITORY_STRUCTURE.md`. There is no concise root contributor README, LaTeX compile contract, Python environment description, or published-versus-experimental content index.
4. **Medium — define an academic-year lifecycle without deduplicating active books.** All 159 exact duplicate groups span the two book years (159 duplicated files, approximately 2.59 MB of duplicate copies), but the duplicated, self-contained year trees also protect old documents from later preamble changes. The right response is an explicit copy-forward/archive policy and a manifest, not a shared cross-year preamble.
5. **Medium — separate named experiments and dated external inputs from ambiguous containers.** `other/Test Basic/` and `other/Test Codex/` are browser experiments, not automated tests. The dated `.xls` inputs are stored beside reusable Python code under `teacher/tools/`. Selective relocations would clarify intent, but only after confirming published URLs and data-retention requirements.

All claims above are **verified** from the checkout unless explicitly described as inferred. This proposal used `REPOSITORY_STRUCTURE.md` as an initial map, then checked the actual tree, source references, file hashes, configuration, and executable validation. No application framework, monorepo manager, or general-purpose build system is recommended: the repository does not demonstrate enough need to justify their maintenance cost.

## 2. Areas That Should Remain Unchanged

- **Keep `index.html`, `grade10/`, and `grade11/` at the repository root.** `index.html` directly links the two grade hubs and `teacher/schedule.html`; this is a simple, static-host-friendly navigation model. Moving the grade trees under a new `site/` directory would rewrite many relative paths and possibly public URLs without a demonstrated benefit.
- **Keep shared browser code in `assets/css/` and `assets/js/`.** Grade pages already consume these paths. The division is small and comprehensible; introducing a package workspace, bundler, or component framework would add a build requirement to a site that currently runs as static files.
- **Keep `assets/interactive/` together.** Its `index.html`, `template/`, `shared/`, and `tools/` directories form a coherent browser-only authoring/runtime subsystem. Its use of browser globals and downloaded configuration files is deliberate. Improve its workflow documentation and validation rather than moving it.
- **Keep `teacher/` as a top-level domain.** Teacher pages, schedule data, authoring input, and tools have a clear shared audience. The internal `assets/`, `pages/`, `authoring/`, and `tools/` distinction is appropriate; only the dated results inputs need a clearer source/data boundary.
- **Keep each academic year's LaTeX preamble and images inside that year's book.** `book2025-2026/preamble/` and `book2026-2027/preamble/` make each year's documents self-contained. Although the checkout contains many byte-identical cross-year files, centralizing them would make archived material depend on mutable current-year resources and would require fragile `\input` and image-path rewrites.
- **Keep source datasets beside the LaTeX activity that consumes them.** CSV files under term activity directories are contextual source inputs, not generic repository data. Moving them to a central data lake would reduce discoverability and complicate compilation paths.
- **Keep PDFs and LaTeX auxiliaries untracked.** `.gitignore` already excludes PDFs and common compiler outputs, while each book has `clean-latex.bat`. There is no evidence that a committed build-output tree is needed.
- **Keep the Cambridge dashboard and validator colocated.** `other/cambridge/grade3_heatmap_dashboard.html`, its CSS/JS/data, and `validate_grade3_heatmap_data.js` form a small, cohesive static subproject with an executable check. Relocating it merely to normalize top-level naming would not materially improve maintenance.
- **Do not treat directories containing “Test” as a test suite.** No runner invokes `other/Test Basic/` or `other/Test Codex/`; they contain standalone HTML quiz variants. They should be labeled as experiments, not moved into `tests/`.
- **Do not add CI merely because none exists.** A small optional check is justified after deterministic local validation commands exist. A broad deployment or test platform is not justified until the actual hosting and compilation expectations are known.

## 3. Improvement Opportunities

| Priority | Current area | Problem | Proposed change | Benefit | Effort |
| --- | --- | --- | --- | --- | --- |
| High | Local links in four Grade 10 pages and one teacher prototype | Five referenced local resources do not exist | Repair or retire each reference; add a zero-dependency local-reference validator | Prevents silently unstyled or nonfunctional pages and catches regressions | Small |
| High | `teacher/authoring/`, `teacher/tools/schedule_authoring_tool.html`, `teacher/assets/js/` | Missing `slots.csv` and ambiguous generated-file installation make schedule regeneration incomplete | Commit or remove the slot source as appropriate; document one canonical generation mapping; add a deterministic equivalence check | Makes canonical CSV edits reproducible and generated drift detectable | Medium |
| Medium | Repository root and subproject entry points | No contributor-oriented README or dependency/run inventory exists | Add a concise root `README.md` plus narrowly scoped READMEs where commands differ | Makes entry points, serving, validation, privacy, and build expectations discoverable | Small |
| Medium | `book2025-2026/` and `book2026-2027/` | Copy-forward relationship, active year, and archive policy are undocumented; current-year term/content labels conflict | Add per-year manifests and an archive/copy-forward policy; audit only demonstrated naming mismatches | Avoids editing the wrong year and copying mislabeled content while preserving self-contained books | Small |
| Medium | `teacher/tools/2026-02-19-results/` | Reusable Python code and ten dated external `.xls` inputs are mixed; dependencies are unpinned and undocumented | Split reusable code from dated inputs and add a minimal requirements/usage file | Clarifies code ownership, input provenance, retention, and reproducibility | Medium |
| Medium | `other/Test Basic/`, `other/Test Codex/`, `other/src/pages/` | “Test” implies automation and `src/pages` does not reveal publication status | After URL confirmation, group them under explicit `other/experiments/` and `other/standalone/` paths | Makes experimental and standalone content discoverable without pretending it is production or tested | Small |
| Low | LaTeX file naming within year trees | Verified typos, “Copy”, wrong grade prefixes, and term/path disagreements hinder search and automation | Maintain a reviewed exception/rename list; rename only after checking imports and published references | Improves reliable lookup and enables targeted compilation inventories | Medium |
| Low | CDN dependencies and external teaching links | Versions/providers are scattered; external availability is not locally controlled | Document an inventory and periodically check syntax/reachability; do not vendor by default | Exposes offline and access risks without adding a package toolchain | Small |

### 3.1 Repair local references and add a link check

- **Current paths:**
  - `grade10/src/G10_T2.html`
  - `grade10/src/pages/practice_activity3_1.html`
  - `grade10/src/pages/formulas.html`
  - `grade10/src/pages/main_examples.html`
  - `teacher/pages/schedule_prototype_generated.html`
- **Evidence of the problem (verified):** the four Grade 10 files reference `assets/css/decision-tree.css`, but that file does not exist. The teacher prototype loads `teacher/assets/generated/schedule-flat.generated.js`, but neither the directory nor file exists. A repository-wide parse of quoted `href` and `src` attributes found these five missing local targets. The missing teacher file is also one of the artifacts offered for download by `teacher/tools/schedule_authoring_tool.html`.
- **Proposed structure/workflow:** first decide whether the Grade 10 pages should use an existing stylesheet or whether the missing stylesheet was accidentally omitted; repair the references accordingly. For the prototype, either generate and track the declared artifact, update it to the supported runtime dataset, or remove/archive the prototype if it is obsolete. Add a small standard-library script at new path `tools/validate_local_references.py` that resolves local `href`/`src` values while ignoring fragments, `data:`, `mailto:`, and external URLs.
- **Expected benefit:** current pages stop making failed requests, and future moves or edits receive a fast repository-wide regression check.
- **Affected files, links, imports, or commands:** the five source pages above; the chosen stylesheet or prototype artifact; new command `python3 tools/validate_local_references.py`. The validator should include HTML/CSS references initially and report, rather than request, external URLs.
- **Migration steps:** (1) inspect the affected pages visually to identify the intended CSS; (2) determine whether the prototype is published; (3) make the minimum repairs; (4) add the validator with fixtures or self-tests for URL normalization; (5) run it from the repository root and serve affected pages over HTTP.
- **Compatibility/regression risks:** substituting an incorrect CSS file can change page layout. Removing the prototype or changing its data global can break a bookmarked URL. A naive validator can misclassify template strings or root-relative host paths; scope it to statically resolvable references and allow documented exclusions.
- **Priority / effort / status:** **high / small / required.** The repairs are required. Automating the check is required for the recommended target state but does not require CI.

### 3.2 Establish one reproducible schedule source-to-artifact contract

- **Current paths:** canonical input is identified as `teacher/authoring/schedule.csv`; generation UI is `teacher/tools/schedule_authoring_tool.html`; runtime data includes `teacher/assets/js/schedule-data.js` and `teacher/assets/js/schedule-data-base.js`; the prototype expects a third shape at `teacher/assets/generated/schedule-flat.generated.js`.
- **Evidence of the problem (verified):** the authoring tool fetches `teacher/authoring/slots.csv` on default load and uses it to validate every slot, but that path is absent. It downloads `schedule-flat.generated.js`, `schedule-norm.generated.js`, and `schedule-adapter.generated.js`; no generated destination directory or installation instructions exist. Conversely, both runtime schedule files declare themselves generated from `teacher/authoring/schedule.csv`, yet there is no clean-checkout command that reproduces and compares them. Generation is browser-download/manual-copy work, so schema or data drift is easy.
- **Proposed structure/workflow:** preserve the browser authoring UI, but define exactly one supported output contract. If slot definitions remain part of validation, add new source `teacher/authoring/slots.csv`; otherwise remove that dependency and derive/validate slots against the actual authoritative data. Document the mapping from each retained output to its runtime destination. Add a small deterministic generator/check command only if the same transformation can be shared or faithfully ported without maintaining two competing implementations. Generated files should retain headers identifying source, generator, and “do not edit” status.
- **Expected benefit:** a contributor can edit the CSV from a clean checkout, validate it, install the right artifact, and prove that committed runtime data is current.
- **Affected files, links, imports, or commands:** the paths above; `teacher/assets/js/class-data.js` if class IDs remain a validation dependency; all teacher schedule/class pages that load schedule globals. A possible command is `python3 tools/check_schedule_data.py --check`, but the implementation language should be chosen only after the browser transform is reviewed for parity.
- **Migration steps:** (1) identify the authoritative slot list and runtime data shape; (2) add the missing source or remove the obsolete requirement; (3) document output destinations; (4) create a golden comparison using current CSV/runtime files; (5) validate the weekly, full, and class pages; (6) only then retire unsupported generated shapes or the prototype.
- **Compatibility/regression risks:** date formatting and field names differ between canonical CSV and legacy runtime objects. Changing global names or load order can break all schedule pages. Preserve existing globals until visual and data-equivalence checks pass. Do not overwrite runtime files from a generator whose output has not been compared field by field.
- **Priority / effort / status:** **high / medium / required.** A CLI generator is **optional** if the browser workflow can instead become fully documented and verifiable.

### 3.3 Add concise contributor and subproject documentation

- **Current structure:** `REPOSITORY_STRUCTURE.md` is the only tracked Markdown file. Root `index.html` is user-facing rather than contributor-facing. No `README.md`, contribution guide, package manifest, requirements file, or LaTeX build guide exists.
- **Evidence of the problem (verified):** the repository contains several distinct execution models—static HTTP pages, browser authoring tools that use `fetch`, a Node validator, a pandas utility, and individually compiled LaTeX sources—but their commands and dependencies are not available from a normal root entry point. Running the Python utility's `--help` in the inspected environment fails before argument parsing because `pandas` is not installed. The canonical LaTeX engine and working directory are not declared.
- **Proposed structure/workflow:** add a short new root `README.md` that links rather than duplicates `REPOSITORY_STRUCTURE.md`, names published and contributor entry points, gives `python3 -m http.server` as the minimal local server, lists validation commands, and explains which areas are source, generated, archived, experimental, or externally sourced. Add scoped READMEs only where commands differ: proposed `teacher/README.md`, `teacher/tools/results-normalizer/README.md`, and `bookYYYY-YYYY/README.md` manifests.
- **Expected benefit:** contributors can find and run the site/tools without reverse-engineering imports, and future architectural documentation is less likely to become a substitute for operational instructions.
- **Affected files, links, imports, or commands:** documentation only; commands should include the Cambridge validator and the eventual local-reference/schedule checks. The README should inventory Python packages (`pandas`, legacy `.xls` engine such as `xlrd`, and optional `tabulate`) without claiming versions until a compatible environment is tested.
- **Migration steps:** (1) confirm hosting and LaTeX engine; (2) add root README with verified commands; (3) add only the scoped guides that contain unique information; (4) cross-link `REPOSITORY_STRUCTURE.md`; (5) exercise every copied command on a clean environment where practical.
- **Compatibility/regression risks:** stale docs are worse than no docs. Keep commands executable, avoid repeating the full tree, and assign the README update to the same change that alters a workflow.
- **Priority / effort / status:** **medium / small / required.** Separate contribution templates or a formal governance document are not currently justified.

### 3.4 Define academic-year manifests and copy-forward/archive rules

- **Current paths:** `book2025-2026/` and `book2026-2027/`, each with grade directories and its own `preamble/`.
- **Evidence of the problem (verified):** byte hashing found 159 duplicate groups, all spanning the two academic-year trees, representing about 2.59 MB of duplicated copies. That strongly supports a copy-forward workflow. However, no file identifies which year is active, whether the older tree is frozen, or how later fixes should propagate. In `book2026-2027/grade10/term_1/`, many filenames still carry `G10_T2_`, while Grade 10 has no `term_2/` directory. This may encode curriculum numbering rather than a mistake, so it must be resolved rather than automatically renamed.
- **Proposed structure/workflow:** keep both existing year roots unchanged. Add a small manifest README inside each year stating status (`active` or `archived`), included grades/terms, canonical compile working directory/engine, and copy-forward rules. Record whether fixes to shared content must be cherry-picked across years. Treat old years as immutable except for correctness/security fixes once confirmed archived. Use a hash report during annual rollover to distinguish intentional carry-forward from changed material; do not introduce symlinks or shared cross-year `\input`s.
- **Expected benefit:** contributors know where new work belongs and whether a fix must be applied twice, while archived PDFs remain reproducible from self-contained sources.
- **Affected files, links, imports, or commands:** new year READMEs; no LaTeX imports initially. A future rollover helper may report hashes but should never delete duplicates automatically.
- **Migration steps:** (1) owner confirms current year and term-label semantics; (2) add both manifests; (3) inventory compilable entry points and exceptions; (4) mark archive status; (5) use the policy for the next copy-forward.
- **Compatibility/regression risks:** aggressive deduplication would create cross-year coupling and can break `\input`, `\includegraphics`, and compilation working-directory assumptions. This proposal explicitly avoids it. Incorrectly declaring a year archived could hide active content.
- **Priority / effort / status:** **medium / small / required** for manifests and policy; hash tooling is **optional**.

### 3.5 Separate the results normalizer from dated input data

- **Current path:** `teacher/tools/2026-02-19-results/` contains reusable `results.py` and ten class `.xls` exports (`10A.xls` through `11E.xls`).
- **Evidence of the problem (verified):** the directory name describes one dated run, but the Python program is a general CLI that accepts files/directories and output options. Code and external inputs therefore share lifecycle and ownership. No dependency file exists, and execution currently stops with `ModuleNotFoundError: pandas` in the inspected environment. `results.py` itself explains that legacy `.xls` support needs a compatible `xlrd` and that `tabulate` is optional.
- **Proposed structure:** after retention/privacy confirmation, relocate reusable code to new `teacher/tools/results-normalizer/results.py`, add `teacher/tools/results-normalizer/README.md` and a minimal tested requirements file, and relocate retained inputs to new `teacher/data/results/2026-02-19/`. If inputs should not be retained, remove them in a separately reviewed data-retention change rather than silently moving them.
- **Expected benefit:** code changes no longer look like edits to a one-off data dump; dependencies, input provenance, retention, and output handling become explicit.
- **Affected files, links, imports, or commands:** the current Python script and ten `.xls` files; documentation or scripts that invoke the old path (none were found in tracked content). Example new command: `python3 teacher/tools/results-normalizer/results.py teacher/data/results/2026-02-19`.
- **Migration steps:** (1) confirm whether workbooks are appropriate to retain and whether they contain protected student information; (2) add README/requirements and test in an isolated environment; (3) use `git mv` for script and approved inputs; (4) run old and new script versions against the same copies and compare normalized output; (5) update root documentation.
- **Compatibility/regression risks:** moving data can break personal shell commands even though no tracked references exist. Pinning versions without testing can reduce compatibility. Data-history/privacy decisions may require removal outside this structural proposal.
- **Priority / effort / status:** **medium / medium / required** to document dependencies and data status; relocation is **required only if the workbooks remain tracked**.

### 3.6 Give experiments and standalone pages explicit locations

- **Current paths:** `other/Test Basic/`, `other/Test Codex/`, and `other/src/pages/g9-t3-correlation-coefficient.html`.
- **Evidence of the problem (verified):** the two “Test” directories contain five standalone quiz HTML variants and no automated test configuration. Spaces and title case also make shell and URL handling less convenient. The Grade 9 page is nested under generic `other/src/pages/`, is not linked from the root hub, and its production/publication status is undocumented. `other/cambridge/`, by contrast, has a cohesive name and validator and should remain unchanged.
- **Proposed structure:** conditional on published-URL confirmation, move the quiz files to new `other/experiments/quiz-basic/` and `other/experiments/quiz-codex/`; move the Grade 9 page to new `other/standalone/grade9/g9-t3-correlation-coefficient.html`. Add new `other/README.md` listing each entry point, owner/purpose, and status. Do not create a root `tests/` directory for these pages.
- **Expected benefit:** directory names communicate lifecycle accurately and reduce the chance that manual demos are mistaken for regression coverage.
- **Affected files, links, imports, or commands:** the six HTML files and any untracked hosting/bookmarks. No tracked incoming links to these paths were found, but absence of a deployment manifest means external URLs remain an unresolved risk.
- **Migration steps:** (1) confirm hosted URLs/consumers; (2) add status README before moves; (3) move one group at a time with `git mv`; (4) update internal relative imports and root documentation; (5) run the local-reference validator and manually open each page through HTTP; (6) retain redirect stubs only if the static host supports the required behavior.
- **Compatibility/regression risks:** static hosts usually do not redirect moved files automatically; bookmarks may break. Case sensitivity can expose paths that worked only on Windows. If URLs cannot be audited, keep the physical paths and use only `other/README.md` labels.
- **Priority / effort / status:** **medium / small / optional.** Documentation is recommended even if relocation is rejected.

### 3.7 Audit only verified LaTeX naming anomalies

- **Current paths/evidence (verified examples):** five `G10_T2_*_soution.tex` files occur in each year; `book2026-2027/grade10/term_1/1-practice_activities/G10_T1_L1_C1-C2_practice_activity2 - Copy.tex` has an ambiguous copy suffix; three `G10_T3_L4_C10_dataset_*.csv` files sit under `book2026-2027/grade11/term_3/2-learning_evidences/` alongside similarly named `G11_*` datasets; `proyect` and `suplementary` spellings recur across both years. These patterns make searches and generated inventories unreliable, but some may be intentional legacy identifiers.
- **Proposed workflow:** create a reviewed rename manifest before touching files. Prioritize wrong grade/term identifiers and ambiguous copies; do not mass-normalize language or capitalization merely for aesthetics. For each candidate, search all `\input`, graphics, CSV references, HTML links, and scripts, then compile affected documents before and after.
- **Expected benefit:** removes genuine ambiguity while avoiding a high-churn naming campaign.
- **Affected files, links, imports, or commands:** only approved manifest entries and their literal references. Git history can trace renames, but external links and local LaTeX working-directory assumptions still require checks.
- **Migration steps:** (1) ask owners which identifiers are erroneous; (2) record old/new paths; (3) rename one content cluster per commit; (4) update literal references; (5) compile affected entry points; (6) run local-reference and missing-LaTeX-input scans.
- **Compatibility/regression risks:** case-only renames and spaces behave differently across filesystems; LaTeX can resolve resources relative to invocation directory rather than source directory; external references are not discoverable from Git.
- **Priority / effort / status:** **low / medium / optional.** No blanket naming normalization is recommended.

### 3.8 Inventory, but do not vendor, external dependencies

- **Current paths:** CDN imports are embedded in individual HTML pages and include pinned jsPDF 2.5.1, SheetJS 0.20.3, QRCode 1.0.0, MathJax 3, and unpinned D3 `@7`; grade pages also contain many SharePoint, YouTube, and Canva links.
- **Evidence of the problem (verified):** there is no dependency inventory, and the static pages have no offline fallback. External teaching URLs may require access and cannot be validated solely by local reference checks. However, the URLs generally identify versions, and no evidence shows that vendoring is required.
- **Proposed workflow:** document external runtime dependencies, version URLs, purpose, and affected entry points in the root README or a small `docs/DEPENDENCIES.md` only if the list outgrows the README. Add an optional, nonblocking external-link report with timeouts; do not fail changes merely because an access-controlled SharePoint resource rejects an unauthenticated check.
- **Expected benefit:** dependency upgrades and offline limitations become visible without introducing npm or duplicated vendor files.
- **Affected files, links, imports, or commands:** documentation first; page edits only when an owner approves an upgrade. External checks must redact or avoid reproducing access query values in logs.
- **Migration steps:** inventory, classify public versus access-controlled, record pinned versions, manually smoke-test critical pages, then decide whether any single dependency merits vendoring based on actual outages.
- **Compatibility/regression risks:** automated requests may trigger rate limits or false failures; CDN upgrades can change globals. Keep this check optional until its signal quality is demonstrated.
- **Priority / effort / status:** **low / small / optional.** No package manager is recommended.

## 4. Proposed Repository Tree

This selective tree shows only recommended or decision-dependent structural changes. `[unchanged]`, `[new]`, `[relocated]`, `[generated]`, `[archive candidate]`, and `[conditional]` describe the target state.

```text
.
├── README.md                                      [new: contributor entry point]
├── REPOSITORY_STRUCTURE.md                        [unchanged: verified architecture map]
├── REPOSITORY_RESTRUCTURING_PROPOSAL.md           [new: this proposal]
├── index.html                                     [unchanged: public site entry]
├── assets/                                        [unchanged]
├── grade10/                                       [unchanged]
├── grade11/                                       [unchanged]
├── tools/
│   ├── validate_local_references.py               [new]
│   └── check_schedule_data.py                     [new, optional if parity is feasible]
├── teacher/
│   ├── README.md                                  [new]
│   ├── authoring/
│   │   ├── schedule.csv                           [unchanged: canonical source]
│   │   └── slots.csv                              [new, conditional on authority decision]
│   ├── assets/js/                                 [unchanged; generated files clearly marked]
│   ├── data/results/2026-02-19/                   [new, conditional]
│   │   └── 10A.xls ... 11E.xls                    [relocated external inputs]
│   └── tools/
│       ├── schedule_authoring_tool.html            [unchanged location]
│       └── results-normalizer/                     [new]
│           ├── README.md                           [new]
│           ├── requirements.txt                   [new after version testing]
│           └── results.py                         [relocated reusable utility]
├── book2025-2026/                                 [unchanged tree; archive candidate]
│   ├── README.md                                  [new: status/build/copy-forward manifest]
│   └── preamble/                                  [unchanged and year-local]
├── book2026-2027/                                 [unchanged tree; active status unconfirmed]
│   ├── README.md                                  [new: status/build/content manifest]
│   └── preamble/                                  [unchanged and year-local]
└── other/
    ├── README.md                                  [new: publication/status index]
    ├── cambridge/                                 [unchanged]
    ├── experiments/                               [new, conditional on URL audit]
    │   ├── quiz-basic/                            [relocated from `Test Basic/`]
    │   └── quiz-codex/                            [relocated from `Test Codex/`]
    └── standalone/grade9/                         [new, conditional on URL audit]
        └── g9-t3-correlation-coefficient.html     [relocated from `src/pages/`]
```

No `dist/`, monorepo package hierarchy, centralized LaTeX preamble, or committed PDF directory is proposed.

## 5. Migration Plan

### Phase 0 — Record a baseline

- **Exact moves/renames:** none.
- **References to update:** none.
- **Validation:** record `git status --short`; run `node other/cambridge/validate_grade3_heatmap_data.js`; run a one-off local-reference scan; hash both book trees; inventory all literal LaTeX `\input`, `\include`, `\includegraphics`, and CSV references. Serve the repository with `python3 -m http.server 8000` and smoke-test root/grade/teacher entry points.
- **Rollback point:** baseline commit and captured reports.
- **Dependencies:** none.

### Phase 1 — Repair demonstrated broken references

- **Exact moves/renames:** none unless the owner declares `teacher/pages/schedule_prototype_generated.html` obsolete, in which case archive or delete it in a dedicated change rather than combining it with unrelated moves.
- **References to update:** the four references to missing `assets/css/decision-tree.css`; the prototype's generated script reference or data contract.
- **Validation:** new `python3 tools/validate_local_references.py`; browser smoke tests for the five affected pages; existing Cambridge validator.
- **Rollback point:** commit containing only reference repairs and validator.
- **Dependencies:** Phase 0 reports; prototype ownership decision.

### Phase 2 — Make schedule generation coherent

- **Exact moves/renames:** none initially. Add `teacher/authoring/slots.csv` only if confirmed canonical. Retire unsupported generated outputs only after consumers are proven absent.
- **References to update:** authoring-tool fetch path and validation messages if slots are derived elsewhere; output names/destinations; prototype import; schedule README.
- **Validation:** compare generated objects to `teacher/assets/js/schedule-data.js` and `schedule-data-base.js`; verify counts/keys/dates; open `teacher/schedule.html`, `teacher/pages/full_schedule.html`, and representative Grade 10/11 class pages.
- **Rollback point:** one commit for authoritative input/schema, a second for generator/check, and a third for consumer retirement.
- **Dependencies:** Phase 1 validator and authoritative-slot/data-shape decisions.

### Phase 3 — Add operational documentation and year manifests

- **Exact moves/renames:** none.
- **References to update:** add root links among `README.md`, `REPOSITORY_STRUCTURE.md`, teacher guide, and book manifests.
- **Validation:** run every documented command from the stated working directory; confirm every linked path exists; have the content owner confirm active/archive labels and term semantics.
- **Rollback point:** documentation-only commit.
- **Dependencies:** schedule contract from Phase 2; confirmed host and LaTeX engine for definitive commands.

### Phase 4 — Separate results code and data

- **Exact moves/renames:** `git mv teacher/tools/2026-02-19-results/results.py teacher/tools/results-normalizer/results.py`; after retention approval, `git mv` the ten `.xls` files into `teacher/data/results/2026-02-19/`.
- **References to update:** root/teacher/results READMEs and any contributor commands. No tracked code references to the old path were found, but repeat the search immediately before migration.
- **Validation:** create a clean Python environment using tested requirements; run old/new revisions on copies of the same workbooks; compare normalized output and CLI help; confirm Git detects moves.
- **Rollback point:** one isolated commit that can be reverted without affecting the website.
- **Dependencies:** data-retention/privacy decision and tested Python versions.

### Phase 5 — Clarify `other/` physically, if URLs permit

- **Exact moves/renames:** move `other/Test Basic/` to `other/experiments/quiz-basic/`; move `other/Test Codex/` to `other/experiments/quiz-codex/`; move `other/src/pages/g9-t3-correlation-coefficient.html` to `other/standalone/grade9/`.
- **References to update:** internal asset/CDN references if relative depth changes, root/other documentation, hosting configuration or inbound links discovered during the audit.
- **Validation:** local-reference check, case-sensitive HTTP serving, manual opening of all six pages, and verification of any known public URLs.
- **Rollback point:** separate commit per moved content group. If URL ownership is unknown, stop after adding `other/README.md` and make no moves.
- **Dependencies:** deployment/publication answers and Phase 1 validator.

### Phase 6 — Apply reviewed LaTeX renames incrementally

- **Exact moves/renames:** only entries approved in a rename manifest; begin with confirmed wrong-grade datasets or the ambiguous `- Copy` file, not a mass spelling rewrite.
- **References to update:** literal LaTeX inputs, image/CSV paths, shell/editor recipes, and documented entry-point manifests.
- **Validation:** compile every affected entry point with the documented engine and working directory; scan for missing inputs; compare PDF page count or render where meaningful; ensure ignored outputs do not enter Git.
- **Rollback point:** one commit per grade/term cluster.
- **Dependencies:** Phase 3 compiler documentation and owner decisions on identifiers.

## 6. Tooling and Workflow Improvements

### Required, proportional improvements

1. **Document a local static server:** from the repository root, `python3 -m http.server 8000`. This is enough for relative assets and browser tools using `fetch`; no development server dependency is warranted.
2. **Add deterministic local-reference validation:** a standard-library script should exit nonzero for missing local static targets, print source/reference/resolved path, and support a small explicit exclusion list. It must not conflate external reachability with local correctness.
3. **Expose the existing Cambridge check:** list `node other/cambridge/validate_grade3_heatmap_data.js` in the root README. Keep its current location because it validates a colocated data/dashboard contract.
4. **Verify generated schedule drift:** whether implemented in Python or JavaScript, compare canonical input transformation to committed generated data. Avoid requiring a package installation for a transformation currently performed with native browser JavaScript.
5. **Document Python dependencies:** test and record compatible `pandas` and `xlrd` versions; clearly mark `tabulate` optional. A requirements file belongs beside the utility, not at repository root, because no other Python application exists.
6. **Document LaTeX compilation per year:** specify distribution, engine, working directory, number of passes, shell-escape expectations, and representative smoke documents. Do not add a build-all command until the entry-point inventory distinguishes compilable documents from included fragments/templates.

### Optional enhancements after the required checks stabilize

- **Minimal CI:** run the local-reference validator, Cambridge validator, and schedule drift check on relevant changes. Add this only after each command is deterministic locally. LaTeX compilation in CI should start with a small representative matrix because 300 `.tex` files and a broad package set may make build-all expensive and noisy.
- **External-link report:** check public CDN/resource URLs with timeouts and report access-controlled links separately. Keep it nonblocking until false-positive behavior is understood.
- **Annual copy-forward hash report:** report identical/changed/new/removed files between book years. It should inform editorial review, not automatically deduplicate or overwrite files.
- **HTML standards validation:** consider it after broken local paths are fixed; inline math/SVG and large standalone pages may require documented exceptions. No new Node package is justified solely for this check.

### Tools explicitly not recommended now

- No npm workspace, bundler, static-site generator, container, monorepo orchestrator, or general task runner.
- No shared cross-year LaTeX package or symlink-based deduplication.
- No committed build artifacts or vendored CDN libraries absent a demonstrated availability requirement.
- No automated test framework created around the manual quiz examples.

## 7. Risks and Trade-offs

- **Relative URL breakage:** moving any HTML file changes the depth of `../` references. Existing static hosts may expose repository paths directly and may not support redirects. This is why `grade10/`, `grade11/`, `assets/`, and teacher entry points remain in place and `other/` moves are conditional.
- **LaTeX import failures:** many documents assume a particular working directory or use search paths for preambles, graphs, images, and logos. Cross-year deduplication or broad directory renames could make apparently valid files uncompilable. Preserve year-local resources and compile every affected cluster.
- **Generated-data incompatibility:** schedule consumers use browser globals and legacy field shapes. A generator can be deterministic yet still emit the wrong schema. Establish golden comparisons and retain adapters until consumers are tested.
- **Archive divergence versus independence:** keeping duplicate book content costs storage and can require fixes twice, but it preserves historical reproducibility. At the present scale, independence is more valuable than saving roughly 2.59 MB.
- **External data handling:** dated assessment workbooks may have provenance, retention, or privacy constraints not stated in the repository. A cleaner directory does not resolve those concerns; obtain an explicit decision before moving or retaining them.
- **Dependency pinning:** pins improve reproducibility only when tested together. Guessing exact versions from current import errors can create a misleading setup. Test first and scope dependencies to the one Python utility.
- **CI maintenance:** checks that depend on external links, browser downloads, a full TeX distribution, or access-controlled services can be flaky and costly. Begin with zero-network deterministic checks.
- **Documentation drift:** additional READMEs create maintenance work. Keep the root guide short, store unique workflow details near their subproject, and update docs in the same commits as workflow changes.
- **Naming churn:** spelling and casing consistency alone does not justify breaking links. Rename only confirmed ambiguity or wrong identifiers, using a reviewed manifest and isolated commits.

## 8. Recommended Target State

### Smallest coherent required set

1. Repair the five verified missing local references or explicitly retire the obsolete consumers.
2. Add a zero-dependency local-reference check and surface the existing Cambridge validator.
3. Resolve the missing schedule slot authority, document one source-to-runtime artifact mapping, and add a deterministic drift/equivalence check.
4. Add a concise root README, a teacher workflow guide, and per-year status/build manifests.
5. Document the Python utility's tested dependencies and decide the retention/provenance status of its `.xls` inputs; if retained, separate reusable code from dated data.
6. Preserve the current root grade/site layout, year-local LaTeX resources, colocated activity datasets, and Cambridge subproject.

This set addresses actual broken references, an incomplete generation workflow, and major discoverability/reproducibility gaps without changing public site paths or introducing a framework.

### Optional later refinements

- Relocate quiz experiments and the standalone Grade 9 page after public URL confirmation.
- Rename only owner-confirmed LaTeX anomalies after compiler documentation exists.
- Add minimal CI after local commands are stable.
- Add external-link and annual book-diff reports if contributors find the manual audits burdensome.

## 9. Open Questions

1. **Which static host and public base URL are authoritative?** This must be known before moving `other/` pages or retiring `teacher/pages/schedule_prototype_generated.html`.
2. **Is `teacher/pages/schedule_prototype_generated.html` still a supported entry point?** If yes, which generated artifact and global schema should it consume?
3. **What is the authoritative source for schedule slots?** Should `teacher/authoring/slots.csv` be committed, derived from an existing schedule/class dataset, or removed from validation?
4. **Which schedule output is canonical at runtime?** The relationship among flat, normalized, adapter, `schedule-data.js`, and `schedule-data-base.js` must be settled before automation.
5. **Which academic-year tree is active, and when does a year become immutable?** This determines manifest status and whether fixes should be backported.
6. **Do `G10_T2_*` files under `book2026-2027/grade10/term_1/` reflect intended curriculum numbering or a copy-forward placement error?** Do not rename or move them until answered.
7. **Which TeX distribution, engine, invocation directory, and representative documents define supported compilation?** These are required before a reliable LaTeX validation matrix or rename campaign.
8. **May the ten dated `.xls` assessment exports remain in version control, and what provenance/retention rules apply?** This must precede the proposed code/data separation.
9. **Are the quiz variants and Grade 9 standalone page externally linked or intentionally published?** If unknown, leave their paths unchanged and clarify status only in documentation.

