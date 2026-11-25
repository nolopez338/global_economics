from pathlib import Path
root=Path.cwd()
template=(root/'.agents/skills/global-economics-classroom-activity/assets/template_classroom_activity.tex').read_text(encoding='utf-8')
prefix=template.split('{\\centering\n    {\\Large\\bfseries [Criterion')[0]
prefix=prefix.replace('{../../../preamble/}{../../../../book2026-2027/preamble/}', '{../../../preamble/}')
body=r'''
{\centering {\Large\bfseries Confidence intervals and economic report audits\par}
Global Economics \textbar{} Grade 11 \textbar{} Term 2 \textbar{} Lesson 1\par}
\criterionbox{C4}{Constructs confidence intervals for a population mean with known variance using the normal distribution, applying them to contexts such as average income, average investment return, or average price level.}

\stageheading{Equations and basic procedure}
Use independent random observations from a normal population, or a sufficiently large sample for the normal approximation, with known population variance. All data here are hypothetical. Each inverse report is independent of every other report and of the forward comparison. Its endpoints are exact relative to its stated construction cutoff.
\NotationReferenceTable{
$\mu,\bar x$ & Population and sample means & $\mu$ is fixed but unknown; $\bar x$ is the observed interval center.\\
$\sigma,\sigma^2,s$ & Population SD, variance; sample SD & Known $\sigma>0$ is required; $\sigma^2$ has squared response units. A sample SD $s$ is not a substitute here.\\
$n,\mathrm{SE}$ & Sample size; standard error & $n$ is a positive integer; $\mathrm{SE}=\sigma/\sqrt n$ is the sampling SD of the mean.\\
$C,\alpha$ & Confidence and significance & $\alpha=1-C$; each tail has area $\alpha/2$.\\
$\Phi,z^*$ & Standard normal CDF; positive cutoff & $\Phi(z)=P(Z\le z)$, $Z\sim N(0,1)$; $z^*=\Phi^{-1}((1+C)/2)$.\\
$E,[L,U],W$ & Margin, endpoints and full width & $E=z^*\sigma/\sqrt n$; $[L,U]=[\bar x-E,\bar x+E]$; $W=2E$.\\
$\bar x,E$ & Recovery from endpoints & $\bar x=(L+U)/2$; $E=(U-L)/2$.\\
$n,\sigma$ & Inverse rules & $n=(z^*\sigma/E)^2$; $\sigma=E\sqrt n/z^*$.\\
}
Use $z^*=1.645$ for 90\%, $1.96$ for 95\%, and $2.576$ for 99\%. Use the stated cutoff in inverse calculations. Means, SD, SE, margins, bounds and widths share response units; $n,C,\alpha,z^*$ are unitless.
\begin{enumerate}[label=\arabic*.,itemsep=2pt]
\item Define the population mean and units; organize each report's knowns and unknowns and convert confidence information into $C,\alpha,\alpha/2,z^*$.
\item For forward comparisons, calculate the full two-size, two-confidence grid. For inverse reports, find the midpoint and half-width, then rearrange $E\sqrt n=z^*\sigma$ for the missing quantity.
\item Interpret the interval and the economic decision. At fixed other inputs, width increases with $C$ and $\sigma$, and decreases with $\sqrt n$.
\end{enumerate}
Confidence describes long-run coverage of the fixed population mean, not the fraction of individual values inside an interval or a probability assigned to the fixed mean after sampling. Rounded endpoints can make inverse recovery nonunique; rounding $n$ upward does not recover a historical count.

\stageheading{General tasks}
\task{Task 1 --- Construct intervals and select a research budget.}{}
\begin{enumerate}[label=\arabic*.,itemsep=2pt]
\item Population mean and units; known quantities; $C,\alpha,\alpha/2,z^*$ at both levels.
\item A ruled comparison table for all four $(n,C)$ combinations, with SE, $E$, $[L,U]$ and $W$.
\item The smallest offered sample meeting the width limit at both levels; interval interpretations and effects of confidence and sample size on width.
\end{enumerate}
\task{Task 2 --- Recover sample means and sample sizes.}{}
\begin{enumerate}[label=\arabic*.,itemsep=2pt]
\item Each report's population mean, units, confidence settings, midpoint and half-width.
\item The recovered $\bar x$ and $n$ for each report.
\item Report eligibility under the stated count and observed-mean thresholds; interval interpretations.
\end{enumerate}
\task{Task 3 --- Recover sample means and population variability.}{}
\begin{enumerate}[label=\arabic*.,itemsep=2pt]
\item Each report's population mean, units, confidence settings, midpoint and half-width.
\item The recovered $\bar x$ and known population SD $\sigma$ for each report.
\item The group with both a higher observed mean and greater population SD, if any; interval interpretations and the meanings of $\sigma$ and SE.
\end{enumerate}
\clearpage

\stageheading{Worked example}
\problemtitle{1}{Courier reference-week earnings}{Complete}
A cooperative studies mean reference-week earnings in thousand COP per courier. Independent random samples are large enough for the normal approximation. For its research-budget comparison, keep $\bar x=450$ and known $\sigma=60$ at both offered sizes $n=36,144$. Use $C=95\%$ and $\alpha=0.01$, with cutoffs 1.96 and 2.576. The full-width limit is 30 thousand COP at both levels.
\task{Task 1 --- Construct intervals and select a research budget.}{}
\subtaskheading{1}{Model and settings}
$\mu$ is the population mean reference-week earnings. Here $\bar x=450$, $\sigma=60$ and $\sigma^2=3600$ in squared thousand COP. A courier is one sampled unit.
\InformationTable{
$C$ & 95\% confidence & $C=0.95$, $\alpha=0.05$, $\alpha/2=0.025$, $z^*=1.96$.\\ \hline
$\alpha$ & 1\% significance & $C=1-0.01=0.99$, $\alpha/2=0.005$, $z^*=2.576$.\\ \hline
}
\subtaskheading{2}{Four constructions}
The standard errors are $60/\sqrt{36}=10$ and $60/\sqrt{144}=5$ thousand COP. Multiply each by the relevant cutoff and subtract/add the resulting margin from/to 450.
\ClassroomRuledTable{.14\linewidth}{.25\linewidth}{\textbf{$n$ and $C$} & \textbf{SE and margin $E$} & \textbf{Endpoint calculations and full width}}{
$36,95\%$ & $\mathrm{SE}=10$; $E=1.96(10)=19.6$ & $[450-19.6,450+19.6]=[430.4,469.6]$; $W=39.2$.\\ \hline
$36,99\%$ & $\mathrm{SE}=10$; $E=2.576(10)=25.76$ & $[450-25.76,450+25.76]=[424.24,475.76]$; $W=51.52$.\\ \hline
$144,95\%$ & $\mathrm{SE}=5$; $E=1.96(5)=9.8$ & $[450-9.8,450+9.8]=[440.2,459.8]$; $W=19.6$.\\ \hline
$144,99\%$ & $\mathrm{SE}=5$; $E=2.576(5)=12.88$ & $[450-12.88,450+12.88]=[437.12,462.88]$; $W=25.76$.\\ \hline
}
\subtaskheading{3}{Decision and interpretation}
Choose 144 couriers: $19.6\le30$ and $25.76\le30$, whereas both widths for 36 couriers exceed 30. Quadrupling $n$ halves SE and width. Raising confidence from 95\% to 99\% increases width by $2.576/1.96\approx1.3143$ at either size.
At 95\% confidence, the respective intervals estimate the population mean as 430.4--469.6 and 440.2--459.8 thousand COP; at 99\%, they estimate it as 424.24--475.76 and 437.12--462.88 thousand COP. In repeated sampling each procedure covers $\mu$ at its stated rate. These are not ranges for individual earnings.
\textbf{Checks.} Every midpoint is 450; for example, $459.8-440.2=19.6=2(9.8)$. All margins are positive and the four intervals are symmetric.

\task{Task 2 --- Recover sample means and sample sizes.}{}
Two separate reports qualify for a briefing only if $n\ge100$ and $\bar x\ge465$ thousand COP. Report A gives $[444.32,475.68]$, $C=95\%$, $\sigma=80$ and $z^*=1.96$. Report B gives $[459.696,480.304]$, $\alpha=0.01$, $\sigma=60$ and $z^*=2.576$. Both used the known-$\sigma$ normal procedure; neither shares unknowns with Task 1 or the other report.
\subtaskheading{1}{Centers and margins}
Both reports estimate their own population mean reference-week earnings. A uses $(C,\alpha,\alpha/2)=(0.95,0.05,0.025)$; B uses $(0.99,0.01,0.005)$.
\ClassroomRuledTable{.10\linewidth}{.40\linewidth}{\textbf{Report} & \textbf{Midpoint $\bar x=(L+U)/2$} & \textbf{Half-width $E=(U-L)/2$}}{
A & $(444.32+475.68)/2=460$ & $(475.68-444.32)/2=15.68$.\\ \hline
B & $(459.696+480.304)/2=470$ & $(480.304-459.696)/2=10.304$.\\ \hline
}
\subtaskheading{2}{Recover the counts}
From $E\sqrt n=z^*\sigma$, divide by $E$ and square: $n=(z^*\sigma/E)^2$.
\[
n_A=\left(\frac{1.96(80)}{15.68}\right)^2=10^2=100,
\qquad n_B=\left(\frac{2.576(60)}{10.304}\right)^2=15^2=225.
\]
The units cancel, giving exact integer counts rather than planned minimum sizes.
\subtaskheading{3}{Eligibility and interpretation}
Only B qualifies: $225\ge100$ and $470\ge465$; A fails the observed-mean threshold. We are 95\% confident that A's population mean is between 444.32 and 475.68 thousand COP, and 99\% confident that B's is between 459.696 and 480.304 thousand COP. Eligibility concerns observed evidence, without proving a population mean above 465.
\textbf{Checks.} A has $\mathrm{SE}=80/10=8$, so $460\pm1.96(8)=[444.32,475.68]$. B has $\mathrm{SE}=60/15=4$, so $470\pm2.576(4)=[459.696,480.304]$.

\task{Task 3 --- Recover sample means and population variability.}{}
Two further independent reports used population SDs known from records but omitted them. Report C gives $[460.13,479.87]$, $C=90\%$, $n=100$, $z^*=1.645$. Report D gives $[463.32,486.68]$, $\alpha=0.05$, $n=144$, $z^*=1.96$. The coordinator prioritizes the group with both the higher observed mean and the greater population SD.
\subtaskheading{1}{Centers and margins}
Each $\mu$ refers to its own group's mean reference-week earnings. C uses $(C,\alpha,\alpha/2)=(0.90,0.10,0.05)$; D uses $(0.95,0.05,0.025)$.
\ClassroomRuledTable{.10\linewidth}{.40\linewidth}{\textbf{Report} & \textbf{Midpoint} & \textbf{Half-width}}{
C & $(460.13+479.87)/2=470$ & $(479.87-460.13)/2=9.87$.\\ \hline
D & $(463.32+486.68)/2=475$ & $(486.68-463.32)/2=11.68$.\\ \hline
}
\subtaskheading{2}{Recover population SDs}
Divide $E\sqrt n=z^*\sigma$ by $z^*$ to obtain $\sigma=E\sqrt n/z^*$:
\[
\sigma_C=\frac{9.87\sqrt{100}}{1.645}=\frac{98.7}{1.645}=60,
\qquad \sigma_D=\frac{11.68\sqrt{144}}{1.96}=\frac{140.16}{1.96}\approx71.5102.
\]
Both SDs are in thousand COP and describe individual population earnings; they are not sample SDs. The corresponding SEs are 6 and $11.68/1.96\approx5.9592$ thousand COP.
\subtaskheading{3}{Priority and interpretation}
Prioritize D: $475>470$ and $71.5102>60$. Its larger individual spread coexists with a slightly smaller SE because it has more observations. We are 90\% confident that C's population mean is between 460.13 and 479.87 thousand COP, and 95\% confident that D's is between 463.32 and 486.68 thousand COP. This does not establish an ordering of the population means or of every courier's earnings.
\textbf{Checks.} C gives $470\pm1.645(60/10)=470\pm9.87$. Using the exact recovered expression for D gives $475\pm1.96[(11.68\cdot12/1.96)/12]=475\pm11.68$. Both reproduce the supplied limits; rounding is only for reporting.
\clearpage
'''
# Guided helpers copied from the scaffold, kept within the guided group.
guided_helpers=template[template.index('\\begingroup % Guided Example ONLY'):template.index('\\stageheading{Guided Example}')]
body+=guided_helpers+r'''
\stageheading{Guided Example}
\problemtitle{2}{Quarterly warehouse handling charges}{Scaffolded}
An importer studies population mean quarterly handling charges in USD per pallet. Assume independent random observations and a valid normal approximation. In the budget comparison, $\bar x=84$ and known $\sigma=18$ for both $n=36$ and $n=144$. The levels are $C=90\%$ and $\alpha=0.05$, with $z^*=1.645$ and 1.96. The full-width limit is USD 7 per pallet at both levels.
\task{Task 1 --- Construct intervals and select a research budget.}{}
\subtaskheading{1}{Model and settings}
Define $\mu$ and give its units.\par\nopagebreak[4]
\guidedresponsebox[18mm]{\dimexpr\linewidth-1pt\relax}
\par For the second level, $C=1-0.05=$ \guidedresponsebox{18mm}.
\par Complete $(\alpha,\alpha/2)$ for 90\%: \guidedresponsebox[12mm]{48mm}; for the second level: \guidedresponsebox[12mm]{48mm}.
\subtaskheading{2}{Four constructions}
Start with $\mathrm{SE}_{36}=18/\sqrt{36}=18/6$. Complete the calculations in USD per pallet.
\ClassroomRuledTable{.14\linewidth}{.30\linewidth}{\textbf{$n$ and $C$} & \textbf{SE and margin $E$} & \textbf{Both endpoint calculations and full width}}{
$36,90\%$ & \guidedresponsebox[19mm]{\dimexpr\linewidth-1pt\relax} & \guidedresponsebox[19mm]{\dimexpr\linewidth-1pt\relax}\\ \hline
$36,95\%$ & \guidedresponsebox[19mm]{\dimexpr\linewidth-1pt\relax} & \guidedresponsebox[19mm]{\dimexpr\linewidth-1pt\relax}\\ \hline
$144,90\%$ & \guidedresponsebox[19mm]{\dimexpr\linewidth-1pt\relax} & \guidedresponsebox[19mm]{\dimexpr\linewidth-1pt\relax}\\ \hline
$144,95\%$ & \guidedresponsebox[19mm]{\dimexpr\linewidth-1pt\relax} & \guidedresponsebox[19mm]{\dimexpr\linewidth-1pt\relax}\\ \hline
}
\Needspace{14\baselineskip}
\subtaskheading{3}{Decision and interpretation}
Select the smallest offered sample meeting the width limit at both levels, state the interval meanings and describe the effects of $n$ and confidence on width.\par\nopagebreak[4]
\guidedresponsebox[38mm]{\dimexpr\linewidth-1pt\relax}
\clearpage
\task{Task 2 --- Recover sample means and sample sizes.}{}
Two independent quarterly reports used known population SDs. Report A gives $[80.08,87.92]$, $C=95\%$, $\sigma=20$, $z^*=1.96$. Report B gives $[84.848,95.152]$, $\alpha=0.01$, $\sigma=24$, $z^*=2.576$. A report qualifies for a supplier review when $n\ge100$ and $\bar x\ge88$ USD per pallet.
\subtaskheading{1}{Centers and margins}
Each $\mu$ is that report's population mean quarterly charge in USD per pallet. Complete the confidence settings and midpoint/half-width calculations separately.
\guidedpair{
\textbf{Report A}\par
$(C,\alpha,\alpha/2)=$\par
\guidedresponsebox[12mm]{\dimexpr\linewidth-1pt\relax}\par
$\bar x=(80.08+87.92)/2$; $E=(87.92-80.08)/2$.\par
\guidedresponsebox[22mm]{\dimexpr\linewidth-1pt\relax}
}{
\textbf{Report B}\par
$(C,\alpha,\alpha/2)=$\par
\guidedresponsebox[12mm]{\dimexpr\linewidth-1pt\relax}\par
Write the midpoint and half-width calculations.\par
\guidedresponsebox[22mm]{\dimexpr\linewidth-1pt\relax}
}
\subtaskheading{2}{Recover the counts}
Rearrange $E\sqrt n=z^*\sigma$ and substitute each report's values.
\guidedpair{\textbf{Report A: $n$ (pallets)}\par\guidedresponsebox[30mm]{\dimexpr\linewidth-1pt\relax}}
{\textbf{Report B: $n$ (pallets)}\par\guidedresponsebox[30mm]{\dimexpr\linewidth-1pt\relax}}
\subtaskheading{3}{Eligibility and interpretation}
State which report qualifies and interpret both confidence intervals in context.\par\nopagebreak[4]
\guidedresponsebox[40mm]{\dimexpr\linewidth-1pt\relax}
\clearpage
\task{Task 3 --- Recover sample means and population variability.}{}
Two further independent quarterly reports used population SDs known from records but omitted them. Report C gives $[82.065,91.935]$, $C=90\%$, $n=64$, $z^*=1.645$. Report D gives $[88.12,99.88]$, $\alpha=0.05$, $n=100$, $z^*=1.96$. The manager prioritizes a group only if it has both the higher observed mean and greater population SD.
\subtaskheading{1}{Centers and margins}
Each $\mu$ is its own group's population mean quarterly charge in USD per pallet. Complete the settings and midpoint/half-width calculations.
\guidedpair{\textbf{Report C}\par
$(C,\alpha,\alpha/2)=$\par\guidedresponsebox[12mm]{\dimexpr\linewidth-1pt\relax}\par
$\bar x=(82.065+91.935)/2$; $E=(91.935-82.065)/2$.\par
\guidedresponsebox[22mm]{\dimexpr\linewidth-1pt\relax}
}{\textbf{Report D}\par
$(C,\alpha,\alpha/2)=$\par\guidedresponsebox[12mm]{\dimexpr\linewidth-1pt\relax}\par
Write the midpoint and half-width calculations.\par
\guidedresponsebox[22mm]{\dimexpr\linewidth-1pt\relax}}
\subtaskheading{2}{Recover population SDs}
Rearrange $E\sqrt n=z^*\sigma$; calculate each $\sigma$ and its corresponding SE, in USD per pallet.
\guidedpair{\textbf{Report C}\par\guidedresponsebox[32mm]{\dimexpr\linewidth-1pt\relax}}
{\textbf{Report D}\par\guidedresponsebox[32mm]{\dimexpr\linewidth-1pt\relax}}
\subtaskheading{3}{Priority and interpretation}
State the priority group, the meanings of its SD and SE, and both interval interpretations.\par\nopagebreak[4]
\guidedresponsebox[42mm]{\dimexpr\linewidth-1pt\relax}
\par\clearpage
\endgroup

\stageheading{Independent Practice}
'''
# Each exercise contains all three source families, with four independent inverse reports.
# Data definitions: title, unit, mean, SD, sizes, levels, width limit, count/mean thresholds,
# inverse tuples (mean, SD, n, confidence). All inverse bounds are generated exactly with Decimal.
from decimal import Decimal as D
from math import sqrt
problems=[
('Delivery reference-week earnings','thousand COP per courier',480,72,(36,144),(.95,.99),32,(100,490),[(480,60,100,.95),(500,72,144,.99),(495,64,64,.90),(505,90,225,.95)]),
('Quarterly storage charges','USD per pallet',66,15,(25,100),(.90,.95),6,(64,70),[(66,15,25,.90),(72,20,100,.95),(68,16,64,.95),(75,24,144,.99)]),
('Monthly freight processing charges','USD per shipment',150,30,(100,400),(.95,.99),8,(144,155),[(150,30,100,.99),(158,36,144,.95),(152,24,64,.90),(160,40,256,.99)]),
('Weekly market-basket prices','USD per basket',102.5,22.5,(81,225),(.90,.99),8,(144,104),[(103.5,27,81,.99),(105.25,30,225,.90),(106,32,256,.95),(108.5,30,144,.99)]),
('Quarterly export handling charges','USD per container',210,35,(49,196),(.95,.99),12,(100,215),[(212,28,49,.95),(216.5,42,196,.99),(218,48,144,.90),(222,45,225,.95)])]
z={.90:D('1.645'),.95:D('1.96'),.99:D('2.576')}
def fmt(x): return format(D(str(x)).normalize(),'f')
for num,p in enumerate(problems,3):
    title,unit,mean,sd,ns,cs,limit,threshold,reports=p
    body+=f'\\problemtitle{{{num}}}{{{title}}}{{'+('Core' if num<6 else 'Extension')+'}\n'
    body+=f'The population response is {title.lower()}, measured in {unit}. Assume independent random samples and a valid normal approximation. For the budget comparison, $\\bar x={mean}$ and known $\\sigma={sd}$ at both $n={ns[0]}$ and $n={ns[1]}$. The two levels are $C={int(cs[0]*100)}\\%$ and $\\alpha={fmt(1-D(str(cs[1])))}$, using cutoffs {fmt(z[cs[0]])} and {fmt(z[cs[1]])}. The full-width limit is {limit} {unit} at both levels.\n'
    body+=f'Reports A and B each omit $\\bar x,n$; eligibility requires $n\\ge{threshold[0]}$ and $\\bar x\\ge{threshold[1]}$ {unit}. Reports C and D each omit $\\bar x,\\sigma$; the priority rule requires both the higher observed mean and the greater population SD. Every report is independent and used the known-$\\sigma$ normal procedure; in C and D that known population SD was omitted from publication. Bounds are exact for the stated cutoffs.\n'
    body+=r'\ClassroomRuledTable{.12\linewidth}{.31\linewidth}{\textbf{Report} & \textbf{Published interval} & \textbf{Supplied construction information}}{'+'\n'
    for j,(m,s,n,c) in enumerate(reports):
        e=z[c]*D(str(s))/D(str(int(sqrt(n))))
        lower,upper=D(str(m))-e,D(str(m))+e
        info=(f'$\\sigma={s}$' if j<2 else f'$n={n}$')
        clevel=f'$C={int(c*100)}\\%$' if j%2==0 else f'$\\alpha={fmt(1-D(str(c)))}$'
        body+=f'{chr(65+j)} & $[{fmt(lower)},{fmt(upper)}]$ & {info}; {clevel}; $z^*={fmt(z[c])}$.\\\\ \\hline\n'
    body+='}\n\n'
body+=r'\par\clearpage'+'\n'+r'\endgroup'+'\n'+r'\end{document}'+'\n'
out=root/'book2026-2027/grade11/term_2/2-class_activities/G11_T2_L1_C4_classroom_activity.tex'
out.write_text(prefix+body,encoding='utf-8')
print(out)
