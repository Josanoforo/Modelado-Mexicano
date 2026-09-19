# GEN2-ENIGH2022-PERFIL-ESTRUCTURAL-CLI-1

## Cabecera y autorización de lanzamiento

- Repositorio: `Josanoforo/Modelado-Mexicano`.
- SHA de redacción: `8e455bd6a3870566d6776fef19834c4da16d2fa9`, leído el 19/sep/2026.
- ENTORNO: CAJA, Codex CLI con corpus local. No ejecución de microdatos en nube.
- Una sesión, un worktree, una rama: `codex/gen2-enigh2022-perfil-estructural-cli-1`.
- Ejecutor: Codex CLI, modelo de razonamiento disponible para medidores. No trasladar este encargo a una sesión Claude que esté ejecutando otro objeto.
- Entrega: medición descriptiva, CALC sellado, publicación canónica y PR abierto sin merge. Al pegar este encargo se autoriza commit, push y apertura de ese PR; no merge ni cambios de gobierno.
- Propuesta de CALC: `CALC-ENIGH2022-PERFIL-ESTRUCTURAL-0001`, condicionada a comprobar unicidad antes del congelamiento en todas las ramas remotas y la historia pertinente.
- Contador: `PENDIENTE-DE-MESA` conforme al contrato vigente; no inventar una firma de `cuenta_gen2=SI` ni una adopción. Reportar por separado nuevas mediciones registradas y contador adjudicado.

Este encargo implementa la separación acordada con Jonás: «Codex mide; Claude gobierna y construye el motor; mesa adopta con su merge». Las reservas propias se entregan en la nota; Claude hace el recibo. No hay una firma previa de mesa sobre los resultados que todavía no se han medido.

## Resultado buscado

Medir la distribución de los descriptores estructurales observables en ENIGH 2022 a nivel persona y el soporte de su conjunta observada. Entregar insumos numéricos que permitan a dirección decidir cómo construir la composición poblacional del modelo, sin implementar π, calibrar pesos, adjudicar cortes ni actualizar el motor.

Tres piezas en un solo encargo: marginales y cobertura; conjunta de cuatro descriptores inequívocos; distribución nativa de residencia si su pregunta y universo quedan acreditados antes de abrir respuestas. Una limitación exclusiva de residencia no bloquea las otras dos piezas.

## Demanda y comprobación previa

Fuentes leídas directamente en el SHA indicado:

1. `data/corrida0/demanda-corridas.tsv`: CORR-0076 enlaza los seis descriptores de π; `demanda-resultados.tsv`, RES-0165 a RES-0170, declara como consumidores los cortes de `milpa/src/celdas.py`.
2. `milpa/src/pi.py`: `construir_pi()` sigue sin fuente cargable. Esa falta no autoriza modificar el módulo.
3. `milpa/src/celdas.py`: edad ya tiene corte declarado; migración sigue pendiente. La fila vieja de demanda que atribuye ambos pendientes a FP-53 no gobierna el estado actual. No abrir una corrección documental por esa divergencia.
4. `forense/notas/2026-07-31-p1-enigh-semilla.md`: documenta variables y uniones, pero dice expresamente que NO midió cobertura de perfiles ni abrió filas de microdatos. Su conclusión de disponibilidad documental no acredita soporte empírico.
5. Las ofertas ENIGH revisadas en `corridas.tsv` y sus specs cubren remesas y líneas base temporales; no encontré en ese conjunto una medición del perfil aquí solicitado. No se declara inexistencia universal: hay que verificar contenido e historia antes de ejecutar.
6. `data/INFRAESTRUCTURA-v1_0.md` describe la publicación a través de `corrida0`; los derivados no se editan a mano.

Al redactar no había PR abiertos y la única rama remota era main. Repite la comprobación al comenzar. Ejecuta `python3 tools/corrida0.py demanda` en lectura y verifica ofertas por contenido, no solo por nombre CALC: `segsoc`, `tam_loc`, `est_socio`, `conex_inte`, `celular`, `residencia`, composición poblacional y perfil. Consulta las specs/resultados que la búsqueda encuentre. Si la medición equivalente ya existe, entrega su referencia y no la repitas.

**Relación con la demanda:** una proporción poblacional NO sustituye un corte categórico. No declarar relevo directo de RES-0165…0170 ni escribir que estos slots quedan satisfechos. La entrega aporta la distribución y soporte de los atributos que esos consumidores requieren. El enlace y uso posterior corresponden a Claude/mesa.

## Compuerta y congelamiento

Lee AGENTS.md y las instrucciones aplicables. Reporta ruta, rama, HEAD y estado local. Comprueba las compuertas de medición vigentes. Usa una rama nueva desde main; no reabras sesiones canceladas ni heredes sus cambios.

Resuelve el payload `enigh2022_nc_csv` y verifica hash/tamaño por los mecanismos existentes. Una raíz no configurada no prueba ausencia: monta el corpus compartido sin versionar rutas privadas ni microdatos. Localiza documentación ya disponible y acredita ponderación, universo, diseño, variables, códigos y preguntas con sus páginas/miembros. La nota P1 es una guía histórica; revalida sus definiciones.

Antes de abrir respuestas congela en COMMIT-1 la spec humana con hash, el contrato YAML, el medidor autocontenido y pruebas sintéticas. Congela también los estados de no estimación, el tratamiento de faltantes, uniones, método de incertidumbre y cada RESULT. El primer resultado producido por ese procedimiento es el que se reporta. COMMIT-2 publica ejecución, resultados y sello; no modifica la spec anterior. Si aparece un defecto material, preserva el intento y usa el procedimiento de sucesión, nunca parchees una corrida sellada.

No consumir reservas de ENIF 2024, ENCIG 2025 o ENVIPE 2025 ni momentos HOLDOUT. Este trabajo describe atributos ENIGH 2022; no evalúa reglas conductuales ni el piloto 3.

## P1 — Marginales y cobertura con significado correcto

Universo principal: personas residentes de ENIGH 2022 con edad válida entre 18 y 96, declarando explícitamente esa restricción para la comparación futura con los cortes actuales. No convertir edades válidas fuera de ese rango en no respuesta. Documentar cobertura respecto del universo residente del instrumento, y las exclusiones por edad y validez, con n y masa. Aplicar las exclusiones oficiales de pertenencia al hogar/residencia que correspondan según documentación, congeladas previamente.

La base es persona: llave `(folioviv, foliohog, numren)`. Unir atributos de hogar mediante `(folioviv, foliohog)` con cardinalidad m:1 verificada. No multiplicar filas por trabajos o por partidas de ingreso. Derivar el peso de persona desde la documentación oficial; no asumir que un peso de hogar aplicado a una tabla duplicada produce un estimando de hogar.

Medir por separado:

- `segsoc`: derechohabiencia/seguridad social conforme al diccionario. Conservar el nombre del atributo; no presentarlo como una tasa oficial de informalidad laboral.
- `edad`: cuatro tramos operativos del modelo, con intervalo superior explícito 60–96 para este universo y n/masa excluidos separados.
- `tam_loc`: categorías nativas de tamaño de localidad, atributo heredado del hogar.
- `est_socio`: categorías nativas de estrato socioeconómico. No llamarlas cuartiles de ingreso ni confundirlas con `est_dis`.
- `conex_inte` y `celular`: dos distribuciones distintas de tenencia en el hogar, si su documentación confirma esas variables. No elegir una como sustituto automático de `acceso_digital`; no afirmar uso personal, smartphone o banca digital.

Para cada categoría: n sin ponderar, numerador y denominador ponderados, proporción, EE/IC cuando estén sustentados, desconocidos/excluidos, unidad, universo y fuente. Publicar cobertura válida por variable; no cambiar silenciosamente de denominador entre filas ni imputar para completar la malla.

## P2 — Conjunta observada y soporte

Medir la conjunta `segsoc × tramo_edad × tam_loc × est_socio` en el mismo registro persona. Enumerar el producto cartesiano de las categorías congeladas mediante código. Mantener tanto celdas observadas como celdas sin observaciones, diferenciando cero muestral, no estimable y combinaciones imposibles solo cuando la documentación pruebe esa imposibilidad.

Publicar para cada celda n, masa, proporción sobre el universo completo clasificable, incertidumbre sustentada y soporte de UPM. Publicar cuánto universo se pierde por requerir los cuatro descriptores válidos. No presentar la distribución de casos completos como si cubriera automáticamente toda la población.

Marginalizar la conjunta y comprobar coincidencia con marginales calculados sobre EL MISMO subconjunto completo. Informar aparte las marginales P1 que tengan otra cobertura. No fabricar la conjunta multiplicando marginales, ejecutar IPF/IPU ni reponderar. Los atributos de hogar siguen constantes entre integrantes del mismo hogar; no se interpretan como variación intra-hogar.

Esta tabla es una estimación descriptiva del perfil observado, no una nueva malla adjudicada al modelo. Las celdas vacías no demuestran ausencia poblacional ni autorizan eliminarlas de un futuro modelo.

## P3 — Residencia nativa, sin decidir el corte migratorio

La nota P1 no acreditaba el texto ni el periodo de `residencia`. Antes de abrir esa columna, busca el cuestionario/diccionario pertinente del corpus y fija pregunta, periodo de referencia, universo por edad, saltos y catálogo. Si se acredita, mide la distribución de sus categorías originales y su cobertura, sin agruparlas en «migrante/no migrante» ni sustituir el corte pendiente.

Si no se acredita, deja P3 `NO-ESTIMABLE-POR-DEFINICION-NO-ACREDITADA`, con los documentos y búsqueda examinados; no abreviar eso a «no existe». Sigue y entrega P1/P2 completos. No abrir una adquisición general ni usar la variable solo porque su nombre parece suficiente.

## Incertidumbre y control material

Usa el diseño muestral documentado, conservando el marco y calculando dominios con indicadores; no eliminar del marco hogares/UPM solo por quedar fuera de una celda. Congela un único método adecuado, con tratamiento de estratos de UPM única y valores degenerados. Si empleas réplicas, comparte el plan entre celdas y congela semilla, generador y cantidad; reporta réplicas válidas sin convertir fallos en cero. Sin diseño acreditado, reporta puntos con precisión no disponible, no un IC iid inventado.

Controles suficientes: llave persona única y joins sin expansión; exclusiones reconciliadas; particiones suman uno en su universo; conjunta marginalizada coincide con su subconjunto; contraste de puntos y denominadores mediante implementación separada para total y categorías representativas; comprobación independiente focalizada de una varianza no degenerada si se publican IC. Pruebas sintéticas para los riesgos materiales de duplicación por join, confusión hogar/persona y categorías faltantes. No dedicar la sesión a corregir tests heredados.

## Perímetro y concurrencia

Escritura autorizada: nuevo directorio CALC y sus sucesores propios si fueran necesarios; `forense/prereg-caja/ENIGH2022-PERFIL-ESTRUCTURAL-*`; `forense/analisis/enigh2022-perfil-estructural-cli-1/`; test propio `tests/test_enigh2022_perfil_estructural.py`; archivo verbatim de este encargo; nota propia de cierre; asientos propios en replay; derivados canónicos exclusivamente por comando.

**Si te encuentras escribiendo fuera de esta lista, PARA esa modificación.** No escribir `milpa/**`, herramientas generales de corrida0, `tests/check.py`, workflows, canon, firmas, decisiones, tablero, NC globales ni inventarios generales. Hallazgos propios y necesidades de adopción van en la nota, con sucesor «recibo Claude». El uso de comandos existentes para publicar derivados sí está autorizado.

## Publicación y entrega

Registra la medición en el mismo acto mediante los comandos de la casa. Replay dirigido y asiento propio antes de publicación; no usar un lote amplio para aceptar transiciones ajenas. Si hay un bloqueo del generador que requiera cambiar código de Claude, entrega evidencia concreta y la corrida preservada, sin ampliar el perímetro ni afirmar registro exitoso.

Una segunda proyección debe mantener iguales los derivados. No crear usos activos: todavía no hay consumidor adoptado. No escribir cierres de slots ni firmas. Conserva el material necesario para reproducir el cálculo en corpus y publica únicamente agregados, contratos y código.

El PR debe entregar conjuntamente las tablas marginales, la tabla de soporte/conjunta, la medición o limitación precisa de residencia, mapa RESULT→significado→demanda, ejecución/sello/replay y una lectura sustantiva breve. La primera línea de esa lectura declara universo, unidad persona, escala de proporción y evidencia (a), datos primarios en México. Distingue composición estructural de psicología y evita inferencias culturales.

Reporta qué puede usar dirección para decidir, qué no identifica la medición y qué falta para construir π. Incluye `## NO-CORRIDO / RESERVAS` y `## CONSUMIDO`. FP/ADR/NC: no asignar números, presentar necesidades concretas al recibo Claude. Termina con PR abierto y SHA final; nunca hagas merge.
