# GEN2-ADQ-CODEX-PRODUCCION · cierre

**Estado: INSTALADO Y EJECUTADO CON CODEX.** Fecha: 11/sep/2026. Entorno:
CAJA Windows/Ubuntu WSL2. PR de implementación: #718. Recibo operativo: PR
#716, commit remoto `8c6ca3382b8ad3d916923bfe0eca9076946b51eb`.

## Cadena aceptada

| Resultado | Evidencia |
|---|---|
| Codex principal | `/home/pc0/.local/bin/codex` → release standalone 0.154.0; `codex-cli 0.154.0`; `Logged in using ChatGPT`; configuración del runner `ejecutor=codex`, modelo explícito/efectivo observable `gpt-5.6-sol`. La configuración general del usuario no se modificó. |
| Despliegue persistente | `/home/pc0/mm-adq` quedó en `1e880f05faa16c7cee1ca86aea322188336d279f`. La tarea fija ese SHA; `tools/adquiere_launcher.sh` toma el lock antes de resolverlo y sólo transita a `origin/main` cuando el SHA sea ancestro de main. Rollback: exportaciones de tarea en `%TEMP%` y revisión anterior `04a2227f506c062803e24cf5305421ffe5b68fd4`. |
| Eventos habilitados | Script acotado `tools/windows/habilita-operational-adquisicion.ps1`, UAC bajo `FF-5563\\PC0`; evidencia `%TEMP%\\ModeladoMexicano-Operational-20260911-100129.json`; `IsEnabled=True`. |
| Adquisición real | Trigger `Once` de hora, no ejecución manual: Windows inicia 10:26:45; WSL `run_id=2026-09-11T102646-1498932`; máximo 5; 0 elegibles y 140 excluidas con causa; Codex devuelve `cola_vacia`; salida 0. Cola vacía acreditada es el resultado sustantivo real y no se fabricó una fila. |
| Correlación Windows/WSL | `RecordId 77`/evento 107 identifica condición de trigger de hora; 79/100 usuario; 80/200 `wsl.exe`; 81/201 y 82/102 finalizan correctamente. `ActivityId 53e8f092-5db2-4510-a807-d1b0d13207a8`. Inicio WSL 10:26:46, fin 10:29:22. |
| Resultado y publicación separados | Hijo: `resultado_sustantivo=cola_vacia`, sin commit/PR propio porque no hubo filas. Runner: publicación `OK`, recibo remoto `8c6ca338` en `censo/2026-09-11`/PR #716. Heartbeat final `TERMINADO/FIN`, salida 0. |
| Tarea final | `\\ModeladoMexicano\\AdquiereCron`, `Ready`, `PC0`, `Interactive`, `Limited`, Ubuntu/`pc0`, `StartWhenAvailable`, `IgnoreNew`, PT2H. Un solo trigger semanal lunes-viernes 07:30; siguiente `2026-09-14T07:30:00-06:00`; trigger temporal retirado; Operational sigue activo. Exportación final `%TEMP%\\ModeladoMexicano-AdquiereCron-final-20260911-110415.xml`, SHA-256 `7c9d26ea5e2ef85b939ce36d683ee98fea2e2ec88459e8c64d568774cc2569cc`. |
| Trabajo ajeno | `data/manifiesto-staging.yaml` observado antes con SHA-256 `c72508bc0fd29a83348730d6cdc10087b3d281e7cb2b08f61080a4e405be6597`, 392 inserciones/1 borrado. El censo lo regeneró durante la corrida y al final se restituyó exactamente desde el objeto `stash@{0}` ya creado por 07R; mismo hash y diff, stash conservado. Corpus y otros worktrees no se borraron ni detuvieron. |

## Intentonas y consumo

La primera activación horaria, `run_id=2026-09-11T101801-1489048`, alcanzó
`codex exec` pero fue rechazada por `invalid_json_schema` antes de trabajo
sustantivo; terminó 1 y publicó el fallo. Se corrigieron los tipos del esquema
en `1e880f05…` y se repitió sólo el tramo necesario. La activación aceptada
duró 151 s. El evento final de Codex reporta 162,979 tokens de entrada,
117,888 cacheados, 6,193 de salida y 303 de razonamiento. `stderr` quedó vacío.
Ninguna intentona invocó Claude.

## Estado de NC

- `NC-0114` cierra: existe recorrido programado de producción, tipo exacto
  `TimeTrigger`, evento/ActivityId, run_id, resultado y recibo correlacionados.
- `NC-0120` conserva sólo observar una recuperación real futura de
  `StartWhenAvailable`. Operational ya está habilitado; una corrida normal no
  prueba recuperación y este residual no bloquea Codex.
- `NC-0133` y la receta CompraNet permanecen en su cierre acreditado por #711;
  no se repitieron.

## NO-CORRIDO / RESERVAS

Sólo `NC-0120`: observar una recuperación real futura si ocurre naturalmente.
No reiniciar, suspender ni mover el reloj para fabricarla. No queda reserva de
instalación, migración, autenticación, evento o corrida Codex.
