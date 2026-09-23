# ASTRA4-U1 · cierre y refresco de #1071

El catálogo publica 1 537 lecturas de estimando/segmento/ola en cinco áreas. `forense/analisis/catalogo/genera_catalogo.py` releyó 57 CALC y sus sellos: 85 usos GEN2 remiten a 72 RESULT únicos. `publica.py` regeneró portada y TSV sin variar el inventario fuente (`399726f7b9da30f0ebae821079bef9fc554dbdc114facba117f4633356c922e7`).

Tras la fusión de #1086, `python3 tools/celdas_validadas.py --linea` entrega **219** (antes 92). Siete de las nueve celdas-D de crédito de #1058 están PUNTUADA y aportan 111 celdas; k4a/k4b quedan SKIP. Otras 16 proceden de ENCIG 2025. La NC de P3 de crédito está CERRADA por `ADR-260923-GEN2-CONTADORES-CONSUMO-1-988c-01`. Es validación contable de celdas, no firma de adopción ni consumo de sus RESULT por el modelo.

El inventario conserva 52 filas con consumo GEN2 activo, 20 con adopción por firma, 1 242 pisos históricos sin adopción por este catálogo, 120 lecturas selladas por dictaminar, 10 firmas de adoptar pendientes de consumo y 2 vetos. La matriz AMAI no calcula NSE ni activa la regla completa en dos instrumentos. Las reservas de ancho ENIF/ENVIPE/ENCIG, la falta de oferta compatible, K1 y el déficit de drivers por área siguen expresos. La publicación del marcador al canal depende de `FP-260923-GEN2-CONTADORES-CONSUMO-1-988c-01`; esta corrección no lo simula.

## NO-CORRIDO / RESERVAS

- **Qué:** cinco reglas causales respaldadas por cada área. **Por qué:** `NO-VERIFICABLE-AQUÍ`; los RESULT disponibles no distinguen cinco mecanismos por dominio. **Impacto:** el catálogo conserva las lecturas y declara el déficit. **Sucesor:** mediciones por dominio con spec y evidencia de mecanismo.
- **Qué:** adopción o consumo de las celdas-D de crédito. **Por qué:** `DECISIÓN-DE-MESA-PENDIENTE`; #1086 cambió el contador, sin firmar adopción. **Impacto:** los pisos de crédito siguen como contexto. **Sucesor:** firma de mesa y escritor de consumo competente.
- **Qué:** publicación del marcador al canal. **Por qué:** `DECISIÓN-DE-MESA-PENDIENTE` en `FP-260923-GEN2-CONTADORES-CONSUMO-1-988c-01` por origen numérico de dos CALC de GOB-DIGITAL-EXE. **Impacto:** el inventario usa la vista actual con reserva de rezago. **Sucesor:** `GEN2-CONTADORES-CONSUMO-2`.

## CONSUMIDO

PR #1071; #1086 para el contador y la decisión P3; #1058 para las nueve celdas-D de crédito; #1002, #1009 y #1041 para las reservas de marginales. Recibo Codex para Claude: revisar la distinción validación/adopción/consumo, el déficit de mecanismos y la FP de origen numérico antes de fusionar.
