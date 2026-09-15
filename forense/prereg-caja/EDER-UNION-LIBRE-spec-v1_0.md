# EDER 2017 · tipo de primera unión — pre-registro congelado de `CALC-EDER-0003`

### `prereg-caja-EDER-UNION-LIBRE` · **v1.0** · 15 de septiembre de 2026

> | | |
> |---|---|
> | **ARCHIVO** | `forense/prereg-caja/EDER-UNION-LIBRE-spec-v1_0.md` |
> | **NOMBRE ESTABLE** | **`prereg-caja-EDER-UNION-LIBRE`** — cítalo así, nunca por nombre de archivo |
> | **QUÉ ES** | Pre-registro, congelado **en NUBE y antes de abrir un solo byte de microdato**, de `CALC-EDER-0003`: la proporción ponderada de personas cuya **primera unión** fue unión libre en EDER 2017, con IC95 **de diseño**. Releva el **payload** de `CORR-0013` (`RES-0043`, `RES-0044`). |
> | **QUÉ NO ES** | **No reproduce la cifra GEN1 de esas dos celdas, y no debe intentarlo.** `RES-0043`/`RES-0044` declaran payload EDER 2017 y `clase` *«ENADID 2023, `p3_27_ag`»*: el número que el motor carga **no salió del archivo que el registro le atribuye** (§0.2). Son dos preguntas distintas — *tipo de primera unión* (retrospectiva) vs. *situación conyugal actual* (transversal) — y esta spec mide la primera. No promedia las dos. No adopta nada a `milpa/`. No corre el medidor. |
> | **VERIFICAS ASÍ** | CAJA confirma, antes de calcular, que el join persona→vivienda y persona→antecedentes **no deja huérfanos** (`G-N-SIN-VIVIENDA`, `G-N-SIN-FACTOR-PER`), que ningún primer-código-no-cero cae en el conjunto de disolución `{6,7,8,60,70,80}` (censura izquierda), y que los códigos fuera de `LIBRE ∪ DIRECTO` se **cuentan y se declaran**, nunca se fuerzan a una rama. |

**Acto:** `ACTO GEN2-SPECS-DEMANDA-1`, 15/sep/2026, entorno **NUBE** (`cloud_default`, `data/raw` ausente, corpus `montado=NO`, `archivos_examinados=0`), sobre `origin/main = f5a52272a8208eaf56f3b6d5db9531786d0d6534`.

**Regla consumidora:** `familia.union.libre` (`R5.3`, `canon/modelo-decision-v4_0.md:537`), `milpa/tramite.yaml:990`, `situacion: primera_union`, `tier: FUERTE`.

---

## 0 · A.8 — qué ya existe, y el defecto material que aparece al mirarlo

### 0.1 · La salida de la herramienta, cruda

```
$ python3 tools/ya_medido.py familia.union.libre
  términos de búsqueda (match exacto): familia.union.libre
  -- milpa/tramite.yaml -- :990  situacion=primera_union tier=FUERTE
       veredicto=CORROBORADA  p=0.190500  [CORROBORADA]
  -- milpa/tramite-ola5-propuesta-v0.yaml -- (sin apariciones)
  -- data/corrida0 (RESULT + ejecución + sello) -- (sin apariciones)
  -- canon/modelo-decision-v4_0.md §7 -- (sin apariciones)
  -- forense/notas/*-L*-*.md --
       2026-09-02-MAESTRA35-L7-resultados.md:20 · 2026-09-02-MAESTRA35-L7-spec.md:49
  -- forense/prereg-caja/S*-spec-*.md -- (sin apariciones)
```

Cero `CALC`. La resolución de códigos, universo y join, en cambio, **ya está
hecha y verificada línea por línea contra el FD** por `ACTO MAESTRA35-L7`
(2/sep/2026); esta spec la reverifica por archivo (§1) y la eleva a las dos
capas de `D-15`.

### 0.2 · El defecto material: el payload declarado no produjo el número

`data/corrida0/demanda-resultados.tsv`, filas `RES-0043` y `RES-0044`,
verbatim de las columnas que importan:

```
RES-0043  valor=0.1905   payload=eder_2017_eder2017_bases_csv
          sha=bcc7eb90c2d016976fd8ba24528ce614bf4db0c29a1e3e0cf674bdfb024de0e3
          clase=MEDIDO·p(prevalencia bruta ponderada 15+, tasa base; ENADID 2023, p3_27_ag)
RES-0044  valor=0.8095   payload=eder_2017_eder2017_bases_csv   (mismo sha, misma clase)
```

**El `payload` dice EDER 2017; la `clase` dice ENADID 2023.** Y
`milpa/tramite.yaml:1005` confirma de dónde salen las cifras: *«ENADID 2023:
15+ condicional a casada(o)/unión libre, `p3_27_ag`, n = 152 950»* — `n` de
ENADID, no de EDER (EDER aporta 18 687 personas).

Consecuencias, las tres, sin colapsarlas:

1. **`E.2` rompería en silencio.** Un `verify` resolvería `bcc7eb90…` (el ZIP
   de EDER) como INPUT de un número calculado sobre otro instrumento. El hash
   *coincidiría* y la cadena sería falsa.
2. **ENADID 2023 es un payload invisible para la demanda.** `grep ENADID
   data/corrida0/demanda-corridas.tsv` → **0 aciertos**, pese a que
   `enadid2023_base_datos_csv` está en el manifiesto. El instrumento que
   produjo la cifra activa no aparece en ninguna corrida.
3. **No hay control positivo posible para esta corrida.** `A-DELTA-VS-GEN1`
   sale **`NO-APLICA-ESTIMANDO-DISTINTO`**, declarado y no calculado. Comparar
   *tipo de primera unión* (retrospectivo, por cohorte) contra *situación
   conyugal actual* (transversal, 15+) sería exactamente el promedio de
   preguntas distintas que `milpa/tramite.yaml:1003` prohíbe: *«no se
   promedian, miden preguntas distintas»*.

Esta spec **no corrige `milpa/`** (no es su perímetro) y **no borra nada**:
deja el defecto asentado con su comando, y la celda ENADID queda como fila
propia del mapa de este acto, con su propio sucesor.

---

## 1 · A.15 — los reactivos existen, verificados **por archivo**

### 1.1 · Payload y codebook, resueltos por manifiesto

| | `payload_id` | archivo | `sha256` |
|---|---|---|---|
| microdato | **`eder_2017_eder2017_bases_csv`** | `eder2017/eder2017_bases_csv.zip` | `bcc7eb90c2d016976fd8ba24528ce614bf4db0c29a1e3e0cf674bdfb024de0e3` |
| codebook | `eder_2017_eder2017_fd` | `eder2017/eder2017_fd.pdf` | `dd4d93114a38e80192bbc29a4a4ab7fba6e4bce0067ecfcdbb4540ada5890541` |
| receta oficial | `eder_2017_eder2017_descripcion_calculor` | `eder2017/eder2017_descripcion_calculoR.pdf` | `01c21e5e4879fb44e7da477ebbacc014f1e59ec145c551e912063eaaa6ff2e6f` |

### 1.2 · Las secciones del instrumento, del índice del codebook

El FD de EDER 2017 es un PDF; el inventario canónico lo indexa con **1 422
entradas de variable** bajo un único payload (`eder2017/eder2017_fd.pdf`).
Las cinco tablas del microdato, verificadas contra el ZIP real, no contra el
nombre del FD:

```
$ python3 -c "…" data/inventario-reactivos-v1_2.tsv  # payload eder2017/eder2017_bases_csv.zip
  antecedentes.csv (52 col) · historiavida.csv (200 col) · hogar.csv (13 col) ·
  persona.csv (57 col) · vivienda.csv (109 col)
```

### 1.3 · Tres archivos, tres papeles — y ninguno los tiene todos

Este es el punto de `A.15(c)` en esta corrida: **el desenlace, el ponderador
y el diseño viven en tres archivos distintos**, y un medidor que los buscara
todos en `historiavida.csv` no encontraría dos de los tres.

| archivo | variable | etiqueta oficial (FD) | papel |
|---|---|---|---|
| `historiavida.csv` | **`edo_civil1`** | *«Estado civil primera unión»* | **desenlace** |
| `historiavida.csv` | `anio_retro` | año de la fila del panel retrospectivo | orden para «primer no-cero» |
| `historiavida.csv` | `anio_nac` | *«Año de nacimiento»* | eje de cohorte (secundario) |
| `historiavida.csv` | `folioviv`·`foliohog`·`id_pobla` | *«Identificador de la vivienda / del hogar / de la persona»* | llave de persona |
| `antecedentes.csv` | **`factor_per`** | *«Factor de expansión»* | **ponderador de persona** |
| `vivienda.csv` | **`est_dis`** | *«Estrato de diseño muestral»* | estratificación del bootstrap |
| `vivienda.csv` | **`upm`** | *«Unidad primaria de muestreo»* | conglomerado re-muestreado |

Join declarado: persona = `(folioviv, foliohog, id_pobla)` contra
`antecedentes.csv`; vivienda = `folioviv` contra `vivienda.csv`.
`ACTO MAESTRA35-L7` verificó **0 huérfanos por ambos lados** sobre las 18 689
personas del universo; esta corrida **lo vuelve a contar** (`G-N-SIN-FACTOR-PER`,
`G-N-SIN-VIVIENDA`) en vez de heredarlo, porque un conteo heredado no es un
conteo.

### 1.4 · El catálogo de `edo_civil1` — leído del FD, no del nombre

El catálogo tiene **27 códigos**, verificados línea por línea contra
`eder2017_fd.pdf` por `ACTO MAESTRA35-L7`
(`forense/notas/2026-09-02-MAESTRA35-L7-P0-censo.md:134`). Las dos ramas:

| rama | códigos | qué son |
|---|---|---|
| **`LIBRE`** | `{1, 12, 13, 14, 17, 18, 126}` | inicio de unión libre, **y** las transiciones *«posterior a inicio de unión libre»* — el código confirma que la unión empezó como libre aunque la fila de inicio esté censurada por el borde del panel |
| **`DIRECTO`** | `{2, 3, 4, 26, 27, 28, 46, 47, 48}` | matrimonio civil / religioso / ambos, inicio o transición |

**Lo que no se fuerza:** el código `37` (n = 2 en el censo de L7) queda
**sin clasificar y contado** (`A-N-SIN-CLASIFICAR`), no se adjudica a ninguna
rama. Los códigos de disolución pura `{6,7,8,60,70,80}` (divorcio, separación,
viudez) **nunca aparecen como primer-no-cero** — verificado, 0 casos: no hay
censura izquierda que corregir. Si esta corrida encuentra alguno,
`A-CENSURA-IZQUIERDA = DETECTADA` y el punto se reporta con esa marca, sin
recodificar sobre la marcha.

Los códigos se leen **como cadena cruda** (`dtype=str`): `'1'` y `'1.0'` no
son el mismo texto y `pandas` produce uno u otro según el `dtype` inferido.
`G-VEREDICTO-TIPO-CODIGO` lo declara antes de usar el mapa.

---

## 2 · Qué mide, exactamente

### 2.1 · Universo

Personas de EDER 2017 (unidad: persona de 20 a 54 años, FD §1.1.2) con al
menos un `edo_civil1` distinto de `0` en `historiavida.csv`. El **primer**
código no-cero por persona, en orden ascendente de `anio_retro`, es el
desenlace. Entran las que además tienen `factor_per` finito y `> 0` en
`antecedentes.csv`.

Referencia del censo de L7 (**no** es el resultado de esta corrida, y se
vuelve a contar): 23 831 personas en `antecedentes.csv`, 18 689 con primer
código no-cero (78.4%), de las cuales 18 687 clasificables.

### 2.2 · Estimando

`A-P-LIBRE` = `Σ(w·d)/Σ(w)` sobre el universo, con `w = factor_per` y
`d = 1[edo_civil1 ∈ LIBRE]`. `A-P-DIRECTO` se **cuenta directamente** sobre
`d = 1[edo_civil1 ∈ DIRECTO]` — **nunca** `1 − A-P-LIBRE`, porque el código
`37` está fuera de las dos ramas y el complemento lo borraría.
`A-SUMA-LIBRE-DIRECTO-MAS-SIN-CLASIFICAR` cierra la partición y sale como
`RESULT`. **DESCRIPTIVO**; ningún `RESULT` es causal.

### 2.3 · Diseño — el IC nace donde GEN1 puso `NO-APLICA`

`milpa/tramite.yaml:1007` declara `ic95: "NO-APLICA"` para esta regla. EDER
2017 **sí trae diseño** (`est_dis`, `upm`, `factor`, `factor_per` en el FD —
es el mismo hallazgo que tumbó `FP-201` y dio a `CALC-EDER-0001` su IC de
diseño, `ADR-501`, 14/sep/2026). Bootstrap de `upm` con reemplazo **dentro de**
`est_dis`, conservando el número de UPM por estrato, 2 000 réplicas,
`numpy.PCG64`, semilla `20260915`, percentiles 2.5/97.5. `est_dis`/`upm` como
**cadena cruda opaca**. Estrato con UPM única se re-muestrea a sí mismo,
**no se colapsa ni se descarta**; si el conteo es `> 0`, `A-METODO-IC` sale
`IC-CON-ESTRATOS-DE-UPM-UNICA` y el IC se lee como **límite inferior** de la
anchura verdadera. Precedente directo: `CALC-EDER-0001` reportó 3 estratos de
UPM única sobre este mismo instrumento.

### 2.4 · Eje secundario, declarado y no adoptable

`B-*`: cohorte de nacimiento (`anio_nac`) en cuatro tramos
(`≤1970`, `1971-1980`, `1981-1990`, `1991+`), **descriptivo**, con su propio
IC de diseño por celda. No entra a ningún consumidor: `milpa/` ya trae una
segmentación por cohorte sellada y **esta corrida no la sucede** — la emite
para que mesa vea si la dirección se sostiene bajo el ponderador y el diseño
de esta spec, nada más.

---

## 3 · Control positivo y adopción

**No hay control positivo contra GEN1 para el punto principal**, y decirlo es
el entregable, no la falta: `A-DELTA-VS-GEN1 = NO-APLICA-ESTIMANDO-DISTINTO`
(§0.2). La única comparación autorizada es contra el censo de `MAESTRA35-L7`,
que midió **este mismo estimando** sobre **este mismo payload** — y es una
comparación de **conteos sin ponderar**, no de `p`:

| `RESULT` | contra qué (censo L7, 2/sep/2026) | vocabulario |
|---|---|---|
| `A-N-PRIMER-NO-CERO` | `18689` | `COINCIDE` / `DIFIERE:<delta>` |
| `A-N-LIBRE-SIN-PONDERAR` | `9044` | idem |
| `A-N-DIRECTO-SIN-PONDERAR` | `9643` | idem |
| `A-N-SIN-CLASIFICAR` | `2` | idem |

`DIFIERE` **no** autoriza tocar el mapa de códigos ni el orden de
`anio_retro`: se reporta y la lectura es de mesa. `A-ADOPCION` sale
`LISTADO-PARA-MESA` / `NO-ADOPTABLE-NO-ESTIMABLE`; **este acto no escribe
cita en `milpa/`**, y la celda ENADID que hoy ocupa `RES-0043`/`RES-0044`
**no se toca** — sustituirla es decisión de mesa, no de esta spec.

**Contaminación declarada (`ADR-46`).** Al congelar, la sesión ya había leído
`p = 0.1905` y `0.8095` (GEN1/ENADID), los conteos sin ponderar del censo de
L7, el mapa de 27 códigos y la segmentación por cohorte sellada. No es ciega.
Lo genuinamente desconocido al congelar: el `p` **ponderado por `factor_per`**
de esta partición (el censo de L7 publica proporciones sobre conteos crudos,
48.4% / 51.6%, que **no** son el estimando de esta spec), la anchura del IC de
diseño, cuántos estratos quedan con UPM única en el universo de personas, y
si los códigos llegan como `'1'` o `'1.0'`.

---

## 4 · Lo que NO hace

No abre microdato · no corre el medidor (lo escribe el acto de CAJA a partir
de este contrato) · no mide ENADID 2023 · no promedia EDER con ENADID · no
corrige `milpa/tramite.yaml` ni `demanda-resultados.tsv` (derivado) · no
sucede la segmentación por cohorte ya sellada · no toca `CALC-EDER-0001` ni
`CALC-EDER-0002` (otro estimando, otra regla) · no toca `CORR-0011`,
`CORR-0012` ni `CORR-0014`.
