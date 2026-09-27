# Reconstrucción congelada antes de revelación

Única llave solicitada: `RESULT-ENVIPE-DEN-P-C2-U4`. Se conserva literalmente
su identidad en `reconstruccion.tsv`; C2 y U4 están definidos en `entrada/metodo.md`.
No se consultaron resultados esperados ni se solicitó revelación al preparador.

Ejecutar desde este directorio: `python3 reconstruir.py`.
Requiere Python 3, NumPy y pandas; versiones ejecutadas en `recibo.json`.
Los argumentos `--entrada`, `--raw` y `--salida` permiten cambiar rutas.
Los datos se leen directamente del ZIP externo; no se incluyen raw, PDF ni
transcripciones de PDF en Git. `entradas_zip.json` conserva nombres, tamaños
y SHA-256 de todos los miembros del ZIP. El recibo conserva hashes observados
de los cuatro insumos, las entradas y el SHA-256 del manifiesto original.

## Implementación

Se seleccionan delitos BPCOD 05–15, BP1_20=2 y BP1_23 01–08.
C2 vale uno para 01, 02, 06 y 08. Se toma el máximo por ID_PER y se enlaza
exactamente con tper_vic2 para obtener FAC_ELE, EST_DIS y UPM_DIS.
Se comprueban unicidad, cobertura y concordancia de UPM, VIV_SEL, HOGAR,
R_SEL y diseño entre tablas. No se deduce ni repara ninguna identidad.
La proporción es suma(FAC_ELE × máximo C2) / suma(FAC_ELE).
Los blancos de BP1_23 se cuentan fuera de los universos, sin imputación.

Fuentes humanas consultadas: descriptor, sección 1.2.4 (relación entre tablas),
tablas TPer_Vic2 (FAC_ELE, EST_DIS, UPM_DIS; página impresa 61) y TMod_Vic
(BP1_23, página 71; diseño, página 80); cuestionario de módulo, pregunta 1.23.
Los documentos se identifican mediante hashes y rutas en el recibo.

El bootstrap usa las UPM observadas en el universo U4 y los identificadores
literales, ordenados lexicográficamente por estrato y UPM. Para cada réplica,
en cada estrato se sortean n_h UPM con reemplazo; sus totales ponderados se
suman y se calcula el cociente. Los estratos de UPM única se sortean a sí
mismos. Se usa PCG64, semilla 20260909, 2000 réplicas y percentiles lineales.
`replicas.tsv` conserva todas las proporciones simuladas.

La especificación no fija el orden de consumo del generador ni la convención
de interpolación de percentiles; aquí quedan explícitos. Tampoco explicita si
deben entrar UPM sin observaciones en el dominio: se usa el universo filtrado
declarado. No se afirma coincidencia numérica con una implementación oculta.
La tolerancia recibida (1e-10) se conserva, sin comparación contra esperados.

## Resultado y límites

Proporción: 0.29431298745731216; intervalo: [0.28240840531755856,
0.30562527544837575]. Numerador ponderado 4409572; denominador 14982594.
Hay 13023 personas, 725 estratos observados y 83 estratos de UPM única.
Por la regla recibida, `METODO-IC=IC-CON-ESTRATOS-DE-UPM-UNICA`: la anchura
se interpreta como límite inferior de la verdadera, no como IC exacto.

El descriptor y el método mencionan EST_DIS 001–607, pero los datos contienen
más estratos. Se preservan sus etiquetas observadas, sin truncar, fusionar ni
reasignar estratos. Esta discrepancia documental queda advertida; los campos
están presentes y completos para U4 y concuerdan entre ambas tablas.

`verificacion.json` registra un cálculo independiente de la estimación con la
biblioteca estándar y la reproducción byte a byte de las salidas principales.
El commit congela código, entradas, recibo, auditoría, réplicas y reconstrucción.
La identificación del commit se entrega fuera del propio recibo para evitar
una referencia circular al hash del commit.
