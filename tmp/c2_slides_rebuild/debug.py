from pathlib import Path
p=Path('book2026-2027/grade11/term_2/3-slides/G11_T2_L1_C2_slides.tex')
s=p.read_text(encoding='utf8').replace(r'\CtwoCoverage{Cover}}}',r'\CtwoCoverage{Cover}}').replace(r'\CtwoCoverage{Miss}}}',r'\CtwoCoverage{Miss}}')
p.write_text(s,encoding='utf8')
# Fast draft renderer has the same intended padding and avoids TikZ work while diagnosing layout.
a=s.index(r'\newcommand{\GEHighlight}[2]')
b=s.index(r'\makeatother',a)
fast=s[:a]+r'\newcommand{\GEHighlight}[2]{\begingroup\setlength{\fboxsep}{.6mm}\ifmmode\fbox{\ensuremath{#2}}\else\fbox{#2}\fi\endgroup}'+'\n'+s[b:]
fast=fast.replace('[12pt,aspectratio=169]','[handout,12pt,aspectratio=169]')
Path('tmp/c2_slides_rebuild/fast.tex').write_text(fast,encoding='utf8')
Path('tmp/c2_slides_rebuild/lesson.tex').write_text(s,encoding='utf8')
