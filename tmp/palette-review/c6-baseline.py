from pathlib import Path
r=Path.cwd();p=r/'book2026-2027/grade10/term_2/1-practice_activities/G10_T2_L2_C6_practice_activity.tex';s=p.read_text();s=s.replace(r'\input{graphs/specific_highlights.tex}',r'\input{C:/Users/orlan/Desktop/SanBartolo/global_economics/tmp/palette-review/original-specific_highlights.tex}');(r/'tmp/palette-review/c6-baseline.tex').write_text(s)
