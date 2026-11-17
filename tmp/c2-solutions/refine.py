from pathlib import Path
p=Path('book2026-2027/grade10/term_2/2-class_activities/G10_T2_L1_C2_classroom_activity.tex')
s=p.read_text(); h,b=s.split('\n\\ifprintsolutions\n',1)
b=b.replace(r'\cTwoOutcome{On time/early: $t\leq0$}',r'\cTwoOutcome{On time}\newline\cTwoOutcome{or early:}\newline\cTwoOutcome{$t\leq0$}')
b=b.replace(r'\cTwoOutcome{Grace: $0<t\leq5$}',r'\cTwoOutcome{Grace:}\newline\cTwoOutcome{$0<t\leq5$}')
b=b.replace('width=\\linewidth,\n        height=4.15cm,','width=\\dimexpr\\linewidth-6pt\\relax,\n        height=4.15cm,',1)
p.write_text(h+'\n\\ifprintsolutions\n'+b)
