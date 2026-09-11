# F5-B · transferencia reservada de M · propuesta v1.0

Estado: **PROPUESTA PARA MESA; NO AUTORIZA EMISIONES, R NI LLAMADAS**. Este
producto pregunta por generalización y no comparte fuentes ni interpretación
con `F5-documental-dirigida-spec-v1_0.md`.

## Pregunta primaria

En familias de estimandos no vistas durante desarrollo/ajuste, ¿el M renovado
reduce en al menos **2 pp** el error absoluto medio frente a `L_SOLO`, sin
perder más de 5 puntos porcentuales de cobertura?

`L_CORPUS` queda como contraste secundario con corrección Holm si se pretende
adjudicar; no se escoge después de ver cuál pierde. R es árbitro. El punto,
incertidumbre de encuesta, variación L y dependencia familiar se reportan en
capas separadas.

## Partición y cegamiento

La unidad de partición es la **familia de estimando/fuente**, no la réplica ni
una etiqueta nueva de la misma encuesta. Antes de ajustar M se congela un
registro de familias, olas, muestras y fechas de disponibilidad. Se excluyen:

- las 14 celdas F5 conocidas y cualquier reestimación, traducción, complemento
  o etiqueta que materialice el mismo objetivo;
- familias usadas por Gen1/Gen2 para elegir arquitectura, reglas, parámetros,
  umbrales, filtros o el propio diseño de evaluación;
- R, derivados de R y fuentes que revelen el objetivo al competidor.

Una ola distinta sólo crea una unidad retenida si su muestra/estimando y fecha
de disponibilidad satisfacen el corte. Dos celdas de una familia aumentan
cobertura, no el número de familias independientes.

Para cada celda, antes de emitir, se completa la tarjeta común: población,
unidad, evento, códigos, ponderador/transformación, fecha de referencia,
disponibilidad, función de R, origen numérico y criterio de comparación. Una
diferencia de unidad no se resuelve por cercanía numérica.

## Tamaño por precisión, no por disponibilidad

Se propone un diseño en dos muestras **disjuntas**:

1. Piloto de varianza: 6 familias reservadas × 2 celdas × 2 brazos L × 8
   réplicas = **12 celdas, 24 brazos, 192 llamadas**. Sirve sólo para estimar
   la dispersión entre familias y no entra a confirmación.
2. Confirmación: el tamaño se fija antes de abrir sus R mediante
   `n = ceil(((1.96 + 0.84) * sigma_plan / 2 pp)^2)`, mínimo 12 y máximo 30
   familias; `sigma_plan` es el límite superior unilateral 80% de la DE de la
   diferencia primaria por familia estimada en el piloto. Cada familia aporta
   2 celdas.

Coste confirmatorio: **2n celdas, 4n brazos L, 32n llamadas, 2n emisiones M y
2n estimaciones R**. Rango autorizado por la fórmula si mesa la adopta:
24–60 celdas y 384–960 llamadas; máximo total incluido el piloto:
**72 celdas, 144 brazos, 1,152 llamadas, 72 M y 72 R**. Si la fórmula exige
más de 30 familias, el diseño para por inviabilidad y no reduce `n` buscando
significación.

## Estimación e incertidumbre

- Por celda/brazo L: mediana de hasta 8 réplicas válidas; abstención no es
  cero. El IQR y conteo válido se reportan aparte.
- Por familia: media de los errores absolutos de sus dos celdas; ésta es la
  observación primaria para inferencia.
- Contraste: media pareada por familia de `error_M - error_L_SOLO`.
- IC95: bootstrap/t por familia según se fije antes de confirmación; R se
  propaga con réplicas oficiales/diseño acreditado cuando existan. Si no hay
  varianza R defendible, el punto queda descriptivo y el resultado inferencial
  de esa celda se reserva, no se asigna varianza cero.
- Las réplicas L no se remuestrean como familias. Familias compartidas no se
  presentan como independientes.

DIN y S6 siguen el benchmark web del 11/sep/2026: sus puntos descriptivos no
adquieren inferencia por folio/localidad, tamaño bruto o estabilidad del
bootstrap aproximado.

## Éxito, faltantes y parada

Éxito primario requiere simultáneamente:

- límite superior del IC95 de `MAE_M - MAE_L_SOLO` menor que `-2 pp`;
- cobertura M al menos 90% y no más de 5 pp inferior a L_SOLO;
- al menos 12 familias confirmatorias analizables;
- cero celda contaminada, identidad rota o tarjeta no comparable en el
  conjunto puntuado.

Una celda faltante se conserva como `NO_COVERAGE` y sale de los tres errores
pareados; la pérdida cuenta contra cobertura. Menos de 12 familias analizables
produce `NO-ADJUDICABLE-POR-COBERTURA`. Cualquier contaminación o cambio de
snapshot produce `NO-ADJUDICABLE-POR-CONTROL`.

No hay parada temprana por victoria/derrota. Se para por identidad, fuente o
control roto; por dos fallos sistémicos consecutivos; al alcanzar `n`; o por
inviabilidad si `n>30`. La selección y el análisis no cambian después de R.

## Arquitectura e interpretación

La arquitectura/hipótesis heredada de Gen1 se enumera antes de partir. Los
componentes modificados con errores de F5 y el procedimiento de selección de
modelos se registran con hashes. Una cifra, prior, umbral o grado de evidencia
Gen1 no entra automáticamente al M renovado. La exposición del LLM durante
preentrenamiento no puede certificarse desde el repo; sólo se acredita el
contexto experimental controlado.

El diseño aplica el principio de separar selección y evaluación descrito por
Cawley y Talbot (2010) a familias/estimandos; no presupone que validación
cruzada genérica sea apropiada para todas las encuestas.
