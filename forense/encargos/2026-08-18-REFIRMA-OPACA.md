# ENCARGO · REFIRMA-OPACA — re-derivar los cuatro expedientes ESP-OPACA por la herramienta canónica

**SHA de redacción:** `93a4dd9` (`origin/main`, tras `ADR-100`/`ADR-101`, ACTO MESA-18AGO, 18/ago/2026)
**Entorno asignado:** **UBUNTU**, con acceso al microdato (`data_raw`). **NO nube** — `prepare_production.py` exige `input_path`/`hash_microdato` reales por especificación; verificado en este acto que una caja de nube repo-only con `data/raw` vacío no puede correrlo (`validate_master_spec` revienta en el primer expediente).
**Estado:** VIVO
**Origen:** `FP-47`, con D-6 (`ADR-101(j)`) — *"se re-firman con V5."* La "V5" de mesa es el `baseline_sha256` **vigente al ejecutar**, no una constante heredada de este encargo.

## Verificación de existencia (A.8), contestada por quien escribe

```
$ sha256sum data/curacion-registro/baseline.json
db88a09a27c3b5e569198ef6033c2a479cfe286babb7d3571011a8646e079703
```
**Re-deriva este valor al ejecutar** — no lo heredes de aquí; si `baseline.json` cambió entre este encargo y su ejecución, el valor real es otro y el expediente debe firmarse contra ese, no contra el de esta línea.

```
tools/curador_registro/prepare_production.py            EXISTE (leído, no ejecutado, en ACTO MESA-18AGO)
data/curacion-registro/expedientes-produccion/
  t0-89f4c3a49c00c0e1/ESP-OPACA-{A-7baf278d,B-d13ec4fe,
  C-9ecb5c61,D-d800e103}/especificacion-recibida.json      EXISTEN, divergentes de la maestra (verificado,
                                                            test_produccion_correctiva falla 4x, mismo mensaje)
config/snapshot de prepare_production                      A DERIVAR -- prepare_production.prepare() exige
                                                            --config/--snapshot/--baseline/--output-root; el
                                                            config maestro y el snapshot t0 no se localizaron
                                                            en este acto (nube, sin necesidad de correrlo) --
                                                            derívalos del propio directorio de expedientes
                                                            (t0-89f4c3a49c00c0e1 es el snapshot_t0_sha256) o de
                                                            quien generó el bootstrap semántico (93160c3)
```

## Perímetro

ESCRIBE: `data/curacion-registro/expedientes-produccion/t0-89f4c3a49c00c0e1/ESP-OPACA-{A,B,C,D}-*/especificacion-recibida.json` (regenerados por `prepare_production.prepare()`, nunca a mano) · nota del acto con la salida cruda del comando. NO ESCRIBE: `canon/`, `tests/`, `milpa/`, ningún otro archivo de `data/curacion-registro/`.

## Tarea

1. Re-derivar `baseline_sha256` vigente (`sha256sum data/curacion-registro/baseline.json`).
2. Localizar `--config` (especificación maestra con las cuatro `especificaciones`) y `--snapshot` (el que declara `snapshot_t0_sha256` = `89f4c3a49c00c0e1`).
3. Correr `python3 tools/curador_registro/prepare_production.py --config <config> --snapshot <snapshot> --baseline data/curacion-registro/ --output-root data/curacion-registro/expedientes-produccion/t0-89f4c3a49c00c0e1/`.
4. Verificar `test_produccion_correctiva` (o el test que `FP-47` cita) cae de 4 fallas a 0.
5. Citar D-6 verbatim en la nota, marcando los cuatro expedientes como re-firmados contra el `baseline_sha256` vigente al ejecutar.

## Cierre

Los cuatro expedientes re-firmados, cero divergencia contra la maestra (comando y salida cruda en la nota) · `firmas-pendientes.tsv`: `FP-47` → `FIRMADA`, cita D-6 y el `baseline_sha256` real usado · `tests/check.py --baseline` VERDE · línea en `hallazgos.md` · encargo `CONSUMIDO`.
