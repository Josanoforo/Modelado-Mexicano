# ACTO GEN2-LOTE-MEDICION-PENDIENTE-1 · cierre — cuatro filas `NC` de microdato, un lote D-11: la premisa «puro COMMIT-2» era falsa y el trabajo caro se hizo igual

**Acto:** `ACTO GEN2-LOTE-MEDICION-PENDIENTE-1` · 14/sep/2026 · CAJA (Ubuntu/WSL2, corpus compartido, red INEGI 200) · Opus · rama `acto/gen2-lote-medicion-pendiente-1` · worktree `/home/pc0/mm-gen2-lote-medicion-pendiente-1`
**Encargo:** `forense/encargos/2026-09-14-GEN2-LOTE-MEDICION-PENDIENTE-1.md` (A.3, verbatim, 0-bis `01dab9a`; llegó como brief de despacho «2 · CAJA», sin `FIRMAS DE MESA` ni compuerta; «corre detrás del RUN» = carril, `PR #756` ya `MERGED`).
**Base:** `a29d873` al abrir (PR #759) → `7de3acb4` tras `0.a` (PR #761) → `a3ed97f` al cerrar (PR #763). Cero conflictos en los tres merges.
**Commits:** `01dab9a` (0-bis) · `e99aa21` (COMMIT-1: tres specs + tres CALC congelados) · `059c6ae` / `6868630` / `84f38fc` (COMMIT-2 a/b/c: sellos) · `eedceca` + `4481986` (COMMIT-3 de la pieza P2: spec v1.1 + sello) · `d21840e` (registro) · cascada.

---

## 0 · ARRANQUE, en cinco líneas

0.a `git rev-list --count HEAD..origin/main` = 0 tras merge (`a29d873`; luego +6 y +3, fusionados). 0.b árbol limpio. 0.c `ls-remote`/`worktree list`/`gh pr list` sin el rótulo. 0.d `limpia_arbol --reporta`: 88 worktrees, base al día, 1 rama fuera de política (`claude/tramite-2026-09-14`, ajena). `data/raw` enlazada a `/home/pc0/mm-corpus/raw` (+ `raices.local.yaml` del clon padre). `tools/entorno.py --sonda-red`: `CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE=sin_variable · red=200 · corpus=SI(examinados=413) · numpy 2.3.5 · pandas 2.3.3 · scipy 1.16.3 · pyreadstat 1.3.6`. Espejo: ninguna cifra sale de él.

## 1 · Premisas del encargo, contrastadas contra el árbol

| pieza | lo que el encargo declaró | lo real |
|---|---|---|
| P1 | «correr el CALC de la spec EDER-CORRESIDENCIA-DISENO-spec-v1_0 … cero corridas la consumen (grep -i corresid: 0) … puro COMMIT-2» | **FALSO en la sustancia.** La spec v1_0 ya corrió como `CALC-EDER-0001` en el mismo PR #760 que la congeló (`corridas.tsv` la lista por el id del CALC, no por la palabra «corresidencia» — el grep léxico buscó la palabra equivocada). `NC-0184` pide **otro estimando** (`adulto_familiar_actual`, universo Jefe/Cónyuge de `MAESTRA33-C1`), que v1_0 §4.2 excluyó explícitamente. Se hizo el COMMIT-1 nuevo (spec hermana) y el COMMIT-2. |
| P2 | «la ruta U4 en ENVIPE 2012 vía join a tsdem por N_REN == R_SEL; 0 filas U4/tsdem-2012 en corridas.tsv» | CIERTO. Ningún `spec.yaml` de 83 declara `archivo: tsdem.DBF` ni `tper_vic.dbf`. |
| P3 | «fase 1 declaró 66.89%; la corrida mide 67.53/68.06» | CIERTO en las cifras; **falsa la nota de `NC-0125`** «el script de fase 1 no existe en el árbol»: existe (`tools/medidor_horizonte_enif24.py`) y su log está archivado (`data/l7-log-pieza-d.txt`). |
| P4 | «adjudicar la categoría colapsada P4_10» | La adjudicación es de mesa; este acto produce las **cotas** con que adjudicar. |

**Hipótesis H1 (P3), formulada desde el árbol antes de abrir el dato:** 66.89 % = 9 031 / 13 502 = fracción **sin ponderar** del **universo triple** de L7 (`P3_13 ∈ {1..7} ∧ P4_10 ∈ {1..5}`), no la cobertura de `P3_13` (68.97 %) ni la ponderada del lote.

## 2 · Resultados por pieza

### P1 · `CALC-EDER-0002` — `familia.corresidencia.adulto_familiar_actual` con diseño (`NC-0184` → CERRADA)

| `RESULT` | valor |
|---|---|
| `A-P` (sucesor, `factor`) | **0.0575307** (`A-REPRODUCE-GEN1 = REPRODUCE`, Δ −2.86e-07 vs `0.057531`; `A-ADOPCION = LISTADO-PARA-MESA-REPRODUCE`) |
| `A-N-U` | **9 397** (Δ 0); `A-EMBUDO-C1 = EMBUDO-COINCIDE` (94 101 · 23 831 · 16 687 · 9 397) |
| IC95 de diseño (bootstrap UPM en `est_dis`, 2 000 réplicas) | **[0.051658, 0.063726]**, `IC-CON-ESTRATOS-DE-UPM-UNICA` (289 estratos, 3 150 UPM, **9** con UPM única → límite inferior) |
| Taylor (cotejo) | EE 0.003375 → [0.050915, 0.064146] |
| `B-P` (`factor_per`, sensibilidad) | **0.056374**, IC [0.050188, 0.062679]; `B-DELTA-VS-A = −0.001156` (−0.12 pp) |
| desenlace | 522 ego con `d = 1` (453 con ascendiente, 244 con suegro, solapes), 8 875 con `d = 0`; `A-SUMA = 1.0` |

El punto de C1 se reproduce al séptimo decimal y el IC de bootstrap simple de filas (`[0.051297, 0.063913]`, no comparable, A-bis.3) queda **sucedido** por un IC de diseño. Consumidor único `tramite-ola5-propuesta-v0.yaml:192` (`SELLADA-SIN-CARGA`): sin cita GEN2, **listado para adopción de mesa**; `milpa/` intocado.

### P2 · `CALC-ENVIPE-U4-2012` + `-v1_1` — la ruta a `tsdem`, declarada y medida (`NC-0099` → CERRADA)

**La ruta, con su cardinalidad:** 32 493 delitos → `U1` = 14 532 (`G-CONTROL-U1 = REPRODUCE`: `P-C1-U1 = 0.29557241046799515` y `N-U1` exactos a `CALC-R-CIV-M-01`) → **9 854 personas seleccionadas** candidatas (`(CONTROL, VIV_SEL, HOGAR, R_SEL)`; 0 con `R_SEL` discordante, 0 sin hogar en `tper_vic`) → `FAC_ELE` resuelto por hogar: `tper_vic.dbf` trae **una fila por integrante** (311 436 = `tsdem`, 0 hogares con filas ≠ `TOT_PER`) y **en 74 944 de 83 483 hogares `FAC_ELE` no es constante**: sólo la fila de la persona seleccionada trae un `FAC_ELE` válido `> 0` (rama 2 de la regla pre-declarada; 0 ambiguos) → join a `tsdem` por `N_REN == R_SEL`: **9 854 / 9 854 con exactamente una fila, 0 con cero, 0 con más de una**; 0 menores de 18, 35 con edad no especificada (sólo contados). **`N-U4 = 9 854`**, masa `FAC_ELE` 9 959 198.

| `RESULT` | v1.0 | v1.1 |
|---|---|---|
| `P-C2-U4` (partición GEN1, persona) | **0.338397** | idéntico (`G-CONTROL-V1-0 = REPRODUCE`) |
| `P-C1-U4` | 0.306970 | idéntico |
| estratos / UPM / UPM única | **4** / 6 486 / 0 | **355** / 6 486 / **44** |
| IC95 `C2-U4` (bootstrap) | [0.321230, 0.354993] | **[0.322115, 0.355328]** (límite inferior) |
| Taylor `C2-U4` | EE 0.008678 | EE 0.008781 |

**Hallazgo que motivó la v1.1** (COMMIT-3 de la pieza, D-11): el FD de 2012 declara `EST` «Estrato de diseño muestral, 001…303» para `TPer_Viv`, `TSDem` y `TMod_Vic`; **el archivo lo contradice en dos**: `tper_vic.dbf` y `tsdem.DBF` traen en `EST` un dígito con dos espacios (`'1  '`…`'4  '`; por su forma, un estrato socioeconómico — la misma clase de `EST_SOC` que `VERIFICACION-CAJA-2` halló sin documentar en 2013), y sólo `Tmod_Vic.DBF` trae el de diseño (361 valores; un solo par `(EST, UPM)` por hogar en los 19 648, `UPM` idéntico al de `tper_vic` en todos). v1.0 queda sellada e intacta (su IC está estratificado por 4 estratos); v1.1 toma el par de `Tmod_Vic` y no cambia el punto. **`NC-0098` conserva 2013/2015** (la ruta vale para 2012; 2015 trae `ID_PER` y no la necesita).

### P3 · `CALC-ENIF-0003` — la cobertura reconciliada por recuento (`NC-0125` → CERRADA)

| fracción | valor | veredicto |
|---|---|---|
| `P3_13 ∈ {1..7}` / 13 502, sin ponderar | 9 312 / 13 502 = **0.689676** | `68.97` **REPRODUCE** (log L7) |
| `P3_13 ∈ {1..7}`, ponderada `FAC_PER` | 0.675320 | `67.53` **REPRODUCE** (lote ENIF-1) |
| `P3_13 ∈ {1..7, 9}`, ponderada | 0.680578 | `68.06` **REPRODUCE** (= 1 − 0.319422) |
| universo triple, sin ponderar | **9 031 / 13 502 = 0.668864** | **`66.89` LOCALIZADA:UNIVERSO-TRIPLE-NO-PONDERADA** · `H1 = REPRODUCIDA` |
| universo triple, ponderada | 0.654976 | — |
| `0.668937` (`propuesta-v0.yaml:2169`) | ninguna de las dos a 6 decimales | `NO-REPRODUCE` (residuo de 7.3e-05 en una cifra escrita a mano; la de dos decimales sí) |

`C-VEREDICTO-GUARDIAS-GEN1 = COINCIDEN` (4275/2443/3405/1328/1479/74/498; 9 312). **El «residuo no explicado» de `NC-0125` no era residuo de medición: eran tres cantidades distintas.** La `clase` que `MAESTRA35-N8` selló en `milpa/tramite.yaml:1082,1112` («cobertura declarada 66.89%») es la cobertura del **universo de la pieza** (9 031 de 13 502, sin ponderar), no la del reactivo `P3_13`; el lote ENIF-1 midió la del reactivo, ponderada. Corregir la prosa histórica de `tramite.yaml` es cosmético y de mesa (mismo criterio que `NC-0106`): **`NC-0189`**.

### P4 · `CALC-ENIF-0003` — la categoría colapsada, acotada (`NC-0126` sigue ABIERTA: adjudica mesa)

Proxy declarado antes del dato: «no ahorró por ninguna vía en 12 meses» (`P5_1_1..6 ≠ 1 ∧ P5_6_1..9 ≠ 1`) — **cota**, no valor, de «no tiene ahorros».

| universo (`FAC_PER`) | n | sin ninguna vía | IC95 |
|---|---|---|---|
| `P4_10 = 1` («< 1 semana / no tiene ahorros») | 4 275 | **0.6356** (2 724) | [0.6156, 0.6544] |
| `P4_10 = 2` («≥ 1 semana, < 1 mes») | 2 443 | **0.3771** (861) | [0.3505, 0.4062] |
| `P4_10 ∈ {3,4,5}` | 6 212 | 0.1539 (948) | — |
| población 18+ | 13 502 | 0.3579 (4 803) | — |

En los universos del lote: `U_A_SIN` (n 4 973): **19.96 pp** del universo es `P4_10 = 1 ∧ ninguna vía` — es decir, **60.4 %** [57.1, 63.3] de quienes tienen `P4_10 = 1` y **36.9 %** del corte primario `{1,2}`; `U_A_CON` (n 3 969): **9.29 pp**, **53.4 %** [48.9, 57.8] del código 1, **24.9 %** del corte `{1,2}`. Lectura, sin adjudicar: **el colapso muerde** — el código 1 está dominado por no-ahorradores (63.6 %) y el 2 no (37.7 %), así que el corte `S1 = {1}` mezcla dos poblaciones en proporción ≈ 3:2 y el primario `{1,2}` lleva ≈ un tercio de «1 ∧ ninguna vía». Con estas cotas, mesa decide si el corte se mantiene, se mueve o se pide otro reactivo. 80 estratos con UPM única sumados en los cuatro IC (límite inferior).

## 3 · Registro

`registro --verifica` (dry-run 4m50s) proyectó **+4 corridas, +260 `RESULT`, 0 transiciones** de `resultado_replay`/`contexto_replay` (no hizo falta `--lote`); `--verifica --escribe` escribió `corridas.tsv` (168) y `resultados.tsv` (4 743); `usos.tsv` idéntico (207: cero adopciones). Pisada medida contra la base excluyendo las cuatro corridas: **163 filas de 4 corridas ajenas cambian sólo `fuente_replay`** de `VERIFY-EN-ESTA-SESION` a `VERIFY-ESTRUCTURADO · ACTO GEN2-VERIFICACION-CAJA-2` (el recibo de #761 ya en `main`): refresco hacia la fuente más autoritativa, ninguna otra columna. `verify` aislado ×2 en las cuatro corridas: `REPRODUCE · CONTEXTO=IDENTICO` 8/8. Las cuatro nacen `cuenta_gen2 = PENDIENTE-DE-MESA` (§5).

## 4 · Hallazgos

1. **Un grep léxico sobre `corridas.tsv` no prueba que una spec no tenga corrida.** El registro identifica la corrida por el id del CALC; buscar la palabra del rótulo humano dio 0 sobre 166 filas y la spec ya estaba corrida. Conjunto, no léxico.
2. **El FD de ENVIPE 2012 documenta `EST` como estrato de diseño en tres tablas y sólo una lo trae.** `tper_vic`/`tsdem`: 4 valores con espacios; `Tmod_Vic`: 361. Sin la guardia `N-ESTRATOS` la v1.0 habría publicado un IC de 4 estratos como IC de diseño. Manda el archivo; el descriptor se cita y se contradice con conteo.
3. **`FAC_ELE` en 2012 vive en una sola fila por hogar** (74 944 de 83 483 hogares con más de un valor; la única válida es la de la persona seleccionada): la regla de resolución pre-declarada (rama 2) absorbió el caso sin adivinar; 0 ambiguos.
4. **Tres números de «cobertura» eran tres cantidades.** 66.89 = universo triple sin ponderar; 68.97 = `P3_13` sin ponderar; 67.53 = `P3_13` ponderada. Una fila `NC` que dice «no se reconcilia» puede estar comparando definiciones distintas — y decir que el script no existe cuando existe.
5. **`P4_10 = 1` es 63.6 % no-ahorradores en 12 meses; `P4_10 = 2`, 37.7 %.** La cota es interna a ENIF; la sonda externa (IIEG Jalisco, `GEN2-38`) no hacía falta para acotar.

## 5 · Contador y firmas

Cuatro corridas selladas GEN2 (`CALC-EDER-0002`, `CALC-ENVIPE-U4-2012`, `CALC-ENVIPE-U4-2012-v1_1`, `CALC-ENIF-0003`; 260 `RESULT`), **todas `cuenta_gen2 = PENDIENTE-DE-MESA`**: el encargo llegó sin firma de mesa con OBJETO sobre el contador (estándar FP-367/368) y el ejecutor no la inventa → **`FP-375`** (firma de contador para las cuatro; `decisiones.tsv` sin fila). `NC` cerradas: **0184, 0099, 0125**. Nueva: **`NC-0189`** (corrección cosmética de `tramite.yaml:1082,1112`, mesa). `NC-0126` sigue abierta con las cotas de §2-P4 para adjudicar; `NC-0098` conserva 2013/2015. Numeración: `NC-0186..0188` ya redactadas en `PR #762`/`#764` (0186 dos veces) → se saltan.

**Actualización 15/sep/2026 — `FP-375` firmada, OPCIÓN A (revertida, ver abajo).** Primer intento: `cuenta_gen2 = SI` para las cuatro corridas del lote, escrito además en `etiquetas.cuenta_gen2`/`firma_de_contador` de cada `spec.yaml`. CI lo rechazó: editar un `spec.yaml` de un CALC ya **sellado** rompe `sello.json` (cubre `spec.yaml`; "una corrida sellada es evidencia histórica, no se reescribe" — `tools/corrida0.py::run()`). Los 4 `spec.yaml` se revirtieron a su contenido sellado original (commit `fcddf9a`); la firma quedó viviendo únicamente en `data/corrida0/decisiones.tsv`, que tiene precedencia D-1 sobre la etiqueta de la spec (`_cuenta_gen2_resuelto`) — funcionalmente suficiente, sin tocar bytes sellados.

**Actualización 15/sep/2026 — `FP-375` firmada, OPCIÓN B (vigente, ADENDA P0 de dirección).** Sustituye a la opción A. OBJETO 1: `cuenta_gen2 = SI` para `CALC-EDER-0002`, `CALC-ENVIPE-U4-2012-v1_1` y `CALC-ENIF-0003` (**tres** corridas, no cuatro). OBJETO 2: `CALC-ENVIPE-U4-2012` (v1.0) queda **NO** contado — superado por v1_1 en la práctica, `cuenta_gen2 = NO` vía `decisiones.tsv` (motivo: superada por v1_1, precedente FP-367→368); su `CALC`, bytes y sello no se tocan (E.3). Guardia A.8/A.13 previo a escribir OBJETO 2: `comm -23` de `RESULT-ENVIPE-U4-12-*` (sin `V11-`) contra `RESULT-ENVIPE-U4-12-V11-*` → **vacío**, 57/57 absorbidos por la v1_1 — sin huérfanos. Escrito solo en `data/corrida0/decisiones.tsv` (4 filas actualizadas, sin tocar ningún `spec.yaml`); registro re-derivado (`corrida0.py demanda` + `registro --escribe`, tras traer `origin/main` fresco — PR #775 mergeado, `MEDICION-DEMANDA-1`). `N_corridas_selladas` 63→**66**, `N_resultados_gen2_sellados` 2882→**3085** (+74 EDER-0002, +64 ENVIPE-U4-2012-v1_1, +65 ENIF-0003 — el `CALC-ENVIPE-U4-2012` v1.0, 57 `RESULT`, no suma). `N_resultados_gen2_pendientes_adopcion` sin cambio (5): esta firma sella, no adopta.

**Limitación declarada, `NC-0199` (ABIERTA):** el campo `estado` de `CALC-ENVIPE-U4-2012` en `corridas.tsv` sigue leyendo `SELLADA`, no `SUPERADO→CALC-ENVIPE-U4-2012-v1_1` — el `spec.yaml` de la v1_1 declara `repite_de` bajo `etiquetas:`, y `tools/corrida0.py` (línea ~3241) solo lee `spec.get("repite_de")` a nivel raíz, no vía `_etiqueta()`. No se movió el campo (spec sellada, E.3). Sin efecto numérico: `cuenta_gen2=NO` vía `decisiones.tsv` ya excluye la v1.0 de los contadores igual que si dijera `SUPERADO→`; el control de reproducibilidad de la v1.0 sigue contado dentro de la v1_1 como `RESULT-ENVIPE-U4-12-V11-G-CONTROL-V1-0`. Sucesor: acto que arregle la lectura de `repite_de` en `corrida0.py` sin tocar specs selladas.

## 6 · Límites declarados

Ninguna corrida es ciega (ADR-46; contaminación en cada spec §0) · IC de diseño como **límite inferior** donde hay estratos de UPM única (P1: 9; P2 v1.1: 44; P4: 80 acumulados) · `factor_per` es sensibilidad, no sucesor · U4 2012 no se compara con 2025 ni con GEN1 (no existe en unidad persona para 2012) · el proxy de P4 es cota · `milpa/` intocado (`git diff --stat origin/main -- milpa/` vacío) · cero adopciones · cero descargas · cero llamadas a modelos.

## 7 · A.13 — qué se examinó

Descriptores: `fd_envipe2012.xls` (hojas `TPer_Viv` 985 filas, `TSDem` 114, `TMod_Vic`), `enif_2024_fd.xlsx` (hoja `TMODULO`), la spec de C1 y el FD de EDER vía sus specs. Cabeceras/descriptores DBF de las 4 tablas de 2012; cabeceras de los 4 CSV de EDER y de `TMODULO.csv`. Microdato, sólo por los medidores sellados en COMMIT-2/3: `eder2017_bases_csv.zip` (`bcc7eb90…`), `base_de_datos_envipe_2012_dbf.zip` (`d7caa74e…`), `enif_2024_bd_csv.zip` (`00e4b0b4…`); más una lectura diagnóstica post-sello de `EST`/`UPM` en las tres tablas de 2012 para atribuir el hallazgo 2 (no cambió ningún resultado sellado). Registro: `registro --verifica` re-ejecutó todas las corridas selladas; `spec-check` 16/22/20/22 OK sobre 317 718 filas de inventario. Sin abrir: `tvivienda.dbf`, ENVIPE 2013/2015, EDER 2011/2025.
