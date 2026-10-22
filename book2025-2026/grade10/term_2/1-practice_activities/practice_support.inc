% Local compatibility helpers; compile the six G10 documents, not this include.
\graphicspath{{../../../preamble/}{../../../preamble/imgs/}}
\providecommand{\ExamTitleBlock}[3]{%
  \begin{center}
    {\large\bfseries GLOBAL ECONOMICS\par}
    \textbf{#1}\par
    \textbf{#2}\par
    #3
  \end{center}
}
\providecommand{\ExamSection}[1]{\section*{#1}}
\newenvironment{ExamProblems}
  {\begin{enumerate}[label=\arabic*.,leftmargin=*]}
  {\end{enumerate}}
