from pathlib import Path
import re,difflib
old=Path('tmp/c3-compact/original.tex').read_text(); new=Path('book2026-2027/grade11/term_2/2-class_activities/G11_T2_L1_C3_classroom_activity.tex').read_text()
print('Solutions source unchanged:', old.split('\\restoregeometry',1)[1]==new.split('\\restoregeometry',1)[1])
print('All inline mathematics unchanged:', re.findall(r'(?<!\\)\$(.*?)(?<!\\)\$',old,re.S)==re.findall(r'(?<!\\)\$(.*?)(?<!\\)\$',new,re.S))
print('All plots unchanged:',re.findall(r'\\addplot.*?;',old,re.S)==re.findall(r'\\addplot.*?;',new,re.S))
print('All point/linear labels unchanged:',re.findall(r'\\(?:PointLabel|LinearGuideLabel).*?\n',old)==re.findall(r'\\(?:PointLabel|LinearGuideLabel).*?\n',new))
print('Five section titles unchanged:',re.findall(r'\\stageheading\{(.*?)\}',old)==re.findall(r'\\stageheading\{(.*?)\}',new))
Path('tmp/c3-compact/layout-final.diff').write_text(''.join(difflib.unified_diff(old.splitlines(True),new.splitlines(True))),encoding='utf-8')
