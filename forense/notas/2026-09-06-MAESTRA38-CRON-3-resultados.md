# MAESTRA38-CRON-3 · resultados

## Ajuste de base (verificado contra el árbol)

Ver `forense/notas/2026-09-06-MAESTRA38-CRON-3-spec.md` para el detalle
completo. Resumen: dirección fusionó `PR #558` por error antes de lanzar
este acto; `#556`/`#557` se fusionaron igual (D-a); `#557` traía un
conflicto real contra `forense/tablero/TABLERO-PROGRAMA-v1_1.md` con el
ya-fusionado `#558`, resuelto conservando ambas entradas en orden
cronológico (verificación de integridad: 352 ADR, máximo 352, sin
duplicados, sin huecos, tras el merge).

## Hallazgo de arranque: el sandbox de Bash bloquea el crontab real

`crontab -l` con el sandbox de Bash de esta sesión en su modo por
defecto:

```
Exit code 1
crontabs/pc0/: fopen: Permission denied
```

Con `dangerouslyDisableSandbox: true`:

```
30 7 * * 1-5 cd /home/pc0/mm-adq && ./tools/adquiere_cron.sh >> forense/adq-log/cron-stdout.log 2>&1
```

Dato nuevo, no descartado, sobre por qué "van 4 actos y sigue sin
quedar" — ver hallazgo en `forense/hallazgos.md`.

## COMMIT-2: verificación de PATH antes de instalar

```
$ which claude python3 git curl gh
/home/pc0/.local/bin/claude
/usr/bin/python3
/usr/bin/git
/usr/bin/curl
/usr/bin/gh

$ env -i PATH=/usr/local/bin:/usr/bin:/bin:/home/pc0/.local/bin sh -c 'which claude; which python3; which git; which curl; which gh'
/home/pc0/.local/bin/claude
/usr/bin/python3
/usr/bin/git
/usr/bin/curl
/usr/bin/gh
```

Los cinco resuelven bajo el `PATH` exacto de §2 de `REGISTRO-CRON-v1_0.md`.
Instalado. `crontab -l` después:

```
# tools/adquiere_cron.sh resuelve su propio REPO_DIR por
# $(dirname "${BASH_SOURCE[0]}")/.. -- pero cron NO hereda el PATH
# interactivo del usuario (sin él, `git`, `curl`, `claude`, `python3` no
# se encuentran). Fijar PATH explícito en el propio crontab, no asumir
# que hereda el del shell de login (forense/cron/REGISTRO-CRON-v1_0.md §2).
PATH=/usr/local/bin:/usr/bin:/bin:/home/pc0/.local/bin
30 7 * * 1-5 cd /home/pc0/mm-adq && ./tools/adquiere_cron.sh >> forense/adq-log/cron-stdout.log 2>&1
```

Horario `30 7 * * 1-5` sin tocar.

## P1(b) · PARO forzado

Desviación declarada (ver nota de spec): se forzó `PARO-CORPUS`
(renombrando `data/raw`), no `PARO-RAIZ`, porque `PARO-RAIZ` no detiene
el script antes de `claude -p`.

```
[2026-09-06 16:06:48-0600] === adquiere_cron.sh arrancando en /home/pc0/mm-adq ===
[2026-09-06 16:06:48-0600] git fetch && git checkout main && git pull
[2026-09-06 16:06:49-0600] HEAD tras pull: dccefdc3 Merge pull request #557 from Josanoforo/acto/maestra38-cron-diagnostico-clean
[2026-09-06 16:06:50-0600] PARO: data/raw ausente o vacío (corpus no montado en esta caja). No se invoca claude -p.
[2026-09-06 16:06:50-0600] [ADQ] 2026-09-06 16:06: invocado=no motivo=PARO-CORPUS exit=- duracion=0s commits_nuevos=0 ramas_nuevas=0 archivos_modificados=4
```

(Ese primer intento tenía cambios sin commitear del propio script de
desarrollo en el árbol — `archivos_modificados=4` — y el `checkout` a
`censo/2026-09-06` chocó con ellos; se repitió tras commitear COMMIT-2:)

```
[2026-09-06 16:36:48-0600] === adquiere_cron.sh arrancando en /home/pc0/mm-adq ===
[2026-09-06 16:36:48-0600] git fetch && git checkout main && git pull
[2026-09-06 16:36:50-0600] HEAD tras pull: dccefdc3 Merge pull request #557 from Josanoforo/acto/maestra38-cron-diagnostico-clean
[2026-09-06 16:36:50-0600] PARO: data/raw ausente o vacío (corpus no montado en esta caja). No se invoca claude -p.
[2026-09-06 16:36:51-0600] [ADQ] 2026-09-06 16:36: invocado=no motivo=PARO-CORPUS exit=- duracion=0s commits_nuevos=0 ramas_nuevas=0 archivos_modificados=2
```

Commiteado y empujado a `censo/2026-09-06` (commit `0096c2be`, luego
absorbido por el force-push de reconciliación de P1(a) — su contenido
sigue en el archivo del censo final, ver abajo). `data/raw` restaurado;
`git status` limpio salvo `data/manifiesto-staging.yaml` (trabajo en
curso de `MAESTRA38-A6`, no tocado).

## P1(a) · corrida manual completa

```
9ee99180 COMMIT-2: huella [ADQ] real (no constante) y [ADQ-PDN] commiteado
Sun Sep  6 16:38:55 CST 2026
[2026-09-06 16:38:55-0600] === adquiere_cron.sh arrancando en /home/pc0/mm-adq ===
[2026-09-06 16:38:55-0600] git fetch && git checkout main && git pull
[2026-09-06 16:38:56-0600] HEAD tras pull: dccefdc3 Merge pull request #557 from Josanoforo/acto/maestra38-cron-diagnostico-clean
[2026-09-06 16:38:56-0600] corpus montado: ls data/raw | head -1 -> 2005trim1_csv.zip
[2026-09-06 16:39:17-0600] [CENSO] 2026-09-06: Total en disco: 599 · nuevos: 139 · ya registrados: 460 · conflicto de nombre: 0 · fuera de alcance de dato: 0
[2026-09-06 16:39:18-0600] PARO-CENSO-PUSH: el commit [CENSO] 2026-09-06 quedó local, no se pudo empujar censo/2026-09-06.
[2026-09-06 16:39:18-0600] [ADQ-PDN] 2026-09-06: fuera de ventana (día 6, ventana 1-3)
[2026-09-06 16:39:19-0600] PARO-CENSO-PUSH: el commit de censo/2026-09-06 ([ADQ-PDN] 2026-09-06) quedó local, no se pudo empujar.
[2026-09-06 16:39:19-0600] sonda inegi.org.mx: curl -s -o /dev/null -w '%{http_code}' --max-time 10 https://www.inegi.org.mx/ -> 200
[2026-09-06 16:39:19-0600] prompt extraído (§1 de forense/agente-adquisicion-v1_0.md), 18 líneas:
[2026-09-06 16:39:19-0600] invocando: claude --add-dir /home/pc0/mm-corpus -p "$PROMPT"
[2026-09-06 16:41:55-0600] claude -p terminó con código 0
[2026-09-06 16:41:55-0600] [ADQ] 2026-09-06 16:41: invocado=si motivo=- exit=0 duracion=179s commits_nuevos=1 ramas_nuevas=0 archivos_modificados=1
[2026-09-06 16:41:56-0600] PARO-CENSO-PUSH: el commit de censo/2026-09-06 ([ADQ] 2026-09-06) quedó local, no se pudo empujar.
[2026-09-06 16:41:56-0600] === adquiere_cron.sh terminado ===
[exited with code 0]
```

**Las tres `PARO-CENSO-PUSH` de esta corrida no son un defecto de
producción**: son el resultado de correr el script dos veces el mismo
día calendario (P1(b) ya había empujado un `[ADQ]` a `censo/2026-09-06`
sobre una base distinta) — el paso 2.5 hace `git checkout -B
censo/<fecha>` (reconstruye la rama desde `HEAD` cada vez), así que un
segundo `push` en el mismo día es *non-fast-forward* contra el primero.
El cron real corre una vez al día; esta colisión es un artefacto de la
prueba manual repetida, no algo que el cron real produciría. Reconciliado
a mano:

```
$ git push --force-with-lease origin censo/2026-09-06
 + 0096c2be...2beede37 censo/2026-09-06 -> censo/2026-09-06 (forced update)
```

`git log --oneline origin/censo/2026-09-06 -5`:

```
2beede37 [ADQ] 2026-09-06
9eec72e1 [ADQ-PDN] 2026-09-06
a37e0025 [CENSO] 2026-09-06
dccefdc3 Merge pull request #557 from Josanoforo/acto/maestra38-cron-diagnostico-clean
238e969a Merge origin/main (PR #558) into PR #557: resuelve conflicto en TABLERO-PROGRAMA-v1_1.md
```

`PR #560` abierto contra `main` con las tres.

Contenido íntegro de `forense/censo-raiz/2026-09-06.txt` en
`origin/censo/2026-09-06`: 512 líneas (censo completo de 139 archivos
nuevos + resumen), con las tres líneas de huella al final:

```
[ADQ-PDN] 2026-09-06: fuera de ventana (día 6, ventana 1-3)

[ADQ] 2026-09-06 16:41: invocado=si motivo=- exit=0 duracion=179s commits_nuevos=1 ramas_nuevas=0 archivos_modificados=1
```

(la línea `[ADQ] 2026-09-06 16:36: invocado=no motivo=PARO-CORPUS ...`
de P1(b) quedó en la historia del commit `0096c2be`, absorbida por el
`force-with-lease`; el archivo final en `main` tras la fusión de este
`PR #560` sólo conserva la corrida completa, que es la que corresponde a
un día hábil real.)

## Lo que este acto no puede probar

El disparo automático real del cron. Primera evidencia posible:
`censo/2026-09-07`, lunes 07:30 hora de mesa. `T31 T-CRON` lo vigila
desde el martes. `FP-323` (de `#557`) sigue `ABIERTA` hasta entonces.
