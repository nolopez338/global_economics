from pathlib import Path
import re
p=Path('book2026-2027/grade10/term_2/2-class_activities/G10_T2_L1_C1_classroom_activity.tex')
s=p.read_text(encoding='utf-8'); old=Path('tmp/c1_classroom_layout/original.tex').read_text(encoding='utf-8')
marker='\\ifprintsolutions\n\\clearpage'
a,b=s.split(marker,1); original=old.split(marker,1)[1]
def tasks(t):
    found=[]
    for m in re.finditer(r'\\task\{[123]\}\{',t):
        level=1; i=m.end()
        while level:
            if t[i]=='{': level+=1
            elif t[i]=='}': level-=1
            i+=1
        found.append((m.start(),i,t[m.start():i]))
    return found
before=tasks(original); after=tasks(b)
assert len(before)==len(after)==18
for cur,orig in reversed(list(zip(after,before))):
    b=b[:cur[0]]+orig[2]+b[cur[1]:]
b=b.replace('\\GTenHLOutcome{Complete} \\GTenHLOutcome{outcomes}\\quad','\\GTenHLOutcome{Complete outcomes}\\quad',1)
p.write_text(a+marker+b,encoding='utf-8',newline='\n')
assert a==old.split(marker)[0]
assert [x[2] for x in tasks(b)]==[x[2] for x in before]
print('Outside solutions unchanged; all 18 original task explanations preserved verbatim.')
