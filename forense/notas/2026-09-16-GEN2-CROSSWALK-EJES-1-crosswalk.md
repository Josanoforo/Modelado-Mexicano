# `ACTO GEN2-CROSSWALK-EJES-1` — nota de cierre

**16 de septiembre de 2026 · NUBE, Opus · cero microdato · cero red · cero
medición · cero adopción · cero cambio a `milpa/src/celdas.py`, al marcador,
a specs o a resultados**

Encargo archivado verbatim (0-bis A.3):
`forense/encargos/2026-09-16-GEN2-CROSSWALK-EJES-1.md`.
Compuerta: ninguna. Base declarada por el encargo: `1366d65b`.
**Base real, re-derivada al abrir como el propio encargo manda: `31afb18`**
(`PR #816` fusionó entre la redacción y la apertura; `git rev-list --count
HEAD..origin/main` → `0`).

---

## 0 · El veredicto, primero

> **Cero ejes del árbitro son `EQUIVALENTE` a un corte del modelo por
> definición.** Ninguno. Y las dos predicciones que el encargo escribió en
> `P4` salen **las dos al revés**:
>
> | par | lo que el encargo anticipó | lo que la definición dice |
> |---|---|---|
> | `localidad` ↔ `urbanizacion` | `EQUIVALENTE` por definición | **`MAPEO-N-A-1`** |
> | `dominio_urbano_rural` ↔ `urbanizacion` | `MAPEO-N-A-1` con tabla | **`NO-EQUIVALENTE`**, sin mapeo construible |
>
> Y hay un tercero que el encargo mandó verificar **antes de ratificar**, y
> que nadie esperaba que se moviera, porque mesa ya lo había ratificado:
>
> | par | lo que F-17 ratifica | lo que la definición dice |
> |---|---|---|
> | `formalidad` ↔ `formalidad` | `≡` (identidad) | **`MAPEO-N-A-1`** |
>
> **Consecuencia sobre la frase de cierre de la propia F-17** —*«Con esto, el
> marcador por segmento tiene hoy un eje comparable, y se dice»*—: queda
> **vencida por medición** en el sentido estricto de «comparable». El
> marcador tiene hoy **un eje utilizable, no un eje comparable**, y la
> distinción no es retórica: `formalidad` sirve a **grano 2 contra 2 sobre
> universo restringido a quien trabaja**, no por identidad. Se dice, que es
> lo que la firma pidió que se hiciera.

**Lo que este acto sí entrega:** la primera tabla sellada de crosswalk que el
árbol ha tenido, `data/crosswalk-ejes-arbitro-modelo-v1_0.tsv` — 15 filas, 18
columnas, **con `firma` vacía en las 15**, porque la firma es de mesa.

---

## 1 · La firma, propagada y con su numeración corregida (`P1`)

F-17 llegó el 15/sep citando «`NC-0226` renumerada». `ACTO
GEN2-FIRMAS-MESA-3` hizo lo correcto: la archivó verbatim, **no la propagó**,
y declaró la discrepancia como `NC-0262`, porque `NC-0226` está `CERRADA`
desde el 15/sep con otro objeto (la hoja de firmas 2, cerrada por el acto de
`PR #792`). La cabecera del encargo de hoy es mesa resolviendo exactamente esa
pregunta, con estas palabras:

> «Corrige la referencia de la firma de ayer, que citaba "NC-0226 renumerada"
> (NC-0226 ya existía CERRADA con otro objeto; FIRMAS-MESA-3 la registró sin
> propagar, correctamente). El texto sustantivo es idéntico»

Era la **primera** de las dos opciones que `NC-0262` puso a mesa (lapsus de
dedo), no la segunda: `NC-0226` **no se reabre**. Propagado, entonces:

- **`data/corrida0/decisiones.tsv`** — fila nueva, objeto
  `crosswalk-ejes-v1:F-17`, con la firma **verbatim** en `fuente`.
- **`NC-0240`** — enmienda fechada en `sucesor` (el texto previo **no** se
  reescribe, patrón de `NC-0077`/`NC-0239`) y **`CERRADA`**: lo que esa fila
  pedía —*«se MIDE el cruce y NO se decide»*— está entregado. La decisión es
  de mesa y vive ahora en `NC-0269` / `FP-376`.
- **`NC-0262`** — **`CERRADA`**. Su `sucesor` era literalmente «mesa aclara si
  F-17 quería decir NC-0240», y mesa lo aclaró. Está **dentro** del perímetro
  (`forense/no-corrido.tsv` lo nombra) y dejarla `ABIERTA` sería mantener una
  fila cuyo sucesor ya se ejecutó.
- **`forense/encargos/2026-09-16-GEN2-FIRMAS-MESA-3.md`** — **no se edita**,
  como su propio `P1` pidió. Queda como historia y se enlaza.

---

## 2 · Los dos pares, por definición (`P2`) — y el tercero que se movió

### 2.1 · `localidad` ↔ `urbanizacion` → **`MAPEO-N-A-1`**

La pregunta de `P2.1` tiene dos mitades y **se contestan distinto**.

**¿Es `tam_loc`? ¿Con los mismos cuatro cortes? — SÍ.** El eje `localidad`
del árbitro se construye desde `tloc` de ENIF 2024
(`conjunto_de_datos_tmodulo_enif2024`), y `tloc` trae el **mismo esquema de
cuatro códigos con los mismos umbrales** que el `tam_loc` que el modelo corta:

| código | `tloc` (ENIF 2024) | `tam_loc` (modelo, `CORTES_C1`) |
|---|---|---|
| `1` | 100 000+ | 100 000+ |
| `2` | 15 000–99 999 | 15 000–99 999 |
| `3` | 2 500–14 999 | 2 500–14 999 |
| `4` | <2 500 | <2 500 |

Verificado **contra el catálogo**, no contra el nombre: `tloc.csv` cotejado
con `tam_loc.csv` por `ACTO cal-conf fase B` el 3/ago/2026
(`forense/notas/2026-08-03-cal-conf-faseb-medicion.md:202-206`, *«idéntico
esquema a `tam_loc` de ENIGH … verificado contra el catálogo `tloc.csv`. Es
el único de los tres componentes donde el eje de ENIGH tiene análogo exacto en
el mismo instrumento»*), y **materializado** en un marginal medido que imprime
las cuatro categorías con sus umbrales literales y sus `n` (`:372-378`).

**¿Entonces es `EQUIVALENTE`? — NO.** Porque el eje que el árbitro
**publica** no tiene cuatro celdas: tiene **dos**. El colapso está en el
código, literal (`tools/medidor_ahorro_enif24.py:138-143`):

```python
Eje("localidad",
    lambda d: d["TLOC"].map({"1": "15 000 y mas", "2": "15 000 y mas",
                             "3": "menor de 15 000",
                             "4": "menor de 15 000"}).fillna(FUERA),
```

**Tabla explícita del mapeo:**

| corte del modelo | celda del árbitro |
|---|---|
| `urbanizacion` ∈ {`1`, `2`} | «15 000 y mas» |
| `urbanizacion` ∈ {`3`, `4`} | «menor de 15 000» |

**Qué pierde el marcador:** la **mitad de la resolución del eje**. Las 4
celdas selladas colapsan a 2; el marcador no puede distinguir `tam_loc=1`
(100 000+) de `tam_loc=2` (15 000–99 999), ni `tam_loc=3` de `tam_loc=4`.
**Ninguna de las cuatro celdas del modelo recibe un número propio** — cada
número del árbitro habla de una *unión* de dos celdas. Las 4 celdas del
árbitro (2 entradas × 2) caen sobre 2 coordenadas.

**Reserva, escrita y no escondida (`NC-0270`):** esta fila descansa en
evidencia **`REGISTRADA`**, no abierta aquí. No hay `data/raw` en la nube
(`tools/entorno.py` → `acceso_corpus.montado = NO`, `archivos_examinados = 0`)
y ni el FD de ENIF ni `tloc.csv` ni `tam_loc.csv` existen en el repo. La
cabecera del encargo ordena exactamente esta conducta: *«si un FD necesario
solo está en `data/raw`, esa pieza se declara NO-ACCESIBLE-AQUÍ y se rutea a
caja, no se adivina»*. La lectura citada es sólida —fue hecha **con el
catálogo abierto**, y su marginal imprime las cuatro categorías— pero es de
segunda mano, y la columna `evidencia_grado` lo dice en vez de aplanarlo.

### 2.2 · `dominio_urbano_rural` ↔ `urbanizacion` → **`NO-EQUIVALENTE`**

`P2.2` autoriza `MAPEO-N-A-1` **«si y solo si los umbrales coinciden en el
FD»**. La condición **no es falsa: es insatisfacible**, y la diferencia
importa. Del lado de ENVIPE 2025 **no hay umbrales que coincidan o dejen de
coincidir** — ENVIPE no publica ninguno:

> *«ENVIPE 2025 **no publica un solo umbral de población** — 6 diccionarios
> (2 225 líneas) y `fd_envipe2025.pdf` (7 207 líneas) solo dan `DOMINIO` como
> `U`/`C`/`R`»* — `forense/hallazgos.md:551`, medido por `ACTO MAESTRA35-L1`
> el 2/sep/2026 **con el FD abierto**.

El eje del árbitro es `DOMINIO` → `U` Urbano / `C` Complemento urbano / `R`
Rural (`tools/medidor_evasion_norma_envipe25.py:155-161`). Escribir
`R ↔ tam_loc=4` sería **inventar el corte**, que es literalmente lo que el
encargo prohíbe y lo que el sellado del propio eje ya declaró: nació
**«eje PROPIO Y DISTINTO, no el corte de 15 000 que el encargo pedía»**
(`milpa/tramite-ola5-propuesta-v0.yaml:1724-1727`).

**A.13 — por qué un negativo aguanta sin reabrir el FD.** El comando que lo
produjo declaró cuántos archivos examinó (6 diccionarios + el FD íntegro), y
es un negativo **exhaustivo sobre el universo entero del documento**, no un
«no lo encontré». Corroborado dos veces más, sobre la **misma variable
`DOMINIO`**, en dos instrumentos distintos:
`forense/notas/2026-08-04-endireh-paso1bis-verificacion-microdato.md:286`
(*«no es `tam_loc` …; es un proxy más burdo, no intercambiable sin
reclasificar»*) y `forense/notas/2026-08-03-cal-conf-faseb-medicion.md:165`
(ENCUCI: *«no es idéntico al `tam_loc` de 4 tramos de ENIGH»*).

**Qué pierde el marcador:** el eje entero. Y hay un costo extra que conviene
decir en voz alta, porque un mapeo forzado lo pagaría en silencio: **invertiría
un signo ya medido.** La evasión de norma sale **más alta en lo urbano**
(`0.592703`) que en lo rural (`0.403310`), con complemento urbano en medio
(`0.522090`) y los tres IC95 **sin traslape** — al revés de la corazonada
«menor de 15 000 más alta» sobre la que se escribió la predicción original.

### 2.3 · `formalidad` ↔ `formalidad` → **`MAPEO-N-A-1`** (y esto es lo que mesa no esperaba)

`P3` no pidió ratificar: pidió **verificar antes de ratificar**, y fijó la
consecuencia por adelantado — *«verificar que el árbitro también corta por
`segsoc` en las mismas dos categorías antes de ratificar; si no, es
`MAPEO-N-A-1` y se dice»*.

**El árbitro no corta por `segsoc`.** Corta por `P3_13` de ENIF 2024
(`tools/medidor_ahorro_enif24.py:144-149`):

```python
Eje("formalidad",
    lambda d: d["P3_13"].map({k: "sin seguridad social" if k == "7"
                              else "con seguridad social"
                              for k in "1234567"}).fillna(FUERA),
```

Son **tres diferencias, no una**, y sólo la primera es cosmética:

1. **Variable e instrumento distintos.** `P3_13` de ENIF 2024, no `segsoc` de
   ENIGH (`concentradohogar`/`poblacion`, nivel persona —
   `forense/notas/2026-07-31-p1-enigh-semilla.md:54`).
2. **7 códigos nativos colapsados a 2**, más dos valores que **no reciben
   celda en el modelo**: blanco (no trabaja) y `9` (no sabe), excluidos.
3. **Universo restringido.** El eje del árbitro **excluye a quien no
   trabaja**: cobertura `0.689676` en `via_informal` y `0.668937` en
   `horizonte_corto`. No es una inferencia de este acto — el yaml **sellado**
   lo marca él mismo, `universo_restringido: true`, con la nota `A-bis 4`
   *«no reconcilia contra el marginal poblacional»*.

Y hay una cuarta, conceptual, que es la que muerde: **`segsoc` es
derechohabiencia por cualquier vía; `P3_13` pregunta por derecho a servicio
médico *por parte de su trabajo*.** Quien es derechohabiente por su cónyuge es
`segsoc=1` **y** `P3_13=7`. El árbol ya había hecho esta misma distinción, en
otro instrumento y sin relación con este acto:
`forense/notas/2026-08-04-enut-paso1-familismo-obligacion.md:103` llama a
`P5_6_7` de ENUT *«mismo espíritu que `segsoc` pero no la misma variable ni el
mismo catálogo»*, y
`forense/notas/2026-08-04-encup-paso1-deferencia.md:179` precisa que *«`segsoc`
es específicamente afiliación a seguridad social»*.

**Qué pierde el marcador:** aquí **no colapsan celdas** (2 contra 2) — por eso
el parecido de nombre engaña tan bien. Lo que se pierde es el **universo** y
el **concepto**: un punto del árbitro sobre `formalidad` es una `p` calculada
sobre **personas que trabajan**, marcada contra una celda del modelo definida
sobre **toda la población**.

**Esto no revierte la firma de mesa.** F-17 ratificó por nombre, y la misma
F-17 ordenó verificar por definición. El ejecutor no decide cuál de las dos
gana: asienta la diferencia medida y la manda a firma (`FP-376`).

---

## 3 · La tabla sellada (`P3`)

`data/crosswalk-ejes-arbitro-modelo-v1_0.tsv` — **15 filas, 18 columnas,
escrita a mano, no derivada** (no hay script que la regenere, y envejece: se
dice en su cabecera y en el índice).

| veredicto | filas |
|---|---:|
| `EQUIVALENTE` | **0** |
| `MAPEO-N-A-1` | 2 — `formalidad`, `localidad` |
| `NO-EQUIVALENTE` | 1 — `dominio_urbano_rural` |
| `PENDIENTE-FP-53` | 1 — `edad` |
| `SIN-CORRESPONDENCIA` | 11 — 8 ejes del árbitro + **3 cortes sellados del modelo** |

**Auto-verificación que la tabla trae incorporada, y que cazó un defecto
real.** La primera versión de la tabla confundió *cardinalidad de la
partición* con *celdas totales* y sumaba **48**. La columna
`n_celdas_total_arbitro` ahora suma **74** sobre las 12 filas del árbitro, que
reconcilia exactamente con `RESULT-AGGOLA-PUNTOS-POR-EJE-CON-IC` (74 celdas,
de las cuales 64 con IC — `NC-0241`). Comando:

```
awk -F'\t' '!/^#/ && NR>1 && $2=="ARBITRO->MODELO"{s+=$7; n++} END{print n, s}' \
  data/crosswalk-ejes-arbitro-modelo-v1_0.tsv     #  ->  12 74
```

**La dirección inversa, que es la peor y por eso está en la tabla.** De los
cuatro cortes **sellados** del modelo, **tres no tienen un solo punto del
árbitro**: `ingreso` (`est_socio`, 4 categorías) y `acceso_digital`
(`celular`/`conex_inte`) salen `SIN-CORRESPONDENCIA` con cero candidatos, y
`migracion` está doblemente vacío — ni corte sellado ni punto del árbitro.

**Dos trampas de nombre que la tabla desarma explícitamente**, porque son
exactamente la clase de error que `A.15c` vigila (`hs02g` fue `CENTRO RURAL`
en un libro y `DIF` en otro):

- **`cobertura_seguro`** (ENVIPE `BP2_1`) es el seguro **del vehículo robado**
  (regla `R7.2`), no cobertura de salud ni seguridad social. Comparte con
  `formalidad` la palabra «seguro» y nada más.
- **`cuenta_formal`** (ENIF `P5_4_1..9`) es tenencia de **cuenta bancaria**.
  Comparte con `acceso_digital` la **forma** binaria de hogar y nada más.

Y una tercera que vale para cualquier intento futuro de unificar
`escolaridad`: **`NIV` no significa lo mismo en las tres encuestas** — ENIF
invierte `04`/`05` (normal básica ↔ técnica con secundaria) respecto de ENCIG
y ENVIPE (`forense/hallazgos.md:551`).

**Aviso al sucesor sobre `edad`, que este acto NO decide.** `FP-53` está
`FIRMADA` (`ADR-111(b)`, 18/ago/2026) con la convención **15-29** para
«joven», y su mitad empírica sigue en cola (`CORTE-EDAD-EMPIRICO`, Ubuntu);
`CORTES_C1` sigue registrando `edad: None`. El árbitro corta **18-29** /
30-44 / 45-59 / 60+ (`tools/ejes_maestra35_l1.py:54-62`), porque el universo
de ENIF/ENCIG/ENVIPE arranca en 18. **`18-29` no es `15-29`.** Se deja escrito
para que el día que el corte se selle no se resuelva por parecido de nombre —
que es el defecto entero que este acto existe para no repetir.

---

## 4 · El hueco del índice, que era entregable (`P3`)

`P3` mandaba: *«o donde `data/INFRAESTRUCTURA-v1_0.md` diga; si el índice no
cubre "crosswalk de ejes", ese hueco es entregable y se reporta»*.

**No lo cubría.** Verificado **antes** de escribir, contra `HEAD`:

```
git show HEAD:data/INFRAESTRUCTURA-v1_0.md | grep -ic "crosswalk"          # 4
git show HEAD:data/INFRAESTRUCTURA-v1_0.md | grep -c "CORTES_C1\|celdas.py" # 0
```

Los 4 aciertos son `crosswalk-fuente-puerta` y `crosswalk-tablas-fd` —
ninguno sobre ejes ni vocabulario de segmentación. Ninguno de los 9 dominios
cubría el caso. Y el hueco no era cosmético: `NC-0240` llevaba desde el 15/sep
pidiendo esa tabla y **no había dónde ponerla**. Cerrado con una fila en
«Si tu encargo hace X, escribe en Y» y la declaración del hueco arriba de esa
tabla.

---

## 5 · Lo que va a mesa (`P4`)

`FP-376`, tres veredictos, cada uno con su evidencia y su costo escrito.
**Recomendación del ejecutor, que mesa toma o deja:**

1. **Firmar `localidad` = `MAPEO-N-A-1` con su reserva** (`NC-0270`: evidencia
   registrada, no abierta aquí). Habilita el marcador a **grano colapsado**:
   2 celdas donde el modelo tiene 4. Es más que nada y menos que identidad.
2. **Firmar `dominio_urbano_rural` = `NO-EQUIVALENTE`, sin mapeo.** Lo que no
   se recomienda bajo ninguna lectura es consumirlo: no hay umbral que
   respetar y forzarlo invierte un signo medido.
3. **Firmar `formalidad` = `MAPEO-N-A-1` con universo declarado.** Es el eje
   que F-17 ratificó por nombre; la definición dice otra cosa y `P3` fijó de
   antemano que en ese caso «se dice».

**Y lo que esta firma NO desbloquea, para que nadie lo lea como luz verde.**
El marcador por segmento tiene **tres bloqueadores independientes** y esta
firma levanta **uno**:

| # | bloqueador | estado |
|---|---|---|
| i | **θ** — `theta.valor()` lanza `ThetaNoDisponible` en **43/43** entradas | `NC-0239`, **ABIERTA** |
| ii | **vocabulario de ejes** — este acto | `NC-0269` / `FP-376`, a firma |
| iii | columna de segmento del marco (`RESULT-AGGOLA-MARCO-TIENE-COLUMNA-SEGMENTO = NO`) | abierto |

---

## 6 · Contador

**Cero.** Cero mediciones sobre México, cero corridas selladas, cero
adopciones al motor, cero microdato abierto, cero red. `milpa/src/celdas.py`
intacto (los cortes son dato sellado bajo `ADR-100(2)`); marcador, specs y
resultados intactos. Lo que produce es **registro**: una tabla que no existía,
una firma propagada con su numeración corregida, dos `NC` cerradas y dos
abiertas, y una decisión que hoy sí es firmable porque está escrita con su
evidencia y con su costo.
