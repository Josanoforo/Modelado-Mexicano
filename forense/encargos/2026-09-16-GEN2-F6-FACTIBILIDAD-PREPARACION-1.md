# ENCARGO · GEN2-F6-FACTIBILIDAD-PREPARACION-1

Fecha de emisión: 16 de septiembre de 2026.  
Repositorio: `Josanoforo/Modelado-Mexicano`.  
Ejecutor principal: Codex CLI en CAJA/WSL, en worktree propio.  
Producto: un paquete operativo de factibilidad F6, probado sin datos reales, y un PR delimitado. No es otra auditoría del panel ni una autorización de medición.  
Base consultada: `origin/main @ 9dffd6455c67e2ca99740e79f90be59a13f250e1` (#823 fusionado). Al arrancar manda el `origin/main` vigente, no este SHA ni los ZIP de agosto.

## 0. Resultado encargado y autoridad

Dejar preparada la ejecución no confirmatoria de las candidatas R01-MOCIBA y R09-ISSP: definición verificable del desenlace, filtros y denominador, dieta de los candidatos, orden ciego, contrato de entradas/salidas, preparación técnica comprobada con fixtures y una decisión de mesa breve para autorizar o rechazar la ejecución posterior.

No termines con «conviene redactar una spec»: rédactala, materializa sus tarjetas y comprueba la preparación técnica. No presentes como lista para producción una pieza que aún requiera inventar códigos, transformar constructos o elegir un estimador después de ver R.

Se autorizan al lanzar este encargo: edición en el perímetro, pruebas sintéticas, commits, push sin force y apertura/actualización de un único PR. No se autorizan merges, cierre de PR ajenos, llamadas experimentales a modelos, adquisición, nuevas mediciones ni cambios a decisiones firmadas. Usar un agente CLI para implementar no equivale a autorizar llamadas de los brazos experimentales.

## 1. Arranque breve, aislamiento y concurrencia

1. Localiza el clon existente; lee `AGENTS.md` y este encargo completo. Reporta ruta absoluta, rama, HEAD y `git status --short`. Actualiza refs y consulta ramas, worktrees y PR del mismo rótulo antes de iniciar una segunda ejecución.
2. Crea un worktree propio desde `origin/main`, rama sugerida `acto/gen2-f6-factibilidad-preparacion-1`. No cambies de rama ni hagas stash, limpieza o descarte en el árbol de otra sesión. Si ya existe una ejecución viva, no la dupliques ni la cierres: reporta su ubicación.
3. Resuelve las raíces documentales por la configuración existente. Un worktree sin `data/raw` no demuestra ausencia del corpus: consulta el clon padre y `tools/entorno.py`. Enlaza sólo lo necesario conforme al mecanismo existente; no copies corpus a Git.
4. Revalida sólo las premisas que afectan este encargo. Si el panel o una firma sucesora ya resolvió una pieza, úsala; no repitas el trabajo. Un cambio de SHA no es un paro.
5. Archiva este encargo verbatim en `forense/encargos/2026-09-16-GEN2-F6-FACTIBILIDAD-PREPARACION-1.md`, sin insertar contenido posterior dentro de su texto. Anexa procedencia/consumo fuera del bloque verbatim según la convención vigente. Publica pronto esa rama para hacer visible la ejecución.

### Excepción específica de concurrencia a la cascada

CAREO-1, TRÁMITE-4 y CELDA-D-PILOTO-1 están a cargo de Opus. Este acto y el correctivo del digesto pueden desarrollarse en paralelo, pero **no ejecutan la cascada de escritura compartida**. Esta excepción forma parte del encargo que mesa autoriza al lanzarlo; no cambia permanentemente las reglas del programa.

No escribas `decisiones.tsv`, `no-corrido.tsv`, `firmas-pendientes.tsv`, `hallazgos.md`, PARA, canon/gobernanza, canon/estado, registro de rótulos, tableros, `rutinas.tsv`, manifiesto, colas ni contadores. No asignes ni reserves ADR, NC, FP o CALC. Las reservas y la decisión necesaria quedan en la nota de este acto y en el PR, con dueño y siguiente acción, sin abrir otro registro.

Si `/acto` exige esas escrituras, aplica la excepción, no la cascada automática. Tampoco ejecutes `/tramite`, `/despacha`, `/deriva` ni el cron. No edites `tests/check.py` o baseline para eximir el encargo. Evita rótulos ambiguos en la prosa nueva; si la convención impide integrar sin tocar un archivo compartido, entrega el producto probado y reporta ese impedimento concreto en el PR para integración serial. No inventes un falso CI verde ni abandones el producto por contabilidad auxiliar.

**Reserva absoluta:** no abras ni derives ENIF 2024 `localidad × edad`, ni directa ni incidentalmente. No leas sus microdatos, capturas nuevas o resultados reservados del piloto de Opus. No modifiques su spec, celda-D, crosswalk, corte de edad, motor, θ ni magnitud de G5. No uses una suite o script que vaya a generar esas salidas como efecto lateral.

## 2. Insumos y premisas materiales

Lee primero, en el árbol vigente:

- `forense/prereg-duelo-v2/F5-panel-candidatos-v1_3.tsv`, o su sucesor vigente si existe.
- `forense/notas/2026-09-15-GEN2-F6-PANEL-CAJA-1-cierre.md` y el encargo homónimo.
- `forense/prereg-duelo-v2/F5-transferencia-reservada-spec-v1_0.md`.
- `forense/prereg-duelo-v2/F5-panel-viabilidad-presupuesto-spec-v1_0.md`: sólo lo pertinente a FP-374, presupuesto y unidad de inferencia.
- Fila FP-374 de `forense/firmas-pendientes.tsv` y firmas sucesoras pertinentes, si existen.
- `data/reactivos-contexto-verificados-v1_0.tsv`, su tabla de fuentes y las entradas de `data/manifiesto.yaml` correspondientes a los documentos de R01/R09.
- Interfaz de elegibilidad/capturas/cálculo ya existente: localizar por símbolo y usar sólo lo necesario. `tools/calcula_f5_sin_fugas.py` y `tests/test_f5_sin_fugas.py` son puntos de entrada, no permiso para reescribir F5.

Estado observado al emitir, a verificar sin rehacer el censo:

- R01 propone MOCIBA 2021/2022; `P12_5` es consistente entre olas. El universo de respuesta fue inferido de estructura, no confirmado por una instrucción documental explícita.
- R09 propone ZA6980, México 2017, `v26`, dos dominios por `SEX`. El cuestionario mexicano agrupa «Familiares o amigos cercanos». El texto del panel que habla sólo de «un familiar» es más estrecho que el reactivo.
- FP-374 aparece `FIRMADA-CON-ALCANCE-ACOTADO`; la firma F-16 habla de seis familias, no autoriza automáticamente un experimento de dos. No heredes glosas antiguas que la llamen simplemente ABIERTA.
- Dos celdas, olas o dominios de una misma familia no crean familias independientes. Este encargo no puede declarar confirmación, resolver H0 ni recuperar el tamaño de diseño con réplicas L.

## 3. P1 · Cerrar las dos definiciones sin consumir la reserva

### R01 · MOCIBA 2021/2022

Consulta exclusivamente FD, cuestionario, manual/flujo y documentación de diseño ya adquiridos de esas dos olas. Busca el filtro que determina quién recibe `P12_5`; distingue universo elegible, no respuesta, salto válido y respuesta negativa. Confirma códigos de las variables de screening y de respuesta, ponderador y edad/universo de la encuesta. No deduzcas que todo blanco equivale a «No».

No vuelvas a comprobar indiscriminadamente todos los hashes: verifica identidad de los documentos efectivamente usados y cita página/hoja/variable. Si el flujo no puede acreditarse con ellos, conserva un estado `FILTRO-NO-ACREDITADO` para esa candidata. No abras la BD para resolverlo, no adivines el denominador y continúa con R09. Identifica el documento exacto faltante o la pregunta técnica que permitiría resolverlo.

### R09 · ISSP ZA6980

Con cuestionario mexicano y codebook/documentación internacional, confirma que la etiqueta y códigos mexicanos corresponden a `v26` del archivo integrado: una categoría del formulario nacional no se convierte sin comprobación en el código del fichero internacional. Fija filtro México, dominio por `SEX`, ponderación y manejo de no respuesta/no puede elegir. Si falta esa correspondencia, la candidata queda condicionada, no «CONGELABLE» por inferencia.

Define como propuesta el evento realmente observado: elegir «familiares o amigos cercanos» como primera fuente hipotética de préstamo grande. **No desagregues familiares de amigos ni lo equipares a recepción efectiva de dinero.** Explica qué transferencia de constructo se estaría evaluando y qué no identifica. Esa definición se somete a mesa; no cambia automáticamente la fila histórica del panel o el modelo.

### Límite de lectura común

No abras archivos de respondentes, previews de filas, frecuencias, marginales, tabulados con tasas objetivo ni resultados de estas candidatas. No uses lectores que calculen estadísticas al abrir el archivo. No leas otras olas/módulos reservados de ISSP ni MOCIBA 2024/2025. El corpus de referencia para L no se amplía con los documentos leídos. Si una página documental revela incidentalmente una cifra objetivo, no la copies al contexto de candidatos: registra alcance de exposición en la nota, retira su pretensión de evaluación ciega y continúa con la candidata no afectada.

La falta de acceso en CAJA se verifica con uno o dos intentos razonables. No exige recorrer todo el disco o adquirir de nuevo. Si el trabajo se traslada a Claude Cloud, entregar únicamente documentación permitida necesaria con procedencia y hash; nunca microdatos o resultados. No transferir en automático credenciales o archivos restringidos.

## 4. P2 · Spec concreta de factibilidad, no confirmación reducida

Crea una spec nueva, sin reescribir protocolos sellados. Estado visible: `PREPARADA-PARA-MESA · NO AUTORIZA EMISIONES NI R`. Debe contener:

1. Lista cerrada de candidatas y celdas propuestas, con familia explícita. Máximo inicial: dos familias y cuatro celdas (MOCIBA por las dos olas; ISSP por dos dominios `SEX` documentados). Si alguna no cumple, reduce la propuesta y recalcula el presupuesto; no busques sustitutos en todo el corpus.
2. Para cada celda: estimando, población, unidad, evento, códigos, filtro, denominador, missing, ponderador, diseño, periodo, escala, regla consumidora y referencias documentales. Usa una escala común explícita y conversión declarada a pp para errores; no mezcles 0–1 y 0–100.
3. Comparación primaria M frente a `L_SOLO`; B adicional sólo donde sea construible. Distingue el emisor M de F5 del motor matricial `B·θ`: no son sustituibles por compartir una letra.
4. Ruta exacta por la que M produciría una predicción del desenlace propuesto con el snapshot preexistente. Una tasa de no denuncia por miedo no es el complemento de toda denuncia; recepción efectiva de apoyo no es la intención de acudir a familiares/amigos. Si no existe un enlace explícito suficiente, marca `CANDIDATO-NO-ELEGIBLE` o `ENLACE-PENDIENTE-DE-MESA`; no inventes transformaciones ni afines M con estas familias. Un R descriptivo posible no basta para afirmar que el duelo de transferencia es ejecutable.
5. Dieta y transporte de M y L, con información permitida/prohibida; snapshot congelado, modelo/versión/cliente a firmar, réplicas, abstenciones y errores técnicos. Reutiliza la cadena de procedencia vigente en una ubicación nueva exclusiva de F6. No reutilices capturas pre-GEN2 ni directorios de emisión del piloto de Opus.
6. Orden de ejecución posterior: spec y snapshot → emisiones M/L/B admisibles selladas → apertura de R → comparación. La spec incluye la secuencia de commits y cómo se verifica que ningún resultado precedió a las emisiones.
7. Para B, explica fuente y disponibilidad. Si construir B para 2022 exige abrir el R de 2021 todavía reservado, no lo hagas en preparación ni antes de sellar las emisiones afectadas. Declara la incompatibilidad y propón su exclusión/orden autorizado; no simules independencia temporal ni uses marginales del objetivo como baseline independiente.
8. Resultado posterior por celda y familia: errores pareados, cobertura y abstenciones. Mantén separados incertidumbre muestral de R, variación de L y variación entre familias. No fabriques IC poblacionales de transferencia con dos familias, bootstrap de réplicas L o una varianza cero de R. Donde no se acredite diseño muestral, propone puntos descriptivos y la limitación, sin bloquear todo por un IC imposible.
9. Parada: terminar al completar la lista cerrada o por identidad/exposición/contrato roto; no parar cuando un resultado guste o cruce significación. El aprendizaje de factibilidad no se vuelve evidencia confirmatoria del mismo procedimiento ajustado.
10. Lo que no decide: θ, G5, M1, corte de edad, crosswalk, adopción de candidatos, generalización confirmatoria, cierre de FP-374 o de las NC de transferencia.

Incluye una tabla de presupuesto propuesto, no autorizado. Base orientativa si las cuatro celdas resultan elegibles: 4 × 8 réplicas de `L_SOLO` = 32 posiciones lógicas, 4 emisiones M y hasta 4 estimaciones R; B sólo donde proceda. Fija por separado posiciones, intentos máximos con reintentos técnicos, turnos y unidades efectivamente facturadas por el cliente vigente; no confundas estos conceptos como ocurrió en F5. No agregues `L_CORPUS` por inercia. Si no existe tarifa verificable, deja coste monetario pendiente sin inventarlo. Cero llamadas para estimar ese presupuesto.

## 5. P3 · Preparación técnica utilizable y pruebas

Materializa las tarjetas como YAML/JSON/TSV legible por la infraestructura actual y un comando reproducible de preflight **sólo sobre esas tarjetas y documentación**, sin resolver ni abrir los payloads de respondentes. Preferir las funciones existentes; si falta un adaptador pequeño, créalo en el perímetro abajo. No construyas un segundo runner general ni un framework de adjudicación.

El preflight debe distinguir preparación completa, autorización pendiente y definición/candidato insuficiente. Un archivo parseable no equivale a una celda elegible. Debe reportar las dependencias concretas, no un único «OK» que oculte la firma faltante.

Valida las transformaciones ya definidas y la interfaz con fixtures mínimos inequívocamente `SINTETICO-NO-MEDICION`, aislados del registro productivo. Casos indispensables según las rutas que se implementen:

- filtro/missing fuera del denominador correcto, sin convertirlos en «No»;
- categoría compuesta ISSP sin desagregación ficticia;
- escala válida y rechazo de escala incompatible; pesos inválidos/denominador vacío se rechazan explícitamente;
- dos olas o dos sexos siguen siendo una familia; abstención no se puntúa como cero;
- preflight no abre microdatos, no llama modelos, no escribe resultados canónicos y no declara autorizado un caso sin firma.

No añadas pruebas redundantes si la interfaz existente ya las protege: cita y ejecuta las relevantes. No modifiques medidores sellados o módulos compartidos para hacer pasar las candidatas. Si una definición sigue materialmente abierta, entrega un rechazo explícito probado en lugar de un medidor inventado.

## 6. Perímetro de escritura cerrado

- `forense/encargos/2026-09-16-GEN2-F6-FACTIBILIDAD-PREPARACION-1.md`.
- `forense/prereg-duelo-v2/F6-factibilidad-preparacion-v1_0/`: spec nueva, tarjetas y fixtures sintéticos mínimos necesarios. No agregar copias de protocolos/documentos fuente.
- `tools/f6_factibilidad_prepara.py`, sólo si la infraestructura no cubre el preflight/adaptación; reutilizar por importación sin editar componentes compartidos.
- `tests/test_f6_factibilidad_prepara.py`, si hace falta regresión específica.
- `forense/notas/2026-09-16-GEN2-F6-FACTIBILIDAD-PREPARACION-1-cierre.md`: nota breve de resultado y reservas.

Si alguno de estos destinos ya pertenece a otro trabajo, no lo sobrescribas. Resuelve si es el mismo encargo; si no, informa la colisión puntual. No amplíes el perímetro al panel histórico, el digesto, adquisición, motor o gobernanza.

## 7. Entrega, publicación e integración

Abre un único PR; la fusión queda con Jonás. Antes del push final, incorpora `origin/main` vigente a tu rama y verifica sólo premisas y pruebas afectadas. Un conflicto de significado con una firma nueva se lleva a mesa; no se resuelve escogiendo un lado automáticamente.

Ejecuta pruebas dirigidas y la comprobación de baseline pertinente, revisando antes que no derive datos reservados. Nunca recongeles baseline ni desactives un check. Reporta fallos heredados, nuevos materiales y los de cascada diferida por separado. Si falta una dependencia declarada, corrige el entorno antes de atribuirlo al código. No ejecutes toda la batería de mediciones por comodidad.

Devuelve este resumen, además del PR:

| Candidata | Definición acreditada | M elegible | Reserva preservada | Preparación técnica | Falta para correr |
| --- | --- | --- | --- | --- | --- |
| R01 | resultado real | resultado real | resultado real | comando/prueba | dependencia exacta |
| R09 | resultado real | resultado real | resultado real | comando/prueba | dependencia exacta |

Incluye: SHA base/final, enlaces a spec/tarjetas, comandos realmente ejecutados, CI, presupuesto recalculado y máximo tres decisiones materiales. Redacta el texto propuesto de firma para el alcance realmente viable y la autorización de llamadas; **no lo firmes ni lo registres como adoptado**. El cuerpo del PR indicará `CIERRE COMPARTIDO DIFERIDO — integrar después de CAREO/TRÁMITE-4` y enumerará sólo las propagaciones realmente necesarias, sin asignar IDs.

No esperes indefinidamente a Opus para entregar: termina con el PR de producto completo dentro de este perímetro. No marques pendientes de mesa como tareas incompletas de implementación. Si ninguna candidata es elegible, entrega la causa material de cada una y el único cambio/documento que la habilitaría, con preflight que rechace honestamente; no fabriques una ganadora ni una siguiente ola de auditoría.

Presupuesto de control aproximado: 20%; el resto, definición y preparación usable. No gastar la sesión en recontar el programa. Avance esperado: la siguiente sesión puede decidir y ejecutar un protocolo concreto, sin rediseñarlo ni consumir por accidente su evaluación.

## Prompt de lanzamiento

> Ejecuta íntegramente el adjunto ENCARGO-GEN2-F6-FACTIBILIDAD-PREPARACION-1.md en Codex CLI/CAJA. Actualiza origin/main, trabaja en worktree y rama propios y respeta su perímetro. Autorizo la preparación documental y técnica, pruebas exclusivamente sintéticas, commits, push y un PR; merges conmigo. Autorizo expresamente la excepción temporal de cascada del encargo: no escribas registros, numeraciones, firmas ni gobernanza compartidos. No abras microdatos/resultados reservados ni ejecutes emisiones M/L/R, adquisición o cron; ENIF 2024 localidad × edad queda reservado al piloto de Opus. Entrega spec, tarjetas, preflight/adaptación mínima comprobada, presupuesto y decisión de mesa lista para resolver. No repitas el censo del panel ni sustituyas impedimentos materiales por supuestos silenciosos. Completa todo lo posible sin esperar al trámite de Opus; informa por separado lo preparado, lo autorizado y lo ejecutado.

---

## Procedencia y consumo (fuera del texto verbatim)

Fuente local recibida de mesa: `/mnt/c/Users/PC0/Descargas MX/ENCARGO-GEN2-F6-FACTIBILIDAD-PREPARACION-1.md`.
Archivado por el propio acto el 16 de septiembre de 2026. El bloque anterior se conserva verbatim; esta nota posterior registra únicamente procedencia y consumo. Estado: en ejecución en la rama `acto/gen2-f6-factibilidad-preparacion-1`.

