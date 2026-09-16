# ACTO GEN2-CAJA-RESIDUAL-1 · LOTE D-11 CHICO — CIERRA NC-0181 Y NC-0126

**SHA de redacción:** `2f5cffe` (`origin/main`, merge de PR #768, re-derivado al abrir el 15/sep/2026 — el encargo llegó pegado en el mensaje de lanzamiento, sin SHA propio)
**Entorno asignado:** CAJA (Ubuntu/WSL2, corpus montado) — el encargo lo dice en su primera palabra
**Modelo sugerido por el encargo:** Sonnet — la sesión que lo ejecuta corre en Opus 5; se declara aquí y no se disfraza
**Rama:** `acto/gen2-caja-residual-1`
**Estado:** CONSUMIDO (PR #772)
**Compuerta:** ninguna declarada en el texto

## ENCARGO (verbatim, tal como se lanzó)

1 · CAJA — ACTO GEN2-CAJA-RESIDUAL-1 (Sonnet, lote D-11 chico; caja quedó libre): P1 = NC-0181 — resolver el contexto de CALC-B-0001 con corpus montado y asentar replay-evidencia para que los AVISOS dejen de disparar (SANEA lo dejó ruteado aquí, verbatim en su fila). P2 = NC-0126 — verificar P4_10 contra el archivo real, no el descriptor (A.15: los mapas de códigos se verifican por archivo); si de verdad está colapsada, declarar el corte acotado con su universo y cerrar. Cero mediciones nuevas, dicho sin disfraz; apaga ruido de suite y cierra dos colas.

## VERIFICACIÓN DE EXISTENCIA (A.8, contestada al abrir, contra `2f5cffe`)

- `forense/no-corrido.tsv` fila `NC-0181` EXISTE, `estado = ABIERTA`, sucesor = «CAJA (unico entorno que puede resolver contexto de CALC-B-0001 con corpus montado)» — coincide con lo que el encargo dice que SANEA dejó ruteado.
- `forense/no-corrido.tsv` fila `NC-0126` EXISTE, `estado = ABIERTA`, razón `NO-VERIFICABLE-AQUI`, sucesor `SIN-ASIGNAR`, pieza SEMANTICA (P4_10 = 1 colapsada según el descriptor).
- `forense/replay-evidencia.tsv` línea 24, `CALC-B-0001`: `resultado_replay = REPRODUCE`, `contexto_replay = IDENTICO`, procedencia `HEREDADO-DEL-REGISTRO-PUBLICADO` — el asiento que NC-0181 declara desfasado. Líneas 32-33 (`CALC-MOTOR-celdas-semilla`, `-v2`) ya dicen `DISTINTO` (SANEA, 15/sep).
- `data/raw` enlazada a `/home/pc0/mm-corpus/raw` (worktree nuevo; `tools/entorno.py` reporta `corpus=SI(examinados=413)`).

## NO-CORRIDO / RESERVAS

| qué | por qué | impacto | sucesor |
|---|---|---|---|
| «(Sonnet, lote D-11 chico; …)» — el modelo que el encargo sugiere para la sesión | DECISIÓN-DE-MESA-PENDIENTE — la sesión que tomó el encargo corre en Opus 5 y no puede cambiar de modelo; se ejecutó igual porque el lote es mecánico (verify, lectura de archivo, asientos con cita) y la asignación material del encargo —CAJA con corpus— sí se cumplió. Se declara como desviación de lo pedido, no como error de contenido | Ninguno sobre contadores: cero mediciones en ambos casos; ambas colas cerradas con la evidencia que el encargo pedía. Sin fila `NC` nueva (mismo criterio que la fila «contador» de `GEN2-SANEA-REGISTRO-Y-RESCATE`: reserva sin sucesor ni impacto no abre cola) | Ninguno — si mesa quiere que los lotes D-11 chicos corran en Sonnet, es una instrucción de despacho, no una pieza pendiente |

## CONSUMIDO

PR [#772](https://github.com/Josanoforo/Modelado-Mexicano/pull/772), rama `acto/gen2-caja-residual-1`, abierto el 15/sep/2026 contra `main` — ejecutado por `ACTO GEN2-CAJA-RESIDUAL-1` (ADR-508; nota `forense/notas/2026-09-15-GEN2-CAJA-RESIDUAL-1-cierre.md`). El merge es de mesa.
