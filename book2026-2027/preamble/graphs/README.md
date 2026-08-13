# Probability graph utilities

This directory contains reusable LaTeX macro libraries that draw probability
density graphs for the 2026–2027 collection.  They generate TikZ/PGFPlots
figures at compile time; they are not image assets.  The year-local templates
load the libraries with `\input{graphs/<filename>.tex}` after loading
`preamble.tex`.

## Inventory and loading

| File | Purpose | Repository use |
| --- | --- | --- |
| `README.md` | This contributor and usage reference. | Documentation only; it is not included by LaTeX. |
| `normal_distribution_graphs.tex` | Standard-normal tail, band, complement, and symmetry diagrams. | Imported by `preamble/template_practice.tex`, `preamble/template_exam_solved.tex`, Grade 10 Term 3 probability activities/solutions, and several Grade 11 Term 1 files. |
| `probability_distribution_graphs.tex` | Overlays three or four uniform, triangular, or normal densities with a shared legend. | Imported by both templates above and by Grade 10 Term 3 and Grade 11 Term 1 activities/solutions; for example, `grade10/term_3/2-learning_evidences/G10_T3_C1C7_midterm_solutionV2.tex` uses all three four-graph commands. |
| `uniform_linear_probability_distributions.tex` | Single-density, highlighted-interval, threshold, endpoint, and compact investment graphs for uniform, linear, and piecewise densities. | Imported by both templates above and by Grade 10 Term 3 and Grade 11 Term 1 activities/solutions. |

The standard setup is:

```latex
% preamble.tex supplies xparse, TikZ, PGFPlots, and the patterns library.
\input{graphs/uniform_linear_probability_distributions.tex}
\input{graphs/probability_distribution_graphs.tex}
\input{graphs/normal_distribution_graphs.tex}
```

These paths rely on the documents' configured `\input@path` pointing at
`book2026-2027/preamble/`; otherwise use a path appropriate to the compiling
document.  The confirmed shared preamble loads `xparse`, `tikz`, `pgfplots`
with `compat=1.18`, and TikZ's `patterns` library.  All three libraries require
TikZ and PGFPlots; `probability_distribution_graphs.tex` additionally requires
`xparse` (for `\NewDocumentCommand` and `\SplitArgument`) and `patterns`.

No command in this directory has an optional argument.  Every argument shown
below is required.

## `normal_distribution_graphs.tex`

All full-size commands create a centered `11cm` by `6cm` standard-normal plot
on \(z\in[-3.5,3.5]\), \(0\leq\phi(z)\leq0.45\), with a grid, dashed bounds,
and a black density curve.  The two `Small` variants use `6.6cm` by `4.3cm`.
Labels are inserted in math mode by the macros, so pass math content without
surrounding dollar signs.

| Command | Required arguments, in order | Result |
| --- | --- | --- |
| `\StandardNormalLeftTailGraph` | cutoff, cutoff label, region label | Shades `-3.5` to the cutoff in `blue!55`. |
| `\StandardNormalRightTailGraph` | cutoff, cutoff label, region label | Shades the cutoff to `3.5` in `blue!55`. |
| `\StandardNormalRightTailGraphSmall` | cutoff, cutoff label, region label | Compact right-tail version. |
| `\StandardNormalLeftTailOrangeGraphSmall` | cutoff, cutoff label, region label | Compact left-tail version using `orange!70`. |
| `\StandardNormalCentralBandGraph` | left cutoff, right cutoff, left label, right label, region label | Shades the interval between two bounds. |
| `\StandardNormalTwoTailGraph` | left cutoff, right cutoff, left label, right label, left-region label, right-region label | Shades both outside tails. |
| `\StandardNormalComplementMirrorGraph` | cutoff, left-region label, right-region label | Splits at one cutoff: orange left area and dark-green right complement; the bound is automatically labeled `z=<cutoff>`. |
| `\StandardNormalSymmetryGraph` | positive magnitude, left-region label, right-region label | Shades the tails outside `-<magnitude>` and `+<magnitude>` and draws a dotted symmetry axis. |

Convenience wrappers supply the bound labels: `\StdLeft{cutoff}{region}`,
`\StdRight{cutoff}{region}`, `\StdBand{left}{right}{region}`,
`\StdTwo{left}{right}{region}` (the same region text labels both tails),
`\StdComp{cutoff}{left text}{right text}`, and
`\StdSym{magnitude}{left text}{right text}`.

```latex
\StdLeft{1.50}{P(Z<1.50)}
\StdBand{-0.95}{1.05}{P(-0.95<Z<1.05)}
\StdTwo{-1.05}{1.35}{P(Z<-1.05\ \text{or}\ Z>1.35)}
\StdComp{1.50}{P(Z<1.50)=0.9332}{P(Z>1.50)=0.0668}
\StdSym{1.20}{P(Z<-1.20)}{P(Z>1.20)}
```

Cutoffs are used directly in PGF arithmetic, domains, ticks, and coordinates;
they must therefore be numeric PGF expressions appropriate to the fixed
`[-3.5,3.5]` display.  Region-label arrow placement is calculated from the
cutoffs and is fixed near the top of the axes, so unusually long labels or
out-of-range/reversed bounds can overlap or produce misleading plots.

## `probability_distribution_graphs.tex`

The principal overlay commands have five common leading arguments:
`{width}{height}{xmin}{xmax}{ymax}`.  Each remaining braced argument is a
comma-separated parameter tuple—do not replace its commas with separate
braced arguments.

| Commands | Tuple(s) after the five axis arguments | Density and conventions |
| --- | --- | --- |
| `\UniformThreeGraph`, `\UniformFourGraph` | Three/four `{left,right}` tuples | Height is `1/(right-left)`; each support is filled to the axis. |
| `\TriangularThreeGraph`, `\TriangularFourGraph` | Three/four `{left,mode,right}` tuples | Vertices are `(left,0)`, `(mode,2/(right-left))`, `(right,0)`. |
| `\NormalTwoGraph`, `\NormalThreeGraph`, `\NormalFourGraph` | Two/three/four `{mean,standard deviation}` tuples | Normal density is sampled 300 times across the entire displayed x-domain. |

All use left axes labeled \(x\) and \(f(x)\), `ymin=0`, and `grid=both`.
Series A–D are monochrome: increasing black fill opacity (`0.10`, `0.18`,
`0.26`, `0.34`) combined respectively with solid, horizontal-line, densely
dotted, and north-east-line treatments.  Legends are fixed as “Graph A” etc.
at `(1,0.83)`, anchored south-east, through the global PGFPlots style
`SharedLegendPosition`.

```latex
\UniformThreeGraph{10cm}{5.4cm}{0}{8}{0.35}{1,5}{2,6}{3,7}

\TriangularFourGraph
  {7cm}{5cm}{-4}{14}{0.65}
  {-3,-1,1}{-1,2,5}{5,6,7}{5,9,13}

\NormalFourGraph
  {7cm}{5cm}{-2}{10}{0.70}
  {1.0,1.2}{3.0,0.7}{5.0,1.6}{7.0,1.0}
```

The file also exposes implementation helpers
`\UniformPlotA`–`\UniformPlotD`, `\TriangularPlotA`–`\TriangularPlotD`, and
`\NormalPlotA`–`\NormalPlotD`, plus matching `\UniformLegendA`–
`\UniformLegendD`, `\TriangularLegendA`–`\TriangularLegendD`, and
`\NormalLegendA`–`\NormalLegendD` commands.
Plot helpers take the same single-series values described above (normal helpers
instead take `domain minimum`, `domain maximum`, `mean`, `standard deviation`)
and must be used inside a PGFPlots `axis`; legend helpers take one legend label.
They are principally called by the public overlay commands.

Widths must be nonzero, standard deviations must be positive, and tuple values
must be valid PGF math.  The macros do not validate ordering, normalization,
axis bounds, clipping, or whether `ymax` is high enough.  Loading the file more
than once, or defining a command/style with the same global name, causes a
LaTeX definition conflict or style override.

## `uniform_linear_probability_distributions.tex`

The PGFPlots interval graphs use light blue for the full support and darker
blue for a selected interval.  Support-based axes add horizontal padding equal
to 12% of `support end - support start`.

| Command | Required arguments, in order | Purpose / fixed behavior |
| --- | --- | --- |
| `\PiecewiseProbGraph` | support start, support end, PGF density expression, highlight start, highlight end, x-tick list | General piecewise density; fixed `ymax=0.45`, 200 samples. |
| `\COneGraph` | support start, support end, density expression, highlight start, highlight end, x-tick list, `ymax` | General smooth density, 160 samples, thick outline. |
| `\COneCompareGraph` | axis `xmin`, axis `xmax`, domain start, domain end, density expression, `ymax` | Compares the blue expression with a red dashed `1.6` multiple; ticks are fixed at `0,1,2,3,4,5`. |
| `\CtwoProbGraph` | support start, support end, density expression, highlight start, highlight end, x-tick list, `ymax` | Piecewise-constant (`const plot`) density, 400 samples. |
| `\CtwoThresholdGraph` | support start, support end, density expression, threshold, x-tick list, `ymax`, guide height | Red below and green above the threshold; constant plot and dashed threshold guide. |
| `\LinearProbGraph` | support start, support end, density expression, highlight start, highlight end, x-tick list | Linear/smooth density; fixed `ymax=0.075`, 150 samples. |
| `\LinearThresholdGraph` | support start, support end, density expression, threshold, x-tick list, `ymax`, guide height | Red below and green above the threshold; smooth blue curve and dashed guide. |
| `\UniformEndpointGraph` | x scale, x-axis minimum, x-axis maximum, y-axis top, support end, density height, highlight start, highlight end, extra TikZ code | Uniform rectangle whose support is fixed to start at `x=0`; TikZ uses `x=<scale>cm,y=8cm`. |
| `\UniformVariableEndpointsGraph` | x scale, x-axis minimum, x-axis maximum, support start, support end, density height, highlight start, highlight end, extra TikZ code | Arbitrary uniform support; y-axis top is `max(0.18,1.8*density height)`. |
| `\UniformGuideSet` | five `coordinate/label` pairs, guide height | Emits five dashed TikZ guides and math-mode labels; intended for an endpoint graph's final argument. |
| `\InvestmentUniformDensityGraph` | support start, support end, density height, `ymax`, x-tick list | Compact `5.3cm` by `2.6cm` uniform outline, x-label \(v\), no y ticks. |
| `\InvestmentThresholdGraph` | support start, support end, density height, threshold, x-tick list, `ymax` | Compact red/green threshold graph labeled “investment”. |

PGF density expressions use `x` and PGF syntax; repository examples include
the ternary form `x <= 18 ? x/396 : (44-x)/572`.  Tick lists are comma-separated
within their one argument.

```latex
\PiecewiseProbGraph
  {0}{44}{x <= 18 ? x/396 : (44-x)/572}{0}{44}{0,12,18,44}

\LinearThresholdGraph
  {0}{4}{0.06*x}{2.5}{0,1,2,2.5,3,4}{0.28}{0.15}

\UniformVariableEndpointsGraph
  {0.8}{-1}{11}{0.8}{10.2}{0.1}{2.8}{8.4}{%
    \UniformGuideSet{0.8/a}{2.8/2}{7.2/7}{8.4/8}{10.2/b}{0.1}%
  }

\InvestmentThresholdGraph{8}{16}{1/8}{10}{8,10,16}{0.18}
```

The endpoint commands insert their final argument directly inside a
`tikzpicture`; it must be valid TikZ drawing/node code.  The uniform endpoint
variants use raw TikZ coordinates rather than PGFPlots coordinates and assume
the supplied axes, support, highlight, and scale values are mutually
consistent.  None of these commands checks that the highlighted interval or
threshold lies inside the support, that a density integrates to one, or that
the chosen y-limit/guide height contains the graph.

## Maintenance conventions

- Preserve the established blue probability shading and the A–D monochrome
  overlay styles unless all consumers are intentionally migrated.
- Keep numeric expressions PGF-compatible and test boundary cases, negative
  coordinates, tuple splitting, labels, legend placement, and clipping.
- Add a new public macro with an explicit argument contract and a repository
  example.  Prefer the existing `{width}{height}{xmin}{xmax}{ymax}` prefix for
  overlays and `{support start}{support end}{expression}` prefix for single
  densities.
- Update this inventory and the relevant command table whenever a utility is
  added, removed, renamed, or changes arguments.  Because definitions are
  global `\newcommand`s, choose names that do not collide and do not input a
  library twice.
- Compile from a document whose preamble supplies the dependencies; these
  `.tex` files are fragments and cannot be compiled as standalone documents.
