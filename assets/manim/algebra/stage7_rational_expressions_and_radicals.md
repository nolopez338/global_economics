# Stage 7: Rational Expressions and Radicals

**Duration:** 2 weeks

## 1. Purpose and learning goals

Fractions from [Stage 1](stage1_arithmetic_foundations.md), factors from [Stage 5](stage5_polynomials_and_factoring.md), and roots from [Stage 6](stage6_quadratic_equations_and_functions.md) now work together. You will manipulate algebraic fractions and radicals, state real-number domains, solve equations, check extraneous candidates, and interpret basic rational graphs.

**Prerequisite check**

- **P1.** Factor \(x^2-4\).
- **P2.** Calculate \(1/2+1/3\).
- **P3.** Solve \(x^2=9\). What is \(\sqrt9\)?

## 2. Guided lessons

### Lesson 1: Rational expressions and multiplicative operations

A **rational expression** is a quotient of polynomials. Its original denominator must not be zero, even if a simplified form appears to allow that input. Factoring permits cancellation of common **factors**, since a nonzero quantity divided by itself is one. Multiply fractions across; divide by multiplying by the reciprocal. In division, the divisor itself must also be defined and nonzero.

**Worked example.**
\[
\frac{x^2-4}{x-2}=\frac{(x-2)(x+2)}{x-2}=x+2,\qquad x\ne2.
\]
Extend this to a product:
\[
\frac{x^2-4}{x-2}\cdot\frac1{x+2}=1,
\qquad x\ne2,-2.
\]
For division,
\[
\frac{x^2-4}{x-2}\div\frac{x+2}{3}
=\frac{x^2-4}{x-2}\cdot\frac3{x+2}=3,
\qquad x\ne2,-2.
\]
Here \(x=-2\) is excluded because the original divisor would equal zero.

**Avoid this misconception:** \((x+2)/x\) does not simplify to 2. Terms in a sum cannot be canceled; \((x+2)/x=1+2/x\), with \(x\ne0\).

**Practice L1.** Simplify and retain restrictions: (a) \((x^2-9)/(x+3)\); (b) \((x/2)\div((x-1)/4)\).

### Lesson 2: Adding and subtracting rational expressions

As with numerical fractions, rewrite with a common denominator before combining numerators. Factoring helps find the **least common denominator (LCD)**, containing every needed factor to its largest required power. State exclusions from all original denominators. Subtracting a numerator subtracts the entire group.

**Worked example.** For \(x\ne0,-1\),
\[
\frac1x-\frac1{x+1}
=\frac{x+1}{x(x+1)}-\frac{x}{x(x+1)}
=\frac{(x+1)-x}{x(x+1)}
=\frac1{x(x+1)}.
\]
Each rewrite multiplies a fraction by a form of one. The denominator does not change during the final subtraction because the parts now have the same size.

**Avoid this misconception:** adding denominators, as in \(1/x+1/(x+1)=2/(2x+1)\), is not fraction addition.

**Practice L2.** Simplify \(2/x+3/(2x)\), giving restrictions.

### Lesson 3: Rational equations and excluded candidates

To solve a rational equation, list forbidden inputs, multiply every term by the LCD, solve the resulting equation, and check in the original. Multiplication by the LCD is reversible only where it is nonzero. An **extraneous solution** is a candidate produced by transformed equations that fails the original conditions.

**Worked example.** The outline's equation has \(x\ne2\):
\[
\frac{x+1}{x-2}=3\Rightarrow x+1=3(x-2)
\Rightarrow x=\frac72.
\]
Checking gives \((9/2)/(3/2)=3\). By contrast, \(1/(x-1)=x/(x-1)\), with \(x\ne1\), produces \(1=x\) after clearing denominators. Its only candidate is forbidden, so there is no solution.

**Avoid this misconception:** clearing a denominator does not remove its original restriction.

**Practice L3.** Solve \(2/(x-1)=1\), and check the candidate.

### Lesson 4: Radical expressions and rational exponents

An \(n\)th root reverses an \(n\)th power. For even \(n\), the real radicand must be nonnegative and the root symbol denotes the nonnegative root. Odd roots permit all real radicands. For positive bases, define \(a^{m/n}=\sqrt[n]{a^m}\), with integers \(m\) and positive \(n\); negative exponents take reciprocals, so zero is excluded. Zero to a positive rational power is zero; \(0^0\) and negative powers of zero are undefined here. For a negative base, first reduce \(m/n\); a real value is available when its reduced denominator is odd. This course uses exponent laws with positive bases unless such an odd-root case is explicitly stated.

For \(u,v\ge0\), \(\sqrt{uv}=\sqrt u\sqrt v\); the quotient rule also requires \(v>0\). These follow because both sides are nonnegative with the same square. In particular, \(\sqrt{x^2}=|x|\), not always \(x\).

**Worked example.** Extract square factors: \(\sqrt{72}=\sqrt{36\cdot2}=6\sqrt2\). Hence \(\sqrt{72}+\sqrt8=6\sqrt2+2\sqrt2=8\sqrt2\). Like radicals combine like terms. Products use \(\sqrt3\sqrt6=\sqrt{18}=3\sqrt2\); quotients use \(\sqrt{18}/\sqrt2=3\). Also, \(8^{2/3}=(\sqrt[3]8)^2=4\), linking roots and exponents. This now simplifies Stage 6's \(-3\pm\sqrt8\) to \(-3\pm2\sqrt2\).

**Avoid this misconception:** \(\sqrt{a+b}\) is not generally \(\sqrt a+\sqrt b\); for example, \(\sqrt{9+16}=5\ne7\).

**Practice L4.** (a) Simplify \(\sqrt{50}-\sqrt8\). (b) Evaluate \(16^{3/4}\) and \(\sqrt{(-5)^2}\).

### Lesson 5: Radical equations and checking after squaring

Isolate a radical before applying a power. Squaring both sides preserves equality but can lose sign information: \(2^2=(-2)^2\) although \(2\ne-2\). Thus it can introduce extraneous candidates. For a square-root equation, check both the radicand's nonnegativity and the other side's nonnegativity, then substitute candidates into the original.

**Worked example.** Solve \(\sqrt{x+2}=x\). The domain and sign conditions together require \(x\ge0\). Squaring gives \(x+2=x^2\), or \((x-2)(x+1)=0\). Candidate 2 works since \(\sqrt4=2\). Candidate \(-1\) fails since \(\sqrt1=1\ne-1\). The solution is \(x=2\).

**Avoid this misconception:** solving the squared equation is not the final step. Always check the unsquared equation.

**Practice L5.** Solve \(\sqrt{x+6}=x\), showing candidate checks.

### Lesson 6: Rational functions, holes, and asymptotes

A rational function uses a rational expression as its rule. A canceled denominator factor leaves a **hole**, a missing point, rather than restoring an input. A **vertical asymptote** \(x=a\) occurs when function values grow without bound as inputs approach \(a\) from a side. In a reduced rational expression, real denominator zeros give vertical asymptotes. A **horizontal asymptote** \(y=L\) describes the value approached as inputs grow very large positively or negatively; it need not be a boundary the graph never crosses.

**Worked example.** Rewrite
\[
f(x)=\frac{2x+1}{x-1}=2+\frac3{x-1},\qquad x\ne1.
\]
Near 1, the reciprocal term is unbounded: from the left \(f(x)\) decreases without bound, from the right it increases without bound. Thus \(x=1\) is a vertical asymptote. For large \(|x|\), \(3/(x-1)\) approaches zero, so \(y=2\) is horizontal. Range excludes 2 because the numerator 3 cannot become zero. Intercepts are \((-1/2,0)\) and \((0,-1)\); use these and the two asymptotes to sketch its two branches.

For a reduced rational function, degree comparison explains horizontal behavior: lower numerator degree gives \(y=0\); equal degrees give the ratio of leading coefficients; higher numerator degree gives no horizontal asymptote. For \((x^2-4)/(x-2)\), cancellation instead gives the line \(y=x+2\) with a hole at \((2,4)\), no vertical or horizontal asymptote.

**Avoid this misconception:** a denominator zero alone does not establish a vertical asymptote until common factors have been canceled and restrictions retained.

**Practice L6.** Find the domain, range, intercepts, and asymptotes of \(h(x)=1/(x+2)\).

## 3. Connected application

The event still has cost \(120+3n\) dollars and $8 tickets, with whole-number attendance up to 40. For \(n>0\), average cost per attendee is
\[
\overline C(n)=\frac{120+3n}{n}=3+\frac{120}{n}.
\]
At 20 attendees it is $9 per attendee; at 40 it is $6. Unlike total cost, this is not constant-rate behavior: the fixed $120 is shared among more people. The unrestricted positive-input extension approaches $3 per attendee, but never equals it at a finite attendance. With our capacity, actual inputs are just \(1,\ldots,40\); approaching an asymptote describes an extension beyond that feasible model. Setting \(\overline C(n)\le8\) and multiplying by positive \(n\) gives \(120\le5n\), so \(n\ge24\): the same break-even threshold from a new representation. Average cost is undefined for zero attendees.

## 4. Essential summary

Rational arithmetic follows fraction rules, with factoring exposing cancelable factors and permanent domain exclusions. Radicals and rational exponents express inverse powers with real-domain and sign conditions. Clearing denominators and squaring require checking candidates. Rational graphs distinguish holes from unbounded behavior and finite inputs from long-run trends.

## 5. Independent mastery check

- **M1.** Simplify \((x^2-x-6)/(x-3)\), giving restrictions and the missing graph point.
- **M2.** Simplify \(1/(x-1)+1/(x+1)\), stating restrictions.
- **M3.** Solve \((x+1)/(x-2)=3\), checking the original equation.
- **M4.** Simplify \(\sqrt{12}+\sqrt{27}\), and evaluate \(27^{2/3}\).
- **M5.** Error analysis: a learner squares \(\sqrt{x+2}=-x\), obtains candidates 2 and \(-1\), and accepts both. Find the actual solution and explain.
- **M6.** Analyze \(f(x)=4+2/(x-3)\): domain, range, intercepts, and asymptotes. Explain why 4 is not an output.
- **M7.** An unfamiliar square sign has area \(A\) square meters and perimeter 12 m. Write and solve a radical equation for \(A\), including the initial domain.
- **M8.** For the event, explain why total cost is linear in attendance but average cost is rational. Find the average at 30 attendees.

**Mastery criteria:** at least 7 of 8 correct, with restrictions and original-equation checks wherever needed. Revisit Lessons 1–2 for fractions, Lesson 3 for denominator exclusions, Lesson 4 for radicals, Lesson 5 for extraneous candidates, or Lesson 6 for graph behavior.

## 6. Answers and feedback

**Prerequisites**

- **P1.** \((x-2)(x+2)\).
- **P2.** \(5/6\).
- **P3.** equation roots \(\pm3\), principal square root 3.

**Practice**

- **L1.** (a) \(x-3\), \(x\ne-3\); (b) \(2x/(x-1)\), \(x\ne1\), since the divisor cannot be zero.
- **L2.** \(7/(2x)\), \(x\ne0\).
- **L3.** \(x=3\); \(2/(3-1)=1\).
- **L4.** (a) \(3\sqrt2\); (b) 8 and 5.
- **L5.** candidates 3 and \(-2\); only 3 works: \(\sqrt9=3\), while \(\sqrt4\ne-2\).
- **L6.** domain excludes \(-2\), range excludes 0, no \(x\)-intercept, \(y\)-intercept \((0,1/2)\); vertical \(x=-2\), horizontal \(y=0\).

**Mastery**

- **M1.** \(x+2\), \(x\ne3\); hole \((3,5)\).
- **M2.** \(2x/((x-1)(x+1))\), \(x\ne1,-1\).
- **M3.** \(x=7/2\); the original ratio is 3.
- **M4.** \(5\sqrt3\); 9.
- **M5.** only \(-1\) works: \(\sqrt1=1=-(-1)\); 2 gives \(2\ne-2\). Squaring lost the sign requirement \(x\le0\).
- **M6.** domain excludes 3, range excludes 4; \(x\)-intercept \((5/2,0)\), \(y\)-intercept \((0,10/3)\); vertical \(x=3\), horizontal \(y=4\). The nonzero reciprocal term cannot vanish.
- **M7.** using numerical measures in meters, \(4\sqrt A=12\); the radical requires \(A\ge0\), and a physical sign requires \(A>0\). Thus \(\sqrt A=3\), so \(A=9\) m²; its 3 m sides give a 12 m perimeter.
- **M8.** \(C(n)=120+3n\) adds $3 per attendee; dividing by \(n>0\) gives \(3+120/n\), a rational rule. At 30, average cost is $7 per attendee.

## 7. Bridge to the next stage

Power rules now include fractional and negative exponents. What if the variable itself is an exponent, as in repeated percentage growth? [Stage 8: Exponential and Logarithmic Functions](stage8_exponential_and_logarithmic_functions.md) introduces multiplicative models and the inverse operation needed to find elapsed time.
