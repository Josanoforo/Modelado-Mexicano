# ENCARGO GEN2 · Handoff verificable del resultado ADQ y salud de investigación

**Entorno:** Codex CLI en CAJA/WSL, sobre el clon operativo que conserva `forense/adq-log/`.
**Prioridad:** alta; corrige un cierre productivo que perdió la acreditación formal de trabajo ya ejecutado.
**Rama sugerida:** `acto/gen2-adq-handoff-resultado-y-salud-1`.
**Fusiones:** exclusivamente Jonás.

## 1. Resultado encargado

Eliminar el punto único de fallo entre el trabajo de Codex y el recibo del
runner: una corrida que haya producido un resultado estructurado válido debe
poder entregarlo, normalizarlo y validarlo aunque `--output-last-message`
quede en `null`; una corrida sin ningún resultado estructurado válido debe
seguir cerrando en fallo, sin reconstruir ciencia desde commits, notas o
estado derivado.

El acto debe entregar:

1. diagnóstico reproducible de la corrida
   `2026-09-17T091024-412182`;
2. handoff primario o redundante, explícito y validable para corridas futuras;
3. selección determinista entre las salidas disponibles, con fallo cerrado
   ante ausencia o contradicción;
4. métricas que distingan investigación validada, evidencia nueva, reducción
   de brecha y adquisición de bytes;
5. regresiones dirigidas y un PR pequeño, sin invocar de nuevo al modelo ni
   descargar datos.

## 2. Punto de partida verificado por mesa

Actualizar estas referencias al iniciar; son premisas, no sustituyen la
consulta del repo:

- `main` observado en `b5ddea0b0f7b93f4c767666adb4cac372672a603`.
- PR #852 abierto: `censo/2026-09-17`, SHA
  `ff844de460c66ebf00a79c41354ef503f5752524`. Regenera demanda y publica el
  recibo; no es estado científico consolidado.
- PR #853 abierto: `adq/2026-09-17`, SHA
  `55377305827a387ddf0fc15229db95fb9a8f95fa`. Conserva tres investigaciones
  y cero adquisiciones nuevas; tampoco es estado consolidado.
- El recibo del 17/sep registra `invocado=si`, tres investigaciones elegidas,
  consumo `3/0/430s`, pero `[ADQ-RESULTADO] ... null`,
  `resultado=resultado_invalido`, `necesidades_atendidas=0` y `exit=65`.
- #853 acredita actividad sobre `DEM-AHORRO-STOCK-DURACION-01`, `NC-0202` y
  `NC-0162`; no acredita por sí solo el JSON final exigido por
  `tools/adq-resultado.schema.json`.
- El contrato reparado el 16/sep para IHSN/ENPOL sigue vigente. No reabrirlo ni
  debilitar sus verificaciones.

Leer completos `AGENTS.md`, `tools/adquiere_cron.sh`,
`tools/adq_doctor.py::valida_resultado_adquisicion`,
`tools/adq-resultado.schema.json`, `tools/adq_investigacion.py` y las pruebas
ADQ directamente relacionadas. Revisar también #852/#853 y la nota de #853.

## 3. Perímetro y preservaciones

Autorizado:

- modificar el runner, el validador o añadir un helper pequeño si es el camino
  mínimo;
- extender únicamente las pruebas ADQ necesarias;
- añadir la nota de diagnóstico/recuperación y archivar este encargo;
- commits, push y apertura de un PR nuevo;
- leer logs gitignorados del run indicado y consultar GitHub.

No autorizado:

- ejecutar `tools/adquiere_launcher.sh`, `tools/adquiere_cron.sh`, Task
  Scheduler, otro Codex/Claude o cualquier corrida productiva;
- búsquedas web sustantivas, descargas, contactos, compras o adopciones
  científicas;
- editar o reescribir el recibo histórico, sus `exit=65`, #852 o #853 para
  aparentar éxito;
- contar ramas, notas, diffs, commits o checkpoints como sustituto de un
  resultado estructurado válido;
- cambiar calendario, modelo, timeouts, cupos, privilegios, criterios de
  suficiencia o reglas de selección;
- tocar el trabajo concurrente de #850, #851 o #854 salvo conflicto material
  inevitable; si aparece, rebasar y mantener los perímetros separados;
- fusionar PR.

Preservar corpus, manifiestos, ledgers, reservas, cursores, ramas operativas y
modificaciones ajenas. No incluir `forense/adq-log/` ni archivos sensibles en
Git.

## 4. Diagnóstico obligatorio antes de editar

En el clon operativo, localizar para `run_id=2026-09-17T091024-412182`, cuando
existan:

- `forense/adq-log/<run_id>-codex.jsonl`;
- `forense/adq-log/<run_id>-codex.stderr.log`;
- `forense/adq-log/<run_id>-codex-final.json`;
- su salida normalizada, validación, prompt y ledger diario;
- checkpoints de presupuesto y referencias remotas exactas.

Registrar rutas, tamaños y SHA-256, sin copiar los logs al repo. Determinar con
evidencia cuál caso ocurrió:

A. Codex nunca emitió un objeto conforme al esquema.
B. El JSONL contiene exactamente un objeto final conforme, pero
`--output-last-message` escribió `null`.
C. Existió un handoff temporal conforme usado para persistir investigación,
pero no llegó al canal final.
D. El objeto existe y fue rechazado por normalización/validación.
E. Hay varios objetos incompatibles y no puede elegirse uno sin arbitraje.

No comenzar por asumir B o C. El informe debe mostrar el primer punto donde se
perdió la salida y distinguir fallo de ejecución, transporte, normalización,
validación y publicación.

## 5. Contrato de handoff corregido

Implementar el cambio mínimo que satisfaga estas invariantes:

1. Antes de invocar Codex, el wrapper define una ruta runtime única por
   `run_id`, dentro de `forense/adq-log/`, y la inserta literalmente en el
   prompt. Codex debe escribir allí, de forma atómica, el mismo objeto final
   que entrega al canal de cierre, después de conocer sus refs y SHA remotos.
2. El wrapper conserva `--output-schema` y `--output-last-message`; el nuevo
   handoff es redundancia verificable, no permiso para aceptar prosa libre.
3. Cada candidato se parsea, normaliza con las selecciones autoritativas y
   valida con la misma función de producción. No crear un validador indulgente.
4. Si sólo un candidato es válido, se usa ese. Si dos son válidos, deben ser
   canónicamente iguales después de normalizar. Si difieren, cerrar con error
   explícito de conflicto; nunca escoger «el más completo».
5. Si ninguno es válido, conservar `resultado_invalido`, `exit=65`,
   `necesidades_atendidas=0` y la liquidación por checkpoints. Notas, ramas y
   archivos modificados no pueden completar el JSON faltante.
6. Publicar en la huella el origen aceptado del resultado —por ejemplo
   `resultado_origen=last-message|handoff|ninguno|conflicto`— y una causa breve
   verificable. No exponer rutas locales completas.
7. El candidato aceptado y el informe de validación quedan en runtime para
   diagnóstico. No se versionan automáticamente.

Si los logs demuestran una causa más pequeña y una solución igualmente fuerte,
puede usarse, pero debe conservar todas las invariantes anteriores. No añadir
un sistema general de replay.

## 6. Contabilidad y salud: cuatro cosas distintas

No redefinir `necesidades_atendidas` para volver verde el recibo. Debe contar
solamente investigaciones presentes en el resultado aceptado, una por elegido
y en el orden validado. Los checkpoints y `presupuesto_consumido` acreditan
trabajo iniciado/consumo aunque el cierre sea inválido.

Separar en la huella, con nombres compatibles con el lector vigente:

- investigaciones seleccionadas;
- investigaciones iniciadas según checkpoints;
- investigaciones validadas/atendidas según el resultado aceptado;
- objetos intentados, objetos adquiridos y bytes nuevos;
- investigaciones con evidencia nueva y con reducción de brecha.

Para evidencia/reducción, usar comparación mecánica pre/post de los estados de
las necesidades elegidas, capturada antes de invocar el hijo. No confiar en una
afirmación libre del modelo. Como mínimo:

- evidencia nueva: ruta de evidencia añadida y existente, o candidata nueva
  estructurada en el resultado;
- reducción de brecha: mejora explícita de una dimensión de suficiencia o de
  `uso_habilitado`, con orden documentado; no contar mero cambio de texto,
  cursor, fecha, PR o publicación;
- sin avance: investigación válida que no cumple ninguna de las anteriores.

No borrar los campos actuales. Ajustar `salud_trabajo` para que cero bytes no
equivalga automáticamente a cero evidencia, y para que publicación exitosa no
equivalga a salud. Mantener categorías distinguibles, por ejemplo:

- `AVANCE_ADQUISICION`;
- `REDUCCION_BRECHA`;
- `EVIDENCIA_NUEVA_SIN_REDUCCION`;
- `EJECUCION_SIN_EVIDENCIA_NUEVA`;
- `RESULTADO_INVALIDO`.

Actualizar el lector/vigilante sólo donde sea necesario para comprender estas
categorías; no declarar sano un ciclo sólo por `exit=0`.

## 7. Tratamiento de la corrida del 17/sep

Sin invocar otro modelo ni editar su historia:

- Si existe exactamente un artefacto estructurado original que pase esquema,
  selecciones, evidencia y refs remotas, revalidarlo mediante el código
  corregido y añadir una nota de recuperación. La nota debe conservar el
  `exit=65` y el `null` publicados, declarar que es revalidación posterior y
  separar investigaciones, adquisiciones, bytes y aptitud.
- Si no existe ese artefacto, no reconstruirlo desde #853. Documentar que #853
  contiene evidencia operativa pendiente de revisión, pero la corrida no puede
  recibir cierre exitoso retroactivo. El correctivo futuro sigue siendo un
  resultado completo.
- No regenerar ni fusionar la demanda de #852. Comprobar únicamente que el
  nuevo código no rompe su relación con el recibo.

La lectura sustantiva esperada, si el artefacto original la acredita, es:

- adquiridos nuevos: cero;
- investigaciones: tres;
- `DEM-AHORRO-STOCK-DURACION-01`: quinto ciclo, sin reducción; acción explícita
  de mesa ya identificada;
- `NC-0202`: evidencia existente, aún incompatible para el uso completo;
- `NC-0162`: mejora documental/diseño y sólo `APTA_ALCANCE_MENOR`.

No elevar esta lectura a estado consolidado mientras #853 siga abierto.

## 8. Pruebas de aceptación

Añadir fixtures mínimos y ejecutar primero pruebas dirigidas. Deben cubrir:

1. `last-message` válido, handoff ausente: cierre normal.
2. Handoff válido, `last-message=null`: se recupera el objeto válido, se
   normaliza y se valida; tres investigaciones pueden dar
   `necesidades_atendidas=3` con cero objetos/bytes.
3. Ambos válidos e iguales: cierre único, sin doble conteo.
4. Ambos válidos pero distintos: fallo cerrado y sin contabilidad científica.
5. Ambos ausentes/inválidos: `exit=65`, resultado inválido, presupuesto
   preservado por checkpoints.
6. Rama, nota o estado persistido sin JSON válido: no se reconstruye resultado.
7. Publicación declarada con ref/SHA incorrectos: sigue fallando.
8. Investigación válida con evidencia nueva y cero descargas no se clasifica
   como «sin evidencia».
9. Investigación válida que sólo mueve fecha/cursor no se presenta como
   reducción de brecha.
10. Adquisición válida mantiene verificaciones de manifiesto, hashes,
    pertinencia y publicación reparadas el 16/sep.

Ejecutar, como mínimo, las pruebas ADQ modificadas y las regresiones existentes
de cierre, continua, contrato y cableado. Comparar contra baseline vigente; no
perseguir fallos heredados ajenos.

No probar lanzando el servicio real. Si hace falta recorrer el shell, usar el
seam de definición o un fixture aislado con dobles de Codex/git y directorio
temporal.

## 9. Entrega

Abrir un PR nuevo y reportar:

1. causa comprobada del `null` y primer punto de pérdida;
2. regla de selección del resultado y comportamiento fail-closed;
3. campos/categorías de salud añadidos o corregidos;
4. dictamen de recuperación del run del 17/sep: revalidable o no revalidable,
   con razón;
5. pruebas ejecutadas y baseline;
6. archivos modificados y confirmación de que #852/#853 no fueron reescritos;
7. SHA remoto del PR y orden de integración recomendado si existe dependencia.

Parar cuando el handoff futuro esté protegido, la contabilidad no pueda
inventar ni perder trabajo válido, el incidente esté dictaminado y el PR esté
listo para revisión. No esperar otra corrida productiva como sustituto de las
pruebas y no dispararla para «comprobar».

## Prompt de lanzamiento

> Ejecuta íntegramente `ENCARGO-GEN2-ADQ-HANDOFF-RESULTADO-Y-SALUD-1.md` en Codex CLI sobre CAJA/WSL y el clon operativo que conserva los logs del run `2026-09-17T091024-412182`. Actualiza primero contra `origin/main`, informa worktree/rama/HEAD/status y verifica el estado actual de #852/#853. Autorizo leer los logs gitignorados, implementar el handoff redundante y fail-closed, corregir la clasificación mecánica de salud, añadir pruebas y nota de diagnóstico, hacer commits, push y abrir un PR nuevo. No invoques Task Scheduler, el runner productivo, otro agente ni nuevas búsquedas/adquisiciones; usa fixtures y replay dirigido sin modelo. No reconstruyas un resultado científico desde diffs, notas, checkpoints o ramas: sólo revalida el run histórico si existe un artefacto estructurado original que pase el contrato completo. Conserva el `null`, `exit=65`, recibos, presupuesto, corpus, cursores y PR #852/#853; cero bytes no significa cero investigación, y publicación exitosa no significa salud. No cambies calendario, modelo, cupos, criterios científicos ni trabajo concurrente. No fusiones: las fusiones quedan conmigo.
