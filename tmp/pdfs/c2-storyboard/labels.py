from pathlib import Path
p=Path('book2026-2027/grade10/term_2/3-slides/G10_T2_L1_C2_slides.tex');s=p.read_text(encoding='utf-8')
s=s.replace('(-1.9,-.90) rectangle (5.65,5.15)','(-2.2,-.90) rectangle (5.65,5.15)')
s=s.replace(r'\node[anchor=south west,font=\small] at (-1,{\base+2.22}){$\label$};',r'\node[rotate=90,font=\small] at (-1.9,{\base+1.1}){$\label$};')
s=s.replace(r'\textcolor{cTwoGuideColor}{Dashed: translated masses}',r'\textcolor{GEInk}{Dashed: translated masses}')
p.write_text(s,encoding='utf-8')
q=Path('tmp/pdfs/c2-storyboard');(q/'portable/lesson.tex').write_text(s,encoding='utf-8');(q/'off/lesson.tex').write_text(s.replace('% \\GTenHighlightsfalse % Uncomment','\\GTenHighlightsfalse % Uncomment'),encoding='utf-8')
