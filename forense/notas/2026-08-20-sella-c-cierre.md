# Nota de cierre — `ACTO SELLA-C`, 20/ago/2026

**Entorno:** NUBE, repo-only, sin sonda de red de datos. `data/raw` no se usó (este acto no la toca).
**SHA de arranque:** rama `claude/adv1-m6-rewrite-amendments-bykxjf`, working tree limpio al arrancar.

## Mandato

Gate `FP-91`, firma de mesa de `SELLA-C`, verbatim: **«C: 2 mueren y ADV1-M6 se reescribe»**. `FP-91` registraba tres textos vigentes con tres lecturas distintas del criterio de cierre de `PILOTO-E1E3 T4` — los siete umbrales de `ADR-68(c)` (`ADR-128(b)`, `VENCIDO EN ALCANCE` salvo el umbral (1)), `ADV1-M6` («de los 7 umbrales, ≥3 de resultado»), y `PLAN-CALCULO-TOTAL` OLA 4 («7 umbrales por comando → GO/NO-GO»). La firma «C» adjudica: los siete umbrales mueren (ya vencidos, no repetido aquí) y `ADV1-M6` se reescribe.

## Verificación de existencia, antes de escribir

- `forense/CAREO-ADV-DUELO-diseno-v2-2026-08-19.md:44` — confirmado por lectura completa del §B: la línea `ADV1-M6` dice exactamente *"GO con dientes. De los 7 umbrales, ≥3 de resultado: cuotas de ADV1-M1 cumplidas por comando (P2, CV, sondas corridas) · cobertura de intervalos de M ≥60% de celdas puntuadas · M>B en ≥2/3 de celdas puntuadas. Al menos un umbral lo determina la naturaleza, no el equipo."* Los tres criterios de resultado citados por la tarea coinciden exactamente con esta línea — no hizo falta reinterpretarlos.
- Los seis sitios de enmienda (`PLAN-CALCULO-TOTAL-v1_1.md:40,62,67`; `APERTURA-FASE-CALCULO-v1_2.md:17,25,41`) se localizaron por contenido citado, no ciegamente por número de línea — los seis coincidieron exactamente con los números de línea reales del árbol al momento de escribir. Ninguno resultó `NO-ENCONTRADO`.
- `forense/firmas-pendientes.tsv`: `FP-91` confirmada `ABIERTA` antes de este acto (`grep`, línea 92).
- ADR máximo re-verificado: `grep -oE 'ADR-[0-9]+' canon/gobernanza-v1_15.md | sort -t- -k2 -n -u | tail -1` → `137`, único, sin huecos → candidato `ADR-138`.
- FP máximo re-verificado: `grep -oE 'FP-[0-9]+' forense/firmas-pendientes.tsv | sort -t- -k2 -n -u | tail -1` → `102` — sin filas nuevas necesarias, solo el cierre de `FP-91`.

## Patrón `ADV1-M5`→`ADV1-M5 v2` (`ADR-136`) replicado

`forense/adv-duelo/ADV1-M6-v2-2026-08-20.md`: capa nueva, párrafo original del careo (`:44`) intacto — verificado con `git diff` que `forense/CAREO-ADV-DUELO-diseno-v2-2026-08-19.md` no aparece en el diff de este acto. Los tres criterios de resultado se presentan como conjunto completo, no como subconjunto de siete, con la lógica: el universo de siete ya está `VENCIDO EN ALCANCE` (`ADR-128(b)`), así que "≥3 de 7" pierde su denominador vivo.

## `T25` (`T-ROTULOS`) — rótulo pelado, corregido sin tocar `tests/`

La primera redacción del documento nuevo y del encargo traía los tres rótulos del mecanismo sin el prefijo `ADV1-` en varias citas — disparó `T25` en corridas sucesivas, una vez por cada rótulo distinto. Corregido reescribiendo cada mención propia con el prefijo `ADV1-` (doctrina `D-6`, `ADR-128(e)`), preservando la única cita verbatim del careo (que empieza tras "GO con dientes" para no reproducir el rótulo pelado del título de la fuente) — perímetro respetado: `tests/check.py` **no se tocó**, ninguna entrada nueva en `_T25_ARCHIVOS_CONOCIDOS`.

## Tabla de entregables

| Tarea | Entregable | Resultado |
|---|---|---|
| T1 | `forense/adv-duelo/ADV1-M6-v2-2026-08-20.md` (nuevo) | Capa nueva sobre `ADV1-M6`, tres criterios como conjunto completo, careo intacto |
| T2 | Enmiendas in situ, 20/ago/2026, en `PLAN-CALCULO-TOTAL-v1_1.md:40,62,67` y `APERTURA-FASE-CALCULO-v1_2.md:17,25,41` | Seis sitios localizados y enmendados; cero `NO-ENCONTRADO`; texto original intacto en los seis |
| T3 | Cláusula de compuerta, sellada en `ADR-138(c)` | El `GO` de `ADV1-M6 v2` ocupa el lugar reservado a los siete umbrales — nueva compuerta formal de apertura de la fase de cálculo |
| T4 | `ADR-138` (`canon/gobernanza-v1_15.md`) · `FP-91` → `FIRMADA` (`forense/firmas-pendientes.tsv`) · `forense/hallazgos.md` (una línea) · `canon/estado-programa-v1_10.md` (cascada `137→138` ADR, `142→141` WARN) · `forense/encargos/2026-08-20-SELLA-C.md` (`CONSUMIDO`) · esta nota | Cerrado |

## Fila `ABIERTA` nueva — evaluación

**No se agregó ninguna.** T1-T3 no dejaron nada pendiente que un archivo del perímetro de este acto pueda nombrar sin inventar: el único punto declarado como pendiente — cuál de los tres criterios "lo determina la naturaleza" (`ADV1-M6 v2 §2`) — no es una decisión de mesa gateada, es una derivación que el piloto produce cuando corra, exactamente como `ADV1-M4` ya trata la lectura (5) del duelo. No hay contradicción nueva, ni criterio sin resolver, ni acto sucesor bloqueado por falta de firma: `FP-91` cierra limpio.

## Contador

Medición sobre México movida por este acto: **cero**, dicho (`v2.3`). Este acto adjudica un criterio de cierre y enmienda cuatro documentos; no calcula ningún β ni ninguna θ ni corre ninguna celda-D.

## Línea base

```
19 FAIL · 141 WARN
LÍNEA BASE: VERDE — nada nuevo frente a tests/baseline.json (HEAD congelado e24d033ed3c095f1e81c2fbb8248f108e9d3ef65)
(5 entradas de la línea base ya no aparecen — mejora, no bloquea, no baja la cifra congelada sin --freeze explícito)
```

Recifrado `142→141` WARN (`FP-91` `ABIERTA`→`FIRMADA`, `T22`), FAIL sin cambio en `19`. `gobernanza`/`estado` recifrados `137→138` ADR (`ADR-138`). Sin `--freeze` en ningún punto.

## Perímetro

Tocado: `forense/adv-duelo/ADV1-M6-v2-2026-08-20.md` (nuevo) · enmiendas in situ en `canon/PLAN-CALCULO-TOTAL-v1_1.md` y `canon/APERTURA-FASE-CALCULO-v1_2.md` (solo notas añadidas, cuerpo original intacto) · `canon/gobernanza-v1_15.md` (`ADR-138`, cabecera) · `canon/estado-programa-v1_10.md` (cascada, cabecera) · `forense/firmas-pendientes.tsv` (fila `FP-91`) · `forense/hallazgos.md` (una línea) · `forense/encargos/2026-08-20-SELLA-C.md` (nuevo) · esta nota.
No tocado: `forense/CAREO-ADV-DUELO-diseno-v2-2026-08-19.md` (el careo original, verificado ausente del diff) · `milpa/` · `data/` · `tests/`.
