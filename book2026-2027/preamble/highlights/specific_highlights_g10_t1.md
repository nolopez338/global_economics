# G10 T1

[Highlights index](specific_highlights_index.md). LaTeX is authoritative.

Authoritative modules: [highlights_g10_t1.tex](highlights_g10_t1.tex).

Load through `specific_highlights.tex`, after the shared preamble and marker loader. This module declares records and explicit memberships using the [common syntax](specific_highlights_catalog.md). Edit mathematical wording/notation and membership here; edit marker colors in the palette and presentation in tables/adapters. Shared concepts are declared only in their owning dataset; other datasets point to that stable ID.

Concept IDs owned here (definitions and source provenance remain exclusively in LaTeX):

`decision-alternative`, `decision-state`, `decision-payoff`, `decision-quantity`, `decision-rate`, `decision-fixed`, `decision-revenue`, `decision-cost`, `decision-revenuerate`, `decision-costrate`, `decision-fixedrevenue`, `decision-fixedcost`, `decision-best`, `decision-worst`, `decision-benchmark`, `decision-regret`, `decision-maxregret`, `decision-probability`, `decision-expected`, `decision-retained`, `decision-eliminated`.

| Reference key | Status | Member contexts |
|---|---|---|
| `G10-T1-C1-C2` | available | 6 |
| `G10-T1-C1-C3` | available | 10 |
| `G10-T1-C4` | available | 5 |
| `G10-T1-C5` | available | 6 |
| `G10-T1-C4-C5` | available | 8 |
| `G10-T1-C6` | available | 5 |
| `G10-T1-C7` | available | 6 |
| `G10-T1-C8` | available | 10 |
| `G10-T1-C9` | available | 11 |
| `G10-T1-C10` | available | 11 |
| `G10-T1-C1-C2-school` | available | 6 |
| `G10-T1-full` | available | 78 |

C1/C2, C1/C3 and C4/C5 are combined references; no individual C1, C2 or C3 tables are synthesized. `G10-T1-C1-C2-school` owns the printing-service variant. Other examples include enterprise profit, delivery-fleet comparison and city-logistics filtering; C10 explicitly records the absence of a worked introductory example. `decision-*` IDs separate choices, states, quantity, payoff, revenue, costs and decision rules even when colors coincide.

Practice provenance: [`book2026-2027/grade10/term_1/1-practice_activities`](../../grade10/term_1/1-practice_activities). Each context records relevant source paths and all applicable criteria. To inspect exact membership, read the `members` field of its declaration, then the named context records. Historical adapter locations are listed in [compatibility](specific_highlights_compat.md).

Records use `\HighlightDeclareConcept`, `\HighlightDeclareContext` and `\HighlightDeclareReference`; `\HighlightReference{key}[concise|detailed]` prints a common reference.

Used concept IDs (including shared concepts owned elsewhere):

`decision-alternative`, `decision-state`, `decision-payoff`, `decision-quantity`, `decision-rate`, `decision-fixed`, `decision-revenue`, `decision-cost`, `decision-revenuerate`, `decision-costrate`, `decision-fixedrevenue`, `decision-fixedcost`, `decision-best`, `decision-worst`, `decision-benchmark`, `decision-regret`, `decision-maxregret`, `decision-probability`, `decision-expected`, `complement-probability`, `decision-retained`, `decision-eliminated`.

Criterion membership by concept ID, in declared order (edit the LaTeX `members` fields first, then reconcile this interface inventory):

- `G10-T1-C1-C2`: `decision-alternative`, `decision-state`, `decision-payoff`, `decision-quantity`, `decision-rate`, `decision-fixed`.
- `G10-T1-C1-C3`: `decision-alternative`, `decision-state`, `decision-payoff`, `decision-quantity`, `decision-revenue`, `decision-cost`, `decision-revenuerate`, `decision-costrate`, `decision-fixedrevenue`, `decision-fixedcost`.
- `G10-T1-C4`: `decision-alternative`, `decision-state`, `decision-payoff`, `decision-best`, `decision-worst`.
- `G10-T1-C5`: `decision-alternative`, `decision-state`, `decision-payoff`, `decision-benchmark`, `decision-regret`, `decision-maxregret`.
- `G10-T1-C4-C5`: `decision-alternative`, `decision-state`, `decision-payoff`, `decision-best`, `decision-worst`, `decision-benchmark`, `decision-regret`, `decision-maxregret`.
- `G10-T1-C6`: `decision-alternative`, `decision-state`, `decision-payoff`, `decision-probability`, `decision-expected`.
- `G10-T1-C7`: `decision-alternative`, `decision-state`, `decision-payoff`, `decision-probability`, `complement-probability`, `decision-expected`.
- `G10-T1-C8`: `decision-alternative`, `decision-state`, `decision-payoff`, `decision-best`, `decision-worst`, `decision-benchmark`, `decision-regret`, `decision-maxregret`, `decision-probability`, `decision-expected`.
- `G10-T1-C9`: `decision-alternative`, `decision-state`, `decision-payoff`, `decision-best`, `decision-worst`, `decision-regret`, `decision-maxregret`, `decision-probability`, `decision-expected`, `decision-retained`, `decision-eliminated`.
- `G10-T1-C10`: `decision-alternative`, `decision-state`, `decision-payoff`, `decision-best`, `decision-worst`, `decision-regret`, `decision-maxregret`, `decision-probability`, `decision-expected`, `decision-retained`, `decision-eliminated`.
- `G10-T1-C1-C2-school`: `decision-alternative`, `decision-state`, `decision-payoff`, `decision-quantity`, `decision-rate`, `decision-fixed`.

The complement probability shared with Bernoulli models has one stable concept ID, `complement-probability`; decision-specific notation, wording and color wrappers remain in its Grade 10 contexts.
