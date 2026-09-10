# `GEN2-R-COMPLETA-MARCO` — cierre

**Fecha:** 9/sep/2026 · **Entorno:** CAJA, Ubuntu/WSL, Opus · **Compuerta:** contrato TRIADA de `ENCARGO 2/5` presente en la base fusionada · **Motor:** intacto · **L/M:** no leídos durante la medición.

## Resultado

El árbol determinó 6 árbitros R ya sellados y 8 faltantes ejecutables. Los ocho pasaron `spec-check → preflight VERDE → run → verify REPRODUCE/CONTEXTO=IDENTICO`; no hubo celda bloqueada ni sin spec. `UR` queda congelado en **14/14** mediante `universo-triada-v1_1.tsv`; esto amplía el panel disponible al `ENCARGO 5/5`, pero no decide `U3` ni adjudica contendiente alguno.

`codificacion-R-v1_1.tsv` es una copia byte a byte de v1.0 (`sha256 cf5dfb182f3c914fd8a91ce6d589ad745c507a8c3defad2d6459ee876c01f598`). La firma/sucesión vive en su nombre y sidecar: no cambió código, universo, ponderador, estrato, UPM ni estimando después de abrir microdato.

La fila `FP-370` queda `FIRMADA -- EJECUTADA` por la firma de mesa de este encargo y remite a la sucesora byte-idéntica; v1.0 permanece intacta.

## Las 14 celdas

| celda | estado R final | UR | punto R | n | masa ponderada | excluidos | estratos / UPM | IC95 / reserva |
|---|---|---:|---:|---:|---:|---:|---:|---|
| CIV-M-01 | R-YA-SELLADO | SI | control positivo, no re-medido | — | — | — | — | CALC histórico |
| CIV-M-02 | R-YA-SELLADO | SI | control positivo, no re-medido | — | — | — | — | CALC histórico |
| CIV-M-04 | R-YA-SELLADO | SI | control positivo, no re-medido | — | — | — | — | CALC histórico |
| CIV-M-10 | R-YA-SELLADO | SI | control positivo, no re-medido | — | — | — | — | CALC histórico |
| CIV-M-12 | R-YA-SELLADO | SI | control positivo, no re-medido | — | — | — | — | CALC histórico |
| CIV-M-13 | R-YA-SELLADO | SI | control positivo, no re-medido | — | — | — | — | CALC histórico |
| DIN-M-01 | R-YA-SELLADO | SI | 0.15558094338412926 | 19,739 | 68,002,840 | 63 | 1 / 8,050 | [0.1461309873, 0.1650308994]; diseño aproximado, cota inferior |
| FAM-M-01 | R-YA-SELLADO | SI | 0.5571925669683186 | 12,054 | 76,430,133 | 392 | 182 / 1,908 | [0.5439300566, 0.5704550773] |
| FAM-M-05 | R-YA-SELLADO | SI | 0.04745859252351374 | 70,311 | 32,974,661 | 0 | 536 / 7,891 | [0.0449844107, 0.0499327743] |
| FAM-M-06 | R-YA-SELLADO | SI | 0.04728548395278385 | 74,647 | 34,400,515 | 0 | 543 / 8,377 | [0.0449423946, 0.0496285733] |
| FAM-M-07 | R-YA-SELLADO | SI | 0.04377543852935772 | 89,006 | 35,749,659 | 0 | 558 / 10,118 | [0.0417927636, 0.0457581134] |
| TRA-M-02 | R-YA-SELLADO | SI | 0.12602486953090247 | 13,412 | 61,126,927 | 8,107 | 281 / 3,003 | [0.1161074373, 0.1359423018]; 1 estrato con UPM única |
| TRA-M-03 | R-YA-SELLADO | SI | 0.04453797671500066 | 22,081 | 32,965,687 | 10,919 | 180 / 6,510 | [0.0389693871, 0.0501065663]; 1 estrato con UPM única |
| TRA-M-07 | R-YA-SELLADO | SI | 0.07181522879909936 | 39,763 | 51,117,793 | 167 | 353 / 9,190 | [0.0671184263, 0.0765120313] |

Cada CALC nuevo declara `cuenta_gen2=SI` y `FP-370; OBJETO=CALC-R-…:<id_celda>`. Los conteos de faltantes se desagregan en cada `resultados.json`; en estas ocho corridas `N-FALTANTES-EXCLUIDOS` coincide con código excluido y `N-FUERA-UNIVERSO=N-SIN-PONDERADOR=0`.

## Independencia y controles

Los ocho CALC sólo declaran payload, `codificacion-R-v1_1.tsv`, marco v1.3 y el aparato estadístico R existente. No declaran ni abren `corridas-L/`, `corridas-M/`, extractor L, CALC TRIADA ni errores de contendientes. Los seis controles positivos coinciden literalmente en variable, universo, códigos, ponderador, estrato y UPM con la sucesora; no se volvieron a medir. Sólo después del sello se compararon los ocho puntos con `corridas-R/`: ocho deltas exactamente cero. Evidencia tabular: `2026-09-09-GEN2-R-COMPLETA-MARCO-P4-control.tsv`.

## Frontera, NC y sucesor

Ningún target R requiere una fuente nueva: **0 bloqueados, 0 sin spec, 0 NC nuevas**. Se mantienen las reservas estadísticas nombradas arriba. `NC-0143` sigue abierta porque cerrar `U3` requiere los puntos válidos de L y el snapshot M; su habilitador se actualiza para consumir el `UR=14` congelado aquí. Este acto no amplía el panel después de observar quién gana y no realiza comparación triádica.

## Cascada

- Sucesoras: `codificacion-R-v1_1.tsv` y `universo-triada-v1_1.tsv`, ambas con hash.
- Ocho CALC-R nuevos, sellados y reproducibles; vistas de `corrida0` rederivadas. La rederivación global incorporó además el `CALC-DUELO-0001` ya fusionado pero ausente de las vistas; la guardia NC-0094 exigió revalidar tres asientos ajenos y `CALC-M-marco-M-sorteado-v1_3`, sin cambiar ningún CALC: sus estados finales conservaron la evidencia que ya mostraba el árbol.
- `ADR-451`, L0 y rótulo `GEN2-R-COMPLETA-MARCO` registran el acto.
- `ENCARGO 5/5` debe usar este `UR=14` congelado y aplicar, sin ampliarlo, la intersección U3 de la spec TRIADA.
