---
description: Corre las cuatro derivaciones diarias por script (universo declarado, tablero, registro en seco, suite en línea base) y abre UN PR [DERIVADOS] <fecha> con la huella, o cero PR con huella NADA-QUE-HACER. Nunca decide, nunca recongela la línea base.
argument-hint: (sin argumentos; disparador=windows-task-scheduler|manual|prueba-programada|fixture vía $DERIVA_DISPARADOR)
---

# `/deriva` — cuatro derivaciones, todas por script, ninguna por juicio

Instaurada por `ACTO GEN2-RUTINA-DERIVADOS-1`
(`forense/encargos/2026-09-16-GEN2-RUTINA-DERIVADOS-1.md`). Corrige el
defecto real que ese encargo midió: tres líneas base (`data/curacion-
universo/snapshot-t0.json`, `forense/tablero/TABLERO-PROGRAMA.md`, la
línea base de `tests/check.py`) se venían recongelando **a mano** — T0 un
mes/1178 PRs atrás, el tablero 50 PRs atrás, la suite cuatro veces a mano.

**Este agente no invoca ningún modelo.** A diferencia de `/adquiere`
(que camina una cola con juicio y una invocación de lenguaje por fila) y
de `/tramite` (que mueve filas de `firmas-pendientes.tsv` con juicio
acotado), las cuatro derivaciones de aquí son mecánicas de principio a
fin. El mecanismo entero vive en `tools/deriva_cron.sh`; esta skill es un
envoltorio delgado que lo invoca, reporta lo que produjo, y **nunca**
reimplementa a mano ninguno de sus cuatro pasos.

El runbook de mesa —la línea de disparador que se instala en el
scheduler, cómo leer el PR y el falsador— vive en
`forense/agente-derivacion-v1_0.md`.

---

## 0 · LO QUE ESTE AGENTE NO ES

1. **Nunca escribe `canon/`, `milpa/`, ni decide nada.** Las cuatro
   derivaciones son lectura + regeneración mecánica de artefactos ya
   existentes (`data/curacion-universo/derivados/`, el bloque
   `<!-- TABLERO-DERIVADO -->`). Si algo del árbol pide una decisión, se
   reporta como hallazgo en el PR — nunca se resuelve aquí.
2. **Nunca adopta.** No toca `milpa/tramite.yaml` ni ninguna adopción de
   regla del motor.
3. **Nunca recongela la línea base.** `tests/check.py` corre siempre con
   `--baseline` (comparación), jamás con `--freeze`.
4. **Si el diff del universo declarado es material** (activos que
   desaparecen, el hash compuesto del snapshot cambia), **lo reporta como
   hallazgo A.7 en el PR y no lo resuelve.** Reconciliar un universo que
   se movió es de mesa/dirección.
5. **Un PR diario es lo máximo que produce.** Si ya hay un PR
   `[DERIVADOS] <fecha>` abierto para hoy, se reutiliza — nunca se abre
   un segundo.
6. **Perímetro duro, cerrado**: `tools/deriva_cron.sh` (su propio lock,
   nunca `forense/adq-log/`) · `data/curacion-universo/derivados/`
   (solo archivos fechados nuevos — nunca `snapshot-t0.json` ni los TSV
   de T0) · el bloque `<!-- TABLERO-DERIVADO:BEGIN/END -->` de
   `forense/tablero/TABLERO-PROGRAMA.md`. **Nada más.** Ni
   `tools/adquiere_cron.sh` ni `tools/adquiere_launcher.sh` — ver el
   hallazgo A.7 de cableado en `forense/agente-derivacion-v1_0.md` §1
   sobre por qué esta rutina no comparte ese launcher.

---

## 1 · ARRANQUE LIGERO

Igual de ligero que `/tramite` §1: no es el `ARRANQUE` de cinco puntos de
`/acto` completo, pero sí sus partes materiales para esta rutina:

1. **CLON.** Localiza el clon existente sobre el que corre esta invocación.
2. **ENTORNO.** `echo "${CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE:-<sin_variable>}"`
   — se espera `<sin_variable>` (CAJA). Esta rutina deriva el universo
   declarado del corpus compartido; **la cabecera del propio encargo lo
   dice: "la caja es el único entorno que puede derivar el universo"**.
   Si el valor no es `<sin_variable>`, PARA y repórtalo.
3. **CORPUS.** `ls -la data/raw | head -1` — si falta el symlink en un
   worktree nuevo, enlázalo desde el clon padre (`ln -s
   /home/pc0/mm-corpus/raw data/raw`) antes de correr nada; ausente no es
   PARO, es un paso de arranque (mismo criterio que `/acto` punto 3).

## 2 · LA CORRIDA

```
./tools/deriva_cron.sh
```

(con `DERIVA_DISPARADOR=manual` si no está puesto — el script lo asume
por defecto). El script hace, en este orden, las cuatro derivaciones —
la suite corre **primero**, no en el orden de enumeración del encargo,
por el mismo criterio de `forense/agente-tramite-v1_0.md` §0 P2 (ROJO =
PARO, cero commits, para no apilar ruido sobre un hallazgo ajeno):

- **(d) `tests/check.py --baseline`.** ROJO → el script termina con cero
  commits y huella local `PARO-SUITE-ROJA`. Repórtalo con la salida
  cruda; no repares la suite desde aquí.
- **(a) `snapshot_universe.py`** hacia un directorio efímero, comparado
  contra la última sucesión fechada en `data/curacion-universo/
  derivados/` (o contra `snapshot-t0.json` si es la primera corrida —
  ver P2 del encargo, corrida T1). `T0` nunca se toca.
- **(b) `tablero_programa.py --actualiza`** sobre `forense/tablero/
  TABLERO-PROGRAMA.md` — ya es idempotente por sí mismo.
- **(c) `corrida0.py registro --verifica`** (en seco: sin `--escribe`,
  no toca ningún TSV) **y `corrida0.py status`** (solo lectura).

Si nada de esto produjo un cambio versionable, el script termina con
huella `NADA-QUE-HACER` y **cero PR** — mismo patrón que `/despacha`
cuando la cola está vacía. Si algo cambió, abre (o reutiliza) **un** PR
`[DERIVADOS] <fecha>` con las cuatro deltas en el cuerpo.

No reproduzcas a mano ninguno de estos cuatro pasos si el script ya
corrió — lee su log (`forense/deriva-log/<fecha>.log`) y su huella antes
de repetir nada.

## 3 · CIERRE

Esta skill **no** corre la cascada de `/acto`: no deriva ADR, no toca
`canon/gobernanza-v1_15.md`, no recifra `L0`. Un PR `[DERIVADOS]` no
decide nada, así que no hay decisión que registrar. Si un día uno de
estos PR necesitara un ADR, eso significa que dejó de ser una derivación
mecánica — **PARA y repórtalo**, no lo selles.

Falsador y caducidad: `forense/agente-derivacion-v1_0.md` §3.
