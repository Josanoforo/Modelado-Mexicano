# MARCADOR DEL PILOTO v1.1 — el scoring real arrancó un nivel más, y falló cerrado en el siguiente

> **PILOTO SIN VEREDICTO (D-i) — este documento puntúa; no adjudica ADV1-M5, no mueve tier alguno, no abre fila de tablero.**

**ACTO MAESTRA30-E9 · SCORING-V2**, 26/ago/2026. Duelo `ADV1-M2`, las mismas
15 celdas sorteadas del marco congelado. `main` en `6d213a6` (incluye `E7
#378`, `E8 #380`, `E10 #379`). **Este documento SUPERA a `marcador-piloto-v1_0.md`**
(`ACTO MAESTRA30-E7 · R-SCORING`, `ADR-207`); v1.0 queda intacto, sin
editar, con su cabecera marcada `SUPERADO`.

**Escalas, declaradas antes de la tabla (A-bis 3).** Idénticas a v1.0:
`L-solo` se elicitó en **porcentaje** (mediana de sus `k` capturas
válidas); `R` se computa como **proporción**. El enlace entre ambas es
exactamente `L% / 100`, aplicado a `L` y a nada más. `EE`, `dif` y `banda`
van en **puntos porcentuales**. Ninguna otra escala se cruza en este
documento.

---

## 1 · La tabla, celda por celda

| celda | L-solo | L+corpus | M | B | E | R ± EE | banda TOST | dif (pp) | ¿en banda? | ¿L en IC80(R)? | CV | SKIP | casilla ADV1-M5 v2 |
|---|---:|---|---|---|---|---:|---:|---:|:-:|:-:|---:|:-:|---|
| **CIV-08** | 62.00% | no ejecutado | NO-EMITE | SIN_BASELINE | INEJECUTABLE | 61.88% ± 0.270 | ±0.135 | +0.12 | **sí** | **sí** | 0.44% | no | no evaluable |
| **DIN-03** | 34.50% | no ejecutado | NO-EMITE | SIN_BASELINE | INEJECUTABLE | 20.10% ± 0.863 | ±0.432 | +14.40 | no | no | 4.30% | no | no evaluable |
| **DIN-05** | 27.50% | no ejecutado | NO-EMITE | SIN_BASELINE | INEJECUTABLE | 1.73% ± 0.203 | ±0.101 | +25.77 | no | no | 11.73% | no | no evaluable |
| **DIN-07** | 26.25% | no ejecutado | NO-EMITE | SIN_BASELINE | INEJECUTABLE | — *RESERVA-SIN-MICRODATO* | — | — | — | — | — | — | no evaluable |
| **DIN-11** | 31.50% | no ejecutado | NO-EMITE | SIN_BASELINE | INEJECUTABLE | 45.84% ± 0.724 | ±0.362 | -14.34 | no | no | 1.58% | no | no evaluable |
| **DOC-06** | 80.00% | no ejecutado | NO-EMITE | SIN_BASELINE | INEJECUTABLE | — *RESERVA-SIN-PAYLOAD* | — | — | — | — | — | — | no evaluable |
| **EMP-02** | 90.00% | no ejecutado | NO-EMITE | SIN_BASELINE | INEJECUTABLE | — *RESERVA-SIN-MICRODATO* | — | — | — | — | — | — | no evaluable |
| **EMP-04** | 86.00% | no ejecutado | NO-EMITE | SIN_BASELINE | INEJECUTABLE | — *RESERVA-SIN-MICRODATO* | — | — | — | — | — | — | no evaluable |
| **EMP-05** | 25.00% | no ejecutado | NO-EMITE | SIN_BASELINE | INEJECUTABLE | — *RESERVA-SIN-MICRODATO* | — | — | — | — | — | — | no evaluable |
| **SFT-04** | 11.00% | no ejecutado | NO-EMITE | SIN_BASELINE | INEJECUTABLE | 6.04% ± 0.414 | ±0.207 | +4.96 | no | no | 6.86% | no | no evaluable |
| **SFT-06** | 34.00% | no ejecutado | NO-EMITE | SIN_BASELINE | INEJECUTABLE | 56.45% ± 1.445 | ±0.723 | -22.45 | no | no | 2.56% | no | no evaluable |
| **TIC-01** | 61.00% | no ejecutado | NO-EMITE | SIN_BASELINE | INEJECUTABLE | 12.99% ± 0.190 | ±0.095 | +48.01 | no | no | 1.46% | no | no evaluable |
| **TIC-06** | 48.75% | no ejecutado | NO-EMITE | SIN_BASELINE | INEJECUTABLE | — *RESERVA-SPEC-INCONSISTENTE* | — | — | — | — | — | — | no evaluable |
| **TIC-08** | 32.50% | no ejecutado | NO-EMITE | SIN_BASELINE | INEJECUTABLE | 90.45% ± 0.239 | ±0.119 | -57.95 | no | no | 0.26% | no | no evaluable |
| **TIC-12** | 43.75% | no ejecutado | NO-EMITE | SIN_BASELINE | INEJECUTABLE | 56.25% ± 0.288 | ±0.144 | -12.50 | no | no | 0.51% | no | no evaluable |

`L-solo` es la mediana de las capturas con `valor_extraido` no nulo (misma
fuente que v1.0, `corridas-L/` — sin cambio desde `E6`; re-derivada y
confirmada idéntica por este acto, comando en §4). Las cinco columnas de
corredor que van con una sola palabra **no son abreviaturas de un
resultado**: son estados, y la §2 dice de dónde sale cada uno.

## 2 · Por qué cuatro de los cinco corredores siguen vacíos — y qué cambió en `M`

| corredor | estado | de dónde sale ese estado |
|---|---|---|
| **L-solo** | **corrió** | 120 capturas de `ACTO MAESTRA30-E6 · L-RUN` (`ADR-206`), 15 celdas × `k=8`, temperatura `1.0`, cero descartes. **Es el único corredor con valores.** Sin cambio desde v1.0. |
| **L+corpus** | no ejecutado | `FP-165` **FIRMADA**: mesa cerró la puerta a nuevas llamadas API. «El hueco no se tapa, se declara permanente.» Sin cambio. |
| **M** | `NO-EMITE` en las 15 | **Re-derivado con el crosswalk corregido.** `ACTO MAESTRA30-E8` (`ADR-208`) reparó el defecto de subcadena de `construir_crosswalk` que v1.0 citaba como causa (`AP7_1`/`P7_12_7` vs `P7_1`, etc.). Bajo el crosswalk corregido, **0 de las 15 sorteadas llegan siquiera a `CANDIDATO-EMITE`** — de hecho tres de v1.0 (`DIN-03`, `DIN-11`, `TIC-06`) eran falsos positivos de subcadena y ahora caen a `NO-EMITE` limpio. `enlace-M-v1_0.md` completa la pasada 2 (cita de `(regla, conducta)`) sobre el resto del marco: 1 de 60 emite (`CIV-01`, fuera de la muestra). **Es el mismo cero que v1.0, pero ya no por un defecto conocido del engine — es el resultado honesto tras corregirlo.** Re-verificado en este acto por ejecución real de `construir_crosswalk()`, dos corridas frescas e idénticas entre sí y contra el crosswalk ya comprometido. |
| **B** | `SIN_BASELINE` en las 15 | `elegir_baseline` invocado por su propia firma. Las 9 arbitrables tienen `publicada = NO` en el marco — la prueba del bibliotecario `FP-93` no halló el reactivo publicado en ninguna. Sin cambio desde v1.0; fuera de perímetro de este acto (no se recalcula). |
| **E** | `INEJECUTABLE` | `ADR-141` lo selló como `mediana_por_cuantil({L-solo, L+corpus, M})` — **tres** corredores. Faltan dos. Sin cambio. |

### El scoring real arrancó un nivel más — y encontró un blindaje distinto

`E7` (v1.0) falló en la validación de **corredores**: el contrato exigía
los cuatro activos simultáneos y el piloto solo tenía uno.
`ACTO MAESTRA30-E8` (`ADR-208`) relajó ese contrato (enmienda `F1`):
mínimo `{(L,solo), (M,principal)}`, el resto opcional. Este acto
(`E9`) construyó la configuración más honesta posible bajo el contrato
nuevo — corredores reales, comparación principal ya firmada (`L-solo`,
`F0.1`/`ADR-197`) — y la corrió de verdad:

```json
{
 "resultado": "ErrorScoring",
 "codigo": "CONFIGURACION_INVALIDA",
 "mensaje": "faltan parámetros obligatorios: delta, nivel_ic, seed"
}
```

**Superó la capa que bloqueaba a v1.0 y falló cerrado en la siguiente.**
Los tres parámetros del bootstrap (`delta` como escalar único, `nivel_ic`,
`seed`) no tienen cita en ningún documento del árbol — búsqueda
exhaustiva declarada en `procedimiento-scoring-v1_0.md` §3. `delta` en
particular sí está firmado, pero como **regla por celda** (`0.5·EE(R)`
de esa celda, `FP-163`/`ADR-199`), no como el escalar único que el
esquema de `Configuracion` exige para una comparación agregada entre
celdas — un desajuste estructural entre cómo se firmó la banda TOST y
cómo el script agrega, no un olvido de cita. **No se inventa ninguno de
los tres.** Registro completo, con el documento de entrada íntegro:
`corridas-M/_intento-scoring-v1_1.json`; procedimiento congelado y
resultado: `procedimiento-scoring-v1_0.md`.

**Hallazgo adicional, declarado por lectura de código, no por una
segunda corrida con valores inventados:** aun si los tres parámetros
existieran, la comparación principal (`L-solo` vs `M`) fallaría de
inmediato con `SIN_CELDAS_PAREADAS` — `M` tiene 0 puntos en las 15, y
`L-solo` no tiene una `skill` normalizada poblable de forma honesta sin
un baseline `B` (`SIN_BASELINE` en las 15). Y aunque arrancara: el script
define `interval_score`/`crps_normal_aprox` pero `ejecutar_scoring` nunca
las invoca en su cuerpo — no hay salida de esas dos métricas que este
documento pueda reportar sin calcularlas por fuera del procedimiento
sellado, que está prohibido. Detalle completo en
`procedimiento-scoring-v1_0.md` §4.

**Y por eso la columna de casilla sigue diciendo «no evaluable» en las
15.** Las cinco casillas de `ADV1-M5 v2` se deciden sobre `IC(Δs)`, y `s`
es *skill* **contra `B`**: `skill(error_corredor, error_baseline)`. Sin
`B` no hay `s`; sin `s` no hay casilla — ni siquiera la (4), que es la
que habla de B. `D-i` ya mandaba no adjudicar; aquí además **no habría
con qué**.

### La comparación `L↔M` — no ocurre en este documento

El paso 5 del encargo la condiciona a que `M` tenga **≥1 punto, con su
`n`**. `M` tiene **0 puntos** sobre las 15 sorteadas (§2). `n = 0`. No hay
comparación `L↔M` que reportar — ni siquiera como fila vacía: reportarla
sería fabricar una entrada sin universo detrás.

---

## 3 · Agregados — comparación principal `L-solo` (FP-162)

- **Celdas con árbitro computable:** **9 de 15**. Las otras 6, con su
  razón escrita celda por celda **antes** de correr, en
  `PROCEDIMIENTO-R-v1_0.md` y `ENMIENDA-1`. Sin cambio desde v1.0 (este
  acto no toca `corridas-R/`).
- **SKIP por `CV ≥ 30%` (FP-79): 0.** El CV más alto es `DIN-05` con
  **11.73%**; el más bajo `TIC-08` con **0.26%**. Ninguna celda se acerca
  al umbral. Re-verificado, sin cambio.
- **Dentro de la banda TOST (`|dif| ≤ 0.5·EE(R)`): 1 de 9** — solo
  `CIV-08`.
- **`L-solo` dentro del `IC80` de `R`: 1 de 9** — la misma celda.
- **Desviación absoluta:** mediana **14.40 pp**; mínima **0.12 pp**
  (`CIV-08`); máxima **57.95 pp** (`TIC-08`).
- **`L+corpus` como auxiliar:** no hay auxiliar. No se ejecutó.

**`CIV-08` merece la misma línea que en v1.0, con su reserva corregida.**
`L-solo` dio `62.00%` contra un árbitro de `61.88% ± 0.270`: cae dentro de
la banda por `0.12` pp contra una banda de `0.135` pp — **margen de
0.015 pp**. Se reporta **como cae**, que es lo que la contraparte de
A-bis manda, y no se convierte en «acierto»: es una sola celda de nueve,
la banda es estrecha porque el `EE` es pequeño. **A diferencia de v1.0,
la constante `0.5` que define esa banda YA está firmada por mesa**
(`FP-163` FIRMADA, `ADR-199`, 26/ago/2026) — la reserva que v1.0 traía
("la constante `0.5` no está firmada por mesa") queda **corregida aquí**:
sigue siendo una sola celda de nueve y la banda sigue siendo estrecha,
pero ya no por una constante provisional. En el otro extremo, `TIC-08`
separa `−57.95` pp y `TIC-01` `+48.01` pp.

**Lo que este documento NO dice.** No dice qué casilla de `ADV1-M5`
corresponde — ninguna es evaluable. No dice que `L` gane ni pierda. No
mueve un tier. No abre fila de tablero. No sella la banda (ya está
sellada por otro acto). `D-i` manda, y la cabecera de arriba es su forma
verbatim.

---

## 4 · Procedencia de cada cifra

- `L-solo` → `forense/prereg-duelo-v2/corridas-L/{celda}__L-solo__{01..08}.json`
  (`ADR-206`, `PR #377`). Re-agregado por este acto
  (`python3 -c "..."` sobre `statistics.median`, mediciones no nulas) y
  confirmado idéntico a v1.0 para las 15 celdas.
- `R`, `EE`, `CV`, `IC` → `forense/prereg-duelo-v2/corridas-R/{celda}.json`,
  producidos por `correr-R.py` con `tests/svystat.py:prop_ultimate_cluster`.
  Sin cambio desde v1.0.
- `M` → `forense/prereg-duelo-v2/enlace-M-v1_0.md` (`ACTO MAESTRA30-E8`,
  `ADR-208`), re-verificado en vivo por
  `corridas-M/intento_scoring_e9.py` (ejecuta `construir_crosswalk()`, dos
  corridas frescas). Reemplaza la cita de v1.0 a `DERIVACION-M-v1_0.md`
  (diagnóstico pre-`E8`, con el defecto de subcadena aún presente).
- `B` → `corridas-R/_corredor-B.json`, producido por `correr-B.py`
  invocando `corredor-B-tasa-base.py:elegir_baseline`. Sin cambio.
- Banda TOST → `prereg-corrida-v1_0.md` F3, regla de forma `0.5·EE(R)`,
  **FIRMADA** `FP-163`/`ADR-199` (corrige la reserva `ABIERTA` de v1.0).
- `IC80` → `scoring-adv1-m3.py:ArbitroR.ic_80`, importado. Sin cambio.
- Intento de scoring real → `procedimiento-scoring-v1_0.md` (COMMIT-1 +
  COMMIT-2) y `corridas-M/_intento-scoring-v1_1.json`.
- Spec de cada celda → `marco-congelado-piloto-v1_0.tsv`,
  `sha256 3a0dcf01…0c3742e2`. Sin cambio.

## 5 · Qué avanzó de v1.0 a v1.1, en una línea

**El blindaje se movió una capa más adentro y se identificó con precisión
dónde falta la próxima firma de mesa** (`nivel_ic`/`seed` del bootstrap
de `scoring-adv1-m3.py`, y el desajuste `delta`-por-celda vs.
`delta`-escalar): sigue sin haber un solo punto `M`, sigue sin haber
veredicto, y el scoring de verdad sigue sin producir un número — pero ya
no por la misma razón que v1.0, y la razón nueva está acotada con más
precisión que la anterior.
