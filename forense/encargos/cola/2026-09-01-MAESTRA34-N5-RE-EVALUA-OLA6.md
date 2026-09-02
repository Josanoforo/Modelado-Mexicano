ESTADO: LISTO-NUBE
ENTORNO: NUBE
ENCOLADO: 2026-09-02 · gesto de encolado, precedente §1c del transfer maestra-34 (firma D4-a, 1/sep/2026)
BITACORA:
- 2026-09-02 · LISTO-NUBE · encolado por PR [COLA] encola MAESTRA34-N4/N5. COMPUERTA propia del encargo: MAESTRA34-N3 fusionado en origin/main con forense/prereg-duelo-v2/scoreboard-v1_2-AGREGADO.md que traiga puntos L sobre celdas de los CUATRO dominios activos — verificar por PRODUCTO: `git show origin/main:forense/prereg-duelo-v2/scoreboard-v1_2-AGREGADO.md | grep -c "DIN-M"` > 0 y lo mismo para CIV/FAM/TRA. Si falta cualquiera, cero commits.

──── CUERPO VERBATIM DEL ENCARGO (A.3) · el despachador NO lo edita ────

ENCARGO · ACTO MAESTRA34-N5 · RE-EVALUA-OLA6 — invoca /acto (y /mapea)
SHA de redacción: 9d2e69d. Redacta dirección (Fable), 1/sep/2026, contra v2.12. Estado: GATED — ENCOLADO por D4-a (1/sep). Relanzamiento de MAESTRA33-E14 (ADR-265) con la precondición que entonces era imposible ya satisfecha.

ENTORNO ASIGNADO: NUBE. NO se lanza en UBUNTU (no abre microdato: el criterio 3 «caja libre» se DECLARA, no se ejerce; si (2) requiere abrir microdato para confirmar, se deja como pieza de caja sucesora). MODELO SUGERIDO: Opus (juicio de criterios, propone y no decide).
COMPUERTA: MAESTRA34-N3 fusionado en origin/main con scoreboard-v1_2-AGREGADO.md que traiga puntos L sobre celdas de los CUATRO dominios activos (trámite, cívico, dinero, familia) — verifica por producto: `git show origin/main:forense/prereg-duelo-v2/scoreboard-v1_2-AGREGADO.md | grep -c "DIN-M"` > 0 y lo mismo para CIV/FAM/TRA. Razón: motor-nucleo-medible §3.a criterio 1 exige L sobre los cuatro «simultáneamente»; el agregado-b de v1_1 no tiene celda de dinero (11 celdas: CIV/FAM/TRA). Si falta, cero commits.
FIRMA DE MESA — verbatim (1/sep, firma 9, ya en canon): «Si pero dejando claro cuando se abren o bajo qué criterios se abren». Y FP-220 (EVALUACION-OLA6, dirección, vence 2026-09-15): «al primer agregado que satisfaga (1), o el 15/sep/2026, lo que ocurra primero».

═══ VERIFICACIÓN DE EXISTENCIA (A.8) — dirección contra 9d2e69d ═══
(1) ESTRUCTURA: canon/motor-nucleo-medible-v1_0.md §3.a (tres criterios, verbatim) y §3.b (corredor E); tablero FP-220; /mapea (ADR-247) para el criterio 2.
(2) CONTENIDO: E14 cierre (forense/notas/2026-09-01-evaluacion-ola6-cierre.md) evaluó (i)/(ii) por dominio con tabla del 31/jul: salud CUMPLE (ENSANUT, ENIGH), cooperación CUMPLE (ENCUCI, ENIF, ENUT), trabajo CUMPLE, información CUMPLE, tiempo y comunicación NO; y declaró el caveat de que el corpus creció después (ENDUTIH 24, ENASEM 6, ENTI 6, ENADID 3, ENBIARE 4 payloads) sin re-mapear. Veredicto entonces: criterio 1 imposible (L pendiente 11/11). → EXISTE-NO-SATISFACE: la evaluación existe pero contra un corpus y un criterio 1 ya cambiados. `/mapea` sobre las fuentes nuevas contra los dominios candidatos: NO-ENCONTRADO (buscado en forense/notas/*ola6*, 1/sep).
(3) COBERTURA RETROACTIVA: la tabla rule-level es del 31/jul; los payloads de agosto nunca pasaron por ella — se declara y se re-mapea.

PIEZAS
P1 · Criterio 1 por producto: cita el scoreboard v1_2 y las celdas L por dominio (conteo A.13). CUMPLE / NO-CUMPLE con comando.
P2 · Criterio 2 re-derivado: `/mapea` sobre TODO el corpus vigente (manifiesto, no la tabla del 31/jul) para los dominios de modelo-decision-v4_0 sin regla sellada; tabla dominio × encuestas en corpus × reglas candidatas con vocabulario A.4; umbral ≥2 encuestas y ≥3 EXISTE-SATISFACE. Incluye lo que MAESTRA34-A1 haya registrado (Cero Desabasto, Observatorio de Cuidados, CNGMD, DGIS, SICEE) si ya fusionó — verifica por manifiesto.
P3 · Criterio 3: declara el estado de la caja (libre / ocupada por qué acto) sin ejercerlo.
P4 · Veredicto por dominio candidato (salud, cooperación, trabajo, información, tiempo, comunicación, y cualquiera nuevo que P2 revele): ABRE-PROPUESTO / NO-CUMPLE (qué criterio, qué falta). Para cada ABRE-PROPUESTO deja REDACTADO (no lanzado) el lote de caja «REGLAS-OLA6-<dominio>-L1» con las ≥3 reglas EXISTE-SATISFACE, dos commits por regla, precedente MAESTRA33-E18-P3. Enmienda fechada a §3.a con el resultado; FP-220 → recibo con la propuesta. La apertura la firma mesa: este acto no cambia ningún dominio a ACTIVO.

PERÍMETRO Y CONCURRENCIA: forense/notas/ (evaluación, tablas de mapeo) · canon/motor-nucleo-medible-v1_0.md (enmienda fechada §3.a, sin tocar criterios) · forense/encargos/ (lotes redactados, sin encolar) · tablero (FP-220) · A.3 · cascada. Si te encuentras escribiendo fuera de esta lista, PARA — el perímetro estaba mal calculado y saberlo vale más que el atajo.
FP/ADR CANDIDATOS: deriva al arrancar.
CONTADOR: cero directo, declarado (propone aperturas; no mide).
LO QUE NO HACE: no activa dominios; no abre microdato; no carga reglas; no toca el marco ni corridas.
SUCESORES: los lotes REGLAS-OLA6-<dominio>-L1 que mesa firme (caja) · MAESTRA34-E1 recibe la evaluación como insumo del falsador de alcance.
