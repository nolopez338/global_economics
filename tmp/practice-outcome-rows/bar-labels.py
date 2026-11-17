from pathlib import Path
p=Path('book2026-2027/grade10/term_2/1-practice_activities/G10_T2_L1_C2_practice_activity.tex');s=p.read_text(encoding='utf-8')
s=s.replace(r'\pgfplotsset{execute at begin axis={\tikzset{gtenbar y marker/.append style={rotate=60}}\pgfplotsset{yticklabel style={rotate=0}}}}',r'''\ExplSyntaxOn
\patchcmd{\__gtenbar_draw:nnnn}
  {font=\exp_not:N \small,}
  {font=\exp_not:N \small,rotate=60,}
  {}{\errmessage{Local~PMF~label~layout~failed}}
\ExplSyntaxOff''')
p.write_text(s,encoding='utf-8')
