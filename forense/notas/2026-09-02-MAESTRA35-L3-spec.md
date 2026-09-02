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
