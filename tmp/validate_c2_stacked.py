from pathlib import Path
from fractions import Fraction
import subprocess, re
p = Path('book2026-2027/grade10/term_2/1-practice_activities/G10_T2_L1_C2_practice_activity.tex')
new = p.read_text(encoding='utf-8')
old = subprocess.check_output(['git','show','HEAD:'+p.as_posix()]).decode('utf-8')
def sections(s):
    return s.split(r'\subsection*{Connecting the PMF and CDF}')[1:]
assert len(sections(new)) == 12
total = 0
for i,(a,b) in enumerate(zip(sections(old),sections(new)),1):
    a = a.split(r'\cTwoConnectionReading')[0]
    b = b.split(r'\cTwoConnectionReading')[0]
    # Every original plotted step, endpoint set, and annotation is preserved.
    for line in a.splitlines():
        if line.startswith((r'\addplot[cTwoStep',r'\addplot[cTwoIncluded',r'\addplot[cTwoExcluded',r'\node',r'\draw')):
            assert line in b, (i,line)
    masses = re.findall(r'\\cTwoMass\{([^}]+)\}\{([^}]+)\}',a)
    shadows = re.findall(r'\\cTwoPhantom\{([^}]+)\}\{([^}]+)\}\{([^}]+)\}',b)
    assert masses == re.findall(r'\\cTwoMass\{([^}]+)\}\{([^}]+)\}',b)
    assert [x for x,_ in masses] == re.findall(r'\\cTwoCorrespondence\{([^}]+)\}',b)
    running = Fraction(0)
    for (x,p),(sx,sp,f) in zip(masses,shadows):
        assert x == sx and Fraction(p) == Fraction(sp) and Fraction(f) == running
        running += Fraction(p)
    assert running == (Fraction(673,1024) if i==11 else 1)
    total += len(masses)
    print(f'Section {i}: {len(masses)} exact masses, shadows and arrows; cumulative heights correct.')
# Outside connection sections and local helper preamble, all content is unchanged.
def outside(s):
    s = s[s.index(r'\begin{document}'):]
    return re.sub(r'\\subsection\*\{Connecting the PMF and CDF\}.*?\\cTwoConnectionReading', '', s, flags=re.S)
assert outside(old) == outside(new)
assert not re.search(r'\bPDF\b|overlay|lies behind the blue PMF',new)
print(f'PASS: {total} arrows across 12 pairs; unrelated content and Task 1/2 graphs unchanged.')
