from pathlib import Path
p=Path('book2026-2027/grade10/term_2/1-practice_activities/G10_T2_L1_C2_practice_activity.tex'); s=p.read_text(encoding='utf-8')
for key in ['prize','maintenance','calls']:
 a=s.index('\\stage{'+key+'}{1}'); b=s.index('\\stage{'+key+'}{2}',a)
 part=s[a:b].replace(r'\GTenPMFGraph[',r'''% Rotate dense bar labels locally; preserve all PMF data and spacing.
\pgfplotsset{execute at begin axis={\tikzset{gtenbar y marker/.append style={rotate=60}}\pgfplotsset{yticklabel style={rotate=0}}}}
\GTenPMFGraph[''',1)
 s=s[:a]+part+s[b:]
# Ragged-right explanatory notes avoid stretched spaces within the new narrow columns.
s=s.replace(r'\par\small For each integer',r'\par\small\raggedright For each integer').replace(r'\par\small Label the distinct',r'\par\small\raggedright Label the distinct')
p.write_text(s,encoding='utf-8')
