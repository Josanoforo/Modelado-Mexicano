# El motor adaptativo por celda: seleccionar el estimador, no imponerlo
### Propuesta sin sello · v0.1 · 11/ago/2026

> | | |
> |---|---|
> | **CLASE** | Propuesta. **No es decisión.** No rige hasta que exista un ADR en `gobernanza`. No edita ningún archivo existente: su perímetro es este documento |
> | **ORIGEN** | Encargo directo del usuario, protocolo "2 IA + 1 humano" (IA1 arquitecta-operadora, IA2 Fable adversaria, mesa humana). Continúa el mismo patrón de sesión que ya produjo `propuesta-motor-matriz-v0_1.md` y `propuesta-motor-como-contexto-2026-07-30.md` |
> | **PROCEDENCIA** | Las cifras del programa citadas aquí son tipo (1): derivadas o citadas archivo:línea contra clon de `origin/main` (rama de trabajo `claude/motor-adaptativo-celda-wk91nl`, base = `99190ef`). Cuatro investigaciones de solo-lectura (subagentes) alimentaron este documento con hallazgos citados; donde una cita proviene de una de ellas sin verificación directa mía, se marca **(agente)**. El argumento arquitectónico es tipo (3) |
> | **QUÉ DECIDE** | Si el programa adopta, para cada estimando requerido por MILPA, un contrato uniforme de **comparación de estimadores** (baseline/challenger/champion, con salida nativa heterogénea) en vez de decidir el estimador celda por celda sin registro ni criterio pre-declarado — y si "finanzas del hogar" es la vertical piloto |
> | **QUÉ NO DECIDE** | Ningún valor de ningún parámetro; la granularidad final D de ningún eje; si el programa adopta el cómputo matricial de `propuesta-motor-matriz-v0_1.md` como forma del motor (pregunta M1 de ese documento, intacta); qué celdas concretas se ejecutan primero dentro del piloto (eso es producto del piloto, no de esta propuesta) |

> ⚠️ **Encargo recibido con material de referencia que no existe verbatim en este repositorio.** El protocolo original nombra cinco archivos (`BENCHMARKS-metodologicos-D-ABC.md`, `EDGE-CASES-y-literatura-reciente.md`, `CAREO-benchmarks-4RT-archivo-proyecto.md`, `auditoria_adversarial_benchmarks.md`, `red-team-auditoria-benchmarks.md`) y dos con fecha/versión distinta a la real (`catalogo-fuentes-v1_0.md` → hoy `data/catalogo-fuentes-v2_0.md`; `cruce-catalogo-fichas-2026-07-30.md` → hoy `forense/cruce-catalogo-fichas-v1_0.md`/`v2_0.md`, sin esa fecha). Búsqueda por nombre y por contenido (grep de "D-ABC", "CAREO", "4RT", conteos "119/38/32") no los encontró en `main` ni en ninguna rama remota — **NO-ENCONTRADO, universo declarado: todo el árbol de trabajo + `git log --all`, 11/ago/2026**. Es plausible que vivan en el "espejo del proyecto" que ya alimentó a `propuesta-motor-como-contexto-2026-07-30.md` antes de su recuperación (`forense/hallazgos.md`, entrada 2026-08-10 citada abajo). Esta propuesta **no se detiene a esperarlos**: usa el material real y equivalente que sí existe (§1), y dado que ese material es en varios puntos *más reciente* que las cifras que el encargo cita (p. ej. el catálogo ya corrigió 119→128 fuentes únicas, ver §1.4), no hay evidencia de que la sustitución empobrezca el análisis. Mesa: si esos cinco archivos existen fuera del repo, decisión **M0** de este documento es si deben incorporarse antes de que el veredicto de Ronda 1 se considere completo.

---

## 0 · La tesis, en cuatro eslabones

1. **El estimando manda, no el estimador.** Lo que MILPA necesita —un coeficiente, una condicional, un momento de desenlace— existe antes y con independencia de qué modelo lo produzca. Fijar de antemano "todo se calibra por SMM" o "todo se lee de ENIGH" es el mismo error de categoría en dirección opuesta a fijar de antemano un valor.
2. **El estimando más el dato disponible acotan, no eligen, la familia de modelos elegibles.** `forense/metodologia-identificacion-vs-ajuste-v0_1.md:114-130` **(agente)** ya ordenó cinco rutas por fuerza de garantía —panel intra-sujeto > pseudo-panel de cohortes > ajuste por momentos > transversal con selección > composición—; esa jerarquía es la semilla de "modelos elegibles" en el contrato de abajo, no una invención de esta propuesta.
3. **La comparación entre lo elegible decide el estimador — nunca la sofisticación.** Sin un baseline y un criterio de victoria declarados *antes* de correr el challenger, "elegimos el mejor modelo" es indistinguible de "elegimos el modelo que nos gustó el resultado" — exactamente el defecto anti-post-hoc que `forense/prompts-verticales-validacion.md:40` ya nombró y parchó para las verticales de negocio, aplicado aquí a estimadores en vez de a casos.
4. **La salida hereda la forma que el estimador honesto produjo.** Forzar todo a un punto cuando el diseño solo sostiene una banda es el mismo defecto que `propuesta-motor-matriz-v0_1.md:148` ya declaró para los 15 β: *"decirlo antes es lo que impide leerlo como fracaso."*

**Esta propuesta no es una arquitectura nueva de cero: es el nombre y el contrato para una comparación que hoy no tiene ni nombre ni contrato.** El programa ya declara estimandos (`instrucciones-proyecto-v2_6.md:238`, `production-spec.schema.json:11`), ya cataloga fuentes (`data/catalogo-fuentes-v2_0.md`), ya registra estados de identificabilidad por coeficiente (`forense/censo-estimabilidad-coeficientes-v1_0.md`) y ya ejecuta mediciones bajo contrato ciego (`tools/curador_registro/schemas/production-spec.schema.json`). Lo que no existe en ningún punto del repo es un lugar donde, para un mismo estimando, **dos o más candidatos compitan bajo un criterio pre-declarado y quede escrito quién ganó y por qué** — verificado por grep de "champion", "challenger" y "NROY" en todo el árbol: **0 apariciones de los tres, en cualquier archivo** (agente). Esta propuesta llena ese hueco específico; no reemplaza nada de lo anterior.

---

## 1 · Antes de construir nada: cuatro colisiones de vocabulario que hay que resolver primero

Un vocabulario nuevo que colisiona con uno vigente no es un defecto cosmético cuando el vigente ya tiene contadores de canon atados a él (README.md:34-46). Las cuatro colisiones siguientes se resuelven aquí, no se heredan sin resolver hacia Ronda 1.

### 1.1 "Celda" ya tiene dos sentidos activos, ninguno el de este encargo

`propuesta-motor-matriz-v0_1.md` —el documento más reciente del repo antes de esta rama, todavía sin sello— usa "celda" para: **(a)** una región del producto de los seis ejes de atributos demográficos (`:35`, "celda-x" en adelante); **(b)** una entrada no-cero de la matriz coeficiente×generador, "15 celdas no-cero sobre 9 columnas" (`:65`, "celda-B" en adelante). El encargo pide una tercera cosa: estimando × dominio sustantivo × fuente/diseño disponible. Llamarla "celda" sin apellido produce homónimos activos en el mismo repo el mismo mes. **Resolución de esta propuesta: se llama celda-D (D de demanda), nunca "celda" sola**, y se cita explícitamente contra celda-x y celda-B cada vez que la ambigüedad sea posible.

### 1.2 "Vertical" ya está tomada — el programa usa "dominio"

Grep de "vertical" en `forense/` (agente) muestra un uso establecido y distinto: las validaciones forenses de casos de negocio reales contra el modelo — crédito fácil, crédito popular, clientelismo electoral, consumo aspiracional (V1-V4, `forense/curaduria-archivos.md:53`; metodología en `forense/prompts-verticales-validacion.md:19,32-43`). Para dominios sustantivos (trámites, finanzas, seguridad…) el programa usa **"dominio"**, heredado de los diez códigos de `data/inventarios/` (FIN/MIG/TEC/CAP/CUL/SAL/SEG/TRA/EST/TIE, `forense/cruce-catalogo-fichas-v1_0.md:89-90`, agente). **Resolución: esta propuesta usa "dominio" para lo que el encargo llama "vertical sustantiva"**, y reserva "vertical" para V1-V4 cuando el contexto lo requiera. El encargo y el prompt de Ronda 1 (Anexo A) conservan "vertical" tal como se escribieron, porque están citados verbatim para pegarse.

### 1.3 "Motor" ya nombra cuatro cosas distintas

El "motor de decisión" de `milpa-spec §5` (DSL de reglas, `milpa/milpa-spec-v0_2.md:190`) no es `propuesta-motor-matriz` (cómputo bilineal sobre atributos) ni `propuesta-motor-como-contexto` (función externa: sustituto vs. contexto de un LLM) ni esto. Esta propuesta no rebautiza ninguno de los tres —no es su encargo—, pero en prosa se refiere a sí misma como **"el selector"** para no sumar una quinta lectura a la palabra más sobrecargada del programa.

### 1.4 "Baseline" ya significa otra cosa en este repo, y las cifras del encargo ya están desactualizadas

`grep -rc baseline` (agente) da resultados en 121 archivos, siempre en el sentido de *snapshot* de regresión de la suite (`tests/check.py --baseline`, `tests/baseline.json`, `tools/curador_registro/baseline.py`) — nunca en el sentido de "estimador de referencia frente al cual compite un challenger". Esta propuesta usa "baseline" en el segundo sentido (es el que pide el encargo) pero declara la colisión: si esta arquitectura llega a implementarse en código, el campo debe llamarse `baseline_celda` o equivalente, nunca `baseline` sin apellido, para no chocar con el archivo real `tests/baseline.json`.

Adicionalmente, y sin reabrir nada: el "estado de partida" del encargo (119 fuentes únicas, 38 operables, 32 operables sin descargar) es la cifra de `catalogo-fuentes-v1_0.md`/`cruce-catalogo-fichas-v1_0.md` (9/27 fichas con criterio propio, agente). El catálogo real vigente es v2.0: **128 fuentes únicas (no 119), 43 operables (no 38)**, tras la corrección de identidad MAP-1 del 6/ago (`data/catalogo-fuentes-v2_0.md:62-84`, verificado directamente). El cruce a granularidad de condición del Umbral, también v2.0, da 7 VIABLE + 6 VIABLE ECOLÓGICO + 5 NO ENLAZA + ~16 NO EXISTE sobre ~34 condiciones (`forense/cruce-catalogo-fichas-v2_0.md:30-39,116-118`, agente). Esto no reabre el trabajo del "segundo motor": lo actualiza con una corrección que el propio programa ya hizo y selló antes de esta sesión.

---

## 2 · La celda-D — definición operacional

**celda-D = (estimando requerido por MILPA) × (dominio sustantivo) × (fuente o conjunto de fuentes con diseño disponible).**

Una celda-D no es una fila del canon: es una **vista de trabajo** sobre objetos que el canon ya nombra. Un mismo coeficiente de generador (`modelo §2.2`, 15 en total, todos `ASIGNADO` hoy) puede abrir **varias** celdas-D si hay más de un candidato de dato/diseño — exactamente el caso que `forense/REVERIFICACION-DEMANDA-vs-UNIVERSO-2026-08-07-v1_0.md:74` (verificado directamente) ya documentó para `aversion_riesgo`/`sens_estatus`: la búsqueda se cerró sobre 5 instrumentos (ADR-52A/54) y el índice completo sirve, sin que nadie los haya mirado, ENSAFI y ENFIH — dos celdas-D nuevas sobre el mismo par de coeficientes, ninguna de las cuales reabre el ADR por sí sola (reabrirlo es decisión de mesa, no resultado automático de listar el candidato).

Relación con lo que ya existe, declarada para que nadie la reinvente:

| Objeto existente | Qué resuelve | Qué NO resuelve (el hueco que llena celda-D) |
|---|---|---|
| `forense/censo-estimabilidad-coeficientes-v1_0.md` | Si existe **algún** camino de identificación por coeficiente (RUTA-A/I/C/SIN-RUTA), sin abrir microdato. Cobertura 15/15: A=3, C=2, I=1, SIN-RUTA=9 (agente, verificado contra mi propia lectura de `propuesta-motor-matriz-v0_1.md:50` para el patrón de conteo) | No compara estimadores ni declara criterio de victoria — "no existe campo de modelos elegibles" (agente) |
| `forense/REVERIFICACION-DEMANDA-vs-UNIVERSO-2026-08-07-v1_0.md` | Cruza cada necesidad contra el universo completo (~24,200 URLs, no solo lo bajado) y pide un "REGISTRO DEMANDA↔UNIVERSO" unificado (§6) | Fue encargo de inventario, no de comparación de modelos; no declara baseline ni challenger |
| `tools/curador_registro/` (código real, no propuesta) | Implementa exactamente ese registro demanda-universo: identidad `(necesidad_id, fuente_canonica_normalizada, objeto_evidencia_id_canonico)`, estados `CONFIRMADA/NEGATIVA/CANDIDATA/NO_ACCESIBLE` (`baseline.py:25`) | Clasifica si una fuente **satisface** una necesidad, no si **gana** frente a otra que también satisface — no hay noción de comparación entre CANDIDATAs |
| `tools/curador_registro/schemas/production-spec.schema.json` | Contrato ciego para **una** ejecución: `estimando`, `poblacion`, `dominio`, `diseno_muestral`, `tipo_inferencia`, `criterio_parada`, hashes de reproducibilidad — y **prohíbe explícitamente** (`properties: ... : false`) que se le adjunte `signo_esperado` o `resultado_favorable` | No tiene noción de que dos specs compitan por el mismo estimando; no declara cuál es baseline |
| `forense/matriz-impacto-universal-2026-08-06.md` | 10 estados operativos (NO-ENCONTRADO-EN-UNIVERSO-DECLARADO … SATISFACE-UMBRAL … REQUIERE-DECISION-DE-MESA) sobre reglas, coeficientes y condicionales | Un solo candidato por fila; no hay ranura para "perdió frente a otro candidato que sí satisface" |

**La celda-D no sustituye ninguna de estas piezas: las coordina.** Concretamente: cuando una `relacion` del curador llega a `CANDIDATA` y hay más de una para el mismo `necesidad_id`, ahí nace una celda-D. Cuando esa celda-D declara ganador, ese ganador se materializa como un `production-spec` (o varios, uno por candidato) bajo el contrato ciego que ya existe.

---

## 3 · El contrato de una celda-D, campo por campo

```yaml
celda_d:
  id: <string>                       # estable, no se reasigna
  estimando: <string>                 # cita el objeto de canon: coeficiente/condicional/regla/momento
  dominio: <FIN|MIG|TEC|CAP|CUL|SAL|SEG|TRA|EST|TIE>   # códigos ya vigentes de data/inventarios
  poblacion_objetivo: <string>        # la que MILPA necesita, no la que el instrumento cubre
  candidatos:                         # >= 1; el baseline cuenta como candidato
    - rol: BASELINE | CHALLENGER
      fuente: <string>
      diseno: <string>                # panel | pseudo-panel | ajuste_momentos | transversal_seleccion | composicion | registro_administrativo
      production_spec_ref: <especificacion_id o NINGUNO-AUN>
  criterio_victoria: <string>          # declarado ANTES de correr cualquier challenger; ver §3.5
  champion_actual: <rol.fuente o NINGUNO>
  output_nativo: {tipo: <ver §3.6>, valor_ref: <archivo dueño, nunca un número transcrito aquí>}
  incertidumbre: <string>
  supuesto_transporte: <EXISTE-SATISFACE | ACOTADO-CON-SUPUESTO:<cual> | NO-TRANSPORTABLE:<por que>>
  estado_epistemologico: IDENTIFICADO | AJUSTADO | CALIBRADO | ACOTADO | ASIGNADO
  estado_operativo: LISTO | LEGACY | PENDIENTE | EXCLUIDO
  requiere_decision_mesa: <bool>
  fecha_declaracion: <YYYY-MM-DD>      # anti-circularidad: antes de escanear, §3.5
```

### 3.1 · Estimando y dominio

El campo `estimando` no se redefine aquí: es el mismo objeto que `production-spec.schema.json:11` ya exige y que `canon/gobernanza-v1_15.md:629` ya usa. `dominio` reutiliza los diez códigos de los inventarios en vez de inventar una lista nueva.

### 3.2 · Dato y diseño disponible — con la distinción que el encargo pide

**Dato faltante** (se resuelve buscando, adquiriendo o ejecutando): ninguna fuente del universo declarado contiene el estimando o su co-observación — vocabulario exacto de A.4 (`instrucciones-proyecto-v2_6.md:240-245`, verificado): `NO-ENCONTRADO` (se buscó, no apareció, con universo y términos declarados), `NO-ACCESIBLE` (pago, afiliación o restricción legal — registro gratuito no cuenta aquí), o "nadie ha corrido el mecanismo" cuando el acceso existe pero no se ha ejecutado.

**Transporte inviable** (no se resuelve buscando más): el dato existe, fue medido, es accesible — pero la población, el periodo o la unidad que produjo la medición no es la que el estimando necesita, y no hay supuesto de reponderación creíble que cierre la brecha. Ejemplo real, ya sellado, sin cifra nueva inventada: `forense/hitoD-R1_1-veredicto-v1_0.md` (verificado directamente, líneas 33-70). El falsador de R1.1 pedía productores de temporal con participación voluntaria y sostenida en un seguro agrícola. El dato **existe**: los Fondos de Aseguramiento operan, tienen padrón, CSV abiertos. Pero el 62-66% de esa cobertura vive en Sonora/Sinaloa/Tamaulipas — agricultura de riego, tecnificada — y el instrumento que sí alcanza al productor de temporal vulnerable **no puede ser contratado por él** (`SADER`, citado en el veredicto: "este seguro NO PUEDE SER CONTRATADO POR LOS PRODUCTORES"). Descargar más CSV de AGROASEMEX no cierra esa brecha: es un hueco de mercado, no un hueco de archivo. El veredicto correcto no fue "buscar más" — fue **D, inejecutable**, y el propio Hito D ya distingue esto de una refutación (§8 de este documento).

### 3.3 · Modelos elegibles

Semilla, no lista cerrada — jerarquía ya existente por fuerza de garantía (`forense/metodologia-identificacion-vs-ajuste-v0_1.md:114-130`, agente): panel intra-sujeto > pseudo-panel de cohortes > ajuste por momentos (SMM/indirecta, `propuesta-motor-matriz-v0_1.md §4.1`) > transversal con selección > composición. A esto se añade lo que `censo-estimabilidad` ya clasificó por coeficiente (RUTA-A/I/C/SIN-RUTA) como **restricción de entrada**: una celda-D en SIN-RUTA no tiene challenger disponible hoy — su estado operativo es `PENDIENTE`, no un fallo de esta arquitectura.

### 3.4 · Baseline, challenger, champion

- **Baseline**: el valor o método que ya existe sin esta comparación — en la mayoría de los 74/144 números del programa hoy (`canon/estado-programa-v1_10.md:123,162`, agente), el baseline literal es el `ASIGNADO` vigente en `procedencia.yaml`. Un baseline no necesita ser bueno; necesita ser **el que ya se estaba usando**, para que la comparación sea honesta sobre qué mejoró.
- **Challenger**: un candidato competitivo declarado con su `production_spec` propio (§2, tabla) antes de conocer su resultado.
- **Champion**: el candidato — baseline o challenger — que gana bajo el criterio de victoria pre-declarado. **Que el baseline siga siendo champion es un resultado válido y debe registrarse como tal**, no como "no se hizo nada" (responde directamente a la pregunta I del encargo).

### 3.5 · Criterio de victoria — anti-circularidad

Se declara en `fecha_declaracion`, antes de correr el challenger — mismo patrón de dos commits que `propuesta-motor-matriz-v0_1.md §3.3` ya usa para el catálogo de momentos, y misma disciplina ANTI-POST-HOC que `forense/prompts-verticales-validacion.md:40` ya impuso para las verticales de negocio. Ejemplos de criterio admisible: reproducción dentro de banda de un momento **HOLDOUT** no usado en el ajuste (roles que ya define `propuesta-motor-matriz-v0_1 §6`); menor error cuadrático fuera de muestra; robustez a una perturbación de diseño pre-especificada. **No es admisible**: "el que dio el signo que esperábamos".

### 3.6 · Output nativo

Los siete tipos del encargo, con la regla de cuándo cada uno es honesto — no una preferencia estética:

| Tipo | Cuándo es la salida honesta |
|---|---|
| Punto | El diseño identifica o ajusta sin ambigüedad de dirección ni de escala |
| Distribución | El objeto mismo es una distribución condicional (las 14 condicionales de Θ, `modelo:253`) |
| Intervalo | Hay incertidumbre muestral cuantificable sobre un punto identificado |
| Conjunto identificado / banda | El diseño solo acota (Manski/Ferson, ya adoptado por `propuesta-motor-matriz-v0_1 §4.2` para los 15 β) |
| Función | El estimando es una respuesta continua a un disparador continuo, no un escalar |
| Matriz de transición | El desenlace es un estado discreto que cambia en el tiempo (candidato natural: R5.1/ENASEM, panel) |
| Región NROY | Un ejercicio de calibración conjunta deja varias combinaciones de parámetros "no descartadas todavía" — concepto con **0 apariciones previas** en el repo (agente); se introduce aquí por primera vez, y por eso necesita el escrutinio más alto de Ronda 1 |

### 3.7 · Estado epistemológico — reconciliado con canon, no paralelo a él

El encargo pide `IDENTIFICADO, AJUSTADO, ACOTADO, CALIBRADO, ASIGNADO`. Dos de esos cinco nombres **ya están sellados por ADR** con un significado específico (`canon/glosario-v5_6.md:353-356`; ADR-49 D2, `canon/gobernanza-v1_15.md:439`, agente) y no se redefinen aquí — se heredan:

- **ASIGNADO** = canon, sin cambio: "se puso a criterio" (`glosario:356`).
- **AJUSTADO** = canon, sin cambio: "reproduce los momentos observados de un dato real; no está identificado causalmente" (ADR-49 D2).
- **CALIBRADO** *(nuevo)* = un `AJUSTADO` obtenido específicamente por un ejercicio conjunto, multi-momento y pre-registrado que satisface las condiciones de `propuesta-motor-matriz-v0_1 §4.1` (momentos ≥ parámetros, W declarado, errores sándwich, chequeo de *sloppiness*). Es un `AJUSTADO` auditado, no una familia distinta — la distinción importa para el reporte, no divide el contador.
- **ACOTADO** *(nuevo)* = la salida es una banda o conjunto identificado que no colapsa a un punto (§3.6); puede partir de un ejercicio de fuerza `ASIGNADO` o `AJUSTADO` — es una propiedad de la *forma* del resultado, no un cuarto peldaño de fuerza causal independiente.
- **IDENTIFICADO** *(nuevo — es un nombre, no un estado nuevo)* = el nombre para lo que ADR-57(c) ya define como aprobado: una llave de identificación sellada fue ejercida (panel con desenlace, experimento natural, o diseño experimental de terceros). Hoy, **0 instancias** (`gobernanza:623-627`, agente) — nombrar el estado no crea ninguna.

**Regla explícita, análoga a `propuesta-motor-matriz-v0_1 §8`: ningún estado de celda-D mueve por sí mismo los contadores de canon (0/15, 9/14, 74/144).** Promover un contador sigue exigiendo el mismo sello que ya rige — ADR-57(c) para `IDENTIFICADO` con lectura de intervención, ADR-49/51 para `AJUSTADO`/`CALIBRADO`. Esto responde la pregunta C del encargo sobre "predicción": no es un sexto estado — es un **modo de uso** (evaluación contra momentos HOLDOUT) aplicable a cualquier estado salvo `ASIGNADO` puro.

### 3.8 · Estado operativo — rollup del vocabulario que ya existe, no uno paralelo

`LISTO/LEGACY/PENDIENTE/EXCLUIDO` se define como agregación de los 10 estados ya vigentes en `matriz-impacto-universal` (verificado directamente), para no crear un segundo vocabulario que alguien tenga que mantener sincronizado con el primero:

| Estado de celda-D | Rollup de (`matriz-impacto-universal`) |
|---|---|
| `PENDIENTE` | `NO-ENCONTRADO-EN-UNIVERSO-DECLARADO`, `INDEXADO-NO-DESCARGADO`, `DESCARGADO-NO-ABIERTO`, `ABIERTO-SIN-MAPEO`, `MECANISMO-NO-EJECUTADO` |
| `EXCLUIDO` | `NO-ACCESIBLE`, o supuesto de transporte declarado `NO-TRANSPORTABLE` (§3.2) |
| `LEGACY` | `NO-REPRODUCIBLE-CON-ARTEFACTOS-ACTUALES` (champion anterior sin pipeline ejecutable hoy) |
| `LISTO` | `SATISFACE-UMBRAL`, o champion vigente con `production_spec` ejecutado y auditable |

`REQUIERE-DECISION-DE-MESA` no tiene rollup limpio a los cuatro — se conserva como bandera `requiere_decision_mesa: true`, ortogonal a los cuatro estados, exactamente como ya opera de facto en `matriz-impacto-universal` (varias de sus filas en ese estado tienen además una condición de datos clara).

---

## 4 · Relación declarada, no resuelta, con `propuesta-motor-matriz-v0_1.md`

Ambos documentos nacieron con un día de diferencia y **tiran en direcciones distintas sobre la misma pregunta**: motor-matriz propone una forma computacional única —`m = Σ π(x)·h_r(B·θ(x), C(x))`— aplicada uniformemente a las 49 reglas vía SMM/inferencia indirecta; esta propuesta parte de que ninguna forma única debe imponerse celda por celda. **No son necesariamente incompatibles**: motor-matriz podría ser, para muchas celdas-D, el `CHALLENGER` de la familia "ajuste por momentos" (§3.3) — una entrada más en el menú, no el menú entero. Pero eso es una lectura de esta propuesta, no una decisión: motor-matriz sigue sin sello (`§8` de ese documento), su pregunta **M1** ("¿se adopta el cómputo matricial como definición del ejecutable?") sigue abierta, y esta propuesta no la contesta. Se declara la tensión para que Ronda 1 la examine con las dos propuestas en la mesa, no para que una entierre a la otra por omisión.

---

## 5 · Comparación de verticales piloto (dominios, en el vocabulario de §1.2)

| Criterio | Trámites / confianza institucional | Finanzas del hogar | Seguridad / violencia |
|---|---|---|---|
| Récord de falsación Hito D | **Mejor de las tres**: R3.1→B, R3.2→B, sin ningún D (`canon/estado-programa-v1_10.md:95`, agente) | **Peor de las tres**: R1.1→D (transporte, §3.2), R1.2→E, R1.3→E, ninguna A/B limpia | Intermedio: R7.2→D (variable degenerada `BP2_1`, agente), con reparación ya en curso (8 olas de ENVIPE agrupadas, `hitoD-preregistro-v2_0.md:717-733`, agente) |
| Fuentes operables | ~5-6/23 (agente) | ~7/15 (agente) | ~7/12 (agente) |
| Variedad de diseños | Transversal, panel (ENSU, único confirmado), registro administrativo, "usuario simulado" | Transversal, registro administrativo (CNBV/Banxico), panel (ENASEM/MxFLS con registro) — **la más variada de las tres** | Transversal, panel (ENSU), registro administrativo |
| Material fresco sin explotar | Moderado | **Alto**: ENSAFI/ENFIH recién identificados (`REVERIFICACION-DEMANDA §3`, verificado) tocan 4-5 de los 9 coeficientes SIN-RUTA a la vez | Bajo — el camino de reparación conocido ya está en marcha |
| Conexión con MILPA | **Directa y con nombre**: `R3.4` es literalmente el gate técnico de Fase 1 (`bt.oxxo_vs_codi`, `milpa-spec-v0_2.md:384-390`, agente) | Indirecta, vía coeficientes de G2-G5 | Indirecta, vía condicionales de G4 (ya `MEDIDO·PARCIAL`) |
| Riesgo propio declarado | Circularidad ya señalada en R3.2 (ENCIG como fuente y como prueba) | Ninguna fuente cataloga fondos de aseguramiento agropecuario — hueco estructural propio | — |

**Recomendación de IA1: finanzas del hogar**, por ser donde el aparato actual (un solo estimador por coeficiente, sin comparación) más claramente falla y donde hay más material nuevo y de diseño variado para que un selector adaptativo demuestre diferencia real. **Trámites/confianza es la alternativa fuerte**, casi exclusivamente por su conexión directa y nombrada con el gate de Fase 1 — un argumento de valor de proyecto que finanzas no tiene. Esta es una decisión con *tensión real*, no un cálculo dominado por una sola opción; se entrega a Ronda 1 (pregunta G) exactamente así, y la mesa decide después del veredicto adversarial, no antes (regla explícita del encargo).

---

## 6 · Ejemplo trabajado completo — una celda-D real, sin ningún número nuevo

Para probar que el contrato de §3 es operable y no decorativo, se llena con un caso ya sellado, sin transcribir ni un valor nuevo (mismo principio que `propuesta-motor-matriz-v0_1 §5`: "los valores se derivan del archivo dueño").

```yaml
celda_d:
  id: FIN.R1_1.aseguramiento_agricola
  estimando: "R1.1 (modelo §3.1) — horizonte de ahorro bajo volatilidad de ingreso"
  dominio: FIN
  poblacion_objetivo: "productores de temporal, volatilidad de ingreso máxima"
  candidatos:
    - rol: CHALLENGER
      fuente: "Fondos de Aseguramiento agrícola (AGROASEMEX, padrón + CSV abiertos)"
      diseno: registro_administrativo
      production_spec_ref: NINGUNO-AUN   # el veredicto D se declaró sin necesitar un production-spec: el confusor pre-registrado bastó
  criterio_victoria: "participación voluntaria sostenida >=3 ciclos, tasa >= ahorro formal de asalariados informales urbanos comparables (+-20%), EXCLUYENDO participación atada a crédito/programa"
  champion_actual: NINGUNO   # no hubo baseline formal previo para este falsador: es un candidato de falsación, no de calibración
  output_nativo: {tipo: "ninguno — veredicto D", valor_ref: "forense/hitoD-R1_1-veredicto-v1_0.md"}
  incertidumbre: "no aplica — D no es una estimación con banda, es un dictamen de inejecutabilidad"
  supuesto_transporte: "NO-TRANSPORTABLE: la cobertura del instrumento (62-66% en Sonora/Sinaloa/Tamaulipas, agricultura de riego) no alcanza a la población de volatilidad máxima que el estimando requiere, y el instrumento que sí la alcanza (Seguro Agrícola Catastrófico) es legalmente incontratable por el productor mismo"
  estado_epistemologico: ASIGNADO   # R1.1 sigue en el valor asignado que ya tenía; este ejercicio no lo cambió
  estado_operativo: EXCLUIDO
  requiere_decision_mesa: false
  fecha_declaracion: "2026-07-28"   # fecha del pre-registro original del falsador, no de este documento
```

Esto ilustra, con un caso real: (i) que "dato faltante" y "transporte inviable" son operacionalmente distinguibles (§3.2) — aquí hay CSV, hay padrón, y sigue siendo `NO-TRANSPORTABLE`; (ii) que un resultado `EXCLUIDO` sin champion es informativo, no un fracaso del contrato (pregunta I del encargo); (iii) que llenar el contrato no exige inventar ni una cifra.

---

## 7 · Lo que esta propuesta no resuelve

- **No elige el estimador de ninguna celda-D real.** Eso es trabajo del piloto, no de esta arquitectura.
- **No fija la granularidad D** de ningún eje de atributos — eso sigue siendo `propuesta-motor-matriz-v0_1 §9 M2`.
- **No decide M1** (¿cómputo matricial como definición del ejecutable?) ni resuelve la tensión de §4 — la declara para mesa.
- **No implementa `tools/curador_registro/`** ni le añade campos — propone dónde engancharía una comparación de candidatos, no lo construye.
- **No es canon.** Requiere ADR; sin él, es una hipótesis que gobernó una sesión.

## 8 · Preguntas para mesa

- **M0** · Los cinco archivos que el encargo original nombra (recuadro de apertura) — ¿existen fuera de este repo y deben incorporarse antes de cerrar Ronda 1, o el material equivalente real (§1) es suficiente?
- **M7** · ¿Se adopta "finanzas del hogar" como vertical piloto (§5), o pesa más la conexión nombrada de trámites con el gate de Fase 1?
- **M8** · La región NROY (§3.6) no tiene precedente en el repo — ¿se admite en el primer piloto o se aplaza hasta que exista un ejercicio de calibración conjunta que la necesite de verdad?
- **M9** · ¿El campo `criterio_victoria` se sella en el mismo commit que el catálogo de momentos de `propuesta-motor-matriz §3.3`, si ese catálogo llega a sellarse, o corre en un commit propio?

---

## 9 · Módulo de auditoría

**1-6** · No aplican: propuesta sobre arquitectura, no afirma nada sobre México salvo el ejemplo de §6, que es cita de un veredicto ya sellado.

**7 · ¿Qué conclusión sería peligrosa simplificada?** Tres. *"Ahora el programa elige el mejor modelo"* — esta propuesta define un contrato para comparar; no ha comparado nada todavía, y un contrato vacío no mueve un solo contador (§3.7). *"IDENTIFICADO es un estado nuevo que el programa alcanzó"* — es un nombre para una compuerta que ya existía y que sigue en cero llaves ejercidas; nombrarla no la abre. *"Como hay siete salidas nativas posibles, cualquier forma de reportar sirve"* — la tabla de §3.6 declara cuándo cada una es honesta precisamente para impedir que se elija la forma por conveniencia narrativa en vez de por lo que el diseño sostiene.

**8 · ¿Qué afirmación fue derivada y cuál no?** Derivadas o citadas archivo:línea contra `99190ef`: los conteos de §1.4 (128/43, 7/6/5/16), los estados epistemológicos de §3.7 (ADR-49 D2, ADR-57), el caso de §3.2/§6 (`hitoD-R1_1-veredicto-v1_0.md`, leído directamente), la tabla de §5 (récords de Hito D por dominio, `estado-programa-v1_10.md`). **No derivadas directamente por mí, sí por cuatro subagentes de solo-lectura cuyos hallazgos no re-verifiqué línea por línea**: las citas marcadas (agente) en §1-6 — en particular el conteo exacto de fuentes/diseños por cada uno de los 11 inventarios (§5) y la ausencia total de "champion"/"challenger"/"NROY" en el repo. Esta es la misma clase de honestidad que `data/catalogo-fuentes-v2_0.md:83` ya practica ("no se afirma una cifra más precisa que la que el propio `dedup.py` imprime") aplicada a verificación por agente en vez de por script.

**Contadores movidos por el trabajo que produjo este artefacto: 0.** Es un acto de diseño; ningún `production-spec` corrió, ninguna celda-D real fue evaluada más allá del ejemplo ya sellado de §6.

**(v2.4) Cantidades y escalas:** este documento no transcribe ninguna cantidad estimada nueva; las cifras citadas viajan con su archivo dueño y su fecha, y §6 usa explícitamente solo lo que un veredicto ya sellado contiene.
