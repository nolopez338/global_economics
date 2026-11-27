from pathlib import Path
import re
from fractions import Fraction
from itertools import product, accumulate

root=Path('book/grade10/term_2/4-learning_evidences')
sp=root/'G10_T2_L1_C1C2_exam_solution_1.tex'
ep=root/'G10_T2_L1_C1C2_exam_1.tex'
s=sp.read_text(encoding='utf-8'); original=s
e=ep.read_text(encoding='utf-8')
def hl(kind,x): return '\\'+kind+'{'+str(x)+'}'
def v(x): return hl('GTenHLValue',x)
def p(x): return hl('GTenHLProbability',x)
def o(x): return hl('GTenHLOutcome',x)
def f(x): return hl('HLCumulativeProbability',x)
row='\\\\\n'
def table(head,rows):
    return '\\begin{center}\n\\begin{tabular}{'+'c'*len(head)+'}\\toprule\n'+' & '.join(head)+row+'\\midrule\n'+''.join(' & '.join(r)+row for r in rows)+'\\bottomrule\\end{tabular}\n\\end{center}\n'
def replace_between(text,start,end,new):
    a=text.index(start); b=text.index(end,a)
    return text[:a]+new+text[b:]
old1='Each reservation independently has exactly two mutually exclusive possible outcomes: the buyer keeps it with probability 0.3, or cancels it with probability 0.7. These probabilities apply to every reservation.'
new1='The three reservations are independent. Each reservation is either kept or cancelled, two mutually exclusive and exhaustive outcomes. The keep probabilities for reservations 1, 2 and 3 are 0.2, 0.5 and 0.8, respectively.'
s=s.replace(old1,new1)
s=s.replace('0, 0, 3, 6, 10, 15, 21 and 29 USD','0, 0, 6, 6, 10, 10, 21 and 21 USD')
s=s.replace('0, 3, 7, 11, 16, 22, 22 and 34 USD','0, 0, 11, 11, 22, 22, 34 and 34 USD')
old5=re.search(r'For one booking, a travel platform awards.*?record the account credit\.',s).group()
names=['Booking completed as scheduled','Customer cancellation within the free period','Platform cancellation before departure','Duplicate booking corrected','Accommodation unavailable on arrival','Transport connection cancelled','Booking cancelled after a service disruption']
new5='For one booking, a travel platform records exactly one of seven distinct, mutually exclusive and exhaustive booking-resolution outcomes: '+ '; '.join(f'{a} ({n.lower()})' for a,n in zip('ABCDEFG',names))+'. These named outcomes form the sample space. Outcomes A and B award 0 USD account credit; C and D award 12 USD; E, F and G award 18 USD. Thus seven outcomes map to three possible credit values. B is twice as likely as A; C is three times as likely as A; D is twice as likely as B; E is as likely as B; F is twice as likely as E; G is as likely as F. There are no other payments or adjustments. Determine the outcome probabilities from these likelihood relationships and record the account credit.'
s=s.replace(old5,new5)
oldtask='Define the random variable and support. Derive the six probabilities using normalization and produce the PMF table and labeled graph.'
newtask='Define the random variable and support. Derive the seven named outcome probabilities using normalization, map each outcome to its credit value, and construct the grouped PMF table and labeled graph.'
s=s.replace(oldtask,newtask)
# Question 1: independent products, in reservation order.
a=s.index('Write $\\GTenHLOutcome{K}'); b=s.index('\\par\\smallskip',a)
intro=r'''Write $\GTenHLOutcome{K}$ for \GTenHLOutcome{kept} and $\GTenHLOutcome{C}$ for \GTenHLOutcome{cancelled}. Each triple is in reservation 1, 2, 3 order. Before calculating products, use the complementary outcomes:
\[
\begin{aligned}
P(C_1)&=1-P(K_1)=1-0.2=\GTenHLProbability{0.8},\\
P(C_2)&=1-P(K_2)=1-0.5=\GTenHLProbability{0.5},\\
P(C_3)&=1-P(K_3)=1-0.8=\GTenHLProbability{0.2}.
\end{aligned}
\]
There are $2^3=8$ ordered complete outcomes. Independence permits multiplication using each reservation's own probabilities; the trials have different keep probabilities.
'''
outcomes=[]
for bits in product('KC',repeat=3):
    probs=[Fraction(x) if z=='K' else 1-Fraction(x) for z,x in zip(bits,['0.2','0.5','0.8'])]
    prob=probs[0]*probs[1]*probs[2]; outcomes.append((''.join(bits),prob))
intro+=table(['Ordered outcome','Product','Exact probability'],[['$'+o(r'\mathrm{'+z+'}')+'$','$'+'\\cdot'.join(p(str(float(q))) for q in [Fraction(x) if t=='K' else 1-Fraction(x) for t,x in zip(z,['0.2','0.5','0.8'])])+'$','$'+p(str(prob))+ '='+p(f'{float(prob):.2f}')+'$'] for z,prob in outcomes])
intro+='Exhaustiveness check: $(0.2+0.8)(0.5+0.5)(0.8+0.2)=1$; the eight probabilities sum to 1.\n\n'
s=s[:a]+intro+s[b:]
a=s.index('\\begin{center}',s.index('The table maps all eight outcomes')); b=s.index('Thus $',a)
groups=[(-5,['CCC'],[8]),(2,['KCC','CKC','CCK'],[2,8,32]),(9,['KKC','KCK','CKK'],[2,8,32]),(16,['KKK'],[8])]
s=s[:a]+table(['$'+v('x')+'$ (USD)','Complete outcomes','Grouped probability'],[['$'+v(x)+'$','$'+','.join(o(r'\mathrm{'+z+'}') for z in zs)+'$','$'+'+'.join(p(str(n)+'/100') for n in ns)+'='+p(str(sum(ns))+'/100')+'$'] for x,zs,ns in groups])+s[b:]
s=s.replace(r'(\GTenHLProbability{343}+\GTenHLProbability{441}+\GTenHLProbability{189}+\GTenHLProbability{27})/\GTenHLProbability{1000}',r'(\GTenHLProbability{8}+\GTenHLProbability{42}+\GTenHLProbability{42}+\GTenHLProbability{8})/\GTenHLProbability{100}')
s=s.replace('189/1000','42/100').replace('0.189','0.42').replace('18.9\\%','42\\%')
s=s.replace('Their probabilities using independent products','Cancellation complements and independent product probabilities')

# Rebuild affected PMF and CDF content from each explicit outcome mapping.
data={3:([0,6,10,21],[5,5,5,5],['Walking courier','Bicycle','Cargo bicycle','Motorcycle','Car','Van','Refrigerated van','Truck'],[3,2,2,3,4,1,3,2],[0,0,6,6,10,10,21,21]),4:([0,11,22,34],[4,5,6,5],['No service','Remote diagnosis','Software reset','Minor repair','Major repair','Replacement','Store credit','Cash refund'],[3,1,3,2,2,4,2,3],[0,0,11,11,22,22,34,34]),5:([0,12,18],[3,7,10],names,[1,2,3,4,2,4,4],[0,0,12,12,18,18,18])}
for q,(xs,ns,cats,weights,values) in data.items():
    assert sum(weights)==sum(ns)==20
    assert [sum(w for w,x in zip(weights,values) if x==z) for z in xs]==ns
    a=s.index(r'\sectionScored{'+{3:'Produce',4:'Equipment',5:'Travel'}[q]); b=s.index(r'\sectionScored{',a+1)
    sec=s[a:b]
    if q in (3,4):
        for name,x in zip(cats,values):
            sec=re.sub(r'(\\GTenHLOutcome\{'+re.escape(name)+r'\}.*? & \$\\GTenHLValue\{)\d+(\}\$)',lambda m:m[1]+str(x)+m[2],sec)
        start='The distinct walking-courier' if q==3 else 'Replacement and store credit are distinct'
        pos=sec.index(start)
        end=sec.index('\\par\\smallskip',pos)
        lead='There are eight distinct sample-space outcomes and four monetary values. Add probabilities of mutually exclusive outcomes with the same value:\n'
    else:
        pos=sec.index('Let $\\GTenHLValue{X}$'); end=sec.index('\\par\\smallskip',pos)
        lead=r'''Let $\GTenHLValue{X}$ be the account credit for one booking, in USD. The sample space is $\Omega=\{A,B,C,D,E,F,G\}$, whereas $\GTenHLValue{S_X}=\{0,12,18\}$ USD. Set $\GTenHLParameter{a}=P(A)$, an outcome probability, not the grouped mass $p_X(0)$.
\begin{align*}
P(A)&=a,&P(B)&=2a,&P(C)&=3a,\\
P(D)&=2P(B)=4a,&P(E)&=P(B)=2a,\\
P(F)&=2P(E)=4a,&P(G)&=P(F)=4a.
\end{align*}
Normalization over the seven exhaustive outcomes gives
\[
a+2a+3a+4a+2a+4a+4a=1,\qquad 20a=1,\qquad \GTenHLParameter{a}=\frac1{20}.
\]
The complete outcome probabilities and mappings are:
'''
        lead+=table(['Named outcome','$'+p(r'P(\mathrm{outcome})')+'$','$'+v('X')+'$ (USD)'],[[o(f'{z}: {name}'),'$'+p(f'{w}a')+'='+p(f'{w}/20')+'$','$'+v(x)+'$'] for z,name,w,x in zip('ABCDEFG',cats,weights,values)])
        lead+='The seven outcomes are distinct even when they award the same credit. Group their probabilities to obtain $p_X(x)=P(X=x)$:\n'
    lead+='\n'.join(r'\['+p(f'p_X({x})')+'='+ '+'.join(p(f'{w}/20') for w,z in zip(weights,values) if z==x)+'='+p(f'{n}/20')+r'.\]' for x,n in zip(xs,ns))+'\n'
    lead+='$'+v('S_X')+'=\\{'+','.join(map(str,xs))+r'\}$ USD.'+'\n'
    lead+=table(['$'+v('x')+'$ (USD)','$'+p('p_X(x)')+'$'],[['$'+v(x)+'$','$'+p(f'{n}/20')+'$'] for x,n in zip(xs,ns)])
    lead+='\\begin{center}\\begin{tikzpicture}\n'+r'\begin{axis}[keyaxis,width=.70\linewidth,height=5cm,xmin=-2,xmax='+str(xs[-1]+2)+',ymin=0,ymax=.65,xtick={'+','.join(map(str,xs))+'},ylabel={$'+p('p_X(x)')+'$},yticklabel={$'+p(r'\pgfmathprintnumber{\tick}')+'$}]\n'
    lead+=''.join(r'\draw[fill=keyMassFill,draw=keyMassColor] (axis cs:'+f'{x-.45:g},0) rectangle (axis cs:{x+.45:g},{n}/20);\n' for x,n in zip(xs,ns))
    lead+=r'\end{axis}\end{tikzpicture}\end{center}\Needspace{5\baselineskip}\textbf{PMF checks.}\begin{itemize}\item Every mass is positive.\item Normalization: $('+'+'.join(map(str,ns))+r')/20=1$.\item Set $p_X(x)=0$ outside the support. Bars use actual monetary spacing; gaps carry no mass.\end{itemize}'+'\n'
    if q==5: lead+=r'\textbf{Relationship check.} Outcome numerators satisfy $2=2(1)$, $3=3(1)$, $4=2(2)$, $2=2$, $4=2(2)$ and $4=4$, reproducing all six relationships.'+'\n'
    sec=sec[:pos]+lead+'\n'+sec[end:]
    sec=sec.replace('All six PMF entries','All seven outcome probabilities, mappings and three grouped PMF entries')
    pos=sec.index('For $\\HLCumulativeProbability'); end=sec.index('\\par\\smallskip',pos)
    cs=list(accumulate(ns)); assert cs[-1]==20
    cdf='For $'+f('F_X(x)')+r'=P(X\leq x)$, add masses in increasing monetary order. The successive cumulative numerators are $'+','.join(map(str,cs))+'$, all over $20$.\n'
    rows=[['$'+v('x')+'<'+v(xs[0])+'$','$'+f(0)+'$']]
    rows += [['$'+v(x)+r'\leq '+v('x')+'<'+v(y)+'$','$'+f(f'{n}/20')+'$'] for x,y,n in zip(xs,xs[1:],cs)]
    rows += [['$'+v('x')+r'\geq '+v(xs[-1])+'$','$'+f(1)+'$']]
    cdf+=table(['Cutoff interval (USD)','$'+f('F_X(x)')+'$'],rows)
    cdf+=r'\begin{center}\begin{tikzpicture}'+'\n'+r'\begin{axis}[keyaxis,width=.86\linewidth,height=7cm,xmin=-2,xmax='+str(xs[-1]+2)+',ymin=-.07,ymax=1.1,xtick={'+','.join(map(str,xs))+'},ylabel={$'+f('F_X(x)')+'$},yticklabel={$'+f(r'\pgfmathprintnumber{\tick}')+'$},ytick={0,.25,.5,.75,1}]\n'
    cdf+=r'\addplot[keyCDFColor,thick,<-] coordinates {(-2,0)(0,0)};'+'\n'
    cdf+=''.join(r'\addplot[keyCDFColor,thick] coordinates {'+f'({x},{n}/20)({y},{n}/20)'+'};\n' for x,y,n in zip(xs,xs[1:],cs))
    cdf+=r'\addplot[keyCDFColor,thick,->] coordinates {'+f'({xs[-1]},1)({xs[-1]+2},1)'+'};\n'
    for open_,ys in [(True,[0]+cs[:-1]),(False,cs)]:
        cdf+=r'\addplot[keyCDFColor,only marks,mark=*,mark size=1.6pt'+(',mark options={fill=white}' if open_ else '')+'] coordinates {'+''.join(f'({x},{n}/20)' for x,n in zip(xs,ys))+'};\n'
    cdf+=r'\end{axis}\end{tikzpicture}\end{center}\textbf{CDF checks.}\begin{itemize}\item The intervals cover every real cutoff, and every height lies in $[0,1]$.\item The heights never decrease.\item Each segment includes its left endpoint and excludes its right endpoint; the filled point gives the value at a jump, so the CDF is right-continuous.\item The lower-tail limit is 0 and the upper-tail limit is 1; the arrows extend both tails.\item Successive cumulative differences recover the PMF numerators $'+','.join(map(str,ns))+r'$ over $20$. Thus $F_X(a)-F_X(a^-)=p_X(a)$; unsupported cutoffs have zero jump and zero mass.\end{itemize}'+'\n\n'
    sec=sec[:pos]+cdf+sec[end:]
    low,high={3:(10,21),4:(11,22),5:(12,18)}[q]
    pos=sec.index(r'\textbf{(i)} Include only'); end=sec.index(r'\par\smallskip',pos)
    ans=''
    context={3:'handling fee for one produce crate',4:"provider's payout for one claim",5:'account credit for one booking'}[q]
    for label,cut,op,keep in [('i',low,'<',lambda x:x<low),('ii',high,r'\geq',lambda x:x>=high)]:
        selected=[(x,n) for x,n in zip(xs,ns) if keep(x)]; total=sum(n for x,n in selected); frac=str(Fraction(total,20))
        ans+=r'\textbf{('+label+')} Include only $'+','.join(str(x) for x,n in selected)+'$ USD; '+('exclude' if label=='i' else 'include')+f' the boundary mass at {cut} USD.\n'
        ans+=r'\[P('+v('X')+op+v(cut)+')='+'+'.join(p(f'p_X({x})') for x,n in selected)+r'=\frac{'+ '+'.join(str(n) for x,n in selected)+'}{20}='+p(frac)+'='+p(f'{total/20:.2f}')+r'.\]'+'\n'
        ans+='The '+context+' is '+('below' if label=='i' else 'at least')+f' {cut} USD with probability $'+p(frac)+'$, or $'+p(f'{total*5}'+r'\%')+'$.\n\n'
    sec=sec[:pos]+ans+sec[end:]
    s=s[:a]+sec+s[b:]
# Save solution first, then synchronize student statements and task.
sp.write_text(s,encoding='utf-8')
for old,new in [(old1,new1),('0, 0, 3, 6, 10, 15, 21 and 29 USD','0, 0, 6, 6, 10, 10, 21 and 21 USD'),('0, 3, 7, 11, 16, 22, 22 and 34 USD','0, 0, 11, 11, 22, 22, 34 and 34 USD'),(old5,new5),(oldtask,newtask)]:
    assert old in e
    e=e.replace(old,new)
ep.write_text(e,encoding='utf-8')
print('Updated solution first, then student exam.')
