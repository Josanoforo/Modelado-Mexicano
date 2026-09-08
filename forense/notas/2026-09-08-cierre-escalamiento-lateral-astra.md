# Nota de cierre · ACTO GEN2-SONDA-3 · ESCALAMIENTO-LATERAL

**Ruta del 0-bis:** `forense/encargos/2026-09-08-GEN2-SONDA-3-ESCALAMIENTO-LATERAL.md`.

**Encargo del piloto y su compuerta:** `forense/encargos/cola/2026-09-08-GEN2-SONDA-3-PILOTO-CAJA.md` — `GATED a GEN2-SONDA-3 · ESCALAMIENTO-LATERAL`, verificable por producto contra `origin/main` (presencia de `§5-bis · Segunda pasada crítica` en `.claude/commands/sonda.md`).

**Perímetro efectivo y diferencias contra la propuesta original de Astra (ChatGPT):**

1. **Deep Research a procedencia (3).** La propuesta original citaba dos estudios Deep Research como insumo. No están en el repo (`grep -rc "Deep Research"` → `0` sobre las notas de `SONDA-CAJA-1`/`SONDA-2`) y no fueron adjuntados al lanzamiento de este acto. Se ejecutó P4 con la lista de supuestos autocontenida de la propuesta (§8 del encargo) — no se buscó fuera del repo ni se reconstruyó de memoria.
2. **Piloto a sucesor.** La propuesta original (§9) trataba la validación como parte del mismo acto. Este acto la deja como sucesor GATEADO — el piloto ejercita el criterio nuevo contra un negativo material real, y requiere entorno CAJA con red, distinto del entorno NUBE de este acto.
3. **Fichaje P0.** La propuesta original no incluía un paso explícito de fichar antes de editar. Este acto lo añade como P0, rompiendo el patrón de los dos actos previos del linaje (`#632`, `#635`), que corrieron sin fichar primero.

**Estado real: preparado.** El criterio nuevo (`sonda.md §5-bis`/`§8`, `adquiere.md §6-bis`) está escrito, `tests/check.py --baseline` en VERDE, y el encargo sucesor está en la cola — pero sin ejercitarse todavía contra un negativo material real (`NC-0060`, `DIFERIDO-A:GEN2-SONDA-3-PILOTO-CAJA`). Preparación no se presenta como ejecución; ejecución no se presenta como adopción — el piloto es quien produce evidencia de que el criterio funciona, no este acto.
