---
description: Corre tools/arbitra.py sobre un lote de ≤4 celdas de un marco congelado, en dos commits (specs + resultados). Uso — /arbitra <ruta-marco.tsv> <columna_elegible> <id1> [id2] [id3] [id4]
argument-hint: <marco.tsv> <columna_elegible> <id...>
---

# `/arbitra` — lote de árbitro R, ciego a M

Ejecuta `tools/arbitra.py` (ENCARGO MAESTRA33-C2 ARBITRO-R-1) sobre **como
máximo 4 celdas por corrida** (D-11). El argumento es la ruta al marco
congelado, la columna de elegibilidad a filtrar (vacío = sin filtro) y de
1 a 4 ids de celda.

CIEGO: esta skill jamás abre `corridas-M/` ni `milpa/tramite.yaml`. Si en
algún punto del lote necesitas ese contenido, PARA y decláralo — no lo
abras "para confirmar".

## COMMIT-1 · congela las specs del lote

Copia verbatim (sin resumir, sin corregir) las filas del marco
correspondientes a los ids del lote a
`forense/prereg-duelo-v2/notas-arbitra/<fecha>-lote-<ids>.md`, con esta
frase de sello al final:

> Specs congeladas para este lote, copiadas verbatim del marco citado
> arriba, antes de ejecutar `tools/arbitra.py`. Ninguna se edita después
> de este commit.

Commit: `arbitra COMMIT-1: congela specs del lote <ids>`.

## COMMIT-2 · resultados

Corre:

```
python3 tools/arbitra.py <marco.tsv> <columna_elegible> <id1> <id2> ...
```

Commit lo que el script haya escrito en `corridas-R/` y, si aplicó,
las filas nuevas en `data/cola-adquisicion-v1_0.tsv`. Reporta la salida
cruda del comando (estado por celda) en el mensaje de commit o en la
nota de cierre.

Commit: `arbitra COMMIT-2: resultados del lote <ids>`.

## COMMIT-3 (solo si aplica) · una spec estaba mal

Si tras COMMIT-2 se descubre que una spec congelada en COMMIT-1 era
incorrecta, un tercer commit lo dice — nunca se reescribe COMMIT-1 ni
COMMIT-2 hacia atrás.

Commit: `arbitra COMMIT-3: corrige spec de <id>, ver COMMIT-1 <sha>`.

## Al cerrar

Lista los archivos que esta invocación abrió (para que quien audite
verifique el CIEGO). No hay compuerta de merge para este mecanismo.

---

## Actualización · CODIFICA-R-1 (P2, 31/ago/2026) — ACEPTADA

`tools/arbitra.py` ahora también sabe leer
`forense/prereg-duelo-v2/codificacion-R-v1_0.tsv` (la tabla de codificación
binaria + diseño muestral que ARBITRO-R-1/P3 encontró ausente de todo
marco) y, con ella, calcular R de verdad para una celda — ya no solo
declarar `NO-EJECUTABLE-SIN-CODIFICACION`. Reusa `estima()`/`csv_zip()`/
`dbf_zip()` de `corridas-R/correr-R.py` (no reimplementa el cálculo).

**Regresión ejecutada** (`python3 tools/arbitra.py --regresion DIN-11
SFT-04 TIC-08`, contra `corridas-R/` real, sin escribir nada):

| celda  | R nuevo == existente | EE_R | n_efectivo | n_estratos | n_upm_total |
|--------|:---:|:---:|:---:|:---:|:---:|
| DIN-11 | ✅ 0.4583913965555015 | ✅ | ✅ 12446 | ✅ 182 | ✅ 1908 |
| SFT-04 | ✅ 0.0604055335123943 | ✅ | ✅ 10103 | ✅ 128 | ✅ 4555 |
| TIC-08 | ✅ 0.9044714694763597 | ✅ | ✅ 47240 | ✅ 437 | ✅ 8741 |

Las tres coinciden exacto (comparación de flotantes con tolerancia
1e-9, en la práctica bit-idénticas). **Veredicto: ACEPTADA** — resuelve el
PARO de ARBITRO-R-1/P3 para estas tres celdas. Detalle completo:
`forense/notas/2026-08-31-codifica-r-1-p2-regresion.md`.

**Límite declarado de este modo** (no oculto): `universo_filtro` en la
tabla es prosa, no código — el nuevo mecanismo NO aplica ningún filtro de
universo más allá de la codificación binaria. Correcto para celdas donde
la tabla ya es el universo (las 3 de arriba); para una celda que sí
necesite filtro real (p.ej. `DIN-05`: `TLOC=='4'`) o cuya `tabla` declare
un `join` (`DIN-03`/`TIC-01`/`TIC-12`), el mecanismo se abstiene
explícitamente o produciría un número distinto que la propia regresión
atraparía como NO-COINCIDE — no se generalizó el join/filtro en este acto
(fuera de perímetro de CODIFICA-R-1).
