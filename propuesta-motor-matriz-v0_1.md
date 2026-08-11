# El motor como matriz: la ponderación como especificación y la demanda de datos como derivación
### Propuesta sin sello · v0.1 · 10/ago/2026

> | | |
> |---|---|
> | **CLASE** | Propuesta. **No es decisión.** No rige hasta que exista un ADR en `gobernanza`. No edita ningún archivo existente: su perímetro es este documento |
> | **ORIGEN** | Sesión del 10/ago/2026 (continuación de la maestra 24). Encargo del autor, citado: *"el motor define qué se pondera y cómo se pondera, eso nos dice qué se va a calcular, saber qué y cómo se va a calcular nos dice qué información necesitamos, y de esa forma mantenemos consistencia"* |
> | **PROCEDENCIA** | Las cifras del programa son tipo (1): derivadas o citadas archivo:línea contra clon fresco de `origin/main = 76710a0` (10/ago/2026, delta de solo 1 línea de hallazgos respecto de `1e4b9848`). La literatura metodológica proviene de los tres dictámenes compass del **espejo del proyecto** — tipo (2) sin sello de commit, se leen como (3); sus citas externas (Gourieroux/Monfort/Renault 1993; Grazzini/Richiardi 2015; Dridi/Guay/Renault 2007; Manski; Ferson; Iskandar 2021) son verificables por sí mismas. El argumento es tipo (3) |
> | **QUÉ DECIDE** | Si el ejecutable del programa se especifica como **cómputo matricial sobre la distribución de atributos** (esperanza directa, calibrada por momentos), con un **catálogo de momentos pre-declarado como fuente única de demanda de datos** — o si MILPA sigue especificado como ABM por agentes con la demanda de datos curada a mano |
> | **QUÉ NO DECIDE** | La función externa del motor (contexto vs. sustituto — `gobernanza:463` ya la consideró y no la adoptó como entregable primario); la granularidad de celdas; el tratamiento final de G1b; ningún valor de ningún parámetro |

---

## 0 · La tesis, en una cadena de cuatro eslabones

El encargo formula la cadena; este documento la formaliza y le añade las dos correcciones que la hacen compatible con el canon:

**motor → ponderación → cálculo → demanda.**

1. **El motor define la ponderación.** Pero "ponderar" son *dos objetos distintos* que la propuesta separa desde el título de §2: **π** (quién pesa cuánto en la población) y **W** (qué momento pesa cuánto en la calibración). Confundirlos es el error de categoría que A-bis regla 3 prohíbe entre escalas.
2. **La ponderación define qué se calcula.** Toda salida del motor es una forma π-ponderada sobre celdas de atributos (§1.6). El conjunto de salidas calculables es finito, enumerable y se escribe: es el **catálogo de momentos** (§3.1).
3. **Qué se calcula define qué se necesita.** Cada entrada del catálogo demanda datos de una de **tres clases** (§3.2): distribuciones de parámetros Θ, momentos de desenlace m, o co-observaciones conjuntas (llaves). Las tres clases ya existen dispersas en el programa; el catálogo las unifica bajo una sola fuente de demanda.
4. **La consistencia es la derivación, no la disciplina.** La demanda deja de escribirse a mano (como las necesidades N1–N33 del curador) y pasa a derivarse de la especificación — el mismo movimiento que la v2.1 hizo con las cifras: derivar en vez de teclear.

**Ancla canónica — esto no inventa un requisito, construye un artefacto que un ADR ya exige.** `gobernanza` (bloque ADR-50/51, inciso (3), `canon/gobernanza-v1_15.md:461`): *"Los momentos a reproducir SE DECLARAN ANTES DE AJUSTAR. […] Esto NO crea el pre-registro aquí: establece que hará falta antes de que exista una sola corrida `AJUSTADO`."* El catálogo de §3.1 es ese pre-registro.

---

## 1 · Los objetos — todos existen ya a medias en el repo

### 1.1 `x` y las celdas: el vector de atributos

`modelo` v4.0 §1.1.A (`canon/modelo-decision-v4_0.md:110-137`) define los **seis ejes** con variable ENIGH exacta, módulo y llave, verificados por P1 contra el paquete en disco: **formalidad laboral** (`segsoc` + `contrato`/`pres_8`, nivel persona), **edad** (persona), **urbanización** (`tam_loc`, nivel hogar), **ingreso** (`ing_cor`/`est_socio`, hogar), **acceso digital** (`celular`/`conex_inte`, hogar), **condición migratoria** (`residencia`, persona; `remesas` complementaria, hogar). Veredicto de P1: **CONJUNTA COMPLETA**.

Una **celda** es una región del producto de los seis ejes bajo una discretización **D** que esta propuesta deja como decisión de mesa (M2, §9), con dos restricciones heredadas que la discretización no puede violar:

- **Tres ejes son de hogar por diseño del instrumento** (urbanización, ingreso, acceso digital): no existe varianza intra-hogar; ninguna celda puede definirse por contraste intra-hogar en esos ejes (`modelo:110-137`, advertencia de P1 citada en el propio §1.1.A).
- **La discretización es una dicotomización generalizada** y hereda sus artefactos (dictamen compass `wf-8b198c56`, espejo): cortar un eje continuo en pocos tramos puede fabricar o borrar heterogeneidad. D se declara antes de calibrar, con análisis de sensibilidad a cortes alternativos, y donde el instrumento dé escala original, el momento se define en escala original (§4.5).

### 1.2 `π`: la ponderación poblacional

π es la distribución de la población sintética sobre las celdas: síntesis ENIGH + reponderación IPU de §1.1.C, con su restricción intacta y citada: *"el IPU reproduce marginales; no fabrica conjuntas que nadie midió"* (`modelo:173`). Consecuencia para el catálogo: **ningún momento demandado puede requerir una conjunta de atributos que ENIGH no observe** — la malla de pares (parámetro, desenlace) no se amplía por reponderar (§1.1.C, corolario de P2 §1.d).

π **se congela antes de la calibración** y no es grado de libertad del ajuste (§2).

### 1.3 `Θ(x)`: los parámetros como distribuciones condicionales

Los **nueve parámetros** que los generadores multiplican (`modelo:251`): `confianza_institucional` (vector de 6 componentes, ADR-28.b), `radio_confianza`, `sens_estatus`, `aversion_riesgo`, `horizonte_temporal`, `familismo_apoyo`, `familismo_obligacion`, `exposicion_violencia`, `deferencia`. Bajo v4.0 son **distribuciones condicionales sobre atributos**, no escalares por perfil.

Estado (dos poblaciones de conteo, no se mezclan): el contador de **condicionales medidas es 9 de 14** (`modelo:11`, con la lista MEDIDAS en `modelo:273`); las **producciones del barrido** (`data/curacion-registro/produccion-modelo.tsv`, 11 filas) añaden distribuciones nuevas de Θ para G5 — 2 de `familismo_apoyo` (ENBIARE `PB2_1`/`PB2_2`, `LISTA_PARA_USO_MODELO`), 8 de `radio_confianza` (frenadas por DH-ea9e932f70ce12) y 1 de `familismo_obligacion` (`NO_DETERMINADO`, CRES-7cb78abf). Nota B-bis que viaja con las de familismo: `procedencia.yaml:633-635` marca las escalas de familismo como validadas solo en diáspora (marca (b)); las distribuciones ENBIARE son el primer dato en población EN México para ese constructo — corroboración anticipada declarable, no fracaso.

### 1.4 `B`: la matriz de coeficientes generador × parámetro

Ya está escrita — como lista, no como matriz — en `milpa/procedencia.yaml:625-636`. Transcrita aquí con cita (los valores son los `ASIGNADO` vigentes; **no son mediciones** y esta tabla no los promueve):

| | conf_inst | radio_conf | sens_estatus | aversion | horizonte | fam_apoyo | fam_oblig | expo_viol | deferencia |
|---|---|---|---|---|---|---|---|---|---|
| **G1** (a/b) | **[financiera] −0.60** (ADR-52 B) | −0.35 | | | | | | | |
| **G2** | | | 0.55 | 0.20 | | | | | |
| **G3** | | | | 0.40 | −0.60 | 0.20 (ADR-30: pooling/tanda) | | | |
| **G4** | **[justicia] −0.40** (`modelo:398`) | | −0.15 | | −0.20 | | | 0.70 | |
| **G5** | | 0.15 | | | | 0.50 | **SIN MAGNITUD** (signo neg. o no monotónico) | | |
| **G6** | | | | | | | | | 0.45 |

**15 celdas no-cero sobre 9 columnas.** Precisiones que la matriz hace visibles: (a) la fila `G1` de procedencia agrupa lo que ADR-20 desdobló — el −0.60 está adjudicado a **G1a** con componente nombrado (ADR-52 B), y **G1b está en HIPÓTESIS con "coeficiente a revisión"** (`modelo:371`, ya contradicho por Casos 2-3); (b) `familismo_apoyo` aparece en dos filas **sin doble conteo** por mecanismos distintos (ADR-30, `procedencia.yaml:82-89`); (c) el check de compilación de ADR-30 (`procedencia.yaml:629-632`: una configuración donde `familismo_obligacion` alto mejore *todos* los desenlaces se rechaza) se vuelve, bajo la matriz, un test de una línea sobre signos de columna.

### 1.5 `C`: la capa de contexto

Los **42 disparadores de dominio + 7 globales** entran como booleanos de contexto, no como parámetros calibrables (adenda a ADR-26, `modelo:88` y `modelo:601`). En la matriz son conmutadores: seleccionan qué mapa de respuesta aplica en cada celda (formal/informal, quién observa, sanción creíble, puente personal…). Esta capa es la ventaja comparativa documentada del programa frente al muestreo sintético (fallos de Sarstedt et al. 2024 en regularidades profundas: los disparadores no son declarables en encuesta) y **no gana grados de libertad** con esta propuesta.

### 1.6 `R` y las salidas: formas π-ponderadas

Cada regla `r` de las 49 tiene un mapa de respuesta `h_r` que toma el índice del generador que la enruta, `g(x) = B·θ(x)`, y el estado de contexto `C(x)`, y devuelve una probabilidad de conducta en la celda. Toda salida agregada del motor es

**m = Σ_celdas π(x) · h_r( B·θ(x), C(x) )**,

una forma (por tramos) bilineal en (π, θ) dada B — auditable celda por celda, sin ruido Monte Carlo, y **exactamente igual en esperanza al ABM de agentes independientes**. La simulación por agentes queda como modo opcional para trayectorias y varianza, no como definición del motor.

**Honestidad sobre `h_r`, para que nadie la descubra después:** la forma de `h_r` es justo lo que `D-ABC` dejó pendiente y ADR-65 probó que no se lee de las curvas. Esta propuesta **no la resuelve por magia**: bajo la ruta agregada, `h_r` es una **elección de mecanismo declarada antes de ajustar** (p. ej. umbral lineal vs. logística), con sensibilidad reportada sobre una familia corta pre-declarada. Lo que la ruta agregada elimina es la necesidad de una *función de enlace por coeficiente para importar estimados externos* (dictamen compass `wf-7edaceda`, TL;DR: "decisivo") — no la necesidad de escribir el mecanismo.

### 1.7 `G1b`: la única excepción, declarada

La difusión radial es interacción entre agentes y no se reduce a formas independientes por celda. Tratamiento propuesto: **aproximación de campo medio** (la fracción adoptante de la celda entra como estado agregado en `h`), declarada como aproximación en la spec. Costo honesto: pierde la dinámica de red fina. Atenuante material: G1b ya está **CONTRADICHO → HIPÓTESIS** (`modelo:371`); construir el motor exacto alrededor de la pieza más débil del modelo sería optimizar lo refutado.

---

## 2 · Las dos ponderaciones — y por qué no se tocan entre sí

| | **π** (poblacional) | **W** (de calibración) |
|---|---|---|
| Responde | quién pesa cuánto en México | qué momento pesa cuánto en el criterio de ajuste |
| Vive en | la síntesis ENIGH+IPU (§1.1.C) | el criterio SMM: (m(β)−m_obs)ᵀ W (m(β)−m_obs) |
| Se fija | **antes** de calibrar; no es grado de libertad | por elección declarada (identidad → diagonal por varianza → dos etapas), con corrección sándwich bajo mala especificación (Dridi/Guay/Renault 2007, vía dictamen `wf-7edaceda`) |
| Falla como | sesgo de representación (quién falta en la síntesis) | eficiencia degradada o momentos dominantes arbitrarios |

Regla de la propuesta: **ninguna cifra cruza de una columna a la otra**, y ningún documento del programa dice "la ponderación" sin apellido. Es la misma clase de disciplina que A-bis regla 3 impone entre escalas.

---

## 3 · La cadena de demanda — la aportación central del encargo

### 3.1 El catálogo de momentos `M`

Artefacto nuevo, pre-registrado, append-only. Cada entrada:

```
id_momento · definición · ESCALA declarada · UNIVERSO declarado ·
nivel (persona/hogar) · instrumento(s) candidato(s) ·
rol (AJUSTE | HOLDOUT | DIAGNÓSTICO) · estatus de disponibilidad
```

Tres obligaciones heredadas, con dueño: escala y universo por A-bis reglas 3-4; computabilidad **por celda** o el momento no cuenta para identificar (inciso (5) del bloque AJUSTE, `gobernanza:465`); declaración **antes** de ajustar (inciso (3), `gobernanza:461`). El rol AJUSTE/HOLDOUT se asigna al sellar, no al ver resultados (§6).

### 3.2 El libro de demanda: tres clases, un solo registro

Cada entrada de `M` y cada celda de Θ que el motor consume genera una **demanda con ID**. La demanda es de tres clases — y las tres ya existen en el programa como corrientes separadas; el libro las unifica:

| Clase | Qué pide | Corriente existente que absorbe |
|---|---|---|
| **Θ-lado** | distribución condicional de un parámetro sobre celdas | las 14 condicionales (9 medidas), las producciones del barrido, CAL-CONF |
| **m-lado** | un agregado de desenlace observado, en su escala y universo | los medidos del Hito D y los estimandos propios (ENCIG, ENIF, ENVIPE, ENIGH) |
| **conjunta** | reactivo de θ y desenlace co-observados en el mismo instrumento (C1–C4, `modelo:153`) | las **llaves de identificación** de ADR-57(c) — hoy 0 ejercidas |

La demanda insatisfecha **se clasifica con el vocabulario de A.4** (`instrucciones-proyecto-v2_6.md:238`): `EXISTE-SATISFACE` / `EXISTE-NO-SATISFACE` (y qué le falta) / `NO-ENCONTRADO` (dónde y con qué términos) / `NO-ACCESIBLE`, más la marca del programa `MECANISMO-NO-CORRIDO` cuando nadie ha resuelto la fuente. **La demanda insatisfecha es entregable, no fracaso** — el Hito D ya lo demostró: 7 de sus 13 veredictos son `D` precisamente porque el estimando demandado no existe donde se buscó.

**Regla de gasto que esto habilita:** ningún acto de apertura de fuente corre sin citar el `id_momento` o la celda de Θ que lo demanda. Es el freno estructural a la expansión horizontal que el diagnóstico del 10/ago identifica como el riesgo de estancamiento.

### 3.3 Anti-circularidad: congelar antes de escanear

El riesgo simétrico de la cadena es que la "demanda" sea oferta disfrazada — escribir el catálogo mirando lo que ya hay en disco. Blindaje, con la maquinaria de Bloque D que ya existe: **commit 1** sella catálogo y roles (AJUSTE/HOLDOUT) *antes* de abrir el escaneo de disponibilidad; **commit 2** trae el libro de demanda con estatus; si el catálogo estaba mal, un **commit 3** lo dice y nunca se corrige hacia atrás. Mismo patrón de dos commits que los actos de estimación.

### 3.4 Relación con el curador N1–N33 (pregunta M5, no decisión)

Hoy las necesidades del curador se escriben a mano y el registro las cruza contra evidencia. Bajo esta propuesta, la lista de necesidades **se deriva del libro de demanda** — una sola fuente de verdad, el mismo principio por el que la cola del curador se deriva y produce exactamente sus 147 filas. No se implementa aquí; se pregunta a mesa si el curador adopta el libro como su fuente de necesidades o mantiene las dos listas con un cruce declarado.

---

## 4 · Calibración: el AJUSTE de ADR-50/51, operacionalizado

### 4.1 SMM / inferencia indirecta sobre la matriz

Se buscan los β (y las 7 libertades de probabilidad; **22 grados de libertad**, ADR-51) que minimizan la distancia ponderada por W entre momentos simulados y observados. Condiciones del dictamen `wf-7edaceda` que se adoptan como requisitos: número de momentos informativos ≥ número de parámetros libres; elección de momentos y de W declarada; errores estándar **no** por fórmula default (sándwich doble bajo mala especificación); y chequeo explícito de *sloppiness*/equifinalidad (sensibilidad del criterio por dirección del espacio de parámetros — direcciones planas se reportan como no identificadas, no se rellenan).

Sobre la matriz, m(β) es barato y casi lineal por tramos: el jacobiano ∂m/∂β se calcula por celda en forma cerrada para los tramos lineales, lo que vuelve viables el chequeo de identificación local y la optimización que en un ABM por agentes serían ruidosos y caros.

### 4.2 Los β entran como conjuntos, no como puntos

Adoptando el veredicto del dictamen `wf-d72e6a97`: los coeficientes se representan como **conjuntos identificados** (intervalos/p-boxes à la Manski/Ferson), se propagan por la matriz, y la salida es una **banda**, reportada como identified set — nunca como intervalo de confianza. El riesgo dominante documentado se pre-declara como desenlace posible e informativo (§6): **que la banda no firme el signo del output**. Con 15 intervalos simultáneos, ese resultado es probable en la primera corrida; decirlo antes es lo que impide leerlo como fracaso o, peor, estrecharlo con supuestos no declarados. Los supuestos que estrechan cotas (monotonicidad, exclusiones, restricciones de forma) se listan con su precio de credibilidad, uno por uno.

### 4.3 Qué clase de número produce esto — y qué sigue prohibido

Todo β calibrado así es **`AJUSTADO`** (la clase que ADR-49 selló), jamás `MEDIDO`. **El contador 0/15 no se mueve con esta propuesta** — cambia la clase de 15 `ASIGNADO` puntuales a `AJUSTADO` con banda y procedencia, que es mejor y sigue sin ser medición. ADR-57 queda íntegro en sus dos direcciones: ni el marginal se promueve, ni el condicionado (`gobernanza:619`, corolario simétrico). Y la **compuerta de identificación** de ADR-57(c) gobierna las salidas del motor igual que hoy: la matriz **reproduce, describe y segmenta** — con bandas y tiers; afirmaciones de intervención solo detrás de una llave ejercida, y hoy hay **cero**.

### 4.4 Compatibilidad con ADR-65, dicha con precisión

ADR-65 cerró la ruta de *leer* la forma funcional de las curvas para destrabar los β. Esta propuesta no la reabre: la ruta agregada no necesita enlace por coeficiente porque el enlace queda implícito en el mecanismo (dictamen `wf-7edaceda`, hallazgo sobre inferencia indirecta). Lo que sí exige — y §1.6 lo declara — es fijar el mecanismo `h_r` antes de ajustar, con sensibilidad sobre una familia corta. `D-ABC` sigue abierto como pregunta de forma; deja de ser bloqueante para calibrar.

### 4.5 Dicotomización, dos veces vigilada

El artefacto entra por dos puertas: la discretización D de los atributos (§1.1) y la definición de momentos sobre desenlaces recortados. Regla: donde el instrumento entregue la escala original, el momento se define en escala original y el corte, si hace falta para comunicar, es una vista derivada — no el estimando. El dictamen `wf-8b198c56` es la referencia de auditoría de ambas puertas.

---

## 5 · Catálogo semilla (candidatos v0 — valores deliberadamente NO transcritos)

Regla de este cuadro: **los valores se derivan del archivo dueño en el acto de calibración, nunca de esta propuesta** (v2.1: ninguna cifra esperada se teclea; este documento no es archivo dueño de ningún número). Se listan identidad, clase, escala y dueño.

| Candidato | Clase | Escala / universo (a declarar al derivar del dueño) | Dueño del valor | Estatus |
|---|---|---|---|---|
| Pago/experiencia en trámites (linaje R3.1/R3.2, ENCIG) | m-lado | proporción · universo ENCIG | `forense/hitoD-preregistro-v2_0.md` + notas de corrida | medido; reproducibilidad de ejecutable histórico en deuda (veredictos B) |
| Uso formal de servicios financieros (R1.2, ENIF) | m-lado | proporción · adultos ENIF | ficha R1.2 del preregistro | medido (E) |
| Penetración fintech segmento popular + brecha rural-urbana (R1.3) | m-lado | proporción y diferencia en pp | ADR-63 / ficha R1.3 | medido (E); condición 3 inconstruible, declarada |
| Apoyo familiar vs. Estado 65+ (R5.2, ENASEM/ENIGH) | m-lado | proporción con IC · universo del diseño | ficha R5.2 | medido (A **con reserva punto-vs-IC pendiente de mesa**) |
| Distribuciones `familismo_apoyo` (ENBIARE `PB2_1`/`PB2_2`) | Θ-lado | escala del reactivo · universo ENBIARE | `data/curacion-registro/produccion-modelo.tsv` (+ hash de microdato por fila) | `LISTA_PARA_USO_MODELO` |
| Distribuciones `radio_confianza` (ENBIARE, 8 filas) | Θ-lado | ídem | ídem | **frenadas por DH-ea9e** (equivalencia paramétrica) |
| Distribución `familismo_obligacion` (ENASIC `P7_12_7`) | Θ-lado | ídem | ídem | **DH-332 + CRES-7cb78abf** (especificación) |
| Condicionales de `confianza_institucional`, `radio_confianza`, `exposicion_violencia` (Fase B) | Θ-lado | por componente / por ítem, como `modelo:273` las declara | notas CAL-CONF / procedencia | medidas (parte del 9/14) |
| ENNViH/MxFLS · ENASEM+Bienestar | conjunta (llave) | — | ADR-57(c), lista corta | **0 ejercidas**; cada una exige pre-registro propio (R5.1 espera §8) |

El catálogo real se sella aparte (commit 1 de §3.3), con más filas m-lado de los estimandos propios sobre ENVIPE/ENCUCI/ENIGH; este cuadro solo demuestra que la semilla existe y de qué archivos se deriva.

---

## 6 · Pre-registro de falsación de la arquitectura (Bloque B-bis)

Declarado antes de que exista una sola corrida, para que ningún ejecutor tenga que inventar la fila:

- **Corrobora** la arquitectura: reproducir, dentro de banda, los momentos **HOLDOUT** (no usados en el ajuste), con roles asignados en el commit 1 de §3.3.
- **Acota**: bandas de salida que no firman signo. Resultado informativo pre-declarado — mide cuánta identificación falta, y alimenta la priorización del libro de demanda (qué momento nuevo estrecharía más). No se estrecha con supuestos no listados en §4.2.
- **Refuta**: fallo sistemático de signo en momentos HOLDOUT no atribuible a huecos declarados de Θ; o un chequeo de compilación tipo ADR-30 (§1.4.c) imposible de satisfacer sin violar signos sostenidos por el corpus.
- **Precedencia**: si una corrida satisface "acota" y "refuta" a la vez, manda la fila de refutación. Declarado aquí, al sellar, no después.

---

## 7 · Interacciones de gobernanza — declaradas, no resueltas aquí

1. **`milpa-spec` espera un gate.** El banner de ADR-62 (`milpa/milpa-spec-v0_2.md:4`) declara la spec como snapshot perfil-céntrico superado y condiciona su reescritura al *"veredicto del benchmark (milpa-plan, gate de Fase 1)"*. Esta propuesta es candidata natural a ser esa reescritura; si procede sin el gate, es decisión de mesa (M1), no default.
2. **"Motor como contexto": CONSIDERADA Y NO ADOPTADA como entregable primario** (`gobernanza:463`, que además registra que la propuesta escrita no existe en el repo — vive solo en el espejo, `propuesta-motor-como-contexto-2026-07-30.md`, y `gobernanza:463` es la referencia a citar si entra). Esta propuesta **se alinea con la razón de esa no-adopción**: su métrica primaria es reproducir agregados observados directamente — lo que gobernanza prefiere sobre el delta contra un modelo sin motor, contaminable por repo público. El benchmark-delta queda como métrica secundaria posible, compatible, no incluida aquí.
3. **ADR-57(b) apunta a `B(x)`.** La heterogeneidad de `familismo_apoyo` por celdas quedó registrada como *"el primer soporte empírico propio de la segmentación al nivel de coeficiente"* (`gobernanza:621`) — un escalar único por generador es menos segmentado que la filosofía del modelo. La matriz admite esa extensión con naturalidad (bloques de B por región de atributos). **No es el default de v0.1**: cada bloque multiplica grados de libertad en un ajuste ya subidentificado. Se declara como extensión condicionada a que el chequeo de identificación de §4.1 la soporte.
4. **Lo congelado sigue congelado:** `4 de 144` (MESA-M4) no se toca; los 42 disparadores no entran al conteo de calibrables (adenda ADR-26); `conf.06` cerrado (ADR-64) — el catálogo hereda la lección: identidad de reactivo y corte viajan con cada momento.

---

## 8 · Lo que esta propuesta no resuelve

- **No mueve 0/15** ni ningún contador. Cambia la clase alcanzable de los 15 (ASIGNADO puntual → AJUSTADO con banda) condicionada a que la calibración corra.
- **No fija D** (granularidad de celdas), **no fija la familia de `h_r`**, **no fija W**: los tres se sellan en el commit 1 del catálogo, con esta propuesta como marco.
- **No decide la función externa del motor** (ver §7.2).
- **No sustituye ninguna decisión de mesa pendiente**: DH-ea9e y DH-332/CRES gatean dos filas del propio catálogo semilla; el §8 de R5.1 gatea la única llave con pre-registro sellado.
- **No es canon.** Requiere ADR; sin él, es una hipótesis que gobernó una sesión.

## 9 · Preguntas para mesa

- **M1** · ¿Se adopta el cómputo matricial sobre la distribución de atributos como definición del ejecutable (la reescritura que el banner de ADR-62 espera), con el ABM por agentes como modo derivado — y procede antes del gate de Fase 1 de `milpa-plan`, o espera su veredicto?
- **M2** · Granularidad D: ¿cortes iniciales por eje (respetando los tres ejes de hogar), y quién los sella?
- **M3** · ¿Se acepta campo medio como tratamiento declarado de G1b mientras conserve estatus HIPÓTESIS?
- **M4** · ¿El catálogo de momentos se constituye como el pre-registro que `gobernanza:461` exige, con roles AJUSTE/HOLDOUT sellados en commit 1 (§3.3)?
- **M5** · ¿El curador deriva sus necesidades del libro de demanda (fuente única), o mantienen listas separadas con cruce declarado?
- **M6** · ¿Los tres dictámenes compass entran al repo (hoy son espejo sin sello) antes de sellar cualquier ADR que los cite?

## 10 · Módulo de auditoría (acotado por v2.3: este artefacto no afirma nada sobre México)

**1–6** · No aplican: propuesta sobre la arquitectura de un artefacto.

**7 · ¿Qué conclusión sería peligrosa simplificada?** Tres. *"La matriz reproduce los agregados, luego el modelo está validado"* — reproducir con 22 libertades no es identificar; AJUSTADO ≠ MEDIDO, y la compuerta de ADR-57(c) sigue cerrada para intervención. *"Más celdas = más fiel"* — cada celda y cada bloque de B(x) compra varianza y subidentificación; la fidelidad sin identificación es la infalsabilidad que el Bloque A persigue. *"Las bandas anchas se estrechan con supuestos razonables"* — solo con los supuestos listados y precio declarado (§4.2).

**8 · ¿Qué afirmación sobre el estado del corpus fue derivada y cuál no?** Derivadas o citadas archivo:línea contra `76710a0`: 13/27 y 0/15 (`README.md:36,38`), 49 reglas, 22 gl (ADR-51), 9 parámetros (`modelo:251`), 9/14 (`modelo:11,273`), las 15 celdas de B (`procedencia.yaml:625-636`), 42+7 disparadores (`modelo:88,601`), 11 producciones (`produccion-modelo.tsv`), incisos (3)-(5) del bloque AJUSTE (`gobernanza:461-465`), ADR-57(a-e) (`gobernanza:619-627`), banner ADR-62 (`milpa-spec:4`), A.4 (`instrucciones v2_6:238`). **No derivadas:** el contenido de los tres dictámenes compass (espejo, tipo (3) — M6); y la equivalencia en esperanza matriz↔ABM independiente, que es un enunciado matemático de la propuesta, no un hecho del corpus — se prueba en la spec, no se cita.

**Contadores movidos por el trabajo que produjo este artefacto: 0.** Es un acto de diseño; los actos que moverían contadores (T1-A, SELLO-B/CORRIDA-B, primera corrida AJUSTADO) están gateados por decisiones de mesa nombradas en §8.

**(v2.4) Cantidades y escalas:** este documento no transcribe ninguna cantidad estimada; los `ASIGNADO` de §1.4 viajan con su clase y su cita, y §5 prohíbe explícitamente usarlo como dueño de valores.
