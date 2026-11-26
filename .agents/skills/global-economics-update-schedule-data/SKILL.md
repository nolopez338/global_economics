---
name: global-economics-update-schedule-data
description: Update active lesson, meeting, materials, calendar, class reference, task, and seminar roster data supporting the Global Economics teacher schedule pages. Identify static timetable or frontend dependencies before expanding a data update into page or behavior changes.
---

# Update schedule data

Translate the request into the smallest authoritative-source edit and its affected artifacts. All paths below are repository-relative; run commands from the repository root.

## Establish scope and live relationships

- Read applicable repository instructions and `teacher/authoring/README.md`. Read the affected domain in [the data and consumer map](references/data-flow.md), then confirm its schemas, imports, lookup keys and validators against live code. Counts, dates, examples and historical assertions are not permanent requirements.
- Exclude `teacher/assets/js/databases/archive/` completely from discovery, reading, editing, generation and validation. Use explicit active filenames or exclude `**/archive/**` before recursive searches. Do not enumerate that directory or run commands that traverse it.
- Inspect existing changes without disturbing unrelated work. Establish grade, section, term, dates and intended reach. Find every meeting and catalog reference to an affected lesson ID and inspect their overrides before a shared edit.
- Both landing pages contain static six-day timetables; Class View reads that markup through an iframe. Dated lesson edits do not alter periods, rooms or duties. For those or frontend behavior, identify the required page/renderer scope explicitly; do not silently expand an ordinary data update.

## Choose the authoritative source

| Requested change | Edit or operation |
| --- | --- |
| Shared lesson description, summary or materials | Existing lesson in `teacher/authoring/lessons.json`; preserve UUID and inspect all references/overrides. |
| One meeting or section-specific content/materials | `Overrides` on selected rows of `teacher/authoring/schedule.csv`; change only requested fields. Materials overrides replace the whole list. |
| New lesson or reusable intentional variant | New UUID in `lessons.json`, compatible Grade/Term and explicit kind; repoint only intended assignments/catalog slots. |
| Reorder lessons between occupied meetings | Existing `reschedule.js move`; move complete assignments, including overrides. |
| Cancel and postpone | Existing `reschedule.js cancel`; inspect trailing Extra capacity first. |
| Undated base catalog | `lessons.json` catalog mapping and referenced definitions. Create a new lesson ID if a base-only edit would otherwise change dated consumers. |
| Calendar, class reference, tasks or seminar roster | Directly maintained active file identified in the reference; these are not generator outputs. |

Never directly edit `schedule-data.js`, `schedule-data-base.js`, `materials-data.js` or `materials-data-base.js`. Do not invent URLs, rerun migration as routine authoring, or rewrite `migration-baseline.json`. Use the existing Node workflow, not the obsolete browser authoring prototype.

## Apply the smallest correct change

- Separate meeting identity/metadata from its assignment (`Lesson ID` **and** `Overrides`). Use the existing CSV parser/writer for structured edits so JSON quoting survives. Assigning a different lesson from scratch resets overrides to `{}` unless specific overrides are intended.
- Preserve stable IDs, grade/term compatibility, unique assignments within each section/term, complete material lists, intentional empty lists and historical variants. `Materials: []` is valid; missing Materials or an unknown lesson is an error. Extra lessons have explicit `kind: extra`, Description `Extra Class`, and no assignment overrides.
- Reorder using `node teacher/authoring/reschedule.js move GRADE SECTION FROM_DATE TO_DATE`. Endpoints must be assigned meetings in the same section and term; intervening assignments rotate. Canceled meetings, dates, displayed class numbers and other meeting metadata stay fixed.
- Cancel/postpone using `node teacher/authoring/reschedule.js cancel GRADE SECTION DATE "Reason"`. CLI dates are ISO `YYYY-MM-DD`. It skips cancellations, shifts complete assignments within the term and consumes the first slot in the trailing run of Extra lessons. Insufficient capacity fails without writes; do not cross terms, discard lessons or manufacture capacity. Canceling Extra consumes itself. Repeated cancellation does not shift again or update the reason; correct cancellation wording separately.
- Reschedule commands already validate and regenerate all four outputs. Review their source and artifact diffs before further changes.
- Keep regular Grade 10 and seminar lessons/catalogs distinct. Dated seminar Grade is numeric `10`, Section `Seminar`; base catalog Grade is string `10S`. Class detail never falls back to the undated catalog.
- For calendar changes, inspect `calendar-validation.js` and affected consumers. Explicitly reconcile requested CSV coverage, metadata and assignments before generation: editing the calendar does **not** rebuild `schedule.csv`. Identify any required authoring-tool or static-page changes beyond the requested data scope.
- Preserve teacher-context navigation and conditional roster loading; never make the roster unconditional to simplify an update or preview.

## Validate and report

Capture a pre-edit baseline for affected checks. For generated lesson/meeting/catalog data, run:

```powershell
node teacher/authoring/generate-schedule-data.js
node teacher/authoring/generate-schedule-data.js --check
node teacher/authoring/validate-materials-data.js
node --test teacher/authoring/tests/*.test.js
```

These commands work in PowerShell with tested Node 24; the README requires Node 18+. Recheck Node/glob support locally. If native glob expansion fails, pass explicit test filenames or an array from `Get-ChildItem teacher/authoring/tests -Filter *.test.js -File`. Check each command's exit code independently. See [validation and preview](references/data-flow.md#validation-and-preview) for targeted tests and baseline limitations.

Compare meaningful before/after relationships: effective content and full materials, schedule/materials joins, changed consumers, unchanged meeting metadata for rescheduling, intended assignment order/capacity, and unaffected sections/terms/catalog slots. Review all four artifacts, even when some remain byte-identical; deliver sources and generated changes together.

For direct data edits use relevant consumer checks/tests; regenerate lesson artifacts only when calendar constraints or authoring-source changes require it. Inspect representative rendered views for visible changes, including real public/teacher navigation when relevant. Check cards, links, empty states, hidden past rows and conditional roster network loading as applicable. Report unavailable browser checks explicitly.

Classify failures as new regressions, pre-existing issues or demonstrably obsolete historical assertions. Never weaken validation to obtain a pass. Preserve migration audit evidence. When intentional changes invalidate frozen assertions, explain the mismatch and use request-specific expectations plus preservation checks for unaffected records. Updating tests needs justified scope, not blind hash replacement.

Finish with changed paths, affected consumers, validation results and unresolved limitations or required scope decisions.
