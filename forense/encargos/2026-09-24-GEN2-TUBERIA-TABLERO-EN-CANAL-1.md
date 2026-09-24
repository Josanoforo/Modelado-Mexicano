# ENCARGO · ACTO GEN2-TUBERIA-TABLERO-EN-CANAL-1 · El tablero deja de tener dos productores: se deriva en CI sobre `origin/main` en cada push, entra al PR `[deriva]` que se auto-fusiona, se publica en Pages, y `/tramite` T0 se niega a regenerarlo desde un árbol que no sea `origin/main`

> ENTORNO: **NUBE** — CI, derivador del tablero, `docs/`. Hook imprime ENTORNO-DERIVADO; si dice CAJA, PARA.

CABECERA · SHA de redacción `3252aaec` (re-deriva al abrir) · una sola sesión, rama propia `acto/gen2-tuberia-tablero-en-canal-1` (o la que la plataforma fije; se declara en el 0-bis) · MODELO: Sonnet (sube a Opus si toca `tablero_programa.py` más allá de la guarda) · MODO: ABIERTO · ids con raíz de acto (D-24) · D-21 aplica · «Si te encuentras escribiendo fuera de la lista de §9, PARA.» · cierre por /acto: `## NO-CORRIDO / RESERVAS` («Ninguno.» obligatorio si aplica) y `## CONSUMIDO` al pie.
CONTADOR: cero mediciones; no adopta; no cambia ningún número del tablero (lo deriva; si un número cambia respecto al v6 es porque `main` cambió, y la nota lo muestra con `git log`).

## 1 · OBJETIVO
Un solo productor del tablero, mecánico, sobre `origin/main`. (P1) En `.github/workflows/verify.yml`, en el paso que deriva las vistas y abre el PR `[deriva]` (el que VISTA-NORMALIZADA-2 está dejando bajo la guarda de tamaño), añadir `python3 tools/tablero_programa.py --actualiza` después de `registro --escribe` y de las dos pasadas del marcador, de modo que el bloque `<!-- TABLERO-DERIVADO:BEGIN … END -->` de `canon/TABLERO-PROGRAMA.md` se regenere con el árbol de `main` del push y viaje en el mismo PR. (P2) Guarda en el propio derivador: si `git rev-parse HEAD` ≠ `origin/main` (o el árbol está sucio), `--actualiza` **se niega** con mensaje claro salvo `--permitir-rama` explícito que rotula el bloque `NO-ES-ORIGIN-MAIN`; `/tramite` T0 no pasa esa bandera. (P3) `docs/tablero.md` en Pages: enlaza (o incluye por script del sitio) el bloque derivado de `main`, con la fecha y el SHA del bloque en la cabecera, para que mesa lo abra por URL en vez de recibir archivos. (P4) `docs/PROTOCOLO-TABLERO.md`: dos párrafos para la conversación del tablero y para mesa — el tablero se lee de `https://raw.githubusercontent.com/Josanoforo/Modelado-Mexicano/main/canon/TABLERO-PROGRAMA.md` o de Pages; una conversación lo interpreta, lo cita y **nunca lo regenera ni sube versiones**; un bloque con `árbol == origin/main? False` es inválido y se ignora.
«Hecho» sobre el commit final con origin/main fusionado: el primer PR `[deriva]` posterior trae `canon/TABLERO-PROGRAMA.md` con `SHA` = el commit del push y `¿árbol == origin/main? True` (cita del PR y del bloque) · `python3 tools/tablero_programa.py --actualiza` desde una rama devuelve código ≠ 0 sin `--permitir-rama` (salida pegada) · `docs/tablero.md` y `docs/PROTOCOLO-TABLERO.md` existen y Pages los sirve (o queda la receta si Pages aún no está activa: FP `4296-01`, fin de semana) · test propio: el bloque regenerado sobre `origin/main` en un clon limpio es idéntico byte a byte al que el job produjo · `check.py --baseline` VERDE sin `--force`.

## 2 · FIRMAS DE MESA
Decisión de dirección del 24/sep, comunicada a mesa en chat sin objeción: «El tablero se deriva en CI sobre origin/main y entra al PR [deriva]; la conversación del tablero pasa a lectora; T0 se niega fuera de origin/main.» Es proceso, no medición: no requiere fila FP; el ADR la cita. Vigentes: D4-A y R(a) (auto-merge cubre `[deriva]`), D-23 (un comando que deriva no escribe estado fuera de su derivado).

## 3 · LO QUE DIRECCIÓN SABE
- `[EJECUTADO]` (`3252aaec`) `canon/TABLERO-PROGRAMA.md` en main: bloque derivado con `SHA 8a867a04 · ¿árbol == origin/main? False` (regenerado por `/tramite` desde una rama, commit `78f79c80`). El v6 que mesa recibió por chat: `SHA 3423b498 · True`, de un clon limpio. Dos productores, dos resultados.
- `[LEÍDO]` `.claude/commands/tramite.md` l.135-137: T0 corre `tools/tablero_programa.py --actualiza` «con la línea base verde… derivación mecánica». `[EXISTE]` `tools/tablero_programa.py`, `tools/tablero_vista.py`, `data/curacion-universo/tablero-cobertura.json`.
- `[LEÍDO]` `verify.yml`: el paso de derivados corre `lote_desde_asientos.py`, `registro --verifica --escribe --lote`, `resuelve_citas.py tabla --escribe`, `marcador_segmento.py --escribe` ×2 (#1101), y abre el PR `derivados/auto-*` con `gh pr create` (casilla de Actions activa desde el 23/sep). VISTA-NORMALIZADA-2 (en vuelo) añade una guarda de tamaño antes de ese paso: **este acto se inserta después de esa guarda y rebasa si choca**.
- `[SUPUESTO]` que `tablero_programa.py --actualiza` es determinista sobre un mismo árbol (dos corridas = mismo bloque); el test de P4 lo demuestra. Si no lo es (fechas, orden de dict), se arregla en ≤ 10 líneas y se declara.
- ADJUNTOS: ninguno (el v6 está en el chat de mesa; el acto lo cita como referencia, no lo archiva: el archivo canónico es el de `main`).

## 4 · YA HECHO / YA DECIDIDO
`grep -c 'tablero_programa' .github/workflows/verify.yml` → reporta (esperado 0). `ls docs | grep -c tablero` → 0. `git ls-remote --heads origin | grep -i tablero` → 0.

## 5 · PIEZAS
P1 · Paso de CI (después de las vistas y el marcador; antes de `gh pr create`). P2 · Guarda `origin/main` en el derivador + `--permitir-rama` con rótulo; `/tramite` T0 sin bandera (una línea en `tramite.md` que lo diga). P3 · `docs/tablero.md`. P4 · `docs/PROTOCOLO-TABLERO.md` + test de determinismo. P5 · Prueba real: tras el merge, el primer `[deriva]` trae el bloque con `True`; cita.

## 6 · LATITUD
Cómo incluir el bloque en Pages (enlace, include de Jekyll, copia por el mismo job): tuyo. ≤ 10 líneas adyacentes: sí. Pregunta a mesa: ninguna.

## 7 · PAROS — lista cerrada
a) no aplica · b) editar el bloque derivado a mano, tocar `registro`, `marcador_segmento.py`, la guarda de tamaño de VISTA-2, o un sello · c) mover contadores a mano · d) no aplica · e) CAJA · f) el tablero ya llega por `[deriva]` con `True`.

## 8 · COMPUERTAS
«El bloque solo lo escribe el job sobre origin/main; T0 se niega fuera» protege: **congelar / borrar** (un tablero de rama es un estado falso publicado). «Test de determinismo antes de meterlo al canal» protege: **congelar** (un derivado no determinista genera PR infinitos).

## 9 · PERÍMETRO Y CONCURRENCIA
Propio: `.github/workflows/verify.yml` (solo la línea del tablero en el paso de derivados), `tools/tablero_programa.py` (guarda y `--permitir-rama`), `.claude/commands/tramite.md` (una línea en T0), `docs/tablero.md`, `docs/PROTOCOLO-TABLERO.md`, `canon/TABLERO-PROGRAMA.md` **solo por el job**, test propio, nota, L0, cascada. Ajeno: vistas, marcador, guarda de tamaño (VISTA-2), `check.py`. En vuelo: VISTA-NORMALIZADA-2 (mismo paso de `verify.yml`: lanzar después de su COMMIT-A o rebasar), ADOPCION-3, CATALOGO, ENCIG-PISOS, REPLAY, U5.

## 10 · LO QUE NO HACE · SUCESORES
No cambia qué mide el tablero ni sus definiciones (`celdas_validadas_definicion_desde` sigue siendo de CONTADORES). Sucesor: ninguno; si Pages exige un include que Jekyll no soporte, `-2` con la copia por job.

## NO-CORRIDO / RESERVAS

- **qué:** P5 — prueba real de que el primer PR `[deriva]` posterior al merge trae `forense/tablero/TABLERO-PROGRAMA.md` con `SHA` = commit del push y `¿árbol == origin/main? True`.
  **por qué:** NO-VERIFICABLE-AQUÍ — solo se puede observar sobre un commit ya fusionado en `origin/main`; este acto abre el PR, no lo fusiona (mesa fusiona).
  **impacto:** el mecanismo (P1 + P2) sí quedó verificado unitariamente (`tests/test_tablero_programa.py`, 14 pruebas) y a mano (`--actualiza` sin `--permitir-rama` se niega fuera de `origin/main`, código 1, salida citada en el ADR); falta únicamente la confirmación empírica de la primera corrida real en canal.
  **sucesor:** seguimiento de este mismo PR tras el merge, o el siguiente `/tramite` que lea el primer bloque publicado en canal.

- **qué:** P3 — verificar que GitHub Pages sirve `docs/tablero.md` y `docs/PROTOCOLO-TABLERO.md` por URL.
  **por qué:** DIFERIDO-A:FP-260923-GEN2-FRONT-1-4296-01 — Pages desde `main/docs` todavía no está activo (fila `ABIERTA`, mesa propuso activarlo el fin de semana 26-27/sep/2026, después de que `CONTADORES-2` fusionara).
  **impacto:** los dos archivos existen, están commiteados y siguen la receta de Jekyll del resto de `docs/`; nadie puede confirmar hoy que Pages los sirve, solo que están listos para cuando se active.
  **sucesor:** `FP-260923-GEN2-FRONT-1-4296-01` (ya `ABIERTA`, fin de semana 26-27/sep/2026).

Corrección de premisa declarada aquí (no se edita el cuerpo, A.3): las cinco menciones de `canon/TABLERO-PROGRAMA.md` en este encargo (§1, §9) citan una ruta que no existe en el árbol; el archivo real, con el mismo contenido que la premisa `[EJECUTADO]` de §3 describe (`SHA 8a867a04`), es `forense/tablero/TABLERO-PROGRAMA.md`. Todas las piezas (P1-P4) se implementaron contra la ruta real.
