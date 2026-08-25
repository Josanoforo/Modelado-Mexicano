# ACTO EVAL-COMPARTAMOS-LLAVE3 — el primer renglón de la clase (iii)
### Nota de cierre · 25 de agosto de 2026 · entorno UBUNTU · modelo Opus · `ADR-162`

> | | |
> |---|---|
> | **ENCARGO** | `forense/encargos/2026-08-25-EVAL-COMPARTAMOS-LLAVE3.md` (archivado en este mismo acto, `A.3`) |
> | **FIRMA QUE EJECUTA** | Mesa (D2), 24/ago/2026, verbatim: *«Valor propio, GO, pero asegurándonos que el motor lo soporta y que va ligado a lo que queremos construir.»* |
> | **QUÉ PRODUJO** | Un valor de vocabulario nuevo con criterio propio (`DISENO_EXPERIMENTAL`) · la primera apertura a nivel de columna del microdato del RCT de Compartamos · la **primera fila de clase (iii)** del registro de llaves (`EXP-COMPARTAMOS-1`, `SELLADA_NO_EJERCIDA`) · y dos negativos medidos que son el hallazgo principal |
> | **CONTADOR** | **Cero directo**, declarado desde el encargo (v2.3). Llaves: `3` de `3` → `3` de `4` — sube el denominador, no el numerador |
> | **PERÍMETRO** | `data/diseno-muestral.yaml` · `forense/registro-llaves-identificacion-v1_0.md` · `forense/firmas-pendientes.tsv` · `canon/gobernanza-v1_15.md` · `canon/estado-programa-v1_10.md` · esta nota · el encargo. **No se tocó `milpa/`** |

---

## 0 · El titular, en tres frases

El censo de diseño gana su quinto valor y su primer criterio propio para experimentos, escrito dentro del propio yaml y no en esta nota. El registro de llaves gana su **primer renglón de clase (iii)** desde que `ADR-67(c)` lo abrió el 11/ago/2026 — la clase que `ADR-57(c)` definió hace veintiún días y que nadie había podido poblar.

Y el amarre al motor que la firma de mesa exigió — *«asegurándonos que el motor lo soporta y que va ligado a lo que queremos construir»* — **se midió, y da negativo por las dos mitades**: ninguna necesidad del programa nombra esta evidencia, y ninguna de las tres piezas donde el motor podría consumirla tiene clase para ella. Eso no invalida el GO: lo convierte en el hallazgo del acto. La llave existe, está sellada, y **no puede ejercerse todavía por dos razones distintas**, las dos ahora con fila de tablero.

---

## 1 · Arranque

**1 · REPO.** Clon existente `/home/pc0/Modelado-Mexicano`; worktree propio `/home/pc0/mm-eval-compartamos`, rama `eval-compartamos`. No se clonó nada nuevo.

**2 · SHA.** Base al arrancar: `21ab042` (`Merge pull request #326`, `ACTO ADQ-CORRE-R74R75`). `origin/main` **se movió tres veces mientras este acto estaba abierto**, y las tres se absorbieron antes de cerrar: a `e8ce5ef` (`PR #327`, `ACTO SPEC-R10.1-v2`, que trajo `ADR-159`), fusionado sin conflicto antes de numerar; a `e70b424` (`PR #328`, `ACTO R34-CONDA-V2`), que se llevó `ADR-160` **y** las filas `FP-129`/`FP-130` — los tres rótulos que este acto ya había candidateado; y a `a5f1bf6` (`PR #329`, `ACTO BANDAS-DOC-6`), que se llevó el `ADR-161` al que este acto acababa de renumerar. Se rebasó sobre cada punta y se renumeró cada vez (ver §9). Base final: **`a5f1bf6`**.

**3 · `data/raw`.** Enlace simbólico al corpus compartido (`/home/pc0/mm-corpus/raw`). Cero descargas en todo el acto.

**4 · ENTORNO — las tres partes de `A.2`.**

| parte | comando | resultado |
|---|---|---|
| variable de entorno | `echo $CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE` | `<sin_variable>` → no es nube |
| sonda de red | `curl -o /dev/null -w '%{http_code}' https://www.inegi.org.mx/` | `HTTP 200` en 0.59 s |
| **corpus montado** | `ls data/raw/ \| head -1` | `2005trim1_csv.zip` — **321 entradas en la raíz**, corpus presente |

Las tres coherentes con UBUNTU. La tercera es la que decide: este acto abre microdato, y sin bytes no hay acto (`A.2`, el defecto medido el 5/ago que la creó).

**Herramientas.** `iconv` presente. **`unzip` NO está en la caja** — se abrió el paquete con `zipfile` de Python 3, mismo mecanismo que `REG-LOTE3` ya había usado sobre este mismo zip. `pandas` 2.3.3 y `pypdf` 6.16.1 presentes; `pyreadstat` no.

**5 · ESPEJO.** Nada, por instrucción del encargo.

---

## 2 · Verificación de existencia — las dos premisas del encargo, comprobadas antes de escribir

**Premisa 1: el paquete existe en el corpus.** Cierta. `data/manifiesto.yaml`, entrada `116334_v1`, raíz `descargas_mx`, archivo `Descargas Manuales/116334-V1.zip`. Resuelto contra `data/raices.local.yaml` (`descargas_mx: /mnt/c/Users/PC0/Descargas MX`), el archivo está en disco, 1,404,772 bytes, y su **sha256 coincide** con el declarado en el manifiesto: `776d56bf91535beaecef9480c352b022c3aec1ec7fae36c969ccdf6c8cc89d1c`. 98 entradas en el zip.

**Premisa 2: el registro no tiene ningún renglón de clase (iii).** Cierta, y el camino a comprobarlo trae su propia lección. Las dos recetas, corridas sobre el archivo **antes** de escribir la fila nueva:

```
$ sed -n '/^## 3 · Tabla de llaves/,/^## 4/p' forense/registro-llaves-identificacion-v1_0.md \
    | command grep -E '^\| `' | awk -F'|' '{print $11}' | command grep -c '(iii)'
1
$ sed -n '/^## 3 · Tabla de llaves/,/^## 4/p' forense/registro-llaves-identificacion-v1_0.md \
    | command grep -E '^\| `' | awk -F'|' '{print $11}' | command grep -cE '^ *\*\*\(iii\)\*\*'
0
```

**El `1` es un falso positivo, y la cifra correcta es `0`.** El único `(iii)` que había en la columna `clase_ADR57c` vive dentro de la fila `R5.1-D2`, en la frase que lo **descarta**: *"Falla (i) por definición (2018 y 2022 no son los mismos sujetos) y (iii) por definición (no hay aleatorización de terceros)"*. Es una **mención**, no un uso. La receta anclada al uso —la clase se declara siempre como `**(iii)**` en negritas al inicio del campo, igual que `**(i)**` y `**(ii)**`— da `0`, que además coincide con lo que §8.1 del propio registro ya había tabulado a mano el 20/ago/2026 (*"(iii) experimento de terceros | 0 | 0"*). Universo del negativo, declarado (`A.13`): **1 archivo, 3 filas de datos**, la tabla completa de §3, no una muestra.

**Premisa 3: el vocabulario del censo no tiene valor experimental.** Cierta — `MAPEADO`, `SIN_DISEÑO_PUBLICADO`, `PENDIENTE`, `NO_APLICA_REGISTRO_ADMINISTRATIVO`, y la fila del paquete estaba en `PENDIENTE` con la razón escrita por `ACTO RECENSO-DISEÑO-2`. Es exactamente lo que `FP-123` puso ante mesa.

---

## 3 · Tarea 1 · El valor propio, con su criterio dentro del yaml

`DISENO_EXPERIMENTAL` entra al bloque de vocabulario de `data/diseno-muestral.yaml`, **con su criterio operable escrito ahí mismo** — no en esta nota, no en el ADR: quien lea el censo dentro de seis meses tiene que poder aplicar el criterio sin abrir el historial.

**Qué dice el criterio.** Los tres campos heredados (`ponderador`/`estrato`/`upm`) se escriben `no aplica — experimento` **con la razón**, nunca vacíos ni omitidos. Encima de ellos, **cinco campos propios, los cinco obligatorios y los cinco con cita**:

1. **`unidad_y_nivel_aleatorizacion`** — qué objeto se sorteó, a qué nivel, cuántas unidades por brazo, y si hubo bloqueo o estratificación del sorteo.
2. **`brazos`** — cuántos, cómo se llaman, qué recibió cada uno.
3. **`variable_asignacion`** — el **nombre de columna** en el microdato que porta la asignación, verificado constante dentro de la unidad de aleatorización.
4. **`cumplimiento_y_atricion`** — las columnas que miden toma del tratamiento y pérdida de seguimiento, con su universo; *"el paquete no lo reporta"* si no las trae, nunca silencio.
5. **`cita_publicacion`** — la referencia del artículo que el paquete replica, con su procedencia.

**El tercero es el que da o quita la etiqueta.** Sin nombre de columna de asignación verificado en el microdato, la fila no es un diseño experimental: es un paquete de réplica sin asignación legible. Es la diferencia entre "esto parece un RCT por los nombres de los do-files" (que es lo que el listado de archivos de `RECENSO-DISEÑO-2` podía sostener) y "esto es un RCT y aquí está la columna".

**Y el criterio declara sus límites.** El estado no estima ningún efecto, no adjudica llave de identificación (eso vive en el registro de llaves) y **no autoriza al motor a consumir el paquete**. Las tres cosas quedan escritas dentro del yaml para que nadie las herede por omisión.

`FP-123` → **`FIRMADA`**, con la firma D2 verbatim en su columna `firmada_en`, y `ejecutada_en` lleno en el mismo acto (una firma resuelve la pregunta de mesa; no escribe el archivo — por eso las dos columnas existen desde `ADR-94`).

---

## 4 · Tarea 2 · La apertura a nivel de columna

Se abrió `Compartamos_AEJ/Main/data/analysis_data_AEJ_pub.dta` con `pandas.io.stata.StataReader` — **nombres y etiquetas**, más los conteos necesarios para identificar la estructura. **Ningún efecto se estimó**, y ni siquiera se calculó la toma de tratamiento por brazo: la diferencia entre brazos es medición, no censo de identificación.

**Lo que trae el archivo:** 124 variables, 21,523 filas, sin etiqueta de dataset, con solo dos conjuntos de etiquetas de valor (`missing`, `YesNo`).

**La variable de asignación existe, y son dos.**

| variable | etiqueta | dónde vive | reparto |
|---|---|---|---|
| **`Treatment`** | "Treatment" | ola de seguimiento (16,560 no nulos; nula en las 4,963 filas de "Baseline only") | 8,262 tratamiento · 8,298 control |
| **`BTreatment`** | "Treatment Assignment" | línea base (6,778 no nulos) | 2,770 tratamiento · 4,008 control |

La codificación no se infirió: el propio paquete la escribe, *"treatment assignment (1=Treatment, 0=Control)"* (`Source/Analysis/tables_descriptive/Table-1.do:447-448` y `Appendix-Table-1.do:160-161`).

**La aleatorización es por conglomerado, y se derivó — no se supuso.**

```
clusters (ola de seguimiento) con más de un valor de Treatment:  0 de 238
BClusters (línea base) con más de un valor de BTreatment:        0 de 34
```

238 conglomerados en seguimiento (**120 tratados / 118 control**) y 34 en línea base (**17 / 17** — partición exacta que sugiere sorteo pareado; el paquete no trae el documento de aleatorización, así que no se afirma). Lo confirma el propio código por la vía independiente de la inferencia: las **60** regresiones de `Main/Compartamos-AEJ-tables-2-8.do:9-79` agrupan sus errores estándar en `vce(cl cluster)`, y la nota al pie de las tablas dice con esas palabras *"standard errors clustered by the unit of randomization"* (`Table-1.do:453`).

**Unidad de análisis y N.** La **persona** — mujer de 18 a 60 años (`F5_1` va exactamente de 18 a 60 en el dato, y las notas del paquete dicen *"Respondents are Mexican women aged 18-60 and all reside in outlying areas of Nogales"*, `Appendix-Table-1.do:159-160`). Una fila por persona-encuesta. **N = 16,560** en la ola de seguimiento; 4,963 en "Baseline only"; 1,823 personas aparecen en las dos (`InPanel`). **El archivo público no trae identificador de persona ni de hogar** — barrido sobre las 124 columnas por `weight|wt|pond|fac|id|folio|hh`: ninguna columna de expansión, ninguna llave de persona. Eso cierra por sí solo la puerta a leer esto como panel.

**Cumplimiento y atrición: el paquete los reporta, con columna propia.**

| qué | columna | cifra (universo completo de la ola, **sin desglose por brazo**) |
|---|---|---|
| toma de tratamiento, registro administrativo | `in_admin` — "Any loan from Compartamos - admin data" | 2,048 de 16,560 = **12.37%** |
| toma de tratamiento, declarada en encuesta | `Q21_3_comp` — "Any loan from Compartamos - survey data" | 1,331 de 15,845 = **8.40%** |
| conducta de pago | `A_ever_late_not_cond` — "Client was ever late on payments" | (presente, no cuantificada aquí) |
| atrición | `attrited` / `surveyed` | **1,090 de 2,912** buscadas = **37.43%**; 1,822 sí encontradas |

El universo de la atrición no es el de la ola: es la muestra **buscada** para seguimiento, definida en el propio paquete como `!mi(attrited)` (`Source/ado/Enumerated-types/compartamos_sample.mata:196-197`). Y el paquete no se limita a marcarla: le dedica una tabla entera de atrición **diferencial** — `surveyed` regresado sobre la asignación y sobre sus interacciones con las covariables, agrupado por `BCluster` (`Appendix-Table-1.do:117`, "Appendix Table 1: Attrition").

**Lo que el paquete NO trae, y es hallazgo.** No hay codebook. El `Readme.pdf` remite explícitamente a un *"Data Appendix"* para la definición de cada variable — y ese apéndice **no viene dentro del zip**. Tampoco viene la cita bibliográfica: barrido sobre los 98 archivos por `angelucci|karlan|zinman|american economic journal|doi|10.1257` → cero coincidencias fuera de los archivos de ayuda de paquetes SSC de terceros. Lo más que el zip dice de sí mismo es *"Readme for AEJ Compartamos source code"* y *"COPYRIGHT 2015 American Economic Association"* (`LICENSE.txt:11`). **La cita completa sale de una tabla del propio repositorio, no del paquete**: *"Microcredit Impacts: Randomized Microcredit Program Placement Experiment" · "OpenICPSR; Compartamos Banco; Angelucci, Karlan y Zinman"* (`data/mapa-ext-academico-2026-08-06.tsv:4`). El volumen y las páginas del artículo no se declaran: no están en el corpus, y `openicpsr.org` no se alcanzó en este acto.

**Discrepancia declarada, no resuelta.** Esa misma fila de `mapa-ext-academico` dice *"16,560 mujeres; 250 vecindarios"*. El N coincide exacto; el número de conglomerados **no** — el microdato trae 238 en la ola de seguimiento. No se corrige esa tabla desde aquí: está fuera del perímetro del acto. Queda escrito en el campo `notas` de la fila del censo y aquí.

---

## 5 · Tarea 3 · El renglón de la llave, y el id que no fue el propuesto

Entra `EXP-COMPARTAMOS-1` a `## 3 · Tabla de llaves`, naciendo `SELLADA_NO_EJERCIDA`, con clase **(iii)** citando `ADR-57(c)` verbatim (`canon/gobernanza-v1_15.md:629` — el inciso; `:623`, que es como §0 del registro lo cita, es el título del ADR). Detalle completo de la alta: §10 del propio registro.

**El id se derivó, y salió distinto del que el encargo proponía.** El encargo sugería `CAL-EXP-1` y autorizaba expresamente derivarlo. La convención de las tres filas existentes es que el `llave_id` **nombra el objeto del modelo al que la llave sirve**: `CAL-G3` → el generador `G3`; `R5.1-D2`/`R5.1-D3` → la regla `R5.1` del Hito D con ordinal de diseño. Y el prefijo `CAL-` es de la familia de actos de **calibración de un coeficiente nombrado** (`CAL-G3` ×222 menciones en el árbol, `CAL-CONF` ×49, `CAL-ENOE` ×19).

Aquí **no hay coeficiente nombrado** — ése es justamente el hallazgo de §6. Un id `CAL-EXP-1` presupondría la pieza que falta y la escondería detrás de un rótulo que suena a que existe. `EXP-COMPARTAMOS-1` nombra lo que sí existe (la clase, el objeto, el ordinal de diseño que `R5.1-D2`/`-D3` ya usan) y deja el hueco visible donde tiene que verse: en la columna `coeficiente_o_regla`, que dice `NO-ENCONTRADO` con su universo.

**Nace sin pre-registro, a diferencia de las otras tres.** No hay diseño que pre-registrar mientras nadie declare qué θ o qué generador informa esta evidencia. Por eso `preregistro_ref` = **NINGUNO** y la columna `escala_del_veredicto` dice que la fija la spec B-bis que aún no existe: escribirla hoy sería fijar la escala de un veredicto antes de tener el diseño — el defecto exacto que la fila `R5.1-D2` dejó documentado en esa misma columna el 4/ago.

**Contador.** `3` de `3` → **`3` de `4`**. El numerador **no** se mueve: el acto abre el renglón, no ejerce la llave — misma disciplina de `ACTO FICHA-R51-D3` (§6 del registro). Derivado con la receta congelada de §4, no tecleado:

```
$ sed -n '/^## 3 · Tabla de llaves/,/^## /p' forense/registro-llaves-identificacion-v1_0.md \
    | command grep -E '^\| `' | awk -F'|' '{print $6}' | command grep -c 'EJERCIDA_'
3
$ sed -n '/^## 3 · Tabla de llaves/,/^## /p' forense/registro-llaves-identificacion-v1_0.md \
    | command grep -cE '^\| `'
4
```

La tabla de §8.1 del registro queda: **(i) 1 · (ii) 2 · (iii) 1**.

---

## 6 · Tarea 4(a) · A qué necesidad liga — `NO-ENCONTRADO`, con universo

**Universo declarado (`A.13`): las 37 filas de datos de `data/curacion-registro/necesidad-objeto-modelo.tsv`, todas, 1 archivo examinado.** Comando y control positivo en la misma pasada:

```
$ tail -n +2 data/curacion-registro/necesidad-objeto-modelo.tsv | wc -l
37
$ command grep -c -i "compartamos\|microcr\|openicpsr\|116334\|aleatoriz\|rct\|experiment" \
    data/curacion-registro/necesidad-objeto-modelo.tsv
0
$ command grep -c -i "credito" data/curacion-registro/necesidad-objeto-modelo.tsv     # control positivo
1
```

**Cero de 37.** Ninguna necesidad nombra este paquete, ni microcrédito, ni una evaluación aleatorizada. El control positivo prueba que el comando sí examinó el archivo — la clase de defecto que `A.13` existe para atrapar.

**Y no es que el modelo no tenga crédito.** Tiene dos reglas:

| regla | dónde | qué dice |
|---|---|---|
| `dinero.credito.scoring_alternativo` | `canon/modelo-decision-v4_0.md:500` | el segmento popular paga sobreprecios hasta un techo; la mora regulada se estabiliza en 15-20% |
| `dinero.credito.baja_friccion_usura_dano_downstream` | `canon/modelo-decision-v4_0.md:501` | baja fricción **más** tasa usuraria **más** reporte invisible producen daño downstream |

Las dos son sobre **precio, mora y daño**, ninguna sobre **acceso aleatorizado**. Y la necesidad `N19`, que cubre a la primera, cita otra fuente por completo — `NBER_RappiCard` (`milpa/procedencia.yaml:722`), un estudio de scoring por huella digital.

**Hallazgo lateral del mismo cruce, no buscado:** la terna del curador **no cubre** `dinero.credito.baja_friccion_usura_dano_downstream`. De las dos reglas `dinero.credito.*` del motor, solo una tiene necesidad declarada. Se registra aquí; corregir la terna está fuera del perímetro de este acto.

**Consecuencia, y es la que va a mesa:** hay evidencia causal de primera clase —un sorteo por conglomerado, con 238 unidades, cumplimiento y atrición medidos, publicada y replicable— **sin ningún consumidor declarado en el programa**. Eso es `FP-132`.

---

## 7 · Tarea 4(b) · Dónde lo consumiría el motor — el conducto no existe

Se derivó contra las tres piezas donde podría vivir. Las tres, negativas.

**(1) `milpa/procedencia.yaml` — siete clases, ninguna de evidencia identificada de terceros.** `MEDIDO` · `DERIVADO` · `ORDINAL→CARDINAL` · `ASIGNADO` · `AJUSTADO` · `MEDIDO·PARCIAL(x)` · `MEDIDO·NACIONAL`. La más cercana es `AJUSTADO`, y su propia definición la descarta: *"reproduce los momentos observados ... **NO está identificado causalmente**. Contesta CUÁNTO, nunca SI EL PATRÓN EXISTE (ADR-47)"*.

**(2) El contrato de celda-D — siete valores de `diseno_datos`, con la clase (ii) y sin la (iii).**

```
diseno_datos: panel | pseudo_panel | transversal | registro_administrativo |
              experimento_natural | auditoria_campo | enlace_ecologico
```

`propuesta-motor-adaptativo-celda-v0_3.md:56-57`, **idéntico** en `propuesta-motor-adaptativo-celda-v0_4.md:49-50`, y `propuesta-motor-adaptativo-celda-v0_5.md` no lo toca (verificado: cero menciones de `diseno_datos` en v0.5). Tiene `experimento_natural` —que es exactamente la clase (ii) de `ADR-57(c)`, la que `R5.1-D2` y `R5.1-D3` ejercen— y **no tiene** la (iii). El hueco no es de olvido: es que nadie había traído una llave de esa clase.

**(3) `milpa/refutations.yaml` — tres tipos, ninguno sobre clase de evidencia.** `A · mecánica` · `B · paramétrica` · `C · de lectura`. Son tipos de **prueba**, no de procedencia.

**Y sin embargo el motor ya consume un RCT de terceros, dos veces, por la puerta de atrás y sin clase.** `Progresa_RCT` —**el ejemplar que `ADR-57(c)` nombra para definir la clase (iii)**, "clase Progresa/Oportunidades"— aparece:

- en `fuente_citada` de la regla `dinero.planeacion.formal_estable` (`milpa/procedencia.yaml:715`), bajo clase `ASIGNADO`, con un `que_sostiene_de_verdad` que dice literalmente *"Progresa prueba la DIRECCIÓN causal (estabilizar ingreso alarga horizonte), no la proporción"*;
- en `fuente` de una refutación (`milpa/refutations.yaml:227`), cuya `evidencia_contraria` termina en *"Progresa aleatorizado"*.

Es decir: la distinción que `ADR-57(c)` selló —evidencia identificada frente a asociación— **ya está siendo usada en el ejecutable sin que exista un campo que la marque**. Un lector del yaml no puede distinguir hoy un `ASIGNADO` sostenido por un RCT de un `ASIGNADO` sostenido por un reporte de consultoría.

### 7.1 · PROPUESTA-SELLADA, 25/ago/2026 (`ACTO SELLA-AGO25-F`, L7/`FP-131`, firma de mesa verbatim "sí") — escrita, no implementada

Tres piezas, en este orden, ninguna ejecutada en este acto (`milpa/` no se toca, y el contrato de celda-D no es de este perímetro). Va a mesa como `FP-131`:

1. **Un valor nuevo de `diseno_datos`** en el contrato de celda-D: `experimento_aleatorizado_terceros`, con su `vocabulario_version` propia — el mecanismo de versión de vocabulario ya existe y ya se usó para `BASELINE_INGENUO`/`ENSAMBLE` en v0.5, así que no hay maquinaria que inventar.
2. **Una octava clase de procedencia** en `milpa/procedencia.yaml` que marque el número como sostenido por evidencia identificada de terceros, con **dos campos obligatorios**: la cita de la publicación (que es lo que `ADR-57(c)` exige textualmente, *"usado como evidencia (a) con su cita"*) y el `llave_id` del registro de llaves que la respalda. Sin el segundo campo la clase sería una etiqueta sin trazabilidad, que es el defecto que `MEDIDO·PARCIAL(x)` evitó al obligar a listar los ejes.
3. **Qué hacer con las dos citas de `Progresa_RCT` que ya existen** — reclasificarlas bajo la clase nueva, o declararlas excepción fechada con su razón. Dejarlas como están sería sellar una clase nueva y no aplicarla al único caso que ya la necesitaba.

**Lo que la propuesta deliberadamente NO incluye:** nada sobre cómo se pondera, combina o transporta un efecto experimental de terceros a la población del modelo. Eso es una decisión de método, mucho más grande, y no hace falta para responder la pregunta que mesa hizo — que era si el motor *soporta* la evidencia, no cómo la usaría.

---

## 8 · Párrafo a mesa

**Qué se puede ejercer con esto, hoy.** Nada todavía, y la razón no es la que se esperaba. El paquete es sólido y está completamente identificado: sorteo real por conglomerado (238 unidades, 120/118), asignación legible en el microdato con nombre de columna, unidad de análisis y N confirmados (16,560 mujeres de 18-60), cumplimiento medido con registro administrativo del banco (12.37%) y atrición medida con tabla de atrición diferencial propia (37.43% sobre las 2,912 buscadas). Como evidencia de clase (iii), es de la mejor calidad que el programa tiene a la mano — y ahora tiene renglón, que es lo que faltaba desde que `ADR-57(c)` definió la clase el 4/ago.

**Qué falta, y son dos cosas independientes.** **Primera:** nadie ha declarado qué θ o qué generador del modelo informa esta evidencia. El cruce contra las 37 necesidades del curador dio cero. Sin esa declaración no hay spec B-bis que escribir, y sin spec B-bis la llave no se ejerce — es la regla de `ADR-57(c)`, no una preferencia de este acto. **Segunda, y es la que sorprende:** aunque mesa firmara mañana qué θ informa, **el resultado no tendría dónde entrar al ejecutable**. Ninguna de las tres piezas del motor tiene clase para evidencia experimental de terceros, y la comprobación de que el hueco es real —y no un descuido de este acto— es que el motor ya cita `Progresa_RCT` dos veces sin poder marcarlo como lo que es.

**Lo que este acto pide.** Dos firmas, `FP-131` (el conducto) y `FP-132` (el consumidor), en ese orden de dependencia lógica pero no necesariamente de tiempo: `FP-132` puede firmarse primero y dejar la llave esperando conducto; `FP-131` puede firmarse primero y dejar el conducto esperando quién lo use. **Lo que no debería pasar es que se firme una y se dé por atado el motor**: la firma D2 pedía las dos mitades, y las dos están abiertas.

**Una observación que no se convierte en propuesta, a propósito.** El instrumento de seguimiento trae, a nivel de columna, `Q15_2_mean_formal` ("Trust in institutions index") y `Q15_2_mean_people` ("Trust in people index") — medidos en el brazo de un sorteo. Los nombres se parecen a `confianza_institucional` (`G1`) y `radio_confianza` (`G1`/`G5`) del modelo. **Este acto no afirma que sean el mismo constructo**, y esa contención es deliberada: establecerlo exige abrir el reactivo, verificar escala y universo, y una decisión de mesa. Afirmarlo por parecido de nombre sería exactamente lo que `ADR-57(c)` existe para impedir. Queda nombrado en `FP-132` como una de las vías que mesa puede tomar, no como una conclusión.

---

## 9 · Tablero, cascada y suite

**Tablero (`A.12`).**

| fila | movimiento |
|---|---|
| `FP-123` | `ABIERTA` → **`FIRMADA`**, con la firma D2 verbatim en `firmada_en` y `ejecutada_en` lleno el mismo día |
| `FP-131` | **nueva, `ABIERTA`** — mesa decide si el motor gana el conducto para la clase (iii) (la propuesta de §7.1) |
| `FP-132` | **nueva, `ABIERTA`** — mesa decide qué necesidad/θ reclama la evidencia, o declara que se queda sin consumidor |

Las dos filas nuevas citan en `dónde` los archivos nuevos del acto, que es lo que `T22`(b) exige de todo documento nuevo que traiga un marcador de decisión sin resolver.

**Cascada, con TRES renumeraciones.** El ADR de este acto se candidateó primero como `ADR-160`, contra el máximo verificado sobre el árbol ya fusionado con `origin/main = e8ce5ef`. Después:

| fusionó | se llevó | este acto pasó a |
|---|---|---|
| `PR #328` · `ACTO R34-CONDA-V2` | `ADR-160`, `FP-129`, `FP-130` | `ADR-161`, `FP-131`, `FP-132` |
| `PR #329` · `ACTO BANDAS-DOC-6` | `ADR-161` | **`ADR-162`** (las filas de tablero no vuelven a moverse) |

Aplicada cada vez la regla del encargo —*renumera quien fusiona segundo*—, con el máximo re-derivado por `grep` sobre el árbol ya fusionado, nunca por aritmética. Estado final: **`ADR-162`**, **`FP-131`**, **`FP-132`**, sobre `a5f1bf6`.

**Cómo se resolvió la colisión, y qué se verificó.** Los tres archivos que chocaron (`canon/gobernanza-v1_15.md`, `canon/estado-programa-v1_10.md`, `forense/firmas-pendientes.tsv`) se resolvieron **por unión**, nunca eligiendo un lado: el cuerpo del `ADR-160` ajeno queda intacto y el mío entra después como `ADR-162`; las filas `FP-129`/`FP-130` de `R34-CONDA-V2` quedan intactas y las mías entran después; y en `estado` cada entrada de recifrado ajena se conserva completa con la mía antepuesta. Una primera pasada de renumeración tocó por error tres referencias ajenas dentro de líneas compartidas —esas líneas son párrafos enteros donde conviven entradas de varios actos—; se detectó comparando contra `origin/main` y se corrigió restaurando el archivo desde la punta y re-aplicando las ediciones una por una. Verificación final: `161` ADR sin huecos, `132` filas de tablero sin ids duplicados y con 9 columnas cada una, y ninguna referencia ajena movida.

`canon/estado-programa-v1_10.md` recifra `161` → `162` ADR, llaves `3 de 3` → `3 de 4`, y `145` → `146` WARN. Ningún otro contador se mueve.

**Suite.** Corrida con `--baseline`, que es el modo que gobierna (el modo plano da su cifra de siempre y no dice si algo es **nuevo**). Resultado al cierre: **19 FAIL · 146 WARN · LÍNEA BASE VERDE**, sin entradas nuevas frente a `tests/baseline.json`. El movimiento neto de WARN es **+1** sobre la punta (`145`): `+2` de `T22`(a) por `FP-131` y `FP-132`, `−1` porque `FP-123` sale de `ABIERTA` con `ejecutada_en` lleno el mismo día —así que tampoco entra al WARN de `T22`(c)—. Los FAIL propios fueron de `T15` y `T16` (`gobernanza`/`estado` desincronizados tras cada renumeración, y dos cifras de un acto ajeno que mi `+1` volvió históricas — se les puso `{cita-historica}`, que es el mecanismo que la casa ya usa), cerrados dentro del acto. Se verificó también que la base estaba VERDE **antes** de tocar nada, para no atribuirse un desfase heredado — lo estaba. `tests/baseline.json` no se recongela: `ADR-76(f)` exige ADR de mesa para eso y este acto no lo trae firmado.

---

## 10 · Lo que este acto NO hizo

- **No estimó ningún efecto.** Ni siquiera la toma de tratamiento por brazo, que ya sería una diferencia entre brazos. Las cifras de cumplimiento y atrición que aparecen arriba son del universo completo, sin desglose.
- **No tocó `milpa/`.** Ni `procedencia.yaml`, ni `refutations.yaml`, ni `tramite.yaml`. La propuesta de §7.1 está escrita y no implementada, por instrucción expresa del encargo.
- **No tocó el contrato de celda-D** ni subió su versión de vocabulario.
- **No ejerció la llave** `EXP-COMPARTAMOS-1` ni escribió spec B-bis alguna. El numerador de llaves ejercidas sigue en `3`.
- **No movió Hito D** (`18 de 27` al escribir esto), ni el contador de condicionales, ni `4 de 144`, ni ningún tier.
- **No corrigió `data/mapa-ext-academico-2026-08-06.tsv`** por la discrepancia 250 vs 238 conglomerados, ni `data/curacion-registro/necesidad-objeto-modelo.tsv` por la regla `dinero.credito.*` que le falta. Las dos quedan declaradas, fuera de perímetro.
- **No adjudicó** que los reactivos de confianza del instrumento sean el mismo constructo que las θ homónimas del modelo.
- **No re-congeló** `tests/baseline.json`.
