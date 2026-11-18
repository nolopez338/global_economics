from pathlib import Path
p=Path('book2026-2027/grade10/term_2/2-class_activities/G10_T2_L1_C1_classroom_activity.tex')
s=p.read_text(encoding='utf-8'); p.write_bytes(s.replace('\n','\r\n').encode('utf-8'))
a=Path('tmp/c1_classroom_layout/original.tex').read_bytes(); b=p.read_bytes(); mark=b'\\ifprintsolutions\r\n\\clearpage'
assert a.split(mark)[0]==b.split(mark)[0]
assert a[a.rindex(b'\\fi'):]==b[b.rindex(b'\\fi'):]
print('Content outside solutions is byte-for-byte unchanged, including line endings.')
