# PREDICCIÓN 2024 · adjudicación guardada · spec v1.1

Sucede a `DIN-CREDITO-PREDICCION-2024-ADJUDICACION-spec-v1_0.md`
(sha256 `01a384aa16985328d3b8e310108209730bafe6ce52d11d48d27dcfa6b577ec78`,
sellado en `#987`/COMMIT-1, intacto en `origin/main`, no editado). §§0-5 de
aquí abajo son copia verbatim de v1.0 — ningún renglón de §0-5 cambia
entre versiones (D-15); v1.1 sólo AÑADE §6, escrito por
ACTO GEN2-DIN-CREDITO-PREDICCION-2024-COMMIT-2-3 (22/sep/2026, CAJA),
`commit_3a`, ANTES de que `commit_2` abra `enif2024_csv`.

El primer resultado que produzca este procedimiento es el que se reporta.

ACTO GEN2-DIN-CREDITO-PREDICCION-2024-COMMIT-1 (21/sep/2026, CAJA), pieza
P2 (segunda mitad — la primera, emisiones, está en
`CALC-DIN-CREDITO-PREDICCION-2024-EMISIONES-0001`, COMMIT-1+2 ya sellados
en este mismo acto). CALC:
`CALC-DIN-CREDITO-PREDICCION-2024-ADJUDICACION-0001`. Encargo archivado por
A.3 en `forense/encargos/2026-09-21-GEN2-DIN-CREDITO-PREDICCION-2024-COMMIT-1.md`
(sha256 `b3c62b4a7ed4bf65175c795fdd462379811554b8f0a99d7b65fce8d0da90c72b`).

**CONGELADO SIN CORRER (a la fecha de v1.0).** Este CALC no tenía
`ejecucion.json` ni `resultados.json` al cierre de COMMIT-1, y no los
tendrá hasta COMMIT-2/3 — F3 de la cabecera del encargo: «quien congela no
ejecuta el COMMIT-2/3». El código de `medidor.py` SÍ se probó,
exhaustivamente, sobre un ZIP sintético fabricado por
`tests/test_din_credito_prediccion_2024_adjudicacion.py` — nunca sobre
`data/raw/enif2024_csv.zip` real. `python3 tools/corrida0.py preflight`
sobre este CALC es seguro (verifica sha256 de archivos, no abre filas,
A.7); `python3 tools/corrida0.py run` sobre este CALC **no se ejecutó en
COMMIT-1** — esa fue la compuerta hasta este acto (COMMIT-2-3).

## 0 · Qué congela esta pieza y qué NO

Congela: (1) la lista blanca de conductas autorizadas a abrirse
(`CONDUCTAS_AUTORIZADAS`, idéntica a `ENTERING` de -EMISIONES-0001 — las
9 conductas del encargo §1); (2) el mapa de columnas 2021→2024
(`COLUMNA_2024`, §1 de aquí abajo, derivado del descriptor); (3) la
guardia de una variable (`abre_conducta_2024`, §2); (4) la extracción y
estimación de las 16 celdas por conducta (`medir()`, §3), con el MISMO
marco de réplicas (`_cells`/`_estimate` importados por bytes de
`CALC-PISOS-ENIF2021-EJES-0003`, 10 000 réplicas `PCG64(42)`) que toda la
serie histórica.

**NO congela la regla de adjudicación (a la fecha de v1.0; fijada ahora en
§6 de v1.1).** El encargo mismo lo dice (§3): «C2 no existe hasta abrir
los marginales… C2 se compone dentro del COMMIT-3». Comparar el marginal
real (que este CALC extraería en COMMIT-2) contra las emisiones ya
selladas (`-EMISIONES-0001`, `PERSISTENCIA`/`TENDENCIA-2`/`TENDENCIA-3`/
`TENDENCIA-SERIE`, escala logit analítica, sin réplicas bootstrap) con un
veredicto tipo `VENCE-RETADOR`/`PROPUESTA-CON-RESERVA`/`NADIE-VENCE`
(v2.16 §4) exige una regla de incertidumbre sobre la DIFERENCIA de dos
cantidades — y `tools/duelo/cruces_familia.py::adjudica()`, la
implementación de referencia de este proyecto para esa regla, está
construida sobre réplicas bootstrap por celda (que esta serie de pisos
nunca tuvo: usa propagación analítica en logit desde el IC95 sellado, spec
de -EMISIONES §3). Forzar el contrato de `adjudica()` aquí sin réplicas
sería inventar una compatibilidad que no existe. La regla se diseña en
COMMIT-3, con las dos cosas ya abiertas y la decisión (bootstrap sintético
desde el SE analítico, o una regla puramente analítica sobre la
diferencia) tomada con las cifras reales delante, no antes.

## 1 · Códigos desde el descriptor (A.15) — sin abrir microdato

Leído: `data/raw/enif_2024_fd.xlsx` (hoja `TMODULO`, hasta fila 1579; hoja
`TSDEM`) y, dentro de `enif2024_csv.zip` (manifiesto, sha256
`a3507b4038888247f565f1640a718ef552bb8fc363378e3372a5bf2796bb2e4c`):
`conjunto_de_datos_tmodulo_enif_2024/diccionario_de_datos/diccionario_datos_tmodulo_enif2024.csv`
(399 filas: nombre de campo, nemónico, catálogo, rango de claves — nunca
`conjunto_de_datos/*.csv`), los catálogos
`catalogos/{niv,gra,p6_16,p3_10}.csv`, y la primera línea (encabezado de
columnas, no datos) de `conjunto_de_datos_tmodulo_enif2024.csv` — un
encabezado es la lista de nombres de columna, no una fila de respuesta.

**Hallazgo (nemónico desplazado, A.15): 2024 renombró y reordenó variables
de crédito respecto de 2021** — verificado campo por campo, no inferido
del nombre:

| rol | 2021 (`#943`) | 2024 (este descriptor) | verificado contra |
|---|---|---|---|
| tenencia por producto | `P6_2_1..9` | `p6_2_1..9` | mismos códigos 1/2 (diccionario fila `p6_2_*`) |
| atraso por producto | `P6_4_1..9` | `p6_3_1..9` | `data/credito-comparabilidad-texto-v1_1.tsv` fila K6·2024: «P6_3_1..P6_3_9 (6.3)» |
| informal (K3) | `P6_1_1..5` | `p6_1_1..5` | mismos códigos 1/2, mismo orden (caja/empeño/conocidos/familiares/otro) |
| alguna vez tuvo (base K4) | `P6_14` | `p6_13` | comparabilidad K4·2024: «base … P6_13 = 2» |
| motivo nunca tuvo (K4) | `P6_15` | `p6_14` | comparabilidad K4·2024: «P6_14 (6.14)» — **mismo nemónico que 2021 usaba para OTRA pregunta**: el número solo no basta, A.15 |
| rechazo de solicitud (K5) | `P6_17` (códigos 1/2/3) | `p6_16` (códigos 1/2/3, catálogo `p6_16.csv` verificado idéntico) | comparabilidad K5·2024 = MISMO-INSTRUMENTO |
| edad | `EDAD` (18-96) | `edad_v` (18-95, 97=«97+», 98=«no especificada» — catálogo `edad_v.csv`) | diccionario fila 4 |
| ponderador | `FAC_ELE` | `fac_per` | diccionario, rango `126...106896` |
| escolaridad | `P3_1_1` (código único 0-9) | `niv` + `gra` (nivel 00-11, grado 0-9) | catálogo `niv.csv`: 12 categorías vs. 10 de 2021 — mapa `NIV_A_ESCOLARIDAD` en el código bucketiza 00-02→hasta_primaria, 03→secundaria, 04-07→media_superior, 08-11→superior, 99→indefinido, construido comparando etiqueta por etiqueta con el mapa de `_school()` (`CALC-PISOS-ENIF2021-EJES-0003`), no adivinado |
| formalidad | `P3_10` (1..6) | `p3_10` (1..6, catálogo idéntico) | sin cambio |
| sexo, localidad, diseño | `SEXO`/`TLOC`/`EST_DIS`/`UPM_DIS` | `sexo`/`tloc`/`est_dis`/`upm_dis` | sin cambio salvo minúsculas |

**Estructura del archivo:** a diferencia de 2021 (un solo CSV
`conjunto_de_datos_tmodulo_enif_2021.csv` con todo), 2024 reparte en
CUATRO tablas (`TVIVIENDA`, `THOGAR`, `TSDEM`, `TMODULO`) — pero, medido
contra el encabezado real de `conjunto_de_datos_tmodulo_enif2024.csv`
(398 columnas), **`TMODULO` por sí solo ya trae las 398 columnas
necesarias** (`sexo`, `tloc`, `est_dis`, `upm_dis`, `fac_per`, `edad_v`,
`niv`, `gra`, `p3_10` y todo `p6_*` están ahí) — **no hace falta cruzar
con `TSDEM`** para ninguna de las 9 conductas de este acto, aunque TSDEM
también trae una copia de los demográficos (probablemente para quien
sólo necesita el nivel hogar). Verificado leyendo únicamente la primera
línea (nombres de columna) del CSV real, nunca una fila de respuesta.

**Eje omitido a propósito:** la extracción de este CALC cubre los cinco
«ejes de la casa» que el encargo nombra para cruces (sexo, edad,
escolaridad, localidad, formalidad) — **no** `cuenta` (que sí trae el
piso histórico de -RECORTE1870-0001, pero el encargo no lo pide aquí).

## 2 · La guardia (`abre_conducta_2024`)

Única función del módulo que recibe `inputs["enif2024_csv"]`. Firma:
`abre_conducta_2024(inputs, conducta_id: str, contrato) -> dict`.
`conducta_id` debe ser exactamente uno de los 9 strings de
`CONDUCTAS_AUTORIZADAS` — una lista, `"*"`, `None`, una cadena vacía o
cualquier conducta fuera de esa lista (incluida la propia `K6-PR`, que
esta pieza no adjudica) lanza `ReservaRota` **antes** de tocar el ZIP.
Probado en `tests/test_din_credito_prediccion_2024_adjudicacion.py` con
una ruta de archivo inexistente: si la guardia fallara, el código
reventaría con `FileNotFoundError`, no con `ReservaRota` — el test
distingue las dos cosas.

Dentro de la guardia, sólo se piden las columnas que esa conducta
necesita (§1 de aquí, tabla) — nunca las 398 columnas de `TMODULO`. El
marco se recorta a `EDAD` (`edad_v`) en `[18,70]`, idéntico al recorte de
`CALC-DIN-CREDITO-PISOS-ENIF2021-RECORTE1870-0001` (P0-a de este mismo
acto), para que un futuro COMMIT-2 mida sobre el mismo universo que toda
la serie 2012-2021-2024.

## 3 · Estimación (`medir()`)

Recorre las 9 conductas autorizadas, una llamada guardada a
`abre_conducta_2024` por conducta, y estima 16 celdas
(`nacional` + 2 sexo + 4 edad + 4 escolaridad + 2 localidad + 2
formalidad + 1 universo-trabaja) con `_cells`/`_estimate` de
`CALC-PISOS-ENIF2021-EJES-0003` (importado por bytes) — 10 000 réplicas
`PCG64(42)`, la misma semilla que toda la serie. La dicotomización por
conducta (`_desenlace`) es la MISMA lógica que `#943`/-RECORTE1870-0001
(K1: tenedor de algún producto; K2-*: producto específico; K3: informal
de algún tipo; K4A/K4B: motivo entre quien nunca tuvo; K5: rechazo;
K6-P-TENEDORES: atraso entre tenedores) sobre las columnas YA TRADUCIDAS
por `COLUMNA_2024` — no una lógica nueva, la misma con nombres 2024.

**Probado sobre sintético (D-22):** 1 200 filas inventadas con la forma
exacta de `TMODULO` 2024 (columnas, tipos, saltos de la sección 6);
`medir()` corre sin reventar, emite 9 × 16 × 6 = 864 campos de celda +
18 de diagnóstico = 882 ids, ninguno NaN/inf. **No hay oro**: no existe
ningún «2024 tal como si fuera la ola nueva» que reproducir — 2024 ES la
ola nueva, reservada; el oro de esta familia de código ya se pagó en
-RECORTE1870-0001 (P0-a) y -EMISIONES (P3), que reusan la misma
maquinaria de `_cells`/`_estimate` sobre datos que sí se pudieron abrir.

## 4 · `commit_3a` previsto (a la fecha de v1.0; HECHO en §6 de v1.1)

Cuando la reserva de crédito 2024 se levante (mesa, o el código
pre-registrado de un acto sucesor): `corrida0 run` sobre este CALC
extrae las 9×16 celdas reales; un commit posterior en la MISMA sesión de
ese COMMIT-2, antes de derivar cualquier R, escribe en este `spec.yaml`
la regla de adjudicación decidida (§0) y corre `preflight` de nuevo antes
del COMMIT-3 que adjudica. Ningún otro renglón de este spec ni del
código cambia entre COMMIT-1 y ese momento — si algo más cambia, es una
spec nueva, no una continuación.

## 5 · Lo que esta spec no hace (a la fecha de v1.0)

No abre ENIF 2024 (COMMIT-1 no lo ejecutó); no adjudicaba; no componía
C2; no editaba `#943`, `-RECORTE1870-0001`, `-EMISIONES-0001` ni ningún
CALC sellado; no adoptaba. (§6 de v1.1 es la única adición: sigue sin
adoptar, sin editar ningún CALC sellado.)

## 6 · `commit_3a` — regla de adjudicación fijada (ACTO GEN2-DIN-CREDITO-PREDICCION-2024-COMMIT-2-3, CAJA, 22/sep/2026)

Fijada ANTES de que este CALC (`commit_2`) abra `enif2024_csv`. Ninguna
cifra de la sección de crédito de ENIF 2024 se leyó para decidir esta
regla — se decide sólo con lo ya sellado de `-EMISIONES-0001`
(`resultados.json` sha256
`aa0db17c79581516fc326a4728f1b6969c75e8e837e350168771614db3a008cd`) y el
propio `medir()` de este CALC (aún sin correr al escribir esto).

**Método decidido (FP-260921-GEN2-DIN-CREDITO-PREDICCION-2024-COMMIT-1-7866-01-02,
resuelta por dirección con recomendación, confirmada por mesa 22/sep/2026):
bootstrap sintético desde el SE analítico.** Ninguno de los dos lados de
la comparación expone réplicas: R (este CALC, `_estimate` de
`CALC-PISOS-ENIF2021-EJES-0003`, líneas 57-94) sólo declara punto + IC
percentil 2.5/97.5; las emisiones (`-EMISIONES-0001`) sólo declaran punto
+ IC analítico en logit (`tools/encig_origen_movil.py::predice`). Se
fabrican 10 000 réplicas SINTÉTICAS para cada cantidad (R y cada
contendiente) por separado, MUTUAMENTE INDEPENDIENTES entre sí (son
muestras independientes: 2024 vs. la combinación de olas 2012-2021), con
la misma familia de funciones que ya usa esta serie
(`tools/encig_origen_movil.py::_logit/_expit/_ee_logit`, `Z95=1.959964`):

```
SE = _ee_logit(IC-LO, IC-HI)                    # mismo SE que ya reportó cada punto sellado
z_1..z_10000 ~ N(0,1)                           # numpy.random.Generator(numpy.random.PCG64(20260922))
réplica_b = _expit(_logit(P) + SE · z_b)
```

Celda con `IC-LO<=0` o `IC-HI>=1` (logit indefinido) o `P` en {0,1} →
`CELDA-RARA-LOGIT-INDEFINIDO`, excluida de esa comparación (misma
convención que `-EMISIONES-0001` §2); celda sin R o sin candidato →
`SIN-R`/`SIN-CANDIDATO`, excluida y declarada, nunca imputada con 0.

**Orden de consumo de la semilla** (determinista, fijado aquí antes de
abrir el dato, para que el flujo de números aleatorios no dependa de qué
resulte habilitado en R): un único
`numpy.random.Generator(numpy.random.PCG64(20260922))`, consumido en el
orden `ENTERING` de `-EMISIONES-0001` (K1, K2-DEPARTAMENTAL, K2-NOMINA,
K2-AUTOMOTRIZ, K3, K4A-AUTOEXCLUSION, K4B-OFERTA, K5, K6-P-TENEDORES) ×
las 16 celdas que mide este CALC en el orden de `medir()` (§3 de aquí
arriba: nacional, sexo-1, sexo-2, edad-18-29/30-44/45-59/60-mas,
escolaridad-hasta_primaria/secundaria/media_superior/superior,
localidad-menor_de_15000/15000_y_mas, formalidad-sin_seguridad_social/con_seguridad_social,
universo-trabaja) × (R, PERSISTENCIA, TENDENCIA-2, TENDENCIA-3,
TENDENCIA-SERIE) en ese orden, **10 000 draws por cantidad siempre**
(aunque esa cantidad no exista para esa celda — se consumen y se
descartan, para que el consumo de semilla no dependa del dato real).

**Comparación** (piso = PERSISTENCIA, retador = cada TENDENCIA-X
habilitada, v2.16 §4), por conducta, sobre las celdas puntuadas (con R y
ambos contendientes no-raros):

```
error_piso(b, celda)    = 100 · |réplica_persistencia(b, celda) − réplica_R(b, celda)|
error_retador(b, celda) = 100 · |réplica_tendencia-X(b, celda) − réplica_R(b, celda)|
MAE_piso(b)    = media sobre celdas puntuadas de error_piso(b, ·)
MAE_retador(b) = media sobre celdas puntuadas de error_retador(b, ·)
ΔMAE(b) = MAE_piso(b) − MAE_retador(b)        (positivo = el retador tiene menor error)
```

Punto: `ΔMAE = MAE_piso(punto) − MAE_retador(punto)` con los `P` sellados
directamente (no la media de las réplicas). IC95 = percentil [2.5, 97.5]
de `ΔMAE(b)` sobre las 10 000 réplicas.

Si una conducta tiene más de una TENDENCIA-X habilitada (T2, T3, T-SERIE
pueden coexistir con >= 3 olas previas), el retador que se enfrenta a
PERSISTENCIA en el ΔMAE primario es el de MENOR MAE en el punto (mismo
criterio "MEJOR-CONTENDIENTE" que ya usó `-EMISIONES-0001` para el
backtest); las otras tendencias habilitadas se reportan (MAE, cobertura)
pero no entran al ΔMAE primario de esa conducta.

**Umbral de materialidad: NO SE FIJA, a propósito**, heredando la postura
ya declarada en `-EMISIONES-0001` (spec.md §4 de esa pieza: "inventar una
constante que nadie va a usar para decidir nada es justo lo que v2.16 §2
prohíbe"). Vocabulario de veredicto ALCANZABLE en este acto (v2.16 §4):
`NADIE-VENCE` (IC95 de ΔMAE incluye 0) y `PROPUESTA-CON-RESERVA` (IC95
excluye 0). `VENCE-RETADOR` queda declarado INALCANZABLE-POR-DISEÑO en
este acto — no hay umbral que un IC pueda despejar; si mesa quiere que
sea alcanzable, fija el umbral en un acto propio, no aquí, no con el dato
ya abierto.

**Cobertura** (v2.16 §4, «R dentro del IC del candidato»): por candidato
habilitado y por conducta, proporción de celdas puntuadas donde el punto
observado de R (no una réplica) cae dentro de `[IC-LO, IC-HI]` del
candidato, con intervalo binomial (Wilson) sobre esa proporción.
Declarado explícitamente: las celdas de una misma conducta comparten la
MISMA muestra de personas de ENIF 2024 — no son observaciones
independientes entre sí (v2.16 §4); la cobertura se reporta como
descriptiva, con esa salvedad, nunca como si fuera n independientes.

**K4(b) y K5 junto a K1-K3** (encargo §1/§5, «oferta antes que
preferencia», v2.16 §3): el reporte por conducta de K1, K2-*, K3 se
publica junto con el marginal de K4B-OFERTA y K5 de la MISMA celda (mismo
eje, misma categoría) — ninguna de las dos entra al cómputo de ΔMAE de
K1/K2/K3 (cada conducta adjudica contra su propio piso); es contexto para
no leer «no tiene crédito formal» como «no lo prefiere».

**Celdas fuera de este CALC:** `-EMISIONES-0001` predijo también
`CUENTA-CON-CUENTA`/`CUENTA-SIN-CUENTA` (eje `cuenta`, 2 de 18 celdas);
este CALC (§1 de aquí arriba) no mide ese eje — se declara
`SIN-R-EJE-CUENTA-OMITIDO-POR-DISENO` para esas 2 celdas × 9 conductas,
«nadie ocupó la fila» (v2.16 §2), no una derrota ni un NO-CONSTRUIBLE.

Escrito por la sesión de COMMIT-2-3 (ACTO
GEN2-DIN-CREDITO-PREDICCION-2024-COMMIT-2-3), commit propio, antes de que
`commit_2` abra el ZIP. `preflight` corre de nuevo después de este commit
y debe salir VERDE antes de seguir (spec.yaml `commit_3a`).
