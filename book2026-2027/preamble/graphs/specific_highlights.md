# Specific Highlight Legends

This reference summarizes the registered legends, notation, and color mappings in [specific_highlights.tex](specific_highlights.tex). Shared Grade 10 colors and marker behavior are defined in [highlights.tex](highlights.tex). The LaTeX files are authoritative; this document describes their current definitions rather than introducing a new palette.

## Loading and legend selection

Load `highlights.tex` after the shared preamble, then load `specific_highlights.tex`. Both files guard against repeated loading.

Use `\PracticeHighlightLegend{key}` to print a registered legend. An unknown key raises a LaTeX package error. Keys include grade, term, and applicable criteria; a suffix distinguishes a variant when needed.

| Registered key | Content and presentation |
|---|---|
| `G10-T2-C1` | Six-row table headed “Highlighted item” and “What it means”; uses `\GTenHighlightLegend`. |
| `G10-T2-C1-C2-C3-C4-C5-C6-C7-C8-C9` | Compact “Reading the markers.” paragraph covering the same six roles. |
| `G11-T2-C1` | Side-by-side Sample and Population tables, each headed “Symbol or notation”, “Concept”, and “Brief meaning”. |
| `G11-T2-C1-slides` | Two-column “Sample (green)” / “Population (red)” table: groups, means, standard deviations, then proportions. |
| `G11-T2-C2` | “Terms and symbols” / “Meaning in context” table with sample size, population SD, significance level, and observed coverage; applies a local orange interval palette. |
| `G11-T2-C3` | “Terms and symbols” / “Meaning in context” table using shared mean and interval rows with the default palette. |

## Marker behavior

`\HighlightStroke{color}{fragment}` draws a rounded background marker. `\GTenHLStroke` is an alias. The shared renderer uses fill opacity `0.32` and text opacity `1`: the background is translucent, while glyphs retain their current color. Hex values below describe base colors, not the final translucent appearance.

Highlights default to enabled with `\GTenHighlightstrue`; `\GTenHighlightsfalse` disables the markers while retaining their contents. Names, notation, and units preserve meaning without color. Role wrappers accept one short text or math fragment in its current mode. Do not nest strokes; keep alignment markers, line breaks, relation signs, and binary operators outside them. Use `\text{...}` for text inside math.

## Grade 10: outcomes, variables, and probabilities

Both Grade 10 entries use these roles. The full table follows the order below; the compact paragraph lists outcomes, the three variables, probabilities, and unknown quantities.

| Highlighted item | Meaning | Wrapper / color identifier | Base hex |
|---|---|---|---|
| Outcome | A possible result of the experiment; a complete outcome or label. | `\GTenHLOutcome` / `GTenHLOutcome` | `#BC9DE0` |
| Probability | Unitless chance of an outcome or event; known probability masses or results. | `\GTenHLProbability` / `GTenHLProbability` | `#86BFF0` |
| First variable | Primary variable, including its numerical values and units. | `\GTenHLValue` / `GTenHLValue` | `#FFBB55` |
| Second variable | Second simultaneous variable, including its values and units. | `\GTenHLSecond` / `GTenHLSecond` | `#8FD49A` |
| Third variable | Third simultaneous variable, including its values and units. | `\GTenHLThird` / `GTenHLThird` | `#F1DA55` |
| Unknown parameter | A quantity to determine from the information given. | `\GTenHLParameter` / `GTenHLParameter` | `#ED9DAA` |

The shared role comments specify that an unknown probability mass or constant retains the parameter role when solved; when substituted as a known mass, it uses the probability role.

## Grade 11 C1: sample and population

The practice legend uses green sample roles and red population roles. The slides variant pairs the same groups and measures but omits the separate size rows.

| Concept | Sample notation and meaning | Sample color / base hex | Population notation and meaning | Population color / base hex |
|---|---|---|---|---|
| Group | $X,\ X_i$: selected units. | `G11T2C1Sample` / `#173B17` | $\mathcal{P}$: all units in scope. | `G11T2C1Population` / `#75162B` |
| Size | $n$: number selected. | `G11T2C1Sample` / `#173B17` | $N$: number in scope. | `G11T2C1Population` / `#75162B` |
| Mean | $\bar{x}$: sample mean. | `G11T2C1SampleMean` / `#9BDD36` | $\mu$: population mean. | `G11T2C1PopulationMean` / `#FF765C` |
| Standard deviation | $s$: sample standard deviation. | `G11T2C1SampleSD` / `#189338` | $\sigma$: population standard deviation. | `G11T2C1PopulationSD` / `#E42134` |
| Proportion | $\hat{p}$: fraction meeting a condition in the sample. | `G11T2C1SampleProportion` / `#23B895` | $p$: fraction meeting a condition in the population. | `G11T2C1PopulationProportion` / `#D74383` |

The slide helpers are `\GradeElevenCOneLegendGroups`, `\GradeElevenCOneLegendMeans`, `\GradeElevenCOneLegendDeviations`, and `\GradeElevenCOneLegendProportions`, assembled by `\GradeElevenCOneLegendTable`. Each row helper accepts a reveal-step argument. `\PracticeHighlightLegendCell{step}{content}` displays all content by default; slides may redefine it locally. The table passes steps 2, 3, 4, and 5 to its four row helpers.

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
| Endpoints | Lower and upper bounds: $\bar{x}\pm\mathrm{MoE}$; example: $60\pm3.92$ gives 56.08 and 63.92 units. | `\CtwoEndpoint` | `CtwoEndpointColor` / `#A75A27` |
| Full width, $2\mathrm{MoE}$ | Distance between endpoints; example: $2(3.92)=7.84$ units. | `\CtwoWidth` | `CtwoWidthColor` / `#B83769` |
| Confidence level, $C$; C2 also includes significance level, $\alpha$ | Nominal long-run coverage under the model; $95\%=0.95$ is the central normal area. In C2, $\alpha=1-C=0.05$ and each tail has area $\alpha/2=0.025$. | `\CtwoConfidence` | `CtwoConfidenceColor` / `#55C8F0` |
| Observed coverage, $\text{rate}$ | Fraction of intervals covering the fixed mean in a run; C2 example: $4/5=80\%$. Each interval covers or misses; the observed fraction can differ from $C$. | `\CtwoCoverage` | `GTenHLOutcome` / `#BC9DE0` |

### C2-specific legend and palette

The C2 legend lists: population mean; point estimate; population SD and sample size together; standard error; critical value; margin of error; endpoints; full width; confidence and significance levels together; observed coverage. Its sample-size row connects $\sigma=20$ units and $n=100$ to $\mathrm{SE}=20/\sqrt{100}=2$ units. Nominal confidence and significance settings do not come from observed coverage.

`\CtwoPracticeIntervalPalette` changes the endpoint and width colors to relatives of the margin-of-error orange. The C2 legend invokes it inside a group, so its overrides do not change the shared defaults used by C3. C2 documents may also invoke the palette explicitly.

| Role | C2 color expression | Interpretation |
|---|---|---|
| Margin of error | `CtwoMoEColor` (`#F28A18`) | Unchanged base orange. |
| Endpoints | `CtwoMoEColor!45!white` | 45% base orange mixed with 55% white. |
| Full width | `CtwoMoEColor!45!black` | 45% base orange mixed with 55% black. |

These are xcolor mix expressions, applied before the shared marker's `0.32` fill opacity. They are not the default endpoint and width hex colors in the shared-role table.

### C3 legend and shared row helpers

The C3 legend lists: population mean; point estimate; standard error; margin of error; endpoints; full width; confidence level; critical value. It does not add C2's population-SD/sample-size row, significance-level explanation, or observed-coverage row, and does not invoke the C2 interval palette.

`\CtwoLegendMeans` supplies the two mean rows. `\CtwoLegendConfidence` supplies the confidence row. `\CtwoLegendCritical` supplies the critical-value row. `\CtwoLegendInterval` supplies the interval rows and accepts an optional argument: default `[0]` places the critical-value row after confidence; `[1]` places it before margin of error. C2 uses `[1]` and locally redefines the mean, interval, and confidence helpers to supply its unit-aware and significance-level wording. C3 uses the shared defaults.
