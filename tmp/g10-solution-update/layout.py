from pathlib import Path
p=Path('book2026-2027/grade10/term_2/4-learning_evidences/G10_T2_L1_C1C2_exam_solution.tex');s=p.read_text()
a=s.index('\\section*{Highlight legend}');b=s.index('\\sectionScored{Online',a)
legend=s[a:b].replace('\\clearpage','').strip()
s=s[:a]+r'\clearpage'+'\n'+legend+'\n\n'+s[b:]
s=s.replace('\\subsection*{Task',r'\Needspace{8\baselineskip}'+'\n'+r'\subsection*{Task')
p.write_text(s)
Path('tmp/g10-solution-update/disabled.tex').write_text(s.replace('% \\GTenHighlightsfalse % Uncomment','\\GTenHighlightsfalse % Uncomment'))
