# Recibo Codex para Claude · ASTRA5-U2 ENDIREH · 23/sep/2026

**PR borrador:** [#1093](https://github.com/Josanoforo/Modelado-Mexicano/pull/1093), rama `codex/astra5-genero-endireh-1`, worktree `/home/pc0/mm-astra5-genero-endireh-1`. **No es cierre ni propuesta de merge.** La mesa firma únicamente tras completar el encargo y resolver las ocho fallas propias de registro.

## EJECUTADO

1. Se localizó `04-ASTRA5-U2-GENERO-ENDIREH.md` en Descargas MX, se leyó íntegro con AGENTS, `/acto`, decisiones y reservas, y se archivó verbatim con hash. No existía trabajo previo de esta rama en worktrees, ramas ni sesiones Codex.
2. Se congelaron, ejecutaron, sellaron y verificaron con `REPRODUCE` ocho procedimientos finales: 2021 pareja física A1/A2 V4, ayuda/denuncia/razones A1/A2, decisiones y dinero A1/A2, comunitario, familiar, escolar, laboral interpersonal; 2016 pareja física A1/A2 V2. Los intentos V1/V2/V3 previos se preservan según su estado, sin repetir sellos. Cada resultado utilizable figura en `forense/analisis/dominios/genero/*-tabla.tsv` con CALC, RESULT, hash, universo, punto, IC y soporte; las réplicas agregadas están en `resultados.json` sellados. `forense/replay-evidencia.tsv` contiene asientos reales.
3. Se dictaminó documentalmente la ola 2003. Se identificaron 2006 y 2011 como olas propias en FD XLS y módulos de situación conyugal, no como espejos de 2021. Se documentó matriz de cobertura y tareas restantes.

## LEÍDO

Manifiesto, cuestionario A/FD/diseño 2021 de #1082, FD 2016, FD 2003 y FD XLS 2006/2011; contrato U0 GEN-001 de subcomponente físico. U0 no valida el agregado 70.1%. Raw local reutilizado sin incorporación al repositorio; GEN1 nunca fue origen numérico.

## REPORTADO / NO-CORRIDO / RESERVAS

- `python3 tests/check.py --baseline`: **ROJO, 8 FAIL nuevos propios**. V3 y V4 de pareja física 2021 sellaron RESULT IDs iguales sin cadena `repite_de`; el registro se detiene. Los sellos no se modificaron. V3/V4 también contienen errata en el campo informativo `hash_medidor_sha256`; el blob ejecutado consta correctamente en `ejecucion.json` y `verify` reproduce. Ruta exacta para resolver: mecanismo de sucesión que no mutile sello, o resolución explícita de mesa. Hasta entonces: **sellada en disco, no registrada**.
- Pendientes de medición: pareja B/C y otros tipos de violencia de pareja 2021; 8.3 discriminación laboral; otros ámbitos, ayuda y economía 2016; módulos por estado conyugal de 2011/2006; posible 2003 solo después de diseño específico. Detalle en `2026-09-23-endireh-matriz-y-pendientes.md`.
- No hay calibración temporal, adopción, ni contraste directo del 70.1%. No se atribuye violencia a una persona ni cultura. Las reservas siguen vigentes; no se abrió una ola reservada.

El siguiente turno debe continuar las piezas independientes, solucionar el registro sin alterar sellos, repetir `check.py --baseline` y solo entonces preparar nota de cierre, FP/NC, ADR raíz y estado de publicación. PR #1093 permanece borrador hasta ello.
