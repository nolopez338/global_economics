# Term 2 highlights gaps: consolidated source reconciliation

## 1. Scope and linked input inventory

This report reconciles **six input gaps reports**, all `*gaps.md` files directly within the two requested Term 2 practice directories. It covers Grade 10 and Grade 11, criteria C1–C3. Individual reports are evidence of adaptation requirements; live LaTeX declarations, their effective fields, compatibility implementations and practice callers determine what is currently supported. Olympiad work is excluded.

| Origin ID | Grade / criterion | Input report | Affected practice source |
|---|---|---|---|
| R10.1 | 10 / C1 | [C1 gaps](../../grade10/term_2/1-practice_activities/G10_T2_L1_C1_practice_activity_highlights_gaps.md) | [G10 C1 practice](../../grade10/term_2/1-practice_activities/G10_T2_L1_C1_practice_activity.tex) |
| R10.2 | 10 / C2 | [C2 gaps](../../grade10/term_2/1-practice_activities/G10_T2_L1_C2_practice_activity_highlights_gaps.md) | [G10 C2 practice](../../grade10/term_2/1-practice_activities/G10_T2_L1_C2_practice_activity.tex) |
| R10.3 | 10 / C3 | [C3 gaps](../../grade10/term_2/1-practice_activities/G10_T2_L1_C3_practice_activity_highlights_gaps.md) | [G10 C3 practice](../../grade10/term_2/1-practice_activities/G10_T2_L1_C3_practice_activity.tex) |
| R11.1 | 11 / C1 | [C1 gaps](../../grade11/term_2/1-practice_activities/G11_T2_L1_C1_practice_highlights_gaps.md) | [G11 C1 practice](../../grade11/term_2/1-practice_activities/G11_T2_L1_C1_practice.tex) |
| R11.2 | 11 / C2 | [C2 gaps](../../grade11/term_2/1-practice_activities/G11_T2_L1_C2_practice_highlights_gaps.md) | [G11 C2 practice](../../grade11/term_2/1-practice_activities/G11_T2_L1_C2_practice.tex) |
| R11.3 | 11 / C3 | [C3 gaps](../../grade11/term_2/1-practice_activities/G11_T2_L1_C3_practice_highlights_gaps.md) | [G11 C3 practice](../../grade11/term_2/1-practice_activities/G11_T2_L1_C3_practice.tex) |

### Authority and dependency path

The starting point is [specific_highlights_index.md](specific_highlights_index.md). [highlights.tex](highlights.tex) loads palette, renderer and base roles; [specific_highlights.tex](specific_highlights.tex) initializes registry palette/roles, then loads [catalog](highlights_catalog.tex), datasets in the order [G11 T1](highlights_g11_t1.tex) → [G10 T1](highlights_g10_t1.tex) → [G10 T2](highlights_g10_t2.tex) → [G11 T2](highlights_g11_t2.tex), [tables](highlights_tables.tex), and [compatibility](highlights_compat.tex). The last loads the Term 2, G11 and G10 adapters. Relevant live implementations here are [roles](highlights_roles.tex), [palette](highlights_palette.tex), and [Term 2 compatibility](highlights_compat_ttwo.tex).

Inherited concepts require particular care: `random-variable`, `event-probability`, `cumulative-probability`, `expected-value`, `population-mean`, `standard-error`, `critical-value`, `tail-probability` and `interval-bounds` originate in G11 T1. Term 2 contexts specialize several definitions. In [catalog lines 87–96](highlights_catalog.tex#L87), `\HighlightEffectiveField` uses a context field when that key exists and otherwise falls back to its concept. An explicitly empty `examples` field is not a request to invent examples. A context's grouped `notation` is also not a collection of separately addressable symbol records.

All file links below are relative to this report. Stable identifiers and practice labels are the primary source anchors; `#L…` references give additional source locations, not rendered-page assertions. In tables, abbreviated record prefixes are explicitly defined and suffixes name the complete record IDs. Origin links identify every contributing report; the inventory supplies each report's practice link. Each classification retains its existing local workaround. Proposed changes are recommendations only; only this consolidated report is written. No compilation, rendering, tests, validators or validation helpers are part of this work.

## 2. Actionable ecosystem gaps, grouped by responsibility

### A1. G10 T2 mathematical records: an explicit discrete CDF jump identity

**Origin and affected notation:** [R10.2](../../grade10/term_2/1-practice_activities/G10_T2_L1_C2_practice_activity_highlights_gaps.md), G10 C2, `F_X(a)-F_X(a^-)=p_X(a)`. The reusable missing capability is a directly retrievable statement connecting a point mass to a CDF jump. It is distinct from storing a graph's translated-shadow convention.

**Authoritative anchors:** [G10 T2 lines 445–470](highlights_g10_t2.tex#L445), `g10-t2-c2-coordinated-10-mass` and `g10-t2-c2-coordinated-10-cum`; inherited `cumulative-probability` at [G11 T1 line 40](highlights_g11_t1.tex#L40). These define the mass, inclusive CDF and strict left limit, but do not explicitly store their difference identity. The [G10 C2 practice](../../grade10/term_2/1-practice_activities/G10_T2_L1_C2_practice_activity.tex#L91), `\cTwoConnectionReading`, states that identity explicitly; its `tab:notation-reference` includes a separate jump-expression row.

**Existing support and local handling:** mass and cumulative wrappers already distinguish `p_X(a)` from the two cumulative heights. The local row uses those wrappers and the payment example's `1-0.25=0.75`; the local macro explains the stacked graphs. No new probability role is needed.

**Smallest proposed change:** add the general discrete jump identity to the C2 cumulative context's definition. Add a separately selectable context under the existing mass concept only if independent jump-row selection is actually required. Do not register the payment values or graphical arrows as shared mathematics.

**Uncertainty:** the identity follows from existing definitions, so this is missing explicit reusable exposition, not missing underlying probability semantics. The evidence supports the identity addition; it does not establish a need for a graph renderer, translated-shadow field or new concept.

### A2. G11 T2 record and compatibility responsibility: population size is not the population group

**Origin and affected notation:** [R11.1](../../grade11/term_2/1-practice_activities/G11_T2_L1_C1_practice_highlights_gaps.md), G11 C1, `\mathcal P` versus `N`, and `n` as the sample count. The mathematical distinction exists; what is unavailable is an independently selectable population-size record with a size-specific treatment consistent with the practice's count usage.

**Authoritative anchors:** [G11 T2 line 13](highlights_g11_t2.tex#L13), concept `population`, explicitly defines `N` as the number of units but assigns the grouped concept `group.population`; [line 756](highlights_g11_t2.tex#L756), `g11-t2-c1-coordinated-11-population`, wraps both `\mathcal P` and `N` with `\HLPopulationGroup`. `g11-t2-c1-coordinated-11-size` at line 768 is specifically the sample/trial count `n`. [Term 2 compatibility lines 89–114](highlights_compat_ttwo.tex#L89), `practicehighlightlegend@G11-T2-C1`, already has separate population and size rows but gives its fixed `N` cell the population palette treatment. [Roles](highlights_roles.tex), `\HLObservationCount` / `count.design`, provide the existing count treatment.

**Local handling:** [G11 C1 practice](../../grade11/term_2/1-practice_activities/G11_T2_L1_C1_practice.tex#L71), `subsec:c1-population-and-sample` and `tab:notation-reference`, uses `\HLObservationCount{N}` and `\HLObservationCount{n}`, identifies the full-list size as unspecified and the sample size as 40, and leaves the supported special opening helper intact. Phrases describing a whole selected group retain `\HLSampleGroup`.

**Smallest proposed change:** introduce a population-size context with an explicit `N` definition and existing count wrapper, rather than a new color or dedicated role. If that convention is adopted, align the compatibility helper's fixed size cell with it while preserving its two-panel layout. `count.design` currently emphasizes selected/trial counts, so its documented scope must be considered rather than silently redefining `N` as sample size.

**Uncertainty/conflict:** the opening has a distinct size row already; claiming that population-size mathematics or the special layout is absent would be false. The conflict is between its current semantic treatment and the practice's count treatment. A new population-size role is not demonstrated as necessary, and a change in convention would require an explicit ecosystem decision.

### A3. Shared mean fields and compatibility specialization: avoid simulation qualification in unrelated C1/C3 definitions

**Origins:** [R11.1](../../grade11/term_2/1-practice_activities/G11_T2_L1_C1_practice_highlights_gaps.md) and [R11.3](../../grade11/term_2/1-practice_activities/G11_T2_L1_C3_practice_highlights_gaps.md), G11 C1/C3, `\mu`, `\mu_{\mathrm{1D}}`, `\mu_{\mathrm{2D}}`. R11.3 describes generic meaning/specialization rather than asserting a new missing mean concept.

**Authoritative anchors:** [G11 T2 line 794](highlights_g11_t2.tex#L794), `g11-t2-c1-coordinated-11-meanpop`, and [line 1137](highlights_g11_t2.tex#L1137), `g11-t2-c3-coordinated-11-meanpop`, store `\CoordinatedPopulationMeanMeaning` as `brief` and `definition`, but a separate generic `meaning` field. [Term 2 compatibility line 227](highlights_compat_ttwo.tex#L227) defines that macro as “Fixed mean of the defined population; simulation mean is supplied separately.” The C1/C3 coordinated legend helpers locally redefine it to their contexts' `meaning` at [lines 688 and 742](highlights_compat_ttwo.tex#L688). A direct field lookup outside those helper groups does not inherit that local redefinition. The inherited [population-mean concept](highlights_g11_t1.tex#L148) already supplies a generic parameter definition, but an existing context `definition` takes precedence.

**Local handling:** both practices retrieve the C1/C3 context `meaning` for their population-mean rows. C1 uses `subsec:c1-population-and-sample` / `subsec:c1-quick-check`; C3 uses `subsec:c3-transport-example` / `subsec:c3-quick-check`. Their existing mean wrappers suffice.

**Smallest proposed change:** give only the affected C1/C3 contexts a generic population-mean `brief` and `definition`, or remove the unsuitable override where concept fallback is appropriate. Keep the simulation qualification in C2, where it is relevant. No new mathematical concept is needed.

**Uncertainty:** current local handling and the coordinated helpers already avoid the irrelevant qualification. This is a reusable-field specialization issue, not evidence of incorrect numerical examples or a missing population-mean meaning.

## 3. Notation-granularity limitations

### G1. Catalog/selection/table responsibility: concept unions cannot automatically split notation

**Origins:** [R10.1](../../grade10/term_2/1-practice_activities/G10_T2_L1_C1_practice_activity_highlights_gaps.md), [R10.2](../../grade10/term_2/1-practice_activities/G10_T2_L1_C2_practice_activity_highlights_gaps.md), [R10.3](../../grade10/term_2/1-practice_activities/G10_T2_L1_C3_practice_activity_highlights_gaps.md), [R11.1](../../grade11/term_2/1-practice_activities/G11_T2_L1_C1_practice_highlights_gaps.md), [R11.2](../../grade11/term_2/1-practice_activities/G11_T2_L1_C2_practice_highlights_gaps.md), [R11.3](../../grade11/term_2/1-practice_activities/G11_T2_L1_C3_practice_highlights_gaps.md). All six practices need distinct rows at `tab:notation-reference`; the mathematical needs within those rows remain separate in G2–G12 below.

**Authority:** [catalog](highlights_catalog.tex), `hl_union_context:n` and `hl_collect_selected:`, collect effective fields keyed by concept; [tables line 49](highlights_tables.tex#L49), `hl_union_print:n` / `\SpecificHighlightUnionRows`, print one row per collected concept. They cannot extract an independent definition for each symbol from a compound field or infer local example interpretations. `\HighlightForEachMember` already exposes reference members, but neither it nor `\HighlightContextField` splits one member's notation field.

**Existing handling:** explicit local rows, applicable field lookups and shared `\HighlightDetailedTable` / `\COneToneDetailedHeaders` provide the expanded references. G10 C1/C2 use local longtables; the other practices use the shared detailed presentation. Concise legends retain their intended grouping.

**Smallest proposal:** none is needed to support the current local tables. If reusable automatic symbol rows become a requirement, add narrowly scoped notation contexts and an opt-in member-based rendering path using the existing member iterator. Merely adding same-concept contexts to a union will still merge them. Do not replace concept unions or create artificial concepts solely to force row breaks. The reports establish an automation limitation, not missing four-column, header or pagination support.

### G2. G10 C1/C2: variable, value, outcome and sample-space fields

**Origins/documents:** [R10.1](../../grade10/term_2/1-practice_activities/G10_T2_L1_C1_practice_activity_highlights_gaps.md), G10 C1, and [R10.2](../../grade10/term_2/1-practice_activities/G10_T2_L1_C2_practice_activity_highlights_gaps.md), G10 C2. Required distinctions include `\omega` / `\Omega`, `X` / `x` / `X(\omega)`, C1 `F`, `E`, `C`, `Y`, `y`, `Z`, `z` and their assigned values. An indicator's particular condition is local; a random variable and one of its values are mathematically different objects.

**Authority/support:** [G10 T2](highlights_g10_t2.tex#L273), `g10-t2-c1-coordinated-10-outcome`, `-variable`, `-second`, `-third`; [line 420](highlights_g10_t2.tex#L420), `g10-t2-c2-coordinated-10-variable`; concepts `outcome-space`, `second`, `third`, and inherited [random-variable](highlights_g11_t1.tex#L4). The records define the meanings but group notation or inherit broader definitions. `third` explicitly defines an indicator; `second` permits context-dependent variables rather than prescribing C1's electronic-payment condition.

**Local handling:** individual rows in the two practices' `tab:notation-reference`, with existing `\GTenHLOutcome`, `\GTenHLValue`, `\GTenHLSecond` and `\GTenHLThird`, plus effective briefs where applicable. C1 links `subsec:t2-c1-given-outcomes` and `subsec:t2-c1-independent-outcomes`; C2 links `prob:payment-intro` and `ex:refund-intro`.

**Smallest proposal/uncertainty:** separately addressable generic outcome/space and variable/value fields only if shared symbol-row reuse is needed. No new indicator role or record for every numerical assignment is justified; fee, electronic/card and first-visitor definitions remain local (L1).

### G3. G10 C1/C3: supports retain the full variable subscript

**Origins:** [R10.1](../../grade10/term_2/1-practice_activities/G10_T2_L1_C1_practice_activity_highlights_gaps.md), C1 `S`, `S_F`, `S_E`, `S_C`, `S_X`, `S_Y`, `S_Z`; [R10.3](../../grade10/term_2/1-practice_activities/G10_T2_L1_C3_practice_activity_highlights_gaps.md), C3 `S_X`, `S_Y`, `S_{Y_i}`. Renamed supports and indicator/monetary supports share positive-mass membership, but their units and endpoint evaluations must not be collapsed.

**Authority/support:** [G10 T2 line 31](highlights_g10_t2.tex#L31), `discrete-support`, already specifies positive probability, variable units and parameter endpoints; contexts `g10-t2-c1-coordinated-10-support` at [line 310](highlights_g10_t2.tex#L310) and `g10-t2-c3-coordinated-10-support` at [line 557](highlights_g10_t2.tex#L557) expose `S_X`, not each requested variant.

**Local handling:** C1's `subsec:t2-c1-notation-reference` gives separate support rows, applies the primary/secondary/tertiary wrapper matching the variable and uses `S` in normalization prose. C3's `tab:notation-reference` uses `\Indicator` and `\Money`, gives `S_X={0,1}` only for `0<p<1`, and retains only state 0 at `p=0` or state 1 at `p=1`; the monetary support retains only the corresponding positive-mass payoff. The four initial monetary supports remain attached to `ex:intro-one` and `ex:intro-two`.

**Smallest proposal/uncertainty:** optional generic support variants or a reusable positive-mass specialization under the existing concept; do not add concepts for mere renaming. The endpoint rule is supported already. Fixed support sets and USD values are local, and C3's distinct opposite-sign payoffs are a document assumption, not a universal transformation condition.

### G4. G10 C1/C3: point-mass records, distinct from transformations and cumulative probabilities

**Origins:** [R10.1](../../grade10/term_2/1-practice_activities/G10_T2_L1_C1_practice_activity_highlights_gaps.md), C1 `p_F(f)`, `p_X(x)`, `p_Y(y)`, `p_Z(z)`; [R10.3](../../grade10/term_2/1-practice_activities/G10_T2_L1_C3_practice_activity_highlights_gaps.md), C3 `m_X(x)` and `m_{Y_i}(y)`.

**Authority/support:** [G10 T2 line 346](highlights_g10_t2.tex#L346), `g10-t2-c1-coordinated-10-mass`, explicitly defines `p_X(x)=m_X(x)=P(X=x)` despite its concept name `event-probability`; [line 607](highlights_g10_t2.tex#L607), `g10-t2-c3-coordinated-10-mass`, already displays both indicator and monetary PMFs in one context. These context definitions specialize the broader inherited [event-probability](highlights_g11_t1.tex#L31), whose continuous-model qualification must not replace the discrete definition.

**Local handling:** separate rows in the C1/C3 notation references reuse `\GTenHLProbability` / `\HLProbability`. C1 supplies variable-specific inputs and grouped outcome probabilities. C3 states input units separately from unitless output, both state masses and zero elsewhere; `m_{Y_i}` assigns mass to money, whereas `f_i` assigns money to a state. Neither is a density or a CDF.

**Smallest proposal/uncertainty:** optional indicator and transformed-variable mass contexts under existing support if separately selectable fields are needed. No new PMF concept or probability wrapper is missing. Numerical masses and C3's particular two-payoff specialization remain local.

### G5. G10 C2/C3: CDF, cutoff and left-limit granularity

**Origins:** [R10.2](../../grade10/term_2/1-practice_activities/G10_T2_L1_C2_practice_activity_highlights_gaps.md), C2 `F_X(x)`, `F_X(a)`, `F_X(a^-)`, including concrete `F_X(0.5)`, `F_X(1)`, `F_X(1^-)` and mass `p_X(1)`; [R10.3](../../grade10/term_2/1-practice_activities/G10_T2_L1_C3_practice_activity_highlights_gaps.md), C3 `F_X(t)` versus `F_{Y_i}(t)`.

**Authority/support:** [G10 T2 line 458](highlights_g10_t2.tex#L458), `g10-t2-c2-coordinated-10-cum`, distinguishes inclusive and strict probabilities in one context; `g10-t2-c2-coordinated-10-cutoff` permits real cutoffs in variable units. [Line 620](highlights_g10_t2.tex#L620), `g10-t2-c3-coordinated-10-cum`, groups indicator and monetary CDFs and uses the inclusive/left-limit definition. The explicit jump relation is separately treated in A1.

**Local handling:** both practices use individual rows and `\HLCumulativeProbability`. C2 explains unsupported cutoffs without interpreting them as supported values: payment `F_X(0.5)=0.25`, `F_X(1)=1`, `F_X(1^-)=0.25`, but `p_X(1)=0.75`; refunds use `F_X(1)=0.70` versus `p_X(1)=0.50`. C3 gives right-continuous two-state CDFs, keeps unitless indicator thresholds distinct from USD thresholds, and orders monetary values numerically rather than by state label. Labels: C2 `prob:payment-intro`, `ex:refund-intro`; C3 `ex:intro-one`, `ex:intro-two`, all with `tab:notation-reference`.

**Smallest proposal/uncertainty:** optional independent inclusive/left-limit and indicator/monetary CDF contexts under the current concept. The source already supports the underlying meanings. Do not register concrete evaluations or claim a new cumulative role is needed; C3 plateau heights depend on the local payoff ordering.

### G6. G10 C3: transformation function versus state payoff

**Origin:** [R10.3](../../grade10/term_2/1-practice_activities/G10_T2_L1_C3_practice_activity_highlights_gaps.md), G10 C3, `Y`, `Y_i`, `f`, `f_i`, `f_i(0)`, `f_i(1)`.

**Authority/support:** [G10 T2 line 595](highlights_g10_t2.tex#L595), `g10-t2-c3-coordinated-10-second`, exposes `Y_i=f_i(X)`; [line 658](highlights_g10_t2.tex#L658), `g10-t2-c3-coordinated-10-transform`, groups `f_i(0),f_i(1)`. Concepts `second` and `transform` already explain transformations and state payoffs, but C3 has no standalone `f` / `f_i` fields or separate state-0/state-1 definitions.

**Local handling:** the practice's `tab:notation-reference` gives six rows; `\Money` treats monetary outputs and variables, while function names remain contextual plain notation. `ex:intro-one` and `ex:intro-two` supply the binary domain, USD codomain and fixed payoff mappings. No PMF/CDF role is assigned to `f_i`.

**Smallest proposal/uncertainty:** if reusable rows are needed, add generic function and state-payoff subcontexts within existing transformation support. Do not conflate a function with its evaluated monetary output. A universal binary domain, USD codomain or opposite-sign requirement is not established by the general ecosystem definitions and should remain local.

### G7. G10 C3: expectation operator versus expected monetary value

**Origin:** [R10.3](../../grade10/term_2/1-practice_activities/G10_T2_L1_C3_practice_activity_highlights_gaps.md), `\mathbb E` versus `\mathbb E[Y_i]`.

**Authority/support:** [G10 T2 line 633](highlights_g10_t2.tex#L633), `g10-t2-c3-coordinated-10-expected`, displays only the expected value but explicitly distinguishes the operator from an event/indicator named `E`. The inherited [expected-value](highlights_g11_t1.tex#L139) also recognizes the operator's own role; the Term 2 context supplies the discrete weighted-average definition.

**Local handling:** separate operator/result rows use `\ExpectedValue`, `\Money` and the effective context definition at `tab:notation-reference`. Introductory formulas, USD values, periods and long-run interpretations remain linked to `ex:intro-one` / `ex:intro-two`.

**Smallest proposal/uncertainty:** an optional operator-only notation context if independent selection is needed. The operator's meaning and wrapper already exist; no new expectation concept or numerical example record is justified.

### G8. G11 C1: samples, sizes and indexed parameter/statistic variants

**Origin:** [R11.1](../../grade11/term_2/1-practice_activities/G11_T2_L1_C1_practice_highlights_gaps.md). Preserve the full symbols: populations `\mathcal P`, `\mathcal P_{\mathrm{1D}}`, `\mathcal P_{\mathrm{2D}}`; whole samples `X`, `X_1`, `X_2`, `X_i`, `X_{\mathrm{2D}}`; sizes `n`, `n_1`, `n_2`, `n_i`; population means `\mu`, `\mu_{\mathrm{1D}}`, `\mu_{\mathrm{2D}}`; sample means `\bar x`, `\bar x_1`, `\bar x_2`, `\bar x_i`, `\bar x_{\mathrm{2D}}`. The separate `N` treatment is A2, not an indexed-sample gap.

**Authority/support:** [G11 T2 lines 744–820](highlights_g11_t2.tex#L744), `g11-t2-c1-coordinated-11-sample`, `-population`, `-size`, `-meanpop`, `-meansample`, and concepts `sample`, `population`, `design-count`, `sample-mean`. Whole sample `X_i` and indexed mean `\bar x_i` already occur. `design-count` recognizes indexed `n_i`, though the C1 context overrides its definition with a shorter sample-size statement. The variants are not individually selectable records.

**Local handling:** `tab:notation-reference` supplies explicit rows with `\HLSampleGroup`, `\HLPopulationGroup`, `\HLObservationCount`, `\HLPopulationMean` and `\HLSampleMean`. `subsec:c1-quick-check` distinguishes draw indices 1/2 from one-/two-district scope 1D/2D. Redraws can change statistics while preserving the parameter; redefining scope changes which parameter is targeted, without guaranteeing a different numerical mean.

**Smallest proposal/uncertainty:** optional generic sample/indexed-size/indexed-mean fields; no separate shared concept for each district or draw. Existing grouped notation is real support. The absence is fine-grained retrieval, and the district semantics must remain local.

### G9. G11 C2/C3: total excluded area, each tail and confidence

**Origins:** [R11.2](../../grade11/term_2/1-practice_activities/G11_T2_L1_C2_practice_highlights_gaps.md), C2 `\alpha` versus `\alpha/2`; [R11.3](../../grade11/term_2/1-practice_activities/G11_T2_L1_C3_practice_highlights_gaps.md), C3 `(1-C)/2`.

**Authority/support:** [G11 T2 line 990](highlights_g11_t2.tex#L990), `g11-t2-c2-coordinated-11-tail`, and [line 1216](highlights_g11_t2.tex#L1216), `g11-t2-c3-coordinated-11-tail`, explicitly define `\alpha=1-C` as total excluded area and `\alpha/2` as each equal tail, using `\HLTailArea`. The [roles module](highlights_roles.tex) has `tail`, confidence and critical-value treatments but no dedicated significance role.

**Local handling:** C2's local `\CtwoSignificance` aliases `\HLTailArea`; independent rows retain `0.05` versus `0.025`. C3 keeps the actual `(1-C)/2` expression in its reference and its introductory paragraph following “Relationships and critical values,” rather than introducing alpha into those examples. Both retain distinct confidence and critical-value treatments.

**Smallest proposal/uncertainty:** optional notation contexts for total excluded area and each-tail area, including the confidence expression. A significance alias could improve naming consistency if needed; a new palette or role is not justified by these sources. Lack of a dedicated significance role is true, but does not imply lack of semantic support. Historical conflicting treatment is retained in S4 below.

### G10. G11 C2/C3: endpoints and intervals, including reported values

**Origins:** [R11.2](../../grade11/term_2/1-practice_activities/G11_T2_L1_C2_practice_highlights_gaps.md), C2 `L`, `U`, `\mathrm{CI}`, `L_{\rm rep}`, `U_{\rm rep}`, `\mathrm{CI}_{\rm rep}`; [R11.3](../../grade11/term_2/1-practice_activities/G11_T2_L1_C3_practice_highlights_gaps.md), C3 `L` and `U`.

**Authority/support:** [G11 T2 line 1028](highlights_g11_t2.tex#L1028), `g11-t2-c2-coordinated-11-bounds`; `...-reported` at [line 1053](highlights_g11_t2.tex#L1053); C3 `g11-t2-c3-coordinated-11-bounds` at [line 1254](highlights_g11_t2.tex#L1254). Grouped definitions already distinguish lower/upper bounds and interval; concept `reported` distinguishes reporting rounding. `width` / `reportedwidth` are separate records, not endpoint aliases.

**Local handling:** explicit rows use `\CtwoEndpoint`, the local C2 `\CtwoCI` alias and existing bounds wrappers. Definitions state subtraction for `L`, addition for `U` and interval construction separately. C2's `subsec:c2-comprehensive`, Step 4, keeps calculated 99% endpoints `(34.848,45.152)` and width `10.304` minutes distinct from reported `(34.85,45.15)` and width `10.30`. C3's `subsec:c3-quick-check` retains both confidence-level endpoint pairs.

**Smallest proposal/uncertainty:** optional lower/upper/interval subcontexts and their reported counterparts under existing concepts, only for reusable independent selection. No new bounds role is required, and the grouping does not erase existing mathematical distinctions. Margin `\mathrm{MoE}` and full width `W=U-L=2\mathrm{MoE}` remain separate.

### G11. G11 C2: covering counts versus observed coverage

**Origin:** [R11.2](../../grade11/term_2/1-practice_activities/G11_T2_L1_C2_practice_highlights_gaps.md), `N_{\rm cover}(C)`, `N(C)`, `\mathrm{Cov}(C)`.

**Authority/support:** [G11 T2 line 87](highlights_g11_t2.tex#L87), concept `coverage`, defines the covering numerator, total denominator and percentage, expressly excluding population-size meaning for `N(C)`; [line 1077](highlights_g11_t2.tex#L1077), `g11-t2-c2-coordinated-11-coverage`, groups all three. Existing coverage wrappers suffice; the limitation is independent record selection and fields for each quantity.

**Local handling:** C2's `\CtwoCoverCount` and `\CtwoTotalCount` use the coverage treatment while the argument `C` retains confidence treatment. `tab:notation-reference`, `subsec:c2-coverage-example` and worked Step 5 retain separate count and ratio rows: 4 covering intervals out of 5, or 80%. Nominal confidence is 95%; `E_{\rm abs}(C)` is the 15-percentage-point gap, not margin of error or relative percentage error.

**Smallest proposal/uncertainty:** optional numerator, denominator and percentage contexts under coverage. Do not reuse A2's population-size record for `N(C)` or turn counts into a nominal confidence measure. All three mathematical meanings already exist.

### G12. G11 C2/C3: normal CDF, inverse cutoff, standardized variable and inverse argument

**Origins:** [R11.2](../../grade11/term_2/1-practice_activities/G11_T2_L1_C2_practice_highlights_gaps.md), C2 `\Phi(z)` / `\Phi^{-1}(u)`; [R11.3](../../grade11/term_2/1-practice_activities/G11_T2_L1_C3_practice_highlights_gaps.md), C3 `Z`, `\Phi(z)`, `\Phi^{-1}(p)`, `p`.

**Authority/support:** [G11 T2 line 105](highlights_g11_t2.tex#L105), concept `normal`, defines `Z\sim N(0,1)`, the left-tail probability and inverse domain `0<u<1`. Contexts `g11-t2-c2-coordinated-11-normal` at [line 1105](highlights_g11_t2.tex#L1105) and `g11-t2-c3-coordinated-11-normal` at [line 1279](highlights_g11_t2.tex#L1279) group forward and inverse notation, with `u` as argument. Embedded wrappers already distinguish cumulative output/input from inverse cutoff despite the concept's overall cumulative role.

**Local handling:** separate reference rows retain `\HLCumulativeProbability` for areas and the inverse input, `\HLCriticalValue` for the cutoff. C2 worked Step 2 retains `\Phi(1.960)\approx0.975` and `\Phi^{-1}(0.975)\approx1.960`. C3's introductory paragraph and `tab:notation-reference` preserve `p`, explicitly a left-tail inverse input, not a population proportion; `Z` is a unitless reference variable, not monetary spending.

**Smallest proposal/uncertainty:** optional distinct forward/inverse/variable/input contexts with their existing roles; preserve argument spelling when used locally. The mathematical support and mixed embedded treatments already exist. No new normal-distribution concept or forced renaming of C3's `p` is needed.

### G13. G11 C3: functional dependence of SE, critical value and margin

**Origin:** [R11.3](../../grade11/term_2/1-practice_activities/G11_T2_L1_C3_practice_highlights_gaps.md), three distinct needs: `\mathrm{SE}(n)`, `z^*(C)` and `\mathrm{MoE}(n,C)`.

**Authority/support:** [G11 T2 line 1191](highlights_g11_t2.tex#L1191), `g11-t2-c3-coordinated-11-se`, displays base `SE` but its definition already mentions `SE(n)`; [line 1229](highlights_g11_t2.tex#L1229), `...-critical`, describes confidence-dependent cutoffs; [line 1242](highlights_g11_t2.tex#L1242), `...-margin`, uses the general `margin` definition. The [G11 C3 practice](../../grade11/term_2/1-practice_activities/G11_T2_L1_C3_practice.tex), “Relationships and critical values,” explicitly gives `SE(n)=\sigma/\sqrt n`, `z^*(C)=\Phi^{-1}((1+C)/2)` and `MoE(n,C)=z^*(C)\sigma/\sqrt n` under its known-SD model.

**Local handling:** three function rows use existing SE, size, critical, confidence and margin wrappers, keeping relationships in definition cells. Example 1 varies size at fixed confidence; Example 2 varies confidence at fixed size/SE.

**Smallest proposal/uncertainty:** optional function-notation contexts for each distinct dependence, without merging SE, critical value and margin into one record. The base meanings already exist. Known fixed `\sigma`, independent sampling and the normal approximation are local model assumptions; the general SE definition also covers estimates and proportions, so the specialized formula must not replace it universally.

## 4. Local-only requirements

### L1. G10 C1/C2 example meanings, labels and elementary reading notation

**Origins:** [R10.1](../../grade10/term_2/1-practice_activities/G10_T2_L1_C1_practice_activity_highlights_gaps.md) and [R10.2](../../grade10/term_2/1-practice_activities/G10_T2_L1_C2_practice_activity_highlights_gaps.md).

**Source anchors and affected notation:** [G10 C1 practice](../../grade10/term_2/1-practice_activities/G10_T2_L1_C1_practice_activity.tex), `subsec:t2-c1-given-outcomes`, `subsec:t2-c1-independent-outcomes`, `subsec:t2-c1-notation-reference`; [G10 C2 practice](../../grade10/term_2/1-practice_activities/G10_T2_L1_C2_practice_activity.tex#L124), `prob:payment-intro`, `ex:refund-intro`, `tab:notation-reference`. Ecosystem counterparts are [G10 T2](highlights_g10_t2.tex), C1/C2 coordinated `-outcome`, `-variable`, `-support`, `-mass`, C1 `-second`, `-third`, `-ops`, C2 `-cum`, all with empty `examples`.

**Precise local requirement and handling:** C1 defines payment methods, fee `F`, electronic indicator `E`, card indicator `C`, ordered visitor decisions `B`/`N`, buyer count `X`, revenue `Y=5X` and first-visitor indicator `Z`. Buying remains 0.4, passing 0.6; fee units, indicator conditions and visitor order stay in linked local meanings. C2 independently defines its payment fee and refund-count `X`; its payment probabilities are 0.25/0.45/0.30, not C1's four-method 0.1/0.2/0.3/0.4 model. Equal letter names do not identify the same random variable across examples.

C1's `\in` membership, selection colon `:`, `B`/`N` labels and sum-specific explanation remain separate local rows. `\sum` already exists in `mathematical-operations` / `g10-t2-c1-coordinated-10-ops`; the local PMF formula explains adding mutually exclusive outcomes once each and an empty sum of zero. Decision labels use the outcome wrapper; membership, colon and sigma remain plain. The shared `event` definition also mentions an event named `B`, which must not redefine this decision label.

**Smallest proposal/uncertainty:** none for these examples or problem labels. Missing standalone elementary-notation fields do not establish a new semantic-role need. Generic notation reuse could be considered separately if demonstrated elsewhere; the reports do not justify promoting these example meanings or filling their empty example fields.

### L2. G10 C2 graph correspondence and translated shadows

**Origin:** [R10.2](../../grade10/term_2/1-practice_activities/G10_T2_L1_C2_practice_activity_highlights_gaps.md). The report combines the reusable identity in A1 with a graph-specific requirement; these are separated here.

**Authority/local handling:** [G10 C2 practice line 91](../../grade10/term_2/1-practice_activities/G10_T2_L1_C2_practice_activity.tex#L91), `\cTwoConnectionReading`, and “From bars to stems” specify matching axes/scales, isolated PMF stems, vertically translated shadows from `F_X(a^-)` to `F_X(a)`, and curved midpoint-correspondence arrows. Their paths do not represent additional probabilities. Existing mass/CDF roles and local graph settings support the explanation; [G10 T2 C2 mass/cum records](highlights_g10_t2.tex#L445) do not encode this particular drawing convention.

**Smallest proposal/uncertainty:** no shared graph field, role, palette or renderer change is justified. The lack of a translated-shadow record is real as a storage observation, but this visualization is document-specific and should remain local. This does not cancel the narrower explicit identity proposal in A1.

### L3. G10 C3 binary monetary specializations, loss events and break-even interpretations

**Origin:** [R10.3](../../grade10/term_2/1-practice_activities/G10_T2_L1_C3_practice_activity_highlights_gaps.md), `\{Y_i<0\}`, payoff/support/PMF/CDF values, `\mathbb E[Y_i]`, `p_i^*`.

**Authority:** [G10 C3 practice](../../grade10/term_2/1-practice_activities/G10_T2_L1_C3_practice_activity.tex), `ex:intro-one` (clothing weekend), `ex:intro-two` (coffee-shop day), “Binary models and distributions” and `tab:notation-reference`; [G10 T2](highlights_g10_t2.tex#L532), `g10-t2-c3-coordinated-10-event`, `-support`, `-second`, `-mass`, `-cum`, `-expected`, `-break`, `-transform`. Concept `event` already supports conditions; `discrete-support` already handles positive-mass endpoints, and `break` already defines each individual threshold.

**Precise local requirement and handling:** the practice gives a separate `\{Y_i<0\}` row using `\HLMathEvent`. Clothing maps loss to `E^c`, initially 0.6, with supports `S_{Y_1}={-20,60}` and `S_{Y_2}={-40,120}` USD. Coffee maps loss to `E`, initially 0.1, with supports `S_{Y_1}={-20,100}` and `S_{Y_2}={-10,60}` USD. Thus monetary CDF middle plateaus are 0.6 for clothing and 0.1 for coffee, while indicator CDF plateaus are 0.6 and 0.9. These are different mathematical quantities despite sharing wrappers.

The local functions retain opposite-sign fixed payoffs, both state masses, zero elsewhere, ordered right-continuous CDFs and endpoint support changes. Initial expectations remain 12/24 USD per weekend and 88/53 USD per day. Break-even probabilities remain `p_1^*=p_2^*=1/4` for clothing, versus `p_1^*=5/6`, `p_2^*=6/7` for coffee; the expectation's sign direction differs between those examples. Complete subscripts identify alternatives, not interchangeable generic values.

**Smallest proposal/uncertainty:** no shared loss-event concept, numeric example record or universal financial interpretation of “success.” A generic event can already express loss. Reusable notation variants are addressed separately in G3–G7; their addition must not elevate USD, opposite signs, those periods or the particular loss-state mappings to ecosystem-wide assumptions.

### L4. G11 C1 introductory interpretations and intentionally absent values

**Origin:** [R11.1](../../grade11/term_2/1-practice_activities/G11_T2_L1_C1_practice_highlights_gaps.md). Affected notation includes all G8 indices plus `y_j`, `s`, `\sigma`, `s^2`, `\sigma^2`, `p`, `\hat p`.

**Authority/local handling:** [G11 C1 practice lines 64–136](../../grade11/term_2/1-practice_activities/G11_T2_L1_C1_practice.tex#L64), `subsec:c1-population-and-sample`, `subsec:c1-quick-check`, `tab:notation-reference`; [G11 T2 C1 contexts](highlights_g11_t2.tex#L744), all with empty `examples`. Local rows link electricity-bill, redraw and district-scope meanings; 40-bill draws and the stated sample mean of 210 thousand COP are reused where present. `s` estimates individual-value population spread `\sigma`; `\hat p` estimates population proportion `p` for bills paid on time. Their numeric values are not supplied.

The variance pair is present in `g11-t2-c1-coordinated-11-variance` / `-varsample` and the special opening legend, but absent from the introductory narrative. Both rows are retained with shared definitions and explicit statements that no introductory interpretation/value is assigned. Do not invent squared bill spreads, values for unspecified `N`, or generic indexed spread/proportion examples.

**Smallest proposal/uncertainty:** none for bill-specific meanings, district names or absent values. Empty examples and the lack of a narrative variance example are not ecosystem gaps. The narrower grouping and mean-field limitations are G8 and A3.

### L5. G11 C2/C3 contextual models, controlled comparisons and graph roles

**Origins:** [R11.2](../../grade11/term_2/1-practice_activities/G11_T2_L1_C2_practice_highlights_gaps.md) and [R11.3](../../grade11/term_2/1-practice_activities/G11_T2_L1_C3_practice_highlights_gaps.md).

**Authority/local handling:** [G11 C2 practice](../../grade11/term_2/1-practice_activities/G11_T2_L1_C2_practice.tex), `subsec:c2-cycling-example`, `subsec:c2-coverage-example`, `subsec:c2-comprehensive`, `tab:notation-reference`; [G11 C3 practice](../../grade11/term_2/1-practice_activities/G11_T2_L1_C3_practice.tex), `subsec:c3-transport-example`, `subsec:c3-quick-check`, “Relationships and critical values,” `tab:notation-reference`. Corresponding [G11 T2](highlights_g11_t2.tex#L900) C2/C3 contexts have empty `examples` but already supply means, sample size, SD, SE, confidence, cutoff, margin, bounds and width support.

C2 keeps unknown original `\mu` separate from known simulation `\mu_{\rm sim}=41` minutes, the observed estimate `\bar x=40` minutes, individual SD 14 minutes and SE 2 minutes at `n=49`. Counts, 80% observed coverage, nominal 95%, percentage-point error, and calculated/reported rounding remain local. `CtwoCentralArea`, `CtwoCoverLine`, `CtwoMissLine` and disabled-highlight branches describe local graph status; covering/missing lines are not population-mean roles.

C3 preserves a known fixed individual SD 20 thousand COP and fixed estimate 60 thousand COP for its controlled comparisons. Example 1 changes 100 to 400 households at 95% confidence, changing SE 2 to 1 and margin 3.920 to 1.960. Example 2 fixes `n=100`, SE 2, changes 90% to 99%, and retains critical values 1.645/2.576, margins 3.290/5.152, endpoint pairs `(56.710,63.290)` / `(54.848,65.152)` and full widths 6.580/10.304, all monetary quantities in thousand COP. Fixed centres isolate uncertainty changes; actual sample estimates may vary. Sampling, independence, known-SD, normal-model assumptions and the stated rounding policy stay local.

**Smallest proposal/uncertainty:** no registered cycling/transport meanings are required. Reuse the supported fields and local fourth-column explanations. C2's organizational choice to list `n` and SE under “Sample statistics” is explicitly a document convention, not an ecosystem-wide redefinition of a design count or of standard error. Broader course definitions should not be narrowed globally to these known-SD examples.

## 5. Already-supported or unresolved claims

### S1. Simulation support exists; C2 selection is the narrower limitation

**Origin:** [R11.2](../../grade11/term_2/1-practice_activities/G11_T2_L1_C2_practice_highlights_gaps.md). [G11 T2 line 179](highlights_g11_t2.tex#L179), concept `simulation`, independently defines `\mu_{\rm sim}` as the supplied simulation reference mean; `g11-t2-intro-simulation` at [line 2909](highlights_g11_t2.tex#L2909) exposes it in the wider introduction. [Line 900](highlights_g11_t2.tex#L900), `g11-t2-c2-coordinated-11-meanpop`, already includes `\mu` and `\mu_{\rm sim}` together. [Line 4000](highlights_g11_t2.tex#L4000), `G11-T2-C2-coordinated`, selects that combined context, not a standalone simulation member.

**Reconciliation/local handling:** the report's separate-selectability complaint is valid, but a missing simulation concept claim is not. C2 supplies two explicit mean rows and the separate-population explanation locally. If separate coordinated selection is required, the smallest change is a C2-specific simulation context under the existing concept and a narrowly scoped membership adjustment; do not append an entire unrelated introduction selection. No new mean role or numeric simulation example is needed. Whether a separate concise row is desirable remains a presentation decision, not a demonstrated missing capability.

### S2. `y_j` observation support already exists

**Origin:** [R11.1](../../grade11/term_2/1-practice_activities/G11_T2_L1_C1_practice_highlights_gaps.md), which describes the absence of a symbol-specific `y_j` definition record. [G11 T2 line 782](highlights_g11_t2.tex#L782), `g11-t2-c1-coordinated-11-obs`, already has `y_j` as its sole notation; [line 22](highlights_g11_t2.tex#L22), concept `obs`, defines `y_j` or `x_i` as one measured observation and distinguishes it from the whole sample `X_i`.

The practice's `y_j` row correctly uses the effective observation definition and a local bill-charge interpretation. The narrow fact is that its definition is inherited and mentions alternative notation; no independent `y_j`-only definition text is stored. That does not establish missing observation support. No ecosystem change is justified unless a shorter symbol-specific definition is an explicit reusable requirement; such a context override would be sufficient. The local bill interpretation remains L4.

### S3. Opening legends, table infrastructure, wrappers and palettes are supported

**Origins:** [R10.1](../../grade10/term_2/1-practice_activities/G10_T2_L1_C1_practice_activity_highlights_gaps.md), [R10.2](../../grade10/term_2/1-practice_activities/G10_T2_L1_C2_practice_activity_highlights_gaps.md), [R10.3](../../grade10/term_2/1-practice_activities/G10_T2_L1_C3_practice_activity_highlights_gaps.md), [R11.1](../../grade11/term_2/1-practice_activities/G11_T2_L1_C1_practice_highlights_gaps.md), [R11.2](../../grade11/term_2/1-practice_activities/G11_T2_L1_C2_practice_highlights_gaps.md), [R11.3](../../grade11/term_2/1-practice_activities/G11_T2_L1_C3_practice_highlights_gaps.md).

**Authority and existing handling:** [Term 2 compatibility](highlights_compat_ttwo.tex), `practicehighlightlegend@G10-T2-C1-coordinated`, `@G10-T2-C2-coordinated`, `@G10-T2-C3-coordinated`, and `@G11-T2-C3-coordinated` provide the used concise legends. `practicehighlightlegend@G11-T2-C1` at line 89 supplies the supported Sample/Population side-by-side opening including both variance partners; the single-table coordinated helper at line 688 is a different existing layout. G11 C2 uses `\HighlightReference{G11-T2-C2-coordinated}[concise]`, whose catalog implementation selects and renders the standard schema rather than invoking the old fixed-cell legend. [Tables](highlights_tables.tex), `\HighlightDetailedTable`, `\COneToneDetailedHeaders`, already supply four columns and repeated headings; local explicit rows are supported.

[Roles](highlights_roles.tex) already distinguish quantity, event, probability, cumulative probability, count, population/sample means, population/sample SD and variance, proportions, SE, confidence, tail area, critical value, margin, bounds, width and coverage. [Palette lines 129–166](highlights_palette.tex#L129) define the variance aliases, related interval shades and coordinated setup. Existing wrappers accept complete indexed arguments. Color relationships do not make the mathematical quantities interchangeable.

**Smallest proposal/uncertainty:** none for layout, headers, wrappers, colors, renderer geometry, loaders or toggles. A2 preserves the narrower `N` treatment issue; G1 preserves the genuine automatic-splitting limitation. These source findings do not assert rendered fit, pagination quality or runtime correctness.

### S4. Historical confidence/significance treatment conflicts with coordinated semantics

**Origin:** [R11.2](../../grade11/term_2/1-practice_activities/G11_T2_L1_C2_practice_highlights_gaps.md). The absence of a dedicated significance role does not mean alpha has no support. In addition to the coordinated tail definitions in G9, [G11 T2 line 3675](highlights_g11_t2.tex#L3675), `g11-t2-legacy-cell-15`, bundles confidence `C` and significance `\alpha` using `\CtwoConfidence` for both. Its meaning still explains `\alpha=1-C` and each tail. This is a historical presentation with a different treatment, not authority for remapping the current C2 alpha to confidence.

**Existing local handling:** C2 selects the coordinated reference and uses the local `\CtwoSignificance` → `\HLTailArea` alias for alpha/tails, preserving confidence separately. The smallest current change is none; any future compatibility alignment is a separate deliberate migration. The source conflict is retained here rather than silently choosing one history or claiming a missing color.

### S5. Remaining limits on claims and proposed changes

**Origins:** [R10.1](../../grade10/term_2/1-practice_activities/G10_T2_L1_C1_practice_activity_highlights_gaps.md), [R10.2](../../grade10/term_2/1-practice_activities/G10_T2_L1_C2_practice_activity_highlights_gaps.md), [R10.3](../../grade10/term_2/1-practice_activities/G10_T2_L1_C3_practice_activity_highlights_gaps.md), [R11.1](../../grade11/term_2/1-practice_activities/G11_T2_L1_C1_practice_highlights_gaps.md), [R11.2](../../grade11/term_2/1-practice_activities/G11_T2_L1_C2_practice_highlights_gaps.md), [R11.3](../../grade11/term_2/1-practice_activities/G11_T2_L1_C3_practice_highlights_gaps.md).

The cited records substantiate grouped notation, empty example fields and local specializations; they do not establish a requirement that every locally displayed symbol, numerical evaluation or example must become a shared record. G2–G13 therefore identify specific retrieval limitations and conditional minimal changes, not mandatory additions. The absence of a standalone named PMF, indicator, loss-event or simulation member must not be read as absence of all underlying mathematical support. `g10-t2-c3-coordinated-10-break` already supplies individual break-even support and requires no addition on this evidence.

The reports describe source adaptations and repeatedly disclaim compilation/verification. This synthesis uses source evidence only and makes no claim that their earlier edits were validated, that grouped notation can be split automatically, or that any proposed ecosystem change has been implemented. Source line references may shift; stable identifiers and document labels remain the intended anchors. No unresolved claim is converted into invented mathematical data, and no empty introductory interpretation is filled by inference.

Source-based consolidation only; no LaTeX compilation or rendering performed.
