# MAESTRA38-CRON · DIAGNOSTICO-Y-ARREGLO — nota de cierre

Encargo: `forense/encargos/2026-09-06-MAESTRA38-CRON-DIAGNOSTICO-Y-ARREGLO.md`.
Ninguna de las cuatro lecturas pre-declaradas (a)/(b)/(c)/(d) se cumple.
No se toca `tools/adquiere_cron.sh`.

## P0 · salida cruda de los cinco comandos

```
$ crontab -l
30 7 * * 1-5 cd /home/pc0/mm-adq && ./tools/adquiere_cron.sh >> forense/adq-log/cron-stdout.log 2>&1
```

(el comando falló dentro del sandbox de esta sesión — `crontabs/pc0/:
fopen: Permission denied` — y se repitió con
`dangerouslyDisableSandbox`; es restricción del sandbox de la sesión,
no del sistema: `systemctl is-active cron` → `active`.)

```
$ ls -la forense/adq-log/ forense/censo-raiz/
forense/adq-log/: 2026-09-02.log, 2026-09-04.log, 2026-09-05.log
forense/censo-raiz/: .gitkeep, 2026-09-04-cron-2339.txt, 2026-09-04.txt
(sin archivo de 2026-09-05: coherente con P0 abajo — 2026-09-05 es sábado)
```

```
$ tail -40 forense/adq-log/2026-09-05.log
[2026-09-05 15:25:50-0600] claude -p terminó con código 0 (corrida anterior, cortada por el tail)
[2026-09-05 16:47:21-0600] === adquiere_cron.sh arrancando en /home/pc0/mm-adq ===
[2026-09-05 16:47:21-0600] git fetch && git checkout main && git pull
Already on 'main'
M	data/manifiesto-staging.yaml
M	tools/adquiere_cron.sh
Your branch is ahead of 'origin/main' by 1 commit.
[2026-09-05 16:47:22-0600] HEAD tras pull: a60c6611 [CENSO] 2026-09-04
[2026-09-05 16:47:22-0600] corpus montado: ls data/raw | head -1 -> 2005trim1_csv.zip
[2026-09-05 16:47:22-0600] PARO-RAIZ: descargas_mx no resuelve en esta máquina (data/raices.local.yaml). Censo omitido, sigue con /adquiere.
[2026-09-05 16:47:22-0600] sonda inegi.org.mx: ... -> 200
[2026-09-05 16:47:54-0600] claude -p terminó con código 0
[2026-09-05 16:47:54-0600] === adquiere_cron.sh terminado ===
```

No hay `forense/adq-log/cron-stdout.log` con contenido nuevo relevante
más allá de lo anterior (el archivo agrega el stdout de cron, no de
corridas manuales).

```
$ git branch --show-current
main
$ git status --short | head
(vacío tras `git checkout main && git pull --ff-only` — el estado sucio
visto en el log del 5/sep, con data/manifiesto-staging.yaml y
tools/adquiere_cron.sh modificados y la rama 1 commit adelante, ya no
existe: quedó resuelto por el merge de PR #546 esa misma noche)
```

```
$ systemctl is-active cron
active
$ grep -i cron /var/log/syslog | grep -i adquiere
(vacío: syslog de systemd solo registra las sesiones PAM de cron —
root, run-parts horarios — no el comando que cron ejecutó como pc0; no
es evidencia de que el job de pc0 no disparara)
```

Adicional (`date`): la caja está en `CST` (`-0600`), no en UTC — la
línea `30 7` corre a las 07:30 hora local, como el runbook pretende. No
aplica el ajuste a `30 13` de la lectura (a).

## Por qué ninguna lectura pre-declarada se cumple

- **(a)** descartada: `crontab -l` **sí** trae la línea, con la hora
  correcta (`30 7 * * 1-5`) y rutas ya absolutas. El disparo de las
  23:39 del 4/sep fue, en efecto, una corrida manual/de prueba — pero
  la línea instalada hoy ya es la correcta, no hace falta reinstalarla.
- **(b)** descartada: el estado sucio (`manifiesto-staging.yaml`
  modificado, rama 1 commit adelante) que el log del 5/sep muestra
  **ya no existe** — se resolvió solo, vía el merge de PR #546
  ([N6-bis], fusionado 2026-09-06T00:32:56Z), que reescribió el propio
  script para no pisar `main` protegida (ver abajo). No hace falta el
  arreglo COMMIT propuesto porque el defecto que lo motivaba ya se
  corrigió por otra vía antes de este acto.
- **(c)** descartada: el servicio está activo y la línea es correcta,
  pero la premisa («sin log del 5/sep») es falsa — **sí** hay log del
  5/sep, solo que de corridas manuales, no del cron programado.
- **(d)** descartada: no hay ningún `[CENSO]` commiteado-y-empujado sin
  PR en ningún log examinado.

## El hallazgo real: 2026-09-05 fue sábado

La línea de cron es `30 7 * * 1-5` — **lunes a viernes**. `date -d
2026-09-05 +%A` → `Saturday`. La ausencia de `censo/2026-09-05` no es
un defecto: el cron nunca debió dispararse ese día. El único disparo
programado desde que el runbook quedó instalado con la hora correcta
fue el viernes 2026-09-04 a las 07:30, y ese sí produjo
`forense/censo-raiz/2026-09-04.txt` + el `[CENSO] 2026-09-04` que ya
está fusionado (`a60c661`, mismo commit que el encargo cita en A.10).
El commit `a60c6611`, con "(cron 23:39)" en el mensaje del rename, es
de un **rename posterior** de ese mismo censo — no evidencia de un
segundo disparo de cron a las 23:39; no se investigó más porque no
altera la conclusión (la única corrida de cron programada de la semana
sí produjo censo).

Las entradas `PARO-RAIZ` del log del 5/sep vienen de corridas manuales
hechas dentro de una sesión de Claude Code sandboxed — la ruta
`descargas_mx` resuelve a `/mnt/c/Users/PC0/Descargas MX`
(`data/raices.local.yaml`), y el sandbox de esa fecha bloqueaba lecturas
de `/mnt/c` (defecto de sandbox, corregido el propio 6/sep, ver memoria
de proyecto). El cron real —proceso de sistema, sin el sandbox de
Claude Code— nunca estuvo sujeto a esa restricción; no es un defecto
del script ni de la línea de crontab.

## P1 · prueba de extremo a extremo (hoy, domingo 2026-09-06)

Corrida manual de `./tools/adquiere_cron.sh` desde `/home/pc0/mm-adq`,
fuera del sandbox de esta sesión (para replicar las condiciones del
proceso de cron real):

```
[2026-09-06 15:13:06] === adquiere_cron.sh arrancando en /home/pc0/mm-adq ===
[2026-09-06 15:13:07] HEAD tras pull: ef9ba360 Merge pull request #555 ...
[2026-09-06 15:13:07] corpus montado: ls data/raw | head -1 -> 2005trim1_csv.zip
[2026-09-06 15:13:22] [CENSO] 2026-09-06: Total en disco: 599 · nuevos: 139 · ya registrados: 460 · conflicto de nombre: 0 · fuera de alcance de dato: 0
[2026-09-06 15:13:23] [CENSO] 2026-09-06 commiteado y empujado a censo/2026-09-06
[2026-09-06 15:13:25] [CENSO] 2026-09-06: PR abierto para censo/2026-09-06
[2026-09-06 15:13:25] [ADQ-PDN] 2026-09-06: fuera de ventana mensual (día 6, ventana 1-3), no se re-baja el bulk PDN hoy.
[2026-09-06 15:13:25] sonda inegi.org.mx: ... -> 200
[2026-09-06 15:15:16] claude -p terminó con código 0
[2026-09-06 15:15:16] === adquiere_cron.sh terminado ===
EXIT: 0
```

Éxito: `PR #556 [CENSO] 2026-09-06` (rama `censo/2026-09-06`), sin
fusionar. **Control positivo cumplido**: `nuevos: 139` (>0) — incluye
el/los payload(s) que mesa depositó desde el último censo del 4/sep;
no se aisló el conteo al único archivo `MEX_2016_APIPIE_v01_M_Stata.zip`
citado en el encargo porque el censo no reporta por archivo individual,
solo el agregado — el agregado ya basta como control positivo (>0
nuevos donde antes había 0 disponibles no cambia la conclusión: la
tubería censo→commit→rama→PR funciona de punta a punta).

El sub-paso `/adquiere` (vía `claude -p`) declaró correctamente una
caminata vacía (cero filas con ≥7 días sin intento y sin veredicto de
mesa vigente) — comportamiento correcto de la skill, no un fallo del
cron.

## Conclusión y arreglo

**Ningún arreglo de código o de crontab es necesario.** La línea de
`crontab -l` ya es la correcta, el script ya resuelve el estado sucio
por sí mismo (git checkout/pull al arrancar, ya presente antes de este
acto), y la prueba de extremo a extremo de hoy cerró con éxito
completo. `tools/adquiere_cron.sh` y
`forense/agente-adquisicion-v1_0.md` **no se tocan** — el perímetro
condicionaba esos dos archivos a que (b) o (c) se cumplieran, y
ninguna se cumplió.

## P2 · verificación del programador — declarada, no cerrada

La prueba real sigue siendo `censo/2026-09-07` (lunes) a las 07:30
hora local (`CST`, confirmado con `date`). Este acto deja **un** dato a
favor (`censo/2026-09-06` manual, hoy) pero **cero** disparos
automáticos de cron observados con la línea ya correcta — el conteo
del encargo (programador: 1 declarado → 0 medido) sigue en 0 hasta el
lunes.
