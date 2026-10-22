from pathlib import Path
from pypdf import PdfReader
from PIL import Image,ImageOps,ImageDraw
import re
b=Path('.exam-build-check/c8c9c10-solution')
r=PdfReader(b/'G10_T1_L2_C8C9C10_exam_solution.pdf')
print('Pages:',len(r.pages))
dests=r.named_destinations
bad=[];uri=[];internal=0
for n,p in enumerate(r.pages,1):
 t=p.extract_text()
 print(n, t[:65].replace('\n',' '), '...', t[-110:].replace('\n',' '))
 for ref in p.get('/Annots',[]):
  a=ref.get_object(); action=a.get('/A',{})
  if action.get('/S')=='/URI':uri.append(action.get('/URI'))
  d=a.get('/Dest') or action.get('/D')
  if isinstance(d,str):
   internal+=1
   if d not in dests:bad.append(d)
assert not bad,bad
assert uri==['https://nolopez338.github.io/global_economics/grade10/src/pages/term1/g10-t1-c10dashboard.html'],uri
assert Path('grade10/src/pages/term1/g10-t1-c10dashboard.html').is_file()
print('Internal links verified:',internal,'C10 URI:',uri)
# Independent enumeration from original payoff data.
a=[[120,25,-20],[85,65,10],[50,45,35],[70,75,20]]
p=[.2,.6,.2]
def stats(rows,prob):
 best=list(map(max,zip(*rows)))
 return [(max(x),min(x),max(v-y for v,y in zip(best,x)),sum(v*y for v,y in zip(prob,x))) for x in rows]
assert stats(a,p)==[(120,-20,55,35.0),(85,10,35,58.0),(50,35,70,44.0),(75,20,50,63.0)]
wins=[]
for subsidy in range(31):
 rows=[x.copy() for x in a]; rows[0][2]+=subsidy;rows[1][2]+=subsidy
 eligible=[i for i,x in enumerate(rows) if min(x)>=0]
 expected=[1,2,3] if subsidy<20 else [0,1,2,3]
 assert eligible==expected
 mins=[min(rows[i]) for i in eligible]
 winners=[i for i,v in zip(eligible,mins) if v==max(mins)]
 if winners==[1]:wins.append(subsidy)
 if subsidy==26: print('Q1 updated statistics:',stats(rows,p))
assert min(wins)==26
for g in range(48,81):
 st=stats([[80,10],[g,32]],[.4,.6])
 w=[i for i,x in enumerate(st) if x[2]==min(z[2] for z in st)]
 assert w==([0] if g<58 else [0,1] if g==58 else [1])
print('Q2 threshold: 59; boundary tie: 58; increase USD:',(59-48)*100)
# Fixed summary columns: Max, Min, Regret, EMV.
d=[[100,0,40,65],[90,10,30,65],[80,20,20,65],[70,30,30,59],[60,40,40,53],[50,30,50,43]]
f=[[120,0,45,61],[105,15,30,64.5],[95,25,25,68.5],[85,35,35,70],[75,45,45,64],[65,40,55,55]]
for name,data,rules,expected in [('D',d,[(3,2,True),(1,1,True)],[[1,2,3],[3]]),('F',f,[(2,5,False),(3,4,True),(0,2,True),(1,1,True)],[[1,2,3,4,5],[2,3,4,5],[2,3],[3]]),('H',f,[(1,4,True),(2,3,False),(0,2,True),(3,1,True)],[[3,4,5,6],[3,4,5],[3,4],[4]])]:
 alive=list(range(6))
 for (col,k,high),want in zip(rules,expected):
  cutoff=sorted([data[i][col] for i in alive],reverse=high)[k-1]
  alive=[i for i in alive if (data[i][col]>=cutoff if high else data[i][col]<=cutoff)]
  assert [i+1 for i in alive]==want
 print(name,'all filtering stages verified')
print('C8: 3+3=6; C9: 2+2+2=6; pass threshold 4 each.')
