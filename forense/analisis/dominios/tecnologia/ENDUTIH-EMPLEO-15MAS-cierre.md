# ENDUTIH · cierre del sucesor de `actividad_empleo`

Corrección de PR #1085, 23/sep/2026. **Los tres RESULT originales `CALC-ENDUTIH-PISOS-2023/2024/2025-0001` permanecen sellados como evidencia histórica del primer procedimiento.** Sus 141 celdas de `actividad_empleo` dejan de alimentar el producto utilizable. Las sustituyen 141 celdas de `CALC-ENDUTIH-EMPLEO-15MAS-2023/2024/2025-0001`, con contrato humano congelado en `forense/prereg-caja/ENDUTIH-EMPLEO-15MAS-spec-v1_0.md` y COMMIT-1 `08353948`, antes del primer run del sucesor. Primeros sellos: `70975942` (2023), `c0fdbed4` (2024), `099e9f13` (2025). Los tres `verify` devolvieron `REPRODUCE`, `CONTEXTO=IDENTICO`; asientos en `forense/replay-evidencia.tsv`.

## Evidencia del filtro

El cuestionario 2024 `endutih2024_cuestionario_pdf` de PR #1082, SHA256 `95514c5fe0a000bfaf29062a9cf9225ec64674dbb83df6a44a3dceda13187800`, y los [cuestionarios oficiales 2023](https://www.inegi.org.mx/contenidos/programas/endutih/2023/doc/CENDUTIH2023.pdf) y [2025](https://www.inegi.org.mx/contenidos/programas/endutih/2025/doc/CENDUTIH2025.pdf), indican expresamente «solo para [la persona] elegida de 15 años o más» en 7.10.02. Los FD locales verificados repiten ese texto: `tic_2023_usuarios` fila 167, `tic_2024_usuarios` fila 167, `tic_2025_usuarios` fila 201. `P7_1=1` fija uso de internet en los últimos tres meses; el estimando es búsqueda de información sobre empleos o bolsas de trabajo entre usuarios de internet **15+ con edad conocida**. Las respuestas 1/2 son Sí/No. Los blancos de usuarios 6–14 son `SALTO` estructural, no `NR` ni `NO`.

La inspección diagnóstica de `P7_1`, `P7_10_2` y `EDAD` por ola confirmó que **todos** los blancos entre usuarios eran menores de 15: 5,886/5,886 en 2023, 6,019/6,019 en 2024, 6,017/6,017 en 2025. Entre usuarios elegibles de 15–97, blancos observados: **0/0/0**. El primer cálculo ya excluía esos blancos del denominador por respuesta válida, pero rotulaba indebidamente la tasa como de usuarios 6+ y clasificaba el salto etario como `NR`. Incluía además 96/111/92 respuestas 1/2 de personas con `EDAD=98/99` (edad no especificada), cuya pertenencia a 15+ no se acredita; el sucesor las excluye de su universo.

| Ola | CALC anterior: punto, n | CALC sucesor: punto [IC95], n | Cambio del denominador |
| --- | ---: | ---: | ---: |
| 2023 | 25.878% · 40,745 | **25.907% [25.237, 26.548] · 40,649** | −96 de edad no especificada |
| 2024 | 25.331% · 41,221 | **25.373% [24.725, 26.068] · 41,110** | −111 de edad no especificada |
| 2025 | 23.512% · 42,701 | **23.522% [22.888, 24.160] · 42,609** | −92 de edad no especificada |

`tabla-principal.tsv` sustituye únicamente sus tres filas `actividad_empleo/TOTAL`: `ESTIMABLE`, universo «usuarios internet 15+ edad conocida», id y SHA256 de cada RESULT sucesor. Las 42 filas del catálogo principal permanecen; para ENDUTIH el producto utilizable es **1,410 celdas** de las 10 medidas originales no afectadas más **141 celdas** del sucesor = **1,551** (1,548 estimables y 3 suprimidas por `n<100`, una `EDAD_06_11` por ola). Las 141 celdas originales de empleo se conservan sólo como evidencia, **no se suman** a la cobertura utilizable. `EDAD_12_17` contiene respuestas elegibles de 15–17 y se interpreta con esa restricción.

## Calibración

La frase del spec/cierre original «dos transiciones no permiten ajuste y evaluación separados» era incorrecta. Dos transiciones permiten asignar una al ajuste y otra a la evaluación. Una sola transición de ajuste no estima de forma estable la distribución de errores ni un cuantil extremo para IC predictivo; una sola de evaluación no identifica cobertura con precisión. El cambio de composición entre olas agrega incertidumbre. Por eso el estado sigue `SIN-HISTORIA-PARA-CALIBRAR`: los IC publicados son **de diseño muestral**, no predictivos, y no se anuncia detección de cambios. El spec original permanece byte a byte por su sello; este párrafo y el spec sucesor son la errata explícita.

**Auditoría de rigor extremo.** Buscar información sobre empleos no equivale a estar desempleado ni a conseguir trabajo. La tasa es condicional en acceso y uso de internet, y no atribuye motivos a quienes no lo usan. No se unen individuos entre olas.
