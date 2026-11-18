from pathlib import Path
import re
p=Path('book2026-2027/grade11/term_2/3-slides/G11_T2_L1_C2_slides.tex')
s=p.read_text(encoding='utf8')
def edit(m):
 f=m[0]
 if '{Task 2 -- Point estimate}' in f:
  for step in [7,15]:f=f.replace('\\csname Input'+str(step)+r'\endcsname{4}','\\csname Input'+str(step)+r'\endcsname{0}')
 if '{Task 2 -- Margin of error}' in f:
  f=re.sub(r'\\(R|At)\{([4-7])\}',lambda x:'\\'+x[1]+'{'+str(int(x[2])-2)+'}',f)
  f=f.replace(r'\Words{4}',r'\Words{2}')
  for step in [7,15]:f=f.replace('\\csname Input'+str(step)+r'\endcsname{4}','\\csname Input'+str(step)+r'\endcsname{2}')
 if '{Task 2 -- Full width}' in f:f=f.replace(r'\csname Input9\endcsname{6}',r'\csname Input9\endcsname{0}')
 if '{Task 2 -- Interpret the interval}' in f:f=f.replace(r'\csname Input9\endcsname{6}',r'\csname Input9\endcsname{2}')
 if '{Task 3 -- Assess' in f:
  f=f.replace(r'$L$ (min)&$U$ (min)',r'$\At{3}{Endpoint}{L}$ (min)&$\At{3}{Endpoint}{U}$ (min)')
 return f
s=re.sub(r'\\begin\{frame\}.*?\\end\{frame\}',edit,s,flags=re.S)
p.write_text(s,encoding='utf8')
Path('tmp/c2_slides_rebuild/lesson.tex').write_text(s,encoding='utf8')
Path('tmp/c2_slides_rebuild/disabled.tex').write_text(s.replace('[12pt,aspectratio=169]','[handout,12pt,aspectratio=169]').replace('% \\GTenHighlightsfalse % Uncomment','\\GTenHighlightsfalse % Uncomment'),encoding='utf8')
