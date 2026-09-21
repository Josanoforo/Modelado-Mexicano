# Lista para mesa · lecturas L pineables por la vía (i)

**Acto:** `GEN2-L-DESDE-CAPTURAS-1`, 21/sep/2026. **CALC:**
`CALC-L-DESDE-CAPTURAS-v1_0` (`RESULT-LDESC-TABLA-JSON`,
`RESULT-LDESC-DIFERENCIAS-VS-GEN1-JSON`).

**No pinea nada** (PARO (b) del encargo). Esto es insumo para que mesa
firme, con el RESULT que cada fila citaría si lo hace.

## 1 · Vía (i) satisfecha para las 26/28 con mediana

Las 26 de 28 slots con al menos una réplica válida cumplen la vía (i) de
4.1 (`CALC-L-DESDE-CAPTURAS-v1_0` mide desde capturas selladas con hash).
Eso es condición necesaria, no suficiente: mesa puede vetar por cobertura
baja (`n_validas` pequeño) aunque haya mediana.

| slot | n_validas/8 | mediana | IC95 | nota de cobertura |
|---|---|---|---|---|
| CIV-M-01:L-solo | 8 | 0.235 | [0.23, 0.26] | cobertura completa |
| CIV-M-01:L+corpus | 8 | 0.25 | [0.22, 0.27] | cobertura completa |
| CIV-M-02:L-solo | 8 | 0.275 | [0.25, 0.29] | cobertura completa |
| CIV-M-02:L+corpus | 8 | 0.24 | [0.23, 0.27] | cobertura completa |
| CIV-M-04:L-solo | 8 | 0.255 | [0.25, 0.26] | cobertura completa |
| CIV-M-04:L+corpus | 8 | 0.25 | [0.24, 0.26] | cobertura completa |
| CIV-M-10:L-solo | 8 | 0.23 | [0.21, 0.23] | cobertura completa |
| CIV-M-10:L+corpus | 8 | 0.23 | [0.22, 0.23] | cobertura completa |
| CIV-M-12:L-solo | 8 | 0.22 | [0.215, 0.23] | cobertura completa |
| CIV-M-12:L+corpus | 8 | 0.24 | [0.23, 0.25] | cobertura completa |
| CIV-M-13:L-solo | 8 | 0.2125 | [0.20, 0.22] | cobertura completa |
| CIV-M-13:L+corpus | 8 | 0.22 | [0.22, 0.23] | cobertura completa |
| FAM-M-05:L-solo | 8 | 0.05 | [0.046, 0.05] | cobertura completa |
| FAM-M-05:L+corpus | 8 | 0.0475 | [0.045, 0.048] | cobertura completa |
| FAM-M-06:L-solo | 8 | 0.05 | [0.045, 0.05] | cobertura completa |
| FAM-M-06:L+corpus | 8 | 0.05 | [0.047, 0.05] | cobertura completa |
| FAM-M-07:L-solo | 8 | 0.05 | [0.05, 0.055] | cobertura completa |
| FAM-M-07:L+corpus | 8 | 0.05 | [0.05, 0.05] | cobertura completa |
| TRA-M-03:L-solo | 6 | 0.105 | [0.10, 0.12] | 2 abstenciones |
| TRA-M-03:L+corpus | 6 | 0.12 | [0.12, 0.12] | 2 abstenciones |
| DIN-M-01:L-solo | 2 | 0.18 | [0.14, 0.22] | **baja cobertura (2/8)** |
| FAM-M-01:L-solo | 5 | 0.30 | [0.17, 0.31] | IC ancho |
| FAM-M-01:L+corpus | 1 | 0.30 | [0.30, 0.30] | **una sola réplica -- IC degenerado, no informativo** |
| TRA-M-02:L-solo | 4 | 0.15 | [0.14, 0.17] | mitad abstención |
| TRA-M-02:L+corpus | 1 | 0.15 | [0.15, 0.15] | **una sola réplica -- IC degenerado, no informativo** |
| TRA-M-07:L-solo | 2 | 0.10 | [0.08, 0.12] | **baja cobertura (2/8)** |

**Sin mediana (fuera de la vía (i) por ausencia de evento):**
`DIN-M-01:L+corpus` (0/8 válidas, todas abstención) ·
`TRA-M-07:L+corpus` (0/8 válidas, todas abstención).

## 2 · Recomendación (dirección, no adjudica)

Pineables sin reserva: las 18 filas con cobertura completa (8/8). Cinco
filas (`DIN-M-01:L-solo`, `FAM-M-01:L-solo`, `FAM-M-01:L+corpus`,
`TRA-M-02:L-solo`, `TRA-M-02:L+corpus`, `TRA-M-03:*`, `TRA-M-07:L-solo`)
tienen cobertura reducida por abstención — un IC ancho o degenerado no
adjudica por sí solo (§4 A-bis, instrucciones-proyecto-v2_15): «un punto
que satisface un umbral con un IC que no lo despeja no adjudica: propuesta
con reserva». Dos filas quedan sin mediana.

## 3 · Los 9 «rehecho con diferencia» (P6, `#959`), releídos con este CALC

Sobre el conjunto vigente (224 completas), la brecha entre GEN1 y GEN2 se
reduce en varias celdas frente a lo que reportó `CALC-TRIADA-0001`
(que agregó sobre `corridas-L/`, el conjunto viejo — ver spec.md §6). El
caso legible a mano, `TRA-M-02:L-solo`: `CALC-TRIADA-0001` publicó `0.14`;
este CALC, sobre el conjunto vigente, publica `0.15` — igual a la mediana
del conjunto v1.2 (`delta_conjunto_pp ≈ 0`). El detalle completo de los 28
slots está en `RESULT-LDESC-DIFERENCIAS-VS-GEN1-JSON`.

**No se toca `CALC-TRIADA-0001` ni `CALC-TRIADA-0002`.** Sus RESULT no se
mueven ni se adoptan desde este acto.
