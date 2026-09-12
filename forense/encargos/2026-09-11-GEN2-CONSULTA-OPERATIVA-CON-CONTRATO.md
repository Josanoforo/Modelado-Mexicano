# 29 · GEN2 · Consulta operativa con contrato

ACTO: GEN2-CONSULTA-OPERATIVA-CON-CONTRATO
ENTORNO: NUBE
Estado de despacho: **EJECUTABLE TRAS MERGE DE #720**.
Resultado: un comando usable para consultar GEN2 desde entradas explícitas y recibir punto, alcance, procedencia o causa de no cobertura.


## Contrato de ejecución

Repositorio: `Josanoforo/Modelado-Mexicano`. Este documento es un encargo autónomo: no requiere la conversación previa.

Al despacharlo, Jonás autoriza el alcance expresamente indicado, su implementación, comprobación dirigida, archivo del encargo, commits, push y apertura/actualización de PR. **La fusión corresponde a Jonás.** Una recomendación metodológica ajena a este alcance no queda firmada.

Lee `AGENTS.md` y las instrucciones aplicables. Usa worktree y rama propios; reporta ruta absoluta, rama, HEAD y estado inicial. Comprueba en `origin/main` y PR abiertos qué parte ya existe. Si otro trabajo resolvió el objeto, consúmelo y concilia el residual; no lo dupliques. No reconstruyas el historial completo.

Los PR predecesores abiertos son dependencias, no hechos consolidados. Puedes preparar el encargo desde ahora; ejecuta sus fases dependientes sobre el commit efectivo fusionado. Resuelve conflictos de integración ordinarios dentro de la tarea. Si el entorno necesario falta, resuelve su acceso antes de la fase productiva y evita presentarla como terminada.

Reutiliza registros, resolvedores, escritores canónicos y herramientas existentes. No reescribas artefactos sellados, datos ajenos ni historial compartido. Un resultado sucesor lleva su propia identidad. Conserva replay, evidencia independiente y reservas existentes al regenerar proyecciones.

La validación debe responder riesgos concretos del resultado. Ejecuta las comprobaciones dirigidas y gates aplicables; no amplíes el alcance para limpiar CI heredada. Una vez suficientemente comprobado, entrega el resultado.

Cierra la cadena vigente: encargo → implementación/resultado → evidencia → registros y vistas pertinentes → nota de cierre → ADR/L0/rótulo cuando corresponda → PR. Usa IDs disponibles al integrar, sin reservar números desde este documento. Cierra sólo obligaciones acreditadas; conserva residual, causa y siguiente acción. No confundas commit, merge, validación, adopción y nueva medición.

No envíes mensajes/formularios externos, aceptes compromisos institucionales ni realices compras desde este encargo. La descarga pública y el uso de accesos previamente autorizados sí pueden avanzar. Los secretos y microdatos permanecen fuera de Git según el contrato del corpus.


## Autoridad y propósito

Autoriza construir o completar una entrada operativa del emisor GEN2 usando los parámetros ya adoptados. No abre F6, no calibra coeficientes, no modifica probabilidades ni emite predicciones experimentales retenidas.

#720 corrige el contrato de selección y conserva las 16 salidas directas del snapshot. El producto siguiente es poder consultarlas desde una interfaz utilizable, sin depender de generar un snapshot completo.

## Fase 1 · Elegir la entrada existente más cercana

Inspecciona sólo:
- `milpa/src/emisor.py` y su interfaz posterior a #720.
- `tools/snapshot_motor_gen2.py`.
- `tools/emite_m.py` y comandos de consulta ya existentes.
- Usos/resultados y dominios adoptados.
- Snapshot GEN2 v1.1 o sucesor vigente.

Si ya existe un comando que cumple el objetivo, amplíalo. Si no, añade un wrapper pequeño —nombre sugerido `tools/consulta_gen2.py`— sobre la interfaz vigente. No sustituir el motor E0 histórico ni convertir una herramienta de replay histórico en la ruta GEN2.

## Fase 2 · Implementar la consulta real

Contrato mínimo de entrada:
- consumidor por identidad exacta;
- propósito: consulta o transferencia;
- contexto de dominio explícito;
- objetivo/corte y selección verificable cuando corresponda;
- uso solicitado.

Ofrece ayuda/listado de consumidores y campos de dominio. No rellenes silenciosamente los datos que determinan elegibilidad a partir del resultado que se desea obtener. No infieras características personales por nombre o texto libre.

La ruta normal de este comando usa GEN2. El histórico, si se expone aquí, exige selección explícita y produce su identidad separada.

La salida JSON y lectura humana incluyen:
- estado y valor, sólo si procede;
- RESULT y fuente;
- población, unidad, evento y periodo;
- transformación y dependencia;
- aptitud, validación independiente disponible y alcance;
- motivo preciso de no cobertura;
- versión/hash del contrato y referencias utilizadas.

No hay fallback numérico legacy, imputación con cero, ni sustitución por R. Un contexto inválido o desconocido conserva su causa. Una salida de proporción poblacional no se redacta como diagnóstico o probabilidad personalizada validada.

En transferencia, usa el selector autenticado de #720. Los parámetros sueltos o un JSON que únicamente declara ser válido no pueden eludirlo.

## Fase 3 · Entregar usos operativos demostrados

Ejecuta el comando con:
1. Una consulta válida de cada familia directa disponible en el snapshot.
2. Un consumidor con dominio incompleto/falso.
3. Un consumidor legacy solicitado en GEN2.
4. La transferencia ENIGH anterior al corte que ya funciona.
5. El intento ENVIPE→remesas y una selección posterior al corte.
6. Complemento adoptado con padre/transformación y proxy solicitado para un uso no permitido.

No son nuevas celdas F5 ni una evaluación de generalización. Son recorridos de consulta sobre consumidores conocidos.

Entrega un archivo de peticiones de ejemplo y sus respuestas reproducibles. La documentación debe permitir que Jonás haga una consulta desde terminal sin escribir Python. No construyas un chatbot ni añadas llamadas LLM.

## Fase 4 · Cerrar el recorrido

Comprueba que las respuestas válidas conservan los valores vigentes y que ningún ejemplo escribe sobre capturas o snapshots sellados. Si se necesita una salida persistida, usa un destino propio y evita sobreescritura accidental.

Incluye una guía breve con comandos reales, resultado esperado y límites de interpretación. Añade sólo las pruebas necesarias para proteger esta nueva entrada y sus bloqueos materiales.

No modifiques criterios científicos para lograr que todas las consultas emitan. El criterio de éxito es una consulta utilizable y fiel al contrato, incluyendo NO_COVERAGE cuando corresponde.

## Dependencias y convivencia

Requiere #720 fusionado. Puede avanzar con 27/28/30. El encargo 30 es dueño del overlay nuevo de validación; este comando lo consume por la interfaz vigente, sin fijar totales ni exigir que todo esté PASA.

No esperes a 30 para entregar una consulta que declare honestamente el estado de validación actual. Al integrarlo, sólo vuelve a comprobar la lectura del overlay; no repitas los cálculos independientes.
