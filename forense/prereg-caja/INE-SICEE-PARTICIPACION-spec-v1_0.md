# CALC-INE-PISOS-SICEE-0001 · Participación federal publicada por el SICEE-INE, 1991–2024

El primer resultado que produzca este procedimiento es el que se reporta.

Acto `ASTRA5-U3-POLITICA-COMPLETAR` (0-bis `d459637e`). Lo que se conserva:
`CALC-INE-PISOS-2024-0001` (#1084) ya midió las marcas de voto sobre la
lista nominal de los cuadernillos 2024 (Conteos Censales DECEyEC). Ese
producto no se recalcula ni se mezcla con éste.

## Objeto

Payload `a6_sicee_participacion_nacional_1991_2024`, JSON de la API pública
`sicee-api.ine.mx`, sha256
`8088f9f36345e99203e8bb6f32c657c3f85335977bcf49da5084064ec893d87b`
(recalculado en disco: COINCIDE). Cada fila es una elección federal o
mecanismo de participación nacional × año × `distribucion`, con los campos
`total_votos`, `lista_nominal`, `num_votos_nulos`, `num_votos_can_nreg` y
`porcentaje_participacion` publicado. Los cargos se tratan por separado y
nunca se suman: `PRE`, `SEN_MR`, `SEN_RP`, `SEN`, `DIP_MR`, `DIP_RP`,
`CONS_POP` (consulta popular 2021) y `CONS_POP_RM` (revocación de mandato
2022). Consulta y revocación no son elecciones y se rotulan así.

El corpus no documenta qué significa `distribucion` (1/2). Existe desde 1991,
antes del voto en el extranjero, así que no se le atribuye ese sentido. Se
trata como llave opaca. Las dos filas de cada cargo×año se conservan, no se
suman ni se elige una. Como diagnóstico se informa si `total_votos` y
`lista_nominal` coinciden entre ellas.

## Medición

Para cada fila: `tasa = total_votos / lista_nominal`, con los enteros
publicados. `total_votos` incluye votos nulos y por candidaturas no
registradas; por eso esta tasa es participación sobre la lista nominal, no
voto válido. Se reportan también la tasa publicada, leída de
`porcentaje_participacion`, y la diferencia en puntos entre ambas, como
control aritmético de la fuente. Parseo: se quitan espacios, comas y `%`;
cualquier valor que así no se convierta a número detiene la corrida sin
sello. Filas con `lista_nominal <= 0` salen `NO-ESTIMABLE`. Las filas se
emiten ordenadas por cargo, año y distribución.

No hay IC: es un registro administrativo de cómputo. Su error es de
captura, de cobertura del listado y de tratamiento de casillas especiales
(votantes fuera de su sección) y del voto desde el extranjero (desde 2006).
La fuente no desglosa esos componentes y aquí no se modelan. Tampoco hay
serie calibrada: las elecciones presidenciales, intermedias y los mecanismos
de consulta son objetos distintos, y el año electoral cambia la oferta.
Estado: `SIN-HISTORIA-PARA-CALIBRAR`, sin tendencia, sin retador y sin
atribuir causas a diferencias entre años.

## Auditoría de rigor extremo

La tasa describe marcas administrativas sobre un denominador de registro,
no motivación ni conducta individual. No hay unión con LAPOP ni con ENCUP, y
ninguna asociación agregada se presenta como conducta de personas
(falacia ecológica). Tampoco se desagrega por entidad: la tabla por entidad
(`a6_sicee_participacion_entidad_1991_2024`) queda dictaminada y sin medir.
