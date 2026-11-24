from pathlib import Path
import re
p=Path('book2026-2027/grade10/term_2/1-practice_activities/G10_T2_L1_C4_practice_activity.tex')
s=p.read_text(encoding='utf-8')
for heading in ['Introductory example 2: a fixed set of payment reminders','Practice procedure','Loan defaults','On-time invoices','Insurance claims at most one','At least one business sale','Supplier defects and a failed assumption']:
    s=s.replace('\\subsection{'+heading+'}', '\\clearpage\n\\subsection{'+heading+'}')
s=s.replace('Both monetary endpoints are included.', 'Both monetary endpoints are included.\n\n\\textbf{Follow-up: a changed fee.} If each late payment costs 10 USD instead, the same 10--20 USD band means $1\\leq X\\leq2$. The count model remains $X\\sim\\operatorname{Bin}(10,0.2)$, but the event changes:\n\\[P(1\\leq X\\leq2)=\\binom{10}{1}(0.2)(0.8)^9+\\binom{10}{2}(0.2)^2(0.8)^8\\approx \\GTenHLProbability{0.5704}.\\]\nThe probability falls from $\\GTenHLProbability{0.5914}$ to $\\GTenHLProbability{0.5704}$ for this particular band; doubling the fee does not double the probability.')
s=s.replace('Explain why this is also the event $10\\leq Y\\leq20$ USD.', 'Explain why this is also the event $10\\leq Y\\leq20$ USD. Then change the fee to 10 USD per late payment: find the probability of the same monetary band and explain what changes in your model or event.')
s=s.replace('\\subsection*{Key ideas and common errors}', '\\secInicio[prob:defects][sec:t2-c4-advanced]\n\\subsection*{Key ideas and common errors}')
s=s.replace('\\secInicio\n\\secInicio[prob:defects][sec:t2-c4-advanced]', '\\secInicio')
# Carry roles through numerical substitutions in cumulative worked calculations.
for n,pval,q in [(6,'0.4','0.6'),(6,'0.05','0.95'),(8,'0.25','0.75'),(10,'0.2','0.8'),(7,'0.15','0.85')]:
    s=s.replace('\\binom{'+str(n)+'}j('+pval+')^j('+q+')^{'+str(n)+'-j}', '\\binom{\\HLObservationCount{'+str(n)+'}}j(\\HLSuccessProbability{'+pval+'})^j(\\HLComplementProbability{'+q+'})^{'+str(n)+'-j}')
p.write_text(s,encoding='utf-8')
off=s.replace('% \\GTenHighlightsfalse % Uncomment', '\\GTenHighlightsfalse % Uncomment')
Path('tmp/g10-c4-update/off.tex').write_text(off,encoding='utf-8')
