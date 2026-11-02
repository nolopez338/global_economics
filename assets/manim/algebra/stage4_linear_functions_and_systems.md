# Stage 4: Linear Functions and Systems

**Duration:** 2 weeks

## 1. Purpose and learning goals

[Stage 3](stage3_equations_and_inequalities.md) found inputs satisfying a condition. Here you will represent whole relationships with tables, graphs, and functions; interpret constant rates; and solve simultaneous conditions. You will move between verbal descriptions, coordinates, equations, and graphs, with attention to units and allowed inputs.

**Prerequisite check**

- **P1.** Solve \(5n-120=0\).
- **P2.** Evaluate \(2x-3\) at \(x=0\) and \(x=2\).
- **P3.** Solve \(2y+4=10\).

## 2. Guided lessons

### Lesson 1: Coordinates, relations, and functions

The **Cartesian coordinate system** has a horizontal \(x\)-axis and vertical \(y\)-axis meeting at the origin \((0,0)\). An ordered pair \((x,y)\) gives horizontal then vertical position; negative coordinates go left or down. A **relation** is a set of input–output pairs. A **function** assigns exactly one output to each allowed input. A graph represents a function when every vertical line meets it at most once.

The **domain** is the set of allowed inputs; the **range** is the set of resulting outputs. The independent variable is the input, and the dependent variable is the output. Function notation \(f(x)\), read “f of x,” means the output associated with \(x\), not \(f\) times \(x\).

**Worked example.** For \(f(x)=2x-3\) with domain \(\{0,1,2\}\), the pairs are \((0,-3),(1,-1),(2,1)\), and the range is \(\{-3,-1,1\}\). Plot these three points using the axes. If instead the domain is all real numbers, the same formula gives an entire line with real-number range. The relation \(\{(1,2),(1,4)\}\) is not a function because input 1 has two outputs.

**Avoid this misconception:** different inputs may share an output. \(\{(1,4),(2,4)\}\) is a function.

**Practice L1.** (a) Is \(\{(-1,3),(0,3),(2,5)\}\) a function? State its domain and range. (b) Find \(g(-2)\) for \(g(x)=3x+1\).

### Lesson 2: Slope, line forms, and intercepts

A linear function has constant rate of change \(m=\Delta y/\Delta x=(y_2-y_1)/(x_2-x_1)\), where \(x_2\ne x_1\). Equal input changes give equal output changes. In **slope-intercept form**, \(y=mx+b\), \(b\) is the output at input zero. Rearranging the slope formula gives **point-slope form**, \(y-y_1=m(x-x_1)\), useful when a point and slope are known.

**Worked example.** For the outline's \(y=2x-3\), slope is 2 and the \(y\)-intercept is \((0,-3)\). Setting \(y=0\) gives the \(x\)-intercept \((3/2,0)\). Starting at \((0,-3)\), moving right 1 and up 2 gives \((1,-1)\); draw the line through those points. Conversely, points \((1,-1)\) and \((3,3)\) give slope \((3-(-1))/(3-1)=2\), so \(y+1=2(x-1)\), equivalent to \(y=2x-3\). Its domain and range are both all real numbers unless context restricts them.

Horizontal lines \(y=c\) have slope zero and range \(\{c\}\). Vertical lines \(x=c\) have undefined slope because \(\Delta x=0\); they are not functions of \(x\). Distinct nonvertical parallel lines have equal slopes. Nonvertical perpendicular lines have slopes with product \(-1\): a direction \((1,m)\) rotated a quarter-turn becomes \((-m,1)\), with slope \(-1/m\). Horizontal and vertical lines form the separate perpendicular case.

**Avoid this misconception:** slope is a ratio of changes, not \(y/x\) unless the line passes through the origin.

**Practice L2.** (a) Find the equation through \((2,5)\) and \((4,9)\). (b) Find the slope perpendicular to a line of slope \(-3\).

### Lesson 3: Systems by graphing, substitution, and elimination

A **system** requires all its equations to hold at once. A solution pair is an intersection of their graphs. Substitution replaces a quantity by an equal expression. Elimination adds equations, possibly after nonzero scaling, to cancel a variable; this preserves the simultaneous solutions.

**Worked example.** Solve \(y=2x+1\) and \(x+y=7\). Substitute the first expression for \(y\): \(x+2x+1=7\), giving \(x=2,y=5\). By elimination, write \(-2x+y=1\) and \(x+y=7\); subtract the first from the second to obtain \(3x=6\), then \(y=5\). Both lines intersect at \((2,5)\), and substitution in both equations checks the result.

Two distinct parallel lines have no common point; equivalent line equations have infinitely many common points. For example, \(y=2x+1\) and \(y=2x+3\) have no solution, while \(2y=4x+2\) describes the same line as the first equation. Graphing estimates intersections; algebra gives exact values.

**Avoid this misconception:** a pair must satisfy both original equations, not just the one used to calculate the second coordinate.

**Practice L3.** (a) Solve \(x+y=5\), \(x-y=1\). (b) Classify the system \(y=3x-2\), \(2y=6x-4\).

### Lesson 4: Systems of inequalities

A linear inequality in two variables describes a half-plane. Draw its boundary line, solid for \(\le\) or \(\ge\), dashed for \(<\) or \(>\). Test a point off the boundary to determine which side to shade. A system's **feasible region** is the overlap, because every condition must hold.

**Worked example.** For \(x\ge0,y\ge0,x+y\le6\), draw solid axes and the solid line through \((6,0)\) and \((0,6)\). The point \((0,0)\) satisfies \(x+y\le6\), so shade its side of that line, within the first quadrant. The overlap is a triangle including its edges. \((2,3)\) is feasible; \((4,4)\) is not. If \(x,y\) count objects, only whole-number points in this region are allowed.

**Avoid this misconception:** shading each condition separately is unfinished; the answer is their overlap.

**Practice L4.** Describe the feasible region of \(y> x\), \(y\le4\). Is \((2,3)\) included? Is \((4,4)\)?

## 3. Connected application

For the event, let \(n\) be attendance, \(C(n)=120+3n\) cost in dollars, and \(R(n)=8n\) revenue in dollars. Their slopes are $3 and $8 per attendee; the intercepts are $120 and $0.

| Attendance \(n\) | Cost \(C(n)\) | Revenue \(R(n)\) |
|---|---|---|
| 0 | $120 | $0 |
| 20 | $180 | $160 |
| 24 | $192 | $192 |
| 30 | $210 | $240 |

On horizontal attendance and vertical dollar axes, the two straight-line extensions meet at \((24,192)\): solving \(120+3n=8n\) confirms break-even. Now add a new assumption: the venue holds at most 40 attendees. The contextual domain is \(n\in\{0,1,\ldots,40\}\), so actual graphs contain discrete points. Profit \(P(n)=5n-120\) has range \(\{-120,-115,\ldots,80\}\) dollars. The graph makes comparison across attendance counts visible. Constant marginal cost and a fixed ticket price justify linear models; changing either would require revising them.

## 4. Essential summary

A function pairs each domain value with one output. Tables and graphs expose patterns; slope quantifies constant change. Intercepts anchor a line, while point-slope form builds it from data. Systems locate shared pairs, and inequality systems locate shared regions. Context can turn a continuous algebraic line into a finite set of meaningful points.

## 5. Independent mastery check

- **M1.** For \(f(x)=-2x+6\) on \(0\le x\le3\), find \(f(1)\), domain, range, and both intercepts.
- **M2.** A line passes through \((-1,4)\) and \((2,10)\). Find its slope and equation.
- **M3.** Explain why \(x=4\) is a line but is not a function of \(x\). Give a perpendicular line.
- **M4.** Error analysis: someone finds slope between \((1,2)\) and \((3,6)\) as \((3-1)/(6-2)=1/2\). Correct and explain.
- **M5.** Solve \(2x+y=9\), \(x-y=3\), and interpret graphically.
- **M6.** Describe the boundaries and shading for \(x\ge0,y\ge0,x+y<5\). Is \((2,3)\) included?
- **M7.** An unfamiliar tank contains 90 L and drains at 6 L/min. Write a linear model, interpret both parameters, and give its physical domain through emptying.
- **M8.** With the event's 40-person capacity, which attendance counts produce at least $50 profit?

**Mastery criteria:** at least 7 of 8 correct, with accurate graph descriptions and units. Revisit Lesson 1 for domains/function tests, Lesson 2 for rates and intercepts, Lesson 3 for simultaneous equations, or Lesson 4 for boundaries. Recheck M8 against [Stage 3](stage3_equations_and_inequalities.md) if needed.

## 6. Answers and feedback

**Prerequisites**

- **P1.** 24.
- **P2.** \(-3,1\).
- **P3.** \(y=3\).

**Practice**

- **L1.** (a) yes; domain \(\{-1,0,2\}\), range \(\{3,5\}\); (b) \(-5\).
- **L2.** (a) slope 2, \(y-5=2(x-2)\), or \(y=2x+1\); (b) \(1/3\).
- **L3.** (a) \((3,2)\), by adding equations; (b) infinitely many solutions, the same line.
- **L4.** above dashed \(y=x\) and on/below solid \(y=4\); \((2,3)\) yes, \((4,4)\) no.

**Mastery**

- **M1.** 4; domain \([0,3]\), range \([0,6]\); \(y\)-intercept \((0,6)\), \(x\)-intercept \((3,0)\).
- **M2.** slope 2; \(y=2x+6\).
- **M3.** input 4 has many outputs; any horizontal line, such as \(y=0\), is perpendicular.
- **M4.** \((6-2)/(3-1)=2\), vertical change divided by horizontal change.
- **M5.** \((4,1)\), the unique intersection.
- **M6.** solid axes, dashed line through \((5,0),(0,5)\); shade the first-quadrant side containing the origin; \((2,3)\) is excluded because the sum equals 5.
- **M7.** \(V(t)=90-6t\) L, \(t\) in minutes; 90 L initially, change \(-6\) L/min; \(0\le t\le15\).
- **M8.** \(n=34,35,\ldots,40\); intersect \(n\ge34\) with the whole-number capacity restriction.

## 7. Bridge to the next stage

The garden's area \(x(x+3)\) is not linear: both dimensions change. [Stage 5: Polynomials and Factoring](stage5_polynomials_and_factoring.md) develops the multiplication and factor structure needed to understand such expressions.
