# Recibo técnico para Claude · ASTRA6 C1 ejecutor v3

## Identidad

EJECUTADO: corte `7748208614570a50a97c1ba830aee72a972185f9`, worktree `/home/pc0/mm-astra6-c1-ejecutor-v3-1`, rama `codex/astra6-c1-ejecutor-v3-1`. Contrato v3 fijado antes de la prueba final en commit `ea302f89` (archivo `CONTRATO-v3.md`, validador `contract.py`). Encargo archivado con SHA-256 de bytes recibidos `5b9ad354e956482d8112d32c56e7325289ca5a85bf340bc9a9ae5c121296207b` y sello canónico `3278bb941a1bcddd7159ad86c87f41722d65fc22914b202a3f19a04d6706421c`. #1221, #1222 y #1229 son antecedentes leídos; sus objetos permanecen intactos.

## Qué recibe

EJECUTADO: bundle portátil en `tools/validacion/astra6_ejecutor_v3/` con materialización por allowlist, runtime científico NumPy, aislamiento con namespace o contenedor dedicado, exportación íntegra de archivos y rechazo de salida alterada. Contrato sucesor, flujo de dos etapas y orden parametrizada en `forense/validacion-independiente/catalogo-1-ejecutor-v3/`. El artefacto `evidencia-sintetica.json` (`run_id=d78b453b5d4b43bb`) contiene canarios, cálculo y hashes de entrada/salida. Ninguna cifra real ni resultado sellado se ha abierto o comparado.

## Revisión pedida

LEÍDO/PROPUESTO: verificar que la frontera local y el contrato v3 sean aptos para preparar un lote futuro. No convertir la prueba del proceso en `CONTEXTO-NUEVO-ACREDITADO`; la conexión verificable de un proveedor en sesión nueva se gatea aparte. No se solicita adopción, acceso reservado, fusión automática ni contador. Decisiones materiales: `hoja-firma-ejecutor-v3.md`.

## Comandos y límites

```sh
python3 -m unittest -q tools/validacion/astra6_ejecutor_v3/test_contract.py tools/validacion/astra6_ejecutor_v3/test_session_request.py tools/validacion/astra6_ejecutor_v3/test_e2e.py
python3 tools/validacion/astra6_ejecutor_v3/test_e2e.py --evidence forense/validacion-independiente/catalogo-1-ejecutor-v3/evidencia-sintetica.json
python3 tests/check.py --rapido
```

EJECUTADO: diez tests dirigidos OK; gate rápido 0 FAIL, 622 WARN. SHA-256 del runtime `92611d15c1ea0c0110372f8039804d69b2ab491841e76f1a7036a396ae388b5a`, del cliente `a50f005a6e9f5bdd4e236ccc78d2f93038832d9610e96cfaeaf3f19f278bf0eb`, del contrato validador `183e6f0bda82d967da5f69fcb67a240543fec6297c1f69d6b093af12355cc886`, de la spec v3 `821a5ecb762eff1f563964a72f1e794b2899e57f66c1f62a28aae008552194eb` y de la evidencia `7338b25ee43407b3609299fe224b24c0fdc11f37b95c3d37c127158e15262a45`. El PR pide recibo por el circuito de mesa; este documento no afirma haberlo obtenido.
