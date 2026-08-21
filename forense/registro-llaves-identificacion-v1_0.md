# Registro de llaves de identificación ejercidas
### `registro-llaves-identificacion` · **v1.0** · 11 de agosto de 2026 · ENCARGO A (nube) · abre el contador que ADR-67(c) creó sin renglón

> | | |
> |---|---|
> | **ARCHIVO** | `registro-llaves-identificacion-v1_0.md` |
> | **NOMBRE ESTABLE** | **`registro-llaves-identificacion`** — cítalo así, nunca por nombre de archivo |
> | **QUÉ ES** | Registro append-only, una fila por llave de identificación (ADR-57(c)) o por diseño que la ejercería. Población de conteo propia — **`llaves de identificación ejercidas`** — abierta por ADR-67(c) (`canon/gobernanza-v1_15.md:868`), que la nombró sin darle renglón donde anotarse. |
> | **QUÉ NO ES** | No adjudica ningún veredicto de Hito D ni mueve su denominador. No sella nada: todo veredicto de aquí es **PROPUESTO** hasta que mesa lo firme. No es la taxonomía RUTA-A/I/C/SIN-RUTA (esa vive en `censo-estimabilidad-coeficientes-v1_0.md` y tampoco está sellada por ADR). |
> | **VERIFICAS ASÍ** | §4 trae el comando de conteo, corrido contra este mismo archivo antes de escribirse aquí — salida esperada hoy: `0`. |

---

## 0 · Qué es una llave

`ADR-57(c)` (`canon/gobernanza-v1_15.md:623`) sella la compuerta de identificación: cualquier afirmación de intervención ("si se interviene X, pasa Y") exige una **llave de identificación declarada y sellada**, de una de tres clases, citadas aquí verbatim de esa misma línea:

> "(i) panel con el desenlace en el instrumento (mismos sujetos entre olas); (ii) experimento natural con grupo de comparación sobre encuestas repetidas; (iii) diseño experimental de terceros (evaluaciones aleatorizadas publicadas, clase Progresa/Oportunidades), usado como evidencia (a) con su cita."

Un coeficiente o regla clasificado `RUTA-I` en `forense/censo-estimabilidad-coeficientes-v1_0.md` (definición en su §1, línea 26: *"Identificada, llave sellada y no ejercida"*) tiene la llave **sellada y no ejercida**: la vía existe y está verificada para ese caso concreto, pero ningún diseño que la use ha corrido todavía. **Ejercerla** es correr un diseño pre-registrado que use esa llave — no basta con nombrarla, y una fase meramente descriptiva sobre el mismo panel tampoco basta si no llega a emitir un veredicto de identificación.

Fuente de la taxonomía de rutas: `forense/censo-estimabilidad-coeficientes-v1_0.md`. Acto que crea este contador: `ADR-67(c)`.

---

## 1 · La regla de contadores — verbatim de ADR-67(c), no reinterpretada

`canon/gobernanza-v1_15.md:868` (ADR-67, inciso (c)), citado sin editar:

> "el denominador **27 no se toca** (cuenta fichas del pre-registro original, y `R5.1`→`A` de ADR-58 queda como historia con su estampa de universo — diseño transversal por recepción declarada, régimen de 5 instrumentos, con la reserva que ADR-58 dejó escrita); la métrica del renglón nuevo es **llaves de identificación ejercidas** (hoy 0), que `R5.1-D2` movería a 1 si corre conforme a su pre-registro sellado."

Este registro es una **población de conteo distinta** de la de Hito D. Ninguna fila de aquí mueve `13 de 27` (Hito D, `estado-programa-v1_10.md:95`), `15 coeficientes, cero medidos` (misma línea — el "0 de 15" que cita el encargo que abrió este acto es una paráfrasis; el texto vigente en el archivo dice literalmente "15 coeficientes, cero medidos", corregido aquí sin editar la fuente), `9 de 14` (corregido de `8 de 14`, vencido desde el 4/ago/2026; fuente vigente `modelo-decision-v4_0.md:277`, Encargo K, 4/ago/2026) ni `4 de 144` (`estado-programa-v1_10.md:97`).

Un veredicto anotado en la tabla de abajo es **PROPUESTO** hasta que mesa lo firme — la clase `A`–`E` del Hito D **no aplica aquí**; la escala de cada fila es la que su propio pre-registro declaró (Bloque B-bis, `instrucciones-proyecto-v2_4.md`).

---

## 2 · Vocabulario de `estado` — cerrado

| estado | significa |
|---|---|
| `SELLADA_NO_EJERCIDA` | pre-registro sellado, diseño no corrido |
| `EJERCIDA_CORROBORA` | corrió y el falsador no refutó; la regla queda corroborada en el alcance declarado |
| `EJERCIDA_ACOTA` | corrió, no refutó, y el resultado acota el alcance de la regla — se dice a qué |
| `EJERCIDA_REFUTA` | corrió y refutó |
| `EJERCIDA_INDECISA` | corrió y el falsador resultó demasiado débil para decir nada — se dice por qué |
| `NO_EJECUTABLE` | el diseño no se pudo correr; se dice si fue por dato, por entorno o porque nadie corrió el mecanismo (las tres son hallazgos distintos y no se colapsan) |

Solo `EJERCIDA_*` cuenta como llave ejercida.

---

## 3 · Tabla de llaves

Filas iniciales: la que el censo clasifica `RUTA-I` (1 de las 15 filas de coeficientes de generador, verificado en §4 con la receta del propio censo) más la fila que ADR-67(c) nombró y dejó sin renglón, `R5.1-D2`. Ambas nacen `SELLADA_NO_EJERCIDA` — ninguna llave de la lista está ejercida hoy (`gobernanza:623`, verbatim).

| llave_id | coeficiente_o_regla | diseño | preregistro_ref | estado | veredicto | escala_del_veredicto | fecha | ADR | clase_ADR57c |
|---|---|---|---|---|---|---|---|---|---|
| `CAL-G3` | `G3 → horizonte_temporal` (−0.60), fila 5 de `censo-estimabilidad-coeficientes-v1_0.md` §5, única fila `RUTA-I` de las 15 | panel (ENNViH/MxFLS, tres olas — llave (i) de ADR-57(c)) | `forense/hitoD-preregistro-v2_0.md` Nota 7 (líneas 478-524, sellada 29/jul/2026), Adenda 1 (525-553), Nota 8 (554-648), Nota 10 (649+, Fase C corrida) | `SELLADA_NO_EJERCIDA` | — | `CAL-A`/`CAL-B`/`CAL-C`/`CAL-D`/`CAL-X` (Nota 7 §9a) — declarada, **no invocada**: Nota 10 corre Fase C completa sobre olas 2-3 pero es descriptiva y, verbatim, *"sigue sin emitir `CAL-A`/`B`/`C`/`X` y no entra al bloque de abajo"* (`hitoD-preregistro-v2_0.md:634`). El censo (§5, fila 5, columna Prioridad) declara además que falta el **diseño intra-persona** para promover de descriptivo a identificado — no concedido todavía, no es un instrumento nuevo lo que falta | 29/jul/2026 | — (ficha de `hitoD-preregistro`, sin ADR propio; nombrada por `ADR-57(c)`) | **(i)** — ya rotulada así en la columna `diseño` desde que este registro abrió (*«panel (ENNViH/MxFLS, tres olas — llave (i) de ADR-57(c))»*); este acto no la re-adjudica, solo la traslada a columna propia. Adjudicada `ADR-143` |
| `R5.1-D2` | la regla `R5.1` del Hito D — la pregunta sustantiva de si la elegibilidad al programa sustituye transferencia intrafamiliar hacia mayores, no la operacionalización por recepción declarada de ADR-58 | cuasi-experimental, diferencias-en-diferencias por grupo de elegibilidad (ENIGH 2018 → 2022) | `forense/r5-1-diseno-por-regla-preregistro-v1_0.md` (sellado 4/ago/2026, §9 sin enmiendas a la fecha) | `EJERCIDA_INDECISA` | **Fila B — Ambiguo, no refuta ni confirma.** Firma de mesa (ACTO ADJ-4, 13/ago/2026): *"Adjudico fila B, `EJERCIDA_INDECISA`."* Los dos desenlaces cumplen DiD<10pp-o-signo-contrario (transferencia +2.32pp, corresidencia −0.81pp — Commit 8 §2), pero la segunda condición conjuntiva de la fila A, "monto documentado como suficiente", **no se sostiene** con la medida sellada (razón monto/`gasto_mon`, no ingreso): 29.05% media ponderada, IC95% (26.16%, 31.94%) variante dominio / (25.95%, 32.14%) variante extensión-cero — entero por debajo del piso de 33% en las dos (Commit 9 §4/§7, Commit 10 §3-4). Por la precedencia sellada `A → E → B → C → D` (ADR-71(b)), la cláusula de "monto insuficiente" de B gana sobre A y sobre E sin excepción por magnitud del DiD. Fila propuesta y verbatim citada de `forense/notas/2026-08-12-e4c-r5-1-d2-commit10-incertidumbre-razon.md:56` (§4): *"No cambia la fila propuesta (B, `EJERCIDA_INDECISA`) ni la precedencia citada en Commit 9 §7."* — **no** del transfer del 12-13/ago, cuyo titular dice "fila A" (arrastrando el veredicto retirado de Commit 8) mientras su propio cuerpo, siguiendo Commits 9-10, confirma B; el repo es la fuente, no el titular del transfer. | **INCOMPLETA — no nombra el desenlace de no-refutación.** §6 del propio pre-registro, citado verbatim: fila `A` = "DiD <10pp... **La regla se refuta a este nivel de identificación también**"; fila `B` = "DiD entre 10 y 20pp... **Ambiguo — no refuta ni confirma**"; fila `C` = archivo por panel de persona no sostenido en disco; fila `D` = archivo por diseño (hueco de identificación de la clave de pensión contributiva, o muestra insuficiente). Ninguna de las cuatro filas nombra el caso "DiD ≥20pp con identificación exitosa y monto suficiente" — evidencia limpia de que la brecha **no** converge — como corroboración: ese desenlace cae fuera de A (exige <10pp), fuera de B (exige 10-20pp explícito), fuera de C (exige que la reserva dominante sea específicamente ausencia de panel) y fuera de D (exige fallo de diseño). Es el defecto de B-bis: se ve antes de correr, no después. E4c arranca con la instrucción de **reportar** este vacío, nunca de forzar una fila que la escala sellada no contempla. **CERRADO 12/ago/2026 por ADR-71(b):** el pre-registro gana fila `E` (§9, antes apéndice suelto a §6, reubicado por E4c Paso 3 §0.1) — DiD >20pp decisivo (IC95% que despeja el umbral) en al menos uno de los dos desenlaces, monto documentado como suficiente e identificación de §2 exitosa, corroboración acotada — con precedencia sellada **A → E → B → C → D**; la cláusula de "monto insuficiente" de B gana sobre E sin excepción por magnitud del DiD, igual que ya ganaba sobre A. La escala está completa desde esa fecha; la observación original de 4/ago queda arriba, sin borrar. | 4/ago/2026 | 67(c) | **(ii)** — *experimento natural con grupo de comparación sobre encuestas repetidas*. Los tres elementos de la definición sellada están escritos, no inferidos, en `forense/r5-1-diseno-por-regla-preregistro-v1_0.md` §2: el **corte natural** es el cambio de regla de elegibilidad de 2019 (desaparece la prueba de ingreso por pensión contributiva de $1,092/mes); el **grupo de comparación** es explícito (*«elegible en ambos regímenes»*, quien ya era elegible bajo la regla vieja); las **encuestas repetidas** son ENIGH 2018→2022, transversales, no panel. Falla (i) por definición (2018 y 2022 no son los mismos sujetos) y (iii) por definición (no hay aleatorización de terceros). Adjudicada `ADR-143`, `ACTO ADQ-ENOE-PRE2019` T3 |

| `R5.1-D3` | la misma regla `R5.1` del Hito D, misma pregunta sustantiva que `R5.1-D2` — tercer diseño sobre ella, y segundo de la familia "por regla de elegibilidad" | cuasi-experimental, diferencias-en-diferencias por grupo de elegibilidad (ENIGH 2018 → 2022), con el criterio `D-1` firmado por mesa: umbral **deflactado** a pesos constantes de 2018 ($4,034.74/trim en 2022) y hogares mixtos T/C **excluidos** del desenlace de corresidencia, con universo ACOTADO declarado (A-bis r4) y el marginal recalculado sobre ese universo; sensibilidades obligatorias pre-declaradas: (i) umbral nominal, (ii) universo completo con la regla *any-member* | `forense/bbis-r5-1-d3-v1_0.md` (COMMIT A, congelado 19/ago/2026 antes de abrir microdato) sobre `forense/r5-1-diseno-por-regla-preregistro-v1_0.md` (sellado 4/ago/2026), firma `ADR-110(a)`/`FP-54`, benchmark `forense/BENCHMARK-R51D3-hogares-mixtos-2026-08-18.md` | `EJERCIDA_INDECISA` | **Fila B — sellada por dirección, LOTE·NUBE-DECISIONES-1/T6 (FP-69), 19/ago/2026, verbatim "FIRMO FP-69: B se sella".** Corrida primaria (universo ACOTADO × umbral deflactado): DiD corresidencia **−1.82pp**, IC95% (−5.11pp, +1.48pp) — **cruza cero**; transferencia `P040` +2.32pp, IC95% (+0.54pp, +4.10pp); identificación de `P032` exitosa. La compuerta de monto **empeora** en vez de destrabarse: razón `P104`/`gasto_mon` per cápita pasa de 29.05% (población de `R5.1-D2`) a **26.45%** (personas T en hogar T del universo `U1`/ACOTADO), IC95% (23.15%, 29.75%) — entero bajo el piso de 33%. Por la precedencia sellada `A → E → B → C → D` (`ADR-71(b)`): la primera condición de `A` (DiD<10pp o signo contrario) se satisface, la tercera (identificación de `P032`) también, pero la segunda (monto suficiente) **no se sostiene** — la cláusula de "monto insuficiente" de `B` gana sobre `A` y sobre `E` **sin excepción por magnitud del DiD**. Las tres sensibilidades obligatorias caen en la misma fila (Commit B, `forense/notas/2026-08-19-ficha-r51-d3-resultados.md`). Reserva que va con la firma, heredada del propio pre-registro: el supuesto de tendencias paralelas está escrito y **no verificado** — el placebo 2014→2018 sigue sin correr. Mapeo al vocabulario de §2 aplicado: `B`→`EJERCIDA_INDECISA`, exactamente como esta misma fila ya anticipaba antes de sellarse (columna siguiente). | Heredada verbatim del pre-registro sellado, **no re-derivada**: filas `A`/`E`/`B`/`C`/`D` de §6 tal como quedaron tras `ADR-71(b)`, con precedencia `A → E → B → C → D` y la cláusula de "monto insuficiente" de `B` ganando sobre `A` y sobre `E` sin excepción por magnitud del DiD. Mapeo al vocabulario de §2: `A`→`EJERCIDA_REFUTA` · `E`→`EJERCIDA_ACOTA` · `B`→`EJERCIDA_INDECISA` (la fila que se selló) · `C`/`D`→`NO_EJECUTABLE` o archivo por diseño. Regla de adjudicación entre corridas, declarada al sellar (`bbis-r5-1-d3` §6): **adjudica la corrida primaria** (universo ACOTADO × umbral deflactado); las sensibilidades no votan — no discreparon, las tres caen en la misma fila | 19/ago/2026 | 67(c) (regla de renglón propio); 110(a) (criterio `D-1` firmado); ADR del lote, LOTE·NUBE-DECISIONES-1/T6 (sella, no re-deriva) | **(ii)** — misma adjudicación y por la misma razón: `bbis-r5-1-d3` §6 declara el mismo corte, el mismo grupo de comparación y las mismas dos olas transversales, con el criterio `D-1` encima. Adjudicada `ADR-143`, `ACTO ADQ-ENOE-PRE2019` T3 |

**Contador vigente: `2` llaves ejercidas de `3` filas.** *(Movido 13/ago/2026, ACTO ADJ-4 — `R5.1-D2` firma `EJERCIDA_INDECISA`, primera llave que sale de `SELLADA_NO_EJERCIDA` desde que este registro abrió. Verificación en §5. Denominador movido 19/ago/2026, ACTO FICHA-R51-D3 — entra la fila `R5.1-D3` naciendo `SELLADA_NO_EJERCIDA`; el numerador no se movió en ese acto porque proponía y no firmaba. **Numerador movido de nuevo 19/ago/2026, LOTE·NUBE-DECISIONES-1/T6 (`FP-69`)** — dirección sella fila `B`/`EJERCIDA_INDECISA` para `R5.1-D3` (firma verbatim "FIRMO FP-69: B se sella"), segunda llave que sale de `SELLADA_NO_EJERCIDA`. **CORRECCIÓN DE PREMISA, material:** el encargo que autorizó este sello anticipaba "2 de 2" — verificado por la propia receta de este archivo (§4), el denominador ya había subido a 3 el 19/ago/2026 (alta de `R5.1-D3`, antes de esta firma), así que sellar su numerador da **2 de 3**, no 2 de 2; no hay una segunda fila que retirar del denominador. Verificación por la receta de §4 en §7.)*

---

## 4 · Receta de conteo — probada antes de escribirse

**Primer intento, ingenuo — descartado y declarado, no silenciado.** `grep -c 'EJERCIDA_' registro-llaves-identificacion-v1_0.md` sobre el archivo completo contaría también la fila `SELLADA_NO_EJERCIDA` de la tabla de vocabulario (§2) si el patrón no exigiera el guion bajo final, y colapsaría llave_id con estado si se contara por línea física en vez de por columna — el mismo modo de falla que `instrucciones-proyecto` advierte para `grep -c "^## R"`. Se corrige acotando el conteo a la sección `## 3 · Tabla de llaves` y extrayendo la columna `estado` (sexta columna de la tabla, campo 6 tras dividir por `|`) en vez de buscar la subcadena en la línea completa.

**Receta corregida:**

```
sed -n '/^## 3 · Tabla de llaves/,/^## /p' forense/registro-llaves-identificacion-v1_0.md \
  | grep -E '^\| `' \
  | awk -F'|' '{print $6}' \
  | grep -c 'EJERCIDA_'
```

Denominador (filas de datos de la tabla):

```
sed -n '/^## 3 · Tabla de llaves/,/^## /p' forense/registro-llaves-identificacion-v1_0.md \
  | grep -cE '^\| `'
```

**Corrida contra este archivo tal como quedó escrito:** numerador `0`, denominador `2`. `llaves de identificación ejercidas: 0 de 2`.

La columna `estado` nunca contiene la subcadena `EJERCIDA_` (con guion bajo final) salvo en sus cuatro valores `EJERCIDA_*` — `SELLADA_NO_EJERCIDA` termina en `EJERCIDA` sin guion bajo posterior y no coincide con el patrón, verificado arriba. Cuando la primera fila `EJERCIDA_*` aparezca, esta receta la cuenta sin tocarse.

---

### 4.1 · Verificación del denominador `RUTA-I` citado en §3 (línea 55) — corregido, Acto A′

§3 dice que la fila `RUTA-I` (1 de las 15 filas de coeficientes de generador) queda "verificado en §4 con la receta del propio censo". Esa derivación nunca se copió a este §4 — vivía solo en `forense/hallazgos.md:121` (Encargo E-CE, 4/ago/2026). Se corrige citando aquí el comando y su salida cruda, corridos contra el estado actual de `forense/censo-estimabilidad-coeficientes-v1_0.md` (su propia receta, §7 de ese archivo):

```
grep -E '^\| [0-9]+ \|' forense/censo-estimabilidad-coeficientes-v1_0.md \
  | grep -oE 'RUTA-[CIA]|SIN-RUTA' | sort | uniq -c
```

Salida real:

```
      3 RUTA-A
      2 RUTA-C
      1 RUTA-I
      9 SIN-RUTA
```

`3 + 2 + 1 + 9 = 15` — coincide con las 15 filas de datos del censo (`grep -cE '^\| [0-9]+ \|' forense/censo-estimabilidad-coeficientes-v1_0.md` = `15`). El reparto discrimina correctamente: `RUTA-I = 1`, la cifra que §3 línea 55 cita como denominador de la primera fila de la tabla.

---

## 5 · Firma de mesa — `R5.1-D2`, 13/ago/2026 (ACTO ADJ-4)

**Firma, verbatim:** *"Adjudico fila B, `EJERCIDA_INDECISA`."* Mesa firma sobre lo que el propio repo ya tenía derivado (E4c Paso 3, Commits 8-10) — este acto no corre ningún diseño nuevo, no recalcula ningún estimador, solo adjudica cuál fila de la escala ya sellada (ADR-71(b)) gobierna el resultado ya producido. Detalle completo de la fila en §3, columnas `estado`/`veredicto` de la fila `R5.1-D2`.

**La trampa evitada, declarada.** El transfer del 12-13/ago que trajo este encargo titula la fila con el veredicto de Commit 8 ("fila A", `EJERCIDA_REFUTA`) — superado dentro del propio E4c antes de que el transfer se escribiera: Commit 9 (`forense/notas/2026-08-12-e4c-r5-1-d2-commit9-monto-gasto.md:62`) retira A y propone B con la medida correcta (`gasto_mon`, no el proxy de ingreso de Commit 8 §4), y Commit 10 (`forense/notas/2026-08-12-e4c-r5-1-d2-commit10-incertidumbre-razon.md:56`, §4) lo confirma con intervalo tras calcular el IC95% de RM: *"No cambia la fila propuesta (B, `EJERCIDA_INDECISA`) ni la precedencia citada en Commit 9 §7."* Esta firma sigue al repo (B), no al titular del transfer (A) — ni intuición, ni el encargo, deciden la fila; la decide la escala ya sellada aplicada al resultado ya corrido.

**El contador se mueve según la receta propia de este archivo (§4), no por decreto de este encargo.** Corrida contra el archivo tal como queda escrito tras esta firma:

```
$ sed -n '/^## 3 · Tabla de llaves/,/^## /p' forense/registro-llaves-identificacion-v1_0.md \
    | grep -E '^\| `' | awk -F'|' '{print $6}' | grep -c 'EJERCIDA_'
1
$ sed -n '/^## 3 · Tabla de llaves/,/^## /p' forense/registro-llaves-identificacion-v1_0.md \
    | grep -cE '^\| `'
2
```

**`llaves de identificación ejercidas: 1 de 2`** — coincide exacto con lo que el encargo esperaba (`0 de 2 → 1 de 2`); la receta no dijo otra cosa. Se propaga a `canon/estado-programa-v1_10.md` (línea del contador de llaves) en el mismo acto.

---

## 6 · Alta de la fila `R5.1-D3`, 19/ago/2026 (ACTO FICHA-R51-D3) — denominador movido, numerador no

**Qué entra.** La fila `R5.1-D3`, naciendo `SELLADA_NO_EJERCIDA`, igual que nacieron `CAL-G3` y `R5.1-D2`. Su pre-registro es `forense/bbis-r5-1-d3-v1_0.md` (COMMIT A), congelado antes de que la sesión abriera ningún ZIP de `data/raw`, sobre el pre-registro sellado del 4/ago y con el criterio `D-1` que mesa firmó en `ADR-110(a)` (`FP-54`).

**Por qué renglón propio y no una edición de la fila `R5.1-D2`.** Por la misma razón que `ADR-67(c)` dio para abrir aquella: *"una fila por diseño escala; una fila por pregunta obliga a sobrescribir para siempre."* `R5.1-D3` no es una re-corrida de `R5.1-D2`: cambia la regla de hogar del desenlace de corresidencia y promueve el umbral deflactado de sensibilidad a especificación primaria. Sobrescribir la fila de `R5.1-D2` borraría el `EJERCIDA_INDECISA` que `ADJ-4` firmó.

**El numerador no se mueve en este acto.** El acto **propone**, no firma — misma disciplina que `E4c` Commit 8 respetó y que `ADJ-4` cerró. Si mesa firma un `EJERCIDA_*` para `R5.1-D3`, el numerador pasa a `2` en el acto de adjudicación, no aquí.

**Corrida de la receta de §4 contra el archivo tal como queda tras esta alta** — con `command grep`, no con el `grep` del entorno (que es `ugrep -I` y descarta archivos con un byte no-UTF8 en silencio; aquí ambos coinciden, verificado, y se declara el mecanismo igual):

```
$ sed -n '/^## 3 · Tabla de llaves/,/^## /p' forense/registro-llaves-identificacion-v1_0.md \
    | command grep -E '^\| `' | awk -F'|' '{print $6}' | command grep -c 'EJERCIDA_'
1
$ sed -n '/^## 3 · Tabla de llaves/,/^## /p' forense/registro-llaves-identificacion-v1_0.md \
    | command grep -cE '^\| `'
3
```

**`llaves de identificación ejercidas: 1 de 3`** — derivado por la receta, no tecleado. Se propaga a `canon/estado-programa-v1_10.md` en el mismo acto.

**Lo que esta alta NO hace, y su razón sellada.** No escribe ninguna línea en el bloque append-only de `hitoD-preregistro` ni mueve `13 de 27`. El encargo que abrió este acto y `ADR-110(a)` declaran que `FICHA-R51-D3` es *"la vía al 14 de 27"*; `ADR-67(c)` selló lo contrario antes, y `T18`/`T20` lo confirman por mecánica independiente (el contador es un `set` de identificadores `RX.Y`, y `R5.1` ya está dentro desde el 4/ago/2026). La contradicción queda registrada como `FP-68`, **ABIERTA** — no se adjudica desde aquí.

---

## 7 · `FP-68` se adjudica y `FP-69` se sella, 19/ago/2026 (LOTE·NUBE-DECISIONES-1/T6)

**`FP-68` — la colisión de contadores se resuelve a favor de `ADR-67(c)`, sin adjudicación nueva que hacer.** No hay dos reglas válidas compitiendo: `ADR-110(a)`/el encargo `FICHA-R51-D3` declararon que este diseño era *"la vía al 14 de 27"*, pero esa declaración nunca fue una regla sellada de mesa sobre el denominador — era una premisa heredada, no verificada contra `ADR-67(c)`, que **ya** había sellado la regla real el 10/ago/2026 (`canon/gobernanza-v1_15.md:868`): un veredicto de diseño por regla de elegibilidad **no** cuenta como veredicto de `R5.1` para el bloque append-only de `hitoD-preregistro`, el denominador **27 no se toca**, y la métrica del renglón nuevo es **llaves de identificación ejercidas** — este mismo registro, creado por ese ADR para exactamente este propósito. Confirmado además por mecánica independiente, no solo por regla escrita: `T18`/`T20` (`tests/check.py`) derivan el contador de Hito D de un `set` de identificadores `RX.Y` vía `_VEREDICTO_CANONICO`, y `R5.1` **ya está** en ese set desde el 4/ago/2026 (`R5.1`→`A`, `ADR-58(c)`) — una línea nueva para `R5.1-D3` no incrementaría `13 de 27` aunque se escribiera, y una línea con la forma literal `` `R5.1-D3` → veredicto `` no coincide con el patrón que el parser reconoce y entraría **invisible**, sin disparar ni el guardia de forma sospechosa. **Propaga, sin tocar el original:** `ADR-110(a)` (`canon/gobernanza-v1_15.md:2151`) queda con su texto intacto — su declaración de que `FICHA-R51-D3` sería "la vía al 14 de 27" se corrige por ADR nuevo que la cita, patrón `ADR-112`→`ADR-110(d)` / `ADR-122`→`ADR-113` ya precedentado; detalle completo en el ADR del lote, subsección `T6`. **Contador de llaves que resulta de aplicar esta regla:** ver `FP-69` abajo — `FP-68` por sí sola no mueve el numerador, solo confirma dónde vive.

**`FP-69` — fila `B` sellada, numerador movido a `2`.** Firma de dirección, verbatim en el mensaje de lanzamiento del lote: *"FIRMO FP-69: B se sella"*. Ejecutada en la fila `R5.1-D3` de §3 arriba: `estado` `SELLADA_NO_EJERCIDA` → `EJERCIDA_INDECISA`; `veredicto` con la narrativa completa (DiD, compuerta de monto, precedencia, reserva de tendencias paralelas). Mismo mecanismo de firma que el precedente exacto que la propia fila `FP-69` cita: `ACTO ADJ-4` sobre `R5.1-D2`, 13/ago/2026 (§5 arriba) — mesa/dirección adjudica cuál fila de una escala **ya sellada** (`ADR-71(b)`, vía `bbis-r5-1-d3` COMMIT A) gobierna un resultado **ya corrido** (`bbis-r5-1-d3` COMMIT B); este acto no corre ningún diseño nuevo ni recalcula ningún estimador.

**Contador re-derivado por la receta de §4, no tecleado:**

```
$ sed -n '/^## 3 · Tabla de llaves/,/^## /p' forense/registro-llaves-identificacion-v1_0.md \
    | grep -E '^\| `' | awk -F'|' '{print $6}' | grep -c 'EJERCIDA_'
2
$ sed -n '/^## 3 · Tabla de llaves/,/^## /p' forense/registro-llaves-identificacion-v1_0.md \
    | grep -cE '^\| `'
3
```

**`llaves de identificación ejercidas: 2 de 3`.** **Corrección de premisa, material:** el mensaje de lanzamiento que autorizó este sello nombraba "2 de 2" como resultado esperado — verificado contra la receta de este archivo, el denominador **ya** había subido a 3 el 19/ago/2026 (alta de `R5.1-D3`, `ACTO FICHA-R51-D3`, antes y de forma independiente de esta firma) y ninguna fila sale del denominador al sellar `B`. El resultado correcto, derivado y no supuesto, es **2 de 3**. Se propaga a `canon/estado-programa-v1_10.md` en el mismo acto.

**Hito D no se mueve — dicho sin adorno, como el propio mensaje de lanzamiento exige.** `13 de 27` queda exactamente donde estaba: esta fila nunca entra al bloque append-only de `hitoD-preregistro` (ver `FP-68` arriba), y su veredicto `EJERCIDA_INDECISA` no es un veredicto de Hito D en absoluto — es un veredicto sobre si el **diseño** identifica algo, población de conteo distinta desde que `ADR-67(c)` la abrió (§1). Ninguna línea de `canon/hitoD-preregistro-v2_0.md` se toca por este acto.

**Lo que este acto NO hace.** No re-corre ningún diseño ni recalcula ningún estimador — la corrida ya vive en `bbis-r5-1-d3-v1_0.md` COMMIT B, congelada. No verifica el supuesto de tendencias paralelas (reserva declarada, placebo 2014→2018 sigue sin correr). No edita `ADR-67(c)` ni `ADR-110(a)` — los cita. No escribe en `canon/hitoD-preregistro-v2_0.md`.

---

## 8 · Adjudicación de clase contra la taxonomía de ADR-57(c), 20/ago/2026 (`ACTO ADQ-ENOE-PRE2019`, T3)

**Qué pedía `FP-64`, verbatim:** *«R5.1-D2 … nunca fue adjudicada contra la taxonomía de tres clases — su diseño (DiD por elegibilidad sobre transversales repetidas) encaja en la definición de la (ii) pero nadie lo ha escrito»*. Este acto lo escribe. La columna `clase_ADR57c` de §3 es nueva y **va al final de la tabla a propósito**: `T24` extrae `estado` por posición (campo 6 tras dividir por `|`, §4), y una columna insertada antes de `estado` habría roto la receta congelada y el vigía a la vez.

**Universo de la adjudicación, declarado (`A.13`):** las **3** filas de §3, todas — no una muestra. Las tres clases contra las que se adjudican son las de `canon/gobernanza-v1_15.md` `ADR-57(c)`, citadas ya verbatim en §0 de este mismo archivo y no re-interpretadas aquí.

| llave | clase | por qué, y por qué no las otras dos |
|---|---|---|
| `CAL-G3` | **(i)** | Panel ENNViH/MxFLS, tres olas, mismos sujetos. Ya estaba rotulada así dentro de la columna `diseño`; este acto solo la saca a columna propia. No re-adjudicada |
| `R5.1-D2` | **(ii)** | Los tres elementos de la definición sellada están **escritos** en `r5-1-diseno-por-regla-preregistro` §2, no inferidos por parecido: corte natural (el cambio de regla de elegibilidad de 2019, que elimina la prueba de ingreso por pensión contributiva de $1,092/mes), grupo de comparación explícito (*«elegible en ambos regímenes»*) y encuestas repetidas (ENIGH 2018→2022). No es **(i)**: 2018 y 2022 no son los mismos sujetos, y el propio pre-registro lo dice al llamarse "transversales repetidas". No es **(iii)**: no hay aleatorización de terceros |
| `R5.1-D3` | **(ii)** | Misma regla, mismo corte, mismo grupo de comparación, mismas dos olas transversales, con el criterio `D-1` encima (`bbis-r5-1-d3` §6) |

### 8.1 · La consecuencia que `FP-64` no sacó, y que cambia lo que vuelve a mesa

`FP-64` abre diciendo que **la llave (ii) *«sigue sin renglón operativo en ningún archivo del programa»***. Adjudicadas las tres filas, esa frase **queda refutada por el propio registro**: la (ii) no sólo tiene renglón, tiene **dos**, y son **las dos únicas llaves ejercidas del programa**.

| clase de `ADR-57(c)` | filas | `EJERCIDA_*` |
|---|---|---|
| (i) panel | 1 (`CAL-G3`) | **0** |
| (ii) experimento natural sobre encuestas repetidas | 2 (`R5.1-D2`, `R5.1-D3`) | **2** |
| (iii) experimento de terceros | 0 | 0 |

**Leído así, el `2 de 3` del contador es enteramente (ii).** Lo que faltaba no era una llave (ii): era que alguien mirara las que ya estaban y les pusiera la etiqueta. El contador **no se mueve** — adjudicar la clase de una fila existente no toca su `estado`, y `T24` deriva numerador y denominador **sólo** de `estado`. Verificado por la receta de §4 después de escribir la columna: `2` de `3`, igual que antes.

### 8.2 · Y la tensión con `ADR-57(c)`, nombrada porque este acto tuvo que resolverla para poder ejecutar

La Razón 1 de `FP-64` —ENOE es portador de desenlaces **sin exposición θ**— se ofrece como fundamento para *«retirar ENOE como candidato de la llave (ii)»* (opción (a)). Pero `ADR-57(c)`, sellado, dice de ENOE exactamente lo contrario, verbatim (`gobernanza-v1_15.md`, mismo inciso que define las tres clases):

> "ENOE — su panel rotativo queda refutado como ruta de conducta financiera (`CAL-ENOE` Fase A, 31/jul: **el instrumento no trae reactivo de ahorro/crédito/deuda/planeación**); **permanece elegible únicamente como portador de desenlaces laborales para experimentos naturales** (p. ej. salario mínimo de franja fronteriza)."

Las dos mitades de esa frase son la Razón 1 y su consecuencia, y `ADR-57(c)` las separó a propósito: la ausencia de reactivo de θ refuta la ruta **(i)** —el panel— y **no** toca la **(ii)**, porque en un experimento natural la exposición la pone la **política**, no el cuestionario. `FP-64` aplica un hallazgo verdadero a la clase para la que `ADR-57(c)` ya había dictaminado que **no** es descalificante, y el ejemplo que `ADR-57(c)` nombra —*«salario mínimo de franja fronteriza»*— es el mismo decreto del 1/ene/2019 que este acto acaba de habilitar con la adquisición.

**Consecuencia operativa, y es la que vuelve a mesa:** el `NO-ENCONTRADO` que T2 de este acto midió (`bbis-adq-enoe-pre2019` §6, Desenlace 2) **no descarta a ENOE de la llave (ii)** bajo el texto sellado — descarta a ENOE como fuente de **exposición θ**, que es otra cosa y ya estaba dicho. Este registro **no decide** cuál de las dos lecturas gobierna: `ADR-57(c)` es firma de mesa y sólo mesa lo enmienda. Lo que este acto hace es dejar de poder ignorarlo.
