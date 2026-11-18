from pathlib import Path
p = Path('book2026-2027/grade11/term_2/3-slides/G11_T2_L1_C2_slides.tex')
s = p.read_text(encoding='utf-8')
start = s.index(r'\begin{frame}[t]{Task 2 -- Point estimate}')
end = s.index(r'\section{Coverage evidence}', start)
replacement = r'''% Task 2 uses one cumulative overlay sequence. Both tables are typeset in
% full on every overlay; \R reserves the final size of each unrevealed cell.
% Task 1's \InfoTables and its original overlay sequence are unchanged.
\newcommand{\TaskTwoTableStyle}{%
  \fontsize{9.5}{10}\selectfont\setlength{\parskip}{0pt}%
  \setlength{\tabcolsep}{2pt}\renewcommand{\arraystretch}{1.0}%
  \setlength{\aboverulesep}{1pt}\setlength{\belowrulesep}{1pt}%
  \tikzset{ge marker/.append style={inner xsep=.25mm,inner ysep=.1mm}}}
\newcommand{\TaskTwoReference}{%
  \begingroup\TaskTwoTableStyle
  \textbf{Task 1 reference}\par\smallskip
  \begin{tabularx}{\linewidth}{@{}>{\raggedright\arraybackslash}p{.15\linewidth}>{\raggedright\arraybackslash}p{.39\linewidth}>{\raggedright\arraybackslash}X@{}}
  \toprule
  \textbf{Symbol}&\textbf{Concept}&\textbf{In context...}\\\midrule
  \multicolumn{3}{@{}l}{\textbf{Sample statistics}}\\\midrule
  \IR{5}{SampleMean}{\bar{x}}{Sample mean}{40 minutes}{}
  \IR{6}{SampleSize}{n}{Sample size}{49 trips}{}
  \IR{7}{StandardError}{\mathrm{SE}}{Standard error}{2 minutes}{}
  \midrule
  \multicolumn{3}{@{}l}{\textbf{Procedure Settings}}\\\midrule
  \IR{9}{Confidence}{C}{Confidence level}{95\% = 0.95}{}
  \IR{11}{Confidence}{\alpha}{Significance level}{0.05}{}
  \IR{13}{Confidence}{\alpha/2}{Tail area}{0.025}{}
  \IR{15}{Critical}{z^*}{Critical value}{1.960}{}
  \bottomrule
  \end{tabularx}\par\endgroup}
\newcommand{\TaskTwoLabel}[4]{\At{#1}{#2}{$#3$}\par\Words{#1}{#2}{#4}}
\newcommand{\TaskTwoWorkingTable}{%
  \begingroup\TaskTwoTableStyle
  \textbf{Task 2 working table}\par\smallskip
  \begin{tabularx}{\linewidth}{@{}>{\raggedright\arraybackslash}p{.20\linewidth}>{\raggedright\arraybackslash}X@{}}
  \toprule
  \textbf{Symbol / Concept}&\textbf{Calculation, Result and meaning in context}\\\midrule
  \TaskTwoLabel{2}{SampleMean}{\bar{x}}{Point estimate}&
  \R{2}{$\CtwoPoint{\bar{x}}$}\R{3}{$=\CtwoPoint{40}$ minutes.}\par
  \R{4}{One estimate of the mean cycling-trip duration.}\\\midrule
  \TaskTwoLabel{5}{MarginError}{\mathrm{MoE}}{Margin of error}&
  \R{5}{$\CtwoMoE{\mathrm{MoE}}=\CtwoCritical{z^*}\times\CtwoSE{\mathrm{SE}}$}\par
  \R{6}{$=\CtwoCritical{1.960}\times\CtwoSE{2}$}\R{7}{$=\CtwoMoE{3.92}$ minutes.}\par
  \R{8}{Centre-to-endpoint uncertainty in mean duration.}\\\midrule
  \TaskTwoLabel{9}{Endpoint}{L}{Lower endpoint}&
  \R{9}{$\CtwoEndpoint{L}=\CtwoPoint{\bar{x}}-\CtwoMoE{\mathrm{MoE}}$}\R{10}{$=\CtwoPoint{40}-\CtwoMoE{3.92}$}\R{11}{$=\CtwoEndpoint{36.08}$ min.}\\\midrule
  \TaskTwoLabel{12}{Endpoint}{U}{Upper endpoint}&
  \R{12}{$\CtwoEndpoint{U}=\CtwoPoint{\bar{x}}+\CtwoMoE{\mathrm{MoE}}$}\R{13}{$=\CtwoPoint{40}+\CtwoMoE{3.92}$}\R{14}{$=\CtwoEndpoint{43.92}$ min.}\\\midrule
  \TaskTwoLabel{15}{Endpoint}{\mathrm{CI}}{Confidence interval}&
  \R{15}{$\CtwoCI{\mathrm{CI}}=[\CtwoEndpoint{L},\CtwoEndpoint{U}]$}\R{16}{$=[\CtwoEndpoint{36.08},\CtwoEndpoint{43.92}]$ minutes.}\par
  \R{17}{Plausible values for the fixed population mean under the model.}\\\midrule
  \TaskTwoLabel{18}{Width}{W}{Full width}&
  \R{18}{$\CtwoWidth{W}=\CtwoEndpoint{U}-\CtwoEndpoint{L}=2\CtwoMoE{\mathrm{MoE}}$}\par
  \R{19}{$=\CtwoEndpoint{43.92}-\CtwoEndpoint{36.08}=2(\CtwoMoE{3.92})$}\R{20}{$=\CtwoWidth{7.84}$ minutes.}\par
  \R{21}{The interval span describes precision.}\\\midrule
  \TaskTwoLabel{22}{Endpoint}{\mathrm{CI}}{Interval interpretation}&
  \R{22}{We are \CtwoConfidence{95\%} \CtwoConfidence{confident} that the population mean cycling-trip duration lies in $[\CtwoEndpoint{36.08},\CtwoEndpoint{43.92}]$ minutes, a range of plausible values under the model.}\\
  \bottomrule
  \end{tabularx}\par\endgroup}
\begin{frame}[t]{Task 2 -- Point estimate and confidence interval}
\Referencetrue
% Reference values never disappear; their colors activate when first used.
\expandafter\def\csname Input5\endcsname{2}
\expandafter\def\csname Input6\endcsname{0}
\expandafter\def\csname Input7\endcsname{5}
\expandafter\def\csname Input9\endcsname{22}
\expandafter\def\csname Input11\endcsname{0}
\expandafter\def\csname Input13\endcsname{0}
\expandafter\def\csname Input15\endcsname{5}
\begin{columns}[T,onlytextwidth]
\begin{column}{.28\textwidth}\TaskTwoReference\end{column}
\begin{column}{.70\textwidth}\TaskTwoWorkingTable\end{column}
\end{columns}
\end{frame}
'''
p.write_text(s[:start]+replacement+s[end:], encoding='utf-8')
