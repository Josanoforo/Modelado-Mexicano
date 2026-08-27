# MARCADOR DEL PILOTO v1.0 — el primer marcador del programa

> **SUPERADO por `marcador-piloto-v1_1.md`** (`ACTO MAESTRA30-E9 · SCORING-V2`, 26/ago/2026, `ADR-209`). Este documento queda intacto, sin editar, como registro histórico del primer intento; v1.1 corrige la reserva `FP-163` (aquí citada como `ABIERTA`; FIRMADA desde `ADR-199`) y re-deriva `M` bajo el crosswalk corregido de `ADR-208` (el mismo cero, ya no por el defecto de subcadena que este documento cita como causa).

> **PILOTO SIN VEREDICTO (D-i) — este documento puntúa; no adjudica ADV1-M5, no mueve tier alguno, no abre fila de tablero.**

**ACTO MAESTRA30-E7 · R-SCORING**, 26/ago/2026. Duelo `ADV1-M2`, 15 celdas sorteadas del marco congelado. `main` en `3bc28b1`.

**Escalas, declaradas antes de la tabla (A-bis 3).** `L-solo` se elicitó en **porcentaje** (mediana de sus `k` capturas válidas); `R` se computa como **proporción**. El enlace entre ambas es exactamente `L% / 100`, aplicado a `L` y a nada más. `EE`, `dif` y `banda` van en **puntos porcentuales**. Ninguna otra escala se cruza en este documento.

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

`L-solo` es la mediana de las capturas con `valor_extraido` no nulo. Las cinco columnas de corredor que van con una sola palabra **no son abreviaturas de un resultado**: son estados, y la §2 dice de dónde sale cada uno.

## 2 · Por qué cuatro de los cinco corredores están vacíos

| corredor | estado | de dónde sale ese estado |
|---|---|---|
| **L-solo** | **corrió** | 120 capturas de `ACTO MAESTRA30-E6 · L-RUN` (`ADR-206`), 15 celdas × `k=8`, temperatura `1.0`, cero descartes. **Es el único corredor con valores.** |
| **L+corpus** | no ejecutado | `FP-165` **FIRMADA**: mesa cerró la puerta a nuevas llamadas API. «El hueco no se tapa, se declara permanente.» |
| **M** | `NO-EMITE` en las 15 | `DERIVACION-M-v1_0.md`: el crosswalk sellado cubre las 15 pero da `NO-EMITE` en 12, y los 3 `CANDIDATO-EMITE` son falsos positivos de subcadena que cruzan encuesta. **Cero puntos M.** |
| **B** | `SIN_BASELINE` en las 15 | `elegir_baseline` invocado por su propia firma. Las 9 arbitrables tienen `publicada = NO` en el marco — la prueba del bibliotecario `FP-93` no halló el reactivo publicado en ninguna. Sin ola pública previa y sin serie, aplica la rama (3) del propio corredor. |
| **E** | `INEJECUTABLE` | `ADR-141` lo selló como `mediana_por_cuantil({L-solo, L+corpus, M})` — **tres** corredores. Faltan dos. Consecuencia ya declarada en `FP-165`, no descubierta aquí. |

**El scoring no adjudica porque no arranca.** `scoring-adv1-m3.py` se ejecutó y falló cerrado, verbatim: `CONFIGURACION_INVALIDA: se requiere exactamente 1 corredor L/corpus; hay 0`. Su `validar_configuracion` exige los **cuatro** corredores activos y el piloto tiene **uno**. Registro completo del intento en `corridas-R/_scoring-intento.json`. No se le pasó una configuración falsa para arrancarle números.

**Y por eso la columna de casilla dice «no evaluable» en las 15.** Las cinco casillas de `ADV1-M5 v2` se deciden sobre `IC(Δs)`, y `s` es *skill* **contra `B`**: `skill(error_corredor, error_baseline)`. Sin `B` no hay `s`; sin `s` no hay casilla — ni siquiera la (4), que es la que habla de B. `D-i` ya mandaba no adjudicar; aquí además **no habría con qué**.

---

## 3 · Agregados — comparación principal `L-solo` (FP-162)

- **Celdas con árbitro computable:** **9 de 15**. Las otras 6, con su razón escrita celda por celda **antes** de correr, en `PROCEDIMIENTO-R-v1_0.md` y `ENMIENDA-1`.
- **SKIP por `CV ≥ 30%` (FP-79): 0.** El CV más alto es `DIN-05` con **11.73%**; el más bajo `TIC-08` con **0.26%**. Ninguna celda se acerca al umbral.
- **Dentro de la banda TOST (`|dif| ≤ 0.5·EE(R)`): 1 de 9** — solo `CIV-08`.
- **`L-solo` dentro del `IC80` de `R`: 1 de 9** — la misma celda.
- **Desviación absoluta:** mediana **14.40 pp**; mínima **0.12 pp** (`CIV-08`); máxima **57.95 pp** (`TIC-08`).
- **`L+corpus` como auxiliar:** no hay auxiliar. No se ejecutó.

**`CIV-08` merece una línea propia, dicha con su reserva.** `L-solo` dio `62.00%` contra un árbitro de `61.88% ± 0.270`: cae dentro de la banda por `0.12` pp contra una banda de `0.135` pp — **margen de 0.015 pp**. Se reporta **como cae**, que es lo que la contraparte de A-bis manda, y no se convierte en «acierto»: es una sola celda de nueve, la banda es estrecha porque el `EE` es pequeño, y la constante `0.5` que la define **no está firmada por mesa** (`FP-163` sigue abierta). En el otro extremo, `TIC-08` separa `−57.95` pp y `TIC-01` `+48.01` pp.

**Lo que este documento NO dice.** No dice qué casilla de `ADV1-M5` corresponde — ninguna es evaluable. No dice que `L` gane ni pierda. No mueve un tier. No abre fila de tablero. No sella la banda. `D-i` manda, y la cabecera de arriba es su forma verbatim.

---

## 4 · Procedencia de cada cifra

- `L-solo` → `forense/prereg-duelo-v2/corridas-L/{celda}__L-solo__{01..08}.json` (`ADR-206`, `PR #377`).
- `R`, `EE`, `CV`, `IC` → `forense/prereg-duelo-v2/corridas-R/{celda}.json`, producidos por `correr-R.py` con `tests/svystat.py:prop_ultimate_cluster`.
- `B` → `corridas-R/_corredor-B.json`, producido por `correr-B.py` invocando `corredor-B-tasa-base.py:elegir_baseline`.
- Banda TOST → `prereg-corrida-v1_0.md` F3, regla de forma `0.5·EE(R)`.
- `IC80` → `scoring-adv1-m3.py:ArbitroR.ic_80`, importado.
- Spec de cada celda → `marco-congelado-piloto-v1_0.tsv`, `sha256 3a0dcf01…0c3742e2`.
