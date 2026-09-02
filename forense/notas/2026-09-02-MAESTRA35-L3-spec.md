# `ACTO MAESTRA35-L3` — spec congelada (COMMIT-1 del lote, D-11)

Bloque `B-bis` / `A-bis` de `instrucciones-proyecto-v2_12.md`: este archivo se
escribe **antes** de calcular una sola cifra sobre el panel ampliado. El commit
que lo crea no toca ningún archivo de resultados. Lo que produzca el
procedimiento se **añade** después, en un segundo commit, sin editar nada de lo
que está aquí.

Hereda **verbatim** las secciones `§1.1`, `§1.2`, `§1.3`, `§1.4`, `§1.6`, `§1.7`
y `§1.10` de `forense/notas/2026-09-02-MAESTRA34-L6-P2-spec.md`, con la **única
sustitución de `§1.5`**, que es la firma **`c1`** de mesa (2/sep/2026):
«sustituir la tendencia lineal por un efecto fijo de TIPO de año federal
(presidencial / intermedia / sin federal)».

---

## §0 · Premisas

### 0.1 · De dónde sale el tratamiento

De `data/p0-calendario-ayuntamientos-v1_0.tsv` y
`data/p0-tratamiento-homologacion-v1_0.tsv`, **sin editarlas** (el encargo lo
prohíbe expresamente y este acto no las tocó). El tipo de año federal se deriva
de esas mismas tablas más el hecho constitucional del ciclo federal: **2018 y
2024 presidenciales, 2015 y 2021 intermedias**. La derivación completa, por
entidad y transición, está congelada en `data/l3-tabla-identificacion-v1_0.tsv`
(**73 transiciones, 32 entidades**), escrita en el commit de `P0`, **antes** de
este archivo y antes de cualquier adquisición.

### 0.2 · Contaminación declarada (`ADR-46`), antes de medir y no después

La sesión que congela esta spec **ya vio** lo siguiente:

1. **Los resultados completos de `MAESTRA34-L6`**, que están publicados en el
   repo (`§2`-`§12` de su spec) y que el encargo **ordena** usar: el `β` pooled
   `+0.0149` con IC95 `[−3.3765, +3.4064]`, los dos `ATT` por cohorte
   (`g2018 = +2.4113`, `g2021 = −5.6914`), la `γ` `−0.2692`, la tabla de
   participación agregada de Coahuila / Nayarit / Zacatecas / Durango y las
   `Δ` medias por transición. **No hay ceguera posible sobre el panel de `L6`**:
   es material publicado y el control de regresión de `P2` consiste
   precisamente en reproducirlo. Se declara y no se rodea.
2. **La hipótesis a falsar viene firmada por mesa, no elegida por el ejecutor.**
   El encargo fija, verbatim, que la lectura no refutada de `L6` es «concurrir
   con presidencial SUBE, concurrir con intermedia BAJA», y fija las cuatro
   ramas del veredicto. El signo esperado estaba escrito **antes** de que esta
   sesión abriera un solo archivo nuevo.
3. **Zacatecas 2016**: al identificar la tabla HTML del IEEZ, la sesión vio las
   **dos primeras filas municipales** —`APOZOL` (`LN = 5408`) y `APULCO`
   (`LN = 4278`), con sus columnas de partido—. Conoce por tanto, en dos de los
   58 municipios, lo suficiente para formar una participación de 2016.
4. **Hidalgo**: las primeras ~8 filas por casilla de una hoja de 2020 (`ACATLÁN`)
   y de un municipio de 2024 (`CHAPULHUACÁN`). Son **votos por casilla suelta,
   sin lista nominal**, y Hidalgo queda fuera del universo por `§1.3`.
5. **El preámbulo del PREP federal 2024**: los agregados nacionales de la
   elección presidencial (`ACTAS_ESPERADAS = 170648`,
   `PORCENTAJE_ACTAS_CAPTURADAS = 95.2352`, y la última cifra del renglón,
   `60.9253`). Son cifras **federales y nacionales**; el desenlace de esta spec
   es **municipal y local**.
6. **De Baja California** —la entidad de mayor rendimiento del censo— la sesión
   vio **únicamente las cabeceras** (fila 6) de los cuatro archivos y el conteo
   de filas. **Ninguna fila de datos.**

**No se ha calculado ninguna participación, ninguna diferencia, ningún `ATT` y
ningún intervalo sobre ninguna entidad nueva antes de este commit.**

### 0.3 · La reserva de identificación, escrita antes de medir

`P0` de este acto midió, sobre las 73 transiciones del calendario, que bajo el
modelo de `§1.5` sólo **5** son `STAY` (mismo tipo de año federal en las dos
patas) y por tanto sólo esas identifican `α` sin mezcla. El panel de `L6`
contiene **una sola** (Durango 2016→2019, y en **un** municipio).

Consecuencia, aceptada aquí y no rodeada, con el umbral que el encargo fija:
**si al cierre de `P1` las transiciones `STAY` del panel son menos de 3, `α` se
declara identificada con reserva y se reporta también la variante sin `α`.** La
variante sin `α` se reporta **pase lo que pase**, porque es el único modo de
enseñar cuánto de `β_pres` y `β_int` depende de extrapolar una deriva anual
estimada de casi nada.

### 0.4 · Alcance, declarado como falta

El encargo fija una **meta declarada, no compuerta**, de **≥ 8 entidades
tratadas medibles**. `L6` alcanzó **2**. Lo que `P1` alcance se declara en `P2`
con nombre y apellido de cada entidad que faltó y por qué; si no llega a 8,
**`P2` corre y se declara ACOTADO**, sin sustituir el faltante por ninguna
imputación.

---

## §1 · Spec

### 1.1 · Estimando *(verbatim de `L6 §1.1`, con el estimando de `c1`)*

Efecto de que la elección municipal se celebre el mismo día que la elección
federal sobre la **participación electoral municipal**, medido en **puntos
porcentuales**, **separado por el TIPO de boleta federal que se comparte**
(presidencial / intermedia). Escala declarada: **pp**. No es una probabilidad y
no puede cargarse al motor tal cual.

### 1.2 · Unidad y desenlace *(verbatim de `L6 §1.2`)*

Unidad de observación: **municipio × elección de ayuntamiento**.

```
participacion(m, e) = 100 * votos_totales(m, e) / lista_nominal(m, e)
```

`votos_totales` = votación total emitida, **incluyendo** nulos y candidaturas no
registradas (es la definición que `MAESTRA34-L4` usó y la que las tablas de los
OPLE publican como «TOTAL»). `lista_nominal` = lista nominal del municipio en esa
elección, tomada de la **misma fuente** que los votos siempre que la fuente la
traiga, y del listado nominal oficial del propio OPLE cuando la tabla de
cómputos no la traiga (caso Nayarit).

### 1.3 · Universo *(verbatim de `L6 §1.3`)*

Los municipios de las entidades cuya serie de `P1` trae lista nominal en la
fuente, presentes con `lista_nominal > 0` **en todas** las elecciones de la serie
de su entidad.

Exclusiones declaradas:

- **Usos y costumbres (Oaxaca): NO-APLICA con conteo.** Si Oaxaca no entra al
  universo, la exclusión se declara **satisfecha por vacío, no por filtro**, con
  el conteo `0`; si entra, se aplica como **filtro** y se declara el número de
  municipios excluidos.
- Filas que no son municipios (agregados estatales, votos del extranjero, notas
  al pie): se excluyen **nombrándolas una por una** y se comprueba
  aritméticamente que la suma de los municipios más las filas excluidas
  reproduce el total que publica el organismo. Es el control que `L4` fijó.
- Municipio ausente de alguno de los años de su serie: se excluye de **todas**
  las transiciones de esa entidad, y se cuenta.

### 1.4 · Tratamiento *(verbatim de `L6 §1.4`)*

`D(m, e) = 1` si la jornada de la elección `e` se celebró el mismo día que la
jornada federal; `0` si no. Se lee de
`data/p0-calendario-ayuntamientos-v1_0.tsv`, columna
`concurrente_con_federal`, que ya incorpora la excepción documentada de Chiapas
2015 y la verificación A.13 de que no hay otras.

### 1.5 · Estimador principal — **LA ÚNICA SUSTITUCIÓN (firma `c1`)**

Sustituye la tendencia lineal única de `L6` por un **efecto fijo de TIPO de año
federal**. Para cada entidad `s` y cada par de elecciones **consecutivas**
`e_k → e_{k+1}`:

```
Δy(m,k)      = participacion(m, e_{k+1}) − participacion(m, e_k)          [pp]
hueco(k)     = anio(e_{k+1}) − anio(e_k)                                  [años]
D_pres(e)    = 1 si la jornada de e coincide con una federal PRESIDENCIAL (2018, 2024)
D_int(e)     = 1 si coincide con una federal INTERMEDIA (2015, 2021)
ΔD_pres(k)   = D_pres(e_{k+1}) − D_pres(e_k) ; ΔD_int(k) análogo          ∈ {−1, 0, +1}

Δy(m,k) = α·hueco(k) + β_pres·ΔD_pres(k) + β_int·ΔD_int(k) + ε(m,k)
```

Regresión a nivel **municipio**, por mínimos cuadrados **sin intercepto** (con
`hueco = 0` no hay diferencia que explicar), sobre **todas** las transiciones del
universo.

**Referencia = elección local sin federal.**

`α` se identifica **sólo** por transiciones sin cambio de tipo (`STAY`:
no-fed→no-fed, pres→pres, int→int). `β_pres` y `β_int` por los `SWITCH` de las
cohortes tratadas. Y **las entidades siempre concurrentes
(pres→int→pres) identifican `β_int − β_pres`** y, sumando sus dos transiciones,
**`6α`**. Cuáles hay en el universo está contado en
`data/l3-tabla-identificacion-v1_0.tsv` y transcrito en `§0.3`: **5 `STAY`,
9 `β_pres`, 5 `β_int`, 54 `β_pres − β_int`**.

**Lo que este modelo NO separa, dicho antes:** un choque específico de 2021 (la
pandemia) queda **dentro** de `β_int` si 2021 es la única intermedia de la
ventana con elecciones municipales concurrentes. Se reporta y **no se corrige
después de ver el número**.

### 1.6 · Errores estándar *(verbatim de `L6 §1.6`, con el nº de conglomerados abierto)*

Agrupados por **entidad**. Con pocos conglomerados la aproximación asintótica no
aplica: el intervalo principal se calcula por **bootstrap wild cluster** con
pesos de Rademacher sobre las entidades, `B = 10 000`, `seed = 42`, y se reporta
**también** el bootstrap por municipio con reemplazo (`B = 10 000`, `seed = 42`)
como intervalo de contraste. **El intervalo que decide el falsador es el wild
cluster por entidad**, por ser el conservador; si los dos discrepan en si cruzan
cero, se reporta la discrepancia y manda el wild cluster.

**Restricción bajo `H₀`, escrita antes:** el bootstrap wild cluster de cada
coeficiente se calcula con los residuos del modelo **restringido a que ese
coeficiente sea 0**, dejando los otros dos libres (Cameron–Gelbach–Miller), que
es el mismo procedimiento que `tools/l6_estimador_concurrencia.py` implementa
para su `β` único. Para el contraste `β_int − β_pres`, la restricción es
`β_int = β_pres`.

**Límite mecánico del test, con el `k` real:** con `k` entidades el wild cluster
de Rademacher tiene `2^k` patrones de signo y el **p-valor mínimo alcanzable es
`2/2^k`**. Se escribe con el `k` que quede al cierre de `P1` y se verifica cuántos
valores distintos de coeficiente producen esos patrones, igual que `L6` hizo.

### 1.7 · Diagnósticos pre-registrados *(verbatim de `L6 §1.7`, con los dos parámetros)*

1. **`ATT` por cohorte**: el efecto estimado por separado para cada cohorte de
   adopción presente en el panel, cada uno contra la `α` común estimada **sólo**
   de las transiciones `STAY`.
2. **El contraste que `L4` no podía hacer**: `β_int − β_pres`, con su IC. Bajo el
   modelo de `§1.5` este contraste está identificado **también** por las
   entidades siempre concurrentes, que `L6` no podía usar.
3. **Event-study por año relativo al tratamiento**, con las pre-transiciones
   disponibles como diagnóstico de pre-tendencia, declarando de antemano su
   debilidad si las `STAY` son pocas.
4. **Heterogeneidad por tamaño**: terciles de `lista_nominal` del municipio en su
   primera elección de la serie. Se reportan los coeficientes por tercil.
5. **Sensibilidad**: (a) sin la transición de hueco 1 (Coahuila 2017→2018);
   (b) **sin Coahuila** (el encargo la pide por nombre: `L6` midió que sin ella
   el pooled cae a `−5.69`); (c) sin Durango.
6. **Controles aritméticos** (ninguno es opcional; si alguno falla se reporta el
   fallo **antes** que el resultado):
   - reagregar casilla por casilla reproduce la tabla por municipio, con
     `|Δvotos| = 0` y `|Δlista nominal| = 0`, donde existan las dos tablas;
   - donde la fuente publique `% PART`, la participación recalculada coincide con
     la publicada (diferencia máxima reportada);
   - ninguna participación fuera de `(0, 100]`;
   - la suma de municipios más las filas excluidas reproduce el total publicado.
7. **Control de regresión sobre `L6`** (añadido por el encargo): antes de correr
   nada nuevo, se re-ejecuta `tools/l6_estimador_concurrencia.py` sobre el panel
   de `L6` y se exige que reproduzca `data/l6-resultados-concurrencia-v1_0.json`
   **byte a byte**. **PARO si no coincide.**

### 1.8 · Comparaciones

Contra `MAESTRA34-L4` (`+10.4790 pp`, IC95 `[+9.6890, +11.2652]`, n=163, diseño
**entre años** Coahuila+Edomex 2023→2024), misma escala: se reporta **cuánto de
ese `Δ` explica cada componente** (`α·hueco`, `β_pres`, `β_int`). Contra los
benchmarks de la firma `DC1`: Alemania **≈10 pp** (Leininger, Rudolph y Zittlau,
PSRM 2018) y EE.UU. **36 pp** (Hajnal y Lewis 2003). El benchmark del TEPJF
(1991-2018) **sólo si mesa lo depositó**; si sigue `NO-OBTENIDO`, **no se cita de
memoria**.

### 1.9 · Falsador `B-bis`, verbatim del encargo

Sobre los **IC95 wild cluster por entidad** (manda el conservador; si discrepa
con el de municipio, se reporta). La hipótesis que `L6` dejó como lectura no
refutada es **«concurrir con presidencial SUBE, concurrir con intermedia BAJA»**:

- **CORROBORADA** si `β_pres > 0` con IC que excluye 0 **Y** `β_int < 0` con IC
  que excluye 0;
- **ACOTADA** si sólo una de las dos se sostiene (se dice cuál);
- **NO-DISCRIMINA** si ambos IC contienen 0 — entonces la participación municipal
  no responde al tipo de boleta federal, y el vaivén de Zacatecas
  `64.7 → 50.7 → 59.4` queda **sin explicar por este diseño**;
- **CONTRARIA** si alguno sale con signo opuesto e IC fuera de 0.

**Precedencia: `CONTRARIA` manda sobre `ACOTADA`.**

**Y lo que significa corroborar, dicho antes:** sería el primer dato mexicano que
sostenga «lo que mueve la participación municipal es **qué trae** la boleta
federal, no **compartirla**» — una regla cívica nueva,
`civico.participacion.tipo_boleta_federal`, con **dos disparadores**
(presidencial / intermedia) y **signo opuesto**, que mesa decidiría si entra a
Ola 5 como regla ACTIVA. Este acto **no** la carga al motor.

### 1.10 · Lo que este procedimiento no puede decir, dicho antes *(verbatim de `L6 §1.10`, ampliado)*

- No separa concurrencia de **jerarquía del cargo**: en las transiciones tratadas
  el cargo municipal es el mismo a ambos lados, pero la boleta federal que se le
  suma no lo es.
- No separa el tipo de boleta federal de **cualquier choque nacional** que
  coincida exactamente con los años de ese tipo. En particular: **2021 es, en
  esta ventana, a la vez la intermedia y la elección de la pandemia**. `β_int`
  carga las dos cosas y este diseño no las separa.
- `α` se estima de muy pocas transiciones (`§0.3`) y todo lo que dependa de
  extrapolar la deriva a huecos largos hereda esa fragilidad. Por eso la variante
  sin `α` se reporta siempre.
- Con pocos conglomerados, cualquier intervalo es frágil; se usa el estimador
  conservador y se dice.

### 1.11 · Sello

**El primer resultado que produzca este procedimiento es el que se reporta.**

---
---

# `P2` — RESULTADOS (COMMIT-2)

Añadido en un segundo commit. **Nada de lo escrito arriba se ha editado.** El
procedimiento corrió una vez, tal como está congelado, y lo que sigue es lo que
produjo. Script: `tools/mide_participacion_tipo_boleta.py` (hermano nuevo; **no
toca** `tools/l6_estimador_concurrencia.py` ni `tools/l6_lectores.py`, que
importa). Salida cruda: `data/l3-resultados-tipo-boleta-v1_0.json`.

## §2 · El control de regresión, antes de todo (`§1.7.7`)

```
$ python3 tools/mide_participacion_tipo_boleta.py --control-l6
{ "identico_byte_a_byte": true,
  "sha256_recorrida":  "8054034f4d0eca5378f0d2c8994e4587e7334472fa9da8cb38552e2cc11e9b8c",
  "sha256_archivada":  "8054034f4d0eca5378f0d2c8994e4587e7334472fa9da8cb38552e2cc11e9b8c",
  "bytes_recorrida": 8793, "bytes_archivada": 8793, "PARO": false }
```

El estimador de `MAESTRA34-L6` reproduce `data/l6-resultados-concurrencia-v1_0.json`
**byte a byte**. No hay `PARO`. La corrida de `L6` queda intacta y comparable.

## §3 · El panel que quedó

**187 municipios · 540 observaciones municipio × transición · 15 transiciones ·
6 entidades.** `L6` tenía 116 municipios, 269 observaciones, 8 transiciones y 4
entidades.

| entidad | municipios | serie | de las cuales |
|---|---:|---|---|
| Chihuahua | **66** | 2016, 2018, 2021, 2024 | **nueva en `L3`** |
| Zacatecas | 58 | **2016**, 2018, 2021, 2024 | la pata **2016** es nueva en `L3` |
| Coahuila | 38 | 2017, 2018, 2021, 2024 | de `L6` |
| Nayarit | 19 | 2017, 2021, 2024 | de `L6` |
| Baja California | **5** | 2016, 2019, 2021, 2024 | **nueva en `L3`** |
| Durango | 1 | 2016, 2019 | de `L6` |

**Entidades tratadas medibles: 2 → 5** (Coahuila, Nayarit, Zacatecas, Baja
California, Chihuahua). La meta declarada del encargo era **≥ 8**. **No se
alcanzó: `P3` corre y se declara ACOTADO**, con las entidades faltantes
nombradas una por una en la nota de cierre y en la cola.

**Municipios perdidos por la regla de `§1.3`, nombrados y contados:**

* **`LA YESCA`** (Nayarit) — heredado de `L6`: elección extraordinaria en 2021.
* **`SAN FELIPE`** y **`SAN QUINTÍN`** (Baja California) — municipios **creados
  después** de 2016; sólo existen en 2024. No es dato faltante: no existían.
* **`OCAMPO`** (Chihuahua) — presente en 2016, 2018 y 2021 y **ausente de 2024**.
  Verificado en la fuente: sus **23** filas de 2024 traen lista nominal pero
  **ninguna cifra de votos**.
* **38 de los 39 municipios de Durango** — heredado de `L6`: el archivo de 2016
  del IEPC cubre sólo el municipio de Durango.

Ninguno se imputó. **Ninguna participación cayó fuera de `(0, 100]`: 0 casos en
las 540 observaciones.**

## §4 · Los controles de `§1.7.6`, corridos antes de mirar el estimador

| control | resultado |
|---|---|
| **Zacatecas 2016**, reagregar casilla → municipio contra la tabla por municipio que publica el mismo IEEZ | **58/58 municipios, `max|Δ lista nominal| = 0.0`**, ninguno sobra ni falta en ninguno de los dos lados |
| **Zacatecas 2016**, identidad `TOTAL / LN` contra el `% PARTICIPACIÓN` publicado | **`max|Δ| = 0.0 pp` en 2 520 casillas** |
| **Baja California 2016**, identidad contra `% DE PARTICIP.` | `max|Δ| = 0.0 pp` en 4 439 casillas (5 hojas) |
| **Baja California 2019 / 2024** | `0.0100 pp` (4 772) · `1.4e-14 pp` (5 350) |
| **Baja California 2021** | `0.2779 pp` en 4 931 — y son **exactamente 2 casillas**: `TIJUANA` s.2016 C2 y `ROSARITO` s.1295 C4, donde el `%` publicado viene **redondeado a dos decimales**. No es un dato malo |
| **Chihuahua 2018**, identidad contra `% de Particip.` | `1.4e-14 pp` en 5 265 casillas |
| **Chihuahua 2016**, identidad contra `% de Particip.` | **`78.78 pp` — FALLA, y se reporta antes que el resultado** (`§5`) |
| **Chihuahua 2021 / 2024** | la fuente **no publica** `%` en esas hojas: el control no se puede correr y se dice, en vez de darlo por bueno |
| participación fuera de `(0, 100]` | **0 municipios** en las 540 observaciones |

### El defecto de fuente que el control atrapó

**Chihuahua 2016, `JUÁREZ`, sección 2186, casilla C1: la fuente publica
`Votación Total = 3` con `Listado Nominal = 377` y `% de Particip. = 79.576`.**
79.576 % de 377 son **300**, no 3: es un dígito perdido en el archivo del IEECH.
Es **1 casilla de 5 125**.

**No se repara.** La spec define la participación sobre `votos_totales` de la
fuente y este acto no cambia el procedimiento después de ver el número. Lo que
sí se hace es **cuantificar el daño**, que es lo que el control existe para
permitir:

| | |
|---|---|
| Juárez 2016 tal como lo publica la fuente | 427 720 / 1 023 228 = **41.8010 %** |
| Juárez 2016 reparando esa sola casilla | 428 017 / 1 023 228 = **41.8301 %** |
| efecto sobre Juárez | **+0.0290 pp** |
| efecto sobre la `Δy` **media municipal** de Chihuahua 2016→2018 (66 municipios, sin ponderar) | **+0.00044 pp** |

El defecto es real y es irrelevante para el estimando. Las dos cosas se dicen.

### Casillas sin denominador, clasificadas una por una

| año | sin votos **ni** lista nominal (casilla no instalada) | con votos y **sin** lista nominal (casilla especial) | con lista nominal y **sin** votos |
|---|---:|---:|---:|
| Chihuahua 2016 | 70 | **31** (2 411 votos) | 0 |
| Chihuahua 2018 | 66 | **32** (1 530 votos) | 0 |
| Chihuahua 2021 | 0 | 0 | 1 |
| Chihuahua 2024 | 0 | 0 | **23** (todas de `OCAMPO`) |

Las casillas **especiales** no tienen lista nominal por construcción, así que sus
votos quedan fuera del numerador igual que del denominador. Afecta a 2016 y 2018
de forma simétrica (31 y 32 casillas), que son justamente los dos extremos de la
transición que identifica `β_pres` en Chihuahua.

## §5 · Participación observada, agregada por entidad

| entidad | año | tipo de boleta federal | participación agregada | n |
|---|---:|---|---:|---:|
| Baja California | 2016 | sin federal | **32.42** | 5 |
| Baja California | 2019 | sin federal | **29.75** | 5 |
| Baja California | 2021 | intermedia | **38.11** | 5 |
| Baja California | 2024 | **presidencial** | **46.78** | 5 |
| Chihuahua | 2016 | sin federal | 48.77 | 66 |
| Chihuahua | 2018 | **presidencial** | 53.79 | 66 |
| Chihuahua | 2021 | intermedia | 46.52 | 66 |
| Chihuahua | 2024 | **presidencial** | 52.25 | 66 |
| Coahuila | 2017 | sin federal | 57.05 | 38 |
| Coahuila | 2018 | **presidencial** | 60.36 | 38 |
| Coahuila | 2021 | intermedia | 57.58 | 38 |
| Coahuila | 2024 | **presidencial** | 64.65 | 38 |
| Nayarit | 2017 | sin federal | 60.94 | 19 |
| Nayarit | 2021 | intermedia | 52.36 | 19 |
| Nayarit | 2024 | **presidencial** | 55.67 | 19 |
| Zacatecas | 2016 | sin federal | 61.14 | 58 |
| Zacatecas | 2018 | **presidencial** | 64.74 | 58 |
| Zacatecas | 2021 | intermedia | 50.68 | 58 |
| Zacatecas | 2024 | **presidencial** | 59.39 | 58 |
| Durango | 2016 | sin federal | 57.12 | 1 |
| Durango | 2019 | sin federal | 41.67 | 1 |

## §6 · El estimador de `§1.5`

```
Δy(m,k) = α·hueco(k) + β_pres·ΔD_pres(k) + β_int·ΔD_int(k)
```

| | punto | **IC95 wild cluster por entidad** (el que decide) | IC95 bootstrap por municipio | p (wild) |
|---|---:|---|---|---:|
| **`α`** (deriva) | **−0.4447 pp/año** | **[−1.1828, +0.2934]** | [−0.6598, −0.2212] | 0.3151 |
| **`β_pres`** | **+3.1542 pp** | **[−0.1957, +6.5040]** | [+2.4755, +3.8315] | 0.1577 |
| **`β_int`** | **−0.9229 pp** | **[−3.7769, +1.9311]** | [−1.7652, −0.0575] | 0.6704 |
| **`β_int − β_pres`** | **−4.0771 pp** | **[−8.1622, +0.0081]** | [−4.7332, −3.4202] | 0.0920 |

`n = 540` observaciones, 15 transiciones, **6 conglomerados**.

**El límite mecánico del test, con el `k` real.** Con `k = 6` entidades el
bootstrap wild cluster de Rademacher tiene `2⁶ = 64` patrones de signo, y se
verificó que producen **64 valores distintos** del estadístico: el **p mínimo
alcanzable es `2/64 = 0.03125`**. **Esta vez el test sí podía rechazar al 5 %** —
en `L6`, con 4 conglomerados, el mínimo era `0.125` y no podía pasara lo que
pasara. Podía, y no rechazó.

**Variante sin `α`** (`§0.3`, se reporta pase lo que pase porque el panel tiene
**2** transiciones `STAY`, menos que las 3 del umbral):

| | |
|---|---:|
| `β_pres` sin `α` | **+2.2595 pp** |
| `β_int` sin `α` | **−1.7766 pp** |

## §7 · Qué identifica qué, en el panel real

| identifica | transiciones | obs. |
|---|---|---:|
| **`α`** (`STAY`) | Baja California 2016→2019 · Durango 2016→2019 | **6** |
| **`β_pres`** solo | Chihuahua 2016→2018 · Coahuila 2017→2018 · Zacatecas 2016→2018 | 162 |
| **`β_int`** solo | Baja California 2019→2021 · Nayarit 2017→2021 | **24** |
| **`β_pres − β_int`** | 8 transiciones (Coahuila ×2, Zacatecas ×2, Chihuahua ×2, Nayarit, Baja California) | 348 |

**`α` sigue siendo el parámetro frágil, y ahora se ve cuánto.** Estimada **sólo**
de las 2 transiciones `STAY` da **−1.8436 pp/año**; estimada conjuntamente con
todo el panel da **−0.4447**. Las 6 observaciones que la identifican en solitario
son 5 municipios de Baja California y **1** de Durango.

## §8 · `Δy` media municipal, transición por transición

| entidad | transición | h | tipo → tipo | ΔD_p | ΔD_i | n | Δy media |
|---|---|---:|---|---:|---:|---:|---:|
| Coahuila | 2017→2018 | 1 | sin fed → **presidencial** | +1 | 0 | 38 | **+2.142** |
| Zacatecas | 2016→2018 | 2 | sin fed → **presidencial** | +1 | 0 | 58 | **+2.522** |
| Chihuahua | 2016→2018 | 2 | sin fed → **presidencial** | +1 | 0 | 66 | **+2.823** |
| Nayarit | 2017→2021 | 4 | sin fed → intermedia | 0 | +1 | 19 | **−6.768** |
| Baja California | 2019→2021 | 2 | sin fed → intermedia | 0 | +1 | 5 | **+7.597** |
| Coahuila | 2018→2021 | 3 | presidencial → intermedia | −1 | +1 | 38 | +1.907 |
| Zacatecas | 2018→2021 | 3 | presidencial → intermedia | −1 | +1 | 58 | −12.487 |
| Chihuahua | 2018→2021 | 3 | presidencial → intermedia | −1 | +1 | 66 | −2.650 |
| Coahuila | 2021→2024 | 3 | intermedia → presidencial | +1 | −1 | 38 | +2.053 |
| Nayarit | 2021→2024 | 3 | intermedia → presidencial | +1 | −1 | 19 | +2.007 |
| Zacatecas | 2021→2024 | 3 | intermedia → presidencial | +1 | −1 | 58 | +6.550 |
| Baja California | 2021→2024 | 3 | intermedia → presidencial | +1 | −1 | 5 | +8.296 |
| Chihuahua | 2021→2024 | 3 | intermedia → presidencial | +1 | −1 | 66 | −0.116 |
| Baja California | 2016→2019 | 3 | sin fed → sin fed (`STAY`) | 0 | 0 | 5 | −3.548 |
| Durango | 2016→2019 | 3 | sin fed → sin fed (`STAY`) | 0 | 0 | 1 | −15.444 |

**Lo que esta tabla enseña sin ningún modelo:** las **tres** transiciones de
«local sola → presidencial» dan **+2.14, +2.52 y +2.82** — tres entidades
distintas, tres años de partida distintos, el mismo signo y casi la misma
magnitud. Las **dos** de «local sola → intermedia» dan **−6.77 y +7.60**: signos
opuestos. Ahí está, en crudo, por qué `β_pres` sale estable y `β_int` no.

## §9 · `ATT` por transición (`§1.7.1`), contra la `α` de las `STAY`

`α` de las `STAY` = **−1.8436 pp/año** (6 obs.). Con esa referencia, **los 13
`ATT` de transiciones `SWITCH` son positivos salvo uno**:

| transición | Δ bruto | h | ΔD_p | ΔD_i | **ATT** | n |
|---|---:|---:|---:|---:|---:|---:|
| Baja California 2021→2024 | +8.296 | 3 | +1 | −1 | **+13.827** | 5 |
| Zacatecas 2021→2024 | +6.550 | 3 | +1 | −1 | **+12.081** | 58 |
| Baja California 2019→2021 | +7.597 | 2 | 0 | +1 | **+11.284** | 5 |
| Coahuila 2021→2024 | +2.053 | 3 | +1 | −1 | +7.584 | 38 |
| Nayarit 2021→2024 | +2.007 | 3 | +1 | −1 | +7.537 | 19 |
| Coahuila 2018→2021 | +1.907 | 3 | −1 | +1 | +7.437 | 38 |
| Chihuahua 2016→2018 | +2.823 | 2 | +1 | 0 | +6.510 | 66 |
| Zacatecas 2016→2018 | +2.522 | 2 | +1 | 0 | +6.209 | 58 |
| Chihuahua 2021→2024 | −0.116 | 3 | +1 | −1 | +5.414 | 66 |
| Coahuila 2017→2018 | +2.142 | 1 | +1 | 0 | +3.986 | 38 |
| Chihuahua 2018→2021 | −2.650 | 3 | −1 | +1 | +2.880 | 66 |
| Nayarit 2017→2021 | −6.768 | 4 | 0 | +1 | +0.606 | 19 |
| **Zacatecas 2018→2021** | −12.487 | 3 | −1 | +1 | **−6.957** | 58 |

Que casi todos salgan positivos **no** es evidencia de concurrencia: es la señal
de que la `α` de las `STAY` (**−1.84 pp/año**) es demasiado negativa, porque está
estimada de 6 observaciones, una de ellas un municipio suelto de Durango que cae
**−15.4 pp** en tres años. Se dice aquí, no en la conclusión.

## §10 · Heterogeneidad y sensibilidad (`§1.7.4`, `§1.7.5`)

| corte (terciles de lista nominal: 6 141 / 20 513) | `α` | `β_pres` | `β_int` | n |
|---|---:|---:|---:|---:|
| municipios chicos | −0.565 | **+3.524** | +1.926 | 189 |
| medianos | −0.597 | **+3.085** | −1.915 | 178 |
| grandes | −0.210 | **+3.448** | −2.287 | 173 |

| sensibilidad | `α` | `β_pres` | `β_int` | n | entidades |
|---|---:|---:|---:|---:|---:|
| **completo** | −0.445 | **+3.154** | −0.923 | 540 | 6 |
| sin la transición de hueco 1 (Coahuila 2017→2018) | −0.453 | **+3.321** | −0.767 | 502 | 6 |
| **sin Coahuila** (la que el encargo pide por nombre) | −0.767 | **+4.204** | −0.971 | 426 | 5 |
| sin Durango | −0.432 | **+3.128** | −0.948 | 539 | 5 |
| sólo el panel de `L6` | −0.475 | **+2.761** | −2.978 | 327 | 4 |
| sólo las entidades nuevas de `L3` | −0.389 | **+4.033** | **+2.675** | 213 | 2 |

**La respuesta directa a lo que el encargo pregunta.** `L6` midió que quitando
Coahuila su `β` pooled se desplomaba a **−5.69**. Bajo el modelo de `c1`, quitar
Coahuila **no desploma nada**: `β_pres` pasa de `+3.15` a `+4.20` y `β_int` de
`−0.92` a `−0.97`. **La inestabilidad que `L6` encontró era un artefacto de su
especificación de un solo `β`**, que promediaba dos efectos de signo contrario;
al separarlos, la sensibilidad desaparece. Ése es, medido, el rendimiento de la
corrección `c1`.

**`β_pres` es estable en las seis columnas: `+2.76` a `+4.20`, siempre positivo.
`β_int` cambia de signo entre subconjuntos: `−2.98` en el panel de `L6`, `+2.67`
en las entidades nuevas.**

## §11 · Cuánto del `Δ` de `MAESTRA34-L4` explica cada componente (`§1.8`)

`L4` midió **+10.4790 pp** entre la local **no concurrente** de 2023 y la local
**concurrente con presidencial** de 2024 — `hueco = 1`, `ΔD_pres = +1`,
`ΔD_int = 0`. Este modelo predice para exactamente esa transición:

| componente | pp |
|---|---:|
| `α × hueco` = −0.4447 × 1 | **−0.445** |
| `β_pres` | **+3.154** |
| **suma explicada** | **+2.709** |
| **`Δ` de `L4`** | **+10.479** |
| **resto no explicado por este diseño** | **+7.770 (74.1 %)** |

**El modelo del tipo de boleta explica alrededor de una cuarta parte del `+10.48`
de `L4`.** El resto no queda identificado por este diseño y **no** se le puede
llamar «efecto de año» sin más: es lo que este procedimiento no separa.

## §12 · Veredicto del falsador `B-bis` (`§1.9`)

La spec designó **el IC95 wild cluster por entidad** para decidir, por ser el
conservador.

* `β_pres = +3.1542`, IC95 **[−0.1957, +6.5040]** → **contiene 0**
* `β_int = −0.9229`, IC95 **[−3.7769, +1.9311]** → **contiene 0**

> ### **`NO-DISCRIMINA`.**

Es la tercera rama del falsador, aplicada literalmente: **ambos intervalos
contienen 0**. Con el vocabulario que la propia spec fijó antes de medir: en este
panel **la participación municipal no responde, con evidencia que este test pueda
distinguir de cero, al tipo de boleta federal**, y **el vaivén de Zacatecas
`64.7 → 50.7 → 59.4` queda sin explicar por este diseño**.

**La discrepancia entre los dos intervalos, que la spec obliga a reportar.** El
bootstrap por municipio da `β_pres` **[+2.4755, +3.8315]** y `β_int`
**[−1.7652, −0.0575]**: los dos **excluyen 0** y **los dos apuntan en la
dirección de la hipótesis** (presidencial sube, intermedia baja). Ese intervalo
llevaría a `CORROBORADA`. **Manda el wild cluster, y el veredicto es
`NO-DISCRIMINA`.** La discrepancia no se promedia ni se elige: se declara.

**Qué NO significa este veredicto, dicho con la misma claridad:**

1. **No significa que `β_pres` sea cero.** Su punto es `+3.15 pp`, su IC de
   municipio excluye cero, su signo es el mismo en las **seis** columnas de
   sensibilidad de `§10`, y las **tres** transiciones «local sola →
   presidencial» del panel dan `+2.14`, `+2.52` y `+2.82` en tres entidades
   distintas. Significa que **con 6 conglomerados el intervalo conservador no
   descarta el cero**, y su extremo inferior es `−0.196`: falla por dos décimas.
2. **`β_int` es otra cosa.** No es que su intervalo sea ancho: es que **cambia de
   signo** entre subconjuntos (`−2.98` en el panel de `L6`, `+2.67` en las
   entidades nuevas). Está identificado por **2** transiciones, y esas dos
   —Nayarit `−6.77` y Baja California `+7.60`— se contradicen. Aquí el
   `NO-DISCRIMINA` no es un problema de potencia: es que **no hay señal común**.
3. **No refuta la hipótesis; no la puede refutar.** Ninguno de los dos
   coeficientes sale con signo contrario e IC fuera de 0, así que la rama
   `CONTRARIA` no aplica y no hay nada que declarar refutado.
4. **El test sí podía rechazar.** Con `k = 6` el `p` mínimo alcanzable es
   `0.03125 < 0.05`. La `p` de `β_pres` fue `0.1577`. No es el test degenerado de
   `L6`.

**Lo que este acto deja medido y no estaba antes:** que el `β ≈ 0` de `L6` **no
era un cero**, y que su inestabilidad ante quitar Coahuila era un artefacto de
promediar dos efectos opuestos. Al separarlos con la corrección `c1`, `β_pres`
resulta **estable, positivo y del mismo tamaño en cinco entidades**, y toda la
fragilidad se concentra en `β_int` y en `α`. Eso es un resultado sobre el
*diseño*, y sobrevive al veredicto del falsador.

## §13 · Contra los benchmarks (`§1.8`)

| referencia | efecto |
|---|---|
| Alemania, Leininger, Rudolph y Zittlau (PSRM 2018) | ≈ **+10 pp** |
| EE.UU., Hajnal y Lewis (2003) | **+36 pp** |
| `MAESTRA34-L4` (México, entre años, sin identificar) | +10.48 pp |
| `MAESTRA34-L6` (concurrencia sin distinguir tipo, 4 entidades) | +0.01 pp, IC95 [−3.38, +3.41] |
| **este acto, `β_pres`** (6 entidades) | **+3.15 pp**, IC95 wild cluster [−0.20, +6.50] |
| **este acto, `β_int`** | **−0.92 pp**, IC95 wild cluster [−3.78, +1.93] |

**Ninguno de los dos benchmarks cae dentro de ninguno de los dos intervalos.**
El `+10` alemán queda fuera del IC de `β_pres` (`[−0.20, +6.50]`) y fuera del de
`β_int` (`[−3.78, +1.93]`); el `+36` estadounidense, mucho más lejos de los dos.
Dicho de otro modo: aun tomando el extremo superior del intervalo conservador de
`β_pres`, este panel no reproduce la magnitud alemana. El benchmark del TEPJF
1991-2018 sigue **`NO-OBTENIDO`**:
`P0` de este acto no lo adquirió y mesa no lo depositó. **No se cita de memoria.**

## §14 · Contador

| | `L6` | **`L3`** |
|---|---:|---:|
| entidades tratadas medibles | 2 | **5** (meta declarada 8 — **ACOTADO**) |
| entidades en el panel (con el control nunca tratado) | 4 | **6** |
| municipios en el panel | 116 | **187** |
| observaciones municipio × transición | 269 | **540** |
| transiciones | 8 | **15** |
| conglomerados / `p` mínimo alcanzable | 4 / 0.125 | **6 / 0.03125** |
| transiciones `STAY` (identifican `α` sin mezcla) | 1 | **2** |
| payloads nuevos con sha | — | **10** |
| cargas al motor | 0 | **0** |
| corridas de Hito D | 0 | **0** |
