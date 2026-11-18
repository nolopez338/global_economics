from pathlib import Path
p=Path('book2026-2027/grade11/term_2/3-slides/G11_T2_L1_C2_slides.tex')
s=p.read_text(encoding='utf8').replace(r'\begin{column}{.35\textwidth}',r'\begin{column}{.36\textwidth}')
s=s.replace(r'p{.19\linewidth}>{\raggedright\arraybackslash}p{.48\linewidth}',r'p{.23\linewidth}>{\raggedright\arraybackslash}p{.46\linewidth}')
s=s.replace(r'\end{minipage}'+ '\n'+r'\InfoTables',r'\end{minipage}\par\vspace{-1.5mm}'+ '\n'+r'\InfoTables')
s=s.replace(r'\begin{minipage}[t][1.2cm][t]{\linewidth}',r'\begin{minipage}[t][1.2cm][t]{\linewidth}\raggedright')
s=s.replace(r'\begin{minipage}[t][.45cm][t]{\linewidth}',r'\begin{minipage}[t][.45cm][t]{\linewidth}\raggedright')
p.write_text(s,encoding='utf8')
Path('tmp/c2_slides_rebuild/next.tex').write_text(s,encoding='utf8')
