# Nota de cierre · ACTO GEN2-TUBERIA-TABLERO-EN-CANAL-1 · 24/sep/2026

ADR: `ADR-260924-GEN2-TUBERIA-TABLERO-EN-CANAL-1-3726-01`. Encargo:
`forense/encargos/2026-09-24-GEN2-TUBERIA-TABLERO-EN-CANAL-1.md`
(`.cuerpo.sha256` = `dc1392b5…`). Entorno NUBE, Sonnet 5, MODO ABIERTO,
COMPUERTA: ninguna. Rama `claude/new-session-tydnvn` (la que la plataforma
fijó; el encargo lo permite explícitamente).

## Qué se hizo

- **P1.** `.github/workflows/verify.yml`, job `guardias`, paso "Deriva
  vistas y abre PR automático verificado": después de la guarda de tamaño
  de `VISTA-NORMALIZADA-2` y antes de `git add`, se añadió
  `git fetch -q origin main` + `python3 tools/tablero_programa.py
  --actualiza`. El checkout de este job solo trae `refs/remotes/origin/ci`
  (nunca `origin/main` con ese nombre), así que el `fetch` explícito es
  necesario para que el guardián de P2 pueda resolver `origin/main` ahí
  también. `git add` ahora incluye `forense/tablero/TABLERO-PROGRAMA.md` y
  `docs/tablero.md`.
- **P2.** `tools/tablero_programa.py`: nueva función pura
  `_compara_head_origin_main(head, remoto)` (testeable sin git real) y
  `_es_origin_main_limpio()` que la alimenta con `git rev-parse HEAD` /
  `git rev-parse -q --verify origin/main`. `main()` la consulta antes de
  derivar nada cuando se pide `--actualiza`; si no coincide y no se pasó
  `--permitir-rama`, se niega con código 1 y un mensaje que nombra los dos
  SHA. Con `--permitir-rama`, procede pero `render_bloque_vivo(...,
  no_es_origin_main=True)` antepone el rótulo `NO-ES-ORIGIN-MAIN`.
  `.claude/commands/tramite.md` (T0) se actualizó para dejar de pasar esa
  bandera y documentar que el refuso esperado (su rama administrativa casi
  siempre está adelante de `origin/main`, con la huella del ciclo ya
  commiteada) no es un fallo del ciclo.
- **P3/P4.** `docs/tablero.md` (Jekyll, con marcadores
  `TABLERO-DERIVADO:BEGIN/END` igual que el canónico) se actualiza con la
  MISMA llamada a `_actualiza_tablero` — dos salidas, un solo productor,
  no un segundo escritor. `docs/PROTOCOLO-TABLERO.md` fija el protocolo:
  una conversación lee, cita e interpreta; nunca regenera ni sube
  versiones; un bloque `¿árbol == origin/main? False` sin
  `--permitir-rama` es inválido y se ignora. `docs/index.md` gana una
  entrada de navegación al tablero.

## Verificación de existencia (§6, antes de tocar código)

`grep -c 'tablero_programa' .github/workflows/verify.yml` → **1**, no el 0
esperado por el encargo — pero es solo un comentario de prosa
(`GEN2-TUBERIA-METRICA-RECTORA-1`, l.284, "la métrica rectora deja de
vivir sólo en tablero_programa.py"), no una invocación real: no hay
trabajo ya hecho que este acto duplique. `ls docs | grep -c tablero` → 0.
`git ls-remote --heads origin | grep -i tablero` → 0 (sin rama con este
rótulo). Duplicado (0.c): sin rama remota, sin worktree ajeno, sin PR
abierto con este rótulo.

## Corrección de premisa (logística, no PARO)

El encargo cita `canon/TABLERO-PROGRAMA.md` en §1 (tres veces) y §9 (dos
veces). Ese archivo **no existe** en el árbol
(`ls canon/TABLERO-PROGRAMA.md` → `No such file or directory`;
`find . -name TABLERO-PROGRAMA.md` → únicamente
`./forense/tablero/TABLERO-PROGRAMA.md`). El contenido de ese archivo real
coincide exactamente con la premisa `[EJECUTADO]` del encargo (`SHA
8a867a04 · ¿árbol==origin/main? False`, línea "Procedencia" del bloque
vivo), así que no hay duda de CUÁL archivo dirección tenía en mente —
solo un error de ruta al redactar. Se implementaron las cuatro piezas
contra la ruta real; el cuerpo del encargo archivado no se edita (A.3),
la corrección queda aquí, en el ADR y en `## NO-CORRIDO / RESERVAS` del
propio encargo.

## Defecto de determinismo encontrado y corregido (P4)

El propio test de determinismo que P4 pide
(`prueba_determinismo_dos_pasadas`, que corre `derivar_indicadores()` dos
veces sobre el árbol real) **falló en su primera corrida**: dos
derivaciones sobre el MISMO `HEAD`, separadas por los varios minutos que
tarda `derivar_indicadores()` (recorre 335 entradas de `data/corrida0/`
vía `corrida0.py status`), produjeron bloques distintos.

Diagnóstico (`difflib.unified_diff` entre las dos derivaciones): la única
diferencia material era la sección "Ramas presentes en origin" — `3`
ramas en la primera derivación, `4` en la segunda (el commit del propio
0-bis de este acto se había publicado entretanto, y otra sesión concurrente
también movió una rama). Causa: `tools/estado_comun.py::
ramas_remotas_detalle()` corre `git ls-remote --heads origin` y además
`git fetch --prune origin +refs/heads/*:refs/remotes/origin/*` **en
vivo**, contra un repositorio con sesiones concurrentes empujando ramas
todo el tiempo. Esto no es una función del commit congelado (`HEAD`): es
el estado del remoto en el instante exacto de la llamada.

El propio docstring de `render_bloque_vivo()` ya decía: "sin cifras
efímeras (edad en días de FP, ramas remotas presentes), que siguen
disponibles en la salida interactiva normal (markdown/--json) pero no
aquí" — pero el código sí las imprimía (`ACTO GEN2-TABLERO-SENAL-1` las
añadió después de que se escribiera ese docstring, sin actualizarlo).
Corrección (autorizada por el `[SUPUESTO]` del propio encargo: "si no lo
es… se arregla en ≤10 líneas y se declara"): se retiró el bloque de
"Ramas presentes en origin" de `render_bloque_vivo()` (11 líneas
retiradas, un comentario de 8 líneas explicando por qué). El indicador
`ramas_remotas_detalle` **no se borra**: `derivar_indicadores()` lo
sigue calculando y queda disponible en `--json` y para
`tools/tablero_vista.py`, que son los consumidores que el propio
docstring ya nombraba como destino correcto.

El test existente que afirmaba lo contrario
(`prueba_render_incluye_marcador_corridas_ramas_nc`, de
`ACTO GEN2-TABLERO-SENAL-1`) se renombró a
`prueba_render_incluye_marcador_corridas_nc` y su aserción sobre "Ramas
presentes en origin" se invirtió (ahora afirma que NO aparece), con nota
explicando por qué. El resto de esa prueba (marcador, corridas
pendientes, censo de NC, corrección del rótulo del Corredor) sigue
intacto.

Confirmación durante el desarrollo (test temporal, no committeado): dos
llamadas reales a `derivar_indicadores()` sobre el árbol, después del fix,
dieron `render_bloque_vivo()` idéntico byte a byte.

**Por qué esa prueba de dos pasadas NO quedó en el archivo committeado.**
Medida por separado: **una sola** llamada a `derivar_indicadores()` tarda
`123.1s` (recorre las 335 entradas de `data/corrida0/` vía `corrida0.py
status`). `tools/ci_guardias.py --censo` clasifica cada archivo de test
por EJECUCIÓN real contra un timeout de `40s` (`ejecuta()`, default); dos
pasadas (>240s) habrían hecho que el PRÓXIMO `--censo` clasificara **el
archivo entero** `FALLA-DE-VERDAD (TIMEOUT>40s)`, y `--ejecuta-huerfanos`
solo corre lo clasificado `CORRE-EN-CI` — las otras 13 pruebas de este
mismo archivo (idempotencia, anclas inválidas, `_estado_cola`, el
guardián P2, etc.) habrían dejado de correr en CI, en silencio, por el
costo de una sola prueba (D-14: "verificar tiene precio"). Se optó por
NO incluirla y dejar en su lugar dos guardas baratas que cubren la MISMA
clase de defecto sin pagar la derivación completa: `prueba_render_
incluye_marcador_corridas_nc` (afirma que "Ramas presentes en origin" NO
aparece) y el resto de las pruebas del guardián P2. El código deja un
comentario explicando esta decisión donde estaba la prueba retirada.

Confirmación de la versión committeada: `python3 tests/test_tablero_programa.py`
→ **13 pruebas, 0 fallos**, `0.32s`.

## Verificación manual del "Hecho" (P2)

```
$ git fetch -q origin main
$ python3 tools/tablero_programa.py --actualiza
error: --actualiza se niega -- HEAD (372646f64792d93d79e133677ce664b19fe24b9b) != origin/main (82e16b421dfad4d5ac6a789bdccff1db491ed998). El único productor del canal es el job `guardias` de CI sobre origin/main (.github/workflows/verify.yml); usa --permitir-rama para forzarlo de todos modos -- rotula el bloque NO-ES-ORIGIN-MAIN.
$ echo "RC=$?"
RC=1
```

## Suite

`python3 tests/check.py --rapido` → 0 FAIL, 410 WARN (WARN no adjudican,
D-16), 9.16s. `python3 tests/check.py --baseline` corrido antes de
empujar el cierre final (ver commit de cierre para la salida).

## `## NO-CORRIDO / RESERVAS`

Ver la sección homónima en el propio encargo archivado
(`forense/encargos/2026-09-24-GEN2-TUBERIA-TABLERO-EN-CANAL-1.md`):
P5 (prueba real post-merge) queda NO-VERIFICABLE-AQUÍ, y la verificación
de que Pages sirve `docs/tablero.md` queda DIFERIDO-A
`FP-260923-GEN2-FRONT-1-4296-01` (fin de semana 26-27/sep/2026).
Filas `NC-260924-GEN2-TUBERIA-TABLERO-EN-CANAL-1-3726-01` y `…-3726-02`
en `forense/no-corrido.tsv`, estado `ABIERTA`.

## Contadores

Cero mediciones. `celdas_validadas: 219 → 219 (Δ0)`. No adopta, no toca
`milpa/tramite.yaml`, no toca ningún CALC ni RESULT.

**El PR no se fusiona en este acto: mesa fusiona.**
