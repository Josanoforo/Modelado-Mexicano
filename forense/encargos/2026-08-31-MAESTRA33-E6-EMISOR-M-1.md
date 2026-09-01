ENCARGO · MAESTRA33-E6 · EMISOR-M-1 — invoca /acto · ESTADO: LISTO-NUBE
SHA de redacción: a6d8504. ENTORNO: NUBE — NO CAJA. COMPUERTA: marco-M-sorteado-v1_1.tsv en origin/main (B″ fusionado); si no, cero commits. MODELO SUGERIDO: Sonnet (receta congelada).
FIRMA DE MESA (verbatim, 31/ago/2026): "Dame las siguientes automatizaciones".
A.8 (dirección contra a6d8504): corridas-M/M-TRA-M-01.json y M-TRA-M-02.json EXISTEN (esquema, grado_DD). Herramienta emisora: NO-ENCONTRADO (E20-P3 los escribió sin script: git show 16c37b6 --stat → 2 json, 0 .py).
P1 · tools/emite_m.py: por celda del sorteado v1_1 con regla cargada en milpa/tramite.yaml y SIN corridas-M/M-<id>.json: llama al motor (emitir_binaria) → valor_punto = p de la regla; escribe M-<id>.json con el esquema leído de M-TRA-M-01 (no de memoria) y grado_DD según F-DD (misma ola/instrumento que calibró p → VERIFICACION-NO-PUNTUA; otra → PUNTÚA). Celda sorteada sin regla cargada → fila "sin regla" en la nota, no se inventa.
P2 · Regresión antes de emitir: reproduce M-TRA-M-01/02 byte a byte salvo fecha y sha. No coincide → PARO-reporta, sin ajustar.
P3 · Caminata sobre todas las sorteadas elegibles + skill .claude/commands/emite-m.md para caminatas futuras. CIEGO: jamás abre corridas-R/; lista archivos abiertos al cierre.
PERÍMETRO: tools/emite_m.py, emite-m.md, corridas-M/ (solo nuevos), forense/notas propia, tablero (recibo), archivo A.3, cascada. Frase exacta de perímetro vigente. FP/ADR: deriva. CONTADOR: puntos M 2→N, declarado.
LO QUE NO HACE: no carga ni sella reglas; no toca R; no puntúa; no sortea.

FIRMA DE MESA (FP-212, verbatim): «[tu texto del punto 2]».
P4 · Propaga la firma de FP-212 verbatim al tablero y deja en la nota de emisión la declaración del benchmark v1_1: sin asiento en tramite|P1|MEDIA; TRA-M-02 informativo, no puntúa.
