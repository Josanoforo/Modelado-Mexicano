- **SHA de redacción:** `3e071f0` (merge de #175, `origin/main`, 12/ago/2026 — mismo multi-encargo que `2026-08-12-M6-sello.md`, ver ahí para el ARRANQUE compartido y el resto del contexto)
- **Entorno asignado:** cualquiera con el repo (no toca microdato ni red)
- **Estado:** CONSUMIDO — rama `claude/cuatro-decisiones-firmadas-9z54wq` (encargo pedía `mesa/v-vocabulario-celda-d`; misma desviación declarada de rama que `2026-08-12-M6-sello.md`)

---

ACTO V · VOCABULARIO CELDA-D — dos campos, sin cajón de sastre
ARRANCA DESPUÉS DE QUE M-6 FUSIONE. Cita el ADR ya en `main`, no en vuelo.
ENTORNO: cualquiera con repo. No toca microdato ni red — dilo y salta el punto 4.
PERÍMETRO. SOLO: `propuesta-motor-adaptativo-celda-v0_4.md` (archivo nuevo; `v0_3` no se edita, gana un banner de una línea que apunta a v0.4) · `data/curacion-registro/celdas-d/G5.familismo_obligacion.actitud.yaml` · `data/curacion-registro/celdas-d/G5.radio_confianza.encuci_vs_enbiare.yaml` · `forense/notas/` (1 nota) · `forense/hallazgos.md` · `forense/encargos/`. NO toca `tools/`, `tests/`, `canon/`, `milpa/`.
PASO 1 · Premisas
```bash
grep -c "ADR-NN" canon/gobernanza-v1_15.md          # ≥1 — M-6 ya fusionó
grep -n "fuerza" propuesta-motor-adaptativo-celda-v0_3.md | head -3
grep -n "fuerza:" data/curacion-registro/celdas-d/*.yaml     # esperado: 2, ambos fuera del enum
grep -rln "celdas-d" tools/ tests/ --include=*.py            # esperado: vacío — nada valida en código
```
Si algo en código sí valida los YAML, PARA: el costo del acto cambia y ADR-68(a) vuelve a aplicar.
PASO 2 · v0.4 — el campo se parte en dos, porque son dos objetos
En `propuesta-motor-adaptativo-celda-v0_4.md`, §3, sustituye `fuerza` por:

1. `fuerza_coeficiente` — enum cerrado, sin cambios: `ASIGNADO | AJUSTADO | IDENTIFICADO`. Describe el coeficiente de `milpa/procedencia.yaml` que la condicional alimenta, no la condicional. Para `radio_confianza` el valor es `ASIGNADO` y la propia celda ya lo dice.
2. `procedencia_condicional` — vocabulario extensible, que describe lo que la celda realmente compara. Conjunto inicial, derivado de los dos casos reales y de ningún otro lado: `MEDICION_DIRECTA_MICRODATO` · `MEDICION_CONDICIONAL_MICRODATO` · `PROXY_PARCIAL` · `SIN_ESTIMACION_TODAVIA`.

Reglas del vocabulario extensible, escritas en v0.4:

* No contiene, ni contendrá, un valor de "otro" / "no especificado" / "no determinado" como miembro. Un vocabulario extensible con comodín es de facto cerrado y esconde la señal — es la razón declarada, con su fuente (FHIR/openEHR), en ADR-NN(d).
* Un valor fuera del conjunto se admite solo con: razón escrita en el propio YAML y el valor más cercano del conjunto, o `sin_equivalente_canonico: true` explícito.
* Cada celda declara la versión del vocabulario que usó (`vocabulario_version: 0.4`). Los conjuntos cerrados se citan por versión, no por nombre.
* Falsador y caducidad (v2.3): si en tres meses ninguna celda nueva necesita un valor fuera del conjunto, el vocabulario se declara suficiente y `procedencia_condicional` pasa a cerrado. Si tres celdas nuevas necesitan valores distintos fuera del conjunto, el vocabulario está mal cortado y se rediseña — no se parcha con miembros sueltos.

PASO 3 · Reescribir las dos celdas — sin perder una sola palabra de las reservas

* `familismo_obligacion.actitud`: `fuerza: NO_DETERMINADO` → `fuerza_coeficiente:` el valor que corresponda al coeficiente que alimenta (derívalo de `milpa/procedencia.yaml`, no lo teclees; si no hay coeficiente todavía, `sin_coeficiente_asociado: true` con la razón) + `procedencia_condicional: SIN_ESTIMACION_TODAVIA`.
* `radio_confianza`: `fuerza: "MEDIDO·PARCIAL(x)"` → `fuerza_coeficiente: ASIGNADO` (la celda ya lo argumenta: `radio_confianza=0.15`, `milpa/procedencia.yaml:629`, "magnitud: asignada" — verifícalo contra el archivo) + `procedencia_condicional: MEDICION_CONDICIONAL_MICRODATO`.
* Los comentarios de reserva de ambas celdas se conservan verbatim, con una línea nueva que diga qué versión del vocabulario resolvió cada uno. Fueron el mecanismo que detectó el defecto; borrarlos borraría la evidencia.

PASO 4 · Cierre
7 líneas · `--baseline` cruda · PR `mesa/v-vocabulario-celda-d`, NO FUSIONAR. Contadores de medición: 0 — este acto evita paros falsos en E0, no mide.

---

**Nota de ejecución (no parte del encargo original, añadida al archivar):** el PASO 1 de arriba usa el placeholder `ADR-NN`, escrito antes de que `ACTO M-6` derivara el número real (`ADR-71`, ver `2026-08-12-M6-sello.md`). Al ejecutar, `grep -c "ADR-NN"` se corrió como `grep -c "ADR-71"`, y las dos referencias a `ADR-NN(d)` de este texto se resolvieron como `ADR-71(d)` en los artefactos producidos. Además, `grep -rln "celdas-d" tools/ tests/ --include=*.py` del PASO 1 ya NO dio vacío al ejecutar este acto (`tests/test_celdas_d.py` llegó vía PR #177 después de que este encargo se escribiera) — el PARO de PASO 1 se consultó con mesa antes de proceder; ver `forense/hallazgos.md` y `forense/notas/2026-08-12-acto-v-vocabulario-celda-d.md` para la resolución completa.

## INDETERMINADO

Derivado por auditoría 2026-09-03 (ACTO MAESTRA37-N9 · AUDITA-ENCARGOS-166). `grep -Fc -- "2026-08-12-V-vocabulario-celda-d.md" canon/gobernanza-v1_15.md` → 0 (sin cita en ningún ADR). Rastro fuera de gobernanza, sin nota de cierre propia: tests/check.py. Insuficiente para CONSUMIDO, insuficiente para NO-EJECUTADO — rótulo/evidencia parcial, se lista para mesa.
