from pathlib import Path
import math

OUT = Path('book2026-2027/grade10/term_2/1-practice_activities')
OUT.mkdir(parents=True, exist_ok=True)
records = []
def number(tag, value):
    records.append((tag, value))
    return f'{value:.4f}'
def table(headers, rows, spec=None):
    spec = spec or 'l' * len(headers)
    return '\\begin{center}\n\\begin{tabular}{'+spec+'}\n\\toprule\n'+' & '.join(headers)+r' \\ \midrule'+'\n'+'\n'.join(' & '.join(map(str,row))+r' \\' for row in rows)+'\n\\bottomrule\n\\end{tabular}\n\\end{center}\n'
def problem(title, statement, tasks, steps):
    return '\\subsection{'+title+'}\n'+statement+'\n\n\\textbf{Questions/Tasks}\n\\begin{enumerate}\n'+''.join('\\item '+t+'\n' for t in tasks)+'\\end{enumerate}\n\\subsubsection*{Complete worked solution}\n'+''.join('\\textbf{Step '+str(i)+': '+heading+'.} '+body+'\n\n' for i,(heading,body) in enumerate(steps,1))
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
    body=head+intro+'\\section{General worked problems}\n'+general+'\\subsection{Bridge to the general model}\n'+bridge+advanced+ref
    for level,items in zip(['Foundational','Intermediate','Advanced'],practice):
        body+='\\clearpage\n\\section{'+level+' contextual practice}\\label{sec:'+prefix+'-'+level.lower()+'}\n'
        for j,p in enumerate(items,1):
            body+=p+'\\secInicio[][sec:'+prefix+'-'+level.lower()+']\n'
    body+='\\section{Closing reference: key ideas and common errors}\n'+closing+'\n\\secInicio\n\\end{document}\n'
    path=OUT/f'G10_T1_L{lesson}_C{c}_practice_activity.tex'
    path.write_text(body,encoding='utf-8')

# C1: outcomes, numerical mappings and probability mass.
c1='Characterises discrete random variables in economic and financial contexts by identifying their support, probability mass function and possible outcomes.'
intro=r'''\subsection{From a school sale to a number}
A school enterprise offers a notebook to each of two visitors. Each visitor either buys (B) or does not buy (N). An \emph{outcome} records the whole story, such as BN: first visitor buys, second does not. A \emph{random variable} assigns a number to every outcome. Let $X$ be the number of buyers. Then $X(\mathrm{BN})=1$, read ``X of BN equals one''. The capital letter names the rule; a small $x$ names a possible or observed numerical value.
''' + check('Are BN and NB the same outcome?',r'No; they record different visitors buying, but both give $X=1$.')+r'''
\subsection{Support, measurements and units}
The \emph{support} is the set of values with positive probability. Here it can be $\{0,1,2\}$ buyers. Braces mean ``the set containing''. A discrete support is finite or can be listed as a sequence, even if the list never ends. A waiting count $1,2,3,\ldots$ is countably infinite; the dots mean ``continue with the same pattern''. An exact processing time can take any real value in a time interval and is modelled as continuous. Rounded time records can instead be discrete.
''' +check(r'Can the buyer count be $1.6$?',r'No. Counts are integers; the support contains only 0, 1 and 2.')+r'''
\subsection{Assign probability to each value}
The \emph{probability mass function} (PMF) is $p_X(x)=P(X=x)$, read ``the probability that X equals x''. The subscript identifies the variable. Every mass must be non-negative and the masses must add to 1. A value outside the support has mass zero. To find a mass, add the probabilities of all outcomes mapped to that value; do not assume outcomes are equally likely unless stated.
''' +check(r'Is $p_X(1)=0.4$ a payment of 0.4 USD?',r'No. It is a dimensionless probability, or 40\%.')+check(r'If a sale earns 5 USD, are $X$ and $5X$ the same quantity?',r'No. $X$ counts buyers and $5X$ measures revenue in USD.')
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
