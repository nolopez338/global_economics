from pathlib import Path
from decimal import Decimal as D
import re,json,hashlib
root=Path.cwd(); work=root/'tmp/exam-alternate-g11-1';dest=root/'book/grade11/term_2/4-learning_evidences'
stem='G11_T2_L1_C1C2_exam'; idx=(work/'index.txt').read_text()
p=dest/f'{stem}_solution_{idx}.tex';s=p.read_text(encoding='utf-8')
# Corrections found by independently checking text against recomputed data.
s=s.replace(r'105-110=-3',r'105-110=-5').replace(r'\CtwoPoint{-3}',r'\CtwoPoint{-5}')
s=s.replace('has mean fee 45 thousand COP','has mean fee 46 thousand COP')
s=s.replace('with 45 values at $m-d$ and 45 at $m+d$','with 50 values at $m-d$ and 50 at $m+d$')
s=s.replace('6.9451<45','11.9398<46')
s=s.replace(r'\CtwoError{2}$ percentage point.',r'\CtwoError{2}$ percentage points.')
p.write_text(s,encoding='utf-8')

data=json.loads((work/'alternate-data.json').read_text())
num=r'[-+]?\d+(?:\.\d+)?'
errors=[];checks=0
for q,d in enumerate(data,1):
    start=s.index('\\sectionScored{'+['Retail electricity','Savings-account','Create an integrated'][q-1])
    end=s.index('\\subsection*{Proposed partial-credit guidance',start)
    start2=s.index('\\subsection*{Problem '+str(q)+':')
    end2=s.index('\\subsection*{Problem '+str(q+1)+':',start2) if q<3 else s.index('\\end{document}')
    block=s[start:end]+s[start2:end2]
    allowed={'CtwoPoint':[d[k] for k in ['a','b','dm']], 'SSD':[d[k] for k in ['sa','sb','ds']],
        'CtwoSD':[d['sigma']],'CtwoMean':[d['mu']],'CtwoSE':[d['se']],
        'CtwoSize':[d['n']], 'Sam':[d[k] for k in ['n','ka','kb']],
        'CtwoMoE':d['moe'],'CtwoWidth':d['W'],
        'SP':[d['pa'],d['pb'],d['dp'],str(D(d['pa'])*100),str(D(d['pb'])*100)],
        'CtwoSignificance':[str((1-D(c))/t) for c in d['cs'] for t in [1,2]],
        'CtwoConfidence':d['cs']+[str(D(c)*100) for c in d['cs']],
        'CtwoCritical':d['zs'],'CtwoError':d['err'],
        'CtwoEndpoint':d['L']+d['U']+[v for pair in d.get('intervals',[]) for v in pair],
        'CtwoCI':d['L']+d['U']}
    for macro,values in allowed.items():
        vals=set(map(D,map(str,values)))
        for m in re.finditer(r'\\'+macro+r'\{([^{}]*)\}',block):
            content=m.group(1)
            if re.search(r'[A-Za-z\\]',content.replace(r'\%','')):continue
            for number in re.findall(num,content.replace(r'\%','')):
                # In a compact subtraction, '-' is the operation, not a sign.
                if D(number) not in vals and abs(D(number)) not in {abs(v) for v in vals}:
                    errors.append((q,macro,content,number,sorted(map(str,vals))))
                checks+=1
    # Flatten semantic highlights before checking compact numeric equations.
    flat=block
    while re.search(r'\\(?:Ctwo\w+|Pop|Sam|SSD|SP|PP)\{([^{}]*)\}',flat):
        flat=re.sub(r'\\(?:Ctwo\w+|Pop|Sam|SSD|SP|PP)\{([^{}]*)\}',r'\1',flat)
    flat=flat.replace(r'\%','')
    for m in re.finditer(r'(?<![\d.+\-])('+num+r')\s*([+\-])\s*('+num+r')\s*=\s*('+num+r')',flat):
        a,op,b,c=m.groups(); actual=D(a)+D(b) if op=='+' else D(a)-D(b)
        if actual!=D(c):errors.append((q,'equation',m.group(),str(actual)))
        checks+=1
    assert D(d['pa'])==D(d['ka'])/D(d['n'])
    assert D(d['pb'])==D(d['kb'])/D(d['n'])
    for z,m,l,u,w in zip(d['zs'],d['moe'],d['L'],d['U'],d['W']):
        assert D(m)==D(z)*D(d['sigma'])/D(d['n']).sqrt()
        assert D(l)==D(d['a'])-D(m) and D(u)==D(d['a'])+D(m) and D(w)==D(u)-D(l)
    if 'intervals' in d:
        assert [D(l)<=D(d['mu'])<=D(u) for l,u in d['intervals']]==d['flags']
        assert all(D(u)-D(l)==D(d['W'][0]) for l,u in d['intervals'])
    else:assert sum(d['cats'])==d['total'] and sum(d['cats'][:2])==d['counts'][1]

assert not errors,json.dumps(errors,indent=2)
e=(dest/f'{stem}_{idx}.tex').read_text(encoding='utf-8')
for title,first in [('Retail electricity','An energy-cost review'),('Savings-account','A bank reviews all')]:
    a=e.index(first,e.index('\\SubsectionBox{'+title));b=e.index('Complete all five \\textbf{General tasks',a)
    a2=s.index(first,s.index('\\sectionScored{'+title));b2=s.index('Complete all five \\textbf{General tasks',a2)
    norm=lambda t:re.sub(r'\s+',' ',t.replace('\\keytable','\\examtable').replace('\\textbf{Subsequent study}&\\textbf{Lower endpoint}&\\textbf{Upper endpoint}','\\textbf{Study \\#}&\\textbf{L}&\\textbf{U}')).strip()
    assert norm(e[a:b])==norm(s[a2:b2])
# Exact construction paragraph/checklist and five shared task definitions.
for macro in ['cOneA','cOneB','cTwoA','cTwoB','cTwoC']:
    pat=r'\\newcommand\{\\'+macro+r'\}\{[^\n]*\}'
    assert re.search(pat,e).group()==re.search(pat,s).group()
construct=lambda t:t[t.index('Invent a new economic'):t.index('\\end{enumerate}',t.index('Invent a new economic'))+len('\\end{enumerate}')]
assert construct(e)==construct(s)
for path,value in json.loads((work/'preexisting-sha256.json').read_text()).items():
    assert hashlib.sha256((root/path).read_bytes()).hexdigest()==value,path
print(f'PASS: {checks} explicit numeric/macro checks; all intervals, proportions, coverage, question agreement and existing-file hashes verified.')

