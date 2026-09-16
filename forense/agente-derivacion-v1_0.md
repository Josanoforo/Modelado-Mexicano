# Agente de derivación · v1.0 — runbook de mesa

**P3** de `ACTO GEN2-RUTINA-DERIVADOS-1`
(`forense/encargos/2026-09-16-GEN2-RUTINA-DERIVADOS-1.md`).

Este archivo es para **mesa**, no para el ejecutor. Dice cuatro cosas:
qué se congeló (§0), qué línea se registra en el scheduler (§1), qué
esperar de cada PR y cómo leerlo en dos minutos (§2), y cuándo retirar la
pieza (§3).

**Por qué un runbook propio y no una enmienda a
`forense/agente-tramite-v1_0.md`.** El encargo de lanzamiento describía
esto como "el runbook (agente-tramite v1.1, mismo archivo, sucesión)".
Verificado contra el árbol antes de escribir (regla de la casa: la
premisa de un encargo se verifica contra el árbol, no se transcribe):
`forense/agente-tramite-v1_0.md` es el runbook de `/tramite`, con
perímetro **duro y cerrado** a `forense/firmas-pendientes.tsv` ·
`forense/digesto/` · marcas `## CONSUMIDO` · `forense/rutinas.tsv` ·
tres columnas de `forense/no-corrido.tsv`
(`.claude/commands/tramite.md` §0, punto 5: *"Nada más. Ni `canon/`, ni
`tests/`, ni `milpa/`, ni `tools/`, ni `.github/`, ni el resto de
`data/`"*). Esta rutina necesita escribir exactamente lo que ese
perímetro excluye por nombre: `tools/deriva_cron.sh`,
`data/curacion-universo/derivados/`, el bloque derivado del tablero.
Doblarla dentro de `agente-tramite-v1_0.md` habría violado el perímetro
duro de esa pieza el mismo día que se escribe, o habría obligado a
reabrir esa pieza para ensanchar un perímetro que su propio §0 declara
cerrado a propósito. Se sigue en cambio el patrón real que el repo ya
usa para cada agente de fondo — un runbook por agente
(`agente-adquisicion-v1_0.md`, `agente-tramite-v1_0.md`,
`agente-despacho-v1_0.md`, `agente-revisor-v1_0.md`) — y se conserva la
parte de la instrucción original que sí es correcta: **"mismo archivo,
sucesión"** como convención de versionado (una pieza no se renombra en
cada enmienda; las enmiendas se apendizan datadas al final del mismo
archivo, como ya hace `agente-tramite-v1_0.md` en su propia "Enmienda de
precedencia fechada"). Ese principio se aplica aquí desde `v1.0`, no
desde una `v1.1` que no tendría de qué ser sucesora.

---

## §0 · SPEC CONGELADA — COMMIT-1 del acto

### P1 · `tools/deriva_cron.sh` — el ejecutor

**No invoca ningún modelo de lenguaje.** Es la diferencia estructural
con `agente-adquisicion-v1_0.md` y con este mismo archivo si se hubiera
copiado su forma: ahí el runbook existe sobre todo para congelar **el
prompt** que se pega en la tarea recurrente, porque ese agente sí decide
con juicio acotado. Aquí no hay prompt que congelar — las cuatro
derivaciones son deterministas, y decirlo explícitamente importa porque
evita que una futura enmienda intente colarle un paso de juicio por la
puerta de atrás de "total, ya tiene un runbook".

Toma su **propio lock** (`forense/deriva-log/estado/deriva_cron.lock`,
nunca `forense/adq-log/`, que es de adquisición) y su propia rama diaria
`derivados/<AAAA-MM-DD>` (mismo patrón "reutiliza si existe, crea si es
nueva de verdad" que `checkout_o_crea_censo()` fija en
`tools/adquiere_cron.sh`, reimplementado localmente — no importado,
porque tocar `tools/adquiere_cron.sh` está fuera de perímetro de este
acto).

**Hallazgo A.7 de cableado, declarado en el propio script (comentario de
cabecera de `tools/deriva_cron.sh`):** el encargo de lanzamiento pedía
"colgado del mismo scheduler y launcher" que `/adquiere`. Verificado
contra el árbol: `tools/adquiere_launcher.sh` resuelve presupuesto y una
revisión fijada específicos de adquisición (líneas 130-175 de ese
archivo) y corre contra un clon dedicado, `/home/pc0/mm-adq`
(`forense/cron/REGISTRO-CRON-v1_0.md` §1/§9/§10) — no un multiplexor
genérico de scripts de cron. Engancharse ahí habría acoplado el disparo
diario, incondicional, de esta rutina al presupuesto y a la semántica de
"hay trabajo atendible" de adquisición, sin necesidad real: esta rutina
no tiene concepto de presupuesto y corre siempre, todos los días
hábiles. **Se mantiene "mismo scheduler"** (Windows Task Scheduler, la
misma máquina) **con "launcher" propio**: `tools/deriva_cron.sh` es su
propio lanzador, y se registra como entrada independiente en
`forense/cron/REGISTRO-CRON-v1_0.md` §11 — sin tocar
`tools/adquiere_launcher.sh` ni `tools/adquiere_cron.sh`.

**El universo declarado, como sucesión fechada, sin tocar T0.**
`tools/curador_registro/snapshot_universe.py` no tiene hoy noción de
fecha ni de sucesión — su único modo histórico escribe siempre a rutas
fijas bajo `--output-dir`, incluido `snapshot-t0.json`, cuyo
`snapshot_t0_sha256` `integrate_production.py::canonical_analyst_spec()`
verifica contra tres expedientes ya sellados
(`data/curacion-registro/expedientes-produccion/t0-89f4c3a49c00c0e1/`).
Regenerar esas rutas in situ, aunque fuera aditivo, rompería esa
verificación (confirmado en este acto contra
`tools/curador_registro/tests/test_produccion_correctiva.py`, y ya
documentado como riesgo real en `forense/hallazgos.md`,
2026-08-12). Por eso `tools/deriva_cron.sh` corre el mismo script, sin
tocarlo, hacia un directorio efímero (`mktemp -d`) y solo persiste un
**resumen compacto** nuevo en `data/curacion-universo/derivados/
universo-<fecha>.json` (conteos + hash del día + diff contra la sucesión
anterior o contra `snapshot-t0.json` en la primera corrida) — nunca los
TSV de decenas de MB que el script también produce. `T0` queda intacto
porque nunca se escribe ahí; "solo sucesiones nuevas" (perímetro del
encargo) se cumple porque lo único que se añade es ese archivo fechado.

**Ledger de inspecciones arrastrado por hash.** No es una pieza nueva:
`data/curacion-universo/ledger-inspecciones-t0.tsv` ya lleva su propia
regla de idempotencia ("la condición histórica se lee del ledger y se
valida contra filas derivadas; nunca se reclasifica por existencia del
expediente vigente"). Esta rutina no re-corre el pipeline de inspección
ni escribe ese ledger — al no tocarlo, la propiedad de arrastre por hash
que ya tenía se conserva sin más.

**Si el diff del universo es material** (cualquier conteo de activos
que baja, o el hash compuesto del día cambia frente al anterior): el
script lo marca `HALLAZGO A.7` dentro del propio `universo-<fecha>.json`
y en su huella — lo reporta, no lo resuelve. Reconciliar un universo que
se movió es de mesa/dirección.

**La suite corre primero, no en el orden de enumeración del encargo.**
Mismo criterio, verbatim, que `forense/agente-tramite-v1_0.md` §0 P2 fijó
para `/tramite`: "ROJO → PARA. Termina con cero commits... la suite roja
no es tuya para arreglarla: es un hallazgo, y va al reporte." Enumerar
cuatro derivaciones en el encargo no fija su orden de ejecución.

### P2 · `.claude/commands/deriva.md` — el envoltorio

Arranque ligero (clon, entorno CAJA, corpus montado), invoca
`tools/deriva_cron.sh`, reporta lo que produjo. No reimplementa ninguna
de las cuatro derivaciones a mano.

### P3 · este archivo

Runbook de mesa. §1 la línea de disparador, §2 cómo leer el PR, §3 el
falsador.

---

## §1 · La línea que se registra en el scheduler

**Distinto de `agente-adquisicion-v1_0.md` §1: no hay prompt que pegar
en ninguna tarea de Claude Code, porque esta rutina no invoca ningún
modelo.** Lo que mesa registra es una acción de Windows Task Scheduler
que invoca `tools/deriva_cron.sh` directamente — mismo mecanismo que
`forense/cron/REGISTRO-CRON-v1_0.md` §9 documenta para adquisición, pero
como **tarea independiente**, nunca encadenada al launcher de ese
archivo (ver el hallazgo A.7 de §0 arriba).

**Este acto NO instala la tarea.** Corre en CAJA, dentro de un sandbox
de Ubuntu/WSL sin acceso al Task Scheduler del host Windows — el mismo
motivo, verificado de nuevo aquí, por el que
`forense/encargos/2026-09-01-MAESTRA34-N7-SKILLS-COLA-Y-ADQ.md` declaró
"instalación manual por mesa, no se instala desde aquí" para el primer
cron de adquisición. La línea sugerida, para que mesa la registre contra
el clon que aloje esta rutina:

```text
wsl.exe -d Ubuntu -u pc0 -- env DERIVA_DISPARADOR=windows-task-scheduler bash -lc <RUTA_DEL_CLON>/tools/deriva_cron.sh
```

Cadencia sugerida: diaria en día hábil, después de que el corpus del día
haya tenido oportunidad de asentarse (p. ej. 08:30 hora de mesa, una hora
después del disparo de adquisición a las 07:30 — ver
`REGISTRO-CRON-v1_0.md` §1). Registrar el resultado de la instalación
(exportación de la tarea, ventana siguiente) en una futura enmienda
datada de este mismo archivo, siguiendo el patrón de §9/§10 de
`REGISTRO-CRON-v1_0.md`.

## §2 · Qué esperar de cada PR

Un PR `[DERIVADOS] <fecha>` sano trae, siempre:

- **A lo sumo dos rutas de archivo** fuera del propio commit: un archivo
  nuevo en `data/curacion-universo/derivados/` (solo si el universo
  cambió) y/o un diff del bloque `<!-- TABLERO-DERIVADO -->` de
  `forense/tablero/TABLERO-PROGRAMA.md`. Nada más.
- **Las cuatro deltas en el cuerpo**, una línea por derivación, con la
  suite primero.
- **Un `HALLAZGO A.7`** citado explícitamente si el universo trajo un
  diff material — sin resolverlo.
- **Cero decisiones.** Si el PR pregunta algo, no es de esta rutina.
- Si nada cambió: **cero PR**, y la huella `NADA-QUE-HACER` vive solo en
  `forense/deriva-log/<fecha>.log` (gitignorado) — mismo patrón que
  `/despacha` con la cola vacía.

**Fusionar es firmar.** El PR propone; mesa firma al fusionar.

## §3 · Falsador, a un mes

Se revisa la pieza y se anota si en un mes ocurre cualquiera de estas
dos:

- **(a)** un PR `[DERIVADOS]` **requiere retrabajo de mesa** más allá de
  decidir si fusiona;
- **(b)** un PR `[DERIVADOS]` **toca algo fuera del perímetro** de dos
  rutas (`data/curacion-universo/derivados/`, el bloque derivado del
  tablero), aunque el cambio sea correcto.

Y la prueba de que la pieza sirvió, para el otro lado: que las tres
líneas base que `ACTO GEN2-RUTINA-DERIVADOS-1` midió como recongeladas a
mano (T0, tablero, suite) dejen de envejecer sin que nadie las corra a
mano en cada corte.

**CONTADOR de este acto: la primera corrida (T1) se reporta a mano en el
propio encargo (P2) — no es una medición GEN2, es infraestructura.**
