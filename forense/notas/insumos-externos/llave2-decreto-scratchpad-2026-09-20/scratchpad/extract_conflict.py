with open('canon/estado-programa-v1_10.md', encoding='utf-8') as f:
    content = f.read()

start = content.find('<<<<<<< HEAD')
mid = content.find('=======\n', start)
end_marker = content.find('>>>>>>> origin/main', mid)
end = end_marker + len('>>>>>>> origin/main')

head_part = content[start+len('<<<<<<< HEAD\n'):mid]
origin_part = content[mid+len('=======\n'):end_marker]

print("HEAD part length:", len(head_part))
print("ORIGIN part length:", len(origin_part))

with open('scratchpad/conflict_head.txt', 'w', encoding='utf-8') as f:
    f.write(head_part)
with open('scratchpad/conflict_origin.txt', 'w', encoding='utf-8') as f:
    f.write(origin_part)

print("pre-conflict tail:", repr(content[start-80:start]))
print("post-conflict head:", repr(content[end:end+80]))
