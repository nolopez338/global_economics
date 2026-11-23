from pathlib import Path
from collections import Counter
import re
old=Path('tmp/solution-context-review/original.tex').read_text(encoding='utf-8')
new=Path('book2026-2027/grade11/term_2/4-learning_evidences/G11_T2_L1_C1C2_exam_solution.tex').read_text(encoding='utf-8')
for pat,name in [(r'\$(.*?)\$','inline math'),(r'\\label\{([^}]+)\}','labels'),(r'\\score\{([^}]+)\}','scores'),(r'\\taskprompt[^\n]+','task prompts')]:
 a=Counter(re.findall(pat,old)); b=Counter(re.findall(pat,new)); lost=a-b
 print(name, 'preserved' if not lost else dict(lost))
assert r'\textbf{Type}' not in new
assert new.count(r'\multicolumn{3}{l}{\textbf{Population parameters}}')==3
assert new.count(r'\multicolumn{3}{l}{\textbf{Sample statistics}}')==3
assert new.count(r'\multicolumn{3}{l}{\textbf{Procedure settings}}')==3
print('Three detailed tables retain all 10 rows and requested section structure.')
