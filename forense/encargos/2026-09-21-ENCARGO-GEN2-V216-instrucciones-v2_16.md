# ENCARGO · ACTO GEN2-V216 · LAS INSTRUCCIONES v2.16 ENTRAN AL REPO EN DOS CUERPOS, `instrucciones_vigentes` SUBE, Y SALE LA PLANTILLA DE ENCARGO v2.1

> ENTORNO: **NUBE** (cualquiera): todo lo que lee está en el repo. Si el hook dice CAJA puedes correrlo igual: dilo en la primera línea de la nota.

CABECERA · SHA de redacción `b219aeef`; re-deriva al abrir · una sola sesión, rama `acto/gen2-v216` · MODELO: Opus (redacta norma) · MODO: **ABIERTO**, con una pieza VERBATIM (P1) · CONTADOR: `cuenta_gen2` NO-APLICA; no mide; no mueve ningún contador · FP/ADR/NC: raíz de acto.
**Si al fusionar `main` choca la línea L0 de `canon/estado-programa-v1_14.md`: NO conserves los dos lados; toma la de `main` y re-inserta solo tu anotación.** `canon/L0/` ya existe: tu anotación va ahí como fragmento. No edites `.github/workflows/verify.yml`, `tests/check.py`, `.gitattributes`, `tools/cierre_acto.py`, `tools/tablero_programa.py`, `tools/estado_comun.py` ni `tools/digesto_tramite.py` (TUBERÍA); lo que necesites de ahí queda en NC con sucesor.

## 1 · OBJETIVO
Que toda sesión de Claude Code y toda conversación de dirección lean las mismas reglas: las que esta semana costaron cinco actos perdidos del piloto 3 (D-22 ampliada, enmienda de cableado), una línea L0 de 27 MB (D-21, D-24), dos transfers con negativos falsos sobre el corpus (A.15), dos filas de cola que el agente no leía (A.16), y las decisiones de mesa sobre medición (§4: comparación primaria con IC, cobertura, PROSPECTIVA/RETROSPECTIVA, θ como generador de retadores). «Hecho» significa: `instrucciones-proyecto-v2_16.md` en el repo **byte a byte igual al adjunto**, con sidecar · `instrucciones-proyecto-v2_16-HISTORIA.md` que absorbe el delta · `CLAUDE.md` y todo sitio que nombre la versión vigente apuntan a v2.16 · `PLANTILLA-ENCARGO-v2_1.md` · ADR que cita la línea de mesa con la fecha del pegado · `tests/check.py --baseline` VERDE.

## 2 · FIRMAS DE MESA — verbatim
A.9, lado proyecto — mesa (21/sep/2026): «estas que me diste ya las pegué en este proyecto». **Fecha del pegado: 21/sep/2026.** El ADR cita esta línea tal cual. A.9, lado repo: es este acto.
Las reglas nuevas del cuerpo ya están firmadas una por una (delta al final del cuerpo, con PR y hallazgo); este acto no reabre ninguna. Las tres preguntas de regla que el cuaderno de mesa (`#963` §7) encontró sin asiento quedan resueltas en el cuerpo: precedencia de `cuenta_gen2` (E.2), toda ola nueva nace reservada (E.6), respaldo del corpus (pendiente de destino, no de regla: fila FP del acto `#974`).

## 3 · LO QUE DIRECCIÓN SABE (contra `b219aeef`)
- `[EJECUTADO]` adjunto: `instrucciones-proyecto-v2_16.md` · sha256 `afc0280b173a147a…` · 5 473 palabras (v2.15: 3 303; el excedente es el DELTA, que la HISTORIA absorbe y el cuerpo operativo suelta). El cuerpo se escribió por secciones sobre el texto operativo v2.15 del proyecto; **no** se generó por script sobre `instrucciones-proyecto-v2_15.md` del repo: si el v2.15 del repo y el del proyecto difieren, ése es un hallazgo (A.9), no un PARO.
- `[EXISTE]` `instrucciones-proyecto-v2_15.md`, `…-HISTORIA.md` y sidecars; `forense/encargos/2026-09-20-GEN2-V215-instrucciones-v2_15.md` (el precedente: úsalo de molde para la HISTORIA y el ADR-566 de gobernanza). `[LEÍDO]` `CLAUDE.md:5`: «Instrucciones vigentes del proyecto: @instrucciones-proyecto-v2_15.md». `[EXISTE]` `tests/test_arnes_sesion.py` (V215 supuso que falla si `CLAUDE.md` no nombra la versión más alta; verifícalo).
- `[EJECUTADO]` `grep -c "PARA-v2.16" forense/hallazgos.md` → **13** por rótulo exacto (A.9). Las 13 están promovidas o absorbidas en el cuerpo; comprueba una por una y, si alguna no quedó, dilo y propón texto (no la metas tú: el cuerpo es verbatim).
- `[LEÍDO]` `forense/encargos/PLANTILLA-ENCARGO-v2_0.md` (92 líneas). La v2.1 la escribes tú (P3); el cuerpo dice qué debe traer.
- `[LEÍDO: .claude/commands/acto.md:341-370]` TUBERÍA ya escribió en `/acto` los ids con raíz de acto, la L0 por fragmentos y la cascada nueva: el cuerpo v2.16 (D-10, D-21, D-24) describe lo que `/acto` ya hace. **No toques `acto.md`** salvo que cite «v2.15» por nombre: ahí solo el número.

## 4 · YA HECHO
Por objeto («v2.16», «v2_16», «PLANTILLA-ENCARGO-v2_1») en `git ls-files`, `decisiones.tsv`, `firmas-pendientes.tsv` y ramas vivas: 0 archivos, ninguna firma ni ADR. **Repítela tú.**

## 5 · PIEZAS
**P1 · El cuerpo operativo, VERBATIM.** El adjunto entra como `instrucciones-proyecto-v2_16.md` byte a byte (sha256 arriba); sidecar. Si el sha no coincide, pídelo: no lo reconstruyas.
**P2 · La HISTORIA.** `instrucciones-proyecto-v2_16-HISTORIA.md` = HISTORIA v2.15 + una entrada por cada renglón del DELTA del cuerpo (regla, fecha, acto/PR, hallazgo o firma), con los mismos rótulos. Cuando la HISTORIA tenga el delta, **no** lo borres del cuerpo operativo: eso lo hace la versión siguiente (el cuerpo es verbatim en este acto).
**P3 · Plantilla v2.1.** `forense/encargos/PLANTILLA-ENCARGO-v2_1.md` (la v2.0 no se edita). Queda bien si: sin «renumera quien fusiona segundo» ni «deriva ids al cierre» — ids con raíz de acto (D-24) · adendas como archivo propio citadas desde el cierre (A.3) · ningún campo que se rellene al cierre ni línea de estado en el cuerpo · adjuntos con sha256, y la opción de embebido entre marcadores · «hecho» por comando sobre el commit final con origin/main fusionado · el test propio entra como huérfano, no «se cablea en CI» (D-21) · cabecera con MODO, LATITUD, PAROS en lista cerrada, compuertas que dicen qué protegen, archivos que otro acto en vuelo toca. `PLANTILLA-LOTE-v1_0.md` y `tramite.md`: solo la cita a la versión.
**P4 · Vigencia.** `CLAUDE.md` → `@instrucciones-proyecto-v2_16.md`; `instrucciones_vigentes` donde viva (tablero derivado o campo): a v2.16; `AGENTS.md` solo la cita. `tests/test_arnes_sesion.py` verde.
**P5 · ADR y cierre.** ADR con raíz de acto en gobernanza citando la línea de mesa de §2 con fecha; fragmento L0; hallazgo con el conteo de semillas (13, por rótulo exacto y patrón declarado); nota de media página.

## 6 · LATITUD
Decides tú: redacción de la HISTORIA y de la plantilla; orden. Replantea y sigue si `instrucciones_vigentes` no vive donde V215 supuso (di dónde vive). Pregunta a mesa, siguiendo: si una semilla no promovida te parece norma (propón texto en la nota).

## 7 · PAROS — lista cerrada
Editar el cuerpo operativo adjunto · borrar versiones anteriores · mover un contador · entorno sin repo.

## 8 · COMPUERTAS
Ninguna. Orden sugerido: P1 → P4 → P2 → P3 → P5.

## 9 · PERÍMETRO
Propio: `instrucciones-proyecto-v2_16*.md` y sidecars · `forense/encargos/PLANTILLA-ENCARGO-v2_1.md` · una línea en `PLANTILLA-LOTE-v1_0.md` y `.claude/commands/tramite.md` · `CLAUDE.md`, `AGENTS.md` (cita) · el sitio de `instrucciones_vigentes` · hallazgos, ADR, L0, nota, cascada. Ajeno: `acto.md` salvo el número de versión · todo lo demás. Si te encuentras escribiendo fuera de esta lista, PARA.

## 10 · NO HACE · SUCESORES · CIERRE
No reescribe encargos archivados · no borra el delta del cuerpo · no instrumenta linters. Sucesor: v2.17, que suelta el delta absorbido y revisa la caducidad de A.3+, D-16–D-24 (§9) el 21/dic/2026. Auditoría §5: no aplica. `## NO-CORRIDO / RESERVAS` · `## CONSUMIDO`.

## NO-CORRIDO / RESERVAS

- **Qué:** `.claude/commands/tramite.md` — línea de cita a la versión de la plantilla (P3 del encargo: "`PLANTILLA-LOTE-v1_0.md` y `tramite.md`: solo la cita a la versión").
  **Por qué:** `NO-VERIFICABLE-AQUÍ` no aplica — se verificó y no hay nada que hacer: `grep -n "PLANTILLA-ENCARGO" .claude/commands/tramite.md` no encuentra ninguna cita a `PLANTILLA-ENCARGO-v2_0` ni a ninguna versión de la plantilla en ese archivo. No había línea que actualizar.
  **Impacto:** ninguno — el archivo no cita la plantilla y no queda desactualizado.
  **Sucesor:** `SIN-ASIGNAR` (nada que resolver; se deja escrito para que un acto futuro no repita la búsqueda).

- **Qué:** `AGENTS.md` — actualizar cita a la versión de instrucciones (P4 del encargo: "`AGENTS.md` solo la cita").
  **Por qué:** `NO-VERIFICABLE-AQUÍ` no aplica — se verificó: `grep -n "v2_15\|v2\.15" AGENTS.md` no encuentra ninguna cita de versión. El archivo no existe con ese contenido en este repo (no se creó ni se tocó).
  **Impacto:** ninguno.
  **Sucesor:** `SIN-ASIGNAR`.

- **Qué:** Dos semillas `PARA-v2.16` (`hallazgos.md:967` `MOTOR-LINAJE-1`; `hallazgos.md:1016` `ARBITRO-MARGINALES-1`, la mitad sobre «vencido» sin retador) que dirección esperaba ver promovidas y el cuerpo adjunto no trae.
  **Por qué:** `PARO-PREMISA` no aplica — no es que la premisa cayera, es que el cuerpo verbatim (P1, no editable por este acto) simplemente no las escribió. Se declaran con texto propuesto en la HISTORIA (§6 del encargo: "si una semilla no promovida te parece norma, propón texto en la nota — no la metas tú").
  **Impacto:** ninguna norma nueva sobre el estado `superado` de un índice de linaje ni sobre «vencido» sin retador; ambas siguen sin instrumentar hasta que mesa decida.
  **Sucesor:** `DIFERIDO-A:v2.17` (§9 del cuerpo lo declara explícitamente como su primera tarea).

## CONSUMIDO
Ejecutado por `ACTO GEN2-V216`, rama `acto/gen2-v216`, PR #978 contra `main`.
