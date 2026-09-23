# ADR-260923-GEN2-TRAMITE-FIRMAS-10-6980-01

**ACTO GEN2-TRAMITE-FIRMAS-10**, 23/sep/2026. Dos asientos que `GEN2-TRAMITE-FIRMAS-9` (PR #1032) no llevó.

**P1.** Verificado por comando: `python3 tools/marcador_segmento.py --escribe` sí sube `N_resultados_gen2_adoptados_activos` de 72 a 87 — confirma el diagnóstico de `NC-260922-GEN2-TRAMITE-FIRMAS-7-369b-02`. No se commitea: los dos archivos que escribe son DERIVADOS y la guardia de PR los rechaza (mismo motivo que revirtió `GEN2-TRAMITE-FIRMAS-9`). Sube solo al fusionar, vía el job de push a `main`. NC `…-6980-01`.

**P2.** De las 10 filas de §Ñ, 7 tenían 11 campos por falta de `que_no_se_corrio` (token de `razon` corrido una posición antes) — corregidas sin tocar id/razón/sucesor. Las otras 3 (`NC-0338/9/40`) ya tenían 12 campos con un defecto distinto y ambiguo (`razon` sin token de A.14) — se dejan como están. Universo completo del archivo: 9 filas más con menos campos, fuera del perímetro declarado — NC `…-6980-02`, `DECISIÓN-DE-MESA-PENDIENTE`.

Suite: VERDE, 0 FAIL. `cuenta_gen2 = NO`. No adopta.
