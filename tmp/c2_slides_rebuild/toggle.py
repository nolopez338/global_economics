from pathlib import Path
s=Path('tmp/c2_slides_rebuild/next.tex').read_text(encoding='utf8').replace('[12pt,aspectratio=169]','[handout,12pt,aspectratio=169]')
Path('tmp/c2_slides_rebuild/enabled_check.tex').write_text(s,encoding='utf8')
Path('tmp/c2_slides_rebuild/disabled_check.tex').write_text(s.replace('% \\GTenHighlightsfalse % Uncomment','\\GTenHighlightsfalse % Uncomment'),encoding='utf8')
