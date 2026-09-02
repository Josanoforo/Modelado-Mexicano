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
