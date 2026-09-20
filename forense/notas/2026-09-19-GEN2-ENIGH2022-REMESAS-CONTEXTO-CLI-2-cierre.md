# Cierre: GEN2-ENIGH2022-REMESAS-CONTEXTO-CLI-2

Fecha: 2026-09-19

## Identidad y alcance

- Worktree: `/home/pc0/mm-gen2-enigh2022-remesas-contexto-cli-2`.
- Rama: `codex/gen2-enigh2022-remesas-contexto-cli-2`.
- `origin/main` al abrir: `ea88cb3b94ad820bcd92a485eae51ce24ef07fae`.
- Base revisada declarada: `6f365928ada3714a02954a7a5be64eb8013ecc9e`, ancestro de la base efectiva.
- CALC reservado: `CALC-ENIGH2022-REMESAS-CONTEXTO-0001`.
- La búsqueda previa en el repositorio, encargos, referencias remotas y PR encontró los antecedentes nacionales de prevalencia e intensidad, pero ningún equivalente de remesas por tamaño de localidad o estrato socioeconómico.
- Se trabajó sólo dentro del perímetro autorizado. No se modificaron manifiesto, gobierno, milpa, motor, `corrida0.py` ni pruebas generales.

## Congelamiento y commits de resultado

- COMMIT-1: `b7eeb48` (`GEN2: congela perfil de remesas por contexto`). Congeló catálogo, universos, estimandos, cuantiles, contrastes, réplicas, semilla, tratamiento de singleton, denominadores nulos y réplicas degeneradas, además del código y las pruebas dirigidas, antes de conocer el resultado contextual.
- COMMIT-2: `feed7d5` (`GEN2: sella resultado de remesas por contexto`). Conservó la primera corrida, el RESULT, las tablas y el sello.
- Evidencia de replay: `24a51b8` (`GEN2: asienta replay dirigido de remesas`).
- Sello: `9aa50b55b7a1bfa5aca04a7026b3287a1cf0cb1f457aaff25592385ae8e81a94`.

La fuente fue `enigh2022_nc_csv`, hash `3b2b0bc9c95323b470608113d2902ff3a832764367135f136270b4ce092c9e06`. El diccionario confirmó que remesas, `ing_cor`, `tam_loc`, `est_socio`, factor y diseño pertenecen al mismo registro de `concentradohogar`; la llave `folioviv+foliohog` fue única y no se necesitó enlace.

## Resultado principal

El universo nacional contiene 90,102 hogares, con masa ponderada 37,560,123. Hubo 5,208 hogares receptores, masa 1,716,276. No hubo remesas inválidas, receptores sin `ing_cor` válido positivo, ni incompatibilidades `remesas > ing_cor + 0.01`. Los residuos de clasificación de localidad y estrato fueron vacíos, pero se publican.

Contrastes predefinidos, calculados con réplicas compartidas:

| Comparación | Estimando | Diferencia | IC 95% |
|---|---:|---:|---:|
| Localidad 4 (menor) − 1 (mayor) | prevalencia | 0.083903 | [0.077192, 0.090774] |
| Localidad 4 − 1 | participación media | 0.124560 | [0.100604, 0.149336] |
| Localidad 4 − 1 | proporción ≥ 50% | 0.147053 | [0.109260, 0.185640] |
| Estrato 1 (inferior) − 4 (superior) | prevalencia | 0.079816 | [0.071981, 0.088050] |
| Estrato 1 − 4 | participación media | 0.185546 | [0.148856, 0.222186] |
| Estrato 1 − 4 | proporción ≥ 50% | 0.244787 | [0.192428, 0.289108] |

Las tablas conservan todas las categorías intermedias. La lectura distingue frecuencia de recepción e intensidad condicional y no atribuye causalidad, protección o dependencia; `est_socio` no se presenta como pobreza ni decil.

## Diseño, controles y reproducción

- Marco completo conservado: 560 estratos de diseño y 10,211 UPM; cero estratos singleton.
- Precisión: 2,000 réplicas comunes PSU-dentro-de-estrato, PCG64, semilla `20260919`; las 2,000 réplicas fueron válidas para cada contraste.
- Los controles nacionales reprodujeron los antecedentes sobre universos idénticos: prevalencia 0.0456941; monto medio 14,455.43; mediana 8,310.32; media de participaciones 0.304923; razón de sumas 0.274688; proporción ≥ 50% 0.241461.
- El cálculo focal independiente de la media dio 14,455.429835947132 y EE linealizado 386.341958.
- Dos verificaciones consecutivas devolvieron `REPRODUCE (CONTEXTO=IDENTICO · RESULTADO=REPRODUCE)`, con 11/11 resultados y 6/6 entradas.
- La prueba propia cubrió desconocidos, negativos y ceros; cuantiles; reconstrucción; diferencia entre media de cocientes y cociente de sumas; dirección/replicación compartida de contrastes; y conservación de incompatibilidades.

## Proyección de vistas

Se ejecutó la interfaz de registro con lote limitado al CALC propio y sin `--verifica`:

`python3 tools/corrida0.py registro --escribe --lote CALC-ENIGH2022-REMESAS-CONTEXTO-0001`

La proyección escrita produjo 228 filas en `corridas.tsv`, 8,940 en `resultados.tsv` y 228 en `usos.tsv`. Una segunda proyección, sin escritura, reportó cero diferencias en las tres vistas. No se ejecutaron replays ajenos ni se eligió manualmente un lado de los TSV.

Las vistas compartidas de la base efectiva ya estaban rezagadas respecto de los CALC presentes en el árbol; por ello la regeneración integral de la interfaz incorpora también ese arrastre derivado. Se conserva porque el mandato exige regenerar las vistas compartidas al integrar y la segunda proyección es estable. Las advertencias heredadas quedan fuera de este perímetro.

El CALC y sus 11 resultados permanecen `PENDIENTE-DE-MESA`; no se creó uso ni adopción. No se hizo merge.
