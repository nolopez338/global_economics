from pathlib import Path
s=Path('book2026-2027/grade10/term_2/1-practice_activities/G10_T2_L1_C2_practice_activity.tex').read_text(encoding='utf-8')
a=s.index('\\stage{prize}{1}');g=s.index('% Rotate dense',a);e=s.index(r'\end{minipage}',g)
Path('tmp/practice-outcome-rows/graph-check.tex').write_text(s[:s.index(r'\begin{document}')]+r'\begin{document}\begin{minipage}{.40\linewidth}'+s[g:e]+r'\end{minipage}\end{document}',encoding='utf-8')
