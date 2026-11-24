from pathlib import Path
p=Path('book2026-2027/grade10/term_2/3-slides/G10_T2_L1_C3_slides.tex')
s=p.read_text().replace(r'\newcommand{\ActiveHierarchy}{%',r'\newcommand{\ActiveHierarchy}{%'+ '\n  \\begingroup\\setlength{\\parskip}{0pt}')
s=s.replace('  \\fi}\n\n\\setbeamertemplate{frametitle}', '  \\fi\\endgroup}\n\n\\setbeamertemplate{frametitle}')
p.write_text(s)
