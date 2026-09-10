# `CALC-ENCUCI-0001` — cara mecánica

Gobierna esta corrida la spec SELLADA
`forense/prereg-caja/ENCUCI-MORDIDA-PROTESTA-spec-v1_0.md`
(**`prereg-caja-ENCUCI-MORDIDA-PROTESTA`**,
`sha256 33add37841455a9da6402e2dce8c7edaaa33e8ecc9a94c3c5a9d44b10961a919`).
Este archivo no la sustituye: la resume en la forma que `spec.yaml` cablea.
Donde los dos digan cosas distintas, **manda la sellada**.

**Acto:** `ACTO GEN2-LOTE-ENCUCI-1`, 9/sep/2026, CAJA (Ubuntu/WSL2), sobre
`d20039a3`.
**Releva:** `CORR-0003` (ENCUCI2020) → `RES-0005`, `RES-0006`, `RES-0061`,
`RES-0062`. Consumidores: `milpa/tramite.yaml:tramite.mordida.discrecional`
(familia A) y `milpa/tramite.yaml:civico.protesta.agravio_urbano_encuci2020`
(familia B).

**CONGELADO en el COMMIT-1, antes de leer un solo registro de un `.dbf`.**
Lo único abierto al congelar: manifiesto, `FD_ENCUCI2020.pdf`, la lista de
miembros del ZIP y la **cabecera** de cada `.dbf` (descriptores de campo de 32
bytes), los inventarios, `milpa/tramite.yaml` y `demanda-*.tsv`.

---

## Qué mide

**Dos constructos, un payload.**

- **Familia A — mordida.** Proporción ponderada de personas de 15+ **con
  contacto declarado** con algún servidor público en los 12 meses previos que
  declaran que (i) **les pidieron** una dádiva (`AP5_17`), (ii) **tuvieron que
  darla** (`AP5_18`), o (iii) **cualquiera de las dos** (la codificación GEN1).
- **Familia B — protesta.** Proporción ponderada de personas de 15+ que
  declaran haber **participado en una protesta alguna vez en su vida**
  (`AP7_3_5`), en cada celda del eje **entorno (`DOMINIO`) × agravio
  (`AP4_3_2`)**.

## Unidad de observación — declarada, porque cambia el denominador

| universo | unidad | tabla | filtro | ponderador |
|---|---|---|---|---|
| **`U_A` (punto de A)** | persona seleccionada | `SEC_4_5` | contacto `AP5_16_k = 1` para algún `k` · `AP5_17 ∈ {1,2}` · `AP5_18 ∈ {1,2}` | `FAC_SEL` |
| `U_A_POB` (secundario) | persona seleccionada | `SEC_4_5` | sólo `FAC_SEL` válido; «sin contacto» cuenta como `0` | `FAC_SEL` |
| **`U_B` (punto de B)** | persona seleccionada | `SEC_6_7_8` ⨝ `SEC_4_5` por `ID_PER` | `AP7_3_5 ∈ {1,2}` · `AP4_3_2 ∈ {1,2}` · `DOMINIO ∈ {U,C,R}` | `FAC_SEL` |

## Codificación — la primaria NO es la de GEN1 (familia A)

| celda | `= 1` | `= 0` | papel |
|---|---|---|---|
| `A-P-ENTREGA` **(PRIMARIA)** | `AP5_18 = 1` | `AP5_18 = 2` | el único reactivo que mide **entrega** |
| `A-P-SOLICITUD` (primaria) | `AP5_17 = 1` | `AP5_17 = 2` | **solicitud** |
| `A-P-CUALQUIERA` | `AP5_17 = 1` **o** `AP5_18 = 1` | ambos `= 2` | **codificación GEN1 — la única adoptable** |
| `A-P-AMBAS` | ambos `= 1` | resto de `U_A` | secundaria |

`9` (NS/NR) y blanco **salen contados**, jamás imputados a `0`.

**Familia B:** `d = 1` si `AP7_3_5 = 1`, `0` si `= 2`. Eje congelado:
`urbano = {U, C}` (el descriptor llama a `C` «**Complemento urbano**»),
`rural = {R}`; la agrupación alternativa `{U}` vs `{R,C}` se emite como
**sensibilidad declarada**, no adoptable.

**Escala:** proporción en `[0,1]`. Nunca porcentaje, nunca puntos
porcentuales. Más alto = más mordida (A) / más protesta (B).

## Tipos: manda el header del DBF, no el descriptor

`AP5_16_*` y `AP4_3_2` son **`N` 19,15** (el texto crudo llega
`1.000000000000000`); `AP5_17`/`AP5_18` son **`C` 6**; `AP7_3_5` es **`C` 7**;
`FAC_SEL` es **`N` 19,10** y **no se normaliza**; `EST_DIS`/`UPM_DIS` son
**llaves opacas de texto** (el descriptor dice ancho 3 para `EST_DIS`; el DBF
dice 7). `_cod()` normaliza `'1'` y `'1.000000000000000'` al mismo entero, y la
guardia `G-3` **mide** la trampa emitiendo los dos conteos.

## Incertidumbre de diseño

`FAC_SEL`, `DOMINIO`, `ESTRATO`, `UPM_DIS` y `EST_DIS` están declarados por el
descriptor en el bloque «Campos empleados para el diseño muestral» y presentes
en la cabecera de las cinco tablas: **`FP-201` es falso también para ENCUCI
2020**. Bootstrap de `UPM_DIS` con reemplazo dentro de `EST_DIS`, 2 000
réplicas, `numpy.PCG64`, semilla `20260909`, percentiles 2.5/97.5. Un estrato
con **una sola UPM** se re-muestrea a sí mismo (varianza cero), se cuenta, y si
hay alguno `METODO-IC` sale `IC-CON-ESTRATOS-DE-UPM-UNICA`: el IC se lee como
**límite inferior de la anchura verdadera**.

Los `ic95` GEN1 **no se ponen lado a lado** con éstos (A-bis.3): el método de
GEN1 no está escrito en ningún artefacto reproducible. El control positivo es
**sólo del punto**.

## Guardias que PARAN (no arreglan)

`NO-ESTIMABLE-MIEMBRO-AUSENTE:<m>` · `NO-ESTIMABLE-COLUMNA-AUSENTE:<col>` ·
`NO-ESTIMABLE-COLUMNA-VACIA:<col>` · `NO-ESTIMABLE-UNIVERSO-VACIO` ·
`NO-ESTIMABLE-LLAVE-NO-UNICA` · `NO-ESTIMABLE-DISENO-INCOMPLETO`.

## Adopción de P3 — criterio pre-declarado

`CANTIDAD-MEDIDA` (recibe cita) si y sólo si (1) el numerador es una categoría
declarada del reactivo contada **directamente** —no `1 −` otra cosa— **y**
(2) `round(medido, 6) == valor_sellado`. `RES-0006` falla la condición (1) por
construcción: `D1`/`NC-0108` ya lo declaró `DERIVADO-NO-MEDIDO`, y esta spec lo
obedece. El `p` del motor **no se mueve**: la adopción es cita.
