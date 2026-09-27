# Reconstrucción independiente ENFIH 2019

Se recibieron únicamente `/entrada` y `/raw`. No se consultaron resultados esperados, servicios externos ni al preparador. La entrega se congela mediante el commit de este repositorio antes de cualquier revelación.

Ejecutar `python3 reconstruir.py` desde cualquier directorio, con las entradas en sus rutas originales y las versiones de Python, NumPy y pandas registradas en `recibo.json`. El programa verifica SHA-256 antes del cálculo. Un fallo de integridad o validación aborta la ejecución; no autoriza resultados nuevos.

`reconstruccion.tsv` conserva todas las columnas e identidades recibidas. La columna `celda` estaba vacía y continúa vacía: no se ha asignado una celda o identidad adicional. Ambas llaves tienen un método suficiente para sus proporciones descriptivas y se marcan RECONSTRUIDO. `motivo` queda disponible para estados sin cifras. El complemento no tiene IC identificado en las entradas y sus límites permanecen vacíos.

La población son todas las filas de TCONCENTRADORA con FAC_HOG finito y positivo. C_AFORE se usa directamente como 0/1; no se aplica la codificación del cuestionario individual al agregado del hogar. El descriptor, hoja TConcentradora, confirma ambos códigos; el cuestionario, pregunta 9.10, documenta la pregunta de tenencia individual. THOGAR.csv no se abre. La inspección del descriptor no implica usar otra tabla de microdatos.

Se suman los pesos en orden lexicográfico de FOLIO, VIV_SEL, HOGAR como cadenas crudas, con componentes separados. El complemento cuenta directamente C_AFORE == 0. Se comprueban unicidad de la llave, soporte de C_AFORE, diseño no vacío y suma de proporciones con tolerancia absoluta 1e-10.

Para el IC se ejecutan 2.000 réplicas de conglomerados UPM_DIS con reemplazo dentro de EDIS, manteniendo el número de UPM de cada estrato. Se usa numpy.PCG64 con semilla 20260915. Convenciones de implementación que la entrada no detalla: iteración exterior por réplica; estratos y UPM ordenados lexicográficamente como texto; selección con Generator.integers; percentiles con interpolación lineal. Los totales de cada conglomerado incluyen todas sus filas elegibles. Las convenciones se fijan antes de revelación; el IC Monte Carlo puede diferir de otra implementación con distinto orden de consumo del generador. No hay calibración ni corrección de población finita especificada.

`diagnosticos.json` contiene el perfil de anchos de las llaves de diseño, el conteo de estratos con UPM única, la comprobación A-SUMA-UNO y la sensibilidad B para H_PPAL == 1 con diferencia firmada. B no sustituye el resultado A. `bootstrap.tsv` conserva las réplicas calculadas.

`recibo.json` registra el SHA-256 del manifiesto original, hashes y rutas de cada entrada e insumo, inventario central del ZIP y hash de la única tabla de microdatos abierta. El repositorio incluye copias exactas de las entradas textuales. No contiene raw, XLSX, PDF ni texto extraído del PDF.
