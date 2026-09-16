# `CALC-ENVIPE-DENUNCIA-SEGURO-0001` — cara mecánica

Gobierna esta corrida la spec SELLADA `forense/prereg-caja/ENVIPE-DENUNCIA-SEGURO-spec-v1_0.md`
(**`prereg-caja-ENVIPE-DENUNCIA-SEGURO`**, `sha256 dc700571dd1770903e0b75dc7b68656d605aa9b84b3a561f2e31fcd305463463`).
Este archivo no la sustituye: la resume en la forma que `spec.yaml` cablea.
Donde los dos digan cosas distintas, **manda la sellada**.

**Acto:** `ACTO GEN2-FIRMAS-MESA-1`, 15/sep/2026, **NUBE**, rama `claude/epic-thompson-wbbmg7`.
**Autoridad:** firma de mesa «**Si a todas.**» (15/sep/2026), OBJETO 10 verbatim:
«*NC-0088 — apertura estrecha ENVIPE-DENUNCIA-SEGURO-v1_0 para RES-0039..0042. Spec aquí; corrida en caja.*»
**Releva:** `CORR-0007` (ENVIPE2025, `envipe2025_csv`) → **4** `RESULT`: `RES-0039`, `RES-0040`, `RES-0041`, `RES-0042`.
Consumidores: `milpa/tramite.yaml:civico.denuncia.con_seguro` y `:civico.denuncia.sin_seguro`.

**CONGELADO en el COMMIT-1, en NUBE, antes de abrir un solo byte de microdato.**

---

## Qué mide

Un solo payload (`envipe2025_csv`, `sha256 8a7a99fd…`), un solo miembro
(`tmod_vic_envipe2025/conjunto_de_datos/conjunto_de_datos_tmod_vic_envipe2025.csv`),
unidad **delito**, restringido a `BPCOD = 01` (robo total de vehículo), ola **2025**:

| familia | estrato | desenlace | ponderador | releva |
|---|---|---|---|---|
| **CON** · con cobertura | `BP2_1 = "1"` | `BP1_20 = "1"` denuncia | `FAC_DEL` | **`RES-0039`** |
| **CON** · complemento **contado** | `BP2_1 = "1"` | `BP1_20 = "2"` no denuncia | `FAC_DEL` | **`RES-0040`** |
| **SIN** · sin cobertura | `BP2_1 = "2"` | `BP1_20 = "1"` denuncia | `FAC_DEL` | **`RES-0041`** |
| **SIN** · complemento **contado** | `BP2_1 = "2"` | `BP1_20 = "2"` no denuncia | `FAC_DEL` | **`RES-0042`** |

## Las decisiones que esta spec toma

1. **Es la opción A, y sólo la A.** La propuesta ofrecía A (estrecha descriptiva)
   y B (redefinición de motor). Mesa firmó **A**. Esta spec no redefine población,
   unidad, tratamiento de cobertura, desenlace ni uso en el motor. Si A no resulta
   medible, la consecuencia es `NO-ESTIMABLE`, **nunca** una migración a B.
2. **`EST_DIS`/`UPM_DIS` verificados, no supuestos.** El encargo pidió comprobarlo:
   ambos existen con **ese nombre exacto** en el archivo de víctimas de 2025 según
   `data/inventario-reactivos-v1_2.tsv`. No hizo falta guardia de renombre. Pero
   conviven con `ESTRATO` y `UPM`, que **no** son lo mismo: se resuelven por nombre
   literal, `A.15(c)`.
3. **El ponderador se fija por nombre literal.** `FAC_DEL`, nunca `FAC_DEL_AM`,
   que existe en el mismo archivo.
4. **Los complementos se cuentan.** `CON-P-NO-DENUNCIA` y `SIN-P-NO-DENUNCIA`
   salen de contar `BP1_20 = "2"` dentro del mismo estrato. **Prohibido `1 − p`**:
   derivarlo haría que la suma-uno se cumpliera por construcción y el control
   no comprobaría nada.

## Diseño

Bootstrap de `UPM_DIS` con reemplazo **dentro de** `EST_DIS`, 2 000 réplicas,
`numpy.PCG64`, semilla `20260915`, percentiles 2.5/97.5; EE = sd de las réplicas.
`EST_DIS`/`UPM_DIS` como **llaves de texto opacas**. Estratos de UPM única →
`IC-CON-ESTRATOS-DE-UPM-UNICA` y el IC se lee como **límite inferior**.

## Control positivo y adopción

Los cuatro puntos contra `0.7909 / 0.2091 / 0.6720 / 0.3280` (legacy, ya leídos —
contaminación declarada) con `DELTA-VS-GEN1` **con signo**. `NO-REPRODUCE` **no**
autoriza tocar el medidor. `ADOPCION` sale `LISTADO-PARA-MESA-*`; este acto
**no escribe cita en `milpa/`**.

## Lo que NO hace

No abre microdato · **no escribe el medidor** (lo escribe el acto de CAJA a partir
de este contrato) · **no es causal** y ningún `RESULT` puede citarse como efecto del
seguro · **no extrapola fuera de `BPCOD = 01`** ni a otras olas · no abre el gemelo
`envipe2025/bd_envipe_2025_csv.zip` · no edita `tools/medidor_denuncia_seguro_envipe25.py`
(antecedente técnico, **no** el script de esta spec) · no adopta nada · no toca
ningún CALC ni prereg sellado.
