with open('forense/firmas-pendientes.tsv', encoding='utf-8') as f:
    lines = f.readlines()

assert lines[136] == '<<<<<<< HEAD\n'
assert lines[138] == '=======\n'
assert lines[140] == '>>>>>>> origin/main\n'

mine_line = lines[137]
origin_line = lines[139]
assert mine_line.startswith('FP-135\t')
assert origin_line.startswith('FP-135\t')

mine_renumbered = mine_line.replace('FP-135', 'FP-136', 1)
# also fix the internal self-reference the row makes to its own id, if any further occurrence
# (check for a second FP-135 inside the row text itself, e.g. self-citation)
extra = mine_renumbered.count('FP-135')
print("extra internal FP-135 mentions in my row after first replace:", extra)

new_lines = lines[:136] + [origin_line, mine_renumbered] + lines[141:]
with open('forense/firmas-pendientes.tsv', 'w', encoding='utf-8') as f:
    f.writelines(new_lines)
print("OK, total lines:", len(new_lines))
