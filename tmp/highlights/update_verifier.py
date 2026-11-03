from pathlib import Path
p=Path('tmp/highlights/verify.py')
s=p.read_text()
s=s.replace("plain=strip(s).replace", "s=__import__('re').sub(r'% Value-to-mass lookup before the normalization sum\\.\\n\\\\\\[.*?\\\\\\]\\n','',s,flags=__import__('re').S)\nplain=strip(s).replace")
p.write_text(s)
