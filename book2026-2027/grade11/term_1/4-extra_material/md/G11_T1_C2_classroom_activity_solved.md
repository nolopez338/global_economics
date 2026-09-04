# Grade 11 — Term 1 — Practice Activity with Solutions

## Problem Descriptions

### Line through two points

For \(x_1\ne x_2\),

\[
m=\frac{y_2-y_1}{x_2-x_1},
\qquad
b=y_1-mx_1,
\qquad
y=mx+b.
\]

### 1. Waiting for TransMilenio after class

On weekday evenings, a university student leaves class and waits at a TransMilenio station near the Universidad Nacional. The wait always lasts between 2 and 10 minutes, and every waiting time in that span is equally plausible.

Determine the complete probability density rule for the waiting time, including what happens outside the stated span. Then find the chance that the student waits longer than 7 minutes and the chance that the wait lasts from 3 through 7 minutes.

### 2. An evening commute across Bogotá

A young apprentice travels by SITP from Kennedy to a training programme in Chapinero during the evening rush. Traffic can add anywhere from no delay to 8 minutes to the usual journey. A delay of any length in that span is possible, and longer delays become steadily more common. An 8-minute delay is 5 times as common as no delay.

Determine the complete probability density rule for the added travel time, including what happens outside the stated span. Then find the chance of more than 6 minutes of added time and the chance of between 2 and 6 minutes of added time.

### 3. Weekly study at a public library

Members of a Bogotá youth scholarship programme record the time they study each week at the Biblioteca Pública Virgilio Barco. Weekly totals range from 2 to 10 hours. Totals become steadily more common from 2 hours up to a most common total of 5 hours, then steadily less common through 10 hours; there are no totals right at either limit.

Determine the complete probability density rule for weekly study time, including what happens outside the stated span. Then find the chance of studying for more than 7 hours and the chance of studying from 4 through 8 hours.

### 4. A Sunday on the Ciclovía

A group of young adults tracks how long its members spend cycling and meeting friends on Bogotá's Sunday Ciclovía. A recorded visit can last from 0 to 5 hours. All durations up to 2 hours are equally common. All durations from 2 to 5 hours are also equally common, but they occur 2 times as often as durations in the shorter band.

Determine the complete probability density rule for the visit length, including what happens outside the stated span. Then find the chance that a visit lasts more than 4 hours and the chance that it lasts from 1 through 4 hours.

### 5. Time at a youth entrepreneurship fair

Young adults attend a Bogotá entrepreneurship fair at Corferias for up to 6 hours. Immediate departures are not observed. Departures become steadily more common during the first 2 hours, remain equally common at their highest level from 2 through 4 hours, and then become steadily less common until 6 hours, when none are observed.

Determine the complete probability density rule for the length of a visit, including what happens outside the stated span. Then find the chance of staying longer than 5 hours and the chance of staying from 1 through 5 hours.

---

# Solutions

## Problem 1 — Uniform distribution

### 1.1 Support and Shape

The random variable \(T\) has support \([2,10]\). The context says that all waiting times in this interval are equally plausible, so the density is a rectangle of unknown height \(h\) and is zero outside the support.

### 1.2 Total Area = 1

The rectangle must have area \(1\):

\[
1=(10-2)h=8h,
\qquad
h=\frac18.
\]

### 1.3 Straight Line Rule

The only segment is horizontal. Thus \(m=0\), and its constant rule on the support is

\[
f_T(t)=\frac18.
\]

No nontrivial line calculation is needed.

### 1.4 Complete PDF

\[
f_T(t)=
\begin{cases}
\dfrac18, & 2\le t\le10,\\[1mm]
0, & \text{otherwise.}
\end{cases}
\]

### 1.5 Tail Probability

The relevant right-tail region is a rectangle:

\[
P(T>7)
=(10-7)\frac18
=\frac38
=37.5\%.
\]

### 1.6 Interval Probability

This interval is obtained directly as a rectangle:

\[
P(3\le T\le7)
=(7-3)\frac18
=\frac12.
\]

---

## Problem 2 — Linear distribution

### 2.1 Support and Shape

The random variable \(X\) has support \([0,8]\). The context supplies a steadily increasing straight line whose height at \(8\) is five times its height at \(0\).

Write the endpoint heights as \(h\) and \(5h\). The density is zero outside the support.

### 2.2 Total Area = 1

The trapezoid must have area \(1\):

\[
1=\frac12(8)(h+5h)
=24h.
\]

Therefore,

\[
h=\frac1{24},
\qquad
5h=\frac5{24}.
\]

### 2.3 Straight Line Rule

Use the points

\[
(x_1,y_1)=\left(0,\frac1{24}\right)
\]

and

\[
(x_2,y_2)=\left(8,\frac5{24}\right).
\]

The slope is

\[
m=
\frac{y_2-y_1}{x_2-x_1}
=
\frac{\frac5{24}-\frac1{24}}{8-0}
=
\frac1{48}.
\]

The intercept is

\[
b
=
y_1-mx_1
=
\frac1{24}-\frac1{48}(0)
=
\frac1{24}.
\]

Therefore,

\[
f_X(x)
=
\frac{x}{48}+\frac1{24}
=
\frac{x+2}{48}.
\]

### 2.4 Complete PDF

\[
f_X(x)=
\begin{cases}
\dfrac{x+2}{48}, & 0\le x\le8,\\[1mm]
0, & \text{otherwise.}
\end{cases}
\]

### 2.5 Tail Probability

Since

\[
f_X(6)=\frac16
\]

and

\[
f_X(8)=\frac5{24},
\]

the right-tail region is a width-\(2\) trapezoid:

\[
P(X>6)
=
\frac12(8-6)
\left(
\frac16+\frac5{24}
\right)
=
\frac38.
\]

### 2.6 Interval Probability

This is obtained directly from the trapezoid between \(2\) and \(6\).

Since

\[
f_X(2)=\frac1{12}
\]

and

\[
f_X(6)=\frac16,
\]

we have

\[
P(2\le X\le6)
=
\frac12(6-2)
\left(
\frac1{12}+\frac16
\right)
=
\frac12.
\]

---

## Problem 3 — Triangular distribution

### 3.1 Support and Shape

The random variable \(Q\) has support \([2,10]\). The context supplies zero height at both endpoints, a steady rise to the most common value at \(q=5\), and a steady fall thereafter.

Denote the unknown peak height by \(H\). The density is zero outside the support.

### 3.2 Total Area = 1

The triangle must have area \(1\):

\[
1
=
\frac12(10-2)H
=
4H.
\]

Therefore,

\[
H=\frac14.
\]

### 3.3 Straight Line Rule

For the rising segment, use

\[
(2,0)
\]

and

\[
\left(5,\frac14\right).
\]

Then

\[
m_1
=
\frac{\frac14-0}{5-2}
=
\frac1{12},
\]

and

\[
b_1
=
y_1-m_1x_1
=
0-\frac1{12}(2)
=
-\frac16.
\]

Therefore,

\[
y
=
m_1q+b_1
=
\frac{q-2}{12}.
\]

For the falling segment, use

\[
\left(5,\frac14\right)
\]

and

\[
(10,0).
\]

Then

\[
m_2
=
\frac{0-\frac14}{10-5}
=
-\frac1{20},
\]

and

\[
b_2
=
y_1-m_2x_1
=
\frac14-\left(-\frac1{20}\right)5
=
\frac12.
\]

Therefore,

\[
y
=
m_2q+b_2
=
\frac{10-q}{20}.
\]

The adjacent rules agree at \(q=5\):

\[
\frac{5-2}{12}
=
\frac14
\]

and

\[
\frac{10-5}{20}
=
\frac14.
\]

### 3.4 Complete PDF

\[
f_Q(q)=
\begin{cases}
\dfrac{q-2}{12}, & 2\le q\le5,\\[1mm]
\dfrac{10-q}{20}, & 5<q\le10,\\[1mm]
0, & \text{otherwise.}
\end{cases}
\]

As checked above, the pieces are continuous at \(q=5\).

### 3.5 Tail Probability

Since

\[
f_Q(7)=\frac3{20},
\]

the right-tail region is a triangle:

\[
P(Q>7)
=
\frac12(10-7)\frac3{20}
=
\frac9{40}
=
22.5\%.
\]

### 3.6 Interval Probability

Use the complement of the two outside tail triangles.

Since

\[
f_Q(4)=\frac16
\]

and

\[
f_Q(8)=\frac1{10},
\]

we obtain

\[
\begin{aligned}
P(4\le Q\le8)
&=
1
-\frac12(4-2)\frac16
-\frac12(10-8)\frac1{10}\\
&=
\frac{11}{15}
\approx73.3\%.
\end{aligned}
\]

---

## Problem 4 — Piecewise-uniform distribution

### 4.1 Support and Shape

The random variable \(W\) has support \([0,5]\), with breakpoint \(2\).

The context supplies a constant height \(k\) on \([0,2)\) and twice that height, \(2k\), on \([2,5]\). The density is zero outside the support.

### 4.2 Total Area = 1

The two rectangles must have total area \(1\):

\[
1
=
2k+(5-2)(2k)
=
8k.
\]

Therefore,

\[
k=\frac18,
\qquad
2k=\frac14.
\]

### 4.3 Straight Line Rule

Both segments are horizontal, so each has

\[
m=0.
\]

No nontrivial line calculation is needed.

The constant rules are

\[
f_W(w)=\frac18
\]

on \([0,2)\), and

\[
f_W(w)=\frac14
\]

on \([2,5]\).

### 4.4 Complete PDF

\[
f_W(w)=
\begin{cases}
\dfrac18, & 0\le w<2,\\[1mm]
\dfrac14, & 2\le w\le5,\\[1mm]
0, & \text{otherwise.}
\end{cases}
\]

### 4.5 Tail Probability

The right-tail region is a width-\(1\), height-\(\frac14\) rectangle:

\[
P(W>4)
=
(5-4)\frac14
=
\frac14.
\]

### 4.6 Interval Probability

Split the interval at the breakpoint \(2\) and add the two rectangles:

\[
\begin{aligned}
P(1\le W\le4)
&=
(2-1)\frac18
+
(4-2)\frac14\\
&=
\frac18+\frac12\\
&=
\frac58.
\end{aligned}
\]

---

## Problem 5 — Piecewise-linear distribution

### 5.1 Support and Shape

The random variable \(D\) has support \([0,6]\).

The context supplies a steady rise from zero to an unknown height \(H\) at \(d=2\), that same constant height through \(d=4\), and a steady fall to zero at \(d=6\).

Thus, the symbolic vertices are

\[
(0,0),\quad(2,H),\quad(4,H),\quad(6,0),
\]

and the density is zero outside the support.

### 5.2 Total Area = 1

The two triangles and middle rectangle must have total area \(1\):

\[
1
=
\frac12(2)H
+
(4-2)H
+
\frac12(6-4)H.
\]

Therefore,

\[
1=4H,
\qquad
H=\frac14.
\]

### 5.3 Straight Line Rule

For the first segment, use

\[
(0,0)
\]

and

\[
\left(2,\frac14\right).
\]

Then

\[
m_1
=
\frac{\frac14-0}{2-0}
=
\frac18,
\]

and

\[
b_1
=
y_1-m_1x_1
=
0-\frac18(0)
=
0.
\]

Therefore,

\[
y=m_1d+b_1=\frac d8.
\]

For the horizontal segment, use

\[
\left(2,\frac14\right)
\]

and

\[
\left(4,\frac14\right).
\]

Then

\[
m_2
=
\frac{\frac14-\frac14}{4-2}
=
0,
\]

and

\[
b_2
=
y_1-m_2x_1
=
\frac14-0(2)
=
\frac14.
\]

Therefore,

\[
y=m_2d+b_2=\frac14.
\]

For the last segment, use

\[
\left(4,\frac14\right)
\]

and

\[
(6,0).
\]

Then

\[
m_3
=
\frac{0-\frac14}{6-4}
=
-\frac18,
\]

and

\[
b_3
=
y_1-m_3x_1
=
\frac14-\left(-\frac18\right)4
=
\frac34.
\]

Therefore,

\[
y=m_3d+b_3
=
\frac{6-d}{8}.
\]

At \(d=2\), the first two rules both give \(\frac14\), and at \(d=4\), the last two rules both give \(\frac14\).

### 5.4 Complete PDF

\[
f_D(d)=
\begin{cases}
\dfrac d8, & 0\le d\le2,\\[1mm]
\dfrac14, & 2<d\le4,\\[1mm]
\dfrac{6-d}{8}, & 4<d\le6,\\[1mm]
0, & \text{otherwise.}
\end{cases}
\]

The breakpoint checks above verify continuity.

### 5.5 Tail Probability

Since

\[
f_D(5)=\frac18,
\]

the right-tail region is a triangle:

\[
P(D>5)
=
\frac12(6-5)\frac18
=
\frac1{16}
=
6.25\%.
\]

### 5.6 Interval Probability

Use the complement of the two congruent outside tail triangles:

\[
\begin{aligned}
P(1\le D\le5)
&=
1
-\frac12(1)\frac18
-\frac12(1)\frac18\\
&=
\frac78
=
87.5\%.
\end{aligned}
\]