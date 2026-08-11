# El motor adaptativo por celda: seleccionar el estimador, no imponerlo
### Propuesta sin sello · v0.2 · 11/ago/2026

> | | |
> |---|---|
> | **ARCHIVO** | `propuesta-motor-adaptativo-celda-v0_2.md` |
> | **REEMPLAZA A** | `propuesta-motor-adaptativo-celda-v0_1.md` — se conserva, no se borra: es el registro exacto de lo que Ronda 1 revisó |
> | **CLASE** | Propuesta. **No es decisión.** No rige hasta que exista un ADR en `gobernanza` |
> | **ORIGEN** | Ronda 1 del protocolo "2 IA + 1 humano": v0.1 (IA1) → veredicto adversarial (IA2/Fable, `forense/RONDA1-motor-adaptativo-celda-veredicto-fable-2026-08-11-v1_0.md`) → adjudicación (IA1, `forense/RONDA1-motor-adaptativo-celda-adjudicacion-v1_0.md`, los ocho defectos D1-D8 clasificados **material y correcto**, cero controversias, Ronda 2 no ejecutada) → esta versión |
> | **QUÉ CAMBIA DE v0.1** | Ocho correcciones de contrato (D1-D8, §3); tres correcciones factuales a la comparación de verticales (§5); lenguaje de M0 calibrado (recuadro de apertura). El diseño central —celda-D como unidad, champion/challenger/baseline, coordinación sobre infraestructura existente en vez de duplicarla— **no cambió**: sobrevivió Ronda 1 intacto |
> | **QUÉ NO DECIDE** | Igual que v0.1: ningún valor de ningún parámetro; la granularidad D de ningún eje; si el programa adopta el cómputo matricial de `propuesta-motor-matriz-v0_1.md` (M1, intacta); qué celdas concretas se ejecutan primero |

> ⚠️ **Sobre el material de referencia no encontrado (M0), redacción corregida tras Ronda 1.** v0.1 afirmaba "no hay evidencia de que la sustitución empobrezca el análisis" — Fable señaló, correctamente, que esa frase sobre-afirma: uno de los cinco archivos no encontrados (`BENCHMARKS-metodologicos-D-ABC.md`) versa por nombre sobre `D-ABC`, una decisión de mesa viva y pendiente (`milpa/procedencia.yaml:780-781`), y este programa ya tiene precedente de texto del espejo resultando imprescindible (`forense/hallazgos.md:131`). Redacción corregida: la sustitución **es suficiente para que Ronda 1 evalúe esta arquitectura** (verificado independientemente por IA2), pero **no es suficiente para sellar el menú de "modelos elegibles"** del commit 1 del piloto — eso espera a que mesa incorpore los cinco archivos o los declare irrecuperables (decisión humana **M0**, §8).

---

## 0 · La tesis, en cuatro eslabones

*(sin cambio respecto a v0.1 — el diseño central sobrevivió Ronda 1)*

1. **El estimando manda, no el estimador.** Fijar de antemano "todo se calibra por SMM" o "todo se lee de ENIGH" es el mismo error de categoría en dirección opuesta a fijar de antemano un valor.
2. **El estimando más el dato disponible acotan, no eligen, la familia de modelos elegibles.** La jerarquía de cinco rutas por fuerza de garantía (`forense/metodologia-identificacion-vs-ajuste-v0_1.md:114-130`) es la semilla de "modelos elegibles", no una invención de esta propuesta.
3. **La comparación entre lo elegible decide el estimador — nunca la sofisticación.** Sin baseline y criterio declarados *antes* del challenger, "elegimos el mejor modelo" es indistinguible de "elegimos el que nos gustó" — el defecto ANTI-POST-HOC que `forense/prompts-verticales-validacion.md:40` ya nombró para casos de negocio, aplicado aquí a estimadores.
4. **La salida hereda la forma que el estimador honesto produjo.** Forzar todo a un punto cuando el diseño solo sostiene una banda es el defecto que `propuesta-motor-matriz-v0_1.md:148` ya declaró para los 15 β.

El hueco que esta propuesta llena sigue verificado tras Ronda 1: **0 apariciones de "champion", "challenger" en sentido de selección, en toda la base** (confirmado independientemente por IA1 en v0.1 y por IA2 en Ronda 1). Esta propuesta no reemplaza `forense/censo-estimabilidad-coeficientes-v1_0.md`, `tools/curador_registro/` ni `production-spec.schema.json`: los coordina.

---

## 1 · Cuatro colisiones de vocabulario resueltas — sin cambio respecto a v0.1, con una quinta que Ronda 1 encontró y v0.1 no vio

### 1.1-1.4 · Celda, vertical/dominio, motor, baseline

Sin cambio — ver v0.1 §1.1-1.4. Resumen: esta propuesta usa **celda-D** (nunca "celda" sola, por colisión con celda-x y celda-B de `propuesta-motor-matriz-v0_1.md:35,65`); **dominio** para lo que el encargo llama "vertical sustantiva" (por colisión con las verticales V1-V4 de negocio, `forense/prompts-verticales-validacion.md:19`); **"el selector"** en prosa para no sumar una quinta lectura a "motor"; y declara la colisión de **baseline** con `tests/baseline.json` sin resolverla en prosa (solo en código futuro, como `baseline_celda`).

### 1.5 · La quinta colisión que Ronda 1 encontró — vocabulario de diseño/ruta (D3)

v0.1 introdujo un enum `diseno` (`panel | pseudo-panel | ajuste_momentos | transversal_seleccion | composicion | registro_administrativo`) sin notar que **ADR-49 D2 ya selló un campo `ruta:` con valores casi idénticos** (`pseudo_panel | momentos | composicion | transversal_con_seleccion`, `canon/gobernanza-v1_15.md:439`) — exactamente la quinta colisión de vocabulario que el propio documento, bajo su propio estándar de §1, debía resolver y no resolvió. Se corrige aquí: el contrato de §3 separa **`diseno_datos`** (qué es el dato en el mundo: panel, transversal, registro administrativo, experimento natural, auditoría de campo, enlace ecológico — ninguno de estos nombra una estrategia de estimación) de **`estrategia`** (cómo se estima a partir de ese dato: los cuatro valores **verbatim** de ADR-49 D2, extensible solo por el mismo ADR que los selló). Dos familias de diseño que v0.1 no representaba y que Ronda 1 nombró con evidencia real quedan de primera clase: **experimento natural/discontinuidad** (la llave (ii) de ADR-57(c), `gobernanza:623`; el RDD de R7.3, `forense/cruce-catalogo-fichas-v2_0.md:89`) y **enlace ecológico** (categoría propia del cruce v2.0, "diseño distinto, no versión peor", `cruce-catalogo-fichas-v2_0.md:32-33`) — más **"usuario simulado"**, ya nombrado en la tabla §5 de v0.1 y real en el corpus (`data/inventarios/inventario_fuentes_tramites_estado_mexico.md:466`).

---

## 2 · La celda-D — definición operacional, corregida (D1)

**celda-D = (estimando requerido por MILPA) × (población objetivo).** El dominio se deriva del estimando (no es un tercer eje independiente); **la fuente y el diseño NUNCA son parte de la clave** — viven exclusivamente como atributos de cada candidato dentro de `candidatos` (§3). Esta es la corrección del defecto D1: v0.1 definía la celda con la fuente dentro de la tupla identificadora y al mismo tiempo construía un contrato donde varios candidatos (cada uno con su propia fuente) conviven dentro de una sola celda — dos lecturas incompatibles del mismo objeto, visibles hasta en el id de su propio ejemplo trabajado. Bajo la clave corregida, el caso que v0.1 describía mal ("dos celdas-D nuevas" para ENSAFI/ENFIH) se lee así: **dos candidatos nuevos, cada uno instanciado en cada una de las hasta cuatro celdas-D que ya abren las filas 3, 4, 6 y 11 del censo de estimabilidad** (`forense/REVERIFICACION-DEMANDA-vs-UNIVERSO-2026-08-07-v1_0.md:48-56,74`) — no celdas nuevas por candidato, sino candidatos nuevos sobre celdas que ya existían por estimando.

La tabla de relación con infraestructura existente no cambia respecto a v0.1 §2 (censo-estimabilidad resuelve identificabilidad sin comparar estimadores; `tools/curador_registro/` implementa el registro demanda-universo sin noción de "gana frente a otro candidato que también satisface"; `production-spec.schema.json` es el contrato ciego de una ejecución, no de una comparación; `matriz-impacto-universal` no tiene ranura para "perdió frente a un candidato que sí satisface"). Esta propuesta sigue sin sustituir ninguna: coordina.

---

## 3 · El contrato de una celda-D — revisado, campo por campo (D1-D8)

```yaml
celda_d:
  id: <string>                        # estable; NUNCA contiene la fuente (D1)
  estimando: <string>                  # objeto de canon citado; sin cambio (production-spec.schema.json:11)
  tipo_adjudicacion: COMPARACION | FALSACION | CALIBRACION_CONJUNTA   # nuevo (D2)
  dominio: <FIN|MIG|TEC|CAP|CUL|SAL|SEG|TRA|EST|TIE>   # DERIVADO del estimando, no clave independiente
  poblacion_objetivo: <string>         # PARTE DE LA CLAVE junto con estimando (D1)
  unidad_objetivo: persona | hogar | establecimiento | agregado_geografico   # nuevo — el cruce v2.0
                                        #   ya distingue VIABLE ECOLÓGICO de VIABLE (cruce-v2_0:32-33);
                                        #   sin este campo el compilador no sabe si puede bajar a celda-x
  universo_candidatos: <qué se barrió, con qué mecanismo, en qué fecha>   # nuevo (D4) — misma
                                        #   disciplina A.4 que ya rige el resto del programa
                                        #   (instrucciones-proyecto-v2_6.md:238-245)
  candidatos:                          # >=1; el baseline cuenta como candidato; SIEMPRE aquí,
                                        #   jamás en la clave (D1)
    - rol: BASELINE | CHALLENGER
      fuentes: []                      # lista, no string — 1 elemento en el caso simple (D5)
      edicion_periodo: <string>        # ola/año del instrumento — dos olas son candidatos distintos
      diseno_datos: panel | pseudo_panel | transversal | registro_administrativo |
                    experimento_natural | auditoria_campo | enlace_ecologico    # corregido (D3)
      estrategia: pseudo_panel | momentos | composicion | transversal_con_seleccion   # verbatim
                    # ADR-49 D2 (gobernanza:439); extensible solo por el mismo ADR (D3)
      regla_composicion: <declarada en fecha_declaracion> | NO-APLICA   # obligatoria si len(fuentes)>1 (D5)
      production_spec_refs: []         # lista, no singular; NINGUNO-AUN admitido (D5)
      resultado: GANO | PERDIO:<margen> | NO-EJECUTADO | INEJECUTABLE   # nuevo, mejora no bloqueante
  criterio_adjudicacion: <string>      # renombrado de `criterio_victoria` (D2); si
                                        #   tipo_adjudicacion=FALSACION, HEREDA la escala B-bis
                                        #   de la ficha Hito D correspondiente — no se reinventa
  momentos_holdout_refs: []            # nuevo — los que NINGÚN candidato de esta celda puede tocar;
                                        #   sellados en el commit 1 del piloto, no después (D8)
  champion_actual: <rol.fuente o NINGUNO>   # "el baseline retiene" es resultado válido, no vacío
  output_nativo: {tipo: <7 tipos, ver v0.1 §3.6, sin cambio>, valor_ref: <archivo dueño>}
  incertidumbre: {tipo: <string>, ref: <string>}   # tipada (mejora no bloqueante), no string libre
  supuesto_transporte: EXISTE-SATISFACE | ACOTADO-CON-SUPUESTO:<cual> | NO-TRANSPORTABLE:<por que>
  fuerza: ASIGNADO | AJUSTADO | IDENTIFICADO   # corregido (D6) — nombres sellados
                                        #   (glosario-v5_6.md:356; ADR-49 D2; ADR-57(c))
  calibrado: <bool>                    # nuevo (D6) — marca de auditoría §4.1 motor-matriz sobre
                                        #   un AJUSTADO; NO es una cuarta clase de `fuerza`
  # "ACOTADO" ya no es un valor de este campo — se LEE de output_nativo.tipo (D6); "predicción"
  # no es un estado — es un modo de evaluación contra momentos_holdout_refs, aplicable a
  # cualquier `fuerza` salvo ASIGNADO puro
  estado_operativo: LISTO | LEGACY | PENDIENTE | EXCLUIDO
  requiere_decision_mesa: <bool>
  fecha_declaracion: <YYYY-MM-DD>       # anti-circularidad: antes de correr cualquier challenger
  commit_declaracion: <sha>            # nuevo, mejora no bloqueante — patrón de dos commits
  fecha_adjudicacion: <YYYY-MM-DD>      # nuevo, mejora no bloqueante
  commit_adjudicacion: <sha>           # nuevo, mejora no bloqueante
```

### 3.1 · Regla de agregación de `estado_operativo` — corregida (D7)

v0.1 mapeaba 9 de los 10 estados de `matriz-impacto-universal-2026-08-06.md:8-12`; **faltaba `MAPEADO-NO-SATISFACE`**, y la tabla confundía nivel-candidato (donde viven los 10 estados de la matriz, uno por relación fuente×necesidad) con nivel-celda (donde vive `estado_operativo`, uno por celda con potencialmente varios candidatos en estados distintos). Regla de agregación explícita, corregida:

- **`LISTO`** — existe un candidato `champion_actual` vigente, con `production_spec_refs` ejecutados y auditables.
- **`PENDIENTE`** — ningún champion vigente, pero existe ≥1 candidato en `NO-ENCONTRADO-EN-UNIVERSO-DECLARADO`, `INDEXADO-NO-DESCARGADO`, `DESCARGADO-NO-ABIERTO`, `ABIERTO-SIN-MAPEO` o `MECANISMO-NO-EJECUTADO` (trabajo pendiente, no agotado).
- **`EXCLUIDO`** — todos los candidatos están en `NO-ACCESIBLE` o **`MAPEADO-NO-SATISFACE`** (el estado que v0.1 omitió: examinado y descartado, no simplemente no mirado), o `supuesto_transporte` es `NO-TRANSPORTABLE`.
- **`LEGACY`** — el champion anterior está en `NO-REPRODUCIBLE-CON-ARTEFACTOS-ACTUALES` (pipeline perdido, no dato perdido).
- **`REQUIERE-DECISION-DE-MESA`** no es un quinto valor de `estado_operativo`: es la bandera `requiere_decision_mesa: true`, ortogonal a los cuatro — exactamente como opera de facto en `matriz-impacto-universal`.

### 3.2 · Etapa de coherencia conjunta — nueva, requisito de diseño del piloto (D8)

v0.1 declaraba la tensión entre selección independiente por celda y coherencia conjunta (su propio §4, sobre la relación con `propuesta-motor-matriz-v0_1.md`) sin darle mecanismo — exactamente el defecto que el propio README.md prohíbe ("un principio sin artefacto que falte visiblemente cuando no se cumple no obliga a nada"). Se corrige como **requisito del commit 1 del piloto, no como trabajo aplazable**: antes de declarar la primera celda-D, el piloto sella una lista corta de `momentos_holdout_refs` **globales** —ningún candidato de ninguna celda del piloto puede haberlos usado para ajustar— y una etapa de cierre, al final del piloto, que (i) evalúa el ensamble de champions contra esos momentos globales y (ii) corre un chequeo de signos tipo ADR-30 (`propuesta-motor-matriz-v0_1.md:65`: una configuración donde un parámetro mejore *todos* los desenlaces se rechaza). Una violación no aborta el piloto: obliga una fila de refutación registrada y decisión de mesa — mismo tratamiento que el resto del programa da a un veredicto adverso.

### 3.3-3.9 · Estimando/dominio, dato faltante vs. transporte inviable, modelos elegibles, baseline/challenger/champion, criterio de adjudicación, output nativo

Sin cambio sustantivo respecto a v0.1 §3.1-3.2, §3.3-3.6 — las correcciones de esta sección viven en el schema de arriba, no en la prosa que las explica. El ejemplo trabajado de R1.1/AGROASEMEX (v0.1 §6) se conserva íntegro, con dos ajustes de campo (`criterio_adjudicacion` con `tipo_adjudicacion: FALSACION` en vez de `criterio_victoria`; `fuerza: ASIGNADO` en vez de `estado_epistemologico: ASIGNADO`) — el contenido sustantivo del ejemplo no cambió, solo los nombres de campo que lo alojan.

---

## 4 · Relación con `propuesta-motor-matriz-v0_1.md` — sin cambio, con el mecanismo de D8 como puente

La tensión declarada en v0.1 §4 se mantiene íntegra: motor-matriz propone una forma computacional única aplicada uniformemente; esta propuesta parte de que ninguna forma única debe imponerse celda por celda. Lo que cambia es que ahora esa tensión **tiene un mecanismo de detección** (§3.2 de esta versión): si motor-matriz llega a implementarse como challenger de la familia `estrategia: momentos` en varias celdas, la etapa de coherencia conjunta es exactamente el lugar donde se vería si sus 15 β compilan de forma consistente con los champions de celdas que eligieron otra estrategia. No se resuelve la pregunta M1 aquí; se le da un lugar donde su respuesta, cuando llegue, sería verificable.

---

## 5 · Comparación de verticales piloto — corregida (tres hallazgos de Ronda 1)

| Criterio | Trámites / confianza institucional | Finanzas del hogar | Seguridad / violencia |
|---|---|---|---|
| Récord de falsación Hito D | Mejor de las tres: R3.1→B, R3.2→B, sin ningún D | Peor de las tres: R1.1→D (transporte), R1.2→E, R1.3→E | Intermedio: R7.2→D |
| Fuentes operables | ~5-6/23 | ~7/15 | ~7/12 |
| Variedad de diseños | Transversal, panel (ENSU), registro administrativo, usuario simulado | Transversal, registro administrativo (CNBV/CONSAR/Banxico), la única llave de identificación viva del programa (ENNViH/MxFLS, RUTA-I) — **la más variada de las tres** | Transversal, panel (ENSU), registro administrativo |
| Material fresco sin explotar | Moderado | Alto: ENSAFI/ENFIH tocan 4 de los 9 SIN-RUTA a la vez, más el puente de la fila 14 | **Agotado, no bajo** — el camino conocido (agrupar 8 olas ENVIPE) ya corrió y no alcanzó umbral (`hitoD-preregistro-v2_0.md:717-727`): resultado negativo ya obtenido, no trabajo pendiente |
| Conexión con MILPA | **Corregido — parcial, no total.** El gate `bt.oxxo_vs_codi` exige A∧B∧C; la propia ficha de R3.4 pre-registra B y C como inejecutables con fuente pública, dejando solo A (agregado) medible (`hitoD-preregistro-v2_0.md:841`; `cruce-catalogo-fichas-v2_0.md:67`) — un piloto de trámites conecta con un tercio operable del gate, no con el gate completo | Indirecta, vía coeficientes de G2-G5 | Indirecta, vía condicionales de G4 (ya `MEDIDO·PARCIAL`) |
| Riesgo propio declarado | **Corregido — ya cerrado, no abierto.** La circularidad de ENCIG en R3.1/R3.2 fue rastreada y resuelta: "no es circular medir el contraste ahí, porque el contraste nunca se extrajo de ahí" (`hitoD-preregistro-v2_0.md:417,750`) | Ninguna fuente cataloga fondos de aseguramiento agropecuario — hueco estructural propio, ya ilustrado por el ejemplo de §6 | — |

**Recomendación, reforzada tras Ronda 1: finanzas del hogar.** Las dos correcciones sobre trámites eliminan a la vez su argumento más fuerte (conexión con el gate — resulta parcial) y su riesgo más citado (circularidad — resulta ya resuelto), dejándolo como lo que en realidad es: el dominio con mejor récord de falsación, que es exactamente donde un selector nuevo tiene **menos** que demostrar. La corrección sobre seguridad retira su presentación como "reparación en curso" — el camino conocido ya se agotó con resultado negativo limpio, lo que lo hace un buen caso de estudio de "resultado negativo informativo" (§7) pero no el mejor piloto generativo. **Finanzas del hogar sigue siendo la única de las tres con material fresco genuinamente sin explotar y con la mayor variedad de diseños**, incluida la única llave de identificación viva del programa. Gate de semana 1 sin cambio: verificación byte a byte de que ENSAFI y ENFIH publican microdato utilizable; si ambos fallan, fallback nombrado a trámites, por decisión de mesa (no automático).

---

## 6 · Ejemplo trabajado — sin cambio sustantivo, campos renombrados

```yaml
celda_d:
  id: FIN.R1_1.aseguramiento_agricola
  estimando: "R1.1 (modelo §3.1) — horizonte de ahorro bajo volatilidad de ingreso"
  tipo_adjudicacion: FALSACION
  dominio: FIN
  poblacion_objetivo: "productores de temporal, volatilidad de ingreso máxima"
  unidad_objetivo: persona
  universo_candidatos: "Fondos de Aseguramiento agrícola (padrón AGROASEMEX + CSV abiertos), Seguro Agrícola Catastrófico, Fondo CNOG, seguros estatales, Producción para el Bienestar, adopción voluntaria ENA 2017 — barrido del 28/jul/2026, tabla de descartes completa en hitoD-R1_1-veredicto-v1_0.md §5"
  candidatos:
    - rol: CHALLENGER
      fuentes: ["Fondos de Aseguramiento agrícola (AGROASEMEX)"]
      diseno_datos: registro_administrativo
      estrategia: NO-APLICA   # es un ejercicio de falsación, no de ajuste/comparación
      regla_composicion: NO-APLICA
      production_spec_refs: []   # el veredicto D se declaró sin production-spec: el confusor
                                  #   pre-registrado bastó para resolver por completo
      resultado: "INEJECUTABLE"
  criterio_adjudicacion: "participación voluntaria sostenida >=3 ciclos, tasa >= ahorro formal de asalariados informales urbanos comparables (+-20%), EXCLUYENDO participación atada a crédito/programa — escala B-bis de la ficha Hito D, heredada, no reinventada"
  momentos_holdout_refs: []   # no aplica a un ejercicio de falsación aislado
  champion_actual: NINGUNO
  output_nativo: {tipo: "ninguno — veredicto D", valor_ref: "forense/hitoD-R1_1-veredicto-v1_0.md"}
  incertidumbre: {tipo: "no aplica", ref: "D no es una estimación con banda, es un dictamen de inejecutabilidad"}
  supuesto_transporte: "NO-TRANSPORTABLE: la cobertura del instrumento (62-66% en Sonora/Sinaloa/Tamaulipas, agricultura de riego) no alcanza a la población de volatilidad máxima que el estimando requiere, y el instrumento que sí la alcanza (Seguro Agrícola Catastrófico) es legalmente incontratable por el productor mismo"
  fuerza: ASIGNADO
  calibrado: false
  estado_operativo: EXCLUIDO
  requiere_decision_mesa: false
  fecha_declaracion: "2026-07-28"
```

---

## 7 · Lo que esta propuesta no resuelve

Sin cambio respecto a v0.1: no elige el estimador de ninguna celda-D real; no fija la granularidad D de ningún eje; no decide M1 ni resuelve del todo la tensión de §4 (ahora tiene mecanismo de detección, no resolución); no implementa `tools/curador_registro/`; no es canon.

## 8 · Preguntas para mesa — actualizada

- **M0** · ¿Se incorporan los cinco archivos del espejo o se declaran irrecuperables? Antes del commit 1 del piloto, no antes de aprobar esta arquitectura.
- **M7** · ¿Se confirma finanzas del hogar como vertical piloto (recomendación conjunta de IA1 y IA2 tras Ronda 1), con trámites como fallback nombrado?
- **M8** · ¿Se aplaza la región NROY (0 precedentes en el repo, recomendación conjunta de IA1 y IA2) hasta que un ejercicio de calibración conjunta la necesite?
- **M9** · ¿Se aceptan los umbrales de go/no-go propuestos en Ronda 1 (10-15 celdas, ≥3 con ambos brazos ejecutados, ≥2 tipos de output no-punto, ≥1 negativo informativo) o mesa fija otros?
- **M10** *(nueva)* · ¿El ADR de adopción del contrato de celda-D se sella junto con el catálogo de momentos de `propuesta-motor-matriz §3.3` si ese catálogo llega a sellarse, o corre en un commit propio, independiente de M1?

---

## 9 · Módulo de auditoría

**1-6** · No aplican, igual que v0.1.

**7 · ¿Qué conclusión sería peligrosa simplificada?** Las tres de v0.1, sin cambio, más una cuarta específica de esta versión: *"v0.2 ya corrigió todo, el contrato está terminado"* — v0.2 corrige los ocho defectos que Ronda 1 encontró en una sola pasada; no hay garantía de que sea la última pasada, y el propio criterio go/no-go (v0.1 §7, sin cambio) sigue siendo la prueba real, no esta corrección de escritorio.

**8 · ¿Qué fue derivado y cuál no?** Derivado o citado archivo:línea: los ocho defectos (releídos por IA1 contra su propio texto de v0.1, no solo contra la cita de Fable — ver `RONDA1-motor-adaptativo-celda-adjudicacion-v1_0.md §1`); las tres correcciones a §5 (verificadas de primera mano por IA1 contra `hitoD-preregistro-v2_0.md` y `cruce-catalogo-fichas-v2_0.md` — ver adjudicación §2). No derivadas directamente por IA1 en esta versión: las citas de apoyo de Fable a ADR-47 y al conteo "cuatro veces" de A.4 (ver adjudicación §7, módulo de auditoría) — no cambian la adjudicación porque los defectos que apoyan ya eran evidentes por evidencia primaria independiente.

**Contadores movidos por el trabajo que produjo esta versión: 0.**

**(v2.4) Cantidades y escalas:** sin cambio respecto a v0.1 — ninguna cantidad estimada nueva se transcribe en esta versión.
