ENCARGO · ACTO GEN2-RECIBO-CODEX-5 · RECIBO DE SEIS PR CODEX (#876, #877, #879, #881, #882, #887): DOCE CORRIDAS NUEVAS, OCHO ESPERAN CONTADOR, DOS ENCARGOS SIN ARCHIVO

CABECERA (D-12) · SHA de redacción `6f365928`; re-deriva al abrir · ENTORNO: NUBE; NO caja · una sola sesión, rama propia; carril Claude — si existe `codex/*recibo-codex-5*`, PARA y reporta · COMPUERTA: los seis PR en main (cumplida) · MODELO: Sonnet · FP/ADR/NC: deriva al cierre; renumera quien fusione segundo (corren `C2-COMPUESTO-RESERVADAS-1` y `PILOTO-3 COMMIT-1`) · CONTADOR: `cuenta_gen2 = NO`; mueve `N_corridas_selladas` solo por las firmas de abajo.

FIRMAS DE MESA (propuestas; tu lanzamiento es el sello; sin texto, PARA esa pieza y sigue)

Contador: "Cuentan (`cuenta_gen2 = SI`): `CALC-PISO-PERSISTENCIA-ERROR-0001`, `CALC-ENCIG2023-CRUCES-HISTORICOS-0002`, `CALC-ENCIG2021-CRUCES-HISTORICOS-0003`, `CALC-ENFIH2019-SALDOS-AFORE-0001`, `CALC-ENFIH2019-SALDOS-AFORE-CONCENTRACION-0001`, `CALC-ENIGH2022-PERFIL-ESTRUCTURAL-0003`, `CALC-ENIGH2022-INTENSIDAD-REMESAS-0001`, `CALC-ENUT2024-PARTICIPACION-INTENSIDAD-0001` — cada una condicionada a que P2 no encuentre ejecución previa a su spec congelada."

VERIFICACIÓN DE EXISTENCIA (contra `6f365928`)

`status`: `selladas = 92`, `adoptados_activos = 46`, `no_corrido_abiertas = 101`. En `corridas.tsv`: las ocho de arriba `SELLADA · PENDIENTE-DE-MESA` (remesas: `PENDIENTE-DE-CASCADA-DIFERIDA`); `CALC-ENCUCI2020-EXPOSICION-RESPUESTA-0001` ya figura `cuenta = SI` — dirección no encontró esa firma. `CALC-PISO-PERSISTENCIA-ERROR-0001`: replay = NO-VERIFICADO. `git ls-files forense/encargos | grep -i` → ISSP2017-REDES: NO-ENCONTRADO; ENCUCI2020: NO-ENCONTRADO (universo: `forense/encargos/`, declara el conteo). Sin recibo previo de estos seis PR.

PIEZAS

P1 · ADR de recibo, una línea por producto; qué tocó cada PR fuera de su carril (compara contra `BRIEF-ASTRA-CARRILES`, hoy en `forense/encargos/fuentes/` si fue archivado; si no, NO-ENCONTRADO y sigue).
P2 · Orden spec → resultado, por `git log --reverse`, en las ocho + ENCUCI. Patrón a documentar, no a castigar: ENCIG 2021 tiene `-0001` y `-0002` con solo `spec.yaml`, ENCIG 2023 un `-0001`, ENIGH dos `SUPERADO→` con `n_res = 0`. ¿Alguna tuvo ejecución (`ejecucion.json`, sello, salida en nota) antes de ser sucedida? Si ninguna, una línea de hallazgo: "specs sucedidas sin correr: limpio". Si alguna sí: NC y la firma de contador de esa corrida no se aplica.
P3 · Firmas de contador por el mecanismo de la casa, tras P2. `status` antes/después con worktree. ENCUCI `cuenta = SI`: localiza la decisión que la ampara (`decisiones.tsv`, `firmas-pendientes.tsv`); si no existe, fila en `firmas-pendientes.tsv` y una línea — no la reviertas.
P4 · A.3, dos encargos sin archivo. ISSP-REDES y ENCUCI: busca por contenido en `forense/encargos/**` y en la nota de cierre de cada PR. Si están, corrige la cita; si no, NC `NO-VERIFICABLE-AQUÍ` pidiendo a Astra el texto con sha256. No los reconstruyas.
P5 · La regla de elección del cruce y su enmienda. Asienta en hallazgos, con los RESULT por id: Codex paró en `SELECCION-PENDIENTE-DE-DEFINICION` porque la regla de dirección (brief 03) no definía la coherencia con categoría residual (107 trámites con edad fuera de bandas) — paro correcto del ejecutor, hueco de dirección. Dirección fijó la definición antes de leer puntajes (consta en la conversación del 19/sep) y después propuso a mesa enmendar la elegibilidad; la firma F1 vive en el encargo PILOTO-3. Semilla PARA-v2.15: una regla de selección se prueba contra un caso sintético antes de congelarla (§2: la receta también se verifica).
P6 · ISSP-REDES, rótulo de contenido, igual que en RECIBO-4: si no hay diseño muestral acreditado, evidencia (a) sin incertidumbre; descriptivo, no adjudica.
P7 · Replay pendiente: `CALC-PISO-PERSISTENCIA-ERROR-0001` sin asiento → NC (E.7(2)); no lo corras aquí.

PERÍMETRO

TSV y ADR de gobierno · `registro-rotulos` · tablero · derivados por comando · specs solo en `cuenta_gen2` si ése es el mecanismo · nota. No toca `tools/`, `tests/`, `milpa/`, marcador, resultados de ningún CALC. «Si te encuentras escribiendo fuera de esta lista, PARA.»

LO QUE NO HACE

No mide · no decide el cruce · no re-ejecuta · no interpreta los resultados de ENIGH/ENFIH/ENUT (eso es de quien los consuma).
SUCESOR: informe v1.2 (el v1.1 del 17/sep quedó viejo: no conoce pisos, marcador, error de persistencia ni la corrección de unión libre).

CIERRE

Cascada D-10 · `## NO-CORRIDO / RESERVAS` · `## CONSUMIDO` · cero ramas.

## NO-CORRIDO / RESERVAS

| qué | por qué | impacto | sucesor |
|---|---|---|---|
| P3 — firma de contador para `CALC-ENCUCI2020-EXPOSICION-RESPUESTA-0001` | `DECISIÓN-DE-MESA-PENDIENTE`: la corrida ya trae `cuenta_gen2=SI` en `corridas.tsv` pero ninguna fila de `decisiones.tsv`/`firmas-pendientes.tsv` la respalda por su id exacto; el ejecutor no revierte una cifra que mesa no le pidió tocar (D-1) | `N_corridas_selladas` incluye esa corrida sin respaldo verificable hasta que mesa conteste | `FP-388` (ABIERTA) |
| P4 — dos encargos sin archivo, `CALC-ISSP2017-REDES-APOYO-COTIDIANO-0001` y `CALC-ENCUCI2020-EXPOSICION-RESPUESTA-0001` | `NO-VERIFICABLE-AQUÍ`: ningún archivo de `forense/encargos/` ni cita en el cuerpo de `#881`/`#882` gobierna estos dos CALC por su id exacto; no se reconstruye el texto | trazabilidad A.3 incompleta para dos corridas ya selladas; no bloquea la corrida | `NC-0349`/`NC-0350` (ABIERTAS) — a Astra, el texto verbatim con sha256 |
| P7 — replay de `CALC-PISO-PERSISTENCIA-ERROR-0001` | `SUSTITUIDO-POR`: el encargo pedía abrir una NC por E.7(2) sin correr el replay; la verificación mecánica encontró que el asiento **ya existe** en `forense/replay-evidencia.tsv` (`VERIFY-DIRIGIDO · GEN2-MARCADOR-PISOS-ENLACE-1`) — la premisa del encargo no se sostenía, así que no hay nada que sustituir ni que dejar huérfano: se documenta la corrección en `hallazgos.md` y en el `ADR-549` en su lugar | ninguno — E.7(2) ya estaba satisfecho | ninguno |
| CIERRE — `python3 tests/check.py --baseline` en VERDE | `FUERA-DE-PERÍMETRO`: LÍNEA BASE ROJO, 2 FAIL nuevos (`T16`×2) frente a `tests/baseline.json`; drift preexistente de ocho citas históricas "`N FAIL vigente`" en `canon/gobernanza-v1_15.md`/`canon/estado-programa-v1_14.md`, quedadas atrás por los tests propios que los seis PR de este recibo trajeron — reescribir esas ocho anotaciones no es una de las piezas P1-P7 de este acto y no tiene instrucción explícita de mesa que amplíe el perímetro a `tests/`/narrativa histórica (a diferencia de `GEN2-RECIBO-CODEX-4`, donde mesa dijo "solve ci") | la línea base cierra ROJO en vez de VERDE; ningún consumidor de las firmas de este acto se ve afectado | `NC-0351` (ABIERTA) — DEMANDA-A-MESA |

## CONSUMIDO

PR #895.
