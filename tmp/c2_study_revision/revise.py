from pathlib import Path
import re

root = Path(__file__).resolve().parents[2]
p = root / 'book2026-2027/grade11/term_2/2-class_activities/G11_T2_L1_C2_classroom_activity.tex'
original = p.read_bytes()
s = original.decode('utf-8').replace('\r\n', '\n')
start = s.index('\\vspace{-3mm}\n\\subsubsection*{Task 1 solution}')
end = s.index('\n\nFour of the five simulated', start)
protected = s[start:end]
s = s[:start] + 'PROTECTED_WORKED_CONTENT' + s[end:]
s = s.replace('% User override: one worked, one guided, eight independent problems (1--10).', '% User override: one worked, one guided, four independent problems (1--6).')
s = s.replace(r'\mu_{\rm sim}', r'\mu_{\mathrm{known}}').replace('Simulation population mean', 'Later established population mean')
old = 'Assume independent random observations, known $\\sigma$, and normally distributed $\\bar{x}$ (exact for normal populations). Estimate fixed, unknown $\\mu$ with $\\bar{x}$. Normal simulations use stated fixed means and the original $\\sigma$ and $n$. A simulated interval covers the fixed simulation mean when $L\\leq\\mu_{\\mathrm{known}}\\leq U$. No sample SD $s$ is provided or needed.'
new = r'''Assume independent random observations, known $\sigma$, and normally distributed $\bar{x}$ (exact for normal populations). Each problem's studies sample the same fixed population for the same target period, using the same $n$, known $\sigma$, and confidence-interval procedure at each stated level. Initially estimate unknown $\mu$ with $\bar{x}$. A later comprehensive population investigation establishes $\mu_{\mathrm{known}}$, the value of that same parameter, treated as known for this activity; repeated sample estimates alone do not establish it. No sample SD $s$ is needed.

Each subsequent study constructs its own interval $[L_i,U_i]$ around its own sample mean $\bar{x}_i$. It covers the population mean when $L_i\leq\mu_{\mathrm{known}}\leq U_i$. The nominal confidence level describes the procedure's long-run interval coverage, including the procedure used for the initial interval. It is neither the percentage of subsequent sample means nor individual observations inside the initial interval, nor a probability assigned to the fixed mean after calculation.'''
assert old in s
s = s.replace(old,new)
s = s.replace('$C$ & Confidence level &', '$C$ & Nominal confidence level &',1)
s = s.replace('$z^*$ & Critical value &', '$\\mu$ & Population mean & Initially unknown \\\\\n$\\mu_{\\mathrm{known}}$ & Later established population mean & Same parameter $\\mu$ \\\\\n$z^*$ & Critical value &',1)
s = s.replace('Use coverage and confidence as percentages in these formulas; report absolute error in percentage points. Compare coverage with the confidence level, not the interval endpoints. For tail-area calculations, use $C$ as a proportion.', 'Use coverage and nominal confidence as percentages here; $E_{\\rm abs}$ is their absolute difference in percentage points. For tail areas, use $C$ as a proportion.')
oldtask = 'Calculate observed coverage and its absolute error relative to the confidence level. Interpret the results in context and explain the difference.'
newtask = 'Compare observed interval coverage with nominal confidence.'
s = s.replace(oldtask,newtask)
s = s.replace('For each confidence level, show the covering count, denominator, coverage, and absolute error separately, and give a separate interpretation. Report error in percentage points.', r'For each level separately, count subsequent intervals satisfying $L_i\leq\mu_{\mathrm{known}}\leq U_i$; divide by the total number of intervals and multiply by $100\%$. Compare with the corresponding nominal confidence percentage used in the initial study and calculate the absolute difference in percentage points. Interpret discrepancies as finite-sample variation under the stated model: coverage need not equal nominal confidence, especially with few studies, and need not approach it monotonically as studies are added.')

contexts = [
('A random sample of 49 cycling trips', 'Each sample uses the same 95\\% procedure.', r'''An initial study of cycling trips made in a specified month used a random sample of 49 trips, with an average duration of 40 minutes, to estimate the then unknown average for all such trips. The known population standard deviation was 14 minutes, and the report used 95\% confidence.

Five subsequent independent studies each sampled 49 trips from that same month's population, using the same standard deviation and 95\% procedure. A later comprehensive investigation of all trips in that population established an average duration of 41 minutes, enabling retrospective assessment of the intervals shown.'''),
('A random sample of 100 school offices', 'the 99\\% intervals missed it 5 times.', r'''An initial study of all school offices in a district during a specified week used a random sample of 100 offices, with an average weekly printing cost of 86 thousand COP, to estimate the then unknown district average. The known population standard deviation was 32 thousand COP. Reports used 90\% and 99\% confidence.

Two hundred subsequent independent studies each sampled 100 offices from that same population for that week, using the same standard deviation and both confidence procedures. A later comprehensive population investigation established an average weekly cost of 88 thousand COP. Retrospectively, the 90\% intervals missed this value 23 times and the 99\% intervals missed it 5 times.'''),
('A random sample of 64 customers', 'Endpoints in thousand COP:', r'''An initial study of all customers at a sports centre during a specified week used a random sample of 64 customers, with an average weekly locker rental charge of 72 thousand COP, to estimate the then unknown population average. The known population standard deviation was 20 thousand COP, and the report used 95\% confidence.

Five subsequent independent studies each sampled 64 customers from that same population for that week, using the same standard deviation and 95\% procedure. A later comprehensive population investigation established an average weekly charge of 70 thousand COP, allowing retrospective assessment. The table gives interval endpoints in thousand COP.'''),
('A random sample of 144 registered households', 'the 99\\% intervals missed it 3 times.', r'''An initial study of all registered households in a district during a specified month used a random sample of 144 households, with average monthly pet-care spending of 145 thousand COP, to estimate the then unknown district average. The known population standard deviation was 42 thousand COP. Reports used 90\% and 99\% confidence.

One hundred fifty subsequent independent studies each sampled 144 households from that same population for that month, using the same standard deviation and both confidence procedures. A later comprehensive population investigation established average monthly spending of 148 thousand COP. Retrospectively, the 90\% intervals missed this value 17 times and the 99\% intervals missed it 3 times.'''),
('A random sample of 49 appointments', 'by generation order.', r'''An initial study of all appointments at a clinic during a specified month used a random sample of 49 appointments, with an average waiting time of 26 minutes, to estimate the then unknown monthly population average. The known population standard deviation was 14 minutes, and the report used 90\% confidence.

Twenty subsequent independent studies each sampled 49 appointments from that same month's population, using the same standard deviation and 90\% procedure. A later comprehensive population investigation established an average waiting time of 27 minutes. The table groups counts of intervals covering this later established mean by study order.'''),
('A random sample of 100 books', 'each sample appears once.', r'''An initial study of all books returned to a library during a specified month used a random sample of 100 books, with an average processing time of 24 minutes, to estimate the then unknown monthly population average. The known population standard deviation was 15 minutes. Reports used 90\%, 95\%, and 99\% confidence.

Two hundred fifty subsequent independent studies each sampled 100 books from that same month's population, using the same standard deviation and all three confidence procedures. A later comprehensive population investigation established an average processing time of 25 minutes. Within each study, intervals share its own sample average and are nested from narrowest at 90\% to widest at 99\%. The covering categories are mutually exclusive; each study appears once.''')]
for begin, finish, text in contexts:
    a=s.index(begin); b=s.index(finish,a)+len(finish)
    s=s[:a]+text+s[b:]
s=s.replace('Clinic waiting times in a simulation','Studies of clinic waiting times')
s=s.replace('Intervals containing the fixed simulation mean & Samples', 'Intervals covering the later established mean & Studies')
s=s.replace('Sample&$\\bar{x}$', 'Study&$\\bar{x}$').replace('Sample & Lower endpoint', 'Study & Lower endpoint').replace('Samples in order & Covering intervals', 'Studies in order & Covering intervals')
s=s.replace('For each level, complete the calculations and interpret both results for intervals estimating the fixed mean weekly printing cost of 88 thousand COP.', r'For each level separately, use $\mu_{\mathrm{known}}=88$ thousand COP to find observed interval coverage and its absolute difference from nominal confidence. Interpret both discrepancies in context.')
s=s.replace('Reflect on why the finite covering counts can vary even when the confidence levels stay fixed.', 'Explain finite-sample variation under the model. Must observed coverage equal nominal confidence or approach it monotonically as studies are added?')
oldinterp = s[s.index('Four of the five simulated'):s.index('\n\n\\clearpage',s.index('Four of the five simulated'))]
s=s.replace(oldinterp,r'''Four of the five subsequent cycling-trip intervals contain the later established population mean, $\mu_{\mathrm{known}}=41$ minutes. Observed coverage is 80\%, 15 percentage points below nominal 95\% confidence. This discrepancy reflects finite-sample variation under the model: with five intervals, coverage changes in steps of 20 percentage points and need not equal 95\%. In the long run, this procedure, also used for the initial study, produces intervals covering the same fixed population mean about 95\% of the time; observed coverage need not approach 95\% monotonically as studies are added. Confidence describes neither subsequent sample means nor individual trip durations inside the initial interval, nor a probability assigned to the fixed mean after calculation.''')
clarification = r'''Legacy-label clarification: in the preserved worked solutions below, ``simulation population mean,'' ``fixed simulation mean,'' and $\mu_{\rm sim}$ represent the later established mean $\mu_{\mathrm{known}}$ of the same cycling-trip population.'''
s=s.replace('\\stageheading{Worked example}', clarification+'\n\n\\stageheading{Worked example}')
s=s.replace('PROTECTED_WORKED_CONTENT',protected)
p.write_bytes(s.replace('\n','\r\n').encode('utf-8'))
# Preserve every byte of Task 1, Task 2 and Task 3 identification/calculations.
newbytes=p.read_bytes()
block=protected.replace('\n','\r\n').encode('utf-8')
assert block in original and block in newbytes
print('Protected worked block unchanged:',len(block),'bytes')
print('Problems:',re.findall(r'\\problemtitle\{(\d)\}',s))
