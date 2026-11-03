from pathlib import Path
p=Path('book2026-2027/grade10/term_2/1-practice_activities/G10_T2_L1_C1_practice_activity.tex')
s=p.read_text()
s=s.replace(r'$Y=5X$',r'$\GTenHLSecond{Y}=5\GTenHLValue{X}$')
s=s.replace(r'Let $\GTenHLThird{Z}$ equal 1 if',r'Let $\GTenHLThird{Z}$ equal \GTenHLThird{1} if',1)
s=s.replace('and 0 otherwise. Then',r'and \GTenHLThird{0} otherwise. Then',1)
lookup=r'''% Value-to-mass lookup before the normalization sum.
\[
p_X(\GTenHLValue{0})=\GTenHLProbability{0.1},\qquad
p_X(\GTenHLValue{1})=\GTenHLProbability{0.5},\qquad
p_X(\GTenHLValue{2})=\GTenHLProbability{0.4}.
\]
'''
needle='For this support,\n'
assert s.count(needle)==1
s=s.replace(needle,needle+lookup)
p.write_text(s)
