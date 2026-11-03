# C1 graph audit

Added three panels: Notebook buyers outcome-to-revenue mapping; general infinite model outcome probabilities and outcome-to-call-count mapping.

Retained all existing correct graphs, including Notebook buyers revenue PMF. Audited 30 panels across the introductory example and nine worked/contextual problems. Graphs use existing semantic markers; probability bars stay blue and assigned-value fills/labels follow variable roles. Widened crowded rows, standardized graph heights, kept captions in graph minipages and added page-space guards.

Distribution-only models (finite refund, daily claims, investment gain, contextual calls) retain only supplied PMFs. No outcomes were invented. Continuous call duration and exact delivery time have no invented mapping or distribution.

Infinite previews explicitly continue: five stopping outcomes omit 1/32; eight waiting-count values omit 1/256. Bars use original masses without renormalization.

Validation: three successful final pdflatex passes using the repository workflow, no final warnings or over/underfull boxes, 18 pages rendered and inspected as contact sheets, with new infinite/revenue and negative-bonus panels also reviewed at page scale. Exact Fraction checks pass for all graph totals/tails, applicable panel counts, grouped PMFs, mappings, numerical order and semantic graph colors; key probability results checked.

Repository-wide validate_probability.py was attempted but stops on its stale expected heading "Advanced general problem: a finite and an infinite model". The source already has separate finite and infinite model subsections; its structure was preserved. The validator was not changed.
