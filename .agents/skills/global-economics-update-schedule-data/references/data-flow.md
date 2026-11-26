# Active data and consumer map

Contents: sources/schemas; navigation/renderers; calendar constraints; validation/preview.
Verified on 2026-11-26. Recheck cited live implementations before future edits; examples and historical counts are not permanent requirements. Never traverse `teacher/assets/js/databases/archive/`.

## Sources and schemas

`teacher/authoring/lesson-workflow.js` reads `schedule.csv` through `csv.js`, plus `lessons.json`'s `lessons` and `catalog` arrays. `build()` validates references, assignments, overrides, calendar coverage and material metadata. `generate()` writes exactly these active files under `teacher/assets/js/databases/`:

| Output | Global | Record shape / consumer |
| --- | --- | --- |
| `schedule-data.js` | `window.SCHEDULE_DATA` | Meeting identity fields plus Description, Material, Material teacher, Summary. Class detail and full schedule. |
| `schedule-data-base.js` | `window.SCHEDULE_DATA` | Grade, Class #, Term plus those four content strings. Undated catalog; no active frontend importer was found. |
| `materials-data.js` | `window.MATERIALS_DATA` | Grade, Term, uppercase Section, Class #, ISO Date, Materials. Class detail lookup and dated materials page. |
| `materials-data-base.js` | `window.MATERIALS_DATA_BASE` | Grade, Term, Class #, Materials. Undated materials page. |

The two schedule scripts overwrite the same global: never load them together or invent a dated-page fallback. Materials globals are distinct and load together in `materials.html`. Generation resolves all four from linked lesson assignments/defaults, validates before replacement, stages files and rolls back reported I/O failures. `--check` compares deterministic output (normalizing CRLF) without writing.

### Dated meetings and assignments

CSV header order is fixed:

```text
Grade,Section,Class #,Date,Term,Weekday,Day,Status,Reason,Canceled summary,Lesson ID,Overrides
```

- Grade, Term, Day parse as numbers; empty numeric fields become null. Canonical source sections are A–E and case-sensitive `Seminar`. Dates must be zero-padded `YYYY / MM / DD`; Weekday is the full English name. Rows sort by grade, section (`localeCompare`), date.
- Authoring identity is `Grade|Section|Date`. Meeting-owned fields are Grade, Section, Class #, Date, Term, Weekday, Day. They do not move during lesson reordering/postponement. Class # is a displayed cycle-meeting label, never lesson identity or a material ordinal crosswalk.
- `scheduled` requires a known grade/term-compatible assignment. `canceled` is in-term, with no ID or overrides. `unassigned` has null Term and no assignment, only outside terms. Only canceled rows carry Reason/Canceled summary.
- Overrides is a JSON object allowing only Description, Summary, Material, Material teacher, Materials. Merge is shallow. Materials replaces the complete array; preserve mock resources and empty assessment lists. ID and overrides move together.
- A lesson ID may occur only once per grade/section/term. Intentional repeats need new IDs. Historical shared variants and explicit section overrides must not be flattened into catalog defaults.
- Cancellation emits Description `No Class` + exact Reason suffix, Summary Canceled summary or `No Class`, both legacy material strings `-`, Materials `[]`. CLI adds ` - reason`; leave Canceled summary empty for new cancellations. Preserve historical punctuation/labels.
- Dated materials exist for every in-term meeting, including canceled/empty meetings. Out-of-term schedule placeholders have `-` content and no dated material record; do not assign lessons just to eliminate expected missing-material warnings.

### Lessons and base catalog

Lesson fields: permanent opaque UUID `id`, numeric Grade, Term 1–3, kind (`instruction` or `extra`), nonempty Description, Summary, Material, Material teacher strings, and required Materials array. `-` is a valid existing placeholder. Keep IDs on content edits; allocate new definitions with `node -e "console.log(require('node:crypto').randomUUID())"`.

Catalog slots are `{ Grade, Term, "Class #": "ordinal", lessonId }`, unique by Grade/Term/Class #, with digit-string ordinals and no Date/Section. Base content uses lesson defaults, never dated overrides. Enumerate both catalog and dated references before changing a definition. A base-only change can require a new definition and repointing only that slot.

Seminar conventions: numeric lesson/datum Grade 10; source/dataset schedule Section `Seminar`; emitted materials Section `SEMINAR`; reference key `10SEMINAR`; display `10S`; catalog Grade string `10S` resolves to numeric lesson Grade 10. Keep seminar definitions distinct from regular Grade 10. Present seminar catalogs have sequential 9/10/9 slots in Terms 1/2/3; preserve unless asked to change them. Some Term 3 base placeholders have no dated assignment; do not populate them by assigning out-of-term meetings.

### Materials

`teacher/assets/js/materials-validation.js` exposes `window.MaterialsValidation` and CommonJS. Cards require Acronym (trimmed 1–4 characters), meaningful nonempty Name, absolute HTTP/S Hyperlink, Category from:
`slides`, `classroom-activities`, `practice-activities`, `extra-resources`, `mock-practices`.
Names equal to category labels/narrow singular aliases are rejected after normalization. Empty arrays and unknown fields warn but are valid. Missing/null arrays, malformed cards and duplicate keys fail. URL validation checks syntax, not remote availability.

Dated material key is `Grade|UPPERCASE_SECTION|YYYY-MM-DD`; base key is `Grade|Term|Class #`. No grade/section/date query means base mode; supplying any requires all three. Requests normalize date and section, but persisted dated records must already be ISO/uppercase. `10S` is valid only as base Grade.

`schedule-renderer.js/findMaterialsRecord()` additionally checks Class # alongside grade, case-normalized section and normalized date. Preserve this agreement. A valid empty meeting still has a materials button leading to an empty state. Missing, malformed, ambiguous and unavailable data have distinct handling; never mask missing required data with `[]`.

Legacy Material and Material teacher strings are distinct from structured Materials. Class detail buttons use Materials; the full schedule displays legacy Material text. Changing one does not automatically change the other.

Preserve existing links or use verified supplied/repository targets. Regular Term 2 references include `grade10/src/G10_T2.html`, `grade11/src/G11_T2.html`; seminar uses `seminars/src/G10_T2.html`, existing guides and anchors. Current seminar assessments reuse guides/instruction anchors, not invented assessment PDFs. Resolve relative links against the established published source URL; verify local targets/anchors when applicable. Retain placeholders unless replacement is requested.

### Directly maintained active data

| File under `teacher/assets/js/databases/` | Authority and affected consumers |
| --- | --- |
| `year-calendar-data.js` | Calendar-year date/cycle-day matrices, holidays `{date: ISO, name}`, academic-year configuration with inclusive term ranges. `window.academicCalendar` and CommonJS. See below. |
| `class-data.js` | CLASS_METADATA keyed by uppercase grade+section (coordinator; seminar name/shortLabel), CLASS_STUDENT_LISTS (pdfUrl, students with name), CLASS_NOTES (title/date/items/links with url/label). class-page.js consumer; relative pdfUrl resolves from pages/class.html. PDF link is teacher-mode-only; notes/nonempty students arrays are not automatically teacher-only. |
| `teacher-seminar-data.js` | TEACHER_SEMINAR_STUDENTS array `{firstNames, surnames, className}`; class-page.js renders its order for display classKey 10S. Roster edits are separate from seminar lesson edits; preserve conditional loading. |
| `teacher-tasks.js` | `window.magisTasks` array `{description, dueDate}` with timezone-bearing ISO timestamps. tasks.html/tasks.js display/edit countdowns in America/Bogota; requested Bogotá wall times use explicit `-05:00`. Existing browser File System Access save targets this same file; no schedule generator needed. |

## Navigation and renderers

| Entry / path | Actual dependency and behavior |
| --- | --- |
| `teacher/schedule.html`, `teacher/schedule-teacher.html` | Static six-day timetable, periods, rooms/duties and class links in HTML. Import only calendar data, schedule-teacher.js and theme-toggle.js. Script highlights today's cycle/time and rewrites links; no lesson database import. Public landing has fewer cards. |
| Landing class links | schedule-teacher.js rewrites class_schedules links directly to `pages/class.html?grade=10&section=A&mode=public|teacher&origin=schedule|schedule-teacher`. 10Seminars maps to Seminar. Legacy class_schedules HTML files redirect with public-default parameters; direct visits do not retain teacher mode. |
| `pages/class.html` | Inline query setup + class-data.js/class-page.js build metadata, notes, shell; dated schedule/materials + schedule-renderer.js populate grade/section-filtered rows; schedule-today.js and inline controls handle today/past rows. No base catalog fallback. Origin chooses breadcrumb. |
| Teacher seminar route | Real teacher landing click writes sessionStorage `grade10SeminarNavigationContext`, destination `10Seminar`, createdAt. class.html consumes/removes it; requires grade query `10`, Seminar section, teacher mode, schedule-teacher origin and age 0–<30000 ms. Only then inline code attempts roster script loading via document.write. Query flags alone are insufficient; verify actual runtime load. |
| `pages/full_schedule.html` | Imports calendar, class reference/page helpers, dated SCHEDULE_DATA, schedule renderer/today helpers, full-schedule-page.js/full-schedule-today.js and theme. Aggregates dated records, normalizes class IDs (Seminar displays Sem), sorts and renders legacy Material text. Does not import MATERIALS_DATA or create class-detail cards. `?date=ISO` focuses date; origin selects back link. |
| `pages/materials.html` | Both materials databases + materials-validation.js/materials-page.js. Dated query renders one meeting; absent grade/section/date renders grouped base catalog including Grade 10S. Back link currently points to public schedule; do not silently add teacher-origin propagation. |
| `pages/general_calendar.html` | Calendar data + inline renderer for dates, holidays, terms, cycleNumber-cycleDay labels and filters. Origin selects Week View return. Date clicks link to full_schedule.html?date=ISO without forwarding origin. Title/filter defaults also contain static year bounds. |
| `pages/class_view.html` | class-view.js loads hidden iframe of selected public/teacher landing and extracts rotation-schedule rows/time ranges/day cells; academicCalendar supplies today's cycle/holiday. Not a lesson view. countdown_timer.js supplies its timer. |
| Teacher ancillary paths | Static study-hour.html and assets/pdf/week.pdf; magis.html has static resources and access=teacher link visibility, forwarding context to tasks.html. Current teacher landing Magis link has no access flag. tasks.html imports teacher-tasks.js/tasks.js. seminarios.html is a static/context-sensitive resource page, not the seminar lesson catalog. |

`principal-schedule.js` contains an older fetch/DOMParser class-page lookup; `render-weekly-schedule-table.js` injects weekly markup. Neither is imported by the current landing pages. Follow actual imports, iframe and script loading rather than assuming header comments prove active dependencies.

## Calendar constraints

`year-calendar-data.js` keeps aligned Monday–Sunday date and cycle-day matrices (1–6 or null) by calendar year. Holidays are separate: a holiday name does not automatically remove a cycle day. Academic-year boundaries cover months; exact inclusive terms currently end 2026-11-07, 2027-03-13, 2027-05-11. Read live configuration for future edits.

Computed cycle numbers reset per term and advance only on an existing 6→1 Day wrap; after the final term they continue without assigning a term. `getTermCycleNumber()` separately resets on entry into the unassigned period for seminar validation/audits. Calendar labels use six days; regular Class # labels use two meetings per section/cycle; seminar uses one. These are different sequences.

`authoring/calendar-validation.js` derives complete expected meeting coverage from cycleDayRegistry/calendarRegistry and its meetingDays mapping:

```text
10A 1,3   10B 3,4   10C 1,5   10D 4,6   10E 1,5   10Seminar 4
11A 1,3   11B 2,3   11C 1,6   11D 3,5   11E 1,6
```

It enforces exact coverage, supported classes, unique identities, canonical dates, weekday, Day, term, Class # and sorted order. Within terms labels use term cycle plus the meeting's index in that section's day list. Regular sections explicitly continue their two-meeting sequence after a hardcoded 2027-05-11 cutoff, starting from each preceding label; seminar keeps term-scoped numbering. Preserve partial cycles (6-1→6-2) rather than resetting all tails to 7-1. A new year may need validator work beyond ordinary data scope: identify it.

Calendar loading computes cycle numbers in memory; it never authors CSV meetings. After calendar changes, explicitly reconcile requested meeting coverage/metadata and assignment intent, distinguishing an existing canceled meeting from removed/changed cycle-day coverage. Then regenerate/check. Term changes may require compatible lesson/catalog decisions; never cross-assign terms merely to pass validation.

Other calendar consumers include school-day-timer.js, timer-view.js, class/exam instruction pages and full-schedule cycle displays. Check them when affected. Timetable changes can also affect static landing markup and the validator's meetingDays map.

## Validation and preview

Use SKILL.md commands for generated data. At creation, PowerShell with Node v24.19.0 accepted the literal `teacher/authoring/tests/*.test.js` through Node's glob handling. For older runtimes use explicit filenames or a Get-ChildItem array; do not assume PowerShell expands native globs or accepts Bash heredocs. Generator CLI and --check were exercised in an isolated whitelist copy of sources/dependencies; all four generated outputs matched live files without rewriting production data.

Inspect tests for current scope and archive exclusion before running:

- `lesson-workflow.test.js`: validation, complete assignment movement/cancellation, capacity, deterministic generation/staleness/failure behavior, material joins; also frozen migration hashes and isolated legacy importer fixtures. Tests exercising migration do not justify running the importer as routine authoring.
- `materials-workflow.test.js`: schema/category/URL rules, dated/base card rendering, empty/error states and joins; also exact Term 2 sequences/links and preservation hashes.
- `seminar.test.js`: distinct identifiers/catalogs, dated/base semantics and existing source-link/anchor checks; exact counts/orders/hashes describe current content.
- `calendar-numbering.test.js`, `post-cutoff-numbering.test.js`: continuation, term behavior, rendered calendar and coverage rejection; also fixed dates/counts/fingerprints.
- `teacher/tools/tests/tasks-countdown.test.js` for tasks; `school-day-timer.test.js` for calendar-dependent timers. Direct class reference/roster edits need targeted syntax/global/schema and rendered-consumer checks; there is no equivalent complete authoring validator for them.

Creation baseline: read-only generation check and materials validator pass; authoring suite 45/46 pass. Existing failure `rendered continuing codes use the existing green style without claiming Term 3` reaches a CSS assertion expecting `.cycle-day.term-3` to use `--term-3-code`, while `teacher/assets/css/general_calendar.css` uses `--term-3`. This observed mismatch does not authorize skipping/weakening the check or establish the intended visual appearance. Reassess live state.

`migration-baseline.json` is immutable audit input, not current authoring truth. Intentional changes may invalidate historical fingerprints/exact sequences. Explain which requested records differ; retain behavioral invariants and compare unaffected records against pre-edit snapshots. Report unresolved baseline failures. Never blindly refresh hashes, delete tests, disable calendar validation or rerun migration to manufacture a pass.

Serve repository root with an available local HTTP server for visible changes, e.g. `python -m http.server 8000 --bind 127.0.0.1` in a managed session; stop after preview. Choose real dates/sections from live source:

- Follow public and teacher landing class links; verify modes/back links, affected rows and an unchanged section. Expand hidden past dates.
- Follow the actual dated materials button; inspect full list, names/categories/URLs and a valid empty state. Open materials.html without query for affected base slots.
- Check full schedule with ?date=YYYY-MM-DD for date/Class #, content/summary-dependent UI and legacy Material text.
- Calendar edits: inspect Calendar View around changed dates/term boundaries and Class View from both origins; check cycle labels/holidays and timetable-derived current blocks.
- Roster edits: use a real teacher landing click and inspect network/console/roster cells, then public/direct-query and expired/reused-context routes; verify roster script is absent outside intended context. Browser loading defects need explicit frontend scope, not roster-data workarounds.
- Class reference/tasks: verify notes/PDF/student visibility or due-time/countdown in actual consumers and an unchanged neighboring record.

Skill creation used source inspection and existing DOM-adapter tests, not a full browser smoke test. Calendar CSS mismatch and browser roster loading remain checks for affected future work; do not present them as browser-verified.
