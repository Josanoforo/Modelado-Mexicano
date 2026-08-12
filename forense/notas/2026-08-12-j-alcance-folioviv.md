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

---

## §2 · Resultados y arreglo (commit 2 — el §0/§1 de arriba no se editó)

### 2.0 · La demostración del hueco (ajuste 6)

**Una simplificación frente a §1.3, declarada aquí (el §1 no se edita):** los dos asserts que §1.3 preveía (no perder cobertura que el arreglo ya tenía; frenar si el código sin arreglar muestra >5pp de asimetría entre entidades) se colapsan en uno solo, más estricto — `assert n_perdidos_total == 0` por ola. Cero pérdidas implica asimetría cero para esa ola (la implicación lógica corre en un solo sentido, y es el sentido que hace falta), y es más simple de verificar dentro de una sola invocación que una comparación cruzada entre dos corridas del mismo proceso. La asimetría se sigue calculando e imprimiendo como diagnóstico (ver la salida cruda abajo), ya no como umbral que decide pasa/falla.

`tests/test_join_folioviv.py` se corrió **una vez contra el código sin arreglar** (el que quedó congelado en el commit 1, `7525b70`), antes de tocar `r5_1_pension_bienestar.py`/`p3_lca_data.py`. Salida cruda completa (también en la bitácora de comandos de esta sesión):

```
TEST R5.1 -- cobertura del cruce ingresos->hogares (deteccion de `beneficiario`), por entidad, seis olas:
  2012 (ancho nativo=6): hogares=9002 beneficiarios_perdidos_en_silencio=0 asimetria_max_min=0.00pp entidades_afectadas=[]
  2014 (ancho nativo=10): hogares=19479 beneficiarios_perdidos_en_silencio=0 asimetria_max_min=0.00pp entidades_afectadas=[]
  2016 (ancho nativo=10): hogares=70311 beneficiarios_perdidos_en_silencio=2179 asimetria_max_min=14.59pp entidades_afectadas=['01', '02', '03', '04', '05', '06', '07', '08', '09']
  2018 (ancho nativo=10): hogares=74647 beneficiarios_perdidos_en_silencio=2094 asimetria_max_min=13.50pp entidades_afectadas=['01', '02', '03', '04', '05', '06', '07', '08', '09']
  2020 (ancho nativo=10): hogares=89006 beneficiarios_perdidos_en_silencio=0 asimetria_max_min=0.00pp entidades_afectadas=[]
  2022 (ancho nativo=10): hogares=90102 beneficiarios_perdidos_en_silencio=0 asimetria_max_min=0.00pp entidades_afectadas=[]
  FALLA -- procesar_ola() pierde hogares beneficiarios en silencio (join folioviv roto sin zfill): 2016: 2179 hogares en entidades ['01'..'09']; 2018: 2094 hogares en entidades ['01'..'09']

TEST P3-LCA -- cobertura del cruce poblacion->concentradohogar/hogares, por entidad, 2022:
  n_poblacion_total=309684 n_18_mas=217375 sin_match_concentradohogar=0 sin_match_hogares=0
  OK -- cero personas sin hogar en concentradohogar/hogares, ENIGH 2022.

test_join_folioviv.py: AL MENOS UN TEST FALLÓ (ver arriba).
```

Y, en el mismo estado pre-arreglo, `python3 tests/r5_1_pension_bienestar.py --validar` — la prueba de que `validar_contra_publicado()` pasa **verde** con el join roto:

```
n hogares ENIGH 2022 sin ponderar = 90102
  OK -- Total de hogares (sum factor): calculado=37,560,123.0 publicado=37,560,123 (dif rel 0.000%)
  OK -- bene_gob promedio ponderado: calculado=1,776.5 publicado=1,777 (dif rel 0.027%)
  OK -- donativos promedio ponderado: calculado=1,270.9 publicado=1,271 (dif rel 0.006%)
  OK -- jubilacion promedio ponderado: calculado=5,168.6 publicado=5,169 (dif rel 0.009%)
Validado contra caso conocido publicado.
```
Pasa verde porque, como declaró §1.3, valida exclusivamente contra 2022 y contra columnas propias de `concentradohogar` — nunca abre `poblacion`/`ingresos`, nunca ejercita el cruce por `folioviv`. No es que "la corrida buena tapó la mala": es que la función nunca mira el lugar donde vive el defecto, en ninguna ola.

### 2.1 · La magnitud (§1.1, ejecutada)

**Primer resultado, y corrige una premisa del propio encargo antes de reportar el resto: el universo de olas NO es binario (defecto/limpia).** El ajuste 4 de dirección decía *"2018 es la única verificada con el defecto y 2022 está limpia — ninguna otra se ha mirado"*. Verificado aquí, ola por ola:

| Ola | `concentradohogar` (testigo) | `poblacion` folioviv corto | `ingresos` folioviv corto | Entidades afectadas |
|---|---|---|---|---|
| 2012 | **6 caracteres, uniforme** (9,002/9,002) — esquema propio, NO una versión truncada de 10 | 0/33,726 (0%) | 0/46,616 (0%) | ninguna |
| 2014 | 10, uniforme (19,479/19,479) | 0/73,592 (0%) | 0/89,147 (0%) | ninguna |
| **2016** | 10, uniforme (70,311/70,311) | **80,587/257,805 (31.26%)** | **106,135/334,337 (31.74%)** | **01–09** (las 9) |
| 2018 | 10, uniforme (74,647/74,647) | 83,070/269,206 (30.86%) | 107,549/348,487 (30.86%) | 01–09 (las 9) |
| 2020 | 10, uniforme (89,006/89,006) | 0/315,743 (0%) | 0/394,912 (0%) | ninguna |
| 2022 | 10, uniforme (90,102/90,102) | 0/309,684 (0%) | 0/397,182 (0%) | ninguna |

`n_filas_folioviv_otro` (ni ancho nativo ni ancho nativo−1) = **0 en las seis olas, las tres tablas** — el cuadro es limpio, binario dentro de cada ola, sin longitudes sorpresa.

**Dos correcciones a la premisa del encargo, ambas a favor de mesa (más información, no menos):**
1. **2016 tiene el mismo defecto que 2018**, en la misma magnitud (~31%) y las mismas nueve entidades (01–09) — nadie lo había mirado antes de este acto. `2018` deja de ser el único caso conocido.
2. **2012 no es "limpia" ni "con defecto" — es un esquema distinto (`C(6)`, no `C(10)`), autoconsistente en sus tres tablas.** No es la misma clase de hallazgo que 2016/2018 (ahí el 9-vs-10 es una fila truncada respecto a su propia tabla testigo); es una ENIGH de una generación anterior con un identificador más angosto por diseño, y el cruce ya funciona tal cual viene. Aplicarle `zfill(10)` a ciegas la habría roto — ver §2.2.

Filas que el cruce viejo perdía (conteo directo, sin ambigüedad: un `folioviv` de 9 caracteres nunca coincide por igualdad de cadena con uno de 10, cero falsos empates posibles): exactamente `n_folioviv_corto` de la tabla de arriba, por tabla — 80,587 filas de `poblacion` y 106,135 de `ingresos` en 2016; 83,070 y 107,549 en 2018 (estas dos últimas cifras reproducen exacto lo que e4c commit 3 ya había medido para 2018, cruzado aquí con método independiente).

### 2.2 · El arreglo — generalizado, no reinventado

Heredado de e4c commit 3: normalizar `folioviv` de `poblacion`/`ingresos` antes de cruzar contra `concentradohogar`/`hogares`. **Lo que cambia frente al `zfill(10)` literal del §1.2 original: el ancho al que se rellena se deriva del propio `concentradohogar` de esa ola (siempre uniforme, medido en §2.1), no se asume 10.** Esto no es reinventar el mecanismo que e4c verificó (rellenar hacia el ancho correcto, confirmado contra el valor real de `concentradohogar`) — es la única forma de aplicar ESE MISMO mecanismo sin romper 2012 en el proceso, algo que §1.2 no podía anticipar porque se congeló antes de abrir dato alguno (tal como pedía R2). El §1 no se edita; esta es la generalización que produjo abrir el dato, documentada aquí.

Aplicado en:
- `tests/r5_1_pension_bienestar.py::procesar_ola()` — `ancho_folioviv` se deriva de la primera fila de `concentradohogar` leída; `poblacion`/`ingresos` normalizan cada `folioviv` con `.strip().zfill(ancho_folioviv)` al construir `hkey`/`pkey` (join contra `hogares`, y el `pkey` que `ingresos` usa para mirar la edad en `edad_persona`). `concentradohogar` no se toca (ya es la tabla correcta).
- `tests/p3_lca_data.py::construir_universo()` — mismo patrón, aplicado más ancho: `ancho_folioviv` se deriva de la primera fila de `concentradohogar`, y las CUATRO tablas (`concentradohogar`, `hogares`, `trabajos`, `poblacion`) normalizan con él al construir sus llaves — aquí no se dejó `concentradohogar` sin tocar como en `r5_1_pension_bienestar.py`, por simetría con las otras tres y porque `zfill` sobre un valor que ya tiene el ancho nativo es un no-op, no un riesgo. Con efecto práctico nulo hoy (2022 es la única ola que este script abre, y salió limpia en §2.1) — se aplica por consistencia y por el ajuste 2 de dirección, no porque hoy corrija algo. El campo `folioviv` que queda en cada registro de `universo` también pasa a ser el valor normalizado (antes era el crudo de `poblacion`), para que `p3_lca_run.py`/`p3_lca_stage.py` (que solo lo usan para des-duplicar hogar dentro de la misma lista, nunca para cruzar contra otra tabla — ver §0) reciban el valor canónico.

Ningún archivo de `data/raw/` se tocó. Ningún otro script del perímetro necesitaba el cambio (`p3_lca_run.py`/`p3_lca_stage.py`, ver §0).

**Test nuevo, en HEAD, pasando:**
```
TEST R5.1 ...
  2012 (ancho nativo=6): ... beneficiarios_perdidos_en_silencio=0 ...
  2014 (ancho nativo=10): ... beneficiarios_perdidos_en_silencio=0 ...
  2016 (ancho nativo=10): ... beneficiarios_perdidos_en_silencio=0 ...
  2018 (ancho nativo=10): ... beneficiarios_perdidos_en_silencio=0 ...
  2020 (ancho nativo=10): ... beneficiarios_perdidos_en_silencio=0 ...
  2022 (ancho nativo=10): ... beneficiarios_perdidos_en_silencio=0 ...
  OK -- cero hogares beneficiarios perdidos en silencio, en las seis olas.
TEST P3-LCA ... OK -- cero personas sin hogar en concentradohogar/hogares, ENIGH 2022.
test_join_folioviv.py: todos los tests pasaron.
```
2012 en cero confirma que el ancho dinámico no rompió el cruce que ya funcionaba. `tests/test_svystat.py` y `--validar` se re-corrieron después del arreglo: sin cambios (esperado — ninguno de los dos ejercita este cruce).

### 2.3 · Efecto sobre los estimandos, escala nativa (A-bis regla 3)

**R5.1 (veredicto `A`, ADR-58).** `resumen_ola()` real, corrida contra el código del commit 1 (`7525b70`, sin arreglar) y contra el código de HEAD (arreglado), para las dos olas con defecto. Advertencia de A-bis regla 4 aplicada: el universo nominal (hogares con `p65mas≥1`) es el mismo antes y después, pero la composición benef/no_benef DENTRO de ese universo cambia — cifras "antes"/"después" de la MISMA medición, no dos mediciones independientes.

| | 2016 antes | 2016 después | Δ | 2018 antes | 2018 después | Δ |
|---|---|---|---|---|---|---|
| `n_benef` (sin ponderar) | 5,913 | 8,066 | **+2,153 (+36.4%)** | 6,065 | 8,135 | **+2,070 (+34.1%)** |
| `n_benef` (ponderado) | 2,661,861 | 3,310,133 | **+648,272 (+24.4%)** | 2,705,823 | 3,329,135 | **+623,312 (+23.0%)** |
| corresidencia, benef | 44.84% [43.16,46.52] | 44.41% [42.91,45.91] | −0.43pp | 43.92% [42.38,45.45] | 43.97% [42.56,45.38] | +0.06pp |
| corresidencia, no benef | 43.23% [41.72,44.75] | 43.33% [41.68,44.98] | +0.10pp | 43.23% [41.84,44.61] | 43.09% [41.62,44.56] | −0.14pp |
| transferencia, benef | 27.17% [25.71,28.62] | 26.58% [25.27,27.89] | −0.59pp | 29.60% [28.10,31.10] | 29.10% [27.73,30.47] | −0.50pp |
| **transferencia, no benef** | **12.18% [11.20,13.17]** | **19.24% [17.93,20.56]** | **+7.06pp** | **12.66% [11.83,13.49]** | **18.49% [17.43,19.55]** | **+5.83pp** |

`corresidencia_benef`/`corresidencia_no_benef` y `transferencia_benef` apenas se mueven (IC95 se solapan ampliamente en las cuatro comparaciones) — **magnitud despreciable en esas tres proporciones**. `transferencia_no_benef` **no** es despreciable: sube 5.8–7.1 puntos porcentuales en las dos olas, y los IC95 de antes/después **no se solapan** (2016: [11.20,13.17] vs [17.93,20.56]; 2018: [11.83,13.49] vs [17.43,19.55]) — un movimiento que la propia varianza de la encuesta no explica. Mecanismo (no solo el número): bajo el cruce roto, un hogar de entidad 01–09 pierde TODAS sus filas de `ingresos` en el `hh.get()`, no solo la de clave de pensión — así que un hogar genuinamente no beneficiario en esas entidades también perdía en silencio su detección de `transferencia_mayor` (P040). El arreglo revela esas transferencias que ya estaban ahí, además de mover 2,153/2,070 hogares de `no_benef` a `benef`. Efecto compuesto sobre la brecha benef−no_benef que compara el propio falsador de R5.1 (`transferencia_benef − transferencia_no_benef`, en su misma escala nativa): **2016, 14.98pp → 7.34pp (se reduce a menos de la mitad); 2018, 16.94pp → 10.61pp (se reduce ~37%).** Este acto no dice qué significa ese cambio para el veredicto `A` — eso es adjudicación de mesa (§2.5).

**D5 (veredicto INESTABLE, ADR-53).** `p3_lca_data.py` abre exclusivamente 2022, medida limpia en §2.1 (0 filas cortas en `poblacion`, 0/0 en `n_sin_match_concentradohogar`/`n_sin_match_hogares`, antes **y** después del arreglo — confirmado por las dos corridas de `test_join_folioviv.py`, §2.0 y arriba). El arreglo es matemáticamente un no-op sobre 2022 (`zfill` de un valor que ya tiene el ancho nativo no cambia nada). **Efecto sobre D5: cero, por construcción — no hizo falta re-correr el LCA para saberlo**, tal como preveía §1.4.

Las dos escalas (puntos porcentuales de proporción para R5.1; "cero por construcción" para D5) se reportan por separado, no se combinan.

### 2.4 · Suite `--baseline`

`tests/check.py --baseline` (HEAD congelado del baseline: `2cf3e289`): **primera corrida, ROJO — 3 entradas nuevas** (no silenciado, se reporta completo, tal como exige el propio encargo):
- `T02`: `forense/notas/2026-08-12-j-join-folioviv.md` colisionaba (nombre normalizado — NFKD/ascii/minúsculas/solo alfanumérico) con `forense/encargos/2026-08-12-J-join-folioviv.md`, mismo defecto de nomenclatura que la convención de este repo ya evita en cada par encargo/nota existente (`E4a`↔`e4a-radio-celda-d`, `B-estimador-contraste`↔`estimador-contraste` — slugs deliberadamente distintos, no solo distinta mayúscula). Auto-infligido, corregido renombrando la nota a `j-alcance-folioviv.md` (este archivo).
- `T16` ×2: efecto en cascada del `T02` de arriba — el mensaje de T16 embebe el conteo total de FAIL, y el `+1` del `T02` nuevo lo corrió de "18 FAIL" a "19 FAIL" en el texto, generando una entrada "nueva" aunque el hallazgo de fondo (canon cita un conteo WARN vigente que ya no coincide) es preexistente y no lo tocó este acto.

Corregido el nombre, **segunda corrida (post-arreglo del propio arnés, no del código de R5.1/P3): VERDE — nada nuevo frente a `tests/baseline.json`.** 22 FAIL · 101 WARN (baja de 23 FAIL tras el renombre; el 18 FAIL que cita el canon en `estado-programa-v1_10.md`/`gobernanza-v1_15.md` ya estaba desincronizado de la cifra real ANTES de este acto — 18 declarado vs. 18-real-en-baseline.json más el WARN 95→101 también preexistente — no es un defecto nuevo de este acto, así que no se toca ni se corrige aquí: fuera de perímetro). Ninguna entrada de la línea base "ganó" (desapareció) por una razón distinta al propio vaivén del conteo de T02/T16 ya explicado arriba — no hubo mejora real que reportar aparte.

`tests/test_svystat.py`: verde, sin cambios (nueve casos, no tocado por este acto).

### 2.5 · Plan de remediación — PROPUESTO a mesa, no ejecutado aquí

**(i) Qué re-correr, en qué orden.** Solo `R5.1` tiene trabajo pendiente; `D5` no:
1. `python3 tests/r5_1_pension_bienestar.py` en modo de corrida oficial completa (`--estratos`, las seis olas) sobre el código ya arreglado de este PR — es la corrida que produciría el número que mesa necesitaría para re-adjudicar. Barata: la medición de este acto (dos olas, `resumen_ola` sin `--estratos`) tardó ~15s por ola; las seis olas con estratos no debería pasar de 1–2 minutos.
2. `D5`/`p3_lca_run.py` — **no requiere re-corrida.** El efecto es cero por construcción (§2.3); mesa puede cerrar este punto citando §2.1/§2.3 de esta nota, sin gastar el tiempo de cómputo del LCA (minutos, según el propio docstring del script).

**(ii) Qué veredictos quedan expuestos, y cuánto se moverían en su escala nativa.**
- `R5.1 → A` (ADR-58, con "reserva estadística escrita en la línea" ya declarada por el propio ADR — no se cita aquí de memoria, mesa la relee al adjudicar): expuesto en 2016 y 2018 únicamente. Tres de las cuatro proporciones del falsador se mueven <1pp con IC95 solapados (despreciable). La brecha `transferencia_benef − transferencia_no_benef` — la comparación que el propio falsador usa — se reduce a menos de la mitad en 2016 y ~37% en 2018, con el movimiento de `transferencia_no_benef` estadísticamente inequívoco (IC95 sin solape). Si el veredicto `A` se apoyó en la magnitud de esa brecha (no solo en su signo), esto es material; si se apoyó solo en la dirección/signo de la brecha (que no cambia: `benef` sigue por encima de `no_benef` en ambas olas, antes y después), el veredicto en sí podría sobrevivir con la reserva estadística ampliada. **Esto no lo decide este acto.**
- `D5 → INESTABLE` (ADR-53): no expuesto. Efecto cero, confirmado dos veces (§2.0 y §2.3).

**(iii) Costo estimado.** Cómputo: trivial (minutos, un solo script, sin tocar el LCA). El costo real es de **adjudicación**: una sesión de mesa que relea la reserva estadística de ADR-58, decida si la magnitud de 2.3 la satisface o la rebasa, y — si corresponde — abra una entrada fechada nueva (ADR-67 preámbulo, `gobernanza:862`: *"un sello cuyo universo creció queda VENCIDO EN ALCANCE… la anterior conservada verbatim"*) sin reescribir la línea `R5.1→A` ya sellada.

**Si la magnitud hubiera sido despreciable en las cuatro proporciones, decirlo habría sido el entregable completo.** No lo fue en una de las cuatro (`transferencia_no_benef`) — decir CUÁL, con qué IC95 y por qué mecanismo, es el entregable en su lugar.

---

## §2.6 · Addendum post-rebase (no edita §1 ni §2 de arriba)

Al rebasar sobre `origin/main` fresco para el cierre, `origin/main` había avanzado de `3e071f0` a `0c4d52a` (18 commits) — entre ellos, **ADR-71(c)** (`canon/gobernanza-v1_15.md:928`, sellado 12/ago/2026 por el ACTO M-6, mismo día, acto distinto): *"Se autoriza medir el alcance del defecto de `folioviv`, sin comprometer reapertura."* M-6 verificó de primera mano, independientemente y por su cuenta, el mismo mecanismo que §0/§1 de esta nota describen — `hogares.get(hkey)` + `continue` silencioso en `r5_1_pension_bienestar.py:165-168`; `grep -rn "zfill\|rjust(10" tests/ tools/` = 0 antes de este acto; `p3_lca_data.py:131,136,155` cruza por la misma llave; `validar_contra_publicado()` nunca ejercita el join — y declaró explícitamente: *"Ningún veredicto se reabre por este ADR: `R5.1 → A` (ADR-58) y `D5 — INESTABLE` (ADR-53) siguen vigentes hasta que exista magnitud medida y mesa adjudique en acto propio."* Esa magnitud es exactamente lo que produce el §2 de esta nota. ADR-71(c) también sella, para este caso específico, la misma regla de vencimiento-en-alcance que §2.5(iii) ya citaba de ADR-67: *"Una entrada fechada posterior vence en alcance a la anterior, la anterior se conserva verbatim, y la nueva lo dice en su propia línea."* No hay contradicción ni duplicación de trabajo — M-6 autorizó y verificó el mecanismo antes del dato; este acto midió la magnitud después. El gate de PASO 1 (intersección con `origin/e4c/r5-1-d2`) se re-corrió tras el rebase: sigue vacío. Ningún archivo del perímetro de este acto fue tocado por los 18 commits de por medio.
