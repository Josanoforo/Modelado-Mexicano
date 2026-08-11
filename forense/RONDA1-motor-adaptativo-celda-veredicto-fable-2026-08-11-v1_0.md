# RONDA 1 · Motor adaptativo por celda · Veredicto adversarial (mesa Fable)
### v1.0 · 11/ago/2026 · IA2 (Fable 5) contra `propuesta-motor-adaptativo-celda-v0_1.md` · rama `claude/motor-adaptativo-celda-wk91nl`, base `99190ef`

> | | |
> |---|---|
> | **ARCHIVO** | `RONDA1-motor-adaptativo-celda-veredicto-fable-2026-08-11-v1_0.md` |
> | **CLASE** | Artefacto forense fechado, append-only. Registra el veredicto emitido en esta sesión contra la v0.1 de la propuesta; no se reescribe si la propuesta se corrige — la corrección vive en la adjudicación y en la v0.2 |
> | **ORIGEN** | Protocolo "2 IA + 1 humano" del encargo del usuario. IA2 recibió el prompt adversarial original verbatim (transcrito íntegro en el Anexo de este archivo) más un mapa de material real, con herramientas de lectura sobre el repo y la instrucción explícita de verificar por sí misma, no de confiar en las citas de IA1 |
> | **VERIFICAS ASÍ** | Este documento reproduce el texto que IA2 entregó como respuesta final, con mínimo formateo de encabezado. La adjudicación de IA1 vive en `RONDA1-motor-adaptativo-celda-adjudicacion-v1_0.md`, archivo separado |

---

<!-- El cuerpo de este documento es el texto entregado por el agente IA2 (model: fable), sin editar salvo nivel de encabezados para anidarlo bajo este archivo. -->

## 1 · Veredicto ejecutivo

> Todas las rutas citadas son relativas a `/home/user/Modelado-Mexicano/`. Toda cita archivo:línea fue leída directamente en esta sesión salvo donde se marca lo contrario. Verificación propia del recuadro de apertura de IA1: los cinco archivos del encargo **no existen** en el árbol ni en `git log --all --diff-filter=A` (corrido en esta sesión); "champion"/"challenger" tienen **0 apariciones** en sentido de selección en la base `99190ef` (los dos únicos hits de mi grep insensible a mayúsculas para "NROY" son el apellido "Monroy" en `corpus/reports/`, falso positivo mío, no de IA1).

La arquitectura es adoptable: da nombre y contrato a una comparación que el corpus necesita y no tiene (verificado: cero usos previos de champion/challenger en la base), y se ancla en piezas reales — la jerarquía de cinco rutas (`forense/metodologia-identificacion-vs-ajuste-v0_1.md:114-130`), el contrato ciego (`tools/curador_registro/schemas/production-spec.schema.json:86-93`), los diez estados de `forense/matriz-impacto-universal-2026-08-06.md:8-12`. La sustitución de material que IA1 declara es honesta y verificable (128/43 vigente contra 119/38 del encargo, `data/catalogo-fuentes-v2_0.md:66,70`), pero su frase "no hay evidencia de que la sustitución empobrezca el análisis" exagera: el primer archivo faltante versa sobre `D-ABC`, que es una decisión de mesa viva y pendiente (`milpa/procedencia.yaml:780-781`), y `forense/hallazgos.md:131` documenta un precedente exacto de texto del espejo que resultó imprescindible e inexistente en el repo. M0 no bloquea este veredicto; sí debe resolverse antes de sellar los menús de "modelos elegibles".

Encontré ocho defectos materiales. Ninguno es conceptual; todos se corrigen con ediciones de una línea a un párrafo: la clave de identidad de la celda-D está definida de dos maneras incompatibles dentro del mismo documento; el vocabulario `diseno` colisiona sin declararlo con el campo `ruta:` que ADR-49 D2 ya selló; el rollup operativo omite un estado; falta el universo de búsqueda de candidatos (la lección A.4 aplicada al selector); los candidatos multi-fuente no son representables; `ACOTADO` duplica `output_nativo`; `criterio_victoria` carga dos semánticas; y no existe etapa de coherencia conjunta post-selección.

Piloto: **finanzas del hogar** — coincido con IA1 por razones parcialmente distintas, con dos correcciones a su tabla §5 que debilitan aún más la alternativa. Condición de semana 1: ENSAFI/ENFIH operables, con trámites como fallback nombrado.

**Conclusión: APROBAR CON CAMBIOS.**

---

## 2 · Defectos materiales

| # | Defecto | Evidencia en los archivos | Efecto sobre resultados | Corrección mínima | ¿Bloquea piloto? |
|---|---|---|---|---|---|
| **D1** | **La clave de identidad de la celda-D está definida de dos maneras incompatibles** *(pregunta A)*. La definición pone la fuente en la clave; el contrato y la regla del curador la ponen dentro de la celda como atributo del candidato; el ejemplo ENSAFI/ENFIH no cuadra con ninguna lectura | Definición: `propuesta-motor-adaptativo-celda-v0_1.md:53` ("… × fuente o conjunto de fuentes"). Contrato: `:79-83` (`candidatos:` lista multi-fuente con rol BASELINE\|CHALLENGER dentro de UNA celda). Regla curador: `:67` ("más de una [CANDIDATA] para el mismo `necesidad_id`, ahí nace UNA celda-D"). Ejemplo: `:55` ("dos celdas-D nuevas sobre el mismo par de coeficientes" — pero el par toca 4 filas del censo: `forense/REVERIFICACION-DEMANDA-vs-UNIVERSO-2026-08-07-v1_0.md:74`, filas 3,4,6,11 de `:48-56`). Hasta el id del ejemplo (`FIN.R1_1.aseguramiento_agricola`, `:187`) mete la fuente en la clave mientras su lista `candidatos` sigue la otra lectura | IDs inestables desde la celda 1; la misma comparación puede registrarse partida en N celdas o duplicada; imposible contar celdas, champions o cobertura del piloto de forma reproducible | Clave = `estimando × poblacion_objetivo` (dominio se deriva del estimando); fuente y diseño pasan a ser **exclusivamente** atributos de cada candidato; reescribir la frase de `:55` como "dos candidatos nuevos en cada una de las hasta cuatro celdas-D de esas filas del censo" | **Sí** — es el sustrato del registro; arreglo de un párrafo |
| **D2** | **`criterio_victoria` carga dos semánticas sin declararlo** *(preguntas A y C)*: §3.5 lo define como adjudicación challenger-vs-baseline; el ejemplo §6 lo usa como umbral de falsación de una regla, sin baseline ni comparación | Definición: `:117` ("antes de correr el challenger… menor error fuera de muestra…"). Ejemplo: `:196` (el umbral del falsador de R1.1, con `champion_actual: NINGUNO`, `:197`) — que es la escala B-bis de las fichas de Hito D, no una comparación de estimadores. El campo comentado en `:76` admite "coeficiente/condicional/regla/momento" como estimando, mezclando objetos de adjudicación distinta (ADR-47 ya selló falsar ≠ calibrar, `canon/gobernanza-v1_15.md` §0.1) | El go/no-go del piloto contaría "champions" mezclando victorias de comparación con veredictos de falsación; el mismo campo significaría cosas distintas fila por fila | Campo nuevo `tipo_adjudicacion: COMPARACION \| FALSACION \| CALIBRACION_CONJUNTA`, y `criterio_victoria` → `criterio_adjudicacion`, con la escala B-bis heredada (no reinventada) cuando el tipo es FALSACION | **Sí** — una línea de schema, pero antes de registrar la primera celda |
| **D3** | **El enum `diseno` mezcla dos ejes y colisiona sin declararlo con vocabulario ya sellado** *(preguntas C y F)*. `ajuste_momentos` y `composicion` son estrategias de estimación, no diseños de dato; y ADR-49 D2 ya selló `ruta: pseudo_panel \| momentos \| composicion \| transversal_con_seleccion` con nombres casi-pero-no idénticos. La propuesta resuelve cuatro colisiones de vocabulario en §1 y omite esta quinta — bajo su propio estándar (`:29`) no es cosmética | Enum propuesto: `:82`. Vocabulario sellado: `canon/gobernanza-v1_15.md:439` (ADR-49 D2). Diseños reales del corpus ausentes del enum: experimento natural/discontinuidad — la llave (ii) de ADR-57(c) y la ruta ENOE "salario mínimo de franja fronteriza" (`gobernanza:623`), el RDD de R7.3 (`forense/cruce-catalogo-fichas-v2_0.md:89`); "usuario simulado" — nombrado por la propia tabla §5 (`:172`) y real en el corpus (`data/inventarios/inventario_fuentes_tramites_estado_mexico.md:466`); enlace ecológico — categoría de primera clase en el cruce ("VIABLE ECOLÓGICO… diseño distinto, no versión peor", `cruce-catalogo-fichas-v2_0.md:32-33`) | Dos vocabularios casi-idénticos para lo mismo, uno sellado y uno no; celdas con los diseños omitidos (los que ADR-57(c) necesita para `IDENTIFICADO`) no serían registrables | Partir en dos campos: `diseno_datos: panel \| pseudo_panel \| transversal \| registro_administrativo \| experimento_natural \| auditoria_campo \| enlace_ecologico` × `estrategia:` con los valores **verbatim** de ADR-49 D2 | **Sí** — es el vocabulario del registro; barato |
| **D4** | **Falta el universo de búsqueda de los candidatos** *(preguntas B y E)*: la lista `candidatos` es implícitamente la afirmación "estos son los elegibles", sin declarar contra qué universo se pobló — la clase (a) exacta del gap que A.4 existe para impedir, ahora al nivel del selector | `instrucciones-proyecto-v2_6.md:236,238-245`; `forense/AUDITORIA-PREMISAS-SELLADOS-2026-08-07-v1_0.md` §1 clase (a). Precedente vivo: la búsqueda "cerrada" sobre 5 de 137 programas que ENSAFI/ENFIH reabren (`REVERIFICACION:74`) | "Champion" significaría "campeón entre lo que casualmente miramos" — un cierre sin denominador | Campo `universo_candidatos: <qué se barrió, con qué mecanismo, fecha>` | **Sí** — un campo; sin él cada celda nace con denominador indeclarado |
| **D5** | **Los candidatos multi-fuente no son representables** *(preguntas B y D)*: `production_spec_ref` es singular por candidato pero la celda-D admite "conjunto de fuentes" y el menú incluye `composicion` | `:83`; `production-spec.schema.json:80-82` (mono-microdato). Celdas que la necesitan: fila 14 del censo, "falta puente entre instrumentos" (`REVERIFICACION:59`; `censo-estimabilidad-coeficientes-v1_0.md:78`) | Las celdas-D que más justifican el selector (los 9 SIN-RUTA) no podrían declarar su candidato principal | `production_spec_refs: []` (lista) + campo `regla_composicion: <declarada en fecha_declaracion \| NO-APLICA>` | **Sí para finanzas** — el piloto recomendado incluye exactamente esas celdas |
| **D6** | **`estado_epistemologico` no es exclusivo: la prosa hace de `ACOTADO` una propiedad de forma, el campo lo hace excluyente con `AJUSTADO`** *(pregunta C)*. Además `ACOTADO` duplica información que `output_nativo.tipo` ya carga | Prosa: `:140`. Campo: `:89` (enum de un solo valor). Duplicación: `:128` ⇔ `ACOTADO`. Una banda salida de SMM (`propuesta-motor-matriz-v0_1.md:148`) es AJUSTADO **y** ACOTADO a la vez — el campo obliga a perder una de las dos | Registros inconsistentes desde el día 1; los rollups serían incomparables entre celdas | Dos campos: `fuerza: ASIGNADO \| AJUSTADO \| IDENTIFICADO` + `calibrado: bool`; la forma se **lee** de `output_nativo.tipo`, no se re-declara | **Sí** — una línea; evita corromper el registro desde el arranque |
| **D7** | **El rollup de §3.8 omite `MAPEADO-NO-SATISFACE` (1 de los 10 estados) y confunde nivel-candidato con nivel-celda** *(pregunta B)* | Los 10 estados: `matriz-impacto-universal-2026-08-06.md:8-12`. La tabla de `:149-155` mapea 9; `MAPEADO-NO-SATISFACE` no aparece. Los estados de la matriz son por candidato-relación, mientras `estado_operativo` es por celda | Celdas con candidato examinado-y-descartado quedarían sin estado, o forzadas a un estado falso | Añadir el estado al rollup **y** declarar la regla de agregación explícita | **Sí** — dos líneas |
| **D8** | **No hay etapa de coherencia conjunta después de seleccionar champions celda por celda** *(pregunta E)*. La tensión con motor-matriz se declara (§4) pero el contrato no trae ni un campo ni una etapa que la detecte | `:160-162` (tensión declarada, sin mecanismo). El corpus ya tiene las piezas: el chequeo tipo ADR-30 (`propuesta-motor-matriz-v0_1.md:65`), los roles AJUSTE/HOLDOUT (`motor-matriz:104-112,130`), el chequeo de *sloppiness* (`motor-matriz:142`) | Champions individualmente ganadores, conjuntamente imposibles; el piloto "pasaría" sin haber probado lo único que el escalamiento necesita saber | El diseño del piloto sella en su commit 1 una lista corta de momentos HOLDOUT **globales** + una etapa de cierre de ensamble | **Sí en diseño** — debe estar en el commit 1 del piloto, no puede añadirse después sin ser post-hoc |

**Sobre M0:** la sustitución de IA1 es honesta (NO-ENCONTRADO con universo declarado, verificado por mí) y suficiente **para evaluar esta arquitectura**. No es defecto material bloqueante del piloto. Pero es insuficiente para sellar los **menús de modelos elegibles**: el faltante `BENCHMARKS-metodologicos-D-ABC.md` versa, por nombre, sobre la función de enlace que sigue sin sellar (`procedencia.yaml:780-781`; `motor-matriz:79,156`). Precedente de que el texto del espejo puede ser imprescindible: `hallazgos.md:131`. Disposición: mesa incorpora los cinco archivos o los declara irrecuperables **antes** del commit 1 del piloto.

---

## 3 · Mejoras no bloqueantes

1. **`fecha_adjudicacion` + `commit_adjudicacion`** junto a `fecha_declaracion` + `commit_declaracion`: el patrón real del programa es de dos commits (`motor-matriz:130`).
2. **Ranura de resultado por candidato** (`resultado: GANO | PERDIO:<margen> | NO-EJECUTADO | INEJECUTABLE`).
3. **Grafo fuente→celdas automatizado** (derivable de `candidatos`): ENIF sola aparece en ≥4 filas del censo (`censo:71,76,78`; `REVERIFICACION:48-59`).
4. **Menú cerrado de criterios de adjudicación a nivel piloto** (sellado en commit 1), del cual cada celda solo instancia parámetros.
5. **Registro de supuestos de transporte nombrados y reutilizables** (catálogo, no texto libre).
6. **Adjudicaciones `requiere_decision_mesa` por método de tres brazos** (`forense/metodo-tres-brazos-v0_1.md`).
7. **`incertidumbre` tipada y condicionada a `output_nativo.tipo`** (heredando `production-spec.schema.json:22`).
8. **`edicion/periodo` del candidato visible a nivel celda** (heredado de `periodo_levantamiento`, `production-spec.schema.json:27`).
9. **Registrar (sin ejecutar) las dos celdas LEGACY reales** — R3.1/R3.2, `NO-REPRODUCIBLE-CON-ARTEFACTOS-ACTUALES` — para probar que el estado LEGACY es representable.
10. **Nota de vocabulario en glosario al sellar**: "celda-D" contra celda-x y celda-B, y `baseline_celda`.

---

## 4 · Matriz de riesgos del selector por celda

| Riesgo | Mecanismo | Evidencia de que es real aquí | Severidad | Mitigación concreta |
|---|---|---|---|---|
| **Doble uso de datos / winner's curse** | La misma fuente elige al champion y provee su estimado | Régimen de pocas fuentes grandes reutilizadas (`censo:65-79`) | Alta | Momentos HOLDOUT por celda sellados en commit 1; criterio evaluado solo sobre holdout jamás tocado por ningún candidato |
| **Dependencia entre celdas** | Champions de celdas distintas comparten fuente → errores correlacionados tratados como independientes | ENIF es reactivo, desenlace y puente fallido en filas distintas del censo; ADR-30 ya vigila un caso (`motor-matriz:65`) | Alta | Grafo fuente→celdas (mejora 3); análisis de sensibilidad "quitar una fuente" |
| **Equifinalidad / sloppiness** | Dos candidatos reproducen los mismos momentos y divergen fuera de muestra | Riesgo dominante ya documentado del ajuste conjunto (`motor-matriz:142,148`) | Alta | Empate declarado = empate (no se adjudica); chequeo de sloppiness heredado de §4.1 motor-matriz |
| **Multiplicidad** | Decenas de adjudicaciones ⇒ champions falsos esperados sin control de error global | El piloto abrirá 10-15 celdas | Media | Go/no-go cuenta patrones, nunca celdas sueltas; menú cerrado reduce grados de libertad |
| **Coherencia conjunta ausente** | Champions individualmente óptimos, conjuntamente imposibles | Defecto D8 | Alta | Etapa de cierre de D8 + registro de supuestos nombrados |
| **Baseline débil / efecto halo** | El baseline literal es el `ASIGNADO` vigente — vencerlo es una vara bajísima | 74/144 sin calibrar (`estado-programa-v1_10.md:123`) | Media | Todo champion reporta desempeño absoluto contra holdout, no solo victoria relativa; clase de fuerza viaja con el rótulo |
| **Criterio a la medida** | Pre-declarar por celda no impide elegir el criterio que el challenger favorito va a ganar | Precedente ANTI-POST-HOC en verticales de negocio (`prompts-verticales-validacion.md:40`) | Media | Menú cerrado + auditoría de mesa por muestreo (método de tres brazos) |

---

## 5 · Comparación de verticales piloto y recomendación

Criterios del encargo más uno propio: **capacidad de estresar el selector**.

Dos correcciones verificadas a la tabla §5 de IA1, ambas contra trámites:

- La "conexión directa y nombrada con el gate de Fase 1" está sobredimensionada: el gate `bt.oxxo_vs_codi` exige A∧B∧C (`milpa-spec-v0_2.md:370,384-390`), y la propia ficha de R3.4 pre-registra que B y C degradan a inejecutables con fuente pública (`hitoD-preregistro-v2_0.md:841`; confirmado por `cruce-catalogo-fichas-v2_0.md:67`: "VIABLE ECOLÓGICO para A; NO ENLAZA para B/C"). Un piloto de trámites conectaría con un tercio operable del gate.
- El "riesgo propio" de trámites está sobredimensionado en dirección opuesta: la circularidad de ENCIG en R3.2 ya fue rastreada y resuelta ("no es circular medir el contraste ahí, porque el contraste nunca se extrajo de ahí", `hitoD-preregistro-v2_0.md:417,750`).

Sobre seguridad: la "reparación en curso" (8 olas ENVIPE) no está en curso — ya corrió y no alcanzó: 43 casos de asegurado×conocido caen en 42 conglomerados singleton, cero varianza estimable; donde sí se pudo medir, el IC cruza el umbral (`hitoD-preregistro-v2_0.md:717-733`).

**Recomendación: finanzas del hogar.** ENSAFI/ENFIH tocan 4 de los 9 SIN-RUTA a la vez más el puente de la fila 14 (`REVERIFICACION:74,78-81`); mejor variedad de diseños (transversal + registro administrativo CNBV/CONSAR/Banxico + la única llave de identificación viva del programa, ENNViH/MxFLS, RUTA-I); el peor récord de falsación es el terreno más informativo para un selector nuevo; el riesgo de dependencia entre celdas está documentado justo ahí (`censo:76`) — el riesgo E se prueba donde existe. Gate de semana 1: verificación byte a byte de que ENSAFI y ENFIH publican microdato utilizable (hoy "formato no verificado", `data/inventarios/inventario-fuentes-credito-ahorro-finanzas-hogar-mexico.md:145,197`); si ambos fallan, fallback nombrado a trámites, por decisión de mesa.

---

## 6 · Contrato mínimo revisado (ver adjudicación para la versión que IA1 adopta)

*(Fable propuso una versión completa campo por campo; se omite aquí para no duplicar — su contenido íntegro quedó incorporado, con las correcciones de IA1, directamente en `propuesta-motor-adaptativo-celda-v0_2.md §3`.)*

---

## 7 · Criterio go/no-go del piloto

**GO al escalamiento si y solo si:**
1. **Proceso**: 10-15 celdas-D FIN registradas con la clave corregida y `commit_declaracion` anterior en historia de git a todo resultado.
2. **Discriminación en ambas direcciones**: ≥3 celdas con baseline y challenger ejecutados; ≥1 donde el challenger gana y ≥1 donde el baseline retiene.
3. **Heterogeneidad compilable**: ≥2 tipos de output no-punto producidos y compilados en un dry-run hacia `procedencia.yaml`, sin colapsar banda→punto.
4. **≥1 negativo informativo registrado con estado, no con prosa**.
5. **Coherencia conjunta ejecutada** (D8).
6. **Gobernanza intacta**: contadores movidos = 0 salvo ADR.
7. **Costo medido**: horas/celda y bloqueos por clase.

**NO-GO / re-pilotar**: gate de semana 1 fallido sin sustituto → fallback trámites; o incumplimiento del punto 1.

---

## 8 · Decisiones que requieren al humano (propuestas por IA2)

1. M0: incorporar los cinco archivos del espejo o declararlos irrecuperables — antes del commit 1 del piloto.
2. ADR de adopción del contrato con las correcciones D1-D8.
3. Piloto: finanzas del hogar con gate de semana 1, trámites como fallback nombrado.
4. Reapertura acotada de ADR-52A/54 solo si la verificación byte a byte de ENSAFI/ENFIH encuentra reactivo.
5. Todo sello de EXCLUIDO/NO-TRANSPORTABLE y todo movimiento de contador o promoción de champion a canon. M8 (NROY): aplazar.

---

## 9 · Conclusión de IA2

**APROBAR CON CAMBIOS.**

La arquitectura llena un hueco real y verificado, y lo hace coordinando piezas existentes en lugar de duplicarlas, con una honestidad de procedencia que sobrevivió la verificación por muestreo en todos los casos sustantivos. Pero el contrato, tal como está escrito, no puede ejecutarse sin corromper su propio registro. Todas las correcciones son ediciones de una línea a un párrafo más un requisito de diseño del commit 1 del piloto; ninguna exige teoría nueva, ninguna reabre decisiones selladas, y ninguna justifica RECHAZAR una arquitectura cuyo fondo es correcto.

---

## Anexo · Prompt adversarial original recibido (verbatim, tal como fue transcrito del encargo del usuario)

*(Omitido en este archivo para no duplicar contenido — el texto íntegro que IA2 recibió está transcrito en el prompt de invocación del agente, sesión de esta rama, y coincide verbatim con la sección "Ronda 1 · Prompt adversarial para Fable 5" del encargo original del usuario.)*
