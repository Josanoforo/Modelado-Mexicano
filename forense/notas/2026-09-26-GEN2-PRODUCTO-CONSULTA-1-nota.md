# Nota de cierre · ACTO GEN2-PRODUCTO-CONSULTA-1

26/sep/2026 · NUBE (hook: `ENTORNO-DERIVADO = NUBE`; corpus montado=NO, archivos examinados=0; este acto no abre microdato ni red) · MODO AUTÓNOMO-AMPLIO · rama `claude/new-session-nz807l` · 0-bis `dcde797` · `ADR-260926-GEN2-PRODUCTO-CONSULTA-1-dcde-01`.

**Contadores movidos: cero.** Cero mediciones; no adopta; no escribe catálogo, vistas, CALC, motor ni CI.

## ARRANQUE
- Base: `3494975` = SHA de redacción `34949751` (main sin moverse; `HEAD..origin/main` = 0).
- Duplicado: rama remota 0 · worktree 1 (este) · PR abiertos con el rótulo 0.
- `limpia_arbol.py --reporta`: 1 worktree, base al día; D NO-VERIFICABLE-SIN-GH.

## Premisas (§3 del encargo) re-verificadas
- `tools/consulta.py`, `tools/vista.py`: EXISTEN; `consulta.py` lee TSV/YAML de corrida0 fila a fila. **No se reusan como biblioteca**: la consulta del producto lee sólo el catálogo (contrato §1) y los RESULT sellados; importar `vista.py` habría traído otra fuente de cifras. Discrepancia resuelta por el ejecutor (cláusula 1).
- Catálogo v1.1: catalogo=v1_1 · archivo=canon/catalogo-del-mexicano-v1_1.tsv · filas=36143 (por comando). Tabla de piso v1.0: 72 filas, EXISTE; la consulta no la usa como fuente de cifras (el catálogo la subsume en adopción); `docs/reto.md` sigue citándola como v1.0 lo hacía.
- `docs/reto.md` **ya existía** (v1.0, 54 líneas): el encargo §4 no lo contó («consulta|consultar|ejemplos» → 0 es cierto; `reto` no estaba en el patrón). Se actualizó a v1.1 añadiendo una sección; no se reescribió v1.0.
- [SUPUESTO] Pages sirve JSON y JS inline: NO-VERIFICABLE-AQUÍ (Pages no activo; FP-260923-GEN2-FRONT-1-4296-01 ABIERTA). Prueba local, abajo.

## Qué se entregó
1. `docs/consulta.md` — contrato v1.0, commiteado **antes** del código (`9b831c0`, D-15). Enmienda v1.0-a en el mismo acto, antes de fusionar: segmento exacto antes que subcadena (`superior` casaba `media_superior`).
2. `tools/benchmark.py` — `puntero` (N mayor de `canon/catalogo-del-mexicano-v*_*.tsv`: la consulta apunta a v1.2 cuando CIERRE-SEMANAL la publique, sin editar código) · `consulta` (humana y `--json`) · `verificar` (sello.sha256 → sello.json → resultados.json → valor = catálogo → calcs.tsv → spec/ejecucion) · `exporta` · `ejemplos`.
3. `tests/test_benchmark.py` — 9 tests; el de **equivalencia recorre las 36 143 filas** y compara punto e IC con el RESULT sellado; **prueba por mutación**: alterar un punto en 1e-9 → `ATRAPA: 1 filas de v1_1 no reproducen su RESULT`. `pytest -q tests/test_benchmark.py` → `9 passed in 2.52s`. Entra a CI como huérfano (`ci_guardias --ejecuta-huerfanos`), sin editar verify.yml ni check.py (D-21).
4. `docs/data/catalogo-v1_1.json` (4634728 bytes, sha256 `ccebca9a6abcaf9aa399370aa99df32ef2a312b4491296fa01596799bd28cef7`) + `docs/data/catalogo-vigente.json` (puntero). Columnar con diccionarios; números como el texto del catálogo; cota del test 8 MB.
5. `docs/consultar.md` — búsqueda del lado del cliente, sin servidor ni dependencias externas; misma lógica que la CLI.
6. `docs/reto.md` v1.1 — familia 2027: formato = contrato de consulta, sello previo (sha256 en el commit del PR + sello externo opcional), recibo, comparación primaria ΔMAE (regla 2). PROPUESTO-POR-EJECUTOR sobre el plan §3.6 aprobado en bloque.
7. `docs/ejemplos.md` — cinco preguntas (TRABAJO, GÉNERO, TECNOLOGÍA, DINERO, SALUD) + un límite (ENOE 2026, OLA-RESERVADA); salida cruda regenerada por `benchmark.py ejemplos`, las cinco con `CADENA-VERIFICADA`; un test impide el desfase.

## Prueba en navegador sin red
Chromium (Playwright, `/opt/pw-browsers/chromium`) sobre la página renderizada (front matter quitado, `relative_url` resuelto a rutas relativas), servida por `python3 -m http.server` en 127.0.0.1, **con toda petición fuera de localhost abortada**: `Catálogo v1_1 · 36143 pisos adoptados`; `laboral`+`escolaridad=superior` → 2 filas (= CLI); `no_tiene_ahorros_enif2024`+`nse=bajo` → 1; `empleo` ENOE 2026 → 0 + `OLA-RESERVADA` (= CLI); `violencia` → `DOMINIO-NO-MEDIDO` (= CLI); `errores_js=[]`, `peticiones_fuera_de_localhost_bloqueadas=0`. En `file://` Chromium bloquea `fetch`: la página lo dice («sírvela con: python3 -m http.server»). Captura en el scratchpad de la sesión (no versionada).

## Hallazgos (una línea cada uno)
- El eje `region` del contrato es entidad federativa: el eje regional v1.0 no está adoptado; la consulta lo declara `EJE-NO-DISPONIBLE` si se pide otra cosa.
- `olas_reservadas` se deriva de ids del manifiesto por patrón `<instrumento>_<año>` (sin abrir payloads); un id que no siga el patrón no aparecería — la ola igual no está en el catálogo, así que la consulta no devuelve cifra de ella.
- Todo el catálogo es RETROSPECTIVA (36 143/36 143): la columna PROSPECTIVA existe en el contrato y hoy va vacía.

## Módulo de auditoría (§5)
¿Contadores movidos? Cero. ¿Escala? Cada respuesta trae `unidad` verbatim y el contrato prohíbe comparar unidades distintas. ¿PROSPECTIVA vs RETROSPECTIVA? Ninguna frase las mezcla; todo es RETROSPECTIVA. ¿Pobreza/estructura como cultura? Los ejemplos cierran con la lectura estructura-y-oferta; la columna de oferta viaja en cada fila de DINERO. ¿Afirmación a mano sobre el corpus? Ninguna cifra de la página ni de los ejemplos está tecleada: todas salen de `benchmark.py`.
