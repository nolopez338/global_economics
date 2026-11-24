from pathlib import Path
import re
p=Path('book2026-2027/grade11/term_2/1-practice_activities/G11_T2_L1_C4_practice.tex')
s=p.read_text(encoding='utf-8')
pat=r'(\\textbf\{Problem statement with concept highlights\.\}\n)(.*?)(?=\n\n(?:\\begingroup|Report 1 gives|Let \$|The parameter is))'
s,n=re.subn(pat,lambda m:m[1]+'\\begingroup\\raggedright\n'+m[2]+'\n\\par\\endgroup',s,flags=re.S)
assert n==11
p.write_text(s,encoding='utf-8',newline='\n')
