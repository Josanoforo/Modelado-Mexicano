# ENCARGO · ACTO GEN2-TUBERIA-SELLO-EXTERNO-1 · Los 226 sellos y las 116 specs congeladas quedan atestiguados por un tercero con fecha (OpenTimestamps o TSA RFC 3161), más la receta para que cualquiera lo verifique sin creernos; y cada sello futuro se atestigua solo

> ENTORNO: **NUBE**. Necesita egress a un calendario OpenTimestamps o a una TSA; si ninguno responde, el fallback (P2-c) no necesita red más allá de la API de GitHub. Hook imprime ENTORNO-DERIVADO; si dice CAJA, PARA.

CABECERA · SHA de redacción `7ca31cb4` (re-deriva al abrir) · una sola sesión, rama propia `acto/gen2-tuberia-sello-externo-1` (D-17) · MODELO: Sonnet (sube a Opus si P3 toca la cascada) · MODO: ABIERTO · ids con raíz de acto (D-24) · D-21 aplica · «Si te encuentras escribiendo fuera de la lista de §9, PARA.» · cierre por /acto: `## NO-CORRIDO / RESERVAS` («Ninguno.» obligatorio si aplica) y `## CONSUMIDO` al pie; adendas como `<este-encargo>-ADENDA-N.md`.
CONTADOR: cero mediciones; no adopta; no toca ningún sello (los lee y los atestigua); mueve cero contadores del tablero y lo dice en la primera línea de la nota.

## 1 · OBJETIVO
Que exista prueba **externa y verificable por terceros** de que cada emisión sellada existía en la fecha que decimos — el único activo del programa que un competidor con INEGI y un LLM no puede fabricar hacia atrás (informe de competencia 23/sep, §6). Hoy el sellado es interno: `sello.json` y sidecars `.sha256` en un repo público, con merge commits firmados por la llave de GitHub (`B5690EEEBB952194`, verificado con `git log --show-signature`). Eso atestigua fecha de merge, no existencia previa al merge ni ante quien no confíe en GitHub. Habilita: la posición «benchmark auditable del comportamiento del mexicano» (decisión 2) y las familias 2027 (U4 de ASTRA-4), cuyo valor depende de que el sello sea creíble antes de que INEGI publique la ola.
«Hecho» sobre el commit final con origin/main fusionado: `forense/sellos/manifiesto-sellos-2026-09-23.tsv` con N filas = número de `sello.json` + número de sidecars `.sha256` en `forense/prereg-caja/` (derivado por comando, citado; al redactar 226 + 116) · un archivo de atestación por manifiesto (`.ots` o `.tsr`) commiteado, con la salida cruda del comando de verificación en la nota (`ots verify` o `openssl ts -verify`) · `docs/sello-externo.md` con la receta de verificación para un tercero, probada por el ejecutor desde un clon limpio · `tools/sello_externo.py` con `manifiesto` y `stamp` como subcomandos, test propio huérfano · una fila FP para mesa: si la cascada de `/acto` debe llamar `stamp` en cada cierre (sucesor), con recomendación.

## 2 · FIRMAS DE MESA
**Decisión 1 del 23/sep (propuesta por dirección, mesa la da verbatim al lanzar):** «Se atestigua con un tercero de tiempo todo sello existente y todo COMMIT-1 futuro; la mecánica la elige el ejecutor entre las que respondan; ninguna sustituye al sello interno, lo acompaña.» Sin esta firma: §7 f. Ninguna otra.

## 3 · LO QUE DIRECCIÓN SABE
- `[EJECUTADO]` `git grep -il 'opentimestamps|\.ots|rfc3161|freetsa|sello de tiempo' -- tools forense/encargos docs canon .github` → 0 archivos pertinentes (un hit en `gobernanza-v1_15.md` es otro tema). `ls data/corrida0/CALC-*/sello.json | wc -l` → 226; `ls forense/prereg-caja/*.sha256 | wc -l` → 116. `git tag | wc -l` → 0. `sello.json` lista los archivos sellados (`ejecucion.json`, `medidor.py`, `resultados.json`, `spec.yaml`) con sus hashes.
- `[LEÍDO]` Informe de competencia 23/sep (sha `acbaa795b67017c8`) §6 y Recomendación 1: «hacer público y verificable el sellado (hash o sello de tiempo de terceros)… es el único activo que no se puede copiar»; riesgo: backtesting vendido como predicción.
- `[SUPUESTO]` que la sesión de nube tiene egress a `a.pool.opentimestamps.org` / `alice.btc.calendar.opentimestamps.org` o a una TSA pública (freetsa.org, DigiCert). **Verifícalo primero** (`curl -sI` con conteo); si no hay egress, P2-c y NC con receta para que mesa corra `ots stamp` en su máquina (un minuto).
- ADJUNTOS: ninguno.

## 4 · YA HECHO / YA DECIDIDO
Nada del objeto existe (§3). Ramas vivas: las cuatro sesiones de ASTRA-4 y U5 no tocan `forense/sellos/` ni `docs/`. **Repítelo.**

## 5 · PIEZAS
- **P1 · Manifiesto.** `tools/sello_externo.py manifiesto --escribe` produce `forense/sellos/manifiesto-sellos-<fecha>.tsv`: una fila por sello (`tipo` CALC|SPEC · `id` · `ruta` · `sha256` del sello · `commit` que lo introdujo, por `git log --diff-filter=A --format=%H -1 -- <ruta>` · `fecha_commit` · `pr` y `merged_at` desde la API de GitHub si está disponible, o NO-ACCESIBLE con conteo) y una última línea con el sha256 del propio manifiesto. Determinista: dos corridas sobre el mismo árbol dan el mismo archivo (test).
- **P2 · Atestación, en este orden y con todas las que respondan:** (a) OpenTimestamps sobre el sha256 del manifiesto → `.ots` commiteado; la prueba se completa cuando el calendario ancle en Bitcoin (horas): la nota dice «pendiente de anclaje» y el sucesor lo actualiza con `ots upgrade`. (b) TSA RFC 3161 (`openssl ts -query` → `.tsq`, respuesta `.tsr` commiteada, `openssl ts -verify` con la cadena de la TSA). (c) Fallback sin red: registrar en el manifiesto la firma GPG de GitHub del merge commit de cada sello y su `merged_at` por API, y dejar receta para que mesa firme un tag GPG con su llave (`git tag -s sellos-2026-09-23`). Se declara cuál funcionó con salida cruda; ninguna se inventa.
- **P3 · Receta para un tercero.** `docs/sello-externo.md`: qué archivo tomar, qué comando correr, qué tiene que salir, y qué demuestra cada mecanismo (y qué no: OTS demuestra existencia-antes-de, no autoría). Probada desde un clon limpio en la misma sesión, salida pegada.
- **P4 · Futuro.** `tools/sello_externo.py stamp --desde <manifiesto anterior>` atestigua solo sellos nuevos (delta). FP a mesa: ¿entra `stamp` a la cascada de `/acto` en cada cierre (recomendación de dirección: sí, como paso que no bloquea si el calendario no responde y deja NC)? Este acto **no** edita `.claude/commands/acto.md` ni CI: lo propone.

## 6 · LATITUD
Librerías (`opentimestamps-client`, `openssl`) libres; instalación con `pip --break-system-packages`. Obstáculos reversibles: egress, versiones. Pregunta a mesa (sigues): solo si ningún mecanismo (a)/(b) responde y (c) exige su llave GPG.

## 7 · PAROS — lista cerrada
a) no aplica · b) modificar, mover o re-hashear cualquier `sello.json`, sidecar o RESULT · c) no aplica · d) no aplica · e) CAJA · f) mesa no dio la decisión 1, o el objeto ya existe en origin/main.

## 8 · COMPUERTAS
«Los sellos se leen; nada se reescribe» protege: **borrar/reescribir**. «El manifiesto es determinista y su sha va dentro de la atestación» protege: **congelar** (una atestación de algo no reproducible no atestigua nada).

## 9 · PERÍMETRO Y CONCURRENCIA
Propio: `tools/sello_externo.py`, `forense/sellos/` (nuevo), `docs/sello-externo.md`, test propio, `firmas-pendientes.tsv`/`no-corrido.tsv` (append), nota, L0, cascada. Ajeno: `data/corrida0/`, `forense/prereg-caja/`, `.claude/`, `.github/`, `check.py`. En vuelo: ASTRA-4 U1–U5 (no tocan estos archivos), `derivados/auto-*`.

## 10 · LO QUE NO HACE · SUCESORES
No cambia la cascada ni CI; no firma por mesa. Sucesores: `GEN2-TUBERIA-SELLO-EXTERNO-2` (`ots upgrade` cuando ancle; cableado a `/acto` si mesa firma la FP de P4).
