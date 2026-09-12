# 38 · GEN2 · Descubrimiento externo, adquisición y suficiencia en producción

ENTORNO: CAJA
EJECUTOR: Codex CLI en Windows/WSL
ESTADO: listo para despacho como encargo integral sucesor de 32/#726.
RESULTADO: un ciclo operativo que parte de una necesidad científica, explora fuera del corpus, incorpora datos utilizables y declara qué preguntas puede y no puede responder.

## 1. Decisión y autoridad del encargo

Instrucción de Jonás, 12 de septiembre de 2026: «Qué tenemos que hacer para que funcione [...] para que la sonda le dé el input suficiente [...] si realmente tanto sonda como el CRON son lo suficientemente potentes para que corran sobre el universo desconocido y nos traigan la data que necesitamos. Si estamos haciendo cálculos con data insuficiente porque “es lo que hay” esto no debe suceder».

**Camino elegido: implementación integral con diagnóstico inicial acotado.** No encargar una auditoría general previa, ni volver a entregar sólo dos reparaciones del selector. Este acto asume la responsabilidad completa de descubrimiento→adquisición→disponibilidad→suficiencia para el uso.

Al despachar este documento, Jonás autoriza:

- Investigación externa periódica para las necesidades científicas activas, incluyendo fuentes que aún no figuren en el corpus ni en la cola.
- Descarga y registro de fuentes públicas pertinentes y uso de accesos previamente autorizados, dentro de ese alcance, sin pedir una firma por cada URL o formato alterno.
- Reparar e integrar las herramientas existentes, ajustar su configuración, desplegar en el clon operativo y ejecutar recorridos reales hasta publicación; commits, push y PR. Los merges siguen con Jonás.
- Cadencia propuesta para esta campaña: **diaria a las 07:30, America/Mexico_City**, con un único programador. El despacho autoriza ese cambio respecto de lunes–viernes; registrar explícitamente la modificación.

Esta autorización de adquisición **no es autorización de adopción científica**. No autoriza compras, contratos, envíos en nombre de Jonás, uso de identidad/afiliación inventada, eludir barreras de acceso, cambiar el modelo competidor F5 o abrir FP-373/374/F6. Una relación candidata necesidad→fuente puede registrarse sin declararla confirmada.

La autorización general debe quedar asentada con su cita y alcance. Los objetos nuevos se vinculan a ese acto; no inventar firmas individuales de mesa. Si el esquema exige autorización por ID, implementar una derivación comprobable desde el mandato asentado y los límites de adquisición pública. Fuera de ese alcance, conservar la acción humana concreta pendiente. Ajustar explícitamente la instrucción anterior de SONDA que exigía firma individual: no dejar dos políticas incompatibles.

## 2. Estado comprobado y problema real

Repositorio: `Josanoforo/Modelado-Mexicano`. Corte: main `d14d715339227c7de3c8c4d7ef35e0b2a14f7325`, #726 fusionado. Consultar cambios posteriores pertinentes antes de actuar.

- **Disparador/publicación:** #726/#727 acreditan recorridos desde Task Scheduler y recibos con `adq-codex-3`, incluidos `run_id=2026-09-11T182258-1971648`, SHA `50e693d508b9191047039930f00d886c5d818188`, salida 0 y publicación OK. Eran corridas sin objetos elegibles; no descargaron datos.
- **SONDA tiene método de exploración externa:** `.claude/commands/sonda.md` contempla CONSTRUCTO, HERMANAS y LATERAL. Es invocable, propone y entrega candidatas. No es un servicio periódico de descubrimiento conectado al cron.
- **El cron termina con cero elegibles antes de explorar:** `tools/adquiere_cron.sh` selecciona la cola existente y sale con `cola_vacia`. `sonda_red()` comprueba transporte/HTTP; no ejecuta investigación SONDA.
- **Siete residuales no son toda la demanda científica:** #726 estructuró seis necesidades de acceso y una sin vía. `resumen_necesidades` sólo cuenta filas marcadas `RESIDUAL-ADQ-V1`; no acredita que las demás necesidades activas estén cubiertas.
- **Dos defectos reproducidos:** la autorización de un residual guardada en JSON puede ser rechazada por `_autorizada` al conservar `SONDA-LATERAL-RECOMENDADA`; «intento efectivo pendiente de conciliar» se trata como ausencia de intento. Ambos siguen dentro del perímetro.
- **La validación numérica no acredita suficiencia:** #731 propone 16/16 puntos concordantes y deja diseño/EE/IC no comprobados. #730 ya integra medición ENSAFI. Eso no identifica automáticamente el efecto de BNPL, costo exacto del producto o daño causal de N34.

No se concluye que todo GEN2 esté mal medido. Se concluye que la maquinaria actual no garantiza por sí sola búsqueda externa recurrente ni ajuste entre evidencia y pregunta. Es posible calcular correctamente un objeto que responde sólo una parte de la necesidad.

## 3. Arranque y reparto de responsabilidades

Lee `AGENTS.md`, este encargo y sólo los archivos necesarios. Reporta ruta absoluta, rama, SHA y estado; usa worktree propio. Verifica cada premisa material y consume correctivos posteriores equivalentes. No reconstruyas los PR históricos.

Reutiliza:

- `tools/adquiere_launcher.sh`, `tools/adquiere_cron.sh`, `tools/adq_config.py`, `tools/adq_doctor.py`, `tools/adq_residual.py` y `tools/adq-resultado.schema.json`.
- `data/adq-config.yaml`, `.claude/commands/{sonda,adquiere}.md`, `forense/agente-adquisicion-v1_0.md`.
- Registro canónico de adquisición, sus escritores y vista; relaciones/evidencias/utilidad-modelo para necesidad→fuente→uso.
- Contratos/specs y resultados vigentes; `data/corrida0/demanda-*.tsv` son derivados, no una nueva autoridad para editar ni una lista exhaustiva de la ciencia GEN2.
- Buscador de reactivos, manifiesto y resolvedor de raíces; contratos de emisión GEN2 y consulta.

Concurrencia vigente:

| Frente | Responsabilidad que conserva |
|---|---|
| 33 | Materialización del corpus; consumir su operación, no construir otra. |
| 34 | Metadatos/buscador; consumir su actualización y cobertura textual. |
| 35 | Panel de tandas; no repetir su CALC ni llamarlo ledger de impagos. |
| 36 | Búsqueda/descarga de producto financiero y daño N34; incorporar sus hallazgos y evitar otra búsqueda simultánea del mismo objeto. |
| 37 | Delta; no convertir su comparación en juicio automático de suficiencia. |
| 29/#729 y 30/#731 | Consulta y validación independiente; usar sus interfaces y coordinar cambios puntuales al consumo de aptitud. |
| 31/#728 | F5; paquetes, firmas, modelo y capturas fuera de este acto. |

Este acto es dueño del servicio de descubrimiento, cron y conexión con suficiencia. Los otros encargos aportan trabajo por objeto. No habrá dos dueños escribiendo la misma necesidad al mismo tiempo: usar el mecanismo de asignación vigente o una reserva mínima con vencimiento, identidad y reanudación. No crear otro tablero maestro para ello.

## 4. Fase A · Demanda científica y suficiencia por uso

Construye una proyección de trabajo desde las necesidades activas y sus contratos, no desde «archivos que tenemos». Incluye: sin fuente, NO_COVERAGE, fuente parcial, proxy, diseño insuficiente, antigüedad incompatible, acceso pendiente y nuevas hipótesis expresamente activas. No reactivar automáticamente todas las reglas históricas GEN1 ni las decisiones comerciales diferidas.

Para cada necesidad, enlaza:

- pregunta y consumidor; uso descriptivo, asociativo, predictivo, causal o inferencial;
- población/unidad/evento/periodo y variables necesarias;
- evidencia disponible y qué parte cubre;
- brecha concreta y efecto sobre el uso;
- investigación previa y su frontera, prioridad vigente y próximo paso.

Reutiliza relaciones y utilidad-modelo; si falta un campo operativo, ampliar mínimamente su contrato o producir una vista derivada. No duplicar el registro de necesidades.

No inventar una nota única de «suficiencia 80%». Evaluar separadamente identidad del objeto, cobertura conceptual y poblacional, selección/no respuesta, unidad, temporalidad, ponderación/diseño e identificación exigida por el uso. Los umbrales de precisión/tamaño se justifican para la decisión concreta, no se fijan a posteriori para aprobar el resultado.

Tres consecuencias prácticas, mapeadas a los estados existentes:

1. **Evidencia apta para el uso declarado:** puede calcularse y utilizarse bajo el contrato vigente.
2. **Evidencia útil para un alcance menor:** puede producir descripción o exploración con ese rótulo; la pregunta original queda abierta y alimenta SONDA. No presentarla como resuelta.
3. **Evidencia incompatible con el uso solicitado:** el consumidor no emite ese resultado y explica la brecha; búsqueda o gestión pendientes.

Las comprobaciones deterministas se automatizan. La equivalencia de constructos o identificación causal que exige juicio no se aprueba por una puntuación, por pasar tests o porque un LLM diga «suficiente». Reutilizar decisiones explícitas; elevar sólo elecciones científicas nuevas con alternativas concretas.

## 5. Fase B · SONDA recurrente sobre fuentes externas

Implementa una fase real de descubrimiento dentro del ciclo operativo. Debe ejecutarse cuando haya necesidades de investigación listas, **aunque haya cero descargas elegibles**. Si no hay búsqueda pendiente ni descarga, cerrar sin LLM, declarando esa situación.

Selección de investigaciones: prioridad de consumidor ya fijada, bloqueo material y tiempo desde la última exploración. Evitar que los mismos expedientes sin acceso ocupen todas las corridas. Contemplar también necesidades con fuentes «obtenidas» pero insuficientes para su uso.

Para cada necesidad seleccionada:

1. Leer el estado conocido para no repetir trabajo; no usarlo como límite de búsqueda.
2. Ejecutar CONSTRUCTO para otras familias/instrumentos, HERMANAS para olas/módulos/replicaciones y LATERAL para vías legítimas alternativas, según la brecha.
3. Buscar realmente en web, portales oficiales, repositorios de autores/universidades, catálogos y paquetes de replicación. Probar que el ejecutor tiene búsqueda externa operativa: leer un runbook no acredita capacidad de búsqueda. Si falta la herramienta, configurarla por una vía disponible y autorizada; no fingir exploración desde el buscador local.
4. Seguir pistas concretas, versiones, diccionarios y archivos asociados. Registrar qué se examinó, cuándo, qué era nuevo respecto del corpus y por qué sirve o no.
5. Verificar contenido y objeto. HTTP 200, un paper o una landing page no equivalen a microdatos. Fuente extranjera o proxy puede aportar contexto, no convertirse en dato mexicano por omisión.

La investigación produce candidatas y evidencia, no una nueva cifra del motor. No solicitar ni exponer valores de evaluación retenida para orientar la selección de fuentes. Una fuente incorporada después del corte no mejora retrospectivamente una evaluación congelada; sólo alimenta trabajo prospectivo compatible.

Guardar progreso por necesidad y versión de su pregunta. Un timeout conserva pistas y cursor de continuación: no equivale a «no existe». Reabrir por nueva edición, nueva vía, nueva evidencia, cambio de necesidad o fecha de revisión declarada. No repetir diariamente rutas agotadas sin motivo, ni dar por agotado el universo desconocido tras N consultas.

Configuración inicial propuesta, autorizada al despacho: hasta **3 necesidades investigadas y 5 objetos de adquisición por ciclo**, 30 minutos de descubrimiento y 30 de adquisición, con margen para publicación dentro del límite global de la tarea. Son límites de ejecución, no umbrales de suficiencia ni prohibición de continuar manualmente. Medir consumo y ajustar por configuración; no ocultar trabajo truncado como terminado.

## 6. Fase C · Handoff y adquisición sin atasco de firmas

Cada candidata pública que encaje en el mandato de adquisición debe recibir vínculo verificable al acto y un objeto residual ejecutable. No esperar una nueva firma individual sólo por ser una URL desconocida. Para acceso institucional, costo, identidad o compromiso externo, preparar la acción precisa y seguir investigando alternativas públicas cuando sean pertinentes.

Reparar los dos defectos conocidos usando un contrato de autorización común: leer la metadata JSON como JSON y la historia como historia; una marca antigua de recomendación no borra una autorización vigente válida. Detectar ambigüedad, objeto distinto, negación y fecha inválida. Un intento explícito sin fecha determinable no habilita reintento automático.

Integrar un único recorrido:

`necesidad → búsqueda externa → candidata con evidencia → autorización de adquisición por alcance → residual accionable → descarga → validación de bytes/contenido → manifiesto/corpus → indexación → evaluación de cobertura → consumidor`.

A.8 compara el objeto/variables/ola/unidad que se necesita, no sólo nombre/host. Preservar padres obtenidos y residuales distintos. No sustituir archivos bajo una identidad/hash histórica. Descargar a temporal propio, verificar, publicar atómicamente y usar los escritores existentes.

Comprobar actualizaciones concurrentes reales: el nombre «alta atómica» no demuestra protección entre procesos. Registro/vista no deben perder una fila cuando cron y un encargo manual publican casi juntos. Reutilizar locks y semántica de escritor existentes; si falta protección, añadirla en el punto común con alcance corto y recuperación. Nunca retener un lock de publicación durante una investigación web larga.

Aislar errores por proveedor/objeto. Un fallo de `inegi.org.mx` no debe impedir una investigación o descarga legítima en otro proveedor. Conservar verificación de transporte, contenido, timeout y publicación sin usar un único portal como prueba universal de internet.

## 7. Fase D · Conectar cálculo y uso con la brecha real

Al preparar una spec y al publicar un resultado, enlazar el estimando al uso y a la cobertura acreditada. Si la inspección descubre que falta un reactivo/denominador/ola/diseño, escribir la necesidad residual y su destino SONDA, no sólo una nota «no se pudo».

Esto no impone esperar a explorar todo internet para medir un punto descriptivo bien definido. Impide sustituir silenciosamente la pregunta por lo disponible. Ejemplos obligatorios:

- ENSAFI atraso por clase de deuda puede describir ese fenómeno; no acredita efecto causal de BNPL ni costo de un producto específico. Mantener abierto el enlace NC-0164 y consumir el trabajo de 36.
- Tandas individuales y su panel no acreditan impago por turno ni efecto de conocer a la organizadora. La brecha de ledger o instrumento específico sigue visible.
- Puntos DIN/S6 pueden conservar el alcance ya autorizado; un IC aproximado no se convierte en inferencia de diseño aprobada por concordancia numérica.

Consume los controles GEN2 ya existentes y añade sólo la conexión que falte. No reescribir las 16 adopciones por una sospecha general. Si la inspección identifica una incompatibilidad material concreta en una emisión actual, proteger ese uso y entregar la evidencia; corrección numérica sucesora sólo si se acredita su necesidad.

Para el conjunto activo al inicio, entregar estado por necesidad/uso y cambios prospectivos. No etiquetar toda la ciencia como suficiente porque un subconjunto pase replay, ni bloquear toda la ciencia porque otra pregunta requiera acceso externo.

## 8. Fase E · Despliegue y demostración completa en CAJA

Desplegar en `/home/pc0/mm-adq` por el mecanismo vigente, preservando staging ajeno, revisión fijada/main, identidad, corpus y una sola tarea `\\ModeladoMexicano\\AdquiereCron`. No cambiar globalmente configuraciones de otros CLI ni usar Claude como fallback del operador de adquisición.

El modelo operador es el de `data/adq-config.yaml` y puede ejecutar el trabajo con Codex. Los modelos competidores F5 permanecen fuera de este cambio.

La tarea actual usa `Interactive`: declarar que requiere sesión PC0 iniciada. Si se quiere operación con sesión cerrada, resolver el privilegio y validar WSL/autenticación bajo la identidad permitida; no declarar S4U funcional sin comprobarlo ni saltar un rechazo de permisos. No es condición para integrar la mejora científica, pero sí limita la disponibilidad que se promete. El equipo apagado no ejecuta el trabajo; registrar recuperación y retrasos honestamente.

Demostración de producción en esta misma tarea, no una entrega posterior de «sólo tests»:

1. **Cola de descargas vacía + necesidad abierta:** el ciclo ejecuta investigación externa real y publica lo encontrado/descartado y su frontera. Ya no sale antes de SONDA.
2. **Candidata pública nueva y pertinente:** con una necesidad real, demostrar autorización por alcance, selección, adquisición de bytes, registro, disponibilidad e indexación/lectura, y actualización de la brecha. Comparar contra el manifiesto inicial para acreditar qué es nuevo. No usar un CSV ficticio o una descarga duplicada como éxito.
3. **Necesidad con acceso externo o instrumento insuficiente:** preserva la barrera, investiga vías razonables distintas y no produce un número ficticio ni un cierre científico falso.
4. **Consumo:** una consulta/preparación real reconoce la evidencia apta o la no cobertura con causa, sin fallback GEN1 y sin tocar paquetes F5.

Elegir los objetos al iniciar desde la demanda real y los encargos en curso. NC-0122 (producto fintech específico) y NC-0153 (evento×canal nacional) son candidatos de investigación, no promesa de disponibilidad; N34 pertenece a 36 y se consume su entrega. No repetir su búsqueda simultáneamente. Los datos ya obtenidos de ENSAFI/IMOR sirven para demostrar consumo, no como hallazgo externo nuevo.

Si ninguna fuente nueva examinada resulta accesible/pertinente, documentar ese resultado: el caso 2 queda pendiente por objeto, sin declarar cumplido lo que no ocurrió. Terminar el servicio, publicar la investigación y continuar otras necesidades legítimas; no forzar una descarga irrelevante para aprobar el acto.

Los eventos de Task Scheduler, run_id, SHA, proveedor/modelo efectivo, selección, búsqueda, descarga y publicación deben corresponder al mismo recorrido o identificar expresamente corridas distintas. Una activación manual es manual; el valor de una variable `disparador` no sustituye los eventos Windows. Restaurar la programación diaria final y comprobar próxima ejecución. No duplicar corridas caras sólo para obtener más capturas de pantalla.

## 9. Cierre y aceptación

El cierre debe responder con evidencia:

- ¿Qué necesidad entró y qué pedía exactamente?
- ¿Qué se buscó fuera del corpus y qué frontera quedó sin examinar?
- ¿Qué fuente/objeto nuevo se obtuvo o qué barrera concreta apareció?
- ¿Dónde están los bytes y puede leerlos una sesión diferente?
- ¿Qué uso quedó suficientemente cubierto y cuál sigue abierto?
- ¿Qué ejecutará el próximo ciclo, con qué límites y por qué?

Recibo operativo: necesidades candidatas/en proceso, búsquedas intentadas y pendientes de continuación, objetos elegibles/obtenidos/bloqueados, brechas resueltas/parciales, errores, consumo observable y refs de publicación. Los contadores no deben confundirse: consultas web, URLs, archivos, estudios independientes y necesidades cubiertas son unidades distintas.

Pruebas dirigidas para los dos defectos reproducidos, ruta de selección vacía que ahora investiga, reanudación y concurrencia; luego la demostración real. No una auditoría global ni una batería nueva como sustituto de producción.

Actualizar registro/vistas/relaciones y cierre con los escritores vigentes; conservar historia y residuales de NC existentes. No cerrar los seis accesos humanos de #726 por instalar este servicio. El acto puede entregar software operativo con barreras externas explícitas; no afirmar que ya existe toda la data necesaria.

**Entrega indivisible de ingeniería:** corrección, descubrimiento conectado, política de adquisición asentada, conexión de cobertura, despliegue y recibo de producción. Pueden publicarse commits por fase en un PR, pero «SONDA lista para conectar después» o «falta otra sesión para probar producción» no completan el encargo, salvo bloqueo real de acceso/privilegios documentado con acción precisa.

## 10. Prompt de lanzamiento

> Ejecuta íntegramente el encargo 38. Autorizo la investigación externa recurrente y adquisición pública dentro de su alcance, la cadencia diaria propuesta, implementación, despliegue, commits, push y PR; los merges quedan conmigo. Esta es la autorización de adquisición por alcance que debe quedar asentada y enlazada a cada objeto, sin inventar firmas nuevas ni aprobar adopciones científicas. Revisa sólo lo necesario, consume lo ya resuelto y coordina los frentes 33–37. Termina con necesidad→descubrimiento externo→adquisición→suficiencia→uso demostrado en producción. No cierres con un diagnóstico, tests o cola vacía si hay investigación pendiente. Si una gestión externa o privilegio impide una parte, deja la acción exacta preparada y completa las demás. No sustituyas la pregunta científica por “es lo que hay”.

## Fuentes de este diagnóstico

- [#726 · Residuales y cron](https://github.com/Josanoforo/Modelado-Mexicano/pull/726), código y nota de cierre.
- [#727 · Recibos](https://github.com/Josanoforo/Modelado-Mexicano/pull/727).
- [#730 · ENSAFI](https://github.com/Josanoforo/Modelado-Mexicano/pull/730).
- [#731 · Validación independiente](https://github.com/Josanoforo/Modelado-Mexicano/pull/731), alcance declarado en el PR abierto al corte.
- `.claude/commands/sonda.md`, `tools/adquiere_cron.sh`, `tools/adq_residual.py`, `tools/adq_doctor.py`, `data/adq-config.yaml`, `data/curacion-registro/utilidad-modelo.tsv` y contratos GEN2 vigentes.
