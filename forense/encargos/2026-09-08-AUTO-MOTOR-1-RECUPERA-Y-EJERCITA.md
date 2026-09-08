# Propuesta de ejecución 1 · Motor ejecutable y prueba automática

Rótulo propuesto: `ACTO AUTO-MOTOR-1 · RECUPERA-Y-EJERCITA`  
Proyecto: `Josanoforo/Modelado-Mexicano`  
Fecha de preparación: 8 de septiembre de 2026  
Base comprobada: `origin/main = fbd847deee91c3e3efe283bb2f5921addcdda3a9`, merge del PR #615.

Este documento es un encargo listo para entregar al ejecutor. Su preparación no significa que el trabajo esté ejecutado, aprobado en PR o fusionado. Los nombres nuevos aquí indicados son propuestas; comprobar colisiones antes de crearlos.

## Objetivo y resultado útil

Recuperar la ejecución del motor matricial reconocido por el PR #615 y conectar una prueba automática sobre las entradas reales versionadas del repositorio. La entrega debe cargar la procedencia y la matriz B, ejercer la evaluación de las tres celdas semilla y detectar una futura regresión de esa ruta.

El resultado útil es un motor que se puede ejercer, con salida explícita por celda, y una prueba que impide volver a perder esa capacidad inadvertidamente. No se exige obtener un veredicto sustantivo favorable: un resultado nativo de insuficiencia de evidencia puede ser correcto. Una excepción de infraestructura o la omisión de la evaluación no equivalen a haber evaluado una celda.

## Premisas verificadas

- PR #615 revoca D11: `milpa/src/**` ya no puede descartarse por aquella declaración de «scaffold histórico».
- `procedencia.cargar()` falla en la base indicada con `ClaseDesconocida` para `REFUTADO-POR-COTA`. El PR documenta también `EVIDENCIA_EXPERIMENTAL_TERCEROS`.
- El CALC sellado `data/corrida0/CALC-MOTOR-celdas-semilla/` conserva `RESULT-MOTOR-ESTADO-B = NO-EJECUTABLE`. Ese diagnóstico histórico se preserva.
- La regla refutada conserva `[0.91, 0.09]` en el YAML para trazabilidad; su presencia no autoriza su consumo.
- La evidencia de terceros de `EXP-COMPARTAMOS-1` sostiene una dirección y declara que no calibra ni sustituye la magnitud vigente. Tiene `cita` y `llave_id`.
- Ya existen pruebas `tests/test_motor_*.py`. `tests/check.py` no descubre automáticamente cualquier archivo nuevo de pruebas.

## Inicio del ejecutor

1. Leer `AGENTS.md` y las instrucciones operativas vigentes. Reportar ruta absoluta, rama, HEAD y estado del árbol. Usar un worktree limpio y una rama propios.
2. Actualizar la referencia de `origin/main` y comprobar las premisas materiales. Si existe una reparación o un PR equivalente, identificarlo y completar solo lo que falte. Un PR abierto no sustituye una reparación fusionada.
3. Leer este encargo completo. Consultar únicamente las decisiones que fundamentan las dos clases y la revocación de D11; no abrir una auditoría histórica general.
4. Reproducir el fallo vigente con una llamada de lectura a `procedencia.cargar()`. Registrar el estado inicial de `corrida0 status` para explicar cualquier cambio posterior.

## Perímetro

Implementación principal: `milpa/src/clases.py`, `milpa/src/procedencia.py` y las pruebas del motor afectadas. Se permite modificar `milpa/src/matriz.py` o `milpa/src/motor.py` únicamente si la ruta real necesita respetar el tratamiento de esas clases y no basta con corregir el cargador.

Automatización: un punto de entrada de prueba, preferentemente reutilizando pruebas existentes, y `.github/workflows/verify.yml` para invocarlo. Usar dependencias ya declaradas; ampliar `requirements.txt` solo ante una necesidad material demostrada.

Evidencia: un nuevo directorio CALC sucesor, sus vistas derivadas mediante herramientas existentes y una nota de cierre breve. Registrar únicamente las reservas y referencias de cierre exigidas por el flujo vigente.

Para resolver `NC-0022`, se incluye una revisión textual acotada de E5-0/E5/E6 y otros encargos posteriores a ADR-396 que citen D11. Si hay una premisa operativa activa incorrecta, corregir su fuente maestra y sincronizar la cola con la herramienta existente. Los encargos consumidos se preservan; una corrección se registra como tal, no reescribiendo la instrucción histórica.

Quedan fuera: recalibrar parámetros, adjudicar evidencia nueva, cambiar umbrales o puntuaciones, ampliar segmentos u olas, ejecutar las 224 corridas L, introducir un orquestador general, modificar CALC sellados o activar adopciones automáticas.

## P1 · Reparación semántica mínima

Implementar reconocimiento explícito de ambas clases y conservar su texto original, identidad y referencia. Mantener el criterio de prefijo más largo del clasificador y el error ante cualquier clase desconocida nueva. No introducir un caso por defecto que admita todo.

Contrato de tratamiento:

| Clase | Carga y trazabilidad | Uso numérico |
|---|---|---|
| `REFUTADO-POR-COTA` | Se reconoce y conserva junto con el motivo de refutación. | No reingresa el prior refutado como parámetro utilizable ni mediante la clase implícita del bloque que lo contiene. No convertirlo en cero, pendiente genérico o asignado vigente. |
| `EVIDENCIA_EXPERIMENTAL_TERCEROS` | Se reconoce como clase propia; comprobar `cita` y `llave_id` conforme a su contrato vigente. | Para la entrada actual, conservar su alcance de corroboración de dirección. No extraer un número del texto para transformarlo automáticamente en coeficiente de B, probabilidad o magnitud calibrada. |

Inspeccionar tanto la lista de entradas como los accesos efectivos a `procedencia.crudo`: cambiar solo `consumibles()` no protege lectores que consuman el YAML por otra vía. En particular, verificar si la clase explícita y la del bloque producen dos representaciones contradictorias de la misma entrada refutada; corregir el caso por precedencia semántica, sin rediseñar toda la taxonomía.

Apoyar el tratamiento en las decisiones existentes. Si aparece una ambigüedad que exige elegir un parámetro o resolver una decisión epistemológica nueva, aislar esa celda y registrar la pregunta exacta. Completar los cambios independientes; no inventar una respuesta para declarar el motor recuperado.

## P2 · Ejecución real y corrida sucesora

1. Cargar el archivo real versionado de procedencia, sin eliminar temporalmente filas incómodas.
2. Cargar el catálogo de momentos y B mediante sus funciones vigentes.
3. Ejercer `motor.evaluar()` sobre las tres celdas semilla, con semilla fija. Usar el camino real que llega al cálculo matricial cuando los contratos de la celda lo permiten.
4. Comprobar que cada celda tiene salida identificable y que el muro AJUSTE/HOLDOUT sigue intacto. No fabricar magnitudes para superar `SinMagnitud` ni sustituir una excepción inesperada por un resultado tranquilizador.
5. Crear una corrida sucesora con la convención de identificación y parentesco aceptada por el esquema vigente. Elegir el nombre libre en ese momento. No suponer que `repite_de` permite cualquier cambio de contexto: verificar su contrato antes de usarlo.
6. Declarar fuentes, código, semilla y relación con el diagnóstico anterior. Ejecutar los pasos existentes de preflight, run, verify y registro en el orden que exige el runner, respetando sus requisitos de commits limpios y sellado. Consultar su ayuda en vez de inventar flags.
7. Preservar íntegramente el CALC histórico y sus hashes. La nueva evidencia explica el cambio de estado, no lo borra.

Que esta corrida ejerza el motor reparado no la convierte automáticamente en una medición Gen2. Si sus insumos siguen dependiendo del legado, debe conservar esa clasificación, incluida la dependencia transitiva que fijó #615. Los contadores Gen2 solo cambian por derivación legítima.

## P3 · Prueba automática de la ruta del motor

Reutilizar el arnés y las pruebas existentes cuando cubran el riesgo. Si hace falta un nuevo punto de entrada, proponer `tests/test_motor_ejecutable.py`.

La prueba debe usar las entradas reales versionadas, cargar procedencia y B, evaluar las tres celdas y fallar si una de ellas deja de ejercerse. No debe admitir un `skip` o capturar `ClaseDesconocida` como éxito. Debe poder correr sin corpus privado, sin red, sin sesión de Claude y sin escribir resultados de producción.

Añadir una invocación bloqueante al workflow existente. Por sencillez y para cubrir también cambios de datos, ejecutarla en sus PR y pushes a main; no crear otro scheduler ni un filtro de rutas incompleto. Confirmar primero si una invocación equivalente ya existe.

Esta prueba de ejecutabilidad debe fallar directamente aunque la suite histórica tolere otros fallos mediante baseline. No congelar el nuevo fallo dentro del baseline para conseguir un verde.

## Validación suficiente

- Dos clases reconocidas con el tratamiento anterior; una clase inventada continúa fallando.
- Una entrada refutada dentro de un bloque ASIGNADO no reaparece como asignado consumible.
- La entrada de terceros conserva su alcance y no alimenta una magnitud no autorizada.
- Carga y evaluación reales de las tres celdas; mantener las pruebas relevantes de clases, procedencia y HOLDOUT.
- Mismos insumos y semilla conservan determinismo mediante la prueba existente aplicable.
- La prueba automática falla al introducir una clase desconocida en un fixture o copia temporal, sin modificar entradas versionadas.
- Verificación del CALC sucesor y confirmación de que el histórico permanece idéntico.
- Ejecutar una vez la suite de baseline requerida por el flujo para el cambio final; no reparar fallos heredados ajenos ni congelar otra línea base.

## Criterios de cierre

La entrega está completa cuando el motor carga, las tres celdas se evalúan, la protección está conectada a CI, existe evidencia sucesora verificable y no se reclasificó legado como Gen2.

Cerrar `NC-0023` solo si se cumplieron sus condiciones materiales; cerrar `NC-0022` solo si terminó su revisión acotada y quedaron resueltas o explicitadas las consecuencias. Identificar las reservas por su texto además del número, porque el historial tuvo colisiones de identificadores.

Si CI no pudo ejecutarse remotamente, distinguir «prueba local pasó y workflow conectado» de «CI pasó». Si hay otro bloqueo material que exige una decisión nueva, declarar entrega parcial y dejar el caso concreto, sin afirmar recuperación completa.

## Entrega del ejecutor

Una rama y un PR pequeño cuando su publicación esté autorizada por mesa; de otro modo, diff y texto de PR listos para revisión. No fusionar automáticamente.

El cierre debe indicar: causa corregida; tratamiento de cada clase; celdas efectivamente evaluadas; CALC sucesor y relación histórica; pruebas con resultado real; estado de NC-0022/0023; contadores derivados y reservas. No presentar cantidad de pruebas o documentos como avance sustantivo.

## Referencias

- [PR #615: motor matricial, revocación de D11 y diagnóstico](https://github.com/Josanoforo/Modelado-Mexicano/pull/615).
- [Procedencia en la base revisada](https://github.com/Josanoforo/Modelado-Mexicano/blob/fbd847deee91c3e3efe283bb2f5921addcdda3a9/milpa/procedencia.yaml).
- [Diagnóstico sellado](https://github.com/Josanoforo/Modelado-Mexicano/blob/fbd847deee91c3e3efe283bb2f5921addcdda3a9/data/corrida0/CALC-MOTOR-celdas-semilla/resultados.json).
- [PR #614: límites previos a E5](https://github.com/Josanoforo/Modelado-Mexicano/pull/614).
