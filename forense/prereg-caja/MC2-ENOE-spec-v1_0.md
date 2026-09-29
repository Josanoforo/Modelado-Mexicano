# MC2 · ENOE (olas vistas 2025T4 y 2023T3) · participación, brecha de ingreso, estado conyugal y menores de 25 · spec v1.0

ACTO GEN2-MEDICION-CARRILES-2, hija ENOE, CAJA, rama `acto/gen2-medicion-carriles-2--enoe`. CALC
`data/corrida0/CALC-MC2-ENOE-0001` (prueba `tests/test_mc2_enoe.py`). Todo RETROSPECTIVA. No adopta.

## 0 · Premisas, reserva y lectura previa

- `[EJECUTADO]` Reserva: `enoe_2026_1t_*` (RESERVADA-ASTRA5-U1-ULTIMA-OLA-CORPUS-NO-ABRIR) y `cc1_inegi_enoe_2026t2__*`
  (RESERVADA-NO-ABIERTA-NO-INDEXAR-L) son la última ola y no son input (regla de mesa, ADENDA-2: se miden olas vistas
  y se declara). 2025T4 y 2023T3 son olas vistas: las leyó `CALC-ENOE-PISOS-0003` (sellado).
- Payloads: `enoe_2025_4t_microdatos` (miembro `ENOE_SDEMT425.csv`) y `enoe_2023_3t_microdatos` (`ENOE_SDEMT323.csv`).
- Lectura previa: cabecera de los dos SDEMT; FD de ENOE citado por el mapa (CLASE1, CLASE2, SEX, EDA, E_CON, INGOCUP,
  EMP_PPAL); de `CALC-ENOE-PISOS-0003` **sólo las llaves** de su tabla (conducta, eje, segmento, ola), no sus valores.
- E.5: `CALC-ENOE-PISOS-0003` ya trae por trimestre `empleo_informal` (EMP_PPAL) y `ingreso_ocupado_nominal` en los ejes
  nacional, sexo, edad (15-29 …), escolaridad, localidad (MENOS-2K5 … 100K+) y entidad. Esas afirmaciones se contrastan
  contra sus celdas selladas (reglas de §3, fijadas antes de leer los valores). Lo nuevo aquí: participación (CLASE1)
  por sexo, brecha de ingreso como razón con IC de la misma réplica, peso de 15-24 en la población ocupada y estado
  conyugal (E_CON).

## 1 · Variables por texto (A.15)

Universo INEGI de la población de 15 años y más: `r_def` = 00, `c_res` ∈ {1, 3}, `eda` 15–98. Ponderador `fac_tri`;
estrato `est_d_tri`; UPM `upm`.
- `clase1` «clasificación de la población en PEA y PNEA»: 1 PEA, 2 PNEA → PARTICIPA = 1.
- `clase2` 1 = población ocupada. `ingocup` «ingreso mensual» (valor de la pregunta 6b): válido si > 0 y < 999 998;
  INGRESO-MEDIO = media ponderada entre ocupados con ingreso válido; BRECHA = 1 − media MUJER / media HOMBRE (misma réplica).
- OCUPADO-MENOR25 = `eda` 15–24 entre ocupados.
- `e_con` «estado conyugal»: 1 unión libre, 2 separado, 3 divorciado, 4 viudo, 5 casado, 6 soltero, 9 no especificado
  (fuera). Categorías UNION-LIBRE, CASADO, SOLTERO, SEPARADO-DIVORCIADO-VIUDO; 15+ y 15-29.
- `sex` 1 hombre, 2 mujer.

IC95: bootstrap de UPM dentro de estrato, 2 000 réplicas, `PCG64(42)`, percentiles 2.5/97.5.

## 2 · Pre-registro B-bis (fijado antes del dato)

Regla de nivel: `c` ∈ IC95 → CONFIRMA; |punto − c| ≤ 0.10 → MATIZA; si no, ROMPE. Para celdas selladas de
`CALC-ENOE-PISOS-0003` se usan su `punto`, `ic95_lo`, `ic95_hi`. Otra ola o proxy → tope MATIZA.

| afirmación | estimando que manda y regla |
|---|---|
| GEN-009 | 2025T4-PARTICIPA-MUJER vs 0.46 y -HOMBRE vs 0.77 (nivel); el alza 2005→2025 no se mide: `PARCIAL` |
| GEN-011 | 2025T4-INGRESO-BRECHA-MUJER-HOMBRE vs 0.14 (nivel); ROMPE si punto ≤ 0 |
| PAREJA-003 | (2023T3) 15MAS: UNION-LIBRE 0.178, CASADO 0.369, SOLTERO 0.331; 15-29: SOLTERO 0.727, UNION-LIBRE 0.17, CASADO 0.083 (nivel, el peor) |
| TRAB-022 | «55 % de la fuerza de trabajo tiene menos de 25 años»: 2025T4-OCUPADO-MENOR25-NAC vs 0.55 (nivel) |
| CLASE-006 | sellado `empleo_informal` 2025T4 nacional NAC vs 0.55 (nivel) |
| CONOC-029 | sellado 2025T4: nacional vs 0.55; entidad 20 (Oaxaca) 0.801, 12 (Guerrero) 0.757, 07 (Chiapas) 0.749 (nivel, el peor); ROMPE si esas tres no son las tres de mayor punto entre las 32 |
| GEN-010 | sellado 2025T4 sexo: MUJER vs 0.55, HOMBRE vs 0.49 (nivel); ROMPE si MUJER ≤ HOMBRE. La ola del report no se nombra: tope MATIZA |
| JUV-028 | «más de la mitad de los ocupados de 20–30 trabaja en la informalidad»: sellado 2025T4 edad 15-29 (proxy de 20–30, tope MATIZA): ROMPE si punto < 0.5 |
| TIME-009 | «tasa urbana (TIL1) de 42.9 %» (2025): sellado 2025T4 localidad 100K+ vs 0.429 (nivel); proxy de «urbana», tope MATIZA |
| ENOE-001 / TIME-008 | ya dictaminadas en `forense/analisis/dominios/resultado-por-afirmacion-v1_0.tsv` (CALC-ENOE-PISOS-0003, 2024T3): **citadas**, no se re-miden ni se re-dictaminan |

## 3 · Módulo de auditoría v2.16

Unidad persona 15+ (o ocupada); RETROSPECTIVA. Informalidad y participación son estructura del mercado de trabajo, no
cultura; la brecha de ingreso es asociación sin control de horas, ocupación ni escolaridad (se declara). Segmentos por
sexo, edad, localidad y entidad. Sin variables de ascendencia.

El primer resultado que produzca este procedimiento es el que se reporta.
