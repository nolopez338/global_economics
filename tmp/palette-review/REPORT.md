# Shared highlight palette update

## Final mapping

| Mathematical role | Wrapper | Effective color |
|---|---|---|
| General probability and PMF mass | `\HLProbability` / `\GTenHLProbability` | `GTenHLProbability`, `#86BFF0` |
| Success parameter and its individual break-even threshold | `\HLSuccessProbability` | `MathHLSuccessColor = GTenHLProbability!65!CtwoCriticalColor`; xcolor HTML `#6495DD` |
| Complement parameter | `\HLComplementProbability` | `MathHLComplementColor = G11T2C1PopulationProportion`, `#D74383` |
| Confidence level | `\HLConfidence` / `\CtwoConfidence` | `CtwoConfidenceColor`, unchanged `#55C8F0` |
| Population or planning proportion | `\HLPopulationProportion` | `G11T2C1PopulationProportion`, unchanged `#D74383` |

The original registry success color was `#D74383` and complement color was `#6495DD`, verified with xcolor before editing. General masses shared the population-proportion wrapper; these now have a dedicated probability wrapper. C3 success previously forwarded inconsistently to general blue; it now uses the dedicated success wrapper. Its dark probability graph ink follows that role. Mathematical meaning, rather than symbol spelling, determines these bindings.

## Changed source files

- `book2026-2027/preamble/graphs/highlights.tex`
- `book2026-2027/preamble/graphs/specific_highlights.tex`
- `book2026-2027/preamble/graphs/specific_highlights_view.tex`
- `book2026-2027/preamble/graphs/specific_highlights.md`
- `book2026-2027/grade10/term_2/1-practice_activities/G10_T2_L1_C3_practice_activity.tex`

## Build and inspection coverage

- All 28 registered legends appear exactly once in the preview, including legacy G10-T2-C1; duplicate combined catalogs were removed.
- Preview compiled with latexmk/pdfLaTeX; all 15 rendered pages inspected. C3 compiled twice and all 34 pages inspected, with detailed checks of the legend, formulas, values and graphs.
- G10 C1–C9 practices and G11 C2 confidence reference compiled successfully. G10 legend opening and continuation pages inspected; G11 C2 reference pages 2–3 inspected. This is a targeted palette review, not a full visual review of all pages in the other practices.
- Disabled-highlight preview and C3 variants compiled in isolation; opening legend, mathematical content and black graph labels inspected. Grayscale palette proof inspected.
- xcolor assertions checked general, confidence, success, complement and population-proportion colors at default scope, within each scoped palette, and after groups closed.
- Source checks confirmed unchanged C3 mathematics and toggle, unchanged renderer opacity (fill 0.32/text 1), unchanged unrelated color definitions and both scoped palette commands.
- Markdown reconciled against live aliases, defaults, palette scope, omitted context rows and actual printed row selections. All registry keys and relative source links checked.
- Final logs reviewed for errors, overflow and unresolved references. Three G10 documents needed an additional reference-settling pass.

## Matching PDFs

- `book2026-2027/grade10/term_2/1-practice_activities/G10_T2_L1_C1_practice_activity.pdf`
- `book2026-2027/grade10/term_2/1-practice_activities/G10_T2_L1_C2_practice_activity.pdf`
- `book2026-2027/grade10/term_2/1-practice_activities/G10_T2_L1_C3_practice_activity.pdf`
- `book2026-2027/grade10/term_2/1-practice_activities/G10_T2_L1_C4_practice_activity.pdf`
- `book2026-2027/grade10/term_2/1-practice_activities/G10_T2_L2_C5_practice_activity.pdf`
- `book2026-2027/grade10/term_2/1-practice_activities/G10_T2_L2_C6_practice_activity.pdf`
- `book2026-2027/grade10/term_2/1-practice_activities/G10_T2_L2_C7_practice_activity.pdf`
- `book2026-2027/grade10/term_2/1-practice_activities/G10_T2_L3_C8_practice_activity.pdf`
- `book2026-2027/grade10/term_2/1-practice_activities/G10_T2_L3_C9_practice_activity.pdf`
- `book2026-2027/preamble/graphs/specific_highlights_view.pdf`

## Remaining scope limits

No remaining requested palette mismatch was found in the audited registry and affected practice forwarding commands. G10 C10 still has no source-backed registered legend, and the preview states that explicitly. The existing G11 C8 criterion wording issue recorded in the shared reference remains outside this palette change. Other practice pages were not comprehensively re-reviewed. Unrelated existing workspace edits were preserved.
