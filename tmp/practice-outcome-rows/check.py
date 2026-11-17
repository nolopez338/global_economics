from pathlib import Path
import re,difflib
b=Path('tmp/practice-outcome-rows/before.tex').read_text(encoding='utf-8'); a=Path('book2026-2027/grade10/term_2/1-practice_activities/G10_T2_L1_C2_practice_activity.tex').read_text(encoding='utf-8')
# Remove the modified three-block PMF rows: everything else must be identical.
def strip(s):
 for key in ['fees','bike','recycling','claims','notebooks','investment','refund','prize','maintenance','calls','reserve']:
  start=s.index('\\stage{'+key+'}{1}'); end=s.index('\\stage{'+key+'}{2}',start)
  part=s[start:end]; left=part.index(r'\par\noindent\begin{minipage}'); right=part.index(r'\end{minipage}\par',left)+len(r'\end{minipage}\par')
  part=part[:left]+'<PMF ROW>'+part[right:]; s=s[:start]+part+s[end:]
 return s
assert strip(a)==strip(b), 'Change outside PMF rows'
for key in ['fees','bike','recycling','claims','notebooks','investment','refund','prize','maintenance','calls','reserve']:
 def pmf(s):
  start=s.index('\\stage{'+key+'}{1}'); end=s.index('\\stage{'+key+'}{2}',start)
  return re.search(r'\\GTenPMFGraph\[.*?\](\{[^}]*\}\{[^}]*\})',s[start:end]).group(1)
 assert pmf(a)==pmf(b),key
print('PASS: all edits confined to 11 PMF rows; every PMF coordinate and probability list is unchanged.')
Path('tmp/practice-outcome-rows/edit.diff').write_text(''.join(difflib.unified_diff(b.splitlines(True),a.splitlines(True))),encoding='utf-8')
