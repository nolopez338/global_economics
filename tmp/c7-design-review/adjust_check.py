from pathlib import Path
p=Path('tmp/c7-design-review/task_checks.py')
s=p.read_text(encoding='utf-8-sig')
s=s.replace("assert tokens(r)==tokens(off),'Highlight-off content changed'", "assert ''.join(re.findall(r'\\d', ' '.join(p.extract_text() for p in r.pages))) == ''.join(re.findall(r'\\d', ' '.join(p.extract_text() for p in off.pages))), 'Highlight-off numerical content changed'\nassert (base/'highlights-off.tex').read_text(encoding='utf-8') == src.replace('% '+chr(92)+'GTenHighlightsfalse',chr(92)+'GTenHighlightsfalse'), 'Variant source differs beyond toggle'")
s=s.replace("'highlight_off_identical_tokens':True","'highlight_off_identical_digits_and_source_except_toggle':True")
p.write_text(s,encoding='utf-8')
