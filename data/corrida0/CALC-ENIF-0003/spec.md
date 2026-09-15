# `CALC-ENIF-0003` — cara mecánica

Gobierna esta corrida la spec SELLADA
`forense/prereg-caja/ENIF-COBERTURA-Y-P410-spec-v1_0.md`
(**`prereg-caja-ENIF-COBERTURA-Y-P410`**, sha256 en el sidecar y en
`spec.yaml`). No edita `ENIF-AHORRO-spec-v1_0` ni ningún `RESULT` de
`CALC-ENIF-0001`/`0002`. Donde este resumen y la sellada digan cosas
distintas, **manda la sellada**.

**Acto:** `ACTO GEN2-LOTE-MEDICION-PENDIENTE-1` (piezas P3 `NC-0125` y P4
`NC-0126`), 14/sep/2026, CAJA (Ubuntu/WSL2), sobre `7de3acb4`.
**No releva ninguna `CORR-*`, no adopta, no toca `milpa/`.**

**CONGELADO en el COMMIT-1, antes de leer un solo valor del microdato.**

## P3 — qué recuenta

Sobre `TMODULO.csv` (ENIF 2024): filas totales, filas con `P3_13 ∈ {1..7}`,
filas del **universo triple** (`P3_13 ∈ {1..7} ∧ P4_10 ∈ {1..5}`), y sus
fracciones sin ponderar y ponderadas por `FAC_PER`. Hipótesis H1
pre-registrada: la «cobertura 66.89 %» sellada por `MAESTRA35-N8` es
`9 031 / 13 502` (universo triple, sin ponderar), no la cobertura de
`P3_13` (68.97 %) ni la ponderada del lote (67.53 % / 68.06 %). Veredictos
mecánicos al segundo decimal y a seis decimales contra `0.668937`.

## P4 — qué descompone

Dentro de `P4_10 = 1` («menos de una semana / no tiene ahorros»), la
proporción ponderada que **no ahorró por ninguna vía** en 12 meses
(`P5_1_1..6 ≠ 1 ∧ P5_6_1..9 ≠ 1`), con IC de diseño; el mismo indicador en
`P4_10 = 2` y `{3,4,5}` como contraste; y, en los universos del lote
(`U_A_SIN`, `U_A_CON`), cuánto del corte `{1}` y del `{1,2}` es «1 ∧ ninguna
vía». Todo se lee como **cota** del componente «no tiene ahorros», nunca como
su valor. La adjudicación es de mesa.
