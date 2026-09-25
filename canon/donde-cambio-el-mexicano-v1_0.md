**Resumen.** 7872 series (conducta × segmento) dictaminadas: 583 ESTABLE · 8 CAMBIO-SOSTENIDO · 0 SALTO-DE-INSTRUMENTO · 81 SALTO-SIN-EXPLICAR · 7200 SIN-SERIE — suma de RESULT-DC-<INST>-N-<DICTAMEN> y RESULT-DC-<INST>-N-SERIES de los nueve CALC-<INST>-SERIE-DICTAMEN-0001.

# Dónde sí cambió el mexicano

ACTO GEN2-DONDE-CAMBIO-EL-MEXICANO-1 · GEN2 · `cuenta_gen2: SI` · `adopta: NO` · todo lo que sigue es **RETROSPECTIVA** (v2.16 §4): ninguna ola evaluada es posterior al sello de ninguna emisión. Vocabulario, umbrales y desempate sellados antes del primer dato en `forense/prereg-caja/DONDE-CAMBIO-spec-v1_0.md` (commit `9aea5a09`); mapa de series congelado sin valores en `forense/analisis/donde-cambio/mapa/CONGELADO.md`; tabla completa, una fila por serie, en `forense/analisis/donde-cambio/tabla-dictamen-v1_0.tsv`.

«Cambió» es un hecho de la serie, no de la psicología (v2.16 §3): este documento no atribuye causa. Unidad de cada cifra: puntos porcentuales (pp) de la proporción que la serie mide, en la unidad que declara (persona, hogar, delito o trámite); ninguna cifra de una unidad se suma con otra.

## Vocabulario (spec §4, primera regla que se cumple)

- `SIN-SERIE` — menos de tres olas comparables por texto con punto e IC en (0,1).
- `CAMBIO-SOSTENIDO` — dos o más pares COMPARABLE fuera del IC calibrado en la misma dirección, y más que en la contraria.
- `SALTO-DE-INSTRUMENTO` — un par fuera coincidente con un cambio de cuestionario, modo o diseño citado por texto.
- `SALTO-SIN-EXPLICAR` — algún par COMPARABLE fuera sin cumplir la regla de cambio sostenido (término de #972).
- `ESTABLE` — el piso t−1 cubre a t en todos los pares del tramo.

## Por instrumento

| instrumento | series | ESTABLE | CAMBIO-SOSTENIDO | SALTO-DE-INSTRUMENTO | SALTO-SIN-EXPLICAR | SIN-SERIE | τ² | RESULT |
|---|---|---|---|---|---|---|---|---|
| ENVIPE | 33 | 0 | 0 | 0 | 2 | 31 | CALCULADO-AQUI | `RESULT-DC-ENVIPE-N-*`, `RESULT-DC-ENVIPE-TAU2-*` |
| ENCIG | 11 | 9 | 0 | 0 | 2 | 0 | SELLADO | `RESULT-DC-ENCIG-N-*`, `RESULT-DC-ENCIG-TAU2-*` |
| ENIF | 796 | 132 | 0 | 0 | 5 | 659 | SELLADO | `RESULT-DC-ENIF-N-*`, `RESULT-DC-ENIF-TAU2-*` |
| ENUT | 46 | 2 | 0 | 0 | 0 | 44 | CALCULADO-AQUI | `RESULT-DC-ENUT-N-*`, `RESULT-DC-ENUT-TAU2-*` |
| ENIGH | 11 | 2 | 0 | 0 | 1 | 8 | CALCULADO-AQUI | `RESULT-DC-ENIGH-N-*`, `RESULT-DC-ENIGH-TAU2-*` |
| ENOE | 517 | 438 | 8 | 0 | 71 | 0 | CALCULADO-AQUI | `RESULT-DC-ENOE-N-*`, `RESULT-DC-ENOE-TAU2-*` |
| ENDIREH | 6311 | 0 | 0 | 0 | 0 | 6311 | CALCULADO-AQUI | `RESULT-DC-ENDIREH-N-*`, `RESULT-DC-ENDIREH-TAU2-*` |
| MOCIBA | 126 | 0 | 0 | 0 | 0 | 126 | CALCULADO-AQUI | `RESULT-DC-MOCIBA-N-*`, `RESULT-DC-MOCIBA-TAU2-*` |
| OTROS | 21 | 0 | 0 | 0 | 0 | 21 | CALCULADO-AQUI | `RESULT-DC-OTROS-N-*`, `RESULT-DC-OTROS-TAU2-*` |

τ²: `SELLADO` = parámetro de persistencia ya sellado (ENIF #1009, ENCIG #1041); `CALCULADO-AQUI` = mismo método, calculado en este acto y emitido como `RESULT-DC-<INST>-TAU2-<EJE>` reutilizable. OTROS = BANXICO, EDER, ENCUCI, ENFIH, ENNViH, ENSANUT, LAPOP, MOTRAL.

## Por dominio: qué cambió, qué saltó, qué es estable

### Seguridad y norma

2 series: 2 SALTO-SIN-EXPLICAR (conteo de filas de `tabla-dictamen-v1_0.tsv`, columna `result` → `RESULT-DC-<INST>-TABLA`).

**SALTO-SIN-EXPLICAR**

- `ENVIPE-NODENUNCIA-MIEDO-DESCONFIANZA-NACIONAL-TOTAL` — Proporción ponderada de delitos personales no denunciados cuya razón principal declarada f; unidad DELITO-PERSONAL-NO-DENUNCIADO; olas 2011–2025 (k=15); acumulado -6.2 pp; pares fuera: 2019→2020 -3.9 pp (COMPARABLE, toca 2020) · `RESULT-DC-ENVIPE-TABLA#serie_id=ENVIPE-NODENUNCIA-MIEDO-DESCONFIANZA-NACIONAL-TOTAL`
- `ENVIPE-R-NACIONAL-TOTAL` — R = proporción ponderada, sobre U_R (todos los tipos de delito de TMod_Vic, sin filtro de ; unidad DELITO-TODOS-TIPOS; olas 2012–2024 (k=6); acumulado -6.4 pp; pares fuera: 2015→2021 -3.9 pp (COMPARABLE) · `RESULT-DC-ENVIPE-TABLA#serie_id=ENVIPE-R-NACIONAL-TOTAL`

### Trámites y Estado

11 series: 2 SALTO-SIN-EXPLICAR · 9 ESTABLE (conteo de filas de `tabla-dictamen-v1_0.tsv`, columna `result` → `RESULT-DC-<INST>-TABLA`).

**SALTO-SIN-EXPLICAR**

- `ENCIG-C-LUZ-DIGITAL-EDAD-18-29` — Pago ordinario del servicio de luz realizado por canal digital útil (Internet/app o cajero; unidad TRAMITE; olas 2015–2023 (k=5); acumulado +9.4 pp; pares fuera: 2019→2021 +9.0 pp (COMPARABLE) · `RESULT-DC-ENCIG-TABLA#serie_id=ENCIG-C-LUZ-DIGITAL-EDAD-18-29`
- `ENCIG-C-LUZ-DIGITAL-ESCOLARIDAD-HASTA-PRIMARIA` — Pago ordinario del servicio de luz realizado por canal digital útil (Internet/app o cajero; unidad TRAMITE; olas 2015–2023 (k=5); acumulado -7.4 pp; pares fuera: 2021→2023 -9.2 pp (COMPARABLE) · `RESULT-DC-ENCIG-TABLA#serie_id=ENCIG-C-LUZ-DIGITAL-ESCOLARIDAD-HASTA-PRIMARIA`

### civico

7 series: 7 SIN-SERIE (conteo de filas de `tabla-dictamen-v1_0.tsv`, columna `result` → `RESULT-DC-<INST>-TABLA`).

### dinero

801 series: 664 SIN-SERIE · 5 SALTO-SIN-EXPLICAR · 132 ESTABLE (conteo de filas de `tabla-dictamen-v1_0.tsv`, columna `result` → `RESULT-DC-<INST>-TABLA`).

**SALTO-SIN-EXPLICAR**

- `ENIF-DIN-CREDITO-PISOS-ENIF-K2-AUTOMOTRIZ-ESCOLARIDAD-SECUNDARIA` — Proporciones marginales ponderadas ENIF 2012 de las conductas de crédito comparables por t; unidad proporción ponderada [0,1]; olas 2012–2021 (k=4); acumulado +0.2 pp; pares fuera: 2018→2021 +0.4 pp (COMPARABLE) · `RESULT-DC-ENIF-TABLA#serie_id=ENIF-DIN-CREDITO-PISOS-ENIF-K2-AUTOMOTRIZ-ESCOLARIDAD-SECUNDARIA`
- `ENIF-DIN-CREDITO-PISOS-ENIF-K2-NOMINA-CUENTA-SIN-CUENTA` — Proporciones marginales ponderadas ENIF 2012 de las conductas de crédito comparables por t; unidad proporción ponderada [0,1]; olas 2012–2018 (k=3); acumulado -0.2 pp; pares fuera: 2015→2018 -0.2 pp (COMPARABLE) · `RESULT-DC-ENIF-TABLA#serie_id=ENIF-DIN-CREDITO-PISOS-ENIF-K2-NOMINA-CUENTA-SIN-CUENTA`
- `ENIF-DIN-CREDITO-PISOS-ENIF-K2-NOMINA-EDAD-60-MAS` — Proporciones marginales ponderadas ENIF 2012 de las conductas de crédito comparables por t; unidad proporción ponderada [0,1]; olas 2012–2021 (k=4); acumulado -1.6 pp; pares fuera: 2015→2018 -1.1 pp (COMPARABLE); 2018→2021 +0.9 pp (COMPARABLE) · `RESULT-DC-ENIF-TABLA#serie_id=ENIF-DIN-CREDITO-PISOS-ENIF-K2-NOMINA-EDAD-60-MAS`
- `ENIF-DIN-CREDITO-PISOS-ENIF-K2-NOMINA-ESCOLARIDAD-HASTA-PRIMARIA` — Proporciones marginales ponderadas ENIF 2012 de las conductas de crédito comparables por t; unidad proporción ponderada [0,1]; olas 2012–2021 (k=4); acumulado -0.2 pp; pares fuera: 2018→2021 +0.5 pp (COMPARABLE) · `RESULT-DC-ENIF-TABLA#serie_id=ENIF-DIN-CREDITO-PISOS-ENIF-K2-NOMINA-ESCOLARIDAD-HASTA-PRIMARIA`
- `ENIF-DIN-CREDITO-PISOS-ENIF-K6-P-TENEDORES-EDAD-60-MAS` — Proporciones marginales ponderadas ENIF 2012 de las conductas de crédito comparables por t; unidad proporción ponderada [0,1]; olas 2012–2021 (k=4); acumulado -9.1 pp; pares fuera: 2015→2018 -16.4 pp (COMPARABLE) · `RESULT-DC-ENIF-TABLA#serie_id=ENIF-DIN-CREDITO-PISOS-ENIF-K6-P-TENEDORES-EDAD-60-MAS`

### familia

12 series: 12 SIN-SERIE (conteo de filas de `tabla-dictamen-v1_0.tsv`, columna `result` → `RESULT-DC-<INST>-TABLA`).

### genero

6311 series: 6311 SIN-SERIE (conteo de filas de `tabla-dictamen-v1_0.tsv`, columna `result` → `RESULT-DC-<INST>-TABLA`).

### ingreso-y-gasto

6 series: 3 SIN-SERIE · 1 SALTO-SIN-EXPLICAR · 2 ESTABLE (conteo de filas de `tabla-dictamen-v1_0.tsv`, columna `result` → `RESULT-DC-<INST>-TABLA`).

**SALTO-SIN-EXPLICAR**

- `ENIGH-REMINT-NACIONAL-PARTICIPACION_GE50_DE_REMESAS` — Marco completo de hogares del concentrado ENIGH 2016; dominio receptor remesas>0; dominio ; unidad proporcion; olas 2016–2022 (k=4); acumulado +7.4 pp; pares fuera: 2020→2022 +6.7 pp (COMPARABLE, toca 2020) · `RESULT-DC-ENIGH-TABLA#serie_id=ENIGH-REMINT-NACIONAL-PARTICIPACION_GE50_DE_REMESAS`

### salud

2 series: 2 SIN-SERIE (conteo de filas de `tabla-dictamen-v1_0.tsv`, columna `result` → `RESULT-DC-<INST>-TABLA`).

### tecnologia

126 series: 126 SIN-SERIE (conteo de filas de `tabla-dictamen-v1_0.tsv`, columna `result` → `RESULT-DC-<INST>-TABLA`).

### tiempo-y-cuidado

45 series: 43 SIN-SERIE · 2 ESTABLE (conteo de filas de `tabla-dictamen-v1_0.tsv`, columna `result` → `RESULT-DC-<INST>-TABLA`).

### trabajo

520 series: 3 SIN-SERIE · 8 CAMBIO-SOSTENIDO · 71 SALTO-SIN-EXPLICAR · 438 ESTABLE (conteo de filas de `tabla-dictamen-v1_0.tsv`, columna `result` → `RESULT-DC-<INST>-TABLA`).

**CAMBIO-SOSTENIDO**

- `ENOE-BUSCA-OTRO-TRABAJO-ESCOLARIDAD-PRIM-INCOMPLETA` SUBE — ENOE PISOS :: busca_otro_trabajo; unidad proporcion_0_1; olas 2005T1–2020T1 (k=21); acumulado -0.1 pp; pares fuera: 2008T1→2012T1 +0.5 pp (COMPARABLE); 2014T1→2016T1 -0.4 pp (COMPARABLE); 2016T4→2017T1 +0.4 pp (COMPARABLE); 2017T4→2018T1 +0.5 pp (COMPARABLE); 2019T4→2020T1 -0.8 pp (COMPARABLE, toca 2020) · `RESULT-DC-ENOE-TABLA#serie_id=ENOE-BUSCA-OTRO-TRABAJO-ESCOLARIDAD-PRIM-INCOMPLETA`
- `ENOE-BUSCA-OTRO-TRABAJO-LOCALIDAD-100K` BAJA — ENOE PISOS :: busca_otro_trabajo; unidad proporcion_0_1; olas 2005T1–2020T1 (k=21); acumulado -0.4 pp; pares fuera: 2005T1→2008T1 -0.3 pp (COMPARABLE); 2017T2→2017T3 -0.2 pp (COMPARABLE) · `RESULT-DC-ENOE-TABLA#serie_id=ENOE-BUSCA-OTRO-TRABAJO-LOCALIDAD-100K`
- `ENOE-DESALIENTO-DESISTIO-EDAD-15-29` SUBE — ENOE PISOS :: desaliento_desistio; unidad proporcion_0_1; olas 2005T1–2020T1 (k=21); acumulado -0.1 pp; pares fuera: 2008T1→2012T1 +0.2 pp (COMPARABLE); 2014T1→2016T1 -0.2 pp (COMPARABLE); 2019T2→2019T3 +0.1 pp (COMPARABLE) · `RESULT-DC-ENOE-TABLA#serie_id=ENOE-DESALIENTO-DESISTIO-EDAD-15-29`
- `ENOE-DESALIENTO-DESISTIO-ESCOLARIDAD-PRIM-INCOMPLETA` BAJA — ENOE PISOS :: desaliento_desistio; unidad proporcion_0_1; olas 2005T1–2020T1 (k=21); acumulado -0.0 pp; pares fuera: 2012T1→2014T1 -0.1 pp (COMPARABLE); 2017T1→2017T2 +0.1 pp (COMPARABLE); 2017T2→2017T3 -0.1 pp (COMPARABLE); 2017T3→2017T4 +0.0 pp (COMPARABLE); 2017T4→2018T1 -0.1 pp (COMPARABLE); 2018T2→2018T3 -0.0 pp (COMPARABLE); 2018T3→2018T4 +0.0 pp (COMPARABLE) · `RESULT-DC-ENOE-TABLA#serie_id=ENOE-DESALIENTO-DESISTIO-ESCOLARIDAD-PRIM-INCOMPLETA`
- `ENOE-DESALIENTO-DESISTIO-LOCALIDAD-100K` BAJA — ENOE PISOS :: desaliento_desistio; unidad proporcion_0_1; olas 2005T1–2020T1 (k=21); acumulado -0.1 pp; pares fuera: 2008T1→2012T1 +0.2 pp (COMPARABLE); 2014T1→2016T1 -0.2 pp (COMPARABLE); 2017T2→2017T3 -0.1 pp (COMPARABLE); 2019T1→2019T2 -0.1 pp (COMPARABLE) · `RESULT-DC-ENOE-TABLA#serie_id=ENOE-DESALIENTO-DESISTIO-LOCALIDAD-100K`
- `ENOE-DESALIENTO-DESISTIO-NACIONAL-NAC` BAJA — ENOE PISOS :: desaliento_desistio; unidad proporcion_0_1; olas 2005T1–2020T1 (k=21); acumulado -0.0 pp; pares fuera: 2008T1→2012T1 +0.2 pp (COMPARABLE); 2014T1→2016T1 -0.1 pp (COMPARABLE); 2017T2→2017T3 -0.1 pp (COMPARABLE) · `RESULT-DC-ENOE-TABLA#serie_id=ENOE-DESALIENTO-DESISTIO-NACIONAL-NAC`
- `ENOE-DESALIENTO-DESISTIO-SEXO-HOMBRE` BAJA — ENOE PISOS :: desaliento_desistio; unidad proporcion_0_1; olas 2005T1–2020T1 (k=21); acumulado -0.2 pp; pares fuera: 2008T1→2012T1 +0.2 pp (COMPARABLE); 2014T1→2016T1 -0.2 pp (COMPARABLE); 2018T1→2018T2 -0.2 pp (COMPARABLE); 2019T1→2019T2 -0.1 pp (COMPARABLE) · `RESULT-DC-ENOE-TABLA#serie_id=ENOE-DESALIENTO-DESISTIO-SEXO-HOMBRE`
- `ENOE-SUBOCUPACION-LOCALIDAD-MENOS-2K5` SUBE — ENOE PISOS :: subocupacion; unidad proporcion_0_1; olas 2005T1–2020T1 (k=21); acumulado -1.1 pp; pares fuera: 2005T1→2008T1 -3.6 pp (COMPARABLE); 2008T1→2012T1 +3.0 pp (COMPARABLE); 2019T1→2019T2 +2.3 pp (COMPARABLE) · `RESULT-DC-ENOE-TABLA#serie_id=ENOE-SUBOCUPACION-LOCALIDAD-MENOS-2K5`

**SALTO-SIN-EXPLICAR**

- `ENOE-BUSCA-OTRO-TRABAJO-EDAD-15-29` — ENOE PISOS :: busca_otro_trabajo; unidad proporcion_0_1; olas 2005T1–2020T1 (k=21); acumulado -0.1 pp; pares fuera: 2008T1→2012T1 +0.3 pp (COMPARABLE) · `RESULT-DC-ENOE-TABLA#serie_id=ENOE-BUSCA-OTRO-TRABAJO-EDAD-15-29`
- `ENOE-BUSCA-OTRO-TRABAJO-EDAD-30-44` — ENOE PISOS :: busca_otro_trabajo; unidad proporcion_0_1; olas 2005T1–2020T1 (k=21); acumulado -0.2 pp; pares fuera: 2008T1→2012T1 +0.4 pp (COMPARABLE) · `RESULT-DC-ENOE-TABLA#serie_id=ENOE-BUSCA-OTRO-TRABAJO-EDAD-30-44`
- `ENOE-BUSCA-OTRO-TRABAJO-EDAD-60` — ENOE PISOS :: busca_otro_trabajo; unidad proporcion_0_1; olas 2005T1–2020T1 (k=21); acumulado +0.0 pp; pares fuera: 2005T1→2008T1 +0.3 pp (COMPARABLE); 2017T4→2018T1 +0.2 pp (COMPARABLE); 2018T2→2018T3 -0.2 pp (COMPARABLE); 2019T4→2020T1 -0.4 pp (COMPARABLE, toca 2020) · `RESULT-DC-ENOE-TABLA#serie_id=ENOE-BUSCA-OTRO-TRABAJO-EDAD-60`
- `ENOE-BUSCA-OTRO-TRABAJO-ENTIDAD-01` — ENOE PISOS :: busca_otro_trabajo; unidad proporcion_0_1; olas 2005T1–2020T1 (k=21); acumulado -0.7 pp; pares fuera: 2012T1→2014T1 +0.6 pp (COMPARABLE) · `RESULT-DC-ENOE-TABLA#serie_id=ENOE-BUSCA-OTRO-TRABAJO-ENTIDAD-01`
- `ENOE-BUSCA-OTRO-TRABAJO-ENTIDAD-03` — ENOE PISOS :: busca_otro_trabajo; unidad proporcion_0_1; olas 2005T1–2020T1 (k=21); acumulado +0.7 pp; pares fuera: 2008T1→2012T1 +1.2 pp (COMPARABLE) · `RESULT-DC-ENOE-TABLA#serie_id=ENOE-BUSCA-OTRO-TRABAJO-ENTIDAD-03`
- `ENOE-BUSCA-OTRO-TRABAJO-ENTIDAD-10` — ENOE PISOS :: busca_otro_trabajo; unidad proporcion_0_1; olas 2005T1–2020T1 (k=21); acumulado -0.0 pp; pares fuera: 2005T1→2008T1 -0.7 pp (COMPARABLE) · `RESULT-DC-ENOE-TABLA#serie_id=ENOE-BUSCA-OTRO-TRABAJO-ENTIDAD-10`
- `ENOE-BUSCA-OTRO-TRABAJO-ENTIDAD-12` — ENOE PISOS :: busca_otro_trabajo; unidad proporcion_0_1; olas 2005T1–2020T1 (k=21); acumulado +0.8 pp; pares fuera: 2005T1→2008T1 -0.3 pp (COMPARABLE); 2008T1→2012T1 +1.3 pp (COMPARABLE); 2012T1→2014T1 -1.2 pp (COMPARABLE); 2014T1→2016T1 +1.1 pp (COMPARABLE); 2017T1→2017T2 -0.9 pp (COMPARABLE); 2019T3→2019T4 +1.2 pp (COMPARABLE) · `RESULT-DC-ENOE-TABLA#serie_id=ENOE-BUSCA-OTRO-TRABAJO-ENTIDAD-12`
- `ENOE-BUSCA-OTRO-TRABAJO-ENTIDAD-15` — ENOE PISOS :: busca_otro_trabajo; unidad proporcion_0_1; olas 2005T1–2020T1 (k=21); acumulado -0.7 pp; pares fuera: 2012T1→2014T1 -0.7 pp (COMPARABLE) · `RESULT-DC-ENOE-TABLA#serie_id=ENOE-BUSCA-OTRO-TRABAJO-ENTIDAD-15`
- `ENOE-BUSCA-OTRO-TRABAJO-ENTIDAD-16` — ENOE PISOS :: busca_otro_trabajo; unidad proporcion_0_1; olas 2005T1–2020T1 (k=21); acumulado +0.2 pp; pares fuera: 2016T4→2017T1 -0.7 pp (COMPARABLE) · `RESULT-DC-ENOE-TABLA#serie_id=ENOE-BUSCA-OTRO-TRABAJO-ENTIDAD-16`
- `ENOE-BUSCA-OTRO-TRABAJO-ENTIDAD-30` — ENOE PISOS :: busca_otro_trabajo; unidad proporcion_0_1; olas 2023T1–2025T4 (k=12); acumulado -0.0 pp; pares fuera: 2023T4→2024T1 +0.3 pp (COMPARABLE) · `RESULT-DC-ENOE-TABLA#serie_id=ENOE-BUSCA-OTRO-TRABAJO-ENTIDAD-30`
- `ENOE-BUSCA-OTRO-TRABAJO-ESCOLARIDAD-MEDIA-SUPERIOR` — ENOE PISOS :: busca_otro_trabajo; unidad proporcion_0_1; olas 2005T1–2020T1 (k=21); acumulado -0.4 pp; pares fuera: 2005T1→2008T1 -0.3 pp (COMPARABLE) · `RESULT-DC-ENOE-TABLA#serie_id=ENOE-BUSCA-OTRO-TRABAJO-ESCOLARIDAD-MEDIA-SUPERIOR`
- `ENOE-BUSCA-OTRO-TRABAJO-ESCOLARIDAD-PRIM-COMPLETA` — ENOE PISOS :: busca_otro_trabajo; unidad proporcion_0_1; olas 2005T1–2020T1 (k=21); acumulado +0.0 pp; pares fuera: 2008T1→2012T1 +0.5 pp (COMPARABLE) · `RESULT-DC-ENOE-TABLA#serie_id=ENOE-BUSCA-OTRO-TRABAJO-ESCOLARIDAD-PRIM-COMPLETA`
- `ENOE-BUSCA-OTRO-TRABAJO-ESCOLARIDAD-SECUNDARIA` — ENOE PISOS :: busca_otro_trabajo; unidad proporcion_0_1; olas 2005T1–2020T1 (k=21); acumulado -0.1 pp; pares fuera: 2008T1→2012T1 +0.3 pp (COMPARABLE) · `RESULT-DC-ENOE-TABLA#serie_id=ENOE-BUSCA-OTRO-TRABAJO-ESCOLARIDAD-SECUNDARIA`
- `ENOE-BUSCA-OTRO-TRABAJO-LOCALIDAD-15K-99K` — ENOE PISOS :: busca_otro_trabajo; unidad proporcion_0_1; olas 2005T1–2020T1 (k=21); acumulado -0.0 pp; pares fuera: 2008T1→2012T1 +0.5 pp (COMPARABLE) · `RESULT-DC-ENOE-TABLA#serie_id=ENOE-BUSCA-OTRO-TRABAJO-LOCALIDAD-15K-99K`
- `ENOE-BUSCA-OTRO-TRABAJO-LOCALIDAD-2K5-15K` — ENOE PISOS :: busca_otro_trabajo; unidad proporcion_0_1; olas 2005T1–2020T1 (k=21); acumulado -0.2 pp; pares fuera: 2019T4→2020T1 -0.4 pp (COMPARABLE, toca 2020) · `RESULT-DC-ENOE-TABLA#serie_id=ENOE-BUSCA-OTRO-TRABAJO-LOCALIDAD-2K5-15K`
- `ENOE-BUSCA-OTRO-TRABAJO-LOCALIDAD-MENOS-2K5` — ENOE PISOS :: busca_otro_trabajo; unidad proporcion_0_1; olas 2005T1–2020T1 (k=21); acumulado +0.4 pp; pares fuera: 2008T1→2012T1 +0.7 pp (COMPARABLE); 2014T1→2016T1 -0.4 pp (COMPARABLE); 2017T4→2018T1 +0.6 pp (COMPARABLE); 2019T4→2020T1 -0.6 pp (COMPARABLE, toca 2020) · `RESULT-DC-ENOE-TABLA#serie_id=ENOE-BUSCA-OTRO-TRABAJO-LOCALIDAD-MENOS-2K5`
- `ENOE-BUSCA-OTRO-TRABAJO-NACIONAL-NAC` — ENOE PISOS :: busca_otro_trabajo; unidad proporcion_0_1; olas 2005T1–2020T1 (k=21); acumulado -0.1 pp; pares fuera: 2005T1→2008T1 -0.2 pp (COMPARABLE); 2008T1→2012T1 +0.3 pp (COMPARABLE) · `RESULT-DC-ENOE-TABLA#serie_id=ENOE-BUSCA-OTRO-TRABAJO-NACIONAL-NAC`
- `ENOE-BUSCA-OTRO-TRABAJO-SEXO-HOMBRE` — ENOE PISOS :: busca_otro_trabajo; unidad proporcion_0_1; olas 2005T1–2020T1 (k=21); acumulado -0.2 pp; pares fuera: 2005T1→2008T1 -0.3 pp (COMPARABLE); 2008T1→2012T1 +0.4 pp (COMPARABLE) · `RESULT-DC-ENOE-TABLA#serie_id=ENOE-BUSCA-OTRO-TRABAJO-SEXO-HOMBRE`
- `ENOE-BUSCA-OTRO-TRABAJO-SEXO-MUJER` — ENOE PISOS :: busca_otro_trabajo; unidad proporcion_0_1; olas 2005T1–2020T1 (k=21); acumulado -0.0 pp; pares fuera: 2018T1→2018T2 +0.1 pp (COMPARABLE) · `RESULT-DC-ENOE-TABLA#serie_id=ENOE-BUSCA-OTRO-TRABAJO-SEXO-MUJER`
- `ENOE-DESALIENTO-DESISTIO-EDAD-30-44` — ENOE PISOS :: desaliento_desistio; unidad proporcion_0_1; olas 2005T1–2020T1 (k=21); acumulado -0.0 pp; pares fuera: 2008T1→2012T1 +0.4 pp (COMPARABLE); 2016T2→2016T3 -0.2 pp (COMPARABLE) · `RESULT-DC-ENOE-TABLA#serie_id=ENOE-DESALIENTO-DESISTIO-EDAD-30-44`
- `ENOE-DESALIENTO-DESISTIO-EDAD-45-59` — ENOE PISOS :: desaliento_desistio; unidad proporcion_0_1; olas 2005T1–2020T1 (k=21); acumulado +0.0 pp; pares fuera: 2016T4→2017T1 -0.1 pp (COMPARABLE); 2017T1→2017T2 +0.2 pp (COMPARABLE) · `RESULT-DC-ENOE-TABLA#serie_id=ENOE-DESALIENTO-DESISTIO-EDAD-45-59`
- `ENOE-DESALIENTO-DESISTIO-EDAD-60` — ENOE PISOS :: desaliento_desistio; unidad proporcion_0_1; olas 2005T1–2020T1 (k=21); acumulado +0.0 pp; pares fuera: 2017T1→2017T2 -0.0 pp (COMPARABLE); 2019T2→2019T3 +0.0 pp (COMPARABLE) · `RESULT-DC-ENOE-TABLA#serie_id=ENOE-DESALIENTO-DESISTIO-EDAD-60`
- `ENOE-DESALIENTO-DESISTIO-ENTIDAD-03` — ENOE PISOS :: desaliento_desistio; unidad proporcion_0_1; olas 2005T1–2020T1 (k=21); acumulado +0.1 pp; pares fuera: 2008T1→2012T1 +1.6 pp (COMPARABLE) · `RESULT-DC-ENOE-TABLA#serie_id=ENOE-DESALIENTO-DESISTIO-ENTIDAD-03`
- `ENOE-DESALIENTO-DESISTIO-ENTIDAD-04` — ENOE PISOS :: desaliento_desistio; unidad proporcion_0_1; olas 2005T1–2020T1 (k=21); acumulado +0.1 pp; pares fuera: 2019T1→2019T2 +0.7 pp (COMPARABLE) · `RESULT-DC-ENOE-TABLA#serie_id=ENOE-DESALIENTO-DESISTIO-ENTIDAD-04`
- `ENOE-DESALIENTO-DESISTIO-ENTIDAD-06` — ENOE PISOS :: desaliento_desistio; unidad proporcion_0_1; olas 2008T1–2020T1 (k=20); acumulado +0.1 pp; pares fuera: 2008T1→2012T1 +0.9 pp (COMPARABLE) · `RESULT-DC-ENOE-TABLA#serie_id=ENOE-DESALIENTO-DESISTIO-ENTIDAD-06`
- `ENOE-DESALIENTO-DESISTIO-ENTIDAD-12` — ENOE PISOS :: desaliento_desistio; unidad proporcion_0_1; olas 2020T3–2022T4 (k=10); acumulado -0.5 pp; pares fuera: 2020T4→2021T1 -0.5 pp (COMPARABLE) · `RESULT-DC-ENOE-TABLA#serie_id=ENOE-DESALIENTO-DESISTIO-ENTIDAD-12`
- `ENOE-DESALIENTO-DESISTIO-ENTIDAD-18` — ENOE PISOS :: desaliento_desistio; unidad proporcion_0_1; olas 2005T1–2020T1 (k=21); acumulado -0.0 pp; pares fuera: 2014T1→2016T1 -0.7 pp (COMPARABLE) · `RESULT-DC-ENOE-TABLA#serie_id=ENOE-DESALIENTO-DESISTIO-ENTIDAD-18`
- `ENOE-DESALIENTO-DESISTIO-ENTIDAD-20` — ENOE PISOS :: desaliento_desistio; unidad proporcion_0_1; olas 2012T1–2020T1 (k=19); acumulado -0.3 pp; pares fuera: 2018T1→2018T2 -0.3 pp (COMPARABLE) · `RESULT-DC-ENOE-TABLA#serie_id=ENOE-DESALIENTO-DESISTIO-ENTIDAD-20`
- `ENOE-DESALIENTO-DESISTIO-ENTIDAD-21` — ENOE PISOS :: desaliento_desistio; unidad proporcion_0_1; olas 2023T1–2025T2 (k=10); acumulado -0.0 pp; pares fuera: 2024T2→2024T3 -0.2 pp (COMPARABLE) · `RESULT-DC-ENOE-TABLA#serie_id=ENOE-DESALIENTO-DESISTIO-ENTIDAD-21`
- `ENOE-DESALIENTO-DESISTIO-ENTIDAD-22` — ENOE PISOS :: desaliento_desistio; unidad proporcion_0_1; olas 2020T3–2021T4 (k=6); acumulado -0.2 pp; pares fuera: 2021T1→2021T2 +0.8 pp (COMPARABLE) · `RESULT-DC-ENOE-TABLA#serie_id=ENOE-DESALIENTO-DESISTIO-ENTIDAD-22`
- `ENOE-DESALIENTO-DESISTIO-ENTIDAD-25` — ENOE PISOS :: desaliento_desistio; unidad proporcion_0_1; olas 2014T1–2020T1 (k=18); acumulado -0.2 pp; pares fuera: 2019T3→2019T4 -0.2 pp (COMPARABLE); 2019T4→2020T1 +0.3 pp (COMPARABLE, toca 2020) · `RESULT-DC-ENOE-TABLA#serie_id=ENOE-DESALIENTO-DESISTIO-ENTIDAD-25`
- `ENOE-DESALIENTO-DESISTIO-ENTIDAD-27` — ENOE PISOS :: desaliento_desistio; unidad proporcion_0_1; olas 2008T1–2020T1 (k=20); acumulado +0.4 pp; pares fuera: 2008T1→2012T1 -0.4 pp (COMPARABLE) · `RESULT-DC-ENOE-TABLA#serie_id=ENOE-DESALIENTO-DESISTIO-ENTIDAD-27`
- `ENOE-DESALIENTO-DESISTIO-ENTIDAD-30` — ENOE PISOS :: desaliento_desistio; unidad proporcion_0_1; olas 2023T1–2025T4 (k=12); acumulado +0.2 pp; pares fuera: 2023T3→2023T4 -0.2 pp (COMPARABLE); 2024T4→2025T1 +0.4 pp (COMPARABLE) · `RESULT-DC-ENOE-TABLA#serie_id=ENOE-DESALIENTO-DESISTIO-ENTIDAD-30`
- `ENOE-DESALIENTO-DESISTIO-ENTIDAD-32` — ENOE PISOS :: desaliento_desistio; unidad proporcion_0_1; olas 2005T1–2020T1 (k=21); acumulado +0.1 pp; pares fuera: 2008T1→2012T1 +1.1 pp (COMPARABLE) · `RESULT-DC-ENOE-TABLA#serie_id=ENOE-DESALIENTO-DESISTIO-ENTIDAD-32`
- `ENOE-DESALIENTO-DESISTIO-LOCALIDAD-15K-99K` — ENOE PISOS :: desaliento_desistio; unidad proporcion_0_1; olas 2005T1–2020T1 (k=21); acumulado -0.0 pp; pares fuera: 2008T1→2012T1 +0.2 pp (COMPARABLE); 2017T2→2017T3 -0.2 pp (COMPARABLE) · `RESULT-DC-ENOE-TABLA#serie_id=ENOE-DESALIENTO-DESISTIO-LOCALIDAD-15K-99K`
- `ENOE-DESALIENTO-DESISTIO-LOCALIDAD-2K5-15K` — ENOE PISOS :: desaliento_desistio; unidad proporcion_0_1; olas 2005T1–2020T1 (k=21); acumulado -0.1 pp; pares fuera: 2012T1→2014T1 -0.1 pp (COMPARABLE) · `RESULT-DC-ENOE-TABLA#serie_id=ENOE-DESALIENTO-DESISTIO-LOCALIDAD-2K5-15K`
- `ENOE-DESALIENTO-DESISTIO-LOCALIDAD-MENOS-2K5` — ENOE PISOS :: desaliento_desistio; unidad proporcion_0_1; olas 2005T1–2020T1 (k=21); acumulado +0.1 pp; pares fuera: 2008T1→2012T1 +0.1 pp (COMPARABLE) · `RESULT-DC-ENOE-TABLA#serie_id=ENOE-DESALIENTO-DESISTIO-LOCALIDAD-MENOS-2K5`
- `ENOE-DESALIENTO-DESISTIO-SEXO-MUJER` — ENOE PISOS :: desaliento_desistio; unidad proporcion_0_1; olas 2005T1–2020T1 (k=21); acumulado -0.0 pp; pares fuera: 2008T1→2012T1 +0.1 pp (COMPARABLE); 2017T2→2017T3 -0.1 pp (COMPARABLE) · `RESULT-DC-ENOE-TABLA#serie_id=ENOE-DESALIENTO-DESISTIO-SEXO-MUJER`
- `ENOE-DESALIENTO-SIN-POSIBILIDADES-LOCALIDAD-100K` — ENOE PISOS :: desaliento_sin_posibilidades; unidad proporcion_0_1; olas 2005T1–2020T1 (k=21); acumulado +2.6 pp; pares fuera: 2005T1→2008T1 +3.0 pp (COMPARABLE) · `RESULT-DC-ENOE-TABLA#serie_id=ENOE-DESALIENTO-SIN-POSIBILIDADES-LOCALIDAD-100K`
- `ENOE-DESALIENTO-SIN-POSIBILIDADES-NACIONAL-NAC` — ENOE PISOS :: desaliento_sin_posibilidades; unidad proporcion_0_1; olas 2005T1–2020T1 (k=21); acumulado +1.3 pp; pares fuera: 2005T1→2008T1 +2.6 pp (COMPARABLE) · `RESULT-DC-ENOE-TABLA#serie_id=ENOE-DESALIENTO-SIN-POSIBILIDADES-NACIONAL-NAC`
- `ENOE-DESALIENTO-SIN-POSIBILIDADES-SEXO-HOMBRE` — ENOE PISOS :: desaliento_sin_posibilidades; unidad proporcion_0_1; olas 2005T1–2020T1 (k=21); acumulado +0.3 pp; pares fuera: 2005T1→2008T1 +3.4 pp (COMPARABLE) · `RESULT-DC-ENOE-TABLA#serie_id=ENOE-DESALIENTO-SIN-POSIBILIDADES-SEXO-HOMBRE`
- `ENOE-DESALIENTO-SIN-POSIBILIDADES-SEXO-MUJER` — ENOE PISOS :: desaliento_sin_posibilidades; unidad proporcion_0_1; olas 2005T1–2020T1 (k=21); acumulado +1.3 pp; pares fuera: 2005T1→2008T1 +2.3 pp (COMPARABLE) · `RESULT-DC-ENOE-TABLA#serie_id=ENOE-DESALIENTO-SIN-POSIBILIDADES-SEXO-MUJER`
- `ENOE-DESOCUPACION-EDAD-15-29` — ENOE PISOS :: desocupacion; unidad proporcion_0_1; olas 2005T1–2020T1 (k=21); acumulado -0.5 pp; pares fuera: 2008T1→2012T1 +1.8 pp (COMPARABLE) · `RESULT-DC-ENOE-TABLA#serie_id=ENOE-DESOCUPACION-EDAD-15-29`
- `ENOE-DESOCUPACION-EDAD-30-44` — ENOE PISOS :: desocupacion; unidad proporcion_0_1; olas 2005T1–2020T1 (k=21); acumulado +0.3 pp; pares fuera: 2008T1→2012T1 +0.9 pp (COMPARABLE) · `RESULT-DC-ENOE-TABLA#serie_id=ENOE-DESOCUPACION-EDAD-30-44`
- `ENOE-DESOCUPACION-ESCOLARIDAD-PRIM-INCOMPLETA` — ENOE PISOS :: desocupacion; unidad proporcion_0_1; olas 2005T1–2020T1 (k=21); acumulado -0.7 pp; pares fuera: 2008T1→2012T1 +1.1 pp (COMPARABLE) · `RESULT-DC-ENOE-TABLA#serie_id=ENOE-DESOCUPACION-ESCOLARIDAD-PRIM-INCOMPLETA`
- `ENOE-DESOCUPACION-LOCALIDAD-100K` — ENOE PISOS :: desocupacion; unidad proporcion_0_1; olas 2005T1–2020T1 (k=21); acumulado -0.5 pp; pares fuera: 2008T1→2012T1 +1.3 pp (COMPARABLE); 2014T1→2016T1 -1.2 pp (COMPARABLE) · `RESULT-DC-ENOE-TABLA#serie_id=ENOE-DESOCUPACION-LOCALIDAD-100K`
- `ENOE-DESOCUPACION-LOCALIDAD-2K5-15K` — ENOE PISOS :: desocupacion; unidad proporcion_0_1; olas 2005T1–2020T1 (k=21); acumulado -0.4 pp; pares fuera: 2017T4→2018T1 -0.8 pp (COMPARABLE) · `RESULT-DC-ENOE-TABLA#serie_id=ENOE-DESOCUPACION-LOCALIDAD-2K5-15K`
- `ENOE-DESOCUPACION-LOCALIDAD-MENOS-2K5` — ENOE PISOS :: desocupacion; unidad proporcion_0_1; olas 2005T1–2020T1 (k=21); acumulado +0.1 pp; pares fuera: 2008T1→2012T1 +1.0 pp (COMPARABLE) · `RESULT-DC-ENOE-TABLA#serie_id=ENOE-DESOCUPACION-LOCALIDAD-MENOS-2K5`
- `ENOE-DESOCUPACION-NACIONAL-NAC` — ENOE PISOS :: desocupacion; unidad proporcion_0_1; olas 2005T1–2020T1 (k=21); acumulado -0.4 pp; pares fuera: 2008T1→2012T1 +1.0 pp (COMPARABLE); 2014T1→2016T1 -0.8 pp (COMPARABLE) · `RESULT-DC-ENOE-TABLA#serie_id=ENOE-DESOCUPACION-NACIONAL-NAC`
- `ENOE-DESOCUPACION-SEXO-HOMBRE` — ENOE PISOS :: desocupacion; unidad proporcion_0_1; olas 2005T1–2020T1 (k=21); acumulado -0.1 pp; pares fuera: 2008T1→2012T1 +1.3 pp (COMPARABLE) · `RESULT-DC-ENOE-TABLA#serie_id=ENOE-DESOCUPACION-SEXO-HOMBRE`
- `ENOE-DESOCUPACION-SEXO-MUJER` — ENOE PISOS :: desocupacion; unidad proporcion_0_1; olas 2005T1–2020T1 (k=21); acumulado -0.9 pp; pares fuera: 2014T1→2016T1 -0.9 pp (COMPARABLE) · `RESULT-DC-ENOE-TABLA#serie_id=ENOE-DESOCUPACION-SEXO-MUJER`
- `ENOE-NO-PARTICIPACION-OBLIGACIONES-EDAD-60` — ENOE PISOS :: no_participacion_obligaciones; unidad proporcion_0_1; olas 2005T1–2020T1 (k=21); acumulado +10.8 pp; pares fuera: 2012T1→2014T1 +6.0 pp (COMPARABLE) · `RESULT-DC-ENOE-TABLA#serie_id=ENOE-NO-PARTICIPACION-OBLIGACIONES-EDAD-60`
- `ENOE-PLURIEMPLEO-LOCALIDAD-MENOS-2K5` — ENOE PISOS :: pluriempleo; unidad proporcion_0_1; olas 2005T1–2020T1 (k=21); acumulado -3.0 pp; pares fuera: 2005T1→2008T1 -3.1 pp (COMPARABLE) · `RESULT-DC-ENOE-TABLA#serie_id=ENOE-PLURIEMPLEO-LOCALIDAD-MENOS-2K5`
- `ENOE-SUBOCUPACION-EDAD-15-29` — ENOE PISOS :: subocupacion; unidad proporcion_0_1; olas 2005T1–2020T1 (k=21); acumulado -1.2 pp; pares fuera: 2005T1→2008T1 -2.3 pp (COMPARABLE) · `RESULT-DC-ENOE-TABLA#serie_id=ENOE-SUBOCUPACION-EDAD-15-29`
- `ENOE-SUBOCUPACION-EDAD-30-44` — ENOE PISOS :: subocupacion; unidad proporcion_0_1; olas 2005T1–2020T1 (k=21); acumulado -0.5 pp; pares fuera: 2005T1→2008T1 -2.3 pp (COMPARABLE); 2008T1→2012T1 +1.9 pp (COMPARABLE) · `RESULT-DC-ENOE-TABLA#serie_id=ENOE-SUBOCUPACION-EDAD-30-44`
- `ENOE-SUBOCUPACION-EDAD-45-59` — ENOE PISOS :: subocupacion; unidad proporcion_0_1; olas 2005T1–2020T1 (k=21); acumulado -0.5 pp; pares fuera: 2005T1→2008T1 -2.1 pp (COMPARABLE) · `RESULT-DC-ENOE-TABLA#serie_id=ENOE-SUBOCUPACION-EDAD-45-59`
- `ENOE-SUBOCUPACION-EDAD-60` — ENOE PISOS :: subocupacion; unidad proporcion_0_1; olas 2005T1–2020T1 (k=21); acumulado +0.9 pp; pares fuera: 2005T1→2008T1 -2.3 pp (COMPARABLE); 2008T1→2012T1 +3.1 pp (COMPARABLE) · `RESULT-DC-ENOE-TABLA#serie_id=ENOE-SUBOCUPACION-EDAD-60`
- `ENOE-SUBOCUPACION-ENTIDAD-03` — ENOE PISOS :: subocupacion; unidad proporcion_0_1; olas 2005T1–2020T1 (k=21); acumulado +8.4 pp; pares fuera: 2008T1→2012T1 +11.8 pp (COMPARABLE) · `RESULT-DC-ENOE-TABLA#serie_id=ENOE-SUBOCUPACION-ENTIDAD-03`
- `ENOE-SUBOCUPACION-ENTIDAD-04` — ENOE PISOS :: subocupacion; unidad proporcion_0_1; olas 2005T1–2020T1 (k=21); acumulado +2.0 pp; pares fuera: 2019T1→2019T2 +10.5 pp (COMPARABLE) · `RESULT-DC-ENOE-TABLA#serie_id=ENOE-SUBOCUPACION-ENTIDAD-04`
- `ENOE-SUBOCUPACION-ENTIDAD-08` — ENOE PISOS :: subocupacion; unidad proporcion_0_1; olas 2005T1–2020T1 (k=21); acumulado -1.0 pp; pares fuera: 2005T1→2008T1 -3.9 pp (COMPARABLE) · `RESULT-DC-ENOE-TABLA#serie_id=ENOE-SUBOCUPACION-ENTIDAD-08`
- `ENOE-SUBOCUPACION-ENTIDAD-17` — ENOE PISOS :: subocupacion; unidad proporcion_0_1; olas 2005T1–2020T1 (k=21); acumulado -9.9 pp; pares fuera: 2005T1→2008T1 -9.6 pp (COMPARABLE) · `RESULT-DC-ENOE-TABLA#serie_id=ENOE-SUBOCUPACION-ENTIDAD-17`
- `ENOE-SUBOCUPACION-ENTIDAD-25` — ENOE PISOS :: subocupacion; unidad proporcion_0_1; olas 2005T1–2020T1 (k=21); acumulado -10.7 pp; pares fuera: 2005T1→2008T1 -11.3 pp (COMPARABLE) · `RESULT-DC-ENOE-TABLA#serie_id=ENOE-SUBOCUPACION-ENTIDAD-25`
- `ENOE-SUBOCUPACION-ENTIDAD-26` — ENOE PISOS :: subocupacion; unidad proporcion_0_1; olas 2005T1–2020T1 (k=21); acumulado +0.9 pp; pares fuera: 2008T1→2012T1 +7.2 pp (COMPARABLE) · `RESULT-DC-ENOE-TABLA#serie_id=ENOE-SUBOCUPACION-ENTIDAD-26`
- `ENOE-SUBOCUPACION-ESCOLARIDAD-MEDIA-SUPERIOR` — ENOE PISOS :: subocupacion; unidad proporcion_0_1; olas 2005T1–2020T1 (k=21); acumulado -0.2 pp; pares fuera: 2005T1→2008T1 -2.1 pp (COMPARABLE) · `RESULT-DC-ENOE-TABLA#serie_id=ENOE-SUBOCUPACION-ESCOLARIDAD-MEDIA-SUPERIOR`
- `ENOE-SUBOCUPACION-ESCOLARIDAD-PRIM-COMPLETA` — ENOE PISOS :: subocupacion; unidad proporcion_0_1; olas 2005T1–2020T1 (k=21); acumulado +0.3 pp; pares fuera: 2008T1→2012T1 +2.6 pp (COMPARABLE) · `RESULT-DC-ENOE-TABLA#serie_id=ENOE-SUBOCUPACION-ESCOLARIDAD-PRIM-COMPLETA`
- `ENOE-SUBOCUPACION-ESCOLARIDAD-PRIM-INCOMPLETA` — ENOE PISOS :: subocupacion; unidad proporcion_0_1; olas 2005T1–2020T1 (k=21); acumulado +0.2 pp; pares fuera: 2005T1→2008T1 -3.1 pp (COMPARABLE); 2008T1→2012T1 +3.4 pp (COMPARABLE) · `RESULT-DC-ENOE-TABLA#serie_id=ENOE-SUBOCUPACION-ESCOLARIDAD-PRIM-INCOMPLETA`
- `ENOE-SUBOCUPACION-LOCALIDAD-100K` — ENOE PISOS :: subocupacion; unidad proporcion_0_1; olas 2005T1–2020T1 (k=21); acumulado -0.2 pp; pares fuera: 2005T1→2008T1 -1.8 pp (COMPARABLE); 2008T1→2012T1 +1.7 pp (COMPARABLE) · `RESULT-DC-ENOE-TABLA#serie_id=ENOE-SUBOCUPACION-LOCALIDAD-100K`
- `ENOE-SUBOCUPACION-LOCALIDAD-2K5-15K` — ENOE PISOS :: subocupacion; unidad proporcion_0_1; olas 2005T1–2020T1 (k=21); acumulado -1.4 pp; pares fuera: 2005T1→2008T1 -2.6 pp (COMPARABLE) · `RESULT-DC-ENOE-TABLA#serie_id=ENOE-SUBOCUPACION-LOCALIDAD-2K5-15K`
- `ENOE-SUBOCUPACION-NACIONAL-NAC` — ENOE PISOS :: subocupacion; unidad proporcion_0_1; olas 2005T1–2020T1 (k=21); acumulado -0.5 pp; pares fuera: 2005T1→2008T1 -2.3 pp (COMPARABLE); 2008T1→2012T1 +1.9 pp (COMPARABLE) · `RESULT-DC-ENOE-TABLA#serie_id=ENOE-SUBOCUPACION-NACIONAL-NAC`
- `ENOE-SUBOCUPACION-SEXO-HOMBRE` — ENOE PISOS :: subocupacion; unidad proporcion_0_1; olas 2005T1–2020T1 (k=21); acumulado -1.4 pp; pares fuera: 2005T1→2008T1 -2.7 pp (COMPARABLE); 2008T1→2012T1 +2.2 pp (COMPARABLE) · `RESULT-DC-ENOE-TABLA#serie_id=ENOE-SUBOCUPACION-SEXO-HOMBRE`
- `ENOE-SUBOCUPACION-SEXO-MUJER` — ENOE PISOS :: subocupacion; unidad proporcion_0_1; olas 2005T1–2020T1 (k=21); acumulado +1.1 pp; pares fuera: 2005T1→2008T1 -1.4 pp (COMPARABLE); 2008T1→2012T1 +1.4 pp (COMPARABLE) · `RESULT-DC-ENOE-TABLA#serie_id=ENOE-SUBOCUPACION-SEXO-MUJER`

### tramite

29 series: 29 SIN-SERIE (conteo de filas de `tabla-dictamen-v1_0.tsv`, columna `result` → `RESULT-DC-<INST>-TABLA`).

## Por qué tantas series son SIN-SERIE

- MENOS-DE-3-OLAS-EN-EL-CORPUS: 7027 series (columna `causa_sin_serie` de la tabla; dictamen `RESULT-DC-<INST>-TABLA`).
- COMPARABILIDAD-NO-DOCUMENTADA-O-NO-COMPARABLE: 142 series (columna `causa_sin_serie` de la tabla; dictamen `RESULT-DC-<INST>-TABLA`).
- FUERA-DE-ESCALA-(0,1): 30 series (columna `causa_sin_serie` de la tabla; dictamen `RESULT-DC-<INST>-TABLA`).
- SIN-IC-O-VALOR-EN-FRONTERA: 1 series (columna `causa_sin_serie` de la tabla; dictamen `RESULT-DC-<INST>-TABLA`).

Por instrumento y causa: BANXICO MENOS-DE-3-OLAS-EN-EL-CORPUS 5 · EDER MENOS-DE-3-OLAS-EN-EL-CORPUS 3 · ENCUCI MENOS-DE-3-OLAS-EN-EL-CORPUS 4 · ENDIREH COMPARABILIDAD-NO-DOCUMENTADA-O-NO-COMPARABLE 141 · ENDIREH MENOS-DE-3-OLAS-EN-EL-CORPUS 6170 · ENFIH MENOS-DE-3-OLAS-EN-EL-CORPUS 2 · ENIF MENOS-DE-3-OLAS-EN-EL-CORPUS 659 · ENIGH FUERA-DE-ESCALA-(0,1) 2 · ENIGH MENOS-DE-3-OLAS-EN-EL-CORPUS 5 · ENIGH SIN-IC-O-VALOR-EN-FRONTERA 1 · ENNVIH MENOS-DE-3-OLAS-EN-EL-CORPUS 1 · ENSANUT MENOS-DE-3-OLAS-EN-EL-CORPUS 2 · ENUT FUERA-DE-ESCALA-(0,1) 28 · ENUT MENOS-DE-3-OLAS-EN-EL-CORPUS 16 · ENVIPE MENOS-DE-3-OLAS-EN-EL-CORPUS 31 · LAPOP COMPARABILIDAD-NO-DOCUMENTADA-O-NO-COMPARABLE 1 · MOCIBA MENOS-DE-3-OLAS-EN-EL-CORPUS 126 · MOTRAL MENOS-DE-3-OLAS-EN-EL-CORPUS 3 (misma columna, `RESULT-DC-<INST>-TABLA`).

La causa dominante es de corpus, no de dato: la mayoría de las celdas del catálogo (ENIF) y de los pisos (ENDIREH, MOCIBA) existen en una o dos olas. ENDIREH une series entre olas sólo por cadena idéntica de resultado, eje, categoría y ventana (sin mapeo semántico entre módulos que cambian de nombre), y no tiene tabla ni spec de comparabilidad por texto: donde sí hay tres olas, el par no se presume comparable (spec §2, A.15) y la serie se corta. MOCIBA 2016→2017 es NO-COMPARABLE por su propia spec (`RESULT-DC-MOCIBA-TABLA`). Ese hueco es el entregable: sin crosswalk de módulos y tabla de comparabilidad no hay serie que dictaminar.

## Módulo de auditoría de rigor extremo

- **¿Estructura o crisis —2020— y no cultura?** 3 de 89 series con par fuera lo tienen sólo en un par que toca 2020: `ENVIPE-NODENUNCIA-MIEDO-DESCONFIANZA-NACIONAL-TOTAL`, `ENIGH-REMINT-NACIONAL-PARTICIPACION_GE50_DE_REMESAS`, `ENOE-BUSCA-OTRO-TRABAJO-LOCALIDAD-2K5-15K` (`RESULT-DC-<INST>-TABLA`, campo `pares_fuera`, marca `2020=SI`). Son candidatas a estructura o crisis, no a cultura.
- **Los 8 CAMBIO-SOSTENIDO son todos ENOE y no se leen como cambio de conducta.** Acumulados entre -1.1 pp y -0.0 pp (`RESULT-DC-ENOE-<SERIE>-DELTA-PP`), con pares fuera en ambas direcciones: la regla sellada los cuenta porque el IC muestral de ENOE es estrecho y su τ² calculado aquí es pequeño (`RESULT-DC-ENOE-TAU2-*`); la spec de ENOE declara que no hay covarianza longitudinal estimable (`SIN-COVARIANZA-LONGITUDINAL`). No se reinterpreta la regla (PARO d); se declara aquí.
- **¿Pobreza, violencia o informalidad confundidas con cultura?** El dictamen no atribuye causa. Una caída de la no denuncia (ENVIPE) o del desaliento laboral (ENOE) es compatible con cambios de incidencia, de mercado laboral o de oferta institucional antes que de disposición.
- **¿Sobregeneralización desde clase media urbana?** ENCIG cubre ciudades de 100 mil o más (universo de los CALC-ENCIG-SERIE-CANAL-* que consume `RESULT-DC-ENCIG-TABLA`); sus dictámenes no hablan de lo rural.
- **¿Qué afirmación sobre el corpus fue escrita a mano?** Ninguna cifra de este documento: se regenera desde los RESULT sellados (`tests/test_donde_cambio_documento.py`).
- **¿Cuántos contadores movió este trabajo?** Nueve CALC sellados con `cuenta_gen2: SI`, `adopta: NO` (`CALC-<INST>-SERIE-DICTAMEN-0001`); ninguna adopción, ningún movimiento de `celdas_validadas`.
- **PROSPECTIVA/RETROSPECTIVA:** todo RETROSPECTIVA; ninguna frase mezcla columnas.
- **Unidad:** cada serie conserva la suya (columna `unidad`); ninguna suma cruza persona, hogar, delito o trámite.
- **Lo que sería peligroso leído simplista:** «ESTABLE» no es «no cambió nada»: es que el piso de la ola anterior cubre a la siguiente con el IC calibrado; un IC ancho vuelve ESTABLE casi cualquier serie.

## Sucesores

Informe v1.3 §«dónde cambió»; U4 (familias 2027) toma los CAMBIO-SOSTENIDO como candidatos a estimando prospectivo, con la reserva ENOE de arriba. Tablas de comparabilidad por texto para ENDIREH y las conductas ENIF sin tabla convertirían SIN-SERIE en series dictaminables.
