# CALC-LAPOP-PISOS-2019-0001 · Oferta y confianza policial

El primer resultado que produzca este procedimiento es el que se reporta.
Fuente `mexico_lapop_americasbarometer_2019_v1_0_w`, estudio mexicano
AmericasBarometer 2018–19 v1.0_W. Unidad: persona entrevistada, nacional.
No se mezcla con la muestra especial del terremoto 2017. El CALC anterior
`CALC-ARBITRO-MARGINALES-2-LAPOP-0001` ya midió asociaciones oferta/voto;
éste mide prevalencias marginales distintas directamente desde microdato.

`clien1na`: «Y pensando en las últimas elecciones presidenciales/generales
de [año] ¿alguien le ofreció a usted un favor, regalo o beneficio a cambio
de su voto?» 1 sí, 2 no, faltantes fuera. Se estima proporción de sí entre
1/2. Ofrecimiento no implica recepción, aceptación ni voto vendido.

`b18`: «¿Hasta qué punto tiene confianza usted en la Policía Nacional?»
escala ordinal 1 nada a 7 mucho. Se conserva universo 1..7 y se estima
proporción 6/7, umbral de confianza alta fijado antes de abrir resultado.
No se atribuye esta pregunta a ENCUP.

Para ambos reactivos se requiere `wt>0`, `estratopri` y `upm` presentes.
Proporción = suma ponderada del evento / suma de peso del universo. IC95:
2 000 réplicas de bootstrap de UPM con reemplazo dentro de estrato, semilla
42 para clien1na y 43 para b18, PCG64; percentiles 2.5/97.5. Estratos con
una sola UPM quedan fijos. n mínimo 30. Se reportan n, n afirmativos, masa
ponderada, estratos, UPM y réplicas finitas. Sin celdas geográficas:
la geografía admisible requiere verificación propia del diseño; no se
infieren perfiles de votantes ni se une a secciones INE. Este punto no
pronostica otra ola: SIN-HISTORIA-PARA-CALIBRAR. Rupturas de modo y texto
entre 2019 y 2021/2023 se dictaminan antes de compararlas.

## Auditoría de rigor extremo

Las dos proporciones son retrospectivas y de personas entrevistadas.
El IC es de muestreo bajo diseño aproximado, no de sesgo de no respuesta.
La confianza declarada puede responder a violencia, acceso y experiencias
con instituciones, no a una disposición cultural aislada. Cobertura rural,
indígena y popular no debe inferirse de un único marginal nacional. No hay
contraste causal de compra de voto ni relación individual entre la oferta
de una campaña y confianza policial.
