# ENCARGO · ACTO GEN2-TUBERIA-VISTA-NORMALIZADA-2 · Sucesor del -1 (PARO por premisa de dirección, #1109): destraba el canal hoy moviendo los tres campos constantes por corrida, y cumple los 50 MB sacando `camino_linaje` de la vista por deduplicación o cálculo bajo demanda

> ENTORNO: **NUBE**. Hook imprime ENTORNO-DERIVADO; si dice CAJA, PARA.

CABECERA · SHA de redacción: el de `main` al abrir (re-deriva) · una sola sesión, rama propia `acto/gen2-tuberia-vista-normalizada-2` (D-17) · MODELO: Opus · MODO: ABIERTO · ids con raíz de acto (D-24) · D-21 aplica · «Si te encuentras escribiendo fuera de la lista de §9, PARA.» · cierre por /acto: `## NO-CORRIDO / RESERVAS` («Ninguno.» obligatorio si aplica) y `## CONSUMIDO` al pie.
CONTADOR: cero mediciones; no adopta; **ningún valor de ningún RESULT cambia** (test de equivalencia del multiconjunto {resultado_id, valor, estado, cuenta_gen2} antes/después, y `join` que reconstruye cada fila completa).

## 1 · OBJETIVO
Dos commits en un acto, cada uno con su criterio:
- **COMMIT-A (destrabar):** `tolerancia`, `funciones_dependencia` y `fuente_replay` —demostrados constantes por `corrida_id` en #1109— salen de `resultados.tsv` y viven una vez por corrida; guarda de tamaño en `verify.yml` antes del paso de derivados: **falla a 100 MB, avisa a 50**. Tras fusionar, el primer `derivados/auto-*` abre PR y `check` VERDE. `resultados.tsv` re-derivado ≈ 70 MB (cifra de #1109; se mide y se pega).
- **COMMIT-B (cumplir):** `camino_linaje` (≈497 chars/fila, no constante por corrida: 262/313) sale de la vista. Regla decidida por medición, no por gusto: `n_distinct(camino_linaje) / n_filas` sobre el archivo completo; si < 0.5 → tabla `data/corrida0/linajes.tsv` (`linaje_id` = sha1 del texto, `camino`) y `resultados.tsv` lleva `linaje_id`; si ≥ 0.5 → el campo no se almacena y `tools/vista.py` lo deriva bajo demanda (resultado → corrida → spec → inputs), con test de que reproduce el texto original para una muestra de 500 filas. Resultado: `resultados.tsv` < 50 MB; la guarda baja a **falla a 50** en este mismo commit.
«Hecho» sobre el commit final con origin/main fusionado: un `derivados/auto-*` posterior a COMMIT-A con `check` VERDE (run y PR citados) · `ls -la data/corrida0/resultados.tsv` < 50 MB tras COMMIT-B · test de equivalencia VERDE · los 18 consumidores (`git grep -l 'resultados.tsv\|camino_linaje\|funciones_dependencia' -- tools tests`) adaptados con test · spec de la vista en `data/INFRAESTRUCTURA-v1_0.md` actualizada antes de cada commit · `status` idéntico en contadores antes/después · `check.py --baseline` VERDE sin `--force`.

## 2 · FIRMAS DE MESA (propuesta; sustituye a la del -1 en un solo punto; mesa la da verbatim al lanzar; sin ella §7 f)
«Las vistas derivadas se normalizan: los campos constantes por corrida viven una vez por corrida; `camino_linaje` sale de `resultados.tsv` por deduplicación o cálculo bajo demanda según su cardinalidad medida; la guarda de CI falla a 100 MB y avisa a 50 hasta que `camino_linaje` salga, y desde entonces falla a 50; ningún archivo derivado vuelve a superar 50 MB; sin Git LFS y sin sacar la vista del canal. Publicar a ~70 MB entre COMMIT-A y COMMIT-B está autorizado.»

## 3 · LO QUE DIRECCIÓN SABE
- `[LEÍDO]` #1109 (ADR y nota del -1): GH001 real, run `36034606289`, re-derivado 155 MB; `tolerancia`, `funciones_dependencia`, `fuente_replay` constantes por corrida; `camino_linaje` no (262/313); solo con los tres constantes ≈ 70 MB; tres opciones documentadas. **Premisa falsa del -1 era de dirección** (`[SUPUESTO]` constancia del linaje); este encargo la corrige con la regla de cardinalidad.
- `[EJECUTADO]` (24/sep) `resultados.tsv` 85.8 MB en main, 65 289 filas, 26 columnas; ~1 206 bytes/fila; `camino_linaje` ≈ 41 % del archivo. Ningún `[deriva]` desde el 23/sep 23:30. #1101 fusionado (marcador en dos pasadas en el paso de derivados: se hereda).
- `[SUPUESTO]` que ninguno de los 18 consumidores lee `camino_linaje` para decidir algo (es trazabilidad, no medición). **Verifícalo primero**: `git grep -n camino_linaje -- tools tests`; si alguno decide con él, ese consumidor pasa por `vista.py` y se dice.
- ADJUNTOS: ninguno.

## 4 · YA HECHO / YA DECIDIDO
`git ls-remote --heads origin | grep vista` → 0 (el -1 cerró con PARO y su rama se borra al fusionar #1109). `grep -c 'size\|MB' .github/workflows/verify.yml` → reporta (no debe haber guarda aún).

## 5 · PIEZAS
- **P1 · COMMIT-A.** Spec de la vista (INFRAESTRUCTURA) → `registro --escribe` con los tres campos en `corridas.tsv` → `tools/vista.py join` → consumidores adaptados → guarda 100/50 → test de equivalencia → medir tamaño re-derivado y pegar.
- **P2 · Prueba real A.** Merge por mesa (o auto-merge si aplica) → run → `derivados/auto-*` con `check` VERDE; cita.
- **P3 · COMMIT-B.** Cardinalidad medida y pegada → dedupe o bajo demanda → spec → consumidores → guarda a 50 → test de reproducción del linaje (500 filas) → tamaño final pegado.
- **P4 · Cierre.** NC `…749c-03` cerrada `SUSTITUIDO-POR: este acto`; FP V (cola de fusión) marcada `EJECUTA: mesa` con receta de un minuto en la nota.

## 6 · LATITUD
Dónde viven los campos y el nombre de la tabla: tuyos. ≤ 10 líneas adyacentes: sí. Pregunta a mesa (sigues con A): solo si un consumidor decide con `camino_linaje` y no puede pasar por `vista.py`.

## 7 · PAROS — lista cerrada
a) no aplica · b) tocar un sello, un RESULT, `--force`, `--excluye`, comprimir o binarizar, Git LFS, sacar la vista del canal · c) mover contadores a mano · d) no aplica · e) CAJA · f) el canal ya publica bajo 50 MB en origin/main.

## 8 · COMPUERTAS
«Test de equivalencia antes/después en los dos commits» protege: **congelar**. «Spec antes que código, en cada commit» protege: **congelar** (D-15). «Guarda en CI» protege: **borrar** (un GH001 silencioso es una publicación perdida).

## 9 · PERÍMETRO Y CONCURRENCIA
Propio: `tools/corrida0.py` (solo `registro --escribe` y lectura de vistas), `tools/vista.py` (nuevo), los 18 consumidores, `data/INFRAESTRUCTURA-v1_0.md` (sección de vistas), `.github/workflows/verify.yml` (guarda), `data/corrida0/*.tsv` solo por el derivador, tests, `no-corrido.tsv`/`firmas-pendientes.tsv` (estado/append), nota, L0, cascada. Ajeno: CALC, `marcador_segmento.py`, el paso del marcador en `verify.yml` (#1101), `.claude/`. En vuelo: ADOPCION-BLOQUE-Y-PINES-2 (por escribir; toca `decisiones.tsv`, no la vista), U0 mapa-dominios (mesa), MOTOR-DEUDA-LOTE-2.

## 10 · LO QUE NO HACE · SUCESORES
No decide qué se publica; no adopta. Sucesor: ninguno si «Hecho»; -3 solo si COMMIT-B deja un consumidor `DIFERIDO-A`.

## NO-CORRIDO / RESERVAS

- **qué**: P3 · COMMIT-B (cardinalidad medida y pegada, dedupe o bajo demanda, spec, consumidores, guarda a 50, test de reproducción de 500 filas, tamaño final). **por qué**: `DIFERIDO-A` -- cardinalidad medida (n_distinct(camino_linaje)/n_filas = 1.0 sobre las 65 287 filas de main, regla del encargo: ≥0.5 → bajo demanda, no dedup); implementar la derivación bajo demanda fielmente y su test de reproducción de 500 filas es pieza propia con su propio riesgo de correctitud -- camino_linaje es exactamente el campo que la disciplina de procedencia del proyecto (A.7, D-24, E.2) más cuida, y apresurarla en el mismo acto que COMMIT-A habría sido exactamente lo que este trámite evita. **impacto**: resultados.tsv sigue sin bajar de ~70 MB (autorizado por la firma de mesa); el umbral de 50 MB firmado no se cumple en su forma literal hasta que corra el sucesor. **sucesor**: `GEN2-TUBERIA-VISTA-NORMALIZADA-3`.
- **qué**: P2 · Prueba real A (merge por mesa → run → `derivados/auto-*` con check VERDE, cita del run y del PR). **por qué**: `NO-VERIFICABLE-AQUÍ` -- depende de que mesa fusione este PR; el job de derivados corre automáticamente tras el push a `main`, fuera del alcance de esta sesión. **impacto**: sin cita del run real hasta que mesa fusione. **sucesor**: se completa solo, vía el job `guardias` de `verify.yml` tras el merge; si algo falla ahí, `GEN2-TUBERIA-VISTA-NORMALIZADA-3` lo hereda junto con COMMIT-B.
- **qué**: P4 · Cierre -- NC `…749c-03` cerrada `SUSTITUIDO-POR: este acto`; FP V marcada `EJECUTA: mesa`. **por qué**: `FUERA-DE-PERÍMETRO` -- ya resuelto por `GEN2-TRAMITE-FIRMAS-15-ADENDA-1` (mesa firmó V como `FIRMADA`, `EJECUTA: mesa`, gateada a que este acto devuelva el canal a verde); `NC-…-749c-03` no se re-verificó en este acto (fuera de perímetro declarado, §9). **impacto**: ninguno -- ya cubierto por el acto que corresponde. **sucesor**: ninguno, ya resuelto.

## CONSUMIDO

PR #1113 (ACTO GEN2-TUBERIA-VISTA-NORMALIZADA-2, ADR-260924-GEN2-TUBERIA-VISTA-NORMALIZADA-2-f1b2-01). COMMIT-A completo y verificado; P2 (prueba real) depende del merge de mesa; COMMIT-B y su spec/consumidores propios NO-CORRIDO, sucesor GEN2-TUBERIA-VISTA-NORMALIZADA-3.
