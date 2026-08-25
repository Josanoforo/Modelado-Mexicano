# Nota de cierre — `ACTO SELLA-SORTEO-V2`

25/ago/2026. Propaga la firma de mesa sobre `FP-150`, sellando el reglamento del sorteo de `ACT-PIL-3` (`forense/prereg-duelo-v2/sorteo-act-pil-3-v2-PROPUESTA.md`) sobre las cifras post-`#345` que `ADR-175` ya re-derivó. Comando a comando.

## Arranque

1. **Repo**: clon existente en `/home/user/Modelado-Mexicano`, rama `claude/sella-sorteo-v2-firma-cn7hr9`. `git log -1` al arrancar: `769fa97 Merge pull request #350 from Josanoforo/claude/new-session-37oj2p`.
2. **SHA**: el encargo declaraba `c502a43`; `origin/main` había avanzado a `769fa97` (incluye el merge de `SELLA-A1-CODI`/`ADR-177`, `PR #350`). No es PARO — `c502a43` es ancestro de `HEAD`. Re-derivado en fresco: `FP-150` seguía `ABIERTA`, sha256 del reglamento coincidía exacto con el pin, `grep -ci "SELLAD"` → 0, máximo ADR vigente `ADR-177` (subió de `ADR-175` citado en el encargo) → nuevo ADR es `ADR-178`.
3. **data/raw**: ausente. Este acto no toca `data/` ni descarga nada — no se crea ni se enlaza, mismo patrón que precedentes ya registrados en `canon/estado-programa-v1_10.md` (p. ej. línea 234).
4. **Entorno**: `CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE=cloud_default`. Este acto no toca microdato ni red de datos — sonda saltada.
5. **Espejo**: ninguna cifra de este acto sale del espejo del proyecto; todas de comandos corridos en este clon.

## F0 — Compuertas

1. **Firma.** Mensaje de lanzamiento contenía `FIRMO FP-150: sello sorteo-v2 sobre cifras post-#345 (33/60=55.0% · 27/50=54.0%).` como línea propia — aceptada.
2. **Integridad del reglamento.** `sha256sum forense/prereg-duelo-v2/sorteo-act-pil-3-v2-PROPUESTA.md` → `92c017765820585e7ab2471e187f4cb7221d35ba59e3c215bef1b076bc487a79` — coincide exacto con el pin del encargo.
3. **A.8 en fresco.** `grep -n "FP-150" forense/firmas-pendientes.tsv` → fila `ABIERTA`, `ejecutada_en` vacía. `grep -ci "SELLAD" forense/prereg-duelo-v2/sorteo-act-pil-3-v2-PROPUESTA.md` → 0. Sin sello previo — se procede.

## F1 — Propagar la firma

1. `canon/gobernanza-v1_15.md`: `ADR-178` insertado tras `ADR-177` (candidateado contra el máximo re-derivado con la receta de la casa, sin huecos). Verbatim de mesa completo, qué sella (algoritmo §2-§2.3, cifras post-`#345`, discrepancia ya declarada por `ADR-175` citada no re-litigada) y qué NO sella (marco, sorteo real, Hito D). Cabecera y `§L0`/línea de suite de `estado-programa` recifradas 177→178 ADR.
2. `forense/prereg-duelo-v2/sorteo-act-pil-3-v2-PROPUESTA.md`: append al final, sección `## Sello de mesa — 25/ago/2026` — firma verbatim, referencia a `ADR-178`, pin sha256 verificado, línea sobre la semilla (SHA de merge del acto sucesor, §3). §0-§7 no se tocaron hacia atrás; el archivo no se renombró.
3. `forense/firmas-pendientes.tsv`: fila `FP-150` → `estado=FIRMADA`, `firmada_en`="2026-08-25, mesa, verbatim: ""FIRMO FP-150...""  -- ADR-178", `ejecutada_en`="2026-08-25, ACTO SELLA-SORTEO-V2: propaga la firma al reglamento...", `encargo`=`forense/encargos/2026-08-25-SELLA-SORTEO-V2.md`.

## F2 — Sincronía y cierre

- `canon/gobernanza-v1_15.md:2` (cabecera, 177→178 ADR).
- `canon/estado-programa-v1_10.md`: línea 27 (tabla de artefactos, 177→178 ADR), línea 105 (`L0 · Gobierno`, recifrado con nota fechada del acto), línea 210 y línea 302 (línea de suite y su duplicado — sentencia principal recifrada a 131 WARN, nota `ACTO SELLA-A1-CODI` recibe marca `{cita-historica}` por dejar de ser la entrada vigente).
- `README.md` fuera de perímetro — sin movimiento, declarado.
- Hito D sin movimiento (18 de 27).
- `forense/marco-candidatas-piloto-v1_0.tsv`, `milpa/`, `FP-133`, `data/`, `corpus/`, perímetro de Codex — ninguno tocado.

## Suite

Antes (antes de este acto, con `FP-150` recién pasada a `FIRMADA` en el tablero pero doc de `estado-programa` aún sin recifrar): `timeout 900 python3 tests/check.py --baseline` → `23 FAIL · 131 WARN` (T16 en rojo, 2 entradas: `canon/estado-programa-v1_10.md:210`/`:302` declaraban `132 WARN` vigente contra la corrida real `131`).

Después de recifrar `estado-programa` (incluida la marca `{cita-historica}` en la entrada superada de `ACTO SELLA-A1-CODI`): `timeout 900 python3 tests/check.py --baseline` → **19 FAIL · 131 WARN** (núcleo sin T16), **LÍNEA BASE: VERDE**, cero entradas nuevas frente a `tests/baseline.json`. Neto: **−1 WARN** — `FP-150` sale de `ABIERTA` y deja de imprimirse en `T22`, exactamente el neto esperado por el encargo. `FAIL` sin cambio en el núcleo (19); los 19 FAIL restantes (T09/T05/T02/T06/T08/T11) son pre-existentes, ajenos a este perímetro, verificados sin movimiento entre la corrida antes/después.

No se usó `--freeze` en ningún momento.

## Lo que este acto NO hizo

No congeló el marco de candidatas, no corrió el sorteo real, no movió Hito D, no tocó `FP-133`, `milpa/`, `data/`, `corpus/`, el perímetro de Codex, ni renombró el reglamento. Sucesor declarado: `CONGELA-SORTEA`.

**CONTADOR: cero**, declarado — ninguna cifra de medición sobre México se mueve; esta firma adjudica un reglamento ya redactado.
