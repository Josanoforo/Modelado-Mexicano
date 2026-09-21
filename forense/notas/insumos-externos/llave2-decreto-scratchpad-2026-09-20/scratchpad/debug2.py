with open('canon/gobernanza-v1_15.md', encoding='utf-8') as f:
    content = f.read()

old_cascada = ("**Cascada.** Candidateó `ADR-166` contra el máximo verificado por "
    "`grep -oE '^\\*\\*ADR-[0-9]+' canon/gobernanza-v1_15.md | sort -t- -k2 -n -u | tail -1` "
    "sobre `origin/main` re-fetched antes de commitear (`164`, `ADR-164`/`ACTO SELLA-AGO25-E`, "
    "ya fusionado): único `166`, sin huecos → `166`, a re-verificar por quien fusione. "
    "`canon/estado-programa-v1_10.md`: conteo de ADR recifrado (`164→165`). "
    "`forense/registro-llaves-identificacion-v1_0.md`: fila nueva, contador `3 de 4`→`4 de 5`. "
    "`forense/firmas-pendientes.tsv`: `FP-109` recibe `ejecutada_en`; fila nueva `FP-135`, `ABIERTA`.")
print("old_cascada found:", content.count(old_cascada))

old_sentence = ", 0 de 37 necesidades) — el efecto queda `PROPUESTO`, fila `FP-135` nueva para que mesa firme su destino."
print("old_sentence found:", content.count(old_sentence))
