# Nota de cierre · ACTO GEN2-TUBERIA-CANAL-PUBLICACION-1

22/sep/2026. Entorno **NUBE** (`cloud_default`, red DENEGADA-POR-POLITICA,
corpus no montado, 0 archivos examinados). SHA de redacción `3f48be30`,
base `3f48be3` (HEAD real de `origin/main` al arrancar, coincide). Sonnet 5
(el encargo sugería Opus; el modelo servido cambió a mitad de sesión — se
declara, no afecta la ejecución). ADR de raíz:
`ADR-260922-GEN2-TUBERIA-CANAL-PUBLICACION-1-7d98-01` (0-bis `7d986cea`).

## Qué se hizo

**P1 · `tools/lote_desde_asientos.py`.** Deriva el lote mecánicamente del
`git diff` de `forense/replay-evidencia.tsv` entre dos refs: toma las
líneas AÑADIDAS, extrae `calc_id`, y filtra a los que tienen `sello.json`
válido (`_verifica_sello() == COINCIDE`) bajo `data/corrida0/<calc_id>/`.
Cero juicio: no decide si un asiento debe entrar, solo lee cuáles entraron
en el push. `tests/test_lote_desde_asientos.py`: parser del diff (líneas
añadidas vs. quitadas, cabecera repetida) + extremo a extremo con git DE
VERDAD en un repo temporal (un CALC con sello entra, uno sin sello se
descarta con razón A.13, una edición en su sitio —no asiento nuevo— no
entra).

**P2 · el job (`verify.yml`).** Paso nuevo en el job de push a `main`,
después de la re-derivación existente, con el MISMO guard anti-loop
`[deriva]` — pero leído de `github.event.head_commit.message`, no de
`git log -1` local (el paso de re-derivación de arriba ya pudo avanzar el
checkout con un commit `[deriva]` propio antes de que este paso corra).
`github.event.before` es la base real del diff. Si el lote no está vacío:
`registro --verifica --escribe --lote <lote>` y commit `[deriva]` con la
lista en el mensaje; si el guardia `REPLAY-PISADO` para, el paso (y el
job) fallan con la salida cruda — sin `--force`, sin `--excluye`.

**Probado en rama, con git real, en un clon desechable (no en `main`,
compuerta §8 del encargo):**
- *Camino feliz*: partiendo de un estado catch-up (sin drift), un push
  sintético con un asiento nuevo de un CALC fixture (`sello.json` +
  sidecar sellado con la CLI real) produce `ESCRITO corridas.tsv: 309
  filas` y un commit `aa3ee5f [deriva] registro --lote
  CALC-FIXTURE-CANAL-0002` con la fila publicada.
- *Camino de guardia*: el MISMO mecanismo contra el estado REAL de `main`
  hoy (sin catch-up) dispara `REPLAY-PISADO (NC-0094)` sobre **13
  corridas AJENAS** (26 campos) cuyo veredicto en `replay-evidencia.tsv`
  ya no coincide con lo publicado en `corridas.tsv` — drift preexistente,
  no producido por este acto (medido también sin lote: `SECO
  corridas.tsv: 61+/38−`, el mismo orden de magnitud que el `60+/38-` de
  la sesión de arranque, antes de tocar el árbol). El job no fuerza: falla
  con la lista completa. **Esto es exactamente lo que §3/§6 del encargo
  anticipaba** ("si resulta falso... el job no fuerza: falla en voz alta
  con la lista y ese es el hallazgo").

**P3 · `.gitattributes` + `tests/test_tuberia_ids_union.py` caso I.**
`forense/replay-evidencia.tsv`, `forense/analisis/ci-guardias/
censo-tests.tsv` y `data/corrida0/decisiones.tsv` entran a `merge=union`.
T46 (salto de línea final) y T50 (líneas repetidas ≥200 caracteres), ya
GENÉRICAS sobre todo archivo declarado `union`, los cubren sin tocar
`tests/check.py` — verificado con `git check-attr merge` sobre los tres.
Caso I, tres sub-casos por archivo, MEDIDOS con git real (no supuestos):
  - I1: dos ramas apendican filas DISTINTAS → fusiona sin conflicto, las
    dos sobreviven.
  - I2: dos ramas apendican la fila IDÉNTICA sobre una base que termina en
    `\n` → **NO duplica**. Hallazgo honesto: el riesgo real de duplicación
    que el propio `.gitattributes` documenta (línea COMPARTIDA de la base
    deformada) es la FALTA de salto final (caso B3, ya cubierto por T46),
    no el append+append de contenido idéntico — git ya trata una adición
    idéntica en ambos lados como un solo cambio.
  - I3: una línea ≥200 caracteres YA repetida en el archivo (por cualquier
    mecanismo) → T50 la atrapa, con el vocabulario exacto que P3 pedía.

## Premisas caídas

Ninguna tocó qué se mide ni una firma de mesa. La única premisa que no se
sostuvo tal cual (§6 del encargo: "si `--lote` re-proyecta todo y el
guardia para por corridas ajenas sin asiento, el job no fuerza") resultó
CIERTA en la práctica actual del repo — el drift preexistente (13
corridas) hace que el guardia SÍ vaya a disparar en el primer push real.
No es un PARO: el objetivo (a) — que el mecanismo exista, funcione y
falle en voz alta sin forzar — se cumplió y se probó. Es logística de
estado del repo, no del procedimiento.

**Pregunta a mesa** (§6, LATITUD — se sigue con lo demás mientras
responde, D-19), asentada como
`FP-260922-GEN2-TUBERIA-CANAL-PUBLICACION-1-7d98-01`: ¿se añade una
bandera de lote **estricto** en `corrida0.py` (recomendado por dirección
en el encargo, ≤30 líneas, con test) que restrinja la escritura sólo a
las filas del lote, para que el drift preexistente no bloquee cada push?
¿O el job sigue registrando todo lo que tenga asiento y mesa hace un
catch-up explícito primero (`--lote` con los 13 ids listados en el log de
la prueba de este acto) antes del primer push real?

## P4 · Primer push real

**NO ejecutado desde este acto** (D-19: no es de este acto forzar un
catch-up sin que mesa decida entre las dos opciones de arriba, y este PR
no toca `data/corrida0/corridas.tsv`/`resultados.tsv`/`usos.tsv` —
respeta la firma de mesa 21/sep §2(2), "los derivados no viajan en los
PR"). El mecanismo existe y está probado; las corridas que "sólo esperaban
el canal" (22 CALC selladas sin fila al redactar el encargo original, más
las que las NC de abajo describen) siguen "selladas en disco, no
registradas" hasta que: (a) mesa fusiona este PR, Y (b) o bien un push
posterior trae un asiento nuevo que no choque con el drift, o bien mesa
autoriza el catch-up explícito. Ver `## NO-CORRIDO` del encargo archivado.

`NC-0257`/`NC-0284`/`NC-0329` (citadas en el encargo P4) ya estaban
**CERRADA** al re-verificar (por otra vía, antes de este acto) — premisa
de logística del encargo, no un hallazgo de contenido; no se re-tocan
(E.1: lo ya cerrado no se reescribe). Las cuatro `NO-CORRIDO`
`DIFERIDO-A: acto TUBERIA` de #1008/#1012/#1005/#1003
(`NC-260922-GEN2-DIN-CREDITO-PISOS-1870-RUN-1-009f-01`,
`NC-260922-GEN2-DIN-CREDITO-K2-HISTORIA-RUN-1-ef6f-01`,
`NC-260922-GEN2-DIN-CREDITO-ESCOLARIDAD-2-0af9-01`,
`NC-260922-GEN2-DIN-LOTE-C2-RESTRINGIDO-1-4e12-01`) se ENMENDARON con
fecha: el mecanismo que esperaban ya existe y está probado (PR de este
acto), pero **NO se cierran** — sus filas siguen sin publicarse en
`corridas.tsv`/`resultados.tsv` hasta el primer push real. Cerrarlas
ahora sería falso: la corrida sigue "sellada en disco, no registrada".

## Suite

`python3 tests/check.py --rapido` → **VERDE, 0 FAIL** (295 WARN, ninguno
nuevo de este acto salvo el T-NO-CORRIDO esperado de las 4 filas
enmendadas), tras un hallazgo de `T25` (rótulo pelado en el cuerpo sellado
del encargo — su §9 cita a cuatro actos hermanos en vuelo por su letra y
número, no un rótulo propio de este acto; censado en
`_T25_ARCHIVOS_CONOCIDOS` sin tocar el cuerpo).

## Perímetro respetado

Propio: `.github/workflows/verify.yml` (un paso), `tools/
lote_desde_asientos.py` (nuevo), `.gitattributes` (tres líneas),
`tests/test_tuberia_ids_union.py` (caso I), `tests/
test_lote_desde_asientos.py` (nuevo), `tests/check.py` (censo T25),
`forense/no-corrido.tsv` (cuatro enmiendas), `forense/
firmas-pendientes.tsv` (una fila nueva, la pregunta a mesa), esta entrada
de gobernanza, `canon/L0/ADR-260922-GEN2-TUBERIA-CANAL-PUBLICACION-1-
7d98-01.md`, `canon/registro-rotulos.tsv`. Ajeno NO tocado:
`tools/corrida0.py` (la bandera de lote estricto queda pendiente de
mesa), ningún CALC, ninguna vista a mano (`corridas.tsv`/`resultados.tsv`/
`usos.tsv` no viajan en este PR).

## CONTADOR

Cero mediciones (como declaraba la cabecera del encargo). Al primer push
real posterior con un asiento nuevo que no choque con el drift —o al
catch-up que mesa autorice—, `corridas.tsv` gana las filas de los CALC
correspondientes; ese es el evento que mueve el contador, no este acto.
No adopta.

**El PR no se fusiona en este acto: mesa fusiona.**
