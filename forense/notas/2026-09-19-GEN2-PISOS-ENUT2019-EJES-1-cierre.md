# ACTO GEN2-PISOS-ENUT2019-EJES-1 · CIERRE — cascada, contadores y lo que no se corrió

Dictamen sustantivo (P0/P3): `forense/notas/2026-09-19-GEN2-PISOS-ENUT2019-EJES-1-dictamen.md`
(congelado; su sha256 viaja en `metadata_source_sha256` de la tabla de identidad y
`tests/test_pisos_enut2019.py` lo verifica byte a byte — no se edita después del sello).
Encargo: `forense/encargos/2026-09-19-GEN2-PISOS-ENUT2019-EJES-1.md`. ADR: `ADR-556`
(candidato del comando de la casa era `ADR-552`; `PR #906`, `GEN2-TABLERO-SENAL-1`, fusionó
primero y lo tomó junto con `NC-0359`/`NC-0360`; después `PR #907`, `GEN2-C2-COMPUESTO-IC-ENVIPE2025-1`,
tomó `ADR-553` y `NC-0361`; luego `PR #905`, `GEN2-RELEVO-TANDA-1`, tomó `ADR-554` y `NC-0362`..`NC-0366`,
y `PR #903`, `GEN2-CELDA-D-PILOTO-3-P0`, tomó `ADR-555` y `NC-0367` — renumerado aquí tres veces, a `ADR-556`
y `NC-0368`..`NC-0373`, regla de la casa: renumera quien fusiona después).

## 1 · ARRANQUE (cinco líneas, crudas)

- **0.a** `git rev-list --count HEAD..origin/main` → `0` al abrir (`a92126f0`); `4` al
  cerrar (`#902`), fusionados sin conflicto antes de la cascada.
- **0.b** `git status --porcelain` → vacío antes del 0-bis.
- **0.c** `git ls-remote --heads origin | grep -i 'pisos-enut\|enut2019'` → 0 ·
  `git worktree list | grep -i …` → 0 · `gh pr list --search PISOS-ENUT2019 --state open` → 0.
- **0.d** `tools/limpia_arbol.py --reporta`: base al día (`al_dia=SI`), 4 ramas remotas
  sin PR abierto (`claude/*`), worktrees vivos listados (no se borra nada desde aquí).
- **1 REPO** `/home/pc0/mm-gen2-pisos-enut2019-ejes-1` (worktree nuevo sobre `a92126f0`;
  el clon padre estaba en `claude/tramite-2026-09-17`, no en `main`).
- **3 data/raw** enlazado a `/home/pc0/mm-corpus/raw` + `data/raices.local.yaml` copiado.
- **4 ENTORNO** `python3 tools/entorno.py --sonda-red` → `commit=a92126f0a930 ·
  git_status=LIMPIO(0) · python=3.14.4 · numpy=2.3.5 pandas=2.3.3 scipy=1.16.3 yaml=6.0.3
  pyreadstat=1.3.6 · CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE=sin_variable … · red=200 ·
  raices=data_raw:SI descargas_mx:SI · corpus=SI(examinados=419)`.
- **A.8 / ya_medido**: este acto no clasifica, pre-registra, carga ni sella ninguna regla
  del motor (dictamen NO-CONSTRUIBLE); no aplica.

## 2 · COMPUERTA — cumplida vacuamente al abrir, y lo que pasó después

`COMPUERTA: que GEN2-CELDA-D-PILOTO-3-P0 haya cerrado su rama — un acto de caja a la vez`.
Verificado a las 20:47-20:50 (hora local, 19/sep): `git ls-remote --heads origin | grep -i
piloto` → 0; `git worktree list | grep -i piloto-3` → 0; `gh pr list --state open` → 0.
`PILOTO-3` cerró por `#894` (`## CONSUMIDO` en `origin/main`, rama borrada); su P0 en caja
(`NC-0355`) no tenía encargo, rama, worktree ni PR. Las tres ramas `claude/*` vivas
(`RECIBO-CODEX-6`, `RELEVO-TANDA-1`, `TABLERO-SENAL-1`) declaraban `ENTORNO: NUBE; NO caja`.

Al correr `tools/cierre_acto.py` (preflight) el remoto ya traía **tres actos de caja
nuevos**, todos posteriores al 0-bis de este acto (`992f454`, 20:50 local):
`acto/gen2-c2-compuesto-ic-enif2024-1` (20:53), `acto/gen2-c2-compuesto-ic-envipe2025-1`
(20:54) y `claude/lucid-lamport-32k9t3` = `GEN2-CELDA-D-PILOTO-3-P0` (03:00 UTC = 21:00
local), los tres `ENTORNO: CAJA`. **Decisión del ejecutor, declarada:** no parar. La
compuerta existe por la colisión de CALC-id del 19/sep; este acto no sella ningún CALC
(P0 salió NO-CONSTRUIBLE), así que esa clase de colisión no puede producirse desde aquí.
Lo que sí colisiona (`ADR-556`, `NC-0368..0364`) se resuelve por la regla de la casa. Si
mesa lee la compuerta como «PARO aunque el acto no selle», la fila correspondiente de
`## NO-CORRIDO / RESERVAS` lo deja a su decisión.

## 3 · Qué escribió este acto (perímetro) y qué no

| archivo | qué |
|---|---|
| `forense/encargos/2026-09-19-GEN2-PISOS-ENUT2019-EJES-1.md` | 0-bis A.3 verbatim; `## NO-CORRIDO / RESERVAS` y `## CONSUMIDO` al cierre |
| `forense/notas/2026-09-19-GEN2-PISOS-ENUT2019-EJES-1-dictamen.md` | P0 (tabla actividad por actividad, veredicto) + P3 (a)/(b) |
| `forense/prereg-caja/PISOS-ENUT2019-ejes-metadatos-v1_0.tsv` + `.sha256` | tabla de identidad: 11 filas `NO-CONSTRUIBLE`, categorías leídas del yaml del árbitro, `metadata_source` = dictamen + sha256 |
| `tools/marcador_segmento.py` | enlace de la segunda tabla (**tres sitios**, no una línea — `NC-0372`) |
| `data/corrida0/marcador-segmento.tsv` | re-derivado por `--escribe`; diff = exactamente las 11 filas ENUT |
| `tests/test_pisos_enut2019.py` | rejilla emitida == rejilla del árbitro; causa única; sin CALC; sidecar/fuente byte a byte; transporte de la causa por el marcador |
| cascada | `hallazgos.md` (una entrada), `no-corrido.tsv` (`NC-0368..0364`), `gobernanza-v1_15.md` (`ADR-556`), `estado-programa-v1_14.md` (L0), `registro-rotulos.tsv` (una fila) |

**No escribió**: `forense/prereg-caja/PISOS-ENUT2019-ejes-spec-v1_0.md` (P1 — no hay spec
que congelar sobre un estimando inexistente en la ola fuente),
`data/corrida0/CALC-PISOS-ENUT2019-EJES-0001/` (P2), filas en `corridas.tsv` /
`replay-evidencia.tsv` (no hay corrida), `tools/pisos_ejes.py` (no se tocó), ningún
payload `enut2024*` más allá de su FD, ningún `eder2025*`, ningún cruce, el yaml del
árbitro. **Microdato abierto: ninguno** (ENUT 2019 y 2024, EDER 2011/2017, ENIF 2021/2024:
sólo FD, diccionarios RNM, descripciones de archivos y listados de miembros de ZIP).

## 4 · Verificaciones mecánicas al cierre

| qué | comando | salida |
|---|---|---|
| marcador re-derivado | `python3 tools/marcador_segmento.py --escribe` | `sin_piso=21 · cobertura_de_piso=73 · total_filas=214 · estimador_adoptado=20 · valor_anadido=0` |
| composición de `sin_piso` | lectura de `data/corrida0/marcador-segmento.tsv` | 11 `NO-CONSTRUIBLE:ENUT 2019 sin tvar_crea…` · 4 `NO-CONSTRUIBLE:P3_13 comparable no existe en ENIF 2021` · 6 `SIN-CONSUMER-EN-TABLA-DE-IDENTIDAD` (4 EDER + 2 ENIF horizonte_corto) |
| guardias del marcador | `python3 tests/test_marcador_segmento.py` | `PASA -- 10 casos` |
| test propio | `python3 tests/test_pisos_enut2019.py` | `PASA` · control negativo (categoría `mujer · 60+` → `65+` en la tabla): 3 `FALLA` (rejilla ≠ árbitro, sidecar, enlace `SIN-FILA-EN-TABLA-DE-IDENTIDAD`), exit 1; restaurada |
| sidecar | `sha256sum -c PISOS-ENUT2019-ejes-metadatos-v1_0.tsv.sha256` | `OK` |
| contadores | `python3 tools/cierre_acto.py --aplica --sin-suite` | `APLICADO: gobernanza 551->552 · L0 551->552 · tabla estado 551->552`; segunda corrida `sin cambios` |
| suite | `TZ=UTC python3 tests/check.py --baseline` | ver §5 |

## 5 · Suite en línea base

Primera corrida (`TZ=UTC timeout 1800 python3 tests/check.py --baseline`, exit 1): **ROJO — 5
FAIL nuevos**, todos propios: 3 × `T-NO-CORRIDO` (`NC-0369`/`NC-0372`/`NC-0373` con sucesor
literal `SIN-ASIGNAR` → `NC-HUÉRFANA`) y 2 × `T16` (canon declara 3 FAIL, la corrida da 6 —
los tres de arriba). Corrección: los tres sucesores se asignaron a actos/decisiones concretas
(el sucesor de `NC-0368`; mesa al fusionar; el acto que cierre `NC-0370`). `T16` no se
editó: vuelve a cuadrar solo al bajar la cuenta real a 3.

Segunda corrida (mismo comando, exit 0), salida cruda del bloque final:

```
  FAIL (3)
────────────────────────────────────────────────────────────────────────
  · T06: 2
      7 valores distintos de **Gini** en el corpus: 0.39 (1x, Confianza_y_Desconfianza_en_:165(s/f)) · 0.391 (4x, El_Clasemediero_Mexicano__Id:182(2024)) · 0.449 (1x, El_Clasemediero_Mexicano__Id:37(2016)) · 0.45 (2x, Ps
      12 valores distintos de **confianza interpersonal** en el corpus: 12 (4x, Confianza_y_Desconfianza_en_:221(2009)) · 15 (4x, Psicología__Conducta_y_Socie:3(2025)) · 16 (1x, Report_26__The_Contemporary_:161(s/f)) · 2
  · T08: 1
      7 reports sin mapa de evidencia — todo constructo suyo es DERIVADO, no LEÍDO: Humor_in_Mexican_Psychological_Life__2023-2026 · La_arquitectura_invisible_de_la_interacción_so · Mexican_Population_Genomics__2025-2026

════════════════════════════════════════════════════════════════════════
  3 FAIL · 7587 WARN
════════════════════════════════════════════════════════════════════════

────────────────────────────────────────────────────────────────────────
  LÍNEA BASE: VERDE — sin FAIL nuevos frente a tests/baseline.json (HEAD congelado 7100cd0317132b1f4513b2efdc04058fd7ae89a2)
```

Los 3 FAIL son los heredados de la línea base (`T06` ×2, `T08` ×1); `7587 WARN`, ninguno
adjudica. Tras la suite, `git status --porcelain` no muestra ningún archivo modificado fuera
de los de este acto (la suite no reescribió derivados en este árbol).

## 6 · A.8 · `tools/ya_medido.py` (una línea por regla citada; este acto no clasifica, pre-registra, carga ni sella ninguna)

```
familia.cuidado.recae_mujeres_40mas          → MEDIDA-EN: CALC-ENUT-0001, tramite.yaml
familia.cuidado.reparto_mujeres40            → NUNCA-MEDIDA   (falso negativo conocido del tool, ver feedback_ya_medido_falso_negativo_en_tasa_base; la entrada _ejes_enut2024 está SELLADA en tramite-ola5-propuesta-v0.yaml:2089)
familia.union.baja_garantia_institucional    → NUNCA-MEDIDA
familia.union.libre                          → MEDIDA-EN: CALC-EDER-0003, CALC-ENADID-0001, tramite.yaml
dinero.ahorro.volatilidad_horizonte_corto    → NUNCA-MEDIDA
dinero.ahorro.horizonte_corto                → MEDIDA-EN: CALC-ENIF-0001, tramite.yaml
```
