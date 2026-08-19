# ENCARGO · FP10-PRECEDENCIA — adjudicar FP-10 (precedencia de pares en universo-puertas)

**SHA de redacción:** `93a4dd9` (`origin/main`, tras `ADR-100`/`ADR-101`, ACTO MESA-18AGO, 18/ago/2026)
**Entorno asignado:** **NUBE** (`cloud_default`, repo-only) para la adjudicación por lectura; si el resultado exige ejecutar fusión + diff sobre `data/`, ese commit corre en el mismo acto si el entorno lo permite (son archivos versionados del repo, no microdato).
**Estado:** VIVO — **DISPARADOR-B** de `FP-26` (`ADR-101(h)`): consume productos semánticos del barrido, que hoy no existen (`ADR-98(f)/(g)`, `W0` sin correr, durables de `data/curacion-universo/` no regenerables). No lanzar antes de que la fase semántica de `BARRIDO-2` cierre.
**Origen:** `FP-10`, firmada-condicional `ADR-91` (`PR #246`) — *"Al cierre de BARRIDO-2, un acto único adjudica FP-10 y FP-12: SUPERADAS por los productos del barrido si los cubren, o ejecución de fusión + diff si no. Nada se toca antes."*

## Verificación de existencia (A.8), contestada por quien escribe

```
regla sellada (Regla 1/Regla 2):    canon/gobernanza-v1_15.md (ADR-76(e))                     EXISTE
diff pendiente, 16 pares:           PROPUESTA-reconciliacion-universo-puertas.md               A VERIFICAR
                                     (re-confirmar que sigue vigente, ACTO SANEA-MAPEO ya la
                                     reconfirmó sin ejecutar el 14/ago)
productos semánticos del barrido:   data/curacion-universo/ (durables) -- HOY NO REGENERABLES,
                                     gate material en rojo (ADR-98(f)), W0 sin correr           NO SATISFECHO
                                     -- este encargo NO se lanza mientras esto siga así
```

## Perímetro

ESCRIBE (al lanzarse, no antes): `data/universo-puertas-2026-08-14.tsv` (o el vigente al momento) · `data/UNIVERSO-MINIMO-FUENTE-v1_0.md`, si la fusión con `FP-12` ya corrió · nota del acto con el diff de los 16 pares, comando por comando. NO ESCRIBE: `canon/`, `tests/`, `milpa/`.

## Tarea

1. Al cierre de la fase semántica de `BARRIDO-2` (verificar: `data/curacion-universo/` con productos durables regenerados, gate material en verde), releer `PROPUESTA-reconciliacion-universo-puertas.md` y comparar sus 16 pares contradictorios contra el universo nuevo.
2. Si el universo nuevo ya resuelve las 16 contradicciones (mismo criterio, misma fuente, una sola fila): `FP-10` → `FIRMADA` por superación, sin ejecutar el diff a mano.
3. Si no: ejecutar la fusión + diff declarado en la propuesta, incluida la fusión de `MassMobilization` que la fila nombra.

## Cierre

`FP-10` con veredicto (superada o ejecutada) y evidencia · `tests/check.py --baseline` VERDE · línea en `hallazgos.md` · encargo `CONSUMIDO`.

---

## CONSUMIDO — 19/ago/2026, `ACTO FP10-PRECEDENCIA`

Precondición reverificada (no heredada): gate material 672/672 (`ADR-103`, `PR #260`) y fase semántica de `BARRIDO-2` cerrada (`ADR-108`/`ADR-109`, `ACTO B2-SEMANTICO`, `PR #268`), ambos fusionados. Las 16 fuentes de `PROPUESTA-reconciliacion-universo-puertas.md` §2 seguían sin resolver en `data/universo-puertas-2026-08-14.tsv` — **no superada**, se ejecutó el diff: 16 filas `gap_mapeo_map_b` retiradas (122→106 filas, `gap_mapeo_map_b` 61→45, 0 duplicados, 0 filas ajenas tocadas). `FP-10` → `FIRMADA` (ejecutada). `FP-12`/`FUSION-PUERTAS` verificada sin tocar, sin colisión de perímetro. `ADR-114` sellado. `python3 tests/check.py --baseline`: 21 FAIL · 118 WARN, LÍNEA BASE VERDE, sin `--freeze`. Detalle: `forense/notas/2026-08-19-fp10-precedencia.md`. Contadores de medición sobre México movidos: cero.
