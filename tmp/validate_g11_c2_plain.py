from pathlib import Path
import re
s=Path('book2026-2027/grade11/term_2/1-practice_activities/G11_T2_L1_C2_practice.tex').read_text(encoding='utf-8')
b=Path('tmp/g11-c2-plain-before.tex').read_text(encoding='utf-8')
intro=r'\section{Introduction}'
notation=r'\section{Notation Reference'
general=r'\section{General Worked Problems}'
advanced=r'\section{Advanced Problems}'
assert s[s.index(intro):s.index(notation)]==b[b.index(intro):b.index(notation)]
assert s[s.index(advanced):]==b[b.index(advanced):]
g=s[s.index(general):s.index(advanced)]
oldg=b[b.index(general):b.index(advanced)]
pattern=r'\\InformationTable\{\n(.*?)\n\}'
tables=re.findall(pattern,g,re.S)
oldtables=re.findall(pattern,oldg,re.S)
assert len(tables)==4
for t,old in zip(tables,oldtables):
    rows=[r.strip().split(' & ') for r in t.splitlines() if ' & ' in r]
    oldrows=[r.strip().split(' & ') for r in old.splitlines() if ' & ' in r]
    assert [r[2] for r in rows if r[2]]==['Population parameters','Sample statistics','Procedure Settings']
    assert t.count(r'\midrule')==2
    assert sorted((r[0],r[1],r[3]) for r in rows)==sorted((r[0],r[1],r[3]) for r in oldrows)
    assert [r[0] for r in rows]==[oldrows[i][0] for i in [0,3,1,2,8,4,5,6,7]]
print('PASS: four tables; one label per group in required order; two separators; all other cells unchanged.')
print('PASS: Introduction and Advanced Problems unchanged.')
for problem in re.split(r'\\subsection\{',g)[1:]:
    pre=problem.split(r'\QuestionsTasks')[0]
    pre=re.sub(r'\\begin\{tikzpicture\}.*?\\end\{tikzpicture\}','',pre,flags=re.S)
    assert '$' not in pre
    banned=r'\b(normal|independent|critical|standard error|two-sided|coverage|interval|nominal|distribution|endpoints|mutually exclusive|denominator|numerator|probability|decimal|multiplier)\b'
    assert not re.search(banned,pre,re.I),re.findall(banned,pre,re.I)
print('PASS: all four descriptions and table headings have no math notation or screened technical terms; diagrams excluded.')
print('PASS: labels and hyperlink commands preserved:', re.findall(r'\\(?:label|hyperref|secInicio|SectionProblemLink)[^\n]*',s)==re.findall(r'\\(?:label|hyperref|secInicio|SectionProblemLink)[^\n]*',b))
