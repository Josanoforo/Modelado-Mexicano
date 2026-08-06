# Verificación ad hoc · CRC de extracción y hallazgo de corrupción ENVIPE 2023

**Rama:** `tc1-corpus-010528-2` · **HEAD:** `b649995` (idéntico al contenido fusionado en
`origin/main` vía PR #144 — TC-1 ya cerrado y mergeado; este acto es posterior y no
forma parte de TC-1) · **Entorno:** local · **`data/raw`:** symlink a
`/home/pc0/mm-corpus/raw`.

Acto no asignado a un ENCARGO formal — verificación puntual pedida por mesa sobre este
worktree porque ya tenía `data/raw` montado. No se tocó `data/manifiesto.yaml`, no se
re-descargó nada, no se corrigió nada — solo se investigó y se deja constancia.

## Parte 1 · Script de verificación de extracción por CRC

Se corrió un script ad hoc que indexa `(basename, CRC32)` de todos los miembros de los
317 zips declarados en `data/manifiesto.yaml` y lo cruza contra los archivos sueltos en
`data/raw/ennvih/doc/*` y `data/raw/inegi_mmsi_2016/*` (43 candidatos, archivos sueltos
únicamente — no expande subdirectorios `*_all`, cobertura parcial declarada).

Resultado: **24 EXTRACCION-CONFIRMADA** (todos los PDFs de `ennvih/doc/*_b2.pdf`,
`*_b3a.pdf`, `*_b3b.pdf`, `*_bc.pdf`, `*_bcc*.pdf`, coinciden por CRC exacto con
miembros de los zips `ennvih1/2/3_*_hogar_cb/q` y `ennvih1/2/3_*_local_cb/q`) · **0**
casos de mismo nombre con CRC distinto · **2 huérfanos reales**
(`inegi_mmsi_2016/cuestionario_mmsi_2016.pdf`, `inegi_mmsi_2016/manual_entrevistador_mmsi_2016.pdf`).
Al abrir los 317 zips declarados, **2 no abrieron** (`BadZipFile`) — ver Parte 3, mismo
hallazgo que motivó la Parte 3 de esta nota.

## Parte 2 · Los 2 huérfanos `inegi_mmsi_2016` — no es hallazgo nuevo

Confirmado por `grep` contra `forense/`: ya están documentados en
`forense/notas/2026-08-05-tc1-corpus.md` (líneas 310-311, 351-358) y citados en
`forense/hallazgos.md`, entre los 27 huérfanos de C1 (`tests/corpus.py`) sin conexión
declarada encontrada en el acto TC-1. `data/manifiesto.yaml` no tiene ninguna entrada
con `mmsi` en absoluto (`grep -in mmsi` da cero resultados) — el paquete MMSI 2016 nunca
se dio de alta, aunque sus URLs sí están en
`data/indice-descarga-masiva-2026-08-05.tsv:7577-7581` (doc + los 4 formatos de
microdatos) y el contenido del programa sí se cita en varios reports del corpus
(`corpus/reports/*.md`, `canon/glosario-v5_6.md`, `canon/integrador-psicologia-mexicano.md`).
No se adjudica aquí si falta la entrada o si nunca debió tenerla — mismo límite que TC-1
ya declaró para este caso.

## Parte 3 · Zips corruptos `envipe2023_bd_envipe_2023_{dta,sav}` — hallazgo nuevo

No encontrado en ninguna nota previa de `forense/` (`grep -rl` sobre los dos ids y sobre
"envipe2023.*corrupt\|truncad\|BadZip" da cero resultados antes de esta nota).

Confirmado con la herramienta oficial `python3 tests/manifiesto.py --verifica --id
envipe_2023_bd_envipe_2023_dta --id envipe_2023_bd_envipe_2023_sav` — **NO COINCIDE**
en ambas entradas:

| id | sha256 manifiesto | sha256 real | tamaño manifiesto | tamaño real | % completo |
|---|---|---|---|---|---|
| `envipe_2023_bd_envipe_2023_dta` | `4a7110be…4be7` | `612c9051…746b` | 16 221 003 B | 9 289 283 B | 57% |
| `envipe_2023_bd_envipe_2023_sav` | `9c8da8e7…c9c` | `383159fb…9de5` | 26 786 689 B | 21 495 362 B | 80% |

Diagnóstico binario (no solo el mismatch de hash): ambos archivos abren con firma
`PK\x03\x04` válida al inicio (header local correcto, primer miembro `THogar.dta` /
`THogar.sav` reconocible), el `dta` tiene 4 firmas de header local de los 6 miembros que
el manifiesto declara, el `sav` tiene 5 de 6 — pero **ninguno de los dos tiene central
directory (`PK\x01\x02`) ni End-Of-Central-Directory (`PK\x05\x06`)** en ningún punto
del archivo. Es la firma de una descarga cortada a media transferencia (`curl`
interrumpido), no de un archivo con contenido erróneo ni de una corrupción por otra
causa — Python's `zipfile` no puede ni siquiera listar los miembros (`BadZipFile: File
is not a zip file`) porque no hay directorio central del que partir.

El manifiesto (`ENCARGO DESC-1, 2026-08-05`, `data/manifiesto.yaml:8413-8451`) declara
`formato: ZIP (6 miembros)` para ambos, como si la descarga hubiera cerrado bien — no se
validó la integridad al momento de `--registra`, o se validó y el archivo se corrompió
después (no investigado, fuera de perímetro de este acto).

**No corregido.** Pendiente para un acto futuro: re-descargar ambos desde las URLs ya
declaradas (`.../envipe/2023/microdatos/bd_envipe_2023_{dta,sav}.zip`) y re-correr
`--verifica` sobre los dos ids para confirmar cierre.

## Parte 4 · Barrido de EOCD sobre los 317 zips declarados (sin re-descargar)

A pedido de mesa, se extendió el chequeo de EOCD (`PK\x05\x06`, buscado en la cola de
cada archivo — últimos `22 + 65535` bytes, cubre comentario de EOCD de tamaño máximo) a
los **317 zips declarados** en `data/manifiesto.yaml`, no solo a los dos ya sospechosos.
Sin descargar nada nuevo — solo lectura de lo que ya está en disco en este worktree.

- **299 con EOCD presente** (estructuralmente cerrados; no implica que el contenido
  interno sea correcto, solo que el archivo no está truncado en la cola).
- **2 con EOCD AUSENTE** — exactamente los mismos dos de la Parte 3
  (`envipe_2023_bd_envipe_2023_dta`, `envipe_2023_bd_envipe_2023_sav`). Ningún otro zip
  del corpus tiene este defecto.
- **16 declarados sin archivo en disco** en este worktree — no evaluados (no es lo
  mismo que "ausente"; puede ser una raíz no montada aquí, p. ej. `descargas_mx`, no
  investigado en este acto, fuera de perímetro de la pregunta de mesa).

299 de 317 comprimidos terminan con EOCD; 2 no; 16 no evaluados por no estar en disco en
este worktree. Este chequeo no detecta corrupción interna ni sustitución de archivo — la
ausencia de más casos no es evidencia de que no los haya.

## Cierre

No se corrió `check.py --baseline` (no se tocó ningún archivo bajo perímetro de T-checks,
solo `data/raw`, que T02 excluye desde TC-1). No se tocó `data/manifiesto.yaml`. No se
descargó nada. Contadores movidos: 0.
