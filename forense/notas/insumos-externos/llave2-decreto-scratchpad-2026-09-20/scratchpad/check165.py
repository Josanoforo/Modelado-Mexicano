with open('canon/gobernanza-v1_15.md', encoding='utf-8') as f:
    content = f.read()
start = content.find("**ADR-166 · `ACTO LLAVE2-DECRETO`")
end = content.find("→ **PRIMER `EJERCIDA_REFUTA` DEL PROGRAMA")
end_full = content.find("*)", end) + 2
block = content[start:end_full+50]
import re
for m in re.finditer(r'165', block):
    print(repr(block[max(0,m.start()-40):m.start()+40]))
