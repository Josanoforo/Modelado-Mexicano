# ENCARGO · FUSION-PUERTAS — fusionar UNIVERSO-MINIMO-FUENTE y universo-puertas en una sola tabla

**SHA de redacción:** `93a4dd9` (`origin/main`, tras `ADR-100`/`ADR-101`, ACTO MESA-18AGO, 18/ago/2026)
**Entorno asignado:** **NUBE** (`cloud_default`, repo-only) — fusión de dos archivos ya en el repo, sin microdato.
**Estado:** VIVO — **DISPARADOR-B** de `FP-26` (`ADR-101(h)`), mismo gate que `FP10-PRECEDENCIA`: espera el cierre de la fase semántica de `BARRIDO-2`.
**Origen:** `FP-12`, firmada-condicional `ADR-91` (`PR #246`) — misma firma que `FP-10`: *"Al cierre de BARRIDO-2, un acto único adjudica FP-10 y FP-12: SUPERADAS por los productos del barrido si los cubren, o ejecución de fusión + diff si no."* Regla de fondo: `ADR-79(g)`, firma de mesa *"fusionemos"*.

## Verificación de existencia (A.8), contestada por quien escribe

```
data/UNIVERSO-MINIMO-FUENTE-v1_0.md     EXISTE (sellado ADR-69, universo mínimo de búsqueda por fuente)
data/universo-puertas-2026-08-14.tsv    EXISTE (vigente al 18/ago; ADQ-15 lo actualiza si corre antes)
solapa de columnas/filas                A DERIVAR al lanzarse -- no asumir que las dos tablas
                                         describen exactamente las mismas fuentes; el ADR-69 es
                                         universo MÍNIMO (requisito de NO-ENCONTRADO), universo-
                                         puertas es el resultado material del sondeo -- pueden
                                         diferir en cobertura, no solo en formato
```

## Perímetro

ESCRIBE: tabla fusionada nueva (nombre a derivar, p. ej. `data/universo-fuentes-v1_0.md` o `.tsv`, según cuál de las dos formas — Markdown de `UNIVERSO-MINIMO-FUENTE` o TSV de `universo-puertas` — retiene mejor ambos contratos; decisión declarada en la nota, no heredada) · `data/UNIVERSO-MINIMO-FUENTE-v1_0.md` y `data/universo-puertas-*.tsv` (marcados `SUPERADO POR <tabla nueva>`, no borrados — mismo criterio que `M-APERTURA`/`ADR-95`) · nota del acto. NO ESCRIBE: `canon/`, `tests/`, `milpa/`.

## Tarea

1. Al cierre de la fase semántica de `BARRIDO-2`, releer ambas tablas contra el universo nuevo.
2. Si los productos del barrido ya cubren la fusión (misma cobertura, sin pérdida de ninguna fila de ninguna de las dos): `FP-12` → `FIRMADA` por superación.
3. Si no: ejecutar la fusión declarada — una sola tabla, con `sha256` de cada tabla origen citado y verificación de que ninguna fila de ninguna de las dos se perdió (diff fila por fila, no confianza en el conteo).

## Cierre

Tabla fusionada (o superación declarada) · `FP-12` con veredicto y evidencia · `tests/check.py --baseline` VERDE · línea en `hallazgos.md` · encargo `CONSUMIDO`.
