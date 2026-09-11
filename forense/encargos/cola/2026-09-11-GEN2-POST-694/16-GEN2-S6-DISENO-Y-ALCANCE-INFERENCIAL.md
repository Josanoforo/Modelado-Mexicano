# ENCARGO · GEN2-S6-DISENO-Y-ALCANCE-INFERENCIAL

ENTORNO: NUBE
COMPUERTA: PR #688 y #693 fusionados; entradas agregadas de CALC-0003-v4 disponibles.
RAMA: acto/gen2-s6-diseno-alcance
MODELOS: cero llamadas nuevas. Si una fase precisa microdatos, continuar en CAJA.

## Resultado útil y prioridad

Resolver una contradicción material entre el diseño que S6 dice acreditar y la evidencia oficial revisada en #693. Determinar qué afirmaciones dependen de esa premisa, corregir el alcance documental no sustentado y entregar la opción de uso inferencial que mesa debe decidir. **No volver a correr S6 por rutina ni reabrir la corrección del join de #688.**

## Evidencia nueva que justifica este encargo

1. `forense/prereg-caja/S6-L16-spec-v1_3.md` §3.5 usa `id_loc` como conglomerado y `c_portad.estrato` como estrato; levanta una reserva de varianza por considerar que ya tiene el conglomerado correcto. El mismo texto también llama a localidad una aproximación. S6 v1.4 documentó el join por hogar, sin resolver esta equivalencia estadística.
2. `CALC-0003-v4` publicó 150 valores de id_loc, cuatro estratos y correspondencia con geografía; su primaria C1/B3B da NO-DISCRIMINA y las secundarias C3/C4 dan CORROBORADA bajo esa receta. El resultado del join no acredita por sí mismo el diseño de muestreo.
3. #693 documenta, para la misma ENNViH-1, que la UPM oficial no es pública y que localidad y estrato de tamaño no sustituyen sin justificación a UPM/estrato de selección.
4. Verificación externa al preparar: la [FAQ oficial](https://ennvih-mxfls.org/faq.html) describe `estrato` mediante cuatro tamaños de localidad y declara que las UPM no se publican. El [diseño muestral ENNViH-1](https://www.ennvih-mxfls.org/assets/ennvih-1_muestra.pdf), §4.1.2 y cuadro 1, describe estratos alto/medio/bajo y 180 UPM seleccionadas. Estos hechos cuestionan la equivalencia asumida; la diferencia 150/180 por sí sola no calcula el sesgo del IC.

**Inferencia a comprobar:** no está acreditado que el bootstrap por localidad dentro de cuatro categorías reproduzca la varianza del diseño real. No se conoce por ello la dirección ni magnitud del error. No se afirma que los puntos estén mal, que toda significación desaparezca o que S6 carezca de valor descriptivo.

## Fase 1 · Contraste focalizado

Leer S6 v1.3 §3.5/v1.4, `data/corrida0/CALC-0003-v4/{spec.md,spec.yaml,resultados.json}`, el dictamen DIN de #693, `data/diseno-muestral.yaml` y las dos fuentes oficiales ya registradas. Verificar versión/ola y localizar una justificación explícita de id_loc/estrato como unidades equivalentes de selección o como aproximación admitida.

No abrir una búsqueda general de encuestas. Revisar la documentación oficial disponible y una vía directa adicional del productor si aporta un dato concreto. Si no hay diseño público ejecutable, declararlo; no tratar falta de respuesta como inexistencia mundial ni suplir la UPM inventando geografía. Reutilizar la solicitud oficial preparada en #693, sin enviarla ni abrir otro expediente duplicado.

## Fase 2 · Alcance afectado, desde salidas existentes

Seguir exclusivamente los RESULT de C1/C3/C4 y sus consumidores/tiers actuales. Informar: punto observado, IC calculado, supuesto de diseño, conclusión bajo ese supuesto y conclusión que puede mantenerse sin acreditarlo. Mostrar que R4.4 no se promovió por este CALC si eso sigue vigente; evitar atribuir al defecto un cambio de tier que nunca ocurrió.

La primera salida debe ser una tabla de impacto que permita usar la medición con su reserva. No recalcular los 143 RESULT ni las otras encuestas. Comparaciones ya existentes v2/v3/v4 sirven como sensibilidades, no como pruebas de cuál es el IC verdadero. No inferir que el intervalo más ancho es automáticamente correcto o conservador.

## Fase 3 · Corrección técnica y propuesta de decisión

Si la equivalencia no se acredita, preparar una enmienda fechada de alcance y referencias activas que deje de afirmar diseño oficial/garantía de varianza. Preservar bytes de specs, medidores, resultados y sellos históricos; nunca reescribir el veredicto emitido bajo el contrato original. Explicar la diferencia entre veredicto histórico condicionado y evidencia inferencial actual para consumidores.

Propuesta recomendada a mesa: conservar puntos y asociaciones descriptivas; mantener IC por localidad como sensibilidad explícita mientras no exista vía oficial; no promover nuevas conclusiones basadas exclusivamente en dichos IC. Alternativa: esperar EE/IC oficiales para cualquier uso inferencial. Una aprobación del diseño de DIN (FP-371) no se inventa ni se extiende automáticamente a S6: presentar el objeto de cada decisión.

No crear un nuevo diseño muestral por conveniencia ni un v5 calculado con otra aproximación para conseguir el mismo veredicto. Sólo si aparece una vía oficial ejecutable, preparar spec sucesora y continuación CAJA antes del primer resultado. El diseño nuevo y sus consecuencias se entregan para la decisión pertinente, con los puntos históricos intactos.

## Fase 4 · Protección del trabajo en curso y cierre

El encargo 12 de tandas ya prohíbe heredar un diseño no acreditado: sus puntos descriptivos pueden continuar. Entregar un aviso preciso para su ejecutor y para el análisis 13 de F5. El punto DIN tampoco se retira por discutir su IC.

Actualizar únicamente la reserva de diseño y sus referencias directas; no volver a pedir D13, FP-361 ni la antigua decisión FP-332 sobre la rama fallida. Si hace falta una nueva fila de decisión, el objeto es el uso inferencial de S6 ante esta evidencia nueva, con candidato derivado al cierre. No declararla firmada por escribir la recomendación. La investigación/corrección de alcance queda completa aunque falte la elección final de mesa.

## Perímetro y aceptación

Nota de contraste/tabla de impacto, evidencia oficial reutilizada, enmienda sucesora de alcance en ruta nueva, referencia de diseño pertinente y administración común. Lectura de CALC/motor. No escribir `milpa/tramite-ola5-propuesta-v0.yaml`, medidores, snapshots, índices de reactivos ni vistas globales mientras corren los otros actos; entregar las enmiendas de consumo propuestas para su integración delimitada.

Aceptación: equivalencia de diseño acreditada o reserva explícita fundada; impacto en C1/C3/C4 trazado sin inventar un cambio de signo/tier; puntos preservados; decisión concreta y continuación al productor si se necesita. Es una revisión focalizada que puede alterar la confianza en un resultado; no una auditoría general. El análisis documental puede empezar ya en Cloud en paralelo con todos los encargos activos.

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
