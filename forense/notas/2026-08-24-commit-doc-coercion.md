# Nota · `ACTO COMMIT-DOC-COERCION` · 24/ago/2026

Comando a comando, entorno **NUBE** (`cloud_default`), modelo Sonnet.

## Arranque

```
git status            # limpio, rama claude/coercion-adopcion-commit-doc-zi6v1p
git log -1            # 8791bcf, merge de PR #318 (SELLA-AGO24-D), ya fusionado
git branch -a
```

`data/raw`: no aplica, declarado. Sin red ni microdato — sonda saltada, declarado.

## Verificación de existencia

`forense/coercion-adopcion-espec-operativa-v0_1.md` existía, rotulado `PROPUESTA·PARCIAL` (`ACTO EMISOR-M-2`/`ADR-146`). `FP-113` existía `ABIERTA` en `forense/firmas-pendientes.tsv:114`, declarando que el íntegro no estaba en el repo (verificado por `EMISOR-M-2`: 607 `.md`, 0 hits).

## El adjunto

```
sha256sum "/root/.claude/uploads/.../2c311022-COERCIONYADOPCIONrediseno20260820.md"
# f77d705eac4b9f5eadd846e96503c4add5ef798b779de52e3e4f8080c107f5cb
```

Copiado a `forense/COERCION-Y-ADOPCION-rediseno-2026-08-20.md`. Única edición permitida: una cabecera nueva de una línea insertada tras el título —

```
**PROPUESTA (no sellada) — adjunto de mesa 24/ago, sha256 f77d705eac4b9f5eadd846e96503c4add5ef798b779de52e3e4f8080c107f5cb**
```

Verificado con `diff` contra el archivo original sin esa línea: cero diferencias en el resto del cuerpo (119 líneas del original, todas idénticas salvo el desplazamiento por la inserción).

## Parcial

`forense/coercion-adopcion-espec-operativa-v0_1.md` recibe una línea de cabecera, fechada: *«SUPERADA por el íntegro — ver `forense/COERCION-Y-ADOPCION-rediseno-2026-08-20.md`, 24/ago/2026.»* No se borra. Ninguna cita `{cita-ilustrativa}` existente que apunte a ella se toca.

## `FP-113`

`forense/firmas-pendientes.tsv` columna `estado`: `ABIERTA` → `FIRMADA`; `firmada_en`: `ADR-151, documento integro commiteado byte-identico, 24/ago/2026`; `ejecutada_en`: `ADR-151`.

## Cascada de ADR

```
grep -oE '^\*\*ADR-[0-9]+' canon/gobernanza-v1_15.md | sort -t- -k2 -n -u | tail -1
# ADR-150 — máximo sobre el árbol al arrancar (origin/main = 8791bcf), único, sin huecos → candidatea ADR-151
```

`canon/gobernanza-v1_15.md`: cabecera (150→151) y párrafo del ADR-151. `canon/estado-programa-v1_10.md`: `:27` y `:103` recifrados (150→151).

## Suite

Primera corrida, tras commitear el documento y cerrar `FP-113`, antes de tocar `tests/`:

```
python3 tests/check.py --baseline
# ROJO — T22 nuevo: forense/COERCION-Y-ADOPCION-rediseno-2026-08-20.md,
# forense/encargos/2026-08-24-COMMIT-DOC-COERCION.md,
# forense/notas/2026-08-24-commit-doc-coercion.md
```

`_T22_MARCADOR_PENDIENTE` (`PROPUESTA.*mesa`) dispara por la cabecera nueva que el propio acto rotula, verbatim, en el documento que commitea: "PROPUESTA (no sellada) — adjunto de mesa 24/ago". Autocaptura, no una decisión nueva sin registrar — es exactamente lo que `FP-113` ya rastreaba y este mismo acto cierra. Mismo patrón que toda `_T22_ARCHIVOS_CONOCIDOS` ya documenta (`ACTO TABLERO-FIRMAS`, `CI-CATEGORIA`, `NOTAS-P3`…). Se suman los tres archivos a esa lista.

Colisión adicional: el encargo `2026-08-24-COMMIT-DOC-COERCION.md` y esta nota `2026-08-24-commit-doc-coercion.md` normalizan al mismo nombre (`T02`) — el encargo se renombra a `forense/encargos/2026-08-24-ACTO-COMMIT-DOC-COERCION.md` para desambiguar.

Tras ambos ajustes, y tras recifrar `estado-programa-v1_10.md:207,299` (150→151 ADR, `150 ADR` marcado `{cita-historica}`; 149→148 WARN vigente):

```
python3 tests/check.py --baseline
# 19 FAIL · 148 WARN
# LÍNEA BASE: VERDE — nada nuevo frente a tests/baseline.json
```

`--freeze` NO invocado.

## Perímetro

Tocado lo que el encargo lista: `forense/COERCION-Y-ADOPCION-rediseno-2026-08-20.md` (nuevo), `forense/coercion-adopcion-espec-operativa-v0_1.md` (una línea de cabecera), `forense/firmas-pendientes.tsv` (fila `FP-113`), `canon/gobernanza-v1_15.md`, `canon/estado-programa-v1_10.md`, esta nota, y el encargo archivado (`forense/encargos/2026-08-24-ACTO-COMMIT-DOC-COERCION.md`). **Extensión mecánica, declarada:** `tests/check.py`, tres líneas nuevas en `_T22_ARCHIVOS_CONOCIDOS` — mismo precedente de perímetro corto que `ADR-147(c)`/`ADR-149(f)` ya fijaron, sin el ajuste la suite quedaba roja por un defecto que el encargo no podía anticipar en su lista. No toca `milpa/`, `corpus/`, `data/`, ni `canon/modelo-decision-v4_0.md`.
