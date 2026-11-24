from pathlib import Path
import re

root = Path(__file__).resolve().parents[2]
path = root / 'book2026-2027/grade10/term_2/1-practice_activities/G10_T2_L1_C4_practice_activity.tex'
s = path.read_text(encoding='utf-8')
Path(__file__).with_name('before.tex').write_text(s, encoding='utf-8')
s = s.replace('\\section*{Evaluated criterion}\n\\textbf{C4:}', '\\section*{Evaluated criteria}\n\\begin{description}\n\\item[\\textbf{C4}]')
s = s.replace('\\section{Introduction}', r'''\end{description}
\textbf{How to practise.} Attempt each C4 task before following its solution link. Define success, check all four binomial conditions and translate the event before calculating. Keep exact intermediate values and round final probabilities to four decimal places. Use the arrows to return to the contents, problem or problem group.
\clearpage
\section{Introduction}''', 1)
s = s.replace('\\subsection{A fixed set of opportunities}', '\\subsection{Introductory example 1: a fixed set of offers}\\label{ex:intro-one}')
s = s.replace('probability $p$.', 'probability $\\HLSuccessProbability{p}=\\HLSuccessProbability{0.3}$.', 1)
s = s.replace('\\subsection{Four conditions}', r'''\subsection{Introductory example 2: a fixed set of payment reminders}\label{ex:intro-two}
A business sends \HLObservationCount{three reminders}, each concerning a different invoice. Assume independent results and constant probability $\HLSuccessProbability{p}=\HLSuccessProbability{0.5}$ that each invoice is paid by Friday. Let $\GTenHLValue{X}$ count paid invoices, with support $\GTenHLValue{\{0,1,2,3\}}$ invoices. Exactly $\GTenHLValue{k}=\GTenHLValue{2}$ payments can appear in three orders: SSF, SFS and FSS. Here S means paid by Friday and F means not paid by Friday. Each order has probability $\HLSuccessProbability{0.5}\cdot\HLSuccessProbability{0.5}\cdot\HLComplementProbability{0.5}$; adding the three disjoint orders gives $\GTenHLProbability{0.375}$. This is a probability, not a dollar amount.
\textbf{Quick check.} If the firm stops sending reminders as soon as an invoice is paid, is the number of reminders fixed? \emph{Suggested answer:} No; a fixed-trial binomial count no longer describes that stopping rule.

\subsection{Four conditions}''')
start = s.index('\\section{Notation reference and practice procedure}')
end = s.index('\\Needspace{19\\baselineskip}', start)
procedure = s[start:end]
procedure = procedure[procedure.index('\\begin{enumerate}'):]
table = r'''\clearpage
\section{Notation Reference and Practice Procedure}\label{sec:notation-and-procedure}
\subsection{Notation reference}\label{tab:notation-reference}
\begingroup
\setlength{\tabcolsep}{4pt}
\begin{longtable}{@{}>{\raggedright\arraybackslash}p{.16\linewidth}>{\raggedright\arraybackslash}p{.18\linewidth}>{\raggedright\arraybackslash}p{.27\linewidth}>{\raggedright\arraybackslash}p{\dimexpr.39\linewidth-6\tabcolsep\relax}@{}}
\toprule
\textbf{Symbol or notation} & \textbf{Concept} & \textbf{Definition} & \textbf{Meaning in the introductory examples} \\
\midrule\endfirsthead
\toprule
\textbf{Symbol or notation} & \textbf{Concept} & \textbf{Definition} & \textbf{Meaning in the introductory examples} \\
\midrule\endhead
$\GTenHLValue{X}$; $\GTenHLValue{k}$ & \GTenHLValue{Success count} & $X$ is the random count; $k$ is a possible value, measured in successes. & \textbullet\ \hyperref[ex:intro-one]{Example 1}: purchases.\par\textbullet\ \hyperref[ex:intro-two]{Example 2}: paid invoices; $\GTenHLValue{k}=\GTenHLValue{2}$ specifies exactly two. \\[4pt]
$\GTenHLValue{\{0,\ldots,n\}}$ & \GTenHLValue{Support} & All possible integer success counts, from zero to the fixed trial count. & \textbullet\ \hyperref[ex:intro-one]{Example 1}: $\GTenHLValue{\{0,1,2,3,4\}}$ purchases.\par\textbullet\ \hyperref[ex:intro-two]{Example 2}: $\GTenHLValue{\{0,1,2,3\}}$ paid invoices. \\[4pt]
$\HLObservationCount{n}$ & \HLObservationCount{Trial count} & Number of trials fixed before observing outcomes. & \textbullet\ \hyperref[ex:intro-one]{Example 1}: $\HLObservationCount{4}$ offers.\par\textbullet\ \hyperref[ex:intro-two]{Example 2}: $\HLObservationCount{3}$ reminders. \\[4pt]
$\HLSuccessProbability{p}$ & \HLSuccessProbability{Success probability} & Constant probability of success on one trial; $0\leq p\leq1$. & \textbullet\ \hyperref[ex:intro-one]{Example 1}: purchase probability $\HLSuccessProbability{0.3}$.\par\textbullet\ \hyperref[ex:intro-two]{Example 2}: payment probability $\HLSuccessProbability{0.5}$. \\[4pt]
$\HLComplementProbability{1-p}$ & \HLComplementProbability{Failure probability} & Probability of the other binary outcome. & \textbullet\ \hyperref[ex:intro-one]{Example 1}: no purchase, $\HLComplementProbability{0.7}$.\par\textbullet\ \hyperref[ex:intro-two]{Example 2}: unpaid by Friday, $\HLComplementProbability{0.5}$. \\[4pt]
$\binom nk$; $n!$ & Arrangements; factorial & $\binom nk=n!/[k!(n-k)!]$ counts success-position choices. $n!$ multiplies integers from 1 to $n$; $0!=1$. & \textbullet\ \hyperref[ex:intro-two]{Example 2}: $\binom32=3$ possible orders with two payments. \\[4pt]
$\GTenHLProbability{P(X=k)}$; $\GTenHLProbability{P(X\leq b)}$ & \GTenHLProbability{Event probability} & Probability of exactly $k$, or at most $b$, successes. Probabilities are unitless. & \textbullet\ \hyperref[ex:intro-two]{Example 2}: exactly two paid invoices has probability $\GTenHLProbability{0.375}$. \\[4pt]
$\sum_{j=a}^{b}$ & Summation & Add a term for each integer index $j$ from $a$ to $b$, including endpoints. & \textbullet\ \hyperref[ex:intro-two]{Example 2}: $\sum_{j=0}^{2}P(X=j)$ adds the probabilities of zero, one or two payments. \\[4pt]
$\GTenHLSecond{Y=5X}$ & \GTenHLSecond{Revenue} & A monetary consequence of a count, with 5 USD earned per success. & \textbullet\ \hyperref[ex:intro-one]{Example 1}: revenue in USD, distinct from the purchase count and its probability. \\
\bottomrule
\end{longtable}
\endgroup
\subsection{Practice procedure}
'''
s = s[:start] + s[end:]
insert = s.index('\\section{General worked problems}')
s = s[:insert] + table + procedure + '\n' + s[insert:]
# Keep all eight original worked problems; group distinct methods consecutively.
s = s.replace('\\section{General worked problems}', '\\clearpage\n\\section{General Worked Problems --- Exact Counts}\\label{sec:t2-c4-foundational}')
s = s.replace('\\section{Foundational contextual practice}\\label{sec:t2-c4-foundational}', '')
s = s.replace('\\section{Intermediate contextual practice}', '\\clearpage\n\\section{General Worked Problems --- Cumulative Events}')
s = s.replace('\\section{Advanced contextual practice}', '\\clearpage\n\\section{Advanced Problems}')
s = s.replace('\\section{Closing reference: key ideas and common errors}', '\\subsection*{Key ideas and common errors}')
# Move interval problem to the cumulative group, and bridge to the procedure.
a = s.index('\\subsection{Advanced general problem: a central interval}')
b = s.index('\\Needspace{19\\baselineskip}', a)
interval = s[a:b].replace('Advanced general problem: a central interval', 'A central interval')
s = s[:a] + s[b:]
a = s.index('\\subsection{Bridge to the general model}')
b = s.index('\\Needspace{14\\baselineskip}', a)
bridge = s[a:b]
s = s[:a] + s[b:]
pos = s.index('\\clearpage\n\\section{General Worked Problems --- Exact Counts}')
s = s[:pos] + bridge + s[pos:]
pos = s.index('\\Needspace{14\\baselineskip}', s.index('\\section{General Worked Problems --- Cumulative Events}'))
s = s[:pos] + interval + s[pos:]
groups = [('sec:t2-c4-foundational', ['exactly-two','loans','invoices']), ('sec:t2-c4-intermediate',['interval','claims','sales']), ('sec:t2-c4-advanced',['fees','defects'])]
for group, ids in groups:
    start = s.index('\\label{' + group + '}') + len('\\label{' + group + '}')
    next_section = s.find('\\section{', start)
    end = next_section if next_section != -1 else s.index('\\end{document}', start)
    body = s[start:end]
    matches = list(re.finditer(r'\\subsection\{([^}]+)\}', body))
    assert len(matches) == len(ids), (group,len(matches))
    for match, ident in reversed(list(zip(matches,ids))):
        a = match.start()
        b = body.find('\\subsection{', match.end())
        if b == -1: b = len(body)
        chunk = body[a:b]
        chunk = chunk.replace(match.group(0), match.group(0) + '\\label{prob:' + ident + '}', 1)
        task = re.search(r'\\textbf\{Questions/Tasks\}\s*\\begin\{enumerate\}\s*\\item (.*?)\\end\{enumerate\}', chunk, re.S)
        assert task, ident
        chunk = chunk[:task.start()] + '\\QuestionsTasks['+group+']{{4}/{sol:'+ident+'}/{'+task.group(1).strip()+'}}\n' + chunk[task.end():]
        chunk = chunk.replace('\\subsubsection*{Complete worked solution}', '\\subsubsection*{Complete worked solution}\\label{sol:'+ident+'}')
        chunk = re.sub(r'\\secInicio\[\]\[[^\]]+\]', '', chunk)
        # Attach return links directly to the solution, before any next-stage reservation.
        pos = chunk.find('\\Needspace{')
        if pos == -1: pos = len(chunk)
        chunk = chunk[:pos] + '\\secInicio[prob:'+ident+']['+group+']\n' + chunk[pos:]
        body = body[:a] + chunk + body[b:]
    titles = [m.group(1) for m in matches]
    links = '\n\\SectionProblemsTableOfContents{\n' + '\\\\\n'.join('\\SectionProblemLink{prob:'+i+'}{'+t+'}' for i,t in zip(ids,titles))+'\n}\n'
    s = s[:start] + links + body + s[end:]
# Apply existing roles to instructional parameter statements and substitutions.
s = s.replace('Let $X$ count purchases.', 'Let $\\GTenHLValue{X}$ count \\GTenHLValue{purchases}.')
s = s.replace('$n=4$', '$\\HLObservationCount{n}=\\HLObservationCount{4}$', 1)
s = s.replace('$Y=5X$ USD.', '$\\GTenHLSecond{Y=5X}$ USD.', 1)
s = s.replace('\\textbf{Step 2: State parameters and check conditions.}', '\\textbf{Step 2: State parameters and check conditions.}')
def mark_parameters(m):
    n,p,q=m.groups()
    return f'$\\HLObservationCount{{n}}=\\HLObservationCount{{{n}}}$ is fixed, $\\HLSuccessProbability{{p}}=\\HLSuccessProbability{{{p}}}$ and $\\HLComplementProbability{{1-p}}=\\HLComplementProbability{{{q}}}$'
s = re.sub(r'\$n=(\d+)\$ is fixed, \$p=([\d.]+)\$ and \$1-p=([\d.]+)\$', mark_parameters, s)
def mark_sub(m):
    n,k,p,pe,q,qe=m.groups()
    return r'\binom{\HLObservationCount{'+n+r'}}{\GTenHLValue{'+k+r'}}(\HLSuccessProbability{'+p+'})^{'+pe+r'}(\HLComplementProbability{'+q+'})^{'+qe+'}'
s = re.sub(r'\\binom\{(\d+)\}\{(\d+)\}\(([\d.]+)\)\^\{?(\d+)\}?\(([\d.]+)\)\^\{?(\d+)\}?', mark_sub, s)
s = re.sub(r'\\approx (0\.\d+)', r'\\approx \\GTenHLProbability{\1}', s)
s = re.sub(r'probability of the requested success count is (0\.\d+)', r'probability of the requested success count is $\\GTenHLProbability{\1}$', s)
# Avoid redundant page reservations left by relocating whole sections.
s = re.sub(r'(\\Needspace\{(?:14|19)\\baselineskip\}\s*)+(?=\\clearpage)', '', s)
path.write_text(s, encoding='utf-8')
print(path)
