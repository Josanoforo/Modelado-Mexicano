# GEN2-PENDIENTES-3 · nota de cierre · 28/sep/2026

ADR `ADR-260928-GEN2-PENDIENTES-3-6e2d-01` · CAJA (`ENTORNO-DERIVADO = CAJA`) · Opus 5.5 · base `98f80cc75` · 0-bis `6e2d0318`.

Contadores: cero mediciones; no adopta. `no_corrido_abiertas` 497 → 312, sólo por cierres con cita.

## ARRANQUE
- Guardias 0.a–0.d: base al día (0 detrás), árbol limpio, sin duplicado (rama, worktree y PR: 0), `limpia_arbol --reporta` pegado en sesión.
- `data/raw` enlazado a `/home/pc0/mm-corpus/raw`.
- `ENTORNO-DERIVADO = CAJA`, igual al que declara el encargo.

## Premisas que cayeron (logística, declaradas)
- **Adjunto.** `PENDIENTES-PROGRAMA__4_.md` llegó como `Downloads/PENDIENTES-PROGRAMA (4).md` y su cabecera dice «inventario v3». Deriva del mismo `98f80cc75` y sus clases suman 497 = 11/63/75/4/122/222, como declara el encargo. Se archivó verbatim como `forense/analisis/pendientes-3/PENDIENTES-PROGRAMA-v4.md`, sha256 `56eb060f…` (sidecar).
- **Vocabulario del «hecho».** `nc_por_clase.py --json` no emite `VENCIDA-CANDIDATA` ni `ASIGNAR`: esas son clases del inventario (§C), que las mapea desde `SUCESOR-YA-FUSIONADO` y desde `SIN-ASIGNAR`/`NO-CLASIFICABLE`. Contra el vocabulario literal, el criterio daba 0 antes de empezar (degenerado), así que se midió contra el mapeo. Para que el clasificador lea el dueño, se añadió en 6 líneas (D-21) que el token de dueño manda sobre la prosa (A.16).
- **Dueños.** La lista cerrada de P4 no incluye EN-CURSO, pero §4/§5 lo exigen para las filas de actos en vuelo. Se admite con la forma `EN-CURSO (<ACTO> · rama <rama>)`. `CAJA (<encargo archivado>)` se lee como «un encargo archivado lo ejecuta», con la ruta verificada por el test.
- **Sucesores inexistentes.** GEN2-CIERRE-SEMANAL-3 no tiene encargo archivado ni rama en vuelo, así que no se le asignó nada (§7 c).
- **PR.** Un solo PR, con un commit por bloque: P1 mecanismo `bda84cc6` → barrido `1c6790d4`. La latitud de §6 lo permite, y la compuerta «mecanismo con test antes del barrido» se cumple por el orden de los commits.

## P1 · mecanismo
- `tools/cierre_acto.py`:
  - `--nombran <RÓTULO>` lista las NC que nombran al acto, por nombre con frontera. Control positivo: GEN2-OBTENCION-EXTERNA-2 → 8.
  - Fase A con `--encargo` sale con código 1 cuando hay FALTA-DICTAMEN o RUTA-SIN-SUCESOR.
- `tests/test_nc_cierre_hacia_atras.py`, casos A–F:
  - un acto sintético que nombra una NC falla sin dictamen y pasa con él;
  - la guardia rechaza una NC nueva sin sucesor archivado.
  - Huérfano censado `CORRE-EN-CI`; `ci_guardias --ejecuta-huerfanos` → `OK`.
- `/acto` paso 10-bis.
- Delta v2.17 → v2.17.1 en `gobierno/pendiente-de-pegado/`. El cuerpo v2.17 no se tocó.

## P2–P4 · barrido
- **Evidencia.** Ocho ejecutores Sonnet de solo lectura (lotes A1–A8, `evidencia/prop-A*.tsv`) propusieron por fila con ruta, comando y salida.
- **Adjudicación.** La hizo el auditor en `arma_dictamen.py`: reglas por propuesta más excepciones con razón, fila por fila.
  - 11 cierres por firma pasaron a MESA: la firma exige un producto que no existe.
  - 10 cierres por firma pasaron a EN-CURSO: el producto viaja en CALC-ALTERNOS o C1-SUCESORES.
  - 7 cierres propuestos se rechazaron por producto distinto, firma que no nombra la fila o cita sin re-verificar.
  - Las propuestas EN-CURSO hacia la rama `[deriva]` se pasaron a MESA: el `[deriva]` es un canal automático, no un acto.
- **Muestreo.** Se re-ejecutaron los comandos de 8 cierres por producto y los 8 coincidieron.
- **Decisiones reversibles.** Las 170 se decidieron por delegación y cada una está en `decididas-por-delegacion.tsv`. 30 se cierran con la opción recomendada; el resto queda con dueño `MESA (2026-10-05) · encargo por escribir`.
- **Aplicación.** Se hizo por línea (`aplica_dictamen.py`): `git diff --numstat` = 497/497 y ninguna fila ajena tocada.

## «Hecho», por comando
- `python3 tools/nc_por_clase.py --json` → `SUCESOR-YA-FUSIONADO` 0 · `SIN-ASIGNAR` 0 · `NO-CLASIFICABLE` 0 (312: ESPERA-MESA 218 · EN-CURSO 43 · ESPERA-ADQUISICION 27 · ESPERA-APERTURA 18 · ESPERA-ACTO-NOMBRADO 6).
- `python3 tests/test_nc_cierre_hacia_atras.py --libro` → «fuera de la lista cerrada: 0».
- `python3 tools/cierre_acto.py --encargo forense/encargos/2026-09-28-GEN2-PENDIENTES-3.md --sin-suite` → dictaminadas 185 · FALTA-DICTAMEN 0 · RUTA-SIN-SUCESOR 0.

## Para mesa
`forense/analisis/pendientes-3/hoja-mesa-pendientes-3.md`, con dos secciones:
- 13 irreversibles con opciones.
- 39 acciones de titular con receta de un minuto. El inventario contaba 11 HUMANO; los ejecutores añadieron filas que piden correo, registro con identidad o una corrida de CI/Actions.

## Límites declarados
- **Cobertura.** Fuera de los 8 re-ejecutados, los cierres por producto descansan en la salida que citó el ejecutor. No todos se re-corrieron.
- **CI.** Cuatro cierres dependen de que un job de CI exista y su PR esté fusionado; no se leyeron logs de run.
- **P3 no abrió ninguna base.** La verificación de las 122 ESPERA-DATO fue de existencia, sha y metadatos. No se abrió ni recalculó ninguna ola reservada.
