from pathlib import Path
import re
p=Path('book2026-2027/grade10/term_2/2-class_activities/G10_T2_L1_C3_classroom_activity.tex')
s=Path('tmp/c3-layout-final-20261124/baseline.tex').read_text()
a=s.index(r'\stageheading{Worked example}')
b=s.index(r'\stageheading{Guided Example}')
c=s.index(r'\stageheading{Independent Practice}')
w=s[a:b]
w=re.sub(r'\\vspace\{-\d+mm\}',r'\\vspace{2mm}',w)
w=w.replace(r'\stageheading{Worked example}',r'''\begingroup
% Consistent positive separation, confined to the worked example.
\NewDocumentCommand{\WorkedColumnPair}{+m +m}{\par\noindent\begin{minipage}[t]{.49\linewidth}\vspace{0pt}\raggedright #1\end{minipage}\hfill\begin{minipage}[t]{.49\linewidth}\vspace{0pt}\raggedright #2\end{minipage}\par}
\RenewDocumentCommand{\ColumnPair}{+m +m}{%
  \par\addvspace{3mm}\WorkedColumnPair{#1}{#2}\par\addvspace{3mm}}
\stageheading{Worked example}''')
w=w.replace(r'\Needspace{6\baselineskip}',r'\newpage')
w+= '\\par\\clearpage\n\\endgroup\n\n'
g=s[b:c]
g=re.sub(r'\\vspace\{-\d+mm\}',r'\\vspace{2pt}',g)
g=g.replace(r'\setlength{\abovedisplayskip}{8pt}',r'\setlength{\abovedisplayskip}{5pt}')
g=g.replace(r'\setlength{\belowdisplayskip}{8pt}',r'\setlength{\belowdisplayskip}{5pt}')
g=g.replace(r'\setlength{\abovedisplayshortskip}{6pt}',r'\setlength{\abovedisplayshortskip}{4pt}')
g=g.replace(r'\setlength{\belowdisplayshortskip}{6pt}',r'\setlength{\belowdisplayshortskip}{4pt}')
helpers=r'''% Empty neutral writing areas; all definitions end with this example.
\newcommand{\writingbox}[2][6mm]{%
  \tikz[baseline=(answer.base)]{\node[draw=black!25,fill=black!3,
    line width=.3pt,inner sep=0pt,outer sep=.3pt,
    minimum width=#2,minimum height=#1] (answer) {\phantom{0}};}}
\renewcommand{\calcblank}{\writingbox[7mm]{11mm}}
\renewcommand{\shortblank}{\writingbox{7mm}}
\newcommand{\wordblank}[1]{\writingbox[7mm]{#1}}
'''
g=g.replace(r'\setlength{\abovedisplayskip}',helpers+r'\setlength{\abovedisplayskip}',1)
g=re.sub(r'\\underline\{\\hspace\{([^}]+)\}\}',r'\\wordblank{\1}',g)
g=g.replace(r'\responseline',r'\par\noindent\writingbox[10mm]{\linewidth}\par')
# Fraction numerators and denominators need their own writing clearance.
g=g.replace(r'\tfrac{\shortblank}{7}',r'\frac{\shortblank}{7}')
# PMF and CDF get separate, fresh paired rows to preserve readable case spacing.
start=g.index(r'\ColumnPair{'+'\n'+r'\textbf{$Y_1$ --- Complete PMF')
end=g.index(r'\Needspace{13\baselineskip}',start)
old=g[start:end]
parts=re.findall(r'\\begin\{gathered\}(.*?)\\end\{cases\}',old,re.S)
# Reuse every distribution verbatim, only moving its display into aligned rows.
dist=[r'\begin{gathered}'+x+r'\end{cases}' for x in parts]
g=g[:start]+r'''\ColumnPair{
\textbf{$Y_1$ --- Complete PMF and ordered CDF.}
\[ '''+dist[0]+r''' \quad '''+dist[1]+r''' \]
}{
\textbf{$Y_2$ --- Complete PMF and ordered CDF.}
\[ '''+dist[2]+r''' \quad '''+dist[3]+r''' \]
}
'''+g[end:]
# Task boundary is the deliberate page 4--5 break.
g=g.replace(r'\Needspace{18\baselineskip}',r'\newpage')
# The boxes supply vertical handwriting clearance; row gaps are additional space.
g=re.sub(r'\\\\\[(?:5|8|9|10|12)pt\]',r'\\\\[2pt]',g)
g=re.sub(r'\\Needspace\{(?:19|13|22|14|11)\\baselineskip\}', '',g)
# Keep the final interpretation together; reserve its response area.
g=g.replace(r'\textbf{Endpoint and root calculations.}',r'\Needspace{8\baselineskip}'+'\n'+r'\textbf{Endpoint and root calculations.}')
g=g.replace(r'\addvspace{4pt}',r'\addvspace{2pt}')
g=g.replace(r'\smallskip}',r'\vspace{2pt}}')
g=g.replace(r'\vspace{2pt}', '')
# Preserve all intermediate calculations while sharing lines where they fit.
for x,y in [
 (r'&=\frac{144-\calcblank}{7}\\[2pt]'+'\n'+r'&=\calcblank',r'&=\frac{144-\calcblank}{7}=\calcblank'),
 (r'&=\frac{252-\calcblank}{7}\\[2pt]'+'\n'+r'&=\calcblank',r'&=\frac{252-\calcblank}{7}=\calcblank'),
 (r'&=72p-24(1-p)\\[2pt]'+'\n'+r'&=-24+',r'&=72p-24(1-p)=-24+'),
 (r'&=\calcblank p-54(1-p)\\[2pt]'+'\n'+r'&=-54+',r'&=\calcblank p-54(1-p)=-54+'),
 (r'&\iff\calcblank p=24\\[2pt]'+'\n'+r'&\iff p=',r'&\iff\calcblank p=24\iff p='),
 (r'&\iff\calcblank p=54\\[2pt]'+'\n'+r'&\iff p=',r'&\iff\calcblank p=54\iff p='),
 (r'&\iff p>\calcblank\\[2pt]'+'\n'+r'&\iff p\in',r'&\iff p>\calcblank\iff p\in'),
]: g=g.replace(x,y)
g=g.replace(r'\writingbox[10mm]{\linewidth}',r'\writingbox[10mm]{\dimexpr\linewidth-1pt\relax}')
g=g.replace(r'\writingbox[7mm]{11mm}',r'\writingbox[6mm]{11mm}')
g=g.replace(r'\abovedisplayskip}{5pt}',r'\abovedisplayskip}{3pt}')
g=g.replace(r'\belowdisplayskip}{5pt}',r'\belowdisplayskip}{3pt}')
g=g.replace(r'\abovedisplayshortskip}{4pt}',r'\abovedisplayshortskip}{3pt}')
g=g.replace(r'\belowdisplayshortskip}{4pt}',r'\belowdisplayshortskip}{3pt}')
g=g.replace(r'\setlength{\abovedisplayskip}',r'\setlength{\parskip}{0pt}\setlength{\jot}{0pt}'+'\n'+r'\setlength{\abovedisplayskip}',1)
g=g.replace(r'\quad \begin{gathered}F_',r'\; \begin{gathered}F_')
g=g.replace(r'\\[2pt]',r'\\[1pt]')
for value in ('24','54'):
    g=g.replace(r'\mathbb E[Y_'+('1' if value=='24' else '2')+r']<0&\iff\calcblank p<'+value+r'\\[1pt]'+'\n'+r'&\iff p\in',r'\mathbb E[Y_'+('1' if value=='24' else '2')+r']<0&\iff\calcblank p<'+value+r'\iff p\in')
g=g.replace(r'\end{aligned}'+'\n'+r'\]'+'\n'+r'\['+'\n'+r'\begin{aligned}',r'\\[3pt]')
# Initial exact expectations and break-even roots are fraction-sized answers.
g=g.replace(r'=\calcblank\approx',r'=\writingbox[8mm]{11mm}\approx')
g=g.replace(r'\shortblank}=\calcblank',r'\shortblank}=\writingbox[8mm]{11mm}')
# Smaller numerical blanks in sign intervals still accept a handwritten fraction.
g=g.replace(r'\shortblank,1]',r'\writingbox[8mm]{9mm},1]')
g=g.replace(r'[0,\shortblank)',r'[0,\writingbox[8mm]{9mm})')
explanation=r'''Dividing by the \wordblank{1.5cm} (positive/negative)
coefficient \wordblank{1.8cm} (keeps/reverses) both inequalities.'''
g=g.replace(explanation+'\n}', '}\n'+explanation+'\n')
g=g.replace(r'\mathbb E[Y_1](1)&=\calcblank,\\[1pt]',r'\mathbb E[Y_1](1)&=\calcblank,\quad')
g=g.replace(r'\writingbox[10mm]{\dimexpr\linewidth-1pt\relax}',r'\writingbox[7mm]{\dimexpr\linewidth-1pt\relax}')
g=g.replace(r'p>\calcblank',r'p>\writingbox[8mm]{11mm}')
g=g.replace(r'\subtaskheading{3}{Graphs}',r'\par\vspace{3pt}\subtaskheading{3}{Graphs}')
g=g.replace(r'\renewcommand{\shortblank}{\writingbox{7mm}}',r'\renewcommand{\shortblank}{\writingbox{7.5mm}}')
g=g.replace(r'\setlength{\jot}{0pt}',r'\setlength{\jot}{0pt}\setlength{\arraycolsep}{2.5pt}')
g=g.replace(r'\calcblank p',r'\calcblank\,p').replace(r'\calcblank X',r'\calcblank\,X')
g=g.replace(r'\calcblank(\calcblank)',r'\calcblank(\writingbox[8mm]{11mm})')
# Fraction-valued probability responses retain more vertical writing room.
ga,gb=g.split(r'\newpage',1)
ga=ga.replace(r'\calcblank',r'\probblank')
# Keep the transformation coefficients as ordinary numerical boxes.
cut=ga.index(r'\subtaskheading{2}')
ga=ga[:cut].replace(r'\probblank',r'\calcblank')+ga[cut:]
ga=ga.replace(r'\newcommand{\wordblank}',r'\newcommand{\probblank}{\writingbox[8mm]{11mm}}'+'\n'+r'\newcommand{\wordblank}')
g=ga+r'\newpage'+gb
g=g.replace(r'\; \begin{gathered}F_',r'\hspace{1pt}\begin{gathered}F_')
endpoint_start=g.index(r'\[' ,g.index(r'\textbf{Endpoint and root calculations.}'))
endpoint_end=g.index(r'\]',endpoint_start)+2
g=g[:endpoint_start]+r'''\[
\mathbb E[Y_1](0)=\calcblank,\quad \mathbb E[Y_1](1)=\calcblank,\quad
\mathbb E[Y_2](0)=\calcblank,\quad \mathbb E[Y_2](1)=\calcblank\quad\text{(USD).}
\]'''+g[endpoint_end:]
w=w.replace(r'\addvspace{3mm}',r'\addvspace{4mm}')
g=g.replace(r'\endgroup',r'\par\clearpage'+'\n'+r'\endgroup')
p.write_text(s[:a]+w+g+s[c:])
