from fractions import Fraction as F
from pathlib import Path
import re, hashlib

folder=Path('book2026-2027/grade10/term_1/2-class_activities')
old=(folder/'G10_T1_L1_C6C7_classroom_activity.tex').read_text()
new=(folder/'G10_T1_L1_C6C7_classroom_activityV2.tex').read_text()
def tables(text):
    result={}
    for n,section in enumerate(re.split(r'(?=\\section\{)',text)[1:],1):
        if n==1: continue
        table=re.search(r'\\begin\{tabular\}.*?\\end\{tabular\}',section,re.S)[0]
        rows=[]
        for row in table.split(r'\\'):
            if re.search(r'&\s*-?\d+\s*&',row):
                cells=re.findall(r'&\s*(-?\d+)\s*(?=&|$)',row)
                rows.append(list(map(int,cells)))
        result[n]=rows
    return result
a,b=tables(old),tables(new)
assert a.keys()==b.keys()
for n in a:
    assert len(a[n])==len(b[n])
    for x,y in zip(a[n],b[n]):
        assert len(x)==len(y)
        assert all(i!=j for i,j in zip(x,y)),(n,x,y)
        assert all(j<0 for i,j in zip(x,y) if i<0)
        if len(set(x))==1: assert len(set(y))==1
print('All',sum(len(row) for rows in b.values() for row in rows),'payoff cells changed; dimensions, negative entries and constant rows preserved.')

prob={2:['.7','.3'],3:['.4','.35','.25'],4:['.55','.45'],5:['.45','.25','.30'],6:['.25','.30','.25','.20']}
for n,ps in prob.items():
    ps=list(map(F,ps)); assert all(p>=0 for p in ps) and sum(ps)==1
    section=re.split(r'(?=\\section\{)',new)[n]
    actual=list(map(lambda s:F(s)/100,re.findall(r'(\d+)\\%',section)[:len(ps)]))
    assert actual==ps,(n,'stated probability mismatch',actual,ps)
    terms=[(F(p),int(v)) for p,v in re.findall(r'\((0\.\d+)\)\((-?\d+)\)',section)]
    if n in (3,4):
        assert terms==[(p,v) for row in b[n] for p,v in zip(ps,row)],(n,terms)
    emvs=[sum(p*v for p,v in zip(ps,row)) for row in b[n]]
    assert emvs.count(max(emvs))==1
    print('C6 section',n,'EMVs:',', '.join(map(str,emvs)), 'winner A'+str(emvs.index(max(emvs))+1))

def envelope(n,lines,expected):
    def best(p):
        vals=[m*p+c for m,c in lines]; hi=max(vals)
        return tuple(i+1 for i,v in enumerate(vals) if v==hi)
    crosses={F(0),F(1)}
    for i,(m,c) in enumerate(lines):
        for mm,cc in lines[i+1:]:
            if m!=mm:
                p=F(cc-c,m-mm)
                if 0<p<1: crosses.add(p)
    crosses=sorted(crosses)
    intervals=[(l,r,best((l+r)/2)) for l,r in zip(crosses,crosses[1:])]
    actual=[(x,best(x)) for x in crosses[1:-1] if len(best(x))>1]
    assert [p for p,_ in actual]==expected,(n,actual,expected)
    for l,r,winner in intervals:
        assert len(winner)==1
        for p in [(3*l+r)/4,(l+3*r)/4]: assert best(p)==winner
    assert len(best(F(0)))==len(best(F(1)))==1
    assert set(w[0] for _,_,w in intervals)==set(range(1,len(lines)+1)) if expected else best(F(0))==best(F(1))
    print('C7 section',n,'functions (slope,intercept)',lines)
    print('  optimal thresholds:',[(str(p),float(p),ties) for p,ties in actual],'; endpoints:',best(F(0)),best(F(1)))
    print('  checked all intersections, interval samples and endpoints:',intervals)
    return actual

for n,thresholds in [(7,[F(3,5)]),(8,[F(5,8)]),(9,[F(4,9)]),(10,[]),(11,[F(1,3),F(1,2)]),(13,[F(1,4),F(1,2),F(3,4)])]:
    lines=[(F(x-y),F(y)) for x,y in b[n]]
    envelope(n,lines,thresholds)
    if n==10:
        assert all(x>y for x,y in zip(*b[n]))
        assert lines[0][0]==lines[1][0] and lines[0][1]>lines[1][1]

alpha=F(1,4)
assert 0<alpha<1
for p in [F(0),F(1,5),F(1,2),F(1)]:
    ps=[p,alpha*(1-p),(1-alpha)*(1-p)]
    assert min(ps)>=0 and sum(ps)==1
lines=[]
for x,y,z in b[12]:
    c=alpha*y+(1-alpha)*z
    lines.append((x-c,c))
envelope(12,lines,[F(4,19)])

# Two-parameter EMVs are m*p+n*q+c. Check the complete feasible triangle.
lines=[(x-z,y-z,z) for x,y,z in b[14]]
diff=tuple(x-y for x,y in zip(*lines))
assert diff==(50,35,-20)
assert -F(diff[2],diff[0])==F(2,5)
assert -F(diff[2],diff[1])==F(4,7)
def difference(p,q):return diff[0]*p+diff[1]*q+diff[2]
assert difference(F(1,5),F(2,7))==0
assert F(1,5)+F(2,7)<1
assert difference(F(1,2),F(1,5))>0
assert difference(F(1,10),F(1,10))<0
for i in range(21):
    for j in range(21-i):
        p,q=F(i,20),F(j,20)
        ps=[p,q,1-p-q]
        assert min(ps)>=0 and sum(ps)==1
        vals=[sum(v*s for v,s in zip(row,ps)) for row in b[14]]
        assert vals[0]-vals[1]==difference(p,q)
print('C7 section 14: EMVs',lines,'indifference 10p+7q=4; both interior regions verified.')
assert hashlib.sha256((folder/'G10_T1_L1_C6C7_classroom_activity.tex').read_bytes()).hexdigest()=='075cd61d5e7ad2c93d1c51ed98a83fa9dfc6bbeaa0467fb4e77e3852aede6593'
print('PASS: source unchanged; all probability and EMV requirements verified exactly.')
