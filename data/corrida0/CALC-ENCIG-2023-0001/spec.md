# `CALC-ENCIG-2023-0001` — cara mecánica

Gobierna esta corrida la spec SELLADA `forense/prereg-caja/ENCIG-MORDIDA-2023-spec-v1_0.md`
(**`prereg-caja-ENCIG-MORDIDA-2023`**, `sha256 ea4379e5d659e5b103b6d8d20db2a166bdbfc93caa27a3408efe771c6b76bda6`).
Este archivo no la sustituye: la resume en la forma que `spec.yaml` cablea.
Donde los dos digan cosas distintas, **manda la sellada**.

**Acto:** `ACTO GEN2-FIRMAS-MESA-1`, 15/sep/2026, **NUBE**, sobre `2b65202d`.
**Firma:** «Si a todas.» — mesa, 15/sep/2026, HOJA DE FIRMAS DE MESA 2026-09-15,
**OBJETO 4**: *«D1 / NC-0197 — opción (b): medir ENCIG 2023 con spec sucesora de
`CALC-ENCIG-0001`. Spec aquí; corrida en caja.»*
**Sucesora de:** `prereg-caja-ENCIG-MORDIDA` v1.0 (`sha256 00c7c4a6…`), familia **B**.

**CONGELADO en el COMMIT-1, en NUBE, antes de abrir un solo byte de microdato.**

---

## Qué mide

**El mismo estimando de la familia B de `CALC-ENCIG-0001`, sobre la ola 2023.**
Un payload (`encig23_base_datos_csv`, `sha256 af733d86…`, 38 309 647 bytes),
**dos** miembros, unidad **evento de trámite**:

| familia | unidad | archivos | desenlace | canal | ponderador |
|---|---|---|---|---|---|
| **B · `SD`** (PRIMARIA) | evento de trámite, sin deduplicar | `sec_7` ⋈ `sec_8` | `P8_4` (1/0) | `P7_3`: `PRE={1}`, `DIG={3,4,5}` | **`FAC_TRA` de `sec_7`** |
| **B · `CD`** (secundaria) | ídem, deduplicado por `ID_TRA` | ídem | ídem | ídem | ídem |

## Los dos hechos que gobiernan el medidor

1. **El ponderador se fija POR ARCHIVO.** `FAC_TRA` vive en
   `encig2023_04_sec_7.csv` y **no** en `encig2023_05_sec_8.csv`, que trae
   `FAC_P18` — otro ponderador sobre otro universo. Resolverlo por nombre sobre
   la tabla unida tomaría el equivocado **sin avisar**. Por eso
   `archivo_de_ponderador` es un **parámetro explícito** y no hay sustituto: sin
   `FAC_TRA`, `NO-ESTIMABLE-COLUMNA-AUSENTE:FAC_TRA`. `A.15(c)`.
2. **La medición exige un JOIN.** `P7_3` está en `sec_7` y `P8_4` en `sec_8`;
   ningún miembro trae los dos. **Llave primaria `ID_TRA`** (la de 2025, por
   continuidad del estimando); **llave de control `(ID_VIV,ID_PER,ID_TRA,N_TRA)`**,
   que se computa también y cuyo desacuerdo es un `RESULT`. Si `ID_TRA` no es
   única en `sec_8`, o si las dos llaves emparejan conjuntos distintos →
   **`NO-ESTIMABLE-LLAVE-NO-UNICA`**. No se deduplica sobre la marcha.

## Diseño

Bootstrap de `UPM_DIS` con reemplazo **dentro de** `EST_DIS`, 2 000 réplicas,
`numpy.PCG64`, semilla `20260915`, percentiles 2.5/97.5. Método **heredado**, no
elegido: `prereg-caja-ENCIG-MORDIDA` **v1.1** lo elevó a estándar de la familia
(cierra `NC-0112`). `EST_DIS`/`UPM_DIS` como **llaves de texto opacas**. Estratos
de UPM única → `IC-CON-ESTRATOS-DE-UPM-UNICA` y el IC se lee como **límite
inferior**.

## Contraste de ola, y por qué no es una serie

`B-DELTA-2023-VS-2025-*` compara contra `0.1410407168724654` (presencial) y
`0.029867554626649372` (digital), **con signo**, rotulado
**`CONTRASTE-DE-OLA-NO-SERIE`**. Dos olas no son una tendencia y esta spec no la
construye. La hipótesis **con** signo pre-registrado es sólo `H1`
(`B-P-PRE-SD > B-P-DIG-SD`); el nivel de 2023 no se pre-registra porque **nada en
el árbol lo dice**.

## La frase sellada que esto corrige sin reescribirla

`ENCIG-MORDIDA-spec-v1_0.md:142` dice «`CORR-0001` (ENCIG2023, **sin payload**…)».
`NC-0197` la declara **FALSA EN LA LETRA desde el 29/jul/2026** (el payload está
en el manifiesto en cinco formatos) y **NO editable** (`E.3`). Esta sucesora es el
vehículo correcto: mide lo que la frase declaró no medible **sin tocar un byte del
sello**.

## Lo que NO hace

No abre microdato · **no escribe el medidor** (lo escribe el acto de CAJA a partir
de este contrato; `preflight` dirá `BLOQUEADO:script_ausente` y eso es correcto) ·
no mide las familias A (`P8_3_*`), C (`N_TRA`=01) ni X (`P8_6`), que **existen en
este payload** y quedan fuera por perímetro, no por imposibilidad · no promedia
olas ni construye serie · no adopta cifra alguna a `milpa/` ni crea conducta nueva ·
no reescribe la v1.0, la v1.1 ni `CALC-ENCIG-0001` · no releva `CORR-0001` por sí
solo: `RES-0007`/`RES-0008` son `ASIGNADO` **sin canal** y esta spec mide **por
canal** — la correspondencia la decide mesa.
