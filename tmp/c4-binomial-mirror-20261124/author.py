from pathlib import Path
from fractions import Fraction as F
from math import comb, lcm
import json

ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'book2026-2027/grade10/term_2/1-practice_activities/G10_T2_L1_C4_practice_activity.tex'
C3=OUT.with_name('G10_T2_L1_C3_practice_activity.tex').read_text(encoding='utf-8')
def frac(x):
    x=F(x)
    return str(x.numerator) if x.denominator==1 else rf'\frac{{{x.numerator}}}{{{x.denominator}}}'
def expr(a,b,v='X'):
    return f'{a}'+('+' if b>0 else '-')+f'{abs(b)}{v}'
def pair(parts):
    s=''
    for j in range(0,len(parts),2):
        if j+1<len(parts): s+='\\PracticeColumnPair{\n'+parts[j]+'\n}{\n'+parts[j+1]+'\n}\n'
        else: s+='\\par\\noindent\\begin{minipage}[t]{.48\\linewidth}\\vspace{0pt}\n'+parts[j]+'\n\\end{minipage}\\par\n'
    return s

# Same economic sequence and endpoint payoffs as C3 wherever convenient.
DATA=[
dict(key='art',title='Introductory example 1: campus art-print stall',label='ex:intro-one',n=4,p=F(2,5),period='one weekend',trial='one of four pre-booked campus-market sales slots',success='attendance in that slot meets its fixed target',failure='attendance in that slot falls below its target',count='high-demand slots',context='A student books all four sales slots before the weekend. Compare a small print batch with a large batch; both can serve every slot without stock shortages.',alts=[('small print batch',-20,20),('large print batch',-40,40)],event=('exact',2,2)),
dict(key='internet',title='Introductory example 2: freelance livestream work',label='ex:intro-two',n=3,p=F(1,10),period='one day',trial='one of three scheduled livestream sessions',success='a home-internet disruption occurs during that session',failure='no home-internet disruption occurs during that session',count='disrupted sessions',context='A freelancer commits to three paid sessions before the day begins. Compare home internet alone with mobile-data backup. Count home-internet disruptions even when backup limits their financial effect.',alts=[('home internet alone',100,-40),('mobile-data backup',60,-25)],event=('atleast',1,3)),
dict(key='inventory',title='Campus sticker sales for one weekend',label='prob:c4-inventory',n=4,p=F(2,5),period='one weekend',trial='one of four pre-booked campus-market sales slots',success='attendance in that slot meets its fixed target',failure='attendance in that slot falls below its target',count='high-demand slots',context='A student books four sales slots in advance. Compare a basic sticker pack with a premium pack obtained more cheaply per sticker through a shared bulk order. Each plan can serve every slot.',alts=[('basic sticker pack',-40,30),('premium sticker pack',-20,50)],event=('atmost',0,2)),
dict(key='coffee',title='Campus fair or online CV workshop',label='prob:c4-coffee',n=4,p=F(1,2),period='one day',trial='one of four separately organized campus careers fairs scheduled that day',success='that fair goes ahead',failure='that fair is cancelled',count='fairs that go ahead',context='A graduate chooses a plan covering four separately organized fairs: portrait sessions for their customers, or an online CV workshop for the same four student groups. Each fair that goes ahead brings portrait business but draws one group away from the workshop.',alts=[('portrait sessions',-40,35),('online CV workshop',100,-30)],event=('interval',1,3)),
dict(key='energy',title='Freelance digital projects for one month',label='prob:c4-energy',n=4,p=F(1,4),period='one month',trial='one of four client enquiries fixed at the start of the month',success='that enquiry confirms a paid project by month end',failure='that enquiry does not confirm a project by month end',count='confirmed projects',context='A freelancer follows the same four enquiries under either hypothetical service plan: social-media graphics or short video edits. Assume confirmation depends on the client budget decision and has the same probability under either plan; capacity suffices for all four.',alts=[('social-media graphics',-30,30),('short video edits',-60,30)],event=('exact',1,1)),
dict(key='manufacturing',title='Graduation photography for one quarter',label='prob:c4-manufacturing',n=3,p=F(3,5),period='one quarter',trial='one of three separately organized graduation ceremonies booked in advance',success='that ceremony goes ahead',failure='that ceremony is cancelled',count='ceremonies that go ahead',context='A graduate reserves three photography bookings for the quarter. Compare a basic photo package with an edited package, using the same ceremony outcomes and advance preparation costs.',alts=[('basic photo package',-100,100),('edited photo package',-100,200)],event=('atleast',2,3)),
dict(key='restaurant',title='Campus concert: three venue choices',label='prob:fees',n=5,p=F(9,25),period='one evening',trial='one of five preselected campus ticket-sales groups',success='that group reaches its fixed ticket-sales target by the evening',failure='that group falls below its target',count='groups reaching their targets',context='A student group chooses a small hired room, a discounted student-union room or a large hired room for the same concert. Tickets are sold in five fixed group allotments; all venues can accommodate all allotments. Extra net receipts arise from each group reaching its target.',alts=[('small hired room',-80,36),('student-union room',-20,48),('large hired room',-100,100)],event=('interval',2,4)),
dict(key='agriculture',title='Student fitness sessions: three break-even thresholds',label='prob:defects',n=4,p=F(1,2),period='one university term',trial='one of four preselected campus fitness-interest groups',success='that group reaches its fixed enrollment target by the registration deadline',failure='that group falls below its target',count='groups reaching their enrollment targets',context='A student plans walking, dance or circuit sessions for the same four groups. All formats have capacity for all groups. Use the same enrollment responses for every hypothetical format, with different fixed preparation costs and receipts per successful group.',alts=[('walking group',-70,40),('dance sessions',-30,55),('circuit sessions',-150,75)],event=('atmost',0,1)),
]

pre=C3.split('\\begin{document}')[0]
pre=pre.replace('Bernoulli Models and Individual Break-Even Analysis','Binomial Models and Individual Break-Even Analysis').replace('Criterion C3','Criterion C4')
pre=pre.replace('Probability} $\\SuccessProb{p}=\\SuccessProb{P}(\\HLMathEvent{E})$','Trial success probability} $\\SuccessProb{p}$')
pre=pre.replace('\\begin{minipage}[t]{.48\\linewidth}#1','\\begin{minipage}[t]{.48\\linewidth}\\vspace{0pt}#1').replace('\\begin{minipage}[t]{.48\\linewidth}#2','\\begin{minipage}[t]{.48\\linewidth}\\vspace{0pt}#2')
pre+=r'''
% Document-local extension: shared registry and other consumers remain unchanged.
\newcommand{\TrialCount}[1]{\HLObservationCount{#1}}
\newcommand{\Count}[1]{\GTenHLValue{#1}}
\expandafter\renewcommand\csname practicehighlightlegend@G10-T2-C4-coordinated\endcsname{%
\HighlightConciseTable{
$\HLMathEvent{E_j},\HLMathEvent{E_j^c}$ & \HLMathEvent{Trial events} & Success and failure on one trial.\\[4pt]
$\Indicator{B_j}$; $\Count{X,k}$ & \Count{Indicator; count} & One binary result; total successes and a possible count.\\[4pt]
$\TrialCount{n}$ & \TrialCount{Fixed trial count} & Number observed, chosen beforehand.\\[4pt]
$\SuccessProb{p}$; $\FailureProb{1-p}$ & \SuccessProb{Success}; \FailureProb{failure} & Complementary probabilities for one trial.\\[4pt]
$\Money{Y_i},\Money{a_i},\Money{b_i}$; $\TransformationFunction{f_i}$ & \Money{Money}; \TransformationFunction{rule} & Net payoff, baseline, change per success; count-to-money map.\\[4pt]
$\HLProbability{m_X(k),q_k}$ & \HLProbability{Probability mass} & Probability at exactly one count.\\[4pt]
$\HLCumulativeProbability{F_X(t)}$ & \HLCumulativeProbability{Cumulative probability} & Probability up to and including a threshold.\\[4pt]
$\ExpectedValue{\mathbb E}[\Money{Y_i}]$ & \ExpectedValue{Expectation} & Long-run average net payoff.\\[4pt]
$\SuccessProb{p_i^*}$ & \SuccessProb{Break-even probability} & Trial probability making one expectation zero.\\[4pt]
}}
'''
front=r'''
\begin{document}
\maketitle
\setcounter{tocdepth}{1}
\setcounter{secnumdepth}{2}
\phantomsection\label{toc}
\tableofcontents
\section*{Evaluated criteria}
\begin{description}
\item[\textbf{C4}] Applies the binomial distribution to fixed-trial financial situations by verifying its conditions and calculating probabilities using the binomial probability formula.
\end{description}
\textbf{How to practise.} Attempt each C4 task before opening its linked worked solution.
Use the return arrows for the contents, problem and problem list. All data are hypothetical.
Keep exact expressions and round final probabilities to four decimal places.
Money is net profit in USD for the entire stated period, after the stated costs.
Choose one hypothetical alternative; all alternatives in a problem are functions of the same count $X$.
Independent trials do not make these monetary variables independent.
Analyse each expectation against its own zero threshold.

\clearpage
\section{Introduction}\label{sec:introduction}\label{sec:t2-c4-introduction}
\subsection*{Highlight legend}
\phantomsection\label{tab:highlight-legend}
\PracticeHighlightLegend{G10-T2-C4-coordinated}
Related probability shades distinguish success, failure, exact mass and cumulative probability.
Names, notation and units preserve meaning in grayscale and with highlights disabled.
See the \hyperref[tab:notation-reference]{detailed notation reference} after the two examples.

\subsection*{From one binary result to a fixed count}
A single trial has two outcomes; a fixed collection can have many success counts.
For trial $j$, let $\HLMathEvent{E_j}$ denote success and $\HLMathEvent{E_j^c}$ failure, and define
\[
\Indicator{B_j}=\begin{cases}1,&E_j\text{ occurs},\\0,&E_j^c\text{ occurs}.\end{cases}
\qquad
\Count{X}=\sum_{j=1}^{\TrialCount{n}}\Indicator{B_j}\sim\operatorname{Bin}(\TrialCount{n},\SuccessProb{p}),\quad n>1.
\]
The indicators are independent Bernoulli$(p)$ variables. $B_1=1$ concerns one trial;
$X=2$ concerns the whole collection and is a different event.
Mathematical success can be financially undesirable, as in Example 2.

\textbf{Four binomial conditions.} (1) Fix $n$ before observation and observe all $n$ trials;
do not stop at the first success. (2) Each trial has mutually exclusive and exhaustive success/failure outcomes.
(3) Assume independence: learning other results does not change a trial's probability.
(4) Use the same $p$ for every trial. Separate customers or sessions alone do not prove independence:
common shocks or changing groups can invalidate the model. The following scenarios explicitly assume these conditions.

\textbf{Why combinations?} A specified order with $k$ successes has probability $p^k(1-p)^{n-k}$.
There are $\binom nk=n!/[k!(n-k)!]$ such orders; $0!=1$.
For example, two successes in three trials can be SSF, SFS or FSS, so their total is
$3p^2(1-p)$, not just $p^2(1-p)$. Thus
\[
\HLProbability{P(X=k)}=\binom nk\SuccessProb{p}^{k}\FailureProb{(1-p)}^{n-k},\qquad k=0,\ldots,n.
\]
'''

def scenario(d,stage,intro=False):
    n,p=d['n'],d['p']; alts=d['alts']; key=d['key']; label=d['label']
    q=[F(comb(n,k))*p**k*(1-p)**(n-k) for k in range(n+1)]
    D=lcm(*(v.denominator for v in q)); weights=[int(v*D) for v in q]
    d['q']=[str(v) for v in q]
    s=('' if key in ('inventory','restaurant') else '\\clearpage\n')+rf'\subsection{{{d["title"]}}}\label{{{label}}}'+'\n'
    if key=='restaurant': s+=r'\label{prob:c4-restaurant}'+'\n'
    if key=='agriculture': s+=r'\label{prob:c4-agriculture}'+'\n'
    s+=d['context']+'\n'+f"The observation period is {d['period']}. One trial is {d['trial']}.\n"
    s+=f"Success means {d['success']}; failure means {d['failure']}.\n"
    s+=rf'All $\TrialCount{{n}}=\TrialCount{{{n}}}$ trials are fixed before observation and all are observed. '+'\n'
    s+=rf'Assume independent outcomes and constant $\SuccessProb{{p}}=\SuccessProb{{{frac(p)}}}$ for each trial, under every alternative. '+'\n'
    s+='The following baseline and per-success changes already include the relevant costs.\n'
    s+=r'\begin{center}\begin{tabular}{lrr}\toprule Alternative & Baseline $a_i$ (USD) & Change $b_i$ (USD/success)\\\midrule'+'\n'
    for i,(name,a,b) in enumerate(alts,1): s+=rf'$A_{i}$: {name} & {a} & {b}\\'+'\n'
    s+=r'\bottomrule\end{tabular}\end{center}'+'\n'
    typ,lo,hi=d['event']
    ev={'exact':rf'X={lo}','atmost':rf'X\leq {hi}','atleast':rf'X\geq {lo}','interval':rf'{lo}\leq X\leq {hi}'}[typ]
    s+=rf'''\QuestionsTasks[{stage}]{{
{{4}}/{{sol:c4-{key}-model}}/{{\textbf{{Task 1 --- Establish the binomial model and monetary transformations.}}
\textbf{{1.}} Define the trial indicators, count and model; verify the four conditions and derive each monetary rule.
\textbf{{2.}} Give positive-probability supports, complete PMFs and real-threshold CDFs for the count and every alternative, including $p=0,1$.
\textbf{{3.}} Calculate the full initial masses, $P({ev})$ and each probability of a strictly negative payoff. Translate each loss into an integer count event.}},
{{4}}/{{sol:c4-{key}-decision}}/{{\textbf{{Task 2 --- Individual expected values.}}
\textbf{{1.}} Calculate and interpret every initial expectation.
\textbf{{2.}} Hold $n$ and the monetary rules fixed; derive each expectation for $p\in[0,1]$, its exact zero threshold and both strict sign intervals.
\textbf{{3.}} Graph each expectation separately with its zero line, endpoints and exact root. Check the endpoints and root, and distinguish expected profit, realized profit and loss probability.}}
}}
\subsubsection*{{Task 1 --- Worked solution}}\label{{sol:c4-{key}-model}}
\paragraph{{1. Binomial model and monetary transformations.}}
For $j=1,\ldots,{n}$, $\HLMathEvent{{E_j}}$ means {d['success']}; $E_j^c$ means {d['failure']}.
Set $\Indicator{{B_j}}=1$ on $E_j$ and $B_j=0$ otherwise.
The fixed count, binary outcomes, assumed independence and common probability give
\[
\Count{{X}}=\Indicator{{B_1}}+\cdots+\Indicator{{B_{n}}}\sim\operatorname{{Bin}}({n},p),
\quad \SuccessProb{{p_0}}=\SuccessProb{{{frac(p)}}},\quad \FailureProb{{1-p_0}}=\FailureProb{{{frac(1-p)}}}.
\]
$X$ counts {d['count']}; it has count units, whereas each $Y_i$ is in USD per {d['period']}.
'''
    parts=[]
    for i,(name,a,b) in enumerate(alts,1):
        meaning=(f'a fixed cost of {abs(a)} USD' if a<0 else f'a baseline net receipt of {a} USD with no successes')
        change=f'{abs(b)} USD '+('extra net receipts' if b>0 else 'net reduction through refunds, lost receipts and disruption costs')+' per success'
        parts.append(rf'''\textbf{{$Y_{i}$: {name}.}}
Here $\Money{{a_{i}}}=\Money{{{a}}}$ represents {meaning}; $\Money{{b_{i}}}=\Money{{{b}}}$ means {change}.
\[
\Money{{Y_{i}}}=\TransformationFunction{{f_{i}}}(\Count{{X}})=\Money{{{a}}}{'+' if b>0 else '-'}\Money{{{abs(b)}}}\Count{{X}}.
\]
Thus $f_{i}(0)={a}$ and $f_{i}({n})={a+b*n}$ USD: both strict payoff signs are attainable when $0<p<1$.''')
    s+=pair(parts)
    s+=rf'''\clearpage
\paragraph{{2. Supports, PMFs, and ordered CDFs.}}
Write $\HLProbability{{q_k}}=\binom{{{n}}}k p^k(1-p)^{{{n}-k}}$ for integer $k=0,\ldots,{n}$.
\[
S_X=\{{x\in\mathbb R:P(X=x)>0\}}=
\begin{{cases}}\{{0,\ldots,{n}\}},&0<p<1,\\\{{0\}},&p=0,\\\{{{n}\}},&p=1.\end{{cases}}
\]
\[
m_X(x)=\begin{{cases}}q_x,&x\in\{{0,\ldots,{n}\}},\\0,&\text{{otherwise}},\end{{cases}}
\qquad
F_X(t)=\begin{{cases}}0,&t<0,\\\displaystyle\sum_{{j=0}}^{{\lfloor t\rfloor}}q_j,&0\leq t<{n},\\1,&t\geq {n}.\end{{cases}}
\]
The PMF is zero at noninteger counts too. At $p=0$ use $q_0=1$, all others zero;
at $p=1$ use $q_{{{n}}}=1$, all others zero (equivalently take endpoint limits).
The sum $\sum_{{k=0}}^{n}q_k=(p+(1-p))^{n}=1$ checks normalization.
Each affine rule is one-to-one, so its mass at $f_i(k)$ is exactly $q_k$.
'''
    parts=[]
    for i,(name,a,b) in enumerate(alts,1):
        vals=sorted(a+b*k for k in range(n+1)); low,high=vals[0],vals[-1]
        floor=rf'\lfloor(t-({a}))/{b}\rfloor' if b>0 else rf'\lceil({a}-t)/{abs(b)}\rceil'
        mid=rf'\sum_{{j=0}}^{{{floor}}}q_j' if b>0 else rf'\sum_{{j={floor}}}^{{{n}}}q_j'
        parts.append(rf'''\textbf{{$Y_{i}$: {name}.}}
For $0<p<1$, the support in ascending USD order is
\[S_{{Y_{i}}}=\{{{','.join(map(str,vals))}\}}.\]
This is $\{{y:P(Y_{i}=y)>0\}}$. At $p=0$ only ${a}$ remains; at $p=1$ only ${a+b*n}$ remains.
\[
m_{{Y_{i}}}(y)=\begin{{cases}}q_k,&y={expr(a,b,'k')},\\&k=0,\ldots,{n},\\0,&\text{{otherwise}}.\end{{cases}}
\]
Since ${expr(a,b)}\leq t$ means $X{'\\leq' if b>0 else '\\geq'} {floor}$,
\[
F_{{Y_{i}}}(t)=\begin{{cases}}0,&t<{low},\\\displaystyle {mid},&{low}\leq t<{high},\\1,&t\geq {high}.\end{{cases}}
\]
For example, $F_{{Y_{i}}}({vals[1]})={'q_0+q_1' if b>0 else f'q_{n}+q_{{{n-1}}}'}$; the jump includes its threshold.''')
    s+=pair(parts)
    s+='CDFs run from the smallest to largest monetary value, regardless of count order. Floors round down; ceilings round up. The displayed finite sums include every jump at its threshold and are right-continuous. Endpoint formulas still apply, but zero-mass values leave the support.\n'
    s+=r'\clearpage\paragraph{3. Initial probabilities and loss events.}'+'\n'
    s+=rf'At $p_0={frac(p)}$, $q_k=\binom{{{n}}}k({frac(p)})^k({frac(1-p)})^{{{n}-k}}$. The following exact table gives all initial count and monetary masses. In column $k$, each amount $f_i(k)$ has probability $q_k=w_k/{D}$; all other amounts have probability zero.'+'\n'
    s+='\\begin{center}\\begin{tabular}{l'+'r'*(n+1)+r'}\toprule'+'\n'
    s+='$k$ & '+' & '.join(map(str,range(n+1)))+r'\\\midrule'+'\n'
    s+='$w_k$ & '+' & '.join(map(str,weights))+r'\\'+'\n'
    for i,(name,a,b) in enumerate(alts,1): s+=rf'$f_{i}(k)$ (USD) & '+' & '.join(str(a+b*k) for k in range(n+1))+r'\\'+'\n'
    s+=r'\bottomrule\end{tabular}\end{center}'+'\n'
    value=sum(q[lo:hi+1]); terms='+'.join(f'q_{{{k}}}' for k in range(lo,hi+1))
    form={'exact':rf'\binom{{{n}}}{{{lo}}}({frac(p)})^{{{lo}}}({frac(1-p)})^{{{n-lo}}}',
        'atmost':rf'F_X({hi})=\sum_{{j=0}}^{{{hi}}}\binom{{{n}}}j({frac(p)})^j({frac(1-p)})^{{{n}-j}}',
        'atleast':rf'1-F_X({lo-1})=1-\sum_{{j=0}}^{{{lo-1}}}\binom{{{n}}}j({frac(p)})^j({frac(1-p)})^{{{n}-j}}',
        'interval':rf'F_X({hi})-F_X({lo-1})=\sum_{{j={lo}}}^{{{hi}}}\binom{{{n}}}j({frac(p)})^j({frac(1-p)})^{{{n}-j}}'}[typ]
    s+=rf'\textbf{{Requested count event (C4).}} The endpoints in ${ev}$ are explicit. Using the binomial formula,'+'\n'
    s+=rf'\[P({ev})={form}.\]'+'\n'
    s+=rf'\[P({ev})={terms}={frac(value)}\approx\HLProbability{{{float(value):.4f}}}.\]'+'\n'
    if typ=='atleast': s+=f'The complement ends at {lo-1}, not {lo}.\n'
    if typ=='interval': s+=f'Both {lo} and {hi} are included; subtract counts at most {lo-1}, not at most {lo}.\n'
    s+=f'This is the probability of the stated count of {d["count"]} over {d["period"]}, with no monetary units.\n'
    parts=[]
    for i,(name,a,b) in enumerate(alts,1):
        r=F(-a,b); ks=[k for k in range(n+1) if a+b*k<0]; loss=sum(q[k] for k in ks)
        cutoff=max(ks) if b>0 else min(ks)
        relation=rf'X<{frac(r)}\iff X\leq {cutoff}' if b>0 else rf'X>{frac(r)}\iff X\geq {cutoff}'
        sumform=rf'\sum_{{j=0}}^{{{cutoff}}}q_j' if b>0 else rf'1-\sum_{{j=0}}^{{{cutoff-1}}}q_j'
        parts.append(rf'''\textbf{{$Y_{i}$: {name}.}}
\[
\begin{{aligned}}
Y_{i}<0&\iff {expr(a,b)}<0\\
&\iff {relation}.
\end{{aligned}}
\]
Hence the initial probability of a net loss is
\[
P(Y_{i}<0)={sumform}
={frac(loss)}\approx\HLProbability{{{float(loss):.4f}}}.
\]
The loss counts are $\{{{','.join(map(str,ks))}\}}$. '''+('A zero payoff is excluded by the strict inequality.' if r.denominator==1 else 'The cutoff is an integer; do not round the strict threshold to the nearest integer.'))
    s+=pair(parts)
    s+=rf'\secInicio[{label}][{stage}]'+'\n'
    s+=rf'''\clearpage
\subsubsection*{{Task 2 --- Worked solution}}\label{{sol:c4-{key}-decision}}
\paragraph{{1. Initial expected values.}}
Connect expectation to the full distribution: $\mathbb E[X]=\sum_{{k=0}}^{n}kq_k=np$.
Equivalently, $\mathbb E[B_j]=1p+0(1-p)=p$, so linearity gives
$\mathbb E[B_1+\cdots+B_{n}]={n}p$.
At the supplied $p_0={frac(p)}$, $\ExpectedValue{{\mathbb E[X]}}={n}({frac(p)})={frac(n*p)}$ successes.
For each alternative, the same distribution gives $\mathbb E[Y_i]=\sum_k f_i(k)q_k$.
'''
    parts=[]
    for i,(name,a,b) in enumerate(alts,1):
        val=a+b*n*p
        interp=('expected net gain' if val>0 else 'expected net loss' if val<0 else 'break-even')
        parts.append(rf'''\textbf{{$Y_{i}$: {name}.}}
\[
\begin{{aligned}}
\ExpectedValue{{\mathbb E}}[\Money{{Y_{i}}}]&=\sum_{{k=0}}^{n}({expr(a,b,'k')})q_k\\
&={a}{'+' if b>0 else '-'}{abs(b)}\left({frac(n*p)}\right)\\
&=\ExpectedValue{{{frac(val)}\ \text{{USD}}}}.
\end{{aligned}}
\]
This is \ExpectedValue{{{interp}}} per {d['period']}: a long-run average, with negative values denoting a net loss.''')
    s+=pair(parts)
    s+=r'\paragraph{2. Expectation formulas and sign intervals.}'+'\n'
    s+=rf'''Keep $n={n}$, the trial definition and all $a_i,b_i$ fixed; vary only $p\in[0,1]$.
Since $\sum q_k=1$ and $\sum kq_k=np$,
\[
\ExpectedValue{{\mathbb E}}[\Money{{Y_i}}]=\sum_{{k=0}}^{n}(a_i+b_i k)q_k
=a_i\sum q_k+b_i\sum kq_k=a_i+b_i np.
\]
'''
    parts=[]
    for i,(name,a,b) in enumerate(alts,1):
        slope=b*n; root=F(-a,slope); rt=frac(root)
        pos=rf'\left({rt},1\right]' if b>0 else rf'\left[0,{rt}\right)'
        neg=rf'\left[0,{rt}\right)' if b>0 else rf'\left({rt},1\right]'
        parts.append(rf'''\textbf{{$Y_{i}$: {name}.}}
\[
\begin{{aligned}}
\ExpectedValue{{\mathbb E}}[\Money{{Y_{i}}}]&={a}+({b})({n})p\\
&={expr(a,slope,'p')}\quad\text{{USD}},\\
\mathbb E[Y_{i}]=0&\iff {slope}p={-a}\\
&\iff \SuccessProb{{p_{i}^*}}=\SuccessProb{{{rt}}}.
\end{{aligned}}
\]
\[
\begin{{aligned}}
\mathbb E[Y_{i}]>0&\iff {slope}p>{-a}\\
&\iff p{'>' if b>0 else '<'}{rt}\\
&\iff p\in {pos},\\
\mathbb E[Y_{i}]<0&\iff {slope}p<{-a}\\
&\iff p{'<' if b>0 else '>'}{rt}\\
&\iff p\in {neg}.
\end{{aligned}}
\]
'''+('Dividing by the negative slope reverses both inequalities. ' if b<0 else '')+rf'At $p={rt}$, the expectation is zero: break-even.')
    s+=pair(parts)
    s+='Positive expectation means expected net gain; negative means expected net loss. Equality concerns average money, not the probability of success or loss.\n'
    s+=r'\clearpage\paragraph{3. Individual graphs and checks.}'+'\n'
    for i,(name,a,b) in enumerate(alts,1):
        root=F(-a,b*n); rt=frac(root); rg=str(root.numerator)+'/'+str(root.denominator)
        if i==3: s+=r'\clearpage'+'\n'
        s+=rf'''\textbf{{$Y_{i}$: {name}.}}
\begin{{center}}\BreakEvenGraph{{{i}}}{{{a}}}{{{a+b*n}}}{{{rg}}}\end{{center}}
The endpoints are $(0,{a})$ and $(1,{a+b*n})$: $\mathbb E[Y_{i}](0)=f_{i}(0)={a}$ and
$\mathbb E[Y_{i}](1)=f_{i}({n})={a+b*n}$ USD.
The exact root check is ${a}+({b*n})({rt})=0$.
\par\medskip
'''
    s+=rf'''Each period realizes one of the listed count-based payoffs, not necessarily the expectation.
Expected profit is an average in USD; probability of loss is a unitless chance of $Y_i<0$.
Both strictly negative and strictly positive outcomes retain positive probability at each interior break-even value.
All alternatives share $X$; separate graphs do not imply independent monetary outcomes.
\secInicio[{label}][{stage}]
'''
    if key in ('inventory','restaurant','agriculture'):
        s=s.replace(r'\subsubsection*{Task 1 --- Worked solution}',r'\clearpage\subsubsection*{Task 1 --- Worked solution}')
    return s

notation=r'''
\clearpage
\section{Notation Reference and Practice Procedure}\label{sec:notation-and-procedure}
\subsection*{Detailed notation reference}\phantomsection\label{tab:notation-reference}
\begingroup\small
\HighlightDetailedTable{
$\HLMathEvent{E_j,E_j^c}$ & \HLMathEvent{Trial success; failure} & Complementary events for one specified trial, not events about the aggregate count. &
\textbullet\ \hyperref[ex:intro-one]{Example 1}: one slot meets/falls below its attendance target.\par
\textbullet\ \hyperref[ex:intro-two]{Example 2}: one session has/has no home-internet disruption.\\[4pt]
$\Indicator{B_j}$; $\Count{X,k}$ & \Count{Indicator; success count} & Independent $B_j\sim\operatorname{Bernoulli}(p)$; $X=\sum B_j\sim\operatorname{Bin}(n,p)$. $k$ is an integer possible count; $B_j$ is only 0 or 1. &
\textbullet\ \hyperref[ex:intro-one]{Example 1}: $X$ counts high-demand slots.\par
\textbullet\ \hyperref[ex:intro-two]{Example 2}: $X$ counts disrupted sessions.\\[4pt]
$\TrialCount{n}$ & \TrialCount{Fixed trial count} & Chosen before results; all trials are observed, with $n>1$. &
\textbullet\ \hyperref[ex:intro-one]{Example 1}: $\TrialCount{4}$ slots per weekend.\par
\textbullet\ \hyperref[ex:intro-two]{Example 2}: $\TrialCount{3}$ sessions per day.\\[4pt]
$\SuccessProb{p}$; $\FailureProb{1-p}$ & \SuccessProb{Success}; \FailureProb{failure probability} & Constant, unitless per-trial probabilities. $0\leq p\leq1$. Independence concerns the trials. &
\textbullet\ \hyperref[ex:intro-one]{Example 1}: $\SuccessProb{2/5}$ and $\FailureProb{3/5}$.\par
\textbullet\ \hyperref[ex:intro-two]{Example 2}: $\SuccessProb{1/10}$ and $\FailureProb{9/10}$.\\[4pt]
$\binom nk$; $\sum$ & Arrangements; summation & $\binom nk=n!/[k!(n-k)!]$ counts orders; $\sum$ adds terms over the displayed integer endpoints. &
\textbullet\ \hyperref[ex:intro-one]{Example 1}: $\binom42=6$ orders of two high-demand slots.\par
\textbullet\ \hyperref[ex:intro-two]{Example 2}: add disruption-count masses for a cumulative event.\\[4pt]
$\Count{S_X}$; $\Money{S_{Y_i}}$ & Positive-mass support & $S_Z=\{z:P(Z=z)>0\}$. For $0<p<1$, all counts $0,\ldots,n$ and their distinct affine images occur. At $p=0,1$, supports shrink to one value. &
\textbullet\ \hyperref[ex:intro-one]{Example 1}: counts $0,1,2,3,4$; $Y_1$ values $-20,0,20,40,60$ USD initially.\par
\textbullet\ \hyperref[ex:intro-two]{Example 2}: counts $0,1,2,3$; $Y_1$ values $-20,20,60,100$ USD initially.\\[4pt]
$\TransformationFunction{f_i}$; $\Money{Y_i}$ & \TransformationFunction{Transformation}; \Money{monetary variable} & $f_i:\{0,\ldots,n\}\to\mathbb R$, $Y_i=f_i(X)=a_i+b_iX$, $b_i\ne0$. All alternatives use the same $X$ and need not be independent. &
\textbullet\ \hyperref[ex:intro-one]{Example 1}: $Y_1=-20+20X$, $Y_2=-40+40X$.\par
\textbullet\ \hyperref[ex:intro-two]{Example 2}: $Y_1=100-40X$, $Y_2=60-25X$ (USD).\\[4pt]
$\Money{a_i,b_i}$ & \Money{Baseline; change per success} & $a_i=f_i(0)$ in USD; $b_i$ in USD/success. Endpoint $f_i(n)=a_i+b_in$ is different from $f_i(1)$. &
\textbullet\ \hyperref[ex:intro-one]{Example 1}: small batch costs 20 USD fixed, earns 20 extra USD per high-demand slot.\par
\textbullet\ \hyperref[ex:intro-two]{Example 2}: home-only baseline 100 USD, reduced by 40 USD per disruption.\\[4pt]
$\HLProbability{q_k,m_{Y_i}(y)}$ & \HLProbability{PMF} & $q_k=\binom nk p^k(1-p)^{n-k}$; $m_{Y_i}(f_i(k))=q_k$, zero elsewhere. PMFs give discrete masses, not densities. &
\textbullet\ \hyperref[ex:intro-one]{Example 1}: $q_2=216/625$; $Y_1=20$ has this mass.\par
\textbullet\ \hyperref[ex:intro-two]{Example 2}: $q_3=1/1000$; $Y_1=-20$ has this mass.\\[4pt]
$\HLCumulativeProbability{F_Z(t)}$ & \HLCumulativeProbability{CDF} & $F_Z(t)=P(Z\leq t)$ for real $t$. Accumulate masses in numerical value order, including each threshold. &
\textbullet\ \hyperref[ex:intro-one]{Example 1}: $F_{Y_1}(0)=q_0+q_1$.\par
\textbullet\ \hyperref[ex:intro-two]{Example 2}: $F_{Y_1}(20)=q_3+q_2$ (reversed count order).\\[4pt]
$\HLMathEvent{\{Y_i<0\}}$ & \HLMathEvent{Loss event} & A strict monetary condition, translated to integer counts before summing. A zero payoff is excluded. &
\textbullet\ \hyperref[ex:intro-one]{Example 1}: $X<1$, hence $X=0$ for both batches.\par
\textbullet\ \hyperref[ex:intro-two]{Example 2}: $X>5/2$, hence $X=3$ for home only.\\[4pt]
$\ExpectedValue{\mathbb E}[\Money{Y_i}]$ & \ExpectedValue{Expected net profit} & $\mathbb E[X]=np$, $\mathbb E[Y_i]=\sum f_i(k)q_k=a_i+b_inp$, in USD per period. &
\textbullet\ \hyperref[ex:intro-one]{Example 1}: initially \ExpectedValue{12 USD} and \ExpectedValue{24 USD} per weekend.\par
\textbullet\ \hyperref[ex:intro-two]{Example 2}: initially \ExpectedValue{88 USD} and \ExpectedValue{52.5 USD} per day.\\[4pt]
$\SuccessProb{p_i^*}$ & \SuccessProb{Individual break-even probability} & $p_i^*=-a_i/(b_in)$ makes only alternative $i$'s expectation zero. With opposite-sign endpoint payoffs it lies strictly inside $[0,1]$. &
\textbullet\ \hyperref[ex:intro-one]{Example 1}: both roots $\SuccessProb{1/4}$.\par
\textbullet\ \hyperref[ex:intro-two]{Example 2}: roots $\SuccessProb{5/6}$ and $\SuccessProb{4/5}$.\\[4pt]
}\endgroup
\clearpage\subsection{Reusable practice procedure}
\textbf{Task 1 --- Establish the binomial model and monetary transformations.}
\begin{enumerate}
\item Define the period, one trial, success $E_j$ and failure $E_j^c$. Check fixed $n$, binary outcomes, independence and constant $p$; define $B_j$ and $X=\sum B_j$.
\item Derive $Y_i=a_i+b_iX$ from fixed costs or baseline receipts and money per success. Use positive-mass supports. Give the full count PMF, zero elsewhere, and its real-threshold CDF.
\item Derive each monetary distribution by mapping every count to its payoff. Sort values numerically for CDFs; a decreasing rule reverses count order. At $p=0$, only $f_i(0)$ remains; at $p=1$, only $f_i(n)$ remains.
\item Substitute $p_0$ for initial masses. Exact $k$ uses $q_k$; at most integer $b$ uses $F_X(b)$; at least integer $a$ uses $1-F_X(a-1)$; an inclusive interval uses $F_X(b)-F_X(a-1)$. Translate $Y_i<0$ before adding masses.
\end{enumerate}
For $b_i>0$, loss means $X<-a_i/b_i$, hence $X\leq\lceil-a_i/b_i\rceil-1$.
For $b_i<0$, loss means $X>-a_i/b_i$, hence $X\geq\lfloor-a_i/b_i\rfloor+1$.
Intersect these events with $0\leq X\leq n$. Strict inequalities exclude zero payoffs.

\textbf{Task 2 --- Individual expected values.}
\begin{enumerate}
\item Calculate every initial $\sum f_i(k)q_k=a_i+b_inp_0$ before varying $p$; interpret the sign and units.
\item Keep $n,a_i,b_i$ fixed. Derive $\mathbb E[X]=np$ from the indicators or distribution, then $\mathbb E[Y_i]=a_i+b_inp$. Solve its zero equation and both strict sign inequalities on $[0,1]$.
\item For each alternative draw its own line joining $(0,f_i(0))$ to $(1,f_i(n))$, with the zero line and exact root. Substitute the root and both endpoints to check.
\end{enumerate}
For an increasing expectation, gain occurs on $(p_i^*,1]$ and loss on $[0,p_i^*)$.
For a decreasing expectation these intervals reverse. Division by a negative slope reverses inequalities.
At equality the expectation is zero, while realized payoffs remain uncertain.
Probability of loss and expected net profit are different quantities: the former measures the chance of negative outcomes; the latter weights all payoffs by their probabilities.
\secInicio[][sec:t2-c4-introduction]
'''

s=pre+front
for d in DATA[:2]: s+=scenario(d,'sec:t2-c4-introduction',True)
s+=notation
s+=r'\clearpage\section{General Worked Problems}\label{sec:t2-c4-general}\label{sec:t2-c4-foundational}\label{sec:t2-c4-intermediate}'+'\n'
s+='Each C4 problem verifies a fixed-trial binomial model, calculates exact and cumulative probabilities, then analyses each monetary expectation separately.\n'
s+='\\SectionProblemsTableOfContents{'+('\\\\\n'.join(rf'\SectionProblemLink{{{d["label"]}}}{{{d["title"]}}}' for d in DATA[2:6]))+'}\n'
for d in DATA[2:6]: s+=scenario(d,'sec:t2-c4-general')
s+=r'\clearpage\section{Advanced Problems}\label{sec:t2-c4-advanced}'+'\n'
s+="Coordinate three monetary transformations of one fixed count. Preserve each alternative's own zero threshold.\n"
s+='\\SectionProblemsTableOfContents{'+('\\\\\n'.join(rf'\SectionProblemLink{{{d["label"]}}}{{{d["title"]}}}' for d in DATA[6:]))+'}\n'
for d in DATA[6:]: s+=scenario(d,'sec:t2-c4-advanced')
s+=r'''
\subsection*{Key ideas and common errors}
A trial event and an aggregate count event are different. Fix $n$ before observation;
do not stop after success. Verify independence and constant $p$, rather than inferring them from separate customers.
For example, if all five concert ticket groups react to one common publicity shock, their outcomes may be dependent;
the same binomial PMF is then unjustified. Enrollment responses sampled without replacement from a small fixed pool can also violate independence and constant probability.
Count mathematical successes even when they cause monetary losses. The combination coefficient counts all arrangements.
Use complete PMFs, positive-mass supports and ordered, right-continuous CDFs.
The complement of at least $k$ ends at $k-1$; strict losses exclude zero money.
Hold $n$ and payoff rules fixed when varying $p$. Each expectation has its own zero threshold;
an intersection of alternatives does not answer an individual break-even question.
Expected profit does not guarantee realized profit and does not equal the probability of avoiding loss.
\secInicio[][sec:t2-c4-advanced]
\end{document}
'''
OUT.write_text(s,encoding='utf-8')
(Path(__file__).parent/'data.json').write_text(json.dumps(DATA,default=str,indent=2),encoding='utf-8')
print(f'Wrote {OUT}: {len(s.splitlines())} lines')
