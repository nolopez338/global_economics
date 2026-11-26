from itertools import permutations, combinations, product
from math import factorial, comb
from collections import Counter
from pathlib import Path
import re

outfits=list(product(range(1,3),range(1,4)))
assert len(set(outfits))==6
rows=[''.join(p) for p in permutations('ABC')]
assert rows==['ABC','ACB','BAC','BCA','CAB','CBA']
jobs=[''.join(p) for p in permutations('ABCD',2)]
assert len(jobs)==12 and all(a!=b for a,b in jobs)
teams=Counter(''.join(sorted(p)) for p in jobs)
assert len(teams)==6 and set(teams.values())=={2}
assert set(teams)==set(''.join(c) for c in combinations('ABCD',2))
assert len(rows)==factorial(3)==6
for cards,expected,multiplicity in [('AAB',3,2),('AABB',6,4),('ABB',3,2)]:
    counts=Counter(''.join(p) for p in permutations(cards))
    assert len(counts)==expected and set(counts.values())=={multiplicity}
assert set(''.join(p) for p in permutations('AABB'))=={'AABB','ABAB','ABBA','BAAB','BABA','BBAA'}
for n in range(7):
    for r in range(n+1):
        assert len(list(permutations(range(n),r)))==factorial(n)//factorial(n-r)
        assert len(list(combinations(range(n),r)))==comb(n,r)==factorial(n)//(factorial(r)*factorial(n-r))
p=Path(__file__).parent
tex=(p/'lesson.tex').read_text()
assert len(re.findall(r'\\begin\{frame\}',tex))==26
assert not re.search(r'\\(?:input|include|includegraphics)\b',tex)
nav=(p/'build/lesson.nav').read_text()
frames=re.findall(r'\\beamer@framepages\s*\{(\d+)\}\{(\d+)\}',nav)
assert len(frames)==26 and int(frames[-1][1])==78
log=(p/'build/lesson.log').read_text()
assert not re.search(r'Overfull|Underfull|Missing character|LaTeX Warning|undefined references',log)
print('PASS: exhaustive counts, ordered pairs, equal-size duplicate groups, factorial formulas (0 through 6), standalone source, 26 frames / 78 pages, clean compile log.')
gray=tex.replace(r'\begin{document}',r'''\definecolor{GEInk}{gray}{0}
\definecolor{GETeal}{gray}{0}
\definecolor{GEFooter}{gray}{.94}
\begin{document}''')
(p/'gray.tex').write_text(gray)
