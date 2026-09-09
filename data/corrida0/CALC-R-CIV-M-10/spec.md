# `CALC-R-CIV-M-10` — cara mecánica

Gobierna esta corrida la spec SELLADA `forense/prereg-caja/R-ENVIPE-SERIE-spec-v1_0.md`
(**`prereg-caja-R-ENVIPE-SERIE`**, `sha256 b9a29cf656b9fcfe2794eaa4e2b3de0a9df699d72af1d143e0059c64b051dba4`).
Este archivo no la sustituye: la resume en la forma que `spec.yaml` cablea.
Donde los dos digan cosas distintas, **manda la sellada**.

**Acto:** `ACTO GEN2-R-SERIE-CSV`, 9/sep/2026, CAJA (Ubuntu) con corpus montado, sobre `071406a`.
**Celda:** `CIV-M-10` — ENVIPE 2021, **delitos de 2020**.
**Releva:** `CORR-0036` → `RES-0108`, el árbitro `R` de esta celda del marco `M`.
Consumidor natural: `forense/prereg-duelo-v2/marco-M-sorteado-v1_3.tsv:CIV-M-10:R`.
**La adopción NO es de este acto**: la decide mesa por lote (`F3`).

**CONGELADO en el COMMIT-1, antes de abrir un solo `conjunto_de_datos/*.csv`.**

---

## Qué mide

**Dos estimandos sobre la misma lectura del mismo archivo**, cada uno con su escala declarada:

1. **PRIMARIO — el árbitro `R`.** Proporción ponderada de delitos con razón principal de
   no-denuncia en `{01, 02, 06}` (miedo al agresor · miedo a extorsión · desconfianza en la
   autoridad), sobre el universo de **todos** los delitos con `BP1_23 ∈ {01..09}`, ponderador
   `FAC_DEL`, diseño `EST_DIS`/`UPM_DIS`. La codificación, el universo, el ponderador y el
   diseño se copian **verbatim** de `forense/prereg-duelo-v2/codificacion-R-v1_0.tsv`; la
   variable y la escala, de `espec-R-ciega-v1_2.tsv`. **Ninguno lo elige el ejecutor.**
2. **SECUNDARIO HOMOLOGADO — el punto de serie.** El mismo desenlace bajo el universo `U1` y la
   codificación `C1` de `prereg-caja-ENVIPE-DENUNCIA` (delitos **personales** `BPCOD 05..15`,
   `BP1_20 = 2`, denominador `{01..08}`), para que esta ola pueda ponerse junto al punto de la
   ola 2025 sin cambiar dos cosas a la vez. Se emite también `C2` (la partición GEN1) y el delta.

**`U_R` y `U1` no se comparan entre sí** (`A-bis.4`): están en la misma corrida porque salen de
la misma lectura, no porque sean comparables.

## Identidad del insumo

| campo | valor |
|---|---|
| `id` de manifiesto | **`envipe2021_csv`** — resuelto por `tests/payload_resolver.py`, nunca por heurística |
| miembro | `conjunto_de_datos_TMod_Vic_ENVIPE_2021/conjunto_de_datos/conjunto_de_datos_TMod_Vic_ENVIPE_2021.csv` |
| `Identifier` (metadato) | `DDI-MEX-INEGI-ENVIPE-2021-V01` |
| `Temporal` (metadato) | `2020-01-01-2020-12-31` → **delitos de 2020** |
| catálogo `bp1_23` | leído en **latin-1** (la codificación se prueba por archivo, no por ZIP) |

**Nota de esta ola:** el catalogo y el descriptor de esta ola NO declaran el codigo b (blanco); 2023 y 2024 si. El tratamiento del blanco es identico en las tres.
**Redacción del reactivo en esta ola:** 'ante el Ministerio Publico' (sin 'o Fiscalia Estatal'); 'Por miedo al agresor' — ninguna de esas diferencias mueve un código.

## Diseño

`EST_DIS` y `UPM_DIS` se agrupan como **cadenas opacas** (nunca `int()`, nunca `zfill()`). El
descriptor de esta ola declara `EST_DIS Numerico(3), 001..303 SEGUN DESCRIPTOR` y `UPM_DIS Numerico(5), 00001..99999 SEGUN DESCRIPTOR`; el perfil **real**
se emite en `RESULT-R-CIV-M-10-PERFIL-DISENO`, porque el descriptor ya mintió sobre esto en la
ola 2025. `EE` e `IC95` por conglomerado último con `tests/svystat.py:prop_ultimate_cluster`,
**importado y no reimplementado**. Un estrato con una sola UPM entra al punto, aporta varianza
cero, y su conteo va en `N-ESTRATOS-UPM-UNICA`; si es `> 0`, el IC es **límite inferior** de la
anchura verdadera.

## Control positivo

**Este medidor no lo calcula.** No abre `forense/prereg-duelo-v2/corridas-R/CIV-M-10.json` y no
recibe el valor GEN1 por ningún parámetro. El control lo corre
`forense/prereg-caja/R-ENVIPE-SERIE-control-gen1.py` **después** de `verify`, sobre el **punto** y
no sobre el IC, con las cuatro ramas pre-declaradas en §6.1 de la sellada. `NO-REPRODUCE` **no**
invalida la corrida, **no** autoriza tocar el medidor y **no** cambia el estimando.

> **El primer resultado que produzca este procedimiento es el que se reporta.**
