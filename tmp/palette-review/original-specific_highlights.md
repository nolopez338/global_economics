# Specific Highlight Legends

This reference summarizes the registered legends, notation, and color mappings in [specific_highlights.tex](specific_highlights.tex). Shared Grade 10 colors and marker behavior are defined in [highlights.tex](highlights.tex). The LaTeX files are authoritative. The opening sections describe retained legacy keys and shared defaults; coordinated opt-in keys and the migrated practices are documented below.

## Loading and legend selection

Load `highlights.tex` after the shared preamble, then load `specific_highlights.tex`. Both files guard against repeated loading: `highlights.tex` uses `\GTenHighlightLoaded`, and `specific_highlights.tex` uses `\PracticeHighlightRegistryLoaded`. The shared renderer requires TikZ without adding package options.

Use `\PracticeHighlightLegend{key}` to print a registered legend. An unknown key raises a LaTeX package error. Keys include grade, term, and applicable criteria; a suffix distinguishes a variant when needed.

| Registered key | Content and presentation |
|---|---|
| `G10-T2-C1` | Six-row table headed “Highlighted item” and “What it means”; uses `\GTenHighlightLegend`. |
| `G10-T2-C1-C2-C3-C4-C5-C6-C7-C8-C9` | Compact “Reading the markers.” paragraph covering the same six roles. |
| `G10-T2-C8` | Four-row “Symbol or notation” / “Concept” / “Brief meaning” table for primary and transformed variables, expected value, and expected value of squared values. |
| `G11-T2-C1` | Side-by-side Sample and Population tables, each headed “Symbol or notation”, “Concept”, and “Brief meaning”. |
| `G11-T2-C1-slides` | Two-column “Sample (green)” / “Population (red)” table: groups, means, standard deviations, then proportions. |
| `G11-T2-C2` | “Terms and symbols” / “Meaning in context” table with sample size, population SD, significance level, and observed coverage; applies a local orange interval palette. |
| `G11-T2-C3` | Three-column “Symbol or notation” / “Concept” / “Brief meaning” table with nine explicit rows, using the default palette. |

## Marker behavior

`\HighlightStroke{color}{fragment}` draws a rounded background marker. `\GTenHLStroke` is an alias. The shared renderer uses fill opacity `0.32` and text opacity `1`: the background is translucent, while glyphs retain their current color. Hex values below describe base colors, not the final translucent appearance, which also depends on the background. Markers have 1 mm rounded corners, no outline, 1.5 mm horizontal and 0.8 mm vertical inner padding, and zero outer separation. Text and math nodes align to the content baseline; math uses `\mathpalette` to preserve display, text, script, and scriptscript sizes, with `\mathsurround` reset locally to zero.

Highlights default to enabled with `\GTenHighlightstrue`; `\GTenHighlightsfalse` disables the markers while retaining their contents. Names, notation, and units preserve meaning without color. Role wrappers accept one short text or math fragment in its current mode. Do not nest strokes; keep alignment markers, line breaks, relation signs, and binary operators outside them. Use `\text{...}` for text inside math.

## Grade 10: outcomes, variables, and probabilities

The Grade 10 C1 and combined-criteria entries use these roles. The full table follows the order below; the compact paragraph lists outcomes, the three variables, probabilities, and unknown quantities.

| Highlighted item | Meaning | Wrapper / color identifier | Base hex |
|---|---|---|---|
| Outcome | A possible result of the experiment; a complete outcome or label. | `\GTenHLOutcome` / `GTenHLOutcome` | `#BC9DE0` |
| Probability | Unitless chance of an outcome or event; known probability masses or results. | `\GTenHLProbability` / `GTenHLProbability` | `#86BFF0` |
| First variable | Primary variable, including its numerical values and units. | `\GTenHLValue` / `GTenHLValue` | `#FFBB55` |
| Second variable | Second simultaneous variable, including its values and units. | `\GTenHLSecond` / `GTenHLSecond` | `#8FD49A` |
| Third variable | Third simultaneous variable, including its values and units. | `\GTenHLThird` / `GTenHLThird` | `#F1DA55` |
| Unknown parameter | A quantity to determine from the information given. | `\GTenHLParameter` / `GTenHLParameter` | `#ED9DAA` |

The shared role comments specify that an unknown probability mass or constant retains the parameter role when solved; when substituted as a known mass, it uses the probability role.

### Expected value and the C8 legend

The shared `\HLExpectedValue{fragment}` wrapper calls `\HighlightStroke{ExpectedValueColor}{fragment}`. `ExpectedValueColor` has base hex `#6500A8` (deep violet); it uses the same `0.32` background fill opacity, fully opaque text, and highlight toggle as the other roles. It is distinct from outcome lavender and from the legacy coral population-mean default; the coordinated population-mean alias below reuses this violet.

The `G10-T2-C8` legend groups `\tabcolsep=4pt` and has four rows in this order:

| Notation | Concept and meaning | Effective wrappers / colors |
|---|---|---|
| $X,\ x$ | Primary variable and supported values, retaining units. | `\GTenHLValue` / `GTenHLValue` (`#FFBB55`). |
| $Y$ | Transformed variable after scaling and a fixed addition. | `\GTenHLSecond` / `GTenHLSecond` (`#8FD49A`). |
| $E(X),\ E(Y)$ | Expected value: probability-weighted average, in original units. | `\HLExpectedValue` / `ExpectedValueColor` on the operator and concept name; arguments keep their variable roles. |
| $E(X^2)$ | Expected value of squared values: average after squaring, in squared units. | Violet operator and “Expected value”; $X^2$ keeps the primary-variable role. |

The role also supports $\mathbb{E}[\cdot]$ notation and numerical expectation results, including their units where appropriate. Positive, negative, and zero expectations use the same violet. Relations and binary operators remain outside strokes, with no nested markers or whole-calculation strokes. $E(X^2)$ and $[E(X)]^2$ remain distinct through their notation and definitions; both have squared units. The C8 legend adds no population-mean, variance, or standard-deviation color and has no reveal behavior. The existing C1 and combined-criteria legends do not acquire the expected-value role.

## Grade 11 C1: sample and population

The legacy practice key uses green sample roles and red population roles. The slides variant pairs the same groups and measures but omits the separate size rows.

| Concept | Sample notation and meaning | Sample color / base hex | Population notation and meaning | Population color / base hex |
|---|---|---|---|---|
| Group | $X,\ X_i$: selected units. | `G11T2C1Sample` / `#173B17` | $\mathcal{P}$: all units in scope. | `G11T2C1Population` / `#75162B` |
| Size | $n$: number selected. | `G11T2C1Sample` / `#173B17` | $N$: number in scope. | `G11T2C1Population` / `#75162B` |
| Mean | $\bar{x}$: sample mean. | `G11T2C1SampleMean` / `#9BDD36` | $\mu$: population mean. | `G11T2C1PopulationMean` / `#FF765C` |
| Standard deviation | $s$: sample standard deviation. | `G11T2C1SampleSD` / `#189338` | $\sigma$: population standard deviation. | `G11T2C1PopulationSD` / `#E42134` |
| Proportion | $\hat{p}$: fraction meeting a condition in the sample. | `G11T2C1SampleProportion` / `#23B895` | $p$: fraction meeting a condition in the population. | `G11T2C1PopulationProportion` / `#D74383` |

The practice legend groups its layout settings (`\small`, `\tabcolsep=3pt`, and `\arraystretch=1.18`) and places each table in a minipage of `0.49\linewidth`.

The slide helpers are `\GradeElevenCOneLegendGroups`, `\GradeElevenCOneLegendMeans`, `\GradeElevenCOneLegendDeviations`, and `\GradeElevenCOneLegendProportions`, assembled by `\GradeElevenCOneLegendTable`, which accepts four row-helper commands in the desired order. Each row helper accepts a reveal-step argument. `\PracticeHighlightLegendCell{step}{content}` displays all content by default; slides may redefine it locally. The table passes steps 2, 3, 4, and 5 to its four row helpers.

## Grade 11 C2 and C3: confidence intervals

The `\Ctwo...` wrappers below are shared by C2 and C3. Some reuse C1 or Grade 10 colors; the prefix alone does not restrict a wrapper to C2.

| Concept / notation | Meaning and representative source values | Wrapper | Default color / base hex |
|---|---|---|---|
| Population mean, $\mu$ | Fixed population parameter being estimated. | `\CtwoMean` | `G11T2C1PopulationMean` / `#FF765C` |
| Point estimate, $\bar{x}$ | Sample mean and interval centre; example: 60 units. | `\CtwoPoint` | `G11T2C1SampleMean` / `#9BDD36` |
| Population SD, $\sigma$ | Spread of individual observations; C2 example: 20 units. | `\CtwoSD` | `G11T2C1PopulationSD` / `#E42134` |
| Sample size, $n$ | Number of sampled units; C2 example: 100. | `\CtwoSize` | `G11T2C1Sample` / `#173B17` |
| Standard error, $\mathrm{SE}$ | Spread of sample means across repeated samples, or its estimate; example: 2 units. | `\CtwoSE` | `CtwoSEColor` / `#F4D94B` |
| Critical value, $z^*$ | Unitless standard-normal multiplier selected by $C$; example: 1.96 bounds central area 0.95 between $-z^*$ and $z^*$. | `\CtwoCritical` | `CtwoCriticalColor` / `#2648BB` |
| Margin of error, $\mathrm{MoE}$ | Distance from centre to an endpoint: $\mathrm{MoE}=z^*\mathrm{SE}$; example: $1.96(2)=3.92$ units. | `\CtwoMoE` | `CtwoMoEColor` / `#F28A18` |
| Endpoints; C3 uses $L,\ U$ | Lower and upper bounds: $\bar{x}\pm\mathrm{MoE}$; example: $60\pm3.92$ gives 56.08 and 63.92 units. | `\CtwoEndpoint` | `CtwoEndpointColor` / `#A75A27` |
| Full width, $2\mathrm{MoE}$; C3 uses $W$ | Distance between endpoints; example: $2(3.92)=7.84$ units. | `\CtwoWidth` | `CtwoWidthColor` / `#B83769` |
| Confidence level, $C$; C2 also includes significance level, $\alpha$ | Nominal long-run coverage under the model; $95\%=0.95$ is the central normal area. In C2, $\alpha=1-C=0.05$ and each tail has area $\alpha/2=0.025$. | `\CtwoConfidence` | `CtwoConfidenceColor` / `#55C8F0` |
| Observed coverage, $\text{rate}$ | Fraction of intervals covering the fixed mean in a run; C2 example: $4/5=80\%$. Each interval covers or misses; the observed fraction can differ from $C$. | `\CtwoCoverage` | `GTenHLOutcome` / `#BC9DE0` |

### Legacy C2-specific legend and palette

The C2 legend lists: population mean; point estimate; population SD and sample size together; standard error; critical value; margin of error; endpoints; full width; confidence and significance levels together; observed coverage. Its sample-size row connects $\sigma=20$ units and $n=100$ to $\mathrm{SE}=20/\sqrt{100}=2$ units. Nominal confidence and significance settings do not come from observed coverage.

`\CtwoPracticeIntervalPalette` changes the endpoint and width colors to relatives of the margin-of-error orange. The C2 legend invokes it inside a group, so its overrides do not change the shared defaults used by the legacy C3 key. The palette command itself creates no group: an explicit call in a document has caller-controlled scope. The legend also groups its helper redefinitions, restoring the shared helpers afterward.

| Role | C2 color expression | Interpretation |
|---|---|---|
| Margin of error | `CtwoMoEColor` (`#F28A18`) | Unchanged base orange. |
| Endpoints | `CtwoMoEColor!45!white` | 45% base orange mixed with 55% white. |
| Full width | `CtwoMoEColor!45!black` | 45% base orange mixed with 55% black. |

These are xcolor mix expressions, applied before the shared marker's `0.32` fill opacity. They are not the default endpoint and width hex colors in the shared-role table.

### Legacy C3 legend and shared row helpers

The C3 legend has explicit rows in this order: sample size $n$; population SD $\sigma$ (known individual-observation spread); standard error $\mathrm{SE}$ (spread of sample means); confidence level $C$ (nominal long-run coverage, decimal in formulas); critical value $z^*$ (unitless normal multiplier selected by $C$); margin of error $\mathrm{MoE}$ (centre-to-endpoint distance); point estimate $\bar{x}$ (sample mean and interval centre); endpoints $L,\ U$ (lower and upper bounds); full width $W$ (distance between endpoints, twice the margin). Symbols and concept names use their corresponding wrappers. The legend groups `\tabcolsep=4pt`. It does not invoke the C2 interval palette or the shared row helpers, and contains no population-mean, significance-level, observed-coverage, or numerical-example row.

`\CtwoLegendMeans` supplies population mean, then point estimate. `\CtwoLegendConfidence` supplies the confidence row. `\CtwoLegendCritical` supplies the critical-value row. `\CtwoLegendInterval` accepts an optional numeric argument, default `[0]`: its fixed row order is standard error, margin of error, endpoints, full width, then confidence. `[0]` adds the critical-value row after confidence; `[1]` inserts it between standard error and margin of error. Any other numeric value adds neither critical-value row. These helpers have no reveal mechanism.

C2 calls `\CtwoLegendInterval[1]` and locally redefines the mean, interval, and confidence helpers. The mean and interval versions preserve the shared row order and numeric branches but include units inside selected highlighted values: 60 units for the point estimate, 2 units for standard error, 3.92 units for margin of error, 63.92 units for the upper endpoint, and 7.84 units for full width. The lower endpoint 56.08 is a separate highlight without units inside it. The local confidence helper adds $\alpha=1-C$ and the tail areas. The shared helpers remain defined even though C3 now supplies its rows directly.

## Coordinated Term 2 legends

The `-coordinated` keys below are opt-in, three-column concise legends. They do not replace the seven legacy keys above. The legacy C1 slide helpers and their reveal steps remain unchanged; no coordinated slide variant is registered. The general keys are catalogs, rather than required opening tables for every activity. G10 C10 has no source: **source not found; legend pending**, with no registered student-facing key. G11 C8 covers demonstrated t intervals for means; the existing assessed wording about proportions still needs author review.

`\CoordinatedLegendTable{rows}` uses a non-floating `longtable`, with repeated headers, a continuation footer, whole-row page breaks, `\tabcolsep=4pt` and `\arraystretch=1.18`. Its paragraph columns are 32%, 25%, and the remaining 43% minus four column spacings. It preserves the document's type size and locally compacts marker padding to 0.6 mm horizontally / 0.3 mm vertically, without changing body markers. It requires the article preamble's `longtable`; it is not a Beamer layout. Each registry entry groups the table settings, notation specializations and `\CoordinatedTermTwoPalette`. The final two rows are kept together with a no-break penalty. There are no reveal overlays in these new tables.

`\CoordinatedLegendEntry{grade}{entry ID}` dispatches to shared `coordinatedrow@<grade>@<entry>` data. `\CoordinatedLegendRow{role ID}{notation}{styled concept}{brief meaning}` emits the three cells; its first argument records the semantic binding. Concept words are wrapped separately so they can reflow. Notation comes from `coordinatednotation@<grade>@<entry>`, locally specialized by criterion entries. Definitions and concepts are shared with the catalogs. Detailed notation references retain separate table bodies and example interpretations.

### Palette scope and aliases

`\CoordinatedTermTwoPalette` creates no group; its lifetime is controlled by its caller. It maps `G11T2C1PopulationMean` to `ExpectedValueColor`, `G11T2C1PopulationProportion` to `GTenHLProbability`, `CtwoEndpointColor` to `MathHLBoundsColor`, and `CtwoWidthColor` to `MathHLWidthColor`. Consequently existing raw color calls and `\CtwoMean`, `\CtwoEndpoint` and `\CtwoWidth` follow the selected palette. Loading the registry alone does not opt legacy callers into these changes. The original `\CtwoPracticeIntervalPalette` remains available.

The palette also provides the one-argument `\CtwoError` forwarding alias to `\HLCoverageError` only when that name is undefined. This opt-in definition avoids a duplicate with independently defined classroom commands. Canonical aliases are ordinary one-argument forwarding commands or direct `\HighlightStroke` calls, rather than frozen `\let` copies. `\CoordinatedRole{stable role ID}{fragment}` dispatches to the corresponding wrapper. `\HLMathContext` returns its argument without a fill.

New color identifiers are defined at registry load time; these are additional colors, not load-time overrides of legacy identifiers:

| Identifier | Exact base or xcolor mix |
|---|---|
| `MathHLCumulativeColor` | HTML `43A5C9` |
| `CtwoErrorColor` | HTML `28AFA2` |
| `MathHLComplementColor` | `GTenHLProbability!65!CtwoCriticalColor` |
| `MathHLPopulationVarianceColor` | `G11T2C1PopulationSD!55!white` |
| `MathHLSampleVarianceColor` | `G11T2C1SampleSD!55!white` |
| `MathHLTailColor` | `CtwoConfidenceColor!55!CtwoCriticalColor` |
| `MathHLBoundsColor` | `CtwoMoEColor!45!white` |
| `MathHLWidthColor` | `CtwoMoEColor!45!black` |

The base colors referenced by these mixes are listed above. Mixes are captured by `\colorlet` at definition time, before the renderer's 0.32 fill opacity; they are not final displayed hex values. Population mean and expectation share violet only under this opt-in mapping; the legacy population-mean default remains coral. Names, definitions, units and notation distinguish concepts sharing hues, including sample groups/design counts and outcomes/observed coverage.

| Stable role | Canonical wrapper | Effective color identifier |
|---|---|---|
| `outcome` | `\GTenHLOutcome` | `GTenHLOutcome` |
| `event` | `\HLMathEvent` | `GTenHLOutcome` |
| `quantity.primary` | `\GTenHLValue` | `GTenHLValue` |
| `quantity.secondary` | `\GTenHLSecond` | `GTenHLSecond` |
| `quantity.tertiary` | `\GTenHLThird` | `GTenHLThird` |
| `probability` | `\HLPopulationProportion` | `GTenHLProbability` |
| `unknown` | `\GTenHLParameter` | `GTenHLParameter` |
| `probability.complement` | `\HLComplementProbability` | `MathHLComplementColor` |
| `cumulative` | `\HLCumulativeProbability` | `MathHLCumulativeColor` |
| `count.design` | `\HLObservationCount` | `G11T2C1Sample` |
| `model.control` | `\HLModelControl` | `GTenHLParameter` |
| `expectation` | `\HLPopulationMean` | `ExpectedValueColor` |
| `variance.population` | `\HLPopulationVariance` | `MathHLPopulationVarianceColor` |
| `sd.population` | `\HLPopulationSD` | `G11T2C1PopulationSD` |
| `context` | `\HLMathContext` | `No fill; identity` |
| `group.sample` | `\HLSampleGroup` | `G11T2C1Sample` |
| `group.population` | `\HLPopulationGroup` | `G11T2C1Population` |
| `mean.sample` | `\HLSampleMean` | `G11T2C1SampleMean` |
| `sd.sample` | `\HLSampleSD` | `G11T2C1SampleSD` |
| `variance.sample` | `\HLSampleVariance` | `MathHLSampleVarianceColor` |
| `proportion.sample` | `\HLSampleProportion` | `G11T2C1SampleProportion` |
| `standard.error` | `\HLStandardError` | `CtwoSEColor` |
| `confidence` | `\HLConfidence` | `CtwoConfidenceColor` |
| `tail` | `\HLTailArea` | `MathHLTailColor` |
| `critical` | `\HLCriticalValue` | `CtwoCriticalColor` |
| `margin` | `\HLMarginOfError` | `CtwoMoEColor` |
| `bounds` | `\HLIntervalBounds` | `MathHLBoundsColor` |
| `width` | `\HLIntervalWidth` | `MathHLWidthColor` |
| `coverage` | `\HLObservedCoverage` | `GTenHLOutcome` |
| `coverage.error` | `\HLCoverageError` | `CtwoErrorColor` |

### Catalog entries

Row order is the order printed by each general key. Shared IDs do not make unlike objects identical: nominal confidence, tail area, finite-run coverage, theoretical area, individual spread, standard error, margin, bounds and full width retain separate definitions.

Grade 10:

| Entry ID / stable role | Notation | Concept and brief meaning |
|---|---|---|
| `outcome` / `outcome` | $\omega$, $\Omega$ | Outcome and sample space: One complete result; all possible complete results. |
| `event` / `event` | $A$, $E$, $E^c$; $\{X\leq a\}$ | Event and complement: Outcomes meeting a condition; those outside it. |
| `variable` / `quantity.primary` | $X$, $x$, $T$, $t$; $X(\omega)$ | Primary variable and value: Numerical rule and possible value; state the units. |
| `support` / `quantity.primary` | $S_X=\{x:P(X=x)>0\}$ | Support: Distinct values with positive probability, in the variable's units. |
| `second` / `quantity.secondary` | $Y$, $y$; $Y=f(X)$; $Y_i=f_i(X)$ | Second or transformed variable: Another numerical description, with its own units. |
| `third` / `quantity.tertiary` | $Z$, $z$, $C$ | Third variable: A third numerical description; an indicator is unitless. |
| `mass` / `probability` | $P(A)$, $P(\omega)$, $p_X(x)$, $m_X(x)$ | Probability and mass: Unitless chance of an event or one supported value. |
| `unknown` / `unknown` | $k$, $q$, $c$, $a$, $w$ | Unknown quantity: A model quantity to determine, with a context-defined domain. |
| `ops` / `context` | $\sum$, $\binom nk$, $n!$, $e$, $\sim$ | Operations and distribution notation: Sum, count selections, take factorials, use the exponential constant, or name a model. |
| `assume` / `context` | Independence, constant $p$, fixed observation rule | Model conditions: Conditions to check before using the selected distribution. |
| `cum` / `cumulative` | $F_X(a)$, $F_X(a^-)$; $P(X\leq a)$ | Cumulative probability: Chance up to a cutoff; the left limit excludes the cutoff. |
| `cutoff` / `quantity.primary` | $a$, $b$, $m$, $\lfloor x\rfloor$ | Cutoff and integer part: A boundary in the variable's units; specify included endpoints. |
| `aux` / `context` | $K,a,b,c$; $a_m,b_m,c_m$; $N_k,b_j,R_m$ | Auxiliary counts and states: Problem-defined counts, recurrence states, balances or survival quantities. |
| `p` / `probability` | $p=P(X=1)$ | Success probability: Chance of the specified state labelled 1, between 0 and 1. |
| `q` / `probability.complement` | $1-p$ | Complement probability: Chance of the complementary state labelled 0. |
| `expected` / `expectation` | $E(X)$, $\mathbb E[Y_i]$, $\mu$ | Expected value or model mean: Probability-weighted average, in original units. |
| `break` / `probability` | $p_i^*$ | Individual break-even probability: Probability at which the specified expected net payoff is zero. |
| `transform` / `context` | $a,b$; $f_i(0),f_i(1)$ | Transformation inputs: Scale, fixed addition or state payoffs, with required units. |
| `size` / `count.design` | $n$ | Observation count: Fixed trial count or sample size; a positive integer. |
| `wait` / `quantity.primary` | $T$, $t$; $F=T-1$ or $F=T-r$ | Trials and failures: Total trials include the final success; failures exclude successes. |
| `target` / `model.control` | $r$ | Success target: Fixed number of successes required before stopping. |
| `rate` / `context` | $\mathrm{rate}$, $\mathrm{exposure}$ | Rate and exposure: Events per exposure unit and length of the observation window. |
| `lambda` / `expectation` | $\lambda$ | Poisson interval mean: Expected count for the selected exposure. |
| `secondmoment` / `expectation` | $E(X^2)$, $[E(X)]^2$ | Second moment and squared mean: Average of squares; square of the average. Both use squared units. |
| `variance` / `variance.population` | $\operatorname{Var}(X)$, $\sigma_X^2$ | Variance: Mean squared deviation from the mean; squared units. |
| `sd` / `sd.population` | $\sigma_X$, $\sigma$ | Population or model standard deviation: Spread of individual values, in original units. |

Grade 11:

| Entry ID / stable role | Notation | Concept and brief meaning |
|---|---|---|
| `sample` / `group.sample` | $X$, $X_i$ | Sample: Selected units; here each index identifies a whole draw. |
| `population` / `group.population` | $\mathcal P$, $N$ | Population and size: All units in the stated scope; their total number. |
| `size` / `count.design` | $n$ | Observation count: Fixed trial count or sample size; a positive integer. |
| `obs` / `quantity.primary` | $y_j$, $x_i$ | Observation: Measured value on one selected unit, with the response's units. |
| `meanpop` / `expectation` | $\mu$, $\mu_{\rm sim}$ | Population mean: Fixed mean of the defined population; simulation mean is supplied separately. |
| `meansample` / `mean.sample` | $\bar x$, $\bar x_i$ | Sample mean and point estimate: Average of one sample; estimates its population mean. |
| `sd` / `sd.population` | $\sigma_X$, $\sigma$ | Population or model standard deviation: Spread of individual values, in original units. |
| `sdsample` / `sd.sample` | $s$, $s_i$ | Sample standard deviation: Spread of sample observations, in response units. |
| `proppop` / `probability` | $p$ | Population proportion: Fraction of all units meeting the condition; unitless. |
| `propsample` / `proportion.sample` | $\hat p=x/n$ | Sample proportion: Observed success fraction among selected units; unitless. |
| `se` / `standard.error` | $\mathrm{SE}$, $\widehat{SE}$ | Standard error: Spread of a statistic across samples, or its estimate. |
| `confidence` / `confidence` | $C$ | Confidence level: Chosen nominal long-run coverage under the model; decimal in formulas. |
| `tail` / `tail` | $\alpha$, $\alpha/2$ | Significance level and tail area: Total excluded area and each equal tail in a two-sided procedure. |
| `critical` / `critical` | $z^*$, $t^*$ | Critical value: Positive unitless reference cutoff selected by confidence and model. |
| `margin` / `margin` | $\mathrm{MoE}$, $E$, $E_{\rm target}$ | Margin of error: Centre-to-bound distance, or its precision target. |
| `bounds` / `bounds` | $L$, $U$; $\mathrm{CI}=[L,U]$ | Bounds and confidence interval: Lower and upper limits; the range they delimit for the parameter. |
| `width` / `width` | $W=U-L$; $W=2\mathrm{MoE}$ | Full interval width: Total distance between bounds, in the parameter's units. |
| `reported` / `bounds` | $L_{\rm rep}$, $U_{\rm rep}$, $\mathrm{CI}_{\rm rep}$ | Reported bounds and interval: Rounded reporting values, separate from calculated values. |
| `reportedwidth` / `width` | $W_{\rm rep}$ | Reported full width: Difference of reported endpoints; may differ from calculated width. |
| `coverage` / `coverage` | $N_{\rm cover}(C)$, $N(C)$, $\mathrm{Cov}(C)$ | Observed coverage and counts: Covering intervals, all intervals at that level, and their finite-run percentage. |
| `error` / `coverage.error` | $E_{\rm abs}(C)$ | Absolute coverage error: Absolute gap between observed and nominal percentages, in percentage points. |
| `normal` / `cumulative` | $\Phi(z)$, $\Phi^{-1}(u)$ | Normal cumulative area and inverse: Left-tail standard normal area; the cutoff with that area. |
| `shape` / `context` | Random selection, shape, outliers, groups | Inference conditions: Check design and procedure-specific assumptions. |
| `theoretical` / `cumulative` | $C_{\rm normal}$ | Theoretical normal coverage: Model area from a rounded cutoff; may differ slightly from nominal confidence. |
| `budget` / `context` | Cost per unit, budget, benchmark | Design inputs and comparison values: Fixed constraints or reference amounts, with stated units. |
| `variance` / `variance.population` | $\operatorname{Var}(X)$, $\sigma_X^2$ | Variance: Mean squared deviation from the mean; squared units. |
| `fraction` / `context` | $n/N$ | Sampling fraction: Share of the finite population selected; check design conditions. |
| `successcount` / `count.design` | $x$; $n\hat p$, $n(1-\hat p)$ | Observed outcome counts: Success and other-outcome counts within a sample. |
| `planning` / `probability` | $p_0$ | Planning proportion: Pilot or conservative input; not a null-hypothesis value here. |
| `precisionplan` / `count.design` | $n_{\min}$, $E(n)$ | Sample-size plan: Minimum usable integer count and its achieved margin. |
| `df` / `model.control` | $df=n-1$ | Degrees of freedom: Reference index for the one-sample t procedure. |
| `varsample` / `variance.sample` | $s^2$ | Sample variance: Squared sample spread; use the specified divisor. |
| `ops` / `context` | $\sum$, $\binom nk$, $n!$, $e$, $\sim$ | Operations and distribution notation: Sum, count selections, take factorials, use the exponential constant, or name a model. |

### Registry selections and notation variants

Each list below is the exact printed row order. Notation and meaning variants change only the indicated cells inside that legend’s group. All other cells resolve to the catalog data above. `\CoordinatedSampleMeaning` defaults to the whole-draw index explanation; C9/C10 specialize it to selected units under the stated design. `\CoordinatedPopulationMeanMeaning` includes the separately supplied simulation mean by default; criterion groups without that supplied quantity use only the fixed population mean and response units.

- `G10-T2-C1-C2-C3-C4-C5-C6-C7-C8-C9-coordinated`: `outcome`, `event`, `variable`, `support`, `second`, `third`, `mass`, `unknown`, `ops`, `assume`, `cum`, `cutoff`, `aux`, `p`, `q`, `expected`, `break`, `transform`, `size`, `wait`, `target`, `rate`, `lambda`, `secondmoment`, `variance`, `sd`.
- `G11-T2-C1-C2-C3-C4-C5-C6-C7-C8-C9-C10-coordinated`: `sample`, `population`, `size`, `obs`, `meanpop`, `meansample`, `sd`, `sdsample`, `proppop`, `propsample`, `se`, `confidence`, `tail`, `critical`, `margin`, `bounds`, `width`, `reported`, `reportedwidth`, `coverage`, `error`, `normal`, `shape`, `theoretical`, `budget`, `variance`, `fraction`, `successcount`, `planning`, `precisionplan`, `df`, `varsample`, `ops`.
- `G10-T2-C1-coordinated`: `outcome`, `event`, `variable`, `support`, `second`, `third`, `mass`, `unknown`, `ops`, `assume`. Notation: `variable`: $X$, $x$, $F$; $X(\omega)$; `second`: $Y$, $y$, $E$; `third`: $Z$, $z$, $C$; `event`: $A$; `unknown`: $k$, $q$, $c$; `mass`: $P(\omega)$, $p_X(x)$; `ops`: $\sum$.
- `G10-T2-C2-coordinated`: `outcome`, `event`, `variable`, `support`, `mass`, `cum`, `unknown`, `cutoff`, `ops`, `assume`, `aux`. Notation: `variable`: $X$, $x$; `mass`: $p_X(x)$; `ops`: $\sum$, $\binom nk$, $n!$; `event`: $\{X\leqa\}$.
- `G10-T2-C3-coordinated`: `event`, `variable`, `support`, `p`, `q`, `second`, `mass`, `cum`, `expected`, `break`, `transform`. Notation: `variable`: $X$, $x$; `second`: $Y_i=f_i(X)$; `transform`: $f_i(0),f_i(1)$; `event`: $E$, $E^c$; `mass`: $m_X(x)$, $m_{Y_i}(y)$; `cum`: $F_X(t)$, $F_{Y_i}(t)$; `expected`: $\mathbb E[Y_i]$.
- `G10-T2-C4-coordinated`: `variable`, `support`, `second`, `p`, `q`, `size`, `mass`, `cum`, `cutoff`, `ops`, `assume`. Notation: `variable`: $X$, $x$; `second`: $Y$; `mass`: $P(X=k)$; `cum`: $P(X\leq b)$; `cutoff`: $a$, $b$, $k$; `ops`: $\sum$, $\binom nk$, $n!$, $\sim$; `p`: $p$.
- `G10-T2-C5-coordinated`: `wait`, `support`, `p`, `q`, `second`, `mass`, `cum`, `cutoff`, `event`, `assume`. Notation: `second`: $C$; `support`: $S_T$; `wait`: $T$, $t$; $F=T-1$; `mass`: $P(T=t)$; `cum`: $P(T\leq t)$; `event`: $A$, $B$; `cutoff`: $m$; `p`: $p$.
- `G10-T2-C6-coordinated`: `wait`, `support`, `p`, `q`, `target`, `second`, `mass`, `cum`, `size`, `cutoff`, `ops`, `assume`. Notation: `second`: $C$; `support`: $S_T$; `wait`: $T$, $t$; $F=T-r$; `mass`: $P(T=t)$; `cum`: $P(T\leq t)$; `cutoff`: $m$; `ops`: $\sum$, $\binom nk$, $n!$, $\sim$; `p`: $p$.
- `G10-T2-C7-coordinated`: `variable`, `support`, `mass`, `cum`, `cutoff`, `rate`, `lambda`, `second`, `ops`, `assume`. Notation: `variable`: $X$, $k$; `second`: $L$; `mass`: $P(X=k)$; `cum`: $P(X\leq b)$; `cutoff`: $a$, $b$, $k$; `ops`: $\sum$, $k!$, $e$, $\sim$; `assume`: Constant rate, independent interval counts, isolated events.
- `G10-T2-C8-coordinated`: `variable`, `support`, `second`, `mass`, `expected`, `secondmoment`, `variance`, `sd`, `transform`, `ops`. Notation: `variable`: $X$, $x$; `second`: $Y$; `transform`: $a,b$; `expected`: $E(X)$, $E(Y)$, $\mu$; `ops`: $\sum_x$; `mass`: $p_X(x)$.
- `G10-T2-C9-coordinated`: `event`, `variable`, `support`, `wait`, `second`, `p`, `q`, `size`, `target`, `mass`, `cum`, `rate`, `lambda`, `ops`, `assume`. Notation: `variable`: $X$, $x$; `second`: $L$; `p`: $p$; `mass`: $P(X=k)$, $P(T=t)$; `event`: $\{X\geqa\}$.
- `G11-T2-C1-coordinated`: `sample`, `population`, `size`, `obs`, `meanpop`, `meansample`, `sd`, `sdsample`, `proppop`, `propsample`. Notation: `sd`: $\sigma$; `sdsample`: $s$; `meanpop`: $\mu$; `obs`: $y_j$. Meanings: `\CoordinatedPopulationMeanMeaning`: Fixed mean of the defined population, in the response's units..
- `G11-T2-C2-coordinated`: `meanpop`, `meansample`, `sd`, `size`, `sdsample`, `se`, `confidence`, `tail`, `critical`, `margin`, `bounds`, `width`, `reported`, `reportedwidth`, `coverage`, `error`, `normal`, `obs`, `shape`. Notation: `sd`: $\sigma$; `sdsample`: $s$; `meansample`: $\bar x$; `critical`: $z^*$; `margin`: $\mathrm{MoE}$; `se`: $\mathrm{SE}$; `obs`: $x_i$.
- `G11-T2-C3-coordinated`: `meanpop`, `meansample`, `sd`, `size`, `se`, `confidence`, `tail`, `critical`, `margin`, `bounds`, `width`, `normal`, `theoretical`, `budget`, `shape`. Notation: `sd`: $\sigma$; `meanpop`: $\mu$; `meansample`: $\bar x$; `critical`: $z^*$; `margin`: $\mathrm{MoE}$; `se`: $\mathrm{SE}$. Meanings: `\CoordinatedPopulationMeanMeaning`: Fixed mean of the defined population, in the response's units..
- `G11-T2-C4-coordinated`: `meanpop`, `meansample`, `variance`, `sd`, `size`, `population`, `se`, `confidence`, `tail`, `critical`, `margin`, `bounds`, `normal`, `fraction`, `shape`, `budget`. Notation: `sd`: $\sigma$; `meanpop`: $\mu$; `meansample`: $\bar x$; `critical`: $z^*$; `margin`: $E$; `se`: $\mathrm{SE}$; `population`: Population; $N$; `bounds`: Confidence interval; $L$, $U$; `variance`: $\sigma^2$; `normal`: $P(Z\leq z)$. Meanings: `\CoordinatedPopulationMeanMeaning`: Fixed mean of the defined population, in the response's units..
- `G11-T2-C5-coordinated`: `proppop`, `propsample`, `successcount`, `size`, `population`, `se`, `confidence`, `critical`, `margin`, `bounds`, `fraction`, `shape`, `budget`. Notation: `critical`: $z^*$; `margin`: $E$; `se`: $\widehat{SE}$; `population`: Population; $N$; `bounds`: Confidence interval; $L$, $U$; `propsample`: $\hat p$.
- `G11-T2-C6-coordinated`: `meanpop`, `sd`, `proppop`, `planning`, `size`, `precisionplan`, `population`, `confidence`, `critical`, `margin`, `fraction`, `shape`, `budget`. Notation: `sd`: $\sigma$; `meanpop`: $\mu$; `critical`: $z^*$; `margin`: $E$, $E_{\rm target}$; `population`: Population; $N$. Meanings: `\CoordinatedPopulationMeanMeaning`: Fixed mean of the defined population, in the response's units..
- `G11-T2-C7-coordinated`: `proppop`, `propsample`, `successcount`, `size`, `population`, `se`, `confidence`, `critical`, `margin`, `bounds`, `width`, `fraction`, `shape`. Notation: `critical`: $z^*$; `margin`: $E$; `se`: $\widehat{SE}$; `population`: Population; $N$; `bounds`: Confidence interval; $L$, $U$; `propsample`: $\hat p$.
- `G11-T2-C8-coordinated`: `meanpop`, `meansample`, `sd`, `sdsample`, `size`, `population`, `se`, `confidence`, `tail`, `critical`, `margin`, `bounds`, `df`, `fraction`, `shape`, `budget`. Notation: `sd`: $\sigma$; `sdsample`: $s$; `meanpop`: $\mu$; `meansample`: $\bar x$; `critical`: $t^*$, $z^*$; `margin`: $E$; `se`: $\widehat{SE}$; `population`: Population; $N$; `bounds`: Confidence interval; $L$, $U$. Meanings: `\CoordinatedPopulationMeanMeaning`: Fixed mean of the defined population, in the response's units..
- `G11-T2-C9-coordinated`: `sample`, `population`, `size`, `meansample`, `sdsample`, `propsample`, `successcount`, `fraction`, `shape`, `budget`. Notation: `sdsample`: $s$; `meansample`: $\bar x$; `sample`: Selected sample; `population`: Population; $N$; `propsample`: $\hat p$. Meanings: `\CoordinatedSampleMeaning`: Selected units drawn under the stated sampling design..
- `G11-T2-C10-coordinated`: `sample`, `population`, `size`, `obs`, `meanpop`, `meansample`, `sdsample`, `varsample`, `se`, `confidence`, `critical`, `margin`, `bounds`, `df`, `precisionplan`, `fraction`, `shape`, `budget`, `ops`. Notation: `sdsample`: $s$; `meanpop`: $\mu$; `meansample`: $\bar x$; `critical`: $z^*$, $t^*$; `margin`: $E$; `se`: $\widehat{SE}$; `obs`: $x_i$; `sample`: Selected sample; `population`: Population; $N$; `bounds`: Confidence interval; $L$, $U$; `precisionplan`: $n$; achieved $E$; `ops`: $\sum x_i$, $\sum x_i^2$. Meanings: `\CoordinatedSampleMeaning`: Selected units drawn under the stated sampling design.; `\CoordinatedPopulationMeanMeaning`: Fixed mean of the defined population, in the response's units..

### Practice-local integration

All source-backed G10 C1–C9 and G11 C1–C10 Term 2 practices load the renderer and registry once and select their respective coordinated key. Each selects `\CoordinatedTermTwoPalette` at document setup scope, before deriving graph colors. Existing toggle settings are preserved; newly integrated practices have the same commented disable instruction. No new document-wide body-markup pass is implied.

G10 C1/C2 keep their local 0.6 mm horizontal / 0.3 mm vertical marker padding. The C1 superseded registry override and C2/C3 local concise tables were retired at their existing anchors. C2's `\cTwoValue`, `\cTwoOutcome`, `\cTwoMassHL`, and `\cTwoCDFHL` forward to primary, outcome, probability, and cumulative roles; `cTwoMassMarker=GTenHLProbability` and `cTwoCDFMarker=MathHLCumulativeColor`. Its opaque mass/CDF/guide graph inks remain separate (`blue!75!black`, `cyan!65!blue!80!black`, `cTwoMassColor!35`; black/black/gray when disabled). C3's one-argument `\FailureProb` now forwards to complementary probability; its expectation/probability graph inks retain their darker mixes and black disabled variants. The C8 existing detailed reference aligns mass, mean, variance and SD with the coordinated roles.

G11 C1 retains its group and statistic markers while its setup palette makes population means violet and population fractions blue; its explanatory prose and observation reference row agree. G11 C2 retires its local Symbol/Concept/Formula legend and removes the enclosing opening-guide minipage so the coordinated longtable can break across pages. Its `\CtwoSignificance` forwards to `\HLTailArea`, complete `\alpha/2` quantities remain together, and `\CtwoCI` still forwards to endpoints. Zero-argument `\CtwoCoverCount` and `\CtwoTotalCount` retain their calling convention and coverage meaning; their external confidence argument keeps its own role. Its central fill/cover/miss inks remain `CtwoConfidenceColor!55`, `GTenHLOutcome!70!black`, and `red!85!black` (disabled: `black!25`, black, black). Cover/miss line styles and symbols retain meaning independently of hue.

G11 C3 selects the coordinated orange family before graph ink derivation. Theoretical `C_{\rm normal}` names and existing calculated coverage results use the cumulative role; nominal confidence keeps its separate cyan role. Its graph inks remain `CtwoSEColor!55!black`, `CtwoMoEColor!75!black`, `CtwoCriticalColor`, and `CtwoConfidenceColor!50!black`, all black when disabled. Its local `\CthreeTableHeader[alignment]{quantity}{qualifier}` (default alignment `r`, with two strut-bearing shortstack lines) and 0.4 mm graph-label padding are preserved. These target-scoped choices do not migrate slides, classrooms or outlines. Extended-reference expansion for the previously short/absent references remains outside this legend integration.
