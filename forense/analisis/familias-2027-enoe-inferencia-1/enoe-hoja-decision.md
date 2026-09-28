# ENOE · hoja de decisión

PROPUESTO-POR-EJECUTOR. Opción recomendada: **NO-LANZAR-TODAVIA** la candidata ENOE-INFORMALIDAD para2027T4. El encargo queda resuelto mediante prueba reproducible del bloqueo con estos insumos; no se afirma imposibilidad universal de inferencia ENOE. No nueva familia adoptada, no COMMIT-3, ninguna apertura futura ni cambio de umbrales.

## Causa y evidencia

EJECUTADO: mismo ZIP histórico autorizado enoe_2024_4t_microdatos; identidad verificada antes de abrir solo ENOE_SDEMT424.csv. Auditoría agregada por estrato y grupo en diagnostico/. Los39 estratos observados con una sola UPM aparecen también en todas las filas del archivo; no proceden del filtro de entrevista, edad, ocupación o sexo. La unión es39, compartida por ambos grupos. Filtrar dominio eliminaría UPM de contribución cero y produciría singleton adicionales; el sucesor conserva esas UPM.

EJECUTADO: no hay colisión de EST_D_TRI entre entidades ni de UPM entre entidades; sí códigos UPM reutilizados entre estratos. La auditoría de llaves no demuestra que unidades físicas con el mismo código sean selecciones independientes. La propuesta anida UPM en ENT+EST_D_TRI según la notación publicada, pero requiere resolver el significado oficial de esa reutilización. CD_A no se añade arbitrariamente a la llave ni se utiliza para colapsar estratos.

LEÍDO: RNM1016 para ENOE2024T2–T4 y sus documentos vinculados, diccionario2024 y Métodos2020 §3.11 p54. La fórmula de conglomerados últimos linealiza la razón y usa m/(m−1) por estrato; no acredita regla singleton ni bandera de certeza. Documentación, URL, fecha y hashes en documentacion/; receta fijada en commit82ea8d23 antes del recálculo sucesor.

Prueba del bloqueo: en cada estrato m=1 solo se observa un total linealizado de UPM. No se identifica su dispersión entre UPM; m/(m−1) es indefinido. Distintos mecanismos de selección o totales no observados son compatibles con ese único total y generan componentes de varianza distintos. Asignarle cero, media de otros estratos o un colapso inventado añadiría una hipótesis ausente de la documentación. Un punto y una suma parcial de estratos con m>=2 no identifican la varianza total. Certeza de primera etapa por sí sola tampoco elimina el componente aleatorio de etapas inferiores. No se usa Kish para reemplazar diseño.

## Insumo específico para decidir

Solicitar a INEGI, para ENOE2024T4 / ENOE_SDEMT424.csv y esos39 códigos EST_D_TRI enumerados en la auditoría agregada, **la instrucción oficial de estimación de varianza aplicable a estratos con una UPM**, con:

- definición/crosswalk de unidad de selección a partir de ENT, EST_D_TRI, UPM y CD_A, que explique códigos UPM presentes en distintos estratos;
- indicador de certeza o probabilidades de inclusión de primera etapa para las unidades afectadas, si ese es su tratamiento, y regla para las etapas inferiores;
- si no son certeza, estructura oficial de agrupación para varianza o pesos de réplica y escalas compatibles con FAC_TRI2024T4 que identifiquen el componente faltante.

Estas son rutas alternativas de identificación; no se exige conjuntamente todo si una ruta oficial basta. Un campo arbitrario nuevo o un factor basado en pesos finales no resuelve el bloqueo. No hace falta abrir otra ola ni una reserva para formular esta solicitud. Esta entrega redacta el insumo; no contacta a terceros.

## Comparabilidad y potencia

EJECUTADO: los puntos, numeradores y denominadores históricos se conservan exactamente. El sucesor añade diagnóstico de llaves y componentes identificables; no sobrescribe p0, emisiones, lector histórico o contrato de potencia. La equivalencia de ENT+estrato con la llave anterior se verifica en el oro; no se extrapola a2027.

EJECUTADO: tabla potencia/enoe-escenarios.tsv completa, ambos grupos y seis escenarios previos intactos, con potencia/MDE/informatividad null por no identificación. Null no significa potencia cero. Alpha, banda, horizonte, dependencia temporal asumida y escenario adverso no se ajustan para obtener verde. p0 fijo y cambio entre poblaciones son preguntas distintas; rho=0 sigue siendo supuesto. No se ejecuta comparación con réplicas porque no se dispone de réplicas oficiales sustentadas. No se usa el componente parcial para calcular potencia.

Alternativa: adoptar antes del dato un tratamiento alternativo de singleton como análisis de sensibilidad con fundamento y firma específicos. No recomendada con la evidencia disponible; elegir por potencia introduciría una selección post hoc. Cualquier nueva regla queda propuesta hasta firma FP-260927-GEN2-ASTRA6-C2-ENOE-INFERENCIA-1-310e-01.

## Límites y auditoría de interpretación

No se interpreta informalidad como cultura, mecanismo psicológico ni efecto causal. La estimación nacional ponderada por sexo incluye la muestra rural/popular del instrumento; no acredita subgrupos indígenas ni transportabilidad de modelos importados. Incentivos y estructura no se aíslan en este diagnóstico. La evidencia débil es el tratamiento de diseño faltante, no el punto histórico reproducido. Lectura peligrosa: confundir oro reproducible con acierto futuro o null con ausencia de incertidumbre. Unidad: persona, proporciones0–1 y diferencias en esa misma escala; no mezcla hogares. Todo aquí es RETROSPECTIVO/planificación informada; ningún RESULT prospectivo nuevo. Contador sin incremento por diagnóstico, derivado por herramienta de cierre.
