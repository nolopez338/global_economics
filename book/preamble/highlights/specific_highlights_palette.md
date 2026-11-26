# Palette

[Highlights index](specific_highlights_index.md). LaTeX is authoritative.

Authoritative modules: [highlights_palette.tex](highlights_palette.tex), [tone_highlight_colors.tex](tone_highlight_colors.tex).

`highlights_palette.tex` requires xcolor. All literal HTML declarations occur here, once per RGB value. `\HighlightBasePalette` executes base bindings once when `highlights.tex` loads. Reading the palette through `tone_highlight_colors.tex` initializes only Tone bindings and does not capture the base aliases prematurely. `\HighlightTonePalette` installs Tone names and captures Ttwo aliases once; `tone_highlight_colors.tex` calls it. `\HighlightRegistryPalette` executes registry bindings and snapshots in historical order, then initializes Tone colors if needed. It is called by `specific_highlights.tex`, not ordinary marker loading.

`G10T2C3FunctionColor` is bound in the base palette as `GTenHLSecond!85!black`, a slightly darker monetary green for the opt-in G10 Term 2 C3 transformation-function role. Existing secondary-variable bindings are unchanged.

`\colorlet{alias}{source}` captures the effective color at execution time. It does not follow later source changes. Examples: `GTenTtwoHLValue` captures `ConeToneValueColor` at base loading; `CtwoTtwoEndpointColor` captures the legacy brown before any local interval override. `MathHLSuccessColor` captures `GTenHLProbability!65!CtwoCriticalColor`; `MathHLComplementColor` captures `G11T2C1PopulationProportion`. A forwarding wrapper instead resolves its target at use time; see [roles](specific_highlights_roles.md).

Named overrides create no group: their lifetime is their caller's scope. `\CoordinatedTermTwoPalette` maps `ExpectedValueColor` to `MathHLExpectedValueColor`, `CtwoEndpointColor` to `MathHLBoundsColor`, and `CtwoWidthColor` to `MathHLWidthColor`; it also provides `\CtwoError` if absent. `\CtwoTtwoPracticeIntervalPalette` derives endpoints as `CtwoMoEColor!45!white` and width as `CtwoMoEColor!45!black`. `\CtwoPracticeIntervalPalette` forwards to it. Registry entries group their opt-in overrides; practice callers may select one before deriving graph colors.

`\COneTonePracticePalette` installs TikZ styles `COne Tone probability area` and `COne Tone density curve`. Their code checks the switch at use time: disabled fills are `none` and curves black. Retain the graph's mathematical information.

Edit literals/bindings/overrides here, not in records or viewers. Preserve operation order around snapshots. The following inventory describes literal declarations and binding statements; it is not an alternate editable palette.

| Literal identifier | HTML |
|---|---|
| `HighlightLiteral1` | `FFBB55` |
| `HighlightLiteral2` | `8FD49A` |
| `HighlightLiteral3` | `F1DA55` |
| `HighlightLiteral4` | `BC9DE0` |
| `HighlightLiteral5` | `86BFF0` |
| `HighlightLiteral6` | `ED9DAA` |
| `HighlightLiteral7` | `6500A8` |
| `HighlightLiteral8` | `D6A52A` |
| `HighlightLiteral9` | `D74383` |
| `HighlightLiteral10` | `619CC7` |
| `HighlightLiteral11` | `EC7963` |
| `HighlightLiteral12` | `65C7C1` |
| `HighlightLiteral13` | `C7AE78` |
| `HighlightLiteral14` | `78BFCB` |
| `HighlightLiteral15` | `C595C9` |
| `HighlightLiteral16` | `A3B75A` |
| `HighlightLiteral17` | `E89BBD` |
| `HighlightLiteral18` | `B977A4` |
| `HighlightLiteral19` | `65B68C` |
| `HighlightLiteral20` | `B8A7A1` |
| `HighlightLiteral21` | `9BDD36` |
| `HighlightLiteral22` | `FF765C` |
| `HighlightLiteral23` | `189338` |
| `HighlightLiteral24` | `E42134` |
| `HighlightLiteral25` | `23B895` |
| `HighlightLiteral26` | `173B17` |
| `HighlightLiteral27` | `56A86B` |
| `HighlightLiteral28` | `6B8E23` |
| `HighlightLiteral29` | `B54A45` |
| `HighlightLiteral30` | `75162B` |
| `HighlightLiteral31` | `55C8F0` |
| `HighlightLiteral32` | `2648BB` |
| `HighlightLiteral33` | `F4D94B` |
| `HighlightLiteral34` | `F28A18` |
| `HighlightLiteral35` | `A75A27` |
| `HighlightLiteral36` | `B83769` |
| `HighlightLiteral37` | `43A5C9` |
| `HighlightLiteral38` | `28AFA2` |
| `HighlightLiteral39` | `D95F50` |
| `HighlightLiteral40` | `91B4DC` |
| `HighlightLiteral41` | `8B8FC4` |
| `HighlightLiteral42` | `EBA6CA` |
| `HighlightLiteral43` | `69CDC2` |
| `HighlightLiteral44` | `49AF9B` |
| `HighlightLiteral45` | `D9B884` |
| `HighlightLiteral46` | `AE97D6` |
| `HighlightLiteral47` | `CD91C7` |

Binding operations (in source order; overrides appear within their named commands):

```tex
\colorlet{ConeToneValueColor}{HighlightLiteral1}
\colorlet{GTenHLValue}{ConeToneValueColor}
\colorlet{GTenTtwoHLValue}{ConeToneValueColor}
\colorlet{ConeToneSecondColor}{HighlightLiteral2}
\colorlet{GTenHLSecond}{ConeToneSecondColor}
\colorlet{GTenTtwoHLSecond}{ConeToneSecondColor}
\colorlet{ConeToneThirdColor}{HighlightLiteral3}
\colorlet{GTenHLThird}{ConeToneThirdColor}
\colorlet{GTenTtwoHLThird}{ConeToneThirdColor}
\colorlet{ConeToneOutcomeColor}{HighlightLiteral4}
\colorlet{GTenHLOutcome}{ConeToneOutcomeColor}
\colorlet{GTenTtwoHLOutcome}{ConeToneOutcomeColor}
\colorlet{ConeToneProbabilityColor}{HighlightLiteral5}
\colorlet{GTenHLProbability}{ConeToneProbabilityColor}
\colorlet{GTenTtwoHLProbability}{ConeToneProbabilityColor}
\colorlet{ConeToneParameterColor}{HighlightLiteral6}
\colorlet{GTenHLParameter}{ConeToneParameterColor}
\colorlet{GTenTtwoHLParameter}{ConeToneParameterColor}
\colorlet{ExpectedValueColor}{HighlightLiteral7}
\colorlet{GTenToneQuantityColor}{HighlightLiteral1}
\colorlet{GTenToneSecondaryColor}{HighlightLiteral2}
\colorlet{GTenToneTertiaryColor}{HighlightLiteral3}
\colorlet{GTenToneOutcomeColor}{HighlightLiteral4}
\colorlet{GTenToneProbabilityColor}{HighlightLiteral5}
\colorlet{GTenToneUnknownColor}{HighlightLiteral6}
\colorlet{GTenToneExpectedValueColor}{HighlightLiteral8}
\colorlet{GTenToneComplementColor}{HighlightLiteral9}
\colorlet{GTenToneAlternativeColor}{HighlightLiteral10}
\colorlet{GTenToneCostColor}{HighlightLiteral11}
\colorlet{GTenToneRateColor}{HighlightLiteral12}
\colorlet{GTenToneFixedColor}{HighlightLiteral13}
\colorlet{GTenToneBestColor}{HighlightLiteral14}
\colorlet{GTenToneWorstColor}{HighlightLiteral15}
\colorlet{GTenToneBenchmarkColor}{HighlightLiteral16}
\colorlet{GTenToneRegretColor}{HighlightLiteral17}
\colorlet{GTenToneMaxRegretColor}{HighlightLiteral18}
\colorlet{GTenToneRetainedColor}{HighlightLiteral19}
\colorlet{GTenToneEliminatedColor}{HighlightLiteral20}
\colorlet{GTenTtwoQuantityColor}{GTenToneQuantityColor}
\colorlet{GTenTtwoSecondaryColor}{GTenToneSecondaryColor}
\colorlet{GTenTtwoTertiaryColor}{GTenToneTertiaryColor}
\colorlet{GTenTtwoOutcomeColor}{GTenToneOutcomeColor}
\colorlet{GTenTtwoProbabilityColor}{GTenToneProbabilityColor}
\colorlet{GTenTtwoUnknownColor}{GTenToneUnknownColor}
\colorlet{GTenTtwoExpectedValueColor}{GTenToneExpectedValueColor}
\colorlet{GTenTtwoComplementColor}{GTenToneComplementColor}
\colorlet{CsevenToneSampleMeanColor}{HighlightLiteral21}
\colorlet{G11T2C1SampleMean}{CsevenToneSampleMeanColor}
\colorlet{CfiveTonePopulationMeanColor}{HighlightLiteral22}
\colorlet{G11T2C1PopulationMean}{CfiveTonePopulationMeanColor}
\colorlet{CsevenToneSampleSDColor}{HighlightLiteral23}
\colorlet{G11T2C1SampleSD}{CsevenToneSampleSDColor}
\colorlet{CfiveTonePopulationSDColor}{HighlightLiteral24}
\colorlet{G11T2C1PopulationSD}{CfiveTonePopulationSDColor}
\colorlet{CsixToneEmpiricalColor}{HighlightLiteral25}
\colorlet{G11T2C1SampleProportion}{CsixToneEmpiricalColor}
\colorlet{ConeTonePopulationProportionColor}{HighlightLiteral9}
\colorlet{G11T2C1PopulationProportion}{ConeTonePopulationProportionColor}
\colorlet{CsixToneCountColor}{HighlightLiteral26}
\colorlet{G11T2C1Sample}{CsixToneCountColor}
\colorlet{CsixToneSampleGroupColor}{HighlightLiteral27}
\colorlet{G11T2C1SampleGroup}{CsixToneSampleGroupColor}
\colorlet{CsevenToneSampleVarianceColor}{HighlightLiteral28}
\colorlet{G11T2C1SampleVariance}{CsevenToneSampleVarianceColor}
\colorlet{CfiveTonePopulationVarianceColor}{HighlightLiteral29}
\colorlet{G11T2C1PopulationVariance}{CfiveTonePopulationVarianceColor}
\colorlet{CsixTonePopulationColor}{HighlightLiteral30}
\colorlet{G11T2C1Population}{CsixTonePopulationColor}
\colorlet{CtwoConfidenceColor}{HighlightLiteral31}
\colorlet{CeightToneCriticalColor}{HighlightLiteral32}
\colorlet{CtwoCriticalColor}{CeightToneCriticalColor}
\colorlet{CtwoSEColor}{HighlightLiteral33}
\colorlet{CtwoMoEColor}{HighlightLiteral34}
\colorlet{CtwoEndpointColor}{HighlightLiteral35}
\colorlet{CtwoWidthColor}{HighlightLiteral36}
\colorlet{CtwoEndpointColor}{CtwoMoEColor!45!white}
\colorlet{CtwoWidthColor}{CtwoMoEColor!45!black}
\colorlet{ConeToneCumulativeColor}{HighlightLiteral37}
\colorlet{MathHLCumulativeColor}{ConeToneCumulativeColor}
\colorlet{CsixToneAbsoluteErrorColor}{HighlightLiteral38}
\colorlet{CtwoErrorColor}{CsixToneAbsoluteErrorColor}
\colorlet{ConeToneSuccessColor}{GTenHLProbability!65!CtwoCriticalColor}
\colorlet{MathHLSuccessColor}{ConeToneSuccessColor}
\colorlet{ConeToneComplementColor}{G11T2C1PopulationProportion}
\colorlet{MathHLComplementColor}{ConeToneComplementColor}
\colorlet{CfiveToneVarianceAliasColor}{G11T2C1PopulationVariance}
\colorlet{MathHLPopulationVarianceColor}{CfiveToneVarianceAliasColor}
\colorlet{CsevenToneVarianceAliasColor}{G11T2C1SampleVariance}
\colorlet{MathHLSampleVarianceColor}{CsevenToneVarianceAliasColor}
\colorlet{CeightToneTailColor}{CtwoConfidenceColor!55!CtwoCriticalColor}
\colorlet{MathHLTailColor}{CeightToneTailColor}
\colorlet{CeightToneBoundsColor}{CtwoMoEColor!45!white}
\colorlet{MathHLBoundsColor}{CeightToneBoundsColor}
\colorlet{CeightToneWidthColor}{CtwoMoEColor!45!black}
\colorlet{MathHLWidthColor}{CeightToneWidthColor}
\colorlet{CfiveToneExpectedColor}{HighlightLiteral8}
\colorlet{MathHLExpectedValueColor}{CfiveToneExpectedColor}
\colorlet{ConeTonePoissonMeanColor}{HighlightLiteral39}
\colorlet{MathHLPoissonMeanColor}{ConeTonePoissonMeanColor}
\colorlet{ExpectedValueColor}{MathHLExpectedValueColor}
\colorlet{CtwoEndpointColor}{MathHLBoundsColor}
\colorlet{CtwoWidthColor}{MathHLWidthColor}
\colorlet{CtwoTtwoConfidenceColor}{CtwoConfidenceColor}
\colorlet{CtwoTtwoSEColor}{CtwoSEColor}
\colorlet{CtwoTtwoMoEColor}{CtwoMoEColor}
\colorlet{CtwoTtwoEndpointColor}{CtwoEndpointColor}
\colorlet{CtwoTtwoWidthColor}{CtwoWidthColor}
\colorlet{G11TtwoConeSampleMeanColor}{CsevenToneSampleMeanColor}
\colorlet{G11TtwoConePopulationMeanColor}{CfiveTonePopulationMeanColor}
\colorlet{G11TtwoConeSampleSDColor}{CsevenToneSampleSDColor}
\colorlet{G11TtwoConePopulationSDColor}{CfiveTonePopulationSDColor}
\colorlet{G11TtwoConeSampleProportionColor}{CsixToneEmpiricalColor}
\colorlet{G11TtwoConePopulationProportionColor}{ConeTonePopulationProportionColor}
\colorlet{G11TtwoConeSampleColor}{CsixToneCountColor}
\colorlet{G11TtwoConeSampleGroupColor}{CsixToneSampleGroupColor}
\colorlet{G11TtwoConeSampleVarianceColor}{CsevenToneSampleVarianceColor}
\colorlet{G11TtwoConePopulationVarianceColor}{CfiveTonePopulationVarianceColor}
\colorlet{G11TtwoConePopulationColor}{CsixTonePopulationColor}
\colorlet{CtwoTtwoCriticalColor}{CeightToneCriticalColor}
\colorlet{MathHLTtwoCumulativeColor}{ConeToneCumulativeColor}
\colorlet{CtwoTtwoErrorColor}{CsixToneAbsoluteErrorColor}
\colorlet{MathHLTtwoExpectedValueColor}{CfiveToneExpectedColor}
\colorlet{MathHLTtwoPoissonMeanColor}{ConeTonePoissonMeanColor}
\colorlet{MathHLTtwoSuccessColor}{ConeToneSuccessColor}
\colorlet{MathHLTtwoComplementColor}{ConeToneComplementColor}
\colorlet{MathHLTtwoPopulationVarianceColor}{CfiveToneVarianceAliasColor}
\colorlet{MathHLTtwoSampleVarianceColor}{CsevenToneVarianceAliasColor}
\colorlet{MathHLTtwoTailColor}{CeightToneTailColor}
\colorlet{MathHLTtwoBoundsColor}{CeightToneBoundsColor}
\colorlet{MathHLTtwoWidthColor}{CeightToneWidthColor}
\colorlet{CtwoToneDensityColor}{HighlightLiteral40}
\colorlet{CtwoToneSlopeColor}{HighlightLiteral41}
\colorlet{CtwoToneModeColor}{HighlightLiteral42}
\colorlet{CThreeTonePeriodColor}{HighlightLiteral43}
\colorlet{CfourToneRateColor}{HighlightLiteral44}
\colorlet{CeightToneLocationColor}{HighlightLiteral45}
\colorlet{CeightToneScaleColor}{HighlightLiteral46}
\colorlet{CsixToneRelativeErrorColor}{HighlightLiteral47}
```
