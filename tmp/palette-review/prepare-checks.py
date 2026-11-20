from pathlib import Path
import re
r=Path.cwd();d=r/'book2026-2027/preamble/graphs';o=r/'tmp/palette-review'
p=d/'specific_highlights.md';s=p.read_text(encoding='utf8').replace('`expected`: $E(X)$, $E(Y)$, $\\mu$','`expected`: $E(X)$, $E(Y)$; `meanpop`: $\\mu$').replace('Family mappings', 'Family mappings');p.write_bytes(s.replace('\n','\r\n').encode('utf8'))
tex=(d/'specific_highlights.tex').read_text();keys=set(re.findall(r'practicehighlightlegend@(G[^\\]+)\\endcsname',tex));calls=re.findall(r'\\PreviewLegend\{([^}]+)\}',(d/'specific_highlights_view.tex').read_text());assert keys==set(calls) and len(keys)==len(calls);assert all('`'+k+'`' in s for k in keys);print(len(keys),'unique preview entries, all documented')
preview=(d/'specific_highlights_view.tex').read_text().replace(r'\GTenHighlightstrue',r'\GTenHighlightsfalse').replace('Highlights are enabled for this preview.','Highlights are disabled for this verification copy.');(o/'preview-off.tex').write_text(preview)
c3=r/'book2026-2027/grade10/term_2/1-practice_activities/G10_T2_L1_C3_practice_activity.tex';(o/'c3-off.tex').write_text(c3.read_text().replace(r'% \GTenHighlightsfalse',r'\GTenHighlightsfalse'))
(o/'palette-proof.tex').write_text(r'''\input{../preamble.tex}
\input{highlights.tex}
\input{specific_highlights.tex}
\newcommand{\CheckColor}[2]{\convertcolorspec{named}{#1}{HTML}\actual\def\expected{#2}\ifx\actual\expected\else\errmessage{Unexpected color #1: \actual}\fi\typeout{CHECK-COLOR #1=\actual}}
\newcommand{\CheckPalette}{\CheckColor{GTenHLProbability}{86BFF0}\CheckColor{CtwoConfidenceColor}{55C8F0}\CheckColor{MathHLSuccessColor}{6495DD}\CheckColor{MathHLComplementColor}{D74383}\CheckColor{G11T2C1PopulationProportion}{D74383}}
\CheckPalette
\begingroup\CoordinatedTermTwoPalette\CheckPalette\endgroup
\begingroup\CtwoPracticeIntervalPalette\CheckPalette\endgroup
\CheckPalette
\begin{document}
\section*{Effective probability roles at shared opacity 0.32}
\HLProbability{General probability / mass} $\HLProbability{p_X(x)}=\HLProbability{0.4}$\par
\HLConfidence{Confidence level} $\HLConfidence{C}=\HLConfidence{0.95}$\par
\HLSuccessProbability{Success probability} $\HLSuccessProbability{p}=\HLSuccessProbability{0.4}$\par
\HLComplementProbability{Complement probability} $\HLComplementProbability{1-p}=\HLComplementProbability{0.6}$\par
\HLPopulationProportion{Population proportion} $\HLPopulationProportion{p}=\HLPopulationProportion{0.4}$\par
\GTenHighlightsfalse
\section*{Same content with highlights disabled}
\HLProbability{General probability / mass} $\HLProbability{p_X(x)}=\HLProbability{0.4}$\par
\HLConfidence{Confidence level} $\HLConfidence{C}=\HLConfidence{0.95}$\par
\HLSuccessProbability{Success probability} $\HLSuccessProbability{p}=\HLSuccessProbability{0.4}$\par
\HLComplementProbability{Complement probability} $\HLComplementProbability{1-p}=\HLComplementProbability{0.6}$\par
\end{document}
''')
