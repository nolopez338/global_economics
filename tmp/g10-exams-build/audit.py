from pathlib import Path
import re
from decimal import Decimal as D
from pypdf import PdfReader

root = Path(__file__).resolve().parents[2]
folder = root/'book2026-2027/grade10/term_1/3-learning_evidences'
pattern = r'\\sectionScored\{(.*?)\}\{(.*?)\}\{sec:q([1-5])\}(.*?)(?=\\phantomsection)'
def normalize(s):
    s = re.sub(r'\\(?:columnbreak|newpage|raggedcolumns)|\\(?:begin|end)\{multicols\}(?:\{2\})?', '', s)
    return re.sub(r'\s+', '', s)
for version in ['2','2A','2B','2C','2D','2E']:
    base = f'G10_T1_L2_C8C9C10_examV{version}'
    source = (folder/(base+'_solution.tex')).read_text(encoding='utf-8')
    output = (folder/(base+'.tex')).read_text(encoding='utf-8')
    blocks = re.findall(pattern, source, re.S)
    assert len(blocks) == 5
    for title, score, q, body in blocks:
        heading = f'\\SubsectionBox{{{q}. {title} \\score{{{score}}}}}'
        part = output.split(heading)[1].split('\\SubsectionBox{')[0]
        if q == '5':
            part = part.rsplit('\\par',1)[0]
        assert normalize(body) == normalize(part), (version,q,'content mismatch')
        if int(q) <= 2:
            assert re.findall(r'\\score\{([^}]+)\}',body) == ['1','0.5','1.5']
            tables = re.findall(r'\\begin\{tabular\}.*?\\end\{tabular\}',body,re.S)
            prob = list(map(D,re.search(r'\$P\(S_j\)\)??\$\s*&\s*(.*?)\\\\',tables[0]).group(1).split('&')))
            rows = re.findall(r'\([\$]?[AC]_\d[\$]?\)\s*&\s*(.*?)\\\\',tables[0])
            data = [list(map(D,row.split('&'))) for row in rows]
            assert len(data) == 4
            best = list(map(max, zip(*data)))
            stats = re.findall(r'\$[AC]_\d\$\s*&\s*(.*?)\\\\',tables[1])
            for i,(pay,stat) in enumerate(zip(data,stats),1):
                expected = [max(pay), min(pay), max(b-p for b,p in zip(best,pay)), sum(p*v for p,v in zip(prob,pay))]
                assert expected == list(map(D,stat.split('&'))), (version,q,i,expected,stat)
    assert len(re.findall(r'\\SubsectionBox\{[1-5]\.',output)) == 5
    assert output.count('Illustrate each filtering stage, showing survivors and eliminations.') == 3
    assert output.count('C10: Separate activity reminder (unscored)') == 1
    assert not re.search(r'\\(?:phantomsection|label|secInicio|tableofcontents|tikzset|boxed)|sol:q|Supporting filtering|Selected:',output)
    pdf = PdfReader(Path(__file__).parent/(base+'.pdf'))
    assert len(pdf.pages) == 3
    print(f'Version {version}: exact source statements, tables, scores, five questions, no solution artifacts; 3 PDF pages.')
