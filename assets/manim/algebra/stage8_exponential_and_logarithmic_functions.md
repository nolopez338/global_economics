# Stage 8: Exponential and Logarithmic Functions

**Duration:** 2 weeks

## 1. Purpose and learning goals

Earlier functions put variables in sums, products, or denominators. Here the variable can be an exponent. Building on [Stage 7's exponent rules](stage7_rational_expressions_and_radicals.md), you will recognize repeated percentage change, interpret growth and decay parameters, model compound interest, and use logarithms to recover an exponent. You will also connect inverse functions and their graphs.

**Prerequisite check**

- **P1.** Simplify \(2^3\cdot2^{-1}\).
- **P2.** Increase 200 by 10%. Then increase that result by 10%.
- **P3.** If \(f(x)=3x+1\), what input produces output 10?

## 2. Guided lessons

### Lesson 1: Exponential functions and multiplicative change

An exponential function has form \(f(t)=Ab^t\), where \(b>0\), \(b\ne1\), and \(A\ne0\). We use \(A>0\) for growth/decay quantities. Unlike a polynomial such as \(t^2\), its variable is in the exponent. Exponent laws explain the constant ratio: \(f(t+1)/f(t)=b\). For positive bases these laws extend from integer powers through rational powers to real powers. Equal input increments multiply outputs by equal factors; linear functions instead add equal differences.

**Worked example.** A population begins at 200 and increases by 10% each year under a simplified model. Let \(t\) be years since observation began and \(N(t)\) the predicted population count:
\[
N(t)=200(1.10)^t.
\]
At years 0, 1, 2, the values are 200, 220, 242. Differences 20 and 22 are unequal, but both ratios are 1.10. For \(t\ge0\), the continuous model has range \([200,\infty)\); actual observed counts at integer years are whole numbers, while predictions may need rounding. The all-real-input extension has domain all real numbers, range \((0,\infty)\), \(y\)-intercept \((0,200)\), no \(x\)-intercept, and horizontal asymptote \(y=0\) toward negative time.

A growth rate \(r\) gives factor \(b=1+r>1\). A decay fraction \(d\), with \(0<d<1\), gives \(b=1-d\), between zero and one. For example, retaining 80% each hour gives \(Q(t)=Q_0(0.8)^t\), not \(Q_0(0.2)^t\). Decay approaches zero as time increases without reaching it in this model.

**Avoid this misconception:** 10% growth does not add 20 forever; the percentage applies to the current amount.

**Practice L1.** (a) A substance starts at 80 g and loses 25% each hour. Write its model and find the amount after 2 hours. (b) Is \(3t^2\) exponential? Explain.

### Lesson 2: Compound interest as repeated growth

Compound interest adds interest to the balance, so later interest is earned on earlier interest. With principal \(P\), nominal annual rate \(r\) as a decimal, and \(m\) equal compounding periods per year, each period multiplies the balance by \(1+r/m\). After \(mt\) periods,
\[
A(t)=P\left(1+\frac rm\right)^{mt}.
\]
For balances at crediting times, \(mt\) is a nonnegative integer. The model assumes a fixed rate, no deposits, withdrawals, taxes, or fees.

**Worked example.** A hypothetical $500 deposit earns a nominal 6% per year compounded quarterly. The quarterly rate is \(0.06/4=0.015\). After 2 years (8 quarters), \(A=500(1.015)^8\approx563.25\) dollars. Simple interest would give \(500(1+0.06\cdot2)=560\) dollars because it uses only the original principal as the base. The difference comes from compounding, not a changed quoted annual rate.

**Avoid this misconception:** use 0.06 for 6%, and match the rate per period with the number of periods.

**Practice L2.** Find the balance of a hypothetical $1,000 deposit at 4% annually, compounded annually for 3 years. Round to cents only at the end.

### Lesson 3: Inverse functions, logarithms, and graphs

An **inverse function** reverses input and output. It exists on a chosen domain when the original function is **one-to-one**: no two inputs share an output. Exponentials \(b^x\), for \(b>0,b\ne1\), are one-to-one. Their inverse is the **logarithm**:
\[
\log_b y=x\quad\Longleftrightarrow\quad b^x=y,
\qquad y>0.
\]
A logarithm is the exponent required to produce its argument. Thus \(\log_2 8=3\), \(\log_b1=0\), and \(\log_b b=1\). Inverse identities are \(\log_b(b^x)=x\) and \(b^{\log_b y}=y\) for \(y>0\).

**Worked example.** The points \((0,1),(1,2),(2,4)\) on \(y=2^x\) become \((1,0),(2,1),(4,2)\) on \(y=\log_2x\). Swapping coordinates reflects a graph across \(y=x\). The logarithmic graph has domain \((0,\infty)\), range all real numbers, \(x\)-intercept \((1,0)\), no \(y\)-intercept, and vertical asymptote \(x=0\). For base greater than one it increases; for base between zero and one it decreases. For \(y=\log_2x\), outputs decrease without bound as \(x\) approaches zero from the right.

**Avoid this misconception:** an inverse function is not a reciprocal. \(f^{-1}(x)\) means an inverse rule; \(1/f(x)\) means a reciprocal value.

**Practice L3.** (a) Convert \(5^3=125\) to logarithmic form. (b) Find \(\log_3(1/9)\) and state why \(\log_3(-9)\) has no real value.

### Lesson 4: Logarithmic properties and natural logarithms

For \(u,v>0\), exponent laws give
\[
\log_b(uv)=\log_bu+\log_bv,\quad
\log_b(u/v)=\log_bu-\log_bv,\quad
\log_b(u^k)=k\log_bu.
\]
For example, writing \(u=b^p,v=b^q\) turns a product into \(b^{p+q}\), proving the product rule. These properties require positive arguments. \(\ln x\) means \(\log_e x\), where \(e\approx2.71828\) is a standard base used in growth mathematics; \(\log_{10}x\) is a common logarithm. We write the base explicitly unless using \(\ln\).

**Worked example.** For \(x>0\), \(\ln(3x^2)=\ln3+2\ln x\). Conversely, \(\ln12-\ln3=\ln4\). To change bases, let \(y=\log_bu\), so \(b^y=u\). Taking natural logarithms gives \(y\ln b=\ln u\), hence
\[
\log_bu=\frac{\ln u}{\ln b},\qquad u>0,\ b>0,\ b\ne1.
\]
The denominator is nonzero because \(\ln b=0\) only at \(b=1\).

**Avoid this misconception:** there is no sum rule \(\log_b(u+v)=\log_bu+\log_bv\). At base 10, \(\log_{10}(1+1)\ne0+0\).

**Practice L4.** (a) Expand \(\ln(5x^3/y)\) for \(x,y>0\). (b) Write \(\log_2 7\) using natural logarithms.

### Lesson 5: Exponential and logarithmic equations

If both sides are powers of the same valid base, equality of outputs forces equality of exponents. Otherwise isolate the exponential, take logarithms, and use the power rule. For logarithmic equations, state argument restrictions first, combine logs where appropriate, convert to exponential form, and check all candidates.

**Worked example.** The outline's \(2^x=16=2^4\) gives \(x=4\). For \(2^x=10\), take natural logarithms: \(x\ln2=\ln10\), so \(x=\ln10/\ln2\approx3.3219\). Check that \(2^3<10<2^4\). For a logarithmic equation, \(\ln x+\ln(x-1)=\ln6\) requires \(x>1\). Combining logs gives \(x(x-1)=6\), so \((x-3)(x+2)=0\). Only \(x=3\) is valid; \(-2\) makes the original logarithms undefined.

**Avoid this misconception:** do not round a logarithm ratio before the final step, or accept a candidate without checking its original arguments.

**Practice L5.** Solve (a) \(3^{2x}=27\); (b) \(\ln(x-2)=\ln5\), with restrictions.

## 3. Connected application

Return to the population starting at 200 with 10% annual growth: \(N(t)=200(1.10)^t\). When does the model reach 400?
\[
200(1.10)^t=400\Rightarrow(1.10)^t=2
\Rightarrow t=\frac{\ln2}{\ln1.10}\approx7.27\text{ years}.
\]
This is a continuous interpolation of yearly multiplication. If we inspect only year-end observations, the first year with at least 400 is year 8: predictions are about 389.74 at year 7 and 428.72 at year 8. Logs answer a new question: how long until a target, rather than how much after a given time? The model assumes a constant percentage rate and sufficient resources. Real populations have varying rates, whole-number counts, and environmental constraints; indefinite growth is an extrapolation, not a guarantee.

## 4. Essential summary

Linear change adds a fixed amount; exponential change multiplies by a fixed factor. Growth, decay, and compounding differ in the factor and period used. Logarithms reverse exponentiation, so their domains are positive and their graphs reverse exponential input–output roles. Log laws follow from exponent laws and turn exponent equations into solvable linear statements in the unknown exponent.

## 5. Independent mastery check

- **M1.** Values at times 0, 1, 2 are 50, 60, 72. Justify an exponential model and write it. Explain why a linear model fails for these points.
- **M2.** An amount starts at 300 g and decays by 20% per day. Find the amount after 3 days.
- **M3.** Find the hypothetical balance after 2 years for $800 at nominal 8% compounded semiannually.
- **M4.** Explain the inverse relationship between \(y=3^x\) and \(y=\log_3x\). State the logarithm's domain, range, intercept, and asymptote.
- **M5.** Error analysis: a learner says \(\ln(x+2)=\ln x+\ln2\). Explain the mistake using \(x=1\).
- **M6.** Solve \(5^x=12\), giving an exact logarithmic expression and a decimal to three places.
- **M7.** Solve \(\log_2(x-1)+\log_2(x-3)=3\), checking restrictions.
- **M8.** An unfamiliar machine retains 90% of its current value each year. Starting at $2,000, when does its continuous exponential model fall to $1,000? What is the first whole year at or below that value?

**Mastery criteria:** at least 7 of 8 correct, including model justification, log domains, and interpretation of time. Revisit Lesson 1 for growth factors, Lesson 2 for compounding periods, Lesson 3 for inverses/graphs, Lesson 4 for log properties, or Lesson 5 for equations.

## 6. Answers and feedback

**Prerequisites**

- **P1.** \(2^2=4\).
- **P2.** 220, then 242.
- **P3.** 3, since \(3(3)+1=10\).

**Practice**

- **L1.** (a) \(Q(t)=80(0.75)^t\) g for \(t\ge0\) hours, giving 45 g; (b) no, it is a polynomial with fixed exponent.
- **L2.** \(1000(1.04)^3=1124.864\), or $1,124.86.
- **L3.** (a) \(\log_5 125=3\); (b) \(-2\); a positive-base exponential never outputs a negative number.
- **L4.** (a) \(\ln5+3\ln x-\ln y\); (b) \(\ln7/\ln2\).
- **L5.** (a) \(x=3/2\); (b) \(x>2\), candidate \(x=7\) works.

**Mastery**

- **M1.** ratios 1.2, unequal differences 10 and 12; \(N(t)=50(1.2)^t\).
- **M2.** \(300(0.8)^3=153.6\) g.
- **M3.** \(800(1.04)^4\approx935.89\) dollars.
- **M4.** each undoes the other; swapped coordinates reflect across \(y=x\). Log domain \((0,\infty)\), range all real numbers, intercept \((1,0)\), vertical asymptote \(x=0\).
- **M5.** at \(x=1\), left is \(\ln3\), right is \(\ln1+\ln2=\ln2\), disproving the claim. The product rule applies to \(2x\), not \(x+2\).
- **M6.** \(x=\ln12/\ln5\approx1.544\).
- **M7.** \(x>3\); \((x-1)(x-3)=8\) gives \(x=5,-1\), so only 5.
- **M8.** \(2000(0.9)^t=1000\), so \(t=\ln(0.5)/\ln(0.9)\approx6.579\) years; first whole year 7.

## 7. Bridge to the next stage

You now have several model families and inverse operations. [Stage 9: Advanced Functions and Mathematical Modeling](stage9_advanced_functions_and_mathematical_modeling.md) combines them, changes their graphs, builds sequences and piecewise rules, and asks which model is justified by a situation and its evidence.
