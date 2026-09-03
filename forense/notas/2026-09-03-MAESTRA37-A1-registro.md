# MAESTRA37-A1 · P2–P4 — registro, curador, cola y re-indexado (COMMIT-2)

3/sep/2026 · rótulo `MAESTRA37-A1` · firmas de mesa D13 (convención de versión), D14 (la versión
vigente rige; enero es historia), D15 (se registran e indexan los 129 —resultan **131**—, salud y nutrición).

El censo y el mapeo de ids que este registro ejecuta están congelados en
`forense/notas/2026-09-03-MAESTRA37-A1-censo.md` (COMMIT-1), escrito antes de tocar el manifiesto.

## 1 · Desviación de la SPEC, declarada antes que sus resultados

La SPEC de P2 dice: `--registra --id <base>__v2026_09_01 --archivo ENSANUT2024-v2026-09-01/<archivo>`.
**Ese comando no puede correr**, y no por una limitación de esta caja:

- `cmd_registra` resuelve la ruta como `os.path.join(raw_dir, a.archivo)` (`tests/manifiesto.py:320`)
  y aborta con «`data/raw/<archivo>` no existe». `--registra` **sólo alcanza `data_raw`**; lo dice
  su propio docstring («este script solo alcanza data/raw/»). La raíz `descargas_mx` se registra
  por `--escanea` + `--promueve`, que es la única vía que escribe el campo `raiz`.
- `--promueve` **deriva** el id con `_derivar_id` y no acepta `--id` ni `--nota`.
- `tests/manifiesto.py` está en el NO-TOCA del perímetro de este acto.

**Lo que se hizo, y qué garantiza cada mitad.** Las 129 entradas las creó el registrador por su vía
propia (`--escanea descargas_mx --grupo … --url … --usado-para …` seguido de `--promueve --grupo …`),
así que `sha256`, `tamano_bytes`, `fecha_descarga`, `entorno_descarga`, `raiz` y `archivo` salen del
archivo real en disco — ninguno se tecleó, que es la invariante por la que el registrador existe.
Sobre esas entradas ya escritas, un script de este acto aplicó la convención D13 a **dos campos que
el registrador no expone**: `id` (el derivado → `<slug>__v2026_09_01`) y `nota`. Nada más se tocó.

**El guard de `--escanea` no se rodeó: no llegó a dispararse.** El guard marca CONFLICTO cuando un
archivo trae el mismo `archivo` que una entrada existente con otro sha. Las entradas de enero llevan
el basename pelado (`adolescentes_ensanut2024_w.stata.stata.zip`) y las nuevas llevan la subcarpeta
(`ENSANUT2024-v2026-09-01/adolescentes_ensanut2024_w.stata.stata.zip`): son claves distintas en
`por_nombre`. Colisiones medidas: **0**. Y el dedup por sha sí actuó, en la dirección correcta —
ver §3.

Esto es **FP-280**: si mesa quiere `version_publicada` y `sustituye_a` como campos formales del
manifiesto y no como `clave: valor` dentro de `nota`, el registrador necesita una vía; este acto no
la abre.

## 2 · P2 · Las 125 entradas de ENSANUT v2

| veredicto A.7 | n |
|---|---|
| CONTENIDO-DISTINTO | 17 |
| NUEVO-SIN-HOMONIMO | 108 |
| **total registrado** | **125** |

Cada entrada lleva en `nota`, como `clave: valor`:

```
POST ArchId=<b64 de la ruta del portal>; version_publicada: 2026-09-01;
sustituye_a: <id de enero | ninguno>; contenido interno <miembro> sha256 <…>
(<bytes>, fecha interna <YYYY-MM-DD>); veredicto_A7: <…>;
A.7 doble descarga 2026-09-03 COINCIDE …
```

`version_publicada: 2026-09-01` aparece en **125** entradas (antes: 0).

### 2.1 · Corrección al criterio A.7 sobre `.xlsx`, hecha antes de escribir la nota

El primer paso de comparación tomaba «el miembro más grande del zip» como contenido interno. Sobre
un `.xlsx` eso da un **falso RE-EMPAQUETADO**: en `nse_hogar_ensanut_2024.Catálogo.xlsx` y
`nse_Integrantes_ensanut_2024.Catálogo.xlsx` el miembro más grande es un logo PNG embebido de
127 537 B, idéntico en las dos versiones (`5611425 9fb…`), aunque el contenedor pasa de 137 855 a
263 728 B. Corregido: para OOXML se compara el conjunto `xl/worksheets/*` + `sharedStrings.xml`, no
el binario más grande. Con el criterio corregido los dos son **CONTENIDO-DISTINTO**, y el veredicto
`RE-EMPAQUETADO` queda en **cero** para los 131 archivos.

### 2.2 · Los 17 con homónimo de enero — todos CONTENIDO-DISTINTO

| archivo (v2) | id de enero (`sustituye_a`) | interno viejo → nuevo (bytes, fecha) |
|---|---|---|
| `adolescentes_ensanut2024_w.csv.csv.zip` | `adolescentes_ensanut2024_w_csv_csv` | 4,240,707 / 2026-01-08 → 4,210,882 / 2026-09-01 |
| `adolescentes_ensanut2024_w.stata.stata.zip` | `adolescentes_ensanut2024_w_stata_stata` | 16,288,917 / 2026-01-08 → 16,575,279 / 2026-09-01 |
| `adultos_ensanut2024_w.Catálogo.xlsx` | `adultos_ensanut2024_w_catlogo` | 1,191,732 / 2026-01-08 → 2,014,794 / 2026-09-01 |
| `hogar_ensanut2024_w_icb.Catálogo.xlsx` | `hogar_ensanut2024_w_icb_catlogo` | 239,655 / 2026-01-08 → 374,179 / 2026-09-01 |
| `hogar_ensanut2024_w_icb.csv.csv.zip` | `hogar_ensanut2024_w_icb_csv_csv` | 6,391,078 / 2026-01-08 → 6,402,083 / 2026-09-01 |
| `integrantes_ensanut2024_w_icb.Catálogo.xlsx` | `integrantes_ensanut2024_w_icb_catlogo` | 678,963 / 2026-01-08 → 1,202,837 / 2026-09-01 |
| `integrantes_ensanut2024_w_icb.csv.csv.zip` | `integrantes_ensanut2024_w_icb_csv_csv` | 23,120,111 / 2026-01-08 → 22,746,129 / 2026-09-01 |
| `menores_ensanut2024_w.Catálogo.xlsx` | `menores_ensanut2024_w_catlogo` | 609,639 / 2026-01-08 → 991,687 / 2026-09-01 |
| `menores_ensanut2024_w.csv.csv.zip` | `menores_ensanut2024_w_csv_csv` | 5,193,434 / 2026-01-08 → 5,159,135 / 2026-09-01 |
| `menores_ensanut2024_w.stata.stata.zip` | `menores_ensanut2024_w_stata_stata` | 20,767,441 / 2026-01-08 → 21,074,435 / 2026-09-01 |
| `nse_Integrantes_ensanut_2024.Catálogo.xlsx` | `nse_integrantes_ensanut_2024_catlogo` | 17,170 / 2026-01-08 → 11,766 / 2026-09-01 |
| `nse_Integrantes_ensanut_2024.csv.csv.zip` | `nse_integrantes_ensanut_2024_csv_csv` | 1,958,708 / 2026-01-08 → 1,994,727 / 2026-09-01 |
| `nse_hogar_ensanut_2024.Catálogo.xlsx` | `nse_hogar_ensanut_2024_catlogo` | 11,069 / 2026-01-08 → 10,538 / 2026-09-01 |
| `nse_hogar_ensanut_2024.csv.csv.zip` | `nse_hogar_ensanut_2024_csv_csv` | 388,338 / 2026-01-08 → 399,311 / 2026-09-01 |
| `utilizadores_ensanut2024_w.Catálogo.xlsx` | `utilizadores_ensanut2024_w_catlogo` | 157,656 / 2026-01-08 → 257,801 / 2026-09-01 |
| `utilizadores_ensanut2024_w.csv.csv.zip` | `utilizadores_ensanut2024_w_csv_csv` | 1,392,437 / 2026-01-08 → 1,366,670 / 2026-09-01 |
| `utilizadores_ensanut2024_w.stata.stata.zip` | `utilizadores_ensanut2024_w_stata_stata` | 5,152,126 / 2026-01-08 → 5,197,750 / 2026-09-01 |

La fecha interna salta de `2026-01-08` a `2026-09-01` en los diecisiete. **Ningún sha interno
coincide.** Es re-publicación de contenido, no re-empaquetado.

### 2.3 · Las 23 entradas de enero: nota append fechada, nada más

Las 23 conservan `id`, `sha256`, `tamano_bytes` y `archivo` intactos. Se les añadió, tras ` || `,
una nota fechada: «superada por `<id nuevo>`…» a las 17 con sucesor, y a las 6 restantes la
constancia de que su contenido reaparece byte-idéntico en la versión vigente (por eso el registrador
no abrió entrada nueva). **Ninguna se borró ni se reemplazó** (D13/D14).

## 3 · Lo que el registrador se negó a registrar, y por qué está bien

- **6 archivos del depósito** (5 cuestionarios PDF + `indice_bienestar.Cuestionarios.docx`) tienen el
  mismo `sha256` que una entrada ya registrada en julio. El dedup por hash los rechaza. Por eso el
  contador es **125 y no 131**: el contenido de esos seis ya está en el manifiesto, bajo su id de julio.
- **6 copias sueltas en la raíz** (las que mesa bajó antes de crear la subcarpeta) son **byte-idénticas**
  a las de la subcarpeta. Se registró la de la subcarpeta; la suelta la bloqueó el mismo dedup. No se
  borró nada del disco de mesa. Detalle en el censo §1.3.

## 4 · P3 · ICPSR y PDN

| id | archivo | qué es | A.7 |
|---|---|---|---|
| `icpsr35024_ds1_w2_tabulados_t5_t9_derivados_2026_09_02` | `ICPSR35024-…-derivados-2026-09-02.csv` | 647 filas, tabulados de la ola 2 | un solo hash: re-exportar un tabulador en línea no es reproducible |
| `leeme_icpsr35024_ds1_w2_tabulados_t5_t9_procedencia_2026_09_02` | el `LEEME` de procedencia | declara «salida de tabulador en línea», clase (3) reportada | ídem |
| `35024_questionnaire_spanish` | `ICPSR_35024/35024-Questionnaire-spanish.pdf` | cuestionario, documentación | ídem |
| `pdn_s3v2` | `PDN_S3v2.zip` | 34 miembros, un `.json` por entidad, sólo S3 | sin URL directa conocida: un solo hash, declarado |

**FP-263 queda materialmente cerrada por este depósito** (medido con `csv.DictReader`, no supuesto):

- (i) **T9b sí está**: 45 celdas, `row_var=W2_P38A`, `col_var=W2_P38B`, `control_var=P46` — exactamente
  la receta que FP-263 pedía.
- (ii) **La ronda 1 sí está**: `P40` (48 celdas), `P39` (39) y `P38B_oportunidades` (144, control
  `P36C`) aparecen como variable de fila. El control negativo de FP-263 había medido que **ninguna**
  tabla del disco usaba esas tres.
- Además: el nombre dice `T5-T9` pero el archivo trae **once** tablas (T5, T6, T7a, T7b, T8, T9a, T9b,
  T10, T11, T12, T13).
- Lo que **no** cambia: sigue siendo instrumento de segunda mano, conteos SIN PONDERAR; el microdato
  `35024-0001-Data.dta` sigue sin obtenerse. La adjudicación es de `MAESTRA37-L2`, no de este acto.

**Cola de adquisición.** `PDN_SESNA_S1_S2_S3_S6`: `PENDIENTE` → **`OBTENIDO-PARCIAL`**, con
`ids_manifiesto=pdn_s3v2`. Llegó S3 (servidores públicos sancionados por faltas graves, un `.json`
por entidad, fechados 9/may/2025); **S1, S2 y S6 no llegaron**. `MEXICO_PANEL_STUDY_2012` mantiene
`OBTENIDO` y suma los tres ids nuevos. Vista `data/cola-adquisicion-v1_0.tsv` regenerada (T26).

## 5 · P2 (segunda mitad) · Las tres capas del curador

Alta por `tools/curador_registro/GUIA-CURADOR-REGISTRO.md` §alta, **+8 componentes**: etiquetado,
actividad física, antropometría, frecuencias, rec24h, lactancia, plomo, sangre. Una operación,
las tres tablas: **+8 relaciones · +8 procedencias · +8 filas de utilidad · +1 alias**.

- `fuente_canonica_normalizada` = `ENSANUT_CONTINUA_2024`, alias nuevo con `accion_fuente=NO_FUSIONAR`
  (por defecto misma institución no es mismo objeto).
- `clasificacion_relacion` = **`CANDIDATA`** en las ocho, por A.4 conservador: el payload existe y está
  verificado, pero **no se ha leído una sola variable** en este acto.
- `capa2_manifiesto = SI` y `capa3_disco_real = SI`: **medidos en esta caja y en este acto**, no citados
  de otro. `python3 tests/manifiesto.py --verifica` → `descargas_mx: coincide=267 · no_coincide=0 ·
  ausente=0 · sin_configurar=0`.
- Control positivo Y negativo sobre `via_capa2.verificar_entrada` (A.13): las **125** entradas v2 dan
  `COINCIDE=125`, y la misma entrada con el `sha256` alterado da `NO_COINCIDE` — el verificador sí
  estaba mirando lo que se le pidió.

### 5.1 · La necesidad bajo la que se asientan: hallazgo, no decisión

La GUÍA dice que si la regla no tiene `N`, «el alta empieza ahí»; el encargo dice **sin inventar N
nuevas**. Las dos se cumplen a la vez sólo declarando el hueco:

**`N36` (R4.3) es hoy la única necesidad de salud de `necesidad-objeto-modelo.tsv`.** `R4.1`, `R4.2`,
`R4.4` y `R4.5` — las otras cuatro reglas de salud que `MAESTRA37-L3` arbitró hoy mismo — **no tienen
`necesidad_id`**. Es el mismo hueco de mapa que `FP-230` nombró para R4.3 antes de `MAESTRA34-N6`.
Las ocho altas se asientan bajo `N36` **porque el alta exige una necesidad existente**, y cada una lo
dice en su `nota`, su `incertidumbre` y su `reserva`: *esta alta no afirma que el componente sirva a
R4.3*. La adjudicación regla↔componente es de mesa / `MAESTRA37-L3-BIS`.

### 5.2 · Baseline recifrado y validado

```
python3 tools/curador_registro/baseline.py data/curacion-registro   → "ok": true, "errores": []
python3 tools/curador_registro/via_capa2.py --root .                → 0 diffs; COINCIDE=193 NO_COINCIDE=0
```
Conteos: relaciones 211→**219** · procedencias 212→**220** · utilidad 211→**219** · alias 14→**15** ·
candidatas 147→**155**. La invariante 3 (`evidencias − relaciones == fusiones`) se conserva: 220−219=1.

## 6 · P4 · Re-indexado → `data/inventario-reactivos-descargas-mx-v1_1.tsv`

Archivo **NUEVO**; `v1_0` queda intacto en el árbol. Los dos scripts escriben a un `-v1_0` fijo por
diseño y están en el NO-TOCA: se corrieron tal cual, sus salidas se movieron a `v1_1` y el `v1_0`
comiteado se restauró desde git.

| | filas de dato |
|---|---|
| `inventario_reactivos.py --raiz descargas_mx` | 19 501 |
| `inventario_reactivos_ext.py --raiz descargas_mx` | 23 035 |
| **v1_1 (unión)** | **42 536** |
| v1_0 (para comparar) | 31 677 |

**Regresión, medida y no supuesta:** de los **116** `payload_id` presentes en v1_0, los **116** traen
sus filas **idénticas byte a byte** en v1_1. `0` payloads de v1_0 desaparecieron; `92` son nuevos.

### 6.1 · Cobertura sobre los 131 archivos de ENSANUT v2 (DE2, se reporta, no se repara)

| tipo | n | filas en v1_1 | con `texto_reactivo` no vacío |
|---|---|---|---|
| `.stata.stata.zip` | 38 | sí | **sí** (etiquetas STATA) |
| `.csv.csv.zip` | 38 | sí | **no — 0** |
| `.Catálogo.xlsx` | 38 | **0 filas** | — |
| `.Cuestionarios.pdf` / `.docx` | 17 | **0 filas** | — |

El extractor **sí alcanza** `_variables.csv` (266 filas) y `_valores.csv` (114 filas) dentro de los
zip CSV — pero devuelve **`texto_reactivo` vacío en las 380**. No es que no los lea: los lee y no
saca texto. Los `.Catálogo.xlsx` no producen ninguna fila. **Es DE2 y no se repara aquí** (el
extractor está en el NO-TOCA).

### 6.2 · `busca_reactivos.py`

Se añadió la clave `descargas_mx_v1_1` a `TABLAS`. **`descargas_mx` sigue apuntando a v1_0 a
propósito**: reapuntarla habría cambiado en silencio lo que ya lee quien pide esa clave, y v1_0 es la
única cifra contra la que la regresión se midió. Control:

```
--tablas descargas_mx_v1_1 --palabra lactancia → universo 42536 filas, 2 candidatas
--tablas descargas_mx     --palabra lactancia → universo 31677 filas, 1 candidata
```

## 7 · Contador

| cifra | encargo | real |
|---|---|---|
| entradas del manifiesto | 1 104 → «declara» | **1 104 → 1 233** (+129: 125 ENSANUT v2 + 3 ICPSR + 1 PDN) |
| payloads con `version_publicada` | 0 → 129 | **0 → 125** (6 del depósito ya estaban bajo su id de julio) |
| archivos en la subcarpeta | 129 | **131** (169 `ArchId` de la página − 38 `.spss`) |
| componentes ENSANUT 2024 en corpus | 10 → esperado 27 | **38 con microdato** (42 bases de archivo distintas) |
| inventario `descargas_mx` | 31 678 → «declara» | **31 677 → 42 536** (archivo nuevo v1_1) |
| cargas al motor | 0 | **0** |
| dominios abiertos | 0 → 0 | **0** |
| medición de modelo | cero directo | **cero**: no se abrió una sola variable |
