ACTO MAESTRA31-E8 · LOS-388 — COMMIT-1: congela la escala de valor

27/ago/2026, entorno UBUNTU, worktree `/home/pc0/mm-maestra31-e8-los-388` sobre `origin/main` = `9578ee6` (incluye el merge de `PR #387`/`ACTO MAESTRA31-E6 · DICCIONARIOS-FD`, que libera la caja UBUNTU — el gate del encargo). `E7 · ETIQUETA` (FP-174, NUBE) no ha fusionado a esta hora: no existe rama ni commit con "etiqueta" en `origin/main`, verificado por `git log origin/main --oneline --all | grep -i etiqueta` (vacío). Este acto usa `data/inventario-reactivos-v1_0.tsv` **v1_0**, declarado.

## Paso 1 — partición re-derivada (no heredada del .meta)

Universo recorrido con `tools/inventario_reactivos.py::enumerar_universo()` (lectura pura, sin invocar `inspect_one`; no es "re-correr el inventario", es listar el árbol que el propio módulo ya expone como función pública): **720** payloads, excluyendo el ciclo `data/raw/raw`.

`data/inventario-reactivos-v1_0.tsv`: **316** `payload_id` distintos con ≥1 fila (columna `variable_id` no vacía) — el conjunto OK.

`no_extraido` (suffix fuera de `FORMATOS_CON_CAMPOS ∪ FORMATOS_SIN_CAMPOS`): **16** — `.dta`×8, `.2a`×6, `.gz`×1, `.tab`×1.

`sin_campos` = universo − OK − no_extraido = 720 − 316 − 16 = **388**.

**316 + 388 + 16 = 720.** Suma correcta, sin brecha.

Caso de control: `BD_ENCUCI2020_dbf.zip` aparece en el universo y tiene **458** filas en el TSV (`grep -c "^BD_ENCUCI2020_dbf.zip" data/inventario-reactivos-v1_0.tsv` → 458) → cae en OK, como el encargo predijo.

Nota de método sobre honestidad procedimental: para construir la partición de causas de Q1 (paso siguiente) fue necesario inspeccionar la extensión, el tamaño y —solo para `.zip`/`.xlsx`— el listado de miembros de cada uno de los 404 payloads no-OK (permitido explícitamente por REGLA DE TOPE punto 2). Esa inspección reveló, de forma incidental y antes de escribir este COMMIT-1, que **algunos** de los 404 sí tienen coincidencia de nombre en fuentes externas (se vio de pasada al construir la búsqueda de cruce, no se contó ni se ordenó). Este COMMIT-1 declara la regla de puntaje **sin haber mirado qué payload individual queda arriba o abajo del ranking** — la regla se deriva del principio que el propio encargo ya declaró como prioridad (Q2: "un payload ya explotado... es la señal más fuerte"), no de un ranking ya visto. Se documenta esta secuencia en vez de ocultarla porque ocultarla sería peor que declararla.

## Escala de valor — orden lexicográfico, congelado

Cuatro señales, en el orden de peso decreciente que sigue (de mayor a menor):

**1. `hitoD` (booleano).** El payload aparece citado por nombre en `forense/hitoD-preregistro-v2_0.md`. Máximo peso: es el único documento del programa cuyas citas están atadas a una regla `R#.#` con falsador pre-registrado ante mesa — la forma más fuerte de "esto importa" que existe en este repo.

**2. `n_notas` (entero, ≥0).** Número de archivos distintos de `forense/notas/*.md` que mencionan el payload por nombre (basename o ruta relativa). Evidencia de que uno o más actos ya lo manejaron por escrito, aunque no haya llegado al pre-registro formal.

**3. `manifiesto` (categórico, tres valores).** Estado de `usado_para` en `data/manifiesto.yaml`, emparejado por `archivo` (ruta relativa completa o basename) contra el `payload_id`:
   - `SEÑAL_DE_USO` — el texto de `usado_para` describe una explotación real (cita un encargo/hito/confirmación de esquema), sin marcador negativo ("no abierto", "aún no explotado", "solo hasheado", etc.) o con marcador negativo pero corregido explícitamente en el mismo texto ("corregido", "usaron", "confirmar", "sustituto").
   - `SIN_ENTRADA` / `ENTRADA_SIN_USADO_PARA` — no hay fila en el manifiesto para ese archivo, o la hay sin texto en `usado_para`. Neutral: no es señal a favor ni en contra.
   - `DECLARADO_NO_USADO` — el texto trae un marcador negativo sin corrección explícita en el mismo campo.
   Puesto en tercer lugar, no primero, porque `usado_para` es una fuente conocida por quedarse obsoleta (ver `feedback_manifiesto_usado_para_stale`, sesiones previas de este programa: el campo no se actualiza cuando una sesión posterior sí abre el archivo). Se usa como señal débil, nunca como negativo fuerte.

**4. `milpa` (booleano).** El payload aparece citado por nombre en `milpa/procedencia.yaml` o `milpa/tramite.yaml`. Declarada por completitud —el encargo la pide expresamente— aunque el resultado empírico (ver hallazgo abajo) es 0/404: ninguno de los 404 aparece en ninguno de los dos archivos. Se deja en la escala igual, para que quede en el registro que se buscó y no se encontró, no que se omitió.

**Orden final:** `(hitoD desc, n_notas desc, manifiesto desc [SEÑAL_DE_USO > SIN_ENTRADA/ENTRADA_SIN_USADO_PARA > DECLARADO_NO_USADO], milpa desc, payload_id asc)`.

**Empate.** Dos o más payloads que coinciden en las primeras cuatro señales se desempatan por orden alfabético ascendente de `payload_id` — determinista, sin discrecionalidad de quien ejecuta el acto.

## B-bis — qué significaría cada resultado

**Si ninguno de los 404 tuviera señal en ninguna de las cuatro fuentes:** sería el resultado excelente. Diría que el extractor, al fallar en silencio, dejó fuera exactamente el contenido que ningún acto del programa ha necesitado tocar todavía — coincidencia entre "no rinde variables" y "no se usa" que valida el statu quo (no escribir extractores nuevos con urgencia).

**Si muchos tienen señal (sobre todo en `hitoD` o `n_notas`, las dos fuentes fuertes):** sería la prueba de que el 54% sin rendimiento no es basura — incluye contenido que el programa ya demostró que le importa, simplemente en un formato que la herramienta actual no sabe leer. Ese es el caso que convierte "faltan extractores" en una recomendación con números detrás, no una intuición.

## Frase de sello

«El primer resultado que produzca este procedimiento es el que se reporta.»

Congelado aquí. El siguiente commit (COMMIT-2) aplica esta regla mecánicamente sobre los 404 payloads y no se vuelve a tocar la escala después de ver la tabla.
