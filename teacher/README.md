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

## Schedule authoring workflow

`teacher/authoring/schedule.csv` is the source for the display-shaped runtime
records in `teacher/assets/js/schedule-data.js`. After editing the CSV, regenerate
and validate the JavaScript with:

```bash
node teacher/authoring/generate-schedule-data.js
```

The generator preserves the runtime field order and global name. It also uses
`year-calendar-data.js` to validate the complete Global Economics meeting
coverage, supported classes, cycle days and numbers, terms, weekdays, duplicate
keys, placeholder content, and grade/section/date ordering before writing the
artifact. A validation failure leaves the existing JavaScript untouched.

The browser authoring tool remains a **prototype** whose normalized schema and
optional slot-file workflow differ from this canonical generator. Do not use its
generated output to overwrite `teacher/assets/js/schedule-data.js`.

The second retained data file, `schedule-data-base.js`, has a different, undated
field shape and no tracked HTML consumer. Its ownership and retirement status
remain unconfirmed.

Browser smoke testing can be run with:

```bash
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
