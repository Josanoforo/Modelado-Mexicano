# Cierre · ACTO GEN2-TUBERIA-PARSER-FP-1 · 23/sep/2026

Encargo: `forense/encargos/2026-09-22-GEN2-TUBERIA-PARSER-FP-1.md`.
ADR: `canon/gobernanza-v1_15.md` → `ADR-260923-GEN2-TUBERIA-PARSER-FP-1-9641-01`.

## Qué se midió antes de tocar nada

- `RE_FP_ID = re.compile(r"\bFP-\d+\b")` (`tools/digesto_tramite.py:2325`)
  sobre `FP-260921-GEN2-TUBERIA-SUCESOR-1-6e60-01` → `['FP-260921']`
  (reproducido, confirma la premisa `[EJECUTADO]` del encargo).
- La premisa `[EJECUTADO]` de efecto en la vista («`--mesa` reportó *374
  (0 ABIERTA)* con 17 `ABIERTA` en el TSV») **no se reprodujo** sobre
  `ab01b3fe`: `--mesa --stdout --sin-suite` → `FP examinadas: **464** (4
  ABIERTA)`; TSV por `awk -F'\t' 'NR>1 && $6 ~ /^ABIERTA/'` → **4**; por
  `csv.DictReader` + `EC.es_abierta` (ancla `^ABIERTA(\s|$)`) → **4**.
  El criterio de «hecho» §1 sobre el CONTEO DE ESTADO ya se cumplía antes
  del parche. Lo que sí reproduce es la pérdida de CITAS (ver abajo).
- Único consumidor de `RE_FP_ID` en el archivo: `_nc_a_fila_mesa`
  (`:2416`, `fp_citadas = RE_FP_ID.findall(sucesor)`). Ningún otro regex
  del archivo usa `\d+` para NC/ADR/CALC (`grep -nE`, cero coincidencias
  fuera de `RE_FP_ID`); `RE_ENCOLADO` es de fecha, no de id.

## Impacto medido, universo declarado

Lector de CSV (`csv.DictReader`, nunca `awk` por línea física para el
conteo — §2), sobre `forense/no-corrido.tsv` (613 filas) y
`forense/firmas-pendientes.tsv` (462 filas):

| | parser viejo | parser nuevo |
|---|---|---|
| citas de `sucesor` que resuelven contra el tablero | 95 | 141 |
| filas NC cuya lista de FP citadas cambia | — | 41 |
| ids fantasma inventados (prefijo de fecha) | `FP-260921`, `FP-260922`, `FP-260923` | 0 |

En la vista renderizada `--mesa` (que aplica filtros de presentación
adicionales) el cambio visible es más chico: 2 filas (`NC-0161`,
`NC-0162`) pasan a citar `FP-260922-GEN2-FP374-RESELLO-1-dfbe-01` con su
estado, donde antes esa cita no resolvía. El resto de las 41 filas están
`CERRADA` o fuera de la selección de hoy — el defecto era real y estaba
ahí, aunque hoy mueva pocas filas visibles.

## Por qué el diff de `NC-…-6e60-01` no se aplicó a ciegas

Proponía `FP-\d{6}-GEN2(?:-[A-Z0-9]+)+-[0-9a-f]{4}-\d{2}|FP-\d{1,3}` —
la gramática de `tools/nc_por_clase.py::RE_FP`. Verificado contra el
tablero real:

```
FP-260921-MOTOR-THETA-CONGELADA-1-e8fa-01                  # sin "GEN2-"
FP-260921-GEN2-CELDA-D-PILOTO-3-COMMIT-2-3-v1_2-a6f5-01    # "v1_2" en minúscula
```

Ninguno de los dos casa con esa gramática; D-24 no exige `GEN2-` ni
mayúsculas en el rótulo. Con lector de CSV: 6 pares `(NC, FP)` que
citan cualquiera de esas dos FP habrían seguido sin resolver
(`NC-0451..454`, `NC-…-a6f5-01`, `NC-…-e8fa-02`). Se implementó D-24
literal, más ancho a propósito que `nc_por_clase.RE_FP`.

## Gramática final

```python
_RE_FP_NUEVA = r"FP-\d{6}-[A-Za-z0-9_]+(?:-[A-Za-z0-9_]+)*-[0-9a-f]{4}-\d{2}"
_RE_FP_VIEJA = r"FP-\d{1,3}"
RE_FP_ID = re.compile(rf"\b(?:{_RE_FP_NUEVA}|{_RE_FP_VIEJA})(?![\d\-A-Za-z_])")
```

Ancho `{1,3}` re-derivado sobre este árbol (no copiado): 394 ids
numéricos, ancho máximo 3, máximo `FP-409`.

## Verificación de «hecho» (§1 del encargo)

1. `findall('FP-260921-GEN2-TUBERIA-SUCESOR-1-6e60-01 FP-374')` →
   `['FP-260921-GEN2-TUBERIA-SUCESOR-1-6e60-01', 'FP-374']` — OK.
2. `--mesa --stdout --sin-suite` ABIERTA (4) == TSV ABIERTA (4) — OK,
   y ya lo era antes (premisa 1 no se reprodujo, declarado arriba).
3. `tests/test_digesto_ids_raiz.py` → 13/13 OK; huérfano, cableado por
   censo (`tools/ci_guardias.py --censo` → fila `CORRE-EN-CI`).
4. `NC-260921-GEN2-TUBERIA-SUCESOR-1-6e60-01` → `CERRADA`, con cita al
   impacto medido.

## Lo que no se tocó (perímetro, §9)

- `tools/nc_por_clase.py`, `tests/test_tuberia_ids_union.py`: AJENOS por
  nombre. `NC-…-9641-01`.
- `tools/estado_comun.py::lee_tablero` cuenta líneas físicas: la vista
  publica `FP examinadas: 464` sobre 462 filas reales (cabecera + una
  fila con salto de línea embebido en una glosa). No es el defecto de
  este encargo (el conteo de ABIERTA sí coincidía). `NC-…-9641-02`.
- `.github/workflows/verify.yml`: el encargo pedía cablear el test a
  mano citando `NC-0331`; D-21 (perímetro de cierre permanente, huérfano
  vía `ci_guardias --ejecuta-huerfanos`) manda sobre eso. No se tocó.
- `ADENDA-1` de `GEN2-TRAMITE-FIRMAS-8`: llegó adjunta a esta invocación
  pero su encargo vive en PR #1027 (rama `claude/new-session-edpgs6`,
  ya con `## CONSUMIDO`); D-17 impide un segundo escritor sobre ese
  encargo. Se devuelve a dirección sin archivar. `NC-…-9641-03`.

## Suite

`python3 tests/check.py --rapido` → VERDE. `tools/ci_guardias.py --censo`
re-derivado (177 archivos, 42 cableados, el nuevo test entra como
`CORRE-EN-CI`).
