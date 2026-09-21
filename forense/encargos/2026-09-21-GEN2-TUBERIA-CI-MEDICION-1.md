ENCARGO · ACTO GEN2-TUBERIA-CI-MEDICION-1 · CUÁNTO TARDA DE VERDAD EL CI EN GITHUB, EN QUÉ SE VA EL TIEMPO, Y QUÉ TESTS HAN ATRAPADO ALGO

CABECERA · redactado contra 13129c05 (re-deriva al abrir; si main se movió no es PARO) · ENTORNO: CAJA, con gh autenticado contra GitHub (sonda en P0) · NO es NUBE: la API sin credenciales da 60 peticiones por hora por IP y las IP de la nube son compartidas — la de dirección y la de TUBERÍA quedaron en cero (EJECUTADO, 21/sep 06:05–06:12 UTC, tres intentos) · cero microdato: la caja tiene corpus montado y este acto no lo abre · una sola sesión, rama propia (D-17) · MODO: ABIERTO · MODELO SUGERIDO: Opus · COMPUERTA: ninguna — no abre dato, no congela spec, no adopta, no borra (D-20) · CONTADOR: cuenta_gen2 = NO · vehículo: /acto.

SÓLO LECTURA SOBRE GITHUB. Este acto no relanza, no cancela, no borra ni dispara ningún workflow. Lee corridas, jobs, pasos y logs que ya existen.

EL PR NO SE FUSIONA EN ESTE ACTO: queda propuesto; mesa central fusiona. Lo que entrega es medición y una lista de recomendaciones; no elimina ni cambia ningún test. La lista la decide dirección en una pasada.

IDS. ADR numérico (deriva al cierre). NC/FP con raíz de acto: NC-<AAMMDD>-GEN2-TUBERIA-CI-MEDICION-1-<4 hex del 0-bis>-<NN>.

1 · EL MANDATO

De dirección, 21/sep, REPORTADO y en lo sustancial corroborado por TUBERÍA: más de la mitad del tiempo de un acto se va después de ## CONSUMIDO, en el ciclo re-fusionar → renumerar → correr la suite → empujar → esperar CI. Dirección pidió a TUBERÍA un barrido de caducidad (§9 de las instrucciones): para cada test y cada paso de la cascada, qué defecto real ha atrapado y cuándo fue la última vez, devuelto como una sola lista con mantener, abaratar o eliminar.

Lo que nadie ha medido todavía es lo que ocurre en GitHub: cuánto espera un PR su CI, en qué pasos y en qué tests se va el tiempo en el runner, y qué tests han fallado alguna vez en CI —es decir, han atrapado algo—. Este acto lo mide y construye la lista con esa evidencia.

2 · OBJETIVO Y CRITERIO DE «HECHO»

Entregar, en forense/analisis/ci-medicion-1/, con universo y conteo declarados (A.13):

Duración real del CI por corrida, por job y por paso, con mediana y p90.
Duración de cada test de la suite en el runner, sacada de los logs.
Historia de fallos en CI: qué paso y qué test ha fallado, en qué corridas, cuándo por última vez.
Espera de CI por PR: cuántas corridas tuvo cada PR desde el 18/sep, cuántas se cancelaron, y cuánto tiempo sumaron.
La lista del barrido: una fila por test de check.py, por paso del CI y por paso de la cascada de /acto, con su costo, su evidencia de captura y la recomendación.

Hecho = los cinco entregables en el árbol con su script de un solo uso, cada cifra con el comando que la produjo, check.py --baseline --parallel en LÍNEA BASE VERDE, PR propuesto y ## CONSUMIDO con el PR real.

3 · LO QUE TUBERÍA SABE — cada línea con su rótulo
LEÍDO · El camino ya funcionó una vez. forense/analisis/optimiza-verificacion-ci/ (PR #901, fusionado) midió seis corridas reales de Actions el 20/sep entre 01:46 y 02:12 UTC, desde un worktree en /home/pc0/… —la caja—. mediciones-actions.json tiene el formato de gh run view --json (databaseId, createdAt, updatedAt, jobs y pasos). Resultado de entonces: corrida completa ~172 s de mediana; job suite ~165 s y adicionales ~160 s en paralelo; el paso del marcador consumió 134 s en un runner. Ese acto midió 6 corridas controladas; éste mide la historia completa.
LEÍDO · El CI hoy, .github/workflows/verify.yml: se dispara en push a main, en pull_request y en workflow_dispatch; concurrency con cancel-in-progress: true —cada empuje nuevo cancela la corrida anterior del mismo PR—; 32 pasos en los jobs suite, adicionales, guardias y check, más los jobs propios de los PR #948 (preflight-calc) y #949 (guardas-res) si ya fusionaron.
LEÍDO · Los logs ya traen el tiempo por test. tests/check.py:7592 imprime [tiempo] <test>: X s por cada test. El log del paso de la suite es, por tanto, la duración de cada test en cada corrida.
EJECUTADO (TUBERÍA, 21/sep, un núcleo, main 32e23f7a) · check.py --baseline 189 s. T16 relanzando la suite: 94 s. T-CORRIDA0 36 s · T-PINES-MESA 27 s · T-REPRO 7 s · T45 7 s · T36 5.5 s · T32-ter 3.5 s · los otros 45 tests 6.5 s. tests/test_marcador_segmento.py: 129 s. Dirección midió T-REPRO en 17 s: la diferencia se resuelve con los tiempos del runner.
EJECUTADO · T16 compara hoy contra nada: cero afirmaciones vigentes de FAIL/WARN en los 11 archivos de canon/. Por la regla de dirección, T16 se elimina — este acto aporta la evidencia, no lo elimina.
EJECUTADO · La cascada de /acto corre la suite tres veces (acto.md:351, :384, :456), más una por cada re-fusión. La línea L0 de estado-programa se escribe a mano en cada cierre (acto.md:358-362; 141 commits a ese archivo en 7 días).
LEÍDO · Tests que ya no corre nadie. forense/analisis/ci-guardias/censo-tests.tsv —134 archivos de test— marca 36 como NECESITA-DEPENDENCIA (numpy, pandas, pytest, jsonschema, scipy, openpyxl) y 8 como FALLA-DE-VERDAD. Un test que no corre no atrapa nada; uno que falla y nadie lo mira, tampoco.
EJECUTADO (TUBERÍA) · PR fusionados desde el 18/sep: 78; con ≥1 re-fusión de main: 60; con ≥2: 35; con renumeración: 29; mediana del trabajo tras CONSUMIDO: 39 min. Todas las renumeraciones posteriores a #939 son de ADR.
4 · YA HECHO — búsqueda por OBJETO (A.8)
Medición de Actions: EXISTE-NO-SATISFACE — optimiza-verificacion-ci/ midió 6 corridas controladas para comparar dos variantes; no mide la historia, ni tiempos por test en el runner, ni fallos, ni espera por PR. Este acto reusa su método (gh … --json) y cita sus cifras como antecedente, no las repite.
Barrido de caducidad: NO-ENCONTRADO — ningún archivo en forense/ lista tests con su última captura.
Censo de archivos de test: EXISTE-SATISFACE para «qué corre y qué no» (ci-guardias/censo-tests.tsv); este acto lo lee, no lo rehace.
5 · PIEZAS — resultado esperado, no receta

P0 · 0-bis y sonda de acceso. Este encargo verbatim a forense/encargos/, con chequeo de duplicado por contenido. Luego, antes de pedir un solo dato: gh auth status y gh api rate_limit (el límite core debe ser 5 000, no 60). Si no hay credenciales: PARO-ENTORNO con esta receta para el titular, de un minuto:

gh auth login → GitHub.com → HTTPS → login con el navegador. O, sin gh auth: un token de grano fino, repositorio Josanoforo/Modelado-Mexicano únicamente, permisos Actions: Read-only y Metadata: Read-only, exportado como GH_TOKEN en la sesión.

El token no se escribe nunca en disco, en el repo, en un log ni en la nota.

P1 · El universo de corridas. Todas las corridas del workflow verify.yml desde el 18/sep —la ventana de dirección— hasta la cabeza. Por corrida: id, evento, rama, commit, intento, conclusión (éxito, fallo, cancelada), creación, inicio y fin. Declara cuántas examinaste y cuántas no pudiste leer (A.13).

P2 · Jobs y pasos. Por corrida, cada job y cada paso con su inicio, fin y conclusión. De ahí: mediana y p90 por paso; qué job fija la ruta crítica de cada corrida; y la espera inicial (creación → primer job en marcha), separada de la ejecución.

P3 · Tests en el runner. Descarga el log del job suite de cada corrida —o de una muestra declarada si el volumen lo impide— y extrae las líneas [tiempo] y las líneas de FAIL por test. De ahí: duración de cada test en el runner (mediana y p90) y cada fallo de cada test, con la corrida, el evento y la fecha. Distingue los fallos en ramas de PR —el test atrapó algo antes de fusionar— de los fallos en main.

P4 · Espera de CI por PR. Para cada PR fusionado desde el 18/sep: cuántas corridas tuvo, cuántas se cancelaron por un empuje nuevo, y el tiempo total de runner y de reloj que esperó. Cruza con lo que TUBERÍA ya midió del ciclo posterior a CONSUMIDO.

P5 · La lista del barrido. Una fila por cada test de tests/check.py (los 54, incluido T16), por cada paso de verify.yml y por cada paso de la cascada de /acto, con:

costo — local, en el runner, y cuántas veces corre por acto;
nacimiento — el defecto que lo motivó, leído de su propia cabecera o de su ADR, con archivo y línea;
evidencia de captura — cuántas veces ha fallado en CI, cuándo por última vez, y si alguna de esas veces fue en una rama de PR;
recomendación: mantener, abaratar (con cómo, sin tocar una aserción) o eliminar, y qué le costaría a un lector eliminarlo.

Y aparte, los 44 archivos de test que no corren según el censo (36 por dependencia, 8 que fallan de verdad), cada uno con la misma recomendación. Un test que nadie corre es decoración; un test que falla y nadie mira puede ser un defecto real sin atender — se distinguen, no se colapsan.

Reglas para recomendar:

«Nunca falló» no es por sí solo «no sirve»: un test puede prevenir sin fallar. La recomendación de eliminar exige además que la afirmación que protege ya no exista, que otra guarda la cubra, o que su costo supere lo que protege.
T-REPRO y la verificación de sellos se pueden abaratar, nunca eliminar.
Nada que proteja abrir dato, congelar spec, adoptar o borrar se recomienda eliminar.
Las reglas de contenido (§3 de las instrucciones) quedan fuera.

P6 · Informe forense/analisis/ci-medicion-1/INFORME-ci-medicion-1-v1_0.md, que abre con las cinco metas de dirección y dónde está hoy cada una medida en el runner:

Meta    Objetivo
Trabajo posterior a CONSUMIDO (mediana)    ≤ 10 min
PR con renumeración    0
PR con dos o más re-fusiones    < 10 %
Suite local    ≤ 60 s
Ejecuciones de la suite por cierre    1

Y cierra con el ahorro estimado de cada recomendación de la lista, en segundos por corrida y por acto, para que dirección decida con el precio a la vista.

P7 · Cierre. Cascada de /acto, check.py --baseline --parallel VERDE o PARO, ## NO-CORRIDO / RESERVAS al final del encargo («Ninguno.» es obligatorio), ## CONSUMIDO con el PR real. La nota de cierre lleva basename distinto del encargo (T02) y los rótulos nuevos van con prefijo de espacio (T25).

6 · LATITUD

El cómo es tuyo: gh run list, gh api o gh run view --log; el formato de los TSV; si bajas todos los logs o una muestra —si es muestra, se declara cuál y por qué—. El script de medición vive en la carpeta del análisis, como en optimiza-verificacion-ci/: es de un solo uso, no es infraestructura, no se cablea en CI. Un obstáculo reversible y barato se resuelve y se declara (D-19).

7 · PAROS — lista cerrada

Sin credenciales de lectura de Actions (con la receta de P0) · relanzar, cancelar, borrar o disparar cualquier workflow · escribir el token en cualquier parte · abrir microdato · modificar un test, un workflow, check.py o acto.md · eliminar o desactivar cualquier comprobación · objetivo inalcanzable. Fuera de esta lista no se para: se resuelve, o se pregunta a mesa con opciones y recomendación y se sigue con lo demás.

8 · PERÍMETRO

Escribes en: forense/analisis/ci-medicion-1/ (datos, script, informe) · forense/encargos/ (este encargo) · forense/notas/ (nota de cierre) · forense/hallazgos.md · forense/no-corrido.tsv · y la cascada de gobernanza que cierre_acto.py --aplica reconcilia. Más el perímetro de cierre permanente (D-21). Si te encuentras escribiendo fuera de esta lista, PARA.

No tocas: tests/ · .github/workflows/ · .claude/commands/ · tools/ · data/ · milpa/ · ningún CALC.

9 · LO QUE NO HACE · SUCESORES

No elimina, no abarata y no desactiva nada: mide y recomienda · no dispara corridas nuevas · no rediseña la cascada ni los ids de ADR · no toca la línea L0. Sucesores: el acto de velocidad que dirección decida con esta lista, y el diseño de ADR con raíz de acto y de la L0 derivada, que atacan la causa de las re-fusiones.

10 · FALSADOR (§9)

Si la lista sale con cero recomendaciones de abaratar o eliminar, o las metas de dirección ya se cumplen en el runner, el diagnóstico de dirección estaba mal y se dice así en la primera línea del informe.

## NO-CORRIDO / RESERVAS

- Ninguno.

## CONSUMIDO

`PR #955` (rama `acto/gen2-tuberia-ci-medicion-1`), 21/sep/2026. Entregables:
`forense/analisis/ci-medicion-1/` (43 archivos: scripts de un solo uso,
TSV con universo y conteo declarados, `runs.json`/`jobs.json` crudos de
`gh api`, informe `INFORME-ci-medicion-1-v1_0.md`); `ADR-587`
(`canon/gobernanza-v1_15.md`); anotación `L0` nueva
(`canon/estado-programa-v1_14.md`); rótulo censado
(`canon/registro-rotulos.tsv`); hallazgo sobre el tamaño de la línea `L0`
(`forense/hallazgos.md`); nota de cierre
(`forense/notas/2026-09-21-GEN2-TUBERIA-CI-MEDICION-1-cierre.md`).
`tests/check.py --baseline --parallel` VERDE (dos veces). Sólo lectura
sobre GitHub: ningún workflow se relanzó, canceló ni disparó; `tests/`,
`.github/workflows/`, `.claude/commands/`, `tools/`, `data/` y `milpa/`
sin tocar.

**Vuelta 2 (`ADENDA-1`, `forense/encargos/2026-09-21-GEN2-TUBERIA-CI-MEDICION-1-ADENDA-1.md`),
21/sep/2026 — mismo `PR #955`, misma rama.** `main` fusionado (24 commits);
`ADR` renumerado `587 → 588` (`PR #949`/`ACTO GEN2-TUBERIA-RES-LLAVE-1`
tomó `587` mientras este PR seguía abierto). Cinco correcciones sobre el
informe y la lista del barrido: (A2) `p4b_refusiones_por_pr.py` contaba
re-fusión por mensaje de commit y subcontaba a la mitad — reescrito para
contar todo commit de dos padres, sale 78.3%/47.0% (confirma el
antecedente de TUBERÍA); (A3) T16 aparecía como "señal real" con 66
fallos — medido que las 66 son eco (otro test falla en la misma
ejecución), cero fallos propios; la recomendación ELIMINAR no cambia, la
evidencia que la sostiene sí; (A4) 27 de 53 filas de
`barrido-check-tests.tsv` sin `nacimiento_citas` — completadas contra
`tests/check.py`, `SIN-DEFECTO-CITADO` donde no hay ninguno; (A5) la
recomendación de saltar el `check.py` interno de `cierre_acto.py` ahora
dice "mismo árbol", no "commit reciente"; (A6) dos líneas en el informe
sobre por qué `runs.json`/`jobs.json` se quedan, y hallazgo
`PARA-v2.16` sobre archivar encargos adjuntos, no pegados/renderizados.
`tests/check.py --baseline --parallel` VERDE sobre el árbol fusionado.
El encargo original y su sello: sin cambios de bytes.

**Vuelta 3 (mismo `PR #955`, sin adenda nueva — autorizada por
ADENDA-1 §5: "si main vuelve a moverse, fusiona otra vez y re-deriva el
ADR").** Entre el push de la vuelta 2 y la verificación del PR, `main`
avanzó otros 12 commits; `ACTO MOTOR-THETA-CONGELADA-1` (`PR #947`)
también tomó `ADR-588`. Renumerado de nuevo, a `ADR-589`. Mismo
procedimiento: conflictos resueltos en `canon/gobernanza-v1_15.md` y
`canon/estado-programa-v1_14.md` (tres anotaciones `L0` encadenadas,
589→588→587), los tres contadores mecánicos reconciliados,
`tests/check.py --baseline --parallel` VERDE.

**Vuelta 4 (mismo `PR #955`).** 8 commits más; `ACTO
GEN2-CELDA-D-PILOTO-3-COMMIT-1-v1_3` (`PR #958`) también tomó `ADR-589`.
Renumerado a `ADR-590`. Cuarta anotación `L0` encadenada
(590→589→588→587), tres contadores reconciliados, suite VERDE. Cuatro
vueltas para cerrar un acto que sólo mide: el informe (P7) lo cita como
la medición más directa de su propio mandato.
