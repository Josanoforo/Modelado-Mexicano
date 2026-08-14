# ENCARGO B2 · mantenimiento acotado de la vía bajo la ventana ADR-70(d)

- **SHA de redacción:** `8925588` (`origin/main`, post-#238). El plan de remediación que lo origina se adjudicó contra `cf0dd68` (post-#236).
- **Entorno asignado:** caja, con corpus montado. Sin red — declarado, sonda saltada.
- **Estado:** CONSUMIDO — ejecutado en `forense/notas/2026-08-14-acto-b2-via-capa3.md`, con **(a) y (c) ejecutados y (b) en PARO** por medición que no sostiene su premisa (ver §(b) de `ADR-84`).

## Bloque VERIFICACIÓN DE EXISTENCIA (A.8, Parte 2 — contestado por quien ejecuta)

- **Estructura — qué gobierna este dominio, derivado del árbol:** `tools/curador_registro/via_capa2.py` es el único escritor de `capa2_manifiesto` en todo el repo (`grep -rn "capa2" tools/ tests/` daba 0 resultados antes de ACTO V2, y hoy solo la vía y sus pruebas); `tests/check.py` es la suite gobernante y su registro de pruebas vive en `main()`; `tools/curador_registro/tests/test_via_capa2.py` es la única prueba unitaria de la vía. **Ninguna herramienta nueva se crea.**
- **Contenido — qué hay ya escrito sobre lo que el encargo pide:** el precedente exacto de mantenimiento bajo esta misma ventana y sobre este mismo archivo es `ADR-73` (ENCARGO B · ALIAS-P + MOTOR-DIAG). El defecto que (a) repara lo midió ENLACE-2 (PR #236) y el costo de no repararlo lo documenta CAPA3-RECONCILIA (PR #202). **Este encargo no reabre ninguno de los tres: los consume.**
- **Cobertura retroactiva:** antes de este acto, `grep -c "capa2\|capa3" tests/check.py` = **0**. Cero cobertura de suite sobre las dos columnas, verificado, que es la razón por la que el defecto pudo vivir callado.

## Texto de la firma de mesa, verbatim

> "B1: SELLADO — mantenimiento acotado de la vía bajo la ventana ADR-70(d), lista CERRADA de tres: (a) via_capa2.py escribe capa3 al promover solo con estado COINCIDE; (b) bootstrap.py::derive_evidence_state deja de casar NO_REFERENCIADO por subcadena; (c) test nuevo que cubra capa2/capa3 en check.py y test_via_capa2.py — hoy cero cobertura, por eso el defecto vivió callado. Nada más entra bajo este sello. El ADR lo redacta el acto B2 con número por T15."

## Contexto de la firma, verbatim del plan adjudicado (§2 y §3)

> El carril B tiene reloj (la ventana ADR-70(d) cierra cuando E0 registre su primera celda — todo mantenimiento de la vía entra antes).
>
> B2 corre con esa firma; su PR debe fusionar ANTES de que peguemos las seis firmas M — es el reloj del §3.
>
> El reloj: B2 fusiona → rama de E0 con compass/RT fusiona (la precondición del esqueleto muere) → pegas las seis firmas M → MOTOR-2/ADR (número por T15, hoy candidato 84 — se re-deriva al sellar) → la ventana ADR-70(d) CIERRA → E0 ejecuta completo. Ningún mantenimiento de la vía después de ese punto — por eso B2 va hoy.

**Nota de archivo.** El texto de mesa vive fuera del repo (conversación de dirección); se pega aquí íntegro por la convención de este directorio. El número de ADR **no se hereda de este documento**: el propio plan lo advierte (*"hoy candidato 84 — se re-deriva al sellar"*), y el acto lo derivó con la receta de T15 contra el `main` real antes de escribir el primer commit — 83 únicos, contiguos, sin huecos ⇒ **ADR-84**, que coincidió con el candidato sin heredarlo.
