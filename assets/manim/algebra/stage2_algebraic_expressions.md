# Stage 2: Algebraic Expressions

**Duration:** 2 weeks

## 1. Purpose and learning goals

In [Stage 1](stage1_arithmetic_foundations.md), you calculated event costs for particular attendance counts. Algebra lets one expression describe all those calculations. You will define variables, translate descriptions, evaluate expressions, and use number properties to expand and simplify them without changing their values.

**Prerequisite check**

- **P1.** Evaluate \(120+3(20)\).
- **P2.** Calculate \(-4+7\) and \(2(3+5)\).
- **P3.** Calculate \(3/4+1/2\).

## 2. Guided lessons

### Lesson 1: Variables, constants, and algebraic notation

A **variable** is a symbol representing a quantity whose value may change or be unknown. A **constant** has a fixed value in the situation. An **expression**, such as \(3n+120\), names a value through operations; it makes no claim that two things are equal. An **equation**, such as \(3n+120=180\), asserts equality and asks which values make it true. Solving equations comes in Stage 3.

Terms are parts separated by addition or subtraction; treat subtraction as addition of a negative. In \(3n-2m+120\), the terms are \(3n,-2m,120\); 3 and \(-2\) are **coefficients**, the numerical multipliers of variables. Adjacent letters mean multiplication: \(ab=a\cdot b\), not a two-digit number. Write \(3n\) instead of \(3\times n\) to avoid confusing \(\times\) with the letter \(x\).

**Worked example.** Let \(n\) be the number of event attendees. The cost expression \(120+3n\), in dollars, has constant term 120 and coefficient 3 dollars per attendee. For \(n=20\), substitution gives \(120+3(20)=180\) dollars. Here \(n\) takes whole-number values \(0,1,2,\ldots\), because attendees are counted.

**Avoid this misconception:** a variable need not stand for one permanently hidden number; here it describes many possible attendance counts.

**Practice L1.** In \(5t-9\), identify the variable, coefficient, and constant term. Evaluate at \(t=4\).

### Lesson 2: Translating words and evaluating expressions

First name the quantity and its units, then translate the operations. “Five less than twice a number” becomes \(2x-5\): the phrase “less than” reverses the spoken order. Parentheses show which quantity an operation acts on. Evaluating means replacing every occurrence of a variable with its specified value and then using the arithmetic order of operations.

**Worked example.** A rectangular garden is \(x\) meters wide and \(x+3\) meters long, where \(x>0\). Its perimeter is the sum of all four sides:
\[
2x+2(x+3).
\]
At \(x=4\), this is \(2(4)+2(4+3)=8+14=22\) meters. Its area is \(x(x+3)\) square meters; at \(x=4\), the area is \(4(7)=28\) square meters. Perimeter and area describe different measurements.

**Avoid this misconception:** “the square of the sum of \(x\) and 3” is \((x+3)^2\), not \(x^2+3\). For negative substitutions, use parentheses: at \(x=-2\), \(x^2=4\).

**Practice L2.** (a) Write “half the sum of \(a\) and 6,” then evaluate at \(a=10\). (b) Evaluate \(2x^2-x\) at \(x=-3\).

### Lesson 3: Combining like terms

**Like terms** have exactly the same variable factors and exponents. Distribution explains why coefficients can be combined: \(ax+bx=(a+b)x\). Thus \(3x+5x\) means eight copies of \(x\), but \(3x+5\) combines unlike quantities and cannot become \(8x\). Simplification produces an equivalent expression, one with the same value for every allowed input.

**Worked example.** Simplify
\[
4x+3-2x+7=(4-2)x+(3+7)=2x+10.
\]
Commutative and associative properties allow the regrouping. At \(x=5\), both forms give 20; this checks one input, while the properties justify all inputs. Terms \(x\) and \(x^2\) are unlike because they represent different powers.

**Avoid this misconception:** \(x+x=2x\), whereas \(x\cdot x=x^2\). Addition counts copies; multiplication builds a power.

**Practice L3.** Simplify (a) \(7y-3+2y+8\); (b) \(3x^2+2x-x^2\).

### Lesson 4: Distribution and expansion

To **expand** an expression is to remove products involving parentheses by distributing each multiplier to every term. This follows from splitting a total into parts. A negative sign outside parentheses means multiplication by \(-1\), so every enclosed sign changes.

**Worked example.** The outline's expression becomes
\[
3(x+2)-2x=3x+6-2x=x+6.
\]
For subtraction of a group, \(5x-2(x-3)=5x-2x+6=3x+6\). Each equality here is an **identity**: it holds for every real \(x\). Unlike solving an equation for selected values, we are rewriting the same quantity.

**Avoid this misconception:** \(3(x+2)\ne3x+2\); both terms must be multiplied by 3.

**Practice L4.** Expand and simplify (a) \(4(a-2)+a\); (b) \(6-2(3-y)\).

## 3. Connected application

The school event still costs $120 plus $3 per attendee and charges $8 per ticket. Let \(n\) be the nonnegative whole-number attendance. Cost is \(120+3n\) dollars; revenue is \(8n\) dollars. Profit is revenue minus the entire cost:
\[
8n-(120+3n)=8n-120-3n=5n-120.
\]
The coefficient 5 means each additional attendee contributes $5 toward covering the fixed cost and then earning profit. At \(n=30\), profit is \(5(30)-120=30\) dollars, matching Stage 1. We can now represent any attendance count without rewriting the reasoning. We still assume one ticket per attendee, constant costs, and no capacity limit; we have not yet found the attendance needed for a target profit.

## 4. Essential summary

An expression names a quantity; an equation asserts equality; an identity is an equality true throughout its stated domain. Variables require meanings and allowed values. Evaluation turns a general expression into a number. Combining like terms and distributing produce equivalent expressions because real-number properties hold for every permitted substitution.

## 5. Independent mastery check

- **M1.** Identify the terms and coefficients in \(6x-4y+9\).
- **M2.** Evaluate \(3a^2-2b\) at \(a=-2,b=5\).
- **M3.** Simplify \(2(3x-4)-(x+5)\).
- **M4.** Explain why \(4x+3x=7x\) is an identity but \(4x+3=7x\) is not.
- **M5.** Error analysis: a learner simplifies \(7-(2x-1)\) to \(6-2x\). Correct and explain.
- **M6.** An unfamiliar phone plan charges $9 monthly plus $0.04 per message. Define a variable, write the monthly cost, and evaluate for 150 messages.
- **M7.** Write a simplified perimeter expression for the garden with width \(x\) m and length \(x+3\) m. Evaluate at \(x=5/2\).

**Mastery criteria:** at least 6 of 7 correct, including accurate translation, distribution, and the explanation in M4. Revisit Lesson 1 for notation, Lesson 2 for translation/substitution, Lesson 3 for unlike terms, or Lesson 4 for sign errors. Explain corrections and attempt a new example independently.

## 6. Answers and feedback

**Prerequisites**

- **P1.** 180.
- **P2.** 3 and 16.
- **P3.** \(5/4\). Review [Stage 1](stage1_arithmetic_foundations.md) if signs or fractions prevent substitution.

**Practice**

- **L1.** variable \(t\), coefficient 5, constant \(-9\); value 11.
- **L2.** (a) \((a+6)/2\), value 8; (b) \(2(9)+3=21\).
- **L3.** (a) \(9y+5\); (b) \(2x^2+2x\).
- **L4.** (a) \(5a-8\); (b) \(2y\), since \(6-6+2y=2y\).

**Mastery**

- **M1.** terms \(6x,-4y,9\); variable coefficients 6 and \(-4\).
- **M2.** \(12-10=2\).
- **M3.** \(6x-8-x-5=5x-13\).
- **M4.** distribution gives \((4+3)x\) for all \(x\); the second equality fails, for example, at \(x=0\).
- **M5.** \(7-2x+1=8-2x\); subtracting the group changes both signs.
- **M6.** \(m\) is a nonnegative whole-number message count; cost \(9+0.04m\) dollars, giving $15.
- **M7.** \(4x+6\) meters; at \(x=5/2\), 16 m.

## 7. Bridge to the next stage

An expression predicts profit for a chosen attendance. How many attendees produce zero profit, or at least $50? [Stage 3: Equations and Inequalities](stage3_equations_and_inequalities.md) uses equality and comparisons to find the allowed inputs.
