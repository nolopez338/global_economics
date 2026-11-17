from pathlib import Path
from fractions import Fraction as F
from itertools import product
import re
s=Path('book2026-2027/grade10/term_2/2-class_activities/G10_T2_L1_C2_classroom_activity.tex').read_text().split('\n\\ifprintsolutions\n')[1]
cases={2:([0,0,6,12,18,24,24],['.36','.14','.18','.12','.08','.07','.05']),3:([0,4,4,9,9,15],['.20','.12','.18','.15','.10','.25']),4:([0,5,10,15,15],['.15','.20',str(1-F('.15')-F('.20')-F('.20')-F('.10')),'.20','.10'])}
vals=[]; probs=[]
for bits in product([0,1],repeat=3):
 n=sum(bits); vals.append(7*n-(5 if n==3 else 0)); probs.append(F('.3')**n*F('.7')**(3-n))
cases[5]=(vals,probs)
vals=[];probs=[]
for r,p in [(17,'.20'),(0,'.30'),(7,'.50')]:
 for r2,p2 in [(0,'.4'),(7,'.6')]: vals.append(r+r2-7);probs.append(F(p)*F(p2))
cases[6]=(vals,probs)
for n,(vals,probs) in cases.items():
 probs=list(map(F,probs)); assert sum(probs)==1
 grouped={x:sum(p for y,p in zip(vals,probs) if y==x) for x in sorted(set(vals))}
 xs=list(grouped); mass=list(grouped.values()); cum=[];c=F(0)
 for p in mass: c+=p;cum.append(c)
 b=s.split('\\problemtitle{'+str(n)+'}')[1].split('\\problemtitle{')[0]
 graph=b.split('\\begin{axis}[classCDF')[1].split('\\end{axis}')[0]
 coords=re.findall(r'coordinates\s*\{([^;]*?)\};',graph,re.S)
 parse=lambda t:[(F(x),F(y)) for x,y in re.findall(r'\((-?[\d.]+),(-?[\d.]+)\)',t)]
 assert parse(coords[-1])==list(zip(map(F,xs),cum)),n
 assert parse(coords[-2])==list(zip(map(F,xs),[F(0)]+cum[:-1])),n
 for i in range(len(xs)-1): assert parse(coords[i+1])==[(F(xs[i]),cum[i]),(F(xs[i+1]),cum[i])]
 assert parse(coords[0])[-1]==(F(xs[0]),0)
 assert parse(coords[-3])[0]==(F(xs[-1]),1)
 # Every CDF table row has the expected cutoff and cumulative height.
 for i,x in enumerate(xs[:-1]):
  pat=rf'\${x}\\leq x<{xs[i+1]}\$ & \$\\cTwoCDFHL\{{([\d.]+)\}}'
  m=re.search(pat,b);assert m and F(m[1])==cum[i],(n,x)
 assert re.search(r'\$x\\geq\s*'+str(xs[-1])+r'\$ & \$\\cTwoCDFHL\{1\}',b)
 # Compare the PMF graph data and the grouped table against derived values.
 if n>2:
  m=re.search(r'xstep=1\]\{([^}]+)\}\{([^}]+)\}',b)
  assert list(map(F,m[1].split(',')))==list(map(F,xs))
  assert list(map(F,m[2].split(',')))==mass
 else:
  assert parse(re.search(r'fill=cTwoMassColor!20\]\s*coordinates\s*\{([^}]+)',b)[1])==list(zip(map(F,xs),mass))
 print(n,'support',xs,'PMF',list(map(str,mass)),'CDF',list(map(str,cum)),'PASS')
print('Exact arithmetic, independence, grouping, graph coordinates, CDF intervals and endpoints verified.')
