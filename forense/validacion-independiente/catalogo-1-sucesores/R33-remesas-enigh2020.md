# R33 · NO-PASA formal de remesas ENIGH 2020 y spec sucesora · expediente

`ACTO GEN2-C1-SUCESORES-Y-LOTE-3`, P2 · `FP-260928-GEN2-ASTRA-CONTINUIDAD-C1-1-26a2-05` · 28/sep/2026.

## Firma de mesa, verbatim

`forense/encargos/2026-09-28-GEN2-TRAMITE-FIRMAS-21-ADENDA-1.md`, R33 **(1)**: «Queda el NO-PASA formal de los dos RESULT de remesas ENIGH2020. Autorizo una spec sucesora con tolerancia absoluta 1e-10 para su próxima validación; la spec sellada no se edita.»

## 1 · NO-PASA formal: se conserva

Las dos filas de `data/corrida0/validaciones-independientes.tsv` (`CALC-ENIGH2020-INTENSIDAD-REMESAS-0001`) quedan como están:

| RESULT | Estado | Δ | Tolerancia que adjudicó |
|---|---|---|---|
| `RESULT-ENIGH20-REMINT-PARTICIPACION-AGREGADA` | NO-PASA | −4.44e−16 | `spec.yaml` L51, `abs: 0.0` |
| `RESULT-ENIGH20-REMINT-REMESAS-MEDIA` | NO-PASA | −1.82e−12 | ídem |

Evidencia de las dos: `catalogo-1-ejecucion-lote2/p3/dictamenes/enigh2020-intensidad-remesas-0001-v4--dictamen.json`, sha256 `2e331d04…41b7`.

## 2 · Spec sucesora (solo spec)

`forense/prereg-caja/ENIGH2020-INTENSIDAD-REMESAS-spec-v1_1.md`, con su `.sha256`. Premisa que cae: el CALC padre no tenía spec humana en `prereg-caja/`, sino `data/corrida0/CALC-ENIGH2020-INTENSIDAD-REMESAS-0001/spec.md` (sha256 `340f59bd…777f`), y la «L51» es del `spec.yaml` (sha256 `65ae9bdb…6d2a`). La sucesora es entonces la primera spec de este CALC en `prereg-caja/`, y cita a los dos padres por sha.

Único cambio: flotantes y proporciones, abs 1e−10 rel 0. Enteros y textos siguen exactos. Todo lo demás es verbatim del padre. El sucesor será `CALC-ENIGH2020-INTENSIDAD-REMESAS-0002`, con `repite_de` en la raíz del `spec.yaml`.

## Lo que no hace

No edita la spec sellada. No escribe el `spec.yaml` sucesor ni corre el CALC: los dos son de `GEN2-RELEVO-TRAMITE-CAJA-2`, que hoy no existe como encargo en `forense/encargos/` (0 archivos). No cambia los dos NO-PASA.
