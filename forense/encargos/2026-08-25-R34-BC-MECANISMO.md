# Encargo R34-BC-MECANISMO — medir las condiciones B y C del gate de R3.4 (base medida 0→2, ADR-37)

*(Archivado por el propio acto conforme a `A.3`. Texto verbatim del encargo recibido de dirección el 25/ago/2026; no se edita.)*

---

SHA de redacción: 2b7d787. Dirección, 25/ago/2026. ENTORNO: UBUNTU (abre microdato; la NUBE no tiene los bytes). No NUBE, no doble. FIRMA: ninguna nueva — este acto MIDE y PROPONE; el veredicto integrado A∧B∧C es acto posterior de mesa.

Qué son B y C, del canon y no de memoria. ADR-37 (gobernanza:267): el gate de R3.4 exige TRES condiciones — A reproducción (SELLADA: fila A1, ADR-177), B prueba de mecanismo, C anti-confusión. La explicación canónica del fracaso de CoDi es «riesgo fiscal percibido + fricción», no desconfianza (gobernanza:212, corrección del defecto S2 más antiguo del programa). Hoy B y C tienen base medida 0 de 2, ambas ASIGNADO. Este acto les da dato mexicano: B = evidencia de que la percepción de riesgo fiscal/vigilancia y la fricción están asociadas al no-uso de CoDi entre usuarios digitales; C = evidencia de que el canal de confianza personal (§3.1/G1a) NO explica esa brecha — la separación utilidad-vs-coerción que ADR-25 conflacionó.

════ ARRANQUE ════ 1·REPO. 2·SHA. 3·data/raw: sustantiva — enlaza al CORPUS COMPARTIDO y reporta. 4·ENTORNO tres partes (A.2): sin_variable · sonda INEGI cruda (nunca curl -I) · ls data/raw/; corpus no montado → PARO (asignación de entorno falló). 5·Cero cifras del espejo. Negativos con conteo (A.13). ════

═══ EXISTENCIA (dirección, contra 2b7d787) ═══ Base medida de B/C = 0 de 2 (estampa ASIGNADO del emisor; verbatim del tablero FP-104: «hoy 0 de 2, ambos ASIGNADOS»). Ningún abridor B/C existe: find forense -iname "*r34*b*"-clase → solo la ficha de la condición A y sus notas (universo: forense/ completo, esta sesión). La ficha ficha-r34-conda-v2-spec.md:148 ya aisló friccion_uso como «componente sin disparador» — insumo, no resultado. Re-corre en F0; si un abridor B/C ya existe → PARA (A.8). ═══════════════════════════════

FASES — censo primero, spec congelada después, dato al final

F1 · CENSO de fuentes (sin abrir microdato). Deriva candidatas del canon: data/manifiesto.yaml + inventarios (inventario-fuentes-credito-ahorro-finanzas-hogar, tecnologia-digital, tramites-estado) + data/diseno-muestral.yaml. Busca ítems que midan: percepción de riesgo fiscal/SAT/vigilancia al usar pagos digitales · razones de no-adopción de CoDi/pagos móviles · fricción declarada · confianza en canal personal vs institucional. Candidatas obvias a verificar (verifícalas, no las asumas): ENIF (razones de no uso), ENDUTIH, ENSAFI, encuestas CoDi de Banxico si están en corpus. Veredicto A.4 por candidata (EXISTE-SATISFACE / EXISTE-NO-SATISFACE / NO-ENCONTRADO con universo / NO-ACCESIBLE). Si el censo da cero EXISTE-SATISFACE para B o para C: ese hallazgo ES el entregable — se reporta con universo y el acto cierra proponiendo la vía (llave, adquisición o D), sin forzar un proxy. F2 · COMMIT 1 — spec congelada por condición (solo sobre EXISTE-SATISFACE): instrumento/ola · ítems verbatim con escala declarada · universo (usuarios digitales / bancarizados — dilo) · ponderador y diseño (usa diseno-muestral.yaml; si la fuente exige varianza sin diseño → la reserva correspondiente escrita) · qué patrón cuenta como B-satisfecha / C-satisfecha / no-satisfecha, POR ADELANTADO · «el primer resultado que produzca este procedimiento es el que se reporta». F3 · COMMIT 2 — resultados. A-bis completo: marginales = ASOCIACIÓN; estratificados sin promover; escalas declaradas y sin cruzar; subpoblación vs poblacional no se comparan; punto sin IC que despeje umbral NO adjudica — propone con reserva. Ficha forense/ficha-r34-condBC-v1_0.md con PROPUESTA por condición (B: satisfecha/no/indeterminada; C: ídem) y sus reservas. El gate integrado NO se toca — tests/aceptacion_r3_4.py intacto; el veredicto R3.4 completo lo firma mesa después. Cierre: ADR (qué se midió, qué se propone, base medida 2 de 2 o lo que resulte — declarado=medido) · estado (línea R3.4: «A sellada · B/C medidas, propuesta en mesa») · tablero: fila nueva nacida ABIERTA («mesa adjudica el gate A∧B∧C de R3.4», gatea Hito D 19/21/23 según el resto) — A.12 · nota -cierre · suite · encargo CONSUMIDO. CONTADOR: cero, declarado — este acto fabrica la base; el contador lo mueve la firma del gate.

NO hace

No adjudica R3.4 ni toca su test. No re-abre la condición A. No cablea disparadores a milpa/tramite.yaml (eso es acto de motor aparte; ficha:215 lo documenta). No descarga fuentes nuevas (si el censo exige una: NO OBTENIDO + receta A.5, y para).

## CONSUMIDO

Derivación mecánica (`/tramite`, §3.3): único `Merge pull request #N` cuyo mensaje cita el rótulo `R34-BC-MECANISMO` — `PR #359` (`c6a5ab3`), y ese merge toca este archivo además de otros 6 (`git diff --stat c6a5ab3^1 c6a5ab3`).
