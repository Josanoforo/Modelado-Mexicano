# Encargo · ACTO REPARA-PROPAGA-15 — CONSUMIDO

Redactado por dirección, 24/ago/2026, contra clon propio `origin/main = fb02421`.

**Contexto.** `CORROBORA-MOTOR` (B1, `forense/notas/2026-08-24-corrobora-motor.md`) reportó la suite en ROJO: el movimiento `14→15` del Hito D dejaba `README.md` y tres citas de `14 de 27` en `canon/modelo-decision-v4_0.md` fuera del perímetro que `SELLA-AGO24` cerró.

**Resultado.** Defecto no reproducido. `grep -n "14 de 27" README.md canon/modelo-decision-v4_0.md`: `README.md` no contiene la cadena (ya cita `15 de 27`, `README.md:36`); `canon/modelo-decision-v4_0.md:65` y `:700` sí la contienen, pero en ambas líneas la cita viva del contador ya dice `15 de 27 corridas archivadas` — el `14 de 27` que el grep encuentra es narración fechada de la bitácora de correcciones de cada línea, historia que se queda sin editar por regla del propio encargo. `python3 tests/check.py --baseline`: `T20 T-CASCADA-MARCADA` en `[ ok ]`, línea base **VERDE**. Ningún archivo del perímetro (`README.md`, `canon/modelo-decision-v4_0.md`) editado.

**Cierre.** `ADR-147` (`canon/gobernanza-v1_15.md`) y una línea en `forense/hallazgos.md`. Este archivo queda consumido al cerrar el acto.
