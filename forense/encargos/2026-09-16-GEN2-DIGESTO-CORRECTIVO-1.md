<!-- PROCEDENCIA: recibido de mesa el 2026-09-16 desde /mnt/c/Users/PC0/Descargas MX/ENCARGO-GEN2-DIGESTO-CORRECTIVO-1.md. -->
<!-- CONSUMO: ejecutado en acto/gen2-digesto-correctivo-1; evidencia y cierre en forense/notas/2026-09-16-GEN2-DIGESTO-CORRECTIVO-1-cierre.md. -->

# ENCARGO · GEN2-DIGESTO-CORRECTIVO-1

Fecha de emisión: 16 de septiembre de 2026.  
Repositorio: `Josanoforo/Modelado-Mexicano`.  
Ejecutor preferido: Codex CLI, worktree propio; Claude Cloud es alternativa válida para este mismo encargo porque no requiere corpus. No correr dos ejecutores simultáneos sobre él.  
Producto: un correctivo pequeño del generador de digesto, reproducido y probado, listo para integrar sin interferir con CAREO/TRÁMITE-4.  
Base consultada: `origin/main @ 9dffd6455c67e2ca99740e79f90be59a13f250e1`. Es referencia de preparación, no un pin de ejecución; actualizar al comenzar.

## 0. Resultado encargado y límites de autoridad

Restablecer la capacidad de generar un digesto íntegro sin marcadores que el propio verificador rechaza. No rehacer el cron ni auditar el programa: corregir el defecto concreto, si sigue vigente, con evidencia antes/después y regresión mínima.

El PR #816 registró que `tools/digesto_tramite.py --fecha 2026-09-16` terminó dos veces con código 2: «T22(b): marcador de pendiente-de-mesa sobrevivió a la neutralización». En el corte consultado no existe `forense/digesto/DIGESTO-2026-09-16.md`. Es una pista reproducible, no prueba suficiente de la causa actual ni permiso para arreglar todos los FAIL del programa.

Las reparaciones de adquisición/derivados y su ciclo automático ya fueron acreditadas. No las reabras. Un rc=0 local tampoco demuestra que se haya publicado un digesto o que su rutina automática haya entregado.

Al lanzar este encargo se autorizan edición en perímetro, pruebas locales sin datos/modelos, commits, push sin force y un PR. No se autorizan merges, despliegues, activaciones del scheduler, modificaciones a rutinas o llamadas a modelos experimentales. La fusión queda con Jonás.

## 1. Arranque y separación del trabajo paralelo

1. Lee `AGENTS.md`, este encargo completo y las instrucciones pertinentes del generador. Reporta ruta absoluta, rama, HEAD y `git status --short`; fetch de `origin/main` y comprobación de duplicado en ramas, PR y worktrees.
2. Usa el clon existente con worktree aislado; rama sugerida `acto/gen2-digesto-correctivo-1`. No cambies la rama del cron, de Opus o de F6. No uses stash/descarte de trabajo ajeno, `reset --hard`, force-push ni borrado de ramas/worktrees.
3. No necesitas `data/raw`, raíces de Windows ni permisos del scheduler. No montes corpus ni reproduzcas el entorno de medición para esta tarea. Instala sólo dependencias declaradas en un entorno local aislado si faltan; no edites requisitos sin una necesidad del correctivo.
4. Archiva el encargo verbatim en `forense/encargos/2026-09-16-GEN2-DIGESTO-CORRECTIVO-1.md`; procedencia y consumo fuera de su bloque. Publica pronto la rama para evitar otra ejecución del mismo rótulo.

### Excepción específica de cascada y publicación

Este acto puede correr junto a F6 y Opus. **No escribe la cascada compartida**: quedan fuera `decisiones.tsv`, `no-corrido.tsv`, `firmas-pendientes.tsv`, `hallazgos.md`, PARA, canon/gobernanza, canon/estado, registro de rótulos, tableros, `rutinas.tsv`, manifiestos, colas, contadores y baseline. No reserves ADR/NC/FP. Las reservas se comunican en la nota y el PR.

Esta excepción del encargo que mesa autoriza prevalece sobre la cascada genérica de `/acto`; no modifica permanentemente el protocolo. No ejecutes `/tramite`, `/despacha`, `/deriva` ni el cron. No crees una segunda rutina ni un nuevo registro.

**No publiques el digesto canónico del día durante este acto.** CAREO y TRÁMITE-4 están cambiando sus insumos. Toda salida de prueba va a stdout o a un directorio temporal externo al repositorio, identificado por su SHA efectivo y sin atribuirlo a una ejecución automática. La publicación definitiva ocurrirá sobre un corte posterior integrado; la prueba de capacidad puede hacerse ahora.

No abras o calcules el cruce reservado ENIF 2024 `localidad × edad`, capturas del piloto de Opus o microdatos de F6. Leer registros administrativos no concede permiso para ejecutar las derivaciones que nombran.

## 2. P1 · Reproducción mínima en el árbol vigente

Lee `tools/digesto_tramite.py`, las pruebas `tests/test_digesto_{candidatas,fecha,mesa,nc}.py` y las constantes T22/T25 pertinentes de `tests/check.py`, sólo en lectura. Lee el recibo de #816 en `forense/rutinas.tsv` y, si es necesario, el PR. No busques durante horas la historia del cron.

Comienza por una ejecución de diagnóstico de solo lectura:

```bash
python3 tools/digesto_tramite.py --fecha 2026-09-16 --stdout --sin-suite
```

Captura el código de salida real y stderr, sin perderlos en un pipeline. `--sin-suite` acelera el aislamiento del renderizado; **no acredita** que el recorrido completo con la suite funcione. Guarda el stdout potencial en temporal, no en `forense/digesto/`.

Si falla como el recibo:

- Localiza el fragmento exacto que satisface el patrón, su sección y archivo/campo origen. Distingue un texto fuente copiado, un literal de la plantilla y un marcador que aparece al unir columnas/líneas. No cambies por reflejo el regex global.
- Comprueba que neutralizador y verificador coinciden en la semántica necesaria para el caso real. Identifica si la neutralización se omitió, se aplicó antes de ensamblar el texto o se perdió posteriormente.
- Reduce el caso a un fixture pequeño estable que reproduzca el fallo, sin copiar toda la gobernanza o miles de filas.

Si no falla, ejecuta también el recorrido completo con `--stdout` y verificación activa. Revisa si una corrección ya integrada lo explica. Puedes reproducir el incidente en un worktree temporal del SHA histórico pertinente si es accesible y barato; no cambies el árbol principal. Si el defecto ya está resuelto, no introduzcas otro parche: entrega `NO-REPRODUCIBLE-EN-CORTE-VIGENTE` o `YA-CORREGIDO`, diferenciando lo probado de lo no observado en automatización. Dos comprobaciones razonables bastan; no fabriques un problema para justificar el encargo.

Si aparece otro error local directo que impida generar la salida, acótalo: corrige dentro del generador sólo si es material y entra en este perímetro. Un fallo externo de GitHub, autenticación o scheduler no autoriza ampliar el acto.

## 3. P2 · Correctivo mínimo, sin ocultar información

Corrige la causa reproducida en la ruta de renderizado. Conserva las firmas, reservas, IDs, citas y el sentido de los pendientes. Neutralizar un token operativo no debe ocultar que existe una decisión pendiente o que falta una evidencia. El usuario debe seguir pudiendo llegar al texto fuente íntegro.

No se admite como solución:

- `--sin-verificar-marcadores`, vaciar el verificador o debilitar T22/T25;
- eximir todos los digestos en `tests/check.py`;
- borrar secciones, filas o citas para que dejen de disparar el control;
- cambiar `firmas-pendientes.tsv`, los textos firmados u otras fuentes administrativas para acomodar al generador;
- falsear un rc=0, neutralizar el mensaje de error o publicar un archivo truncado;
- recongelar baseline, recifrar WARN en gobernanza o reparar la auditoría global;
- reemplazar el digesto por uno manual.

Prefiere reparar el punto donde entró el texto sin neutralizar; una pasada final sobre el render completo sólo procede si conserva el contenido y se prueba su necesidad. No introduzcas un framework de sanitización o nuevos formatos.

Mantén la escritura atómica y los paros de integridad existentes. Si hay error antes de completar, no debe quedar una salida parcial reemplazando el archivo previo. El modo `--mesa --stdout` continúa siendo sólo lectura; no debe cambiar el estado de una fila al mostrarla.

## 4. P3 · Verificación que acredita el correctivo

Usa pruebas dirigidas, reutilizando las existentes. Añade una regresión del defecto real, no una batería de ceremonias. Evidencia mínima:

1. **Antes/después:** fixture del texto/ensamblado real falla con el generador anterior y pasa con el corregido. Si no hubo defecto vigente, no afirmes esta comparación.
2. **Contenido preservado:** la fila/decisión sigue visible con ID y procedencia; sólo cambia la representación que disparaba el marcador. Incluye caso de texto inocuo que no debe alterarse. Si el defecto cruzaba límites de columna/fragmento, el fixture debe ejercitar esa unión.
3. **Verificación activa:** salida final aceptada por el verificador; modo ordinario y `--mesa --stdout` siguen funcionando. Probar además texto sin truncar (`--tope-texto 0`) cuando el camino corregido participa, para no «resolver» el fallo ocultándolo tras el tope.
4. **Cero escritura de fuentes:** hashes antes/después de los registros que el generador consulta; ninguna prueba los modifica en el worktree real. Los casos que escriben usan directorios temporales.
5. **Escritura completa o ninguna:** prueba o reutiliza prueba existente de destino temporal con archivo previo y error de validación; el previo se conserva. En éxito, el archivo temporal generado contiene el digesto completo y pasa verificación.
6. **Repetición:** mismos insumos efectivos, fecha y refs capturadas producen el mismo contenido. No confundas movimiento concurrente del remoto con no determinismo del generador; usa entradas fijas en la prueba y declara cualquier diferencia externa en la ejecución real. No «estabilices» borrando procedencia.

Para integración, corre las pruebas de digesto relevantes y el baseline requerido, comparándolo con la misma base y entorno. Antes de lanzar cualquier suite, comprueba que sus casos no abren datos reservados o ejecutan mediciones. No hace falta ejecutar el motor o el corpus.

Comprueba por separado el recorrido completo del generador, con suite y verificación activa, usando `--stdout`. Si funciona y es seguro, comprueba también la ruta `--salida` hacia un archivo temporal externo; no generes el nombre canónico dentro del árbol. Para mantener fidelidad del corte de `no-corrido.tsv`, no sustituyas silenciosamente una ref inaccesible por otra: corrige el acceso a la historia necesaria o declara la limitación. Un clon shallow puede requerir traer el commit de referencia; no prueba un defecto científico.

Registra todos los códigos relevantes y diferencia: prueba dirigida, generación completa, escritura temporal, CI, publicación y automatización. Un éxito en una etapa no acredita las restantes.

## 5. Perímetro de escritura cerrado

- `tools/digesto_tramite.py`.
- `tests/test_digesto_candidatas.py`, `tests/test_digesto_fecha.py`, `tests/test_digesto_mesa.py`, `tests/test_digesto_nc.py`: sólo los archivos necesarios para la regresión del caso. Si ninguno corresponde, se permite `tests/test_digesto_neutralizacion.py`, ejecutado explícitamente sin editar el agregador compartido.
- `forense/encargos/2026-09-16-GEN2-DIGESTO-CORRECTIVO-1.md`.
- `forense/notas/2026-09-16-GEN2-DIGESTO-CORRECTIVO-1-cierre.md`: causa, evidencia, comandos y un paso de publicación posterior.

No modificar `tests/check.py`, `.github/`, launcher, scheduler, configuración de agentes, los scripts de derivados o adquisición, ni fuentes administrativas. Si un cambio a esos archivos se vuelve realmente indispensable, completa el correctivo posible y pide decisión puntual; no lo incorpores por iniciativa propia.

## 6. P4 · PR listo y entrega independiente de Opus

Un solo PR, con título `[DIGESTO] Corrige <causa comprobada>`. Archiva el encargo y devuelve el producto probado sin esperar indefinidamente a CAREO/TRÁMITE-4. Antes del push final, incorpora `origin/main` vigente y repite las pruebas afectadas; nunca sobrescribas una corrección concurrente ni elimines trabajo ajeno.

Si el fallo vigente quedó corregido: reporta PR, SHA, causa, prueba anterior/corregida, estado de CI y reservas. Si el CI bloquea sólo por la cascada excluida, dilo con el check exacto y conserva el producto; no manipules cifras o excepciones globales para pintarlo verde. Si hay un fallo material nuevo propio, corrígelo antes de recomendar fusión.

Si no hubo nada que corregir: entrega el diagnóstico breve y sus comandos/salidas; no abras un PR de código vacío. Si sólo se archiva una nota, indícala como documentación, no reparación.

El cuerpo del PR debe incluir:

| Evidencia | Estado real |
| --- | --- |
| Fallo en corte base | reproducido / no reproducido, comando y rc |
| Caso mínimo | descripción y resultado |
| Pruebas dirigidas | número/resultados reales |
| Generación completa | SHA, fecha, rc y verificación activa |
| Escritura a temporal | comprobada / no corrida y causa |
| Registros fuente | sin cambios / discrepancia concreta |
| Digesto canónico publicado | NO, diferido |
| Rutina automática acreditada | NO por este acto |

### Paso posterior de integración, no autorizado a ejecutar aquí

Después de CAREO/TRÁMITE-4 y del merge de este correctivo, el responsable de publicación actualizará su árbol y generará el digesto sobre ese corte mediante la rutina existente. La nota debe devolver el comando exacto del generador y el runbook pertinente, sin inventar otro publicador. Para el incidente histórico puede mantenerse `--fecha 2026-09-16`; una publicación de otro día llevará su fecha real y SHA actual, nunca se presentará como generada el día anterior.

Si el trámite de Opus ya incluye publicación, informar que el correctivo está listo para que él la haga después de integrarlo; no competir por el archivo. Si hace falta propagación administrativa, anótala en el PR sin asignar numeración. No encargues una auditoría 360 ni un redespliegue del cron de adquisición como sucesor.

## 7. Parada y criterio de avance

Termina cuando el defecto está corregido con regresión y generación comprobada, y el PR tiene una siguiente acción de integración clara; o cuando está demostrado que el fallo ya no existe en el corte vigente. No esperes un ciclo programado dentro de este encargo, no lo simules y no declares automatización acreditada con una ejecución manual.

Auditoría/documentación: aproximadamente 20% del esfuerzo. El resultado principal es un generador utilizable, no un inventario nuevo de pendientes. Deja una causa externa concreta si la integración depende de otro responsable, y completa todo el trabajo técnico seguro ahora.

## Prompt de lanzamiento

> Ejecuta íntegramente ENCARGO-GEN2-DIGESTO-CORRECTIVO-1.md en worktree y rama propios desde origin/main vigente. Autorizo diagnosticar y corregir el generador dentro de su perímetro, pruebas sin corpus/modelos, commits, push y un PR; merges conmigo. Autorizo expresamente diferir la cascada compartida: no escribas firmas, decisiones, numeraciones, gobernanza, tableros ni rutinas. Reproduce antes de corregir; conserva verificación T22/T25, contenido y escritura atómica. Comprueba la generación completa y la escritura sólo en temporal; no publiques el digesto canónico mientras Opus corre CAREO/TRÁMITE-4, no actives cron ni cambies su despliegue. Si el fallo ya no existe, demuéstralo y no inventes un parche. Entrega el producto terminado, pruebas, PR y el paso exacto posterior de publicación. Este mismo encargo puede ejecutarse en Claude Cloud si hace falta, pero nunca simultáneamente en ambos entornos.
