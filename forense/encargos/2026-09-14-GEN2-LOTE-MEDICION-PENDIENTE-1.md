# ACTO GEN2-LOTE-MEDICION-PENDIENTE-1 · LOTE D-11 DE MEDICIÓN PENDIENTE (NC-0184 · NC-0099 · NC-0125 · NC-0126)

**SHA de redacción:** no declarado en el texto (llegó como brief de despacho, ítem «2 · CAJA»); **re-derivado al abrir:** `a29d873b` (`origin/main`, PR #759 fusionado, 14/sep/2026)
**Entorno asignado:** CAJA (Ubuntu/WSL) — NO se lanza en NUBE
**Modelo:** Opus
**Rama:** `acto/gen2-lote-medicion-pendiente-1`
**Compuerta:** ninguna declarada (`GATED a` / `COMPUERTA:` ausentes). «corre detrás del RUN» se lee como carril: `ACTO GEN2-F5-DOCUMENTAL-RUN` (PR #756) `MERGED` 2026-09-14T19:11Z, `## CONSUMIDO` en su encargo archivado — la secuencia se cumple.
**Estado:** VIVO

## Texto del encargo, verbatim tal como se lanzó

2 · CAJA — ACTO GEN2-LOTE-MEDICION-PENDIENTE-1 (lote D-11, Opus, hasta 4 piezas afines de microdato; corre detrás del RUN)

P1 = NC-0184: correr el CALC de la spec EDER-CORRESIDENCIA-DISENO-spec-v1_0. Verificado: la spec quedó congelada en COMMIT-1 por #760 (0cbaba6c, 14/sep) y cero corridas la consumen (grep -i corresid en corridas.tsv: 0 coincidencias, 166 filas examinadas — A.13). Es puro COMMIT-2: el trabajo caro ya está hecho. Cierra la única regla EDER con IC de bootstrap simple.
P2 = NC-0099: la ruta U4 en ENVIPE 2012 vía join a tsdem por N_REN == R_SEL. Verificado: 0 filas U4/tsdem-2012 en corridas.tsv.
P3/P4 (opcionales) = NC-0125 + NC-0126: reconciliar la cobertura ENIF (fase 1 declaró 66.89%; la corrida mide 67.53/68.06) y adjudicar la categoría colapsada P4_10
