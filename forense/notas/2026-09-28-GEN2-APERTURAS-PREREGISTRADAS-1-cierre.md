# Nota de cierre · ACTO GEN2-APERTURAS-PREREGISTRADAS-1 · 28–29/sep/2026

ADR-260928-GEN2-APERTURAS-PREREGISTRADAS-1-68b3-01 · rama `claude/new-session-bhqoo8` · 0-bis `68b3c611` · base `9d2550b9` (= SHA de redacción; `git rev-list --count HEAD..origin/main` = 0 al cerrar) · PR #1313.

**Contadores movidos: cero.** No abre, no mide, no adopta, no pide firmas: la vista muestra qué firma abriría cada ola.

## Respuesta de mesa (verbatim, 29/sep, en sesión)
A la pregunta «¿un solo PR o uno por programa?» y al informe de lo que faltaba: «Hazlo como mejor creas conveniente pero termina el encargo completo». Decisión: **un solo PR** (#1313); la cabecera pedía «PR por programa», pero 17 expedientes comparten plantilla, guardia, prueba común y vista, y partirlos multiplicaría los conflictos en esos archivos compartidos.

## ARRANQUE
- [EJECUTADO] Hook: `ENTORNO-DERIVADO = NUBE`, `montado=NO archivos_examinados=0`, red `DENEGADA-POR-POLITICA`. Coincide con el encargo (NUBE). `data/raw` ausente; nada se descarga.
- [EJECUTADO] Duplicado: `git ls-remote --heads origin | grep -ic APERTURAS` → 0; un worktree.

## P1 · Inventario (universo declarado, A.4/A.15)
- [EJECUTADO] Premisa §3 caída (logística, prevista): el campo es `estado_reserva`, no `reserva`. Pero el campo no es el universo completo: la definición operativa de «reservado» es `tools/corpus_loader.py::motivo_reserva` (campo que empieza por RESERVADA **o** `RESERVA_FUERA_DEL_MANIFIESTO`: firmas R04/R05/R06 y régimen de la memoria: ENVIPE 2026, ENIGH 2024, ENCO). Reserva **257** ids de 7 198.
- [EJECUTADO] Segunda fuente: 27 CALC sellados declaran en su `spec.yaml` una ola «RESERVADA (E.6), no es input» (`inventario_aperturas.contendientes_declarados()`; regex `ola_reservada:|RESERVAD[AO]…no (es|son) input|RESERVADA para estos reactivos` sobre las 200 primeras líneas de los 390 `spec.yaml`, sólo CALC con `sello.json`).
- [EJECUTADO] Tercera fuente: `data/corrida0/marcador-segmento.tsv` (csv.DictReader, 327 filas): 19 celdas `estado=RESERVADA` (ENIF 2024 14, ENVIPE 2025 4, ENUT 2024 1).
- [LEÍDO] Estados cambiados por firma o por código congelado, cada uno con cita en `ESTADO_POR_FIRMA`: R09 (ADENDA-1 de TRAMITE-FIRMAS-21) levanta por escrito CAAS 2015, ENG 2009 (ENGPEE) y MIGRACIÓN 2002 (MSM) —payloads aún en custodia, NC-260928-GEN2-TRAMITE-FIRMAS-21-8560-01— y deja ENCRIGE 2016 como vista; ENVIPE 2026, ENIF 2024 (módulo 7 R06 + cruces), ENIGH 2024 (salvo AMAI y remesas) y ENUT 2024 son reservas parciales; ENCIG 2025 (FP-260923-…-657c-01) y ENVIPE 2025 (sus 38 celdas de cruce tienen R sellada en `CALC-TRA-EVADE-NORMA-CRUCES-ENCOGIDA-ARBITRO-CRUCES-0001`) están abiertas por código congelado.
- [EJECUTADO] `python3 forense/prereg-aperturas/inventario_aperturas.py --escribe` → `filas=41 ids=299`. `--verifica` → CASA.

## P2 · Expedientes
- [EJECUTADO] Familias 2027: las 8 de `familias-2027-estado-v1_0.tsv` apuntan a olas 2027 → ninguna ola hoy reservada es R de una familia (`familia = NINGUNA` en toda fila).
- 17 expedientes completos (6 910 celdas R), uno por ola con contendiente sellado pendiente; los dos del 28/sep (ENSANUT, ENCODAT) más 15 escritos por cinco subagentes con perímetro propio sobre la misma plantilla (REGLAS-DE-LECTURA: lote ≥ 3 piezas). Al fusionar origin/main entraron dos contendientes sellados nuevos de GEN2-MEDICION-CARRILES-2 (`CALC-MC2-ENSANUT2024-0001` → ENSANUT 2025, `CALC-MC2-ENVIPE2025-0001` → ENVIPE 2026); la prueba de contendientes declarados los atrapó y ambos expedientes se ampliaron (E.6: una apertura sirve a todos los sellados antes; una sola primaria): ENSANUT +35 celdas MC2 (4 duplicadas y 7 diferencias apartadas sin abrir); ENVIPE 2026 +170 celdas MC2 puntuables, 21 RETROSPECTIVAS (tmod_vic ya abierta por los duelos) y 11 duplicadas de PERCEPCION que no puntúan.

| expediente | contendientes sellados | payloads | celdas R |
|---|---|---|---|
| `CENSO-2020` | `CALC-EIC-HOGARES-2015-0001`, `CALC-CCPV-FAM-PISOS-0001` | 32 | 800 |
| `EDR-2024` | `CALC-EDR-SUICIDIO-PISOS-0001` | 1 | 288 |
| `EMAT-2024` | `CALC-EMAT-PAREJA-PISOS-0001` | 1 | 225 |
| `ENADID-2023` | `CALC-ENADID-FAMILIA-HOGARES-0001`, `CALC-ENADID-COLA-2018-0001` | 1 | 313 |
| `ENASEM-2024` | `CALC-ENASEM-ESCOLARIDAD-2021-0001` | 1 | 14 |
| `ENCODAT-2025` | `CALC-ENCODAT-PISOS-SUSTANCIAS-0001` | 2 | 130 |
| `ENGASTO-2013` | `CALC-ENGASTO-CONSUMO-PISOS-0001` | 3 | 330 |
| `ENIF-2024` | `CALC-C2-COMPUESTO-RESERVADAS-0001`, `CALC-C2-COMPUESTO-IC-ENIF2024-0001` | 1 | 68 |
| `ENIGH-2024` | `CALC-ENIGH-CONSUMO-PISOS-0002`, `CALC-ENIGH-CONSUMO-PISOS-0001`, `CALC-PDR1-ENIGH2022-0001` | 5 | 1100 |
| `ENOE-2026T2` | `CALC-ENOE-PARTICIPACION-2024T4-0001` | 1 | 144 |
| `ENPECYT-2017` | `CALC-ENPECYT-CONOC-PISOS-0001` | 1 | 100 |
| `ENSANUT-2025` | `CALC-ENSANUT-PISOS-SALUD-0001`, `CALC-MC2-ENSANUT2024-0001` | 4 | 202 |
| `ENSU-2026` | `CALC-ENSU-PISOS-0001`, `CALC-ENSU-SERIE-0001` | 1 | 2025 |
| `ENVIPE-2026` | `CALC-ENVIPE-PERCEPCION-2024-0001`, `CALC-MC2-ENVIPE2025-0001` | 1 | 340 |
| `LAPOP-2023` | `CALC-LAPOP-PISOS-CAPITAL-SOCIAL-0001` | 1 | 260 |
| `LATINOBAROMETRO-2024` | `CALC-LATINOBAROMETRO-PISOS-2023-0001`, `CALC-LATINOBAROMETRO-COLA-2023-0001` | 1 | 408 |
| `PEW-2025` | `CALC-PEW-RELIGION-2024-0001`, `CALC-PEW-PISOS-RELIGION-AUTORIDAD-0001`, `CALC-PEW-MIGRACION-MEX-0001` | 1 | 163 |


- Cada expediente: `APERTURA-<X>-spec-v1_0.md` + sidecar (D-15, secciones 0–7 con módulo de auditoría v2.16), `APERTURA-<X>-spec.yaml` (contrato `corrida0` completo, `calc_id CALC-APERTURA-<X>-0001`, payloads con sha del manifiesto y todo código como input `origen: repo` con sha), `medidor_apertura_<x>.py` (auditoría AST de sí mismo como primera sentencia; `lee_payload_reservado` única lectura; `proporcion_por_grupo` único agregador), `RECETA-APERTURA-<X>.md` (firma → caja → preflight documental → un commit: levantar custodia + copiar contrato → preflight → run → asiento).
- Regla de adjudicación fijada antes de abrir: cobertura «R dentro del IC del contendiente» con Wilson 95 %, dictamen CALIBRADO/SUBCUBRE/SOBRECUBRE/NO-ESTIMABLE; en ENIF 2024 (piso vs retador C2) la regla del precedente sellado (ΔMAE, umbral 0.5 pp, `DIN-lote-enif2024-spec-v1_0.md:181-194`), dictaminada antes de abrir como NADIE-OCUPÓ-LA-FILA para `informal_cualquiera` (sin retador sellado; regla 6) → primaria la cobertura del piso.
- Rama prevista del encargo §5 tomada en los 17: los códigos se fijan sobre la ola del piso (la documentación de la ola reservada no está montada en NUBE); columna ausente → NO-ESTIMABLE; columna con otros códigos → PARO y v1_1 (NC-…-68b3-01).
- 24 expedientes mínimos (`EXPEDIENTE-<X>.md`): olas sin contendiente sellado → «sólo mesa por escrito» (o ya levantadas/abiertas, con su cita).

## P3 · Vista, tablero, receta
- `data/corrida0/aperturas-pendientes-v1_0.tsv` registrada en INFRAESTRUCTURA; viaja versionada con cabecera de procedencia (la marca `# DERIVADO — NO EDITAR` la reservaba al canal y rompía `enrutamiento-pr`: corregido en 00f928fa).
- `tools/tablero_carriles.py`: F15, 9 líneas; el stopper RESERVA cita el expediente. `--verifica` md/html NO-CASA también sin este cambio (lo regenera el job de derivados).

## Defectos corregidos en el camino (≤ 10 líneas, declarados)
- `guardia_apertura.wilson` daba −3e-18 o 1+2e-16 con k = 0 o k = n y `_valida_outputs` lo rechazaba (lo encontró el subagente de ENIF): acotado a [0, 1].
- `-MAE-PUNTO` en ENADID promediaba hogar con persona (§4 v2.16): se calcula sólo sobre celdas persona.
- La auditoría AST sólo vedaba `read_*`, `lee_dta`, `lee_csv_zip`: ahora veda todo `lee*`/`_lee*` fuera de `lee_payload_reservado` (lectores propios de los medidores sellados) y `E.MUTACIONES` suma esa mutación (10).
- La fila ENIF 2024: el módulo 7 quedó ABIERTA-PARCIAL (P7_1_1, P7_1_2, P7_2_1, P7_3_1) por la ADENDA-1 de GEN2-MEDICION-CARRILES-2, fusionada durante el acto; los cruces del expediente no se tocaron (CALC-MC2-ENIF2024-0001 mide marginales de un eje).
- ENSANUT/ENCODAT: la spec prometía NO-ESTIMABLE por columna ausente pero el lector levantaba KeyError: ahora reactivo ausente entra vacío y diseño ausente es PARO (test con lector falso).

## Premisas caídas (no PARO)
- ENVIPE 2026 no está «reservada» entera ni «abierta»: los duelos leyeron sólo `tmod_vic` y `NIV`; `tper_vic1` (el piso de percepción) sigue reservada → expediente ENVIPE-2026.
- ENIF 2024 «m7»: reserva por módulo en `corpus_loader` (R06); los cruces del marcador son otra reserva; ambos en su fila.
- ENCIG 2025 «fuera del árbitro» y ENVIPE 2025: ya abiertas por código congelado; sin expediente.
- ENDUTIH 2025 y CSES módulo 5: RESERVADAS por firma, sin contendiente sellado → sólo mesa. ENDUTIH además consumida por tres CALC (hallazgo).

## Hallazgos (`forense/hallazgos.md`, 28/sep)
Reserva por estimando sin marca en manifiesto ni cargador (nueve olas); marcador-segmento desfasado; ENGASTO 2013 sin tabla de lugar de compra; columna con mismo nombre y códigos nuevos → PARO y v1_1; ENDUTIH 2025 reservada y consumida; ENVIPE 2026 en la memoria como reservada entera.

## Verificación (sobre el commit final con origin/main fusionado)
- [EJECUTADO] Commit `f83f7be1` (merge de origin/main `10538563`, 0 detrás): `python3 -m pytest -q tests/test_prereg_aperturas.py tests/test_apertura_*.py` → `375 passed` (17 medidores × auditoría AST limpia y 10 mutaciones detectadas; contrato `corrida0` con campos obligatorios y `resultados` == esquema; `_valida_outputs` sobre las ramas todas/parcial/cero/sin IC; input ajeno rechazado; vista casa; ids reservados sin fila: 0; contendientes declarados sin fila: 0; sintéticos por ola).
- [EJECUTADO] `escribe_expedientes.py --verifica` → 34 CASA, 0 NO-CASA · `inventario_aperturas.py --verifica` → CASA (41 filas, 299 ids).
- [EJECUTADO] `python3 tests/check.py --rapido` → `0 FAIL · 461 WARN`.
- [EJECUTADO] `python3 forense/prereg-aperturas/simula_apertura.py --todos` (receta §4 aplicada en un worktree temporal, sin payload; sobre el commit final): 14 `PRE-FLIGHT: VERDE` (avisos NO-VISIBLE-EN-ESTE-CONTEXTO, FP-352); LAPOP-2023 bloquea sólo por `input_manifiesto_RAIZ_NO_CONFIGURADA` de `descargas_mx` (raíz inexistente en NUBE: NO-VERIFICABLE-AQUÍ, contrato sin otro bloqueo). LATINOBAROMETRO-2024 (VERDE) y PEW-2025 (sólo `descargas_mx`) salen de la corrida completa previa al merge (rc 0); sus contratos no cambiaron salvo el sha de la guardia.
- [EJECUTADO] `check.py --baseline` local previo al merge: LÍNEA BASE VERDE (sin FAIL nuevos frente a `tests/baseline.json`). Sobre el head final lo juzgó el CI del PR (P-A): `suite`, `adicionales`, `guardias`, `preflight-calc`, `guardas-res`, `enrutamiento-pr` y `check` en success sobre `8ff8636a`.
- Defectos del propio acto atrapados por el CI y corregidos: la vista con cabecera `# DERIVADO` (enrutamiento-pr), el id NC duplicado por el merge union de `forense/no-corrido.tsv` (T47) y el sidecar de esta nota editada tras su sello.

## Archivos leídos
`forense/prereg-aperturas/archivos-leidos-v1_0.txt` (el test comprueba que ningún id ni archivo reservado del manifiesto aparece).

## Auditoría (v2.16)
PROSPECTIVA por construcción en los 17 (contendiente sellado antes de R); las celdas ya vistas (ENADID 18, Censo 7, ENIGH 3 con reserva) se reportan RETROSPECTIVAS y no puntúan. Unidad declarada por expediente; ninguna media de hogar con persona ni de delito con persona. Un eje a la vez, o una etiqueta de celda construida en los cruces de ENIF. Oferta antes que preferencia en conductas de uso de servicios y consumo. Cifras tecleadas a mano: ninguna (hashes y umbrales de la regla).
