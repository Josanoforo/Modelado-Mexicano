# ENCARGO · ACTO GEN2-TUBERIA-RESUMEN-SUITE-1 · Tres cosas que el tablero no puede leer hoy y que el repo sí sabe: el resultado de la suite completa (que su puesto no puede correr) publicado por el nocturno en un archivo derivado; T03 sin falsos positivos por directorios ocultos; y `status` diciendo desde qué commit cuenta el contador de legacy, como ya dice para `celdas_validadas`

> ENTORNO: **NUBE** — CI, `tests/check.py`, `tools/corrida0.py`, `tools/tablero_programa.py`. Cero microdato. Hook imprime ENTORNO-DERIVADO; si dice CAJA, PARA.

CABECERA · SHA de redacción `5f708a47` (re-deriva al abrir) · una sesión, rama propia · MODELO: **Opus** (P1 toca el job que publica; no es receta sin juicio); P2 y P3 podrían ir a Sonnet si se separan · MODO: **ABIERTO**, cláusula v1.0 (`3fbc487684b77b7f`) · ids con raíz de acto (D-24) · D-21 aplica.
CONTADOR: cero mediciones; no adopta; no cambia ningún valor de `status` — **añade una clave** (`dependencias_numericas_legacy_definicion_desde`, o el nombre que siga la convención de `celdas_validadas_definicion_desde`).

## 1 · OBJETIVO
(P1) **Resumen de la suite, derivado y publicado.** El run nocturno (`schedule` de `verify.yml`, 09:00 UTC) deja en el repo, por el canal `[deriva]` que CI-TIEMPO-2 acaba de dejar funcionando, un archivo pequeño y derivado (p. ej. `data/derivados/suite-resumen.tsv` o donde el canal ya publique vistas) con: commit evaluado · fecha · VERDE/ROJO por FAIL · lista de FAIL · conteo de WARN y la lista de firmas `WARN NUEVOS` contra la línea base · duración. `tools/tablero_programa.py` lo lee y lo muestra en el bloque derivado con su commit y su fecha; si el archivo es más viejo que N días, lo dice («suite: sin corrida nocturna desde …»). D-14: defecto real → el tablero lleva siete cortes diciendo «suite no derivada» y esta semana reportó 3 FAIL (T06 ×2, T08) que en CI no existen: sin este archivo, nadie puede distinguir «la suite falla en main» de «mi puesto no puede correrla». Qué le costó a un lector: leer «peor que en v2.20» como estado del repo.
(P2) **T03 ve los directorios ocultos.** El glob de `tests/check.py` T03 no desciende a `.claude/` (`check.py:334-362` lo declara y lo parcha con `HISTORICOS`): las referencias a `.claude/commands/*.md` se reportan como colgantes. Que el índice de existentes incluya ocultos (o que `.claude/` entre explícitamente), y que las entradas de `HISTORICOS` que solo existían por esa limitación salgan, con el comando que demuestra que ya resuelven. D-14: defecto real → el tablero contó 19 de 117 firmas `WARN NUEVOS` como falsos positivos de T03 en v2.18.
(P3) **Marca de definición del legacy en `status`.** `dependencias_numericas_legacy_activas` cambió de definición el 25–26/sep (FIRMAS-16 B3, FIRMAS-18 H1–H3: 60 lecturas «fuera del contador por firma»); `status` ya publica `legacy_fuera_del_contador_por_firma__*` pero no desde qué commit cuenta así. Añadir la clave con el commit donde entró la definición (derivado del historial de `corrida0.py`/`decisiones.tsv`, no tecleado), igual que `celdas_validadas_definicion_desde=38dd709`. D-14: el tablero (§9.17, T10) y el inventario tuvieron que anotar a mano que 137 → 67 no es relevo.

«Hecho», por comando sobre el commit final con `origin/main` fusionado: tras un run nocturno (o un `workflow_dispatch` que lo simule, citado por run_id) existe el archivo de resumen con el commit evaluado y `tablero_programa.py --actualiza` lo muestra · `python3 tests/check.py --baseline` no reporta como colgante ninguna referencia a un archivo que exista bajo un directorio oculto (caso de prueba: `tramite.md`) y la suite sigue VERDE · `python3 tools/corrida0.py status | grep -c legacy.*definicion_desde` = 1, con un commit que existe en `origin/main` · el test propio corre como huérfano.

## 2 · FIRMAS DE MESA — dadas
Ninguna nueva hace falta: D-14 (gate de automatización, cumplido arriba), D-21 (test huérfano), D-23 (el job publica derivados por PR, no muta el clon que verifica), E.4 (contador derivado, no reportado), R(a)/D4-A (el `[deriva]` es rutina con auto-merge). Las letras G1 (formato del marcador por rango), H1/H2 (parser de ids) y H5 (`docs/index.md` en el `git add` del job) de la hoja de NC-DECISIONES-1 son de esta misma línea de tubería pero **esperan firma**: no entran aquí; van al `-2` cuando FIRMAS-21 las asiente.

## 3 · LO QUE DIRECCIÓN SABE
- [LEÍDO] `.github/workflows/verify.yml:38-41`: `schedule: cron '0 9 * * *'` (03:00 México); comentario: «el derivador de guardias no corre en schedule (su if exige push o workflow_dispatch)». [EXISTE] job `derivados` nuevo de CI-TIEMPO-2 (#1198, #1208, #1210, #1211): lo que hace y cómo publica lo lees en `forense/encargos/2026-09-26-GEN2-TUBERIA-CI-TIEMPO-2.md` y su nota, no de aquí. Su §NO-CORRIDO dejó P3 (drenar) y P5 (cerrar `c6d9-05` y las NC del canal) a «esta sesión tras el merge»: **verifica su estado (A.17) antes de tocar el job**; si esa sesión sigue drenando, coordina por archivo, no por rama.
- [EJECUTADO] `python3 tools/corrida0.py status | grep definicion` → solo `celdas_validadas_definicion_desde=38dd709`. Claves de legacy presentes: `dependencias_numericas_legacy_activas=67`, `legacy_fuera_del_contador_por_firma__corte_pi=6`, `…__historico_sin_relevo=54`.
- [LEÍDO] `tests/check.py:334-362`: T03 «Referencias colgantes»; `HISTORICOS` incluye `tramite.md` con el comentario «el glob recursivo de T03 (`**/*.*`) no desciende a directorios ocultos como `.claude/`».
- [REPORTADO] Tablero del 27/sep (`TABLERO-PROGRAMA__7_.md`, sha `05238d53…`, archivado por PENDIENTES-2 en `forense/tablero/`) §10: T1 (falso positivo T03: 19 de 117), T9 (suite no termina en 300 s en su puesto; «la corrida nocturna nueva no deja su resumen en el repo»), T10 (marca de definición). §N del inventario: «3 FAIL hasta T31 (T06 ×2, T08 ×1)» en ese puesto; en CI, `check` VERDE en main. Cifras del tablero: se re-derivan, no se copian.
- [EJECUTADO] `git ls-remote --heads origin`: `derivados/auto-36300637254` existe (trozo 2 del canal, «20 CALC, quedan 81»): el canal está vivo y en uso; P1 no puede romperlo.

## 4 · YA HECHO / YA DECIDIDO — por objeto
`git ls-tree -r --name-only origin/main forense/encargos | grep -c 'RESUMEN-SUITE\|CI-TIEMPO-3'` → 0. Homónimos a descartar: `GEN2-TUBERIA-CI-TIEMPO-1` (paralelizó la suite; consumido) y `-2` (job de derivados; consumido, con post-merge en curso). La memoria operativa §3 dice que **no** se propone sacar la vista del canal (E.7) ni empujar directo con deploy key: el resumen viaja por el `[deriva]`, como todo derivado. En vuelo: el drenaje del canal (mismo job: **coordinar**), CIERRE-SEMANAL-2 (`canon/`, `docs/`: si tocas `docs/` para el tablero, rebasa), PENDIENTES-2, RECIBO-ASTRA6-2.

## 5 · PIEZAS
P3 → P2 → P1 es el orden de menor riesgo (P1 toca el job vivo). Por pieza: qué produce · comando de «hecho» · rama prevista: si el job de derivados no admite un paso más sin exceder el tope de tiempo de CI-TIEMPO-2, el resumen se publica desde el job `suite` como artefacto que el job de derivados recoge, o como archivo propio con su propio `[deriva]`: decides tú y lo declaras; lo que no se negocia es que **ningún paso corra la suite dos veces**.

## 6 · LATITUD
Nombres, formato del archivo, umbral de «viejo», dónde lo lee el tablero: tuyos. ≤ 10 líneas adyacentes declaradas. PREGUNTA A MESA prevista: ninguna. NO DECIDES: nada de §7.

## 7 · PAROS — lista cerrada (D-19 estricta)
a) no aplica · b) borrar o reescribir una vista, un `[deriva]` en cola o un sello · c) cambiar el valor de un contador existente (solo se añade una clave) · d) no aplica · e) CAJA · f) objetivo inalcanzable.

## 8 · COMPUERTAS
«El resumen se publica por el canal, nunca por commit directo a main» protege **borrar** (D-23) · «Ningún valor de `status` cambia» protege **adoptar** (E.4).

## 9 · PERÍMETRO Y CONCURRENCIA
Propio: `.github/workflows/verify.yml` (solo el paso de resumen del nocturno y su publicación; nada del job `check`), `tests/check.py` (**solo** T03 y `HISTORICOS`: esta es la excepción explícita a «no editar check.py», porque T03 es el objeto de P2; el test propio nuevo sigue entrando como huérfano), `tools/corrida0.py` (solo la clave nueva de `status`), `tools/tablero_programa.py` (lectura del resumen), archivo derivado del resumen, nota, L0, cascada. Ajeno: `automerge-rutinas.yml`, lote/trozos del canal (`lote_desde_asientos.py` y afines: de CI-TIEMPO-2), vistas, `canon/`. Archivos que OTRO ACTO EN VUELO toca: la sesión post-merge de CI-TIEMPO-2 (`verify.yml` job `derivados`, si aún drena — verifica) · CIERRE-SEMANAL-2 (`docs/`). «Si te encuentras escribiendo fuera de esta lista, PARA.»

## 10 · LO QUE NO HACE · SUCESORES · CIERRE
No cambia qué verifica la suite ni su línea base; no corre la suite en el tablero; no cierra `749c-03` (G1, espera firma) ni implementa G1/H1/H2/H5; no toca `nc_por_clase.py` (PENDIENTES-2). Sucesores: `GEN2-TUBERIA-RESUMEN-SUITE-2` o `CI-TIEMPO-3` con G1/H5 cuando FIRMAS-21 los asiente; el tablero del siguiente corte lee el resumen. Sin módulo de auditoría (no afirma sobre México). El cuerpo no lleva campos para rellenar; `## NO-CORRIDO / RESERVAS` («Ninguno.» obligatorio) y `## CONSUMIDO` las añade /acto. Adendas: `2026-09-27-GEN2-TUBERIA-RESUMEN-SUITE-1-ADENDA-N.md`, selladas al recibirse.

## NO-CORRIDO / RESERVAS

| qué | por qué | impacto | sucesor |
|---|---|---|---|
| P1: primera publicación de `suite-resumen.tsv` por run nocturno o `workflow_dispatch` (run_id) y `tablero_programa.py --actualiza` mostrándolo | NO-VERIFICABLE-AQUÍ — `resumen-suite` sólo corre sobre main tras el merge | el tablero no lee la suite hasta el primer nocturno tras el merge | primer run nocturno tras el merge · `NC-260927-GEN2-TUBERIA-RESUMEN-SUITE-1-6127-01` |

## CONSUMIDO

PR #1224 (`ADR-260927-GEN2-TUBERIA-RESUMEN-SUITE-1-6127-01`; nota `forense/notas/nota-2026-09-27-gen2-tuberia-resumen-suite-1.md`).
