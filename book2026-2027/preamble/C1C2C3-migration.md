# C1--C3 solution presentation migration

## Dependency structure

- `preamble_G10_T1_C1C2C3.tex` loads `preamble.tex` once and owns the
  decision-elements and calculation presentation helpers.
- `preamble_G10_T1_C2C3.tex` is a documented compatibility wrapper around the
  unified preamble, preserving existing consumers without parallel definitions.
- `preamble_exam_layout.tex` contains the existing exam geometry, list/table
  settings, assessment columns, problem headings, and header commands. It
  requires the common preamble and does not load a class or packages again.
- `preamble_exams.tex` retains its public entry point and loads the compatibility
  wrapper, followed by the exam-only layer. Migrated solutions load the unified
  preamble directly, followed by that same exam-only layer where required.
- The requested former `preamble_G10_T1_C1C2.tex` was absent from this checkout.
  A repository-wide search found no direct inputs of it, so there were no
  additional documents to migrate and no old C1C2 wrapper to retain.

All nine migrated documents use the exact input
`\input{preamble_G10_T1_C1C2C3}`. Their search paths cover source-directory,
academic-year-directory, and repository-root invocation. Graph dependencies
remain independent and year-local.

## Public presentation interfaces

| Helper | Arguments / purpose |
| --- | --- |
| `\DecisionElementsTable` | Four arguments: semicolon-separated alternatives, semicolon-separated states, uncertain event, contextual consequences. Printed labels explicitly use indexed `A_i` and `S_j`. |
| `\SymbolsTable` | One argument of `symbol & value with units & contextual meaning \\` rows. |
| `\PayoffStrut` | Legacy two-line minimum strut. |
| `\CalculationCell` | `{expression lines}{visible result}`; shared cell implementation. |
| `\SymbolicCell` | `{expression lines}{indexed result identifier}`. |
| `\CalcResult` | `{numerical substitution lines}{numerical result}`. |
| `\PayoffNumber` | Backward-compatible alias with the same two arguments. |
| `\CalculationPair` | `{heading}{symbolic tabular}{numerical tabular}`. Measures all cells first and gives both tables common cell height/depth; no font scaling. Corresponding rows, components, line breaks, and final result lines are supplied explicitly by the document. |
| `\FinalPayoffTable` | `{measure and units}{state headings}{alternative rows}`. Locally set `\CalculationStateCount` for tables other than two states. |
| `CalculationLandscape` | `{paper width}{paper height}`; page-scoped calculation sheets. Saves and restores the caller's exact geometry and media dimensions. |
| `L`, `M` columns | Flexible text and centered extraction-table columns formerly defined in classroom sheets. |

Every helper has one authoritative definition in the unified preamble.
Data, formulas, units, and problem-specific prose remain in the documents.
The references' former local definitions and overrides have been removed.

## Migrated documents

All paths below start at `book2026-2027/grade10/term_1/`.

| Folder | Document |
| --- | --- |
| `1-practice_activities` | `G10_T1_L1_C1C2_practice_activity-alternate-descriptions.tex` |
| `1-practice_activities` | `G10_T1_L1_C1C3_practice_activity-alternate-descriptions.tex` |
| `2-class_activities` | `G10_T1_L1_C1C2_classroom_activity.tex` |
| `2-class_activities` | `G10_T1_L1_C1C3_classroom_activity.tex` |
| `3-learning_evidences` | `G10_T1_C1C2C3C4C5C6C7_exam_solution.tex` |
| `3-learning_evidences` | `G10_T1_C1C2C3C4C5C6C7_examV2_solution.tex` |
| `3-learning_evidences` | `G10_T1_L1_C1C2C3C4_exam_solution.tex` |
| `3-learning_evidences` | `G10_T1_L1_C1C2C3C4_examV2_solution.tex` |
| `3-learning_evidences` | `G10_T1_L1_C1C2C3C4_examV3_solution.tex` |

## Presentation and preservation

Calculated solutions now show contextual input tables with units, the applicable
model, mirrored indexed symbolic/numerical tables, and a separate final table.
Additive models use `P_{ay}`. Component profit models calculate `R` and `C`
independently before `P=R-C`. Direct revenue/cost cases use only the supplied
totals. Negative substitutions retain their correct signs and meaning.

The classroom questions, exam scores, criterion assignments, labels, version
specific values, results, and conclusions are preserved. Existing dead
navigation targets received aliases. The Version 2 C1--C4 exam summary gained
a page break before its three-column C4 summary to remove vertical overflow.
Later-criterion content is otherwise unchanged.

## Validation

The existing batch files compile from each source directory with:

```text
latexmk -pdf -interaction=nonstopmode -halt-on-error DOCUMENT.tex
```

All nine documents passed that workflow. Validation used a separate `-outdir`
to avoid PDF locks in open viewers. Repository-root compilation was also checked.
All final validation logs have zero LaTeX errors, undefined references, or
overfull boxes. Rendered affected pages were inspected for clipping, overlaps,
readable type, aligned paired tables, and restored page orientation.

A content audit covered 130 paired tables and 570 corresponding cells across
the references and targets. It verified line counts, visible correctly indexed
result identifiers, numerical arithmetic, and unchanged later-criterion content
apart from the stated page break. Original final-payoff values were retained;
no mathematical inconsistency requiring an assumption or answer change was found.
