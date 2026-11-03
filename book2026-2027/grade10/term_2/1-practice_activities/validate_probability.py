"""Independent numerical and structural audit. Run with Python + scipy.

This checks rendered source answers against scipy distributions (which use
failures for nbinom), exact rational arithmetic, and direct central moments.
It does not generate the activity answers.
"""
from pathlib import Path
from fractions import Fraction as F
import itertools
import math
import re
from scipy.stats import binom, geom, nbinom, poisson

HERE = Path(__file__).resolve().parent
checks = 0
def require(condition, message):
    global checks
    assert condition, message
    checks += 1
def close(a,b):
    require(math.isclose(float(a),float(b),abs_tol=1e-11), f'{a} != {b}')
def source(c):
    return next(HERE.glob(f'*_C{c}_practice_activity.tex')).read_text(encoding='utf-8')
def block(c,title):
    text=source(c).split('\\subsection{'+title+'}',1)
    require(len(text)==2, f'C{c}: missing {title}')
    return text[1].split('\\subsection{',1)[0].split('\\section{',1)[0]
def answer(c,title,value):
    text=block(c,title)
    # Floating distribution libraries can straddle an exact half-way decimal
    # (e.g. 0.32805). Accept a last-place tie within the rounding error.
    displayed=[float(x) for x in re.findall(r'(?<![\d.])(?:0|1)\.\d{4}(?!\d)',text)]
    require(any(abs(x-value)<=0.000050000001 for x in displayed),
            f'C{c} {title}: expected {value:.4f}')
    require(0 <= value <= 1, f'Invalid probability {title}')

# A different implementation from the authored PMF products and sums.
bin_cases=[
('Introductory general problem: exactly two successes',3,.5,2,2),
('Advanced general problem: a central interval',6,.4,2,4),
('Loan defaults',5,.1,1,1),('On-time invoices',4,.8,3,3),
('Insurance claims at most one',6,.05,0,1),
('At least one business sale',8,.25,1,8),
('Payment fees in a band',10,.2,2,4),
('Supplier defects and a failed assumption',7,.15,2,7)]
for title,n,p,lo,hi in bin_cases:
    value=binom.cdf(hi,n,p)-binom.cdf(lo-1,n,p)
    answer(4,title,value)
    # Independently enumerate every binary sequence to check combinatorics.
    enumeration=sum(p**sum(s)*(1-p)**(n-sum(s))
                    for s in itertools.product([0,1],repeat=n)
                    if lo<=sum(s)<=hi)
    close(value,enumeration)
    close(sum(binom.pmf(k,n,p) for k in range(n+1)),1)

geo_cases=[
('Introductory general problem: first success on trial three',.5,3,'exact'),
('First sale on call four',.2,4,'exact'),
('Loan approval on the second application',.4,2,'exact'),
('Payment completed by attempt three',.7,3,'by'),
('Still waiting after five enquiries',.15,5,'after'),
('Call budget and first sale',.25,4,'by'),
('Failures before an insurance sale',.1,4,'exact')]
for title,p,t,mode in geo_cases:
    value=geom.pmf(t,p) if mode=='exact' else geom.cdf(t,p) if mode=='by' else geom.sf(t,p)
    answer(5,title,value)
    close(geom.cdf(t,p)+geom.sf(t,p),1)
answer(5,'Advanced general problem: a window and a changed starting point',geom.cdf(5,.3)-geom.cdf(2,.3))
answer(5,'Advanced general problem: a window and a changed starting point',geom.cdf(3,.3))
close((F(7,10)**2-F(7,10)**5)/(F(7,10)**2), F(657,1000))

nb_cases=[
('Introductory general problem: second success on trial three',2,.5,3,'exact'),
('Advanced general problem: target by a deadline',3,.4,6,'by'),
('Two sales on call four',2,.3,4,'exact'),
('Third approval on application five',3,.6,5,'exact'),
('Second invoice settled by contact four',2,.5,4,'by'),
('Below the insurance-sales target',3,.2,6,'after'),
('Sales within an outreach budget',3,.4,6,'by'),
('Failure counts and a geometric special case',2,.25,5,'exact')]
for title,r,p,t,mode in nb_cases:
    failures=t-r
    value=nbinom.pmf(failures,r,p) if mode=='exact' else nbinom.cdf(failures,r,p) if mode=='by' else nbinom.sf(failures,r,p)
    answer(6,title,value)
    close(nbinom.cdf(failures,r,p),binom.sf(r-1,t,p))
    if r==1: close(nbinom.pmf(t-1,1,p),geom.pmf(t,p))
for t in range(1,15):
    close(nbinom.pmf(t-1,1,.25),geom.pmf(t,.25))

poi_cases=[
('Introductory general problem: two events in one unit',1,1,2,'exact'),
('Advanced general problem: rescaling and a complement',.8,2.5,3,'atleast'),
('No insurance claims',.6,1,0,'exact'),('Two customer arrivals',3,1,2,'exact'),
('At most one defect',.02,50,1,'atmost'),
('At least one payment alert',4,.25,1,'atleast'),
('Claim costs over five days',.4,5,3,'atleast'),
('Defaults and a clustering warning',.5,2,1,'atmost')]
for title,rate,exposure,k,mode in poi_cases:
    lam=rate*exposure
    value=poisson.pmf(k,lam) if mode=='exact' else poisson.cdf(k,lam) if mode=='atmost' else poisson.sf(k-1,lam)
    answer(7,title,value)
    close(poisson.cdf(k,lam)+poisson.sf(k,lam),1)
    close(sum(poisson.pmf(j,lam) for j in range(100)),1)

# C8: inspect every numerical calculation table directly from the sources.
tables=re.findall(r'\\begin\{tabular\}\{rrrr\}(.*?)\\end\{tabular\}',source(8),re.S)
require(len(tables)==10,'Expected ten C8 calculation tables')
for t in tables:
    numeric=[]
    total=None
    for row in t.splitlines():
        row=row.replace('\\\\','').strip()
        cells=[x.strip() for x in row.split('&')]
        if len(cells)!=4: continue
        if cells[0]=='Total':
            total=list(map(F,cells[1:]))
        elif re.fullmatch(r'-?\d+(?:\.\d+)?',cells[0]):
            x,p,xp,x2p=map(F,cells)
            close(x*p,xp); close(x*x*p,x2p)
            numeric.append((x,p))
    require(bool(numeric) and total is not None,'Empty moment table')
    mu=sum(x*p for x,p in numeric)
    m2=sum(x*x*p for x,p in numeric)
    close(sum(p for x,p in numeric),1)
    close(total[0],1); close(total[1],mu); close(total[2],m2)
    close(sum((x-mu)**2*p for x,p in numeric),m2-mu**2)
    require(min(x for x,p in numeric)<=mu<=max(x for x,p in numeric),'Mean out of range')

for title,values,probs,variance in [
('Introductory general problem: a small score distribution',[0,1,2],[.25,.5,.25],.5),
('School-enterprise net gain',[-10,10,30],[.25,.5,.25],200),
('Insurance claim counts',[0,1,2],[.5,.4,.1],.44),
('Sales and a fixed operating cost',[0,1,2],[.2,.5,.3],.49),
('Claims and a reserve balance',[0,1,2],[.6,.3,.1],.45)]:
    mu=sum(x*p for x,p in zip(values,probs))
    direct=sum((x-mu)**2*p for x,p in zip(values,probs))
    close(direct,variance)
    require(f'{math.sqrt(direct):.4f}' in block(8,title),f'SD in {title}')
close(64*F(49,100),F('31.36'))
close(100-30*F(1,2),85)
close(900*F(45,100),405)
require(f'{math.sqrt(405):.4f}' in source(8),'Transformed reserve SD')
require(f'{math.sqrt(72):.4f}' in source(8),'Advanced transformed SD')

# Finite PMF, mapping, complement and endpoint checks from C1--C3.
finite=[
([0,1,2],[.1,.5,.4]),([0,2,5],[1/6,1/3,1/2]),
([0,1,2],[.25,.5,.25]),([0,1,2],[.7,.2,.1]),
([0,1],[.25,.75]),([-20,0,30],[.2,.5,.3]),
([-3,2],[.3,.7]),([0,2,5],[.2,.5,.3]),
([-1,1,4],[.25,.35,.4]),([0,1,2],[.5,.3,.2]),
([0,2,5],[.4,.35,.25]),([0,2,3],[.6,.3,.1]),
([-10,0,15,40],[.2,.3,.4,.1]),([0,3],[.4,.6])]
for values,probs in finite:
    close(sum(probs),1)
    require(all(p>0 for p in probs),'Positive support')
    def C(x): return sum(p for v,p in zip(values,probs) if v<=x)
    close(C(min(values)-1),0); close(C(max(values)),1)
    for v,p in zip(values,probs):
        close(C(v)-sum(q for u,q in zip(values,probs) if u<v),p)
        close(C(v),C(v+1e-8))
for p in [.3,.2,.04,.12,.85,.6,.08]:
    close(binom.pmf(0,1,p)+binom.pmf(1,1,p),1)
for title,p,money in [
('One loan default',.04,'800'),('One policy claim',.12,'300'),
('Invoice payment and reversal',.85,'6'),('Investment gain',.6,'25'),
('Chargeback and merchant balance',.08,'35')]:
    answer(3,title,p)
    s=block(3,title)
    require(money in s,f'C3 {title}: monetary transformation')
    require(f'{1-p:g}' in s,f'C3 {title}: complementary mass')
answer(3,'Introductory general problem: one binary trial',.3)
answer(3,'Introductory general problem: one binary trial',.7)
answer(3,'Advanced general problem: reversing success and measuring money',.2)
answer(3,'Three sales categories',.5)
close(12-50,-38); close(-10+25,15); close(30-35,-5)
close(F(1,6)+F(1,3)+F(1,2),1)
close(F(1,3)+F(1,2),F(5,6))
close(F(1,2)+F(1,4)+F(1,8),F(7,8))
close(math.factorial(4)/(math.factorial(2)*math.factorial(2)),6)
for title,value in [
('Introductory general problem: grouping outcomes',.5),
('Advanced general problem: a finite and an infinite model',5/6),
('Advanced general problem: a finite and an infinite model',1/8),
('Notebook buyers',.5),('Daily insurance claims',.3),
('Payment methods and a fee',.75),('Investment results with a missing mass',.8),
('Calls until a sale',7/8),('Delivery records: two numerical descriptions',.3)]:
    answer(1,title,value)
for title,values in [
('Introductory general problem: PMF to CDF',[.8,.7]),
('Advanced general problem: recovering jumps and testing candidates',[.75]),
('Afternoon refunds',[.3,.8]),('Transaction fees',[.4,.75,.35]),
('Late-payment counts',[.4,.3]),('Investment gain intervals',[.2,.5,.7]),
('Insurance PMF audit',[.4,.9]),('Account-fee CDF audit',[.6])]:
    for v in values: answer(2,title,v)
# The graph stems and included CDF endpoints agree with accumulated masses.
for xy in ['(0,0.2)(2,0.5)(5,0.3)','(0,0.2)(2,0.7)(5,1)']:
    require(xy in source(2),'C2 graph/table agreement')
for title,value in [
('Introductory general problem: same trials, different variables',.5),
('Introductory general problem: same trials, different variables',binom.pmf(1,3,.5)),
('Introductory general problem: same trials, different variables',geom.pmf(3,.5)),
('Advanced general problem: target versus interval',nbinom.pmf(2,2,.4)),
('Advanced general problem: target versus interval',poisson.sf(0,2)),
('One loan: a binary event',.07),('Five independent invoice payments',binom.pmf(4,5,.8)),
('First insurance sale',geom.sf(3,.25)),
('Third contract signed on visit five',nbinom.pmf(2,3,.4)),
('Claims in a half-day exposure',poisson.sf(1,1.5)),
('When the information cannot choose a count model',.1)]:
    answer(9,title,value)
close(F(1,10)**5,F('0.00001'))

# Required structure and navigation. The conventional toc anchor is shared
# only across independent documents; content labels must be Term 2 names.
files=sorted(HERE.glob('*.tex'))
require(len(files)==9,'Exactly nine activities')
for c in range(1,10):
    s=source(c)
    require(s.count('\\textbf{Questions/Tasks}')==8,f'C{c}: eight problems')
    require(s.count('\\subsubsection*{Complete worked solution}')==8,f'C{c}: eight solutions')
    require(s.count('\\textbf{Check.}')>=4,f'C{c}: four checks')
    require('Grade 10, Term 2' in s,f'C{c}: document term')
    require('Symbol & Value & Meaning in this problem' in s,f'C{c}: input table')
    require(all(label=='toc' or label.startswith(f'sec:t2-c{c}-')
                for label in re.findall(r'\\label\{([^}]+)\}',s)),f'C{c}: labels')
    for level in ['Foundational','Intermediate','Advanced']:
        group=s.split('\\section{'+level+' contextual practice}',1)[1].split('\\section{',1)[0]
        require(group.count('\\textbf{Questions/Tasks}')==2,f'C{c}: {level}')
print(f'PASS: {checks} independent numerical, PMF/CDF, support, graph and structure checks.')
