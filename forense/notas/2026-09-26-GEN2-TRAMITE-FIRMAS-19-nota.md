# Nota · ACTO GEN2-TRAMITE-FIRMAS-19 · 26/sep/2026

Contadores movidos: cero mediciones. `adoptados` se mueve cuando GEN2-CATALOGO-V1-2-1 y el marcador consuman estas firmas.

ARRANQUE: clon `/home/user/Modelado-Mexicano`, base `aa36232a` = SHA de redacción (0 detrás de origin/main). ENTORNO-DERIVADO = NUBE (hook), red DENEGADA-POR-POLÍTICA, corpus montado = NO (0 archivos examinados); el acto no toca microdato ni red. 0-bis `901269fa`, raíz `9012`. §4: `grep -c 'FIRMAS-19' forense/firmas-pendientes.tsv` → 0 antes del acto.

## Premisas re-verificadas
- [EJECUTADO] 14 FP ABIERTA a `aa36232a`: COINCIDE (lector CSV, estado=ABIERTA → 14).
- Las diez FP leídas enteras; recomendación del ejecutor = opción de §1 en las diez.
- Discrepancia menor (cláusula 1): J10 dice «evidencia (a) o (b) según la FP»; la FP 2a0e-03 ya rotula evidencia (a). Se sigue la FP.

## Firma
§2: «El lanzamiento es la constancia». La hoja llegó lanzada sin corrección por letra → «firmo» a las diez con la recomendación (INTERPRETACIÓN-DECLARADA, cláusula 2).

## P1 · filas
Diez FP → FIRMADA, `firmada_en` con el texto de §1 rellenado por fila, `ejecutada_en` = ADR + `EJECUTA: GEN2-CATALOGO-V1-2-1`.

## P2 · J3
Universo derivado por comando sobre `data/corrida0/CALC-ENIGH-CONSUMO-PISOS-0001/resultados.json` (23 100 RESULT):
`jq -r '.resultados|keys[]' | grep -E 'PART-EFECTIVO-EN-GASTO-DIRECTO|PART-CANAL-|HOG-COMPRA-FIADO|HOG-COMPRA-TARJETA-CREDITO|HOG-COMPRA-INTERNET' | grep -E -- '-20(16|18)-|TAU2|N-DELTAS|-ICC-'` → 4516 ids (3640 de olas 2016/2018 + 876 TAU2/N-DELTAS/ICC que las consumen).
Los 4516 ids existen idénticos en -0002 (4516/4516). Por eso la llave en `decisiones.tsv` es `CALC-ENIGH-CONSUMO-PISOS-0001/<RESULT>`: una llave pelada vetaría también el piso que rige (INTERPRETACIÓN-DECLARADA; el consumidor —CATALOGO-V1-2-1— lee el prefijo). El -0001 no se reescribe.

## P3 · NC
NC-260925-GEN2-FAMILIA-CUIDADOS-Y-MIGRACION-PISOS-1-2a0e-06 (DECISIÓN-DE-MESA-PENDIENTE sobre 2a0e-01..03) → CERRADA. Las unidades CONSUMO y CONFIANZA no dejaron NC de decisión pendiente sobre estas FP (2d37-08 es edición del manifiesto, no se toca).

## K
3d56-01, 4296-01, c3fa-05, 43d6-01: sin cambio.

## Defecto adyacente (D-21, declarado; `tools/corrida0.py` fuera de §9)
CI del PR #1158: `suite` cancelada a los 10 min en T32 (T-CORRIDA0). Causa: `corrida0.py` releía `decisiones.tsv` completo por objeto (`_firma_de_decision` dentro de un bucle sobre decisiones: cuadrático) y por RESULT (`_lee_decisiones` desde `_lee_oferta`); con las 4516 filas de J3 dejó de terminar. Arreglo (≤10 líneas por sitio): mapa objeto→firma leído una vez, y caché de `_lee_decisiones` por (ruta, mtime, tamaño). Tras el arreglo, `corrida0.py status` termina en 38 s; `check.py --baseline` → «LÍNEA BASE: VERDE — sin FAIL nuevos» (3 FAIL heredados T06/T08).
