# GEN2-EMISOR-ESTADO-1 · nota de cierre

**Acto:** `forense/encargos/2026-09-17-GEN2-EMISOR-ESTADO-1.md` (archivado
verbatim por A.3) · **base:** `1a6a530` · **entorno:** nube, `cloud_default`,
corpus `data/raw` NO montado (0 archivos examinados), red no sondeada — este
acto no abre microdato ni toca red: lee dos YAML versionados.

**El encargo se redactó contra `0189562` y `main` se movió 6 commits.** Se
fusionó `origin/main` en el arranque (0.a) y TODO lo que sigue está
re-derivado contra `1a6a530`. Las tres cifras que el encargo declaraba en su
A.8 se re-verificaron y siguen siendo las mismas: `copiada verbatim` → 12,
`^ *escala:` → 3, y las 15 `RES-*` sin escala son exactamente las que el
encargo nombra.

---

## P1 · Censo de identidad emisor ↔ árbitro

**Tabla:** `forense/notas/2026-09-16-GEN2-EMISOR-ESTADO-1-censo.tsv`
(97 filas, una por celda del emisor con contraparte candidata en el árbitro).

| veredicto | celdas | % |
|---|---:|---:|
| `IDENTICO` | 89 | 91.8% |
| `INDEPENDIENTE` | 3 | 3.1% |
| `SIN-CONTRAPARTE` | 5 | 5.2% |
| `MISMO-INSTRUMENTO-OTRA-OLA` | 0 | 0.0% |

Por entrada `_ejes_` (las 5 `segmentacion_ejes_*` del emisor):

| entrada | IDENTICO | SIN-CONTRAPARTE |
|---|---:|---:|
| `segmentacion_ejes_encig2025` (`tramite.yaml:437`) | 10 | 0 |
| `segmentacion_ejes_envipe2025` (`:537`) | 13 | 0 |
| `segmentacion_ejes_enif2024` (`:708`) | 32 | 0 |
| `segmentacion_ejes_eder2017_enadid2023` (`:1047`) | 4 | 4 |
| `segmentacion_ejes_enut2024` (`:1106`) | 10 | 0 |
| **total ejes** | **69** | **4** |

Las 24 celdas restantes del censo son nacionales (bloques `enmienda_*`):
20 `IDENTICO`, 3 `INDEPENDIENTE`, 1 `SIN-CONTRAPARTE`.

### Cómo se resolvió cada contraparte (y un defecto que vale la pena decir)

**Las citas `origen:` del emisor están DESFASADAS.** Los once `origen:` que
apuntan al árbitro lo hacen por RANGO DE LÍNEA, y el árbitro se movió desde
que se escribieron. Ejemplo comprobable: `tramite.yaml:441` cita
`tramite-ola5-propuesta-v0.yaml:1347-1418
(tramite.gobierno_digital.util_sin_coercion_ejes_encig2025)`, pero hoy la
línea 1347 del árbitro es un bloque de coeficientes de panel, y ese id vive
en la línea 1600. Igual `:114`, que cita `107-138` y hoy ahí está
`familia.corresidencia.adulto_familiar`. **El censo no usa el rango de línea
en ningún caso**: resuelve por id citado entre paréntesis, por bloque
anidado nombrado, o por el id de la regla base. La columna del resumen dice
cuál se usó en cada una de las 14 entradas.

Dos resoluciones merecen constar por nombre, porque no salen de una cita:

* `familia.union.libre / segmentacion_ejes_eder2017_enadid2023` → árbitro
  `familia.union.libre_ejes_eder2017`, por prefijo de id. Sus 4 celdas de
  cohorte EDER son `IDENTICO`; las 4 del eje ENADID 2023 son
  `SIN-CONTRAPARTE` — ese eje es del emisor y no está en el árbitro.
* `familia.cuidado.recae_mujeres_40mas / segmentacion_ejes_enut2024` →
  árbitro `familia.cuidado.reparto_mujeres40_ejes_enut2024`, **alias
  declarado**: no comparten prefijo ni hay cita, pero las 10 celdas
  etiquetadas coinciden en el valor exacto, 10 de 10. No es adivinar la
  contraparte: es haberla medido. Queda escrito como alias único y
  explícito, no como regla general.

**`(complemento)`**: donde el árbitro asienta `p` y el emisor asienta `1-p`
para la conducta complementaria, la columna `p_arbitro` sale marcada así y el
veredicto es `IDENTICO`. Son el mismo número medido, y contarlos como
distintos inflaría artificialmente la comparación legítima.

### Refinamiento de NC-0275

NC-0275 registró «5 segmentaciones copiadas + 1 número idéntico + 1 sin
rastro» sobre las 7 ids `_ejes_` del árbitro. El censo por celda lo confirma y
lo afina: de las 5 entradas `_ejes_` del emisor, **4 son copia íntegra**
(encig2025, envipe2025, enif2024, enut2024 — 65 de 65 celdas `IDENTICO`) y la
quinta (eder2017_enadid2023) es **copia parcial**: la mitad EDER es copia, la
mitad ENADID es material propio del emisor. Y el hallazgo se extiende más allá
de los ejes: también **20 de las 24 celdas nacionales** son el árbitro.

### Las 3 celdas `INDEPENDIENTE`, nombradas

Todas en `tramite.mordida.discrecional / enmienda_encuci2020`:

| celda | p_emisor | p_arbitro |
|---|---:|---:|
| `solicitud_o_entrega_mordida_encuci2020` | 0.126006 | 0.125822 |
| `paga_mordida_encuci2020` | 0.126006 | 0.125822 |
| `tramite_normal_encuci2020` | 0.873994 | 0.874178 |

**Advertencia de lectura, sin disfraz:** estas tres NO son «otra fuente». Son
el MISMO instrumento y la MISMA ola (ENCUCI 2020, única ola), con números que
difieren en la cuarta cifra. El vocabulario de cuatro veredictos que mesa
firmó no tiene casilla para «mismo payload, dicotomización distinta», y este
acto no inventa una: las clasifica `INDEPENDIENTE` por descarte y lo declara
aquí. Para el marcador **no** cuentan como comparación legítima; cuentan como
una diferencia de procedimiento sobre un payload común, que es otra cosa.

### Propuesta de marcador (NO se implementa — va a mesa como FP-383)

El marcador por segmento compara M (emisor) contra R (árbitro). El censo dice
qué queda de esa comparación:

**(a) Las celdas `IDENTICO` salen de la comparación y se rotulan «emisor =
árbitro».** Son 89 de 97. Comparar M contra R ahí no mide acuerdo: mide
identidad, y siempre da 1. Es el grado P0 de ADV1-M1 en su forma extrema
—mismo número, no sólo misma encuesta+ola— que el careo ADV1 manda fuera del
marcador, a anexo de plomería
(`forense/CAREO-ADV-DUELO-diseno-v2-2026-08-19.md:34`). El rótulo importa
tanto como la exclusión: una celda excluida sin rótulo se vuelve a incluir en
el siguiente rediseño.

**(b) Donde el emisor venga de una ola anterior del mismo instrumento, M-vs-R
se lee como PERSISTENCIA, no como acuerdo, y se dice** — es el mismo piso b de
la tríada. **En este censo esa categoría está VACÍA: 0 celdas.** No hay ni una
sola celda del emisor que sea una ola anterior de un instrumento que el
árbitro también mida. La regla se propone igual, porque el aparato la va a
necesitar en cuanto entre una ola nueva; hoy no mueve ninguna celda.

**(c) Lo que queda como comparación legítima, contado: 3 celdas de 97
(3.1%), y las tres con la advertencia de arriba** — mismo payload ENCUCI 2020,
dicotomización distinta. Si mesa acepta esa advertencia, la comparación
legítima M-vs-R sobre este perímetro es **0 celdas**.

Esa es la sustancia que va a mesa: **el marcador por segmento, tal como está
planteado, no tiene sobre qué correr en el emisor.** No es que salga débil;
es que el universo comparable es de 3 celdas discutibles o de cero. La
decisión de diseño —rediseñar el marcador por segmento sobre otro universo, o
declarar que el emisor no entra en la competencia— es de dirección, no del
ejecutor. **FP-383.**

**Ninguna cifra nueva.** Cada `p` del censo ya estaba sellado en uno de los dos
YAML. Ninguno de los dos se modificó por P1.

---

## P2 · Escala declarada — N = 11, NC-0276 sigue ABIERTA

`python3 tools/corrida0.py demanda` re-derivado. `escala_legacy`
`NO-DECLARADO` en filas `conducta_p_medido`: **15 → 11.**

**Declaradas (4 de las 15), con la fórmula de la casa:**

| RES | regla | escala escrita |
|---|---|---|
| RES-0057, RES-0058 | `dinero.ahorro.via_informal` (`tramite.yaml:1324`) | `"proporcion ponderada [0,1], ENIF 2024, PERSONA de 18 anios y mas ELEGIDA en TMODULO (ponderador FAC_PER)"` |
| RES-0061, RES-0062 | `civico.protesta.agravio_urbano_encuci2020` (`:1379`) | `"proporcion ponderada [0,1], ENCUCI 2020, PERSONA (ponderador FAC_SEL), condicional a la celda entorno x agravio -- las dos conductas NO suman 1"` |

Las dos son `p ∈ [0,1]` y su origen citado es una proporción ponderada, así
que la fórmula aplica. El segundo lleva la salvedad pegada porque las dos
conductas son condicionales a celdas distintas y **no** son complementarias:
escribir la escala sin decirlo invitaría a leerlas como un par que suma 1.

**Por qué las otras 11 siguen `NO-DECLARADO` (la razón, en una línea cada
una — es la MISMA razón):**

`tools/corrida0.py:282` lee `escala` **al nivel de la REGLA**, no de la
salida: `escala = crudo.get("escala") or (...)`, y en la línea 307 estampa ese
único valor en TODAS las conductas de esa regla. Las 11 restantes viven en
cuatro reglas cuyas salidas **no comparten escala**, así que no hay ninguna
cadena que sea verdadera para todas:

| RES | regla | por qué una sola escala de regla sería falsa |
|---|---|---|
| RES-0003, RES-0004, RES-0005 | `tramite.mordida.discrecional` | tres universos en la misma regla: ASIGNADO 0.62/0.38 sin instrumento, ENCIG 2025 PERSONA 18+ (FAC_P18), ENCUCI 2020 PERSONA condicional a contacto (FAC_SEL) |
| RES-0009, RES-0011, RES-0013, RES-0015 | `tramite.mordida.con_registro` | ASIGNADO 0.88/0.12 sin unidad declarada conviviendo con 8 salidas ENCIG 2025 de unidad TRÁMITE |
| RES-0021, RES-0022 | `tramite.gobierno_digital.util_sin_coercion` | ASIGNADO 0.71/0.29 conviviendo con ENCIG 2025 unidad TRÁMITE (FAC_TRA) |
| RES-0025, RES-0026 | `tramite.evasion_norma` | ASIGNADO 0.66/0.34 conviviendo con ENVIPE 2025 |

La escala de cada una de esas 11 **sí** es determinable desde su `origen`
citado. Lo que no se puede es declararla a la granularidad que el registro
lee sin afirmar, de paso, algo falso sobre sus hermanas. Escribir `escala:`
al nivel de la conducta no sirve hoy: el derivador no la leería, y un campo
que nadie lee es ruido, no declaración. **Arreglarlo es tocar
`tools/corrida0.py`, que está FUERA del perímetro de este acto** («si te
encuentras escribiendo fuera de esta lista, PARA»). Va como **NC-0293**.

**Efecto lateral, dicho:** por ser la escala de nivel regla, las 4 filas
`conducta_p_derivado` hermanas de `dinero.ahorro.via_informal` (RES-0053,
RES-0054, RES-0055, RES-0056) también pasaron de `NO-DECLARADO` a esa escala.
Es verdadera para ellas —mismo instrumento, mismo universo, mismo
ponderador— y ningún `p` cambió. Se deja dicho porque no estaba entre las 15.

**Prohibiciones respetadas (A.16):** el diff de `milpa/tramite.yaml` es de
**+2 líneas y 0 eliminaciones**. Ningún `p`, `tier`, `situacion`, `clase`,
`ic95`, `n`, `ponderador` ni `sha256_payload` se tocó.

---

## Derivado

`data/corrida0/demanda-resultados.tsv` y `demanda-corridas.tsv` re-derivados
por comando. **Nota:** el derivado en `main` venía desfasado de su fuente
antes de este acto — el merge de #834 agregó una celda-D que corre la
numeración `RES-*` desde `RES-0174` y `CORR-*` desde `CORR-0080`. Ese
desfase entra en este commit junto con lo del acto, porque el comando lo
re-deriva entero. **Los 15 ids que este acto toca (RES-0003 … RES-0062) están
por debajo del corte y no se renumeran.**

---

## Suite, y una corrección al propio cierre

`python3 tests/check.py --baseline` → **3 FAIL · 4371 WARN**, **LÍNEA BASE
VERDE**, `exit=0`, `tests/baseline.json` sin tocar. Los 3 `FAIL` son los
congelados (`T06`, `T08`); los 3 `WARN` nuevos frente al cierre de `ADR-533`
son las filas que este acto abre (`FP-383`, `NC-0293`, `NC-0294`).

**La primera cifra que este acto declaró era 4364 y estaba mal, por defecto de
entorno propio.** `ADR-535` se redactó contra una corrida local a la que le
faltaba `jsonschema` —declarada en `requirements.txt`, ausente en este
contenedor—, así que `T38 T-ALTA-RELACION` salía `NO-CORRIDO` y sumaba un
`WARN` que el repo no tiene. CI, con la dependencia instalada, dio **4363** y
`T16` marcó la contradicción: la afirmación era mía y era falsa. Se instaló la
dependencia (`python3 -m pip install jsonschema`), se re-corrió, y la corrida
local ahora **reproduce la de CI cubeta por cubeta** — `T-REPRO` 4100,
`T-NO-CORRIDO` 76, `T10` 65, `T03` 62, `T22` 50, `T-SUCESOR-EXISTE` 6, `T13` 3,
`T-CRON` 1 —, sin `T-ALTA-RELACION`. La cifra de `ADR-535` quedó corregida a
4363.

Vale la pena dejarlo escrito porque es la lección y no la anécdota: **una
corrida a la que le falta una dependencia declarada no es la corrida del
repo**, y `T16` es exactamente el mecanismo que lo atrapa. `tools/entorno.py`
ya reportaba `numpy=AUSENTE pandas=AUSENTE scipy=AUSENTE pyreadstat=AUSENTE` en
el ARRANQUE de este acto; `jsonschema` no está en esa lista de dependencias
materiales, y por eso su ausencia no se vio hasta que CI la contradijo.
**Hallazgo de aparato, no de este acto:** `tools/entorno.py` no censa
`jsonschema` aunque `requirements.txt` la declare y la suite la use.

---

## Colisión de cascada con GEN2-TRAMITE-4 — renumera quien fusiona segundo

La concurrencia que el encargo declaró («en paralelo … GEN2-TRAMITE-4 … quien
fusione después renumera») ocurrió. `GEN2-TRAMITE-4` fusionó primero (PR #848) y
tomó `ADR-534`, `FP-380`/`381`/`382` y `NC-0283`…`NC-0292`. Este acto fusiona
segundo, así que **renumera**, y las cifras anteriores de este cierre quedan
superadas:

| era | es |
|---|---|
| `ADR-534` | **`ADR-535`** |
| `FP-380` | **`FP-383`** |
| `NC-0283` | **`NC-0293`** |
| `NC-0284` | **`NC-0294`** |
| suite `3 FAIL · 4363 WARN` | **`3 FAIL · 4371 WARN`** |

Los cinco conflictos (`gobernanza`, `estado-programa`, `registro-rotulos`,
`firmas-pendientes`, `no-corrido`) se resolvieron **tomando la versión de
`origin/main` como base** y re-insertando encima lo de este acto con los números
nuevos — nunca al revés: nada de `GEN2-TRAMITE-4` se perdió ni se reescribió. Los
tres contadores de ADR se reconciliaron otra vez con
`python3 tools/cierre_acto.py --aplica` (`534 → 535`).

**La cifra de suite de `ADR-534` (GEN2-TRAMITE-4) quedó marcada
`{cita-historica}`**, por la misma razón y con el mismo mecanismo con que este
acto marcó la de `ADR-533` y con que se renumeró a sí mismo: dejó de ser el
estado vigente en cuanto este acto cerró encima. **Su sustancia no se
reescribe** — sólo deja de leerse como estado de hoy. Es lo que `T16` exige y lo
que la regla de la casa manda al que fusiona segundo.

**Lo que NO cambió al renumerar, y es lo que importa:** el censo se re-generó
contra el árbol fusionado y salió **idéntico byte a byte** (97 filas, `IDENTICO`
89, `INDEPENDIENTE` 3, `SIN-CONTRAPARTE` 5) — no depende de nada que trajera
`main`. `escala_legacy` `NO-DECLARADO` sigue en **11**, con los mismos 11 ids.
`milpa/tramite.yaml` sigue en **+2 líneas, 0 eliminaciones** contra `main`, y
**0 de 15 `p` alterados**.
