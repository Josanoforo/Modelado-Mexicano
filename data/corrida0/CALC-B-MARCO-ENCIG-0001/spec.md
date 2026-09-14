# `CALC-B-MARCO-ENCIG-0001` — la línea base temporal `B` sobre la serie ENCIG de intento de apropiación de beneficio por un servidor público, para una celda del marco-M

Cara **local** de la spec sellada `forense/prereg-caja/B-MARCO-spec-v1_0.md`
(`prereg-caja-B-MARCO`). Manda la sellada. Congelado en el `COMMIT-1` de
`ACTO GEN2-B-MARCO`, antes de abrir microdato. Sucesora de familia de `CALC-B-0001`.

## 1 · Qué mide

Proporción ponderada de personas de 18 años y más que responden `1` (Sí) a `P8_3_1`
(«¿un servidor público o empleado del gobierno intentó apropiarse o le solicitó de
forma directa algún beneficio…?»), sobre {1,2}, ponderador `FAC_P18`, tabla
`sec1_…_8_9_10` — el estimando que `corridas-R/TRA-M-07.json` declara. Olas: 2019
(predecesora) y 2021 (objetivo, TRA-M-07). Selector `tools/baseline_temporal.py` sin
modificar, dos brazos (`OPERATIVO`: `Modified` de cada CSV; `PERSISTENCIA`:
`periodo_fin`), `fecha_corte(2021) = 2020-12-31`.

## 2 · Qué NO hace

No lee `R`, `M` ni `L`. No construye `B` para TRA-M-03 (ENCIG 2011 no trae la
pregunta a nivel persona: `NO-CONSTRUIBLE`, §1 de la sellada) ni para TRA-M-02
(ENCUCI, ola única). Ninguna cifra entra a un veredicto (`T9`).

## 3 · Guardias que PARAN · 4 · IC95 · 5 · Contaminación · 6 · Contador

Idénticos a la sellada §4, §0.2 y §7.7: `NO-ESTIMABLE-DISENO-INCOMPLETO` /
`NO-ESTIMABLE` / `NO-ESTIMABLE-P-DEGENERADA`; bootstrap de UPM dentro de `EST_DIS`,
2 000 réplicas, semilla `20260908`, `numpy.PCG64`, implementación verbatim de
`CALC-B-0001`; contaminación total declarada; `cuenta_gen2 = SI` por la FIRMA DE
MESA del 14/sep/2026 citada en el encargo archivado, objeto: este CALC-B.
