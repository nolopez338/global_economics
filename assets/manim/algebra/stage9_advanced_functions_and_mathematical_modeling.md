# Stage 9: Advanced Functions and Mathematical Modeling

**Duration:** 2–4 weeks

## 1. Purpose and learning goals

You can now use linear, polynomial, rational, radical, exponential, and logarithmic rules. Building on [Stage 8](stage8_exponential_and_logarithmic_functions.md), this unit combines and reverses functions, interprets graph changes, describes discrete patterns, and evaluates models. You will analyze unfamiliar functions by asking what inputs are allowed, what outputs occur, and what structure explains their behavior.

**Prerequisite check**

- **P1.** Find the vertex and range of \(y=(x-2)^2+3\) on the real numbers.
- **P2.** Simplify \((x^2-1)/(x-1)\), keeping its restriction.
- **P3.** Solve \(200(1.1)^t=400\), giving an exact expression for \(t\).

## 2. Guided lessons

### Lesson 1: Evaluation, domains, ranges, and composition

Recall that \(f(x)\) is an output, the **domain** contains allowed inputs, and the **range** contains actual outputs. A formula's domain must respect denominators, even roots, and logarithm arguments, as well as contextual limits. Range requires examining the resulting values, not merely listing forbidden inputs.

The **composition** \((f\circ g)(x)=f(g(x))\) feeds the output of \(g\) into \(f\). Its domain requires both that \(g(x)\) exist and that its value lie in the domain of \(f\). Apply the inside function first.

**Worked example.** Let \(g(x)=x-1\) on all real numbers and \(f(u)=\sqrt u\) for \(u\ge0\). Then \((f\circ g)(x)=\sqrt{x-1}\), defined for \(x\ge1\), with range \([0,\infty)\). At \(x=10\), \(g(10)=9\), then \(f(9)=3\). Reversing the order gives \((g\circ f)(x)=\sqrt x-1\), with domain \([0,\infty)\) and range \([-1,\infty)\). These represent different operations.

**Avoid this misconception:** composition is not multiplication, and its order generally matters.

**Practice L1.** For \(f(u)=1/u\) and \(g(x)=x+2\), find \(f\circ g\), its domain and range, and its value at \(x=0\).

### Lesson 2: Constructing inverse functions and restricting domains

An inverse reverses a one-to-one function, as logarithms reverse exponentials in Stage 8. To construct it, write \(y=f(x)\), solve for \(x\) in terms of \(y\), then exchange the letters. The original domain becomes the inverse range; the original range becomes the inverse domain. Check both compositions on their proper domains.

**Worked example.** Event revenue is \(R(n)=8n\) dollars for \(n\in\{0,1,\ldots,40\}\). Solving \(r=8n\) gives \(R^{-1}(r)=r/8\) attendees. Its domain is \(\{0,8,16,\ldots,320\}\) dollars, not every real dollar amount: \(R^{-1}(192)=24\), but $193 cannot be exact ticket revenue under these assumptions. Also, \(R^{-1}(R(n))=8n/8=n\).

For \(q(x)=x^2\) on all real numbers, inputs 2 and \(-2\) share output 4, so it has no inverse function there. Restricting the domain to \([0,\infty)\) makes it one-to-one, with inverse \(q^{-1}(x)=\sqrt x\) on \([0,\infty)\). The restriction explains why the inverse uses the nonnegative root rather than \(\pm\sqrt x\).

**Avoid this misconception:** swapping coordinates does not guarantee the inverse relation is a function. Check one-to-one behavior or restrict the domain first.

**Practice L2.** Find the inverse of \(h(x)=3x-6\) on all real numbers and verify \(h^{-1}(h(x))=x\).

### Lesson 3: Graph transformations and absolute value

For \(y=af(b(x-h))+k\), with \(a,b\ne0\), \(h\) shifts horizontally and \(k\) vertically. Multiplication by \(a\) scales vertical distances by \(|a|\), with reflection across the horizontal axis if \(a<0\). The inside factor \(b\) scales horizontal distances by \(1/|b|\), with reflection if \(b<0\). These rules follow by tracking a point: \((u,f(u))\) becomes \((h+u/b,k+af(u))\). Transform the domain along with the graph.

The absolute value function \(y=|x|\) measures distance from zero. It has a V-shaped graph: \(y=x\) for \(x\ge0\) and \(y=-x\) for \(x<0\). This connects to the distance inequalities of [Stage 3](stage3_equations_and_inequalities.md).

**Worked example.** The outline's \(f(x)=|x-2|+3\) shifts that V right 2 and up 3. Its vertex is \((2,3)\), minimum is 3, domain is all real numbers, and range is \([3,\infty)\). It has \(y\)-intercept \((0,5)\) and no \(x\)-intercept because outputs are at least 3. Points \((1,4),(2,3),(3,4)\) guide the sketch; the two arms have slopes \(-1\) and 1. The expression \(x-2\) places the vertex at 2 because that is where the absolute-value input becomes zero.

**Avoid this misconception:** a minus sign inside a function does not shift the graph left; solve for the input that makes the inside zero.

**Practice L3.** Analyze \(p(x)=-2|x+1|+4\): vertex, domain, range, maximum, intercepts, and transformations from \(|x|\).

### Lesson 4: Piecewise-defined functions

A **piecewise-defined function** uses different rules on specified input regions. Evaluate by locating the input's region first. Boundaries must be assigned deliberately so that every domain input has exactly one output. On graphs, a filled endpoint is included and an open endpoint is excluded. A function may have a jump and still be a function.

**Worked example.** We introduce a new event cost policy for comparison; the original cost was \(C(n)=120+3n\). A supplier now offers a $20 total rebate once attendance reaches 30. With the same 40-person capacity and one $8 ticket per attendee, revised cost in dollars is
\[
C_{\mathrm{new}}(n)=
\begin{cases}
120+3n,&0\le n<30,\\
100+3n,&30\le n\le40,
\end{cases}
\qquad n\text{ a whole number}.
\]
Thus \(C_{\mathrm{new}}(29)=207\), while \(C_{\mathrm{new}}(30)=190\). The drop represents the stated rebate, not an arithmetic mistake. In a continuous sketch, the first branch ends with an open point at \((30,210)\) and the second begins with a filled point at \((30,190)\); actual attendance data are discrete points.

**Avoid this misconception:** do not substitute into both branches and choose a preferred result; the input condition selects the rule.

**Practice L4.** Under the revised policy, find cost and profit at 30 attendees and compare them with the original policy at 30.

### Lesson 5: Polynomial and rational function behavior

For large \(|x|\), a polynomial's leading term dominates its lower powers. An even-degree polynomial has matching end directions, up for a positive leading coefficient and down for a negative one. An odd-degree polynomial has opposite ends, rising to the right for a positive leading coefficient. A zero has **multiplicity** \(m\) when its factor \((x-r)^m\) appears \(m\) times. An odd power changes sign through \(r\); an even power does not, so the graph crosses or touches the axis, respectively.

**Worked example.** \(p(x)=(x+1)^2(x-2)\) has degree 3 with positive leading coefficient: its left end falls and its right end rises. It touches the axis at \(-1\) (multiplicity 2), crosses at 2 (multiplicity 1), and has \(y\)-intercept \((0,-2)\). Except at the double zero, its sign is negative for \(x<2\) and positive for \(x>2\). Its domain and range are all real numbers: the continuous graph extends without bound in both vertical directions. These features guide a sketch without locating every turning point.

For rational functions, factor first and retain exclusions. For \(r(x)=(x^2-1)/(x-1)=x+1\), \(x\ne1\), the graph is a line missing \((1,2)\), so its range excludes 2. For a noncanceled denominator, division can expose behavior: \((x^2-1)/(x-2)=x+2+3/(x-2)\). It has vertical asymptote \(x=2\); for large \(|x|\), it approaches the sloping line \(y=x+2\) because the remainder term approaches zero. This extends [Stage 7's horizontal-asymptote analysis](stage7_rational_expressions_and_radicals.md).

**Avoid this misconception:** multiplicity does not change the location of a zero; it changes local graph behavior. A denominator exclusion may create a hole rather than an asymptote.

**Practice L5.** Describe the zeros, multiplicities, axis-crossing behavior, \(y\)-intercept, and end behavior of \(q(x)=-(x-1)^2(x+2)^2\).

### Lesson 6: Arithmetic and geometric sequences

A **sequence** is a function with integer indices, here \(n=0,1,2,\ldots\). An **explicit formula** gives a term directly from its index; a **recursive formula** gives a starting term and a rule using previous terms. An arithmetic sequence adds a common difference \(d\):
\[
a_n=a_0+nd,\qquad a_{n+1}=a_n+d.
\]
A geometric sequence multiplies by a common ratio \(r\):
\[
a_n=a_0r^n,\qquad a_{n+1}=ra_n.
\]
These formulas follow by adding \(d\), or multiplying by \(r\), exactly \(n\) times. For nonzero terms, a constant ratio tests a geometric pattern. Always state the starting index; using \(a_1\) instead requires \(n-1\) in the explicit formulas.

**Worked example.** Event costs at successive attendance counts form \(c_0=120\), \(c_{n+1}=c_n+3\), or \(c_n=120+3n\), for \(0\le n\le40\) under the original policy. Population predictions form \(N_0=200\), \(N_{n+1}=1.1N_n\), or \(N_n=200(1.1)^n\), with \(n\) in whole years. These are discrete versions of linear and exponential models. The revised rebate policy is not one arithmetic sequence across its threshold because the difference changes there.

**Avoid this misconception:** arithmetic and geometric patterns are distinguished by differences and ratios, not by whether the values “grow quickly.”

**Practice L6.** A sequence begins \(5,15,45,\ldots\), with first index 0. Give recursive and explicit formulas and find term \(a_4\).

### Lesson 7: Comparing and testing model families

Choose a model by its mechanism and evidence, then test it. Constant differences suggest linear behavior; constant second differences at equally spaced inputs suggest a quadratic; constant positive ratios suggest an exponential. Reciprocal sharing suggests a rational rule. These patterns support a model over the observed range; a few points cannot establish that it will hold forever.

**Worked example.** Measured outputs at inputs 0, 1, 2, 3 are 1, 4, 9, 16. First differences are 3, 5, 7; second differences are 2, 2. A candidate quadratic is \(y=(x+1)^2\), which matches all four points. It predicts 25 at input 4. A new measurement of 24.8 gives a **residual**, observed minus predicted, of \(-0.2\). Whether that is acceptable depends on units and measurement precision; systematic residual patterns would suggest a poor model. The formula alone does not reveal a physical cause, so seek a mechanism and test more data before extrapolating.

**Avoid this misconception:** matching known points is insufficient justification for unlimited prediction. **Interpolation** stays within observed inputs; **extrapolation** goes beyond them and needs stronger assumptions.

**Practice L7.** At equally spaced inputs 0, 1, 2, outputs are 8, 12, 18. Propose a model and justify its family. What further evidence would you seek before extending it far beyond input 2?

## 3. Connected application

The three recurring contexts now answer different questions with different model families:

| Context and unchanged or revised assumptions | Model and parameter meanings | What the structure explains |
|---|---|---|
| Original event: $120 fixed, $3 per attendee, $8 tickets, capacity 40 | \(C(n)=120+3n\), \(R(n)=8n\), \(P(n)=5n-120\); \(n\) whole, \(0\le n\le40\) | Constant marginal amounts justify linear rules; break-even is 24 attendees. |
| Same event, average cost, \(1\le n\le40\) | \(\overline C(n)=3+120/n\) dollars per attendee | Sharing a fixed cost creates a reciprocal term. |
| Redesigned garden: perimeter 20 m; the earlier length-plus-3 rule is replaced | \(A(x)=x(10-x)=-(x-5)^2+25\), \(0<x<10\) | Two linked dimensions create a quadratic; maximum is 25 m² at width 5 m. |
| Population: initial 200, constant 10% yearly growth | \(N(t)=200(1.1)^t\), \(t\ge0\) years | A constant ratio justifies exponential growth; doubling time is \(\ln2/\ln1.1\). |

Suppose the original event can expect 30 attendees. Revenue is $240 and cost is $210, giving $30 profit. Under the explicitly revised rebate policy, cost is $190 and profit $50. At 40 attendees, revised profit is \(320-220=100\) dollars. Both revised profit branches rise by $5 per additional attendee, with an upward jump at 30; hence the maximum over the feasible domain is $100 at 40 attendees. This conclusion uses the piecewise rule, capacity, and integer domain together. It assumes the supplier actually honors the rebate and that attendance causes no further costs.

For each new situation, define variables and units, identify constraints, justify a family, estimate parameters, solve the relevant question, and compare predictions with evidence. Algebra now supports a defensible decision rather than only a calculation.

## 4. Essential summary

Composition chains processes; inversion reverses one-to-one processes and exchanges domain with range. Transformations track points from a familiar graph. Piecewise rules encode changes in conditions. Factors and leading terms explain polynomial zeros and end behavior; cancellations and division explain rational graphs. Sequences represent discrete change. A useful model combines mathematical fit, meaningful parameters, explicit restrictions, and a credible mechanism.

## 5. Independent mastery check

- **M1.** Let \(f(u)=\ln u\), \(g(x)=x-3\). Find \(f\circ g\), domain, range, value at \(x=4\), and vertical asymptote.
- **M2.** For \(q(x)=(x-2)^2\) restricted to \(x\ge2\), find its inverse, inverse domain and range, and explain the chosen square-root sign.
- **M3.** Analyze \(f(x)=|x-2|+3\): transformations, vertex, domain, range, minimum, and intercepts. Explain why there is no real zero.
- **M4.** Under the revised event rebate rule, calculate profit at 29 and 30 attendees and explain the size of the change. Is the profit sequence arithmetic across this threshold?
- **M5.** Error analysis: “\((x^2-4)/(x-2)=x+2\), so its domain and range are all real numbers.” Correct the domain, range, and graph description.
- **M6.** For \(p(x)=(x+2)^3(x-1)^2\), state zeros, multiplicities, crossing/touching behavior, degree, \(y\)-intercept, and end behavior.
- **M7.** Give explicit and recursive formulas, starting at index 0, for (a) \(7,11,15,\ldots\); (b) \(3,6,12,\ldots\). Find term 5 of each.
- **M8.** An unfamiliar cooling experiment records temperatures 80, 50, 35 °C at 0, 1, 2 minutes in a room at 20 °C. Compare raw differences and ratios, then examine temperature **above room temperature**. Propose a justified model, interpret its parameters, predict minute 3, and give a limitation and a way to check the prediction.

**Mastery criteria:** at least 7 of 8 correct independently, including M8's model justification and accurate restrictions in M1–M2 and M5. Revisit Lessons 1–2 for composition/inverses, Lesson 3 for transformations, Lesson 4 for branch conditions, Lesson 5 for polynomial/rational graphs, Lesson 6 for sequence indexing, or Lesson 7 for evidence and limitations. Repair errors, then apply the ideas to a fresh problem before declaring mastery.

## 6. Answers and feedback

**Prerequisites**

- **P1.** vertex \((2,3)\), range \([3,\infty)\).
- **P2.** \(x+1\), \(x\ne1\).
- **P3.** \(t=\ln2/\ln1.1\).

**Practice**

- **L1.** \(1/(x+2)\), domain excludes \(-2\), range excludes 0, value \(1/2\).
- **L2.** \(h^{-1}(x)=(x+6)/3\); \((3x-6+6)/3=x\).
- **L3.** left 1, vertical stretch by 2, reflection across the horizontal axis, up 4; vertex \((-1,4)\), domain all real numbers, range \((-\infty,4]\), maximum 4, \(x\)-intercepts \((-3,0),(1,0)\), \(y\)-intercept \((0,2)\).
- **L4.** revised cost $190 and profit $50; original cost $210 and profit $30.
- **L5.** degree 4, leading coefficient \(-1\), both ends down; zeros 1 and \(-2\), both multiplicity 2, both touch without crossing; \(y\)-intercept \((0,-4)\).
- **L6.** \(a_0=5\), \(a_{n+1}=3a_n\); \(a_n=5\cdot3^n\), \(a_4=405\).
- **L7.** \(y=8(1.5)^x\), justified by ratios 1.5; seek more measurements, a multiplicative mechanism, and limits on constant growth.

**Mastery**

- **M1.** \(\ln(x-3)\), domain \((3,\infty)\), range all real numbers, value 0 at 4, vertical asymptote \(x=3\).
- **M2.** \(q^{-1}(x)=2+\sqrt x\), domain \([0,\infty)\), range \([2,\infty)\); the original restriction requires \(x-2\ge0\).
- **M3.** right 2 and up 3; vertex \((2,3)\), domain all real numbers, range \([3,\infty)\), minimum 3, \(y\)-intercept \((0,5)\), no \(x\)-intercept because \(|x-2|+3\ge3\).
- **M4.** profits \(232-207=25\) dollars and \(240-190=50\) dollars; the $25 increase is the usual $5 contribution plus the new $20 rebate. It is not arithmetic across the threshold.
- **M5.** domain excludes 2, range excludes 4; line \(y=x+2\) with hole \((2,4)\).
- **M6.** \(-2\), multiplicity 3, crosses; 1, multiplicity 2, touches; degree 5, \(y\)-intercept \((0,8)\); left end down, right end up.
- **M7.** (a) \(a_n=7+4n\), \(a_0=7,a_{n+1}=a_n+4\), \(a_5=27\); (b) \(b_n=3\cdot2^n\), \(b_0=3,b_{n+1}=2b_n\), \(b_5=96\).
- **M8.** raw differences \(-30,-15\) and ratios \(50/80,35/50\) are not constant. Excess temperatures 60, 30, 15 halve each minute, suggesting \(T(t)=20+60(0.5)^t\) °C, \(t\ge0\) minutes. The room baseline is 20 °C, initial excess 60 °C, retention factor 0.5 per minute. At minute 3, prediction is 27.5 °C. Constant room conditions and proportional cooling are assumptions; measure minute 3 and compare its residual with instrument precision before extending the model.

## 7. Bridge to further study

The progression began with meaningful arithmetic, used letters to generalize it, then used equations and functions to describe constraints and change. Factoring linked structure to zeros; quadratics linked graphs to optimization; rational and radical work clarified domains; logarithms reversed multiplicative growth. You can now combine these tools, select a model, and explain both its predictions and its limits.

You are ready for precalculus and trigonometry when you can analyze an unfamiliar function, justify transformations, and check a contextual result independently. Later calculus will ask how change behaves at an instant and how quantities accumulate. Keep the same habits: define quantities, respect domains, connect representations, justify steps, and test conclusions against the original problem.
