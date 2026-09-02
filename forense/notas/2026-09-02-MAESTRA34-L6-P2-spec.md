# `ACTO MAESTRA34-L6` — `P2`, spec congelada (COMMIT-1)

Bloque B-bis / A-bis de `instrucciones-proyecto-v2_12.md`: este archivo se
escribe **antes** de calcular una sola tasa de participación. El commit que lo
crea no toca ningún otro archivo. Los resultados se **añaden** después, en un
segundo commit, sin editar nada de lo que está aquí.

---

## §0 · Premisas

### 0.1 · De dónde sale el tratamiento

De `data/p0-calendario-ayuntamientos-v1_0.tsv` y
`data/p0-tratamiento-homologacion-v1_0.tsv`, derivadas en el commit de `P0` de
30 acuerdos del Consejo General del INE (ver
`forense/notas/2026-09-02-MAESTRA34-L6-P0-tabla-tratamiento.md`). No se usa
memoria ni ninguna tabla previa del repo: `P0` verificó que no existía.

### 0.2 · Contaminación declarada (`ADR-46`)

La sesión que congela esta spec **ya vio** lo siguiente, y lo declara antes de
medir en vez de después:

1. **Cabeceras y primeras filas** de cada tabla de resultados adquirida en `P1`.
   En concreto vio, de `iec_coahuila_2017_ayuntamientos_x_municipio.xlsx`, las
   filas 6-14: los totales de votación y la lista nominal de **9 de los 38
   municipios de Coahuila en 2017** (Abasolo, Acuña, Allende, Arteaga, Candela,
   Castaños, Cuatrociénegas, Escobedo, Francisco I. Madero). Conoce, por tanto,
   el orden de magnitud de la participación de esos 9 municipios en el año
   **antes** del tratamiento de la cohorte `g2018`. **No** vio ninguna fila de
   la tabla de 2018, 2021 ni 2024 de Coahuila más allá de la cabecera.
2. **La cifra estatal de participación del PREP de Nayarit 2017**:
   `PORCENTAJE_PARTICIPACION_CIUDADANA = 62.0791`, que viene en el preámbulo del
   CSV de datos abiertos del INE (`DatosAbiertos-UNICOM-NAYARIT_AYUN_2017.csv`)
   y se leyó al inspeccionar su estructura. Es una cifra **estatal** y
   **preliminar** (PREP, no cómputo); ese CSV **no** entra al universo de esta
   spec, pero el número fue visto y podría anclar expectativas sobre el «antes»
   de la cohorte `g2021`.
3. **La lista nominal por municipio de Nayarit 2021** (17 de 20 municipios,
   primera página de `LN2021.pdf`). Es denominador, no desenlace.
4. Primeras filas de las tablas por casilla de Coahuila 2017/2018/2021,
   Zacatecas 2018/2021/2024, Durango 2016/2019, Hidalgo 2020/2024 y
   Aguascalientes 2019/2021 — casillas sueltas, no agregados municipales.

**No** se ha calculado ninguna tasa de participación, ninguna suma municipal,
ninguna diferencia y ningún intervalo, en ninguna entidad ni año, antes de este
commit.

### 0.3 · La reserva de identificación, escrita antes de medir

`P0 §7` demostró, contando fechas de fin de campaña en los 30/32/32 anexos de
los ciclos 2018/2021/2024, que **en los años federales de la ventana no existe
ni un solo municipio no tratado**: todas las elecciones locales de esos años se
celebraron el mismo día que la federal. La única elección municipal no
concurrente celebrada en un año federal es Chiapas 2015 (19 de julio), que este
acto **no** logró adquirir.

Consecuencia, aceptada aquí y no rodeada: **el tratamiento es colineal con el
año electoral**, y una especificación con efectos fijos de año saturados —que
es lo que la firma de mesa propone— **no lo identifica**. Esta spec sustituye
esos efectos fijos por una **tendencia temporal lineal** estimada de las
transiciones sin cambio de tratamiento, y lo declara como el supuesto de
identificación principal, no como un detalle técnico. Si ese supuesto es falso
—si la participación municipal salta en años federales por razones distintas de
compartir boleta—, este diseño no lo distingue y el número que produzca **no**
es causal. Lo que sí hace, y `MAESTRA34-L4` no podía hacer, es separar
**concurrencia con intermedia** de **concurrencia con presidencial** (§1.7).

### 0.4 · Alcance, declarado como falta

`P0` identificó **14** entidades tratadas con antes y después en la ventana. El
encargo fija un mínimo de **≥8** para que `P3` no corra acotado. `P1` obtuvo
serie con lista nominal en la fuente para **4** entidades y **2** de ellas son
tratadas. Por lo tanto **`P3` corre y se declara ACOTADO**, con las 12 entidades
tratadas faltantes nombradas una por una en la nota de cierre. No se sustituye
el faltante por ninguna imputación.

---

## §1 · Spec

### 1.1 · Estimando

Efecto de que la elección municipal se celebre el mismo día que la elección
federal («concurrencia») sobre la **participación electoral municipal**, medido
en **puntos porcentuales**. Escala declarada: **pp**. No es una probabilidad y
no puede cargarse al motor tal cual.

### 1.2 · Unidad y desenlace

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

### 1.3 · Universo

Los municipios de las entidades cuya serie de `P1` trae lista nominal en la
fuente, presentes con `lista_nominal > 0` **en todas** las elecciones de la serie
de su entidad:

| entidad | elecciones de la serie | transiciones |
|---|---|---|
| Coahuila | 2017 (no conc.), 2018 (conc.), 2021 (conc.), 2024 (conc.) | 1 SWITCH-ON + 2 STAY-ON |
| Nayarit | 2017 (no conc.), 2021 (conc.), 2024 (conc.) | 1 SWITCH-ON + 1 STAY-ON |
| Zacatecas | 2018 (conc.), 2021 (conc.), 2024 (conc.) | 2 STAY-ON |
| Durango | 2016 (no conc.), 2019 (no conc.) | 1 STAY-OFF |

Exclusiones declaradas:

- **Usos y costumbres (Oaxaca): NO-APLICA con conteo 0.** Oaxaca no está en el
  universo, porque `P1` no adquirió su serie. La exclusión que el encargo ordena
  se declara satisfecha por vacío, no por filtro.
- Filas que no son municipios (agregados estatales, votos del extranjero, notas
  al pie): se excluyen **nombrándolas una por una** y se comprueba
  aritméticamente que la suma de los municipios más las filas excluidas
  reproduce el total que publica el organismo. Es el control que `L4` fijó.
- Municipio ausente de alguno de los años de su serie: se excluye de **todas**
  las transiciones de esa entidad, y se cuenta.

### 1.4 · Tratamiento

`D(m, e) = 1` si la jornada de la elección `e` se celebró el mismo día que la
jornada federal; `0` si no. Se lee de
`data/p0-calendario-ayuntamientos-v1_0.tsv`, columna
`concurrente_con_federal`, que ya incorpora la excepción documentada de Chiapas
2015 y la verificación A.13 de que no hay otras.

### 1.5 · Estimador principal

**Diferencias en diferencias escalonadas sobre primeras diferencias**, que es la
forma en que un estimador tipo **Callaway–Sant'Anna** se puede escribir cuando el
panel es **desbalanceado por construcción** —cada entidad vota en años distintos,
así que no hay periodos calendario comunes— y el tratamiento es colineal con el
año.

Para cada entidad `s` y cada par de elecciones **consecutivas** `e_k → e_{k+1}`:

```
Δy(m,k)  = participacion(m, e_{k+1}) − participacion(m, e_k)      [pp]
hueco(k) = anio(e_{k+1}) − anio(e_k)                              [años]
ΔD(k)    = D(e_{k+1}) − D(e_k)  ∈ {+1 SWITCH-ON, 0 STAY, −1 SWITCH-OFF}
```

Regresión, a nivel **municipio**, sobre todas las transiciones del universo:

```
Δy(m,k) = γ · hueco(k) + β · ΔD(k) + ε(m,k)
```

`β` es el estimando: el salto de participación atribuido a la concurrencia, en
pp. `γ` es la deriva secular anual, identificada **sólo** por las transiciones
con `ΔD = 0` (las cuatro STAY-ON de Coahuila/Nayarit/Zacatecas y la STAY-OFF de
Durango). Es la traducción exacta de un modelo con efectos fijos de municipio y
tendencia lineal de año:
`y(m,e) = α_m + γ·anio(e) + β·D(e) + u`.

**Por qué este y no Callaway–Sant'Anna canónico**, declarado como el encargo
pide: el estimador de Callaway–Sant'Anna necesita, para cada cohorte `g` y cada
periodo `t`, un grupo de comparación observado **en ese mismo `t`** y todavía no
tratado. `P0 §7` midió que ese grupo **no existe** en 2018, 2021 ni 2024. Lo que
sí sobrevive de Callaway–Sant'Anna, y es lo que se usa, son sus dos piezas
esenciales: (i) el contraste se construye por **cohorte de adopción** y no
agregando todo en un `TWFE` que promedia comparaciones prohibidas (el problema
de Goodman-Bacon), y (ii) el grupo de comparación son unidades **nunca tratadas
o aún no tratadas** —aquí, las transiciones sin cambio de tratamiento—, nunca
unidades ya tratadas usadas como control de unidades que se tratan después.

### 1.6 · Errores estándar

Agrupados por **entidad**. Con sólo 4 conglomerados, la aproximación asintótica
no aplica: el intervalo principal se calcula por **bootstrap wild cluster** con
pesos de Rademacher sobre las 4 entidades, `B = 10 000`, `seed = 42`, y se
reporta **también** el bootstrap por municipio con reemplazo (`B = 10 000`,
`seed = 42`) como intervalo de contraste. **El intervalo que decide el falsador
es el wild cluster por entidad**, por ser el conservador; si los dos discrepan en
si cruzan cero, se reporta la discrepancia y manda el wild cluster.

### 1.7 · Diagnósticos pre-registrados

1. **ATT por cohorte**: `β` estimado por separado para `g2018` (Coahuila,
   concurrencia con **presidencial**) y `g2021` (Nayarit, concurrencia con
   **intermedia**), cada uno contra la `γ` común de las transiciones `ΔD = 0`.
2. **El contraste que `L4` no podía hacer**: `ATT(g2021) − ATT(g2018)`. Si el
   efecto fuera «atención de año presidencial» y no «misma boleta», `ATT(g2021)`
   —cuya elección federal es intermedia, sin presidencia— tendría que ser
   **sustancialmente menor**. Se reporta el signo, la magnitud y si su IC cruza
   cero. **Este contraste no adjudica por sí solo**: es un diagnóstico con `n = 2`
   entidades y así se reporta.
3. **Event-study por año relativo al tratamiento**: media de `Δy` por transición,
   ordenadas por año relativo al tratamiento de la entidad, con las
   pre-transiciones disponibles como diagnóstico de pre-tendencia. Se declara de
   antemano que la única pre-transición no tratada disponible es la de Durango
   (2016→2019) y que, por tanto, **la prueba de pre-tendencias de este acto es
   débil y se reporta como débil**.
4. **Heterogeneidad por tamaño**: terciles de `lista_nominal` del municipio en su
   primera elección de la serie. Se reporta `β` por tercil.
5. **Sensibilidad al hueco**: `β` re-estimado excluyendo la transición de hueco 1
   (Coahuila 2017→2018), que es la que más depende de extrapolar `γ`.
6. **Controles aritméticos** (ninguno es opcional; si alguno falla se reporta el
   fallo antes que el resultado):
   - reagregar casilla por casilla reproduce la tabla por municipio, con
     `|Δvotos| = 0` y `|Δlista nominal| = 0`, donde existan las dos tablas;
   - donde la fuente publique `% PART`, la participación recalculada coincide con
     la publicada (diferencia máxima reportada);
   - ninguna participación fuera de `(0, 100]`;
   - la suma de municipios más las filas excluidas reproduce el total publicado.

### 1.8 · Comparaciones

Contra `MAESTRA34-L4` (`+10.4790 pp`, IC95 `[+9.6890, +11.2652]`, n=163, diseño
**entre años** Coahuila+Edomex 2023→2024), misma escala. Contra los benchmarks
que la firma `DC1` declara: Alemania **≈10 pp** (Leininger, Rudolph y Zittlau,
PSRM 2018) y EE.UU. **36 pp** (Hajnal y Lewis 2003). El benchmark nacional del
TEPJF (1991-2018) **no está en el corpus** (`P0` lo verificó: 0 aciertos de
`tepjf` en `data/manifiesto.yaml`); si `P3` no lo adquiere, se reporta como
`NO-OBTENIDO` y **no** se cita de memoria.

### 1.9 · Falsador `B-bis`, verbatim del encargo

Sobre el **IC95 wild cluster por entidad** de `β`:

- **el IC contiene 0** → `civico.participacion.contingente` queda
  **REFUTADA-como-causal**, y el `Δ` de `MAESTRA34-L4` se reinterpreta como
  efecto de año;
- **`β` entre 5 y 15 pp** → **CORROBORADA**, y el `+10.5` de `L4` se lee como
  mayormente concurrencia;
- **`β > 15 pp`, o `β < 5 pp` con IC fuera del rango de `L4`** → **acotada**, y se
  dice cuánto del `Δ` de `L4` era año.

Se decide con el signo y los extremos del intervalo, no con el punto.

### 1.10 · Lo que este procedimiento no puede decir, dicho antes

- No separa concurrencia de **jerarquía del cargo**: en las dos transiciones
  tratadas el cargo municipal es el mismo a ambos lados, pero la boleta federal
  que se le suma no lo es.
- No separa concurrencia de cualquier **choque nacional** que coincida
  exactamente con los años federales y no sea capturado por una tendencia lineal.
- Con 4 conglomerados, cualquier intervalo es frágil; se usa el estimador
  conservador y se dice.

### 1.11 · Sello

**El primer resultado que produzca este procedimiento es el que se reporta.**

---
---

# `P3` — RESULTADOS (COMMIT-2)

Añadido en un segundo commit. **Nada de lo escrito arriba se ha editado.** El
procedimiento corrió una vez, tal como está congelado, y lo que sigue es lo que
produjo. Script: `tools/l6_estimador_concurrencia.py`; lectores por fuente:
`tools/l6_lectores.py`; salida cruda: `data/l6-resultados-concurrencia-v1_0.json`.

## §2 · El panel que quedó, y los controles antes del número

**8 transiciones, 269 observaciones municipio × transición, 4 entidades.**

| entidad | municipios | serie | transiciones |
|---|---|---|---|
| Coahuila | **38** | 2017, 2018, 2021, 2024 | 1 SWITCH-ON + 2 STAY-ON |
| Nayarit | **19** | 2017, 2021, 2024 | 1 SWITCH-ON + 1 STAY-ON |
| Zacatecas | **58** | 2018, 2021, 2024 | 2 STAY-ON |
| Durango | **1** | 2016, 2019 | 1 STAY-OFF |

Municipios perdidos por la regla de `§1.3`, nombrados: **`LA YESCA`** (Nayarit) —
no aparece en el concentrado ordinario de 2021 porque su elección fue
**extraordinaria**, y el propio IEE publica su resultado en un archivo aparte
(`PyS21-Ext.xlsx`); y **38 de los 39 municipios de Durango**, porque el archivo
que el IEPC publica para 2016 (`resultados_2016.xlsx`) cubre **sólo el municipio
de Durango**, no el estado. Ninguno se imputó.

**Los controles de `§1.7.6`, corridos antes de mirar el estimador:**

| control | resultado |
|---|---|
| Coahuila 2021: reagregar casilla → municipio | `max|Δvotos| = 0`, `max|Δlista nominal| = 0`, 38/38 |
| Coahuila 2018: reagregar casilla → municipio | `max|Δvotos| = 0`, 37 municipios en común |
| Coahuila 2021 y 2024: `% PART` publicada vs recalculada | diferencia máxima **0.000000 pp**, 38/38 en los dos años |
| Coahuila 2018: suma de los 38 municipios vs la fila `TOTALES` de la propia tabla | **1 359 037 / 2 251 549 = exacto** |
| Durango 2016: suma de casillas vs fila de gran total publicada | lista nominal **exacta** (455 230); votos difieren en **782** de 260 008 (**0.30 %**), por filas de casilla cuya etiqueta no cae en los cuatro tipos — se usa la **fila publicada**, no la suma |
| Zacatecas 2018: identidad `VÁLIDOS + NULOS + NO REG = TOTAL` | **2 498 de 2 509** casillas; las **11** que fallan son todas de `NOCHISTLÁN DE MEJÍA` y suman **2 231 votos = 0.2964 %** del estado |
| Zacatecas 2024: identidad `Σ(columnas de partido) = VTOTAL` | **2 646 de 2 646**, exacta |
| participación fuera de `(0, 100]` | **0 municipios** |

**Un defecto de fuente que el control atrapó y que habría envenenado el
resultado:** la tabla de Zacatecas 2024 trae dos columnas de total,
`T VOTARON` y `VTOTAL`. **`T VOTARON` dice `Sin Dato` en 839 de 2 649 casillas
(31.7 %), repartidas en 29 de los 58 municipios** — Guadalupe pierde 216 de 261
casillas, Río Grande 105 de 106. Usarla habría hundido la participación de medio
Zacatecas sin ningún aviso. `VTOTAL` está en 2 646 de 2 649 y cumple
`Σ(partidos) = VTOTAL` en **todas**. Se usa `VTOTAL`.

## §3 · Participación observada

Agregada (suma de votos / suma de lista nominal) y media municipal no ponderada:

| entidad | año | conc. | agregada | media municipal | n |
|---|---|:--:|---:|---:|---:|
| Coahuila | 2017 | **no** | 57.05 | 62.53 | 38 |
| Coahuila | 2018 | sí | 60.36 | 64.67 | 38 |
| Coahuila | 2021 | sí | 57.58 | 66.58 | 38 |
| Coahuila | 2024 | sí | 64.65 | 68.63 | 38 |
| Nayarit | 2017 | **no** | 61.03 | 65.51 | 20 |
| Nayarit | 2021 | sí | 52.36 | 58.75 | 19 |
| Nayarit | 2024 | sí | 55.75 | 60.75 | 20 |
| Zacatecas | 2018 | sí | 64.74 | 67.75 | 58 |
| Zacatecas | 2021 | sí | 50.68 | 55.27 | 58 |
| Zacatecas | 2024 | sí | 59.39 | 61.82 | 58 |
| Durango (capital) | 2016 | **no** | 57.12 | 57.12 | 1 |
| Durango (estado) | 2019 | **no** | 44.90 | 41.67 | 39 |

## §4 · El estimador de `§1.5`

```
Δy(m,k) = γ · hueco(k) + β · ΔD(k)
```

| | |
|---|---|
| **`β` (efecto de la concurrencia)** | **+0.0149 pp** |
| **IC95 wild cluster por entidad** (el que decide, `§1.6`) | **[−3.3765, +3.4064]** |
| IC95 bootstrap por municipio | [−1.3865, +1.3312] |
| `γ` (deriva) | −0.4215 pp/año |
| n | 269 observaciones, 8 transiciones, 4 conglomerados |

**Los dos intervalos contienen cero.**

**Advertencia mecánica que hay que decir para que el intervalo no se
sobreinterprete:** con **4** conglomerados, el bootstrap wild cluster de
Rademacher sólo tiene `2⁴ = 16` patrones de signo, y se verificó que producen
**16 valores distintos** de `β*`; el **p-valor mínimo alcanzable es 0.125**.
Ese test **no podía rechazar al 5 % pasara lo que pasara**. Por eso importa que
el bootstrap por municipio —que no sufre esa limitación— **también** contenga
cero, y con un intervalo cuatro veces más estrecho: `[−1.39, +1.33]`. El
veredicto no depende del test degenerado.

## §5 · El diagnóstico que decide la lectura (`§1.7.2`)

Los `ATT` por cohorte, cada uno contra la misma `γ = −0.2692 pp/año` estimada
**sólo** de las 6 transiciones sin cambio de tratamiento:

| cohorte | qué elección federal | Δ bruto | hueco | **ATT** | IC95 municipios | n |
|---|---|---:|:--:|---:|---|---:|
| **`g2018`** Coahuila 2017→2018 | **presidencial** | +2.142 | 1 | **+2.4113 pp** | [+1.53, +3.28] | 38 |
| **`g2021`** Nayarit 2017→2021 | **intermedia** | −6.768 | 4 | **−5.6914 pp** | [−6.94, −4.38] | 19 |

**Los signos son opuestos, y ninguno de los dos intervalos cruza cero.**
`ATT(g2021) − ATT(g2018) = −8.10 pp`. Cuando la elección municipal se juntó con
una **presidencial**, la participación subió 2.4 pp más de lo que la tendencia
predecía; cuando se juntó con una **intermedia**, bajó 5.7 pp. Nayarit votó
**más** en su elección local sola de 2017 (61.03 % agregado) que concurriendo con
la federal intermedia de 2021 (52.36 %).

Que el pooled `β` salga ≈ 0 no es que «no pase nada»: es que **el promedio de
+2.4 y −5.7 se cancela**. Lo que el dato dice no es «la concurrencia no importa»,
sino **«concurrencia» no es la variable que mueve la participación**.

## §6 · La lectura que lo confirma sin usar ninguna cohorte tratada

Las transiciones **entre dos elecciones que ya eran concurrentes** (`ΔD = 0`,
`D = 1` en los dos extremos) no pueden mover nada por concurrencia, y aun así:

| entidad | transición | Δ media municipal |
|---|---|---:|
| Zacatecas | 2018 → 2021 | **−12.487 pp** |
| Zacatecas | 2021 → 2024 | **+6.550 pp** |
| Coahuila | 2018 → 2021 | +1.907 pp |
| Coahuila | 2021 → 2024 | +2.053 pp |
| Nayarit | 2021 → 2024 | +2.007 pp |

Zacatecas es concurrente en **las tres** elecciones de su serie y su
participación agregada hace **64.74 → 50.68 → 59.39**: un vaivén de **14 pp
hacia abajo y 8.7 hacia arriba con el tratamiento fijo en 1**. El año 2021 es
elección federal **intermedia**; 2018 y 2024, **presidenciales**. Ese vaivén es
del tamaño del efecto que se le atribuía a la concurrencia, y la concurrencia no
lo puede explicar.

## §7 · Cuánto del `Δ` de `MAESTRA34-L4` era año

`MAESTRA34-L4` midió **+10.4790 pp** entre la local **no concurrente** de 2023 y
la local **concurrente** de 2024 en Coahuila y Edomex. En la misma escala y en la
misma entidad, este acto mide el salto **2021 → 2024 con la concurrencia fija en
1**:

| entidad | 2021 → 2024, ambas concurrentes | agregada |
|---|---:|---:|
| Coahuila | **+2.053 pp** (media municipal) | **+7.07 pp** |
| Zacatecas | **+6.550 pp** | **+8.71 pp** |
| Nayarit | **+2.007 pp** | **+3.39 pp** |

Entre 2021 y 2024, sin que ninguna de esas entidades cambiara de tratamiento, la
participación municipal subió entre **+2.0 y +6.6 pp** en media municipal y entre
**+3.4 y +8.7 pp** en agregado. El `Δ` de `L4` es **+10.48 pp**. **Una parte
grande de ese número —del orden de la mitad a los cuatro quintos según la
entidad— es movimiento de año, no de concurrencia**, y el resto no queda
identificado por este diseño.

## §8 · Heterogeneidad y sensibilidad (`§1.7.4`, `§1.7.5`)

| corte | `β` (pp) | n |
|---|---:|---:|
| municipios chicos (lista nominal ≤ 4 862) | +3.227 | 91 |
| medianos | −1.702 | 89 |
| grandes (> 14 660) | −1.409 | 89 |

| sensibilidad | `β` (pp) |
|---|---:|
| sin la transición de hueco 1 (Coahuila 2017→2018) | **−5.6914** |
| sin Durango | −0.0273 |

La sensibilidad es la que hay que leer con cuidado, y estaba pre-registrada:
quitar Coahuila deja sólo la cohorte de intermedia y `β` se va a **−5.69**;
quitar Durango casi no mueve nada. **`β` no es un número estable: es el promedio
de dos efectos de signo contrario**, y el promedio depende de cuál cohorte pese
más. Es otra forma de ver `§5`.

## §9 · Contra los benchmarks

| referencia | efecto de concurrencia |
|---|---|
| Alemania, Leininger, Rudolph y Zittlau (PSRM 2018) | **≈ +10 pp** |
| EE.UU., Hajnal y Lewis (2003) | **+36 pp** |
| `MAESTRA34-L4` (México, entre años, sin identificar) | +10.48 pp |
| **este acto** (México, escalonado, 4 entidades) | **+0.01 pp**, IC95 [−3.38, +3.41] |
| — de las cuales, con presidencial | +2.41 pp [+1.53, +3.28] |
| — de las cuales, con intermedia | −5.69 pp [−6.94, −4.38] |

El caso alemán y el estadounidense **no se replican** en este universo. El
benchmark del TEPJF («Elecciones concurrentes y participación electoral en
México, 1991-2018», 2020) **`NO-OBTENIDO`**: no está en el corpus (`P0` verificó
0 aciertos de `tepjf` en `data/manifiesto.yaml`) y este acto no lo adquirió. No
se cita de memoria.

## §10 · Veredicto del falsador `B-bis` (`§1.9`)

El IC95 que la spec designó para decidir —wild cluster por entidad— es
**[−3.3765, +3.4064]** y **contiene 0**. El de contraste, bootstrap por
municipio, es **[−1.3865, +1.3312]** y **también contiene 0**. Los dos coinciden,
así que no hay discrepancia que arbitrar.

> **`civico.participacion.contingente` queda `REFUTADA-COMO-CAUSAL`**, y el `Δ`
> de `MAESTRA34-L4` se reinterpreta como **efecto de año**.

Es la primera de las tres ramas del falsador, aplicada literalmente. Y hay que
decir con la misma claridad **qué NO significa**:

1. **No significa que la participación municipal no cambie entre esas
   elecciones.** Cambia mucho: hasta 14 pp. Significa que **no cambia por
   compartir la boleta**.
2. **No refuta que exista un efecto de concurrencia en México.** Refuta la
   lectura causal del número de `L4` con la evidencia de estas 4 entidades, y
   con `β` promediando dos efectos opuestos de tamaño no despreciable.
3. **No es un cero de precisión.** El IC por municipio es estrecho (`±1.4 pp`) y
   excluye tanto el +10 alemán como el +36 estadounidense. Lo que es ancho —y se
   dijo antes de medir— es el supuesto de identificación, no el intervalo.

## §11 · Reserva, escrita antes y no movida

`§0.3` y `§1.10` de la spec ya decían que este diseño no separa la concurrencia
de un choque nacional que coincida con los años federales y no sea capturado por
una tendencia lineal. **Los resultados muestran que ese choque existe, es grande
y no es lineal**: es el ciclo presidencial/intermedia, visible en `§6` con el
tratamiento fijo. La `γ` lineal de la spec lo absorbe mal, y esa mala absorción
es la razón principal de que el `β` pooled sea inestable (`§8`). El acto reporta
el número que su procedimiento congelado produjo, y **señala el defecto del
procedimiento en vez de cambiarlo después de ver el resultado**: la corrección
—sustituir la tendencia lineal por un efecto fijo de *tipo* de año federal
(presidencial / intermedia / sin federal)— es lo que el acto sucesor debe
pre-registrar, con las 12 entidades tratadas que `P1` no alcanzó.

## §12 · Contador

| | antes | después |
|---|---|---|
| payloads en `data/manifiesto.yaml` | 953 | **1026** (+73: 30 de calendario + 43 de resultados) |
| entidades con calendario de tratamiento derivado de fuente primaria | 0 | **32** |
| entidades tratadas identificadas (antes y después en la ventana) | 0 | **14** |
| entidades con serie municipal medible | 0 | **4** (2 tratadas) |
| reglas con `Δ` identificado | 0 | **1** (`civico.participacion.contingente`, veredicto `REFUTADA-COMO-CAUSAL`) |
| cargas al motor | 0 | **0** |
| corridas de Hito D | — | **0** |
