# TABLERO DEL PROGRAMA · Psicología del Mexicano Contemporáneo / Modelado-Mexicano
**v1.0 · snapshot `57a365e` (origin/main, merge PR #471, 2/sep/2026 15:26 −06:00) · construido por dirección (Fable) el 2/sep/2026**

> Esto es una **VISTA DERIVADA**, no canon. La única fuente de estado sigue siendo `canon/estado-programa-v1_10.md` (§L0 al día por cascada) y la única fuente de decisiones `canon/gobernanza-v1_15.md`. Si este tablero y el canon discrepan, la discrepancia es un hallazgo (§7), nunca una corrección al canon desde aquí. Toda cifra de este archivo trae el comando que la produjo; una cifra sin comando no entra.

---

## 0 · Protocolo de actualización — para la sesión que solo actualiza este tablero

**Qué eres.** Una sesión de lectura y derivación. No lanzas actos, no decides, no renumeras, no editas `canon/`, `milpa/` ni `forense/` salvo este archivo (y su bitácora). Tu producto es este archivo actualizado más una entrada de bitácora (§8).

**Arranque, en este orden y sin saltar ninguno.**
1. `git fetch origin && git rev-parse --short origin/main` — el SHA es la identidad del snapshot (A.10). Nada se deriva del espejo del proyecto: está versiones atrás y contiene archivos que el repo nunca tuvo (v2.4).
2. `git branch -r | grep -v HEAD` — ramas vivas = PR abiertos = actos que aún no fusionan. Trabaja sobre `origin/main`, no sobre ramas, salvo para §4 (pipeline).
3. `python3 tools/tablero_programa.py` (si el script no está en el árbol, corre la columna «comando» de §2 fila por fila; no teclees ninguna cifra de memoria, v2.1). Pega la salida cruda en la bitácora.
4. `python3 tests/check.py --baseline | tail -6` — pega las tres líneas finales (FAIL · WARN · LÍNEA BASE).
5. Lee, en este orden, sólo lo que cambió desde el snapshot anterior: `git log --merges --format="%h %ad %s" --date=short <SHA_anterior>..origin/main` · las entradas de ADR nuevas (`grep -oE '^\*\*ADR-[0-9]+' canon/gobernanza-v1_15.md | tail -N`, y de cada una las primeras 400 palabras) · `forense/digesto/DIGESTO-<fecha>.md` más reciente · la cola `awk -F'\t' '$6=="ABIERTA"' forense/firmas-pendientes.tsv` · `forense/encargos/cola/` · las últimas 15 líneas de `forense/hallazgos.md`.

**Reglas de escritura.**
- Cada indicador de §2 se sustituye por el valor nuevo con su SHA; el valor anterior va a la columna Δ. **Un contador que no se movió se escribe igual** — es el único síntoma que no admite interpretación (v2.3). Si `motor_reglas_sin_dato`, `celdas_puntuables_LMR` o `propuesta_tier_PENDIENTE-DE-MESA` no se mueven en dos snapshots seguidos, va a §5 como bloqueador con el nombre del acto que debería moverlos.
- Negativos con conteo (A.13): «no encontré X» se escribe «NO-ENCONTRADO en N archivos examinados con el comando C».
- Vocabulario A.4 para cualquier clasificación: EXISTE-SATISFACE / EXISTE-NO-SATISFACE / NO-ENCONTRADO / NO-ACCESIBLE. «No existe» está prohibido.
- Un hito pasa a HECHO sólo con el PR fusionado y el ADR citados; «casi» no existe en §3.
- Un bloqueador tiene dueño (mesa / dirección / ejecutor / fuente), fecha de origen (FP o ADR) y criterio de cierre. Sin las tres cosas no es bloqueador, es comentario.
- Lo que no puedas derivar lo escribes «NO-DERIVADO (razón)». Nunca un número estimado.
- No resumas el canon: cítalo por archivo y línea. No cites de memoria ningún `p`: si lo necesitas, pégalo con `grep -n`.

**Cadencia.** Un snapshot por sesión de dirección o por día tras el digesto de trámite, lo que ocurra antes. Cada snapshot = una entrada en §8 con: SHA, fecha, Δ de los siete indicadores de la señal (§1), hitos que cambiaron de estado, bloqueadores abiertos/cerrados, y la línea «contadores que no se movieron».

**Dónde vive.** `forense/tablero/`, firmado por fusión de PR #483: `forense/tablero/TABLERO-PROGRAMA.md` + `tools/tablero_programa.py`, entrando por PR de trámite (`[COLA]`/`/tramite`), versionado por fecha en la bitácora y no por número.

---

## 1 · La señal — qué es avance y qué es contabilidad

El objetivo del programa es **un motor con reglas medidas que la simulación consume** (transfer maestra-34 §7; DE1: «no perdamos de vista el objetivo final»). Tres números lo dicen todo; el resto es contabilidad del programa sobre sí mismo.

| señal | @57a365e | meta declarada | qué la mueve |
|---|---|---|---|
| **S1 · reglas del motor sin dato** (`motor_reglas_sin_dato`) | **1** de 10 — `tramite.gobierno_digital.coercitivo` | 0 | otra fuente que distinga obligatoriedad del canal (ENCIG no puede: ADR-287) o re-especificación por dirección |
| **S2 · celdas puntuables L∩M∩R del corredor v1_2** (`celdas_puntuables_LMR`) | **9** de 14 | 13 (DIN-M-01 excluida con razón, DF-a) | L4 (4 R en ciego, PR #470 fusionado antes) · N2 (M de DIN-M-01) · R de DIN-M-01 (sucesor `.dta`) |
| **S3 · Ola 6 abierta / criterios explícitos** | NO (ADR-265); N5 encolado LISTO | decisión de mesa con criterios escritos (firma 9) | N3 · AGREGA-2 → N5 · RE-EVALUA-OLA6 (`/despacha`) |
| S4 · valores MEDIDO en el motor (`motor_conductas_medido`) | 24 | ↑ | actos de propagación (N-series) sobre lo que la propuesta acumula |
| S5 · entradas de la propuesta esperando sello (`propuesta_tier_PENDIENTE-DE-MESA`) | 8 | 0 al cierre de cada lote | firmas de mesa en RH + acto NUBE de propagación |
| S6 · celdas con IC por ejes en la propuesta (`propuesta_celdas_por_ejes`) | 55 | ↑ (disparadores medidos) | lotes de caja tipo MAESTRA35-L1 |
| S7 · payloads registrados (`manifiesto_ids`) | 1 029 | ↑ sólo si sirve a S1–S3 | adquisición (L3, cron FP-233) |

**Contabilidad (se mide, no es avance):** ADR, FP, encargos, WARN de la suite, versiones de instrucciones. Están en §2 porque hay que verlas, no porque cuenten.

---

## 2 · Indicadores derivados @ `57a365e` — con comando

Salida íntegra de `python3 tools/tablero_programa.py` (2/sep/2026). Δ vacío: primer snapshot.

### 2.1 Motor (`milpa/tramite.yaml`, `procedencia.yaml`, `canon/modelo-decision-v4_0.md`)

| indicador | valor | comando / receta | Δ | lectura |
|---|---|---|---|---|
| `motor_reglas` | 10 | `grep -cE '^  - id: ' milpa/tramite.yaml` | — | de 49 del modelo canónico (T12, `validador_registro_ids.py`: «49 reglas · 27 en perímetro») |
| `motor_reglas_con_dato` | 9 | python: reglas con ≥1 conducta `MEDIDO*` | — | |
| `motor_reglas_sin_dato` | `["tramite.gobierno_digital.coercitivo"]` | python: reglas cuyas conductas son todas ASIGNADO | — | **S1** · EXISTE-NO-SATISFACE en ENCIG (ADR-287), sin sucesor en esa fuente |
| `motor_conductas_medido` | 24 | `grep -c 'MEDIDO·' milpa/tramite.yaml` | — | **S4** |
| `motor_clase_asignado_lineas` | 11 | `grep -c 'clase: ASIGNADO' milpa/tramite.yaml` | — | incluye las conservadas como historia (mordida ×2 refutadas, util_sin_coercion y evasion_norma confirmadas y sustituidas en cálculo, coercitivo vigente) |
| `motor_tiers` | FUERTE 9 · MEDIA-FUERTE 1 | python: Counter(tier) | — | la MEDIA-FUERTE es `coercitivo` |
| `coef_generador_sellados` | 7 | yaml `coeficientes_generador_sellados` | — | escala «proporción ponderada, enlace identidad» (ADR-220) |
| `asignados_probabilidad` | 13 | yaml `asignados_probabilidad` | — | reglas del modelo con p ASIGNADO y no cargadas al motor; hoy con veredicto de dato: `informal_sin_puente` CONTRARIA (MAESTRA35-L1 P2, firma m1, pendiente N4) |
| `rutas_coeficiente` | RUTA-A=5 · RUTA-I=1 · RUTA-C=0 · SIN-RUTA=9 (suma 15) | yaml `rutas_estimabilidad_coeficiente.reparto` | — | 9 coeficientes sin reactivo en el corpus: hueco de mundo, no de trabajo |

### 2.2 Propuesta (acumulador `milpa/tramite-ola5-propuesta-v0.yaml`)

| indicador | valor | comando | Δ | lectura |
|---|---|---|---|---|
| `propuesta_entradas` | 19 | `grep -cE '^  - id: ' …propuesta-v0.yaml` | — | |
| `propuesta_tier_SELLADA` | 10 | `grep -cE '^\s+tier: SELLADA'` | — | ya cargadas al motor |
| `propuesta_tier_PENDIENTE-DE-MESA` | 8 | `grep -cE '^\s+tier: PENDIENTE-DE-MESA'` | — | **S5** · 4 son de MAESTRA35-L1 (firmadas r1/s1, ejecuta N4); el resto: corresidencia ×2, mordida serie, via_informal (c3) |
| `propuesta_tier_MEDIA` | 2 | `grep -cE '^\s+tier: MEDIA'` | — | cívica L4 y L6 (a1/b1 propagadas por N3, PR #473) |
| `propuesta_situacion_refutada` | 1 | `grep -cE '^\s+situacion: REFUTADA'` | — | `civico.participacion.contingente` → REFUTADA-COMO-CAUSAL (b1) |
| `propuesta_celdas_por_ejes` | 55 | `grep -cE '^\s+- \{celda: '` | — | **S6** · MAESTRA35-L1 (ENIF 2024, ENCIG 2025, ENVIPE 2025) |

### 2.3 Corredor / duelo (`forense/prereg-duelo-v2/`)

| indicador | valor | comando | Δ | lectura |
|---|---|---|---|---|
| `marco_v1_2_congelado` / `_sorteado` | 34 / 14 | filas sin `#` de `marco-M-congelado-v1_2.tsv` / `marco-M-sorteado-v1_2.tsv` | — | |
| `celdas_con_R` · `_con_M` · `_con_L` | 9 · 13 · 14 | `ls corridas-R/<id>.json` · `corridas-M/M-<id>*.json` · `corridas-L/L-<id>-M__*.json` | — | «R 11 → 14» de ADR-277 contó filas de codificación; R computadas son 9 (declarado por MAESTRA35-L2) |
| `celdas_puntuables_LMR` | 9 | R∩M∩L | — | **S2** |
| `celdas_sin_LMR` | DIN-M-01 · FAM-M-05 · FAM-M-06 · FAM-M-07 · TRA-M-02 | sorteado − (R∩M∩L) | — | 4 sin R (L4 las arbitra en ciego) + DIN-M-01 sin M ni R |
| `dominios_sorteado` | TRA 3 · CIV 6 · DIN 1 · FAM 4 | prefijo de id | — | dinero tiene una sola celda y está excluida: **N5 no puede encontrar «L en los cuatro dominios» hasta que DIN-M-01 tenga M y R** |
| `L_capturas_total` / `_v1_2` | 304 / 128 | `ls corridas-L/L-*.json` · `grep -l sha256_prompt` | — | 128 = 14 celdas × 8 réplicas × 2 variantes − 96 reanudadas de v1_1 (PR #465) |
| `scoreboards` | v1_1 · v1_1-AGREGADO · v1_1-AGREGADO-b | `ls scoreboard*` | — | v1_2 lo produce N3 · AGREGA-2 (LISTO en cola) |
| `dominios_activos` | 4 (tramite, civico, dinero, familia) | ADR-265 | — | **S3** |

### 2.4 Corpus (`data/`)

| indicador | valor | comando | Δ | lectura |
|---|---|---|---|---|
| `manifiesto_ids` | 1 029 | `grep -c '^- id: ' data/manifiesto.yaml` | — | **S7** |
| `payloads_verificados_ultimo_registro` | `data_raw: coincide=918 · no_coincide=0 · ausente=0` | último registro en `forense/notas/2026-09-0*.md` (MAESTRA34-L6) | — | sólo se re-mide en caja: `tests/manifiesto.py --verifica`, una invocación por `--id` (A.1) |
| `cola_adquisicion_estados` | OBTENIDO 63 · PENDIENTE 11 · NO-ACCESIBLE 8 · NO-OBTENIDO-POR-ESTE-AGENTE 7 · OBTENIDO-SIN-DENOMINADOR 2 | col. 2 de `data/cola-adquisicion-v1_0.tsv` (VISTA GENERADA, T26) | — | los 7 NO-OBTENIDO traen receta manual para mesa (A.5) |
| `registro_curador_filas` / `relaciones_filas` | 92 / 208 | `grep -vc '^#'` sobre `data/curacion-registro/…` | — | infraestructura Codex (A5/PR #441): tres capas |
| `inventario_reactivos_v1_2` | 178 247 | `grep -vc '^#' data/inventario-reactivos-v1_2.tsv` | — | |

### 2.5 Gobernanza y aparato

| indicador | valor | comando | Δ | lectura |
|---|---|---|---|---|
| `adr_max` | 291 | `grep -oE '^\*\*ADR-[0-9]+' canon/gobernanza-v1_15.md \| sort -n \| tail -1` | — | contiguo, sin huecos (comando de la casa) |
| `fp_max` / filas | 242 / 232 | `grep -oE '^FP-[0-9]+' forense/firmas-pendientes.tsv` | — | |
| `fp_abiertas` | FP-179 (30/ago, 3 d) · FP-233 (1/sep, 1 d) · FP-235 (2/sep) · FP-240 (2/sep) | `awk -F'\t' '$6=="ABIERTA"'` | — | ver §5 — **snapshot obsoleto, ver nota 2026-09-04 abajo** |

**Nota 2026-09-04 (restauración post-`PR #527`, ADR-335, renumerado desde el candidato original `ADR-334` al fusionar `origin/main`/`PR #529` que ya traía `ADR-334` para `MAESTRA38-N2`).** La fila de arriba es un snapshot congelado de una fecha anterior a esta nota, no se regeneró (el resto del tablero también lo está — `adr_max`/`fp_max` de este archivo no reflejan el árbol actual; regenerar con `tools/tablero_programa.py` queda fuera de perímetro de esta pieza). Corrección puntual de la **receta**, que sí aplica adelante: `$6=="ABIERTA"` subcuenta — usar `$6 ~ /^ABIERTA/` (ver `.claude/commands/tramite.md`). Con la receta corregida, contra `forense/firmas-pendientes.tsv` de HOY: **6 filas `ABIERTA`** — `FP-263` (3/sep) · `FP-282` (3/sep) · `FP-286` (3/sep) · `FP-287` (4/sep) · `FP-288` (4/sep) · `FP-293` (4/sep, nueva de esta pieza). `FP-290` salió del conteo (resuelta a `EJECUTADA` por esta pieza). Fuera de perímetro de esta pieza tocar `FP-286`/`FP-282`/`FP-288` (esperan lo que ya esperaban) ni `FP-263`/`FP-287` (no mencionadas en el encargo de esta restauración) — se documentan aquí en vez de forzar el conteo a un número distinto del que el comando corregido realmente da.

**Nota 2026-09-04 (recibo, `ACTO MAESTRA38-N3 · PRE-REGISTRO-DE-CAJA`, NUBE, `FP-296` — recibo, no requiere firma; renumerado desde `FP-295`, ver nota siguiente).** Tres specs de pre-registro selladas, cero medición: `forense/prereg-caja/{S1-A2,S2-L2,S3-C1}-spec-v1_0.md` + `.sha256` (universo/comandos del recenso de raíz; variables/ponderador/texto del futuro `MAESTRA38-L2` sobre ICPSR 35024; entrada ya llenada de `alta_relacion.py` para el re-asiento `N36→N41`). Dos correcciones de premisa declaradas en las specs mismas, no aquí: `S1` fija que el universo son tres raíces (no dos) con `downloads` excluida por diseño ya vigente; `S3` fija que `L3-BIS` adjudicó destino a 1 de 8 relaciones bajo `N36`, no a 7. Este snapshot del tablero sigue sin regenerarse (mismo `adr_max`/`fp_max` obsoletos de la nota de arriba) — esta pieza no toca `data/**`/`tests/**`/`tools/**`, sólo registra el recibo.

**Nota 2026-09-04 (colisión con `MAESTRA38-N4`, `ADR-337`).** `PR #531`/`ACTO MAESTRA38-N4 · PROPAGA-Y-PAGA` fusionó primero contra `main` y tomó, de forma independiente, los mismos candidatos `ADR-336`/`FP-295` que `MAESTRA38-N3` (nota de arriba) había derivado. Regla de la casa, "renumera quien fusiona segundo": `MAESTRA38-N3` cede y se renumera a `ADR-337`/`FP-296` al fusionar `origin/main` (commit `1f93518`) — la nota de arriba ya refleja el número final. Detalle: `forense/encargos/2026-09-04-MAESTRA38-N3-PRE-REGISTRO-DE-CAJA.md` §"Enmienda post-cierre".

**Nota 2026-09-04 (recibo, `ACTO MAESTRA38-N5 · DISEÑO-9-REGLAS-SIN-INSTRUMENTO`, NUBE, `FP-297` — recibo, no requiere firma).** Clasifica con evidencia las 9 reglas `NO-ENCONTRADO` que el censo de cierre de `MAESTRA38-A1` dejó sin falsador (`forense/notas/2026-09-03-MAESTRA38-A1-censo-9-no-encontrado.md`): **2 REFORMULABLE** (`civico.voto.clientelar_si_observable` vía LAPOP AmericasBarometer México 2019, ítems `clien1n`/`clien1na`/`clien4a`/`clien4b`, ya en corpus; `civico.protesta.agravio_urbano` vía LAPOP multi-ola, `PROT1`/`PROT2`/`prot3` + `VIC1`/`vicbar4a` + `AOJ12` + `CP6`/`CP9`/`E8` + `TAMANO`), **5 SIN-INSTRUMENTO** (`tramite.evasion.norma_inutil_sancion_improbable`, `dinero.ahorro.seguro_deposito_atenua_aversion`, `civico.voto.agencia_con_secreto`, `civico.transferencia.atribucion_lider`, `familia.cortejo.urbano_joven_apps`, cada una con instrumento hipotético mínimo y recomendación `MANTENER-COMO-HIPÓTESIS`), **2 CON-CANDIDATA** (`dinero.credito.scoring_alternativo` vía CNBV — objeto administrativo, estructuralmente invisible a `busca_reactivos.py`, que solo indexa reactivo de hogar; `dinero.credito.baja_friccion_usura_dano_downstream`/`N34` vía ENCRIGE FD completo + CONDUSEF). Universo de búsqueda: `data/inventario-reactivos-descargas-mx-v1_1.tsv` (42536 filas, superset de la tabla que usó el censo de A1 — la diferencia es por qué esta pieza sí encuentra señal donde A1 declaró cero). Cero medición, cero regla cerrada, cero canon tocado (perímetro explícito del encargo: `NO toca: canon/**` sin la excepción "salvo ADR" que sí traía `N3` — no se abre `ADR-338`, la propagación a canon queda para el sucesor que dispare mesa). Tabla `PENDIENTE-DE-MESA` completa en `forense/notas/2026-09-04-MAESTRA38-N5-diseno-9-reglas.md` §3; `FP-298` (decisión de mesa, vence 7 días, 11/sep/2026). Este snapshot del tablero sigue sin regenerarse (mismo `adr_max`/`fp_max` obsoletos de las notas de arriba).
| `encargos_archivados` / `_consumidos` | 272 / 102 | `ls forense/encargos/*.md` · `grep -l '## CONSUMIDO'` | — | consumidos = ejecutados con PR citado |
| `cola_encargos` | LISTO: MAESTRA34-N3 · MAESTRA34-N5 · CONSUMIDO ×4 | `forense/encargos/cola/` | — | `/despacha` los toma por compuerta de producto |
| `skills` | 10: acto · adquiere · arbitra · despacha · emite-m · encola · mapea · revisa · score · tramite | `ls .claude/commands/` | — | |
| `instrucciones_vigentes` | v2.12 | máximo numérico de `instrucciones-proyecto-v2_*.md` | — | A.9: la copia del proyecto de Claude debe ser la misma |
| `para_v2_13_entradas` | 2 | `grep -c 'PARA-v2.13' forense/hallazgos.md` | — | v2.13 se entrega con ≥3 (regla 3 de maestra-34) |
| `hallazgos_entradas` | 461 | `grep -c '^- \*\*2026' forense/hallazgos.md` | — | |
| suite | **19 FAIL · 166 WARN · LÍNEA BASE VERDE** | `python3 tests/check.py --baseline \| tail -6` (corrido en este snapshot) | — | los 19 FAIL núcleo son históricos y congelados en `tests/baseline.json` |
| `reports_tematicos` / `forenses` | 31 / 6 | `ls corpus/reports/*.md` · `corpus/forense/*.md` | — | capa de evidencia, append-only |
| `digesto_ultimo` | DIGESTO-2026-09-02.md | `ls forense/digesto/` | — | rutina de trámite |
| `hito_d_historico` | 26 de 27 corridas archivadas | `grep -oE '[0-9]+ de 27 corridas archivadas' canon/estado-programa-v1_10.md` | — | histórico; **no es señal** (transfer §6) |
| `commits` / `prs_fusionados` | 2 203 / 467 | `git rev-list --count HEAD` · merges con «pull request» | — | repo nace 29/jul/2026 (`git log --reverse`) |

---

## 3 · Hitos

Fechas derivadas de `git log --format="%ad|%s" --date=short origin/main | grep -i <rótulo> | tail -1` (primera aparición) o citadas del texto de instrucciones/gobernanza con su versión.

### 3.1 Hechos (sellados)

| # | hito | fecha | sello | qué dejó |
|---|---|---|---|---|
| H1 | Corpus inicial: 31 reports + forenses + suite | 29/jul | commit `343d589` | capa de evidencia (L1) y `tests/check.py` |
| H2 | Modelo de decisión con 49 reglas y motor MILPA (Fase 0/1) | jul–ago | ADR-35/50/51; `modelo-decision` v4_0 | 27 reglas en perímetro falsable |
| H3 | Hito D — falsación pre-registrada de reglas | jul–ago | T20; `estado-programa` L5 | 26 de 27 corridas archivadas (histórico) |
| H4 | Primera medición propia con microdato (β̂ de generador, ENVIPE/ENCUCI) | 4/ago | instrucciones v2.4; ADR-57 | A-bis: asociación ≠ coeficiente |
| H5 | Red al corpus público verificada (sonda a 9 hosts) y adquisición masiva INEGI/ISSP/WVS | 3–13/ago | v2.2 nota; ADR-134/194/198 | manifiesto por script; A.7 hash de contenido |
| H6 | Aparato de rigor completo v2.4→v2.12 (A.1–A.13, D-10 skill `/acto`) | 4–31/ago | ADR-142 (A.13), MAESTRA32-E19 (v2.12) | encargos ejecutables; formato corto |
| H7 | Piloto ADV1-M2 y procedimiento R (valor del microdato por celda) | 11–26/ago | ADR-68; MAESTRA30-E7 · R-SCORING | `tests/svystat.py`, corridas-R |
| H8 | Cruce inverso motor→corpus y censo de estimabilidad de coeficientes | 27/ago | MAESTRA31-E5 · MAESTRA31-E7 · MAESTRA31-E10 | 42 variables EXISTE-SATISFACE; 9 SIN-RUTA |
| H9 | Ola 5 fase 1: reglas nuevas con tasa base medida cargadas al motor | 31/ago–1/sep | MAESTRA32-E20, MAESTRA34-N1 (D1-a) | motor 8 → 10 reglas |
| H10 | Corredor v1_1: marco M sorteado, emisor M, árbitro R, scoreboard 11 celdas | 31/ago–1/sep | ADR-232/250/253; MAESTRA33-E21 | L reproduce la sobre-estimación de M frente a R |
| H11 | Ola 6 evaluada y NO abierta, con criterios pendientes | 1/sep | ADR-265 (MAESTRA33-E14) | N5 relanza con L en los cuatro dominios |
| H12 | Corredor v1_2: marco 34/14, 128 capturas L con `sha256_prompt`, runner re-sellado | 2/sep | PR #450, #459, #465 | S2 arranca en 9 |
| H13 | Trámite medido: mordida 62 % → 8.5 % (serie 8 olas), con_registro por canal | 1–2/sep | MAESTRA34-L1/N4 (DM) | primera regla del motor refutada por dato y sustituida |
| H14 | Priors de trámite con dato: util_sin_coercion 0.673, evasion_norma 0.563; ahorro re-medido 0.642 (ENIF 2024) | 2/sep | MAESTRA34-L5 (ADR-287) · MAESTRA35-N1 (a1/b1/c1) | S1 pasa de 3 a 1 |
| H15 | Cívica: concurrencia electoral REFUTADA-COMO-CAUSAL con calendario de 32 entidades desde fuente primaria | 2/sep | MAESTRA34-L6 (ADR-288) · MAESTRA35-N3 (a1/b1/c1, PR #473) | hipótesis nueva: presidencial +2.4 / intermedia −5.7 pp |
| H16 | Disparadores por ejes medidos por primera vez (55 celdas) y con_registro recorrida sin dedup | 2/sep | MAESTRA35-L1 (PR #471, ADR-291) | G3/`informal_sin_puente` CONTRARIA; escolaridad = gradiente más limpio de adopción digital |

### 3.2 En curso (con PR abierto o rama viva)

| # | hito | acto | estado | cierra cuando |
|---|---|---|---|---|
| C1 | Árbitro R reparado (umbral, compuesto, lector, captura por celda) + proyección ciega | MAESTRA35-L2 | PR #470 MERGEABLE, renumera al fusionar | mesa fusiona |
| C2 | F-DD v1.1 (rangos de ola) + M de DIN-M-01 | MAESTRA35-N2 | rama con CONSUMIDO, PR sin fusionar | mesa fusiona; regresión 13 M sin drift verificada |
| C3 | Scoreboard v1_2 (13 de 14) | MAESTRA34-N3 · AGREGA-2 | LISTO en cola, `/despacha` | el scoreboard agregado v1_2 (producto de MAESTRA34-N3 · AGREGA-2) presente en forense/prereg-duelo-v2/ — hoy NO-ENCONTRADO, es un hito pendiente |

### 3.3 Próximos, con criterio de cierre (no se declaran «casi»)

| # | hito | criterio verificable | qué lo mueve | dueño |
|---|---|---|---|---|
| P1 | S2 = 13: cuatro R en ciego | `corridas-R/{FAM-M-05,06,07,TRA-M-02}.json` en main | MAESTRA35-L4 (encargo listo, GATED a #470) | mesa lanza |
| P2 | Dominio dinero puntuable | M y R de DIN-M-01 | N2 (M) + sucesor caja `.dta` (R) | dirección redacta el sucesor tras N2 |
| P3 | Ola 6: decisión con criterios escritos | ADR de mesa con la firma 9 | N5 tras N3 | mesa |
| P4 | S1 = 0 | `coercitivo` con dato o re-especificada | otra fuente (NO-ENCONTRADO fuera de ENCIG hoy) o dirección | dirección |
| P5 | Motor con los disparadores por ejes y la recorrida cargados | S5 baja 8 → 4; `con_registro` con dos canales de la corrida 2 | MAESTRA35-N4 · SELLA-L1 (FP-241/242 FIRMADAS, ejecutada_en = N4) | dirección redacta, mesa lanza |
| P6 | Cívica ≥ 8 entidades tratadas y regla `tipo_boleta_federal` medida | entrada nueva en propuesta con β_pres, β_int e IC | MAESTRA35-L3 (encargo listo; enmienda Codex ya en main, PR #475) | mesa lanza |
| P7 | Instrucciones v2.13 | archivo íntegro pegado en los dos lados (A.9) | `para_v2_13_entradas` ≥ 3 (hoy 2) | dirección |
| P8 | Canon de estado refrescado (`estado-programa` v1.11) | §3 L3–L5 y §7 con fecha ≥ 1/sep | acto de dirección | dirección + mesa |
| P9 | Re-lectura de las reglas de ahorro (informal = complemento) | propuesta en RH y firma | hallazgo MAESTRA35-L1 P2 | dirección |

---

## 4 · Pipeline @ `57a365e` (2/sep, 15:26)

| entorno | acto | estado | perímetro que ocupa | gate |
|---|---|---|---|---|
| NUBE | MAESTRA35-N2 · F-DD-RANGOS-Y-M-DIN | rama viva con CONSUMIDO; PR sin fusionar | `tools/emite_m.py`, `corridas-M/`, `exclusiones-v1_2.md` | — |
| NUBE | MAESTRA35-N3 · SELLA-CIVICA-L6 | **fusionado** PR #473 | — | — |
| NUBE | MAESTRA34-N3 · AGREGA-2 → MAESTRA34-N5 · RE-EVALUA-OLA6 | LISTO en cola (`/despacha`) | corredor | N5 gateado a N3 por producto |
| NUBE | MAESTRA35-N4 · SELLA-L1 | **por redactar** (firmas ya en el tablero: r1/s1/u1/m1) | motor, propuesta, procedencia | GATED a nada (PR #471 ya en main) |
| CAJA | MAESTRA35-L1 · RECORRE-Y-SEGMENTA | **fusionado** PR #471 (ADR-291) | — | — |
| CAJA | MAESTRA35-L2 · R-v1_2-COMPLETA | PR #470 abierto | `tools/arbitra.py`, `espec-R-ciega-v1_2.tsv` | — |
| CAJA | MAESTRA35-L3 · CIVICA-TIPO-DE-BOLETA | encargo entregado; **no lanzado** (sin A.3 en main); enmienda Codex en `GUIA-CURADOR-REGISTRO.md` (PR #475) | manifiesto, `data/raw`, cola, propuesta (append) | ninguno |
| CAJA | MAESTRA35-L4 · R-v1_2-CIEGA | encargo entregado; **no lanzado** | `corridas-R/` ×4, `codificacion-R` (append) | GATED a PR #470 |
| mesa | fusionar #470 · lanzar L3/L4 · pegar input a N2 si lo pide · cron FP-233 · descargas manuales | — | — | — |

Regla de concurrencia vigente (2/sep): no hay «una sola caja»; lo que limita es perímetro de archivos, sesión ciega (ADR-46), numeración (renumera quien fusiona segundo) y escritura en `data/raw`/manifiesto (único recurso serial).

---

## 5 · Bloqueadores y riesgos (dueño · desde · cierre)

| id | qué bloquea | dueño | desde | cómo se cierra |
|---|---|---|---|---|
| B1 | **Dominio dinero sin celda puntuable** → N5 no puede cumplir «L en los cuatro dominios» | dirección/mesa | DF-a, 1/sep (`exclusiones-v1_2.md`) | N2 (M) + sucesor caja con lector `.dta` y join `fac_3b` (R) |
| B2 | **`coercitivo` sin fuente**: ENCIG no distingue obligatoriedad; sin sucesor | dirección | ADR-287, 2/sep | buscar fuente fuera de ENCIG (NO-ENCONTRADO declarado) o re-especificar la regla |
| B3 | **Bloqueo de IP del INE** a la caja (`siceen`, `siceef`, `computos2024`, `portalanterior`, `prep2021`) | fuente | ADR-288, 2/sep | usar `repositoriodocumental.ine.mx` (200) y navegador de mesa (DS-a); no golpear los cinco hosts |
| B4 | **Cron de adquisición no instalado** (adquisición autónoma parada) | mesa | FP-233, 1/sep | instalar `tools/adquiere_cron.sh` en la caja |
| B5 | **Descargas manuales vivas**: ICPSR Mexico Panel 2012, SSRN Bauchet 2014, CompraNet; TEPJF 1991-2018; Hidalgo 2016 `.rar` sin extractor | mesa | cola (7 NO-OBTENIDO) | recetas ≤1 min en `data/cola-adquisicion-v1_0.tsv`; depositar en corpus compartido y registrar por las tres capas |
| B6 | **FP-179 COLA-UBUNTU**: PDF-FD rama (b), mediciones diferidas de FP-172, WVS A4 | dirección/mesa | 30/ago | redactar los encargos que faltan; relanzar A4 |
| B7 | **FP-235** nomenclatura de `corridas-L` sin versión de spec y **FP-240** `modelo_real=None` | dirección | 2/sep | decidir antes de la spec v1_3 del corredor |
| B8 | **Contaminación de sesión ciega**: el marco sorteado incrusta `p` en `razon_DD`; la cascada cita `p` | ejecutor/dirección | FP-241/242 de L2 | mitigado: proyección ciega + cascada después de R (firmado 2/sep); vive en PR #470 |
| B9 | **Colisiones de numeración** con ≥2 PR abiertos (ADR-290 ×2, FP-241/242 ×2 el 2/sep) | proceso | recurrente | regla de la casa: renumera quien fusiona segundo; costo: merges extra (L1 hizo 3) |
| B10 | **Canon de estado desactualizado**: `estado-programa-v1_10` §3 L3–L5, §4 y §7 son de la era Hito D (4/ago); sólo L0 vive por cascada | dirección | — | acto de refresco a v1.11 (P8) |
| B11 | **Instrucciones**: v2.13 pendiente (2 de 3 entradas PARA); riesgo de desfase entre repo y proyecto (A.9) | dirección/mesa | 2/sep | entregar archivo íntegro y pegarlo en los dos lados en el mismo acto |
| B12 | **`revisa` SIN-DATO**: 6 `BLOQUEA` del revisor en PRs #442–#455 sin clasificar | mesa | transfer §4 | clasificar correcto / falso positivo |
| B13 | **Modelo vs dato en ahorro**: `informal_sin_puente` (0.74/0.21/0.05) CONTRARIA al dato ENIF 2024; regla fuera del motor pero viva en `procedencia` | dirección | MAESTRA35-L1, 2/sep | N4 anota el veredicto; dirección propone re-lectura (P9) |
| B14 | **Cívica acotada**: 2 de 14 entidades tratadas; wild cluster con p mínimo 0.125 | ejecutor | ADR-288 | L3 (≥8 entidades, diseño por tipo de boleta) |

---

## 6 · Mapa del repo — qué existe (@ `57a365e`)

| directorio | archivos | qué es | artefactos vivos (versión) |
|---|---|---|---|
| `corpus/reports/` · `corpus/forense/` | 31 · 6 | evidencia primaria, append-only | reports temáticos v1; 5 validaciones forenses + compass-4 |
| `canon/` | 12 | canon versionado, una versión viva por artefacto | `gobernanza-v1_15` (291 ADR) · `estado-programa-v1_10` · `glosario-v5_6` · `modelo-decision-v4_0` (49 reglas, 27 en perímetro) · `integrador` · `motor-nucleo-medible-v1_0` · `protocolo-sesion-v1_0` · `registro-rotulos.tsv` · `APERTURA-FASE-CALCULO-v1_2` · `PLAN-CALCULO-TOTAL-v1_1` |
| `milpa/` | 19 | el simulador y su motor | `tramite.yaml` (10 reglas) · `tramite-ola5-propuesta-v0.yaml` (19 entradas, 55 celdas) · `procedencia.yaml` (7 coef. sellados, 13 asignados) · `refutations.yaml` (52 ids) · `src/` (emisor, motor, celdas, theta…) · whitepaper/spec/plan v0 |
| `forense/prereg-duelo-v2/` | — | el corredor del duelo M/L vs R | marco v1_2 (34/14) · `corridas-R` (9 de 14) · `corridas-M` (13) · `corridas-L` (304, 128 v1_2) · scoreboard v1_1 · `codificacion-R-v1_0.tsv` · `exclusiones-v1_2.md` · `PAQUETE-L-v1_2` |
| `forense/encargos/` (+ `cola/`) | 272 (+6) | encargos archivados verbatim (A.3), CONSUMIDO al ejecutarse | 102 consumidos; cola: N3, N5 LISTO |
| `forense/notas/` · `forense/digesto/` · `hallazgos.md` · `firmas-pendientes.tsv` | 2 334 en total | bitácora del programa: specs, cierres, digesto diario, 461 hallazgos, 232 firmas (4 ABIERTA) | `agente-adquisicion-v1_0.md` (runbook) |
| `data/` | 218 | corpus registrado y tablas gobernantes | `manifiesto.yaml` (1 029 ids) · `INFRAESTRUCTURA-v1_0.md` (índice de tablas) · `curacion-registro/` (registro Codex: cola 92, relaciones 208, aliases) · `curacion-universo/` (barrido-2, autoridad semántica) · `cola-adquisicion-v1_0.tsv` (vista) · `p0-calendario/tratamiento-homologacion` · inventarios de reactivos · cruce-inverso v1_1 |
| `tools/` | 110 | herramientas versionadas | medidores (`medidor_*_encig25/envipe25/enif24`, `recorre_mordida…`, `mide_participacion_concurrente`, `calibracion_mordida_encig_serie`) · `arbitra.py` · `emite_m.py` · `curador_registro/` (Codex) · `vista_cola_adquisicion.py` · `p0_calendario_pel.py` · `tablero_programa.py` (propuesto) |
| `tests/` | 55 | la suite; un ADR sin test es decorativo | `check.py` (19 FAIL núcleo · 166 WARN · baseline VERDE) · `manifiesto.py` · `svystat.py` · `validador_registro_ids.py` · `baseline.json` |
| `.claude/commands/` | 10 | skills | acto · adquiere · arbitra · despacha · emite-m · encola · mapea · revisa · score · tramite |
| raíz | — | instrucciones v2.x (vigente v2.12), propuestas de motor, README, AGENTS, CITATION, LICENSE, USO-ACEPTABLE | |

Vías que gobiernan dominios (de `data/INFRAESTRUCTURA-v1_0.md`, no de memoria): payload → `tests/manifiesto.py`; registro del curador → tres capas Codex (`GUIA-CURADOR-REGISTRO.md` §alta); tablero de firmas → a mano en el TSV; ADR → cascada de `/acto`; propuestas → append al pie del acumulador; corredor → `/arbitra`, `/emite-m`, `runner_l_cli.py`, `/score`.

---

## 7 · Discrepancias encontradas al construir este tablero (hallazgos, no correcciones)

| # | qué | dónde | qué hacer |
|---|---|---|---|
| D1 | `estado-programa-v1_10.md` se declara «ÚNICA FUENTE DE ESTADO» con fecha 4/ago; sus §3 L1–L5, §4 y §7 describen la era Hito D y no mencionan corredor, Ola 5 ni mediciones propias; sólo L0 vive por cascada | `canon/estado-programa-v1_10.md:2, 85-105, 256` | P8: refresco a v1.11 por acto de dirección; mientras, leer L0 y este tablero |
| D2 | «R 11 → 14» (ADR-277, FP-227) cuenta filas de codificación; R computadas en `corridas-R/` son 9 | `canon/gobernanza-v1_15.md` ADR-277 · `corridas-R/` | declarado por MAESTRA35-L2; no se corrige el ADR (historia); el indicador del tablero es el conteo de archivos |
| D3 | Hito D aparece como «24 de 27» (nota v1.8, 29/jul) y «26 de 27 corridas archivadas» (L5, T20) en el mismo archivo | `estado-programa-v1_10.md:50, 95` | el vigente es el de T20 (26); el 24 es histórico del pre-registro |
| D4 | README «Estado del modelo» sigue en cifras de julio (49 reglas · 20 FUERTE · Hito D) — correcto pero no es la señal | `README.md` | anotar en P8 |
| D5 | Rótulo MAESTRA35-L3 reclamado dos veces (R-v1_2-CIEGA por L2 · CIVICA-TIPO-DE-BOLETA por dirección) | `canon/registro-rotulos.tsv` en rama de #470 | resuelto por input de mesa a L2: R-CIEGA = MAESTRA35-L4 |
| D6 | Dos PR abiertos reclamaron ADR-290 y FP-241/242 a la vez (#470 y #471) | ramas | regla de la casa aplicada por L1 al fusionar (ADR-291); L2 renumera |

---

## 8 · Bitácora del tablero

| snapshot | SHA | fecha | Δ señal (S1…S7) | hitos que cambiaron | bloqueadores | contadores que no se movieron |
|---|---|---|---|---|---|---|
| v1.0 | `57a365e` | 2/sep/2026 15:26 | S1 1 · S2 9 · S3 NO · S4 24 · S5 8 · S6 55 · S7 1 029 (línea base) | H14, H15, H16 sellados hoy; C1–C3 en curso | B1–B14 abiertos | — (primer snapshot) |

Próximo snapshot esperado: tras fusionar #470 y el PR de N2 — cambian C1, C2, `celdas_con_M` (13 → 14) y, si L4 corre, `celdas_con_R` (9 → 13) y S2.
