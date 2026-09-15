# `CALC-ENFIH-0001` — cara mecánica

Gobierna esta corrida la spec SELLADA `forense/prereg-caja/ENFIH-AFORE-spec-v1_0.md`
(**`prereg-caja-ENFIH-AFORE`**, `sha256 5c5a4981bfeff29aaf98d7738e6d98dd88a1628cc9c0e356514aae880cc55c7e`).
Este archivo no la sustituye: la resume en la forma que `spec.yaml` cablea.
Donde los dos digan cosas distintas, **manda la sellada**.

**Acto:** `ACTO GEN2-SPECS-DEMANDA-1`, 15/sep/2026, **NUBE**, sobre `f5a5227`.
**Releva:** `CORR-0012` (ENFIH2019) → **2** `RESULT`: `RES-0037`, `RES-0038`.
Consumidor: `milpa/tramite.yaml:dinero.planeacion.formal_estable` (`R1.2`).

**CONGELADO en el COMMIT-1, en NUBE, antes de abrir un solo byte de microdato.**

---

## Qué mide

Un solo payload (`enfih2019_bd_csv_zip`, `sha256 be372533…`), una sola tabla
(`TCONCENTRADORA.csv`), universo **hogares** (llave `FOLIO+VIV_SEL+HOGAR`),
referencia **2019**:

| familia | unidad | archivo | desenlace | ponderador |
|---|---|---|---|---|
| **A** · tenencia de Afore | **HOGAR** | `TCONCENTRADORA.csv` | `C_AFORE` (0/1 crudo) | `FAC_HOG` **de ese archivo** |
| **B** · robustez de universo | hogar principal | `TCONCENTRADORA.csv` | `C_AFORE` \| `H_PPAL==1` | `FAC_HOG` |
| **C** · descriptivo NO sellado | hogar | `TCONCENTRADORA.csv` | `C_AFORE` por `CAT_POS` | `FAC_HOG` |

## Las tres decisiones que esta spec toma y GEN1 no

1. **El IC nace de diseño.** GEN1 selló `ic95` sin declarar un campo de
   diseño; `EDIS`/`UPM_DIS` están en `TCONCENTRADORA.csv` y esta corrida los
   usa. `A-DELTA-IC-VS-GEN1` mide cuánto cambia la anchura.
2. **`FAC_HOG` se fija por archivo, no por nombre.** La misma etiqueta existe
   en `THOGAR.csv`, que **no se abre**. `A.15(c)`.
3. **`CAT_POS` no es formalidad.** La condicional de `R1.2` no es construible
   en ENFIH (0 aciertos en 664 columnas); `CAT_POS` sale como descriptivo
   rotulado `C-*`, nunca como la condicional.

## Diseño

Bootstrap de `UPM_DIS` con reemplazo **dentro de** `EDIS`, 2 000 réplicas,
`numpy.PCG64`, semilla `20260915`, percentiles 2.5/97.5. `EDIS`/`UPM_DIS` como
**llaves de texto opacas**. Estratos de UPM única → `IC-CON-ESTRATOS-DE-UPM-UNICA`
y el IC se lee como **límite inferior**.

## Control positivo y adopción

`A-P` contra `0.538502` (GEN1) con `A-DELTA-VS-GEN1` **con signo**.
`NO-REPRODUCE` **no** autoriza tocar el medidor. `A-ADOPCION` sale
`LISTADO-PARA-MESA-*`; este acto **no escribe cita en `milpa/`**.

## Lo que NO hace

No abre microdato · **no escribe el medidor** (lo escribe el acto de CAJA a
partir de este contrato) · no mide formalidad laboral · no abre `THOGAR.csv` ·
no adopta nada · no toca ningún CALC sellado.
