import re
with open('canon/estado-programa-v1_10.md', encoding='utf-8') as f:
    for i, l in enumerate(f, 1):
        for m in re.finditer(r'164\s*`?\s*ADR', l):
            print(i, repr(l[max(0,m.start()-80):m.start()+80]))
