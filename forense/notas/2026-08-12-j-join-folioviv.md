# ACTO J · Medición del alcance de `folioviv`, normalización y remediación propuesta

**Encargo:** `forense/encargos/2026-08-12-J-join-folioviv.md` (texto completo, con la adjudicación de dirección de seis ajustes).
**Rama:** `mesa/j-join-folioviv` · **Worktree:** `~/mm-j-join-folioviv`, creado nuevo desde `origin/main` (no reutiliza ningún worktree existente).
**HEAD inicial:** `3e071f0` (Merge PR #175) — SHA de redacción del encargo confirmado exacto contra `origin/main`, 0 commits de diferencia.
**Entorno (huella de 2 valores crudos, ajuste 5):** `CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE` = `UNSET` (no declarada) · sonda `curl -s -o /dev/null -w "%{http_code}" https://www.inegi.org.mx/` = `200`. Combinación `sin_variable + 200` = **caja local = adelante**. Corroborado por un tercer valor no pedido por el ajuste pero exigido por `instrucciones-proyecto-v2_6.md` Bloque D-bis A.2 (la firma tiene tres partes, no dos): `ls data/raw/` lista archivos ENIGH reales (`enigh2012_nc_csv.zip` … `enigh2022_nc_csv.zip`, `R1_1_AGROASEMEX`, etc.) a través del symlink `data/raw -> /home/pc0/mm-corpus/raw`, replicado en este worktree desde `mm-e4c-r5-1-d2` (mismo corpus compartido, no descargado aquí).

## §0 · Premisas (PASO 1, script literal contra `origin/main` fresco)

```
$ git fetch -q origin
$ git diff --name-only origin/main...origin/e4c/r5-1-d2 | grep -cE "r5_1_pension|p3_lca"
0
PASA interseccion-e4c-vacia
```

Diff completo `origin/main...origin/e4c/r5-1-d2` (7 archivos, ninguno del perímetro de este acto):
```
data/manifiesto.yaml
forense/encargos/2026-08-12-E4c-commit4.md
forense/hallazgos.md
forense/notas/2026-08-11-e4c-r5-1-d2-commit3-ajuste-preejecucion.md
forense/notas/2026-08-11-e4c-r5-1-d2-especificacion.md
forense/notas/2026-08-12-e4c-r5-1-d2-commit4-diseno-resuelto.md
forense/notas/2026-08-12-e4c-r5-1-d2-commit5-correccion-varianza-ddd.md
```

Universo de olas, derivado de `data/manifiesto.yaml`:
```
$ grep -oE "enigh[_-]?20[0-9]{2}" data/manifiesto.yaml | grep -oE "20[0-9]{2}" | sort -u | tr '\n' ' '
2012 2014 2016 2018 2020 2022
```
Seis olas — coincide exacto con lo que el ajuste 4 de dirección ya adelantó ("ENIGH 2012 · 2014 · 2016 · 2018 · 2020 · 2022"). Re-derivado en esta sesión, no heredado de la prosa del ajuste.

**Defecto de instrumento encontrado y evitado, no heredado — `grep -q` de `ugrep` no lee sustitución de proceso.** La línea literal del script de PASO 1, `grep -q "2018" <(grep -oE "enigh[_-]?20[0-9]{2}" data/manifiesto.yaml) && echo PASA-ola-2018 || echo PARA-sin-2018`, imprime **`PARA sin-2018`** en esta caja — pero 2018 sí está presente, verificado por triple vía independiente:
1. El mismo `grep -oE` sin `-q` y sin sustitución de proceso lista `enigh2018` (×2) + `enigh_2018` (×1).
2. El mismo `grep -oE` canalizado por un **pipe normal** (no sustitución de proceso) hacia `grep -q "2018"` sí encuentra la coincidencia (`exit 0`).
3. Un caso trivial, ajeno por completo al dato: `grep -q "hello" <(echo "hello world")` también falla (`exit 1`, "no encontrado") bajo esta misma combinación.

Causa raíz: el `grep` de esta caja es `ugrep 7.5.0` (`x86_64-pc-linux-gnu`), y su bandera `-q` no lee correctamente un FIFO de sustitución de proceso (`<(...)`) — reporta "sin coincidencia" sin haber leído el flujo completo, de forma reproducible (5/5 corridas, ver bitácora de comandos de esta sesión). No es un defecto de `data/manifiesto.yaml` ni del universo de olas — es un defecto del binario `grep`/`ugrep` de esta máquina frente a un patrón de shell específico (`-q` + `<(...)`), capturado aquí para que ningún acto futuro confíe en esa combinación en esta caja sin verificar por una vía alterna. Registrado en `forense/hallazgos.md` al cierre (commit 2). El PASO 1 continúa con el universo verificado por las tres vías independientes (seis olas, 2018 incluida) — esto **no** es un PARA real; es un falso negativo del arnés de verificación, exactamente la clase de cosa que este programa ya aprendió a no heredar sin comprobar (`tests/manifiesto.py --verifica` con `--id` repetido, Nota de `hitoD-r5-1-pension-bienestar`, mismo género de defecto: un verificador que no revisa lo que dice revisar).

Scripts del perímetro:
```
$ ls tests/r5_1_pension_bienestar.py tests/p3_lca_data.py
PASA scripts
```

**Hermanos derivados por `grep -rln "folioviv" tests/ tools/`** (el propio PASO 1 exige derivarlo y reportarlo) — **cuatro archivos, no dos**:
- `tests/r5_1_pension_bienestar.py` (nombrado en el encargo)
- `tests/p3_lca_data.py` (nombrado en el encargo)
- `tests/p3_lca_run.py` (hermano no nombrado en el encargo — usa `row["folioviv"]` solo como llave de deduplicación de hogar dentro de la lista `universo` que **ya construyó** `p3_lca_data.cargar_universo()`; no abre ninguna tabla nueva ni hace un cruce contra otra fuente. No necesita el arreglo — se declara aquí por transparencia, no se edita)
- `tests/p3_lca_stage.py` (mismo caso que `p3_lca_run.py`: su función `stage_universo_meta` repite la misma deduplicación sobre la misma lista ya construida — no edita)

Ningún resultado de `tools/` (el grep cubrió ambos directorios, cero coincidencias en `tools/`).

El cruce real que puede perder filas en silencio vive en dos sitios, ambos ya dentro del perímetro nombrado por el encargo:
1. **`tests/r5_1_pension_bienestar.py::procesar_ola()`** — `hogares` se construye desde `concentradohogar` (llave `folioviv+foliohog`); cada fila de `ingresos` se busca en ese diccionario por su propio `folioviv+foliohog` (`hh = hogares.get(hkey)`). Si `ingresos.folioviv` viene truncado a 9 caracteres y `concentradohogar.folioviv` correcto a 10, la búsqueda falla, `hh is None`, y la fila se descarta en silencio (`continue`) — se pierde la detección de `beneficiario`/`transferencia_mayor`/sus montos para ese hogar, en ese trimestre de esa clave.
2. **`tests/p3_lca_data.py::construir_universo()`** — `conc_por_hogar`/`hog_por_hogar` se construyen desde `concentradohogar`/`hogares` (llave `folioviv+foliohog`); cada fila de `poblacion` los busca por su propio `folioviv`. Mismo patrón de riesgo estructural — aunque el universo que este script recorre **hoy** es únicamente ENIGH 2022 (`ENIGH_ZIP = "enigh2022_nc_csv.zip"`, constante de módulo, sin parámetro de ola), y esa ola ya la verificó limpia e4c commit 3 (`poblacion.factor == concentradohogar.factor` exacto en 29,974/29,974 personas 65+, sin una sola discrepancia).

No se abrió ningún archivo de `data/raw/` para escribir lo anterior — todo sale de leer el código de los cuatro scripts y la nota de e4c commit 3 (`git show origin/e4c/r5-1-d2:forense/notas/2026-08-11-e4c-r5-1-d2-commit3-ajuste-preejecucion.md`), no del microdato mismo.

## §1 · Especificación (congelada aquí, antes de abrir cualquier archivo de `data/raw/`)

### 1.1 · Qué se mide

Para cada una de las seis olas derivadas en §0 (2012, 2014, 2016, 2018, 2020, 2022) y para cada una de las tres tablas `concentradohogar`, `poblacion`, `ingresos` (rutas ya declaradas dentro del diccionario `WAVES` de `tests/r5_1_pension_bienestar.py`, no re-tecleadas):

- `n_filas_total` — filas leídas de la tabla.
- `n_filas_folioviv_9` — filas cuyo campo `folioviv` (después de `.strip()`, sin reinterpretar el valor) mide exactamente 9 caracteres.
- `n_filas_folioviv_otro` — cualquier longitud que no sea 9 ni 10 (caso borde declarado por adelantado: si aparece, se reporta aparte, nunca se descarta en silencio ni se fuerza dentro de las otras dos categorías).
- `proporcion_9 = n_filas_folioviv_9 / n_filas_total`.
- `entidades_afectadas` — lista de entidades (columna `entidad` propia de la tabla si la tabla la trae; `poblacion` la trae, confirmado leyendo `p3_lca_data.py::migracion()`, que ya la usa). Si una tabla no trae `entidad` propia (a verificar al abrir, no asumido aquí), se deriva por un cruce **dentro de la misma ola**, tabla afectada ↔ `poblacion` de esa misma ola por `folioviv+foliohog` usando el valor crudo (sin zfill) como llave — es un cruce entre hermanas de la misma exportación para caracterizar el defecto, no el cruce roto contra `concentradohogar`/`hogares` que se está midiendo, así que no hereda el problema que mide.
- `concentradohogar` se mide igual, como **tabla testigo/control** en las seis olas — e4c ya reportó `0/74,647` para 2018; esta medición re-confirma esa cifra como parte del barrido uniforme y añade la cifra testigo de las otras cinco olas, con el mismo procedimiento, no copiada.

Reporte: una tabla por ola (o una tabla única con las seis olas como filas), tres tablas por ola. `2018` es la única con el defecto ya confirmado por e4c commit 3; `2022` está confirmada limpia; `2012`, `2014`, `2016`, `2020` no se han mirado antes de este acto — sus cifras son la primera medición.

### 1.2 · Cómo (normalización)

`folioviv.str.zfill(10)` — heredada de e4c commit 3, verificada ahí contra el valor real de `concentradohogar` para el mismo hogar (`"100013601"` → `"0100013601"`). **No se re-verifica esa equivalencia aquí — se hereda tal cual.** Se aplica de forma puntual, solo al construir la llave de cruce (`folioviv+foliohog` o `folioviv+foliohog+numren`) en el momento de leer cada fila de `poblacion`/`ingresos`; nunca reescribe la columna cruda en memoria más allá de esa llave, y nunca toca ningún archivo de `data/raw/` ni de otro acto — mismo criterio que e4c commit 3 declaró para su propio arreglo puntual.

### 1.3 · El test que faltaba — `tests/test_join_folioviv.py`

- Para cada ola con datos en disco: localiza las filas de `ingresos` (perímetro de `r5_1_pension_bienestar.py`) y de `poblacion` (perímetro de `p3_lca_data.py`) cuyo `folioviv` no mide 10 caracteres tras `zfill(10)` — declarado por adelantado: si algún `folioviv` real mide **más** de 10 caracteres, `zfill` no lo trunca y no lo arregla; ese caso se cuenta y se reporta aparte, nunca se descarta.
- Ejercita el join real de `procesar_ola()` / `construir_universo()` contra `concentradohogar`/`hogares` de la misma ola, **con y sin** la normalización, y compara — por entidad — cuántas filas encuentran hogar (`hh is not None` / `crow is not None`) antes y después.
- **Falla (assert)** si, tras aplicar la normalización, alguna entidad tiene cobertura *menor* que antes de aplicarla (el arreglo nunca debe perder una fila que antes sí casaba).
- **Falla (assert)** también sobre el código SIN arreglar si alguna entidad muestra una caída de cobertura de más de 5 puntos porcentuales frente al resto de entidades de la misma ola (umbral elegido aquí, antes de ver el dato) — esa caída asimétrica y concentrada por entidad es la firma declarada del defecto (entidades 01-09 truncan, el resto no tendría por qué). Este es el mecanismo de "cobertura por entidad" que `validar_contra_publicado()` nunca tuvo: esa función solo suma columnas propias de `concentradohogar` (`bene_gob`, `donativos`, `jubilacion`, `factor`) contra un número publicado por INEGI — nunca abre `ingresos` ni `poblacion`, nunca ejercita el join, y por construcción no puede ver una fila que el join pierde silenciosamente. Es la explicación de por qué pasó verde con el join roto: mide una tabla que nunca tuvo el defecto.
- Modo `--baseline`: nunca silencia — si una corrida gana entradas de cobertura frente a la corrida anterior, se reportan explícitamente, no se absorben en un contador agregado.
- Por diseño explícito del ajuste 6: este test se **corre una vez contra el código sin arreglar antes de tocar los scripts del perímetro**, y esa salida (la falla) se archiva verbatim en la §2 de esta misma nota, en el commit 2. No se edita esta §1 después de esa corrida.

### 1.4 · Efecto sobre los estimandos, en escala declarada (A-bis regla 3, `instrucciones-proyecto-v2_6.md:83`: *"Toda cantidad medida entra con su escala declarada, y no se compara contra otra escala… Está prohibido escribir 'el medido es X, el asignado era Y, difiere en Z%' entre escalas distintas: es un error de categoría, no una medición."*)

- **R5.1 (veredicto `A`, ADR-58, `canon/gobernanza-v1_15.md:637`).** Escala nativa: diferencia de proporciones ponderada por conglomerado último (`prop_ultimate_cluster` de `tests/svystat.py`, ya validado contra caso SRS conocido — no se re-valida aquí), en **puntos porcentuales**, con IC95%. Se recalcula `resumen_ola()` para cada ola con defecto medido en §1.1, antes y después de aplicar la normalización, y se reporta la diferencia en puntos porcentuales de **cada** proporción por separado (`corresidencia_benef`, `corresidencia_no_benef`, `transferencia_benef`, `transferencia_no_benef`) — nunca un solo número agregado entre ellas, y nunca agregado entre olas de universo distinto (regla 4, ver 1.5).
- **D5 (veredicto INESTABLE, ADR-53, `canon/gobernanza-v1_15.md:543`).** Escala nativa: la curva BIC/aBIC de `k=1..8` y las señales de estabilidad E1/E2/E3 de `tests/p3_lca_run.py`. Como `p3_lca_data.py` abre **exclusivamente** ENIGH 2022 (constante de módulo, confirmado en §0, sin parámetro de ola), y 2022 ya se mide en §1.1 como parte de las seis olas: si 2022 sale limpia (como e4c ya encontró de forma independiente para el join `poblacion`↔`concentradohogar`), el efecto sobre D5 es **cero por construcción** — no hace falta re-correr el LCA (fuera de alcance: este acto no re-corre protocolos ni produce veredictos) para saberlo, basta con que la medición de §1.1 lo confirme para 2022. Si 2022 apareciera con `folioviv` de 9 caracteres en `poblacion` (contradiciendo a e4c), esa sería la señal de "algo destraba un cálculo mayor" que el cierre del encargo pide reportar y parar antes de seguir — no se seguiría midiendo D5 en ese escenario sin volver a mesa.
- Las dos escalas (puntos porcentuales de proporción para R5.1; BIC/aBIC y correlaciones de estabilidad para D5) **no se combinan entre sí ni se agregan** — se reportan en tablas separadas.

### 1.5 · Universo, declarado por ola

| Ola | Tablas que este acto mide | Llave de cruce | Filas que entran a la medición |
|---|---|---|---|
| 2012 | `concentradohogar`, `poblacion`, `ingresos` | `folioviv+foliohog` (hogar) / `+numren` (persona, solo para derivar entidad de `ingresos` si hace falta) | Todas las filas de las tres tablas, sin filtrar por edad ni por beneficio — la medición de §1.1 es sobre el universo completo de cada tabla, no sobre el universo analítico de R5.1 (que sí filtra por `p65mas>=1`) |
| 2014 | ídem | ídem | ídem |
| 2016 | ídem | ídem | ídem |
| 2018 | ídem | ídem | ídem (re-mide lo que e4c ya midió, con el mismo método, para cruzar cifras) |
| 2020 | ídem | ídem | ídem |
| 2022 | ídem | ídem | ídem (re-mide lo que e4c ya midió para el join `poblacion`↔`concentradohogar`; añade `ingresos`, que e4c no tocó) |

**Advertencia de A-bis regla 4** (`instrucciones-proyecto-v2_6.md:85`: *"Un estimando restringido a una subpoblación no se compara contra uno poblacional… Se recalcula el marginal restringido al mismo universo, o se declara el resultado como acotado a esa subpoblación."*) — aplicada aquí a su generalización temporal declarada por el propio encargo: si el arreglo cambia qué hogares caen en `benef`/`no_benef` (porque antes se perdían en el join y ahora se encuentran), el universo de hogares detrás del marginal **corregido** de R5.1 no es el mismo conjunto de hogares que el marginal **sellado** por ADR-58 — son composiciones distintas del mismo universo nominal (hogares con `p65mas>=1`). La comparación entre ambos, si se hace, se declara explícitamente como "marginal sobre universo corregido" vs. "marginal sobre universo con el defecto", nunca como si fueran la misma medición repetida.

### 1.6 · Qué NO se hace aquí

No se re-corren `tests/r5_1_pension_bienestar.py` en modo de corrida oficial completa (`--estratos` como entrega) ni `tests/p3_lca_run.py` / `tests/p3_lca_stage.py assemble` para producir un veredicto nuevo. Si en el commit 2 se invoca `resumen_ola()` para medir el antes/después del join (§1.4), esa invocación es explícitamente una **medición de magnitud para este acto** — no una corrida oficial: no escribe a `forense/hitoD-preregistro-v2_0.md`, no toca su bloque append-only, no adjudica `R5.1` ni `D5`. No se toca `canon/`, `milpa/`, `data/curacion-*`, ni archivos de `e4c/r5-1-d2` ni de ninguna otra rama viva. La adjudicación de `R5.1`/`D5` es acto propio de mesa, posterior a este.

---

**El primer resultado que produzca este procedimiento es el que se reporta.**
