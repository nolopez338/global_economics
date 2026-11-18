from pathlib import Path
import re, hashlib
root=Path(__file__).resolve().parents[2]
p=root/'book2026-2027/grade11/term_2/2-class_activities/G11_T2_L1_C2_classroom_activity.tex'
old=(Path(__file__).parent/'original.tex').read_bytes()
new=p.read_bytes()
begin=b'\\vspace{-3mm}\r\n\\subsubsection*{Task 1 solution}'
end=b'\r\n\r\nFour of the five simulated'
block=old[old.index(begin):old.index(end)]
assert block in new
print('Protected Task 1/2 solutions and Task 3 identification/calculations: byte-identical')
print('SHA256:',hashlib.sha256(block).hexdigest())
s=new.decode('utf-8').replace('\r\n','\n')
unprotected=s.replace(block.decode('utf-8').replace('\r\n','\n'),'')
assert not re.search(r'simulat|\\rm sim',unprotected,re.I)
print('Obsolete simulation terminology/notation: only in protected content')
paragraphs=re.findall(r'An initial study.*?(?=\n\\end\{minipage\}|\n\n\n\\task|\n\n\\problemtitle)',s,re.S)
# Contexts 1, 3, 5 and 6 end at their minipage; 2 and 4 at the next task/title.
assert len(paragraphs)==6, len(paragraphs)
for i,text in enumerate(paragraphs,1):
    clean=text.replace(r'\%','%')
    assert not re.search(r'[$_=]|\\',clean),(i,text)
    assert 'subsequent independent studies' in text
    assert 'later comprehensive' in text
print('All six narratives: ordinary prose, no math symbols/variable names; study sequence verified')
assert r'\mu_{\mathrm{known}}' in s
assert r'L_i\leq\mu_{\mathrm{known}}\leq U_i' in s
assert 'mutually exclusive' in s and 'nested' in s
for stage in ['Worked example','Guided Example','Independent Practice']:
    assert s.count('\\stageheading{'+stage+'}')==1
assert re.findall(r'\\problemtitle\{(\d)\}',s)==['1','2','2','3','4','5','6']
assert not re.search(r'\\(?:hl|highlight|colorbox|boxed)\b',s)
print('Structure, nested categories, Task 3 coverage rule and absence of highlights: verified')
log=p.with_suffix('.log').read_text(errors='replace')
assert not re.search(r'Overfull|Underfull|LaTeX Warning|^!',log,re.M)
assert '4 pages' in log
print('Compile: four pages; no overfull/underfull boxes or LaTeX warnings')
