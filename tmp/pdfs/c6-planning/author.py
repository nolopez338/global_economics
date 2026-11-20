from pathlib import Path
from math import ceil,sqrt
from statistics import NormalDist
norm=NormalDist()

root=Path.cwd()
out=root/'book2026-2027/grade11/term_2/1-practice_activities/G11_T2_L2_C6_practice.tex'
old=out.read_text()
preamble=old.split('\\begin{document}')[0]
local=r'''
% Local specialization of the existing C6 entry: shared registry stays unchanged.
\expandafter\renewcommand\csname practicehighlightlegend@G11-T2-C6-coordinated\endcsname{%
\begingroup
\CoordinatedLegendTable{
$\HLObservationCount{n}$, $\HLObservationCount{n_{\min}}$ & \HLObservationCount{Sample size} & Number of usable observations.\\
$\HLPopulationSD{\sigma}$; $\HLModelControl{p_0}$ & Fixed variability inputs & Known spread; assumed planning share.\\
$\HLStandardError{SE(n)}$, $\HLStandardError{S}$ & \HLStandardError{Standard error} & Sampling spread and its cap.\\
$\HLConfidence{C}$, $\HLConfidence{C_0}$ & \HLConfidence{Confidence level} & Central normal probability and target.\\
$\HLCriticalValue{z^*}$, $\HLCriticalValue{z_0}$ & \HLCriticalValue{Critical value} & Normal multiplier for confidence.\\
$\HLMarginOfError{E}$, $\HLMarginOfError{E_0}$ & \HLMarginOfError{Margin of error} & Half-width and its cap.\\
$\HLIntervalWidth{W}$, $\HLIntervalWidth{W_0}$ & \HLIntervalWidth{Total width} & Full interval length and its cap.\\
}\endgroup}
\newcommand{\IntroOne}{\textbullet\ \hyperref[ex:intro-one]{Example 1}: }
\newcommand{\IntroTwo}{\textbullet\ \hyperref[ex:intro-two]{Example 2}: }
'''
s=r'''\begin{document}
\maketitle
\setcounter{tocdepth}{1}\setcounter{secnumdepth}{3}
\phantomsection\label{toc}\tableofcontents
\section*{Evaluated criteria}
\begin{enumerate}[label=\textbf{C\arabic*},start=6]
\item Determines the sample size required to estimate a population's mean or proportion with a specified margin of error, using it to plan economic surveys or financial studies with predetermined precision.
\end{enumerate}
\textbf{How to practise.} Try each task before opening its blue solution link. Record the target, what stays fixed, the inequality, the unrounded bound and the smallest integer that works. The arrows return to the contents, problem list or current problem.
\clearpage
\section{Introduction}\label{sec:introduction}
\subsection*{Highlight legend}\phantomsection\label{tab:highlight-legend}
\PracticeHighlightLegend{G11-T2-C6-coordinated}
Names and units retain meaning without color. Related shades connect related quantities; standard error, confidence, critical value, half-width and total width remain distinct roles.
\subsection{Introductory example 1: cargo clearance}\label{ex:intro-one}
A port wants the unknown population mean $\HLPopulationMean{\mu}$ clearance time. Its known population standard deviation is $\HLPopulationSD{\sigma}=\HLPopulationSD{12\text{ min}}$. For a random sample of $\HLObservationCount{n}$ records, the sample mean has
\[
\HLStandardError{SE_{\rm mean}(n)}=\frac{\HLPopulationSD{\sigma}}{\sqrt{\HLObservationCount{n}}}.
\]
At $n=100$, $SE=1.2$ minutes. A central $\HLConfidence{95\%}$ normal interval uses $\HLCriticalValue{z^*}\approx\HLCriticalValue{1.95996398454}$, so its $\HLMarginOfError{E}=z^*SE\approx2.352$ minutes and its $\HLIntervalWidth{W}=2E\approx4.704$ minutes. The interval is centered on the future sample mean, not on the unknown $\mu$.
\subsection{Introductory example 2: household energy}\label{ex:intro-two}
An energy office wants the unknown population proportion $\HLPopulationProportion{p}$ eligible for a subsidy. A pilot suggests the fixed planning value $\HLModelControl{p_0}=\HLModelControl{0.20}$; the future sample proportion $\HLSampleProportion{\hat p}$ will be calculated from collected responses. For planning,
\[
\HLStandardError{SE_{\rm proportion}(n)}\approx
\sqrt{\frac{\HLModelControl{p_0}(1-\HLModelControl{p_0})}{\HLObservationCount{n}}}.
\]
At $n=400$, planning $SE=0.02$, or 2 percentage points. A 95\% interval has planning $E\approx0.03920$ (3.920 percentage points), and $W\approx0.07840$ (7.840 percentage points). A cap of 4 percentage points means $E_0=0.04$, not 4. The pilot is an assumption, not knowledge of $p$ or a prediction that $\hat p=p_0$.
\textbf{Quick check.} A full width of 8 percentage points permits a margin of only 4 percentage points. Changing confidence changes the multiplier, not the standard error for a fixed design and $n$.
\clearpage
\section{Notation Reference and Practice Procedure}\label{sec:notation-and-procedure}
\subsection{Notation reference}\label{tab:notation-reference}
\begingroup\setlength{\tabcolsep}{4pt}\renewcommand{\arraystretch}{1.18}
\begin{longtable}{@{}>{\raggedright\arraybackslash}p{.17\linewidth}>{\raggedright\arraybackslash}p{.18\linewidth}>{\raggedright\arraybackslash}p{.27\linewidth}>{\raggedright\arraybackslash}p{\dimexpr.38\linewidth-6\tabcolsep\relax}@{}}
\toprule
\textbf{Symbol or notation}&\textbf{Concept}&\textbf{Definition}&\textbf{Meaning in the introductory examples}\\\midrule\endfirsthead
\toprule\textbf{Symbol or notation}&\textbf{Concept}&\textbf{Definition}&\textbf{Meaning in the introductory examples}\\\midrule\endhead
$\HLObservationCount{n},\HLObservationCount{n_{\min}}$ & \HLObservationCount{Sample size} & Positive integer count; least count meeting all targets. & \IntroOne Usable cargo records.\par\IntroTwo Completed household responses.\\
$\HLPopulationMean{\mu},\HLSampleMean{\bar x}$ & Population and sample means & Fixed population average; average calculated from the sample. & \IntroOne Unknown mean clearance time and its estimate, in minutes.\\
$\HLPopulationSD{\sigma}$ & \HLPopulationSD{Population spread} & Known population standard deviation, in response units. & \IntroOne $\HLPopulationSD{12\text{ min}}$, held fixed as $n$ changes.\\
$\HLPopulationProportion{p}$; $\HLModelControl{p_0}$; $\HLSampleProportion{\hat p}$ & Population, planning and sample shares & Unknown population share; assumed design input; observed sample share. All are proportions. & \IntroTwo Subsidy eligibility: $p$ is unknown, $\HLModelControl{p_0}=\HLModelControl{0.20}$ comes from a pilot; $\hat p$ is future data.\\
$\HLStandardError{SE(n)},\HLStandardError{S}$ & \HLStandardError{Sampling spread and cap} & Standard deviation of an estimator (planning approximation for a proportion); maximum allowed SE. & \IntroOne Minutes.\par\IntroTwo Proportion units; $0.02=2$ percentage points.\\
$\HLConfidence{C},\HLConfidence{C_0}$ & \HLConfidence{Confidence and target} & Central normal probability and its minimum required level. & \IntroOne\IntroTwo $\HLConfidence{0.95}$ corresponds to $\HLConfidence{95\%}$.\\
$\HLCriticalValue{z^*},\HLCriticalValue{z_0}$; $\Phi$ & \HLCriticalValue{Normal quantile}; CDF & $z^*=\Phi^{-1}((1+C)/2)$; $z_0$ uses $C_0$. $\Phi(t)=P(Z\le t)$ for $Z\sim N(0,1)$. & \IntroOne\IntroTwo At 95\%, $\HLCriticalValue{z^*}\approx\HLCriticalValue{1.95996398454}$.\\
$\HLMarginOfError{E},\HLMarginOfError{E_0}$ & \HLMarginOfError{Half-width and cap} & $E=z^*SE$; maximum permitted distance from interval center to an endpoint. & \IntroOne Minutes.\par\IntroTwo $\HLMarginOfError{0.04}$ means a cap of $\HLMarginOfError{4}$ percentage points.\\
$\HLIntervalWidth{W},\HLIntervalWidth{W_0}$ & \HLIntervalWidth{Total width and cap} & $W=2E$; maximum full interval length. & \IntroOne About 4.704 minutes.\par\IntroTwo About 7.840 percentage points.\\
$V$; $\lceil b\rceil$ & Compact variability; ceiling & $V=\sigma^2$ or $p_0(1-p_0)$; least integer at least $b$. & \IntroOne $V=144\text{ min}^2$.\par\IntroTwo $V=0.16$ (squared proportion units).\\
$N$; $np_0$, $n(1-p_0)$ & Population size; expected counts & Use $n\le0.10N$ without replacement; check both expected counts at least 10. & \IntroTwo Expected eligible and other households under the planning assumption.\\
\bottomrule\end{longtable}\endgroup
\hyperref[tab:highlight-legend]{Return to the concise legend.}
\clearpage
\subsection{Models, assumptions and calculator use}
For a mean, use a simple random sample, known $\sigma>0$, and a normal population or a sample mean for which a normal approximation is suitable. For a proportion, use random binary outcomes and the normal planning approximation, with $0<p_0<1$. A pilot-based result is conditional on that assumed planning proportion. Check $np_0\ge10$ and $n(1-p_0)\ge10$ at planning; after collection check the actual counts $n\hat p$ and $n(1-\hat p)$ and the interval conditions again.

Without a dependable pilot, $p_0=0.50$ is conservative because
\[
p_0(1-p_0)=\tfrac14-(p_0-\tfrac12)^2\le\tfrac14.
\]
This bounds variability and the normal-formula planning margin over possible proportions. It does not guarantee exact finite-sample coverage or accuracy for every realized sample. All worked populations below have $N=100{,}000$ eligible units; their samples satisfy $n\le10{,}000$. This supports approximate independence without replacement. Finite-population corrections are outside scope.

\textbf{Calculator instructions.} Use inverse normal with mean 0, standard deviation 1 and left-tail area $(1+C)/2$. Use normal CDF with lower endpoint $-\infty$, upper endpoint $t$, mean 0 and standard deviation 1 to obtain $\Phi(t)$. Store full calculator precision:
\[
z_{.95}=\Phi^{-1}(0.975)\approx1.959963984540054,\qquad
z_{.90}=\Phi^{-1}(0.95)\approx1.644853626951472.
\]
These stored values are used throughout; displayed results are rounded only after calculation. Use extra digits when comparing a result with a cap; a coarse normal table can obscure a minimum-size decision.
\subsection{Reusable decision procedure}
\begin{enumerate}
\item Identify the unknown integer $n$, the estimator and units. List the target and what stays fixed: variability always; confidence in Types 2--3; precision cap in Type 4. Convert percentage points to proportions.
\item Write the explicit mean or proportion SE formula first. Check the model, sampling fraction and expected counts where relevant.
\item Choose the inequality: $SE\le S$, $z^*SE\le E_0$, $2z^*SE\le W_0$, or $C(n)\ge C_0$ with fixed $E_0>0$.
\item Rearrange using positive quantities. Calculate the unrounded lower bound $b$, then $n_{\min}=\lceil b\rceil$. An integer bound stays unchanged; never automatically add one.
\item Check $n_{\min}$ works and $n_{\min}-1$ fails when $n_{\min}>1$. The relevant SE, margin and width decrease with $n$; fixed-cap confidence increases with $n$. Thus the adjacent checks establish minimality.
\item Interpret the answer as usable observations or completed responses. Invitations may need to exceed this count if there is nonresponse.
\end{enumerate}
\clearpage
\section{General Worked Problems}\label{sec:worked-solution-examples}
\SectionProblemsTableOfContents{
\SectionProblemLink{prob:t1}{Type 1: maximum standard error}\\
\SectionProblemLink{prob:t2}{Type 2: maximum margin of error}\\
\SectionProblemLink{prob:t3}{Type 3: maximum total width}\\
\SectionProblemLink{prob:t4}{Type 4: minimum confidence with fixed precision}}
\medskip
After the explicit SE formulas above, write $V=\sigma^2$ for a mean or $V=p_0(1-p_0)$ for a proportion. Thus $SE(n)=\sqrt{V/n}$ (approximately for a proportion). Treat all proportion calculations below as normal-formula planning calculations.
'''
types=[
('t1','Type 1: minimum sample size for a standard-error cap',r'''Keep population variability fixed and supply $\HLStandardError{S}>0$. Confidence level does not enter either standard-error formula:
\[
\sqrt{V/n}\le S\ \Longleftrightarrow\ V/n\le S^2
\ \Longleftrightarrow\ n\ge V/S^2,
\qquad n_{\min}=\left\lceil V/S^2\right\rceil.
\]'''),
('t2','Type 2: minimum sample size for a margin-of-error cap',r'''Keep confidence level and population variability fixed; supply $\HLMarginOfError{E_0}>0$:
\[
z^*\sqrt{V/n}\le E_0
\ \Longleftrightarrow\ \sqrt n\ge\frac{z^*\sqrt V}{E_0}
\ \Longleftrightarrow\ n\ge\frac{(z^*)^2V}{E_0^2}.
\]
Hence $n_{\min}=\left\lceil (z^*)^2V/E_0^2\right\rceil$.'''),
('t3','Type 3: minimum sample size for a total-width cap',r'''Keep confidence level and population variability fixed; supply $\HLIntervalWidth{W_0}>0$. Total width is twice the margin, so $E_0=W_0/2$:
\[
2z^*\sqrt{V/n}\le W_0
\ \Longleftrightarrow\ \sqrt n\ge\frac{2z^*\sqrt V}{W_0}
\ \Longleftrightarrow\ n\ge\frac{4(z^*)^2V}{W_0^2}.
\]
Hence $n_{\min}=\left\lceil4(z^*)^2V/W_0^2\right\rceil$.'''),
('t4','Type 4: minimum sample size to support a confidence target',r'''Supply a target $\HLConfidence{C_0}\in(0,1)$ \emph{and} a fixed positive precision cap $\HLMarginOfError{E_0}$. Keep variability and that cap fixed. Confidence alone cannot determine $n$: one must also limit the interval's half-width (or total width).

Under the normal planning model, the maximum central confidence associated with fixed half-width $E_0$ is
\[
\HLConfidence{C(n)}=2\Phi\!\left(\frac{E_0\sqrt n}{\sqrt V}\right)-1.
\]
Indeed the interval reaches $E_0/SE$ standard errors on each side of its center. Since $\Phi$ is increasing, with $z_0=\Phi^{-1}((1+C_0)/2)$,
\[
C(n)\ge C_0\ \Longleftrightarrow\ \frac{E_0\sqrt n}{\sqrt V}\ge z_0
\ \Longleftrightarrow\ n\ge\frac{z_0^2V}{E_0^2},\qquad
n_{\min}=\left\lceil z_0^2V/E_0^2\right\rceil.
\]
This is the Type 2 inequality at the target critical value, viewed as the confidence a fixed precision cap can support. At the chosen $n$, use $C_0$ or any confidence up to $C(n)$ while respecting the cap. It does not permit arbitrarily high confidence at the same precision.''')]
cases=[
 dict(t=1,k='mean',label='prob:t1-mean',title='Cargo records: a standard error of at most 1.5 minutes',sig=12,cap=1.5,C=None,unit='minutes',obs='cargo records'),
 dict(t=1,k='prop',label='prob:t1-prop',title='Energy eligibility: a standard error of at most 2.5 percentage points',p=.2,cap=.025,C=None,unit='proportion units',obs='household responses'),
 dict(t=2,k='mean',label='prob:c6-1',title='Planning a port inspection study (C6)',sig=12,cap=3,C=.95,unit='minutes',obs='cargo records'),
 dict(t=2,k='prop',label='prob:c6-2',title='Planning a household energy survey (C6)',p=.2,cap=.04,C=.95,unit='proportion units',obs='household responses'),
 dict(t=3,k='mean',label='prob:t3-mean',title='Export processing: a total width of at most 5 minutes',sig=15,cap=5,C=.9,unit='minutes',obs='export records'),
 dict(t=3,k='prop',label='prob:t3-prop',title='Energy uptake: a total width of at most 6 percentage points',p=.5,cap=.06,C=.95,unit='proportion units',obs='household responses'),
 dict(t=4,k='mean',label='prob:t4-mean',title='Cargo planning: support at least 95 percent confidence',sig=12,cap=2,C=.95,unit='minutes',obs='cargo records'),
 dict(t=4,k='prop',label='prob:t4-prop',title='Subsidy planning: support at least 90 percent confidence',p=.3,cap=.03,C=.9,unit='proportion units',obs='household responses')]
for tid,title,derivation in types:
 s+='\n\\subsection{'+title+'}\\label{prob:'+tid+'}\n'+derivation+'\n'
 group=[c for c in cases if c['t']==int(tid[-1])]
 s+='\\SectionProblemsTableOfContents{\n'+'\\\\\n'.join('\\SectionProblemLink{'+c['label']+'}{'+('Mean: '+c['obs'] if c['k']=='mean' else 'Proportion: '+('conservative planning' if c['p']==.5 else 'pilot-based planning'))+'}' for c in group)+'}\n\\medskip\n'
 for c in group:
  t=c['t']; prop=c['k']=='prop'; cap=c['cap']; z=norm.inv_cdf((1+c['C'])/2) if c['C'] else 1
  v=c['p']*(1-c['p']) if prop else c['sig']**2
  b=v/cap**2*(z*z if t in (2,4) else 4*z*z if t==3 else 1)
  if abs(b-round(b))<1e-9:b=round(b)
  n=ceil(b); c.update(v=v,b=b,n=n,z=z)
  label=c['label']; sol=label.replace('prob:','sol:')
  s+='\\clearpage\n\\subsubsection{'+c['title']+'}\\label{'+label+'}\n'
  if prop:
   s+=('An energy office estimates the unknown population share $p$ of households '+('adopting an efficiency tariff' if t==3 else 'eligible for a bill subsidy')+'. It will draw a simple random sample without replacement from $N=100{,}000$ households. ')
   s+=('No dependable pilot is available: hold $\\HLModelControl{p_0}=\\HLModelControl{0.50}$ fixed for conservative planning. ' if c['p']==.5 else f'A pilot suggests $\\HLModelControl{{p_0}}=\\HLModelControl{{{c["p"]:.2f}}}$; hold this planning value fixed. ')
  else:
   s+=f'A logistics agency estimates the unknown population mean {"export-processing" if t==3 else "cargo-clearance"} time. It will draw a simple random sample without replacement from $N=100{{,}}000$ eligible {c["obs"]}. Hold the known population spread $\\HLPopulationSD{{\\sigma}}=\\HLPopulationSD{{{c["sig"]}\\text{{ min}}}}$ fixed. Assume the sample mean is suitably approximated by a normal distribution. '
  capname={1:'standard error',2:'margin of error',3:'total interval width',4:'margin of error'}[t]
  captext=(f'{cap*100:g} percentage points, namely {cap:g} in proportion units' if prop else f'{cap:g} minutes')
  s+=f'The {capname} cap is {captext}. '
  if c['C']:s+=f'{"Require at least" if t==4 else "Hold confidence fixed at"} $\\HLConfidence{{{100*c["C"]:g}\\%}}$, using ${"z_0" if t==4 else "z^*"}=z_{{.{round(c["C"]*100)}}}$. '
  else:s+='No confidence level is needed for this standard-error target. '
  if t==4:s+='Keep the positive precision cap fixed while finding the minimum sample size that supports the confidence target. '
  s+='\n\\QuestionsTasks[sec:worked-solution-examples]{{6}/{'+sol+'}/{Find the minimum integer sample size. State the unknown, target, fixed quantities, units and model; rearrange the inequality, round correctly, check adjacent integers and interpret the result.}}\n'
  s+='\\subsubsection*{Worked solution (C6)}\\label{'+sol+'}\n'
  if label=='prob:c6-1':s+='\\phantomsection\\label{sol:c6-1-a}\\label{sol:c6-1-b}\n'
  if label=='prob:c6-2':s+='\\phantomsection\\label{sol:c6-2-a}\\label{sol:c6-2-b}\n'
  s+=f'\\textbf{{Design.}} The unknown is $\\HLObservationCount{{n}}$, the number of usable {c["obs"]}. '
  s+=f'The target is {capname} at most {captext}'+(f' with {"at least " if t==4 else ""}{100*c["C"]:g}\\% confidence. ' if c['C'] else '. ')
  s+=('The planning share remains fixed; $p$ is unknown and $\\hat p$ is the future estimate. Use the normal approximation for random binary outcomes; expected-count checks appear below. ' if prop else 'Population variability remains fixed. Use the known-$\\sigma$ normal model for the sample mean. ')
  if t in (2,3):s+='Confidence also remains fixed. '
  if t==4:s+='The margin cap also remains fixed. '
  if t==1:s+='Confidence does not enter $SE(n)$. '
  spread=f'\\sqrt{{{c["p"]:.2f}({1-c["p"]:.2f})}}' if prop else str(c['sig'])
  explicit=f'\\sqrt{{\\frac{{{c["p"]:.2f}({1-c["p"]:.2f})}}{{n}}}}' if prop else f'\\frac{{{c["sig"]}}}{{\\sqrt n}}'
  mult='2z^*' if t==3 else 'z^*' if t==2 else 'z_0' if t==4 else ''
  if t==4:s+='\n\\[C(n)\\ge C_0\\ \\Longleftrightarrow\\ E_0\\sqrt n/\\sqrt V\\ge z_0\\ \\Longleftrightarrow\\ z_0SE(n)\\le E_0.\\]\n'
  s+='\n\\[\n'+mult+explicit+f'\\le {cap:g}\\quad\\Longrightarrow\\quad'
  factor='2' if t==3 else ''
  zn='z_0' if t==4 else 'z^*' if t==2 or t==3 else ''
  s+='\\sqrt n\\ge\\frac{'+factor+zn+spread+'}{'+f'{cap:g}'+'}.\n\\]\n'
  s+='\\[n\\ge\\left(\\frac{'+factor+zn+spread+'}{'+f'{cap:g}'+'}\\right)^2'
  s+='='+str(b) if isinstance(b,int) else '\\approx'+f'{b:.9f}'
  s+=f',\\qquad \\HLObservationCount{{n_{{\\min}}}}=\\left\\lceil {b:.9f}'.rstrip('0').rstrip('.')+'\\right\\rceil=\\HLObservationCount{'+str(n)+'}.\\]\n'
  if isinstance(b,int):s+='The bound is already an integer, so retain it; do not add one.\n'
  else:s+='Round upward, because rounding down would violate the inequality.\n'
  if t==4:
   def conf(m):return 2*norm.cdf(cap*sqrt(m)/sqrt(v))-1
   s+=f'\\textbf{{Check confidence at fixed half-width.}} With $V={v:g}$,\n\\[\nC({n})=2\\Phi({cap:g}\\sqrt{{{n}}}/\\sqrt{{{v:g}}})-1\\approx {conf(n):.9f}\\ge {c["C"]:g},\n\\]\n\\[C({n-1})\\approx {conf(n-1):.9f}<{c["C"]:g}.\\]\n'
   metric=lambda m:z*sqrt(v/m)
   s+=f'Equivalently, at the target confidence the margins are ${metric(n):.9f}\\le {cap:g}$ and ${metric(n-1):.9f}>{cap:g}$ {c["unit"]}, respectively. '
  else:
   metric=lambda m:(2*z if t==3 else z if t==2 else 1)*sqrt(v/m)
   name={1:'SE',2:'E',3:'W'}[t]
   s+=f'\\textbf{{Adjacent-integer check}} ({c["unit"]}):\n\\[ {name}({n})\\approx{metric(n):.9f}\\le {cap:g},\\qquad {name}({n-1})\\approx{metric(n-1):.9f}>{cap:g}.\\]\n'
   if t==3:s+=f'The permitted half-width is ${cap/2:g}$ {c["unit"]}; ${cap:g}$ is the full width, not the margin. '
  if prop:
   s+=f'Expected outcome counts are $np_0={n*c["p"]:g}$ and $n(1-p_0)={n*(1-c["p"]):g}$, both at least 10. '
  s+=f'The sampling fraction is ${n}/100{{,}}000={n/1000:g}\\%<10\\%$. '
  s+=f'Because {"C(n) increases" if t==4 else "the target quantity decreases"} with $n$, the checks establish minimality. Plan for $\\HLObservationCount{{{n}}}$ usable {c["obs"]}. '
  if prop:s+=('This conservative variability bound applies under the normal-formula planning model, not as exact coverage or guaranteed realized accuracy. ' if c['p']==.5 else 'This pilot-based result is conditional on the assumed planning proportion. ')+ 'After data collection, check actual outcome counts and the interval conditions. '
  s+='\n\\secInicio['+label+'][sec:worked-solution-examples]\n'
# Advanced section appended separately.
out.write_text(preamble+local+s,encoding='utf-8')
for c in cases:print(c['t'],c['k'],'bound=',c['b'],'n=',c['n'])


