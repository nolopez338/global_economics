from pathlib import Path
from decimal import Decimal as D, ROUND_HALF_UP
import re, json, hashlib

root=Path(__file__).resolve().parents[2]
dest=root/'book2026-2027/grade11/term_1/3-learning_evidences'
exam2=(dest/'G11_T1_L3_C8C9C10_exam_2.tex').read_text(encoding='utf-8')
sol2=(dest/'G11_T1_L3_C8C9C10_exam_solution_2.tex').read_text(encoding='utf-8')
ref=(root/'book2026-2027/fundamentals/normal-table.tex').read_text(encoding='utf-8')
hashes={str(p.relative_to(root)):hashlib.sha256(p.read_bytes()).hexdigest() for p in [dest/'G11_T1_L3_C8C9C10_exam_2.tex',dest/'G11_T1_L3_C8C9C10_exam_solution_2.tex',root/'book2026-2027/fundamentals/normal-table.tex']}
(Path(__file__).parent/'source_hashes.json').write_text(json.dumps(hashes,indent=2))
alphas=list(map(D,['.30','.20','.10','.05','.025','.01','.005']))
tt={}; nt={}
for line in ref.splitlines():
    vals=re.findall(r'(?<![\w.])\d+(?:\.\d+)?',line.split('\\\\')[0]) if '&' in line else []
    if re.match(r'^\s*\d+\s+&',line) and len(vals)==8:
        tt[int(vals[0])]=dict(zip(alphas,map(D,vals[1:])))
    if re.match(r'^\s*\d\.\d\s+&',line) and len(vals)==11:
        for j,v in enumerate(vals[1:]): nt[D(vals[0])+D(j)/100]=D(v)
assert len(tt)==39 and len(nt)==260,(len(tt),len(nt))
def s(v):
    return format(D(v),'f').rstrip('0').rstrip('.') if '.' in format(D(v),'f') else str(v)
def f(v,n=2): return format(D(v).quantize(D(10)**-n,rounding=ROUND_HALF_UP),f'.{n}f')
def math(x): return '$'+x+'$'
def display(x): return '\\[\n'+x+'\n\\]\n'
def align(lines): return display('\\begin{aligned}\n'+'\\\\\n'.join(lines)+'\n\\end{aligned}')
def box(v): return '\\boxed{'+v+'}'

# Entries follow V2 identities until the final, deliberately small shuffle.
# n, location, scale, signed tail columns; all critical values come from ref.
spec=[
 (21,'3','6',[(1,'.30'),(1,'.10')]),
 (10,'2','4',[(-1,'.025'),(1,'.10')]),
 (13,'.8','4',[(-1,'.10')]),
 (19,'-4','8',[(-1,'.30')]),
 (12,'-.8','3',[(-1,'.05'),(-1,'.30')]),
 (15,'-.7','1.8',[(-1,'.025'),(1,'.025')]),
 (20,'-4.2','5.5',[(-1,'.10')]),
 (23,'-1.8','6',[(-1,'.01'),(1,'.10')]),
 (26,'3','7',[(1,'.025')]),
 (17,'4','9',[(-1,'.05'),(1,'.05')]),
 (16,'2.6','5',[(-1,'.30')]),
 (19,'.9','6',[(-1,'.20'),(1,'.05')]),
 (17,'-1.8','5',[(-1,'.025')]),
 (14,'2.2','4.5',[(-1,'.025'),(1,'.025')]),
 (12,'-1.6','4',[(-1,'.05')]),
 (21,'1.8','5',[(1,'.10')]),
]
order=[2,1,3,4,5,7,6,8,9,10,13,12,11,14,15,16,17]
mapping={old:new for new,old in enumerate(order,1)}
eblocks=re.split(r'(?=\\SubsectionBox\{\d+\.)',exam2)
assert len(eblocks)==18
oldsol=re.split(r'(?=\\needspace\{(?:8|12)\\baselineskip\}\n\\sectionScored)',sol2)
assert len(oldsol)==18,len(oldsol)
questions={}; data={}
for old,(n,m,a,cols) in enumerate(spec,1):
    m,a=D(m),D(a); df=n-1
    cs=[sign*tt[df][D(alpha)] for sign,alpha in cols]; xs=[m+a*c for c in cs]
    b=eblocks[old].split('\\SubsectionBox',1)[0] if False else eblocks[old]
    if old==17: continue
    context=b[b.index('\\textbf'):].strip()
    n0=re.search(r'n=(\d+)',context)[1]; m0=re.search(r'm=([-\d.]+)',context)[1]; a0=re.search(r'a=([\d.]+)',context)[1]
    context=context.replace('n='+n0+'$',f'n={n}$').replace('m='+m0+'$',f'm={s(m)}$').replace('a='+a0+'$',f'a={s(a)}$')
    for var in ['X','X_T','X_N']:
        context=context.replace(var+'='+m0+'+'+a0,var+'='+s(m)+'+'+s(a))
    if old in [1,2,3,4,5,11,12,13]:
        oldbounds={1:['8.441','14.58'],2:['-7.875','8.675'],3:['-5.142'],4:['-12.83'],5:['-9.5016','-4.4004'],11:['-0.7285'],12:['-8.25','16.32'],13:['-13.372']}[old]
        for orig,x in zip(oldbounds,xs):context=context.replace(orig,s(x))
    title=re.search(r'\\SubsectionBox\{\d+\. (.*?) \\score',b)[1]
    typ=re.search(r'\\textbf\{C\d+ -- (.*?)\.\}',context)[1]
    event=re.search(r'Find (.*)',context)[1].split(' Find both')[0]
    d=dict(old=old,n=n,df=df,m=m,a=a,cols=cols,cs=cs,xs=xs,title=title,typ=typ,context=context,event=event,unit={1:'kWh',2:'thousands of dollars',3:'minutes',4:'dollars',5:'tonnes',6:'g',7:'dollars',8:'minutes',9:'minutes',10:'tonnes',11:'minutes',12:'litres',13:'thousands of dollars',14:'kg',15:'dollars',16:'minutes'}[old])
    data[old]=d;questions[old]=context

def entry(d,j):
    return f"Row ${d['df']}$, column $\\alpha={s(D(d['cols'][j][1]))}$, gives $t^*={f(abs(d['cs'][j]),3)}$. "
def stand(d):
    m,a=d['m'],d['a']; lines=[]
    for j,(x,c) in enumerate(zip(d['xs'],d['cs'])):
        suffix=['_L','_U'][j] if len(d['cs'])==2 else ''
        lines.append(f"c{suffix}&=\\frac{{{s(x)}-({s(m)})}}{{{s(a)}}}={f(c,3)}.")
    return 'Standardize:\n'+align(lines)
def invstand(d):
    return f"Standardize the unknown cutoff(s) using $c=(x-({s(d['m'])}))/{s(d['a'])}$. "
def back(d,normal=False):
    cs=d['zs'] if normal else d['cs']; xs=[d['m']+d['a']*c for c in cs]
    lines=[]
    for j,(c,x) in enumerate(zip(cs,xs)):
        var=(['L','U'][j] if len(cs)==2 else 'x')+('_N' if normal else ('_T' if d['old']>=11 else ''))
        lines.append(f"{var}&={s(d['m'])}+{s(d['a'])}({f(c,2 if normal else 3)})={s(x)}\\approx{box(f(x)+'\\text{ '+d['unit']+'}') }.")
    return align(lines)
def normalentry(z):
    az=abs(z); row=(az*10//1)/10; col=az-row
    return f"Row ${f(row,1)}$, column ${f(col)}$, gives $\\Phi({f(az)})={f(nt[az],4)}$. "
def comparison(rt,rn,unit='',suffix=''):
    ea=abs(rt-rn); nd=2 if unit else 4
    return align([f'E_{{A{suffix}}}&=|{s(rt)}-({s(rn)})|={s(ea)}\\approx'+box(f(ea,nd)+('\\text{ '+unit+'}' if unit else ''))+r',',
       f'E_{{Pt{suffix}}}&=\\frac{{100({s(ea)})}}{{|{s(rt)}|}}\\approx'+box(f(100*ea/abs(rt))+r'\%')+',',
       f'E_{{Pn{suffix}}}&=\\frac{{100({s(ea)})}}{{|{s(rn)}|}}\\approx'+box(f(100*ea/abs(rn))+r'\%')+'.'])

solutions={}
for old,d in data.items():
    n,df,m,a,cs,xs=d['n'],d['df'],d['m'],d['a'],d['cs'],d['xs']; unit=d['unit']; als=[D(c[1]) for c in d['cols']]
    text=f'Here $\\nu={n}-1={df}$. '
    if old in [1,2,3,4,5,11,12,13]:
        text+=stand(d)+''.join(entry(d,j) for j in range(len(cs)))+'\n'
        if old==1:
            p=als[0]-als[1]; expr=f'{s(als[0])}-{s(als[1])}'
            text+=f'Both bounds exceed $m={s(m)}$. Subtract the nested right tails:\n'+display(f'P({s(xs[0])}<X<{s(xs[1])})\\approx{expr}={box(s(p))}.')+f'About ${s(100*p)}\\%$ of days use between ${f(xs[0])}$ and ${f(xs[1])}$ kWh above forecast.\n'
        elif old==2:
            p=sum(als);expr=f'{s(als[0])}+{s(als[1])}'
            text+='By symmetry, the left tail has the first printed area. Add the disjoint tails:\n'+display(f'P(X<{s(xs[0])}\\text{{ or }}X>{s(xs[1])})\\approx{expr}={box(s(p))}.')+f'About ${s(100*p)}\\%$ of weeks trigger an alert: revenue is more than ${f(abs(xs[0]))}$ thousand dollars below plan or ${f(xs[1])}$ thousand dollars above it.\n'
        elif old in [3,13]:
            p=als[0];expr=s(p)
            text+='By symmetry,\n'+display(('p_T=' if old==13 else '')+f'P(T<{f(cs[0],3)})\\approx{box(f(p,4) if old==13 else s(p))}.')
            if old==3:text+=f'About ${s(100*p)}\\%$ of trips arrive more than ${f(abs(xs[0]))}$ minutes early.\n'
        elif old in [4,11]:
            p=1-als[0];expr=f'1-{s(als[0])}'
            text+='Symmetry gives the excluded left tail; take its complement:\n'+display(('p_T=' if old==11 else '')+f'1-P(T<{f(cs[0],3)})\\approx{expr}={box(f(p,4) if old==11 else s(p))}.')
            if old==4:text+=f'About ${s(100*p)}\\%$ have costs above the threshold of approximately $\\${f(abs(xs[0]))}$ below budget. The cutoff is below $m={s(m)}$, so the right-tail event includes more than half the symmetric model.\n'
        elif old==5:
            p=als[1]-als[0];expr=f'{s(als[1])}-{s(als[0])}'
            text+=f'Both bounds lie below $m={s(m)}$. By symmetry the cumulative areas are ${s(als[0])}$ and ${s(als[1])}$:\n'+display(f'P({s(xs[0])}<X<{s(xs[1])})\\approx{expr}={box(s(p))}.')+f'About ${s(100*p)}\\%$ of shipments fall short of forecast by between ${f(abs(xs[1]))}$ and ${f(abs(xs[0]))}$ tonnes.\n'
        else:
            p=1-sum(als);expr=f'1-{s(als[0])}-{s(als[1])}'
            text+=f'The interval crosses $m={s(m)}$ and excludes unequal tails:\n'+display(f'p_T\\approx{expr}={box(f(p,4))}.')
        d.update(p=p,expr=expr)
        if old>=11:
            zs=[c.quantize(D('.01'),rounding=ROUND_HALF_UP) for c in cs];d['zs']=zs
            text+='For normal, round the standardized bound(s) to '+', '.join('$z='+f(z)+'$' for z in zs)+'.\n'+''.join(normalentry(z) for z in zs)+'\n'
            if old==11:
                pn=nt[abs(zs[0])]; ne=f'\\Phi({f(zs[0])})=1-{f(pn,4)},\\quad p_N=1-(1-{f(pn,4)})'
            elif old==13:
                pn=1-nt[abs(zs[0])];ne=f'p_N=1-{f(nt[abs(zs[0])],4)}'
            else:
                pn=nt[zs[1]]-(1-nt[abs(zs[0])]);ne=f'p_N={f(nt[zs[1]],4)}-(1-{f(nt[abs(zs[0])],4)})'
            text+=display(ne+'='+box(f(pn,4))+'.')+comparison(p,pn)
            ea=abs(p-pn); d.update(pn=pn,ea=ea)
            if old==11:text+=f'The event includes arrivals less than about ${f(abs(xs[0]))}$ minutes early and all late arrivals. Normal assigns ${f(100*pn)}\\%$, which is ${f(100*ea)}$ percentage points higher than $t$\'s ${f(100*p)}\\%$. Both exceed $0.5$ because the cutoff is below $m={s(m)}$; $t$ does not give the larger probability for this event.\n'
            elif old==12:text+=f'Fuel use lies from ${f(abs(xs[0]))}$ litres below forecast to ${f(xs[1])}$ litres above it with probability about ${f(100*p)}\\%$ under $t$ or ${f(100*pn)}\\%$ under normal. Normal assigns ${f(100*ea)}$ percentage points more to this interval.\n'
            else:text+=f'A shortfall greater than ${f(abs(xs[0]))}$ thousand dollars has probability about ${f(100*p)}\\%$ under $t$, compared with ${f(100*pn)}\\%$ under normal, a difference of ${f(100*ea)}$ percentage points.\n'
    else:
        text+=invstand(d)
        if old==6:text+='Each tail has probability $0.05/2=0.025$.\n'
        elif old in [10,14]:text+=('Each tail is $(1-0.90)/2=0.05$.\n' if old==10 else 'Each tail is $(1-0.95)/2=0.025$, so cumulative targets are $0.0250$ and $0.9750$.\n')
        elif old==8:text+='Use the two unequal tails separately.\n'
        elif old in [7,15]:text+=f'The lower-tail target is ${s(als[0])}$.\n'
        else:text+=f'The right-tail target is ${s(als[0])}$.\n'
        text+=''.join(entry(d,j) for j in range(len(cs)) if j==0 or als[j]!=als[j-1])+'\n'+('Obtain the negative cutoff by symmetry, giving ' if any(c<0 for c in cs) else 'The positive cutoff is ')+', '.join('$c='+f(c,3)+'$' for c in cs)+'.\n'
        if old>=14:
            if old==14:
                zs=[D('-1.96'),D('1.96')];text+=normalentry(zs[1])+'This matches $0.9750$ at printed precision; symmetry gives $\\Phi(-1.96)=0.0250$.\n'
            elif old==15:
                zs=[D('-1.64')];text+='For normal, row $1.6$, columns $0.04$ and $0.05$, gives $0.9495$ and $0.9505$. The negative cumulative entries are $0.0505$ and $0.0495$, equally close to $0.0500$. The tie rule selects $c_N=-1.64$.\n'
            else:
                zs=[D('1.28')];text+='Convert right tail $0.10$ to cumulative target $0.9000$. For normal, row $1.2$, column $0.08$, gives $\\Phi(1.28)=0.8997$, closer to $0.9000$ than $\\Phi(1.29)=0.9015$ (column $0.09$). Thus $c_N=1.28$.\n'
            d['zs']=zs
        text+='Back-transform, retaining unrounded values:\n'+back(d)
        if old>=14:
            text+=back(d,True)
            rns=[m+a*z for z in d['zs']];d['rns']=rns
            for j,(rt,rn) in enumerate(zip(xs,rns)):
                if old==14:text+='\\textbf{'+['Lower','Upper'][j]+' endpoint comparison:}\n'
                else:text+='Use unrounded contextual results:\n'
                text+=comparison(rt,rn,unit,','+['L','U'][j] if old==14 else '')
            if old==14:text+=f'The central intervals are approximately $({f(xs[0])},{f(xs[1])})$ kg under $t$ and $({f(rns[0])},{f(rns[1])})$ kg under normal, with $2.5\\%$ in each excluded tail. Negative limits mean below target mass; positive limits mean above it. The normal interval extends about ${f(abs(xs[0]-rns[0]))}$ kg less far from $m$ at each end. Percentage comparisons differ because the endpoint magnitudes differ.\n'
            elif old==15:text+=f'About $5\\%$ of batches save more than $\\${f(abs(xs[0]))}$ under $t$, or $\\${f(abs(rns[0]))}$ under normal. The normal threshold is about $\\${f(abs(xs[0]-rns[0]))}$ closer to the mean deviation.\n'
            else:text+=f'About $10\\%$ of orders take more than ${f(xs[0])}$ minutes above target under $t$, or ${f(rns[0])}$ minutes under normal. The normal cutoff is about ${f(abs(xs[0]-rns[0]))}$ minutes lower.\n'
        elif old==6:text+=f'About $2.5\\%$ of packages fall below $L$ and $2.5\\%$ above $U$. An alert means more than ${f(abs(xs[0]))}$ g under target or ${f(xs[1])}$ g over target.\n'
        elif old==7:text+=f'About $10\\%$ of days have costs more than $\\${f(abs(xs[0]))}$ below budget.\n'
        elif old==8:text+=f'About $1\\%$ depart more than ${f(abs(xs[0]))}$ minutes early, and $10\\%$ more than ${f(xs[1])}$ minutes late. The combined alert probability is $0.01+0.10=0.11$; $0.89$ lies between the limits.\n'
        elif old==9:text+=f'About $2.5\\%$ of jobs take more than ${f(xs[0])}$ minutes longer than target.\n'
        else:text+=f'About $90\\%$ lie between ${f(abs(xs[0]))}$ tonnes below forecast and ${f(xs[1])}$ tonnes above it, with $5\\%$ in each excluded tail.\n'
    solutions[old]=text

matrix=r'''\begin{center}
\begin{tabular}{|c|c|c|c|c|}
\hline
\textbf{Questions} & \textbf{C8} & \textbf{C9} & \textbf{C10} & \textbf{Total}\\\hline
1--10 & 10 & -- & -- & 10\\\hline
11--16 & -- & 12 & -- & 12\\\hline
17 & -- & -- & 6 & 6\\\hline
\textbf{Total} & \textbf{10} & \textbf{12} & \textbf{6} & \textbf{28}\\\hline
\end{tabular}
\end{center}'''
epre=eblocks[0].replace('Version 2','Version 3')
epre=re.sub(r'% Version 3 student exam;[^\n]*', '% Version 3 student exam; matching key: G11_T1_L3_C8C9C10_exam_solution_3.tex.',epre)
epre=re.sub(r'\\begin\{center\}.*?\\end\{center\}',lambda _:matrix,epre,count=1,flags=re.S)
epre=epre.replace('\\SubsectionBox{Criteria assessment}','\\SubsectionBox*{Criteria assessment}').replace('\\SubsectionBox{Conventions}','\\SubsectionBox*{Conventions}')
epre=epre.replace('\\begin{document}',r'''\usepackage{needspace}
% Account exactly for the three cells, six paddings and four rules.
\patchcmd{\ExamHeader}{\textwidth-6cm-4\tabcolsep-4\arrayrulewidth}
{\textwidth-5.6cm-6\tabcolsep-4\arrayrulewidth}{}{\errmessage{Header width patch failed}}
\let\VThreeSubsectionBox\SubsectionBox
\RenewDocumentCommand{\SubsectionBox}{s m}{%
\par\Needspace{5\baselineskip}%
\IfBooleanTF{#1}{\VThreeSubsectionBox*{#2}}{\VThreeSubsectionBox{#2}}%
}
\begin{document}''')
conventions=r'''
\textbf{Tables and rounding.} Use the supplied reference sheet, without interpolation.
Direct normal bounds: round $z$ to two decimals before lookup.
Inverse normal: choose the closest printed cumulative entry; at the
$0.0500/0.9500$ tie, choose $|z|=1.64$.
Retain three-decimal $t$ and two-decimal $z$ cutoffs.
Report C8 probabilities from the printed entries; C9 probabilities and their
$E_A$ to four decimals; contextual cutoffs and their $E_A$ to two decimals
with units; relative percentages to two decimals.
Use unrounded back-transformed values for comparisons.
All distribution results are approximations from rounded entries.
The models share scale $a$, not an actual variance; use $a$ directly.
For direct comparisons, $r_T,r_N$ are probabilities; for inverse comparisons,
they are contextual cutoffs (compare both interval endpoints separately).
Probability differences are $100E_A$ percentage points; $E_{Pt},E_{Pn}$
are relative percentages.
'''
epre+=conventions+'\n'
exam=epre
sp=oldsol[0].replace('Version 2','Version 3')
sp=re.sub(r'^%.*\n','',sp,flags=re.M)
sp=re.sub(r'\\begin\{center\}.*?\\end\{center\}',lambda _:matrix,sp,count=1,flags=re.S)
sp=sp.replace(' (and its PDF)','').replace('as in the C9 activity','as stipulated for this exam')
sol=sp
for new,old in enumerate(order,1):
    if old==17:
        exam+=eblocks[17].replace('\\SubsectionBox{17. ','\\SubsectionBox{')
        c10=oldsol[17].split('\\newpage\n\\section{Summarized Solutions}')[0]
        c10=c10.replace('\\needspace{12\\baselineskip}','\\needspace{48\\baselineskip}')
        c10=c10.replace('\\secInicio[sec:q17]','\\secInicio[][sec:q17]').replace('\\QuestionsTasks{','\\QuestionsTasks[sec:q17]{')
        sol+=c10
        continue
    d=data[old];crit=8 if old<=10 else 9;points=1 if crit==8 else 2
    exam+='\\noindent\\begin{minipage}{\\linewidth}\n'+f"\\SubsectionBox{{{d['title']} \\score{{C{crit}-\\sml{{{points}}}}}}}\n"+d['context']+'\n\\end{minipage}\\par\n\n'
    context,task=d['context'].split('\n',1)
    reserve=24 if crit==8 else (49 if new==14 else 38)
    sol+=f"\\needspace{{{reserve}\\baselineskip}}\n\\sectionScored{{{d['title']}}}{{C{crit}-\\sml{{{points}}}}}{{sec:q{new}}}\n{{\n{context}\n\\QuestionsTasks[sec:q{new}]{{\n{{{crit}}}/{{sol:q{new}}}/{{{task.strip()}}}\n}}\n\\needspace{{5\\baselineskip}}\n\\phantomsection\n\\label{{sol:q{new}}}\n\\subsection*{{C{crit} -- Problem {new}: {d['typ']} solution \\score{{{points}}}}}\n"+solutions[old]+f'\\secInicio[][sec:q{new}]\n}}\n\n'

# Retain the explanatory summary conventions and C10 summary verbatim.
summary_start=sol2.split('\\section{Summarized Solutions}',1)[1].split('\\needspace{18\\baselineskip}',1)[0]
sol+='\\newpage\n\\section{Summarized Solutions}'+summary_start
def table(headers,rows,spec):
    return '\\begin{tabularx}{\\linewidth}{'+spec+'}\n\\toprule\n'+headers+'\\\\\n\\midrule\n'+'\\\\\n'.join(rows)+'\\\\\n\\bottomrule\n\\end{tabularx}\n'
sol+='\\subsection*{C8}\n\\textbf{A. Direct probabilities --- Problems 1--5}\n\n'
rows=[]
for new in range(1,6):
    d=data[order[new-1]]
    ev=re.search(r'\$P\((.*?)\)\$',d['context'])
    ev=ev[1] if ev else f"X<{s(d['xs'][0])}\\text{{ or }}X>{s(d['xs'][1])}"
    rows.append(f"{new} & {d['df']} & ${ev}$ & "+'\\shortstack[l]{'+'\\\\'.join('$'+f(c,3)+'$' for c in d['cs'])+'}'+f" & ${d['expr']}$ & ${s(d['p'])}$")
sol+=table(r'Problem & $\nu$ & Event & Bound(s) & Area calculation & $P$ ($\approx$)',rows,r'@{}lr>{\raggedright\arraybackslash}Xllr@{}')
sol+='Event units (1--5): thousands of dollars, kWh, minutes, dollars, tonnes.\n\n\\medskip\n\\textbf{B. Inverse cutoffs and intervals --- Problems 6--10}\n\n'
rows=[]
for new in range(6,11):
    d=data[order[new-1]]
    target='; '.join(('left' if sign<0 else 'right')+' '+s(D(alpha)) for sign,alpha in d['cols'])
    rows.append(f"{new} & {d['df']} & {target} & "+'\\shortstack[l]{'+'\\\\'.join('$'+f(c,3)+'$' for c in d['cs'])+'} & '+'\\shortstack[l]{'+'\\\\'.join('$'+f(x)+'$' for x in d['xs'])+'} & '+d['unit'])
sol+=table(r'Problem & $\nu$ & Tail(s) & Signed $t$ & Result ($\approx$) & Units',rows,r'@{}lr>{\raggedright\arraybackslash}Xlll@{}')
sol+='For pairs, results are $(L,U)$ in order. Problem 8: outside $=0.01+0.10=0.11$; inside $=0.89$.\n'
sol+='\\newpage\n\\subsection*{C9}\n'+sol2.split('\\textbf{Comparison measures.}',1)[1].split('\\needspace{13\\baselineskip}',1)[0].join(['\\textbf{Comparison measures.}',''])
sol+='\\textbf{A. Direct model comparisons --- Problems 11--13}\n\n'
rows=[]
for new in range(11,14):
    d=data[order[new-1]];p,pn,ea=d['p'],d['pn'],d['ea']
    rows.append(f"{new} & {d['df']} & {f(p,4)} & {f(pn,4)} & {f(ea,4)} & {f(100*ea/p)}\\% & {f(100*ea/pn)}\\%")
sol+=table(r'Problem & $\nu$ & $p_T$ & $p_N$ & $E_A$ & $E_{Pt}$ & $E_{Pn}$',rows,r'@{}Xrrrrrr@{}')
sol+='All numerical results $\\approx$; probabilities and $E_A$ are unitless.\n\n'
for new in range(11,14):
    d=data[order[new-1]];sol+=f"Problem {new}: "+', '.join('$c='+f(c,3)+'\\to z='+f(z)+'$' for c,z in zip(d['cs'],d['zs']))+'.\\par\n'
sol+='\\medskip\n\\textbf{B. Inverse model comparisons --- Problems 14--16}\n\n'
rows=[]
for new in range(14,17):
    d=data[order[new-1]]
    for j,(rt,rn) in enumerate(zip(d['xs'],d['rns'])):
        ea=abs(rt-rn);ep=' / '+['$L$','$U$'][j] if new==14 else ' / $x$'
        rows.append(f'{new}{ep} & {f(rt)} & {f(rn)} & {f(ea)} & {f(100*ea/abs(rt))}\\% & {f(100*ea/abs(rn))}\\% & '+d['unit'])
sol+=table(r'Problem/endpoint & $r_T$ & $r_N$ & $E_A$ & $E_{Pt}$ & $E_{Pn}$ & Units',rows,r'@{}Xrrrrrl@{}')
sol+='All numerical results $\\approx$; contextual cutoffs and $E_A$ have the stated units.\n\n'
for new in range(14,17):
    d=data[order[new-1]];sol+=f"Problem {new} ($\\nu={d['df']}$): "+', '.join('$c_T='+f(c,3)+',\\ z='+f(z)+'$' for c,z in zip(d['cs'],d['zs']))+'.\\par\n'
sol+='Use unrounded back-transformed values for comparisons. For Problem 16, $r_T=8.425$, $r_N=8.20$, $E_A=0.225$ in selected working values.\n'
sol+='\\needspace{23\\baselineskip}\n\\subsection*{C10}'+sol2.split('\\subsection*{C10}',1)[1]
(dest/'G11_T1_L3_C8C9C10_exam_3.tex').write_text(exam,encoding='utf-8')
(dest/'G11_T1_L3_C8C9C10_exam_solution_3.tex').write_text(sol,encoding='utf-8')
serial={str(mapping[k]):{key: ([str(vv) for vv in val] if isinstance(val,list) else str(val)) for key,val in d.items() if key not in ['context','cols']} for k,d in data.items()}
(Path(__file__).parent/'calculations.json').write_text(json.dumps(serial,indent=2))
print('Created V3 sources; V2 -> V3:',mapping)
for new,old in enumerate(order[:-1],1):
    d=data[old]; print(new,'df',d['df'],'t',d['cs'],'x',d['xs'], 'normal',d.get('pn',d.get('rns','')), 'p',d.get('p',''))
