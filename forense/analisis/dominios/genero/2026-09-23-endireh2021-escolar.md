# ASTRA5-U2 · ENDIREH · Ámbito escolar 2021

Estado: **procedimiento sellado**. Medición descriptiva retrospectiva, sin inferencia causal ni adopción.

- CALC: `CALC-ENDIREH-PISOS-2021-ESCOLAR-0001`; COMMIT-1 `88f3eba4166bf34596b7fe6ddad0531ffd47cfb5`.
- `preflight` verde; `run` selló; `verify` **REPRODUCE** (2/2 RESULT).
- `resultados.json` SHA256 `16bda30b84b25a621cd51f3a6d5ae9583148ccb4aae93deff60646037910a4fa`; sello `34e66f6b6cc8ed6a758d60df95f834640a1a366e1ffba32f9295a2fb5d423994`.
- [endireh2021-escolar-tabla.tsv](endireh2021-escolar-tabla.tsv): 100 celdas, 96 publicables; RESULT `RESULT-ENDIREH2021-ESC-TABLA` conserva réplicas agregadas.

| Ventana | Universo conocido | Prevalencia unión de actos | IC95 de diseño |
|---|---:|---:|---:|
| vida | 104,212 | 32.2558% | 31.8329–32.7362% |
| desde_octubre_2020 | 11,092 | 20.1903% | 19.0958–21.0655% |

Unidad mujer de 15+; factor `FAC_MUJ`; diseño `EST_DIS`/`UPM_DIS`. IC bootstrap por UPM completas dentro de estrato, con dominios de contribución cero. Elegibilidad y códigos de actos están congelados en `spec.md`/`medidor.py`. Un acto es unión de reactivos; salto, no aplica, NS y no respuesta quedan fuera del denominador conocido.

Supresión predefinida por soporte, UPM, CV y ancho de IC; las celdas no publicables figuran sin punto en la tabla. Cortes por edad, escolaridad, localidad, pareja y entidad son estimaciones de dominio. La ventana reciente depende de la redacción del instrumento. No se identifica subregistro ni causalidad. El agregado U0 de 70.1% no se contrasta directamente con este componente.

Origen numérico: microdatos primarios INEGI registrados en manifiesto; GEN1 sólo orientación. La tabla está sellada en disco, pendiente de registro de publicación.
