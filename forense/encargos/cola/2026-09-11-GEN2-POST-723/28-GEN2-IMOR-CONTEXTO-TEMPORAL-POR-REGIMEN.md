# 28 · GEN2 · IMOR: contexto temporal por régimen

ACTO: GEN2-IMOR-CONTEXTO-TEMPORAL-POR-REGIMEN  
ENTORNO: NUBE  
Estado de despacho: **EJECUTABLE TRAS MERGE DE #723**.  
Resultado: análisis reproducible de la serie publicada, con gráficos, cambios y dispersión dentro de cada régimen.


## Contrato de ejecución

Repositorio: `Josanoforo/Modelado-Mexicano`. Este documento es un encargo autónomo: no requiere la conversación previa.

Al despacharlo, Jonás autoriza el alcance expresamente indicado, su implementación, comprobación dirigida, archivo del encargo, commits, push y apertura/actualización de PR. **La fusión corresponde a Jonás.** Una recomendación metodológica ajena a este alcance no queda firmada.

Lee `AGENTS.md` y las instrucciones aplicables. Usa worktree y rama propios; reporta ruta absoluta, rama, HEAD y estado inicial. Comprueba en `origin/main` y PR abiertos qué parte ya existe. Si otro trabajo resolvió el objeto, consúmelo y concilia el residual; no lo dupliques. No reconstruyas el historial completo.

Los PR predecesores abiertos son dependencias, no hechos consolidados. Puedes preparar el encargo desde ahora; ejecuta sus fases dependientes sobre el commit efectivo fusionado. Resuelve conflictos de integración ordinarios dentro de la tarea. Si el entorno necesario falta, resuelve su acceso antes de la fase productiva y evita presentarla como terminada.

Reutiliza registros, resolvedores, escritores canónicos y herramientas existentes. No reescribas artefactos sellados, datos ajenos ni historial compartido. Un resultado sucesor lleva su propia identidad. Conserva replay, evidencia independiente y reservas existentes al regenerar proyecciones.

La validación debe responder riesgos concretos del resultado. Ejecuta las comprobaciones dirigidas y gates aplicables; no amplíes el alcance para limpiar CI heredada. Una vez suficientemente comprobado, entrega el resultado.

Cierra la cadena vigente: encargo → implementación/resultado → evidencia → registros y vistas pertinentes → nota de cierre → ADR/L0/rótulo cuando corresponda → PR. Usa IDs disponibles al integrar, sin reservar números desde este documento. Cierra sólo obligaciones acreditadas; conserva residual, causa y siguiente acción. No confundas commit, merge, validación, adopción y nueva medición.

No envíes mensajes/formularios externos, aceptes compromisos institucionales ni realices compras desde este encargo. La descarga pública y el uso de accesos previamente autorizados sí pueden avanzar. Los secretos y microdatos permanecen fuera de Git según el contrato del corpus.


## Autoridad científica concreta

El despacho autoriza analizar descriptivamente la tabla Banxico de #723 y registrar los derivados. No autoriza convertir IMOR en probabilidad individual, calibrar scoring alternativo, estimar causalidad ni declarar una validación de predicción. Se analiza el artefacto publicado en Git; CAJA sólo es necesaria si aparece una discrepancia material con el original.

## Datos y pregunta

Entrada principal: `data/fuentes-financieras-20/banxico-imor-consumo-mensual.csv`, propuesta por #723. Contiene 123 meses, 2016-01..2026-03, y cinco productos, con 615 filas en ese corte.

Pregunta: ¿cómo varían nivel, cambios y dispersión de IMOR por producto dentro de regímenes metodológicamente comparables, y qué contexto aporta a R1.6 sin atribuirle riesgo individual?

Consumir la nota de cierre de #723 y las notas de la publicación. Mantener separada la foto CNBV R16 de diciembre de 2021. Banxico no se renombra R16.

## Fase 1 · Congelar definición y ventanas

Fija la versión del CSV, hash, corte y universo. Registra las inclusiones/exclusiones institucionales declaradas y la agrupación ABCD.

Separación inicial acreditada: antes de enero de 2022 y desde enero de 2022 por IFRS9. Verifica otras rupturas documentadas. Una ruptura adicional cambia el tramo comparable, no se ignora para obtener una curva continua.

Fija antes de calcular:
- nivel mensual por producto;
- cambio mensual en puntos porcentuales dentro del mismo régimen;
- cambio interanual sólo cuando ambos extremos pertenecen al mismo régimen;
- media temporal, mediana, mínimo/máximo y sus fechas por producto y régimen;
- dispersión temporal del nivel y de los cambios, con definición explícita.

No agregues productos con promedio simple como si fuera IMOR total: usa la serie de consumo total publicada. No llames probabilidad ni error estándar de encuesta a la dispersión mensual.

## Fase 2 · Ejecutar y explicar

Produce tablas de nivel, cambios y resúmenes por régimen. Identifica diferencias aritméticas en pp y porcentajes relativos sin mezclarlos. Conserva meses sin cambio calculable al inicio de cada régimen.

La media temporal pondera meses de forma uniforme; no representa un ratio agregado de saldos si no se dispone de sus denominadores. Los extremos son descriptivos del periodo observado. No uses los mismos meses para vender una selección de modelo y una evaluación independiente.

Entrega gráficos exportables con unidad, universo, periodo y ruptura visible. Evita unir gráficamente ambos regímenes como si fueran una sola definición. Incluye como mínimo nivel por producto y cambios mensuales comparables.

## Fase 3 · Producto para el proyecto

Entrega una lectura de resultados de máximo dos páginas:
- niveles y variabilidad observados;
- comparaciones permitidas dentro de régimen;
- qué cambió en la definición en 2022;
- relación posible con contexto crediticio de R1.6;
- qué dato faltaría para una calibración individual.

Prepara una ficha de consumo contextual: unidad de saldos, agregado bancario, periodo, fuente y usos excluidos. No insertes estos valores en un consumidor Bernoulli de persona ni sustituyas una regla de scoring.

Si el contrato canónico admite estos estadísticos como CALC, intégralos por esa ruta. En caso contrario usa el artefacto analítico vigente; no fabriques una nueva clase de medición para incrementar el contador.

## Fase 4 · Comprobación y cierre

Verifica llaves, continuidad del corte, ausencia de cruces de régimen y varias operaciones numéricas de referencia. No repitas toda la adquisición de #723 ni una tercera descarga por rutina.

Entrega script, tablas, gráficos, ficha contextual, nota y PR. NC-0163 permanece satisfecha por la alternativa oficial tras #723. No reabrirla por faltar R16 exacto; tampoco cerrar N34 o adoptar R1.6 por este análisis.

## Dependencias y convivencia

Requiere #723 fusionado. Compatible con 27, 29 y 30. Lee las tablas de #723 sin reescribirlas; usa una carpeta de salida propia. No modifica cron, motor, microdatos ENSAFI ni diseño F5.
