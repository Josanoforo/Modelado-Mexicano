# GEN2-DERIVADOS-CORRECTIVO-Y-DESPLIEGUE · cierre

Fecha: 16/sep/2026. PR correctivo: #819. Activaciones de validación: **manuales
mediante el launcher compartido** y limitadas a `MM_TRAMO=derivacion`.

## Resultado

La tarea existente `\ModeladoMexicano\AdquiereCron` se actualizó sin crear
otra tarea. Conservó `PC0`/`Interactive`/`Limited`, tres triggers y estado
`Ready`. Su acción quedó fijada mediante
`ADQ_DEPLOY_REVISION=3f759e5e2feee0d5b42892b88bb19b2b0b8542e6` y sigue
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
| universo | OK; hash `5a3526bd…`; no material | `universo-2026-09-16-r02.json` | incluida en #819 tras la comprobación controlada |
| tablero | OK | bloque derivado actualizado | incluido en #819 |
| registro `--verifica` + `status` | ambos exit 0; el diff en seco es esperado | cero escritura en vistas | no aplica |
| repetición | exit 0 en 1 s; `NADA-QUE-HACER-YA-COMPLETADO` | cero snapshot, commit o PR adicional | ninguna |

La corrida completa fue `run_id=2026-09-16T101948-508120`, duró 543 s y
cerró `COMPROBACION-SIN-PUBLICAR`; la repetición fue
`run_id=2026-09-16T102919-516780`. Ninguna entró a recuperación, selección,
descarga, ledger de adquisición ni ejecutor de lenguaje.

`DERIVA_PUBLICAR=0` evitó que la comprobación abriera un segundo PR diario.
Después, ya sobre el mismo `origin/main`, se invocaron las funciones reales
`deriva_universo` y `deriva_tablero` del runner y sus dos salidas se añadieron
al único PR correctivo #819. Una segunda materialización devolvió
`SIN_CAMBIOS` para el resumen fechado, no creó `r03` y dejó el tablero sin
cambios.

El trigger real de las 11:00 ocurrió durante la transición intermedia a
`60629d6…`: la tarea ya citaba el SHA, pero el clon que sólo seguía `main`
todavía no tenía su objeto, por lo que propagó exit 5 (`revision-autorizada-no-existe`)
sin entrar a derivación ni adquisición. Ese caso medido originó el último
correctivo: desde `3f759e5…`, si el commit autorizado falta localmente, el
launcher lo obtiene de `origin` antes de validarlo y hacer checkout. Una
regresión reproduce el caso con un clon `--single-branch`. Tras cargar la
revisión final, la validación manual `run_id=2026-09-16T111733-532096` terminó
exit 0 en 1 s, con `NADA-QUE-HACER-YA-COMPLETADO` y SHA cargado `3f759e5…`.

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

- `python3 tests/test_deriva_correctivo.py`: 7 casos, OK.
- `python3 tests/test_adq_config.py`: 7 casos, OK.
- `python3 tests/test_adq_doctor.py`: 9 casos, OK.
- `python3 tests/test_adq_cableado.py`: 34 casos, OK.
- `python3 tests/test_adq_cierre_verificable.py`: 13 casos, OK.
- `python3 tests/check.py --baseline`: VERDE contra baseline, cero entradas nuevas.

Estado final distinguido: revisión ejecutable cargada = `3f759e5…`; revisión
final del PR = la que encabece #819 tras esta nota; integrada en `main` = no.
Después del merge no hay que editar la tarea: el launcher reconoce que la
revisión fijada ya es ancestro de `origin/main` y retoma éste automáticamente.
