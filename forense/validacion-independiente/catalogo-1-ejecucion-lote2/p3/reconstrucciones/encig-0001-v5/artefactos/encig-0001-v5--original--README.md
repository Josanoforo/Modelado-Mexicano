# Reconstrucción independiente ENCIG 2025

Se recibieron únicamente `/entrada` y los tres insumos enumerados en `/raw`.
No se consultaron resultados esperados, otras implementaciones ni fuentes externas;
no se solicitó revelación ni se contactó al preparador.

`recibo.json` conserva el SHA-256 del manifiesto, los hashes de todas las entradas,
las rutas, URL, tamaños y hashes de los insumos y el inventario con hashes de cada
miembro del ZIP. Las seis entradas originales se conservan en `entrada/`.
Los datos y los PDF permanecen fuera del repositorio.

Ejecutar `python3 reconstruir.py` y `python3 verificar.py` desde cualquier directorio,
con los insumos en las rutas registradas. Se requiere NumPy; la versión usada queda
en el recibo. La verificación vuelve a leer los CSV y calcula los cuatro puntos
con aritmética Decimal. No compara contra resultados externos.

## Correspondencias y alcance

Las cuatro llaves RESULT nombran literalmente las fórmulas A-P-SOL1,
B-P-DIG-SD, B-P-PRE-SD y C-P-ADOPTA de las secciones 3.2, 3.3–3.4 y 3.6.
Se conservan todos los campos de estimandos.tsv sin cambios. No se deduce una
identidad alternativa desde `conducta`, `segmento` o el sufijo `_r2`; tampoco
se certifica una equivalencia semántica de esos rótulos con la medida calculada.
La celda vacía permanece vacía y `VER-SPEC` se conserva en la entrada;
las unidades del cálculo son persona (A), evento (B) y evento del tipo 01 (C).

El descriptor confirma P8_4=1/0 y los códigos de P7_3; define NT_TIPO como
número de trámite/último evento, 01–03, y N_TRA=01 como pago ordinario de luz.
El cuestionario, preguntas 8.3 y 8.4, confirma el salto cuando todos los incisos
son 2 o 9. Se leyó la documentación mediante pdftotext, fuera del repositorio.

La llave declarada de sección 7 no es única (7.430 grupos, 18.027 filas), pero
(ID_TRA,NT_TIPO) y el ID_TRA de sección 8 sí son únicos. Se mantiene SD primaria.
CD conserva la primera fila por ID_TRA y descarta 10.597 eventos; sus cálculos
auxiliares y SOLANY constan en diagnosticos.json.

El join SD cubre 124.314/124.314 filas. Esa cobertura nominal no elimina la selección:
99.340 filas emparejadas tienen P8_4 fuera de {0,1}. B debe leerse como proporción
de trámites señalados entre los que tienen respuesta válida en 8.4, por canal,
condicionada por el flujo de 8.3; no acredita pago de soborno. DIG incluye teléfono
(código 3) porque así lo prescribe el método. A mide solicitud directa declarada.
C mide asociación descriptiva de canal: el cero representa canal físico, no rechazo
al servicio digital; la condición sin coerción/sin riesgo fiscal la impone la
construcción del universo, no el informante.

## Convenciones numéricas y límites

Los puntos se suman en orden de archivo; los ceros de P8_4 son respuestas válidas.
Los faltantes y pesos inválidos se excluyen sin imputar. Los diagnósticos incluyen
frecuencias, residuos, cobertura, diseño y guardias. El residuo ponderado de B
usa como denominador U_B y el de C todos los eventos tipo 01 con peso positivo.

IC: 2.000 réplicas, PCG64, semilla 20260909, UPM con reemplazo dentro de estrato.
Las llaves de diseño se conservan como texto opaco. Se agrupan las filas elegibles
de cada estimando en orden de primera aparición; se reinicia el generador por
estimando, se recorre primero estrato y se genera una matriz (2000,n_UPM).
Se usa el percentil lineal de NumPy. Los estratos con UPM única se conservan.

El método no fija el orden de consumo aleatorio, el reinicio entre estimandos,
el orden de estratos/UPM, la interpolación del percentil ni si el marco de UPM
debe incluir unidades fuera del dominio. Estas son convenciones explícitas de
esta implementación, no información recuperada de resultados esperados.
Por ello no se afirma que la especificación determine un único IC a tolerancia
1e-10. Los puntos sí se verifican a esa tolerancia. Hay números y por ello las
cuatro filas llevan RECONSTRUIDO, conforme a la instrucción recibida.

B-DIG-SD tiene 78 estratos con UPM única; B-PRE-SD, 71; C, 8. Sus intervalos
se leen como límite inferior de la anchura verdadera, nunca como IC exacto.
No hay filas elegibles sin diseño. A-SOL1 no tiene estratos de UPM única.

El commit de congelación contiene código, entradas, recibo, números y verificación.
La tarea termina con ese commit, antes de cualquier revelación.
