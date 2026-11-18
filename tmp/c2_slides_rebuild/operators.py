from pathlib import Path
p=Path('book2026-2027/grade11/term_2/3-slides/G11_T2_L1_C2_slides.tex')
s=p.read_text(encoding='utf8').replace(r'\seq_map_inline:Nn \l_tmpa_seq {\At{#1}{#2}{##1}\space}',r'\seq_map_inline:Nn \l_tmpa_seq {\str_if_eq:nnTF {##1}{=} {=}{\At{#1}{#2}{##1}}\space}')
p.write_text(s,encoding='utf8')
Path('tmp/c2_slides_rebuild/next.tex').write_text(s,encoding='utf8')
