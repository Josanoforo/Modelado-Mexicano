# ENCARGO 2 · CELDA-D-COMPLEMENTO — el test y el ADR se contradecían por una lectura, no por un conflicto real

**Acto:** ENCARGO 2 · CELDA-D-COMPLEMENTO · **Entorno:** nube, repo-only (sin `data/raw`, sin corpus, sin microdato) · **SHA de redacción:** `b653bb4` (`origin/main`, confirmado sin drift — `git fetch origin main` deja `origin/main` = `b653bb4`, idéntico a la base de rama) · **Rama:** `claude/celda-d-complemento-conflict-jursjw` · **Depende de:** `tests/test_celdas_d.py`, `propuesta-motor-adaptativo-celda-v0_3.md` §3/§3.1, `ADR-75(b)` (`canon/gobernanza-v1_15.md:878-896`).

## §0 · ARRANQUE

`git status`: rama designada, árbol limpio, `HEAD` = `b653bb4`. Ningún clon nuevo. No hay `data/raw`; el acto no abre microdato — confirmado innecesario, el defecto es de esquema/YAML, no de cálculo.

## §1 · Verificación de existencia — recibida ya contestada por el encargo, verificada de nuevo aquí

**1 · ESTRUCTURA.** `data/INFRAESTRUCTURA-v1_0.md:113` — "## Dominio 5 · Registrar una celda-D del piloto". Fila del índice (`:163`): *"voy a registrar una celda-D → archivo nuevo `data/curacion-registro/celdas-d/<celda_d.id>.yaml`, a mano, y corre `tests/test_celdas_d.py` antes de darla por buena — 23 claves, 7 enums cerrados, regla `COMPLEMENTO→"NO-APLICA"`."* Confirmado: este acto escribe exactamente ese archivo, y nada más de `data/`.

**2 · CONTENIDO.** `ls data/curacion-registro/celdas-d/` → 3 archivos. Corrida real, antes de tocar nada (ver §4 para la salida cruda completa):

```
G5.familismo_obligacion.actitud.yaml [G5.familismo_obligacion.actitud]: ok
G5.obligacion_medida.conducta.yaml [G5.obligacion_medida.conducta]: FAIL -- 1 error(es)
G5.radio_confianza.encuci_vs_enbiare.yaml [G5.radio_confianza.encuci_vs_enbiare]: ok
```

Dos pasan, una falla — confirmado, exactamente como declara el encargo. Vocabulario `NO-APLICA` para este mismo campo, ya en uso antes de este acto:

```
$ grep -n relacion_complemento data/curacion-registro/celdas-d/*.yaml
G5.familismo_obligacion.actitud.yaml:138:  relacion_complemento: G5.familismo_obligacion.conducta
G5.radio_confianza.encuci_vs_enbiare.yaml:204:  relacion_complemento: NO-APLICA
```

**3 · COBERTURA RETROACTIVA.** `propuesta-motor-adaptativo-celda-v0_3.md` — autodatado *"v0.3 · 11/ago/2026"* en su propia cabecera; commit real que lo incorpora a `main`, `816d3b6` "AJUSTE v0.3: incorpora las cinco respuestas de mesa (M0-M10)", fusionado el 12/ago/2026 15:15 (`72a566f`, PR #188). `G5.obligacion_medida.conducta.yaml` nace el 13/ago/2026 22:29:42 (`1224c37`, "ACTO PROC-11 COMMIT 2"). Sin brecha: el contrato exigía `relacion_complemento` un día antes de que la celda existiera — nació ya incumpliendo, no dejó de cumplir después.

**Adicional, no pedido pero relevante para el perímetro:** este defecto ya estaba visto y declarado, sin perseguir, en `forense/hallazgos.md` (entrada 2026-08-14, ACTO RECONCILIA-SPEC): *"Hallazgo ajeno declarado y no perseguido: `test_celdas_d.py` sigue `FAIL` sobre `G5.obligacion_medida.conducta.yaml` (`falta relacion_complemento`) — archivo que este acto no toca."* Tres días sin que nadie lo resolviera — consistente con que el validador no corre en CI (§3, abajo).

## §2 · Paso 1 — la pregunta que decide: ¿`NO-APLICA` cubre el caso de ADR-75(b)?

**Contrato, verbatim (`propuesta-motor-adaptativo-celda-v0_3.md:81`):** `relacion_complemento: <id de la celda-D ligada> | NO-APLICA` — campo obligatorio de nivel `celda_d`, dos únicos valores posibles. No existe un tercer valor "omitido"; el esquema no admite ausencia (confirmado por `REQUIRED_TOP_FIELDS` de `tests/test_celdas_d.py:71`, que no distingue este campo de los otros 22).

**§3.1, verbatim, la mitad que importa:** *"Cuando dos fuentes miden constructos relacionados pero distintos — no el mismo estimando en dos escalas, sino dos estimandos distintos que se informan entre sí — no van en la misma celda como BASELINE/CHALLENGER: cada una abre o alimenta su propia celda-D, y la relación entre ambas se declara como un objeto de relación con su propio momento (`relacion_complemento`)... Caso vivo, decidido por mesa el 10/ago (§4-bis): `familismo_obligacion` — ENASIC (actitud) y ENUT (conducta) son celdas-D distintas, ligadas por una brecha declarable como momento."* Es decir: `relacion_complemento` lleva un ID cuando dos celdas son dos facetas (actitud/conducta) de **un mismo constructo** que se informan entre sí; lleva `NO-APLICA` cuando no lo son. El precedente ya en uso (`G5.radio_confianza...:204`) lo dice en el propio comentario del esquema: *"rol COMPLEMENTO/relacion_complemento (H2, v0.3 §3.1) es para el caso familismo_obligacion (dos celdas distintas ligadas por brecha-momento) — no aplica aquí: esta celda es COMPARACION de un único estimando, **sin celda hermana ligada**."*

**ADR-75(b), verbatim completo (`canon/gobernanza-v1_15.md:880-892`, cita ya presente en la cabecera del propio YAML):**

> P6_38 deja de ser sensibilidad condicional de `familismo_obligacion` y pasa a medida propia, nombrada: `obligación_medida`... El `familismo_obligacion` atitudinal (`P7_12_7`) se renombra en el mismo acto a `norma_de_género`... **Las dos son celdas-D distintas, sin `rol: COMPLEMENTO` entre ellas (mismo criterio que ya separa la celda de actitud ENASIC de la celda de conducta ENUT, arriba) — dos medidas, dos análisis, sin fusión ni jerarquía.**

Y, en el mismo ADR, la parte que el YAML original no citaba (`gobernanza:896`, párrafo de política de denominador):

> El propio criterio de separabilidad de ENASIC-SPLIT... establece que `norma_de_género` y `obligación_medida` son constructos distintos por texto y evidencia — una norma-sobre-terceros y un motivo-propio-reportado, **no dos facetas de lo mismo**.

**Respuesta, con cita: SÍ, `NO-APLICA` cubre el caso.** Dos mecanismos del contrato comparten la palabra "COMPLEMENTO" y no son el mismo: `rol: COMPLEMENTO` (candidato dentro de `candidatos`, §3.1, primera mitad — nunca aplica entre dos `celda_d` separadas) y `relacion_complemento` (campo de `celda_d`, §3.1, segunda mitad — declara si esta celda tiene una hermana ligada). ADR-75(b) nombra el primero ("sin `rol: COMPLEMENTO` entre ellas") — cierto, pero trivial: ninguna celda-D es candidato dentro de otra celda-D, eso no estaba en duda. Sobre el segundo, ADR-75(b) no calla: lo contesta de frente, en el mismo párrafo del denominador, con la frase exacta que el contrato usa para decidir cuándo aplica una relación de complemento — "dos facetas de lo mismo" — y la niega: **no lo son.** A diferencia de actitud/ENUT-conducta (que sí son dos facetas de un mismo constructo, `familismo_obligacion`, y sí llevan `relacion_complemento` poblado entre sí, verbatim en `G5.familismo_obligacion.actitud.yaml:138` y en el propio §4-bis del contrato), `norma_de_género` y `obligación_medida` son "una norma-sobre-terceros y un motivo-propio-reportado" — sin brecha-momento que declarar, sin celda hermana ligada. Es exactamente la condición que el vocabulario ya sancionado resuelve con `NO-APLICA` (`G5.radio_confianza...:204`).

**Ejecutado.** `data/curacion-registro/celdas-d/G5.obligacion_medida.conducta.yaml`:
- Se añade `relacion_complemento: NO-APLICA` al final del bloque `celda_d` (misma posición que en las dos celdas hermanas), con comentario que cita `ADR-75(b)` (`gobernanza:886-889` y `:896`) y el precedente de `radio_confianza:204`.
- La cabecera (líneas 13-19, "NO LLEVA `relacion_complemento`...") **no se borra ni se reescribe** — mismo criterio que ya fijó el campo `correccion_2026-08-14` de la celda hermana (`G5.familismo_obligacion.actitud.yaml:122-133`, "sin borrar la afirmación original"): es la prueba de qué decidió PROC-11 y por qué, y borrarla borraría esa evidencia. Se añade, debajo, un párrafo fechado `CORRECCIÓN 2026-08-17` que explica la lectura correcta, cita este acto y la entrada de `hallazgos.md` del 14/ago, y deja escrito que **no es cambio semántico** (ADR-75(b) no se enmienda, se termina de leer completo) y **no abre ADR nuevo** — el propio ADR ya contestaba la pregunta, solo que la cita original se detuvo a medio párrafo.

## §3 · Paso 2 — el validador no está en CI, en los dos casos

```
$ grep -n "check.py\|svystat\|test_celdas_d" .github/workflows/verify.yml
61:        run: python3 tests/check.py --baseline
64:        run: python3 tests/test_svystat.py
```

`ls .github/workflows/` → un único archivo, `verify.yml`. Dos pasos bloqueantes: `check.py --baseline` y `test_svystat.py`. Cero apariciones de `test_celdas_d`. El defecto de `G5.obligacion_medida.conducta.yaml` vivió cuatro días (13→17/ago) sin que ningún PR lo bloqueara, y ya había sido visto y declarado "no perseguido" el 14/ago (§1, arriba) — confirma que el mecanismo que lo dejó vivir no es que nadie lo viera, es que nada automático lo hacía imposible de ignorar.

**No se añade aquí.** Tocar `.github/workflows/` con dos actos en vuelo (mínimo `PROC-10-BIS`/`MOTOR-COND-v2` y el ciclo `RUTA-SELLO`/`T16`/`T22` recién sellado el mismo 17/ago, ver `forense/notas/2026-08-17-t16-deriva.md`, `2026-08-17-ruta-sello.md`) no vale el riesgo de un tercer fallo de CI en la misma ventana — el propio `verify.yml` lleva un comentario de cabecera fechado 7/ago documentando tres fallos así en 30 minutos. Decisión propia de este acto, declarada y no ejecutada.

**Fila redactada, no escrita — `forense/firmas-pendientes.tsv` es perímetro de `E-DEC`, no de este acto:**

```
id      qué_se_firma    dónde   creado  gatea   estado  firmada_en
FP-NN (número lo asigna quien la escriba — evita colisión con actos concurrentes, mismo criterio que ya aplicó a la numeración de ADR)   ¿Se añade `tests/test_celdas_d.py` a `.github/workflows/verify.yml` (tercer paso bloqueante, junto a `check.py --baseline`/`test_svystat.py`), o se declara explícitamente fuera de CI con razón escrita en el propio workflow?      `.github/workflows/verify.yml` (2 pasos, ninguno corre `test_celdas_d.py`); `tests/test_celdas_d.py` (validador existente, hoy solo se corre a mano)     2026-08-17      el piloto va a escribir "10-15 más" celdas-D (docstring propio del validador, `tests/test_celdas_d.py:9-11`); sin este gate, cada una puede fusionarse incumpliendo `propuesta-motor-adaptativo-celda-v0_3.md` §3 sin que CI lo vea — ya ocurrió una vez (`G5.obligacion_medida.conducta.yaml`, nació incumpliendo el 13/ago, visto y no perseguido el 14/ago, corregido aquí el 17/ago — cuatro días, ningún PR intermedio lo habría bloqueado)      ABIERTA
```

## §4 · Verificación de cierre — comando por comando, antes y después

**ANTES de tocar el YAML:**

```
$ python3 tests/test_celdas_d.py
G5.familismo_obligacion.actitud.yaml [G5.familismo_obligacion.actitud]: ok
G5.obligacion_medida.conducta.yaml [G5.obligacion_medida.conducta]: FAIL -- 1 error(es)
G5.radio_confianza.encuci_vs_enbiare.yaml [G5.radio_confianza.encuci_vs_enbiare]: ok

1 error(es) contra el contrato v0.3 §3:
  G5.obligacion_medida.conducta.yaml: falta campo obligatorio 'relacion_complemento' (v0.3 §3)
exit=1

$ python3 tests/check.py --baseline
[...]
20 FAIL · 130 WARN
────────────────────────────────────────────────────────────────────────
  LÍNEA BASE: VERDE — nada nuevo frente a tests/baseline.json (HEAD congelado 408a3d1d5274fd8dbd5e3c9308eeb8c1f82bbe4b)
────────────────────────────────────────────────────────────────────────
exit=0
```

**DESPUÉS de añadir `relacion_complemento: NO-APLICA` (único cambio de contenido del acto):**

```
$ python3 tests/test_celdas_d.py
G5.familismo_obligacion.actitud.yaml [G5.familismo_obligacion.actitud]: ok
G5.obligacion_medida.conducta.yaml [G5.obligacion_medida.conducta]: ok
G5.radio_confianza.encuci_vs_enbiare.yaml [G5.radio_confianza.encuci_vs_enbiare]: ok

3 archivo(s) de celda-D validan contra propuesta-motor-adaptativo-celda-v0_3.md §3.
exit=0

$ python3 tests/check.py --baseline
[...]
20 FAIL · 130 WARN
────────────────────────────────────────────────────────────────────────
  LÍNEA BASE: VERDE — nada nuevo frente a tests/baseline.json (HEAD congelado 408a3d1d5274fd8dbd5e3c9308eeb8c1f82bbe4b)
────────────────────────────────────────────────────────────────────────
exit=0
```

`check.py --baseline` da la cifra idéntica (`20 FAIL · 130 WARN`, VERDE) antes y después — el cambio es puramente de `celdas-d/`, ajeno a lo que esa suite mide. `test_celdas_d.py` pasa de `1 error(es)` / `exit=1` a `3 archivo(s)... validan` / `exit=0`.

**Merge local.** Rama al día contra `origin/main` (`b653bb4`, sin drift, confirmado en §0/cabecera) — sin conflicto que resolver, sin necesidad de tocar el editor web de GitHub.

**Perímetro respetado, verificado por `git status`/`git diff --stat` antes de commitear:** `data/curacion-registro/celdas-d/G5.obligacion_medida.conducta.yaml` · `forense/notas/2026-08-17-celda-d-complemento.md` (este archivo) · `forense/hallazgos.md` (una línea) · `forense/encargos/2026-08-17-CELDA-D-COMPLEMENTO-test-vs-adr.md`. Nada más de `data/`. `canon/`, `tests/`, `.github/`, `forense/firmas-pendientes.tsv`, `data/curacion-universo/`, `tools/` — cero líneas tocadas, verificado.

**Contadores del programa: 0.** `13 de 27` (Hito D) · `11 de 15` (condicionales) · `0 de 15` (coeficientes) · `1 de 2` (llaves) · `4 de 144`. Ninguno se mueve — este acto corrige un campo de esquema en un registro ya congelado, no mide México ni adjudica nada nuevo.
