---
name: grade11-c10-practice-assessment
description: Assess submitted Grade 11 Term 1 Global Economics C10 practice PDFs against the seven-item assignment rubric and record verified results and submission links in the 11A–11E roster CSVs.
---

# Assess Grade 11 C10 practice reports

Work from the repository root. Read the authoritative assignment and rubric at `book2026-2027/grade11/term_1/1-practice_activities/G11_T1_C10_practice_activity.tex`. The companion `G11_C10_Task1_report.tex` illustrates evidence presentation. Its skew-normal mixture is optional. Assess the required work using one of the assignment's three model options.

## Locate submissions and verify identities

Find the PDFs and these rosters under `book2026-2027/grade11/term_1/5-extra_material/C10 Submissions/`.

- `11A-resultados_criterios.csv`
- `11B-resultados_criterios.csv`
- `11C-resultados_criterios.csv`
- `11D-resultados_criterios.csv`
- `11E-resultados_criterios.csv`

Read each student's full name and stated class from the PDF. Verify the name against `ESTUDIANTES` in the corresponding roster. Normalize accents, capitalization, whitespace, and unambiguous name-order variations for matching. Preserve the roster's stored name. If the class is omitted, infer it only from a unique verified name match across all five rosters. Flag class conflicts, ambiguous names, missing roster entries, unreadable submissions, and conflicting submissions for the same student. Leave unresolved rows at their existing values and continue with verified cases.

## Review and score

Review the full PDF, including plots, tables, and scanned pages. Render pages or use OCR when needed. Test the actual hyperlink targets and confirm that the intended content opens. A missing required link or one confirmed broken or requiring a permission request fails the relevant item. Recompute statistics, event counts, and other calculations against available observations where feasible. If a tool or session limitation prevents a reliable determination, mark the assessment pending and leave its CSV cells at their existing values.

Use exactly these seven items, in order. Award 1 point (`Yes`) only when all required evidence for an item is present and correct. Award 0 points (`No`) for missing or materially incorrect work in an identifiable submission. Accept mathematically equivalent methods and reasonable rounding consistent with the reported calculations. Record a page or section reference for each decision and a short reason for each `No`. For pending reports, record decisions that can be verified and explain what remains unresolved.

1. **Question and data.** Require a clear economic, financial, or operational question about a defined continuous variable, with units, context, target population, observation period, final sample size, selection and preparation. Check exclusions, missing values, and transformations where applicable. Require at least 30 usable real observations from a credible source, a source citation, and an accessible clickable original source link. If a file was downloaded or a cleaned dataset created, also verify the accessible Google Drive or OneDrive link to the exact dataset used.
2. **Sample statistics and histogram.** Verify mean, sample variance with denominator `n − 1`, and sample SD, with formulas, numerical substitutions, intermediate totals, and correct units, including squared units for variance. Check the histogram title, axis labels, units, class intervals, and bin explanation. For a density overlay, verify that the bars use density or the curve is rescaled to match the frequency scale.
3. **Fitted density.** Require a fitted density with numerical parameters, support, estimation method, a justification based on shape and assumptions, checks against the histogram and sample mean and SD, and a limitation. Moment equality by construction cannot independently establish fit. For the guide's increasing or decreasing linear density, check that the finite interval encloses the retained data, the density is nonnegative with unit area, and sample extrema are identified as estimated endpoints if used. For the exponential, check nonnegative waiting times, rate equal to the reciprocal of the sample mean in inverse time, and plausible independence and constant arrival rate. For the normal, check the guide's sample mean and positive sample SD estimates for individual observations and consider impossible values where physical bounds matter.
4. **Quantiles and model probabilities.** Verify numerical fitted-model 10th and 90th quantiles with units, parameter substitutions, and working. Check the lower, central, and upper probabilities of 0.10, 0.80, and 0.10 at the model quantiles. Require a meaningful numerical threshold `c` from the question, with the calculation and contextual interpretation of `P(X > c)`. Check the model support when evaluating the threshold.
5. **Empirical comparison.** Require a table for all four events with numerical boundaries, observation counts, sample size, empirical and fitted probabilities, absolute error, and relative percentage error. Check counts from individual observations for `X < q10`, `q10 ≤ X ≤ q90`, `X > q90`, and `X > c`. Match boundaries and inequalities in the empirical and model calculations. If counting uses rounded cutoffs, evaluate the model at those cutoffs too. Verify count divided by sample size, absolute probability difference, and 100 times that difference divided by the model probability. Relative percentage error is undefined when the model probability is zero.
6. **Interpretation and report.** Require a clear LaTeX report that answers the question with at least one calculated probability, identifies the largest absolute discrepancy, explains a plausible reason, and acknowledges that fitting and checking on the same data is descriptive.
7. **AI-use register.** Require each AI tool's name, purpose, main prompts, and working, accessible clickable links to every AI conversation used. If AI estimated parameters, check the estimation method, parameter values and units, and verification against sample statistics and the guide's model guidance. Accept an explicit statement that no AI was used.

## Stage, write, and verify roster updates

For each finalized assessment, save one `Yes` or `No` per item in these columns, in rubric order.

| CSV header | Rubric requirement |
| --- | --- |
| `C10_1` | Question and data |
| `C10_2` | Sample statistics and histogram |
| `C10_3` | Fitted density |
| `C10_4` | Quantiles and model probabilities |
| `C10_5` | Empirical comparison |
| `C10_6` | Interpretation and report |
| `C10_7` | AI-use register |

Count the `Yes` values in the seven decisions being saved. Set `C10` to `Yes` at 7/7 and `No` at 0/7 through 6/7. Set `C10P` to `100 × completed / 7`, rounded to at most two decimal places, with trailing decimal zeros omitted and a `%` suffix. For example, 6/7 gives `No` and `85.71%`. Never derive item decisions from an existing overall result or percentage.

Inspect the actual headers, delimiter, encoding (including any BOM), line endings, and quoting conventions in each target CSV. Use CSV-aware parsing and serialization. Snapshot the original and stage the proposed changes by class and verified roster row. Write all seven item decisions together with `C10`, `C10P`, and `ENLACE_ACTIVIDAD`. If missing, insert `C10P` immediately after `C10`, append any missing `C10_1`–`C10_7` headers in rubric order, and append `ENLACE_ACTIVIDAD` if needed. Preserve the relative order of existing columns and leave new cells blank for rows without finalized updates.

Use the direct submission URL when available. For a local PDF, construct an absolute URL-encoded `file://` URL from its resolved path. Preserve existing distinct links and add only new links, keeping one plain URL per line in the same CSV field when there are multiple links.

Before writing, reparse each staged CSV and compare it with the snapshot. Verify unique required headers, the correct class and row for each update, all seven `Yes` or `No` values against the reviewed evidence, and the link to the assessed PDF. Recompute `C10` and `C10P` from the seven parsed decisions and verify that both stored values match. Check that roster names, row order, CSV formatting, other criteria, unrelated cells, and existing results for rows without finalized updates are preserved. Recheck the original against the snapshot before replacing it to avoid overwriting concurrent changes. Replace each changed file as a unit and reparse it afterward to verify the same invariants and all ten updated fields.

## Handle revised submissions

When reassessing an identified student's revised PDF, link to the exact version reviewed. For a finalized reassessment, replace all seven decisions, update the overall result and percentage from those decisions, and append the revised PDF URL to the same `ENLACE_ACTIVIDAD` field, retaining distinct earlier links and skipping a URL that is already present. If the revised PDF replaces the earlier file at the same URL, keep that URL once. Treat an explicitly identified revision as the version to assess. Flag competing versions when the intended revision is unclear.

## Report the assessment

For each finalized assessment, report the stored student name, class, a clickable hyperlink to the exact PDF assessed, seven numbered `Yes`/`No` decisions with evidence locations and reasons for every `No`, completed count out of seven, percentage, and overall result. List unresolved cases separately with the submission, verified identity details and item decisions, affected row or candidate rows where known, and the evidence or identity information needed to finalize.
