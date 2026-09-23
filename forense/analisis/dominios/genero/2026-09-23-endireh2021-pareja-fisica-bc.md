# ASTRA5-U2 · ENDIREH · Pareja física B1/B2/C1 2021

Estado: **procedimiento sellado**. Medición descriptiva retrospectiva, sin inferencia causal ni adopción.

- CALC: `CALC-ENDIREH-PISOS-2021-PAREJA-FISICA-BC-0001`; COMMIT-1 `973d67f34db157924bbd5e1ae4dc8f0bb6b78621`.
- `preflight` verde; `run` selló; `verify` **REPRODUCE** (2/2 RESULT).
- `resultados.json` SHA256 `51af312d94b053998bd12095d0444fc750da0c81260db12b55aec2b6970037a1`; sello `36ccd2d347323ec0c785da51bbae59e8915afd880b730aaa6b1de9ca5a361159`.
- [endireh2021-pareja-fisica-bc-tabla.tsv](endireh2021-pareja-fisica-bc-tabla.tsv): 94 celdas, 94 publicables; RESULT `RESULT-ENDIREH2021-PF-BC-TABLA` conserva réplicas agregadas.

| Ventana | Universo conocido | Prevalencia unión de actos | IC95 de diseño |
|---|---:|---:|---:|
| vida | 36,676 | 18.5683% | 18.0114–19.0651% |
| desde_octubre_2020 | 36,675 | 3.0915% | 2.8364–3.3517% |

Unidad mujer de 15+; factor `FAC_MUJ`; diseño `EST_DIS`/`UPM_DIS`. IC bootstrap por UPM completas dentro de estrato, con dominios de contribución cero. Elegibilidad y códigos de actos están congelados en `spec.md`/`medidor.py`. Un acto es unión de reactivos; salto, no aplica, NS y no respuesta quedan fuera del denominador conocido.

Supresión predefinida por soporte, UPM, CV y ancho de IC; las celdas no publicables figuran sin punto en la tabla. Cortes por edad, escolaridad, localidad, pareja y entidad son estimaciones de dominio. La ventana reciente depende de la redacción del instrumento. No se identifica subregistro ni causalidad. El agregado U0 de 70.1% no se contrasta directamente con este componente.

Origen numérico: microdatos primarios INEGI registrados en manifiesto; GEN1 sólo orientación. La tabla está sellada en disco, pendiente de registro de publicación.

La fila nacional de este CALC reúne únicamente B1/B2/C1 y mezcla situaciones de pareja distintas; la lectura sustantiva usa las filas por instrumento. Vida de la relación: B1 37.1538% (n=12,598), B2 21.6617% (n=9,553), C1 4.9741% (n=14,525). Desde octubre 2020: B1 5.7169% (n=12,598), B2 0.8501% (n=9,552), C1 2.4017% (n=14,525). Los IC95, RESULT, hash y soporte de cada una constan en la tabla TSV. B pregunta por expareja también después de la separación; C1 por relación actual o última. Ninguna de estas filas se suma a la A1/A2 ni implica prevalencia para C2.
