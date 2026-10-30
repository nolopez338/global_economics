from pathlib import Path
p=Path('book2026-2027/grade10/term_1/1-practice_activities/G10_T1_L1_C1C3_practice_activity-alternate-descriptions.tex')
s=p.read_text(encoding='utf-8')
a=s.index('\\subsubsection*{Theory:'); b=s.index('\\subsection{Introductory General')
s=s[:a]+r'''\subsection{From a decision situation to a profit table}
\label{subsec:intro-first-steps}

\subsubsection*{Start with the situation}
A school enterprise organises services for community events. Before bookings
are confirmed, its students must choose either a basic service plan or an
expanded service plan with more equipment and capacity. Demand may turn out
to be high or low. The enterprise chooses its plan first; demand is revealed
later. This timing makes the decision uncertain.

The uncertain process is customers making bookings. High demand and low
demand are the two possible \textbf{states} of that process in this model.
The students control the service plan, but they cannot choose the demand state.
A consequence can first be described in words: ``the basic plan operates under
high demand, earns sales income, and uses staff and supplies.'' We then assign
a monetary payoff to that consequence. Here the payoff will be the profit
remaining after costs. Describing what happens and measuring its financial
result are related, but different, tasks.

\subsubsection*{Name the choices, then the states}
The basic and expanded plans are the \textbf{alternatives}: the available
choices. We now shorten their names to \(A_1\), read ``alternative one,''
and \(A_2\), read ``alternative two.''
\begin{center}
\begin{tabular}{@{}ll@{}}
\toprule Symbol & Choice made by the enterprise \\ \midrule
\(A_1\) & Choose the basic service plan. \\
\(A_2\) & Choose the expanded service plan. \\
\bottomrule
\end{tabular}
\end{center}
High and low demand are possible outcomes outside the enterprise's control.
We label them \(S_1\), read ``state one,'' and \(S_2\), read ``state two.''
\begin{center}
\begin{tabular}{@{}ll@{}}
\toprule Symbol & Demand outcome revealed after the choice \\ \midrule
\(S_1\) & High demand. \\
\(S_2\) & Low demand. \\
\bottomrule
\end{tabular}
\end{center}
The small numbers below the letters are \textbf{subscripts}. They identify
choices and states; they do not rank them or give their monetary values.

\textbf{Check.} Can the enterprise choose \(S_1\)?
\textit{Suggested answer:} No. It chooses a plan; customers' bookings determine
which demand state occurs.

\subsubsection*{Match one choice with one state}
To describe a possible result, name both the chosen plan and the demand
outcome. The pair \((A_1,S_1)\), read ``alternative one with state one,''
means the basic plan under high demand. There are four combinations:
\begin{center}
\begin{tabular}{@{}ll@{}}
\toprule Pair & Contextual meaning \\ \midrule
\((A_1,S_1)\) & Basic plan, high demand. \\
\((A_1,S_2)\) & Basic plan, low demand. \\
\((A_2,S_1)\) & Expanded plan, high demand. \\
\((A_2,S_2)\) & Expanded plan, low demand. \\
\bottomrule
\end{tabular}
\end{center}
Only one pair will be realised for this particular decision. We analyse all
four beforehand so that the financial consequence of each possible
choice--state combination is recorded.

\subsubsection*{Give the consequence a monetary value}
\textbf{Revenue} is money earned from the activity. \textbf{Cost} is money
spent or resources charged to the activity. \textbf{Profit} is revenue minus
cost. Suppose the basic plan under high demand earns 20 thousand USD and
costs 9 thousand USD. Its profit is \(20-9=11\) thousand USD.
One thousand USD means 1,000 US dollars. Throughout these introductory
examples, monetary totals are in thousand USD. Revenue alone is not the
payoff in this activity: profit is.

We introduce a separate symbol for each total. First,
\[
R(A_1,S_1)=20.
\]
Read this as ``total revenue for alternative one in state one is 20 thousand
USD.'' The capital \(R\) names total revenue; \(A_1\) identifies the basic
plan and \(S_1\) identifies high demand. The parentheses identify the inputs
to this quantity; they do not mean multiplication.

Next, write the corresponding total cost as
\[
C(A_1,S_1)=9.
\]
Read this as ``total cost for alternative one in state one is 9 thousand
USD.'' Capital \(C\) names total cost, with the same two inputs.

Finally, capital \(P\) names profit, which is our payoff:
\[
P(A_1,S_1)=R(A_1,S_1)-C(A_1,S_1)=11.
\]
Read this as ``profit for alternative one in state one equals its revenue
minus its cost: 11 thousand USD.'' All three quantities refer to the
\emph{same} plan and demand state. The result is positive because revenue
exceeds cost. In separate small illustrations, revenue 9 and cost 9 give
zero profit (\(9-9=0\)); revenue 8 and cost 9 give a loss
(\(8-9=-1\) thousand USD).

\subsubsection*{Organise the four profits}
A profit payoff table puts alternatives in rows and states in columns.
For example, take the basic plan's high-demand revenue of 20 and matching
cost of 9, subtract to obtain 11, then put 11 in row \(A_1\), column
\(S_1\). Repeat that process for the other three pairs. The next problem
consolidates this process using directly supplied totals. Its input table
records the data; the paired calculation tables match each symbolic
subtraction to its arithmetic; the clean final table contains profits only.

\textbf{Check.} Could we subtract the cost for \((A_2,S_1)\) from the revenue
for \((A_1,S_1)\)? \textit{Suggested answer:} No. That would mix two plans.
Both amounts in a subtraction must belong to the same alternative--state pair.

''' +s[b:]
# Clarify existing problem context without changing its numerical data or tables.
s=s.replace('A school enterprise must commit to either alternative', 'Use the school service enterprise just described. It must commit to either alternative',1)
s=s.replace('before learning whether demand will be \\(S_1\\) or \\(S_2\\). Its accounting', 'before learning whether demand will be high (\\(S_1\\)) or low (\\(S_2\\)). Its accounting',1)
s=s.replace('{\\(A_1\\); \\(A_2\\)}\n\t{\\(S_1\\); \\(S_2\\)}\n\t{Demand revealed after the enterprise choice}\n\t{Profit in thousand USD for each alternative--state pair}', '{Basic service plan; Expanded service plan}\n\t{High demand; Low demand}\n\t{Customer bookings reveal demand after the enterprise chooses its plan}\n\t{Services are delivered with sales income and resource use; profit measures the monetary consequence in thousand USD}',1)
a=s.index('\t\\subsection{Advanced General Problem')
components=r'''\subsection{Build totals from quantities, rates, and fixed amounts}
\label{subsec:intro-components}

\subsubsection*{Generalise a familiar calculation}
The first problem has two choices and two states. To refer to any one of
them without writing a separate rule for every cell, use \(A_i\), read
``alternative i,'' and \(S_j\), read ``state j.'' The letters \(i\) and
\(j\) are \textbf{indices}: they tell us which alternative and which state
to use. For example, substituting \(i=2\) and \(j=1\) gives \(A_2\),
\(S_1\), and the expanded-plan, high-demand pair \((A_2,S_1)\).
In the first problem, \(R(A_2,S_1)=18\), \(C(A_2,S_1)=10\), and
\(P(A_2,S_1)=18-10=8\) thousand USD. The indices 2 and 1 are identifiers;
the number 8 is a monetary value. The number of alternatives is a count,
not an index or a profit. Later problems may have more choices or states.

The relationship already used in every cell can now be written generally:
\[
P(A_i,S_j)=R(A_i,S_j)-C(A_i,S_j).
\]
This says ``profit for a chosen alternative and a particular state is the
revenue for that pair minus the cost for that same pair.''

\subsubsection*{Why build revenue and cost?}
A \textbf{direct model}, such as the first problem, supplies total revenue
and total cost. Use those totals as given; we cannot infer a unique set of
prices, quantities, or fixed payments from them. A \textbf{component model}
instead supplies ingredients: quantities, rates per unit, and fixed amounts.
We must use those ingredients to build total revenue and total cost
\emph{independently}, then subtract.

We now study a new version of the same school service enterprise. Its plans
and demand labels keep their meanings, but its financial arrangements will
be stated component by component. These are new assumptions, not a
breakdown of the first problem's directly supplied totals. Each extension
below explicitly adds an arrangement to this new version.

\subsubsection*{Quantity: how much service is completed?}
Suppose the basic plan completes two service batches under high demand and
one under low demand. A \textbf{service batch} is one package of work for an
event; it is the quantity unit throughout this running example. The expanded
plan can complete three batches under high demand and two under low demand.
Write \(q(A_1,S_1)=2\) batches, read ``quantity for alternative one in state
one is two batches.'' More generally, \(q(A_i,S_j)\) means the quantity for
the named pair.
\begin{center}
\begin{tabular}{@{}lcc@{}}
\toprule Quantity (service batches) & \(S_1\): high demand & \(S_2\): low demand \\ \midrule
\(A_1\): basic plan & 2 & 1 \\
\(A_2\): expanded plan & 3 & 2 \\
\bottomrule
\end{tabular}
\end{center}
Demand affects bookings, while the chosen plan affects capacity, so quantity
can depend on both inputs. A quantity of 2 batches is not 2 thousand USD.

\subsubsection*{A revenue rate determined by the plan}
Assume initially that the only revenue is payment for each completed batch.
The basic plan earns 10 thousand USD per batch; the expanded plan earns 11
thousand USD per batch for its larger service package. These are earning
\textbf{rates}, rather than total amounts. Write \(r(A_1)=10\) and
\(r(A_2)=11\) thousand USD per batch. Read \(r(A_1)\) as ``revenue rate
for alternative one.'' More generally, \(r(A_i)\) is the rate set by the plan.

Multiply the number of batches by the payment for each batch:
\[
R(A_i,S_j)=q(A_i,S_j)r(A_i).
\]
For the basic plan under high demand, substitute the quantity and rate:
\[
R(A_1,S_1)=\CalcResult{2\times10}{20}\quad\text{(thousand USD).}
\]
The units are batches times thousand USD per batch, giving thousand USD.
The basic plan's rate stays at 10 across its row; under low demand its
revenue is \(1\times10=10\) thousand USD because quantity changes.
Dependence tells us which input determines a component. It does not require
different inputs to have different values: two plans could happen to have
equal rates.

\subsubsection*{A cost rate determined by the plan}
Now add a cost assumption: each basic-plan batch uses 3 thousand USD of
resources, while each expanded-plan batch uses 4 thousand USD. These are
costs \emph{per batch}. Write \(c(A_1)=3\), read ``cost rate for alternative
one,'' and \(c(A_2)=4\), in thousand USD per batch. The general plan-based
cost rate is \(c(A_i)\). If these are the only costs,
\[
C(A_i,S_j)=q(A_i,S_j)c(A_i).
\]
Keep the revenue and cost calculations separate before finding profit:
\[
\begin{aligned}
R(A_1,S_1)&=\CalcResult{2\times10}{20},&
C(A_1,S_1)&=\CalcResult{2\times3}{6},&
P(A_1,S_1)&=\CalcResult{20-6}{14}.
\end{aligned}
\]
All three results are in thousand USD. Lowercase \(r\) and \(c\) name
rates per batch; uppercase \(R\) and \(C\) name monetary totals.

\textbf{Check.} Why is \(20-3\) not the profit for two basic-plan batches?
\textit{Suggested answer:} 20 is total revenue, but 3 is cost per batch.
First find total cost, \(2\times3=6\), then subtract \(20-6=14\).

\subsubsection*{A revenue rate determined by demand}
Consider a separate pricing variation first: suppose payment comes only
from a demand-based rate, with no plan-based payment. A community booking
scheme pays 5 thousand USD per batch under high demand and 3 under low
demand. Write \(r(S_1)=5\) and \(r(S_2)=3\) thousand USD per batch;
read \(r(S_1)\) as ``revenue rate for state one.'' The rate \(r(S_j)\)
is determined by the demand state. For this state-only pricing variation,
\[
R(A_i,S_j)=q(A_i,S_j)r(S_j),\qquad
R(A_1,S_1)=\CalcResult{2\times5}{10}.
\]
The result is in thousand USD. The rate is the same down a state column,
but total revenue need not be: three batches under \(A_2\) earn
\(3\times5=15\) thousand USD in that same state.

Return now to the plan-based pricing version and \emph{extend} it: assume
the booking scheme's payment is an addition to the plan payment, so both
rates apply to each batch. Then
\[
\begin{aligned}
R(A_i,S_j)&=q(A_i,S_j)r(A_i)+q(A_i,S_j)r(S_j)\\
          &=q(A_i,S_j)[r(A_i)+r(S_j)].
\end{aligned}
\]
For the basic plan under high demand, \(2\times10+2\times5=2(10+5)=30\)
thousand USD. Factoring out quantity works because the same two batches
earn both rates. We add 10 and 5 because both use thousand USD per batch;
multiplying the combined rate by two batches gives money.

\subsubsection*{A cost rate determined by demand}
High-demand bookings may use shared deliveries, while low-demand bookings
need separate handling. Suppose handling costs 1 thousand USD per batch in
high demand and 2 in low demand. Write \(c(S_1)=1\) and \(c(S_2)=2\)
thousand USD per batch; read \(c(S_1)\) as ``cost rate for state one.''
The general state-based rate is \(c(S_j)\). In a simple variation where
handling is the only charged cost,
\[
C(A_i,S_j)=q(A_i,S_j)c(S_j),\qquad
C(A_1,S_1)=\CalcResult{2\times1}{2}.
\]
The result is in thousand USD. Now extend the plan-cost version instead:
assume handling is charged \emph{in addition} to the plan's resource cost.
Then
\[
C(A_i,S_j)=q(A_i,S_j)[c(A_i)+c(S_j)],\qquad
C(A_1,S_1)=\CalcResult{2(3+1)}{8}.
\]
The handling rate stays at 1 down the high-demand column, but its total
charge changes from \(2\times1=2\) to \(3\times1=3\) thousand USD as
quantity changes. A state-based component does not make the entire total
state-only when quantity also depends on the alternative.

\textbf{Check.} Under the version with both revenue rates and both cost
rates, what is the basic plan's high-demand profit?
\textit{Suggested answer:} Revenue is 30, cost is 8, and profit is
\(30-8=22\) thousand USD. Equal state rates across plans do not imply equal totals.

\subsubsection*{Fixed revenue: first a plan payment, then a state payment}
Extend the version with both revenue rates: a sponsor now pays 7 thousand
USD for choosing the basic plan, or 9 for choosing the expanded plan,
regardless of how many batches are completed. We write \(f_r(A_1)=7\) and
\(f_r(A_2)=9\) thousand USD. Read \(f_r(A_1)\) as ``fixed revenue for
alternative one.'' The letter \(f\) indicates a fixed amount; the subscript
\(r\) identifies it as revenue. The plan determines \(f_r(A_i)\).
For the basic plan under high demand, revenue becomes
\[
R(A_1,S_1)=\CalcResult{2(10+5)+7}{37}\quad\text{(thousand USD).}
\]
The 7 is added once; it is not a payment for each batch.

Add one more assumption: a community grant pays 6 thousand USD if demand
is high and 7 if it is low, independently of the number of batches served.
Write \(f_r(S_1)=6\) and \(f_r(S_2)=7\) thousand USD. Read \(f_r(S_1)\)
as ``fixed revenue for state one.'' The state determines \(f_r(S_j)\).
The high-demand grant alone contributes 6 thousand USD, whether the plan
serves two or three batches. With both fixed payments now included,
\[
R(A_1,S_1)=\CalcResult{2(10+5)+7+6}{43}\quad\text{(thousand USD).}
\]
``Fixed'' means independent of quantity within the model. A fixed amount
can still differ between plans or states. For a compact \emph{fixed-only}
variation, suppose there are no per-batch earnings, only the sponsor and
grant. Then \(R(A_i,S_j)=f_r(A_i)+f_r(S_j)\), and
\(R(A_1,S_1)=7+6=13\) thousand USD; no quantity is needed.

\subsubsection*{Fixed cost: first setup, then administration}
Return to the version with both per-batch cost rates. Extend it by charging
setup once: 8 thousand USD for the basic plan and 10 for the expanded plan.
Write \(f_c(A_1)=8\) and \(f_c(A_2)=10\) thousand USD. Read \(f_c(A_1)\)
as ``fixed cost for alternative one.'' The subscript \(c\) identifies cost;
the plan determines \(f_c(A_i)\). For the basic plan under high demand,
\[
C(A_1,S_1)=\CalcResult{2(3+1)+8}{16}\quad\text{(thousand USD).}
\]
Now add a state-specific administration bill: 5 thousand USD under high
demand or 3 under low demand, charged once whichever plan is chosen.
Write \(f_c(S_1)=5\) and \(f_c(S_2)=3\) thousand USD. Read \(f_c(S_1)\)
as ``fixed cost for state one.'' The state determines \(f_c(S_j)\).
The high-demand bill contributes 5 thousand USD, not \(2\times5\).
With setup and administration included,
\[
C(A_1,S_1)=\CalcResult{2(3+1)+8+5}{21}\quad\text{(thousand USD).}
\]
Ordinary positive costs are added \emph{inside total cost}. Total cost is
then subtracted once from revenue: \(43-21=22\) thousand USD. Making every
cost negative and then subtracting it would reverse its effect.

\textbf{Check.} If the basic plan completes one batch instead of two, does
its setup charge become 4? \textit{Suggested answer:} No. Setup remains
8 thousand USD; only the per-batch charges change with quantity.

\subsubsection*{Assemble the complete models}
We have now taught every ingredient. When \emph{all} the arrangements just
introduced apply together, their complete models are
\[
\begin{aligned}
R(A_i,S_j)&=q(A_i,S_j)[r(A_i)+r(S_j)]+f_r(A_i)+f_r(S_j),\\
C(A_i,S_j)&=q(A_i,S_j)[c(A_i)+c(S_j)]+f_c(A_i)+f_c(S_j),\\
P(A_i,S_j)&=R(A_i,S_j)-C(A_i,S_j).
\end{aligned}
\]
The four additive revenue components are \(q(A_i,S_j)r(A_i)\),
\(q(A_i,S_j)r(S_j)\), \(f_r(A_i)\), and \(f_r(S_j)\).
The four additive cost components are \(q(A_i,S_j)c(A_i)\),
\(q(A_i,S_j)c(S_j)\), \(f_c(A_i)\), and \(f_c(S_j)\).
Each is a monetary amount. Quantity \(q(A_i,S_j)\) is a multiplier,
not an extra monetary component.

The later sections count components \emph{within} the revenue and cost
models. A one-component example can have one revenue component and one
cost component. The two models need not use matching types. For example,
if the stated arrangements provide only plan-based per-batch revenue and
state-based handling cost, then
\[
R(A_i,S_j)=q(A_i,S_j)r(A_i),\qquad
C(A_i,S_j)=q(A_i,S_j)c(S_j).
\]
If instead there is only a plan sponsorship payment and a state
administration bill, the fixed-only models are
\[
R(A_i,S_j)=f_r(A_i),\qquad C(A_i,S_j)=f_c(S_j).
\]
A two-component version might add a fixed plan payment to per-batch plan
revenue; a three-component version could add a fixed state grant as well.
Use only components included by the stated arrangements. An excluded
component can be treated as zero. A necessary input that is merely missing
is unknown, not automatically zero.

\subsubsection*{Keep the meaning of a signed adjustment}
Some financial descriptions may explicitly give a reduction. For example,
a 2 thousand USD rebate on a 9 thousand USD bill gives total cost
\(9+(-2)=7\), whereas an additional charge of 2 gives \(9+2=11\).
A reduction and a further cost have opposite effects. If a stated model
actually gives a negative total cost, subtract it with parentheses:
revenue 5 and total cost \(-2\) give profit \(5-(-2)=7\) thousand USD.
These signed cases do not change the basic rule: build the stated totals,
then subtract cost once.

The Advanced General Problem now brings the familiar steps together. Its
community business is a variation of our service enterprise: it uses the
same component values, with one completed service batch counted as one
``unit.'' Its input table connects every quantity, rate, and fixed amount
to the notation above. Rates are in thousand USD per unit, while fixed
amounts and totals are in thousand USD.

'''
s=s[:a]+components+s[a:]
# Correct surrounding unit explanation (input values and calculation tables untouched).
s=s.replace('All revenue rates, cost rates, fixed amounts, and profits are measured in thousand USD, with each variable rate applying to every unit completed.', 'Each completed service batch counts as one unit. Revenue and cost rates are in thousand USD per unit; fixed amounts and profits are in thousand USD. Each variable rate applies to every unit completed.',1)
# Add capstone walkthrough immediately before existing navigation after its model.
a=s.index('\t\\subsection{Advanced General Problem'); b=s.index('\t\\secInicio[sec:problem2-advanced-general-c1-c3][sec:introduction]',a)
s=s[:b]+r'''\textbf{Trace one cell before completing the tables.} For \((A_1,S_1)\),
use quantity 2, revenue rates 10 and 5, and fixed revenue 7 and 6:
\[
R(A_1,S_1)=\CalcResult{2(10+5)+7+6}{43}.
\]
Independently, use cost rates 3 and 1 and fixed costs 8 and 5:
\[
C(A_1,S_1)=\CalcResult{2(3+1)+8+5}{21}.
\]
Finally, \(P(A_1,S_1)=43-21=22\) thousand USD. This is the entry in row
\(A_1\), column \(S_1\) of the final profit table. Apply these same three
steps to each remaining pair; do not mix a rate or payment from another
plan or state. The following paired tables show revenue first, cost second,
and profit third.

''' +s[b:]
a=s.index('\t\\section{Direct Revenue and Cost Models}')
ending=r'''\subsection{Reference and classroom solving routine}
\label{subsec:intro-reference}

\textbf{Notation already used.} Monetary units below are thousand USD;
``per unit'' refers to the quantity unit stated in the problem.
\begin{longtable}{@{}p{0.30\linewidth}p{0.64\linewidth}@{}}
\toprule Symbol & Meaning and units \\ \midrule
\endhead
\(A_i\), \(S_j\) & Alternative and state labels; \(i\) and \(j\) are indices, not money or ranks. \\
\(q(A_i,S_j)\) & Quantity for that pair, in batches or another stated quantity unit. \\
\(r(A_i)\), \(r(S_j)\) & Revenue rates determined by the plan or the state, in thousand USD per unit. \\
\(c(A_i)\), \(c(S_j)\) & Cost rates determined by the plan or the state, in thousand USD per unit. \\
\(f_r(A_i)\), \(f_r(S_j)\) & Fixed revenue determined by the plan or the state, in thousand USD; add once. \\
\(f_c(A_i)\), \(f_c(S_j)\) & Fixed cost determined by the plan or the state, in thousand USD; add once inside cost. \\
\(R(A_i,S_j)\) & Total revenue for the pair, in thousand USD. \\
\(C(A_i,S_j)\) & Total cost for the pair, in thousand USD. \\
\(P(A_i,S_j)\) & Profit/payoff for the pair: revenue minus cost, in thousand USD. \\
\bottomrule
\end{longtable}

\textbf{Practical solving procedure.}
\begin{enumerate}
\item Identify who chooses, the alternatives, the uncertain process, its
possible states, the timing, and the consequences in their economic context (C1).
\item Map each choice and state to a symbol. List every alternative--state
pair so none is missed.
\item Record inputs in a \emph{Symbol | Value | Meaning in this problem}
table. Include units and distinguish direct totals, quantities, rates, and
fixed amounts. Check that every necessary input is supplied.
\item Calculate revenue for each pair using its stated model, or record the
directly supplied revenue total. Keep quantity and rate units compatible.
\item Calculate cost separately for the same pair, or record the supplied
cost total. Add each applicable fixed amount once.
\item Subtract total cost from total revenue (C3). For substantial worked
examples, match symbolic and numerical tables side by side: revenue first
and cost second when calculation is needed, then profit. Put the complete
arithmetic on one line in each numerical cell and its result below.
\item Construct the clean profit payoff table (C3): alternatives in rows,
states in columns, profits only in the cells, and monetary units stated.
Keep row and column order consistent across all tables.
\end{enumerate}

\textbf{Final checks with suggested answers.}
\begin{itemize}
\item Is 10 thousand USD per batch a total revenue? \textit{No: it is a
rate. Two batches earn 20 thousand USD at that rate.}
\item Should a fixed payment of 7 thousand USD become 14 when quantity is
two batches? \textit{No: add the fixed payment once. A per-batch payment
would be multiplied by quantity.}
\item If revenue is 43 and cost is 21 thousand USD, which belongs in the
payoff table? \textit{Profit, \(43-21=22\) thousand USD, rather than revenue 43.}
\end{itemize}

\secInicio[sec:introduction][toc]
\clearpage

'''
s=s[:a]+ending+s[a:]
s=s.replace('\\SectionProblemLink{sec:problem1-introductory-general-c1-c3}{Introductory General Problem (C1--C3)}', '\\SectionProblemLink{subsec:intro-first-steps}{From a decision situation to a profit table} \\\\\n\t\t\\SectionProblemLink{sec:problem1-introductory-general-c1-c3}{Introductory General Problem (C1--C3)}',1)
s=s.replace('\\SectionProblemLink{sec:problem2-advanced-general-c1-c3}{Advanced General Problem (C1--C3)}','\\SectionProblemLink{subsec:intro-components}{Build totals from quantities, rates, and fixed amounts} \\\\\n\t\t\\SectionProblemLink{sec:problem2-advanced-general-c1-c3}{Advanced General Problem (C1--C3)} \\\\\n\t\t\\SectionProblemLink{subsec:intro-reference}{Reference and classroom solving routine}',1)
p.write_text(s,encoding='utf-8',newline='\n')
print('Updated Introduction; later practice suffix identical:', s[s.index('\\section{Direct Revenue and Cost Models}'):]==Path('tmp/c1c3-intro-review/before.tex').read_text(encoding='utf-8').split('\\section{Direct Revenue and Cost Models}',1)[1].join(['\\section{Direct Revenue and Cost Models}','']))
