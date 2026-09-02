ESTADO: LISTO-CAJA
ENTORNO: UBUNTU (abre microdato)
ENCOLADO: 2026-09-02 · gesto de encolado, precedente §1c del transfer maestra-34 (firma D4-a, 1/sep/2026)
BITACORA:
- 2026-09-02 · LISTO-CAJA · encolado por PR [COLA] encola MAESTRA34-L1/N1/N2/L2/N3. `/despacha` NO ejecuta este encargo (es de caja, no de nube): lo nombra y lo deja para que una sesión de CAJA lo tome cuando su compuerta se cumpla. COMPUERTA propia: MAESTRA34-N2 fusionado en origin/main con marco-M-sorteado-v1_2.tsv y su sha. Si falta, cero commits. Un solo acto de caja a la vez: no arranca si MAESTRA34-L1 no fusionó.

──── CUERPO VERBATIM DEL ENCARGO (A.3) · el despachador NO lo edita ────

ENCARGO · ACTO MAESTRA34-L2 · ARBITRA-v1_2 — invoca /acto (y /arbitra)
SHA de redacción: 8598a72. Redacta dirección (Fable), 1/sep/2026, contra v2.12. Estado: GATED — ENCOLADO por firma D4-a (1/sep): «D4-a» = los tres encargos de la cadena se archivan en forense/encargos/cola/ en un solo PR [COLA] y /despacha los toma por orden de nombre cuando su compuerta se cumpla. La fusión de ese PR es la firma.

ENTORNO ASIGNADO: UBUNTU (abre microdato). NO se lanza en NUBE. MODELO SUGERIDO: Opus. Un solo acto de caja a la vez: no arranca si MAESTRA34-L1 no fusionó.
COMPUERTA: MAESTRA34-N2 fusionado en origin/main con marco-M-sorteado-v1_2.tsv y su sha. Si falta, cero commits.
FIRMA DE MESA: régimen del árbitro ya sellado (ADR-244: dicotomización y diseño en codificacion-R, legible por máquina; ciego a M/L). No hay firma nueva que propagar.

═══ VERIFICACIÓN DE EXISTENCIA (A.8) — dirección contra 8598a72 ═══
(1) ESTRUCTURA: codificacion-R-v1_0.tsv gobierna la dicotomización; corridas-R/ el resultado; INFRAESTRUCTURA D4/D5.
(2) CONTENIDO: corridas-R 11/11 para v1_1 EXISTE-SATISFACE; filas de codificacion-R para celdas v1_2 → NO-ENCONTRADO por construcción (las celdas aún no existen); la fila de calibración ENCIG 2025 la trae MAESTRA34-L1 → REUTILIZA, no dupliques.
(3) COBERTURA RETROACTIVA: no aplica.

PIEZAS (lotes de ≤4 celdas por COMMIT-1/COMMIT-2, tantos lotes como celdas sorteadas nuevas ÷ 4; todos en este PR)
Por lote: COMMIT-1 añade a codificacion-R las filas de las ≤4 celdas (variable, codificación, universo, ponderador, diseño) y cierra con la frase de sello; COMMIT-2 corre /arbitra y escribe corridas-R/R-<id>__v1_2.json. Ciego a corridas-M/L. Una celda que PARA (variable inexistente, diseño sin UPM) se reporta con A.4/A.13 y no tumba el lote.
Al cierre: recuento R v1_2 completo / parcial, y fila R-v1_2 del tablero → FIRMADA-EJECUTADA con este PR.

PERÍMETRO Y CONCURRENCIA: codificacion-R-v1_0.tsv (filas nuevas) · corridas-R (solo __v1_2) · notas · tablero · A.3 · cascada. En paralelo: mesa corriendo PAQUETE-L-v1_2 (corridas-L). Si te encuentras escribiendo fuera de esta lista, PARA — el perímetro estaba mal calculado y saberlo vale más que el atajo.
FP/ADR CANDIDATOS: deriva al arrancar.
CONTADOR: R 11 → 11+N, declarado.
LO QUE NO HACE: no emite M; no corre L; no puntúa; no toca v1_1.
SUCESOR: MAESTRA34-N3.
