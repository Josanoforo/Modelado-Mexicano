# ASTRA-6 · Primera tanda ejecutable · 26/sep/2026

**Aprobación de mesa:** Jonás, «Acordado», 26/sep/2026 12:07:56 America/Mexico_City, sobre MISION-ASTRA-6 y ADENDA-1. **Preparación:** Astra. **Estado de esta entrega:** seis encargos preparados; ninguna sesión CLI lanzada desde este chat, ningún PR creado y ninguna corrida ejecutada por esta entrega.

Base GitHub consultada: `34949751113358869be981e2220f25d97e8097bd`. El repo puede avanzar: cada sesión verifica el estado material y fija su propio corte antes de trabajar. La consulta de abiertos al preparar mostró #1162 (ENSU), sin incorporarlo a main.

## Cómo lanzar

Extrae el ZIP. Abre seis sesiones Codex independientes en tu entorno habitual y adjunta **un archivo de encargo por sesión**, según la tabla. Cada archivo contiene misión, adenda, firma y autonomía con sus hashes; no necesitas adjuntar la conversación ni los documentos de base por separado. Mensaje de lanzamiento: **«Ejecuta el encargo adjunto completo con sus adendas y firma de mesa, verifica main, trabaja en tu worktree, entrega PR y recibo para Claude; no fusiones».**

| Archivo | Sesión y entorno | Entrega |
|---|---|---|
| `01-2026-09-26-ASTRA6-C1-PAQUETES-1.md` | ASTRA6-C1-PAQUETES-1 · CAJA | universo adoptado y paquetes listos para validadores nuevos |
| `02-2026-09-26-ASTRA6-C2-ENIF-1.md` | ASTRA6-C2-ENIF-1 · CAJA | dos familias ENIF con emisiones congeladas y prueba futura preparada |
| `03-2026-09-26-ASTRA6-C2-ENCIG-1.md` | ASTRA6-C2-ENCIG-1 · CAJA | dos familias ENCIG con emisiones congeladas y prueba futura preparada |
| `04-2026-09-26-ASTRA6-C2-ENVIPE-1.md` | ASTRA6-C2-ENVIPE-1 · CAJA | dos familias ENVIPE con emisiones congeladas y prueba futura preparada |
| `05-2026-09-26-ASTRA6-C3-SOCIAL-1.md` | ASTRA6-C3-SOCIAL-1 · NUBE o CLI sin microdato, con web | reports v2 completos de confianza, capital social y religiosidad |
| `06-2026-09-26-ASTRA6-C3-CONSUMO-FAMILIA-1.md` | ASTRA6-C3-CONSUMO-FAMILIA-1 · NUBE o CLI sin microdato, con web | reports v2 completos de consumo y familia |

**Las seis pueden empezar en paralelo.** Los recálculos ciegos de C1 todavía no: 01 debe entregar primero los paquetes separados y sus lanzamientos. La sesión 01 es preparadora y tiene acceso a contexto conocido. Las sesiones de recálculo serán NUEVAS y recibirán únicamente su paquete aislado; no estos seis encargos, este índice, la conversación ni el clon completo. No llamar «ciego» a un recálculo que no cumpla esa separación.

C2: los tres instrumentos agrupan dos familias cada uno para coordinar una apertura futura por instrumento. Todas se preparan sin abrir R futura; calendarios y atestación se declaran por su estado real. La recomendación inicial es cero retadores externos.

C3: 05 entrega tres reports; 06 entrega dos. Es la primera entrega de cinco de los 31, no una reducción del objetivo. No esperan a C1; indican validación pendiente y ajustan hallazgos materiales cuando lleguen.

## Secuencia que queda comprometida

1. **C1:** recibir 01, lanzar cada paquete aislado en sesión nueva, congelar reconstrucciones, revelar comparación y llevar discrepancias materiales a recibo/mesa. Completar el universo del corte; no cerrar con una muestra.
2. **C2:** recibir los tres lotes, integrar hojas locales y hashes para atestación; preparar el lote de hasta cuatro propuestas adicionales ENSU/ENOE/ENSANUT/MOCIBA solo con evidencia consolidada suficiente. Esa evaluación posterior no bloquea las seis familias actuales. No etiquetar aún como atestiguado lo que solo tiene hash interno.
3. **C3:** tras estos cinco reports, seguir por lotes delimitados hasta los 31; integrar índice final y reglas propuestas con los recibos. Abajo queda el inventario exacto de los 26 reports restantes en este corte. Ninguna fila está cancelada ni sustituida por este primer lote.

## Reports posteriores · rutas originales

- `corpus/reports/Adopción_y_Resistencia_Tecnológica_en_México__La_Paradoja_de_la_Baja_Confianza_Institucional.md`
- `corpus/reports/Ausencia_sin_certeza__duelo_y_pérdida_ambigua_en_familias_de_personas_desaparecidas_en_México.md`
- `corpus/reports/Autoridad_y_jerarquía_en_el_México_contemporáneo__anatomía_psicológica_de_un_sistema_dual.md`
- `corpus/reports/Behavioral_Finance_Mexicano__Estructura__Adaptación_Racional_y_Cultura_en_el_Ahorro__Crédito_y_Riesgo.md`
- `corpus/reports/El_Clasemediero_Mexicano__Identidad__Ansiedad_de_Estatus_y_el_Miedo_Racional_a_Caer.md`
- `corpus/reports/El_Efecto_Ambiental_de_la_Violencia_Crónica_en_México__Cómo_el_Miedo_Reorganiza_la_Conducta_Psicológica_de_la_Población.md`
- `corpus/reports/El_Mexicano_y_el_Tiempo__Estructura__no_Cultura__en_la_Planeación_y_el_Compromiso_Temporal.md`
- `corpus/reports/El_México_Rural_e_Indígena_en_sus_Propios_Términos__Comunalidad__Autoridad_y_Reciprocidad_como_Sistemas_con_Lógica_Propia.md`
- `corpus/reports/Elegir__Cortejar_y_Amar_en_el_México_de_Hoy__Díada_de_Pareja__Apps_de_Citas_y_Cambio_en_los_Guiones_de_Género.md`
- `corpus/reports/Genetica_y_Conducta_del_Mexicano_Contemporaneo__Canal_Individual_vs__Estructura.md`
- `corpus/reports/Health__Body__Food_and_Substance_Use_in_Mexico__The_Behavioral_Layer_of_Decisions__Environment_and_Structure.md`
- `corpus/reports/Humor_in_Mexican_Psychological_Life__2023-2026_Update.md`
- `corpus/reports/La_arquitectura_invisible_de_la_interacción_social_en_México.md`
- `corpus/reports/Mexican_Population_Genomics__2025-2026_Scientific_and_Market_Opportunity_Update.md`
- `corpus/reports/Moral_Emotions_in_Mexico__Declared_Dignity__Relational_Face__and_Residual_Catholic_Guilt.md`
- `corpus/reports/Mérito__Movilidad_Social_y_Desigualdad_en_México__Actualización_2025-2026.md`
- `corpus/reports/Psicología_Política_y_Comportamiento_Cívico_del_Mexicano_Contemporáneo__Una_Lectura_Anti-Esencialista_desde_Abajo__2026_.md`
- `corpus/reports/Psicología__Conducta_y_Sociedad_en_el_México_Contemporáneo__Análisis_Transcultural_y_Estructural.md`
- `corpus/reports/Psicología_de_la_Juventud_Mexicana_Contemporánea__Gen_Z_y_Millennials_Jóvenes_como_Cohorte_Divergente.md`
- `corpus/reports/Psicología_del_Trabajo_en_México__Un_Mapa_Basado_en_Evidencia.md`
- `corpus/reports/Psychology_of_Mexico-US_Migration__Identity__Family__Aspiration__and_Wellbeing_in_2025.md`
- `corpus/reports/Reconfiguración_de_los_Guiones_de_Género_en_México__Masculinidades__Feminidades_y_Violencia_a_través_de_Clase__Generación_y_Región.md`
- `corpus/reports/Report_26__The_Contemporary_Mexican_and_Knowledge__Expertise__Education_and_Information_as_Decision_Behavior.md`
- `corpus/reports/Salud_Mental_en_México__Prevalencia__Estigma_y_la_Brecha_entre_Necesidad_y_Atención.md`
- `corpus/reports/Sanción_Social_Horizontal_en_México__Chisme__Envidia_y_Mal_de_Ojo_como_Mecanismos_de_Nivelación.md`
- `corpus/reports/Vejez_y_Cuidado_Intergeneracional_en_México__El_Debilitamiento_del_Seguro_Familiar.md`

## Qué revisar al volver

El usuario trae los PR o sus resultados. Astra revisa cumplimiento sustantivo, discrepancias y siguiente acción. Claude emite el recibo que exige la misión; mesa adopta/fusiona. No presentar número de archivos ni CI verde como evidencia de avance por sí solos.

Los textos originales adjuntos se preservan íntegros dentro de los encargos. Su cabecera histórica de «pendiente de acordado» no invalida la firma literal reproducida en cada §2. Esta entrega no modifica los originales ni registra la aprobación directamente en GitHub: cada ejecutor comprueba el asiento de la firma para evitar duplicarlo.

`SHA256SUMS.txt` identifica los siete archivos Markdown de esta tanda. Comprueba con `sha256sum -c SHA256SUMS.txt` después de extraer.
