from pathlib import Path
p=Path('book2026-2027/grade11/term_2/1-practice_activities/G11_T2_L2_C6_practice.tex');s=p.read_text()
a=s.index('\\SectionProblemsTableOfContents{',s.index('\\section{General Worked Problems}'))
b=s.index('After the explicit SE formulas',a)
s=s[:a]+r'''Choose a question type: \hyperref[prob:t1]{standard error},
\hyperref[prob:t2]{margin of error}, \hyperref[prob:t3]{total width}, or
\hyperref[prob:t4]{confidence with fixed precision}.

'''+s[b:]
s=s.replace(r'\IntroOne\IntroTwo $\HLConfidence{0.95}$ corresponds to $\HLConfidence{95\%}$.',r'\IntroOne $\HLConfidence{95\%}$ confidence.\par\IntroTwo $\HLConfidence{0.95}$ as a proportion.')
s=s.replace(r'\IntroOne\IntroTwo At 95\%, $\HLCriticalValue{z^*}\approx\HLCriticalValue{1.95996398454}$.',r'\IntroOne The 95\% multiplier.\par\IntroTwo The same multiplier, $\HLCriticalValue{z^*}\approx\HLCriticalValue{1.95996398454}$.')
p.write_text(s)
