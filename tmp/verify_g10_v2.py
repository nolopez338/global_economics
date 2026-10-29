from pathlib import Path
from fractions import Fraction as F
import re
base=Path('book2026-2027/grade10/term_1/3-learning_evidences')
s=(base/'G10_T1_C1C2C3C4C5C6C7_examV2_solution.tex').read_text(encoding='utf-8')
old=(base/'G10_T1_C1C2C3C4C5C6C7_exam_solution.tex').read_text(encoding='utf-8')
parts=re.split(r'\\sectionScored\{',s)[1:]
assert len(parts)==14
original=re.split(r'\\sectionScored\{',old)[1:]
summaries=re.split(r'\\subsection\{',parts[-1])[1:]
assert len(summaries)==13
def paytable(text):
    t=text.split('\\midrule',1)[1].split('\\bottomrule',1)[0]
    rows=[]
    for row in t.split('\\\\'):
        cells=row.strip().split('&')
        if len(cells)>1 and '$P(S_j)$' not in cells[0]: rows.append([int(x.strip()) for x in cells[1:]])
    return rows
def calc(expr):
    expr=re.sub(r'(?<=[0-9)])(?=\()','*',expr)
    return eval(expr,{'__builtins__':{}},{})
expected=[[[622,379],[571,345]],[[1392,500],[1242,292]]]
for n in [1,2]:
    p=parts[n-1]; su=summaries[n-1]
    assert paytable(p)==expected[n-1]
    chains=re.findall(r'P\(A_\d,S_\d\)&=([^\n]+)',p)
    results=[]
    for chain in chains:
        terms=[x.rstrip(',.\\') for x in chain.split('=')]
        values=[calc(x) for x in terms]
        assert len(set(values))==1,terms
        results.append(values[-1])
    assert results==sum(expected[n-1],[])
    for expr in re.findall(r'\$([0-9][^$]*=[0-9]+)\$',su):
        values=[calc(x) for x in expr.split('=')]
        assert values[0]==values[1]
    print(n,'four payoffs and summary calculations verified')
for n in range(3,14):
    p=parts[n-1]; su=summaries[n-1]; rows=paytable(p); prev=paytable(original[n-1])
    assert list(map(len,rows))==list(map(len,prev))
    assert all(a!=b for r,t in zip(rows,prev) for a,b in zip(r,t)),n
    assert [len(set(r))==1 for r in rows]==[len(set(r))==1 for r in prev]
    if n<=5:
        for block in [p,su]:
            for r in rows:
                if block==p:
                    vals=','.join(map(str,r))
                    assert r'\max\{'+vals+r'\}='+str(max(r)) in block
                    assert r'\min\{'+vals+r'\}='+str(min(r)) in block
        mx=list(map(max,rows)); mn=list(map(min,rows))
        assert mx.index(max(mx))==0 and mn.index(max(mn))==({3:2,4:3,5:3}[n])
        print(n,'all extrema; winners',mx.index(max(mx))+1,mn.index(max(mn))+1)
    elif n<=8:
        best=[max(col) for col in zip(*rows)]
        regrets=[[b-x for b,x in zip(best,r)] for r in rows]
        worst=list(map(max,regrets))
        assert worst.index(min(worst))==1 and worst.count(min(worst))==1
        for block in [p,su]:
            found=re.findall(r'\\begin\{gathered\}(-?\d+)-\(?(-?\d+)\)?\\\\=(\d+)\\end\{gathered\}',block)
            assert len(found)==sum(map(len,rows))
            for (b,x,r),expected_r in zip(found,sum(regrets,[])):
                assert int(b)-int(x)==int(r)==expected_r
        print(n,'all column bests and regrets verified; maxima',worst)
    elif n<=11:
        pr=re.search(r'\$P\(S_j\)\$ & (.*?)\\\\',p)[1]
        q=[F(x.strip()) for x in pr.split('&')]
        assert sum(q)==1 and all(0<x<1 for x in q)
        vals=[sum(x*y for x,y in zip(q,row)) for row in rows]
        assert vals.index(max(vals))==1 and vals.count(max(vals))==1
        for block in [p,su]:
            found=re.findall(r'EMV\(A_\d\)&=(.*?)(?=,\\\\|\.\n)',block,re.S)
            assert len(found)==len(rows)
            for chain,v in zip(found,vals):
                terms=chain.replace('\\\\&','').replace('\n','').split('=')
                for term in terms: assert abs(calc(term)-float(v))<1e-9,(n,term,v)
        print(n,'probabilities, weighted terms, and EMVs',list(map(str,vals)))
    else:
        weights=[F(1),F(1,2)] if n==12 else [F(2),F(1)]
        lim=1/sum(weights)
        def direct(row,p): return weights[0]*p*row[0]+weights[1]*p*row[1]+(1-sum(weights)*p)*row[2]
        slopes=[direct(row,F(1))-row[2] for row in rows]
        threshold=F(rows[1][2]-rows[0][2],slopes[0]-slopes[1])
        assert threshold==({12:F(2,5),13:F(3,14)}[n])
        tie=direct(rows[0],threshold)
        assert tie==direct(rows[1],threshold)==({12:F(48),13:F(424,7)}[n])
        for point in [F(0),threshold/2,(lim+threshold)/2,lim]:
            diff=direct(rows[0],point)-direct(rows[1],point)
            assert (diff>0)==((point>threshold) if n==12 else (point<threshold))
        print(n,'domain',lim,'threshold',threshold,'tie',tie,'endpoints',[(direct(r,0),direct(r,lim)) for r in rows])
labels=re.findall(r'\\label\{([^}]+)\}',s)+re.findall(r'\\sectionScored\{[^\n]+\}\{(sec:[^}]+)\}',s)
assert len(labels)==len(set(labels))
refs=re.findall(r'(?:sec|sol|summary):[a-z0-9-]+',s)
assert set(refs)<=set(labels)
assert 'Version 2' in s and '2026--2027' in s
assert s[s.index('\\section*{Learning objective}'):s.index('\\clearpage\n\\sectionScored')]==old[old.index('\\section*{Learning objective}'):old.index('\\clearpage\n\\sectionScored')]
print('All labels resolve. Assessment text and 42-point / six-per-criterion allocation unchanged.')
