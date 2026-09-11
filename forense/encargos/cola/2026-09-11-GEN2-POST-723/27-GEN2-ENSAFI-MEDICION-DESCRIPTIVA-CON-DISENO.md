# 27 · GEN2 · ENSAFI: medición descriptiva con diseño

ACTO: GEN2-ENSAFI-MEDICION-DESCRIPTIVA-CON-DISENO  
ENTORNO: CAJA  
Estado de despacho: **EJECUTABLE TRAS MERGE DE #723**.  
Resultado: cálculo registrado de atraso y afrontamiento, con denominadores explícitos e incertidumbre acreditada donde el diseño lo permita.


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

El despacho acepta las clases amplias y los estimandos de abajo **para descripción de ENSAFI 2023**. Autoriza fijar spec, calcular y registrar resultados. No autoriza asignarlos a N34 como efecto causal, identificar BNPL/usura con una clase amplia, ni convertir tasas de hogar en riesgo individual. La adopción de un parámetro nuevo conserva su decisión propia.

## Antecedentes que se consumen

#723 obtuvo/reutilizó datos y documentación de ENSAFI y publicó 4 puntos de hogar más 9 de persona. Ya no hay que buscar esos archivos ni repetir la adquisición. El cálculo propuesto es una **formalización y extensión de resultados conocidos**, no un pre-registro ciego ni una muestra independiente.

Leer primero:
- Nota `2026-09-11-GEN2-FUENTES-FINANCIERAS-CONTINUACION-EFECTIVA-cierre.md`.
- `tools/extrae_fuentes_financieras.py`, funciones ENSAFI.
- `data/fuentes-financieras-20/ensafi2023-atraso-deuda-producto-hogar.csv`.
- `data/fuentes-financieras-20/ensafi2023-deuda-y-afrontamiento-persona.csv`.
- Manifiesto: base CSV, descriptor, cuestionario, diseño y presentación ENSAFI.
- Infraestructura de CALC, especificación, replay y validación vigente.

## Fase 1 · Spec antes de extender el análisis

Resuelve el corpus y verifica identidades. Fija población, tablas, llaves, factores, dominios, códigos válidos/desconocidos y método antes de estimar incertidumbre.

Estimandos principales:
1. Cuatro tasas de hogar: `P4_8_j=1` entre `P4_7_j=1` y respuesta válida de atraso, j=1..4. Factor `FAC_HOG`. Conservar las clases literales; “formal” es una agrupación de productos.
2. Atraso general de persona: `P6_7=1` entre personas con deuda según `P6_8=1..4`, con regla explícita para respuestas no válidas. Factor `FAC_ELE`. P6_7 no identifica producto ni una ventana temporal explícita.
3. Ocho estrategias: `P6_10_k=1` entre `P6_9=2` y respuesta válida en cada estrategia, k=1..8. Son respuestas múltiples.

No añadas segmentaciones exploratorias por encontrar diferencias atractivas. Este lote cubre los 13 estimandos nominales. Si la lectura oficial contradice una codificación de #723, documenta la corrección antes de continuar, conserva el resultado anterior y mide su efecto.

## Fase 2 · Estimar desde el diseño correspondiente

Usa `EST_DIS` y `UPM_DIS` con la documentación oficial de cada tabla y el factor correcto. Verifica si los identificadores necesitan anidamiento y conserva la información de diseño necesaria para dominios. No elimines observaciones fuera del dominio antes de construir la varianza.

Para cada estimando publica: n expuesto, n válido, desconocidos y su masa; numerador/denominador ponderados; punto; EE/IC95 y grados de libertad cuando estén acreditados. Fija el procedimiento del intervalo antes de inspeccionar sus resultados. Trata explícitamente PSU singleton, fronteras p=0/1 y denominador nulo; no fuerces precisión con agrupaciones inventadas.

Si un componente del diseño no está acreditado, conserva punto y causa de incertidumbre no disponible. No sustituirla por cero ni por una receta arbitraria. Resuelve lo que sí admite la documentación en esta misma tarea.

## Fase 3 · Contraste y productos utilizables

Contrasta los puntos con #723 y la publicación oficial comparable. El 27.3% publicado es un contraste de redondeo, no un objetivo al que ajustar la codificación. Explica cualquier discrepancia por identidad, universo, factor, no respuesta o transformación.

Entrega:
- CALC/spec y resultados con identidad propia.
- Tabla legible de los 13 estimandos y precisión disponible.
- Lectura breve: qué permite decir ENSAFI sobre atraso/afrontamiento y qué no identifica.
- Ficha de consumo por RESULT: unidad, población, periodo, uso descriptivo y restricciones.
- Ejecutor reproducible y verificación suficiente de ponderación, dominio y faltantes.

No compares “agiotista vs formal” como efecto causal. No sumes clases de deuda ni estrategias como categorías excluyentes.

## Fase 4 · Registro y cierre

Integra mediante la vía canónica. Distingue extracción anterior, extensión analítica, medición registrada y adopción. El contador se deriva del contrato vigente; no contabilices 13 filas como 13 nuevas fuentes o muestras.

NC-0164 conserva el residual producto exacto/costo/fricción/daño causal. No se cierra completo por estas tasas. El PR debe dejar una propuesta de uso descriptivo concreta y sus límites, sin imponer otra sesión sólo para producir las tablas.

## Dependencias y convivencia

Requiere #723 fusionado. Puede correr junto con 28, 29 y 30. Escribe su CALC y evidencia; concilia registros compartidos por identidad. No modifica el extractor financiero general salvo una corrección material indispensable y coordinada. No cambia el motor ni las capturas F5.
