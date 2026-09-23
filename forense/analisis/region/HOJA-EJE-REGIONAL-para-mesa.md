# Hoja U5 · eje regional · para revisión de mesa

**Estado:** propuesta en PR; `adopta: NO`. La firma operativa es el merge del PR. Este documento no autoriza fusionar ni altera reservas de datos. Todos los resultados y contrastes históricos se rotulan **RETROSPECTIVA**.

## Decisiones ya asentadas antes del microdato

| Decisión | Resolución de mesa del 23/sep/2026 | Aplicación |
|---|---|---|
| R1, geografía | Entidades donde diseño y estimando lo admiten; regiones oficiales de cada instrumento; ninguna macroregión nueva. | ENVIPE y ENCIG: 32 códigos de entidad de residencia, sin convertirlos en lugar del delito o del trámite. ENIF: seis regiones de diseño `REGION=1..6`; no se fuerzan entidades. |
| R2, publicación | Punto e IC solo con denominador no ponderado ≥200, varianza estimable y regla oficial más estricta. | Los estados SUPRIMIDA-N, NO-REPRESENTATIVA y VARIANZA-NO-ESTIMABLE conservan fila y punto/IC nulos. El corte es operativo, no garantía de precisión. |

Las specs humanas [ENVIPE](../../prereg-caja/REGION-ENVIPE-spec-v1_0.md), [ENCIG](../../prereg-caja/REGION-ENCIG-spec-v1_0.md), [ENIF](../../prereg-caja/REGION-ENIF-spec-v1_0.md), [portafolio ENIF](../../prereg-caja/REGION-ENIF-PORTAFOLIO-spec-v1_0.md), [complemento ENVIPE](../../prereg-caja/REGION-ENVIPE-COMPLEMENTO-spec-v1_0.md) y [consumidores ENCIG 2025](../../prereg-caja/REGION-ENCIG2025-CONSUMIDORES-spec-v1_0.md), con sidecars, fijaron esas decisiones antes de sus corridas. Las specs históricas REGION-HIST fijaron las olas y el mismo protocolo antes de abrir cada una. La unidad ENVIPE es **delito** para evasión de denuncia y su complemento; ENCIG usa **persona** para solicitud general, **trámite de luz** para adopción digital y **registro de trámite sin deduplicar** para brazos `_r2`; ENIF usa **persona elegida** para tenencia/ahorro. No se promedian unidades distintas. El diseño usa UPM dentro de estrato, réplicas compartidas por ola y dominios sobre el marco completo. Los `RESULT-*-JSON` preservan las réplicas conjuntas sin identificadores ni pesos individuales.

## Decisiones que siguen a revisión por merge

| Decisión | Propuesta de U5 | Reserva material |
|---|---|---|
| 3, entrada de región al marcador | **No incorporar aún** como eje adoptado. Usar el [canon](../../../canon/eje-regional-v1_0.md) solo para las conductas medidas y sus intervalos retrospectivos. | La cobertura de conductas adoptadas/adoptables no está cerrada; el IC predictivo existe para tres series, pero una sola transición de evaluación por serie no permite inferencia válida de cobertura por conglomerado. |
| 4, unidad de cada conducta | Mantener delito, persona, trámite y registro sin deduplicar según tabla anterior; complemento solo con el mismo denominador y RESULT propio. | Otras conductas de los tres instrumentos requieren spec y unidad independientes. |

La recomendación por instrumento es consultar entidades ENVIPE y ENCIG únicamente para sus universos declarados, y regiones ENIF únicamente para población elegida. ENCIG representa el marco urbano 100 mil+; no debe extrapolarse a rural. ENIF no da aquí estimación estatal. Celdas regionales medidas y precisiones son trazables al TSV y quince CALC sellados, cada uno con `verify: REPRODUCE` y asiento en `forense/replay-evidencia.tsv`. En los brazos ENCIG por canal, 20 entidades quedan SUPRIMIDA-N según R2 y conservan cifra nula. El complemento `cumple_norma` de ENVIPE es una transformación heredada de las mismas réplicas, no una conducta independiente para contar dos veces en el mapa.

## ADENDA-1 · factibilidad AMAI, sin NSE

Se consumió la matriz U1 `forense/analisis/catalogo/matriz-amai-2024.md` por el commit de entrega `3d8e82fb` de `origin/codex/astra4-catalogo-1` (rama no fusionada al corte). AMAI 2024 requiere seis componentes exactos para hogar. **Cero de los cinco cuestionarios cotejados acredita la regla completa; el disparador de dos instrumentos no se cumple.** Por tanto no hay quinta decisión de clase en esta hoja, ni NSE calculado, ni cruces región×clase.

| Instrumento | Componente que impide la regla exacta según U1 |
|---|---|
| ENIF 2024 | Personas ocupadas de 14+ bajo la definición completa; pregunta de trabajo remunerado es aproximación. |
| ENVIPE 2025 | Dormitorios, número de baños completos e internet fijo ausentes; ocupación 18+ y vehículos del año previo son aproximaciones. |
| ENCIG 2023 | Dormitorios, baños completos, autos e internet fijo ausentes; actividad solo 18+ es aproximación. |
| ENIGH 2024 | Internet del hogar no distingue expresamente servicio fijo de móvil; equivalencia AMAI no acreditada. |
| ENUT 2024 | Número de baños completos ausente; auto e internet son aproximaciones sin cantidad/tipo fijo. |

Este cotejo textual no prueba imposibilidad de toda construcción externa y no sustituye una homologación oficial posterior. La adenda solo autoriza evaluar factibilidad y proponer entrada si dos reglas exactas fueran calculables.

## Resultado y dictamen de alcance

El canon se genera por `python3 tools/astra/region/publica.py`; el [mapa muestral](mapa-estabilidad-v1_0.md) y el [mapa predictivo](mapa-predictivo-v1_0.md) por `python3 tools/astra/region/mapa.py`. Las tres series predictivas usan `CALC-REGION-IC-PREDICTIVO-0001`, con ajuste anterior a la evaluación: punto posterior dentro en 32/32 entidades ENVIPE, 29/32 ENCIG y 6/6 regiones ENIF. Son comparaciones **RETROSPECTIVA** con intervalos potencialmente anchos, no pruebas de estabilidad. El Wilson binomial del mapa muestral declara su supuesto de independencia y no se presenta como IC de diseño ni por conglomerado. No hay IC válido de cobertura por conglomerado para una transición evaluada por serie; no se promete detectar cambios futuros. La serie ENIF comparable recorta 18–70 años; el piso de tenencia 2024 original cubre 18+ y no se encadena a esa serie.

**No se acredita cierre integral del encargo U5 todavía.** El [snapshot U1](alcance-u1-v1_0.tsv) deja visibles las identidades consumidoras aún pendientes y diferencia la serie ENIF 18–70 del portafolio 18+. Permanecen conductas adoptadas/adoptables sin medición regional; la calibración disponible es retrospectiva y la cobertura por conglomerado no puede inferirse de esta historia. La mesa puede revisar este lote sellado sin adoptar el eje. Ninguna reserva de datos cambia por este PR.
