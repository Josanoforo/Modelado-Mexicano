# Cierre de integridad v3 · continuación de PR #1241

## Corte e identidad

EJECUTADO: misma rama y worktree `/home/pc0/mm-astra6-c1-ejecutor-v3-1`, `codex/astra6-c1-ejecutor-v3-1`; HEAD inicial `0b999e5d0be7d2f4c73baea9193c1c0beffa56e4`; main consultado `eda5bb9f871a85613cfb4eda7d40dc741e55d0b5`. #1241 seguía abierto; no se abrió otro PR. El encargo nuevo se archivó una vez en `forense/encargos/2026-09-27-ASTRA6-C1-CIERRE-INTEGRIDAD-V3-1.md`: SHA de bytes recibidos `e8cfe160dc1f250ad17341cc6f18dcccda84726d086a299b90774a8c8dca8ddc`, sello canónico de cuerpo `e2a569fe5acf85e0d15950ff5a5191fec22aa0b72e6210c8931df9d5ce9970ae`, prefijo idéntico al original. Los tres adjuntos embebidos verificaron sus SHA publicados. LEÍDO: firma «Acordado» de Jonás asentada ya en `forense/encargos/fuentes/ASTRA6-lanzamiento-20260926/00-LEEME-LANZAMIENTO.md:3`; no se duplica.

## Corrección material

EJECUTADO: `runtime.freeze_export` exige identidad esperada de paquete y SHA de manifiesto de entrada, y crea ancla externa nueva con SHA del manifiesto de exportación. `runtime.verify_export` exige esa ancla además de consistencia interna. La sustitución conjunta de `resultado.json` y `export-manifest.json` ya no cruza la frontera; tampoco una exportación internamente consistente de otro paquete. Ningún sello anterior se reescribió.

EJECUTADO: `session_request.py` conserva la solicitud canónica en el recibo y exige prompt original y SHA del recibo retenido fuera de él al ensamblar. Verifica `request_sha256`, `request_id`, archivos, herramientas, respuesta y código. Registra proveedor, modelo, sesión y `attestation` con emisor y alcance literal de declaración del broker. Esa declaración no se presenta como firma del proveedor ni como prueba por sí sola de memoria ausente.

EJECUTADO: `compare_v3.py` congela todos los archivos exportados, tolerancia v2, contrato y código comparador; entrega un SHA para guardar fuera del directorio congelado. `compare` exige ese SHA y verifica todos los bytes antes de leer referencia. Rechaza identidad, llaves y unidades incompatibles; reporta por fila estado e IC, y por componente punto, `ic95_inf` y `ic95_sup` con diferencia y tolerancia v2 sin cambiarlas. Un estado sin número se compara por contrato, sin volver `null` un cero. `COINCIDE` habla de coincidencia numérica/estructural, no de validez inferencial, adopción ni capacidad predictiva.

## Verificación

EJECUTADO: `python3 -m unittest -q tools/validacion/astra6_ejecutor_v3/test_contract.py tools/validacion/astra6_ejecutor_v3/test_session_request.py tools/validacion/astra6_ejecutor_v3/test_compare_v3.py tools/validacion/astra6_ejecutor_v3/test_e2e.py` → **15 tests OK**. Cubren los dos fallos reproducidos por el revisor, replay entre solicitudes con prompts distintos, hash inválido, código cambiado después del recibo, IC alterado que produce DISCREPA y llave/unidad/estado alterados. Conservan TAR con allowlist no vacía y canarios internos. La corrida positiva `run_id=7428fdea119d5fe6` ejecutó NumPy en el namespace de esta caja, exportó TSV de 1328899 bytes, congeló salida y comparó punto y ambos extremos IC con referencia sintética: COINCIDE. Evidencia por componente en `evidencia-sintetica-integridad-v3.json`.

EJECUTADO: `git diff --check` sin errores y `tests/check.py --rapido` → **0 FAIL, 622 WARN** (advertencias preexistentes). El contador derivado por `python3 tools/corrida0.py status` informó `celdas_validadas=219`, `resultados_con_validacion_independiente=215`, `N_resultados_gen2_adoptados_activos=81`; esta tarea no escribió datos, decisiones ni contadores.

## Gates y límite

EJECUTADO: APTO-TECNICAMENTE para runtime namespace de esta caja con sintéticos. **NO-VERIFICADO:** backend OCI, otra máquina y sesión nueva real de proveedor. `codex login status` informa cuenta ChatGPT activa, pero no hay broker con política de contexto/herramientas acreditada aquí; `provision-broker-v3.md` deja una sola operación y prueba sintética concretas. `CONTEXTO-NUEVO-ACREDITADO`, `CONTRATO-FIRMADO` y `ACCESO-AUTORIZADO` siguen pendientes por separado. No se abrió microdato ni se intentó C1 real.

## Hashes de producto

`runtime.py` `5e90cb09e59ff1b3c36ad228554b1418cf7b0a2f7828774e39e43b29758e6583`; `session_request.py` `d9f9eb30497b1ec9b503626dbb8d18ca0df8bd7d30338fd3d851f79d958ebf79`; `compare_v3.py` `4670900e4c243a4a174e3eee8a866dd1494577bb8bbf6a8484df532b611352eb`; evidencia `bbf0b29311b4bac4307b586852e4e741624ee3cd536464f0137ae2985103f48d`. Contrato v3 permanece byte a byte (`CONTRATO-v3.md` `821a5ecb762eff1f563964a72f1e794b2899e57f66c1f62a28aae008552194eb`); v2, históricos y tolerancias intactos.
