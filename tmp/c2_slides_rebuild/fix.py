from pathlib import Path
p=Path('book2026-2027/grade11/term_2/3-slides/G11_T2_L1_C2_slides.tex')
s=p.read_text(encoding='utf8')
s=s.replace(r'\small\setlength{\parskip}{0pt}\setlength{\tabcolsep}{3pt}\renewcommand{\arraystretch}{1.12}',r'\fontsize{10.5}{12}\selectfont\setlength{\parskip}{0pt}\setlength{\tabcolsep}{2pt}\renewcommand{\arraystretch}{1.02}')
s=s.replace(r'\\[6pt]',r'\\[2pt]')
# Legend's long concept fragments may wrap at spaces; preserve exact text and roles.
import re
for name in ['Confidence','Critical','SE','MoE','Endpoint','CI','Width','Significance','Coverage']:
 s=re.sub(r'\\Ctwo'+name+r'\{([^{}]* [^{}]*)\}',lambda m:' '.join('\\Ctwo'+name+'{'+word+'}' for word in m[1].split()),s)
# More room for count symbols; formulas have their own balanced space.
s=s.replace(r'p{.24\linewidth}>{\raggedright\arraybackslash}p{.28\linewidth}',r'p{.28\linewidth}>{\raggedright\arraybackslash}p{.30\linewidth}')
# Task 1 uses the same asymmetric pair on every overlay and every reference.
a=s.index(r'\newcommand{\InfoTables}')
b=s.index(r'\ExplSyntaxOn',a)
part=s[a:b]
part=part.replace(r'\begin{column}{.49\textwidth}',r'\begin{column}{.59\textwidth}',1)
pos=part.index(r'\begin{column}{.49\textwidth}')
part=part[:pos]+part[pos:].replace(r'\begin{column}{.49\textwidth}',r'\begin{column}{.38\textwidth}',1)
part=part.replace(r'p{.14\linewidth}p{.39\linewidth}',r'p{.18\linewidth}p{.36\linewidth}')
part=part.replace('Mean duration of all cycling trips in the month','All cycling trips in the specified month; mean duration (minutes)')
part=part.replace(r'\renewcommand{\arraystretch}{1.03}',r'\renewcommand{\arraystretch}{1.0}\tikzset{ge marker/.append style={inner xsep=.25mm,inner ysep=.1mm}}')
s=s[:a]+part+s[b:]
s=s.replace('[1.65cm]','[1.45cm]').replace('[.65cm]','[.55cm]').replace('{1.0cm}','{.75cm}')
s=s.replace(r'\CtwoEndpoint{U_i}}$',r'\CtwoEndpoint{U_i}$}')
# Complete problem data table needs a wider right column.
s=s.replace(r'\begin{column}{.60\textwidth}'+"Five subsequent",r'\begin{column}{.56\textwidth}'+"Five subsequent")
s=s.replace(r'\begin{column}{.37\textwidth}\begin{tabular}{@{}rrrr@{}}',r'\begin{column}{.42\textwidth}\begin{tabular}{@{}rrrr@{}}')
p.write_text(s,encoding='utf8')
Path('tmp/c2_slides_rebuild/lesson.tex').write_text(s,encoding='utf8')
