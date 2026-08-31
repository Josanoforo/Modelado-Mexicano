ENCARGO · MAESTRA33-E3 · CABLEADO-COLA-DIGESTO — invoca /acto
SHA de redacción: 6a12244. ENTORNO: NUBE — NO CAJA, NO doble. COMPUERTA: PR #413 (rama claude/agente-despacho-d13-0l8pdg) fusionado; si no, cero commits. MODELO SUGERIDO: Opus.
FIRMA DE MESA (verbatim, 31/ago/2026): "Necesito que queden cableadas de la A a la Z sin espacios por donde se filtre el agua."
A.8 (dirección contra 6a12244 + rama E2): digesto cubre secciones A-E+Pie (verificado en DIGESTO-2026-08-31.md) — cola: NO cubierta. Runbook de E2: estados LISTO-NUBE/EN-CURSO/CONSUMIDO/PARO-REPORTADO definidos; regla de caducidad de EN-CURSO: NO-ENCONTRADO (grep stale|huerfan|caduc → 0). Escaneo PENDIENTE-DE-MESA en digesto: NO-ENCONTRADO.
P1 · Caducidad de EN-CURSO: añade a forense/agente-despacho-v1_0.md y a la skill /despacha la regla — un EN-CURSO de >24h SIN rama remota ni PR propios es HUÉRFANO: el despachador NO lo ejecuta ni lo resetea (juicio de mesa), lo reporta; el reset es un commit de una línea de mesa/dirección devolviéndolo a LISTO-NUBE o a PARO-REPORTADO con la razón.
P2 · Digesto v1_1 (tools/digesto_tramite.py + su nota): sección F · Cola — LISTO-NUBE en espera (con edad), LISTO/esperando-CAJA (con edad), EN-CURSO (edad + ¿tiene rama/PR? → HUÉRFANO si no), PARO-REPORTADO sin triaje, y la línea "COLA VACÍA — dirección debe redactar" cuando no haya LISTO. Sección G · PENDIENTE-DE-MESA — grep derivado sobre milpa/*.yaml, lista de ids con fecha de su acto de origen. Todo negativo con conteo A.13.
P3 · Pie del digesto: fechas de revisión de los falsadores vivos (leídas de los runbooks de trámite/despacho/skill, no de memoria), para que "en un mes" no dependa de que alguien se acuerde.
PERÍMETRO: tools/digesto_tramite.py, .claude/commands/despacha.md, forense/agente-despacho-v1_0.md, forense/agente-tramite-v1_0.md (§2 si aplica), archivo A.3, tablero (recibo), cascada. Frase exacta de perímetro vigente. FP/ADR: deriva, no heredes. CONTADOR: cero mediciones, declarado.
LO QUE NO HACE: no ejecuta items de la cola; no resetea ningún EN-CURSO; no toca milpa/ (solo lo lee); no crea schedule.
SUCESORES: ninguno — cierra el cableado nube.

## CONSUMIDO

Ejecutado por `ACTO MAESTRA33-E3 · CABLEADO-COLA-DIGESTO` el 31/ago/2026,
rama `claude/cableado-cola-digesto-affup3`, `ADR-243`.
Compuerta `PR #413` verificada mecánicamente antes de tocar nada.
PR: `#415` (https://github.com/Josanoforo/Modelado-Mexicano/pull/415),
abierto sobre esa rama. Fusionar es firmar: el acto lo propone, mesa lo
firma al fusionar.
