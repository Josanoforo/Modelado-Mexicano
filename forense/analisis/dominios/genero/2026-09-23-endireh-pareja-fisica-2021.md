# ASTRA5-U2 · ENDIREH 2021 · pareja física A

Estado: **un subcomponente sellado**, programa ENDIREH aún abierto. Este archivo no declara completo el agregado GEN-001 de 70.1% ni las otras olas, ámbitos, ayuda/denuncia o decisiones del hogar.

## Primer resultado y cadena

- `CALC-ENDIREH-PISOS-2021-PAREJA-FISICA-0001`, COMMIT-1 `b1983de2`: primer intento `NO-EJECUTABLE`, `UnicodeDecodeError` al abrir CSV como UTF-8; no sellado. Congelación intacta.
- `CALC-ENDIREH-PISOS-2021-PAREJA-FISICA-0002`, COMMIT-1 `b66a134c`: primer intento produjo 92 celdas dentro del medidor, pero `run` rechazó el valor `list` declarado como `texto`; no sellado. Congelación intacta. Ninguna cifra de ese intento se usa en producto.
- `CALC-ENDIREH-PISOS-2021-PAREJA-FISICA-0003`, COMMIT-1 `e0f94f3b`: mismo estimando y reglas, decodificación Latin-1 y tabla serializada como JSON texto. `preflight` VERDE; `run` selló; `verify` **REPRODUCE**, 2/2 RESULT. Sello SHA256 `ba6c9fbf1872feae42a388542e4a7e23d065c74dc3558602902a96bf56f06fef`, `resultados.json` SHA256 `72bd7015a31173d120009deba8b75713641cb439b03185d5fbec7ec6206b6e9d`.
- `CALC-ENDIREH-PISOS-2021-PAREJA-FISICA-0004`, COMMIT-1 `700ad2b8`: corrige el remuestreo de dominios incorporando UPM de contribución cero. V3 sigue sellada; sus IC de cortes quedan superados. V4 selló y `verify` devolvió **REPRODUCE**, 2/2 RESULT. Sello SHA256 `4de09138c1316c4d6e13a6f95db2dbf6154dd192b6e35a369893603220d53da7`; `resultados.json` SHA256 `2924630885c0577d76bb039a02d6ce039f09ecdd19c9a679aaae0d97df06c067`.

## Tabla utilizable

[endireh2021-pareja-fisica-tabla.tsv](endireh2021-pareja-fisica-tabla.tsv) contiene 92 celdas univariadas V4 (92 publicables bajo umbrales congelados) con RESULT/CALC/hash, punto, IC de diseño, soporte y ventana. Las 500 réplicas agregadas por celda viven en `RESULT-ENDIREH2021-PF-TABLA` del CALC V4 sellado; no incluyen personas ni identificadores de UPM.

| Ventana | Universo conocido | Prevalencia unión de nueve actos | IC95 de diseño |
|---|---:|---:|---:|
| Desde inicio de relación actual | 68,540 mujeres A1/A2 | 15.5953% | 15.2003–15.9944% |
| Desde octubre de 2020 hasta entrevista | 68,537 mujeres A1/A2 | 6.7629% | 6.4633–7.0364% |

Unidad mujer de 15+; factor `FAC_MUJ`; estrato `EST_DIS`, conglomerado `UPM_DIS`; temporalidad **RETROSPECTIVA**. La diferencia de tres respuestas conocidas entre ventanas permanece fuera del denominador reciente. El 70.1% de U0 alude a violencia de cualquier tipo/ámbito y no se contrasta directamente con estas cifras. Etiqueta del componente: **sin contraste directo** del agregado; el subcomponente físico está medido.

La tabla está **sellada en disco, no registrada** hasta que el canal de publicación del registro consuma el CALC y su replay. `forense/replay-evidencia.tsv` tiene el asiento de este verify. No adopción, no causalidad, no atribución individual. El subregistro por silencio, recuerdo y denuncia no puede cuantificarse con este procedimiento.

## NO-CORRIDO / RESERVAS

Sin nueva apertura de otra ola o módulo por este procedimiento. ENDIREH 2003 requiere dictamen documental separado; B/C/General de 2021, las otras olas y los demás ámbitos continúan como piezas independientes del encargo.

## CONSUMIDO

FD y cuestionario A 2021 registrados en manifiesto, documentos de #1082, contrato U0 GEN-001 y notas ENDIREH del 4/ago. Ningún resultado GEN1 fue origen numérico.
