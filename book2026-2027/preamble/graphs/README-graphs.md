# Directory Summary

## Purpose

Reusable LaTeX macros for economic and probability graphs in the 2026–2027 teaching materials.

## Files

| File | Type | Purpose |
|---|---|---|
| `G10_T1_C7_graphs.tex` | LaTeX | Plots expected monetary value against subjective probability. |
| `G11_C4.tex` | LaTeX | Draws exponential density graphs with shaded probability regions. |
| `G11_C5_graphs.tex` | LaTeX | Draws distribution density graphs, including compact variants. |
| `G11_C6C7_graphs.tex` | LaTeX | Draws normal density graphs, sample histograms, and overlays. |
| `normal_distribution_graphs.tex` | LaTeX | Draws standard-normal tails, intervals, complements, and symmetry. |
| `probability_distribution_graphs.tex` | LaTeX | Compares uniform, triangular, and normal densities. |
| `uniform_linear_probability_distributions.tex` | LaTeX | Draws uniform, linear, and piecewise densities with highlighted regions. |
| `README.md` | Markdown | Summarizes this directory. |

## Folders

None.

## Directory Structure

```text
graphs/
├── G10_T1_C7_graphs.tex
├── G11_C4.tex
├── G11_C5_graphs.tex
├── G11_C6C7_graphs.tex
├── normal_distribution_graphs.tex
├── probability_distribution_graphs.tex
├── uniform_linear_probability_distributions.tex
└── README.md
```

## Public Commands

| File | Commands |
|---|---|
| `G10_T1_C7_graphs.tex` | `\EMVGraph` |
| `G11_C4.tex` | `\ExponentialProbabilityGraph`, `\ExponentialLessThanGraph`, `\ExponentialGreaterThanGraph` |
| `G11_C5_graphs.tex` | `\UniformGraph`, `\TriangularGraph`, `\LinearIncreasingGraph`, `\LinearDecreasingGraph`, `\ExponentialGraph`, `\NormalGraph`, `\CompactUniformGraph`, `\CompactTriangularGraph`, `\CompactLinearIncreasingGraph`, `\CompactLinearDecreasingGraph`, `\CompactTrapezoidalGraph`, `\CompactExponentialGraph`, `\CompactNormalGraph` |
| `G11_C6C7_graphs.tex` | `\CNormalPDFGraph`, `\CSampleHistogramNormal`, `\CNormalPDFAndHistogram`, `\CSampleHistogramTwenty`, `\CSampleHistogramHundred`, `\CSampleHistogramThousand`, `\CSampleCountHistogramTwenty`, `\CSampleCountHistogramHundred`, `\CSampleCountHistogramThousand` |
| `normal_distribution_graphs.tex` | `\StandardNormalLeftTailGraph`, `\StandardNormalComplementMirrorGraph`, `\StandardNormalSymmetryGraph`, `\StandardNormalRightTailGraph`, `\StandardNormalRightTailGraphSmall`, `\StandardNormalLeftTailOrangeGraphSmall`, `\StandardNormalCentralBandGraph`, `\StandardNormalTwoTailGraph`, `\StdLeft`, `\StdRight`, `\StdBand`, `\StdTwo`, `\StdComp`, `\StdSym` |
| `probability_distribution_graphs.tex` | `\UniformThreeGraph`, `\UniformFourGraph`, `\TriangularThreeGraph`, `\TriangularFourGraph`, `\NormalTwoGraph`, `\NormalThreeGraph`, `\NormalFourGraph` |
| `uniform_linear_probability_distributions.tex` | `\PiecewiseProbGraph`, `\CompactDensityCoordinatesGraph`, `\UniformEndpointGraph`, `\UniformVariableEndpointsGraph`, `\UniformGuideSet`, `\COneGraph`, `\COneCompareGraph`, `\CtwoProbGraph`, `\CtwoThresholdGraph`, `\LinearProbGraph`, `\LinearThresholdGraph`, `\InvestmentUniformDensityGraph`, `\InvestmentThresholdGraph` |
| `README.md` | None. |
