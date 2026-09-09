# R-ENVIPE-SERIE · Pre-registro de familia de los tres árbitros `R` de ENVIPE moderna (olas 2021, 2023, 2024)

### `prereg-caja-R-ENVIPE-SERIE` · **v1.0** · 9 de septiembre de 2026

> | | |
> |---|---|
> | **ARCHIVO** | `forense/prereg-caja/R-ENVIPE-SERIE-spec-v1_0.md` |
> | **NOMBRE ESTABLE** | **`prereg-caja-R-ENVIPE-SERIE`** — cítalo así, nunca por nombre de archivo |
> | **QUÉ ES** | Pre-registro de familia, congelado **antes de abrir un solo byte de microdato**, de tres corridas hermanas — `CALC-R-CIV-M-10` (ENVIPE 2021), `CALC-R-CIV-M-12` (ENVIPE 2023) y `CALC-R-CIV-M-13` (ENVIPE 2024) — que producen, con cadena `E.2` completa, el árbitro `R` de las tres celdas `CIV-M-10/-12/-13` del marco `M`. Releva las demandas `CORR-0036`/`CORR-0040`/`CORR-0044` (`RES-0108`/`RES-0113`/`RES-0118`). |
> | **QUÉ NO ES** | No es una re-lectura de los dictámenes `R` de GEN1: `forense/prereg-duelo-v2/corridas-R/CIV-M-10.json` / `-12` / `-13` son **control positivo calculado DESPUÉS de sellar, por script aparte**, y no entran como insumo de nada (§0.4, §6.1). No adjudica el duelo, no mueve `tier`, no adopta ningún `R` en ningún consumidor (§7.5). No toca las olas DBF (2012–2020), que son encargo hermano. No toca `milpa/`, ni el marcador, ni las capturas `L`. |
> | **VERIFICAS ASÍ** | `python3 tools/corrida0.py preflight CALC-R-CIV-M-10` (y `-12`, `-13`) en VERDE antes de correr; después `run` y `verify`. El control positivo externo corre **después**, con `python3 forense/prereg-caja/R-ENVIPE-SERIE-control-gen1.py`, y sus tres ramas están pre-declaradas en §6.1. |

**Acto:** `ACTO GEN2-R-SERIE-CSV`, 9/sep/2026, entorno **CAJA (UBUNTU)**, corpus montado (`data/raw` → `/home/pc0/mm-corpus/raw`, 400 archivos examinados por `tools/entorno.py`), sobre `origin/main = 071406a` (`PR #655`). SHA de redacción del encargo archivado: `5969990`.

---

## 0 · Premisas verificadas contra el árbol, y la contaminación declarada

### 0.1 · La premisa del encargo sobre `origin/main` no se sostiene, y no bloquea

El encargo declara su `VERIFICACIÓN DE EXISTENCIA` «contra el clon de `05f5fc56`» y ordena re-derivar contra `origin/main` al abrir. Se movió: **10 commits** entre `05f5fc56` y `071406a` (`PR #654` `GEN2-REVISA-CALC` y `PR #655`). Re-derivación completa, con los comandos a la vista:

```
$ grep -E "^CORR-(0036|0040|0044)" data/corrida0/demanda-corridas.tsv
CORR-0036  ENVIPE 2021  envipe2021_csv  tools/arbitra.py  1  RES-0108  CAJA  PARCIAL:sha256+spec_sha  4
CORR-0040  ENVIPE 2023  envipe2023_csv  tools/arbitra.py  1  RES-0113  CAJA  PARCIAL:sha256+spec_sha  4
CORR-0044  ENVIPE 2024  envipe2024_csv  tools/arbitra.py  1  RES-0118  CAJA  PARCIAL:sha256+spec_sha  4

$ ls data/corrida0/ | grep -c '^CALC-R'
0                                    ← 22 directorios CALC-*, ninguno R (A.13)

$ python3 tests/manifiesto.py --verifica --id envipe2021_csv   → COINCIDE (22 334 244 bytes)
$ python3 tests/manifiesto.py --verifica --id envipe2023_csv   → COINCIDE (17 728 995 bytes)
$ python3 tests/manifiesto.py --verifica --id envipe2024_csv   → COINCIDE (17 837 779 bytes)
```

Las cuatro afirmaciones del bloque `A.8` del encargo **siguen valiendo** sobre `071406a`. Tres cifras derivadas se fijan aquí, porque el encargo mandó derivarlas al cierre y no heredarlas: **ADR real máximo `431`** (candidato `432`), **`FP` máximo `369`**, **`NC` máxima `NC-0088`** (siguiente `NC-0089`). El rótulo `GEN2-R-SERIE-CSV` está **AUSENTE** de `canon/registro-rotulos.tsv` y se censa en la cascada.

`python3 tools/ya_medido.py civico.denuncia.miedo_desconfianza` → **`MEDIDA-EN: tramite.yaml`** (`milpa/tramite.yaml:574`, `p = 0.294313`, `tier: FUERTE`, `ACTO MAESTRA32-E18`). Esa cifra es de **ENVIPE 2025** y **este acto no la toca**: mide otras tres olas, y ninguna de ellas se propaga a ningún sello.

### 0.2 · La tabla ciega **no define** cuatro de los cinco elementos que el encargo le atribuye

El encargo dice, verbatim: *«estimando primario = `R` tal como lo define la tabla ciega (variable, codificación, universo, ponderador, diseño EST/UPM)»*. Verificado contra el archivo, **la tabla ciega define dos de esos cinco y declara los otros tres no estimados**:

```
$ awk -F'\t' '$1=="CIV-M-10"' forense/prereg-duelo-v2/espec-R-ciega-v1_2.tsv
  variable    = BP1_23
  escala      = binaria
  cv_arbitro  = BP1_23
  universo    = "NO ESTIMADO EN ESTE ACTO -- censo de existencia sobre inventario de reactivos, …"
  estimador   = "NO ESTIMADO EN ESTE ACTO"
  ponderador  = "NO ESTIMADO EN ESTE ACTO"
```

Idéntico en `CIV-M-12` y `CIV-M-13`, e idéntico en `forense/prereg-duelo-v2/marco-M-congelado-v1_2.tsv`. **La premisa del encargo se corrige aquí, no en silencio**, y el hueco se llena con la única fuente pre-registrada que existe para esas cuatro columnas, no por inferencia del ejecutor:

| elemento | fuente que manda | valor |
|---|---|---|
| variable, escala | `espec-R-ciega-v1_2.tsv` (`sha256 b2dacd8a…`) — **manda sobre cualquier otra fuente**, como el encargo dice | `BP1_23`, binaria |
| codificación `y→{0,1}` | `forense/prereg-duelo-v2/codificacion-R-v1_0.tsv` (`sha256 cf5dfb18…`), filas `CIV-M-10/-12/-13`, `estado = PROPUESTA`, fechadas 31/ago y 1/sep/2026 | `y=1` si `BP1_23 ∈ {01,02,06}`; `y=0` si `∈ {03,04,05,07,08,09}`; `99` y blanco **fuera** |
| universo | idem | delitos captados en `TMod_Vic` §I, **todos los tipos de delito**, sin filtro adicional más allá de la codificación |
| ponderador · estrato · UPM | idem | `FAC_DEL` · `EST_DIS` · `UPM_DIS` |
| estimador puntual y varianza | `forense/prereg-duelo-v2/corridas-R/PROCEDIMIENTO-R-v1_0.md` §1 | proporción ponderada `Σwy/Σw`; `EE` por **conglomerado último** con `tests/svystat.py:prop_ultimate_cluster`, **que se importa y no se reimplementa** |

**Consecuencia declarada:** `codificacion-R-v1_0.tsv` está en `estado = PROPUESTA`, no `SELLADA`. Esta spec la adopta como definición del estimando primario **porque es la única pre-registración de esas cuatro columnas que existe y es anterior al dato de estas tres celdas**, y lo dice en vez de presentarla como sellada. Cada uno de sus seis elementos se verifica, ola por ola, contra el codebook de la ola en §2 — no se hereda por cita.

### 0.3 · Contaminación declarada (`ADR-46`) — esta corrida NO es ciega

Se dice antes de cualquier cifra, no después. Al congelar esta spec la sesión **ya había leído**:

| dónde | qué | valor |
|---|---|---|
| el propio encargo, bloque de CONTAMINACIÓN | los tres puntos `R` de GEN1 | `0.2049` / `0.2081` / `0.1946` |
| `data/corrida0/demanda-resultados.tsv:RES-0108/0113/0118` | los mismos, con todos sus decimales | `0.20493399286059008` · `0.20811159524290274` · `0.1946118021509308` |
| `codificacion-R-v1_0.tsv`, columna `fuente` de `CIV-M-10` | que alguien abrió el microdato 2021 para verificar presencia de columnas, y **cuántas filas tiene `TMod_Vic` 2021** | `37156` filas |
| `forense/prereg-caja/ENVIPE-DENUNCIA-spec-v1_0.md` completa | el universo `U1`, la codificación `C1`/`C2` y el método de IC de la ola 2025 | — |

**Consecuencia, sin adornos:** el ejecutor conoce los tres resultados GEN1 antes de congelar. Lo que esta spec hace con eso son tres cosas mecánicas, no promesas:

1. **La codificación primaria no se elige aquí.** Se copia verbatim de `codificacion-R-v1_0.tsv`, que es anterior a esta sesión y a este encargo. El ejecutor no tiene ninguna palanca sobre `{01,02,06}` vs. el resto: si la quisiera mover para acercarse o alejarse de `0.2049`, tendría que editar un archivo que esta spec cita por `sha256` y que el `preflight` verifica.
2. **El control positivo se calcula DESPUÉS de sellar y por un script aparte** (§6.1). El medidor **no abre** los tres JSON de GEN1 y **no recibe** los tres valores como parámetro. No hay ninguna ruta por la que el número GEN1 pueda entrar al cálculo.
3. **La rama de discrepancia está escrita antes** (§6.1): `NO-REPRODUCE` **no invalida** la corrida, **no autoriza** tocar el medidor, y se reporta con el embudo de la ola. Escribirla antes es lo que impide construir la excusa después.

**Qué sigue siendo genuinamente desconocido al congelar:** todo el embudo de las tres olas (elegibles, `09`, `99`, blanco, filas sin ponderador, sin diseño, masa de ponderadores, número de estratos y de UPM, estratos con UPM única), el punto y el IC del estimando **secundario homologado** en las tres olas, la relación de ese secundario con el punto 2025 (que esta sesión **no ha leído**, §0.4), y si los tres puntos primarios reproducen a GEN1 o no.

### 0.4 · Lo que esta sesión NO ha abierto, y por qué

Declarado como negativo con universo (A.13), porque el valor probatorio del control de §6.1 depende enteramente de esto:

| no abierto | por qué |
|---|---|
| `tools/arbitra.py` (47 319 B) | es la aritmética GEN1 que produjo los tres puntos de control. Leerla antes de congelar convertiría el control positivo en una tautología: mismo código sobre el mismo archivo da el mismo número por construcción, y eso no verifica nada. `E.1` verbatim: **GEN1 no elige la codificación de GEN2.** |
| `forense/prereg-duelo-v2/corridas-R/CIV-M-10.json`, `-12`, `-13` | son el dictamen GEN1 completo (punto, IC, `n`, diseño). Su existencia y su `estado=COMPUTADO` los verifica el script de control de §6.1 al correr, no esta redacción. |
| `data/corrida0/CALC-ENVIPE-0001/resultados.json` | trae el punto 2025 con el que P3 arma la serie. Se lee **en P3, después de sellar las tres corridas** — leerlo antes le daría al ejecutor una expectativa numérica sobre el estimando secundario, que es justo la mitad del trabajo que aquí es ciega. |
| cualquier `conjunto_de_datos/*.csv` de las tres olas | es el microdato. Lo abierto hasta este punto, y nada más: el manifiesto, los tres `diccionario_de_datos/*`, los tres `catalogos/*`, los tres `metadatos/*.txt`, la lista de miembros de los tres ZIP, los tres `cuest_modulo_envipe20NN.pdf`, y `data/inventario-reactivos-v1_2.tsv`. |

`tools/arbitra_gen2.py` (259 líneas) **sí** se leyó, y se declara: es el adaptador GEN2 que `NC-0018` dejó listo, resuelve el payload por `payload_id` exacto de `codificacion-R-v1_0.tsv` y emite una `spec.yaml` de cuatro `RESULT`. **Esta spec no lo usa como medidor** y dice por qué en §5.3 — su `medir()` delega en `arbitra.calcula_desde_tabla`, es decir, en la aritmética GEN1, con las dos consecuencias del renglón 1 de la tabla de arriba. Lo que sí se hereda de él, porque es reuso y no duplicación (`D-14`), es su **vocabulario de identificadores** (`CALC-R-<celda>`, `RESULT-R-<celda>-{PUNTO,EE,N,ESTADO}`) y su regla de resolución de payload por `id` exacto.

---

## 1 · Identidad: instrumento, ola, payload, tabla — las tres, una por una

### 1.1 · Payloads, por el manifiesto (nunca «está en `data/raw`»)

| celda | ola | `id` de manifiesto | archivo | `sha256` | bytes | `fecha_descarga` |
|---|---|---|---|---|---|---|
| `CIV-M-10` | ENVIPE 2021 | **`envipe2021_csv`** | `envipe2021_csv.zip` | `88153c67ff3666be511dab3f3b483226a0af9f0e8683bd8dbfba8d616ddbfdd1` | 22 334 244 | 2026-07-30 |
| `CIV-M-12` | ENVIPE 2023 | **`envipe2023_csv`** | `envipe2023_csv.zip` | `0dcc00a7fc37b79806f1bf1b85b12cd090b5ecc8e76983a3a1a861f2ef3fb404` | 17 728 995 | 2026-07-30 |
| `CIV-M-13` | ENVIPE 2024 | **`envipe2024_csv`** | `envipe2024_csv.zip` | `90776b2fab6e3666dad1cb5f5f3eb7d6a7699dbfefd4f8f04f07fb01e61a6fb2` | 17 837 779 | 2026-07-30 |

Los tres `id` salen de la columna `payload_id` de `codificacion-R-v1_0.tsv` y coinciden con los que `demanda-corridas.tsv` declara para `CORR-0036`/`CORR-0040`/`CORR-0044`. **Ninguno se busca por heurística**: cada `spec.yaml` los declara como `origen: manifiesto` y `tests/payload_resolver.py` los resuelve, que es lo mismo que hace `preflight`.

⚠️ **Homónimos, revisados y descartados.** El manifiesto registra además, para estas olas, `envipe2021_fd_pdf`, `envipe2021_cuest_principal_pdf` y `envipe2021_cuest_modulo_pdf` (y sus equivalentes 2023/2024) — documentación, no microdato — y una entrada `envipe2022_csv` que **no** es de este lote. A diferencia de ENVIPE 2025, **ninguna de las tres olas de este lote tiene un segundo payload de microdato con otro `sha256`**: `grep -n "envipe" data/manifiesto.yaml | grep -E "202[1234]"` devuelve exactamente las cuatro entradas de microdato (`2021`, `2022`, `2023`, `2024`) y las nueve de documentación. No hay confusión de canasta que sellar.

### 1.2 · Ola y periodo de referencia, por el metadato de cada payload

Verbatim de `*/metadatos/metadatos_*.txt`:

| ola del nombre | `Identifier` | `Temporal` | **delitos de** |
|---|---|---|---|
| ENVIPE 2021 | `DDI-MEX-INEGI-ENVIPE-2021-V01` | `2020-01-01-2020-12-31` | **2020** |
| ENVIPE 2023 | `MEX-INEGI.EGS3.02-ENVIPE-2023` | `2022-01-01-2022-12-31, 2023-03-01-2023-04-30 …` | **2022** |
| ENVIPE 2024 | `MEX-INEGI.EGS3.02-ENVIPE-2024` | `2023-01-01-2023-12-31, 2024-03-01-2024-04-30 …` | **2023** |

**La ola se llama 20NN; los delitos que mide ocurrieron en 20NN−1.** Toda unidad de esta spec dice «ENVIPE 20NN (delitos de 20NN−1)». Consecuencia que P3 tiene que respetar y que se declara aquí, antes de medir: con la ola 2025 (delitos de 2024) del `prereg-caja-ENVIPE-DENUNCIA`, la serie que este lote puede armar cubre los años de delito **2020 · 2022 · 2023 · 2024**, y **le falta 2021**, que vive en `envipe2022_csv` — una ola que existe en el corpus y que **este lote no mide** (§7.4).

### 1.3 · Tabla y unidad de observación — **declarado, porque cambia el denominador**

`BP1_23` vive en `TMod_Vic`, cuya fila es **un DELITO** (hasta 15 por persona, llave `ID_DEL`) y cuyo ponderador es `FAC_DEL` («Factor delito»). Las tres corridas son **de unidad delito** y ninguna colapsa a persona: `codificacion-R-v1_0.tsv` pide `FAC_DEL`, y colapsar a persona sería una regla de analista que ni la tabla ciega ni la tabla de codificación dictan.

Rutas exactas del miembro dentro de cada ZIP, tomadas del inventario de reactivos (`data/inventario-reactivos-v1_2.tsv`, columna `archivo_miembro`) y no de la forma del nombre:

| ola | miembro |
|---|---|
| 2021 | `conjunto_de_datos_TMod_Vic_ENVIPE_2021/conjunto_de_datos/conjunto_de_datos_TMod_Vic_ENVIPE_2021.csv` |
| 2023 | `tmod_vic_envipe2023/conjunto_de_datos/conjunto_de_datos_tmod_vic_envipe2023.csv` |
| 2024 | `tmod_vic_envipe2024/conjunto_de_datos/conjunto_de_datos_tmod_vic_envipe2024.csv` |

⚠️ **La ola 2021 escribe las rutas en mayúsculas y las otras dos en minúsculas.** No es cosmético: un medidor que arme la ruta por plantilla en vez de leerla de la spec falla en una de las tres. Cada `spec.yaml` trae su ruta literal.

---

## 2 · El reactivo, verbatim del cuestionario de cada ola

`pdftotext -layout` sobre `data/raw/cuest_modulo_envipe2021.pdf` (`911 976 B`), `…2023.pdf` (`947 099 B`) y `…2024.pdf` (`933 605 B`), los tres `COINCIDE` contra el manifiesto. Bloque 1.20–1.23, **las tres olas**:

```
1.20 ¿Acudió ante el Ministerio Público [o Fiscalía Estatal, 2023/2024] a denunciar el delito?
     Sí ... 1  PASE A 1.24   ·   No ... 2      CIRCULE UN SOLO CÓDIGO
     SI EL CÓDIGO DEL DELITO ES DEL 05 AL 15, PASE A LA PREGUNTA 1.23.

1.21 ¿Algún(a) otro(a) integrante de este hogar acudió a denunciar el delito …?
     Sí ... 1   ·   No ... 2  PASE A 1.23   ·   No sabe / no responde ... 9

1.23 ¿Cuál fue la razón principal por la que no denunció o no denunciaron el delito …?
     CIRCULE UN SOLO CÓDIGO
     Por miedo al (a la) agresor(a) .............. 01      No tenía pruebas ................. 07
     Por miedo a que lo (la) extorsionaran ....... 02      Por actitud hostil de la aut. .... 08
     Delito de poca importancia .................. 03      Otra ............................. 09
     Pérdida de tiempo ........................... 04      No sabe / no responde ............ 99
     Trámites largos y difíciles ................. 05
     Desconfianza en la autoridad ................ 06
```

**Veredicto de estabilidad del reactivo, ola por ola:** el enunciado, el orden de las diez categorías, sus códigos y el flujo de saltos son **idénticos en 2021, 2023 y 2024** — y también en 2025, contra el §2 de `prereg-caja-ENVIPE-DENUNCIA`. Las únicas diferencias son de **redacción**, no de contenido:

| ola | diferencia literal |
|---|---|
| 2021 | «ante el Ministerio Público» (sin «o Fiscalía Estatal»); «Por miedo al agresor» |
| 2023 | añade «o Fiscalía Estatal»; sigue «Por miedo al agresor» |
| 2024 | añade lenguaje de género: «Por miedo al (a la) agresor(a)», «que lo (la) extorsionaran» |

**Ninguna de esas diferencias mueve un código.** Por eso las tres olas son construibles con la MISMA codificación y **ninguna sale `NO-CONSTRUIBLE`** — que era la rama que el encargo mandaba declarar si el reactivo o sus códigos difirieran.

### 2.1 · Catálogo embebido y descriptor, POR ARCHIVO (`A.15`)

`catalogos/BP1_23.csv` (2021) · `catalogos/bp1_23.csv` (2023, 2024), leído con un lector que prueba UTF-8 y cae a latin-1 **por archivo** — 2021 y 2023 vienen en **latin-1**, 2024 en **UTF-8**; una codificación fija para el ZIP entero rompe una de las tres. Los diez códigos y sus etiquetas coinciden con el cuestionario en las tres olas. **Diferencia declarada:** el catálogo y el descriptor de 2021 **no listan el código `b` (blanco)**; 2023 y 2024 sí. No cambia nada del tratamiento — el blanco se cuenta y se excluye igual en las tres (§3.5) —, pero se dice porque es una asimetría real del descriptor.

Columnas declaradas en `diccionario_de_datos/*` de cada ola, y **verificadas además contra el inventario de reactivos** (que se deriva del archivo, no del descriptor): las **nueve** columnas que esta spec usa —`ID_PER`, `ID_DEL`, `BPCOD`, `BP1_20`, `BP1_21`, `BP1_23`, `FAC_DEL`, `EST_DIS`, `UPM_DIS`— aparecen en el inventario para el miembro exacto de las tres olas (`0 faltantes` en las tres, sobre 129 variables inventariadas por ola).

| campo | 2021 | 2023 | 2024 |
|---|---|---|---|
| `BP1_23` | Numérico(2) `01..09, 99` | Numérico(2) `01..09, 99, b` | Numérico(2) `01..09, 99, b` |
| `BPCOD` | Numérico(2) `01..15` | Numérico(2) `01..15` | **Carácter**(2) `01..15` |
| `BP1_20` | Numérico(1) `1,2` | Numérico(1) `1,2` | Numérico(1) `1,2` |
| `FAC_DEL` | Numérico(6) `000001..999999` | Numérico(6) | Numérico(6) |
| `EST_DIS` | **Numérico(3)** `001..303` | **Alfanumérico(3)** `001..595` | **Carácter(3)** `001..607` |
| `UPM_DIS` | **Numérico(5)** `00001..99999` | **Alfanumérico(5)** | **Carácter(7)** `0000001..9999999` |

⚠️ **El descriptor cambia de tipo y de rango entre olas, y ya se ha medido que miente.** En ENVIPE 2025 el descriptor declaró `EST_DIS` `Carácter(3)` `001..607` y el archivo trajo cuatro caracteres, `0001..0746`, 739 valores distintos. **Esta spec no confía en ninguna de las seis celdas de las dos últimas filas**: trata `EST_DIS` y `UPM_DIS` como **llaves de texto opacas** (§3.4) y emite el perfil observado como `RESULT` para que la discrepancia, si la hay, quede medida y no supuesta.

---

## 3 · Estimandos, universos y codificación — todo pre-declarado

Cada corrida emite **dos** estimandos sobre la **misma apertura** (una lectura del mismo archivo), cada uno con su escala declarada (`A-bis.3`).

### 3.1 · Estimando **PRIMARIO** — el árbitro `R`

Copiado verbatim de `codificacion-R-v1_0.tsv` (§0.2), sin una sola elección del ejecutor:

| | |
|---|---|
| **universo `U_R`** | filas de `TMod_Vic` con `BP1_23 ∈ {01,…,09}` y `FAC_DEL` válido. **Todos los tipos de delito** (`BPCOD 01..15`), sin filtro adicional: la tabla de codificación dice «sin filtro adicional más allá de la codificación», y observa que `BP1_23` viene en blanco para quien sí denunció, caso que el código no válido ya deja fuera. |
| **codificación `C_R`** | `y = 1` si `BP1_23 ∈ {01, 02, 06}` · `y = 0` si `BP1_23 ∈ {03, 04, 05, 07, 08, 09}` · `99` y blanco **fuera del universo** |
| **ponderador** | `FAC_DEL` |
| **diseño** | estrato `EST_DIS`, UPM `UPM_DIS` |
| **escala** | proporción en `[0,1]`; **más alto = más peso del miedo/desconfianza como razón principal**. No es porcentaje ni puntos porcentuales. |

**Dos rasgos de `C_R` que se señalan porque no son obvios y no se van a cambiar:** el código `08` («actitud hostil de la autoridad») está en el **cero**, y el `09` («Otra») está **dentro del denominador**, también en el cero. Las dos son decisiones de `codificacion-R-v1_0.tsv`, anteriores a esta sesión.

### 3.2 · Estimando **SECUNDARIO** — el punto de serie homologado a la ola 2025

Para que la serie hable el mismo idioma que el punto de 2025, cada corrida mide además el estimando de `prereg-caja-ENVIPE-DENUNCIA` (`sha256 e404e7b5…`), **verbatim de su §3.1 y §3.2**, sobre la misma tabla:

| | |
|---|---|
| **universo `U1`** | `BPCOD ∈ {05,…,15}` (delitos personales — el único tramo al que el cuestionario enruta a 1.23 por una sola condición) **y** `BP1_20 = 2` **y** `BP1_23 ∈ {01,…,08}` **y** `FAC_DEL` válido |
| **codificación `C1`** (la primaria de 2025) | `y = 1` si `BP1_23 ∈ {01, 02, 06}` · `y = 0` si `∈ {03, 04, 05, 07, 08}` |
| **codificación `C2`** (la partición GEN1 de 2025) | `y = 1` si `BP1_23 ∈ {01, 02, 06, 08}` · `y = 0` si `∈ {03, 04, 05, 07}` |
| **ponderador · diseño · escala** | `FAC_DEL` · `EST_DIS`/`UPM_DIS` · proporción en `[0,1]`, más alto = más miedo/desconfianza |

Se emiten `p(C1,U1)` y `p(C2,U1)` con su IC y su delta. **`p(C1,U1)` es el punto de serie** — el único que P3 puede poner junto al de 2025.

### 3.3 · `U_R` y `U1` **no son el mismo universo**, y por eso no se comparan entre sí

Se escribe antes de medir, porque después es tarde. Las tres diferencias, cada una en su dirección:

1. **`U_R` incluye los delitos de hogar (`BPCOD 01..04`); `U1` no.** Esos delitos llegan a 1.23 por una ruta de **dos** condiciones (`BP1_20 = 2` y `BP1_21 ≠ 1`), no de una.
2. **`U_R` incluye el código `09` («Otra») en el denominador; `U1` lo excluye.**
3. **`U_R` no exige `BP1_20 = 2`** — se apoya en que el blanco de quien denunció ya cae fuera por código no válido. `U1` lo exige explícitamente. Esta spec **mide la diferencia** en vez de suponerla: `RESULT-…-N-INCONSISTENTES-BP1-20` cuenta las filas con `BP1_23 ∈ {01..09}` y `BP1_20 ≠ 2`. Si sale `0`, las dos rutas coinciden en las tres olas y queda dicho con un número; si sale `> 0`, la premisa de la tabla de codificación tiene excepciones y también queda dicho con un número. **Ninguna rama cambia el estimando primario**, que es el que `codificacion-R-v1_0.tsv` define.

`A-bis.4` verbatim, adoptado aquí: **jamás se compara el primario contra el secundario entre universos.** Están en la misma corrida porque salen de la misma lectura del mismo archivo, no porque sean comparables. La única serie que P3 publica es la del **secundario**, y la única comparación del primario es contra su propio control GEN1, celda por celda.

### 3.4 · Diseño: llaves opacas y la regla de estratos de UPM única

**`EST_DIS` y `UPM_DIS` se tratan como cadenas opacas.** Nunca `int()`, nunca `zfill()`, nunca re-relleno al ancho que dice el descriptor: convertirlas partiría o fundiría estratos **en silencio** y el IC saldría mal sin ningún error. La llave de conglomerado es el par `(EST_DIS, UPM_DIS)` construido con un separador (`U+241F`) que no aparece en el dato.

Como el descriptor ya mintió sobre esto en la ola 2025, cada corrida emite `RESULT-…-PERFIL-DISENO`: las longitudes observadas de `EST_DIS` y `UPM_DIS` sobre el universo, con su conteo, y si alguna trae espacios en los bordes. **Es la comprobación que el descriptor no puede dar**, y su desacuerdo con el descriptor es hallazgo que se reporta, no defecto que se corrige.

**Varianza.** `EE(R)` por el estimador de **conglomerado último** ya sellado en el repo, `tests/svystat.py:prop_ultimate_cluster`, **importado y no reimplementado** — es lo que `PROCEDIMIENTO-R-v1_0.md` §1 manda y lo que `U2-CRUCE` (`PR #335`, `ADR-165`) validó contra una cifra publicada del INEGI. `IC95 = p ± 1.959963985 · EE`, recortado a `[0,1]`, que es lo que esa función ya devuelve.

**Regla para estratos con una sola UPM**, pre-declarada:

- Un estrato con **exactamente una** `UPM_DIS` no aporta varianza estimable con este método. **No se colapsa con otro estrato** (colapsar es una decisión de diseño que esta spec no está autorizada a tomar) y **no se descarta** (sesgaría el punto): entra al punto y aporta varianza cero, que es el contrato verbatim del docstring de `prop_ultimate_cluster` («se reportan aparte, no se fuerzan a cero silenciosamente»).
- Su conteo va en `RESULT-…-N-ESTRATOS-UPM-UNICA`. Si es `> 0`, `RESULT-…-METODO-IC` sale **`IC-CON-ESTRATOS-DE-UPM-UNICA`** y el IC se lee como **límite inferior de la anchura verdadera**, nunca como IC exacto.
- Si `EST_DIS` o `UPM_DIS` faltan como columna, o vienen vacías en toda fila del universo, el IC sale `null` y `METODO-IC` = **`NO-ESTIMABLE-DISENO-INCOMPLETO`**; **el punto se reporta igual**.
- Si sólo **algunas** filas del universo vienen sin diseño, **entran al punto igual** (el estimador no depende del diseño) y en la varianza forman un **pseudo-estrato de llave vacía**, que es lo que hace la función sellada con cualquier llave. No se descartan y no se imputan a un estrato vecino. Su conteo va en `RESULT-…-N-SIN-DISENO`, y si es `> 0` el IC se lee con ese número a la vista.

**Segundo método de IC, sólo para el secundario homologado.** El punto de 2025 trae su IC de un **bootstrap de UPM con reemplazo dentro de estrato**, 2000 réplicas, percentiles 2.5/97.5, `numpy.PCG64`, semilla `20260909` (`prereg-caja-ENVIPE-DENUNCIA` §3.4). Una serie cuya columna de IC mezcla dos métodos no es legible, así que cada corrida emite **también** ese bootstrap para `p(C1,U1)` y `p(C2,U1)`, con la misma semilla y la misma regla de estrato de UPM única (el estrato singleton se re-muestrea a sí mismo). Los dos IC del secundario se emiten y se etiquetan; **ninguno sustituye al otro** y la nota dice cuál usa la serie. El estimando **primario** conserva **sólo** el IC de conglomerado último, porque es lo que `PROCEDIMIENTO-R` manda para `R`.

**`CV` y la regla de `SKIP`.** `CV = EE/R` sobre el estimando primario. `PROCEDIMIENTO-R` §1 fija `CV ≥ 30% ⇒ SKIP` (`FP-79`) y manda aplicarla en el `COMMIT-2` y sólo ahí, con su `CV` a la vista: se emite `RESULT-…-CV` y `RESULT-…-VEREDICTO-CV` ∈ {`CV-ACEPTABLE`, `SKIP-POR-CV`}. **`SKIP-POR-CV` no borra el punto ni lo oculta**: lo marca como no utilizable por el marcador y se reporta con su cifra.

### 3.5 · Guardias de existencia, antes de medir

Pre-declaradas porque el descriptor puede documentar una variable que el archivo no trae, y una columna puede existir y estar vacía:

1. **Columna ausente.** Si falta cualquiera de `ID_DEL`, `BPCOD`, `BP1_20`, `BP1_23`, `FAC_DEL`, `EST_DIS`, `UPM_DIS` → todos los `RESULT` de estimación salen `null`, `ESTADO` = **`NO-ESTIMABLE-COLUMNA-AUSENTE:<col>`**, nombrando la columna.
2. **Columna vacía.** Si `BP1_23` existe pero no tiene **ningún** valor válido en todo el archivo → **`NO-ESTIMABLE-COLUMNA-VACIA:BP1_23`**.
3. **Universo vacío.** Si `N(U_R) = 0` → **`NO-ESTIMABLE-UNIVERSO-VACIO`**. Idéntico, por separado, para `U1`.
4. **Ponderador no positivo.** Filas con `FAC_DEL` no finito o `≤ 0` se **cuentan** (`N-SIN-PONDERADOR`) y salen del universo.
5. **Blanco.** `BP1_23` que no parsea a entero (vacío, `b`, cualquier otra cosa) se **cuenta** (`N-BP1-23-BLANCO`) y sale de todo universo. **Cero nunca sustituye falta de dato.**

Ninguna guardia «arregla» el dato: cada una **para y declara**.

---

## 4 · Estimadores

Sobre el universo `U` y la codificación `C`:

```
p(C, U) = Σ_{i∈U} w_i · d_i(C)  /  Σ_{i∈U} w_i          w = FAC_DEL
```

con `d ∈ {0,1}` según §3.1/§3.2, sumas en **orden fijo de fila** para que dos corridas del mismo árbol den bytes idénticos. `EE` y `IC95` por `prop_ultimate_cluster` sobre las tuplas `(EST_DIS, UPM_DIS, FAC_DEL, d)` del mismo universo.

- **Primario:** `R = p(C_R, U_R)`, con `EE(R)`, `IC95`, `CV`.
- **Secundario homologado:** `p(C1, U1)` y `p(C2, U1)`, cada uno con `EE`/`IC95` de conglomerado último **y** con IC de bootstrap; más `DELTA-C2-C1` con signo.

---

## 5 · Lo que emiten las tres corridas (contrato)

### 5.1 · Identificadores

Tres corridas, un nombre por celda, siguiendo el vocabulario que `NC-0018` y `tools/arbitra_gen2.py` ya fijaron:

| celda | `calc_id` | prefijo de `RESULT` | demanda que releva |
|---|---|---|---|
| `CIV-M-10` | `CALC-R-CIV-M-10` | `RESULT-R-CIV-M-10-…` | `CORR-0036` → `RES-0108` |
| `CIV-M-12` | `CALC-R-CIV-M-12` | `RESULT-R-CIV-M-12-…` | `CORR-0040` → `RES-0113` |
| `CIV-M-13` | `CALC-R-CIV-M-13` | `RESULT-R-CIV-M-13-…` | `CORR-0044` → `RES-0118` |

Los cuatro sufijos canónicos que `arbitra_gen2.spec_de_celda()` anticipa — `PUNTO`, `EE`, `N`, `ESTADO` — se emiten con **esos nombres exactos**, para que el `R` que este lote sella sea el que cualquier consumidor del duelo ya sabe nombrar.

### 5.2 · Los `RESULT`, por bloque

La lista cerrada vive en cada `data/corrida0/CALC-R-<celda>/spec.yaml` y es la que `corrida0 run` valida output por output. Lectura humana (`<C>` = la celda):

| bloque | `RESULT-R-<C>-…` | qué trae |
|---|---|---|
| **A · embudo** | `N-FILAS-TABLA` · `N-BP1-23-01-09` · `N-BP1-23-99` · `N-BP1-23-BLANCO` · `N-SIN-PONDERADOR` · `N-SIN-DISENO` · `N-CODIGO-FUERA-DE-CATALOGO` · `N-INCONSISTENTES-BP1-20` · `N-BPCOD-01-04` · `N-BPCOD-05-15` · `MASA-FAC-DEL` | conteos **antes y después** de cada filtro, la masa de ponderadores del universo primario, y las dos particiones que hacen legible la diferencia con `U1` |
| **B · primario (`R`)** | **`PUNTO`** · **`EE`** · `IC-LO` · `IC-HI` · **`N`** · `CV` · `VEREDICTO-CV` | el árbitro, su error estándar de diseño y su IC |
| **C · diseño** | `N-ESTRATOS` · `N-UPM` · `N-ESTRATOS-UPM-UNICA` · `METODO-IC` · `PERFIL-DISENO` | el conteo real de estratos y UPM, los singleton, y el perfil observado de las llaves opacas |
| **D · secundario homologado** | `N-U1` · `MASA-FAC-DEL-U1` · `P-C1-U1` · `EE-C1-U1` · `IC-LO-C1-U1` · `IC-HI-C1-U1` · `IC-BOOT-LO-C1-U1` · `IC-BOOT-HI-C1-U1` · `P-C2-U1` · `EE-C2-U1` · `IC-BOOT-LO-C2-U1` · `IC-BOOT-HI-C2-U1` · `DELTA-C2-C1` · `N-ESTRATOS-UPM-UNICA-U1` | el punto de serie y su gemelo en la partición GEN1, con los dos métodos de IC |
| **E · estado** | **`ESTADO`** | `CALCULADO` o el motivo exacto de abstención (§3.5) |

**Ningún `RESULT` de esta familia se rotula causal**, y ninguno se emite como porcentaje: todos los puntos son proporciones en `[0,1]` con su dirección de escala escrita en la unidad.

### 5.3 · Por qué el medidor es nuevo y qué se reutiliza

`D-14` manda no duplicar lo que ya existe. Lo que **se reutiliza, sin envolver ni copiar**: `tests/svystat.py:prop_ultimate_cluster` (la varianza), `tests/payload_resolver.py` (la resolución de payload, vía `corrida0`), `tools/corrida0.py` (`preflight`/`run`/`verify`/`registro`), `codificacion-R-v1_0.tsv` (la codificación), y el vocabulario de identificadores de `tools/arbitra_gen2.py`.

Lo que **no** se reutiliza es la **ruta de cálculo** de `tools/arbitra_gen2.py`, por dos razones que se escriben antes de correr:

1. Su `medir()` delega en `arbitra.calcula_desde_tabla` — la aritmética GEN1. Un control positivo contra el JSON GEN1 producido por el **mismo código** sobre el **mismo archivo** no verifica nada: coincide por construcción. El encargo pide correr de 0 y el control existe para tener valor probatorio.
2. Su `spec_de_celda()` emite **cuatro** `RESULT` (`PUNTO`, `EE`, `N`, `ESTADO`) y ningún conteo de embudo. `P2` de este encargo pide el embudo contado paso a paso por ola. La spec que emite no alcanza para lo que se pidió.

Los tres `medidor.py` son **byte-idénticos**: todo lo específico de la ola (miembro del ZIP, `id` de payload, tipos declarados) entra por `contrato["parametros"]`. Que sus tres `script_blob_sha256` coincidan en los tres `sello.json` **es la prueba mecánica de que las tres olas corrieron exactamente el mismo código**, y es la razón de que se depositen tres copias en vez de un archivo compartido: cada corrida se sella con su propio script dentro de su propio directorio.

---

## 6 · Ramas pre-declaradas — escritas ANTES del dato

### 6.1 · Control positivo externo contra GEN1 — **después de sellar, y sólo entonces**

Lo corre `forense/prereg-caja/R-ENVIPE-SERIE-control-gen1.py`, **después** de que `corrida0 verify` cierre las tres corridas. El medidor no participa: no abre los JSON de GEN1 y no recibe sus valores. El script compara `RESULT-R-<C>-PUNTO` contra el campo `R` de `forense/prereg-duelo-v2/corridas-R/<C>.json`, **sobre el punto y no sobre el IC** — el bootstrap de GEN1 no fijó semilla comparable, así que los extremos no se comparan.

Tres ramas, cada una con su consecuencia escrita:

- **`REPRODUCE`** si `|Δ| ≤ 1.0e-9`. Lectura: un medidor escrito de cero desde `codificacion-R-v1_0.tsv` reconstruye el punto GEN1 al bit. El control positivo **pasa** y la cadena `E.2` queda montada sobre la misma cantidad que el duelo ya usa.
- **`REPRODUCE-CON-TOLERANCIA`** si `1.0e-9 < |Δ| ≤ 1.0e-6`. Lectura: misma cantidad, distinto orden de suma en `float64`. También pasa, y se dice cuál de las dos es.
- **`NO-REPRODUCE`** si `|Δ| > 1.0e-6`. **Esto NO invalida la corrida, NO autoriza tocar el medidor y NO cambia el estimando.** Se reporta el delta **con signo** junto al embudo completo de esa ola, y se abre `NC` con el sucesor: reconciliar el universo GEN1 contra el de `codificacion-R-v1_0.tsv`. Los candidatos conocidos, escritos ahora para que no se inventen después: (a) GEN1 pudo exigir `BP1_20 = 2` explícitamente y esta spec no; (b) GEN1 pudo excluir el código `09` del denominador; (c) GEN1 pudo restringir `BPCOD`. `N-INCONSISTENTES-BP1-20`, `N-BP1-23-09` y las dos particiones de `BPCOD` del bloque A están en el contrato **precisamente** para que esa reconciliación se haga con cifras de esta corrida y no con conjeturas.
- **`NO-COMPARABLE`** si la celda salió `NO-ESTIMABLE` por cualquiera de las guardias de §3.5, o si el JSON GEN1 no trae `R`.

El veredicto de las tres celdas va en el **primer párrafo** de la nota del lote, sea cual sea.

### 6.2 · Derivaciones de lo ya leído, declaradas para que mesa las descuente

No son pronósticos ciegos y se separan de lo que sí lo es. De `§0.3` se sigue, **por aritmética y no por medición**, que si el medidor implementa `codificacion-R-v1_0.tsv` sin error y GEN1 implementó lo mismo, `REPRODUCE` es lo esperable — el control mide si **ambas** premisas se cumplen, no si el número es cierto. Lo que **no** se sigue de nada leído: el embudo entero, `p(C1,U1)` y `p(C2,U1)` en las tres olas, el `DELTA-C2-C1` de cada ola, el `CV` de cada `R`, el número de estratos con UPM única, el perfil real de las llaves de diseño, y la forma de la serie.

### 6.3 · Lo que ninguna rama puede hacer

Ninguna rama de §6.1 cambia `C_R`, `U_R`, el ponderador ni el diseño. Ninguna autoriza a re-correr con otra codificación «a ver si ahora sí». **El primer resultado que produzca este procedimiento es el que se reporta**, y una discrepancia es un hallazgo con embudo, no un motivo de ajuste.

---

## 7 · Límites declarados (van también en la nota)

### 7.1 · La serie es descriptiva y le falta un año
La serie que este lote puede armar con la ola 2025 cubre los años de delito **2020 · 2022 · 2023 · 2024** y **le falta 2021** (`envipe2022_csv`, no medida aquí). Cuatro puntos con un hueco no son una tendencia estimada: se publican como cuatro cantidades fechadas. **Ninguna transferencia, ninguna estabilidad temporal y ninguna extrapolación se adjudican aquí** — la tesis del duelo temporal se contrata en `F5`.

### 7.2 · La serie completa espera al trío DBF
Las olas 2012–2020 viven en payloads DBF y son **encargo hermano** (`GEN2-R-SERIE-DBF`), gateado al merge de éste. Hasta que corran, cualquier lectura de forma sobre la serie es sobre **cuatro** puntos, no sobre trece.

### 7.3 · Primario y secundario nunca se comparan entre sí
`A-bis.4`, ya escrito en §3.3. Son universos distintos en la misma corrida.

### 7.4 · Lo que queda fuera y no se declara cubierto
`envipe2022_csv` (ENVIPE 2022, delitos de 2021) **no se mide**: no es una de las tres plazas que la demanda declara, y meterla sería trabajo fuera de perímetro. La ola 2025 **no se re-mide**: su punto se **lee** del `CALC-ENVIPE-0001` ya sellado, y si esa lectura no fuera posible la serie se publica con tres puntos y se dice.

### 7.5 · Ninguna adopción
Ningún `RESULT` de esta familia se cita en `milpa/tramite.yaml`, `milpa/procedencia.yaml`, `milpa/src/celdas.py` ni en el catálogo de momentos — que son las **cuatro** clases que el registro reconoce como consumidor. El consumidor natural de estos tres `R` es `forense/prereg-duelo-v2/marco-M-sorteado-v1_3.tsv:<celda>:R`, y **qué `R` consume el duelo lo adopta mesa por lote (`F3`)**, no este acto. Se registra como `NO-CORRIDO`, no como cobertura.

### 7.6 · Causalidad
Ningún `RESULT` se rotula causal. «Miedo/desconfianza como razón principal» es lo que la persona **declaró**, no una causa medida de la no-denuncia.

---

## 8 · Congelamiento

Esta spec se congela en el **COMMIT-1** de `ACTO GEN2-R-SERIE-CSV`, junto con los tres `data/corrida0/CALC-R-CIV-M-{10,12,13}/{spec.md, spec.yaml, medidor.py}` y con `forense/prereg-caja/R-ENVIPE-SERIE-control-gen1.py`, **antes de abrir un solo byte de microdato**. El inventario exacto de lo abierto hasta aquí, y nada más, está en §0.4.

> **El primer resultado que produzca este procedimiento es el que se reporta.**
