ESTADO: CONSUMIDO
ENTORNO: NUBE
ENCOLADO: 2026-09-02 · gesto de encolado, precedente §1c del transfer maestra-34 (firma D4-a, 1/sep/2026)
BITACORA:
- 2026-09-02 · LISTO-NUBE · encolado por PR [COLA] encola MAESTRA34-L1/N1/N2/L2/N3. COMPUERTA propia del encargo: MAESTRA34-N1 fusionado en origin/main con ≥1 regla nueva cargada en milpa/tramite.yaml (reglas del motor > 8) Y MAESTRA33-E21 fusionado (#446, ya lo está). Si falta cualquiera, cero commits.
- 2026-09-02 · CONSUMIDO · ejecutado por `ACTO MAESTRA34-N2 · MARCO-M-v1_2`, PR `[MAESTRA34-N2] ACTO MAESTRA34-N2 · MARCO-M-v1_2` (`#450`, fusionado), `ADR-275`. Marca aplicada por P4(a) de `ACTO MAESTRA34-N4 · PLOMERIA-v1_2` — la ejecución ya tenía `## CONSUMIDO` abajo, pero el header `ESTADO` seguía `LISTO-NUBE` (`EXISTE-NO-SATISFACE`, verificación A.8 de `MAESTRA34-N4`); esta línea es la marca que faltaba.

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

## CONSUMIDO

Ejecutado 2/sep/2026 por `ACTO MAESTRA34-N2 · MARCO-M-v1_2` con la skill `/acto`
(`ADR-237`), entorno NUBE `cloud_default`, sin abrir microdato ni descargar nada.

**Compuerta verificada dos veces.** Al primer lanzamiento de la sesión NO se
cumplía (`MAESTRA34-N1` ausente de `origin/main`, motor en 8 reglas) y el acto
paró con **cero commits**. `origin/main` avanzó de `92fd3f7` a `ec3cf0f` durante
la sesión; re-verificada (`#449` fusionado, motor en 10 reglas, `#446`
fusionado), CUMPLE.

Piezas entregadas: **P1** `marco-M-congelado-v1_2.tsv` (34 filas,
`N_elegibles=27`) + `CONGELADO-M-v1_2.sha256` · **P2** `marco-M-sorteado-v1_2.tsv`
(14 celdas, `sorteo_v3`, sin estrato no vacío en cero) · **P3** 6
`corridas-M/M-<id>__v1_2.json` · **P4** `L-spec-v1_2.json` + `.sha256` +
`PAQUETE-L-v1_2/` + filas `FP-227`/`FP-228`.

Dos hallazgos entregados y **no parchados**, por estar su arreglo fuera del
perímetro que este encargo declara: `DIN-M-01` no emitible (F-DD no sabe
expresar calibración sobre un rango de olas) y `PAQUETE-L-v1_2` no lanzable
(`runner_l_cli.py` dimensionado a 11 celdas). Ambos con parche propuesto en las
notas de cierre.

PR: `[MAESTRA34-N2] ACTO MAESTRA34-N2 · MARCO-M-v1_2` (rama
`claude/acto-maestra34-n2-marco-gv8cq6`). Cascada: `ADR-275`,
`canon/estado-programa-v1_10.md` L0 (274 → 275), `canon/registro-rotulos.tsv`,
`forense/firmas-pendientes.tsv`.
