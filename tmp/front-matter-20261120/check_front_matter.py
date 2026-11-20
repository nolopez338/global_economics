# Task-specific preservation and navigation audit for these four activities.
from pathlib import Path
from pypdf import PdfReader
from collections import Counter
import re, difflib, json
root=Path.cwd(); work=root/'tmp/front-matter-20261120'
source_dir=root/'book2026-2027/grade11/term_2/1-practice_activities'
results=[]
for c in range(4,8):
    stem=f'G11_T2_L{1 if c==4 else 2}_C{c}_practice'
    before=(work/(stem+'.tex')).read_bytes().decode('utf-8')
    after=(source_dir/(stem+'.tex')).read_bytes().decode('utf-8')
    assert before.split(r'\begin{document}')[0]==after.split(r'\begin{document}')[0]
    assert before.split(r'\section{Introduction}',1)[1]==after.split(r'\section{Introduction}',1)[1]
    before_criterion=re.search(r'\\item(?:\[[^\n]*?\])? (.+)', before.split(r'\section*{Evaluated criteria}')[1]).group(1)
    after_criterion=re.search(r'\\item\[\\textbf\{C'+str(c)+r'\}\] (.+)', after.split(r'\section*{Evaluated criteria}')[1]).group(1)
    assert before_criterion==after_criterion
    assert before.split(r'\textbf{How to practise.}',1)[1]==after.split(r'\textbf{How to practise.}',1)[1]
    assert r'\setcounter{secnumdepth}{2}' in after
    assert r'\phantomsection\label{toc}\tableofcontents' in re.sub(r'\s+', '',after)
    assert re.search(r'\\clearpage\s*\\section\{Introduction\}\\label\{sec:introduction\}\s*\\subsection\*\{Highlight legend\}',after)
    assert not re.search(r'\\(?:addcontentsline|addtocontents|pdfbookmark|bookmark)\b',after)
    pdf=PdfReader(work/f'C{c}'/(stem+'.pdf')); destinations=pdf.named_destinations
    assert [x['/Title'] for x in pdf.outline]==['Introduction','Notation Reference and Practice Procedure','General Worked Problems','Advanced Problems']
    first=pdf.pages[0].extract_text()
    assert first.count('Evaluated criteria')==1
    assert re.search(r'\nEvaluated criteria\n',first)
    assert 'Evaluated criteria' not in (work/f'C{c}'/(stem+'.toc')).read_text()
    tocblock=first.split('Contents',1)[1].split('Evaluated criteria',1)[0]
    assert all(x in tocblock for x in ['Introduction','Notation Reference and Practice Procedure','General Worked Problems','Advanced Problems'])
    links=Counter()
    for i,page in enumerate(pdf.pages):
        for ref in page.get('/Annots',[]):
            annotation=ref.get_object(); action=annotation.get('/A',{})
            if action.get('/S')=='/GoTo':
                target=action['/D']; assert target in destinations,(c,i,target)
                dest=destinations[target]; page_number=pdf.get_destination_page_number(dest)
                assert 0<=page_number<len(pdf.pages)
                assert 0<=float(dest.top)<=float(pdf.pages[page_number].mediabox.height)
                links[target]+=1
    aux=(work/f'C{c}'/(stem+'.aux')).read_text()
    labels=re.findall(r'\\newlabel\{([^}]+)\}\{\{[^}]*\}\{(\d+)\}\{.*\}\{([^{}]+)\}\{\}\}',aux)
    assert labels
    for label,page,target in labels:
        assert target in destinations,(label,target)
        assert pdf.get_destination_page_number(destinations[target])+1==int(page)
        if label.startswith(('prob:','sol:','ex:')) or label in ('toc','sec:introduction','tab:highlight-legend','tab:notation-reference'):
            # Not every legend has an explicit incoming link in the original activity.
            if label.startswith(('prob:','ex:')) or label in ('toc','sec:introduction'):
                assert links[target]>0,(c,label,target)
    for target_label in re.findall(r'\{\d+\}/\{([^}]+)\}',after):
        target=next(target for label,page,target in labels if label==target_label)
        assert links[target]>0,(c,target_label)
    toc_target=next(target for label,page,target in labels if label=='toc')
    assert pdf.get_destination_page_number(destinations[toc_target])==0
    assert pdf.get_destination_page_number(destinations['section.1'])==1
    result={'criterion':f'C{c}','pages':len(pdf.pages),'internal_links':sum(links.values()),'labels_checked':len(labels),'source_preserved':True,'contents_and_outline_pass':True}
    results.append(result)
    (work/f'C{c}-changes.diff').write_text(''.join(difflib.unified_diff(before.splitlines(True),after.splitlines(True),fromfile='before',tofile='after')),encoding='utf-8')
    print(json.dumps(result))
scaffold=(root/'.agents/skills/global-economics-home-practice/assets/template_home_practice.tex').read_text()
assert not re.search(r'\\(?:addcontentsline|addtocontents|pdfbookmark|bookmark)\b',scaffold)
(work/'verification.json').write_text(json.dumps(results,indent=2))
print('PASS: exact criterion wording, instructions, preambles, and entire instructional bodies preserved; contents, outline, labels, all internal links and return destinations verified.')
