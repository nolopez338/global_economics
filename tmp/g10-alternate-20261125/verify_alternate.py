from pathlib import Path
from fractions import Fraction as F
import re, json, hashlib
root=Path(__file__).resolve().parents[2]
work=Path(__file__).resolve().parent
folder=root/'book2026-2027/grade10/term_2/4-learning_evidences'
stem='G10_T2_L1_C1C2_exam'
exam=(folder/(stem+'_1.tex')).read_text(encoding='utf-8')
sol=(folder/(stem+'_solution_1.tex')).read_text(encoding='utf-8')
original=(folder/(stem+'.tex')).read_text(encoding='utf-8')
calc=json.loads((work/'calculation-checks.json').read_text())
pmfs=[{int(x):F(p) for x,p in d.items()} for d in calc['pmfs']]
sections=re.split(r'(?=\\sectionScored\{)',sol)[1:]
questions=re.split(r'(?=\\SubsectionBox\{)',exam)[1:]
assert len(sections)==len(questions)==6
for i,(q,s) in enumerate(zip(questions,sections)):
    prompt=q.split('\\QuestionLabel{q:'+str(i+1)+'}')[1].split('\\begin{enumerate}')[0].strip()
    assert prompt in s
    tasks=re.findall(r'\\item (.*?) \\sscore\{',q,re.S)
    assert len(tasks)==3
    for task in tasks: assert task.strip() in s
assert re.findall(r'\\sscore\{[^\n]+',exam)==re.findall(r'\\sscore\{[^\n]+',original)
assert re.findall(r'\\score\{C[12]-\\sml\{\d+\}\}',exam)==re.findall(r'\\score\{C[12]-\\sml\{\d+\}\}',original)
assert re.findall(r'\\score\{(\d+(?:\.\d+)?)\}',sol)==['1','1','1','1','1','1','0.5','1','0.5','0.5','1','0.5','1','2','1','1.5','3','1.5']

for i,s in enumerate(sections):
    # Grouped tables for the two complete-outcome questions.
    if i<2:
        group=s.split('Grouped probability')[1].split('\\bottomrule')[0]
        actual={}
        for line in group.splitlines():
            x=re.search(r'\$(-?)\\GTenHLValue\{(\d+)\}\$',line)
            ps=re.findall(r'\\GTenHLProbability\{(\d+/\d+)\}',line)
            if x:
                actual[int(x[1]+x[2])]=F(ps[-1])
                if len(ps)>2: assert sum(map(F,ps[:-1]))==F(ps[-1])
        assert actual==pmfs[i],(i,actual)
    if i==0:
        rows=s.split('Ordered outcome & Product')[1].split('\\bottomrule')[0]
        for line in rows.splitlines():
            w=re.search(r'\\mathrm\{([KC]+)\}',line)
            if not w: continue
            product=F(1)
            for p in re.findall(r'\\GTenHLProbability\{(0\.\d+)\}',line.split('&')[1]): product*=F(p)
            exact=F(re.findall(r'\\GTenHLProbability\{(\d+/\d+)\}',line)[0])
            expected=F(2,5)**w[1].count('K')*F(3,5)**w[1].count('C')
            assert product==exact==expected
    if i==1:
        rows=s.split('Ordered credit outcome')[1].split('\\bottomrule')[0]
        for line in rows.splitlines():
            pair=re.findall(r'\\GTenHLOutcome\{(\d+)\}',line)
            if not pair: continue
            a,b=map(int,pair)
            exact=F(re.findall(r'\\GTenHLProbability\{(\d+/\d+)\}',line)[0])
            assert exact==dict(zip([0,4,9],[F(1,5),F(1,2),F(3,10)]))[a]*dict(zip([0,4,9],[F(2,5),F(2,5),F(1,5)]))[b]
    if i<2: continue
    xs=list(pmfs[i]); cumulative=[]; acc=F(0)
    for x,p in pmfs[i].items(): acc+=p; cumulative.append(acc)
    table=s.split('Cutoff interval')[1].split('\\bottomrule')[0]
    intervals=[]; heights=[]
    for line in table.splitlines():
        if '&' not in line: continue
        vals=list(map(int,re.findall(r'\\GTenHLValue\{(\d+)\}',line)))
        prob=re.findall(r'\\HLCumulativeProbability\{(\d+(?:/\d+)?)\}',line)
        if not prob: continue
        intervals.append(vals); heights.append(F(prob[-1]))
    assert intervals==[[xs[0]]]+[xs[j:j+2] for j in range(len(xs)-1)]+[[xs[-1]]]
    assert heights==[F(0)]+cumulative
    graphs=re.findall(r'\\begin\{tikzpicture\}(.*?)\\end\{tikzpicture\}',s,re.S)
    assert len(graphs)==2
    bars=re.findall(r'axis cs:([\d.-]+),0\) rectangle \(axis cs:([\d.-]+),([\d/]+)\)',graphs[0])
    assert {int((F(a)+F(b))/2):F(p) for a,b,p in bars}==pmfs[i]
    segments=[]; openpoints=[]; filledpoints=[]
    for line in graphs[1].splitlines():
        if '\\addplot' not in line: continue
        coords=[(F(x),F(y)) for x,y in re.findall(r'\((-?\d+),(\d+(?:/\d+)?)\)',line)]
        if 'only marks' in line:
            if 'fill=white' in line: openpoints=coords
            else: filledpoints=coords
        else: segments.append(coords)
    assert filledpoints==list(zip(map(F,xs),cumulative))
    assert openpoints==list(zip(map(F,xs),[F(0)]+cumulative[:-1]))
    assert segments[1:-1]==[[(F(xs[j]),cumulative[j]),(F(xs[j+1]),cumulative[j])] for j in range(len(xs)-1)]
    assert segments[0][-1]==(F(xs[0]),0) and segments[-1][0]==(F(xs[-1]),1)

rows=sections[5].split('Subset count & Probability')[1].split('\\bottomrule')[0]
for line,expected in zip([l for l in rows.splitlines() if 'GTenHLOutcome' in l],calc['q6_compositions']):
    composition=list(map(int,re.findall(r'\\GTenHLOutcome\{(\d+)\}',line)))
    monetary=list(map(int,re.findall(r'\\GTenHL(?:Value|Second)\{(\d+)\}',line)))
    probability=F(re.search(r'\\GTenHLProbability\{(\d+/\d+)\}',line)[1])
    assert composition==expected[:3] and monetary==expected[4:] and probability==F(expected[3],84)

before=json.loads((work/'before.json').read_text())
changed=[p for p,h in before.items() if hashlib.sha256((root/p).read_bytes()).hexdigest()!=h]
expected_concurrent={str((folder/(stem+ext)).relative_to(root)) for ext in ['.tex','.pdf','.aux','.log','.synctex.gz']}
assert set(changed).issubset(expected_concurrent),changed
if changed:
    import subprocess
    baseline=subprocess.check_output(['git','show','HEAD:book2026-2027/grade10/term_2/4-learning_evidences/'+stem+'.tex']).decode('utf-8')
    # The external change is confined to the instructions paragraph.
    strip_policy=lambda t:re.sub(r'(?<=\\SubsectionBox\*\{Criteria assessment\})\s*.*?(?=\\noindent)', '',t, count=1, flags=re.S).replace('\r\n','\n')
    assert strip_policy(baseline)==strip_policy(original)
    assert 'minimum of 4 points in each criterion' in original
    (work/'concurrent-changes.json').write_text(json.dumps({'external_changes_preserved':changed,'remaining_preexisting_artifacts_unchanged':len(before)-len(changed)},indent=2),encoding='utf-8')
print(f'PASS: exact prompts and marks; all outcome products, grouped PMFs, CDF intervals, graph coordinates and nine bonus/cap compositions. {len(before)-len(changed)} pre-existing artifacts unchanged; {len(changed)} concurrent original-exam edits preserved.')
