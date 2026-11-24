"""Checks specific to the eight C4 scenarios; not a general PDF validator."""
from pathlib import Path
from fractions import Fraction as F
from itertools import product
from math import prod, floor, ceil
import json,re
from pypdf import PdfReader

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
src=ROOT/'book2026-2027/grade10/term_2/1-practice_activities/G10_T2_L1_C4_practice_activity.tex'
text=src.read_text(encoding='utf-8')
data=json.loads((HERE/'data.json').read_text())
graphs=re.findall(r'\\BreakEvenGraph\{(\d+)\}\{(-?\d+)\}\{(-?\d+)\}\{([^}]+)\}',text)
assert len(graphs)==18
g=0
report=[]
for d in data:
    n,p=d['n'],F(d['p'])
    # Enumerate ordered sequences rather than using the binomial formula.
    mass=[F(0)]*(n+1)
    for trial_results in product((0,1),repeat=n):
        mass[sum(trial_results)]+=prod(p if b else 1-p for b in trial_results)
    assert mass==list(map(F,d['q']))
    assert sum(mass)==1 and sum(k*mass[k] for k in range(n+1))==n*p
    typ,lo,hi=d['event']; event=sum(mass[lo:hi+1])
    vals=[]
    for i,(name,a,b) in enumerate(d['alts'],1):
        ys=[a+b*k for k in range(n+1)]
        assert min(ys)<0<max(ys) and len(set(ys))==n+1
        loss=sum(mass[k] for k in range(n+1) if ys[k]<0)
        cutoff=ceil(F(-a,b))-1 if b>0 else floor(F(-a,b))+1
        assert [k for k in range(n+1) if ys[k]<0]==[k for k in range(n+1) if (k<=cutoff if b>0 else k>=cutoff)]
        expected=sum(ys[k]*mass[k] for k in range(n+1))
        assert expected==a+b*n*p
        root=F(-a,b*n)
        assert 0<root<1 and a+b*n*root==0
        assert tuple(graphs[g])==(str(i),str(a),str(a+b*n),str(root.numerator)+'/'+str(root.denominator))
        g+=1
        # Check monetary CDFs at every payoff and on both sides of each jump,
        # including degenerate endpoint distributions and a noninitial p.
        for testp in (F(0),p,F(1,3),F(1)):
            mm=[F(0)]*(n+1)
            for outcomes in product((0,1),repeat=n):
                mm[sum(outcomes)]+=prod(testp if v else 1-testp for v in outcomes)
            for y in ys:
                for t in (F(y)-F(1,100),F(y),F(y)+F(1,100)):
                    direct=sum(mm[k] for k in range(n+1) if ys[k]<=t)
                    if t<min(ys): inverse=F(0)
                    elif t>=max(ys): inverse=F(1)
                    elif b>0: inverse=sum(mm[:floor((t-a)/b)+1])
                    else: inverse=sum(mm[ceil((a-t)/(-b)):])
                    assert direct==inverse
        # The two strict sign intervals and endpoint signs agree with slope.
        for tp in (F(0),root/2,root,(root+1)/2,F(1)):
            assert ((a+b*n*tp)>0)==(tp>root if b>0 else tp<root)
            assert ((a+b*n*tp)<0)==(tp<root if b>0 else tp>root)
        vals.append(dict(alternative=name,initial_expectation=str(expected),loss_probability=str(loss),root=str(root),endpoints=[a,a+b*n],loss_cutoff=cutoff))
    report.append(dict(scenario=d['key'],count_event_probability=str(event),alternatives=vals))

criterion='Applies the binomial distribution to fixed-trial financial situations by verifying its conditions and calculating probabilities using the binomial probability formula.'
assert text.count(criterion)==1
assert re.findall(r'\\section\{([^}]+)\}',text)==['Introduction','Notation Reference and Practice Procedure','General Worked Problems','Advanced Problems']
assert text.index(r'\subsection*{Highlight legend}')<text.index(r'\subsection{Introductory example 1')
assert len(re.findall(r'\{4\}/\{sol:c4-',text))==16
assert not re.search(r'\{3\}/\{sol:',text)
assert not re.search(r'\\addcontentsline[^\n]*Evaluated',text)
assert text.count('% \\GTenHighlightsfalse')==1

pdf=PdfReader(HERE/'build/G10_T2_L1_C4_practice_activity.pdf')
names=pdf.named_destinations
aux=(HERE/'build/G10_T2_L1_C4_practice_activity.aux').read_text(encoding='utf-8')
labels={m[0]:(int(m[1]),m[2]) for m in re.findall(r'\\newlabel\{([^}]+)\}\{\{[^}]*\}\{(\d+)\}\{[^}]*\}\{([^}]+)\}',aux)}
checks=['toc','sec:introduction','tab:highlight-legend','tab:notation-reference','sec:t2-c4-general','sec:t2-c4-advanced']
for d in data:
    checks.extend([d['label'],f"sol:c4-{d['key']}-model",f"sol:c4-{d['key']}-decision"])
for label in checks:
    page,dest=labels[label]
    assert dest in names,(label,dest)
    assert pdf.get_destination_page_number(names[dest])+1==page,label
    page_text=pdf.pages[page-1].extract_text()
    if label.endswith('-model'): assert 'Task 1' in page_text
    if label.endswith('-decision'): assert 'Task 2' in page_text
    if label=='toc': assert 'Contents' in page_text
    if label=='tab:highlight-legend': assert 'Highlight legend' in page_text
    if label=='tab:notation-reference': assert 'Detailed notation reference' in page_text
links=0
for page in pdf.pages:
    for ref in page.get('/Annots',[]):
        annot=ref.get_object()
        action=annot.get('/A',{})
        target=action.get('/D') if action.get('/S')=='/GoTo' else annot.get('/Dest')
        if target is not None:
            assert isinstance(target,str) and target in names,target
            assert 0<=pdf.get_destination_page_number(names[target])<len(pdf.pages)
            links+=1
outline=str(pdf.outline)
assert 'Evaluated criteria' not in outline
toc=(HERE/'build/G10_T2_L1_C4_practice_activity.toc').read_text()
assert 'Evaluated criteria' not in toc
assert 'Evaluated criteria' in pdf.pages[0].extract_text()
assert all(len(page.extract_text().strip())>40 for page in pdf.pages)
summary=dict(pages=len(pdf.pages),internal_links=links,checked_label_destinations=len(checks),graphs=g,scenarios=report)
(HERE/'verification.json').write_text(json.dumps(summary,indent=2))
print(json.dumps({k:v for k,v in summary.items() if k!='scenarios'}))
print('Exact enumeration, CDF jump boundaries, supports, losses, expectations, graph roots/endpoints, sign intervals, structure and PDF navigation passed.')
