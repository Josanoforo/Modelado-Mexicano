# `CALC-EDER-0001` — cara mecánica

Gobierna esta corrida la spec SELLADA
`forense/prereg-caja/EDER-CORRESIDENCIA-DISENO-spec-v1_0.md`
(**`prereg-caja-EDER-CORRESIDENCIA-DISENO`**,
`sha256 b6c755447c0ad33b40e44efe44c593725539a2dd51a4727a498dd82d91eb5a41`).
Este archivo no la sustituye: la resume en la forma que `spec.yaml` cablea.
Donde los dos digan cosas distintas, **manda la sellada**.

**Acto:** `ACTO GEN2-DISENO-FASE1-CIERRE`, 14/sep/2026, CAJA (Ubuntu/WSL2),
sobre `4fedf1cf`.
**Sucesor de:** la tasa de fase 1 `familia.corresidencia.adulto_familiar`
(`FP-201`, `p = 0.996086`, `n = 14887`, `factor`, bootstrap simple), sellada
sin carga en `milpa/tramite-ola5-propuesta-v0.yaml:110-129`. **No releva
ninguna `CORR-*`**: la tasa nunca entró al motor. Consumidor con cita GEN2
vigente: **ninguno** — queda listado para adopción de mesa.

**CONGELADO en el COMMIT-1, antes de leer un solo valor del microdato.**
Lo único abierto al congelar: manifiesto, `eder2017_fd.pdf`,
`eder2017_descripcion_calculoR.pdf`, la lista de miembros del ZIP, la primera
línea (cabecera) de los cinco `.csv`, el conteo de líneas de `vivienda.csv` y
`antecedentes.csv`, `data/diseno-muestral.yaml`, el inventario, la propuesta
`tramite-ola5-propuesta-v0.yaml`, `tools/tasas_base_fase1.py` y
`demanda-*.tsv`.

---

## Qué mide

Proporción ponderada de personas de 20-54 años (respondientes de EDER 2017,
con fila en `historiavida.csv`) cuya vivienda tiene `tipo_adqui` no blanco y
que **en alguna fila de su panel retrospectivo** declaran co-residir con
padre, madre, hermanos, suegro o suegra (`padre_cor ∨ madre_cor ∨ hnos_cor ∨
suegro_cor ∨ suegra_cor = '1'`) — **la tasa de fase 1, sin cambios** — ahora
con **varianza de diseño** (`est_dis` × `upm`).

## Unidad de observación — declarada, porque cambia el denominador

| universo | unidad | tablas | filtro | ponderador |
|---|---|---|---|---|
| **`U_A` (sucesor)** | persona | `historiavida` ⨝ `vivienda` por `folioviv` | `tipo_adqui` no blanco · `factor` finito > 0 | `factor` (vivienda, ENH) |
| `U_B` (sensibilidad) | persona | `U_A` ⨝ `antecedentes` por `(folioviv, foliohog, id_pobla)` | `factor_per` finito > 0 | `factor_per` (persona, EDER) |

## Codificación

`d = 1` si alguna de las cinco `*_cor` es exactamente la cadena `'1'` en
alguna fila de la persona; `0` en otro caso (codificación GEN1 verbatim). El
complemento se cuenta directamente, nunca como `1 − p`.

## Varianza

Primaria: bootstrap de `upm` con reemplazo dentro de `est_dis`, 2 000
réplicas, `seed 20260914`, PCG64; estrato con una sola UPM se re-muestrea a sí
mismo (`IC-CON-ESTRATOS-DE-UPM-UNICA`, límite inferior). Secundaria de cotejo:
Taylor con aproximación declarada de `lonely.psu="adjust"` — la receta R de
INEGI para EDER.

## Ramas pre-declaradas

- `A-DELTA-VS-GEN1 = A-P − 0.996086`; `A-REPRODUCE-GEN1` con `|δ| ≤ 1e-6`.
- `A-DELTA-N-VS-GEN1 = A-N-U − 14887`.
- `A-ADOPCION-P3`: `LISTADO-PARA-MESA-REPRODUCE` / `LISTADO-PARA-MESA-NO-REPRODUCE`
  / `NO-ADOPTABLE-NO-ESTIMABLE` — sin cita en `milpa/` desde este acto.
- `B-CLAUSULA-SE-MUEVE-SI`: `DENTRO-DEL-IC-FASE1` si `0.994794 ≤ B-P ≤ 0.997250`,
  si no `FUERA-DEL-IC-FASE1` — la lectura literal de la cláusula que la propuesta
  escribió; la consecuencia es de mesa.

**El primer resultado que produzca este procedimiento es el que se reporta.**
