# ENCARGO · ACTO GEN2-RETIRO-CRON-LEGADO

Recibido en mesa 9/sep/2026. Texto verbatim del lanzamiento:

> ENCARGO · ACTO GEN2-RETIRO-CRON-LEGADO · MICRO · CAJA, Sonnet · COMPUERTA: ninguna · FIRMA DE MESA, 9/sep/2026, verbatim: «Retiremoslo, no se por qué lo estamos retirando hasta ahorita, pero vamos a retirarlo.» — única pieza: pega crontab -l completo ANTES, retira únicamente la entrada de adquiere_cron.sh (las demás líneas, si las hay, no se tocan), pega crontab -l DESPUÉS, y asienta en forense/notas/ la nota de retiro citando la atribución del acto VERIFICACION-CAJA (los dos run_id del mismo segundo y el PARO-LOCK que nos salvó) como la evidencia que lo autoriza. El scheduler de Windows queda como disparador único. PERÍMETRO: crontab de WSL + una nota + no-corrido si hay reserva + 0-bis + cascada. CONTADOR: no, y se dice.

## NO-CORRIDO / RESERVAS

| NC | Qué no se corrió | Razón | Impacto | Sucesor |
|---|---|---|---|---|
| `NC-0133` | Documentar la retirada del crontab legado en `forense/cron/REGISTRO-CRON-v1_0.md` (paso 3 de `tools/windows/GUIA-TAREA-ADQUISICION.md`) | `FUERA-DE-PERÍMETRO` — el encargo declara únicamente crontab de WSL + una nota + no-corrido + 0-bis + cascada; `forense/cron/` no está nombrado | El paso (3) de la GUÍA queda sin su registro canónico en ese archivo específico. La retirada SÍ queda documentada, con antes/después y atribución citada, en `forense/notas/2026-09-09-gen2-retiro-cron-legado-cierre.md`. Ningún contador de GEN2 se mueve por esto | `acto con forense/cron/ en su perímetro` — huérfano heredado de `NC-0119`, que este mismo acto cierra por su pieza sustantiva (retirar la línea) |

`NC-0119` (`GEN2-ADQ-VERIFICACION-CAJA`) queda **CERRADA** por este acto: la pieza que nombraba — «retirar la línea del crontab legado de WSL» — es exactamente la ejecutada aquí, con evidencia de atribución citada (§1 de la nota de cierre).

**Contador:** no se movió. Retiro de disparador redundante; ninguna cifra del motor cambia.

## CONSUMIDO

`ACTO GEN2-RETIRO-CRON-LEGADO` cierra con `PR #668` (`ADR-442`), rama `acto/gen2-retiro-cron-legado`, base y ejecución `origin/main = ffeeca2`.
