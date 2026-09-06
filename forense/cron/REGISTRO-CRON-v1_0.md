# Registro canónico del cron de adquisición · v1.0

`ACTO MAESTRA38-CRON-2 · REGISTRO-Y-HUELLA` (dirección/Fable, 6/sep/2026,
contra `origin/main = ef9ba36` + ramas `censo/2026-09-06` (`PR #556`) y
`acto/maestra38-cron-diagnostico-clean` (`PR #557`), ambas sin fusionar al
momento de escribir esto).

Nota de origen: este documento traslada al repo las secciones §1-§5 del
encargo de dirección del mismo nombre. El texto de dirección se recibió
resumido por encabezados dentro de esta sesión, no pegado íntegro
carácter por carácter — donde el resumen no bastaba para reconstruir una
cifra exacta, este documento cita en su lugar la fuente verificable del
propio repo (`tools/adquiere_cron.sh`, `forense/agente-adquisicion-v1_0.md`,
`PR #557`) y lo declara así en vez de inventar la redacción original.

## §1 · Identidad del cron

| campo | valor |
|---|---|
| script | `tools/adquiere_cron.sh` |
| caja | `mm-adq` (Ubuntu/WSL de mesa — fijada por firma `DC-a`, `ACTO MAESTRA34-N7`: "cloud claude code no tiene acceso a hacer esas revisiones") |
| horario | lunes a viernes, 07:30 hora de mesa (`CST`, UTC-6) |
| usuario del crontab | el de mesa en `mm-adq` (no root) |
| repo que opera | el clon de trabajo de mesa en `mm-adq`, rama `main` |
| log | `forense/adq-log/<AAAA-MM-DD>.log` (por corrida) + `forense/adq-log/cron-stdout.log` (stdout/stderr crudo del propio crontab, apéndice) |
| huella mínima esperada por corrida | **tres commits** en `censo/<AAAA-MM-DD>` (ACTO MAESTRA38-CRON-3, `ADR-353`): `[CENSO] <fecha>` (paso 2.5), `[ADQ-PDN] <fecha>` (paso 2.6 — el re-escaneo si cae en ventana día 1-3, o la línea `fuera de ventana` si no) y `[ADQ] <fecha> <HH:MM>: invocado=<si\|no> motivo=<-\|PARO-RAIZ\|PARO-RED\|PARO-PROMPT\|PARO-CORPUS> exit=<código\|-> duracion=<s> commits_nuevos=<k> ramas_nuevas=<j> archivos_modificados=<m>` (D-b) — medida contra el estado real del clon, nunca una constante; se escribe siempre, incluso `invocado=no` |
| commit del censo | `[CENSO] <AAAA-MM-DD>`, rama `censo/<AAAA-MM-DD>`, PR (main protegida, check `check` requerido) |
| runbook | `forense/agente-adquisicion-v1_0.md` §1 (bloque ```text``` que el script extrae para `claude -p`) |
| modelo que lo declara | `D-13` (`canon/gobernanza-v1_15.md`, `ADR-281`, `ACTO MAESTRA34-N7 · SKILLS-COLA-Y-ADQ`) |
| diagnóstico previo | `PR #557` (`ACTO MAESTRA38-CRON · DIAGNOSTICO-Y-ARREGLO`) — cero código tocado, las cuatro lecturas pre-declaradas del encargo anterior no se cumplieron: la línea de crontab ya era correcta, el estado sucio del log del 5/sep ya estaba resuelto por `PR #546`, el 5/sep/2026 fue **sábado** (fuera de ventana `1-5`, no defecto), y las líneas `PARO-RAIZ` venían de un sandbox de Claude Code que entonces bloqueaba `/mnt/c` |

## §2 · Línea de crontab definitiva

```cron
# tools/adquiere_cron.sh resuelve su propio REPO_DIR por
# $(dirname "${BASH_SOURCE[0]}")/.. -- pero cron NO hereda el PATH
# interactivo del usuario (sin él, `git`, `curl`, `claude`, `python3` no
# se encuentran). Fijar PATH explícito en el propio crontab, no asumir
# que hereda el del shell de login:
PATH=/usr/local/bin:/usr/bin:/bin:/home/pc0/.local/bin
# minuto hora día-mes mes día-semana   comando
30   7    *        *   1-5   cd /ruta/al/clon && ./tools/adquiere_cron.sh >> forense/adq-log/cron-stdout.log 2>&1
```

`/ruta/al/clon` es el clon real de mesa en `mm-adq` — se sustituye al
instalar (`crontab -e`), no se deja literal. `1-5` = lunes a viernes;
domingo=0/7 y sábado=6 quedan fuera a propósito (mismo criterio que T-CRON
§4 usa para calcular "el último día hábil").

## §3 · Calendario de qué debe existir cuándo

| día | ventana del cron | huella esperada | si falta |
|---|---|---|---|
| lunes-viernes | corre (07:30 CST) | **tres commits** en `censo/<fecha>` (ACTO MAESTRA38-CRON-3, ver §1): `[CENSO]`, `[ADQ-PDN]` (aunque sea "fuera de ventana") y `[ADQ]` (D-b), este último aunque `invocado=no` | revisar §5 antes de asumir defecto — puede ser `PARO-RAIZ`/`PARO-RED` ya logueado |
| sábado, domingo | no corre | ninguna — su ausencia **no** es defecto | T-CRON no exige nada esos días (cuenta el viernes previo) |
| días 1-3 de cada mes (además de lo de arriba, si caen en día hábil) | el commit `[ADQ-PDN]` trae el re-escaneo real (no solo la línea "fuera de ventana") | los 4 zips de `pdn_bulk_<AAAA_MM>/` re-bajados y escaneados por `tests/manifiesto.py --escanea descargas_mx` (D-c), commiteados en `censo/<fecha>` (corregido por `ACTO MAESTRA38-CRON-3`: antes quedaba huérfano, sin commitear) | si el día 1-3 cae en fin de semana, el paso 2.6 se corre el siguiente día hábil dentro de la ventana `1-3`; si `1-3` completo cae en fin de semana (no puede pasar con 3 días consecutivos salvo mes que empieza en sábado), queda sin re-bajar ese mes y se declara en el log, no se fuerza fuera de ventana |
| 4/sep/2026 | fecha de instalación del cron | primera huella exigible | T-CRON no exige nada antes de esta fecha |

## §4 · T-CRON (`tests/check.py`, T31)

Implementada en `tests/check.py` (función `t31_cron`, con los
auxiliares `t_cron_ultimo_habil` y `_t_cron_existe_huella`). Regla:

- Para el último día hábil estrictamente anterior a "hoy" (lunes cuenta
  el viernes anterior; martes-viernes cuentan el día anterior; los dos
  días de fin de semana, si `check.py` corre en fin de semana, cuentan
  también el viernes previo), revisa si existe `forense/censo-raiz/
  <fecha>*.txt` en el árbol, o —vía `git ls-remote --heads origin`— una
  rama remota `censo/<fecha>` sin fusionar todavía.
- Si ninguna de las dos existe: **WARN**, nunca FAIL —
  `WARN T-CRON: sin censo del <fecha> (último hábil); cron no dejó
  huella -- ver forense/cron/REGISTRO-CRON-v1_0.md §5`.
- Excepción: no exige nada antes del 4/sep/2026 (fecha de instalación
  del cron).
- Test dedicado: `tests/test_t_cron.py` — positivo (censo local presente
  → sin huella faltante) y negativo (fecha hábil sin censo local ni rama
  remota → huella ausente, el WARN que T31 emitiría). Corre suelto:
  `python3 tests/test_t_cron.py`.

Es un WARN de vigilancia, no de regresión puntual: por diseño puede
disparar en cualquier corrida de `tests/check.py` si la caja `mm-adq` no
corrió ayer, exactamente como `T22`/`T-FIRMAS` vigila firmas pendientes.
El playbook de §5 es el primer paso al verlo, no una alarma que se
silencia editando el test.

## §5 · Playbook de diagnóstico (5 minutos)

Cuando `T-CRON` da WARN o alguien sospecha que el cron dejó de correr:

1. **¿Es fin de semana o feriado el "último hábil" que reclama el WARN?**
   `date -d <fecha> +%A` — si cae en sábado/domingo, el WARN mismo tiene
   un defecto de cálculo (repórtalo, no lo ignores); si el propio
   "último hábil" reportado es entre semana, sigue al paso 2.
2. **¿Hay log de esa fecha?** `forense/adq-log/<fecha>.log`. Si no
   existe ni local ni en ninguna rama remota reciente: el cron no
   arrancó — ir directo al paso 5 (crontab).
3. **¿El log tiene una línea `PARO-*`?** (`PARO`, `PARO-RAIZ`,
   `PARO-RED`, `PARO-CENSO-PUSH`). Cada una apunta a una causa distinta
   ya instrumentada en el propio script (corpus no montado, raíz local
   no resuelve, red caída, o el push del commit `[CENSO]` falló) — no
   son el mismo defecto que "el cron no corrió".
4. **¿El log llega hasta `claude -p` y el código de salida es != 0?**
   Revisar las últimas líneas del log para el mensaje de error de
   `claude -p` — puede ser cuota, autenticación, o el prompt extraído
   de `forense/agente-adquisicion-v1_0.md` §1 vacío/roto.
5. **¿El crontab sigue instalado y con la línea de §2?**
   `crontab -l | grep adquiere_cron` en `mm-adq`. Si la línea no está,
   o `PATH=` no está fijado, esa es la causa más común y más silenciosa
   — cron no hereda el `PATH` de un shell interactivo, así que un cron
   sin `PATH=` explícito puede fallar en el primer `git`/`curl` sin
   dejar log alguno (nada se ejecuta después del fallo del intérprete).
6. **¿La máquina `mm-adq` estuvo encendida y con red a las 07:30?**
   Última verificación, la más manual: si las cinco de arriba no
   explican la ausencia de huella, la caja pudo estar apagada,
   suspendida, o sin red en la ventana exacta del cron.

## §6 · Decisiones de dirección aplicadas en este acto

- **D-a** — fusionar `PR #556`/`PR #557` primero: **compuerta declarada
  abierta** (ver §7) — este acto no pudo fusionarlos desde este entorno
  con seguridad suficiente (`PR #557` trae explícito en su propio cuerpo
  "No se fusiona — merge de mesa"); se procede con el resto del encargo
  sin bloquear en la fusión, tal como el propio encargo autoriza.
- **D-b, opción (2)** — el trabajo `[ADQ]` **siempre** deja huella,
  incluso con `0` objetivos: implementado en `tools/adquiere_cron.sh`,
  el paso 2.5 ahora escribe, además del censo crudo, una línea
  `[ADQ] <fecha>: <n> objetivos intentados / <m> obtenidos` en el mismo
  archivo del censo del día, sin condicionarla a que `n` sea distinto de
  cero — nunca calla.
- **D-c** — tras `[ADQ-PDN]` (días 1-3 de mes), correr
  `tests/manifiesto.py --escanea descargas_mx`: implementado al final
  del paso 2.6 de `tools/adquiere_cron.sh`, para que los 4 bulk de la
  PDN aparezcan en el censo del día en vez de quedar visibles solo en el
  log de la re-baja.
- **D-d** — nunca `git reset --hard` con `data/manifiesto-staging.yaml` modificado:
  `git stash` primero. Añadida como nota en `.claude/commands/acto.md`
  (una línea) y documentada en `forense/hallazgos.md`.

## §7 · Estado de la compuerta y de los dos commits

**Compuerta (`PR #556`/`PR #557`): CUMPLIDA (`ACTO MAESTRA38-CRON-3`,
6/sep/2026).** Ambos fusionados antes de tocar código (D-a). `PR #557`
traía un conflicto real con el ya-fusionado `PR #558` (dirección lo
fusionó por error antes de lanzar el acto — ver `ADR-353`,
`gobernanza-v1_15.md`) contra `forense/tablero/TABLERO-PROGRAMA-v1_1.md`,
resuelto conservando ambas entradas en orden cronológico.

**Commit 1** (este documento + `data/INFRAESTRUCTURA-v1_0.md` + `T-CRON`
en `tests/check.py` + `tests/test_t_cron.py` + `tools/adquiere_cron.sh`
D-b/D-c + `.claude/commands/acto.md` D-d + `forense/hallazgos.md` +
tablero): hecho desde un entorno de nube, sin acceso a `mm-adq` — con dos
defectos de código (huella `[ADQ]` constante, `[ADQ-PDN]` huérfano)
corregidos por `ACTO MAESTRA38-CRON-3` (`ADR-353`).

**Commit 2 — EJECUTADO (`ACTO MAESTRA38-CRON-3`, 6/sep/2026, caja `mm-adq`
real, no sesión de nube):**
1. `crontab -e`: instalada la línea `PATH=/usr/local/bin:/usr/bin:/bin:/home/pc0/.local/bin`
   de §2 (verificado antes de instalar que `claude`/`python3`/`git`/`curl`/
   `gh` resuelven bajo ese `PATH` exacto, `env -i PATH=... which ...`, los
   cinco encontrados). `crontab -l` antes: sin `PATH=`. Después: con
   `PATH=` y el horario `30 7 * * 1-5` intacto.
2. Corrida manual de prueba, dos veces:
   - PARO forzado (`data/raw` ausente — desviación declarada del ejemplo
     del encargo, `data/raices.local.yaml`/`PARO-RAIZ`, que no detiene el
     script antes de `claude -p`): `[ADQ] 2026-09-06 16:36: invocado=no
     motivo=PARO-CORPUS exit=- duracion=0s commits_nuevos=0
     ramas_nuevas=0 archivos_modificados=2`, commiteado y empujado a
     `censo/2026-09-06` (`0096c2be`, luego reconciliado en la corrida
     completa de abajo).
   - Corrida completa: paso 2.5 escribió el censo (`139 nuevos`) y, al
     terminar, `[ADQ] 2026-09-06 16:41: invocado=si motivo=- exit=0
     duracion=179s commits_nuevos=1 ramas_nuevas=0 archivos_modificados=1`
     — invocación real de `claude -p`, `179 s`, código `0`. Paso 2.6
     escribió `[ADQ-PDN] 2026-09-06: fuera de ventana (día 6, ventana
     1-3)`. Tres commits en `censo/2026-09-06`, `PR #560` abierto.
3. Constancia: `ACTO MAESTRA38-CRON-3 · HUELLA-REAL-Y-PRUEBA-EN-CAJA`,
   6/sep/2026, ejecutado por la sesión Sonnet que corre `/acto` en esta
   caja. Detalle completo, log crudo y el archivo del censo íntegro en
   `forense/notas/2026-09-06-MAESTRA38-CRON-3-resultados.md`.

**Lo que ninguna de las dos corridas prueba: el disparo automático.**
Primera evidencia posible: `censo/2026-09-07`, lunes 07:30. `T31 T-CRON`
lo vigila desde el martes; `FP-323` sigue `ABIERTA` hasta entonces.
