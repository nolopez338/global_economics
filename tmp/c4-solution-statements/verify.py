from pathlib import Path
import re,json
p=Path('book2026-2027/grade11/term_2/1-practice_activities/G11_T2_L1_C4_practice.tex')
s=p.read_text(encoding='utf-8');old=Path('tmp/c4-solution-statements/original.tex').read_text(encoding='utf-8')
pat=r'\\textbf\{Problem statement with concept highlights\.\}\n\\begingroup\\raggedright\n(.*?)\n\\par\\endgroup\n\n'
blocks=list(re.finditer(pat,s,re.S));assert len(blocks)==11
restored=re.sub(pat,'',s,flags=re.S);restored=restored.replace('\\clearpage\n\\par\\noindent\\textbf{Report 2:', '\\par\\noindent\\textbf{Report 2:')
for heading in ['C4 -- Coordinate all three problem types','C4 -- Test what the reported precision supports']:
 restored=restored.replace('\\clearpage\n\\subsubsection*{'+heading+'}', '\\subsubsection*{'+heading+'}')
assert restored==old,'Existing source changed'
def arg(text,start):
 d=1
 for i in range(start,len(text)):
  if text[i]=='{':d+=1
  if text[i]=='}':
   d-=1
   if d==0:return text[start:i]
for m,b in zip(re.finditer(r'\{4\}/\{(sol:c4-[^}]+)\}/\{',old),blocks):
 label=m[1];prob=label.replace('sol:','prob:');prob=prob if 'advanced' in label else prob[:-2]
 context=re.search(r'\\subsection\{[^\n]+\\label\{'+re.escape(prob)+r'\}\n([^\n]+)',old)[1]
 expected=context+'\n\n'+arg(old,m.end())
 actual=re.sub(r'\\HL\w+\{([^{}]*)\}',r'\1',b[1])
 assert actual==expected,label
 assert s[:b.start()].endswith('\\label{'+label+'}\n'),label
 assert not re.search(r'\\HLConfidence\{[^}]*significance',b[1])
 print(label+': exact wording, full context, immediate placement verified')
Path('tmp/c4-solution-statements/disabled.tex').write_text(s.replace('% \\GTenHighlightsfalse %','\\GTenHighlightsfalse %'),encoding='utf-8')
