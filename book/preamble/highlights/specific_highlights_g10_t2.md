# G10 T2

[Highlights index](specific_highlights_index.md). LaTeX is authoritative.

Authoritative modules: [highlights_g10_t2.tex](highlights_g10_t2.tex).

Load through `specific_highlights.tex`, after the shared preamble and marker loader. This module declares records and explicit memberships using the [common syntax](specific_highlights_catalog.md). Edit mathematical wording/notation and membership here; edit marker colors in the palette and presentation in tables/adapters. Shared concepts are declared only in their owning dataset; other datasets point to that stable ID.

Concept IDs owned here (definitions and source provenance remain exclusively in LaTeX):

`outcome-space`, `event`, `discrete-support`, `second`, `third`, `mathematical-operations`, `assume`, `cutoff`, `aux`, `break`, `transform`, `design-count`, `wait`, `target`, `event-rate-per-exposure`, `secondmoment`.

| Reference key | Status | Member contexts |
|---|---|---|
| `G10-T2-C1-C2-C3-C4-C5-C6-C7-C8-C9` | available | 6 |
| `G10-T2-C8` | available | 8 |
| `G10-T2-C1-C2-C3-C4-C5-C6-C7-C8-C9-coordinated` | available | 101 |
| `G10-T2-C1-coordinated` | available | 10 |
| `G10-T2-C2-coordinated` | available | 11 |
| `G10-T2-C3-coordinated` | available | 12 |
| `G10-T2-C4-coordinated` | available | 11 |
| `G10-T2-C5-coordinated` | available | 10 |
| `G10-T2-C6-coordinated` | available | 12 |
| `G10-T2-C7-coordinated` | available | 10 |
| `G10-T2-C8-coordinated` | available | 11 |
| `G10-T2-C9-coordinated` | available | 15 |
| `G10-T2-C1` | available | 12 |
| `G10-T2-introduction` | available | 27 |
| `G10-T2-full` | available | 128 |
| `G10-T3-full` | pending | 0 |
| `G10-T2-C10` | pending | 0 |

`-coordinated` keys own the source-backed criterion selections; legacy and slide variants keep their specialized schemas through compatibility renderers. `-introduction` explicitly records extra notation and prerequisite scope without inventing criteria. Context `variant` distinguishes coordinated, legacy, slides, introductory-prerequisite and compatibility-default records. `-full` selects coordinated and introductory coverage. Term 3 stays explicitly pending. No missing introductory-example interpretations were invented for Term 2.

Practice provenance: [`book/grade10/term_2/1-practice_activities`](../../grade10/term_2/1-practice_activities). Each context records relevant source paths and all applicable criteria. To inspect exact membership, read the `members` field of its declaration, then the named context records. Historical adapter locations are listed in [compatibility](specific_highlights_compat.md).

Records use `\HighlightDeclareConcept`, `\HighlightDeclareContext` and `\HighlightDeclareReference`; `\HighlightReference{key}[concise|detailed]` prints a common reference.

Used concept IDs (including shared concepts owned elsewhere):

`outcome-space`, `event-probability`, `random-variable`, `second`, `third`, `unknown-constant`, `expected-value`, `secondmoment`, `event`, `discrete-support`, `mathematical-operations`, `assume`, `cumulative-probability`, `cutoff`, `aux`, `success-probability`, `complement-probability`, `break`, `transform`, `design-count`, `wait`, `target`, `event-rate-per-exposure`, `poisson-expected-count`, `population-mean`, `population-variance`, `population-standard-deviation`.

Criterion membership by concept ID, in declared order (edit the LaTeX `members` fields first, then reconcile this interface inventory):

- `G10-T2-C1-C2-C3-C4-C5-C6-C7-C8-C9`: `outcome-space`, `event-probability`, `random-variable`, `second`, `third`, `unknown-constant`.
- `G10-T2-C8`: `random-variable`, `second`, `expected-value`, `secondmoment`.
- `G10-T2-C1-C2-C3-C4-C5-C6-C7-C8-C9-coordinated`: `outcome-space`, `event`, `random-variable`, `discrete-support`, `second`, `third`, `event-probability`, `unknown-constant`, `mathematical-operations`, `assume`, `cumulative-probability`, `cutoff`, `aux`, `success-probability`, `complement-probability`, `expected-value`, `break`, `transform`, `design-count`, `wait`, `target`, `event-rate-per-exposure`, `poisson-expected-count`, `population-mean`, `secondmoment`, `population-variance`, `population-standard-deviation`.
- `G10-T2-C1-coordinated`: `outcome-space`, `event`, `random-variable`, `discrete-support`, `second`, `third`, `event-probability`, `unknown-constant`, `mathematical-operations`, `assume`.
- `G10-T2-C2-coordinated`: `outcome-space`, `event`, `random-variable`, `discrete-support`, `event-probability`, `cumulative-probability`, `unknown-constant`, `cutoff`, `mathematical-operations`, `assume`, `aux`.
- `G10-T2-C3-coordinated`: `event`, `random-variable`, `discrete-support`, `success-probability`, `complement-probability`, `second`, `event-probability`, `cumulative-probability`, `expected-value`, `break`, `transform`.
- `G10-T2-C4-coordinated`: `random-variable`, `discrete-support`, `second`, `success-probability`, `complement-probability`, `design-count`, `event-probability`, `cumulative-probability`, `cutoff`, `mathematical-operations`, `assume`.
- `G10-T2-C5-coordinated`: `wait`, `discrete-support`, `success-probability`, `complement-probability`, `second`, `event-probability`, `cumulative-probability`, `cutoff`, `event`, `assume`.
- `G10-T2-C6-coordinated`: `wait`, `discrete-support`, `success-probability`, `complement-probability`, `target`, `second`, `event-probability`, `cumulative-probability`, `design-count`, `cutoff`, `mathematical-operations`, `assume`.
- `G10-T2-C7-coordinated`: `random-variable`, `discrete-support`, `event-probability`, `cumulative-probability`, `cutoff`, `event-rate-per-exposure`, `poisson-expected-count`, `second`, `mathematical-operations`, `assume`.
- `G10-T2-C8-coordinated`: `random-variable`, `discrete-support`, `second`, `event-probability`, `expected-value`, `population-mean`, `secondmoment`, `population-variance`, `population-standard-deviation`, `transform`, `mathematical-operations`.
- `G10-T2-C9-coordinated`: `event`, `random-variable`, `discrete-support`, `wait`, `second`, `success-probability`, `complement-probability`, `design-count`, `target`, `event-probability`, `cumulative-probability`, `event-rate-per-exposure`, `poisson-expected-count`, `mathematical-operations`, `assume`.
- `G10-T2-C1`: `outcome-space`, `event-probability`, `random-variable`, `second`, `third`, `unknown-constant`.
- `G10-T2-C10`: pending; no members.

Supplemental `G10-T2-C1-notation`, `G10-T2-C2-notation` and `G10-T2-C3-notation` references expose notation contexts under existing concepts. These are opt-in; coordinated/full memberships and concise legend grouping are retained. Use `\HighlightEffectiveField{context-id}{definition}` in explicit practice rows, or `\HighlightForEachMember` with a local callback. `\HighlightReference` still groups by concept and does not split notation into rows. Numbers, units and introductory interpretations remain local.

C2 now stores the explicit discrete CDF jump identity. Supplemental contexts separate outcomes/space, rules/values, inclusive/strict heights, jumps, transformation functions/state outputs, PMFs/CDFs and the expectation operator. Shared transformation definitions do not impose USD, binary domains or opposite-sign payoffs on unrelated callers.

The C3-only `g10-t2-c3-coordinated-10-function` context adds the transformation-function legend row immediately below the secondary variable. It and the two C3 notation-function contexts use `transformation.function.c3` / `\HLGtenCThreeFunction`; `f` and indexed rule symbols are darker green, while evaluated state payoffs keep the monetary-consequence role. Other transformation contexts and combined-reference memberships are unchanged.
