ENCARGO · MAESTRA33-A4 · REGISTRA-DESCARGAS-MANUALES — invoca /acto (y /adquiere)
SHA de redacción: ee6a8a2 (merge PR #436). ENTORNO: CAJA — NO NUBE. COMPUERTA: ninguna; corre cuando el barrido de recetas termine. MODELO SUGERIDO: Sonnet.
FIRMA DE MESA (verbatim, 2/sep/2026): "no vamos a esperar a esa fecha a que se venza, ni esta ni ninguna otra".
A.8: PAQUETE-RECETAS-2026-09-01 EXISTE; descargas manuales: se derivan de ~/descargas-mx/ al arrancar (declara cuántos archivos examinó, A.13); manifiesto y cola-adquisicion EXISTEN.
P1 · Por cada archivo bajado: mover al corpus compartido (cierre anti-PR#77), sha256 (doble si trae token, A.7), entrada en data/manifiesto.yaml con descargado_por: mesa-navegador y la receta como url_origen, fila de cola → OBTENIDO. Lo que la receta no logró → queda NO-OBTENIDO con el paso exacto donde falló (A.5), sin re-sondear.
P2 · Corre /mapea sobre las 6 necesidades de FP-190 contra SOLO los payloads nuevos; tabla de candidatas con vocabulario A.4. Si alguna pasa a EXISTE-SATISFACE, deja redactado el lote C10 · REGLAS-OLA5-FASE2-B como sucesor con las celdas nombradas.
PERÍMETRO: data/raw, manifiesto, cola-adquisicion, notas, tablero (recibo), A.3, cascada. Frase exacta vigente. CONTADOR: payloads OBTENIDO +N.
LO QUE NO HACE: no abre microdato para medir; no carga reglas; no descarga por red.

## CONSUMIDO

Ejecutado por `ACTO MAESTRA33-A4 · REGISTRA-DESCARGAS-MANUALES`, `PR #440`
(rama `acto/maestra33-a4-registra-descargas-manuales`). Cierre por hallazgo:
P1 encontró cero descargas manuales nuevas en `descargas_mx` (122 archivos
examinados, A.13, mtime máximo 2026-08-13, anterior a la emisión de
`PAQUETE-RECETAS-2026-09-01`); P2 quedó sin universo que caminar
(dependiente de P1). Detalle:
`forense/notas/2026-09-01-maestra33-a4-registra-descargas-manuales-cierre.md`.
CONTADOR: payloads `OBTENIDO` +0.
