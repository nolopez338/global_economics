# Prompt: Extract the Grade 10 and Grade 11 academic calendar

Review `teacher/assets/pdf/programador-ajustado-agenda-22026-2027.pdf` and create `teacher/grade10-grade11-academic-calendar-2026-2027.md` with all calendar information relevant to Grade 10 and Grade 11 students, their families, and teachers planning their classes.

Perform the review and write the output file; do not stop at a plan. Keep the source PDF unchanged. Write the report in Spanish, preserving the calendar's original event names and abbreviations.

## Source and review method

- Treat the PDF as the authoritative source. Review all 11 pages, covering August 2026 through June 2027, including past dates. Verify those boundaries against the actual document.
- Extract text as a search aid, then visually inspect every page. This is a calendar grid: text extraction order alone cannot establish which date an event belongs to.
- Read the month and year headings, weekday columns, numbered dates, school-cycle labels (`DÍA 1` through `DÍA 6`), and any legends or notes together. Distinguish the day of the month from the school-cycle day.
- Carefully verify events spanning multiple cells, weeks, or months. Determine their start and end dates from the visible grid or bars. Do not assume that a centered label applies to the entire week, or that a bar crossing a weekend schedules activity on that weekend.
- Cite the PDF page number, counted from 1, for every event and date boundary. Include a short original-text excerpt where helpful for ambiguous entries.
- Do not use existing JavaScript calendar data, external calendars, or general knowledge to fill gaps in the PDF. If comparison with another repository source is necessary, label it separately and retain the PDF's wording and dates.

## What to include

1. **Grade 10 events:** every explicit reference to Grade 10, décimo, 10°, 10º, or individual sections such as 10°A. Include ECC, FAS, IGCSE examinations and subjects, family activities, outings, retreats, assessments, and other events actually shown.
2. **Grade 11 events:** every explicit reference to Grade 11, undécimo, once, 11°, 11º, or individual sections such as 11°A. Include spiritual exercises, family activities, examinations, graduation activities, the proclamation of graduates, and other relevant events actually shown. Record whether applicability is explicit or inferred from the event wording.
3. **Shared academic milestones:** student entry, period starts and ends, academic cutoffs, academic tests, evaluation commissions, reports or family meetings, individual development plans and their tests, and closing activities affecting either grade.
4. **Schoolwide scheduling information:** holidays marked in the PDF, recesses, vacations, institutional development days, pedagogical days, and other stated changes that affect teaching or attendance. Also include schoolwide civic, cultural, religious, sports, student-government, and family events when they are presented as general events.
5. **Cycle-based events:** include events for cycles that the source explicitly maps to Grade 10 or Grade 11. If the PDF mentions `Ciclo IV`, `Ciclo V`, or another cycle without defining its grades, place potentially relevant entries in the uncertainty section; do not invent the mapping.

Exclude events explicitly restricted to other grades unless the source also establishes an effect on Grade 10 or Grade 11. Do not infer cancellation of classes, compulsory participation, all-day duration, or an event time merely because an event appears in the calendar. Preserve undefined abbreviations rather than inventing their expansions.

## Required Markdown structure

### 1. Source and scope

Identify the source with a relative Markdown link to the PDF, the academic year, months reviewed, page count, and any document date or revision information actually printed in it. Distinguish printed document dates from file metadata. Explain that general events are included for planning but attendance and class changes are asserted only where stated.

### 2. Academic periods and major date ranges

Provide a compact table of period boundaries, recesses, vacations, and major assessment or development-plan windows. Include start date, end date where stated, original label, affected grades or scope, and source pages. Mark missing or unclear boundaries explicitly.

### 3. Chronological event register

Create one complete register, grouped by month and sorted by date, with these columns:

| ID | Start date | End date | Event | Grade / section / scope | Applicability | School-cycle day | Time | Explicit scheduling effect / notes | PDF page(s) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |

- Use ISO dates (`YYYY-MM-DD`). For single-day events, use the same start and end date. For uncertain boundaries, state `Por confirmar` rather than assigning a guessed date.
- Use `Explícita`, `General`, or `Inferida; por confirmar` in the applicability column and explain any inference in the notes.
- Preserve the exact section when stated. Never turn an event for 10°A into an event for all of Grade 10.
- Record times only if printed; otherwise write `No indicada`. Use `No indicado` for absent school-cycle days. For ranges, record cycle days only when clearly attributable; do not generate an unsupported sequence.
- Give each distinct event a stable identifier such as `CAL-001`. Separate different events on the same date.
- Consolidate clearly continuous events into one range. Keep separate sessions or nonconsecutive occurrences in separate rows. If continuity is unclear, preserve the visible occurrences and flag the uncertainty.
- For general events, state `Ambos grados; evento general` as the scope without implying mandatory participation. For relevant teacher-only entries, identify that audience explicitly.

### 4. Grade-specific quick indexes

Provide separate Grade 10 and Grade 11 indexes listing the IDs, dates, and titles of their specific events. Reference the shared register for general schoolwide dates so those events are not duplicated throughout the report.

### 5. Uncertainties and items requiring confirmation

List ambiguous date spans, illegible text, undefined cycle mappings, unclear audiences, and apparent inconsistencies. For each item, cite its page and explain exactly what needs confirmation. Preserve conflicting source information rather than silently correcting it. If there are no unresolved items, say so only after completing the visual review.

### 6. Coverage check

Include a checklist or compact table showing every source page and month reviewed. State that explicit Grade 10 and Grade 11 references, section-specific entries, shared milestones, and schoolwide scheduling events were checked. Summarize event counts by applicability and unresolved-item counts using the completed register, counting each event ID once.

## Final verification and delivery

- Recheck every date and range against its calendar cell and month/year heading, especially multi-day bars and month transitions.
- Search the extracted text for grade variants and inspect the corresponding pages to catch references split across lines or embedded in ranges. Keyword searches supplement the full visual review; they do not replace it.
- Confirm that no other-grade-only events were promoted to shared events, no section labels were lost, and no unsupported cycle-to-grade mapping was introduced.
- Check chronological order, unique IDs, valid dates, source pages, index references, counts, and consistency between the summary and register.
- Save the completed Markdown report at the specified output path. In your final response, link to it and briefly state the number of recorded events and any unresolved ambiguities. Do not claim complete extraction if pages could not be read; identify the missing coverage explicitly.
