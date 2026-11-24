from pathlib import Path
import re
W=Path(__file__).resolve().parent;ROOT=W.parent.parent
D=ROOT/'book2026-2027/grade10/term_2/3-slides/G10_T2_L1_C3_slides.tex'
s=D.read_text()
s=s.replace('(0,0) rectangle (12,5.35)','(0,-.4) rectangle (12,5.35)')
s=s.replace('at (5.6,.25)', 'at (5.6,-.15)')
s=s.replace(r'\begin{frame}[t]{Worked example 1: the weekend choice}',r'\begin{frame}[t]{Worked example 1: the weekend choice}'+'\n'+r'\framesubtitle{Campus concert food stand or indoor games}')
# Add paragraph boundaries between conceptual text blocks without changing math.
def braces(text,start):
    depth=1;i=start+1
    while depth:
        if text[i]=='{':depth+=1
        elif text[i]=='}':depth-=1
        i+=1
    return i
# Only visible blocks whose contents contain prose outside display math and which
# are outside aligned displays/TikZ. Keep paragraph skips reserved on all overlays.
parts=[];last=0
for m in re.finditer(r'\\visible<\d+->\{',s):
    start=m.end()-1;end=braces(s,start)
    preceding=s[:m.start()]
    if preceding.rfind(r'\begin{aligned}')>preceding.rfind(r'\end{aligned}'):continue
    if preceding.rfind(r'\begin{tikzpicture}')>preceding.rfind(r'\end{tikzpicture}'):continue
    content=s[start+1:end-1]
    # End every entire visible text/display block at a stable paragraph boundary.
    parts.append(s[last:end]+r'\par'+'\n');last=end
parts.append(s[last:]);s=''.join(parts)
# Keep source-map frame indices equal to logical counters, excluding section lines.
counter=1
def renumber(m):
    global counter
    counter+=1
    return '% Frame '+str(counter)+': '
s=re.sub(r'% Frame \d+: ',renumber,s)
D.write_text(s,encoding='utf-8');(W/'portable/lesson.tex').write_text(s,encoding='utf-8')
for v in ['disabled','grayscale']:
    copy=s.replace('[12pt,aspectratio=169]','[handout,12pt,aspectratio=169]')
    if v=='disabled':copy=copy.replace(r'\GTenHighlightstrue',r'\GTenHighlightsfalse')
    else:copy=copy.replace(r'\begin{document}',r'\selectcolormodel{gray}\begin{document}')
    (W/v/'lesson.tex').write_text(copy,encoding='utf-8')
print('Refined graph label clearance, conceptual paragraph boundaries and source map.')
