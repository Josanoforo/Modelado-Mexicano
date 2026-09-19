# Spec fijada · ISSP México 2017, redes de apoyo cotidiano Q7

Estado: `FIJADA-ANTES-DE-ABRIR-FILAS`. Operación descriptiva autorizada por
`GEN2-ISSP2017-REDES-APOYO-COTIDIANO-CLI-1`. No ejecuta F6, M, L, HOLDOUT ni
piloto 3; no calibra ni adopta parámetros. La apertura de agosto ya mostró
distribuciones, por lo que el análisis se declara explícitamente no ciego.

## Pregunta, unidad y fuente

Q7 pregunta a quién acudiría primero la persona entrevistada en cinco
situaciones: trabajo en hogar/jardín (`v21`), ayuda en el hogar durante una
enfermedad (`v22`), hablar al sentirse deprimido (`v23`), consejo sobre
problemas familiares (`v24`) y una ocasión social agradable (`v25`). Son cinco
situaciones distintas, no una escala psicológica.

La fuente es ISSP 2017 *Social Networks and Social Resources*, ZA6980 v2.0.0,
DOI `10.4232/1.13322`. La unidad es una persona adulta entrevistada. México se
selecciona conjuntamente con `c_alphan=MX` y `country=484`; se exige además
`studyno=6980`, DOI y versión embebidos. `CASEID` debe ser completo y único.
El marco ya es adulto: una edad desconocida no excluye; una edad observada
menor a 18 invalida la corrida.

El cuestionario mexicano (PDF p.3 / impresa p.2) y el Variable Report integrado
(páginas impresas 50, 52, 54, 56 y 58) acreditan Q7a-e↔v21-v25 y el catálogo.
El DTA y SAV deben coincidir en dimensiones, etiquetas de variable y valores.

## Catálogo y ponderación

Las respuestas sustantivas son: 1 familiar cercano; 2 familiar más lejano;
3 amigo cercano; 4 vecino; 5 alguien con quien trabaja; 6 alguien más;
7 ninguno. El código 8, no puedo elegir, y el código 9/vacío, no respuesta, son
estados separados. Ninguno es sustantivo; desconocidos nunca se recodifican a
cero ni a ninguno. Se conservan categorías con cero observaciones.

Se usa `WEIGHT`, numérico, finito y positivo. La documentación mexicana lo fija
en 1 (`No weighting`); no se inventa ajuste poblacional. Un peso inválido tiene
prioridad como estado de cobertura. No hay imputación, recorte ni compensación
de no respuesta.

## Estimandos congelados

P1. Para cada ítem y para TOTAL, HOMBRES (`SEX=1`) y MUJERES (`SEX=2`), se
publica la distribución de códigos 1..7 sobre el denominador válido específico,
con n y masa de numerador/denominador, proporción, porcentaje y cobertura. El
sexo no clasificable permanece en TOTAL y se publica como residuo de la
reconstrucción.

P2. Para cada ítem y dominio se agrega familia = códigos 1+2. Se conserva la
distribución nativa y se publica mujeres menos hombres en puntos porcentuales.
No se suman amistades a familia.

P3. Entre quienes tengan cinco respuestas válidas y peso utilizable se cuenta
en cuántas situaciones respondieron ninguno (`v=7`), con distribución 0..5 y
proporciones sin ninguna, con alguna y en todas. Sobre ese mismo universo se
publica la matriz 5×5 de coocurrencia de ninguno; las diez parejas únicas quedan
representadas simétricamente y las diagonales son los marginales del universo
completo. Se publica la cobertura de casos completos respecto de toda la
muestra con peso utilizable.

Cada salida lleva n, masa, numerador, denominador y unidad. Las distribuciones
por ítem no se comparan como si tuvieran el mismo universo; P3 usa sólo casos
completos. El conteo 0..5 es descriptivo, no índice validado de soledad,
aislamiento, depresión o capital social.

## Precisión, controles y límites

No se acreditaron UPM/estratos ejecutables para México. Todos los puntos y
contrastes llevan `EE-IC-NO-DISPONIBLES-DISENO-NO-ACREDITADO`; no se usan
bootstrap iid, pruebas de significación ni tamaños efectivos inventados.

Controles: identidad México, catálogo cerrado, peso válido, llave única,
particiones unitarias, reconstrucción TOTAL por sexo más residuo, exhaustividad
0..5, matriz simétrica y diagonal igual a los marginales de ninguno sobre casos
completos. Un programa separado recalcula puntos y denominadores sin importar
el medidor.

Los resultados describen la primera persona declarada a quien acudirían. No
miden apoyo recibido, disponibilidad real, dinero, calidad u obligación del
vínculo, causalidad ni representatividad más allá del marco documentado.
