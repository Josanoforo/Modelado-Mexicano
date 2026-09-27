# C1 edad · sincronización posterior a #1200

EJECUTADO el27/sep/2026 por instrucción de mesa: esperar fusión de #1200, hacer fetch/sync y resolver CI contra nuevo main.

GitHub confirmó #1200 fusionado en `16f360321a42426b4a5a56d83689ed5193d16f2a`. Fetch de origin y merge a `codex/astra6-c1-precision-edad-1` incorporan ese corte; commit de integración `ab3a6646b94637c672f23229297f0fa68fe5f527`. Cero commits de main pendientes y cero conflictos. El diff propio conserva únicamente la adenda de edad, su sidecar y esta nota; no modifica contratos o testimonios incorporados desde main.

EJECUTADO: `python3 tools/sella_sha256.py --verifica --cuerpo forense/validacion-independiente/catalogo-1-adjudicacion-puntos/c1-puntos-precision-edad-adenda-1.md` devuelve SELLO_COINCIDE, SHA2133d646ec7c8c9e0219b356600ef3b4a324f5ade29bd7a938714fc792860bf4. `git diff --check origin/main..HEAD` no señala defectos.

EJECUTADO sobre corte16f36032 incorporado: `python3 tests/check.py --baseline --rapido`,0FAIL615WARN, baseline VERDE; log local `/tmp/astra6-precision-edad-main16f36032-gate.log`. El primer fetch limitado por sandbox no se usó como evidencia de actualización: se repitió fuera del sandbox y se comprobó que la fusión de #1200 es ancestro de origin/main antes del corte final.

CI remota: se comprobará el nuevo HEAD publicado de #1205; la ejecución verde anterior36297747755 correspondía al HEADc8e2f83b y no acredita esta integración. No se modificó CI, baseline, código sellado, datos o adopción. EDAD98 sigue elegible nacional15+ y sin corte etario observado; exclusión nacional conjunta98/99 no autorizada. La fusión de #1205 sigue a cargo de mesa.
