# ENCARGO · GEN2-ENIF-FINTECH-SERIE-DESCRIPTIVA

ENTORNO: CAJA
COMPUERTA: PR #689 y #694 fusionados; comprobar corpus ENIF y ausencia de tarea duplicada.
RAMA: acto/gen2-enif-fintech-serie
MODELOS: cero llamadas nuevas.

## Resultado útil y decisión ya tomada

Completar lo que NC-0121 conserva pendiente: extender a ENIF 2018/2021 el proxy descriptivo del canal del último producto entre personas con fintech, y compararlo con 2024 sólo cuando sea semánticamente válido. **D10 ya lo autorizó**; no pedir esa firma otra vez. Este objeto no está en el alcance de ENIF población #691 ni de los seis encargos 07R/09–13.

## Entradas y alcance real

Leer el cierre `forense/notas/2026-09-09-GEN2-ADQ-VERIFICACION-CAJA-cierre.md` §P2, la enmienda de #689 en `milpa/procedencia.yaml` y NC-0121/0122. Resolver los archivos manifestados `enif2018_csv`, `enif2021_csv` y documentación de las tres olas desde el corpus compartido. Los IDs concretos se confirman en el manifiesto, sin inventar rutas.

El antecedente 2024 cruza P6_2_8 con P6_6 para crédito y P5_4_8 con P5_16 para cuenta; usa FAC_PER y diseño EST_DIS/UPM_DIS. Esas variables identifican tenencia y canal del **último** producto: no el canal del producto fintech específico. “Recomendación de conocidos” no equivale a un canal de contratación. No reutilizar nombres de variable/código entre olas sin cuestionario.

## Fase 1 · Correspondencia antes de calcular

Construir una tabla por ola y familia (cuenta/crédito): texto del reactivo, población/edad, ventana, criterio de fintech, canal, códigos, no respuesta, ponderador y diseño. Evaluar cambios en definición, tipos de proveedor y productos. No considerar automáticamente equivalentes “internet”, “app” y “fintech” a través de años.

Si una ola no mide el mismo objeto, marcar ruptura/no comparable y conservar el mejor descriptivo que sí identifique. No recodificar hasta que la serie parezca continua. La ausencia de texto en el inventario de reactivos no acredita ausencia en ENIF; NC-0123 ya documentó ese límite. Leer los cuestionarios/FD existentes en vez de indexar 102 instrumentos desde este encargo.

## Fase 2 · Congelamiento y medición por ola

Pre-registrar una spec sucesora y método antes de generar resultados: cuenta y crédito separados, denominadores, especiales, pesos, categorías y aceptación. Medir todas las olas compatibles disponibles. Reportar n, masa ponderada, porcentajes por canal, faltantes y precisión compatible con el diseño cuando esté acreditado.

Usar 2024 como control existente; no recontar como nueva medición una envoltura de sus porcentajes ya publicados. Reproducir una tabulación puntual de control si hace falta comprobar la receta. Para el primer tipo nuevo, reconstruir numerador/denominador por una implementación separada. Los tamaños pequeños, en especial crédito, se informan; no fusionar categorías por buscar significación después del dato.

## Fase 3 · Producto temporal útil

Entregar tabla derivada y figura exacta por ola, distinguiendo cuenta/crédito y rupturas. Cuantificar cambios en puntos porcentuales sólo entre objetos comparables; el resto queda como comparación descriptiva rotulada. No atribuir cambios al crecimiento del mercado fintech, ni medir adquisición causal, aprobación, rechazo o recomendación a partir de este proxy.

Proponer su uso concreto como evidencia descriptiva/contextual. No alterar tasas del motor ni el M congelado de F5. Para no chocar con 11/12, entregar la actualización propuesta de `milpa/procedencia.yaml` en la nota; se integra después en el acto dueño de esa ruta. No cambiar el mapa id↔R-n basándose en una mención de la nota antigua: resolver el consumidor exacto en main.

## Fase 4 · Cierre

NC-0121 cierra cuando las olas estén medidas o la comparabilidad imposible esté demostrada con los reactivos y el residual preciso. No llamarlo serie completa si una ola tiene un objeto distinto. NC-0122 conserva la limitación del canal del producto fintech exacto, aunque D10 ya aceptó el proxy; no reabrir esa decisión.

Publicar recibos mediante el mecanismo vigente. Coordinar con 09 mientras esté abierto; si ya fusionó, incorporar main y publicar sólo el lote propio, sin transiciones ajenas. No modificar vistas globales desde una base previa al trabajo del publicador.

## Perímetro y aceptación

Specs/CALC(s) nuevos cuando haya cantidades nuevas, medidor y control de tabulación, tabla/figura y nota de fintech, NC-0121/0122 y administración común. Lectura del motor, manifiesto e inventario; cero escritura en `milpa/`, `tools/corrida0.py`, `tools/ya_medido.py` y configuración del cron.

Aceptación: cantidades 2018/2021 medidas donde el instrumento lo permita; comparación 2024 con sus rupturas; ningún canal del último producto presentado como canal fintech exacto; fuente, n y denominador por cifra. Puede correr en otro worktree de CAJA a la vez que 10/11/12, compartiendo corpus sólo en lectura y ajustando carga a la RAM disponible.

## Contrato común, incluido para ejecutar este archivo por separado

Autoridad: decisiones de mesa asentadas por #685 y solicitud de revisar decisiones y preparar trabajo adicional mientras corren los encargos 07R/09–13. Este documento es un encargo preparado por ChatGPT: se ejecuta cuando mesa lo entregue a Codex. No convierte recomendaciones metodológicas pendientes en firmas. Base consultada: `origin/main=4816101e506f527d018dd2c47467a8b57bfbd487`, 11/sep/2026 UTC. El corte incluye #694, que encoló el paquete anterior la noche del 10/sep en México; sus seis tareas están declaradas en curso por mesa. `main` acredita lo consolidado; un PR abierto acredita trabajo en curso.

**Arranque y autorización operativa.** Lee `AGENTS.md`, este archivo completo, las instrucciones vigentes y `.claude/commands/acto.md` en lo aplicable; Codex ejecuta sus comandos equivalentes sin necesitar Claude. Reporta ruta absoluta, rama, HEAD y estado. Usa un worktree propio desde el clon existente; consulta main, ramas, worktrees y PR del mismo objeto antes de crear trabajo duplicado. Continúa una rama compatible cuando proceda. Archiva el encargo por 0-bis A.3. Al lanzarlo quedan autorizados sus cambios, commits, push y PR propio revisable; **el merge pertenece a mesa**. No cerrar PR ajenos, borrar worktrees, descartar cambios ajenos ni modificar el candado de `/despacha`.

**Entorno.** `ENTORNO` en la cabecera identifica dónde terminar. Cloud/NUBE puede trabajar código, documentos públicos y resultados agregados. Los microdatos se abren únicamente en CAJA/Ubuntu, según el repo. Usa `tools/entorno.py` y las raíces configuradas; enlaza correctamente el corpus compartido antes de concluir que falta. No inventes rutas Windows/WSL, no copies microdatos ni credenciales a Git. Si una capacidad falta, completa las fases independientes y entrega la continuación exacta; no confundas NO-VERIFICABLE con AUSENTE. Dos intentos razonables y una alternativa bastan para registrar un bloqueo.

**Concurrencia e integración.** Estas son tareas manuales separadas; no cambian la regla de una sesión del despacho automático. Verifica compuertas por ascendencia y producto, conforme a ADR-277, no buscando un título en el log. No reserves números de ADR/NC/FP: derívalos contra main al cerrar. Se aplica el precedente ya utilizado en #687–#693: **quien fusiona después renumera**. Integra main en tu rama, conserva las filas ajenas por identidad y significado y reconcilia referencias del acto; nunca reemplaces un TSV completo por la copia vieja de tu rama. Los IDs que aparecen abajo son los definitivos en main al corte, no los candidatos antiguos del cuerpo de un PR.

Usa `tools/cierre_acto.py` primero en seco y luego `--aplica` cuando corresponda para la cascada existente. Conserva una única ancla L0. Ejecuta las pruebas materiales sobre la integración final; verifica también la sincronización del HEAD remoto mediante el procedimiento vigente de `/acto`. Un push posterior a la revisión requiere comprobar su delta pertinente. Serializar merges, no necesariamente todos los trabajos.

**Perímetro administrativo permitido.** Copia archivada de este encargo, una nota de cierre, sus filas de `forense/no-corrido.tsv`, `forense/firmas-pendientes.tsv`, cola y decisiones cuando corresponda, y la cascada existente en `canon/gobernanza-v1_15.md`, `canon/estado-programa-v1_12.md`, `canon/registro-rotulos.tsv`. Resolver renombres al lanzamiento. No crear otra plantilla, índice, tablero o ADR de política para problemas ya cubiertos. Modificar las vistas globales sólo si el encargo lo incluye; de otro modo entregar comprobantes al responsable de publicación.

**Medición y decisiones.** Corre `tools/ya_medido.py <regla>` antes de clasificar o medir una regla; conserva la salida pertinente. Para una medición nueva, congela pregunta, universo, codificación, unidad, ponderador, exclusiones, método y aceptación en un commit previo al primer resultado. Un diagnóstico posterior a ver datos se etiqueta exploratorio; no se vende como prueba confirmatoria. Usa el flujo `spec-check → preflight → run → verify` cuando corresponda. Verifica fuente, periodo, muestra, transformación y relación con el parámetro. Preserva specs, resultados, snapshots y sellos históricos; una sucesora no reescribe su antecedente. Un mismo número reutilizado o un replay técnico no es otra medición independiente. `cuenta_gen2` sigue las firmas y reglas existentes; los CALC científicos nuevos explicitan objeto y cita. **Contar, reproducir, validar independientemente y adoptar son actos diferentes.**

**Límites de gasto y comunicación externa.** Salvo el ejecutor productivo configurado del cron, estos encargos no requieren llamadas nuevas a modelos. No cambiar proveedor ni abrir gasto de API para destrabar una tarea. Las vías comerciales de tandas siguen diferidas. Preparar solicitudes no autoriza firmarlas, aceptar acuerdos o enviarlas en nombre del usuario. No fabricar identidad, afiliación o recepción. Si una fase exige una decisión científica aún abierta, dejar producto y opciones concretas; continuar las demás.

**Pruebas y parada.** Validar primero el resultado material; correr el baseline requerido sin ampliarlo para ocultar fallos. No perseguir los tres FAIL históricos por rutina. No volver a arreglar NC-0141/0148: #690 ya lo hizo. Revisar el diff después de las pruebas y añadir sólo archivos deliberados. D-14: cualquier automatización adicional debe evitar un error observado con efecto material y costar menos que su corrección repetida; si no, resolver directamente. Auditoría aproximadamente 20%, salvo riesgo material en números, identidad o decisión.

Avanza entre fases ya autorizadas sin pedir confirmación. Termina cuando entregues el resultado suficiente o un residual externo concreto. Cadena de cierre: autorización → producto → evidencia → consumidor cuando aplique → obligaciones → vistas/cola → PR → merge de mesa. Una fila mixta conserva su parte pendiente. No cerrar por palabra coincidente ni por recomendación. Respuesta final del ejecutor: resultado útil, fases cumplidas/pendientes, PR/SHA, pruebas, y tabla `obligación | evidencia | cerrada/residual | siguiente acción`.
