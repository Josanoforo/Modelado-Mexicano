# Revisión de auditoría · enadid-cola-2018-0001 · CAMPOS-DENTRO

La auditoría automática (`compara_vc1.py`) marcó `CAMPOS-DENTRO: false` por dos tokens del código, `edad` y `upm`, que coinciden con nombres de columnas reales de algún archivo del paquete y no están autorizados.

**Revisión (receptora, 28/sep/2026, antes de dictaminar).** El código lee microdato en un solo punto: `lee_csv(nombre, cols)` → `pd.read_csv(ruta, usecols=cols, …)`, líneas 33–37. Las tres listas que recibe (`COLS_MUJ`, `COLS_SDEM`, `COLS_MIG`, líneas 26–28) son idénticas, elemento por elemento, a `campos_autorizados` del allowlist. `edad` y `upm` aparecen como nombres de columnas internas del DataFrame derivadas de `edad_muj` y `upm_dis` (líneas 145–146 y 185). No se leen del archivo.

**Veredicto:** CAMPOS-DENTRO por revisión. La regla automática es más estricta que la de `catalogo-1-lote3/audita_residuales.py` (esa solo mira tokens con forma de reactivo, y `edad`/`upm` no la tienen); el falso positivo se declara, no se ajusta la regla.
