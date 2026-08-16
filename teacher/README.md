# Teacher Directory Reference

## Purpose and scope

`teacher/` is the self-contained home of the teacher-facing timetable and its
supporting academic-calendar, class-detail, presentation, authoring, and results
normalization tools. Its main browser entry points are `schedule.html` (the
standard weekly view), `schedule-teacher.html` (the teacher variant),
`class_view.html` (a projector/current-period view), and the pages under
`pages/`. The directory also retains schedule source/history, an experimental
browser authoring tool, and a dated set of assessment workbooks plus a command
line normalizer.

This document describes **only files in `teacher/`**. Several pages deliberately
load styles, scripts, or links from elsewhere in the site; those are identified
only where they are direct dependencies. Paths in this document are relative to
`teacher/` unless shown otherwise.

## Current directory structure

```text
teacher/
├── README.md
├── schedule.html
├── schedule-teacher.html
├── class_view.html
├── assets/
│   ├── css/
│   │   ├── class-view.css
│   │   ├── general_calendar.css
│   │   └── principal-schedule.css
│   ├── html/
│   │   └── schedule_prototype_generated.html
│   └── js/
│       ├── class-data.js
│       ├── class-page.js
│       ├── class-view.js
│       ├── full-schedule-page.js
│       ├── full-schedule-today.js
│       ├── principal-schedule.js
│       ├── render-weekly-schedule-table.js
│       ├── schedule-data - 2025-2026.js
│       ├── schedule-data-base.js
│       ├── schedule-data.js
│       ├── schedule-renderer.js
│       ├── schedule-teacher.js
│       ├── schedule-today.js
│       ├── theme-toggle.js
│       └── year-calendar-data.js
├── authoring/
│   ├── generate-schedule-data.js
│   └── schedule.csv
├── pages/
│   ├── class.html
│   ├── full_schedule.html
│   ├── general_calendar.html
│   ├── magis.html
│   ├── seminarios.html
│   ├── sum_symbol.html
│   └── class_schedules/
│       ├── 10A.html  10B.html  10C.html  10D.html  10E.html
│       └── 11A.html  11B.html  11C.html  11D.html  11E.html
└── tools/
    ├── schedule_authoring_tool.html
    └── 2026-02-19-results/
        ├── README.md
        ├── results.py
        ├── 10A.xls  10B.xls  10C.xls  10D.xls  10E.xls
        └── 11A.xls  11B.xls  11C.xls  11D.xls  11E.xls
```

## Published pages and navigation

### Weekly schedules: `schedule.html` and `schedule-teacher.html`

These two pages contain their six-cycle-day timetable directly in HTML. Each
table row is a timed activity; class cells link to class pages, Seminarios, or
Magis. Both pages provide links to Class View, Calendar View, and a collapsible
grid of Grade 10 and Grade 11 sections. The teacher variant additionally exposes
a Full Schedule card, a Magis card, and an external weekly document link.

Both pages load the site-wide `../assets/css/schedule.css` (outside this
directory), then `assets/css/principal-schedule.css`,
`assets/js/year-calendar-data.js`, `assets/js/schedule-teacher.js`, and
`assets/js/theme-toggle.js`. `schedule-teacher.js`:

- expands/collapses the class-card panel;
- assigns cycle-day numbers to the table columns, including cells affected by
  row/column spans;
- asks `window.academicCalendar` for today's cycle day and highlights that
  column;
- draws and periodically updates the current-time line within a timetable row;
- rewrites every class-card wrapper URL to
  `pages/class.html?grade=…&section=…&mode=teacher&origin=schedule-teacher`.

That last behavior is the implementation currently loaded by **both** weekly
pages, so even wrapper links originating in `schedule.html` become teacher-mode
links whose back button returns to `schedule-teacher.html`. This differs from
the richer public/teacher branching implemented in the currently unused
`principal-schedule.js` described below.

### Projector view: `class_view.html`

Class View is not a section-specific class record. It is a fullscreen-friendly
display of the current timed block in either weekly schedule. The `origin`
query parameter selects `schedule.html` or `schedule-teacher.html`; the chosen
page is loaded into a hidden iframe, and `assets/js/class-view.js` reads the
rendered timetable rows for the calendar's current cycle day. It displays the
current activity, time remaining, next activity, or an appropriate no-schedule
state. It also provides a live clock, progress graphic, Fullscreen API control,
and an independent countdown timer with an optional Web Audio alarm.
`assets/css/class-view.css` supplies the projector, progress, dialog, responsive,
and dark-theme presentation. `year-calendar-data.js` supplies the cycle day and
`theme-toggle.js` supplies persistent dark mode.

### Class detail page: `pages/class.html`

This is the real implementation behind all ten class schedules. Its inline
bootstrap reads `grade`, `section`, `mode`, and `origin` query parameters (with
a legacy filename fallback), then places them in `#class-page` data attributes.
The scripts must remain in their present dependency order:

1. `class-data.js` defines `window.CLASS_STUDENT_LISTS` and
   `window.CLASS_NOTES`.
2. `class-page.js` builds breadcrumbs, title, notes/student-list content, the
   class calendar table, and theme control. Teacher mode may expose a configured
   PDF student-list link.
3. `schedule-data.js` defines `window.SCHEDULE_DATA`.
4. `schedule-renderer.js` filters that data by grade/section, chooses public
   `Material` or teacher-only `Material teacher`, renders rows, groups older
   dates behind an expandable control, and emits `class-schedule-rendered`.
5. `schedule-today.js` highlights today's row or inserts a Today divider.
6. `theme-toggle.js` restores and controls dark mode.

Additional inline code formats displayed dates and augments the past-date
control with a numeric setting (default: the two most recent past dates).
The page loads the shared `../../assets/css/schedule.css`, which is outside
`teacher/`.

### Legacy class wrappers: `pages/class_schedules/`

`10A.html` through `10E.html` and `11A.html` through `11E.html` are minimal
compatibility/redirect pages. Each offers a normal link and immediately uses
`location.replace` to open `../class.html` with its fixed grade and section.
The weekly schedule initially points to these stable URLs, after which its
JavaScript may rewrite those links directly to `class.html`. Their only style
reference is the external site stylesheet `../../../assets/css/schedule.css`.

### Combined view: `pages/full_schedule.html`

Full Schedule combines every class in `window.SCHEDULE_DATA` into one table.
Its initial inline script creates `window.fullScheduleDateFocus`, initialized
from a valid `?date=YYYY-MM-DD` or today's local date, and keeps an explicitly
selected date in the URL. It then loads calendar and class globals, the class
page helper, schedule data/rendering utilities, the full-schedule controller,
today-marker controllers, and theme support.

`full-schedule-page.js` flattens/sorts the class records, builds the full table,
supports a date picker, collapses older dates, dispatches the shared
`class-schedule-rendered` event, and scrolls to an explicitly focused date.
`full-schedule-today.js` uses the focus date (not necessarily real today) to
highlight all matching rows or insert a divider. Generic
`schedule-today.js` intentionally detects and skips this page. The HTML's final
inline controller adds the configurable count of visible past dates and date
formatting. Breadcrumbs return to `schedule-teacher.html` only when
`?origin=schedule-teacher`; otherwise they return to `schedule.html`.

The page references the site-wide `../../assets/css/schedule.css`, outside
`teacher/`.

### Academic calendar: `pages/general_calendar.html`

This page renders the August 2026–June 2027 academic year entirely from
`year-calendar-data.js`. Its inline application creates month grids with
weekdays, cycle days/numbers, terms, holidays, and today's date; offers From/To
date filters; and provides a collapsible filter panel. Filter values, filter
visibility, and user-selected legend colors are persisted in `localStorage`.
`assets/css/general_calendar.css` provides the grid, term/holiday/today states,
filters, legend, responsive layout, and dark theme. `theme-toggle.js` adds the
shared theme control. The inline origin map currently assigns
`../../schedule-teacher.html` for `?origin=schedule-teacher` and
`../../schedule.html` otherwise. From `teacher/pages/`, those paths resolve
outside `teacher/`, unlike the initial `/teacher/schedule.html` link in the
markup; this is a visible path inconsistency, not a connection to another
teacher page.

### Magis: `pages/magis.html`

Magis is a resource page reached from Magis timetable cells and from the teacher
page's card grid. It contains external SharePoint teacher/student resources, a
printing portal, and four YouTube resource cards. Two report/schedule links are
hidden unless the URL contains `?access=teacher`; inline JavaScript applies that
access state. The current back link always targets `schedule-teacher.html`.
Inline CSS handles the video-card specialization, while the page also loads the
external site-wide `../../assets/css/schedule.css` and local
`theme-toggle.js`.

### Seminarios: `pages/seminarios.html`

Seminarios is a placeholder resource page linked from the “Seminarios - 431”
weekly block. Its Resources grid is currently empty. Inline JavaScript uses
`?origin=schedule-teacher` to choose the teacher schedule as the back target and
otherwise uses `schedule.html`; `theme-toggle.js` handles dark mode. Its layout
comes from external `../../assets/css/schedule.css`.

### Summation lesson: `pages/sum_symbol.html`

This standalone Grade 11 statistics lesson explains summation notation through
a table of contents, progressive examples, a standard-deviation bridge, and
more complex examples. Its internal fragment links drive navigation within the
long page. It directly depends on site-wide CSS (`../../assets/css/base.css`,
`components.css`, and `schedule.css`) and `../../assets/js/collapsible.js`, all
outside `teacher/`, plus the external MathJax 3 CDN for mathematical notation.
Its Back link also targets a Grade 11 page outside `teacher/`. No page inside
`teacher/` currently links to this lesson.

### Generated schedule prototype: `assets/html/schedule_prototype_generated.html`

This retained prototype loads `../js/schedule-data.js`, reports record counts,
and renders a compact table from `window.SCHEDULE_DATA` using inline CSS and
JavaScript. It has no navigation connection from another tracked teacher page;
it is a diagnostic/generated-artifact view rather than a main entry point.

## Shared CSS and JavaScript

### CSS in `assets/css/`

- `principal-schedule.css` styles the weekly timetable's collapsible class grid,
  class/activity colors, active cycle-day column, current-time line, responsive
  layout, and dark mode. It is loaded by both weekly HTML files.
- `class-view.css` is dedicated to `class_view.html`: projector layout, progress
  display, timer dialog/alarm, fullscreen treatment, and light/dark palettes.
- `general_calendar.css` is dedicated to `pages/general_calendar.html`: yearly
  month cards, legend and color controls, filters, term/holiday/today markings,
  responsive rules, and dark mode.

The schedule/class/Magis/Seminarios/full-schedule pages also rely on the shared
site stylesheet `assets/css/schedule.css` located one level **outside**
`teacher/`; it is not part of this directory.

### Active JavaScript in `assets/js/`

- `year-calendar-data.js` is the calendar source and lookup library. It stores
  2026 and 2027 month matrices, cycle-day matrices, holiday lists, and the
  `2026-2027` academic-year/term configuration. It validates/normalizes dates,
  generates cycle numbers that restart each term, and exposes lookup functions
  as both `window.academicCalendar` and CommonJS exports. Browser schedule and
  calendar views use the global; the Node generator uses the exports.
- `theme-toggle.js` shares one `scheduleTeacherTheme` `localStorage` setting
  among pages containing `#dark-mode-toggle`, applying `body.dark-theme`.
- `schedule-teacher.js` enhances both current weekly pages as detailed above.
- `class-data.js` holds per-class student-list metadata and class notes. It is
  consumed by `class-page.js` and loaded by the browser authoring prototype to
  derive allowed class IDs.
- `class-page.js`, `schedule-renderer.js`, and `schedule-today.js` cooperate on
  `pages/class.html`. The renderer's custom event is the handoff to today
  markers and the HTML's inline past-date controls.
- `full-schedule-page.js` and `full-schedule-today.js` specialize that same data
  and event convention for `pages/full_schedule.html`.
- `class-view.js` combines the calendar API with a hidden weekly-page iframe for
  the live projector display.

### Retained but not loaded by current HTML

- `principal-schedule.js` is a more extensive weekly controller: it distinguishes
  public/teacher modes, rewrites class/Magis/calendar links, and implements
  weekday selection, weekday-only/plain-style/week-summary controls, schedule
  lifecycle events, and responsive/current-time behavior. No HTML file in
  `teacher/` currently includes it. One of its calendar rewrite targets,
  `assets/html/general_calendar.html`, also does not exist (the actual page is
  `pages/general_calendar.html`).
- `render-weekly-schedule-table.js` contains weekly timetable markup and exposes
  `window.renderWeeklyScheduleTable(target)`. No current HTML includes or calls
  it because both weekly pages embed their tables directly.

These files document an alternate/dormant rendering path; they should not be
mistaken for dependencies of the current weekly pages.

## Schedule and calendar data

### Canonical runtime schedule

`authoring/schedule.csv` is the editable source for the current 2026–2027
class-meeting records. It contains display-shaped columns for grade, section,
class slot, date, term, weekday, cycle day, description, public material,
teacher material, and summary.

`authoring/generate-schedule-data.js` is the canonical Node generator. It parses
the CSV, imports `year-calendar-data.js`, validates supported classes, dates,
terms, weekdays, cycle days/numbers, required meeting coverage, duplicate keys,
placeholder content, and ordering, then writes
`assets/js/schedule-data.js`. A validation failure occurs before the existing
artifact is replaced. Run it from the repository root with:

```bash
node teacher/authoring/generate-schedule-data.js
```

`assets/js/schedule-data.js` is marked auto-generated and assigns the current
records to `window.SCHEDULE_DATA`; do not edit it by hand. It is consumed by
class pages, Full Schedule, and the generated prototype.

### Retained schedule datasets

- `assets/js/schedule-data - 2025-2026.js` is an auto-generated historical
  2025–2026 `window.SCHEDULE_DATA` snapshot. No current HTML loads it.
- `assets/js/schedule-data-base.js` is an auto-generated, undated base organized
  only by grade/class slot/term and lacks section/date fields. It uses the same
  global name but has no current HTML consumer. Loading it alongside the
  canonical artifact would overwrite the same global.

### Calendar data

`assets/js/year-calendar-data.js` is both runtime data and executable lookup
logic. It is shared by the weekly highlight, Class View, General Calendar, Full
Schedule shell, and the generator. The schedule CSV is therefore validated
against the same academic calendar used in the browser.

## Authoring and utility tools

### Browser schedule authoring prototype

`tools/schedule_authoring_tool.html` is a browser-only experiment with inline
styles and logic. It loads `class-data.js`, accepts uploaded/pasted schedule CSV
and an optional slots CSV, validates a normalized schema, previews/downloads a
flat `window.SCHEDULE_DATA` artifact or normalized `window.SCHEDULE_NORM` plus
adapter, and tries to fetch `authoring/schedule.csv` and
`authoring/slots.csv` as defaults.

The tracked `schedule.csv` does not have the normalized columns this prototype
requires, and `authoring/slots.csv` does not exist. The page explicitly reports
this known schema block. Consequently its downloads are **not** the canonical
runtime generation path and must not replace `schedule-data.js`; use the Node
generator above.

### Assessment-results normalizer

`tools/2026-02-19-results/` is a dated, independent data-processing utility:

- `results.py` discovers legacy `.xls`/`.xlsx` inputs, reads irregular sheets,
  detects their structural columns, extracts repeating four-row student
  records, normalizes C1–C10 and yes/no fields, and prints cleaned tables and
  summaries. It can process a chosen file (default `10A.xls`) or all adjacent
  workbooks. It requires Python 3 and `pandas`, plus an Excel engine such as
  `xlrd`; `tabulate` is optional.
- `README.md` documents the utility's commands, environment, and privacy rules.
- `10A.xls`–`10E.xls` and `11A.xls`–`11E.xls` are the ten adjacent source
  workbooks. They may contain student-level information; do not expose derived
  output or relocate/delete them without authorization.

This results tool does not feed any teacher HTML page or schedule dataset.

## Runtime conventions and maintenance notes

- Serve the repository over HTTP (for example,
  `python3 -m http.server 8000`) rather than opening files directly when testing
  iframe/fetch behavior.
- Preserve script order wherever a consumer expects globals such as
  `window.academicCalendar`, `window.CLASS_STUDENT_LISTS`,
  `window.CLASS_NOTES`, or `window.SCHEDULE_DATA`.
- Do not manually edit files marked `AUTO-GENERATED FILE`; update their source
  and use the relevant generator.
- Query parameters are part of navigation state: `origin` controls return links,
  `mode=teacher` controls teacher-only class material/student links,
  `access=teacher` reveals teacher-only Magis resources, and Full Schedule's
  `date` controls its focus marker.

## File Connection Trees

The following trees show direct loading, data, event, iframe, and navigation
relationships rather than repeating the filesystem hierarchy.

### Weekly schedule and live Class View

```text
schedule.html                         schedule-teacher.html
├── [CSS] assets/css/principal-schedule.css
├── [CSS, external to teacher/] ../assets/css/schedule.css
├── [data/API] assets/js/year-calendar-data.js
├── [controller] assets/js/schedule-teacher.js
├── [theme] assets/js/theme-toggle.js
├── [nav] class_view.html?origin=schedule|schedule-teacher
│   ├── assets/css/class-view.css
│   ├── assets/js/year-calendar-data.js
│   ├── assets/js/class-view.js
│   │   └── [hidden iframe/read table] schedule.html OR schedule-teacher.html
│   └── assets/js/theme-toggle.js
├── [nav] pages/general_calendar.html
├── [nav] pages/class_schedules/{10A..10E,11A..11E}.html
│   └── [redirect] pages/class.html?grade=…&section=…
├── [nav] pages/seminarios.html
└── [nav, teacher page/card and timetable links] pages/magis.html

schedule-teacher.html only
├── [nav] pages/full_schedule.html?origin=schedule-teacher
└── [nav] external weekly document
```

### Class and full schedules

```text
pages/class_schedules/{10A..10E,11A..11E}.html
└── pages/class.html?grade=…&section=…
    ├── [CSS, external to teacher/] ../../assets/css/schedule.css
    ├── assets/js/class-data.js
    │   ├── window.CLASS_STUDENT_LISTS
    │   └── window.CLASS_NOTES
    ├── assets/js/class-page.js ── builds .class-schedule-table
    ├── assets/js/schedule-data.js ── window.SCHEDULE_DATA
    ├── assets/js/schedule-renderer.js
    │   └── emits class-schedule-rendered
    ├── assets/js/schedule-today.js ── listens for render event
    ├── [inline] date formatting + visible-past-date control
    ├── assets/js/theme-toggle.js
    └── [nav by origin] schedule.html OR schedule-teacher.html

pages/full_schedule.html
├── [CSS, external to teacher/] ../../assets/css/schedule.css
├── [inline] window.fullScheduleDateFocus (?date=…)
├── assets/js/year-calendar-data.js
├── assets/js/class-data.js
├── assets/js/class-page.js
├── assets/js/schedule-data.js ── window.SCHEDULE_DATA
├── assets/js/schedule-renderer.js
├── assets/js/schedule-today.js ── detects full page and yields
├── assets/js/full-schedule-page.js ── combines records + emits render event
├── assets/js/full-schedule-today.js ── focused-date marker
├── [inline] date formatting + visible-past-date control
├── assets/js/theme-toggle.js
└── [nav by origin] schedule.html OR schedule-teacher.html
```

### Calendar and generated schedule data

```text
authoring/schedule.csv
└── authoring/generate-schedule-data.js (Node/CommonJS)
    ├── imports assets/js/year-calendar-data.js for validation
    └── generates assets/js/schedule-data.js
        ├── pages/class.html
        ├── pages/full_schedule.html
        └── assets/html/schedule_prototype_generated.html

assets/js/year-calendar-data.js
├── schedule.html + schedule-teacher.html (active cycle column)
├── class_view.html (current cycle day)
├── pages/general_calendar.html
│   ├── assets/css/general_calendar.css
│   ├── [inline] month/legend/filter renderer + localStorage
│   ├── assets/js/theme-toggle.js
│   └── [origin rewrite, currently resolves outside teacher/] ../../schedule.html
│       OR ../../schedule-teacher.html
├── pages/full_schedule.html
└── authoring/generate-schedule-data.js

assets/js/schedule-data - 2025-2026.js ── [retained; no HTML consumer]
assets/js/schedule-data-base.js          ── [retained; no HTML consumer]
```

### Teacher resources, prototypes, and independent tools

```text
schedule.html / schedule-teacher.html
├── pages/seminarios.html
│   ├── [CSS, external to teacher/] ../../assets/css/schedule.css
│   ├── assets/js/theme-toggle.js
│   └── [nav by origin] weekly schedule
└── pages/magis.html
    ├── [CSS, external to teacher/] ../../assets/css/schedule.css
    ├── [inline] access=teacher visibility logic
    ├── assets/js/theme-toggle.js
    ├── [external] SharePoint + printing resources
    ├── [external] YouTube resources
    └── [nav] schedule-teacher.html

pages/sum_symbol.html
├── [external to teacher/] shared CSS + collapsible.js
├── [external CDN] MathJax 3
└── [external to teacher/] Grade 11 return page

tools/schedule_authoring_tool.html
├── assets/js/class-data.js ── allowed class IDs
├── [fetch] authoring/schedule.csv
├── [attempted fetch; absent] authoring/slots.csv
└── [browser downloads] experimental flat/normalized/adapter JS

tools/2026-02-19-results/results.py
├── tools/2026-02-19-results/{10A..10E,11A..11E}.xls
└── tools/2026-02-19-results/README.md

assets/js/principal-schedule.js          ── [dormant; no HTML loader]
assets/js/render-weekly-schedule-table.js ── [dormant; no HTML loader]
```
