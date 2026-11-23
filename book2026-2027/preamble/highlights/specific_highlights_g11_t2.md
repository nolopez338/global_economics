# G11 T2

[Highlights index](specific_highlights_index.md). LaTeX is authoritative.

Authoritative modules: [highlights_g11_t2.tex](highlights_g11_t2.tex).

Load through `specific_highlights.tex`, after the shared preamble and marker loader. This module declares records and explicit memberships using the [common syntax](specific_highlights_catalog.md). Edit mathematical wording/notation and membership here; edit marker colors in the palette and presentation in tables/adapters. Shared concepts are declared only in their owning dataset; other datasets point to that stable ID.

Concept IDs owned here (definitions and source provenance remain exclusively in LaTeX):

`sample`, `population`, `obs`, `population-proportion`, `confidence`, `margin`, `width`, `reported`, `reportedwidth`, `coverage`, `error`, `normal`, `shape`, `theoretical`, `budget`, `fraction`, `successcount`, `planning`, `precisionplan`, `simulation`, `variability`, `ceiling`.

| Reference key | Status | Member contexts |
|---|---|---|
| `G11-T2-C1` | available | 11 |
| `G11-T2-C1-slides` | available | 20 |
| `G11-T2-C2` | available | 29 |
| `G11-T2-C3` | available | 18 |
| `G11-T2-C1-C2-C3-C4-C5-C6-C7-C8-C9-C10-coordinated` | available | 146 |
| `G11-T2-C1-coordinated` | available | 12 |
| `G11-T2-C2-coordinated` | available | 19 |
| `G11-T2-C3-coordinated` | available | 15 |
| `G11-T2-C4-coordinated` | available | 16 |
| `G11-T2-C5-coordinated` | available | 13 |
| `G11-T2-C6-coordinated` | available | 13 |
| `G11-T2-C7-coordinated` | available | 13 |
| `G11-T2-C8-coordinated` | available | 16 |
| `G11-T2-C9-coordinated` | available | 10 |
| `G11-T2-C10-coordinated` | available | 19 |
| `G11-T2-introduction` | available | 37 |
| `G11-T2-full` | available | 183 |
| `G11-T3-full` | pending | 0 |

`-coordinated` keys own the source-backed criterion selections; legacy and slide variants keep their specialized schemas through compatibility renderers. `-introduction` explicitly records extra notation and prerequisite scope without inventing criteria. Context `variant` distinguishes coordinated, legacy, slides, introductory-prerequisite and compatibility-default records. `-full` selects coordinated and introductory coverage. Term 3 stays explicitly pending. No missing introductory-example interpretations were invented for Term 2.

Practice provenance: [`book2026-2027/grade11/term_2/1-practice_activities`](../../grade11/term_2/1-practice_activities). Each context records relevant source paths and all applicable criteria. To inspect exact membership, read the `members` field of its declaration, then the named context records. Historical adapter locations are listed in [compatibility](specific_highlights_compat.md).

Records use `\HighlightDeclareConcept`, `\HighlightDeclareContext` and `\HighlightDeclareReference`; `\HighlightReference{key}[concise|detailed]` prints a common reference.

Used concept IDs (including shared concepts owned elsewhere):

`sample`, `population`, `design-count`, `sample-mean`, `population-mean`, `sample-standard-deviation`, `population-standard-deviation`, `sample-variance`, `population-variance`, `sample-proportion`, `population-proportion`, `standard-error`, `confidence`, `critical-value`, `margin`, `interval-bounds`, `width`, `coverage`, `tail-probability`, `obs`, `reported`, `reportedwidth`, `error`, `normal`, `shape`, `theoretical`, `budget`, `fraction`, `successcount`, `planning`, `precisionplan`, `degrees-of-freedom`, `mathematical-operations`, `complement-probability`, `simulation`, `variability`, `ceiling`.

Criterion membership by concept ID, in declared order (edit the LaTeX `members` fields first, then reconcile this interface inventory):

- `G11-T2-C1`: `sample`, `population`, `design-count`, `sample-mean`, `population-mean`, `sample-standard-deviation`, `population-standard-deviation`, `sample-variance`, `population-variance`, `sample-proportion`, `population-proportion`.
- `G11-T2-C1-slides`: `sample`, `population`, `sample-mean`, `population-mean`, `sample-standard-deviation`, `population-standard-deviation`, `sample-variance`, `population-variance`, `sample-proportion`, `population-proportion`.
- `G11-T2-C2`: `sample-mean`, `population-mean`, `design-count`, `population-standard-deviation`, `standard-error`, `confidence`, `critical-value`, `margin`, `interval-bounds`, `width`, `coverage`, `tail-probability`.
- `G11-T2-C3`: `sample-mean`, `population-mean`, `standard-error`, `confidence`, `critical-value`, `margin`, `interval-bounds`, `width`, `coverage`.
- `G11-T2-C1-C2-C3-C4-C5-C6-C7-C8-C9-C10-coordinated`: `sample`, `population`, `design-count`, `obs`, `population-mean`, `sample-mean`, `population-standard-deviation`, `sample-standard-deviation`, `population-variance`, `sample-variance`, `population-proportion`, `sample-proportion`, `standard-error`, `confidence`, `tail-probability`, `critical-value`, `margin`, `interval-bounds`, `width`, `reported`, `reportedwidth`, `coverage`, `error`, `normal`, `shape`, `theoretical`, `budget`, `fraction`, `successcount`, `planning`, `precisionplan`, `degrees-of-freedom`, `mathematical-operations`.
- `G11-T2-C1-coordinated`: `sample`, `population`, `design-count`, `obs`, `population-mean`, `sample-mean`, `population-standard-deviation`, `sample-standard-deviation`, `population-variance`, `sample-variance`, `population-proportion`, `sample-proportion`.
- `G11-T2-C2-coordinated`: `population-mean`, `sample-mean`, `population-standard-deviation`, `design-count`, `sample-standard-deviation`, `standard-error`, `confidence`, `tail-probability`, `critical-value`, `margin`, `interval-bounds`, `width`, `reported`, `reportedwidth`, `coverage`, `error`, `normal`, `obs`, `shape`.
- `G11-T2-C3-coordinated`: `population-mean`, `sample-mean`, `population-standard-deviation`, `design-count`, `standard-error`, `confidence`, `tail-probability`, `critical-value`, `margin`, `interval-bounds`, `width`, `normal`, `theoretical`, `budget`, `shape`.
- `G11-T2-C4-coordinated`: `population-mean`, `sample-mean`, `population-variance`, `population-standard-deviation`, `design-count`, `population`, `standard-error`, `confidence`, `tail-probability`, `critical-value`, `margin`, `interval-bounds`, `normal`, `fraction`, `shape`, `budget`.
- `G11-T2-C5-coordinated`: `population-proportion`, `sample-proportion`, `successcount`, `design-count`, `population`, `standard-error`, `confidence`, `critical-value`, `margin`, `interval-bounds`, `fraction`, `shape`, `budget`.
- `G11-T2-C6-coordinated`: `population-mean`, `population-standard-deviation`, `population-proportion`, `planning`, `design-count`, `precisionplan`, `population`, `confidence`, `critical-value`, `margin`, `fraction`, `shape`, `budget`.
- `G11-T2-C7-coordinated`: `population-proportion`, `sample-proportion`, `successcount`, `design-count`, `population`, `standard-error`, `confidence`, `critical-value`, `margin`, `interval-bounds`, `width`, `fraction`, `shape`.
- `G11-T2-C8-coordinated`: `population-mean`, `sample-mean`, `population-standard-deviation`, `sample-standard-deviation`, `design-count`, `population`, `standard-error`, `confidence`, `tail-probability`, `critical-value`, `margin`, `interval-bounds`, `degrees-of-freedom`, `fraction`, `shape`, `budget`.
- `G11-T2-C9-coordinated`: `sample`, `population`, `design-count`, `sample-mean`, `sample-standard-deviation`, `sample-proportion`, `successcount`, `fraction`, `shape`, `budget`.
- `G11-T2-C10-coordinated`: `sample`, `population`, `design-count`, `obs`, `population-mean`, `sample-mean`, `sample-standard-deviation`, `sample-variance`, `standard-error`, `confidence`, `critical-value`, `margin`, `interval-bounds`, `degrees-of-freedom`, `precisionplan`, `fraction`, `shape`, `budget`, `mathematical-operations`.

Legacy-cell `display`/`meaning` fields retain the existing illustrative interval values and specialized sample/population cells. They do not invent introductory-practice interpretations.

Supplemental `G11-T2-C1-notation`, `G11-T2-C2-notation` and `G11-T2-C3-notation` references expose notation contexts under existing concepts. These are opt-in; coordinated/full memberships and concise legend grouping are retained. Use `\HighlightEffectiveField{context-id}{definition}` in explicit practice rows, or `\HighlightForEachMember` with a local callback. `\HighlightReference` still groups by concept and does not split notation into rows. Numbers, units and introductory interpretations remain local.

C1 population-size notation uses `count.design` / `\HLObservationCount`; population groups retain `group.population` and the opening retains its Sample/Population layout. C1/C3 population-mean briefs and definitions are generic; C2 retains the simulation qualification and adds a separately selectable context under `simulation`. Supplemental contexts distinguish indexed groups/counts/means, excluded/tail areas, calculated/reported endpoints and intervals, coverage counts/percentage, normal functions and model-scoped functional dependence. District meanings and numerical assumptions stay local.
