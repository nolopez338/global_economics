"""Navigation and text checks for the final C4 practice, with its specific labels."""
from pathlib import Path
import re,json
from pypdf import PdfReader
base=Path('tmp/c4-purpose-20261124')
reader=PdfReader(base/'G11_T2_L1_C4_practice.pdf')
aux=(base/'G11_T2_L1_C4_practice.aux').read_text(encoding='utf-8')
source=Path('book2026-2027/grade11/term_2/1-practice_activities/G11_T2_L1_C4_practice.tex').read_text(encoding='utf-8')
dests=reader.named_destinations
pages=[p.extract_text() for p in reader.pages]
expected=['toc','sec:introduction','tab:highlight-legend','ex:intro-one','ex:intro-two','sec:notation-and-procedure','tab:notation-reference','sec:general-worked','sec:advanced','prob:c4-advanced-1','prob:c4-advanced-2','sol:c4-advanced-1','sol:c4-advanced-2']
expected += [f'prob:c4-{i}' for i in (1,2,3)]
expected += [f'sol:c4-{i}-{letter}' for i in (1,2,3) for letter in 'abc']
report={}
for label in expected:
    line=next(x for x in aux.splitlines() if x.startswith('\\newlabel{'+label+'}'))
    # Hyperref's aux fields: number, physical page, title, destination, extra.
    match=re.search(r'\}\{(\d+)\}\{.*\}\{([^{}]+)\}\{\}\}',line)
    assert match,line
    page,dest=match.groups(); assert dest in dests,(label,dest)
    actual=reader.get_destination_page_number(dests[dest])+1
    assert actual==int(page),(label,page,actual)
    report[label]=dict(page=actual,destination=dest)
links=0
for page in reader.pages:
    for ref in page.get('/Annots',[]):
        annotation=ref.get_object()
        action=annotation.get('/A',{})
        target=annotation.get('/Dest')
        if action.get('/S')=='/GoTo':target=action['/D']
        if target is not None:
            if isinstance(target,str): assert target in dests,target
            links+=1
assert links>40
outline=str(reader.outline)
assert 'Evaluated criteria' not in outline
assert 'Evaluated criteria' in pages[0]
assert 'Advanced Problems' in outline
assert sum(re.sub(r'\s+', ' ', x).count('Practical conclusion.') for x in pages)==9
# Each solution's destination starts on the page containing its heading.
for i in (1,2,3):
    for letter,stage in zip('abc',(1,2,3)):
        page=report[f'sol:c4-{i}-{letter}']['page']
        text=pages[page-1]
        assert f'Stage {stage}:' in text,(i,letter,page)
for lo,hi in [('390.4','429.6'),('404.392','445.608'),('416.84','443.16'),('405.2','424.8'),('68.848','79.152'),('75.5325','80.4675'),('69.06','74.94'),('76.136','83.864'),('115.065','124.935'),('121.1','130.9'),('117.065','126.935'),('124.848','135.152')]:
    assert lo in ''.join(pages) and hi in ''.join(pages)
(base/'navigation-audit.json').write_text(json.dumps(dict(pages=len(pages),links=links,labels=report),indent=2))
print(f'PASS: {len(pages)} PDF pages, {links} internal link annotations, {len(expected)} expected destinations, nine practical conclusions, correct criterion/front-matter outline scope.')
