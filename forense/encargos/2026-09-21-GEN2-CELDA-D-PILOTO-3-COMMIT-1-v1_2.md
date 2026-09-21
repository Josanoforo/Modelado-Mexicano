# ENCARGO · ACTO `GEN2-CELDA-D-PILOTO-3-COMMIT-1-v1_2` · al cerrar, los dos CALC del piloto 3 pasan el preflight que sella, sin tocar una línea del código ni de la spec humana

> ENTORNO: **CAJA** — el hook de arranque imprime `ENTORNO-DERIVADO`. Si no dice `CAJA`, PARA en una línea. Tiene que ser la caja, aunque este acto no abre la ola: el preflight que prueba el arreglo tiene que ser el mismo que verá el COMMIT-2, con el payload montado.

**CABECERA** · SHA de redacción: `origin/main = 5a888bcb` + `PR #941` (cabeza `b1f1cb13`). Arranca de main **con `#941` fusionado**, que es donde vive la fila `FP-407`; si al abrir no está fusionado, arranca de `b1f1cb13` y lo declara. Si main se movió no es PARO · **una sola sesión, rama propia nueva.** La congela **la sesión que paró en `#941`** —su nota, línea 33, declara que no tiene los diseños A/B ni el careo, y que de ENCIG 2025 sólo vio el `sha256` del preflight— **u otra con esa misma exposición declarada**. F3 (`FP-400`): quien congela no ejecuta, así que **esta sesión no corre los COMMIT-2/3** · **MODELO: Opus** (congela un medidor; D-13 prohíbe bajar) · **MODO: RÍGIDO** — spec congelada y reserva de evaluación viva sobre ENCIG 2025: la latitud es sobre logística y nunca sobre el procedimiento · **CONTADOR:** `cuenta_gen2 = NO-APLICA` en este acto (no corre nada); la firma de contador del piloto se hereda para los COMMIT-2/3 (§2 (c)) · **CALC-id:** no se crean; se re-congelan `CALC-GOB-DIGITAL-EXE-EMISIONES-0002` y `CALC-GOB-DIGITAL-EXE-ADJUDICACION-0001` · **FP/ADR/NC:** deriva al cierre, no heredes.

---

## 1 · OBJETIVO

Que `corrida0 run` pueda correr el piloto 3. Hoy **no puede por construcción**: `run` llama a `preflight` primero (`tools/corrida0.py:2064-2069`) y el preflight sale `BLOQUEADO` en los dos CALC. **Tres actos seguidos del mismo piloto se han perdido por cableado invisible a la prueba del congelador** (`#903`, `#924`, `#926`). Éste lo arregla sin tocar lo que se congeló de verdad —el código y la spec humana— y deja escrita la secuencia que el COMMIT-2/3 necesita para no caer por quinta vez.

**«Hecho» significa**, con la salida cruda pegada en la nota:
- `corrida0 preflight CALC-GOB-DIGITAL-EXE-EMISIONES-0002` → **`VERDE`**, en la caja y con el payload montado.
- `corrida0 preflight CALC-GOB-DIGITAL-EXE-ADJUDICACION-0001` → `BLOQUEADO` **exactamente** por estas cuatro entradas y ninguna otra: `input_repo_ausente=emisiones_resultados…`, `input_repo_no_commiteado=emisiones_resultados`, `input_repo_ausente=emisiones_sello…`, `input_repo_no_commiteado=emisiones_sello`. La lista esperada se escribe en la nota **antes** de correr el preflight.
- `git diff --stat` contra `origin/main`, fuera de la cascada, sólo toca los dos `spec.yaml`, un archivo nuevo —el snapshot de §5 P1 (3)— y dos filas de `decisiones.tsv` (P5).
- `tests/test_piloto3_v11.py` → 7/7, incluida `test_b_oro_2023_reproduce_los_sellados`.
- `cuenta_gen2` resuelto a `SI` para los dos CALC-id desde `decisiones.tsv` (P5).

---

## 2 · FIRMAS DE MESA

Verbatim de lo ya firmado:

**Firma de contador del piloto** (lanzamiento de `ACTO GEN2-CELDA-D-PILOTO-3-COMMIT-2-3`) — «Cuentan (cuenta_gen2 = SI) CALC-GOB-DIGITAL-EXE-EMISIONES-0002 y CALC-GOB-DIGITAL-EXE-ADJUDICACION-0001, sea cual sea el veredicto: una prueba pre-registrada que sale "nadie vence" o "falsador débil" cuenta igual que una que sale "vence".»

**`FP-399`** — FIRMADA el 20/sep/2026 (lanzamiento de `ACTO GEN2-CELDA-D-PILOTO-3-COMMIT-1-v1_1`); texto íntegro en `forense/firmas-pendientes.tsv`.

**FIRMA `FP-407`** (mesa, 21/sep/2026):

> **(a)** «El COMMIT-1 v1.2 lo congela la sesión que paró en #941 u otra sin contexto de los diseños A/B ni exposición a ENCIG 2025. Quien congela no ejecuta: los COMMIT-2/3 los corre otra sesión, como en FP-400.»
>
> **(b)** «Cuentan como "hereda verbatim" cuatro llaves de cableado en cada `spec.yaml` —`spec_md` relativo al CALC, `sha256` de los tres inputs sellados, la guardia S2 apuntada a una copia inmutable de `firmas-pendientes.tsv` al commit que firmó FP-399, y `dependencias_materiales`— sin tocar `spec.md`, su sidecar ni ningún `.py`. Prueba obligatoria antes de congelar: EMISIONES en VERDE y ADJUDICACION bloqueada sólo por los dos inputs que crea el COMMIT-2. Las huellas de esos dos inputs se escriben en un COMMIT-3a, después de sellar las emisiones y antes de derivar R, como en el piloto 1.»
>
> **(c)** «La firma de contador del piloto se hereda al v1.2 y a sus COMMIT-2/3: los CALC-id no cambian. Este acto la asienta como fila de `decisiones.tsv` para que cuente.»

---

## 3 · LO QUE DIRECCIÓN SABE — cada línea con su rótulo

- `[EJECUTADO]` sobre `pr941`: preflight de los dos CALC → `BLOQUEADO`. Los tres defectos que reporta `#941` son reales, y hay **dos más** que el v1.2 heredaría si sólo arregla esos tres (los dos siguientes puntos).
- `[EJECUTADO]` **Cuarto defecto: la guardia S2 lee un libro vivo.** `firmas_pendientes_tsv` apunta a `forense/firmas-pendientes.tsv`, que casi todo acto edita. Su huella era `e0f1ec86…` en `04a2edeb` y `5df43a05…` dos commits después, en la cabeza de `#941` —el propio `#941` la cambió al añadir `FP-407`—. **Fijarle un `sha256` hoy haría caer el COMMIT-2 en cuanto cualquier otro PR se fusione antes.** Es la misma clase de defecto que rompió el sidecar de `#932`: sellar contra un archivo que se sigue escribiendo.
- `[LEÍDO]` `medidor.py:103-111`: la guardia S2 sólo exige que la fila `FP-399` tenga `estado = FIRMADA`, y lee el archivo por `ruta_absoluta`. `[EJECUTADO]` `git show 826bf3a1:forense/firmas-pendientes.tsv` —el commit que firmó `FP-399` y congeló el v1.1— trae `FP-399` con `estado = FIRMADA`. Una copia de ese blob es inmutable y cumple la guardia sin tocar el `.py`.
- `[EJECUTADO]` **Quinto defecto: ADJUDICACION no puede pasar el preflight antes del COMMIT-2, con ningún arreglo.** Tiene dos inputs —`emisiones_resultados`, `emisiones_sello`— que sólo existen después de que EMISIONES corra, y el preflight exige su `sha256` declarado. **Si nadie lo escribe ahora, el COMMIT-3 cae igual.**
- `[EJECUTADO]` **El precedente que lo resuelve es de la casa.** Piloto 1, commits del 16/sep: `c169edc9` 21:27 *COMMIT-2 · emisiones selladas · R NO EXISTE en el árbol*; `39bf1af3` 21:30 *COMMIT-3a · contrato y medidor del árbitro del cruce, antes de correr* —fija el `sha256` de las emisiones ya selladas—; `18b99142` 21:37 *COMMIT-3 · R del cruce, adjudicación*. El orden de E.6 se conserva: R se deriva después de fijar el árbitro.
- `[EJECUTADO]` **Los CALC-id no pueden cambiar sin tocar código:** `adjudicacion.py:48` fija `_MEDIDOR = …/CALC-GOB-DIGITAL-EXE-EMISIONES-0002/medidor.py`, y `tests/test_piloto3_v11.py:27-28` fija los dos directorios. Por eso el v1.2 re-congela los mismos ids, y por eso la firma de contador —que nombra esos ids— se hereda sin re-firma. **No hay ninguna corrida sellada bajo esos ids**, así que re-congelar su `spec.yaml` no reescribe evidencia (E.3 protege corridas selladas).
- `[EJECUTADO]` **Prueba en seco de las cuatro llaves** (worktree temporal descartado; no toca el clon): EMISIONES → `PRE-FLIGHT: VERDE`; ADJUDICACION → `BLOQUEADO` sólo por las cuatro entradas de `emisiones_*`. **Límite de esa prueba:** corrió en un contenedor sin `data/raw`, así que el input de manifiesto quedó sin verificar. Por eso este acto repite la prueba en la caja.
- `[EJECUTADO]` en esa prueba reserialicé cada `spec.yaml` con `yaml.safe_dump` y **el diff salió de 59 y 68 líneas** por puro reformateo. Que parezca una reescritura es justo lo que D-18 no admite: por eso §5 P1 pide edición quirúrgica.
- `[EJECUTADO]` **La firma de contador del piloto no contaría hoy.** `cuenta_gen2` se resuelve con una fila de `data/corrida0/decisiones.tsv` (`objeto · decision · fuente · fecha`; `tools/corrida0.py:3233`, `_cuenta_gen2_resuelto`), no editando la spec. `grep` en `decisiones.tsv`: 63 filas `cuenta_gen2=SI` en main, **ninguna** para `CALC-GOB-DIGITAL-EXE-*`; tampoco en la rama de `#940`, que propaga las firmas del 21/sep. La firma vive sólo en el texto del encargo `2026-09-20-GEN2-CELDA-D-PILOTO-3-COMMIT-2-3.md:25`. **Si nadie escribe la fila, el COMMIT-2 sella y el contador no se mueve.**
- `[LEÍDO]` nota de `#941`, línea 91: `python3 tools/asienta_replay_aislado.py --help` **re-asentó una fila ajena** en `forense/replay-evidencia.tsv` —el script no tiene `argparse`— y hubo que revertirla. En `tools/` hay herramientas que escriben aunque se les pida ayuda.
- `[LEÍDO]` `tests/test_piloto3_v11.py` construye sus inputs sintéticamente y no lee las llaves que cambian, así que el 7/7 del P0 de `#941` debería sostenerse. `[SUPUESTO]` hasta que corra: aquí no pude correrlo porque el contenedor no tiene `pytest`.

---

## 4 · YA HECHO / YA DECIDIDO — búsqueda por OBJETO

Objeto: **«`spec.yaml` del piloto 3 que pasa preflight»**.

| dónde | universo | resultado |
|---|---|---|
| ramas remotas | todas | `acto/gen2-celda-d-piloto-3-commit-1-v1_1` sigue viva; `#941` abierto. Ninguna rama arregla el preflight |
| `forense/encargos/` | los encargos del piloto 3 (P0, v1.1, EJECUCIÓN, COMMIT-2-3) | ninguno pide preflight VERDE como prueba de congelado |
| `data/corrida0/*/spec.yaml` | 166 | 29 consumen `resultados.json` o `sello.json` de otro CALC; los que miré fijan el `sha256` porque se escribieron **después** del sello del CALC anterior. Ninguno se congeló antes de que existiera su input |

**Al ejecutor: repítela con tu acceso.**

---

## 5 · PIEZAS — resultado esperado, no receta

**P1 · Las cuatro llaves, en cada `spec.yaml`, con edición quirúrgica.** Se cambian líneas; **no se reserializa el archivo**. El diff debe mostrar sólo esas líneas.
1. `spec_md` → `../../../forense/prereg-caja/GOB-gobierno-digital-exe15-spec-v1_1.md` (la forma que ya usan 7 CALC de la casa). `spec_md_sha256` **no cambia**: el archivo es el mismo.
2. `sha256` en `encig2021_cruces_resultados`, `encig2023_cruces_resultados` y `c2_compuesto_resultados`: **derivados en la sesión**, no copiados de este encargo. Son `resultados.json` de CALC sellados, así que sus huellas no se mueven.
3. `firmas_pendientes_tsv` → `ruta` a **un solo** archivo nuevo, `data/corrida0/CALC-GOB-DIGITAL-EXE-EMISIONES-0002/fp399-firmada-826bf3a1.tsv` = `git show 826bf3a1:forense/firmas-pendientes.tsv`, con su `sha256`. Los dos CALC apuntan a ese mismo archivo, y su nota dice de qué commit sale y por qué. El `id` del input no cambia, así que el `.py` lo encuentra igual.
4. `dependencias_materiales`, **derivadas de los `import` de cada `.py`**, no tecleadas.

**P2 · La prueba, en la caja.** Primero se escribe en la nota la lista de bloqueos esperada de §1; luego se corren los dos preflight; se pega la salida cruda. *Rama prevista*: si EMISIONES no sale `VERDE` con las cuatro llaves, **PARO (g)** — no se añade una quinta llave para que pase. Es cableado que nadie ha visto, y verlo es el entregable.

**P3 · La secuencia del COMMIT-2/3, escrita ahora.** Una sección en la spec ejecutable —y sólo ahí; la consecuencia vive en un sitio— que diga: COMMIT-2 corre y sella EMISIONES; **COMMIT-3a** escribe en el `spec.yaml` de ADJUDICACION el `sha256` de `emisiones_resultados` y `emisiones_sello` recién sellados, y verifica ADJUDICACION en `VERDE` antes de correr; **COMMIT-3** deriva R y adjudica. Se cita el precedente del piloto 1 (`c169edc9` → `39bf1af3` → `18b99142`). **Esto no cambia el procedimiento**: sólo escribe el orden que el procedimiento ya necesitaba.

**P4 · Lo que no se tocó, probado.** `git diff --stat` contra `origin/main`: sólo los dos `spec.yaml`, el snapshot y la fila de P5, fuera de la cascada. `sha256sum` de los dos `.py`, de `spec.md` y de su sidecar, **idénticos** a `826bf3a1`. Test 7/7.

**P5 · La firma de contador, asentada donde cuenta.** Dos filas en `data/corrida0/decisiones.tsv`, una por CALC, con la forma de las 63 que ya existen: `objeto` = el CALC-id · `decision` = `cuenta_gen2=SI` · `fuente` = la firma verbatim, más `FP-407 (c)` y la ruta del encargo `2026-09-20-GEN2-CELDA-D-PILOTO-3-COMMIT-2-3.md` · `fecha`. *Queda bien si*: `corrida0.py` resuelve `cuenta_gen2 = SI` para los dos ids —se prueba con la función que lo resuelve (`_cuenta_gen2_resuelto`), sin correr nada—. **No se mueve ningún contador**: la fila decide cómo contará una corrida que todavía no existe.

---

## 6 · LATITUD

**Decides tú, y lo dices en la nota:** el orden de P1–P5 · cómo editas las líneas · enlazar o crear `data/raw` · instalar `pytest` · arreglar un defecto adyacente de ≤ 10 líneas **fuera** de los dos CALC que te impida terminar, declarándolo.

**No decides:** nada de §7. En particular, **ninguna quinta llave**.

---

## 7 · PAROS — lista cerrada

- **(a)** Abrir, leer o derivar cualquier miembro de ENCIG 2025 más allá del `sha256` que calcula el preflight. **Hashear no es leer; `unzip`, `head` o `pandas.read_csv` sí.**
- **(b)** Tocar un `.py` de los dos CALC, `GOB-gobierno-digital-exe15-spec-v1_1.md`, su sidecar, o cualquier `resultados.json` sellado. Borrar, forzar o reescribir algo sellado.
  **Cuidado que no es PARO, pero cuesta:** no invoques ningún `tools/*` que no sea `corrida0.py preflight` y el propio de la cascada, **ni con `--help`** —`asienta_replay_aislado.py` escribe aunque se le pida ayuda (`#941`, nota l. 91)—. Antes de cada commit, `git status` debe mostrar sólo tu perímetro; si aparece algo ajeno, se revierte y se declara.
- **(c)** Correr `corrida0 run` en cualquiera de los dos CALC, o mover un contador.
- **(d)** Cambiar en un `spec.yaml` cualquier cosa fuera de las cuatro llaves de P1 y la sección de secuencia de P3: parámetros, semilla, tolerancia, rejilla, resultados, guardias.
- **(e)** `ENTORNO-DERIVADO ≠ CAJA`.
- **(f)** El objetivo dejó de ser alcanzable, y eso es el entregable.
- **(g)** Con las cuatro llaves puestas, EMISIONES no sale `VERDE`, o ADJUDICACION sale bloqueada por algo que no está en la lista esperada.

---

## 8 · COMPUERTAS

**«Salida cruda de los dos preflight pegada, coincidiendo con la lista esperada escrita antes de correrlos» protege: congelar spec.** Sin eso el v1.2 no se declara congelado y el COMMIT-2 no se lanza.

Lo demás en este encargo es orden sugerido, no compuerta.

---

## 9 · PERÍMETRO

**Propio:** los dos `spec.yaml` · `data/corrida0/CALC-GOB-DIGITAL-EXE-EMISIONES-0002/fp399-firmada-826bf3a1.tsv` · las dos filas de `data/corrida0/decisiones.tsv` de P5 · la fila de `FP-407` en `forense/firmas-pendientes.tsv`, que pasa a `FIRMADA` con el PR de este acto (A.12) · la línea de la celda-D del piloto 3 que cita la spec congelada, **si existe**, y sólo para citar el v1.2 · nota de cierre · NC y FP propias · `forense/hallazgos.md` · el archivo verbatim de este encargo con su `sha256` (0-bis, A.3) · la cascada de `/acto`.

**Ajeno, no se toca y por qué:** los dos `.py`, `spec.md` y su sidecar — son lo congelado de verdad · `tools/corrida0.py` — el preflight hace bien su trabajo; el defecto es del contrato · `tests/test_piloto3_v11.py` — se corre, no se edita · `.claude/commands/acto.md` y D-22 — el cambio de regla es de DIRECCIÓN (§10) · ENCIG 2025.

**Perímetro de cierre, permanente (D-21):** `## NO-CORRIDO / RESERVAS` con «Ninguno.» obligatorio si no hay, antes de `## CONSUMIDO`.

**«Si te encuentras escribiendo fuera de esta lista, PARA.»**

---

## 10 · LO QUE NO HACE · SUCESORES · PARA MESA · CIERRE

**No hace:** no corre el piloto · no abre ENCIG 2025 · no escribe la regla de elección de ningún cruce · no cambia D-22.

**Sucesores:**
1. **COMMIT-2 / 3a / 3 del piloto 3**, en **otra** sesión (F3), con la secuencia de P3 y la firma de contador ya asentada en `decisiones.tsv`.
2. **El piloto de ahorro de PRODUCTO-DINERO**, que espera este patrón para reutilizarlo en vez de reinventarlo.

**Para mesa, dos cosas que este acto no resuelve y deberían resolverse:**
- **D-22 debería exigir el preflight.** Hoy «congelado» exige que el punto de entrada haya corrido sobre sintético, y el v1.1 lo cumplió: 7/7 con oro 2023. Aun así no corría por el único conducto que sella. **Tres actos perdidos por esto** (`#903`, `#924`, `#926`) pasan el gate D-14 para instrumentar. La propuesta: «congelado» exige también `corrida0 preflight` en `VERDE`, o bloqueado sólo por una lista declarada antes de correr. Es regla de gobierno: va a DIRECCIÓN.
- **Nada se sella contra un libro vivo.** El sidecar de `#932` y la guardia S2 de este piloto son el mismo defecto: un `sha256` fijado sobre un archivo que la casa sigue escribiendo. Vale una línea para TUBERÍA junto con la pieza del sidecar que ya tiene.

**Cierre:** cascada de `/acto` · primera línea de la nota: qué preflight pasó, dónde y con qué payload montado.

---

**Falsador de este encargo, a tres meses:** si el COMMIT-2/3 del piloto 3 para en el preflight por una causa que este encargo no nombró, la prueba en seco no bastaba y la exigencia de D-22 tiene que ir más lejos.


---

## NO-CORRIDO / RESERVAS

| qué | por qué | impacto | sucesor |
|---|---|---|---|
| Ninguno. | — | — | — |

Todas las piezas P1–P5 se ejecutaron en la caja; la compuerta de §8 se cumplió (nota §2 y §3). Los dos puntos «para mesa» de §10 (D-22 y el libro vivo) no son piezas de este acto: van a DIRECCIÓN, como el propio encargo lo asigna.
