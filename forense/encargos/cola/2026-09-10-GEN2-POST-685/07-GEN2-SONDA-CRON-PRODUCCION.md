# ENCARGO · GEN2-SONDA-CRON-PRODUCCION

> **ESTADO 2026-09-10:** EJECUTADO en PR #704, ADR-466, por
> `forense/encargos/2026-09-10-GEN2-SONDA-CRON-PRODUCCION-POST693.md`
> en la rama `acto/gen2-sonda-cron-produccion`. No es una segunda tarea.
>
> **BITÁCORA:** configuración única, prueba de caja y cierre operativo se
> ejecutaron en la continuación POST693. Este cuerpo se conserva como
> antecedente; la evidencia y los residuales están en su nota de cierre.

## Configuración única → prueba de caja → rastro de producción

Fecha de preparación: 10 de septiembre de 2026. Corte verificado: `486eda19944a94d978791eb423559144de98d16b` (merge de #685).

**Destino:** Cloud puede preparar código/tests; **CLI Windows/WSL es necesario para terminar la prueba real**. **Integra:** E10; D19; NC-0114/0115/0120. **Rama:** `acto/gen2-sonda-cron-produccion`.

## Resultado y perímetro

Un solo calendario leído por sus consumidores y evidencia que permita saber si corrió, quién lo disparó y qué consiguió. El cron instalado/configurado no equivale a recuperación de disparo perdida observada.

Leer/editar `data/adq-config.yaml`, `tools/adq_config.py`, `tools/adq_doctor.py`, `tools/adquiere_cron.sh`, `tools/windows/instala-tarea-adquisicion.ps1`, T31 en `tests/check.py`, pruebas `tests/test_adq_*.py` pertinentes y runbook vigente. Añadir sólo el código y recibos necesarios. No cambiar horario por otro, proveedores, políticas sustantivas de fuentes ni añadir scheduler.

## Fase 0 · Estado instalado y capacidades

Identificar qué está instalado en la caja, con ruta, versión/SHA y configuración. Desde Cloud, leer evidencia registrada y producir la continuación exacta de caja; no interpretar NO-VERIFICABLE como “no instalada”. Respetar tareas/runners activos y no matar un cálculo ajeno para probar timeout.

**Observado:** NC-0115 localiza 07:30 en instalador, runner y T31; `claude_kill_after_segundos` falta en config. NC-0120 documenta Operational deshabilitado y recuperación no demostrada. **Consecuencia:** reparar esos enlaces y medir la operación; no repetir las reparaciones H1/H4/H5/H6 ya cubiertas.

## Fase 1 · Unificar configuración conservando conducta

Hacer que instalador, runner y T31/doctor lean una única autoridad de horario/zona/días, manteniendo 07:30 America/Mexico_City y la periodicidad efectiva ya registrada. Resolver traducción entre zona Windows e IANA sin depender de que el host esté en la zona correcta por casualidad.

Añadir `claude_kill_after_segundos` con default compatible de 60 s, validación y precedencia de override explícita. Conservar timeout de modelo y gracia de observación como conceptos separados. La configuración degradada debe dejar causa y valor usado; no un éxito silencioso.

**Compuerta:** pruebas dirigidas con misma próxima hora esperada en consumidores, cambio de día/zona, config inválida, override y escalamiento TERM→KILL. Reusar el caso de proceso que ignora TERM; aislamiento de procesos del test.

## Fase 2 · Instalar/verificar en la caja real

Preparar comandos PowerShell/WSL reproducibles basados en los scripts efectivos. Leer/exportar la tarea previa; comparar antes de cambiar. Habilitar el canal Operational con el permiso del operador cuando el SO lo exija. Un rechazo de elevación se reporta con la acción exacta pendiente, no se elude.

Instalar/actualizar la tarea autorizada; verificar ruta, argumentos, distribución/usuario WSL, zona, horario, StartWhenAvailable y origen de ejecución. Confirmar que no quedan dos programadores disparando lo mismo. No deshabilitar un programador sin identificar cuál queda a cargo y conservar el procedimiento de reversión de esta modificación.

## Fase 3 · Probar disparo, recuperación y fallos

Correlacionar evento del programador, instancia/tarea, inicio del proceso WSL, run_id, SHA, log, heartbeat y recibo publicado. Diferenciar invocación manual, fixture y programada. Usar un disparo controlado con hora próxima si procede y conservar/restaurar el calendario productivo.

Demostrar una recuperación real de hora perdida con un procedimiento de caja que no interrumpa trabajos del usuario. StartWhenAvailable=True y una invocación manual no bastan. Una tarea de prueba aislada puede acreditar el mecanismo en ese alcance; no se etiqueta como corrida productiva. Terminar la correlación de producción con un disparo de la tarea efectiva.

Probar candado/doble lanzamiento, fallo de red, modelo no disponible, timeout y fallo de publicación mediante fixtures o inyección acotada; no provocar indisponibilidad real innecesaria. Cada intento debe terminar con resultado distinguible. No atribuir a hoy el arranque histórico cuyo origen no se pudo conocer.

## Fase 4 · Conectar demandas y cierre

Comprobar que una demanda válida del lote 06 llega a SONDA/cola, se clasifica, intenta o difiere con causa y aparece en el recibo/digesto. La máquina no adopta fuentes ni decide que un cambio de contenido es equivalente.

Fechas indeterminadas: buscar evidencia; no fabricarlas ni leer ausencia de fecha como ausencia de intento. Si la política no cubre el residual, entregar una decisión puntual y completar el resto. Modelo: comprobar el configurado; no convertir el cambio de cuenta o el uso de Codex CLI en migración automática de Claude.

Cerrar NC-0115 con código integrado; NC-0114/0120 sólo por las pruebas que exigen. Entregar comandos/recibos y alcance de la recuperación. Si Cloud termina F1, declarar “código listo, caja pendiente”, mantener PR de continuación y no afirmar producción lista.

**D-14:** defecto real: calendario disperso y disparo/recuperación sin correlación; materialidad: adquisición silenciosamente ausente; menor costo: unificar config y reutilizar doctor/recibos evita reconstruir cada mañana la historia. Costo acotado a herramientas existentes.

## Contrato de ejecución incluido en este encargo

Este archivo es autocontenido. Su fuente de autoridad es la instrucción de mesa registrada en `forense/encargos/2026-09-10-MESA-CONCILIACION-E01.md` y la solicitud posterior: «dame los siguientes encargos, multi encargos, multifase, para correr en codex cloud o codex cli». E01 y el diagnóstico #684 ya están fusionados: no repetirlos.

**Alcance del despacho:** implementar las fases autorizadas, hacer commits y presentar el resultado en una rama/PR propios para revisión. El merge pertenece a mesa. No ejecutar otro encargo, hacer merges automáticos ni cerrar PR ajenos. Si la plataforma publica el PR por una acción propia, preparar la rama y el contenido para esa misma entrega; no duplicar el PR.

**Arranque obligatorio y corto:** informar ruta absoluta, rama, HEAD y `git status --short`; leer `AGENTS.md` y este archivo; consultar origin/main y PR/rama con el mismo objeto. Reutilizar o continuar el trabajo compatible. Usar un worktree propio, sin limpiar ni cambiar la rama de otra ejecución. Archivar este encargo por 0-bis A.3 antes de modificar el objeto. Las rutas aquí son las verificadas al corte: resolver renombres y colisiones sin reconstruir toda la historia.

**Fases:** avanzar a la siguiente cuando se cumpla su compuerta objetiva; no pedir confirmación entre fases ya autorizadas. Si una depende de caja, credenciales personales, datos ausentes o una decisión científica no tomada, completar el resto y entregar el punto exacto de continuación. No llamar “terminado” al encargo entero si sólo quedó preparado en Cloud. El destino depende de capacidades comprobadas, no del nombre del producto.

**Perímetro administrativo común:** archivo de este encargo, nota de cierre, sus filas FP/NC/cola, referencias de decisiones y cascada vigente en `canon/gobernanza-v1_15.md`, `canon/estado-programa-v1_12.md` y `canon/registro-rotulos.tsv`. Cada sección añade archivos sustantivos. Conservar los IDs históricos E02–E11 como antecedentes y apuntarlos al lote correspondiente; no crear una segunda obligación por cambiar el nombre del encargo.

**Cambios concurrentes:** el perímetro es propio aunque otros lotes avancen. Antes de integrar, actualizar con main y reconciliar sólo colisiones de IDs, registros y archivos compartidos del propio acto. No copiar una versión antigua del TSV completo. No relajar el candado del despacho automático. Las entradas congeladas de un experimento se resuelven por versión/hash aunque el árbol avance.

**Medición:** reutilizar resultados sellados cuando coincidan estimando e insumos; para un cálculo nuevo, congelar spec y método en un commit anterior al primer resultado. Resolver datos por manifiesto/raíz configurada; no inventar `/home/...`, no subir microdatos restringidos ni credenciales. Registrar unidad, universo, ponderador, exclusiones, incertidumbre y uso. Los cambios a código usado por un sello exigen preservar su reproducción por la vía existente o crear una sucesora explícita; no romper históricos para modernizar una herramienta.

**Objeto de firma al merge:** propagación de las decisiones de mesa citadas y de los resultados del encargo. Para CALC científicos nuevos, aplicar `cuenta_gen2=SI` con objeto y cita explícitos conforme al contrato vigente; los sucesores técnicos no inflan mediciones independientes. Contar no equivale a adoptar: sólo se activa en el motor lo autorizado por la decisión concreta y sustentado por su evidencia.

**Pruebas y cierre:** validar primero el riesgo material; ejecutar el gate requerido sobre la integración, sin limpiar deuda ajena ni cambiar baseline. Revisar `git diff` después de las pruebas; nunca incorporar con `git add -A` una derivación accidental. Mientras NC-0141 siga viva, registrar y preservar cualquier cambio previo del usuario antes de aislar efectos de la suite; no restaurar a ciegas sobre trabajo ajeno.

Cada fase termina con resultado o bloqueo preciso y prueba. Cierre completo: autorización → resultado/cambio → evidencia → consumidor, si aplica → FP/NC → vistas/cola → PR y merge. Una decisión firmada no cierra una ejecución pendiente. Registrar fecha real, cita y universo; nada se borra ni se rejuvenece por traslado. Si falta una pieza, usar el vocabulario vigente y sucesor concreto.

**Formato final del ejecutor:** resultado útil en cinco líneas; fases realizadas/pendientes; PR y SHA; pruebas; tabla `obligación | evidencia | cerrada/residual | siguiente acción`. No parar en un inventario cuando el entorno permite ejecutar. No continuar por inercia después de satisfacer el resultado.
