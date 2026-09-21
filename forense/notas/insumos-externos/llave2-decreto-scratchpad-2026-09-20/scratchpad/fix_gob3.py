with open('canon/gobernanza-v1_15.md', encoding='utf-8') as f:
    content = f.read()

start = content.find("**ADR-166 · `ACTO LLAVE2-DECRETO`")
end_marker = "→ **PRIMER `EJERCIDA_REFUTA` DEL PROGRAMA · EL PAQUETE FRONTERIZO 2019 NO MOVIÓ INGRESO NI INFORMALIDAD EN LOS MUNICIPIOS TRATADOS.** *(`ACTO LLAVE2-DECRETO`, 25/ago/2026. Entorno **UBUNTU**. Candidateó `ADR-166` contra `origin/main` re-fetched; por quien fusione. Detalle completo: `forense/notas/2026-08-25-llave2-decreto-cierre.md`.)*"
end = content.find(end_marker)
end_full = end + len(end_marker)
print("start", start, "end_full", end_full)

old_cascada = ("**Cascada.** Candidateó `ADR-166` contra el máximo verificado por "
    "`grep -oE '^\\*\\*ADR-[0-9]+' canon/gobernanza-v1_15.md | sort -t- -k2 -n -u | tail -1` "
    "sobre `origin/main` re-fetched antes de commitear (`164`, `ADR-164`/`ACTO SELLA-AGO25-E`, "
    "ya fusionado): único `166`, sin huecos → `166`, a re-verificar por quien fusione. "
    "`canon/estado-programa-v1_10.md`: conteo de ADR recifrado (`164→165`). "
    "`forense/registro-llaves-identificacion-v1_0.md`: fila nueva, contador `3 de 4`→`4 de 5`. "
    "`forense/firmas-pendientes.tsv`: `FP-109` recibe `ejecutada_en`; fila nueva `FP-135`, `ABIERTA`.")
idx_cascada = content.find(old_cascada)
print("cascada within block range?", start <= idx_cascada <= end_full, idx_cascada)

old_sentence = ", 0 de 37 necesidades) — el efecto queda `PROPUESTO`, fila `FP-135` nueva para que mesa firme su destino."
idx_sentence = content.find(old_sentence)
print("sentence within block range?", start <= idx_sentence <= end_full, idx_sentence)
