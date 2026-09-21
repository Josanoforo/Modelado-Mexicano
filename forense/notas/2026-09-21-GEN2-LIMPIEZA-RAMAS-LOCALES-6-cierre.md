# GEN2-LIMPIEZA-RAMAS-LOCALES-6 · cierre — el último de la línea de limpieza

Encargo archivado verbatim en `forense/encargos/2026-09-21-GEN2-LIMPIEZA-RAMAS-LOCALES-6.md`.
Sesión CAJA (`pc0-0d`), Sonnet 5, `origin/main` al abrir = `d5825063` (merge de `#933`).

## ENMIENDA a `#936` (`GEN2-LIMPIEZA-RAMAS-LOCALES-5`) — su P5 estaba equivocado

`#936` (nota `2026-09-20-GEN2-LIMPIEZA-RAMAS-LOCALES-5-cierre.md`, sección P5) clasificó
`acto/gen2-f5-recaptura-l` como `A-MEDIAS` con una "remedición completa sin commitear". **Esa
lectura era falsa**, y el defecto de método fue exactamente el que dirección señaló: se comparó
el `git diff` del worktree contra el **HEAD de su propia rama** (9/sep/2026), no contra la
**historia de `origin/main`**. Verificado de nuevo, esta vez contra `origin/main`, con las tres
comprobaciones que dirección pidió más dos propias:

1. `git log --first-parent --format='%h %cs %s' origin/main | grep '#669'` →
   `d20039a3 2026-09-09 Merge pull request #669 from Josanoforo/acto/gen2-f5-recaptura-l`. El PR
   sí fusionó, y trajo consigo los `corridas-L/*__v1_3.json` y `L-spec-v1_3.json` — la medición
   real de las 16 réplicas ya vive en `main` desde el 9/sep.
2. `grep CAPTURA-CORREDOR data/corrida0/demanda-resultados.tsv | grep -o '([0-9]* replicas)' |
   sort | uniq -c` en `origin/main` → **28 filas, las 28 en "(16 replicas)"**. El valor que el
   worktree tenía sin commitear ya está, íntegro, en `main`.
3. `head -1 data/corrida0/demanda-resultados.tsv` → `# DERIVADO — NO EDITAR`. El archivo no es
   dato primario: es un derivado que se regenera desde los `corridas-L/*.json` sellados.
4. **Verificación propia añadida:** los 256 archivos `forense/prereg-duelo-v2/corridas-L/*CIV-M*`
   trackeados en la rama son **byte a byte idénticos** a `origin/main` (`git diff --quiet` en los
   256, cero diferencias). No hay ninguna captura sin seguimiento en el worktree.
5. `git status --porcelain --ignored=matching` del worktree, antes de tocar nada: **una sola
   línea modificada** (`data/corrida0/demanda-resultados.tsv`), cero archivos nuevos de captura.

**Veredicto correcto: `CERRADO-FALTA-BORRAR`, no `A-MEDIAS`.** Lo único que el worktree tenía sin
commitear era la regeneración local de un archivo derivado, ya idéntica a lo que `main` calcula
por su cuenta desde los mismos insumos sellados. No hay medición en riesgo. `#936` no se edita
(A.10/A.3 — un registro ya sellado no se reescribe); esta enmienda queda como corrección posterior
citable. `NC-0433` (`terminar o abandonar acto/gen2-f5-recaptura-l`) **CIERRA** con esta evidencia
como razón — la pregunta que planteaba (¿terminar o abandonar una medición?) no aplicaba: no había
medición pendiente que terminar ni abandonar. `FP-404` se retira del tablero de pendientes por la
misma razón.

## F-1 a F-5 · ejecutado

- **F-1** (`acto/gen2-f5-recaptura-l`): `git checkout -- data/corrida0/demanda-resultados.tsv`
  tras la verificación de arriba. Worktree limpio, `git worktree remove` (sin `--force`) y
  `git branch -d` — **ambos sin fallo** (PR #669 sí es ancestro real de `main`, a diferencia de
  los casos F-B/F-C de `#929` donde el contenido rescatado vivía solo archivado, no fusionado).
- **F-2** (`acto/gen2-reparacion-cierre-consolidacion-cron`): `fuser`/`lsof` confirmaron
  **ningún proceso** con `data/curacion-registro/cola-adquisicion-registro.tsv.lock` abierto;
  borrado (`rm`, 0 bytes). Worktree limpio, retirado sin `--force`, `branch -d` sin fallo.
- **F-3** (`encuci2020-respuesta-por-contacto-cli-2`, `issp2017-consistencia-apoyo-familiar-cli-2`):
  las dos copias de `controles-medidor.json` dan el **mismo sha256**
  (`a5356e5d…f5360b`); `git grep` confirmó que ningún `medidor.py`/`spec.yaml`/`ejecucion.json`
  sellado de `main` cita ese nombre de archivo como insumo (solo citan el directorio
  `forense/analisis/issp2017-redes-apoyo-cotidiano-cli-1/` como destino de sus propios outputs,
  con nombres distintos). Borrados los dos, worktrees limpios, retirados sin `--force`,
  `branch -d` sin fallo en ninguna de las dos.
- **F-4** (`codex/autoridad-semantica-enif`, `llave2-decreto`): verificación archivo por archivo
  contra lo archivado por `#929` — **`llave2-decreto`**: `sha256sum` de los 25 archivos de
  `scratchpad/` coincide 25/25 con `llave2-decreto-scratchpad-2026-09-20-SHA256SUMS.txt`.
  **`autoridad-semantica-enif`**: los 3 archivos sin seguimiento coinciden con el
  `SHA256SUMS.txt` archivado (jsonl, script) o con el blob de `main` (schema.json, byte a byte
  idéntico, por eso no se archivó aparte en `#929`); los 2 archivos trackeados modificados
  (`generar_marco.py`, `marco_e2_adapter.py`) se verificaron por **`git hash-object`** contra los
  blobs `d7821c52…`/`79fe3e81…` que el propio `diff-trackeados.patch` archivado declara como el
  lado "nuevo" — coinciden exactamente (el diff en sí ya no coincidía byte a byte porque su base,
  `origin/main`, se movió desde el 20/sep; el archivo del worktree no se había tocado). Todo
  coincidió: se borró el contenido sin seguimiento y se descartaron las 2 modificaciones
  (`git checkout --`). Worktrees limpios, retirados sin `--force`, `branch -d` sin fallo en
  ninguno.
- **F-5** (`codex/optimiza-verificacion-ci-prueba-compuerta`): medida su edad al cerrar este
  acto: **23h46m**, todavía `<24h`. **No se tocó**, tal como la firma lo condiciona. Queda para
  un barrido futuro cuando cumpla 24h (archivar su único commit como insumo + `git branch -D`,
  dado que no tiene PR propio).

Ningún `-d` fue rechazado en este acto (a diferencia de `#929`/`#910`, donde varios casos
rechazados por contenido-redundante-pero-no-ancestro quedaron para firma de mesa): todas las
ramas tocadas aquí eran, o ancestros reales verificados de `main`, o su contenido sin seguimiento
ya estaba archivado/confirmado en `main` con verificación byte a byte — así que ninguna necesitó
escalar a `-D`.

## Estado final crudo, por clon

```
$ git -C /home/pc0/Modelado-Mexicano branch --no-color
+ acto/gen2-din-credito-comparabilidad-texto-1
+ acto/gen2-limpieza-ramas-locales-4-cierre-fp402
+ acto/gen2-limpieza-ramas-locales-5
+ acto/gen2-limpieza-ramas-locales-6
+ worktree-agent-a336d4013203d5b8e
+ worktree-agent-a7d8e527ae88b7feb
+ worktree-agent-a9facc03b479266d6
codex/optimiza-verificacion-ci-prueba-compuerta
main

$ git -C /home/pc0/Modelado-Mexicano branch | wc -l
9
$ git -C /home/pc0/Modelado-Mexicano worktree list | wc -l
8
$ git -C /home/pc0/mm-adq branch | wc -l
4
$ git -C /home/pc0/mm-adq worktree list | wc -l
2
$ git -C /home/pc0/Modelado-Mexicano rev-parse --is-shallow-repository
false
```

**Lo que queda y por qué:**
- 4 `EN-CURSO`, no se tocan: `acto/gen2-din-credito-comparabilidad-texto-1` (PR #932 abierto),
  `acto/gen2-limpieza-ramas-locales-4-cierre-fp402` (PR #934 abierto),
  `acto/gen2-limpieza-ramas-locales-5` (PR #936 abierto, "se fusiona como está"),
  `acto/gen2-limpieza-ramas-locales-6` (este acto).
- `codex/optimiza-verificacion-ci-prueba-compuerta`: `<24h` (F-5 diferida).
- 3 `worktree-agent-*` + `main`: `INFRAESTRUCTURA`, ajenos al perímetro del proyecto.
- `mm-adq`: sin cambios en este acto (4 ramas / 2 worktrees, automatización ajena — el segundo
  worktree efímero de `/tmp` que existía al abrir `#936` ya se cerró solo entre actos).

## La cuenta completa de la línea de limpieza

`Modelado-Mexicano`: **270 → 9** ramas locales (censo inicial de `#910`, 20/sep/2026, antes de
tocar nada). Cinco actos (`#910`, `#913`, `#923`, `#929`, este) y sus dos cierres de firma
intermedios (`#934`, y `#936` en curso) redujeron el inventario en **261 ramas** a lo largo de
~30 horas, sobre un clon que además recibió, en el mismo lapso, docenas de actos nuevos y
merges concurrentes de al menos tres sesiones distintas de la caja.

## Suite y shallow

VERDE (ver commit de cierre). `git rev-parse --is-shallow-repository` → `false`.

## Semilla PARA-v2.16

**"Trabajo sin commitear se juzga contra la historia de `origin/main`, no contra el HEAD de su
rama; un archivo con cabecera `DERIVADO` nunca es trabajo sin guardar."** Medido dos veces en la
misma línea de actos: `#929`/`#910` (`branch -d` rechaza ramas cuyo contenido es redundante con
`main` pero no es su ancestro literal — ahí el error era del lado de `-d`, no del clasificador) y
ahora `#936` (el clasificador mismo comparó contra la base equivocada y produjo un falso
`A-MEDIAS`). Ambos defectos comparten la misma raíz: **"¿está esto ya en `main`?" es una pregunta
sobre `origin/main`, nunca sobre el `HEAD` local de la propia rama o worktree** — ni para decidir
si se borra, ni para decidir si algo se perdería al borrar.

## NO-CORRIDO / RESERVAS

Ninguno.

## CONSUMIDO

Este cierre consume `forense/encargos/2026-09-21-GEN2-LIMPIEZA-RAMAS-LOCALES-6.md`.
