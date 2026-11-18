from pathlib import Path
from fractions import Fraction as F
from itertools import product, combinations
from math import comb

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'book2026-2027/grade10/term_2/4-learning_evidences'
OUT.mkdir(parents=True,exist_ok=True)
parts=[]
def add(s): parts.append(s+'\n')
def table(headers,rows,spec=None):
    return '\\begin{center}\n\\begin{tabular}{'+(spec or 'c'*len(headers))+'}\\toprule\n'+ ' & '.join(headers)+r'\\\midrule'+'\n'+'\n'.join(' & '.join(map(str,r))+r'\\' for r in rows)+'\n\\bottomrule\\end{tabular}\n\\end{center}\n'
def m(s): return '$'+str(s)+'$'
def frac(v):
    v=F(v)
    return str(v.numerator) if v.denominator==1 else f'{v.numerator}/{v.denominator}'
def heading(n,title,c,marks):
    add(r'\clearpage'+f'\n\\sectionScored{{{title}}}{{C{c}-\\sml{{{marks}}}}}{{sec:q{n}}}')
def task(n,t,marks,prompt):
    add(f'\\textbf{{Original Task {t} (proposed allocation).}} \\hyperref[sol:q{n}t{t}]{{{prompt}}} \\score{{{marks}}}\n')
    add(f'\\subsection*{{Worked solution to Task {t} \\score{{{marks}}}}}\n\\label{{sol:q{n}t{t}}}')
def credit(s): add(r'\textbf{Proposed partial credit.} '+s)
def back(n): add(f'\\par\\vspace{{3mm}}\\secInicio[][sec:q{n}]')
def pmf(xs,nums,den):
    assert sum(nums)==den and all(n>0 for n in nums)
    add(table([r'$x$ (USD)',r'$p_X(x)$'],[[m(x),m(f'{n}/{den}'+(f'={frac(F(n,den))}' if F(n,den).denominator!=den else ''))] for x,n in zip(xs,nums)]))
    lo,hi=xs[0]-2,xs[-1]+2
    ticks=','.join(map(str,xs))
    width=min((b-a for a,b in zip(xs,xs[1:])),default=1)*.45
    add(r'\begin{center}\begin{tikzpicture}'+'\n'+f'\\begin{{axis}}[keyaxis,width=.86\\linewidth,height=5cm,xmin={lo},xmax={hi},ymin=0,ymax=.65,xtick={{{ticks}}},xticklabel style={{rotate=45,anchor=north east}},ylabel={{$p_X(x)$}},ytick={{0,.1,.2,.3,.4,.5,.6}}]')
    for x,n in zip(xs,nums):
        add(f'\\draw[fill=black!15] (axis cs:{x-width/2},0) rectangle (axis cs:{x+width/2},{n}/{den});')
    add(r'\end{axis}\end{tikzpicture}\end{center}')
    add(r'\textbf{PMF check.} Every listed mass is strictly positive, and $'+ '+'.join(map(str,nums))+f'={den}$, so the masses sum to ${den}/{den}=1$. Set $p_X(x)=0$ outside the support. The graph places bars at the actual monetary values; gaps carry no mass.')
def cdf(n,xs,nums,den,marks):
    add(r'\clearpage'+f'\n\\textbf{{Question {n} --- continued}}')
    task(n,2,marks,'Construct the complete CDF table, including both tails, and draw a labeled step graph. Use open and filled endpoints correctly and preserve actual monetary spacing. Verify the defining CDF properties and that its jumps equal the PMF masses.')
    cum=[]; total=0
    for a in nums: total+=a; cum.append(total)
    add(r'For $F_X(x)=P(X\leq x)$, add masses in increasing payout order. The successive cumulative numerators are $'+','.join(map(str,cum))+f'$, all over ${den}$.')
    rows=[[m(f'x<{xs[0]}'),m(0)]]
    for i,x in enumerate(xs):
        interval=f'{x}\\leq x<{xs[i+1]}' if i+1<len(xs) else f'x\\geq {x}'
        rows.append([m(interval),m(frac(F(cum[i],den)))])
    add(table(['Cutoff interval (USD)',r'$F_X(x)$'],rows))
    lo,hi=xs[0]-2,xs[-1]+2
    ticks=','.join(map(str,xs))
    add(r'\begin{center}\begin{tikzpicture}'+f'\n\\begin{{axis}}[keyaxis,width=.86\\linewidth,height=7cm,xmin={lo},xmax={hi},ymin=-.07,ymax=1.1,xtick={{{ticks}}},xticklabel style={{rotate=45,anchor=north east}},ytick={{0,.25,.5,.75,1}},ylabel={{$F_X(x)$}}]')
    add(f'\\addplot[thick,<-] coordinates {{({lo},0)({xs[0]},0)}};')
    for i,x in enumerate(xs[:-1]): add(f'\\addplot[thick] coordinates {{({x},{cum[i]}/{den})({xs[i+1]},{cum[i]}/{den})}};')
    add(f'\\addplot[thick,->] coordinates {{({xs[-1]},1)({hi},1)}};')
    opens=''.join(f'({x},{(cum[i-1] if i else 0)}/{den})' for i,x in enumerate(xs))
    fills=''.join(f'({x},{cum[i]}/{den})' for i,x in enumerate(xs))
    marker='.8' if n==6 else '1.6'
    add(f'\\addplot[only marks,mark=*,mark size={marker}pt,mark options={{fill=white}}] coordinates {{{opens}}};')
    add(f'\\addplot[only marks,mark=*,mark size={marker}pt] coordinates {{{fills}}};')
    add(r'\end{axis}\end{tikzpicture}\end{center}')
    add(r'\textbf{CDF checks.} The table covers every real cutoff. Heights lie in $[0,1]$ and never decrease. Each horizontal segment includes its left endpoint and excludes its right endpoint: the filled point gives the value at a jump, so the CDF is right-continuous. Arrows extend the tails to $-\infty$ and $+\infty$, where the limits are 0 and 1.')
    add(r'In support order, subtracting successive cumulative numerators (starting at zero) gives $'+','.join(map(str,nums))+f'$. Hence each jump is its PMF mass over ${den}$: '+r'$F_X(a)-F_X(a^-)=p_X(a)$. At unsupported cutoffs both the jump and the mass are zero.')
    if marks==1: credit('0.25 for cumulative sums; 0.25 for the complete interval table and tails; 0.25 for the labeled, correctly spaced step graph and endpoints; 0.25 for the CDF and jump checks. Total: 1 point.')
    elif marks==2: credit('0.5 for cumulative sums; 0.5 for the complete interval table and tails; 0.5 for the labeled, correctly spaced step graph and endpoints; 0.5 for the CDF and jump checks. Total: 2 points.')
    else: credit('0.75 for cumulative sums; 0.75 for the complete interval table and tails; 0.75 for the labeled, correctly spaced step graph and endpoints; 0.75 for the CDF and jump checks. Total: 3 points.')
    back(n)

add(r'''% Original assessment and worked key governed by the supplied assessment brief.
% Build from this directory; all dependencies remain in this academic-year tree.
\makeatletter
\def\input@path{{../../../preamble/}}
\makeatother
\input{preamble_exams.tex}
\linespread{0.98}
\setlength{\parskip}{2pt}
\renewcommand{\arraystretch}{1.0}
\setlength{\emergencystretch}{2em}
\pgfplotsset{keyaxis/.style={axis lines=left,scaled ticks=false,
 xlabel={$x$ (USD)},grid=major,grid style={gray!15},
 tick label style={font=\small},label style={font=\small},clip=false}}
\title{Global Economics Exam Solutions\\Grade 10 --- Term 2 --- C1 and C2}
\author{}
\date{}
\makeatletter
\renewcommand{\@maketitle}{\begin{center}{\Large\bfseries\@title\par}\end{center}}
\renewcommand\subsection{\@startsection{subsection}{2}{\z@}{-1.4ex plus -.3ex}{.7ex}{\normalfont\large\bfseries}}
\makeatother
\hypersetup{pdftitle={Grade 10 Term 2 C1 and C2 Exam Solutions},pdfauthor={Global Economics}}
\begin{document}
\maketitle
\small
\setcounter{tocdepth}{1}
\phantomsection
\label{toc}
\tableofcontents
\section*{Learning objective}
Model discrete monetary outcomes in economic and financial contexts; derive and verify probability mass functions (PMFs), and construct and interpret cumulative distribution functions (CDFs) with tables and graphs.
\section*{Criteria assessment}
This standalone key authors the original questions required by the governing assessment brief and reproduces each task before its worked solution. Questions 1--2 assess C1; Questions 3--6 assess C2. Show reasoning and exact probabilities. All contextual rules are stated in ordinary language.

\textbf{Independent passing thresholds: C1 requires at least 4 out of 8 points; C2 requires at least 4 out of 14 points. Points cannot transfer between criteria.} The overall available total is 22 points. An overall total alone does not establish a pass in both criteria. These are the passing thresholds for this assessment; no cumulative policy is specified.
\section*{Evaluated criteria}
\begin{description}
\item[C1] Characterises discrete random variables in economic and financial contexts by identifying their support, probability mass function and possible outcomes.
\item[C2] Interprets PMFs and CDFs by verifying their defining properties and using them to calculate point, interval, cumulative, and complementary probabilities in financial contexts.
\end{description}
''')
add(table(['Question','Family','C1','C2','Total','Proposed task marks'],[
['1','Type B','4','---','4','1, 2, 1'],['2','Type B','4','---','4','1, 2, 1'],
['3','Basic Type A','---','2','2','1, 1'],['4','Basic Type A','---','2','2','1, 1'],
['5','Advanced Type A','---','4','4','2, 2'],['6','Advanced Type B','---','6','6','3, 3'],
[r'\textbf{Total}','',r'\textbf{8}',r'\textbf{14}',r'\textbf{22}','']], 'llcccc'))
add(r'\textbf{Marking policy.} Question and criterion totals are fixed by the brief. Every task-level split and partial-credit breakdown below is proposed. Award stated fractions for demonstrated components, including valid alternative methods. Allow consistent follow-through after one arithmetic error when subsequent reasoning is correct; do not award a missing normalization or independent verification merely because a table looks plausible. Cap each task, question and criterion at its allocation.')

heading(1,'Online order contribution',1,4)
add('A small seller handles three orders, in first, second and third order. Each order independently has exactly two mutually exclusive possible outcomes: the buyer keeps it with probability 0.6, or cancels it with probability 0.4. These probabilities apply to every order. Each kept order contributes 5 USD and each cancellation contributes no money. A fixed handling cost of 4 USD is then deducted once from the combined contribution. There are no other receipts or costs. Record the net contribution for the three orders.')
task(1,1,1,'List every complete outcome in order and calculate its probability.')
add(r'Write $K$ for kept and $C$ for cancelled. There are $2^3=8$ ordered complete outcomes. Independence permits multiplication within each triple; it does not make the triples equally likely.')
rows=[]; grouped={}
for seq in product('KC',repeat=3):
    k=seq.count('K'); prob=F(3,5)**k*F(2,5)**(3-k); x=5*k-4
    grouped.setdefault(x,[]).append((''.join(seq),prob))
    rows.append([m('\\mathrm{'+''.join(seq)+'}'),m('\\cdot'.join('0.6' if s=='K' else '0.4' for s in seq)),m(frac(prob)+f'={float(prob):.3f}')])
add(table(['Ordered outcome','Product','Exact probability'],rows))
add(r'The eight probabilities sum to $(3/5+2/5)^3=1$.')
credit('0.5 for all eight ordered outcomes; 0.5 for their probabilities using independent products. Total: 1 point.')
back(1)
task(1,2,2,'Define the random variable and its units. Map every complete outcome to a value, identify the support, and construct and verify the grouped PMF.')
add(r'Let $X$ be the net contribution from the three orders, in USD. If $N$ is the number kept, $X=5N-4$. The table maps all eight outcomes and groups those with the same net contribution.')
add(table([r'$x$ (USD)','Complete outcomes','Grouped probability'],[[m(x),m(','.join(r'\mathrm{'+s+'}' for s,p in vals)),m('+'.join(frac(p) for s,p in vals)+'='+frac(sum(p for s,p in vals)))] for x,vals in sorted(grouped.items())]))
add(r'Thus $S_X=\{-4,1,6,11\}$ USD. The PMF is the last column, and is zero elsewhere. All masses are positive, and $(8+36+54+27)/125=1$. A negative value means the handling cost exceeds receipts.')
credit('0.25 for the variable and units; 0.5 for all outcome mappings; 0.25 for support; 0.75 for grouped PMF masses; 0.25 for positivity and normalization checks. Total: 2 points.')
back(1)
task(1,3,1,'Calculate and interpret the probability that the net contribution is at least 6 USD.')
add(r'From the grouped PMF, $P(X\geq6)=p_X(6)+p_X(11)=54/125+27/125=81/125=0.648$. The seller earns a net contribution of at least 6 USD with probability 64.8\%; this happens exactly when at least two orders are kept.')
credit('0.5 for selecting and adding the correct masses; 0.5 for the contextual interpretation. Total: 1 point. Question total: 4 points for C1.')
back(1)

heading(2,'Two supplier loyalty credits',1,4)
add('A retailer receives one loyalty credit from each of two suppliers. The suppliers award credits independently. Each has exactly three mutually exclusive possible outcomes: no credit, a 3 USD credit, or an 8 USD credit. For the first supplier these probabilities are 0.2, 0.5 and 0.3, respectively. For the second supplier they are 0.4, 0.4 and 0.2, respectively. Add both credits; there are no other adjustments. Record the total credit, keeping first-supplier then second-supplier order.')
task(2,1,1,'List every complete ordered outcome and calculate its probability.')
add(r'Each supplier has three possible outcomes, giving $3^2=9$ ordered pairs. Write a pair as its two credit amounts, in USD. Multiply the appropriate probabilities by independence.')
rows=[]; grouped={}
for i,j in product(range(3),repeat=2):
    a,b=[0,3,8][i],[0,3,8][j]; p=[F(2,10),F(5,10),F(3,10)][i];q=[F(4,10),F(4,10),F(2,10)][j]
    grouped.setdefault(a+b,[]).append((f'({a},{b})',p*q))
    rows.append([m(f'({a},{b})'),m(f'{float(p):.1f}\\cdot{float(q):.1f}'),m(frac(p*q)+f'={float(p*q):.2f}')])
add(table(['Ordered credit outcome (USD)','Product','Exact probability'],rows))
add(r'Exhaustiveness check: $(0.2+0.5+0.3)(0.4+0.4+0.2)=1$.')
credit('0.5 for all nine ordered pairs; 0.5 for independent product probabilities. Total: 1 point.')
back(2)
task(2,2,2,'Define the random variable and units; map every outcome to a value; identify the support; construct and verify the grouped PMF.')
add(r'Let $X$ be the total loyalty credit from the two suppliers, in USD. Add the two amounts in each pair. The complete mapping and grouped PMF are:')
add(table([r'$x$ (USD)','Ordered outcomes','Grouped probability'],[[m(x),m(','.join(s for s,p in vals)),m('+'.join(frac(p) for s,p in vals)+'='+frac(sum(p for s,p in vals)))] for x,vals in sorted(grouped.items())]))
add(r'The support is $S_X=\{0,3,6,8,11,16\}$ USD, with zero mass elsewhere. All masses are positive and $(4+14+10+8+11+3)/50=50/50=1$. Reversing a pair can preserve its monetary value while changing its probability.')
credit('0.25 for variable and units; 0.5 for all mappings; 0.25 for support; 0.75 for grouped masses; 0.25 for positivity and normalization checks. Total: 2 points.')
back(2)
task(2,3,1,'Calculate and interpret the probability that the total credit is at least 11 USD.')
add(r'$P(X\geq11)=p_X(11)+p_X(16)=11/50+3/50=7/25=0.28$. The retailer receives a total credit of at least 11 USD with probability 28\%; the qualifying pairs are $(3,8),(8,3),(8,8)$.')
credit('0.5 for selecting and adding the correct masses; 0.5 for the contextual interpretation. Total: 1 point. Question total: 4 points for C1. Criterion C1 total: 8 points; independent pass: at least 4 points.')
back(2)

basic=[(3,'Local parcel delivery fees',
'A cooperative sends one parcel using exactly one of four exhaustive, mutually exclusive delivery methods: bicycle, walking courier, van or truck. Their probabilities are 0.15, 0.25, 0.35 and 0.25, respectively. Bicycle and walking deliveries have no handling fee. The handling fee is 4 USD for a van delivery and 11 USD for a truck delivery. No other handling charges apply. Record the handling fee for the parcel.',
'handling fee for one parcel',[('Bicycle','0.15',0),('Walking courier','0.25',0),('Van','0.35',4),('Truck','0.25',11)],
r'The bicycle and walking categories both give zero: $p_X(0)=0.15+0.25=0.40=8/20$. The van gives $p_X(4)=0.35=7/20$ and the truck gives $p_X(11)=0.25=5/20$.', [0,4,11],[8,7,5],20),
(4,'Warranty service payouts',
'A warranty provider classifies one claim in exactly one of five exhaustive, mutually exclusive categories: no service, remote assistance, parts repair, replacement or refund. Their probabilities are 0.30, 0.20, 0.15, 0.25 and 0.10, respectively. The provider pays nothing for no service, 2 USD for remote assistance, 6 USD for parts repair and 15 USD for either replacement or refund. No additional payments apply. Record the provider\'s payout for one claim.',
'provider payout for one claim',[('No service','0.30',0),('Remote assistance','0.20',2),('Parts repair','0.15',6),('Replacement','0.25',15),('Refund','0.10',15)],
r'The first three categories give $p_X(0)=0.30=6/20$, $p_X(2)=0.20=4/20$ and $p_X(6)=0.15=3/20$. Replacement and refund are mutually exclusive and share a payout: $p_X(15)=0.25+0.10=0.35=7/20$.',[0,2,6,15],[6,4,3,7],20)]
for n,title,context,definition,mapping,group,xs,nums,den in basic:
    heading(n,title,2,2); add(r'\textbf{Basic Type A.} '+context)
    task(n,1,1,'Define the random variable and support; derive and verify the grouped PMF; produce its table and a labeled graph with actual monetary spacing.')
    add(f'Let $X$ be the {definition}, in USD. Map the supplied categories to payments:')
    add(table(['Category','Given probability',r'$X$ (USD)'],[[a,m(b+'='+frac(F(b))),m(c)] for a,b,c in mapping]))
    add(group)
    add('$S_X=\\{'+','.join(map(str,xs))+r'\}$ USD. Add probabilities of mutually exclusive categories sharing a value, because the events cannot occur together.')
    pmf(xs,nums,den)
    credit('0.25 for variable, units and support; 0.25 for category mapping, grouping and the PMF table; 0.25 for the labeled, correctly spaced graph; 0.25 for positivity and normalization. Total: 1 point.')
    back(n)
    cdf(n,xs,nums,den,1)
    add(r'\textbf{Question total: 2 points for C2.}')

heading(5,'Marketplace account credits',2,4)
add(r'\textbf{Advanced Type A.} For one purchase, a marketplace awards exactly one account credit: 0, 2, 5, 9, 14 or 20 USD. These are all possible credits and their categories are mutually exclusive. A 2 USD credit is twice as likely as no credit. A 5 USD credit is as likely as no credit and a 2 USD credit combined. A 9 USD credit is twice as likely as a 5 USD credit. A 14 USD credit is half as likely as a 9 USD credit. A 20 USD credit is as likely as the 2 USD and 14 USD credits combined. There are no other payments or adjustments. Determine the probabilities from these likelihood relationships and record the account credit.')
task(5,1,2,'Define the random variable and support. Derive the six probabilities using normalization, verify the PMF, and produce its table and labeled graph.')
add(r'''Let $X$ be the account credit for one purchase, in USD, with $S_X=\{0,2,5,9,14,20\}$. Set $a=P(X=0)$. Since the categories are mutually exclusive, a combined likelihood is a sum. Translate the relationships in their stated order:
\begin{align*}
p_X(0)&=a,&p_X(2)&=2a,\\
p_X(5)&=a+2a=3a,&p_X(9)&=2(3a)=6a,\\
p_X(14)&=\tfrac12(6a)=3a,&p_X(20)&=2a+3a=5a.
\end{align*}
Normalization gives
\[
a+2a+3a+6a+3a+5a=1,\qquad 20a=1,\qquad a=\frac1{20}.
\]
Every probability is now uniquely determined: all depend on the single baseline, whose positive coefficient in the normalization equation is 20. No probability is zero. Each credit is already a distinct monetary value, so no additional grouping is needed.''')
pmf([0,2,5,9,14,20],[1,2,3,6,3,5],20)
add(r'\textbf{Relationship check.} The numerators satisfy $2=2(1)$, $3=1+2$, $6=2(3)$, $3=6/2$, and $5=2+3$, exactly reproducing all five verbal relationships.')
credit('0.25 for variable, units and support; 0.75 for translating the relationships and solving normalization; 0.5 for all six PMF entries; 0.25 for the labeled, correctly spaced graph; 0.25 for positivity, normalization and relationship checks. Total: 2 points.')
back(5)
cdf(5,[0,2,5,9,14,20],[1,2,3,6,3,5],20,2)
add(r'\textbf{Question total: 4 points for C2.}')

heading(6,'Community market prize tickets',2,6)
add(r'\textbf{Advanced Type B.} A community market has nine physically distinct prize tickets: four worth 0 USD each, three worth 5 USD each and two worth 12 USD each. Choose a subset of three tickets uniformly without replacement, so every subset of three physically distinct tickets has the same chance. Ignore selection order. First add the face values. Then add one bonus of 7 USD if the selected subset contains at least one 5 USD ticket and at least one 12 USD ticket; otherwise add no bonus. Finally, if this adjusted amount exceeds 25 USD, pay only 25 USD; otherwise pay the adjusted amount. No other payments or deductions apply. Record the final payout.')
task(6,1,3,'Define the random variable and support. Count the distinct-ticket selections, apply the bonus and then the cap, aggregate equal final payouts, and derive and verify the PMF. Produce its table and labeled graph.')
add(r'''Let $X$ be the final payout for one three-ticket subset, in USD. Label the physical tickets $Z_1,\ldots,Z_4$, $L_1,\ldots,L_3$, and $H_1,H_2$, with values 0, 5 and 12 USD. There are
\[
\binom93=\frac{9\cdot8\cdot7}{3\cdot2\cdot1}=84
\]
equally likely unordered subsets, each with probability $1/84$. A composition records $(a,b,c)$, the counts of zero-, five- and twelve-dollar tickets. Feasible counts satisfy $a+b+c=3$, $0\leq a\leq4$, $0\leq b\leq3$, and $0\leq c\leq2$. The number of subsets with that composition is
\[
N(a,b,c)=\binom4a\binom3b\binom2c,\qquad P(a,b,c)=\frac{N(a,b,c)}{84}.
\]
Define $I=1$ if $b\geq1$ and $c\geq1$, and $I=0$ otherwise. The face sum is $5b+12c$; the adjusted amount is $Y=5b+12c+7I$; finally $X=\min\{Y,25\}$. The bonus is added once, before the cap.''')
rows=[]; hist={}; comps=[]
for c in range(3):
    for b in range(4-c):
        a=3-b-c; count=comb(4,a)*comb(3,b)*comb(2,c); face=5*b+12*c; bonus=7 if b and c else 0; pre=face+bonus; x=min(pre,25)
        hist[x]=hist.get(x,0)+count;comps.append((a,b,c,count,x))
        rows.append([m(f'({a},{b},{c})'),m(f'\\binom4{{{a}}}\\binom3{{{b}}}\\binom2{{{c}}}={count}'),m(f'{count}/84'),str(face),str(bonus),str(pre),str(x)])
assert sum(hist.values())==84
add(r'\begingroup\renewcommand{\arraystretch}{1.35}')
add(table([r'$(a,b,c)$','Subset count', 'Probability','Face sum','Bonus',r'$Y$',r'$X$'],rows))
add(r'\endgroup')
add(r'All monetary columns are in USD. These nine compositions are exhaustive: list $c=0,1,2$ and every feasible $b$, then $a=3-b-c$. Their counts sum to $4+18+12+1+12+24+6+4+3=84$. Compositions are not equally likely: for example, $(1,1,1)$ represents 24 subsets, whereas $(0,3,0)$ represents only one.')
add(r'\textbf{Aggregation.} The 24 USD payout comes from $(1,1,1)$ (24 subsets after the bonus) and $(1,0,2)$ (4 subsets without a bonus), so $p_X(24)=(24+4)/84=28/84$. The cap merges the adjusted amounts 29 and 36 USD from $(0,2,1)$ and $(0,1,2)$, so $p_X(25)=(6+3)/84=9/84$. Each other payout arises from one composition.')
add(r'Thus $S_X=\{0,5,10,12,15,24,25\}$ USD. The cap binds only when the adjusted amount is greater than 25 USD; the 24 USD payout remains unchanged.')
back(6)
add(r'\clearpage\textbf{Question 6 --- Task 1 continued: grouped PMF and graph}')
pmf([0,5,10,12,15,24,25],[4,18,12,12,1,28,9],84)
credit('0.25 for variable, units and support; 0.75 for the denominator and exhaustive composition counts; 0.75 for the bonus, cap and aggregation; 0.5 for the grouped PMF table; 0.5 for the labeled, correctly spaced graph; 0.25 for positivity and normalization checks. Total: 3 points.')
back(6)
cdf(6,[0,5,10,12,15,24,25],[4,18,12,12,1,28,9],84,3)
add(r'\textbf{Scoring reconciliation.} Question 6 gives $3+3=6$ points for C2. C2 gives $2+2+4+6=14$ points; its independent passing threshold is 4 points. C1 gives $4+4=8$ points; its independent passing threshold is also 4 points. The overall available total is $8+14=22$ points, with no transfer between criteria.')
add(r'\end{document}')
(OUT/'G10_T2_L1_C1C2_exam_solution.tex').write_text('\n'.join(parts),encoding='utf-8')

# Independent verification by individual physical-ticket subsets.
tickets=[0]*4+[5]*3+[12]*2
direct={}
for inds in combinations(range(9),3):
    vals=[tickets[i] for i in inds]
    payout=min(sum(vals)+(7 if 5 in vals and 12 in vals else 0),25)
    direct[payout]=direct.get(payout,0)+1
assert direct==hist
assert [direct[x] for x in sorted(direct)]==[4,18,12,12,1,28,9]
assert sum([4,4,2,2,4,6])==22
print('Created',OUT/'G10_T2_L1_C1C2_exam_solution.tex')
print('Verified all 84 physical-ticket subsets:',dict(sorted(direct.items())))
