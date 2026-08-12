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

Este registro es una **población de conteo distinta** de la de Hito D. Ninguna fila de aquí mueve `13 de 27` (Hito D, `estado-programa-v1_10.md:95`), `15 coeficientes, cero medidos` (misma línea — el "0 de 15" que cita el encargo que abrió este acto es una paráfrasis; el texto vigente en el archivo dice literalmente "15 coeficientes, cero medidos", corregido aquí sin editar la fuente), `8 de 14` ni `4 de 144` (`estado-programa-v1_10.md:97`).

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

| llave_id | coeficiente_o_regla | diseño | preregistro_ref | estado | veredicto | escala_del_veredicto | fecha | ADR |
|---|---|---|---|---|---|---|---|---|
| `CAL-G3` | `G3 → horizonte_temporal` (−0.60), fila 5 de `censo-estimabilidad-coeficientes-v1_0.md` §5, única fila `RUTA-I` de las 15 | panel (ENNViH/MxFLS, tres olas — llave (i) de ADR-57(c)) | `forense/hitoD-preregistro-v2_0.md` Nota 7 (líneas 478-524, sellada 29/jul/2026), Adenda 1 (525-553), Nota 8 (554-648), Nota 10 (649+, Fase C corrida) | `SELLADA_NO_EJERCIDA` | — | `CAL-A`/`CAL-B`/`CAL-C`/`CAL-D`/`CAL-X` (Nota 7 §9a) — declarada, **no invocada**: Nota 10 corre Fase C completa sobre olas 2-3 pero es descriptiva y, verbatim, *"sigue sin emitir `CAL-A`/`B`/`C`/`X` y no entra al bloque de abajo"* (`hitoD-preregistro-v2_0.md:634`). El censo (§5, fila 5, columna Prioridad) declara además que falta el **diseño intra-persona** para promover de descriptivo a identificado — no concedido todavía, no es un instrumento nuevo lo que falta | 29/jul/2026 | — (ficha de `hitoD-preregistro`, sin ADR propio; nombrada por `ADR-57(c)`) |
| `R5.1-D2` | la regla `R5.1` del Hito D — la pregunta sustantiva de si la elegibilidad al programa sustituye transferencia intrafamiliar hacia mayores, no la operacionalización por recepción declarada de ADR-58 | cuasi-experimental, diferencias-en-diferencias por grupo de elegibilidad (ENIGH 2018 → 2022) | `forense/r5-1-diseno-por-regla-preregistro-v1_0.md` (sellado 4/ago/2026, §9 sin enmiendas a la fecha) | `SELLADA_NO_EJERCIDA` | — | **INCOMPLETA — no nombra el desenlace de no-refutación.** §6 del propio pre-registro, citado verbatim: fila `A` = "DiD <10pp... **La regla se refuta a este nivel de identificación también**"; fila `B` = "DiD entre 10 y 20pp... **Ambiguo — no refuta ni confirma**"; fila `C` = archivo por panel de persona no sostenido en disco; fila `D` = archivo por diseño (hueco de identificación de la clave de pensión contributiva, o muestra insuficiente). Ninguna de las cuatro filas nombra el caso "DiD ≥20pp con identificación exitosa y monto suficiente" — evidencia limpia de que la brecha **no** converge — como corroboración: ese desenlace cae fuera de A (exige <10pp), fuera de B (exige 10-20pp explícito), fuera de C (exige que la reserva dominante sea específicamente ausencia de panel) y fuera de D (exige fallo de diseño). Es el defecto de B-bis: se ve antes de correr, no después. E4c arranca con la instrucción de **reportar** este vacío, nunca de forzar una fila que la escala sellada no contempla. | 4/ago/2026 | 67(c) |

**Contador vigente: `0` llaves ejercidas de `2` filas.**

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
