ESTADO: DECLARADO
ENTORNO: (sin determinar — depende del esquema que dejen E5/E6)
ENCOLADO: 2026-09-08 · ACTO GEN2-T7-CIERRE encola "E7 · ACTO GEN2-E7 · READINESS-2 DEL MARCADOR", texto de `ENCARGOS-GEN2-v1_3-readiness-primero-2026-09-07.md` {cita-ilustrativa} (adjunto por el operador y nunca guardado en el repo — cita al documento fuente, no una ruta que este acto cree), como stub declarado. Nuevo en la cola.
BITACORA:
- 2026-09-08 · DECLARADO (no `LISTO` ni `GATEADO`: el propio cuerpo dice «No se redacta ahora»). Nace de `ENCARGOS-GEN2-v1_3-readiness-primero-2026-09-07.md` {cita-ilustrativa}, D12 de E3.1: la readiness del marcador (wrapper M, corredor R/L, agregado sucesor) se atiende en E7, antes de C0-D, pero su alcance concreto depende del esquema real que dejen E5 y E6 — este archivo es solo la nota de scope, sin cabecera ejecutable todavía.

──── CUERPO VERBATIM DEL ENCARGO (A.3) · el despachador NO lo edita ────

## E7 · ACTO GEN2-E7 · READINESS-2 DEL MARCADOR — declarado, se redacta después de E6

Alcance (D12 de E3.1): wrapper M `marco vigente → cada celda → emite_celda → RESULT-M` sin `regenera_todos()` histórico; R por `payload_id` exacto + spec + ruta de P1 (envolver o adaptar `arbitra.py`, sin heurística de selección); corredor L sucesor para `L-spec-v1_2` (14 celdas) en lugar de `runner_l_cli.py`+`carga_l_v1_1.py`; agregado sucesor que consuma `RESULT-R/M/L` por celda como corrida derivada; `motor.py` y su familia fuera del camino crítico. Go/No-Go propio antes de C0-D. **No se redacta ahora**: depende del esquema real que dejen E5 y E6.

**Después:** C0-B lote 1 (specs para los 7 coeficientes ejecutables y las 4 conductas de D10, sobre `demanda-corridas.tsv`), C0-C, C0-D.
