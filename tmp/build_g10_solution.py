from pathlib import Path
import re, json
from fractions import Fraction as F

ROOT=Path.cwd()
BASE=ROOT/'book2026-2027/grade10/term_1/3-learning_evidences'
source=(BASE/'G10_T1_C1C2C3C4C5C6C7_exam.tex').read_text(encoding='utf-8')
out=BASE/'G10_T1_C1C2C3C4C5C6C7_exam_solution.tex'
blocks=re.findall(r'\\SubsectionBox\{([^\n]+)\}\n(.*?)\\end\{minipage\}',source,re.S)
assert len(blocks)==13
titles=[b[0].split(' \\score')[0] for b in blocks]
slugs=[re.sub('[^a-z0-9]+','-',x.lower()).strip('-') for x in titles]
criteria=[[(1,3),(2,6)],[(1,3),(3,6)]]+[[(4,2)]]*3+[[(5,2)]]*3+[[(6,2)]]*3+[[(7,3)]]*2
totals=[sum(v for c in criteria for k,v in c if k==i) for i in range(1,8)]
assert totals==[6]*7 and sum(totals)==42

def table(headers,rows,spec=None):
    spec=spec or 'l'+'c'*(len(headers)-1)
    return '\\begin{center}\n\\begin{tabular}{@{}'+spec+'@{}}\\toprule\n'+' & '.join(headers)+r'\\\midrule'+'\n'+'\n'.join(' & '.join(map(str,row))+r'\\' for row in rows)+'\n\\bottomrule\\end{tabular}\n\\end{center}\n'
def money(x):
    return str(int(x)) if x==int(x) else f'{float(x):.2f}'
def solhead(slug,c,pts,title):
    return f'\\subsection*{{C{c} - {title} \\score{{{pts}}}}}\n\\phantomsection\\label{{sol:{slug}-c{c}}}\n'
def nav(slug):
    return f'\\secInicio[sec:{slug}][sec:summarized-solutions]\n'
def enumtext(names,states):
    return 'Alternatives: '+ '; '.join(f'$A_{i}$: {x}' for i,x in enumerate(names,1))+'.\\par\nStates: '+ '; '.join(f'$S_{i}$: {x}' for i,x in enumerate(states,1))+'.\n'

# Parse every supplied payoff table directly from the authoritative exam.
data={}
for n in range(3,14):
    b=blocks[n-1][1]
    t=b.split('\\toprule',1)[1].split('\\bottomrule',1)[0]
    head,body=t.split('\\midrule',1)
    rows=[]
    for row in body.split('\\\\'):
        if '&' in row:
            cells=[x.strip() for x in row.strip().split('&')]
            rows.append((cells[0],[int(x) for x in cells[1:]]))
    names=[re.sub(r' \(\$A_\d\$\)','',x[0]) for x in rows]
    values=[r[1] for r in rows]
    states={3:['High','Medium','Low'],4:['High','Medium','Low'],5:['Very strong sales','Strong sales','Steady sales','Weak sales'],6:['High','Medium','Low'],7:['High','Normal','Low'],8:['Very high','High','Moderate','Low'],9:['Strong','Steady','Weak'],10:['High','Normal','Low'],11:['Surge','Strong','Steady','Slow'],12:['High enrolment','Moderate enrolment','Low enrolment'],13:['Early order','Revised order','Late order']}[n]
    data[n]={'names':names,'values':values,'states':states}

calc1=r'''Let $q_{ij}$ be participants, $v_i$ the workshop contribution per participant,
$d_j$ the demand contribution per participant, and $f_i$ the fixed sponsorship.
All monetary rates are in USD per participant; $f_i$ and payoffs are in USD.
\[
P(A_i,S_j)=q_{ij}(v_i+d_j)+f_i.
\]
The per-participant contributions are added before multiplying by participants.
The fixed sponsorship is then added once per workshop; it is not multiplied by participants.
\begin{align*}
P(A_1,S_1)&=30(12+6)+80=540+80=620,\\
P(A_1,S_2)&=18(12+2)+80=252+80=332,\\
P(A_2,S_1)&=24(15+6)+50=504+50=554,\\
P(A_2,S_2)&=16(15+2)+50=272+50=322.
\end{align*}
'''
pay1=table(['Alternative','Strong ($S_1$)','Weak ($S_2$)'],[['Pottery workshop ($A_1$)',620,332],['Weaving workshop ($A_2$)',554,322]])
calc2=r'''Profit equals total revenue minus total variable costs minus fixed seasonal costs:
\begin{align*}
R_{ij}&=q_{ij}(b_i+s_j), & VC_{ij}&=q_{ij}c_i,\\
P(A_i,S_j)&=R_{ij}-VC_{ij}-F_j
=q_{ij}(b_i+s_j)-q_{ij}c_i-F_j.
\end{align*}
Here $q_{ij}$ is places sold; $b_i$, $s_j$, and $c_i$ are base revenue, surcharge,
and variable cost in USD per place; $F_j$ is the fixed seasonal cost in USD.
The surcharge is part of revenue for every place sold. The fixed cost is paid
once in each alternative--state calculation, not once per place.
\begin{align*}
P(A_1,S_1)&=90(32+8)-90(18)-500=3600-1620-500=1480,\\
P(A_1,S_2)&=60(32+3)-60(18)-650=2100-1080-650=370,\\
P(A_2,S_1)&=70(45+8)-70(26)-500=3710-1820-500=1390,\\
P(A_2,S_2)&=40(45+3)-40(26)-650=1920-1040-650=230.
\end{align*}
'''
pay2=table(['Alternative','Strong ($S_1$)','Weak ($S_2$)'],[['Town route ($A_1$)',1480,370],['Countryside route ($A_2$)',1390,230]])
assert [[30*18+80,18*14+80],[24*21+50,16*17+50]]==[[620,332],[554,322]]
assert [[90*40-90*18-500,60*35-60*18-650],[70*53-70*26-500,40*48-40*26-650]]==[[1480,370],[1390,230]]

def extrema(n,compact=False):
    d=data[n]; rows=[]
    for i,(name,v) in enumerate(zip(d['names'],d['values']),1):
        mx,mn=max(v),min(v)
        cells=[f'{name} ($A_{i}$)',str(mx),str(mn)] if compact else [f'{name} ($A_{i}$)',r'$\max\{'+','.join(map(str,v))+r'\}='+str(mx)+'$',r'$\min\{'+','.join(map(str,v))+r'\}='+str(mn)+'$']
        rows.append(cells)
    mxs=[max(v) for v in d['values']]; mns=[min(v) for v in d['values']]
    a=mxs.index(max(mxs)); b=mns.index(max(mns))
    result=table(['Alternative','Row maximum $M_i$','Row minimum $m_i$'],rows)
    result+=r'\[\max_i M_i=\max\{'+','.join(map(str,mxs))+r'\}='+str(mxs[a])+r',\qquad \max_i m_i=\max\{'+','.join(map(str,mns))+r'\}='+str(mns[b])+'.\]\n'
    result+=f'\\textbf{{Maximax:}} choose \\textbf{{{d["names"][a]}}} ($A_{a+1}$), with best-case profit {mxs[a]} thousand USD.\\par\n'
    result+=f'\\textbf{{Maximin:}} choose \\textbf{{{d["names"][b]}}} ($A_{b+1}$), with worst-case profit {mns[b]} thousand USD.\n'
    return result.replace('\\n','\n')

def regret(n,compact=False):
    d=data[n]; v=d['values']; best=list(map(max,zip(*v)))
    r=[[b-x for b,x in zip(best,row)] for row in v]
    worst=list(map(max,r)); k=worst.index(min(worst)); unit='USD' if n==8 else 'thousand USD'
    data[n].update(best=best,regret=r,worst=worst,winner=k)
    result=r'\[\boldsymbol{b}=\bigl('+','.join(map(str,best))+r'\bigr),\qquad b_j=\max_k P(A_k,S_j).\]'+'\n'
    if not compact:
        result+='Each column is compared with its highest profit. Regret is the profit missed by not choosing that state\'s best alternative:\n'+r'\[r(A_i,S_j)=\max_k P(A_k,S_j)-P(A_i,S_j).\]'+'\n'
    rows=[]
    for i,row in enumerate(v):
        cells=[]
        for j,x in enumerate(row):
            xx=f'({x})' if x<0 else str(x)
            cells.append(r'$\begin{gathered}'+f'{best[j]}-{xx}'+r'\\='+str(r[i][j])+r'\end{gathered}$')
        rows.append([f'$A_{i+1}$']+cells+[str(worst[i])])
    result+=f'All payoffs and regrets in this calculation are in {unit}.\n'
    result+=table(['Alternative']+[f'$S_{j+1}$' for j in range(len(best))]+['Maximum regret'],rows)
    result+=r'\[\min_i\max_j r(A_i,S_j)=\min\{'+','.join(map(str,worst))+r'\}='+str(worst[k])+r'.\]'+'\n'
    result+=f'Choose \\textbf{{{d["names"][k]}}} ($A_{k+1}$): its maximum regret is \\textbf{{{worst[k]} {unit}}}. '
    if not compact: result+='This is the smallest worst possible opportunity loss; it does not mean that this loss occurs in every state or that this alternative always earns the most profit.'
    return result+'\n'

probs={9:['0.40','0.35','0.25'],10:['0.30','0.40','0.30'],11:['0.20','0.30','0.30','0.20']}
def emv(n,compact=False):
    d=data[n]; ps=probs[n]; q=list(map(F,ps)); assert sum(q)==1 and all(0<=p<=1 for p in q)
    es=[sum(p*x for p,x in zip(q,row)) for row in d['values']]; k=es.index(max(es))
    d.update(emvs=[str(e) for e in es],winner=k)
    result=r'\[\boldsymbol{q}=('+','.join(ps)+r'),\qquad '+'+'.join(ps)+r'=1.\]'+'\nAll probabilities lie in $[0,1]$, so they are nonnegative and valid.\n'
    if not compact: result+=r'\[EMV(A_i)=\sum_{j=1}^{n}P(S_j)P(A_i,S_j).\]'+'\nMultiply each state payoff by its probability, including any negative payoff, and add the weighted amounts. All EMVs are in thousand USD.\n'
    result+=r'\begin{align*}'+'\n'
    for i,row in enumerate(d['values']):
        terms='+'.join(f'{p}({x})' for p,x in zip(ps,row))
        weighted=''.join(('+' if j and p*x>=0 else '')+money(p*x) for j,(p,x) in enumerate(zip(q,row)))
        result+=f'EMV(A_{i+1})&={terms}'
        if not compact: result+=r'\\&='+weighted
        result+='='+money(es[i])+ (r',\\' if i<len(es)-1 else '.')+'\n'
    result+=r'\end{align*}'+'\n'
    result+=r'\[\max\{'+','.join(money(e) for e in es)+r'\}='+money(es[k])+r'.\]'+'\n'
    result+=f'Choose \\textbf{{{d["names"][k]}}} ($A_{k+1}$), with expected profit \\textbf{{{money(es[k])} thousand USD}} (USD {int(es[k]*1000):,}). '
    if not compact: result+='EMV is a probability-weighted expected payoff, not a guaranteed outcome. The realised profit will be the payoff for the state that actually occurs.'
    return result+'\n'

course=r'''The states are mutually exclusive and exhaustive, so
\[
p+\frac p2+P(S_3)=1\quad\Longrightarrow\quad
P(S_3)=1-\frac{3p}{2},\qquad
\boldsymbol{q}=\left(p,\frac p2,1-\frac{3p}{2}\right).
\]
Every probability must lie in $[0,1]$:
\[
\begin{aligned}
0\le p\le1,&\qquad 0\le p/2\le1\ \Longrightarrow\ 0\le p\le2,\\
0\le1-3p/2\le1&\ \Longrightarrow\ 0\le p\le\frac23.
\end{aligned}
\]
Their intersection is $\boxed{0\le p\le\frac23}$.
Although the question asks about $[0,1]$, the interval
$\frac23<p\le1$ is infeasible because $P(S_3)<0$.
No decision based on these probabilities is valid there.
Using $E_i=EMV(A_i)=\sum_j P(S_j)P(A_i,S_j)$, in thousand USD:
\begin{align*}
E_1&=100p+36\left(\frac p2\right)-8\left(1-\frac{3p}{2}\right)
=100p+18p-8+12p=130p-8,\\
E_2&=52p+48\left(\frac p2\right)+28\left(1-\frac{3p}{2}\right)
=52p+24p+28-42p=28+34p.
\end{align*}
The threshold solves
\[
E_1=E_2\iff130p-8=28+34p\iff96p=36
\iff\boxed{p=\frac38}.
\]
It is feasible: $0<\frac38<\frac23$. At the tie, both EMVs equal
$\frac{163}{4}=40.75$ thousand USD.
The difference $E_1-E_2=96p-36$ is negative below $\frac38$ and positive above it.
At the feasible endpoints, $(E_1,E_2)=(-8,28)$ for $p=0$ and
$(E_1,E_2)=(\frac{236}{3},\frac{152}{3})$ for $p=\frac23$.
Thus both endpoints agree with the decision rule:
\[
\boxed{\begin{cases}
\text{Pilot launch }(A_2),&0\le p<\frac38,\\
\text{Full and pilot launches tied},&p=\frac38,\\
\text{Full launch }(A_1),&\frac38<p\le\frac23.
\end{cases}}
\]
Choose the pilot launch below the threshold and the full launch above it;
either launch is optimal at the tie. These are expected-profit decisions, not guarantees.
'''
printing=r'''The three state probabilities sum to one:
\[
2p+p+P(S_3)=1\quad\Longrightarrow\quad
P(S_3)=1-3p,\qquad \boldsymbol{q}=(2p,p,1-3p).
\]
Requiring every probability to lie in $[0,1]$ gives
\[
0\le2p\le1\iff0\le p\le\frac12,\quad
0\le p\le1,\quad
0\le1-3p\le1\iff0\le p\le\frac13.
\]
The intersection is $\boxed{0\le p\le\frac13}$.
Although the question asks about $[0,1]$, the interval
$\frac13<p\le1$ is infeasible because $P(S_3)<0$.
For $p>\frac12$, $P(S_1)>1$ as well. No alternative is recommended in the infeasible interval.
The expected profits, in thousand USD, are
\begin{align*}
E_1&=EMV(A_1)=24(2p)+60p+84(1-3p)\\
&=48p+60p+84-252p=84-144p,\\
E_2&=EMV(A_2)=78(2p)+42p+36(1-3p)\\
&=156p+42p+36-108p=36+90p.
\end{align*}
Set the expected profits equal:
\[
E_1=E_2\iff84-144p=36+90p\iff48=234p
\iff\boxed{p=\frac8{39}}.
\]
The threshold lies within the domain: $0<\frac8{39}<\frac13$.
Both EMVs are $\frac{708}{13}$ thousand USD at the tie.
Since $E_1-E_2=48-234p$, the standard contract is better below $\frac8{39}$,
and the flexible contract is better above it.
At $p=0$, $(E_1,E_2)=(84,36)$; at $p=\frac13$, $(E_1,E_2)=(36,66)$.
These checks include both feasible endpoints.
\[
\boxed{\begin{cases}
\text{Standard contract }(A_1),&0\le p<\frac8{39},\\
\text{Standard and flexible contracts tied},&p=\frac8{39},\\
\text{Flexible contract }(A_2),&\frac8{39}<p\le\frac13.
\end{cases}}
\]
Choose the standard contract below the threshold and the flexible contract above it;
either contract is optimal at the tie. Expected profit is not guaranteed profit.
'''

objective=re.search(r'\\textbf\{Learning objective:\} (.*?)\}',source).group(1)
crit=[x.split('\\par')[0].split('}')[0] for x in re.findall(r'\\textbf\{C\d\.\} ([^\n]+)',source)]
assert len(crit)==7
doc=r'''% Source: G10_T1_C1C2C3C4C5C6C7_exam.tex (questions and assessment rules).
% Full-width worked solutions; monetary units are local to each problem.
\makeatletter
\def\input@path{{./}{../}{../../}{../../../}{../../../../}{preamble/}{../preamble/}{../../preamble/}{../../../preamble/}}
\makeatother
\input{preamble_exams.tex}
% Local solution-document spacing and readable labels in the inherited table.
\linespread{1.08}
\setlength{\parskip}{4pt}
% Retain the shared four-argument helper and its list handling, with a wider
% label column and explicit spaces for labels defined under ExplSyntaxOn.
\ExplSyntaxOn
\RenewDocumentCommand{\DecisionElementsTable}{mmmm}{
\decision_prepare_lists:nn {#1}{#2}
\begin{center}
\begin{tabularx}{\textwidth}{@{}p{2.6cm}>{\raggedright\arraybackslash}X@{}}
\toprule Element & Description \\ \midrule
Alternatives & \decision_print_slots:Nn \l_decision_alternatives_seq {A} \\
States~of~nature & \decision_print_slots:Nn \l_decision_states_seq {S} \\
Events & #3 \\ Consequences & #4 \\ \bottomrule
\end{tabularx}\end{center}
}
\ExplSyntaxOff
\title{Grade 10 -- Term 1\\C1--C7 Catch-up Exam Solutions}
\author{}
\date{2026--2027}
\begin{document}
\maketitle
\vspace{-1.5cm}
\setcounter{tocdepth}{1}
\setcounter{secnumdepth}{2}
\phantomsection\label{toc}
\tableofcontents
\clearpage
\begingroup\small
\section*{Learning objective}
'''+objective+'\n'+r'''
\section*{Criteria assessment}
This exam assesses C1--C7. Each question and task shows its points.
\textbf{Passing requires a minimum of 5 cumulative points per criterion,
including points earned in previous learning activities}.
Show all procedures; answers without the required procedure receive no credit.
Partial credit may be awarded for a correct method with arithmetic errors.
Missing names or late submissions incur a 1-point deduction per criterion.
\section*{Evaluated criteria}
\begin{enumerate}[label=\textbf{C\arabic*}]
'''+''.join('\\item '+c.strip()+'\n' for c in crit)+r'\end{enumerate}'+'\n'
score_rows=[]
for i,c in enumerate(criteria,1):
    vals=[next((str(v) for k,v in c if k==j),'--') for j in range(1,8)]
    score_rows.append([str(i)]+vals+[str(sum(v for k,v in c))])
score_rows.append([r'\textbf{Total}']+[r'\textbf{6}']*7+[r'\textbf{42}'])
doc+=table(['Question']+[f'C{i}' for i in range(1,8)]+['Points'],score_rows)
doc+='Each criterion has 6 available points; the exam has 42 available points overall.\n'
doc+=r'\textbf{Notation.} $A_i$ and $S_j$ always follow the original alternative and state order within each problem. $P(A_i,S_j)$ denotes a monetary payoff; $P(S_j)$ denotes a probability. Navigation arrows return to the contents, the problem, or the summary.'+'\n'
doc+='\\endgroup\n'

for n,(heading,body) in enumerate(blocks,1):
    slug=slugs[n-1]; cs=criteria[n-1]
    doc+='\n\\clearpage\n'+f'\\sectionScored{{{titles[n-1]}}}{{'+ ' '.join(f'C{k}-\\sml{{{v}}}' for k,v in cs)+f'}}{{sec:{slug}}}\n'
    if n==2: doc+='\\begingroup\\setlength{\\parskip}{2pt}\\linespread{1.02}\\selectfont\n'
    if n<=2:
        scenario,question=body.split('Characterize the key elements',1)
        doc+=scenario.strip()+'\n'
        doc+=r'\QuestionsTasks[sec:'+slug+']{\n'+f'{{1}}/{{sol:{slug}-c1}}/{{Characterize the key elements of the decision-making situation \\sscore{{C1-3}}}},\n'+f'{{{cs[1][0]}}}/{{sol:{slug}-c{cs[1][0]}}}/{{and construct the payoff table. \\sscore{{C{cs[1][0]}-6}}}}\n'+'}\n'
        doc+=solhead(slug,1,3,'Characterization')
        if n==1:
            doc+=r'''\DecisionElementsTable{Pottery workshop; Weaving workshop}
{Strong tourist demand; Weak tourist demand}
{Tourist demand revealed after the workshop is chosen; the studio cannot control it.}
{Total net contribution in USD for each workshop--demand pair.}
The economic context is a craft studio choosing its workshop before tourist demand is known.
The decision controls the workshop, while demand controls attendance and the extra contribution rate.
'''
            doc+=solhead(slug,2,6,'Additive contributions and payoff table')+calc1+'\\textbf{Completed payoff table (USD).}\n'+pay1
            doc+='\\textbf{Conclusion:} the pottery workshop gives a higher contribution in both states: USD 620 under strong demand and USD 332 under weak demand.\n'
        else:
            doc+=r'''\DecisionElementsTable{Town route; Countryside route}
{Strong seasonal demand; Weak seasonal demand}
{Seasonal demand revealed after the route is chosen; the operator cannot control it.}
{Seasonal profit in USD for each route--demand pair.}
The economic context is a tour operator choosing a route before knowing sales,
the demand surcharge, and the seasonal fixed cost.
'''
            doc+=solhead(slug,3,6,'Profit calculations and payoff table')+calc2+'\\textbf{Completed payoff table (profit in USD).}\n'+pay2
            doc+='\\textbf{Conclusion:} the town route earns more in both states: USD 1,480 under strong demand and USD 370 under weak demand.\n'
    else:
        # Preserve the original scenario, table, probability relationships and question wording.
        if n<=5: start='What would the optimistic decision be?'
        elif n<=8: start='What decision would be selected using the Minimax Regret criterion?'
        elif n<=11: start='What decision would be selected using the EMV or Bayes criterion?'
        else: start='State the preferred alternative for every probability value'
        scenario,question=body.split(start,1)
        doc+=scenario.strip()+'\n'
        c,pts=cs[0]
        doc+=f'\\QuestionsTasks[sec:{slug}]{{\n{{{c}}}/{{sol:{slug}-c{c}}}/{{{start+question.rstrip()}}}\n}}\n'
        title={4:'Maximax and Maximin',5:'Minimax Regret',6:'EMV / Bayes',7:'Probability sensitivity analysis'}[c]
        doc+=solhead(slug,c,pts,title)
        doc+=enumtext(data[n]['names'],data[n]['states'])
        if c==4:
            doc+='All profits below are in thousand USD. For every row, find the largest and smallest payoff:\n'+extrema(n)
            doc+='Maximax is optimistic: it focuses on the best possible result and ignores the downside. Maximin is conservative: it protects the best worst-case result and may forgo a large gain. Without probabilities, neither method estimates how likely a payoff is or gives an expected profit.\n'
        elif c==5: doc+=regret(n)
        elif c==6: doc+=emv(n)
        else: doc+=course if n==12 else printing
    doc+=nav(slug)
    if n==2: doc+='\\endgroup\n'

doc+=r'''
\clearpage
\sectionScored{Summarized Solutions}{C1--C7}{sec:summarized-solutions}
{\small
The numbered summaries follow the exam order. $A_i$ and $S_j$ use the original
row and column order. $E_i=EMV(A_i)$; $b_j$ is the best payoff in state $S_j$;
$r_{ij}=b_j-P(A_i,S_j)$. Units are stated for each problem.
'''
for n in range(1,14):
    slug=slugs[n-1]
    if n in [3,6,8,9,12,13]: doc+='\\clearpage\n'
    doc+=f'\\subsection{{{titles[n-1]} \\hfill '+ ' '.join(f'C{k}--{v}' for k,v in criteria[n-1])+'}\n'+f'\\label{{summary:{slug}}}\n'
    if n<=2:
        names=['Pottery workshop','Weaving workshop'] if n==1 else ['Town route','Countryside route']
        doc+=enumtext(names,['Strong demand','Weak demand'])
        doc+='Uncertain event: actual demand after the choice. Context: '+('craft studio selecting a workshop; consequences are net contributions in USD.' if n==1 else 'tour operator selecting a route; consequences are seasonal profits in USD.')+'\n'
        if n==1:
            doc+=r'''\[P_{ij}=q_{ij}(v_i+d_j)+f_i.\]
The fixed sponsorship is added once; the two per-participant rates multiply attendance.
'''
            doc+=table(['Payoff (USD)','$S_1$: strong','$S_2$: weak'],[['Pottery ($A_1$)','$30(12+6)+80=620$','$18(12+2)+80=332$'],['Weaving ($A_2$)','$24(15+6)+50=554$','$16(15+2)+50=322$']])
            doc+='Pottery gives the higher contribution in both demand states.\n'
        else:
            doc+=r'''\[P_{ij}=q_{ij}(b_i+s_j)-q_{ij}c_i-F_j.\]
Revenue includes the surcharge; the seasonal fixed cost is subtracted once.
'''
            doc+=table(['Profit (USD)','$S_1$: strong','$S_2$: weak'],[['Town ($A_1$)','$90(32+8)-90(18)-500=1480$','$60(32+3)-60(18)-650=370$'],['Countryside ($A_2$)','$70(45+8)-70(26)-500=1390$','$40(45+3)-40(26)-650=230$']])
            doc+='The town route earns more in both demand states.\n'
    elif n<=5:
        doc+=enumtext(data[n]['names'],data[n]['states'])+'All profits are in thousand USD.\n'+extrema(n,True)
    elif n<=8:
        doc+=enumtext(data[n]['names'],data[n]['states'])+regret(n,True)
    elif n<=11:
        doc+=enumtext(data[n]['names'],data[n]['states'])+'All EMVs are in thousand USD.\n'+emv(n,True)
        doc+='Expected profit is not guaranteed profit.\n'
    elif n==12:
        doc+=r'''$A_1$: Full launch; $A_2$: Pilot launch. States: high, moderate, low enrolment.
Profits and EMVs are in thousand USD.
\[
P(S_3)=1-p-\tfrac p2=1-\tfrac{3p}{2},\qquad
\boldsymbol{q}=\left(p,\tfrac p2,1-\tfrac{3p}{2}\right).
\]
The conditions $0\le p\le1$, $0\le p/2\le1$ and $0\le1-3p/2\le1$
intersect in $0\le p\le\frac23$. The remaining interval $(\frac23,1]$ gives a negative third probability.
\begin{align*}
E_1&=100p+36(p/2)-8(1-3p/2)=130p-8,\\
E_2&=52p+48(p/2)+28(1-3p/2)=28+34p.\\
E_1=E_2&\iff130p-8=28+34p\iff96p=36\iff p=\tfrac38.
\end{align*}
The threshold is feasible. $E_1-E_2=96p-36$ changes from negative to positive.
At $p=0$, $(E_1,E_2)=(-8,28)$; at $p=\frac23$, $(E_1,E_2)=(\frac{236}{3},\frac{152}{3})$.
\[
\boxed{\begin{cases}
\text{Pilot launch }(A_2),&0\le p<\frac38,\\
\text{Full and pilot launches tied},&p=\frac38,\\
\text{Full launch }(A_1),&\frac38<p\le\frac23.
\end{cases}}
\]
No recommendation is valid for $\frac23<p\le1$.
'''
    else:
        doc+=r'''$A_1$: Standard contract; $A_2$: Flexible contract. States: early, revised, late order.
Profits and EMVs are in thousand USD.
\[
P(S_3)=1-2p-p=1-3p,\qquad \boldsymbol{q}=(2p,p,1-3p).
\]
The restrictions $0\le2p\le1$, $0\le p\le1$ and $0\le1-3p\le1$
intersect in $0\le p\le\frac13$. The interval $(\frac13,1]$ gives $P(S_3)<0$;
also $P(S_1)>1$ when $p>\frac12$.
\begin{align*}
E_1&=24(2p)+60p+84(1-3p)=84-144p,\\
E_2&=78(2p)+42p+36(1-3p)=36+90p.\\
E_1=E_2&\iff84-144p=36+90p\iff48=234p\iff p=\tfrac8{39}.
\end{align*}
The threshold is feasible. $E_1-E_2=48-234p$ changes from positive to negative.
At $p=0$, $(E_1,E_2)=(84,36)$; at $p=\frac13$, $(E_1,E_2)=(36,66)$.
\[
\boxed{\begin{cases}
\text{Standard contract }(A_1),&0\le p<\frac8{39},\\
\text{Standard and flexible contracts tied},&p=\frac8{39},\\
\text{Flexible contract }(A_2),&\frac8{39}<p\le\frac13.
\end{cases}}
\]
No recommendation is valid for $\frac13<p\le1$.
'''
    doc+=f'\\secInicio[sec:{slug}][sec:summarized-solutions]\n'
doc+='}\n\\end{document}\n'
out.write_text(doc,encoding='utf-8')
print('Created',out,'with',len(doc.splitlines()),'lines')
print('Scores:',totals,'Total:',sum(totals))
