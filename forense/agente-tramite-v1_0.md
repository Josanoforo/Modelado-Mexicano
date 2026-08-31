# Agente de trámite · v1.0 — runbook de mesa

**P3** de `ACTO MAESTRA33-E1 · AGENTE-TRAMITE-1`
(`forense/encargos/2026-08-31-MAESTRA33-E1-AGENTE-TRAMITE-1.md`, SHA de
redacción `af41796`).

Este archivo es para **mesa**, no para el ejecutor. Dice tres cosas: qué
se congeló (§0), qué se pega en la tarea recurrente de Claude Code (§1),
qué esperar de cada PR y cómo leerlo en dos minutos (§2), y cuándo
retirar la pieza (§3).

---

## §0 · SPEC CONGELADA — COMMIT-1 del acto

Las tres piezas quedan congeladas aquí antes de que se reporte ningún
digesto. **El primer resultado que produzca este procedimiento es el que
se reporta.**

### P1 · `tools/digesto_tramite.py` — el lector

Emite `forense/digesto/DIGESTO-<fecha>.md`. Determinista: misma
`--fecha` y mismo árbol dan la misma salida byte por byte (verificado en
el acto que lo instaura, con dos corridas y `diff`). La única entrada
que no sale del árbol es la fecha, y es argumento explícito.

Cinco secciones, en este orden y sin otras:

- **A** — filas `ABIERTA` de `forense/firmas-pendientes.tsv` con su
  antigüedad contada desde la columna `creado` hasta `--fecha`.
- **B** — resumen de `python3 tests/check.py --baseline`: veredicto
  (`VERDE` / `ROJO` con su número de entradas nuevas), código de salida,
  cifras crudas `N FAIL · M WARN`, y el `HEAD` congelado de
  `tests/baseline.json`. **El veredicto ES el delta**: la suite compara
  entrada por entrada normalizada, no cifra contra cifra, y restar los
  totales crudos daría un número sin significado. Eso se dice en la
  propia salida, para que nadie lo reste.
- **C** — ramas remotas distintas de `main`, con la fuente declarada:
  `git ls-remote --heads origin` (estado vivo) o, si no responde,
  `git for-each-ref refs/remotes/origin` marcado como RESPALDO, que
  refleja el último `fetch` y no el remoto de ahora.
- **D** — encargos sin marca `## CONSUMIDO`, partidos en dos por un
  **piso derivado del árbol** (la fecha del encargo más antiguo que sí
  trae la marca, hoy `2026-08-18`): en o después del piso son
  accionables; antes del piso son **pasivo histórico**, nacidos cuando
  la convención todavía no se practicaba. Ni el digesto ni la skill
  deciden cuál de esos «ya no aplica»: eso es de mesa.
- **E** — contadores derivados por comando, con el comando a la vista:
  reglas y dominios activos de `milpa/tramite.yaml`, ejecutables de
  `milpa/procedencia.yaml`, y puntos por conteo de
  `forense/prereg-duelo-v2/corridas-*/*.json`.

**A.13 en todas partes**: cada negativo declara cuántos archivos examinó
el comando que lo produjo. Un negativo sin conteo no es un negativo.

**Neutralización de marcadores — la parte no obvia.** El digesto vive en
`forense/`, y su nombre cambia cada día. Eso lo mete en el universo que
recorren `T25` (rótulo `M`/`E` pelado) y `T22(b)` (marcadores de ranura
y de decisión sin resolver), y a la vez lo deja fuera de las tres únicas
salidas que esos tests ofrecen — las dos listas de archivos conocidos y
la cita por `dónde` en el tablero —, porque las tres son por ruta o por
basename, y un nombre que cambia cada día no puede estar en ninguna por
adelantado. Así que la garantía viene **por construcción**: P1
neutraliza los dos marcadores en todo texto que copia del árbol, cuenta
las sustituciones en el pie, y re-corre los regex sobre su propia salida
antes de escribir (`--verifica-marcadores`, encendido por defecto);
si algo se coló, **no escribe** y sale con código 2.

No es precaución hipotética. Medido el 31/ago/2026 contra `af41796`: de
las 6 filas `ABIERTA` del tablero, `FP-179` trae cuatro rótulos pelados
en su texto y `FP-190` uno más. Un digesto que los copiara verbatim
rompería `T25` en su primera corrida: el agente de fondo habría nacido
tumbando la suite. La verificación además atrapó dos defectos reales del
propio P1 durante su construcción — la prosa explicativa del digesto
nombraba el marcador, y después nombraba la constante que lo contiene
como subcadena.

Un rótulo pelado se escribe con guion bajo delantero (`_` + rótulo): el
guion bajo está en la clase que el lookbehind del test excluye, el
rótulo real se lee igual, y **no se inventa un prefijo de espacio** —
decidir a qué espacio pertenece un rótulo es de mesa (D-6/ADR-128). El
digesto nunca sustituye a la fuente: cita el `id`, y la fila íntegra
vive en `forense/firmas-pendientes.tsv`.

### P2 · `.claude/commands/tramite.md` — el actor

Arranque ligero (clon, SHA contra `origin/main`, suite en línea base),
corre P1, y redacta **un** PR etiquetado `[TRAMITE]`. Perímetro duro,
cerrado: `forense/firmas-pendientes.tsv` · `forense/digesto/` · marcas
`## CONSUMIDO` en `forense/encargos/` · **nada más**.

Cuatro acciones permitidas, y ninguna otra:

1. Mover a `FIRMADA` una fila cuyo texto **ya porte** firma o enterado
   verbatim de mesa, citando `archivo:línea` de dónde sale.
2. Cerrar recibos con el mismo criterio.
3. Añadir una marca `## CONSUMIDO` faltante, **con su PR**, solo cuando
   la derivación mecánica da exactamente un candidato.
4. Commitear el digesto del día.

Guardrails: **nunca firma ni decide**; **CONTADOR cero, declarado** (es
infraestructura, no mide); **lo que requiera juicio no se ejecuta — va
como fila del digesto**; el PR **no se fusiona solo**.

### P3 · este archivo

Runbook de mesa. §1 el prompt, §2 cómo leer el PR, §3 el falsador.

---

## §1 · El prompt de la tarea recurrente

Cadencia sugerida: **diaria en día hábil**. La recurrencia vive en la
tarea de mesa en Claude Code — **este acto no crea ningún `schedule` en
GitHub Actions**, deliberadamente: `.github/workflows/verify.yml` es
compuerta de CI (`on: push: main` + `pull_request`), y meterle una
tarea de fondo mezclaría dos cosas que fallan distinto.

Pega esto, tal cual, como prompt de la tarea recurrente:

```text
Corre /tramite sobre este clon. Entorno NUBE: no abras microdato ni descargues nada.
Rama del día: claude/tramite-<AAAA-MM-DD>; si ya existe, continúa sobre ella.
Lo que requiera juicio NO se ejecuta: va como fila del digesto y se queda para mesa.
Abre UN PR titulado "[TRAMITE] digesto <AAAA-MM-DD>" y NO lo fusiones.
Si la suite no está en línea base VERDE, PARA y repórtalo con la salida cruda.
```

Cinco líneas. Todo lo demás —el arranque, el perímetro, las cuatro
acciones permitidas, los guardrails— vive en la skill, versionado en el
repo, no en el prompt: la lección de `D-10` es que el texto que se
transcribe a mano se desfasa, y el que vive en el repo no.

## §2 · Qué esperar de cada PR

Un PR `[TRAMITE]` sano trae, siempre:

- **Un archivo nuevo** en `forense/digesto/`, y ningún otro archivo
  fuera del perímetro de tres rutas.
- **Cero decisiones.** Si el PR te está preguntando algo, la pregunta va
  como fila del digesto y la respuesta la das tú al fusionar (o no).
- **Cada movimiento de fila con su cita.** Una fila que pasa a `FIRMADA`
  trae el `archivo:línea` donde vive la firma verbatim de mesa. Sin cita,
  la fila no se mueve: se reporta.
- **`CONTADOR: cero, declarado.`** El agente de trámite no mide nada. Si
  un día un PR suyo dice que midió algo, algo se rompió.
- **La suite en línea base VERDE**, o un PARO con la salida cruda.

Cómo leerlo en dos minutos: abre el digesto, mira la sección **A** (qué
lleva más días abierto), la sección **B** (¿VERDE?), y el diff del
tablero. Ese diff es la única parte que cambia estado, y es corto por
construcción.

**Fusionar es firmar.** El PR propone; la firma la das tú al fusionar.
Si una fila no debía moverse, se rechaza esa parte y se anota — el
agente no vuelve a proponerla sin cita nueva.

## §3 · Falsador, a un mes

Se revisa la skill y **se anota**, si en un mes ocurre cualquiera de
las dos:

- **(a)** un PR `[TRAMITE]` **requiere retrabajo de mesa** — que mesa
  tenga que corregir, revertir o rehacer lo que el PR propuso, más allá
  de decidir si fusiona;
- **(b)** un PR `[TRAMITE]` **toca algo fuera del perímetro** de tres
  rutas, aunque el cambio sea correcto.

Cualquiera de las dos, con el caso citado, dispara revisión de la pieza
que falló. Es el mismo criterio de caducidad que `A.3`/`A.8`/`A.9`/
`A.10`/`A.12`/`A.13` y que la propia skill `/acto` (`D-13`,
`instrucciones-proyecto-v2_12.md`).

Y la prueba de que la pieza sirvió, para el otro lado: que una fila del
tablero deje de envejecer sin que nadie abriera la suite a mano. Eso es
exactamente lo que `D-13` dejó registrado como práctica y no como regla:

> un agente de fondo recurrente corre tests/check.py --baseline, lista
> las filas ABIERTA del tablero con su antigüedad, y redacta los PRs de
> trámite (recibos, censos, enterados) para firma de mesa — el WARN
> diario deja de depender de que alguien abra la suite a mano.

**CONTADOR de este acto: cero mediciones, declarado.** Es
infraestructura: instala el vehículo, no mide con él.
