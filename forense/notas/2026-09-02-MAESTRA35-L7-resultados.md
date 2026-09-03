# COMMIT-2 · Resultados · ACTO MAESTRA35-L7 · REGLAS-ACTIVOS-L2

Ejecuta la spec de `forense/notas/2026-09-02-MAESTRA35-L7-spec.md`, sin
editarla. Salida cruda en `data/l7-resultados-v1_0.json` (emitido por
`tools/emite_resultados_l7.py`, que solo importa y llama a los cuatro
medidores ya congelados) y `data/l7-log-pieza-{a,b,c,d}.txt` (stdout literal
de cada corrida).

## (a) — `civico.denuncia.con_seguro` (ENVIPE 2025, `BPCOD=01`)

| celda | n | p̂ | IC95% |
|---|---|---|---|
| no asegurado | 614 | 67.20% | [64.25%, 70.16%] |
| asegurado | 402 | 79.09% | [75.23%, 82.78%] |

**VEREDICTO: CORROBORADA.** Reproduce, tercera vez independiente, 79.1%/
67.2%/11.9pp ya publicados por `hitoD-R7_2-veredicto`/`revision`
(4/ago/2026) — control de regresión pasa.

## (b) — `familia.union.libre` (EDER 2017 + ENADID 2023)

**D1 EDER — cohorte de nacimiento** (tipo de primera unión = libre):

| cohorte | n | p̂(unión libre) | IC95% |
|---|---|---|---|
| 1961-1970 | 4 001 | 30.47% | [28.54%, 32.41%] |
| 1971-1980 | 6 274 | 39.02% | [37.27%, 40.74%] |
| 1981-1990 | 5 903 | 57.24% | [55.55%, 58.94%] |
| 1991+ | 2 509 | 77.29% | [75.20%, 79.33%] |

**VEREDICTO: CORROBORADA** (monótono, signo esperado `asc`, ningún par
consecutivo se traslapa).

**D2 ENADID — tramo de edad** (unión libre | pareja actual):

| edad | n | p̂(unión libre) | IC95% |
|---|---|---|---|
| 18-29 | 22 676 | 69.92% | [68.95%, 70.89%] |
| 30-44 | 50 944 | 41.66% | [40.91%, 42.42%] |
| 45-59 | 47 308 | 23.86% | [23.20%, 24.51%] |
| 60+ | 31 171 | 12.67% | [12.04%, 13.31%] |

**VEREDICTO: CORROBORADA** (mismo patrón, monótono, dos instrumentos
independientes triangulando la misma dirección). Prevalencia bruta ENADID
(15+ sin condicionar): 19.05%.

## (c) — `familia.cuidado.reparto_mujeres40` (ENUT 2024)

**D2 — proporción del total de horas de cuidado del hogar hecha por mujeres
40+:** r̂ = **22.15%**, IC95% = [21.31%, 23.00%], n=29 181 hogares (idéntico
sobre el subconjunto con carga>0, n=17 394 — algebráicamente esperado, los
hogares sin carga aportan 0/0). **Contexto declarado, no adjudicado:** el
share poblacional de mujeres 40+ en el universo 12+ es 26.57% — su aporte a
las horas totales (22.15%, IC95 sin traslape con 26.57%) es **menor** que su
peso poblacional, no mayor.

**D1 — horas/semana promedio por sexo × tramo de edad** (descriptivo, sin
signo pre-registrado, VEREDICTO máximo posible `DISCRIMINA`, obtenido
`DISCRIMINA`):

| grupo | horas/semana | grupo | horas/semana |
|---|---|---|---|
| hombre 12-17 | 4.53 | mujer 12-17 | 6.70 |
| hombre 18-29 | 6.10 | mujer 18-29 | 21.89 |
| hombre 30-39 | 11.47 | mujer 30-39 | 28.31 |
| hombre 40-59 | 5.89 | mujer 40-59 | 10.92 |
| hombre 60+ | 5.50 | mujer 60+ | 6.43 |

**Hallazgo declarado, no adjudicado.** Dentro de cada tramo de edad, las
mujeres dedican más horas que los hombres — consistente con "recae sobre
mujeres" en sentido comparativo. Pero el **locus** del cuidado no es 40+: las
mujeres de 30-39 (28.31h) y 18-29 (21.89h) dedican **más** horas por persona
que las de 40-59 (10.92h) o 60+ (6.43h) — y son población más numerosa
(D1 arriba, `n`). Es lo que explica por qué el share agregado de mujeres 40+
(22.15%) es menor que su peso poblacional (26.57%): el cuidado en México
recae desproporcionadamente sobre **mujeres**, pero concentrado en edad
reproductiva/crianza (18-39), no específicamente en el tramo 40+ que la
regla nombra ("hijas/nueras"). Esta pieza no adjudica si eso refuta,
matiza o simplemente añade textura a R5.2 — es lectura de mesa.

## (d) — `dinero.ahorro.horizonte_corto` (ENIF 2024)

| desenlace | sin seg. social | con seg. social | veredicto |
|---|---|---|---|
| horizonte_corto (P4_10=1) | 33.06% [31.22%,34.92%] n=4973 | 17.34% [15.71%,19.07%] n=4058 | **CORROBORADA** |
| horizonte_corto sens. (P4_10∈{1,2}) | 54.13% [52.16%,56.08%] n=4973 | 36.97% [34.80%,39.23%] n=4058 | **CORROBORADA** |
| ahorra_solo_informal | 41.35% [39.40%,43.29%] n=4973 | 31.12% [29.04%,33.17%] n=4058 | **CORROBORADA** |

**Regresión declarada, no silenciada.** `ahorra_solo_informal × formalidad`
YA fue calculado por `MAESTRA35-L1 · P2` (`tools/medidor_ahorro_enif24.py
--ejes`) sobre un universo ligeramente distinto (sin exigir `P4_10` válido):
sin seg. social 41.37% n=5 142, con seg. social 30.93% n=4 170, también
`CORROBORADA`. La fila de esta pieza usa el universo restringido a la
intersección triple (con `P4_10` válido, n=9 031 vs. 9 312 de `L1`) para
mantener los tres desenlaces de esta pieza sobre el mismo universo
comparable entre sí -- **no es una entrada nueva a la propuesta**, es
contexto de regresión que confirma que restringir a `P4_10` válido no mueve
el hallazgo de `L1` (diferencia de 3.º decimal). Lo genuinamente nuevo de
esta pieza es `horizonte_corto`.

---

## Resumen de veredictos B-bis

| Pieza | Desenlace/eje | Veredicto |
|---|---|---|
| a | denuncia × seguro | CORROBORADA |
| b | unión libre × cohorte (EDER) | CORROBORADA |
| b | unión libre × edad (ENADID) | CORROBORADA |
| c | reparto del hogar × mujeres 40+ | (razón, sin eje — ver contexto arriba) |
| c | horas × sexo×edad | DISCRIMINA (sin signo, tope declarado) |
| d | horizonte_corto × seg. social | CORROBORADA |
| d | ahorra_solo_informal × seg. social | CORROBORADA (=L1, no es entrada nueva) |

Ninguna pieza cerró `NO-DISCRIMINA` ni `CONTRARIA`. Cuatro entradas nuevas
van al pie de `milpa/tramite-ola5-propuesta-v0.yaml` en este mismo commit,
todas `PENDIENTE-DE-MESA`, ninguna cargada al motor.
