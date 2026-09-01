# Nota de cierre · ACTO MAESTRA33-E6 · EMISOR-M-1

1/sep/2026. Encargo `forense/encargos/2026-08-31-MAESTRA33-E6-EMISOR-M-1.md`
(archivado verbatim, A.3), SHA de redacción `a6d8504`. Ejecutado con la
skill `/acto` (ADR-237) por sesión manual, en `ENTORNO: NUBE`.

## ARRANQUE / COMPUERTA

`HEAD` de esta rama = `origin/main` = `55c1a3b` (merge PR #419). `a6d8504`
(SHA de redacción del encargo) es ancestro de `HEAD` — `git merge-base
--is-ancestor a6d8504 HEAD` → sí. `main` avanzó dos merges desde la
redacción (PR #419 `MAESTRA33-B2 · MARCO-M-SORTEA-v1_1`, PR #420
`MAESTRA33-E7 · MAPEADOR-1`, más el commit de reconciliación `2a32c09`); el
efecto sobre el perímetro de este acto se re-derivó en marcha, no se heredó
de prosa — ver el hallazgo FP-212→FP-213 abajo.

COMPUERTA (`marco-M-sorteado-v1_1.tsv en origin/main, B″ fusionado`):
`git ls-tree origin/main -- forense/prereg-duelo-v2/marco-M-sorteado-v1_1.tsv`
→ presente (`blob 91d88db0...`), fusionado vía PR #419. **CUMPLE.**

`data/raw`: ausente (clon fresco, no gitignoreada aquí). Este acto no toca
microdato ni red — no aplica la sonda de entorno de tres partes (A.2).

## A.8 — dirección contra `a6d8504`

Confirmado: `corridas-M/M-TRA-M-01.json` y `M-TRA-M-02.json` EXISTÍAN
(esquema, `grado_DD`) antes de este acto. Herramienta emisora: NO-ENCONTRADO
en `a6d8504` — `git show 16c37b6 --stat` → 2 `.json`, 0 `.py`; el commit
`16c37b6` ("P3 EMITE-M-v0...") los escribió a mano, sin script versionado.
`tools/emite_m.py` (este acto) es la primera herramienta versionada.

## P2 — regresión (antes de emitir)

`python3 tools/emite_m.py` re-deriva `M-TRA-M-01.json`/`M-TRA-M-02.json`
desde `marco-M-sorteado-v1_0.tsv` (más la corrección por referencia de
`candidatos-marco-M-v1_1.tsv`, ADR-233, para `TRA-M-02`) y compara campo por
campo contra lo comiteado. **PASA** en todo campo mecánicamente derivable:
`cita_p`, `cita_ola_calibracion`, `clase`, `conducta`, `determinismo`,
`encuesta`, `estado_M`, `grado_DD`/`razon_grado_DD` (F-DD, ADR-237),
`id_celda`, `invocacion_emisor`, `ola`, `ola_calibracion`, `p`/`valor_punto`,
`regla`, y — verificación no trivial — `variable`/`ponderador` YA
CORREGIDOS para `TRA-M-02` (`AP5_17|AP5_18`, `FAC_SEL`; no los valores stale
`AP5_1_1`/`NO_ENCONTRADO_1944_LINEAS_REVISADAS` de `marco-M-sorteado-v1_0.tsv`
sin corregir).

Dos campos exentos/declarados, no forzados (ver docstring de
`tools/emite_m.py`):

- `fuente` — cita el acto+fecha que corre; distinto por construcción entre
  la emisión original (31/ago) y esta regresión (1/sep).
- `correcciones_aplicadas_por_referencia` — prosa compuesta a mano en el
  original (p.ej. `TRA-M-02`: *"...correcciones C1 (variable AP5_1_1 ->
  AP5_17|AP5_18) y C2 (ponderador NO_ENCONTRADO -> FAC_SEL)"*); este emisor
  deriva la MISMA corrección (mismo valor antes/después, misma cita
  ADR-233) con redacción propia. La divergencia es de estilo, no de valor —
  el valor SÍ se verificó byte a byte en los campos `variable`/`ponderador`
  arriba. Declarado aquí explícitamente en vez de forzar un match de texto,
  que sería exactamente el "ajustar" que P2 prohíbe.

Ningún otro campo divergió. Salida cruda completa del comando en la
descripción del commit `f613f1c`.

## P1 — emisión (11 celdas)

Caminata sobre `marco-M-sorteado-v1_1.tsv`, `elegible_v1_1=='SI'` (11 de
11 filas). Las 11 tienen `regla` cargada en `milpa/tramite.yaml` y ninguna
tenía `corridas-M/M-<id>.json` previo → las 11 se emiten:

| id | encuesta/ola | regla | conducta | p | clase | grado_DD |
|---|---|---|---|---|---|---|
| CIV-M-01 | ENVIPE 2012 | civico.denuncia.miedo_desconfianza | denuncia_con_miedo_o_desconfianza | 0.294313 | MEDIDO·p(tasa base ponderada) | P1 PUNTUA |
| CIV-M-06 | ENVIPE 2017 | civico.denuncia.miedo_desconfianza | denuncia_con_miedo_o_desconfianza | 0.294313 | MEDIDO·p(tasa base ponderada) | P1 PUNTUA |
| CIV-M-08 | ENVIPE 2019 | civico.denuncia.miedo_desconfianza | denuncia_con_miedo_o_desconfianza | 0.294313 | MEDIDO·p(tasa base ponderada) | P1 PUNTUA |
| CIV-M-09 | ENVIPE 2020 | civico.denuncia.miedo_desconfianza | denuncia_con_miedo_o_desconfianza | 0.294313 | MEDIDO·p(tasa base ponderada) | P1 PUNTUA |
| CIV-M-11 | ENVIPE 2022 | civico.denuncia.miedo_desconfianza | denuncia_con_miedo_o_desconfianza | 0.294313 | MEDIDO·p(tasa base ponderada) | P1 PUNTUA |
| CIV-M-12 | ENVIPE 2023 | civico.denuncia.miedo_desconfianza | denuncia_con_miedo_o_desconfianza | 0.294313 | MEDIDO·p(tasa base ponderada) | P1 PUNTUA |
| CIV-M-13 | ENVIPE 2024 | civico.denuncia.miedo_desconfianza | denuncia_con_miedo_o_desconfianza | 0.294313 | MEDIDO·p(tasa base ponderada) | P1 PUNTUA |
| FAM-M-01 | ENIF 2018 | familia.apoyo.recibe_dinero_familiares | recibe_dinero_familiares_para_vejez | 0.457707 | MEDIDO·p(tasa base ponderada) | P1 PUNTUA |
| TRA-M-03 | ENCIG 2013 | tramite.mordida.discrecional | paga_mordida | 0.62 | ASIGNADO | P1 PUNTUA |
| TRA-M-05 | ENCIG 2017 | tramite.mordida.discrecional | paga_mordida | 0.62 | ASIGNADO | P1 PUNTUA |
| TRA-M-07 | ENCIG 2021 | tramite.mordida.discrecional | paga_mordida | 0.62 | ASIGNADO | P1 PUNTUA |

Las 11 caen `P1 PUNTUA` — ninguna coincide con la `ola_calibracion` de su
regla este sorteo (todas son transferencia de ola, misma familia de
instrumento; ninguna transferencia de instrumento esta ronda). Ninguna fila
`SIN-REGLA` esta ronda (las tres reglas que el sorteo cita —
`civico.denuncia.miedo_desconfianza`, `familia.apoyo.recibe_dinero_familiares`,
`tramite.mordida.discrecional` — están las tres cargadas en
`milpa/tramite.yaml`).

`ponderador` = `"NO ESTIMADO EN ESTE ACTO"` en las 11: es el valor real que
`marco-M-sorteado-v1_1.tsv` declara para estas filas (censo de existencia,
`MAESTRA32-E15 · MARCO-M-CORRIGE-Y-CENSA` spec §(e)) — no se sustituyó por
el `ponderador` de calibración de la regla (`FAC_ELE`/`FAC_PER` en
`milpa/tramite.yaml`), que mide otra cosa (la calibración de `p`, no el
diseño muestral de esta celda transferida). Inventar ese salto habría sido
exactamente el defecto que el encargo prohíbe.

`correcciones_aplicadas_por_referencia` = "ninguna" en las 11: ninguna
tiene fila en `candidatos-marco-M-v1_1.tsv` con valor distinto al de
`marco-M-sorteado-v1_1.tsv` (`CIV-M-*`/`FAM-M-01` ni siquiera tienen fila en
esa tabla; `TRA-M-03/05/07` sí, idéntica).

**CONTADOR**: puntos M 2 → 13 (2 preexistentes + 11 nuevos).

## P3 — caminata + skill

`.claude/commands/emite-m.md` (commit `a396b8e`) documenta cómo correr
`tools/emite_m.py` para caminatas futuras y cómo leer el veredicto de la
regresión. **CIEGO**: `forense/prereg-duelo-v2/corridas-R/` nunca se abrió
en este acto. Archivos que sí se abrieron (impresos por el propio tool,
copiados aquí sin editar):

- `canon/modelo-decision-v4_0.md` [lectura via emisor (import del módulo)]
- `forense/prereg-duelo-v2/candidatos-marco-M-v1_1.tsv` [lectura]
- `forense/prereg-duelo-v2/marco-M-sorteado-v1_1.tsv` [lectura]
- `milpa/procedencia.yaml` [lectura via emisor (import del módulo)]
- `milpa/tramite.yaml` [lectura via emisor.cargar_reglas]
- `forense/prereg-duelo-v2/marco-M-sorteado-v1_0.tsv` [lectura, regresión P2]
- `forense/prereg-duelo-v2/corridas-M/M-TRA-M-01.json` [lectura, regresión P2]
- `forense/prereg-duelo-v2/corridas-M/M-TRA-M-02.json` [lectura, regresión P2]

(Más los archivos propios de este acto — encargo archivado, la nota que
citas ahora, `canon/gobernanza-v1_15.md`, `canon/estado-programa-v1_10.md`,
`canon/registro-rotulos.tsv`, `tests/check.py`, `forense/firmas-pendientes.tsv`
— leídos/editados por el CIERRE en cascada, no por `tools/emite_m.py`.)

## Hallazgo — FP-212 renumerada a FP-213 (colisión, commit `2a32c09`)

El encargo (redactado en `a6d8504`, antes de que `main` avanzara) cita
`FIRMA DE MESA (FP-212, verbatim)` para el hallazgo de la regla 3 del
sorteo (`TRA-M-02 sin asiento` en el estrato `tramite|P1|MEDIA`). Entre la
redacción y este acto, `PR #420` (`MAESTRA33-E7 · MAPEADOR-1`) fusionó
primero a `main` y tomó `ADR-247`/`FP-212`; la rama de `MAESTRA33-B2 ·
MARCO-M-SORTEA-v1_1` (que ya traía ese hallazgo con los números
provisionales `ADR-247`/`FP-212`) tuvo que renumerarlos a `ADR-248`/`FP-213`
al fusionar `origin/main` (commit `2a32c09`, regla de la casa: renumera
quien fusiona segundo). **`FP-212` hoy es el recibo de `MAESTRA33-E7`, no
el de este hallazgo** — corrección de premisa de dirección, en vivo, sobre
este mismo acto.

Verificado mecánicamente contra el estado actual de
`forense/firmas-pendientes.tsv`: la fila `FP-213` (no `FP-212`) trae el
recibo del hallazgo de regla 3 (*"Recibo de ACTO MAESTRA33-B2 ·
MARCO-M-SORTEA-v1_1..."*), columna `estado=ABIERTA`, columna `firmada_en`
**vacía** — el placeholder `«[tu texto del punto 2]»` del encargo original
no traía el texto verbatim, y no vive en ningún otro archivo del repo (ni
en `## CONSUMIDO` de `forense/encargos/cola/2026-08-31-MAESTRA33-B2-MARCO-M-SORTEA-v1_1.md`,
ni en la entrada `ADR-248` de `canon/gobernanza-v1_15.md` — ambos solo citan
la firma de familia *"Dame las siguientes automatizaciones"*, no una firma
específica sobre el hallazgo de regla 3).

**Pendiente de dirección**: el texto verbatim de la firma de mesa sobre el
hallazgo de regla 3, para propagarlo a `FP-213` (`firmada_en`/`estado`) —
citado tal cual aunque el propio texto diga "FP-212" (dirección: cítalo
verbatim, la renumeración se declara aparte, no se edita la cita). En
cuanto llegue el texto, se propaga en un commit de cascada separado; este
acto no lo inventa ni lo pospone en silencio.

## P4 — benchmark v1_1 (declaración)

**Sin asiento en `tramite|P1|MEDIA`; `TRA-M-02` informativo, no puntúa.**

El estrato `tramite|P1|MEDIA` de `marco-M-congelado-v1_1.tsv` tiene una
sola fila (`TRA-M-02`). La regla 3 del reglamento sellado (piso 1 por
estrato no vacío, `sorteo-act-pil-3-v2-PROPUESTA.md` Sec.2, `ADR-178`) no
se cumplió para ese estrato en el sorteo v1_1: cuota exacta 0.5 empatada,
desempate alfabético — cero asientos nuevos ahí este sorteo (hallazgo de
`FP-213`/`ADR-248`, no forzado ni re-sorteado). Para el benchmark propio de
v1_1 (representación por estrato de ESTE sorteo, no el conteo acumulado de
`corridas-M/`), `TRA-M-02` — sorteada y emitida en la ronda `v1_0`, con su
propio `grado_DD=P1 PUNTUA` ya sellado en `M-TRA-M-02.json` y sin tocar por
este acto — se cuenta como informativa, no como un punto nuevo de v1_1: no
había asiento nuevo que ganar en su estrato esta ronda, y contarla de nuevo
inflaría el benchmark v1_1 con un punto que en realidad es de la ronda
anterior.

## LO QUE NO HACE (verificado, no solo declarado)

No cargó ni selló reglas — `milpa/tramite.yaml` sin diff en este acto
(`git diff` contra `HEAD~4` en ese archivo: vacío). No tocó `R` —
`corridas-R/` nunca abierto. No puntuó — `tools/emite_m.py` no calcula
ningún estimador contra microdato, solo cita `p` de la regla ya cargada. No
sorteó — `marco-M-sorteado-v1_1.tsv` sin diff en este acto.
