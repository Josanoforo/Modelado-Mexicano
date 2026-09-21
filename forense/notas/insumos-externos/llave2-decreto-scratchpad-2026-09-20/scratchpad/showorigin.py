import subprocess
content = subprocess.run(['git','show','origin/main:canon/estado-programa-v1_10.md'],
                          capture_output=True, text=True, encoding='utf-8').stdout
idx = content.find('164 ADR')
print("--- L0 header + first entries (origin/main) ---")
print(content[idx-40:idx+1200])
print()
idx2 = content.find('Validaciones externas materiales')
print("--- Validaciones externas materiales section (origin/main) ---")
print(content[idx2-40:idx2+1600])
