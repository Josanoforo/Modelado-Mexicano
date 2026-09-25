# GEN2-FRONT-2 · cierre técnico

Encargo: `forense/encargos/2026-09-24-GEN2-FRONT-2.md` (0-bis, sello de cuerpo en su sidecar). SHA de redacción declarada `8358b891`; HEAD al abrir era exactamente `8358b891` (merge de PR #1120) — sin drift, no hubo que re-derivar nada. ENTORNO-DERIVADO = NUBE, coincide con lo declarado. Rama: `claude/new-session-punbef` — la cláusula de latitud del propio encargo (§6.6) admite "la que fije la plataforma"; ésta es la rama que la plataforma de esta sesión ya tenía abierta, se declara así en vez de crear `acto/gen2-front-2`. MODO AUTÓNOMO (cláusula de autonomía v1.0, `3fbc487684b77b7f`): cero preguntas a mesa, latitud usada en tres puntos menores (ver más abajo), todas declaradas.

CONTADOR: cero mediciones nuevas, cero adopciones. Todo el trabajo es filtro, presentación y verificación de lo ya sellado en el catálogo v1.0 y en `data/corrida0/`.

## Piezas

**P1 · One-pager.** `docs/one-pager.md` + `docs/one-pager.pdf`. El PDF se genera desde el mismo Markdown con `tools/genera_pdf_one_pager.py` (weasyprint) — no repite texto a mano. Discrepancia declarada (LATITUD §6.1): el encargo asumía que el "informe" público vive en `docs/informe.md`; ese nombre chocó por normalización (T02) en `GEN2-FRONT-1` y el archivo real es `docs/guia-lectura-publica.md` (ver su nota de cierre, 23/sep). Todos los enlaces de este acto usan el nombre real.

**P4 · Tabla de piso y reto.** `tools/genera_tabla_piso.py` filtra `canon/catalogo-del-mexicano-v1_0.tsv` (1537 filas) a las dos etiquetas de `estado_adopcion` que representan adopción real (`ADOPTADO-POR-FIRMA` + `CONSUMO-GEN2-ACTIVO`): **72 filas**, verificado con `csv.DictReader` (no awk, §2) y contra `N_resultados_gen2_adoptados_activos=72` de `corrida0.py status` — dos fuentes independientes, mismo número. Escribe `canon/tabla-de-piso-v1_0.tsv`. `docs/reto.md` publica las reglas (ΔMAE con IC por réplica, umbral fijado antes de abrir el dato, vocabulario B-bis exacto de instrucciones §4), a quién se invita por escrito (Toluna, ThinkNow, Matria/Celestial, YouGov) y cómo se recibe una spec (PR, recibo, sin promesa de adopción). Hallazgo honesto declarado ahí mismo: de las 5 áreas de consulta del catálogo, **Ingreso y gasto no tiene ninguna fila adoptada** en este corte — sellada sólo como contexto.

**P2 · Deck de diez láminas.** `tools/genera_deck.py` genera `docs/deck/01..10-*.md` (Jekyll, con navegación prev/siguiente) y `docs/deck.pptx` desde la misma fuente de datos en el propio script — evita mantener el contenido dos veces. Lámina 6 ("dónde ganan los otros") usa el informe de competencia de dirección (`forense/encargos/fuentes/INFORME-COMPETENCIA-2026-09-23.md`, 23/sep, 33 actores revisados), citando a los tres competidores más cercanos y dónde ganan cada uno — sin inflar ni minimizar. Lámina 3 (corroboración externa) cita los dos arXiv ya usados por el informe v1.3-ANEXO (2608.28615, 2609.07305), aclarando que no son evidencia sobre México.

**P3 · Verificación de un tercero.** Detalle completo en `forense/notas/2026-09-24-GEN2-FRONT-2-verificacion-tercero.md`. Resumen: clon local limpio (HEAD `02eadbc6`, luego re-sincronizado), sin contexto de esta sesión, siguiendo únicamente `docs/verificar.md` como estaba. `status` reprodujo el README dígito a dígito; `sha256sum` de un CALC citado coincidió exactamente con lo declarado en su `sello.json`/`sello.sha256`; `verify` llegó honestamente a `[3/5 INPUT AUSENTE]` sin corpus, pero **halló un defecto real**: sin correr `pip install -r requirements.txt` primero, `[5/5 RESULT]` falla antes por `ModuleNotFoundError` (numpy/pandas), un `NO-EJECUTABLE` distinto del de corpus ausente y que `docs/verificar.md` no distinguía. Se corrigió `docs/verificar.md` con esa distinción y el comando correcto (`pip install -r requirements.txt`). **Autocorrección 25/sep:** la redacción original de esta nota y de `NC-260924-GEN2-FRONT-2-d095-01` decía erróneamente que `requirements.txt` no declaraba esos paquetes — sí los declara (sección ASTRA5-U3-POLITICA); fue un error de lectura propia (`head -20` en vez del archivo completo), ya corregido y con la NC cerrada en el mismo acto. El manifiesto de 344 sellos se confirmó sin `.ots` en este corte, tal como `docs/sello-externo.md` ya declaraba (mecanismo (c), firma GPG).

## Latitud usada (declarada, LATITUD §6.1-3)

1. `docs/informe.md` → `docs/guia-lectura-publica.md` (nombre real, ya resuelto por T02 en otro acto).
2. Rama = la que la plataforma ya tenía abierta (`claude/new-session-punbef`), no `acto/gen2-front-2`.
3. PDF y `.pptx` **sí se generaron por comando real** (weasyprint, python-pptx vía PyPI): la restricción de red genérica del hook de arranque (`red: DENEGADA-POR-POLITICA`) no cubre el registro de paquetes de Python — se midió con `pip install --dry-run` antes de asumir que hacía falta una alternativa sin PDF/pptx (§2: la restricción se mide antes de diseñar alrededor).

## Verificación de existencia (re-confirmada, §6)

`ls docs | grep -c 'one-pager\|deck\|reto'` → 0 y `ls canon | grep -c tabla-de-piso` → 0 al abrir (igual que declaraba el encargo §4); los cuatro artefactos no existían.

## Suite

`tests/test_frente_publico_2.py` (nuevo): corre de verdad cada `<!-- deriva: ... -->` de `docs/one-pager.md` y `docs/reto.md`, compara `canon/tabla-de-piso-v1_0.tsv` contra una re-derivación en vivo, y verifica la cita textual del ΔMAE del piloto 3. Se cachea `corrida0.py status` una sola corrida por proceso (evita pagar ~70s cuatro veces). `tests/test_enlaces_archivo.py`: `PUBLICOS` ampliada con los cuatro artefactos nuevos y sus diez láminas — 0 enlaces rotos.

**Defecto propio encontrado y corregido en este mismo acto** (D-21, ≤10 líneas): el sidecar `forense/encargos/2026-09-24-GEN2-FRONT-2.md.cuerpo.sha256` del propio 0-bis citaba la ruta completa en vez del basename; `verifica_sidecars.py` lo marcaba `NO-CASA`. Se regeneró desde `forense/encargos/` (mismo hash, sólo cambia cómo se cita el nombre) — `check.py --rapido` pasó de 1 FAIL a 0 FAIL.

`python3 tests/check.py --baseline` sobre el clon de verificación, commit `44320625` (`origin/main` había avanzado 8 commits mientras corría esta corrida, todos de `GEN2-TUBERIA-TABLERO-EN-CANAL-1`/`VISTA-NORMALIZADA-4`, ninguno toca `canon/catalogo-*`, `corpus/reports/` ni `data/corrida0/`; se fusionó `origin/main` después, sin conflicto, y `tools/genera_tabla_piso.py` re-confirmó 72 filas y `check.py --rapido` 0 FAIL sobre el árbol ya fusionado):

```
3 FAIL · 67884 WARN
LÍNEA BASE: VERDE — sin FAIL nuevos frente a tests/baseline.json (HEAD congelado 7100cd0317132b1f4513b2efdc04058fd7ae89a2)
WARN NUEVOS: 117 (T03, todos en archivos anteriores a este acto — ninguno en docs/one-pager.md, docs/deck/, docs/reto.md, canon/tabla-de-piso-v1_0.tsv ni tools/genera_*)
```

Los 3 FAIL (`T06` ×2, `T08` ×1) son deuda ya aceptada y documentada en el propio código de la suite (`FP-293`, "Sigue FAIL declarado (deuda aceptada, no re-analizada)"); no los toca ni los agrava este acto.

**Segundo defecto propio, encontrado por el CI de PR #1126 y corregido (D-21):** el job `guardias` falló con `FALLA: tests sin fila en el censo (nacieron huerfanos): test_frente_publico_2` — `tests/test_frente_publico_2.py` no estaba cableado en `forense/analisis/ci-guardias/censo-tests.tsv`. `python3 tools/ci_guardias.py --censo` lo regeneró (232 archivos, 48 cableados hoy, 184 huérfanos — cifras del censo completo, no de este acto); `check.py --rapido` sigue en 0 FAIL después.

## NO-CORRIDO / RESERVAS

- Pages y DOI/Zenodo: `DECISIÓN-DE-MESA-PENDIENTE` bajo `FP-260923-GEN2-FRONT-1-4296-01` (re-verificada ABIERTA, A.17, antes de heredarla). Impacto: los cuatro artefactos quedan listos en `docs/`/`canon/` para servir en cuanto se active Pages (`Settings → Pages → main/docs`, ya preparado por `GEN2-FRONT-1`); mientras tanto se leen directamente en GitHub o desde el clon (`docs/one-pager.pdf`, `docs/deck.pptx` se pueden descargar y abrir sin Pages). Sucesor: `FIRMAS-16` (ya designado por `GEN2-FRONT-1` §10).
- `NC-260924-GEN2-FRONT-2-d095-01`: autocorregida y **CERRADA** en el mismo acto (25/sep). El hallazgo original decía que `requirements.txt` no declaraba `numpy`/`pandas` — es falso, sí los declara; el hallazgo correcto y ya resuelto es que `docs/verificar.md` no decía que `verify` necesita `pip install -r requirements.txt` primero. Nada queda pendiente sobre esto.
- Reto público: cero entregas todavía (se acaba de publicar). Sucesor: `FRONT-3`, ya designado por el propio encargo §10, "con lo que el reto reciba".

## CONSUMIDO

`forense/encargos/2026-09-24-GEN2-FRONT-2.md`, verbatim, sello en `forense/encargos/2026-09-24-GEN2-FRONT-2.md.cuerpo.sha256`. PR: **#1126** (`https://github.com/Josanoforo/Modelado-Mexicano/pull/1126`, rama `claude/new-session-punbef`). Pages, Zenodo y la fusión corresponden a mesa.
