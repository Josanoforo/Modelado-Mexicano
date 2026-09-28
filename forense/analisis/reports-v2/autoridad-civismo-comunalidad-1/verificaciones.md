# Verificaciones ejecutadas · lote C3

Árbol de integración: producto `375d671d` más merge de `origin/main` `eda5bb9f871a85613cfb4eda7d40dc741e55d0b5`. La primera corrida completa del gate fue anterior al archivo de tanda5 en main; la comprobación final se ejecuta sobre el árbol ya integrado. Todos los comandos se ejecutaron desde la raíz del worktree del acto.

| Comando | Resultado |
|---|---|
| Tres verificadores de `autoridad/`, `civismo/`, `comunalidad/` | VERDE: mapa 30/30, 43/43, 49/49; matrices 59, 60, 60; reservas y prosa comprobadas |
| `python3 forense/analisis/reports-v2/autoridad-civismo-comunalidad-1/verifica_lote.py --check` | VERDE: índice, resumen y hashes reproducibles desde las piezas |
| `python3 forense/analisis/reports-v2/autoridad-civismo-comunalidad-1/verifica_lote.py --check` contra archivo canónico de tanda5 y Git 0-bis | Mismos bytes del cuerpo en archivo de #1237 y 0-bis propio; SHA crudo coincide con manifiesto de tanda5; pie posterior fuera del cuerpo |
| `python3 tools/verifica_sidecars.py` | `FAIL: 0 — VERDE`; un WARN heredado ajeno, sin adjudicación |
| `python3 tools/cierre_acto.py --encargo forense/encargos/fuentes/ASTRA6-tanda5-20260927/02-ASTRA6-C3-AUTORIDAD-CIVISMO-COMUNALIDAD-1.md --sin-suite` | `CONSUMIDO` presente; NC propia registrada; `celdas_validadas: 219 → 219 (Δ0)` |
| `python3 tests/check.py --baseline --parallel` | Corrida final tras merge de #1237: exit 0; `LÍNEA BASE: VERDE — sin FAIL nuevos`. La salida cruda informa 3 FAIL heredados y 151 WARN nuevos de estado, ninguno citado por ruta de este lote; T25 VERDE. |
| `git diff --check` | Sin errores después de corregir espacios finales de la fila NC propia |

El primer intento del gate tuvo 3 FAIL nuevos T25 en notas del lote por el identificador del momento 08 sin prefijo. Se corrigieron a «momento 08» con localizador `decisiones.tsv:292` y el segundo gate dio exit 0. No se editó `tests/check.py`, `tests/baseline.json` ni otro archivo para esconder el fallo. La semántica de ROMPE y mecanismos fue revisada manualmente en las piezas; estos controles automáticos no la sustituyen.

La integración de #1237 trajo el cuerpo idéntico del encargo en un archivo canónico. Se eliminó del árbol final la copia creada por el 0-bis propio; la existencia y bytes de esa copia siguen verificables por Git. La primera corrida integrada se interrumpió al hallar una cita literal del identificador del momento 08 en esta misma nota; tras corregirla, T25 dirigido pasó y la corrida completa final terminó con exit 0.

## Continuación de tanda6

Se cotejó la copia de `03-ASTRA6-C3-CIERRE-1240-1.md` con `cmp -s` antes del pie y los SHA-256 de los tres adjuntos embebidos con sus valores declarados: coincidieron. `tools/sella_sha256.py --cuerpo --verifica` dio `SELLO_COINCIDE` tras añadir `NO-CORRIDO / RESERVAS` y `CONSUMIDO` al pie. Los tres verificadores de pieza y `verifica_lote.py --check` siguieron VERDE; `git diff --check` no reportó errores.

`python3 tests/check.py --rapido` encontró primero un FAIL T34 porque el pie nuevo contenía `CONSUMIDO` sin `NO-CORRIDO / RESERVAS` previo. Se añadió la sección exigida fuera del cuerpo sellado y se repitió el gate rápido: exit 0, `0 FAIL · 624 WARN`; T25 y T34 sin FAIL. El gate completo anterior permanece registrado arriba; no se le atribuye la verificación de la adenda nueva.
