with open('canon/gobernanza-v1_15.md', encoding='utf-8') as f:
    content = f.read()
start = content.find("**ADR-166 · `ACTO LLAVE2-DECRETO`")
end = content.find("---", content.find("→ **PRIMER `EJERCIDA_REFUTA` DEL PROGRAMA"))
block = content[start:end]
import re
for m in re.finditer(r'FP-135', block):
    print(repr(block[max(0,m.start()-80):m.start()+40]))
