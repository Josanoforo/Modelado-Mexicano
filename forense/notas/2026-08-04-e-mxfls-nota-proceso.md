# Nota de proceso — ENCARGO E-MXFLS, 2026-08-04

## ARRANQUE (Bloque D)

1. **REPO.** Clon existente en `~/Modelado-Mexicano`. **No estaba en `main`**: rama `sesion/cal-conf-faseb-pos4-envipe-paso1`, ~70 archivos en staging de un acto ajeno no relacionado (verificado, no tocado). Este acto no trabajó ahí — creó worktree dedicado (punto 2 de esta nota).
2. **SHA.** El encargo declaraba `origin/main = 2bc613b`. Al hacer `git fetch --all --prune`, `origin/main` real era `bd2c975` (PR #113, "C-06a: localiza las cinco cifras de conf.06", fusionado después de que se redactara el encargo). **No es PARO** — se verificó `git merge-base --is-ancestor 2bc613b origin/main` (YES) y `git diff --stat 2bc613b bd2c975`: el único delta son `canon/gobernanza-v1_15.md` (ADR-61), `canon/estado-programa-v1_10.md`, `forense/hallazgos.md`, `milpa/procedencia.yaml`, y dos notas forenses de C-06a/ADR-61 — **ninguno toca `CAL-G3`, `tests/calg3_fasec.py`, `tests/calx_g3.py`, ni ningún archivo de este perímetro.** Se trabajó contra `bd2c975`, diferencia reportada aquí en vez de ajustar el encargo.
3. **`data/raw`.** Ausente en el worktree nuevo (esperado, gitignorado). Enlazado: `ln -s /home/pc0/mm-corpus/raw data/raw` — mismo patrón que otros worktrees del programa (verificado contra `~/mm-hitoD-r1-3-canal-confianza/data/raw`, mismo destino). No se descargó nada nuevo.
4. **ENTORNO.** `CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE` = vacío/no seteado → firma Ubuntu-con-red, consistente con "Ubuntu con data/raw" que el encargo asigna. Este acto no necesitó la sonda de red contra INEGI (no descarga nada; ENNViH ya está en el corpus compartido) — se salta el punto, como el propio Bloque D permite cuando el acto no toca microdato ni red nueva.
5. **ESPEJO.** No se usó ningún espejo del proyecto. Toda cifra de la ficha sale del clon fresco en el worktree de este acto, con archivo:línea o comando citado.

**ACTOS VIVOS.** El encargo dejó la línea en blanco ("ACTOS VIVOS DECLARADOS POR MESA AL LANZAR: ______"). Se verificó por cuenta propia, contra origin, no contra ningún worktree: `gh pr list --state open` → un solo PR abierto, **#114** (`sesion/hitoD-r1-3-canal-confianza`, "canal de confianza personal → adopción fintech", R1.3). Hipótesis distinta de `G3`, sin traslape de archivos con este acto (no toca `hitoD-preregistro` en la zona de `CAL-G3`, no toca `procedencia.yaml` en la fila de `G3`). `git worktree list` no mostró ningún otro worktree con nombre o rama relacionados a `G3`, `horizonte_temporal`, `CAL-G3`, `ID-G3` o `e-mxfls`. Se trata como "sin colisión detectada", no como "colisión descartada con certeza" — la salvedad de `[[project-modelado-mexicano]]` sobre dos sesiones arrancando en el mismo worktree recién creado no aplica aquí porque el worktree de este acto es de nombre único y se creó en este mismo acto.

## PERÍMETRO Y CONCURRENCIA

Tocado: `forense/notas/2026-08-04-e-mxfls-ficha-borrador.md` (nuevo), `forense/notas/2026-08-04-e-mxfls-nota-proceso.md` (nuevo, este archivo), `forense/hallazgos.md` (append, una línea). **No tocado:** `canon/`, `milpa/procedencia.yaml`, `forense/hitoD-preregistro-v2_0.md` (el cuerpo ni el bloque append-only), `tests/`, ningún archivo de `CAL-G3`. Ningún `.dta`/`.zip` de microdato abierto — solo PDF de documentación pública (declarado exhaustivamente al final de la ficha).

## Qué hizo este acto y qué no

**Hizo:** (1) inventario exhaustivo de qué reportó `CAL-G3` Fase C, con archivo:línea (Paso 0); (2) verificó, contra el manual de codificación y el cuestionario reales (no heredado), tres candidatos de desenlace nombrados-y-no-corridos por la propia Nota 7 (`AH`, `SE`, `CR`), descartó `CR` por confundidor mecánico de primer orden y prefirió `AH` sobre `SE` por potencia y ajuste teórico, declarando el trade-off; (3) encontró y nombró un confundidor no atrapado antes en este corpus —circularidad AFORE↔IMSS— y lo resolvió modificando la definición de exposición (excluye `tb33p_d`), con la degradación asimétrica de la escala declarada antes de ver ningún dato; (4) escribió la ficha `ID-G3` completa, con chequeo de alcanzabilidad tipo `CAL-X` pre-calculado (técho, SE, IC95%sup) mostrando el trabajo; (5) verificó independientemente ponderador/estrato/UPM contra el FD real de las tres olas, **corrigiendo** una cita existente (`censo-estimabilidad-coeficientes-v1_0.md:36`, que afirmaba estrato/UPM citados cuando no lo están — ver Paso 0.2 de la ficha).

**No hizo, por diseño del encargo:** no corrió ninguna estimación, no abrió ningún `.dta`, no tocó `milpa/procedencia.yaml`, no escribió en el bloque append-only de `hitoD-preregistro`, no selló nada. La ficha queda en `forense/notas/` para que mesa la revise y, si la aprueba, la traslade al pre-registro formal en acto aparte (con su propio commit "el primer resultado que produzca este procedimiento es el que se reporta", Bloque D, antes de abrir ningún `.dta`).

## Corrección encontrada, para el registro

`forense/censo-estimabilidad-coeficientes-v1_0.md:36` (04/ago/2026, Encargo E-CE) afirma que `CAL-G3` "cita su propio ponderador/estrato/UPM por ola". Verificado contra `hitoD-preregistro-v2_0.md` Notas 7-10 completas y contra `forense/notas/2026-07-30-calg3-fasec-salida.txt`: **`CAL-G3` cita ponderador (sí) pero no cita estrato ni UPM en ningún punto** — sus 60 estimaciones usan EE robusto HC1/sandwich, sin ajuste de diseño muestral complejo. No se edita `censo-estimabilidad-coeficientes-v1_0.md` (append-only, fuera de perímetro de este acto) — se deja constancia aquí y en la ficha para que el acto que lo toque próximamente lo corrija con cascada, mismo patrón que `ADR-58(e)`/`ADR-60` usaron para deuda de cascada ajena.

## Verificación de suite

`tests/check.py --baseline` corrido en el worktree de este acto antes de abrir PR (salida y resultado en el mensaje de PR / commit — este acto no modifica ningún test ni ningún archivo que la suite audite, así que no se esperaba ni se encontró cambio de estado).

## Cierre

No impidió medir. Contadores movidos: 0 — ficha borrador entregada a mesa; la corrida y la eventual reversión del rótulo (ADR-57, cláusula de Reversión por coeficiente) son actos posteriores.
