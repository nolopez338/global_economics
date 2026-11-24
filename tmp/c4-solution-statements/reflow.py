from pathlib import Path
import re
p=Path('book2026-2027/grade11/term_2/1-practice_activities/G11_T2_L1_C4_practice.tex')
s=p.read_text(encoding='utf-8')
s=s.replace(r'\HLConfidence{confidence level}s',r'\HLConfidence{confidence levels}').replace(r'\HLPopulationMean{population average}s',r'\HLPopulationMean{population averages}')
# Short fragments preserve natural line breaking with the existing TikZ renderer.
def split(m):
    role,content=m.groups();parts=[];chunk=''
    for word in content.split(' '):
        if chunk and len(chunk)+1+len(word)>22:parts.append(chunk);chunk=word
        else:chunk=(chunk+' '+word).strip()
    if chunk:parts.append(chunk)
    return ' '.join('\\'+role+'{'+x+'}' for x in parts)
# Restrict the wrapping adjustments to newly copied statements.
pat=r'(\\textbf\{Problem statement with concept highlights\.\}\n)(.*?)(?=\n\n(?:\\begingroup|Report 1 gives|Let \$|The parameter is))'
s,n=re.subn(pat,lambda m:m[1]+re.sub(r'\\(HL\w+)\{([^{}]*)\}',split,m[2]),s,flags=re.S)
assert n==11,n
p.write_text(s,encoding='utf-8',newline='\n')
