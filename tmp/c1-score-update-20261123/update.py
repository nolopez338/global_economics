from pathlib import Path
import re
root=Path.cwd()
folder=root/'book2026-2027/grade10/term_2/4-learning_evidences'
work=root/'tmp/c1-score-update-20261123'
for suffix in ('exam','exam_solution'):
    path=folder/f'G10_T2_L1_C1C2_{suffix}.tex'
    source=path.read_text(encoding='utf-8')
    (work/path.name).write_text(source,encoding='utf-8')
    text=source.replace(r'\ref*{q:1} & 4',r'\ref*{q:1} & 3').replace(r'\ref*{q:2} & 4',r'\ref*{q:2} & 3')
    text=text.replace(r'\textbf{Total} & \textbf{8}',r'\textbf{Total} & \textbf{6}').replace(r'C1-\sml{4}',r'C1-\sml{3}')
    if suffix=='exam':
        text=text.replace('C1 = 4+4 = 8; C2 = 2+2+4+6 = 14; overall = 22.','C1 = 3+3 = 6; C2 = 2+2+4+6 = 14; overall = 20.')
        text=text.replace(r'A \textbf{minimum of 4 points per criterion} is required to pass.',r'A \textbf{minimum of 4 out of 6 points for C1 and 4 out of 14 points for C2} is required to pass. The overall available total is 20 points.')
        before,after=text.split(r'\SubsectionBox{Local parcel delivery fees',1)
        assert before.count(r'\sscore{\sml{2}}')==2
        before=before.replace(r'\sscore{\sml{2}}',r'\sscore{\sml{1}}')
        text=before+r'\SubsectionBox{Local parcel delivery fees'+after
    else:
        text=text.replace('4 out of 8 points','4 out of 6 points').replace('overall available total is 22 points','overall available total is 20 points')
        text=re.sub(r'\\ref\*\{q:(\d)\}',r'\\ref*{sec:q\1}',text)
        before,after=text.split(r'\sectionScored{Local parcel delivery fees',1)
        assert before.count(r'\score{2}')==4
        before=before.replace(r'\score{2}',r'\score{1}')
        for line in before.splitlines():
            if 'Proposed partial credit.' in line and 'Total: 2 points.' in line:
                new=line.replace('0.25','0.125').replace('0.5','0.25').replace('0.75','0.375').replace('Total: 2 points.','Total: 1 point.')
                before=before.replace(line,new)
        before=before.replace('Question total: 4 points for C1.','Question total: 3 points for C1.').replace('Criterion C1 total: 8 points','Criterion C1 total: 6 points')
        text=before+r'\sectionScored{Local parcel delivery fees'+after
        text=text.replace('C1 gives $4+4=8$ points','C1 gives $3+3=6$ points').replace('$8+14=22$ points','$6+14=20$ points')
    path.write_text(text,encoding='utf-8',newline='\n')
    import difflib
    print(''.join(difflib.unified_diff(source.splitlines(True),text.splitlines(True),fromfile=suffix+' before',tofile=suffix+' after')))
