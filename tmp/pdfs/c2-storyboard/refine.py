from pathlib import Path
p=Path('book2026-2027/grade10/term_2/3-slides/G10_T2_L1_C2_slides.tex'); s=p.read_text(encoding='utf-8')
s=s.replace(r'\colorlet{cTwoGuideColor}{cTwoMassColor!35}',r'''\colorlet{cTwoGuideColor}{cTwoMassColor!35}
\ifGTenHighlights\else
\colorlet{cTwoMassColor}{black}\colorlet{cTwoCDFColor}{black}\colorlet{cTwoGuideColor}{gray}
\fi''')
s=s.replace(r'\newcommand{\GraphStart}',r'\newcommand{\TickLabel}[1]{#1}'+'\n'+r'\newcommand{\GraphStart}')
s=s.replace(r'\path[use as bounding box] (-1.85,-.28) rectangle (5.65,1.24);',r'\path[use as bounding box] (-1.85,-.28) rectangle (5.65,1.24);\begin{pgfinterruptboundingbox}')
s=s.replace(r'at (\x,-.025){\x}',r'at (\x,-.025){\TickLabel{\x}}')
s=s.replace(r'\newcommand{\GraphEnd}{\end{tikzpicture}}',r'\newcommand{\GraphEnd}{\end{pgfinterruptboundingbox}\end{tikzpicture}}')
a=s.index(r'\begin{frame} <1-7>'); b=s.index(r'\end{frame}',a)
part=s[a:b]
part=part.replace(r'\visible<2-6>{\GraphStart',r'\visible<2-6>{\renewcommand{\TickLabel}[1]{\ifnum##1=0\H<3>{Quantity}{##1}\else\ifnum##1=2\H<4>{Quantity}{##1}\else\H<5>{Quantity}{##1}\fi\fi}\GraphStart')
# In Beamer stored frame body, a local macro definition takes single # tokens.
part=part.replace('##1','#1')
for n,x in [(3,0),(4,2),(5,4)]:
    part=part.replace(r'\node[below] at ('+str(x)+r',-.025){\H<'+str(n)+r'>{Quantity}{'+str(x)+'}};','')
s=s[:a]+part+s[b:]
# Keep the last relationship highlighted during statement removal; clear on overlay 15.
a=s.index(r'\begin{frame} <1-15>');b=s.index(r'\end{frame}',a)
part=s[a:b].replace(r'\H<11-13>',r'\H<11-14>').replace(r'\H<12-13>',r'\H<12-14>').replace(r'\H<13>',r'\H<13-14>')
s=s[:a]+part+s[b:]
# Rebuild final stacked frame using explicitly equal physical scales.
cut=s.index(r'\begin{frame} <1-32>')
stack=r'''\begin{frame}<1-32>[t]{Connecting the PMF and CDF}
\centering
\begin{tikzpicture}[x=1.35cm,y=1cm]
\path[use as bounding box] (-1.9,-.90) rectangle (5.65,5.15);
\begin{pgfinterruptboundingbox}
% Both panels: 8.505 cm plot width; 2 cm per probability unit.
% The upper baseline is exactly 2.55 cm above the lower baseline.
\foreach \base/\label in {0/{p_X(x)},2.55/{F_X(x)}}{
\foreach \v in {0,.25,.5,.75,1}{\draw[gray!15] (-1,{\base+2*\v})--(5.3,{\base+2*\v});
\node[anchor=east,font=\small] at (-1.1,{\base+2*\v}){\pgfmathprintnumber{\v}};}
\draw[->] (-1,\base)--(5.5,\base);\draw[->] (-1,\base)--(-1,{\base+2.2});
\foreach \a in {0,2,4}{\draw (\a,\base)--(\a,{\base-.045});\node[below,font=\small] at (\a,{\base-.045}){\a};}
\node[anchor=south west,font=\small] at (-1,{\base+2.22}){$\label$};
\node[font=\small] at (5.1,{\base-.35}){$x$ (USD)};
}
\foreach \a/\m in {0/.15,2/.60,4/.25}{\draw[cTwoMassColor,thick] (\a,0)--(\a,{2*\m});\fill[cTwoMassColor] (\a,{2*\m}) circle[radius=1.5pt];}
\node[font=\small,anchor=west] at (0,4.95){$F_X(a)-F_X(a^-)=p_X(a)$};
\visible<2->{\draw[cTwoCDFColor,thick,<-] (-1,2.55)--(0,2.55);}
'''
for a,m,b,start,place in [(0,.15,0,3,12),(2,.60,.15,13,22),(4,.25,.75,23,32)]:
    stack+=f'% a={a}: mass {m:.2f}, upper jump {b:.2f} to {b+m:.2f}; motion includes full panel gap.\n'
    for k in range(9):
        shift=(2.55+2*b)*k/8
        stack+=rf'\only<{start+k}>{{\draw[cTwoGuideColor,densely dashed,line width=.9pt] ({a},{shift:.6f})--({a},{shift+2*m:.6f});}}'+'\n'
    stack+=rf'\visible<{place}->{{\draw[cTwoGuideColor,densely dashed,line width=.9pt] ({a},{2.55+2*b:.6f})--({a},{2.55+2*(b+m):.6f});}}'+'\n'
    right={0:2,2:4,4:5.3}[a]; y=2.55+2*(b+m)
    stack+=rf'\visible<{place}->{{\draw[cTwoCDFColor,thick'+(',->' if a==4 else '')+rf'] ({a},{y:.6f})--({right},{y:.6f});}}'+'\n'
stack+=r'% Markers are painted last, above moving/placed dashed stems.'+'\n'+r'\visible<2->{\draw[cTwoCDFColor,fill=white,thick] (0,2.55) circle[radius=2pt];}'+'\n'
for a,y,n in [(0,2.85,12),(2,4.05,22),(4,4.55,32)]:
    stack+=rf'\visible<{n}->{{\fill[cTwoCDFColor] ({a},{y}) circle[radius=2pt];}}'+'\n'
for a,y,n in [(2,2.85,12),(4,4.05,22)]:
    stack+=rf'\visible<{n}->{{\draw[cTwoCDFColor,fill=white,thick] ({a},{y}) circle[radius=2pt];}}'+'\n'
stack+=r'''\node[font=\small,anchor=west] at (-.7,-.78){\textcolor{cTwoMassColor}{PMF stems}\quad\textcolor{cTwoGuideColor}{Dashed: translated masses}\quad\textcolor{cTwoCDFColor}{CDF steps}};
\end{pgfinterruptboundingbox}
\end{tikzpicture}
\end{frame}
\end{document}
'''
s=s[:cut]+stack
s=s.replace('panel separation (2.8 cm)','panel separation (2.55 cm)')
p.write_text(s,encoding='utf-8')

