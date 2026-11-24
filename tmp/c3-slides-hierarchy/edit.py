from pathlib import Path
import re
p=Path('book2026-2027/grade10/term_2/3-slides/G10_T2_L1_C3_slides.tex')
s=p.read_text()
Path('tmp/c3-slides-hierarchy/original.tex').write_text(s)
macros=r'''
% Structural hierarchy adapted from Worked Example 1; independent of highlights.
\newcommand{\TaskName}[1]{\ifcase#1\or
Establish the binary model and monetary transformations.\or
Individual expected values.\fi}
\newcommand{\SubtaskName}[2]{\ifcase#1\or
  \ifcase#2\or Binary model and monetary transformations.\or
  Supports, PMFs, and ordered CDFs.\or Initial probabilities and loss events.\fi
\or
  \ifcase#2\or Initial expected values.\or
  Expectation formulas and sign intervals.\or Graphs.\fi
\fi}
\newcommand{\TaskHeading}[1]{%
  \par\noindent\tikz[baseline=(tasktitle.base)]{%
    \node[fill=black!5,text=GEInk,rounded corners=2mm,
      inner xsep=4pt,inner ysep=3pt,outer sep=0pt,
      text width=\dimexpr\linewidth-8pt\relax,align=left,
      font=\small\bfseries] (tasktitle) {Task #1 --- \TaskName{#1}};}\par}
\newcommand{\SubtaskHeading}[2]{%
  {\normalsize\bfseries\underline{#2. \SubtaskName{#1}{#2}}\par}}
\newcommand{\ActiveTask}{0}
\newcommand{\ActiveSubtask}{0}
\newcommand{\SetTaskSubtask}[2]{\renewcommand{\ActiveTask}{#1}%
  \renewcommand{\ActiveSubtask}{#2}}
\newcommand{\ActiveHierarchy}{%
  \ifnum\ActiveTask>0
    \TaskHeading{\ActiveTask}\vskip2pt
    \SubtaskHeading{\ActiveTask}{\ActiveSubtask}\vskip3pt
  \fi}
'''
s=s.replace('\\setbeamertemplate{frametitle}{%',macros+'\n\\setbeamertemplate{frametitle}{%')
s=s.replace('  \\vskip.5em\n','  \\vskip.3em\n  \\ActiveHierarchy\n',1)
start=s.index('\\begin{frame}[t]{The questions we will answer}')
end=s.index('\\end{frame}',start)+len('\\end{frame}')
s=s[:start]+r'''\begin{frame}[t]{The questions we will answer (1/2)}
\TaskHeading{1}
\medskip
\SubtaskHeading{1}{1}
Define one observation, the two states, the indicator and both monetary rules.
\medskip
\SubtaskHeading{1}{2}
Give supports, complete PMFs and numerically ordered piecewise CDFs.
\medskip
\SubtaskHeading{1}{3}
Identify each loss event, its probability and its contextual meaning.
\end{frame}
\begin{frame}[t]{The questions we will answer (2/2)}
\TaskHeading{2}
\medskip
\SubtaskHeading{2}{1}
Calculate initial expectations and interpret them per weekend.
\medskip
\SubtaskHeading{2}{2}
Keep payoffs fixed; vary $p\in[0,1]$. Find each expectation formula,
its own break-even threshold and sign intervals.
\medskip
\SubtaskHeading{2}{3}
Draw separate labelled graphs and check endpoints and roots.
\end{frame}'''+s[end:]
# Explicit frame metadata keeps every continuation in the same visible hierarchy.
original=Path('tmp/c3-slides-hierarchy/original.tex').read_text()
frames=list(re.finditer(r'\\begin\{frame\}(?:\[t\])?\{([^\n]*)\}',original))
titles=[m.group(1) for m in frames]
def setbefore(title,task,sub):
 global s
 target='\\begin{frame}[t]{'+title+'}'
 assert s.count(target)==1,(title,s.count(target))
 s=s.replace(target,f'\\SetTaskSubtask{{{task}}}{{{sub}}}\n'+target)
# Title-less first frame is excluded; original frame 2 has index 0 here.
for i,title in enumerate(titles,2):
 if 8<=i<=14: setbefore(title,1,1)
 elif 15<=i<=21: setbefore(title,1,2)
 elif 22<=i<=23: setbefore(title,1,3)
 elif 24<=i<=26: setbefore(title,2,1)
 elif 27<=i<=32: setbefore(title,2,2)
 elif 33<=i<=37: setbefore(title,2,3)
 elif i==38: setbefore(title,0,0)
s=s.replace('{Task 2: probability-weighted net profit}','{Probability-weighted net profit}')
# Keep graph text at its current font size; shorten only diagram geometry.
s=s.replace('\\begin{tikzpicture}[x=1cm,y=1cm]','\\begin{tikzpicture}[x=1cm,y=.65cm]')
# Source locations in the original comments predate recent worksheet edits.
s=s.replace('% SOURCE MAP (line numbers refer to sources read 2026-11-24):','% SOURCE MAP (historical line numbers; identify current source by headings):')
s=s.replace('\\begin{document}',r'''% Hierarchy map: Task 1.1 observation/indicator/transformation and checks;
% Task 1.2 support/PMF/CDF prerequisites, distributions and endpoint supports;
% Task 1.3 initial probabilities and loss events. Task 2.1 expectation prerequisite
% and initial expectations; Task 2.2 varying-p formulas, roots and sign intervals;
% Task 2.3 graphs, endpoint/root checks and contextual interpretation.
% Frame comments below retain original frame identifiers for source traceability;
% the two-frame overview adds one logical frame without changing overlay steps.
\begin{document}''',1)
p.write_text(s)
