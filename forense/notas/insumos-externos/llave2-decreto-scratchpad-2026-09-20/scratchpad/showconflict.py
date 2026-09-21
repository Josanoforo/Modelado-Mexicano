with open('canon/estado-programa-v1_10.md', encoding='utf-8') as f:
    content = f.read()
for marker in ['<<<<<<< HEAD', '=======', '>>>>>>> origin/main']:
    idx = content.find(marker)
    print(f"--- {marker} at char {idx} ---")
    print(repr(content[max(0,idx-200):idx+250]))
    print()
