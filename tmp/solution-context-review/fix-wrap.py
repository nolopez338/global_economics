from pathlib import Path
p=Path('book2026-2027/grade11/term_2/4-learning_evidences/G11_T2_L1_C1C2_exam_solution.tex')
s=p.read_text(encoding='utf-8')
s=s.replace(r'\PP{October electricity bills}',r'\PP{October electricity} \PP{bills}')
s='\n'.join(r'\begingroup\raggedright '+line+r'\par\endgroup' if line.startswith('The unknown $') else line for line in s.split('\n'))
p.write_text(s,encoding='utf-8')
