# codex/autoridad-semantica-enif — insumo externo (worktree sucio, GEN2-LIMPIEZA-RAMAS-LOCALES-4)

Contenido sin commitear del worktree `/home/pc0/mm-autoridad-semantica-enif` (rama
`codex/autoridad-semantica-enif`), del 25/ago/2026 03:45–03:49, decisión de mesa "archivar como
insumo". Se preserva tal cual estaba, sin resolver ni limpiar.

## Archivos

- `autoridad-semantica-enif-2026-09-20-diff-trackeados.patch` — diff de los 2 archivos trackeados
  modificados (`tools/curador_registro/generar_marco.py`, `.../marco_e2_adapter.py`) contra el
  HEAD de esa rama.
- `autoridad-semantica-enif-2026-09-20-autoridad_semantica_marco.py` — script sin seguimiento
  (`tools/curador_registro/autoridad_semantica_marco.py` original).
- `autoridad-semantica-enif-2026-09-20-autoridad-semantica-marco-v1_0.jsonl` — dato sin seguimiento
  (originalmente `data/curacion-universo/autoridad-semantica-marco-v1_0.jsonl`), **1 registro**.
- `autoridad-semantica-enif-2026-09-20-autoridad-semantica-marco-v1_0.schema.json` — schema sin
  seguimiento (mismo path original).

## Hallazgo — este contenido parece SUPERADO, no rescatable sin fricción

Verificado contra `origin/main` al archivar (20/sep/2026): `main` **ya tiene**, trackeado desde
`130ee53e` (25/ago/2026), su propio `data/curacion-universo/autoridad-semantica-marco-v1_0.jsonl`
con **253 registros** (vs. el único registro de este borrador) y un `.schema.json` **byte a byte
idéntico** al de este borrador. El único registro del borrador (`autoridad_id`
`ASM-1a8049c050a32c9d2a46355b`, variable `p3_3` de ENIF 2024) **no existe con ese id** en el
archivo de `main`, pero `main` **sí tiene un registro para la misma variable** (`p3_3`, ENIF 2024)
con `autoridad_id` distinto y contenido distinto (otra fuente citada, otro `e2_record_id`) — es
decir, el pipeline de curación semántica del barrido (mencionado en `tests/check.py::t02_duplicates`)
ya volvió a curar esta misma variable de forma independiente, después de este borrador. **No se
verificó si el registro del borrador es estrictamente peor, mejor o solo distinto** — eso excede
lo que pide el archivado; se deja para quien decida si vale la pena diferenciarlos. El schema
idéntico sugiere que el contrato de datos no cambió, solo el contenido de un registro puntual.

**Conclusión operativa:** archivar esto preserva el rastro, pero no cambia la recomendación — no
hay indicio de que valga la pena reabrir/adoptar este fragmento; `main` ya avanzó por su cuenta
sobre la misma variable. Los 2 archivos trackeados modificados (`generar_marco.py`,
`marco_e2_adapter.py`) no se compararon línea a línea contra sus equivalentes actuales en `main`
— solo se archivó el diff crudo.
