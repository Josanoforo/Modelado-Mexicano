# ENCARGO · ACTO GEN2-CORRIDA0-RENDIMIENTO-1

**SHA de redacción:** `adcfa978` (`adcfa97892d57d266c84b08c414b835283652ca0`,
`origin/main` al abrir el acto; re-derivado en sesión: HEAD == origin/main == adcfa978,
0 adelante / 0 atrás).
**Entorno asignado:** NUBE. **El que NO:** caja (no abre microdato).
**Sesión / rama:** `claude/vibrant-goldberg-oxbn3o` (una sola sesión, D-17).
**Estado:** CONSUMIDO — PR de este acto (ver `## CONSUMIDO` de la nota
`forense/notas/2026-09-20-GEN2-CORRIDA0-RENDIMIENTO-1.md`).
**Modelo:** Opus.
**Compuerta:** ninguna.
**CONTADOR:** `cuenta_gen2 = NO` — no mide nada del programa; ningún contador
puede moverse.

## VERIFICACIÓN DE EXISTENCIA (A.8, contestada con comandos)

1. **Estructura.** El dominio es el CLI del registro GEN2, no una tabla de
   `data/INFRAESTRUCTURA-v1_0.md`: gobiernan `tools/corrida0.py` (4517 líneas),
   `tools/sella_sha256.py` (173) y `tests/check.py` (7559).
   `wc -l tools/corrida0.py tools/sella_sha256.py tests/check.py` → 4517 / 173 / 7559.
2. **Contenido.** `ls -la tests/test_corrida0_oro.py` → `No such file or directory`
   (archivos examinados en `tests/`: 162 `.py`, A.13). El arnés de oro NO-ENCONTRADO
   en `tests/` con el patrón `test_corrida0_oro*`. La memoización de
   `_funcion_de_dependencia` NO-ENCONTRADA:
   `grep -nE "lru_cache|_cache|memo" tools/corrida0.py` (1 archivo examinado) devuelve
   `lru_cache` sólo en `:3343` (`_normaliza_ruta_repo`) y `:3408`
   (`_referencias_numericas_de_intermediario`), y los memos locales de
   `_propaga_envuelto` (`:3513`, `:3514`) — ninguno cubre `_funcion_de_dependencia`
   (`:3449`) ni `resuelve_entrada`/`origen_ruta`.
   `verifica()` en `tools/sella_sha256.py:113` **EXISTE-SATISFACE**: ya es función
   importable pura `(codigo, mensaje)`; P3 no necesita añadirla.
3. **Cobertura retroactiva.** `tools/corrida0.py` nace en ACTO GEN2-E2; el último
   trabajo sobre su rendimiento es el memo por `(calc_id, resultado)` que ya vive en
   `_propaga_envuelto` — ningún acto previo tocó `_funcion_de_dependencia` ni
   `_verifica_sello` por costo. No hay trabajo hecho que anule este encargo.

---

## Texto del encargo, verbatim como se lanzó

ENCARGO · ACTO GEN2-CORRIDA0-RENDIMIENTO-1 · CADA INVOCACIÓN DE `corrida0.py` CUESTA ~16 s Y TODO EL APARATO LO INVOCA: DOS FUNCIONES CONCENTRAN EL 85 %. SE ACELERAN SIN CAMBIAR UN BYTE DE SALIDA

ENTORNO: NUBE — NO caja. No abre microdato; mide tiempos y compara salidas.

CABECERA (D-12) · SHA de redacción `adcfa978`; re-deriva al abrir · una sola sesión, rama propia; `/acto` PARA si ya está archivado en otra rama viva · compuerta: ninguna · MODELO: Opus (toca el núcleo del registro; el riesgo es cambiar una derivación sin querer) · CONTADOR: `cuenta_gen2 = NO`; no mide nada del programa; ningún contador puede moverse — si `status` cambia en un solo campo, PARA · FP/ADR/NC: deriva al cierre.

Gate D-14. ¿Defecto observado? Sí: NC-0357 (`cierre_acto.py` agotó su límite de 300 s corriendo la suite y salió 124, no ROJO); dos sesiones de nube reportaron la suite "totalmente bufferizada, cero bytes tras ~25 min" y cerraron sin su veredicto (#894, P0 del piloto); el CI tiene `timeout-minutes: 10`. ¿Cambia una decisión? Sí: sesiones que fusionan sin baseline, o que lo esperan y no producen. ¿Cuesta menos que el defecto? Dos funciones.

LO QUE DIRECCIÓN MIDIÓ (contra `adcfa978`, en un entorno de 1 CPU; re-mídelo en el tuyo, las cifras absolutas no viajan)

* `python3 tools/corrida0.py status` → 15.9 s de pared. Importar el módulo: 0.1 s. Todo el costo es derivación.
* `cProfile` de `status` (32.8 s bajo el perfilador): `_filas_registro` → `_lee_oferta` 31.9 s, de los cuales `_propaga_envuelto` 20.3 s (`corrida0.py:3505`), con 273 385 llamadas a `_funcion_de_dependencia` (`:3449`), y `_verifica_sello` 8.2 s (`:2393`), que lanza 302 `subprocess.run` — un intérprete de Python nuevo por cada sello, para correr `sella_sha256.py --verifica`.
* En `tests/check.py --baseline --parallel`: `T32 T-CORRIDA0` = 67.2 s y `T35 T-REPRO` = 37.8 s; los otros 46 tests cronometrados suman ~19 s. `tests/test_corrida0.py` invoca a `corrida0` 13 veces. `--parallel` hoy solo aísla T35 (`max_workers=1`, `check.py:7441`).
* Quién más paga esos 16 s por llamada: `tablero_programa.py`, `digesto_tramite.py`, `marcador_segmento.py`, `cierre_acto.py`, el ARRANQUE de `/acto`, y cada `status` "antes/después" que los encargos piden.

PIEZAS

P0 · Red de seguridad ANTES de tocar nada (primer commit). Un arnés de oro: para `status`, `demanda`, `registro` (sin escritura) y los derivados que `corrida0` regenera, guarda la salida byte a byte de `origin/main` en un directorio temporal fuera del árbol, y un test (`tests/test_corrida0_oro.py`) que compara contra ella. Incluye los TSV derivados completos, no solo el resumen. Si hoy dos corridas seguidas de `status` no son idénticas entre sí, PARA: hay no-determinismo y eso es el hallazgo.

P1 · `_funcion_de_dependencia`: memoizar sin cambiar semántica. Es función pura de cuatro campos de su entrada (`funcion`, `origen`, `id`, `ruta`). Caché por esa tupla — no por identidad del dict. Verifica que `_normaliza_ruta_repo`, `_ruta_es_fuente_*` no lean estado mutable ni disco; si leen disco, la caché vive por invocación, no por proceso.

P2 · `_propaga_envuelto`: que cada `(calc_id, resultado)` se resuelva una vez. La recursión `resuelve_calc`/`origen_ruta` recorre linajes repetidos; memoiza por nodo respetando la pila de detección de ciclos — un ciclo debe seguir produciendo exactamente lo que produce hoy. Antes de optimizar, cuenta llamadas por nodo y reporta el factor de repetición: si no hay repetición, la hipótesis de dirección es falsa y se dice.

P3 · `_verifica_sello`: sin un intérprete por sello. Importa la verificación de `sella_sha256.py` como función, en proceso. Los tres estados de A.1 no se colapsan (`AUSENTE` · raíz-no-configurada · hash-discordante) y los mensajes quedan idénticos. Si `sella_sha256.py` no expone función importable, añade una sin cambiar su CLI.

P4 · Medición, antes y después, en el mismo entorno, tres repeticiones cada una: `status`, `demanda`, `tests/test_corrida0.py`, `check.py --baseline --parallel`. Reporta mediana y el entorno (`nproc`). No te doy meta. Si la ganancia de alguna pieza es < 10 %, revierte esa pieza: complejidad sin beneficio no entra.

P5 · Solo si sobra presupuesto y P0–P4 están verdes: que `--parallel` solape también T32 (hoy solo T35). Es una línea de pool; mide el efecto.

PERÍMETRO

`tools/corrida0.py` — solo las tres funciones nombradas y lo mínimo para cachearlas · `tools/sella_sha256.py` (exponer función, CLI intacta) · `tests/test_corrida0_oro.py` (nuevo) · `tests/check.py` solo P5 · nota · cascada. No toca ningún TSV derivado a mano · ningún CALC · `relevo_usos.py` · `marcador_segmento.py` · `tablero_programa.py`. «Si te encuentras escribiendo fuera de esta lista, PARA.»

LO QUE NO HACE

No añade caché en disco, ni índice persistente, ni base de datos (D-14: no se construye base central) · no cambia qué se deriva · no paraleliza `corrida0` por dentro.

CIERRE

Cascada D-10 · la nota abre con la tabla antes/después y la frase "salidas byte-idénticas: SÍ/NO" · `## NO-CORRIDO / RESERVAS` · `## CONSUMIDO`. Falsador a tres meses: si NC-0357 o un "suite sin veredicto" reaparece, esta mejora no resolvió el defecto y se anota.
