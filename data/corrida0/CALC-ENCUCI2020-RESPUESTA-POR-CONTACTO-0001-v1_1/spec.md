# CALC-ENCUCI2020-RESPUESTA-POR-CONTACTO-0001-v1_1

ENCUCI 2020, persona seleccionada de 15 años o más; marco: filas de
`ENCUCI_2020_SEC_4_5.dbf` con `FAC_SEL` finito y positivo. La unidad es
persona, no trámite ni transacción. `AP5_16_1..10` son contactos por tipo;
`AP5_17` y `AP5_18` son respuestas generales de persona y no se atribuyen a
una autoridad. Códigos válidos: 1=Sí, 2=No; 9/blanco/otros son desconocidos.
Esta sucesión conserva intacto el sello de `...-0001` y corrige sólo el
control publicado: ahora las identidades de partición y unión se calculan y
publican por los diez contactos, no sólo por el primero.

Por cada contacto afirmativo se estima cobertura de AP5_17/18, las cuatro
categorías exhaustivas (ninguna, sólo solicitud, sólo entrega, ambas), unión,
P(entrega|solicitud) y P(entrega|no solicitud). Dentro de personas con algún
contacto acreditado y respuestas válidas se contrasta, para cada inciso,
contacto Sí frente a No: diferencia de unión y ambas; desconocidos se excluyen
y cuantifican. Finalmente, dentro de cada contacto afirmativo se distribuye el
número de otros contactos (0,1,2+) entre vectores completos y se compara la
cobertura de respuestas con ese subconjunto.

La ponderación es `FAC_SEL` sin normalizar. IC95: bootstrap de UPM con
reemplazo dentro de `EST_DIS`, 2,000 réplicas y semilla 20260919; los
contrastes se calculan por réplica, conservando covarianza. No se suman las
diez comparaciones ni se interpretan como ranking, causalidad o tasa de una
autoridad. Adopción y contador: PENDIENTE-DE-MESA.
