# Revisión de auditoría · enoe-participacion-2024t4-0001 · CAMPOS-DENTRO

La auditoría automática marcó `CAMPOS-DENTRO: false` por el token `est`, que coincide con una columna real del archivo y no está autorizado.

**Revisión (receptora, 28/sep/2026, antes de dictaminar).** El microdato se lee una sola vez: `pd.read_csv(…/sdemt424.csv, usecols=COLUMNAS)`, línea 51. `COLUMNAS` (líneas 31–32) es idéntica, elemento por elemento, a `campos_autorizados`. `est` es el nombre de una columna interna construida desde `est_d_tri` (líneas 83 y 139–143), no una lectura.

**Veredicto:** CAMPOS-DENTRO por revisión (falso positivo de la regla de vocabulario, declarado; la regla no se ajusta).
