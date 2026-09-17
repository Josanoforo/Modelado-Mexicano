<!-- CABECERA DE PROCEDENCIA · añadida por ACTO GEN2-CELDA-D-CAREO-1 (A.3).
     El cuerpo que sigue a la línea de guiones es VERBATIM: no se editó una coma.
     Esta cabecera es del archivo, no del documento. -->

> **PROCEDENCIA (A.3 · archivo verbatim)**
> - **Clase:** INSUMO DE DIRECCIÓN tipo 3 — no entra al canon sin un acto de verificación posterior.
> - **Autor:** Dirección
> - **Fecha del documento:** 16/sep/2026 · **fecha de archivo:** 2026-09-16.
> - **sha256 del cuerpo verbatim, verificado por comando en este acto:** `8a6472a72631dfdcfbcd7be50db5760a214614e15b6afff9f862999ebf1e061d`
>   — coincide con el prefijo `8a6472a72631dfdc…` que el encargo declara.
> - **Archivado por:** `ACTO GEN2-CELDA-D-CAREO-1`, encargo `forense/encargos/2026-09-17-GEN2-CELDA-D-CAREO-1-TRES-DISENOS-UN-CAREO.md`, P0 (segunda entrega, tras el PARO de A.3).
> - **Nota:** Llegó al TERCER intento. `#822` P5 lo dejó `NO-CORRIDO` porque el adjunto no viajó (`NC-0271`); el lanzamiento de este acto tampoco lo trajo (`NC-0277`); mesa lo cargó después, en la misma sesión, y este acto lo archiva. Cierra la premisa de `NC-0271` («dirección re-envía el adjunto y un acto de trámite lo archiva con cabecera de procedencia tipo 3») y cierra `NC-0277`. Su §5 es la fuente de las dos referencias `[ADJ]` del diseño v1.0 §2.5, que hasta ahora se leían como del diseño porque el documento no estaba en el árbol.

---

# D-θ · Cargar Θ en el motor de decisión por celda
## v1.1 · corregida tras la revisión adversarial · 16 de septiembre de 2026

**Qué cambió respecto a v1.0.** La revisión adversarial (ADVERSARIAL-D-THETA-v1_0) encontró tres errores materiales que dirección reprodujo en el repo en `13536163` (merge de #817) y siete correcciones de método que se aceptan. La v1.0 se conserva como historia; esta v1.1 la sucede. Cada corrección lleva su marca `[H#]` y su evidencia. La recomendación de §6 es nueva: **piloto acotado de una ruta completa**, no política universal de bandas.

---

## 1 · Premisa corregida: los objetos, separados `[H1]`

Cuatro objetos que la v1.0 mezcló y que ahora se nombran distinto:

| Objeto | Qué es | Dónde vive | Estado |
|---|---|---|---|
| **B_matriz** | Matriz de coeficientes de generador, clave `(generador, coeficiente)`, 15 celdas: valores ASIGNADOS con algunos overrides MEDIDOS (ADR-220 selló enlace identidad para 3 pares con θ elegida-ciega y β̂ medido) | `milpa/src/matriz.py` (`cargar_B` desde `asignados_coeficiente.detalle`); `canon/modelo-decision-v4_0.md:466` | 15 celdas; **1 sin magnitud** (`G5 × familismo_obligacion`) |
| **b_persistencia** | Referencia externa del duelo: p(última ola de la misma serie al corte). Se consume en la comparación; **sus cifras no se adoptan al motor** | `forense/prereg-caja/TRIADA-B-PISO-spec-v1_0.md`; `CALC-TRIADA-B-PISO-0001` | Sellada como diagnóstico |
| **θ_k(x)** | Parámetros condicionados a la celda que g() consume | `milpa/src/theta.py` (stub E0: lanza para todo nombre); diseño E1 | Ningún nombre alcanza `ARGUMENTO_EXPLICITO`; escala y universo declarables por el esquema E1 |
| **Salida de conducta** | Lo que un consumidor (regla SI-ENTONCES, marcador, agente) lee | `milpa/src/motor.py` (veredictos de estado); `milpa/tramite.yaml` | La transformación generador → probabilidad no está implementada por el mero hecho de cargar θ `[H2]` |

**Lo que sigue siendo cierto de la v1.0:** lo que compitió en F5 como "M" fue el snapshot del emisor de reglas, no g(B_matriz, θ(x)) — confirmado por el adversarial en el código y los insumos de `CALC-TRIADA-0002`. **Por eso F5 no valida ni refuta el motor matricial futuro** `[H7.3]`.

---

## 2 · Lo que el motor tiene hoy, corregido

### 2.1 El bloqueo anterior a θ `[H2]` (reproducido por dirección, 16/sep)
```
B = cargar_B(Procedencia(crudo=yaml.safe_load('milpa/procedencia.yaml')))
→ 15 celdas, 1 CoeficienteSinMagnitud
g(B, θ_stub_que_devuelve_0.5, {"formalidad":"segsoc=1"})
→ SinMagnitud: `G5 × familismo_obligacion`: signo negativo o no monotónico — SIN MAGNITUD.
   No se computa como cero — decidir su forma es acto propio.
→ llamadas a theta.valor: 0
```
El bucle inicial de `g()` recorre toda B y se detiene antes de multiplicar. **Ninguna carga de θ hace computable g() con la matriz completa.** Resolver `G5 × familismo_obligacion` es un acto propio (decisión de forma), no una imputación, y es prerrequisito de cualquier piloto que pase por G5 — o el piloto elige una ruta que no lo toque, y lo dice.

### 2.2 La deuda de dispersión, reformulada `[H3]`
`canon/modelo-decision-v4_0.md` §6: "las **15 familias de distribución** exigidas por ADR-28.d no están declaradas — mientras falten, el check de varianza intra-celda no puede correr". La representación "90 parámetros de perfil" (E1 §4.4, v1.0 §2.2) es la de `modelo-decision-v3_2` y está superada. La deuda no desaparece: cambia de objeto. **Consecuencia:** el piloto se dimensiona por las **condicionales que efectivamente consume**, no por un censo de 90 ni de 15; y E1 debe enmendar su §4.4 leyendo v4.0 §1.1 y §6, sin recenso general.

### 2.3 Lo que E1 sí dejó firme (sin cambio)
Esquema de tres campos (`escala`, `universo`, `identificacion`); censo nombre por nombre; ninguna θ propia con `ARGUMENTO_EXPLICITO` (el único intento, G3 en panel ENNViH/MxFLS, murió por potencia); los 7 coeficientes sellados como `ASOCIACION-MEDIDA·*` (SIN-PROCEDENCIA-VERIFICABLE por D3(b)); `G5_familismo_apoyo` mal colocado en `procedencia.yaml`. **Corrección a v1.0:** "el canon no declara escala para ninguna salida de generador" es falso en absoluto — ADR-220 declara enlace identidad para pares específicos; que ese enlace sea científicamente suficiente es otra pregunta, y sigue abierta.

### 2.4 Evidencia F5 (sobre el emisor; recalculada por el adversarial y coincide al sexto decimal)
MAE U3=12: M 4.986673 · L_SOLO 3.957362 · L_CORPUS 3.889026; cívico 68.8759% del error de M; igual peso por las cinco familias: M 5.028 < L_SOLO 7.315 < L_CORPUS 7.529. **Lectura corregida `[blanco 1]`:** b_persistencia como referencia no es circular por compartir serie con R — pronosticar una ola con la anterior es un baseline legítimo si la información estaba disponible al corte y el estimando es comparable; lo contaminarían revisiones retrospectivas o filtros desiguales, no la fuente compartida. Fechas de publicación no certificadas.

---

## 3 · La decisión, reformulada `[H4]`

La v1.0 preguntaba "¿se carga Θ y cómo?" sobre objetos mezclados. La pregunta correcta se hace **por producto**, porque la falta de identificación causal no vuelve ilegítima una prevalencia descriptiva ni impide un predictor; solo impide leer una asociación como respuesta a una intervención:

| Producto | Pregunta | Evidencia que exige |
|---|---|---|
| Descripción | ¿Qué proporción presenta Y en esta población y periodo? | Universo, medición, muestreo, selección, precisión |
| Predicción | ¿Qué Y esperamos en una población/periodo objetivo? | Predictores disponibles al corte, soporte, **evaluación fuera del desarrollo** |
| Intervención | ¿Cómo cambia Y si modificamos A? | Estimando causal + identificación, o cotas de sensibilidad justificadas |
| Simulación de agentes | ¿Qué trayectorias genera una población sintética? | Distribuciones conjuntas/condicionales y sus dependencias; alcance de validación |

**Las opciones A/B/C se reinterpretan así:** B (esperar identificación) impone una barrera causal a productos descriptivos/predictivos que no la necesitan; C (banda universal) promete compensar esa barrera sin especificar el efecto causal al que la banda correspondería `[H5]`. Ninguna es una política única correcta para objetos estadísticos distintos. **Lo que se decide es un piloto**, con producto y estimando nombrados.

---

## 4 · La investigación, releída con las correcciones

- **Benchmark `[H10]`:** se conserva como **repertorio de métodos**, no como demostración de obligaciones universales. Se retira "todas presentes como obligatorias en los comparables". Li & O'Donoghue (2014) evalúan seis métodos de alineación y describen su uso extendido; **no prohíben alinear**. Ajustar a agregados de entrenamiento y evaluarse en otros datos no equivale a ajustar al árbitro de evaluación. OBR presenta incertidumbre *alrededor de una previsión central*: no respalda "rangos, no puntos" como oposición. La afirmación sobre CBO no se usa.
- **Prohibición de alinear θ al árbitro:** se mantiene **como decisión propia del programa** (aprendizajes §5: "no ajustar p hacia R"), no como consenso de fuentes.
- **Edge cases `[H8, H9]`:** se retira "la inversión 3/3 del 4/ago es firma de una interacción". Contraejemplo del adversarial: media condicional aditiva `0.10 + 0.10X + 0.70Z` con `P(Z=1|X=1)=0.10`, `P(Z=1|X=0)=0.90` da marginales 0.27 vs 0.73 — inversión **sin** interacción, por confusión. Sobol no cura ese diagnóstico. Y las etiquetas **declaran** (escala, universo, ponderador, cuestionario, n chico); no transforman un β en p ni corrigen un ponderador: la transformación, restricción o abstención resuelve el uso. Una distribución marginal por atributo no determina la conjunta (dos binarios con prevalencia 0.5 coocurren entre 0 y 0.5; independencia fija 0.25 sin evidencia).
- **Fuentes `[blanco 7]`:** el adversarial abrió texto de Cinelli–Hazlett, Li–O'Donoghue y Vernon et al.; el resto sigue en resumen. Suficiente para un piloto; insuficiente para obligaciones universales.

---

## 5 · La incertidumbre, tipada `[H5, H6]`

La v1.0 trató como intercambiables seis objetos. No se obtiene cobertura sumando anchuras, y predeclarar una banda no le da validez. El piloto **elige un método por estimando** y declara qué contiene el intervalo, en qué escala, bajo qué supuestos y con qué cobertura:

| Objeto | Qué contiene | Cuándo aplica |
|---|---|---|
| IC muestral | Error de muestreo de un estimador (bootstrap de conglomerados) | Descripción, predicción |
| Heterogeneidad intra-celda | Distribución entre personas de la misma celda (ADR-28.d) | Simulación de agentes; **no** es un IC sobre la media |
| Intervalo predictivo | Rango de un resultado futuro | Predicción |
| Conjunto identificado | Región bajo restricciones explícitas (Manski/Molinari) | Intervención con supuestos débiles |
| Envolvente de escenarios | Rango al variar supuestos | Escenario; se llama así |
| Discrepancia simulador–realidad | Kennedy–O'Hagan; requiere priors sobre la discrepancia | Calibración de g() contra observación |

El E-value mide fuerza de confusión en escala de razón de riesgos; no es receta para ensanchar un IC de p o de un índice. Cinelli–Hazlett ajustan estimaciones e intervalos **dentro de un marco de regresión** con parámetros de sensibilidad definidos; no basta con añadir su robustness value a una salida del motor.

**Emitir ≠ decidir `[H6]`.** Una probabilidad no tiene dos signos; `[0.10, 0.90]` pasaría "ambos signos" y es inútil frente a un umbral de 0.50; `[-0.01, 0.01]` cruza cero y es informativo sobre la pequeñez del efecto. Regla nueva: **se emiten intervalos válidos aunque crucen cero; la decisión automática se abstiene cuando los valores admitidos llevan a acciones distintas bajo la regla del consumidor** (para un tier: si todos los valores del intervalo dan el mismo tier, la decisión es robusta; si no, ambigua). Fuera de soporte es otra razón, se declara aparte.

**Validación `[H7]`.** Descartar θ con datos retenidos (history matching) *usa* esos datos: después no son evaluación independiente. U3 ya fue observada y motivó decisiones: es diagnóstico e historia, no holdout. F5 evaluó el emisor. Regla: datos de desarrollo para calibrar/seleccionar; una partición no usada para seleccionar, para la evaluación final; si hoy no existe, el piloto es **factibilidad**, no validación. La frase del informe queda: **"candidato con incertidumbre declarada; valor predictivo añadido pendiente de evaluación"** — no "validado donde hay piso".

---

## 6 · Recomendación de dirección v1.1 (para firma de mesa)

Se adopta la recomendación sustitutiva del adversarial, con dos añadidos de dirección (marcados):

> **Se autoriza un piloto acotado de carga de θ para un estimando descriptivo o predictivo nombrado, sobre una ruta completa y ejecutable.** Se distinguen B_matriz, b_persistencia, θ_k(x) y la salida de conducta. La ausencia de identificación causal no impide el uso descriptivo o predictivo; impide atribuir efectos de intervención sin supuestos adicionales explícitos.
>
> Cada parámetro del piloto tiene fuente, unidad, universo, escala, transformación y consumidor compatibles. La incertidumbre se representa con el método que corresponda al estimando (§5); no se exige banda causal universal por el solo rótulo `AUSENCIA_DECLARADA`.
>
> Se emiten estimaciones válidas aunque sus intervalos incluyan cero. La decisión automática se abstiene cuando los valores admitidos llevan a acciones distintas bajo la regla del consumidor. Las limitaciones de soporte se declaran por separado.
>
> Los datos usados para ajustar o seleccionar parámetros no se presentan como validación final independiente. El piloto se compara con b_persistencia cuando sea construible bajo el mismo corte y estimando. Su resultado permanece experimental hasta superar la evaluación correspondiente.
>
> La dispersión y las dependencias se resuelven para las condicionales efectivamente consumidas (v4.0 §6: 15 familias, no 90 parámetros). No se declara completado el motor de agentes ni cerrada la deuda por ejecutar una ruta parcial.
>
> *[Dirección añade]* **El bloqueo `G5 × familismo_obligacion` se resuelve por alcance explícito o por la decisión de forma pendiente — nunca por imputación ni cero.** **Queda sellada, como decisión del programa y no como consenso de fuentes, la prohibición de ajustar θ al árbitro de evaluación.**

Lo que esto es: **A acompañada de incertidumbre apropiada; C cuando exista una receta justificada para ese estimando; abstención limitada al uso que carezca de soporte.** Lo que no es: una política idéntica para objetos distintos, ni una habilitación del motor completo.

---

## 7 · Siguiente acción: un solo piloto `[adversarial §6]`

**ACTO GEN2-THETA-PILOTO-1** (entorno según la ruta: nube si los valores de θ ya están sellados en el registro; caja si la ruta exige una corrida nueva — la cabecera lo deriva, no lo hereda):
1. **Elegir una salida y una ruta.** Parámetro que alimenta, enlace, función consumidora, dependencias. Resolver `SinMagnitud` por alcance explícito (una ruta que no pase por G5) o por su decisión de forma, no por imputación. Si no hay ninguna ruta compatible, **entregar esa incompatibilidad nominal**, no otro censo.
2. **Fijar el producto.** Descripción, predicción o escenario; población, periodo, eje homologado (el crosswalk F-17/NC-0240 cuando aplique), unidad, criterio de comparación.
3. **Congelar una receta suficiente** (COMMIT-1 antes de dato): método de estimación, tipo de incertidumbre (§5), tratamiento de dependencias; desarrollo y evaluación separados. E-value, Sobol o history matching solo si esa ruta los necesita.
4. **Producir una salida consumible:** estimación/intervalo/escenarios tipados; referencia b_persistencia si existe; estado del consumidor: decisión estable, ambigua o fuera de soporte.
5. **Parar y decidir.** Sin evaluación independiente, factibilidad; con ella, desempeño y alcance. El informe no pasa a "validado" por éxito técnico.

**Lo que no precede al piloto:** archivar dos investigaciones completas, reclasificar veinte edge cases ni abrir capas de gobernanza. La corrección de E1 §4.4 (15 familias) y este documento viven en la misma entrega.

---

## 8 · Lo que sigue abierto y quién lo decide
- `G5 × familismo_obligacion`: decisión de forma (acto propio) — mesa.
- E1 §4.4 → v4.0 §6 (15 familias): enmienda — el acto del piloto.
- Ubicación del esquema E1 (campo en `procedencia.yaml` vs capa separada): mesa (hueco §5 de E1).
- Crosswalk de ejes (F-17/NC-0240): prerrequisito del marcador por segmento, no del piloto.
- Panel de validación independiente para el motor matricial: no existe hoy; F6 no lo es todavía.

---

### Anexo · Respuestas del adversarial a los nueve blancos, aceptadas
1 no circular por fuente compartida (contamina la revisión retrospectiva, no la serie) · 2 C no es procedimiento validado; se evalúa método por método · 3 el 10% se retira; se sustituye por impacto sobre estimando y decisión · 4 validación disjunta no demostrada; F6 pendiente no es validación · 5 los consumidores se especifican; no punto medio silencioso · 6 ninguna opción autoriza inferencia individual desde agregado; validar agregados acredita agregados · 7 resúmenes insuficientes para obligaciones universales · 8 S2 sigue, reformulada; se dimensiona por condicionales consumidas · 9 emisor/motor se sostiene, y por eso F5 no transfiere al motor.
