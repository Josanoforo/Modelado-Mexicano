# Hoja U5 · eje regional · para revisión de mesa

**Estado:** propuesta en PR; `adopta: NO`. La firma operativa es el merge del PR. Este documento no autoriza fusionar ni altera reservas de datos. Todos los resultados y contrastes históricos se rotulan **RETROSPECTIVA**.

## Decisiones ya asentadas antes del microdato

| Decisión | Resolución de mesa del 23/sep/2026 | Aplicación |
|---|---|---|
| R1, geografía | Entidades donde diseño y estimando lo admiten; regiones oficiales de cada instrumento; ninguna macroregión nueva. | ENVIPE y ENCIG: 32 códigos de entidad de residencia, sin convertirlos en lugar del delito o del trámite. ENIF: seis regiones de diseño `REGION=1..6`; no se fuerzan entidades. |
| R2, publicación | Punto e IC solo con denominador no ponderado ≥200, varianza estimable y regla oficial más estricta. | Los estados SUPRIMIDA-N, NO-REPRESENTATIVA y VARIANZA-NO-ESTIMABLE conservan fila y punto/IC nulos. El corte es operativo, no garantía de precisión. |

Las specs humanas [ENVIPE](../../prereg-caja/REGION-ENVIPE-spec-v1_0.md), [ENCIG](../../prereg-caja/REGION-ENCIG-spec-v1_0.md) y [ENIF](../../prereg-caja/REGION-ENIF-spec-v1_0.md), con sidecars, fijaron esas decisiones antes de ejecutar. Las specs históricas REGION-HIST fijaron las olas y el mismo protocolo antes de abrir cada una. La unidad ENVIPE es **delito** para evasión de denuncia, ENCIG es **trámite** para canal digital de luz y ENIF es **persona elegida** para tenencia/ahorro informal; no se promedian unidades distintas. El diseño usa UPM dentro de estrato, réplicas compartidas por ola y dominios sobre el marco completo. Los `RESULT-*-JSON` preservan las réplicas conjuntas sin identificadores ni pesos individuales.

## Decisiones que siguen a revisión por merge

| Decisión | Propuesta de U5 | Reserva material |
|---|---|---|
| 3, entrada de región al marcador | **No incorporar aún** como eje adoptado. Usar el [canon](../../../canon/eje-regional-v1_0.md) solo como piso descriptivo de las conductas medidas. | La cobertura de conductas adoptadas/adoptables no está cerrada; mapa temporal sin IC predictivo calibrado ni inferencia válida por conglomerado. |
| 4, unidad de cada conducta | Mantener delito, trámite y persona según tabla anterior; complemento solo con el mismo denominador y RESULT propio. | Otras conductas de los tres instrumentos requieren spec y unidad independientes. |

La recomendación por instrumento es consultar entidades ENVIPE y ENCIG únicamente para sus universos declarados, y regiones ENIF únicamente para población elegida. ENCIG representa el marco urbano 100 mil+; no debe extrapolarse a rural. ENIF no da aquí estimación estatal. Celdas regionales medidas y precisiones son trazables al TSV y once CALC sellados, cada uno con `verify: REPRODUCE` y asiento en `forense/replay-evidencia.tsv`.

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

El canon se genera por `python3 tools/astra/region/publica.py`; el [mapa](mapa-estabilidad-v1_0.md) por `python3 tools/astra/region/mapa.py`. La comparación del punto posterior con IC muestral anterior es descriptiva y **RETROSPECTIVA**. El Wilson binomial allí declara su supuesto de independencia y no se presenta como IC de diseño ni por conglomerado. No se promete detectar cambios futuros. La serie ENIF comparable recorta 18–70 años; el piso de tenencia 2024 original cubre 18+ y no se encadena a esa serie.

**No se acredita cierre integral del encargo U5 todavía.** El [snapshot U1](alcance-u1-v1_0.tsv) deja visibles las identidades consumidoras aún pendientes y diferencia la serie ENIF 18–70 del consumidor 18+. Permanecen conductas adoptadas/adoptables sin medición regional, calibración temporal y cobertura por conglomerado no resueltas. La mesa puede revisar este lote sellado sin adoptar el eje. Ninguna reserva de datos cambia por este PR.
