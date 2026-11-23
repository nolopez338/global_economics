from pathlib import Path
import hashlib
root=Path('tmp/solution-context-review')
changed=[]
for i in range(2,36):
 a=(root/'verified-render'/f'page-{i:03}.png').read_bytes()
 b=(root/'ready-render'/f'page-{i:03}.png').read_bytes()
 if a!=b: changed.append(i)
assert not changed,changed
print('Pages 2-35 match the inspected renders exactly; restored contents page inspected separately.')
