# Cierre · GEN2-CRON-DEMANDA-A-DATO-Y-PRODUCCION

Fecha de corte: 2026-09-11 (America/Mexico_City).

## Resultado operativo

Quedó cableado un solo recorrido autoritativo:

`necesidad → tools/adq_residual.py → registro canónico → vista derivada → tools/adq_doctor.py → tools/adquiere_cron.sh → recibo diario`.

`adq_residual.py` usa `tools/curador_registro/tsv_crudo.py::upsert_fila`, conserva el origen histórico al actualizar una fila y no crea una segunda cola. El selector distingue una cola ejecutable vacía de una demanda residual vacía: el cierre informa por separado residuales cubiertos, accionables, sujetos a acceso, sin vía, para reintento y sujetos a decisión.

## Residuales materializados

| Objeto residual | Estado al corte | Consumidor | Barrera / siguiente acción |
|---|---|---|---|
| `ENNVIH_DIN_M_01_DISENO_INFERENCIAL` | `SOLICITUD-PREPARADA` | DIN-M-01; S6-C1/C3/C4; NC-0156 | Titular envía `03-ENNVIH-DIN-S6.md` y aporta acuse. |
| `MPS2012_35024_0001_DATA_DTA` | `SOLICITUD-PREPARADA` | N26; N27; NC-0151 | Identidad/afiliación y RDUA de ICPSR; verificar bytes recibidos. |
| `OECD_TRUST_PUM_2021_2023_2025` | `SOLICITUD-PREPARADA` | N30; NC-0151 | Identidad/firma y envío del borrador técnico; verificar respuesta. |
| `ENJUVE_MICRODATOS_2000_2005_2010` | `SOLICITUD-PREPARADA` | NC-0151; reactivos por ola | Presentar por PNT y aportar folio; verificar cada ola por separado. |
| `ENVIPE_ROSTER_UPM_O_SERVICIO_VARIANZA` | `SOLICITUD-PREPARADA` | CIV-M-10; CIV-M-12; CIV-M-13; NC-0159 | Solicitud a INEGI y folio; congelar especificación antes de recalcular. No bloquea los puntos descriptivos ya validados. |
| `ENCIG_TASA_NACIONAL_PAGO_INFORMAL_POR_CANAL` | `SOLICITUD-PREPARADA` | NC-0111; NC-0153; 07R | Solicitud a INEGI y folio; verificar llave, unidad, negativos y diseño. |
| `ENSAFI_TANDAS_REPUTACION_INCUMPLIMIENTO` | `NO-ENCONTRADO` | R8.2; N29; NC-0037 | Sin instrumento nuevo: reabrir sólo ante candidato concreto o respuesta humana de TandaMas. |

Al corte: 7 residuales, 0 cubiertos, 0 accionables sin intervención, 6 pendientes de acceso y 1 sin vía actual. Por tanto, `elegidos=[]` es un resultado correcto de autorización, no ausencia de demanda. No se fabricó ningún dato ni se degradó un padre parcial para forzar trabajo.

## Ejecución de producción observada

- Tarea: `\ModeladoMexicano\AdquiereCron`.
- Identidad: `PC0`; `Interactive`; privilegios `Limited`.
- Calendario: lunes a viernes, 07:30; `StartWhenAvailable=true`; `MultipleInstances=IgnoreNew`.
- Recorrido probado desde Task Scheduler: `wsl.exe → /home/pc0/mm-adq/tools/adquiere_launcher.sh → tools/adquiere_cron.sh`.
- Revisión ejercida: `b8d2d5e27c6a439072a64694200a3adb7c2fa363`.
- `run_id`: `2026-09-11T180904-1896688`; inicio 18:09:04; fin 18:09:39; `runner_version=adq-codex-3`; salida 0; publicación `OK`.
- Instancia de Windows: `{36768222-57bd-4137-9980-37ec45add51a}`. Eventos Operational 325/110/129/100/200/201/102; el evento 201 acredita que `wsl.exe` devolvió código 0 y el 102 acredita fin correcto.
- Resultado compuesto: cola ejecutable vacía, trabajo no invocado, recibo publicado correctamente. No se gastó una sesión de agente en una cola sin objeto autorizado.
- Publicación diaria: PR `#727`, rama `censo/2026-09-11`, recibo `5ba14eb4511fa93804caf529f611d929f9f91e44`; verificación remota verde.
- El cambio ajeno preexistente en `data/manifiesto-staging.yaml` se restituyó byte por byte tras el ensayo: SHA-256 `c72508bc0fd29a83348730d6cdc10087b3d281e7cb2b08f61080a4e405be6597`.

La tarea quedó de nuevo en estado `Ready`, con su acción automática restaurada (`ADQ_DISPARADOR=windows-task-scheduler`) y próxima ejecución el 2026-09-14 a las 07:30 -06:00. Por usar `Interactive`, requiere que exista una sesión de Windows de `PC0` iniciada.

## Validación

- `tests/test_adq_residuales.py`: 3 casos, 0 fallos.
- `tests/test_adq_contrato_fix.py`: 20 casos, 0 fallos.
- `tests/test_adq_cierre_verificable.py`: 7 casos, 0 fallos.
- `tests/test_adq_cableado.py`: 27 casos, 0 fallos.
- `tests/check.py --baseline`: línea base verde; sólo permanecen los 3 fallos históricos de T06/T08.
- `bash -n`, `py_compile` y `git diff --check`: correctos.

## Cierre honesto

El CRON está operativo para cualquier objeto que satisfaga el contrato de autorización y publicará evidencia aun cuando no haya elegibles. La adquisición material de estos siete residuales no está completa: seis requieren identidad, firma, folio o respuesta externa y uno carece de una vía nueva comprobada. Esas acciones humanas son la única barrera restante; no hay una falla de cableado que pueda resolverlas automáticamente.
