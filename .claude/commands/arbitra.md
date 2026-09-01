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
