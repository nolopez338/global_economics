from pathlib import Path
p=Path('book2026-2027/grade11/term_2/1-practice_activities/G11_T2_L2_C6_practice.tex')
s=p.read_text(encoding='utf-8-sig')
# Keep each question-type framing with its initial worked mean problem.
for t in (1,2,3):
 lab={1:'prob:t1-mean',2:'prob:c6-1',3:'prob:t3-mean'}[t]
 pos=s.index('\\label{'+lab+'}')
 start=s.rfind('\\clearpage',0,pos)
 s=s[:start]+s[start:].replace('\\clearpage\n','',1)
for title in ('Type 2: minimum','Type 3: minimum','Type 4: minimum'):
 s=s.replace('\\subsection{'+title,'\\clearpage\n\\subsection{'+title)
# A deliberate page for Type 4 framing; avoid a short spill of its explanation.
s=s.replace('\\subsection{Type 4:', '\\subsection{Type 4:')
# Advanced: separate the two-constraint solution from the planning comparison.
a=s.index('\\subsection{Coordinate constraints')
b=s.index('\\subsubsection*{Solution: two simultaneous constraints}',a)
header=r'''\subsection{Coordinate precision and confidence}\label{prob:advanced-design}
\QuestionsTasks[sec:advanced]{{6}/{sol:advanced-design}/{A cargo study has known $\sigma=12$ minutes, requires $SE\le1.5$ minutes and at least 95\% confidence with a fixed margin cap of 2 minutes. Under the same normal model, find the minimum $n$ satisfying both constraints. Use $N=100{,}000$.}}
'''
s=s[:a]+header+s[b:]
a=s.index('\\subsubsection*{Solution: pilot versus conservative planning}')
header=r'''\clearpage
\subsection{Compare planning assumptions and justify conclusions}\label{prob:advanced-planning}
\QuestionsTasks[sec:advanced]{
{6}/{sol:advanced-pilot}/{For a random energy-eligibility survey from $N=100{,}000$ households, fix 95\% confidence and a margin cap of 4 percentage points. Compare the pilot choice $p_0=0.20$ with conservative $p_0=0.50$. Explain what each plan supports and what must be checked later.},
{6}/{sol:advanced-missing}/{An analyst requests at least 95\% confidence but specifies no SE, margin or width cap. Explain why this does not determine a minimum sample size for precision planning.}}
'''
s=s[:a]+header+s[a:]
a=s.index('\\label{prob:advanced-planning}')
s=s[:a]+s[a:].replace('\\secInicio[prob:advanced-design]','\\secInicio[prob:advanced-planning]')
s=s.replace('\\SectionProblemLink{prob:advanced-design}{Coordinate constraints and planning assumptions}',r'\SectionProblemLink{prob:advanced-design}{Coordinate precision and confidence}\\'+'\n'+r'\SectionProblemLink{prob:advanced-planning}{Compare planning assumptions and justify conclusions}')
# Apply existing coordinated roles to numerical model components in worked solutions.
labels=['prob:t1-mean','prob:t1-prop','prob:c6-1','prob:c6-2','prob:t3-mean','prob:t3-prop','prob:t4-mean','prob:t4-prop']
for i,lab in enumerate(labels):
 start=s.index('\\subsubsection*{Worked solution (C6)}',s.index('\\label{'+lab+'}'))
 end=s.index('\\secInicio',start)
 block=s[start:end]
 role=['HLStandardError']*2+['HLMarginOfError']*2+['HLIntervalWidth']*2+['HLMarginOfError']*2
 caps=['1.5','0.025','3','0.04','5','0.06','2','0.03']
 block=block.replace('z^*',r'\HLCriticalValue{z^*}').replace('z_0',r'\HLCriticalValue{z_0}')
 block=block.replace('\\le '+caps[i],'\\le \\'+role[i]+'{'+caps[i]+'}')
 if i%2==0:
  sig='15' if i==4 else '12'
  block=block.replace('\\frac{'+sig+'}',r'\frac{\HLPopulationSD{'+sig+'}}').replace('}'+sig+'}',r'}\HLPopulationSD{'+sig+'}}')
 else:
  pv='0.50' if i==5 else '0.30' if i==7 else '0.20'
  block=block.replace(pv+'(',r'\HLModelControl{'+pv+'}(')
 s=s[:start]+block+s[end:]
p.write_text(s,encoding='utf-8')

