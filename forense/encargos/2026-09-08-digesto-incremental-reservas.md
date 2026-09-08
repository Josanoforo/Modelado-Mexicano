# Propuesta de ejecución 2 · Digesto incremental de reservas

Rótulo propuesto: `ACTO AUTO-DIGESTO-1 · CAMBIOS-DESDE-EL-ULTIMO-CORTE`  
Proyecto: `Josanoforo/Modelado-Mexicano`  
Fecha de preparación: 8 de septiembre de 2026  
Base comprobada: `origin/main = fbd847deee91c3e3efe283bb2f5921addcdda3a9`, merge del PR #615.

Este documento es un encargo listo para entregar al ejecutor. Su preparación no significa que el trabajo esté ejecutado, aprobado en PR o fusionado. Los nombres nuevos aquí indicados son propuestas; comprobar colisiones antes de crearlos.

## Objetivo y resultado útil

Actualizar la sección H del digesto de `/tramite` para responder: «¿Qué reservas aparecieron, se cerraron o cambiaron desde el último corte publicado?». Conservar acceso al inventario vigente y su conteo, pero evitar que toda la historia vuelva a presentarse como novedad.

Esta entrega es independiente de recuperar el motor. Puede ejecutarse primero si ese trabajo está bloqueado. Aprovecha la rutina, el generador y los digestos existentes; no necesita otro servicio, cron, canal de mensajes o base de datos.

## Premisas verificadas

- `tools/digesto_tramite.py::seccion_h()` recorre todo `forense/no-corrido.tsv` y muestra todas las filas. No calcula diferencias entre cortes.
- `NC-0008` y `NC-0013` describen este mismo hueco. La segunda señala que los digestos previos ya proporcionan una referencia histórica aprovechable.
- Los digestos identifican un HEAD de emisión. Su formato antiguo no basta por sí solo para recuperar todos los campos de una reserva, porque la tabla H muestra únicamente una selección.
- `corrida0 status` ya deriva `no_corrido_abiertas`; la leyenda del digesto que todavía llama provisional a su propio conteo está desactualizada.
- La rutina existente se documenta en `.claude/commands/tramite.md`; localizar y leer su versión vigente antes de editarla.

## Inicio del ejecutor

1. Leer `AGENTS.md`, este encargo y las instrucciones vigentes de `/tramite`. Reportar ruta absoluta, rama, HEAD y estado del árbol. Usar worktree y rama propios.
2. Actualizar la referencia de `origin/main`. Comprobar si el diff incremental ya se implementó; completar únicamente lo pendiente y distinguir PR abierto de trabajo fusionado.
3. Leer el generador, dos digestos representativos y las filas de reserva afectadas. No revisar de nuevo todas las automatizaciones del proyecto.
4. Comprobar cómo `/tramite` publica un digesto y si su árbol de entrada está limpio. Esa evidencia determina qué referencia puede representar fielmente el corte.

## Perímetro

- `tools/digesto_tramite.py`, concentrando el cambio en sección H, selección de referencia y metadatos de comparación.
- Una prueba dirigida, propuesta `tests/test_digesto_nc.py`, o su equivalente ya existente.
- Un único punto de invocación automática de esa prueba: preferir el mecanismo existente; usar `.github/workflows/verify.yml` si todavía no hay uno.
- `.claude/commands/tramite.md`, solo para documentar el contrato y los argumentos nuevos que realmente resulten necesarios.
- Un digesto de demostración generado con la herramienta y una nota breve de cierre. Las filas NC correspondientes y los archivos de cierre exigidos por el flujo vigente.

Modificar `tools/corrida0.py` solo si es imprescindible exponer un contador ya calculado sin duplicar su significado; preferir consumir una interfaz existente.

Quedan fuera: comparar valores numéricos del modelo, implementar `corrida0 delta` o `vigencia`, cambiar el scheduler, reconstruir todo el historial de reservas, enviar mensajes y cerrar automáticamente reservas de otros actos.

## P1 · Contrato de referencia y determinismo

La unidad de comparación es un corte de reservas, no un día del calendario. Deben funcionar dos ejecuciones el mismo día y también varios días sin ejecución.

Diseño preferido, usando Git y los digestos existentes:

1. Cada digesto nuevo registra el SHA completo del árbol de entrada y el hash del contenido de `forense/no-corrido.tsv` observado. Distinguir ese SHA del commit posterior que publica el documento.
2. Seleccionar el último digesto completado y versionado disponible en el historial del destino de salida, anterior a la nueva emisión. Resolverlo una vez al comenzar y fijarlo durante toda la generación. No escoger por fecha de modificación del sistema de archivos.
3. Recuperar el TSV anterior desde el SHA de entrada declarado por ese digesto. En digestos antiguos, admitir el SHA corto únicamente si resuelve de forma inequívoca. No reconstruir campos ausentes a partir de una tabla Markdown incompleta.
4. La comparación automática requiere una referencia verificable. En la primera ejecución, o si falta el objeto Git por historial superficial, emitir `SIN-BASE-COMPARABLE` con la causa y el inventario actual. No afirmar que todas las filas son nuevas ni que no hubo cambios. La ejecución inicial establece una referencia utilizable para la siguiente.
5. Para uso de diagnóstico, permitir una referencia explícita, por ejemplo `--base-nc-ref <sha>`, si el CLI vigente no ofrece equivalente. Resolverla con Git y argumentos estructurados, sin interpolar texto en un shell. Una referencia explícita inválida es error; no sustituirla silenciosamente por otra.
6. Si el TSV tiene cambios locales que el SHA no representa, no atribuirle falsamente ese contenido al commit. En el modo de publicación, detener esa escritura e indicar que primero debe versionarse el corte. Un modo de vista previa puede mostrarlo, declarando su hash y que no constituye una referencia publicada. No crear commits desde el generador.

El archivo de salida no puede convertirse en su propia referencia mientras se sobrescribe. Un reintento antes de publicar, con el mismo corte y la misma base, produce la misma sección H. Una ejecución posterior a publicar compara contra el corte recién publicado y no repite novedades que ya contiene.

Actualizar la declaración de determinismo para incluir explícitamente fecha, árbol de entrada y referencia de comparación. No añadir reloj de ejecución, UUID o metadatos volátiles al diff.

## P2 · Contrato de comparación

Comparar por `id` de reserva, validando su unicidad en cada corte. Comparar los campos completos comunes del TSV, no solamente las columnas visibles en la tabla. Normalizar únicamente diferencias de transporte inocuas, como BOM y finales de línea; no eliminar tildes, puntuación o contenido de las reservas.

| Situación | Salida requerida |
|---|---|
| ID ausente antes y presente ahora | `NUEVA`, con estado y sucesor actuales. |
| Mismo ID con cambio de estado | `CAMBIO-DE-ESTADO`, con antes y después; identificar cierres y reaperturas a partir de los valores reales. |
| Mismo ID con cambios de contenido, impacto, motivo o sucesor | `MODIFICADA`, indicando campos y valores que cambiaron. |
| ID presente antes y ausente ahora | `AUSENTE-EN-CORTE-ACTUAL`; nunca llamarlo cerrado por inferencia. |
| Mismo contenido con otro orden de filas o columnas | Sin novedad. |
| Cortes iguales | `SIN-CAMBIOS`, conservando el total vigente de abiertas. |
| Primera ejecución o referencia automática no recuperable | `SIN-BASE-COMPARABLE`; inventario actual y motivo, sin delta ficticio. |
| ID duplicado, TSV inválido o esquema incompatible | Error explícito; no emitir un diff aparentemente válido. |

Una reserva con cambio de estado y de contenido aparece una sola vez con ambos cambios. Si un ID parece reutilizado porque cambió la identidad de acto/pieza, mostrarlo como cambio de identidad para revisión; no inventar un parentesco entre filas ni fusionarlas por similitud textual.

Si cambia el esquema del TSV, declarar las columnas añadidas o retiradas. Comparar únicamente lo que siga siendo interpretable y marcar la limitación, o detener el diff si afecta la identidad o el estado. No convertir una columna nueva vacía en decenas de cambios sustantivos.

Orden determinista de la salida, por ID y campos en orden estable. Los textos deben pasar por la neutralización y validación de marcadores ya existentes.

## P3 · Presentación y operación en `/tramite`

La sección H debe mostrar, en este orden:

1. Referencia anterior y corte actual; estado de comparabilidad.
2. Conteos de reservas nuevas, con cambio de estado, modificadas y ausentes. Si las categorías se solapan, declararlo; preferir además un total de IDs afectados sin duplicados.
3. Tabla breve con una fila por reserva afectada: ID, cambio, antes/después y sucesor. Mantener el tope de presentación existente cuando sea aplicable, declarando los elementos omitidos.
4. Total actual de abiertas y enlace al inventario completo versionado. El detalle completo debe seguir siendo accesible, aunque la tabla visible se trunque.

Ejemplo ilustrativo, no estado real del proyecto: «1 nueva; 1 cierre; 1 cambio de sucesor; 3 reservas afectadas». Si no existe base, los conteos de cambios deben presentarse como no disponibles, no como ceros.

Usar el conteo vigente de `corrida0 status` cuando el contexto permita derivarlo sobre el mismo árbol; contrastarlo en la verificación. Si no puede obtenerse, declarar que el conteo es una lectura local del TSV, sin anunciar una corroboración inexistente. Retirar la afirmación obsoleta de que `status` todavía no lo deriva.

Preservar `--stdout`: no escribe un digesto, un checkpoint ni otro estado. Escribir la salida de archivo de forma atómica después de validar todo el contenido; si falla la generación o la validación, conservar el digesto anterior. El generador no realiza push, merge, cierre de reservas ni publicación de mensajes.

## P4 · Pruebas y demostración

Usar fixtures y un repositorio Git temporal para probar el historial. No depender de GitHub, reloj real, corpus privado ni la configuración de la caja.

Casos de aceptación obligatorios:

- Primera emisión: inventario y `SIN-BASE-COMPARABLE`, sin falsas novedades.
- Dos cortes iguales: cero IDs afectados y `SIN-CAMBIOS`.
- Alta, cierre, reapertura, modificación de sucesor y cambio de contenido; una fila por ID afectado.
- Reordenamiento: sin cambios falsos. Eliminación: ausencia explícita, nunca cierre.
- Referencia histórica inequívoca; referencia inexistente y SHA antiguo no recuperable con sus comportamientos respectivos.
- Dos publicaciones el mismo día; salto de varios días; reintento anterior a publicar sin autoconsumir la salida.
- `--stdout` y fallo de validación no escriben ni alteran la referencia anterior.
- TSV duplicado o inválido: error visible; contenido con marcadores: neutralización preservada.

Conectar esta prueba a la verificación automática existente y demostrar que realmente se invoca. Ejecutar una muestra del generador sobre el árbol real en modo de lectura, usando `--sin-suite` para no repetir una suite entera durante cada muestra. La demostración histórica puede hacerse en el repositorio temporal si todavía no hay dos cortes reales comparables.

Si el flujo exige baseline para el cambio final, ejecutarlo una vez y reportar diferencias materiales. No añadir una nueva batería de auditoría ni reparar fallos heredados ajenos.

## Criterios de cierre y entrega

El encargo termina cuando `/tramite` presenta un diff reproducible, no repite el inventario como novedad, maneja honestamente la ausencia de base y tiene una prueba automática conectada.

Cerrar `NC-0008` y `NC-0013` solamente al verificar que corresponden a este hueco por su texto y que la demostración cubre su condición. El generador no se cierra reservas a sí mismo: el cierre se registra por el ejecutor con evidencia. No cerrar otras filas incidentalmente.

Entregar una rama y un PR pequeño si su publicación está autorizada; de otro modo, diff y texto de PR listos. No fusionar automáticamente.

El cierre incluye: ejemplo antes/después de H; contrato de referencia implementado; comportamiento del primer corte; pruebas y automatización conectada; estado real de las dos reservas; limitaciones operativas. Distinguir una demostración en fixture, una generación local real y una ejecución periódica publicada: son evidencias diferentes.

## Referencias

- [PR #611: hueco incremental y referencias históricas disponibles](https://github.com/Josanoforo/Modelado-Mexicano/pull/611).
- [PR #613: actualización de las rutinas existentes](https://github.com/Josanoforo/Modelado-Mexicano/pull/613).
- [Generador en la base revisada](https://github.com/Josanoforo/Modelado-Mexicano/blob/fbd847deee91c3e3efe283bb2f5921addcdda3a9/tools/digesto_tramite.py).
- [Registro de reservas en la base revisada](https://github.com/Josanoforo/Modelado-Mexicano/blob/fbd847deee91c3e3efe283bb2f5921addcdda3a9/forense/no-corrido.tsv).
