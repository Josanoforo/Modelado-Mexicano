> **Insumo externo (ChatGPT/Astra) · entregado a dirección 9/sep/2026 ·
> registrado por ACTO GEN2-SONDA-ADQ-CABLEADO conforme a A.3 y regla de
> mesa 4 · H3/H4/H5/H6 confirmados por dirección en clon propio · el
> texto de abajo no se edita**

---

# SONDA y adquisición · revisión del cableado y encargo de corrección

**Astra → Jonás / dirección (Claude) · 9 de septiembre de 2026.**

**Dictamen: adquisición sí dejó huella hoy. El conjunto todavía no está listo para darse por verificado de extremo a extremo: hay defectos reproducidos de vigilancia, manejo de fallos y entrega de trabajo a CAJA.**

## 1. Qué ocurrió hoy

**Observado.** En `main = 66eed1b4f4a34dcf20a3876c53ac11da12244396`, el PR **#658** está fusionado y `forense/censo-raiz/2026-09-09.txt` termina con:

```text
[ADQ-PDN] 2026-09-09: fuera de ventana (día 9, ventana 1-3)
[ADQ] 2026-09-09 07:33: invocado=si motivo=- exit=0 duracion=228s commits_nuevos=0 ramas_nuevas=1 archivos_modificados=1 run_id=2026-09-09T073007-371
```

El censo registra 465 archivos, tres nuevos y 462 registrados. El PR fue fusionado a las `15:38:35Z`. [PR #658](https://github.com/Josanoforo/Modelado-Mexicano/pull/658), [huella publicada](https://github.com/Josanoforo/Modelado-Mexicano/blob/66eed1b4f4a34dcf20a3876c53ac11da12244396/forense/censo-raiz/2026-09-09.txt).

**Interpretación.** El runner arrancó a las 07:30:07 según su `run_id`, invocó Claude y recogió salida 0. La ventana PDN se omitió correctamente porque era día 9. Esto demuestra ejecución del runner y publicación de su huella; no demuestra por sí solo una adquisición nueva ni qué disparador lo inició. El cierre cita la hora del runner, sin zona explícita en esa línea.

**Consecuencia.** No corresponde diagnosticar "hoy no corrió". Tampoco exigir un PR `[ADQ]` sin contenido: el runbook permite cero commits del agente cuando no hay trabajo. El PR `[CENSO]` contiene también las huellas PDN y ADQ, por eso buscar únicamente un título `[ADQ]` puede ocultar visualmente la corrida.

**Límite.** No tuve acceso al Windows/WSL de mesa ni al log local de Claude. No certifico desde GitHub el disparo autónomo de la tarea de producción, su configuración instalada hoy ni el motivo exacto de la caminata vacía.

## 2. Recorrido real: qué está conectado

| Desde | Hacia | Mecanismo actual | Resultado de la revisión |
|---|---|---|---|
| Windows Task Scheduler | WSL / runner | Tarea `\ModeladoMexicano\AdquiereCron`, lun–vie 07:30, `wsl.exe … bash -lc …/adquiere_cron.sh` | Instalador en repo; instalación actual pendiente de consultar en CAJA |
| Runner | Configuración / corpus | `adq-config.yaml`, clon, `data/raw`, raíz `descargas_mx` | Conectado, con reservas en manejo de fallos |
| Runner | Censo / PDN | Rama diaria, commits y PR de censo | Huella real de hoy consolidada |
| Runner | Agente `/adquiere` | Extrae el bloque `text` del runbook y lo pasa a `claude -p` | Conectado; la carga/ejecución interna de la skill no se acredita solo con exit 0 |
| `/mapea` | `/sonda` | Recomendación explícita para un negativo material | Puente de conversación; no invocación automática |
| `/sonda` | Cola de adquisición | `upsert_fila` en registro canónico + regeneración de vista | Escritor y vista conectados; selección posterior incompleta para algunos estados permitidos |
| `/adquiere` | Corpus / manifiesto / cola / relaciones | Descarga, integridad, registro y PR para firma | Contrato presente; hoy no se acredita alta nueva |
| Censo/ADQ | T-CRON → doctor / suite | Lee commits de la rama diaria | Defecto real tras retirar la rama y riesgo de atribuir huella de otra fecha |
| Piloto SONDA-3 | Trabajo visible para CAJA | Encargo `LISTO-CAJA` | Falta `ENTORNO: CAJA`; el listado mecánico de `/despacha` no lo encuentra |

SONDA no es un cron adicional. El runner tiene una fase llamada `SONDA-RED`, que es un `curl` de conectividad; **esa fase no ejecuta la investigación `/sonda`**. No existe en el prompt diario una orden de ejecutar automáticamente el piloto SONDA-3. La separación puede ser correcta, pero hay que nombrarla para no confundir una corrida de adquisición con una validación de SONDA.

Fuentes: [runner](https://github.com/Josanoforo/Modelado-Mexicano/blob/66eed1b4f4a34dcf20a3876c53ac11da12244396/tools/adquiere_cron.sh), [runbook de adquisición](https://github.com/Josanoforo/Modelado-Mexicano/blob/66eed1b4f4a34dcf20a3876c53ac11da12244396/forense/agente-adquisicion-v1_0.md), [SONDA](https://github.com/Josanoforo/Modelado-Mexicano/blob/66eed1b4f4a34dcf20a3876c53ac11da12244396/.claude/commands/sonda.md), [despacha](https://github.com/Josanoforo/Modelado-Mexicano/blob/66eed1b4f4a34dcf20a3876c53ac11da12244396/.claude/commands/despacha.md).

## 3. Hallazgos que deben corregirse

### H1 · T-CRON puede perder un cierre verdadero y aceptar uno de otro día — prioridad alta

**Observado.** `_t_cron_commits_censo()` busca una rama `censo/<fecha>`, examina prefijos de los últimos 50 commits y toma el último asunto `[ADQ]` sin filtrar su fecha. `t_cron_estado()` solo comprueba `invocado=si` y `exit=0`; no valida fecha ni `run_id`. Si no encuentra la rama, el fallback solo registra que existe un archivo de censo, sin leer su cierre.

Pruebas ejecutadas:

```text
Cierre del 8/sep evaluado para 9/sep → COMPLETO
Cierre con solo prefijo [ADQ], sin [CENSO]/[ADQ-PDN] → COMPLETO
Rama ausente + archivo de hoy fusionado con cierre → CENSO-SIN-CIERRE
```

El tercer caso también se observó **sin simularlo**: el doctor sobre este checkout devuelve `CENSO-SIN-CIERRE`; la consulta a la ref de GitHub devuelve 404 y `git ls-remote --exit-code` devuelve 2 para `censo/2026-09-09`. El archivo consolidado sí contiene la línea `[ADQ]` transcrita arriba.

**Interpretación.** El vigilante depende de una rama temporal para interpretar evidencia que ya está en `main`. Además, los commits heredados de `main` pueden aportar un cierre anterior a una rama nueva. `COMPLETO` no acredita necesariamente todas las fases del mismo intento.

**Consecuencia / reparación.** Resolver primero la evidencia del día publicada en archivos de censo y contrastarla con la de ramas aún abiertas, sin depender de que sobrevivan después del merge. Validar fecha y, para escrituras nuevas, `run_id`; no combinar fases de intentos distintos. Definir explícitamente si el resultado mostrado describe el último intento o si hubo al menos un éxito en el día; mostrar ambos si discrepan. Una lectura fallida del remoto no equivale a ausencia comprobada. Mantener visibles las fases incompletas o no verificables. No eliminar la historia ni ampliar el baseline para ocultar la señal.

Fuente: [`tests/check.py`, T31](https://github.com/Josanoforo/Modelado-Mexicano/blob/66eed1b4f4a34dcf20a3876c53ac11da12244396/tests/check.py).

### H2 · La entrega SONDA → adquisición no garantiza que la candidata sea seleccionable — prioridad alta

**Observado.** SONDA §6 permite entregar `PENDIENTE` o `SIN-FETCH`. `/adquiere` §1 selecciona `PENDIENTE` y reintentos `NO-OBTENIDO-POR-ESTE-AGENTE` bajo su regla de antigüedad. No define el consumo automático de `SIN-FETCH` ni de un faltante dentro de `OBTENIDO-PARCIAL`. Para una fuente existente, SONDA actualiza la nota con la misma clave; esa modificación no necesariamente cambia su elegibilidad.

El prompt del cron pide las cinco más antiguas con último intento de al menos siete días; la skill ordena primero por prioridad y su descripción pública solo anuncia un argumento numérico, aunque el cuerpo admite fuentes nombradas. No hay una selección determinista común que deje una lista auditable de IDs elegidos y excluidos.

Al corte hay **138 filas**: cero `PENDIENTE`, cero `SIN-FETCH`, una `NO-OBTENIDO-POR-ESTE-AGENTE…` y nueve `OBTENIDO-PARCIAL…`. La única fila del primer grupo es `DD_COMPRANET_DICCIONARIOS_DE_DATOS`; su nota registra intento del 6/sep, menos de siete días antes del corte. **Esto es compatible con una caminata vacía; no prueba la selección interna que hizo Claude hoy.** Los nueve parciales no se vuelven automáticamente nueve trabajos autorizados.

**Interpretación.** Tener la candidata escrita en la cola no demuestra que el próximo cron la vaya a tomar. Una fecha de sondeo tampoco debe reiniciar por accidente el plazo desde la última descarga intentada.

**Consecuencia / reparación.** Unificar selección y orden entre runbook y skill; emitir IDs elegidos, excluidos y razón, incluso cuando son cero. Distinguir en la nota fecha de descubrimiento de vía y fecha de intento efectivo. Para un handoff autorizado, explicitar el objeto faltante, la vía nueva, autorización/cita y el modo de invocación por ID. Una recomendación sin autorización no habilita adquisición por sí misma.

No activar todos los `SIN-FETCH`, parciales o negativos. Usar el vocabulario y cola existentes: un objeto completo conserva `OBTENIDO`; el residual debe tener cobertura y sucesor explícitos. Si se implementa un selector, que sea una función pequeña compartida o una opción de una herramienta existente, sin segunda cola ni nueva rutina.

Fuentes: [contrato de adquisición](https://github.com/Josanoforo/Modelado-Mexicano/blob/66eed1b4f4a34dcf20a3876c53ac11da12244396/.claude/commands/adquiere.md), [cola canónica](https://github.com/Josanoforo/Modelado-Mexicano/blob/66eed1b4f4a34dcf20a3876c53ac11da12244396/data/curacion-registro/cola-adquisicion-registro.tsv).

### H3 · Piloto SONDA-3 listo en prosa, invisible en el listado de CAJA — corrección inmediata

**Observado.** El encargo tiene `ESTADO: LISTO-CAJA` y una línea Markdown `**Entorno asignado:** CAJA/Ubuntu…`, pero no `ENTORNO: CAJA`. `/despacha` lista pendientes de caja mediante `grep '^ENTORNO: CAJA'`. La prueba literal sobre el archivo devuelve falso. Su NC vigente es **`NC-0060` ABIERTA**; el cuerpo histórico del PR #642 menciona otro número candidato, que no debe copiarse como ID actual.

**Interpretación.** La compuerta está satisfecha, pero el anuncio de "esperando caja" no incluye esta pieza. No debe ejecutarla el despachador NUBE ni el cron de adquisición por inferencia.

**Consecuencia / reparación.** Añadir la cabecera canónica `ENTORNO: CAJA`, conservar el texto original y registrar la corrección. Despachar el piloto existente a una sesión CAJA. No redactar otro piloto. Su aceptación exige SONDA §5-bis y el handoff real a adquisición cuando corresponda; un negativo acotado también es resultado válido.

Fuente: [piloto pendiente](https://github.com/Josanoforo/Modelado-Mexicano/blob/66eed1b4f4a34dcf20a3876c53ac11da12244396/forense/encargos/cola/2026-09-08-GEN2-SONDA-3-PILOTO-CAJA.md).

### H4 · El fallo de red no activa la parada prevista — prioridad alta

**Observado.** El shell captura `curl -w '%{http_code}' … || echo 'sin-respuesta'` y después compara igualdad con `sin-respuesta`. Ante una conexión fallida, el resultado reproducido fue **`000sin-respuesta`**. La comparación no entra en `PARO-RED`.

**Interpretación.** El runner puede gastar una invocación de Claude pese a no haber superado la compuerta que promete comprobar. No demuestra que la red haya fallado hoy.

**Consecuencia / reparación.** Capturar por separado el código de salida de curl, el HTTP y la causa; hacer que un fallo de transporte produzca la parada/limitación correspondiente antes de invocar al agente. Un HTTP 403 es una respuesta y un bloqueo de ese destino, no evidencia de ausencia de internet ni inexistencia del objeto. Conservar esa distinción y no extender la parada a fuentes independientes sin razón.

### H5 · Fallar al publicar puede acabar como terminación exitosa — prioridad alta

**Observado.** `commit_censo_linea()` registra `PARO-CENSO-PUSH` pero continúa con `git checkout main`. Con el cuerpo real de la función y un doble que hace fallar únicamente `git push`, la función termina con salida 0. El paso inicial de censo también registra el fallo sin propagarlo. Al final, el runner devuelve el exit de Claude, no un resultado compuesto de trabajo y publicación.

**Interpretación.** `exit=0` del proceso no garantiza que el recibo llegó al repo ni que se abrió el PR esperado. Los contadores tampoco son payloads adquiridos: `ramas_nuevas` incluye la rama del censo y se calcula sobre todas las refs remotas.

**Consecuencia / reparación.** Conservar el trabajo local, registrar fase y error de publicación, y devolver un fallo operativo si falta publicar el recibo requerido. Separar "agente terminó" de "huella publicada / PR localizado". No usar force-push. Reutilizar un PR abierto de la rama; distinguirlo de un fallo real de `gh pr create`. Al reintentar, reconciliar la rama local con la remota sin reescribir historia; si divergen, declarar la situación. No atribuir una rama ajena a adquisición nueva.

### H6 · Timeout y heartbeat no cubren todos los casos que prometen — prioridad media

**Observado.** `timeout` no lleva `--kill-after`. En una prueba acotada con un proceso que ignora SIGTERM, seguía vivo tras cuatro veces el límite; el harness lo eliminó al terminar. La prueba antigua con `sleep` solo cubría un proceso que sí termina con TERM.

La instancia rechazada por `flock` escribe además en el **mismo heartbeat** de la instancia activa. Reproducido con el bloque real de arranque: `RUN-A / STARTED` fue reemplazado por `RUN-B / PARO-LOCK`, aunque A seguía siendo dueño del lock. El archivo no se escribe atómicamente ni se actualiza al cambiar cada fase.

**Interpretación.** Una segunda invocación puede ocultar el estado del trabajo que continúa. El límite de dos horas de Windows no prueba que todos los descendientes Linux mueran ni que el trap alcance a escribir un cierre.

**Consecuencia / reparación.** Añadir escalamiento de terminación después de una gracia finita y comprobar descendientes/lock en un entorno aislado. Solo el dueño del lock actualiza el heartbeat activo; el rechazo se apendiza al log con su propio `run_id`. Escribir el heartbeat por temporal + rename y actualizarlo en las transiciones relevantes. Un proceso muerto sin cierre permanece incompleto; no se inventa un éxito ni una causa de muerte.

H4–H6 se localizaron en el [runner al corte](https://github.com/Josanoforo/Modelado-Mexicano/blob/66eed1b4f4a34dcf20a3876c53ac11da12244396/tools/adquiere_cron.sh).

## 4. Diseño del scheduler: qué está bien y qué falta acreditar

La arquitectura Windows → WSL → runner responde al incidente documentado del 7/sep, cuando cron dentro de WSL no tuvo oportunidad de dispararse. El instalador declara `StartWhenAvailable`, exclusión `IgnoreNew`, límite de dos horas y ejecución con sesión `Interactive`. El runner aporta lock, log, heartbeat y timeout: son defensas pertinentes, aunque tengan las fallas descritas.

La aceptación del 7/sep documenta un **disparo autónomo de tarea temporal** y deja la recuperación real de un disparo semanal perdido como **parcial**. No equivale a certificar toda recuperación futura de la tarea de producción. [Aceptación en CAJA](https://github.com/Josanoforo/Modelado-Mexicano/blob/66eed1b4f4a34dcf20a3876c53ac11da12244396/forense/notas/2026-09-07-ADQ-CRON-V2-P7-aceptacion.md).

La configuración propuesta requiere sesión Windows iniciada; no promete ejecutar con la sesión cerrada. El instalador no pide `WakeToRun`: recuperar una hora perdida y despertar el host son opciones diferentes. Microsoft documenta ambos ajustes por separado. No modificar logon, energía ni reinstalar a ciegas: primero consultar lo realmente instalado. [Microsoft: settings del scheduler](https://learn.microsoft.com/en-us/powershell/module/scheduledtasks/new-scheduledtasksettingsset?view=windowsserver2025-ps).

También hay documentación desfasada: el registro canónico aún encabeza cron de WSL, describe el vigilante anterior y conserva instrucciones históricas de PDN; el instalador y el código ya emplean otro mecanismo. Debe haber una enmienda visible que diga qué sección gobierna hoy. La configuración YAML no es todavía autoridad uniforme del calendario: el runner usa `date` local y T31 fija 07:30/México. Cualquier cambio futuro de hora debe propagarse a los consumidores, no solo al instalador.

**Pregunta de verificación para CAJA:** ¿qué tarea, acción, usuario, hora, zona, política de recuperación y crontab legado están efectivamente instalados? Desde aquí, `check_scheduler_windows()` devolvió `NO-VERIFICABLE`; eso no significa que falte la tarea en tu equipo.

## 5. Pruebas realizadas y alcance

| Prueba | Resultado |
|---|---|
| `tests/test_t_cron.py` | 10 pruebas, cero fallos |
| `tests/test_adq_config.py` | Tres pruebas, cero fallos |
| `tests/test_adq_doctor.py` | Cinco pruebas, cero fallos |
| `bash -n tools/adquiere_cron.sh` | Correcto |
| Vista de adquisición contra render del registro | Coincidencia exacta |
| Cierre de ayer evaluado hoy | Falso `COMPLETO` reproducido |
| Rama retirada, censo fusionado | Falso `CENSO-SIN-CIERRE`, simulado y observado en el checkout real |
| Transporte fallido en la sonda HTTP | `000sin-respuesta`; no entra en PARO |
| Publicación fallida, función real con git doble | Devuelve éxito pese al push fallido |
| Proceso que ignora TERM | Supera el límite; eliminado por el harness |
| Segunda instancia rechazada por lock | Sobrescribe heartbeat del dueño |
| Piloto en el selector literal de CAJA | No aparece |

El CI de `main` estaba verde: [run 34371580139](https://github.com/Josanoforo/Modelado-Mexicano/actions/runs/34371580139). Los tres tests anteriores están enlazados en `verify.yml`; el defecto no es que nadie los ejecute, sino los casos que aún no cubren. GitHub Actions verifica en push/PR o invocación manual; no es el scheduler de adquisición de las 07:30.

No se descargó corpus, no se invocó Claude, no se corrió el runner de producción, no se modificó el repo ni se publicó nada en GitHub. Las inyecciones de fallos utilizaron funciones/bloques aislados, dobles y temporales; no se presentan como ensayo completo de Windows/WSL.

## 6. Encargo propuesto para dirección

**Rótulo propuesto:** `SONDA-ADQ-CABLEADO-Y-HUELLA`. Dirección adapta nombre, números y rutas contra `origin/main` del día y ficha por 0-bis A.3 antes de despachar. Esta revisión no firma nuevas decisiones ni cierra filas.

### P0 · Registrar y congelar los casos

Archivar esta revisión íntegra con procedencia. Reproducir los fallos vigentes; conservar como casos de aceptación los ya probados. Separar cambios del repo y operaciones de la CAJA. Reutilizar `NC-0060` para el piloto; no crear otra deuda equivalente.

### P1 · Reparar el vigilante y el runner

Perímetro sugerido: `tools/adquiere_cron.sh`, `tests/check.py` T31, `tools/adq_doctor.py`, tests específicos y la configuración/documentación directamente afectadas.

- H1: lectura por fecha/intento con fallback a evidencia fusionada, sin requerir rama viva. Compatibilidad histórica explícita cuando una huella no tiene `run_id`.
- H4/H5/H6: transporte separado de HTTP, resultado de publicación preservado, timeout con terminación acotada, heartbeat del dueño y escritura atómica.
- Adjuntar a la huella el SHA realmente usado y las identidades necesarias para correlacionar fases. `invocado=si` y salida 0 no se rotulan como número de fuentes obtenidas.
- La extracción del prompt debe comprobar que hay un único bloque esperado; el `awk` actual recoge todos los bloques `text` del archivo. Validar configuración después de sincronizar; no silenciar una configuración rota sustituyéndola por defaults sin informar.
- Reutilizar el mismo PR diario cuando exista y conservar el recibo local si falla la red. No crear un servidor, un scheduler duplicado ni reintentos ilimitados.

### P2 · Cerrar las discrepancias de SONDA y selección

Perímetro: skill SONDA/adquisición, runbook de adquisición, cabecera del piloto y prueba dirigida de selección. Definir un solo orden y contrato de elegibilidad, con IDs y razones de exclusión. Conservar autoridad humana, no barrer todos los parciales por defecto. Añadir `ENTORNO: CAJA` y comprobar con el **comando real** de `/despacha` que el piloto se anuncia.

### P3 · Verificación en CAJA y piloto ya existente

Una sesión local consulta scheduler, action, logs y crontab; contrasta el evento programado con el `run_id` de hoy. Corrige únicamente lo que esa lectura demuestre necesario. No activar un segundo scheduler ni retirar el primero sin evidencia de cuál está operando.

Ejecutar el piloto SONDA-3 pendiente con el presupuesto y perímetro ya aprobados. Si entrega candidata autorizada, comprobar su selección, adquisición o receta, actualización por el escritor canónico, regeneración y PR. Si termina en negativo, conservar frontera y residual. El piloto no debe producir una adquisición ficticia para "pasar".

### Criterio de aceptación

1. El doctor reconoce el cierre real del 9/sep aunque su rama haya sido retirada.
2. Un cierre de otro día/intento no vuelve verde la corrida evaluada; una lectura inaccesible no se rotula "no corrió".
3. Transporte fallido, push fallido y timeout dejan causa distinguible; no resultan en éxito global por defecto.
4. Una segunda invocación no altera el heartbeat de la que trabaja.
5. La misma fecha y conjunto de filas producen la misma selección; una candidata autorizada de SONDA llega al consumidor previsto, y una no autorizada permanece propuesta.
6. El piloto aparece en "esperando caja" y se ejerce el contrato vigente. Su cierre lleva cita y universo.
7. Una ejecución programada de producción se correlaciona desde Task Scheduler hasta su recibo publicado. Una invocación manual se distingue y no sustituye esa evidencia.
8. La prueba de recuperación de un disparo perdido conserva su alcance parcial hasta observarla o realizar una prueba acotada autorizada. No requiere suspender la máquina de mesa para cerrar los arreglos de código.

### Gate D-14

| Pieza | Defecto real | Materialidad | Costo frente al arreglo manual |
|---|---|---|---|
| T31 / doctor | Falso aviso actual y cierre de otra fecha aceptado en prueba | Impide saber si el sistema funcionó | Reparar el lector común evita revisar ramas/logs a mano cada día |
| Runner | Fallos de red/publicación mal propagados; timeout y heartbeat vulnerables en pruebas | Puede ocultar pérdida de publicación, gastar cuota o inmovilizar trabajo | Cambios locales de shell y pruebas pequeñas, sin infraestructura |
| Handoff / cabecera | Piloto invisible; contrato permite estados que el selector no consume | Trabajo preparado puede no llegar a quien debe ejecutarlo | Alineación del contrato y metadato; selector pequeño solo si compensa |
| Configuración desplegada | Acceso actual no verificado; incidente histórico real del scheduler | Condiciona ejecución sin intervención | Una lectura de CAJA y corrección puntual; no justifica instalar otro monitor |

## 7. Lectura de CAJA lista para ejecutar

Estos comandos consultan; no disparan adquisición ni reinstalan tareas. Claude local puede incorporarlos a P3.

**En Ubuntu/WSL de mesa:**

```bash
python3 /home/pc0/mm-adq/tools/adq_doctor.py --json
```

Hasta corregir H1, interpretar `t_cron` junto al censo consolidado; no usar su falso `CENSO-SIN-CIERRE` para relanzar a ciegas.

**En PowerShell:**

```powershell
$adqTask = Get-ScheduledTask -TaskPath '\ModeladoMexicano\' -TaskName 'AdquiereCron'
$adqInfo = Get-ScheduledTaskInfo -TaskPath '\ModeladoMexicano\' -TaskName 'AdquiereCron'
$adqTask | Select-Object TaskName,TaskPath,State
$adqTask.Actions | Format-List Execute,Arguments,WorkingDirectory
$adqTask.Triggers | Format-List *
$adqTask.Settings | Select-Object StartWhenAvailable,WakeToRun,MultipleInstances,ExecutionTimeLimit
$adqTask.Principal | Select-Object UserId,LogonType,RunLevel
$adqInfo | Select-Object LastRunTime,LastTaskResult,NextRunTime,NumberOfMissedRuns
Get-TimeZone
Get-WinEvent -FilterHashtable @{
    LogName = 'Microsoft-Windows-TaskScheduler/Operational'
    StartTime = (Get-Date).Date
} -ErrorAction Continue |
    Where-Object { $_.Message -like '*\ModeladoMexicano\AdquiereCron*' } |
    Select-Object TimeCreated,Id,Message
```

Si el historial operativo está deshabilitado o no es legible, declararlo; no inferir ausencia de disparo. Correlacionar los eventos disponibles con `2026-09-09T073007-371` y con el log local `forense/adq-log/2026-09-09.log`. La lectura anterior es lo que falta para atribuir el arranque de hoy al scheduler concreto y comprobar que no quedó otro disparador activo.
