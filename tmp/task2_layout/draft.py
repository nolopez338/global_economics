from pathlib import Path
s=Path('book2026-2027/grade11/term_2/3-slides/G11_T2_L1_C2_slides.tex').read_text(encoding='utf-8')
body=s[s.index('% Task 2 uses one cumulative'):s.index(r'\section{Coverage evidence}')]
body=body.replace(r'\begin{frame}[t]{Task 2',r'\begin{frame}<22>[t]{Task 2')
Path('tmp/task2_layout/draft.tex').write_text(s[:s.index(r'\begin{document}')]+r'\begin{document}'+body+r'\end{document}',encoding='utf-8')
