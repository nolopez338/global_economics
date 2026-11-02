"""Build standalone Overleaf LaTeX from executed analysis outputs."""
from pathlib import Path
import json
import numpy as np
import pandas as pd
from scipy.optimize import minimize_scalar
from scipy.stats import skewnorm
P=Path(__file__).resolve().parent

def esc(s):
    return str(s).replace('_',r'\_').replace('%',r'\%').replace('&',r'\&')
def num(v):
    if isinstance(v,(int,np.integer)): return str(v)
    if isinstance(v,(float,np.floating)): return f'{v:.5f}' if np.isfinite(v) else '--'
    return esc(v)
def table(headers, rows, small=True):
    out=[r'\begin{center}',r'\small' if small else '',r'\begin{tabular}{'+'l'+'r'*(len(headers)-1)+'}',r'\toprule',' & '.join(esc(h) for h in headers)+r'\\',r'\midrule']
    out+=[' & '.join(num(v) for v in row)+r'\\' for row in rows]
    return '\n'.join(out+[r'\bottomrule',r'\end{tabular}',r'\end{center}'])

if __name__=='__main__':
    R=json.loads((P/'heights_results.json').read_text())
    S=R['sample']; D=R['fit_diagnostics']; w,l,s,a=map(np.array,R['parameters'])
    C=pd.read_csv(P/'heights_components.csv'); M=pd.read_csv(P/'heights_model_comparison.csv')
    B=pd.read_csv(P/'heights_bootstrap.csv'); I=pd.read_csv(P/'heights_bootstrap_intervals.csv',index_col=0)
    Q=pd.read_csv(P/'heights_probabilities.csv')
    # Plain region labels avoid text-font less/greater-than glyph substitution.
    Q['region']=['Lower tail','Central interval','Upper tail']
    n=S['n_retained']; b2=int((B.mode_count==2).sum())
    text=[r'''\documentclass[11pt,a4paper]{article}
\usepackage[margin=20mm]{geometry}
\usepackage{amsmath,amssymb,booktabs,graphicx,float,hyperref,fancyhdr}
\hypersetup{colorlinks=true,urlcolor=blue,linkcolor=blue}
\pagestyle{fancy}\fancyhf{}\lhead{Height distribution analysis}\rhead{Two skew-normal components}\cfoot{\thepage}
\setlength{\headheight}{14pt}\setlength{\parindent}{0pt}\setlength{\parskip}{6pt}
\graphicspath{{./}{assets/data/}}
\begin{document}
\begin{center}{\LARGE Statistical analysis of heights}\\[5pt]
{\large Two-component skew-normal mixture}\\[4pt]
Executed in Python; 2 November 2026\end{center}
\section*{Interpretation}
The constrained best fit has two local maxima. This is a possible descriptive
representation, but the data do not establish a stable two-peaked population.
The second component's shape reaches its upper bound, indicating sensitivity
to nearly one-sided component shapes. AIC favors a two-normal mixture; BIC
favors a single normal. The seven-parameter model is not the preferred model
under either criterion. Components must not be interpreted as demographic,
biological or causal groups without external evidence.
''']
    text.append(f'Of {len(B)} successful observation-bootstrap refits, {b2} ({100*b2/len(B):.1f}\\%) had exactly two modes. These resampling results assume independent observations; they are not a posterior probability of population bimodality.\n')
    text.append(r'\section*{Data inspection and preparation}')
    text.append(f'The UTF-8 CSV has a single header, \\texttt{{height\\_cm}}. With one field per line there is no observable field separator to distinguish comma from other delimiters; comma parsing was used. Decimal formatting uses a point (153.5). There are {S["n_original"]} original data records, {n} retained finite numeric records, and {S["invalid_missing"]} missing/invalid records. No exclusions, winsorization, outlier removal or substantive transformations were performed. Repeated values were preserved. The computational standardization $z=(x-{S["mean_cm"]:.8f})/{S["sd_cm"]:.8f}$ is inverted in all reported parameters.\n')
    text.append(table(['Statistic','Value'],[['Mean (cm)',S['mean_cm']],['Sample variance (cm squared; n-1)',S['variance_cm2']],['Sample SD (cm; n-1)',S['sd_cm']],['Median (cm)',S['median_cm']],['Minimum (cm)',S['min_cm']],['Maximum (cm)',S['max_cm']]]))
    text.append(table(['Percentile','Height (cm)'],[[k,v] for k,v in S['percentiles_cm'].items()]))
    text.append(f'There are {S["unique"]} distinct values; {S["integer_observations"]}/{n} observations are integer centimetres. Rounding/heaping is substantial. Sample percentiles use NumPy linear interpolation. No dates, group labels, censoring, truncation limits or sampling design are supplied. Row-order lag-1 correlation is {S["lag1_correlation"]:.4f}; Spearman correlation with row number is {S["order_spearman"]:.4f}. Neither establishes independence. Repeated measurements or clustering would require an appropriate cluster/block bootstrap with metadata.\n')
    text.append(r'''\clearpage
\section*{Model and estimation}
For real $x$, the fitted model is
\[
 f(x)=w f_{\rm SN}(x;\xi_1,\omega_1,\alpha_1)
 +(1-w)f_{\rm SN}(x;\xi_2,\omega_2,\alpha_2),\qquad
 f_{\rm SN}(x;\xi,\omega,\alpha)=\frac{2}{\omega}\phi(z)\Phi(\alpha z),
 \quad z=\frac{x-\xi}{\omega}.
\]
Here $\phi(z)=(2\pi)^{-1/2}\exp(-z^2/2)$ and
$\Phi(z)=\int_{-\infty}^z\phi(t)\,dt$ are the standard-normal density and CDF.
$\xi$ is a location (cm), $\omega>0$ is a scale (cm); they are generally
not the component mean and standard deviation. Shape $\alpha$ and weight $w$
are dimensionless. Two components do not automatically imply two modes.
The fit was not required to be bimodal.

All seven parameters were jointly optimized against the individual observations.
The log-likelihood is $\ell=\sum_i\log\{wf_1(x_i)+(1-w)f_2(x_i)\}$.
Calculations use normal log-CDFs, stable log-sum-exp, analytic gradients,
log-scales and bounded L-BFGS-B. Analytic gradients were checked against
finite differences (maximum discrepancy $6.8\times10^{-9}$ at an interior point).
This is a best-found constrained likelihood maximum, not a proof of a global
unconstrained maximum.

\textbf{All bounds.} For each component, $71\leq\xi\leq271$ cm,
$1\leq\omega\leq160$ cm, $-20\leq\alpha\leq20$, and
$0.03\leq w\leq0.97$. There is no additional penalty. The location bounds are
the sample range expanded by twice its width; the upper scale is four times
the range. These are broad numerical guards. The 1 cm scale floor corresponds
to the predominant recording increment and prevents arbitrarily narrow
components at repeated observations; it is a modeling choice, not an estimated
measurement-error SD. The weight floor limits tiny fitted groups to roughly
three observations at this sample size. Bounds are frozen to the original
data in every bootstrap refit. Shape caps limit extreme one-sided fits and
are checked below. Scale floors 0.5 and 2 cm are also investigated.
''')
    text.append(f'The primary fit used seed {R["seed"]}, {D["attempted"]} starts with quantile-separated/overlapping locations, random scales and weights, and mixed positive, zero and negative shapes. {D["converged"]} starts converged; {D["within_0.01"]} converged within 0.01 log-likelihood units of the best. The worst converged log-likelihood was {D["worst_converged_loglik"]:.6f}, versus {D["best_loglik"]:.6f} for the best. Thus competing starts can reach materially inferior local solutions. The best used {D["iterations"]} iterations.\n')
    text.append('The best optimizer run stopped on the relative function-reduction criterion (the exact message is in JSON). Active bound: second (higher-mean) component shape $\\alpha_2=20$. The raw gradient infinity norm is '+f'{D["gradient_inf"]:.6g}'+r'; at an active constraint it need not vanish. All other primary bounds are inactive. Full per-start likelihoods are saved in the JSON results. Convergence is the optimizer criterion, not a guarantee of global optimality.'+'\n')
    text.append(r'''\section*{Rounding and sampling limitations}
The analysis maximizes continuous densities at the reported values, as requested.
A rounded-data likelihood integrating over measurement intervals could alter
the sharp valley near common recorded heights; it was not fitted because the
measurement protocol is unknown. No jitter was added. Independence is plausible
only as a working cross-sectional assumption: it cannot be verified from
this one-column file. No evidence in the file establishes selection limits,
truncation or censoring. The empirical extrema are not physical support bounds.
''')
    text.append(r'\clearpage\section*{Parameters and moments}')
    text.append(table(['Component','Weight','Location (cm)','Scale (cm)','Shape'],C[['component','weight','location_cm','scale_cm','alpha']].values.tolist()))
    text.append(table(['Component','Actual mean (cm)','Actual SD (cm)'],C[['component','mean_cm','sd_cm']].values.tolist()))
    text.append(r'''Labels are ordered by actual component mean, including in every bootstrap fit.
For $\delta_j=\alpha_j/\sqrt{1+\alpha_j^2}$,
\[
 m_j=\xi_j+\omega_j\delta_j\sqrt{2/\pi},\quad
 v_j=\omega_j^2(1-2\delta_j^2/\pi),\quad
 \mu=\sum_jw_jm_j,\quad V=\sum_jw_j\{v_j+(m_j-\mu)^2\}.
\]
''')
    text.append(f'The mixture mean is {R["mixture_mean"]:.6f} cm, variance {R["mixture_sd"]**2:.6f} cm$^2$, and SD {R["mixture_sd"]:.6f} cm. Sample mean and sample SD ($n-1$) are {S["mean_cm"]:.6f} and {S["sd_cm"]:.6f} cm. The model variance is a population moment and is not corrected by $n/(n-1)$.\n')
    text.append(r'\textbf{Complete fitted density.} For $x$ measured in cm, define'+f' $z_1=(x-{l[0]:.8f})/{s[0]:.8f}$ and $z_2=(x-{l[1]:.8f})/{s[1]:.8f}$. Then\n')
    text.append('\\[ f(x)='+f'{w[0]:.8f}\\frac{{2}}{{{s[0]:.8f}}}\\phi(z_1)\\Phi({a[0]:.8f}z_1) + {w[1]:.8f}\\frac{{2}}{{{s[1]:.8f}}}\\phi(z_2)\\Phi({a[1]:.8f}z_2)'+'\\]\n')
    text.append(f'Density units are cm$^{{-1}}$. Unrounded parameters in the JSON are used for all calculations. The mathematical support is the entire real line. Heights are physically positive; fitted $P(X<0)={R["probability_below_zero"]:.3g}$ (negligible to numerical precision). No contextual upper physiological bound is supplied, so no invented upper-limit probability is reported.\n')
    text.append(r'\section*{Comparison on the same observations}')
    text.append(table(['Model','k','Log likelihood','AIC','BIC'],M.values.tolist()))
    text.append(r'''AIC $=2k-2\ell$; BIC $=k\log n-2\ell$. A normal has 2 parameters,
a skew-normal 3, two normals 5 and two skew-normals 7. Normal fitting is
analytic; the skew-normal used 60 starts and two normals 100. Alternatives use
the same broad location/scale guards; shape/weight bounds apply when relevant.
The simple normal maximum is interior. AIC favors two normals, while BIC
favors the normal. The two-skew-normal gain over two normals is small for
two additional parameters. These criteria are descriptive approximations:
mixtures are nonregular and the selected shape bound is active. Nominal
parameter counts are not adjusted to make the constrained model look better.
No ordinary chi-square likelihood-ratio test for component count was used:
under the null, component parameters can be unidentified and weights lie on
a boundary. Rounding and possible dependence further limit inference.
''')
    text.append(r'\clearpage\section*{Numerical modes and sensitivity}')
    text.append(table(['Extremum','Height (cm)','Density (1/cm)'],[[e['type'],e['position'],e['density']] for e in R['extrema']]))
    ex=R['extrema']; modes=[e for e in ex if e['type']=='mode']; valley=[e for e in ex if e['type']=='valley']
    if len(modes)==2 and valley: text.append(f'The valley density is {valley[0]["density"]/min(e["density"] for e in modes):.3f} times the lower peak density. The primary fit therefore has two distinct mathematical peaks, but the conclusion about a population remains sensitive to fitted shape and sampling variability.\n')
    text.append(f'The adaptive search spans {R["domain"][0]:.4f} to {R["domain"][1]:.4f} cm, extending ten scale parameters either side of every component location and including the observed range. '+r'Since each skew-normal density is at most twice its corresponding normal density, each omitted tail is bounded above by $2\Phi(-10)<1.6\times10^{-23}$. Derivative sign changes on 8,193 points were refined with Brent root finding. Repeating with 32,769 points gives the same extrema to '+f'{max(abs(e["position"]-f["position"]) for e,f in zip(ex,R["extrema_fine"])):.2g}'+r' cm. The extreme tails lie beyond all component modes; each component is monotone there. No tail peaks are hidden by the search boundary.'+'\n')
    cmodes=[minimize_scalar(lambda xx:-skewnorm.pdf(xx,a[j],loc=l[j],scale=s[j]),bounds=(l[j]-10*s[j],l[j]+10*s[j]),method='bounded').x for j in range(2)]
    text.append(table(['Component','Mean (cm)','Component mode (cm)'],[[j+1,C.mean_cm[j],cmodes[j]] for j in range(2)]))
    text.append('Total-density modes differ from both component means and component modes.\n')
    sensrows=[]
    for d in R['sensitivity']:
        modes2=[e['position'] for e in d['extrema'] if e['type']=='mode']
        sensrows.append([d['floor_cm'],d['alpha_cap'],d['loglik'],len(modes2),', '.join(f'{v:.3f}' for v in modes2)])
    text.append(table(['Scale floor (cm)','Shape cap','Log likelihood','Modes','Mode locations (cm)'],sensrows))
    text.append('Reducing the scale floor to 0.5 cm yields an almost equally likely solution with peaks near 168.68 and 180.03 cm. A shape cap of 10 instead gives peaks near 159.95 and 173.87 cm and an active scale floor. Thus peak positions are not robust to reasonable constraints, even though all these fits are mathematically bimodal.\n')
    text.append('Each sensitivity fit used 80 new starts plus the primary warm start. These are alternative constrained best-found solutions, with no penalty. Full sensitivity parameters and extrema are in the JSON. Active constraints by sensitivity setting:\n\\begin{itemize}\n')
    for d in R['sensitivity']:
        text.append(f'\\item Floor {d["floor_cm"]} cm, shape cap {d["alpha_cap"]}: '+esc(', '.join(d['active']) or 'none')+'.\n')
    text.append(r'''\end{itemize}
Constraint index mapping (zero based optimizer vector): 0 weight; 1,2,3 first
location, log-scale, shape; 4,5,6 second location, log-scale, shape.
Indices refer to optimizer ordering, which can differ from mean-ordered labels.
An increasing shape cap can raise likelihood through a sharper transition near
rounded observations. This is a warning about interpreting the valley literally.
Sensitivity here varies scale and shape bounds; broader weight-floor or
measurement-protocol studies are recommended, not claimed as executed.
''')
    text.append(r'''\clearpage\section*{Density and histogram sensitivity}
\begin{center}\includegraphics[width=0.96\textwidth]{heights_density.png}\end{center}
The histogram integrates to one; component curves are multiplied by their
weights and sum to the total density. Freedman--Diaconis bins are used above.
\begin{center}\includegraphics[width=\textwidth]{heights_bins.png}\end{center}
The same fitted curve is shown over 6, 10 and 20 equal-width bins on the same
observations. Apparent histogram peaks depend on binning and rounding. None
of these views was used to remove observations or force a bimodal fit.
No kernel density estimate was used, so there is no unreported KDE bandwidth.
\clearpage\section*{CDF and mixture Q--Q diagnostics}
\begin{center}\includegraphics[width=0.85\textwidth]{heights_cdf.png}\end{center}
\begin{center}\includegraphics[width=0.72\textwidth,height=0.37\textheight,keepaspectratio]{heights_qq.png}\end{center}
''')
    text.append(f'KS statistic $D={R["KS"]:.6f}$; Cram\\\'er--von Mises statistic $W^2={R["CvM"]:.6f}$. Q--Q plotting positions are $(i-0.5)/n$; mixture quantiles solve $\\sum_jw_jF_j(q)=p$ numerically by Brent root finding. Empirical ties remain visible. No goodness-of-fit p-values are reported: fixed-parameter p-values are invalid after fitting to these data. A valid calibration would simulate from the fitted model and refit in each replicate, with rounding modeled if known. Such a parametric goodness-of-fit bootstrap was not executed. The nonparametric bootstrap below assesses uncertainty, not goodness-of-fit p-values.\n')
    text.append(r'\clearpage\section*{Bootstrap uncertainty and membership}')
    text.append(f'An ordinary observation bootstrap resampled {n} rows with replacement, preserving ties and outliers. All seven parameters were refitted jointly, with components relabeled by actual mean. Requested replicates: {R["bootstrap_requested"]}; successful: {R["bootstrap_successful"]}; failed refits: {len(R["bootstrap_failures"])}. Each replicate used 20 fresh randomized starts plus the primary warm start. There were {R["bootstrap_failed_starts"]} individual nonconverged starts; a replicate succeeded if at least one start converged. Active constraints occurred in {100*R["bootstrap_active_fraction"]:.1f}\\% of replicates. The full replicate output includes counts of converged starts and active bounds.\n')
    text.append(table(['Number of modes','Bootstrap count'],[[k,v] for k,v in sorted(R['bootstrap_mode_counts'].items())]))
    text.append('Intervals below are the 2.5th and 97.5th percentiles of the successful fits, with their bootstrap median. They describe a constrained, potentially nonregular and weakly identified model, not guaranteed 95\\% coverage. The 200 replicates provide a practical uncertainty assessment with appreciable Monte Carlo error; a few modes can change the percentages. Bootstrap refits used fewer starts than the primary fit, so local-optimum error cannot be ruled out.\n')
    labels={'mixture_mean':'Mixture mean (cm)','mixture_sd':'Mixture SD (cm)','lower_mode_if_two':'Lower mode | two modes (cm)','upper_mode_if_two':'Upper mode | two modes (cm)'}
    for j in [1,2]:
        for key in ['weight','location','scale','alpha','mean','sd']:
            labels[f'c{j}_{key}']=f'C{j} {key}'+(' (cm)' if key not in ['weight','alpha'] else '')
    text.append(table(['Quantity','2.5th percentile','Median','97.5th percentile'],[[labels[k]]+I.loc[k].tolist() for k in labels]))
    text.append(f'The mode-location rows condition on exactly two modes ({b2} fits); they exclude unimodal or other fits and must not be read as unconditional mode confidence intervals. The bootstrap bimodal fraction is {b2/len(B):.4f}; its simulation standard error is approximately {np.sqrt((b2/len(B))*(1-b2/len(B))/len(B)):.4f}.\n')
    text.append(r'''For each retained observation, the exported posterior membership is
\[
 \tau_{i1}=\frac{wf_1(x_i)}{wf_1(x_i)+(1-w)f_2(x_i)},\qquad
 \tau_{i2}=1-\tau_{i1}.
\]
These are fitted statistical responsibilities, not verified real-world labels
or probabilities of a causal category. The cleaned CSV retains source row
numbers and the exact numerical observations alongside both probabilities.
''')
    if (P/'heights_validation.json').exists():
        V=json.loads((P/'heights_validation.json').read_text())
        text.append(f'An independent 32,769-point check of every bootstrap density found {len(V["bootstrap_mode_count_discrepancies"])} discrepancies in mode counts relative to the 4,097-point bootstrap search. Numerical integration verified total mass {V["density_integral"]:.10f}, mixture mean and variance, and equality of cleaned observations to the source data.\n')
    text.append(r'\clearpage\footnotesize\setlength{\parskip}{4pt}\section*{Quantiles and probability comparisons}')
    text.append(table(['Mixture quantile','Height (cm)'],list(zip(['q0.10','q0.50','q0.90'],R['quantiles_10_50_90']))))
    text.append('Exact computed boundaries, serialized with full precision in JSON, are used consistently for both empirical counts and fitted CDF calculations. The reported rounded table values are for display only. For this continuous model, endpoint point-mass is zero. No contextual threshold $c$ was supplied.\n')
    text.append(table(['Region','Count','Empirical','Fitted','Absolute difference','Relative error (%)'],Q.values.tolist()))
    text.append(r'''The intervals use exactly $X<q_{0.10}$,
$q_{0.10}\leq X\leq q_{0.90}$, and $X>q_{0.90}$.
Absolute difference is $|p_{\rm empirical}-p_{\rm model}|$; relative percentage
error is $100|p_{\rm empirical}-p_{\rm model}|/p_{\rm model}$, undefined when
the model probability is zero. These in-sample checks use boundaries estimated
from the same data and are not independent validation.
\section*{Reproducibility and delivered files}
Run from any directory:
\begin{verbatim}
python /path/to/assets/data/fit_heights.py
python /path/to/assets/data/validate_heights.py
python /path/to/assets/data/build_heights_report.py
cd /path/to/assets/data
pdflatex -interaction=nonstopmode -halt-on-error heights.tex
pdflatex -interaction=nonstopmode -halt-on-error heights.tex
\end{verbatim}
Only NumPy, SciPy, pandas and Matplotlib are required for the analysis;
no web connection is needed. The random generator is NumPy default\_rng,
seed ''')
    text.append(str(R['seed'])+'. All randomized fits and bootstrap resampling consume this generator sequentially, so rerun the whole script to reproduce the sequence. Package versions used:\n')
    text.append(table(['Package','Version'],list(R['versions'].items())))
    text.append(r'''The standalone \texttt{heights.tex} uses the four PNG figures in this folder.
Upload the TeX and these PNGs together to Overleaf; it requires no local
absolute paths or external bibliography. Delivered tables: model comparison,
components, probability comparisons, bootstrap replicates and percentile
intervals (CSV). The cleaned data and responsibilities are in
\texttt{heights\_cleaned.csv}. Complete numerical results, bounds diagnostics,
per-start likelihoods, sensitivity fits, versions and input checksum are in
\texttt{heights\_results.json}. The source CSV is unchanged.
''')
    text.append('Input SHA-256:\\par{\\scriptsize\\texttt{'+R['sha256_input'][:32]+r'\allowbreak '+R['sha256_input'][32:]+'}}\n')
    text.append(r'''\section*{Methods references and unexecuted checks}
The density convention follows the
\href{https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.skewnorm.html}{SciPy skew-normal documentation}.
The requirement to refit for goodness-of-fit calibration is described in
\href{https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.goodness_of_fit.html}{SciPy goodness-of-fit documentation}.
No parametric goodness-of-fit bootstrap, dependence-aware bootstrap,
rounded/censored likelihood, external validation or causal grouping analysis
was executed. These require additional computation and/or sampling metadata.
All tables and figures in this report were produced by the executed Python analysis.
\end{document}
''')
    (P/'heights.tex').write_text('\n'.join(text),encoding='utf-8')
    print('Wrote',P/'heights.tex')
