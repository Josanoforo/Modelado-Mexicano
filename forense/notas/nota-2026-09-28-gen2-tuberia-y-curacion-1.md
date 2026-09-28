# Nota de cierre · ACTO GEN2-TUBERIA-Y-CURACION-1 · 28/sep/2026 · NUBE

ADR-260928-GEN2-TUBERIA-Y-CURACION-1-247d-01 (raíz `247d`, 0-bis `247d3dd1`). SHA de redacción del encargo `65da69fd`; main avanzó 8 commits desde entonces (no PARO, re-derivado). ARRANQUE: base al día, árbol limpio, sin duplicado de rótulo (ramas remotas, worktrees, PR abiertos/cerrados). ENTORNO-DERIVADO=NUBE coincide con lo declarado.

## Contadores
Cero mediciones; no adopta (cabecera del encargo). `dependencias_numericas_legacy_activas` no se mueve: sigue en 67 (ver P8).

## P8 · Legacy 67→82: el "82" no es reproducible
[EJECUTADO] Reproduje `python3 tools/corrida0.py status` en cuatro puntos de la historia, en worktrees separados del mismo clon:

| commit | fecha | `dependencias_numericas_legacy_activas` |
|---|---|---|
| `3a7b61db` | 28/sep 08:49 | 67 |
| `643a8198` | 28/sep 09:08 | 67 |
| `65da69fd` (SHA de redacción) | 28/sep 09:55 | 67 |
| `1f4bf1cc` (HEAD al abrir este acto) | 28/sep 10:20 | 67 |

Los cuatro dan **67**, no 82. `git log --oneline` sobre los rangos `3a7b61db..643a8198`, `643a8198..65da69fd` y `f70eea0f..b88b92b1` (el rango que la premisa citaba) contra `tools/corrida0.py` y `data/corrida0/usos.tsv` no devuelve **ningún** commit: el mecanismo no cambió en ese tramo. `f70eea0f` (RESUMEN-SUITE-1) solo añade el campo diagnóstico `..._definicion_desde` (pickaxe sobre dos líneas ya existentes); no toca la suma.

**Dictamen (vocabulario cerrado): DEFECTO-DE-CONTEO, no-H1.** No es H1 (el contador de legacy no usa `RE_FP`/`RE_ADR`; H1 es un subsistema distinto — el clasificador de ids FP/ADR). No es CAMBIO-DE-DEFINICIÓN (la marca de definición no cambió el tramo revisado). No es CONTEO-CORRECTO-QUE-NADIE-EXPLICÓ (no hay 15 dependencias nuevas: cero commits tocaron el insumo). El "82" de la premisa de dirección no se pudo reproducir desde `origin/main` en ningún punto citado ni en el actual; probablemente reflejaba un estado local no comiteado de la sesión que redactó el encargo. **No se mueve el contador** (67 es el valor vigente, antes y después de este acto).

## P1 (G1-B) · NO-CORRIDO: la premisa de 100 MB ya no aplica
[EJECUTADO] `git cat-file -s` sobre `data/corrida0/resultados.tsv`: **89 951 772 B** (89.95 MB, coincide con la hoja) en `429ec004` (commit justo antes del último `[deriva]`), pero **15 611 540 B** (15.6 MB) en `1f4bf1cc` (HEAD al abrir). El propio `.github/workflows/verify.yml` (líneas ~644-667, `ACTO GEN2-TUBERIA-VISTA-NORMALIZADA-2/3/4`, firma de mesa) ya instaló una guardia dura: **ningún archivo derivado (`corridas.tsv`/`resultados.tsv`/`usos.tsv`/`valores-vista/*`) puede superar 50 MB**, tras externalizar `camino_linaje` y los valores largos (`valor` > 1 KB) a `data/corrida0/*/valores-vista/*`. El comentario del propio job lo declara cerrado: *"Antes de COMMIT-B este guardia toleraba hasta 100 MB con aviso a 50; ese régimen de transición ya cerró."*

La firma de mesa G1:B ("partir `resultados.tsv` por rango de CALC") se dio sobre la hoja del 27/sep, que no incorporaba este cambio (ya fusionado para cuando este acto abrió, horas antes). El riesgo agudo que motivó la firma (GH001 por superar 100 MB) ya está resuelto por un mecanismo distinto, ya fusionado y ya verificado con guardia de CI — no por partición por rango de CALC, sino por externalización de los campos que inflaban el archivo.

Construir un sistema de partición por rango de CALC ahora mismo, sin que mesa re-confirme si G1:B sigue queriéndose dado este hallazgo, es exactamente "ajustar el procedimiento" sobre una premisa que cambió de terreno (§2, D-19 regla 2: toca una firma de mesa → PARA y reporta). **No se ejecuta P1** en este acto. Ver `## NO-CORRIDO` del encargo.

## P2 (H1-a) · hecho
`RE_FP_NUEVA`/`RE_ADR_NUEVA` ya no exigen el literal `GEN2-`. Test sellado ampliado (no debilitado) con ids reales del tablero. Recuento real: SIN-ASIGNAR 73→71, ESPERA-FIRMA 81→84, SUCESOR-YA-FUSIONADO 33→36 (5 filas cambian de clase — menos que la estimación ilustrativa "6 pares" de la hoja, que citaba un ejemplo, no el universo).

## P3 (H2-b) · hecho
`lee_tablero` cuenta registros lógicos (líneas físicas reunidas hasta que el conteo de tabs cuadra con la cabecera), no líneas físicas. El archivo de hoy no tiene ninguna fila partida (635 líneas de dato == 635 registros), pero el `+1` de la cabecera en el conteo viejo se corrige de todos modos; caso sintético con salto de línea incrustado probado antes de congelar.

## P4 (H5-a) · hecho
Una línea: `docs/index.md` entra al `git add` del job `derivados` junto a `README.md`. Test huérfano estático sobre esa línea (no ejecuta el job completo, D-14).

## P5 (C2-a) · hecho, evidencia orgánica
Run real de `automerge-rutinas.yml` inmediatamente posterior al merge de PR #1213 (GEN2-TRAMITE-NC-DECISIONES-1, merged `2026-09-27T07:32:08Z`):

- **run_id**: `36303593705` (run_number 673)
- **url**: https://github.com/Josanoforo/Modelado-Mexicano/actions/runs/36303593705
- **creado**: `2026-09-27T07:35:53Z` (≈3.5 min después del merge), `head_sha` = `1c7b840a…` (el propio merge commit de #1213), `conclusion` = `success`.
- Detalle por paso (`fusiona-si-rutina`): "Condición 1 — rama o commit de rutina" corrió y el resto de los pasos (guardia, fusiona, registra) salieron `skipped` — correcto: la rama de #1213 (`claude/new-session-8zcdo3`) no está en la lista cerrada de rutina, así que la rutina declinó fusionar (lo fusionó mesa a mano), exactamente el comportamiento esperado.

Sin PR sintético (opción b, no tomada). FP `f2e5-09` marcada FIRMADA citando esta evidencia orgánica.

## P6 (F1-a) · parcial
Re-sellados `respuestas.json` (CONTRATO, 11 peticiones) y `respuestas-ahorro-alcance-menor.json` (AHORRO, 3 peticiones) contra el índice de hoy: diff campo por campo contra el dorado viejo en las dos corridas, **ningún** `estado`/`valor.punto`/`aptitud.estado` cambia — solo deriva de infraestructura esperada (hashes de archivos que cambiaron legítimamente, una cita que se corrió de línea, `resultado.fuente` que pasó a `VERIFY-ESTRUCTURADO` tras E.7). Re-sello seguro. `test_08`/`test_09`: verde.

`test_01`/`test_01b` **no** se tocan. La hoja citaba "13→18" directos GEN2; el conteo real medido hoy con `listar_consumidores()` es **32** (no 18), y de esos 32, **20 no pasan** `aptitud.estado == APTA-POR-LINAJE` / `validacion_independiente == PASA` en la corrida en vivo (`assertEqual` sobre el `for` de `test_01` los marca `SUBFAILED`). El horizonte colapsado de `test_01b` creció de 3 a 6. Corregir solo el conteo (13→32, 3→6) dejaría el test en rojo por una razón nueva y no diagnosticada — eso es "tocar qué se mide" sin verificar la restricción antes de tocarla (§2). Se revierte ese cambio y se deja NO-CORRIDO con hallazgo declarado (ver `## NO-CORRIDO`).

## P7 (D2-a) · hecho
32 ids de `data/manifiesto.yaml` renombrados (18 pares `engasto_2012_<n>`→`engasto_2013_<n>` + `engasto2012_<n>`→`engasto_2012_<n>`), vía herramienta con verificación de que solo `id` cambia. Excluidos 2 pares (`hogar_dta`, `gasto_de_consumo_ajustado_dta`) citados por el CALC sellado `CALC-ENGASTO-CONSUMO-PISOS-0001` — verificado por `git grep`, no supuesto.

## Criterio de «hecho» del encargo
- Tests huérfanos P1–P4, P6: P1 no aplica (NO-CORRIDO); P2, P3, P4 verdes; P6 parcial (test_08/09 verdes, test_01/01b NO-CORRIDO con hallazgo).
- Nota con run_id de C2: arriba.
- `python3 -c` lector YAML: 0 entradas ENGASTO con rótulo 2012 y `url_origen` 2013 *entre las tocadas* — las 2 excluidas (sealed CALC) siguen así a propósito, declarado.
- P8: dos conteos crudos y dictamen: arriba.
- `check.py --baseline`: VERDE — ver cierre.
