# Linked lesson authoring

Run these commands from the repository root with Node.js 18 or newer.

## Authoritative files

- `teacher/authoring/schedule.csv` defines dated meetings and their lesson assignments.
  A meeting owns `Grade`, `Section`, `Term`, `Date`, `Weekday`, cycle `Day`, displayed
  `Class #`, and `Status`. Those identifying fields do not move during postponement.
- `teacher/authoring/lessons.json` defines lessons and the undated catalog. Every
  lesson has a permanent opaque UUID, grade/term compatibility, an explicit `kind`
  (`instruction` or `extra`), Description, Summary, legacy Material / Material teacher
  values, and the **complete** Materials list. Keep its ID when editing content.
  Allocate a new UUID for a genuinely new lesson (`node -e "console.log(require('node:crypto').randomUUID())"`).
  The `catalog` array maps undated grade/term/displayed class numbers to lesson IDs.
  Catalog numbers are presentation metadata, never runtime lesson identity.
  Grade 10 Seminar has a separate base catalog with `Grade: "10S"`: 9, 10,
  and 9 sequential classes in Terms 1, 2, and 3. Its lessons retain numeric
  `Grade: 10`, as do dated meetings (`Section: "Seminar"`). Do not share edited
  seminar lessons with regular classes. The class page filters numeric dated
  records by grade and section; it does not load or fall back to the base catalog.
  Base materials accept `"10S"` only in base mode, and display it as its own group.
- CSV `Lesson ID` plus `Overrides` form one assignment. Overrides are a JSON object
  with optional Description, Summary, Material, Material teacher, or Materials fields.
  Materials overrides replace the whole list. Use them for explicit section-specific
  differences; an override wins over the lesson default. Shared historical variants
  have their own reusable lesson definition instead of repeated override copies.

`Materials: []` is an intentional, valid definition, including for assessments.
A missing Materials property or missing/unknown assigned lesson ID is an error.
There is no fallback from a missing lesson to an empty list or a catalog ordinal.
Each assigned lesson may occur only once within a section and term. A new intentional
repeat needs its own lesson ID. Lesson references cannot cross grades or terms.

Meeting statuses are `scheduled` (requires an assignment), `canceled` (no assignment),
and `unassigned` (only outside the registered terms; no assignment). `Reason` is the
optional suffix after `No Class`, including its punctuation. The cancel command writes
` - reason`. `Canceled summary` preserves original historical cancellation labels;
leave it empty for new cancellations to display `No Class`. Neither field is lesson
content. Cancellation rows cannot carry overrides or materials.

## Generate and check

```sh
node teacher/authoring/generate-schedule-data.js
node teacher/authoring/generate-schedule-data.js --check
node teacher/authoring/validate-materials-data.js
node --test teacher/authoring/tests/*.test.js
```

Generation resolves every dated schedule/materials pair from the same assignment.
It also resolves both base catalogs from the same lesson definitions. All four
outputs are validated **before any file is replaced**, including calendar coverage,
identity, grade/term compatibility, unique assignments, overrides and material metadata.
Files are staged together, with rollback on a reported replacement error. `--check`
and the materials validator are read-only and reject stale output. Generation is
deterministic. Commit the authoritative files and regenerated artifacts together.

The generated files under `teacher/assets/js/databases/` are `schedule-data.js`,
`materials-data.js`, `schedule-data-base.js`, and `materials-data-base.js`. Do not
edit those files. Frontend globals and schemas are unchanged: dated schedules use
`YYYY / MM / DD`; dated materials use ISO dates and uppercase sections. Base schedule
still exposes `window.SCHEDULE_DATA` and must not be loaded beside the dated schedule.
Dated materials are emitted for every in-term meeting, including canceled meetings
with `Materials: []`. The 72 meetings outside terms retain schedule placeholders and
have no dated material records, preserving existing frontend behavior.

Material metadata remains Acronym (1–4 characters), Name, Hyperlink (absolute HTTP/S),
and Category (`slides`, `classroom-activities`, `practice-activities`, `extra-resources`,
`mock-practices`). Preserve existing URLs; the validator checks URL syntax, not live
resource availability. Existing Term 2 placeholder URLs are retained. No resources
are invented by migration or generation.

Regular sections continue their two-class sequence strictly after May 11, 2027,
from each section's last label (including `6-1` continuing to `6-2`). Calendar
validation enforces this continuation without changing the calendar's cycle Day,
registered terms, seminar numbering, or meeting coverage. These out-of-term
meetings remain unassigned. Existing dates end at `9-2` for 10B, 10D, 11B and
11D, and at `10-1` for the other regular sections; no section reaches `10-2`.

Grade 10 Seminar Term 2 materials follow the links and labels in
`seminars/src/G10_T2.html`, resolved against the established GitHub Pages root.
There are no linked dedicated assessment documents: class 5 uses the C3–C4
guide and `#first-learning-evidence`; class 7 uses the C5–C6 guide; class 10
uses `#introduction` (the cumulative LaTeX document instructions),
`#second-learning-evidence`, and the C5–C10 guides. Term 1 and Term 3 base
entries copy available dated seminar content, including historical placeholders
and the canceled meeting. Term 3 base classes 7–9 have no assigned dated content;
they retain `-` fields and empty materials without assigning the out-of-term dates.

## Cancel a meeting and postpone its lesson

```sh
node teacher/authoring/reschedule.js cancel 11 C 2026-11-17 "School event"
```

Use the actual date of the lost meeting. The command keeps its identifying fields,
sets status to canceled and removes its assignment. Its generated content becomes
`No Class - School event`, with Summary `No Class` and Materials `[]`. It moves the
complete assignment (ID **and overrides**) into the next available meeting, cascading
subsequent assignments within that section and term and skipping existing canceled
meetings. It consumes the first slot in the trailing run of lessons explicitly marked
`kind: extra`; later Extra slots stay available. Instructional and assessment lessons
remain in order, including assessments with empty materials.

If no trailing Extra slot exists, the operation fails without changing the CSV or
any generated file. It never crosses a term boundary. Canceling an Extra meeting
consumes that slot itself. Canceling the same meeting again is a no-op with no second
shift, even if a different reason is supplied. Edit its Reason separately to correct
wording. The command validates and regenerates all four datasets in the same operation.

The historical corrections below are **already applied**. Running either command
again safely leaves all assignments unchanged:

```sh
node teacher/authoring/reschedule.js cancel 11 A 2026-11-18
node teacher/authoring/reschedule.js cancel 11 B 2026-11-23
```

## Move an individual lesson

```sh
node teacher/authoring/reschedule.js move 11 B 2026-11-30 2027-01-14
```

This moves the November 30 assignment into January 14 and moves intervening
assignments one meeting earlier, keeping all lessons and their overrides. Moving
backward shifts intervening assignments later. Both endpoints must be assigned
meetings in the same section and term. Dates, displayed class numbers and canceled
meetings stay fixed. This is an explicit reorder; cancellation is the operation that
preserves the original instructional order.

For example, before that move, November 30 has C3 plus the C1C2 mock materials, and
January 14 has C4 materials. Afterwards, January 14 has **both** the C3 description /
summary and its five C3/mock material cards. The empty-material C1C2 assessment moves
to November 30, and C4 moves to December 1. No separate materials edit is needed.
To edit assignments directly, move the pair `Lesson ID` + `Overrides` together; when
assigning a different lesson from scratch, reset Overrides to `{}` unless explicit
section-specific overrides are intended. Then run the generator.

## Migration and preserved history

`migrate-lessons.js` is a one-time importer for the reviewed legacy CSV and four
runtime arrays. It verifies CSV/runtime agreement and the two already synchronized
Grade 11 cancellations before writing. It joins every material list by its original
dated identity, never regenerating dated materials by meeting ordinal. The import
uses a frozen legacy catalog crosswalk, explicitly offset for the two Grade 11
postponements; historical differences become shared variant lessons or assignment
overrides. Runtime generation never infers identity from description text, row
position, calendar position or displayed Class #.

The migration preserved all 594 schedule records exactly, all 112 base schedule and
material records, and all dated materials except stale lists on 15 older No Class
meetings. Those lists are recorded in full in `migration-baseline.json`; no additional
historical cascade was applied. All other historical and section-specific differences
remain explicit, including pre-existing placeholder content. Both corrected Grade 11
sections retain every instructional/assessment lesson and two trailing Extra slots.

`migration-baseline.json` records hashes before/after migration, removed stale links,
and the frozen meeting-to-lesson crosswalk. It is audit evidence, not an authoring
source. Do not update it for routine future scheduling; migration regression hashes
intentionally describe this import baseline. After intentional future authoring changes,
review and replace the baseline-specific assertions with the appropriate new expected
behavior. Existing frontend card tests and assignment invariant tests remain applicable.
The old 2025–2026 snapshot and unrelated working-tree changes are untouched.

```sh
node teacher/authoring/migrate-lessons.js
```

On an already migrated repository this only validates the source and reports that no
changes are needed. A legacy source that has not completed the two reviewed corrections
is rejected for review; this importer does not guess whether to shift it. The older
browser authoring prototype does not support this schema; use the Node commands.

For preview, serve the repository root and open
`/teacher/pages/materials.html?grade=11&section=B&date=2027-01-15` for the postponed
mock, or omit the query string for the base catalog.
