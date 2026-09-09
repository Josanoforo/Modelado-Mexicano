# `CALC-ENVIPE-0001` — cara mecánica

Gobierna esta corrida la spec SELLADA `forense/prereg-caja/ENVIPE-DENUNCIA-spec-v1_0.md`
(**`prereg-caja-ENVIPE-DENUNCIA`**, `sha256 e404e7b5faeb54af6ce3a49b02f1adc4c25fcd9b82c82d79956f68c370bd49b5`).
Este archivo no la sustituye: la resume en la forma que `spec.yaml` cablea.
Donde los dos digan cosas distintas, manda la sellada.

**Acto:** `ACTO GEN2-LOTE-ENVIPE-1`, 9/sep/2026, CAJA (Ubuntu), sobre `6e0381b`.
**Releva:** `CORR-0009` → `RES-0027` (`denuncia_con_miedo_o_desconfianza`) y,
en el sentido acotado de §6.2 de la sellada, `RES-0028`
(`denuncia_por_otra_razon`). Consumidor:
`milpa/tramite.yaml:civico.denuncia.miedo_desconfianza`.

**CONGELADO en el COMMIT-1, antes de abrir un solo `conjunto_de_datos/*.csv`.**

---

## Qué mide

La proporción ponderada de **delitos personales no denunciados** cuya **razón
principal** declarada (`BP1_23`, ENVIPE 2025, delitos de 2024) es miedo o
desconfianza.

## Unidad de observación — declarada, porque cambia el denominador

| universo | unidad | filtro | ponderador |
|---|---|---|---|
| **`U1` (PRIMARIO)** | **delito** (`ID_DEL`, tabla `tmod_vic`) | `BPCOD ∈ {05..15}` · `BP1_20 = 2` · `BP1_23 ∈ {01..08}` | `FAC_DEL` |
| `U3` | delito | idem, con `BP1_23 ∈ {01..09, 99}` | `FAC_DEL` |
| `U4` | **persona** (`ID_PER`, tabla `tper_vic2`) | persona con ≥1 delito en `U1`; colapso GEN1 (`máx`) | `FAC_ELE` |

`U2` de la sellada no se emite como estimación propia: sus dos piezas
(`N-BP1-23-09` y `P-OTRA-U3`) lo determinan sin ambigüedad.

## Codificación — dos, la primaria NO es la de GEN1

| | `= 1` | `= 0` |
|---|---|---|
| **`C1` (PRIMARIA)** — sólo los códigos cuyo texto literal dice «miedo» o «desconfianza» | `01`, `02`, `06` | `03`, `04`, `05`, `07`, `08` |
| `C2` (secundaria declarada) — partición GEN1, añade «actitud hostil de la autoridad» | `01`, `02`, `06`, `08` | `03`, `04`, `05`, `07` |

**Escala:** proporción en `[0,1]`; **más alto = más peso del miedo/desconfianza
como razón principal**. Nunca porcentaje, nunca puntos porcentuales.

## Incertidumbre de diseño

`EST_DIS` (001–607) y `UPM_DIS` están declarados en el descriptor de ambas
tablas: la varianza de diseño **sí** es identificable aquí (a diferencia de lo
que `FP-201` declaró para la corrida GEN1). Bootstrap de `UPM_DIS` con
reemplazo dentro de `EST_DIS`, 2000 réplicas, `numpy.PCG64`, semilla
`20260909`, percentiles 2.5/97.5. Un estrato con **una sola UPM** se
re-muestrea a sí mismo (varianza cero), se cuenta, y si hay alguno el
`METODO-IC` sale `IC-CON-ESTRATOS-DE-UPM-UNICA` — el IC se lee como **límite
inferior de la anchura verdadera**, no como IC exacto.

## Guardias que PARAN (no arreglan)

`NO-ESTIMABLE-COLUMNA-AUSENTE:<col>` · `NO-ESTIMABLE-COLUMNA-VACIA:<col>` ·
`NO-ESTIMABLE-UNIVERSO-VACIO` · `NO-ESTIMABLE-DISENO-INCOMPLETO`.
Los `BP1_23` en blanco pese a `BP1_20 = 2` **no se imputan a cero**: se cuentan
aparte y quedan fuera de todo universo.

## Control positivo externo

`P-C2-U4` (única celda que comparte codificación **y** unidad con GEN1) contra
`0.294313`, con tres ramas pre-declaradas (§6.1 de la sellada). `NO-REPRODUCE`
**no** invalida la corrida ni autoriza tocar el medidor.

## Lo que NO hace

No mide `RES-0039..0042` (otra apertura: `BPCOD=01`, condicional a seguro) · no
transfiere a 2012–2024 · no calibra contra las seis celdas ENVIPE del marco `M`
· no toca `milpa/tramite.yaml` ni ningún sello previo · ningún `RESULT` se
rotula causal.

> **El primer resultado que produzca este procedimiento es el que se reporta.**
