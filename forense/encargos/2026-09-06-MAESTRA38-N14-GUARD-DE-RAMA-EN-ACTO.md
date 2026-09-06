ENCARGO · ACTO MAESTRA38-N14 · GUARD-DE-RAMA-EN-ACTO — invoca /acto
SHA: b337fd7e · COMPUERTA: ninguna · ENTORNO: NUBE · MODELO: Sonnet. Perímetro disjunto de A2-bis.
FIRMA — verbatim (5/sep): «Algo que podamos correr en paralelo?» + revisión del 5/sep: «tercera ejecución
doble en tres días… un guard mecánico de dos líneas en /acto, paso 0».
A.8: grep -c "ls-remote" .claude/commands/acto.md → 0; defectos: A2 (#526 vs rama de N9, 4/sep),
N11 (#541 vs lauyln, 5/sep).
SPEC: en acto.md, paso 0 del ARRANQUE, antes de crear rama: `git ls-remote --heads origin | grep -i
"<rótulo>"`; si hay coincidencia → PARA, reporta la rama y termina con cero commits; además, al abrir
rama, `git push -u` inmediato con el 0-bis (así el rótulo es visible para cualquier segunda sesión
desde el primer minuto). Control positivo en la nota: simular con un rótulo existente y pegar el PARO.
Hallazgo: una línea. PERÍMETRO: .claude/commands/acto.md · hallazgos · tablero (recibo) · A.3 ·
cascada. NO toca nada más. ADR-346 · FP-310 (o los siguientes libres; deriva).
