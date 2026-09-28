# CONTRATO-TOLERANCIAS · ENDUTIH/MOCIBA de C1 · R22

`ACTO GEN2-C1-SUCESORES-Y-LOTE-3`, P2 · `FP-260926-GEN2-ASTRA6-C1-IMPEDIMENTOS-LOTE2-fb50-04` · 28/sep/2026. Congelado por el sha256 de este archivo y de su tabla. **Tras P2 no se cambia** (encargo §7 d). Una corrección se hace en un contrato sucesor con sello nuevo.

## Firma de mesa, verbatim

`forense/encargos/2026-09-28-GEN2-TRAMITE-FIRMAS-21-ADENDA-1.md`, R22 **(1)**: «Fijo las tolerancias por identidad ENDUTIH/MOCIBA: proporciones abs 1e-8 rel 0, enteros y estados exactos, pesos expandidos abs 1e-8 / rel 1e-12; el plan de IC va aparte. No abre reserva ni adopta.»

## Regla

| Clase | Aplica a | abs | rel |
|---|---|---|---|
| PROPORCION | `punto` con `unidad = proporcion`, en escala 0–1 (no se reescala a porcentaje) | 1e-8 | 0 |
| ENTERO-EXACTO | conteos y enteros | 0 | 0 |
| PESO-EXPANDIDO | totales expandidos con factor | 1e-8 | 1e-12 |
| Estados de fila y de IC | `estado`, `estado_ic`, motivos | comparación literal | — |

Se pasa si `|Δ| ≤ abs + rel·|referencia|`. IC: plan aparte. Bajo R23 el protocolo inferencial es diagnóstico, y sin el margen de equivalencia que fije mesa los extremos de IC se reportan pero no adjudican.

## Universo, derivado por comando

`python3 forense/validacion-independiente/catalogo-1-sucesores/r22_tolerancias.py <salida>` lee `estimandos.tsv` de los ocho contenedores de `catalogo-1-preparacion-lote2/entradas/` (solo identidad y unidad; ningún valor) y escribe `r22-tolerancias-por-identidad.tsv`: **1 797 identidades**, todas `proporcion` → PROPORCION.

| Paquete | Identidades |
|---|---:|
| endutih-empleo-15mas-2023-0001 | 46 |
| endutih-empleo-15mas-2024-0001 | 46 |
| endutih-empleo-15mas-2025-0001 | 46 |
| endutih-pisos-2023-0001 | 470 |
| endutih-pisos-2024-0001 | 470 |
| endutih-pisos-2025-0001 | 470 |
| mociba-pisos-2016-0001 | 126 |
| mociba-pisos-2017-0001 | 123 |

Los ocho contenedores traen hoy `tolerancia.json = {"tipo": "texto"}` (comparación de cadena). Esta tabla es lo que la sustituye para un intento futuro: un paquete sucesor lleva la fila de cada llave, no el `tolerancia.json` viejo. El sha256 del contenedor de cada fila fija a qué entrada se refiere.

## Lo que no hace

No abre ENDUTIH 2025 (sigue reservada), no lanza ninguna comparación, no adopta y no toca los contenedores. La propuesta de lote 2 (`catalogo-1-preparacion-lote2/preparacion/p1/p1-propuesta-tolerancias.md`) queda como antecedente; donde difiera, manda este contrato.
