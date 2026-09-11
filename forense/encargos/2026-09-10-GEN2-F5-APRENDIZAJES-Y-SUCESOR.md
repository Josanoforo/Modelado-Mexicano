# ENCARGO · GEN2-F5-APRENDIZAJES-Y-SUCESOR

ENTORNO: NUBE
COMPUERTA: PR #687, #689 y #691 fusionados; snapshots y salidas de TRIADA disponibles.
RAMA: acto/gen2-f5-aprendizajes-sucesor
MODELOS: cero capturas nuevas, cero llamadas a Claude u otro modelo.

## Resultado útil

Explicar qué parte del error observado puede orientar la próxima mejora del motor y qué permitiría cubrir las dos celdas con abstención persistente. Entregar un siguiente experimento propuesto con pregunta y criterio de parada concretos. **No repetir las 224 llamadas, no cambiar el veredicto de TRIADA-0002 y no abrir F6 por inferencia.**

## Estado consolidado

#687 completó 224/224 capturas: 171 puntos, 53 abstenciones válidas, cero errores técnicos/malformados/de identidad. L_SOLO y M tienen punto en 14/14; L_CORPUS, en 12/14. U3=12/14. MAE en U3: L_SOLO 3.957362 pp, L_CORPUS 3.889026 pp, M 4.986673 pp. Las tres pareadas son INCONCLUSAS; resultado SIN-GANADOR-UNICO. No prueba equivalencia entre brazos ni superioridad general de uno.

NC-0152 conserva DIN-M-01 y TRA-M-07: sus 16 respuestas L_CORPUS son abstenciones válidas. No son llamadas faltantes. NC-0146/0147 ya cerraron y el diagnóstico previo #684 no se repite.

Leer `F5-completa-{resultado,extraccion,plan}-v1_0`, `F5-completa-spec-v1_0.md`, `snapshot-M-triada-v1_0.json`, `universo-triada-v1_4.tsv`, capturas ya archivadas, `CALC-TRIADA-0002` y cierres de #687/#689/#691. Las versiones exactas se resuelven por ruta/hash; el motor vivo posterior no sustituye al M congelado del experimento.

## Fase 1 · Descomponer el resultado existente

Derivar una tabla por celda/familia con R, M congelado, medianas de los dos L, réplicas válidas/abstenciones, errores absolutos y contribución al MAE. Mantener U3 y reportar aparte las dos celdas excluidas. Reconciliar aritméticamente el agregado con el resultado sellado sin ejecutar nuevos CALC de medición ni tocar salidas congeladas.

Mostrar tamaños de familia: seis celdas cívicas y tres ENIGH relacionadas no son nueve réplicas independientes de un mecanismo. Una descomposición por familia es exploratoria; no adjudicar “ganadores por familia” con n mínimo ni inventar significación post-hoc. Separar error del panel, variación de capturas e incertidumbre del árbitro, que el cálculo actual no integra por completo.

## Fase 2 · Relacionar errores con el uso del motor

Para las contribuciones materiales al error, seguir el parámetro del snapshot M hasta fuente, año, población, evento y transformación. Comparar con los contratos ya corregidos en #689/#691 para distinguir mejora implementada después del snapshot, limitación de fuente y defecto aún vigente. La repetición de un valor M entre celdas puede ser una regla legítima o extrapolación: comprobar el contrato antes de llamarla error de código.

Entregar como máximo tres acciones priorizadas por resultado esperado: corregir un uso, medir un parámetro pertinente o cambiar el diseño de evaluación. No ajustar M usando los R del mismo panel y después evaluar sobre ellos como prueba nueva. No alterar snapshots. Si se calcula una sensibilidad con el motor actual, rotularla como reanálisis sobre un panel conocido, sin tratarla como confirmación independiente.

## Fase 3 · Las dos abstenciones y el diseño sucesor

Leer las 16 justificaciones existentes de DIN-M-01/TRA-M-07 y el paquete efectivamente entregado. Clasificar si falta documento, evidencia cuantitativa, definición o si el brazo decide abstenerse aun con acceso correcto. Vincular demandas a NC-0153/adquisición cuando sean el mismo objeto; no generar otra búsqueda general.

Proponer prospectivamente la menor modificación que responda una pregunta nueva: dos celdas pueden bastar para probar acceso/cobertura, pero no completan retrospectivamente el ranking de 14 si cambia tratamiento, modelo o ventana. Si se propone comparación de brazos, explicitar captura contemporánea, presupuesto y condición de estabilidad del modelo; no reciclar controles incompatibles. Definir de antemano éxito, abstención aceptable, límite de reintentos y criterio de parada. Una abstención válida no se arregla forzando una cifra.

## Fase 4 · Producto y residual

Entregar tabla reproducible, figura compacta de contribución al error y nota breve de decisión con el próximo cambio recomendado y qué podría refutarlo. Éste es un diagnóstico técnico de F5, no el informe final del programa ni una firma de D21/F6.

NC-0152 conserva pendiente la cobertura mientras no exista el producto que exige; un diseño propuesto no equivale a capturas ejecutadas. No abrir nuevas llamadas desde este encargo. Si la evidencia favorece aceptar el resultado y trabajar en otro parámetro, decirlo expresamente: el objetivo no es conseguir un ganador a toda costa.

## Perímetro y aceptación

Un script de análisis derivado, sus salidas nuevas en una ruta sucesora y nota/figura; NC-0152 sólo para enlazar el siguiente paso; administración común. Lectura de motor, corpus documental versionado, capturas y resultados; cero microdatos, cambios a extractor, snapshots, medidores sellados o adopciones.

Aceptación: agregado reconciliado, errores localizados sin confundir familia con réplica, hasta tres mejoras concretas, dos abstenciones explicadas con evidencia y propuesta prospectiva acotada. Puede ejecutarse ahora en Cloud y en paralelo con todos los trabajos de CAJA. No depende de la publicación global para analizar las salidas selladas.

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

- `NC-0152` permanece ABIERTA: el diseño de 32 posiciones está propuesto,
  pero no se adquirieron las dos fuentes dirigidas ni se hicieron capturas.
- La comparación CIV no queda reparada retrospectivamente: exige estimandos
  M/R alineados por unidad, recorte, códigos y ola.
- `ADR-462` es candidato en colisión con otra rama; quien fusione segundo
  deberá renumerar contra `main`.
- No se abrió F6, no se modificó M y no se alteró `TRIADA-0002`.

## CONSUMIDO

Ejecutado en PR #698 por la rama `acto/gen2-f5-aprendizajes-sucesor`.
Producto sustantivo: `forense/notas/2026-09-10-GEN2-F5-APRENDIZAJES-Y-SUCESOR-diagnostico.md`
y `forense/prereg-duelo-v2/F5-aprendizajes-sucesor-v1_0/`. Conserva
`TRIADA-0002` como `SIN-GANADOR-UNICO`, mantiene NC-0152 abierta y no abre F6.
El merge pertenece a mesa.
