from pathlib import Path
p=Path('book2026-2027/grade10/term_2/1-practice_activities/G10_T2_L1_C1_practice_activity.tex')
s=p.read_text(encoding='utf-8')
start=s.index(r'\newcommand{\GTenDenseProbabilityGraph}')
end=s.index(r'\newcommand{\GTenSolutionOutcomes}',start)
s=s[:start]+r'''\ExplSyntaxOn
\newcommand{\GTenDenseProbabilityGraph}[1]{%
  \group_begin:
  \pgfplotsset{every~axis~post/.append~style={
    execute~at~begin~axis={\tikzset{gtenbar~y~marker/.append~style={rotate=90}}},
    yticklabel~style={rotate=-90}}}
  #1\group_end:}
\ExplSyntaxOff
'''+s[end:]
Path('tmp/c1_layout/refined.tex').write_text(s,encoding='utf-8')
Path('tmp/c1_layout/refined-disabled.tex').write_text(s.replace(r'% \GTenHighlightsfalse',r'\GTenHighlightsfalse'),encoding='utf-8')
