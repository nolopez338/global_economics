# Grade 10 Term 2 probability activities

The nine G10_T1_*_practice_activity.tex files retain the requested filename
prefixes. Their titles and criteria identify **Term 2**. Each contains two
general problems and six contextual problems with complete solutions, grouped
into two foundational, two intermediate and two advanced problems:
**72 worked problems overall**.

## Build

The activities use book2026-2027/preamble/preamble.tex without modifying it.
From this directory, run the following command three times for each source:

    pdflatex -interaction=nonstopmode -halt-on-error G10_T1_L1_C1_practice_activity.tex

Replace the filename for the other eight activities. Three passes allow the
table of contents and navigation references to settle. To keep auxiliary files
outside the source directory, supply -output-directory=<existing-directory>.
The preamble search path also supports compilation from the repository root.

## Numerical and structural validation

From the repository root:

    python book2026-2027/grade10/term_2/1-practice_activities/validate_probability.py

The validation script requires SciPy. It performs **691 checks**, independently
of the source-generation calculations:

- SciPy PMFs, CDFs, survival functions, binary-sequence enumeration and binomial
  tail identities check exact, interval and complementary answers.
- Negative binomial checks explicitly convert total trials into SciPy's
  failures-before-success convention.
- Exact fractions check selected finite sums, transformations and small values.
- Every C8 calculation-table row and total is read from the actual LaTeX and
  checked, including central and second-moment variance formulas.
- Finite PMF normalization, CDF limits, jumps, endpoints and plotted coordinates
  are checked.
- Problem counts, complete solutions, checks, level grouping, Term 2 labels
  and input-reference tables are checked in all nine sources.

Very small values such as 0.00001 are retained exactly. At an exact rounding
tie, the audit allows final-place tolerance because independent floating-point
implementations can lie on opposite sides of that tie.

## Compilation and visual review

Compiled with pdfTeX 1.40.28, TeX Live 2025, using three passes per activity.
All nine builds complete without errors, unresolved references, LaTeX warnings
or overfull boxes.

Rendered page contact sheets were reviewed for all nine activities. The PMF
and CDF graphs, comparison table, model-selection flowchart and calculation
tables were also checked at larger scale. Solution steps stay together and
practice-level headings are kept with the following problem.

The Term 1 reference activities and shared preamble were not edited.
