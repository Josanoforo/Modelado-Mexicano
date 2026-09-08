ESTADO: EJECUTADO
ENTORNO: NUBE
ENCOLADO: 2026-09-07 · ACTO GEN2-T7 · v1.1 — FP-339 DECIDIDA · COMPUERTAS CORREGIDAS · PLAN ENMENDADO. Texto tomado verbatim de `ENCARGOS-GEN2-v1_2-con-E3-1-2026-09-07.md` (adjuntado por el operador), sección "## TRÁMITE-7 · ACTO GEN2-T7 · v1.1"; E0 nunca lo encoló como archivo propio en `forense/encargos/` — este archivo es el 0-bis A.3 tardío que lo formaliza.
BITACORA:
- 2026-09-08 · EJECUTADO. TRÁMITE-7 corrió en esta misma sesión/rama (`claude/tramite-7-decisiones-k7xvyv`) en el commit `fc63f66` (piezas D9/D10, FP-339, `decisiones.tsv`, endurecimiento de compuertas de E5/E6 a v1.2, enmienda del plan y de `tools/limpia_arbol.py`), con un fix posterior de T27 en `4f4bee6` (`decisiones.tsv` registrado en `INFRAESTRUCTURA-v1_0`). Este archivo es el 0-bis A.3 tardío de `ACTO GEN2-T7-CIERRE`, que archiva verbatim el encargo original que E0 no había encolado y deja constancia formal de qué se ejecutó.

──── CUERPO VERBATIM DEL ENCARGO (A.3) · el despachador NO lo edita ────

## TRÁMITE-7 · ACTO GEN2-T7 · v1.1 — FP-339 DECIDIDA · COMPUERTAS CORREGIDAS · PLAN ENMENDADO

Cabecera: **NUBE** · **Sonnet** · COMPUERTA: ninguna. NO se lanza en UBUNTU. Corre en paralelo con E4; **antes** de E3.1 (los dos editan `tools/corrida0.py`).
Decisiones que propaga (firmadas por el merge): **D9 · FP-339 (1–3)**: para `TRA-M-02/03/07` el JSON `__v1_3` es el vivo (marco v1.3) y `M-<id>.json` es histórico. **D10 · FP-339 (4–7)**: `dinero.ahorro.tiene_ahorros` ×2 y `familia.apoyo.recibe_dinero_familiares` ×2 son `SIN-RECETA` por decisión: no se reconstruyen; van a spec nueva en el primer lote de C0-B (alimentan las celdas DIN y FAM del marcador). FP-339 → `FIRMADA (T7)`.
Piezas: (1) `data/corrida0/decisiones.tsv` (nuevo; **se edita a mano, con firma**: `objeto · decision · fuente · fecha`) con las siete filas; `cmd_demanda` lo lee para que `demanda-*.tsv` reflejen `M_vivo=__v1_3` y `receta_legacy=SIN-RECETA (FP-339)`; test en `tests/test_corrida0.py`; re-derivar los dos TSV y pegar el diff (solo esas filas). (2) En `forense/encargos/cola/2026-09-07-GEN2-E5-…md` y `-E6-…md`: sustituir por el texto de E5/E6 v1.2 de este documento (verbatim), cuyas compuertas usan `def cmd_<sub>` y `git show origin/main:<ruta>`; registrar en `hallazgos.md` la lección de E3: «una compuerta cuyo comando no puede pasar nunca es peor que ninguna». Encolar E3.1 (`2026-09-07-GEN2-E3-1-ENDURECE-CALC.md`, estado `LISTO-` tras este merge). (3) `PLAN-FINAL-GEN2-v2_0` en `forense/notas/`: enmienda in situ fechada en §6 C-2 (GitHub ya borra ramas al fusionar; verificado por E1 sobre 598 PR) y §6 C-1 (`gh pr list --limit 500` trunca en silencio; usar 1000 o paginar); `tools/limpia_arbol.py`: si consulta PRs, `--limit 1000` y aviso si el mínimo devuelto no es 1. (4) `canon/registro-rotulos.tsv`: `decisiones.tsv` como artefacto de mesa (no derivado); `historico/` si E4 no lo censó antes.
Perímetro: `data/corrida0/decisiones.tsv` · `tools/corrida0.py` (solo `cmd_demanda`) · `tests/test_corrida0.py` · `data/corrida0/demanda-*.tsv` (re-derivados) · `forense/encargos/cola/` (E5, E6 reemplazados; E3.1 nuevo) · `forense/notas/…PLAN-FINAL-GEN2-v2_0…md` (enmienda fechada) · `tools/limpia_arbol.py` · `forense/hallazgos.md` · `forense/firmas-pendientes.tsv` (FP-339, recibo) · `canon/registro-rotulos.tsv` · cascada. Si te encuentras escribiendo fuera de esta lista, PARA.
Contador: cero; `fp_abiertas` −1 (FP-339).

## NO-CORRIDO / RESERVAS

- Pieza 4 (`#598`) retirada por mesa, que la fusionó a mano: el digesto de TRÁMITE del 7/sep no requirió automatización de este acto de cierre.
- `tools/limpia_arbol.py` no invoca `gh pr list` ni ninguna consulta de PRs — es de solo lectura sobre git local (`git worktree list`, `git for-each-ref` + `git merge-base --is-ancestor`, `git rev-list --count`), verificado leyendo el archivo completo. No hay nada que ajustar a `--limit 1000`; se deja constancia explícita y el archivo no se toca en `GEN2-T7-CIERRE`.
