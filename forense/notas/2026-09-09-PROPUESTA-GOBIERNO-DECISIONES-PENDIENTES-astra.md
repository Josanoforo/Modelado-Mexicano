# PROPUESTA · Gobierno de decisiones pendientes del programa

ChatGPT / Astra · 9 de septiembre de 2026 · para adecuación, registro y despacho por dirección (Claude). Propuesta de diseño; no implementada ni sellada.

**Principio rector: la máquina muestra qué falta y qué evidencia existe; dirección comprueba la cobertura; mesa decide y el merge sella.**

Claude: adapta esta propuesta contra `origin/main` del día, archívala por 0-bis A.3 y prepara el encargo por el circuito vigente. No asignes a este documento un número de acto, ADR o FP tomado de memoria. El registro del origen externo debe ocurrir antes de despachar la ejecución. Esta propuesta sirve para preparar ese encargo; no constituye firma de las decisiones particulares que el derivador encuentre.

## 1. Base observada y alcance de la propuesta

Corte consultado: `Josanoforo/Modelado-Mexicano`, `main` en `b711ee05046ace5603eea610068dffdc67ee93a0`. Se leyeron los dos TSV, el digesto y su comando, las primitivas de estado, las instrucciones v2.13, el contrato de ejecución, partes relevantes de `/acto` y la nota de bandeja. No se ejecutó el programa ni se reconstruyó el barrido de ocho cierres.

| Observado | Interpretación | Consecuencia propuesta |
|---|---|---|
| El brief de dirección reporta ocho filas abiertas con evidencia de cierre ya existente, encontradas el 8/sep. No identifiqué independientemente las ocho. | Hay un defecto reportado de conciliación; no equivale a ocho decisiones todavía pendientes hoy. | Dirección debe citar los ocho IDs y su evidencia original al registrar; reutilizarlos como casos de aceptación, sin abrir una auditoría general. |
| `firmas-pendientes.tsv` contiene `id`, `qué_se_firma`, `dónde`, `creado`, `gatea`, `estado`, `firmada_en`, `ejecutada_en`, `encargo`. NC contiene identidad, pieza, razón, impacto, sucesor, estado y cierre. | Ya existen campos para pregunta, origen, dependencia y evidencia. | Derivar la vista; no crear otro registro maestro. |
| `tools/estado_comun.py` comparte lectura de FP y reconocimiento de `ABIERTA` con glosa. | Reimplementar el parser puede reintroducir el defecto de prefijos ya medido. | Reutilizar los lectores y tokens vigentes; no buscar palabras sueltas como estado. |
| `tools/digesto_tramite.py` ya interpreta `vence: AAAA-MM-DD` en `gatea` y compara NC contra un corte previo. | Ya existen calendario y mecanismo incremental aprovechables. | Extender el derivador existente; no añadir cron ni almacén de snapshots. |
| `/tramite` permite propagar una firma verbatim en FP; excluye expresamente `no-corrido.tsv` de su perímetro. | El bucle de cierre NC necesita una modificación explícita del contrato. | Proponer una autorización limitada a sus campos de estado/cierre, condicionada a evidencia suficiente. |
| FP-362 conserva prefijo `ABIERTA` y declara firma para CALC-0003-v3, con reserva para v4. | Firma parcial y sucesora no son equivalencia de objeto ni cierre total. | Usar este caso como control negativo: la vista debe conservar el residual de v4. |
| La nota de bandeja excluye tareas sin acción actual aunque mantengan tokens de acceso pendientes, y distingue manos de mesa de reintentos de máquina. | Estado de adquisición y necesidad de una decisión no coinciden siempre. | Mostrar el tipo de acción y el desbloqueo; no convertir toda descarga manual en firma pendiente. |
| Coexisten la regla D-14 de instrucciones y una fila `id=D-14` en FP, declinada por proceso. | El identificador desnudo es ambiguo. | Cualificar citas por documento; no reabrir esa fila por invocar el gate de automatización. |

Fuentes primarias del corte: [FP](https://github.com/Josanoforo/Modelado-Mexicano/blob/b711ee05046ace5603eea610068dffdc67ee93a0/forense/firmas-pendientes.tsv), [NC](https://github.com/Josanoforo/Modelado-Mexicano/blob/b711ee05046ace5603eea610068dffdc67ee93a0/forense/no-corrido.tsv), [digesto](https://github.com/Josanoforo/Modelado-Mexicano/blob/b711ee05046ace5603eea610068dffdc67ee93a0/tools/digesto_tramite.py), [trámite](https://github.com/Josanoforo/Modelado-Mexicano/blob/b711ee05046ace5603eea610068dffdc67ee93a0/.claude/commands/tramite.md), [instrucciones](https://github.com/Josanoforo/Modelado-Mexicano/blob/b711ee05046ace5603eea610068dffdc67ee93a0/instrucciones-proyecto-v2_13.md), [bandeja](https://github.com/Josanoforo/Modelado-Mexicano/blob/b711ee05046ace5603eea610068dffdc67ee93a0/forense/notas/2026-09-08-GEN2-TRAMITE-BANDEJA-bandeja-mesa.md).

## 2. Una vista única, generada por el digesto existente

Extender `tools/digesto_tramite.py` para emitir una vista de mesa y consultar una decisión. Interfaz propuesta, **todavía inexistente** y ajustable por dirección:

```bash
python3 tools/digesto_tramite.py --mesa --ref origin/main --fecha AAAA-MM-DD --stdout --sin-suite
python3 tools/digesto_tramite.py --mesa --ref origin/main --id FP-362 --stdout --sin-suite
```

El comando resuelve una vez la ref a SHA. Todos sus cruces usan ese corte; imprime SHA, fecha, fuentes examinadas y limitaciones. La fecha usa la zona operativa vigente, fijada por dirección. No hace fetch ni escribe estados; quien lo invoca refresca el remoto. Sin red puede mostrar el último corte conocido, pero no llamarlo «remoto actualizado».

Entradas: FP, NC y, para la bandeja de acciones humanas, el registro canónico de adquisición ya existente. El Markdown de bandeja es contexto histórico; no una segunda entrada editable que pueda contradecir al registro. Leer además los documentos y decisiones ya citados por esas filas para obtener evidencia y contexto. La vista no puede deducir una firma ausente de los TSV sin consultar dónde se registró.

Una tabla principal, con detalle por ID, responde:

| Campo de presentación | Derivación |
|---|---|
| Referencia y filas relacionadas | ID original y fuente; enlaces explícitos entre FP, NC y objeto de adquisición. |
| Pregunta o acción exacta | `qué_se_firma` o pieza/receta citada; separar el residual si ya hubo cobertura parcial. |
| Quién debe actuar y para qué | Mesa decide; mesa ejecuta algo ya autorizado; trámite concilia; máquina ejecuta/reintenta. Si falta evidencia, indicar «por aclarar». |
| Edad y vencimiento | Fecha original, edad por fila y `vence:` existente. Fecha desconocida se declara, no se sustituye por cero. |
| Qué desbloquea | `gatea`/`impacto` y consumidor citado. Si no está documentado, decirlo; no inferir prioridad causal. |
| Qué ya está cubierto | Decisión relacionada, objeto/versión, alcance, cita y parte que sigue pendiente. |
| Evidencia y siguiente acción | Cita exacta, comprobación pendiente o propuesta de conciliación. |

Las etiquetas de acción y de evidencia son presentación: **no son estados nuevos ni se escriben en `estado`**.

Reglas de composición:

- Vincular NC cuyo sucesor sea FP a esa FP, pero no equiparar dependencia con duplicidad. Una FP firmada puede dejar la ejecución de NC intacta.
- Agrupar como una sola pregunta únicamente cuando hay identidad y cobertura explícitas. Mantener visibles los IDs y residuos de todas las filas; no sumar FP y NC como si fueran decisiones independientes.
- Un NC con sucesor «mesa» sin FP visible aparece como caso a aclarar. Trámite no crea automáticamente una firma nueva.
- Conservar un anexo compacto de reintentos de máquina y dependencias sin acción hoy dentro de la misma vista. No obligar a mesa a buscarlos en otra bandeja.
- Ordenar primero plazos vencidos y bloqueos actuales documentados; después el resto por edad. No construir puntuaciones de urgencia. Los casos de conciliación se distinguen de preguntas sustantivas.
- Emitir el conjunto completo. Si el resumen se limita por legibilidad, incluir el total y el detalle íntegro accesible con el mismo comando; no ocultar candidatos antiguos detrás de un tope.
- La consulta por ID también devuelve decisiones ya tomadas. Una solicitud sin ID puede buscar texto/objeto en los campos y documentos permitidos; sus coincidencias son candidatas, nunca prueba automática de cobertura.

## 3. Bucle de cierre en cada ejecución de `/tramite`

**Descubrimiento completo de pendientes; conciliación dirigida por evidencia.** Cada ciclo exitoso considera todas las filas abiertas, no solo las nuevas. Puede reutilizar trabajo derivado del corte anterior si comprueba que tampoco cambiaron las fuentes de evidencia relevantes. Un diff únicamente de los TSV perdería precisamente las firmas asentadas en otro documento.

Proceso mínimo:

1. Resolver el corte y leer las filas abiertas con los lectores existentes.
2. Buscar sus IDs y referencias explícitas en fuentes autoritativas versionadas: campos de firma/cierre, encargos, notas de resultado, decisiones y documentos citados. Excluir digestos/vistas y la repetición del propio texto original como prueba independiente.
3. Emitir las candidatas junto con el fragmento que las produjo y lo que falta verificar. Revisar también los casos sin enlace claro: una glosa o una decisión conversacional no registrada no se descubrirán siempre mediante el ID.
4. Trámite lee las candidatas y las abiertas no resueltas por cruces inequívocos. Si el presupuesto no permite completar esta lectura, lista IDs no revisados y declara ciclo de conciliación incompleto. No publica «cero cerrables» como conclusión global.
5. Preparar en el PR de trámite existente los cambios de propagación demostrados. Los casos que exijan interpretar o tomar una decisión vuelven a dirección/mesa en la misma vista.
6. Mesa fusiona. El ciclo siguiente deriva desde `main` el nuevo estado; una propuesta en un PR abierto no desaparece de la lista consolidada. Mostrar «propuesto en PR» como información, sin cambiar la autoridad de `main`.

| Evidencia encontrada | Qué deriva la máquina | Qué debe comprobarse antes de cambiar la fila |
|---|---|---|
| Firma fechada que identifica exactamente la FP y su objeto | Referencia, fecha, texto y correspondencia explícita | Cobertura íntegra o parcial y ausencia de condición material incumplida. Propagar solo lo firmado. |
| Sucesora firmada | Vínculo y estado de la sucesora | Que absorbe explícitamente la obligación original; enumerar el residual. Firmar la sucesora no acredita ejecutarla. |
| PR fusionado o relanzamiento | Merge comprobado y archivos afectados | Que el contenido satisface la pieza concreta, no solo que el título o la rama se parecen. Lanzado no significa ejecutado. |
| Glosa «ejecutada» con token inicial `ABIERTA` | Contradicción textual y candidato a revisión | Si es cierre total, parcial, cita histórica o negación. FP-362 debe permanecer abierta en su residual. |
| Objeto, versión, objetivo o universo distinto | Diferencia explícita cuando está representada | Si la decisión anterior aplica al nuevo caso: juicio de dirección/mesa. |
| Ausencia de citas, referencias rotas o fuentes inaccesibles | Falta de evidencia comprobable | Localizar/registrar la evidencia; nunca cerrar por antigüedad o parecido. |

Toda propuesta de cierre necesita: fila/pieza exacta; firma o resultado habilitante; cita permanente a SHA y localizador; transición al token vigente; fecha de decisión o ejecución si consta, separada de la fecha de conciliación; universo cubierto y residual. Usar los campos de evidencia existentes para la explicación, sin agregar columnas por defecto ni reescribir el encargo verbatim.

Para una FP se distingue firma de ejecución. Para una NC, la prueba de cierre depende de la obligación original: si faltaba decidir, una decisión puede bastar; si faltaba ejecutar o verificar, hace falta esa evidencia. Rechazar, diferir o sustituir una obligación exige decisión explícita y el token ya admitido correspondiente. Nada se borra.

**Cambio contractual necesario:** ampliar `/tramite` para permitir actualizar exclusivamente `estado`, `cerrado_por` y `fecha_cierre` de NC cuando la cobertura esté demostrada; preservar las demás celdas originales. En FP mantener la misma restricción a propagación fundada, con transición por el vocabulario vigente, sin declarar `EJECUTADA` por una mera firma. Si una aclaración exige modificar contenido sustantivo, la hace el acto de dirección correspondiente.

Reutilizar un solo PR de trámite. La detección no tiene cupo; el tamaño de los cambios revisables sí puede conservar el límite vigente. Candidatas pendientes siguen visibles con su primera detección, derivada del digesto versionado anterior cuando exista, sin una cola persistente adicional. Antes de actualizar el PR comprobar que fila y evidencia no cambiaron en el nuevo `main`; rederivar lo afectado y conservar el trabajo ajeno.

## 4. Prueba de cobertura antes de pedir otra decisión

Pregunta obligatoria: **«¿Qué parte exacta de esta petición sigue sin resolver después de consultar lo ya firmado para el mismo objeto y alcance?»**

Dirección obtiene la vista por ID u objeto, sigue las referencias relacionadas y compara cuatro elementos: objeto/versión, decisión solicitada, condiciones y universo. Presenta una sola conclusión con cita:

- Cubierto íntegramente: propagar/conciliar; no volver a preguntar.
- Cubierto parcialmente: preguntar solo el residual, conservando la firma previa.
- Sustituido explícitamente: seguir a la sucesora y mostrar lo que absorbió y lo que dejó pendiente.
- Cambió el alcance: mostrar la diferencia y solicitar reexamen de esa parte.
- Sin cobertura encontrada: indicar fuentes/patrones y frontera examinada; presentar la decisión con esa reserva.

Estos son veredictos de cobertura, no estados de los TSV. Compartir tema o aparecer en el mismo PR solo produce una relación candidata. No afirmar que una decisión nunca existió porque no apareció en el universo consultado.

El contexto conversacional más reciente puede ser autoridad decisional, pero si no está en el repo se declara esa procedencia y dirección lo registra antes de encargar propagación mecánica. El programa no simula acceso a conversaciones que no conserva.

Formato de conversación, corto y siempre el mismo:

> **[Referencia] Necesito que decidas:** pregunta exacta. **Ya quedó cubierto:** decisión y cita, con alcance. **Falta:** residual. **Desbloquea:** resultado/consumidor o «sin bloqueo actual documentado». **Recomiendo:** opción y razón. **Revisar de nuevo si:** fecha o cambio material. **Si no respondes:** permanece pendiente; consecuencia concreta de esperar.

Si lo único pendiente es enviar un correo o descargar un archivo ya autorizado, encabezar «Necesito esta acción», y citar la autorización. No pedir otra firma por inercia.

## 5. Identidad estable sin renumerar historia

La referencia canónica es **documento de origen + ID original**; la cita probatoria añade el SHA y el localizador. FP-01 no se transforma en FP-001. No usar números de línea como identidad, ni hashes del texto mutable.

| Situación | Convención mínima |
|---|---|
| FP existente | `forense/firmas-pendientes.tsv#FP-362`. La vista puede abreviar a FP-362 cuando sea inequívoco. |
| NC existente | `forense/no-corrido.tsv#NC-0063`. Conserva su identidad de deuda de ejecución; enlaza a FP si espera una decisión. |
| Fila histórica D-14 | `forense/firmas-pendientes.tsv#D-14`, diferente de `instrucciones-proyecto-v2_13.md#D-14`. |
| D-1..D-6 conversacionales | Citar el documento donde se archive esa conversación/acto, con fecha, sesión/acto y rótulo local. La fecha sola no basta si hubo dos D-1 ese día. |
| Firma en glosa | Reutilizar la FP a la que pertenece y dar cita del fragmento. Si no tiene identidad explícita, dirección fija un ancla en el lugar permitido de registro, sin alterar el verbatim histórico. |
| Nueva decisión pendiente | Usar A.12 y un FP nuevo solo si realmente es una pregunta nueva. El rótulo conversacional queda como alias de origen dentro de los campos existentes. |

Enlace no equivale a identidad: `NC → FP` suele significar dependencia. Solo una declaración explícita de equivalencia permite agrupar como misma pregunta. No inferir transitivamente que todas las filas relacionadas se cierran juntas.

No crear tabla de aliases ni catálogo universal de decisiones. Cuando falte un enlace necesario, dirección lo fija en el registro/campo existente adecuado o en la nota de conciliación citada desde los campos permitidos; el parser no inventa la relación. Aplicar la convención al conjunto activo y a las decisiones que se toquen, no migrar toda la historia.

## 6. Caducidad: vence la pregunta tal como fue formulada, no decide el silencio

Pendientes:

- Reutilizar `vence:` en `gatea` para fecha explícita de revisión. Al alcanzarla, la pregunta sigue abierta y se presenta para confirmar prioridad, reformular, diferir o declinar expresamente.
- Cuando no haya fecha, proponer **siete días desde su creación como umbral de revisión**, no como cierre ni plazo fatal. Es una elección reversible de diseño, no un umbral observado. Dirección puede ajustarlo al ritmo vigente al registrar esta propuesta.
- No reiniciar edad por editar una nota o regenerar un digesto. Si mesa difiere, registrar fecha/condición de retorno y conservar la edad original.
- Un evento puede adelantar la revisión: desapareció el consumidor, cambió el objetivo, llegó una fuente que resuelve la pregunta o la opción dejó de estar disponible. La máquina señala el cambio representado; dirección evalúa su efecto.
- Para NC enlazada a una FP, mostrar el plazo de esa FP y la edad propia de NC. Una NC sin pregunta de decisión no recibe artificialmente un plazo de firma.

Decisiones tomadas:

- Conservan validez para su objeto y universo originales. No caducan por cambiar `HEAD`, pasar siete días o publicarse una versión irrelevante.
- Antes de reutilizarlas ante objetivo, versión, consumidor, universo o supuesto material distinto, ejecutar la prueba de cobertura. Una decisión de no adquirir algo para el objetivo anterior no se hereda automáticamente al nuevo.
- Los cambios de archivo son indicios de revisión, no prueba de caducidad semántica. Aplicar A.10 y el vocabulario vigente de vencimiento en alcance a la parte afectada cuando dirección/mesa lo determine.
- Preservar la decisión anterior, su cita y su alcance; registrar la revisión como sucesora cuando exista una pregunta nueva. No sobrescribir retroactivamente lo decidido.

Una condición expresada solo en lenguaje natural se relee al cambiar el contexto o antes de heredar la decisión. No se promete detectar automáticamente todo cambio de objetivo ni se crea un motor de reglas para ello.

## 7. Gate D-14 y presupuesto de aparato

Las respuestas siguientes distinguen justificación de evidencia de coste. La ventaja económica es una estimación de diseño que dirección debe aceptar contra el árbol; no se ha cronometrado una implementación.

| Pieza | Defecto real que evita | ¿Puede cambiar una decisión? | ¿Más barato que repetir la corrección manual? |
|---|---|---|---|
| Extensión del único derivador: vista, cruces y candidatas | Ocho cierres omitidos reportados; firmas parciales y estados en glosa comprobados | Sí: puede pedir una firma repetida o dar por cubierta una versión distinta | Sí, estimación condicionada a reutilizar lectores, digesto e historia existentes; sin servicio, dependencias externas ni motor semántico. |
| Extensión de la rutina vigente y permiso NC limitado | Trámite no puede asentar cierres NC en su perímetro actual | Sí: mantiene bloqueos aparentes y puede provocar encargos redundantes | Sí, estimado: lectura dirigida y propagación dentro del PR que ya existe; cero rutinas nuevas. |
| Protocolo de cobertura e identidad | D-14 ambiguo; FP-362 cubre v3 y no v4; dispersión descrita por dirección | Sí: cambia el objeto de lo que mesa cree firmar | Sí, estimado: una pregunta y citas en los mismos campos; sin catálogo ni migración masiva. |
| Revisión de vigencia con calendario existente | El brief reporta deudas heredadas que pierden sentido al cambiar el objetivo; el parser de vencimientos ya existe | Sí: puede mantener o retirar trabajo por una razón que ya no aplica | Sí, estimado: ampliar el uso de `vence:` y la conversación. La detección semántica automática queda excluida por falta de justificación de coste. |

Presupuesto: **un derivador existente ampliado + una rutina existente ampliada + un protocolo de conversación**. Los permisos de la rutina y los lectores auxiliares se ajustan solo en lo necesario. Los tests dirigidos protegen los errores observados; no constituyen una nueva capa de seguimiento. Si la adaptación exige una segunda fuente maestra o automatización semántica, recortar esa parte y dejar lectura humana.

## 8. Validación propuesta y límite de la garantía

La afirmación «ninguna fila cerrable sobrevive más de una rutina sin ser candidata» requiere dos niveles honestos:

1. **Enlaces explícitos:** garantía mecánica. En el primer ciclo completo cuyo corte incluya la evidencia, toda abierta con referencia habilitante aparece como candidata. Se consideran todas las abiertas aunque no hayan cambiado los TSV.
2. **Glosas o relaciones implícitas:** garantía operativa por lectura de la rutina, no por parser. Si queda cualquier abierta sin revisar, se publica la lista y el ciclo no acredita cobertura completa. El objetivo de aceptación no se cumple escondiendo esa limitación.

Un tick fallido o sin acceso no cuenta como revisión completada. La huella existente de rutinas debe reflejarlo; la siguiente ejecución recorre las abiertas completas. Se propone emitir la vista de lectura/huella aun si otra comprobación impide publicar el PR, respetando las restricciones vigentes y sin saltarse la compuerta de escritura. Dirección debe adecuar explícitamente ese orden, pues `/tramite` hoy pone la suite antes del digesto.

Pruebas dirigidas dentro de las existentes cuando sea posible:

- Reproducir los ocho casos que dirección cite, usando su fila anterior al cierre y evidencia posterior. Cada uno debe producir candidata o una limitación humana explícita; ninguno puede desaparecer silenciosamente. No es requisito dejarlos abiertos en producción para probarlo.
- FP-362: la firma de v3 no cierra v4. La vista muestra lo cubierto y el residual, sin pedir otra vez lo ya firmado.
- Glosa y tokens: `ABIERTA -- … EJECUTADA para una parte` sigue abierta. D-14 de instrucciones y la fila D-14 no colisionan.
- Sucesora/relanzamiento: un PR abierto, mera mención, firma de alcance distinto o relanzamiento sin resultado no acredita cierre. Estos controles prueban la frontera de los casos reales, no un catálogo de escenarios hipotéticos.
- Cierre independiente del TSV: añadir evidencia pertinente en una nota/decisión sin modificar la fila debe producir candidata en el siguiente corte. Una fila que solo depende de la decisión conserva su ejecución pendiente.
- Repetición y lectura: mismo SHA y fecha producen la misma vista; `--stdout` no modifica archivos; tras merge desaparece únicamente la obligación efectivamente cerrada. Un nuevo ciclo no crea otro PR si el de trámite sigue abierto.
- Vencimiento: superar `vence:` o el umbral de revisión incrementa el aviso, nunca firma, declina ni borra. Cambiar una fuente ajena no invalida decisiones.

Comprobar en el cierre del encargo: cobertura completa de los ocho casos aportados, ausencia de los falsos cierres anteriores, ninguna fila fuente alterada por el derivador, y visualización inequívoca de lo que necesita decisión frente a ejecución/conciliación. Comparar fallos heredados con baseline; no limpiar deuda ajena.

Durante los primeros ciclos registrar en el digesto existente solo lo necesario: candidatas detectadas, propagadas/propuestas en PR y pendientes de lectura. Una candidata falsa o un cierre explícito omitido obliga a corregir la regla afectada. Revisar el coste bajo la política de retiro D-14 vigente, sin instalar otra rutina para vigilar esta rutina.

## 9. Qué no hace y devolución a dirección

No decide por silencio, similitud textual, edad o CI verde. No firma ni fusiona automáticamente. No convierte NC en FP por defecto. No confunde decisión con ejecución. No reconstruye decisiones ausentes de conversaciones invisibles. No altera los estados existentes, numera otra serie, reabre toda la historia, audita el repo entero ni agrega un cron. La conciliación no cuenta como nueva medición: vale porque elimina bloqueos y preguntas redundantes.

Preguntas concretas para dirección al adaptar, sin detener las piezas ya diseñadas:

- ¿Cuáles son los ocho IDs y sus citas habilitantes? ¿Cuáles eran de firma, ejecución o sustitución?
- ¿Dónde quedó registrado el protocolo conversacional vigente y cuáles de sus reglas se pueden reutilizar literalmente?
- ¿Qué tokens y transiciones exactas admite hoy cada TSV para firma parcial, ejecución, sustitución y declinación?
- ¿Cuál es la ubicación permitida de las referencias y estampas de cierre cuando la evidencia solo vive en glosas? Conservar las columnas inmutables de NC.
- ¿Qué metadatos del objeto de adquisición bastan para derivar responsable y acción? Los que falten quedan señalados; no adivinados.
- ¿El ciclo completo actual puede revisar todas las abiertas ambiguas? Si no, declarar el límite y recortar el trabajo ajeno a conciliación; no rebajar en silencio el criterio de cobertura.

Dirección devuelve: referencia del 0-bis archivado; encargo ajustado; comando final; perímetro y permisos de `/tramite`; ocho casos de aceptación; destino y estado real del despacho. Registrar lo no ejecutado por el mecanismo existente. El merge de mesa sella el diseño implementado; los cierres individuales conservan cada uno su evidencia y alcance.

**Decisión que habilita esta propuesta:** aprobar una extensión acotada del circuito existente para que mesa pueda consultar en un comando qué pregunta sigue viva, qué ya está cubierto y qué solo necesita asentarse. El proyecto avanza al retirar deuda ficticia y proteger decisiones sobre objetos distintos.
