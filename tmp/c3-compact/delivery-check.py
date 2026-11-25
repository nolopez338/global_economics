from pathlib import Path
p=Path('book2026-2027/grade11/term_2/2-class_activities/G11_T2_L1_C3_classroom_activity.tex')
a=p.read_text(); preview=Path('tmp/c3-compact/preview.tex').read_text(); original=Path('tmp/c3-compact/original.tex').read_text()
assert a.split('\\restoregeometry',1)[0]+'\\end{document}'==preview
assert a.split('\\restoregeometry',1)[1]==original.split('\\restoregeometry',1)[1]
print('Delivered source still matches inspected build input; appended Solutions source unchanged.')
