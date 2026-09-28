# Cierre editorial · síntesis transcultural

**EJECUTADO.** [PR #1247](https://github.com/Josanoforo/Modelado-Mexicano/pull/1247) abierto, sin fusión ni recibo atribuidos. Report general v2 completo, tabla de afirmaciones, índice de los 31 originales, hoja de cuatro reglas candidatas y solicitud de recibo. El corte inicial `eda5bb9f` se refrescó por fast-forward a `a8c3e341` cuando #1243 y #1240 fusionaron siete reports; el texto general integra su precisión de Smith 2017. No se editó v1, mapa, catálogo, CALC, motor, manifiesto ni CI; cero mediciones, celdas y adopciones nuevas.

| Producto | Resultado usable | Límite |
|---|---|---|
| [Síntesis v2](../../../../corpus/reports-v2/Psicología__Conducta_y_Sociedad_en_el_México_Contemporáneo__Análisis_Transcultural_y_Estructural.md) | Descripción con estimandos separados; inferencias causales y comparaciones acotadas; condiciones que cambiarían la conclusión | No valida C1 ni prueba eficacia de reglas |
| [Tabla](tabla-afirmaciones.tsv) | 28/28 identidades del mapa y 77 tesis adicionales; 2 CONFIRMA, 61 MATIZA, 22 ROMPE, 20 SIN-CIFRA | Los 22 ROMPE requieren revisión humana de contenido; las fuentes heredadas que no se reabrieron no se presentan como lectura primaria |
| [Índice](../../../../corpus/reports-v2/INDICE.md) | 31 filas originales con hash, estado, tabla, conteos, recibo y reglas en columnas separadas | 24 en main, 3 en PR ajenos, este report propuesto en rama y 3 no entregados al último refresco |
| [Hoja](hoja-reglas-propuestas.md) | Cuatro decisiones con consumidor, condición, evidencia, tier y falsador | Propuesta sin firma de contenido ni adopción |

**INTERPRETACIÓN-DECLARADA.** El encargo decía que #1243 estaba abierto y main tenía 17 homónimos; la consulta remota y el fast-forward mostraron que #1243 ya había fusionado, dejando 21. El índice da el estado remoto vigente y no suma archivos de los PR abiertos. Se retuvo el historial del cuerpo original del encargo y se añadió solo cierre al pie.

**LEÍDO.** Original de 328 líneas y mapa por identidad; reports v2 fusionados pertinentes; fuentes primarias públicas para WVS 7, GLOBE, Culture Factor, WHR 2025, ENOE, ENSANUT, familia, trabajo, violencia y la precisión de Smith trazada al report de interacción fusionado. Los enlaces a fuente indican alcance de lectura. No se buscó dato de última ola reservada. Los tres adjuntos embebidos del encargo coincidieron con sus SHA-256 declarados.

**VERIFICACIÓN EJECUTADA.** `tabla-producir.py` y `tabla-verifica.py`: 105 decisiones, 28/28 mapa; `indice.py --verify`: 31 nombres/hashes y estados 24/3/1/3, enlaces locales válidos; `python3 tests/check.py --rapido`: 0 FAIL, 624 WARN heredados; `tools/sella_sha256.py --cuerpo --verifica`: sello del cuerpo coincide. Son controles de trazabilidad y repositorio, no mediciones científicas.

## NO-CORRIDO / reservas puntuales

| Objeto | Razón | Efecto y sucesor |
|---|---|---|
| Tres homónimos pendientes: duelo ambiguo y dos genéticos | Otros encargos, sin report fusionado o propuesta comprobada al corte | Índice dice NO-ENTREGADO; al fusionar, actualizar solo esas filas, conteos y enlaces. Firewall genético sigue vigente. |
| Tres reports propuestos en #1242 | PR abierto, sin fusión | Índice dice EN-PR; no se importan como adopciones. Actualizar sus filas cuando main los incluya. |
| Revisión humana de los 22 ROMPE y recibo de Claude | Circuito de recepción pendiente | No se afirma dictamen independiente, adopción ni cierre de C3. [Solicitud](recibo-para-claude.md). |
| Mecanismos de compensación familiar, superioridad estructural y singularidad cultural | Los objetos disponibles no los identifican | Conclusiones causales acotadas; diseños discriminantes en el report y la hoja. |

## CONSUMIDO

El encargo `ASTRA6-C3-SINTESIS-TRANSCULTURAL-1` queda consumido por esta propuesta editorial, sujeto al recibo y decisión de mesa. La autorización citada es la misión/adenda acordada en el cuerpo archivado; este cierre no inventa otra firma ni fusiona o adopta por sí mismo.
