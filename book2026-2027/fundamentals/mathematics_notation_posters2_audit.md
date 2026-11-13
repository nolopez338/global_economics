# Audit and implemented content plan

The two original posters were read together before selecting additions. Status below describes the original source, not the revised posters. **Essential** means a prerequisite, an unexplained symbol, or a clarification needed to prevent a predictable misconception. **Useful** means a small supporting addition within the existing sections. All entries in the main table were implemented; optional candidates follow separately.

The original source and PDF were preserved. The revision retains two portrait A4 pages, the original palette, table style, and all central font-size settings (9 pt definitions, 8.8 pt examples). Row spacing and repeated examples were rebalanced; no text was scaled down.

## Repository scope

Paths below are relative to the repository root. These materials establish applications, not a requirement to import all their formulas:

- `book2026-2027/fundamentals/basic_algebra.tex`, sections 1–2: juxtaposition, powers, variables, fixed coefficients, and implication in solving linear equations.
- `book2026-2027/grade10/term_1/1-practice_activities/G10_T1_L1_C1C3_practice_activity.tex`, Introduction: alternatives `A_i`, states `S_j`, function arguments, and payoff notation. This supports indices as labels beyond sequence positions.
- `book2026-2027/grade10/term_1/1-practice_activities/G10_T1_L1_C1C2_practice_activity-alternate-descriptions.tex`, introductory notation explanation: finite lists, ellipses, index bounds, and row/column labels.
- `book2026-2027/grade10/term_1/1-practice_activities/G10_T1_L2_C6_practice_activity.tex`, Expected Value Criterion: products, finite sums, indexed probabilities, and the expanded sum containing centered dots. The EMV and optimization formulas remain outside these posters.
- `book2026-2027/fundamentals/probability_challenge.tex`, instructions and problems 5 and 7: equally likely outcomes, independence, and probabilities conditioned on given information.
- `book2026-2027/grade10/term_1/1-practice_activities/G10_T1_L3_C8_practice_activity.tex`, opening conventions: mutually exclusive states.
- `book2026-2027/grade10/term_2/1-practice_activities/G10_T2_L1_C1_practice_activity.tex`, notation guide and independent-outcomes task: outcome/sample-space notation, context-specific uppercase/lowercase roles, and independence as unchanged probabilities.
- `book2026-2027/grade11/term_3/1-practice_activities/G11_T3_L1_C1C2C3_practice_activity.tex`, introduction: Greek parameter names, constants, and benchmark subscripts. Statistical definitions and testing formulas are outside scope.

The existing square-function and square-root examples themselves justify domain, range, real-number, and interval clarifications. An exhaustive course-wide symbol catalogue would exceed the posters' purpose.

## Prioritized findings

| Priority | Missing item / original status | Proposed poster and section | Why it belongs | Concise student-facing definition | Correct example |
|---|---|---|---|---|---|
| Essential | Ellipses `…` and `⋯` — **used but unexplained** | 2: Lists, sequences and subscripts; brief reuse in Summation | Both forms occur repeatedly; readers need to distinguish a finite list from indefinite continuation. | Dots indicate omitted entries following an established pattern. A final term marks the end; dots alone do not specify a unique rule. | `1,2,3,…,n` ends at `n` (`n≥3`); `1,2,3,…` continues indefinitely. `a₁+a₂+⋯+aₙ` omits intermediate summands. |
| Essential | Set-builder notation and “such that” — **used but unexplained** | 1: Sets and number systems | The original empty-set example uses `{x∈ℝ:x²=−1}` without explaining the construction or colon. | `{x∈A:p(x)}` contains the elements of `A` satisfying condition `p(x)`; `:` or `|` means “such that”. | `{x∈ℝ:x>0}` is the set of positive real numbers. |
| Essential | Half-open intervals and infinity — **used but unexplained** | 1: Sets and number systems | Poster 2 uses `[0,∞)` before either convention is taught. | A bracket includes an endpoint; a parenthesis excludes it. Infinity denotes an unbounded direction, is not a real number, and always takes a parenthesis. | `[0,∞)={x∈ℝ:x≥0}`; `2∈[2,5)` and `5∉[2,5)`. |
| Essential | Open/closed interval definitions — **present but incomplete** | 1: Sets and number systems | Names and membership examples are present, but endpoint rules and real-number interpretation are unstated. | For `a<b`, `(a,b)` excludes both endpoints; `[a,b]` includes both. | `x∈(1,3)` means `1<x<3`; `x∈[1,3]` means `1≤x≤3`. |
| Essential | Function as a single-output assignment — **present but incomplete** | 2: Function notation | “Name of a function” supplies no prerequisite definition of a function. | A function assigns exactly one output to each input in its domain. | `f:ℝ→ℝ`, `f(x)=x²`, gives the single output `9` at input `3`. |
| Essential | Domain — **present but incomplete**; codomain — **absent**; range — **absent** | 2: Function notation | Domain is only named; “from A to B” can suggest every element of B must be attained. | Domain: allowed inputs. Codomain: declared output target. Range: outputs actually attained, a subset of the codomain. | For `f:ℝ→ℝ`, `f(x)=x²`, domain and codomain are `ℝ`, but range is `[0,∞)`. |
| Essential | Function evaluation versus multiplication — **present but incomplete** | 2: Function notation | “Value at input” is correct but does not distinguish `f(x)` from juxtaposed multiplication used elsewhere. | In `f(x)`, parentheses identify the input argument. | If `f(x)=x²`, then `f(3)=9`. |
| Essential | Principal square root — **present but incomplete** | 1: General notation | “Square root” alone can invite `√9=±3`. | `√a` is the nonnegative square root; real values require `a≥0`. | `√9=3`, not `±3`; `√(1/4)=1/2`. |
| Essential | Absolute value — **present but incomplete** | 1: General notation | Only a label and examples are provided. | `|a|` is the distance from `a` to zero. | `|−5|=5`, `|0|=0`. |
| Essential | Natural-number zero convention — **present but incomplete** | 1: Sets and number systems | Only positive examples appear, leaving membership of zero undecidable. | Here `ℕ={1,2,3,…}`; some texts include zero, so check their convention. | Under this poster's convention, `1∈ℕ` and `0∉ℕ`, while `0∈ℤ`. |
| Essential | Rational and real numbers — **present but incomplete** | 1: Sets and number systems | Names alone do not explain the distinction shown by `√2` and fractions. | Rationals are ratios of integers with nonzero denominator; reals are the points of the number line. | `1/2∈ℚ`; `−3=−3/1∈ℚ`; `√2∈ℝ`. |
| Essential | Probability scale and counting assumptions — **present but incomplete** | 1: Probability and events | The original counting fractions are correct for fair devices but their validity conditions are unstated. | `0≤P(A)≤1`; `P(Ω)=1`, `P(∅)=0`. Use `|A|/|Ω|` only for a finite space of equally likely outcomes. | For a fair die and odd event `A`, `P(A)=3/6=1/2`. |
| Essential | Complement relative to the sample space — **present but incomplete** | 1: Probability and events | Correct examples are present, but the universal set is implicit. | `Aᶜ` contains the outcomes in `Ω` outside `A`. | For a die and `A={1,3,5}`, `Aᶜ={2,4,6}` and `P(Aᶜ)=1−P(A)=1/2`. |
| Essential | Independence — **used but unexplained** | 1: Probability and events | Original coin context explicitly says “independent”; no meaning is supplied. | Independent events satisfy `P(A∩B)=P(A)P(B)`; if `P(B)>0`, knowing B does not change A's probability. | For independent fair tosses, `E`: first heads, `F`: second heads; `P(E∩F)=1/4=(1/2)(1/2)`. |
| Essential | Indexing conventions — **present but incomplete** | 2: Lists, sequences and subscripts | Index and position are already defined, but the exposition can suggest all indexing starts at one. | An index can identify a position or label; state the starting index. It need not be one. | A sequence may begin with `a₀`; `A₁,A₂` may label alternatives. |
| Useful | Cardinality — **absent** | 1: Sets and number systems | Gives compact meaning to the elementary counting model and distinguishes bars on sets from bars on numbers. | For a finite set A, `|A|` counts its distinct elements. | `|{2,4,6}|=3`; `|∅|=0`. |
| Useful | Subset meaning — **present but incomplete**; proper subset — **absent** | 1: Sets and number systems | The original gives only the subset name and examples; equality versus strict inclusion is unresolved. | `A⊆B`: every element of A is in B, allowing equality. `A⊊B`: additionally `A≠B`. | `{1,2}⊆{1,2}`; `{1}⊊{1,2}`. Use unambiguous `⊊`, not convention-dependent `⊂`. |
| Useful | Set difference — **absent** | 1: Sets and number systems | Supports the irrational set and relates naturally to the event complement. | `A∖B` contains elements in A but not in B. | `{1,2}∖{2,3}={1}`. |
| Useful | Irrationals and full nesting — **absent** (one nesting link is already exemplified) | 1: Sets and number systems | Original examples include `√2` but never identify the non-rational reals; `ℕ⊆ℤ` alone is already present. | Irrationals are `ℝ∖ℚ`. The systems nest as proper subsets. | `√2,π∈ℝ∖ℚ`; `ℕ⊊ℤ⊊ℚ⊊ℝ`. |
| Useful | Mutually exclusive events — **absent** | 1: Probability and events | Connects intersection/empty-set notation to repository states of nature and prevents confusion with independence. | Mutually exclusive events cannot occur together: their intersection is empty. | Odd and even die events are disjoint; if both have positive probability they are not independent. |
| Useful | Conditional probability — **absent** | 1: Probability and events | The repository has elementary “given that” tasks; the bar and reduced sample-space interpretation belong here. | `P(A|B)` is the probability of A given B; `P(A|B)=P(A∩B)/P(B)` requires `P(B)>0`. | For die events `A={1,3,5}`, `B={1,2}`, `P(A|B)=(1/6)/(2/6)=1/2`. |
| Useful | Multiplication and positive integer powers — **used but unexplained** | 1: General notation | `x²`, `2i`, and `2(1)` occur in the original function/sequence examples; a short prerequisite row helps distinguish exponent and subscript. | Juxtaposition and `·` mean multiplication; `aⁿ` has n factors of a for positive integer n. | `2x=2·x`; `3²=3·3=9`. Zero, negative and fractional powers are deliberately not treated. |
| Useful | Pi and uppercase sigma — **used but unexplained** | 2: Letters and Greek symbols | `π` appears in the approximation example; the operator `∑` is already explained but the name/case distinction is absent from the letter reference. | Pi names the circle constant in these examples. `Σ` is uppercase sigma; `∑` is the related summation operator, not an ordinary variable. | `π≈3.14`; `∑ᵢ₌₁³ i=6`. Retain the full definition of summation only in its own section. |
| Useful | Constant versus variable and degree mark — **present but incomplete** / **used but unexplained**, respectively | 2: Variables | Variables are already correctly defined, but fixed letters provide a useful contrast; angle examples use `°` without naming its unit. | A constant stays fixed within a context; a variable takes allowed values. `°` means degrees. | In a chosen line `y=mx+b`, m and b are fixed; x and y vary. `θ=30°`. |
| Useful | Infinite sequences — **absent as an explicit contrast** | 2: Lists, sequences and subscripts | The original thoroughly explains a finite sequence but does not define the indefinitely continuing version. | A finite sequence has a final term; an infinite sequence has no last term. | For `aᵢ=2i`, `(aᵢ)ᵢ₌₁⁴=(2,4,6,8)` and `(aᵢ)ᵢ₌₁^∞=(2,4,6,8,…)`. |
| Useful | `aₙ` versus `Sₙ` — **absent as a contrast** (`aₙ` itself is already explained) | 2: Summation notation | Makes the existing sequence-to-sum transition explicit without adding a closed-form formula. | `aₙ` is one term; define `Sₙ=∑ᵢ₌₁ⁿ aᵢ` as the sum of the first n terms when indexing starts at one. | For `aᵢ=2i`, `a₄=8` while `S₄=20`. |

## Relocate, consolidate, and cross-reference

1. **Set order/repetition:** move its primary explanation and brace examples from Poster 2 to Poster 1's set entry. Poster 2 retains the sequence comparisons and a short cross-reference. This is a relocation, not an absent concept.
2. **Union and intersection:** define set membership meanings once on Poster 1. Keep their probability rows as applications to events (“or, or both” and “and”), explicitly referring left. These applications are useful, not redundant full definitions.
3. **Events:** combine the original “event shown as a set” and “event is a subset of Ω” rows. One definition and one die example suffice.
4. **Example contexts:** use one recurring die context for elementary probability; reserve the two-toss context for the independence example. The original two complete parallel example tracks consumed space and obscured the different jobs of the symbols.
5. **Functions:** use one square-function context to make codomain versus range visible. Remove the parallel square-root track; square-root notation remains in General notation and interval notation has its own primary home. Preserve both arrow types and explain their different jobs.
6. **Domain:** define its meaning together with `f:A→B`; keep `dom(f)` as a notation application, without repeating a full definition.
7. **Sequences:** keep one explicit indexed finite example and one infinite counterpart; remove the separate four-line regeneration of the same four terms. Retain one substitution `a₃=2(3)=6`.
8. **Dots:** teach omission/pattern and finite/infinite contrast once in Lists; refer back briefly when using centered dots in Summation. Poster 1's natural-number list simply reuses dots with a short cross-reference.
9. **Summation:** retain the bounds diagram, inclusive-integer rule, constant and square examples, and index renaming. Replace repeated expansions of `2+4+6+8` with the `a₄`/`S₄` contrast. Drop the additional shifted-linear summand example.
10. **Greek letters and meaning:** the letter table supplies names; Variables explains contextual roles; Probability and Summation supply the meanings of `Ω`, `ω`, and `∑`. Naming and applying these symbols across sections is intentional, not duplicated definition.

## Optional candidates and deliberate omissions

| Candidate / original status | Decision | Accurate definition or example if added later |
|---|---|---|
| Implication and equivalence `⇒`, `⇔` — **absent** | Useful next addition to General notation, supported by basic algebra, but lower priority than symbols already used in these posters. Omitted to preserve two pages and readable spacing. | `⇒`: implies; `⇔`: both directions. `x=2 ⇒ x²=4`; `x+1=3 ⇔ x=2`. |
| Random variable versus value, `P(X=x)` — **absent** | Relevant to Grade 10 Term 2, but better introduced alongside the experiment and random-variable definition. Keep this pair of posters centered on sets/events and general variable conventions. | If X is a fair die result, `P(X=3)=1/6`; `{ω∈Ω:X(ω)=3}` is the event. |
| Exhaustive events / partitions — **absent** | Natural extension for decision-state lessons; omitted as supporting probability structure rather than essential notation here. | Events are exhaustive if their union is Ω. Odd and even die events are exhaustive and mutually exclusive. |
| General addition rule — **absent** | Correct and useful in probability lessons; omitted to avoid turning notation entries into a formula sheet. | `P(A∪B)=P(A)+P(B)−P(A∩B)`. |
| Sample-space complement `A′`, cardinality `n(A)`, subset `⊂`, natural numbers `ℕ₀` — **absent as alternate spellings** | Use one clear convention per concept instead of cataloguing alternatives. Mention the zero convention in words. | If defined locally, `ℕ₀={0,1,2,…}`. `⊂` is avoided because its strictness varies across texts. |
| Complex numbers, universal quantifiers, Cartesian products, inverse/composite functions, limits — **absent** | Outside the introductory focus of the existing sections; no current example needs them. | For a later function lesson, `(f∘g)(x)=f(g(x))`; this is not needed to interpret `f(x)`. |
| Infinite sums, convergence, arithmetic/geometric formulas, nested sums — **absent** | An infinite sequence does not require teaching infinite-series convergence; retain finite summation only. | An infinite sum needs a separate convergence discussion; dots alone do not assign it a finite value. |
| Statistical meanings of every Greek letter, estimates, hats, bars, distribution symbols — **absent as definitions** | Repository courses use them, but permanent assignments would conflict with the posters' context principle and crowd out prerequisites. | In a specified statistics context, `μ` may denote a population mean; it is not the universal meaning of the letter. |
| Fraction notation as a separate arithmetic lesson — **used but unexplained** | Retain basic arithmetic as an entry prerequisite; clarify nonzero denominators where they matter for rationals and conditional probability. | `1/2=0.5`; no catalogue of arithmetic rules is added. |

## Recommended final outline (implemented)

**Poster 1**

1. General notation: equality/inequality, approximation, comparisons, plus/minus, absolute value, principal square root, multiplication and positive integer powers.
2. Sets and number systems: braces and distinct elements; membership; set-builder/such that; empty set and finite cardinality; subset/proper subset; union/intersection/difference; natural-number convention, integers, rationals, reals, irrationals and nesting; open/closed/half-open/unbounded intervals.
3. Probability and events: one die context; sample space and outcome; event subset; probability scale and equally likely counting; complement; event operations; mutual exclusion; conditional probability; independence and its distinction from mutual exclusion.

**Poster 2**

1. Function notation: single-output assignment, evaluation, domain/codomain mapping, value mapping, domain notation, range distinguished from codomain; one square-function context.
2. Letters and Greek symbols: Latin and Greek names, including pi and uppercase sigma; operator versus variable distinction.
3. Variables: context and allowed values, fixed constants, illustrative separate cases, degree unit, fixed coefficients in a chosen line.
4. Lists, sequences and subscripts: ordered terms, series, dots/pattern and finite/infinite contrast, index versus exponent/product, starting index and labels, indexed finite/infinite examples, order/repetition comparison with a set cross-reference.
5. Summation: operator/bounds/index/summand, inclusive integer bounds, expansion, `aₙ` versus `Sₙ`, constant and square summands, local index renaming.

## Validation

- Compiled with pdfLaTeX; final output has exactly two A4 portrait pages.
- Inspected both rendered pages and corrected the initial page spill and a crowded general-notation row.
- Preserved the central font-size definitions and checked the compile log for overfull/underfull boxes and warnings.
- Checked examples against their declared sample spaces, function domain/codomain, index ranges, and the chosen positive-natural-number convention.
- Original source SHA-256: `DC3ED4D654C3811B533DE10803109154BF266CEF70FF6C7E6880B13B493CAAB6`.
