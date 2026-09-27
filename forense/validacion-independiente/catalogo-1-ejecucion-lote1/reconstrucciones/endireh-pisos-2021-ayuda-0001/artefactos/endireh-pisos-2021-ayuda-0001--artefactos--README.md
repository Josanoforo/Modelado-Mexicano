# Reconstrucción independiente ENDIREH 2021

Se entregan 117 llaves: 116 RECONSTRUIDO y una
NO-RECALCULABLE-DESDE-SPEC, con motivo. No se consultaron resultados esperados,
helpers del productor, un clon, comparaciones ni reservas. No se solicitó
revelación ni información al preparador. No se declara coincidencia de resultados.
Se conservan las cifras de la primera ejecución numérica, sin ajuste posterior.

## Reproducción

Desde este directorio, con Python 3.14.4, NumPy 2.3.5 y pandas 2.3.3:

```sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python3 reconstruir.py
python3 verificar.py
sha256sum -c SHA256SUMS
```

Los insumos permanecen fuera del repositorio en `/raw`; puede cambiarse su ubicación
con `ENDIREH_RAW`. `entrada/` contiene copias byte a byte de todos los archivos
recibidos. `inventario_insumos.json` conserva los nombres originales, URLs, SHA
declarados y observados y rutas recibidas. `entradas_zip.json` conserva los nombres,
tamaños y SHA-256 descomprimidos de las 27 entradas del ZIP. No se incluyen raw,
PDF ni texto extraído de PDF en el commit. Los campos originales `estado_acceso`
de insumos se conservan como evidencia recibida, no como evaluación de cifras.

## Implementación y decisiones reproducibles

La unión de 38 actos sigue `metodo.md`: positiva con al menos un 1–3, negativa
solo con todos 4, y desconocida en otro caso. Se valida la unión uno a uno por
`ID_PER`, la cobertura completa de ambos archivos unidos, sexo femenino y pesos
positivos. El universo de las UPM se fija en todas las mujeres A1/A2 antes de
filtrar los dominios. Los estratos y UPM son los de TB_SEC_XIV; una UPM se
identifica por el par (EST_DIS, UPM_DIS).

Las proporciones son cocientes de sumas de FAC_MUJ. Ayuda y denuncia utilizan
denominadores propios con 1/2 conocidos entre unión positiva y edad 15–120.
Instituciones restringen además a ayuda=1 y respuestas 1/2 conocidas de cada
casilla. Razones restringen a ayuda=2 y denuncia=2, usando 0/1 conocidos de
cada motivo. No se recodifica un blanco como cero ni se mezclan ayuda y denuncia.

Se aplican los rangos de edad y los códigos NIV literalmente. Localidad es
DOMINIO (U urbano, C complemento urbano, R rural), pareja es T_INSTRUM y entidad
es CVE_ENT, con ceros iniciales preservados. Estas identidades figuran en FD,
en el encabezado de TB_SEC_XIV, pp. 453–454; FD pp. 454–462 documenta los actos,
pp. 484–486 ayuda, denuncia e instituciones, y pp. 629–632 los motivos. También
se revisó el cuestionario A, preguntas 14.1, 14.7, 14.8 y 14.22. Los segmentos
se asignan por las columnas semánticas de estimandos.tsv, nunca por el orden
lexicográfico o un número de celda supuesto.

Por estrato se seleccionan n_h UPM con reemplazo y probabilidades iguales,
incluidas las de contribución cero al dominio. Se usan las mismas 500 selecciones
para todas las celdas; singleton se autorremuestrea. Semilla 20260923, generador
NumPy Generator(PCG64), estratos y UPM ordenados lexicográficamente, generación
de una matriz de índices de forma (500, n_h) por estrato. Percentiles lineales
2.5/97.5 y CV = desviación estándar de réplicas (ddof=1) / estimación puntual.
La spec no fija RNG, orden de consumo, interpolación del percentil ni ddof:
estas convenciones son explícitas, no se ajustaron a cifras externas. No puede
garantizarse igualdad de IC a tolerancia 1e-10 frente a otra implementación.

Se comprueban n conocido ≥100, UPM con respuestas conocidas ≥5, ancho ≤0.20,
y CV ≤0.30 si p>0. Ninguna celda calculada requirió supresión. El código también
prevé dejar cifras y réplicas vacías para una celda suprimida, con motivo;
usa NO-RECALCULABLE-DESDE-SPEC porque el catálogo solicitado no ofrece un estado
de supresión. No descarta silenciosamente réplicas con denominador cero.
Las réplicas guardadas son exclusivamente proporciones por llave, sin personas
ni identificadores de UPM. control_calidad.json contiene conteos agregados.

## Conflicto de identidad no resuelto

`RESULT-ENDIREH2021-AYU-TABLA#115`, `razon_14`: la especificación describe
«desconocía servicios», mientras FD p. 632 y cuestionario A 14.22 definen
P14_22_14 como «No sabía que existían leyes para sancionar la violencia».
El mnemónico propuesto se conserva en identidades.tsv como referencia del
conflicto, pero no se presume que estos conceptos sean equivalentes. No se
calculan punto, IC ni réplicas para esa llave. Las demás razones mantienen
sus identidades separadas.

## Congelación

recibo.json conserva el SHA-256 exacto del manifiesto recibido y su lista de
entradas. SHA256SUMS cubre código, entradas, recibo, documentación y cifras;
se excluye a sí mismo para evitar una referencia circular. El commit de Git
congela también SHA256SUMS. El hash del propio commit se comunica al entregar;
no se introduce dentro del commit que identifica. No hubo revelación.
