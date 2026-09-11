# ENCARGO · GEN2-CORRUPCION-UNIDAD-Y-FUENTE-GENERAL

ENTORNO: CAJA
COMPUERTA: PR #689 y PR #693 fusionados.
RAMA: acto/gen2-corrupcion-unidad-fuente
MODELOS: cero llamadas nuevas; búsqueda pública sólo donde falte evidencia.

## Resultado útil

Resolver la medición de trámites con canal ambiguo y hacer que la demanda de una tasa general llegue efectivamente a adquisición. Reutilizar la separación solicitud/entrega/unión que #689 ya implementó. Esta continuación responde a D07/D08; no repite el lote del motor.

## Estado real y entradas

- NC-0107 conserva RES-0009/0011 sin adopción: las variantes deduplicadas no reprodujeron la cifra vieja, hay 501 ID_TRA con P7_3 discordante y no existe regla reproducible de desempate histórico.
- #689 creó **NC-0153**, demanda exacta de tasa general por canal sobre trámites elegibles. #693 todavía dice que esperará a que ese objeto se inscriba. Al corte esa dependencia ya está cumplida.
- La r2 disponible es condicional en P8_4 observado entre personas que declararon corrupción. Su dominio ya está restringido. No se puede convertir en tasa general cambiando la etiqueta.

Leer cierres de GEN2-MOTOR-USOS-Y-COMPLEMENTOS, GEN2-LOTE-ENCIG-1 y cartera de adquisición de #693; `milpa/tramite.yaml`, `milpa/src/emisor.py`, CALC-ENCIG-0001, specs ENCIG vigentes, NC-0107/0111/0153 y registro canónico/vista de adquisición. `tools/ya_medido.py tramite.mordida.con_registro` evita otra medición redundante.

## Fase 1 · Unidad y resolución de duplicados

Abrir la documentación y el microdato en CAJA. Reconstruir qué identifica ID_TRA, por qué puede repetirse y si P7_3 pertenece a trámite, contacto o persona. Distinguir duplicados exactos de eventos legítimamente múltiples. No elegir primera/última fila por orden de archivo ni buscar la combinación que reproduzca GEN1.

Si el instrumento determina una solución única, documentarla y congelar una spec sucesora antes de calcular. Si no la determina, producir un tratamiento exploratorio explícito: casos de canal consistente y masa/n de los ambiguos, más sensibilidad o límites que no asignen canal sin fundamento. La elección de un nuevo estimando de producción sigue requiriendo objeto claro de mesa; no detener por ello la medición descriptiva autorizada ni la adquisición.

## Fase 2 · Medición y utilidad para el motor

Ejecutar un CALC sucesor sólo si entrega información nueva: punto/rango por canal bajo la unidad justificada, n, masa, exclusiones y peso de ambigüedad. Comparar con r2 y con la variante antigua post-sello; conservar históricos y las tasas discrepantes sin adopción. Validar numerador/denominador por una tabulación separada.

Entregar propuesta de consumo con evento, universo y activador exactos, o demostrar que r2 ya basta para ese uso y retirar la necesidad de un segundo parámetro. No aplicar tasas de la subpoblación observada a todos los trámites. Un nuevo estimando ambiguo no se adopta automáticamente. La mejora ya autorizada de impedir usos fuera de dominio sí puede probarse con las funciones actuales; no recalibrar snapshots de F5.

## Fase 3 · Adquisición dirigida con demanda existente

Usar NC-0153 como objeto, sin crear otra obligación. Actualizar la cartera que lo declaraba pendiente de definición y comprobar si ya existe una fila de adquisición que lo cubra; reutilizarla. Buscar primero en corpus, cuestionarios y tabulados ya disponibles: ENCUCI y UNAM-IIJ son candidatos, pero personas con contacto no equivalen automáticamente a trámites por canal.

Si hace falta web, buscar en fuentes primarias del productor y registrar texto del reactivo, numerador, denominador, canal, unidad, periodo y disponibilidad de diseño. Descargar sólo insumos públicos pertinentes al corpus compartido por la vía canónica. Demostrar el recorrido demanda → fila canónica → vista → selección/SONDA, con prueba en seco. El intento real productivo puede pertenecer al cron; no lanzar simultáneamente la misma adquisición.

Si ninguna fuente mide el objeto exacto, entregar el mejor estimando disponible con su población y una solicitud dirigida concreta; no concluir que no existe en el mundo. No enviar solicitudes ni aceptar acuerdos. No volver a pedir ENAFIN/WBES/ENVIPE ya adquiridos.

## Fase 4 · Cierre por componente

NC-0107 sólo cierra si se resuelve la obligación de sus dos tasas, o mesa acepta explícitamente su retiro/sustitución; una sensibilidad no equivale a adopción. NC-0153 se actualiza con demanda efectivamente enrutada, fuente/diseño disponible y siguiente fase; no cierra por crear una fila vacía. NC-0111 conserva la limitación estructural de ENCIG mientras aplique.

Entregar un resultado medible y una decisión acotada por cada residual. Las firmas de RES-0028 y DIN no bloquean este trabajo.

## Perímetro y aceptación

Specs/CALC nuevos de ENCIG sólo si necesarios, comprobantes de validación, nota y pruebas de unidad; parámetros/emisor sólo para consumo autorizado; filas propias de cola/manifiesto; NC citadas y administración común. Evitar cambiar `tools/corrida0.py`: si una necesidad es del publicador, entregar comprobante al encargo 09.

Aceptación: ambigüedad de unidad cuantificada y tratada sin desempate arbitrario; cero adopciones discrepantes silenciosas; la demanda general ya definida llega a adquisición; cada candidato muestra numerador y denominador propios. Puede correr con los otros encargos en rama separada. Coordinar las filas de adquisición con 07R; serializar sus escrituras al cierre.

## Contrato común, incluido para ejecutar este archivo por separado

Autoridad: decisiones de mesa asentadas por #685 y solicitud de preparar los siguientes encargos después de los merges. Este documento es un encargo preparado por ChatGPT: se ejecuta cuando mesa lo entregue a Codex. No convierte recomendaciones metodológicas pendientes en firmas. Base consultada: `origin/main=e76f3a1d476049d0c7adcba87535e60f507c8d91`, 11/sep/2026 UTC. Los merges ocurrieron la noche del 10/sep en México. `main` acredita lo consolidado; un PR abierto acredita trabajo en curso.

**Arranque y autorización operativa.** Lee `AGENTS.md`, este archivo completo, las instrucciones vigentes y `.claude/commands/acto.md` en lo aplicable; Codex ejecuta sus comandos equivalentes sin necesitar Claude. Reporta ruta absoluta, rama, HEAD y estado. Usa un worktree propio desde el clon existente; consulta main, ramas, worktrees y PR del mismo objeto antes de crear trabajo duplicado. Continúa una rama compatible cuando proceda. Archiva el encargo por 0-bis A.3. Al lanzarlo quedan autorizados sus cambios, commits, push y PR propio revisable; **el merge pertenece a mesa**. No cerrar PR ajenos, borrar worktrees, descartar cambios ajenos ni modificar el candado de `/despacha`.

**Entorno.** `ENTORNO` en la cabecera identifica dónde terminar. Cloud/NUBE puede trabajar código, documentos públicos y resultados agregados. Los microdatos se abren únicamente en CAJA/Ubuntu, según el repo. Usa `tools/entorno.py` y las raíces configuradas; enlaza correctamente el corpus compartido antes de concluir que falta. No inventes rutas Windows/WSL, no copies microdatos ni credenciales a Git. Si una capacidad falta, completa las fases independientes y entrega la continuación exacta; no confundas NO-VERIFICABLE con AUSENTE. Dos intentos razonables y una alternativa bastan para registrar un bloqueo.

**Concurrencia e integración.** Estas son tareas manuales separadas; no cambian la regla de una sesión del despacho automático. Verifica compuertas por ascendencia y producto, conforme a ADR-277, no buscando un título en el log. No reserves números de ADR/NC/FP: derívalos contra main al cerrar. Se aplica el precedente ya utilizado en #687–#693: **quien fusiona después renumera**. Integra main en tu rama, conserva las filas ajenas por identidad y significado y reconcilia referencias del acto; nunca reemplaces un TSV completo por la copia vieja de tu rama. Los IDs que aparecen abajo son los definitivos en main al corte, no los candidatos antiguos del cuerpo de un PR.

Usa `tools/cierre_acto.py` primero en seco y luego `--aplica` cuando corresponda para la cascada existente. Conserva una única ancla L0. Ejecuta las pruebas materiales sobre la integración final; verifica también la sincronización del HEAD remoto mediante el procedimiento vigente de `/acto`. Un push posterior a la revisión requiere comprobar su delta pertinente. Serializar merges, no necesariamente todos los trabajos.

**Perímetro administrativo permitido.** Copia archivada de este encargo, una nota de cierre, sus filas de `forense/no-corrido.tsv`, `forense/firmas-pendientes.tsv`, cola y decisiones cuando corresponda, y la cascada existente en `canon/gobernanza-v1_15.md`, `canon/estado-programa-v1_12.md`, `canon/registro-rotulos.tsv`. Resolver renombres al lanzamiento. No crear otra plantilla, índice, tablero o ADR de política para problemas ya cubiertos. Modificar las vistas globales sólo si el encargo lo incluye; de otro modo entregar comprobantes al responsable de publicación.

**Medición y decisiones.** Corre `tools/ya_medido.py <regla>` antes de clasificar o medir una regla; conserva la salida pertinente. Para una medición nueva, congela pregunta, universo, codificación, unidad, ponderador, exclusiones, método y aceptación en un commit previo al primer resultado. Un diagnóstico posterior a ver datos se etiqueta exploratorio; no se vende como prueba confirmatoria. Usa el flujo `spec-check → preflight → run → verify` cuando corresponda. Verifica fuente, periodo, muestra, transformación y relación con el parámetro. Preserva specs, resultados, snapshots y sellos históricos; una sucesora no reescribe su antecedente. Un mismo número reutilizado o un replay técnico no es otra medición independiente. `cuenta_gen2` sigue las firmas y reglas existentes; los CALC científicos nuevos explicitan objeto y cita. **Contar, reproducir, validar independientemente y adoptar son actos diferentes.**

**Límites de gasto y comunicación externa.** Salvo el ejecutor productivo configurado del cron, estos encargos no requieren llamadas nuevas a modelos. No cambiar proveedor ni abrir gasto de API para destrabar una tarea. Las vías comerciales de tandas siguen diferidas. Preparar solicitudes no autoriza firmarlas, aceptar acuerdos o enviarlas en nombre del usuario. No fabricar identidad, afiliación o recepción. Si una fase exige una decisión científica aún abierta, dejar producto y opciones concretas; continuar las demás.

**Pruebas y parada.** Validar primero el resultado material; correr el baseline requerido sin ampliarlo para ocultar fallos. No perseguir los tres FAIL históricos por rutina. No volver a arreglar NC-0141/0148: #690 ya lo hizo. Revisar el diff después de las pruebas y añadir sólo archivos deliberados. D-14: cualquier automatización adicional debe evitar un error observado con efecto material y costar menos que su corrección repetida; si no, resolver directamente. Auditoría aproximadamente 20%, salvo riesgo material en números, identidad o decisión.

Avanza entre fases ya autorizadas sin pedir confirmación. Termina cuando entregues el resultado suficiente o un residual externo concreto. Cadena de cierre: autorización → producto → evidencia → consumidor cuando aplique → obligaciones → vistas/cola → PR → merge de mesa. Una fila mixta conserva su parte pendiente. No cerrar por palabra coincidente ni por recomendación. Respuesta final del ejecutor: resultado útil, fases cumplidas/pendientes, PR/SHA, pruebas, y tabla `obligación | evidencia | cerrada/residual | siguiente acción`.

## NO-CORRIDO / RESERVAS

| qué | por qué | impacto | sucesor |
|---|---|---|---|
| Fase 2 · CALC sucesor y adopción de una nueva unidad | DECISIÓN-DE-MESA-PENDIENTE | la sensibilidad exploratoria no mueve RES-0009/0011 ni crea parámetro; NC-0107 permanece abierta | mesa: retirar/sustituir RES-0009/0011 o definir prospectivamente otra unidad |
| Fase 3 · SONDA web y adquisición productiva del objeto exacto | DIFERIDO-A:GEN2-SONDA-CRON-PRODUCCION-POST693 | NC-0153 llega a selección seca, pero no se adquirió ni midió una fuente exacta | fila `TASA_GENERAL_SOLICITUD_PAGO_INFORMAL_POR_CANAL_TRAMITES_MEXICO` y acto 07R |
| Fase 4 · cierre material de NC-0107/0111/0153 | DECISIÓN-DE-MESA-PENDIENTE | las tres obligaciones conservan su residual explícito; ninguna sensibilidad ni fila vacía se trata como cierre | mesa para NC-0107; fuente exacta vía NC-0153 para NC-0111/0153 |
