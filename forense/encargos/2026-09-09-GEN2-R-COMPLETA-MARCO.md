# ENCARGO 3/5 · ACTO GEN2-R-COMPLETA-MARCO

EL ÁRBITRO NO COMPITE, PERO TIENE QUE ESTAR EN LA CANCHA

OBJETIVO: completar, hasta donde permiten los payloads ya presentes, los árbitros R del marco de 14 celdas para que la comparación triádica no quede artificialmente reducida a las seis celdas actuales.

CABECERA: CAJA, Ubuntu/WSL, Opus. Microdato permitido. Cero llamadas LLM. Cero cambios al motor.

COMPUERTA: contrato TRIADA del ENCARGO 2/5 fusionado, o alternativamente el marco v1.3 verificado byte a byte si este acto corre en paralelo por decisión expresa de mesa.

FIRMA DE MESA SOBRE FP-370:

codificacion-R-v1_0.tsv no se modifica in situ. Su codificación, universo, ponderador, estrato y UPM para las filas del marco se sellan mediante sucesora fechada, preservando literalmente los valores preexistentes. R es ground truth de evaluación; sellarlo no adopta nada al motor.

Nace, si el árbol lo confirma necesario, codificacion-R-v1_1.tsv + hash.

La única transformación permitida respecto de v1.0 es el estado/firma y correcciones puramente registrales que no cambien el estimando. Cualquier propuesta de cambiar código, universo, peso o diseño después de abrir el microdato es PARO y firma nueva.

P1 · CENSO

Cruzar mecánicamente: 14 ids de marco-M-sorteado-v1_3.tsv; R GEN2 ya existentes; codificacion-R; payloads; demanda/registro de corrida0. Clasificar cada celda: R-YA-SELLADO · R-LISTO-PARA-CORRER · R-BLOQUEADO-POR-INPUT · R-SIN-SPEC. No hardcodear «faltan ocho» o «faltan nueve». Derivar el número real del árbol. Los seis R ya usados por F5 no se vuelven a medir por ceremonia. Sirven de controles positivos.

P2 · PRE-REGISTRO DE LOS FALTANTES

Para cada grupo coherente de fuente/formato, congelar antes del microdato: payload y hash; tabla; variable; universo; códigos; ponderador; estrato; UPM; estimador; escala; output esperado por nombre, no por valor. Agrupar sólo cuando compartir apertura de archivo y diseño sea real. D-15: un lote coherente puede producir varios RESULT.

P3 · MEDICIÓN

Para cada R faltante ejecutable: preflight → run → verify → registro. Cada CALC-R debe producir como mínimo: punto; n no ponderado; masa/peso pertinente; faltantes/excluidos; número de estratos/UPM cuando aplique; IC o reserva explícita si no puede identificarse correctamente. No leer L_SOLO, L_CORPUS ni M durante la medición. No comparar el R nuevo con la predicción antes de sellarlo.

P4 · CONTROL DE INDEPENDENCIA

La corrida R no puede depender de: corridas-L/; corridas-M/; extractor L; CALC TRIADA; errores históricos del contendiente. Control positivo: para los R ya existentes, la identidad de variable/universo/codificación de la sucesora sellada coincide con los objetos usados por sus CALC actuales. No es necesario volver a calcular su punto.

P5 · FRONTERA

Si un target no puede medirse con archivos existentes: no adquirir nueva fuente dentro de este acto; abrir NC precisa; excluirlo de UR; dejar qué payload o decisión lo habilitaría. El ENCARGO 5/5 usa el UR congelado resultante. No amplía el panel después de ver quién va ganando.

PERÍMETRO: sucesora de codificación R, data/corrida0/CALC-R-* nuevos estrictamente necesarios, vistas derivadas, notas, NC, 0-bis, cascada.

NO TOCA: L, paquete corpus, M, milpa/, F5 histórica.

CONTADOR: cuenta_gen2 = SI para cada nuevo CALC-R sellado, con OBJETO explícito en este lanzamiento. Cuenta como medición GEN2; no como adopción al motor.

CIERRE: tabla de 14 celdas con estado R y UR final; cascada; NC; CONSUMIDO.

## NO-CORRIDO / RESERVAS

- Ninguna celda R quedó sin correr: 0 bloqueadas y 0 sin spec; no nace NC nueva.
- El IC de `DIN-M-01` queda rotulado como aproximación/cota inferior porque estrato y UPM reales no se publican en el payload. `TRA-M-02` y `TRA-M-03` declaran un estrato con UPM única.
- No se calculó U3 ni se comparó contendiente alguno. `NC-0143` permanece abierta para `ENCARGO 5/5`, que debe consumir el UR congelado en 14/14.

## CONSUMIDO

Ejecutado por `ACTO GEN2-R-COMPLETA-MARCO`: 14/14 árbitros R sellados, `UR=14` congelado; ocho CALC-R nuevos con `cuenta_gen2=SI`; cero NC nuevas. Cierre en `forense/notas/2026-09-09-GEN2-R-COMPLETA-MARCO-cierre.md`.
