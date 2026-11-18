from pathlib import Path
from decimal import Decimal as D

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT/'book2026-2027/grade11/term_2/4-learning_evidences'
OUT.mkdir(parents=True, exist_ok=True)
name = 'G11_T2_L1_C1C2_exam_solution'
parts = [r'''% Governing source: user assessment brief; original integrated questions.
% Reference activities: ../2-class_activities/G11_T2_L1_C1_classroom_activity.tex
% and G11_T2_L1_C2_classroom_activity.tex. No archived exam is governing.
% Build from this directory; TEXINPUTS must include ../../../preamble/.
\makeatletter
\def\input@path{{../../../preamble/}}
\makeatother
\input{preamble_exams.tex}
\usepackage{needspace}
\hypersetup{pdftitle={Grade 11 Term 2 C1 and C2 Exam Solutions},pdfauthor={Global Economics}}
\raggedbottom
\linespread{1.04}
\setlength{\parskip}{4pt}
\newcolumntype{K}{>{\raggedright\arraybackslash}X}
\newcommand{\keytable}[2]{\par\begingroup\small\renewcommand{\arraystretch}{1.10}%
\begin{tabularx}{\linewidth}{#1}\toprule #2\bottomrule\end{tabularx}\par\endgroup}
\newcommand{\taskprompt}[3]{\Needspace{5\baselineskip}\par\textbf{Original task: #1}\score{#2}\par #3\par}
\newcommand{\worked}[2]{\subsection*{Worked solution: #1}\label{#2}}
\newcommand{\cOneA}{Identify the population and both samples, with place, period, eligibility and sizes. Pair population parameters with sample statistics for the mean, standard deviation and proportion. Interpret every measure with units where appropriate; compute both sample proportions from their condition counts. Distinguish known quantities from those not established by the information.}
\newcommand{\cOneB}{Compare the second sample with the initial sample. Calculate changes in the mean, sample standard deviation and proportion, using percentage points for the last. Explain which population characteristics remain fixed and why sample differences do not establish changes in population parameters.}
\newcommand{\cTwoA}{Organize the initial study using the C2 reference categories: population parameters, sample statistics and procedure settings. Identify the initially unknown mean and its later established value. Calculate the standard error; identify confidence, significance, each tail area and critical value for every requested level.}
\newcommand{\cTwoB}{Using the initial sample, state the point estimate and calculate the margin of error, lower and upper endpoints, confidence interval and full width for each requested confidence level. Complete a reference-style calculation table; show formulas, substitutions, units and contextual interpretation. Use the known population standard deviation.}
\newcommand{\cTwoC}{Use only the subsequent studies to determine interval coverage at each level and its absolute difference from nominal confidence in percentage points. Interpret long-run coverage and finite-study variation. Distinguish interval coverage from sample means lying inside the initial interval, and avoid assigning probability to a fixed mean after an interval is calculated.}
\title{Grade 11 -- Term 2\\C1 and C2 Integrated Exam --- Solutions}
\author{Global Economics}
\date{2026--2027}
\begin{document}
\maketitle
\setcounter{tocdepth}{1}
\phantomsection\label{toc}\tableofcontents
\section*{Learning objective}
Distinguish fixed population parameters from variable sample statistics in economic and financial contexts; calculate known-population-standard-deviation confidence intervals and interpret their long-run coverage.
\section*{Criteria assessment}
Answer exactly three problems. Problems 1 and 2 each award 3 points to C1 and 3 to C2, for 6 points each. Problem 3 is worth 5 points overall. Its equal allocation of 2.5 to C1 and 2.5 to C2 is \textbf{proposed}: the governing brief specifies only its overall value.

With that proposed split, C1 has 8.5 available points, C2 has 8.5 and the exam has 17. \textbf{Each criterion requires at least 4 points to pass independently. Points cannot transfer between criteria.} An overall total alone does not establish a pass in both criteria. These are the exam's thresholds; no cumulative assessment policy is supplied.
\section*{Evaluated criteria}
\begin{description}
\item[C1] Distinguishes population parameters from sample statistics by interpreting and comparing population and sample means, standard deviations and proportions in economic and financial contexts.
\item[C2] Compares point and interval estimation and interprets confidence through long-run coverage, distinguishing this from probability assigned to a particular calculated interval containing the parameter.
\end{description}
\textbf{Use of this key.} Each original question is printed with its data; every task appears before its worked solution. Links lead to solutions; return arrows lead to the question and contents. All detailed marking breakdowns below are proposed partial-credit guidance under the prescribed task marks. Hypothetical data are used throughout.
\clearpage
\section*{Task reference material}
\textbf{C1 pairings.} Population $\mathcal P$, size $N$; sample $X$, size $n$; population/sample mean $(\mu,\bar x)$; standard deviation $(\sigma,s)$; proportion $(p,\hat p)$. A condition count is $k$, so $\hat p=k/n$. A sample-proportion change is $100(\hat p_B-\hat p_A)$ percentage points.

\textbf{C2 information table.} Use contiguous groups in this order: Population parameters ($\mu,\mu_{\mathrm{known}},\sigma$); Sample statistics ($\bar x,n,\mathrm{SE}$); Procedure settings ($C,\alpha,\alpha/2,z^*$). Columns are Symbol, Concept, Type and Meaning in context. As in the classroom reference, the derived SE is placed in the sample-statistics group; here it uses known $\sigma$ and fixed $n$, so it is not an estimate using $s$. The later-known notation refers to the same fixed mean, not a second parameter.

\textbf{Two-sided standard normal reference.} Use the following numerical critical values for all calculations. They are supplied rounded values; retain all digits generated by them when calculating endpoints and widths.
\keytable{KKK}{
\textbf{Confidence level}&\textbf{Area below positive critical value}&\textbf{Positive critical value}\\\midrule
90\%&0.950&1.645\\
95\%&0.975&1.960\\
99\%&0.995&2.576\\}
\[
\begin{aligned}
\alpha&=1-C,& \text{each tail}&=\alpha/2,&\mathrm{SE}&=\frac{\sigma}{\sqrt n},\\
\mathrm{MoE}&=z^*\mathrm{SE},&L&=\bar x-\mathrm{MoE},&U&=\bar x+\mathrm{MoE},\\
\mathrm{CI}&=[L,U],&W&=U-L=2\mathrm{MoE}.&&
\end{aligned}
\]
For each confidence level separately, a subsequent interval covers when
$L_i\leq\mu_{\mathrm{known}}\leq U_i$. Equality at an endpoint counts as coverage.
\[
\mathrm{Cov}(C)=\frac{N_{\mathrm{cover}}(C)}{N(C)}\,100\%,\qquad
E_{\mathrm{abs}}(C)=|\text{observed percentage}-100C|\text{ percentage points}.
\]
The interval table uses Symbol, Concept, Calculation and Result and meaning in context, with separate endpoint rows. Proportions and confidence settings are unitless; a mean, standard deviation, standard error, margin, endpoint and width use the measurement's units.

\textbf{Common procedure assumptions.} The scenarios specify independent random studies, negligible within-study sampling fractions and sufficiently regular numerical populations for a normal approximation to the sampling distribution of the mean. The finite-population correction is negligible and omitted. Thus nominal normal coverage is an approximation, additionally subject to supplied critical-value rounding. Sample standard deviations describe samples; they do not replace known population standard deviations in this procedure.
\secInicio
''']

data = [
dict(i=1,title='Retail electricity costs',unit='thousand COP',measure='October electricity bill',condition='used electronic invoicing in October',
 scope='all 200,000 registered retail businesses operating in Medellin throughout October 2026',N=200000,n=100,a=240,s=58,k=40,b=252,t=66,j=55,sigma=60,mu=245,levels=[('95',D('1.960'))],centers=[236,244,250,258,230,247,242,254,233,246],
 context=r'''An energy-cost review concerns all 200,000 registered retail businesses operating in Medellin throughout October 2026. Each business contributes its total October electricity bill, measured in thousand COP. A separate yes-or-no condition records whether the business used electronic invoicing in October.

The initial independent random sample contains 100 businesses. Its mean bill is 240 thousand COP, its sample standard deviation is 58 thousand COP, and 40 businesses used electronic invoicing. A second independent random sample from exactly the same business population and October period also contains 100 businesses. Its mean bill is 252 thousand COP, its sample standard deviation is 66 thousand COP, and 55 businesses used electronic invoicing.

A certified spread-only population report makes the population standard deviation of October bills known as 60 thousand COP; it does not disclose the population mean. The two sample standard deviations remain separate descriptive quantities. The initial study estimates the initially unknown mean at 95\% confidence.

Assume the bill distribution is sufficiently regular, without dominant outliers, for a normal approximation to sample means of this size. Each study draws a simple random sample without replacement from the full fixed register. Samples are selected independently across studies; overlap between different samples is permitted. Each study selects only 0.05\% of the population, so dependence within a draw and the finite-population correction are negligible.

Ten subsequent independent studies each use 100 businesses, the same known population standard deviation and the same 95\% normal confidence procedure. These are additional studies, separate from both samples above. A later comprehensive investigation of the entire October population establishes its mean bill as 245 thousand COP. Repeated samples do not establish this value. The following subsequent intervals allow retrospective assessment; all endpoints are in thousand COP.'''),
dict(i=2,title='Savings-account interest',unit='thousand COP',measure='October interest credit',condition='had mobile banking activated on October 31',
 scope='all 500,000 positive-balance personal savings accounts at the Cartagena branch network on October 31, 2026',N=500000,n=144,a=82,s=33,k=54,b=79,t=39,j=72,sigma=36,mu=84,levels=[('90',D('1.645')),('99',D('2.576'))],
 context=r'''A bank reviews all 500,000 positive-balance personal savings accounts at its Cartagena branch network on October 31, 2026. The numerical measurement is the total interest credited to each eligible account during October 2026, in thousand COP. A separate yes-or-no condition records whether the account had mobile banking activated on October 31.

The initial independent random sample contains 144 eligible accounts, with mean October interest of 82 thousand COP, sample standard deviation of 33 thousand COP and 54 accounts with mobile banking activated. A second independent random sample of 144 accounts from exactly the same eligible population and period has mean interest of 79 thousand COP, sample standard deviation of 39 thousand COP and 72 accounts with mobile banking activated.

A certified spread-only report establishes the population standard deviation of October interest as 36 thousand COP while withholding the population mean. This known spread differs from both sample standard deviations. The initial study estimates the initially unknown population mean at 90\% and 99\% confidence.

Assume a sufficiently regular interest distribution without dominant outliers and a valid normal approximation for sample means of this size. Each study draws a simple random sample without replacement from the same full fixed register; draws across studies are independent and may overlap. Each sample contains only 0.0288\% of the population, so the finite-population correction is negligible.

Two hundred subsequent independent studies, separate from the two samples above, each select 144 accounts and use the same known population standard deviation and both confidence procedures. Each study builds both intervals around its own sample mean. The 99\% interval is wider and contains that study's 90\% interval. A later comprehensive investigation of all eligible accounts establishes mean October interest as 84 thousand COP; the repeated samples do not establish it. The table records mutually exclusive retrospective coverage categories for these same 200 studies.'''),
dict(i=3,title='Create an integrated scenario',unit='thousand COP',measure='delivery fee',condition='included optional parcel insurance',
 scope='all 100,000 completed deliveries by registered couriers in a Bogota platform on November 2, 2026',N=100000,n=64,a=32,s=7,k=24,b=34,t=9,j=32,sigma=8,mu=33,levels=[('95',D('1.960'))],centers=[32,33,34,35,D('32.5')],
 context=r'''\textbf{One valid example of a student-created scenario (hypothetical).}
A platform investigates all 100,000 completed deliveries by its registered couriers in Bogota on November 2, 2026. The measurement is the fee for each delivery in thousand COP. The separate yes-or-no condition is whether the delivery included optional parcel insurance.

The initial independent random sample of 64 deliveries has mean fee 32 thousand COP, sample standard deviation 7 thousand COP and 24 insured deliveries. A second independent random sample of 64 deliveries from that identical population and date has mean fee 34 thousand COP, sample standard deviation 9 thousand COP and 32 insured deliveries.

A certified spread-only report gives the known population standard deviation of delivery fees as 8 thousand COP, distinct from either sample standard deviation; the population mean is initially withheld. The initial study uses 95\% confidence. Assume the fee distribution is sufficiently regular with no dominant outliers, so the normal approximation to sample means is suitable. Each sample is selected without replacement from the full register. Study selections are independent and may overlap. Each study samples 0.064\% of the population, so the finite-population correction is negligible.

Five subsequent independent studies, separate from the two original samples, use 64 deliveries each, the same known population standard deviation and the same 95\% normal procedure. A hypothetical later comprehensive investigation of the entire same-day delivery population establishes the population mean as 33 thousand COP; this is not established by the repeated samples. The subsequent interval endpoints below are in thousand COP.''')]

def f(x):
    return format(D(str(x)).normalize(),'f')
def table(cols,body):
    return '\\keytable{'+cols+'}{\n'+body+'}\n'
def add(x): parts.append(x+'\n')
def prompt(title,mark,macro): add(r'\taskprompt{'+title+'}{'+mark+'}{'+chr(92)+macro+'}')
def heading(title,label):
    mark = ('1.5' if 'c1' in label else '1') if 'p3' not in label else ('1.25' if 'c1' in label else ('1' if label.endswith('c2b') else '0.75'))
    add(r'\worked{'+title+r' \score{'+mark+'}}{'+label+'}')
def nav(i): add(r'\secInicio[][sec:p'+str(i)+']')

for q in data:
    i=q['i']; n=q['n']; unit=q['unit']; a=q['a']; b=q['b']; sig=q['sigma']; mu=q['mu']; se=D(sig)/D(n).sqrt()
    add(r'\clearpage')
    alloc=r'C1-\sml{3}\quad C2-\sml{3}' if i<3 else r'C1-\sml{2.5}\quad C2-\sml{2.5}'
    add(r'\sectionScored{'+q['title']+'}{'+alloc+'}{sec:p'+str(i)+'}')
    if i==3:
        add(r'''\textbf{Original construction question}\score{5 overall}
Invent a new economic or financial scenario integrating both criteria. Supply the shared contextual description and all data, then complete both C1 tasks and all three C2 tasks below for your own scenario. One confidence level is sufficient. Write the contextual description in ordinary language: numerals, percentages, written units and plain-language table headings are allowed, but reserve symbols, formulas, inequalities and interval notation for task reference material and solutions.

\textbf{Required construction checklist}
\begin{enumerate}
\item Define a population's place, fixed period, eligibility and size; define one numerical measurement with units and a separate binary condition.
\item Provide an initial independent random sample and a second independent random sample from exactly the same population and period. For each give size, mean, sample standard deviation and integer condition count between zero and that sample size. Ensure summaries are feasible for the numerical measurement.
\item State a known population standard deviation, distinguish it from both sample standard deviations, and explain that the population mean is initially unknown. Choose confidence and a supplied standard normal critical value.
\item Give suitable randomness, independence and normal-approximation assumptions. For finite sampling without replacement, keep the sampling fractions negligible. Subsequent studies must be independent draws from the same full fixed population and period.
\item Specify a number of subsequent studies, each with the initial sample size, known population standard deviation and confidence procedure. Supply all subsequent endpoints or complete coverage/miss counts. Endpoints must have the stated procedure's width; with multiple levels, evidence must respect nesting.
\item Include a later comprehensive population investigation establishing the mean of that same population for retrospective coverage. A clearly hypothetical investigation is acceptable; do not claim repeated samples establish the population mean.
\end{enumerate}
\textbf{Proposed allocation.} C1 Task 1: 1.25; C1 Task 2: 1.25; C2 Task 1: 0.75; C2 Task 2: 1.00; C2 Task 3: 0.75. Total C1: 2.5; total C2: 2.5; overall: 5. Scenario completeness and validity are assessed within these marks.

\textbf{Tasks to complete for your scenario.} Follow the five linked tasks below. Other internally consistent scenarios and correct solutions are equally acceptable; the example after the task list is one possible response.
''')
    else:
        add(r'\textbf{Original shared description}\score{6 overall}')
        add(q['context'])
        if i==1:
            rows=r'\textbf{Subsequent study}&\textbf{Lower endpoint}&\textbf{Upper endpoint}\\\midrule'+'\n'
            moe=q['levels'][0][1]*se
            for j,c in enumerate(q['centers'],1): rows+=f'{j}&{f(D(str(c))-moe)}&{f(D(str(c))+moe)}'+r'\\'+'\n'
            add(table('KKK',rows))
        else:
            add(table('Kr',r'''\textbf{Intervals covering the later established mean}&\textbf{Studies}\\\midrule
Both confidence levels&176\\
Only the 99\% level&20\\
Neither confidence level&4\\'''))
    add(r'\textbf{Linked tasks.} Each full task is reproduced immediately before its solution.')
    add(r'\QuestionsTasks[sec:p'+str(i)+']{'+ '\n'+',\n'.join([
        '{1}/{sol:p'+str(i)+'c1a}/{C1 Task 1: identify and interpret population and sample measures. \\score{'+('1.5' if i<3 else '1.25')+'}}',
        '{1}/{sol:p'+str(i)+'c1b}/{C1 Task 2: compare the two samples and fixed parameters. \\score{'+('1.5' if i<3 else '1.25')+'}}',
        '{2}/{sol:p'+str(i)+'c2a}/{C2 Task 1: organize information and calculate standard error. \\score{'+('1' if i<3 else '0.75')+'}}',
        '{2}/{sol:p'+str(i)+'c2b}/{C2 Task 2: calculate and interpret point and interval estimates. \\score{1}}',
        '{2}/{sol:p'+str(i)+'c2c}/{C2 Task 3: calculate and interpret subsequent coverage. \\score{'+('1' if i<3 else '0.75')+'}}'])+'\n}')
    if i==3:
        add(r'\clearpage')
        add(q['context'])
        moe=q['levels'][0][1]*se
        rows=r'\textbf{Subsequent study}&\textbf{Lower endpoint}&\textbf{Upper endpoint}\\\midrule'+'\n'
        for j,c in enumerate(q['centers'],1): rows+=f'{j}&{f(D(str(c))-moe)}&{f(D(str(c))+moe)}'+r'\\'+'\n'
        add(table('KKK',rows))
        add(r'''\textbf{Validity of the construction.} Counts are integers within sample sizes. The numerical fee is nonnegative; the reported means and spreads are feasible. For example, a 64-value sample with 32 values at $m-d$ and 32 at $m+d$, where $d=s\sqrt{63/64}$, has exactly mean $m$ and sample SD $s$. For the first sample $d\approx6.9451<32$; for the second $d\approx8.9294<34$, so all fees can be positive. Insurance labels can be assigned to 24 and 32 of those observations independently of fee size. The large remainder of the population can accommodate both samples and the stated mean and spread. This construction illustrates feasibility; students need not submit raw observations.''')
        nav(i)
    add(r'\clearpage')
    prompt('C1 Task 1','1.5' if i<3 else '1.25','cOneA')
    heading('C1 Task 1',f'sol:p{i}c1a')
    add(f'The population $\\mathcal P$ is {q["scope"]}; $N={q["N"]:,}$. Initial sample $X_A$ and comparison sample $X_B$ each contain {n} randomly selected eligible units from that same place and period. They are separate independent selections, not populations at two different dates. The subsequent studies are additional samples of {n} from the same frame.')
    pa=D(q['k'])/n; pb=D(q['j'])/n
    add(table('KKK',r'\textbf{Measure}&\textbf{Population parameter and meaning}&\textbf{Sample statistics and meaning}\\\midrule'+'\n'+
        f'Mean&$\\mu$: mean {q["measure"]} across all eligible units; initially unknown, later {mu} {unit}.&$\\bar x_A={a}$; $\\bar x_B={b}$ {unit}: averages within the respective samples.'+r'\\'+'\n'+
        f'Standard deviation&$\\sigma={sig}$ {unit}: known spread of individual {q["measure"]} values across the population.&$s_A={q["s"]}$; $s_B={q["t"]}$ {unit}: sample spreads, calculated about their own sample means.'+r'\\'+'\n'+
        f'Proportion&$p$: fraction of all eligible units that {q["condition"]}; not supplied.&$\\hat p_A={q["k"]}/{n}={f(pa)}={f(pa*100)}\\%$; $\\hat p_B={q["j"]}/{n}={f(pb)}={f(pb*100)}\\%$.'+r'\\'))
    add(f'The condition counts are $k_A={q["k"]}$ and $k_B={q["j"]}$. The proportions are unitless shares of each sample meeting the stated condition. The known population SD does not make either sample SD equal to it. Initially $\\mu$ is unknown; the later investigation establishes that same parameter as {mu} {unit}. The supplied information never establishes $p$: sample proportions are estimates, and the investigation reports only the population mean.')
    nav(i)
    prompt('C1 Task 2','1.5' if i<3 else '1.25','cOneB')
    heading('C1 Task 2',f'sol:p{i}c1b')
    delta=(pb-pa)*100
    add(table('KKK',r'\textbf{Second minus initial}&\textbf{Calculation}&\textbf{Interpretation}\\\midrule'+'\n'+
        f'Mean&${b}-{a}={b-a:+}$ {unit}&Second sample mean is '+('higher' if b>a else 'lower')+'.'+r'\\'+'\n'+
        f'Sample SD&${q["t"]}-{q["s"]}={q["t"]-q["s"]:+}$ {unit}&Second sample has greater numerical spread.'+r'\\'+'\n'+
        f'Proportion&${f(pb*100)}\\%-{f(pa*100)}\\%={f(delta)}$ percentage points&Second sample has a larger condition share.'+r'\\'))
    add(f'Both sample sizes remain {n}; the selected units and descriptive statistics differ. Population membership, size, place, period, measurement and binary-condition definitions remain fixed. Therefore $\\mu$, $\\sigma$ and $p$ remain fixed, whether known or unknown. Random sampling variation can produce these differences; they do not establish a temporal change in population parameters. Learning the value of $\\mu$ later changes our knowledge, not the population mean itself.')
    nav(i)
    add(r'\clearpage')
    prompt('C2 Task 1','1' if i<3 else '0.75','cTwoA')
    heading('C2 Task 1',f'sol:p{i}c2a')
    add(table('p{.11\linewidth}p{.19\linewidth}p{.19\linewidth}K',r'\textbf{Symbol}&\textbf{Concept}&\textbf{Type}&\textbf{Meaning in context}\\\midrule'+'\n'+
        f'$\\mu$&Population mean&Population parameters&Initially unknown mean {q["measure"]} for the defined population.'+r'\\'+ '\n'+
        f'$\\mu_{{\\mathrm{{known}}}}$&Later established mean&Population parameters&{mu} {unit}; same $\\mu$, established by the comprehensive investigation.'+r'\\'+'\n'+
        f'$\\sigma$&Population SD&Population parameters&{sig} {unit}; known population spread.'+r'\\\midrule'+'\n'+
        f'$\\bar x$&Initial sample mean&Sample statistics&{a} {unit}; point estimate of $\\mu$.'+r'\\'+'\n'+
        f'$n$&Initial sample size&Sample statistics&{n} selected eligible units.'+r'\\'+'\n'+
        f'$\\mathrm{{SE}}$&Standard error&Sample statistics&$\\sigma/\\sqrt n={sig}/\\sqrt{{{n}}}={f(se)}$ {unit}; spread of sample means across repeated samples.'+r'\\\midrule'+'\n'+
        '$C$&Confidence&Procedure settings&'+ '; '.join(f'{l}\\%: $C={f(D(l)/100)}$' for l,z in q['levels'])+r'.\\'+'\n'+
        '$\\alpha$&Significance&Procedure settings&'+ '; '.join(f'{l}\\%: $1-{f(D(l)/100)}={f(1-D(l)/100)}$' for l,z in q['levels'])+r'.\\'+'\n'+
        '$\\alpha/2$&Each tail area&Procedure settings&'+ '; '.join(f'{l}\\%: ${f(1-D(l)/100)}/2={f((1-D(l)/100)/2)}$' for l,z in q['levels'])+r'.\\'+'\n'+
        '$z^*$&Positive critical value&Procedure settings&'+ '; '.join(f'{l}\\%: ${z}$' for l,z in q['levels'])+r'.\\'))
    add(f'Use the initial sample only for estimation. The comparison sample describes sample variation; the later mean is reserved for retrospective assessment. Known $\\sigma={sig}$ is used, rather than either $s_A={q["s"]}$ or $s_B={q["t"]}$. The normal approximation is supported by random sampling, the stated regularity assumption and negligible sample fraction.')
    nav(i)
    if i==2: add(r'\clearpage')
    prompt('C2 Task 2','1','cTwoB')
    heading('C2 Task 2',f'sol:p{i}c2b')
    add(f'The shared point estimate is $\\bar x={a}$ {unit}, the average {q["measure"]} in the initial sample; it estimates the population mean with a single value.')
    for level,z in q['levels']:
        moe=z*se; lo=D(a)-moe; hi=D(a)+moe; width=2*moe
        add(r'\textbf{'+level+r'\% confidence}')
        add(table('p{.09\linewidth}p{.16\linewidth}p{.32\linewidth}K',r'\textbf{Symbol}&\textbf{Concept}&\textbf{Calculation}&\textbf{Result and meaning in context}\\\midrule'+'\n'+
            f'$\\bar x$&Point estimate&$\\bar x={a}$&{a} {unit}; estimated mean.'+r'\\'+'\n'+
            f'$\\mathrm{{MoE}}$&Margin of error&$z^*\\sigma/\\sqrt n={z}({sig}/\\sqrt{{{n}}})$&{f(moe)} {unit}; half-width.'+r'\\'+'\n'+
            f'$L$&Lower endpoint&$\\bar x-\\mathrm{{MoE}}={a}-{f(moe)}$&{f(lo)} {unit}; lower plausible mean.'+r'\\'+'\n'+
            f'$U$&Upper endpoint&$\\bar x+\\mathrm{{MoE}}={a}+{f(moe)}$&{f(hi)} {unit}; upper plausible mean.'+r'\\'+'\n'+
            f'$\\mathrm{{CI}}$&Confidence interval&$[L,U]=[{f(lo)},{f(hi)}]$&Range of plausible population means, in {unit}.'+r'\\'+'\n'+
            f'$W$&Full width&$U-L={f(hi)}-{f(lo)}$\n $=2({f(moe)})={f(width)}$&{f(width)} {unit}; interval precision.'+r'\\'))
        add(f'We are {level}\\% confident that the mean {q["measure"]} for {q["scope"]} lies between {f(lo)} and {f(hi)} {unit}, in the repeated-sampling sense described in Task 3. This estimates a population mean, not a range containing {level}\\% of individual values.')
    if i==2: add(r'The 99\% interval contains the 90\% interval: the same center and SE are used, and the larger critical value produces a wider interval and less precision at the higher confidence level.')
    nav(i)
    add(r'\clearpage')
    prompt('C2 Task 3','1' if i<3 else '0.75','cTwoC')
    heading('C2 Task 3',f'sol:p{i}c2c')
    if i!=2:
        moe=q['levels'][0][1]*se
        rows=r'\textbf{Study}&\textbf{Lower endpoint}&\textbf{Upper endpoint}&\textbf{Covers later mean?}\\\midrule'+'\n'
        count=0
        for j,c in enumerate(q['centers'],1):
            lo=D(str(c))-moe; hi=D(str(c))+moe; cover=lo<=mu<=hi; count+=cover
            rows+=f'{j}&{f(lo)}&{f(hi)}&'+('Yes' if cover else 'No')+r'\\'+'\n'
        add(f'Test each subsequent interval against $\\mu_{{\\mathrm{{known}}}}={mu}$ {unit}; include the mean when it equals an endpoint. All endpoints below use {unit}.')
        add(table('KKKK',rows))
        total=len(q['centers']); cov=D(count)/total*100; err=abs(cov-95)
        add(f'At 95\\%: $N_{{\\mathrm{{cover}}}}={count}$ and $N(95\\%)={total}$ subsequent intervals. Thus\n'+r'\['+f'\\mathrm{{Cov}}(95\\%)=\\frac{{{count}}}{{{total}}}\\,100\\%={f(cov)}\\%,\\qquad E_{{\\mathrm{{abs}}}}=|{f(cov)}-95|={f(err)}\\text{{ percentage points}}.'+r'\]')
        add(f'The observed coverage of the later-established mean {q["measure"]} is {f(err)} percentage points below nominal 95\\%. Each listed interval has full width $2({f(moe)})={f(2*moe)}$ {unit}, consistent with the stated $n$, known $\\sigma$ and critical value. Its center is its own subsequent sample mean, found as $(L_i+U_i)/2$, not the initial mean.')
    else:
        add(table('KKK',r'''\textbf{Confidence}&\textbf{Covering and missing counts}&\textbf{Coverage and absolute difference}\\\midrule
90\%&Cover: $176$; miss: $20+4=24$&$176/200\times100\%=88\%$; $|88-90|=2$ percentage points.\\
99\%&Cover: $176+20=196$; miss: $4$&$196/200\times100\%=98\%$; $|98-99|=1$ percentage point.\\'''))
        add(r'The 90\% procedure covers the fixed mean of 84 thousand COP in 176 of 200 subsequent studies, 2 percentage points below nominal confidence. The 99\% procedure covers it in 196 of those same studies, 1 percentage point below nominal confidence. The categories sum to $176+20+4=200$. Every 90\% covering interval also covers at 99\%; all four misses at 99\% are among the 24 misses at 90\%. There is no impossible category in which only the narrower interval covers. These are feasible counts: sample-mean distances from 84 of 0, 6 and 9 thousand COP respectively would realize the three categories, since the margins are 4.935 and 7.728.')
    add(r'''\textbf{Interpretation.} Under the stated model, repeated independent use of each confidence procedure covers the fixed population mean in approximately its nominal percentage of intervals over the long run. A finite collection of intervals need not have exactly nominal coverage, and successive observed proportions need not approach it monotonically. The discrepancies here can arise from finite-study variation; they do not by themselves invalidate the procedure or prove that nominal coverage is wrong.

The population mean is fixed. Once an interval is calculated, it either contains that mean or does not; no nominal probability is assigned to this already determined event. Coverage counts compare each subsequent study's own interval with the later-established population mean. They do not count sample means or individual observations inside the initial interval. The initial and comparison samples are excluded from the subsequent-study denominator.''')
    nav(i)
    add(r'\clearpage')
    if i<3:
        add(r'''\subsection*{Proposed partial-credit guidance}
\keytable{Kp{.12\linewidth}K}{
\textbf{Task}&\textbf{Points}&\textbf{Evidence earning credit}\\\midrule
C1 Task 1&1.5&0.5 population and both sample scopes/sizes; 0.5 mean/SD pairings, units and known status; 0.5 counts, both proportions and meanings, unknown population proportion.\\
C1 Task 2&1.5&0.75 for three signed differences (0.25 each, including percentage points); 0.75 fixed parameters and scope with sampling-variation explanation.\\
C2 Task 1&1&0.25 parameter group and initially unknown/later mean; 0.25 initial sample entries and correct SE with units; 0.5 complete procedure settings at all requested levels.\\
C2 Task 2&1&0.2 point estimate; 0.2 correct margins using known SD; 0.3 endpoints and intervals; 0.15 full widths; 0.15 units and contextual mean interpretation. Divide each multi-level component equally across the two levels in Problem 2.\\
C2 Task 3&1&0.25 correct covering counts; 0.25 coverage percentages; 0.25 absolute differences in percentage points; 0.25 valid coverage/finite-study interpretation. Divide numerical components equally across levels in Problem 2.\\}
\textbf{Task totals:} C1: $1.5+1.5=3$; C2: $1+1+1=3$; problem total: 6. Award proportional credit within each listed component for incomplete but valid reasoning. Accept equivalent notation and reasonable rounding. Carry forward an earlier numerical error when the later method is correct; do not penalize the same arithmetic error repeatedly. Do not award the interpretation component for a probability statement about the fixed mean in an already calculated interval.
''')
    else:
        add(r'''\subsection*{Proposed analytic rubric: exactly 5 points}
This is an explicitly \textbf{proposed} split because the brief assigns only the overall 5 points. Assess the student's own coherent scenario; the model answer is not a required topic or dataset.
\keytable{Kp{.11\linewidth}K}{
\textbf{Task}&\textbf{Points}&\textbf{Analytic evidence, including construction validity}\\\midrule
C1 Task 1&1.25&0.25 complete fixed population scope and sizes; 0.25 two clearly defined independent samples with feasible summaries and valid binary counts; 0.25 mean/SD pairings, units and distinct population/sample spreads; 0.5 both proportion calculations and interpretations, plus correct known/unknown status.\\
C1 Task 2&1.25&0.75 three correct signed differences (0.25 each; percentage points for proportions); 0.5 fixed population characteristics and sound explanation of sample variation.\\
C2 Task 1&0.75&0.25 adequate assumptions, negligible fractions, same-population study design and known spread; 0.25 completed parameter/sample groups, initially unknown mean and explicitly later comprehensive investigation; 0.25 SE and complete confidence/significance/tails/critical-value settings.\\
C2 Task 2&1.00&0.2 point estimate; 0.2 correct margin from known SD; 0.3 endpoints and interval with substitutions; 0.15 full width; 0.15 units and contextual mean interpretation.\\
C2 Task 3&0.75&0.25 complete, valid subsequent evidence consistent with the procedure and later mean; 0.25 counts, coverage and absolute percentage-point difference; 0.25 long-run/finite-study explanation with no fixed-mean probability error.\\}
\textbf{Rubric reconciliation:} C1: $1.25+1.25=2.5$; C2: $0.75+1+0.75=2.5$; overall: $2.5+2.5=5$. No separate construction bonus is available. Missing or invalid scenario elements lose credit within the components that assess them. Correct conditional methods may earn credit even when one supplied datum is flawed; do not repeatedly penalize the same arithmetic mistake. Award proportional credit within components for partially correct work. Other internally consistent scenarios and correct solutions are acceptable.

\textbf{Whole-exam scoring check.} C1: $3+3+2.5=8.5$ available; C2: $3+3+2.5=8.5$ available; overall: $6+6+5=17$. Pass C1 exactly when its earned score is at least 4; pass C2 exactly when its earned score is at least 4. Both must pass separately. For example, C1 = 3.5 and C2 = 8.5 fails C1 even with 12 overall; C1 = 4 and C2 = 4 passes both with 8 overall. Scores never transfer.
''')
    nav(i)
add(r'\end{document}')
(OUT/(name+'.tex')).write_text('\n'.join(parts),encoding='utf-8')
print(OUT/(name+'.tex'))
