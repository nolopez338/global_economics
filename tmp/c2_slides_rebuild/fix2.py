from pathlib import Path
p=Path('book2026-2027/grade11/term_2/3-slides/G11_T2_L1_C2_slides.tex')
s=p.read_text(encoding='utf8').replace(r'\newcommand{\At}[3]{\alt<#1->{\GEHighlight{#2}{#3}}{\GEPlain{#3}}}',r'\newcommand{\At}[3]{\ifnum#1=0\relax\GEPlain{#3}\else\alt<#1->{\GEHighlight{#2}{#3}}{\GEPlain{#3}}\fi}')
s=s.replace('\\endcsname{99}','\\endcsname{0}')
p.write_text(s,encoding='utf8')
Path('tmp/c2_slides_rebuild/lesson.tex').write_text(s,encoding='utf8')
