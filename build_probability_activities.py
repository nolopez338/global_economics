"""Reproduce the nine fully solved Grade 10 Term 2 probability activities."""
from pathlib import Path
import math

OUT = Path(__file__).resolve().parent / 'book2026-2027/grade10/term_2/1-practice_activities'
OUT.mkdir(parents=True, exist_ok=True)
records = []
def number(tag, value):
    records.append((tag, value))
    return f'{value:.4f}'
def table(headers, rows, spec=None):
    spec = spec or 'l' * len(headers)
    return '\\begin{center}\n\\begin{tabular}{'+spec+'}\n\\toprule\n'+' & '.join(headers)+r' \\ \midrule'+'\n'+'\n'.join(' & '.join(map(str,row))+r' \\' for row in rows)+'\n\\bottomrule\n\\end{tabular}\n\\end{center}\n'
def problem(title, statement, tasks, steps):
    return '\\Needspace{14\\baselineskip}\n\\subsection{'+title+'}\n'+statement+'\n\n\\textbf{Questions/Tasks}\n\\begin{enumerate}\n'+''.join('\\item '+t+'\n' for t in tasks)+'\\end{enumerate}\n\\subsubsection*{Complete worked solution}\n'+''.join('\\par\\noindent\\begin{minipage}{\\linewidth}\n\\textbf{Step '+str(i)+': '+heading+'.} '+body+'\n\\end{minipage}\\par\\medskip\n' for i,(heading,body) in enumerate(steps,1))
def check(q,a):
    return '\\textbf{Check.} '+q+' \\emph{Suggested answer:} '+a+'\n\n'
def reference(rows, procedure):
    return '\\section{Notation reference and practice procedure}\n'+table(['Symbol','Meaning and units'],rows,'lp{0.72\\linewidth}')+'\\begin{enumerate}\n'+''.join('\\item '+x+'\n' for x in procedure)+'\\end{enumerate}\n'
routine = [r'Define the random variable in words and give its units and support.',r'List parameters and check that the model assumptions match the situation.',r'Translate ordinary language into an event, paying attention to endpoints.',r'Write the symbolic formula first, then substitute without rounding intermediate values.',r'Check bounds, total probability or a complementary calculation; interpret the answer in context.']
def write(c,title,criterion,intro,general,bridge,advanced,ref,practice,closing):
    lesson = 1 if c<=4 else 2 if c<=7 else 3
    prefix=f't2-c{c}'
    head=r'''\makeatletter
\def\input@path{{./}{../../../preamble/}{book2026-2027/preamble/}}
\makeatother
\input{preamble.tex}
\usepackage{needspace}
\hypersetup{pdftitle={Grade 10 Term 2 Discrete Probability}}
\setlength{\emergencystretch}{2em}
\title{Grade 10, Term 2, Lesson LESSON, Criterion CNUMBER\\TITLE}
\author{}
\date{}
\begin{document}
\maketitle
\setcounter{tocdepth}{1}
\setcounter{secnumdepth}{2}
\phantomsection\label{toc}
\tableofcontents
\section*{Evaluated criterion}
\textbf{CNUMBER:} CRITERION
\section{Introduction}\label{sec:PREFIX-introduction}
All data in this activity are hypothetical teaching models. Probabilities have no monetary units. Keep exact expressions where useful and round final probabilities to four decimal places.
'''.replace('LESSON',str(lesson)).replace('CNUMBER',f'C{c}').replace('TITLE',title).replace('CRITERION',criterion).replace('PREFIX',prefix)
    inputs={
        1:[('$X$','$0,1,2$','Possible score values'),('$p_X(1)$','$0.2+0.3$','Mass grouped from two outcomes')],
        2:[('$X$','$0,2,5$','Supported score values'),('$p_X(x)$','$0.2,0.5,0.3$','Respective masses; no units')],
        3:[('$p$','$0.3$','Probability of event A'),('$X$','$0$ or $1$','Indicator value; no monetary units')],
        4:[('$n$','$3$ trials','Fixed number of trials'),('$p$','$0.5$','Success probability per trial'),('$k$','$2$ successes','Requested success count')],
        5:[('$p$','$0.5$','Success probability per trial'),('$t$','$3$ trials','Requested first-success trial')],
        6:[('$r$','$2$ successes','Target number of successes'),('$p$','$0.5$','Success probability per trial'),('$t$','$3$ trials','Requested stopping trial')],
        7:[('rate','1 event per unit','Event frequency per exposure unit'),('exposure','1 unit','Observation length'),(r'$\lambda$','1 event','Expected count for this exposure')],
        8:[('$x$','$0,1,2$','Supported scores'),('$p_X(x)$','$0.25,0.5,0.25$','Respective masses')],
        9:[('$p$','$0.5$','Success probability per trial'),('$n$','$3$ trials','Fixed trials for variable B only')]
    }
    general=general.replace('\\subsubsection*{Complete worked solution}', '\\subsubsection*{Complete worked solution}\n'+table(['Symbol','Value','Meaning in this problem'],inputs[c],'llp{0.48\\linewidth}'),1)
    body=head+intro+'\\section{General worked problems}\n'+general+'\\subsection{Bridge to the general model}\n'+bridge+advanced+ref
    for level,items in zip(['Foundational','Intermediate','Advanced'],practice):
        body+='\\Needspace{19\\baselineskip}\n\\section{'+level+' contextual practice}\\label{sec:'+prefix+'-'+level.lower()+'}\n'
        for j,p in enumerate(items,1):
            body+=p+'\\secInicio[][sec:'+prefix+'-'+level.lower()+']\n'
    body+='\\section{Closing reference: key ideas and common errors}\n'+closing+'\n\\secInicio\n\\end{document}\n'
    if c==2:
        body=body.replace('\\Needspace{14\\baselineskip}\n\\subsection{Account-fee CDF audit}',
                          '\\Needspace{30\\baselineskip}\n\\subsection{Account-fee CDF audit}')
    path=OUT/f'G10_T1_L{lesson}_C{c}_practice_activity.tex'
    path.write_text(body,encoding='utf-8')

# C1: outcomes, numerical mappings and probability mass.
c1='Characterises discrete random variables in economic and financial contexts by identifying their support, probability mass function and possible outcomes.'
intro=r'''\subsection{From a school sale to a number}
A school enterprise offers a notebook to each of two visitors. Each visitor either buys (B) or does not buy (N). An \emph{outcome} records the whole story, such as BN: the first visitor buys, while the second does not. A \emph{random variable} assigns a number to every outcome.

Consider three random variables defined on this experiment:

\begin{itemize}
	\item \textbf{Example 1 (Number of buyers).} Let $X$ be the number of visitors who buy a notebook. Then $X(\mathrm{BN})=1$, $X(\mathrm{BB})=2$, and $X(\mathrm{NN})=0$.
	
	\item \textbf{Example 2 (Sales revenue).} If each notebook costs \$5, let $Y$ be the total revenue. Then $Y(\mathrm{BN})=5$, $Y(\mathrm{BB})=10$, and $Y(\mathrm{NN})=0$.
	
	\item \textbf{Example 3 (First visitor's purchase).} Let $Z$ equal 1 if the first visitor buys a notebook and 0 otherwise. Then $Z(\mathrm{BN})=1$, $Z(\mathrm{BB})=1$, and $Z(\mathrm{NB})=0$.
\end{itemize}

The notation $X(\mathrm{BN})=1$ is read ``X of BN equals one''. The capital letter names the random variable (the rule), while a lowercase letter such as $x$ represents a possible or observed numerical value.

\textbf{Check.} Are BN and NB the same outcome? Do they produce the same values of $X$, $Y$, and $Z$?

\emph{Suggested answer:} No; they describe different visitors buying. Both give $X=1$ and $Y=5$, but $Z(\mathrm{BN})=1$ whereas $Z(\mathrm{NB})=0$.


\subsection{Support, measurements and units}

The \emph{support} of a random variable is the set of values with positive probability. Different random variables describing the same experiment may have different supports and measurement units.

Consider the three random variables introduced previously:

\begin{itemize}
	\item \textbf{Example 1 (Number of buyers).} The support of $X$ is $\{0,1,2\}$, measured in buyers. The values represent zero, one, or two visitors purchasing a notebook.
	
	\item \textbf{Example 2 (Sales revenue).} The support of $Y$ is $\{0,5,10\}$, measured in dollars. Revenue increases in increments of \$5 because each notebook has a fixed price.
	
	\item \textbf{Example 3 (First visitor's purchase).} The support of $Z$ is $\{0,1\}$, with no physical unit. The values indicate whether the first visitor buys (1) or does not buy (0).
\end{itemize}

Braces denote a set of possible values. All three examples have \emph{discrete} supports because their values can be listed individually. A discrete support may be finite, such as $\{0,1,2\}$, or countably infinite, such as $\{1,2,3,\ldots\}$, where the dots indicate that the pattern continues indefinitely.

A \emph{continuous} random variable, by contrast, can take values throughout an interval. For example, the exact time required to complete a purchase may be modelled as continuous and measured in seconds. If times are rounded to whole seconds, the recorded values become discrete.

\textbf{Check.} Can $X=1.6$, $Y=7$, or $Z=2$? Explain.

\emph{Suggested answer:} No. The buyer count $X$ must be an integer between 0 and 2; revenue $Y$ can only be 0, 5, or 10 dollars; and the indicator $Z$ can only be 0 or 1.


\subsection{Assign probability to each value}

The \emph{probability mass function} (PMF) assigns a probability to each value of a discrete random variable. For $X$, it is written $p_X(x)=P(X=x)$, read ``the probability that X equals x''. The subscript identifies the random variable: $p_Y(y)=P(Y=y)$ describes revenue, while $p_Z(z)=P(Z=z)$ describes the first visitor's purchase indicator.

Every probability must be non-negative, and the probabilities over the support must add to 1. A value outside the support has probability zero. To find the probability of a value, add the probabilities of all outcomes that produce it; different outcomes need not be equally likely.

For the school sale, suppose the outcome probabilities are
\[
P(\mathrm{NN})=0.1,\qquad P(\mathrm{BN})=0.2,\qquad
P(\mathrm{NB})=0.3,\qquad P(\mathrm{BB})=0.4.
\]
These probabilities are supplied for this example; they are not inferred from the number of outcomes.

\begin{itemize}
    \item \textbf{Example 1 (Number of buyers).} Both BN and NB produce $X=1$, so
    \[
    p_X(1)=P(\mathrm{BN})+P(\mathrm{NB})=0.2+0.3=0.5.
    \]
    The complete PMF is $p_X(0)=0.1$, $p_X(1)=0.5$, and $p_X(2)=0.4$.

    \item \textbf{Example 2 (Sales revenue).} Each notebook sells for 5 USD, so $Y=5X$ when revenue is recorded in USD. The same outcomes that produce one buyer produce revenue of 5 USD. Thus the complete PMF is $p_Y(0)=0.1$, $p_Y(5)=0.5$, and $p_Y(10)=0.4$. The revenue values have monetary units; their probabilities do not.

    \item \textbf{Example 3 (First visitor's purchase).} The first visitor buys in BN and BB, so $p_Z(1)=0.2+0.4=0.6$. The first visitor does not buy in NN and NB, so $p_Z(0)=0.1+0.3=0.4$.
\end{itemize}

Each PMF has total probability 1. Although $X$ and $Y$ have different supports and units, corresponding values have the same probabilities because $Y=5X$. The variable $Z$ groups the outcomes differently.

\textbf{Check.} Is $p_Y(5)=0.5$ a payment of 0.5 USD? What does it mean?

\emph{Suggested answer:} No. It is a dimensionless probability: there is a 50\% chance that revenue equals 5 USD.

\textbf{Check.} Are the events $X=1$, $Y=5$, and $Z=1$ the same?

\emph{Suggested answer:} The first two are the same event, consisting of BN and NB. The event $Z=1$ consists of BN and BB, so it is different. Their probabilities are 0.5, 0.5, and 0.6, respectively.

'''

g=problem('Introductory general problem: grouping outcomes',r'An experiment has outcomes $a,b,c,d$ with probabilities $0.1,0.2,0.3,0.4$. Define $X(a)=0$, $X(b)=X(c)=1$, $X(d)=2$.', ['Construct the mapping and PMF; state the support and find $P(X=1)$.'],[
('Define the variable',r'$X$ is the numerical score assigned to an outcome; its units are score units.'),
('Map outcomes',table(['Outcome','$a$','$b$','$c$','$d$'],[['Probability','0.1','0.2','0.3','0.4'],['$X$ value','0','1','1','2']])+'The support is $\{0,1,2\}$. The outcomes are mutually exclusive and exhaustive; equal likelihood is not assumed.'),
('Translate and calculate',r'For any value, $p_X(x)=\sum_{\omega:X(\omega)=x}P(\omega)$. The sum sign means add the probabilities of the matching outcomes. Thus $p_X(1)=P(b)+P(c)=0.2+0.3=0.5000$.'+table(['$x$','0','1','2'],[['$p_X(x)$','0.1','0.5','0.4']])),
('Check and interpret',r'$0.1+0.5+0.4=1$ and all entries are non-negative. The score equals 1 in half of repetitions under this model, even though two distinct outcomes produce it.')])
bridge=r'''For any discrete variable,
\[p_X(x)=P(X=x)\geq0,\qquad \sum_{x\in S}p_X(x)=1.\]
Here $S$ denotes the support and $x\in S$ means ``x belongs to S''. The summation means add once for each supported value, not once for each outcome after it has already been grouped. This applies to any finite or countably infinite list with total mass 1.
'''
a=problem('Advanced general problem: a finite and an infinite model',r'Model A assigns masses $c,2c,3c$ to scores $0,2,5$. Model B assigns $p_T(t)=2^{-t}$ for $t=1,2,\ldots$.',['Determine $c$, verify both PMFs, and calculate $P(X\geq2)$ and $P(T>3)$.'],[
('Define and identify support',r'$X$ is the Model A score with support $\{0,2,5\}$; $T$ is a positive-integer trial count with support $\{1,2,\ldots\}$. These are proposed distributions, so normalization must be checked.'),
('Normalize',r'$\sum_xp_X(x)=c+2c+3c=6c=1$, so $c=1/6$. The masses are $1/6,1/3,1/2$, all positive. For Model B, the first $m$ terms total $1-2^{-m}$; as $m$ grows without bound this approaches 1. Thus the infinite list also defines a PMF.'),
('Translate and calculate',r'$P(X\geq2)=p_X(2)+p_X(5)=1/3+1/2=5/6\approx0.8333$. Also $P(T>3)=1-\sum_{t=1}^{3}2^{-t}=1-(1/2+1/4+1/8)=1/8=0.1250$.'),
('Check and interpret',r'Both probabilities lie between 0 and 1. Model A has only three possible values despite the gap from 2 to 5; Model B has no last possible trial. Infinite support does not mean infinite total probability.')])
ref=reference([(r'$\omega$','One complete experimental outcome'),('$X,x$','Random variable and one numerical value'),('$S$','Support: values with positive probability'),('$p_X(x)$','Probability assigned to value $x$'),(r'$\sum$','Add the indicated terms')],routine)
p=[]
p.append(problem('Notebook buyers',r'Two visitors buy independently with probability $1/2$ each. Let B mean a purchase and N no purchase. Each sale earns 4 USD.', ['List outcomes, define the buyer count $X$, build its PMF and find the chance of revenue 4 USD.'],[
('Define and list',r'$X$ counts buyers, with support $\{0,1,2\}$. Revenue is $Y=4X$ USD, with support $\{0,4,8\}$ USD.'),
('Check the model and map',r'Independence and the two equal probabilities make BB, BN, NB, NN each have probability $(1/2)^2=1/4$. Their $X$ values are 2, 1, 1, 0.'),
('Calculate',r'$p_X(1)=P(\mathrm{BN})+P(\mathrm{NB})=1/4+1/4=0.5$.'+table(['$x$ (buyers)','0','1','2'],[['$p_X(x)$','0.25','0.50','0.25']])+r'$P(Y=4)=P(X=1)=0.5000$.'),
('Check and interpret',r'The table totals 1. A revenue of 4 USD occurs in two of the four equally likely outcomes; 0.5 is a probability, not revenue.')]))
p.append(problem('Daily insurance claims',r'The number $X$ of claims on a small policy group in one day has probabilities $0.7,q,0.1$ for $0,1,2$ claims; no other values are possible.', ['Find $q$, verify the PMF and calculate the probability of any claim.'],[
('Define',r'$X$ counts daily claims, with proposed support $\{0,1,2\}$. The supplied model is a complete finite distribution; no trial independence assumption is required to use its table.'),
('Normalize',r'$q=1-p_X(0)-p_X(2)=1-0.7-0.1=0.2$.'),
('Translate and calculate',r'$P(X\geq1)=p_X(1)+p_X(2)=0.2+0.1=0.3000$.'),
('Check and interpret',r'All masses are positive and total 1. Any claim occurs with probability 30\%; the count itself is measured in claims, not USD.')]))
p.append(problem('Payment methods and a fee',r'A shop receives one payment: cash with probability 0.25, debit with 0.45, or credit with 0.30. Cash costs no processing fee; either card costs 1 USD.', ['Define the fee variable and construct its PMF. Explain why three outcomes need not give three values.'],[
('Define',r'$X$ is the processing fee in USD, with support $\{0,1\}$. The method categories are mutually exclusive and exhaustive.'),
('Map',r'$X(\text{cash})=0$ and $X(\text{debit})=X(\text{credit})=1$. Add the probabilities of the two card outcomes.'),
('Calculate',r'$p_X(0)=0.25$ and $p_X(1)=P(\text{debit})+P(\text{credit})=0.45+0.30=0.75$. Thus $P(X>0)=0.7500$.'),
('Check and interpret',r'$0.25+0.75=1$. There are three method outcomes but only two fee values; a random variable need not assign different values to different outcomes.')]))
p.append(problem('Investment results with a missing mass',r'A hypothetical one-month net gain $G$ takes values $-20,0,30$ USD with masses $0.2,0.5,q$. A student proposes $q=0.4$.', ['Correct the PMF, identify the support and calculate the probability of a non-negative gain.'],[
('Define',r'$G$ is monetary net gain, not a count. A finite set of monetary outcomes is discrete even though money is involved.'),
('Validate',r'$q=1-0.2-0.5=0.3$; the proposed 0.4 would make total mass 1.1, so it is invalid. Support is $\{-20,0,30\}$ USD.'),
('Calculate',r'$P(G\geq0)=p_G(0)+p_G(30)=0.5+0.3=0.8000$.'),
('Check and interpret',r'The corrected masses are non-negative and total 1. A loss remains possible with probability 0.2. Zero gain is included in non-negative gain.')]))
p.append(problem('Calls until a sale',r'A sales team models $T$, the call number of its first sale, by $p_T(t)=(1/2)^t$ for $t=1,2,\ldots$. It also records exact call duration $D$ in minutes.', ['Classify both variables; verify the waiting-count PMF and find $P(T\leq3)$.'],[
('Define and distinguish',r'$T$ counts calls and has countably infinite support. $D$ measures time and is treated as continuous; its exact support contains intervals, rather than a list of isolated counts.'),
('Check the supplied model',r'All masses $2^{-t}$ are positive. Their first $m$ terms sum to $1-2^{-m}\to1$, so the infinite PMF is valid. It is compatible with independent calls with constant sale chance $1/2$.'),
('Calculate',r'$P(T\leq3)=\sum_{t=1}^{3}p_T(t)=1/2+1/4+1/8=7/8=0.8750$.'),
('Interpret',r'The first sale occurs within three calls with probability 87.5\%. There is no fixed maximum call number in the model; this does not make the count continuous.')]))
p.append(problem('Delivery records: two numerical descriptions',r'A delivery has outcomes early, on time, late with probabilities $0.2,0.5,0.3$. A bonus $B$ is 2 USD for early or on time and $-3$ USD for late. An indicator $I$ is 1 if late and 0 otherwise.', ['Build both PMFs and contrast them with an exact delivery-time measurement.'],[
('Define and map',r'$B$ measures bonus in USD, with support $\{-3,2\}$; $I$ labels lateness, with support $\{0,1\}$. Early and on time both map to $B=2$ and $I=0$.'),
('Check the categories',r'The three exclusive outcomes cover all deliveries and their probabilities total 1. No equal-likelihood assumption is justified.'),
('Calculate',r'$p_B(2)=0.2+0.5=0.7$, $p_B(-3)=0.3$; $p_I(0)=0.7$, $p_I(1)=0.3$. Thus $P(B<0)=P(I=1)=0.3000$.'),
('Check and interpret',r'Each PMF totals 1. The same uncertain delivery can generate different discrete variables with different units. Exact elapsed delivery time is a continuous measurement under an ideal model, even though its early/on-time/late classification is discrete.')]))
write(1,'Outcomes, Support and Probability Mass Functions',c1,intro,g,bridge,a,ref,[p[:2],p[2:4],p[4:]],r'An outcome is a whole story; a random variable maps it to a number. Group outcomes before assigning masses. Support contains only positive-mass values. Discrete does not mean equally likely, and a monetary variable need not be continuous. Check every mass and the total; never confuse a number of outcomes with a probability.')

c2='Interprets PMFs and CDFs by verifying their defining properties and using them to calculate point, interval, cumulative, and complementary probabilities in financial contexts.'
intro=r'''\subsection{Individual and accumulated probabilities}
A school shop counts refunds in an afternoon. Exactly two means one value; at most two includes zero, one and two. The PMF $p_X(x)=P(X=x)$ is read as the probability that X equals x. The CDF $F_X(x)=P(X\leq x)$ is read as the probability that X is at most x. Capital $X$ names the random variable, while $x$ is a value or cutoff. Refund counts have units of refunds; probabilities have no units.
'''+check(r'Does $F_X(2)$ mean exactly two?',r'No. It adds all mass at values at most 2.')+r'''
\subsection{Defining properties}
A PMF is non-negative and its masses total 1. A CDF is non-decreasing: raising the cutoff cannot remove outcomes. It is right-continuous: the value at a jump equals the height immediately to its right. Its limits are 0 as $x\to-\infty$ and 1 as $x\to+\infty$, meaning arbitrarily far left and right. For finite discrete support, it is constant between supported values and jumps by $p_X(x)$ at each value.
'''+check('May a CDF decrease from 0.7 to 0.5?',r'No. Cumulative probability cannot decrease.')+r'''
\subsection{Endpoints}
At most means $\leq$; less than means $<$; at least means $\geq$; more than means $>$. For integer counts $P(X<3)=F_X(2)$, but for irregular support list the actual included values. A CDF accepts all real cutoffs, including values outside the support.
'''+check(r'For support $\{0,2,5\}$, what does $1<X<5$ contain?',r'Only $X=2$.')+check(r'What is the complement of $X>2$?',r'$X\leq2$, so $P(X>2)=1-F_X(2)$.')
def cdf(values,probs,var='X'):
    running=0
    lines=[f'0,&x<{values[0]},']
    for i,(v,p) in enumerate(zip(values,probs)):
        running+=p
        lines.append(f'{running:g},&{v}\\leq x<{values[i+1]},' if i<len(values)-1 else f'1,&x\\geq {v}.')
    return '\\[F_'+var+'(x)=\\begin{cases}'+r'\\'.join(lines)+'\\end{cases}\\]\n'
graphs=r'''\begin{center}
\begin{tikzpicture}
\begin{axis}[width=0.43\linewidth,height=5cm,xmin=-1,xmax=6,ymin=0,ymax=1.1,xtick={0,2,5},xlabel={$x$ (score)},ylabel={$p_X(x)$},title={PMF: individual masses}]
\addplot+[ycomb,mark=*] coordinates {(0,0.2)(2,0.5)(5,0.3)};
\end{axis}\end{tikzpicture}\hfill
\begin{tikzpicture}
\begin{axis}[width=0.43\linewidth,height=5cm,xmin=-1,xmax=6,ymin=0,ymax=1.1,xtick={0,2,5},xlabel={$x$ (score)},ylabel={$F_X(x)$},title={CDF: accumulated mass}]
\addplot[blue,thick] coordinates {(-1,0)(0,0)};
\addplot[blue,thick] coordinates {(0,0.2)(2,0.2)};
\addplot[blue,thick] coordinates {(2,0.7)(5,0.7)};
\addplot[blue,thick] coordinates {(5,1)(6,1)};
\addplot[only marks,mark=*,blue] coordinates {(0,0.2)(2,0.7)(5,1)};
\addplot[only marks,mark=*,mark options={fill=white},blue] coordinates {(0,0)(2,0.2)(5,0.7)};
\end{axis}\end{tikzpicture}\end{center}
Filled dots give included endpoint values; open dots exclude them. Each jump matches a PMF stem. Horizontal tails continue to either side.
'''
g=problem('Introductory general problem: PMF to CDF',r'A score $X$ has support $\{0,2,5\}$ and masses $0.2,0.5,0.3$.',['Verify the PMF; construct the complete CDF and graphs; find $P(0<X\leq5)$ and $P(X<5)$.'],[
('Define and validate',r'$X$ is a score. Its masses are positive and $0.2+0.5+0.3=1$, so the table is valid; no independent-trials model is required.'),
('Accumulate',r'$F_X(x)=\sum_{u\leq x}p_X(u)$. The summation sign means add masses at supported values $u$ at most the cutoff $x$.'+cdf([0,2,5],[.2,.5,.3])+graphs),
('Calculate',r'$P(0<X\leq5)=p_X(2)+p_X(5)=0.5+0.3=0.8000$. Also $P(X<5)=p_X(0)+p_X(2)=0.2+0.5=0.7000$, whereas $F_X(5)=1$.'),
('Check and interpret',r'The CDF is non-decreasing, right-continuous and has limits 0 and 1. The strict upper endpoint excludes the 0.3 mass at 5.')])
bridge=r'''Write $F_X(a^-)=P(X<a)$, read as F just to the left of a. Then
\[P(X=a)=F_X(a)-F_X(a^-),\qquad P(a<X\leq b)=F_X(b)-F_X(a).\]
For an inclusive lower endpoint, $P(a\leq X\leq b)=F_X(b)-F_X(a^-)$. Also $P(X>a)=1-F_X(a)$. These identities work for irregular supports as well as consecutive integers.
'''
a=problem('Advanced general problem: recovering jumps and testing candidates',r'Candidate $H$ is 0 for $x<-1$, 0.25 for $-1\leq x<1$, 0.6 for $1\leq x<4$, and 1 for $x\geq4$. Candidate $J$ agrees except $J(1)=0.25$. Candidate $K$ has successive heights $0,0.7,0.6,1$ on the same intervals.',['Validate each; recover the PMF of $H$ and calculate $P(-1<X\leq4)$ and $P(X\geq1)$.'],[
('Define and test',r'$X$ is a score. $H$ has increasing heights, right-continuous endpoints and limits 0 and 1. $J$ fails right-continuity at 1: its value 0.25 differs from height 0.6 immediately to its right. $K$ decreases from 0.7 to 0.6, so it is invalid.'),
('Recover the PMF',r'$p_X(x)=H(x)-H(x^-)$ gives $0.25-0=0.25$, $0.6-0.25=0.35$, $1-0.6=0.4$ on support $\{-1,1,4\}$.'),
('Calculate',r'$P(-1<X\leq4)=H(4)-H(-1)=1-0.25=0.7500$; $P(X\geq1)=1-H(1^-)=1-0.25=0.7500$.'),
('Check and interpret',r'The recovered positive masses total 1. Both events contain precisely 1 and 4; their equal probabilities follow from the support.')])
ref=reference([('$p_X(x)$',r'$P(X=x)$: one value'),('$F_X(x)$',r'$P(X\leq x)$: accumulated mass'),('$F_X(a^-)$',r'$P(X<a)$: height before the jump'),('$1-F_X(a)$',r'$P(X>a)$')],routine)
p=[
problem('Afternoon refunds',r'$X$ counts refunds with masses $0.5,0.3,0.2$ at $0,1,2$.',['Verify the distribution, give its complete CDF and find $P(X=1)$ and $P(X\leq1)$.'],[
('Define and check',r'$X$ counts refunds per afternoon; support $\{0,1,2\}$. The positive masses total $0.5+0.3+0.2=1$.'),
('Construct',r'$F_X(x)=\sum_{u\leq x}p_X(u)$ gives'+cdf([0,1,2],[.5,.3,.2])),
('Calculate',r'$P(X=1)=p_X(1)=0.3000$; $P(X\leq1)=p_X(0)+p_X(1)=0.5+0.3=0.8000$.'),
('Check and interpret',r'The CDF has non-negative jumps, right-continuous endpoints and correct tails. At most one includes zero; exactly one does not.')]),
problem('Transaction fees',r'A fee $Y$ is $0,2,5$ USD with probabilities $0.4,0.35,0.25$.',['Find $P(Y<2)$, $P(Y\leq2)$ and $P(1<Y<5)$.'],[
('Define and validate',r'$Y$ is a fee in USD; support $\{0,2,5\}$. Its positive masses total $0.4+0.35+0.25=1$.'),
('Translate',r'The events contain respectively $\{0\}$, $\{0,2\}$ and $\{2\}$.'),
('Calculate',r'$P(Y<2)=p_Y(0)=0.4000$; $P(Y\leq2)=p_Y(0)+p_Y(2)=0.4+0.35=0.7500$; $P(1<Y<5)=p_Y(2)=0.3500$.'),
('Check and interpret',r'The first two answers differ by the 0.35 jump at 2 USD. A cutoff need not be a supported fee.')]),
problem('Late-payment counts',r'A weekly count has CDF 0 for $x<0$, 0.6 for $0\leq x<2$, 0.9 for $2\leq x<3$, and 1 for $x\geq3$.',['Recover its PMF and find $P(X>0)$ and $P(0<X\leq2)$.'],[
('Define and check',r'$X$ counts late payments; jumps give support $\{0,2,3\}$. The CDF is non-decreasing, right-continuous and has limits 0 and 1.'),
('Recover',r'$p_X(x)=F_X(x)-F_X(x^-)$ gives $0.6$, $0.9-0.6=0.3$, $1-0.9=0.1$; these positive masses total 1.'),
('Calculate',r'$P(X>0)=1-F_X(0)=1-0.6=0.4000$; $P(0<X\leq2)=F_X(2)-F_X(0)=0.9-0.6=0.3000$.'),
('Interpret',r'The first event includes 2 and 3; the second includes only 2. The plateau before 2 shows that 1 has no mass in this simplified model.')]),
problem('Investment gain intervals',r'$G$ takes $-10,0,15,40$ USD with masses $0.2,0.3,0.4,0.1$.',['Find the probabilities of a loss, a positive gain, $0\leq G<40$, and the value $F_G(14)$.'],[
('Define and validate',r'$G$ is net gain in USD; the four positive masses total 1. Its support is the four listed monetary values.'),
('Translate',r'Loss is $G<0$; positive gain is $G>0$. The interval contains 0 and 15.'),
('Calculate',r'$P(G<0)=p_G(-10)=0.2000$; $P(G>0)=1-F_G(0)=1-(0.2+0.3)=0.5000$; $P(0\leq G<40)=p_G(0)+p_G(15)=0.3+0.4=0.7000$.'),
('Check and interpret',r'$F_G(14)=p_G(-10)+p_G(0)=0.5000$. Positive and non-negative gain differ by the mass at zero.')]),
problem('Insurance PMF audit',r'Candidate A has masses $0.6,0.5,-0.1$ at counts $0,1,2$; B has $0.2,0.3,0.3$. The corrected model is $0.6,0.3,0.1$.',['Reject A and B; find $P(X\geq1)$ and $P(X<2)$ for the correction.'],[
('Define and audit',r'$X$ counts daily claims with corrected support $\{0,1,2\}$. A totals 1 but contains a negative mass; B is non-negative but totals 0.8. Both are invalid.'),
('Validate',r'The correction is positive and totals $0.6+0.3+0.1=1$. Its CDF heights are $0,0.6,0.9,1$ on boundaries 0, 1, 2, with closed left endpoints.'),
('Calculate',r'$P(X\geq1)=1-P(X<1)=1-p_X(0)=1-0.6=0.4000$; $P(X<2)=p_X(0)+p_X(1)=0.6+0.3=0.9000$.'),
('Check and interpret',r'The complement of at least one is zero. A total of 1 alone does not establish a PMF.')]),
problem('Account-fee CDF audit',r'Fees can only be 0 or 3 USD. Candidate $H$ is 0 for $y<0$, 0.4 for $0\leq y<3$, and 0.9 for $y\geq3$. Another has heights 0, 0.4, 1 on these intervals but assigns value 0 at $y=0$.',['Explain both defects, construct a valid CDF retaining mass 0.4 at zero, and find $P(0<Y\leq3)$.'],[
('Define and diagnose',r'$Y$ measures fee in USD. $H$ has limit 0.9 instead of 1 at positive infinity. The other fails right-continuity at zero.'),
('Repair',r'$p_Y(3)=1-p_Y(0)=1-0.4=0.6$. \[F_Y(y)=\begin{cases}0,&y<0,\\0.4,&0\leq y<3,\\1,&y\geq3.\end{cases}\]'),
('Calculate',r'$P(0<Y\leq3)=F_Y(3)-F_Y(0)=1-0.4=0.6000$.'),
('Check and interpret',r'The repaired CDF is non-decreasing, right-continuous and has limits 0 and 1. Its jumps total 1; the event is precisely a 3 USD fee.')])]
write(2,'Reading and Checking PMFs and CDFs',c2,intro,g,bridge,a,ref,[p[:2],p[2:4],p[4:]],r'A PMF assigns individual masses; a CDF accumulates them. Check non-negativity, total mass, monotonicity, right-continuity and limits. Use actual support for endpoints. Jumps give masses; plateaus add none. In $1-F_X(a)$ equality at $a$ is excluded.')

c3='Models binary economic outcomes with Bernoulli random variables, interpreting success and failure in contexts such as default, gain, loss, or claim occurrence.'
intro=r'''\subsection{Label one uncertain event}
A school enterprise sends one invoice. Define $X=1$ if it is paid on time and $X=0$ otherwise. This is an \emph{indicator}: its number records whether a precisely defined event happens. A Bernoulli variable describes one binary observation. Success is the event labelled 1; failure is its complement, labelled 0.
'''+check('Must success be financially good?',r'No. Default can be labelled success mathematically.')+r'''
\subsection{Probability and support}
Write $p=P(X=1)$, read as p is the probability that X equals one. Then $P(X=0)=1-p$. These probabilities have no units and add to 1. For $0<p<1$ the support is $\{0,1\}$. If $p=0$ or 1, only one label has positive probability.
'''+check(r'If $p=0.08$, what is $P(X=0)$?',r'$1-0.08=0.92$.')+r'''
\subsection{Separate the label from the consequence}
If an insured event costs 200 USD, $L=200X$ USD measures its loss. The indicator is unitless: $X=1$ records occurrence, while $L=200$ measures money. Reversing success gives $Z=1-X$ with $P(Z=1)=1-p$. A single observation needs no independence assumption; independence matters when combining several observations.
'''+check(r'If $X=1$ means default, what does $X=0$ mean?',r'No default during the stated observation period.')+check('Is a 200 USD loss indicator equal to 200?',r'No. The indicator is 1; its separate monetary consequence is 200 USD.')
g=problem('Introductory general problem: one binary trial',r'An event A has probability 0.3. Define $X=1$ if A occurs and 0 otherwise.',['Give the support and calculate both masses from the Bernoulli formula.'],[
('Define and model',r'$X$ indicates A; support $\{0,1\}$, no monetary units, parameter $p=0.3$. A and its complement are exclusive and exhaustive, so the Bernoulli model applies.'),
('Write the formula',r'$P(X=x)=p^x(1-p)^{1-x}$ for $x\in\{0,1\}$. The notation $x\in\{0,1\}$ means x is either 0 or 1; a nonzero number to power zero is 1.'),
('Substitute',r'$P(X=1)=0.3^1(0.7)^0=0.3000$, and $P(X=0)=0.3^0(0.7)^1=0.7000$.'),
('Check and interpret',r'$0.3+0.7=1$. The value 1 labels A; it does not measure how large A is.')])
bridge=r'''\[X\sim\operatorname{Bernoulli}(p),\qquad P(X=x)=p^x(1-p)^{1-x},\quad x\in\{0,1\}.\]
The symbol $\sim$ means has the distribution. Use this for one yes/no event during a specified period. The exponents select either $p$ or $1-p$. At $p=0$ or 1 use direct masses $P(X=1)=p$ and $P(X=0)=1-p$ to avoid $0^0$. A count from several observations needs a different model.
'''
a=problem('Advanced general problem: reversing success and measuring money',r'$X$ indicates an adverse event of probability 0.2. Define $Z=1-X$ and $Y=12-50X$ USD.',['Find both indicator PMFs, the monetary support and $P(Y<0)$. Explain whether $Y$ is Bernoulli.'],[
('Define',r'$X=1$ labels the adverse event; $Z=1$ labels its absence. Both have support $\{0,1\}$. $Y$ measures money, with support $\{-38,12\}$ USD.'),
('Model and reverse',r'$X\sim\operatorname{Bernoulli}(0.2)$, $Z\sim\operatorname{Bernoulli}(0.8)$. One event is being observed, so no trial independence assumption is needed.'),
('Calculate',r'$P(Z=1)=1-p=1-0.2=0.8$, $P(Z=0)=0.2$. Also $Y(1)=12-50=-38$ and $Y(0)=12$. Hence $P(Y<0)=P(X=1)=0.2000$; $P(Y=12)=0.8$.'),
('Check and interpret',r'Each PMF totals 1. $Y$ is a monetary transformation of an indicator, but it is not itself Bernoulli because its values are not 0 and 1. Reversing labels does not change the event causing the loss.')])
ref=reference([('$X$','Indicator: 1 for the specified event, 0 otherwise'),('$p$','Probability of the event labelled 1; no units'),('$1-p$','Complementary probability'),('$Z=1-X$','Reversed indicator'),('$Y=aX+b$','Monetary consequence if $a,b$ are monetary amounts')],routine)
def bern_problem(title,context,event,p,consequence,extra=''):
    q=1-p
    return problem(title,context,[f'Define the indicator for {event}; give its PMF and the financial interpretation. '+extra],[
('Define the event',f'$X=1$ if {event}, and $X=0$ otherwise. Support is $\\{{0,1\\}}$, without monetary units; $p={p:g}$.'),
('Justify the model',r'This is one observation with two exclusive, exhaustive labels, so it is Bernoulli. Repeated-observation independence is not needed here.'),
('Translate and calculate',r'$P(X=x)=p^x(1-p)^{1-x}$ for $x=0,1$. Thus '+f'$P(X=1)={p:g}$, $P(X=0)=1-{p:g}={q:g}$. '+consequence),
('Check and interpret',f'The non-negative masses sum to $ {p:g}+{q:g}=1$. The success probability is {number(title,p)}. '+r'The indicator records occurrence; money measures its consequence.')])
p=[
bern_problem('One loan default',r'One loan has a hypothetical probability 0.04 of default within one year. Default causes a fixed loss of 800 USD; otherwise default loss is zero.','the loan defaults within one year',.04,r'$L=800X$ USD. Thus $P(L=800)=P(X=1)=0.04$ and $P(L=0)=0.96$. Mathematical success is financially undesirable.'),
bern_problem('One policy claim',r'One insurance policy has probability 0.12 of at least one claim this month. The simplified contract pays 300 USD once if any claim occurs.','at least one claim occurs this month',.12,r'$Y=300X$ USD. Hence $P(Y>0)=P(X=1)=0.12$. The indicator does not count claims.'),
bern_problem('Invoice payment and reversal',r'One invoice is paid by its due date with probability 0.85. Late payment triggers a 6 USD fee.','the invoice is paid on time',.85,r'For lateness use $Z=1-X$, with parameter $1-p=0.15$. The fee is $L=6Z$ USD, so $P(L=6)=P(Z=1)=0.15$.','Reverse success to lateness and find the fee probability.'),
bern_problem('Investment gain',r'One investment yields 15 USD with probability 0.6 and loses 10 USD otherwise.','the investment has a positive gain',.6,r'$G=-10+25X$ USD. Therefore $P(G=15)=0.6$, $P(G=-10)=0.4$ and $P(G<0)=0.4$. The indicator value 1 does not mean 1 USD.'),
bern_problem('Chargeback and merchant balance',r'One sale brings 30 USD initially. With probability 0.08 a chargeback removes 30 USD and adds a 5 USD fee.','the sale produces a chargeback',.08,r'$Y=30-35X$ USD, with values 30 and $-5$. Thus $P(Y<0)=P(X=1)=0.08$. Reversing success to no chargeback gives parameter 0.92, but the loss probability stays 0.08.','Find the negative-balance probability and the reversed parameter.'),
problem('Three sales categories',r'One enquiry produces no sale, a basic sale or a premium sale with probabilities $0.5,0.3,0.2$. Basic revenue is 20 USD; premium revenue is 50 USD.',['Explain why revenue is not Bernoulli. Give PMFs for purchase and premium indicators, and find the chance of revenue at least 20 USD.'],[
('Define',r'$R$ is revenue in USD, support $\{0,20,50\}$. Define $X=1$ for any purchase and 0 otherwise; $Z=1$ for premium and 0 otherwise. Both indicators have support $\{0,1\}$.'),
('Select',r'Three revenue values exclude Bernoulli for $R$. Each indicator groups the exclusive, exhaustive outcomes into two categories, so each is Bernoulli. They concern the same enquiry and are not assumed independent.'),
('Calculate',r'$P(X=1)=P(\text{basic})+P(\text{premium})=0.3+0.2=0.5$; $P(X=0)=0.5$. Also $P(Z=1)=0.2$, $P(Z=0)=0.8$. Therefore $P(R\geq20)=P(X=1)=0.5000$.'),
('Check and interpret',r'Each PMF totals 1. Premium implies purchase, but the two indicators answer different questions. Revenue measures monetary size.')])]
write(3,'Bernoulli Indicators and Financial Consequences',c3,intro,g,bridge,a,ref,[p[:2],p[2:4],p[4:]],r'Define success before assigning $p$. Success may mean default or loss. Reverse the label with $1-p$. Distinguish an indicator, monetary consequence and multiple-trial count. A single Bernoulli observation does not require independence.')

# Binomial calculations, including complements and finite sums.
def binmass(n,p,k): return math.comb(n,k)*p**k*(1-p)**(n-k)
def binprob(title,context,n,p,event,k,mode='exact',upper=None,extra=''):
    q=1-p
    if mode=='exact':
        notation=f'X={k}'
        formula=r'P(X=k)=\binom nk p^k(1-p)^{n-k}'
        numeric=f'\\binom{{{n}}}{{{k}}}({p:g})^{k}({q:g})^{{{n-k}}}'
        val=binmass(n,p,k)
    else:
        lo,hi=(0,k) if mode=='atmost' else (k,n) if mode=='atleast' else (k,upper)
        notation=f'X\\leq{k}' if mode=='atmost' else f'X\\geq{k}' if mode=='atleast' else f'{k}\\leq X\\leq{upper}'
        val=sum(binmass(n,p,j) for j in range(lo,hi+1))
        if mode=='atleast':
            formula=r'P(X\geq k)=1-\sum_{j=0}^{k-1}\binom nj p^j(1-p)^{n-j}'
            numeric=f'1-\\sum_{{j=0}}^{{{k-1}}}\\binom{{{n}}}j({p:g})^j({q:g})^{{{n}-j}}'
        else:
            formula=r'P(a\leq X\leq b)=\sum_{j=a}^{b}\binom nj p^j(1-p)^{n-j}'
            numeric=f'\\sum_{{j={lo}}}^{{{hi}}}\\binom{{{n}}}j({p:g})^j({q:g})^{{{n}-j}}'
    result=number(title,val)
    return problem(title,context,[f'Calculate $P({notation})$, defining success as {event}. '+extra],[
('Define the variable',f'$X$ counts successes among {n} trials. A success means {event}. Its support is $\\{{0,1,\\ldots,{n}\\}}$ successes; money is a separate consequence.'),
('State parameters and check conditions',f'$n={n}$ is fixed, $p={p:g}$ and $1-p={q:g}$. Under the stated independence, binary-outcome and constant-probability assumptions, $X\\sim\\operatorname{{Bin}}({n},{p:g})$.'),
('Translate and calculate',f'The requested event is $ {notation}$. First use\n\\[{formula}.\\]\nThen substitute:\n\\[P({notation})={numeric}\\approx {result}.\\]'),
('Check and interpret',f'The answer is between 0 and 1; the full binomial PMF totals $(p+(1-p))^n=1$. Under this hypothetical model, the probability of the requested success count is {result}. '+('For at least one, the complementary event is no successes. ' if mode=='atleast' and k==1 else '')+extra_solution.get(title,''))])
extra_solution={}
extra_solution['Payment fees in a band']=r'The fee transformation gives $10\leq5X\leq20$ USD, hence $2\leq X\leq4$. Both monetary endpoints are included.'
c4='Applies the binomial distribution to fixed-trial financial situations by verifying its conditions and calculating probabilities using the binomial probability formula.'
intro=r'''\subsection{A fixed set of opportunities}
A school shop sends four independent offers. Each visitor either purchases (success) or does not, with constant purchase probability $p$. Let $X$ count purchases. The number of trials $n=4$ is fixed before results are observed. The support is $\{0,1,2,3,4\}$ purchases. Probability has no monetary units; revenue might be a separate variable $Y=5X$ USD.
'''+check('Does the shop stop after its first sale?',r'No. A binomial count observes all four fixed trials.')+r'''
\subsection{Four conditions}
Use binomial only with a fixed number $n$ of binary trials, independent results and constant success probability $p$. Independent means one result does not change the probability of another. A common economic shock may break independence. Changing customer groups may break constant probability.
'''+check('Are default events automatically independent?',r'No. A shared economic shock can link them.')+r'''
\subsection{Count the arrangements}
Exactly two successes in three trials can occur as SSF, SFS or FSS. Each sequence has probability $p^2(1-p)$. There are three such arrangements, so add their probabilities. In general their number is the combination $\binom nk$, read as n choose k:
\[\binom nk=\frac{n!}{k!(n-k)!}.\]
The factorial $n!$ means multiply positive integers from 1 to $n$: $4!=4\cdot3\cdot2\cdot1=24$, and $0!=1$. Thus $\binom42=24/(2\cdot2)=6$. Order matters for a sequence, but the combination counts all sequences with the same number of successes.
'''+check(r'Why is $p^2(1-p)$ alone insufficient for two successes in three trials?',r'It describes only one arrangement; there are three.')+check(r'What does $\sum_{j=0}^{2}P(X=j)$ mean?',r'Add $P(X=0)+P(X=1)+P(X=2)$; it is an at-most probability.')
g=binprob('Introductory general problem: exactly two successes',r'Three independent binary trials each have success probability $1/2$.',3,.5,'the trial gives the designated S outcome',2)
bridge=r'''\[
X\sim\operatorname{Bin}(n,p),\qquad P(X=k)=\binom nk p^k(1-p)^{n-k},\quad k=0,\ldots,n.
\]
The powers describe one sequence: $k$ successes and $n-k$ failures. The combination counts its possible arrangements. For at most $b$, add terms from 0 to $b$. For at least $a$, use $1-P(X\leq a-1)$; the complement ends at $a-1$, not $a$. For between two values, state whether both endpoints are included.
'''
a=binprob('Advanced general problem: a central interval',r'Six independent binary trials have constant success probability 0.4.',6,.4,'the designated event occurs',2,'between',4)
ref=reference([('$n,k$','Fixed trial count and realised success count'),('$p,1-p$','Success and failure probabilities'),(r'$\binom nk$','Number of success-position arrangements'),('$n!$','Factorial, with $0!=1$'),(r'$\sum_{j=a}^b$','Add one term for every integer $j$ from $a$ to $b$')],routine)
extra_solution['Supplier defects and a failed assumption']=r'In the second version, sampling without replacement from a small lot changes the defect probability after each draw. The binomial assumptions fail; a different sampling model or the full lot composition is needed.'
p=[
binprob('Loan defaults',r'Five independent loans each default within one year with probability 0.1. Default is success mathematically.',5,.1,'a loan defaults within the year',1),
binprob('On-time invoices',r'Four invoices are paid independently, each with constant probability 0.8 of being on time.',4,.8,'an invoice is paid on time',3),
binprob('Insurance claims at most one',r'Six independent policies each have probability 0.05 of a claim this month.',6,.05,'a policy has at least one claim this month',1,'atmost'),
binprob('At least one business sale',r'Eight independent enquiries each have constant sale probability 0.25.',8,.25,'an enquiry becomes a sale',1,'atleast'),
binprob('Payment fees in a band',r'A firm processes ten independent payments, each late with probability 0.2. A late payment costs 5 USD, so total late fees are $Y=5X$ USD.',10,.2,'a payment is late',2,'between',4,extra='Explain why this is also the event $10\\leq Y\\leq20$ USD.'),
binprob('Supplier defects and a failed assumption',r'In version A, seven independently produced items each have defect probability 0.15. In version B, seven items are drawn without replacement from a small lot containing both defective and sound items.',7,.15,'an item is defective',2,'atleast',extra='Calculate for version A; explain why version B does not justify the same binomial model.')]
write(4,'Binomial Counts in Fixed Financial Trials',c4,intro,g,bridge,a,ref,[p[:2],p[2:4],p[4:]],r'Check fixed $n$, binary outcomes, independence and constant $p$ before calculating. The combination counts arrangements; do not omit it. At least $k$ complements at most $k-1$. Count successes separately from monetary costs. Sampling without replacement and common shocks can invalidate the model.')

c5='Models waiting-time situations with geometric distributions, calculating the probability of the first success occurring on a given trial in financial or business contexts.'
intro=r'''\subsection{Wait for the first success}
A school enterprise contacts visitors one by one until somebody buys. Define success as a purchase and $T$ as the call number of the first purchase. The first call is trial 1, so $T$ has support $\{1,2,3,\ldots\}$ calls, provided $0<p<1$. Trials are assumed independent with constant purchase probability $p>0$ and may continue as needed.
'''+check(r'Can $T=0$?',r'No. At least one trial is needed to observe a first success.')+r'''
\subsection{The sequence before stopping}
For $T=4$, the sequence must be FFFS: three failures followed by success. Its probability is $(1-p)^3p$. There is only one such pattern because the first success fixes the final position. $T$ counts all trials; $F=T-1$ counts only failures. These are different variables with different supports.
'''+check(r'If $T=4$, how many failures occur?',r'$F=T-1=3$.')+r'''
\subsection{By and after}
By trial $m$ means $T\leq m$ and includes success on trial $m$. After trial $m$ means $T>m$, so the first $m$ trials all fail. A trial count is not elapsed time unless each trial duration is specified. A 2 USD call cost would give a separate total cost $C=2T$ USD.
'''+check(r'Does after trial 3 include $T=3$?',r'No. It means $T=4,5,\ldots$.')+check('How is this different from binomial?',r'Binomial fixes the number of trials and counts successes; geometric fixes one success and counts trials until it.')
def geom(title,context,p,t,mode='exact',extra='',post=''):
    q=1-p
    notation=f'T={t}' if mode=='exact' else f'T\\leq{t}' if mode=='by' else f'T>{t}'
    sym=r'P(T=t)=(1-p)^{t-1}p' if mode=='exact' else r'P(T\leq m)=1-(1-p)^m' if mode=='by' else r'P(T>m)=(1-p)^m'
    num=f'({q:g})^{{{t-1}}}({p:g})' if mode=='exact' else f'1-({q:g})^{t}' if mode=='by' else f'({q:g})^{t}'
    val=q**(t-1)*p if mode=='exact' else 1-q**t if mode=='by' else q**t
    return problem(title,context,[f'Calculate $P({notation})$. '+extra],[
('Define the variable',r'$T$ is the trial number of the first stated success, in trials, with support $\{1,2,\ldots\}$. '+f'$p={p:g}$ and $1-p={q:g}$.'),
('Check assumptions',r'The trials are binary, independent and have constant success probability; the process stops at the first success. Thus a geometric total-trial model applies.'),
('Translate and calculate',f'Use\n\\[{sym}.\\]\nThen\n\\[P({notation})={num}\\approx {number(title,val)}.\\]'),
('Check and interpret',r'The result is in $[0,1]$; by-trial and after-trial probabilities sum to 1 because their events are complements. '+(f'For the exact event, {t-1} failures precede success on trial {t}. ' if mode=='exact' else 'The endpoint is included for by and excluded for after. ')+post)])
g=geom('Introductory general problem: first success on trial three',r'Independent trials have success probability $1/2$.',.5,3)
bridge=r'''\[
P(T=t)=(1-p)^{t-1}p,\quad t=1,2,\ldots;\qquad
P(T>m)=(1-p)^m,\quad P(T\leq m)=1-(1-p)^m.
\]
There are $t-1$ failures before the final success. Powers mean repeated multiplication. The infinite PMF sums to 1 for $0<p\leq1$; when $p=1$, $T=1$ certainly. If $p=0$, success never occurs and this is not a proper finite waiting-time distribution. In failure-count notation $F=T-1$, $P(F=f)=(1-p)^fp$, with support $\{0,1,\ldots\}$ for $0<p<1$.
'''
a=problem('Advanced general problem: a window and a changed starting point',r'Trials are independent with success probability 0.3.',['Find $P(2<T\leq5)$. Given the first two trials failed, find the chance of a success in the next three.'],[
('Define and model',r'$T$ is the total trial count until first success, support $\{1,2,\ldots\}$ trials. Constant $p=0.3$ and independence justify geometric waiting.'),
('Translate',r'$2<T\leq5$ includes trials 3, 4, 5. Its unconditional probability is $P(T>2)-P(T>5)$.'),
('Calculate',r'$P(2<T\leq5)=(1-p)^2-(1-p)^5=0.7^2-0.7^5='+number('geometric window',.7**2-.7**5)+r'$. The conditional probability, written $P(T\leq5\mid T>2)$, means given no success in two trials. Independence leaves the next three trials unchanged: $1-(1-p)^3=1-0.7^3='+number('geometric conditional',1-.7**3)+r'$.'),
('Check and interpret',r'The unconditional window probability is $0.32193$; dividing by $P(T>2)=0.49$ gives $0.657$. Waiting already observed changes the information, so these two probabilities answer different questions.')])
ref=reference([('$T,t$','Total trials until first success and one possible value'),('$p$','Constant success probability per trial'),('$m$','Trial cutoff; a positive integer'),('$F=T-1$','Failures before first success'),(r'$P(A\mid B)$','Probability of A given that B is known')],routine)
p=[
geom('First sale on call four',r'Independent sales calls have constant purchase probability 0.2; success means a purchase.',.2,4),
geom('Loan approval on the second application',r'In a simplified hypothetical model, independent applications each have approval probability 0.4; success means approval. Stop at the first approval.',.4,2,extra='State the number of rejected applications on this event.',post=r'On this event $F=T-1=1$ rejection. Actual repeat applications may not be independent; the result relies on the supplied hypothetical assumption.'),
geom('Payment completed by attempt three',r'Independent payment attempts each succeed with probability 0.7. Stop when payment completes.',.7,3,'by'),
geom('Still waiting after five enquiries',r'Independent enquiries each lead to a signed contract with probability 0.15. A contract is success.',.15,5,'after'),
geom('Call budget and first sale',r'Independent calls each sell a service with probability 0.25. Each call costs 3 USD. The business can fund at most 12 USD of calls.',.25,4,'by',extra='Translate the 12 USD budget into a trial cutoff.',post=r'$C=3T\leq12$ is equivalent to $T\leq4$. The budget is money; 4 is a call count. The probability is that a first sale arrives before the budget is exceeded.'),
geom('Failures before an insurance sale',r'Independent insurance offers each sell with probability 0.1. Let $F$ count unsuccessful offers before the first sale.',.1,4,extra='Translate $F=3$ into total-trial notation, and contrast the event with exactly one sale among four offers.',post=r'$F=3$ is $T=4$, sequence FFFS. Exactly one sale in four fixed offers also includes SFFF, FSFF and FFSF, so it is a binomial event with probability $\binom41(0.1)(0.9)^3=0.2916$, four times the waiting probability.')]
write(5,'Geometric Waiting for the First Success',c5,intro,g,bridge,a,ref,[p[:2],p[2:4],p[4:]],r'$T$ counts the successful trial as well as preceding failures. Its support starts at 1; $F=T-1$ starts at 0. Use $t-1$ failures in an exact probability and $m$ failures for after trial $m$. Distinguish first success from a fixed-trial success count, and state constant probability and independence.')

c6='Applies the negative binomial distribution to situations that count the number of trials needed to obtain a fixed number of successes.'
intro=r'''\subsection{Wait for a target number of sales}
A school enterprise needs three sales. It contacts visitors independently, with constant purchase probability $p$. Let $T$ count all contacts up to and including the third sale. The target $r=3$ successes is fixed, but the number of trials is random. Support is $\{3,4,5,\ldots\}$ contacts for $0<p<1$.
'''+check('Could the third sale occur on contact two?',r'No. One contact gives at most one success; $T\geq r$.')+r'''
\subsection{Fix the final success}
For the third sale to occur on contact five, contact five must be a success. The first four contacts contain exactly two successes, in any positions. There are $\binom42=6$ choices of those positions, read as four choose two. In general
\[\binom ab=\frac{a!}{b!(a-b)!},\qquad4!=4\cdot3\cdot2\cdot1=24,\quad0!=1.\]
Factorial means multiply positive integers up to the number. Combinations count the selected success positions.
'''+check(r'Why not use $\binom53$?',r'It would allow the third success before contact five; the final position must be fixed as success.')+r'''
\subsection{Trials, failures and probability}
The failure count is $F=T-r$. If three sales require five contacts, there are two failures. Counts have units of contacts or failed contacts; probability has no units. A per-contact expense produces a separate monetary cost. Independence means earlier results do not change later probabilities.
'''+check(r'For $r=3$, $T=7$, what is $F$?',r'$F=T-r=4$ failures.')+check(r'If $r=1$, which model results?',r'Geometric, counting total trials until the first success.')
def nbmass(r,p,t): return math.comb(t-1,r-1)*p**r*(1-p)**(t-r)
def nb(title,context,r,p,t,mode='exact',extra='',post=''):
    q=1-p
    event=f'T={t}' if mode=='exact' else f'T\\leq{t}' if mode=='by' else f'T>{t}'
    if mode=='exact':
        sym=r'P(T=t)=\binom{t-1}{r-1}p^r(1-p)^{t-r}'
        num=f'\\binom{{{t-1}}}{{{r-1}}}({p:g})^{r}({q:g})^{{{t-r}}}'
        val=nbmass(r,p,t)
    else:
        sym=r'P(T\leq m)=\sum_{u=r}^{m}\binom{u-1}{r-1}p^r(1-p)^{u-r}'
        num=f'\\sum_{{u={r}}}^{{{t}}}\\binom{{u-1}}{{{r-1}}}({p:g})^{r}({q:g})^{{u-{r}}}'
        val=sum(nbmass(r,p,u) for u in range(r,t+1))
        if mode=='after':
            sym=r'P(T>m)=1-P(T\leq m)'
            num='1-\\left['+num+'\\right]'
            val=1-val
    return problem(title,context,[f'Calculate $P({event})$. '+extra],[
('Define and identify',f'$T$ is the total trials up to and including success {r}. Support is $\\{{{r},{r+1},\\ldots\\}}$ trials; $r={r}$ and $p={p:g}$.'),
('Check the model',r'Binary trials are independent with constant success probability and stop at the fixed target. This is the total-trial negative binomial convention.'),
('Translate and calculate',f'Use\n\\[{sym}.\\]\nSubstitute:\n\\[P({event})={num}\\approx {number(title,val)}.\\]'),
('Check and interpret',f'The probability is in $[0,1]$; the earliest stopping trial is {r}. '+(f'On the exact event there are {t-r} failures, {r-1} successes in the first {t-1} trials, then the final success. ' if mode=='exact' else f'The cumulative sum includes all stopping trials from {r} through {t}. ')+post)])
g=nb('Introductory general problem: second success on trial three',r'Independent binary trials each succeed with probability $1/2$.',2,.5,3,post=r'Allowed sequences are SFS and FSS; SSF reaches the second success on trial 2.')
bridge=r'''\[P(T=t)=\binom{t-1}{r-1}p^r(1-p)^{t-r},\quad t=r,r+1,\ldots.\]
The final trial is success. Choose $r-1$ success positions among the preceding $t-1$ trials; there are $t-r$ failures overall. Use this when independent binary trials with constant $0<p<1$ continue until success $r$. When $p=1$, $T=r$ certainly; when $p=0$, the target is never reached. For $r=1$, $\binom{t-1}{0}=1$, giving $(1-p)^{t-1}p$, the geometric PMF.

The sum $\sum_{u=r}^{m}$ adds exact stopping probabilities for $u=r,r+1,\ldots,m$. Alternatively $T\leq m$ means at least $r$ successes in the first $m$ trials; a binomial tail provides another calculation.
'''
a=nb('Advanced general problem: target by a deadline',r'Independent trials have success probability 0.4. Stop at the third success.',3,.4,6,'by',extra='Verify using a binomial count in the first six trials.',post=r'For $B\sim\operatorname{Bin}(6,0.4)$, $P(T\leq6)=P(B\geq3)=1-\sum_{j=0}^{2}\binom6j(0.4)^j(0.6)^{6-j}=0.4557$. Both describe reaching three successes by trial 6.')
ref=reference([('$r$','Fixed target successes'),('$T,t$','Total trials and one stopping trial'),('$p$','Constant success probability per trial'),('$F=T-r$','Failures before success $r$'),(r'$\binom{t-1}{r-1}$','Arrangements before the mandatory final success')],routine)
p=[
nb('Two sales on call four',r'Independent calls each sell with probability 0.3. A sale is success; stop at two sales.',2,.3,4),
nb('Third approval on application five',r'In a hypothetical independent stream each application has approval probability 0.6. Approval is success; stop at the third approval.',3,.6,5,extra='Find the rejection count on this event.',post=r'$F=T-r=5-3=2$ rejected applications.'),
nb('Second invoice settled by contact four',r'Independent contacts each lead to a settlement with probability 0.5. Settlement is success; stop after two.',2,.5,4,'by'),
nb('Below the insurance-sales target',r'Independent offers each sell a policy with probability 0.2. Stop at three sales.',3,.2,6,'after',post=r'The target has not been reached after six offers: fewer than three successes occurred in those offers.'),
nb('Sales within an outreach budget',r'Each independent contact has sale probability 0.4 and costs 2 USD. The team needs three sales and has a 12 USD contact budget.',3,.4,6,'by',extra='Translate the budget into a stopping-trial event.',post=r'$C=2T$ USD gives $C\leq12$ exactly when $T\leq6$. The fixed budget does not guarantee reaching the target.'),
nb('Failure counts and a geometric special case',r'Independent recovery contacts succeed with probability 0.25. Stop at the second recovery; a report records three failures before it.',2,.25,5,extra='Translate three failures into total trials, then derive the model for target one.',post=r'$F=3$, $r=2$ imply $T=F+r=5$. For $r=1$, the PMF becomes $\binom{t-1}{0}(0.25)(0.75)^{t-1}=(0.75)^{t-1}(0.25)$, the geometric convention.')]
write(6,'Negative Binomial Trials to a Fixed Success Target',c6,intro,g,bridge,a,ref,[p[:2],p[2:4],p[4:]],r'The target $r$ is fixed and total trials $T$ are random. Include the final success. Use $\binom{t-1}{r-1}$, not $\binom tr$. Failures equal $T-r$. By-trial questions sum feasible stopping trials. Target one recovers geometric; fixed trials with random success count give binomial.')

c7='Evaluates rare-event situations with the Poisson distribution, interpreting the parameter λ in contexts such as claims, arrivals, defects, or defaults within a fixed interval.'
intro=r'''\subsection{Count events over an exposure}
A school shop receives occasional refund requests. Observe requests during one hour rather than fixing customer count. Let $X$ count requests in that hour. A Poisson variable has support $\{0,1,2,\ldots\}$ events: zero is possible and there is no fixed largest count.
'''+check('Does this variable measure time until the next request?',r'No. It counts events over a stated interval.')+r'''
\subsection{Rate and interval mean}
A rate of 0.5 requests per hour gives expected count $\lambda=0.5$ for one hour and $\lambda=1$ for two hours:
\[\lambda=\text{rate}\times\text{exposure}.\]
The Greek letter $\lambda$, read lambda, is the expected count in the chosen exposure. A rate in events per hour times hours gives events. The expected count may be non-integer, although observed counts are integers.
'''+check('At 2 claims per day, what mean applies to half a day?',r'$\lambda=2(0.5)=1$ claim.')+r'''
\subsection{Assumptions and notation}
Assume constant event rate, independent counts in disjoint intervals, and isolated events: in a very short interval the chance of one event is approximately proportional to its length and that of two or more is negligible. These assumptions do not follow from rarity. A shared storm can cluster claims. The constant $e\approx2.71828$ is a mathematical number on a calculator. Factorial means $k!=k(k-1)\cdots1$ and $0!=1$; for example $3!=6$.
'''+check(r'Why is $k=0$ allowed?',r'An interval can contain no events; $0!=1$.')+check('Does rarity alone establish Poisson?',r'No. Check rate stability, independent intervals and absence of clustering.')
def poimass(lam,k): return math.exp(-lam)*lam**k/math.factorial(k)
def poi(title,context,rate,exposure,unit,k,mode='exact',extra='',post=''):
    lam=rate*exposure
    event=f'X={k}' if mode=='exact' else f'X\\leq{k}' if mode=='atmost' else f'X\\geq{k}'
    if mode=='exact':
        sym=r'P(X=k)=e^{-\lambda}\lambda^k/k!'
        num=f'e^{{-{lam:g}}}({lam:g})^{k}/{k}!'
        val=poimass(lam,k)
    elif mode=='atmost':
        sym=r'P(X\leq b)=\sum_{j=0}^{b}e^{-\lambda}\lambda^j/j!'
        num=f'\\sum_{{j=0}}^{{{k}}} e^{{-{lam:g}}}({lam:g})^j/j!'
        val=sum(poimass(lam,j) for j in range(k+1))
    else:
        sym=r'P(X\geq a)=1-\sum_{j=0}^{a-1}e^{-\lambda}\lambda^j/j!'
        num=f'1-\\sum_{{j=0}}^{{{k-1}}}e^{{-{lam:g}}}({lam:g})^j/j!'
        val=1-sum(poimass(lam,j) for j in range(k))
    return problem(title,context,[f'Calculate $P({event})$ for the exposure. '+extra],[
('Define and identify units',f'$X$ counts events over {exposure:g} {unit}; support $\\{{0,1,2,\\ldots\\}}$ events. The count differs from rate and money.'),
('Check and scale',f'Under constant rate, independent disjoint-interval counts and isolated events, use Poisson. $\\lambda=\\text{{rate}}\\times\\text{{exposure}}={rate:g}\\times{exposure:g}={lam:g}$ events.'),
('Translate and calculate',f'The event is $ {event}$. Symbolically,\n\\[{sym}.\\]\nNumerically,\n\\[P({event})={num}\\approx {number(title,val)}.\\]'),
('Check and interpret',r'The probability is in $[0,1]$; the full Poisson PMF sums to 1. '+(r'For zero events, $\lambda^0=1$ and $0!=1$, so $P(X=0)=e^{-\lambda}$. ' if mode=='exact' and k==0 else '')+post)])
g=poi('Introductory general problem: two events in one unit',r'An ideal process has constant rate 1 event per exposure unit, independent disjoint-interval counts and isolated events.',1,1,'exposure unit',2)
bridge=r'''\[X\sim\operatorname{Pois}(\lambda),\qquad P(X=k)=\frac{e^{-\lambda}\lambda^k}{k!},\quad k=0,1,\ldots.\]
The numerator and factorial assign the mass at $k$. Use the mean for the interval in the question, not automatically the reported rate. If $\lambda=0$, no events occur with probability 1; for $\lambda>0$, support is all non-negative integers. The sum $\sum_{j=0}^{b}$ adds counts 0 through $b$; at least $a$ complements at most $a-1$.
'''
a=poi('Advanced general problem: rescaling and a complement',r'An ideal process has constant rate 0.8 events per hour, independent disjoint-interval counts and isolated events. Observe 2.5 hours.',.8,2.5,'hours',3,'atleast',extra='Explain why the parameter is not 0.8.',post=r'The interval mean is 2 events; 0.8 is the hourly rate. The complement includes 0, 1 and 2, not 3.')
ref=reference([('$X,k$','Event count and one non-negative integer value'),(r'$\lambda$','Expected count in the selected exposure'),('rate','Expected events per unit exposure'),('$e$','Mathematical constant, approximately 2.71828'),('$k!$','Factorial, with $0!=1$')],routine)
p=[
poi('No insurance claims',r'Isolated claims occur at constant rate 0.6 per day, with independent counts in disjoint intervals.',.6,1,'day',0),
poi('Two customer arrivals',r'A desk has isolated arrivals at constant rate 3 customers per hour, with independent disjoint-interval counts.',3,1,'hour',2),
poi('At most one defect',r'Defects occur singly at constant rate 0.02 per metre, with independent counts on disjoint lengths. Inspect 50 metres.',.02,50,'metres',1,'atmost'),
poi('At least one payment alert',r'Isolated alerts have constant rate 4 per hour and independent disjoint-interval counts. Observe 15 minutes.',4,.25,'hours',1,'atleast',extra='Convert 15 minutes to hours.',post=r'$15/60=0.25$ hours gives mean 1 alert. Multiplying an hourly rate by 15 minutes without conversion is a unit error.'),
poi('Claim costs over five days',r'Isolated claims have constant rate 0.4 per day and independent disjoint-interval counts. Observe five days; each claim costs exactly 100 USD.',.4,5,'days',3,'atleast',extra='Interpret as a probability of claim cost at least 300 USD.',post=r'$L=100X$ USD gives $L\geq300$ exactly when $X\geq3$. This translation relies on the fixed cost per claim.'),
poi('Defaults and a clustering warning',r'Version A has isolated defaults at constant rate 0.5 per month over stable exposure, with independent disjoint-interval counts. Observe two months. In version B, a market shock triggers many defaults together.',.5,2,'months',1,'atmost',extra='Calculate for A; explain why rarity alone does not justify the model for B.',post=r'Version B may have clustered events and dependent counts. Low frequency does not repair these failures; the numerical answer applies to A.')]
write(7,'Poisson Event Counts and Exposure',c7.replace('λ',r'$\lambda$'),intro,g,bridge,a,ref,[p[:2],p[2:4],p[4:]],r'Fix the interval and units first. Multiply rate by exposure for $\lambda$. Include zero and use $0!=1$. At least $a$ complements counts through $a-1$. Check stable rate, independent intervals and isolated events; rarity alone is insufficient. Money is a separate variable.')

c8='Calculates and interprets the expected value and variance of discrete probability distributions as measures of return and risk in economic and financial contexts.'
intro=r'''\subsection{A return is uncertain}
A school enterprise's daily net gain can be negative, zero or positive. A probability-weighted average summarises its distribution, but does not promise what tomorrow will bring. Let $X$ be gain in USD. The expected value, written $E(X)$ or $\mu$ (read mu), is $\sum_x xp_X(x)$. The sum sign means add one product for every supported value $x$.
'''+check('Does an expected gain of 3 USD guarantee 3 USD tomorrow?',r'No. It is a model-based long-run average, not a guaranteed outcome.')+r'''
\subsection{Calculate an average in small steps}
Multiply each possible value by its probability, then add. A negative return contributes a negative product. The result has the same units as $X$. Even for an integer count, the weighted average can be non-integer and need not lie in the support.
'''+check('Can a claim count have expected value 0.6?',r'Yes. Individual counts remain integers; their weighted average need not be.')+r'''
\subsection{Measure dispersion around the mean}
Variance is $\operatorname{Var}(X)=\sum_x(x-\mu)^2p_X(x)$. Subtract the mean, square each difference and weight it by its probability. Squaring prevents positive and negative deviations cancelling. An equivalent formula is $E(X^2)-\mu^2$. Standard deviation is $\sigma_X=\sqrt{\operatorname{Var}(X)}$, the non-negative square root. If $X$ is USD, variance is USD$^2$ and standard deviation is USD.
'''+check('Can variance be negative?',r'No. It is a weighted sum of non-negative squared deviations.')+r'''
\subsection{What this says about financial risk}
Greater variance means greater dispersion around the mean under the model. It does not alone describe loss probability, extreme losses, liquidity needs or the reliability of assumed probabilities. Equal-mean alternatives can have different variances, without one being universally best.
'''+check('Does lower variance alone prove an investment is best?',r'No. Financial goals, downside, constraints and model reliability also matter.')
def moments(values,probs):
    mu=sum(x*p for x,p in zip(values,probs))
    second=sum(x*x*p for x,p in zip(values,probs))
    return mu,second,second-mu*mu
def momenttable(values,probs):
    mu,m2,var=moments(values,probs)
    rows=[[f'{x:g}',f'{p:g}',f'{x*p:g}',f'{x*x*p:g}'] for x,p in zip(values,probs)]
    rows.append(['Total',f'{sum(probs):g}',f'{mu:g}',f'{m2:g}'])
    return table(['$x$','$p_X(x)$','$xp_X(x)$','$x^2p_X(x)$'],rows,'rrrr')
def momentproblem(title,context,values,probs,unit='USD',post='',extra=''):
    mu,m2,var=moments(values,probs)
    sd=math.sqrt(var)
    value_list=', '.join(f'{x:g}' for x in values)
    prob_list=', '.join(f'{p:g}' for p in probs)
    return problem(title,context+f' The variable $X$ takes values $ {value_list}$ {unit} with respective probabilities $ {prob_list}$.', ['Calculate expected value, variance and standard deviation using a calculation table; interpret their units. '+extra],[
('Define and validate',f'$X$ measures the stated quantity in {unit}; its support is the listed values. All probabilities are non-negative and total $ {sum(probs):g}$. This supplied PMF needs no independent-trials assumption.'),
('Organise the calculation',momenttable(values,probs)+f'The first column is in {unit}, the third in {unit} and the fourth in {unit}$^2$. Probabilities are unitless.'),
('Calculate symbolically then substitute',r'\[E(X)=\sum_xxp_X(x),\quad E(X^2)=\sum_xx^2p_X(x),\quad \operatorname{Var}(X)=E(X^2)-[E(X)]^2.\]'+f'The table gives $\\mu={mu:g}$ {unit} and $E(X^2)={m2:g}$ {unit}$^2$. Thus $\\operatorname{{Var}}(X)={m2:g}-({mu:g})^2={var:g}$ {unit}$^2$, and $\\sigma_X=\\sqrt{{{var:g}}}\\approx{number(title,sd)}$ {unit}.'),
('Check and interpret',f'The mean {mu:g} lies between {min(values):g} and {max(values):g}; variance is non-negative. The mean is a probability-weighted average, and standard deviation measures dispersion in the original units. '+post)])
g=momentproblem('Introductory general problem: a small score distribution',r'A general discrete experiment produces a score.',[0,1,2],[.25,.5,.25],'score units',post=r'Directly, $\sum_x(x-1)^2p_X(x)=1(0.25)+0(0.5)+1(0.25)=0.5$, agreeing with $E(X^2)-\mu^2$.')
bridge=r'''\[
\mu=E(X)=\sum_xxp_X(x),\qquad
\operatorname{Var}(X)=\sum_x(x-\mu)^2p_X(x)=E(X^2)-\mu^2.
\]
These formulas apply when the indicated sums are finite; all distributions used here have finite support. In $E(X^2)$, square each value \emph{before} taking the weighted average; this is different from squaring $E(X)$. Standard deviation is $\sqrt{\operatorname{Var}(X)}$.

For a transformed monetary amount $Y=aX+b$, where $a$ converts each unit of $X$ into money and $b$ is a fixed monetary amount,
\[E(Y)=aE(X)+b,\qquad \operatorname{Var}(Y)=a^2\operatorname{Var}(X),\qquad \sigma_Y=|a|\sigma_X.\]
Adding a fixed amount moves every value equally and does not change dispersion. A negative multiplier reverses the order of values, but its square keeps variance non-negative.
'''
a=problem('Advanced general problem: same mean, different spread',r'Model A has values $-2,2,6$ with probabilities $0.25,0.5,0.25$. Model B is always 2. Let $Y=3X-1$ USD when $X$ follows A.',['Compare the means and variances; calculate the transformed mean, variance and standard deviation.'],[
('Define and validate',r'$X$ is a score under A, support $\{-2,2,6\}$. B has support $\{2\}$ with mass 1. Both are valid PMFs. $Y$ is money, support $\{-7,5,17\}$ USD.'),
('Tabulate A',momenttable([-2,2,6],[.25,.5,.25])),
('Calculate and compare',r'For A, $E(X)=2$, $E(X^2)=12$, so $\operatorname{Var}(X)=12-2^2=8$. For B, $E(B)=2$ and $\operatorname{Var}(B)=(2-2)^2=0$. Their means agree but their dispersions differ.'),
('Transform',r'$E(Y)=aE(X)+b=3(2)-1=5$ USD. $\operatorname{Var}(Y)=a^2\operatorname{Var}(X)=3^2(8)=72$ USD$^2$, $\sigma_Y=\sqrt{72}\approx8.4853$ USD.'),
('Check and interpret',r'Directly $(-7)(0.25)+5(0.5)+17(0.25)=5$ USD. The fixed subtraction affects the mean but not variance. Lower spread does not by itself determine a universally preferred financial choice.')])
ref=reference([('$p_X(x)$','Mass at value $x$; no units'),(r'$\sum_x$','Add over supported values'),('$E(X)=\mu$','Mean; same units as $X$'),('$E(X^2)$','Weighted mean of squared values'),(r'$\operatorname{Var}(X)$','Mean squared deviation; squared units'),(r'$\sigma_X$','Standard deviation; original units'),('$a,b$','Multiplier and fixed addition in $Y=aX+b$')],routine)
p=[
momentproblem('School-enterprise net gain',r'A school enterprise records one-day net gain.',[-10,10,30],[.25,.5,.25],post=r'The chance of a loss is $P(X<0)=0.25$. An expected gain of 10 USD does not remove that possibility.'),
momentproblem('Insurance claim counts',r'A small portfolio records its claim count in one day.',[0,1,2],[.5,.4,.1],'claims',post=r'The mean 0.6 claims is not a possible observed count. It describes an average over repetitions of the daily model.'),
momentproblem('Sales and a fixed operating cost',r'A business counts daily sales; each sale contributes 8 USD and a daily fixed operating cost is 5 USD.',[0,1,2],[.2,.5,.3],'sales',extra=r'Find the moments of net gain $Y=8X-5$ USD.',post=r'$E(Y)=8E(X)-5=8(1.1)-5=3.8$ USD. $\operatorname{Var}(Y)=8^2\operatorname{Var}(X)=64(0.49)=31.36$ USD$^2$ and $\sigma_Y=8(0.7)=5.6$ USD. The monetary support is $\{-5,3,11\}$ USD.'),
problem('Equal-mean investment alternatives',r'Alternative A yields 0 or 20 USD, each with probability $1/2$. B yields 5 or 15 USD, each with probability $1/2$.',['Use calculation tables to compare mean, variance and standard deviation, and give a limited financial conclusion.'],[
('Define and validate',r'$A$ and $B$ are monetary gains with supports $\{0,20\}$ and $\{5,15\}$ USD. Each PMF totals 1. No joint independence assumption is needed to compare their separate distributions.'),
('Tabulate',r'\textbf{A:}'+momenttable([0,20],[.5,.5])+r'\textbf{B:}'+momenttable([5,15],[.5,.5])),
('Calculate',r'$E(A)=10$ USD, $\operatorname{Var}(A)=200-10^2=100$ USD$^2$, $\sigma_A=10$ USD. $E(B)=10$ USD, $\operatorname{Var}(B)=125-10^2=25$ USD$^2$, $\sigma_B=5$ USD.'),
('Check and interpret',r'Both means are within their supports bounds. B has the same mean and less dispersion. A allows a higher gain and a lower gain; a recommendation still depends on objectives and constraints. Neither expected return is a promise.')]),
momentproblem('Claims and a reserve balance',r'A firm has reserve 100 USD and pays 30 USD per claim; $X$ counts daily claims.',[0,1,2],[.6,.3,.1],'claims',extra=r'Find moments of remaining reserve $Y=100-30X$ USD.',post=r'$E(Y)=100-30(0.5)=85$ USD. $\operatorname{Var}(Y)=(-30)^2(0.45)=405$ USD$^2$; $\sigma_Y=\sqrt{405}\approx20.1246$ USD. Reserve values are $\{100,70,40\}$ USD. A negative multiplier does not produce negative variance.'),
problem('What equal variance can hide',r'Investment A yields $-10$ or 10 USD with equal probability. B yields $-20,0,20$ USD with probabilities $0.125,0.75,0.125$.',['Calculate both means and variances; compare loss probabilities and worst outcomes; evaluate the claim that equal mean and variance imply identical risk.'],[
('Define and validate',r'$A$ and $B$ measure net gains in USD. Their listed supports are finite and each positive PMF totals 1.'),
('Tabulate',r'\textbf{A:}'+momenttable([-10,10],[.5,.5])+r'\textbf{B:}'+momenttable([-20,0,20],[.125,.75,.125])),
('Calculate',r'$E(A)=E(B)=0$. For each, $\operatorname{Var}=E(X^2)-\mu^2=100-0^2=100$ USD$^2$ and $\sigma=10$ USD. Yet $P(A<0)=0.5$ and $P(B<0)=0.125$.'),
('Check and interpret',r'A loses more often but its worst loss is 10 USD; B loses less often but can lose 20 USD. Equal mean and variance do not imply identical downside or identical financial risk. Neither statistic alone determines a universally best choice.')])]
write(8,'Expected Return, Variance and Financial Dispersion',c8,intro,g,bridge,a,ref,[p[:2],p[2:4],p[4:]],r'Weight every value, including negative returns, by its probability. $E(X^2)$ is not $[E(X)]^2$. Variance uses squared units; standard deviation uses original units. A fixed addition leaves variance unchanged; scaling multiplies it by $a^2$. Expected values are averages, not guarantees. Dispersion does not fully describe financial risk.')

c9='Compares Bernoulli, binomial, negative binomial, geometric, and Poisson distributions by selecting the most appropriate model for a given financial-risk situation.'
intro=r'''\subsection{Ask what is random}
A school enterprise can record whether one visitor buys, sales among ten visitors, contacts until its first sale, contacts until its third sale, or arrivals during an hour. These are different questions even if all describe the same shop. Start by defining the variable; the word sales alone does not choose a distribution.
'''+check('One customer either buys or does not: which model?',r'Bernoulli, if 1 labels buying and 0 labels not buying.')+r'''
\subsection{Find what is fixed}
Fixed trials with random success count suggest binomial. Fixed target successes with random total trials suggest geometric for target one or negative binomial for target $r$. Event counts over fixed exposure suggest Poisson when its process assumptions hold. Counts have count units, probabilities are unitless and monetary consequences need a separate definition.
'''+check('Ten calls regardless of results: is this geometric?',r'No. A success count over ten fixed calls suggests binomial.')+r'''
\subsection{Recall notation before choosing}
The symbol $\sim$ is read as has the distribution. In a PMF, $P(X=k)$ is the probability of exactly value $k$. The factorial is $k!=k(k-1)\cdots1$, with $0!=1$. Combinations count success-position choices: $\binom nk=n!/[k!(n-k)!]$. A sum $\sum_{j=0}^{b}$ adds the terms for integers 0 through $b$. In Poisson, $e\approx2.71828$ and $\lambda$ (lambda) is the interval mean, not automatically a rate.
'''+check('Which model counts trials until success three?',r'Negative binomial with target $r=3$, including the final successful trial.')+check('Is a rare default automatically Poisson?',r'No. Define the exposure and check constant rate, independent interval counts and isolated events.')
g=problem('Introductory general problem: same trials, different variables',r'Independent binary trials have constant success probability $1/2$. Variable $A$ indicates success on trial one; $B$ counts successes in three fixed trials; $T$ counts trials until first success.',['Select each model, state parameters and support, reject an alternative and calculate $P(A=1)$, $P(B=1)$ and $P(T=3)$.'],[
('Define and select',r'$A\sim\operatorname{Bernoulli}(0.5)$ with support $\{0,1\}$, $B\sim\operatorname{Bin}(3,0.5)$ with support $\{0,1,2,3\}$ successes, and geometric $T$ with $p=0.5$ and support $\{1,2,\ldots\}$ trials.'),
('Check and reject',r'Binary independent constant-probability trials are supplied. A is one label rather than a trial count; B fixes trials rather than waiting for success; T waits rather than observing all three fixed trials. These distinctions reject the corresponding plausible alternatives.'),
('Calculate',r'$P(A=1)=p=0.5000$; $P(B=1)=\binom31p(1-p)^2=3(0.5)(0.5)^2=0.3750$; $P(T=3)=(1-p)^2p=(0.5)^2(0.5)=0.1250$.'),
('Check and interpret',r'The last event is FFS, whereas the middle event includes SFF, FSF and FFS. The threefold difference checks that the stopping rule was used correctly.')])
bridge=r'''\textbf{Comparison reference.} Supports below assume $0<p<1$ and $\lambda>0$. Trials are binary; success must always be stated explicitly. All PMFs are zero outside their stated support.
\begin{center}\small
\begin{tabularx}{\linewidth}{@{}p{0.13\linewidth}p{0.43\linewidth}X@{}}
\toprule Model & What is observed, fixed rule, support and parameters & Assumptions and PMF\\\midrule
Bernoulli & One binary label; one observation in a specified period. Support $\{0,1\}$. Parameter $p$. & Two exhaustive, exclusive labels. No repeated-trial independence required. $P(X=x)=p^x(1-p)^{1-x}$.\\[5pt]
Binomial & Number of successes; fixed $n$ trials. Support $\{0,\ldots,n\}$. Parameters $n,p$. & Independent binary trials with constant $p$. $P(X=k)=\binom nkp^k(1-p)^{n-k}$.\\[5pt]
Geometric & Total trials to first success; stop at success one. Support $\{1,2,\ldots\}$. Parameter $p$. & Independent binary trials with constant $p>0$. $P(T=t)=(1-p)^{t-1}p$.\\[5pt]
Negative binomial & Total trials to success $r$; stop at fixed target $r$. Support $\{r,r+1,\ldots\}$. Parameters $r,p$. & Independent binary trials with constant $p>0$. $P(T=t)=\binom{t-1}{r-1}p^r(1-p)^{t-r}$.\\[5pt]
Poisson & Event count in fixed time, area or exposure. Support $\{0,1,\ldots\}$. Parameter $\lambda=\text{rate}\times\text{exposure}$. & Constant rate, independent disjoint-interval counts, isolated events. $P(X=k)=e^{-\lambda}\lambda^k/k!$.\\
\bottomrule
\end{tabularx}\end{center}
\textbf{Model-selection flowchart.} Follow a yes arrow to a candidate, then check its assumptions. A candidate is not a confirmed model until those checks pass.
\begin{center}
\begin{tikzpicture}[q/.style={draw,rounded corners,text width=7cm,align=center,font=\small},a/.style={draw,text width=5cm,align=center,font=\small},>=Stealth]
\node[q] (q1) at (0,0) {One binary indicator?};
\node[a] (a1) at (8,0) {Bernoulli: identify $p$};
\node[q] (q2) at (0,-1.2) {Success count in fixed $n$ trials?};
\node[a] (a2) at (8,-1.2) {Binomial: identify $n,p$};
\node[q] (q3) at (0,-2.4) {Total trials until first success?};
\node[a] (a3) at (8,-2.4) {Geometric: identify $p$};
\node[q] (q4) at (0,-3.6) {Total trials until success $r$?};
\node[a] (a4) at (8,-3.6) {Negative binomial: identify $r,p$};
\node[q] (q5) at (0,-4.8) {Event count over fixed exposure?};
\node[a] (a5) at (8,-4.8) {Poisson: find interval mean $\lambda$};
\node[q] (q6) at (0,-6.1) {More information or another model needed};
\foreach \i in {1,2,3,4,5}{\draw[->] (q\i) -- node[above,font=\small]{yes} (a\i);}
\foreach \i/\j in {1/2,2/3,3/4,4/5,5/6}{\draw[->] (q\i) -- node[right,font=\small]{no} (q\j);}
\end{tikzpicture}
\end{center}
If an assumption fails, do not force the scenario into a familiar distribution. State the missing information or explain the unsuitable assumption.
'''
a=problem('Advanced general problem: target versus interval',r'Process A consists of independent calls with sale probability 0.4, stopping at the second sale. Process B has isolated arrivals at constant rate 0.5 per hour with independent disjoint-interval counts; observe four hours.',['Select models and supports, reject a plausible alternative for each, and calculate the chance A stops on call four and B has at least one arrival.'],[
('Define and select',r'$T$ counts calls until sale two, so use negative binomial with $r=2,p=0.4$, support $\{2,3,\ldots\}$ calls. $X$ counts arrivals in four hours, so use Poisson with $\lambda=0.5(4)=2$, support $\{0,1,\ldots\}$ arrivals.'),
('Check and reject',r'A supplies independent constant-probability binary trials, but target two rejects geometric. B supplies Poisson process assumptions; binomial is unsuitable because no fixed number of binary trials is specified.'),
('Calculate',r'$P(T=4)=\binom{4-1}{2-1}p^2(1-p)^2=\binom31(0.4)^2(0.6)^2=0.1728$. Also $P(X\geq1)=1-P(X=0)=1-e^{-\lambda}=1-e^{-2}\approx0.8647$.'),
('Check and interpret',r'A permits SS only if stopping on call two, so fixing the final success on four matters. For B, zero and at least one partition all arrivals. Both answers are probabilities rather than call or arrival counts.')])
ref=reference([('$X$','Indicator or fixed-exposure success/event count'),('$T$','Total trials until the specified target success'),('$n$','Fixed trial count'),('$r$','Fixed target successes'),('$p$','Success probability per binary trial'),(r'$\lambda$','Expected events in the selected exposure')],[r'Define the variable and distinguish counts, trial numbers and monetary amounts.',r'Identify what is fixed: one observation, trials, target success or exposure.',r'State support, parameters and units; explicitly define success.',r'Check assumptions and reject at least one plausible alternative.',r'Translate and calculate with a symbolic PMF or complement before substitution.',r'Check the result; if information is insufficient, explain why no unique probability follows.'])
p=[
problem('One loan: a binary event',r'One loan defaults within a year with probability 0.07; default causes a fixed loss of 500 USD.',['Define the indicator, choose and justify the model, reject binomial with ten trials, and find the probability of a 500 USD default loss.'],[
('Define and choose',r'$X=1$ for default within a year and 0 otherwise. It is Bernoulli with $p=0.07$, support $\{0,1\}$, no monetary units.'),
('Justify and reject',r'This is one binary observation. No independence assumption is needed. A ten-trial binomial would describe a different variable and ten loans that are not specified.'),
('Calculate',r'$L=500X$ USD, so $P(L=500)=P(X=1)=p^1(1-p)^0=0.07=0.0700$.'),
('Check and interpret',r'The other mass is $1-p=0.93$ and the total is 1. Success denotes an undesirable default; 500 USD is a loss size, not a probability.')]),
problem('Five independent invoice payments',r'Five invoices are independently paid on time, each with probability 0.8. Observe all five.',['Define the success count, choose the model and parameters, reject geometric and calculate exactly four on-time payments.'],[
('Define and choose',r'$X$ counts on-time payments among five fixed invoices; success means on-time payment. $X\sim\operatorname{Bin}(5,0.8)$ with support $\{0,\ldots,5\}$ payments.'),
('Justify and reject',r'Fixed trials, binary outcomes, independence and constant $p$ are supplied. Geometric would stop at the first on-time payment rather than observe all five.'),
('Calculate',r'$P(X=4)=\binom54p^4(1-p)^{5-4}=5(0.8)^4(0.2)=0.4096$.'),
('Check and interpret',r'The PMF total is $(0.8+0.2)^5=1$. The combination counts which one invoice is late. The answer is a 40.96\% probability, not an expected payment count.')]),
problem('First insurance sale',r'Independent offers each sell a policy with probability 0.25. Continue until the first sale.',['Define the trial variable, choose and justify the model, reject fixed-trial binomial and calculate first sale after call three.'],[
('Define and choose',r'$T$ is total calls up to the first sale; success is a sale. Use geometric with $p=0.25$, support $\{1,2,\ldots\}$ calls.'),
('Justify and reject',r'The independent constant-probability binary process stops at first success. Binomial fixes trials and counts successes, which is a different observation rule.'),
('Calculate',r'$P(T>3)=(1-p)^3=(0.75)^3=0.421875\approx0.4219$.'),
('Check and interpret',r'All first three calls must fail. Its complement $P(T\leq3)=1-0.421875=0.578125$ completes total probability 1. After three excludes sale on call three.')]),
problem('Third contract signed on visit five',r'Independent visits each sign a contract with probability 0.4. Stop at the third signature.',['Define total trials, select parameters and support, reject geometric and find $P(T=5)$. State failures.'],[
('Define and choose',r'$T$ counts visits through signature three. Negative binomial has $r=3,p=0.4$ and support $\{3,4,\ldots\}$ visits.'),
('Justify and reject',r'Binary, independent, constant-probability visits stop at target three; geometric targets just one and is unsuitable.'),
('Calculate',r'$P(T=5)=\binom{t-1}{r-1}p^r(1-p)^{t-r}=\binom42(0.4)^3(0.6)^2=0.13824\approx0.1382$.'),
('Check and interpret',r'The first four visits contain two successes; visit five succeeds. There are $F=T-r=5-3=2$ failures. This is not simply three successes anywhere in five visits.')]),
problem('Claims in a half-day exposure',r'Isolated claims arrive at constant rate 3 per day with independent counts on disjoint intervals. Observe half a day. Each claim costs 200 USD.',['Define the count, select and justify the model, reject binomial and calculate the probability of at least 400 USD claim cost.'],[
('Define and choose',r'$X$ counts claims in half a day, support $\{0,1,\ldots\}$. Poisson mean is $\lambda=\text{rate}\times\text{exposure}=3(0.5)=1.5$ claims.'),
('Justify and reject',r'Constant rate, independent interval counts and isolated events are supplied. No fixed number of independent binary opportunities is given, so binomial is not justified.'),
('Calculate',r'$L=200X$ USD gives $L\geq400$ when $X\geq2$. Thus $P(X\geq2)=1-[P(X=0)+P(X=1)]=1-e^{-\lambda}(1+\lambda)=1-e^{-1.5}(1+1.5)\approx0.4422$.'),
('Check and interpret',r'The complement includes zero or one claim, cost below 400 USD. The mean 1.5 refers to half a day, not a full day; observed counts remain integers.')]),
problem('When the information cannot choose a count model',r'Five loans each have one-year default probability 0.1. They may share a market shock; their dependence is unspecified. A separate call campaign says only that sales are infrequent, without a numerical sale probability or a stopping rule.',['Assess a binomial model for the loan default count, calculate one loan default probability, show that the chance all five default is not uniquely determined, and identify missing campaign information.'],[
('Define and assess',r'$X$ counts defaults among five loans, possible values $\{0,\ldots,5\}$. Fixed binary observations are present, but independence is not supplied. Binomial $(5,0.1)$ cannot be asserted. For one specified loan, $I=1$ for default is Bernoulli $(0.1)$ with support $\{0,1\}$.'),
('Calculate what is known',r'$P(I=1)=p^1(1-p)^0=0.1000$. If all five defaults were independent, $P(X=5)=p^5=(0.1)^5=0.00001$. If one common shock caused all five to default together with probability 0.1, then $P(X=5)=0.1$. Both constructions have the supplied individual default probabilities.'),
('Reject unjustified alternatives',r'The different joint probabilities prove no unique aggregate answer follows. Poisson is also unsupported: a fixed five-loan count and possible common shocks do not supply an isolated-event constant-rate process. For the campaign, define whether counting successes in fixed trials or trials to a target, supply $p$ and test independence and constancy before selecting binomial, geometric or negative binomial.'),
('Check and interpret',r'The exact small value $0.00001$ is retained rather than rounded to zero. A single-loan probability can be known while portfolio clustering risk remains unresolved. No numerical campaign probability is justified by the word infrequent.')])]
write(9,'Selecting and Justifying Discrete Probability Models',c9,intro,g,bridge,a,ref,[p[:2],p[2:4],p[4:]],r'Choose from the variable and observation rule, then verify assumptions. Bernoulli labels one outcome; binomial counts successes in fixed trials; geometric and negative binomial count total trials to fixed success targets; Poisson counts events in fixed exposure. State support and parameter units, reject a plausible alternative and acknowledge insufficient information. Monetary consequences are separate from event counts.')

if __name__=='__main__':
    print('Created nine activities in',OUT)
