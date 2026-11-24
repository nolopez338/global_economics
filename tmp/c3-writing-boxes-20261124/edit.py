from pathlib import Path
import re
p=Path('book2026-2027/grade10/term_2/2-class_activities/G10_T2_L1_C3_classroom_activity.tex')
s=Path('tmp/c3-writing-boxes-20261124/baseline.tex').read_text(encoding='utf-8')
a=s.index('\\stageheading{Worked example}')
b=s.index('\\stageheading{Guided Example}')
c=s.index('\\stageheading{Independent Practice}')
w=s[a:b]
w=re.sub(r'\\vspace\{-[^}]+\}',r'\\vspace{2mm}',w)
w=w.replace('\\stageheading{Worked example}',r'''\begingroup
% Positive spacing is confined to the worked example.
\setlength{\abovedisplayskip}{18pt}
\setlength{\belowdisplayskip}{18pt}
\setlength{\abovedisplayshortskip}{10pt}
\setlength{\belowdisplayshortskip}{10pt}
\stageheading{Worked example}''')
w=w.replace('\\Needspace{6\\baselineskip}\n\\task{Task 2', '\\clearpage\n\\task{Task 2')
w=w.replace('\\textbf{\\underline{2. Expectation', '\\par\\vspace{4mm}\n\\textbf{\\underline{2. Expectation')
w=w.replace('\\textbf{Checks.}', '\\par\\vspace{4mm}\n\\textbf{Checks.}')
w=w.replace('\\ColumnPair{', '\\par\\vspace{4mm}\n\\ColumnPair{')
w+='\\par\\clearpage\n\\endgroup\n\n'
g=s[b:c]
g=re.sub(r'\\vspace\{-[^}]+\}', '',g)
g=g.replace('\\newcommand{\\subtaskheading}',r'''% Empty neutral boxes; centered on the math axis for inline equations.
\newcommand{\writebox}[2]{\tikz[baseline=-.5ex]{%
  \node[draw=black!30,fill=black!3,line width=.3pt,
    inner sep=0pt,outer sep=0pt,minimum width=#1,minimum height=#2] {};}}
\renewcommand{\calcblank}{\writebox{1.05cm}{6.5mm}}
\renewcommand{\shortblank}{\writebox{.58cm}{5.5mm}}
\newcommand{\fractionblank}{\writebox{.8cm}{7mm}}
\newcommand{\subtaskheading}''')
g=g.replace('{8pt}', '{5pt}').replace('{6pt}', '{4pt}')
g=re.sub(r'\\\\\[(?:5|8|9|10|12)pt\]',r'\\\\[3pt]',g)
g=re.sub(r'\\Needspace\{(?:19|13|18|22|14|11)\\baselineskip\}', '',g)
g=g.replace('\\task{Task 2', '\\clearpage\n\\task{Task 2')
g=re.sub(r'\\underline\{\\hspace\{([^}]+)\}\}',r'\\writebox{\1}{6.5mm}',g)
# Fractions in interval endpoints need full-height handwriting space.
g=g.replace('p\\in(\\shortblank,1]', 'p\\in(\\fractionblank,1]')
g=g.replace('p\\in[0,\\shortblank)', 'p\\in[0,\\fractionblank)')
g=g.replace('\\responseline', '\\par\\noindent\\writebox{\\dimexpr\\linewidth-.3pt\\relax}{9mm}\\par')
# Keep verbal responses together on full-width lines.
g=g.replace("weekend for the chosen option. Let $E$ be", "weekend for the chosen option.\\par Let $E$ be")
g=g.replace('and $E^c$ be\n', '\\par and $E^c$ be\n')
# Combine adjacent algebraic links while preserving every intermediate step.
g=g.replace('\\\\[3pt]\n&\\iff p>\\calcblank\\\\[3pt]\n&\\iff p\\in', '\\iff p>\\fractionblank\\\\[3pt]\n&\\iff p\\in')
g=g.replace('\\\\[3pt]\n&\\iff\\calcblank p=24', '\\iff\\calcblank p=24')
g=g.replace('\\\\[3pt]\n&\\iff\\calcblank p=54', '\\iff\\calcblank p=54')
# The event names have room for short verbal phrases.
g=g.replace('\\writebox{3.4cm}{6.5mm}', '\\writebox{4cm}{6.5mm}')
g=g.replace("weekend for the chosen option.\\par Let", "weekend for the chosen option. Let")
g=g.replace('\\par and $E^c$', 'and $E^c$')
g=g.replace('\\setlength{\\abovedisplayskip}', '\\setlength{\\parskip}{1pt}\n\\setlength{\\jot}{1pt}\n\\setlength{\\abovedisplayskip}',1)
# Place equivalent formulas on the same line, retaining the full derivation.
g=g.replace('&=72p-24(1-p)\\\\[3pt]\n&=-24+', '&=72p-24(1-p)=-24+')
g=g.replace('&=\\calcblank p-54(1-p)\\\\[3pt]\n&=-54+', '&=\\calcblank p-54(1-p)=-54+')
g=g.replace('\\iff p>\\fractionblank\\\\[3pt]\n&\\iff p\\in', '\\\\[3pt]\n&\\iff p>\\fractionblank\\iff p\\in')
g=g.replace('\\calcblank p<24\\\\[3pt]\n&\\iff p\\in', '\\calcblank p<24\\iff p\\in')
g=g.replace('\\calcblank p<54\\\\[3pt]\n&\\iff p\\in', '\\calcblank p<54\\iff p\\in')
g=g.replace('}{7}\\\\[3pt]\n&=\\calcblank\\approx', '}{7}=\\calcblank\\approx')
# Box heights provide the writing clearance; ordinary aligned-row glue separates them.
g=g.replace('\\\\[3pt]', '\\\\')
g=g.replace('\\end{aligned}\n\\]\n\\[\n\\begin{aligned}\n', '\\\\[4pt]')
g=g.replace('\\writebox{4cm}{6.5mm} over many', '\\writebox{3.3cm}{6.5mm} over many')
g=g.replace('\\writebox{3cm}{6.5mm}', '\\writebox{2.5cm}{6.5mm}')
g=g.replace('}{9mm}', '}{7mm}')
g=g.replace('\\calcblank p', '\\calcblank\\,p').replace('\\calcblank X', '\\calcblank\\,X')
g=g.replace('\\addvspace{4pt}', '\\addvspace{2pt}').replace('\\nopagebreak[4]\\smallskip', '\\nopagebreak[4]')
g=g.replace('displayskip}{3pt}', 'displayskip}{2pt}').replace('displayshortskip}{4pt}', 'displayshortskip}{2pt}')
g=g.replace('\\\\[4pt]', '\\\\[2pt]')
g=g.replace('(gain/loss) of USD $\\calcblank$ per weekend.', '(gain/loss) of\\par USD $\\calcblank$ per weekend.')
g=g.replace('. At break-even, the long-run average is', '.\\par At break-even, the long-run average is')
# Endpoints are short corresponding calculations in a fresh paired row.
start=g.index('\\[\n\\begin{aligned}\n\\mathbb E[Y_1](0)')
end=g.index('At the roots,',start)
g=g[:start]+r'''\ColumnPair{
\(\mathbb E[Y_1](0)=\calcblank,\quad\mathbb E[Y_1](1)=\calcblank\)
}{
\(\mathbb E[Y_2](0)=\calcblank,\quad\mathbb E[Y_2](1)=\calcblank\quad\text{(USD).}\)
}
'''+g[end:]
g=g.replace('\\setlength{\\abovedisplayskip}{5pt}', '\\setlength{\\abovedisplayskip}{3pt}')
g=g.replace('\\setlength{\\belowdisplayskip}{5pt}', '\\setlength{\\belowdisplayskip}{3pt}')
g=g.replace('\\endgroup', '\\par\\clearpage\n\\endgroup')
p.write_text(s[:a]+w+g+s[c:],encoding='utf-8')
