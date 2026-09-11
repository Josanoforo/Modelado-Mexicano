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
| huella mínima esperada por corrida | **tres commits** en `censo/<AAAA-MM-DD>` (ACTO MAESTRA38-CRON-3, `ADR-354`): `[CENSO] <fecha>` (paso 2.5), `[ADQ-PDN] <fecha>` (paso 2.6 — fuera de ventana día 1-3: una línea `fuera de ventana`; dentro de ventana: cuatro líneas `[ADQ-PDN] <SIS_LOGICO>: …`, una por sistema (s1/s2/s3/s6), con el resultado de `--compara-sha` — formato nuevo desde `ACTO AUTOMATIZA-2-E4 · PDN-COMPARA`, ver §8) y `[ADQ] <fecha> <HH:MM>: invocado=<si\|no> motivo=<-\|PARO-RAIZ\|PARO-RED\|PARO-PROMPT\|PARO-CORPUS> exit=<código\|-> duracion=<s> commits_nuevos=<k> ramas_nuevas=<j> archivos_modificados=<m>` (D-b) — medida contra el estado real del clon, nunca una constante; se escribe siempre, incluso `invocado=no` |
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
fusionó por error antes de lanzar el acto — ver `ADR-354`,
`gobernanza-v1_15.md`) contra `forense/tablero/TABLERO-PROGRAMA.md` (entonces v1_1),
resuelto conservando ambas entradas en orden cronológico.

**Commit 1** (este documento + `data/INFRAESTRUCTURA-v1_0.md` + `T-CRON`
en `tests/check.py` + `tests/test_t_cron.py` + `tools/adquiere_cron.sh`
D-b/D-c + `.claude/commands/acto.md` D-d + `forense/hallazgos.md` +
tablero): hecho desde un entorno de nube, sin acceso a `mm-adq` — con dos
defectos de código (huella `[ADQ]` constante, `[ADQ-PDN]` huérfano)
corregidos por `ACTO MAESTRA38-CRON-3` (`ADR-354`; renumerado de `353` a `354` al sincronizar -- `PR #561`/`MAESTRA38-A6` fusionó primero y tomó `353`).

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

## §8 · AUTOMATIZA-2-E4 · PDN-COMPARA — formato de huella nuevo (6/sep/2026)

**Defecto que corrige.** El paso 2.6 (D-c de §6) corría
`tests/manifiesto.py --escanea descargas_mx` tras la re-baja -- raíz
equivocada: los cuatro bulk de PDN se descargan a
`data/raw/pdn_bulk_<AAAA_MM>/`, no a `descargas_mx`; ese re-escaneo
nunca veía los archivos nuevos y la huella `[ADQ-PDN]` nunca reflejó el
estado real de la re-baja (verificado por dirección en A.8 del encargo
de este acto, re-confirmado línea por línea contra el árbol antes de
editar -- `forense/notas/2026-09-06-AUTOMATIZA-2-E4-PDN-COMPARA-resultados.md`).

**Formato nuevo, por sistema (cuatro líneas, una por `SIS_LOGICO` -- s1,
s2, s3, s6):**
```
[ADQ-PDN] <SIS_LOGICO>: estado=<E> id=<id> sha_manifiesto=<sha|-> sha_real=<sha|-> miembros_zip=<IGUAL|DISTINTO|NO-DISPONIBLE>
```
o, si la re-baja falló: `[ADQ-PDN] <SIS_LOGICO>: PARO-RED, no se pudo
re-bajar desde <URL>`. Las cuatro líneas van en el MISMO commit de
`censo/<fecha>` (`commit_censo_linea` admite cuerpo multilínea, ya
verificado por el bloque anterior de este mismo archivo). `<E>` es uno
de `COINCIDE` / `CAMBIO-DE-CONTENIDO` / `SIN-REFERENCIA-UNIVOCA` /
`SIN-SHA-EN-REFERENCIA` / `ARCHIVO-NO-LEGIBLE` (`tests/manifiesto.py
--compara-sha`, frontera epistemológica del acto que lo instala: detecta
identidad de bytes, no decide equivalencia semántica ni actualiza nada --
una discrepancia queda para adjudicación humana, Enmienda 4).

**Tabla `SIS_LOGICO` → `id_manifiesto` (cableada a mano en
`tools/adquiere_cron.sh`, nunca derivada):** `s1:pdn_s1_2026_09_06` ·
`s2:pdn_s2_2026_09_06` · `s3:pdn_s3v2` · `s6:pdn_s6_2026_09_06`. Se
actualiza a mano cuando un mes trae un id de referencia nuevo -- mientras
no se actualice, sigue comparando contra el id vigente y reporta
`CAMBIO-DE-CONTENIDO` si los bytes ya no coinciden (no es un error del
cron, es el hallazgo que este comparador existe para producir).

Actualiza §1 (huella mínima) y §3 (calendario) arriba, que describían el
`--escanea` retirado.

## §9 · Retiro del cron WSL y despliegue actual de Task Scheduler (11/sep/2026)

`PR #668` (`ACTO GEN2-RETIRO-CRON-LEGADO`) retiró la línea ejecutable
`30 7 * * 1-5 ... tools/adquiere_cron.sh` el 9/sep/2026. La comprobación
directa del 11/sep (`crontab -l`) conserva únicamente los comentarios
históricos de §2 y la asignación `PATH`; no contiene una entrada ejecutable
que nombre el runner. Windows Task Scheduler es, por tanto, el único
scheduler activo. Este asiento satisface el paso 3 de
`tools/windows/GUIA-TAREA-ADQUISICION.md` y cierra `NC-0133`; la evidencia
antes/después original permanece en
`forense/notas/2026-09-09-gen2-retiro-cron-legado-cierre.md`.

La tarea `\ModeladoMexicano\AdquiereCron` se exportó y contrastó el 11/sep.
Antes del despliegue conservaba calendario 07:30 lunes–viernes, principal
`PC0`/`Interactive`, `StartWhenAvailable=True`, `IgnoreNew` y límite `PT2H`,
pero la acción aún no llevaba la marca de atribución (export SHA-256
`3f0ac617bb60fb54948284691d049d68aa177eda7891226262c62f4dafab1a7f`). El
instalador vigente corrió primero con `-WhatIf` y luego una sola vez de forma
efectiva. La exportación posterior (SHA-256
`714e03dee7d4a2bd67ce1461902c8238eecedd203fe0f4c373f0872713eeb7d7`) conserva
esos campos materiales (el `StartBoundary` se reemitió con fecha 11/sep, sin
cambiar hora, días ni próxima ejecución) y usa:

```text
wsl.exe -d Ubuntu -u pc0 -- env ADQ_DISPARADOR=windows-task-scheduler bash -lc /home/pc0/mm-adq/tools/adquiere_cron.sh
```

La siguiente ventana es `2026-09-14T07:30:00-06:00`. El canal
`Microsoft-Windows-TaskScheduler/Operational` sigue deshabilitado: el intento
sin elevación devolvió `Acceso denegado`/código 5. Debe habilitarse antes de la
ventana con PowerShell elevado:

```powershell
wevtutil sl Microsoft-Windows-TaskScheduler/Operational /e:true
```

Hasta observar `EventRecord`/`ActivityId`, la coincidencia de hora entre la
tarea y WSL no distingue trigger semanal, recuperación o clic manual. La
cadena y el fallo externo del 11/sep se documentan en
`forense/notas/2026-09-11-GEN2-PRODUCCION-Y-FALLO-POST707-cierre.md`.
