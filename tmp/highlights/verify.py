from pathlib import Path
import re,difflib
base=Path('tmp/highlights')
s=Path('book2026-2027/grade10/term_2/1-practice_activities/G10_T2_L1_C1_practice_activity.tex').read_text()
o=(base/'original.tex').read_text()
# Remove only wrappers using a balanced brace scan.
def strip(s):
 pat=re.compile(r'\\GTenHL(?:Value|Second|Third|Outcome|Probability|Parameter)\{')
 while (m:=pat.search(s)):
  j=m.end(); depth=1
  while depth:
   if s[j]=='{':depth+=1
   elif s[j]=='}':depth-=1
   j+=1
  s=s[:m.start()]+s[m.end():j-1]+s[j:]
 return s
s=__import__('re').sub(r'% Value-to-mass lookup before the normalization sum\.\n\\\[.*?\\\]\n','',s,flags=__import__('re').S)
plain=strip(s).replace('\\input{graphs/highlights.tex}\n','').replace('\\GTenHighlightLegend\n\n','')
plain=re.sub(r'\\textit\{Markers here:\}[^\n]*\n','',plain)
# Cosmetic TeX grouping of a highlighted PMF subscript is equivalent.
plain=re.sub(r'p_\{([XYZ])\}',r'p_\1',plain)
assert plain==o, '\n'.join(difflib.unified_diff(o.splitlines(),plain.splitlines()))
graph=lambda t:[l for l in t.splitlines() if l.startswith('\\GTen') and 'Graph[' in l]
assert graph(s)==graph(o),'Graph call changed'
print('Verified: every original content character restored by unwrapping; all graph calls unchanged.')
