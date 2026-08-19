# ENCARGO · REFIRMA-OPACA — re-derivar los cuatro expedientes ESP-OPACA por la herramienta canónica

**SHA de redacción:** `93a4dd9` (`origin/main`, tras `ADR-100`/`ADR-101`, ACTO MESA-18AGO, 18/ago/2026)
**Entorno asignado:** **UBUNTU**, con acceso al microdato (`data_raw`). **NO nube** — `prepare_production.py` exige `input_path`/`hash_microdato` reales por especificación; verificado en este acto que una caja de nube repo-only con `data/raw` vacío no puede correrlo (`validate_master_spec` revienta en el primer expediente).
**Estado:** `CONSUMIDO` — ejecutado por `ACTO REFIRMA-OPACA`, 19/ago/2026, rama `refirma-opaca`. Los cuatro expedientes re-firmados contra el `baseline_sha256` **vigente al ejecutar**, `a8782ca10b664cccee955b07c92eff3a70a3177385ce29b4982a3ac004d7a9b2` — **no** el `db88a09a…` que esta cabecera traía escrito: `620d524` (`ACTO B2-SEMANTICO` C5) lo movió al integrar 37 relaciones, entre la redacción de este encargo y su ejecución. Es exactamente el caso que la propia §*Verificación de existencia* mandaba anticipar. `--config` y `--snapshot`, que quedaron `A DERIVAR`, resultaron `data/curacion-registro/especificaciones-produccion.json` y `data/curacion-universo/snapshot-t0.json`. **Dos correcciones al texto de este encargo, ambas medidas:** (i) el `ESCRIBE` no alcanza al `Cierre` — `resultado.tsv` y `resumen.json` incrustan el hash de la especificación (`produce.py:230`, `:260`), así que re-firmar sólo el spec desplaza la falla en vez de cerrarla y además tumba `test_3`; mesa autorizó ampliar la cadena a `produce.py` sobre las tres cifras ya medidas (**5 → 4 → 2** pruebas que no pasan). (ii) `test_produccion_correctiva` no fallaba 4 veces sino **5**, y la quinta no comparte causa: es una expectativa rancia de `U1/E4b′` (12/ago) que no se arregla re-firmando; queda como `FP-60` (nació `FP-58`, renumerada dos veces: `PR #275` ocupó el `FP-58` y `PR #274` el `FP-59`), porque `tests/` está en el `NO ESCRIBE` de este encargo y son cifras testigo de una garantía fail-closed. `FP-47` → `FIRMADA`. `tests/check.py --baseline` VERDE. Detalle completo, con la salida cruda de los cinco comandos: `forense/notas/2026-08-19-refirma-opaca.md`.
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
