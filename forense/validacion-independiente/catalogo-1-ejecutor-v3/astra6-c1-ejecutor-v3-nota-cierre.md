# ASTRA6 C1 · ejecutor aislado v3 · nota de cierre

## Identidad y corte

EJECUTADO: sesión responsable en `/home/pc0/mm-astra6-c1-ejecutor-v3-1`, rama `codex/astra6-c1-ejecutor-v3-1`, arranque limpio desde `origin/main` `7748208614570a50a97c1ba830aee72a972185f9`. El corte de dirección `ffa1df15043befac6abdf0fdafdf2f86382f3186` es ancestro, no el SHA real de arranque. El encargo original quedó archivado una vez, bytes idénticos, bajo `forense/encargos/2026-09-27-ASTRA6-C1-EJECUTOR-AISLADO-3.md`; SHA-256 de bytes recibidos `5b9ad354e956482d8112d32c56e7325289ca5a85bf340bc9a9ae5c121296207b`, sello canónico de cuerpo `3278bb941a1bcddd7159ad86c87f41722d65fc22914b202a3f19a04d6706421c`. Sus tres adjuntos embebidos verificaron los SHA publicados. La firma «Acordado» de Jonás (26/sep, 12:07:56) se cita del asiento existente `forense/encargos/fuentes/ASTRA6-lanzamiento-20260926/00-LEEME-LANZAMIENTO.md:3`; no se duplica.

LEÍDO: #1221, #1222 y #1229 están fusionados en el corte. Se conservan sin cambios `astra6_aislamiento_v2/`, sus sellos, los paquetes residuales y los intentos anteriores. No se abrió microdato ni referencia real. Las 859 ventanas y 312 residuales son conjuntos con permisos propios; no se suman ni se declaran preparados en bloque.

## Producto

EJECUTADO: contrato v3 fijado en `ea302f89` antes de las pruebas finales. Hashes de ese commit y de los artefactos exportados en el recibo. El mapeo v2→v3 conserva cifras, alias y tolerancias y falla si un estado es ambiguo. DENOMINADOR-CERO requiere dominio observado bajo spec suficiente; incertidumbre no identificada conserva el punto útil. Es `PROPUESTO-POR-EJECUTOR` hasta firma material; no reescribe v2.

## Pruebas y alcance

EJECUTADO: `unshare` de usuario, montaje, red y PID con raíz de ejecución copiada a `tmpfs` de solo lectura, entrada también de solo lectura y `/salida` privada. `mount --bind /usr` fue denegado en esta caja; el backend adoptado copia un inventario explícito y no monta el host. OCI no está instalado aquí. `runtime-lock.json` de cada bundle fija Python 3.14.4, NumPy 2.3.5 y SHA-256 de 1055 archivos de biblioteca estándar, NumPy y dependencias ELF; `seal.json` fija sus hashes y `run` comprueba bytes antes de chroot. El inventario es contenido del bundle, no promesa de que otra máquina tenga esas versiones.

EJECUTADO: la prueba sintética `run_id=d78b453b5d4b43bb` ejecutó NumPy dentro de esa frontera. Produjo proporción ponderada 0.75 e IC calculado, dominio vacío `DENOMINADOR-CERO`, punto útil con `NO-IDENTIFICADA`, código y diagnóstico, y TSV auxiliar de 1328899 bytes. Los canarios internos aprobaron lectura permitida, denegación de escritura de entrada, secreto ficticio externo inaccesible, TCP/UDP denegados y selección de exportación (un archivo no listado quedó fuera). Referencia exclusivamente sintética abierta después de verificar exportación: `COINCIDE`. TAR de entrada con allowlist no vacía rechazó traversal, enlaces y duplicados; `verify_export` rechazó alteración posterior al sello y TAR truncado. Evidencia y hashes por archivo en `evidencia-sintetica.json`; no se incorpora el TSV al repo.

EJECUTADO: `python3 -m unittest -q tools/validacion/astra6_ejecutor_v3/test_contract.py tools/validacion/astra6_ejecutor_v3/test_session_request.py tools/validacion/astra6_ejecutor_v3/test_e2e.py` → 10/10 OK. El test de broker usa transporte en memoria y comprueba que la solicitud solo contiene prompt y bytes allowlist, y que el ensamblado posterior conserva el hash del paquete fuente y del recibo. El socket Unix y una cuenta/proveedor real no se conectaron aquí.

NO-VERIFICADO: sesión remota nueva con proveedor, configuración de herramientas y memoria real del servicio. `session_request.py` entrega un protocolo y un ensamblado invocables; falta provisionar un broker que use la cuenta ya autorizada, abra una sesión nueva con herramientas restringidas y entregue un recibo atestado. `CONTEXTO-NUEVO-ACREDITADO=PENDIENTE` para C1 real. No se atribuye esa propiedad al proceso aislado.

EJECUTADO: gate `tests/check.py --rapido` al primer intento produjo 3 FAIL propios de nombres T02/sidecar; se renombraron los dos archivos nuevos con raíz de acto y se corrigió el sidecar al formato canónico con `tools/sella_sha256.py --cuerpo`, antes del cierre. Repetición final: **0 FAIL, 622 WARN** (advertencias heredadas; ninguna nueva material). `git diff --check` sin errores. SHA-256 de archivos clave: `runtime.py` `92611d15c1ea0c0110372f8039804d69b2ab491841e76f1a7036a396ae388b5a`; `session_request.py` `a50f005a6e9f5bdd4e236ccc78d2f93038832d9610e96cfaeaf3f19f278bf0eb`; `contract.py` `183e6f0bda82d967da5f69fcb67a240543fec6297c1f69d6b093af12355cc886`; `CONTRATO-v3.md` `821a5ecb762eff1f563964a72f1e794b2899e57f66c1f62a28aae008552194eb`; `evidencia-sintetica.json` `7338b25ee43407b3609299fe224b24c0fdc11f37b95c3d37c127158e15262a45`.

## Compuertas y decisión

PROPUESTO-POR-EJECUTOR: recibir el paquete portable y su contrato para revisión. El gate `CONTEXTO-NUEVO-ACREDITADO` exige sesión nueva de proveedor con registro de prompt, herramientas y archivos; no se infiere de un `subprocess` o namespace. `CONTRATO-FIRMADO` y `ACCESO-AUTORIZADO` requieren decisiones independientes. La matriz y la orden futura están en `LANZAMIENTO.md`.

## Contador

EJECUTADO: `python3 tools/corrida0.py status` al arranque informó `celdas_validadas=219` y `resultados_con_validacion_independiente=215`. Esta entrega no modifica decisiones, usos, resultados ni contadores; pruebas/editorial no suman celdas adoptadas.
