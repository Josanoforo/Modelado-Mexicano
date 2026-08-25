# Encargo `SELLA-G`

**SHA de redacción:** `f6f8e00` (`origin/main`, merge de `PR #345`).
**Entorno asignado:** NUBE (`cloud_default`), este acto (`ACTO 1` de `PACK NUBE-3`). El encargo mismo, en su
tarea UBUNTU, se ejecuta en el host UBUNTU real donde vive `~/BACKUP-mm-mirror-2026-08-10.git`.
**Estado:** PARCIALMENTE CONSUMIDO — las dos firmas de mesa (`FP-149`, `FP-151`) y las dos micro-enmiendas quedan
registradas por `ACTO SELLA-G` (ver `forense/notas/2026-08-25-sella-g.md`); la tarea UBUNTU (`FP-153`,
destrucción física del backup) queda **SIN EJECUTAR**, encargo abierto para el host real.

## Bloque VERIFICACIÓN DE EXISTENCIA (Parte 2 de A.8)

- `FP-149` — EXISTE en `forense/firmas-pendientes.tsv`: `ABIERTA` antes de este acto, nacida `ACTO
  ESCALA-ASIGNADOS` (25/ago/2026). Pasa a `FIRMADA`.
- `FP-151` — EXISTE en `forense/firmas-pendientes.tsv`: `ABIERTA` antes de este acto, nacida `ACTO
  PURGA-EJECUTA` (25/ago/2026). Pasa a `FIRMADA`.
- `~/BACKUP-mm-mirror-2026-08-10.git` — verificado en **este** entorno (NUBE): `test -e
  ~/BACKUP-mm-mirror-2026-08-10.git` → **NO-ENCONTRADO** (`~` = `/home/user`, sin ese directorio). El objeto que
  `FP-151` describe vive en el host UBUNTU (`/home/pc0/...`), no en este entorno — la destrucción queda diferida,
  no fabricada.
- `forense/notas/2026-08-25-serie-homogenea.md` — EXISTE, editado (una línea insertada, resto intacto,
  verificado por `git diff`).

## Texto del encargo (resumen operativo, transmitido por dirección 25/ago/2026)

Registrar dos firmas de mesa verbatim de la conversación del 25/ago (opción (d) sobre `FP-149`, cadena de
autorización sobre `FP-151`), siguiendo el mismo patrón ya usado para sellos anteriores (`ADR-79(a)`, `ADR-91`,
`ADR-168`, etc.): cita verbatim completa en `firmada_en`, fila mini nueva donde el acto original la reserva.
Aplicar dos micro-enmiendas de revisión de dirección: una línea fechada en
`forense/notas/2026-08-25-serie-homogenea.md` aclarando el contador vigente al fusionar (18, no 13); un
recordatorio en la nota propia del acto de que `L14`/`L16` siguen sin carta de mesa.

## Tarea UBUNTU pendiente (encargo abierto, NO ejecutado aquí)

1. Leer la cadena verbatim de `FP-151` del repo (no de memoria).
2. Verificar la premisa una última vez sobre el host real:
   `git -C ~/BACKUP-mm-mirror-2026-08-10.git count-objects -v`, `git -C ~/BACKUP-mm-mirror-2026-08-10.git fsck`
   — mismos controles que `FP-143` ya corrió sobre `mm-purga.git`, pegar salidas crudas.
3. Destruir `~/BACKUP-mm-mirror-2026-08-10.git`.
4. `FP-153` → `ejecutada_en` con las salidas crudas; línea en `forense/hallazgos.md`.

## PERÍMETRO

`forense/firmas-pendientes.tsv` · `canon/gobernanza-v1_15.md` · `canon/estado-programa-v1_10.md` ·
`forense/notas/2026-08-25-serie-homogenea.md` (una línea) · `forense/notas/2026-08-25-sella-g.md` (nueva) ·
este encargo. Fuera de este perímetro: `tools/curador_registro/**`, `data/curacion-universo/**` (workstream
concurrente ajeno), `milpa/` (fuera de alcance de este acto), y el directorio `~/BACKUP-mm-mirror-2026-08-10.git`
(fuera del repositorio, destino declarado de una destrucción futura, no ejecutada aquí).
