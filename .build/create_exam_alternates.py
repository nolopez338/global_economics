from pathlib import Path
from fractions import Fraction as F
from itertools import product, combinations
from math import comb, prod
import re, json, hashlib, random, sys

ROOT=Path.cwd()
DEST=ROOT/'book/grade10/term_2/4-learning_evidences'
WORK=ROOT/'.build/g10_t2_l1_alternates_1_1_1_2'
WORK.mkdir(exist_ok=True)
EXAM=(DEST/'G10_T2_L1_C1C2_exam_1.tex').read_text(encoding='utf-8')
SOL=(DEST/'G10_T2_L1_C1C2_exam_solution_1.tex').read_text(encoding='utf-8')
names=[f'G10_T2_L1_C1C2_{kind}_1_{v}' for v in (1,2) for kind in ('exam','exam_solution')]
for name in names:
    collisions=list(ROOT.rglob(name+'.*'))
    if collisions and '--revise' not in sys.argv: raise RuntimeError('Collision: '+str(collisions))
protected=list(DEST.iterdir())+list((ROOT/'book/preamble').rglob('*'))
hashes={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in protected if p.is_file()}
if not (WORK/'protected_sha256.json').exists():
    (WORK/'protected_sha256.json').write_text(json.dumps(hashes,indent=2))

def frac(x):
    x=F(x)
    return str(x.numerator) if x.denominator==1 else f'{x.numerator}/{x.denominator}'
def dec(x): return f'{float(x):.6f}'.rstrip('0').rstrip('.')
def prob(x): return r'\GTenHLProbability{'+str(x)+'}'
def val(x): return r'\GTenHLValue{'+str(x)+'}'
def out(x): return r'\GTenHLOutcome{'+str(x)+'}'
def cdf(x): return r'\HLCumulativeProbability{'+str(x)+'}'
def moneyset(xs): return '$'+val('S_X')+r'=\{'+','.join(val(x) for x in xs)+r'\}$ USD.'
def result(p):
    p=F(p)
    terminating=p.denominator
    for d in (2,5):
        while terminating%d==0: terminating//=d
    eq='=' if terminating==1 else r'\approx'
    decimal=dec(p) if terminating==1 else f'{float(p):.4f}'
    percentage=dec(100*p) if terminating==1 else f'{float(p)*100:.2f}'
    return prob(frac(p))+eq+prob(decimal)+r'='+prob(percentage+r'\%')
def table(head,rows,spec=None):
    return '\n'+r'\begin{center}\begin{tabular}{'+(spec or 'c'*len(head))+r'}\toprule'+'\n'+' & '.join(head)+r'\\\midrule'+'\n'+'\n'.join(' & '.join(row)+r'\\[4pt]' for row in rows)+'\n'+r'\bottomrule\end{tabular}\end{center}'+'\n'
def nav(q): return '\n'+r'\par\vspace{3mm}\secInicio[][sec:q'+str(q)+']\n'
def page(q,txt): return nav(q)+r'\clearpage\textbf{Question '+str(q)+' --- '+txt+'}\n\n'
def pmfchecks(ps):
    return (r'\Needspace{5\baselineskip}\textbf{PMF checks.} All masses are positive. Normalization: $('
            +'+'.join(frac(p) for p in ps)+r')=1$. Set $p_X(x)=0$ outside the support; gaps carry no mass.'+'\n\n'+
            r'\textbf{Scoring note.} These explanatory positivity and normalization checks carry no separate points; omitting them does not reduce the task score.'+'\n')

SOURCE={
1:dict(p=list(map(F,['.2','.5','.8'])),unit=7,cost=5),
2:dict(p=list(map(F,['.3','.4','.3'])),r=list(map(F,['.5','.2','.3'])),values=[0,4,9]),
3:dict(p=list(map(F,['.15','.10','.10','.15','.20','.05','.15','.10'])),values=[0,6,10,21]),
4:dict(p=list(map(F,['.15','.05','.15','.10','.10','.20','.10','.15'])),values=[0,11,22,34]),
5:dict(ratios=[2,3,2,2],values=[0,12,18]),
6:dict(counts=[3,4,2],values=[0,6,14],bonus=8,cap=30)}
DATA={1:{
1:dict(p=list(map(F,['.5','.3','.7'])),unit=9,cost=6),
2:dict(values=[0,3,8]),
3:dict(p=list(map(F,['.05','.20','.20','.05','.10','.15','.20','.05'])),values=[0,4,9,18]),
4:dict(p=list(map(F,['.04','.06','.08','.12','.23','.27','.11','.09'])),values=[0,8,19,29]),
5:dict(ratios=[3,2,3,3],values=[0,9,16]),
6:dict(counts=[4,7,2],values=[0,4,10],bonus=6,cap=22)},
2:{
1:dict(p=list(map(F,['.25','.75','.5'])),unit=10,cost=4),
2:dict(values=[0,5,12]),
3:dict(p=[F(1,8)]*8,values=[0,5,12,24]),
4:dict(p=list(map(F,['.07','.09','.13','.09','.18','.22','.08','.14'])),values=[0,7,17,26]),
5:dict(ratios=[4,8,4,4],values=[0,7,15]),
6:dict(counts=[5,3,2],values=[0,5,12],bonus=7,cap=27)}}

def model(q,d):
    d=d.copy()
    if q==1:
        outcomes=list(product((1,0),repeat=3))
        ps=[prod(d['p'][i] if k else 1-d['p'][i] for i,k in enumerate(o)) for o in outcomes]
        xs=[d['unit']*sum(o)-d['cost'] for o in outcomes]
        labels=[''.join('K' if k else 'C' for k in o) for o in outcomes]
    elif q==2:
        outcomes=list(product(range(3),repeat=2))
        ps=[d['p'][a]*d['r'][b] for a,b in outcomes]
        xs=[d['values'][a]+d['values'][b] for a,b in outcomes]
        labels=[f'({d["values"][a]},{d["values"][b]})' for a,b in outcomes]
    elif q in (3,4):
        outcomes=list(range(8));ps=d['p'];xs=[x for x in d['values'] for _ in (0,1)];labels=d.get('labels',list('ABCDEFGH'))
    elif q==5:
        b,c,dd,f=d['ratios'];w=[1,b,c,dd*b,b,f*b,f*b];den=sum(w)
        d.update(weights=w,den=den)
        outcomes=list(range(7));ps=[F(x,den) for x in w];xs=[d['values'][i] for i in [0,0,1,1,2,2,2]];labels=list('ABCDEFG')
    else:
        outcomes=[(3,0,0),(2,1,0),(1,2,0),(0,3,0),(2,0,1),(1,1,1),(0,2,1),(1,0,2),(0,1,2)]
        a,b,c=d['counts'];den=comb(a+b+c,3)
        counts=[comb(a,i)*comb(b,j)*comb(c,k) for i,j,k in outcomes]
        faces=[sum(i*x for i,x in zip(o,d['values'])) for o in outcomes]
        bonuses=[d['bonus'] if j>=1 and k>=1 else 0 for i,j,k in outcomes]
        ys=[x+b for x,b in zip(faces,bonuses)];xs=[min(y,d['cap']) for y in ys]
        ps=[F(n,den) for n in counts];labels=[str(o).replace(' ','') for o in outcomes]
        d.update(den=den,subset_counts=counts,faces=faces,bonuses=bonuses,ys=ys)
        # Independent enumeration of physically distinct subsets.
        tickets=[v for n,v in zip(d['counts'],d['values']) for _ in range(n)]
        exhaustive={}
        for inds in combinations(range(len(tickets)),3):
            vs=[tickets[i] for i in inds];y=sum(vs)+(d['bonus'] if d['values'][1] in vs and d['values'][2] in vs else 0)
            x=min(y,d['cap']);exhaustive[x]=exhaustive.get(x,0)+1
        assert sorted(exhaustive)==sorted(set(xs))
        assert all(F(n,den)==sum(p for p,z in zip(ps,xs) if z==x) for x,n in exhaustive.items())
    support=sorted(set(xs));groups=[[i for i,x in enumerate(xs) if x==s] for s in support]
    masses=[sum((ps[i] for i in g),F(0)) for g in groups]
    cumulative=[sum(masses[:i+1],F(0)) for i in range(len(masses))]
    assert sum(ps)==sum(masses)==1 and all(p>0 for p in ps)
    d.update(outcomes=outcomes,ps=ps,xs=xs,labels=labels,support=support,groups=groups,masses=masses,cumulative=cumulative)
    return d

# Small rational marginals, retaining the source's equal first/third marginal.
prior=model(2,SOURCE[2])
for v in (1,2):
    found=False
    for a in [F(i,20) for i in range(2,9)]:
        for r0 in [F(i,20) for i in range(2,13)]:
            for r1 in [F(i,20) for i in range(2,13)]:
                r2=1-r0-r1
                if r2<=0 or len({r0,r1,r2})<3: continue
                candidate=model(2,dict(DATA[v][2],p=[a,1-2*a,a],r=[r0,r1,r2]))
                old=[model(2,SOURCE[2])]+([model(2,DATA[1][2])] if v==2 else [])
                if all(all(x!=y for x,y in zip(candidate[k],o[k])) for o in old for k in ('p','r','ps','masses')):
                    DATA[v][2].update(p=candidate['p'],r=candidate['r']);found=True;break
            if found:break
        if found:break
    assert found

# Contexts are independently chosen for every version and question.
titles={1:['Workshop registration income','Two utility bill rebates','Museum audio guide charges','Community sports assistance','Online course service credits','Garden fundraiser vouchers'],
        2:['Bicycle tour contribution','Two packaging return rewards','Festival cloakroom charges','Theatre audience reimbursements','Courier service goodwill credits','Animal shelter raffle coupons']}
for v in (1,2):
    DATA[v][3]['labels']=(['Members','Children','Students','Seniors','Visitors','Teachers','Groups','Guests'] if v==1 else ['Volunteers','Performers','Students','Seniors','Spectators','Vendors','Sponsors','Guests'])
    DATA[v][4]['labels']=(['No assistance','Advice','Training','Practice','Equipment','Travel','Voucher','Cash'] if v==1 else ['No adjustment','Apology','Seat change','Programme','Partial refund','Replacement','Voucher','Cash'])

def statements(v,models):
    qs={};cs={}
    d=models[1];p=', '.join(dec(x) for x in d['p']);u=d['unit'];c=d['cost']
    context,things=('A craft studio handles three workshop registrations','workshop registrations') if v==1 else ('A cycling guide handles three bicycle tour bookings','tour bookings')
    qs[1]=f'{context}. The three {things} are independent. Each is either kept or cancelled, two mutually exclusive and exhaustive outcomes. The keep probabilities for {things} 1, 2 and 3 are {p}, respectively. Each kept '+('registration' if v==1 else 'booking')+f' contributes {u} USD and each cancellation contributes no money. A fixed setup cost of {c} USD is then deducted once from the combined contribution. There are no other receipts or costs. Record the net contribution for the three {things}.'
    cs[1]=f'Calculate and interpret the probability that the net contribution is exactly {d["support"][2]} USD.'
    d=models[2];lo,hi=d['values'][1:];ps=', '.join(dec(x) for x in d['p']);rs=', '.join(dec(x) for x in d['r'])
    actor,agents,amount=('A neighbourhood centre','utility providers','rebate') if v==1 else ('A grocery shop','packaging suppliers','return reward')
    qs[2]=f'{actor} receives one {amount} from each of two {agents}. The {agents} award payments independently. Each has exactly three mutually exclusive possible outcomes: no payment, a {lo} USD payment, or an {hi} USD payment. For the first provider these probabilities are {ps}, respectively. For the second provider they are {rs}, respectively. Add both payments; there are no other adjustments. Record the total payment, keeping first-provider then second-provider order.'
    cs[2]=f'Calculate and interpret the probability that the total payment is exactly {lo+hi} USD.'
    for q in (3,4):
        d=models[q];labels=', '.join(d['labels'][:-1])+' or '+d['labels'][-1];ps=', '.join(dec(x) for x in d['p']);xs=', '.join(str(x) for x in d['xs'])
        if q==3:
            context='A museum issues one audio guide under exactly one of eight exhaustive, mutually exclusive visitor categories' if v==1 else 'A festival accepts one cloakroom item under exactly one of eight exhaustive, mutually exclusive attendee categories'
            qs[q]=f'{context}: {labels}. Their probabilities are {ps}, respectively. The corresponding fixed charges are {xs} USD, respectively. No other charges apply. Record the charge for this transaction.'
            cs[q]=f'Calculate and interpret (i) the probability that the charge is less than {d["support"][2]} USD and (ii) the probability that it is at least {d["support"][3]} USD.'
        else:
            context='A community sports fund classifies one assistance application' if v==1 else 'A theatre classifies one audience complaint'
            qs[q]=f'{context} in exactly one of eight exhaustive, mutually exclusive categories: {labels}. These eight named categories are the distinct outcomes in the sample space. Their probabilities are {ps}, respectively; do not assume equal likelihood. The corresponding payouts are {xs} USD, respectively. Count the voucher at its face value as a payout. Each payout is fixed for its category, and no additional payments apply. Record the payout for one case.'
            cs[q]=f'Calculate and interpret (i) the probability that the payout is less than {d["support"][1]} USD and (ii) the probability that it is at least {d["support"][2]} USD.'
    d=models[5];b,c,dd,f=d['ratios'];lo,hi=d['values'][1:]
    contexts=['A (course accessed on time); B (access reset requested); C (short access delay); D (duplicate charge corrected); E (alternative course accepted); F (later session accepted); G (course withdrawn by provider)',
              'A (parcel delivered on time); B (collection rescheduled); C (short transit delay); D (duplicate label corrected); E (alternative depot accepted); F (later delivery accepted); G (parcel returned by carrier)']
    qs[5]=('For one '+('enrolment, an online course provider' if v==1 else 'shipment, a courier company')+' records exactly one of seven distinct, mutually exclusive and exhaustive service-resolution outcomes: '+contexts[v-1]+f'. These named outcomes form the sample space. Outcomes A and B award 0 USD service credit; C and D award {lo} USD; E, F and G award {hi} USD. Thus seven outcomes map to three possible credit values. B is {b} times as likely as A; C is {c} times as likely as A; D is {dd} times as likely as B; E is as likely as B; F is {f} times as likely as E; G is as likely as F. There are no other payments or adjustments. Determine the outcome probabilities from these likelihood relationships and record the service credit.')
    cs[5]=f'Calculate and interpret (i) the probability that the service credit is less than {lo} USD and (ii) the probability that it is at least {hi} USD.'
    d=models[6];a,b,c=d['counts'];lo,hi=d['values'][1:];bonus=d['bonus'];cap=d['cap'];n=a+b+c
    context='A community garden fundraiser' if v==1 else 'An animal shelter raffle'
    qs[6]=f'{context} has {n} physically distinct prize '+('vouchers' if v==1 else 'coupons')+f': {a} worth 0 USD each, {b} worth {lo} USD each and {c} worth {hi} USD each. Choose a subset of three uniformly without replacement, so every subset of three physically distinct items has the same chance. Ignore selection order. First add the face values. Then add one bonus of {bonus} USD if the selected subset contains at least one {lo} USD item and at least one {hi} USD item; otherwise add no bonus. Finally, if this adjusted amount exceeds {cap} USD, pay only {cap} USD; otherwise pay the adjusted amount. No other payments or deductions apply. Record the final payout.'
    cs[6]=f'Calculate and interpret (i) the probability that the final payout is less than {hi} USD and (ii) the probability that it is at least {2*hi} USD.'
    return qs,cs

def pmftable(d,q):
    rows=[]
    for x,g,p in zip(d['support'],d['groups'],d['masses']):
        labels=', '.join(('$'+out(d['labels'][i])+'$') if q in (1,2,6) else out(d['labels'][i]) for i in g)
        terms='+'.join(prob(frac(d['ps'][i])) for i in g)
        rows.append([labels,'$'+val(x)+'$',r'$\begin{aligned}[t]p_X('+val(x)+r')&='+terms+r'\\&='+result(p)+r'\end{aligned}$'])
    return table(['Complete outcomes','$'+val('x')+'$ (USD)','Grouped '+prob('PMF')],rows,r'@{}p{.30\linewidth}c p{.54\linewidth}@{}')

def axisoptions(d):
    xs=d['support'];return f'xmin={xs[0]-2},xmax={xs[-1]+2},xtick={{'+','.join(map(str,xs))+r'},xticklabel style={rotate=45,anchor=north east}'
def pmfgraph(d):
    s=r'\begin{center}\begin{tikzpicture}\begin{axis}[keyaxis,width=.86\linewidth,height=5cm,'+axisoptions(d)+r',ymin=0,ymax=.7,ylabel={$\GTenHLProbability{p_X(x)}$}]'+'\n'
    for x,p in zip(d['support'],d['masses']):
        s+=r'\draw[fill=keyMassFill,draw=keyMassColor] (axis cs:'+str(x-.225)+',0) rectangle (axis cs:'+str(x+.225)+','+frac(p)+');\n'
    return s+r'\end{axis}\end{tikzpicture}\end{center}'+'\n'

def steps(d,combined=False):
    xs=d['support'];cs=d['cumulative'];color='keyStep' if combined else 'keyCDFColor,thick'
    s=r'\addplot['+color+r',<-] coordinates {('+str(xs[0]-2)+',0)('+str(xs[0])+',0)};\n'
    for i in range(len(xs)-1):s+=r'\addplot['+color+r'] coordinates {('+str(xs[i])+','+frac(cs[i])+')('+str(xs[i+1])+','+frac(cs[i])+')};\n'
    s+=r'\addplot['+color+r',->] coordinates {('+str(xs[-1])+',1)('+str(xs[-1]+2)+',1)};\n'
    for filled in (False,True):
        style=('keyIncluded' if filled else 'keyExcluded') if combined else 'keyCDFColor,only marks,mark=*,mark size=1pt'+('' if filled else ',mark options={fill=white}')
        s+=r'\addplot['+style+'] coordinates {'+''.join('('+str(x)+','+frac(cs[i] if filled else (cs[i-1] if i else 0))+')' for i,x in enumerate(xs))+'};\n'
    return s

def cdfwork(q,d):
    xs=d['support'];ps=d['masses'];cs=d['cumulative']
    s=r'For $'+cdf('F_X(x)')+r'=P(X\leq x)$, add the masses in increasing monetary order.'+'\n\n'
    rows=[['$x<'+val(xs[0])+'$',r'No included support values','$'+cdf(0)+'$']]
    for i,x in enumerate(xs):
        interval=val(x)+r'\leq x'+('<'+val(xs[i+1]) if i+1<len(xs) else '')
        terms=[prob(frac(p)) for p in ps[:i+1]]
        chunks=['+'.join(terms[j:j+4]) for j in range(0,len(terms),4)]
        calculation=r'$\begin{aligned}[t]&'+(r'\\&{}+'.join(chunks))+r'\end{aligned}$'
        rows.append(['$'+interval+'$',calculation,'$'+cdf(frac(cs[i]))+'$'])
    s+=table(['Cutoff interval (USD)','Cumulative calculation','$'+cdf('F_X(x)')+'$'],rows,r'@{}l l c@{}')
    s+=r'\begin{center}\begin{tikzpicture}\begin{axis}[keyaxis,width=.86\linewidth,height=7cm,'+axisoptions(d)+r',ymin=-.07,ymax=1.1,ytick={0,.25,.5,.75,1},ylabel={$\HLCumulativeProbability{F_X(x)}$}]'+'\n'+steps(d)+r'\end{axis}\end{tikzpicture}\end{center}'
    s+=page(q,'Task 2 continued: comparison')+r'\textbf{Same distribution: CDF above, PMF below.}'+'\n'
    s+=r'\begin{center}\begin{minipage}{\linewidth}\centering\begin{tikzpicture}'+'\n'+r'\pgfplotsset{keySupport/.style={'+axisoptions(d)+r'}}'+'\n'
    s+=r'\begin{axis}[keyCombined,keySupport,name=keyTop,anchor=south west,ylabel={$\HLCumulativeProbability{F_X(x)}$}]'+'\n'
    for i,(x,p) in enumerate(zip(xs,ps)):s+=r'\keyPhantom{'+str(x)+'}{'+frac(p)+'}{'+frac(cs[i-1] if i else 0)+'}\n'
    s+=steps(d,True)+r'\end{axis}'+'\n'
    s+=r'\begin{axis}[keyCombined,keySupport,at={(keyTop.south west)},anchor=north west,yshift=-1.35cm,ylabel={$\GTenHLProbability{p_X(x)}$}]'+'\n'
    for x,p in zip(xs,ps):s+=r'\keyMass{'+str(x)+'}{'+frac(p)+'}\n'
    s+=r'\addlegendimage{keyStep}\addlegendentry{Top: CDF steps}'+'\n'+r'\addlegendimage{keyPhantom,mark=*}\addlegendentry{Top: PMF shadows (jumps)}'+'\n'+r'\addlegendimage{keyMass,mark=*}\addlegendentry{Bottom: PMF stems}'+'\n'+r'\addlegendimage{keyCorrespondence}\addlegendentry{Midpoint correspondence}'+'\n'+r'\end{axis}'+'\n'
    for x in xs:s+=r'\keyCorrespondence{'+str(x)+'}\n'
    s+=r'\end{tikzpicture}\end{minipage}\end{center}\keyConnectionReading'+'\n\n'
    s+=r'\textbf{CDF checks.}\begin{itemize}\item The intervals cover every real cutoff; all heights lie in $[0,1]$ and never decrease.\item Each segment includes its left endpoint and excludes its right endpoint. Filled endpoints give the values at jumps, so the CDF is right-continuous.\item The lower-tail limit is 0 and the upper-tail limit is 1; arrows extend both tails.\item Successive differences recover the PMF: '
    s+='$'+',\quad '.join(frac(cs[i])+'-'+frac(cs[i-1] if i else 0)+'='+frac(p) for i,p in enumerate(ps))+r'$. Thus $F_X(a)-F_X(a^-)=p_X(a)$; unsupported cutoffs have zero jump and zero mass.\end{itemize}'+'\n'
    return s

def cwork(q,d):
    xs=d['support'];ps=d['masses']
    if q<=2:
        i=2 if q==1 else 4;g=d['groups'][i];p=ps[i]
        terms='+'.join(prob(frac(d['ps'][j])) for j in g) if q==2 else prob(frac(p))
        return ('$P('+val('X')+'='+val(xs[i])+')=p_X('+val(xs[i])+')='+terms+'='+result(p)+'$.\n\n'+
                f'The '+('net contribution' if q==1 else 'total payment')+f' is exactly {xs[i]} USD with probability $'+prob(frac(p))+r'$. This occurs exactly for '+(', '.join('$'+out(d['labels'][j])+'$' for j in g))+'.\n')
    indices=([0,1],[3]) if q==3 else (([0],[2,3]) if q==4 else (([0],[2]) if q==5 else ([0,1,2],[5,6])))
    thresholds=(xs[2],xs[3]) if q==3 else ((xs[1],xs[2]) if q in (4,5) else (xs[3],xs[5]))
    s=''
    for k,(inds,cut) in enumerate(zip(indices,thresholds)):
        relation='<' if k==0 else r'\geq';words='below' if k==0 else 'at least';p=sum((ps[i] for i in inds),F(0))
        s+=r'\textbf{('+('i' if k==0 else 'ii')+')} Include only $'+','.join(val(xs[i]) for i in inds)+'$ USD; '+('exclude' if k==0 else 'include')+f' the boundary mass at {cut} USD.\n'
        s+=r'\[\begin{aligned}P('+val('X')+relation+val(cut)+r')&='+'+'.join('p_X('+val(xs[i])+')' for i in inds)+r'\\&='+'+'.join(prob(frac(ps[i])) for i in inds)+r'\\&='+result(p)+r'.\end{aligned}\]'+'\n'
        s+=f'The '+('charge' if q==3 else ('payout' if q in (4,6) else 'service credit'))+f' for one '+('selected three-item subset after the bonus and cap' if q==6 else 'case')+f' is {words} {cut} USD with probability $'+prob(frac(p))+f'$, approximately {float(p)*100:.2f}'+r'\%.'+'\n\n'
    return s

def task1(q,d):
    if q==1:
        u,c=d['unit'],d['cost']
        return ('Let $'+val('X')+'$ be the net contribution from the three '+d['things']+', in '+val('USD')+'. If $'+r'\GTenHLSecond{N}'+'$ is the number kept,\n'+r'\['+val('X')+'='+val(u)+r'\GTenHLSecond{N}-'+val(c)+r'.\]'+'\n'+
                r'Since $N\in\{0,1,2,3\}$, the monetary values are $'+',\quad '.join(f'{u}({n})-{c}={u*n-c}' for n in range(4))+'$ USD.\n\n'+moneyset(d['support'])+'\nA negative contribution means the setup cost exceeds receipts.\n')
    if q==2:
        vs=d['values']
        return ('Let $'+val('X')+'$ be the sum of the two providers\' payments, in '+val('USD')+'. Each payment belongs to $\\{'+','.join(map(str,vs))+r'\}$ USD. Add the two payments for each ordered outcome:'+'\n'+r'\[\begin{array}{lll}'+('\\\\'+'\n').join('&'.join(f'{a}+{b}={a+b}' for b in vs) for a in vs)+r'.\end{array}\]'+'\nRepeated sums appear only once in the support. '+moneyset(d['support'])+'\n')
    s='Let $'+val('X')+'$ be the '+d['quantity']+', in '+val('USD')+'. '+moneyset(d['support'])+'\n\n'
    if q in (3,4):
        s+='The eight distinct categories map to four monetary values; probabilities are supplied, not assumed equal.\n'
        s+=table(['Category','Given probability','$'+val('X')+'$ (USD)'],[[out(label),'$'+prob(dec(p))+'='+prob(frac(p))+'$','$'+val(x)+'$'] for label,p,x in zip(d['labels'],d['ps'],d['xs'])])
    if q==5:
        b,c,dd,f=d['ratios'];w=d['weights'];den=d['den']
        s+=r'The sample space is $\Omega=\{A,B,C,D,E,F,G\}$. Set $\GTenHLParameter{a}=P(A)$, the baseline outcome probability, not the grouped mass $p_X(0)$.'+'\n'
        s+=r'\begin{align*}P(A)&=a,&P(B)&='+str(b)+'a,&P(C)&='+str(c)+r'a,\\P(D)&='+str(dd)+'P(B)='+str(w[3])+'a,&P(E)&=P(B)='+str(b)+r'a,\\P(F)&='+str(f)+'P(E)='+str(w[5])+'a,&P(G)&=P(F)='+str(w[6])+r'a.\end{align*}'+'\n'
        s+='Normalize over all seven exhaustive outcomes:\n'+r'\['+'+'.join(('a' if i==1 else str(i)+'a') for i in w)+f'=1,\qquad {den}a=1,\qquad '+r'\GTenHLParameter{a}=\frac1{'+str(den)+r'}.\]'+'\n'
        s+=table(['Named outcome','Outcome probability','$'+val('X')+'$ (USD)'],[[out(label),'$'+str(ww)+r'\GTenHLParameter{a}='+prob(frac(p))+'$','$'+val(x)+'$'] for label,ww,p,x in zip(d['labels'],w,d['ps'],d['xs'])])
    if q==6:
        a,b,c=d['counts'];lo,hi=d['values'][1:];den=d['den'];bonus,cap=d['bonus'],d['cap']
        s+=f'Label the distinct items $Z_1,\\ldots,Z_{a}$, $L_1,\\ldots,L_{b}$ and $H_1,H_2$, worth 0, {lo} and {hi} USD respectively. There are $\\binom{{{a+b+c}}}3={den}$ equally likely unordered subsets, each with probability $1/{den}$.\n\n'
        s+=f'A composition $(a,b,c)$ counts zero-, {lo}- and {hi}-dollar items. It satisfies $a+b+c=3$, $0\\leq a\\leq {a}$, $0\\leq b\\leq {b}$ and $0\\leq c\\leq {c}$. Its count is $N(a,b,c)=\\binom{{{a}}}a\\binom{{{b}}}b\\binom{{{c}}}c$ and its probability is $N(a,b,c)/{den}$. Let $I=1$ when $b\\geq1$ and $c\\geq1$, and 0 otherwise. First calculate $Y={lo}b+{hi}c+{bonus}I$, then $X=\\min\\{{Y,{cap}\\}}$: add the bonus once before the cap.\n'
        rows=[]
        for o,n,p,face,bon,y,x in zip(d['outcomes'],d['subset_counts'],d['ps'],d['faces'],d['bonuses'],d['ys'],d['xs']):
            count=''.join(r'\binom{'+str(pop)+'}{'+str(k)+'}' for pop,k in zip(d['counts'],o))+'='+str(n)
            rows.append(['$'+out(str(o).replace(' ',''))+'$','$'+count+'$','$'+prob(frac(p))+'$','$'+val(face)+'$','$'+val(bon)+'$','$'+r'\GTenHLSecond{'+str(y)+'}$','$'+val(x)+'$'])
        s+=table(['$(a,b,c)$','Subset count','Probability','Face sum','Bonus','$Y$','$X$'],rows)
        s+=f'All monetary columns are in USD. Listing $c=0,1,2$ and all feasible $b$ gives the nine compositions. Counts sum to $'+ '+'.join(map(str,d['subset_counts']))+f'={den}$. Compositions are not equally likely: $(1,1,1)$ represents {d["subset_counts"][5]} subsets, while $(3,0,0)$ represents {d["subset_counts"][0]}.\n\n'
        s+=f'\\textbf{{Aggregation.}} Below the cap, {2*hi} USD combines $(1,1,1)$ after its bonus with $(1,0,2)$ without a bonus: $({d["subset_counts"][5]}+{d["subset_counts"][7]})/{den}={frac(d["masses"][5])}$. At the cap, adjusted amounts {d["ys"][6]} and {d["ys"][8]} USD from $(0,2,1)$ and $(0,1,2)$ combine: $({d["subset_counts"][6]}+{d["subset_counts"][8]})/{den}={frac(d["masses"][6])}$. Every other payout comes from one composition; {2*hi} USD stays below the cap.\n'
    s+=page(q,'Task 1 continued: grouped '+prob('PMF')+' and graph')+pmftable(d,q)+pmfgraph(d)+pmfchecks(d['masses'])
    if q==5:
        w=d['weights'];b,c,dd,f=d['ratios']
        s+=r'\textbf{Relationship check.} The outcome numerators satisfy $'+f'{w[1]}={b}(1),\ {w[2]}={c}(1),\ {w[3]}={dd}({w[1]}),\ {w[4]}={w[1]},\ {w[5]}={f}({w[4]}),\ {w[6]}={w[5]}'+ '$, reproducing all six relationships.\n'
    return s

def c1outcomes(q,d):
    rows=[];s=''
    if q==1:
        s=r'Write $'+out('K')+'$ for kept and $'+out('C')+'$ for cancelled. Each triple follows the stated order. Before multiplying, find each complementary probability:\n'+r'\[\begin{aligned}'
        s+=('\\\\'+'\n').join(f'P(C_{i+1})&=1-P(K_{i+1})=1-{dec(p)}='+prob(dec(1-p)) for i,p in enumerate(d['p']))+r'.\end{aligned}\]'+'\n'
        s+=r'There are $2^3=8$ ordered complete outcomes. Independence permits products of three probabilities, each using its own trial probability.'+'\n'
    else:s+='Each provider has three possible outcomes, giving $3^2=9$ ordered pairs. Preserve first-provider then second-provider order. Independence permits multiplication of two marginal probabilities.\n'
    for o,label,p,x in zip(d['outcomes'],d['labels'],d['ps'],d['xs']):
        operands=([d['p'][i] if k else 1-d['p'][i] for i,k in enumerate(o)] if q==1 else [d['p'][o[0]],d['r'][o[1]]])
        rows.append(['$'+out(label)+'$','$'+r'\cdot'.join(prob(dec(k)) for k in operands)+'$','$'+result(p)+'$','$'+val(x)+'$'])
    s+=table(['Ordered outcome','Probability calculation','Exact probability','$'+val('X')+'$ (USD)'],rows)
    marg=[d['p'],[1-x for x in d['p']]] if q==1 else [d['p'],d['r']]
    expression=''.join('('+dec(p)+'+'+dec(1-p)+')' for p in d['p']) if q==1 else ''.join('('+'+'.join(dec(p) for p in mm)+')' for mm in marg)
    s+='Exhaustiveness check: $'+expression+'=1$; the complete outcome probabilities sum to 1. Outcomes are not equally likely.\n'
    s+=page(q,'Task 2 (b) continued: grouped '+prob('PMF'))
    s+=r'For one complete outcome $\omega$, $P(\{\omega\})$ is its probability. Add the probabilities of all outcomes mapping to the same monetary value: $p_X(x)=\sum_{\omega:X(\omega)=x}P(\{\omega\})$.'+'\n'
    return s+pmftable(d,q)+pmfchecks(d['masses'])

def replace_task(section,q,t,body):
    start=section.index(r'\label{sol:q'+str(q)+'t'+str(t)+'}')
    begin=section.index(r'\par\nopagebreak',start)+len(r'\par\nopagebreak')
    end=section.index(r'\par\smallskip'+'\n'+r'\noindent\begin{minipage}{\linewidth}\centering'+'\n'+r'\textbf{Proposed partial credit.}',begin)
    # Retain source subpart allocations before the worked answer.
    prefix=''
    if t==3 and q>=3:
        alloc={3:'0.25',4:'0.25',5:'0.5',6:'0.75'}[q]
        prefix=r'\textbf{Allocation:} (i) '+alloc+' points; (ii) '+alloc+' points.\n\n'
    return section[:begin]+'\n\n'+prefix+body+'\n\n'+section[end:]

# Every model and every corresponding operation is recorded, including operands.
def trace(q,d):
    steps=[]
    def add(role,op,operands,result,dependencies='',reason=''):
        steps.append(dict(role=role,operation=op,operand_count=len(operands),operands=list(map(str,operands)),result=str(result),dependencies=dependencies,reasoning=reason))
    if q==1:
        for i,p in enumerate(d['p']):add(f'complement.{i}','subtract',[1,p],1-p,'given trial p','Complement of mutually exclusive exhaustive outcomes')
        for i,n in enumerate(range(4)):
            add(f'support.multiply.{i}','multiply',[d['unit'],n],d['unit']*n,'unit and kept count')
            add(f'support.subtract.{i}','subtract',[d['unit']*n,d['cost']],d['support'][i],'support.multiply and fixed cost')
    if q in (1,2):
        for i,o in enumerate(d['outcomes']):
            operands=[d['p'][j] if k else 1-d['p'][j] for j,k in enumerate(o)] if q==1 else [d['p'][o[0]],d['r'][o[1]]]
            add(f'outcome.product.{i}','multiply',operands,d['ps'][i],'marginals/complements','Independence')
            if q==2:add(f'outcome.money.{i}','add',[d['values'][o[0]],d['values'][o[1]]],d['xs'][i],'given two payments')
    if q==5:
        b,c,dd,f=d['ratios'];w=d['weights']
        for i,ops in [(1,[b,1]),(2,[c,1]),(3,[dd,w[1]]),(5,[f,w[4]])]:add(f'weight.{i}','multiply',ops,w[i],'A for B,C; B for D; E for F','Likelihood dependency')
        for i,j in [(4,1),(6,5)]:add(f'weight.{i}','copy',[w[j]],w[i],f'weight.{j}','Equal likelihood')
        add('normalization.coefficient','add',w,d['den'],'all seven weights','Exhaustive outcomes')
        add('normalization.solve','divide',[1,d['den']],F(1,d['den']),'normalization.coefficient','Solve denominator times a = 1')
        for i,w in enumerate(w):add(f'probability.{i}','multiply',[w,F(1,d['den'])],d['ps'][i],'weight and solved baseline')
    if q==6:
        add('population','add',d['counts'],sum(d['counts']),'given populations')
        add('denominator','choose',[sum(d['counts']),3],d['den'],'population and fixed selection size','Uniform unordered sampling without replacement')
        for i,o in enumerate(d['outcomes']):
            factors=[]
            for j,(n,k) in enumerate(zip(d['counts'],o)):
                factor=comb(n,k);factors.append(factor);add(f'composition.{i}.choose.{j}','choose',[n,k],factor,'population and composition')
            add(f'composition.{i}.count','multiply',factors,d['subset_counts'][i],'three binomial factors')
            add(f'composition.{i}.probability','divide',[d['subset_counts'][i],d['den']],d['ps'][i],'composition count and denominator')
            for j in (1,2):add(f'composition.{i}.face.term.{j}','multiply',[d['values'][j],o[j]],d['values'][j]*o[j],'face value and composition count')
            add(f'composition.{i}.face','add',[d['values'][1]*o[1],d['values'][2]*o[2]],d['faces'][i],'two face terms')
            add(f'composition.{i}.bonus.term','multiply',[d['bonus'],int(o[1]>0 and o[2]>0)],d['bonuses'][i],'bonus and indicator','Both positive-value categories present')
            add(f'composition.{i}.adjust','add',[d['faces'][i],d['bonuses'][i]],d['ys'][i],'face and bonus','Bonus before cap')
            add(f'composition.{i}.cap','minimum',[d['ys'][i],d['cap']],d['xs'][i],'adjusted amount and cap')
    for i,g in enumerate(d['groups']):add(f'group.{i}','add' if len(g)>1 else 'copy',[d['ps'][j] for j in g],d['masses'][i],','.join('outcome.'+str(j) for j in g),'Group equal final monetary values')
    add('pmf.normalization','add',d['masses'],1,'all grouped masses','Explanatory unscored check')
    if q>=3:
        for i,c in enumerate(d['cumulative']):add(f'cdf.{i}','add' if i else 'copy',d['masses'][:i+1],c,'group.0 through group.'+str(i),'Increasing support; include left boundary')
        for i,p in enumerate(d['masses']):add(f'jump.{i}','subtract',[d['cumulative'][i],d['cumulative'][i-1] if i else F(0)],p,'CDF adjacent heights','CDF jump equals PMF mass')
    inds=([2],) if q==1 else (([4],) if q==2 else (([0,1],[3]) if q==3 else (([0],[2,3]) if q==4 else (([0],[2]) if q==5 else ([0,1,2],[5,6])))))
    for i,g in enumerate(inds):add(f'answer.{i}','add' if len(g)>1 else 'copy',[d['masses'][j] for j in g],sum((d['masses'][j] for j in g),F(0)),'selected grouped masses','Strict lower boundary excluded; inclusive upper boundary included')
    return steps

allmodels={0:{q:model(q,d) for q,d in SOURCE.items()}}
for v in (1,2):allmodels[v]={q:model(q,d) for q,d in DATA[v].items()}
traces={v:{q:trace(q,d) for q,d in ms.items()} for v,ms in allmodels.items()}
repeats=[]
for q in range(1,7):
    source=allmodels[0][q]
    assert all(allmodels[v][q]['groups']==source['groups'] for v in (1,2))
    # Preserve every PMF equality and ordering relationship.
    for v in ((1,2) if q in (1,3,4,5) else ()):
        for i,j in combinations(range(len(source['masses'])),2):
            assert (source['masses'][i]>source['masses'][j])-(source['masses'][i]<source['masses'][j]) == (allmodels[v][q]['masses'][i]>allmodels[v][q]['masses'][j])-(allmodels[v][q]['masses'][i]<allmodels[v][q]['masses'][j]), (q,v,i,j)
    for triplet in zip(*(traces[v][q] for v in (0,1,2))):
        assert len({(t['role'],t['operation'],t['operand_count'],t['dependencies'],t['reasoning']) for t in triplet})==1
        for kind,values in [('result',[t['result'] for t in triplet])]+[(f'operand.{i}',[t['operands'][i] for t in triplet]) for i in range(triplet[0]['operand_count'])]:
            if len(set(values))<3:repeats.append(dict(question=q,role=triplet[0]['role'],field=kind,values=values))
(WORK/'procedure_operand_comparison.json').write_text(json.dumps(traces,indent=2))
(WORK/'numerical_repetitions.json').write_text(json.dumps(repeats,indent=2))

for v in (1,2):
    models=allmodels[v];qs,cs=statements(v,models)
    models[1]['things']='workshop registrations' if v==1 else 'tour bookings'
    for q in (3,4,5,6):models[q]['quantity']={3:'charge for one transaction',4:'payout for one case',5:'service credit for one enrolment' if v==1 else 'service credit for one shipment',6:'final payout for one three-item subset'}[q]
    chunks=re.split(r'(?=\\sectionScored\{)',SOL)
    assert len(chunks)==7
    sections=[]
    for q,section in enumerate(chunks[1:],1):
        # Question statements are established in the solution first.
        intro_end=section.index(r'\Needspace{8\baselineskip}')
        heading=r'\sectionScored{'+titles[v][q-1]+'}{'+('C1' if q<=2 else 'C2')+r'-\sml{'+str([3,3,2,2,4,6][q-1])+'}}{sec:q'+str(q)+'}\n\n'
        section=heading+qs[q]+'\n\n'+section[intro_end:]
        for t in (1,2,3):
            body=(task1(q,models[q]) if t==1 else ((c1outcomes(q,models[q]) if q<=2 else cdfwork(q,models[q])) if t==2 else cwork(q,models[q])))
            section=replace_task(section,q,t,body)
        # Source task (c) prompt and marking row are updated to the verified new question.
        label=section.index(r'\label{sol:q'+str(q)+'t3}')
        a=section.index(r'\noindent\textbf{\boldmath ',label)+len(r'\noindent\textbf{\boldmath ')
        b=section.index(r'}\par\nopagebreak',a)
        section=section[:a]+cs[q]+section[b:]
        if q<=2:
            old=9 if q==1 else 13;new=models[q]['support'][2 if q==1 else 4]
            section=section.replace(f'Selecting the correct mass at $X={old}$',f'Selecting the correct mass at $X={new}$')
        sections.append(section)
    sol=chunks[0].replace('% Alternate 1, derived directly from the original exam-solution pair.',f'% Alternate 1_{v}, derived directly from the explicitly supplied source pair.')+''.join(sections)
    # Read-back verifies complete solution, exact statements, marks and retained rubrics.
    solpath=DEST/f'G10_T2_L1_C1C2_exam_solution_1_{v}.tex'
    with solpath.open('w' if '--revise' in sys.argv else 'x',encoding='utf-8',newline='\n') as f:f.write(sol)
    readback=solpath.read_text(encoding='utf-8')
    assert all(readback.count(qs[q])==1 and cs[q] in readback for q in range(1,7))
    assert readback.count(r'\textbf{Proposed partial credit.}')==SOL.count(r'\textbf{Proposed partial credit.}')==18
    assert readback.count(r'\label{sol:q')==18
    # Only now derive the student exam from the verified solution statements.
    exam=EXAM.replace('% Alternate 1, derived from the verified alternate worked solution.',f'% Alternate 1_{v}, derived from its verified worked solution.')
    starts=list(re.finditer(r'\\SubsectionBox\{(?!\*)',exam))
    assert len(starts)==6
    for q in range(6,0,-1):
        start=starts[q-1].start();end=starts[q].start() if q<6 else exam.index(r'\end{multicols*}')
        section=exam[start:end]
        h_end=section.index(r'\QuestionLabel')
        section=r'\SubsectionBox{'+titles[v][q-1]+r'\score{'+('C1' if q<=2 else 'C2')+r'-\sml{'+str([3,3,2,2,4,6][q-1])+'}}}\n'+section[h_end:]
        a=section.index('\n',section.index(r'\QuestionLabel'))+1;b=section.index('\n\nComplete general tasks',a)
        section=section[:a]+qs[q]+section[b:]
        a=section.index(r'\item ')+len(r'\item ');b=section.index(r' \sscore',a)
        section=section[:a]+cs[q]+section[b:]
        exam=exam[:start]+section+exam[end:]
    lo,hi=models[6]['values'][1:]
    exam=exam.replace('Counts (0,6,14)',f'Counts (0,{lo},{hi})')
    # Uniform blank axes retain the source geometry; fit new monetary ranges.
    for q,oldrange in [(3,30),(4,45),(5,30),(6,40)]:
        newrange=((models[q]['support'][-1]+9)//5)*5+5
        exam=exam.replace(f'\\DistributionBlock{{{q}}}'+{3:'{4}{5}',4:'{4}{5}',5:'{3}{4}',6:'{7}{8}'}[q]+f'{{{oldrange}}}',f'\\DistributionBlock{{{q}}}'+{3:'{4}{5}',4:'{4}{5}',5:'{3}{4}',6:'{7}{8}'}[q]+f'{{{newrange}}}')
    assert all(exam.count(qs[q])==1 and cs[q] in exam for q in range(1,7))
    assert r'\GTenHL' not in exam
    path=DEST/f'G10_T2_L1_C1C2_exam_1_{v}.tex'
    with path.open('w' if '--revise' in sys.argv else 'x',encoding='utf-8',newline='\n') as f:f.write(exam)
    (WORK/f'version_{v}_statements.json').write_text(json.dumps({'questions':qs,'task_c':cs},indent=2))
    print('Wrote verified solution, then exam:',v)

(WORK/'models.json').write_text(json.dumps(allmodels,indent=2,default=str))
print('Repeated corresponding fields requiring justification:',len(repeats))
print('Protected artifacts:',len(hashes))
