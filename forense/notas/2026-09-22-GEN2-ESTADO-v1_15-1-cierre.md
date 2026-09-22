# Cierre · ACTO GEN2-ESTADO-v1_15-1

Retrata el estado del programa del 18–22/sep en `canon/estado-programa-v1_15.md`: cabecera nueva + §0–§13 heredadas verbatim de `v1_14` (diff vacío) + §14 nueva, con status íntegro de `corrida0.py`, 24 filas en la tabla afirmación→comando (mínimo 20) y 4 puntos `NO-DERIVADO`. `v1_14` retirada por T01.

Premisas de dirección (§3 del encargo) verificadas contra el árbol de hoy (`02eda84`, no la cabecera `ccd7c0eb`): status dígito a dígito igual salvo `no_corrido_abiertas` 212→213 (declarado, no PARO). Pilotos, duelos, marginales y `celdas_validadas` re-verificados por objeto: ningún veredicto cambió.

Hallazgo declarado: `celdas_validadas` (92) = `cruce_vs_R` (35) + `persistencia` (57); `duelo_tres_nacional` (12) es clase informativa aparte, no sumada — la lectura ingenua 35+57+12=104 es un error de quien no lee la fuente.

Suite: `python3 tests/check.py --rapido` → VERDE, 0 FAIL (tras corregir dos hallazgos propios de T15 y uno de T25, todos declarados en el ADR de cierre).

Perímetro respetado. Cero microdato, cero contadores del programa movidos (`cuenta_gen2 = NO-APLICA`).
