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

## CONSUMIDO

Ejecutado por PR #422. tools/emite_m.py (primer emisor M versionado, A.8
verificado: los dos puntos M previos se escribieron a mano sin script,
commit 16c37b6) camina marco-M-sorteado-v1_1.tsv y emite los 11 puntos M
nuevos (CIV-M-01/06/08/09/11/12/13, FAM-M-01, TRA-M-03/05/07; puntos M
2→13), las 11 P1 PUNTUA (F-DD, ADR-249). P2: regresión dentro del propio
tool contra M-TRA-M-01/02.json — PASA byte a byte en todo campo
mecánicamente derivable; dos exenciones declaradas (fuente cita el
acto+fecha que corre; correcciones_aplicadas_por_referencia diverge en
redacción pero no en valor, ver forense/notas/2026-09-01-emisor-m-1-cierre.md).
P3: .claude/commands/emite-m.md. CIEGO verificado: corridas-R/ nunca
abierto.

Hallazgo, no producido por este acto: la firma de mesa que este encargo
cita como FP-212 corresponde hoy a FP-213 — FP-212 quedó tomada por ACTO
MAESTRA33-E7 · MAPEADOR-1 (PR #420 fusionó primero, commit 2a32c09, regla
de la casa), confirmado en vivo por dirección sobre este mismo acto. El
texto verbatim de esa firma («[tu texto del punto 2]» del párrafo de
arriba, nunca resuelto) sigue PENDIENTE de dirección — no vive en ningún
archivo del repo al cerrar este PR (forense/firmas-pendientes.tsv fila
FP-213: firmada_en vacía, estado=ABIERTA). Se propaga en un commit de
seguimiento a este mismo PR en cuanto llegue; P4 no se cierra en falso.

ADR-249 (candidato), canon/estado-programa-v1_10.md L0 recifrado,
canon/registro-rotulos.tsv (MAESTRA33-E6 censado), tests/check.py
(_T25_ARCHIVOS_CONOCIDOS extendido). python3 tests/check.py --baseline:
VERDE, sin FAIL nuevo.
