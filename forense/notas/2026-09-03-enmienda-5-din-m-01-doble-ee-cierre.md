# `ENMIENDA 5` · `DIN-M-01` con las dos `EE` — cierre

`ENMIENDA 5` sobre `forense/encargos/cola/2026-09-01-MAESTRA34-N3-AGREGA-2.md`,
3/sep/2026. Implementa la reserva de la firma `d1` (`FP-249`, mesa,
2/sep/2026, verbatim en `exclusiones-v1_2.md:36-42`) que ninguna enmienda
anterior de N3 (1/3/4) cubría: `tools/score_marco_m.py` solo lee `EE_R`
(líneas 80-87), nunca `EE_R_sin_diseno`.

## Qué corrió

`forense/prereg-duelo-v2/din_m_01_doble_ee.py` (nuevo, fuera de
`tools/`; no toca `score_marco_m.py`, `agregado_v1_1.py` ni
`procedimiento-scoring-v1_1.md`). Lee `corridas-R/DIN-M-01.json`
(`R`, `EE_R`, `EE_R_sin_diseno`), `corridas-M/M-DIN-M-01__v1_2.json`
(`valor_punto`) y `L-extraido-v1_2.tsv` (media de las 8 réplicas
`L-solo` EXTRAIBLE) y calcula, con cada `EE`, `z_L`, `z_M`,
`dif_pareada_z = z_L − z_M` (misma unidad y comparación principal de
`procedimiento-scoring-v1_1.md` §1/§3) y su veredicto de banda
(`-0.5 <= dif_pareada_z <= 0.5`).

Salida completa en `forense/prereg-duelo-v2/din-m-01-doble-ee-resultado.json`.

## Resultado

| `EE` usada | valor | `z_L` | `z_M` | `dif_pareada_z` | veredicto |
|---|---|---|---|---|---|
| `EE_R` (aproximada) | `0.004821494748362768` | `11.157` | `3.987` | `7.170` | FUERA-DE-BANDA |
| `EE_R_sin_diseno` | `0.004018626879101259` | `13.386` | `4.783` | `8.603` | FUERA-DE-BANDA |

El veredicto **no cambia** entre las dos `EE` — con el factor de diseño
medido (`1.1997866170250338`, ya escrito en `corridas-R/DIN-M-01.json` por
`ACTO MAESTRA35-L5`) ambas `z` quedan muy por fuera de la banda
`[-0.5, 0.5]`, el `L_solo`/`M` de esta celda están lejos de `R` en
cualquiera de las dos unidades. Por la regla `d1`: **`DIN-M-01` cuenta como
puntuada**, no queda AMBIGUA-POR-DISEÑO. La reserva de diseño
(`EE_R` es cota inferior; factor `≈1.1998`; conglomerado de viviendas del
diseño real no público) queda escrita en el JSON de resultado y en esta
nota, para el scoreboard.

## Contador

`celdas puntuadas v1_2: 0 → 1 de 14` (`DIN-M-01`, con reserva de diseño
declarada, sin AMBIGUA-POR-DISEÑO). Las 13 celdas restantes de
`marco-M-sorteado-v1_2.tsv` quedan fuera del perímetro de esta enmienda —
P1/P2/P3 completos de `ACTO MAESTRA34-N3 · AGREGA-2` siguen pendientes de
ejecución (compuerta y perímetro sin cambio salvo lo aquí declarado).

## Perímetro tocado

- `forense/prereg-duelo-v2/din_m_01_doble_ee.py` (nuevo)
- `forense/prereg-duelo-v2/din-m-01-doble-ee-resultado.json` (nuevo)
- `forense/encargos/cola/2026-09-01-MAESTRA34-N3-AGREGA-2.md` (`ENMIENDA 5`,
  apéndice — A.3, no edita el verbatim anterior)
- esta nota

`tools/score_marco_m.py`, `agregado_v1_1.py` y
`procedimiento-scoring-v1_1.md` **sin editar**.
