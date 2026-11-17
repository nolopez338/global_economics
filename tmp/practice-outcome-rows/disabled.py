from pathlib import Path
p=Path('book2026-2027/grade10/term_2/1-practice_activities/G10_T2_L1_C2_practice_activity.tex')
s=p.read_text(encoding='utf-8').replace(r'% \GTenHighlightsfalse % Uncomment',r'\GTenHighlightsfalse % Uncomment',1)
Path('tmp/practice-outcome-rows/disabled.tex').write_text(s,encoding='utf-8')
