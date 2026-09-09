# S17 · Pre-registro de la MODULACIÓN POR OLA de `R5.1` — `familia.seguro.volatilidad_ausencia_estado` sobre la serie ENIGH de seis olas

### `prereg-caja-S17` · **v1.0** · 8 de septiembre de 2026

> | | |
> |---|---|
> | **ARCHIVO** | `forense/prereg-caja/S17-MODULACION-OLA-R5-1-spec-v1_0.md` |
> | **NOMBRE ESTABLE** | **`prereg-caja-S17`** — cítalo así, nunca por nombre de archivo |
> | **QUÉ ES** | Spec propia de la **modulación por ola** para la primera de las dos reglas que el marco vigente trae con `serie_olas`: `familia.seguro.volatilidad_ausencia_estado` (`R5.1`), seis olas bienales de ENIGH Nueva Serie 2012→2022, tres celdas del marco (`FAM-M-05`, `FAM-M-06`, `FAM-M-07`). Cumple `T9` — *«Es modelo nuevo y va a `C0-B` con spec propia antes de que ninguna cifra suya entre a un veredicto»* — y cierra la mitad de `NC-0025` que le toca. |
> | **QUÉ NO ES** | **No corre ningún CALC y no produce ninguna cifra nueva.** No re-mide la serie (`CALC-B-0001`, del mismo acto, la re-mide bajo GEN2 por su cuenta y con su propia spec). No promedia olas, no ajusta tendencia, no interpola. No mueve `R5.1`. No reescribe las corridas ya selladas (`CALC-M-…-ola-v2` / `CALC-AGG-…-ola-v2` son `CALC-INMUTABLE`). No decide si la modulación entra al agregado: eso es firma de mesa. |
> | **VERIFICAS ASÍ** | La serie que esta spec gobierna está publicada verbatim en `milpa/tramite.yaml:850-856` con `p`, `ic95`, `n`, `estratos`, `upm`, `ponderador`, `sha256_payload` y `payload_manifiesto_id` por ola. El inventario de §3 se re-deriva de ahí, no de esta prosa. |

**Acto:** `ACTO GEN2-C0-B · LA BASE`, 8/sep/2026, entorno **CAJA (UBUNTU)**, sobre `origin/main = 017ac24`.

---

## 1 · Qué es «modular por ola», dicho en una frase

El marcador `M` emite, para cada celda del marco, un punto que se compara contra el `R` arbitrado de esa celda. Sin modulación, `M` emite **la misma `p` base** para todas las celdas de una regla, sin importar de qué ola es el árbitro. **Modular por ola es sustituir esa constante por el punto de la serie que corresponde a la ola del árbitro** — y hacerlo sin mirar la ola del árbitro misma.

`R5.1` es el caso más limpio del marco: su `p` base (`0.045694`) **es** el punto de la ola 2022 de su propia serie, y sus tres celdas arbitran olas 2016, 2018 y 2020. Sin modulación, `M` contesta 2022 tres veces contra árbitros de 2016, 2018 y 2020.

## 2 · Sobre qué serie — y la llave de igualdad que la hace una serie

`milpa/tramite.yaml:familia.seguro.volatilidad_ausencia_estado.serie_olas`, seis entradas bienales:

| ola | `p` | `ic95` | `n` | estratos | upm | ponderador | método |
|---|---|---|---|---|---|---|---|
| 2012 | 0.044704 | [0.039340, 0.050420] | 9 002 | 108 | 1 111 | `factor_hog` | medición GEN1 |
| 2014 | 0.040784 | [0.036551, 0.044978] | 19 479 | 200 | 2 626 | `factor_hog` | medición GEN1 |
| 2016 | 0.047459 | [0.045192, 0.049807] | 70 311 | 536 | 7 891 | `factor` | medición GEN1 |
| 2018 | 0.047285 | [0.045093, 0.049555] | 74 647 | 543 | 8 377 | `factor` | medición GEN1 |
| 2020 | 0.043775 | [0.041877, 0.045680] | 89 006 | 558 | 10 118 | `factor` | medición GEN1 |
| 2022 | 0.045694 | [0.043754, 0.047711] | 90 102 | 560 | 10 211 | `factor` | medición GEN1 |

**Las seis entradas comparten instrumento, universo, desenlace y escala** — ENIGH Nueva Serie, universo completo de `concentradohogar`, `recibe_remesas = 1 si remesas > 0`, proporción en [0,1] — y por eso son *una serie* y no seis números parecidos. La igualdad se declara aquí campo por campo; **no se infiere por semejanza de nombre**.

**Una diferencia de diseño que se declara y NO se colapsa:** las olas 2012 y 2014 usan el ponderador `factor_hog`; las cuatro posteriores usan `factor`. Es el mismo concepto (ponderador de hogar) con nombre distinto entre versiones del microdato, y así lo declara el propio `serie_olas`. Queda como **reserva declarada**: cualquier modulación que use 2012 o 2014 como previa arrastra ese cambio de nombre, y esta spec lo dice en vez de esconderlo.

## 3 · Qué estimando — la regla de selección de ola, y de dónde viene

La regla vigente es la **ADENDA de mesa del 8/sep/2026 a `P3(c)` del `ACTO GEN2-T9`**, asentada en `NC-0025`, y **no** la primera versión de `T9 §6.b`:

- **Vigente:** *«última ola estrictamente anterior a la del árbitro; sin anterior → `SIN-PREVIA` y la celda no modula».*
- **Derogada:** *«la ola más cercana distinta de la del árbitro (leave-one-out; empate → la anterior)»* — elegía una ola **posterior** cuando la serie no traía anterior, que es **fuga temporal**: el modelo contestaría con información que no existía cuando el árbitro se levantó.

**Estimando de la modulación, por celda:** `M_modulado(celda) = p(ola_previa(celda))`, donde `ola_previa` es la última ola de la serie estrictamente anterior a la ola del árbitro de esa celda. Sin previa: la celda emite `modela_ola: SIN-PREVIA` y `M` cae a la `p` base, **declarándolo**, nunca en silencio.

Aplicado a las tres celdas de `R5.1`, derivado de §2 y del marco `v1.3` (esto es derivación mecánica, no medición nueva):

| celda | árbitro | ola previa | `M_modulado` | `M` sin modular |
|---|---|---|---|---|
| `FAM-M-05` | ENIGH 2016 | **2014** | 0.040784 | 0.045694 |
| `FAM-M-06` | ENIGH 2018 | **2016** | 0.047459 | 0.045694 |
| `FAM-M-07` | ENIGH 2020 | **2018** | 0.047285 | 0.045694 |

**Ninguna de las tres cae en `SIN-PREVIA`** — la serie empieza en 2012 y el árbitro más antiguo es 2016. `N-SIN-PREVIA = 0` para esta regla, y el guard se declara aunque no muerda.

**Ninguna de las seis entradas es `ORIGEN-ARBITRO`**: las seis son mediciones GEN1 propias, ninguna es `R-json` reutilizado. Por lo tanto ninguna celda de `R5.1` queda `VERIFICACION-NO-PUNTUA` por esa vía (contrastar con `prereg-caja-S18`, donde tres de ocho sí lo son).

## 4 · La convergencia que este acto encontró, y que hay que decir en voz alta

**La regla de selección de ola de la modulación y el selector `B` son la misma operación.** «Última ola estrictamente anterior; sin anterior, abstente» es, palabra por palabra, lo que `tools/baseline_temporal.py::seleccionar_baseline` hace (`periodo_fin >= objetivo.periodo_inicio → OLA_NO_ANTERIOR`; sin candidatas → `SIN_BASELINE`). Y la serie sobre la que las dos operan, para `R5.1`, **es la misma serie**.

De ahí, dos consecuencias que `C0-D` tiene que heredar explícitas:

1. **La modulación de `R5.1` ES el brazo `PERSISTENCIA` de `CALC-B-0001`.** Lo que `CALC-B-0001` mide como «error de la línea base» para los objetivos 2018 y 2020 es, exactamente, el error que `M` comete al modular `FAM-M-06` y `FAM-M-07`. Un solo ensayo mide las dos cosas.
2. **La modulación NO exige disponibilidad al corte; el selector `B` sí.** El brazo `OPERATIVO` de `CALC-B-0001` aplica además `disponible_desde <= fecha_corte` y por eso puede abstenerse donde la modulación emite. **Es una diferencia real de contrato entre las dos piezas, no un detalle de implementación**, y esta spec la deja escrita para que `C0-D` no la descubra a mitad de una comparación: si `C0-D` quiere que `M` y `B` compitan bajo *el mismo corte informativo* (que es lo que la firma `D-2`/`FP-348` pide), la modulación tendrá que ganar la cláusula de disponibilidad que hoy no tiene, o `B` tendrá que perderla — y esa es **decisión de mesa**, no de un ejecutor.

## 5 · Constructibilidad (A.15) — CONSTRUIBLE, con dos reservas declaradas

**Veredicto: `CONSTRUIBLE`.** La serie tiene seis olas con `p`, `ic95`, `n` y diseño declarados; las tres celdas tienen previa; el inventario está citado en §2 con `payload_manifiesto_id` y `sha256_payload` por ola, y los seis payloads están en corpus (`enigh2012_nc_csv` … `enigh2022_nc_csv`, verificado contra `data/manifiesto.yaml` en este mismo acto).

Reservas, declaradas y no resueltas aquí:

1. **Cambio de nombre del ponderador entre 2014 y 2016** (`factor_hog` → `factor`), §2. Afecta a `FAM-M-05`, cuya previa es 2014.
2. **La serie es GEN1.** Los seis puntos vienen del aparato GEN1 (`ACTO MAESTRA33-E18-P3-L1` y sucesores). Bajo la regla `E.1`, una modulación que los consuma **no cuenta como medición GEN2** por sí sola, exactamente igual que los corredores envueltos. `CALC-B-0001` produce por primera vez cuatro de esos seis puntos bajo GEN2; los otros dos (2012, 2014) quedan sin contraparte GEN2 y por lo tanto **`FAM-M-05` es la única celda cuya previa no tiene medición GEN2 disponible** al cierre de este acto.

## 6 · Lo que esta spec explícitamente NO autoriza

1. **No mueve `R5.1`** ni ninguna otra regla; ninguna cifra de la modulación entra a un veredicto (`T9`).
2. **No promedia ni ajusta tendencia.** Un promedio de olas, una mediana por regla o una interpolación entre olas están prohibidos por `T9` y esta spec no abre ninguna puerta lateral.
3. **No reescribe corridas selladas.** `CALC-M-marco-M-sorteado-v1_3-ola-v2` y `CALC-AGG-marco-M-sorteado-v1_3-ola-v2` son inmutables; cualquier corrección entra por sucesión declarada (`repite_de:`), nunca hacia atrás.
4. **No decide si la modulación entra al agregado.** El agregado conserva su métrica sellada; adoptar la modulación es firma de mesa.

## 7 · Sello

Congelada en el `COMMIT-1` del `ACTO GEN2-C0-B`. Esta spec **no produce cifras**: define qué sería la modulación de `R5.1`, sobre qué serie, con qué regla de ola y con qué reservas, **antes** de que ninguna cifra suya entre a un veredicto. Si un acto sucesor corre un CALC de modulación sobre `R5.1`, **el primer resultado que produzca ese procedimiento es el que se reporta.**
