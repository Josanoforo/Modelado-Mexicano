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
