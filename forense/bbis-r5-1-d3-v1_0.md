# R5.1-D3 · Ficha B-bis — el criterio firmado, congelado antes de abrir microdato

### `bbis-r5-1-d3` · **v1.0** · 19 de agosto de 2026 · **COMMIT A — ESPECIFICACIÓN CONGELADA**

> | | |
> |---|---|
> | **ARCHIVO** | `bbis-r5-1-d3-v1_0.md` |
> | **NOMBRE ESTABLE** | **`bbis-r5-1-d3`** — cítalo así, nunca por nombre de archivo |
> | **QUÉ ES** | La ficha B-bis del diseño `R5.1-D3`, escrita con la firma de mesa `D-1` de `ADR-110(a)` (`FP-54`). Congela estimando, universos, umbral, sensibilidades obligatorias, escala y reservas **antes** de que esta sesión abra ningún ZIP de ENIGH |
> | **QUÉ NO ES** | No es un veredicto del Hito D · no enmienda `r5-1-diseno-por-regla-preregistro` ni `hitoD-preregistro` · no reabre `D-1` · no adjudica ningún DiD · no convierte los abstracts de `BENCHMARK-R51D3-hogares-mixtos` en evidencia de primera mano |
> | **VERIFICAS ASÍ** | §5 enumera **todas** las cantidades que COMMIT B tiene permitido reportar, fijadas antes de calcular ninguna · §6 no inventa ningún umbral: hereda verbatim la escala sellada `A → E → B → C → D` · §10 declara, con la cita, por qué este acto **no puede** mover `13 de 27` |
> | **ESTADO** | **CONGELADO.** COMMIT B no edita este archivo. Si la especificación estaba mal, lo dice un commit posterior — nunca se corrige hacia atrás |

---

## 0 · Contaminación de esta sesión — declarada antes que nada

**Lo que esta sesión ya vio antes de escribir esta ficha:** los diez commits de la cadena `E4c` sobre `R5.1-D2`, **incluidos sus resultados** (Commit 8 §2: transferencia +2.32pp, corresidencia −0.81pp; Commit 9 §4: razón monto/`gasto_mon` 29.0%; Commit 10: su IC95%), el pre-registro sellado, el benchmark de hogares mixtos y la firma `D-1`. El encargo lo exigía: la ficha se escribe *con el criterio firmado*, y el criterio firmado se lee en esos documentos.

**Lo que esta sesión NO había abierto al congelar esta ficha:** ningún ZIP de `data/raw`, ningún `conjunto_de_datos.csv`, ningún diccionario, ningún catálogo de claves de ENIGH — verificable en el árbol: hasta el commit que sella este archivo, ningún comando de este acto referencia `data/raw`.

**Por qué la distinción importa y no se disuelve.** `ADR-46` define la unidad de contaminación como la sesión, y lo que contamina es haber visto **el mismo dato** que el protocolo va a usar. Esta sesión no lo ha visto. Pero sí sabe el resultado de `R5.1-D2` sobre estos dos desenlaces, con la misma encuesta y las mismas olas — es la contaminación de §0 del pre-registro sellado, un grado más fuerte (aquí el diseño es un pariente cercano de aquel, no un diseño ajeno). **Consecuencia operativa, escrita antes de correr:** si algún renglón de §5 o §6 pareciera calibrado para que salga la fila que ya se vio, ése es el sesgo a vigilar. Por eso §5 enumera **todas** las cantidades reportables antes de calcular ninguna: sin lista cerrada, la selección posterior de qué reportar es donde ese sesgo entraría sin dejar huella.

**Mérito reclamado, más estrecho que el de un pre-registro sobre dato nunca visto** — se dice así en vez de disimularlo.

---

## 1 · Identidad del acto y de la fila — qué renglón mueve esto, y cuál no

`R5.1-D3` es el tercer diseño sobre la misma pregunta sustantiva de `R5.1` (*¿la familia opera como seguro sustituto del Estado?*), y el segundo de la familia "por regla de elegibilidad":

| diseño | identificación | estado |
|---|---|---|
| `R5.1` (ficha original) | transversal por **recepción declarada** de `P044`/`P104` | veredicto `A` archivado 4/ago/2026, `ADR-58(c)` — historia con su estampa de universo |
| `R5.1-D2` | DiD por **regla de elegibilidad** (`P032` vs. umbral), ENIGH 2018→2022, regla de hogar *any-member* | `EJERCIDA_INDECISA` (fila B), firmado por `ADJ-4`, 13/ago/2026 |
| **`R5.1-D3`** (este) | **mismo DiD por regla, con el criterio `D-1` firmado**: umbral deflactado + hogares mixtos excluidos del desenlace de corresidencia, universo ACOTADO | esta ficha lo sella; COMMIT B lo corre |

**Fila de registro:** `R5.1-D3` abre **renglón propio** en `forense/registro-llaves-identificacion-v1_0.md`, por la misma regla con que `ADR-67(c)` le dio renglón propio a `R5.1-D2` — *"una fila por diseño escala; una fila por pregunta obliga a sobrescribir para siempre"*. Esta ficha añade esa fila naciendo `SELLADA_NO_EJERCIDA`. **COMMIT B no toca las columnas `estado`/`veredicto`** — mesa adjudica en acto propio, misma disciplina que `E4c` Commit 8 respetó y que `ADJ-4` cerró.

---

## 2 · Qué cambia respecto de `R5.1-D2`, con la razón, antes de tocar dato

**(1) Por qué el falsador anterior no discriminó — medido, no supuesto.** `R5.1-D2` no quedó indeciso por el DiD: los dos desenlaces cumplían la primera condición de la fila A con holgura (transferencia +2.32pp y corresidencia −0.81pp, ambos con el IC95% completo muy por debajo de 10pp en valor absoluto). Quedó indeciso por la **segunda** condición conjuntiva de la fila A: *"monto documentado como suficiente"*. La razón monto/`gasto_mon` per cápita dio **29.05%**, IC95% (26.16%, 31.94%) — entera bajo el piso de 33% (Commit 9 §4/§7, Commit 10 §3-4). La compuerta que cerró es de **atribución**, no de tamaño de efecto.

**(2) Qué cambia en el instrumento — y qué NO cambia, dicho con la misma claridad.**

| Cambia | No cambia |
|---|---|
| **Regla de hogar** para el desenlace de corresidencia: de *any-member* (D2, Commit 4 §2) a **exclusión de mixtos con universo ACOTADO** (firma `D-1b`) | Definición de tratamiento por persona (`P032` > umbral), §2.1-2.2 del Commit 1 de `E4c` |
| **Umbral 2022**: deflactado a pesos constantes de 2018 como **especificación primaria** declarada, no como sensibilidad (firma `D-1a`) | Olas (2018 pre, 2022 post), §4 del pre-registro sellado |
| **Universo del marginal**: recalculado sobre el universo ACOTADO (A-bis r4), no heredado del universo completo | Los dos desenlaces (`clase_hog ∈ {3,4}`; `P040`), §5 del pre-registro sellado |
| **Sensibilidades obligatorias** pre-declaradas en esta ficha, no opcionales (firma `D-1b`) | Estimador (`tests/svystat.py`, sin modificar), y la fuente de diseño (`concentradohogar`) |
| **Monto/gasto recalculado sobre el universo primario de D3** — exigencia de A-bis r4, no un criterio nuevo | El **umbral** de la escala (10pp / 20pp) y el piso de monto — heredados, no re-derivados |

**Declaración honesta, escrita antes de correr:** ninguno de esos cambios ataca de frente la compuerta que dejó indeciso a `R5.1-D2`. El criterio firmado `D-1` gobierna **cómo se clasifica el hogar** y **con qué vara se compara el ingreso entre olas** — no cambia quién está en el grupo de tratamiento a nivel persona, que es la población sobre la que se mide el monto. Es previsible, y se dice ahora y no después, que la razón monto/gasto vuelva a caer bajo el piso y que la fila resultante vuelva a ser `B`. **Si eso ocurre, es un resultado del acto, no un fracaso del acto** — y la lección que deja escrita para mesa es que la firma `D-1`, siendo correcta en lo que resuelve, no era la firma que destrabara `R5.1`. Lo único que puede mover esa compuerta dentro de este acto es que el **universo ACOTADO** cambie la población de hogares tratados lo suficiente como para mover la razón; se mide (§5.6), no se supone.

**(3) La escala completa, con su fila de no-refutación y su precedencia declarada al sellar:** §6. `R5.1-D3` **no inventa umbrales**: hereda verbatim la escala `A → E → B → C → D` del pre-registro sellado (§6 + §9, `ADR-71(b)`). El hueco que `R5.1-D2` tuvo al nacer —una escala sin fila para el desenlace de no-refutación— ya está cerrado desde el 12/ago; esta ficha no lo reabre ni lo re-descubre.

---

## 3 · Estimando y universos — los tres, declarados por separado (A-bis regla 4)

**Clasificación por persona, idéntica a `R5.1-D2` (Commit 1 §2.1-2.3, citada, no re-derivada):** sobre personas con `poblacion.edad ≥ 65` que tengan **≥1 fila en `ingresos`** (cualquier clave), se suma `ingresos.ing_tri` sobre `clave = P032` ("Jubilaciones y/o pensiones originadas dentro del país"):

- **T** ("nuevo elegible por regla"): suma `P032` **> umbral de la ola**.
- **C** ("elegible en ambos regímenes"): suma `P032` **≤ umbral, o nulo**.
- Fuera de universo: 65+ **sin ninguna fila** en `ingresos` — se cuenta, no se imputa.

### 3.1 · `U1` — universo PRIMARIO del desenlace de corresidencia (ACOTADO)

> **Hogares con ≥1 persona 65+ clasificada y SIN mezcla T/C.** Hogar **T** si **todas** sus personas 65+ clasificadas son T. Hogar **C** si **todas** son C. **Excluido del universo** si tiene al menos una T y al menos una C.

**Estimando reescrito, verbatim como la firma lo exige:** *"corresidencia intergeneracional en **hogares 65+ sin mezcla T/C**"* — no "en hogares 65+". El rótulo viaja pegado a toda cantidad que salga de `U1`.

### 3.2 · `U2` — universo de la SENSIBILIDAD (ii), completo, regla *any-member*

> **Todos** los hogares con ≥1 persona 65+ clasificada. Hogar **T** si tiene **≥1 persona 65+ en T**. Hogar **C** si tiene ≥1 persona C y **ninguna** T.

Es exactamente la regla que `R5.1-D2` usó como primaria (Commit 4 §2), y el precedente Duflo/Case-Deaton que `BENCHMARK-R51D3-hogares-mixtos` §1·H2 documenta (*"living with an eligible…"*). Aquí es **sensibilidad obligatoria**, no alternativa opcional.

### 3.3 · `U3` — universo del desenlace de transferencia, **intocado**

> Personas de 65+ con ≥1 fila en `ingresos`, clasificadas T o C por `P032`. Desenlace: `ingresos.clave = P040` ("Donativos en dinero provenientes de otros hogares") con `ing_tri > 0`.

`P040` es persona-nivel y coherente **sin regla de hogar** — lo declara el propio Commit 3 §2.2 y lo repite la firma `D-1b`. Ninguna de las dos reglas de hogar toca este desenlace: se corre una sola vez por umbral, no dos.

**Los tres universos no se comparan entre sí sin decirlo.** Una cantidad de `U1` y una de `U2` estiman sobre poblaciones distintas: reconciliarlas no valida ni invalida nada (A-bis regla 4). COMMIT B reporta cada una con su universo pegado, y la diferencia entre ellas se lee como **efecto de la regla de hogar**, nunca como verificación cruzada.

---

## 4 · Umbral — primario deflactado, sensibilidad nominal

**Primario (firma `D-1a`, verbatim: "Deflactado (45)"):**

| ola | umbral sobre `ing_tri` (trimestral) | razón |
|---|---|---|
| 2018 | **$3,276.00** (nominal, = $1,092/mes × 3) | la ola 2018 **es su propia base**: el umbral de $1,092 regía, nominal, cuando ENIGH 2018 se levantó (ago-nov 2018). No hay nada que deflactar (Commit 4 §1) |
| 2022 | **$4,034.74** (= $1,344.91/mes × 3) | deflactor INPC nov-2018=102.303 → nov-2022=125.997, razón **1.231606**, **23.16%** acumulado. Fuente primaria DOF verificada en Commit 4 §1 (códigos 5546133 y 5676669) |

**Sensibilidad (i), obligatoria:** umbral **nominal en ambas olas** ($3,276.00/trim), la vía que la firma dejó *"como sensibilidad declarada, no como duda"*. Costo de reclasificación ya medido por Commit 3 §1.3 y a re-derivar aquí: **45** personas de 28,626 clasificables en 2022 (0.157%), todas en dirección T→C.

**Reserva del diseño primario, heredada de Commit 4 §1 y no borrada:** el umbral que se deflacta fue, en su origen, un monto que el propio Estado dejó erosionar en términos reales durante los cinco ejercicios en que existió (**0** indexaciones reales encontradas, tres cortes DOF verbatim, Commit 3 §1.1). Deflactarlo corrige la comparación **entre olas**; no reconstruye una intención de política que nunca existió.

---

## 5 · Las cantidades reportables — lista cerrada, fijada antes de calcular ninguna

COMMIT B reporta **estas y solo estas**. Cualquier cantidad adicional que aparezca ahí se rotula explícitamente como **exploratoria** y no entra a ninguna fila de escala.

**5.1 · Conteos de hogares mixtos.** Por ola (2018, 2022) y por umbral (deflactado, nominal): hogares con ≥1 persona 65+ clasificada · con exactamente 1 · con ≥2 · de esos, **mixtos** (T y C simultáneos) y su **% sobre los de ≥2**. *(Re-derivación de las cifras que el encargo cita como antecedente y no como fuente: 1,312 / 31.4% en 2018 y 2,201 / 36.1% en 2022, ambas del Commit 3 §2.2 bajo umbral nominal; y 1,312 / 2,194 del Commit 4 §2 bajo el umbral ya decidido. Si difieren, manda lo que produzca este procedimiento.)*

**5.2 · Tamaños de universo.** `U1`, `U2`, `U3` por ola: hogares/personas totales, en T, en C, y excluidos con su razón (sin fila en `ingresos`; sin persona 65+ clasificada; mixto).

**5.3 · Corresidencia — cuatro corridas.** `{U1, U2} × {deflactado, nominal}`. Por corrida: `p_T`, `p_C`, `d_pre`, `d_post`, **DiD (θ̂)**, `SE`, `IC95%`, `n_estratos_singleton_pre/post`. Desenlace `clase_hog ∈ {3 Ampliado, 4 Compuesto}`. **La corrida `U1` × deflactado es la primaria; las otras tres son sensibilidades.**

**5.4 · Marginal recalculado (A-bis regla 4) — tres universos, rotulados.** Proporción ponderada de `clase_hog ∈ {3,4}`, sin partir por grupo, sobre: (a) `U1`, (b) `U2`, (c) el universo completo de hogares de la ola. Los tres por ola. **Se reportan juntos y con su universo pegado — no se resta uno de otro.**

**5.5 · Transferencia (`P040`, `U3`) — dos corridas** (deflactado, nominal): mismas columnas que 5.3. Intocado por la regla de hogar.

**5.6 · Monto — la compuerta, recalculada sobre el universo primario.** Razón **monto `P104` / `gasto_mon` per cápita**, trimestral/trimestral, media ponderada por `concentradohogar.factor`, ola 2022, pesos corrientes sin deflactar (misma metodología sellada que Commit 9 §4 — no una medida nueva), sobre **dos poblaciones declaradas**:

- **(a) población de `R5.1-D2`**: personas T (deflactado) con `P104 > 0` — reproducción de control del 29.0% ya publicado.
- **(b) población primaria de `R5.1-D3`**: hogares T de `U1` con `P104 > 0` — la que A-bis r4 exige, porque el estimando primario vive en `U1`.

Se reportan además: % de T con recepción efectiva de `P104`, monto medio, `gasto_mon` per cápita medio, y la **mediana** como cifra secundaria declarada (nunca promovida a principal por caer más cerca del piso). **Piso heredado, no re-derivado: 33%** (rango "no trivial" 33%-47% del 4/ago, citado por Commit 9 §7).

**5.7 · Chequeos de consistencia obligatorios.** (a) `n_estratos_singleton` = 0 en las seis corridas — si alguno cambia, se reporta y se explica antes de leer el resultado. (b) Reproducción exacta del universo de `R5.1-D2` (20,751 / 28,626 clasificables; T 6,160 / 8,877) — si no reproduce, **se para y se reporta**, no se sigue. (c) Ancho de `folioviv` derivado de la primera fila de `concentradohogar` de cada ola (mecanismo de ACTO J), no `zfill(10)` fijo.

**5.8 · Mecanismo de toda búsqueda sobre microdato o codebook.** El `grep` de esta caja es `ugrep -I`, que descarta archivos con un byte no-UTF8 **sin error ni código de salida útil**. Toda búsqueda de este acto sobre microdato o diccionario se hace con `command grep` (o `ugrep --binary-files=text`), y **el mecanismo se declara en cualquier `NO-ENCONTRADO`** que COMMIT B escriba. Un negativo sin mecanismo declarado no es un negativo.

---

## 6 · Escala de falsación — heredada verbatim, con su precedencia y su fila de no-refutación

**No se inventa ninguna fila ni ningún umbral.** Se hereda `forense/r5-1-diseno-por-regla-preregistro-v1_0.md` §6 (sellada 4/ago/2026) tal como quedó tras la enmienda `ADR-71(b)` de §9 (12/ago/2026):

- **A** — DiD <10pp (o de signo contrario al predicho por sustitución) en al menos uno de los dos desenlaces, **y** monto documentado como suficiente, **y** identificación de §2 exitosa. *La regla se refuta a este nivel de identificación.*
- **E** — DiD >20pp decisivo (IC95% que despeja el umbral por completo) en al menos uno de los dos desenlaces, **y** monto suficiente, **y** identificación exitosa. *Corroboración acotada.* **Ésta es la fila de no-refutación que B-bis exige, y ya existe: no nace con este acto.**
- **B** — DiD entre 10 y 20pp, **o monto insuficiente**, o las dos medidas dan direcciones opuestas sin significancia clara. *Ambiguo — no refuta ni confirma.*
- **C** — la reserva dominante resulta ser específicamente la ausencia de **panel de persona**.
- **D** — identificación de `P032` fallida, o alguna celda bajo el 5% del universo relevante (umbral **ARBITRARIO**, declarado en el sello original).

**Precedencia, declarada al sellar (Bloque B-bis) y no después: `A → E → B → C → D`.** La cláusula de **"monto insuficiente" de B gana sobre A y sobre E sin excepción por magnitud del DiD** — un monto insuficiente es objeción de *atribución*, no de *tamaño*.

**Mapeo al vocabulario de `registro-llaves-identificacion` §2** (Commit 6 §2 de `E4c`, reconciliado, citado): fila A → `EJERCIDA_REFUTA` · fila E → `EJERCIDA_ACOTA` · fila B → `EJERCIDA_INDECISA` · filas C/D → `NO_EJECUTABLE` o archivo por diseño.

**Qué gobierna si la corrida primaria y una sensibilidad caen en filas distintas — declarado ahora, no después:** **adjudica la corrida primaria (`U1` × deflactado).** Las sensibilidades no votan: si discrepan, la discrepancia **se reporta como reserva escrita en la fila propuesta**, con su magnitud, y mesa decide qué hacer con ella. Una sensibilidad que cambia la fila es un hallazgo de robustez, no un empate a resolver por mayoría.

**Y por encima de toda la escala, la contraparte de A-bis:** *un punto estimado que satisface un umbral con un intervalo de confianza que no lo despeja no adjudica* — se reporta como propuesta con la reserva escrita.

---

## 7 · Reservas de identificación — A-bis, escritas antes de correr

**Llave invocada, de las tres de `ADR-57(c)`: la (ii)** — *"experimento natural con grupo de comparación sobre encuestas repetidas"*. No la (i): ENIGH es **transversal repetida**, no panel; 2018 y 2022 son muestras independientes.

**Supuesto que la sostiene, escrito:** **tendencias paralelas** entre T y C en ausencia de la reforma de 2019. **No verificado con placebo en este acto** — el placebo 2014→2018 que Commit 4 §4.3 declaró factible sigue sin correr; es reserva, no ejecución.

**A-bis regla 1** — un β̂ sin argumento de identificación es asociación. Aquí el argumento es la llave (ii) más el supuesto de arriba; con eso, y solo con eso, el DiD se rotula como estimación de efecto bajo diseño cuasi-experimental — no como coeficiente identificado del generador.

**A-bis regla 2** — no se estratifica por ningún eje en esta corrida. Los dos ejes declarados en Commit 1 §2.7 (ámbito urbano/rural, sexo) **no se ejecutan**. Si un acto futuro estratifica y discrepa, eso establece que el marginal no es robusto a ese eje — **nada más**; no que el estratificado sea "el verdadero".

**A-bis regla 3** — los DiD son diferencias de **proporciones** (pp). La razón monto/gasto es un **cociente adimensional** con su piso propio. **No se comparan entre sí bajo ningún concepto**: son compuertas independientes, ambas deben sostenerse por separado para la fila A o la E.

**A-bis regla 4** — es el eje de este acto: el estimando primario está **acotado a `U1`**, el rótulo viaja pegado, y el marginal se recalcula sobre ese mismo universo (§5.4). Ninguna cantidad de `U1` se reconcilia contra una de `U2` ni contra el universo completo.

---

## 8 · Lo que va al acta con esa dirección — la advertencia Hamoudi-Thomas, no omitida

Firma `D-1b`, verbatim: *"Al acta va la advertencia Hamoudi-Thomas 2014: la exclusión condiciona en composición endógena y sesga hacia cero, por eso la sensibilidad no es opcional."*

**El mecanismo, escrito completo y con su dirección:** Hamoudi & Thomas (2014, *JDE* 109:30-37) muestran, sobre la pensión sudafricana, que los beneficiarios corresiden más con adultos de menor capital humano medido por **estatura y educación — rasgos fijos en adultos**, que por tanto no pueden ser efecto del ingreso. La conclusión es que **la composición del hogar es endógena a la elegibilidad**: quién termina viviendo con quién es, en parte, un desenlace del propio tratamiento.

**Traducido a `U1`:** *ser hogar mixto* no es una característica exógena que se pueda podar sin costo. Si el programa **causa** hogares mixtos (una persona recién elegible se muda con otra que ya lo era), excluirlos **borra precisamente los eventos de corresidencia inducidos por el tratamiento**. La dirección del sesgo es **hacia cero** — es decir, **conservador para el desenlace `EJERCIDA`**: el diseño primario tiende a **subestimar** cualquier sustitución real, no a inventarla.

**Por eso la sensibilidad (ii) no es opcional, y por eso su papel está fijado antes del dato:** `U2` (universo completo, *any-member*) es el contrafactual que muestra cuánto de la señal se fue con la poda. Si `U1` y `U2` coinciden, la poda no costó señal; si difieren, la diferencia **es** la magnitud del condicionamiento endógeno, y se reporta como tal — no como "dos estimaciones y elegimos una".

Es, además, exactamente la advertencia que **A-bis regla 2** (colisionador / selección inducida por condicionar) ya hacía sin cita externa; el benchmark le pone una.

---

## 9 · Descartadas por firma, con su razón — no son dudas abiertas

- **Asignación del hogar por `P032`-máx** (*"el hogar es T si su persona 65+ de mayor pensión contributiva lo es"*): **descartada**. Dos razones firmadas: (i) **sin precedente** — el barrido de `BENCHMARK-R51D3-hogares-mixtos` §1·H2 no encontró un solo estudio que asigne el hogar por el adulto mayor de mayor pensión; (ii) **signo perverso** — un hogar con un 65+ de pensión alta y otro elegible quedaría clasificado en **C** aunque la transferencia del programa **entra a ese hogar**. Su versión con precedente (*any-member*) es la que entra como sensibilidad (ii), no ésta.
- **Doble conteo (el hogar entra en T y en C a la vez)**: **descartada**. Rompe la exclusividad mutua que Commit 1 §2.2 declaró como propiedad del diseño, no es neutral para la varianza, y **cero** de los cinco barridos del benchmark encontró un solo precedente que lo haga (§1·H4).

Ninguna de las dos se reabre en COMMIT B. Aparecen aquí para que el registro muestre **qué se descartó y por qué**, no solo qué se adoptó.

---

## 10 · Lo que este acto NO puede mover — el contador, con la cita que lo impide

El encargo (`forense/encargos/2026-08-19-FICHA-R51-D3.md` §3) declara que este acto es *"la vía al **14 de 27** del bloque append-only de `hitoD-preregistro`"*, y `ADR-110(a)` propaga la misma frase. **Verificado contra el canon sellado antes de correr nada: esa premisa no se sostiene.** Se declara aquí, en COMMIT A, para que no se lea como una excusa construida después de ver un resultado.

**Razón 1 — la firma de mesa que lo prohíbe.** `ADR-67(c)` (`canon/gobernanza-v1_15.md:868`), verbatim:

> *"Un veredicto del diseño por regla de elegibilidad NO cuenta como veredicto de `R5.1` ni lo reemplaza ni coexiste en su fila: abre renglón propio. Regla de contadores, explícita para que T18 no herede ambigüedad: el denominador **27 no se toca** (cuenta fichas del pre-registro original…); la métrica del renglón nuevo es **llaves de identificación ejercidas** (hoy 0), que `R5.1-D2` movería a 1 si corre conforme a su pre-registro sellado."*

`R5.1-D3` es de esa misma familia — diseño por regla de elegibilidad, renglón propio (§1). La regla de contadores de `ADR-67(c)` lo alcanza igual.

**Razón 2 — la mecánica del test, independiente de la firma.** `T18`/`T20` derivan el contador de un `set` de identificadores de regla extraídos del bloque append-only con el patrón `` `RX.Y` → veredicto `Z` `` (`tests/check.py`, `_VEREDICTO_CANONICO`). `R5.1` **ya está en ese conjunto** desde el 4/ago/2026 (veredicto `A`, `ADR-58(c)`). Una línea nueva para `R5.1` no incrementaría el conteo — el `set` ya lo contiene. Y una línea escrita como `` `R5.1-D3` → veredicto `X` `` **no coincide con el patrón** (exige backtick de cierre inmediatamente tras los dígitos), así que no la contaría ni la señalaría como sospechosa: entraría **invisible** al registro. Las dos vías fallan, por razones distintas.

**Dónde sí se anota, entonces:** `forense/registro-llaves-identificacion-v1_0.md`, población de conteo **`llaves de identificación ejercidas`**, hoy `1 de 2`. Esta ficha añade la fila `R5.1-D3` como `SELLADA_NO_EJERCIDA` — el denominador pasa a `3` y el contador queda **`1 de 3`** hasta que mesa firme. Si mesa firmara un `EJERCIDA_*` para `R5.1-D3`, iría a `2 de 3`.

**Lo que este acto hace con la contradicción:** la registra (`FP-68`) y la reporta. **No** la adjudica — decidir si `ADR-110(a)` corrige a `ADR-67(c)` o si `ADR-110(a)` traía una premisa vencida es firma de mesa, y auto-adjudicarla desde aquí sería exactamente lo que la convención repetida de esta cadena prohíbe (*"mesa adjudica en acto propio; este commit no firma"*).

---

## 11 · Perímetro — lo que esta ficha no autoriza

No adjudica el DiD · no toca umbrales fuera de los ya sellados · no reabre `D-1` · no convierte los abstracts de `BENCHMARK-R51D3-hogares-mixtos` (clase segunda-mano `SIN-FETCH`) en evidencia de primera mano · no corre el placebo 2014→2018 · no estratifica por los ejes de Commit 1 §2.7 · no modifica `tests/svystat.py` · no escribe en el bloque append-only de `hitoD-preregistro` · no escribe en las columnas `estado`/`veredicto` de `registro-llaves-identificacion`.

---

## 12 · Cierre — la frase que congela

> **El primer resultado que produzca este procedimiento, sobre los universos de §3, con el umbral de §4, las cantidades de §5 y la escala de §6, es el que se reporta en COMMIT B.**

---

*COMMIT A del `ACTO FICHA-R51-D3`. Escrito y sellado **antes** de que esta sesión abriera ningún ZIP de `data/raw` — §0 declara la contaminación que sí tiene. No se edita jamás: si la especificación estaba mal, lo dice un commit posterior.*
