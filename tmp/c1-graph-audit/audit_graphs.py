from pathlib import Path
from fractions import Fraction as F
import re

source=Path('book2026-2027/grade10/term_2/1-practice_activities/G10_T2_L1_C1_practice_activity.tex')
s=source.read_text(encoding='utf-8')
sections={};name='Introduction'
for line in s.splitlines():
    if line.startswith(r'\subsection{'):
        name=line[len(r'\subsection{'):-1]
    m=re.fullmatch(r'\\GTen(OutcomeProbability|OutcomeValue|PMF)Graph\[(.*)\]\{([^{}]*)\}\{([^{}]*)\}',line)
    if not m:continue
    kind,opts,xs,ys=m.groups()
    xs=xs.split(',');ys=[F(v) for v in ys.split(',')]
    assert len(xs)==len(ys)
    tail=re.search(r'(?:^|,)tail=([^,]+)',opts)
    tail=F(tail[1]) if tail else F(0)
    if kind!='OutcomeValue':
        assert all(0<=v<=1 for v in ys)
        assert sum(ys)+tail==1,(name,kind)
        assert 'color=GTenHLProbability!32' in opts
        assert 'yhighlight=GTenHLProbability' in opts
    else:
        role=re.search(r'yhighlight=(GTenHL\w+)',opts)[1]
        assert f'color={role}!32' in opts
        assert 'xhighlight=GTenHLOutcome' in opts
    if kind=='PMF':
        xs=[F(v) for v in xs]
        assert all(a<b for a,b in zip(xs,xs[1:]))
    sections.setdefault(name,[]).append((kind,xs,ys,tail))

expected={
 'Assign probability to each value':(1,3,3),
 'Introductory general problem: grouping outcomes':(1,1,1),
 'Advanced general problem: a finite model':(0,0,1),
 'Advanced general problem: an infinite model':(1,1,1),
 'Notebook buyers':(1,2,2),
 'Daily insurance claims':(0,0,1),
 'Payment methods and a fee':(1,1,1),
 'Investment results with a missing mass':(0,0,1),
 'Calls until a sale':(0,0,1),
 'Delivery records: two numerical descriptions':(1,2,2),
}
for name,counts in expected.items():
    graphs=sections[name]
    actual=tuple(sum(g[0]==k for g in graphs) for k in ['OutcomeProbability','OutcomeValue','PMF'])
    assert actual==counts,(name,actual,counts)
    probabilities=next((g for g in graphs if g[0]=='OutcomeProbability'),None)
    maps=[g for g in graphs if g[0]=='OutcomeValue']
    pmfs=[g for g in graphs if g[0]=='PMF']
    if probabilities and name!='Advanced general problem: an infinite model':
        for mapping,pmf in zip(maps,pmfs):
            assert mapping[1]==probabilities[1]
            grouped={}
            for val,prob in zip(mapping[2],probabilities[2]):grouped[val]=grouped.get(val,F(0))+prob
            assert grouped==dict(zip(pmf[1],pmf[2])),(name,grouped)
    for g in graphs:
        if g[3]:
            assert g[3] in (F(1,32),F(1,256))
            assert g[2]==[F(1,2**i) for i in range(1,len(g[2])+1)]

notebook=sections['Notebook buyers']
assert notebook[2][2]==[8,4,4,0]
delivery=sections['Delivery records: two numerical descriptions']
assert delivery[1][2]==[2,2,-3]
assert F(1,3)+F(1,2)==F(5,6)
assert F(1)-F('.7')-F('.1')==F('.2')
assert F(1)-F('.2')-F('.5')==F('.3')
assert sum(F(1,2**i) for i in range(1,4))==F(7,8)

print(f'PASS: {sum(len(g) for g in sections.values())} panels across {len(expected)} examples/problems.')
print('PASS: applicable panel counts, exact normalization/tails, grouped PMFs, mappings, semantic graph colors, ordered numeric spacing, and key results.')
