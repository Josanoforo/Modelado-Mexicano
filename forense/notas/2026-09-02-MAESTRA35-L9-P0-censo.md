# `ACTO MAESTRA35-L9 · REGLAS-ACTIVOS-L3` — `P0` · censo `A.4`

> | | |
> |---|---|
> | **ACTO** | `MAESTRA35-L9 · REGLAS-ACTIVOS-L3` |
> | **ENCARGO** | `forense/encargos/2026-09-02-MAESTRA35-L9-REGLAS-ACTIVOS-L3.md` (A.3), SHA de redacción `9cbd8d8` |
> | **ENTORNO** | UBUNTU con corpus. `CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE` = `sin_variable` · `https://www.inegi.org.mx/` → `200` · `ls data/raw/ \| head -1` → `2005trim1_csv.zip` (ese `ls` examinó **374** entradas, no cero) |
> | **QUÉ ES** | El censo `A.4` de las cuatro piezas, **antes** de medir. Denominadores y marginales; ningún cruce contra el desenlace. |
> | **ARTEFACTO** | `data/l9-censo-a4-v1_0.tsv` (10 filas × 16 columnas) |
> | **VERIFICAS ASÍ** | `python3 tools/medidor_clientelismo_lapop.py --censo`, `… medidor_protesta_lapop.py --censo`, `… medidor_entitlement.py --censo`, `… medidor_seguro_deposito_enif24.py --censo` |

---

## §0 · Contaminación declarada (`ADR-46`), antes de la spec y no después

Este acto **abre estructura y marginales** de cinco payloads: LAPOP México
2006/2019/2021/2023, ENCUCI 2020 (sección 6) y ENIF 2024 (`TMODULO`). El
encargo lo ordena así — `P0` es censo *antes* de medir —, de modo que la spec
de `COMMIT-1` se congela **con la estructura ya vista**. Lo que esta sesión
leyó, dicho con precisión y errando por sobre-declarar:

- **Nombres de variable, etiquetas de variable y catálogos de valor** de las
  cuatro olas LAPOP, de `AP6_9`/`AP6_10`/`AP6_11` de ENCUCI y de
  `P5_20`/`P5_23`/`P5_24_*` de ENIF.
- **Marginales univariados** de esas variables, incluidos los del desenlace.
- **Denominadores de los ejes**: `ur × vic1ext` (2019), `mexwf1_19 × countfair3`
  (2023), `AP6_10`, y la cobertura de `P5_23` sobre el universo de `P5_20`.
- **Lo que NO se leyó, y por eso sigue disponible como primer resultado:**
  ninguna tabla cruzada del **desenlace contra el moderador**. No se calculó
  `P(votó | ofrecieron)`, ni `P(derecho | beneficiario)`, ni
  `P(desconfianza | conoce protección)`, ni ninguna proporción ponderada.

Esa frontera es la que hace que el pre-registro de `COMMIT-1` valga algo: fija
qué se estima **sabiendo qué variables hay** pero **sin saber hacia dónde
apunta ninguna**.

## §1 · Verificación de identidad de los payloads

Los cinco payloads se verificaron por **sha256 contra `data/manifiesto.yaml`**,
uno por uno, no por nombre de archivo. Los cinco **COINCIDEN**.

| payload_id | sha256 (prefijo) | coincide |
|---|---|---|
| `mexico_lapop_americasbarometer_2019_v1_0_w` | `c88f79eb…` | sí |
| `mex_2023_lapop_americasbarometer_v1_0_w` | `4a9410a5…` | sí |
| `mex_2021_lapop_americasbarometer_v1_2_w` | `153fb0f8…` | sí |
| `518939279mexico_lapop_final_2006_data_set_092906` | `e4262100…` | sí |
| `encuci2020_bd_dbf` | `0414fd59…` | sí |
| `enif_2024_enif_2024_bd_csv` | `00e4b0b4…` | sí |

**Hallazgo de infraestructura, no de dato.** Las cuatro olas LAPOP **no están
en `data/raw`**: el manifiesto las declara bajo `raiz: descargas_mx`, que
`forense/notas/2026-08-06-map1b-censo-raices.md:68` resuelve a
`/mnt/c/Users/PC0/Descargas MX`. `data/raices.local.yaml` es **gitignorada**, así
que un worktree nuevo nace sin ella y cualquier `find` sobre `data/raw` declara
`NO-ENCONTRADO` **en falso** — exactamente la clase de negativo que `A.13`
persigue. Los cuatro medidores de este acto **PARAN con un mensaje explícito**
cuando la raíz no está configurada, en vez de reportar el payload como ausente.

## §2 · La premisa del encargo, verificada contra el árbol

| lo que el encargo declara | verificado contra `9cbd8d8` | resultado |
|---|---|---|
| las 6 ids existen en `canon/modelo-decision-v4_0.md` §7 | `grep -c -F` por id | **cierto** (6/6) |
| motor: ninguna cargada | `grep -c -F` sobre `milpa/tramite.yaml` | **cierto** (0/6) |
| propuesta: 0 entradas de estas familias | `grep -c` sobre `milpa/tramite-ola5-propuesta-v0.yaml` | **cierto** (0) |
| `grep -c -i lapop data/inventario-reactivos-v1_2.tsv` → 0 | re-corrido **con control positivo** | **cierto** — el archivo sí se lee (5 819 líneas ENIF, 458 ENCUCI), es UTF-8 limpio (32 091 658 bytes), y `lapop`/`barometer`/`latinobar` dan **0** contados en Python, no sólo con `grep` |

El control positivo importa porque `grep` en esta caja es `ugrep -I` y descarta
en silencio archivos con un byte no-UTF8: un `0` sin control positivo no es un
cero.

**Lo que el encargo suponía y el árbol corrige — la ola principal.** El encargo
plantea LAPOP **2023** como ola principal de la pieza (a) y 2019/2021 como
serie. Contra el dato es al revés: **la batería clientelar sólo existe en
2019**. Ver §3.

## §3 · Pieza (a) — `R7.7`, y el muro entre `R7.3`/`R7.6` y la dádiva

`R7.7 · civico.clientelismo.turnout_no_vote_choice` `[MEDIA]`, verbatim del
modelo (`canon/modelo-decision-v4_0.md:555`):

> **SI** hay dádiva o transferencia **Y** el partido puede monitorear al
> **broker** (no al votante) **ENTONCES** compra **ASISTENCIA a las urnas** de
> simpatizantes, **no la elección de voto** — PORQUE *turnout buying* ≠
> *vote-choice buying* — `[MEDIA]`.

**LAPOP 2019 la satisface**: `clien1na` («Le ofrecieron un beneficio por su voto
en la última elección generales», 1 578 válidos, 271 sí / 1 307 no), `vb2`
(asistencia, 1 576) y `vb3n` (elección de voto, 1 035). Es la ola con la batería
completa: `clien1n`, `clien1na`, `clien4a`, `clien4b`.

**El muro, que es el hallazgo negativo central de este censo.** `R7.3`
(`agencia_con_secreto`) y `R7.6` (`clientelar_si_observable`) piden el moderador
de **secreto/monitoreo percibido del voto** cruzado con la dádiva sobre la
**misma persona**. En el corpus completo eso **no existe**:

- **2019** trae `clien1n`/`clien1na`/`clien4a`/`clien4b` y **cero** ítems de
  secreto u observación del voto (búsqueda por etiqueta sobre las 221 columnas).
- **2023** trae `countfair3` («Percepción de una votación secreta») y **cero**
  ítems `clien*` (195 columnas).
- **2021** no trae ni lo uno ni lo otro: es la ola reducida de COVID (262
  columnas, sin `clien*`, `prot3`, `vb2`, `vb3n`, `countfair3` ni `mexwf1_19`),
  y además su `upm` está degenerada — 2 998 valores distintos para 2 998 filas,
  una UPM por persona.
- **2006** no trae `clien*`.

→ **`EXISTE-NO-SATISFACE`** para el cruce *dádiva × secreto*. Se cierra aquí y
**no tumba el lote**.

**Lo que sí queda en pie para `R7.3`/`R7.6`, y por qué es otra cosa.** El
antecedente de `R7.3` no es la dádiva sino la **transferencia** («SI hay
transferencia directa universal no condicionada…»), y de eso 2023 sí tiene
`mexwf1_19` («Recibir ayuda —dinero en efectivo, alimentos, productos básicos—
del gobierno», 1 615 válidos, 363 sí). Cruzado con `countfair3` (1 542) contra
`vb20` (intención de voto en la próxima presidencial, 1 414) el par `R7.3`/`R7.6`
**sí es estimable sobre la misma persona y en el mismo momento**. Se registra
como pieza **(a-bis)**.

Una advertencia de diseño que la spec hereda: el desenlace **tiene que ser
`vb20`**, no `vb3n`. En la ola 2023 `vb3n` pregunta por la presidencial de
**2018** — cinco años antes de que se midiera el moderador. Un moderador de 2023
sobre un desenlace de 2018 no es un cruce, es un anacronismo.

## §4 · Piezas (b), (c), (d)

**(b) `R7.4 · civico.protesta.agravio_urbano` `[MEDIA-FUERTE]`** —
`prot3` × `ur` × `vic1ext` en LAPOP 2019. `EXISTE-SATISFACE`, con una reserva
que la spec convierte en guardia: `prot3` tiene **112** sí sobre 1 576, y los
denominadores del eje son urbano-víctima **455**, urbano-no-víctima **807**,
rural-víctima **65**, rural-no-víctima **252**. La celda rural-víctima tiene
numerador esperado ≈ 5. Que la variable exista no es que la `n` alcance.

**2006 como contraste de serie: `EXISTE-NO-SATISFACE`.** `PROT1`/`PROT2` no son
el mismo instrumento que `prot3`: son escala de frecuencia de tres niveles
(*Algunas veces / Casi nunca / Nunca*) y `PROT2` está **gateada** dentro de
`PROT1` (209 válidos de 1 560). Además el archivo de 2006 no trae columna de
ponderador. No hay serie comparable; no se fuerza.

**(c) `R7.8 · civico.transferencia.entitlement_derecho` `[HIPÓTESIS]`** — el
encargo previó que ningún instrumento preguntara la percepción y dejó abierto el
`EXISTE-NO-SATISFACE`. **ENCUCI 2020 la pregunta, literal.** `AP6_9`:

> 6.9 ¿Cuál de las siguientes frases se acerca más a lo que usted piensa
> respecto a los programas sociales (como becas para el bienestar, jóvenes
> construyendo el futuro, pensión universal para personas adultas mayores,
> tandas para el bienestar, apoyos al campo, etc.)?
> **1** = Los programas sociales son una **ayuda que da el gobierno** ·
> **2** = Los programas sociales son un **derecho de los ciudadanos** ·
> 3 = Ninguna · 9 = No sabe / no responde

Cobertura 21 519 / 21 519 (100 %). El antecedente lo da `AP6_10` (beneficiario en
12 meses: 5 789 sí / 15 676 no), y `AP6_11` («¿A usted le pidieron algo —dinero,
documentos personales, favores o que votara por algún partido— a cambio de
entrar o permanecer en algún programa?», gateada dentro de `AP6_10 = 1`, n = 5 789)
entra como eje secundario. Diseño `FAC_SEL` × `EST_DIS` (281) × `UPM_DIS` (3 096);
el join contra `ENCUCI_2020_SD.dbf` por `ID_PER` es **total**: 21 519 emparejadas,
**0** sin par. → **`EXISTE-SATISFACE`**. Es la percepción que `MAESTRA33-E18` no
encontró en ENASEM, y estaba en un instrumento que sí estaba en el corpus.

**(d) `R1.5 · dinero.ahorro.seguro_deposito_atenua_aversion` `[MEDIA]`** — ENIF
2024. El moderador ya venía nombrado en el propio modelo
(`canon/modelo-decision-v4_0.md:283`: ENIF `P5_23`/`P5_24` mide conocimiento de la
protección IPAB); lo que aquel pasaje descartó fue usarlo como medida de
*aversión*, no como moderador. Aquí se usa como lo que es.

La guardia que decide si la spec sale degenerada se corrió **antes** de
congelarla: `P5_23` se pregunta al **universo completo** (13 502, 100 %) y `P5_20`
a los **2 970** sin cuenta — y **2 970 de 2 970** (100 %) tienen moderador válido.
El cruce **no** es degenerado. → **`EXISTE-SATISFACE`**.

**Sensibilidad IPAB, y un hallazgo que vale por sí mismo: `EXISTE-NO-SATISFACE`.**
`P5_24_*` está anidada dentro del «Sí» de `P5_23`, así que sólo 426 de los 2 970
sin cuenta la traen (14.3 %). Y el marginal dice algo más fuerte que la
insuficiencia de `n`: de los **4 136** que afirman saber que sus ahorros están
protegidos, **3 148 contestan «no sabe»** cuando se les pide nombrar la
institución, y sólo **362 en toda la muestra** (2.7 %) nombran al **IPAB**.
*Creer que hay protección* no es *que el seguro sea visible* — y «visible» es
justo la palabra del `SI` de `R1.5`.

## §5 · Reproducción

```
python3 tools/medidor_clientelismo_lapop.py --censo
python3 tools/medidor_protesta_lapop.py     --censo
python3 tools/medidor_entitlement.py        --censo
python3 tools/medidor_seguro_deposito_enif24.py --censo
```

Requieren `data/raices.local.yaml` (gitignorada) con
`descargas_mx: /mnt/c/Users/PC0/Descargas MX`. Sin ella los medidores **PARAN**
con el mensaje de `A.13` en vez de reportar payload ausente.

## §6 · Contador de este commit

Reglas del modelo con dato: **0** — este commit no mide nada. Celdas con IC:
**0**. Piezas cerradas en `P0` por `EXISTE-NO-SATISFACE`: **3** (el cruce
dádiva × secreto; la serie 2006 de protesta; la sensibilidad IPAB). Piezas que
pasan a `COMMIT-1`: **5** — (a) `R7.7`, (a-bis) `R7.3` y `R7.6`, (b) `R7.4`,
(c) `R7.8`, (d) `R1.5`: **seis reglas del modelo**, las seis que el encargo
nombra.
