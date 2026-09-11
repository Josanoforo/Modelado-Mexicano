# ENCARGO · GEN2-ENVIPE-VALIDACION-Y-LECTURA

ENTORNO: CAJA
COMPUERTA: PR #692 fusionado y los ocho CALC con sus insumos disponibles.
RAMA: acto/gen2-envipe-validacion-lectura
MODELOS: cero llamadas nuevas.

## Resultado útil

Validar por una implementación separada los ocho puntos nuevos de ENVIPE y entregar una lectura temporal usable de la serie 2010–2024. Resolver NC-0155, que pide independencia y no otro replay del mismo código. No adoptar la serie al motor ni presentarla como tasa general de denuncia.

## Entradas y alcance

Leer `forense/prereg-caja/ENVIPE-SERIE-COMPLETA-spec-v1_0.md`, `data/corrida0/envipe-serie-denuncia-v1_0.tsv`, los specs/resultados/recibos de `CALC-ENVIPE-SERIE-{2011,2014,2016,2017,2018,2019,2020,2022}`, el cierre de #692 y los cuestionarios/diseños oficiales ya registrados. Siete puntos previos se reutilizan; no volver a encargar las ocho olas ni descargar archivos que el corpus ya tiene.

Objeto exacto: `p(C1,U1)`, proporción ponderada por FAC_DEL de motivos 01/02/06 entre **delitos personales no denunciados con respuesta 01..08**. Es unidad delito y composición de motivos. No es la probabilidad poblacional de denunciar, ni el complemento de RES-0028 que usa otro recorte/unidad.

## Fase 1 · Segunda implementación

Congelar una receta de comprobación antes de generar sus salidas: por ola, miembro ZIP, variables, códigos de delito personal, respuesta válida, ponderador, estrato y UPM. Usar el cuestionario y spec como autoridad semántica. No importar la función decisiva de `tools/medidor_envipe_serie_completa.py`, ni copiar su algoritmo como supuesta implementación independiente.

Tabular separadamente numerador ponderado, denominador ponderado, n incluido, excluidos por código y punto. Aplicar a las ocho olas un único script pequeño con mapa explícito DBF/CSV. Fijar tolerancia numérica con justificación antes del contraste; no ajustarla para que todo pase. Registrar que los valores originales ya son conocidos: esta es validación técnica independiente, no arbitraje ciego.

Comprobar la rama 2011 (`BP1_21`, 04..14, residuos 88/98/99, EST/UPM), la otra DBF y la rama CSV contra documentación. Si surge diferencia material, rastrearla por universo/peso/código y conservar el resultado original; producir correctivo o sucesora sólo del objeto afectado. No expandir hacia toda la historia.

## Fase 2 · Alcance de la incertidumbre

NC-0155 exige ocho puntos: repetir el bootstrap original no añade independencia. Validar la implementación de incertidumbre en un caso representativo por receta material distinta, mediante un método de referencia compatible con el diseño, si los insumos lo permiten. Separar punto validado, implementación del IC comprobada y comparación metodológica. No exigir igualdad exacta entre IC bootstrap y Taylor, ni acreditar los 40 RESULT de cada CALC a partir de validar un punto.

Si el diseño o una diferencia de IC puede cambiar la lectura, acotar esa comparación. La incertidumbre de diferencias entre años necesita su propia hipótesis de covarianza: no tratar el solapamiento de dos IC como prueba formal ni asumir independencia entre olas sin justificarla.

## Fase 3 · Producto descriptivo

Entregar TSV con trazabilidad y una figura exportable SVG/PNG/PDF usando herramientas de gráficos exactos: año del hecho 2010–2024, punto e IC por ola, ruptura de 2011 marcada y etiqueta completa del estimando. Mantener el archivo canónico existente como fuente; no crear otra serie divergente.

Añadir lectura breve: magnitud en puntos porcentuales, tramos de cambio, límites de comparabilidad, composición de motivos y posibles explicaciones como hipótesis. El máximo puntual 2013 y el cambio 2018→2019 son hallazgos exploratorios ya vistos; no presentarlos como contrastes pre-registrados. No atribuir causalidad ni proclamar una tendencia poblacional de corrupción/denuncia a partir de este recorte.

## Fase 4 · Evidencia y cierre

Registrar la validación independiente mediante el mecanismo vigente, con implementación y resultados comparados, sin editar specs selladas para cambiar `NO-HECHA` retrospectivamente. Cerrar NC-0155 con el alcance exacto satisfecho o conservar únicamente su diferencia material. Este control no crea ocho mediciones científicas adicionales.

Entregar comprobantes al encargo `GEN2-PUBLICACION-POST693-Y-CIERRES` si sigue abierto. Si ya fusionó, usar el registro existente con lote propio y sin pisar evidencia ajena. La lectura descriptiva local no depende de la firma de RES-0028, FP-371 ni F6.

## Perímetro y aceptación

Un validador independiente y una prueba sólo si protege una diferencia real; evidencias/nota/figura de ENVIPE y registro de validación aplicable; NC-0155; administración común. Los CALC originales y el motor son de lectura.

Aceptación: ocho puntos contrastados con numeradores/denominadores reconstruidos; discrepancias resueltas o acotadas; IC descritos con su alcance; producto temporal legible y reproducible; ninguna tasa de denuncia inventada ni cambio de adopción. Puede correr en paralelo con publicación y cron: no comparte microdatos en escritura ni modifica sus herramientas.

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
