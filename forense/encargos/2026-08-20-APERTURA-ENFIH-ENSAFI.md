ENCARGO APERTURA-ENFIH-ENSAFI · «la palanca más grande dormida del corpus»

SHA de redacción: no declarado por el encargo (a diferencia de AI-apertura-issp, que sí lo traía). Ancla derivada por esta sesión al arrancar: `origin/main` = `9f4ea60` (merge PR #298, LOTE-RETRIAGE) — es exactamente el gate que el encargo cita ("gate: LOTE-RETRIAGE fusionado"), verificado por `git fetch`+`git log origin/main` antes de tocar nada. Declarado como gap del encargo, no fabricado.

Entorno asignado: UBUNTU (explícito en el encargo). NO nube (explícito, 🚫). Modelo: Opus (explícito). Dueña única (explícito) — no se lanza en paralelo desde otra sesión.

Estado: `CONSUMIDO` — `PR #302` (rama `apertura-enfih-ensafi`), `ADR-134` (renumerado dos veces: `ADR-132`→`ADR-133` al fusionar con `PR #299`/`ACTO T-SELLO`, luego `ADR-133`→`ADR-134` al fusionar con `PR #301`/`ACTO LOTE-MOTOR2` — ver `forense/notas/2026-08-20-apertura-enfih-ensafi-cierre.md §6` y `§8`). Resultado: 0 de 8 celdas `EXISTE-SATISFACE`, `SIN-RUTA` con ruta `0 de 4` → `0 de 4`. `origin/main` se movió cuatro veces en total mientras este PR estuvo abierto: `PR #299` (`T-SELLO`, colisión real), `PR #300` (`DUELO-PREREG-V2`, sin colisión), `PR #301` (`LOTE-MOTOR2`, colisión real) — las tres fusionadas y resueltas en este mismo acto, `LÍNEA BASE: VERDE` en las tres pasadas de suite tras cada una. `PR #302` mergeable tras el último commit (verificar con `gh pr view 302` antes de fusionar — `origin/main` puede haberse movido de nuevo).

Archivado per forense/encargos/convencion.md (Regla A.3), commit propio, antes de T1 (COMMIT A).

---

Texto completo del encargo, tal como se lanzó (verbatim):

---

4 · APERTURA-ENFIH-ENSAFI — UBUNTU · Opus · gate: LOTE-RETRIAGE fusionado
ENTORNO: UBUNTU. NO nube.  Modelo: Opus.  🚫 --freeze.  Dueña única.
Ley de fondo: APERTURA v1.2 §3, verbatim — ya en canon tras T-SELLO.

Por qué importa. El plan maestro la llama «la palanca más grande dormida del corpus». Intacta desde el 12/ago.

ARRANQUE completo, tres partes, regla del grep. VERIFICACIÓN A.8. data/coef-universo-v1_0.tsv existe, 51 líneas (50 relaciones) — verificado. De ahí salen las celdas objetivo, no del censo β del plan viejo, que quedó superado.

T1 · COMMIT A antes de abrir un solo archivo: los términos de búsqueda pre-registrados, derivados de las necesidades del censo β — no de exploración libre. Codebooks primero, microdato después. T2 · Por celda objetivo: veredicto A.4 con variable_id nombrada, universo del instrumento y escala declarada → data/apertura-enfih-ensafi-v1_0.tsv. T3 · Si aparece reactivo que reabriría ADR-52A/54: NO reabres. Escribes la propuesta acotada con el reactivo exacto a la vista y abres fila — la reapertura es firma de mesa. T4 · Cierra: cuántos SIN-RUTA ganaron ruta (número dicho), fichas B-bis para lo medible ya.

Contador: «β con ruta: antes→después», los dos números derivados. PERÍMETRO. data/apertura-enfih-ensafi-v1_0.tsv · data/coef-universo-v1_0.tsv (solo columna de ruta) · fichas B-bis nuevas · tablero · gobernanza · estado-programa (cascada) · hallazgos · nota · encargo. Microdato solo lectura.

---

Nota de este acto sobre el texto de arriba, sin editarlo (verbatim preservado, según A.3): la premisa "Ley de fondo: APERTURA v1.2 §3, verbatim — ya en canon tras T-SELLO" se verificó contra el árbol antes de ejecutar (regla v2.1, "verificación de premisas antes de ejecución") y no se sostiene tal como está escrita. Detalle completo en la nota de este acto, §0.

## CONSUMIDO

Derivado por auditoría 2026-09-03 (ACTO MAESTRA37-N9 · AUDITA-ENCARGOS-166). `grep -Fc -- "2026-08-20-APERTURA-ENFIH-ENSAFI.md" canon/gobernanza-v1_15.md` → 1: citado bajo ADR-134 en canon/gobernanza-v1_15.md, con lenguaje de ejecución (archivado/ejecutado) en el bloque correspondiente. Marca ausente en el archivo era defecto de trámite, no evidencia de no-ejecución.
