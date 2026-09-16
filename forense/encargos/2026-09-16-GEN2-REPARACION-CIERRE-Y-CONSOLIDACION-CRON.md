# GEN2 · Reparar el cierre y consolidar las adquisiciones del cron

Fecha: 16 de septiembre de 2026.  
Repositorio: Josanoforo/Modelado-Mexicano.  
Ejecutor: Codex CLI en CAJA, con Windows/WSL, clon operativo y logs locales. No requiere Opus.  
Resultado: un PR consolidado, revisable y fusionable, con el contrato reparado y evidencia de recuperación de las adquisiciones existentes. Sin nuevas llamadas al modelo ni nuevas descargas.

## 1. Objetivo y punto de partida

Resolver el fallo que declara `resultado_invalido` y `exit=65` después de adquisiciones efectivas. Recuperar el trabajo único de #805 y #808, absorber la evidencia pertinente de #807 y comprobar el correctivo en CAJA. No rehacer scheduler, investigación ni descargas.

Antecedentes de la revisión anterior, que deben actualizarse al comenzar:

- `main` estaba en `05977efa`, después de #809; #805/#807/#808 seguían pendientes.
- #804 había corregido la rama ocupada por otro worktree y la regeneración desde un árbol antiguo.
- #805 documenta el metadato JSON IHSN de ENNViH-3, aproximadamente 10.24 MB, con ID de adquisición `IHSN_MEX_2009_ENNVIH3_METADATA`.
- #808 documenta ENPOL 2016, 16,801,537 bytes, con ID de adquisición `ENPOL_2016_MICRODATOS_CSV`.
- El validador rechazaba ambos porque `usado_para` describía la necesidad/consumidor sin repetir el ID literal de adquisición. La vinculación estructurada existe mediante `ids_manifiesto` en la fila canónica de la cola.
- #807/#808 presentaban un problema de CI relacionado con T16 y afirmaciones de conteos FAIL/WARN. Comparar con el baseline vigente; no adoptar cifras antiguas como objetivo.

Estos antecedentes no sustituyen la consulta inicial de GitHub. Leer `AGENTS.md`, actualizar referencias y comprobar `origin/main`, PR sucesores y evidencia posterior. Si parte del trabajo ya está integrada, conservarla y ejecutar sólo lo faltante. Los ZIP de agosto no son necesarios ni autoridad para este encargo.

## 2. Alcance y preservación

Trabajar en rama/worktree propio desde `origin/main` vigente. Antes de consolidar, conservar las referencias y SHA de los tres PR y localizar los JSON finales, selección, logs y artefactos correspondientes a cada corrida en `forense/adq-log/` o su ruta efectiva en CAJA.

Preservar corpus, archivos descargados, configuración local, ledger, consumo real, reservas, cursores, fechas de continuación, locks y trabajo ajeno. No usar `reset --hard`, `clean`, eliminación de locks ni sobrescritura indiscriminada de archivos compartidos. Si hay una ejecución activa, no modificar su árbol ni lanzar otra competidora.

No cambiar horarios, modelos, cupos, privilegios, parámetros científicos, adopciones, intervalos o F6. No contactar terceros. No fusionar PR: los merges quedan con Jonás. La recuperación no autoriza contar de nuevo investigaciones, objetos o bytes ni devolver presupuesto ya consumido.

## 3. Reparar el contrato, con una regresión dirigida

Inspeccionar `tools/adq_doctor.py::valida_resultado_adquisicion`, `tools/adq-resultado.schema.json`, el recorrido de cierre de `tools/adquiere_cron.sh` y las pruebas existentes, en particular `tests/test_adq_cierre_verificable.py`. Confirmar el fallo con los casos reales antes de editar.

Aplicar la modificación mínima: para cada objeto de adquisición y cada ID de manifiesto informado, acreditar pertinencia mediante la relación estructurada de la fila canónica exacta de ese objeto con ese ID en `ids_manifiesto`. Conservar la coincidencia literal vigente en `usado_para` como alternativa compatible, sin convertirla en requisito adicional.

La relación debe leerse de la cola canónica del árbol evaluado. No basta que el propio JSON del ejecutor afirme el vínculo, que otra fila lo contenga o que aparezca como subcadena de un ID diferente. Mantener las verificaciones restantes de esquema, selección, existencia, identidad, archivos, hashes y publicación que correspondan. No aceptar manifiestos inexistentes ni vínculos inventados para volver verde el recibo.

Actualizar sólo la guía operativa pertinente para explicar que `usado_para` describe el uso y la vinculación objeto–manifiesto debe quedar explícita en el registro estructurado. No añadir otra capa de índices o protocolos.

Extender la prueba existente con:

- IHSN y ENPOL: la relación canónica exacta permite validar aunque el texto humano no contenga el ID de adquisición.
- Caso negativo: ID de manifiesto presente únicamente en otro objeto, o sin relación válida, sigue rechazado.
- Compatibilidad de la alternativa literal y rechazo de archivo/hash incorrecto, aprovechando las pruebas ya existentes.

Usar fixtures mínimos derivados de los casos observados; no copiar corpus a tests. Si la revalidación descubre otro defecto del mismo contrato, corregirlo dentro de este acto cuando sea necesario para recuperar estos cierres. No iniciar una auditoría general.

## 4. Consolidar el trabajo útil y revalidar los cierres reales

Integrar selectivamente en la rama nueva el trabajo único de #805 y #808. No resolver conflictos tomando un archivo entero por antigüedad o número de PR. Preservar ambos objetos, sus manifiestos, hashes, recibos, relaciones con necesidades y referencias de adquisición. Reutilizar de #807 sólo evidencia que no esté ya preservada o superada en `main`.

En los registros compartidos, especialmente NC-0202, conservar la última frontera y el último cursor respaldados por evidencia, sin perder el avance previo. No reabrir necesidades resueltas ni cerrar una por disponer únicamente de documentación.

Revalidar cada JSON final ORIGINAL contra su selección original y el árbol de evidencia correspondiente, con los bytes locales ya adquiridos. Registrar por corrida: run_id, SHA/contexto original, hash del JSON, comando ejecutado, resultado anterior, errores originales y resultado de la revalidación. Guardar únicamente la evidencia necesaria en el canal existente.

No editar los JSON o recibos históricos para simular que originalmente fueron válidos. Si falta un JSON, buscarlo en los logs o salida final conservada de esa corrida; si debe reconstruirse, etiquetarlo como reconstrucción y distinguirlo de una revalidación del original. Si faltan bytes locales, señalar qué verificación queda pendiente: un manifiesto por sí solo no prueba que el archivo siga disponible. No descargarlo otra vez en este encargo.

Conservar los `exit=65` históricos. Añadir una nota breve de recuperación que enlace cada corrida con su validación posterior, sin sustituir sus métricas originales. Si el ledger quedó indeterminado, corregir sólo lo que permitan demostrar los registros, mediante el mecanismo de reconciliación existente; no reservar ni consumir otra vez y no inventar saldo cuando el consumo no sea recuperable.

Separar claramente:

- Adquirido: objetos y bytes respaldados por las corridas originales; cero adquisiciones nuevas por este encargo.
- Legible/registrado: comprobación local y registro canónico.
- Apto para uso: IHSN ENNViH-3 aporta identidad/inventario documental; no habilita por sí mismo los intervalos de CORR-0008. ENPOL conserva las condiciones de uso vigentes. NC-0202 no se cierra por esta reparación textual.

## 5. Demanda, CI y comprobación en CAJA

Regenerar la demanda con el escritor canónico después de consolidar los registros y sincronizar con `main` vigente. Comprobar sus SHA contra los insumos del mismo corte. Si hay un merge concurrente material antes de entregar, incorporar su efecto y regenerar una vez. No exigir igualdad perpetua con futuros commits.

Ejecutar las pruebas dirigidas del contrato y las de runner/demanda afectadas; luego el gate de integración requerido. Comparar los fallos con `main`. Para T16, actualizar sólo las afirmaciones vigentes que hayan quedado falsas usando la salida real y el mecanismo existente. No desactivar el check, rebajar expectativas, maquillar conteos ni corregir incidentalmente miles de WARN heredados. El PR debe quedar con el CI requerido aprobado; si existe un bloqueo externo, precisarlo sin afirmar que está listo para fusionar.

Publicar el PR consolidado y comprobar el despliegue de su SHA remoto exacto mediante el mecanismo existente en CAJA. Distinguir versión desplegada de versión integrada: un PR publicado todavía no es `main`. Conservar la revisión previa para reversión. Si el launcher permite fijar la revisión autorizada del PR, verificar que el proceso efectivo utiliza esa revisión; no basta el HEAD de la sesión de desarrollo. Tras el merge, el despliegue debe volver a seguir `main` según el mecanismo existente.

Comprobar el recorrido de cierre/publicación con los resultados ya guardados, SIN invocar otra vez al modelo ni volver a adquirir. Usar un modo de reproducción existente si lo hay. Si no existe, hacer la comprobación dirigida con las mismas funciones de producción sobre un estado aislado, sin tocar el ledger operativo, y comprobar por separado que CAJA carga la revisión corregida. No añadir un sistema de replay general para esta tarea.

No disparar la tarea productiva a ciegas: puede encontrar trabajo elegible y consumir nuevas llamadas. Una prueba con fixtures acredita regresión; la revalidación acredita recuperación histórica; un recorrido aislado acredita ese recorrido; ninguna de ellas por separado prueba una nueva adquisición desatendida. Si el mecanismo existente no permite acreditar el cierre completo sin nueva investigación, entregar esa limitación concreta y el paso mínimo pendiente, sin inventar éxito ni dejar sin reparar y consolidar lo que sí puede completarse.

El fin es corregir y recuperar ahora. No sustituir el trabajo por «esperar al siguiente ciclo».

## 6. Sustitución de PR y entrega

Mantener un solo PR consolidado para este acto. Su descripción debe explicar el defecto, el cambio, los objetos preservados, las corridas recuperadas, las pruebas y el estado de despliegue. Archivar este encargo conforme al protocolo existente.

Sólo después de que el PR sustituto contenga todo el trabajo único, tenga CI aprobado y enlaces verificables, cerrar como sustituidos los PR pendientes #805/#807/#808 que realmente hayan quedado absorbidos. Añadir un comentario breve con el enlace sucesor y la cobertura de cada uno. No cerrar un PR que aún contenga trabajo ausente; no borrar ramas ni evidencia histórica. Si alguno ya está integrado o sustituido, no intervenirlo innecesariamente.

Entregar a mesa:

1. PR único, SHA, estado de CI y relación de PR absorbidos o aún pendientes con causa.
2. Regla corregida y regresión positiva/negativa.
3. Tabla por corrida: resultado histórico, revalidación del original o reconstrucción, investigaciones/objetos/bytes acreditados y reserva restante.
4. Confirmación de preservación de IHSN, ENPOL, frontera de NC-0202, presupuesto y cursores; cualquier ajuste contable debe quedar explicado.
5. Demanda coherente con su corte; SHA desplegado y evidencia efectiva de CAJA.
6. Dictamen separado sobre contrato, recuperación histórica, despliegue, publicación e integración. No usar «cron completamente cerrado» si una de esas afirmaciones depende de una comprobación aún no realizada.

Parar cuando el contrato esté reparado, el trabajo recuperable esté consolidado, la validación dirigida esté terminada y el PR esté listo para decisión de fusión, con el despliegue acreditado o una limitación concreta y acotada. No ampliar el encargo a nuevas adquisiciones, nuevas mediciones ni auditoría general. Explicar el avance práctico: el servicio puede reconocer y conservar el trabajo que ya produjo sin repetir su costo.

## Prompt de lanzamiento

> Ejecuta íntegramente ENCARGO-GEN2-REPARACION-CIERRE-Y-CONSOLIDACION-CRON.md en CAJA con Windows/WSL y acceso al clon operativo y logs. Actualiza primero contra origin/main y aprovecha cualquier correctivo ya integrado. Autorizo la reparación mínima del contrato, las regresiones dirigidas, la recuperación y consolidación del trabajo único de #805/#807/#808, la regeneración de demanda, commits, push y apertura o actualización de un PR consolidado. Autorizo desplegar su SHA remoto exacto mediante el mecanismo existente y comprobarlo sin nuevas llamadas al modelo ni descargas. Autorizo comentar y cerrar como sustituidos esos PR sólo cuando el sucesor preserve todo su trabajo único y tenga CI aprobado. Los merges quedan conmigo. Conserva los exit=65 y JSON originales; registra la recuperación sin reescribir la historia ni duplicar consumo, objetos o bytes. Preserva corpus, ledger, reservas, cursores, fechas y cambios ajenos. No cambies horarios, cupos, modelos, privilegios ni criterios científicos. Resuelve el fallo y consolida ahora; no entregues únicamente un diagnóstico ni una recomendación de esperar otro ciclo. Distingue pruebas, revalidación histórica, despliegue efectivo e integración pendiente.
