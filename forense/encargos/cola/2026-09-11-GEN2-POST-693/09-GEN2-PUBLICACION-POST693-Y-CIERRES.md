ESTADO: CONSUMIDO — PR #696; la copia canónica de ejecución está archivada en `forense/encargos/2026-09-10-GEN2-PUBLICACION-POST693-Y-CIERRES.md`.

BITÁCORA: PR #694 encoló esta copia después del arranque y del commit 0-bis del acto. PR #696 publicó las vistas, cerró las obligaciones acreditadas y dejó los residuales expresos. Se conserva el cuerpo recibido verbatim debajo de esta cabecera; no lanzar una segunda ejecución. El ejecutor no fusionó el PR.

---

# ENCARGO · GEN2-PUBLICACION-POST693-Y-CIERRES

ENTORNO: CAJA
COMPUERTA: PR #690 y PR #693 fusionados; comprobar por producto y ascendencia.
RAMA: acto/gen2-publicacion-post693
MODELOS: cero llamadas nuevas.

## Resultado útil

Publicar los cálculos ya terminados y la procedencia de replay sin borrar evidencia histórica. Cerrar NC-0104 y NC-0154 únicamente cuando las tres vistas efectivas estén publicadas. Conciliar dos firmas cuya ejecución ya está probada, sin repetir S6/S12.

## Premisas verificadas al corte

- #690 implementó `fuente_replay` y cerró NC-0141/0148; no publicó las vistas.
- El seco actual da **64 cambios de campos en 32 corridas**: dos C0D pasarían de NO-REPRODUCE/DISTINTO a REPRODUCE/IDENTICO por un asiento heredado contradictorio; 22 pasarían de REPRODUCE/IDENTICO a NO-VERIFICADO; ocho de REPLICA-RESULTADO/DISTINTO a NO-VERIFICADO por falta de asiento.
- Vistas publicadas: 147 filas de corridas, 3,209 de resultados, 205 de usos. Derivación actual: 150, 3,335 y 207. Son filas de vistas, no conteos de mediciones científicas. Faltan `CALC-0001-v2`, `CALC-ENIF-0002` y `CALC-TRIADA-0002`; las ocho olas nuevas ENVIPE ya aparecen. Las tres vistas carecen de la columna fuente.
- FP-361 y FP-363 siguen diciendo ejecución pendiente, aunque #688 cerró NC-0065/0064 y entregó S6 v1.4/S12 v1.2 y CALC-0001-v2.

Leer `tools/corrida0.py`, `forense/replay-evidencia.tsv`, las vistas, `forense/notas/2026-09-10-GEN2-PRUEBAS-LIMPIAS-Y-REPLAY-cierre.md`, los cierres de F5, ENIF y SOCIALES-SUCESORAS, y los asientos posteriores pertinentes. No repetir la investigación general de replay ni reabrir #682/#683.

## Fase 1 · Resolver sólo las transiciones que bloquean

1. Ejecutar `registro` en seco mediante la interfaz existente; recalcular IDs y transiciones actuales. Los 32 son evidencia del corte, no una constante de implementación.
2. Para cada transición, comprobar la identidad exacta y localizar el comprobante o asiento publicado que la sostiene. La identidad incompleta nunca es comodín. Distinguir una limitación del entorno actual de un cambio real del objeto.
3. Reutilizar comprobantes estructurados existentes. Cuando sólo exista evidencia histórica publicada con identidad acreditada, registrarla mediante el mecanismo ya existente como **HEREDADO-DEL-REGISTRO-PUBLICADO**, citando commit, archivo/fila, identidad, fecha conocida y alcance. No llamarla verify nuevo ni validación independiente; no completar fechas desconocidas con la fecha actual. Preservar evidencia negativa.
4. En los dos C0D, resolver la contradicción por evidencia temporal y de identidad: #683 ya trató la transición histórica; no importar el éxito viejo por encima de un negativo posterior. Si requiere reproducción, usar sus entradas congeladas y el procedimiento existente, sin tocar el marcador histórico.
5. Ejecutar `verify` con corpus sólo donde la evidencia siga faltando o haya una contradicción material. Guardar salida real y los campos de contexto; nunca forzar IDENTICO para publicar. Si el código de proyección contiene un defecto demostrado, corregirlo con fixture mínimo que lo reproduzca, preservando históricos.

Este encargo autoriza regularizar las transiciones individualmente justificadas, no autoriza degradar todas las filas ni pasar todos los IDs a `--lote` para saltarse el guard. Si una identidad no puede acreditarse, aislar su limitación por el mecanismo vigente; no inventar un comprobante. Usar la ruta más corta que conserve evidencia y permita publicar.

## Fase 2 · Publicar y comprobar estabilidad

Con demanda y asientos actualizados, derivar nuevamente. Comparar sólo las transiciones autorizadas, declarar el lote explícito y escribir las tres vistas mediante `registro --escribe`. No `--force`, no parche manual de las vistas. Deben aparecer los tres CALC omitidos y sus resultados/usos correspondientes, con fuente propia por corrida/resultado/uso.

Repetir una derivación **sin verify ni nuevas escrituras**: debe ser estable, sin borrar evidencias por falta de corpus. Contrastar antes/después de los dos ejes de replay y de los números sellados. La publicación no modifica valores, snapshots, adopciones ni SELLOS. No fijar los conteos del corte en un test.

## Fase 3 · Cerrar las obligaciones acreditadas

Actualizar `ejecutada_en` y enlaces de FP-361/363 con #688 y los artefactos exactos; preservar sus firmas. Conciliar sólo las cabeceras/bitácoras/CONSUMIDO de los siete lotes ya fusionados cuando sigan ofreciendo ejecutar el mismo objeto; no editar sus cuerpos verbatim, y conservar residuales NC-0152/0153/0155/0151. El lote 07 permanece pendiente.

Cerrar NC-0104 y NC-0154 por publicación efectiva. Una nota que enumere 32 corridas no sustituye este resultado. Si queda un residual real, describir su efecto y la siguiente acción, sin reabrir NC-0140/0145.

## Perímetro y aceptación

Toca `tools/corrida0.py` y pruebas pertinentes sólo ante defecto; `forense/replay-evidencia.tsv`; `data/corrida0/{corridas,resultados,usos}.tsv` y demanda si cambió; filas FP/NC y cierres citados; cabeceras de cola del paquete POST685; administración común. No adopciones nuevas ni suite general de limpieza.

Aceptación: tres vistas con fuente; tres CALC faltantes visibles; ninguna evidencia negativa escondida; diff seco posterior estable; números sellados intactos; FP-361/363 dejan de pedir lo ejecutado. Pruebas dirigidas `test_corrida0.py`, `test_cierre_acto.py`, y baseline sobre el PR integrado. La revisión de preparación ya obtuvo 84/84 y 8/8: no presentar esas ejecuciones como prueba del cambio futuro.

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
