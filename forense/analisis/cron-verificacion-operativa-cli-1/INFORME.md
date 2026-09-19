# Verificación operativa del cron de caja

Fecha: 2026-09-19, America/Mexico_City. Este acto es verificación y
reparación operativa; no cuenta como medición científica.

## Dictamen

**FUNCIONANDO-PARCIAL** al corte 2026-09-19T16:31-06:00. El Task Scheduler,
la propagación de salida, el lock, el despliegue, la derivación y la
comprobación determinista reparada quedaron acreditados por un trigger
horario natural posterior al despliegue. La cadena completa no se declara
sana: esa activación llegó al ejecutor, produjo trabajo y publicó, pero el
cierre fue correctamente rechazado con `exit=65` por un resultado estructurado
inválido. `t_cron` queda `RESULTADO-INVALIDO`, sin reserva activa.

## Estado de trabajo

- Worktree: `/home/pc0/mm-gen2-cron-verificacion-operativa-cli-1`.
- Rama: `codex/gen2-cron-verificacion-operativa-cli-1`.
- Base: `8e455bd6a3870566d6776fef19834c4da16d2fa9`.
- SHA correctivo publicado y desplegado:
  `6ab4cbe78ca31aa70eb93c490a1d43af01219736`.
- Clon productivo: HEAD desprendido en ese SHA; conserva, sin apropiación,
  `data/manifiesto-staging.yaml` modificado y
  `forense/cron/RESPALDO-TAREA-20260915T2245.xml` no versionado.

## Instalación

La definición instalada coincide con `data/adq-config.yaml` y el instalador:
diaria a las 07:30 en `America/Mexico_City`, repetición cada 60 minutos y
recuperación al iniciar sesión. Usa principal `PC0`, `Interactive`, nivel
`Limited`; PowerShell oculto/no interactivo espera `wsl.exe` y propaga su
código. `StartWhenAvailable=true`, `MultipleInstances=IgnoreNew` y el lock
`flock` permanecen. No hay crontab ejecutable duplicado.

El XML anterior se preservó antes de reinstalar. Se usó exclusivamente
`tools/windows/instala-tarea-adquisicion.ps1`, fijando el SHA correctivo ya
publicado. No se cambiaron horario, modelo, principal, presupuesto ni
política de instancia.

## Causa y corrección

El disparador sí arrancaba; el defecto estaba después de una derivación
exitosa y antes del despacho. `tools/adq_investigacion.py` trataba todo
`proxima_revision` como fecha ISO. El resultado válido de `NC-0244` declaró
una barrera `EVENTO: firma de mesa...`, y desde el 18/sep cada comprobación
terminó con `ValueError`.

La corrección reconoce el contrato de revisión por evento en los dos puntos
que lo consumen: selección versionada y checkpoint runtime. La necesidad queda
en espera hasta una señal estructurada o cambio material; no se transforma en
fecha ficticia, no se elimina y no se cambia la política científica.

La activación natural de las 16:00 confirma que la excepción desapareció:
`NC-0244` permaneció excluida por evento y la selección continuó con
`DEM-AHORRO-STOCK-DURACION-01`, `NC-0202` y `NC-0253`.

## Ambos tramos

### Derivación

La firma `ultima-exitosa.json` se conservó. La prueba manual sobre el SHA
correctivo, con `DERIVA_PUBLICAR=0` y `MM_TRAMO=derivacion`, cerró
`NADA-QUE-HACER-YA-COMPLETADO`, `exit=0`; no se presenta como publicación
nueva. Después, el trigger natural de las 16:00 cargó exactamente
`6ab4cbe78ca31aa70eb93c490a1d43af01219736`; su tramo de derivación
`2026-09-19T160003-63890` terminó en 927 s con `exit=0` y
`CAMBIOS-DIFERIDOS-PR-DIARIO-YA-FUSIONADO`.

### Adquisición

El último trabajo real completamente acreditado es
`2026-09-18T083018-433`: selección de objetos vacía, tres investigaciones
seleccionadas/iniciadas/validadas, salida final y handoff iguales, validación
exitosa, trabajo publicado, cero objetos, cero bytes y cero reducción de
brecha. Es éxito operativo con evidencia nueva, sin avance sustantivo.

La activación natural `2026-09-19T160001-63807` sí ejecutó trabajo real:
tres investigaciones y un objeto consumieron presupuesto, el commit de trabajo
`247eee150e2968dbaa317f8ad1268350dea3665d` se publicó en el PR #885 y el
censo reutilizó el PR #884. Sin embargo, ambos candidatos de cierre, iguales
entre sí, eran inválidos. El resultado textual del intento UCLA no aparecía
verbatim en sus rutas de evidencia y declaró `intentos_documentados` cuando el
trabajo calculado era `descubrimiento_documentado`. El validador falló cerrado,
como corresponde; no se reconstruyó ni corrigió ese handoff.

El trabajo publicado además verificó una incompatibilidad anterior: cuatro
entradas vigentes de `data/manifiesto.yaml` usan `estado_reserva`, pero
`tests/manifiesto.py` no la incluye en `CAMPOS_CONOCIDOS`; por ello rechazó
registrar el PDF UCLA ya descargado. Ese defecto no pertenece al
launcher/runner/doctor/handoff/instalador permitido por este encargo y se deja
como bloqueo preciso, sin repetir red ni modificar manifiesto o inventarios.

El SHA efectivo conserva el arreglo del 17/sep que acepta evidencia bajo el
`data/raw` enlazado al corpus compartido y las regresiones de handoff: dos
candidatos válidos iguales cierran una vez; dos válidos distintos fallan
cerrado con conflicto. No se reconstruyó ningún resultado ni se reescribió
un `exit=65` histórico. `gh auth status` confirma sesión activa sin exponer el
token. El presupuesto del 19 quedó consumido en `3/1/524 s`, con
`0/4/3376 s` devuelto y ninguna reserva activa.

## Utilidad y propuesta para recibo Claude

`NC-0244` ya no es una búsqueda pública: la evidencia existente identifica
dos canales para `RES-0047/RES-0049` y la frontera restante es una firma de
mesa sobre el pin canónico, conservando `0.458657` y `0.626870`. Propuesta:
mantener la barrera por evento y, cuando llegue la firma, actualizar el
escritor canónico y re-derivar; no enviarla de nuevo a adquisición por fecha.

`DEM-AHORRO-STOCK-DURACION-01` acumula seis ciclos sin mejora: no apareció un
instrumento probabilístico que mida, para el mismo stock, ausencia/tenencia y
meses o días cubiertos. Frontera restante: catálogos de universidades
estatales fuera de Colmex/UNAM/IIEG y archivos históricos no indexados de
CNBV/CONDUSEF. Propuesta a mesa: elegir entre mantener el bloqueo y una
búsqueda dirigida nueva, autorizar el relabel acotado ya planteado en #772, o
aprobar un proxy nuevo con alcance explícito. Este acto no elige.

## Pruebas

- `tests/test_adq_handoff_resultado.py`: 13 pruebas, 0 fallos; incluye symlink
  del corpus y conflicto entre dos candidatos válidos distintos.
- `tests/test_adq_cierre_verificable.py`: 13 casos, 0 fallos.
- Regresión nueva de revisión por evento: selección y checkpoint, 0 fallos.
- `python3 tools/adq_investigacion.py --comprueba-despacho` sobre el SHA
  desplegado: exit 0 y JSON válido; sin modelo ni descarga.
- Trigger natural de las 16:00: Event 107/100/200 al inicio y 201/102 al
  cierre bajo ActivityId `{2cc74291-aaf4-469c-bcf9-ec8e55cf1f7a}`; Windows
  propagó `65` como `2147942465`. Tarea `Ready`, siguiente 17:00, lock inactivo.
- `python3 tests/test_adq_descubrimiento.py`: una aserción heredada falla
  porque espera el mapa de necesidades de un corte anterior; la regresión
  nueva pasa aislada y el fallo no corresponde a esta causa.

## Cierre y receta pendiente

No repetir la descarga UCLA. En un acto con autoridad sobre el subsistema de
manifiesto: reconciliar el censo de claves de `tests/manifiesto.py` con
`estado_reserva`, ejecutar `--registra` sobre el PDF existente, verificar el
ID y actualizar la fila residual por la vía canónica. Después, permitir que
una activación nueva produzca su propio cierre; no editar el `exit=65` del
19/sep.

La trazabilidad compacta de activaciones está en `activaciones.tsv`; los
extractos sin secretos están en `extractos-saneados.md`.
