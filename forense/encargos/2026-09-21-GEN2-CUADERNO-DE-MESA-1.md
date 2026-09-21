# ENCARGO · ACTO GEN2-CUADERNO-DE-MESA-1 · TODO LO QUE ESPERA UNA DECISIÓN DE MESA, VERIFICADO UNO POR UNO, AGRUPADO Y CON RECOMENDACIÓN, PARA QUE MESA LO RESUELVA EN UNA SENTADA

> ENTORNO: **NUBE** (cualquiera): todo lo que lee está en el repo. NO es CAJA.

CABECERA · SHA de redacción `55c8d57c`; re-deriva al abrir · una sola sesión, rama `claude/cuaderno-de-mesa-1` · MODELO: Opus (juicio) · MODO: **ABIERTO** · CONTADOR: ninguno; **este acto no firma, no cierra y no adopta nada**: prepara · FP/ADR/NC: raíz de acto.
**Si al fusionar `main` choca la línea L0 de `canon/estado-programa-v1_14.md`: NO conserves los dos lados; toma la de `main` y re-inserta solo tu anotación** (27 MB por duplicaciones; TUBERÍA la repara). Si `canon/L0/` ya existe al cerrar, tu anotación va ahí.

## 1 · OBJETIVO
El tablero derivado trae decenas de firmas sin cerrar y más de cien NC abiertas; una parte espera a mesa. El 21/sep mesa resolvió veinte en una sola pasada porque alguien se las llevó verificadas, agrupadas y con recomendación (`GEN2-TRAMITE-FIRMAS-3`). Desde entonces mesa cerró las conversaciones MOTOR y PRODUCTO-DINERO y pidió que dirección le lleve las cosas **resueltas**. Este acto produce el cuaderno: mesa lo lee, tacha lo que no comparte, y su envío a un trámite es la firma.
«Hecho» significa: un documento, `forense/cuadernos/CUADERNO-DE-MESA-<fecha>.md`, donde **cada** renglón pendiente de mesa aparece una vez, con su estado re-verificado hoy, en lenguaje de Recursos Humanos, con una recomendación y su razón en dos líneas, y con el texto de firma listo para copiar; más una lista aparte de lo que **ya no necesita a mesa** (caducó, lo resolvió otro acto, o nunca fue de mesa).

## 2 · FIRMAS DE MESA — verbatim
Mandato (21/sep): «No me des hojas de respuestas para esto, ya damelas resueltas […] hagamos trabajo más estratégico y menos operativo.» Instrucciones §0: «Antes de declarar cualquier decisión pendiente, revisa el repo: contexto, decisiones anteriores relacionadas, dependencias, qué desbloquea. Preséntala en lenguaje de Recursos Humanos para que mesa decida fácil.»

## 3 · LO QUE DIRECCIÓN SABE (contra `55c8d57c`)
- `[EXISTE]` el precedente de forma: `forense/encargos/CUADERNO-DE-FIRMAS-2026-09-21.md` (con su `.sha256`), el cuaderno que mesa resolvió el 21/sep. **Misma forma y mismo lugar**; lo que cambia es que ahora cada renglón llega con recomendación. Si el precedente vive en `forense/encargos/`, el tuyo también: ignora la ruta `forense/cuadernos/` de §1.
- `[EXISTE]` `tools/digesto_tramite.py` y los comandos `/tramite` y `/revisa`; `forense/firmas-pendientes.tsv`; `forense/no-corrido.tsv` con la razón `DECISIÓN-DE-MESA-PENDIENTE` (hay filas con y sin acento: cuenta las dos). **Parte de lo que pide este acto puede estar ya hecho por el digesto: córrelo primero y di qué cubre.**
- `[EJECUTADO]` firmas abiertas que piden dictamen y no tienen quién lo prepare: `FP-408` (¿la corrección de `CALC-ENSAFI2023-ESTRATEGIAS-CONJUNTAS-0001-v1_1` pudo depender de haber visto el resultado?), `FP-409` (lo mismo para `CALC-ENUT2024-DISTRIBUCION-HORAS-0002`), `FP-405` (acota FP-67 a `cloud_default`; el piloto de nube ya midió: `milpa-inegi` tiene egreso a INEGI). Conteo crudo de dirección, con un `awk` sin validar: ~50 FP sin cerrar. **No heredes el número: deriva el tuyo y di cómo.**
- `[LEÍDO]` pendientes que dirección ya conoce y que deben aparecer: el redondeo de `share_horas_mujeres_40mas` (F8: va por canal de relevo; falta dueño) · `motor.py:20` y `:129` citan BARRIDO-2 (tocarlas mueve el replay de dos sellos) · «una corrida puede contar solo por la etiqueta de su propia spec» (pregunta de regla) · respaldo del corpus: 18.4 GB en una sola máquina · toda ola nueva que entra al corpus, ¿nace reservada?

## 4 · YA HECHO
Por objeto («cuaderno», «digesto», «pendientes de mesa») en encargos y notas: existe el digesto y existieron tres trámites de firmas; no hay un cuaderno con recomendaciones posterior al 21/sep. **Repítela tú.**

## 5 · PIEZAS
**P1 · Universo.** Todo lo que espera a mesa: FP no cerradas · NC abiertas cuya razón o sucesor nombre a mesa · preguntas a mesa en notas de cierre desde el 18/sep. Con comando y conteo (A.4, A.13).
**P2 · Re-verificación de estado, una por una (A.17).** ¿Sigue abierta? ¿Lo resolvió otro acto sin marcarlo? ¿Su universo creció y quedó vencida en alcance? ¿Depende de otra que ya se firmó? Lo resuelto-sin-marcar va a la lista aparte **con la evidencia**, no se cierra aquí.
**P3 · Dictámenes de FP-408 y FP-409.** Para cada una: qué cambió entre la versión que corrió y la sucesora (diff de spec y de código), cuándo (orden de commits contra el primer resultado), y si el cambio pudo elegirse mirando el resultado. Rótulo de §5 de las instrucciones: DECLARADO / INFERIDO / RETROSPECTIVO. Se pide la **categoría** del defecto y su razón; no se re-corre nada.
**P4 · El cuaderno.** Por renglón: qué se decide (una frase, sin jerga) · por qué está detenido · qué desbloquea · opciones · **recomendación y su razón** · texto de firma listo · a quién va después. Agrupado por lo que desbloquea, no por id. Primero lo que destraba trabajo en curso; al final lo que puede esperar, dicho así.

## 6 · LATITUD
Decides tú: forma del documento, agrupación, herramientas. Si un renglón no se puede recomendar sin un dato que no está en el repo, dilo y di cuál dato.

## 7 · PAROS — lista cerrada
a) marcar FIRMADA, cerrar una NC o editar una fila ajena · b) recomendar sobre un renglón cuyo estado no re-verificaste · c) re-correr un CALC.

## 8 · COMPUERTAS
Ninguna.

## 9 · PERÍMETRO
Propio: el cuaderno · nota · filas propias · cascada. Ajeno: todo lo demás. Si te encuentras escribiendo fuera de esta lista, PARA.

## 10 · NO HACE · SUCESORES · CIERRE
No firma · no tramita. Sucesor: mesa lee; lo que apruebe va a un trámite de firmas. Auditoría §5: no aplica, no afirma nada sobre México. Falsador a tres meses: si mesa no resuelve al menos la mitad de los renglones con el cuaderno en la mano, el formato no sirve y se anota. `## NO-CORRIDO / RESERVAS` · `## CONSUMIDO`.

## NO-CORRIDO / RESERVAS

| qué | por qué | impacto | sucesor |
|---|---|---|---|
| **P2 · Cerrar las nueve filas que este acto acredita como ya resueltas** (NC-0185, NC-0237, NC-0344, NC-0363, NC-0366, NC-0372, NC-0434, NC-0435, NC-…-5870-01) | `DIFERIDO-A:` trámite de firmas posterior al cuaderno — el **PARO (a)** de §7 veda expresamente marcar `FIRMADA`, cerrar una NC o editar una fila ajena, y §10 declara que este acto no firma ni tramita | `no_corrido_abiertas` no baja hoy por estas nueve (176 sigue 176); la cola de mesa se ve **32 % más larga** de lo que realmente es. Ningún contador de medición se mueve | trámite de firmas, con §1 del cuaderno como evidencia por fila (`NC-…-b6dc-01`) |
| **P1 · Abrir fila FP a las tres preguntas de regla sin asiento** — la etiqueta de la propia spec · el respaldo de 18.4 GB · si toda ola nueva nace reservada | `DECISIÓN-DE-MESA-PENDIENTE` — son preguntas de regla que gobernarían actos futuros, no casos; §10 declara que este acto no tramita. Negativo con universo declarado (A.4/A.13): **2 779** archivos `*.md`/`*.tsv`/`*.yaml` fuera de `.git`, 0 aciertos para dos de ellas | Que tres reglas vivan sólo en la memoria de dirección es el defecto que **A.12** existe para atrapar. Ningún contador se mueve; el costo es que cada acto futuro vuelve a tropezar con las tres | trámite de firmas: una fila FP por pregunta, con el texto de §7 del cuaderno (`NC-…-b6dc-02`) |
| **P4 · Recomendación fundada para dos renglones** — (a) la sonda de `gh` sobre la protección de `main`; (b) el apoyo empírico de la recomendación sobre NC-0369 | `NO-VERIFICABLE-AQUÍ` — (a) esta sesión NUBE no tiene `gh` con credenciales (`tools/limpia_arbol.py --reporta` sale `NO-VERIFICABLE-SIN-GH` en su punto D); (b) la recomendación se apoya en **coherencia con FP-394**, no en una auditoría de los 16 commits de `codex/gen2-enadid2023-union-sexo-edad-cli-2` | Dos de los diecisiete grupos llegan sin recomendación completa. §6 manda decirlo y decir cuál dato falta: está dicho, con el dato nombrado en los dos casos (§8 del cuaderno) | (a) mesa responde, o una sesión con `gh` corre la sonda; (b) acto de auditoría, sólo si mesa quiere la firma apoyada en ella (`NC-…-b6dc-03`) |

**Lo que sí se corrió y conviene dejar asentado, porque el encargo lo suponía de otra manera:** la premisa «~50 FP sin cerrar» de §3 **no se sostiene** y no era una premisa de medición sino de logística, así que —por §2 de las instrucciones (v2.15)— se replanteó, se siguió y se declara: el universo real es **6** FP no cerradas y **28** NC con token de mesa. La ruta `forense/cuadernos/` de §1 se ignoró, como el propio §3 instruye, en favor de `forense/encargos/`. La base `55c8d57c` que el encargo declaraba se re-derivó a `fc13cdc` porque `main` se movió.

**Ninguna otra pieza quedó sin correr.** P1, P2, P3 y P4 se ejecutaron completas; los tres renglones de arriba son reservas dentro de piezas ejecutadas, no piezas omitidas.

## CONSUMIDO

Ejecutado por [PR #963](https://github.com/Josanoforo/Modelado-Mexicano/pull/963) (`ACTO GEN2-CUADERNO-DE-MESA-1`, rama `claude/sleepy-ritchie-nak8pa`, 21/sep/2026).

Commits: `b6dca71` (0-bis A.3 — este encargo verbatim + sello de cuerpo `654fc38c…`) · `929ee13` (cuaderno, dictámenes y cascada) · este commit (`## CONSUMIDO`).

Entregable: `forense/encargos/CUADERNO-DE-MESA-2026-09-21.md` (+ `.sha256` `62a5f415…`). `ADR-260921-GEN2-CUADERNO-DE-MESA-1-b6dc-01` en `canon/gobernanza-v1_15.md`, con fragmento propio en `canon/L0/`. **CONTADOR: ninguno** — el acto no firma, no cierra, no adopta y no re-corre nada.

**Nota de logística, declarada por §2 de las instrucciones (v2.15).** El encargo nombra la rama `claude/cuaderno-de-mesa-1`; la sesión que lo ejecutó tenía asignada `claude/sleepy-ritchie-nak8pa` y se trabajó en ella. Premisa de logística, no de medición: el objetivo seguía alcanzable y D-17 se cumple —un solo escritor, un solo rótulo, sin duplicado (verificado en los tres sitios del guard 0.c: `ls-remote` sin coincidencia, un worktree, cero PR abiertos al arrancar)—. Se declara aquí y no se corrige hacia atrás.
