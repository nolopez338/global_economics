from pathlib import Path
import re
p=Path('book2026-2027/grade10/term_2/3-slides/G10_T2_L1_C2_slides.tex');s=p.read_text(encoding='utf-8')
# Visible thin separators expose reserved blank rows without changing row geometry.
s=s.replace('\\\\\n\\Blank', '\\\\\\specialrule{.2pt}{0pt}{0pt}\n\\Blank')
p.write_text(s,encoding='utf-8')
q=Path('tmp/pdfs/c2-storyboard');(q/'portable/lesson.tex').write_text(s,encoding='utf-8');(q/'off/lesson.tex').write_text(s.replace('% \\GTenHighlightsfalse % Uncomment','\\GTenHighlightsfalse % Uncomment'),encoding='utf-8')
