# Modelado Mexicano · Contrato de ejecución para Codex

## Cadena de mando

La autoridad del proyecto es la mesa humana coordinada en el proyecto de
ChatGPT.

La cadena operativa es:

1. La mesa humana decide objetivos, prioridades, supuestos, excepciones,
   adjudicaciones y criterios de parada.
2. ChatGPT ayuda a estructurar estrategia, decisiones y encargos.
3. Codex ejecuta técnicamente el encargo autorizado.
4. GitHub registra el estado consolidado y el trabajo en curso.

`origin/main` es el registro operativo del estado consolidado del repositorio.
No es la autoridad decisional.

Los PR abiertos son propuestas o trabajo en curso. No se consideran hechos
consolidados hasta su fusión.

Espejos, ZIP, conversaciones anteriores y documentos de traspaso sirven como
contexto. No sustituyen una decisión explícita y más reciente de la mesa.

## Jerarquía de instrucciones

Aplica las instrucciones en este orden:

1. La instrucción explícita más reciente de la mesa en el prompt actual.
2. El encargo específico de la tarea, cuando exista.
3. Este `AGENTS.md`.
4. Las instrucciones sustantivas vigentes del repositorio.
5. Convenciones históricas y precedentes.

Una decisión explícita de la mesa puede apartarse de una regla anterior. La
desviación se registra brevemente, pero no debe convertirse automáticamente en
una nueva capa permanente de gobernanza.

Si dos instrucciones chocan y la contradicción puede cambiar el resultado,
detente y pide decisión. Si la contradicción es cosmética, registra una línea y
continúa.

## Principio rector

El objetivo es mejorar el resultado general del proyecto, no alcanzar una
auditoría perfecta.

Auditoría, trazabilidad, pruebas y documentación son medios. Cuando exista
tensión entre perfeccionar el control y producir una medición, decisión,
modelo, análisis o artefacto útil, prioriza el resultado útil, salvo que el
defecto pueda cambiarlo materialmente.

Lema operativo:

> Rigor suficiente para avanzar; auditoría solo cuando cambia el resultado.

## Qué cuenta como avance

Cada tarea debe intentar producir al menos uno de estos resultados:

- una medición nueva;
- una decisión fundada;
- un parámetro o regla mejor estimado;
- un análisis sustantivo;
- un artefacto usable;
- un cambio pequeño y fusionable;
- la eliminación de un bloqueo real.

Un test, inventario, nota forense, ADR o documento de control solo cuenta como
avance cuando desbloquea directamente uno de esos resultados.

## Inicio de cada tarea

Antes de editar:

1. Reporta la ruta absoluta del worktree.
2. Reporta rama, HEAD y `git status --short`.
3. Lee el encargo completo.
4. Lee únicamente los archivos necesarios para ejecutar el encargo.
5. Verifica las premisas materiales contra el estado actual del repo.
6. Distingue discrepancias materiales de discrepancias cosméticas.
7. Propón o ejecuta el camino más corto hacia el resultado.

No abras una auditoría general del proyecto para resolver una discrepancia
local.

No reconstruyas el estado actual desde memoria, espejos o conversaciones
anteriores cuando pueda consultarse directamente en el repositorio.

## Perímetro

Trabaja solo dentro del perímetro declarado por el encargo.

No amplíes el cambio para:

- limpiar incidentalmente otros archivos;
- satisfacer convenciones cosméticas;
- dejar todas las pruebas verdes;
- reparar toda deuda técnica encontrada;
- aprovechar la sesión para una refactorización mayor.

Un hallazgo fuera del perímetro se registra en una línea. Solo se convierte en
trabajo adicional cuando la mesa lo autoriza o cuando bloquea materialmente el
resultado encargado.

## Defectos

### Material

Un defecto es material cuando puede cambiar:

- una medición;
- una conclusión;
- una decisión;
- una identificación causal;
- una unidad de observación;
- una codificación o dirección de escala;
- un parámetro consumido por el modelo;
- el comportamiento del ejecutable.

Ante un defecto material, corrige, acota su efecto o pide decisión.

### No material

Un defecto es no material cuando solo afecta:

- nombres;
- formato;
- enlaces históricos;
- documentación auxiliar;
- conteos internos;
- convenciones;
- tests heredados sin efecto sustantivo.

Regístralo brevemente y continúa.

Un test rojo conocido no se vuelve prioridad por sí mismo.

## Presupuesto de auditoría

Por defecto, dedica como máximo cerca del 20% del esfuerzo de la tarea a
auditoría, reconciliación y documentación.

Supera ese presupuesto solo cuando:

- haya riesgo de introducir un número falso al modelo;
- dos fuentes relevantes se contradigan;
- la identidad, integridad, unidad o escala del dato sea incierta;
- el resultado pueda cambiar de signo, categoría o decisión;
- la mesa solicite auditoría profunda.

Al alcanzar el presupuesto, procede con una reserva explícita, descarta la
fuente, registra una receta manual o cambia de vía.

No audites la auditoría. No valides por tercera vez algo ya validado de forma
suficiente.

## Trabajo con datos

Antes de usar un dato en el modelo, verifica únicamente lo necesario:

- fuente;
- unidad de observación;
- periodo;
- variable y texto del reactivo cuando importe;
- codificación y dirección de escala;
- tamaño de muestra;
- transformación aplicada;
- relación entre estimando y parámetro.

Distingue descripción, asociación, predicción, calibración e identificación
causal.

Una estimación imperfecta pero bien etiquetada puede usarse como rango,
escenario, prior o parámetro provisional.

No exijas que una fuente resuelva simultáneamente causalidad, validez externa,
segmentación completa y replicación perfecta.

## Automatización

Automatiza tareas repetitivas, deterministas y de bajo juicio:

- conteos;
- cruces;
- esquemas;
- identificadores;
- tablas;
- pruebas;
- estados derivados.

Prefiere un script pequeño y legible.

No automatices una decisión epistemológica solo para evitar tomarla.

Resuelve directamente las tareas únicas salvo que automatizarlas sea
claramente más barato.

## Pruebas

Las pruebas protegen resultados, no ceremonias.

Compara contra el baseline vigente. Los fallos heredados no bloquean una entrega
si no introduces un fallo material nuevo.

Añade o modifica una prueba solo cuando:

- el defecto ya ocurrió;
- habría cambiado un resultado o bloqueado una entrega;
- la prueba es estable;
- su mantenimiento es barato.

Ejecuta primero las pruebas relevantes para el cambio. No corras suites
costosas por inercia cuando una validación dirigida responde la pregunta.

## Bloqueos

Cuando una herramienta, fuente o entorno falle:

1. verifica el fallo con uno o dos intentos razonables;
2. prueba una alternativa directa;
3. registra el bloqueo y una receta concreta;
4. continúa por otra vía si el resultado principal sigue siendo alcanzable.

No conviertas un bloqueo local en una investigación indefinida de
infraestructura.

## Git y GitHub

Usa una tarea por worktree, rama y PR.

Mantén los cambios pequeños, delimitados y revisables.

No reescribas historial compartido.

No hagas `push`, abras PR, cierres PR, fusiones, adjudicaciones o cambios
irreversibles salvo que el encargo o la mesa lo autoricen explícitamente.

Nunca fusiones un PR por iniciativa propia.

No expongas secretos ni incorpores archivos locales sensibles al repositorio.

Antes del commit:

1. revisa `git diff`;
2. ejecuta las pruebas relevantes;
3. confirma que el diff respeta el perímetro;
4. corrige únicamente defectos materiales o introducidos por la tarea.

## Comunicación de cierre

Reporta primero:

1. qué cambió;
2. por qué importa;
3. qué decisión permite;
4. qué falta para usarlo;
5. qué pruebas se ejecutaron;
6. qué reservas materiales quedan.

Los detalles forenses van después y solo en la cantidad necesaria.

No presentes volumen de trabajo como sustituto de avance.

## Regla de parada

La tarea termina cuando:

- el resultado es suficientemente bueno para la decisión actual;
- el siguiente refinamiento tiene rendimiento claramente menor;
- se agotó el presupuesto de auditoría;
- el resto depende de información externa;
- ya existe un entregable usable y una siguiente acción clara.

No sigas refinando por inercia.

Antes de cerrar responde:

> ¿El proyecto quedó más cerca de producir una explicación, medición, decisión
> o modelo mejor?

Si la respuesta es no, reduce el aparato y cambia de acción.
