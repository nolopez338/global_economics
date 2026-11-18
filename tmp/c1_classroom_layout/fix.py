from pathlib import Path
import re
p=Path('book2026-2027/grade10/term_2/2-class_activities/G10_T2_L1_C1_classroom_activity.tex')
s=p.read_text(encoding='utf-8'); a,b=s.split('\\ifprintsolutions\n\\clearpage',1)
b=re.sub(r'\$\\mathrm\{([A-Z]+)\}\$',r'\1',b)
# Short semantic strokes permit native cell wrapping.
b=re.sub(r'\\GTenHLOutcome\{([A-Za-z ]+)\}',lambda m:' '.join('\\GTenHLOutcome{'+w+'}' for w in m[1].split()),b)
p.write_text(a+'\\ifprintsolutions\n\\clearpage'+b,encoding='utf-8',newline='\n')
