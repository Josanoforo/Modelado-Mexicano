# MAP-B — crosswalk demanda↔puertas

**Acto:** ENCARGOS · MAPEO DE UNIVERSO COMPLETO — MAP-B · **Entorno:** CAJA LOCAL Ubuntu CC, repo-only (cero red, sonda omitida como ACTO O) · **Base:** `origin/main = 11083af` (post-#184, verificado antes de abrir worktree) · **Worktree:** `~/mm-map-b-crosswalk`, rama `map-b/crosswalk-fuente-puerta`.

## §0 · Premisas verificadas

```
awk -F'\t' 'NR>1{print $3}' data/curacion-registro/relaciones.tsv | sort -u | wc -l   -> 75
ls data/universo-puertas-*.tsv | sort | tail -1                                        -> data/universo-puertas-2026-08-12.tsv
ls data/cola-adquisicion-*.tsv | sort | tail -1                                        -> data/cola-adquisicion-2026-08-12.tsv
```
`relaciones.tsv`: 198 líneas (197 relaciones + header). `universo-puertas-2026-08-12.tsv`: 32 líneas (31 puertas + header). `cola-adquisicion-2026-08-12.tsv`: 55 líneas (54 fuentes + header, subconjunto de las 75 — solo la capa `NO_REFERENCIADO` que ACTO O derivó).

**Tres actos pushearon hoy (PR #185, #186, #187) tocando `data/universo-puertas-2026-08-12.tsv` en sus propias ramas — ninguno fusionado a `origin/main` todavía.** Este worktree, cortado limpio de `origin/main`, no ve esas filas. Correcto y esperado: este acto trabaja contra lo que realmente hay en `main`, no reconcilia contra ramas sin fusionar — mesa hace esa reconciliación multi-vía al fusionar.

## §1 · El método de equivalencia, declarado ANTES de cruzar nada

El cruce por nombre exacto entre `fuente_canonica_normalizada` (75 valores) y `puerta` (31 valores) da **0 coincidencias** (`comm -12` sobre ambos conjuntos ordenados-únicos). Dos vocabularios sin tabla de equivalencia. Toda equivalencia que este acto declare se establece por evidencia citada, en esta jerarquía, nunca por parecido de cadena:

1. **URL** — `cola-adquisicion.url_conocida` coincide (mismo recurso, aunque difiera el prefijo de colección/ruta) con `universo-puertas.url`.
2. **Necesidad** — `universo-puertas.necesidad_que_sirve` nombra el mismo `necesidad_id` que alguna relación de esa fuente en `relaciones.tsv`, **reforzado por** identidad de nombre/institución (necesidad compartida SOLA, sin refuerzo de nombre, no basta — varias puertas distintas sirven la misma necesidad sin ser la misma fuente; ver ejemplo real en §2, IMSS).
3. **Cita explícita de otro archivo del repo** (archivo:línea) que declare la relación — incluye los registros de alias ya existentes (`data/curacion-registro/aliases-fuentes.tsv`, `data/inventarios/alias-fuentes.yaml`), consultados como fuente de evidencia, no de fusión: si un alias registry no declara una identidad, este acto NO la inventa (verificado: ninguno de los dos registros de alias contiene una entrada relevante a las equivalencias fuente↔puerta de este acto — cubren duplicados dentro del lado de la demanda, `ENBIARE2021→ENBIARE` etc., un problema distinto).

**Ambigüedad:** si una fuente corresponde plausiblemente a **más de una** puerta sin evidencia que prefiera una sobre las otras, la fila queda `gap = EQUIVALENCIA-AMBIGUA`, columna `puerta` lista TODAS las candidatas separadas por `;`, y `evidencia_de_equivalencia` declara por qué ninguna se prefirió. No se resuelve adivinando — ni tomando la primera, ni la de nombre más largo, ni ninguna heurística de conveniencia.

**Rechazo explícito, no silencioso:** una coincidencia de institución o de tema por sí sola, sin URL ni necesidad ni cita que confirme que es el MISMO producto/dataset, se declara y se descarta — la fila queda `SIN-PUERTA` con la candidata rechazada nombrada en `evidencia_de_equivalencia`, no se omite de la nota. Ver §2 para el caso real (IMSS).

**Columnas de `data/crosswalk-fuente-puerta-2026-08-13.tsv`** (una fila por cada una de las 75 fuentes): `fuente_canonica · puerta (o VACIO) · evidencia_de_equivalencia · clasificacion_a4_de_la_puerta (copiada de la puerta real, no re-derivada) · capa2_agregada · en_cola · gap`.

`capa2_agregada`: 10 de las 75 fuentes tienen `capa2_manifiesto` heterogéneo entre sus propias relaciones (p. ej. `ENBIARE` trae tanto `SI` como `SI_O_REFERENCIADO` en filas distintas de `relaciones.tsv`). Regla de agregación, declarada aquí antes de aplicarla: se reporta el valor de mayor cobertura presente, orden `SI > SI_O_REFERENCIADO > NO_REFERENCIADO` — refleja "esta fuente tiene AL MENOS una relación en esta capa", consistente con cómo ACTO O ya trata `capa2_manifiesto` como filtro de máxima-cobertura, no se inventa un criterio nuevo.

`en_cola`: el valor de `palanca` de `data/cola-adquisicion-2026-08-12.tsv` si la fuente aparece ahí (54 de 75), si no, `NO` — no todas las 75 fuentes están en la cola porque la cola es solo la capa `NO_REFERENCIADO` de ACTO O (105 relaciones → 54 fuentes únicas), las demás 21 ya tienen `capa2 ∈ {SI, SI_O_REFERENCIADO}` y no entraron a esa cola por diseño de ese acto, no por omisión de este.

`gap` para `SIN-PUERTA`: por cada una, se añade una fila nueva al puntero vigente (`data/universo-puertas-2026-08-12.tsv`) con `puerta = <fuente_canonica_normalizada misma>` (identificador trazable, no una institución inventada), `clase_origen = gap_mapeo_map_b` (valor nuevo, deliberado — ninguno de los 6 valores ya en uso en esa columna — `canasta_publica`, `catalogo_metadatos_inegi`, `ong_observatorio`, `organismo_internacional`, `repositorio_academico`, `transparencia` — describe honestamente "no se encontró institución", forzar uno de esos sería una clasificación falsa), `clasificacion_a4 = NO-ENCONTRADO`, `universo_declarado` cita el mecanismo exacto de búsqueda y la fecha. Cero red en ninguna de estas filas — nacen `NO-ENCONTRADO` de mapeo, no de sondeo.

**El primer resultado que produzca este cruce es el que se reporta** — no se re-corre buscando un embudo con menos `SIN-PUERTA`.
