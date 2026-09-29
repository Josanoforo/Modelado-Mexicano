# MC2 · ENIGH 2022 (ola vista, en lugar de 2024 reservada) · brechas regionales, decil I y X, Gini · spec v1.0

ACTO GEN2-MEDICION-CARRILES-2, hija ENIGH, CAJA, rama `acto/gen2-medicion-carriles-2--enigh`. CALC
`data/corrida0/CALC-MC2-ENIGH2022-0001` (prueba `tests/test_mc2_enigh2022.py`). Todo RETROSPECTIVA. No adopta.

## 0 · Premisas, reserva y lectura previa

- ENIGH 2024 es ola RESERVADA salvo seis columnas AMAI (memoria operativa §1); por la regla de mesa (ADENDA-2) se mide
  la ola vista **ENIGH 2022 Nueva Serie** (`enigh2022_nc_csv`, ya abierta por `CALC-PDR1-ENIGH2022-0001` y
  `CALC-ENIGH2022-*`) y se declara: toda afirmación sobre 2024 queda con **tope MATIZA** (otra ola).
- Miembro: `conjunto_de_datos_concentradohogar_enigh2022_ns.csv` (unidad hogar; `factor`; `est_dis`; `upm`).
- Lectura previa: cabecera del concentrado y descripción de la base 2022; de `CALC-ENIGH2022-INTENSIDAD-REMESAS-0001`
  sólo los ids de sus RESULT, no sus valores.

## 1 · Variables y construcción

- `ing_cor` ingreso corriente trimestral; `transfer` transferencias; `gasto_mon` gasto corriente monetario trimestral
  (mensual = /3); `alimentos` gasto en alimentos, bebidas y tabaco; entidad = dos primeros dígitos de `ubica_geo`
  (09 CDMX, 07 Chiapas, 19 Nuevo León).
- Deciles de hogares por `ing_cor`, cortes ponderados de la muestra completa (fijos en todas las réplicas; declarado).
- Razones de la misma réplica: GASTO-RAZON-CDMX-CHIAPAS, ING-RAZON-NUEVO-LEON-CHIAPAS, D1-ALIMENTOS-SOBRE-INGRESO,
  D1-TRANSFER-SOBRE-INGRESO (razón de medias en el decil I), D10-PARTICIPACION-INGRESO (Σ ingreso decil X / Σ ingreso).
- Gini ponderado por hogar de `ing_cor` (con transferencias) y de `max(ing_cor − transfer, 0)` (sin transferencias);
  IC por bootstrap de UPM dentro de estrato con semilla `seed + 1` (bucle propio; declarado).
- IC95 del resto: bootstrap de UPM dentro de estrato, 2 000 réplicas, `PCG64(42)`.

## 2 · Pre-registro B-bis (fijado antes del dato)

Regla de nivel (hijas MC2) con **tope MATIZA** por ser otra ola; para razones y montos «nivel» se lee en escala
relativa: CONFIRMA si la cifra ∈ IC95; MATIZA si |punto − c| / c ≤ 0.25; si no, ROMPE.

| afirmación | estimando y regla |
|---|---|
| CONS-023 | GASTO-RAZON-CDMX-CHIAPAS vs 2.5 (relativa); montos mensuales 22 128 y 9 039 reportados, no mandan (pesos de otro año) |
| FAM-036 | ING-RAZON-NUEVO-LEON-CHIAPAS vs 117 034/41 084 = 2.849 (relativa) |
| FAM-034 | D1-ALIMENTOS-SOBRE-INGRESO vs 0.50, D1-TRANSFER-SOBRE-INGRESO vs 0.36, D10-PARTICIPACION-INGRESO vs 0.303 (nivel absoluto; el peor) |
| MER-004 | GINI-CON-TRANSFERENCIAS vs 0.391 (nivel absoluto) |
| MER-005 | GINI-SIN-TRANSFERENCIAS vs 0.450 (nivel absoluto); ROMPE si GINI-SIN ≤ GINI-CON (las transferencias no igualarían) |
| FIN-031 | E.5 `RESULT-ENIGH22-REMINT-PARTICIPACION-MEDIA-HOGAR` (+ IC-LO/IC-HI) vs 0.30 (nivel absoluto) |
| FIN-032 | E.5 `RESULT-ENIGH22-REMINT-RECEPTORES-MASA` (hogares receptores expandidos) vs 1 530 000 (relativa, sin IC: CONFIRMA si ≤ 0.10, MATIZA si ≤ 0.25) |
| MIGR-006 | afirmación sobre la construcción de variables (`remesas`, `transf_hog`, `bene_gob`), no cifra: **PISO-SIN-DICTAMEN**; verificada por texto en la descripción de la base |
| SALMEN-028 | precio por sesión de consulta psicológica: ENIGH registra gasto trimestral del hogar por clase, no precio por sesión: **NO-CONSTRUIBLE** por texto |

## 3 · Módulo de auditoría v2.16

Unidad hogar; RETROSPECTIVA; ninguna cifra se promedia con unidades persona. Brechas regionales y deciles son
estructura de ingreso y precios, no cultura. El Gini «sin transferencias» es contable (no contrafactual de conducta).

El primer resultado que produzca este procedimiento es el que se reporta.
