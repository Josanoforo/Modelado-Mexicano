ESTADO: LISTO-NUBE
ENTORNO: NUBE
ENCOLADO: 2026-09-08 · ACTO GEN2-T7 (D9/D10 · FP-339, `/encola`). Nace de la salvedad dejada por `ACTO GEN2-E3 · AUTOMATIZA-GEN2-1` (`forense/encargos/cola/2026-09-07-GEN2-E3-AUTOMATIZA-GEN2-1.md` · CONSUMIDO) y de la corrección aplicada por este mismo acto a las compuertas de `GEN2-E5`/`GEN2-E6` (v1.2).
BITACORA:
- 2026-09-08 · LISTO-NUBE · encolado por GEN2-T7. COMPUERTA: ninguna -- este encargo no depende de que nada más fusione primero; endurece texto de encargos ya en cola, no código de producción.

──── CUERPO VERBATIM DEL ENCARGO (A.3) · el despachador NO lo edita ────

## E3.1 · ACTO GEN2-E3.1 · ENDURECE-CALC — compuertas verificables de las piezas de cálculo restantes

Cabecera: NUBE · **Sonnet** · sin COMPUERTA de fusión previa.

Por qué existe: la salvedad de `GEN2-E3` declara verbatim que su propia BITACORA pedía `git show origin/main:tools/corrida0.py | grep -c "def demanda"` → 1, y ese comando devuelve **0** aunque `cmd_demanda` exista y esté fusionado -- `"def demanda"` nunca es subcadena de `"def cmd_demanda"`. Una compuerta con un comando estructuralmente irrealizable es peor que ninguna: hace parar en falso a la siguiente sesión que la corra al pie de la letra, sin que el texto delate el error hasta que alguien lo ejecuta (`forense/hallazgos.md`, entrada GEN2-T7). `GEN2-T7` ya corrigió las compuertas de `GEN2-E5`/`GEN2-E6` a v1.2 con este mismo criterio; este encargo generaliza la revisión al resto de la cola de cálculo que cite funciones de `tools/corrida0.py` o archivos de `main` en su compuerta.

Qué hace:
1. Censa con `grep -n "^def cmd_" tools/corrida0.py` el nombre REAL de cada subcomando implementado (`cmd_demanda`, `cmd_spec_check`, `cmd_negativo`, `cmd_preflight`, `cmd_run`, `cmd_verify`, y los que agregue `GEN2-E6`: `cmd_registro`, `cmd_status`).
2. Recorre `forense/encargos/cola/*GEN2*` y cualquier encargo GATEADO/LISTO-* cuya compuerta cite un `grep`/`def` sobre `tools/corrida0.py` u otro archivo de `main`: verifica que el patrón citado sea subcadena literal del nombre real (nunca `"def demanda"` por `"def cmd_demanda"`, nunca el nombre corto de una pieza por el nombre real de la función que la implementa).
3. Donde la compuerta cite un archivo o directorio del árbol de trabajo local (`ls`, `test -f`, `cat` sin `git show`) para verificar un estado de `main`, la reescribe a `git show origin/main:<ruta> | …` (para directorios, `git show origin/main:<ruta>` lista el árbol; para archivos, `sha256sum`/`grep` sobre la salida) -- mismo patrón aplicado en este acto a `GEN2-E5`/`GEN2-E6`.
4. Dos commits: uno con el censo de `def cmd_*` (`forense/notas/2026-09-0X-GEN2-E3-1-censo-compuertas.md`, salida cruda del `grep`), otro con las ediciones puntuales a cada encargo tocado (BITACORA nueva línea, `v1.2` o siguiente, sin borrar el texto verbatim previo -- mismo patrón que este acto usó en `GEN2-E5`/`GEN2-E6`).
5. Para cada compuerta corregida, corre el comando nuevo contra `origin/main` real y pega la salida en la nota -- una compuerta que este acto declara corregida y no corrió, no cuenta como corregida.

A.8: `grep -c "def demanda\"" forense/encargos/cola/*.md` (o cualquier variante `def <pieza-corta>` que no sea subcadena de `def cmd_<pieza-corta>`) → 0 al cerrar. `grep -rn "ls data/corrida0/ \| grep" forense/encargos/cola/*.md` (comprobación local sin `git show`, sobre estado de `main`) → 0 al cerrar.

Perímetro: `forense/encargos/cola/*.md` (solo la BITACORA de cada encargo tocado, nunca el cuerpo verbatim del acto original) · `forense/notas/2026-09-0X-GEN2-E3-1-censo-compuertas.md` · `forense/hallazgos.md` (si aparece un caso nuevo de la misma clase) · cascada. **No toca `tools/corrida0.py`, `milpa/**`, canon ni specs.** Si te encuentras escribiendo fuera de esta lista, PARA — el perímetro estaba mal calculado y saberlo vale más que el atajo.

Contador: cero GEN2 (endurece texto de encargos, no mide nada). Sucesor: ninguno declarado; los encargos corregidos siguen su propio camino de despacho.
