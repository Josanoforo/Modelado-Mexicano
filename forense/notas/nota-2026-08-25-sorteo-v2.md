# Nota · `ACTO SORTEO-V2-PROPUESTA`, 25/ago/2026 (`FP-145`, `L9-c`)

Entorno **NUBE** (`cloud_default`). Sin red externa ni microdato. Encargo archivado: `forense/encargos/2026-08-25-SORTEO-V2-PROPUESTA.md` (`CONSUMIDO`).

## Qué se hizo

Se redactó `forense/prereg-duelo-v2/sorteo-act-pil-3-v2-PROPUESTA.md` ejecutando la opción `c` que `L9`/`FP-133` firmó (`ADR-168(h)`, `canon/gobernanza-v1_15.md:3351`): el marco de 60/50 no se poda ni se re-congela; el sorteo se diseña para respetar el tope del 20% de `ADV1-M1` sin tirar candidatas. **Ningún sorteo real corrió** — el documento es una propuesta de algoritmo, no una ejecución.

Contenido del documento (resumen; ver el propio archivo para el detalle completo):

1. **Estado verificado del marco** (26 estratos, 28 `SI`/24 `NO`/8 `PENDIENTE-FUERA-DE-INDICE` de 60; marcador puntuable 50 = `P1`(17)+`P2`(33)), derivado por comando (`awk` sobre `forense/marco-candidatas-piloto-v1_0.tsv`), no supuesto.
2. **Algoritmo determinista** con la cuota `floor(0.20*n_sorteo)` como restricción dura del muestreo (postcondición verificada, no objetivo blando): asignación de asientos por estrato (Hamilton/mayor resto), sorteo de no-publicadas primero, publicadas solo hasta agotar presupuesto de cuota.
3. **Regla de infactibilidad por estrato**: un estrato con asiento asignado y cero filas `NO` es infactible por aritmética; fallback declarado (asientos se reasignan a estratos factibles, el estrato infactible sale con 0 asientos y se registra, nunca se relaja la cuota para acomodarlo).
4. **Protocolo de semilla**: no un número fijo — `semilla = int(sha256(sha_merge_hex).hexdigest(),16) % 2**63`, derivada del SHA de merge del acto que congele marco+sorteo (reutiliza `derivar_seed_scope` de `forense/prereg-duelo-v2/scoring-adv1-m3.py:685`, mismo patrón que ya deriva semillas hijas en el repo). `867948c` (anulada por `ADR-135(d)`) queda citada como antecedente histórico, no reutilizada.
5. **Interacción con P0/P1/P2**: el sorteo opera solo sobre el marcador puntuable (`P1`∪`P2`); `P0` (10 filas, anexo de plomería) queda fuera, mismo criterio que `canon/estado-programa-v1_10.md:99` ya declara.
6. **Interacción con las 8 `PENDIENTE-FUERA-DE-INDICE`**: elegibles para el sorteo **solo si `FP-146` las resuelve a `SI`/`NO` antes** — mientras tanto se excluyen del universo elegible, no se tratan como `SI` ni como `NO` por default.
7. **Pseudocódigo verificable** (§2.1-§2.3 del documento).
8. **Tres casos de prueba concretos** con estratos y números de ejemplo: caso normal (cuota no se agota), caso de infactibilidad por estrato (dos estratos 100% publicados, fallback reasigna sus asientos), caso límite del 20% (la cuota se toca exacto en el tope, `<=`, válido).

## Tablero

`FP-145` marcado **ejecutada** (`ejecutada_en` = 2026-08-25, este acto) en el sentido que el encargo declara: la propuesta fue redactada, el sorteo no se realizó. Fila nueva `A.12`: `FP-150` (`ABIERTA`), *«mesa sella sorteo-v2»*, apuntando a la propuesta.

## Lo que este acto NO hace

No corre ningún sorteo, real ni simulado. No amplía el marco de 60 (`AUTORIDAD-SEMANTICA-MARCO` pendiente, declarado en `PROPAGA-330-337`). No resuelve las 8 `PENDIENTE-FUERA-DE-INDICE` (`FP-146`, acto aparte, no ejecutado aquí). No modifica `forense/marco-candidatas-piloto-v1_0.tsv`. No toca `milpa/`. No toca ningún directorio de espejo (no existe tal directorio en el árbol, verificado en `PROPAGA-330-337`).
