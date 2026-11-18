from pathlib import Path
p=Path('book2026-2027/grade10/term_2/3-slides/G10_T2_L1_C2_slides.tex');s=p.read_text(encoding='utf-8')
macro=r'\renewcommand{\TickLabel}[1]{\ifnum#1=0\H<3>{Quantity}{#1}\else\ifnum#1=2\H<4>{Quantity}{#1}\else\H<5>{Quantity}{#1}\fi\fi}'
s=s.replace(macro,r'\let\TickLabel\PMFTickLabel')
s=s.replace(r'\newcommand{\TickLabel}[1]{#1}',r'\newcommand{\TickLabel}[1]{#1}'+'\n'+macro.replace(r'\renewcommand{\TickLabel}',r'\newcommand{\PMFTickLabel}'))
p.write_text(s,encoding='utf-8')
p=Path('tmp/pdfs/c2-storyboard');(p/'portable/lesson.tex').write_text(s,encoding='utf-8');(p/'off/lesson.tex').write_text(s.replace('% \\GTenHighlightsfalse % Uncomment','\\GTenHighlightsfalse % Uncomment'),encoding='utf-8')
# Practice toggle-off copy is compiled from original working directory, with an absolute preamble root added.
s=Path('book2026-2027/grade10/term_2/1-practice_activities/G10_T2_L1_C2_practice_activity.tex').read_text(encoding='utf-8')
s=s.replace('% \\GTenHighlightsfalse % Uncomment','\\GTenHighlightsfalse % Uncomment')
(p/'practice-off.tex').write_text(s,encoding='utf-8')
