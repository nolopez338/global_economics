from pathlib import Path
from decimal import Decimal as D
import re, json, hashlib

ROOT=Path.cwd()
DEST=ROOT/'book/grade11/term_2/4-learning_evidences'
WORK=ROOT/'tmp/exam-alternate-g11-1'
STEM='G11_T2_L1_C1C2_exam'
exam=(DEST/(STEM+'.tex')).read_text(encoding='utf-8')
solution=(DEST/(STEM+'_solution.tex')).read_text(encoding='utf-8')

def digest(p): return hashlib.sha256(p.read_bytes()).hexdigest()
# Snapshot all existing artifacts in the source/output tree, and shared inputs.
prior={str(p.relative_to(ROOT)):digest(p) for folder in [DEST,ROOT/'book/preamble'] for p in folder.rglob('*') if p.is_file()}
(WORK/'preexisting-sha256.json').write_text(json.dumps(prior,indent=2),encoding='utf-8')
def occupied(i):
    stems={f'{STEM}_{i}',f'{STEM}_solution_{i}'}
    return any(any(p.name==s or p.name.startswith(s+'.') for s in stems) for base in [DEST,ROOT/'output',ROOT/'tmp'] if base.exists() for p in base.rglob('*') if p.is_file())
i=1
while occupied(i): i+=1

old=[dict(N=200000,n=100,a=240,b=252,sa=58,sb=66,ka=40,kb=55,sigma=60,mu=245,cs=['.95'],zs=['1.960'],centers=[236,244,250,258,230,247,242,254,233,246]),
     dict(N=500000,n=144,a=82,b=79,sa=33,sb=39,ka=54,kb=72,sigma=36,mu=84,cs=['.90','.99'],zs=['1.645','2.576'],cats=[176,20,4]),
     dict(N=100000,n=64,a=32,b=34,sa=7,sb=9,ka=24,kb=32,sigma=8,mu=33,cs=['.95'],zs=['1.960'],centers=[32,33,34,35,32.5])]
new=[dict(N=280000,n=196,a=310,b=326,sa=92,sb=103,ka=49,kb=98,sigma=98,mu=315,cs=['.98'],zs=['2.326'],centers=[300,312,320,334,302,318,308,330,298,316]),
     dict(N=800000,n=400,a=110,b=105,sa=74,sb=83,ka=120,kb=260,sigma=80,mu=113,cs=['.80','.98'],zs=['1.282','2.326'],cats=[185,55,10]),
     dict(N=250000,n=100,a=46,b=51,sa=12,sb=16,ka=20,kb=45,sigma=15,mu=48,cs=['.90'],zs=['1.645'],centers=[46,48,49,51,45])]
def f(x):
    s=format(D(str(x)),'f')
    return s.rstrip('0').rstrip('.') if '.' in s else s
def derive(d):
    d=d.copy()
    for k in ['N','n','a','b','sa','sb','ka','kb','sigma','mu']: d[k]=D(str(d[k]))
    d['cs']=list(map(D,d['cs'])); d['zs']=list(map(D,d['zs']))
    d['pa']=d['ka']/d['n']; d['pb']=d['kb']/d['n']
    d['dm']=d['b']-d['a']; d['ds']=d['sb']-d['sa']; d['dp']=100*(d['pb']-d['pa'])
    d['se']=d['sigma']/d['n'].sqrt()
    d['moe']=[z*d['se'] for z in d['zs']]
    d['L']=[d['a']-m for m in d['moe']];d['U']=[d['a']+m for m in d['moe']];d['W']=[2*m for m in d['moe']]
    if 'centers' in d:
        d['centers']=list(map(lambda x:D(str(x)),d['centers']))
        d['intervals']=[(x-d['moe'][0],x+d['moe'][0]) for x in d['centers']]
        d['flags']=[l<=d['mu']<=u for l,u in d['intervals']]
        d['counts']=[sum(d['flags'])];d['total']=len(d['centers'])
    else:
        d['counts']=[d['cats'][0],sum(d['cats'][:2])];d['total']=sum(d['cats'])
    d['cov']=[D(k)/d['total']*100 for k in d['counts']]
    d['err']=[abs(v-100*c) for v,c in zip(d['cov'],d['cs'])]
    return d
old=list(map(derive,old));new=list(map(derive,new))

# Build a step-by-step audit from explicit dependencies, with unchanged arity.
rows=[]
def step(q,name,op,deps,reason,ov,nv,ofixed=()):
    oa,orr=ov;na,nrr=nv
    assert len(oa)==len(na)
    repeated=[]
    for j,(a,b) in enumerate(zip(oa,na)):
        if D(str(a))==D(str(b)):
            assert j in ofixed,(q,name,j,a,b)
            repeated.append(j+1)
    if D(str(orr))==D(str(nrr)):
        assert ofixed,(q,name,'result repeats')
    rows.append(dict(question=q,step=name,operation=op,dependencies=deps,reasoning=reason,operand_count=len(oa),source_operands=list(map(f,oa)),alternate_operands=list(map(f,na)),source_result=f(orr),alternate_result=f(nrr),fixed_operand_positions=repeated))
for q,(o,n) in enumerate(zip(old,new),1):
    for role in ['pa','pb']:
        k='ka' if role=='pa' else 'kb'
        step(q,role,'division',[k,'n'],'Condition count divided by corresponding sample size',([o[k],o['n']],o[role]),([n[k],n['n']],n[role]))
    for role,ks in [('dm',['b','a']),('ds',['sb','sa'])]:
        step(q,role,'subtraction',ks,'Second minus initial; preserve sign',([o[k] for k in ks],o[role]),([n[k] for k in ks],n[role]))
    step(q,'proportion difference','subtraction',['pb','pa'],'Difference in unitless shares',([o['pb'],o['pa']],o['dp']/100),([n['pb'],n['pa']],n['dp']/100))
    step(q,'dp','multiplication',['proportion difference','100'],'Convert share to percentage points',([o['dp']/100,100],o['dp']),([n['dp']/100,100],n['dp']),(1,))
    step(q,'sqrt(n)','square root',['n'],'Standard error denominator',([o['n']],o['n'].sqrt()),([n['n']],n['n'].sqrt()))
    step(q,'se','division',['sigma','sqrt(n)'],'Use known population SD',([o['sigma'],o['n'].sqrt()],o['se']),([n['sigma'],n['n'].sqrt()],n['se']))
    step(q,'sampling fraction','division',['n','N'],'Negligible fraction of fixed population',([o['n'],o['N']],o['n']/o['N']),([n['n'],n['N']],n['n']/n['N']))
    for j,(oc,nc) in enumerate(zip(o['cs'],n['cs'])):
        step(q,f'alpha[{j}]','subtraction',['1','C'],'Complement of confidence',([1,oc],1-oc),([1,nc],1-nc),(0,))
        step(q,f'tail[{j}]','division',['alpha','2'],'Two equal tails',([1-oc,2],(1-oc)/2),([1-nc,2],(1-nc)/2),(1,))
        step(q,f'z[{j}]','lookup',['C'],'Use unchanged supplied reference table',([oc],o['zs'][j]),([nc],n['zs'][j]))
        for role,op,ks,oa,na in [
            ('moe','multiplication',['z','se'],[o['zs'][j],o['se']],[n['zs'][j],n['se']]),
            ('L','subtraction',['a','moe'],[o['a'],o['moe'][j]],[n['a'],n['moe'][j]]),
            ('U','addition',['a','moe'],[o['a'],o['moe'][j]],[n['a'],n['moe'][j]]),
            ('W','subtraction',['U','L'],[o['U'][j],o['L'][j]],[n['U'][j],n['L'][j]])]:
            step(q,f'{role}[{j}]',op,ks,'Same known-SD interval method',(oa,o[role][j]),(na,n[role][j]))
        step(q,f'width identity[{j}]','multiplication',['2','moe'],'Symmetric interval width',([2,o['moe'][j]],o['W'][j]),([2,n['moe'][j]],n['W'][j]),(0,))
        step(q,f'coverage fraction[{j}]','division',['covering count','total'],'Subsequent studies only',([o['counts'][j],o['total']],o['cov'][j]/100),([n['counts'][j],n['total']],n['cov'][j]/100),(1,) if q!=2 else ())
        step(q,f'coverage percent[{j}]','multiplication',['coverage fraction','100'],'Convert fraction to percent',([o['cov'][j]/100,100],o['cov'][j]),([n['cov'][j]/100,100],n['cov'][j]),(1,))
        step(q,f'coverage gap[{j}]','subtraction',['observed percent','nominal percent'],'Signed difference before absolute value',([o['cov'][j],100*oc],o['cov'][j]-100*oc),([n['cov'][j],100*nc],n['cov'][j]-100*nc))
        step(q,f'absolute gap[{j}]','absolute value',['coverage gap'],'Distance in percentage points',([o['cov'][j]-100*oc],o['err'][j]),([n['cov'][j]-100*nc],n['err'][j]))
    if q==2:
        for name,indices in [('higher cover',[0,1]),('lower misses',[1,2]),('category total',[0,1,2])]:
            step(q,name,'addition',[f'category {k+1}' for k in indices],'Preserve mutually exclusive nested categories',([o['cats'][k] for k in indices],sum(o['cats'][k] for k in indices)),([n['cats'][k] for k in indices],sum(n['cats'][k] for k in indices)))
    else:
        for r,((ol,ou),(nl,nu)) in enumerate(zip(o['intervals'],n['intervals']),1):
            # Endpoint generation and center recovery have the same arity.
            for name,op,oa,na,orr,nrr in [('L','subtraction',[o['centers'][r-1],o['moe'][0]],[n['centers'][r-1],n['moe'][0]],ol,nl),('U','addition',[o['centers'][r-1],o['moe'][0]],[n['centers'][r-1],n['moe'][0]],ou,nu),('width','subtraction',[ou,ol],[nu,nl],ou-ol,nu-nl),('endpoint sum','addition',[ol,ou],[nl,nu],ol+ou,nl+nu),('center','division',[ol+ou,2],[nl+nu,2],o['centers'][r-1],n['centers'][r-1])]:
                step(q,f'study {r} {name}',op,['corresponding interval inputs'],'Same symmetric construction and retrospective comparison',(oa,orr),(na,nrr),(1,) if name=='center' else ())
        rows.append(dict(question=q,step='coverage tests and count',operation='inclusive comparisons, then count',dependencies=['each L','mu','each U'],reasoning='No endpoint equality in either version; equality rule retained',operand_count=3,source_operands=[[f(l),f(o['mu']),f(u)] for l,u in o['intervals']],alternate_operands=[[f(l),f(n['mu']),f(u)] for l,u in n['intervals']],source_result=o['flags'],alternate_result=n['flags']))

(WORK/'solution-step-comparison.json').write_text(json.dumps(rows,indent=2),encoding='utf-8')

# Role-specific replacements; calculate every new result before editing text.
num_re=re.compile(r'(?<![A-Za-z\d.])\d{1,3}(?:,\d{3})+(?:\.\d+)?|(?<![A-Za-z\d.])\d+(?:\.\d+)?')
def numreplace(s,m):
    return num_re.sub(lambda a:m.get(a.group(),a.group()),s)
def transform(s,q):
    o,n=old[q-1],new[q-1]
    # Never transform TeX dimensions, labels, marks, layout parameters or rubric.
    macros={
        'Pop':{f(o['N']):f(n['N']),f'{int(o["N"]):,}':f'{int(n["N"]):,}'},
        'Sam':{f(o[k]):f(n[k]) for k in ['n','ka','kb']},
        'CtwoSize':{f(o['n']):f(n['n'])},
        'CtwoPoint':{f(o[k]):f(n[k]) for k in ['a','b','dm']},
        'SSD':{f(o[k]):f(n[k]) for k in ['sa','sb','ds']},
        'CtwoSD':{f(o['sigma']):f(n['sigma'])},
        'CtwoMean':{f(o['mu']):f(n['mu'])},
        'CtwoSE':{f(o['se']):f(n['se'])},
        'SP':{f(o[k]*factor):f(n[k]*factor) for k,factor in [('pa',1),('pb',1),('pa',100),('pb',100),('dp',1)]},
        'CtwoConfidence':{f(oc*factor):f(nc*factor) for oc,nc in zip(o['cs'],n['cs']) for factor in [1,100]},
        'CtwoSignificance':{f((1-oc)/factor):f((1-nc)/factor) for oc,nc in zip(o['cs'],n['cs']) for factor in [1,2]},
        'CtwoCritical':{f(oz):f(nz) for oz,nz in zip(o['zs'],n['zs'])},
        'CtwoMoE':{f(om):f(nm) for om,nm in zip(o['moe'],n['moe'])},
        'CtwoEndpoint':{f(ov):f(nv) for role in ['L','U'] for ov,nv in zip(o[role],n[role])},
        'CtwoCI':{f(ov):f(nv) for role in ['L','U'] for ov,nv in zip(o[role],n[role])},
        'CtwoWidth':{f(ov):f(nv) for ov,nv in zip(o['W'],n['W'])},
        'CtwoCoverage':{f(ov):f(nv) for role in ['counts','cov'] for ov,nv in zip(o[role],n[role])},
        'CtwoError':{f(ov):f(nv) for ov,nv in zip(o['err'],n['err'])},
    }
    # Original spelling variants of decimal settings.
    for oc,nc in zip(o['cs'],n['cs']):
        macros['CtwoSignificance'][format(1-oc,'.2f')]=format(1-nc,'.2f')
    for oz,nz in zip(o['zs'],n['zs']): macros['CtwoCritical'][format(oz,'.3f')]=format(nz,'.3f')
    if q!=2:
        for (ol,ou),(nl,nu) in zip(o['intervals'],n['intervals']):
            for macro in ['CtwoEndpoint']:
                macros[macro].update({f(ol):f(nl),f(ou):f(nu)})
    else:
        macros['CtwoCoverage'].update({str(a):str(b) for a,b in zip([176,20,4,24,196,200],[185,55,10,65,240,250])})
    saved=[]
    def protect(m):
        macro,content=m.group(1),m.group(2)
        revised='\\'+macro+'{'+numreplace(content,macros[macro])+'}'
        saved.append(revised)
        return f'@@H{chr(0xE000+len(saved)-1)}@@'
    pattern=r'\\('+'|'.join(macros)+r')\{([^{}]*)\}'
    s=re.sub(pattern,protect,s)
    # Raw prose and tables: large data values, and confidence settings only.
    raw={}
    for k in ['N','n','a','b','sa','sb','ka','kb','sigma','mu']:
        if o[k]>=10: raw[f(o[k])]=f(n[k])
    raw[f'{int(o["N"]):,}']=f'{int(n["N"]):,}'
    raw[f(o['n']/o['N']*100)]=f(n['n']/n['N']*100)
    for oc,nc in zip(o['cs'],n['cs']): raw[f(100*oc)]=f(100*nc)
    for oz,nz in zip(o['zs'],n['zs']): raw[format(oz,'.3f')]=format(nz,'.3f')
    for role in ['moe','L','U','W']:
        for ov,nv in zip(o[role],n[role]): raw[f(ov)]=f(nv)
    if q!=2:
        for (ol,ou),(nl,nu) in zip(o['intervals'],n['intervals']): raw.update({f(ol):f(nl),f(ou):f(nu)})
    else: raw.update({str(a):str(b) for a,b in zip([176,20,24,196,200],[185,55,65,240,250])})
    def raw_line(line):
        if any(x in line for x in ['\\hsize','\\linewidth','\\Needspace','\\vspace','\\sscore','\\taskprompt','\\score','\\label','\\secInicio','\\subsection*','\\sectionScored','\\begin{','\\end{']): return line
        # Preserve conversion constant 100 and structural numbers; all n roles
        # in ordinary prose are followed by a contextual noun.
        if q==1:
            line=re.sub(r'\b100(?= businesses|;)', '196',line)
            local={k:v for k,v in raw.items() if k!='100'}
        else: local=raw
        return numreplace(line,local)
    s='\n'.join(raw_line(line) for line in s.split('\n'))
    for j,value in enumerate(saved): s=s.replace(f'@@H{chr(0xE000+j)}@@',value)
    s=s.replace('October','September')
    if q==2: s=s.replace('September 31','September 30').replace('Two hundred subsequent','Two hundred fifty subsequent')
    if q==3: s=s.replace('November 2','November 5')
    return s

def replace_body(text,starts):
    # Transform problem bodies and summaries independently; leave every rubric.
    for q,start,end in reversed(starts):
        segment=text[start:end]
        rubric=segment.find('\\subsection*{Proposed partial-credit guidance')
        if rubric>=0:
            segment=transform(segment[:rubric],q)+segment[rubric:]
        else:segment=transform(segment,q)
        text=text[:start]+segment+text[end:]
    return text

def ranges(text,solution_mode=False):
    if solution_mode:
        starts=[text.index('\\sectionScored{'+title) for title in ['Retail electricity','Savings-account','Create an integrated']]
        summary=text.index('\\section{Summarized Solutions}')
        out=[(q+1,s,starts[q+1] if q<2 else summary) for q,s in enumerate(starts)]
        ss=[text.index('\\subsection*{Problem '+str(q)+':') for q in [1,2,3]]
        out.extend((q+1,s,ss[q+1] if q<2 else text.index('\\end{document}')) for q,s in enumerate(ss))
        return out
    starts=[text.index('\\SubsectionBox{'+title) for title in ['Retail electricity','Savings-account','Create an integrated']]
    return [(q+1,s,starts[q+1] if q<2 else text.index('\\end{multicols}')) for q,s in enumerate(starts)]

sol=replace_body(solution,ranges(solution,True))
# Fix small raw values by their explicit semantic roles, never globally.
sol=sol.replace('Neither confidence level&4','Neither confidence level&10')
sol=sol.replace('1 percentage point below','2 percentage points below')
sol=sol.replace('2 percentage points below \\CtwoConfidence{nominal confidence}. The 98', '6 percentage points below \\CtwoConfidence{nominal confidence}. The 98')
sol=sol.replace('all four misses at 98','all ten misses at 98')
sol=sol.replace('185+55+4=250','185+55+10=250')
sol=sol.replace('distances from 113 of 0, 6 and 9','distances from 113 of 1, 7 and 11')
# Counts/proportions in the construction example need independent roles.
sol=sol.replace('and 46 insured deliveries','and 45 insured deliveries')
sol=sol.replace('assigned to 20 and 46','assigned to 20 and 45')
sol=sol.replace('sample standard deviation 7 thousand','sample standard deviation 12 thousand').replace('sample standard deviation 9 thousand','sample standard deviation 16 thousand')
sol=sol.replace('delivery fees as 8 thousand','delivery fees as 15 thousand')
sol=sol.replace('with 46 values at $m-d$ and 46 at $m+d$','with 50 values at $m-d$ and 50 at $m+d$')
sol=sol.replace('\\sqrt{63/100}','\\sqrt{99/100}').replace('6.9451<46','11.9398<46').replace('8.9294<51','15.9198<51')

# Update coverage classification rows from new endpoints; then the raw count.
for q in [1,3]:
    o,n=old[q-1],new[q-1]
    for r,((l,u),flag) in enumerate(zip(n['intervals'],n['flags']),1):
        prefix=rf'{r}&$\CtwoEndpoint{{{f(l)}}}$&$\CtwoEndpoint{{{f(u)}}}$&\CtwoCoverage{{'
        sol=re.sub(re.escape(prefix)+r'(?:Yes|No)\}',lambda m:prefix+('Yes' if flag else 'No')+'}',sol)
    # Small plain counts occur only in this exact equation.
    sol=sol.replace(r'\CtwoCoverage{N_{\mathrm{cover}}}='+str(o['counts'][0]),r'\CtwoCoverage{N_{\mathrm{cover}}}='+str(n['counts'][0]))

# Match student-facing task wording and reproduce the full shared task formats.
for macro in ['cOneA','cOneB','cTwoA','cTwoB','cTwoC']:
    pat=r'\\newcommand\{\\'+macro+r'\}\{[^\n]*\}'
    sol=re.sub(pat,lambda _:re.search(pat,exam).group(),sol)
general=exam[exam.index('\\SubsectionBox*{General tasks'):exam.index('\\SubsectionBox*{Task reference material}')]
general=general[general.index('\n')+1:].replace('\\columnbreak','')
gs=sol.index('\\section*{General tasks for every problem}')
ge=sol.index('\\noindent\\begin{minipage}{\\linewidth}',gs)
sol=sol[:gs]+'\\section*{General tasks for every problem}\n'+general+'\n'+sol[ge:]
sol=sol.replace('Then complete the five tasks below for your own scenario.','Then complete all five shared general tasks for your own scenario.')
policy=exam[exam.index('To pass, students'):exam.index('\n',exam.index('To pass, students'))]
pos=sol.index('\\section*{Evaluated criteria}')
sol=sol[:pos]+policy+'\n\n'+sol[pos:]
sol=sol.replace('Columns are Symbol, Concept, Type and Meaning in context.','Use the Symbol and Value and Meaning in context headings shown in the shared tasks.')
sol=sol.replace('The interval table uses Symbol, Concept, Calculation and Result and meaning in context, with separate endpoint rows.','The interval table uses the shared task headings, with separate endpoint rows; worked tables below separate concepts, calculations and interpretations for clarity.')
sol=sol.replace('% Governing source: '+STEM+'.tex','% Governing source: '+STEM+f'_{i}.tex')

# Write the solution FIRST, after the calculation and procedural audit passed.
assert not occupied(i)
solpath=DEST/f'{STEM}_solution_{i}.tex'
with solpath.open('x',encoding='utf-8',newline='\n') as h:h.write(sol)

# Derive the student questions directly from the verified solution statements.
student=exam
for q,title in [(1,'Retail electricity'),(2,'Savings-account')]:
    begin=sol.index('\\textbf{Original shared description}',sol.index('\\sectionScored{'+title))
    begin=sol.index('\n\n',begin)+2
    end=sol.index('Complete all five \\textbf{General tasks',begin)
    body=sol[begin:end].replace('\\keytable','\\examtable')
    if q==1:
        body=body.replace('\\textbf{Subsequent study}&\\textbf{Lower endpoint}&\\textbf{Upper endpoint}','\\textbf{Study \\#}&\\textbf{L}&\\textbf{U}')
    a=student.index('An energy-cost review' if q==1 else 'A bank reviews all',student.index('\\SubsectionBox{'+title))
    b=student.index('Complete all five \\textbf{General tasks',a)
    student=student[:a]+body+student[b:]
studentpath=DEST/f'{STEM}_{i}.tex'
with studentpath.open('x',encoding='utf-8',newline='\n') as h:h.write(student)

for q,title in [(1,'Retail electricity'),(2,'Savings-account')]:
    a=student.index('An energy-cost review' if q==1 else 'A bank reviews all',student.index('\\SubsectionBox{'+title))
    b=student.index('Complete all five \\textbf{General tasks',a)
    a2=sol.index('An energy-cost review' if q==1 else 'A bank reviews all',sol.index('\\sectionScored{'+title))
    b2=sol.index('Complete all five \\textbf{General tasks',a2)
    normalize=lambda s:re.sub(r'\s+',' ',s.replace('\\keytable','\\examtable').replace('\\textbf{Subsequent study}&\\textbf{Lower endpoint}&\\textbf{Upper endpoint}','\\textbf{Study \\#}&\\textbf{L}&\\textbf{U}')).strip()
    assert normalize(student[a:b])==normalize(sol[a2:b2])
assert all(digest(ROOT/p)==v for p,v in prior.items())
(WORK/'alternate-data.json').write_text(json.dumps(new,default=str,indent=2),encoding='utf-8')
(WORK/'index.txt').write_text(str(i))
print(json.dumps({'index':i,'solution':str(solpath),'exam':str(studentpath),'audit_steps':len(rows),'preexisting_files_unchanged':len(prior)},indent=2))
