# GEN2-DERIVADOS-CORRECTIVO-Y-DESPLIEGUE · cierre

Fecha: 16/sep/2026. PR correctivo: #819. Activación: **manual mediante el
launcher compartido**, no atribuida a un trigger de Task Scheduler.

## Resultado

La tarea existente `\ModeladoMexicano\AdquiereCron` se actualizó sin crear
otra tarea. Conservó `PC0`/`Interactive`/`Limited`, tres triggers, estado
`Ready` y siguiente activación 11:00. Su acción quedó fijada mediante
`ADQ_DEPLOY_REVISION=0fb94cbac6e0b3f8455404ddf5b30d859b6b590c` y sigue
llamando `/home/pc0/mm-adq/tools/adquiere_launcher.sh`. El clon operativo
cargó ese SHA bajo el lock de adquisición; el manifiesto modificado y el XML
sin seguimiento que ya existían permanecieron intactos.

La primera activación controlada detectó y propagó un bloqueo real: durante el
acto `origin/main` avanzó a `1353616309dde6cd976a7fefe4305d5e4b6c163a` y la
revisión pendiente todavía no lo contenía. Se corrigió el runner para combinar
en el worktree aislado rama diaria (si existe), `origin/main` vigente y revisión
desplegada. La repetición corregida derivó sobre el SHA efectivo
`f0a9fba80473882a77e901a23674dafcfe6255da`.

| derivación | resultado real en CAJA | cambio observado | publicación |
|---|---|---|---|
| suite `tests/check.py --baseline` | VERDE; 3 FAIL y 4346 WARN heredados, cero nuevos | ninguno | no aplica |
| universo | OK; hash `5a3526bd…`; no material | resumen local `universo-2026-09-16-r02.json` | suprimida por `DERIVA_PUBLICAR=0` |
| tablero | OK | bloque derivado cambió; junto con universo: 2 archivos, 52 inserciones y 3 eliminaciones | suprimida |
| registro `--verifica` + `status` | ambos exit 0; el diff en seco es esperado | cero escritura en vistas | no aplica |
| repetición | exit 0 en 1 s; `NADA-QUE-HACER-YA-COMPLETADO` | cero snapshot, commit o PR adicional | ninguna |

La corrida completa fue `run_id=2026-09-16T101948-508120`, duró 543 s y
cerró `COMPROBACION-SIN-PUBLICAR`; la repetición fue
`run_id=2026-09-16T102919-516780`. Ninguna entró a recuperación, selección,
descarga, ledger de adquisición ni ejecutor de lenguaje.

## Universo vigente

| cifra | valor | alcance |
|---|---:|---|
| declarados | 38 364 | cota superior conservadora; no es denominador puntual mientras haya candidatos de reconciliación |
| adquiridos | 1 274 | identidades de contenido local verificadas por SHA-256 |
| inspeccionados | 549 | intersección por SHA-256 del universo vigente con los ledgers T0 y barrido2 terminal |

No se publica porcentaje de inspección: 38 364 no es un denominador puntual y
presencia local no equivale a inspección. T0, sellos y ledgers previos quedaron
intactos.

## Comprobaciones

- `python3 tests/test_deriva_correctivo.py`: 5 casos, OK.
- `python3 tests/test_adq_config.py`: 7 casos, OK.
- `python3 tests/test_adq_doctor.py`: 9 casos, OK.
- `python3 tests/test_adq_cableado.py`: 34 casos, OK.
- `python3 tests/test_adq_cierre_verificable.py`: 13 casos, OK.
- `python3 tests/check.py --baseline`: VERDE contra baseline, cero entradas nuevas.

Estado final distinguido: revisión del proceso cargada = `0fb94cb…`; revisión
final del PR = la que encabece #819 tras esta nota; integrada en `main` = no.
Después del merge no hay que editar la tarea: el launcher reconoce que la
revisión fijada ya es ancestro de `origin/main` y retoma éste automáticamente.
