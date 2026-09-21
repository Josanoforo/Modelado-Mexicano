with open('canon/gobernanza-v1_15.md', encoding='utf-8') as f:
    content = f.read()

start = content.find("**ADR-166 · `ACTO LLAVE2-DECRETO`")
end_marker = "→ **PRIMER `EJERCIDA_REFUTA` DEL PROGRAMA · EL PAQUETE FRONTERIZO 2019 NO MOVIÓ INGRESO NI INFORMALIDAD EN LOS MUNICIPIOS TRATADOS.** *(`ACTO LLAVE2-DECRETO`, 25/ago/2026. Entorno **UBUNTU**. Candidateó `ADR-166` contra `origin/main` re-fetched; por quien fusione. Detalle completo: `forense/notas/2026-08-25-llave2-decreto-cierre.md`.)*"
end = content.find(end_marker)
assert start != -1 and end != -1
end_full = end + len(end_marker)
block = content[start:end_full]

old_cascada = ("**Cascada.** Candidateó `ADR-166` contra el máximo verificado por "
    "`grep -oE '^\\*\\*ADR-[0-9]+' canon/gobernanza-v1_15.md | sort -t- -k2 -n -u | tail -1` "
    "sobre `origin/main` re-fetched antes de commitear (`164`, `ADR-164`/`ACTO SELLA-AGO25-E`, "
    "ya fusionado): único `166`, sin huecos → `166`, a re-verificar por quien fusione. "
    "`canon/estado-programa-v1_10.md`: conteo de ADR recifrado (`164→165`). "
    "`forense/registro-llaves-identificacion-v1_0.md`: fila nueva, contador `3 de 4`→`4 de 5`. "
    "`forense/firmas-pendientes.tsv`: `FP-109` recibe `ejecutada_en`; fila nueva `FP-135`, `ABIERTA`.")
assert block.count(old_cascada) == 1

new_cascada = ("**Cascada.** Candidateó `ADR-165` contra el máximo verificado por "
    "`grep -oE '^\\*\\*ADR-[0-9]+' canon/gobernanza-v1_15.md | sort -t- -k2 -n -u | tail -1` "
    "sobre `origin/main` re-fetched antes de commitear (`164`, `ADR-164`/`ACTO SELLA-AGO25-E`, "
    "ya fusionado): único `165`, sin huecos — **renumerado a `ADR-166` al fusionar**, colisión "
    "con `ADR-165`/`ACTO U2-CRUCE` (`PR #335`), regla de la casa: renumera quien fusiona "
    "segundo. Re-verificado sobre el árbol fusionado: máximo `165`, único `166`, sin huecos. "
    "`canon/estado-programa-v1_10.md`: conteo de ADR recifrado (`165→166`). "
    "`forense/registro-llaves-identificacion-v1_0.md`: fila nueva, contador `3 de 4`→`4 de 5`. "
    "`forense/firmas-pendientes.tsv`: `FP-109` recibe `ejecutada_en`; fila nueva `FP-136` "
    "(renumerada de `FP-135`, colisión con `ACTO U2-CRUCE`), `ABIERTA`.")

block2 = block.replace(old_cascada, new_cascada)
block2 = block2.replace(
    ", 0 de 37 necesidades) — el efecto queda `PROPUESTO`, fila `FP-135` nueva para que mesa firme su destino.",
    ", 0 de 37 necesidades) — el efecto queda `PROPUESTO`, fila `FP-136` nueva para que mesa firme su destino."
)
assert block2 != block
assert 'FP-135' not in block2, "still has FP-135"

new_content = content[:start] + block2 + content[end_full:]
with open('canon/gobernanza-v1_15.md', 'w', encoding='utf-8') as f:
    f.write(new_content)

assert new_content.count('FP-135') == 4, new_content.count('FP-135')  # only U2-CRUCE's legit ones
print("OK")
