# ACTO ADJ-4 — cuatro firmas de mesa en un solo acto

- **SHA de redacción:** `19d885d` (`origin/main`, merge PR #200 — HEAD de la rama antes de este acto).
- **Entorno asignado:** NUBE, repo-only, sin red (declarado por el propio encargo). NO en caja.
- **Estado:** `CONSUMIDO` — ejecutado en la rama `claude/acto-adj-4-firmas-mesa-0fig8f`, COMMIT 1 (las cuatro firmas y sus derivaciones propias) y COMMIT 2 (la propagación: contadores de `canon/estado-programa-v1_10.md`, cascada de FAIL/WARN, esta nota, este archivo, `forense/hallazgos.md`). PR aún no abierto en esta sesión — el registro es el commit, no el PR (mismo criterio que `forense/encargos/2026-08-13-adr-provisionalidad.md`). Detalle completo: `forense/notas/2026-08-13-adj4-cierre-firmas.md`.
- **Naturaleza:** acto de sellado. Mesa dicta las cuatro firmas en el propio texto de lanzamiento. El ejecutor propaga y deriva; no decide, no reescribe texto sellado, no amplía el alcance.

Archivado per `forense/encargos/convencion.md` (A.3).

---

Texto completo del encargo, tal como se lanzó (verbatim):

---

1 · ACTO ADJ-4 — cuatro firmas de mesa en un solo acto
Cierra D2(a) · D6 · D7 · D8 · Entorno: NUBE, repo-only, sin red · NO en caja
Por qué en un acto: las cuatro tocan `canon/` o `forense/` de raíz y chocarían entre sí si corrieran en paralelo. Mesa dicta las firmas en el texto de lanzamiento; el ejecutor propaga y deriva, no decide.
PERÍMETRO
ESCRIBE: `forense/registro-llaves-identificacion-v1_0.md` (append) · `forense/registro-recalculo-v1_0.md` (columna `estado` de las filas 0 y 1) · `canon/gobernanza-v1_15.md` (rótulo de cota + ADR nuevo si la receta lo pide) · `canon/estado-programa-v1_10.md` (contadores) · `tests/baseline.json` · `forense/encargos/2026-08-13-enlace1-mapeo-id-manifiesto.md` (solo la cita colgante) · nota · A.3 · hallazgos. NO ESCRIBE: `forense/hitoD-preregistro-v2_0.md` (el denominador 27 no se toca, ADR-67(c)) · `milpa/**` · `data/**` · `tools/**` · otros de `tests/`.
PREMISAS (script, crudas)
bash

```bash
set -u; cd "$(git rev-parse --show-toplevel)"
grep -c "EJERCIDA_" forense/registro-llaves-identificacion-v1_0.md          # crudo; si ya hay una, PARA
grep -oE '\*\*ADR-[0-9]+' canon/gobernanza-v1_15.md | grep -oE '[0-9]+' | sort -nu | tail -1
python3 tests/check.py --baseline 2>&1 | tail -4
```

COMMIT 1 — las cuatro firmas, verbatim, y las recetas derivadas ANTES de propagar
(a) Llave `R5.1-D2` → `EJERCIDA_INDECISA`, fila B. Firma de mesa: "Adjudico fila B, `EJERCIDA_INDECISA`." ⚠️ El transfer del 12-13/ago dice "fila A" en su titular y su propio cuerpo dice B. El repo confirma B: `forense/notas/2026-08-12-e4c-r5-1-d2-commit10-incertidumbre-razon.md` §4, verbatim, "No cambia la fila propuesta (B, `EJERCIDA_INDECISA`)". No firmes desde el transfer. El contador se mueve según la receta del propio `registro-llaves-identificacion` §4, no según este encargo ni la intuición. Cítala con línea. Esperado `0 de 2 → 1 de 2`; si la receta dice otra cosa, manda la receta.
(b) Rótulo de cota, adoptado. Firma: "Adopto el rótulo de MAP-A §7 verbatim." Propagar a `gobernanza:862` y a la línea del régimen, con estampa de universo (mecanismo + fecha del TSV de cota).
(c) Entradas 0 y 1 del registro de recálculo, cerradas. Entrada 1: el texto ya está propuesto, verbatim, en `forense/notas/2026-08-13-censo-v1_1-abrir4-enasem.md` §12. Cópialo, no lo reescribas. Veredicto `RECALCULADO — CAMBIA`, PR #198. Entrada 0 — y aquí hay una trampa que el censo v1.1 dejó nombrada y hay que respetar. Su §12 declara que NO propone cierre para la Entrada 0 porque "su alcance declarado es más ancho que el de este acto": el cotejo cubre las 15 filas del censo, y v1.1 solo mapeó las 9 `SIN-RUTA`. Cerrarla sin más sería una conclusión más ancha que su universo — exactamente lo que ADR-72 declara provisional. Por eso este acto hace el cotejo de las 12 filas restantes — es derivación de solo-lectura sobre `censo-v1_1` × `relaciones.tsv`, barata: por cada fila del censo, qué `necesidad_id` le corresponde y qué dice su `capa4_apertura_mapeo`. Con eso la Entrada 0 cierra honesta. Si el mapeo de alguna fila no es decidible por lectura, se dice cuál y la entrada cierra acotada a las que sí, con la razón escrita.
(d) Baseline: revertir a `e7cd99d`, y arreglar lo que destapa. Firma: "Se revierte el recongelado de ENLACE-1 commit 4." Verificado antes de escribir este encargo: con `e7cd99d` restaurado la suite da ROJO, 1 entrada nueva — `T03: forense/encargos/2026-08-13-enlace1-mapeo-id-manifiesto.md cita PLANENLACECAPA220260813.md, que no existe`. Es un defecto real y es propio de ENLACE-1, no drift heredado: su encargo cita entre backticks un documento que nunca entró al repo. Revertir y arreglar van en el mismo commit. El arreglo: quitar los backticks de esa cita (queda como texto plano, sin colgar) o archivar el documento si existe fuera del repo. No lo re-congeles. Al cerrar, `--baseline` debe volver a VERDE contra `e7cd99d`.
COMMIT 2 — la propagación
`tests/check.py --baseline` al cierre. T15 (ADR contiguos) y T18/T20 (contadores) vigilan. Reporta los contadores que NO se mueven, declarados: `13 de 27` · `9 de 14` · `0 de 15` · `capa2 SI 43`. Si un test truena, ese es el hallazgo — no se maquilla.
Contador: `llaves 0 → 1` · dos entradas del registro cerradas · un rótulo sellado · una línea base restituida con su defecto a la vista.

## CONSUMIDO

Derivado por auditoría 2026-09-03 (ACTO MAESTRA37-N9 · AUDITA-ENCARGOS-166). `git grep -Fl -- "2026-08-13-adj4-firmas-mesa.md"` (excluyendo forense/digesto/) cita nota(s) de cierre: forense/notas/2026-08-13-adj4-cierre-firmas.md. Encargo pre-ADR-por-archivo (anterior al 18/ago/2026): la evidencia de ejecución vive en la nota de cierre, no en canon/gobernanza-v1_15.md. Marca ausente era defecto de trámite retroactivo, resuelto por esta auditoría.
