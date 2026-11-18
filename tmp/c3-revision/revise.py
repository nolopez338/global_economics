from pathlib import Path
from fractions import Fraction as Q
root=Path.cwd()
target=root/'book2026-2027/grade10/term_2/1-practice_activities/G10_T2_L1_C3_practice_activity.tex'
original=(root/'tmp/c3-revision/original.tex').read_text(encoding='utf-8')
head=original.split(r'\section{Introduction}')[0]
head=head.replace('Bernoulli Indicators and Financial Consequences','Bernoulli Models and Economic Decisions')
head=head.replace('round final probabilities to four decimal places. Monetary amounts are in USD.','use exact thresholds for decisions and decimals only as approximations. Monetary amounts are in USD.\nAll decisions maximize expected net profit; negative payoffs are net losses.')
head=head.replace(r'\begin{document}',r'''% The reference EMVGraph fixes the vertical range at [-25,85]; local axes
% below retain its two-state line-graph approach with context-specific scales.
\pgfplotsset{decisionone/.style={black,solid,thick},
 decisiontwo/.style={black,dashed,thick},decisionthree/.style={black,dashdotted,thick}}
\begin{document}''')
intro=r'''
\section{Introduction}\label{sec:t2-c3-introduction}
\subsection*{Highlight legend}
\phantomsection\label{tab:highlight-legend}
\begin{tabularx}{\linewidth}{@{}p{.25\linewidth}p{.25\linewidth}X@{}}
\toprule
\textbf{Symbol or notation}&\textbf{Concept}&\textbf{Brief meaning}\\\midrule
$\Indicator{X}$ & \Indicator{Indicator} & Unitless label of an event: 0 or 1.\\
$\SuccessProb{p}=P(X=1)$ & \SuccessProb{Success probability} & Chance of the state labelled 1.\\
$\FailureProb{1-p}=P(X=0)$ & \FailureProb{Failure probability} & Chance of the complementary state.\\
$\Money{Y}=f(\Indicator{X})$ & \Money{Monetary consequence} & State-dependent amount, in USD.\\
$\Money{Y_i}=f_i(\Indicator{X})$ & \Money{Alternative payoff} & Monetary consequence of decision $A_i$.\\
\bottomrule
\end{tabularx}

The two probability treatments distinguish an event from its complement within
the same model. Labels and units preserve meaning without color.
See the \hyperref[tab:notation-reference]{detailed notation reference}.

\subsection{Introductory example 1: clothing inventory}\label{ex:intro-one}
Observe one shop's demand over one weekend. Let $E$ be high demand and define
$\Indicator{X}=\Indicator{1}$ for $E$, $\Indicator{X}=\Indicator{0}$ for low demand.
These are the only two states in this simplified model. With
$\SuccessProb{p}=\SuccessProb{0.4}$, low demand has probability
$\FailureProb{1-p}=\FailureProb{0.6}$.
The \Indicator{indicator} has no units; it does not measure sales or profit.

First write $\Money{Y}=f(\Indicator{X})$. For a small stock order,
$f(0)=\Money{20}$ and $f(1)=\Money{60}$ USD, so
$\Money{Y}=f(\Indicator{X})=\Money{20}+\Money{40}\Indicator{X}$ USD.
A larger order has $f_2(0)=-20$, $f_2(1)=120$, hence
$Y_2=f_2(X)=-20+140X$ USD; call the small order $A_1$ and $Y_1=Y$.
The monetary loss event $\{Y_2<0\}=\{X=0\}$ has probability 0.6.
Task 1 describes these distributions. Task 2 holds both payoff rules fixed:
$\mathbb E[Y_1]=20+40p$ and $\mathbb E[Y_2]=-20+140p$ USD.
They tie at $p=2/5$; the small order is preferred below this threshold and
the larger order above it. At the stated $p=0.4$, both have expected profit 36 USD.

\subsection{Introductory example 2: coffee-shop disruption}\label{ex:intro-two}
Observe one coffee shop over one day. Let $E$ be an equipment disruption:
$\Indicator{X}=\Indicator{1}$ if it occurs and $\Indicator{X}=\Indicator{0}$ otherwise.
Suppose $\SuccessProb{p}=\SuccessProb{0.1}$ and
$\FailureProb{1-p}=\FailureProb{0.9}$. Mathematical success can be financially undesirable.
Without backup, the monetary consequence is $\Money{Y_1}=f_1(\Indicator{X})$,
where $f_1(0)=\Money{100}$ and $f_1(1)=\Money{-20}$ USD:
$Y_1=f_1(X)=100-120X$ USD. A backup contract gives
$Y_2=f_2(X)=60$ USD in either state.
Thus $S_{Y_1}=\{y\in\mathbb R:P(Y_1=y)>0\}=\{-20,100\}$,
whereas $S_{Y_2}=\{y\in\mathbb R:P(Y_2=y)>0\}=\{60\}$.
Both state masses combine at 60 USD for $Y_2$.
The CDF for $Y_1$ jumps by 0.1 at $-20$ and by 0.9 at 100: order money
numerically, not by the labels of $X$.
Expected profits are $100-120p$ and 60 USD, tying at $p=1/3$.
At $p=0.1$ choose no backup (88 versus 60 USD); above $1/3$ choose backup.

\subsection{Binary models and distributions}
One observation in a stated period gives two mutually exclusive and exhaustive
states. Write $X\sim\operatorname{Bernoulli}(p)$, $0\leq p\leq1$.
The support is a set of numerical values with \emph{positive} probability:
\[
 S_X=\{x\in\mathbb R:P(X=x)>0\}
 =\begin{cases}\{0,1\},&0<p<1,\\\{0\},&p=0,\\\{1\},&p=1.\end{cases}
\]
An event such as $\{Y_i<0\}$ is a condition on the observation; it is not a support.
These discrete variables have probability mass functions (PMFs), not ordinary
probability density functions. Their cumulative distribution functions (CDFs)
add masses up to and including a threshold. No separate density is required.
One Bernoulli observation requires no independence assumption across trials.

\section{Notation Reference and Practice Procedure}\label{sec:t2-c3-notation}
\subsection*{Detailed notation reference}
\phantomsection\label{tab:notation-reference}
\begingroup\small\setlength{\tabcolsep}{4pt}\renewcommand{\arraystretch}{1.25}
\begin{longtable}{@{}p{.18\linewidth}p{.17\linewidth}p{.30\linewidth}p{.29\linewidth}@{}}
\toprule
\textbf{Symbol or notation}&\textbf{Concept}&\textbf{Definition}&\textbf{Meaning in the introductory examples}\\\midrule\endfirsthead
\toprule\textbf{Symbol or notation}&\textbf{Concept}&\textbf{Definition}&\textbf{Meaning in the introductory examples}\\\midrule\endhead
$E$, $E^c$ & Event; complement & Two mutually exclusive, exhaustive states in a stated period. &
\textbullet\ \hyperref[ex:intro-one]{Example 1}: high/low weekend demand.\par
\textbullet\ \hyperref[ex:intro-two]{Example 2}: disruption/no disruption in one day.\\
$\Indicator{X}$ & \Indicator{Indicator} & $X=1$ on $E$, $X=0$ on $E^c$; unitless. &
\textbullet\ \hyperref[ex:intro-one]{Example 1}: $\Indicator{1}$ means high demand.\par
\textbullet\ \hyperref[ex:intro-two]{Example 2}: $\Indicator{1}$ means disruption.\\
$\SuccessProb{p}$ & \SuccessProb{Success probability} & $p=P(X=1)=P(E)$, with $0\leq p\leq1$. &
\textbullet\ \hyperref[ex:intro-one]{Example 1}: $\SuccessProb{0.4}$.\par
\textbullet\ \hyperref[ex:intro-two]{Example 2}: $\SuccessProb{0.1}$.\\
$\FailureProb{1-p}$ & \FailureProb{Failure probability} & $P(X=0)=P(E^c)$; masses total 1. &
\textbullet\ \hyperref[ex:intro-one]{Example 1}: $\FailureProb{0.6}$.\par
\textbullet\ \hyperref[ex:intro-two]{Example 2}: $\FailureProb{0.9}$.\\
$\Money{Y}=f(\Indicator{X})$; $\Money{Y_i}=f_i(\Indicator{X})$ & \Money{Monetary consequence} & $f(0)=y_0$, $f(1)=y_1$; $Y=y_0+(y_1-y_0)X$. Units belong to money, not $X$. &
\textbullet\ \hyperref[ex:intro-one]{Example 1}: $\Money{Y_1}=f_1(X)=20+40X$ USD.\par
\textbullet\ \hyperref[ex:intro-two]{Example 2}: $\Money{Y_1}=f_1(X)=100-120X$ USD.\\
$S_X$, $S_{Y_i}$ & Support & $S_X=\{x\in\mathbb R:P(X=x)>0\}$; $S_{Y_i}=\{y\in\mathbb R:P(Y_i=y)>0\}$. &
\textbullet\ \hyperref[ex:intro-one]{Example 1}: $S_X=\{0,1\}$, $S_{Y_1}=\{20,60\}$.\par
\textbullet\ \hyperref[ex:intro-two]{Example 2}: $S_{Y_2}=\{60\}$.\\
$m_X(x)$, $m_{Y_i}(y)$ & PMF & $m_X(x)=P(X=x)$; $m_{Y_i}(y)=P(Y_i=y)$, zero outside possible values. &
\textbullet\ \hyperref[ex:intro-two]{Example 2}: $m_{Y_1}(-20)=0.1$; $m_{Y_2}(60)=1$.\\
$F_X(t)$, $F_{Y_i}(t)$ & CDF & $F_X(t)=P(X\leq t)$; $F_{Y_i}(t)=P(Y_i\leq t)$. Right-continuous step functions. &
\textbullet\ \hyperref[ex:intro-two]{Example 2}: $F_{Y_1}(0)=0.1$. Threshold $t$ is in USD for money.\\
$\{Y_i<0\}$ & Monetary event & Evaluate $f_i(0)$ and $f_i(1)$ to find the corresponding indicator event. &
\textbullet\ \hyperref[ex:intro-one]{Example 1}: $\{Y_2<0\}=\{X=0\}$.\\
$\mathbb E[Y_i]$ & Expected monetary value & $p f_i(1)+(1-p)f_i(0)$; in USD. &
\textbullet\ \hyperref[ex:intro-one]{Example 1}: $\mathbb E[Y_1]=20+40p$ USD.\\
$p^*$ & Indifference threshold & Solve $\mathbb E[Y_i]=\mathbb E[Y_j]$; compare all alternatives at and between intersections. &
\textbullet\ \hyperref[ex:intro-two]{Example 2}: $p^*=1/3$ changes the recommendation.\\
\bottomrule
\end{longtable}\endgroup
Here $f_i$ transforms states into money; $m_{Y_i}$ assigns probabilities to
monetary values and $F_{Y_i}$ accumulates them. These are different functions.

\subsection{Reusable practice procedure}
\textbf{Task 1 --- Establish the binary model and monetary transformations.}
\begin{enumerate}
\item Identify one observation, its period, the two states and event $E$.
Define $X=1$ on $E$ and $X=0$ otherwise; retain this definition for every alternative.
\item State $p=P(X=1)$ and $1-p=P(X=0)$. Give $S_X$ in set-builder notation
and evaluate it. Use direct masses at $p=0,1$, avoiding $0^0$.
\item Write the complete PMF and piecewise CDF:
\[
m_X(x)=\begin{cases}1-p,&x=0,\\p,&x=1,\\0,&x\notin\{0,1\},\end{cases}
\qquad
F_X(t)=\begin{cases}0,&t<0,\\1-p,&0\leq t<1,\\1,&t\geq1.\end{cases}
\]
\item For each $A_i$, first write $Y_i=f_i(X)$ in the stated monetary units,
then $f_i(0)=y_{i0}$, $f_i(1)=y_{i1}$ and
$Y_i=f_i(X)=y_{i0}+(y_{i1}-y_{i0})X$.
\item Give $S_{Y_i}=\{y\in\mathbb R:P(Y_i=y)>0\}$ and evaluate it.
For distinct payoffs and $0<p<1$ this is $\{y_{i0},y_{i1}\}$;
at $p=0$ it is $\{y_{i0}\}$ and at $p=1$ it is $\{y_{i1}\}$.
If payoffs coincide, combine masses into one value for every $p$.
\item Give each monetary PMF, zero elsewhere. Sort distinct amounts
$a<b$ and let $q=P(Y_i=a)$; then
\[
F_{Y_i}(t)=\begin{cases}0,&t<a,\\q,&a\leq t<b,\\1,&t\geq b.\end{cases}
\]
Here $q=1-p$ if $a=f_i(0)$, but $q=p$ if $a=f_i(1)$.
If $a=b=c$, the CDF is 0 for $t<c$ and 1 for $t\geq c$.
At endpoints, zero-mass potential values create no jump.
\item Translate monetary events into events involving $X$ and add the
appropriate masses. Check units, signs, total mass 1 and right continuity.
\end{enumerate}
\textbf{Task 2 --- Perform sensitivity analysis on $p$ and make a decision.}
\begin{enumerate}
\item Keep the same two states and fixed monetary rules; vary only $p\in[0,1]$.
Calculate and simplify $\mathbb E[Y_i]=p f_i(1)+(1-p)f_i(0)$.
\item Construct an extended payoff table and graph expected monetary value
against $p$. Each line joins $f_i(0)$ at $p=0$ to $f_i(1)$ at $p=1$.
\item Solve every pairwise equality exactly. Discard intersections outside
$[0,1]$ for decisions; within the interval compare all lines, since an intersection
below the greatest expected value does not change the preferred alternative.
\item State the maximizing decision on every interval, including endpoints
and optimal ties. Interpret slopes, thresholds and the recommendation at the given $p$.
\end{enumerate}
\secInicio[][sec:t2-c3-introduction]
'''

data=[
dict(key='inventory',title='Clothing inventory for one weekend',obs="one clothing shop's net profit over one weekend",event='high demand',other='low demand',p=Q(2,5),alts=[('small order',40,80),('large order',-20,180)],rule=r'$A_1$ for $0\leq p<3/8$; $A_1,A_2$ tie at $p=3/8$; $A_2$ for $3/8<p\leq1$.',why='The large order has a steeper profit line: high demand compensates for its low-demand loss only above $3/8$.',check=r'At $p=2/5$, expected profits are 56 and 60 USD, so choose the large order.'),
dict(key='coffee',title='Coffee-shop service strategy',obs="one coffee shop's net profit over one day",event='a busy day',other='a quiet day',p=Q(1,2),alts=[('seated service',40,100),('quiet-day workshops',100,20)],rule=r'$A_2$ for $0\leq p<3/7$; $A_1,A_2$ tie at $p=3/7$; $A_1$ for $3/7<p\leq1$.',why='Workshops lose bookings when the shop is busy. Their expected profit falls as $p$ rises, whereas seated service benefits.',check=r'At $p=1/2$, expected profits are 70 and 60 USD; choose seated service. For $Y_2$, the smaller amount belongs to $X=1$.'),
dict(key='energy',title='Renewable-energy sales contract',obs="one small solar producer's net profit over one month",event='a sunny month',other='a cloudy month',p=Q(1,4),alts=[('market sales',30,90),('fixed contract',60,60)],rule=r'$A_2$ for $0\leq p<1/2$; $A_1,A_2$ tie at $p=1/2$; $A_1$ for $1/2<p\leq1$.',why='The contract fixes net profit in both states. Market sales gain 60 USD in expected profit for a unit increase in $p$.',check=r'At $p=1/4$, expected profits are 45 and 60 USD; choose the fixed contract. It has one monetary support value even though $X$ has two.'),
dict(key='manufacturing',title='Manufacturing capacity investment',obs="one manufacturer's net profit over one quarter",event='a large order arrives',other='no large order arrives',p=Q(3,5),alts=[('existing equipment',100,200),('capacity investment',-100,500)],rule=r'$A_1$ for $0\leq p<1/2$; $A_1,A_2$ tie at $p=1/2$; $A_2$ for $1/2<p\leq1$.',why='Investment has a low-state loss but a larger response to the order probability. Its 200 USD low-state disadvantage is offset when $400p>200$.',check=r'At $p=3/5$, expected profits are 160 and 260 USD; choose capacity investment.'),
dict(key='restaurant',title='Restaurant capacity: three alternatives, two states',obs="one restaurant's net profit over one evening",event='high demand',other='low demand',p=Q(9,25),alts=[('small room',80,100),('medium room',20,220),('large room',-100,400)],rule=r'$A_1$ for $0\leq p<1/3$; $A_1,A_2$ tie at $p=1/3$; $A_2$ for $1/3<p<2/5$; $A_2,A_3$ tie at $p=2/5$; $A_3$ for $2/5<p\leq1$.',why=r'The $A_1,A_3$ intersection at $3/8$ is not a decision threshold: both yield $175/2$ USD, below $A_2$ at 95 USD. Only $1/3$ and $2/5$ change the maximizing decision.',check=r'At $p=9/25=0.36$, expected profits are $436/5=87.2$, 92 and 80 USD; choose the medium room.'),
dict(key='agriculture',title='Agricultural planting: a dominated alternative',obs="one farm plot's net profit over one growing season",event='favorable weather',other='unfavorable weather',p=Q(1,2),alts=[('hardy crop',70,90),('high-yield crop',30,190),('specialty crop',10,150)],rule=r'$A_1$ for $0\leq p<2/7$; $A_1,A_2$ tie at $p=2/7$; $A_2$ for $2/7<p\leq1$. Alternative $A_3$ is never optimal.',why=r'$A_2$ exceeds $A_3$ in both states: the expected-value difference is $20+20p>0$ throughout $[0,1]$. The $A_1,A_3$ tie at $1/2$ is below $A_2$ (80 versus 110 USD). Their tie does not change the decision.',check=r'At $p=1/2$, expected profits are 80, 110 and 80 USD; choose the high-yield crop. There are three decisions, but only two weather states.')
]
data[3]['rule']=r'$A_1$ for $0\leq p<2/5$; $A_1,A_2$ tie at $p=2/5$; $A_2$ for $2/5<p\leq1$.'
data[3]['why']='Investment has a low-state loss but a larger response to the order probability. Its 200 USD low-state disadvantage is offset when $500p>200$.'
def frac(v):
 v=Q(v)
 return str(v.numerator) if v.denominator==1 else (('-' if v<0 else '')+r'\frac{'+str(abs(v.numerator))+'}{'+str(v.denominator)+'}')
def affine(a,b,var='p'):
 d=b-a
 return str(a) if d==0 else str(a)+('+' if d>0 else '-')+str(abs(d))+var
intro=intro.replace(r'& \Money{Monetary consequence} & $f(0)',r'& \Money{Monetary}\par\Money{consequence} & $f(0)')
intro=intro.replace(r'S_X=\{x\in\mathbb R:P(X=x)>0\}',r'S_X=\{x\in\mathbb R:P(X=x)>0\}',1)
intro=intro.replace('An event such as',r'For a monetary consequence, $S_Y=\{y\in\mathbb R:P(Y=y)>0\}$.\nAn event such as'.replace(r'\n','\n'))
intro=intro.replace(r'\section{Notation Reference',r'\clearpage\section{Notation Reference')
intro=intro.replace(r'@{}p{.18\linewidth}p{.17\linewidth}p{.30\linewidth}p{.29\linewidth}@{}',r'@{}>{\raggedright\arraybackslash}p{.18\linewidth}>{\raggedright\arraybackslash}p{.17\linewidth}>{\raggedright\arraybackslash}p{.30\linewidth}>{\raggedright\arraybackslash}p{.29\linewidth}@{}')
parts=[head,intro]
for advanced, groupdata in [(False,data[:4]),(True,data[4:])]:
 group='sec:t2-c3-'+('advanced' if advanced else 'general')
 parts.append(r'\clearpage'+'\n'+r'\section{'+('Advanced Problems' if advanced else 'General Worked Problems')+r'}\label{'+group+'}\n')
 parts.append('Each problem applies C3 through a single Bernoulli model, then uses it for an expected-net-profit decision.\n')
 parts.append(r'\SectionProblemsTableOfContents{'+'\\\\\n'.join(r'\SectionProblemLink{prob:c3-'+d['key']+'}{'+d['title']+'}' for d in groupdata)+'}\n')
 for di,d in enumerate(groupdata):
  k=d['key']; p=d['p']; alts=d['alts']; n=len(alts)
  if di: parts.append(r'\clearpage'+'\n')
  parts.append(r'\subsection{'+d['title']+r'}\label{prob:c3-'+k+'}\n')
  parts.append('Observe '+d['obs']+'. The two possible states are '+d['event']+' and '+d['other']+'. The initial probability of '+d['event']+' is $p='+frac(p)+'$. All entries below are net profits in USD for the entire stated period, including relevant costs.\n')
  parts.append(r'\begin{center}\begin{tabular}{lrr}\toprule Alternative & '+d['other']+' & '+d['event']+r'\\\midrule'+'\n')
  for i,(name,a,b) in enumerate(alts,1): parts.append(f'$A_{i}$: {name} & {a} & {b}'+r'\\'+'\n')
  parts.append(r'\bottomrule\end{tabular}\end{center}'+'\n')
  parts.append(r'\QuestionsTasks['+group+']{\n'+r'{3}/{sol:c3-'+k+r'-model}/{\textbf{Task 1 --- Establish the binary model and monetary transformations.} Identify the observation, period, two states and event $E$; define a common $X$ and both masses. Give the set-builder support of $X$, its complete PMF and piecewise CDF. For every alternative define $Y_i=f_i(X)$ with USD units and both state values; give its set-builder support, complete PMF and numerically ordered piecewise CDF. Translate $\{Y_i<0\}$ into an event involving $X$ and calculate its probability. Explain supports at $p=0,1$ and combine any equal payoffs.},'+'\n'+r'{3}/{sol:c3-'+k+r'-decision}/{\textbf{Task 2 --- Perform sensitivity analysis on $p$ and make a decision.} Retain Task 1 states and payoff rules. Vary $p$ over $[0,1]$; calculate and simplify every expected monetary value. Give an extended payoff table and graph. Find all exact pairwise indifference probabilities, identify the intersections that change the preferred decision, and state the maximizing alternative on all intervals, endpoints and optimal ties. Interpret changes in $p$ and recommend an alternative at the initial probability.}'+'\n}\n')
  parts.append(r'\subsubsection*{Task 1 --- Worked solution}\label{sol:c3-'+k+'-model}\n')
  parts.append('The observation is '+d['obs']+'. Let $E$ be '+d['event']+'; $E^c$ is '+d['other']+'. Exactly one state occurs. Define $\Indicator{X}=\Indicator{1}$ on $E$ and $\Indicator{X}=\Indicator{0}$ on $E^c$. This unitless indicator is Bernoulli, with\n'+r'\[P(X=1)=\SuccessProb{p}=\SuccessProb{'+frac(p)+r'},\qquad P(X=0)=\FailureProb{1-p}=\FailureProb{'+frac(1-p)+r'}.\]'+'\n')
  parts.append(r'\[S_X=\{x\in\mathbb R:P(X=x)>0\}=\{0,1\}\quad\text{at the initial probability}.\]'+'\n')
  parts.append(r'\[m_X(x)=\begin{cases}1-p,&x=0,\\p,&x=1,\\0,&x\notin\{0,1\},\end{cases}\qquad F_X(t)=P(X\leq t)=\begin{cases}0,&t<0,\\1-p,&0\leq t<1,\\1,&t\geq1.\end{cases}\]'+'\n')
  parts.append('These formulas include endpoints: $S_X=\{0\}$ at $p=0$ and $S_X=\{1\}$ at $p=1$. The initial CDF plateau is $'+frac(1-p)+'$.\n')
  for i,(name,a,b) in enumerate(alts,1):
   lo,hi=sorted([a,b]); lowmass='1-p' if a<b else 'p'; highmass='p' if a<b else '1-p'
   parts.append(r'\needspace{11\baselineskip}\paragraph{'+f'$A_{i}$: {name}.'+'}\n')
   parts.append(f'The \\Money{{monetary consequence}} is $\\Money{{Y_{i}}}=f_{i}(\\Indicator{{X}})$ in USD, with $f_{i}(0)=\\Money{{{a}}}$ and $f_{i}(1)=\\Money{{{b}}}$. Hence\n'+r'\['+f'Y_{i}=f_{i}(X)={a}+({b}-({a}))X='+affine(a,b,'X')+r'\quad\text{USD}.\]'+'\n')
   support=r'\{'+str(lo)+((','+str(hi)) if lo!=hi else '')+r'\}'
   parts.append(r'\[S_{Y_'+str(i)+r'}=\{y\in\mathbb R:P(Y_'+str(i)+'=y)>0\}='+support+r'\quad\text{at the initial probability}.\]'+'\n')
   if a!=b:
    parts.append(r'\[m_{Y_'+str(i)+r'}(y)=\begin{cases}'+lowmass+f',&y={lo},'+r'\\'+highmass+f',&y={hi},'+r'\\0,&\text{otherwise},\end{cases}\qquad F_{Y_'+str(i)+r'}(t)=\begin{cases}0,&t<'+str(lo)+r',\\'+lowmass+f',&{lo}\leq t<{hi},'+r'\\1,&t\geq '+str(hi)+r'.\end{cases}\]'+'\n')
    parts.append(f'Initially $m_{{Y_{i}}}({lo})='+frac(1-p if a<b else p)+f'$ and $m_{{Y_{i}}}({hi})='+frac(p if a<b else 1-p)+f'$. At $p=0$, $S_{{Y_{i}}}=\\{{{a}\\}}$; at $p=1$, $S_{{Y_{i}}}=\\{{{b}\\}}$. The same PMF and CDF remain valid, with any zero-mass jump absent.\n')
   else:
    parts.append(r'\[m_{Y_'+str(i)+r'}(y)=\begin{cases}1,&y='+str(a)+r',\\0,&y\ne '+str(a)+r',\end{cases}\qquad F_{Y_'+str(i)+r'}(t)=\begin{cases}0,&t<'+str(a)+r',\\1,&t\geq '+str(a)+r'.\end{cases}\]'+'\n')
    parts.append(f'The masses combine: $P(Y_{i}={a})=(1-p)+p=1$. Its support is $\\{{{a}\\}}$ for every $p\\in[0,1]$, including endpoints.\n')
   event=(r'\{X=0\}' if a<0<=b else r'\{X=1\}' if b<0<=a else r'\{X\in\{0,1\}\}' if a<0 and b<0 else r'\{X\notin\{0,1\}\}')
   prob=('1-p' if a<0<=b else 'p' if b<0<=a else '1' if a<0 and b<0 else '0')
   val=(1-p if a<0<=b else p if b<0<=a else 1 if a<0 and b<0 else 0)
   parts.append(f'The net-loss event is $\\{{Y_{i}<0\\}}='+event+f'$, so $P(Y_{i}<0)={prob}$, initially $'+frac(val)+'$.\n')
  parts.append('Each nonconstant monetary PMF totals $(1-p)+p=1$; each constant one has mass 1. The CDFs include each threshold in its upper branch, are nondecreasing and right-continuous, and tend to 0 and 1. Monetary supports contain USD amounts; $S_X$ contains unitless labels.\n'+r'\secInicio[prob:c3-'+k+']['+group+']\n')
  parts.append(r'\clearpage\subsubsection*{Task 2 --- Worked solution}\label{sol:c3-'+k+'-decision}\n')
  parts.append('Keep the event definition and all state payoffs fixed. Only $p=P(E)$ varies over $[0,1]$. For each alternative,\n')
  parts.append(r'\begin{align*}'+'\n')
  for i,(name,a,b) in enumerate(alts,1): parts.append(r'\mathbb E[Y_'+str(i)+f']&=p f_{i}(1)+(1-p)f_{i}(0)=p({b})+(1-p)({a})='+affine(a,b)+r'\quad\text{USD}'+(r'\\' if i<n else '')+'\n')
  parts.append(r'\end{align*}'+'\n'+r'\textbf{Extended payoff table (USD).}\begin{center}\begin{tabular}{lrrl}\toprule Alternative & $X=0$ ($1-p$) & $X=1$ ($p$) & $\mathbb E[Y_i]$\\\midrule'+'\n')
  for i,(name,a,b) in enumerate(alts,1): parts.append(f'$A_{i}$ & $\\Money{{{a}}}$ & $\\Money{{{b}}}$ & $\\Money{{{affine(a,b)}}}$'+r'\\'+'\n')
  parts.append(r'\bottomrule\end{tabular}\end{center}'+'\n')
  parts.append(r'\textbf{Exact pairwise comparisons.}\begin{itemize}'+'\n')
  for i,(_,a,b) in enumerate(alts,1):
   for j,(_,c,e) in enumerate(alts[i:],i+1):
    diff=(b-a)-(e-c); threshold=Q(c-a,diff)
    parts.append(f'\\item $A_{i}$ and $A_{j}$: ${affine(a,b)}={affine(c,e)}$, so $({diff})p={c-a}$ and $p='+frac(threshold)+f'\\approx {float(threshold):.4f}$.'+(' This lies outside $[0,1]$.' if not 0<=threshold<=1 else '')+'\n')
  parts.append(r'\end{itemize}'+'\n')
  parts.append(r'\textbf{Complete decision rule (maximize expected net profit).} '+d['rule']+'\n\n'+d['why']+' '+d['check']+'\n')
  ymin=min(a for _,a,b in alts); ymax=max(b for _,a,b in alts)
  ymin=min(ymin,min(b for _,a,b in alts))-20; ymax=max(ymax,max(a for _,a,b in alts))+25
  parts.append(r'\begin{center}\begin{tikzpicture}\begin{axis}[width=.82\linewidth,height=6.4cm,xmin=0,xmax=1,ymin='+str(ymin)+',ymax='+str(ymax)+r',axis lines=left,xlabel={Probability $p=P(E)$},ylabel={Expected net profit (USD)},grid=major,legend style={at={(.5,1.03)},anchor=south,legend columns=-1},legend cell align=left]'+'\n')
  for i,(_,a,b) in enumerate(alts,1): parts.append(r'\addplot[decision'+['one','two','three'][i-1]+',domain=0:1,samples=2]{'+str(a)+'+'+str(b-a)+r'*x};\addlegendentry{$\mathbb E[Y_'+str(i)+']$}\n')
  parts.append(r'\end{axis}\end{tikzpicture}\end{center}'+'\n')
  parts.append('The solid, dashed'+(' and dash-dotted lines identify $A_1,A_2,A_3$, respectively.' if n==3 else ' lines identify $A_1,A_2$, respectively.')+' Their intercepts and endpoint heights reproduce the state payoffs; the greatest line gives the recommendation. At $p=0$ compare the $X=0$ column; at $p=1$ compare the $X=1$ column.\n'+r'\secInicio[prob:c3-'+k+']['+group+']\n')
parts.append(r'''
\subsection*{Closing reminders: Bernoulli modelling and economic decisions}
Define one event $E$ and keep $X=1$ on $E$ throughout both tasks. The indicator
is unitless; the monetary consequence is $Y=f(X)$, or $Y_i=f_i(X)$ in USD
for alternative $A_i$. Do not confuse the transformation $f_i$ with a PMF or CDF.
Use set-builder supports with positive probability, omit zero-mass values,
and combine equal monetary outcomes. Sort amounts numerically before writing CDFs.
Keep the state payoffs fixed during sensitivity analysis. Maximize expected
net profit, use exact decision thresholds, compare every alternative at an
intersection, and include $p=0,1$ and optimal ties. A high expected value is an
average-based decision criterion, not a guarantee of the realized profit.
\secInicio[][sec:t2-c3-advanced]
\end{document}
''')
target.write_text(''.join(parts),encoding='utf-8')
print('Updated',target)
