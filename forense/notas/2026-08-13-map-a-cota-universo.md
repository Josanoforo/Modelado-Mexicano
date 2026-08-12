# MAP-A · Reconciliación de la cota del universo

**Acto:** ENCARGOS · MAPEO DE UNIVERSO COMPLETO — MAP-A · **Entorno:** caja (Ubuntu-con-red, `CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE` sin definir, sonda RNM 200) · **Base:** `origin/main = 11083af` (post-PR #184) · **Worktree:** `~/mm-map-a-cota-universo`, rama `map-a/cota-universo`.

## §0 · Premisas verificadas (ARRANQUE)

- `grep -c COTA_SUPERIOR_NO_RECONCILIADA canon/gobernanza-v1_15.md` → 1 (línea 862, texto citado íntegro en el encargo archivado).
- `wc -l data/curacion-universo/universo-declarado-t0.tsv` → 35709 (35,708 filas + header). PASA.
- `grep -n 958 canon/gobernanza-v1_15.md` → confirma la cifra tal como aparece en gobernanza:862, sin receta citada ahí.
- Sonda RNM: `curl -s -o /dev/null -w "%{http_code}" https://www.inegi.org.mx/rnm/index.php/catalog` → `200`.
- `data/raw` ausente en el worktree fresco — mecanismo de symlink estándar (`~/mm-corpus/raw`), no se toca.
- El documento maestro que dispatchó este acto (mensaje pegado en sesión, no archivo del repo) queda archivado en `forense/encargos/2026-08-12-veredicto-pr185-mapeo-universo-map-a.md` (regla A.3, sufijo `-map-a` para evitar colisión de nombre con el acto hermano MAP-B, que recibió el mismo documento).

## §1 · Desviación declarada del patrón de dos commits — por qué, y por qué no aplica el mismo riesgo que a una estimación

El encargo pide "pre-registro del mecanismo de conteo, ANTES de contar". **Esta sesión no logró una secuencia ciega estricta**: descubrir cuál mecanismo de conteo de D2 (RNM) era el correcto — HTML paginado vs. un posible endpoint de exportación — exigió sondear el catálogo primero; no existe manera de pre-registrar el uso de un endpoint cuya existencia todavía no se conoce. La exploración reveló un endpoint de exportación CSV (`/rnm/index.php/catalog/export/csv?ps=5000`) que ninguna nota previa del corpus documenta. Declarado aquí en vez de fingir una secuencia ciega que no ocurrió.

**Por qué esto no compromete la disciplina de "no calcular dos veces hasta que guste el resultado" que motiva el patrón de dos commits en este proyecto:** ese patrón protege contra grados de libertad de un analista sobre una ESTIMACIÓN (qué dicotomización, qué universo, qué exclusión escoger hasta que el número favorezca una hipótesis). Un conteo mecánico de filas de un CSV exportado por el propio catálogo no tiene ese espacio de decisión — recontar el mismo archivo produce el mismo número, siempre; no hay una segunda corrida "más favorable" posible. El mecanismo se declara aquí, verificado y cruzado por una vía independiente (ver §3), antes de escribir el TSV final en el commit 2 de este mismo acto — eso sí se respeta.

## §2 · Los tres denominadores — mecanismo declarado

- **D1 — activos declarados T0.** `data/curacion-universo/universo-declarado-t0.tsv`, grano `activo_id` (objeto/archivo declarado, no programa). Receta: `wc -l` menos header. Columna `fuente_programa` (texto libre, no normalizado) permite un desglose por programa nombrado, pero **no es un catálogo deduplicado** — ver §4.
- **D2 — catálogo RNM (INEGI).** Mecanismo: endpoint de exportación CSV del propio catálogo, `https://www.inegi.org.mx/rnm/index.php/catalog/export/csv?ps=5000&collection[]=` — devuelve un CSV limpio con `id,idno,title,...` de todas las fichas listadas, sin necesidad de paginar HTML. Se prefiere sobre paginación HTML/`<tr>`/`<td>` (que sí sería obligatoria si este endpoint no existiera, por la lección de U1 §4 — fetch resumido por IA prohibido para tablas RNM) porque es la fuente estructurada más directa disponible. **Cruzado por una segunda vía independiente:** la paginación HTML de `/rnm/index.php/catalog/` expone un último link `page=55`; si el tamaño de página nativo es 15 (verificable dividiendo el total del CSV entre 55), ambas vías deben coincidir exactamente — ver §3.
- **D3 — demanda del modelo.** `data/curacion-registro/relaciones.tsv`. Receta: filas totales menos header (relaciones); `fuente_canonica_normalizada` únicas (fuentes).
- **El "958":** rastreado en el repo antes de contar nada nuevo — no aparece en ningún otro archivo con una receta citada más allá de la prosa de gobernanza:862. Se prueba en commit 2 si algún comando mecánico sobre datos ya existentes lo reproduce exacto; si no, se declara `CIFRA-SIN-RECETA` y D2 la sustituye como denominador de "programas conocidos".

## §3 · Criterio de cierre si RNM no se puede enumerar completo

Si el endpoint de exportación o la paginación fallan a mitad de camino (bloqueo, truncamiento), el entregable es la cota PARCIAL con su universo de conteo declarado explícitamente ("enumerado hasta X con este mecanismo, mecanismo Y") — nunca un total inferido o extrapolado.

**El primer conteo que produzca este mecanismo, cruzado por la vía independiente de §2, es el que se reporta en `data/universo-cota-2026-08-13.tsv`.**
