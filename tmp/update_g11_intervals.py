from pathlib import Path
import re

target = Path('book2026-2027/grade11/term_2/1-practice_activities/G11_T2_L1_C2_practice.tex')
source = target.read_text(encoding='utf-8')
Path('tmp/g11-intervals-before.tex').write_text(source, encoding='utf-8')

def graph(mean, rows, xmin, xmax, ticks, axis):
    n = len(rows)
    rowlabels = ','.join(r'\CtwoConfidence{'+str(level)+r'\%}' for level,_,_ in rows)
    out = rf'''\begin{{center}}
\begin{{tikzpicture}}
\begin{{axis}}[
    width=0.88\linewidth,height={3.5 + .4*n}cm,axis lines=left,
    xmin={xmin},xmax={xmax},ymin=0.35,ymax={n+.7},
    xlabel={{{axis}}},
    ytick={{{','.join(str(i) for i in range(1,n+1))}}},
    yticklabels={{{rowlabels}}},
    xtick={{{ticks}}},tick label style={{font=\small}},label style={{font=\small}}]
    \addplot[black,dashed] coordinates {{({mean},0.35) ({mean},{n+.3})}};
    \node[anchor=south,font=\small] at (axis cs:{mean},{n+.3}) {{$\CtwoPoint{{\bar{{x}}}}$}};
'''
    for i, (level, lo, hi) in enumerate(rows, 1):
        out += rf'''    \addplot[black,thick,mark=|,mark size=5pt] coordinates {{({lo},{i}) ({hi},{i})}};
    \addplot[black,only marks,mark=*,mark size=2pt] coordinates {{({mean},{i})}};
    \node[anchor=south,font=\small] at (axis cs:{lo},{i+.05}) {{$\CtwoEndpoint{{{lo}}}$}};
    \node[anchor=south,font=\small] at (axis cs:{hi},{i+.05}) {{$\CtwoEndpoint{{{hi}}}$}};
'''
    return out + '\\end{axis}\n\\end{tikzpicture}\n\\end{center}\n'

source = source.replace(r'\SectionProblemLink{prob:c2-3}{Bus commute times in a simulation}', r'''\SectionProblemLink{prob:c2-3}{Bus commute times in a simulation} \\
    \SectionProblemLink{prob:c2-compare-three}{Three confidence levels for repair times}''')

graph32 = graph(120, [(90,'113.749','126.251'), (99,'110.2112','129.7888')],108,132,'110,115,120,125,130','Mean monthly household energy bill (thousand COP)')
explain32 = r'''This graph compares the \CtwoConfidence{two unrounded intervals from the same sample}. Both centre markers and the dashed line mark the \CtwoPoint{sample mean} $\CtwoPoint{\bar{x}}=\CtwoPoint{120\,\text{thousand COP}}$; the actual \CtwoMean{population mean} $\CtwoMean{\mu}$ remains unknown. Increasing confidence widens the interval while keeping this centre fixed. The graph uses the calculated endpoints before rounding. The reports instead round each endpoint to the nearest thousand COP and calculate the reported width from those rounded endpoints; nominal confidence and simulated coverage refer to the unrounded procedures.

'''
start = source.index(r'\label{sol:c2-2-b}')
position = source.index(r'\par\vspace{3mm}\secInicio[prob:c2-2]', start)
source = source[:position] + graph32 + '\n' + explain32 + source[position:]

new = r'''\subsection{Three confidence levels for repair times}
\label{prob:c2-compare-three}

A repair cooperative takes one independent random sample of $n=64$ completed appliance repairs from a specified month. The sample mean repair time is $\bar{x}=50$ minutes. Assume normally distributed repair times with known population standard deviation $\sigma=16$ minutes. Use this same sample to calculate exactly three two-sided confidence intervals: 90\%, 95\%, and 99\%, with $z^*=1.645$, $1.960$, and $2.576$, respectively. Keep the sample mean, sample size, population standard deviation, and standard error unchanged across the three procedures. Do not round intermediate calculations or endpoints.

In a separate hypothetical simulation, a normal population has known fixed mean $\mu=51$ minutes and the same $\sigma=16$ minutes. From each of 200 fresh samples of size $n=64$, all three unrounded intervals are constructed around that sample's mean. The mutually exclusive rows below count the outcomes for these triples. The simulated samples are separate from the cooperative's original sample.

\begin{center}
\begin{tabular}{@{}lr@{}}
    \toprule
    Outcome for the intervals from one simulated sample & Number of samples \\
    \midrule
    All three cover the simulated mean & 178 \\
    Only the 95\% and 99\% intervals cover & 12 \\
    Only the 99\% interval covers & 7 \\
    None of the three covers & 3 \\
    \bottomrule
\end{tabular}
\end{center}

\QuestionsTasks[sec:general-worked]{
    {2}/{sol:c2-compare-three-a}/{\InformationTask},
    {2}/{sol:c2-compare-three-b}/{\IntervalTask\ Compare all three widths and explain what happens to the centre as confidence increases.},
    {2}/{sol:c2-compare-three-c}/{\CoverageTask\ Which option gives the observed coverage rates in the order 90\%, 95\%, 99\% and correctly interprets increasing confidence?}
}

\begin{answeroptions}
    \item 90\%, 95\%, 99\%. Every finite simulation must match its nominal levels exactly.
    \item 89\%, 95\%, 98.5\%. Higher confidence gives wider intervals with the same sample mean as centre; confidence describes long-run coverage of the fixed population mean.
    \item 89\%, 95\%, 98.5\%. Higher confidence moves the interval centre closer to the unknown population mean.
    \item 89\%, 95\%, 98.5\%. The cooperative's calculated 99\% interval has a 99\% probability of containing its fixed population mean.
\end{answeroptions}

\clearpage
\subsubsection*{Task 1 solution. Organize the information and calculate SE}
\label{sol:c2-compare-three-a}

\InformationTable{
    $\CtwoMean{\mu}$ & \CtwoMean{Population mean} & Population parameters & The fixed, unknown mean time for all appliance repairs completed by the cooperative in the specified month, in \CtwoMean{minutes}. The separate simulation uses a known mean of \CtwoMean{51 minutes}. \\
    $\CtwoPoint{\bar{x}}$ & \CtwoPoint{Sample mean} & Sample statistics & $\CtwoPoint{\bar{x}}=\CtwoPoint{50\,\text{minutes}}$, shared by all three intervals. The point estimate of the cooperative's unknown mean repair time. \\
    $\CtwoSize{n}$ & \CtwoSize{Sample size} & Sample statistics & $\CtwoSize{n}=\CtwoSize{64\,\text{repairs}}$, shared. All three intervals use the same original sample. \\
    $\CtwoSD{\sigma}$ & \CtwoSD{Population} \CtwoSD{standard} \CtwoSD{deviation} & Population parameters & $\CtwoSD{\sigma}=\CtwoSD{16\,\text{minutes}}$, shared. Known population parameter. \\
    $\CtwoConfidence{C}$ & \CtwoConfidence{Confidence level} & Procedure Settings & \CtwoConfidence{90\%}: $\CtwoConfidence{C}=\CtwoConfidence{0.90}$.\par \CtwoConfidence{95\%}: $\CtwoConfidence{C}=\CtwoConfidence{0.95}$.\par \CtwoConfidence{99\%}: $\CtwoConfidence{C}=\CtwoConfidence{0.99}$. \\
    $\CtwoSignificance{\alpha}$ & \CtwoSignificance{Significance level} & Procedure Settings & \CtwoConfidence{90\%}: $\CtwoSignificance{\alpha}=1-\CtwoConfidence{0.90}=\CtwoSignificance{0.10}$.\par \CtwoConfidence{95\%}: $\CtwoSignificance{\alpha}=1-\CtwoConfidence{0.95}=\CtwoSignificance{0.05}$.\par \CtwoConfidence{99\%}: $\CtwoSignificance{\alpha}=1-\CtwoConfidence{0.99}=\CtwoSignificance{0.01}$. Total area outside the central region. \\
    $\CtwoSignificance{\alpha}/2$ & \CtwoSignificance{Tail area} & Procedure Settings & \CtwoConfidence{90\%}: $\CtwoSignificance{\alpha}/2=\CtwoSignificance{0.05}$.\par \CtwoConfidence{95\%}: $\CtwoSignificance{\alpha}/2=\CtwoSignificance{0.025}$.\par \CtwoConfidence{99\%}: $\CtwoSignificance{\alpha}/2=\CtwoSignificance{0.005}$. Area in each tail. \\
    $\CtwoCritical{z^*}$ & \CtwoCritical{Critical value} & Procedure Settings & \CtwoConfidence{90\%}: $\CtwoCritical{z^*}=\CtwoCritical{1.645}$.\par \CtwoConfidence{95\%}: $\CtwoCritical{z^*}=\CtwoCritical{1.960}$.\par \CtwoConfidence{99\%}: $\CtwoCritical{z^*}=\CtwoCritical{2.576}$. Standard normal multipliers. \\
    $\CtwoSE{\mathrm{SE}}$ & \CtwoSE{Standard error} & Sample statistics & $\CtwoSE{\mathrm{SE}}=\CtwoSD{\sigma}/\sqrt{\CtwoSize{n}}=\CtwoSD{16}/\sqrt{\CtwoSize{64}}=\CtwoSD{16}/\CtwoSize{8}=\CtwoSE{2\,\text{minutes}}$, shared. The standard deviation of sample means over repeated samples of this size. \\
}

\par\vspace{3mm}\secInicio[prob:c2-compare-three][sec:general-worked]

\clearpage
\subsubsection*{Task 2 solution. Calculate MoE and state the intervals}
\label{sol:c2-compare-three-b}

For each level, $\CtwoMoE{\mathrm{MoE}}=\CtwoCritical{z^*}\times\CtwoSE{\mathrm{SE}}$, the endpoints are $\CtwoPoint{\bar{x}}\pm\CtwoMoE{\mathrm{MoE}}$, and the \CtwoWidth{full width} is $2\CtwoMoE{\mathrm{MoE}}$.

\EstimationTable{
    \CtwoConfidence{90\%} interval & $\CtwoMoE{\mathrm{MoE}}=\CtwoCritical{1.645}(\CtwoSE{2})=\CtwoMoE{3.29\,\text{minutes}}$.\par $[\CtwoPoint{50}-\CtwoMoE{3.29},\CtwoPoint{50}+\CtwoMoE{3.29}]=[\CtwoEndpoint{46.71},\CtwoEndpoint{53.29}]$ \CtwoEndpoint{minutes}.\par \CtwoWidth{Width}: $2(\CtwoMoE{3.29})=\CtwoWidth{6.58\,\text{minutes}}$. & The narrowest range of plausible values for the cooperative's mean repair time under the model. \\
    \CtwoConfidence{95\%} interval & $\CtwoMoE{\mathrm{MoE}}=\CtwoCritical{1.960}(\CtwoSE{2})=\CtwoMoE{3.92\,\text{minutes}}$.\par $[\CtwoPoint{50}-\CtwoMoE{3.92},\CtwoPoint{50}+\CtwoMoE{3.92}]=[\CtwoEndpoint{46.08},\CtwoEndpoint{53.92}]$ \CtwoEndpoint{minutes}.\par \CtwoWidth{Width}: $2(\CtwoMoE{3.92})=\CtwoWidth{7.84\,\text{minutes}}$. & A wider range of plausible values for the same unknown mean under the model. \\
    \CtwoConfidence{99\%} interval & $\CtwoMoE{\mathrm{MoE}}=\CtwoCritical{2.576}(\CtwoSE{2})=\CtwoMoE{5.152\,\text{minutes}}$.\par $[\CtwoPoint{50}-\CtwoMoE{5.152},\CtwoPoint{50}+\CtwoMoE{5.152}]=[\CtwoEndpoint{44.848},\CtwoEndpoint{55.152}]$ \CtwoEndpoint{minutes}.\par \CtwoWidth{Width}: $2(\CtwoMoE{5.152})=\CtwoWidth{10.304\,\text{minutes}}$. & The widest range of plausible values for the same unknown mean under the model. \\
}

GRAPH34

These are \CtwoConfidence{three intervals from the same sample}. Their centre markers and dashed line all mark the \CtwoPoint{sample mean} $\CtwoPoint{\bar{x}}=\CtwoPoint{50\,\text{minutes}}$; the cooperative's \CtwoMean{population mean} $\CtwoMean{\mu}$ remains unknown. With the same \CtwoSE{standard error}, increasing confidence increases $\CtwoCritical{z^*}$, hence the \CtwoMoE{margin of error} and \CtwoWidth{width}, while the centre stays fixed. The intervals are nested: the \CtwoConfidence{90\%} interval lies within the \CtwoConfidence{95\%} interval, which lies within the \CtwoConfidence{99\%} interval.

\par\vspace{3mm}\secInicio[prob:c2-compare-three][sec:general-worked]

\clearpage
\noindent\begin{minipage}{\linewidth}
\subsubsection*{Task 3 solution. Calculate coverage and interpret confidence}
\label{sol:c2-compare-three-c}

\textbf{Correct option B.} The mutually exclusive counts total $178+12+7+3=200$ simulated samples. Each level has its own denominator of 200 intervals:
\begin{align*}
    \CtwoConfidence{90\%}:\quad &\frac{178}{200}\times100\%=\CtwoCoverage{89\%},\\
    \CtwoConfidence{95\%}:\quad &\frac{178+12}{200}\times100\%=\frac{190}{200}\times100\%=\CtwoCoverage{95\%},\\
    \CtwoConfidence{99\%}:\quad &\frac{178+12+7}{200}\times100\%=\frac{197}{200}\times100\%=\CtwoCoverage{98.5\%}.
\end{align*}
The evidence is consistent with nested intervals: whenever a narrower interval covers the simulated mean, its wider partners also cover it. Within each simulated triple, the centre is that fresh sample's mean; it can vary between samples.

The \CtwoCoverage{observed rates} describe this finite run and need not match the \CtwoConfidence{nominal levels} exactly. Under the model, about \CtwoConfidence{90\%}, \CtwoConfidence{95\%}, and \CtwoConfidence{99\%} of the respective intervals cover the fixed population mean over many repetitions. Higher confidence requires a \CtwoWidth{wider interval} from a given sample; it does not move the \CtwoPoint{sample mean}. Once calculated, each interval either \CtwoCoverage{contains the fixed mean} or \CtwoCoverage{misses it}; a confidence level is not a probability assigned to that particular fixed interval containing the mean.

\par\vspace{3mm}\secInicio[prob:c2-compare-three][sec:general-worked]
\end{minipage}\par

\clearpage

'''
new = new.replace('GRAPH34', graph(50, [(90,'46.71','53.29'),(95,'46.08','53.92'),(99,'44.848','55.152')],43,57,'44,46,48,50,52,54,56','Mean appliance repair time (minutes)'))
source = source.replace(r'\section{Advanced Problems}', new + r'\section{Advanced Problems}', 1)
target.write_text(source, encoding='utf-8')
print('Updated source; original snapshot saved in tmp/g11-intervals-before.tex')
