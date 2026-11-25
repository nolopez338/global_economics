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
            expected=F(3,10)**w[1].count('K')*F(7,10)**w[1].count('C')
            assert product==exact==expected
    if i==1:
        rows=s.split('Ordered credit outcome')[1].split('\\bottomrule')[0]
        for line in rows.splitlines():
            pair=re.findall(r'\\GTenHLOutcome\{(\d+)\}',line)
            if not pair: continue
            a,b=map(int,pair)
            exact=F(re.findall(r'\\GTenHLProbability\{(\d+/\d+)\}',line)[0])
            assert exact==dict(zip([0,4,9],[F(3,10),F(4,10),F(3,10)]))[a]*dict(zip([0,4,9],[F(5,10),F(2,10),F(3,10)]))[b]
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


# Check every grouped mass, all scored tasks and detailed rubric rows.
old=(work/(stem+'_solution_1.tex.before')).read_text(encoding='utf-8')
assert re.findall(r'\\CreditDescription\{[^\n]*',sol)==re.findall(r'\\CreditDescription\{[^\n]*',old)
for i,s in enumerate(sections[2:],2):
    tab=s.split('p_X(x)')[1].split('\\bottomrule')[0]
    entries={int(x):F(p) for x,p in re.findall(r'\\GTenHLValue\{(\d+)\}.*?&.*?\\GTenHLProbability\{(\d+/\d+)\}',tab)}
    assert entries==pmfs[i],(i,entries)
# Match prompt-level probabilities to the independently verified distributions.
assert 'probability 0.3, or cancels it with probability 0.7' in questions[0]
assert '0.3, 0.4 and 0.3' in questions[1] and '0.5, 0.2 and 0.3' in questions[1]
for i,nums in [(2,[3,2,2,3,4,1,3,2]),(3,[3,1,3,2,2,4,2,3])]:
    text=questions[i].split('Their probabilities are ')[-1] if i==3 else questions[i].split('Their probabilities are ')[1]
    ps=list(map(F,re.findall(r'0\.\d+',text.split('respectively')[0])))
    assert ps==[F(n,20) for n in nums]
assert 'three times as likely' in questions[4]
assert 'three worth 0 USD each, four worth 6 USD each and two worth 14 USD each' in questions[5]
# Verify all unchanged reference/dependency hashes.
protected=json.loads((work/'protected.json').read_text())
assert all(hashlib.sha256(Path(p).read_bytes()).hexdigest()==h for p,h in protected.items())
assert all(F(a)!=F(b) for a,b in zip(calc['finals'],calc['reference_finals']))
print('PASS: exact pair prompts, all 18 subparts and marks, unchanged detailed rubrics, outcome products, grouped PMFs, complete CDF intervals, all graph bars/segments/endpoints, nine bonus/cap compositions; ten distinct final answers; reference pair and shared dependencies unchanged.')

blocks=sol.split('\\textbf{Proposed partial credit.}')[1:]
assert len(blocks)==18
for block in blocks:
    rows=block.split('\\bottomrule')[0]
    scores=re.findall(r'\\CreditDescription\{[^\n]* & (?:\\textbf\{)?(\d+(?:\.\d+)?)(?:\})?\\\\',rows)
    assert sum(map(F,scores[:-1]))==F(scores[-1]),scores
print('PASS: every proposed partial-credit table sums to its unchanged task allocation; C1=6, C2=14, overall=20.')
