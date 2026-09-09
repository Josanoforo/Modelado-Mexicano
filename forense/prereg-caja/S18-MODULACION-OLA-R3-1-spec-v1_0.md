# S18 · Pre-registro de la MODULACIÓN POR OLA de `R3.1` — `tramite.mordida.discrecional` / `enmienda_encig2025` sobre la serie ENCIG de ocho olas

### `prereg-caja-S18` · **v1.0** · 8 de septiembre de 2026

> | | |
> |---|---|
> | **ARCHIVO** | `forense/prereg-caja/S18-MODULACION-OLA-R3-1-spec-v1_0.md` |
> | **NOMBRE ESTABLE** | **`prereg-caja-S18`** — cítalo así, nunca por nombre de archivo |
> | **QUÉ ES** | Spec propia de la **modulación por ola** para la segunda de las dos reglas que el marco vigente trae con `serie_olas`: `tramite.mordida.discrecional`, enmienda `enmienda_encig2025` (`R3.1`), ocho olas de ENCIG 2011→2025, tres celdas del marco (`TRA-M-02`, `TRA-M-03`, `TRA-M-07`). Cumple `T9` y cierra la otra mitad de `NC-0025`. |
> | **QUÉ NO ES** | **No corre ningún CALC y no produce ninguna cifra nueva.** No re-mide ninguna ola de ENCIG. No promedia, no ajusta tendencia, no interpola. No mueve `R3.1` ni toca el `0.62` ASIGNADO que la enmienda ya dejó `REFUTADA-POR-R`. No reescribe corridas selladas. |
> | **VERIFICAS ASÍ** | La serie está publicada verbatim en `milpa/tramite.yaml:109-117` con `p`, `ic95`, `n`, `estratos`, `upm`, `ponderador`, `metodo`, `variable`, `sha256_payload` y `payload_manifiesto_id` por ola. El inventario de §2 y las marcas `ORIGEN-ARBITRO` de §4 se re-derivan de ahí. |

**Acto:** `ACTO GEN2-C0-B · LA BASE`, 8/sep/2026, entorno **CAJA (UBUNTU)**, sobre `origin/main = 017ac24`.

---

## 1 · Qué se modula aquí

La regla `tramite.mordida.discrecional` conserva su `0.62`/`0.38` ASIGNADO como historia **`REFUTADA-POR-R`**; la enmienda `enmienda_encig2025` (firma DM, 1/sep/2026, `ACTO MAESTRA34-N4`) lo sustituye por `paga_mordida_encig2025 = 0.085118`, la ola 2025 de una serie de ocho. Las tres celdas del marco que la arbitran usan árbitros de 2013, 2020 y 2021: **sin modular, `M` contesta 2025 contra los tres.**

## 2 · Sobre qué serie

`milpa/tramite.yaml:tramite.mordida.discrecional.enmienda_encig2025.serie_olas`, ocho entradas:

| ola | `p` | `ic95` | `n` | estratos | upm | variable | método declarado |
|---|---|---|---|---|---|---|---|
| 2011 | 0.068328 | [0.060955, 0.076391] | 23 784 | 116 | 6 544 | `P4_11` | bootstrap-conglomerado |
| 2013 | 0.044538 | [0.038969, 0.050107] | 22 081 | 180 | 6 510 | `P8_3` | **`R-json` (TRA-M-03, ya público)** |
| 2015 | 0.047684 | [0.043130, 0.052521] | 26 417 | 268 | 7 415 | `P8_3` | bootstrap-conglomerado |
| 2017 | 0.077024 | [0.072671, 0.081378] | 39 085 | 357 | 9 138 | `P8_3_1` | **`R-json` (TRA-M-05, ya público)** |
| 2019 | 0.084484 | [0.079530, 0.089737] | 39 454 | 358 | 9 170 | `P8_3_1` | bootstrap-conglomerado |
| 2021 | 0.071815 | [0.067118, 0.076512] | 39 763 | 353 | 9 190 | `P8_3_1` | **`R-json` (TRA-M-07, ya público)** |
| 2023 | 0.072863 | [0.068865, 0.076988] | 38 838 | 347 | 8 928 | `P8_3_1` | bootstrap-conglomerado |
| 2025 | 0.085118 | [0.080935, 0.089260] | 40 042 | 442 | 9 172 | `P8_3_1` | bootstrap-conglomerado |

Ponderador `FAC_P18` en las ocho. **Diferencia de reactivo declarada y NO colapsada:** `P4_11` (2011) → `P8_3` (2013, 2015) → `P8_3_1` (2017 en adelante). El propio `serie_olas` la publica campo por campo; esta spec la conserva como reserva de comparabilidad y no la promedia ni la renombra.

## 3 · Qué estimando — la misma regla de ola que `S17`

Regla vigente (ADENDA de mesa del 8/sep/2026 a `P3(c)` de `ACTO GEN2-T9`, `NC-0025`): **última ola estrictamente anterior a la del árbitro; sin anterior → `SIN-PREVIA` y la celda no modula.** La versión derogada («la más cercana distinta») podía elegir una ola posterior y es fuga temporal.

Derivación mecánica para las tres celdas (no es medición nueva):

| celda | árbitro | encuesta del árbitro | ola previa en la serie | `M_modulado` | `M` sin modular |
|---|---|---|---|---|---|
| `TRA-M-02` | 2020 | **ENCUCI** | 2019 | 0.084484 | 0.085118 |
| `TRA-M-03` | 2013 | ENCIG | 2011 | 0.068328 | 0.085118 |
| `TRA-M-07` | 2021 | ENCIG | 2019 | 0.084484 | 0.085118 |

`N-SIN-PREVIA = 0` para esta regla: el árbitro más antiguo es 2013 y la serie empieza en 2011.

## 4 · Dos reservas que sí muerden en esta regla (y no en `S17`)

### 4.1 · `ORIGEN-ARBITRO` — tres de ocho entradas

Tres entradas de la serie (2013, 2017, 2021) declaran `metodo: R-json (…, ya público)`: **no nacen de una medición propia, sino de la reutilización del `R` arbitrado de otra celda.** La ADENDA de `NC-0025` las rotula `ORIGEN-ARBITRO` y establece que **toda celda que module con una de ellas queda `VERIFICACION-NO-PUNTUA`**, porque `F-DD` (`ADR-237`) cubre misma-encuesta-misma-ola y **no** la reutilización cruzada.

Aplicado a las tres celdas: **ninguna de las tres modula con una entrada `ORIGEN-ARBITRO`** — sus previas son 2019 (bootstrap propio), 2011 (bootstrap propio) y 2019 (bootstrap propio). `N-ORIGEN-ARBITRO-USADAS = 0` hoy. **El guard se declara aunque no muerda**, porque muerde en cuanto el marco sortee una celda con árbitro 2014-2015 (previa 2013), 2018-2019 (previa 2017) o 2022-2023 (previa 2021) — tres de los ocho intervalos posibles.

### 4.2 · `TRA-M-02` cruza instrumento: el árbitro es ENCUCI, la serie es ENCIG

La celda `TRA-M-02` tiene `encuesta = ENCUCI`, `ola = 2020`, y su conducta es `paga_mordida_encig2025`, cuya serie es **ENCIG**. Modular esa celda con la ola ENCIG 2019 **es un crosswalk entre instrumentos**, no una selección dentro de una serie.

Es exactamente lo que el selector hermano prohíbe por escrito (`tools/baseline_temporal.py`, docstring de `seleccionar_baseline`): *«Igualar `Serie` exige igual población, reactivo, codificación, segmento y escala. Un crosswalk entre instrumentos tiene que resolverse antes y estar documentado por el consumidor: este selector no lo decide por semejanza.»*

**Veredicto de esta spec para `TRA-M-02`: `NO-CONSTRUIBLE-SIN-CROSSWALK`.** La celda **no modula** hasta que exista un crosswalk ENCUCI↔ENCIG documentado y firmado, con la equivalencia de universo, reactivo y codificación demostrada — no supuesta por semejanza de tema. La ADENDA de `NC-0025` no cubre este caso: rotula la reutilización de `R` dentro de la misma serie, no el salto de instrumento. Se declara aquí como hallazgo propio de esta spec, no como algo heredado.

## 5 · Constructibilidad (A.15) — CONSTRUIBLE en 2 de 3 celdas

| celda | veredicto | por qué |
|---|---|---|
| `TRA-M-03` | **CONSTRUIBLE** | previa 2011, medición propia, mismo instrumento; reserva de reactivo (`P4_11` vs `P8_3`) declarada en §2 |
| `TRA-M-07` | **CONSTRUIBLE** | previa 2019, medición propia, mismo instrumento y mismo reactivo (`P8_3_1`) |
| `TRA-M-02` | **NO-CONSTRUIBLE-SIN-CROSSWALK** | §4.2 — el árbitro es de otro instrumento |

Inventario citado: las ocho olas están en corpus con `payload_manifiesto_id` y `sha256_payload` publicados en `serie_olas` (`encig_2011_base_datos_encig2011_dbf` … `encig25_base_datos_csv`). Esta spec **no** los re-verifica byte a byte: no corre ningún CALC, y afirmar una verificación que no se hizo sería peor que no hacerla. Un acto sucesor que corra la modulación de `R3.1` los verifica por `preflight`.

## 6 · Lo que esta spec explícitamente NO autoriza

1. **No mueve `R3.1`.** Ni el `0.62` ASIGNADO (que sigue `REFUTADA-POR-R`, se conserva como historia y no se borra) ni el `0.085118` de la enmienda. Ninguna cifra de la modulación entra a un veredicto (`T9`).
2. **No promedia, no interpola, no ajusta tendencia** entre las ocho olas.
3. **No resuelve el crosswalk de `TRA-M-02`** ni lo declara resuelto por semejanza: lo deja `NO-CONSTRUIBLE-SIN-CROSSWALK` con el criterio escrito.
4. **No reescribe corridas selladas** (`CALC-M-…-ola-v2`, `CALC-AGG-…-ola-v2`).

## 7 · Sello

Congelada en el `COMMIT-1` del `ACTO GEN2-C0-B`. Esta spec **no produce cifras**. Si un acto sucesor corre un CALC de modulación sobre `R3.1`, **el primer resultado que produzca ese procedimiento es el que se reporta.**
