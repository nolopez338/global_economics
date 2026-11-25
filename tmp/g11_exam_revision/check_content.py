from pathlib import Path
from decimal import Decimal as D
import re, subprocess

root=Path('book2026-2027/grade11/term_2/4-learning_evidences')
e=(root/'G11_T2_L1_C1C2_exam.tex').read_text(encoding='utf-8')
s=(root/'G11_T2_L1_C1C2_exam_solution.tex').read_text(encoding='utf-8')
marks=[2,2,1,2,1]*2+[3,3,2,2,2]
for text in (e,s):
    got=[int(x) for x in re.findall(r'\\item .*?\\sscore\{\\sml\{(\d+)\}\}',text)]
    assert got==marks,got
    assert not any(x in text for x in ('general tasks','general scoring table','Task-level allocations'))
    assert 'at least 4 out of 14 points' in text
    assert 'Points cannot transfer between criteria.' in text
assert [int(x) for x in re.findall(r'\\taskprompt\{C[12] Task \d\}\{(\d+)\}',s)]==marks
assert [int(x) for x in re.findall(r'\\worked\{C[12] Task \d \\score\{(\d+)\}',s)]==marks
rubric=[D(x) for x in re.findall(r'^C[12] Task \d&([\d.]+)&',s,re.M)]
assert rubric==list(map(D,marks)),rubric
for macro in ('cOneA','cOneB','cTwoA','cTwoB','cTwoC'):
    pat=r'\\newcommand\{\\'+macro+r'\}\{([^\n]+)\}'
    assert re.search(pat,e)[1]==re.search(pat,s)[1]
totals=[0,0]
for p in range(3):
    m=marks[p*5:p*5+5]
    c1,c2=sum(m[:2]),sum(m[2:])
    assert c1==c2==([4,4,6][p])
    totals[0]+=c1;totals[1]+=c2
    assert f'\\ref*{{q:{p+1}}}&{c1}&{c2}&{c1+c2}' in e
assert totals==[14,14] and sum(totals)==28
# Proposed rubric components, in task order; multiplicities already expanded.
components=[
    [[D('.5'),D('.75'),D('.75')],[D('1.5'),D('.5')],[D('.25'),D('.25'),D('.5')],[D('.4'),D('.4'),D('.6'),D('.3'),D('.3')],[D('.25')]*4],
    [[D('.5'),D('.75'),D('.75')],[D('1.5'),D('.5')],[D('.25'),D('.25'),D('.5')],[D('.4'),D('.4'),D('.6'),D('.3'),D('.3')],[D('.25')]*4],
    [[D('.75'),D('.75'),D('.5'),D('1')],[D('1.5'),D('1.5')],[D('.5'),D('.75'),D('.75')],[D('.4'),D('.4'),D('.6'),D('.3'),D('.3')],[D('.75'),D('.75'),D('.5')]]
]
assert [sum(c) for group in components for c in group]==rubric
# Confirm original scenario prose/data and all worked mathematics were preserved.
old=subprocess.check_output(['git','show','HEAD:'+str(root/'G11_T2_L1_C1C2_exam_solution.tex').replace('\\','/')],encoding='utf-8')
for suffix in ('p1c1a','p1c1b','p1c2a','p1c2b','p1c2c','p2c1a','p2c1b','p2c2a','p2c2b','p2c2c','p3c1a','p3c1b','p3c2a','p3c2b','p3c2c'):
    pat=r'\\worked[^\n]+\{sol:'+suffix+r'\}(.*?)\\secInicio'
    assert re.search(pat,old,re.S)[1]==re.search(pat,s,re.S)[1],suffix
# Independent check of initial confidence calculations and retrospective coverage.
for mean,sd,n,z,expected in [(240,60,100,'1.960',('228.240','251.760','23.520')),(82,36,144,'1.645',('77.065','86.935','9.870')),(82,36,144,'2.576',('74.272','89.728','15.456')),(32,8,64,'1.960',('30.040','33.960','3.920'))]:
    se=D(sd)/D(n).sqrt(); margin=D(z)*se
    assert (D(mean)-margin,D(mean)+margin,2*margin)==tuple(map(D,expected))
p1=[('224.24','247.76'),('232.24','255.76'),('238.24','261.76'),('246.24','269.76'),('218.24','241.76'),('235.24','258.76'),('230.24','253.76'),('242.24','265.76'),('221.24','244.76'),('234.24','257.76')]
assert sum(D(a)<=245<=D(b) for a,b in p1)==7
assert all(D(b)-D(a)==D('23.52') for a,b in p1)
assert 176+20+4==200 and (176/200*100,(176+20)/200*100)==(88,98)
assert (abs(70-95),abs(88-90),abs(98-99),abs(80-95))==(25,2,1,15)
print('PASS: 15 task allocations, labels/order, repeated prompts, rubric marks/components, matrix and 14+14=28 totals; original worked content preserved; initial CI and coverage results verified.')
