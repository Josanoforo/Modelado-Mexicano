# ADENDA 1 · ACTO GEN2-TUBERIA-CI-MEDICION-1 · UNA VUELTA SOBRE EL PR #955: FUSIONAR `main`, RENUMERAR EL `ADR`, Y CORREGIR TRES AFIRMACIONES DEL INFORME

**Qué es.** Una adenda al acto `GEN2-TUBERIA-CI-MEDICION-1`, que cerró con `## CONSUMIDO` en el PR #955 y **no está fusionado**. No es un acto nuevo: trabaja en la **misma rama** (`acto/gen2-tuberia-ci-medicion-1`) y en el **mismo PR** (#955). Se rige por la regla de adendas firmada el 21/sep: se archiva como archivo propio junto a su encargo, con su propio sello de cuerpo, **y el cuerpo sellado del encargo no se edita**.

**CABECERA** · revisado contra `main` `4bb29d96` y la cabeza del PR `22cb8dcf` (re-deriva al abrir; si `main` se movió no es PARO) · **ENTORNO: CAJA**, la misma sesión y worktree del acto si siguen vivos; si se lanza otra sesión, **puede ser NUBE**: esta vuelta no usa la API de GitHub ni abre corpus · una sola sesión sobre esa rama (D-17) · **MODO: ABIERTO** · **MODELO SUGERIDO: Opus** · **COMPUERTA: ninguna** (D-20) · **CONTADOR: `cuenta_gen2 = NO`** · vehículo: `/acto`.

**EL PR NO SE FUSIONA EN ESTA VUELTA**: se empuja a la misma rama y queda propuesto; mesa central fusiona.

---

## 1 · POR QUÉ ESTA ADENDA

TUBERÍA revisó el PR #955. La sustancia se sostiene —universo completo, cero tokens en el diff, perímetro limpio, las eras de `verify.yml` bien separadas, y el encargo es el primero sellado con la regla de sello de cuerpo, y pasa—. Pero no se puede fusionar como está: choca con `main`, y tres afirmaciones del informe están mal o incompletas. Todo lo que sigue es `EJECUTADO` por TUBERÍA salvo rótulo distinto.

## 2 · LO QUE TUBERÍA MIDIÓ SOBRE EL PR

- **No fusiona.** `main` avanzó **24 commits** desde la base del PR (`6b898108`). La fusión de prueba conflictúa en `canon/estado-programa-v1_14.md`, `canon/gobernanza-v1_15.md` y `canon/registro-rotulos.tsv`. Y **`ADR-587` ya lo tomó otro acto** en `main` (la entrada renumerada `583 → 586 → 587`).
- **El conteo de re-fusiones subestima a la mitad.** `p4b_refusiones_por_pr.py:31` reconoce sólo mensajes `Merge branch 'main'` o `Merge remote-tracking branch 'origin/main'`. La casa escribe la mitad de sus re-fusiones con otra forma: `GEN2-…: merge origin/main (…) y renumera`. Sobre los 78 PR fusionados entre el 18/sep y `73d7c816`: **126 merges en ramas de PR; el patrón reconoce 63 y se salta 63.** Contando todos: **35 de 78 PR con dos o más re-fusiones**; con el patrón del informe, 15. La nota del informe atribuye la diferencia a PR resincronizados por *rebase*; **no es esa la causa**.
- **T16 no atrapó nada por sí mismo.** En `fallos-tests-runner.tsv`, T16 falla en **66** corridas, y **en las 66 falla también al menos otro test fuera del baseline** (T02 en 51, T27 en 6, T30, T35, T26-bis y T25 en 4 cada uno). Cero fallos propios. El informe lo lista entre los tests que dan «señal real» y a la vez recomienda eliminarlo: la recomendación es correcta, la evidencia está mal leída. T16 falla **por eco** —la cuenta de FAIL cambió porque otro test falló—.
- **La lista está incompleta en «nacimiento».** En `barrido-check-tests.tsv`, **27 de 53** tests tienen vacía la columna `nacimiento_citas`. El encargo pedía, por test, el defecto que lo motivó, con archivo y línea.
- **Una recomendación puede aflojar una verificación.** «Saltar el `check.py` interno de `cierre_acto.py` cuando hay VERDE reciente» no dice **sobre qué árbol**. Si entre las dos corridas cambió algo, el salto deja pasar ese cambio sin suite.
- **El encargo quedó archivado sin formato.** El texto archivado es idéntico al entregado salvo encabezados, negritas, código y marcadores de lista: se pegó el texto renderizado, no el `.md`. **No se corrige** —ese cuerpo está sellado y es verbatim de lo que la sesión recibió—; se asienta como hallazgo del canal de lanzamiento.
- **Los JSON crudos se quedan.** `runs.json` y `jobs.json` suman unos 7.7 MB. Quitarlos en un commit nuevo **no reduce el repo**: la casa fusiona con merge commit, así que esos blobs quedan en la historia igual, y reescribir la historia de la rama está vedado. Quedan como materia prima de la medición.

## 3 · PIEZAS — resultado esperado, no receta

**A0 · Archivar esta adenda.** Como archivo propio, **junto al encargo**: `forense/encargos/2026-09-21-GEN2-TUBERIA-CI-MEDICION-1-ADENDA-1.md`, verbatim del **archivo** que recibas —no del texto renderizado—, con su sello `…-ADENDA-1.md.cuerpo.sha256` hecho con `python3 tools/sella_sha256.py --cuerpo`. Primer commit de la vuelta. El encargo original y su sello **no se tocan**.

**A1 · Fusionar `main` y renumerar.** Fusiona `origin/main` hacia la rama; resuelve los conflictos de los tres archivos **conservando todas las filas de los dos lados**. El `ADR` del acto se re-deriva al siguiente libre (quien fusiona segundo renumera), y se arreglan sus citas —la cabecera de gobernanza, la línea L0, el rótulo, el hallazgo, la nota de cierre y el `## CONSUMIDO`—. **Se renumera por colisión, no por contigüidad**: `T15` acepta huecos desde `#939`. Ningún `NC` ni `FP` con raíz de acto se renumera: no pueden chocar.

**A2 · Corregir la meta de re-fusiones.** `p4b_refusiones_por_pr.py` cuenta como re-fusión **todo commit con dos padres en la rama del PR**, sin mirar el mensaje. Se re-corre y se reescriben `refusiones-por-pr.tsv`, la fila de la tabla de metas del informe y la nota metodológica de P4: fuera la explicación del *rebase*; dentro la causa medida —el patrón reconocía la mitad de los merges— con su conteo. La cifra propia se deriva, no se copia: la de TUBERÍA (35 de 78, otra ventana) es **referencia para comparar**, no valor esperado. Si difieren en orden de magnitud, se declara por qué.

**A3 · Reescribir la evidencia de T16.** Con un comando sobre `fallos-tests-runner.tsv` que cuente las corridas en que T16 falló **sin** ningún otro fallo fuera del baseline (T06/T08). Con ese número: T16 sale de la lista de tests con «señal real» en P3, y su fila en `barrido-check-tests.tsv` justifica ELIMINAR con dos hechos —cero afirmaciones vigentes que comparar hoy (medido por TUBERÍA) y cero fallos propios en CI—. Y se dice **qué le costaría a un lector** eliminarlo: nada que otra guarda no atrape antes.

**A4 · Completar «nacimiento».** Para cada uno de los 27 tests con la columna vacía, lee su cabecera en `tests/check.py` (la línea ya está en la columna `linea`) y escribe el defecto que declara, con `tests/check.py:<línea>`. **Si la cabecera no declara ningún defecto**, escribe `SIN-DEFECTO-CITADO (tests/check.py:<línea>)`: eso también es evidencia para la caducidad, y no se inventa un motivo. Cero filas vacías al terminar.

**A5 · Precisar el salto de la cascada.** La recomendación queda: saltar la suite interna de `cierre_acto.py` **sólo si hay un VERDE sobre el mismo árbol** —mismo hash de árbol que el que se va a verificar—; si el árbol cambió, la suite corre. El ahorro estimado no cambia.

**A6 · Dos líneas en el informe y un hallazgo.** En el informe: por qué los JSON crudos se quedan (§2). En `forense/hallazgos.md`, como **semilla PARA-v2.16**: *un encargo se lanza adjuntando su archivo `.md`, no pegando su texto renderizado; el archivado verbatim de un texto renderizado pierde su estructura*, con este acto como caso.

**A7 · Cierre de la vuelta.** `python3 tests/check.py --baseline --parallel` en **LÍNEA BASE VERDE** sobre el árbol con `main` fusionado. En la sección de cierre del encargo —al final, que es lo único que se puede tocar— una línea que cite esta adenda y lo que cambió; el `## CONSUMIDO` sigue apuntando al PR #955, verificado contra el HEAD remoto. Empuja a la misma rama.

## 4 · CRITERIO DE «HECHO» — por comando, con salida cruda en la nota

1. La fusión de prueba de la rama con `origin/main` no deja conflictos, y el `ADR` del acto no existe en `main`.
2. `refusiones-por-pr.tsv` cuenta todo commit de dos padres; el informe ya no menciona el *rebase* como causa.
3. El conteo de fallos propios de T16 aparece con su comando, y T16 ya no figura en la lista de «señal real».
4. `barrido-check-tests.tsv` tiene cero filas con `nacimiento_citas` vacío.
5. La recomendación del salto de cascada dice «mismo árbol».
6. La adenda está archivada con su sello de cuerpo, y el verificador la da por buena; el encargo original y su sello, sin cambios de bytes.
7. Suite en LÍNEA BASE VERDE.

## 5 · LATITUD

El cómo es tuyo. Un obstáculo reversible y barato se resuelve y se declara (D-19). Si `main` vuelve a moverse, fusiona otra vez y re-deriva el `ADR`: eso es exactamente el ciclo que el acto midió, y la nota dice cuántas vueltas costó.

## 6 · PAROS — lista cerrada

Editar el cuerpo sellado del encargo original o su sello · reescribir la historia de la rama o forzar el empuje · perder una fila de cualquiera de los dos lados al resolver conflictos · tocar un test, un workflow, `check.py`, `acto.md` o `tools/` · usar la API de GitHub o abrir microdato · objetivo inalcanzable. **Fuera de esta lista no se para.**

## 7 · PERÍMETRO

Escribes en: `forense/analisis/ci-medicion-1/` · `forense/encargos/` (sólo la adenda y su sello, y la sección de cierre al final del encargo) · `forense/notas/2026-09-21-GEN2-TUBERIA-CI-MEDICION-1-cierre.md` · `forense/hallazgos.md` · `forense/no-corrido.tsv` · y los archivos que la fusión con `main` y la cascada de `cierre_acto.py --aplica` tocan. **Si te encuentras escribiendo fuera de esta lista, PARA.**

## 8 · LO QUE NO HACE

No elimina T16 ni abarata nada: sigue siendo medición y recomendación · no borra los JSON crudos · no re-mide el CI · no fusiona el PR.
