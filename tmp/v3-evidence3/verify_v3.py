"""Task-specific checks for the requested G11 T1 L3 V3 pair."""
from pathlib import Path
from decimal import Decimal as D, ROUND_HALF_UP
import re,json,hashlib
from pypdf import PdfReader
base=Path(__file__).resolve().parent
root=base.parents[1]
folder=root/'book2026-2027/grade11/term_1/3-learning_evidences'
ename='G11_T1_L3_C8C9C10_exam_3';sname='G11_T1_L3_C8C9C10_exam_solution_3'
e=(folder/(ename+'.tex')).read_text(encoding='utf-8');s=(folder/(sname+'.tex')).read_text(encoding='utf-8')
old_e=(folder/'G11_T1_L3_C8C9C10_exam_2.tex').read_text(encoding='utf-8')
ref=(root/'book2026-2027/fundamentals/normal-table.tex').read_text(encoding='utf-8')
for path,expected in json.loads((base/'source_hashes.json').read_text()).items():assert hashlib.sha256((root/path).read_bytes()).hexdigest()==expected,path
cols=list(map(D,['.30','.20','.10','.05','.025','.01','.005']))
t={};phi={}
for line in ref.splitlines():
    fields=line.strip().split('&')
    if re.match(r'^\d+\s+&',line.strip()) and len(fields)==8:
        t[int(fields[0])]=dict(zip(cols,[D(re.search(r'\d+\.\d+',x)[0]) for x in fields[1:]]))
    if re.match(r'^\d\.\d\s+&',line.strip()) and len(fields)==11:
        phi.update({D(fields[0].strip())+D(j)/100:D(re.search(r'\d+\.\d+',x)[0]) for j,x in enumerate(fields[1:])})
order=[2,1,3,4,5,7,6,8,9,10,13,12,11,14,15,16,17]
eb=re.split(r'\\SubsectionBox\{',e)[1:];ob=re.split(r'\\SubsectionBox\{\d+\. ',old_e)[1:]
sb=re.split(r'\\sectionScored\{',s)[1:]
assert len(eb)==len(sb)==17
expected=[(9,['-.025','.10']),(20,['.30','.10']),(12,['-.10']),(18,['-.30']),(11,['-.05','-.30']),(19,['-.10']),(14,['-.025','.025']),(22,['-.01','.10']),(25,['.025']),(16,['-.05','.05']),(16,['-.025']),(18,['-.20','.05']),(15,['-.30']),(13,['-.025','.025']),(11,['-.05']),(20,['.10'])]
def norm(x):return re.sub(r'\s+',' ',x).strip()
def masked(x):return re.sub(r'[-+]?\d+(?:\.\d+)?','#',norm(x))
def rnd(x,n=2):return f'{x.quantize(D(10)**-n,rounding=ROUND_HALF_UP):.{n}f}'
audit=[]
for q,(eblock,sblock,old) in enumerate(zip(eb,sb,order),1):
    eprompt=eblock[eblock.index('\\textbf'):].split('\\end{minipage}')[0] if q<17 else eblock[eblock.index('\\textbf{Exam:}'):].split('\\end{multicols}')[0]
    # Every final exam sentence, mark and option appears unchanged in the key.
    if q<17:
        context,task=eprompt.split('\n',1)
        assert context in sblock,(q,'context mismatch')
        assert task.strip() in sblock,(q,'task mismatch')
        oprompt=ob[old-1][ob[old-1].index('\\textbf'):].split('\\SubsectionBox')[0].strip()
        assert masked(oprompt)==masked(eprompt),(q,'wording beyond numbers changed')
        crit,points=(8,1) if q<=10 else (9,2)
        assert f'C{crit}-\\sml{{{points}}}' in eblock.split('\n')[0]
        assert f'C{crit}-\\sml{{{points}}}' in sblock.split('\n')[0]
        assert f'\\label{{sol:q{q}}}' in sblock and f'{{sec:q{q}}}' in sblock
        vals=[re.search(p,eprompt)[1] for p in [r'n=(\d+)',r'm=([-\d.]+)',r'a=([\d.]+)']]
        n,m,a=int(vals[0]),D(vals[1]),D(vals[2]);df=n-1
        for pat,val in zip([r'n=(\d+)',r'm=([-\d.]+)',r'a=([\d.]+)'],vals):assert D(re.search(pat,oprompt)[1])!=D(val)
        assert df==expected[q-1][0]
        signedalphas=list(map(D,expected[q-1][1]));cs=[(-1 if alpha<0 else 1)*t[df][abs(alpha)] for alpha in signedalphas]
        xs=[m+a*c for c in cs]
        for c in cs:assert rnd(c,3) in sblock,(q,'missing signed cutoff')
        # Recover each direct bound from the actual printed question.
        if q in [1,2,3,4,5,11,12,13]:
            task=eprompt.split('\n',1)[1]; nums=list(map(D,re.findall(r'(?<![\w])[-+]?\d+(?:\.\d+)?',task.split('\\score')[0])))
            assert nums==xs,(q,nums,xs)
            assert [(x-m)/a for x in nums]==cs
        else:
            for x in xs:assert rnd(x) in sblock,(q,'missing final contextual cutoff',x)
        tdesc='; '.join(f'alpha={alpha}: {t[df][alpha]:.3f}' for alpha in dict.fromkeys(map(abs,signedalphas)))
        ndesc='—'
        if q in [11,12,13]:
            zs=[c.quantize(D('.01'),rounding=ROUND_HALF_UP) for c in cs]
            for z in zs:assert abs(z)<=D('2.59')
            pn=1-phi[abs(zs[0])] if q==11 else (phi[zs[1]]-(1-phi[abs(zs[0])]) if q==12 else phi[abs(zs[0])])
            pt={11:D('.025'),12:D('.75'),13:D('.7')}[q];ea=abs(pt-pn)
            for value,digits in [(pt,4),(pn,4),(ea,4),(100*ea/pt,2),(100*ea/pn,2)]:assert rnd(value,digits) in sblock,(q,value)
            ndesc='; '.join(f'Phi({abs(z):.2f})={phi[abs(z)]:.4f}' for z in zs)
        if q>=14:
            target={14:D('.975'),15:D('.95'),16:D('.90')}[q]
            closest=min(phi,key=lambda z:(abs(phi[z]-target),z))
            assert closest=={14:D('1.96'),15:D('1.64'),16:D('1.28')}[q]
            zs=[-closest,closest] if q==14 else [(-1 if q==15 else 1)*closest]
            for rt,z in zip(xs,zs):
                rn=m+a*z;assert rt and rn
                ea=abs(rt-rn)
                for v in [rn,ea,100*ea/abs(rt),100*ea/abs(rn)]:assert rnd(v) in sblock,(q,v)
            ndesc={14:'Phi(1.96)=.9750',15:'Phi(1.64)=.9495; Phi(1.65)=.9505 (tie)',16:'Phi(1.28)=.8997; Phi(1.29)=.9015'}[q]
        audit.append(f'| {q} | {df} | {tdesc} | {ndesc} |')
    else:
        assert masked(eprompt)==masked(ob[16][ob[16].index('\\textbf{Exam:}'):].split('\\end{multicols}')[0])
        for line in eprompt.splitlines():
            if line.strip() and not line.startswith('\\textbf{Exam:}') and not line.startswith('\t\\item'):
                assert norm(line) in norm(sblock),(q,line)
        assert 'Select one model and describe plausible real-life data in 1--2 sentences. \\score{6}' in sblock
assert 'solutions' not in e.lower().replace('exam_solution_3.tex','').replace('exam_solution_3','')
assert all(str(x) in e for x in [10,12,6,28])
# Independently evaluate the printed standardization and back-transformation arithmetic.
for x,m,a,c in re.findall(r'\\frac\{([-\d.]+)-\(([-\d.]+)\)\}\{([\d.]+)\}=([-\d.]+)',s):assert (D(x)-D(m))/D(a)==D(c.rstrip('.'))
for m,a,c,x in re.findall(r'&=([-\d.]+)\+([\d.]+)\(([-\d.]+)\)=([-\d.]+)',s):assert D(m)+D(a)*D(c)==D(x)
for rt,rn,ea in re.findall(r'&=\|([-\d.]+)-\(([-\d.]+)\)\|=([\d.]+)',s):assert abs(D(rt)-D(rn))==D(ea)

reader=PdfReader(base/'solution-build'/(sname+'.pdf'));names=reader.named_destinations
for i in range(1,18):
    assert f'section.{i}' in names
    section_page=reader.get_destination_page_number(names[f'section.{i}'])
    assert str(i) in reader.pages[section_page].extract_text()
links=0
for page in reader.pages:
    for obj in page.get('/Annots',[]):
        annotation=obj.get_object()
        target=annotation.get('/Dest')
        if target is None and annotation.get('/A'):target=annotation['/A'].get('/D')
        if isinstance(target,str):assert target in names,target;links+=1
assert links>100,links
aux=(base/'solution-build'/(sname+'.aux')).read_text()
for q in range(1,18):
    section=re.search(r'\\newlabel\{sec:q'+str(q)+r'\}\{\{(\d+)\}.*?\{(section\.\d+)\}',aux)
    assert section and int(section[1])==q and section[2]==f'section.{q}'
    solution=re.search(r'\\newlabel\{sol:q'+str(q)+('a' if q==17 else '')+r'\}.*?\{(section\*\.\d+)\}',aux)
    assert solution and solution[1] in names
assert 10*1+6*2+6==28
for kind,name in [('exam-build',ename),('solution-build',sname)]:
    log=(base/kind/(name+'.log')).read_text(errors='replace')
    assert not re.search(r'Overfull|Underfull|undefined|LaTeX Warning|Package .* Warning',log)
report='Verified: source hashes unchanged; 17 exact matching prompts; numerical-only prompt variants; unchanged procedures and point allocations; printed table entries; contextual arithmetic, comparisons and rounding; nonzero denominators; contents and internal PDF destinations.\n'
report+=f'PDFs: exam {len(PdfReader(base/"exam-build"/(ename+".pdf")).pages)} pages; key {len(reader.pages)} pages; {links} internal link annotations checked.\n\n'
report+='| V3 | df | t row entries | Normal cumulative entries |\n|---|---|---|---|\n'+'\n'.join(audit)
(base/'validation-report.md').write_text(report,encoding='utf-8')
print(report)
