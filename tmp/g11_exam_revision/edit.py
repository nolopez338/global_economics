from pathlib import Path
import re

folder = Path('book2026-2027/grade11/term_2/4-learning_evidences')
exam = folder / 'G11_T2_L1_C1C2_exam.tex'
key = folder / 'G11_T2_L1_C1C2_exam_solution.tex'
e, s = exam.read_text(encoding='utf-8'), key.read_text(encoding='utf-8')
labels = ['C1 Task 1','C1 Task 2','C2 Task 1','C2 Task 2','C2 Task 3']
macros = ['cOneA','cOneB','cTwoA','cTwoB','cTwoC']
allocations = [[2,2,1,2,1],[2,2,1,2,1],[3,3,2,2,2]]
def tasklist(points, problem=None):
    lines = [r'\begin{enumerate}[label=(\alph*),itemsep=6pt]']
    for i,(label,macro,mark) in enumerate(zip(labels,macros,points)):
        title = r'\textbf{'+label+'}'
        if problem:
            suffix = ['c1a','c1b','c2a','c2b','c2c'][i]
            title = r'\hyperref[sol:p'+str(problem)+suffix+']{'+title+'}'
        lines.append(r'\item '+title+'. \\'+macro+r' \sscore{\sml{'+str(mark)+'}}')
    return '\n'.join(lines+ [r'\end{enumerate}'])

e = re.sub(r'% Student assessment.*?% Build twice', '% Student assessment with explicit scored tasks in each problem; no solutions.\n% Scoring ledger: Q1 and Q2 C1=2+2=4, C2=1+2+1=4 (8 each).\n% Q3 C1=3+3=6, C2=2+2+2=6 (12); totals C1=14, C2=14, overall=28.\n% Scenario validity is assessed within Q3 task marks; no construction bonus.\n% Build twice', e, count=1, flags=re.S)
e=e.replace('C1 has 11 available points and C2 has 11, for \\textbf{22 points overall}', 'C1 has 14 available points and C2 has 14, for \\textbf{28 points overall}')
for a,b in [(r'\ref*{q:1}&3&3&6',r'\ref*{q:1}&4&4&8'),(r'\ref*{q:2}&3&3&6',r'\ref*{q:2}&4&4&8'),(r'\ref*{q:3}&5&5&10',r'\ref*{q:3}&6&6&12'),(r'\textbf{11}&\textbf{11}&\textbf{22}',r'\textbf{14}&\textbf{14}&\textbf{28}')]: e=e.replace(a,b)
# Remove centralized instructions and allocation table, preserving the problem group.
start=e.index(r'\begingroup\small'+'\n'+r'\SubsectionBox*{General tasks')
end=e.index(r'\begingroup\small'+'\n'+r'\SubsectionBox{Retail',start)
e=e[:start]+e[end:]
e=e.replace(r'C1-\sml{3}\quad C2-\sml{3}',r'C1-\sml{4}\quad C2-\sml{4}').replace(r'C1-\sml{5}\quad C2-\sml{5}',r'C1-\sml{6}\quad C2-\sml{6}')
e=e.replace('6 points overall.','8 points overall.').replace('10 points overall.','12 points overall.')
for p in (1,2):
    e=e.replace(r'\textbf{Complete all five general tasks for this problem.}',r'\columnbreak'+'\n'+r'\textbf{Tasks for this problem}'+'\n'+tasklist(allocations[p-1]),1)
# Give Problem 3 its own page so construction and tasks remain together.
e=e.replace(r'\columnbreak'+'\n'+r'\SubsectionBox{Create',r'\end{multicols}'+'\n'+r'\newpage'+'\n'+r'\begin{multicols}{2}'+'\n'+r'\raggedcolumns'+'\n'+r'\setlength{\parskip}{3pt}'+'\n'+r'\SubsectionBox{Create')
for name in ('e','s'):
    value=locals()[name]
    value=value.replace('Then complete all five general tasks for your own scenario.', 'Then complete the five tasks below for your own scenario.')
    value=value.replace('Scenario completeness and validity are assessed within the task marks in the general scoring table; no separate construction marks are added.', 'Scenario completeness and validity are assessed within the relevant task marks below; no separate construction marks are added.')
    value=value.replace('Each criterion requires at least 4 points from this exam', 'Each criterion requires at least 4 out of 14 points from this exam')
    if name=='e': e=value
    else: s=value
e=e.replace('no separate construction marks are added.','no separate construction marks are added.\n\n'+r'\columnbreak'+'\n'+r'\textbf{Tasks for your scenario}'+'\n'+tasklist(allocations[2]))

s=s.replace('% Governing source:', '% Scoring ledger: Q1/Q2 C1=2+2=4, C2=1+2+1=4; Q3 C1=3+3=6, C2=2+2+2=6.\n% Totals: C1=14, C2=14; overall=28. Construction validity is within Q3 marks.\n% Governing source:',1)
s=s.replace('Problems 1 and 2 each award 3 points to C1 and 3 to C2 (6 overall). Problem 3 awards 5 points to each criterion (10 overall). C1 has 11 available points, C2 has 11, and the exam has 22.', 'Problems 1 and 2 each award 4 points to C1 and 4 to C2 (8 overall). Problem 3 awards 6 points to each criterion (12 overall). C1 has 14 available points, C2 has 14, and the exam has 28.')
s=s.replace(r'C1-\sml{3}\quad C2-\sml{3}',r'C1-\sml{4}\quad C2-\sml{4}').replace(r'C1-\sml{5}\quad C2-\sml{5}',r'C1-\sml{6}\quad C2-\sml{6}')
s=s.replace(r'\score{6 overall}',r'\score{8 overall}').replace(r'\score{10 overall}',r'\score{12 overall}')
s=s.replace('C1: 2.5 and 2.5; C2: 1.5, 2 and 1.5.', 'C1: 3 and 3; C2: 2, 2 and 2.')
# Each original scenario is now followed by a complete linked list, matching the exam.
for p,points in enumerate(allocations,1):
    pattern=r'\\QuestionsTasks\[sec:p'+str(p)+r'\]\{.*?\n\}'
    s,n=re.subn(pattern,lambda m:tasklist(points,p)+'\n'+r'\secInicio[][sec:p'+str(p)+']',s,count=1,flags=re.S)
    assert n==1
    begin=s.index(r'\sectionScored{',s.index(r'\begin{document}')) if p==1 else s.index(r'\sectionScored{'+('Savings-account interest' if p==2 else 'Create an integrated scenario from scratch'))
    end=s.index(r'\sectionScored{',begin+1) if p<3 else s.index(r'\section{Summarized Solutions}',begin)
    block=s[begin:end]
    for label,macro,mark in zip(labels,macros,points):
        block=re.sub(r'(\\taskprompt\{'+label+r'\}\{)[^}]+',lambda m:m[1]+str(mark),block)
        block=re.sub(r'(\\worked\{'+label+r' \\score\{)[^}]+',lambda m:m[1]+str(mark),block)
    s=s[:begin]+block+s[end:]

# Align shared table instructions with the exam's existing four-column specification.
s=s.replace('Use full-width section headings in this order:', 'Use contiguous groups in this order:').replace('The three columns are Symbol, Concept and Meaning in context.', 'Columns are Symbol, Concept, Type and Meaning in context.')
# Revise detailed proposed rubrics without changing the mathematical work.
s=s.replace('C1 Task 1&1.5&0.5 population and both sample scopes/sizes; 0.5 mean/SD pairings, units and known status; 0.5 counts, both proportions and meanings, unknown population proportion.', 'C1 Task 1&2&0.5 population and both sample scopes/sizes; 0.75 mean/SD pairings, units and known status; 0.75 counts, both proportions and meanings, unknown population proportion.')
s=s.replace('C1 Task 2&1.5&0.75 for three signed differences (0.25 each, including percentage points); 0.75 fixed parameters and scope with sampling-variation explanation.', 'C1 Task 2&2&1.5 for three signed differences (0.5 each, including percentage points); 0.5 fixed parameters and scope with sampling-variation explanation.')
s=s.replace('C2 Task 2&1&0.2 point estimate; 0.2 correct margins using known SD; 0.3 endpoints and intervals; 0.15 full widths; 0.15 units and contextual mean interpretation.', 'C2 Task 2&2&0.4 point estimate; 0.4 correct margins using known SD; 0.6 endpoints and intervals; 0.3 full widths; 0.3 units and contextual mean interpretation.')
s=s.replace('C1: $1.5+1.5=3$; C2: $1+1+1=3$; problem total: 6.', 'C1: $2+2=4$; C2: $1+2+1=4$; problem total: 8.')
s=s.replace('Proposed partial-credit guidance: 10 points','Proposed partial-credit guidance: 12 points')
s=s.replace('C1 Task 1&2.5&0.5 complete fixed population scope and sizes; 0.5 two clearly defined independent samples with feasible summaries and valid binary counts;', 'C1 Task 1&3&0.75 complete fixed population scope and sizes; 0.75 two clearly defined independent samples with feasible summaries and valid binary counts;')
s=s.replace('C1 Task 2&2.5&1.5 three correct signed differences (0.5 each; percentage points for proportions); 1 fixed population characteristics and sound explanation of sample variation.', 'C1 Task 2&3&1.5 three correct signed differences (0.5 each; percentage points for proportions); 1.5 fixed population characteristics and sound explanation of sample variation.')
s=s.replace('C2 Task 1&1.5&0.5 adequate assumptions, negligible fractions, same-population study design and known spread; 0.5 completed parameter/sample groups, initially unknown mean and explicitly later comprehensive investigation; 0.5 SE and complete confidence/significance/tails/critical-value settings.', 'C2 Task 1&2&0.5 adequate assumptions, negligible fractions, same-population study design and known spread; 0.75 completed parameter/sample groups, initially unknown mean and explicitly later comprehensive investigation; 0.75 SE and complete confidence/significance/tails/critical-value settings.')
s=s.replace('C2 Task 2&2.00&','C2 Task 2&2&')
s=s.replace('C2 Task 3&1.5&0.5 complete, valid subsequent evidence consistent with the procedure and later mean; 0.5 counts, coverage and absolute percentage-point difference; 0.5 long-run/finite-study explanation with no fixed-mean probability error.', 'C2 Task 3&2&0.75 complete, valid subsequent evidence consistent with the procedure and later mean; 0.75 counts, coverage and absolute percentage-point difference; 0.5 long-run/finite-study explanation with no fixed-mean probability error.')
s=s.replace('C1: $2.5+2.5=5$; C2: $1.5+2+1.5=5$; overall: $5+5=10$.','C1: $3+3=6$; C2: $2+2+2=6$; overall: $6+6=12$.')
s=s.replace('C1: $3+3+5=11$; C2: $3+3+5=11$; overall: $6+6+10=22$. Pass each criterion independently with at least 4 points;', 'C1: $4+4+6=14$; C2: $4+4+6=14$; overall: $8+8+12=28$. Pass each criterion independently with at least 4 out of 14 points;')
exam.write_text(e,encoding='utf-8')
key.write_text(s,encoding='utf-8')
print('Updated exam and solution sources.')
