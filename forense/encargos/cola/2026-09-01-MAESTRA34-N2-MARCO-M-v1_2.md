ESTADO: LISTO-NUBE
ENTORNO: NUBE
ENCOLADO: 2026-09-02 · gesto de encolado, precedente §1c del transfer maestra-34 (firma D4-a, 1/sep/2026)
BITACORA:
- 2026-09-02 · LISTO-NUBE · encolado por PR [COLA] encola MAESTRA34-L1/N1/N2/L2/N3. COMPUERTA propia del encargo: MAESTRA34-N1 fusionado en origin/main con ≥1 regla nueva cargada en milpa/tramite.yaml (reglas del motor > 8) Y MAESTRA33-E21 fusionado (#446, ya lo está). Si falta cualquiera, cero commits.

──── CUERPO VERBATIM DEL ENCARGO (A.3) · el despachador NO lo edita ────

ENCARGO · ACTO MAESTRA34-N2 · MARCO-M-v1_2 — invoca /acto (y /emite-m)
SHA de redacción: 8598a72. Redacta dirección (Fable), 1/sep/2026, contra v2.12. Estado: GATED — ENCOLADO por firma D4-a (1/sep): «D4-a» = los tres encargos de la cadena se archivan en forense/encargos/cola/ en un solo PR [COLA] y /despacha los toma por orden de nombre cuando su compuerta se cumpla. La fusión de ese PR es la firma.

ENTORNO ASIGNADO: NUBE. NO se lanza en UBUNTU (no abre microdato). MODELO SUGERIDO: Opus (lote de 4 piezas con juicio de marco).
CARRILES: puede coincidir con MAESTRA34-L1/L2 en caja; perímetros disjuntos salvo cascada.

COMPUERTA: MAESTRA34-N1 fusionado en origin/main con ≥1 regla nueva cargada en milpa/tramite.yaml (reglas del motor > 8) Y MAESTRA33-E21 fusionado (#446, ya lo está). Si falta cualquiera, cero commits. Semilla: `semilla_desde_sha_merge(<SHA del merge de MAESTRA34-N1>, "MARCO-M-v1_2")` — deriva, no heredes.

FIRMA DE MESA — verbatim (1/sep): «1-aceptarlo. pero necesitamos que quede asentado el sistema corregido para que no vuelva a pasar» — primer sorteo con sorteo_v3 y reglamento v1.1.

═══ VERIFICACIÓN DE EXISTENCIA (A.8) — dirección contra 8598a72 ═══
(1) ESTRUCTURA: forense/prereg-duelo-v2/ (marco, sorteado, corridas-M, L-spec) gobierna; INFRAESTRUCTURA D5 (celdas). Reglamento: reglamento-sorteo-v1_1.md + sha; sorteo_v3.py; candado T-SORTEO.
(2) CONTENIDO: marco-M-congelado-v1_1.tsv + .sha256 EXISTE-SATISFACE (27 filas, 22 elegibles — re-deriva). `ls forense/prereg-duelo-v2 | grep v1_2` → NO-ENCONTRADO (1/sep). corridas-M: 13 archivos v1_1; corridas-R 11/11; L-extraido-v1_1.tsv EXISTE.
(3) COBERTURA RETROACTIVA: no aplica.

PIEZAS
P1 · marco-M-congelado-v1_2.tsv: celdas v1_1 intactas + una por (regla nueva del motor × ola en corpus por la vía del índice/manifiesto), grado_DD por F-DD, columnas idénticas, sha256, N_elegibles derivado. COMMIT-1 antes de sortear, con frase de sello.
P2 · sorteo_v3 bajo reglamento v1.1, tamaño según ADR-231 §e; marco-M-sorteado-v1_2.tsv. Ningún estrato no vacío sin asiento — si ocurre, PARO: bug de v3, es entregable.
P3 · /emite-m sobre las sorteadas nuevas → corridas-M/M-<id>__v1_2.json; los M de v1_1 no se tocan aunque la regla haya cambiado (registro de lo que M creía entonces). Regresión byte a byte de los existentes.
P4 · L-spec-v1_2.json + sha (derivada del marco, sin cifra de R) y PAQUETE-L-v1_2 con runner_l_cli.py (sin API, firma E17). Filas de tablero R-v1_2 (gatea MAESTRA34-L2) y L-v1_2 (mesa corre el paquete) con `vence: 2026-09-08`.

PERÍMETRO Y CONCURRENCIA: forense/prereg-duelo-v2/{marco-M-congelado-v1_2.tsv,.sha256,marco-M-sorteado-v1_2.tsv,L-spec-v1_2.json,PAQUETE-L-v1_2/} · corridas-M (solo archivos __v1_2) · notas · tablero · A.3 · cascada. Si te encuentras escribiendo fuera de esta lista, PARA — el perímetro estaba mal calculado y saberlo vale más que el atajo.
FP/ADR CANDIDATOS: deriva al arrancar.
CONTADOR: celdas v1_2 +N; M +N; declarado.
LO QUE NO HACE: no toca v1_1 ni sus corridas; no calcula R; no corre L; no puntúa.
SUCESORES: MAESTRA34-L2 (arbitra v1_2, caja) · mesa corre PAQUETE-L-v1_2 · MAESTRA34-N3 (AGREGA-2).
