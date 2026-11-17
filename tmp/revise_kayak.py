from pathlib import Path
import re

p = Path('book2026-2027/grade10/term_2/2-class_activities/G10_T2_L1_C2_classroom_activity.tex')
s = p.read_text(encoding='utf-8')
Path('tmp/kayak-before-current.tex').write_text(s, encoding='utf-8')
start = s.index(r'\stageheading{Guided Example}')
end = s.index(r'\stageheading{Independent Practice}', start)
guided = s[start:end]
guided = guided.replace(r'\problemtitle{2}{Kayak returns}', r'\problemtitle{2}{Kayak returns}'+'\n'+r'\begingroup\small', 1)
old = r'''\task{1}{Define $X$, its units and support; write the PMF table and represent it graphically. Show the outcome
  mapping and probability calculations, then verify the PMF. Group all categories that give the same fee.}'''
new = r'''\task{1}{Define $X$, its units and support. Complete the outcome mapping, group categories with the
  same fee in the PMF table, show probability calculations, and draw the PMF graph.}
\textbf{Random variable and units:} \hrulefill\responseline
\textbf{Support:} $S_X=$ \hrulefill
\par'''
assert old in guided
guided = guided.replace(old,new)
guided = guided.replace(r'\textbf{PMF checks:} \hrulefill%',r'\textbf{PMF check.} Verify nonnegative masses and a total of 1.\worklines{2}')
guided = guided.replace(r'''\task{2}{Write the CDF table for every real cutoff and represent it graphically. Verify its defining
  properties and that its jumps reproduce the PMF. Interpret $F_X(12)$ in this context.}''',r'''\task{2}{Complete the CDF interval table for every real cutoff and draw its step graph. Then check
  its defining properties and that its jumps reproduce the PMF.}''')
guided = guided.replace(r'''\textbf{CDF checks and contextual interpretation:}\worklines{3}
\vfill''',r'''\textbf{CDF checks.} Check the range, monotonicity, right-continuity, tails and jumps.\worklines{2}
\textbf{Question 1 --- Fee at most 15 USD ($F_X(15)$).} Use the CDF to find and interpret the probability
that the additional late fee is at most 15 USD.
\textbf{Response 1 (cutoff interval, calculation and interpretation):}\worklines{3}
\textbf{Question 2 --- Fee at most 25 USD ($F_X(25)$).} Use the CDF to find and interpret the probability
that the additional late fee is at most 25 USD.
\textbf{Response 2 (cutoff interval, calculation and interpretation):}\worklines{3}
\endgroup
\vfill''')
s = s[:start]+guided+s[end:]
start = s.index(r'  \problemtitle{2}{Kayak returns}',s.index(r'\ifprintsolutions',s.index(r'\begin{document}')))
end = s.index(r'  \problemtitle{3}{Workshop scrap buyback}',start)
solution = s[start:end]
taskstart = solution.index(r'  \task{1}')
taskend = solution.index(r'  \textbf{PMF check.}')
# Reuse the guided example's three aligned columns with completed cells.
columns = guided[guided.index('% Match the worked example:'):guided.index(r'\textbf{PMF check.}')]
columns = columns.replace('% Retain the starter; students complete the fee mapping and grouped masses.', '% Completed outcome mapping, grouped calculations and PMF graph.')
fees = [0,0,6,12,18,24,24]
rows = columns.splitlines()
idx = 0
for i,line in enumerate(rows):
    if r'\cTwoOutcome{' in line:
        rows[i] = line[:line.rfind('&')+1] + ' $'+str(fees[idx])+r'$ \\'
        idx += 1
assert idx == 7
columns = '\n'.join(rows)+'\n'
values = [(0,'0.50',r'$0.36+0.14=0.50$'),(6,'0.18',r'$P(5<t\leq15)=0.18$'),(12,'0.12',r'$P(15<t\leq30)=0.12$'),(18,'0.08',r'$P(30<t\leq45)=0.08$'),(24,'0.12',r'$0.07+0.05=0.12$')]
for fee,mass,calc in values:
    columns = columns.replace(r'\rule{0pt}{.82cm} & & \\',f'${fee}$ & ${mass}$ & {calc} '+r'\\',1)
plot = r'''
      \addplot[ybar,bar width=8pt,draw=black,fill=cTwoMassColor!20]
        coordinates {(0,.50)(6,.18)(12,.12)(18,.08)(24,.12)};
      \addplot[only marks,mark=none,nodes near coords,
        every node near coord/.append style={font=\scriptsize},
        point meta=explicit symbolic] coordinates
        {(0,.50) [0.50] (6,.18) [0.18] (12,.12) [0.12] (18,.08) [0.08] (24,.12) [0.12]};
'''
columns = columns.replace(r'    \end{axis}%', plot+r'    \end{axis}%',1)
solution = solution[:taskstart]+r'''  \task{1}{Let $X$ be the additional late fee for one completed rental, in USD; exclude the prepaid
    rental charge. The support is $S_X=\{0,6,12,18,24\}$, with $p_X(x)=0$ elsewhere.
    Group the on-time/early and grace categories at 0 USD, and both categories after 45 minutes at 24 USD.}
'''+columns+solution[taskend:]
solution = solution.replace(r'''  \task{2}{Accumulate in increasing fee order: $0.50;\ 0.68;\ 0.80;\ 0.88;\ 1$.
    For example, $F_X(12)=0.50+0.18+0.12=0.80$. Each new height adds the next grouped PMF mass.}''',r'''  \task{2}{Accumulate in increasing fee order: $0.50;\ 0.68;\ 0.80;\ 0.88;\ 1$.
    Each new height adds the next grouped PMF mass.}''')
solution = solution.replace(r'''  \textbf{Interpretation.} $F_X(12)=0.80$: the probability that the additional late fee is at most 12 USD
  (a return no more than 30 minutes late, including on-time/early returns) is 0.80.''',r'''  \textbf{Question 1 --- Fee at most 15 USD ($F_X(15)$).} Use the CDF to find and interpret the probability
  that the additional late fee is at most 15 USD.

  \textbf{Response 1.} Since $12\leq15<18$, use the interval $12\leq x<18$:
  $P(X\leq15)=F_X(15)=P(X=0)+P(X=6)+P(X=12)=0.50+0.18+0.12=0.80$.
  There is an 80\% probability that the additional late fee is at most 15 USD, corresponding to a return
  no more than 30 minutes late, including on-time/early returns. Although $P(X=15)=0$ because 15 USD is
  not a possible fee, $F_X(15)$ includes all fees below 15 USD as well. It is cumulative, so it is not zero.

  \textbf{Question 2 --- Fee at most 25 USD ($F_X(25)$).} Use the CDF to find and interpret the probability
  that the additional late fee is at most 25 USD.

  \textbf{Response 2.} Since $25\geq24$, use the final interval $x\geq24$:
  $P(X\leq25)=F_X(25)=0.50+0.18+0.12+0.08+0.12=1$.
  There is a 100\% probability that the additional late fee is at most 25 USD: every possible return
  incurs a fee of at most 24 USD, even after an hour.''')
assert 'Response 2.' in solution
s = s[:start]+solution+s[end:]
p.write_text(s, encoding='utf-8')
