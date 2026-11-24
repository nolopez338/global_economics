from pathlib import Path
p=Path('book2026-2027/grade10/term_2/3-slides/G10_T2_L1_C3_slides.tex')
s=p.read_text().replace(r'font=\small\bfseries] (tasktitle)',r'font=\footnotesize\bfseries] (tasktitle)')
s=s.replace(r'\newcommand{\Ask}[1]{\textbf{#1}\par\medskip}',r'\newcommand{\Ask}[1]{\textbf{#1}\par\smallskip}')
p.write_text(s)
