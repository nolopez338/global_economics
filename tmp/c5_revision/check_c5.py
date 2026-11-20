import math, re
from pathlib import Path
from statistics import NormalDist
from collections import Counter
from pypdf import PdfReader
root=Path('tmp/c5_revision')
src=Path('book2026-2027/grade11/term_2/1-practice_activities/G11_T2_L2_C5_practice.tex').read_text(encoding='utf-8')
old=(root/'original.tex').read_text(encoding='utf-8')
criterion='Constructs confidence intervals for a population proportion using sample proportions, applying them to contexts such as poverty rates, defaulting borrowers, or successful investments.'
assert criterion in src and criterion in old
assert re.findall(r'\\section\{([^}]+)\}',src)==['Introduction','Notation Reference and Practice Procedure','General Worked Problems','Advanced Problems']
assert src.count('GTenHighlightsfalse')==1 and '% \\GTenHighlightsfalse' in src
assert src.count('\\PracticeHighlightLegend{')==1
labels=re.findall(r'\\label\{([^}]+)\}',src)
assert len(labels)==len(set(labels))
assert src.index('\\PracticeHighlightLegend{') < src.index('\\subsection{Introductory example 1') < src.index('\\subsection{Introductory example 2') < src.index('\\subsection{Notation reference}') < src.index('\\subsection{Reusable practice procedure}')
N=NormalDist()
for name,p,n,z,pop,x,expected_se,expected_e in [
('intro1',.15,200,1.96,4000,30,None,None),
('intro2',.2,400,1.96,10000,80,.0200,.0392),
('loans',.125,400,2.326,8000,50,.01653595,.03846261),
('shipments',.3,600,1.96,12000,180,.01870829,.03666824),
('retailers',.2,500,1.645,10000,100,.01788854,.02942665),
('report A',.25,300,1.96,30000,75,.025,.049),
('report B',.25,1200,2.326,30000,300,.0125,.029075)]:
    se=math.sqrt(p*(1-p)/n); e=z*se; lo=p-e; hi=p+e
    assert x==n*p and min(x,n-x)>=10 and n/pop<=.1 and 0<=lo<hi<=1
    assert math.isclose((lo+hi)/2,p) and math.isclose((hi-lo)/2,e)
    assert math.isclose((z/e)**2*p*(1-p),n)
    assert math.isclose(e/se,z)
    if expected_se is not None: assert abs(se-expected_se)<5.1e-9
    if expected_e is not None: assert abs(e-expected_e)<5.1e-9
    print(name, 'count',x,'n',n,'SE',round(se,10),'interval',round(lo,10),round(hi,10))
assert math.isclose(49*math.sqrt(14)/5000,1.96*math.sqrt(.3*.7/600))
assert math.isclose(329*math.sqrt(5)/25000,1.645*math.sqrt(.2*.8/500))
assert round(100*(2*N.cdf(1.645)-1),3)==90.003
assert round((1.96/.03667)**2*.3*.7,4)==599.9425
assert round((1.96/.03667)**2*.3*.7*.3,4)==179.9827
assert round(1.96*math.sqrt(.125*.875/400),8)==.03241045
assert round(2*1.645*math.sqrt(.5*.5/500),8)==.07356664
assert round((2.326/1.96)*math.sqrt(300/1200),5)==.59337
assert round(100*(1-(2.326/1.96)*.5),2)==40.66
pdf=PdfReader(root/'G11_T2_L2_C5_practice.pdf'); off=PdfReader(root/'highlights_off.pdf')
assert len(pdf.pages)==len(off.pages)==9
aux=(root/'G11_T2_L2_C5_practice.aux').read_text(encoding='utf-8')
links=[]
for page in pdf.pages:
    for ann in page.get('/Annots',[]):
        a=ann.get_object(); action=a.get('/A',{})
        if action.get('/S')=='/GoTo':
            dest=str(action['/D']); assert dest in pdf.named_destinations, dest
            target=pdf.named_destinations[dest]
            assert 0<=pdf.get_destination_page_number(target)<9
            links.append(dest)
expected={'toc':1,'sec:introduction':2,'tab:highlight-legend':2,'ex:intro-one':2,'ex:intro-two':2,'sec:notation-and-procedure':3,'tab:notation-reference':3,'sec:worked-solution-examples':5,'prob:c5-1':5,'sol:c5-1-a':5,'sol:c5-1-b':5,'prob:c5-2':6,'sol:c5-2-a':6,'sol:c5-2-b':6,'prob:c5-3':7,'sol:c5-3-a':7,'sol:c5-3-b':7,'sec:advanced':8,'prob:c5-advanced':8,'sol:c5-advanced-a':8,'sol:c5-advanced-b':9}
for label,page in expected.items():
    pattern=r'\\newlabel\{'+re.escape(label)+r'\}\{\{[^}]*\}\{(\d+)\}\{[^}]*\}\{([^}]+)\}'
    m=re.search(pattern,aux); assert m, label
    dest=pdf.named_destinations[m[2]]
    assert int(m[1])==page==pdf.get_destination_page_number(dest)+1,(label,page)
    if label!='tab:notation-reference': assert m[2] in links, (label,'no inbound link')
# Content retention across the two toggle states: compare visible characters,
# ignoring whitespace, discretionary word-wrap hyphens and page-break order.
a=Counter(c for p in pdf.pages for c in p.extract_text() if not c.isspace() and c!='-')
b=Counter(c for p in off.pages for c in p.extract_text() if not c.isspace() and c!='-')
assert a-b==Counter({'s':3,'!':1}) and b-a==Counter({'r':3,'\x12':1,'\x13':1}), (a-b,b-a)
# The only extraction differences are three stretched radical glyphs and one
# stretched pair of parentheses; these formulas were also inspected visually.
print('PASS: C5 wording, four-stage structure, unique labels, legend order, calculations, conditions,',len(links),'PDF links, all 21 expected label destinations, and highlight-off text retention.')

