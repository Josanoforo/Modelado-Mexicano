# Nota de cierre · ACTO GEN2-REGLAS-Y-RESULT-1 · 28/sep/2026

Contador: **cero mediciones; no adopta** (0 contadores movidos). NUBE; base `16ba3d02` (encargo redactado en `723b62c1`, ancestro); 0-bis `a3cc048f`.

## Universo (P1) — patrón declarado
`\bSI\b.{0,300}ENTONCES` por línea física (EJECUTADO, `p1_universo.py`). Líneas con patrón: reports v1 41 (en 5 de 31 archivos; los otros 26 no traen reglas SI-ENTONCES por este patrón; búsqueda de `IF…THEN` en v1: 0), reports v2 103 (29 archivos), integrador 4 (las 4 son menciones metodológicas de «reglas SI-ENTONCES», no reglas: 0 filas). Tabla C3-1: 107 filas. Tras fundir por llave de texto normalizado: **162 reglas** (107 tabla + 31 v2 no citadas por la tabla + 24 v1). Duplicados fundidos citan todas sus fuentes en `fuentes`.

## Contraste (P2/P3)
Cinco subagentes por grupo de dominio contra `canon/catalogo-del-mexicano-v1_3.tsv` (índice de 10 238 combinaciones). Validación (`p4_ensambla.py`, EJECUTADO): ids sin fila 0 · dictamen vacío 0 · CONFIRMA/ROMPE sin `resultado_id` en `resultados.json`+`sello.json` 0. Dictámenes: CONFIRMA 2 · MATIZA 4 · MATIZA-SIN-CRUCE 6 · ROMPE 0 · INCOMPARABLE 0 · SIN-CIFRA-GEN2 150. Solo (b)/(c): 39.

## Auditoría v2.16
Procedencia por regla en columna; unidad por cifra (hogar en RG-afa48731c6, persona en RG-33ece9e072, delito y trámite en dos MATIZA, sin promediar); ¿incentivo o psicología? y ¿clase media urbana? como columnas; todo RETROSPECTIVO, nada PROSPECTIVO; ninguna afirmación del corpus tecleada: todos los conteos salen de los dos scripts.

## Reservas
- 143 SIN-CIFRA son NO-CONSTRUIBLE por naturaleza prescriptiva o de mecanismo: el dictamen es de subagente con revisión por muestra del hilo principal, no fila a fila.
- `milpa/catalogo-momentos` no consume ninguna de las 162 (grep por texto/id); los momentos R1.4…R10.3 son reglas del motor, no de reports.
- Ajustes de guarda: fila FP para la hoja (T22) y exclusión T30 (la cita R1.4 del encargo es ilustrativa).

## Revisión R2 (adversarial) y R3 (decisiones del usuario, 28/sep)
- R2: cinco revisores fila por fila, con ≥3 términos de búsqueda por regla en el índice. Cambios: RG-21c3d453f6 y RG-b3349eadb3 → MATIZA-SIN-CRUCE; RG-709601ed63 y RG-160683e479 → CONFIRMA (solo SI; la primera pasada decía, en falso, que no había RESULT). Se corrigieron premisas de detalle en RG-7cae748adc, RG-8cfef06376, RG-192242b257 y RG-b57dbe6ebb (existían RESULT que la primera pasada daba por ausentes; los dictámenes se ratifican). G3: 8 de 30 reglas leídas completas, 22 juzgadas por resumen (reserva).
- R3, respuesta verbatim del usuario: «Fundir en una fila (Recomendado)» · «MATIZA, fuera del bloque (Recomendado)» · «RG-55c7a10915 queda MATIZA,RG-df62e016a7 a MATIZA». RG-4fc3bce5d1 no se marcó: sigue SIN-CIFRA-GEN2.
- Criterio de CONFIRMA: el usuario respondió «Dame el input para hacer web search, edge cases y best práctices para el manejo de estos resultados.» → `prompt-criterio-confirma.md`; decisión pendiente (NC-…-a3cc-03).
- Conteo final: CONFIRMA 3 filas = 1 regla · MATIZA 6 · MATIZA-SIN-CRUCE 8 · ROMPE 0 · INCOMPARABLE 0 · SIN-CIFRA-GEN2 145. Tier: 21 declarados que no aguantan (`tier-declarado-vs-evidenciado-v1_0.tsv`), heurística de normalización del tier declarado (texto libre) declarada en la tabla.
- Defecto de la llave P1: la llave por texto normalizado no funde paráfrasis (tres redacciones de la regla de alimentos); se fundieron a mano como VARIANTE-DE.
