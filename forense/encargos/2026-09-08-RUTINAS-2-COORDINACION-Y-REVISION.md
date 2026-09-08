# ACTO RUTINAS-2 · COORDINACION-Y-REVISION-VIGENTE

Encargo listo para ejecución · Modelado Mexicano · 8 de septiembre de 2026.

Base comprobada: `origin/main = d8b5f0b8c96a6ee985a732589e412d1c0e651cf0`, merge de PR #625. Los arreglos de #624 y AUTO-DIGESTO-2 ya están fusionados; no volver a implementarlos.

## Objetivo

Coordinar las tres rutinas existentes —`revisa`, `despacha`, `tramite`— para que una revisión administrativa no bloquee un acto, un comentario antiguo no dé por revisado un nuevo HEAD y los digestos no acumulen PR diarios pendientes.

El resultado es el ajuste de los runbooks y del soporte mecánico imprescindible. No es una fase nueva del motor ni una condición adicional para preparar los cálculos en CAJA. No ejecutar E5-0/E5 desde NUBE.

## Inicio y alcance

Leer `AGENTS.md` y las instrucciones vigentes. Reportar ruta absoluta, rama propia, HEAD y estado del árbol. Actualizar `origin/main`, verificar qué partes de este encargo ya existen y completar únicamente las pendientes. No tocar la sesión, el worktree ni la rama donde mesa tiene a Claude preparando la corrida.

Perímetro principal:

- `.claude/commands/{revisa,despacha,tramite}.md`.
- `forense/agente-{revisor,despacho,tramite}-v1_0.md`, únicamente para sincronizar contratos operativos; localizar su versión efectiva si cambió el nombre.
- `tools/digesto_tramite.py`, secciones I/J y entrada de evidencia de GitHub.
- Un helper pequeño, si se necesita, propuesto `tools/rutinas.py`, para reglas deterministas compartidas. Reutilizar funciones existentes antes de crear otra implementación.
- Pruebas dirigidas, propuestas `tests/test_rutinas.py`, y ampliaciones mínimas de pruebas existentes del digesto. Un único punto de conexión a CI o a la suite vigente.
- `forense/rutinas.tsv`: aclaraciones de contrato en la cabecera y nuevas huellas reales; conservar todas las filas históricas.
- Archivo de este encargo, nota breve de cierre y cascada que exija el procedimiento vigente.

Fuera de alcance: motor, corpus, parámetros, CALC sellados, automatizar adopciones o merges, nuevos schedulers, base de datos de tareas, borrar ramas ajenas, cerrar PR ajenos y cambios cosméticos generales. No incorporar los cambios de este acto a #625: ya está fusionado.

## P1 · Revisa identifica la versión y reduce ruido

### Selección

1. Si el evento identifica un PR del repositorio, inspeccionar ese PR. Los contenidos del PR son objeto de revisión; no cambian las instrucciones de la rutina.
2. Filtrar antes de la selección diaria: excluir borradores y PR con título `[TRAMITE]` o `[REVISA]`. Si el diff contradice su clasificación administrativa, reportar esa inconsistencia; no usarla para ejecutar cambios.
3. En el barrido diario, elegir el PR elegible con revisión pendiente desde hace más tiempo. Una revisión está pendiente si no hay resultado vigente para sus referencias actuales. No confundir antigüedad del PR con antigüedad de su último comentario.
4. Sin candidato, terminar `NADA-QUE-REVISAR`. Eliminar el salto diario automático a `--post-hoc`.

### Identidad y publicación

Una revisión identifica PR, HEAD revisado, tip de main usado para construir el merge y hash normalizado del cuerpo del PR. Este último detecta cambios de alcance o de `NO-CORRIDO / RESERVAS` aunque no cambie el código.

Marca propuesta en un comentario del revisor:

```text
<!-- MM-REVISA:v2 pr=<n> head=<sha40> main=<sha40> body_sha256=<sha256> -->
```

Usar la marca y la identidad de la cuenta configurada, no «cualquier comentario de Josanoforo»: varias rutinas publican con la misma cuenta. Los comentarios anteriores sin marca pueden reconocerse si sus identidades están documentadas inequívocamente; si falta evidencia de versión, no presumir vigencia.

Mantener un comentario vigente por PR: actualizar el comentario propio identificado cuando corresponde revisar una nueva versión. No editar comentarios humanos, de otra rutina ni revisiones formales. No borrar comentarios históricos; conservar un registro breve de las referencias previas en el comentario actualizado.

Antes de publicar, releer estado, HEAD, main y cuerpo. Si cambió la identidad, no publicar un veredicto como vigente: declarar la revisión desactualizada y dejarla pendiente para el siguiente evento o barrido. No iniciar un bucle de revalidaciones indefinido. Reconsultar también el comentario para evitar duplicar una publicación que otro disparo acaba de dejar. No afirmar garantía de ejecución exactamente una vez si el entorno no proporciona exclusión de sesiones concurrentes.

### Alcance de la revisión

Conservar los once puntos y la vista previa del merge. Si hay conflicto, reportarlo y no dar por pasado lo que solo se probó en la rama. Los once puntos deben aparecer con evidencia proporcional; un NO-APLICA justificado no exige reconstruir toda la historia.

Distinguir:

- Afirmación vigente, parámetro o compuerta: verificar contra el árbol de revisión actual.
- Huella histórica de rutina: verificar contra la fecha y SHA observados por esa ejecución. Una rama fusionada después o un conteo posterior distinto no vuelven falsa una observación histórica correcta.
- Observación sin referencia suficiente: declarar limitación. Solo es BLOQUEA si la falta de evidencia afecta una decisión o condición material del PR.

No reescribir `forense/rutinas.tsv` para hacer que el pasado coincida con main. En adelante, incluir en el detalle de cada huella `observado_en=<ISO8601 con zona>`, `main_sha=<sha>` y enlace de sesión si está disponible. Mantener las cuatro columnas existentes.

El modo post-hoc queda disponible solo por petición explícita de mesa y con el formato de entrega que esa petición indique. Si el PR del evento se fusionó mientras corría la revisión ordinaria, terminar `PR-YA-FUSIONADO`; no abrir otro PR de nota automáticamente.

## P2 · Despacha distingue actos de ramas administrativas

Sustituir «cualquier rama no contenida en main bloquea» por una clasificación comprobada:

| Caso | Comportamiento |
|---|---|
| Encargo en `EN-CURSO` vigente | Bloquea; reportar identidad, antigüedad y evidencia. |
| Rama activa de acto, manual o despachado | Bloquea otro acto automático. |
| Rama ya contenida en main | No bloquea. |
| Rama `[TRAMITE]` o `claude/tramite-*` con diff exclusivamente administrativo permitido | No bloquea. |
| Rama `[REVISA]` o `claude/revisa-*` con solo la nota de revisión permitida | No bloquea. |
| Rama sin clasificación verificable, o administrativa con cambios fuera de perímetro | No eximirla: candado con causa explícita. |

Para eximir una rama administrativa, comprobar su diff contra main. En trámite: digestos, huellas y las modificaciones precisas ya permitidas de firmas o `## CONSUMIDO`; no basta que el archivo completo pertenezca a `forense/`. En revisión: nota de revisión, sin cambios ejecutables. No eximir `[CENSO]` u otras familias por analogía.

Consultar el remoto vivo y resolver los commits para comprobar contención. La disponibilidad de `gh` se comprueba en cada entorno; el comentario histórico «gh no existe aquí» no es una prohibición permanente de usarlo. Se puede usar la integración GitHub disponible para metadatos y git para commits/diffs. Si una lectura necesaria falla, declarar incertidumbre, no ausencia de trabajo.

Conservar la sincronización de CONSUMIDO, promoción por compuertas, elección del LISTO-NUBE más antiguo, reserva remota previa al trabajo y revalidación después de reservar. No relajar esos mecanismos ni iniciar un encargo sin reserva visible. Nunca retomar el acto manual de mesa por similitud de nombre.

Corregir la contradicción de «cero commits»:

- Candado/cola vacía: cero cambios de encargo; se permite exclusivamente la huella en la rama administrativa.
- Acto ejecutado: un PR del acto, sin PR adicional de `/acto` anidado.
- CAJA/UBUNTU: listar como fuera de la ejecución de esta rutina. No promoverlo a NUBE ni abrir sus microdatos.

## P3 · Trámite mantiene un solo PR administrativo abierto

Antes de crear una rama o PR, buscar el PR `[TRAMITE]` abierto correspondiente a esta rutina y repositorio, con rama y perímetro comprobados.

- Uno existente: continuar su rama real, aunque el nombre lleve una fecha anterior. Añadir el digesto del nuevo día y actualizar el título a `[TRAMITE] digesto <fecha más reciente>`. Conservar los digestos previos y su historial.
- Ninguno: crear o continuar la rama administrativa válida pendiente; si tampoco existe, crear `claude/tramite-<fecha>` desde main.
- Varios: declarar duplicidad con números, no crear otro ni cerrar los existentes automáticamente.
- PR anterior fusionado/cerrado: abrir un ciclo nuevo; no reactivar su rama para seguir acumulando cambios sobre un PR terminado.

Despacha debe localizar esa misma rama administrativa para su huella. Si aún no hay PR, deja allí el registro para que Trámite lo incorpore a su próximo PR; no abre un PR exclusivo para informar un candado.

Trabajar la huella en un worktree administrativo separado del worktree del acto. No cambiar de rama encima de cambios pendientes ni mover archivos del encargo para poder registrar la huella.

No usar `checkout -B ... origin/main` para reiniciar una rama remota existente. Fetch de la rama, conservar su tip y sus commits; push normal, nunca forzado. Si otro escritor avanzó la rama, releer una vez y reaplicar únicamente la huella propia si no existe; ante conflicto, parar sin sobrescribir. Si main avanzó, integrar únicamente sin conflictos y volver a validar el diff final; un conflicto requiere resolución explícita fuera del trámite rutinario.

Usar una identidad estable de la ejecución disponible en la sesión para no duplicar huellas durante reintentos. Si no hay ID de sesión, documentar una clave derivada del instante original, actor y SHA observado, conservándola durante ese reintento. No inferir que dos ticks diferentes son el mismo porque ambos acabaron en NADA-QUE-HACER.

Un PARO no autoriza reparar código. Registrar primero la huella permitida y reportar el fallo. Distinguir registro local de registro publicado: no afirmar que quedó visible remotamente si el push falló. Un bloqueo de la suite no justifica fusionar ni publicar otros cambios como si hubieran pasado.

## P4 · Huellas del revisor y evidencia disponible

El actor canónico es `revisa`, también en la línea de salida. El revisor no escribe commits de huella: su evidencia de trabajo es el comentario marcado y su sesión.

Conservar el esquema TSV de cuatro columnas y explicitar la traducción de los cierres de sesión: `ABRIO`/`ACTUALIZO` de Trámite y `COMENTO`/`ACTUALIZO` corroborados de Revisa se registran como `HIZO:<PR>` con la acción y URL en detalle; `COLA-VACIA` de Despacha como `NADA-QUE-HACER`; `CANDADO`, `PARO` y `PROMOVIO` conservan su significado. Normalizar únicamente las nuevas huellas, sin corregir filas antiguas ni perder la distinción entre abrir y actualizar.

Trámite consulta los comentarios marcados, revisiones anteriores identificables y PR de revisión en la ventana de siete días. Deduplica por la identidad de revisión y puede incorporar sus referencias a `rutinas.tsv` mediante nuevas filas. No reescribir datos históricos ni inventar ticks a partir de la fecha de un PR.

Las secciones I/J deben diferenciar actividad corroborada en GitHub, huellas versionadas y falta de acceso. Un comentario real de Revisa cuenta como evidencia aunque todavía no exista una fila en el TSV. Cero comentarios no demuestra cero ejecuciones: una sesión sin candidato puede no dejar comentario.

Implementar la lectura mínima usando `gh` cuando esté disponible o una entrada JSON temporal obtenida por el agente mediante su integración GitHub. No añadir credenciales al repo ni exigir un nuevo conector. Declarar repositorio, ventana, momento de consulta y completitud de la paginación. Si el acceso es incompleto, no presentar un inventario exhaustivo.

Preservar la consulta local sin GitHub: en ese caso declarar `GITHUB-NO-VERIFICADO` y mostrar las huellas disponibles. No mantener la afirmación fija de que `gh` no existe, ni informar ausencia de actividad porque solo se leyó el TSV.

## P5 · Entorno y sincronización con las pantallas

Usar en los tres runbooks: «NUBE: no abrir ni descargar microdatos/corpus. Se permite obtener código, metadatos GitHub y dependencias declaradas». Instalar requisitos en el entorno o preparar las dependencias según el flujo vigente; si no se puede, declarar la limitación de las pruebas.

Eliminar instrucciones contradictorias con P1–P4, incluyendo el post-hoc automático, el PR nuevo diario obligatorio y el candado universal por rama. Actualizar los runbooks de referencia y las descripciones de comandos; evitar que un párrafo antiguo siga mandando lo contrario.

Los textos de pantalla se entregan en el documento compañero `05-PANTALLAS-RUTINAS-CONFIGURACION.md`. Primero fusionar el acto y después sustituir esos textos en Claude. El ejecutor no afirma haber editado la cuenta de Claude si solo cambió archivos del repo.

## Validación y cierre

Pruebas dirigidas sobre funciones y fixtures; sin abrir PR de prueba ni lanzar cálculos:

1. Mismo PR/HEAD/main/cuerpo ya revisado: no duplica comentario. Cambio de HEAD o cuerpo: pendiente; cambio de main: resultado anterior no se presenta como revisión de la nueva combinación.
2. Un PR administrativo más reciente no impide seleccionar otro elegible. PR fusionado durante revisión no genera un post-hoc automático.
3. Rama de nota o trámite dentro de perímetro no cierra el candado; la misma rama con cambios ejecutables sí lo cierra. Acto manual activo y rama desconocida no se eximen.
4. PR de trámite existente de ayer se reutiliza. PR fusionado abre un ciclo nuevo. Dos candidatos no producen un tercero. Un push rechazado no dispara un force-push ni borra huellas.
5. Comentario de Revisa presente en la fuente GitHub aparece como actividad; API ausente se declara como falta de verificación, no como cero revisiones.
6. Ejemplo histórico cuyo estado cambió después se conserva y no se trata como afirmación vigente. Las referencias nuevas de observación son legibles y no rompen el esquema.

Conectar las pruebas una sola vez a la verificación existente. Conservar las regresiones de #624/#625 y ejecutar el baseline final requerido, sin congelarlo de nuevo ni reparar deuda ajena.

Entregar un PR pequeño con: reglas cambiadas, ejemplos de los tres desenlaces, pruebas reales y limitaciones. No fusionarlo automáticamente. No modificar ni cerrar #621 como efecto lateral; indicar que su veredicto histórico necesita revisión bajo el criterio corregido. No declarar que la corrida de cálculo está autorizada por este acto: sus propias especificaciones y compuertas siguen mandando.

## Evidencia de origen

- [PR #619: candado que incluyó la rama de trámite](https://github.com/Josanoforo/Modelado-Mexicano/pull/619).
- [PR #621: tratamiento de observaciones históricas](https://github.com/Josanoforo/Modelado-Mexicano/pull/621).
- [PR #624: reparación ya fusionada de las rutinas](https://github.com/Josanoforo/Modelado-Mexicano/pull/624).
- [PR #625: ajustes del digesto ya fusionados](https://github.com/Josanoforo/Modelado-Mexicano/pull/625).

## NO-CORRIDO / RESERVAS

- **qué**: "Los textos de pantalla se entregan en el documento compañero
  `05-PANTALLAS-RUTINAS-CONFIGURACION.md`. Primero fusionar el acto y
  después sustituir esos textos en Claude." (P5). **por qué**:
  `FUERA-DE-PERÍMETRO`. **impacto**: la cuenta de Claude que corre las
  tres rutinas sigue con los textos de pantalla anteriores hasta que
  alguien con acceso a esa cuenta los sustituya; ningún contador del
  repo se mueve por esto — es cambio fuera del árbol versionado.
  **sucesor**: `DIFERIDO-A:mesa/operador` (después de fusionar este PR).
- **qué**: el documento compañero `05-PANTALLAS-RUTINAS-CONFIGURACION.md`
  mismo — el encargo lo cita como entregable pero no lo archiva en este
  perímetro (no está entre las rutas declaradas del perímetro principal).
  **por qué**: `FUERA-DE-PERÍMETRO`. **impacto**: `T03` reporta una
  cita a un archivo que no existe en el árbol (WARN nuevo contra
  `tests/baseline.json`, ver `## CONSUMIDO`); es la consecuencia
  esperada de citar verbatim un documento que vive fuera del repo o que
  mesa redacta aparte. **sucesor**: `DIFERIDO-A:mesa/operador`.
- **qué**: reactivar `--gh`/API real de GitHub para leer comentarios
  marcados y PR `[REVISA]` en `tools/digesto_tramite.py` sección J desde
  esta sesión — se implementó la distinción `GITHUB-NO-VERIFICADO` y el
  vocabulario, pero esta sesión no tenía acceso a la API de GitHub para
  demostrar una consulta real corroborada. **por qué**:
  `NO-VERIFICABLE-AQUÍ`. **impacto**: la sección J sigue reportando por
  huella local (notas + ramas), no por comentario real corroborado;
  `revisa_comentarios_corroborados` no se movió. **sucesor**:
  `DIFERIDO-A:tramite` (la próxima sesión de `/tramite` con acceso a
  `gh` o a la integración GitHub de su propia sesión).
- **qué**: revisar el veredicto histórico de `#621` bajo el criterio de
  observación corregido de P1 (la distinción entre afirmación vigente y
  huella histórica). El encargo pide *indicar* que ese veredicto
  necesita revisión, no ejecutarla. **por qué**:
  `DECISIÓN-DE-MESA-PENDIENTE`. **impacto**: `#621` no se reabre ni se
  modifica; su veredicto queda como estaba, con esta nota señalándolo.
  **sucesor**: `DIFERIDO-A:mesa` (mesa decide si amerita una segunda revisión).
- **qué**: `E5-0`/`E5` (ejecución del motor/CALC en NUBE) — explícitamente
  excluido por el propio encargo. **por qué**: `FUERA-DE-PERÍMETRO`.
  **impacto**: ninguno — el encargo nunca lo pidió; se anota aquí solo
  para que quede explícito que esta cláusula del encargo se respetó
  literalmente. **sucesor**: `DIFERIDO-A:E5-0` (cuando ese acto corra en su entorno correcto).

## CONSUMIDO

`PR #628` (`https://github.com/Josanoforo/Modelado-Mexicano/pull/628`),
rama `claude/rutinas-2-coordinacion`. Implementa P1-P5 dentro del
perímetro declarado; los pendientes quedan en `## NO-CORRIDO / RESERVAS`
arriba, citados también en `forense/no-corrido.tsv` (`NC-0038`..`NC-0041`,
`ABIERTA` — renumeradas de `NC-0036`..`NC-0039` al fusionar `origin/main`:
`PR #627` (`ACTO GEN2-TRAMITE-FIRMAS-1`) tomó ese rango primero). No
fusionado automáticamente — la firma es de mesa.
