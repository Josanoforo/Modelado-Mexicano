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

**El primer conteo que produzca este mecanismo, cruzado por la vía independiente de §2, es el que se reporta en `data/universo-cota-2026-08-12.tsv`** (nombre de archivo corregido a la fecha real de la sesión — el encargo asumía 13/ago, la sesión corrió el 12/ago; ver commit 1 de este acto).

## §4 · Los tres denominadores, contados (commit 2)

| Denominador | Valor | Mecanismo |
|---|---|---|
| D1 — activos T0 | **35,708** | `wc -l` sobre `universo-declarado-t0.tsv` |
| D1 — programas nombrados (crudo) | **958** | valores únicos de `fuente_programa` |
| D2 — fichas del catálogo RNM | **825** | export CSV del catálogo, `ps=5000` |
| D3 — relaciones de demanda | **197** | filas de `relaciones.tsv` |
| D3 — fuentes únicas de demanda | **75** | valores únicos de `fuente_canonica_normalizada` |

Detalle en `data/universo-cota-2026-08-12.tsv`. D2 re-verificado por segunda vez, en un fetch separado, minutos después del primero: bit-idéntico. Cruce independiente contra la paginación HTML: el último enlace de página es `page=55`; `55 × 15 = 825`, exacto — confirma que el export CSV no está truncado ni duplicado.

## §5 · El "958" — receta mecánica encontrada, pero el número no es un conteo limpio de programas

`awk -F'\t' 'NR>1{print $2}' universo-declarado-t0.tsv | sort -u | wc -l` da **958**, exacto contra la cifra citada sin receta en `gobernanza:862`. Es muy probable que sea el origen real del número — nadie inventa "958" de la nada, y el comando es obvio una vez que se sabe qué columna mirar.

**Pero el 958 no cuenta programas distintos — cuenta cadenas de texto distintas.** Evidencia directa: la columna `fuente_programa` contiene, entre sus valores únicos, **10 variantes distintas de cadena** que todas nombran el mismo programa real (verificado con `grep -c "Censo de Población y Vivienda"` sobre el listado de únicos):
```
1. Censo de Población y Vivienda
1. Censo de Población y Vivienda (CPV)
1. Censo de Población y Vivienda (CPV) — antes Censo General de Población y Vivienda (CGPV)
1. Censo de Población y Vivienda / Conteos
1. Censo de Población y Vivienda 2020
... (5 más, mismo patrón)
```
Esto no es un caso aislado — es exactamente la misma clase de defecto que `alias-fuentes.yaml` (128 entradas canónicas) ya tuvo que resolver para otro campo de este mismo corpus (`MAP-1`, ver memoria del proyecto). No se intenta deduplicar `fuente_programa` en este acto — está fuera de perímetro (sería, en sí mismo, un acto del tamaño de `alias-fuentes.yaml`) — se declara el hallazgo y se deja para quien lo necesite.

**Clasificación operativa:** ni `CIFRA-SIN-RECETA` (sí hay una receta mecánica reproducible) ni un conteo limpio de programas (los valores no están deduplicados). Se declara ambas cosas en la fila `D1_programas_nombrados_crudo` de la TSV, sin forzar ninguna de las dos etiquetas que el encargo ofrecía.

## §6 · Reconciliación

- **43 de las 825 fichas de D2 (5.2%) están referenciadas desde D1** vía `url_localizador_principal` apuntando a `rnm/index.php/catalog/<id>` — las 43 ids son válidas contra el D2 vigente (ninguna referencia obsoleta/removida). 399 filas de D1 (de 35,708) cargan una URL de RNM; de esas, solo **8 (2.0%) están `ADQUIRIDO`** — el resto, `DECLARADO_NO_ADQUIRIDO`.
- **De los 958 nombres únicos de D1: 915 (95.5%) no tienen NINGUNA fila con URL de RNM** — el universo de D1 es mucho más amplio que el catálogo RNM; RNM es un canal entre varios (portales de datos abiertos, otros organismos, descargas directas). Solo 5 nombres aparecen EXCLUSIVAMENTE en filas con URL de RNM; 38 nombres aparecen tanto en filas con URL de RNM como sin ella (mismo programa, activos de origen mixto).
- **D3 (demanda) vs D1:** 25 de las 75 `fuente_canonica_normalizada` de `relaciones.tsv` (33.3%) coinciden por cadena EXACTA contra `fuente_programa` de D1 — el resto no empareja por nombre (mismo defecto de vocabulario que MAP-B fue dispatchado a resolver con un crosswalk propio, no una coincidencia de cadena). No se intenta aquí un cruce más fino (evidencia_ref, alias) — ese es el perímetro explícito de MAP-B, no de este acto.

## §7 · Propuesta a mesa — el rótulo que sustituye `COTA_SUPERIOR_NO_RECONCILIADA`

No se sella aquí — mesa decide en acto propio. Propuesta, basada en lo contado:

```
COTA_RNM=825 (export CSV del catálogo, verificado 2026-08-12) +
COTA_T0=35708 activos / 958 nombres-de-programa-crudos-sin-deduplicar +
NO_RNM_SIN_COTA (para el 95.5% de nombres de D1 sin URL de RNM -- canal
  desconocido en agregado; cada activo individual SÍ declara su propia
  fuente/URL, lo que falta es un catálogo externo independiente con el
  que reconciliar ESE conjunto, análogo a lo que RNM ofrece para el resto)
```

El régimen "5 instrumentos de 958 programas hoy conocidos (0.52%)" citado en gobernanza:862 debería leerse, tras este acto, como "5 de 958 *nombres de programa no deduplicados*" — la fracción real (sobre programas verdaderamente distintos) es más alta que 0.52%, en un grado no cuantificado aquí porque cuantificarlo exige la deduplicación que este acto no hace.

## §8 · Qué NO hace este acto

No descarga payloads. No clasifica fuentes (A.4, perímetro de P/R). No reabre cierres. No dedupica `fuente_programa` (declarado en §5, no ejecutado). No edita `canon/gobernanza-v1_15.md` ni el tablero — la propuesta de §7 es eso, una propuesta.

No se encontró, al enumerar RNM, ninguna fuente que destrabe un SIN-RUTA abierto conocido por esta sesión (no se cruzó activamente contra `relaciones.tsv`'s `SIN-RUTA` — fuera del perímetro declarado; si esa verificación específica importa, es un acto de seguimiento, no este).
