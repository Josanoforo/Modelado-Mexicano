# Nota · ACTO SELLA-ADV — cierre

**Fecha:** 2026-08-20 · **Rama:** `claude/lanzamiento-2026-08-19-4eret8` · **Encargo:** `forense/encargos/2026-08-20-SELLA-ADV.md` (§4 del paquete de lanzamiento; §0-§3 y §6 son contexto compartido con `CONTRATO-v0_5`, que no arranca en este acto).
**Base:** `origin/main = 5a60e98687fe23f34edea831bcc296b858b19d04` — re-verificado por `git fetch` al escribir esta nota, sin cambio desde el arranque.
**Entorno:** `CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE=cloud_default` (NUBE), crudo, sin sonda — coincide con lo esperado. `data/raw`: no se usa, no montado, no consultado.

---

## 1 · Compuerta de arranque — dos tiempos, no uno

El encargo llegó como texto puro, sin adjuntos. La compuerta exige cuatro documentos con sha256 declarado; ninguno de los cuatro, ni el paquete Fable, estaba en el árbol ni en el sistema de archivos al arrancar — verificado por `find`/`grep` antes de tocar nada. Siguiendo el precedente que el propio encargo cita (`ADR-124`, "si falta o no coincide alguno, PARA — el paro es correcto"), esta sesión reportó el estado y esperó en vez de fabricar contenido.

Tres documentos llegaron en un primer mensaje del usuario, con sus nombres de adjunto originales (no rutas del repo): *informe_ADV2_estado_del_arte_y_rubrica.md*, *ADV1_demolicion_duelo_v1.md*, *compass_artifact_wfd3f091379eb25e3ebf34dc2883351e73_text_markdown.md*; los tres verificaron sha256 exacto contra la tabla del encargo. Un segundo mensaje trajo el cuarto (*ADV1_demolicion_duelo_L_vs_M.md*, sha256 exacto) más un quinto documento no nombrado en la compuerta — el careo de dirección (*CAREOADVDUELOyDISENOv2.md*) — y una segunda copia, byte-idéntica (`cmp` limpio), de *ADV1_demolicion_duelo_v1.md*. Los cinco se renombraron al aterrizar (`T1`, §4 abajo); ninguno de los cinco nombres de adjunto de este párrafo existe como ruta del repo a propósito.

**Los cuatro documentos de la compuerta verificaron sha256 exacto, comparación de cadena programática, no visual** (los cuatro `EXACT MATCH`, 64 caracteres cada hash). El paquete Fable (`1822bde0…`) nunca llegó como archivo verificable — no bloqueó `T1`, que exige literalmente "los cuatro"; queda declarado, no fabricado (`forense/hallazgos.md`, y el bloque `→ Vigente` de `ADR-128`).

## 2 · Por qué se archiva un quinto documento fuera de "los cuatro"

`forense/CAREO-ADV-DUELO-diseno-v2-2026-08-19.md` no trae sha256 en la compuerta del encargo. Se archiva de todos modos porque es la fuente verbatim de `ADV1-M1`…`ADV1-M6` — sin su texto, `T2(e)` no podría citar los mecanismos que `D-4` sella con precisión, solo parafrasearlos de memoria (exactamente el defecto que este programa existe para evitar). Su propio §D describe un acto sucesor (`§T-SELLO`→`DUELO-PREREG-V2`) que **no** es el que esta sesión ejecuta — mesa sustituyó ese plan tentativo por `SELLA-ADV`/`CONTRATO-v0_5`, con firmas `D-1`…`D-6` propias, verbatim, distintas de las `D-i`…`D-iv` del careo. Se cita el careo por su contenido técnico (`ADV1-M1` … `ADV1-M6`), no por su plan de ejecución.

## 3 · Re-verificación de existencia (A.8), no heredada

`§0` del encargo declaraba: `compass-4` ya en el árbol (encontrado entre 7 archivos de una búsqueda de "los pobres no pagan"); los otros cuatro `NO-ENCONTRADO`. Re-derivado en esta sesión contra `git show`/`git grep` sobre `5a60e98` (no sobre el árbol de trabajo, que ya contiene los documentos aterrizados por `T1`):

```
git ls-tree -r --name-only 5a60e98 | wc -l                    → 1717
git grep -Fc "ROMPE-DISEÑO" 5a60e98                            → 0
git grep -Fc "Fragile Families Challenge" 5a60e98              → 0
git grep -Fc "silicon crowd" 5a60e98                           → 0
git grep -Fc "INDECIDIBLE si" 5a60e98                          → 0
git grep -Fc "skill score" 5a60e98                             → 0
git grep -Fc "Metaculus" 5a60e98                                → 0
git grep -Fc "duelo v2" 5a60e98                                 → 0
git grep -Fc "los pobres no pagan" 5a60e98                     → 7 archivos, incluido corpus/forense/compass-4-e29a28d4-credito-popular-2026.md
```

Coincide exacto con `§0`. `data/curacion-registro/celdas-d/`: tres archivos, verificado por `find`. `data/INFRAESTRUCTURA-v1_0.md`: no cubre archivo de documentos adversariales — verificado por `grep`, confirma el hueco que `§4` anticipaba; se usó el precedente más plano (`forense/BENCHMARK-conf02-…`), y se abrió `FP-78` en vez de decidir en silencio.

## 4 · T1 — aterrizaje, mecánica

Cada documento se copió por bytes desde el adjunto (nunca retipeado) y se le insertó una cabecera de procedencia entre el título y el cuerpo, replicando la estructura exacta de `compass-4` (título / línea en blanco / nota en blockquote / línea en blanco / cuerpo original sin tocar). Verificado con `diff` contra cada adjunto: los cuatro muestran únicamente la inserción de dos líneas (cabecera), y el `compass` además la diferencia de salto final esperada (`\ No newline at end of file` en el original) — exactamente el patrón que `T1` exige, no aproximado.

El nombre de adjunto original del quinto (*compass_artifact_wfd3f091379eb25e3ebf34dc2883351e73_text_markdown.md*) se renombró a `compass-5-d3f09137-estado-arte-duelo-2026.md`, replicando el patrón de `compass-4` (shortid tomado de los 8 caracteres tras `wf`, tema + año). Destino de los cinco: `forense/` (flat), no `corpus/forense/` ni `forense/adv-duelo/` — decisión de `§2`, registrada como abierta en `FP-78`.

## 5 · T2 — `ADR-128`, decisiones que no estaban en el guion

Dos cosas que ninguna instrucción anticipó con ese nombre y que esta sesión tuvo que resolver leyendo, no adivinando:

- **La excepción del umbral (1) de `ADR-68(c)`** exige que `tests/test_motor_holdout.py` lo cite — verificado (`:9`, `:104`), cita textual confirmada antes de escribir la excepción en el ADR.
- **El censo de `M5`/`E-n` del `§2` del encargo no se copió: se re-derivó.** El recuento de `M5` (cuatro habitantes) coincidió con el del encargo tras verificar cada uno por lectura de línea, no por grep de cadena. El de `E-n` **no coincidió**: esta sesión encontró siete rótulos distintos (`E0`, `E2`, `E3-TRIAGE`, `E4a`, `E4b`, `E4c`, `E5`), no seis. La cifra derivada aquí es la que quedó escrita en `ADR-128(g)` y en `canon/registro-rotulos.tsv` — no se forzó la coincidencia con el encargo.

## 6 · T4 — alcance declarado del censo de rótulos

`canon/registro-rotulos.tsv` re-deriva por comando los espacios "sanos" (`ADR-NNN`, `FP-NN`, `TNN`, `conf.NN`, `A.N`) y documenta por lectura individual los dos que colisionan (`M`, `E`). No re-derivó fila por fila los espacios `G`/`N`/`R`/`H`/`S`/`U`/`D` del censo original (8-33 usos cada uno, sin señal de colisión) — declarado como límite de método en el propio `.tsv` y aquí, no omitido en silencio. Si alguno de esos namespaces resulta colisionar, es trabajo para un acto sucesor con ese perímetro.

## 7 · T5 — `T-ROTULOS`, límite declarado

`tests/check.py` gana `T25`/`T-ROTULOS`: `FAIL` si un archivo `.md` **nuevo** de `canon/`o `forense/` trae `M<n>` o `E<n>`/`E-<n>` pelado sin prefijo, con un snapshot de 149 archivos ya conocidos (derivado por `python3` sobre el árbol real, no tecleado) como excepción — mismo patrón de granularidad de archivo, no de línea, que `T22(b)`/`T-FIRMAS` ya usa. **No** intenta detectar cualquier espacio de rótulo nuevo que alguien invente (`K3`, `P7`, …): un regex general se ahoga en falsos positivos de prosa. `T25` entra en `[ ok ]` desde su primer commit — verificado, no supuesto.

## 8 · Cascada — lo que no estaba en la lista de T1-T6 y hubo que hacer de todos modos

Sellar `ADR-128` movió el conteo de ADR (127→128) y el WARN (`FP-78` nueva, `ABIERTA`) — `T15`/`T16` lo exigieron con `FAIL` hasta que se propagó:

- `canon/gobernanza-v1_15.md`: cabecera 127→128 ADR; una cita histórica de "127 ADR" dentro del propio `ADR-127` marcada `{cita-historica}` (quedó stale por este recifrado, no se edita el sentido del ADR).
- `canon/estado-programa-v1_10.md`: `L0` 127→128 ADR; dos declaraciones de WARN (119→120) y FAIL (sin cambio, 21 núcleo sin `T16`), cada una con su propio párrafo de recifrado, seis años de precedente idéntico como modelo.

Verificado por comando en cada paso, no por aritmética de mesa — `python3 tests/check.py` corrido después de cada edición hasta llegar a punto fijo.

## 9 · Suite final

```
$ python3 tests/check.py --baseline
════════════════════════════════════════════════════════════════════════
  21 FAIL · 120 WARN
════════════════════════════════════════════════════════════════════════
LÍNEA BASE: VERDE — nada nuevo frente a tests/baseline.json (HEAD congelado e24d033ed3c095f1e81c2fbb8248f108e9d3ef65)
(1 entradas de la línea base ya no aparecen — mejora, no bloquea, no baja la cifra congelada sin --freeze explícito)
```

Sin `--freeze`. El único movimiento frente a la base declarada por el encargo (21 FAIL · 119 WARN) es **+1 WARN** de `T22` por `FP-78` (`ABIERTA`) — mecanismo ya documentado exhaustivamente en `canon/estado-programa-v1_10.md`.

## 10 · Lo que queda abierto, dicho y no escondido

- **`FP-78` (`ABIERTA`):** sitio canónico de un `compass` archivado. No bloquea nada ejecutado hoy.
- **El paquete Fable (`1822bde0…`):** nunca llegó como archivo. No bloqueó `T1`. Si existe y es distinto de los cinco documentos ya archivados, un acto sucesor puede traerlo y citarlo — no se re-construye de memoria aquí.
- **La colisión `E-n` es de siete, no de seis** — corregido contra el encargo, no heredado.
- **Los namespaces `G`/`N`/`R`/`H`/`S`/`U`/`D`** no se auditaron fila por fila en este acto.

**Contadores de medición sobre México: cero.** Este acto no corre ninguna estimación nueva; aterriza insumos, sella un diseño de piloto, declara vencimiento de alcance sobre reglas de proceso, y registra una convención de rótulos — dicho, no omitido, como exige `§6` del paquete de lanzamiento.
