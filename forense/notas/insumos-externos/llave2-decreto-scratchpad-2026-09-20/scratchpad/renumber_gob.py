with open('canon/gobernanza-v1_15.md', encoding='utf-8') as f:
    content = f.read()

start_marker = "**ADR-165 · `ACTO LLAVE2-DECRETO`"
end_marker = "→ **PRIMER `EJERCIDA_REFUTA` DEL PROGRAMA · EL PAQUETE FRONTERIZO 2019 NO MOVIÓ INGRESO NI INFORMALIDAD EN LOS MUNICIPIOS TRATADOS.** *(`ACTO LLAVE2-DECRETO`, 25/ago/2026. Entorno **UBUNTU**. Candidateó `ADR-165` contra `origin/main` re-fetched; por quien fusione. Detalle completo: `forense/notas/2026-08-25-llave2-decreto-cierre.md`.)*"

start = content.find(start_marker)
end = content.find(end_marker)
assert start != -1 and end != -1
end_full = end + len(end_marker)

block = content[start:end_full]
print("block length:", len(block))
print("occurrences of '165' in block:", block.count('165'))

new_block = block.replace('ADR-165', 'ADR-166').replace('`165`', '`166`')
# the summary line's "Candidateó `ADR-165`" also needs updating -- already covered by ADR-165->166 replace
print("occurrences of 'ADR-165' remaining after replace:", new_block.count('ADR-165'))
print("occurrences of 'ADR-166':", new_block.count('ADR-166'))

new_content = content[:start] + new_block + content[end_full:]
with open('canon/gobernanza-v1_15.md', 'w', encoding='utf-8') as f:
    f.write(new_content)

# sanity: U2-CRUCE's block still intact
assert new_content.count('**ADR-165 · `ACTO U2-CRUCE`') == 1
assert new_content.count('**ADR-166 · `ACTO LLAVE2-DECRETO`') == 1
print("OK")
