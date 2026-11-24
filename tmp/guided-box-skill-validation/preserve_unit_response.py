from pathlib import Path
p=Path('.agents/skills/global-economics-classroom-activity/assets/template_classroom_activity.tex')
s=p.read_text(encoding='utf-8').replace('$a$ & First quantity & 15 units.\\par', '$a$ & First quantity & 15 \\guidedresponsebox{18mm}.\\par')
p.write_text(s,encoding='utf-8')
