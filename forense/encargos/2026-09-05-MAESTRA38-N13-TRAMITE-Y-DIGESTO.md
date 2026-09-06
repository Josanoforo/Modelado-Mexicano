# A.3 retroactivo · `ACTO MAESTRA38-N13 · TRAMITE-Y-DIGESTO` — archivado 5/sep/2026 por `MAESTRA38-A2-bis` (P0)

## Advertencia de origen — declarada antes de archivar nada

Este archivo NO es un A.3 verbatim en el sentido habitual del protocolo (archivar el texto del encargo tal como se pegó al invocar `/acto`). **No existe ningún encargo escrito para el fix que produjo `PR #547` / commit `432f4ea0`.**

Verificado contra el árbol real, per A.8/A.13:

- `git log 432f4ea0 -1` y `git show 432f4ea0 --stat`: el commit es `fix(digesto): cuenta filas ABIERTA con glosa, no solo igualdad exacta`, autor `Claude <noreply@anthropic.com>`, un solo archivo tocado (`tools/digesto_tramite.py`, +17/-3), fusionado a `main` como `PR #547` (`gh pr view 547`).
- El cuerpo del PR (`gh pr view 547 --json body`) es exactamente el cuerpo del commit — no cita ningún `forense/encargos/*.md`, ningún acto con rótulo `MAESTRA38-N13`, ninguna sesión previa con encargo propio.
- Búsqueda dedicada (`grep -rn "digesto_tramite\|N13" forense/encargos/`) no localizó ningún encargo anterior a este PR que describa el defecto o pida el fix.

**Conclusión, no fabricada:** este fue un fix hecho directamente sobre `main` (o una rama de corrección puntual) **fuera del protocolo `/acto`** — sin encargo previo, sin A.3, sin worktree propio documentado. La enmienda de dirección de `MAESTRA38-A2-bis` (5/sep/2026) le asigna retroactivamente el rótulo `MAESTRA38-N13` y pide su A.3 "con el texto de N13" — ese texto verbatim no existe y este documento no lo inventa. Lo que sigue es el registro honesto de lo que el commit real contiene, citado, no parafraseado como si fuera un encargo.

## Lo único que hay: el mensaje del commit, verbatim

```
fix(digesto): cuenta filas ABIERTA con glosa, no solo igualdad exacta

tools/digesto_tramite.py comparaba estado == "ABIERTA" con igualdad
estricta, ciego a filas como "ABIERTA -- pendiente de firma de mesa".
DIGESTO-2026-09-05 reportó 1 de 299 ABIERTA cuando por prefijo eran 5.
Se agrega _es_abierta() (ancla ^ABIERTA(\s|$)) y se usa en la sección A
y en el bloque de vencimientos.
```

`git show 432f4ea0 --stat`: `tools/digesto_tramite.py | 20 +++++++++++++++++---` — 1 archivo, 17 inserciones, 3 borrados.

## Qué NO hace este documento

No inventa un "encargo verbatim" de `N13`. No re-cuenta ni re-verifica el defecto que el commit dice haber corregido (fuera del perímetro de `MAESTRA38-A2-bis`, que no toca `tools/**`). No asigna P1 a este acto — P1 (el fix mismo) ya ocurrió, vía `PR #547`, fuera de `/acto`. No abre ningún hallazgo nuevo sobre la ausencia de protocolo — se anota como hallazgo en la nota de cierre de `MAESTRA38-A2-bis`, no aquí.

## CONSUMIDO

- **P1** (el fix `tools/digesto_tramite.py`, `_es_abierta()`): por `PR #547` / commit `432f4ea0`, fusionado a `main` como `b337fd7` (merge), 5-6/sep/2026 — fuera de `/acto`, sin A.3 previo. Este documento es el A.3 retroactivo, no el trabajo.
- **P2/P3** (cola por writer, tablero `FP-282`/`FP-308`): por `ACTO MAESTRA38-A2-bis` (este acto), P0, commit propio — ver `forense/notas/2026-09-05-MAESTRA38-A2-bis-*.md` para el detalle de qué filas se cerraron y con qué evidencia.

## Hallazgo declarado

El fix de `PR #547` corrigió un defecto real (`DIGESTO-2026-09-05` subcontaba filas `ABIERTA`) pero se hizo fuera del protocolo `/acto`: sin encargo archivado, sin A.3 previo, sin worktree propio verificable desde este árbol. Este A.3 retroactivo es la mejor reconstrucción posible con lo que el repositorio realmente tiene (el commit y el PR); no sustituye el encargo que nunca se escribió. Mesa decide si esto amerita un recordatorio de proceso o si el patrón (fix puntual sin `/acto` cuando el defecto es autocontenido en un solo archivo) se acepta como excepción documentada.
