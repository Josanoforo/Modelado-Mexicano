# GEN2-ADQUISICION · cierre verificable y producción

Fecha: 11/sep/2026. Entorno: CAJA Windows/Ubuntu WSL2. PR correctivo:
#719. Worktree: `/home/pc0/mm-gen2-adq-cierre`, rama
`acto/gen2-adquisicion-cierre-verificable`, base inicial
`70c64d9ead92384ece0eaf18cbfb53372bb88a74`.

## Correctivo

- H2 quedó cerrado por un esquema con resultados por objeto y el validador
  semántico `adq_doctor.py --valida-resultado`: exige igualdad con la selección
  calculada, un desenlace por elegido, evidencia local, archivo/manifiesto
  pertinente para adquisiciones, resultados verificables para intentos y
  `refs/heads/*` con SHA exacto comprobado en el remoto.
- Resultado del trabajo, publicación de objetos/intentos y publicación del
  recibo son estados distintos. Un push fallido conserva resultados parciales
  y hace fallar el cierre; el recibo del wrapper no lo sustituye.
- H3 quedó cerrado desde el launcher: toma el lock, crea `run_id`/heartbeat y
  trap antes de fetch/checkout, registra fase/revisión/motivo/timestamps y
  preserva el código original. El mismo `run_id` e inicio pasan al runner.
- Cero elegidos produce resultado determinista `cola_vacia`, `invocado=no`,
  sin `codex exec` ni Claude. Error del selector produce `PARO-SELECCION`.

Casos dirigidos: 69 sin fallos (7 del acto, 8 doctor, 7 configuración, 27
cableado y 20 contrato). Línea base: verde, cero fallos nuevos; conserva 3
fallos heredados T06/T08.

## Puesta en marcha real

La cola real produjo 0 elegidos y 140 excluidos con causa. La misma tarea
`\ModeladoMexicano\AdquiereCron` recibió un trigger temporal `TimeTrigger`.

La primera activación de las 17:06 conservó un error de operador: se transcribió
un SHA largo incorrecto (`f2a2b754442...`) y el launcher anterior salió 5 en
`PARO-REVISION`, antes de trabajo. No invocó LLM ni alteró el staging. Se
reinstaló inmediatamente la tarea, retirando ese trigger, con el SHA publicado
correcto `f2a2b754c2c2027bdd0c868e913b9eefc3aead69`.

La activación válida quedó correlacionada así:

| Cierre | Evidencia |
|---|---|
| Windows | 17:09:56; evento 107/RecordId 693 (condición de trigger de hora), 100/695 usuario `FF-5563\PC0`, 200/696 `wsl.exe`, 201/697 salida 0 y 102/698 cierre; ActivityId `6f37f84c-3528-4aa7-b8d2-0cd9974d85bb`. |
| Launcher/runner | `run_id=2026-09-11T170957-1772683`; inicio 17:09:57, fin 17:10:23; launcher y runner resolvieron `f2a2b754c2c2027bdd0c868e913b9eefc3aead69`; `runner_version=adq-codex-2`. |
| Selección | Artefacto local `forense/adq-log/2026-09-11T170957-1772683-seleccion.json`: corte 2026-09-11, máximo 5, 0 elegidos, 140 excluidos. |
| Trabajo | `resultado=cola_vacia`, `resultado_trabajo=cola_vacia`, `invocado=no`, `publicacion_trabajo=no_aplica`; no se creó artefacto/evento de Codex ni se invocó Claude. Cola vacía no significa ausencia de necesidades: son 140 exclusiones según el contrato vigente. |
| Publicación | Recibo `[ADQ-SELECCION]` + `[ADQ-RESULTADO]` + `[ADQ]` publicado en `censo/2026-09-11`, commit `b0ae9b0cc2e5ecbc954da40080a8138e45e90fc6`, PR #721; `publicacion=OK`. |
| Heartbeat | `TERMINADO`, fase `FIN`, motivo `COLA-VACIA`, salida 0, SHA/run_id/timestamps iguales a la cadena anterior. |

## Estado final

El trigger temporal fue retirado mediante el instalador idempotente. La tarea
quedó `Ready`, principal `PC0`, `Interactive`, `Limited`, acción WSL
Ubuntu/`pc0`, un trigger semanal lunes-viernes 07:30, siguiente
14/sep/2026 07:30, `StartWhenAvailable`, `IgnoreNew` y Operational habilitado.
La exportación previa está en
`%TEMP%\ModeladoMexicano-AdquiereCron-pre719-20260911-170352.xml`, SHA-256
`7c9d26ea5e2ef85b939ce36d683ee98fea2e2ec88459e8c64d568774cc2569cc`.

El clon `/home/pc0/mm-adq` quedó detached en la revisión desplegada, sin lock ni
proceso de adquisición. `data/manifiesto-staging.yaml` fue restituido desde el
stash preexistente no consumido y conserva exactamente su hash previo
`c72508bc0fd29a83348730d6cdc10087b3d281e7cb2b08f61080a4e405be6597`.

No se abre pendiente gemelo. NC-0114 no se reabre; la migración a Codex sigue
cerrada. NC-0120 conserva exclusivamente observar una recuperación natural
futura de `StartWhenAvailable`; esta puesta en marcha normal no la acredita.
