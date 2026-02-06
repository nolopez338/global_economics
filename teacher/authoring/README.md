# Schedule Authoring Prototype

## Canonical Source
- `teacher/authoring/schedule.csv` is the canonical authoring file for schedule entries.
- It was initially exported from `teacher/assets/js/schedule-data.js` and includes every current entry.

## Open the Browser Tool
1. Open `teacher/tools/schedule_authoring_tool.html` in a browser.
2. Click **Load default authoring CSVs** to load:
   - `teacher/authoring/schedule.csv`
   - `teacher/authoring/slots.csv`

## Validate
- Click **Validate**.
- Validation enforces:
  - required columns
  - date format `YYYY-MM-DD`
  - weekday whitelist (`Mon`..`Fri`)
  - weekday/date consistency and no weekend dates
  - class ID membership from `teacher/assets/js/class-data.js`
  - unique composite key (`class_id + date + slot`)
  - slot membership from `teacher/authoring/slots.csv`

## Generate Artifacts
- Click **Generate Flat** to build:
  - `window.SCHEDULE_DATA` artifact text
- Click **Generate Normalized + Adapter** to build:
  - `window.SCHEDULE_NORM` artifact text
  - adapter artifact that emits `window.SCHEDULE_DATA` from `window.SCHEDULE_NORM`
- Use the download buttons and save generated files under `teacher/assets/generated/`.

## Open Prototype Page
1. Ensure `teacher/assets/generated/schedule-flat.generated.js` exists.
2. Open `teacher/pages/schedule_prototype_generated.html`.
3. The page renders a minimal grouped-by-date schedule and marks today.
