# Cierre — ACTO MAESTRA33-E14 · EVALUACION-OLA6

Encargo: `forense/encargos/2026-09-01-MAESTRA33-E14-EVALUACION-OLA6.md`
(dirección, maestra-33, 1/sep/2026, `SHA de redacción ee6a8a2`). Ejecutado
con la skill `/acto` de `ADR-237`, entorno **NUBE** (`CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE=cloud_default`
— difiere del `sin_variable` que el paso 4 del ARRANQUE espera para caja;
declarado, sin bloquear: este acto no abre microdato ni corre red contra
INEGI, así que el punto 4 del ARRANQUE se limita a la tercera pata —
`ls data/raw/ 2>/dev/null` → vacío/ausente, corpus compartido no montado,
esperado en nube).

## COMPUERTA

`COMPUERTA: E13 fusionado (existe el agregado con L)`.

- **E13 fusionado** — CUMPLE. `git log --oneline origin/main | grep -i E13`
  → `f4d9b7f Merge pull request #403 ... acto/maestra32-e13-marco-m-congela`,
  con `## CONSUMIDO` en `forense/encargos/2026-08-31-MAESTRA32-E13-MARCO-M-CONGELA.md:61-64`
  citando `PR #403` fusionado.
- **"Existe el agregado con L"** — el único candidato es
  `forense/prereg-duelo-v2/scoreboard-v1_1.md` (existe, `sha256 c23238f`,
  31/ago/2026). Verificado en el archivo mismo: línea 41, "**L pendiente:
  11 celdas** — ninguna de las 120 corridas de `corridas-L/` trae un
  `id_celda` del marco-M"; línea 106, "L pendiente: 11 celdas de 11". Su
  tabla marca la columna `L` = `NO` en las 11 filas. **El agregado existe
  como documento, pero trae cero puntos de `L`.**

La compuerta, leída literalmente ("E13 fusionado (existe el agregado con
L)"), se cumple en su primera mitad y es ambigua en la segunda: el
documento existe, los puntos de `L` no. Bajo lectura estricta de existencia
de archivo, CUMPLE — se continúa, declarando la ambigüedad en vez de
usarla para parar sin evidencia (A.13).

## P1 · Universo de candidatos y los tres criterios

**Universo, derivado del propio canon** (`canon/motor-nucleo-medible-v1_0.md`
§1 F-ALCANCE, líneas 22-28): 10 dominios totales. `trámite` es el único
`ACTIVO`. `cívico`, `dinero`, `familia` son candidatos inmediatos con
desenlace ya medido en la capa de coeficientes (no `ACTIVO` todavía, pero
en otra clase que los 6 restantes). **Los 6 dominios no-`ACTIVO` sin
desenlace medido ni candidatura declarada** — el universo que este acto
evalúa — son: **salud, tiempo, cooperación, trabajo, información,
comunicación**.

**Los tres criterios reales de apertura**, sellados en
`canon/motor-nucleo-medible-v1_0.md` §3.a (enmienda E11, `ADR-259`; el
encargo los cita como (i)/(ii)/(iii)):

1. Scoreboard agregado con `L` sobre los 4 dominios `ACTIVO` — "Antes de
   que `L` tenga al menos un agregado publicado, ningún candidato de Ola 6
   puede evaluarse contra este criterio — es lógicamente imposible que se
   cumpla" (§3.a, texto vigente, frase exacta).
2. ≥2 encuestas en corpus + ≥3 reglas candidatas `EXISTE-SATISFACE` por
   `/mapea`, por dominio.
3. Caja libre.

El encargo pide tratar (iii) — que aquí se lee como el agregado L-M-R de
E13 — **como contexto, no como criterio de exclusión** de la tabla: no se
usa para tachar filas de la tabla dominio×criterio. Pero el canon sellado
(§3.a, criterio 1) es explícito en que ese mismo agregado, mientras no
traiga puntos de `L`, hace **lógicamente imposible** que cualquier
candidato cumpla la apertura — no es un criterio más entre tres, es la
precondición de los tres. Se declara la tensión: la tabla de abajo evalúa
(i) y (ii) por dominio sin dejar que (iii) tache filas, tal como el
encargo pide; el veredicto final, sin embargo, no puede ignorar que el
criterio 1 de §3.a sigue sin cumplirse (`L pendiente: 11 celdas de 11`) —
omitirlo sería contradecir el canon que este mismo acto tiene prohibido
reabrir.

### Comandos y hallazgos, por dominio

**(i) ≥2 encuestas en corpus.** Fuente primaria: `data/manifiesto.yaml`
(807 entradas) cruzado, regla por regla, contra
`forense/notas/2026-07-31-inventario-segmentacion.md` (TABLA B — única
fuente que evalúa cobertura Sí/Parcial/No por regla, no solo por nombre de
dominio). Cuenta solo Sí/Parcial:

| Dominio | Encuestas con ≥1 Sí/Parcial | (i) ≥2 |
|---|---|---|
| salud | ENSANUT, ENIGH | **CUMPLE** (2) |
| tiempo | ninguna — las 4 reglas de §3.6 salen "No" en las 8 fuentes, ENUT incluida, búsqueda cerrada | **NO-CUMPLE** (0) |
| cooperación | ENCUCI, ENIF, ENUT | **CUMPLE** (3) |
| trabajo | ENIGH, ENIF, ENOE | **CUMPLE** (3) |
| información | ENIF, ENSANUT | **CUMPLE** (2) |
| comunicación | ENVIPE (1 regla, Parcial) | **NO-CUMPLE** (1) |

Caveat declarado (A.13, no escondido): esta tabla rule-level es del
31/jul/2026; el corpus creció después (ENDUTIH, ENASEM, ENTI, ENADID,
ENBIARE — verificado `grep -c "^- id: endutih\|^- id: enasem"` etc. sobre
`data/manifiesto.yaml`, con conteos 24/6/6/3/4 payloads). Esas fuentes
podrían, por tema, sumar a `tiempo`/`comunicación`/`salud`, pero nadie ha
vuelto a correr el cruce regla-por-regla contra ellas — no se cuenta lo
no verificado.

**(ii) ≥3 reglas candidatas `EXISTE-SATISFACE` por `/mapea`.** El único
`/mapea` corrido hasta hoy (`ACTO MAESTRA33-E7 · MAPEADOR-1`,
`forense/notas/2026-09-01-mapeo-fp190.md`) cubrió candidatas de `FP-190`
— ninguno de los 6 dominios de este acto. `/mapea` **no se ha corrido**
contra ninguno de los 6 candidatos; lo único disponible son veredictos
`EXISTE-SATISFACE` dispersos, subproducto de otro trabajo (barridos de
celdas del corredor E), localizados por
`grep -rn "EXISTE-SATISFACE" . | grep -v .git` filtrado por id `dominio.*`:

| Dominio | `EXISTE-SATISFACE` encontradas | (ii) ≥3 |
|---|---|---|
| salud | 0 | **NO-CUMPLE** |
| tiempo | 0 | **NO-CUMPLE** |
| cooperación | 1 (`forense/notas/2026-08-05-barrido-publico-17-condiciones-no-existe.md:195`) | **NO-CUMPLE** |
| trabajo | 1 (`forense/marco-candidatas-piloto-v1_0.tsv:39`) | **NO-CUMPLE** |
| información | 0 | **NO-CUMPLE** |
| comunicación | 1 (`forense/marco-candidatas-piloto-v1_0.tsv:47`) | **NO-CUMPLE** |

**(iii) Agregado L-M-R de E13 — contexto.** `forense/prereg-duelo-v2/scoreboard-v1_1.md`
existe, cubre las 11 celdas del marco-M congelado por E13, con `M` y `R`
puntuados en 8 de 11 y `L` en 0 de 11. No tacha ninguna fila de esta
tabla (tal como el encargo pide); se retoma en el veredicto porque es,
en canon, el criterio 1 de §3.a — ver arriba.

### Tabla dominio × criterio, veredicto A.4

| Dominio | (i) ≥2 encuestas | (ii) ≥3 EXISTE-SATISFACE | (iii) L-M-R E13 (contexto) | Veredicto |
|---|---|---|---|---|
| salud | CUMPLE (2) | **NO-CUMPLE** (0) | L=0/11, contexto | **NO ABRE** |
| tiempo | **NO-CUMPLE** (0) | **NO-CUMPLE** (0) | L=0/11, contexto | **NO ABRE** |
| cooperación | CUMPLE (3) | **NO-CUMPLE** (1) | L=0/11, contexto | **NO ABRE** |
| trabajo | CUMPLE (3) | **NO-CUMPLE** (1) | L=0/11, contexto | **NO ABRE** |
| información | CUMPLE (2) | **NO-CUMPLE** (0) | L=0/11, contexto | **NO ABRE** |
| comunicación | **NO-CUMPLE** (1) | **NO-CUMPLE** (1) | L=0/11, contexto | **NO ABRE** |

## P2 · Ranking y encargo de fase 1

**Ningún dominio cumple hoy los dos criterios que el encargo pide evaluar
por comando (i)+(ii).** El más cerca por (i) son `salud`/`cooperación`/
`trabajo`/`información` (4 CUMPLE en (i)); ninguno alcanza (ii) — la razón
de fondo, en los cuatro, es la misma: `/mapea` nunca se ha corrido contra
sus reglas del `modelo-decision-v4_0`, así que el conteo real de
candidatas `EXISTE-SATISFACE` es 0 o 1, subproducto accidental de otro
trabajo, no el resultado de una búsqueda dirigida.

Ranking por cercanía (encuestas ya en corpus, reglas por mapear):

1. **trabajo** — (i) CUMPLE (3 encuestas), (ii) 1/3, `/mapea` sin correr.
2. **cooperación** — (i) CUMPLE (3 encuestas), (ii) 1/3, `/mapea` sin correr.
3. **salud** — (i) CUMPLE (2 encuestas), (ii) 0/3, `/mapea` sin correr.
4. **información** — (i) CUMPLE (2 encuestas), (ii) 0/3, `/mapea` sin correr.
5. **comunicación** — (i) NO-CUMPLE (1 encuesta), (ii) 1/3.
6. **tiempo** — (i) NO-CUMPLE (0 encuestas), (ii) 0/3 — búsqueda de
   encuestas ya cerrada sin resultado (§3.6, 31/jul/2026).

**No se redacta `REGLAS-OLA6-FASE1`.** El encargo pide ese borrador "para
el primero que cumpla" — ninguno cumple. Lo que falta, por dominio, y a
qué fila de adquisición se manda:

- **trabajo / cooperación** (los dos mejor posicionados): falta correr
  `/mapea` con ≥3 formulaciones sobre las reglas de `trabajo` (§3.2) y
  `cooperación` (§3.4) de `modelo-decision-v4_0.md`, contando candidatas
  `EXISTE-SATISFACE` reales — no heredadas de otro barrido. No es una
  fila de adquisición de dato nuevo: es trabajo de mapeo sobre corpus ya
  existente. Se enruta como tarea de dirección, no a
  `data/cola-adquisicion-v1_0.tsv`.
- **salud / información**: mismo faltante de `/mapea` dirigido, más
  verificar si `ENSANUT`/`ENASEM`/`ENDUTIH` (crecidas en el corpus después
  del 31/jul) cubren, regla por regla, alguna de sus reglas — hoy sin
  verificar.
- **comunicación**: falta una segunda encuesta con cobertura verificada
  regla-por-regla (hoy solo `ENVIPE`, `Parcial`, 1 regla) — candidata
  temática: `ENDUTIH` (en corpus, sin cruce regla-por-regla corrido). Se
  enruta como tarea de mapeo, no de adquisición (el payload ya está).
- **tiempo**: única fila con faltante real de dato — la búsqueda de
  encuesta quedó cerrada en 0/8 fuentes, incluida `ENUT`. Es la única de
  las seis que calificaría para `data/cola-adquisicion-v1_0.tsv` si mesa
  decide reabrir la búsqueda; no se agrega fila nueva en este acto —
  fuera del perímetro (CONTADOR: cero, evaluación).

Y, sobre todo lo anterior: aunque alguno de los seis alcanzara (i)+(ii)
mañana, el criterio 1 de §3.a (agregado con `L`) sigue en `L pendiente:
11 celdas de 11` — "lógicamente imposible" de cumplir per canon hasta que
exista al menos un punto de `L`. Ningún dominio de Ola 6 puede abrir
hasta que ese agregado tenga aunque sea un punto de `L`, con
independencia de (i)/(ii).

## P3 · FP-220 resuelta

Firma de mesa (2/sep/2026, verbatim): "no vamos a esperar a esa fecha" —
mesa no espera al vencimiento del 15/sep para la primera evaluación.
`forense/firmas-pendientes.tsv` `FP-220` (`EVALUACION-OLA6`) pasa de
`ABIERTA` a **`EJECUTADA`**, con `ejecutada_en` = este acto, fecha real
**2026-09-01** (no la de vencimiento). Veredicto que resuelve: **ningún
dominio abre hoy** — cero de seis cumplen (i)+(ii), y el criterio 1 de
§3.a (agregado con `L`) sigue sin al menos un punto de `L`, lo que hace
"lógicamente imposible" cualquier apertura mientras eso no cambie. La
resolución de `FP-220` es informativa, tal como su propia fila declara
("dirección corre la evaluación, no mesa; no abre ningún dominio por sí
sola") — coincide con "LO QUE NO HACE" del encargo.

## CONTADOR

Cero: ningún dominio abierto (`milpa/tramite.yaml` sin diff), ninguna
regla cargada, ninguna medición corrida, `/mapea` no invocado contra los
6 candidatos (evaluado su ausencia, no ejecutado — correrlo es parte de
lo que falta, declarado en P2, no de este acto). Declarado desde el
encargo.

## Lo que este acto NO hizo

No abrió ningún dominio de Ola 6; no cargó ninguna regla; no midió nada;
no corrió `/mapea` (evaluó que nunca se corrió contra estos 6 dominios,
que es distinto de correrlo); no tocó `scoreboard-v1_1.md`,
`corridas-L/`, `corridas-M/`, `corridas-R/`, ni `milpa/tramite.yaml`.
