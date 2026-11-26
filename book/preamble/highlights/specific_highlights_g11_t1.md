# G11 T1

[Highlights index](specific_highlights_index.md). LaTeX is authoritative.

Authoritative modules: [highlights_g11_t1.tex](highlights_g11_t1.tex).

Load through `specific_highlights.tex`, after the shared preamble and marker loader. This module declares records and explicit memberships using the [common syntax](specific_highlights_catalog.md). Edit mathematical wording/notation and membership here; edit marker colors in the palette and presentation in tables/adapters. Shared concepts are declared only in their owning dataset; other datasets point to that stable ID.

Concept IDs owned here (definitions and source provenance remain exclusively in LaTeX):

`random-variable`, `continuous-support`, `outcome-and-event`, `event-probability`, `cumulative-probability`, `density`, `unknown-constant`, `success-probability`, `complement-probability`, `count`, `poisson-expected-count`, `slope`, `mode`, `period`, `exponential-rate`, `expected-value`, `population-mean`, `population-variance`, `population-standard-deviation`, `sample-mean`, `sample-variance`, `sample-standard-deviation`, `sample-proportion`, `absolute`, `relative`, `degrees-of-freedom`, `critical-value`, `tail-probability`, `scale`, `interval-bounds`, `standard-error`, `location`.

| Reference key | Status | Member contexts |
|---|---|---|
| `G11-T1-introduction-group-1` | available | 14 |
| `G11-T1-introduction-group-2` | available | 9 |
| `G11-T1-introduction-group-3` | available | 9 |
| `G11-T1-introduction` | available | 32 |
| `G11-T1-C1` | available | 14 |
| `G11-T1-C2` | available | 7 |
| `G11-T1-C3` | available | 5 |
| `G11-T1-C4` | available | 4 |
| `G11-T1-C5` | available | 12 |
| `G11-T1-C6-C7` | available | 13 |
| `G11-T1-C8` | available | 14 |
| `G11-T1-C9` | available | 16 |
| `G11-T1-C10` | available | 17 |
| `G11-T1-full` | available | 102 |

C6/C7 is combined-only. C1 distribution introductions include discrete prerequisites (success/complement probabilities and Poisson expected count) in their actual Grade 11 Term 1 context. They do not create other-term criterion references. Rate, density, support, sample measures, Student t and error measures retain their own meanings. Contexts keep the existing courier, warehouse, periodic, waiting-time and comparison interpretations, including C10 investigation guidance.

Practice provenance: [`book/grade11/term_1/1-practice_activities`](../../grade11/term_1/1-practice_activities). Each context records relevant source paths and all applicable criteria. To inspect exact membership, read the `members` field of its declaration, then the named context records. Historical adapter locations are listed in [compatibility](specific_highlights_compat.md).

The grouped introduction declares three non-criterion group references and their complete introduction reference. `\COneToneCatalog` preserves the group headings while reading those memberships.

Records use `\HighlightDeclareConcept`, `\HighlightDeclareContext` and `\HighlightDeclareReference`; `\HighlightReference{key}[concise|detailed]` prints a common reference.

Used concept IDs (including shared concepts owned elsewhere):

`random-variable`, `continuous-support`, `outcome-and-event`, `event-probability`, `cumulative-probability`, `density`, `success-probability`, `complement-probability`, `count`, `poisson-expected-count`, `mode`, `population-mean`, `population-standard-deviation`, `population-variance`, `unknown-constant`, `slope`, `period`, `exponential-rate`, `expected-value`, `sample-mean`, `sample-variance`, `sample-standard-deviation`, `sample-proportion`, `absolute`, `relative`, `degrees-of-freedom`, `critical-value`, `tail-probability`, `scale`, `interval-bounds`, `standard-error`, `location`.

Criterion membership by concept ID, in declared order (edit the LaTeX `members` fields first, then reconcile this interface inventory):

- `G11-T1-C1`: `random-variable`, `continuous-support`, `outcome-and-event`, `event-probability`, `cumulative-probability`, `density`, `success-probability`, `complement-probability`, `count`, `poisson-expected-count`, `mode`, `population-mean`, `population-standard-deviation`, `population-variance`.
- `G11-T1-C2`: `random-variable`, `continuous-support`, `event-probability`, `density`, `unknown-constant`, `slope`, `mode`.
- `G11-T1-C3`: `random-variable`, `continuous-support`, `event-probability`, `density`, `period`.
- `G11-T1-C4`: `random-variable`, `continuous-support`, `event-probability`, `exponential-rate`.
- `G11-T1-C5`: `random-variable`, `continuous-support`, `density`, `mode`, `exponential-rate`, `expected-value`, `population-mean`, `population-variance`, `population-standard-deviation`, `sample-mean`, `sample-variance`, `sample-standard-deviation`.
- `G11-T1-C6-C7`: `random-variable`, `event-probability`, `density`, `count`, `population-mean`, `population-variance`, `population-standard-deviation`, `sample-mean`, `sample-variance`, `sample-standard-deviation`, `sample-proportion`, `absolute`, `relative`.
- `G11-T1-C8`: `random-variable`, `event-probability`, `cumulative-probability`, `count`, `population-mean`, `population-standard-deviation`, `sample-standard-deviation`, `sample-mean`, `degrees-of-freedom`, `critical-value`, `tail-probability`, `scale`, `interval-bounds`, `standard-error`.
- `G11-T1-C9`: `location`, `random-variable`, `event-probability`, `cumulative-probability`, `population-mean`, `population-standard-deviation`, `sample-mean`, `sample-standard-deviation`, `degrees-of-freedom`, `critical-value`, `tail-probability`, `scale`, `interval-bounds`, `standard-error`, `absolute`, `relative`.
- `G11-T1-C10`: `random-variable`, `continuous-support`, `event-probability`, `cumulative-probability`, `density`, `exponential-rate`, `population-mean`, `population-variance`, `population-standard-deviation`, `sample-mean`, `sample-variance`, `sample-standard-deviation`, `count`, `sample-proportion`, `absolute`, `relative`, `critical-value`.
