from pathlib import Path
p=Path('book2026-2027/grade11/term_2/2-class_activities/G11_T2_L1_C2_classroom_activity.tex')
s=p.read_text(encoding='utf-8')
s=s.replace('\\stageheading{Worked example}\n\\vspace{-4mm}', '\\stageheading{Worked example}\n\\vspace{-7mm}')
a=s.index('\\begin{samepage}'); b=s.index('\\end{samepage}',a)+len('\\end{samepage}')
s=s[:a]+r'''Four of five subsequent intervals cover $\mu_{\mathrm{known}}=41$ minutes, the later established population mean: 80\%, 15 percentage points below nominal 95\%. This finite-sample discrepancy is consistent with the model. Nominal confidence describes the initial procedure's long-run interval coverage; observed coverage need not match it or approach it monotonically.'''+s[b:]
s=s.replace('\\stageheading{Guided Example}', '\\clearpage\n\\stageheading{Guided Example}')
p.write_bytes(s.replace('\n','\r\n').encode('utf-8'))
