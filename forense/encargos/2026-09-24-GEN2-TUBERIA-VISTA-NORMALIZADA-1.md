# ENCARGO · ACTO GEN2-TUBERIA-VISTA-NORMALIZADA-1 · El canal de derivados vuelve a publicar: `resultados.tsv` deja de cargar por fila lo que es de la corrida, cae por debajo del límite de GitHub, y una guarda de tamaño en CI impide que vuelva a pasar

> ENTORNO: **NUBE**. Hook imprime ENTORNO-DERIVADO; si dice CAJA, PARA.

CABECERA · SHA de redacción `4bf351ef` (re-deriva al abrir; actualizado 24/sep 11:30 tras la fusión de #1101) · una sola sesión, rama propia `acto/gen2-tuberia-vista-normalizada-1` (D-17) · MODELO: Opus · MODO: ABIERTO · ids con raíz de acto (D-24) · D-21 aplica · «Si te encuentras escribiendo fuera de la lista de §9, PARA.» · cierre por /acto: `## NO-CORRIDO / RESERVAS` («Ninguno.» obligatorio si aplica) y `## CONSUMIDO` al pie.
CONTADOR: cero mediciones; no adopta; la vista es derivada y se re-deriva: **ningún valor de ningún RESULT cambia** (test: el conjunto {resultado_id, valor, estado, cuenta_gen2} antes y después es idéntico).

## 1 · OBJETIVO
Que el push de `derivados/auto-*` vuelva a entrar: hoy falla con GH001 porque `data/corrida0/resultados.tsv` (85.8 MB en main; 129–155 MB re-derivado; 65 289 filas × ~1.2 KB) supera los 100 MB de GitHub. El 40 % de cada fila es `camino_linaje` (≈497 caracteres) y otros campos que son **de la corrida, no del resultado** (`tolerancia`, `funciones_dependencia`, `fuente_replay`): se repiten por cada RESULT de la misma corrida. Normalizarlos a `corridas.tsv` (o a `linajes.tsv` con llave `corrida_id`) baja el archivo a ~40 MB sin perder un dato, y una guarda en CI (`≤ 50 MB` por archivo derivado, o PARO del job con mensaje claro) evita el siguiente GH001. Habilita: todo lo que espera un `[deriva]` — el marcador (#1101), `adoptados` 72 → 87, el bloque ENIGH, los pines (ADOPCION-BLOQUE-Y-PINES-1).
«Hecho» sobre el commit final con origin/main fusionado: el primer `derivados/auto-*` posterior abre PR y `check` VERDE en él · `ls -la data/corrida0/resultados.tsv` < 50 MB (y ningún derivado > 50 MB) · test de equivalencia VERDE (mismo multiconjunto de RESULT y valores antes/después; los campos movidos se reconstruyen por `corrida_id` con `join`) · guarda de tamaño en `verify.yml` con test propio · `status` da los mismos contadores que antes de la normalización (pegar antes/después) · `check.py --baseline` VERDE sin `--force`.

## 2 · FIRMAS DE MESA — dada el 24/sep/2026 («firmo las recomendaciones»), verbatim; viaja en este encargo y la asienta este acto al ejecutarla (A.12)
«Las vistas derivadas se normalizan: los campos de corrida (`camino_linaje`, `tolerancia`, `funciones_dependencia`, `fuente_replay` y los que el ejecutor demuestre constantes por `corrida_id`) salen de `resultados.tsv` y viven una vez por corrida; ningún archivo derivado supera 50 MB y CI lo garantiza; no se usa Git LFS ni se saca la vista del canal.»

## 3 · LO QUE DIRECCIÓN SABE
- `[EJECUTADO]` (`4bf351ef`) `resultados.tsv` 85.8 MB, 26 columnas, 65 289 filas; muestra de 3 000 filas: `camino_linaje` 497 chars/fila, `tolerancia` 160, `funciones_dependencia` 114, `fuente_replay` 100; ~1 206 bytes/fila. `corridas.tsv` 5.0 MB; `marcador-segmento.tsv` 0.1 MB. `.gitattributes` sin LFS.
- `[REPORTADO]` por la sesión CLI de #1101: canal caído desde `0edf93e2` (23/sep 19:15Z), GH001 en cada push de `derivados/auto-*`, `check` rojo en cada push a main, cero `[deriva]` desde #1074; NC `…CONTADORES-CONSUMO-2-749c-03`. **Verifícalo** con el run de Actions más reciente (id citado) y el tamaño del artefacto que intentó empujar.
- `[SUPUESTO]` que los cuatro campos son constantes por `corrida_id` (por diseño lo son: linaje, tolerancia y funciones son de la spec/corrida). **Demuéstralo por comando** antes de mover cada uno: `n_distinct(campo) por corrida_id == 1` en todo el archivo; el que no lo sea se queda en `resultados.tsv` y se dice.
- `[LEÍDO]` `tools/corrida0.py registro --escribe` produce las vistas; `tools/derivados_protegidos.py` impide commit manual. `[EJECUTADO]` `git grep -l 'resultados.tsv\|camino_linaje\|funciones_dependencia' -- tools tests` → **18 archivos**: son los consumidores a adaptar en el mismo PR, cada uno con test. `[EXISTE]` la descripción de las vistas vive en `data/INFRAESTRUCTURA-v1_0.md` (única mención de `resultados.tsv` como spec): es la spec humana que P2 actualiza antes del código (D-15).
- ADJUNTOS: ninguno.

## 4 · YA HECHO / YA DECIDIDO
`git log --oneline -5 -- tools/corrida0.py | grep -i 'vista\|resultados.tsv'` → reporta. `git ls-remote --heads origin | grep -i vista` → 0. #1101 **ya fusionó**: el paso de derivados de `verify.yml` corre `marcador_segmento.py --escribe` en dos pasadas (4 menciones al `4bf351ef`); se hereda tal cual y la guarda de P3 va **antes** de ese paso, no dentro.

## 5 · PIEZAS
- **P1 · Diagnóstico.** Run de Actions con el GH001; tamaño exacto del `resultados.tsv` re-derivado; tabla de campos × bytes/fila sobre el archivo completo; verificación de constancia por `corrida_id` de cada campo candidato.
- **P2 · Normalización.** `registro --escribe` escribe los campos constantes una vez por corrida (en `corridas.tsv` si cabe, o `linajes.tsv`); `resultados.tsv` conserva `corrida_id` como llave; función `join` en `tools/vista.py` (nueva, pequeña) para reconstruir la fila completa; todos los consumidores pasan por ella o por `corrida_id`. Spec humana de la vista (D-15) actualizada antes del código.
- **P3 · Guarda.** En `verify.yml`, antes del push de derivados: `find data/corrida0 -name '*.tsv' -size +50M` → si encuentra, el job falla con mensaje que nombra el archivo y esta NC; test propio. Umbral 50 MB, no 100: margen para crecer.
- **P4 · Prueba real.** Merge por mesa → el push a main dispara el job → `derivados/auto-*` abre PR y `check` VERDE; cita del run y del PR en la nota; `status` antes/después idéntico en contadores.

## 6 · LATITUD
Dónde viven los campos (corridas.tsv vs linajes.tsv) y el nombre de la función: tuyos. ≤ 10 líneas adyacentes: sí. Pregunta a mesa (sigues): si un consumidor de la vista no puede adaptarse sin tocar un CALC sellado (no debería: la vista es derivada).

## 7 · PAROS — lista cerrada
a) no aplica · b) tocar un sello, un RESULT, `--force`, `--excluye`, comprimir o binarizar la vista, Git LFS, sacar la vista del canal · c) mover contadores a mano · d) no aplica · e) CAJA · f) el canal ya publica en origin/main (demuéstralo con un `[deriva]` posterior a `0edf93e2`).

## 8 · COMPUERTAS
«Test de equivalencia del multiconjunto de RESULT antes/después» protege: **congelar** (la vista publica lo sellado, sin cambiar un valor). «Spec de la vista antes que el código» protege: **congelar** (D-15). «Sin LFS ni sacar la vista» protege: **borrar** (la publicación es parte del sello público).

## 9 · PERÍMETRO Y CONCURRENCIA
Propio: `tools/corrida0.py` (solo `registro --escribe` y lectura de vistas), `tools/vista.py` (nuevo), los consumidores de la vista listados en P1, la spec humana de la vista, `.github/workflows/verify.yml` (guarda y, si hace falta, el paso de derivados), `data/corrida0/*.tsv` **solo por el derivador**, tests, `no-corrido.tsv`, nota, L0, cascada. Ajeno: CALC, `marcador_segmento.py`, `celdas_validadas.py` salvo su lectura de la vista, `.claude/`. En vuelo: ADOPCION-BLOQUE-Y-PINES-1 (toca `decisiones.tsv`, escritor, pines; no la vista), AUDITORIA-POST-HOC, mapa-dominios (Claude Code), FIRMAS-14.

## 10 · LO QUE NO HACE · SUCESORES
No decide qué se publica, no adopta. Sucesores: ninguno si «Hecho»; `GEN2-TUBERIA-VISTA-NORMALIZADA-2` si algún consumidor queda `DIFERIDO-A`.
