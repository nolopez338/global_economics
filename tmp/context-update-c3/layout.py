from pathlib import Path
p=Path('book2026-2027/grade10/term_2/2-class_activities/G10_T2_L1_C3_classroom_activity.tex')
s=p.read_text().replace(r'\task{Task 2 --- Analyse each expected value separately.}{}',r'\Needspace{6\baselineskip}'+'\n'+r'\task{Task 2 --- Analyse each expected value separately.}{}',1)
s=s.replace(r'\problemtitle{5}{Freelance video editing equipment}',r'\Needspace{12\baselineskip}'+'\n'+r'\problemtitle{5}{Freelance video editing equipment}')
p.write_text(s)
