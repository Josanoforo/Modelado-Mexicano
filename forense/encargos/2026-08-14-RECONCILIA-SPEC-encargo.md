- **SHA de redacción:** `2f2125c` (`origin/main` — HEAD exacto en el momento de arranque de esta sesión; es el merge de `#235`/`prod-p638` que el propio encargo exige como GATE, y también incluye `d653ab9`/PR#230 como ancestro — ADR-82 ya estaba sellado en ese terreno. Confirmado contra el clon de esta sesión, no supuesto).
- **Entorno asignado:** repo-only — el propio encargo lo declara equivalente para nube o caja (no abre microdato, no escribe `data/raw`). Asignación explícita para esta ejecución: **E2 → Sonnet, nube, HOY**. Ejecutado en nube (`CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE=cloud_default`, sin sonda de red, sin `data/raw` — firma correcta de acto de nube, ver nota).
- **Estado:** CONSUMIDO — PR #238 (rama `claude/encargo-3-reconcilia-specs-kecktd`). *(Re-verificado 17/ago/2026, ACTO E-HIG/HIGIENE-VIVOS, contra `f3873c2`: `git merge-base --is-ancestor 8925588 f3873c2` OK.)*

---

═══ VERIFICACIÓN DE EXISTENCIA — la contesta quien archiva el encargo [Bloque D-ter/A.8, v2.8] ═══

El texto recibido no traía este bloque (probable desfase de versión de quien lo redactó, mismo patrón que A.9 ya documentó para otro caso). Se completa aquí, por quien ejecuta y archiva, con verificación real — no se para por su ausencia porque el propio encargo ya trae premisas verificables por comando y este bloque pide exactamente eso.

**1 · ESTRUCTURA.** Tablas que gobiernan este dominio, derivado de `data/INFRAESTRUCTURA-v1_0.md:90-103` (no de memoria): `especificaciones-produccion.json` — **SIN VÍA de script, A MANO** (precedente `59d6c40`; ningún script en `tools/curador_registro/` tiene un `write` sobre este archivo) y `produccion-modelo.tsv` — escrita solo por `integrate_production.py --output`. Este encargo escribe **solo** la primera, a mano, por el cauce ya documentado como correcto para ese archivo. No escribe la segunda (ya está bien, ver Commit 1). No escribe ningún archivo de `tools/**` ni `canon/**` — declarado y respetado.

**2 · CONTENIDO.** Comando y salida cruda que muestran que la propagación NO existe todavía (no es una clasificación de "no existe fuente" — es la ausencia verificada del propio fix):

```
$ grep -n '"requiere_decision": "SI"' data/curacion-registro/especificaciones-produccion.json
61:      "supervisor_link": {"relacion_id": "REL-fe202a3fa76f0516a6e27f8b", "objeto_modelo_origen": "G5.familismo_obligacion", "requiere_decision": "SI"}
106:      "supervisor_link": {"relacion_id": "REL-5741e12ce3e0a0e076ee48fc", "objeto_modelo_origen": "G5.radio_confianza", "requiere_decision": "SI"}
```

Dos specs (`ESP-OPACA-B-d13ec4fe`, `ESP-OPACA-C-9ecb5c61`) con `requiere_decision: "SI"` pese a que sus ADR gobernantes (75(a), 82) ya sellaron. Detalle completo, con el intento real de `--validate-existing` en esta nube y por qué no llega a ese punto, en la nota.

**3 · COBERTURA RETROACTIVA.** `especificaciones-produccion.json` nace (para A/B/C) antes del 11/ago/2026 y su único cambio posterior es `57a730b` (13/ago, inserción pura de `ESP-OPACA-D`, cero ediciones a B/C — ver mapa). ADR-75(a) sella 13/ago/2026, ADR-82 sella 14/ago/2026 — **ambos posteriores a la última vez que alguien escribió este campo**. La tabla gobernante (el propio archivo) es más vieja que las dos decisiones que debía propagar: su atraso no es un defecto de proceso nuevo, es la consecuencia mecánica de que nadie volvió a tocar un archivo "SIN VÍA, A MANO" después de que la mesa selló. Confirma que el trabajo de este encargo no está ya hecho, en ningún grado.

════════════════════════════════════════════════════════════════════

ENTORNO ASIGNADO — y el que NO: nube, HOY (E2). No se lanza como acto de caja — no lo necesita (repo-only, sin microdato).

PERÍMETRO Y CONCURRENCIA: ver PERÍMETRO dentro del texto del encargo, abajo. Concurrencia verificada al arranque: `git branch -r` → solo `origin/enlace-2` además de `main` y esta rama; `enlace-2` toca `relaciones.tsv` (ajeno a este perímetro). Sin colisión. Si te encuentras escribiendo fuera de la lista del PERÍMETRO, PARA — el perímetro estaba mal calculado y saberlo vale más que el atajo.

════════════════════════════════════════════════════════════════════

Texto completo del encargo, tal como se lanzó (verbatim):

---

ENCARGO 3 · ACTO RECONCILIA-SPEC — el hallazgo §2.5 de #235, cerrado (repo-only, nube o caja · dos commits + A.3 · GATE: #235 FUSIONADO — preservó las 9 filas que este acto toca)
Qué es: propagación de decisiones YA selladas (ADR-75(a) resolvió la reserva de `norma_de_género`; ADR-82 adjudicó `radio`) hacia los specs que dos actos dejaron atrás al parchar la tabla a mano. Cero firmas nuevas de mesa — por eso va completo y sin ranuras.
PREMISAS (script — cada una del hallazgo de #235, re-derivada):
bash

```bash
set -u; cd "$(git rev-parse --show-toplevel)"; git fetch -q origin
git merge-base --is-ancestor pr/235 origin/main && echo GATE-OK || { echo "ESPERA: #235 sin fusionar"; exit 1; }
python3 tools/curador_registro/integrate_production.py --config data/curacion-registro/especificaciones-produccion.json --validate-existing 2>&1 | tail -3   # esperado: FALLA por la deriva B/radio — pega la salida cruda; si pasa, YA HECHO: PARA
grep -n '"requiere_decision": "SI"' data/curacion-registro/especificaciones-produccion.json | head -4        # las specs desfasadas — reporta cuáles
sed -n '115,120p' data/curacion-registro/celdas-d/G5.familismo_obligacion.actitud.yaml                        # la afirmación falsa de :118-119, verbatim a la nota
```

PERÍMETRO: `especificaciones-produccion.json` (SOLO `supervisor_link.requiere_decision` y los campos que la deriva nombre, por spec, citando su ADR) · la celda `G5.familismo_obligacion.actitud.yaml` (SOLO añadir el campo de corrección — la afirmación de `:118-119` NO se borra: se le añade debajo `correccion_2026-08-14:` con "la afirmación anterior era falsa; la spec no se actualizó en ACTO RES — evidencia: git log de `especificaciones-produccion.json` entre `fb4bade` y `HEAD`; corregida por este acto citando ADR-75(a)") · nota · A.3 · hallazgos (union) · fila nueva en `forense/firmas-pendientes.tsv` SOLO si el mapa encuentra algo que sí exija mesa (no se espera). NO toca: `produccion-modelo.tsv` (la tabla YA está bien — refleja lo sellado; el que estaba atrás era el spec) · `tools/**` · `canon/**`.
Commit 1 — el mapa: las 9 filas preservadas por #235, una por una: qué dice la tabla · qué dice su spec · qué ADR sellado gobierna (75(a) para B; 82 para radio; el resto sin deriva se declara `SIN-CAMBIO`) · el edit exacto. La evidencia git de la afirmación falsa, pegada. Frase de siempre. Commit 2 — la reconciliación: los edits del mapa → criterio de cierre: `--validate-existing` PASA en verde (pega la salida) → suite `--baseline` cruda → nota cierra con: "deriva spec↔tabla: 0; la afirmación falsa, corregida con evidencia; contadores tocados: 0 — esto es higiene, y lo dice."
Dónde corre cada uno: E1 → ChatGPT diseña, Codex ejecuta (caja) · E2 → Sonnet, nube, HOY (es el que mata tu problema para siempre: tras él, cada corrida de suite te imprime tus firmas pendientes con días de antigüedad) · E3 → Sonnet, nube o caja, al fusionar #235. Ninguno choca con ENLACE-2, PROD-P638 ni el sello del motor. Y una fila que E2 va a cosechar de inmediato: las seis firmas M del esqueleto — que dejarán de depender de tu memoria a partir de su primer WARN.
