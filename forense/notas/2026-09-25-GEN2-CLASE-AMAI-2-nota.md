# GEN2-CLASE-AMAI-2 · nota de acto · 25/sep/2026 · CAJA · MODO AUTÓNOMO

Encargo `forense/encargos/2026-09-25-GEN2-CLASE-AMAI-2.md` (SHA de redacción `40058c09` = base; 0 commits de diferencia al arrancar). Rama `acto/gen2-clase-amai-2`, worktree `~/mm-gen2-clase-amai-2`. 0-bis `f601d16f`. ADR `ADR-260925-GEN2-CLASE-AMAI-2-f601-01`.

Contadores movidos: **un CALC GEN2 sellado** (`CALC-AMAI-NSE-ENIGH-2024-0001`, `cuenta_gen2: SI`, `adopta: NO`); `celdas_validadas` 219 → 219 (Δ0, `tools/cierre_acto.py` @ `908d7c74`).

## 0 · Arranque

- Entorno: `python3 tools/entorno.py --arranque` → `ENTORNO-DERIVADO = CAJA`, `senal-corpus: montado=SI archivos_examinados=511`. `data/raw` enlazado a `/home/pc0/mm-corpus/raw` y `data/raices.local.yaml` copiado (worktree nuevo).
- Duplicado: `git ls-remote --heads origin | grep -i clase-amai-2` → 0; ningún PR abierto; worktree sólo el propio.
- §4 del encargo re-verificado: `ls data/corrida0 | grep -c AMAI-NSE-ENIGH-2024` → 0 al arrancar.
- `/acto` leída del worktree del acto (`.claude/commands/acto.md`, 519 líneas).

## 1 · Premisas

| Premisa (rótulo del encargo) | Verificación | Resultado |
|---|---|---|
| `[EJECUTADO]` CLASE-AMAI-1 (#1127) fusionado: spec v1.0 y seis CALC | `git log origin/main` (`42807ece`…`678f705b`); `ls data/corrida0` | cierta |
| `[EJECUTADO]` ENIGH 2024 «en manifiesto con `estado_reserva: RESERVADA`» | `grep -n estado_reserva data/manifiesto.yaml` alrededor de `enigh2024_nc_csv` | **falsa en la forma, cierta en el fondo**: la entrada no lleva campo `estado_reserva` (el campo exige `raiz: reserva_respondentes`, `tests/manifiesto.py:294-309`); la reserva vive en `data/corrida0/decisiones.tsv` `reserva:enigh2024`. Logística: la anotación de apertura parcial va en `usado_para` de la entrada (campo existente) + fila nueva en `decisiones.tsv`. |
| `[SUPUESTO]` los nombres pueden haber cambiado en 2024 | descriptor 2024 por texto de pregunta | **uno cambió**: `num_pickup` → `num_pick` (#45 HOGARES, p. 3.3). Los otros siete y el diseño conservan nombre y texto. |
| `[SUPUESTO]` el medidor de #1127 lee por nombre parametrizable | `tools/dominios/amai/componentes.py::enigh2022` | falso: nombres fijos y miembros 2022; además lee `remesas`. No se toca (es código sellado en seis CALC): la apertura 2024 usa un lector propio con lista blanca que importa, sin editar, `regla.py`, `medidor.distribucion` y `medidor.validacion`. |
| «comparación con la publicada por AMAI» | `https://www.amai.org/NSE/index.php?queVeo=NSE2024` (25/sep) | NO-ENCONTRADO una distribución AMAI sobre ENIGH 2024; la publicada vigente es la Figura 1 (ENIGH 2022). Se congela ésa como referencia con el umbral de 5 pp de #1127 (spec §4). |

INTERPRETACIONES-DECLARADAS (cláusula de autonomía, 2): (a) «seis componentes» = seis componentes construidos con 8 columnas sustantivas + llaves + diseño/factor (16 columnas); (b) el rótulo de salida es el de la rama de aproximación de `medidor.validacion` (`APROXIMACION-CONFORME/DESVIADA`), porque la comparación es contra otra ola; (c) la condición (i) de la recomendación de #1127 (internet y celular de ENDUTIH circulares) no está en la letra de A4: se rotula `-CIRCULAR`, no se excluye.

## 2 · P1 · COMMIT-1 (`c9fc621b`) y cableado (`bad0da80`)

Spec `forense/prereg-caja/AMAI-NSE-ENIGH2024-spec-v1_0.md` (+ `.sha256`); medidor `tools/dominios/amai/enigh2024.py` (lector acotado con `usecols`, `GuardiaColumnas`, `agrega` con `GuardiaAgrupacion`, `guardia_salida`); auditoría `tools/dominios/amai/auditoria_enigh2024.py` → `AUDITORIA-VERDE`; mutación `tests/test_amai_enigh2024.py` (11 tests, sintético con columnas señuelo; cada regla A1–A6 detecta su fuente mutado); `corrida0 preflight` → `PRE-FLIGHT: VERDE` y `_valida_outputs` → `[]` en las ramas normal y suprimida. Ninguna lectura de ENIGH 2024 antes de `c9fc621b` (sólo descriptor y lista de miembros del zip, A.7).

**Ejecución descartada por el conducto** (D-6, no es un primer resultado distinto): el primer `corrida0 run` falló antes de sellar con `RESULT-AMAI-NSE-ENIGH-2024-JSON: VALOR-LARGO (1898 bytes)` — regla del conducto de `566fb049` (24/sep) que la prueba sintética del COMMIT-1 no ejercitó (sólo `_valida_outputs`, no `_problemas_valor_largo`). No se imprimió ni se vio cifra alguna. `bad0da80` mueve el JSON a `tablas/` por `REF:` y añade `parametros.calc_id`; regla, columnas, umbral y supresión intactos; auditoría y preflight VERDE de nuevo, y el conducto completo (`_fallas_run`) probado en sintético.

## 3 · P2 · COMMIT-2 (`fade828a`, `167262da`)

`CALC-AMAI-NSE-ENIGH-2024-0001` sellado; `verify` aislado **REPRODUCE / IDENTICO** (18/18 RESULT) asentado en `forense/replay-evidencia.tsv`. `ejecucion.json` → `parametros.columnas_leidas` = las 16 columnas; `RESULT-…-COLUMNAS-LEIDAS` igual.

Distribución NSE nacional de hogares 2024 (RESULT por id, `python3 tools/consulta.py result <id>`): BAJO 44.3 % · MEDIO 34.2 % · ALTO 21.5 %; por nivel E 7.0 · D 21.8 · D+ 15.4 · C− 17.8 · C 16.4 · C+ 13.1 · A/B 8.5. 89 906 hogares con NSE, 1 508 sin NSE (todos por `bano_comp` vacío; ningún otro componente falta — mismo patrón que ENIGH 2022, 1 738 sin `bano_comp` en `CALC-AMAI-NSE-ENIGH-2022-0001`, que el Anexo AMAI excluye igual). Desvío máximo contra la Figura 1: 4.74 pp por grupo (BAJO −4.74), 3.59 pp por nivel (D) → **`APROXIMACION-CONFORME`** (umbral 5.0). Ninguna celda suprimida.

Manifiesto: `enigh2024_nc_csv.usado_para` anota «SIGUE RESERVADA … APERTURA-PARCIAL: C7, columnas […]»; `decisiones.tsv` `reserva:enigh2024-nse-amai-apertura-parcial` (todo lo demás sigue reservado). README al día por `tools/readme_derivado.py --escribe` (272 → 273 corridas).

## 4 · P3 · eje NSE en el marcador (`908d7c74`)

`tools/marcador_segmento.py::filas_eje_nse`: filas de tipo `EJE-NSE`, una por (instrumento A4, conducta, grupo), R/IC/n por id de `CALC-AMAI-NSE-{ENIGH-2022,ENIF-2024,ENDUTIH-2023}-0001`; `decision_ref` = `FP-260924-GEN2-CLASE-AMAI-1-e773-01`; `fuente` lleva la validación NSE del CALC y la calibración contra ENIGH 2024. 84 filas (ENIGH 2022: 3 · ENIF 2024: 51 · ENDUTIH 2023: 30); estados `MEDIDA-POR-NSE` 52 · `-APROXIMACION` 24 · `-APROXIMACION-CIRCULAR` 6 · `SUPRIMIDA-N` 2. Tipo propio, no MARGINAL: no hay ola anterior con NSE en ninguno, así que no son pisos t-1 y no mueven cobertura de piso, `sin_piso` ni `celdas_validadas`. Guarda `tests/test_marcador_eje_nse.py` (sólo A4 — PARO c —, valores por id, celdas únicas, sin tocar contadores). Suites del marcador: 70 passed, 1 skipped.

Marcador re-derivado en árbol: `python3 tools/marcador_segmento.py --escribe` ×2 → `total_filas=327`, 84 `EJE-NSE`, sha256 `ff37d8b991dd695d46ed0b1844c8e885742619319b2f72a87c45d4b584da6533`; `celdas_validadas` 219 → 219. `marcador-segmento.tsv` y `estimadores-por-segmento.yaml` son derivados protegidos (`tools/derivados_protegidos.py`): se revirtieron antes del commit y no viajan en el PR. `estimadores-por-segmento.yaml` salía además con desfase heredado de `main` ajeno a este acto (`n_celdas` 20 → 52).

## 5 · P4 · cobertura por clase v1.1

`python3 -m tools.dominios.amai.calibracion` → `forense/analisis/clase-amai/{calibracion-2024-v1_0.tsv, cobertura-u1-por-clase-v1_1.tsv, resumen-p4-v1_1.json, cobertura-por-clase-v1_1.md}`; los v1_0 no se tocan. Desvío máximo por grupo contra ENIGH 2024: ENIF 2024 1.72 pp · ENDUTIH 2023 1.78 · ENDUTIH 2024 3.47 · ENIGH 2022 4.81 · ENIF 2021 4.85 · ENDUTIH 2025 4.98. Catálogo U1: 17 de 55 identidades de conducta en el eje NSE del marcador (las mismas 17 con piso NSE de v1.0).

Lectura: las dos olas ENDUTIH que #1127 declaró `DESVIADA` contra la Figura 1 (2022) quedan a < 5 pp de ENIGH 2024: su desviación era en buena parte deriva real 2022→2024, no sólo sesgo de imputación. No cambia su exclusión (A4 las deja fuera y este acto no la reabre); se ofrece a mesa como dato (sin FP nueva: la decisión ya está firmada).

## 6 · Hallazgos (una línea cada uno en `forense/hallazgos.md`)

- `_problemas_valor_largo` (conducto, 24/sep) no está en la receta de prueba sintética de COMMIT-1 de ningún medidor AMAI: un medidor con un RESULT texto > 1 KB congela verde y falla en el primer `run`.
- `tests/test_marcador_metrica_y_prospectividad.py` falla en `main` (`tablero_programa` sin `_celdas_d_adjudicadas`), ya censado `FALLA-DE-VERDAD`; ajeno.

## 7 · Auditoría de rigor extremo

¿Contadores? Uno (un CALC GEN2); ninguna adopción. La cifra 2024 es de **hogar**, RETROSPECTIVA, y no se promedia con ninguna de persona. NSE AMAI mide bienes y capital escolar del hogar, no clase sociológica ni ingreso; el movimiento de BAJO hacia MEDIO/ALTO en dos años mezcla bienestar con expansión de internet fijo y de autos a crédito (oferta antes que preferencia): no debe leerse como «ascenso de clase». Las filas del eje son asociaciones de la misma ola (A-bis), no efectos de la clase; las de ENDUTIH heredan la estructura de ENIGH 2022 por imputación y las de uso de internet/celular son circulares. ¿Qué parece cultura y es clase? Lo ya dicho en v1.0 §4 sigue en pie; este acto no añade conductas.

## 8 · Escrituras colaterales revertidas

`tools/ci_guardias.py --ejecuta-huerfanos` (14:09:59) re-derivó `canon/catalogo-del-mexicano-v1_1.md` y `forense/analisis/catalogo/v1_1/cobertura-31.tsv` (MOVILIDAD «EN-MEDICIÓN» 6 → 7: cuenta el CALC nuevo). Son del catálogo (sucesor catálogo v1.2, encargo §10), fuera de §9: se revirtieron con `git checkout --` y no viajan en este PR. La primera pasada de ese corredor reportó 1 fallido transitorio; la segunda, 0 de 158.
