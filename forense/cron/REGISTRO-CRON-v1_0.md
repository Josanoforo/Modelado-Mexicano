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
| huella mínima esperada por corrida | `forense/censo-raiz/<AAAA-MM-DD>.txt` (paso 2.5) **y**, desde este acto, una línea `[ADQ] <fecha>: <n> objetivos intentados / <m> obtenidos` en ese mismo archivo (D-b, ver §6) |
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
| lunes-viernes | corre (07:30 CST) | `forense/censo-raiz/<fecha>.txt` con línea `[ADQ]` (D-b) | revisar §5 antes de asumir defecto — puede ser `PARO-RAIZ`/`PARO-RED` ya logueado |
| sábado, domingo | no corre | ninguna — su ausencia **no** es defecto | T-CRON no exige nada esos días (cuenta el viernes previo) |
| días 1-3 de cada mes (además de lo de arriba, si caen en día hábil) | corre además el paso 2.6 (`[ADQ-PDN]`) | los 4 zips de `pdn_bulk_<AAAA_MM>/` re-bajados y, desde este acto, escaneados por `tests/manifiesto.py --escanea descargas_mx` (D-c) para que aparezcan en el censo del día | si el día 1-3 cae en fin de semana, el paso 2.6 se corre el siguiente día hábil dentro de la ventana `1-3`; si `1-3` completo cae en fin de semana (no puede pasar con 3 días consecutivos salvo mes que empieza en sábado), queda sin re-bajar ese mes y se declara en el log, no se fuerza fuera de ventana |
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

**Compuerta (`PR #556`/`PR #557`): sigue ABIERTA.** Verificado contra
GitHub al escribir este documento: ambos PRs están `open`,
`mergeable_state: clean`, sin conflictos con `main`. No se fusionaron
desde esta sesión porque `PR #557` declara explícitamente en su cuerpo
"No se fusiona — merge de mesa" (decisión de dirección anterior, no de
esta sesión) — fusionarlo de todos modos sería pasar por encima de esa
instrucción. `PR #556` (`[CENSO] 2026-09-06`) es una rama de censo
mecánica sin esa marca, pero fusionarla sola sin `PR #557` no resuelve la
compuerta tal como el encargo la plantea (ambas, juntas). Queda para
mesa: revisar y fusionar (o rechazar con firma) los dos PRs.

**Commit 1** (este documento + `data/INFRAESTRUCTURA-v1_0.md` + `T-CRON`
en `tests/check.py` + `tests/test_t_cron.py` + `tools/adquiere_cron.sh`
D-b/D-c + `.claude/commands/acto.md` D-d + `forense/hallazgos.md` +
tablero): hecho desde este entorno de nube, sin acceso a `mm-adq`.

**Commit 2 — PENDIENTE, requiere acceso físico a `mm-adq`:**
1. `crontab -e` en `mm-adq`: instalar/confirmar la línea de §2
   (con el `PATH=` explícito — verificar con `crontab -l` después).
2. Corrida manual de prueba: `cd /ruta/al/clon && ./tools/adquiere_cron.sh`
   a mano, una vez, y confirmar en el log resultante:
   - el paso 2.5 escribe el censo **y** la línea `[ADQ] <fecha>: … /…`
     (D-b) aunque sea `0 objetivos intentados / 0 obtenidos`;
   - si cae en ventana de mes (día 1-3), el paso 2.6 corre
     `tests/manifiesto.py --escanea descargas_mx` al final (D-c) y los 4
     bulk aparecen en el censo del día.
3. Dejar constancia en este mismo archivo (`§7`, append) de la fecha en
   que ese commit 2 se ejecutó, quién lo corrió, y el resultado de la
   corrida manual.

Este commit 2 **no** se ejecuta desde esta sesión de nube — no hay
acceso a la caja física `mm-adq` desde aquí. Queda documentado como
pendiente explícito, no como hecho.
