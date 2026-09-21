with open('scratchpad/conflict_origin.txt', encoding='utf-8') as f:
    origin_part = f.read()

old_header = ("**L0 · Gobierno — completo y al día.** 165 ADR, protocolo de cambio con "
              "retropropagación bidireccional, severidades S1-S5, casillero de pendientes "
              "irresueltos. *(Recifrado 164→165, `ACTO U2-CRUCE`,")
assert origin_part.count(old_header) == 1, origin_part.count(old_header)

mine = ("*(Recifrado 165→166, `ACTO LLAVE2-DECRETO`, 25/ago/2026: `ADR-166` pre-registra y "
        "corre un DiD sobre `ENOE` con el decreto de la Región Fronteriza Norte (2019) como "
        "corte natural, llave (ii) de `ADR-57(c)`, ejecutando `FP-109` opción (a). Firma "
        "`EJERCIDA_REFUTA` — ni el ingreso real por hora ni la informalidad se movieron en "
        "los 34/43 municipios tratados con muestra, `2017`–`2020T4`; primer `EJERCIDA_REFUTA` "
        "de `registro-llaves-identificacion`. `FP-109` recibe `ejecutada_en`; nace `FP-136` "
        "(renumerada de `FP-135` por colisión con `ACTO U2-CRUCE`, `PR #335`, fusionado "
        "primero — regla de la casa, renumera quien fusiona segundo). Candidateado contra el "
        "máximo verificado por `grep` sobre `origin/main` re-fetched tras el merge (`165`, "
        "`ADR-165`/`ACTO U2-CRUCE`, ya fusionado): único `166`, sin huecos. `gobernanza` "
        "(cabecera) y `estado` (cabecera y aquí) citan 166.)* ")

new_header = ("**L0 · Gobierno — completo y al día.** 166 ADR, protocolo de cambio con "
              "retropropagación bidireccional, severidades S1-S5, casillero de pendientes "
              "irresueltos. " + mine + "*(Recifrado 164→165, `ACTO U2-CRUCE`,")

resolved = origin_part.replace(old_header, new_header)
assert resolved != origin_part

with open('canon/estado-programa-v1_10.md', encoding='utf-8') as f:
    content = f.read()

start = content.find('<<<<<<< HEAD')
end_marker = content.find('>>>>>>> origin/main')
end = end_marker + len('>>>>>>> origin/main')

new_content = content[:start] + resolved + content[end:]
with open('canon/estado-programa-v1_10.md', 'w', encoding='utf-8') as f:
    f.write(new_content)
print("OK, no more conflict markers:", '<<<<<<<' not in new_content)
