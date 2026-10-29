from pathlib import Path
from fractions import Fraction as F
import re
base=Path('book2026-2027/grade10/term_1/3-learning_evidences')
src=(base/'G10_T1_C1C2C3C4C5C6C7_exam.tex').read_text(encoding='utf-8')
tex=(base/'G10_T1_C1C2C3C4C5C6C7_exam_solution.tex').read_text(encoding='utf-8')
blocks=re.findall(r'\\SubsectionBox\{([^\n]+)\}\n(.*?)\\end\{minipage\}',src,re.S)
sections=re.split(r'\\sectionScored',tex)[1:]
assert len(sections)==14
assert tex.count('\\subsection{')==13
norm=lambda s: re.sub(r'\s+','',s)
for i,((title,body),section) in enumerate(zip(blocks,sections),1):
    scenario=body.split('Characterize' if i<=2 else 'What ' if i<=11 else 'State the preferred')[0].strip()
    assert norm(scenario) in norm(section), (i,'scenario/table changed')
    if i>=3:
        q=body[len(scenario):].strip()
        assert norm(q) in norm(section),(i,'question changed')
    else:
        for q in ['Characterize the key elements of the decision-making situation', 'and construct the payoff table.']:
            assert q in section
    assert f'{{{title.split(" "+chr(92)+"score")[0]}}}' in section

labels=re.findall(r'\\label\{([^}]+)\}',tex)+re.findall(r'\\sectionScored\{[^\n]+?\}\{[^\n]*?\}\{([^}]+)\}',tex)
assert len(labels)==len(set(labels)), 'duplicate label'
targets=re.findall(r'\\secInicio\[([^]]*)\]\[([^]]*)\]',tex)
for pair in targets:
    assert all(x in labels for x in pair if x), pair
for target in re.findall(r'\{\d\}/\{([^}]+)\}',tex): assert target in labels,target
assert len(re.findall(r'\\subsection\*\{C[1-7]',tex))==15

values={}
for i in range(3,14):
    body=blocks[i-1][1].split('\\midrule')[1].split('\\bottomrule')[0]
    values[i]=[[int(c.strip()) for c in r.strip().split('&')[1:]] for r in body.split('\\\\') if '&' in r]
expected_extrema={3:([120,84,55,24],[-30,16,29,24]),4:([150,95,60,30],[-45,12,26,30]),5:([140,100,68,48],[-40,8,22,28])}
for i,(mx,mn) in expected_extrema.items():
    assert list(map(max,values[i]))==mx and list(map(min,values[i]))==mn
expected_regrets={6:[[0,16,42],[18,0,12],[38,10,0]],7:[[0,24,64],[26,0,22],[50,10,2],[76,28,0]],8:[[0,100,280,600],[220,0,0,240],[480,160,20,0]]}
for i,expected in expected_regrets.items():
    v=values[i]; best=[max(col) for col in zip(*v)]
    actual=[[b-x for b,x in zip(best,row)] for row in v]
    assert actual==expected
    for row,reg in zip(v,actual):
        for b,x,r in zip(best,row,reg):
            xx=f'({x})' if x<0 else str(x)
            cell=f'{b}-{xx}'+r'\\='+str(r)
            assert tex.count(cell)==2,(i,cell)
expected_emvs={9:['48.40','53.50','44.70'],10:['39.20','51.20','47.60','28'],11:['45.60','58.40','54.60']}
prob={9:['.4','.35','.25'],10:['.3','.4','.3'],11:['.2','.3','.3','.2']}
for i,es in expected_emvs.items():
    q=list(map(F,prob[i])); assert sum(q)==1 and all(0<=p<=1 for p in q)
    for j,(row,e) in enumerate(zip(values[i],es),1):
        result=sum(x*p for x,p in zip(row,q))
        assert result==F(e)
        assert tex.count('='+e+(r',\\' if j<len(es) else '.'))>=2,(i,e)

for i,mults,upper,coefs,threshold in [(12,[F(1),F(1,2)],F(2,3),[(130,-8),(34,28)],F(3,8)),(13,[F(2),F(1)],F(1,3),[(-144,84),(90,36)],F(8,39))]:
    for row,(a,b) in zip(values[i],coefs):
        assert b==row[-1]
        assert a==sum((x-row[-1])*m for x,m in zip(row[:2],mults))
    (a,b),(c,d)=coefs
    assert (d-b)/(F(a)-c)==threshold
    assert 0<threshold<upper
    for p in [F(0),threshold/2,threshold,(threshold+upper)/2,upper]:
        q=[m*p for m in mults]; q+=[1-sum(q)]
        assert all(0<=x<=1 for x in q) and sum(q)==1
        es=[sum(x*z for x,z in zip(row,q)) for row in values[i]]
        assert es==[a*p+b,c*p+d]
        sign=(es[0]>es[1])-(es[0]<es[1])
        desired=((p>threshold)-(p<threshold))*(1 if i==12 else -1)
        assert sign==desired
    q=[m*(upper+F(1,100)) for m in mults]
    assert 1-sum(q)<0
assert F(130)*F(3,8)-8==F(163,4)
assert F(84)-144*F(8,39)==F(708,13)
assert [[q*(b+s)+f for q,s in zip(qs,[6,2])] for b,f,qs in [(12,80,[30,18]),(15,50,[24,16])]]==[[620,332],[554,322]]
assert [[q*(b+s-c)-f for q,s,f in zip(qs,[8,3],[500,650])] for b,c,qs in [(32,18,[90,60]),(45,26,[70,40])]]==[[1480,370],[1390,230]]
assert 'minimum of 5 cumulative points' in tex and 'minimum of 4' not in tex
print('PASS: 13 original scenarios/tables/questions; 15 criterion solutions; 13 summaries; unique labels and navigation.')
print('PASS: all payoffs, row extrema, regret cells, EMVs, probability domains, thresholds, ties and endpoint preferences.')
print('PASS: detailed and summarized numeric results agree; 6 per criterion and 42 overall.')
from pypdf import PdfReader
pdf=PdfReader(base/'G10_T1_C1C2C3C4C5C6C7_exam_solution.pdf')
dest=pdf.named_destinations
links=0
for page in pdf.pages:
    for ref in page.get('/Annots',[]):
        a=ref.get_object()
        if a.get('/Subtype')=='/Link':
            links+=1
            action=a.get('/A',{})
            d=action.get('/D') if action else a.get('/Dest')
            if isinstance(d,str): assert d in dest,d
print(f'PASS: {len(pdf.pages)} PDF pages, {links} links and {len(dest)} named destinations; all internal links resolve.')
