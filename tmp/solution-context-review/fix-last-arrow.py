from pathlib import Path
p=Path('book2026-2027/grade11/term_2/4-learning_evidences/G11_T2_L1_C1C2_exam_solution.tex')
s=p.read_text(encoding='utf-8')
a=s.index(r'\worked{C2 Task 1 \score{1}}{sol:p2c2a}'); b=s.index(r'\secInicio',a)
t=s[a:b].replace('established by the population investigation; unavailable for initial estimation.','established later by the population investigation.')
x=t.index('Use the initial sample only for estimation.')
t=t[:x]+r'Use only the initial sample for estimation; the comparison sample describes variation, and the later mean supports retrospective assessment. Use known $\CtwoSD{\sigma}=\CtwoSD{36}$, rather than $\SSD{s_A}=\SSD{33}$ or $\SSD{s_B}=\SSD{39}$. Random sampling, the stated regularity assumption and negligible sample fraction support the normal approximation.'+'\n\n'
s=s[:a]+t+s[b:]
p.write_text(s,encoding='utf-8')
