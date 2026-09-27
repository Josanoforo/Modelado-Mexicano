# Nota · ACTO GEN2-TRAMITE-FIRMAS-20 · 27/sep/2026

Contadores movidos: cero mediciones. `adoptados` se mueve cuando GEN2-CATALOGO-V1-3-1 y el marcador consuman estas firmas.

ARRANQUE: clon `/home/user/Modelado-Mexicano`, rama `claude/new-session-7teewr` (la fijó la plataforma). Base `57a3f2a4` (#1185) = origin/main tras `git fetch --prune` (0 detrás); SHA de redacción `3149b4e2` es ancestro, main avanzó 12 commits (C1-PAQUETES-2 #1185, CI-TIEMPO-1): se re-derivó todo. ENTORNO-DERIVADO = NUBE (hook), `CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE=cloud_default`, red DENEGADA-POR-POLÍTICA, corpus montado = NO (0 archivos examinados); el acto no toca microdato ni red. `data/raw` creada vacía. 0-bis `96f91541`, raíz `96f9`. Duplicado: sin rama/worktree/PR abierto con `FIRMAS-20` (la búsqueda de PR devolvió solo #1175 [DERIVADOS], por texto). §4: `grep -c 'FIRMAS-20' forense/firmas-pendientes.tsv` → 0 antes del acto.

## Premisas re-verificadas
- [EJECUTADO] «23 FP ABIERTA a `3149b4e2`»: a `57a3f2a4` hay 24 (lector CSV, estado=ABIERTA); la 24.ª es `FP-260926-GEN2-ASTRA6-C1-PAQUETES-2-9c9e-01`, nacida en #1185 después de la redacción. No está en la hoja: **sin cambio** (FUERA de este trámite, se lleva al siguiente).
- Las 18 FP leídas enteras; en todas, la recomendación del ejecutor coincide con la opción de §1, salvo lo que se dice abajo de ad01-01.
- Adopciones con `verify` citado (compuerta §8): 15 CALC (ENSU ×2, CCPV, EMAT, EDR, ENPECYT y los nueve de COLA-COMPLETA-1) con fila REPRODUCE/IDENTICO en `forense/replay-evidencia.tsv` (lector CSV, 15/15; los nueve de A6 son ENDISEG, MMSI, ENASEM, ENVIPE 2024, ENOE 2024T4, Latinobarómetro COLA 2023, PEW 2024, ENADID 2018 y EIC 2015).
- **Premisa de §1 D que no se sostiene al minuto (logística, no toca la firma):** «#1170 y #1173 entraron antes del recibo». Por la API de GitHub: #1170 fusionó 22:56:39Z, el recibo #1178 23:07:51Z y #1173 **23:11:59Z**, cuatro minutos *después* del recibo. La decisión firmada (ii) no cambia; refuerza la regla de D.

## Firma
§2: mesa firmó la hoja completa («firmado») sin corrección por letra. Cada FIRMADA lleva en `firmada_en` el texto de su letra de §1 verbatim y en `ejecutada_en` el ADR + `EJECUTA:`.

## P1 · filas (18 FIRMADA)
A1 5916-01 · A2-A5 3a49-01..04 · A6 0d4a-01 → `EJECUTA: GEN2-CATALOGO-V1-3-1`. B1 fde0-01 y ad01-01 · B3 7045-01 · B4 cca0-01 · B5+D 996b-01 → `EJECUTA: MISION-ASTRA-6 C2`. B2 fde0-02 → `EJECUTA: SELLO-EXTERNO-2`. C edf7-01, 9d28-01, 5803-01, ed83-01, 92f8-01, ed83-02 → `EJECUTA: GEN2-CATALOGO-V1-3-1` como propuestas.
- INTERPRETACIÓN-DECLARADA (ad01-01): la hoja de CIERRE-MATERIAL-1 trae cuatro decisiones; §1 B1 solo nombra pago digital. La FP va FIRMADA con B1 y el alcance escrito en `ejecutada_en`; las otras tres (control ENIF, identidad ENCIG, singleton ENVIPE) no se infieren firmadas → NC-260927-GEN2-TRAMITE-FIRMAS-20-96f9-01.
- INTERPRETACIÓN-DECLARADA (996b-01): la FP del recibo cubre B5, D y la precisión incidental de B3; las tres van en su `firmada_en`.
- El VETO de Intercensal 2015 (A6) no se escribe en `decisiones.tsv`: fuera de §9 y «no adopta en consumidor» → NC-…-96f9-03, DIFERIDO-A GEN2-CATALOGO-V1-3-1.

## P2 · NC
CERRADA: NC-260926-GEN2-CIERRE-SEMANAL-1-dea2-01 (ENSU firmada) · NC-260926-GEN2-COLA-LOTE-1-3a49-04 (adopción firmada; las olas recientes siguen RESERVADAS) · NC-260926-GEN2-RECIBO-ASTRA6-N-996b-05 (B5) · -996b-06 (B3 incidental) · -996b-02 (sucedida por #1179; nuevo recibo en NC-…-9d28-01) · NC-260926-GEN2-ASTRA6-C3-TRABAJO-MOVILIDAD-1-ed83-02 (exposición adjudicada) · NC-260926-GEN2-FRONT-3-PORTADA-1-8914-02 (sucedida por NC-…-96f9-02).
Siguen ABIERTA a propósito: NC-…-996b-01 (#1170: T-REPRO la corrige la siguiente sesión de C2 como CALC sucesor, sin editar sellos; es la «NC por defecto» de D) · NC-…-ad01-01 y -03 (ver 96f9-01) · las NC de recibo técnico de Claude (5803-01, 92f8-01, 9d28-01, edf7-01), que ninguna letra de la hoja decide.
D: el recibo queda `RECIBIDO-POST-MERGE` por la firma asentada en 996b-01; el archivo del recibo (`forense/notas/2026-09-26-GEN2-RECIBO-ASTRA6-N-recibo.md`) es ajeno a §9 y no se edita. La regla «ningún `codex/*` se fusiona sin fila FP del recibo FIRMADA» queda asentada en esa FP.

## P3 · E (`vence:`)
3d56-01, 4296-01, 43d6-01: vence 2026-09-27 (ya asentado; se reafirma). c3fa-05: vence 2026-10-15 (ya asentado). 8914-03: no traía vence → vence 2026-09-27, PROPUESTO-POR-EJECUTOR (mismo fin de semana que Pages/Zenodo). Las cinco siguen ABIERTA con una NOTA fechada.

## Derivados regenerados por comando (D-21, tras CI del PR #1190: `guardias` ROJO en 2 tests)
- `tests/test_cableado_sesiones.py::test_memoria_cabe_y_bloque_coincide`: el bloque T-MEM de `canon/MEMORIA-OPERATIVA.md` se deriva de las FIRMADA → `python3 tools/memoria_operativa.py --escribe` (paso T-MEM de trámite). Arrastra `forense/analisis/cableado/herramientas.tsv` (+2 tools), que ya estaba ROJO en origin/main `57a3f2a4` (`--verifica` → «herramientas.tsv difiere de tools/», comprobado en worktree de origin/main).
- `tests/test_catalogo_v1_2.py::test_regenera_identico`: la sección «pendientes de firma» del catálogo v1.2 lista FP de adopción ABIERTA; con 5916-01 FIRMADA sale de la lista (1 → 0). `python3 forense/analisis/catalogo/genera_catalogo_v1_2.py --sin-registro`: cambian solo `canon/catalogo-del-mexicano-v1_2.md` (−1 fila), `conteos-v1_2.json` (`pendientes_de_firma` 1 → 0) y `pendientes-de-firma-v1_2.tsv` (−1 fila). El TSV del catálogo no cambia: no se adopta nada en el consumidor (la adopción la hace GEN2-CATALOGO-V1-3-1). En origin/main el test pasa: el rojo lo causa este PR.
- Segunda vuelta de CI (`suite` ROJO, 1 FAIL nuevo frente a la línea base): T02 «contenido idéntico bajo nombres distintos» entre `forense/analisis/catalogo/v1_1/pendientes-de-firma.tsv` y `…/v1_2/pendientes-de-firma-v1_2.tsv`. Con cero FP de adopción ABIERTAS, los dos quedan solo con cabecera. Defecto adyacente ≤ 10 líneas (D-21): se añade el par exacto a `EXCEPTED_HASH_GROUPS` de `tests/check.py`, con comentario, sin excluir directorios. Antes se integró origin/main (`0304bf21`, +5 commits, sin conflicto).
