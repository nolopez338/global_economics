from pathlib import Path
import re
from fractions import Fraction as F
old=Path('tmp/context-update-c3/original.tex').read_text()
new=Path('book2026-2027/grade10/term_2/2-class_activities/G10_T2_L1_C3_classroom_activity.tex').read_text()
math=r'\$[^$]*\$|\\\[.*?\\\]'
assert re.findall(math,old,re.S)==re.findall(math,new,re.S)
assert re.findall(r'\\(?:calcblank|shortblank|responseline|workspace)\b',old)==re.findall(r'\\(?:calcblank|shortblank|responseline|workspace)\b',new)
assert old[:old.index('\\begin{document}')]==new[:new.index('\\begin{document}')]
assert re.findall(r'\\stageheading\{[^}]+\}',old)==re.findall(r'\\stageheading\{[^}]+\}',new)
assert re.findall(r'\\problemtitle\{(\d+)\}',new)==list('1234567')
assert re.findall(r'USD (\d+(?:\.\d+)?)',old)==re.findall(r'USD (\d+(?:\.\d+)?)',new)
assert not re.search(r'festival|studio|bookstall|compact.stock|expanded.stock|bicycle|micro.hydro|river flow|bulk order|leased printer|courier|depot|cold.storage|regular storage|emergency storage',new,re.I)
print('PASS: all math blocks, USD amounts, blanks, preamble, headings and seven problem numbers preserved; stale scenario terms absent.')
for prob, p, pairs in [(1,F(3,8),[(-45,105),(90,-30)]),(2,F(2,7),[(-24,72),(-54,126)]),(3,F(3,5),[(-36,84),(72,-48)]),(4,F(2,5),[(-42,98),(-70,70)]),(5,F(4,9),[(-75,150),(-75,375)]),(6,F(5,12),[(F('82.50'),F('-27.50')),(F('67.50'),-45)]),(7,F(7,20),[(96,-64),(-28,112)])]:
    print(prob, 'E probability',p, 'payoffs (complement,event)',pairs,'roots',[F(-a,b-a) for a,b in pairs], 'initial EV',[a+(b-a)*p for a,b in pairs])
