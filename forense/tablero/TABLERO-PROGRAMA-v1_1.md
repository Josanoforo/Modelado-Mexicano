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
| **B24** | **NUEVO · Mesa decide las 9 reglas `NO-ENCONTRADO` clasificadas por `MAESTRA38-N5`** (`FP-298`): por regla, aceptar/rechazar 2 `REFORMULABLE`, 5 `SIN-INSTRUMENTO` (`MANTENER-COMO-HIPÓTESIS` propuesto) y 2 `CON-CANDIDATA` — tabla en `forense/notas/2026-09-04-MAESTRA38-N5-diseno-9-reglas.md` §3 | mesa | `FP-298`, 4/sep | firma por regla, en RH; vence 11/sep |

**Cerrados en esta ventana.** **B1** (dominio dinero sin celda puntuable) por PR #479. **B8** ya venía cerrado. **B10** (canon de estado desactualizado) por PR #485, *con reserva*: el archivo nuevo está en PROPUESTA hasta FP-251. **B15** se reformula como B21: los encargos de `MAESTRA35-L3` sí aterrizaron; el de `MAESTRA35-L4` no.

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
`AOJ12` + `CP6`/`CP9`/`E8` + `TAMANO`) — con objeto reformulado, reactivo, instrumento
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
