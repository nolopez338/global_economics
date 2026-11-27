from pathlib import Path
from decimal import Decimal as D
from statistics import NormalDist
base=Path('book/grade11/term_2/4-learning_evidences')
exam=(base/'G11_T2_L1_C1C2_exam_1.tex').read_text(encoding='utf-8')
sol=(base/'G11_T2_L1_C1C2_exam_solution_1.tex').read_text(encoding='utf-8')
oldexam=Path('tmp/g11-dual-confidence/exam-before.tex').read_text(encoding='utf-8')
oldsol=Path('tmp/g11-dual-confidence/solution-before.tex').read_text(encoding='utf-8')
a=exam.index('An energy-cost review'); b=exam.index('Complete all five',a)
c=sol.index('An energy-cost review'); d=sol.index('Complete all five',c)
assert exam[a:b].replace('\\examtable','\\keytable')==sol[c:d]
assert exam[exam.index('\\SubsectionBox{Savings-account'):]==oldexam[oldexam.index('\\SubsectionBox{Savings-account'):]
for begin,end in [(r'\sectionScored{Savings-account',r'\label{summary:p1}'),(r'\subsection*{Problem 2:',r'\end{document}')]:
    assert sol[sol.index(begin):sol.index(end)]==oldsol[oldsol.index(begin):oldsol.index(end)]
assert D(98)/D(196).sqrt()==7
means=[300,312,320,334,302,318,308,330,298,316]
summary=sol[sol.index(r'\label{summary:p1}'):sol.index(r'\subsection*{Problem 2:')]
for confidence,z,margin,lower,upper,width,count,error in [('.8','1.282','8.974','301.026','318.974','17.948',5,30),('.98','2.326','16.282','293.718','326.282','32.564',8,18)]:
    assert round(NormalDist().inv_cdf((1+float(confidence))/2),3)==float(z)
    assert D(z)*7==D(margin)
    assert D(310)-D(margin)==D(lower) and D(310)+D(margin)==D(upper)
    assert 2*D(margin)==D(width)
    assert sum(abs(D(x)-315)<=D(margin) for x in means)==count
    assert abs(D(count)/10*100-D(confidence)*100)==error
    for value in [z,margin,lower,upper,width]: assert value in summary
    assert f'[{lower},{upper}]' in summary
    print(f'{float(confidence)*100:g}%: z={z}, SE=7, margin={margin}, interval=[{lower},{upper}], width={width}; coverage={count}/10; difference={error} pp')
for rows,total in [(['.25','.25','.5'],1),(['.4','.4','.6','.3','.3'],2),(['.25']*4,1)]: assert sum(map(D,rows))==total
assert D('.125')*2==D('.25') and D('.15')*2==D('.3')
assert sum([2,2,2,2,3,3])==14 and sum([1,2,1,1,2,1,2,2,2])==14
print('PASS: synchronized statements; unchanged Problems 2 and 3; rubric subdivisions; C1=14, C2=14, total=28.')
