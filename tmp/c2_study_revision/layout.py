from pathlib import Path
p=Path('book2026-2027/grade11/term_2/2-class_activities/G11_T2_L1_C2_classroom_activity.tex')
s=p.read_text(encoding='utf-8')
s=s.replace('In independent practice and the worked example, use four columns:', 'In independent practice, use four columns:')
s=s.replace('In the guided example, combine the last two columns as', 'In both examples, combine the last two columns as')
# Optional width applies only to guided confidence blocks; default worked formatting is unchanged.
s=s.replace(r'\newcommand{\GuidedEstimationTable}[1]{%',r'\newcommand{\GuidedEstimationTable}[2][.1\linewidth]{%')
a=s.index(r'\newcommand{\GuidedEstimationTable}')
b=s.index(r'\newcommand{\GuidedConfidenceTable}',a)
chunk=s[a:b].replace('p{.1\\linewidth}', 'p{#1}').replace('        #1\n','        #2\n')
s=s[:a]+chunk+s[b:]
s=s.replace('    \\GuidedEstimationTable{\n        \\multicolumn', '    \\GuidedEstimationTable[.14\\linewidth]{\n        \\multicolumn')
a=s.index('Legacy-label clarification:');b=s.index('\n\n\\stageheading{Worked example}',a)
s=s[:a]+r'Legacy labels in the preserved solutions refer to $\mu_{\mathrm{known}}$, the later established mean of the same population.'+s[b:]
s=s.replace('\\stageheading{Worked example}\n\\vspace{-7mm}', '\\clearpage\n\\stageheading{Worked example}')
s=s.replace('\\begin{minipage}[t]{0.60\\linewidth}', '\\begin{minipage}[t]{0.68\\linewidth}',1)
s=s.replace('\\begin{minipage}[t]{0.38\\linewidth}', '\\begin{minipage}[t]{0.30\\linewidth}',1)
a=s.index('An initial study of cycling trips');b=s.index('\n\\end{minipage}',a)
s=s[:a]+r'''An initial study estimated the then unknown average duration of all cycling trips in a specified month. A random sample of 49 trips averaged 40 minutes; the known population standard deviation was 14 minutes. The report used 95\% confidence.

Five subsequent independent studies sampled the same month's population, each using 49 trips, the same standard deviation and 95\% procedure. A later comprehensive population investigation established an average of 41 minutes, enabling retrospective interval assessment.'''+s[b:]
a=s.index('Four of the five subsequent');b=s.index('\n\n\\clearpage',a)
s=s[:a]+r'''Four of five subsequent intervals cover the later established population mean, $\mu_{\mathrm{known}}=41$ minutes: observed coverage is 80\%, 15 percentage points below nominal 95\% confidence. This is finite-sample variation under the model; five intervals give coverage in 20-point steps. The procedure used in the initial study covers the same fixed mean about 95\% of the time in the long run. Observed coverage need not equal or approach 95\% monotonically. Confidence describes neither subsequent sample means nor individual observations inside the initial interval, nor a probability assigned to the fixed mean after calculation.'''+s[b:]
p.write_bytes(s.replace('\n','\r\n').encode('utf-8'))
