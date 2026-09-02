# `ACTO MAESTRA34-L4` · P3 · SPEC CONGELADA — participación municipal ante una elección local concurrente

**Commit 1 de dos** (Bloque B-bis / A-bis, `instrucciones-proyecto-v2_12.md`). Este
archivo contiene **sólo** las premisas (§0) y la especificación (§1). No contiene
ningún resultado, ninguna cifra municipal y ninguna estimación. El commit 2 le
añade las secciones §2 en adelante y **no edita nada de lo que hay aquí**.

Encargo: `forense/encargos/2026-09-01-MAESTRA34-L4-CIVICA-Y-CORPUS.md` (dirección,
1/sep/2026, SHA de redacción `a39073d`), archivado por A.3 en el primer commit de
este acto. Entorno UBUNTU. Regla del modelo bajo prueba: **`R7.1`** — *peso
percibido del acto → participación diferencial* (`canon/modelo-decision-v4_0.md`
L265, tier `[FUERTE]`, veredicto de Hito D `A` archivado por `ADR-145`).
Necesidad del registro del curador: **`N25`**, que es literalmente `R7.1`
(`data/curacion-registro/necesidad-objeto-modelo.tsv` línea 29).

---

## §0 · Premisas, y qué había visto esta sesión antes de escribir la §1

### 0.1 · El diseño lo fijó mesa, no el ejecutor

La firma **`F232-b`** (mesa, 1/sep/2026, verbatim en el encargo archivado)
adjudica `FP-232` y fija el contraste:

> contraste ENTRE AÑOS — elección local 2023 (no concurrente) vs local 2024
> (concurrente con la federal), mismo estado y mismo municipio, Coahuila y Estado
> de México.

Todos los parámetros de la §1 —unidad, desenlace, universo, contraste principal,
diagnóstico, semilla del bootstrap, escala— **están fijados por el encargo**, no
elegidos aquí. Lo que la §1 añade es la parte mecánica que el encargo no podía
traer porque el dato aún no estaba en el corpus cuando se redactó: en qué fila
vive la cabecera de cada tabla, por qué llave se cruzan los dos años y qué filas
no son municipios. El ejecutor propaga, no decide (`SELLA-3`).

### 0.2 · Declaración de contaminación (`ADR-46`) — se sobre-declara a propósito

`ADR-46` distingue descarga ciega (no contamina) de exploración de estructura
(contamina parcialmente y **debe declararse**). Lo que esta sesión vio antes de
escribir la §1:

**(a) Estructura, abierta deliberadamente en P1 y necesaria para escribir una spec
ejecutable.** Nombres de hoja, fila de la cabecera, nombres de columna, número de
filas y nombres de municipio de las cuatro tablas municipales, más las cabeceras
de las tablas por sección y por casilla y del catálogo de casillas del INE.

**(b) DOS AGREGADOS ESTATALES DE COAHUILA, vistos sin buscarlos.** Al reportar la
estructura de las tablas, una de las sondas de reconocimiento de P1 incluyó en su
descripción las cifras de la **fila de totales estatales**, que esta sesión por
tanto leyó:

- Coahuila 2023, gubernatura: `TOTAL VOTOS` 1 344 882, `Lista Nominal` 2 377 964,
  `% PART` 0.5656 — citado por la sonda desde la fila 46 del propio XLSX.
- Coahuila 2024, ayuntamientos: 1 558 479 votos y 2 410 806 de lista nominal —
  suma cruzada que la sonda declaró, **no** verificada por esta sesión.

Consecuencia honesta, escrita antes de medir: **esta sesión conoce la dirección
del cambio de participación a nivel ESTATAL en Coahuila** antes de congelar la
spec. No la conoce para el Estado de México, no la conoce para ningún municipio
de ninguno de los dos estados, y no conoce ninguna dispersión ni ningún intervalo.
El pre-registro de este acto es, por tanto, **ciego para el Edomex y para todo el
nivel municipal, y NO ciego para el agregado estatal de Coahuila**. Se dice
entero porque el falsador de esta pieza vive en el nivel municipal y en el
intervalo, no en el agregado — pero quien audite esto después tiene derecho a
saberlo sin tener que deducirlo.

**(c) Lo que NO se vio:** ningún valor de `TOTAL_VOTOS` ni de `LISTA_NOMINAL` de
ningún municipio, de ninguno de los dos estados, en ninguno de los dos años;
ninguna participación municipal; ningún dato del Edomex más allá de nombres de
columna, de municipio y conteos de fila.

### 0.3 · Lo que P1 dejó medido y esta spec da por establecido

| hecho | medido por | valor |
|---|---|---|
| municipios de Coahuila con resultado local 2023 y 2024 | P1, `openpyxl` sobre los XLSX | 38 y 38 |
| municipios del Edomex con resultado local 2023 y 2024 | P1, `openpyxl` | 125 y 125 |
| filas no municipales en Coahuila 2023 | P1 | 4 (1 agregada `VMRE_VA_VPPP` + 3 de nota al pie) |
| filas no municipales en Edomex 2023 | P1 | 3 (voto anticipado, prisión preventiva, extranjero) |
| filas no municipales en 2024, ambos estados | P1 | 0 |
| ¿hubo municipios sin comicio local el 2/jun/2024? | P1, sobre la Gaceta del Edomex 28/dic/2023 y el acuerdo `IEC/CG/206/2023` | no se encontró ninguno |

### 0.4 · Confundidor declarado ANTES de medir

**El cargo en disputa no es el mismo en los dos años.** En 2023 la elección local
fue de **gubernatura** en los dos estados; en 2024 fue de **ayuntamiento** (y, en
el Edomex, también diputaciones locales). Un Δ entre esos dos años mezcla, por
construcción:

1. el efecto de **concurrencia** con la elección federal (lo que `F232-b` quiere
   medir),
2. el efecto de la **jerarquía del cargo** en la boleta local (gubernatura pesa
   más que ayuntamiento),
3. todo lo demás que cambia entre 2023 y 2024 (elección presidencial de por
   medio, candidaturas, padrón).

`FP-232` ya lo anticipó al levantar la ambigüedad («carga con todo lo que cambia
entre 2023 y 2024»). Mesa firmó `F232-b` sabiéndolo. **Este acto mide lo que la
firma pide y no puede separar (1) de (2) y (3)**: el diseño no lo permite y no se
va a fingir que sí. Se dice aquí, en el commit de spec, para que la reserva no
parezca una excusa escrita después de ver el número.

### 0.5 · Ciego a corridas

Este acto es **CIEGO a corridas-M/L** (`prereg-duelo-v2`, `scoreboard`,
`agregado`): no se abrió ninguna, no se citará ninguna, y el resultado de P3 no
entra en ninguna. Tampoco carga nada al motor (`milpa/tramite.yaml` intocado): la
entrada va al acumulador de propuesta y el sello es de mesa.

---

## §1 · Especificación congelada

### 1.1 · Unidad de observación

El **municipio**. No la casilla, no la sección, no el distrito. Las tablas por
casilla y por sección adquiridas en P1 se usan sólo como control de reconstrucción
(§1.8), nunca como unidad de la estimación.

### 1.2 · Desenlace

**Participación** = `votos totales / lista nominal`, calculada **por municipio y
por año**, con el numerador y el denominador que publica el propio organismo
electoral local en la misma fila:

| estado | año | archivo (bajo `data/raw/electoral_local_2023_2024/`) | hoja | fila de cabecera | columna municipio | numerador | denominador |
|---|---|---|---|---|---|---|---|
| Coahuila | 2023 | `iec_coahuila_2023/Gubernatura2023_X_Municipio.xlsx` | `XMUNICIPIO` | 6 | `nom_mun` | `TOTAL VOTOS` | `Lista Nominal` |
| Coahuila | 2024 | `iec_coahuila_2024/Ayuntamientos2024_X_Municipio.xlsx` | `XMUNICIPIO` | 6 | `nom_mun` | `TOTAL VOTOS` | `Lista Nominal` |
| Edomex | 2023 | `ieem_edomex_2023/RESULTADOS_DEFINITIVOS_GUBERNATURA_2023_POR_MUNICIPIO.xlsx` | `2023_SEE_GOB_MEX_MUN` | 6 | `MUNICIPIO` (+ `ID_MUNICIPIO`) | `TOTAL_VOTOS` | `LISTA_NOMINAL` |
| Edomex | 2024 | `ieem_edomex_2024/Resultados_definitivos_ayu_municipio.xlsx` | `2024_SEE_AYUN_MEX_MUN` | 8 | `MUNICIPIO` (+ `ID_MUNICIPIO`) | `TOTAL_VOTOS` | `LISTA_NOMINAL` |

**No se recalcula ni se sustituye el denominador.** La lista nominal que se usa es
la que el organismo publica junto al resultado; el catálogo de casillas del INE
(`ine_deoe_2024_pec_ubicacion_casillas_csv`) se adquirió como respaldo y **no
entra** en el cálculo principal.

La columna `% PART` que traen las tablas de Coahuila **no se usa**: se recalcula
el cociente y, como control, se compara contra ella (§1.8).

### 1.3 · Elección de cada año

La elección **local** de mayor jerarquía de la jornada, que es la misma pareja en
los dos estados: **gubernatura en 2023** y **ayuntamiento en 2024**. Las
diputaciones locales de Coahuila 2023 y del Edomex 2024 no entran en el contraste
principal (§1.7 las usa como lectura secundaria en Coahuila, donde existen por
municipio vía casilla).

### 1.4 · Universo

Los municipios de Coahuila y del Estado de México **presentes en los dos años**,
con lista nominal estrictamente positiva en los dos.

- **Exclusión previa, explícita y contada:** las 4 filas no municipales de
  Coahuila 2023 y las 3 del Edomex 2023. Se cuentan y se reportan; no se
  descartan en silencio.
- **Llave de cruce entre años:**
  - Edomex: **`ID_MUNICIPIO`**, nunca el nombre. Medido en P1: en 2024 algunos
    nombres llevan sufijo numérico (`LUVIANOS 18`) y no empatan por texto con los
    de 2023.
  - Coahuila: **nombre normalizado** de `nom_mun` (mayúsculas, sin acentos, sin
    espacios dobles), porque las tablas del IEC no publican clave de municipio
    estable entre años; la columna `No.` no lo es (en 2023 la primera fila de
    datos es la agregada `VMRE_VA_VPPP`).
- Cualquier municipio que no empate se **reporta uno por uno con su nombre**; no
  se rellena, no se imputa y no se descarta callando. El universo efectivo se
  declara como fracción del universo nominal (38 y 125).

### 1.5 · Contraste principal

Δ**ᵢ** = participaciónᵢ,₂₀₂₄ − participaciónᵢ,₂₀₂₃, por municipio *i*, en **puntos
porcentuales**.

Estimador reportado: la **media de Δᵢ sobre el universo conjunto** (Coahuila +
Edomex), sin ponderar por tamaño — la unidad es el municipio, no el elector, y
así lo fija el encargo. Se reporta además la **mediana** como descriptivo.

**IC95 por bootstrap sobre municipios**, tal como el encargo lo fija: se
remuestrean **municipios** con reemplazo (no electores, no casillas), `seed = 42`,
**B = 10 000** réplicas, intervalo por **percentiles 2.5 y 97.5**. `B` no lo fija
el encargo y se congela aquí.

### 1.6 · Diagnóstico

El mismo Δ calculado **por separado para Coahuila y para el Estado de México**,
cada uno con su propio IC95 bootstrap (misma semilla, mismo `B`), y la
**diferencia entre los dos** (Edomex − Coahuila) con su propio IC95 bootstrap
sobre la diferencia de medias. Es diagnóstico, no falsador.

### 1.7 · Robustez y lecturas secundarias

- **Robustez (a) de la firma `F232-a` — `NO-APLICA`.** P1 midió que no hubo, en
  ninguno de los dos estados, municipios sin comicio local el 2/jun/2024: no
  existe la variación dentro de 2024 que esa robustez requiere. Se declara aquí
  para que su ausencia no se lea como omisión.
- **Lectura secundaria 1 — participación FEDERAL 2024 llevada a municipio.** El
  encargo prescribe el crosswalk sección→municipio de 2016
  (`ine_mge_2016_*`, `ACTO MAESTRA34-L3`) para agregar el PREP federal 2024
  (`ine_prep2024_base_datos_20240603_2005_zip`), que trae `SECCION` y
  `LISTA_NOMINAL` pero no municipio. Se ejecuta y se reporta **con el conteo de
  secciones sin correspondencia** (A.13), como lectura secundaria declarada: el
  contraste principal ya no la necesita porque P1 trajo la mitad local de 2024,
  que era justo lo que faltaba cuando el encargo se redactó. Sirve para separar
  «la jornada movió a la gente» de «la boleta local movió a la gente».
- **Lectura secundaria 2 — Coahuila, diputaciones locales 2023.** Se calcula la
  participación municipal de la otra elección de la misma jornada de 2023,
  agregando desde la tabla por casilla, como control de que el Δ de Coahuila no
  depende de haber elegido la gubernatura como cabeza de boleta.

Ninguna de las dos lecturas secundarias puede reemplazar al contraste principal
ni alterar la entrada de §1.10. Si alguna no corre, se dice por qué y se sigue.

### 1.8 · Controles obligatorios (A.13)

1. **Reconstrucción desde casilla.** Para al menos un estado-año, reagregar
   `TOTAL VOTOS` y `Lista Nominal` desde la tabla por casilla y comparar contra la
   tabla por municipio. Se reporta la discrepancia exacta, sea cero o no.
2. **`% PART` publicada vs recalculada** (Coahuila, los dos años): diferencia
   máxima en puntos porcentuales sobre los 38 municipios.
3. **Conteo de lo examinado:** cuántas filas leyó cada archivo, cuántas se
   excluyeron y por qué regla, cuántos municipios entraron al universo.
4. **Rango del desenlace:** ninguna participación puede quedar fuera de
   `(0, 1]`. Si alguna lo hace, es `PARO` y se reporta antes que cualquier Δ.

### 1.9 · Qué significa cada desenlace posible — escrito ANTES de verlo (B-bis)

- **IC95 enteramente por encima de 0** → la participación municipal es mayor en la
  elección local concurrente. `R7.1` recibe una instancia **compatible**, con la
  reserva del §0.4 (no separa concurrencia de jerarquía del cargo).
- **IC95 enteramente por debajo de 0** → la participación municipal es menor en la
  concurrente. Instancia **incómoda** para la lectura ingenua de `R7.1`, y otra
  vez con la reserva del §0.4.
- **IC95 que cruza cero (Δ ≈ 0)** → **la regla queda ACOTADA, no refutada.** Un
  intervalo que cruza cero sobre 163 municipios de dos estados en un solo par de
  años dice que *este* contraste no distingue el efecto, no que el mecanismo de
  `R7.1` no exista. La reserva se escribe en la propia entrada del acumulador. Se
  declara aquí, antes de mirar, para que un Δ pequeño no se convierta después en
  una refutación que el diseño no autoriza.
- En los tres casos la escala es **puntos porcentuales de participación**, y la
  clase es `MEDIDO·Δ` — **NO** una probabilidad. Una regla del motor consume
  probabilidades; ésta no entrega una, y por eso no puede cargarse al motor tal
  cual aunque mesa la firmara.

### 1.10 · Entrada que produce el commit 2

Una sola entrada nueva en `milpa/tramite-ola5-propuesta-v0.yaml`, id
**`civico.participacion.contingente`**, con `clase: "MEDIDO·Δ(puntos porcentuales
de participación)"`, `tier: PENDIENTE-DE-MESA`, `situacion: PENDIENTE-DE-MESA`,
`ic95`, `n`, `universo`, `fuente`, `sha256_payload`, `payload_manifiesto_id`, y la
reserva del §1.9 escrita si el intervalo cruza cero. **No** se toca
`milpa/tramite.yaml`. **No** se carga nada al motor.

### 1.11 · Reproducibilidad

Un solo script nuevo, `tools/mide_participacion_concurrente.py`, determinista
(`seed = 42` fijo en el código, sin `random` sin semilla, sin fecha, sin red), que
lee sólo de `data/raw/electoral_local_2023_2024/` y escribe su salida a `stdout` y
a un JSON. Entra al árbol en el **commit 2**, junto con los resultados, como fija
el patrón de dos commits.

---

**El primer resultado que produzca este procedimiento es el que se reporta.**

---
---

# COMMIT 2 — RESULTADOS

Añadido el 2/sep/2026 por `ACTO MAESTRA34-L4`. **Nada de lo de arriba se ha
editado**: la §0 y la §1 son byte a byte las del commit 1 (`fd54992`), como fija
el patrón de dos commits. Script: `tools/mide_participacion_concurrente.py`,
determinista (`seed = 42`, `B = 10 000`, sin red, sin fecha).

> **El primer resultado que produjo este procedimiento es el que se reporta.** La
> primera corrida completa dio `media Δ = +10.4790 pp`, `IC95 = [+9.6890,
> +11.2652]`. Después de esa corrida se corrigieron **dos defectos del script que
> no tocan el contraste principal**: (i) `py7zr` 1.1.3 no expone `read()`, lo que
> hacía abortar la *lectura secundaria 1* (el script la declaró como no corrida y
> siguió, tal como la §1.7 manda); (ii) la variable de `argparse` se llamaba `a` y
> una de las lecturas la pisaba, lo que rompía sólo la escritura del JSON al
> final, después de imprimir todo. Tras las dos correcciones el contraste
> principal reproduce **exactamente** las mismas cifras — es determinista y no
> depende de ninguna de las dos rutas corregidas.

## §2.1 · Lectura y exclusiones (A.13)

| tabla | hoja | fila de cabecera | `max_row` | municipios | filas excluidas |
|---|---|---|---|---|---|
| Coahuila 2023 gubernatura | `XMUNICIPIO` | 6 | 50 | **38** | 4 |
| Coahuila 2024 ayuntamientos | `XMUNICIPIO` | 6 | 46 | **38** | 0 |
| Edomex 2023 gubernatura | `2023_SEE_GOB_MEX_MUN` | 6 | 134 | **125** | 3 |
| Edomex 2024 ayuntamientos | `2024_SEE_AYUN_MEX_MUN` | 8 | 153 | **125** | 0 |

Las 7 filas excluidas, nombradas una por una (no se descartó nada en silencio):
Coahuila 2023 — `VMRE_VA_VPPP` (fila 7, agregado con `No.`=0) y las tres notas al
pie de las filas 48-50 (`Votación de Mexicanos Residentes en el Extranjero`,
`Votación Anticipada`, `Votación de Presonas en Prsión Preventiva`, con el
*typo* del original). Edomex 2023 — `VOTO ANTICIPADO`, `VOTO DE PERSONAS EN
PRISION PREVENTIVA`, `VOTO EN EL EXTRANJERO` (filas 7-9).

**La exclusión se comprueba, no se supone.** El total estatal que publica el IEC
para 2023 es 1 344 882 votos sobre 2 377 964 de lista nominal; la suma de los 38
municipios da **1 343 764 sobre 2 355 025**. La diferencia —1 118 votos y 22 939
de lista nominal— es exactamente la fila `VMRE_VA_VPPP` que se excluyó. La regla
de exclusión reconstruye la aritmética del propio organismo.

## §2.2 · Universo

**163 municipios de 163 nominales.** Coahuila 38 de 38, Edomex 125 de 125.
Ninguno quedó sólo en un año, ninguno sin denominador. Control de la llave de
Coahuila (que por spec cruza por nombre normalizado): **0 municipios** con nombre
2023 distinto del de 2024.

## §2.3 · Control de rango

**0 municipios** con participación fuera de `(0, 100]` pp, en ninguno de los dos
años. No se disparó el `PARO` de la §1.8.4.

## §2.4 · CONTRASTE PRINCIPAL

Δᵢ = participaciónᵢ,₂₀₂₄ − participaciónᵢ,₂₀₂₃, en puntos porcentuales.

| | |
|---|---|
| n (municipios) | **163** |
| **media Δ** | **+10.4790 pp** |
| mediana Δ | +10.7464 pp |
| desviación estándar | 5.2056 pp |
| **IC95 bootstrap** | **[+9.6890, +11.2652] pp** |
| B / semilla / método | 10 000 · 42 · percentiles 2.5 y 97.5 sobre municipios |
| ¿el IC95 cruza cero? | **NO** |

**La participación municipal es mayor cuando la elección local es concurrente con
la federal.** El intervalo entero está por encima de cero y no lo roza: el
extremo inferior son casi 10 puntos porcentuales.

Reparto: **160 de 163 municipios** tienen Δ positivo. Los 3 negativos son todos
del Edomex y todos pequeños: `LUVIANOS` (−2.775), `AMATEPEC` (−2.152),
`ALMOLOYA DE ALQUISIRAS` (−1.636). El máximo es `ABASOLO`, Coahuila (+22.790).

## §2.5 · Diagnóstico por estado

| estado | n | media Δ | mediana | IC95 |
|---|---|---|---|---|
| Coahuila | 38 | +10.1289 pp | +8.9052 | [+8.5478, +11.8838] |
| Edomex | 125 | +10.5855 pp | +11.0362 | [+9.6889, +11.4965] |
| **Edomex − Coahuila** | — | **+0.4565 pp** | — | **[−1.4331, +2.2600]** |

Los dos estados dan lo mismo dentro del ruido: la diferencia entre ellos **cruza
cero**. El hallazgo no lo produce una entidad sola.

Agregados por estado, derivados de los propios municipios (no de la fila de
totales de nadie): Coahuila 57.0594 % → 64.6456 %; Edomex 50.2408 % → 63.8045 %.

## §2.6 · Control 1 — reconstrucción desde las actas de casilla

| estado-año | actas leídas | municipios comparados | \|Δ votos\| | \|Δ lista nominal\| |
|---|---|---|---|---|
| Coahuila 2023 gubernatura | 4 047 | 38 | **0** | **0** |
| Coahuila 2024 ayuntamientos | 4 156 | 38 | **0** | **0** |

Reagregar acta por acta reproduce **exactamente** la tabla por municipio, en los
dos años, en los 38 municipios, en numerador y denominador. Cero discrepancia, no
"cero aproximado".

## §2.7 · Control 2 — `% PART` publicada vs recalculada

Coahuila, los dos años, 38 municipios cada uno: **diferencia máxima 0.000000 pp**.
El cociente que este acto calcula es el mismo que el organismo publica.

## §2.8 · Lectura secundaria 1 — participación FEDERAL 2024 llevada a municipio

Con el crosswalk sección→municipio de 2016 (`ine_mge_2016_*`, hallado por
`ACTO MAESTRA34-L3`) sobre el PREP presidencial 2024 (corte 03/06/2024 20:05).

| | secciones en el PREP | sin correspondencia en el crosswalk 2016 | municipios emparejados |
|---|---|---|---|
| Coahuila | 1 777 | **138 (7.77 %)** | 38 de 38 |
| Edomex | 6 744 | **406 (6.02 %)** | 125 de 125 |

| contraste | Coahuila | Edomex |
|---|---|---|
| federal 2024 − local 2023 | +7.6560 pp · IC95 [+5.3586, +9.9430] | +9.2557 pp · IC95 [+8.1984, +10.3095] |
| federal 2024 − local 2024 | **−2.4730** pp · IC95 [−4.3549, −0.9268] | **−1.3298** pp · IC95 [−1.8517, −0.8119] |

Dos lecturas, con su reserva:

1. El salto de participación **no** depende de qué boleta se mire: medido contra
   la federal de 2024, el aumento respecto de 2023 sigue ahí (+7.7 y +9.3 pp).
2. Dentro de la **misma jornada** de 2024, la boleta **local** recogió *más*
   votos que la presidencial en estos municipios (−2.5 y −1.3 pp de brecha). No
   se explica por actas faltantes del PREP: en estas dos entidades el corte de
   las 20:05 trae cifra usable en **4 155 de 4 192 actas (99.12 %)** en Coahuila
   y **21 030 de 21 105 (99.64 %)** en el Edomex — muy por encima del 95.24 %
   nacional. **Reserva:** el PREP es conteo preliminar y el resultado local es
   cómputo final (con recuentos), y los universos de casilla y de lista nominal
   no son idénticos entre las dos fuentes. Es una lectura secundaria declarada;
   no la firma nadie aquí.

## §2.9 · Lectura secundaria 2 — Coahuila, diputaciones locales 2023

4 065 actas, 38 municipios emparejados. Δ ayuntamiento 2024 − diputaciones
locales 2023 = **+10.1023 pp**, IC95 [+8.3951, +11.9185] — prácticamente idéntico
al +10.1289 que da contra la gubernatura. **El Δ de Coahuila no es un artefacto
de haber elegido la gubernatura como cabeza de boleta de 2023.**

## §2.10 · Robustez (a) de `F232-a`

`NO-APLICA`, como la §1.7 anticipó: P1 midió que no hubo municipios sin comicio
local el 2/jun/2024 en ninguno de los dos estados.

## §3 · Qué dice y qué no dice este número

**Dice**, con el desenlace que la §1.9 fijó antes de mirar: el `IC95` está
enteramente por encima de cero, luego la participación municipal es **mayor** en
la elección local concurrente, y `R7.1` recibe una **instancia compatible**. La
magnitud es grande —del orden de 10 puntos porcentuales— y homogénea entre los
dos estados.

**No dice** por qué. El confundidor que la §0.4 declaró **antes de medir** sigue
entero: el cargo no es el mismo en los dos años (gubernatura 2023, ayuntamiento
2024), y entre 2023 y 2024 hay además una elección presidencial de por medio,
otras candidaturas y otro padrón. Este diseño **no puede separar** el efecto de
concurrencia del de jerarquía del cargo ni del de calendario. Las dos lecturas
secundarias acotan un poco: la (2) descarta que el resultado dependa de qué
elección de 2023 se tome como base; la (1) muestra que el salto también aparece
contra la boleta federal. Ninguna de las dos convierte esto en una identificación
causal, y este acto no la reclama.

**Lo que se necesitaría para separar los efectos** —y queda nombrado para el acto
sucesor, no rodeado—: variación de concurrencia **dentro** del mismo año y del
mismo cargo, que es justo lo que pedía la spec de
`forense/notas/2026-09-01-MAESTRA33-E18-P3-L1-spec.md` (l. 502-508) y que
`F232-a` fue a buscar sin encontrar en estas dos entidades. Vive en los estados cuyo calendario
local sí se desfasa del federal, o en elecciones extraordinarias.

## §4 · Contaminación, cerrada

La §0.2 declaró que esta sesión había visto los agregados **estatales** de
Coahuila antes de congelar la spec. Medido ahora: ese conocimiento previo cubría
**1 de los 163 municipios · 0**, es decir ninguno; la dirección estatal que la
sesión ya conocía (Coahuila hacia arriba) resultó ser la misma que la del Edomex,
que **no** conocía, y la magnitud del contraste principal la fija el nivel
municipal y el intervalo, que no se conocían. La declaración se mantiene escrita
tal cual: no se borra por haber salido inocua.

## §5 · Entrada al acumulador

`milpa/tramite-ola5-propuesta-v0.yaml`, id `civico.participacion.contingente`,
clase `MEDIDO·Δ(puntos porcentuales de participación)`, `tier:
PENDIENTE-DE-MESA`. **El motor no la carga**: `milpa/tramite.yaml` queda
intocado. El sello es de mesa.
