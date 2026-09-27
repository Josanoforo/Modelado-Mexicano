# Reconstrucción independiente ENCUCI 2020

Se utilizaron exclusivamente `/entrada` y los insumos enumerados de `/raw`.
No se consultaron resultados esperados, sitios externos ni al preparador.
El SHA-256 de `/entrada/manifiesto.json`, conservado en `recibo.json`, es
`f0c6820876e1d5e3341ffa0ce48175deff70f9f69c543d543b1caac173b89d55`.

`reconstruccion.tsv` conserva todas las columnas y las tres identidades originales.
Dos filas se reconstruyen. La fila `RESULT-ENCUCI-B-P-RUR-AGR` queda sin cifras:
llave y conducta dicen rural, segmento dice urbano y celda está vacía. No existe
regla de precedencia que resuelva la contradicción. No se corrige ni se adivina
esa identidad. La fila urbana y la de cualquiera de las dos formas de mordida
son coherentes con sus conductas y con las celdas del método.

`celdas_metodo.tsv` contiene cálculos por definiciones analíticas del método,
sin asignarles `result_id`: las cuatro celdas A, las cuatro celdas B y la
sensibilidad B `{U}` frente a `{R,C}`, etiquetada no adoptable. La existencia
de una cifra para una celda rural no resuelve la contradicción de identidad.
No se estima el universo secundario `U_A_POB`: no se solicita en estimandos.tsv
y no se necesita para ninguna de las celdas principales.

Las estimaciones son cocientes de sumas de `FAC_SEL`, sin normalización,
en escala de proporción. La unión es exacta y uno a uno por `ID_PER`, con
igualdad comprobada de las variables de diseño entre las tablas. Se aplican
los filtros explícitos de U_A y U_B. Se cuentan blancos y NS/NR; no se imputan.
`auditoria.json` registra las cabeceras DBF, las frecuencias de códigos,
exclusiones y la guardia G-3. Las llaves de diseño permanecen como texto.

El bootstrap usa el marco completo de SEC_4_5 antes de los filtros, con aporte
cero fuera de cada dominio. Se sortean n UPM con reemplazo en cada estrato con
n UPM. Se aplican las multiplicidades a numeradores y denominadores. Son 2000
réplicas de PCG64 con semilla 20260909. Para hacer reproducible lo que el método
no detalla, se fija orden lexicográfico de estratos y UPM y se genera una matriz
(2000, n) por estrato; se comparten sorteos entre celdas. Se usan percentiles
lineales 2.5/97.5. Estas convenciones pueden cambiar los extremos simulados
frente a otra implementación con la misma semilla. No hay estratos de UPM
única en el marco observado (281 estratos y 3096 pares estrato-UPM).

El descriptor confirma `C = Complemento urbano` y `AP4_3_2 = 1` como presencia
de pandillerismo, robos o delincuencia (bloques DOMINIO y pregunta 4.3).
AP5_17 y AP5_18 distinguen solicitud y entrega (página impresa 32).
El cuestionario, sección VII, pregunta 7.3, dice «alguna vez en su vida» y
limita el bloque a personas de 18 años y más. Esto difiere de la descripción
15+ de la familia B en metodo.md. Se conserva el filtro explícito de respuestas
válidas, sin atribuir respuestas a menores ni extrapolar el resultado a ellos.
La cifra B representa a quienes tienen respuestas válidas según U_B.

Reproducción, con Python 3 y NumPy (versiones exactas en auditoria.json):

```sh
OPENBLAS_NUM_THREADS=1 python3 reconstruir.py
OPENBLAS_NUM_THREADS=1 python3 verificar.py
```

La verificación repite la ejecución, exige salidas idénticas byte a byte y
comprueba ambas estimaciones mediante sumas directas con Decimal, independientes
de la agregación NumPy por UPM. También exige ausencia de cifras y presencia de
motivo en la identidad no reconstruible. No compara con resultados esperados.

`inventario.json` contiene hashes y rutas de todas las entradas, así como nombres,
tamaños y hashes de cada miembro del ZIP. `entradas/` conserva las entradas
textuales originales. Los datos raw y los PDF se mantienen fuera del repositorio.
El commit local congela código, documentación y cifras antes de revelación;
su identificador se obtiene con `git rev-parse HEAD`. El trabajo termina ahí.
