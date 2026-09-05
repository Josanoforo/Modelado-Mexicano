# TABLERO DEL PROGRAMA · Psicología del Mexicano Contemporáneo / Modelado-Mexicano
**v1.1 · snapshot `9cbd8d8` (origin/main, merge PR #485, 2/sep/2026 18:21 −06:00) · derivado el 2/sep/2026 por la conversación del tablero · snapshot anterior `57a365e` (v1.0, dirección/Fable)**

> Esto es una **VISTA DERIVADA**, no canon. La fuente de estado es `canon/estado-programa-v1_11.md` (v1.11 desde este snapshot, **en PROPUESTA: firma de mesa pendiente, FP-251**) y la de decisiones `canon/gobernanza-v1_15.md`. Si el tablero y el canon discrepan, va a §7 como hallazgo; nunca se corrige canon desde aquí.

**Estampa de universo (A.10).** Clon del repo público movido a `origin/main = HEAD = 9cbd8d8`, árbol limpio salvo un archivo no versionado ajeno a este acto (`tests/check_escala_coeficientes.py`, declarado). 2 285 commits. Firma de entorno (A.2, tres partes): `CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE` = **`sin_variable`** · `curl https://www.inegi.org.mx/` → **403** (política de red del entorno; `github.com` → 200) · `ls data/raw/` → **AUSENTE**. **Tercera parte no cumplida: sin corpus** — ningún indicador que exija abrir microdato se re-mide aquí, y se dice cuál (§2.4). Espejo del proyecto: no leído, cero cifras. Universo: el árbol completo de `9cbd8d8` salvo `.git` y `data/raw`.

**Verificación de premisas del encargo (v2.1), antes de ejecutar.** El encargo declara doce fusiones desde `57a365e`. Derivado con `git log --merges 57a365e..origin/main` y `git show --stat` por PR:

| premisa del encargo | verificación |
|---|---|
| el tablero vive en `forense/tablero/` | **CONFIRMADO** — `forense/tablero/TABLERO-PROGRAMA.md`, nacido en `78f89de` (PR #484) |
| el script vive en `tools/` | **CONFIRMADO** — `tools/tablero_programa.py`, mismo commit; **idéntico byte a byte** al que entregó dirección |
| fusionaron L2 · L3 · N4 · N2 · L5 · A1 ×2 · L6 | **CONFIRMADO** — PR #470 · #476 · #477 · #474 · #479 · #481 y #483 · #480 |
| fusionó **N5** | **NO CONFIRMADO.** `forense/encargos/cola/2026-09-01-MAESTRA34-N5-RE-EVALUA-OLA6.md` sigue **LISTO, sin `## CONSUMIDO`**, y ningún merge lo nombra. Lo que fusionó en PR #485 es **MAESTRA35-N6** (estado-programa v1.11) |
| fusionó N6 y el propio tablero | **CONFIRMADO** — PR #485 y PR #484 |
| — | **Dos fusiones que el encargo no nombra**: PR #478 (`REPARA-REGRESION-CITA-LINEA`, ADR-296) y PR #482 (`l5-espejo-estado-programa`) |

Ninguna de estas correcciones detiene el acto: el tablero es de lectura y las doce fusiones se leen igual. Se declaran porque una premisa mal fundada que nadie corrige se hereda (v2.1).

---

## 0 · Protocolo de actualización — sin cambios respecto de v1.0, salvo una nota

Arranque, en orden y sin saltar ninguno: (1) `git fetch origin && git rev-parse --short origin/main` — el SHA es la identidad del snapshot; nada sale del espejo. (2) `git branch -r | grep -v HEAD` — ramas vivas = actos sin fusionar. (3) `python3 tools/tablero_programa.py`, salida cruda al pie. (4) `python3 tests/check.py --baseline | tail -6`. (5) sólo lo que cambió: merges desde el SHA anterior, ADR nuevos, digesto, `awk -F'\t' '$6=="ABIERTA"' forense/firmas-pendientes.tsv`, `forense/encargos/cola/`, cola de `forense/hallazgos.md`.

Reglas de escritura, sin cambios: cada cifra con su comando; **un contador que no se movió se escribe igual**; negativos con conteo de archivos (A.13); vocabulario A.4; un hito pasa a HECHO sólo con PR y ADR; un bloqueador tiene dueño, fecha y criterio de cierre; lo que no se derive se escribe `NO-DERIVADO (razón)`; rótulos siempre con serie.

**Nota nueva de esta corrida.** El derivador tiene una ruta caduca: `hito_d_historico` apunta a `canon/estado-programa-v1_10.md`, que **PR #485 renombró a `v1_11`**. El indicador devuelve cadena vacía sin avisar — un negativo producido por un comando que examinó cero archivos, que es exactamente lo que A.13 prohíbe tratar como resultado. Va a §7 (D5) y no se corrige desde aquí.

---

## 1 · La señal — **cuatro de siete se movieron**

Primer snapshot del tablero en el que la señal avanza.

| señal | @`57a365e` | @`9cbd8d8` | Δ | meta | qué la mueve |
|---|---|---|---|---|---|
| **S1 · reglas del motor sin dato** | 1 | **1** — `tramite.gobierno_digital.coercitivo` | **0** | 0 | `MAESTRA35-L6` corrió sobre esta regla y **no la cerró**: el barrido de fuente sigue sin sustituto de ENCIG (ADR-301) |
| **S2 · celdas puntuables L∩M∩R** | 9 de 14 | **10** de 14 | **+1** | 13–14 | `MAESTRA35-L5` metió la R de `DIN-M-01` — **dinero deja de estar vacío**. Faltan `FAM-M-05/06/07` y `TRA-M-02`: las arbitra `MAESTRA35-L4` |
| **S3 · Ola 6 abierta** | NO | **NO** | **0** | criterios escritos + firma | `MAESTRA34-N3 · AGREGA-2` → `MAESTRA34-N5`, ambos **LISTO en cola y sin consumir** |
| **S4 · valores MEDIDO en el motor** | 24 | **28** | **+4** | ↑ | `MAESTRA35-N4 · SELLA-L1` cargó lo que `MAESTRA35-L1` midió |
| **S5 · entradas esperando sello** | 8 | **5** | **−3** | 0 al cierre de cada lote | mismo acto: tres sellos bajaron la cola. Suben otra vez con cada lote de caja |
| **S6 · celdas con IC por ejes** | 55 | **55** | **0** | ↑ | lotes de caja tipo `MAESTRA35-L1`; ninguno corrió en esta ventana |
| **S7 · payloads registrados** | 1 029 | **1 070** | **+41** | ↑ sólo si sirve a S1–S3 | `MAESTRA35-A1` ×2 (PR #481 y #483), serie electoral local/municipal al corpus compartido |

**La lectura honesta.** Se movieron S2, S4, S5 y S7. **No** se movieron S1, S3 y S6 — y las tres tienen dueño nombrado en §5. El único que no se movió teniendo un acto corriendo contra él es **S1**: `MAESTRA35-L6` fue a buscarle fuente a `coercitivo` y volvió sin ella. Eso no es un acto perdido; es un negativo con universo declarado, que es el formato correcto.

---

## 2 · Indicadores derivados @ `9cbd8d8` — con comando

Salida íntegra del derivador en §8.1. Δ contra `57a365e`.

### 2.1 Motor

| indicador | valor | Δ | lectura |
|---|---|---|---|
| `motor_reglas` | 10 | = | de 49 canónicas · 27 en perímetro (`validador_registro_ids.py`) |
| `motor_reglas_con_dato` | 9 | = | |
| `motor_reglas_sin_dato` | `["tramite.gobierno_digital.coercitivo"]` | = | **S1** · ver ADR-301 |
| `motor_conductas_medido` | **28** | **+4** | **S4** — `grep -c 'MEDIDO·' milpa/tramite.yaml` |
| `motor_clase_asignado_lineas` | 11 | = | incluye las conservadas como historia |
| `motor_tiers` | FUERTE 9 · MEDIA-FUERTE 1 | = | |
| `coef_generador_sellados` | 7 | = | escala «proporción ponderada, enlace identidad» |
| `asignados_probabilidad` | 13 | = | |
| `rutas_coeficiente` | RUTA-A=5 · RUTA-I=1 · RUTA-C=0 · SIN-RUTA=9 | = | 9 coeficientes sin reactivo: hueco de mundo |

### 2.2 Propuesta (acumulador)

| indicador | valor | Δ | lectura |
|---|---|---|---|
| `propuesta_entradas` | **22** | **+3** | `MAESTRA35-L3` (cívica) y `MAESTRA35-L6` |
| `propuesta_tier_SELLADA` | **14** | **+4** | cargadas al motor por `MAESTRA35-N4` |
| `propuesta_tier_PENDIENTE-DE-MESA` | **5** | **−3** | **S5** · la más reciente es `civico.participacion.tipo_boleta_federal_2016_2024` (FP-245, ABIERTA) |
| `propuesta_tier_MEDIA` / `_FUERTE` | 3 / **1** | +1 / **+1** | primera entrada FUERTE del acumulador |
| `propuesta_situacion_refutada` | 1 | = | |
| `propuesta_celdas_por_ejes` | 55 | = | **S6** |

### 2.3 Corredor / duelo

| indicador | valor | Δ | lectura |
|---|---|---|---|
| `marco_v1_2_congelado` / `_sorteado` | 34 / 14 | = | |
| `celdas_con_R` · `_con_M` · `_con_L` | **10** · **14** · 14 | **+1** · **+1** · = | M completo: `MAESTRA35-N2` cerró `DIN-M-01` |
| `celdas_puntuables_LMR` | **10** | **+1** | **S2** |
| `celdas_sin_LMR` | `FAM-M-05` · `FAM-M-06` · `FAM-M-07` · `TRA-M-02` | 5 → **4** | las cuatro sin R; `MAESTRA35-L4` las arbitra en ciego |
| `dominios_sorteado` | TRA 3 · CIV 6 · DIN 1 · FAM 4 | = | **dinero ya puntúa**: el bloqueador B1 de v1.0 se cierra |
| `L_capturas_total` / `_v1_2` | 304 / 128 | = / = | |
| `scoreboards` | v1_1 · v1_1-AGREGADO · v1_1-AGREGADO-b | = | v1_2 lo produce `MAESTRA34-N3`, LISTO en cola |
| `dominios_activos` | 4 | = | **S3** |

### 2.4 Corpus

| indicador | valor | Δ | lectura |
|---|---|---|---|
| `manifiesto_ids` | **1 070** | **+41** | **S7** |
| `payloads_verificados_ultimo_registro` | `data_raw: coincide=1 · no_coincide=0 · ausente=0 · sin_confi…` | era `coincide=918` | **no re-medido aquí** (entorno sin corpus). **Ojo**: el último registro cubre 1 payload, no 918 — no es una regresión del corpus, es que el registro más reciente es de un acto chico. Se re-mide en caja, una invocación por `--id` (A.1) |
| `cola_adquisicion_estados` | OBTENIDO **79** · PENDIENTE 11 · NO-OBTENIDO-POR-ESTE-AGENTE **9** · NO-ACCESIBLE 8 · **NO-ACCESIBLE-DESDE-LA-CAJA 2** | +16 · = · +2 · = · estado **nuevo** | el estado `OBTENIDO-SIN-DENOMINADOR` desapareció y aparece `NO-ACCESIBLE-DESDE-LA-CAJA`: distinguir el sandbox de la fuente es el hallazgo de `MAESTRA35-A1` |
| `registro_curador_filas` / `relaciones_filas` | **110** / **212** | +18 / +4 | tres capas del curador |
| `inventario_reactivos_v1_2` | 178 247 | = | |

### 2.5 Gobernanza y aparato

| indicador | valor | Δ | lectura |
|---|---|---|---|
| `adr_max` | **301** | **+10** (291 → 301) | ADR-293 a ADR-301, contiguos. **Renumeraciones a mano en la ventana: al menos cinco** (297→298 dos veces, 298→299, 299→300, 250→251) |
| `fp_max` / filas | **251** / **241** | +9 / +9 | receta declarada: `grep -c '^FP-'` |
| `fp_abiertas` | **7**: FP-179 (4 d) · FP-233 (1 d) · FP-235 · FP-240 · FP-245 · FP-246 · FP-251 | 4 → **7** | tres nuevas y ninguna cerrada: ver §5 |
| `encargos_archivados` / `_consumidos` | **280** / **110** | +8 / +8 | A.3 se está cumpliendo: cada acto archivó el suyo |
| `cola_encargos` | LISTO ×2 (`MAESTRA34-N3`, `MAESTRA34-N5`) · CONSUMIDO ×4 | = | **los mismos dos desde v1.0** |
| `skills` | 10 | = | `acto` y `revisa` editadas por PR #485 |
| `instrucciones_vigentes` | v2.12 | = | |
| `para_v2_13_entradas` | 2 | = | v2.13 se entrega con ≥3 |
| `hallazgos_entradas` | **483** | **+22** | |
| `reports_tematicos` / `forenses` | 31 / 6 | = / = | |
| `digesto_ultimo` | `DIGESTO-2026-09-02.md` | = | |
| `hito_d_historico` | **cadena vacía** | era «26 de 27 corridas archivadas» | **receta rota**, no regresión: el archivo se llama `v1_11` (§7·D5). El valor vive en `canon/modelo-decision-v4_0.md:65` — «26 de 27» |
| `commits` / `prs_fusionados` | **2 285** / **479** | +82 / +12 | |
| suite | **19 FAIL · 169 WARN · LÍNEA BASE VERDE** | = · **+3** · = | los 3 WARN nuevos son de los tests que PR #485 añadió a `check.py` |

---

## 3 · Hitos

### 3.1 Nuevos en esta ventana (todos con PR y ADR)

| # | hito | PR | qué dejó |
|---|---|---|---|
| H18 | **Cívica por tipo de boleta**: entrada nueva al acumulador con su serie 2016–2024 | #476 · ADR-293 | `civico.participacion.tipo_boleta_federal_2016_2024`, PENDIENTE-DE-MESA (FP-245) |
| H19 | **Marco M completo**: `DIN-M-01` gana su emisión | #474 | `celdas_con_M` 13 → 14 |
| H20 | **Sello de lo medido por `MAESTRA35-L1`** | #477 · ADR-295 | S4 24 → 28, S5 8 → 5 |
| H21 | **Regresión de cita-línea reparada** | #478 · ADR-296 | acto de reparación que el encargo no nombraba |
| H22 | **R de `DIN-M-01`**: lector `.dta` y join resueltos | #479 · ADR-297–299 | **S2 9 → 10**; el dominio dinero deja de estar vacío |
| H23 | **Adquisición: serie electoral local/municipal** ×2 | #481 y #483 · ADR-300 | S7 +41; cierre anti-PR#77 verificado en el corpus compartido |
| H24 | **Barrido de fuente para `coercitivo` y el puente** | #480 · ADR-301 | **negativo con universo declarado**: ENIF 2024 `EXISTE-NO-SATISFACE`; dos candidatas nuevas (Banxico ECF, IFT) |
| H25 | **Estado del programa refrescado a v1.11** | #485 | cierra el bloqueador B10 de v1.0; **queda en PROPUESTA** hasta FP-251 |
| H26 | **El tablero aterriza en el repo** | #484 | `forense/tablero/TABLERO-PROGRAMA.md` + `tools/tablero_programa.py`; cierra D8/P10 de las vistas previas |

### 3.2 En curso

Ninguno. **La única rama remota viva, `origin/claude/maestra35-n2-launch-jip2j0`, tiene 0 commits propios sobre `main`**: ya fusionó (PR #474) y quedó sin borrar. No es un acto abierto.

### 3.3 Próximos, con criterio de cierre

| # | hito | criterio verificable | quién lo mueve |
|---|---|---|---|
| P1 | **S2 = 14** | `corridas-R/{FAM-M-05,FAM-M-06,FAM-M-07,TRA-M-02}.json` en main | `MAESTRA35-L4`, sin compuerta; encargo aún NO-ENCONTRADO en `forense/encargos/` |
| P2 | **Scoreboard v1_2** | `scoreboard-v1_2-AGREGADO.md`{cita-ilustrativa} en main | `MAESTRA34-N3`, LISTO en cola — mesa `/despacha` |
| P3 | **Ola 6 decidida** | ADR con criterios escritos | `MAESTRA34-N5`, LISTO en cola, gateado a P2 |
| P4 | **S1 = 0** | `coercitivo` con dato o re-especificada | dirección: ADR-301 dejó dos candidatas nuevas sin evaluar (Banxico ECF, IFT) |
| P5 | **estado-programa v1.11 firmado** | FP-251 FIRMADA | mesa |
| P6 | **Instrucciones v2.13** | archivo íntegro pegado en los dos lados (A.9) | dirección; faltan entradas `PARA-v2.13` (2 de 3) |
| P7 | **El derivador con la ruta correcta** | `hito_d_historico` con valor | acto chico de trámite (§7·D5) |

---

## 4 · Pipeline @ `9cbd8d8`

| entorno | acto | estado | gate |
|---|---|---|---|
| — | `MAESTRA34-N3 · AGREGA-2` | **LISTO en cola desde v1.0**, sin consumir | ninguno |
| — | `MAESTRA34-N5 · RE-EVALUA-OLA6` | **LISTO en cola desde v1.0**, sin consumir | producto de `MAESTRA34-N3` |
| CAJA | `MAESTRA35-L4 · R-v1_2-CIEGA` | encargo **NO-ENCONTRADO** en `forense/encargos/` (A.3) | compuerta abierta desde PR #470 |
| mesa | `/despacha` los dos LISTO · firmar FP-251 y las otras seis · cron FP-233 · borrar la rama fusionada | — | — |

**Nada está corriendo ahora mismo.** Cero ramas con commits propios, cero encargos GATED. El programa está entre lotes, y lo que lo destraba está en la cola o en la firma, no en el trabajo.

---

## 5 · Bloqueadores (dueño · desde · cierre)

| id | qué bloquea | dueño | desde | cómo se cierra |
|---|---|---|---|---|
| **B19** | **Dos encargos LISTO llevan dos snapshots en la cola sin despacharse** (`MAESTRA34-N3`, `MAESTRA34-N5`). Entre los dos gobiernan **S3** y el scoreboard v1_2 | mesa | 1/sep | `/despacha` `MAESTRA34-N3`; `MAESTRA34-N5` sale detrás |
| **B20** | **Siete firmas ABIERTA, tres nuevas y ninguna cerrada** en la ventana. FP-251 congela el canon de estado en PROPUESTA; FP-245 congela la entrada cívica en PENDIENTE-DE-MESA | mesa | FP-179 la más vieja (4 d) | firma por fila, en RH |
| **B21** | **El encargo de `MAESTRA35-L4` sigue fuera del repo** (A.3), con la compuerta abierta desde PR #470. Es el único acto que mueve S2 a 14 | dirección | 2/sep, v1.0 (era B15) | commitear a `forense/encargos/` con su SHA y lanzar |
| **B22** | **`hito_d_historico` devuelve vacío**: el derivador apunta a `estado-programa-v1_10.md`, renombrado por PR #485 | dirección | 2/sep | un `sed` en `tools/tablero_programa.py`; entra por trámite |
| B2 | **`coercitivo` sin fuente.** `MAESTRA35-L6` corrió y volvió con ENIF 2024 `EXISTE-NO-SATISFACE` y dos candidatas nuevas sin evaluar | dirección | ADR-287, ampliado por ADR-301 | evaluar Banxico ECF e IFT, o re-especificar la regla |
| B3 | **Bloqueo de IP del INE a la caja** | fuente | ADR-288 | repositorio documental y navegador de mesa |
| B4 | **Cron de adquisición no instalado** | mesa | FP-233 | instalar `tools/adquiere_cron.sh` |
| B5 | **Descargas manuales vivas**: 9 en `NO-OBTENIDO-POR-ESTE-AGENTE` (+2 en la ventana) | mesa | cola | recetas ≤1 min en `data/cola-adquisicion-v1_0.tsv` |
| B6 | **FP-179 COLA-UBUNTU** sin disparar, 4 días | dirección/mesa | 30/ago | redactar los encargos que faltan |
| B7 | **FP-235 y FP-240** (nomenclatura de `corridas-L`, `modelo_real=None`) sin decidir antes de la spec v1_3 | dirección | 2/sep | decisión de mesa |
| B9 | **Colisiones de numeración.** Medido en esta ventana: **al menos cinco renumeraciones a mano** de ADR y FP | proceso | recurrente | renumera quien fusiona segundo; el costo ya es visible en los mensajes de merge |
| B11 | **Instrucciones v2.13 pendiente** (2 de 3 entradas) | dirección | — | entregar y pegar en los dos lados (A.9) |
| B12 | **`revisa` SIN-DATO**: 6 `BLOQUEA` sin clasificar | mesa | transfer §4 | clasificar correcto / falso positivo |
| B13 | **Modelo vs dato en ahorro** (`informal_sin_puente` CONTRARIA) | dirección | `MAESTRA35-L1` | propuesta de re-lectura |
| B14 | **Cívica acotada**: `MAESTRA35-L3` entregó la serie; el tier de la entrada nueva sigue sin sellar | mesa | ADR-293 | FP-245 |
| **B23** | **NUEVO · `via_capa2.py` resuelve `id_manifiesto` como un solo id** (FP-246): toda fila de `relaciones.tsv` con más de uno queda mal resuelta | dirección | 2/sep | acto de reparación; hoy sin encargo |
| ~~B24~~ | ~~NUEVO · Mesa decide las 9 reglas `NO-ENCONTRADO` clasificadas por `MAESTRA38-N5`~~ | mesa | `FP-298`, 4/sep | **CERRADO 4/sep** — `FP-298` → `EJECUTADA` por `ACTO MAESTRA38-N6`, §8.5 |

**Cerrados en esta ventana.** **B1** (dominio dinero sin celda puntuable) por PR #479. **B8** ya venía cerrado. **B10** (canon de estado desactualizado) por PR #485, *con reserva*: el archivo nuevo está en PROPUESTA hasta FP-251. **B15** se reformula como B21: los encargos de `MAESTRA35-L3` sí aterrizaron; el de `MAESTRA35-L4` no. **B24** cerrado por `ACTO MAESTRA38-N6 · PROPAGA-FP298-TESTS-Y-A3` (4/sep) — mesa aceptó la clasificación de las 9 reglas vía `FP-298`.

---

## 6 · Mapa del repo — dos cambios de estructura

Sin cambios respecto de v1.0 salvo: **(a)** `forense/tablero/` nace con este tablero y `tools/tablero_programa.py` con su derivador (PR #484; `git ls-tree -r --name-only`: 110 → 114 archivos versionados en `tools/`); **(b)** `canon/estado-programa-v1_10.md` **ya no existe** — es `v1_11` (PR #485), una sola versión viva por artefacto, como manda la regla de la casa.

---

## 7 · Discrepancias (hallazgos, no correcciones)

| # | qué | dónde | qué hacer |
|---|---|---|---|
| D1 | **RESUELTA.** El canon de estado era de la era Hito D (4/ago) | ahora `canon/estado-programa-v1_11.md` | queda la firma: FP-251 |
| D2 | «R 11 → 14» de ADR-277 cuenta filas de codificación; las R del sorteado v1_2 son 10 | ADR-277 · `corridas-R/` | sigue abierta; el indicador de este tablero cuenta archivos por id sorteado |
| D3 | Hito D aparece como «24 de 27» y «26 de 27» en sitios distintos | `modelo-decision-v4_0.md:65,704` | el vigente es 26 (T20) |
| D4 | README en cifras de julio | `README.md` | anotar en el refresco |
| **D5** | **NUEVA · El derivador del tablero tiene una ruta caduca.** `hito_d_historico` hace `grep` sobre `canon/estado-programa-v1_10.md`, que PR #485 renombró; devuelve **cadena vacía sin error**. Universo del negativo: `ls canon/` = 12 archivos, `estado-programa-v1_10.md` **NO-ENCONTRADO**, `v1_11.md` presente. Es A.13 en su forma pura: un cero producido por un comando que no examinó nada | `tools/tablero_programa.py` | B22 |
| **D6** | **NUEVA · El último registro de verificación de payloads cubre 1 archivo, no 918.** El indicador es «el último registro escrito», no «el estado del corpus»: al haber corrido un acto chico después del grande, el número cae sin que el corpus cambie. La receta describe otra cosa de la que su nombre sugiere | §2.4 · `payloads_verificados_ultimo_registro` | anotar; la re-medición real pide caja con corpus (A.1) |
| **D7** | **NUEVA · Una rama remota fusionada sigue publicada** (`origin/claude/maestra35-n2-launch-jip2j0`, 0 commits propios). El derivador la reporta como «acto que aún no fusiona» y no lo es | `ramas_remotas_vivas` | borrar la rama; el indicador se corrige solo |

---

## 8 · Bitácora

| snapshot | SHA | fecha | Δ señal (S1…S7) | hitos | bloqueadores | contadores que no se movieron |
|---|---|---|---|---|---|---|
| v1.0 | `57a365e` | 2/sep 15:26 | S1 1 · S2 9 · S3 NO · S4 24 · S5 8 · S6 55 · S7 1 029 (línea base) | H14–H16 sellados | B1–B14 abiertos | — (primer snapshot) |
| **v1.1** | **`9cbd8d8`** | **2/sep 18:21** | **S1 1 (=) · S2 9→10 (+1) · S3 NO (=) · S4 24→28 (+4) · S5 8→5 (−3) · S6 55 (=) · S7 1 029→1 070 (+41)** | **H18–H26 sellados** (12 PR, 9 ADR) | **cerrados B1, B10** (con reserva) · **nuevos B19–B23** · B15 → B21 | **S1, S3 y S6.** S1 con un acto corriendo contra él (`MAESTRA35-L6`) que volvió sin fuente — negativo válido, no acto perdido. S3 y S6 no se movieron porque **nadie los tocó**: sus dos encargos llevan dos snapshots LISTO en la cola |

Próximo snapshot esperado: tras `/despacha` de `MAESTRA34-N3` (mueve el scoreboard y destraba S3) y el lanzamiento de `MAESTRA35-L4` (mueve S2 a 14).

### 8.1 Salida cruda

```
$ git rev-parse --short origin/main            → 9cbd8d8
$ git log -1 --format="%h %ad %s" --date=iso   → 9cbd8d8 2026-09-02 18:21:48 -0600
                                                  Merge pull request #485 …maestra35-n5-yw5zmi
$ git branch -r | grep -v HEAD | grep -v 'origin/main$'
  origin/claude/maestra35-n2-launch-jip2j0     (0 commits propios sobre main)
$ git log --merges 57a365e..origin/main → 12 PR: #470 #474 #476 #477 #478 #479 #480 #481 #482 #483 #484 #485
$ python3 tests/check.py --baseline | tail -6
  19 FAIL · 169 WARN
  LÍNEA BASE: VERDE — nada nuevo frente a tests/baseline.json (HEAD congelado e4af4ed)
$ python3 tools/tablero_programa.py   (HEAD 9cbd8d8 · origin/main=True)
  motor_reglas 10 · motor_reglas_con_dato 9 · motor_reglas_sin_dato ["tramite.gobierno_digital.coercitivo"]
  motor_conductas_medido 28 · motor_clase_asignado_lineas 11 · motor_tiers {"FUERTE":9,"MEDIA-FUERTE":1}
  propuesta_entradas 22 · SELLADA 14 · PENDIENTE-DE-MESA 5 · MEDIA 3 · FUERTE 1 · refutada 1 · celdas_por_ejes 55
  coef_generador_sellados 7 · asignados_probabilidad 13 · rutas RUTA-A=5·RUTA-I=1·RUTA-C=0·SIN-RUTA=9
  marco 34/14 · celdas_con_R 10 · _con_M 14 · _con_L 14 · puntuables_LMR 10
  celdas_sin_LMR ["FAM-M-05","FAM-M-06","FAM-M-07","TRA-M-02"] · dominios TRA3·CIV6·DIN1·FAM4
  L_capturas 304/128 · scoreboards [v1_1, v1_1-AGREGADO, v1_1-AGREGADO-b] · dominios_activos 4
  manifiesto_ids 1070 · cola {OBTENIDO:79, PENDIENTE:11, NO-OBTENIDO-POR-ESTE-AGENTE:9,
                              NO-ACCESIBLE:8, NO-ACCESIBLE-DESDE-LA-CAJA:2}
  registro_curador_filas 110 · relaciones_filas 212 · inventario_reactivos_v1_2 178247
  adr_max 301 · fp_max 251 · fp_abiertas 7 (FP-179, 233, 235, 240, 245, 246, 251)
  encargos 280/110 · cola_encargos: 4 CONSUMIDO + 2 LISTO (MAESTRA34-N3, MAESTRA34-N5)
  skills 10 · instrucciones v2.12 · para_v2_13 2 · hallazgos 483 · reports 31 · forenses 6
  digesto DIGESTO-2026-09-02.md · hito_d_historico "" ← receta rota (D5)
  commits 2285 · prs_fusionados 479
```

**Comandos extra de esta corrida** (no están en el derivador):
```
$ grep -c '^FP-' forense/firmas-pendientes.tsv                          → 241
$ ls canon/ | grep estado                                               → estado-programa-v1_11.md
$ ls canon/ | wc -l                                                     → 12   (v1_10: NO-ENCONTRADO)
$ grep -c "de 27 corridas archivadas" canon/modelo-decision-v4_0.md     → 2 (valor vigente: 26 de 27)
$ git rev-list --count origin/main..origin/claude/maestra35-n2-launch-jip2j0 → 0
$ grep -c '## CONSUMIDO' forense/encargos/cola/2026-09-01-MAESTRA34-N5-RE-EVALUA-OLA6.md → 0
$ diff <(git show HEAD:tools/tablero_programa.py) <entregado por dirección> → sin diferencias
```

### 8.2 Recibo — `ACTO MAESTRA37-A2 · REVISA-COLA-A-DETALLE` (3/sep/2026, `ADR-330`, `FP-285`)

No es un snapshot completo de indicadores (fuera de perímetro de A2). Registro puntual: la
COMPUERTA (PR de `MAESTRA37-N8`, `#523`) se satisfizo; el acto revisó a detalle las 28 filas
no `OBTENIDO`/`CERRADA` de `data/curacion-registro/cola-adquisicion-registro.tsv` y clasificó
cada una en `BAJAR` (6) · `MESA-DECIDE` (12) · `NO-BAJAR-PORQUE` (10). Detalle:
`forense/notas/2026-09-03-MAESTRA37-A2-revision-cola.md` ·
`forense/notas/2026-09-03-MAESTRA37-A2-PAQUETE-RECETAS-3.md`. `FP-286` (mesa firma la
clasificación final, vence a 7 días). Ejecutado vía `PR #526`, fusionado a `main`; **una
ejecución independiente de este mismo acto en la rama de auditoría (candidato `ADR-331`,
`FP-288`/`FP-289`, commit `c8e5463`) resultó duplicada y fue descartada al fusionar** — ver
nota de fusión en `forense/encargos/2026-09-03-MAESTRA37-A2-REVISA-COLA-A-DETALLE.md`.

### 8.3 Recibo — `ACTO MAESTRA38-N4 · PROPAGA-Y-PAGA` (4/sep/2026, `ADR-336`, `FP-286`/`FP-287`/`FP-293`)

No es un snapshot completo de indicadores. Registro puntual, P1: `FP-286` (firma de mesa
sobre la clasificación de §8.2) → EJECUTADA — las 28 filas recibieron `nota` vía
`tsv_crudo.upsert_fila(clave=fuente_canonica)`, citando
`forense/notas/2026-09-03-MAESTRA37-A2-revision-cola.md` §2; 4 de ellas (9, 12, 25, 27)
pasaron a `PENDIENTE-DE-MESA` con receta verificada en
`forense/notas/2026-09-04-MAESTRA38-N4-PAQUETE-RECETAS-5.md` (6 recetas reales, no las 11
que el encargo citaba — discrepancia declarada en el recibo de `FP-286`, D-13). `FP-287`
(ausencia de tests de INFRA-1) → EJECUTADA, ya cubierta por `tests/test_cola_writer.py`/
`tests/test_manifiesto_seguro.py` (`ACTO MAESTRA38-N2`, `PR #529`). Detalle completo de P2-P4
en el `## CONSUMIDO` del encargo archivado:
`forense/encargos/2026-09-04-MAESTRA38-N4-PROPAGA-Y-PAGA.md`.

### 8.4 Recibo — `ACTO MAESTRA38-N5 · DISEÑO-9-REGLAS-SIN-INSTRUMENTO` (4/sep/2026, sin ADR, `FP-297`/`FP-298`)

No es un snapshot completo de indicadores; no toca `canon/**` (perímetro explícito,
sin la excepción "salvo ADR" que sí traía `N3` — no se abre `ADR-338`, propagación a
canon diferida al sucesor que mesa dispare). Clasifica con evidencia las 9 reglas
`NO-ENCONTRADO` del censo de cierre de `MAESTRA38-A1`
(`forense/notas/2026-09-03-MAESTRA38-A1-censo-9-no-encontrado.md`), contra
`data/inventario-reactivos-descargas-mx-v1_1.tsv` (42536 filas — superset de la tabla
que A1 examinó, con varias olas de LAPOP AmericasBarometer México que A1 no tenía
indexadas): **2 REFORMULABLE** — `civico.voto.clientelar_si_observable` (LAPOP 2019
`clien1n`/`clien1na`/`clien4a`/`clien4b`, ya en corpus) y `civico.protesta.
agravio_urbano` (LAPOP multi-ola, `PROT1`/`PROT2`/`prot3` + `VIC1`/`vicbar4a` +
`AOJ12` + `CP6`/`CP9`/`LAPOP-E8` + `TAMANO`) — con objeto reformulado, reactivo, instrumento
y `se_mueve_si` cada una. **5 SIN-INSTRUMENTO** — `tramite.evasion.
norma_inutil_sancion_improbable`, `dinero.ahorro.seguro_deposito_atenua_aversion`,
`civico.voto.agencia_con_secreto`, `civico.transferencia.atribucion_lider`,
`familia.cortejo.urbano_joven_apps` — cada una con instrumento hipotético mínimo y
recomendación `MANTENER-COMO-HIPÓTESIS`. **2 CON-CANDIDATA** — `dinero.credito.
scoring_alternativo` (fuente CNBV, objeto administrativo/IMOR, estructuralmente
invisible a `busca_reactivos.py` por diseño de universo — no un `NO-ENCONTRADO`
informativo) y `dinero.credito.baja_friccion_usura_dano_downstream`/`N34` (ENCRIGE FD
completo + CONDUSEF) — con ficha de adquisición cada una. Cero medición, cero regla
cerrada, cero falsador corrido. Tabla completa: `forense/notas/2026-09-04-MAESTRA38-N5-
diseno-9-reglas.md` §3. Bloqueador nuevo: `B24` (§5) — `FP-298`, decisión de mesa sobre
la tabla, vence 11/sep/2026. Detalle de las desviaciones D-13 (ADR no abierto, FP
re-derivado 297/298 no 298/299) en el `## CONSUMIDO` del encargo archivado:
`forense/encargos/2026-09-04-MAESTRA38-N5-DISENO-9-REGLAS-SIN-INSTRUMENTO.md`.

### 8.5 Recibo — `ACTO MAESTRA38-N6 · PROPAGA-FP298-TESTS-Y-A3` (4/sep/2026, `ADR-338`, `FP-299`)

`FP-298` → `EJECUTADA`: mesa acepta, sin excepción de origen, la clasificación con
evidencia de §8.4. Carga en `milpa/tramite-ola5-propuesta-v0.yaml`: **3
`HIPÓTESIS-SIN-INSTRUMENTO`** (`tramite.evasion.norma_inutil_sancion_improbable`,
`civico.transferencia.atribucion_lider`, `familia.cortejo.urbano_joven_apps` —
vocabulario nuevo documentado en `.claude/commands/mapea.md` §4) y **2 `REFORMULABLE`**
como tercera formulación complementaria (`civico.voto.clientelar_si_observable_
lapop2019`, `civico.protesta.agravio_urbano_multiola`), sin reabrir los sellos ya
vigentes de `MAESTRA35-L9`/`L11` (`D2-d`/`D2-f`). Una línea nueva en
`canon/modelo-decision-v4_0.md` §7. Dos filas nuevas en la cola de adquisición
(`CNBV_PORTAFOLIO_INFORMACION_IMOR_CONSUMO`, `ENCRIGE_2020_FD_COMPLETO_MAS_CONDUSEF`,
vía `tsv_crudo.upsert_fila` + `vista_cola_adquisicion.py`, nunca escritas a mano);
`forense/notas/2026-09-04-MAESTRA38-N6-PAQUETE-RECETAS-6.md` (0 de 2 recetas
verificables — red bloqueada en `NUBE`, `curl` → `403`/`000`, declarado en vez de
fabricar una URL).

**Hallazgo (D-13).** `MAESTRA38-N5` clasificó las 9 reglas buscando solo con
`busca_reactivos.py` contra `descargas_mx*`, sin cruzar la propuesta acumulada ni
`canon/modelo-decision-v4_0.md` §7: 2 de las 5 `SIN-INSTRUMENTO`
(`dinero.ahorro.seguro_deposito_atenua_aversion`/`R1.5`,
`civico.voto.agencia_con_secreto`/`R7.3`) ya tenían instrumento medido por
`MAESTRA35-L9`/`L11` — `R1.5` `NO-DISCRIMINA` (`dinero.ahorro.seguro_deposito_
enif2024`), `R7.3` ya `CONTRARIA-REPLICADA` y degradada `[FUERTE]`→`[MEDIA]` (Enmienda
D2-f). Ninguna de las dos se carga como `HIPÓTESIS-SIN-INSTRUMENTO`.

`T-A3`/`T-FIRMAS-2` (`T28`/`T29`) nuevos en `tests/check.py` — defecto real: el
encargo `MAESTRA38-N1-lite` nunca llegó a un commit empujado, `PR #530`/`ADR-335`
ejecutó su restauración sin encargo archivado. Control positivo: `T-A3` **FALLA**
contra el árbol antes de archivar `N1-lite`, `T-FIRMAS-2` ya **PASA** (salidas
pegadas en el `## CONSUMIDO` del encargo). `forense/encargos/2026-09-04-MAESTRA38-
N1-lite-REPARA-TABLERO-Y-COLA.md` archivado post-hoc, `## CONSUMIDO` con `PR #530`
— `T-A3` pasa a VERDE. `tests/baseline.json` sin recifrar por `P2`/`P3`: LÍNEA
BASE **VERDE**, 3 FAIL / 170 WARN. **Enmienda post-cierre, mismo día (CI de `PR
#535`).** Subir `gobernanza` a `338 ADR` desincronizó `canon/estado-programa-
v1_11.md` (`T15` a `ROJO`, 3 entradas) — el acto original no lo tocó por
perímetro (carril `N8`, disjunto); con la CI del PR realmente roja, dirección
pidió resolverlo ahí mismo, autorización puntual para esta cifra mecánica, y
`canon/estado-programa-v1_11.md` se recifró (`337`→`338 ADR`).
`B24` (§5) cerrado. Detalle completo en el `## CONSUMIDO` del encargo archivado:
`forense/encargos/2026-09-04-MAESTRA38-N6-PROPAGA-FP298-TESTS-Y-A3.md`.

### 8.6 Recibo — `ACTO MAESTRA38-N7 · PRE-REGISTRO-CIVICO-LAPOP` (4/sep/2026, sin ADR, `FP-300`)

No es un snapshot completo de indicadores; no toca `canon` (perímetro explícito —
`ADR-338` ya no está libre, lo tomó `N6` en §8.5). Sella dos specs de pre-registro
en `forense/prereg-caja/`, ampliando el conteo de `S1-S3` (3) a `S1-S5` (5):
**`S4-L4-spec-v1_0.md`** (`civico.voto.clientelar_si_observable`, objeto de `N5
§2.6`, LAPOP México 2019, `clien1n`/`clien1na` × `vb3n`, control `vb10`) y
**`S5-L5-spec-v1_0.md`** (`civico.protesta.agravio_urbano`, objeto de `N5 §2.8`,
multi-ola cerrada 2004/2006/2019 — 2021/2023 excluidas por no traer variable de
protesta —, `TAMANO` como estrato). Cada spec cierra con la lista de archivos que caja
necesita abrir (`id_manifiesto` + `sha256`) y la línea "medición: caja, acto
`MAESTRA38-L4`/`L5`", y ahora cita los ids estables que §8.5 ya cargó en la propuesta
(`civico.voto.clientelar_si_observable_lapop2019`,
`civico.protesta.agravio_urbano_multiola`) como el destino de su medición.

**Hallazgo central, por A.8/D-13 — ninguna de las dos es la primera medición de su
`id`, y parte del sello ya vivía en canon antes del `SHA` de redacción de este
encargo.** `MAESTRA35-L9`/`L11` (2/sep/2026) ya corrieron falsaciones reales de los
mismos dos `id` de canon, formalmente propagadas a `canon/modelo-decision-v4_0.md §7`
por las Enmiendas `D2-f`/`D2-d` (firma de mesa **3/sep/2026** — un día **antes** del
`a0e06da4` contra el que este encargo se escribió, y que el primer sello de esta
pieza no había citado):

- `civico.voto.agencia_con_secreto` (`R7.3`, la gemela de `clientelar_si_observable`
  en la misma disyunción del `SI`) — brazo de **observabilidad percibida** (LAPOP 2023
  `mexwf1_19`×`countfair3`→`vb20`, réplica ENCUCI 2020): `CONTRARIA-REPLICADA`,
  degradada `[FUERTE]`→`[MEDIA]` por `D2-f`. `S4` ataca el **otro** brazo de la
  disyunción de `civico.voto.clientelar_si_observable` (proximidad/focalización del
  reparto, único medible en la ola 2019 que trae la batería `clien*`, sin `D2-x` que
  lo toque) y declara por qué la celda de tres factores del encargo —oferta ×
  observabilidad × voto— no es construible en una sola ola.
- `civico.protesta.agravio_urbano` — el contraste `C2` (agravio × urbano, LAPOP 2019 +
  réplica ENCUCI 2020) está **`CARGADA-A-MOTOR`, tier `FUERTE`, `CORROBORADA-
  REPLICADA`** por `D2-d`; `C1` (entorno solo) queda `SELLADA-SIN-CARGA`, `[MEDIA]`,
  `AMBIGUA-ENTRE-INSTRUMENTOS` — no `PENDIENTE-DE-MESA` como el primer sello de esta
  pieza decía. `S5` completa el diseño de cuatro factores que `D2-d`/`L9` dejaron en
  dos, con los dos reactivos (`AOJ12` falla estatal, `CP6`/`CP9` red previa) que
  `data/inventario-reactivos-descargas-mx-v1_1.tsv` —nacido un día después de `L9`—
  sí trae, sin reabrir `D2-d`. Corrige además la caracterización de `N5` sobre
  `LAPOP-E8` (aprobación normativa, no asistencia propia).

`data/INFRAESTRUCTURA-v1_0.md` gana dos líneas (una por spec) bajo la sección
`forense/prereg-caja/`. `B24` — cerrado por `N6` (§8.5), no por esta pieza: la
referencia a "`B24` parcial" del primer sello se retira, D-13. Cero medición, cero
canon tocado, cero corpus abierto. Renumerado de `FP-299` a **`FP-300`** al fusionar
`origin/main` — `PR #535`/`N6` fusionó primero y tomó, de forma independiente, los
mismos candidatos `FP-299`/`ADR-338`; regla de la casa, renumera quien fusiona
segundo (coincide con el número que el encargo original citaba). Detalle completo,
incluidas las correcciones de premisa post-merge, en el `## CONSUMIDO` del encargo
archivado: `forense/encargos/2026-09-04-MAESTRA38-N7-PRE-REGISTRO-CIVICO-LAPOP.md`.

### 8.7 Recibo — `ACTO MAESTRA38-N8 · ESTADO-PROGRAMA-v1_12` (4/sep/2026, `ADR-339`, `FP-301`)

**Snapshot completo de canon, no de este tablero** — crea `canon/estado-programa-v1_12.md`,
retira `canon/estado-programa-v1_11.md` (§0 de abajo). No regenera este archivo
(`tools/tablero_programa.py` sigue fuera de perímetro de esta pieza); las cifras
vigentes viven ahora en `v1_12` §2/§11, no aquí.

**Qué hace.** Re-deriva por comando cada cifra que `v1_11` (2/sep) citaba sin
comando al lado o dejó envejecer mientras el árbol se movía debajo: motor
`10`→`20` reglas (`grep -cE '^  - id: ' milpa/tramite.yaml`), `19` con al menos
una conducta `MEDIDO`/`1` sin dato (`tramite.gobierno_digital.coercitivo`),
dominios activos `4` (`ADR-265`), corredor con `14` de `14` celdas sorteadas
puntuables (`R∩M∩L` completa sobre el marco `v1_2`), Ola 6 `0` de `6` dominios
abiertos con `salud` en `2` de `5` `EXISTE-SATISFACE` (`ADR-327`), manifiesto
`1 040`→`1 281` payloads, relaciones activas `222`/procedencias aceptadas
`223`/`utilidad-modelo.tsv` proyección 1:1 sin error (`python3 tools/curador_
registro/baseline.py data/curacion-registro`), ADR máximo `338`→`339` y FP
máximo `300`→`301` (con las propias entradas de cierre de este acto), las 9
reglas `NO-ENCONTRADO` clasificadas `2/5/2` (`MAESTRA38-N5`, con la corrección
de `D-13` de `N6` ya heredada: 2 de las 5 `SIN-INSTRUMENTO` ya medidas en
`L9`/`L11`), specs de caja selladas `3`→`5` (`S1`–`S5` de `forense/prereg-
caja/`), FAIL absorbidos `3` (`tests/baseline.json`: dos `T06`, un `T08`), y
`6` filas `PENDIENTE-DE-MESA` consolidadas de `PAQUETE-RECETAS-5` (4 filas) y
`-6` (2 filas, `0` de `2` recetas verificables en `NUBE`).

**Secciones nuevas.** §9 «Qué espera a la caja» — tabla de las cinco specs
congeladas (`MAESTRA38-A2` recenso, `L2` ICPSR 35024, `C1` re-asiento
`N36`→`N41`, `L4`/`L5` civico/LAPOP) con su primer resultado esperado. §10
«Qué no se sabe sin caja» — tres preguntas que ningún comando de `NUBE` cierra:
`C1` físico real (si `alta_relacion.py --dry-run` reproduce de verdad el
`relacion_id` pre-registrado `REL-e7c3700e98be2d9aa7bbd55e`), `[CENSO]`
(depende del `crontab` de mesa, `FP-282` sigue `ABIERTA`) y `ENFIH-4` (las
cuatro filas de `relaciones.tsv` bajo `FP-288`, sin resolver hasta que mesa
elija entre sus dos opciones).

**Desviación D-13, declarada contra el propio encargo (A.8, antes de fijar
nada).** El encargo pedía «`v1_11` queda intacta (historia)» y una enmienda de
una línea. Verificado contra `tests/check.py::t01_single_source` (una sola
versión viva de `canon/estado-programa-v*.md`) y contra el precedente
**idéntico** de este mismo artefacto — mesa ya corrigió esta exacta premisa
para `v1_10`→`v1_11` (`git rm canon/estado-programa-v1_10.md`, nota en
`tests/check.py:239-248`) —: dejar `estado-programa-v1_11.md` junto a `estado-programa-v1_12.md` es un `FAIL`
de `T01` nuevo, no baselineado. Este acto sigue el mecanismo del precedente, no
la prosa que lo repite: **retira `canon/estado-programa-v1_11.md`** del árbol
(`git rm`, historia recuperable con `git show 7574008:canon/estado-programa-
v1_11.md`, el commit de A.3 de este mismo acto). **ADR de este acto: `339`, no
el `340` que citaba el encargo** — re-derivado contra el árbol real (`338` era
el máximo, `MAESTRA38-N7` no tomó ningún ADR); **`FP-301` sí coincide** con el
encargo. Citas mecánicas vivas actualizadas: `tests/check.py`
(`_T25_ARCHIVOS_CONOCIDOS`, `HISTORICOS`), `.claude/commands/acto.md` (cita de
ejemplo del paso «Recifrado L0»); las citas de `canon/gobernanza-v1_15.md` y
`canon/registro-rotulos.tsv` a `v1_11` quedan intactas (registro append-only
de decisiones ya selladas).

Cero medición, cero regla del motor tocada, cero corpus abierto. `python3
tests/check.py --baseline`: **LÍNEA BASE VERDE**, sin entradas nuevas frente a
`tests/baseline.json`. Detalle completo en el `## CONSUMIDO` del encargo
archivado: `forense/encargos/2026-09-04-MAESTRA38-N8-ESTADO-PROGRAMA-v1_12.md`.

### 8.8 Recibo — `ACTO MAESTRA38-N9 · YA-MEDIDO` (5/sep/2026, `ADR-340`, `FP-302`)

**Defecto real, mismo patrón dos veces en la misma semana.** `MAESTRA38-N5`
clasificó `R1.5`/`R7.3` como `SIN-INSTRUMENTO` teniendo medición ya sellada
(`MAESTRA38-N6` lo corrigió, `FP-298`); el encargo de `MAESTRA38-N7` llamó
«territorio virgen» a `R7.4`/`R7.6`, pese a que `MAESTRA35-L9`/`L11` ya habían
pre-registrado y corrido falsaciones reales sobre esos mismos dos `id` dos días
antes. Ninguno de los dos actos cruzó, antes de clasificar/pre-registrar, las
fuentes del repo donde una medición real ya dejaba rastro.

**Qué hace.** `tools/ya_medido.py <id-de-regla|R-n>` (nuevo, P1) cruza en un
solo comando `milpa/tramite.yaml`, `milpa/tramite-ola5-propuesta-v0.yaml`,
`canon/modelo-decision-v4_0.md` §7, `forense/notas/*-L*-*.md` y `forense/
prereg-caja/S*-spec-*.md`, e imprime por fuente cada aparición con
`archivo:línea` y los campos `situacion`/`tier`/`veredicto`/`p` que traiga,
cerrando con `NUNCA-MEDIDA` o `MEDIDA-EN: <habitantes>`. Sin heurística de
parecido: el match es por `id` exacto y por `R-n` exacto; la única
equivalencia `id`↔`R-n` que conoce sale del registro congelado de `tests/
validador_registro_ids.py` (ancla cada `R-n` a su regla de §3 por subcadena
estable) cruzado con el tag `**id:**` que esa misma regla ya trae — nunca
inventada. El alias adicional de `canon/registro-rotulos.tsv` es solo el que
esa tabla ya declaraba. Control positivo verificado: `civico.voto.
clientelar_si_observable` y `civico.protesta.agravio_urbano` (los dos `id` de
`N7`) devuelven `MEDIDA-EN:` con `L9`/`L11` en la lista. Control negativo:
`familia.cortejo.urbano_joven_apps` devuelve `NUNCA-MEDIDA` — lo único que
hay es la hipótesis que `MAESTRA38-N6` cargó por `FP-298`.

**P2.** `.claude/commands/mapea.md` (§4, junto a la definición de
`HIPÓTESIS-SIN-INSTRUMENTO`) y `.claude/commands/acto.md` (ARRANQUE, junto a
A.8 contra la raíz) ahora piden pegar la salida de `ya_medido.py` en A.8 antes
de clasificar/pre-registrar/cargar/sellar una regla — una línea de regla, sin
compuerta nueva. `T30`/`T-YAMEDIDO` (`tests/check.py`) lo exige mecánicamente:
`FAIL` si un encargo archivado bajo `forense/encargos/` (no `cola/`) con fecha
de archivo ≥ hoy cita un `id`/`R-n` en su cuerpo sin que el archivo traiga
`NUNCA-MEDIDA`/`MEDIDA-EN:` — con un allowlist declarado
(`_T_YAMEDIDO_ARCHIVOS_CONOCIDOS`, mismo patrón que `_T25_ARCHIVOS_
CONOCIDOS`) para citas ilustrativas, como la de este mismo encargo sobre
`familia.cortejo.urbano_joven_apps` en su propio control negativo.

**P3.** `FP-301` (recibo de `MAESTRA38-N8`) recifrada `ABIERTA`→
`FIRMADA-POR-MERGE`: `PR #537` ya fusionado es la firma (regla 1 de
maestra-34), tal como la propia fila ya declaraba. `forense/hallazgos.md` gana
una línea nombrando el patrón repetido (`N5`/`N7`).

**Cascada.** `data/INFRAESTRUCTURA-v1_0.md` gana una sección nueva
(`tools/ya_medido.py`). `ADR-340` re-derivado contra el árbol (máximo real
`339`, contiguo — coincide con lo que el propio encargo citaba, sin
colisión); `FP-302` (recibo) coincide igual. Cero medición de México, cero
regla del motor tocada — el propio contador del encargo lo declara.

`python3 tests/check.py --baseline`: ver cierre del PR de este acto. Detalle
completo en el `## CONSUMIDO` del encargo archivado: `forense/encargos/
2026-09-05-MAESTRA38-N9-YA-MEDIDO.md`.

### 8.9 Recibo — `ACTO MAESTRA38-N10 · COBERTURA-COMPLETA-OLA6` (5/sep/2026, `ADR-341`, `FP-303`/`FP-304`)

**Mandato de mesa (4/sep/2026), verbatim:** «Entiendo que hay un mínimo y ese
mínimo para lanzar una ola es una cosa. Pero hoy no tenemos lo mínimo y no
quiero hacerlo al mínimo no después de haber invertido tanto en la
infraestructura que creamos.» El producto no es el mínimo que abre un
dominio: es el mapa completo de las 25 reglas de los 6 dominios candidatos y
el plan para cubrirlas todas.

**Universo, congelado por comando.** `canon/modelo-decision-v4_0.md`
`§3.2`/`§3.4`/`§3.6`/`§3.8`/`§3.9`/`§3.10` traen **25** reglas — verificado
dos veces (conteo de bullets `- **SI**` por rango de línea; cruce contra el
`REGISTRO` congelado de `tests/validador_registro_ids.py`) — no `~30` como
estimaba el encargo. `tools/ya_medido.py` corrido en las 25 antes de
clasificar: `NUNCA-MEDIDA` en las 25, sin excepción — sin discrepancia contra
`MAESTRA34-N5`/`MAESTRA36-N6`, que clasificaron por existencia de reactivo,
no por falsación real corrida.

**Tres pasadas independientes, no dos.** `MAESTRA34-N5` buscó en
`inventario-reactivos-v1_2`/`-ext` (241 591 filas, encuesta); `MAESTRA36-N6`
cruzó `data/manifiesto.yaml` (1 104 entradas, administrativo); **este acto
corre la tercera** — `busca_reactivos.py --tablas descargas_mx_v1_1`
(42 536 filas examinadas, 75 corridas, reusando las formulaciones de `N5`
sin inventar vocabulario nuevo) — universo que `MAESTRA38-N5` sí había usado
tres días antes, para otro dominio, y que trae LAPOP AmericasBarometer,
World Values Survey, `ENSANUT 2024` crudo y paneles AEJ/Compartamos no
indexados en `v1_2`/`ext`.

**Resultado: 3 `MEDIBLE-COMO-ESTÁ` · 3 `CON-CANDIDATA` · 19
`HIPÓTESIS-SIN-INSTRUMENTO`.** `salud.atencion.grave` y
`salud.vacunacion.disponible` (ya conocidas por `N5`) más
**`comunicacion.inseguridad.ver_oir_callar`, hallazgo nuevo de este acto**:
el módulo `AOJ` de LAPOP (`aoj1`/`aoj1a`/`aoj1b` como desenlace,
`AOJ11`/`B18`/`B10A`/`AOJ12` como antecedente, misma persona, mismo
instrumento, cinco olas 2004-2023) satisface el criterio con población
general — a diferencia de `ENDIREH` (N5, acotado a violencia de género) y
`CNGMD` (N6, sesgo de selección). `CON-CANDIDATA`:
`salud.adherencia.desabasto_vs_cuidadora` (`N36`/Cero Desabasto, ya
registrada `CANDIDATA/PENDIENTE_EVIDENCIA` desde `ADR-279`),
`cooperacion.comite.monitoreo_sancion_visible` y `cooperacion.faena.
sancion_social_pueblo_mestizo` (CNGMD, pendientes de abrir bytes —
`CAND-2`/`CAND-3` de `N6`). Las otras 19 quedan `HIPÓTESIS-SIN-INSTRUMENTO`,
cada una con instrumento mínimo escrito (una pregunta, una población);
`REFORMULABLE` queda en cero — todo intento de reformulación honesta
(10 `EXISTE-NO-SATISFACE` de encuesta + 7 administrativas) se verificó y
ninguno sobrevivió la regla de honestidad salvo el que resultó
`MEDIBLE-COMO-ESTÁ`.

**Criterio 2, como consecuencia — no se optimizó.** `motor-nucleo-medible-
v1_0.md` §3.a exige `≥3 EXISTE-SATISFACE` por dominio: `0` de `6` con lo
medible hoy, **`0` de `6` aun sumando las 3 adquisiciones con ficha** —
ningún dominio llega a 3 agotando todo lo nombrable hoy (el techo teórico es
`salud`/`cooperación`, 2 de sus reglas cada uno). **Pese a eso, los 6
dominios se declaran `COMPLETABLE`**: las 25 reglas, sin excepción, tienen
ruta escrita.

**Cascada.** `ADR-341` (candidato contra `340`, contiguo, coincide con el
que el propio encargo citaba). `FP-303` (decisión de mesa sobre el plan de
cobertura por dominio, vence 7 días) y `FP-304` (recibo). `canon/registro-
rotulos.tsv`: fila `MAESTRA38-N10` censada. Tres hallazgos en
`forense/hallazgos.md`: cero discrepancia contra `ya_medido.py` (declarada,
no omitida), la subida de `ver_oir_callar` a `MEDIBLE-COMO-ESTÁ`, y un
catálogo de homonimias de `busca_reactivos.py` repetidas entre reglas
("jefe"=jefe de hogar, "cortes"=tribunales/apagones, "favor"=guion de
enumerador, "grave"=problema nacional en LAPOP). Cero medición de México,
cero canon sustantivo tocado (solo la cascada mecánica de ADR/L0) — el
propio contador del encargo lo declara.

`python3 tests/check.py --baseline`: ver cierre del PR de este acto. Detalle
completo, seis tablas por dominio y tabla resumen, en `forense/notas/
2026-09-05-MAESTRA38-N10-cobertura-ola6.md`.

### 8.10 Recibo — `ACTO MAESTRA38-N11 · PRE-REGISTRO-OLA6-MEDIBLES-Y-FICHAS` (5/sep/2026, `ADR-342`, `FP-305`)

**Qué sella.** Tres pre-registros en `forense/prereg-caja/`, patrón `N7`
(`S4`/`S5`), para las tres reglas que `MAESTRA38-N10` clasificó
`MEDIBLE-COMO-ESTÁ`: `S6-L16` (`salud.atencion.grave`), `S7-L17`
(`salud.vacunacion.disponible`), `S8-L18`
(`comunicacion.inseguridad.ver_oir_callar`). `tools/ya_medido.py`
corrido en las tres antes de escribir: `NUNCA-MEDIDA`, sin excepción.

**Tres correcciones de premisa (A.8/D-13), ninguna anticipada por el
encargo.** `S6`: el árbol trae **dos** `EXISTE-SATISFACE` ya sellados
para `salud.atencion.grave` sobre reactivos que no se solapan —
`ENNVIH`+`ENDIREH` (`MAESTRA34-N5`/`MAESTRA37-L1`) y `ENSANUT2024`
(`MAESTRA37-L3`/`L3-BIS`) — sin que ninguna nota los reconcilie; la
afirmación de `L3` de heredar de `N5` no se sostiene contra el texto
real de `N5` (0 menciones de `ENSANUT`/`u0201`/`H0409`). `S6` pre-registra
las dos ramas en paralelo, sin adjudicar cuál prevalece — corregir esa
discrepancia queda fuera del perímetro de un pre-registro. `S7`: la
ficha original de `N5`/`N10` para `salud.vacunacion.disponible` cita
variables (`cen12_1a`/`he25c`/`ce19d_2`/`hs16d_2`) que **no** están en
`data/inventario-reactivos-descargas-mx-v1_1.tsv` — viven en
`data/inventario-reactivos-ext-v1_0.tsv`, el universo de `N5`; `S7`
corrige la cita y, además, aporta un **hallazgo nuevo**: el bloque
`a0927a1`-`a0927e4` de `adultos_ensanut2024_w.dta` (razón de no
vacunación por vacuna nombrada — "no había vacunas"/"no era
derechohabiente"/"no estaba quien aplica"/"estaba enfermo"/"otra razón")
prueba el `PORQUE` de la regla ("el hueco es logístico, no actitudinal")
más directamente que la ficha original, y ni `N5` ni `N10` lo habían
citado. `S8`: el desenlace del módulo `AOJ` de LAPOP (`aoj1`/`aoj1a`/
`aoj1b`) existe **solo en la ola 2004** — verificado variable por
variable, ola por ola — no en "las mismas cinco olas" que `N10 §2.6`
describe de corrido; `S8` acota el falsador a esa sola ola, con
2006/2019/2021/2023 citadas solo como evidencia de estabilidad del
antecedente, no como parte del diseño.

**Fichas de las tres candidatas, en la cola.** Vía el escritor canónico
(`tsv_crudo.upsert_fila` sobre `data/curacion-registro/cola-adquisicion-
registro.tsv`, vista regenerada): `salud.adherencia.desabasto_vs_cuidadora`
(cita `N36`, ya registrada), `cooperacion.comite.monitoreo_sancion_visible`
(cita `N28`, ya registrada), `cooperacion.faena.sancion_social_pueblo_
mestizo` (sin `N` asignada — verificado, `0` filas en `necesidad-objeto-
modelo.tsv` para `R8.4`; se propone `N42` en la nota de la fila, sin
editar esa tabla, fuera de perímetro). `PAQUETE-RECETAS-7`: `SIN-FETCH`
declarado — `HEAD` sobre las tres URLs de las fichas (`cerodesabasto.org`,
`mapadecuidados.inmujeres.gob.mx`, `inegi.org.mx/rnm`) desde NUBE → `000`
en las tres (proxy de egreso rechaza la conexión, política de
organización); 3 URLs examinadas, 0 alcanzables (A.13); no se crea el
archivo condicional.

**Corrección de mapa.** `canon/registro-rotulos.tsv`: `salud.vacunacion.
disponible` es regla de §3.9 (información), no de §3.4 (salud) — el `id`
conserva el prefijo por historia; corrección de mapa, no de canon.

**Cascada.** `ADR-342` (candidato contra `341`, contiguo, coincide con
el que el propio encargo citaba). `FP-305` (recibo — este acto no
depende de `FP-303`, que sigue abierta por cuenta de `N10`). `canon/
registro-rotulos.tsv`: fila `MAESTRA38-N11` censada, junto a la fila de
corrección de mapa (P3). Cero medición de México, cero canon sustantivo
tocado (`canon/modelo-decision-v4_0.md` intacto) — el propio contador
del encargo lo declara: specs selladas `5`→`8`, filas de cola `+3`.

`python3 tests/check.py --baseline`: ver cierre del PR de este acto.
