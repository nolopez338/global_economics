from pathlib import Path
from itertools import combinations,product
p=Path('book2026-2027/grade10/term_2/1-practice_activities/G10_T2_L1_C2_practice_activity.tex')
s=p.read_text(encoding='utf-8')
data={
'fees':[('Cash','0.10','0'),('Debit card','0.20','1'),('Credit card','0.30','1'),('Mobile wallet','0.40','2')],
'bike':[('On time or early','0.10','0'),('1--10 min late','0.20','1'),('11--20 min late','0.30','1'),('Over 20 min late','0.40','2')],
'recycling':[('Non-recyclable','0.10','0'),('Paper','0.15','2'),('Cardboard','0.20','2'),('Plastic','0.25','5'),('Steel','0.10','5'),('Aluminium','0.20','9')],
'claims':[(f'{k} claim'+('' if k==1 else 's'),pr,str(min(2*k,6))) for k,pr in enumerate(['0.25','0.20','0.30','0.15','0.10'])],
'notebooks':[(w,'0.125',str(12 if w=='BBB' else 5*w.count('B'))) for w in ['NNN','BNN','NBN','NNB','BBN','BNB','NBB','BBB']],
'investment':[(f'$({a},{b})$',pr,str(a+b-4)) for a,b,pr in [(10,0,'0.18'),(10,4,'0.12'),(0,0,'0.12'),(0,4,'0.08'),(4,0,'0.30'),(4,4,'0.20')]],
'refund':[('No refund','1/6','0'),('2 USD refund','1/3','2'),('5 USD refund','1/2','5')],
}
tickets=[('A',0),('B',0),('C',0),('D',2),('E',2),('F',5),('G',5)]
data['prize']=[]
for c in combinations(tickets,3):
 vals=[x[1] for x in c]; x=min(10,sum(vals)+(3 if 2 in vals and 5 in vals else 0))
 data['prize'].append((''.join(x[0] for x in c),'1/35',str(x)))
data['maintenance']=[]
for cond in ['R','H']:
 for pat in product('WF',repeat=3):
  k=pat.count('F'); num=3**(3-k if cond=='R' else k)
  data['maintenance'].append((cond+': '+''.join(pat),f'{num}/128',str(min(6,max(0,(2 if cond=='R' else 5)*k-1)))))
notes={
'investment':r'Ordered returns in USD: $(\text{first},\text{second})$.',
'prize':r'Ticket labels: A, B, C: 0 USD; D, E: 2 USD; F, G: 5 USD. Each row is one unordered selection.',
'maintenance':r'R = routine, H = harsh; W = works, F = fails, in printer order.',
}
def table(rows,note='',width='.36',units='USD'):
 out=rf'''\begin{{minipage}}[t]{{{width}\linewidth}}\vspace{{0pt}}
\small\setlength{{\tabcolsep}}{{2pt}}
\begin{{tabularx}}{{\linewidth}}{{@{{}}>{{\raggedright\arraybackslash}}X cc@{{}}}}\toprule
$\cTwoOutcome{{\omega}}$ (outcome) & Probability & $\cTwoValue{{X}}$ (\cTwoValue{{{units}}}) \\\midrule
'''
 for w,pr,x in rows:
  if w.startswith('$'): w='$\\cTwoOutcome{'+w[1:-1]+'}$'
  else: w=r'\cTwoOutcome{'+w+'}'
  out+=w+' & $\\cTwoMassHL{'+pr+'}$ & $\\cTwoValue{'+x+'}$ \\\\\n'
 out+='\\bottomrule\\end{tabularx}\n'
 if note: out+='\\par\\small '+note+'\n'
 return out+'\\end{minipage}\\hfill'
for key,rows in data.items():
 a=s.index('\\stage{'+key+'}{1}')
 b=s.index('\\stage{'+key+'}{2}',a)
 part=s[a:b]
 start=part.index(r'\par\noindent\begin{minipage}')
 end=part.index(r'\end{minipage}\par',start)+len(r'\end{minipage}\par')
 row=part[start:end]
 row=row.replace(r'{.38\linewidth}',r'{.20\linewidth}',1).replace(r'{.33\linewidth}',r'{.20\linewidth}',1)
 row=row.replace(r'{.59\linewidth}',r'{.40\linewidth}',1).replace(r'{.64\linewidth}',r'{.40\linewidth}',1)
 # Only this PMF row gets tighter table spacing.
 row=row.replace(r'\vspace{0pt}\centering',r'\vspace{0pt}\centering\setlength{\tabcolsep}{3pt}',1)
 row=row.replace(r'\par\noindent',r'\par\noindent'+table(rows,notes.get(key,'')),1)
 # Less tall graphs preserve a comfortable aspect ratio at the new width.
 import re
 row=re.sub(r'height=[0-9.]+cm', 'height=4cm',row)
 part=part[:start]+row+part[end:]
 s=s[:a]+part+s[b:]
p.write_text(s,encoding='utf-8')
