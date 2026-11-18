from pathlib import Path
import re

root=Path('book2026-2027/grade11/term_2/1-practice_activities')
p=root/'G11_T2_L1_C2_practice.tex'
original=p.read_text(encoding='utf-8')
def hl(role,text): return '\\Ctwo'+role+'{'+text+'}'
def prose(s):
    # Mark complete mathematical atoms before adding prose markers.
    s=re.sub(r'\\mu_\{\\rm sim\}|\\bar\{x\}|\\sigma|\\mu|z\^\*|(?<![A-Za-z])n(?==)',lambda m:hl({'\\mu_{\\rm sim}':'Mean','\\bar{x}':'Point','\\sigma':'SD','\\mu':'Mean','z^*':'Critical','n':'Size'}[m[0]],m[0]),s)
    s=re.sub(r'(\\Ctwo(Size|Point|SD|Mean|Critical)\{(?:[^{}]|\{[^{}]*\})*\}=)(\d+(?:\.\d+)?)',lambda m:m[1]+hl(m[2],m[3]),s)
    s=re.sub(r'\d+\\%',lambda m:hl('Confidence',m[0]),s)
    terms={'original population mean':'Mean','known fixed mean':'Mean','population standard deviation':'SD','population SD':'SD','sample means':'Point','sample mean':'Point','confidence intervals':'CI','confidence interval':'CI','confidence':'Confidence'}
    s=re.sub('|'.join(map(re.escape,terms)),lambda m:hl(terms[m[0]],m[0]),s)
    return s

blocks=list(re.finditer(r'\\label\{prob:(c2-[^}]+)\}\n\n(.*?)(?=\\QuestionsTasks)',original,re.S))
assert len(blocks)==8
changes=[]
for b in blocks:
    key=b[1]; opening,study=b[2].split('\\textbf{Separate completed repeated-sampling study.}',1)
    opening=opening.strip()
    # Original clearpage belongs to the problem/task layout, not the supplied study.
    study=re.sub(r'\s*\\clearpage\s*$','',study).strip()
    # Endpoint evidence is complete in the table; avoid duplicating its forest plot.
    if '\\begin{tikzpicture}' in study:
        table=re.search(r'\\begin\{tabular\}.*?\\end\{tabular\}',study,re.S)[0]
        caption=re.search(r'\\small (Simulated endpoints .*?)\\end\{center\}',study)[1]
        study=study[:study.index('\\par\\medskip')].strip()+'\n\\begin{center}'+table+'\\par\\small '+caption+'\\end{center}'
    opening_h=prose(opening)
    opening_h=re.sub(r'(A random sample of )(\d+)',lambda m:m[1]+hl('Size',m[2]),opening_h)
    study_h=prose(study)
    study_h=re.sub(r'^(\d+)( fresh independent samples of )(\d+)',lambda m:hl('Coverage',m[1])+m[2]+hl('Size',m[3]),study_h)
    study_h=re.sub(r'(\\CtwoSD\{population SD\} )(\d+)',lambda m:m[1]+hl('SD',m[2]),study_h)
    study_h=re.sub(r'(known mean |missed it )(\d+)( times)',lambda m:m[1]+hl('Coverage',m[2])+m[3],study_h)
    study_h=re.sub(r'(denominator of )(\d+)',lambda m:m[1]+hl('Coverage',m[2]),study_h)
    study_h=study_h.replace('intervals missed',hl('CI','intervals')+' '+hl('Coverage','missed')).replace('known mean',hl('Mean','known mean'))
    study_h=study_h.replace("sample's own mean",hl('Point',"sample's own mean"))
    study_h=study_h.replace('Covering intervals',hl('Coverage','Covering intervals'))
    study_h=study_h.replace('Intervals containing',hl('CI','Intervals')+' containing')
    study_h=study_h.replace(' & Samples', ' & '+hl('Coverage','Samples'))
    study_h=study_h.replace('$L$', '$'+hl('Endpoint','L')+'$').replace('$U$', '$'+hl('Endpoint','U')+'$')
    study_h=study_h.replace('Simulated endpoints', 'Simulated '+hl('Endpoint','endpoints'))
    # Table numeric evidence: first column identifies samples/categories; the
    # remaining columns contain supplied endpoints or covering/sample counts.
    lines=[]
    endpoints='@{}rrr@{}' in study_h
    for line in study_h.splitlines():
        if re.match(r'(?:\d|All three|Only |None)',line) and ' & ' in line:
            cells=line.split(' & ')
            for i in range(1,len(cells)):
                cells[i]=re.sub(r'^\d+(?:\.\d+)?',lambda m:hl('Endpoint' if endpoints else 'Coverage',m[0]),cells[i])
            line=' & '.join(cells)
        lines.append(line)
    study_h='\n'.join(lines)
    # Supply the procedures explicitly, preserving the original instruction.
    settings=opening_h.split('\n\n')[-1]
    task1='% Supplied original problem; only semantic highlight markup added.\n'+opening_h+'\n\n'
    task3='% Supplied separate study; calculations begin after this restatement.\n\\textbf{Separate completed repeated-sampling study.} '+study_h+'\n\n'+settings+'\n\n\\textbf{Calculations and interpretation.}\n'
    for suffix,body in [('a',task1),('c',task3)]:
        marker='\\label{sol:'+key+'-'+suffix+'}\n'
        assert original.count(marker)==1
        changes.append((marker,body))
    # Exact preservation of source restatements after removing new wrappers.
    def strip(s):
        pat=r'\\Ctwo\w+\{((?:[^{}]|\{[^{}]*\})*)\}'
        while re.search(pat,s): s=re.sub(pat,r'\1',s)
        return s
    assert strip(opening_h)==opening,key
    assert strip(study_h)==study,key
result=original
for marker,body in changes: result=result.replace(marker,marker+body)
# Removing the insertions must reproduce the entire pre-edit source exactly.
check=result
for marker,body in changes: check=check.replace(marker+body,marker)
assert check==original
p.write_text(result,encoding='utf-8',newline='\n')
print('Added 16 restatements; exact wording and pre-existing content verified.')
