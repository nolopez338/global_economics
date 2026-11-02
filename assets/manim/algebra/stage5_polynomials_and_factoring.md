# Stage 5: Polynomials and Factoring

**Duration:** 2 weeks

## 1. Purpose and learning goals

You used distribution in [Stage 2](stage2_algebraic_expressions.md) and functions in [Stage 4](stage4_linear_functions_and_systems.md). Now you will operate on polynomials, recognize identities, reverse expansion through factoring, and divide polynomials. These structures prepare you to solve quadratic equations; this unit focuses on rewriting and checking expressions.

**Prerequisite check**

- **P1.** Simplify \(3x+2x-4\).
- **P2.** Expand \(2x(x+3)\).
- **P3.** Evaluate \(p(2)\) if \(p(x)=x^2-5x+6\).

## 2. Guided lessons

### Lesson 1: Polynomial language and addition

A **monomial** is a constant times a variable raised to a nonnegative integer power, such as \(3x^2\). A **polynomial** is a finite sum of such terms; a binomial has two nonzero terms, and a trinomial has three. In one variable, its **degree** is the highest exponent with a nonzero coefficient after simplification. Nonzero constants have degree zero; the zero polynomial has no degree assigned here. Expressions such as \(1/x\) and \(\sqrt x\) are not polynomials in \(x\).

**Worked example.** Add \(3x^2-2x+1\) and \(x^2+5x-4\) by matching powers:
\[
(3x^2-2x+1)+(x^2+5x-4)=4x^2+3x-3.
\]
Subtracting instead gives \(3x^2-2x+1-x^2-5x+4=2x^2-7x+5\). Both results have degree 2. Subtraction distributes a negative sign across every term.

**Avoid this misconception:** the degree of \(4x^3+2x\) is 3, not \(3+1\). Degree concerns the largest power, not a sum across terms.

**Practice L1.** Simplify \((2x^2+x-1)-(x^2-3x+4)\); state its degree and number of terms.

### Lesson 2: Multiplication and special identities

Repeated distribution multiplies every term in one factor by every term in the other. The exponent rule \(x^mx^n=x^{m+n}\) combines variable factors. An area divided into smaller rectangles gives the same distributive structure.

**Worked example.**
\[
(x+2)(x+3)=x^2+3x+2x+6=x^2+5x+6.
\]
In general, \((x+a)(x+b)=x^2+(a+b)x+ab\). Setting \(b=a\), or replacing a plus with a minus, gives the identities
\[
(a+b)^2=a^2+2ab+b^2,\qquad
(a-b)^2=a^2-2ab+b^2,\qquad
(a-b)(a+b)=a^2-b^2.
\]
The last identity works because its two cross terms cancel. These identities hold for all real values of the letters.

**Avoid this misconception:** \((a+b)^2\) includes \(2ab\); it is not generally \(a^2+b^2\).

**Practice L2.** Expand (a) \((2x-3)^2\); (b) \((x-4)(x+4)\).

### Lesson 3: Greatest common factors and trinomial factoring

To **factor** is to rewrite a sum as a product. Start with the **greatest common factor (GCF)**, the largest common numerical factor together with the smallest power of each variable shared by all terms. Factoring reverses distribution, so expansion checks it.

**Worked example.** First factor \(2x^2+10x+12=2(x^2+5x+6)\). Since 2 and 3 have sum 5 and product 6, the outline's trinomial factors as \(x^2+5x+6=(x+2)(x+3)\). Hence the full factorization is \(2(x+2)(x+3)\).

For a leading coefficient other than one, split the middle term to make grouping possible. In \(6x^2+11x+3\), seek two numbers whose product is \(6\cdot3=18\) and sum is 11: 9 and 2. Then
\[
6x^2+9x+2x+3=3x(2x+3)+(2x+3)=(3x+1)(2x+3).
\]
This is justified by distributing the common binomial backward. If no integer pair works, a polynomial may not factor over integers; do not invent factors. Stage 6 supplies other solving methods.

**Avoid this misconception:** a common variable factor uses the smallest shared exponent: the GCF of \(6x^3\) and \(9x^2\) is \(3x^2\).

**Practice L3.** Factor completely over integers (a) \(3x^2-12x\); (b) \(x^2-x-6\).

### Lesson 4: Recognizing squares and grouping

Use the identities from Lesson 2 backward. A **difference of squares** factors as \(a^2-b^2=(a-b)(a+b)\). A **perfect square trinomial** has outer terms that are squares and a middle term equal to plus or minus twice their product. For four terms, **grouping** can expose a shared binomial.

**Worked example.** \(x^3+2x^2-9x-18\) has no overall nonconstant GCF, but grouping gives
\[
x^2(x+2)-9(x+2)=(x+2)(x^2-9)=(x+2)(x-3)(x+3).
\]
The last step uses a difference of squares. By comparison, \(x^2-6x+9=(x-3)^2\) is a perfect square trinomial because \(-6x=-2(x)(3)\).

**Avoid this misconception:** \(a^2+b^2\) has no matching difference-of-squares factorization over the reals. Check signs before choosing a pattern.

**Practice L4.** Factor (a) \(4x^2-25\); (b) \(x^2+8x+16\).

### Lesson 5: Polynomial division, remainders, and zeros

Polynomial long division repeats numerical long division: match leading terms, multiply the divisor, subtract, and continue until the remainder's degree is smaller than the divisor's. The result satisfies \(p(x)=d(x)q(x)+r(x)\), where \(d\ne0\) is the divisor, \(q\) the quotient, and \(r\) the remainder. Write missing powers with zero coefficients to keep columns aligned.

**Worked example.** Divide \(x^2+5x+7\) by \(x+2\). First \(x^2/x=x\). Subtract \(x(x+2)=x^2+2x\), leaving \(3x+7\). Next \(3x/x=3\). Subtract \(3(x+2)=3x+6\), leaving 1. Thus
\[
x^2+5x+7=(x+2)(x+3)+1.
\]
As a quotient expression this is \(x+3+1/(x+2)\), with \(x\ne-2\).

For division by \(x-a\), the remainder is constant. Substituting \(x=a\) into \(p(x)=(x-a)q(x)+r\) gives \(p(a)=r\): the **remainder theorem**. Therefore \(x-a\) is a factor exactly when \(p(a)=0\): the **factor theorem**. Such an input \(a\) is a **zero** of the polynomial function. Here \(p(-2)=1\), confirming the remainder; for \(x^2+5x+6\), \(p(-2)=0\), confirming its factor \(x+2\).

**Avoid this misconception:** quotient and remainder together reconstruct the dividend; dropping a nonzero remainder changes it.

**Practice L5.** Divide \(x^2-1\) by \(x-1\). Then find the remainder when \(x^2+2x+4\) is divided by \(x-2\) without long division.

## 3. Connected application

Recall the garden with width \(x>0\) m and length \(x+3\) m. Its area is \(A=x(x+3)=x^2+3x\) square meters. Increasing width from 2 to 3 to 4 m gives areas 10, 18, and 28 m²: successive gains are 8 and 10 m², not constant. The product of two changing dimensions explains why a linear model is inappropriate.

The expanded form separates a square of side \(x\) from a strip of width 3; the factored form displays the two dimensions. Algebraically, the polynomial has zeros 0 and \(-3\), because the product vanishes there. Neither is a valid width for this physical garden. Factoring now reveals structure; [Stage 6](stage6_quadratic_equations_and_functions.md) will use that structure to solve area equations and optimize a redesigned garden.

## 4. Essential summary

Polynomial addition collects like powers; multiplication distributes. Factoring reverses these operations, often through GCFs, trinomial patterns, special identities, or grouping. Division reconstructs a polynomial as divisor times quotient plus remainder. Evaluation at \(a\) links division by \(x-a\) to factors and zeros. Equivalent forms reveal different information about the same expression.

## 5. Independent mastery check

- **M1.** Simplify \((3x^2-2x+1)-(x^2+x-4)\); state its degree.
- **M2.** Expand \((2x-1)(x+3)\).
- **M3.** Factor completely: (a) \(2x^2+10x+12\); (b) \(9x^2-12x+4\).
- **M4.** Explain why \(x-4\) is a factor of \(p(x)=x^2-3x-4\), using both evaluation and multiplication.
- **M5.** Error analysis: \(x^2-16=(x-4)^2\). Correct the identity and show why the proposed answer fails.
- **M6.** Divide \(x^2+4x+5\) by \(x+1\), giving quotient and remainder; reconstruct the dividend.
- **M7.** An unfamiliar rectangular display has sides \(x+2\) cm and \(x+5\) cm, with \(x>0\). Write its expanded area and find the area at \(x=3\).
- **M8.** Factor \(x^3+3x^2-4x-12\) completely over integers.

**Mastery criteria:** at least 7 of 8 correct, checking factors by expansion and division by reconstruction. Revisit Lesson 1 for signs/degree, Lesson 2 for products, Lessons 3–4 for factoring, or Lesson 5 for remainders and zeros.

## 6. Answers and feedback

**Prerequisites**

- **P1.** \(5x-4\).
- **P2.** \(2x^2+6x\).
- **P3.** 0.

**Practice**

- **L1.** \(x^2+4x-5\), degree 2, three terms.
- **L2.** (a) \(4x^2-12x+9\); (b) \(x^2-16\).
- **L3.** (a) \(3x(x-4)\); (b) \((x-3)(x+2)\).
- **L4.** (a) \((2x-5)(2x+5)\); (b) \((x+4)^2\).
- **L5.** quotient \(x+1\), remainder 0; the second remainder is \(p(2)=4+4+4=12\).

**Mastery**

- **M1.** \(2x^2-3x+5\), degree 2.
- **M2.** \(2x^2+5x-3\).
- **M3.** (a) \(2(x+2)(x+3)\); (b) \((3x-2)^2\).
- **M4.** \(p(4)=16-12-4=0\); \((x-4)(x+1)=x^2-3x-4\).
- **M5.** \((x-4)(x+4)\); the proposed square expands to \(x^2-8x+16\).
- **M6.** quotient \(x+3\), remainder 2; \((x+1)(x+3)+2=x^2+4x+5\).
- **M7.** \(x^2+7x+10\) cm²; at 3, 40 cm².
- **M8.** \((x+3)(x^2-4)=(x+3)(x-2)(x+2)\).

## 7. Bridge to the next stage

Factoring exposes the dimensions hidden in an area expression. To find a width for a target area, we must solve a quadratic equation. [Stage 6: Quadratic Equations and Functions](stage6_quadratic_equations_and_functions.md) connects factors, roots, graphs, and maximum or minimum values.
