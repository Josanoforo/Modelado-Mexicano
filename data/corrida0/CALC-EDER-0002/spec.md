# `CALC-EDER-0002` — cara mecánica

Gobierna esta corrida la spec SELLADA
`forense/prereg-caja/EDER-CORRESIDENCIA-ACTUAL-DISENO-spec-v1_0.md`
(**`prereg-caja-EDER-CORRESIDENCIA-ACTUAL-DISENO`**, sha256 en el sidecar
`.sha256` y en `spec.yaml`). Este archivo no la sustituye: la resume en la
forma que `spec.yaml` cablea. Donde los dos digan cosas distintas, **manda la
sellada**.

**Acto:** `ACTO GEN2-LOTE-MEDICION-PENDIENTE-1` (pieza P1, `NC-0184`),
14/sep/2026, CAJA (Ubuntu/WSL2), sobre `7de3acb4`.
**Sucesor de:** `familia.corresidencia.adulto_familiar_actual`
(`MAESTRA33-C1`, `p = 0.057531`, `n = 9397`, `factor`, bootstrap simple),
sellada sin carga en `milpa/tramite-ola5-propuesta-v0.yaml:192-210`. **No
releva ninguna `CORR-*`**. Consumidor con cita GEN2 vigente: **ninguno**.
**Hermano de:** `CALC-EDER-0001` (mismo lector, misma varianza, otro estimando).

**CONGELADO en el COMMIT-1, antes de leer un solo valor del microdato.**

---

## Qué mide

Proporción ponderada (`factor`) de ego —respondientes EDER 2017 de 20-54 años
con `parentesco ∈ {Jefe, Cónyuge}` en vivienda con `tipo_adqui` no blanco—
que **hoy** co-residen con un ascendiente o un suegro, leído del roster
`persona.csv[parentesco]` de los demás integrantes del hogar (códigos 6/7,
invertidos si ego es cónyuge). `A-P` con IC de diseño (`est_dis × upm`);
`B-P` con `factor_per` como sensibilidad declarada, no adoptable.

## Guardias que paran

Miembro o columna ausente, `folioviv` no único en `vivienda.csv`, terna no
única en `persona.csv` → `NO-ESTIMABLE-*` en `A` y `B`; terna no única en
`antecedentes.csv` → sólo `B`. Universo vacío → `NO-ESTIMABLE-UNIVERSO-VACIO`.
El embudo de C1 (94 101 · 23 831 · 16 687 · 9 397) es guardia con valor
esperado: si discuerda se reporta (`A-EMBUDO-C1`), no se ajusta.

## Control positivo

`A-P` contra `0.057531` (`|Δ| ≤ 1e-6` → `REPRODUCE`); `A-N-U` contra 9 397.
Sólo el punto: el IC de C1 (bootstrap simple) no se compara (A-bis.3).
