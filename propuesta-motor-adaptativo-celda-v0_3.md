# El motor adaptativo por celda: seleccionar el estimador, no imponerlo
### Propuesta sin sello · v0.3 · 11/ago/2026

> | | |
> |---|---|
> | **ARCHIVO** | `propuesta-motor-adaptativo-celda-v0_3.md` |
> | **REEMPLAZA A** | `propuesta-motor-adaptativo-celda-v0_2.md` — se conserva, no se borra. v0.1 y v0.2 son historia de las Rondas 1 de esta propuesta; no se editan |
> | **CLASE** | Propuesta. **No es decisión.** No rige hasta ADR-68 (§8, R2) |
> | **ORIGEN** | ENCARGO AJUSTE v0.3 (sesión `claude/motor-adaptativo-celda-wk91nl`, base `bda44ea`): incorpora las cinco respuestas de mesa sobre la adjudicación de Ronda 1, más tres adiciones (H1, H2, H6) de una revisión de dirección externa hecha contra `ddacc2e`/`bda44ea` desde una sesión con acceso al espejo del proyecto que esta sesión no alcanza |
> | **QUÉ CAMBIA DE v0.2** | Las cinco preguntas de mesa quedan resueltas (§8); tres campos/mecanismos nuevos que Ronda 1 no vio (H1 escala/universo de instrumento, H2 rol `COMPLEMENTO`, H6 interfaz declarada con la propuesta hermana); tres celdas-D semilla registradas (§4-bis); gate de semana 1 del piloto re-especificado (§5). El diseño central —celda-D, champion/challenger/baseline, coordinación sobre infraestructura existente— **no cambia por tercera vez**: sigue siendo el de v0.1, corregido en v0.2, ahora completado |
> | **QUÉ NO DECIDE** | Sin cambio: ningún valor de ningún parámetro; la granularidad D de ningún eje; **M1 sigue abierta** — la matriz de `propuesta-motor-matriz-v0_1.md` como definición del ejecutable no se decide aquí, ni con H6 (ver §4) |

> ⚠️ **M0 — RESUELTO-RECUPERADO, 11/ago/2026.** Los cinco archivos que el encargo original citaba y que Ronda 1 clasificó NO-ENCONTRADO (recuadro de apertura de v0.1/v0.2) **existían en el espejo del proyecto y fueron recuperados por decisión de mesa** (R1, §8). Entran verbatim, con banner de recuperación propio y sha256 verificado contra `MANIFEST-recuperacion-espejo.sha256` (verificación propia, byte a byte, en el acto que produjo esta versión — coincide exacto en los cinco archivos): `forense/BENCHMARKS-metodologicos-D-ABC.md`, `forense/CAREO-benchmarks-4RT-archivo-proyecto.md`, `forense/EDGE-CASES-y-literatura-reciente.md`, `forense/auditoria_adversarial_benchmarks.md`, `forense/red-team-auditoria-benchmarks.md`. Su contenido es tipo (2)/(3) — no se promueve por el solo hecho de entrar al repo — y su lectura completa **no es parte de este acto**: queda para quien selle el menú de "modelos elegibles" citado en la disposición de Fable (Ronda 1, adoptada tal cual por mesa).

---

## 0 · La tesis, en cuatro eslabones — sin cambio, sobrevivió dos Rondas

1. **El estimando manda, no el estimador.**
2. **El estimando más el dato disponible acotan, no eligen, la familia de modelos elegibles.**
3. **La comparación entre lo elegible decide el estimador — nunca la sofisticación.**
4. **La salida hereda la forma que el estimador honesto produjo.**

*(Argumentación completa: v0.1 §0, sin cambio.)* El hueco que llena —0 apariciones de "champion"/"challenger" en sentido de selección, verificado independientemente por IA1 y por Fable— sigue verificado. No sustituye `forense/censo-estimabilidad-coeficientes-v1_0.md`, `tools/curador_registro/`, `production-spec.schema.json` ni `forense/matriz-impacto-universal-2026-08-06.md`: los coordina.

## 1 · Cinco colisiones de vocabulario resueltas — sin cambio respecto a v0.2

celda-D (vs. celda-x/celda-B de la propuesta hermana) · dominio (vs. vertical V1-V4 de negocio) · "el selector" (vs. las otras tres lecturas de "motor") · `baseline_celda` declarado, no resuelto en código (vs. `tests/baseline.json`) · `diseno_datos`/`estrategia` separados (vs. el `ruta:` de ADR-49 D2). Detalle completo: v0.2 §1.

## 2 · La celda-D — sin cambio respecto a v0.2

**celda-D = (estimando) × (población objetivo).** Dominio derivado; fuente y diseño nunca en la clave, solo en `candidatos`. Detalle completo, incluida la corrección de identidad D1: v0.2 §2.

---

## 3 · El contrato de una celda-D — con las dos adiciones de la revisión de dirección (H1, H2)

```yaml
celda_d:
  id: <string>
  estimando: <string>
  tipo_adjudicacion: COMPARACION | FALSACION | CALIBRACION_CONJUNTA
  dominio: <FIN|MIG|TEC|CAP|CUL|SAL|SEG|TRA|EST|TIE>
  poblacion_objetivo: <string>
  unidad_objetivo: persona | hogar | establecimiento | agregado_geografico
  universo_candidatos: <qué se barrió, con qué mecanismo, en qué fecha>
  candidatos:
    - rol: BASELINE | CHALLENGER | COMPLEMENTO          # +COMPLEMENTO, nuevo (H2)
      fuentes: []
      edicion_periodo: <string>
      universo_instrumento: <poblacion y periodo que el instrumento cubre — nuevo (H1);
                              # NO es universo_candidatos (qué se barrió al buscar candidatos):
                              # es qué mide, de quién, cuándo, ESTE instrumento en particular
      diseno_datos: panel | pseudo_panel | transversal | registro_administrativo |
                    experimento_natural | auditoria_campo | enlace_ecologico
      estrategia: pseudo_panel | momentos | composicion | transversal_con_seleccion
      regla_composicion: <declarada en fecha_declaracion> | NO-APLICA
      production_spec_refs: []
      resultado: GANO | PERDIO:<margen> | NO-EJECUTADO | INEJECUTABLE | NO-APLICA   # NO-APLICA
                    # para candidatos con rol COMPLEMENTO — no compiten, no ganan ni pierden
  criterio_adjudicacion: {texto: <string>, escala: <string>}   # `escala` nuevo (H1) — la escala
                    # en la que el criterio se evalúa; obligatoria cuando hay >=2 candidatos
                    # BASELINE/CHALLENGER en escalas de instrumento distintas (A-bis reglas 3-4)
  momentos_holdout_refs: []
  champion_actual: <rol.fuente o NINGUNO>
  output_nativo: {tipo: <7 tipos, v0.1 §3.6>, escala: <string>, valor_ref: <archivo dueño>}   # `escala`
                    # nueva (H1) — obligatoria; sin ella dos salidas AJUSTADAS en escalas distintas
                    # se compilarían como si fueran la misma cantidad
  incertidumbre: {tipo: <string>, ref: <string>}
  supuesto_transporte: EXISTE-SATISFACE | ACOTADO-CON-SUPUESTO:<cual> | NO-TRANSPORTABLE:<por que>
  fuerza: ASIGNADO | AJUSTADO | IDENTIFICADO
  calibrado: <bool>
  estado_operativo: LISTO | LEGACY | PENDIENTE | EXCLUIDO
  requiere_decision_mesa: <bool>
  fecha_declaracion: <YYYY-MM-DD>
  commit_declaracion: <sha>
  fecha_adjudicacion: <YYYY-MM-DD>
  commit_adjudicacion: <sha>
  relacion_complemento: <id de la celda-D ligada> | NO-APLICA   # nuevo (H2), ver 3.1
```

### 3.1 · `rol: COMPLEMENTO` — un candidato que no compite (H1/H2, nuevo)

Regla de granularidad, para que "candidato" no absorba constructos distintos bajo el mismo estimando por conveniencia: **todos los candidatos de rol `BASELINE`/`CHALLENGER` dentro de una misma celda-D deben apuntar al mismo estimando, en escala comparable** (declarada vía `criterio_adjudicacion.escala`, H1). Cuando dos fuentes miden constructos **relacionados pero distintos** — no el mismo estimando en dos escalas, sino dos estimandos distintos que se informan entre sí — **no van en la misma celda como BASELINE/CHALLENGER**: cada una abre o alimenta su propia celda-D, y la relación entre ambas se declara como un objeto de relación con su propio momento (`relacion_complemento`), nunca como candidato de rol `COMPLEMENTO` compitiendo por champion en la celda del otro. El rol `COMPLEMENTO` existe para el caso más simple —una fuente adicional que aporta contexto a una celda ya definida sin aspirar a ganarla— y **nunca sustituye la apertura de una celda propia** cuando el constructo es distinto. Caso vivo, decidido por mesa el 10/ago (§4-bis): `familismo_obligacion` — ENASIC (actitud) y ENUT (conducta) son celdas-D **distintas**, ligadas por una brecha declarable como momento, no una celda con un candidato `COMPLEMENTO` dentro de la otra.

### 3.2-3.9 · Resto del contrato — sin cambio respecto a v0.2

Identidad (D1), tipo de adjudicación (D2), diseño/estrategia (D3), universo de candidatos (D4), multi-fuente (D5), fuerza/calibrado (D6), rollup operativo (D7): sin cambio, ver v0.2 §3 y §3.1. Dato faltante vs. transporte inviable, modelos elegibles, baseline/challenger/champion, output nativo: sin cambio, ver v0.1 §3.2-§3.6.

---

## 4 · Relación con `propuesta-motor-matriz-v0_1.md` — de tensión declarada a interfaz declarada (H6, nuevo)

v0.1 y v0.2 declaraban la tensión sin resolverla. Mesa (R2, §8) confirma que **M1 sigue abierta** — este documento no decide si el cómputo matricial es la forma del ejecutable. Lo que sí se declara ahora, con más precisión, es **dónde** compiten y dónde no:

- **El selector (esta propuesta) gobierna la estimación**: qué fuente, diseño y estrategia produce cada insumo (cada Θ, cada momento de desenlace) y quién gana esa comparación.
- **La matriz (`propuesta-motor-matriz-v0_1.md`) gobierna la composición**: cómo MILPA consume esos insumos ya producidos para simular momentos agregados (`m = Σ π(x)·h_r(B·θ(x), C(x))`).
- **La frontera entre ambas es el catálogo de momentos** (`propuesta-motor-matriz-v0_1.md §3.1`): el selector lo puebla, celda por celda; la matriz lo consume.
- **Compiten en exactamente un territorio, no en todo**: los 15 β. Ahí, si motor-matriz llega a implementarse, entra al selector **como un challenger más de `estrategia: momentos`** (vocabulario ADR-49 D2, conforme a D3 de v0.2) — no como el menú entero ni como sustituto del contrato. Gana o pierde esa celda por el mismo `criterio_adjudicacion` que cualquier otro challenger, no por adopción arquitectónica previa.
- **El mecanismo que verifica que los champions resultantes sean conjuntamente coherentes es D8** (v0.2 §3.2, la etapa de cierre con `momentos_holdout_refs` globales y el chequeo de signos tipo ADR-30): es el lugar donde, si motor-matriz gana varias celdas, se vería si sus β compilan de forma consistente con los champions que eligieron otra estrategia. D8 es la maquinaria de esta interfaz; no es una etapa nueva, es la misma que Ronda 1 ya exigió, ahora nombrada como tal.

---

## 4-bis · Celdas-D semilla, decididas por mesa el 10/ago — registro, no ejecución

Tres celdas se registran para probar que el contrato representa sus tres `tipo_adjudicacion` con casos reales del programa. **Ninguna corre en este acto.** Citas de clase (`MEDIDO·PARCIAL(x)`, `PROXY_PARCIAL`) que dependen de ADR-67 se marcan como decisión de mesa del 10/ago, sellado en curso (`grep -c "ADR-67" canon/gobernanza-v1_15.md` = 0 al derivar esta versión) — no como cita de gobernanza sellada.

```yaml
celda_d:
  id: G5.radio_confianza.encuci_vs_enbiare
  estimando: "G5·radio_confianza (milpa/procedencia.yaml, coeficiente de generador)"
  tipo_adjudicacion: COMPARACION
  candidatos:
    - {rol: BASELINE, fuentes: [ENCUCI], edicion_periodo: "2020", diseno_datos: transversal,
       resultado: "vigente — MEDIDO·PARCIAL(x), modelo:253"}   # ítems AP5_1_1/2/3
    - {rol: CHALLENGER, fuentes: [ENBIARE], edicion_periodo: "por confirmar", diseno_datos: transversal,
       resultado: NO-EJECUTADO}   # ítems PB1_01/02, clase PROXY_PARCIAL — decisión de mesa
                                    # 10/ago, sellado en curso (ADR-67)
  criterio_adjudicacion: {texto: "acto de vinculación con prueba de invarianza (ítems ancla),
                           declarado antes de cualquier resultado del challenger", escala: "por declarar en el acto de vinculación"}
  requiere_decision_mesa: false
  fecha_declaracion: "2026-08-10"
---
celda_d:
  id: G5.familismo_obligacion.actitud
  estimando: "G5·familismo_obligacion (componente actitudinal)"
  tipo_adjudicacion: CALIBRACION_CONJUNTA   # provisional — no se ejecuta en este acto
  candidatos:
    - {rol: BASELINE, fuentes: [ENASIC], diseno_datos: transversal, resultado: NO-EJECUTADO}
  relacion_complemento: G5.familismo_obligacion.conducta
  requiere_decision_mesa: true   # reserva de encuadre declarada por mesa, sin resolver aquí
  fecha_declaracion: "2026-08-10"
---
celda_d:
  id: G5.familismo_obligacion.conducta
  estimando: "G5·familismo_obligacion (componente conductual/m-lado)"
  tipo_adjudicacion: CALIBRACION_CONJUNTA   # provisional — no se ejecuta en este acto
  candidatos:
    - {rol: BASELINE, fuentes: [ENUT], diseno_datos: transversal, resultado: NO-EJECUTADO}
  relacion_complemento: G5.familismo_obligacion.actitud
  requiere_decision_mesa: true
  fecha_declaracion: "2026-08-10"
---
celda_d:
  id: R5_1.D2.diseno_por_regla
  estimando: "R5.1 (modelo, apoyo familiar vs. Estado 65+) — diseño D2 del pre-registro por regla"
  tipo_adjudicacion: FALSACION
  candidatos:
    - {rol: BASELINE, fuentes: [ENASEM], diseno_datos: panel, resultado: NO-EJECUTADO}
  criterio_adjudicacion: {texto: "escala B-bis heredada del pre-registro sellado, renglón propio — no se reinventa",
                           escala: "ver forense/r5-1-diseno-por-regla-preregistro-v1_0.md"}
  requiere_decision_mesa: false   # el §8 de ese pre-registro sigue gateando T1-A; no gatea este registro
  fecha_declaracion: "2026-08-04"
```

Las tres son registro puro: prueban que `COMPARACION`, `CALIBRACION_CONJUNTA` (vía dos celdas ligadas por `relacion_complemento`, no por un candidato `COMPLEMENTO` dentro de una sola) y `FALSACION` conviven en el mismo contrato sin colisión de campos.

---

## 5 · Vertical piloto — FINANZAS DEL HOGAR confirmado (R3); gate de semana 1 re-especificado

Recomendación conjunta de IA1 y Fable (v0.2 §5) **confirmada por mesa**, con trámites como fallback nombrado — no automático.

**Corrección de estado que ninguna de las dos IAs tenía a la vista, verificada en este acto (PASO 0):** ENSAFI y ENFIH están adquiridas en disco — el registro del curador (`data/curacion-registro/relaciones.tsv`) muestra 6 filas de cada fuente en `capa2_manifiesto=SI, capa3_disco_real=EXISTE;COINCIDE;INTEGRO` (12 filas, exacto a lo esperado). El "formato no verificado" que citaba `data/inventarios/inventario-fuentes-credito-ahorro-finanzas-hogar-mexico.md:145,197` es ficha anterior a ese barrido.

**Precisión que este acto añade, y que no cambia la decisión de mesa pero sí cómo se lee el gate:** las 12 filas con integridad de disco confirmada están **todas clasificadas `NEGATIVA`** — relaciones (necesidad × fuente) ya evaluadas y descartadas para su necesidad específica. Las filas todavía **`CANDIDATA`** (20 de las 40 filas totales de ENSAFI/ENFIH, sobre las necesidades N3-N20) están en `capa2=SI_O_REFERENCIADO, capa3=SI_O_PARCIAL` — referenciadas o parcialmente confirmadas, no con integridad de disco cerrada como las NEGATIVA. Esto **no contradice** que "ENSAFI/ENFIH están adquiridas": el archivo existe y una porción ya se abrió y verificó byte a byte (de ahí las 12 NEGATIVA). Sí precisa qué significa el gate para las celdas que de verdad importan al piloto — las `CANDIDATA` vivas, no las ya resueltas.

**Gate de semana 1, re-especificado conforme a R3:** no es "conseguir o verificar que ENSAFI/ENFIH publican microdato" (ya está resuelto que sí, para la porción NEGATIVA) — es **apertura a nivel variable de las relaciones `CANDIDATA` vigentes**: diccionarios abiertos byte a byte, veredicto A.4 (`EXISTE-SATISFACE` / `EXISTE-NO-SATISFACE` / `NO-ENCONTRADO` / `NO-ACCESIBLE`) por cada una de las celdas-D objetivo que el piloto abra sobre esas 20 relaciones `CANDIDATA`. **"Fallar el gate" = las celdas objetivo devuelven `NO-ENCONTRADO` o `EXISTE-NO-SATISFACE`, con universo y términos declarados** — nunca una impresión narrativa de "no funcionó". El fallback a trámites es decisión de mesa sobre ese reporte cuando llegue, no automático.

*(Tabla comparativa completa de las tres verticales, con las tres correcciones factuales de Ronda 1: sin cambio, ver v0.2 §5.)*

---

## 6 · Ejemplo trabajado — sin cambio respecto a v0.2

R1.1/AGROASEMEX, íntegro. Ver v0.2 §6. Con H1 aplicado retroactivamente como ilustración, no como reapertura: `output_nativo.escala = "no aplica — D no produce escala, es un dictamen de inejecutabilidad"`.

---

## 7 · Lo que esta propuesta no resuelve

Sin cambio respecto a v0.2: no elige el estimador de ninguna celda-D real (las cuatro de §4-bis se registran, no se ejecutan); no fija la granularidad D de ningún eje; **no decide M1** (§4 la deja como interfaz declarada, no como pregunta cerrada); no implementa `tools/curador_registro/`; no es canon hasta ADR-68.

## 8 · Preguntas para mesa — resueltas, 11/ago/2026

| # | Pregunta (v0.2) | Resolución de mesa | Dónde queda incorporada |
|---|---|---|---|
| **M0** | ¿Se incorporan los cinco archivos del espejo? | **SÍ, incorporados.** Verificados sha256, en `forense/`, contenido intocable | Recuadro de apertura |
| **M7** | ¿Se confirma finanzas del hogar como piloto? | **SÍ**, trámites como fallback nombrado, no automático | §5 |
| **M8** | ¿Se aplaza NROY? | **SÍ, aplazada.** Condición de entrada: la primera corrida `AJUSTADO` de un catálogo de momentos pre-registrado (coincide con ambas IAs) | Sin cambio respecto a v0.2 §8; se retira de la lista de preguntas abiertas |
| **M9** | ¿Se aceptan los umbrales go/no-go de Fable? | **SÍ, los siete, con dos ajustes**: (a) empate declarado = empate, no se adjudica — 0 victorias de challenger o 0 retenciones de baseline es NO-GO informativo, no un fallo a maquillar; (b) el dry-run de compilación corre sin escribir en `milpa/`, artefacto en `forense/notas/`. Cada umbral se evalúa con conteos derivados por comando, nunca narrados | v0.2 §7 (criterio go/no-go), heredado de Ronda 1, con estos dos ajustes |
| **M10** | ¿El ADR corre junto al catálogo de momentos de motor-matriz o por separado? | **Por separado y en orden.** ADR-67 (otro perímetro, en curso en paralelo) primero o en paralelo; ADR-68 (este contrato) se sella en acto posterior a este, con los cinco recuperados ya en el árbol. ADR-68 NO adopta M1 y no ejecuta ninguna celda | Banner de apertura, `QUÉ NO DECIDE` |

Ninguna pregunta queda abierta en v0.3. Preguntas nuevas que surjan de ejecutar el piloto o de sellar ADR-68 abren su propia numeración, no reutilizan M1-M10.

---

## 9 · Módulo de auditoría

**1-6** · No aplican, igual que v0.1/v0.2.

**7 · ¿Qué conclusión sería peligrosa simplificada?** Las de v0.2, sin cambio, más una quinta: *"con las cinco respuestas de mesa, el contrato ya es definitivo"* — v0.3 resuelve lo que Ronda 1 dejó abierto y añade lo que una revisión externa vio y Ronda 1 no pudo (H1, H2, H6), pero **sigue sin sello**: rige hasta ADR-68, y ADR-68 todavía no corrió. Y una sexta, específica de §5: *"ENSAFI/ENFIH están confirmadas, luego el piloto ya tiene lo que necesita"* — están confirmadas las relaciones ya `NEGATIVA`; las `CANDIDATA` que el piloto necesita siguen en `SI_O_PARCIAL`, por abrir en el gate de semana 1, no antes.

**8 · ¿Qué fue derivado y qué no?** Derivado o verificado de primera mano en este acto: los cinco sha256 (coinciden exacto); `git log -1`, `origin/main`, `origin/claude/motor-adaptativo-celda-wk91nl` (sin divergencia); `grep -c "ADR-67"` = 0; el desglose completo de las 40 filas ENSAFI/ENFIH de `relaciones.tsv` (12 NEGATIVA con integridad de disco, 20 CANDIDATA sin ella, 8 más NEGATIVA sin integridad — ver conteo: 6+14=20 por fuente, ×2 fuentes=40). **No derivado por esta sesión, incorporado tal cual por instrucción explícita del encargo** ("las cinco respuestas de mesa... este acto las incorpora, no las discute"): las cinco resoluciones R1-R5 y las tres adiciones H1/H2/H6 de la revisión de dirección externa — esta sesión no tiene acceso al espejo que esa revisión sí tuvo, y no verificó sus afirmaciones contra él.

**Contadores movidos por el trabajo que produjo esta versión: 0** (dicho explícito, como pide TAREA 3 del encargo). Ninguna celda-D de §4-bis se ejecutó.

**(v2.4) Cantidades y escalas:** ninguna cantidad estimada nueva se transcribe en esta versión; los conteos de `relaciones.tsv` citados en §5 y en el módulo de auditoría son conteos de filas de un TSV ya en disco, re-derivables con los comandos de PASO 0 del encargo de ajuste que produjo esta versión (instrucción de sesión, no archivo del repo), no estimaciones.

---

## Changelog

**v0.2 → v0.3 · 11/ago/2026 (ENCARGO AJUSTE v0.3).**
1. M0 resuelto: cinco archivos recuperados a `forense/`, sha256 verificado.
2. §3: `rol: COMPLEMENTO` (H2) y campos `universo_instrumento`, `criterio_adjudicacion.escala`, `output_nativo.escala` (H1).
3. §4 reescrita: de "tensión declarada" a "interfaz declarada" (H6) — selector=estimación, matriz=composición, frontera=catálogo de momentos, único territorio de competencia=los 15 β.
4. §4-bis nueva: tres celdas-D semilla registradas (`radio_confianza` COMPARACION, `familismo_obligacion` CALIBRACION_CONJUNTA×2 ligadas por `relacion_complemento`, `R5.1-D2` FALSACION).
5. §5: gate de semana 1 re-especificado conforme a R3, con la precisión NEGATIVA-vs-CANDIDATA de `relaciones.tsv` verificada en este acto.
6. §8: las diez preguntas de mesa (M0/M7/M8/M9/M10 de v0.2, más las heredadas) quedan todas resueltas con fecha.

**v0.1 → v0.2 · 11/ago/2026 (Ronda 1):** ver changelog de v0.2.
