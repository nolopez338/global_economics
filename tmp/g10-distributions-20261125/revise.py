from pathlib import Path
from fractions import Fraction as F
from itertools import product, combinations
from collections import defaultdict
from math import comb
import re, json, hashlib

root=Path(__file__).resolve().parents[2]
work=Path(__file__).resolve().parent
folder=root/'book2026-2027/grade10/term_2/4-learning_evidences'
stem='G10_T2_L1_C1C2_exam'
ep=folder/(stem+'_1.tex'); sp=folder/(stem+'_solution_1.tex')
exam=ep.read_text(encoding='utf-8'); sol=sp.read_text(encoding='utf-8')
for p in [ep,sp]: (work/(p.name+'.before')).write_bytes(p.read_bytes())
protected=[p for p in (root/'book2026-2027/preamble').rglob('*') if p.is_file()]
protected += [folder/(stem+suffix) for suffix in ['.tex','.pdf','_solution.tex','_solution.pdf']]
(work/'protected.json').write_text(json.dumps({str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in protected},indent=2))
sections=re.split(r'(?=\\sectionScored\{)',sol)

def H(s): return r'\GTenHLProbability{'+str(s)+'}'
def V(s): return r'\GTenHLValue{'+str(s)+'}'
def O(s): return r'\GTenHLOutcome{'+str(s)+'}'
def C(s): return r'\HLCumulativeProbability{'+str(s)+'}'
def table(head,rows):
    return '\n\\begin{center}\n\\begin{tabular}{'+('c'*(head.count('&')+1))+'}\\toprule\n'+head+r'\\\midrule'+'\n'+'\n'.join(' & '.join(row)+r'\\' for row in rows)+'\n\\bottomrule\\end{tabular}\n\\end{center}\n'
def body(q,t,new):
    global sections
    s=sections[q]; start=s.index(r'\label{sol:q'+str(q)+'t'+str(t)+'}')
    start=s.index(r'\par\nopagebreak',start)+len(r'\par\nopagebreak')
    end=s.index('\\par\\smallskip\n\\noindent\\begin{minipage}',start)
    sections[q]=s[:start]+'\n\n'+new.strip()+'\n\n'+s[end:]
def replace_table(s,marker,new):
    a=s.rfind(r'\begin{center}',0,s.index(marker)); b=s.index(r'\end{center}',s.index(marker))+len(r'\end{center}')
    return s[:a]+new.strip()+s[b:]

# Question 1: independent Bernoulli probability changes to 3/10.
q=sections[1]
mapping={'0.4':'0.3','0.6':'0.7','2/5':'3/10','3/5':'7/10',
 '8/125':'27/1000','12/125':'63/1000','18/125':'147/1000','27/125':'343/1000',
 '54/125':'441/1000','36/125':'189/1000','0.064':'0.027','0.096':'0.063',
 '0.144':'0.147','0.216':'0.343','0.288':'0.189','28.8\\%':'18.9\\%',
 '27':'343','54':'441','36':'189','8':'27','125':'1000'}
q=re.sub(r'\\GTenHLProbability\{([^{}]*)\}',lambda m:H(mapping.get(m[1],m[1])),q)
q=q.replace('probability 0.4, or cancels it with probability 0.6','probability 0.3, or cancels it with probability 0.7')
sections[1]=q

# Question 2: replace both marginal distributions, then enumerate and group.
xs=[0,4,9]; pa=[F(3,10),F(4,10),F(3,10)]; pb=[F(5,10),F(2,10),F(3,10)]
q2=defaultdict(list)
rows=[]
for i,j in product(range(3),repeat=2):
    p=pa[i]*pb[j]; q2[xs[i]+xs[j]].append((xs[i],xs[j],p))
    rows.append(['$('+O(xs[i])+','+O(xs[j])+')$', '$'+H(str(float(pa[i])))+r'\cdot'+H(str(float(pb[j])))+'$', '$'+H(p)+'='+H(f'{float(p):.2f}')+'$'])
sections[2]=sections[2].replace('0.2, 0.5 and 0.3','0.3, 0.4 and 0.3').replace('0.4, 0.4 and 0.2','0.5, 0.2 and 0.3')
body(2,1,r'Each distributor has three possible outcomes, giving $3^2=9$ ordered pairs. Write each pair in first-distributor then second-distributor order, in USD. Independence permits multiplication of the two marginal probabilities.'+table('Ordered credit outcome (USD) & Product & Exact probability',rows)+r'Exhaustiveness check: $(0.3+0.4+0.3)(0.5+0.2+0.3)=1$. The ordered pairs are not equally likely.')
rows=[]
for x,items in sorted(q2.items()):
    rows.append(['$'+V(x)+'$', '$'+','.join('('+O(a)+','+O(b)+')' for a,b,p in items)+'$', '$'+'+'.join(H(p) for a,b,p in items)+'='+H(sum(p for a,b,p in items))+'$'])
body(2,2,r'Let $'+V('X')+r'$ be the total promotional credit, in USD. Add the two amounts in every ordered pair; distinct pairs with equal totals must be grouped.'+table('$'+V('x')+'$ (USD) & Ordered outcomes & Grouped probability',rows)+r'The support is $S_X=\{0,4,8,9,13,18\}$ USD. All masses are positive, their sum is $(15+26+8+24+18+9)/100=1$, and the PMF is zero elsewhere. Reversing a pair can preserve the monetary value while changing its probability.')
body(2,3,r'$P('+V('X')+'='+V(13)+')='+H('p_X(13)')+'='+H('3/25')+'+'+H('3/50')+'='+H('9/50')+'='+H('0.18')+'$. The bookshop receives exactly 13 USD with probability '+H(r'18\%')+r'; the qualifying pairs are $(4,9)$ and $(9,4)$.')

data={3:([0,3,6,10,15,21,29],[5,2,3,4,1,3,2],20),4:([0,3,7,11,16,22,34],[3,1,3,2,2,6,3],20),5:([0,3,7,12,18,27],[1,3,4,8,4,7],27),6:([0,6,12,14,18,28,30],[1,12,18,6,4,27,16],84)}
def checks(ns,d):
    return r'\Needspace{5\baselineskip}\textbf{PMF checks.}\begin{itemize}\item Every mass is positive.\item Normalization: $('+'+'.join(map(str,ns))+f')/{d}=1'+r'$.\item Set $p_X(x)=0$ outside the support. Bars use actual monetary spacing; gaps carry no mass.\end{itemize}'
def graph(q,cdf=False):
    xs,ns,d=data[q]; cum=[]; z=0
    for n in ns: z+=n; cum.append(z)
    ymax='.35' if q in [3,4] else '.65'
    opts=(f'keyaxis,width='+('.86' if cdf or q==6 else '.94')+r'\linewidth,height='+('7' if cdf else '5')+f'cm,xmin=-2,xmax={xs[-1]+2},ymin='+('-.07,ymax=1.1' if cdf else '0,ymax='+ymax)+',xtick={'+','.join(map(str,xs))+r'},xticklabel style={rotate=45,anchor=north east},ylabel={$'+(C('F_X(x)') if cdf else H('p_X(x)'))+r'$},yticklabel={$'+(C(r'\pgfmathprintnumber{\tick}') if cdf else H(r'\pgfmathprintnumber{\tick}'))+'$}'+(',ytick={0,.25,.5,.75,1}' if cdf else ''))
    lines=[r'\begin{tikzpicture}',r'\begin{axis}['+opts+']']
    if not cdf:
        width=.225 if q==6 else .45
        for x,n in zip(xs,ns): lines.append(r'\draw[fill=keyMassFill,draw=keyMassColor] '+f'(axis cs:{x-width:g},0) rectangle (axis cs:{x+width:g},{n}/{d});')
    else:
        lines.append(r'\addplot[keyCDFColor,thick,<-] coordinates {(-2,0)(0,0)};')
        for a,b,n in zip(xs,xs[1:],cum): lines.append(r'\addplot[keyCDFColor,thick] coordinates {'+f'({a},{n}/{d})({b},{n}/{d})'+'};')
        lines.append(r'\addplot[keyCDFColor,thick,->] coordinates {'+f'({xs[-1]},1)({xs[-1]+2},1)'+'};')
        for open_,values in [(True,[0]+cum[:-1]),(False,cum)]:
            lines.append(r'\addplot[keyCDFColor,only marks,mark=*,mark size='+('.8' if q==6 else '1.6')+'pt'+(',mark options={fill=white}' if open_ else '')+'] coordinates {'+''.join(f'({x},{n}/{d})' for x,n in zip(xs,values))+'};')
    return '\n'.join(lines+[r'\end{axis}\end{tikzpicture}'])
def pmf(q):
    xs,ns,d=data[q]
    t=table('$'+V('x')+'$ (USD) & $'+H('p_X(x)')+'$',[['$'+V(x)+'$','$'+H(f'{n}/{d}')+('='+H(F(n,d)) if str(F(n,d))!=f'{n}/{d}' else '')+'$'] for x,n in zip(xs,ns)])
    if q==6: return t+r'\begin{center}'+graph(q)+r'\end{center}'
    t=t.removeprefix('\n\\begin{center}\n').removesuffix('\\end{center}\n')
    return r'\begin{center}\begin{minipage}{.26\linewidth}\centering'+'\n'+t+r'\end{minipage}\hfill\begin{minipage}{.70\linewidth}\centering'+'\n'+graph(q)+r'\end{minipage}\end{center}'
def cdf(q):
    xs,ns,d=data[q]; cum=[]; z=0
    for n in ns: z+=n; cum.append(z)
    rows=[['$'+V('x')+'<'+V(xs[0])+'$','$'+C(0)+'$']]
    rows += [['$'+V(a)+r'\leq '+V('x')+'<'+V(b)+'$','$'+C(F(n,d))+'$'] for a,b,n in zip(xs,xs[1:],cum)]
    rows += [['$'+V('x')+r'\geq '+V(xs[-1])+'$','$'+C(1)+'$']]
    return (r'For $'+C('F_X(x)')+r'=P(X\leq x)$, add the masses in increasing monetary order. The successive cumulative numerators are $'+','.join(map(str,cum))+f'$, all over ${d}$.'+table('Cutoff interval (USD) & $'+C('F_X(x)')+'$',rows)+r'\begin{center}'+graph(q,True)+r'\end{center}'+r'\textbf{CDF checks.}\begin{itemize}\item The intervals cover every real cutoff, and every height lies in $[0,1]$.\item The heights never decrease.\item Each segment includes its left endpoint and excludes its right endpoint; the filled point gives the value at a jump, so the CDF is right-continuous.\item The lower-tail limit is 0 and the upper-tail limit is 1; the arrows extend both tails.\item Successive cumulative differences recover the PMF numerators $'+','.join(map(str,ns))+f'$ over ${d}$'+r'. Thus $F_X(a)-F_X(a^-)=p_X(a)$; unsupported cutoffs have zero jump and zero mass.\end{itemize}')
def final(q,lo,hi,desc):
    xs,ns,d=data[q]; text=[]
    allocation={3:'.25',4:'.25',5:'.5',6:'.75'}[q]
    text.append(r'\textbf{Allocation:} (i) 0'+allocation+r' points; (ii) 0'+allocation+' points.\n')
    for label,cut,op,condition,interpret in [('i',lo,'<',lambda x:x<lo,'below'),('ii',hi,r'\geq',lambda x:x>=hi,'at least')]:
        included=[(x,n) for x,n in zip(xs,ns) if condition(x)]; p=F(sum(n for x,n in included),d)
        text.append(r'\textbf{('+label+')} Include only $'+','.join(str(x) for x,n in included)+r'$ USD; '+('exclude' if label=='i' else 'include')+f' the boundary mass at {cut} USD.\n'+r'\['+'P('+V('X')+op+V(cut)+')='+ '+'.join(H(f'p_X({x})') for x,n in included)+r'=\frac{'+ '+'.join(str(n) for x,n in included)+'}{'+str(d)+'}='+H(p)+r'\approx '+H(f'{float(p):.6f}')+r'.\]'+'\n'+f'The {desc} is {interpret} {cut} USD with probability $'+H(p)+r'$, approximately $'+H(f'{100*float(p):.2f}'+r'\%')+'$.\n')
    return '\n'.join(text)

# Questions 3 and 4 retain eight nonuniform named outcomes and one grouped payout.
cats3=['Walking courier','Bicycle','Cargo bicycle','Motorcycle','Car','Van','Refrigerated van','Truck']
cats4=['No service','Remote diagnosis','Software reset','Minor repair','Major repair','Replacement','Store credit','Cash refund']
for q,cats,values,nums,old,new,desc in [
 (3,cats3,[0,0,3,6,10,15,21,29],[3,2,2,3,4,1,3,2],'0.10, 0.10, 0.15, 0.20, 0.15, 0.10, 0.10 and 0.10','0.15, 0.10, 0.10, 0.15, 0.20, 0.05, 0.15 and 0.10','handling fee for one produce crate'),
 (4,cats4,[0,3,7,11,16,22,22,34],[3,1,3,2,2,4,2,3],'0.20, 0.10, 0.15, 0.15, 0.10, 0.15, 0.05 and 0.10','0.15, 0.05, 0.15, 0.10, 0.10, 0.20, 0.10 and 0.15',"provider's payout for one claim")]:
    sections[q]=sections[q].replace(old,new)
    rows=[ [O(cat),'$'+H(f'{n/20:.2f}')+'='+H(f'{n}/20')+'$','$'+V(x)+'$'] for cat,x,n in zip(cats,values,nums)]
    intro='Let $'+V('X')+f'$ be the {desc}, in USD. Map all eight categories as follows.'+table('Category & Given probability & $'+V('X')+'$ (USD)',rows)
    if q==3: intro+=r'The distinct walking-courier and bicycle outcomes both pay zero, so $p_X(0)=3/20+2/20=5/20$. '
    else: intro+=r'Replacement and store credit are distinct outcomes with the same 22 USD payout, so $p_X(22)=4/20+2/20=6/20$. '
    intro+=r'Add probabilities because the categories are mutually exclusive. There are eight elementary outcomes and seven distinct monetary values. The support is $S_X=\{'+','.join(map(str,data[q][0]))+r'\}$ USD.'
    body(q,1,intro+pmf(q)+checks(data[q][1],20))
    body(q,2,cdf(q))
    body(q,3,final(q,10 if q==3 else 11,21 if q==3 else 22,desc))

# Question 5: alter the first multiplier, preserving the dependent normalization chain.
sections[5]=sections[5].replace('A 3 USD credit is twice as likely','A 3 USD credit is three times as likely')
intro=r'''Let $\GTenHLValue{X}$ be the account credit for one booking, in USD. Its support is $S_X=\{0,3,7,12,18,27\}$. Set $\GTenHLParameter{a}=P(X=0)$. Mutually exclusive categories permit adding probabilities in the combined likelihoods:
\begin{align*}
p_X(0)&=a,&p_X(3)&=3a,\\
p_X(7)&=a+3a=4a,&p_X(12)&=2(4a)=8a,\\
p_X(18)&=\tfrac12(8a)=4a,&p_X(27)&=3a+4a=7a.
\end{align*}
Normalization gives $a+3a+4a+8a+4a+7a=1$, hence $27a=1$ and $a=1/27$. All six probabilities are uniquely determined and positive. Each credit is a distinct monetary value.
'''
body(5,1,intro+pmf(5)+checks(data[5][1],27)+r'\textbf{Relationship check.} The numerators satisfy $3=3(1)$, $4=1+3$, $8=2(4)$, $4=8/2$, and $7=3+4$, reproducing all five verbal relationships.')
body(5,2,cdf(5)); body(5,3,final(5,12,18,'account credit for one booking'))

# Question 6: counts 3,4,2 retain nine tickets, nine compositions, and both aggregations.
sections[6]=sections[6].replace('four worth 0 USD each, three worth 6 USD each','three worth 0 USD each, four worth 6 USD each')
comps=[]
for c in range(3):
    for b in range(4-c):
        a=3-b-c; n=comb(3,a)*comb(4,b)*comb(2,c); face=6*b+14*c; bonus=8 if b and c else 0; y=face+bonus
        comps.append((a,b,c,n,face,bonus,y,min(y,30)))
rows=[]
for a,b,c,n,face,bonus,y,x in comps:
    rows.append(['$('+','.join(O(i) for i in [a,b,c])+')$',r'$\binom3{'+str(a)+r'}\binom4{'+str(b)+r'}\binom2{'+str(c)+'}='+str(n)+'$','$'+H(f'{n}/84')+'$','$'+V(face)+'$','$'+V(bonus)+'$',r'$\GTenHLSecond{'+str(y)+'}$','$'+V(x)+'$'])
intro=r'''Let $\GTenHLValue{X}$ be the final payout for one three-ticket subset, in USD. Label the distinct tickets $Z_1,Z_2,Z_3$, $L_1,\ldots,L_4$, and $H_1,H_2$, worth 0, 6 and 14 USD respectively. There are $\binom93=84$ equally likely unordered subsets, each with probability $1/84$.

A composition $(a,b,c)$ counts zero-, six- and fourteen-dollar tickets. It satisfies $a+b+c=3$, $0\leq a\leq3$, $0\leq b\leq4$ and $0\leq c\leq2$. Its subset count is $N(a,b,c)=\binom3a\binom4b\binom2c$ and its probability is $N(a,b,c)/84$. Let $I=1$ when $b\geq1$ and $c\geq1$, and 0 otherwise. First calculate $Y=6b+14c+8I$, then $X=\min\{Y,30\}$: the bonus is added once, before the cap.
\begingroup\renewcommand{\arraystretch}{1.35}
'''+table('$(a,b,c)$ & Subset count & Probability & Face sum & Bonus & $Y$ & $X$',rows)+r'''\endgroup
All monetary columns are in USD. Listing $c=0,1,2$ and each feasible $b$ gives all nine compositions. Their counts sum to $1+12+18+4+6+24+12+3+4=84$. Compositions are not equally likely: $(1,1,1)$ represents 24 subsets, while $(3,0,0)$ represents only one.

\textbf{Aggregation.} Below the cap, the 28 USD payout combines $(1,1,1)$ (24 subsets after the bonus) with $(1,0,2)$ (3 subsets without a bonus), giving $p_X(28)=(24+3)/84=27/84$. At the cap, adjusted amounts 34 and 42 USD from $(0,2,1)$ and $(0,1,2)$ combine, giving $p_X(30)=(12+4)/84=16/84$. Every other payout comes from one composition. Thus $S_X=\{0,6,12,14,18,28,30\}$ USD; the 28 USD payout stays below the cap.
\par\vspace{3mm}\secInicio[][sec:q6]
\clearpage\textbf{Question 6 --- Task 1 continued: grouped \GTenHLProbability{PMF} and graph}
'''
body(6,1,intro+pmf(6)+checks(data[6][1],84))
body(6,2,cdf(6)); body(6,3,final(6,14,28,'final payout for a uniformly selected three-ticket subset, after the bonus and cap'))

# Independent enumeration: physical subsets and outcome products verify the planned PMFs.
pmfs=[]
for q in [1,2]:
    dist=defaultdict(F)
    if q==1:
        for w in product('KC',repeat=3): dist[7*w.count('K')-5]+=F(3,10)**w.count('K')*F(7,10)**w.count('C')
    else:
        for i,j in product(range(3),repeat=2): dist[xs[i]+xs[j]]+=pa[i]*pb[j]
    pmfs.append(dict(sorted(dist.items())))
for q in range(3,7): pmfs.append(dict(zip(data[q][0],[F(n,data[q][2]) for n in data[q][1]])))
tickets=[0]*3+[6]*4+[14]*2; physical=defaultdict(int)
for ix in combinations(range(9),3):
    vals=[tickets[i] for i in ix]; physical[min(sum(vals)+(8 if 6 in vals and 14 in vals else 0),30)]+=1
assert {x:F(n,84) for x,n in sorted(physical.items())}==pmfs[5]
assert all(sum(p.values())==1 and min(p.values())>0 for p in pmfs)
expected=[F(189,1000),F(9,50),F(1,2),F(1,4),F(7,20),F(9,20),F(8,27),F(11,27),F(31,84),F(43,84)]
reference=[F(54,125),F(11,50),F(11,20),F(1,5),F(9,20),F(3,10),F(3,10),F(2,5),F(17,42),F(37,84)]
actual=[pmfs[0][9],pmfs[1][13]]
for q,lo,hi in [(3,10,21),(4,11,22),(5,12,18),(6,14,28)]: actual += [sum(p for x,p in pmfs[q-1].items() if x<lo),sum(p for x,p in pmfs[q-1].items() if x>=hi)]
assert actual==expected and all(a!=b for a,b in zip(actual,reference))
sol=''.join(sections)
# Write the verified solution before deriving the student's givens from it.
sp.write_text(sol,encoding='utf-8')
questions=re.split(r'(?=\\SubsectionBox\{)',exam)
for q in range(1,7):
    a=questions[q].index('\\QuestionLabel{q:'+str(q)+'}')+len('\\QuestionLabel{q:'+str(q)+'}')
    b=questions[q].index(r'\begin{enumerate}',a)
    prompt=sections[q].split('\n\n',2)[1]
    questions[q]=questions[q][:a]+'\n'+prompt+'\n\n'+questions[q][b:]
exam=''.join(questions); ep.write_text(exam,encoding='utf-8')
(work/'calculation-checks.json').write_text(json.dumps({'pmfs':[{str(x):str(p) for x,p in dist.items()} for dist in pmfs],'q6_compositions':comps,'finals':list(map(str,actual)),'reference_finals':list(map(str,reference))},indent=2))
print('Solution written first; student givens derived. All ten final probabilities differ:',list(map(str,actual)))
