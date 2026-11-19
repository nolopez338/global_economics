# Coordinated mathematical highlight legends — proposal

**Proposal only.** Based on the working-tree sources inspected on 19 November 2026. Current definitions are distinguished from proposed roles, keys and migrations. This task writes only this Markdown proposal; no LaTeX or summary changes are implemented.

Per the latest instruction, omit a C10 legend when no source is available. Grade 10 has C1–C9 sources and no C10 practice source, recorded in the inventory. Grade 11 has C1–C10, including a source-backed C10 legend. The amended principal sequence has 21 sections: Grade 10 general + C1–C9, then Grade 11 general + C1–C10.

Student entries are English, matching all 19 sources; implementation notes are English. Three-column student tables are separate from technical bindings. Each criterion selects from its grade's consolidated catalog. Multiple entries can share roles/colors, with definitions preserving distinctions. General tables are catalogs, not tables to print in full in every practice. No numerical exercise answer, selected option, independent model choice or capstone derivation is disclosed.

Place concise legends before substantial highlighted instruction; retain extended definitions and example-linked interpretations in separate detailed references. Preserve existing anchors/navigation. Do not print a concise registry table twice as both reference layers.

## Grade 10 general legend table

| Symbol or notation | Concept | Brief meaning |
|---|---|---|
| $\omega,\Omega$ | Outcome and sample space | One complete result; all possible complete results. |
| $A,E,E^c,\{X\leq a\}$ | Event and complement | Outcomes meeting a condition; those outside it. |
| $X,x;\ T,t;\ X(\omega)$ | Primary variable and value | Numerical rule and possible value; state the units. |
| $S_X=\{x:P(X=x)>0\}$ | Support | Distinct values with positive probability, in the variable's units. |
| $Y,y;\ Y=f(X),Y_i=f_i(X)$ | Second or transformed variable | Another numerical description, with its own units. |
| $Z,z;\ C$ | Third variable | A third numerical description; an indicator is unitless. |
| $P(A),P(\omega),p_X(x),m_X(x)$ | Probability and mass | Unitless chance of an event or one supported value. |
| $k,q,c,a,w$ | Unknown quantity | A model quantity to determine, with a context-defined domain. |
| $\sum,\binom nk,n!,e,\sim$ | Operations and distribution notation | Sum, count selections, take factorials, use the exponential constant, or name a model. |
| Independence, constant $p$, fixed observation rule | Model conditions | Conditions to check before using the selected distribution. |
| $F_X(a)=P(X\leq a),F_X(a^-)$ | Cumulative probability | Chance up to a cutoff; the left limit excludes the cutoff. |
| $a,b,m,\lfloor x\rfloor$ | Cutoff and integer part | A boundary in the variable's units; specify included endpoints. |
| $K,a,b,c,a_m,b_m,c_m,N_k,b_j,R_m$ | Auxiliary counts and states | Problem-defined counts, recurrence states, balances or survival quantities. |
| $p=P(X=1)$ | Success probability | Chance of the specified state labelled 1, between 0 and 1. |
| $1-p$ | Complement probability | Chance of the complementary state labelled 0. |
| $E(X),\mathbb E[Y_i],\mu$ | Expected value or model mean | Probability-weighted average, in original units. |
| $p_i^*$ | Individual break-even probability | Probability at which the specified expected net payoff is zero. |
| $a,b,f_i(0),f_i(1)$ | Transformation inputs | Scale, fixed addition or state payoffs, with required units. |
| $n$ | Observation count | Fixed trial count or sample size; a positive integer. |
| $T,t;\ F=T-1\text{ or }F=T-r$ | Trials and failures | Total trials include the final success; failures exclude successes. |
| $r$ | Success target | Fixed number of successes required before stopping. |
| $\mathrm{rate},\mathrm{exposure}$ | Rate and exposure | Events per exposure unit and length of the observation window. |
| $\lambda$ | Poisson interval mean | Expected count for the selected exposure. |
| $E(X^2),[E(X)]^2$ | Second moment and squared mean | Average of squares; square of the average. Both use squared units. |
| $\operatorname{Var}(X),\sigma_X^2$ | Variance | Mean squared deviation from the mean; squared units. |
| $\sigma_X,\sigma$ | Population or model standard deviation | Spread of individual values, in original units. |

Implementation bindings (rows follow the student table):

| Row / entry ID | Stable role ID | Supported criteria | Continuity |
|---|---|---|---|
| 1: `outcome` | `outcome` | C1, C2 | Foundation |
| 2: `event` | `event` | C1, C2, C3, C5, C9 | Foundation |
| 3: `variable` | `quantity.primary` | C1, C2, C3, C4, C7, C8, C9 | Foundation |
| 4: `support` | `quantity.primary` | C1, C2, C3, C4, C5, C6, C7, C8, C9 | Foundation |
| 5: `second` | `quantity.secondary` | C1, C3, C4, C5, C6, C7, C8, C9 | Foundation |
| 6: `third` | `quantity.tertiary` | C1 | Foundation |
| 7: `mass` | `probability` | C1, C2, C3, C4, C5, C6, C7, C8, C9 | Foundation |
| 8: `unknown` | `unknown` | C1, C2 | Foundation |
| 9: `ops` | `context` | C1, C2, C4, C6, C7, C8, C9 | Foundation |
| 10: `assume` | `context` | C1, C2, C4, C5, C6, C7, C9 | Foundation |
| 11: `cum` | `cumulative` | C2, C3, C4, C5, C6, C7, C9 | Foundation |
| 12: `cutoff` | `quantity.primary` | C2, C4, C5, C6, C7 | Foundation |
| 13: `aux` | `context` | C2 | Foundation |
| 14: `p` | `probability` | C3, C4, C5, C6, C9 | Foundation |
| 15: `q` | `probability.complement` | C3, C4, C5, C6, C9 | Foundation |
| 16: `expected` | `expectation` | C3, C8 | Foundation |
| 17: `break` | `probability` | C3 | Foundation |
| 18: `transform` | `context` | C3, C8 | Foundation |
| 19: `size` | `count.design` | C4, C6, C9 | Foundation |
| 20: `wait` | `quantity.primary` | C5, C6, C9 | Foundation |
| 21: `target` | `model.control` | C6, C9 | Foundation |
| 22: `rate` | `context` | C7, C9 | Foundation |
| 23: `lambda` | `expectation` | C7, C9 | Foundation |
| 24: `secondmoment` | `expectation` | C8 | Foundation |
| 25: `variance` | `variance.population` | C8 | Foundation |
| 26: `sd` | `sd.population` | C8 | Foundation |

## Grade 10 C1 Legend

Source: [G10_T2_L1_C1_practice_activity.tex](../../../grade10/term_2/1-practice_activities/G10_T2_L1_C1_practice_activity.tex).

| Symbol or notation | Concept | Brief meaning |
|---|---|---|
| $\omega,\Omega$ | Outcome and sample space | One complete result; all possible complete results. |
| $A,E,E^c,\{X\leq a\}$ | Event and complement | Outcomes meeting a condition; those outside it. |
| $X,x;\ T,t;\ X(\omega)$ | Primary variable and value | Numerical rule and possible value; state the units. |
| $S_X=\{x:P(X=x)>0\}$ | Support | Distinct values with positive probability, in the variable's units. |
| $Y,y;\ Y=f(X),Y_i=f_i(X)$ | Second or transformed variable | Another numerical description, with its own units. |
| $Z,z;\ C$ | Third variable | A third numerical description; an indicator is unitless. |
| $P(A),P(\omega),p_X(x),m_X(x)$ | Probability and mass | Unitless chance of an event or one supported value. |
| $k,q,c,a,w$ | Unknown quantity | A model quantity to determine, with a context-defined domain. |
| $\sum,\binom nk,n!,e,\sim$ | Operations and distribution notation | Sum, count selections, take factorials, use the exponential constant, or name a model. |
| Independence, constant $p$, fixed observation rule | Model conditions | Conditions to check before using the selected distribution. |

Implementation row bindings: 1 → `outcome` / `outcome`; 2 → `event` / `event`; 3 → `variable` / `quantity.primary`; 4 → `support` / `quantity.primary`; 5 → `second` / `quantity.secondary`; 6 → `third` / `quantity.tertiary`; 7 → `mass` / `probability`; 8 → `unknown` / `unknown`; 9 → `ops` / `context`; 10 → `assume` / `context`.

Criterion-specific alignment: Reuse `tab:highlight-legend`, `tab:notation-reference` and `subsec:t2-c1-notation-reference`. F is a fee, E an electronic-payment indicator, C a card indicator. Define each variable/unit separately; distinguish outcomes and support. Exact duration is mentioned as continuous without a supplied PMF. Add event/unknown references without disclosing later solutions.

## Grade 10 C2 Legend

Source: [G10_T2_L1_C2_practice_activity.tex](../../../grade10/term_2/1-practice_activities/G10_T2_L1_C2_practice_activity.tex).

| Symbol or notation | Concept | Brief meaning |
|---|---|---|
| $\omega,\Omega$ | Outcome and sample space | One complete result; all possible complete results. |
| $A,E,E^c,\{X\leq a\}$ | Event and complement | Outcomes meeting a condition; those outside it. |
| $X,x;\ T,t;\ X(\omega)$ | Primary variable and value | Numerical rule and possible value; state the units. |
| $S_X=\{x:P(X=x)>0\}$ | Support | Distinct values with positive probability, in the variable's units. |
| $P(A),P(\omega),p_X(x),m_X(x)$ | Probability and mass | Unitless chance of an event or one supported value. |
| $F_X(a)=P(X\leq a),F_X(a^-)$ | Cumulative probability | Chance up to a cutoff; the left limit excludes the cutoff. |
| $k,q,c,a,w$ | Unknown quantity | A model quantity to determine, with a context-defined domain. |
| $a,b,m,\lfloor x\rfloor$ | Cutoff and integer part | A boundary in the variable's units; specify included endpoints. |
| $\sum,\binom nk,n!,e,\sim$ | Operations and distribution notation | Sum, count selections, take factorials, use the exponential constant, or name a model. |
| Independence, constant $p$, fixed observation rule | Model conditions | Conditions to check before using the selected distribution. |
| $K,a,b,c,a_m,b_m,c_m,N_k,b_j,R_m$ | Auxiliary counts and states | Problem-defined counts, recurrence states, balances or survival quantities. |

Implementation row bindings: 1 → `outcome` / `outcome`; 2 → `event` / `event`; 3 → `variable` / `quantity.primary`; 4 → `support` / `quantity.primary`; 5 → `mass` / `probability`; 6 → `cum` / `cumulative`; 7 → `unknown` / `unknown`; 8 → `cutoff` / `quantity.primary`; 9 → `ops` / `context`; 10 → `assume` / `context`; 11 → `aux` / `context`.

Criterion-specific alignment: Reuse `tab:notation-reference` under Notation and graph conventions. Align conditional models, auxiliary counting and finite previews. a may mean cutoff, unknown probability scale or ticket count; r is a conditional failure probability in maintenance, not the C6 target. Recurrence states, reserve balances, counting correspondence and mixture derivations stay in worked material. Conditional independence does not imply unconditional independence. Preserve unequal spacing, open/filled endpoints and omitted tails.

## Grade 10 C3 Legend

Source: [G10_T2_L1_C3_practice_activity.tex](../../../grade10/term_2/1-practice_activities/G10_T2_L1_C3_practice_activity.tex).

| Symbol or notation | Concept | Brief meaning |
|---|---|---|
| $A,E,E^c,\{X\leq a\}$ | Event and complement | Outcomes meeting a condition; those outside it. |
| $X,x;\ T,t;\ X(\omega)$ | Primary variable and value | Numerical rule and possible value; state the units. |
| $S_X=\{x:P(X=x)>0\}$ | Support | Distinct values with positive probability, in the variable's units. |
| $p=P(X=1)$ | Success probability | Chance of the specified state labelled 1, between 0 and 1. |
| $1-p$ | Complement probability | Chance of the complementary state labelled 0. |
| $Y,y;\ Y=f(X),Y_i=f_i(X)$ | Second or transformed variable | Another numerical description, with its own units. |
| $P(A),P(\omega),p_X(x),m_X(x)$ | Probability and mass | Unitless chance of an event or one supported value. |
| $F_X(a)=P(X\leq a),F_X(a^-)$ | Cumulative probability | Chance up to a cutoff; the left limit excludes the cutoff. |
| $E(X),\mathbb E[Y_i],\mu$ | Expected value or model mean | Probability-weighted average, in original units. |
| $p_i^*$ | Individual break-even probability | Probability at which the specified expected net payoff is zero. |
| $a,b,f_i(0),f_i(1)$ | Transformation inputs | Scale, fixed addition or state payoffs, with required units. |

Implementation row bindings: 1 → `event` / `event`; 2 → `variable` / `quantity.primary`; 3 → `support` / `quantity.primary`; 4 → `p` / `probability`; 5 → `q` / `probability.complement`; 6 → `second` / `quantity.secondary`; 7 → `mass` / `probability`; 8 → `cum` / `cumulative`; 9 → `expected` / `expectation`; 10 → `break` / `probability`; 11 → `transform` / `context`.

Criterion-specific alignment: Reuse `tab:notation-reference` with `ex:intro-one`/`ex:intro-two`. m_X aliases a PMF, while f_i maps states to USD. E is an event; E(·)/blackboard-bold E is expectation. All monetary alternatives share the indicator, without independence. Positive payoff does not mean higher success probability. Omit zero-mass values at p=0/1. Keep break-even roots and sign solutions in their original worked sections.

## Grade 10 C4 Legend

Source: [G10_T2_L1_C4_practice_activity.tex](../../../grade10/term_2/1-practice_activities/G10_T2_L1_C4_practice_activity.tex).

| Symbol or notation | Concept | Brief meaning |
|---|---|---|
| $X,x;\ T,t;\ X(\omega)$ | Primary variable and value | Numerical rule and possible value; state the units. |
| $S_X=\{x:P(X=x)>0\}$ | Support | Distinct values with positive probability, in the variable's units. |
| $Y,y;\ Y=f(X),Y_i=f_i(X)$ | Second or transformed variable | Another numerical description, with its own units. |
| $p=P(X=1)$ | Success probability | Chance of the specified state labelled 1, between 0 and 1. |
| $1-p$ | Complement probability | Chance of the complementary state labelled 0. |
| $n$ | Observation count | Fixed trial count or sample size; a positive integer. |
| $P(A),P(\omega),p_X(x),m_X(x)$ | Probability and mass | Unitless chance of an event or one supported value. |
| $F_X(a)=P(X\leq a),F_X(a^-)$ | Cumulative probability | Chance up to a cutoff; the left limit excludes the cutoff. |
| $a,b,m,\lfloor x\rfloor$ | Cutoff and integer part | A boundary in the variable's units; specify included endpoints. |
| $\sum,\binom nk,n!,e,\sim$ | Operations and distribution notation | Sum, count selections, take factorials, use the exponential constant, or name a model. |
| Independence, constant $p$, fixed observation rule | Model conditions | Conditions to check before using the selected distribution. |

Implementation row bindings: 1 → `variable` / `quantity.primary`; 2 → `support` / `quantity.primary`; 3 → `second` / `quantity.secondary`; 4 → `p` / `probability`; 5 → `q` / `probability.complement`; 6 → `size` / `count.design`; 7 → `mass` / `probability`; 8 → `cum` / `cumulative`; 9 → `cutoff` / `quantity.primary`; 10 → `ops` / `context`; 11 → `assume` / `context`.

Criterion-specific alignment: Expand the existing short two-column Notation reference and practice procedure table to four-column detailed schema, with a unique table anchor. Link existing offer and arrangement explanations. Fixed n counts all trials, k realised successes. Check fixed n, binary outcomes, independence and constant p. Combinations count arrangements, not probabilities.

## Grade 10 C5 Legend

Source: [G10_T2_L2_C5_practice_activity.tex](../../../grade10/term_2/1-practice_activities/G10_T2_L2_C5_practice_activity.tex).

| Symbol or notation | Concept | Brief meaning |
|---|---|---|
| $T,t;\ F=T-1\text{ or }F=T-r$ | Trials and failures | Total trials include the final success; failures exclude successes. |
| $S_X=\{x:P(X=x)>0\}$ | Support | Distinct values with positive probability, in the variable's units. |
| $p=P(X=1)$ | Success probability | Chance of the specified state labelled 1, between 0 and 1. |
| $1-p$ | Complement probability | Chance of the complementary state labelled 0. |
| $Y,y;\ Y=f(X),Y_i=f_i(X)$ | Second or transformed variable | Another numerical description, with its own units. |
| $P(A),P(\omega),p_X(x),m_X(x)$ | Probability and mass | Unitless chance of an event or one supported value. |
| $F_X(a)=P(X\leq a),F_X(a^-)$ | Cumulative probability | Chance up to a cutoff; the left limit excludes the cutoff. |
| $a,b,m,\lfloor x\rfloor$ | Cutoff and integer part | A boundary in the variable's units; specify included endpoints. |
| $A,E,E^c,\{X\leq a\}$ | Event and complement | Outcomes meeting a condition; those outside it. |
| Independence, constant $p$, fixed observation rule | Model conditions | Conditions to check before using the selected distribution. |

Implementation row bindings: 1 → `wait` / `quantity.primary`; 2 → `support` / `quantity.primary`; 3 → `p` / `probability`; 4 → `q` / `probability.complement`; 5 → `second` / `quantity.secondary`; 6 → `mass` / `probability`; 7 → `cum` / `cumulative`; 8 → `cutoff` / `quantity.primary`; 9 → `event` / `event`; 10 → `assume` / `context`.

Criterion-specific alignment: Expand the existing short notation reference and add a stable anchor. T includes final success; F=T−1 counts failures. For 0<p<1 supports start at 1 and 0. At p=1 T=1; p=0 gives no proper finite waiting distribution. Trials are not elapsed time. Conditional probability and memorylessness require fuller definitions in the reference, not solved opening examples.

## Grade 10 C6 Legend

Source: [G10_T2_L2_C6_practice_activity.tex](../../../grade10/term_2/1-practice_activities/G10_T2_L2_C6_practice_activity.tex).

| Symbol or notation | Concept | Brief meaning |
|---|---|---|
| $T,t;\ F=T-1\text{ or }F=T-r$ | Trials and failures | Total trials include the final success; failures exclude successes. |
| $S_X=\{x:P(X=x)>0\}$ | Support | Distinct values with positive probability, in the variable's units. |
| $p=P(X=1)$ | Success probability | Chance of the specified state labelled 1, between 0 and 1. |
| $1-p$ | Complement probability | Chance of the complementary state labelled 0. |
| $r$ | Success target | Fixed number of successes required before stopping. |
| $Y,y;\ Y=f(X),Y_i=f_i(X)$ | Second or transformed variable | Another numerical description, with its own units. |
| $P(A),P(\omega),p_X(x),m_X(x)$ | Probability and mass | Unitless chance of an event or one supported value. |
| $F_X(a)=P(X\leq a),F_X(a^-)$ | Cumulative probability | Chance up to a cutoff; the left limit excludes the cutoff. |
| $n$ | Observation count | Fixed trial count or sample size; a positive integer. |
| $a,b,m,\lfloor x\rfloor$ | Cutoff and integer part | A boundary in the variable's units; specify included endpoints. |
| $\sum,\binom nk,n!,e,\sim$ | Operations and distribution notation | Sum, count selections, take factorials, use the exponential constant, or name a model. |
| Independence, constant $p$, fixed observation rule | Model conditions | Conditions to check before using the selected distribution. |

Implementation row bindings: 1 → `wait` / `quantity.primary`; 2 → `support` / `quantity.primary`; 3 → `p` / `probability`; 4 → `q` / `probability.complement`; 5 → `target` / `model.control`; 6 → `second` / `quantity.secondary`; 7 → `mass` / `probability`; 8 → `cum` / `cumulative`; 9 → `size` / `count.design`; 10 → `cutoff` / `quantity.primary`; 11 → `ops` / `context`; 12 → `assume` / `context`.

Criterion-specific alignment: Expand the existing short notation reference and add an anchor. Positive integer r is fixed; T includes final success, F=T−r counts failures. T starts at r for 0<p<1, equals r at p=1; p=0 never reaches target. Distinguish a stopping time from a binomial deadline count. Explain mandatory-final-success arrangements only in detailed instruction.

## Grade 10 C7 Legend

Source: [G10_T2_L2_C7_practice_activity.tex](../../../grade10/term_2/1-practice_activities/G10_T2_L2_C7_practice_activity.tex).

| Symbol or notation | Concept | Brief meaning |
|---|---|---|
| $X,x;\ T,t;\ X(\omega)$ | Primary variable and value | Numerical rule and possible value; state the units. |
| $S_X=\{x:P(X=x)>0\}$ | Support | Distinct values with positive probability, in the variable's units. |
| $P(A),P(\omega),p_X(x),m_X(x)$ | Probability and mass | Unitless chance of an event or one supported value. |
| $F_X(a)=P(X\leq a),F_X(a^-)$ | Cumulative probability | Chance up to a cutoff; the left limit excludes the cutoff. |
| $a,b,m,\lfloor x\rfloor$ | Cutoff and integer part | A boundary in the variable's units; specify included endpoints. |
| $\mathrm{rate},\mathrm{exposure}$ | Rate and exposure | Events per exposure unit and length of the observation window. |
| $\lambda$ | Poisson interval mean | Expected count for the selected exposure. |
| $Y,y;\ Y=f(X),Y_i=f_i(X)$ | Second or transformed variable | Another numerical description, with its own units. |
| $\sum,\binom nk,n!,e,\sim$ | Operations and distribution notation | Sum, count selections, take factorials, use the exponential constant, or name a model. |
| Independence, constant $p$, fixed observation rule | Model conditions | Conditions to check before using the selected distribution. |

Implementation row bindings: 1 → `variable` / `quantity.primary`; 2 → `support` / `quantity.primary`; 3 → `mass` / `probability`; 4 → `cum` / `cumulative`; 5 → `cutoff` / `quantity.primary`; 6 → `rate` / `context`; 7 → `lambda` / `expectation`; 8 → `second` / `quantity.secondary`; 9 → `ops` / `context`; 10 → `assume` / `context`.

Criterion-specific alignment: Expand the existing short notation reference and add an anchor. Lambda is rate times selected exposure, can be noninteger; realised counts are integers. Positive lambda gives unbounded support; lambda=0 is degenerate at zero. Rate, exposure, count and monetary consequence have different units. Rarity does not establish stable rate, independent interval counts or isolated events.

## Grade 10 C8 Legend

Source: [G10_T2_L3_C8_practice_activity.tex](../../../grade10/term_2/1-practice_activities/G10_T2_L3_C8_practice_activity.tex).

| Symbol or notation | Concept | Brief meaning |
|---|---|---|
| $X,x;\ T,t;\ X(\omega)$ | Primary variable and value | Numerical rule and possible value; state the units. |
| $S_X=\{x:P(X=x)>0\}$ | Support | Distinct values with positive probability, in the variable's units. |
| $Y,y;\ Y=f(X),Y_i=f_i(X)$ | Second or transformed variable | Another numerical description, with its own units. |
| $P(A),P(\omega),p_X(x),m_X(x)$ | Probability and mass | Unitless chance of an event or one supported value. |
| $E(X),\mathbb E[Y_i],\mu$ | Expected value or model mean | Probability-weighted average, in original units. |
| $E(X^2),[E(X)]^2$ | Second moment and squared mean | Average of squares; square of the average. Both use squared units. |
| $\operatorname{Var}(X),\sigma_X^2$ | Variance | Mean squared deviation from the mean; squared units. |
| $\sigma_X,\sigma$ | Population or model standard deviation | Spread of individual values, in original units. |
| $a,b,f_i(0),f_i(1)$ | Transformation inputs | Scale, fixed addition or state payoffs, with required units. |
| $\sum,\binom nk,n!,e,\sim$ | Operations and distribution notation | Sum, count selections, take factorials, use the exponential constant, or name a model. |

Implementation row bindings: 1 → `variable` / `quantity.primary`; 2 → `support` / `quantity.primary`; 3 → `second` / `quantity.secondary`; 4 → `mass` / `probability`; 5 → `expected` / `expectation`; 6 → `secondmoment` / `expectation`; 7 → `variance` / `variance.population`; 8 → `sd` / `sd.population`; 9 → `transform` / `context`; 10 → `ops` / `context`.

Criterion-specific alignment: Reuse `tab:highlight-legend` and `tab:notation-reference`, with `ex:c8-score`/`ex:c8-spread`. Add mass, variance, SD and transformation inputs to concise coverage. E(X²) differs from [E(X)]². Y=aX+b scales variance by a² and SD by |a|; fixed addition changes location only. Preserve squared/original units. Do not disclose independent risk-ranking conclusions.

## Grade 10 C9 Legend

Source: [G10_T2_L3_C9_practice_activity.tex](../../../grade10/term_2/1-practice_activities/G10_T2_L3_C9_practice_activity.tex).

| Symbol or notation | Concept | Brief meaning |
|---|---|---|
| $A,E,E^c,\{X\leq a\}$ | Event and complement | Outcomes meeting a condition; those outside it. |
| $X,x;\ T,t;\ X(\omega)$ | Primary variable and value | Numerical rule and possible value; state the units. |
| $S_X=\{x:P(X=x)>0\}$ | Support | Distinct values with positive probability, in the variable's units. |
| $T,t;\ F=T-1\text{ or }F=T-r$ | Trials and failures | Total trials include the final success; failures exclude successes. |
| $Y,y;\ Y=f(X),Y_i=f_i(X)$ | Second or transformed variable | Another numerical description, with its own units. |
| $p=P(X=1)$ | Success probability | Chance of the specified state labelled 1, between 0 and 1. |
| $1-p$ | Complement probability | Chance of the complementary state labelled 0. |
| $n$ | Observation count | Fixed trial count or sample size; a positive integer. |
| $r$ | Success target | Fixed number of successes required before stopping. |
| $P(A),P(\omega),p_X(x),m_X(x)$ | Probability and mass | Unitless chance of an event or one supported value. |
| $F_X(a)=P(X\leq a),F_X(a^-)$ | Cumulative probability | Chance up to a cutoff; the left limit excludes the cutoff. |
| $\mathrm{rate},\mathrm{exposure}$ | Rate and exposure | Events per exposure unit and length of the observation window. |
| $\lambda$ | Poisson interval mean | Expected count for the selected exposure. |
| $\sum,\binom nk,n!,e,\sim$ | Operations and distribution notation | Sum, count selections, take factorials, use the exponential constant, or name a model. |
| Independence, constant $p$, fixed observation rule | Model conditions | Conditions to check before using the selected distribution. |

Implementation row bindings: 1 → `event` / `event`; 2 → `variable` / `quantity.primary`; 3 → `support` / `quantity.primary`; 4 → `wait` / `quantity.primary`; 5 → `second` / `quantity.secondary`; 6 → `p` / `probability`; 7 → `q` / `probability.complement`; 8 → `size` / `count.design`; 9 → `target` / `model.control`; 10 → `mass` / `probability`; 11 → `cum` / `cumulative`; 12 → `rate` / `context`; 13 → `lambda` / `expectation`; 14 → `ops` / `context`; 15 → `assume` / `context`.

Criterion-specific alignment: Align the existing Bridge to the general model comparison and later short notation reference, adding stable anchors. Distinguish one binary label, success count in fixed trials, total trials to fixed success target and count in fixed exposure. Geometric targets one. No opening entry preselects models or certifies assumptions in independent problems.

## Grade 11 general legend table

| Symbol or notation | Concept | Brief meaning |
|---|---|---|
| $X,X_i$ | Sample | Selected units; here each index identifies a whole draw. |
| $\mathcal P,N$ | Population and size | All units in the stated scope; their total number. |
| $n$ | Observation count | Fixed trial count or sample size; a positive integer. |
| $y_j,x_i$ | Observation | Measured value on one selected unit, with the response's units. |
| $\mu,\mu_{\rm sim}$ | Population mean | Fixed mean of the defined population; simulation mean is supplied separately. |
| $\bar x,\bar x_i$ | Sample mean and point estimate | Average of one sample; estimates its population mean. |
| $\sigma_X,\sigma$ | Population or model standard deviation | Spread of individual values, in original units. |
| $s,s_i$ | Sample standard deviation | Spread of sample observations, in response units. |
| $p$ | Population proportion | Fraction of all units meeting the condition; unitless. |
| $\hat p=x/n$ | Sample proportion | Observed success fraction among selected units; unitless. |
| $\mathrm{SE},\widehat{SE}$ | Standard error | Spread of a statistic across samples, or its estimate. |
| $C$ | Confidence level | Chosen nominal long-run coverage under the model; decimal in formulas. |
| $\alpha,\alpha/2$ | Significance level and tail area | Total excluded area and each equal tail in a two-sided procedure. |
| $z^*,t^*$ | Critical value | Positive unitless reference cutoff selected by confidence and model. |
| $\mathrm{MoE},E,E_{\rm target}$ | Margin of error | Centre-to-bound distance, or its precision target. |
| $L,U,\mathrm{CI}=[L,U]$ | Bounds and confidence interval | Lower and upper limits; the range they delimit for the parameter. |
| $W=U-L=2\mathrm{MoE}$ | Full interval width | Total distance between bounds, in the parameter's units. |
| $L_{\rm rep},U_{\rm rep},\mathrm{CI}_{\rm rep}$ | Reported bounds and interval | Rounded reporting values, separate from calculated values. |
| $W_{\rm rep}$ | Reported full width | Difference of reported endpoints; may differ from calculated width. |
| $N_{\rm cover}(C),N(C),\mathrm{Cov}(C)$ | Observed coverage and counts | Covering intervals, all intervals at that level, and their finite-run percentage. |
| $E_{\rm abs}(C)$ | Absolute coverage error | Absolute gap between observed and nominal percentages, in percentage points. |
| $\Phi(z),\Phi^{-1}(u)$ | Normal cumulative area and inverse | Left-tail standard normal area; the cutoff with that area. |
| Random selection, shape, outliers, groups | Inference conditions | Check design and procedure-specific assumptions. |
| $C_{\rm normal}$ | Theoretical normal coverage | Model area from a rounded cutoff; may differ slightly from nominal confidence. |
| Cost per unit, budget, benchmark | Design inputs and comparison values | Fixed constraints or reference amounts, with stated units. |
| $\operatorname{Var}(X),\sigma_X^2$ | Variance | Mean squared deviation from the mean; squared units. |
| $n/N$ | Sampling fraction | Share of the finite population selected; check design conditions. |
| $x,n\hat p,n(1-\hat p)$ | Observed outcome counts | Success and other-outcome counts within a sample. |
| $p_0$ | Planning proportion | Pilot or conservative input; not a null-hypothesis value here. |
| $n_{\min},E(n)$ | Sample-size plan | Minimum usable integer count and its achieved margin. |
| $df=n-1$ | Degrees of freedom | Reference index for the one-sample t procedure. |
| $s^2$ | Sample variance | Squared sample spread; use the specified divisor. |
| $\sum,\binom nk,n!,e,\sim$ | Operations and distribution notation | Sum, count selections, take factorials, use the exponential constant, or name a model. |

Implementation bindings (rows follow the student table):

| Row / entry ID | Stable role ID | Supported criteria | Continuity |
|---|---|---|---|
| 1: `sample` | `group.sample` | C1, C9, C10 | New Grade 11 role |
| 2: `population` | `group.population` | C1, C4, C5, C6, C7, C8, C9, C10 | New Grade 11 role |
| 3: `size` | `count.design` | C1, C2, C3, C4, C5, C6, C7, C8, C9, C10 | Inherited role; inference context |
| 4: `obs` | `quantity.primary` | C1, C2, C10 | Inherited role; inference context |
| 5: `meanpop` | `expectation` | C1, C2, C3, C4, C6, C8, C10 | Inherited role; inference context |
| 6: `meansample` | `mean.sample` | C1, C2, C3, C4, C8, C9, C10 | New Grade 11 role |
| 7: `sd` | `sd.population` | C1, C2, C3, C4, C6, C8 | Inherited role; inference context |
| 8: `sdsample` | `sd.sample` | C1, C2, C8, C9, C10 | New Grade 11 role |
| 9: `proppop` | `probability` | C1, C5, C6, C7 | Inherited role; inference context |
| 10: `propsample` | `proportion.sample` | C1, C5, C7, C9 | New Grade 11 role |
| 11: `se` | `standard.error` | C2, C3, C4, C5, C7, C8, C10 | New Grade 11 role |
| 12: `confidence` | `confidence` | C2, C3, C4, C5, C6, C7, C8, C10 | New Grade 11 role |
| 13: `tail` | `tail` | C2, C3, C4, C8 | New Grade 11 role |
| 14: `critical` | `critical` | C2, C3, C4, C5, C6, C7, C8, C10 | New Grade 11 role |
| 15: `margin` | `margin` | C2, C3, C4, C5, C6, C7, C8, C10 | New Grade 11 role |
| 16: `bounds` | `bounds` | C2, C3, C4, C5, C7, C8, C10 | New Grade 11 role |
| 17: `width` | `width` | C2, C3, C7 | New Grade 11 role |
| 18: `reported` | `bounds` | C2 | New Grade 11 role |
| 19: `reportedwidth` | `width` | C2 | New Grade 11 role |
| 20: `coverage` | `coverage` | C2 | New Grade 11 role |
| 21: `error` | `coverage.error` | C2 | New Grade 11 role |
| 22: `normal` | `cumulative` | C2, C3, C4 | Inherited role; inference context |
| 23: `shape` | `context` | C2, C3, C4, C5, C6, C7, C8, C9, C10 | Inherited role; inference context |
| 24: `theoretical` | `cumulative` | C3 | Inherited role; inference context |
| 25: `budget` | `context` | C3, C4, C5, C6, C8, C9, C10 | Inherited role; inference context |
| 26: `variance` | `variance.population` | C4 | Inherited role; inference context |
| 27: `fraction` | `context` | C4, C5, C6, C7, C8, C9, C10 | Inherited role; inference context |
| 28: `successcount` | `count.design` | C5, C7, C9 | Inherited role; inference context |
| 29: `planning` | `probability` | C6 | Inherited role; inference context |
| 30: `precisionplan` | `count.design` | C6, C10 | Inherited role; inference context |
| 31: `df` | `model.control` | C8, C10 | Inherited role; inference context |
| 32: `varsample` | `variance.sample` | C10 | New Grade 11 role |
| 33: `ops` | `context` | C10 | Inherited role; inference context |

## Grade 11 C1 Legend

Source: [G11_T2_L1_C1_practice.tex](G11_T2_L1_C1_practice.tex).

| Symbol or notation | Concept | Brief meaning |
|---|---|---|
| $X,X_i$ | Sample | Selected units; here each index identifies a whole draw. |
| $\mathcal P,N$ | Population and size | All units in the stated scope; their total number. |
| $n$ | Observation count | Fixed trial count or sample size; a positive integer. |
| $y_j,x_i$ | Observation | Measured value on one selected unit, with the response's units. |
| $\mu,\mu_{\rm sim}$ | Population mean | Fixed mean of the defined population; simulation mean is supplied separately. |
| $\bar x,\bar x_i$ | Sample mean and point estimate | Average of one sample; estimates its population mean. |
| $\sigma_X,\sigma$ | Population or model standard deviation | Spread of individual values, in original units. |
| $s,s_i$ | Sample standard deviation | Spread of sample observations, in response units. |
| $p$ | Population proportion | Fraction of all units meeting the condition; unitless. |
| $\hat p=x/n$ | Sample proportion | Observed success fraction among selected units; unitless. |

Implementation row bindings: 1 → `sample` / `group.sample`; 2 → `population` / `group.population`; 3 → `size` / `count.design`; 4 → `obs` / `quantity.primary`; 5 → `meanpop` / `expectation`; 6 → `meansample` / `mean.sample`; 7 → `sd` / `sd.population`; 8 → `sdsample` / `sd.sample`; 9 → `proppop` / `probability`; 10 → `propsample` / `proportion.sample`.

Criterion-specific alignment: Reuse `tab:highlight-legend`, `tab:notation-reference` and `subsec:c1-notation`. Here X_i identifies a whole sample, y_j one observation. Subscripts identify measure, scope and draw (F/A/H/R, I/C, J/Jun). A redraw changes statistics; a changed population requires redefined parameters. Percentage differences use percentage points.

## Grade 11 C2 Legend

Source: [G11_T2_L1_C2_practice.tex](G11_T2_L1_C2_practice.tex).

| Symbol or notation | Concept | Brief meaning |
|---|---|---|
| $\mu,\mu_{\rm sim}$ | Population mean | Fixed mean of the defined population; simulation mean is supplied separately. |
| $\bar x,\bar x_i$ | Sample mean and point estimate | Average of one sample; estimates its population mean. |
| $\sigma_X,\sigma$ | Population or model standard deviation | Spread of individual values, in original units. |
| $n$ | Observation count | Fixed trial count or sample size; a positive integer. |
| $s,s_i$ | Sample standard deviation | Spread of sample observations, in response units. |
| $\mathrm{SE},\widehat{SE}$ | Standard error | Spread of a statistic across samples, or its estimate. |
| $C$ | Confidence level | Chosen nominal long-run coverage under the model; decimal in formulas. |
| $\alpha,\alpha/2$ | Significance level and tail area | Total excluded area and each equal tail in a two-sided procedure. |
| $z^*,t^*$ | Critical value | Positive unitless reference cutoff selected by confidence and model. |
| $\mathrm{MoE},E,E_{\rm target}$ | Margin of error | Centre-to-bound distance, or its precision target. |
| $L,U,\mathrm{CI}=[L,U]$ | Bounds and confidence interval | Lower and upper limits; the range they delimit for the parameter. |
| $W=U-L=2\mathrm{MoE}$ | Full interval width | Total distance between bounds, in the parameter's units. |
| $L_{\rm rep},U_{\rm rep},\mathrm{CI}_{\rm rep}$ | Reported bounds and interval | Rounded reporting values, separate from calculated values. |
| $W_{\rm rep}$ | Reported full width | Difference of reported endpoints; may differ from calculated width. |
| $N_{\rm cover}(C),N(C),\mathrm{Cov}(C)$ | Observed coverage and counts | Covering intervals, all intervals at that level, and their finite-run percentage. |
| $E_{\rm abs}(C)$ | Absolute coverage error | Absolute gap between observed and nominal percentages, in percentage points. |
| $\Phi(z),\Phi^{-1}(u)$ | Normal cumulative area and inverse | Left-tail standard normal area; the cutoff with that area. |
| $y_j,x_i$ | Observation | Measured value on one selected unit, with the response's units. |
| Random selection, shape, outliers, groups | Inference conditions | Check design and procedure-specific assumptions. |

Implementation row bindings: 1 → `meanpop` / `expectation`; 2 → `meansample` / `mean.sample`; 3 → `sd` / `sd.population`; 4 → `size` / `count.design`; 5 → `sdsample` / `sd.sample`; 6 → `se` / `standard.error`; 7 → `confidence` / `confidence`; 8 → `tail` / `tail`; 9 → `critical` / `critical`; 10 → `margin` / `margin`; 11 → `bounds` / `bounds`; 12 → `width` / `width`; 13 → `reported` / `bounds`; 14 → `reportedwidth` / `width`; 15 → `coverage` / `coverage`; 16 → `error` / `coverage.error`; 17 → `normal` / `cumulative`; 18 → `obs` / `quantity.primary`; 19 → `shape` / `context`.

Criterion-specific alignment: Reuse both table anchors and cycling-example links. Replace local Symbol/Concept/Formula layout with concise schema, retaining detailed four-column reference and task schemas. N(C) counts intervals per level, not population size; equality at endpoints covers. Compare Cov and C on the same percentage scale for E_abs; decimal C for tails. Separate unknown original mu from supplied mu_sim. W_rep comes from reported endpoints. n/known-sigma SE grouping under Sample statistics is organizational. No practice coverage result or chosen option belongs in the legend.

## Grade 11 C3 Legend

Source: [G11_T2_L1_C3_practice.tex](G11_T2_L1_C3_practice.tex).

| Symbol or notation | Concept | Brief meaning |
|---|---|---|
| $\mu,\mu_{\rm sim}$ | Population mean | Fixed mean of the defined population; simulation mean is supplied separately. |
| $\bar x,\bar x_i$ | Sample mean and point estimate | Average of one sample; estimates its population mean. |
| $\sigma_X,\sigma$ | Population or model standard deviation | Spread of individual values, in original units. |
| $n$ | Observation count | Fixed trial count or sample size; a positive integer. |
| $\mathrm{SE},\widehat{SE}$ | Standard error | Spread of a statistic across samples, or its estimate. |
| $C$ | Confidence level | Chosen nominal long-run coverage under the model; decimal in formulas. |
| $\alpha,\alpha/2$ | Significance level and tail area | Total excluded area and each equal tail in a two-sided procedure. |
| $z^*,t^*$ | Critical value | Positive unitless reference cutoff selected by confidence and model. |
| $\mathrm{MoE},E,E_{\rm target}$ | Margin of error | Centre-to-bound distance, or its precision target. |
| $L,U,\mathrm{CI}=[L,U]$ | Bounds and confidence interval | Lower and upper limits; the range they delimit for the parameter. |
| $W=U-L=2\mathrm{MoE}$ | Full interval width | Total distance between bounds, in the parameter's units. |
| $\Phi(z),\Phi^{-1}(u)$ | Normal cumulative area and inverse | Left-tail standard normal area; the cutoff with that area. |
| $C_{\rm normal}$ | Theoretical normal coverage | Model area from a rounded cutoff; may differ slightly from nominal confidence. |
| Cost per unit, budget, benchmark | Design inputs and comparison values | Fixed constraints or reference amounts, with stated units. |
| Random selection, shape, outliers, groups | Inference conditions | Check design and procedure-specific assumptions. |

Implementation row bindings: 1 → `meanpop` / `expectation`; 2 → `meansample` / `mean.sample`; 3 → `sd` / `sd.population`; 4 → `size` / `count.design`; 5 → `se` / `standard.error`; 6 → `confidence` / `confidence`; 7 → `tail` / `tail`; 8 → `critical` / `critical`; 9 → `margin` / `margin`; 10 → `bounds` / `bounds`; 11 → `width` / `width`; 12 → `normal` / `cumulative`; 13 → `theoretical` / `cumulative`; 14 → `budget` / `context`; 15 → `shape` / `context`.

Criterion-specific alignment: Reuse both table anchors and transport-example links. Align Phi/inverse, C_normal and budget constraints. C_normal is theoretical area from rounded cutoffs, not empirical coverage or necessarily exact nominal C. A vs B means A vertically, B horizontally. Integer n points are feasible; curves are guides. Preserve cutoff/coordinate precision and rounding policy. Concurrent header-alignment work adds CthreeTableHeader; preserve its layout. No feasible-confidence answer belongs in the legend.

## Grade 11 C4 Legend

Source: [G11_T2_L1_C4_practice.tex](G11_T2_L1_C4_practice.tex).

| Symbol or notation | Concept | Brief meaning |
|---|---|---|
| $\mu,\mu_{\rm sim}$ | Population mean | Fixed mean of the defined population; simulation mean is supplied separately. |
| $\bar x,\bar x_i$ | Sample mean and point estimate | Average of one sample; estimates its population mean. |
| $\operatorname{Var}(X),\sigma_X^2$ | Variance | Mean squared deviation from the mean; squared units. |
| $\sigma_X,\sigma$ | Population or model standard deviation | Spread of individual values, in original units. |
| $n$ | Observation count | Fixed trial count or sample size; a positive integer. |
| $\mathcal P,N$ | Population and size | All units in the stated scope; their total number. |
| $\mathrm{SE},\widehat{SE}$ | Standard error | Spread of a statistic across samples, or its estimate. |
| $C$ | Confidence level | Chosen nominal long-run coverage under the model; decimal in formulas. |
| $\alpha,\alpha/2$ | Significance level and tail area | Total excluded area and each equal tail in a two-sided procedure. |
| $z^*,t^*$ | Critical value | Positive unitless reference cutoff selected by confidence and model. |
| $\mathrm{MoE},E,E_{\rm target}$ | Margin of error | Centre-to-bound distance, or its precision target. |
| $L,U,\mathrm{CI}=[L,U]$ | Bounds and confidence interval | Lower and upper limits; the range they delimit for the parameter. |
| $\Phi(z),\Phi^{-1}(u)$ | Normal cumulative area and inverse | Left-tail standard normal area; the cutoff with that area. |
| $n/N$ | Sampling fraction | Share of the finite population selected; check design conditions. |
| Random selection, shape, outliers, groups | Inference conditions | Check design and procedure-specific assumptions. |
| Cost per unit, budget, benchmark | Design inputs and comparison values | Fixed constraints or reference amounts, with stated units. |

Implementation row bindings: 1 → `meanpop` / `expectation`; 2 → `meansample` / `mean.sample`; 3 → `variance` / `variance.population`; 4 → `sd` / `sd.population`; 5 → `size` / `count.design`; 6 → `population` / `group.population`; 7 → `se` / `standard.error`; 8 → `confidence` / `confidence`; 9 → `tail` / `tail`; 10 → `critical` / `critical`; 11 → `margin` / `margin`; 12 → `bounds` / `bounds`; 13 → `normal` / `cumulative`; 14 → `fraction` / `context`; 15 → `shape` / `context`; 16 → `budget` / `context`.

Criterion-specific alignment: No dedicated detailed reference or opening legend exists. Plan concise legend before worked instruction and a separate four-column reference after existing examples; add unique anchors. Distinguish known sigma² from sigma and squared from original units. Cumulative left area differs from central confidence. Benchmark is contextual, not a test statistic.

## Grade 11 C5 Legend

Source: [G11_T2_L2_C5_practice.tex](G11_T2_L2_C5_practice.tex).

| Symbol or notation | Concept | Brief meaning |
|---|---|---|
| $p$ | Population proportion | Fraction of all units meeting the condition; unitless. |
| $\hat p=x/n$ | Sample proportion | Observed success fraction among selected units; unitless. |
| $x,n\hat p,n(1-\hat p)$ | Observed outcome counts | Success and other-outcome counts within a sample. |
| $n$ | Observation count | Fixed trial count or sample size; a positive integer. |
| $\mathcal P,N$ | Population and size | All units in the stated scope; their total number. |
| $\mathrm{SE},\widehat{SE}$ | Standard error | Spread of a statistic across samples, or its estimate. |
| $C$ | Confidence level | Chosen nominal long-run coverage under the model; decimal in formulas. |
| $z^*,t^*$ | Critical value | Positive unitless reference cutoff selected by confidence and model. |
| $\mathrm{MoE},E,E_{\rm target}$ | Margin of error | Centre-to-bound distance, or its precision target. |
| $L,U,\mathrm{CI}=[L,U]$ | Bounds and confidence interval | Lower and upper limits; the range they delimit for the parameter. |
| $n/N$ | Sampling fraction | Share of the finite population selected; check design conditions. |
| Random selection, shape, outliers, groups | Inference conditions | Check design and procedure-specific assumptions. |
| Cost per unit, budget, benchmark | Design inputs and comparison values | Fixed constraints or reference amounts, with stated units. |

Implementation row bindings: 1 → `proppop` / `probability`; 2 → `propsample` / `proportion.sample`; 3 → `successcount` / `count.design`; 4 → `size` / `count.design`; 5 → `population` / `group.population`; 6 → `se` / `standard.error`; 7 → `confidence` / `confidence`; 8 → `critical` / `critical`; 9 → `margin` / `margin`; 10 → `bounds` / `bounds`; 11 → `fraction` / `context`; 12 → `shape` / `context`; 13 → `budget` / `context`.

Criterion-specific alignment: No dedicated notation reference exists; plan one after the current examples with definitions separate from example-linked interpretations. x counts successes here. Estimated SE uses p-hat; both outcome counts and sampling design matter. Percentage estimates differ from percentage-point margins. Keep interval results and benchmark conclusions in solutions.

## Grade 11 C6 Legend

Source: [G11_T2_L2_C6_practice.tex](G11_T2_L2_C6_practice.tex).

| Symbol or notation | Concept | Brief meaning |
|---|---|---|
| $\mu,\mu_{\rm sim}$ | Population mean | Fixed mean of the defined population; simulation mean is supplied separately. |
| $\sigma_X,\sigma$ | Population or model standard deviation | Spread of individual values, in original units. |
| $p$ | Population proportion | Fraction of all units meeting the condition; unitless. |
| $p_0$ | Planning proportion | Pilot or conservative input; not a null-hypothesis value here. |
| $n$ | Observation count | Fixed trial count or sample size; a positive integer. |
| $n_{\min},E(n)$ | Sample-size plan | Minimum usable integer count and its achieved margin. |
| $\mathcal P,N$ | Population and size | All units in the stated scope; their total number. |
| $C$ | Confidence level | Chosen nominal long-run coverage under the model; decimal in formulas. |
| $z^*,t^*$ | Critical value | Positive unitless reference cutoff selected by confidence and model. |
| $\mathrm{MoE},E,E_{\rm target}$ | Margin of error | Centre-to-bound distance, or its precision target. |
| $n/N$ | Sampling fraction | Share of the finite population selected; check design conditions. |
| Random selection, shape, outliers, groups | Inference conditions | Check design and procedure-specific assumptions. |
| Cost per unit, budget, benchmark | Design inputs and comparison values | Fixed constraints or reference amounts, with stated units. |

Implementation row bindings: 1 → `meanpop` / `expectation`; 2 → `sd` / `sd.population`; 3 → `proppop` / `probability`; 4 → `planning` / `probability`; 5 → `size` / `count.design`; 6 → `precisionplan` / `count.design`; 7 → `population` / `group.population`; 8 → `confidence` / `confidence`; 9 → `critical` / `critical`; 10 → `margin` / `margin`; 11 → `fraction` / `context`; 12 → `shape` / `context`; 13 → `budget` / `context`.

Criterion-specific alignment: No dedicated notation reference exists; plan one after planning examples. p_0 is a planning share, not null value. E_target is a cap, not realised estimation error. Round required usable n upward, check achieved margin/conditions after sampling. Expected planning counts are not observed counts. Numerical minima and conservative-choice reasoning stay in solutions.

## Grade 11 C7 Legend

Source: [G11_T2_L2_C7_practice.tex](G11_T2_L2_C7_practice.tex).

| Symbol or notation | Concept | Brief meaning |
|---|---|---|
| $p$ | Population proportion | Fraction of all units meeting the condition; unitless. |
| $\hat p=x/n$ | Sample proportion | Observed success fraction among selected units; unitless. |
| $x,n\hat p,n(1-\hat p)$ | Observed outcome counts | Success and other-outcome counts within a sample. |
| $n$ | Observation count | Fixed trial count or sample size; a positive integer. |
| $\mathcal P,N$ | Population and size | All units in the stated scope; their total number. |
| $\mathrm{SE},\widehat{SE}$ | Standard error | Spread of a statistic across samples, or its estimate. |
| $C$ | Confidence level | Chosen nominal long-run coverage under the model; decimal in formulas. |
| $z^*,t^*$ | Critical value | Positive unitless reference cutoff selected by confidence and model. |
| $\mathrm{MoE},E,E_{\rm target}$ | Margin of error | Centre-to-bound distance, or its precision target. |
| $L,U,\mathrm{CI}=[L,U]$ | Bounds and confidence interval | Lower and upper limits; the range they delimit for the parameter. |
| $W=U-L=2\mathrm{MoE}$ | Full interval width | Total distance between bounds, in the parameter's units. |
| $n/N$ | Sampling fraction | Share of the finite population selected; check design conditions. |
| Random selection, shape, outliers, groups | Inference conditions | Check design and procedure-specific assumptions. |

Implementation row bindings: 1 → `proppop` / `probability`; 2 → `propsample` / `proportion.sample`; 3 → `successcount` / `count.design`; 4 → `size` / `count.design`; 5 → `population` / `group.population`; 6 → `se` / `standard.error`; 7 → `confidence` / `confidence`; 8 → `critical` / `critical`; 9 → `margin` / `margin`; 10 → `bounds` / `bounds`; 11 → `width` / `width`; 12 → `fraction` / `context`; 13 → `shape` / `context`.

Criterion-specific alignment: No dedicated notation reference exists; plan one linked to mobile-ticket investigations. Keep percentage-point margins/widths. Holding the fraction fixed matters for sample-size scaling. Raising confidence widens an interval when SE is fixed; simultaneous changes require joint comparison. Label centre, bounds and confidence in diagrams.

## Grade 11 C8 Legend

Source: [G11_T2_L3_C8_practice.tex](G11_T2_L3_C8_practice.tex).

| Symbol or notation | Concept | Brief meaning |
|---|---|---|
| $\mu,\mu_{\rm sim}$ | Population mean | Fixed mean of the defined population; simulation mean is supplied separately. |
| $\bar x,\bar x_i$ | Sample mean and point estimate | Average of one sample; estimates its population mean. |
| $\sigma_X,\sigma$ | Population or model standard deviation | Spread of individual values, in original units. |
| $s,s_i$ | Sample standard deviation | Spread of sample observations, in response units. |
| $n$ | Observation count | Fixed trial count or sample size; a positive integer. |
| $\mathcal P,N$ | Population and size | All units in the stated scope; their total number. |
| $\mathrm{SE},\widehat{SE}$ | Standard error | Spread of a statistic across samples, or its estimate. |
| $C$ | Confidence level | Chosen nominal long-run coverage under the model; decimal in formulas. |
| $\alpha,\alpha/2$ | Significance level and tail area | Total excluded area and each equal tail in a two-sided procedure. |
| $z^*,t^*$ | Critical value | Positive unitless reference cutoff selected by confidence and model. |
| $\mathrm{MoE},E,E_{\rm target}$ | Margin of error | Centre-to-bound distance, or its precision target. |
| $L,U,\mathrm{CI}=[L,U]$ | Bounds and confidence interval | Lower and upper limits; the range they delimit for the parameter. |
| $df=n-1$ | Degrees of freedom | Reference index for the one-sample t procedure. |
| $n/N$ | Sampling fraction | Share of the finite population selected; check design conditions. |
| Random selection, shape, outliers, groups | Inference conditions | Check design and procedure-specific assumptions. |
| Cost per unit, budget, benchmark | Design inputs and comparison values | Fixed constraints or reference amounts, with stated units. |

Implementation row bindings: 1 → `meanpop` / `expectation`; 2 → `meansample` / `mean.sample`; 3 → `sd` / `sd.population`; 4 → `sdsample` / `sd.sample`; 5 → `size` / `count.design`; 6 → `population` / `group.population`; 7 → `se` / `standard.error`; 8 → `confidence` / `confidence`; 9 → `tail` / `tail`; 10 → `critical` / `critical`; 11 → `margin` / `margin`; 12 → `bounds` / `bounds`; 13 → `df` / `model.control`; 14 → `fraction` / `context`; 15 → `shape` / `context`; 16 → `budget` / `context`.

Criterion-specific alignment: No dedicated notation reference exists; plan one after the two mean examples. Unknown sigma estimated by s; t* depends on C and df=n−1. Estimated SE differs from s. Criterion wording mentions proportions, but examples implement mean intervals. Propose only demonstrated t-mean content and flag wording. No observed hypothesis-test statistic is calculated.

## Grade 11 C9 Legend

Source: [G11_T2_L3_C9_practice.tex](G11_T2_L3_C9_practice.tex).

| Symbol or notation | Concept | Brief meaning |
|---|---|---|
| $X,X_i$ | Sample | Selected units; here each index identifies a whole draw. |
| $\mathcal P,N$ | Population and size | All units in the stated scope; their total number. |
| $n$ | Observation count | Fixed trial count or sample size; a positive integer. |
| $\bar x,\bar x_i$ | Sample mean and point estimate | Average of one sample; estimates its population mean. |
| $s,s_i$ | Sample standard deviation | Spread of sample observations, in response units. |
| $\hat p=x/n$ | Sample proportion | Observed success fraction among selected units; unitless. |
| $x,n\hat p,n(1-\hat p)$ | Observed outcome counts | Success and other-outcome counts within a sample. |
| $n/N$ | Sampling fraction | Share of the finite population selected; check design conditions. |
| Random selection, shape, outliers, groups | Inference conditions | Check design and procedure-specific assumptions. |
| Cost per unit, budget, benchmark | Design inputs and comparison values | Fixed constraints or reference amounts, with stated units. |

Implementation row bindings: 1 → `sample` / `group.sample`; 2 → `population` / `group.population`; 3 → `size` / `count.design`; 4 → `meansample` / `mean.sample`; 5 → `sdsample` / `sd.sample`; 6 → `propsample` / `proportion.sample`; 7 → `successcount` / `count.design`; 8 → `fraction` / `context`; 9 → `shape` / `context`; 10 → `budget` / `context`.

Criterion-specific alignment: No dedicated notation reference exists; plan a design-and-conditions reference after three audits. 10% guideline addresses simple random sampling without replacement, not volunteers, undercoverage, skew, outliers or within-firm clustering. Normal proportion approximation uses both outcome counts; n>30 alone is insufficient. Audit judgments remain in solutions.

## Grade 11 C10 Legend

Source: [G11_T2_L3_C10_practice.tex](G11_T2_L3_C10_practice.tex).

| Symbol or notation | Concept | Brief meaning |
|---|---|---|
| $X,X_i$ | Sample | Selected units; here each index identifies a whole draw. |
| $\mathcal P,N$ | Population and size | All units in the stated scope; their total number. |
| $n$ | Observation count | Fixed trial count or sample size; a positive integer. |
| $y_j,x_i$ | Observation | Measured value on one selected unit, with the response's units. |
| $\mu,\mu_{\rm sim}$ | Population mean | Fixed mean of the defined population; simulation mean is supplied separately. |
| $\bar x,\bar x_i$ | Sample mean and point estimate | Average of one sample; estimates its population mean. |
| $s,s_i$ | Sample standard deviation | Spread of sample observations, in response units. |
| $s^2$ | Sample variance | Squared sample spread; use the specified divisor. |
| $\mathrm{SE},\widehat{SE}$ | Standard error | Spread of a statistic across samples, or its estimate. |
| $C$ | Confidence level | Chosen nominal long-run coverage under the model; decimal in formulas. |
| $z^*,t^*$ | Critical value | Positive unitless reference cutoff selected by confidence and model. |
| $\mathrm{MoE},E,E_{\rm target}$ | Margin of error | Centre-to-bound distance, or its precision target. |
| $L,U,\mathrm{CI}=[L,U]$ | Bounds and confidence interval | Lower and upper limits; the range they delimit for the parameter. |
| $df=n-1$ | Degrees of freedom | Reference index for the one-sample t procedure. |
| $n_{\min},E(n)$ | Sample-size plan | Minimum usable integer count and its achieved margin. |
| $n/N$ | Sampling fraction | Share of the finite population selected; check design conditions. |
| Random selection, shape, outliers, groups | Inference conditions | Check design and procedure-specific assumptions. |
| Cost per unit, budget, benchmark | Design inputs and comparison values | Fixed constraints or reference amounts, with stated units. |
| $\sum,\binom nk,n!,e,\sim$ | Operations and distribution notation | Sum, count selections, take factorials, use the exponential constant, or name a model. |

Implementation row bindings: 1 → `sample` / `group.sample`; 2 → `population` / `group.population`; 3 → `size` / `count.design`; 4 → `obs` / `quantity.primary`; 5 → `meanpop` / `expectation`; 6 → `meansample` / `mean.sample`; 7 → `sdsample` / `sd.sample`; 8 → `varsample` / `variance.sample`; 9 → `se` / `standard.error`; 10 → `confidence` / `confidence`; 11 → `critical` / `critical`; 12 → `margin` / `margin`; 13 → `bounds` / `bounds`; 14 → `df` / `model.control`; 15 → `precisionplan` / `count.design`; 16 → `fraction` / `context`; 17 → `shape` / `context`; 18 → `budget` / `context`; 19 → `ops` / `context`.

Criterion-specific alignment: No dedicated notation reference exists; plan one after design/analysis/reporting examples. One merchant reference-week total is one observation. Keep thousand-USD units and n−1 sample variance. Pilot SD is planning input, not known sigma; z planning does not replace final small-sample t analysis. Quarter scope requires merchant-level units or explicit dependence. No benchmark decision belongs in the legend.

## Source inventory and coverage matrix

All 19 sources were inspected across introductions, notation, worked material, exercises and solutions, including the advanced conditional-mixture, stopping-pattern and reserve-path mathematics. README files served as navigation only. Live LaTeX, including local overrides, is authoritative over the existing summary. No applicable AGENTS.md was found in the repository or checked ancestors. The math-legend-highlight skill and LaTeX reference were applied; update-specific-highlights-summary was read for conventions only. Its workflow was not executed.

| Criterion | Source | Mathematical coverage | Detailed reference | Status |
|---|---|---|---|---|
| G10 C1 | [G10_T2_L1_C1_practice_activity.tex](../../../grade10/term_2/1-practice_activities/G10_T2_L1_C1_practice_activity.tex) | Outcomes, variable mappings, support, PMF, missing masses, finite/infinite models | Four-column reference, `tab:notation-reference` | Covered |
| G10 C2 | [G10_T2_L1_C2_practice_activity.tex](../../../grade10/term_2/1-practice_activities/G10_T2_L1_C2_practice_activity.tex) | PMF/CDF, left limits, nonlinear payout, subset counting, hidden-condition mixture, pattern recurrence, reserve paths | Four-column reference, `tab:notation-reference` | Covered |
| G10 C3 | [G10_T2_L1_C3_practice_activity.tex](../../../grade10/term_2/1-practice_activities/G10_T2_L1_C3_practice_activity.tex) | Bernoulli, payoff functions, PMF/CDF, endpoint support, expectation sign/break-even | Four-column reference, `tab:notation-reference` | Covered |
| G10 C4 | [G10_T2_L1_C4_practice_activity.tex](../../../grade10/term_2/1-practice_activities/G10_T2_L1_C4_practice_activity.tex) | Binomial fixed trials, combinations, interval/complement events | Short notation reference; expand and anchor | Covered |
| G10 C5 | [G10_T2_L2_C5_practice_activity.tex](../../../grade10/term_2/1-practice_activities/G10_T2_L2_C5_practice_activity.tex) | Geometric total trials, failures, conditional waiting/memorylessness | Short notation reference; expand and anchor | Covered |
| G10 C6 | [G10_T2_L2_C6_practice_activity.tex](../../../grade10/term_2/1-practice_activities/G10_T2_L2_C6_practice_activity.tex) | Negative binomial target, total trials, deadline/binomial connection | Short notation reference; expand and anchor | Covered |
| G10 C7 | [G10_T2_L2_C7_practice_activity.tex](../../../grade10/term_2/1-practice_activities/G10_T2_L2_C7_practice_activity.tex) | Poisson counts, rate/exposure, scaling and clustering | Short notation reference; expand and anchor | Covered |
| G10 C8 | [G10_T2_L3_C8_practice_activity.tex](../../../grade10/term_2/1-practice_activities/G10_T2_L3_C8_practice_activity.tex) | Expectation, moments, variance/SD, affine transforms and risk limits | Four-column reference, `tab:notation-reference` | Covered |
| G10 C9 | [G10_T2_L3_C9_practice_activity.tex](../../../grade10/term_2/1-practice_activities/G10_T2_L3_C9_practice_activity.tex) | Five-model comparison, observation rules, assumptions, insufficient information | Short notation reference; expand and anchor | Covered |
| G11 C1 | [G11_T2_L1_C1_practice.tex](G11_T2_L1_C1_practice.tex) | Whole samples/observations, parameters/statistics, scope/draw subscripts | Four-column reference, `tab:notation-reference` | Covered |
| G11 C2 | [G11_T2_L1_C2_practice.tex](G11_T2_L1_C2_practice.tex) | z intervals, nominal/empirical coverage, simulation mean, counts/error, rounding, tails/Phi | Four-column reference, `tab:notation-reference` | Covered |
| G11 C3 | [G11_T2_L1_C3_practice.tex](G11_T2_L1_C3_practice.tex) | Interval-component graphs, rounded-cutoff theoretical area, budget feasibility | Four-column reference, `tab:notation-reference` | Covered |
| G11 C4 | [G11_T2_L1_C4_practice.tex](G11_T2_L1_C4_practice.tex) | Known-variance z intervals, cutoff areas, benchmark | Dedicated reference absent; propose after existing examples | Covered |
| G11 C5 | [G11_T2_L2_C5_practice.tex](G11_T2_L2_C5_practice.tex) | Population fraction, estimated SE, outcome counts, percentage points | Dedicated reference absent; propose after existing examples | Covered |
| G11 C6 | [G11_T2_L2_C6_practice.tex](G11_T2_L2_C6_practice.tex) | Mean/proportion sample-size planning, pilot input, achieved precision | Dedicated reference absent; propose after existing examples | Covered |
| G11 C7 | [G11_T2_L2_C7_practice.tex](G11_T2_L2_C7_practice.tex) | Sample-size/confidence comparisons for proportion intervals | Dedicated reference absent; propose after existing examples | Covered |
| G11 C8 | [G11_T2_L3_C8_practice.tex](G11_T2_L3_C8_practice.tex) | Unknown-SD t mean intervals, df and shape | Dedicated reference absent; propose after existing examples | Covered |
| G11 C9 | [G11_T2_L3_C9_practice.tex](G11_T2_L3_C9_practice.tex) | Design bias, sampling fraction, rare counts, outliers, grouping | Dedicated reference absent; propose after existing examples | Covered |
| G11 C10 | [G11_T2_L3_C10_practice.tex](G11_T2_L3_C10_practice.tex) | Merchant investigation, pilot planning, n−1 variance, t interval and scope | Dedicated reference absent; propose after existing examples | Covered |
| G10 C10 | No matching source in target directory | Source not found; legend pending. | No source-backed entries | Legend omitted per latest instruction |

Navigation aids: [README-G10T2PA.md](../../../grade10/term_2/1-practice_activities/README-G10T2PA.md); [README-G11T2PA.md](README-G11T2PA.md). Their descriptions lag revisions to G10 C3 and G11 C2/C3; this proposal follows live mathematics.

## Relevant dependencies and current definitions

| Source | Current responsibility |
|---|---|
| [specific_highlights.tex](../../../preamble/graphs/specific_highlights.tex) | Authoritative registry, G11 C1 palette, Ctwo wrappers, row helpers and local interval palette. |
| [highlights.tex](../../../preamble/graphs/highlights.tex) | Authoritative guarded renderer, six G10 bases and expectation wrapper. |
| [specific_highlights.md](../../../preamble/graphs/specific_highlights.md) | Descriptive reference; not authority over LaTeX/local overrides. |
| [G10_T2_bar_graphs.tex](../../../preamble/graphs/G10_T2_bar_graphs.tex) | Shared outcome/value/PMF graph APIs, color options, disabled mode and omitted-tail checks. |
| [preamble.tex](../../../preamble/preamble.tex) | Article class, math/table/TikZ/pgfplots packages, navigation. |
| [preamble_exams.tex](../../../preamble/preamble_exams.tex) | Exam-layer load chain and layout. |
| [preamble_G10_T1_C2C3.tex](../../../preamble/preamble_G10_T1_C2C3.tex) | Compatibility input into unified preamble. |
| [preamble_G10_T1_C1C2C3.tex](../../../preamble/preamble_G10_T1_C1C2C3.tex) | Loads common article preamble and decision/calculation helpers. |
| [preamble_exam_layout.tex](../../../preamble/preamble_exam_layout.tex) | Inherited exam geometry, columns and headers. |

**Current loading:** article/exam preamble → highlights → specific highlights where registry selection is used. Both highlight files guard repeated loading. `PracticeHighlightLegend{key}` dispatches to `practicehighlightlegend@<key>` and raises a package error for an unknown key. Neither preamble opts every activity into highlighting: G10 C4–C7/C9 and G11 C4–C10 lack highlight inputs. G10 C2/C3 load the renderer but have local legends without the registry.

**Current renderer:** `HighlightStroke` (`GTenHLStroke` alias) uses fill opacity **0.32**, text opacity **1**, 1 mm corners, no outline, 1.5 mm horizontal/.8 mm vertical padding. Math uses `mathpalette`, zero `mathsurround` and baseline-aligned nodes. Highlights default on; `GTenHighlightsfalse` returns the original argument. G10 C1/C2 compact padding to .6/.3 mm; G11 C2's local legend uses 1 mm horizontal padding; G11 C3 graph labels use .4 mm locally. A concurrent layout revision adds `CthreeTableHeader[alignment]{quantity}{qualifier}` using a two-line shortstack; preserve this local header helper, column alignment and unit qualifiers. Preserve footprints pending layout checks.

**Current overrides:** G10 C1 replaces its shared six-row/two-column entry with a mathematical three-column table. G10 C2 defines `cTwoMassMarker=GTenHLProbability` and `cTwoCDFMarker=#43A5C9` with local Value/Outcome/MassHL/CDFHL wrappers. G10 C3 forwards Indicator→Value, SuccessProb→Probability, FailureProb→Parameter, Money→Second and ExpectedValue→HLExpectedValue. G11 C2 replaces its shared legend with two Symbol/Concept/Formula tables, forwards Significance→Confidence and CI→Endpoint, and adds coverage counts and teal Error. Shared-summary behavior does not describe every activity-local override.

**Current bases:** G10 `GTenHLValue=#FFBB55`, Second `#8FD49A`, Third `#F1DA55`, Outcome `#BC9DE0`, Probability `#86BFF0`, Parameter `#ED9DAA`; `ExpectedValueColor=#6500A8`. G11 `G11T2C1SampleMean=#9BDD36`, PopulationMean `#FF765C`, SampleSD `#189338`, PopulationSD `#E42134`, SampleProportion `#23B895`, PopulationProportion `#D74383`, Sample `#173B17`, Population `#75162B` (all `G11T2C1`-prefixed). Ctwo Confidence `#55C8F0`, Critical `#2648BB`, SE `#F4D94B`, MoE `#F28A18`, default Endpoint `#A75A27`, default Width `#B83769` (identifiers `Ctwo<name>Color`). Ctwo Mean/Point/SD/Size reuse G11 population mean/sample mean/population SD/sample; Coverage reuses outcome lavender.

**Current orange override:** `CtwoPracticeIntervalPalette` selects Endpoint `CtwoMoEColor!45!white` and Width `CtwoMoEColor!45!black`. It creates no group: caller scope controls lifetime. The shared C2 legend calls it in a group, also grouping its helper redefinitions; the C2 activity calls it at setup scope. C3 uses default endpoint/width colors and explicit rows without this command.

**Base, mix, appearance:** an opaque base hex is not a final marker hex. Resolve xcolor mixes before applying .32 opacity over the actual background. On white the approximate RGB composition is .32 × selected RGB + .68 × white; other backgrounds and PDF/print color management differ. Opaque graph ink, a `!32` white mix and a translucent marker are different rendering mechanisms.

## Master semantic-role and palette specification

**Proposed contract.** Applicability and meanings are resolved by the criterion bindings above; the table below specifies the implementation. New aliases take one short text/math fragment. Reusing a color does not identify mathematical objects. `context` intentionally has no marker.

| Stable role ID | Meaning / representative notation | Grades and criteria | Wrapper / color identifier | Exact base or mix | Status / related family | Evidence and implementation implications |
|---|---|---|---|---|---|---|
| `outcome` | Complete result/space: $\omega,\Omega$ | G10 C1,C2 | `\GTenHLOutcome` / `GTenHLOutcome` | `#BC9DE0` | Retained structural lavender | Mapping tables/sequences; retain complete labels. |
| `event` | Set/complement: $E,E^c,A$ | G10 C1,C2,C3,C5,C9 | proposed `\HLMathEvent` / `GTenHLOutcome` | `#BC9DE0` | Added alias, structural family | Events/conditional waiting; define set versus result. |
| `quantity.primary` | Rule, value, support, cutoff; observations $y_j,x_i$ | G10 C1–C9; G11 C1,C2,C10 | `\GTenHLValue` / `GTenHLValue` | `#FFBB55` | Retained primary orange | Local definitions distinguish variable/value; exclude whole-sample X_i in G11 C1. |
| `quantity.secondary` | Second/transformed description: $Y=f(X),Y_i$ | G10 C1,C3–C9 | `\GTenHLSecond` / `GTenHLSecond` | `#8FD49A` | Retained secondary green | Revenue/payoff/transformation sources; own units, no independence implied. |
| `quantity.tertiary` | Third description: $Z,C$ | G10 C1 | `\GTenHLThird` / `GTenHLThird` | `#F1DA55` | Retained third yellow | First-buyer/card indicators; keep local definitions. |
| `probability` | Chance/mass/fraction: $P(A),p_X,m_X,p,p_0,p_i^*$ | G10 C1–C9; G11 C1,C5,C6,C7 | `\GTenHLProbability`, proposed `\HLPopulationProportion` / `GTenHLProbability` | `#86BFF0` | Retained; added alias changes target G11 p | Population fraction is success probability for a random unit. Planning/break-even definitions remain explicit. |
| `probability.complement` | Complement chance $1-p$ | G10 C3,C4,C5,C6,C9 | proposed `\HLComplementProbability` / `MathHLComplementColor` | `GTenHLProbability!65!CtwoCriticalColor` | Added blue mix; changes known failure pink | C3 FailureProb currently means known complement using unknown color. |
| `cumulative` | CDF/model area: $F_X,F_X(a^-),\Phi,C_{\rm normal}$ | G10 C2–C7,C9; G11 C2,C3,C4 | proposed `\HLCumulativeProbability` / `MathHLCumulativeColor` | `#43A5C9` | Added shared wrapper; retains local CDF base | Accumulation differs from mass; inverse output receives critical role, input is area. |
| `unknown` | Quantity to determine: $k,q,c,a,w$ | G10 C1,C2 | `\GTenHLParameter` / `GTenHLParameter` | `#ED9DAA` | Retained unknown pink | Missing masses/hidden conditions; solved unknown stays pink in derivation, blue as substituted known mass. |
| `count.design` | Fixed n, observed success counts, usable minimum | G10 C4,C6,C9; G11 C1–C10 | proposed `\HLObservationCount`, `\CtwoSize` / `G11T2C1Sample` | `#173B17` | Added alias retaining G11 count green | Fixed n differs from random quantity X; counts retain units and definitions. |
| `model.control` | Target r; reference df | G10 C6,C9; G11 C8,C10 | proposed `\HLModelControl` / `GTenHLParameter` | `#ED9DAA` | Added model-input alias | Given status/labels distinguish from unknowns; positive integer r and df=n−1. |
| `expectation` | $E(X),\mathbb E[Y_i],\mu,\lambda$, moments | G10 C3,C7,C8,C9; G11 C1,C2,C3,C4,C6,C8,C10 | `\HLExpectedValue`, proposed `\HLPopulationMean` / `ExpectedValueColor` | `#6500A8` | Retained expectation; target population mean changed from coral | G10 E(X)=mu; uniform population draw has expectation mu. Mark operator/result, preserve argument roles. |
| `variance.population` | Var(X), sigma²; squared spread | G10 C8; G11 C4 | proposed `\HLPopulationVariance` / `MathHLPopulationVarianceColor` | `G11T2C1PopulationSD!55!white` | Added light red mix | Squared units/name distinguish variance from SD. |
| `sd.population` | Individual-value spread sigma | G10 C8; G11 C1,C2,C3,C4,C6,C8 | proposed `\HLPopulationSD`, `\CtwoSD` / `G11T2C1PopulationSD` | `#E42134` | Retained G11; extended to G10 | Known/unknown sigma remains individual spread, not SE. |
| `context` | Operators/constants, rates, auxiliary states, assumptions, budgets | G10 C1–C9; G11 C2–C10 | optional `\HLMathContext` identity / `black` glyphs | `black` named xcolor; **no fill** | Retained neutral; optional alias | Definitions supply distinctions without new hues. No marker opacity applies. |
| `group.sample` | Whole selected sample X,X_i | G11 C1,C9,C10 | proposed `\HLSampleGroup` / `G11T2C1Sample` | `#173B17` | Retained identity; new alias | C1 indices identify entire draws, never observations. |
| `group.population` | Population and size: $\mathcal P,N$ | G11 C1,C4–C10 | proposed `\HLPopulationGroup` / `G11T2C1Population` | `#75162B` | Retained population identity; alias | Include eligibility/time/place; exclude interval-run N(C). |
| `mean.sample` | Sample mean/point estimate | G11 C1,C2,C3,C4,C8,C9,C10 | proposed `\HLSampleMean`, `\CtwoPoint` / `G11T2C1SampleMean` | `#9BDD36` | Retained sample lime | Keep bar/full subscripts; distinguish fixed population expectation. |
| `sd.sample` | Sample observation spread s | G11 C1,C2,C8,C9,C10 | proposed `\HLSampleSD` / `G11T2C1SampleSD` | `#189338` | Retained sample dispersion green | Original units; estimated SE remains yellow. |
| `variance.sample` | Sample variance s² | G11 C10 | proposed `\HLSampleVariance` / `MathHLSampleVarianceColor` | `G11T2C1SampleSD!55!white` | Added sample-dispersion mix | Preserve n−1 divisor and squared units from source. |
| `proportion.sample` | Observed fraction p-hat | G11 C1,C5,C7,C9 | proposed `\HLSampleProportion` / `G11T2C1SampleProportion` | `#23B895` | Retained sample teal | Define condition, numerator and denominator; fixed p is blue. |
| `standard.error` | Sampling spread or estimate: SE, estimated SE | G11 C2,C3,C4,C5,C7,C8,C10 | `\CtwoSE`, proposed `\HLStandardError` / `CtwoSEColor` | `#F4D94B` | Retained uncertainty yellow | Hat/formula distinguish estimated from known-sigma SE; neither individual SD nor realised error. |
| `confidence` | Chosen nominal central coverage C | G11 C2–C8,C10 | `\CtwoConfidence`, proposed `\HLConfidence` / `CtwoConfidenceColor` | `#55C8F0` | Retained nominal cyan | Setting differs from observed coverage/rounded-cutoff model area. |
| `tail` | Total excluded alpha, per-tail alpha/2 | G11 C2,C3,C4,C8 | proposed `\HLTailArea`, migrated `\CtwoSignificance` / `MathHLTailColor` | `CtwoConfidenceColor!55!CtwoCriticalColor` | Added related blue mix; changed target tails | Separate total/half-tail labels; no testing/p-value invented. |
| `critical` | Unitless reference cutoff z*,t* | G11 C2–C8,C10 | `\CtwoCritical`, proposed `\HLCriticalValue` / `CtwoCriticalColor` | `#2648BB` | Retained dark-blue cutoff | Reference distribution/df explicit; cutoff is not probability area. |
| `margin` | Half-width/target MoE,E | G11 C2–C8,C10 | `\CtwoMoE`, proposed `\HLMarginOfError` / `CtwoMoEColor` | `#F28A18` | Retained orange distance base | Target/achieved labels; response or percentage-point units. |
| `bounds` | L,U,CI,reported bounds | G11 C2,C3,C4,C5,C7,C8,C10 | `\CtwoEndpoint`, proposed `\HLIntervalBounds` / `MathHLBoundsColor` | `CtwoMoEColor!45!white` | Retained C2 mix; changed target C3 default | Separate bound strokes; brackets/comma neutral; no nested whole-interval stroke. |
| `width` | Full/reported width W | G11 C2,C3,C7 | `\CtwoWidth`, proposed `\HLIntervalWidth` / `MathHLWidthColor` | `CtwoMoEColor!45!black` | Retained C2 mix; changed target C3 default | Formula components retain roles; resulting full width gets this shade. |
| `coverage` | Finite-run Cov,N_cover,N(C) | G11 C2 | `\CtwoCoverage`, proposed `\HLObservedCoverage` / `GTenHLOutcome` | `#BC9DE0` | Retained empirical lavender; new alias | Counts are per procedure; not population N or sample n. Endpoint equality covers. |
| `coverage.error` | Absolute percentage-point gap E_abs | G11 C2 | `\CtwoError`, proposed `\HLCoverageError` / `CtwoErrorColor` | `#28AFA2` | Promoted local role with same teal | Compare percentage numbers; distinguish MoE/SE in response units. |

### Composition, domains and contextual distinctions

- Primary variables and values share orange; uppercase/lowercase, domains and units distinguish rule from value. Cutoffs may be outside support. Transformed variables keep their own channel. G11 C1 X_i is a whole green sample; G11 C10 x_i is one observation. Neither notation nor hue asserts independence.
- Outcomes are complete results; events sets; P(·) probabilities. Structural lavender does not identify sets with results. PMF mass is blue, cumulative area cyan, a CDF jump mass. Parameters follow meaning (p probability, n count, r target, lambda expectation); unknown status is contextual.
- Violet mu connects population mean to expectation of the measured variable, including uniform draws from finite populations. Sample x-bar stays lime. E(X²) averages squares; [E(X)]² squares a mean. Keep parentheses/squares and units; arguments retain variable roles, without nested strokes.
- Population/model variance and SD share red, sample variance/SD green, with distinct mixes and squared/original units. SE is yellow sampling spread or its estimate, not realised x-bar−mu or individual SD. Preserve n−1 in G11 C10. Hat/formula distinguish estimated SE.
- Keep nominal C, total alpha, each alpha/2, empirical Cov and theoretical C_normal separately defined. Use decimal 0<C<1 in finite two-sided normal-cutoff formulas; percentages on axes. E_abs compares percentage numbers and uses percentage points, not relative error. Observed coverage does not determine alpha.
- Preserve component roles in centre ± critical × SE. MoE is half-width, L/U bounds, W full width. Mark separate bounds in [L,U], punctuation neutral; do not nest markers. E is an event in G10 C3, expectation only as operator, margin in G11 C4–C10. W_rep=U_rep−L_rep need not equal unrounded W.
- Retain USD, thousand USD, thousand/million COP, minutes/hours and count units. Probability/proportion is unitless; percentage-point margin differs from percentage change. Counts are integers even when their expectations are not. Rate × exposure requires compatible units. Monetary signs do not alter probability roles. Support excludes zero masses and follows source endpoint cases.
- Define sums, factorials including 0!, combinations, e, distribution names, floor, conditioning, set membership, caps/waivers, nonnegativity/normalization and assumptions without extra hues. Auxiliary compositions, mixture states, recurrences and reserve balances stay local; their problem-solving insight remains in worked solutions. No opening legend certifies validity.
- Preserve open/filled endpoints, stems/steps, solid/dashed cover/miss lines and dots/crosses. Correspondence arrows are not probability trajectories. Label infinite models as finite previews and preserve omitted mass. Distinguish table points, theoretical curves and integer designs. Definitions remain readable without color.

## Grade 10-to-Grade 11 continuity

| Foundation | Grade 11 inheritance/extension | Concrete consequence |
|---|---|---|
| Variable, value, support and units | Measured observations; added sample/group objects | Keep orange observations; whole-sample X_i green only under its explicit local definition. |
| Event probability and Bernoulli p | Population fraction p is success probability for a randomly selected unit | Blue p across both grades; sample p-hat remains teal, with numerator/denominator defined. |
| PMF versus CDF | Normal cumulative areas and inverse cutoff selection | CDF cyan for Phi/model area, dark-blue critical cutoff for inverse output. |
| E(X)=mu | Fixed population mean estimated by a sample mean | Violet mu, including known simulation mean; lime x-bar estimates it. |
| Model variance/SD | Sample spread estimates and sampling uncertainty | Red population spread, green sample spread, yellow SE; preserve squared/original units. |
| Independence and observation rules | Random selection, sampling fraction, shape/outliers and grouping | Neutral explicit conditions; no “passed assumption” coloring that solves an audit task. |
| No inference intervals in G10 sources | Confidence/tails, cutoffs, margin, bounds, width and empirical coverage | Add source-backed inference roles only; do not repeat unrelated Poisson/stopping-model content in G11 general table. |

The tables list representative notation alternatives. When printing a criterion legend, show only forms defined in that activity (for example, X rather than an unused T); this is notation specialization within the same entry/role, not a new palette or mathematical meaning. Uppercase/lowercase and transformed/observed status remain part of definitions.

## Conflicts and their proposed resolution

| Current source evidence | Proposed resolution | Scope and dependency consequence |
|---|---|---|
| G10 C1 registry has a six-row/two-column table; activity overrides it locally | New coordinated three-column variant from shared row data | Retain old public key/macro; retire target override only after parity/anchor checks. |
| G10 C2 local CDF base/wrappers absent from registry | Promote #43A5C9 cumulative marker through a new alias | Preserve darker graph ink separately; do not treat marker hex as an opaque plot color. |
| G10 C3 FailureProb uses unknown pink for known 1−p | Blue-family complementary-probability wrapper | Keep GTenHLParameter unchanged for real unknowns. |
| G10 C8 legend omits variance, SD, mass and transformation inputs | Use the consolidated C8 subset above | Align detailed reference/body; keep old C8 key compatible. |
| G10 violet expectation versus G11 coral population mean | Target violet expectation/population-mean alias | Do not globally recolor G11T2C1PopulationMean; scope target palette explicitly. |
| G10 blue Bernoulli p versus G11 magenta population fraction | Blue probability/population-proportion treatment | Update target prose that currently describes all population measures as red. Legacy C1 slides retain their old appearance. |
| G11 C2 local legend uses Symbol/Concept/Formula | Requested concise schema plus separate detailed reference | Preserve four-column notation reference and task-table schemas; move extended formulas to their proper layer. |
| CtwoSignificance forwards to CtwoConfidence | Dedicated related-blue total-excluded/per-tail role | Keep alpha=1−C, separate total and half-tail labels; do not introduce p-values. |
| C2 orange-mixed bounds/width versus C3 brown/berry defaults | One orange family across coordinated interval targets | Keep shared defaults and original palette command available to legacy callers. |
| C2 local teal E_abs omitted by shared registry legend | Promote coverage-error alias/color and concise row | Remove duplicate local definition only once shared loading provides it. |
| C3 C_normal uses nominal-confidence marker | Model/cumulative-area role | Preserve numerical values and rounded-cutoff distinction; update labels/prose only. |
| Lavender covers outcomes and empirical coverage; dark green sample groups and n | Deliberate related/shared hues with separate semantic IDs | Concept labels and definitions remain mandatory; shared hue does not imply object identity. |
| G11 C8 assessed wording mentions proportions; demonstrated t methods estimate means | Propose only the demonstrated t-mean legend | Flag author review; do not invent t-proportion inference. |

## Registry and wrapper implementation plan

This is a future implementation specification. Keep the renderer and current toggle settings unchanged. Add shared role aliases and concise row data after existing definitions. Do not redefine legacy colors at registry load time. Add an explicit `CoordinatedTermTwoPalette` command in `specific_highlights.tex`, with caller-controlled scope; each new registry legend must call it inside a group. Target documents also select it before deriving graph colors so body and legend agree.

For existing target raw color calls, the target-only palette may map `G11T2C1PopulationMean` to `ExpectedValueColor`, `G11T2C1PopulationProportion` to `GTenHLProbability`, and Ctwo endpoint/width identifiers to the orange mixes. New wrappers should reference canonical semantic identifiers directly. Refresh derived `colorlet` graph colors after palette selection: `colorlet` captures the effective color when called. Forward aliases with one-argument commands when later redefinitions must be followed, rather than assuming every `let` behaves dynamically.

Keep complete atomic hats, bars and subscripts together. Keep relation/binary operators, alignment tokens and line breaks outside strokes; never nest markers. Apply roles by meaning, not global replacement of letters/numbers. Share row data and role macros between legends/references, but retain separate concise and detailed table bodies.

### Proposed general and criterion keys

All keys below are **new proposed keys**, including suffix `-coordinated` to preserve public legacy behavior.

| Grade | General catalog key | Criterion keys |
|---|---|---|
| 10 | `G10-T2-C1-C2-C3-C4-C5-C6-C7-C8-C9-coordinated` | `G10-T2-C1-coordinated`, `G10-T2-C2-coordinated`, `G10-T2-C3-coordinated`, `G10-T2-C4-coordinated`, `G10-T2-C5-coordinated`, `G10-T2-C6-coordinated`, `G10-T2-C7-coordinated`, `G10-T2-C8-coordinated`, `G10-T2-C9-coordinated` |
| 11 | `G11-T2-C1-C2-C3-C4-C5-C6-C7-C8-C9-C10-coordinated` | `G11-T2-C1-coordinated`, `G11-T2-C2-coordinated`, `G11-T2-C3-coordinated`, `G11-T2-C4-coordinated`, `G11-T2-C5-coordinated`, `G11-T2-C6-coordinated`, `G11-T2-C7-coordinated`, `G11-T2-C8-coordinated`, `G11-T2-C9-coordinated`, `G11-T2-C10-coordinated` |

Print each criterion's exact subset; general keys are catalogs for overviews, not required additions to every practice. No G10 C10 key is proposed.

Retain all **seven current public keys** with their default definitions/appearance:

- `G10-T2-C1` — shared six-row two-column table, while the target activity currently overrides it.
- `G10-T2-C1-C2-C3-C4-C5-C6-C7-C8-C9` — compact “Reading the markers” paragraph.
- `G10-T2-C8` — four-row expectation-focused table.
- `G11-T2-C1` — side-by-side Sample/Population concise tables.
- `G11-T2-C1-slides` — paired two-column table.
- `G11-T2-C2` — two-column shared legend with grouped orange palette and helper redefinitions.
- `G11-T2-C3` — explicit nine-row concise table with default palette.

Keep `GTenHighlightLegend` and existing registry dispatch/error behavior. Do not alias the compact overview key to a long catalog. Future coordinated slides need their own key/variant after source and overlay review; do not alias them to an incompatible practice layout.

Preserve `PracticeHighlightLegendCell{step}{content}` and C1 slide row helpers `GradeElevenCOneLegendGroups`, `...Means`, `...Deviations` and `...Proportions`. Each row helper accepts its reveal step; `GradeElevenCOneLegendTable` accepts four helpers and passes steps 2–5. The default cell emits all content. G11 C1 slides locally use `visible<step->` at the opening and print every cell in the closing table.

Preserve `CtwoLegendMeans`, `CtwoLegendConfidence`, `CtwoLegendCritical` and `CtwoLegendInterval` for legacy keys. Interval helper default [0] orders SE, margin, endpoints, width, confidence, critical; [1] inserts critical between SE and margin; other numeric arguments omit critical. C2's grouped local versions preserve branches/order and add units inside selected values; its confidence helper adds alpha/tails. C3 now uses explicit rows rather than those helpers. New coordinated keys should use separate row data instead of globally mutating these APIs.

### Explicit migration table

| Current key / wrapper / color → | Proposed treatment → | Affected consumers → | Compatibility approach |
|---|---|---|---|
| G10 C1 key/local override | Coordinated concise key with shared mathematical rows | Target G10 C1 | Keep old key and GTenHighlightLegend; remove target override only after parity/anchor checks. |
| Combined G10 C1–C9 key | Keep compact paragraph; add separate coordinated catalog | G10 Term 2 outline | No automatic alias to a long table. |
| G10 C8 key; HLExpectedValue/#6500A8 | Preserve expectation; add complete coordinated C8 subset | G10 C8; G10 C3 ExpectedValue alias | Old key callable; no expectation recoloring. |
| GTenHLValue/Second/Third/Outcome/Probability/Parameter | Retain bases and meanings; add semantic aliases | Target G10, G10 C1 slides/classroom, graph API | Do not globally redefine shared originals. |
| cTwoValue/Outcome/MassHL/CDFHL; local CDF #43A5C9 | Target aliases to canonical quantity/outcome/mass/cumulative | G10 C2; copied local names in G10 C2 classroom | Migrate target only; independently loaded classroom definitions remain valid. |
| Indicator/SuccessProb/FailureProb/Money/ExpectedValue | Keep roles except FailureProb → complement-blue mix | G10 C3 and its BreakEvenGraph | One-argument forwarding compatibility; do not redefine GTenHLParameter globally. |
| G11 C1 key; PopulationMean #FF765C; PopulationProportion #D74383 | Coordinated C1, violet mu and blue p | G11 C1 and CtwoMean target callers | Explicit target palette; old public colors/key remain default for slides. |
| G11 C1-slides key and paired-row helpers | Preserve legacy layout/palette/reveals | G11 C1 slide opening/closing | No implicit migration; future coordinated slide variant requires review. |
| CtwoMean/Point/SD/Size/SE/Critical/Confidence | Forward to canonical matching roles where needed | G11 C2/C3 and future C4–C10 | Explicit palette/key selection; no load-time global recoloring. |
| CtwoPracticeIntervalPalette; default Endpoint #A75A27, Width #B83769 | Coordinated orange mixes | G11 C2/C3 and future interval consumers | Preserve original command/defaults; apply target palette before graph derivation. |
| CtwoSignificance→Confidence; alpha/2 partly outside stroke | Tail role, complete alpha/2 atomic quantity | G11 C2 and relevant new legends | Preserve one-argument syntax and separate total/half-tail definitions. |
| CtwoCI→Endpoint | CI label/bound components | G11 C2 | Preserve syntax; avoid nested whole-interval strokes. |
| CtwoCoverage, zero-argument CtwoCoverCount/CtwoTotalCount | Preserve coverage/counter meaning | G11 C2 | Retain existing count-helper calling convention; N(C) per procedure, not population. |
| CtwoError / CtwoErrorColor #28AFA2 | Shared coverage-error alias/base | G11 C2 | Remove local duplicate only once shared definition is loaded. |
| CthreeSELine/MoELine/CriticalLine/ConfidenceLine | Retain dark derived inks; align labels | G11 C3 graphs and CthreePointLabel | Re-evaluate after palette selection; preserve coordinates/padding/line styles. |
| G10 C4–C7/C9, G11 C4–C10 without highlight inputs | Add renderer/registry once and select respective coordinated key | 12 currently unintegrated target activities | Preserve toggle policy and existing math/navigation; validate inherited load chain. |
| Existing specific_highlights.md | Reconcile only after actual LaTeX implementation | Shared reference/readers | Separate later summary workflow; never describe these proposals as live definitions. |

### Local graph inks and outside consumers

Retain graph ink derivations separately from marker fills:

- G10 C2 mass `blue!75!black`, CDF `cyan!65!blue!80!black`, guides `cTwoMassColor!35`; disabled mass/CDF black, guide gray. The marker colors remain their separate definitions.
- G10 C3 expectation ink `ExpectedValueColor!55!black` and probability ink `GTenHLProbability!50!black`; both black when disabled. Break-even dots/zero lines and explicit labels retain meaning.
- G11 C2 central fill `CtwoConfidenceColor!55`, cover ink `GTenHLOutcome!70!black`, miss ink `red!85!black`; disabled central fill `black!25` and both lines black. Solid/dot versus dashed/cross identifies cover/miss; red miss ink is not a population-parameter role.
- G11 C3 SE ink `CtwoSEColor!55!black`, MoE ink `CtwoMoEColor!75!black`, critical ink `CtwoCriticalColor`, confidence ink `CtwoConfidenceColor!50!black`; all black when disabled.

| Consumer outside target folders | Observed dependency / protection |
|---|---|
| [G10 C1 slides](../../../grade10/term_2/3-slides/G10_T2_L1_C1_slides.tex) | Shared GTen wrappers and local tables; no registry call. Preserve bases and local layout. |
| [G11 C1 slides](../3-slides/G11_T2_L1_C1_slides.tex) | Calls C1-slides key twice; opening locally reveals cells, closing shows all. Preserve default paired green/red presentation. |
| [G10 Term 2 outline](../../../grade10/term_2/5-extra_material/G10_T2_outline.tex) | Calls compact combined key; keep paragraph-sized behavior. |
| [G10 C1 classroom](../../../grade10/term_2/2-class_activities/G10_T2_L1_C1_classroom_activity.tex) | GTen wrappers/shared graph APIs; preserve source data, defaults and toggle state. |
| [G10 C2 classroom](../../../grade10/term_2/2-class_activities/G10_T2_L1_C2_classroom_activity.tex) | Own cTwo definitions; promoting names must not create duplicate commands. |
| [G11 C1 classroom](../2-class_activities/G11_T2_L1_C1_classroom_activity.tex) | Highlight load/toggle context; do not automatically opt into coordinated palette. |
| [G11 C2 classroom](../2-class_activities/G11_T2_L1_C2_classroom_activity.tex) | Highlight load/toggle context; preserve independent classroom flow. |
| [G11 Term 1 C3 practice](../../term_1/1-practice_activities/G11_T1_C3_practice_activity.tex) | Earlier highlight integration; no migration of its mathematics in this scope. |

Other search matches in G10 Term 1 and G11 Term 1/2 outlines include highlight-related guidance; they are not evidence that each calls the registry. Direct key-call search found the G10 Term 2 outline and G11 C1 slides as external registry callers. Shared graph-helper defaults affect multiple standalone consumers. No outside source is scheduled for migration by this proposal.

## Validation and acceptance criteria

### Proposal checks

Scope verification: this task wrote only this proposal in the repository. During the renderer check, 38 of 39 snapshotted LaTeX/reference files remained byte-identical; G11 C3 changed concurrently outside this task. Its new table-header/alignment work was re-inspected and does not alter the proposed semantic mapping. Pre-existing and concurrent repository edits, PDFs and temporary folders were left untouched.

- All 19 source-backed criteria are covered: G10 C1–C9 and G11 C1–C10. G10 C10 has no source and no legend section under the latest instruction.
- General tables are the ordered unions of criterion entry IDs. Every criterion row binds to a consolidated entry and stable master role; identical meanings are deduplicated. Meaningful distinctions (nominal, theoretical and observed coverage; individual versus sampling spread) remain explicit.
- Grade 11 contains only its source-backed content and identifies inherited versus new roles. Proposed changes have source evidence and target-scoped migration instructions.
- Check relative links, table cell counts, balanced math, section order, role references, criterion/general membership and byte preservation of existing sources/reference before delivery.
- Concise tables supply definitions rather than numerical practice answers or independent validity/model-selection decisions. Preserve extended definitions and introductory-example interpretations in detailed references.

Proposal validation performed: **57 relative file links resolved; 21 principal sections in the amended order; all 19 criterion tables match their grade catalogs; all 30 bound role IDs exist in the master specification; Markdown table cell counts and inline math delimiters passed.**

### Temporary renderer assessment

A temporary two-page palette sheet was compiled successfully with the installed pdfLaTeX engine using the actual unmodified `highlights.tex` renderer and loaded `specific_highlights.tex` definitions. It exercised all 30 proposed semantic-role treatments (including neutral context) as text and math atoms on white, once enabled and once disabled. Poppler rasterized both pages in color and grayscale. Visual inspection found legible black glyphs, intact superscripts/subscripts, no clipped samples, and no overfull/underfull box warnings in the preview log. Disabled wrappers retained every sample fragment. The two sheets have different spacing because disabling removes marker padding; that is existing renderer behavior.

The proposed violet expectation is distinguishable from outcome lavender; the orange margin/bounds/width family is coordinated, with bounds intentionally pale. Several blue shades, greens, and light variance markers are close, and related treatments collapse in grayscale. Therefore explicit concept labels, notation, units and line styles remain mandatory; hue alone is not an acceptance criterion. No claim of color-vision-deficiency simulation or print calibration is made.

This checks isolated palette/renderer behavior, not the full 19-activity layouts, all graph compositions, hyperlinks or slide overlays. Those checks have **not been performed** in this proposal stage. Temporary preview artifacts were removed after inspection; this task wrote no LaTeX or summary files. A concurrent G11 C3 source update was detected and rechecked separately. No preview is a permanent deliverable.

### Acceptance for a later implementation

1. Select explicit coordinated keys and retire only superseded local legends. Reuse table anchors and navigation; add unique anchors only where missing. Concise and detailed references remain different tables.
2. Check each role in prose, notation references, examples, solutions, table values and diagram labels by context, especially whole-sample X_i, conditional q/r, planning p_0, event/operator/margin E and interval/population N.
3. Build all 19 activities using the established article/exam chain and rerun for TOC/hyperlinks. Reject unknown keys, undefined wrappers/colors, duplicate anchors/destinations, new overfull tables and clipped labels. Inspect opening pages and long references.
4. Build isolated enabled/disabled versions, preserving committed toggles. Compare text retention and inspect grayscale. Related shades may collapse; labels, units, notation, line styles and open/filled endpoints must remain sufficient.
5. If shared definitions change, rebuild external G10 C1 slides/classroom, G11 C1 slides and compact overview, plus any other affected caller. Compare before/after appearance, reveal steps/closing visibility and Ctwo helper branches, rather than relying only on successful compilation.
6. Preserve mathematical wording, data, formulas, precision, rounding policies, graph coordinates/scales and independent tasks. Dark plot inks need their own contrast checks; pale marker mixes are not necessarily suitable opaque inks. Never renormalize finite previews.
7. After approved LaTeX implementation and verification, run the separate summary-update workflow to describe effective definitions, aliases, scope and variants. A second reconciliation should be unchanged.

## Missing sources and unresolved questions

- **G10 C10:** no practice LaTeX source found in the specified directory. “Source not found; legend pending.” remains an inventory status. The actual legend is omitted per the latest instruction. Inspect any later source before adding entries or a key.
- **G11 C8 wording:** assessed criterion mentions mean/proportion with Student's t; both worked methods estimate means. Author review must decide the wording or provide separate valid proportion content. No t-proportion method is invented.
- **Detailed-reference work:** G11 C4–C10 need dedicated references; G10 C4–C7/C9 need expansion/alignment and anchors. Their concise legends are source-backed; extended-table authoring and body markup remain future work.
- **Continuity tradeoff:** violet population mean and blue population proportion intentionally depart from the current all-red population-measure family. Target explanatory prose must reflect actual roles. Legacy slides keep public behavior until a separate source/overlay migration.
- **Visual limits:** a palette-sheet review does not certify all 19 document layouts, projection, paper/print conditions or all color-vision deficiencies. Those remain implementation acceptance work. No permanent preview is part of this Markdown-only deliverable.
- **Testing scope:** no observed hypothesis-test statistic, p-value calculation or hypothesis-test decision procedure occurs in these sources. z*/t* are critical values; reference distributions and standardized-statistic prose do not justify invented testing legends.
