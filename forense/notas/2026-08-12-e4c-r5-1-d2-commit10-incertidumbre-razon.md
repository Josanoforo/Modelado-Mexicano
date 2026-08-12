# E4c Paso 3 · Commit 10 — incertidumbre de la razón monto/gasto, y el estimador declarado

**No edita los commits 0, 7, 8 ni 9.** Commit 9 cerró el conjunto "monto suficiente" con un punto (29.0%) contra un criterio sellado (60–63%) y un piso informal (33%, borde inferior del rango 33%-47% que el 4/ago llamó "no trivial" pre-reforma). Un punto sin intervalo no despeja una compuerta — mesa no debe firmar A↔B sobre eso. Este commit nombra con precisión los dos estimadores que Commit 9 reportó y calcula el IC95% del que sí es un estimador de diseño.

## 1 · Universo — reproducido exacto, verificado antes de calcular nada más

| | Commit 9 | Este commit |
|---|---|---|
| Tratamiento 2022 (deflactado) | 8,877 | 8,877 ✅ |
| Con `P104>0` | 6,497 (73.2%) | 6,497 (73.2%) ✅ |

`N_hat` del dominio (personas ponderadas por `factor_ch`): 2,794,831.

## 2 · Los dos estimadores de Commit 9, nombrados con precisión

**RM — razón de medias ponderadas.** `R̂ = Σ(w·monto) / Σ(w·gasto_pc)`, sobre las 6,497 filas del dominio. Reproduce **29.05%** (Commit 9 redondeó a 29.0%). Responde: *para la población de receptores de `R5.1-D2` (ponderada al universo nacional vía `factor_ch`), ¿qué fracción del gasto per cápita promedio representa la pensión?* Es un estimador de diseño: replica exactamente `monto_pension_tri_prom` del script sellado (media ponderada por `factor`), como Commit 9 §4 declaró.

**La "mediana, secundaria" — NO es razón de medianas ponderadas, ni mediana de razones por persona. Es razón de medianas SIN PONDERAR sobre las filas de muestra.** Se probaron las alternativas y solo una reproduce el número exacto de Commit 9:

| candidato | mediana(monto) | mediana(gasto_pc) | razón |
|---|---|---|---|
| **mediana SIN ponderar de m y g, por separado** | **$5,576.08** | **$11,483.86** | **48.56%** ✅ reproduce Commit 9 |
| mediana ponderada (interpolada) de m y g, por separado | $5,606.55 | $12,226.06 | 45.86% |
| mediana ponderada de la razón por-persona (`monto_i/gasto_pc_i`) | — | — | 40.31% |
| mediana SIN ponderar de la razón por-persona | — | — | 43.06% |

El primer renglón reproduce `$5,576.08` y `$11,483.86` con exactitud de centavo. **El 48.6% de Commit 9 es `statistics.median` crudo sobre las 6,497 filas de la muestra, sin `factor_ch`.** Responde una pregunta distinta de RM: *¿cuál es la razón entre el monto típico y el gasto típico dentro de la muestra levantada?* — una estadística descriptiva de la muestra, no necesariamente consistente para el parámetro poblacional bajo un diseño complejo (estratificado, por conglomerados, con probabilidades de selección desiguales que el factor de expansión corrige y que un cálculo sin ponderar ignora). Commit 9 §6 la llamó "secundaria" y no la promovió a cifra principal — correcto — pero no dijo que no estaba ponderada. Queda dicho aquí: **no compite con RM en el mismo plano epistémico**, no por ser mediana en vez de media, sino por no ser un estimador de diseño.

Hallazgo menor, declarado no oculto: 2 de los 6,497 hogares receptores reportan `gasto_mon=0` (`folioviv` `0801279704` y `1906192405` — casos reales del microdato, no defecto de construcción). No mueven las medianas de m/g por separado (caen en la cola), pero sí exigen exclusión explícita al construir la razón por-persona (división por cero); se excluyeron para las dos filas de razón-por-persona de la tabla.

## 3 · IC95% de RM — linealización de cociente + ultimate cluster, no la fórmula de proporción

`prop_ultimate_cluster`/`diff_ultimate_cluster` en `tests/svystat.py` linealizan una proporción y una diferencia — ninguna sirve para un cociente de dos totales. Se implementó, en script de scratch (no toca `tests/`), la linealización estándar de razón (Wolter, *ratio estimator*):

```
z_i = w_i · (monto_i − R̂ · gasto_pc_i) / Σ(w · gasto_pc)
```

agregada por `(est_dis, upm_ch)` y reducida con el mismo patrón de ultimate cluster ya en `tests/svystat.py` (`Σ_h (m_h/(m_h-1))·Σ_i(z_hi − z̄_h)²`, cuantil `1.959963985`, singleton excluido de la suma y contado aparte). Dos variantes, porque RM es una razón de **dominio** (P104>0 es una subpoblación aleatoria, no un estrato de diseño) y la teoría de estimación de dominio exige tratamiento explícito:

| variante | filas | `n_estratos` | `n_upm_total` | `n_estratos_singleton` | `se` | IC95% |
|---|---|---|---|---|---|---|
| **A — solo dominio** (las 6,497 filas de receptores) | 6,497 | 497 | 3,891 | 93 | 1.47pp | (26.16%, 31.94%) |
| **B — extensión-cero sobre universo T completo** (8,877, no-receptores con `monto=0`) | 8,877 | 520 | 4,885 | 75 | 1.58pp | (25.95%, 32.14%) |

`R̂ = 29.0471%` es **idéntico** en ambas variantes — confirma que la extensión-cero no mueve el punto (los no-receptores aportan cero a numerador y denominador por construcción), solo la varianza. Variante B es la teóricamente correcta para una razón de dominio: conserva la estructura completa de estratos/UPM del universo `T`, incluyendo estratos sin receptores, que la variante A descarta silenciosamente al quedarse solo con las filas del dominio — descartarlas reduce artificialmente el número de UPM por estrato y puede subestimar el `se`. Aquí la diferencia es pequeña (1.58pp vs 1.47pp) y **no cambia la conclusión del §4** — se reportan ambas por transparencia, no porque la elección esté indecisa.

No se tocó `tests/svystat.py`: la función vive solo en el script de scratch de este commit.

## 4 · Comparación contra el piso de 33% — veredicto de la compuerta

**El IC95% de RM queda entero por debajo de 33% en las dos variantes** (cota superior 31.94% en A, 32.14% en B — ambas < 33.00%). **DESPEJA POR ABAJO.**

Reserva escrita, no forzada: el piso de 33% mide una población distinta (universo amplio de recepción declarada del 4/ago, sin condición de ingreso — Commit 9 §6 ya lo declaró) — la comparación hereda esa asimetría poblacional, no la resuelve este commit. Y la mediana sin ponderar (48.6%) **no se evalúa contra el piso**: no es un estimador de diseño, no tiene un IC95% construible con las herramientas de este acto sin un tratamiento distinto (bootstrap replicado o linealización de cuantiles, ninguno implementado aquí), y tratarla como alternativa competidora sería exactamente el error que este commit viene a cerrar — se declara la limitación, no se calcula un intervalo de adorno para algo que no lo sostiene.

**Consecuencia:** el "no se sostiene" de Commit 9 §7 queda reforzado con intervalo, no solo con punto — la compuerta de "monto insuficiente" cierra con margen estadístico bajo las dos variantes de varianza ensayadas, no por apenas cruzar el piso. No cambia la fila propuesta (B, `EJERCIDA_INDECISA`) ni la precedencia citada en Commit 9 §7.

## 5 · Lo que este commit deliberadamente no hace

No corre el placebo 2014→2018 (reserva de Commit 8 §5, sigue abierta). No estratifica por los ejes de Commit 1 §2.7. No calcula un IC95% para el estimador de mediana sin ponderar (§4). No toca `tests/svystat.py` — la razón y su linealización viven en script de scratch, no commiteado.

---

*Commit 10 de este acto (Bloque A-bis/D). No edita Commits 0, 7, 8 ni 9. Nombra con precisión los dos estimadores de Commit 9 (RM = razón de medias ponderadas, 29.0%; la "mediana secundaria" = razón de medianas sin ponderar, 48.6%, no comparable en el mismo plano) y calcula el IC95% de RM vía linealización de cociente + ultimate cluster: despeja por abajo del piso de 33% en dos variantes de varianza. Mesa adjudica en acto propio; este commit no firma.*
