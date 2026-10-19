from pathlib import Path
import re, hashlib
base=Path('book2026-2027/grade11/term_1/3-learning_evidences')
e=(base/'G11_T1_L1_C1C2C3C4_examV2.tex').read_text(encoding='utf-8')
s=(base/'G11_T1_L1_C1C2C3C4_examV2_solution.tex').read_text(encoding='utf-8')
def group(t,start):
    depth=0
    for j in range(start,len(t)):
        if t[j] in '{}' and (j==0 or t[j-1]!='\\'):
            depth+=1 if t[j]=='{' else -1
            if depth==0:return t[start+1:j],j+1
    raise ValueError(start)
def norm(t):return re.sub(r'\s+',' ',t).strip()
exam=[]
for m in re.finditer(r'\\SubsectionBox\{\d+\.',e):
    _,end=group(e,e.index('{',m.start()))
    b,_=group(e,e.index('{',end));exam.append(b.replace('\\columnbreak',''))
for i,m in enumerate(list(re.finditer(r'\\sectionScored\s*\n',s))[:12]):
    pos=m.end()
    for j in range(3):_,pos=group(s,s.index('{',pos))
    begin=s.index('{',pos)+1
    statement=s[begin:s.index('\\phantomsection',begin)]
    n=statement.index('\\QuestionsTasks')
    body,end=group(statement,statement.index('{',n))
    pos=0
    for j in range(3):task,pos=group(body,body.index('{',pos))
    task=re.sub(r'\\score\{[^}]*\}','',task)
    reconstructed=statement[:n]+task+statement[end:]
    assert norm(reconstructed)==norm(exam[i]),f'Problem {i+1} statement differs'
print('PASS: All 12 statements verbatim after removing navigation/score formatting.')
assert hashlib.sha256((base/'G11_T1_L1_C1C2C3C4_examV2.tex').read_bytes()).hexdigest()=='14e09242be5480c0ae390e20102235f7607ee0c0a71b3656e479351b63de69af'
print('PASS: Authoritative exam unchanged.')
