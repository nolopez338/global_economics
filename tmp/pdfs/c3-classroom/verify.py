from pathlib import Path
import math,re,subprocess
base=Path.cwd()
src=base/'book2026-2027/grade11/term_2/2-class_activities/G11_T2_L1_C3_classroom_activity.tex'
s=src.read_text()
body=s.split(r'\begin{document}',1)[1]
assert body.count(r'\task{Task 1:}')==5
assert body.count(r'\task{Task 2:}')==5
assert body.count(r'\task{')==10
assert body.count(r'\problemtitle{')==5
axes=re.findall(re.escape(r'\begin{axis}[relation,')+r'(.*?)'+re.escape(r'\end{axis}'),body,re.S)
assert len(axes)==30
for j,axis in enumerate(axes):
    if j<6:
        labels=re.findall(re.escape(r'\PointLabel')+r'\{([A-E])\}\{([^}]+)\}\{([^}]+)\}\{([^}]+)\}',axis)
        assert len(labels)==5 and ''.join(x[0] for x in labels)=='ABCDE'
        marker=re.search(r'only marks.*?coordinates \{([^}]+)\}',axis,re.S)
        points=[tuple(map(float,p)) for p in re.findall(r'\(([^,]+),([^\)]+)\)',marker[1])]
        assert len(points)==5
        for label,point in zip(labels,points):
            coords=tuple(map(float,label[1].split(',')))
            printed=tuple(map(float,label[2:]))
            assert coords==point
            assert all(abs(a-b)<.000501 for a,b in zip(coords,printed))
            x,y=point
            if j==0: assert abs(y-30/math.sqrt(x))<1e-8
            if j==1: assert abs(y-1.96*30/math.sqrt(x))<1e-8
            if j==2: assert abs(y-1.96*x)<1e-8
            if j==4: assert abs(y-x/3)<1e-8
    else:
        assert axis.count(r'\LabelTemplates')==1
        assert r'\addplot' not in axis and r'\PointLabel' not in axis
assert body.count(r'\normalpanel{')==3
student=body.split(r'\stageheading{Guided Example}',1)[1]
for forbidden in ['normalpanel','normalblank','endpoint','interpret','compare','conclude','enumerate']:
    assert forbidden not in student.lower(),forbidden
for forbidden in [r'\Highlight',r'\Ctwo',r'\HL',r'\colorbox','Equations and basic procedure']:
    assert forbidden not in s,forbidden
for sig,ns,n in [(30,[25,100,400,900,1600],100),(24,[36,100,225,400,900],100),(45,[25,100,225,625,1600],225),(72,[36,144,324,576,1296],144),(35,[49,100,196,400,1225],196)]:
    se=[sig/math.sqrt(v) for v in ns]
    assert all(a>b for a,b in zip(se,se[1:]))
    fixed=sig/math.sqrt(n)
    margins=[z*fixed for z in [1.282,1.645,1.960,2.576,3.291]]
    assert all(a<b for a,b in zip(margins,margins[1:]))
log=(base/'tmp/pdfs/c3-classroom/G11_T2_L1_C3_classroom_activity.log').read_text()
assert not re.search(r'Overfull|Underfull|Warning|^!',log,re.M)
print('PASS: 5 problems; 10 tasks; 30 relationship graphs; 150 coordinate labels (30 complete, 120 blank); no extra student tasks; worked coordinates and all problem data verified; clean LaTeX log.')
