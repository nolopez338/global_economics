from pathlib import Path
from itertools import permutations, product, combinations
from math import factorial
import hashlib, json

root=Path(__file__).resolve().parents[2]
target=root/'book2026-2027/fundamentals/permutations1-introduction-slides.tex'
source=root/'book2026-2027/fundamentals/permutations1.tex'
original_hash=hashlib.sha256(source.read_bytes()).hexdigest()
# Preserve the established starter typography and footer, entirely inline.
old=target.read_text(encoding='utf-8')
preamble=old[:old.index('\\usetikzlibrary')]
preamble+=r'''
\usetikzlibrary{shapes.geometric,decorations.pathreplacing,arrows.meta}
\usepackage{cancel}
\definecolor{CircleBlue}{HTML}{2879B9}
\definecolor{TriangleOrange}{HTML}{DD8428}
\definecolor{SquareGreen}{HTML}{398553}
\definecolor{DiamondPurple}{HTML}{8954A2}
% Source map: permutations1.tex, Introduction: Counting Choices ONLY.
% Stop before Worked Examples. The source practice is preserved unchanged.
% Case 1: multiplication paragraph; case 2: factorial bullet;
% case 3: ordered positions bullet; case 4: unordered groups bullet;
% case 5: indistinguishable copies bullet; closing frames synthesize these.
% The fifteen concrete illustrations and opening are specified by the user.
% Scope adaptation: no official criteria, invented metadata or highlight registry.
% Colors identify supplied shape types, not mathematical highlight roles.
% Shapes, identifiers, outlines and text preserve meaning in grayscale.
\tikzset{every picture/.style={draw=GEInk,text=GEInk,line width=.7pt},
 group/.style={draw=GEInk,rounded corners=2mm,line width=1pt},
 object/.style={draw=GEInk,minimum size=3.4mm,inner sep=0pt},
 C/.style={object,circle,fill=CircleBlue},
 T/.style={object,regular polygon,regular polygon sides=3,fill=TriangleOrange},
 S/.style={object,rectangle,fill=SquareGreen},
 D/.style={object,diamond,aspect=1,fill=DiamondPurple}}
% Object identifiers are ABOVE objects. Position/job labels are BELOW rows.
\newcommand{\Obj}[4]{\node[#1] at (#2,#3) {};\node[font=\small] at (#2,{#3+.30}) {#4};}
\newcommand{\Q}[1]{\textbf{#1}\par}
\newcommand{\DiagramStart}{\par\centering\begin{tikzpicture}
 \path[use as bounding box] (-.05,-.55) rectangle (13.55,4.05);}
\newcommand{\DiagramEnd}{\end{tikzpicture}\par\raggedright}
\begin{document}
'''
frames=[]
audit=[]
def vis(s,ov='2-'): return '\\visible<'+str(ov)+'>{'+s+'}'
def node(x,y,t,ov=None,opts=''):
    s=rf'\node[{opts}] at ({x},{y}) {{{t}}};'
    return vis(s,ov) if ov else s
def box(x1,y1,x2,y2,ov='3-',style='group'):
    return vis(rf'\draw[{style}] ({x1},{y1}) rectangle ({x2},{y2});',ov)
def obj(t,x,y,label=''): return rf'\Obj{{{t}}}{{{x}}}{{{y}}}{{{label}}}'
def row(vals,x,y,types=None,ov=None,labels=True,positions=False,step=.54,tail=None):
    types=types or ['C']*len(vals)
    s=''
    for j,(v,t) in enumerate(zip(vals,types)):
        a=obj(t,round(x+j*step,3),y,str(v) if labels else '')
        if tail is not None and j>=tail:
            a=r'\begin{scope}[opacity=.30]'+a+r'\end{scope}'
        s+=a
        if positions:
            s+=node(round(x+j*step,3),y-.32,str(j+1),opts='font=\small')
    return vis(s,ov) if ov else s
def pool(n):
    return row(range(1,n+1),4.8,2.8,step=1.1)+node(6.7,3.65,'Available distinct objects')
def caption(lines):
    # One reasoning step at a time in a fixed-size, space-reserving area.
    parts=[]
    for j,(ov,t) in enumerate(lines):
        if ov.endswith('-') and j+1<len(lines):
            end=int(lines[j+1][0].split('-')[0])-1
            ov=ov[:-1] if end==int(ov[:-1]) else ov+str(end)
        parts.append(r'\only<'+ov+'>{'+t+r'\par}')
    return r'\begin{overlayarea}{\linewidth}{1.15cm}'+ '\n'.join(parts)+r'\end{overlayarea}'
def frame(title,q,diagram='',lines=(),note='',section=None):
    idx=len(frames)+1
    s=(rf'\section{{{section}}}'+'\n' if section else '')
    s+=f'% Frame {idx}. Teaching note: {note or q}\n'
    s+=rf'\begin{{frame}}[t]{{{title}}}'+'\n'+rf'\Q{{{q}}}'+'\n'
    if diagram: s+='\\DiagramStart\n'+diagram+'\n\\DiagramEnd\n'
    s+=caption(lines)+'\n\\end{frame}\n'
    frames.append(s)
def intro(title,n,outcome,types=None):
    d=pool(n) if types is None else ''.join(row(range(1,k+1),x,2.7,[t]*k,step=.75)+node(x+.4,1.8,name) for t,k,x,name in types)
    if title.startswith('2'):
        for j in range(n):
            x=5.2+j*.95
            d+=rf'\draw ({x-.3},.6) rectangle ({x+.3},1.25);'
            d+=node(x,.25,str(j+1),opts='font=\small')
        d+=node(6.75,-.3,'Empty left-to-right positions',opts='font=\small')
        d+=node(6.75,1.55,outcome,opts='font=\small')
    else: d+=node(6.75,.5,outcome)
    frame(title,'Predict: how many different outcomes are possible?',d,
          note='Collect predictions before revealing outcomes. Numbers identify objects; never multiply the identifiers.')
def grid_ordered(n,r,title,section=None):
    ps=list(permutations(range(1,n+1),r)); d=''
    width=12.8/n
    for a in range(1,n+1):
        x=.65+(a-1)*width
        d+=node(x+.5,3.55,rf'First: {a}',opts='font=\small')
        for j,p in enumerate(v for v in ps if v[0]==a):
            y=2.75-j*.9
            d+=row(p,x,y,ov=f'{a+1}-',step=1.25 if r==2 else .54)
            if r==2:
                d+=node(x,y-.32,'Reader',ov=f'{a+1}-',opts='font=\small')
                d+=node(x+1.25,y-.32,'Recorder',ov=f'{a+1}-',opts='font=\small')
        d+=box(x-.65,2.75-(n-2)*.9-.52,x+(r-1)*(1.25 if r==2 else .54)+.8,3.3,f'{n+2}-')
    frame(title,'How many choices remain after the first object is used?',d,
          [(f'{n+2}-',f'{n} first-object groups; {n-1} assignments in each.'),
           (f'{n+3}-',rf'${n}\times{n-1}={len(ps)}$ assignments. Each object is used at most once.')],
          'Columns fix the Reader. Recorder excludes that object. No repeated-object rows.',section)
    audit.append(dict(kind='ordered',n=n,r=r,rows=ps,count=len(ps)))
    return ps

# Opening: five cases with miniature diagrams, no formulas.
d=''
opening=[('Choose one from each input group',['C','T'],[1,1]),
 ('Arrange all distinct objects',['C','C','C'],[1,2,3]),
 ('Fill some ordered positions',['C','C'],[1,2]),
 ('Choose a group without roles',['C','C'],[1,2]),
 ('Arrange indistinguishable copies',['C','C','T'],['','',''])]
for i,(txt,types,vals) in enumerate(opening):
    y=3.45-i*.79
    d+=node(.1,y,rf'{i+1}. {txt}',opts='anchor=west')
    d+=row(vals,10.5,y-.07,types)
    if i==0:d+=r'\draw (10.25,3.12) rectangle (10.75,3.85);\draw (10.79,3.12) rectangle (11.29,3.85);'
    if i==2:d+=node(10.5,y-.34,'1',opts='font=\small')+node(11.04,y-.34,'2',opts='font=\small')
    if i==3:d+=r'\draw (10.77,1.03) ellipse (.65 and .43);'
frame('Counting choices: five cases','What counts as one different outcome?',d,section='Five cases',note='Opening overview deliberately has no formulas. Return to the question for every example.')
frame('How to read our objects','Does object 2 mean a value of two?',
      row([1,2,3],4.8,2.6,step=1.1)+node(6,1.4,'Same shape and color; different identities.'),
      [('2-','No. A number above a shape identifies that object.'),('3-','Position labels go below the row. Shapes also work without color.')],
      'Misconception: multiplying object labels. Count choices, not the identifying numbers.')

# CASE 1
intro('1A. One circle, then one triangle',0,'One outcome: one circle followed by one triangle.',
      [('C',2,2,'Circle choices'),('T',3,7,'Triangle choices')])
def mult_grid(a,b,circle_fixed=False):
    d=''; cells=[]
    for i in range(a):
        for j in range(b):
            x=1.5+j*(10.5/(b-1)); y=2.8-i*(2.4/max(1,a-1))
            vals=[1,i+1,j+1] if circle_fixed else [i+1,j+1]
            ts=['C','T','S'] if circle_fixed else ['C','T']
            d+=row(vals,x,y,ts,ov=f'{i+2}-',step=.55)
            cells.append(vals)
    return d,cells
d,cells=mult_grid(2,3)
for i in range(2):d+=box(1.05,2.8-i*2.4-.45,12.95,2.8-i*2.4+.57,'4-5')
for j in range(3):d+=box(1.05+j*5.25,-.05,2.5+j*5.25,3.37,'6-')
frame('1A. The same outcomes, two organizations','How many outcomes are in each visual group?',d,
      [('4-5',r'Two row groups; three outcomes in each.'),('5',r'$2\times3=6$ outcomes.'),
       ('6-',r'Three column groups; two outcomes in each.'),('7-',r'$3\times2=6$. These are the same six outcomes.')],
      'Reveal rows in order. At overlay 6 replace row boundaries with column boundaries; do not move outcomes.',section='1. Choose from input groups')
audit.append(dict(kind='product',sizes=[2,3],rows=cells,count=6))
intro('1B. One circle, one triangle, one square',0,'One outcome: circle, triangle, square, in that order.',
      [('C',1,1,'Circle'),('T',3,4,'Triangles'),('S',4,9,'Squares')])
d,cells=mult_grid(3,4,True)
d+=box(1.05,-.06,13.48,3.38,'5-6')
for i in range(3):d+=box(1.05,2.8-i*1.2-.43,13.48,2.8-i*1.2+.55,'7-8')
for j in range(4):d+=box(1.05+j*3.5,-.06,2.95+j*3.5,3.38,'9-10')
frame('1B. All outcomes keep the same circle','Which choices change across rows and columns?',d,
      [('5-6','One outer group: there is only one circle choice.'),
       ('7-8','Three row groups: one for each triangle; four outcomes each.'),
       ('9-10','Four column groups: one for each square; three outcomes each.'),
       ('11-',r'$1\times3\times4=12$. The circle step offers no alternative.')],
      'Only one grouping view at a time. The factor 1 never creates another branch.')
audit.append(dict(kind='product',sizes=[1,3,4],rows=cells,count=12))
intro('1C. Four input groups',0,'One outcome: circle, triangle, square, diamond.',
      [('C',2,.7,'Circles'),('T',2,3.7,'Triangles'),('S',2,7,'Squares'),('D',2,10.5,'Diamonds')])
def panels(boundaries=True):
    d=''; cells=[]
    for a,b in product(range(1,3),repeat=2):
        x=.6+(b-1)*6.7; y=3.0-(a-1)*2.0
        d+=node(x,y+.43,'Fixed:',opts='anchor=west,font=\small')+row([a,b],x+1.3,y+.43,['C','T'])
        for c,e in product(range(1,3),repeat=2):
            xx=x+(e-1)*2.8; yy=y-.3-(c-1)*.82
            d+=row([a,b,c,e],xx,yy,['C','T','S','D'],ov=f'{2+(a-1)*2+b-1}-',step=.46)
            cells.append([a,b,c,e])
        if boundaries: d+=box(x-.3,y-1.48,x+4.7,y+.97,'6-8')
    return d,cells
d,cells=panels()
frame('1C. Four panels, each with its own fixed start','How many outcomes belong to each panel?',d,
      [('6-','Four panels. Inside each: two square choices and two diamond choices.'),
       ('7-',r'Four outcomes per panel: $4\times4=16$.'),
       ('8-',r'Each $4$ is $2\times2$, so $2\times2\times2\times2=16$.')],
      'Panel rows fix circle; panel columns fix triangle. Inside panels rows vary square and columns vary diamond.')
# Unchanged grid with alternative boundaries.
d,_=panels(False)
for y in [3,1]:d+=box(.3,y-1.48,12,y+.97,'6-7')
for a,b,c,e in product(range(1,3),repeat=4):
    x=.6+(b-1)*6.7+(e-1)*2.8; y=3-(a-1)*2-.3-(c-1)*.82
    d+=box(x-.25,y-.25,x+1.65,y+.5,'8-9' if e==1 else '10-',style='group,dashed' if e==1 else 'group')
frame('1C. Regroup without moving any outcome','Can the same sixteen outcomes make two groups of eight?',d,
      [('6-7',r'Circle 1 gives eight; circle 2 gives eight. $2\times8=16$.'),
       ('8-9','The eight dashed boxes all end in diamond 1: one group of eight.'),
       ('10-',r'The other eight all end in diamond 2: another group. $2\times8=16$.')],
      'Last-choice groups are nonadjacent cells. Use different boundary overlays, never simultaneous panel/row/cell outlines.')
audit.append(dict(kind='product',sizes=[2,2,2,2],rows=cells,count=16))
frame('The multiplication principle','When can we multiply choice counts?',
      node(2,2.5,'Step 1')+node(6.5,2.5,'Step 2')+node(11,2.5,'Step 3')+
      node(2,1.4,'2 choices')+node(6.5,1.4,'3 choices each')+node(11,1.4,'4 choices each'),
      [('2-','Every earlier choice must leave the same next-step choice count.'),
       ('3-',r'The numbers can differ between steps: $2\times3\times4$.'),
       ('4-','Multiply the step counts to count complete outcomes.')],
      'Equal branch counts at each step are the condition; the factors need not equal one another.')

# CASE 2
intro('2A. Arrange both distinct objects',2,'Use every object once. Read positions from left to right.')
d=row([1,2],5.6,2.6,ov='2-',positions=True)+row([2,1],5.6,1,ov='3-',positions=True)
d+=box(5.2,2.08,6.6,3.18,'4-')+box(5.2,.48,6.6,1.58,'4-')
frame('2A. Both possible rows','Does exchanging the objects change the row?',d,
      [('4-','Two first-position groups; one row in each.'),('5-',r'$2\times1=2$ rows. Yes: the objects exchange positions.')],
      'Position numbers below the rows are separate from identifiers above the circles.',section='2. Arrange all distinct objects')
intro('2B. Arrange three distinct objects',3,'Use every object once in three left-to-right positions.')
d=''
for a in range(1,4):
    x=1.4+(a-1)*4.2
    d+=node(x+.54,3.5,rf'First object: {a}',opts='font=\small')
    for j,p in enumerate(p for p in permutations(range(1,4)) if p[0]==a):
        d+=row(p,x,2.65-j*1.35,ov=f'{a+1}-',positions=True)
    d+=box(x-.4,.75,x+1.5,3.2,'5-')
frame('2B. Three first-position groups','How many rows start with each first object?',d,
      [('5-','Three first choices. Each group has two orders of the remaining objects.'),
       ('6-',r'Three positions give $3\times2\times1=6=3!$ rows.')],
      'List complete outcomes before naming factorial. Do not treat these three columns as three outcomes.')
audit.append(dict(kind='ordered',n=3,r=3,rows=list(permutations(range(1,4))),count=6))
d=node(.4,3.25,'Available:',opts='anchor=west')+row([1,2,3],4.5,3.1,step=1.4)
for j in range(3):
    x=3+j*3.3
    d+=rf'\draw ({x-.45},.9) rectangle ({x+.45},1.8);'+node(x,.5,f'Position {j+1}',opts='font=\small')
    d+=row([j+1],x,1.25,ov=f'{j+2}-')
    xx=4.5+j*1.4
    d+=vis(rf'\draw ({xx-.24},2.88)--({xx+.24},3.55);\draw ({xx+.24},2.88)--({xx-.24},3.55);',f'{j+2}-')
    d+=node(x,0,rf'{3-j} '+('choice' if j==2 else 'choices'),ov=f'{j+2}-',opts='font=\small')
frame('2B. Follow one path through the positions','Why do the choice counts decrease?',d,
      [('2','Use object 1: it cannot be chosen again.'),('3','Use object 2: only object 3 remains.'),
       ('4-','Every other path has the same counts: three, then two, then one.')],
      'Synchronize used-object crosses with filled boxes. Crosses mean already placed, not removed from the outcome.')
intro('2C. Arrange four distinct objects',4,'Use every object once in four left-to-right positions.')
for firsts in [(1,2),(3,4)]:
    d=''
    for col,a in enumerate(firsts):
        x=1+col*6.5
        d+=node(x+1,3.85,rf'First object: {a}',opts='font=\small')
        others=[v for v in range(1,5) if v!=a]
        for j,b in enumerate(others):
            y=3.2-j*1.3
            remain=[v for v in others if v!=b]
            for k,tail in enumerate(permutations(remain)):
                d+=row([a,b,*tail],x,y-k*.65,ov=f'{j+2}-',step=.6)
            d+=box(x-.35,y-.96,x+2.2,y+.48,'5-')
            d+=node(x+3.55,y-.1,rf'Second: {b}',ov='5-',opts='font=\small')
        d+=box(x-.55,-.5,x+4.65,4.05,'6-')
    frame(f'2C. Complete rows starting with {firsts[0]} or {firsts[1]}',
          'How many second-position subgroups fit inside each block?',d,
          [('5-','Three second-position subgroups; two rows in every subgroup.'),
           ('6-','Each first-position block has six complete rows. The last object is forced.')],
          'All twelve rows on this frame are complete; the next frame keeps identifiers and shows the other two blocks.')
audit.append(dict(kind='ordered',n=4,r=4,rows=list(permutations(range(1,5))),count=24))
d=''
for a in range(1,5):
    x=1.6+(a-1)*3.35
    d+=box(x-1,1,x+1,3.4,'2-')+row([a],x,2.8)
    d+=node(x,1.7,'6 rows',ov='2-')
frame('2C. Put the four blocks together','What does each factor count?',d,
      [('2-','Four first-position blocks, with six rows in each.'),
       ('3-',r'$4\times3\times2\times1=24=4!$.'),
       ('4-','First choice; second choice; third choice; one last object.')],
      'The four six-row blocks correspond exactly to the preceding two frames; none is omitted.')
frame('Factorial names a decreasing product','How would this work for any number of distinct objects?',
      node(6.75,2.7,r'$n!=n\times(n-1)\times\cdots\times2\times1$',ov='3-',opts='font=\Large')+
      node(6.75,1.2,r'$4!=4\times3\times2\times1$',ov='4-'),
      [('2-','$n$ is the total number of objects, a whole number.'),
       ('3-',r'$!$ means factorial: multiply down to 1. Here $n\geq1$.'),
       ('4-',r'$n-1$ means one fewer; the dots mean keep decreasing by one.')],
      'Factorial is introduced after all three concrete examples. The exclamation mark is an operation, not another factor.')
frame('One object, and the empty arrangement','How many arrangements can one object make? How about none?',
      row([1],3,2.5)+node(3,1.2,r'$1!=1$',ov='2-')+
      node(10,2.5,'[ empty row ]')+node(10,1.2,r'$0!=1$',ov='3-'),
      [('2-','One object has exactly one arrangement.'),('3-','No objects have one empty arrangement. We define zero factorial as 1.')],
      'Zero objects is not zero outcomes: the one empty arrangement is the outcome.')

# CASE 3
intro('3A. One Reader from three objects',3,'One assignment contains only the selected Reader.')
d=''
for a in range(1,4):
    x=2+(a-1)*4.5
    d+=row([a],x,2.6,ov=f'{a+1}-')+node(x,1.9,'Reader',opts='font=\small')
frame('3A. Three one-position assignments','How many choices fill the single job?',d,
      [('5-','Three choices for one position: three assignments.')],
      'Unused objects are absent from the assignment. Only the selected Reader is counted.',section='3. Fill some ordered positions')
d=''
for a in range(1,4):
    x=1.5+(a-1)*4.2
    for j,p in enumerate(p for p in permutations(range(1,4)) if p[0]==a):
        y=2.7-j*1.3
        d+=row(p,x,y,ov='2-',tail=1,step=.65)
    d+=node(x,.55,'Reader',opts='font=\small')+node(x+1,.55,'unused tail',opts='font=\small')
    d+=box(x-.4,.9,x+1.7,3.3,'3-')
frame('3A. Full rows overcount the Reader assignment','Do the two faded tail orders change the Reader?',d,
      [('3-','No. Both rows in a box give the same one-position assignment.'),
       ('4-',r'Each assignment has $2!$ orders of its unused objects.'),
       ('5-',r'$3!\div2!=6\div2=3$ Reader assignments.')],
      'The divisor counts orders of unused objects, never the selected Reader. Keep faded tails visible.')
intro('3B. Reader and Recorder from three',3,'One assignment: Reader first, Recorder second. No object repeats.')
grid_ordered(3,2,'3B. Every ordered two-job assignment')
frame('3B. The unused object has one order','Why is the unused-tail divisor now only one?',
      row([1,2,3],5,2.7,tail=2,step=1.2)+node(5,1.8,'Reader',opts='font=\small')+
      node(6.2,1.8,'Recorder',opts='font=\small')+node(7.4,1.8,'Unused',opts='font=\small'),
      [('2-','After two jobs are filled, only one object is unused.'),
       ('3-',r'Its single order contributes $1!$: $3!\div1!=6$ assignments.')],
      'Every two-job assignment has exactly one full-row completion; do not divide by two job orders.')
intro('3C. Reader and Recorder from four',4,'One assignment has two job holders. The other two are unused.')
assignments=grid_ordered(4,2,'3C. Four columns of three assignments')
d=''
for a in range(1,5):
    for j,p in enumerate(p for p in assignments if p[0]==a):
        x=.5+(a-1)*1.65;y=2.9-j*.95
        d+=row(p,x,y,step=.5)
d+=node(3.1,.03,'All twelve assignments',opts='font=\small')
for j,p in enumerate([(1,2),(1,3)]):
    x=8.1;y=3-j*1.8
    remain=[v for v in range(1,5) if v not in p]
    for k,t in enumerate(permutations(remain)):
        d+=row([*p,*t],x,y-k*.65,ov=f'{j+2}-',tail=2,step=.8)
    d+=box(x-.3,y-.94,x+2.8,y+.55,f'{j+2}-')
    d+=vis(rf'\draw[decorate,decoration={{brace,mirror}}] ({x+1.35},{y-1})--({x+2.7},{y-1});',f'{j+2}-')
    d+=node(x+2,y-1.25,'unused tail',ov=f'{j+2}-',opts='font=\small')
frame('3C. Completion boxes explain the divisor','How many full rows complete each two-job assignment?',d,
      [('4-','Every assignment leaves two unused objects: exactly two tail orders.'),
       ('5-',r'$24$ full rows $\div2$ completions per assignment $=12$ assignments.')],
      'Left grid remains complete. Right boxes illustrate 12 and 13; every one of the twelve has exactly the same two-completion structure.')
frame('3C. Cancel the unused tail','Which factors count only unused-tail orders?',
      node(6.75,2.8,r'$\displaystyle\frac{4!}{2!}=\frac{4\times3\times\underbrace{(2\times1)}_{\text{unused orders}}}{2\times1}$',ov='2-')+
      node(6.75,.9,r'$\displaystyle\frac{4\times3\times\cancel{(2\times1)}}{\cancel{(2\times1)}}=4\times3=12$',ov='3-'),
      [('2-','The selected positions keep their order.'),('3-','Divide by the two orders of the unused tail.')],
      'Cancellation removes equal multiplicities. It does not identify Reader--Recorder with Recorder--Reader.')
frame('Some ordered positions: the general rule','What do the symbols count?',
      node(6.75,2.9,r'$n$ available; $r$ positions; $n-r$ unused',ov='2-')+
      node(6.75,1.5,r'$\displaystyle n(n-1)\cdots(n-r+1)=\frac{n!}{(n-r)!}$',ov='3-')+
      node(6.75,.3,r'Keep $r$ decreasing choice counts.',ov='3-'),
      [('2-',r'$n,r$ are whole numbers; $0\leq r\leq n$. No object is used twice.'),
       ('3-',r'The last position has $n-r+1$ choices: $r-1$ objects are already used.'),
       ('4-',r'Or divide full rows by the $(n-r)!$ orders of each unused tail.')],
      'For r=0 there is one empty assignment; for r=n the divisor is 0!=1. The dots represent r factors, even if r is small.')

# CASE 4
intro('4A. Choose two members from three',3,'No jobs or position labels. A group contains members, not roles.')
def membership(vals,x,y,ov='3-'):
    return vis(rf'\draw ({x+.28*(len(vals)-1)},{y+.1}) ellipse ({.45+.28*(len(vals)-1)} and .48);'+row(vals,x,y,step=.56),ov)
def pairs_frame(n,title,starting=False):
    pairs=list(combinations(range(1,n+1),2));d=''
    for j,p in enumerate(pairs):
        col=j%3; rr=j//3;x=1.2+col*4.4;y=3.0-rr*1.9
        d+=row(p,x,y,ov='2-')+row(p[::-1],x+1.6,y,ov='2-')
        d+=box(x-.35,y-.35,x+2.5,y+.55,'3-')
        d+=membership(p,x+.8,y-.95,'4-')
    count=n*(n-1)
    frame(title,'How many ordered lists name the same group?',d,
          [('3-',f'{count} ordered lists; two lists in each membership box.'),
           ('4-',f'{len(pairs)} groups. An oval has members, with no labelled positions.'),
           ('5-',rf'${count}\div2!={len(pairs)}$ distinct groups.')],
          'Each box pairs ab with ba. The oval below represents that single membership, not an extra outcome.',
          '4. Choose a group without roles' if n==3 else None)
    audit.append(dict(kind='groups',n=n,r=2,groups=[list(permutations(p)) for p in pairs],count=len(pairs)))
pairs_frame(3,'4A. Six lists become three groups')
intro('4B. Choose two members from four',4,'Same objects as before. Remove jobs; keep only membership.')
d=''
for a in range(1,5):
    for j,p in enumerate(p for p in assignments if p[0]==a):
        d+=row(p,1+(a-1)*3.4,2.9-j*1.05,ov=f'{a+1}-')
frame('4B. Begin with the same twelve ordered lists','Which lists contain exactly the same members?',d,
      [('6-','Now reorganize these twelve lists into pairs with the same members.')],
      'This is the preceding twelve-assignment grid with job labels removed. Next frame changes arrangement explicitly.')
pairs_frame(4,'4B. Pair lists by membership')
frame('4B. Write the same division with factorials','What does each divisor remove?',
      node(6.75,2.7,r'$\displaystyle\frac{4!}{2!}=12\quad\hbox{ordered lists}$',ov='2-')+
      node(6.75,1.2,r'$\displaystyle\frac{4!}{2!\,2!}=12\div2=6\quad\hbox{groups}$',ov='3-'),
      [('2-','The unused-tail orders were removed to get the twelve lists.'),
       ('3-','Now remove the two list orders of each selected pair as well.')],
      'The two 2! factors happen to have the same value but count different things.')
intro('4C. Choose three members from four',4,'One group contains three distinct members, with no roles.')
teams=list(combinations(range(1,5),3))
d=''
for j,p in enumerate(permutations(teams[0])):
    x=1.4+(j//2)*4.2;y=2.8-(j%2)*1.25
    d+=row(p,x,y,ov=f'{j//2+2}-')
for col in range(3):d+=box(1.05+col*4.2,1.05,2.9+col*4.2,3.35,'5-')
frame('4C. Develop one membership block: 1, 2, 3','How many lists can name this one group?',d,
      [('5-','Three first-member columns; two orders of the remaining members.'),
       ('6-',r'$3\times2\times1=3!=6$ lists, all naming one group.')],
      'These are orders of the selected members. None of the six lists makes a different membership.')
for half in [teams[:2],teams[2:]]:
    d=''
    for j,team in enumerate(half):
        x=1+j*6.5
        d+=node(x+1.9,3.55,'Members '+', '.join(map(str,team)),opts='font=\small')
        for k,p in enumerate(permutations(team)):
            # Three first-member subgroups, with two orders each.
            xx=x+(k//2)*1.75; yy=2.7-(k%2)*1.0
            d+=row(p,xx,yy,ov=f'{j+2}-',step=.47)
        d+=box(x-.3,1.1,x+4.85,3.25,'4-')
        d+=membership(team,x+1.65,.35,'5-')
    frame('4C. Two membership blocks','Does changing the list change the members?',d,
          [('4-','Each block contains six lists of its own three members.'),
           ('5-','Each block collapses to one membership diagram.')],
          'The two frames together show all 24 ordered triples. Ovals are one-per-block summaries.')
audit.append(dict(kind='groups',n=4,r=3,groups=[list(permutations(t)) for t in teams],count=4))
d=''
for j,t in enumerate(teams):
    x=.8+j*3.35
    d+=box(x-.3,1.1,x+2.0,3.4,'2-')+membership(t,x+.3,2.6,'2-')
    d+=node(x+.85,1.5,'6 lists',ov='2-',opts='font=\small')
frame('4C. Four blocks, six lists in each','How do twenty-four lists become four groups?',d,
      [('2-','Four membership blocks have the same six-list structure.'),
       ('3-',r'$24$ ordered lists $\div6$ lists per group $=4$ groups.')],
      'Division works because every block has equal size, not because lists are simply discarded.')
frame('Groups: divide by orders of the selected members','How many lists name every group of r members?',
      node(6.75,2.9,r'Every $r$-member group has $r!$ lists.',ov='2-')+
      node(6.75,1.4,r'$\displaystyle\binom nr=\frac{\text{ordered choices}}{\text{orders per group}}=\frac{n!}{r!(n-r)!}$',ov='3-')+
      node(6.75,.2,r'Read the symbol as ``$n$ choose $r$.''',ov='4-'),
      [('3-',r'$(n-r)!$ removes orders of the unused objects.'),
       ('4-',r'$r!$ removes list orders of the selected members. Membership stays the same.')],
      'n counts available distinct objects; r counts members, 0<=r<=n. The denominator factors remove different overcounts.')

# CASE 5
frame('5A. Two matching circles and one triangle','Predict: how many different visible rows can we make?',
      row(['','',''],5,2.6,['C','C','T'],step=1.1)+node(6.4,1.2,'Place every supplied copy exactly once.'),
      [('2-','Positions matter. Exchanging matching circles makes no visible change.')],
      'Copies begin without numbers; temporary identifiers appear only in the next labelled counting stage.',section='5. Arrange indistinguishable copies')
d=''
for col,tpos in enumerate([2,1,0]):
    x=1.4+col*4.2
    d+=node(x+.55,3.55,['Triangle last','Triangle middle','Triangle first'][col],opts='font=\small')
    for rr,cids in enumerate([(1,2),(2,1)]):
        vals=[];ts=[];i=0
        for pos in range(3):
            ts.append('T' if pos==tpos else 'C'); vals.append('' if pos==tpos else cids[i]); i+=pos!=tpos
        s=''
        for j,(v,t) in enumerate(zip(vals,ts)):
            lab=(rf'\alt<5->{{}}{{{v}}}' if v!='' else '')
            s+=obj(t,x+j*.55,2.7-rr*1.25,lab)
        d+=vis(s,f'{col+2}-')
    d+=box(x-.35,.95,x+1.45,3.25,'6-')
frame('5A. Count with temporary circle identifiers','Which labelled rows become identical when identifiers vanish?',d,
      [('4',r'Three labelled objects give $3!=6$ rows.'),
       ('5','Erase only the temporary identifiers. Both rows remain visible.'),
       ('6-','Each outlined pair is now two copies of the same visible row.')],
      'Overlay 5 removes labels without moving shapes. Overlay 6 encloses equal pairs after the change is visible.')
d=''
for col,tpos in enumerate([2,1,0]):
    ts=['C']*3;ts[tpos]='T';d+=row(['']*3,1.4+col*4.2,2.5,ts)
frame('5A. Keep one row from each matching pair','Why divide by two circle-label orders?',d,
      [('2-',r'Every visible row had $2!=2$ labelled versions.'),
       ('3-',r'$3!\div2!=6\div2=3$ visible arrangements.')],
      'This new frame collapses the three stationary pairs to one row each; identifiers remain absent.')
def visible_copies(c,t):
    return sorted(set(permutations('C'*c+'T'*t)))
def copies_grid(c,t,counts=False):
    rows=visible_copies(c,t);d=''
    for j,ts in enumerate(rows):
        x=1.1+(j%3)*4.4;y=3-(j//3)*1.9
        d+=row(['']*len(ts),x,y,ts,positions=True,step=.55,ov='2-')
        if counts:
            d+=box(x-.35,y-.65,x+2,y+.5,'3-')
            d+=node(x+.8,y-1.03,'4 labelled versions',ov='3-',opts='font=\small')
        else:
            positions=[str(i+1) for i,v in enumerate(ts) if v=='C']
            d+=node(x+.8,y-.73,'Circle positions '+', '.join(positions),ov='2-',opts='font=\small')
    return d,rows
frame('5B. Two matching circles and two matching triangles','Predict: how many visible rows use these four copies?',
      row(['']*4,4.5,2.5,['C','C','T','T'],step=1.1),
      note='Every supplied object is placed once; circle positions determine the visible arrangement.')
d,rows=copies_grid(2,2)
frame('5B. Organize by the two circle positions','How many labelled versions belong to each visible row?',d,
      [('3-','These six rows use each possible pair of circle positions once.')],
      'Position numbers below the rows identify slots. There are no numbers above the real matching copies.')
for pattern in [('C','C','T','T'),('C','T','C','T')]:
    d=''
    for rr,cc in product(range(2),repeat=2):
        x=2+cc*6.2;y=2.8-rr*1.65
        ci=iter([1,2] if rr==0 else [2,1]); ti=iter([1,2] if cc==0 else [2,1])
        for j,t in enumerate(pattern):
            label=next(ci) if t=='C' else next(ti)
            d+=obj(t,x+j*.75,y,rf'\alt<5->{{}}{{{label}}}')
        d+=box(x-.35,y-.4,x+2.6,y+.6,'5-')
    frame('5B. Expand one visible row into labelled versions',
          'What changes across rows? What changes across columns?',d,
          [('2','Rows switch circle identifiers; columns switch triangle identifiers.'),
           ('3-4',r'$2!$ circle orders $\times2!$ triangle orders $=4$ labelled versions.'),
           ('5-','Erase identifiers: all four entries become the same visible row.')],
          'Row changes are independent of column changes. Temporary identifiers disappear at overlay 5; shapes never move.')
d,rows=copies_grid(2,2,True)
frame('5B. Every visible row has the same four-version structure','Can we use the same divisor for all six rows?',d,
      [('3-','Yes. In each box: two circle orders and two triangle orders.'),
       ('4-',r'$4!\div(2!\times2!)=24\div4=6$ visible arrangements.')],
      'Each of the six boxes refers to four labelled versions, not four distinct visible arrangements.')
frame('5C. Three matching circles and one triangle','Predict: how many visible rows use these four copies?',
      row(['']*4,4.5,2.6,['C','C','C','T'],step=1.1),
      note='Triangle position will organize the complete list; temporary identifiers are not yet present.')
d=''
for p in range(4):
    ts=['C']*4;ts[p]='T';x=.8+p*3.35
    d+=row(['']*4,x,2.5,ts,positions=True,ov=f'{p+2}-',step=.55)
    d+=node(x+.8,1.5,f'Triangle: position {p+1}',ov=f'{p+2}-',opts='font=\small,text width=2.6cm,align=center')
frame('5C. Four triangle positions','How many labelled versions hide behind each visible row?',d,
      [('6-','Four visible arrangements. Keep the triangle fixed and label only the circles.')],
      'All four visible rows are complete. Circle copies have no distinguishing numbers.')
d=''
for j,cs in enumerate(permutations([1,2,3])):
    x=1+(j//2)*4.3;y=2.8-(j%2)*1.35
    d+=row([*cs,''],x,y,['C','C','C','T'],ov=f'{j//2+2}-',step=.6)
for col in range(3):d+=box(.65+col*4.3,.95,3.1+col*4.3,3.4,'5-')
frame('5C. Fix the triangle last; order the circle labels','How many circle-label orders give this one visible row?',d,
      [('5-','Three first-circle groups; two label orders in each.'),
       ('6-',r'$3\times2\times1=3!=6$ labelled versions of this visible row.')],
      'All six label orders are shown in three columns of two. Triangle stays in the fourth position.')
d=''
for p in range(4):
    ts=['C']*4;ts[p]='T';x=.8+p*3.35
    d+=row(['']*4,x,2.7,ts,step=.55)+box(x-.3,1,x+2,3.25,'2-')
    d+=node(x+.8,1.5,'6 labelled versions',ov='2-',opts='font=\small')
frame('5C. The same six-version structure in every box','How many labelled rows altogether?',d,
      [('2-',r'Four visible arrangements; six versions each: $4\times6=24$.'),
       ('3-',r'$4!\div3!=24\div6=4$ visible arrangements.')],
      'Triangle position does not restrict the independent circle-label orders.')
for c,t in [(2,1),(2,2),(3,1)]:
    v=visible_copies(c,t)
    groups=[]
    # Labelled circles C1..Cc and triangles T1..Tt project to visible types.
    labels=[('C',i) for i in range(1,c+1)]+[('T',i) for i in range(1,t+1)]
    for pattern in v:
        groups.append([p for p in permutations(labels) if tuple(a[0] for a in p)==pattern])
    assert all(len(g)==factorial(c)*factorial(t) for g in groups)
    audit.append(dict(kind='copies',copies=[c,t],visible=v,multiplicities=[len(g) for g in groups],count=len(v)))
frame('Matching copies: name the copy counts','What do the subscripts tell us?',
      node(6.75,2.8,r'$n$: total supplied objects; $k$: number of types',ov='2-')+
      node(6.75,1.6,r'$m_1,\ m_2,\ \ldots,\ m_k$: copy counts for types $1,2,\ldots,k$',ov='3-')+
      node(6.75,.4,r'$m_1+m_2+\cdots+m_k=n$',ov='4-'),
      [('3-','A subscript identifies a type. For example, the 2 in $m_2$ means type 2.'),
       ('4-','Every copy count is a positive whole number. The counts add to the total.')],
      'Subscripts are identifiers, not multiplication. k is positive and i in m_i ranges from 1 through k.')
frame('Matching copies: the general rule','How often does each visible arrangement get counted?',
      node(6.75,2.9,r'$m_1!\times m_2!\times\cdots\times m_k!$ label orders',ov='2-')+
      node(6.75,1.3,r'$\displaystyle\text{visible rows}=\frac{n!}{m_1!m_2!\cdots m_k!}$',ov='3-'),
      [('2-','For every label order of one type, all label orders of the other types remain.'),
       ('3-','So the label orders multiply across types; divide them out of the full count.'),
       ('4-','Identical supplied copies are different from reuse: place each supplied copy once.')],
      'The dots continue through all k types. Order of positions still matters; only invisible label exchanges are removed.')

# SYNTHESIS
d=node(6.75,3.5,'What makes an outcome different?')
for x,head,body in [(2.1,'Input groups','One choice from each'),(6.75,'Membership','A group without roles'),(11.4,'Positions','A row or job assignment')]:
    d+=node(x,2.55,head,opts=r'font=\bfseries')+node(x,1.8,body,opts='font=\small')
d+=node(2.1,.6,'Multiply step counts',ov='2-',opts='font=\small')
d+=node(6.75,.6,'Distinct members: divide list orders',ov='3-',opts='font=\small,text width=3.6cm,align=center')
d+=node(11.4,.6,'All or some? Matching copies?',ov='4-',opts='font=\small,text width=3.3cm,align=center')
frame('A visual decision guide','Are we choosing from inputs, assigning positions, or choosing members?',d,
      [('4-','For positions: all distinct objects, some distinct objects, or all matching copies?')],
      'Ask the outcome question first. Membership has no jobs; arrangements keep positions.',section='Synthesis')
d=''
for i,(title,vals,ts,form,meaning) in enumerate([
 ('Input choices',[1,1],['C','T'],r'$2\times3$','2 circle groups; 3 triangle choices each'),
 ('All distinct',[1,2,3],['C']*3,r'$n!$','one fewer choice after every placement'),
 ('Some ordered',[1,2],['C']*2,r'$n!/(n-r)!$','divide by unused-tail orders')]):
    y=3.2-i*1.28
    d+=node(.1,y,title,opts='anchor=west,font=\small')+row(vals,3.1,y,ts)
    d+=node(6.5,y,form)+node(9.8,y,meaning,opts='text width=4cm,align=left,font=\small')
frame('Rule summary: what the factors count','Can you explain each factor or divisor using its picture?',d,
      [('2-','Input counts stay the same after earlier choices. Distinct-object counts decrease.')],
      'The miniature diagrams anchor rules already derived; no new contexts or formulas.')
d=membership([1,2],1.8,2.8,'1-')+node(7.9,2.8,r'$\displaystyle\binom nr=\frac{n!}{r!(n-r)!}$')
d+=node(7.9,1.85,r'$r!$: selected-member list orders; $(n-r)!$: unused-tail orders',opts='font=\small')
d+=row(['','',''],1.8,.7,['C','C','T'])+node(8.2,.7,r'$\displaystyle\frac{n!}{m_1!m_2!\cdots m_k!}$')
frame('Rule summary: what division removes','Which versions are different lists but the same actual outcome?',d,
      [('2-','Groups: remove list orders of the same members.'),
       ('3-','Matching copies: remove label orders within each type. Positions still matter.')],
      'Do not confuse member-list orders, unused-tail orders and temporary-copy-label orders.')
frame('Oral check 1: input groups','Two circles and two triangles: how many circle--triangle outcomes?',
      row([1,2],2,2.7,['C']*2,step=1)+row([1,2],8,2.7,['T']*2,step=1),
      [('2-',r'$2\times2=4$. Each circle leaves two triangle choices.')],
      'Wait for reasoning before overlay 2. Identifiers do not represent numeric values.',section='Oral checks')
frame('Oral check 2: jobs or members?','From objects 1, 2, 3: how many two-job assignments? Two-member groups?',
      row([1,2,3],5,2.6,step=1.1),
      [('2-',r'Jobs: $3\times2=6$. Switching holders changes their jobs.'),
       ('3-',r'Groups: $6\div2!=3$. Both lists of a pair name the same members.')],
      'Do not reveal the member answer together with the job answer.')
frame('Oral check 3: matching copies','Two matching circles and one triangle: how many visible rows?',
      row(['','',''],5,2.6,['C','C','T'],step=1.1),
      [('2-',r'$3!\div2!=3$. Each visible row has two circle-label versions.'),
       ('3-','Every supplied copy appears once. The triangle has three possible positions.')],
      'Ask what the divisor counts before advancing. No labels appear on the real matching copies.')

target.write_text(preamble+'\n'.join(frames)+'\n\\end{document}\n',encoding='utf-8')
for item in audit:
    if item['kind']=='product':
        assert len(item['rows'])==len(set(map(tuple,item['rows'])))==item['count']
        assert set(map(tuple,item['rows']))==set(product(*(range(1,s+1) for s in item['sizes'])))
    elif item['kind']=='ordered':
        assert len(item['rows'])==factorial(item['n'])//factorial(item['n']-item['r'])==item['count']
        assert len(set(item['rows']))==len(item['rows'])
    elif item['kind']=='groups':
        assert item['count']==factorial(item['n'])//factorial(item['r'])//factorial(item['n']-item['r'])
        assert all(len(g)==factorial(item['r']) for g in item['groups'])
        assert len({p for g in item['groups'] for p in g})==sum(map(len,item['groups']))
assert hashlib.sha256(source.read_bytes()).hexdigest()==original_hash
(Path(__file__).parent/'outcome-audit.json').write_text(json.dumps({'source_sha256':original_hash,'frames':len(frames),'examples':audit},indent=2))
print(f'Wrote {len(frames)} logical frames. Outcome sets, counts and multiplicities pass; original source unchanged.')
