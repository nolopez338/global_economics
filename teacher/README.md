# Teacher Resources

## Published entry points and runtime data

- `teacher/schedule.html` and `teacher/schedule-teacher.html` render the weekly
  timetable shell.
- `teacher/pages/full_schedule.html` and the class-specific wrappers below
  `teacher/pages/class_schedules/` use `teacher/pages/class.html`.
- Full and class views load `window.CLASS_STUDENT_LISTS` and
  `window.CLASS_NOTES` from `teacher/assets/js/class-data.js`, then load
  `window.SCHEDULE_DATA` from `teacher/assets/js/schedule-data.js` before the
  renderer/controller scripts execute.
- `teacher/pages/schedule_prototype_generated.html` now reads the same retained
  runtime `window.SCHEDULE_DATA` artifact. It is not linked from the main
  schedule, so its publication/support status remains unconfirmed.
- `teacher/assets/js/schedule-data-base.js` also declares
  `window.SCHEDULE_DATA`, but no tracked HTML page loads it. Its ownership and
  intended generation contract remain unconfirmed; it has not been removed.

Do not change the global names or script order without checking every consumer.
Files that say `AUTO-GENERATED FILE` must not be edited manually.

## Schedule authoring status

`teacher/authoring/schedule.csv` is labelled as the source by the headers in
both retained runtime data files. The current checkout does **not**, however,
contain a reproducible source-to-runtime generation contract:

- the CSV has 115 records and the primary runtime artifact has 383 records;
- the current CSV uses the nine display columns beginning with `Grade`, whereas
  `teacher/tools/schedule_authoring_tool.html` requires normalized columns such
  as `class_id`, `date`, and `slot`;
- the authoring tool requests `teacher/authoring/slots.csv`, which is absent;
- the runtime artifact contains additional `Term` and `Material teacher`
  fields that the current browser generator does not emit; and
- the second retained data file has a different, undated field shape.

These differences are verified repository state, not an approved schema choice.
Consequently, the browser authoring tool is retained as a **prototype**, but its
default-load/generate workflow must not be used to overwrite
`teacher/assets/js/schedule-data.js`. No slot list, normalized schema, or adapter
has been invented in this change.

Resolving the workflow requires a maintainer to designate:

1. the authoritative current dataset;
2. the authoritative slot source;
3. whether normalized or display-shaped CSV fields are canonical;
4. whether `Term` and `Material teacher` must be authoring fields; and
5. the purpose or retirement status of `schedule-data-base.js`.

After those decisions, a generator must compare record count, keys, types,
classes, slots, dates/weekdays, collision keys, global name, values, and ordering
against the retained runtime before replacing it. Until then, validation is
limited to static references and browser smoke testing:

```bash
python3 tools/validate_local_references.py --self-test
python3 -m http.server 8000
```

Open the weekly, full, representative Grade 10/11 class pages, the prototype,
and `teacher/tools/schedule_authoring_tool.html`. The authoring tool's missing
slot/schema contract is a known blocked baseline issue even though all of its
static file references now resolve.

## Assessment-results normalizer

`teacher/tools/2026-02-19-results/results.py` normalizes irregular Excel exports
stored beside it. See its local README for dependencies and usage. The
workbooks may contain student-level information. Their provenance, retention,
and privacy authorization are not recorded, so neither the script nor workbooks
have been relocated.
