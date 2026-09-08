# `/revisa --post-hoc` · PR #614 · ACTO GEN2-PRE-E5 · CABLEADO-Y-AUTOMATIZACION-FINAL

Corrida diaria de `/revisa` (entorno NUBE). No había PR abierto sin revisar
(el único abierto, PR #615, ya tenía comentario de este revisor sobre su
`HEAD` actual — sin commits nuevos desde entonces). PR #614 es el más
reciente fusionado en las últimas 24 h y no tenía veredicto en
`forense/notas/`.

**VEREDICTO: FUSIONABLE-CON-RESERVA** *(retrospectivo — el PR ya está
fusionado; este veredicto es de calibración, A.3 bloque 1.4)*
`0 BLOQUEA · 2 RESERVA · 0 NO-VERIFICADO · 1 NO-APLICA`

## Identidades

Modo `--post-hoc` (bloque 1.4): no hay vista previa que construir, el
merge ya ocurrió.

```
$ git show --no-patch --format='%H %P' 6f1500e
6f1500e2d279b89051168d7aea599ff144296583 7a958b06940b6c36e416859d7cd79879a8370e5a ed29a2630017b65e627a917eac9011a51a41df41
```

`MERGE=6f1500e` · `P1(base antes)=7a958b0` · `P2(head del PR)=ed29a26`.
Diff `P1..P2` sobre el árbol final:

```
$ git diff --stat 6f1500e ed29a26
(vacío — el árbol del commit de merge es byte-idéntico al HEAD del PR;
el merge no tuvo resolución de conflictos que cambiara nada)
```

Los once puntos corrieron sobre `<merge>^1..<merge>^2` con un
`git worktree add --detach` en el commit de merge (`6f1500e`), retirado al
cerrar.

---

## Hallazgos

**1 · RESERVA (punto 2.5, cifra no re-derivable en este entorno).** El PR
reporta `3 FAIL · 189 WARN`. Re-derivado en vivo sobre el worktree del
merge:

```
$ python3 tests/check.py --baseline 2>&1 | tail -3
  3 FAIL · 188 WARN
────────────────────────────────────────────────────────────────────────
  LÍNEA BASE: VERDE — nada nuevo frente a tests/baseline.json
```

Diferencia de 1 `WARN`. Causa localizada, no fabricada: este entorno de
revisión no tiene `jsonschema` instalado —

```
$ python3 -c "import jsonschema"
ModuleNotFoundError: No module named 'jsonschema'
```

— y la propia suite lo declara al correr: `T-ALTA-RELACION` sale
`NO-CORRIDO -- falta jsonschema`, degradando el conteo de WARN en un
paso frente al entorno donde el PR se generó (que sí lo tenía instalado).
`tests/baseline.json` no cambió (`git diff --stat 7a958b0 ed29a26 --
tests/baseline.json` → vacío), así que la línea base sigue VERDE en
ambos entornos — la cifra exacta de WARN es lo único no re-derivable
aquí, con su razón declarada.

**2 · RESERVA (adyacente al punto 2.8, cabecera de conteo estancada).**
`forense/tablero/TABLERO-PROGRAMA.md` se autodescribe "Estado vivo
derivado" y en el commit de merge declara `ADR máximo `399``:

```
$ git show 6f1500e:forense/tablero/TABLERO-PROGRAMA.md | grep -n 'ADR máximo'
10:- **Gobernanza operativa.** ADR máximo `399` · FP máximo `346` ...
```

mientras que el máximo real en el mismo commit es `400`, y las dos
cabeceras que el punto 2.8 exige que coincidan sí coinciden entre sí y
con ese máximo:

```
$ git show 6f1500e:canon/gobernanza-v1_15.md | sed -n '2p'
### `gobernanza` · v1.15 · 30 de julio de 2026 · **400 ADR**
$ git show 6f1500e:canon/gobernanza-v1_15.md | grep -c '^\*\*ADR-'
400
$ git show 6f1500e:canon/estado-programa-v1_12.md | grep -n '400 ADR' | head -1
27:| **`gobernanza`** | `gobernanza-v1.15.md` | 400 ADR, protocolo de cambio |
```

Causa mecánica, no aleatoria: `tools/tablero_programa.py --actualiza`
(P5 del encargo) corrió en el commit `7c6042e`, **antes** de que la
cascada (`3279155`) añadiera `ADR-400`:

```
$ git log --oneline -- forense/tablero/TABLERO-PROGRAMA.md 7a958b0..ed29a26 | head -1
7c6042e ACTO GEN2-PRE-E5: estado_calc, firewall T35 no circular, ...
$ git log --oneline -S"ADR-400" -- canon/gobernanza-v1_15.md 7a958b0..ed29a26
3279155 Cascada GEN2-PRE-E5: ADR-400, L0, registro-rotulos
```

No es `BLOQUEA`: las cabeceras canónicas (línea 2 de `gobernanza-v1_15.md`
y `L0` de `estado-programa-v1_12.md`, que sí están dentro del alcance
literal del punto 2.8) coinciden entre sí y con el máximo re-derivado.
`NC-0014` cerró correctamente por los contadores GEN2 que sí pedía (P5
del encargo no exigía ADR). Pero el tablero, que se presenta como
snapshot vivo del gobierno del repo, queda desactualizado por una cifra
en su propio ADR dentro del mismo PR que lo "actualizó" — hallazgo real
para el próximo `--actualiza`.

Ningún hallazgo es `BLOQUEA`: ninguna pieza pedida por el encargo quedó
ausente del diff y sin fila en `## NO-CORRIDO / RESERVAS` (punto 2.11).

---

## Los once puntos

| # | Punto | Estado | Comando / evidencia |
|---|---|---|---|
| 2.1 | Encargo archivado verbatim, coherente con reporte | **PASA** | `git log --reverse 7a958b0..ed29a26 \| head -1` → `029db81 0-bis A.3: archiva encargo...` (primer commit, 548 líneas nuevas, 0 sustancia previa). `git diff 029db81 ed29a26 -- forense/encargos/2026-09-08-GEN2-PRE-E5-*.md` → solo `+`, todo después de `──── FIN DEL CUERPO VERBATIM (A.3) ────`. P1-P6 cotejados uno por uno contra el diff: `estado_calc`/`cmd_estado` en `tools/corrida0.py:2253,2307` (P1); `corrida0_generacion` como señal independiente en `tests/check.py:5491-5515` (P2); `N_resultados_gen2_{sellados,pendientes_adopcion,adoptados_activos}` re-derivados en vivo, todos `0` (P3, coherente con `CONTADOR GEN2: cero`); `ENCARGOS-GEN2-v1_5` archivado + sidecar sha256, cuerpos de cola E5-0/E5 resincronizados, `tools/verifica_encargos_gen2.py` nuevo (P4); `tablero_programa.py --actualiza` corrido (P5, ver hallazgo 2); 5 falsadores nuevos localizados por nombre en `tests/test_corrida0.py` (P6). `cmd_registro`/`_lee_oferta` reutiliza `estado_calc()` (`tools/corrida0.py:2355`, comentario explícito "Misma maquina que estado_calc() (P1, NC-0010)") — cumple la exigencia IMPORTANTE del encargo. |
| 2.2 | Spec congelada antes de resultados | **NO-APLICA** | `CONTADOR GEN2: cero.` (línea 7 del encargo) — el acto no mide México. |
| 2.3 | Perímetro declarado vs. tocado | **PASA** | Perímetro declarado en el cuerpo del PR (14 rutas/patrones) vs. `git diff --name-only 7a958b0 ed29a26` (15 archivos): coincidencia exacta en ambas direcciones — cada archivo tocado cae dentro de un patrón declarado, y ningún patrón declarado queda sin archivo tocado. |
| 2.4 | Negativos con conteo de archivos | **PASA** | Los negativos portantes (`N_resultados_gen2_sellados=0`, `_pendientes_adopcion=0`, `_adoptados_activos=0`) se re-derivaron en vivo vía `python3 tools/corrida0.py status --json` sobre el universo de `_dirs_calc()`; coherente con `dependencias_numericas_legacy_activas=162` sin bajar (nada se adoptó todavía). |
| 2.5 | Toda cifra re-derivada por comando | **RESERVA** | Ver hallazgo 1. `59 casos · 59 ok` (`python3 tests/test_corrida0.py`), `OK` ×2 (`tools/verifica_encargos_gen2.py --verifica`), `RUN: CALC-INMUTABLE · YA-SELLADO` (`corrida0.py run CALC-SMOKE-0002`), ADR `399→400`, contigüidad sin huecos — todas re-derivadas exactas. Solo `189 WARN` no reprodujo (188, por dependencia ausente en este entorno, declarada). |
| 2.6 | Originales intactos donde el encargo lo exige | **PASA** | `git diff --numstat 7a958b0 ed29a26` → ninguno de los archivos "No se tocaron" (`milpa/src/**`, `milpa/tramite.yaml`, `milpa/procedencia.yaml`, `procedimiento-scoring-v1_2.md`, CALC sellados, `L-spec-v1_2.json`) aparece en el diff. |
| 2.7 | Escala y universo declarados | **NO-APLICA** | `CONTADOR GEN2: cero` — ninguna cantidad nueva es cifra de México que entre a corpus/canon. La única cifra de gobierno (`400 ADR`) está cubierta por el punto 2.8. |
| 2.8 | ADR/FP: colisión, referencias, contigüidad, cabeceras | **RESERVA** | Max ADR `399→400` sin colisión (`origin/main` en `7a958b0` ya tenía `399`, ninguna renumeración necesaria). FP máximo sin cambio (`346` antes y después — este PR no toca `firmas-pendientes.tsv`). Contigüidad sin huecos (`awk` sobre `1..400`). Cabeceras `gobernanza-v1_15.md:2` y `L0` de `estado-programa-v1_12.md` coinciden entre sí y con `400`. Ver hallazgo 2 (tablero desactualizado, RESERVA adyacente). |
| 2.9 | `tests/check.py --baseline` sobre el merge | **PASA** | `LÍNEA BASE: VERDE` (exit=0) sobre el árbol del commit de merge. `tests/baseline.json` sin diff (`git diff --stat 7a958b0 ed29a26 -- tests/baseline.json` → vacío). Ver hallazgo 1 sobre la cifra exacta de WARN. |
| 2.10 | "Lo que NO hace", respetado | **PASA** | `git diff 7a958b0 ed29a26 -- tools/corrida0.py \| grep -iE '^\+.*(vigencia\|delta)'` → vacío (no implementadas). Ningún archivo `*orquest*` nuevo. T35 sigue emitiendo `warn(...)`, no `fail(...)` (`grep -n 'warn(\|fail('` sobre el bloque T-REPRO → 8/8 son `warn`). `E6` no aparece como sucesor en el cuerpo resincronizado de la cola E5. Ninguno de los archivos "No se tocaron" está en el diff (mismo comando que 2.6). |
| 2.11 | `## NO-CORRIDO/RESERVAS` cotejado contra diff y encargo | **PASA** | El propio encargo archivado trae su `## NO-CORRIDO/RESERVAS` (P2(a) reservado a acto sucesor, P3(e) motor no arranca `PARO-PREMISA`, P3(b) `DIFERIDO-A:C0-D`, P3(c) `NO-VERIFICABLE-AQUÍ`) — pero ésas pertenecen al encargo *revocador* de `D11` (PR #615), no a `#614`. Para `#614`: `git diff 7a958b0 ed29a26 -- forense/no-corrido.tsv` → solo `NC-0010` y `NC-0014` pasan de `ABIERTA` a `CERRADA`, exactamente las dos que el propio encargo esperaba cerrar ("NC-0010 → CERRADA si estado_calc queda operativo. NC-0014 → CERRADA si tablero materializado queda actualizado."); `NC-0007/0008/0009/0011/0012/0013` quedan intactas, tal como el encargo pedía ("No hace falta cerrar aquí"). `P7` (`vigencia`/`delta`, orquestador) queda declarado como "NO IMPLEMENTAR AHORA" en el propio cuerpo del encargo, no como pieza pendiente de asentar — no aplica la lectura de "pieza pedida y ausente sin fila", porque el encargo la excluye explícitamente del alcance, no la pide y omite. |

`CONTADOR: cero mediciones, declarado (infraestructura).`

**Qué NO revisó este pase:** no se re-corrieron los 5 falsadores nuevos de
`tests/test_corrida0.py` uno por uno de forma aislada (`t_estado_calc_derivado`,
`t_gen2_sin_resultado_id_avisa`, `t_resultado_id_sin_generacion_avisa`,
`t_status_mide_no_adopta`, `t_encargo_gen2_desfasado`) — se confirmó su
existencia por nombre y que la suite agregada (`59 casos · 59 ok`) los
incluye, pero no se leyó cada aserción línea por línea contra la
especificación P1-P6. Tampoco se auditó `git blame` de
`tools/tablero_programa.py --json` para confirmar que el bloque
materializado no oculta un segundo desfase además del de ADR. No se
verificó `tools/verifica_encargos_gen2.py --aplica` (opcional, el
encargo no lo exige).

---

Este veredicto es de calibración (bloque 1.4): no se publica en GitHub.
Se abre como PR propio, `[REVISA] post-hoc #614`, que contiene
únicamente este archivo. No aprueba, no fusiona y no empuja nada sobre
`PR #614` ni sobre ninguna otra rama. Fusionar es firmar, y firmar es de
mesa — y este PR #614 ya lo firmó mesa antes de esta revisión.
