# RONDA 1 · Motor adaptativo por celda · Adjudicación de IA1
### v1.0 · 11/ago/2026 · IA1 contra `RONDA1-motor-adaptativo-celda-veredicto-fable-2026-08-11-v1_0.md`

> | | |
> |---|---|
> | **CLASE** | Adjudicación. Aplica la tabla de clasificación del encargo (material y correcto / material pero discutible / no material / reapertura sin evidencia / sustitución por ecuación universal) a cada hallazgo de Ronda 1 |
> | **REGLA DE ADJUDICACIÓN** | *Material y correcto* → incorporar antes del piloto. *Material pero discutible* → prueba empírica pequeña o decisión humana. *No material* → registrar en una línea y continuar. *Reapertura sin evidencia nueva* → descartar. *Sustitución por ecuación universal* → fuera de encargo |
> | **VERIFICACIÓN** | Antes de clasificar, releí directamente (no delegué) cada uno de los ocho defectos contra el texto real de `propuesta-motor-adaptativo-celda-v0_1.md`, y verifiqué de primera mano las tres correcciones factuales de Fable a la tabla de verticales (`forense/hitoD-preregistro-v2_0.md:405-424,705-750,830-849`; `forense/cruce-catalogo-fichas-v2_0.md:60-74`) antes de aceptarlas |

---

## 1 · Los ocho defectos materiales (D1-D8)

**Los ocho son MATERIAL Y CORRECTO.** Verifiqué cada uno releyendo mi propio texto, no solo la cita de Fable:

| # | Verificación propia | Adjudicación |
|---|---|---|
| D1 | Confirmado: §2 define la celda-D con la fuente dentro de la tupla identificadora ("estimando × dominio × fuente…"); §3 la contradice al poner `candidatos` (multi-fuente) *dentro* de una sola celda; el id de mi propio ejemplo (`FIN.R1_1.aseguramiento_agricola`) sigue la primera lectura. Es una contradicción real, no una lectura uncharitable de Fable | **Incorporar.** Clave = `estimando × poblacion_objetivo`; fuente/diseño quedan exclusivamente dentro de `candidatos` |
| D2 | Confirmado: mi §3.5 define `criterio_victoria` como adjudicación challenger-vs-baseline; mi propio ejemplo de §6 lo reutiliza para un umbral de falsación Hito D sin baseline ni challenger. Usé el mismo campo para dos objetos de decisión distintos | **Incorporar.** Campo `tipo_adjudicacion: COMPARACION \| FALSACION \| CALIBRACION_CONJUNTA`; renombrar a `criterio_adjudicacion` |
| D3 | Confirmado, y es el más incómodo de aceptar porque mi propio §1 se jacta de resolver colisiones de vocabulario — y dejé pasar esta quinta. Mi primer agente de investigación (Ronda de research previa a esta propuesta) ya me había reportado el vocabulario `ruta:` de ADR-49 D2 casi textual a lo que reinventé en `diseno` | **Incorporar.** Separar `diseno_datos` (real-world) de `estrategia` (vocabulario verbatim de ADR-49 D2) |
| D4 | Confirmado por ausencia: repasé los 14 campos de mi contrato §3 y ninguno declara el universo de búsqueda de `candidatos`. Es exactamente la clase (a) que A.4 existe para prohibir, ahora un nivel más arriba | **Incorporar.** Campo `universo_candidatos` |
| D5 | Confirmado: `production_spec_ref` es singular en mi schema; las celdas que motivan el piloto recomendado (fila 14 del censo, el puente ENSAFI) necesitan más de uno | **Incorporar.** `production_spec_refs: []` + `regla_composicion` |
| D6 | Confirmado, y también incómodo: escribí explícitamente en la prosa de §3.7 que ACOTADO "es una propiedad de la forma… no un cuarto peldaño", y en el mismo documento lo dejé como enum excluyente de un solo valor. Noté la tensión mientras escribía y no la resolví en el schema | **Incorporar.** `fuerza` (3 valores) + `calibrado: bool`; la forma se lee de `output_nativo.tipo` |
| D7 | Confirmado por conteo directo: mi tabla §3.8 mapea 9 de los 10 estados de `matriz-impacto-universal`; `MAPEADO-NO-SATISFACE` falta | **Incorporar.** Añadir el estado; declarar regla de agregación explícita (candidato→celda, no solo estado→estado) |
| D8 | Confirmado: mi §4 *declara* la tensión con motor-matriz pero no le da ningún mecanismo — bajo la propia regla que cito de README.md ("un principio sin artefacto que falte visiblemente no obliga a nada"), mi §4 es exactamente ese defecto aplicado a mí mismo | **Incorporar como requisito de diseño del commit 1 del piloto**, no como trabajo aplazable |

No encontré ningún desacuerdo genuino con D1-D8: en los ocho casos, releer mi propio texto confirma el defecto sin necesidad de interpretar la evidencia de Fable de manera caritativa. Los ocho se incorporan en `propuesta-motor-adaptativo-celda-v0_2.md`.

## 2 · Las tres correcciones factuales a la tabla de verticales (§5)

Verifiqué las tres directamente contra los archivos primarios antes de adjudicar, no solo contra la palabra de Fable:

1. **Gate de Fase 1 sobredimensionado para trámites.** Leí `hitoD-preregistro-v2_0.md:837-841` y `cruce-catalogo-fichas-v2_0.md:63-67` de primera mano: la propia ficha de R3.4 pre-registra, antes de buscar nada, que las condiciones B y C del gate "degradan automáticamente… a inejecutables" con fuente pública, y el cruce v2.0 lo confirma como veredicto ("VIABLE ECOLÓGICO para A; NO ENLAZA para B/C"). **Material y correcto.**
2. **Circularidad de R3.2 ya resuelta, no abierta.** Leí `hitoD-preregistro-v2_0.md:413-417` y `:750` de primera mano: el texto dice, verbatim, "no es circular medir el contraste ahí, porque el contraste nunca se extrajo de ahí" — para R3.1 y R3.2 por igual. Mi tabla original citaba esto (vía uno de mis agentes de investigación) como riesgo abierto; era un riesgo ya cerrado. **Material y correcto.**
3. **Reparación de seguridad ya corrida, no en curso.** Leí `hitoD-preregistro-v2_0.md:717-727` de primera mano: la Nota 13 confirma que las ocho olas de ENVIPE ya se agruparon y ejecutaron, y que "ninguna vía cierra A sin reserva" — 43 casos caen en 42 conglomerados singleton sin varianza estimable, y donde sí es calculable el IC cruza el umbral. Es un resultado negativo ya obtenido, no un camino prometedor todavía por recorrer. **Material y correcto.**

**Efecto neto sobre la recomendación de vertical piloto: se refuerza, no se debilita.** Las dos correcciones sobre trámites eliminan simultáneamente su argumento más fuerte (conexión con el gate) y su riesgo más citado (circularidad) — quedando como lo que Fable describe con precisión: el dominio con mejor récord de falsación, que es exactamente donde un selector nuevo tiene menos que demostrar. Mantengo la recomendación de **finanzas del hogar** con más confianza que en v0.1, e incorporo las tres correcciones a la tabla en v0.2.

## 3 · M0 (material de referencia no encontrado)

**Material y correcto, como calibración de mi propia sobre-afirmación.** Escribí "no hay evidencia de que la sustitución empobrezca el análisis"; Fable señaló, con cita verificable (`milpa/procedencia.yaml:780-781`, `forense/hallazgos.md:131`), que uno de los cinco archivos faltantes (`BENCHMARKS-metodologicos-D-ABC.md`) es nombralmente sobre una decisión de mesa viva (`D-ABC`, la función de enlace) y que este programa ya tiene un precedente de texto del espejo resultando imprescindible. Mi frase no estaba mal fundada para el propósito de esta Ronda 1 (evaluar la arquitectura), pero sí para cualquier lectura más amplia. Adopto la disposición exacta de Fable: **no bloquea este veredicto; sí bloquea sellar el menú de "modelos elegibles" antes de resolver M0.** Se corrige la redacción en v0.2.

## 4 · Las diez mejoras no bloqueantes

Las diez son razonables y de bajo costo. Adopto ocho directamente en el contrato de v0.2 (1, 2, 5, 7, 8, 10, y las dos de D3/D6 que ya las subsumen). Registro las otras dos en una línea sin bloquear nada:
- **Mejora 3** (grafo fuente→celdas automatizado): útil, pero es una herramienta derivada del registro, no un campo del contrato — se construye *después* de que existan celdas reales que grafiquen, no antes. No material para el contrato en sí.
- **Mejora 9** (registrar las dos celdas LEGACY de trámites dentro del piloto de finanzas): buena idea de cobertura de prueba, pero mezclar un dominio ajeno dentro del piloto declarado diluye el criterio go/no-go del §7. Se registra como sugerencia para la mesa de diseño del piloto, no como cambio al contrato.

## 5 · ¿Ronda 2?

**No se ejecuta.** La regla del encargo es correr Ronda 2 solo si quedan entre una y tres controversias materiales. Tras esta adjudicación, **cero** quedan: los ocho defectos son correcciones de contrato que yo mismo verifiqué contra mi propio texto (no hay lado opuesto que defender), las tres correcciones factuales se verificaron de primera mano contra archivo primario y se confirmaron en los tres casos, y M0 se resolvió como calibración de lenguaje, no como desacuerdo. No hubo, en ningún punto de este veredicto, un juicio arquitectónico de Fable que yo sostenga distinto — Fable fortaleció el diseño, no lo contestó. Los umbrales numéricos del §7 de Fable (10-15 celdas, ≥3 con ambos brazos ejecutados, etc.) no son una controversia IA1-IA2: son una decisión de alcance/costo que el propio encargo reserva para mesa ("cuánto costo computacional y de adquisición de datos se tolera") — se listan como decisión humana en vez de adjudicarse aquí.

## 6 · Clasificación de conducta de Fable frente a las restricciones del encargo

Verificado explícitamente porque el encargo lo exige: Fable no propuso una ecuación universal (extendió el contrato de comparación); no reabrió ninguna decisión sellada sin evidencia nueva (ancló sus correcciones en ADR-49/57 ya sellados, reutilizándolos, no disputándolos); no exigió identificación causal universal (preservó ASIGNADO/AJUSTADO/ACOTADO explícitamente, §6 de su veredicto); no confundió complejidad con mejora (sus ocho defectos son simplificaciones/correcciones, no adiciones de sofisticación); no usó auditoría como sustituto de medición (D8 pide un chequeo estructural, no una nueva medición). Cero hallazgos de la clase "reapertura sin evidencia nueva" o "sustitución por ecuación universal" — no hay nada que descartar por esas dos vías.

## 7 · Lista final de decisiones humanas (IA1, tras adjudicar; máximo cinco)

1. **M0** — ¿Se incorporan al repo los cinco archivos del espejo citados por el encargo original, o se declaran irrecuperables? Debe resolverse antes de sellar el menú de "modelos elegibles" del commit 1 del piloto (no bloquea aprobar esta arquitectura).
2. **Adopción formal** — ¿Se abre un ADR para el contrato de celda-D con las correcciones D1-D8 ya incorporadas en v0.2, dejándolo listo para regir el piloto?
3. **Vertical piloto** — ¿Se confirma finanzas del hogar (recomendación conjunta de IA1 y IA2, reforzada tras las correcciones de §2) con trámites como fallback nombrado si ENSAFI/ENFIH fallan el gate de semana 1?
4. **Alcance y costo del piloto** — ¿Se aceptan los umbrales de Fable para el go/no-go (10-15 celdas, ≥3 con ambos brazos ejecutados, ≥2 tipos de output no-punto) o la mesa fija otros?
5. **NROY (M8)** — ¿Se aplaza la región NROY (0 precedentes en el repo) hasta que exista un ejercicio de calibración conjunta que la necesite, como recomiendan IA1 y IA2 por igual, o se habilita ya en el piloto?

## Módulo de auditoría

**7 · ¿Qué conclusión sería peligrosa simplificada?** *"Fable encontró ocho defectos, luego la arquitectura de v0.1 estaba mal concebida"* — los ocho son correcciones de contrato (campos, claves, enums), no objeciones al diseño central (celda-D como unidad, champion/challenger/baseline como mecánica, coordinación en vez de duplicación de infraestructura existente); ese diseño central sobrevivió intacto. *"Cero controversias significa que la revisión fue superficial"* — al contrario: los ocho defectos son específicos, citados y verificados de primera mano por ambas partes; la ausencia de controversia es porque las correcciones eran objetivamente correctas, no porque Fable haya sido indulgente.

**8 · ¿Qué fue derivado y qué no?** Derivado o verificado de primera mano por IA1 en este acto: los ocho defectos releídos contra el texto propio; las tres correcciones factuales, cada una contra su archivo primario citado. **No verificado de primera mano por IA1**: la cita de Fable a `canon/gobernanza-v1_15.md` §0.1 sobre ADR-47 ("falsar ≠ calibrar", D2) y la cita a `instrucciones-proyecto-v2_6.md:236` sobre los "cuatro" casos previos de A.4 violado (D4) — ambas son citas de apoyo a defectos que ya eran evidentes por evidencia primaria independiente, por lo que su falta de verificación directa no cambia la adjudicación.

**Contadores movidos por este acto: 0.**
