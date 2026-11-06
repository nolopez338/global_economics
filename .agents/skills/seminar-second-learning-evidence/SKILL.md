---
name: seminar-second-learning-evidence
description: Assess Grade 10 Global Economics seminar PDFs for Term 1 second learning evidence and record individual Yes/No results, completion percentages for criteria C5 through C10, and submission links in resultados_criterios.csv.
---

# Assess second learning evidence

Work from the repository root. Read the submitted PDFs in `book2026-2027/seminars/term_1/second_learning_evidence`. Use these LaTeX guides in `book2026-2027/seminars/term_1` as the requirements.

| Guide | CSV columns |
| --- | --- |
| `C5C6-Activity.tex` | `C5` and `C5P`, `C6` and `C6P` |
| `C7C8-Activity.tex` | `C7` and `C7P`, `C8` and `C8P` |
| `C9C10-Activity.tex` | `C9` and `C9P`, `C10` and `C10P` |

## 1. Establish the checklists

Read all three guides before opening submissions. Build a separate checklist for each criterion from C5 through C10. Use the criterion labels in the guide to assign required deliverables and responses, then list them in task order. Use numbered tasks where present and substantive task sections where unnumbered, including their explicitly required subparts. Give each item a stable ID and identify its source task. Count each required response once within its criterion. Use the final verification list to cross-check coverage and avoid counting repeated requirements twice.

Exclude examples, optional work, and formatting directions. Where the guide allows alternative formats or gives an alternative response for insufficient evidence, count the requirement once and accept the prescribed alternatives. Keep requirements that apply to every group member within fixed checklist items so the denominator stays the same across groups. Record a separate total for each criterion and apply its checklist consistently to every group.

## 2. Review the PDFs

Identify the applicable guide from the title, task content, and filename together. For cumulative PDFs, assess each guide for which the submission contains evidence. Read the full PDF, including tables, diagrams, images, and scanned pages that may contain evidence. Render pages or use OCR as needed, and inspect page images where text extraction is incomplete.

Credit an item when the PDF shows a substantive attempt and note the page or location. A blank, placeholder, or copied instruction earns no credit. Assess completion and accept imperfect answers that substantively address the requirement. Flag unreadable evidence for resolution.

## 3. Calculate each criterion's result and percentage

For each criterion, divide its completed items by its own total required items. Compare the exact fraction to 60% before formatting the percentage for reporting. The equivalent integer test is `10 * completed >= 6 * total`.

At least 60% earns `Yes` for that criterion. Below 60% earns `No`. Calculate the completion percentage as `100 × completed items ÷ total required items` for that criterion. Round to at most two decimal places, omit trailing decimal zeros, and append `%`.

For an identifiable C5–C6 submission with 6 of 10 C5 items complete and zero C6 items complete, record `C5 = Yes` and `C5P = 60%`, and `C6 = No` and `C6P = 0%`.

## 4. Match group members and resolve updates

Look for `resultados_criterios.csv` in the submission folder first. If absent, search the repository and verify the intended roster before editing. Identify all group members named in the PDF and match them to existing rows in the `ESTUDIANTES` column. Compare names across variations in accents, capitalization, whitespace, and name order. Require a unique match and preserve the stored roster name.

Flag ambiguous names, missing roster entries, unreadable evidence, uncertain guide assignments, and conflicting submissions for the same student and criterion. Stage proposed updates and check for conflicts before writing. Leave affected cells at their existing values until resolved and continue with unambiguous cases. Preserve results for students and guides without submission evidence. Within an identifiable submission, count missing work for a criterion as incomplete.

## 5. Write and verify the CSV

Inspect the actual delimiter, encoding, and header before editing. Use CSV-aware parsing. Ensure `C1P, C2P, C3P, C4P, C5P, C6P, C7P, C8P, C9P, C10P` form a single block in that order immediately after `C10`. Add only missing columns and initialize their cells to blank. Place any existing percentage columns in the block while retaining their values by row. Preserve the relative order of all other columns.

For each verified C5–C10 assessment, update the criterion cell and its matching percentage cell together for every matched student. Write exactly `Yes` or `No` in the criterion cell. Preserve both existing values for unassessed criteria and unresolved cases, and leave any newly added percentage cells for those cases blank. Treat `C1P`–`C4P` as schema columns and preserve their existing values.

Append a single `ENLACE_ACTIVIDAD` column if it is missing. For each matched student with a verified assessment, record the URL of the submitted PDF that supports the assessment. Use the original direct submission URL when available. For a local PDF, use an absolute `file://` URL with URL-encoded path characters. Use plain URLs as cell values so the CSV remains readable across applications. Write the same URL for each verified member of a group. If several PDFs support the student's assessments, keep one URL per line in the same CSV field, preserving existing links and adding only distinct URLs. Preserve the existing link cell when there is no verified update and leave newly added cells blank for those rows.

Validate the proposed CSV before replacing the original. Reparse the written file and compare it with the pre-edit snapshot. Verify that the percentage block appears exactly once in the required order and position, that `ENLACE_ACTIVIDAD` appears exactly once, and that all other columns retain their relative order. Check each intended pair against the exact threshold and formatted percentage from the same checklist counts. Verify that each added URL points to the assessed PDF for the matched student and that existing links are retained. Verify that all unrelated existing cells retain their original values, all newly added cells without a verified update are blank, and row order, roster names, delimiter, and encoding are preserved.

## 6. Report the assessment

For each assessed group, give its members and report the guide, completed count out of the criterion checklist total, completion percentage, and `Yes` or `No` result separately for each assessed criterion. List unresolved cases separately with the submission, reason, and pending CSV cells by roster name or row and criterion. If a roster row or criterion cannot be identified, report what is known and flag any candidate cells without guessing.
