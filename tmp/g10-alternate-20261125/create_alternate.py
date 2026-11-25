from pathlib import Path
import re, json, hashlib, itertools
from fractions import Fraction as F
from collections import defaultdict
from math import comb

root = Path(__file__).resolve().parents[2]
out = Path(__file__).resolve().parent
folder = root/'book2026-2027/grade10/term_2/4-learning_evidences'
stem = 'G10_T2_L1_C1C2_exam'
exam = (folder/(stem+'.tex')).read_text(encoding='utf-8')
sol = (folder/(stem+'_solution.tex')).read_text(encoding='utf-8')
artifacts = list((root/'book2026-2027/preamble').rglob('*')) + list(folder.rglob('*'))
artifacts += [p for p in root.rglob(stem+'*') if p.is_file()]
snapshot = {str(p.relative_to(root)):hashlib.sha256(p.read_bytes()).hexdigest() for p in artifacts if p.is_file()}
(out/'before.json').write_text(json.dumps(snapshot,indent=2),encoding='utf-8')
n=1
while any(root.rglob(stem+f'_{n}.*')) or any(root.rglob(stem+f'_solution_{n}.*')):
    n+=1
assert n == 1, 'Replan for the next unused index before rerunning.'

maps = [
 {0:0,1:2,4:5,5:7,6:9,11:16},
 {0:0,3:4,6:8,8:9,11:13,16:18},
 {0:0,2:3,4:6,7:10,11:15,16:21,23:29},
 {0:0,2:3,4:7,6:11,10:16,15:22,25:34},
 {0:0,2:3,5:7,9:12,14:18,20:27},
 {0:0,5:6,7:8,10:12,12:14,15:18,17:20,22:26,24:28,25:30,29:34,36:42},
]
contexts = [
 [('Online order contribution','Meal reservation contribution'),('A small seller','A meal vendor'),('the seller','the vendor'),('three orders','three meal reservations'),('Each order','Each reservation'),('every order','every reservation'),('kept order','kept reservation'),('two orders','two reservations')],
 [('Two supplier loyalty credits','Two distributor promotional credits'),('A retailer','A bookshop'),('The retailer','The bookshop'),('suppliers','distributors'),('supplier','distributor'),('loyalty','promotional')],
 [('Local parcel delivery fees','Produce crate delivery fees'),('A cooperative','A farm cooperative'),('one parcel','one produce crate'),('the parcel','the crate'),('for a parcel','for a crate')],
 [('Warranty service payouts','Equipment protection payouts'),('A warranty provider','An equipment protection provider')],
 [('Marketplace account credits','Travel platform account credits'),('a marketplace','a travel platform'),('one purchase','one booking')],
 [('Community market prize tickets','Library fundraiser prize tickets'),('A community market','A library fundraiser')],
]
def context(s,i):
    for a,b in contexts[i]: s=s.replace(a,b)
    return s

# Establish new prompts in memory. Source solution makes independence explicit.
parts = re.split(r'(?=\\SubsectionBox\{)',exam)
assert len(parts)==7
questions=[]
for i,p in enumerate(parts[1:]):
    p=p.split('\\end{multicols*}')[0]
    p=p.replace('\\columnbreak','').strip()
    if i==0:
        p=p.replace('Each order has','Each order independently has')
        p=p.replace('probability 0.6','probability TEMP').replace('probability 0.4','probability 0.6').replace('probability TEMP','probability 0.4')
    # Only context and task text, never criterion/point macros or labels.
    lines=p.splitlines()
    for j,line in enumerate(lines):
        if not line.startswith('\\') or line.startswith('\\item'):
            # Leave inline score and allocation values unchanged.
            chunks=re.split(r'(\\sscore\{.*|\\textbf\{Allocation:.*)',line)
            chunks[0]=re.sub(r'(?<![\w.])\d+(?![\w.])',lambda m:str(maps[i].get(int(m[0]),int(m[0]))),chunks[0])
            lines[j]=''.join(chunks)
    p=context('\n'.join(lines),i)
    questions.append(p)

# Recalculate each distribution independently from the new givens.
pmfs=[]
d=defaultdict(F)
for w in itertools.product('KC',repeat=3):
    k=w.count('K'); d[7*k-5]+=F(2,5)**k*F(3,5)**(3-k)
pmfs.append(dict(sorted(d.items())))
d=defaultdict(F)
for a,pa in zip([0,4,9],[F(1,5),F(1,2),F(3,10)]):
    for b,pb in zip([0,4,9],[F(2,5),F(2,5),F(1,5)]): d[a+b]+=pa*pb
pmfs.append(dict(sorted(d.items())))
for xs,ps in [([0,0,3,6,10,15,21,29],[2,2,3,4,3,2,2,2]),([0,3,7,11,16,22,22,34],[4,2,3,3,2,3,1,2]),([0,3,7,12,18,27],[1,2,3,6,3,5])]:
    d=defaultdict(F)
    for x,p in zip(xs,ps): d[x]+=F(p,20)
    pmfs.append(dict(sorted(d.items())))
d=defaultdict(F); compositions=[]
for c in range(3):
    for b in range(4-c):
        a=3-b-c; count=comb(4,a)*comb(3,b)*comb(2,c)
        face=6*b+14*c; bonus=8 if b and c else 0; adjusted=face+bonus; x=min(adjusted,30)
        compositions.append([a,b,c,count,face,bonus,adjusted,x]); d[x]+=F(count,84)
pmfs.append(dict(sorted(d.items())))
assert [len(d) for d in pmfs]==[4,6,7,7,6,7]
assert all(sum(d.values())==1 and min(d.values())>0 for d in pmfs)
assert pmfs[0][9]==F(36,125) and pmfs[1][13]==F(11,50)
assert pmfs[5][28]==F(28,84) and pmfs[5][30]==F(9,84)
assert sum(r[3] for r in compositions)==comb(9,3)==84
expected = [[-5,2,9,16],[0,4,8,9,13,18],[0,3,6,10,15,21,29],[0,3,7,11,16,22,34],[0,3,7,12,18,27],[0,6,12,14,18,28,30]]
assert [list(d) for d in pmfs]==expected

def transform_solution(s,i):
    mp=maps[i]
    s=context(s,i)
    # Semantic monetary roles, including mathematical arguments.
    for role in ['GTenHLValue','GTenHLSecond'] + (['GTenHLOutcome'] if i==1 else []):
        s=re.sub(r'\\'+role+r'\{(\d+)( USD)?\}',lambda m:'\\'+role+'{'+str(mp.get(int(m[1]),int(m[1])))+(m[2] or '')+'}',s)
    s=re.sub(r'p_X\((\d+)\)',lambda m:'p_X('+str(mp.get(int(m[1]),int(m[1])))+')',s)
    if i==0:
        prob={'0.6':'0.4','0.4':'0.6','3/5':'2/5','2/5':'3/5','27/125':'8/125','8/125':'27/125','18/125':'12/125','12/125':'18/125','36/125':'54/125','54/125':'36/125','0.216':'0.064','0.064':'0.216','0.144':'0.096','0.096':'0.144','0.432':'0.288','43.2\\%':'28.8\\%','8':'27','36':'54','54':'36','27':'8'}
        s=re.sub(r'\\GTenHLProbability\{([^{}]+)\}',lambda m:r'\GTenHLProbability{'+prob.get(m[1],m[1])+'}',s)
        s=s.replace('$X=6$','$X=9$')
    if i==1: s=s.replace('$X=11$','$X=13$').replace('an \\GTenHLValue{9 USD}','a \\GTenHLValue{9 USD}')
    # Graph x coordinates and horizontal monetary ticks, leaving probabilities intact.
    def graph(g):
        oldright=int(re.search(r'xmax=(\d+)',g)[1])
        g=re.sub(r'xtick=\{([\d,]+)\}',lambda m:'xtick={'+','.join(str(mp.get(int(v),int(v))) for v in m[1].split(','))+'}',g)
        g=re.sub(r'xmax=(\d+)',lambda m:'xmax='+str(max(expected[i])+2),g)
        def coord(m):
            x=float(m[1]); nearest=min(mp,key=lambda v:abs(v-x))
            nx=max(expected[i])+2 if x==oldright else (mp[nearest]+x-nearest if abs(x-nearest)<.5 else x)
            return m[0].replace(m[1],f'{nx:g}',1)
        g=re.sub(r'(?:axis cs:|\()(-?\d+(?:\.\d+)?),',coord,g)
        return g
    s=re.sub(r'\\begin\{tikzpicture\}.*?\\end\{tikzpicture\}',lambda m:graph(m[0]),s,flags=re.S)
    if i==5:
        s=s.replace('with values 0, 5 and','with values 0, 6 and').replace('zero-, five- and twelve-dollar','zero-, six- and fourteen-dollar').replace('amounts 29 and','amounts 34 and')
    return s

sections=re.split(r'(?=\\sectionScored\{)',sol)
assert len(sections)==7
newsections=[]
for i,s in enumerate(sections[1:]):
    s=transform_solution(s,i)
    q=questions[i]
    title=re.search(r'\\SubsectionBox\{(.*?)\\score',q)[1]
    prompt=q.split('\\QuestionLabel{q:'+str(i+1)+'}')[1].split('\\begin{enumerate}')[0].strip()
    tasks=re.findall(r'\\item (.*?) \\sscore\{',q,flags=re.S)
    assert len(tasks)==3
    # Exact new question wording in both files; preserve solution layout and highlights in answers.
    s=re.sub(r'(\\sectionScored\{)[^}]+',lambda m:m[1]+title,s,count=1)
    headend=s.index('\n',s.index('\\sectionScored'))
    nexthead=s.index('\\Needspace',headend)
    s=s[:headend]+'\n\n'+prompt+'\n\n'+s[nexthead:]
    counter=[0]
    def task_prompt(m):
        task=tasks[counter[0]].strip(); counter[0]+=1
        return r'\noindent\textbf{\boldmath '+task+r'}\par\nopagebreak'
    s=re.sub(r'\\noindent\\textbf\{\\boldmath .*?\}\\par\\nopagebreak',task_prompt,s,flags=re.S)
    assert counter[0]==3
    newsections.append(s)

front=sections[0].replace('This standalone key authors the original questions required by the governing assessment brief and reproduces each task before its worked solution.','This key reproduces each alternate question before its worked solution.')
policy=re.search(r'This exam assesses C1 and C2\..*?(?=\n\n)',exam,re.S)[0]
front=front.replace('All contextual rules are stated in ordinary language.','All contextual rules are stated in ordinary language.\n\n'+policy)
front=front.replace('Every task-level split and partial-credit breakdown below is proposed.','Task totals match the student exam; detailed partial-credit breakdowns below are proposed.')
solution=front+''.join(newsections)
solution=solution.replace('% Original assessment and worked key governed by the supplied assessment brief.','% Alternate 1, derived directly from the original exam-solution pair.')
sp=folder/(stem+f'_solution_{n}.tex')
ep=folder/(stem+f'_{n}.tex')
assert not sp.exists() and not ep.exists()
with sp.open('x',encoding='utf-8',newline='\n') as f: f.write(solution)

# Verify all rendered PMF-table rows in the solution against exact independent arithmetic.
for i,s in enumerate(newsections):
    rows=re.findall(r'\$\\GTenHLValue\{(\d+)\}\$ & \$\\GTenHLProbability\{(\d+/\d+)\}',s)
    if i>=2:
        assert {int(x):F(p) for x,p in rows}==pmfs[i], (i,rows,pmfs[i])
report={'index':n,'pmfs':[{str(x):str(p) for x,p in d.items()} for d in pmfs],'q6_compositions':compositions,'totals':{'C1':6,'C2':14,'overall':20},'selection_questions':[]}
for i,(lo,hi) in enumerate([(10,21),(11,22),(12,18),(14,28)],2):
    report[f'q{i+1}_probabilities']=[str(sum(p for x,p in pmfs[i].items() if x<lo)),str(sum(p for x,p in pmfs[i].items() if x>=hi))]
(out/'calculation-checks.json').write_text(json.dumps(report,indent=2),encoding='utf-8')

# Derive the student exam only after the complete alternate solution is verified.
student=parts[0]+('\n\\columnbreak\n'.join(questions[:3]))+'\n\n'+questions[3]+'\n\\columnbreak\n'+questions[4]+'\n\n'+questions[5]+'\n\\end{multicols*}\n\\end{document}\n'
student=student.replace('% Student assessment reconstructed from the complete matching solution PDF.','% Alternate 1, derived from the verified alternate worked solution.')
for i,s in enumerate(newsections):
    prompt=questions[i].split('\\QuestionLabel{q:'+str(i+1)+'}')[1].split('\\begin{enumerate}')[0].strip()
    assert prompt in s
    for task in re.findall(r'\\item (.*?) \\sscore\{',questions[i],flags=re.S): assert task.strip() in s
with ep.open('x',encoding='utf-8',newline='\n') as f: f.write(student)
print('Created shared index',n)
print(json.dumps(report,indent=2))
