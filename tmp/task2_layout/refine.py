from pathlib import Path
p=Path('book2026-2027/grade11/term_2/3-slides/G11_T2_L1_C2_slides.tex')
s=p.read_text(encoding='utf-8')
a=s.index(r'\newcommand{\TaskTwoReference}')
b=s.index(r'\newcommand{\TaskTwoLabel}',a)
s=s[:a]+r'''\newcommand{\TaskTwoInput}[5]{%
  \At{\csname Input#1\endcsname}{#2}{$#3$}\ \Words{\csname Input#1\endcsname}{#2}{#4}&%
  \Words{\csname Input#1\endcsname}{#2}{#5}\\[2pt]}
\newcommand{\TaskTwoReference}{%
  \begingroup\TaskTwoTableStyle
  \begin{tabularx}{\linewidth}{@{}>{\raggedright\arraybackslash}p{.61\linewidth}>{\raggedright\arraybackslash}X@{}}
  \toprule
  \textbf{Symbol / Concept}&\textbf{In context...}\\\midrule
  \multicolumn{2}{@{}l}{\textbf{Sample statistics}}\\\midrule
  \TaskTwoInput{5}{SampleMean}{\bar{x}}{Sample mean}{40 minutes}
  \TaskTwoInput{6}{SampleSize}{n}{Sample size}{49 trips}
  \TaskTwoInput{7}{StandardError}{\mathrm{SE}}{Standard error}{2 minutes}
  \midrule
  \multicolumn{2}{@{}l}{\textbf{Procedure Settings}}\\\midrule
  \TaskTwoInput{9}{Confidence}{C}{Confidence level}{95\% = 0.95}
  \TaskTwoInput{11}{Confidence}{\alpha}{Significance level}{0.05}
  \TaskTwoInput{13}{Confidence}{\alpha/2}{Tail area}{0.025}
  \TaskTwoInput{15}{Critical}{z^*}{Critical value}{1.960}
  \bottomrule
  \end{tabularx}\par\endgroup}
''' +s[b:]
s=s.replace(r'  \textbf{Task 2 working table}\par\smallskip'+ '\n','')
s=s.replace(r'\textbf{Symbol / Concept}&\textbf{Calculation',r'\textbf{Symbol/Concept}&\textbf{Calculation')
# Tight rule spacing is local to Task 2. Text and highlight sizes stay unchanged.
start=s.index(r'\newcommand{\TaskTwoTableStyle}')
end=s.index(r'\begin{frame}[t]{Task 2',start)
part=s[start:end].replace(r'\setlength{\aboverulesep}{1pt}\setlength{\belowrulesep}{1pt}',r'\setlength{\aboverulesep}{.2pt}\setlength{\belowrulesep}{.2pt}')
s=s[:start]+part+s[end:]
p.write_text(s,encoding='utf-8')
