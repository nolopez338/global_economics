# Stage 6: Quadratic Equations and Functions

**Duration:** 2 weeks

## 1. Purpose and learning goals

[Stage 5](stage5_polynomials_and_factoring.md) developed polynomial factors and zeros. Now you will solve degree-two equations, choose efficient methods, analyze parabola graphs, and use a maximum or minimum to answer a design question. You will connect equations, factors, roots, and function values while distinguishing real and complex solutions.

**Prerequisite check**

- **P1.** Factor \(x^2-5x+6\).
- **P2.** Expand \((x-3)^2\).
- **P3.** Evaluate \(f(0)\) for \(f(x)=x^2-5x+6\); what graph feature does it give?

## 2. Guided lessons

### Lesson 1: Factoring and the square root method

A **quadratic expression** has form \(ax^2+bx+c\), where \(a\ne0\); a quadratic equation sets such an expression equal to zero. The **zero-product property** says that a product is zero only if at least one factor is zero: if neither factor were zero, dividing by either could not yield a zero product.

**Worked example.** The outline's equation becomes
\[
x^2-5x+6=0\Rightarrow(x-2)(x-3)=0
\Rightarrow x=2\text{ or }x=3.
\]
Substitution checks both. If a square is already isolated, use roots instead: \((x-1)^2=9\Rightarrow x-1=\pm3\Rightarrow x=4,-2\). The symbol \(\pm\) means consider both plus and minus. Generally, \(u^2=k\) gives \(u=\pm\sqrt k\) for \(k>0\), one solution \(u=0\) for \(k=0\), and no real solution for \(k<0\).

**Avoid this misconception:** \((x-2)(x-3)=6\) does not permit setting each factor equal to 6 or zero. First rewrite an equation with zero on one side.

**Practice L1.** Solve (a) \(x^2-7x+12=0\); (b) \((x+2)^2=16\).

### Lesson 2: Completing the square

Completing the square rewrites \(x^2+px\) using \((x+p/2)^2=x^2+px+(p/2)^2\). Half the linear coefficient, then square it: this supplies precisely the missing constant. For equations, add that amount to both sides. For expressions, add and subtract it to preserve value.

**Worked example.** Solve \(x^2+6x+1=0\):
\[
x^2+6x=-1\Rightarrow x^2+6x+9=8
\Rightarrow(x+3)^2=8
\Rightarrow x=-3\pm\sqrt8.
\]
These exact roots need not be decimals; Stage 7 will simplify radicals. The same reasoning rewrites the expression as \(x^2+6x+1=(x+3)^2-8\). Its smallest real value is \(-8\), achieved at \(x=-3\), since a real square cannot be negative. If the leading coefficient is not 1, divide the equation by it before completing the square.

**Avoid this misconception:** adding 9 to only one side changes the equation; adding and subtracting 9 inside one expression preserves that expression.

**Practice L2.** Rewrite \(x^2-4x+7\) as a square plus a constant, then state its minimum value and where it occurs.

### Lesson 3: Quadratic formula, discriminant, and complex roots

Completing the square in \(ax^2+bx+c=0\) gives \((2ax+b)^2=b^2-4ac\). Taking both square roots and isolating \(x\) yields
\[
x=\frac{-b\pm\sqrt{b^2-4ac}}{2a},\qquad a\ne0.
\]
This **quadratic formula** works even when factoring is inconvenient. The **discriminant** \(\Delta=b^2-4ac\) describes the roots: two distinct real roots if \(\Delta>0\), one repeated real root if \(\Delta=0\), and no real roots if \(\Delta<0\).

**Worked example.** For \(2x^2+3x-2=0\), \(a=2,b=3,c=-2\), so \(\Delta=9+16=25\). Thus \(x=(-3\pm5)/4\), giving \(1/2\) and \(-2\). Factoring \((2x-1)(x+2)\) checks them.

To describe roots when \(\Delta<0\), define \(i\) by \(i^2=-1\). A **complex number** is \(u+vi\), with real \(u,v\). For \(x^2-2x+5=0\), completing the square gives \((x-1)^2=-4\), so \(x=1\pm2i\), since \((2i)^2=-4\). These are algebraic solutions, not points on a real \(x\)-axis. No broader complex-number theory is needed here.

**Avoid this misconception:** a negative discriminant means no **real** roots, not no complex roots. Keep all of \(2a\) beneath the full numerator.

**Practice L3.** (a) Use the formula on \(x^2+x-1=0\). (b) Classify and find the roots of \(x^2+4=0\).

### Lesson 4: Quadratic forms and parabola graphs

A quadratic function's graph is a **parabola**. Its forms reveal different features:

- Standard form \(f(x)=ax^2+bx+c\) shows the \(y\)-intercept \((0,c)\).
- Factored form \(f(x)=a(x-r_1)(x-r_2)\), when real roots exist, shows the zeros and \(x\)-intercepts.
- Vertex form \(f(x)=a(x-h)^2+k\) shows the vertex \((h,k)\) and vertical axis of symmetry \(x=h\).

The squared distances \((x-h)^2\) match on both sides of \(h\), explaining symmetry. If \(a>0\), the graph opens upward with minimum \(k\); if \(a<0\), it opens downward with maximum \(k\). Its unrestricted real domain is all real numbers; range is \([k,\infty)\) or \((-\infty,k]\), respectively. Larger \(|a|\) makes equal horizontal displacements produce larger vertical changes. Completing the square gives \(h=-b/(2a)\), and \(k=f(h)\).

**Worked example.** \(f(x)=x^2-4x+3=(x-1)(x-3)=(x-2)^2-1\). Plot vertex \((2,-1)\), intercepts \((1,0),(3,0),(0,3)\), and its symmetric partner \((4,3)\); draw a smooth upward curve. The minimum is \(-1\), the axis is \(x=2\), and the range is \([-1,\infty)\). These features all describe the same function.

**Avoid this misconception:** the vertex is not generally an intercept. Zeros are inputs; intercepts are coordinate pairs.

**Practice L4.** For \(g(x)=-2(x-1)^2+8\), state the vertex, axis, maximum, range, and both \(x\)-intercepts.

### Lesson 5: Quadratic inequalities

A quadratic inequality asks where the graph lies above or below the \(x\)-axis. Find real zeros to divide the number line into intervals, then test the sign in each interval. A polynomial is continuous, so it cannot change sign between zeros without passing through zero. Include zeros for \(\le\) or \(\ge\); exclude them for strict inequalities.

**Worked example.** Solve \(x^2-4x+3\le0\). Factor to \((x-1)(x-3)\le0\). Below 1, both factors are negative, so their product is positive. Between 1 and 3, their signs differ, so the product is negative. Above 3, both are positive. Including zeros gives \([1,3]\), matching the portion of the parabola on or below its axis intercepts.

**Avoid this misconception:** do not solve an inequality by requiring both factors to be negative; their product would be positive.

**Practice L5.** Solve \(x^2-9>0\), giving interval notation.

## 3. Connected application

We now redesign the garden. Earlier its length was always width plus 3 m. **Replace that constraint** with a fixed perimeter of 20 m; the old length rule no longer applies. Let width be \(x\) m and length \(l\) m. From \(2x+2l=20\), \(l=10-x\), and positive dimensions require \(0<x<10\).
\[
A(x)=x(10-x)=-x^2+10x=-(x-5)^2+25.
\]
Area is in square meters. This quadratic has maximum 25 m² at \(x=5\) m, giving a 5 m by 5 m square. Increasing one dimension now forces the other to decrease, so area first rises and then falls. Widths 4 and 6 m both give 24 m². The physical range is \((0,25]\); zero area is excluded by positive dimensions. The model assumes a rectangle, no gate allowance, and exactly 20 m of usable boundary. Vertex form turns earlier area calculations into an optimization argument.

## 4. Essential summary

Choose factoring when factors are apparent, roots when a square is isolated, completing the square to reveal a vertex, or the formula for a general equation. The discriminant connects algebraic root types to real-axis crossings. Standard, factored, and vertex forms reveal intercepts, zeros, and extrema. Inequalities compare graph heights with zero; optimization applies extrema within a contextual domain.

## 5. Independent mastery check

- **M1.** Solve \(x^2-5x+6=0\) by factoring and verify both roots.
- **M2.** Solve \(2(x-3)^2=18\).
- **M3.** Complete the square for \(x^2+2x-5\). Use the result to find its roots and minimum.
- **M4.** Find the discriminant and all complex solutions of \(x^2-4x+8=0\). Explain what its real graph does relative to the \(x\)-axis.
- **M5.** Error analysis: “\(f(x)=(x+2)^2-9\) has vertex \((2,-9)\).” Correct it; give its axis, range, and intercepts.
- **M6.** Solve \(x^2-x-6\ge0\).
- **M7.** An unfamiliar rectangular pen has 24 m of fencing for all four sides. Find the dimensions giving maximum area and justify the model and domain.
- **M8.** Explain why a constant-rate model cannot describe \(A(x)=x(x+3)\). Compare increases from widths 1 to 2 to 3 m.

**Mastery criteria:** at least 7 of 8 correct, including method explanations, graph features, and domain-aware optimization. Revisit Lesson 1 for roots/factors, Lesson 2 for square completion, Lesson 3 for formula/complex roots, Lesson 4 for graph forms, or Lesson 5 for signs. Review Section 3 for contextual extrema.

## 6. Answers and feedback

**Prerequisites**

- **P1.** \((x-2)(x-3)\).
- **P2.** \(x^2-6x+9\).
- **P3.** 6, the \(y\)-intercept \((0,6)\).

**Practice**

- **L1.** (a) 3, 4; (b) 2, \(-6\).
- **L2.** \((x-2)^2+3\), minimum 3 at \(x=2\).
- **L3.** (a) \((-1\pm\sqrt5)/2\); (b) \(\Delta=-16\), no real roots, complex roots \(\pm2i\).
- **L4.** vertex \((1,8)\), axis \(x=1\), maximum 8, range \((-\infty,8]\), intercepts \((-1,0),(3,0)\).
- **L5.** \((-\infty,-3)\cup(3,\infty)\).

**Mastery**

- **M1.** 2 and 3; each gives zero on substitution.
- **M2.** \((x-3)^2=9\), so \(x=0,6\).
- **M3.** \((x+1)^2-6\), roots \(-1\pm\sqrt6\), minimum \(-6\) at \(x=-1\).
- **M4.** \(\Delta=-16\), \(x=2\pm2i\); \((x-2)^2+4>0\), so the graph lies above the axis.
- **M5.** vertex \((-2,-9)\), axis \(x=-2\), range \([-9,\infty)\), \(x\)-intercepts \((-5,0),(1,0)\), \(y\)-intercept \((0,-5)\).
- **M6.** \((x-3)(x+2)\ge0\), giving \((-\infty,-2]\cup[3,\infty)\).
- **M7.** width \(x\), length \(12-x\), \(0<x<12\); \(A=-(x-6)^2+36\), so 6 m by 6 m, maximum 36 m².
- **M8.** areas 4, 10, 18 m² have unequal gains 6 and 8 m²; two changing dimensions produce a quadratic, not a constant rate.

## 7. Bridge to the next stage

Roots such as \(\sqrt8\) need useful equivalent forms, and averages such as cost per attendee place a variable in a denominator. [Stage 7: Rational Expressions and Radicals](stage7_rational_expressions_and_radicals.md) develops both ideas with careful restrictions and solution checks.
