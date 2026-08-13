# GDELT-UCDP-RECON — caracterización, no descarga

**Acto:** ENCARGO B · GDELT-UCDP-RECON (relanzado) · **Cierra:** D9 · **Entorno:** CAJA con red, NO nube · **Base:** `origin/main = 959006a` (post-PR #206, ENASIC-SPLIT, coincide con el declarado por el encargo, no hizo falta refrescar) · **Worktree:** `~/mm-gdelt-ucdp-recon`, rama `gu/gdelt-ucdp-recon`.

## §0 · ARRANQUE — verificado, no supuesto

- `$CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE` → vacío (confirma `caja`, no `nube`).
- `grep -rliE "multi.?agent|agent.?fleet|orchestrat|subagent" tools/ tests/` → **vacío**. No se encontró "infraestructura de agentes" declarada en este repo. Se procede con `curl` directo, como instruye el encargo para este caso.
- `data/raw` → symlink nuevo a `/home/pc0/mm-corpus/raw` (`ln -s`, verificado con `readlink -f`, 258 entradas visibles). `data/raices.local.yaml` copiado del clon base (gitignorado, no lo hereda un worktree nuevo).
- `curl -s -o /dev/null -w "%{http_code}\n" --max-time 10 https://www.gdeltproject.org/data.html` → **200**, sin override de sandbox necesario (a diferencia de lo medido por SONDA-1 el 8/ago para otros dominios — este host respondió directo). GET, nunca HEAD, en todos los sondeos de este acto.
- Filas de acceso ya sondeadas por VERIFICA-PUERTAS (`data/acceso-puertas-2026-08-13.tsv`, verificado contra el archivo real, no solo contra el texto pegado del encargo): `GDELT_RawDataFiles` y `UCDP_Downloads_GED`, ambas `206`/`AGENTE`/`N17,N27`. No se repite el sondeo de acceso — este acto sondea **estructura**, que es otra cosa.
- Las dos filas duplicadas del puntero (`GDELT`/`UCDP`, `gap_mapeo_map_b`, `NO_PROBADO`) no se tocan — regla de precedencia de RECONCILIA-PUERTAS: gana la fila con sondeo de portal.

## §1 · COMMIT 1 — techo y criterio, congelados antes de bajar nada

**Techo de descarga por fuente: ≤500 MB.** Si caracterizar exige más, este acto para y reporta cuánto haría falta — no se negocia en vuelo.

**Archivo mínimo que caracteriza la estructura, nombrado antes de bajarlo:**
- **GDELT:** el índice/manifiesto de archivos de la portada de datos (se buscará un listado tipo "master file list" bajo `data.gdeltproject.org`, categoría "índice/manifiesto" del propio encargo) — si existe, es el artefacto mínimo; si no, el archivo diario más pequeño que ese índice referencie ("un solo día de datos").
- **UCDP:** la página de descargas ya declara un listado de datasets versionados (GED Global) y, por convención de UCDP, un codebook — el codebook (PDF, típicamente pequeño) es el candidato de "manifiesto/codebook"; si no basta para ver la estructura de columnas, el archivo de datos más pequeño ofrecido ahí.

**Mecanismo de recorte candidato, escrito antes de mirar el contenido (no la portada) — de conocimiento general sobre estos dos proyectos, declarado como hipótesis a verificar, no como hecho:**
- **GDELT:** se espera **COLUMNA** — registros a nivel de evento con campos de código de país del actor/ubicación geográfica (convención FIPS en GDELT), no separación por archivo ni por endpoint en el nivel "Raw Data Files" (que la propia portada organiza por fecha, no por país). Costo esperado: alto si es solo columna — hay que bajar y filtrar, no solo pedir un recorte ya hecho.
- **UCDP:** se espera **COLUMNA** también — evento/díada/país-año con un código de país (convención Gleditsch-Ward) por fila; candidato secundario a verificar: **archivo aparte**, si la página de descargas ofrece extractos regionales o por país ya recortados (no asumido, se revisa la página real en Commit 2 antes de descartarlo).

**Veredicto, criterio cerrado (idéntico para ambas fuentes):**
- **RECORTE-VIABLE** — el mecanismo existe y se puede ejercer con lo que ya hay en este repo (p. ej. `awk`/`grep` sobre una columna de país).
- **VIABLE-CON-PARSER-NUEVO** — el mecanismo existe pero exige código que no está (p. ej. geocodificación lat/lon → país, sin campo de país directo).
- **NO-SEPARABLE** — no hay forma de aislar México sin bajar todo.

**Pre-registro de falsación (B-bis):** si el archivo mínimo trae un campo de país de dos-letras/Gleditsch-Ward legible y filtrable con herramientas ya presentes → `RECORTE-VIABLE`, y este acto da el comando y el volumen estimado del recorte mexicano. Si el único camino para aislar México exige cruzar contra una tabla de referencia geográfica que no está en el repo (lat/lon sin país, o un ID que no mapea a país sin una tabla externa) → `VIABLE-CON-PARSER-NUEVO`, sin escribir el parser aquí. Si no hay ningún campo, archivo ni endpoint que distinga país → `NO-SEPARABLE`, resultado válido y cierre completo de la pregunta.

**Reserva de A.4, no se salta:** `EXISTE-NO-SATISFACE` es la clasificación vigente y correcta de ambas fuentes hoy. Solo cambia si este acto demuestra el recorte con comando y salida real. Un `200` en la portada no es satisfacción.

**El primer resultado que produzca este procedimiento es el que se reporta.**
