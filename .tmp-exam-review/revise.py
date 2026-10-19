from pathlib import Path
import re, math, hashlib
from fractions import Fraction as Q
p=Path('book2026-2027/grade11/term_1/3-learning_evidences')
exam=p/'G11_T1_L1_C1C2C3C4_examV2.tex'
sol=p/'G11_T1_L1_C1C2C3C4_examV2_solution.tex'
e=exam.read_text(encoding='utf-8'); s=sol.read_text(encoding='utf-8')
original_hash=hashlib.sha256(exam.read_bytes()).hexdigest()
# Balanced TeX groups, retaining the original statement text.
def group(t,start):
    depth=0
    for j in range(start,len(t)):
        if t[j] in '{}':
            if j and t[j-1]=='\\': continue
            depth += 1 if t[j]=='{' else -1
            if depth==0:return t[start+1:j],j+1
    raise ValueError(start)
statements=[]
for m in re.finditer(r'\\SubsectionBox\{\d+\.',e):
    title,end=group(e,e.index('{',m.start()))
    body,_=group(e,e.index('{',end))
    statements.append(body.replace('\\columnbreak','').strip())
assert len(statements)==12
starts=list(re.finditer(r'\\sectionScored\s*\n',s))
for i in range(11,-1,-1):
    pos=starts[i].end()
    for _ in range(3):
        _,pos=group(s,s.index('{',pos))
    opening=s.index('{',pos)
    end=s.index('\\phantomsection',opening)
    old=s[opening+1:end]
    nav=re.search(r'\\QuestionsTasks\{.*?\n\s*\}',old,re.S).group()
    if i==0:
        task='For each context, characterize the random variable and identify the appropriate probability distribution.'
    elif i==8:
        task=statements[i][statements[i].index('On average,'):]
    elif i==9:
        task=statements[i][statements[i].index('Find the average'):]
    elif i==11:
        task=statements[i][statements[i].index('From the moment'):]
    else:
        task=statements[i][statements[i].index('Determine'):]
    label=re.search(r'/\{([^}]+)\}/',nav).group(1)
    score=['5','3','4','2','3','0.5','0.5','1','1','1','2','2'][i]
    nav='\\QuestionsTasks{\n\t\t\t{'+score+'}/{'+label+'}/\n\t\t\t{'+task+' \\score{'+score+'}}\n\t\t}\n\n\t\t'
    s=s[:opening+1]+'\n\t\t'+statements[i]+'\n\n\t\t'+nav+s[end:]
s=s.replace('Grade 11 - Term 3','Grade 11 - Term 1').replace('{CX-\\sml{1}}','{CX-\\sml{2}}').replace('CX--1','CX--2')
s=s.replace('\\frac14+\\frac18','\\frac{7}{24}+\\frac{5}{24}').replace('\\frac38=0.375','\\frac12=50\\%').replace('\\frac38=37.5\\%','\\frac12=50\\%').replace('\\frac38.','\\frac12.')
s=s.replace('{0,1,3,4}{0,1,3,4}\n\t\t\t{0,0.30,0.15}', '{0,1,3,4}{0,1,3,4}\n\t\t\t{0,0.333333,0.166667}')
# Correct the completed charging plot and its vertical range.
s=s.replace('Graph{-1}{5}{0.30}', 'Graph{-1}{5}{0.38}')
s=s.replace('{(-1,0) (0,0) (0,0.30) (4,0.15) (4,0) (5,0)}%\n\t\t}', '{(-1,0) (0,0) (0,0.333333) (4,0.166667) (4,0) (5,0)}%\n\t\t}',1) if False else s
idx=s.index('\\SolvedGraph{Completed density graph}')
tail=s[idx:];tail=tail.replace('{0,0.30,0.15}','{0,0.333333,0.166667}',1).replace('(0,0.30) (4,0.15)','(0,0.333333) (4,0.166667)',1)
s=s[:idx]+tail
s=s.replace('{0,1,3,4}{0.30}','{0,1,3,4}{0.38}')
s=s.replace('=1-e^{-(0.2667)(3)}\n\t\t\t\\approx1-e^{-0.8}', '=1-e^{-(4/15)(3)}\n\t\t\t=1-e^{-4/5}')
s=s.replace('N=(0.1833)\\frac{\\text{orders}}{\\text{minute}}(12\\text{ minutes})\n\t\t\\approx \\boxed{2.2\\text{ orders}}', 'E[N(12)]=12\\left(-\\frac{\\ln(0.40)}5\\right)\n\t\t\\approx \\boxed{2.1991\\text{ orders}}')
s=s.replace('E[N(12)]\\approx2.2\\text{ orders}','E[N(12)]= -\\frac{12\\ln(0.40)}5\\approx2.1991\\text{ orders}')
s=s.replace('\\approx0.1204-0.1155\n\t\t=0.0049', '=-\\frac{\\ln(0.30)}{10}+\\frac{\\ln(0.50)}6\n\t\t\\approx0.0048727503')
s=s.replace('=\\frac{1}{0.0049}\n\t\t\\approx \\boxed{204\\text{ minutes}}', '=\\frac{1}{-\\ln(0.30)/10+\\ln(0.50)/6}\n\t\t\\approx \\boxed{205.2229\\text{ minutes}}')
s=s.replace('t\\approx204\\text{ minutes}', 't\\approx205.2229\\text{ minutes}')
s=s.replace('ln\\left(e^{-\\lambda}-0.50\\right)', '\\ln\\left(e^{-\\lambda}-0.50\\right)') if False else s
s=s.replace('\n\t\t\tln\\left','\n\t\t\t\\ln\\left')
# Preserve the one-event calculation, but explicitly state its scope and alternative.
marker='\t\tFor an exponential random variable with rate'
pos=s.index(marker,s.index('{sec:exponential-50-percent-interval}'))
note=r'''\textbf{Ambiguity in the exam.} The statement does not specify whether the
        alarm concerns only the first event measured from time zero, or any
        subsequent event in a recurring process. These give different answers.

        \textbf{Single-event interpretation (unconditional).} If an alarm that
        already occurred is missed permanently, the requested probability is
        \(P(1<T\leq1+L)=1/2\). The calculation below applies to this interpretation.

        '''
s=s[:pos]+note+s[pos:]
pos=s.index('\\vspace{-5mm}',s.index('\\boxed{\\lambda<\\ln 2}'))
s=s[:pos]+r'''For a finite waiting time, the full condition is \(0<\lambda<\ln2\)
        (with time measured in minutes). At \(\lambda=\ln2\), the probability
        approaches \(1/2\) only as \(L\to\infty\); for larger rates it never reaches \(1/2\).

        \textbf{Recurring-event interpretation.} If successive waiting times are
        independent exponentials (a homogeneous Poisson process), the wait \(W\)
        from observation to the next event satisfies
        \[
        P(W\leq L)=1-e^{-\lambda L}=\tfrac12,
        \qquad \boxed{L=\frac{\ln2}{\lambda}}.
        \]
        This holds for every \(\lambda>0\), even if events occurred in the first
        minute. The same formula holds for a single event conditional on \(T>1\),
        but that conditioning is not given in the exam. Clarification is required
        to select a unique answer.
        '''+s[pos:]
s=s.replace('The required condition is','For a single event, a finite wait requires')
pos=s.index('\\end{multicols}',s.index('For a single event, a finite wait requires'))
s=s[:pos]+r'''For a recurring Poisson process, instead:
            \[
            \boxed{L=\ln2/\lambda,\quad\lambda>0}.
            \]
            The exam does not select a unique interpretation.
        '''+s[pos:]
# Explicitly flag underdetermined model identification instead of inventing facts.
pos=s.index('\\begin{enumerate}',s.index('C1 - Distribution identification: Solutions'))
s=s[:pos]+r'''\textbf{Model qualification.} The labels below are the intended candidate
        models, rather than uniquely determined distributions. Contexts 1 and 8
        need independent trials with a common success probability; Context 5
        needs a constant failure probability; Contexts 3 and 7 need a constant
        arrival rate for a Poisson model. Peaked or monotone descriptions in
        Contexts 2, 4, 9 and 10 do not alone establish triangular, linear or
        normal densities. In particular, Context 9 does not explicitly state
        symmetry or a normal shape.

        '''+s[pos:]
s=s.replace('\\(X_9\\) is approximately symmetric and concentrated around 3.5\\%.','\\(X_9\\) measures fat content in percent, clustered around 3.5\\%;\n            a normal model is a candidate if an approximately symmetric bell shape is confirmed.')
# State support, positivity and normalization before further uses of pdfs.
s=s.replace('\\SolutionStage{4}{Probability Between 1 and 3 Minutes}',r'''The density is nonnegative on \([0,4]\), zero outside, and
        \(\int_0^4(8-x)/24\,dx=1\); its units are inverse minutes.
        \SolutionStage{4}{Probability Between 1 and 3 Minutes}''')
s=s.replace('\\SolutionStage{4}{Probability Between \\$2 and \\$6 Million}',r'''Both branches are nonnegative on their support, and their areas are
        \(5/6+1/6=1\). Density units are inverse million dollars.
        \SolutionStage{4}{Probability Between \$2 and \$6 Million}''')
s=s.replace('\\SolutionStage{2}{Probability Between 8 p.m. and 6 a.m.}',r'''Here \(f(t)=0\) outside \([0,24)\), and
        \(\int_0^{24}(1/24)\,dt=1\); density units are inverse hours.
        \SolutionStage{2}{Probability Between 8 p.m. and 6 a.m.}''')
s=s.replace('\\SolutionStage{1}{Probability Within',r'''For the angle in radians, \(f_A(a)=1/(2\pi)\) on \([0,2\pi)\)
        and zero elsewhere; its integral is one. The degree-labelled plot below
        uses radian coordinates, so its density height is also \(1/(2\pi)\).
        \SolutionStage{1}{Probability Within''',1)
s=s.replace('f(\\theta)=\\frac{1}{360^\\circ}','f(\\theta)=\\frac{1}{2\\pi}\\;\\text{rad}^{-1}')
s=s.replace('\\approx1.67\\%.','\\approx0.0167.' )
s=s.replace('\\text{ by }\\frac{1}{60}\\approx1.67\\%.','\\text{ by }\\frac{1}{60}\\text{ (1.67 percentage points)}.')
s=s.replace('\\boxed{\\frac1{60}\\approx1.67\\%}','\\boxed{\\frac1{60}\\text{ (1.67 percentage points)}}')
pos=s.index('% C4 - Find Probability')
s=s[:pos]+s[pos:].replace('\\newpage',r'''\newpage
    \noindent\textbf{Exponential model check (Problems 6--12).}
    For \(\lambda>0\), \(f_T(t)=\lambda e^{-\lambda t}\) on \([0,\infty)\)
    and zero otherwise is nonnegative, with
    \(\int_0^\infty\lambda e^{-\lambda t}\,dt=1\).
    Rates below are per minute and waiting times are in minutes.
    Problems 6--8 supply average rates but do not explicitly give a constant
    hazard or independent arrivals; their answers use the intended exponential
    model. Expected counts in Problem 9 use the standard homogeneous Poisson
    interpretation of independent exponential interarrival times.
''',1)
sol.write_text(s,encoding='utf-8')
assert hashlib.sha256(exam.read_bytes()).hexdigest()==original_hash
norm=lambda x:re.sub(r'\s+',' ',x).strip()
for i,body in enumerate(statements):
    assert norm(body) in norm(s),f'Statement {i+1}'
assert Q(7,24)+Q(5,24)==Q(1,2)
assert Q(5,6)+Q(1,6)==1
assert 1-Q(1,30)-Q(1,6)==Q(4,5)
print('All 12 exam statements matched; exam SHA256:',original_hash)
print('P2=',Q(1,2),'P3=',Q(4,5),'P4=',Q(10,24),'P5=',Q(1,10)-Q(1,12))
print('P6,7,8=',math.exp(-5/4),1-math.exp(-4/5),math.exp(-1)-math.exp(-2))
print('P9=',-12*math.log(.4)/5,'P10=',-math.log(.25)/10)
print('P11=',1/(-math.log(.3)/10+math.log(.5)/6))
for rate in (.1,.5):
    L=-math.log(math.exp(-rate)-.5)/rate-1
    assert abs(math.exp(-rate)-math.exp(-rate*(1+L))-.5)<1e-12
    assert abs(1-math.exp(-rate*(math.log(2)/rate))-.5)<1e-12
print('Both P12 interpretations cross-checked.')
