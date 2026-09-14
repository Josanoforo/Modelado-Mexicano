# `CALC-B-MARCO-ENIGH-0001` — la línea base temporal `B` sobre remesas ENIGH, extendida hacia atrás (2014 → 2016) para una celda del marco-M

Cara **local** de la spec sellada `forense/prereg-caja/B-MARCO-spec-v1_0.md`
(`prereg-caja-B-MARCO`). Manda la sellada. Congelado en el `COMMIT-1` de
`ACTO GEN2-B-MARCO`, antes de abrir microdato. Es la extensión hacia atrás que
`prereg-caja-B-REMESAS` §0.1 dejó a un sucesor; **`CALC-B-0001` no se toca**.

## 1 · Qué mide

Proporción ponderada de hogares con `concentradohogar.remesas > 0`, universo
completo, ponderador de hogar (`factor_hog` en 2014, `factor` en 2016 — cambio de
nombre documentado por los diccionarios, no de existencia), olas 2014 (predecesora,
NCV) y 2016 (objetivo, FAM-M-05, NS). Selector `tools/baseline_temporal.py` sin
modificar, dos brazos, `fecha_corte(2016) = 2015-12-31`. Serie idéntica a la de
`CALC-B-0001` (`ENIGH-NS · concentradohogar.remesas`).

## 2 · Control positivo de familia

`RESULT-BM-ENIGH-2016-{P,IC-LO,IC-HI,N}` deben coincidir con
`RESULT-B-ENIGH-2016-{P,IC-LO,IC-HI,N}` de `CALC-B-0001`: misma ola, mismo payload,
misma lectura, mismo bootstrap, misma semilla. Se verifica con las ocho cifras a la
vista (sellada §6.3).

## 3 · Guardias · IC95 · Contaminación · Contador

Las de la sellada: rama NA inexistente (`N-FUERA-CODIGO > 0` → `NO-ESTIMABLE-NULOS-INESPERADOS`,
guardia §1.1 de B-REMESAS heredada), `NO-ESTIMABLE-DISENO-INCOMPLETO`, `NO-ESTIMABLE`,
`NO-ESTIMABLE-P-DEGENERADA`; bootstrap de UPM dentro de `est_dis`, 2 000 réplicas, semilla
`20260908`; contaminación total declarada; `cuenta_gen2 = SI` por la FIRMA DE MESA del
14/sep/2026 citada en el encargo archivado, objeto: este CALC-B. No lee `R`.
