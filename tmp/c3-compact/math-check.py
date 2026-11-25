from pathlib import Path
import re
old=Path('tmp/c3-compact/original.tex').read_text(); new=Path('book2026-2027/grade11/term_2/2-class_activities/G11_T2_L1_C3_classroom_activity.tex').read_text()
norm=lambda s:re.sub(r'\\guidedresponsebox(?:\[[^]]*\])?\{[^}]*\}',r'GUIDEDBOX',s)
print('Mathematics unchanged except response-box dimensions:',re.findall(r'(?<!\\)\$(.*?)(?<!\\)\$',norm(old),re.S)==re.findall(r'(?<!\\)\$(.*?)(?<!\\)\$',norm(new),re.S))
for d in ['.','book2026-2027','book2026-2027/grade11','book2026-2027/grade11/term_2','book2026-2027/grade11/term_2/2-class_activities']:
    p=Path(d)/'AGENTS.md'
    if p.exists(): print(str(p),p.read_text())
