---
name: seminar-work-summary-term1
description: Generate a Spanish, source-cited LaTeX summary of Term 1 seminar groups from resultados_criterios.csv and submitted PDFs, without reassessing student work.
---

# Term 1 seminar work summary

When invoked, generate `book2026-2027/seminars/term_1/second_learning_evidence/seminars_summary.tex` from verified student submissions. Paths below are relative to the project root. Creating or editing this skill does not invoke the summary workflow. Do not reassess, grade, or modify the CSV or submissions.

## Discover sources and verify groups

- Read `book2026-2027/seminars/term_1/second_learning_evidence/resultados_criterios.csv` with a CSV parser that preserves quoted multiline fields (for example, Python `csv.DictReader` with `newline=''`); never split the file into lines as records.
- Identify students using `ESTUDIANTES`; extract every URL in `ENLACE_ACTIVIDAD`, including newline-separated URLs within one cell. Deduplicate links while preserving their associations with every roster row. `No` identifies a roster row, not a seminar group.
- Retrieve and read every distinct relevant PDF. Inspect tables, figures, and scanned pages as well as extracted text; render pages or use OCR where necessary. Record inaccessible sources and unreadable pages individually; do not treat failed extraction as absent student content.
- Establish group membership using both shared submission links and explicit membership statements in PDFs. Verify membership across related submissions; one overlapping student or link alone does not justify merging groups. Retain separately verified groups while recording unresolved relationships without guessing.
- Preserve group numbers explicitly stated in submissions. If none is available, assign an unused sequential summary number and label it `número asignado para este documento`. Report conflicting numbers without silently selecting one.
- Maintain a coverage/evidence ledger relating every CSV row to verified membership or an unresolved status, every distinct link to its retrieval/readability status, and each group claim to a PDF and page. Explicitly track ambiguous membership, numbering conflicts, inaccessible/unreadable sources, and students with no linked work. Do not silently omit any row.

## Interpret evidence

Read these guides solely to interpret the criteria:

- `book2026-2027/seminars/term_1/C5C6-Activity.tex`
- `book2026-2027/seminars/term_1/C7C8-Activity.tex`
- `book2026-2027/seminars/term_1/C9C10-Activity.tex`

All claims about completed work, problems, and solution ideas must come from the group's submitted PDFs. CSV Yes/No results and completion percentages are not evidence of what students wrote. Never convert assignment instructions into student work, infer a solution from a problem, or invent content. Preserve students' meaning and distinguish proposals from actions actually implemented.

## Write the document

Use Spanish unless the user requests another language. Give each verified group its own section with:

1. Its submission group number (or clearly labeled assigned number) and verified members, with membership source/page references.
2. Clickable links to all PDFs used for that group, labeled with readable filenames or titles.
3. Six labeled entries, **C5** through **C10**, each containing exactly one sentence summarizing the actual work completed for that criterion. Include source citations within the sentence; do not add separate explanatory sentences.
4. A **Problema abordado** subsection summarizing the group's identified problem.
5. An **Ideas de solución** subsection presenting at least two distinct ideas from the group's work when available.

Attach a source filename/title linked to its PDF and a page reference to every substantive criterion summary, problem statement, and solution idea. Use 1-based PDF page positions, explicitly distinguished from printed page labels if they differ. Unresolved or unverifiable claims must not receive fabricated citations.

Handle missing evidence explicitly:

- If a criterion has no identifiable evidence, its single sentence must state that; distinguish absence in readable work from inability to verify due to an inaccessible source or unreadable pages.
- If no problem is identified, say so with the same distinction.
- If only one solution idea is identifiable, present it and state that no second idea was identified. If none are identifiable, say so. Do not duplicate or artificially split an idea to reach two.
- If evidence is partial, limit claims to verified material and state which source limitations prevent fuller verification; never assert that inaccessible content is absent.

Include a clearly labeled **Casos pendientes y limitaciones** section accounting for unresolved membership, conflicting numbers, inaccessible PDFs, unreadable pages, and every student without linked work. If there are no unresolved cases, say so. Continue with verified groups even when other cases remain unresolved.

## Verify and deliver

Create readable, standalone LaTeX with working hyperlinks, correctly escaped Spanish text, and URL-safe link arguments (including special characters). Before delivery, reconcile the ledger against all CSV rows and distinct relevant URLs; check that every verified group has all six one-sentence criterion entries, PDF links, source/page citations for substantive claims, and required missing-information statements. Review that solution ideas are distinct and grounded in the submissions.

If compilation tools are available, compile a matching `seminars_summary.pdf` beside the `.tex`, resolve compilation errors, and inspect rendered pages for layout and link readability. Otherwise report that compilation was unavailable. Finish by reporting output paths and any unresolved source or membership issues.
