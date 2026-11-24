from pathlib import Path
p=Path('book2026-2027/grade11/term_2/1-practice_activities/G11_T2_L1_C4_practice.tex')
s=p.read_text(encoding='utf-8')
s=s.replace(r'\par\noindent\textbf{Report 2: midpoint and half-width first.}',r'\clearpage'+'\n'+r'\par\noindent\textbf{Report 2: midpoint and half-width first.}')
for heading in ['C4 -- Coordinate all three problem types','C4 -- Test what the reported precision supports']:
 s=s.replace('\\subsubsection*{'+heading+'}', '\\clearpage\n\\subsubsection*{'+heading+'}')
p.write_text(s,encoding='utf-8',newline='\n')
v=Path('tmp/c4-solution-statements/verify.py')
t=v.read_text(encoding='utf-8').replace("assert restored==old,'Existing source changed'", "restored=restored.replace('\\\\clearpage\\n\\\\par\\\\noindent\\\\textbf{Report 2:', '\\\\par\\\\noindent\\\\textbf{Report 2:')\nfor heading in ['C4 -- Coordinate all three problem types','C4 -- Test what the reported precision supports']:\n restored=restored.replace('\\\\clearpage\\n\\\\subsubsection*{'+heading+'}', '\\\\subsubsection*{'+heading+'}')\nassert restored==old,'Existing source changed'")
v.write_text(t,encoding='utf-8')
