# E5-0 · ACTO GEN2-E5-0 · SPECS EJECUTABLES

- **SHA de redacción (base del encargo):** `df9336c5` (reencolado por `ACTO GEN2-V213`, 8/sep/2026). **SHA de ejecución:** `origin/main = d8b5f0b` (113 commits después; `df9336c5` es ancestro — verificado con `git merge-base --is-ancestor`, main avanzó, no divergió).
- **Entorno asignado:** UBUNTU (caja), worktree nuevo desde `origin/main`, Opus. **NO se lanza en NUBE** (lo dice el propio cuerpo).
- **Estado:** VIVO.


## E5-0 · ACTO GEN2-E5-0 · SPECS EJECUTABLES — códigos y ponderadores desde metadato; congelar `spec.yaml`

Cabecera: **UBUNTU (caja)**, worktree nuevo desde `origin/main` · **Opus** · COMPUERTA por producto: E7 fusionado con `GO-MARCADOR` en su nota (`git show origin/main:forense/notas/<nota-E7> | grep -c GO-MARCADOR` ≥ 1); `python3 tools/limpia_arbol.py --reporta` sin árboles ni ramas fuera de política; gates de spec en `main`: S12 `870522a3…`, S13 `c41235b8…`, S6 v1.2 `c1cd3b63…` (íntegros del sidecar). NO se lanza en NUBE.
Principio (E.5 de v2.13): «spec conceptual pre-registrada → abrir **solo** codebook/metadato → resolver códigos y ponderador → congelar `spec.yaml` → COMMIT-1 → (E5) abrir microdato → calcular». **Termina en el COMMIT-1; no abre microdato ni calcula.** Adivinar códigos para lograr un `preflight` VERDE está prohibido.
**CALC-0001 / S12 (CIDE-CSES 2015).** Codebook y metadatos del `.sav` (etiquetas y códigos, sin valores): `pcyc13`, `pcyc14`, `pvoto1/2/3`, desenlace §2, ponderador. Si el desenlace no existe con esos códigos → `NO-CONSTRUIBLE` declarado (outputs `null` solo en ese brazo). `spec.yaml` (D-15), `spec-check` y `preflight` VERDE, COMMIT-1.
**CALC-0002 / S13 (LAPOP 2019/2021/2023, R10.3).** **No se convierte ausencia de desenlace en veredicto D2-h.** (a) Confirmar en los codebooks de las tres olas si existe desenlace comparable al de la corrida 2004 (leer en la nota de LOTE-LAPOP cuál usó); (b) si existe: escribir **S13 v1.1** (md + sidecar, antes de cualquier microdato) y `spec.yaml` contra v1.1; (c) si no: `spec.yaml` contra v1.0 con `veredicto_D2h: NO-CONSTRUIBLE` y solo outputs descriptivos pre-registrados. Las dos rutas están autorizadas; el acto reporta cuál y por qué, con codebook citado.
**CALC-0003 / S6 v1.2 (ENNViH 2002).** Riesgo técnico: `seed {aplica: true, valor, rng}`, `dependencias_materiales: [zipfile-deflate64, …]`, `ponderador` por brazo (`fac_3b`; `fac_3b_px` y `fac_3a_px` en pareja), rutas de los ocho `.dta` por `resolver_payload`, ventanas de `es09`/`ce01` leídas de `ennvih1_2002_hogar_q` y citadas con página **en el yaml**, outputs con tipo/unidad y `NO-ESTIMABLE` permitido por celda. `spec-check` y `preflight` VERDE, COMMIT-1.
Común: un COMMIT-1 por CALC con «el primer resultado que produzca este procedimiento es el que se reporta»; sidecars; nota con codebooks abiertos (id de manifiesto, página) y **ningún número**. Cierre A.14; rama fusionada o borrada.
Perímetro: `data/corrida0/CALC-000{1,2,3}/spec.yaml` (+ `spec.md` local citando la spec sellada) · `forense/prereg-caja/S13-R10-3-spec-v1_1.md` + sidecar (solo ruta b) · `forense/notas/` (1) · `forense/firmas-pendientes.tsv` (recibo) · cascada. **No toca microdato, `tramite.yaml`, canon ni S12/S6.** Si te encuentras escribiendo fuera de esta lista, PARA.
Contador: cero; tres CALC en `PRE-FLIGHT-VERDE`.
