from pathlib import Path
p=Path('book2026-2027/grade11/term_2/4-learning_evidences/G11_T2_L1_C1C2_exam_solution.tex')
s=p.read_text(encoding='utf-8')
a=s.index(r'\worked{C2 Task 1 \score{1}}{sol:p2c2a}')
x=s.index(r'\keytable{p{.12\linewidth}p{.24\linewidth}K}',a)
s=s[:x]+r'\clearpage'+'\n'+s[x:]
p.write_text(s,encoding='utf-8')
