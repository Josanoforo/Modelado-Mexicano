ACTO restauración post-`PR #527` · FAIL absorbidos en línea base (P5)
======================================================================

`python3 tests/check.py --baseline`, corrido el 2026-09-04 al cierre de
esta restauración, contra `tests/baseline.json` (HEAD congelado
`3c5182ddbe982450067a9d476744b07229d464a2`): **VERDE — nada nuevo**.

Esta pieza no corrige ninguno de los FAIL de abajo — `tests/**` está
fuera de perímetro. Se listan tal como los reporta la suite, para que
mesa decida cuáles "se pagan" (`FP-293`).

19 FAIL, en 6 categorías:

| Test | Cuenta | Qué mide |
|---|---:|---|
| `T09` | 8 | marco importado (Hofstede/GLOBE/WVS/PDI/IDV/IVR, etc.) citado como CAUSA sin el bloque (c) de matiz/contexto |
| `T05` | 5 | constructo usado por el motor (`milpa/`) y ausente del glosario — `turnout buying`, `vote-choice`, `confianza personalizada`, `interruptor formal`, y 1 más |
| `T02` | 2 | nombre normalizado colisiona entre `AGENTS.md`/`decisiones-humanas.tsv` reales y sus copias en `forense/rescate/curador-untracked-20260807/` |
| `T06` | 2 | valores numéricos distintos para el mismo constructo en el corpus — 7 valores de Gini, 12 de confianza interpersonal |
| `T08` | 1 | 7 reports del corpus sin mapa de evidencia (todo constructo es DERIVADO, no LEÍDO) |
| `T11` | 1 | afirmación de estado con cuantificador absoluto en `corpus/reports/Psicología_del_Consumidor_Mexicano…md:16` |

Ninguno de los 19 es nuevo frente a `tests/baseline.json` — todos
estaban absorbidos ya antes de esta restauración (verificado corriendo
la misma suite antes y después de cada commit de esta pieza; el único
FAIL nuevo que apareció en el camino, `T15` por la cita "333 ADR" que
quedó desactualizada tras `ADR-335` (renumerado desde el candidato original `ADR-334` al fusionar `origin/main`/`PR #529`, que ya traía `ADR-334` para `MAESTRA38-N2`), se corrigió en el mismo commit de
cascada y no llegó a quedar absorbido).

Ver `FP-293` en `forense/firmas-pendientes.tsv`.
