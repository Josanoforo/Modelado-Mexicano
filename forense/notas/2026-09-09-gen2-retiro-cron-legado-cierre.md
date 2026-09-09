# ACTO GEN2-RETIRO-CRON-LEGADO — nota de retiro

**Fecha:** 2026-09-09 · **Entorno:** CAJA (Ubuntu/WSL de mesa), Sonnet · **Redactado y ejecutado contra** `origin/main = ffeeca2cd1a9df65f513f1b286b35761c1fcf806`.

**Compuerta:** ninguna.

**Firma de mesa (9/sep/2026, verbatim):** «Retiremoslo, no se por qué lo estamos retirando hasta ahorita, pero vamos a retirarlo.»

---

## 1 · La evidencia que autoriza el retiro

Este acto no re-produce la atribución: la cita, ya sellada por `ACTO GEN2-ADQ-VERIFICACION-CAJA` (`PR #666`, `ADR-440`, 9/sep/2026).

Ese acto midió que el 9/sep dispararon **los dos** disparadores a las 07:30:07, con dos `run_id` distintos en el mismo segundo:

```
[2026-09-09 07:30:07-0600] === adquiere_cron.sh arrancando ... (run_id=2026-09-09T073007-491) ===
[2026-09-09 07:30:07-0600] === adquiere_cron.sh arrancando ... (run_id=2026-09-09T073007-371) ===
[2026-09-09 07:30:07-0600] PARO-LOCK: ... Esta invocación (run_id=...-491) no toca git ni el corpus, termina de inmediato.
[2026-09-09 07:33:59-0600] [ADQ] ... invocado=si motivo=- exit=0 duracion=228s ... run_id=2026-09-09T073007-371
```

Atribución, por dos discriminadores independientes (no lexicales):

1. **`forense/adq-log/cron-stdout.log` sólo lo escribe el redirect del propio crontab** (`30 7 * * 1-5 cd ... >> forense/adq-log/cron-stdout.log 2>&1`); el runner nunca nombra ese archivo (`grep "cron-stdout" tools/adquiere_cron.sh` → 0, control positivo `grep -c "adq-log"` → 3). Ese archivo trae exactamente `run_id=...-491` — **el crontab de WSL fue el perdedor**.
2. **`PARO-LOCK` sale con `exit 3`** (`tools/adquiere_cron.sh:104`). Task Scheduler reportó `LastTaskResult = 0`, no 3 — **la tarea de Windows (`\ModeladoMexicano\AdquiereCron`) fue la que operó**: `run_id ...-371`, 228 s, `exit=0`, huella fusionada en `forense/censo-raiz/2026-09-09.txt`.

El `flock` de instancia única ya contenía el daño de tener dos disparadores vivos (la invocación perdedora no tocó git ni el corpus), pero mantener ambos activos indefinidamente es ruido, no defensa (`tools/windows/GUIA-TAREA-ADQUISICION.md`, sección «Retirar el crontab de WSL»). Con la atribución probada y una corrida de producción ya observada bajo Task Scheduler en solitario como disparador operante, el retiro del respaldo de WSL queda autorizado.

## 2 · `crontab -l` ANTES

```
# tools/adquiere_cron.sh resuelve su propio REPO_DIR por
# $(dirname "${BASH_SOURCE[0]}")/.. -- pero cron NO hereda el PATH
# interactivo del usuario (sin él, `git`, `curl`, `claude`, `python3` no
# se encuentran). Fijar PATH explícito en el propio crontab, no asumir
# que hereda el del shell de login (forense/cron/REGISTRO-CRON-v1_0.md §2).
PATH=/usr/local/bin:/usr/bin:/bin:/home/pc0/.local/bin
30 7 * * 1-5 cd /home/pc0/mm-adq && ./tools/adquiere_cron.sh >> forense/adq-log/cron-stdout.log 2>&1
```

## 3 · Qué se retiró (única línea, verbatim, verificada con diff)

```
30 7 * * 1-5 cd /home/pc0/mm-adq && ./tools/adquiere_cron.sh >> forense/adq-log/cron-stdout.log 2>&1
```

`diff` contra el crontab instalado después confirma una sola línea de diferencia — el bloque de comentario que explica el `PATH=` y la propia línea `PATH=` **no se tocaron**, tal como el encargo lo pide («las demás líneas, si las hay, no se tocan»), aunque el comentario ya no describa una entrada activa.

## 4 · `crontab -l` DESPUÉS

```
# tools/adquiere_cron.sh resuelve su propio REPO_DIR por
# $(dirname "${BASH_SOURCE[0]}")/.. -- pero cron NO hereda el PATH
# interactivo del usuario (sin él, `git`, `curl`, `claude`, `python3` no
# se encuentran). Fijar PATH explícito en el propio crontab, no asumir
# que hereda el del shell de login (forense/cron/REGISTRO-CRON-v1_0.md §2).
PATH=/usr/local/bin:/usr/bin:/bin:/home/pc0/.local/bin
```

Instalado con `crontab <archivo>` sobre el crontab de usuario `pc0`, `exit=0`, verificado de inmediato con `crontab -l`.

## 5 · Disparador único

El scheduler de Windows Task Scheduler (`\ModeladoMexicano\AdquiereCron`, `tools/windows/instala-tarea-adquisicion.ps1`) queda como **único** disparador diario de `tools/adquiere_cron.sh`. El `flock` de instancia única (`tools/adquiere_cron.sh`) sigue en su sitio como defensa de segunda línea; ya no tiene un segundo disparador vivo que evitar.

## 6 · Reservas — lo que este acto no cierra

El paso (3) de `tools/windows/GUIA-TAREA-ADQUISICION.md` («Retirar el crontab de WSL») pide documentar la retirada en `forense/cron/REGISTRO-CRON-v1_0.md`. `forense/cron/` **no está en el perímetro** de este encargo (que declara únicamente: crontab de WSL + una nota + no-corrido si hay reserva + 0-bis + cascada) — la ausencia es deliberada, no una omisión, y escribir ahí sin que el perímetro lo nombre convertiría un cierre correcto en una violación. Esa pieza queda en `## NO-CORRIDO / RESERVAS` de abajo, como sucesora de `NC-0119` (que este mismo acto cierra, porque la pieza que `NC-0119` nombraba — «retirar la línea del crontab legado» — es exactamente la que este acto ejecutó).

**Contador:** no se mueve. Este acto no adquiere, no mide, no sella ninguna cifra del motor — es retiro de un disparador redundante, con su propia evidencia.
