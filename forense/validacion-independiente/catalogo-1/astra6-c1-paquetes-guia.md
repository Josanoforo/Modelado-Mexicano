# C1 · preparación del catálogo al corte

Preparación NO CIEGA, sin recálculos ni adopciones. Corte `4f125e709d3b3830078fe749c82068b3d55e6e70`, catálogo v1.1: 36143 filas/estimadores únicos, 68 CALC, 1210 RESULT únicos (cada tabla es un RESULT y contiene muchos estimadores). No hay reutilizaciones de la misma identidad CALC/RESULT/registro en este corte. Sus 36 referencias habilitantes se desglosan en 21 objetos de decisiones.tsv, 14 FP firmadas y 1 encargo archivado; no son un conteo de filas de decisiones del programa. El catálogo no trae el mapeo de afirmaciones: su conteo no se inventa ni se equipara a estimadores.

9 paquetes con documentación y entradas disponibles (3371 estimadores); 59 paquetes incompletos (32772 estimadores), con faltantes específicos en cada faltantes.json. El primer lote, ENDIREH 2021 comunitaria (100 estimadores), está disponible fuera del clon y pasó la prueba de separación local. No se lanzó una sesión de recálculo. Todos los estados del universo son NO-EVALUADO; las validaciones históricas no se transfieren por analogía.

- [Universo](universo.tsv): identidad, adopción, paquete y estado por fila; cero valores objetivo.
- [Paquetes](paquetes/): un contenedor `<paquete>-entradas.tar.gz` por lote, con las entradas y su manifiesto SHA-256 interno; lotes.json fija también el hash del contenedor. Al materializar se recuperan nombres internos comunes en una carpeta fuera del clon.
- [Orden y comandos](lanzamientos.md): lanzamiento nuevo por paquete y revelación posterior.
- [Lotes y faltantes](lotes.json): partición exhaustiva y disponibilidad.
- preparacion/: materiales NO ENTREGABLES al validador: catálogo con esperados, adopciones, hashes productores y procedencia de las extracciones. ubicaciones.local.json está gitignorado; el resolver reconstruye las ubicaciones si el archivo no existe.

`python3 tools/validacion/astra6_paquetes.py --verifica` comprueba cobertura, hashes, puntos contra resultados sellados, identidad de raw disponibles y ausencia de archivos productores en entradas. El escáner textual detecta patrones conocidos, no cualquier filtración semántica; se complementó con revisión dirigida del primer paquete y de las specs seleccionadas. Las extracciones conservan líneas/rangos y supresiones en preparación, sin completar métodos desde código. Las omisiones de contenido mixto siguen como faltantes; no se diagnostican como ausencia de dato ni se adjudica NO-RECALCULABLE sin reconstrucción real.

Las causas compartidas son acceso documental no identificado, método remitido a código o tablas externas, tolerancia previa ausente, y reservas. ENIF 2024 contiene crédito reservado en el ZIP: exige proyección autorizada antes de entregar datos; estos paquetes quedan INCOMPLETO. ENDIREH 2006 necesita los cuestionarios sin tabulados; ENUT necesita eliminar N observado de una extracción sucesora. Nada abre nuevas reservas. Que un archivo esté hasheado no autoriza todos sus campos.

La disponibilidad se comprobó por ids sobre el manifiesto y el corpus montado, sin abrir miembros individuales del raw. Documentos no identificados son una brecha de preparación, no una afirmación de ausencia en todas las raíces. Los paquetes no tienen referencias de valores esperados, helpers numéricos, código productor, reports, historial, conversación ni encargos de dirección. Los originales mixtos se conservan fuera de entradas.

El comparador conserva la tolerancia numérica previa. Coincidencia de intervalos aleatorios y equivalencia estadística son preguntas distintas: no se relajan umbrales con los resultados. La preparación permite lanzar el primer lote y completar los faltantes de los restantes; no permite declarar validación total ni tasa global. Recibo técnico de Claude pendiente.
