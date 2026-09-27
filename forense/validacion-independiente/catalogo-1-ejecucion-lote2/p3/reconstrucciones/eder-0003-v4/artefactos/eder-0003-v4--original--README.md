# Reconstrucción independiente EDER 2017

Ejecutar `python3 reconstruir.py` desde este directorio. Requiere Python 3,
NumPy y pandas; las versiones utilizadas están en `recibo.json`.
Lee únicamente `/entrada` y los dos insumos enumerados bajo `/raw`.
No se consultaron resultados esperados ni se solicitó revelación.

`reconstruccion.tsv` conserva las columnas de identidad entregadas y añade
estado, proporción en escala 0–1, intervalo y motivo. Se implementan las dos
llaves de `estimandos.tsv`; la familia B no contiene llaves solicitadas.
La columna original `naturaleza_ic` se conserva literalmente como metadato
recibido; `metodo_ic` describe los intervalos calculados desde `metodo.md`.
Todos los resultados son descriptivos.

La identidad de persona usa conjuntamente `folioviv`, `foliohog`, `id_pobla`;
la vivienda se enlaza por `folioviv`. Fuente: FD §§1.1.2–1.1.4 y descripción
de tablas (§2.1). No se asignan identidades por posición ni similitud.
Se exige unicidad persona-año, unicidad en antecedentes y vivienda y enlace
completo. El desenlace conserva el texto crudo de `edo_civil1`; el año se
ordena numéricamente. Se selecciona el primer código distinto de `0` y
se exige peso finito y positivo. FD variable 43 (página impresa 71) y
cuestionario §6.3–6.5 respaldan el significado de los códigos.
Las ramas son exactamente las del método, incluyendo las transiciones
indicadas, y los códigos restantes permanecen en el denominador.

Convenciones reproducibles del bootstrap: marco formado por las UPM
presentes en el universo analítico, identificadas por el par de cadenas
crudas `(est_dis, upm)`, orden lexicográfico; generador PCG64 con semilla
20260915, 2.000 réplicas, recorrido por estrato y matriz de sorteos
(réplica, extracción). No se colapsan estratos de UPM única. Percentiles
con interpolación lineal. Estas convenciones operativas precisan aspectos
que el método no ordena explícitamente; no afectan los estimandos puntuales.
Si hay estratos de UPM única, la anchura del IC se interpreta como límite
inferior de la verdadera, según la advertencia del método.

`diagnostico.json` registra el flujo de selección, los códigos, numeradores,
denominador y cierre de partición. `inventario.json` conserva rutas,
entradas del ZIP, tamaños y SHA-256, incluyendo los documentos PDF.
`entrada/` conserva las entradas textuales recibidas, incluido el manifiesto.
No se incluyen microdatos, ZIP, PDF ni sus extracciones en el repositorio.
El SHA-256 del manifiesto original está también en `recibo.json`.
El commit de congelación incluye el código y los números antes de cualquier
revelación; su identificador se obtiene con `git rev-parse HEAD`.
