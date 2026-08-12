# E4c Paso 3 · Commit 9 — cerrar el conjunto "monto suficiente" con la medida sellada

**No edita los commits 0, 7 ni 8.** Cierra, con la medida correcta, la segunda de las tres condiciones conjuntivas de la fila A (DiD<10pp-o-signo-contrario, **monto suficiente**, identificación exitosa). El resultado cambia el veredicto propuesto — se declara aquí, no se reescribe Commit 8.

## 1 · La premisa falsa, declarada en una línea

Commit 8 §4 dijo *"no se abrió tabla de gastos, fuera de lo que este acto tenía preparado"*. Falso: `concentradohogar.gasto_mon` vive en la misma tabla que el acto ya abría para `est_dis`/`upm`/`factor`. No fue una limitación del dato — fue una limitación de lo que el acto tenía preparado. Se escribe así para que no se repita.

## 2 · El factor de conversión — verificado, no supuesto, y un hallazgo de etiqueta en el documento sellado

**La tabla del 4/ago (`2026-08-04-hitoD-r5-1-pension-bienestar.md:157`) está mal etiquetada — dice "mensual" en las dos columnas y ambas son trimestrales.** Verificado por dos vías independientes, no una:

1. `tests/r5_1_pension_bienestar.py:272-273,392`: la variable se llama `monto_pension_tri_prom`, calculada como `sum(monto*factor)/sum(factor)` sobre `monto_pension_tri` (línea 190: `hh["monto_pension_tri"] += ing_tri`, directo de `ingresos.ing_tri`), y el propio `print` de la línea 392 dice literalmente `"monto pension **trimestral** promedio"`.
2. El diccionario de `concentradohogar` (2022): `gasto_mon = alimentos + vesti_calz + ... + transf_gas`, y cada sub-categoría (`cereales`, `carnes`, etc.) se construye explícitamente como `Σ de gastoshogar.gasto_tri` — `gasto_mon` es trimestral por construcción, no mensual.

**Esto no invalida el 60.3% sellado.** Es una razón (monto/gasto), y ambos términos son trimestrales por igual — el factor de conversión se cancela en el cociente. El error es de la etiqueta de columna del documento sellado (`:157`), no de la cifra `60-63%` que reporta (`:168`). Se declara la corrección de etiqueta, no se edita el documento sellado (fuera de perímetro de este commit).

**Para este commit:** se calcula la misma razón, trimestral/trimestral (equivalente a mensual/mensual — el `/3` se cancela), sobre pesos corrientes de 2022, sin deflactar, tal como exige `:166`.

## 3 · Universo — reproducido exacto del Commit 8, verificado antes de calcular nada más

| | Commit 8 §4 | Este commit |
|---|---|---|
| Tratamiento 2022 (deflactado) | 8,877 | 8,877 ✅ |
| Con `P104>0` (recepción efectiva) | 6,497 (73.2%) | 6,497 (73.2%) ✅ |

Universo reproducido exacto — no se redefinió nada.

## 4 · La medida — monto / `gasto_mon` per cápita, ponderada, dentro de la ola 2022

| | Trimestral (ponderado, factor de `concentradohogar`) | Mensual (÷3, mismo cociente) |
|---|---|---|
| `P104` medio (beneficiarios) | $5,100.83 | $1,700.28 |
| `gasto_mon` per cápita medio (mismos hogares) | $17,560.54 | $5,853.51 |
| **Razón monto/gasto (media ponderada)** | **29.0%** | **29.0%** |
| Razón monto/gasto (mediana, secundaria) | 48.6% | 48.6% |

**La media ponderada (29.0%) es la cifra metodológicamente comparable al 60.3% sellado** — el script sellado calcula `monto_pension_tri_prom` como media ponderada por `factor`, no mediana; se replica el mismo estimador, no uno distinto que casualmente diera un número más cómodo. La mediana se reporta aparte, no se promueve a cifra principal solo porque cae más cerca del rango de referencia — ver §6.

## 5 · La comparación — en la escala sellada, y solo ahí

| medida | valor | escala | fuente |
|---|---|---|---|
| Criterio sellado, 2020 y 2022 | 60%–63% | monto / `gasto_mon` per cápita | `2026-08-04-…:168` |
| Medido aquí, 2022 (media ponderada) | **29.0%** | monto / `gasto_mon` per cápita | este commit |
| Commit 8 §4 (proxy retirado) | 20.0% / 29.1% | monto / **ingreso** per cápita | `commit8:§4` |

**La tercera fila se muestra para dejar registro de qué se sustituyó, no para compararla contra las otras dos.** Un cociente sobre gasto y uno sobre ingreso son cantidades distintas — compararlos sería el error de categoría que A-bis regla 3 prohíbe, exactamente el que este commit viene a cerrar. Coincidencia declarada, no usada para nada: el 29.0% medido aquí (gasto) y el 29.1% mediana del proxy retirado (ingreso) son números parecidos por casualidad de la población, no porque gasto e ingreso se comporten igual — no se usa esta coincidencia como validación cruzada de nada.

## 6 · Por qué 29.0% y no algo más cercano a 60-63% — declarado, no forzado

La población de este commit **no es la misma** que la del 4/ago. La ficha sellada mide "beneficiarios" por **recepción declarada de `P104`, sin condición de ingreso** — población amplia, con sesgo hacia hogares de menor ingreso (el propio programa original, "65 y más", se diseñó para adultos mayores sin cobertura contributiva). El tratamiento de `R5.1-D2` es **personas con pensión contributiva >$1,092/mes que además reciben `P104`** — por construcción, una subpoblación con más ingreso propio, y por tanto con `gasto_mon` per cápita más alto — el mismo monto de `P104` cubre una fracción menor de un gasto más grande. No es un error de cómputo: es que la fila A de `R5.1-D2` exige "monto suficiente" para **esta** población, no para la población general de beneficiarios.

**Media vs. mediana, declarado como tensión real, no resuelta a favor de la lectura más cómoda:** la mediana (48.6%) cae dentro del rango que el 4/ago llamó "no trivial" pre-reforma (33%-47%, de hecho lo cruza por arriba); la media ponderada (29.0%) cae por debajo de ese mismo rango. La brecha entre las dos sugiere una distribución de `gasto_mon` per cápita con cola pesada dentro de este universo (hogares pequeños con gasto per cápita muy alto empujan la media hacia abajo del cociente, ya que están en el denominador). Se usa la media ponderada por ser la que replica la metodología sellada — no porque sea la que da el resultado más limpio; si hubiera sido al revés (mediana metodológicamente correcta y media más favorable), este commit reportaría la mediana igual.

## 7 · Veredicto sobre el conjunto — NO SE SOSTIENE

**29.0% queda por debajo del criterio sellado (60-63%) y por debajo del piso que el 4/ago llamó "no trivial" en el periodo pre-reforma (33%-47%).** "Monto documentado como suficiente" **no se sostiene** para la población de `R5.1-D2` con la medida correcta.

**Consecuencia, por la precedencia sellada (A → E → B → C → D, ADR-71(b)): la fila A no se satisface — "monto insuficiente" de B gana sobre A, sin excepción por magnitud del DiD, exactamente como ya ganaba sobre A y sobre E según el propio apéndice.** El resultado no cae en A pese a que el DiD de ambos desenlaces cumplía <10pp-o-signo-contrario — esa condición sola no basta, la fila A es una conjunción de tres, y la segunda falla.

**Se retira la propuesta de fila A del Commit 8, sin editarlo — se propone B en su lugar.** `EJERCIDA_REFUTA` (Commit 8) queda como lo que se propuso con un proxy de ingreso que resultó ser la comparación equivocada; con la medida correcta, el veredicto propuesto pasa a **`EJERCIDA_INDECISA`** (fila B — "ambiguo, no refuta ni confirma", por monto insuficiente, no por la magnitud del DiD, que sigue siendo <10pp/signo-contrario en ambos desenlaces).

**Lo que NO cambia:** los DiD y DDD de Commit 8 (transferencia +2.32pp, corresidencia −0.81pp, con sus IC) siguen siendo las cifras correctas — nada en este commit las recalcula ni las cuestiona. Solo cambia cuál fila de §6 gobierna, porque la condición de monto es una compuerta independiente de la magnitud del efecto.

## 8 · Lo que este commit deliberadamente no hace

No corre el placebo 2014→2018 (reserva de Commit 8 §5, sigue abierta). No estratifica por los ejes de Commit 1 §2.7. No toca `tests/` — la lectura de `gasto_mon` se hizo con un script de scratch (no commiteado), reutilizando exactamente el universo ya construido en Commit 8/9 sin modificar ningún archivo de `tests/`.

---

*Commit 9 de este acto (Bloque A-bis/D). No edita Commits 0, 7 ni 8. Cierra el conjunto "monto suficiente" de la fila A con la medida sellada (`gasto_mon`, no ingreso) — resultado: no se sostiene. Veredicto propuesto revisado: fila B, `EJERCIDA_INDECISA`, no fila A. Mesa adjudica en acto propio; este commit no firma.*
