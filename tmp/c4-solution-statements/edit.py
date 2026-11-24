from pathlib import Path
import re
root=Path.cwd()
p=root/'book2026-2027/grade11/term_2/1-practice_activities/G11_T2_L1_C4_practice.tex'
s=p.read_text(encoding='utf-8')
original=s

def argument(text, start):
    depth=1
    for i in range(start,len(text)):
        if text[i]=='{': depth+=1
        elif text[i]=='}':
            depth-=1
            if not depth: return text[start:i]
    raise ValueError('Unclosed argument')

def highlight(text):
    spans=[]
    def mark(pattern,role,group=0):
        for m in re.finditer(pattern,text):
            a,b=m.span(group)
            if not any(a<y and b>x for x,y,_ in spans):spans.append((a,b,role))
    # Values only in clauses that establish their statistical role.
    for pat,role in [
        (r'between ([\d.]+) and ([\d.]+)','HLIntervalBounds'),
        (r'budgets cover (\d+) and (\d+)','HLObservationCount'),
        (r'sets of records cover (\d+) and (\d+)','HLObservationCount')]:
        mark(pat,role,1);mark(pat,role,2)
    for pat,role in [
        (r'(?:confidence level of )(\d+ percent)','HLConfidence'),
        (r'(?:records at |either set is )(\d+ thousand Colombian pesos|\d+ US dollars)','HLSampleMean'),
        (r'(?:earnings at |charges at |earnings is |charges is |charges of )(\d+ thousand Colombian pesos|\d+ US dollars)','HLPopulationSD'),
        (r'(?:It covers |and covers )(\d+ (?:couriers|pallets|shipments))','HLObservationCount'),
        (r'(?:average by |multiplier of )(\d+\.\d+)','HLCriticalValue'),
        (r'Use multipliers of ([\d.]+) and','HLCriticalValue'),
        (r'Use multipliers of [\d.]+ and ([\d.]+)','HLCriticalValue')]:mark(pat,role,1)
    for pat,role in [
        (r'population average(?: reference-week earnings| charge)?','HLPopulationMean'),
        (r'population averages','HLPopulationMean'),
        (r'confidence level','HLConfidence'),
        (r'confidence levels','HLConfidence'),
        (r'known spread of individual (?:earnings|charges)','HLPopulationSD'),
        (r'population spread(?: already known from population records)?','HLPopulationSD'),
        (r'spread used by (?:its|each report\'s) analyst','HLPopulationSD'),
        (r'greater spread of individual (?:earnings|charges)','HLPopulationSD'),
        (r'spread of individual (?:earnings|charges)','HLPopulationSD'),
        (r'average observed in (?:the|its) records','HLSampleMean'),
        (r'average observed in either set','HLSampleMean'),
        (r'averages observed in the records','HLSampleMean'),
        (r'higher observed average','HLSampleMean'),
        (r'equal observed averages','HLSampleMean'),
        (r'exact observed average','HLSampleMean'),
        (r'number of (?:couriers|pallets|shipments) observed','HLObservationCount'),
        (r'number of pallets observed','HLObservationCount'),
        (r'original number of couriers','HLObservationCount'),
        (r'uncertainty in the average','HLStandardError'),
        (r'distance from the average to either (?:reported )?limit','HLMarginOfError'),
        (r'distance to a limit','HLMarginOfError'),
        (r'(?:reported|published|displayed) limits','HLIntervalBounds'),
        (r'Both limits','HLIntervalBounds'),
        (r'both limits','HLIntervalBounds'),
        (r'multipliers','HLCriticalValue'),
        (r'multiplier','HLCriticalValue')]: mark(pat,role)
    for a,b,role in sorted(spans,reverse=True):text=text[:a]+'\\'+role+'{'+text[a:b]+'}'+text[b:]
    return text

blocks={}
for m in re.finditer(r'\{4\}/\{(sol:c4-[^}]+)\}/\{',original):
    label=m.group(1);task=argument(original,m.end())
    prob=label.replace('sol:','prob:')
    if 'advanced' not in label:prob=prob[:-2]
    ctx=re.search(r'\\subsection\{[^\n]+\\label\{'+re.escape(prob)+r'\}\n([^\n]+)',original).group(1)
    # The subsection context supplies the population and separate-report condition.
    plain=ctx+'\n\n'+task
    marked=highlight(plain)
    stripped=re.sub(r'\\HL\w+\{([^{}]*)\}',r'\1',marked)
    assert stripped==plain,label
    blocks[label]=(plain,marked)
assert len(blocks)==11
for label,(plain,marked) in blocks.items():
    anchor='\\label{'+label+'}\n'
    insert='\\textbf{Problem statement with concept highlights.}\n'+marked+'\n\n'
    assert s.count(anchor)==1
    s=s.replace(anchor,anchor+insert,1)
p.write_text(s,encoding='utf-8',newline='\n')
# Exact restoration demonstrates that every pre-existing byte of logical source survives.
restored=s
for label,(_,marked) in blocks.items():
    restored=restored.replace('\\textbf{Problem statement with concept highlights.}\n'+marked+'\n\n','',1)
assert restored==original
print('Verified 11 verbatim copies with context; existing source preserved exactly.')
