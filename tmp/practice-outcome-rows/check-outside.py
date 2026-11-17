from pathlib import Path
import difflib
ns={}
exec(Path('tmp/practice-outcome-rows/check.py').read_text().split('assert strip(a)')[0],ns)
print(''.join(difflib.unified_diff(ns['strip'](ns['b']).splitlines(True),ns['strip'](ns['a']).splitlines(True))))
