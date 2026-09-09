# `CALC-ENCIG-0001` — cara mecánica

Gobierna esta corrida la spec SELLADA `forense/prereg-caja/ENCIG-MORDIDA-spec-v1_0.md`
(**`prereg-caja-ENCIG-MORDIDA`**, `sha256 00c7c4a67a4a579fff8a64c01979deefe2d458c75cfbaa630de21fa05d37cf8a`).
Este archivo no la sustituye: la resume en la forma que `spec.yaml` cablea.
Donde los dos digan cosas distintas, **manda la sellada**.

**Acto:** `ACTO GEN2-LOTE-ENCIG-1`, 9/sep/2026, CAJA (Ubuntu), sobre `606f6ee`.
**Releva:** `CORR-0002` (ENCIG2025) → **12** `RESULT`: `RES-0003`, `RES-0004`,
`RES-0009`…`RES-0016`, `RES-0021`, `RES-0022`. Consumidores:
`milpa/tramite.yaml:tramite.mordida.discrecional`,
`…:tramite.mordida.con_registro`,
`…:tramite.gobierno_digital.util_sin_coercion`.

**CONGELADO en el COMMIT-1, antes de abrir un solo `conjunto_de_datos/*.csv`.**

---

## Qué mide

Tres familias sobre un solo payload (`encig25_base_datos_csv`,
`sha256 47daf2f7…`), universo **82 áreas urbanas de 100 mil habitantes o más**,
población **18 años y más**, referencia **2025**:

| familia | unidad | tabla | desenlace | ponderador |
|---|---|---|---|---|
| **A** · mordida discrecional | **PERSONA** | `encig2025_01_sec1_A_3_4_5_8_9_10.csv` | reactivo 8.3 (`P8_3_1/2/3`) | `FAC_P18` |
| **B** · mordida por canal | **EVENTO DE TRÁMITE** | `sec_7` × `sec_8` por `ID_TRA` | `P8_4` × canal `P7_3` | `FAC_TRA` |
| **C** · adopción de gobierno digital | **TRÁMITE `N_TRA=01`** (luz) | `sec_7` | canal `P7_3` | `FAC_TRA` |
| **X** · pago efectivo (hallazgo) | trámite | `sec_8` | `P8_6` | `FAC_P18` |

## Las tres decisiones que esta spec toma y GEN1 no

1. **A · primaria `SOLANY`, no `SOL1`.** El reactivo 8.3 tiene **tres** incisos
   (servidor público directo · coyote · insinuación). GEN1 usó sólo el primero.
   `A-DELTA-SOLANY-SOL1` mide lo que vale la restricción. `E.1`: GEN1 no elige
   la codificación de GEN2.
2. **B · primaria `SD` (sin deduplicar), no `CD`.** El descriptor define
   `NT_TIPO` (*«Número de trámite / Último evento», 01-03*) para distinguir
   eventos repetidos del mismo tipo. La rama `CD` reproduce la corrida base y
   `B-N-EVENTOS-DESCARTADOS-POR-DEDUP` mide cuántos eventos borra.
3. **Ninguna llave se adopta por autoridad.** El descriptor declara la llave de
   `sec_7` como `(CVE_ENT,UPM,V_SEL,R_ELE,N_TRA)` y **omite `NT_TIPO`**;
   `MAESTRA35-L1` verificó `(ID_TRA,NT_TIPO)`. `G-2`/`G-3`/`G-4` **miden las
   tres** y, si la llave del join no es única, B sale
   `NO-ESTIMABLE-LLAVE-NO-UNICA`. No se elige otra sobre la marcha.

## El recorte que se mide antes de rotular

`P7_3` tiene **ocho** categorías sustantivas. El par presencial `{1}` /
digital `{3,4,5}` usa cuatro y deja fuera `2` (banco/tienda/farmacia) y `6`
(módulos móviles). `B-P-RESIDUO-CANAL` mide su peso. Igual que el hallazgo 3.2
del lote ENVIPE: **«presencial vs digital» es propiedad del recorte, no del
instrumento.**

## Diseño

Bootstrap de `UPM_DIS` con reemplazo **dentro de** `EST_DIS`, 2 000 réplicas,
`numpy.PCG64`, semilla `20260909`, percentiles 2.5/97.5. `EST_DIS`/`UPM_DIS`
como **llaves de texto opacas** (nunca a entero, nunca re-rellenadas). Estratos
de UPM única → `IC-CON-ESTRATOS-DE-UPM-UNICA` y el IC se lee como **límite
inferior** de la anchura verdadera.

## Control positivo y adopción

Seis celdas contra su valor GEN1 sellado (`A-P-SOL1` 0.085118 · `B-P-PRE-CD`
0.116000 · `B-P-DIG-CD` 0.027358 · `B-P-PRE-SD` 0.141041 · `B-P-DIG-SD`
0.029868 · `C-P-ADOPTA` 0.673393), con `DELTA-VS-GEN1` **con signo**.
`NO-REPRODUCE` **no** autoriza tocar el medidor ni ajustar hacia atrás.

Cita de P3 sólo para `CANTIDAD-MEDIDA` (numerador contado directamente **y**
`round(medido,6) == sellado`). Los complementos con residuo `> 0` quedan
**sin cita** y con fila `NC` (patrón `NC-0085`).

## Lo que NO hace

No mide ENIF ni ENCUCI · no toca `CORR-0001` · no toca las reglas `_ejes_*` ·
no adjudica causalidad del canal (`B-DIFERENCIA-PRE-DIG-SD` va rotulada
`ASOCIACION`) · no toca marcador, capturas ni los `CALC-R` · no promedia olas
ni toca `serie_olas`.
