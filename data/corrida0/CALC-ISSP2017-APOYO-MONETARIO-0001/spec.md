# Spec fijada · ISSP México 2017, apoyo para pedir prestada una gran suma

Estado: `FIJADA-ANTES-DE-ABRIR-FILAS`. Operación descriptiva nueva autorizada por `GEN2-ISSP-APOYO-MONETARIO-DESCRIPTIVO-CLI-1`. No ejecuta F6, M o L; no calibra ni valida el motor. El objetivo tiene exposición histórica documentada y la operación no es ciega.

## Pregunta y estimandos

El instrumento mexicano pregunta en Q8a a quién o dónde acudiría primero la persona si necesitara pedir prestada una gran suma de dinero. La variable integrada acreditada es `v26`.

Se estiman, para México total adulto, hombres y mujeres, siete proporciones ponderadas entre respuestas válidas (`v26=1..7`), conservando categorías con cero casos. Se publica además la cobertura y el contraste descriptivo mujeres menos hombres para el código 1. Los tres dominios pertenecen a una sola muestra.

## Fuente, versión y correspondencia

- Estudio: ISSP 2017, *Social Networks and Social Resources*, ZA6980 v2.0.0, DOI `10.4232/1.13322`; universo integrado: personas de 18 años o más (con excepciones para otros países que no incluyen México).
- Informe integrado oficial GESIS: *Variable Report 2019/13*, publicación documental 2019-08-19, página impresa 60. Vincula expresamente `v26` con Q8a y publica los códigos 1–9.
- Cuestionario mexicano `ZA6980_q_mx.pdf`, PDF p.3 / impresa p.2: contiene Q8a y las mismas categorías en español.
- `ZA6980_backgroundvar_mx.pdf`: acredita `SEX` (`1 Male`, `2 Female`, `9 No answer`), edad mínima construida 18 y `WEIGHT=1 No weighting`; declara que México no aplicó ajuste por probabilidades desiguales ni por no respuesta.
- DTA y SAV integrados: 44,492 filas y 356 columnas; ambos llevan la etiqueta `v26 = Q8a Whom or where to ask for help: borrow large sum of money?` y el mismo conjunto de etiquetas de valor. La corrida usa el DTA y verifica metadatos del SAV sin materializar sus filas.

## Columnas y selección cerradas

Únicas columnas leídas del DTA: `studyno`, `doi`, `version`, `country`, `c_alphan`, `CASEID`, `SEX`, `AGE`, `WEIGHT`, `v26`. Se selecciona México con la conjunción `c_alphan == "MX"` y `country == 484`; `studyno=6980`, `doi="doi:10.4232/1.13322"` y `version="2.0.0 (2019-08-19)"` deben coincidir exactamente con la identidad embebida. La unidad es una persona entrevistada. El universo adulto viene del diseño del estudio; `AGE` sólo controla que ninguna edad observada sea menor a 18 y no excluye la no respuesta de edad.

Dominios: `TOTAL` incluye toda la muestra México; `HOMBRES` requiere `SEX=1`; `MUJERES`, `SEX=2`. `SEX=9` o vacío permanece en el total y se conserva como sexo no clasificable para reconstrucción; no entra a los dominios por sexo.

## Códigos, peso y denominadores

| Código | Texto integrado acreditado | Texto mexicano | Tratamiento |
|---:|---|---|---|
| 1 | Family members or close friends | Familiares o amigos cercanos | sustantiva |
| 2 | Other persons | Otras personas | sustantiva |
| 3 | Private companies | Compañías privadas | sustantiva |
| 4 | Public services | Servicios públicos | sustantiva |
| 5 | Non-profit or religious organisations | Organizaciones sin fines de lucro o religiosas | sustantiva |
| 6 | Other organisations | Otras organizaciones | sustantiva |
| 7 | No person or organisation | Ninguna persona u organización | sustantiva |
| 8 | Can't choose | No puedo elegir | exclusión separada |
| 9 | No answer | No respuesta | exclusión separada |

El vacío de sistema se clasifica con el código 9 como `NO_RESPUESTA`. No se admite otro código observado. El código 7 es respuesta sustantiva; el 8 no se recodifica como ausencia de apoyo.

El ponderador es `WEIGHT`. Debe ser numérico, finito y estrictamente positivo; los casos que fallen se clasifican primero como `PESO_INVALIDO` y no aportan masa ni respuesta a los otros estados. No hay recorte, winsorización ni ajuste de extremos. Entre casos con peso válido, la clasificación exclusiva es `VALIDA` (`1..7`), `NO_PUEDE_ELEGIR` (`8`) o `NO_RESPUESTA` (`9`/vacío). Así, para cada dominio, `elegibles = peso inválido + válidos + no puede elegir + no respuesta`.

El punto por categoría es la razón de masas `sum(WEIGHT * I[v26=k]) / sum(WEIGHT * I[v26 in 1..7])`. La cobertura ponderada es masa válida / masa elegible con peso utilizable. Si un denominador es cero, punto y cobertura quedan vacíos con estado explícito.

## Precisión y contraste

La documentación disponible acredita el ponderador, pero no identificadores ejecutables de UPM o estrato para México. Por ello todos los puntos y el contraste se rotulan `EE-IC-NO-DISPONIBLES-DISENO-NO-ACREDITADO`. No se sustituye iid, Kish, bootstrap de personas ni suma de varianzas entre dominios.

El contraste es `p(v26=1 | MUJERES) - p(v26=1 | HOMBRES)`, en proporción y puntos porcentuales. Preserva la categoría conjunta familiares/amigos; no separa los vínculos ni identifica un efecto causal de género.

## Controles y límites

El medidor exige identidad y hashes, miembros ZIP exactos, llaves únicas dentro de México, catálogo cerrado, particiones y reconstrucción del total desde hombres, mujeres y sexo no clasificable. Un script separado, que no importa el medidor, recalcula puntos y denominadores. La reproducción se hace desde inputs identificados y el sello no depende de archivos de resultado preexistentes.

La salida permite describir a quién acudirían primero los adultos entrevistados en México en este módulo. No mide recepción efectiva de dinero, apoyo exclusivamente familiar, disponibilidad real del préstamo, causalidad, México en otra fecha ni una validación independiente del modelo.
