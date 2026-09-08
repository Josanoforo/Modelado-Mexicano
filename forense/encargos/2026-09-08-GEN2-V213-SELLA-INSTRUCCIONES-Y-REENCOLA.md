ESTADO: EN-CURSO
ENTORNO: NUBE
ENCOLADO: 2026-09-08 · lanzado por mesa directo (sin paso previo por `forense/encargos/cola/`), pegado verbatim en el mensaje que invocó `/acto` — este commit es el 0-bis A.3 que lo escribe al repo, per `.claude/commands/acto.md` §"El argumento...".
BITACORA:
- 2026-09-08 · COMPUERTA (A.9) verificada por pregunta directa a mesa, no por archivo: mesa confirmó explícitamente, vía `AskUserQuestion`, que el texto de v2.13 (v2.12 íntegra + el delta `instrucciones-proyecto-v2_13-DELTA-2026-09-08.md`, adjuntado por el operador en este mismo lanzamiento) ya está pegado en las instrucciones del proyecto de Claude, con fecha 2026-09-08. Sin archivo que lo demuestre (A.9 gobierna un artefacto fuera del repo, misma exención que Bloque D/D-10), la única verificación posible es la declaración de mesa en el lanzamiento — que es exactamente lo que la propia COMPUERTA pide.

──── CUERPO VERBATIM DEL ENCARGO (A.3) · el despachador NO lo edita ────

V213 · ACTO GEN2-V213 · SELLA INSTRUCCIONES v2.13 Y REENCOLA EL ORDEN NUEVO

Cabecera: NUBE · Sonnet · COMPUERTA: mesa declara en el lanzamiento, con fecha, que v2.13 ya está pegada en el proyecto de Claude (A.9). NO se lanza en UBUNTU. Qué hace: (1) instrucciones-proyecto-v2_13.md = v2.12 íntegra + el delta adjunto (instrucciones-proyecto-v2_13-DELTA-2026-09-08.md, verbatim), con sidecar; instrucciones_vigentes del tablero → v2.13 (receta ya deriva por versión máxima). (2) Enmienda a A.1 aplicada como el delta la declara (no se reescribe v2.12; v2.13 la lleva). (3) Reencola: reemplaza en forense/encargos/cola/ los cuerpos de E5-0, E5, E6 y E7 por los de este documento, verbatim, con estados LISTO- (E6) y GATED (E7, E5-0, E5) según sus compuertas. (4) hallazgos.md: entrada «v2.13 entregada íntegra; las cuatro PARA-v2.13 quedan absorbidas; fecha de pegado en el proyecto: <la que mesa declare>». (5) ADR con la línea de A.9 verbatim. Sección ## NO-CORRIDO / RESERVAS y ## CONSUMIDO. Perímetro: instrucciones-proyecto-v2_13.md + .sha256 · forense/encargos/cola/ (cuatro reemplazos) · forense/hallazgos.md · cascada (ADR, L0, rótulos, tests/check.py solo exenciones). No toca corrida0.py, milpa/**, canon de reglas, specs. Si te encuentras escribiendo fuera de esta lista, PARA — el perímetro estaba mal calculado y saberlo vale más que el atajo. Contador: instrucciones_vigentes v2.12 → v2.13; para_v2_13_entradas deja de contar (absorbidas).

## NO-CORRIDO / RESERVAS

| qué | por qué | impacto | sucesor |
|---|---|---|---|
| Paso 9 de la cascada estándar de `/acto` (abrir UN PR contra `main`) | `DECISIÓN-DE-MESA-PENDIENTE` — la política de esta sesión (harness) es no crear un pull request salvo pedido explícito del operador, y este lanzamiento no lo pidió | `## CONSUMIDO` (abajo) no puede citar un número de PR real; cita el/los commit(s) de esta rama en su lugar, tal como `.claude/commands/acto.md` paso 11 permite explícitamente ("o el commit, si el acto no abre PR") | `SIN-ASIGNAR` — mesa decide si pide el PR en un mensaje posterior; registrado como `NC-0009` en `forense/no-corrido.tsv`, `ABIERTA` |

## CONSUMIDO

Ejecutado en la rama `claude/v213-instrucciones-reencola-16y3i4`, sin PR (ver `## NO-CORRIDO / RESERVAS` arriba y `NC-0009`). Commit real: `bb70945` — sella `instrucciones-proyecto-v2_13.md` + `.sha256` y `instrucciones-proyecto-v2_13-DELTA-2026-09-08.md` + `.sha256`, reencola `forense/encargos/cola/{GEN2-E5-0,GEN2-E5,GEN2-E6,GEN2-E7}`, añade la entrada de `forense/hallazgos.md`, `ADR-395` (`canon/gobernanza-v1_15.md`), el recifrado de `L0` (`canon/estado-programa-v1_12.md`), `canon/registro-rotulos.tsv` (`GEN2-V213`), la exención T25 en `tests/check.py` y `forense/no-corrido.tsv` (`NC-0009`). `python3 tests/check.py --baseline`: **LÍNEA BASE VERDE** (3 FAIL preexistentes/180 WARN, sin entrada nueva frente a `tests/baseline.json`).
