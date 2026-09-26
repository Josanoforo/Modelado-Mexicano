# Estructura — Latinobarómetro 2023 (confianza / capital social)

Informe de ESTRUCTURA (solo metadatos: nombres/etiquetas de variable, etiquetas de valor, filas/columnas). NO se leyó ningún valor de respuesta del microdato. `pyreadstat` se llamó siempre con `metadataonly=True`. Latinobarómetro **2024 está RESERVADA (E.6)**: no se abrió el .zip ni el .dta 2024 de ninguna forma; solo se leyó el texto del cuestionario PDF 2024 (`data/raw/latinobarometro2024_cuestionario_esp.pdf`) para comparar el TEXTO de las preguntas, nunca cifras.

## 1. Payload y dimensiones

- Payload: `data/raw/LATINOBAROMETRO/2023/latinobarometro-2023-stata-v1-0.zip`
- Miembro usado: `Latinobarometro_2023_Esp_Stata_v1_0.dta` (también existe `..._Eng_Stata_v1_0.dta`, no usado; el zip también trae `Latinobarometro_2023_Esp.pdf` y `Latinobarometro_2023_Eng.pdf`, que resultaron ser el **cuestionario aplicado**, no una ficha técnica de muestreo separada).
- Dimensiones: **19,205 filas × 274 columnas**.
- Nota de codificación: las etiquetas del `.dta` vienen con mojibake (UTF-8 re-decodificado como Latin-1, p.ej. `PaÃ\xads`). Se corrigieron con `s.encode('latin1').decode('utf-8')` para este informe; cualquier lector debe aplicar el mismo fix.

## 2. País y diseño

- Variable de país: `idenpa` (IDENPA — País). Etiqueta de valor de **México: código `484`** (`"Mexico"`).
- Variable de región/circunscripción de México: `reg`, con 5 valores para México: `484905`..`484909` = "MX: Circunscripcion I".."V". También `ciudad` trae localidades específicas de México con prefijo `484...` agrupadas por macrorregión (Norte/Occidente/Centro/Sur), p.ej. `484309009 = MX: Centro/Distrito Federal/Iztapalapa`.
- Ponderador: `wt` (WT — Ponderación). Sin etiquetas de valor (variable continua), como se espera de un peso.
- **Estrato de diseño / UPM-PSU: NO EXISTEN.** Se buscó en las 274 variables con patrones `estrat|upm|psu|conglom|cluster|segmento` y el único hit fue `wt` (por "ponder"). No hay variable de estrato ni de conglomerado/UPM en el archivo.
- Ficha técnica del diseño para México: **no disponible en este payload.** Los dos PDF incluidos en el zip (`Latinobarometro_2023_Esp.pdf` / `_Eng.pdf`) son el cuestionario aplicado (6 páginas), no un documento metodológico; se buscaron los términos "muestra", "ficha", "diseño", "estrato", "UPM", "representa" en el texto extraído y no aparece información de diseño muestral por país.

## 3. Segmentación

| Variable | Etiqueta | Etiquetas de valor |
|---|---|---|
| `sexo` | Sexo entrevistado | 1=Hombre, 2=Mujer |
| `edad` | Edad | Variable continua (años); sin etiquetas de valor salvo códigos de sistema (-1 No sabe, -2 No contesta, -3 No aplicable, -4 No preguntada, -5 No sabe/No contesta) |
| `reedad` | EDAD RECODIFICADA | 1=16-25, 2=26-40, 3=41-60, 4=61 y más (+ códigos de sistema) |
| `tamciud` | Tamaño de hábitat | 1=Menos de 5.000 … 7=100.001 y más, 8=(Capital) |
| `reg` / `ciudad` | Región/Ciudad | ver §2 (para México: circunscripciones I-V y localidades) |
| `S11` | Nivel de estudios alcanzado - Entrevistado | 1=Sin estudios … 13=12 años, 14=Universitario incompleto, 15=Universitario completo, 16/17=Instituto superior técnico incompl./compl. |
| `REEEDUC_1` | Nivel de estudios (recodificado) | 1=Analfabeto, 2=Básica incompleta, 3=Básica completa, 4=Secundaria/media/técnica incompleta, 5=…completa, 6=Superior incompleta, 7=Superior completa |
| `S18_A` | Estado ocupacional | 1=Independiente/cuenta propia, 2=Asalariado emp. pública, 3=Asalariado emp. privada, 4=Temporalmente no trabaja, 5=Retirado/pensionado, 6=No trabaja/responsable del hogar, 7=Estudiante |
| `S19` | Tipo de trabajo | 1=Profesional, 2=Dueño de negocio, 3=Agricultor/Pescador, 4=Cuenta propia/ambulante, 5=Profesional, 6=Alto ejecutivo, 7=Ejecutivo mando medio, 8=Otro empleado |
| `S2` | Clase social subjetiva | 1=Alta, 2=Media Alta, 3=Media, 4=Media Baja, 5=Baja |
| `S24` | Apreciación NSE (por el encuestador) | 1=Muy bueno … 5=Muy malo |
| `S20_A`…`S20_K` | Bienes del hogar (vivienda propia, lavadora, celular, auto, agua caliente, alcantarillado, comida caliente diaria, agua potable, internet, calefacción/aire) | 1=Sí, 2=No (por ítem) |
| `S7` | Raza/Etnia | 1=Asiático, 2=Negro, 3=Indígena, 4=Mestizo, 5=Mulato, 6=Blanco, 7=Otra raza |

Todos con el mismo bloque de códigos de sistema (-1 a -5) para no sabe/no contesta/no aplicable/no preguntada.

## 4. Reactivos candidatos (confianza / capital social / participación / democracia)

Comparación de texto SOLO contra el cuestionario PDF 2024 (`latinobarometro2024_cuestionario_esp.pdf`), sin abrir la base 2024.

| Variable | Etiqueta | Etiquetas de valor completas | ¿Mismo texto en cuestionario 2024? |
|---|---|---|---|
| `P9STGBS` | Confianza Interpersonal | -5 No sabe/No contesta, -4 No preguntada, -3 No aplicable, -2 No contesta, -1 No sabe, 1=Se puede confiar en la mayoría de las personas, 2=Uno nunca es lo suficientemente cuidadoso en el trato con los demás | **IDÉNTICO** — mismo texto exacto, en 2024 aparece como `P10STGBS` (renumerado) |
| `P10STGBS` | Apoyo a la democracia | (mismos códigos de sistema) 1=La democracia es preferible…, 2=En algunas circunstancias un gobierno autoritario puede ser preferible…, 3=A la gente como uno nos da lo mismo | No verificado directamente (fuera del foco de confianza; no localizado con el mismo rótulo en 2024) — **CAMBIA/no localizado** |
| `P13STGBS_A` | Confianza en las Fuerzas Armadas | 1=Mucha, 2=Algo, 3=Poca, 4=Ninguna (+ sistema) | **CAMBIA** (texto de ítem igual "Las Fuerzas Armadas", pero renumerado a `P14STGBS.A` dentro de una batería ampliada de A-N, antes A-I) |
| `P13STGBS_B` | Confianza en la Policía | ídem | **CAMBIA** (renumerado a `P14STGBS.B`, mismo texto "La policía/Carabineros") |
| `P13ST_C` | Confianza en la Iglesia | ídem | **CAMBIA** (renumerado a `P14ST.C`, mismo texto "La Iglesia") |
| `P13ST_D` | Confianza en el Congreso | ídem | **CAMBIA** (renumerado a `P14ST.D`, texto ampliado a "Congreso/Parlamento") |
| `P13ST_E` | Confianza en el Gobierno | ídem | **CAMBIA** (renumerado a `P14ST.E`, mismo texto "Gobierno") |
| `P13ST_F` | Confianza en el Poder Judicial | ídem | **CAMBIA** (renumerado a `P14ST.F`, mismo texto) |
| `P13ST_G` | Confianza en los Partidos Políticos | ídem | **CAMBIA** (renumerado a `P14ST.G`, mismo texto) |
| `P13ST_H` | Confianza en la institución electoral del país | ídem | **CAMBIA** (renumerado a `P14ST.H`, texto "la institución Electoral del país") |
| `P13ST_I` | Confianza en el Presidente | ídem | **CAMBIA** (renumerado a `P14ST.I`, mismo texto "El presidente") — la batería 2024 agrega J=Radio, K=Televisión, L=Redes sociales, M=Diarios, N=Sindicatos (**AUSENTE** en 2023 como ítems de esta batería) |
| `S1` | Religión | 1=Católica, 2=Evangélica sin especificar, 3=Evangélica bautista, 4=Evangélica metodista, 5=Evangélica pentecostal, 6=Adventista, 7=Testigos de Jehová, 8=Mormón, 9=Judía, 10=Protestante, 11=Cultos afro/americanos/Umbanda, 12=Creyente sin Iglesia, 13=Agnóstico, 14=Ateo, 96=Otra, 97=Ninguna (+ sistema) | **IDÉNTICO** — "¿Cuál es su religión? (ANOTE LO QUE LE DIGAN)" |
| `S1A` | Práctica religiosa | 1=Muy practicante, 2=Practicante, 3=No muy practicante, 4=No practicante (+ sistema; 2024 agrega código 9=No aplicable/Sin religión, ausente como etiqueta explícita en 2023) | **IDÉNTICO** en texto de pregunta |
| `S2` | Clase social subjetiva | 1=Alta, 2=Media Alta, 3=Media, 4=Media Baja, 5=Baja (+ sistema) | **IDÉNTICO** — mismo texto "La gente algunas veces se describe a sí misma como perteneciendo a una clase social…" |
| `P18ST_A` | Acuerdo: "La democracia puede tener problemas pero es el mejor sistema de gobierno" | 1=Muy de acuerdo, 2=De acuerdo, 3=En desacuerdo, 4=Muy en desacuerdo (+ sistema) | **IDÉNTICO** (P18ST.A en ambos años) |
| `P18STM_B` | Acuerdo: "No me importaría que un gobierno no democrático llegara al poder si resuelve los problemas" | ídem escala | **IDÉNTICO** — mismo texto exacto, en 2024 es `P18ST.B` |
| `P18STM_C` | Acuerdo: "En caso de dificultades está bien que el presidente controle los medios de comunicación" | ídem escala | **CAMBIA** — en 2024 `P18ST.C` dice "Está bien que el Presidente pase por encima de las leyes, el parlamento y/o las instituciones con el objeto de resolver los problemas" (pregunta distinta, mismo lugar en la batería) |
| `P19N` | Sociedad que defiende nuestras costumbres vs. sociedad abierta a la diversidad | 1=Prefiero una sociedad que defienda nuestras costumbres, 2=Prefiero una sociedad abierta a la diversidad de todo tipo de costumbres (+ sistema) | **AUSENTE** — no se localizó este ítem (ni "costumbres" ni "diversidad de todo tipo de costumbres") en el cuestionario 2024 |
| `P20STM` | Apoyaría un gobierno militar si las cosas se ponen muy difíciles | 1=Apoyaría a un gobierno militar…, 2=En ninguna circunstancia apoyaría un gobierno militar (+ sistema) | **AUSENTE** — no se localizó ningún ítem con el texto "gobierno militar" como pregunta de apoyo en el cuestionario 2024 (solo aparece "Los militares" como opción de confianza institucional en otra pregunta) |
| `P21ST` | Sin partidos políticos no puede haber democracia | 1=Sin partidos políticos no puede haber democracia, 2=La democracia puede funcionar sin partidos (+ sistema) | **IDÉNTICO** — mismo texto exacto, renumerado a `P20ST` en 2024 |
| `P44ST_A` | Frecuencia con que habla de política con los amigos | 1=Muy frecuentemente, 2=Frecuentemente, 3=Casi nunca, 4=Nunca (+ sistema) | **AUSENTE** — no localizado en cuestionario 2024 |
| `P44ST_B` | Frecuencia en que trabaja por un tema que lo afecta a Ud. o su comunidad | ídem escala | **AUSENTE** |
| `P44ST_C` | Frecuencia con que trata de convencer políticamente | ídem escala | **AUSENTE** |
| `P44ST_D` | Frecuencia con que trabaja para un partido político o candidato | ídem escala | **AUSENTE** |
| `P45ST_A` | Acción política: Firmar una petición | 1=La ha realizado, 2=La podría realizar, 3=Nunca las haría (+ sistema) | **AUSENTE** — "petición" no aparece en cuestionario 2024 |
| `P45S_B` | Acción política: Asistir a manifestaciones autorizadas | ídem escala | **AUSENTE** — "manifestación" en 2024 solo aparece como opción de otra pregunta (P.ej. tipo de violencia), no como este ítem de acción política |
| `P45ST_C` | Acción política: Participar en protestas no autorizadas | ídem escala | **AUSENTE** — "protesta" no aparece con este formato en 2024 |
| `P45STN_D` | Acción política: Protestar en redes sociales | ídem escala | **AUSENTE** |

Notas sobre justicia por propia mano, tolerancia/discriminación explícita, y organizaciones/acción colectiva formal (asociativismo): no se identificaron variables 2023 dedicadas a "justicia por propia mano" ni a un índice de pertenencia a organizaciones/ayuda mutua en la lista de 274 columnas (más allá de S6 "Beneficiario de programa de ayuda del Estado", que es receptor, no donante/participante). No se tabularon por no existir en este payload.

## 5. Anomalías detectadas

- Mojibake sistemático en TODAS las etiquetas de variable y de valor (UTF-8 doble-decodificado). Afecta lectura directa con `pyreadstat`/`meta.column_names_to_labels`; requiere el fix `encode('latin1').decode('utf-8')`.
- El PDF incluido en el zip 2023 es el **cuestionario aplicado**, no una ficha técnica de muestreo; no hay documento de diseño muestral por país dentro de este payload.
- No existe variable de estrato ni de UPM/PSU: cualquier análisis de varianza por diseño complejo solo puede apoyarse en `wt` (ponderación), sin poder reconstruir el efecto de diseño real.
- La batería de confianza institucional (P13/P14) no es 1:1 entre años: 2023 tiene 9 ítems (A-I), 2024 tiene 14 (A-N), con 5 ítems nuevos (radio, TV, redes sociales, diarios, sindicatos) y renumeración de letra en dos casos (H pasa a "institución Electoral del país" en ambos, pero desplazamiento general porque P13 pasa a ser P14 en 2024).
- `S1A` (práctica religiosa) en 2023 no trae explícitamente el código 9="No aplicable (sin religión)" que sí aparece documentado en el cuestionario 2024; en el `.dta` 2023 solo se documentan los códigos de sistema genéricos -1 a -5, sin un código dedicado para "sin religión" en esta variable (la exclusión de quienes no tienen religión se maneja por diseño de salto de pregunta, no por código de valor visible en la etiqueta).
