# ENCARGO · GEN2-TANDAS-MEDICION-ACADEMICA

ENTORNO: CAJA
COMPUERTA: PR #693 fusionado; documentos Campos/BANSEFI y corpus ENNViH resueltos por manifiesto.
RAMA: acto/gen2-tandas-medicion-academica
MODELOS: cero llamadas nuevas; no inversión comercial.

## Resultado útil

Pasar de fuentes localizadas a una primera medición mexicana utilizable de participación y atributos de tandas. La búsqueda académica ya está hecha: no repetirla. Entregar la evidencia que realmente permita el instrumento, sin fabricar una tasa de incumplimiento ni efectos causales.

## Entradas y límites

Leer `forense/notas/2026-09-10-GEN2-ADQUISICION-DIRIGIDA-tandas.md`, manifiesto, NC-0037, documentación ENNViH de cada ola y `tools/ya_medido.py R8.2` antes de abrir una medición duplicada. Documentos adquiridos: `campos_1998_tandas_mexico_pdf` y BANSEFI–PATMIR 2006. Microdatos ENNViH 2002/2005/2009 ya están en corpus según #693; comprobarlos en CAJA.

La ruta conocida: `iiib_cr.dta` con cr04 y variables de montos/duración. Son candidatos de reactivo, no un contrato semántico ya homologado: el cuestionario manda. La expectativa hipotética de invertir en una tanda (`rg08_11`) no es comportamiento observado. D18 mantiene diferida la vía comercial.

## Fase 1 · Ficha medible y congelamiento

Elegir el primer estimando identificado por los datos y con uso concreto en R8.2: participación individual en la ventana temporal que cada cuestionario realmente mida. Preferir medición por ola; no prometer comparabilidad si las ventanas cambian. Registrar edad/universo, unidad persona, códigos especiales, enlace, ponderador de libro/ola, fecha de campo y muestra efectiva.

Definir como secundarios montos y duración sólo cuando sus preguntas, unidades y patrones de salto estén claros. No convertir “recibido o por recibir” en aporte. Congelar spec y método antes del primer cálculo; permitir entrega por ola para que un insumo bloqueado no detenga las demás.

## Fase 2 · Medir sobre el corpus existente

Ejecutar punto ponderado, n, masa, faltantes y cortes mínimos útiles por ola. Los joins siguen la identidad oficial de cada ola: no trasladar sin prueba folio/ls de 2002 al panel completo. Una tabulación independiente verifica el primer tipo de cantidad.

Si no hay UPM/estrato o réplicas oficiales, publicar el punto descriptivo y la reserva de diseño; no heredar constante+folio como diseño correcto ni declarar conservador su IC. No retener una medición útil esperando resolver FP-371 de otro objeto. Si se muestran sensibilidades, separarlas del IC del diseño.

Montos: conservar moneda nominal y año. Comparaciones reales sólo con índice oficial, base y transformación documentados; si no existe ese insumo, el primer producto no necesita inventar deflación. Duración: homologar días/semanas/meses sin convertir periodicidad de cuota en duración de la tanda.

## Fase 3 · Evidencia de grupos y avance condicionado del panel

Extraer de Campos/BANSEFI sólo tablas o afirmaciones que añadan un parámetro/rango/mecanismo al producto. Cada fila cita página, encuesta, fecha, denominador, unidad y carácter cuantitativo o cualitativo. Campos tiene discrepancia 49%/41% y pies de gráficas ambiguos entre nacional 1997 y tres ciudades 1996: etiquetar y excluir de calibración puntual lo que no pueda resolverse. El 10% por pago incompleto entre ex participantes **no es tasa de incumplimiento**.

Si la documentación resuelve de forma inequívoca la identidad longitudinal y ponderación/attrition, continuar con entrada/salida entre olas bajo una spec separada. Si no, terminar con las mediciones por ola y un residual concreto de panel. No alargar la tarea con un estudio completo de attrition para poder entregar el primer punto.

## Fase 4 · Destino y cierre

Entregar tabla `cantidad | valor/rango | población/periodo | fuente | uso permitido | uso no identificado`. Vincularla con R8.2 mediante una propuesta concreta de parámetro o escenario. La adopción nueva necesita firma del objeto; hasta entonces la evidencia queda disponible sin alterar probabilidades de incumplimiento/reputación del motor.

Actualizar NC-0037 con medición académica realizada; mantener explícitos el ledger no localizado y la vía comercial diferida. No cerrar la necesidad de datos de turnos/pagos con una encuesta individual. Recibos al publicador 09 o publicación por lote propio después de su merge. No aumentar el contador por extraer varias veces la misma tabla.

## Perímetro y aceptación

Spec/CALC(s) acotados de tandas, medidor, resultados agregados, extracción bibliográfica y nota; manifiesto sólo para el insumo nuevo estrictamente necesario; NC-0037 y administración común. No motor, cron, árbitros ni panel F5 en escritura.

Aceptación: al menos una medición nueva identificada, o demostración material del impedimento en las variables examinadas; todas las olas disponibles y compatibles avanzan; cada cifra tiene denominador y destino; no se imputa impago. Las fases documentales pueden prepararse en Cloud; la apertura de microdatos y medición termina en CAJA.

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

- `NC-0037` permanece ABIERTA en dos componentes: no se localizó un ledger mexicano abierto de grupo, organizadora, turnos, cuotas y pagos; la vía comercial continúa diferida por D18. La encuesta individual no los sustituye.
- La entrada/salida entre olas no se calculó: requiere una spec sucesora que homologue crosswalk, universo longitudinal, ponderación y attrition. No bloquea los tres puntos transversales entregados.
- No se adoptó una nueva probabilidad para R8.2 ni se modificó el motor. La propuesta de escenario espera firma del objeto.

## CONSUMIDO

Ejecutado por `ACTO GEN2-TANDAS-MEDICION-ACADEMICA`, 10/sep/2026, en CAJA/Ubuntu, worktree `/home/pc0/mm-gen2-tandas-medicion-academica`, rama `acto/gen2-tandas-medicion-academica`, `PR #700`. Commits de congelamiento y resultado: `911be66`, `3c9a6fa`, `534cfca`, `77338cf`, `d2ba406`; cierre administrativo renumerado finalmente a `ADR-470` al integrar los PR #695–#706 ya fusionados. `CALC-TANDAS-ENNVIH-0001` entrega tres puntos ponderados de participación individual en tanda durante los últimos 12 meses: 14.67% (2002), 8.58% (2005–06), 12.04% (2009–12); `verify REPRODUCE`, `CONTEXTO=IDENTICO`, 39/39. Sin IC por ausencia de UPM/estrato/réplicas oficiales, sin tasa de incumplimiento, sin adopción de R8.2 y sin incremento del contador GEN2. Como el publicador 09 ya fusionó antes de que existiera este CALC, este acto publica por lote propio sus filas en `corridas.tsv`, `resultados.tsv` y `usos.tsv`. `NC-0037` conserva abiertos el ledger de turnos/pagos no localizado y la vía comercial diferida; el panel entrada/salida queda para una spec sucesora. El merge pertenece a mesa.
