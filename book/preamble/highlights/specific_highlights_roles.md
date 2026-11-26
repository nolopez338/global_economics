# Roles

[Highlights index](specific_highlights_index.md). LaTeX is authoritative.

Authoritative modules: [highlights_roles.tex](highlights_roles.tex).

Base roles load with `highlights.tex`; `\HighlightRegistryRoles` installs the remaining wrappers once at registry load. Each wrapper accepts one short text or math fragment. These interfaces rely on the renderer and palette; edit meanings/mappings here, not by replacing matching symbols throughout practice material.

`\CoordinatedRole{role-id}{fragment}` dispatches through `coordinatedrole@<role-id>`. `\GTenToneHL{role-id}{fragment}` dispatches through `tonerole@<role-id>` for decision mathematics; `g11tone@role@<id>` retains the Grade 11 namespace. Concept records may also name a local role ID; an ID denotes meaning, not a unique color.

Keep `\HLSuccessProbability{p}` distinct from `\HLPopulationProportion{p}`, `\HLPoissonMean{\lambda}` distinct from `\CfourToneRate{\lambda}`, and `\HLSampleSD{s}` distinct from `\HLStandardError{\mathrm{SE}}`. Population and sample variance are separate from their standard deviations. Shared colors do not establish concept identity. `\HLMathContext` is a deliberately unmarked identity wrapper.

```tex
The $\HLPopulationProportion{p}$ parameter is estimated by
$\HLSampleProportion{\hat p}$.
\[\HLStandardError{\mathrm{SE}}=\frac{\HLSampleSD{s}}{\sqrt{\HLObservationCount{n}}}\]
```

Historical unsuffixed `\HL...` and `\Ctwo...` interfaces forward to the explicit `\HLTtwo...` / `\CtwoTtwo...` commands. Forwarding follows later command redefinitions; xcolor snapshots do not. Do not replace forwarding with `\let` without checking callers. `\HLExpectedValue` retains its original use of `ExpectedValueColor` and responds to named overrides.

Implemented dispatch keys and public wrapper definitions (read palette identifiers in the palette document):

```tex
\newcommand{\GTenHLValue}[1]{\GTenHLStroke{GTenHLValue}{#1}}
\newcommand{\GTenHLSecond}[1]{\GTenHLStroke{GTenHLSecond}{#1}}
\newcommand{\GTenHLThird}[1]{\GTenHLStroke{GTenHLThird}{#1}}
\newcommand{\GTenHLOutcome}[1]{\GTenHLStroke{GTenHLOutcome}{#1}}
\newcommand{\GTenHLProbability}[1]{\GTenHLStroke{GTenHLProbability}{#1}}
\newcommand{\GTenHLParameter}[1]{\GTenHLStroke{GTenHLParameter}{#1}}
\newcommand{\HLExpectedValue}[1]{%
  \HighlightStroke{ExpectedValueColor}{#1}}
\newcommand{\CtwoTtwoMean}[1]{\HighlightStroke{G11T2C1PopulationMean}{#1}}
\newcommand{\CtwoTtwoPoint}[1]{\HighlightStroke{G11T2C1SampleMean}{#1}}
\newcommand{\CtwoTtwoSD}[1]{\HighlightStroke{G11T2C1PopulationSD}{#1}}
\newcommand{\CtwoTtwoSize}[1]{\HighlightStroke{G11T2C1Sample}{#1}}
\newcommand{\CtwoTtwoSE}[1]{\HighlightStroke{CtwoSEColor}{#1}}
\newcommand{\CtwoTtwoMoE}[1]{\HighlightStroke{CtwoMoEColor}{#1}}
\newcommand{\CtwoTtwoEndpoint}[1]{\HighlightStroke{CtwoEndpointColor}{#1}}
\newcommand{\CtwoTtwoWidth}[1]{\HighlightStroke{CtwoWidthColor}{#1}}
\newcommand{\CtwoTtwoConfidence}[1]{\HighlightStroke{CtwoConfidenceColor}{#1}}
\newcommand{\CtwoTtwoCritical}[1]{\HighlightStroke{CtwoCriticalColor}{#1}}
\newcommand{\CtwoTtwoCoverage}[1]{\HighlightStroke{GTenHLOutcome}{#1}}
\expandafter\newcommand\csname coordinatedrole@outcome\endcsname[1]{\GTenHLOutcome{#1}}
\newcommand{\HLTtwoMathEvent}[1]{\HighlightStroke{GTenHLOutcome}{#1}}
\expandafter\newcommand\csname coordinatedrole@event\endcsname[1]{\HLMathEvent{#1}}
\expandafter\newcommand\csname coordinatedrole@quantity.primary\endcsname[1]{\GTenHLValue{#1}}
\expandafter\newcommand\csname coordinatedrole@quantity.secondary\endcsname[1]{\GTenHLSecond{#1}}
\expandafter\newcommand\csname coordinatedrole@quantity.tertiary\endcsname[1]{\GTenHLThird{#1}}
\newcommand{\HLTtwoPopulationProportion}[1]{\HighlightStroke{G11T2C1PopulationProportion}{#1}}
\newcommand{\HLTtwoProbability}[1]{\GTenHLProbability{#1}}
\newcommand{\HLTtwoSuccessProbability}[1]{\HighlightStroke{MathHLSuccessColor}{#1}}
\expandafter\newcommand\csname coordinatedrole@probability\endcsname[1]{\HLProbability{#1}}
\expandafter\newcommand\csname coordinatedrole@probability.success\endcsname[1]{\HLSuccessProbability{#1}}
\expandafter\newcommand\csname coordinatedrole@proportion.population\endcsname[1]{\HLPopulationProportion{#1}}
\expandafter\newcommand\csname coordinatedrole@unknown\endcsname[1]{\GTenHLParameter{#1}}
\newcommand{\HLTtwoComplementProbability}[1]{\HighlightStroke{MathHLComplementColor}{#1}}
\expandafter\newcommand\csname coordinatedrole@probability.complement\endcsname[1]{\HLComplementProbability{#1}}
\newcommand{\HLTtwoCumulativeProbability}[1]{\HighlightStroke{MathHLCumulativeColor}{#1}}
\expandafter\newcommand\csname coordinatedrole@cumulative\endcsname[1]{\HLCumulativeProbability{#1}}
\newcommand{\HLTtwoObservationCount}[1]{\HighlightStroke{G11T2C1Sample}{#1}}
\expandafter\newcommand\csname coordinatedrole@count.design\endcsname[1]{\HLObservationCount{#1}}
\newcommand{\HLTtwoModelControl}[1]{\HighlightStroke{GTenHLParameter}{#1}}
\expandafter\newcommand\csname coordinatedrole@model.control\endcsname[1]{\HLModelControl{#1}}
\newcommand{\HLTtwoPopulationMean}[1]{\HighlightStroke{G11T2C1PopulationMean}{#1}}
\expandafter\newcommand\csname coordinatedrole@expectation\endcsname[1]{\HLExpectedValue{#1}}
\expandafter\newcommand\csname coordinatedrole@mean.population\endcsname[1]{\HLPopulationMean{#1}}
\newcommand{\HLTtwoPoissonMean}[1]{\HighlightStroke{MathHLPoissonMeanColor}{#1}}
\expandafter\newcommand\csname coordinatedrole@mean.poisson\endcsname[1]{\HLPoissonMean{#1}}
\newcommand{\HLTtwoPopulationVariance}[1]{\HighlightStroke{MathHLPopulationVarianceColor}{#1}}
\expandafter\newcommand\csname coordinatedrole@variance.population\endcsname[1]{\HLPopulationVariance{#1}}
\newcommand{\HLTtwoPopulationSD}[1]{\HighlightStroke{G11T2C1PopulationSD}{#1}}
\expandafter\newcommand\csname coordinatedrole@sd.population\endcsname[1]{\HLPopulationSD{#1}}
\expandafter\newcommand\csname coordinatedrole@context\endcsname[1]{\HLMathContext{#1}}
\newcommand{\HLTtwoSampleGroup}[1]{\HighlightStroke{G11T2C1SampleGroup}{#1}}
\expandafter\newcommand\csname coordinatedrole@group.sample\endcsname[1]{\HLSampleGroup{#1}}
\newcommand{\HLTtwoPopulationGroup}[1]{\HighlightStroke{G11T2C1Population}{#1}}
\expandafter\newcommand\csname coordinatedrole@group.population\endcsname[1]{\HLPopulationGroup{#1}}
\newcommand{\HLTtwoSampleMean}[1]{\HighlightStroke{G11T2C1SampleMean}{#1}}
\expandafter\newcommand\csname coordinatedrole@mean.sample\endcsname[1]{\HLSampleMean{#1}}
\newcommand{\HLTtwoSampleSD}[1]{\HighlightStroke{G11T2C1SampleSD}{#1}}
\expandafter\newcommand\csname coordinatedrole@sd.sample\endcsname[1]{\HLSampleSD{#1}}
\newcommand{\HLTtwoSampleVariance}[1]{\HighlightStroke{MathHLSampleVarianceColor}{#1}}
\expandafter\newcommand\csname coordinatedrole@variance.sample\endcsname[1]{\HLSampleVariance{#1}}
\newcommand{\HLTtwoSampleProportion}[1]{\HighlightStroke{G11T2C1SampleProportion}{#1}}
\expandafter\newcommand\csname coordinatedrole@proportion.sample\endcsname[1]{\HLSampleProportion{#1}}
\newcommand{\HLTtwoStandardError}[1]{\HighlightStroke{CtwoSEColor}{#1}}
\expandafter\newcommand\csname coordinatedrole@standard.error\endcsname[1]{\HLStandardError{#1}}
\newcommand{\HLTtwoConfidence}[1]{\HighlightStroke{CtwoConfidenceColor}{#1}}
\expandafter\newcommand\csname coordinatedrole@confidence\endcsname[1]{\HLConfidence{#1}}
\newcommand{\HLTtwoTailArea}[1]{\HighlightStroke{MathHLTailColor}{#1}}
\expandafter\newcommand\csname coordinatedrole@tail\endcsname[1]{\HLTailArea{#1}}
\newcommand{\HLTtwoCriticalValue}[1]{\HighlightStroke{CtwoCriticalColor}{#1}}
\expandafter\newcommand\csname coordinatedrole@critical\endcsname[1]{\HLCriticalValue{#1}}
\newcommand{\HLTtwoMarginOfError}[1]{\HighlightStroke{CtwoMoEColor}{#1}}
\expandafter\newcommand\csname coordinatedrole@margin\endcsname[1]{\HLMarginOfError{#1}}
\newcommand{\HLTtwoIntervalBounds}[1]{\HighlightStroke{MathHLBoundsColor}{#1}}
\expandafter\newcommand\csname coordinatedrole@bounds\endcsname[1]{\HLIntervalBounds{#1}}
\newcommand{\HLTtwoIntervalWidth}[1]{\HighlightStroke{MathHLWidthColor}{#1}}
\expandafter\newcommand\csname coordinatedrole@width\endcsname[1]{\HLIntervalWidth{#1}}
\newcommand{\HLTtwoObservedCoverage}[1]{\HighlightStroke{GTenHLOutcome}{#1}}
\expandafter\newcommand\csname coordinatedrole@coverage\endcsname[1]{\HLObservedCoverage{#1}}
\newcommand{\HLTtwoCoverageError}[1]{\HighlightStroke{CtwoErrorColor}{#1}}
\expandafter\newcommand\csname coordinatedrole@coverage.error\endcsname[1]{\HLCoverageError{#1}}
\newcommand{\CoordinatedRole}[2]{\csname coordinatedrole@#1\endcsname{#2}}
\newcommand{\CtwoMean}[1]{\CtwoTtwoMean{#1}}
\newcommand{\CtwoPoint}[1]{\CtwoTtwoPoint{#1}}
\newcommand{\CtwoSD}[1]{\CtwoTtwoSD{#1}}
\newcommand{\CtwoSize}[1]{\CtwoTtwoSize{#1}}
\newcommand{\CtwoSE}[1]{\CtwoTtwoSE{#1}}
\newcommand{\CtwoMoE}[1]{\CtwoTtwoMoE{#1}}
\newcommand{\CtwoEndpoint}[1]{\CtwoTtwoEndpoint{#1}}
\newcommand{\CtwoWidth}[1]{\CtwoTtwoWidth{#1}}
\newcommand{\CtwoConfidence}[1]{\CtwoTtwoConfidence{#1}}
\newcommand{\CtwoCritical}[1]{\CtwoTtwoCritical{#1}}
\newcommand{\CtwoCoverage}[1]{\CtwoTtwoCoverage{#1}}
\newcommand{\HLMathEvent}[1]{\HLTtwoMathEvent{#1}}
\newcommand{\HLPopulationProportion}[1]{\HLTtwoPopulationProportion{#1}}
\newcommand{\HLProbability}[1]{\HLTtwoProbability{#1}}
\newcommand{\HLSuccessProbability}[1]{\HLTtwoSuccessProbability{#1}}
\newcommand{\HLComplementProbability}[1]{\HLTtwoComplementProbability{#1}}
\newcommand{\HLCumulativeProbability}[1]{\HLTtwoCumulativeProbability{#1}}
\newcommand{\HLObservationCount}[1]{\HLTtwoObservationCount{#1}}
\newcommand{\HLModelControl}[1]{\HLTtwoModelControl{#1}}
\newcommand{\HLPopulationMean}[1]{\HLTtwoPopulationMean{#1}}
\newcommand{\HLPoissonMean}[1]{\HLTtwoPoissonMean{#1}}
\newcommand{\HLPopulationVariance}[1]{\HLTtwoPopulationVariance{#1}}
\newcommand{\HLPopulationSD}[1]{\HLTtwoPopulationSD{#1}}
\newcommand{\HLSampleGroup}[1]{\HLTtwoSampleGroup{#1}}
\newcommand{\HLPopulationGroup}[1]{\HLTtwoPopulationGroup{#1}}
\newcommand{\HLSampleMean}[1]{\HLTtwoSampleMean{#1}}
\newcommand{\HLSampleSD}[1]{\HLTtwoSampleSD{#1}}
\newcommand{\HLSampleVariance}[1]{\HLTtwoSampleVariance{#1}}
\newcommand{\HLSampleProportion}[1]{\HLTtwoSampleProportion{#1}}
\newcommand{\HLStandardError}[1]{\HLTtwoStandardError{#1}}
\newcommand{\HLConfidence}[1]{\HLTtwoConfidence{#1}}
\newcommand{\HLTailArea}[1]{\HLTtwoTailArea{#1}}
\newcommand{\HLCriticalValue}[1]{\HLTtwoCriticalValue{#1}}
\newcommand{\HLMarginOfError}[1]{\HLTtwoMarginOfError{#1}}
\newcommand{\HLIntervalBounds}[1]{\HLTtwoIntervalBounds{#1}}
\newcommand{\HLIntervalWidth}[1]{\HLTtwoIntervalWidth{#1}}
\newcommand{\HLObservedCoverage}[1]{\HLTtwoObservedCoverage{#1}}
\newcommand{\HLCoverageError}[1]{\HLTtwoCoverageError{#1}}
\newcommand{\GTenToneHL}[2]{\csname tonerole@#1\endcsname{#2}}
\expandafter\newcommand\csname tonerole@alternative\endcsname[1]{\HighlightStroke{GTenToneAlternativeColor}{#1}}
\expandafter\newcommand\csname tonerole@state\endcsname[1]{\HighlightStroke{GTenToneOutcomeColor}{#1}}
\expandafter\newcommand\csname tonerole@payoff\endcsname[1]{\HighlightStroke{GTenToneQuantityColor}{#1}}
\expandafter\newcommand\csname tonerole@quantity\endcsname[1]{\HighlightStroke{GTenToneQuantityColor}{#1}}
\expandafter\newcommand\csname tonerole@revenue\endcsname[1]{\HighlightStroke{GTenToneSecondaryColor}{#1}}
\expandafter\newcommand\csname tonerole@cost\endcsname[1]{\HighlightStroke{GTenToneCostColor}{#1}}
\expandafter\newcommand\csname tonerole@rate\endcsname[1]{\HighlightStroke{GTenToneRateColor}{#1}}
\expandafter\newcommand\csname tonerole@fixed\endcsname[1]{\HighlightStroke{GTenToneFixedColor}{#1}}
\expandafter\newcommand\csname tonerole@probability\endcsname[1]{\HighlightStroke{GTenToneProbabilityColor}{#1}}
\expandafter\newcommand\csname tonerole@complement\endcsname[1]{\HighlightStroke{GTenToneComplementColor}{#1}}
\expandafter\newcommand\csname tonerole@expected\endcsname[1]{\HighlightStroke{GTenToneExpectedValueColor}{#1}}
\expandafter\newcommand\csname tonerole@best\endcsname[1]{\HighlightStroke{GTenToneBestColor}{#1}}
\expandafter\newcommand\csname tonerole@worst\endcsname[1]{\HighlightStroke{GTenToneWorstColor}{#1}}
\expandafter\newcommand\csname tonerole@benchmark\endcsname[1]{\HighlightStroke{GTenToneBenchmarkColor}{#1}}
\expandafter\newcommand\csname tonerole@regret\endcsname[1]{\HighlightStroke{GTenToneRegretColor}{#1}}
\expandafter\newcommand\csname tonerole@maxregret\endcsname[1]{\HighlightStroke{GTenToneMaxRegretColor}{#1}}
\expandafter\newcommand\csname tonerole@retained\endcsname[1]{\HighlightStroke{GTenToneRetainedColor}{#1}}
\expandafter\newcommand\csname tonerole@eliminated\endcsname[1]{\HighlightStroke{GTenToneEliminatedColor}{#1}}
\newcommand{\ConeToneVariable}[1]{\HighlightStroke{ConeToneValueColor}{#1}}
\expandafter\newcommand\csname g11tone@role@variable\endcsname[1]{\ConeToneVariable{#1}}
\newcommand{\ConeToneSecond}[1]{\HighlightStroke{ConeToneSecondColor}{#1}}
\expandafter\newcommand\csname g11tone@role@second\endcsname[1]{\ConeToneSecond{#1}}
\newcommand{\ConeToneOutcome}[1]{\HighlightStroke{ConeToneOutcomeColor}{#1}}
\expandafter\newcommand\csname g11tone@role@outcome\endcsname[1]{\ConeToneOutcome{#1}}
\newcommand{\ConeToneProbability}[1]{\HighlightStroke{ConeToneProbabilityColor}{#1}}
\expandafter\newcommand\csname g11tone@role@probability\endcsname[1]{\ConeToneProbability{#1}}
\newcommand{\ConeToneSuccess}[1]{\HighlightStroke{ConeToneSuccessColor}{#1}}
\expandafter\newcommand\csname g11tone@role@success\endcsname[1]{\ConeToneSuccess{#1}}
\newcommand{\ConeToneComplement}[1]{\HighlightStroke{ConeToneComplementColor}{#1}}
\expandafter\newcommand\csname g11tone@role@complement\endcsname[1]{\ConeToneComplement{#1}}
\newcommand{\ConeToneUnknown}[1]{\HighlightStroke{ConeToneParameterColor}{#1}}
\expandafter\newcommand\csname g11tone@role@unknown\endcsname[1]{\ConeToneUnknown{#1}}
\newcommand{\ConeToneCDF}[1]{\HighlightStroke{ConeToneCumulativeColor}{#1}}
\expandafter\newcommand\csname g11tone@role@cdf\endcsname[1]{\ConeToneCDF{#1}}
\newcommand{\CtwoToneDensity}[1]{\HighlightStroke{CtwoToneDensityColor}{#1}}
\expandafter\newcommand\csname g11tone@role@density\endcsname[1]{\CtwoToneDensity{#1}}
\newcommand{\CtwoToneSlope}[1]{\HighlightStroke{CtwoToneSlopeColor}{#1}}
\expandafter\newcommand\csname g11tone@role@slope\endcsname[1]{\CtwoToneSlope{#1}}
\newcommand{\CtwoToneMode}[1]{\HighlightStroke{CtwoToneModeColor}{#1}}
\expandafter\newcommand\csname g11tone@role@mode\endcsname[1]{\CtwoToneMode{#1}}
\newcommand{\CThreeTonePeriod}[1]{\HighlightStroke{CThreeTonePeriodColor}{#1}}
\expandafter\newcommand\csname g11tone@role@period\endcsname[1]{\CThreeTonePeriod{#1}}
\newcommand{\CfourToneRate}[1]{\HighlightStroke{CfourToneRateColor}{#1}}
\expandafter\newcommand\csname g11tone@role@rate\endcsname[1]{\CfourToneRate{#1}}
\newcommand{\CfiveToneExpected}[1]{\HighlightStroke{CfiveToneExpectedColor}{#1}}
\expandafter\newcommand\csname g11tone@role@expected\endcsname[1]{\CfiveToneExpected{#1}}
\newcommand{\ConeTonePoissonMean}[1]{\HighlightStroke{ConeTonePoissonMeanColor}{#1}}
\expandafter\newcommand\csname g11tone@role@poisson\endcsname[1]{\ConeTonePoissonMean{#1}}
\newcommand{\CfiveTonePopulationMean}[1]{\HighlightStroke{CfiveTonePopulationMeanColor}{#1}}
\expandafter\newcommand\csname g11tone@role@mean\endcsname[1]{\CfiveTonePopulationMean{#1}}
\newcommand{\CfiveTonePopulationVariance}[1]{\HighlightStroke{CfiveTonePopulationVarianceColor}{#1}}
\expandafter\newcommand\csname g11tone@role@variance\endcsname[1]{\CfiveTonePopulationVariance{#1}}
\newcommand{\CfiveTonePopulationSD}[1]{\HighlightStroke{CfiveTonePopulationSDColor}{#1}}
\expandafter\newcommand\csname g11tone@role@sd\endcsname[1]{\CfiveTonePopulationSD{#1}}
\newcommand{\CsevenToneSampleMean}[1]{\HighlightStroke{CsevenToneSampleMeanColor}{#1}}
\expandafter\newcommand\csname g11tone@role@samplemean\endcsname[1]{\CsevenToneSampleMean{#1}}
\newcommand{\CsevenToneSampleVariance}[1]{\HighlightStroke{CsevenToneSampleVarianceColor}{#1}}
\expandafter\newcommand\csname g11tone@role@samplevariance\endcsname[1]{\CsevenToneSampleVariance{#1}}
\newcommand{\CsevenToneSampleSD}[1]{\HighlightStroke{CsevenToneSampleSDColor}{#1}}
\expandafter\newcommand\csname g11tone@role@samplesd\endcsname[1]{\CsevenToneSampleSD{#1}}
\newcommand{\CsixToneCount}[1]{\HighlightStroke{CsixToneCountColor}{#1}}
\expandafter\newcommand\csname g11tone@role@count\endcsname[1]{\CsixToneCount{#1}}
\newcommand{\CsixToneEmpirical}[1]{\HighlightStroke{CsixToneEmpiricalColor}{#1}}
\expandafter\newcommand\csname g11tone@role@empirical\endcsname[1]{\CsixToneEmpirical{#1}}
\newcommand{\CsixToneAbsoluteError}[1]{\HighlightStroke{CsixToneAbsoluteErrorColor}{#1}}
\expandafter\newcommand\csname g11tone@role@absolute\endcsname[1]{\CsixToneAbsoluteError{#1}}
\newcommand{\CsixToneRelativeError}[1]{\HighlightStroke{CsixToneRelativeErrorColor}{#1}}
\expandafter\newcommand\csname g11tone@role@relative\endcsname[1]{\CsixToneRelativeError{#1}}
\newcommand{\CeightToneControl}[1]{\HighlightStroke{ConeToneParameterColor}{#1}}
\expandafter\newcommand\csname g11tone@role@control\endcsname[1]{\CeightToneControl{#1}}
\newcommand{\CeightToneCritical}[1]{\HighlightStroke{CeightToneCriticalColor}{#1}}
\expandafter\newcommand\csname g11tone@role@critical\endcsname[1]{\CeightToneCritical{#1}}
\newcommand{\CeightToneTail}[1]{\HighlightStroke{CeightToneTailColor}{#1}}
\expandafter\newcommand\csname g11tone@role@tail\endcsname[1]{\CeightToneTail{#1}}
\newcommand{\CeightToneBounds}[1]{\HighlightStroke{CeightToneBoundsColor}{#1}}
\expandafter\newcommand\csname g11tone@role@bounds\endcsname[1]{\CeightToneBounds{#1}}
\newcommand{\CeightToneScale}[1]{\HighlightStroke{CeightToneScaleColor}{#1}}
\expandafter\newcommand\csname g11tone@role@scale\endcsname[1]{\CeightToneScale{#1}}
\newcommand{\CeightToneSE}[1]{\HighlightStroke{CtwoSEColor}{#1}}
\expandafter\newcommand\csname g11tone@role@se\endcsname[1]{\CeightToneSE{#1}}
\newcommand{\CeightToneLocation}[1]{\HighlightStroke{CeightToneLocationColor}{#1}}
```

`count.design` / `\HLObservationCount` also treats population size `N` when explicitly selected by a population-size context, using the existing count palette. This does not redefine `N` as sample size or the population group as a count. Coverage counts `N(C)` and `N_{\rm cover}(C)` retain coverage treatment. Transformation names remain unmarked context notation by default. In the G10 Term 2 C3 activity only, `transformation.function.c3` / `\HLGtenCThreeFunction` marks `f` and indexed function symbols using `G10T2C3FunctionColor`; evaluated state payoffs retain the secondary monetary wrapper. Other contexts keep their existing mappings.
