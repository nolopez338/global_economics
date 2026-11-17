from pathlib import Path
p=Path('book2026-2027/grade10/term_2/2-class_activities/G10_T2_L1_C2_classroom_activity.tex')
s=p.read_text(); o=Path('tmp/c2-solutions/original.tex').read_text()
a=s.split('\n\\ifprintsolutions\n')[0].replace('\\printsolutionstrue % Set \\printsolutionsfalse for the original student-only handout.','\\printsolutionsfalse % Set \\printsolutionstrue to append the complete review solutions.').replace('Disable instructional highlights on all student pages.','Disable instructional highlights throughout this activity.')
assert a==o.split('\n\\ifprintsolutions\n')[0]
Path('tmp/c2-solutions/student.tex').write_text(s.replace('\\printsolutionstrue % Set','\\printsolutionsfalse % Set',1))
print('Student source unchanged, except toggle and comment.')
