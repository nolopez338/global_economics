from pathlib import Path
p=Path('book2026-2027/grade11/term_2/3-slides/G11_T2_L1_C2_slides.tex')
s=p.read_text(encoding='utf8')
s=s.replace(r'\fontsize{10.5}{12}\selectfont',r'\fontsize{10}{10.8}\selectfont')
s=s.replace(r'\renewcommand{\arraystretch}{1.02}',r'\renewcommand{\arraystretch}{1.0}\setlength{\aboverulesep}{1pt}\setlength{\belowrulesep}{1pt}\tikzset{ge marker/.append style={inner xsep=.4mm,inner ysep=.1mm}}')
s=s.replace(r'\\[2pt]',r'\\[1pt]')
s=s.replace(r'\fontsize{10}{11.4}',r'\fontsize{10}{10.6}')
s=s.replace(r'\renewcommand{\arraystretch}{1.0}\tikzset',r'\renewcommand{\arraystretch}{1.0}\setlength{\aboverulesep}{.7pt}\setlength{\belowrulesep}{.7pt}\tikzset')
s=s.replace(r'\begin{column}{.59\textwidth}',r'\begin{column}{.63\textwidth}').replace(r'\begin{column}{.38\textwidth}',r'\begin{column}{.35\textwidth}')
s=s.replace(r'p{.18\linewidth}p{.36\linewidth}',r'p{.22\linewidth}p{.37\linewidth}')
s=s.replace('All cycling trips in the specified month; mean duration (minutes)',"Month's mean trip duration (minutes)")
s=s.replace(r'[1.45cm]',r'[1.35cm]').replace(r'[.55cm]',r'[.45cm]').replace(r'{.75cm}',r'{.65cm}')
s=s.replace(r'\InfoTables\medskip\small',r'\InfoTables\smallskip\fontsize{10.5}{11.5}\selectfont\setlength{\parskip}{0pt}\setlength{\aboverulesep}{1pt}\setlength{\belowrulesep}{1pt}')
s=s.replace(r'\begin{frame}[t]{Task 3 -- Assess',r'\begin{frame}[t]{Task 3 -- Assess')
# Task 3 reserve enough vertical space and use a readable compact evidence table.
s=s.replace(r'\small \At{8}{Coverage}',r'\fontsize{10.5}{11.5}\selectfont\setlength{\parskip}{2pt} \At{8}{Coverage}')
s=s.replace(r'\begin{overlayarea}{\linewidth}{1.1cm}',r'\begin{overlayarea}{\linewidth}{.8cm}')
s=s.replace(r'\begin{overlayarea}{\linewidth}{1.5cm}',r'\begin{overlayarea}{\linewidth}{1.6cm}')
# Input highlights persist between Task 2 frames after first use.
start=s.index(r'\begin{frame}[t]{Task 2 -- Build')
end=s.index(r'\section{Coverage evidence}',start)
part=s[start:end]
for step in [5,7,15]:
 import re
 part=re.sub(r'\\csname Input'+str(step)+r'\\endcsname\{\d+\}',r'\\csname Input'+str(step)+r'\\endcsname{1}',part)
part=part.replace(r'\csname Input9\endcsname{5}',r'\csname Input9\endcsname{6}')
s=s[:start]+part+s[end:]
s=s.replace(r'\csname Input7\endcsname{5}',r'\csname Input7\endcsname{4}').replace(r'\csname Input15\endcsname{5}',r'\csname Input15\endcsname{4}')
p.write_text(s,encoding='utf8')
Path('tmp/c2_slides_rebuild/lesson.tex').write_text(s,encoding='utf8')
Path('tmp/c2_slides_rebuild/handout.tex').write_text(s.replace('[12pt,aspectratio=169]','[handout,12pt,aspectratio=169]'),encoding='utf8')
