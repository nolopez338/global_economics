from pathlib import Path
p=Path('book2026-2027/grade10/term_2/3-slides/G10_T2_L1_C2_slides.tex')
s=p.read_text(encoding='utf-8')
s=s.replace(r'\newcommand<>{\H}[2]{\begingroup',r'\newcommand<>{\H}[2]{\leavevmode\begingroup')
s=s.replace(r'\rule{0pt}{.66cm}',r'\rule{0pt}{.56cm}')
s=s.replace(r'\begin{tabular}',r'\small\begin{tabular}')
s=s.replace(r'\visible<',r'\leavevmode\visible<')
s=s.replace(r'\end{tabular}\begin{overlayarea}',r'\end{tabular}\par\medskip\begin{overlayarea}')
s=s.replace(r'\begin{frame}[t]{Highlight legend}'+'\n'+r'\small',r'\begin{frame}[t]{Highlight legend}'+'\n'+r'\small\renewcommand{\arraystretch}{1.1}')
s=s.replace(r'\begin{column}{.49\textwidth}\leavevmode\visible<1-13>',r'\begin{column}{.49\textwidth}\small\leavevmode\visible<1-13>')
# Outcome header probability needs adequate width in narrower grouping column.
s=s.replace('p{0.43\\linewidth}>{\\raggedright\\arraybackslash}p{0.27\\linewidth}', 'p{0.40\\linewidth}>{\\raggedright\\arraybackslash}p{0.30\\linewidth}')
# Clean, two-column PMF on its own at the final grouping overlay; retain prior geometry until transition.
a=s.index('\\begin{frame} <1-9>'); b=s.index('\\end{frame}',a)
part=s[a:b]
start=part.index('\\small\\begin{tabular}',part.index('\\end{column}'))
end=part.index('\\end{tabular}',start)+len('\\end{tabular}')
two=r'''\only<9>{\small\begin{tabular}{@{}p{.38\linewidth}p{.48\linewidth}@{}}\toprule
$x$ (USD)&$p_X(x)$\\\midrule
\Blank{0}&0.15\\\Blank{2}&0.60\\\Blank{4}&0.25\\\bottomrule\end{tabular}}'''
part=part[:start]+r'\only<1-8>{'+part[start:end]+'}'+two+part[end:]
s=s[:a]+part+s[b:]
p.write_text(s,encoding='utf-8')
