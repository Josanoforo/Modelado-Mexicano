# `CALC-ENIGH-0001` — cara mecánica

Gobierna esta corrida la spec SELLADA `forense/prereg-caja/ENIGH-REMESAS-R51-spec-v1_0.md`
(**`prereg-caja-ENIGH-REMESAS-R51`**, `sha256 e58b3901cc49e25500b01df19752ba57e46e862b925141d7a9714a22fc9a59e0`).
Este archivo no la sustituye: la resume en la forma que `spec.yaml` cablea.
Donde los dos digan cosas distintas, **manda la sellada**.

**Acto:** `ACTO GEN2-SPECS-DEMANDA-1`, 15/sep/2026, **NUBE**, sobre `f5a5227`.
**Releva:** `CORR-0011` (ENIGH2022) → **2** `RESULT`: `RES-0035`, `RES-0036`.
Consumidor: `milpa/tramite.yaml:familia.seguro.volatilidad_ausencia_estado` (`R5.1`).

**CONGELADO en el COMMIT-1, en NUBE, antes de abrir un solo byte de microdato.**

---

## Qué mide

Un payload (`enigh2022_nc_csv`, `sha256 3b2b0bc9…`), un miembro
(`conjunto_de_datos_concentradohogar_enigh2022_ns/conjunto_de_datos/…_ns.csv`),
universo **hogares** (`folioviv+foliohog`), referencia **2022**:

| familia | unidad | desenlace | ponderador |
|---|---|---|---|
| **A** · recibe remesas | **HOGAR** | `remesas > 0` | `factor` |

## Por qué no es un duplicado de `CALC-B-0001`

`CALC-B-0001` ya midió esta misma cantidad sobre este mismo payload
(`RESULT-B-ENIGH-2022-P = 0.04569409956405095`, sello válido) y **su propia
spec sellada le prohíbe alimentar un veredicto** (`T9`, firma de mesa):
`tipo: ENSAYO-LINEA-BASE-TEMPORAL-B`, `reglas_bajo_prueba: NINGUNA`. El
bloqueo de `CORR-0011` **no es de medición: es de autorización**. Esta spec
abre la corrida que `T9` dejó vacante — la celda de la regla — y añade lo que
el ensayo no tiene: el **complemento contado**, la vía de adopción, y una
**reejecución** del punto (`A-REPLICA-B0001`, vocabulario `REPLICA-RESULTADO`,
nunca `REPRODUCE`: `E.3`).

## Diseño

Bootstrap de `upm` con reemplazo **dentro de** `est_dis`, 2 000 réplicas,
`numpy.PCG64`, semilla `20260915`, percentiles 2.5/97.5. `est_dis`/`upm` como
**llaves de texto opacas**. Estratos de UPM única → `IC-CON-ESTRATOS-DE-UPM-UNICA`
y el IC se lee como **límite inferior**. La semilla y las réplicas **difieren**
de las del ensayo `B` (42 / 10 000): por eso la réplica se juega **sobre el
punto**, nunca sobre los extremos del IC.

## Lo que NO hace

No abre microdato · **no escribe el medidor** (lo escribe el acto de CAJA) ·
no mide 2012/2014/2016/2018/2020 · no promedia olas ni toca `serie_olas` ·
no levanta `T9` ni reinterpreta la spec sellada de `CALC-B-0001` · no adopta
nada a `milpa/`.
