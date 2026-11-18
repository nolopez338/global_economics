from pathlib import Path
p=Path('book2026-2027/grade11/term_2/2-class_activities/G11_T2_L1_C2_classroom_activity.tex')
s=p.read_text(encoding='utf-8')
a=s.index('Four of five subsequent'); b=s.index('\n\n\\clearpage',a)
s=s[:a]+'\\begin{samepage}\n'+s[a:b]+'\n\\end{samepage}'+s[b:]
s=s.replace('\\clearpage\n\n\\stageheading{Guided Example}', '\\stageheading{Guided Example}')
s=s.replace('\\stageheading{Independent Practice}', '\\clearpage\n\\stageheading{Independent Practice}')
a=s.index('\\stageheading{Guided Example}')
s=s[:a]+s[a:].replace('\\task{2}{Calculate MoE and state the interval.}', '\\Needspace{20\\baselineskip}\n\\task{2}{Calculate MoE and state the interval.}',1)
p.write_bytes(s.replace('\n','\r\n').encode('utf-8'))
