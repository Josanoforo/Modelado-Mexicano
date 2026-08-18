# Nota del acto · SELLA-RUTAS — el procedimiento de `AJUSTADO` deja de ser propuesta

18/ago/2026 · rama `claude/sella-rutas-ajustado-metodologia-023jkq` · SHA de arranque `68a3466` (`origin/main`, coincide con la base que el encargo declara — sin desvío, `git status` limpio al arrancar, sin worktree residual).

## §0 · Arranque, verificado por comando

`git log -1 --format="%h %s"` → `68a3466 Merge pull request #257 from Josanoforo/claude/new-session-yzskdx` — coincide con la base declarada. `data/raw/` ausente — declarado, no paro (este acto no usa microdato). `CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE=cloud_default` — nube, como el encargo asigna; la sonda de red de A.2 se omite porque este acto no toca microdato ni red (regla explícita del punto 4 del ARRANQUE). Ninguna cifra sale de espejo: todas las de abajo se derivaron del clon, con el comando a la vista.

## §1 · Verificación de premisas del encargo, re-derivada (no heredada)

```
sed -n '50p' forense/metodologia-identificacion-vs-ajuste-v0_1.md
  → "**31/jul/2026 · propuesta metodológica, sin sellar. No es canon.**"      EXISTE-NO-SATISFACE (el sello) — confirmado
grep -n "§4\|§5\|§6\|§8" forense/metodologia-identificacion-vs-ajuste-v0_1.md
  → §4 :114 · §5 :134 · §6 :148 · §8 :176 — coincide exacto con lo que el encargo cita
grep -n "ADR-49\|ruta:\|propuesta sin sello" milpa/procedencia.yaml
  → :18 "Exige campo `ruta:`..." · :20 "Rutas argumentadas (propuesta sin sello,
    no canon)... §4" · :23-25 "Sellada por ADR-49 (D2): nace VACÍA..."           EXISTE-SATISFACE / EXISTE-NO-SATISFACE, ambos confirmados tal como el encargo los describe
grep -n "AJUSTADO" tests/check.py tools/curador_registro/validate.py
  → cero líneas que validen `ruta:` de una entrada AJUSTADO (el único match de
    "AJUSTADO" en *.py es la subcadena de OBJETO_NIVEL1_RETROAJUSTADO, ajeno)
grep -n "ESTRATEGIAS" tests/test_celdas_d.py:58
  → {"pseudo_panel","momentos","composicion","transversal_con_seleccion","NO-APLICA"}
    — valida las celdas-D de data/curacion-registro/celdas-d/, dominio distinto
    de milpa/procedencia.yaml; no es el test que vigilaría un AJUSTADO sin ruta
grep -noE "ADR-[0-9]+" canon/gobernanza-v1_15.md | máximo → 101 (ADR-101, ACTO MESA-18AGO)
```

Las cuatro filas de la VERIFICACIÓN DE EXISTENCIA del encargo se sostienen exactas contra `68a3466`. `ADR-50` (31/jul/2026) ya había hecho vinculante el orden de §7 y citado las rutas 2/3/5 de §4 para planear el trabajo, pero no sella su contenido — releído completo para confirmarlo antes de escribir esta nota (`gobernanza:449-475`).

## §2 · C1 — la lectura de mesa

Resumen fiel de §2–§6 presentado en el turno de chat de este acto (identificación vs. ajuste, la partición de §3 ya vinculante por `ADR-50`, las cinco rutas de §4 con su condición dura cada una —incluida la regla de `composicion`: descomposición declarada antes de ver los datos—, y el costo de §5 sin suavizar). `AskUserQuestion` con las tres opciones del encargo (a/b/c). **Respuesta de mesa, verbatim:** *"Sello tal como están escritas."* — opción (a). Nada se escribió antes de esta respuesta.

## §3 · C2 — el sello

`ADR-102` (`canon/gobernanza-v1_15.md`, entre `ADR-101` y `## 5. Deuda declarada`): cita `ADR-49` como el sello de la clase `AJUSTADO` y a sí mismo como el sello del procedimiento — §2 (identificación ≠ ajuste), §4 completo (las cinco rutas verbatim, con la exclusión de "panel intra-sujeto" del enum `ruta:` sin cambiar, ya fijada por `ADR-49`) y §5 (el costo) pasan a canon. Declara explícito que sellar el cómo no puebla nada: cada `AJUSTADO` futuro exige acto propio, con `ruta:` declarada y, si es `composicion`, la regla de descomposición pre-declarada. Falsador: si en tres meses ningún `AJUSTADO` se puebla por ruta sellada, capacidad ociosa, se anota; si alguno se puebla sin `ruta:`, **ningún test lo vigila hoy** (verificado en §1) — se declara el hueco, no se instrumenta aquí.

Rótulos actualizados en `forense/metodologia-identificacion-vs-ajuste-v0_1.md`: nueva línea de cabecera **`v1.0 — SELLADA · 18/ago/2026 · ADR-102`** justo bajo el título; `:50` (ahora un par de líneas más abajo por la inserción) reescrita con la fecha de redacción y la de sello; `§8` gana un párrafo fechado que declara operable la clase por `ADR-102`, sin editar una sola línea del texto original de §1–§7 (ni una línea de contenido metodológico tocada, tal como el perímetro exige). `milpa/procedencia.yaml:20` deja de citar "propuesta sin sello, no canon" y cita `ADR-102` como el sello del procedimiento.

## §4 · Control, pegado crudo

```
ANTES de tocar :101 completo (solo el commit del sello, previo al fix de la cascada):
  python3 tests/check.py            → 21 FAIL · 127 WARN   (+2 sobre el estado previo)
  · T15: canon/estado-programa-v1_10.md:101 cita 101 ADR; gobernanza tiene 102 únicos
  · T16: canon/estado-programa-v1_10.md:221 declara 19 FAIL · 127 WARN vigente; la corrida real da 20 FAIL · 127 WARN
```

Causa: `estado-programa:101` narra el conteo de ADR dos veces en la misma línea — el `102 ADR, protocolo de cambio` de apertura (declaración VIGENTE, sin `{cita-historica}`, la que `T15` exige que coincida con el real) y la cadena `"a N después, con ADR-N..."` al final (la que el encargo pide cascadear). El primer commit del sello tocó solo el cierre de la cadena; la apertura de la misma línea se quedó en `101 ADR` y T15 la marcó, arrastrando a T16 detrás (el FAIL extra de T15 sube el conteo real a 20, que ya no coincide con el `19 FAIL` que `estado-programa:221` declaraba vigente).

```
Corregido `estado-programa:101` apertura (101→102 ADR) y re-corrido:
  python3 tests/check.py            → 19 FAIL · 127 WARN   (idéntico al estado antes de este acto)
  python3 tests/check.py --baseline → LÍNEA BASE: VERDE contra 997482bbda18b52621e24909eedbed0630c7a111
                                       (2 entradas de la línea base ya no aparecen — mejora, no se congela sin --freeze)
```

Los 19 FAIL restantes (T09×8, T05×5, T06×2, T22×2, T08×1, T11×1) son íntegramente preexistentes — ninguno menciona `AJUSTADO`, `procedencia.yaml`, `gobernanza`, `estado-programa` ni ningún archivo de este perímetro. Cero `--freeze` en todo el acto.

## §5 · Lo que este acto NO hace, verificado

No escribió un solo valor `AJUSTADO` en `milpa/procedencia.yaml` (`git diff milpa/procedencia.yaml` — solo el comentario de cabecera, cero líneas bajo `valores:`). No reclasificó ningún `ASIGNADO`. No tocó ninguna ficha (`data/curacion-registro/celdas-d/` sin cambios) ni el pre-registro (`hitoD-preregistro-v2_0.md` sin cambios). No reordenó Hito E — el orden de §7 sigue vinculante solo por `ADR-50`, sin tocar. No creó ningún test ni instrumentó el hueco del falsador declarado en `ADR-102`. No adjudicó `FP-07`. No tocó `forense/firmas-pendientes.tsv` (fuera del perímetro declarado del encargo). **Contadores de medición sobre México: cero.**

## Commit de cierre

`ADR-102` — número re-derivado al escribir esta nota (`ADR-101` era el más alto al arrancar, confirmado por `grep -noE "ADR-[0-9]+" canon/gobernanza-v1_15.md | sort -n | tail`) y re-verificado una segunda vez antes de empujar (`git fetch origin main` → sigue en `68a3466`, sin movimiento). Colisión de número esperada y no ocurrida esta vez; si otro acto en paralelo también reclamó `102`, rige el protocolo de renumeración ya usado cinco veces (`estado-programa:101`, declarado en el propio texto). Cascada `canon/estado-programa-v1_10.md:27,101` actualizada a 102 en sus dos sitios (incluida la apertura de `:101`, que T15 exige y el primer commit había omitido). Encargo `forense/encargos/2026-08-18-SELLA-RUTAS-ajustado-metodologia.md` archivado `CONSUMIDO` con esta rama. Línea en `forense/hallazgos.md`.
