# Estructura WVS Ola 7 México 2018 — confianza y capital social

Informe de ESTRUCTURA únicamente. No se leyó, imprimió ni calculó ningún valor de microdato (ni frecuencias, ni medias, ni `head()`, ni `value_counts`). Toda la información proviene de metadatos (`pyreadstat.read_dta(..., metadataonly=True)`: nombres de variable, etiquetas de variable, etiquetas de valor, número de filas/columnas) y de los PDF de documentación.

## 1. Payload

- Payload: `/home/pc0/mm-corpus/descargas_mx_espejo/F00013084-WVS_Wave_7_Mexico_Stata_v5.1.zip`
- sha256 verificado: `a676a7601e25cb15a670828d8bf2990d8a73958c7367118c3a5293c6ae84d9a4` (coincide con el prefijo `a676a760…` del encargo)
- Miembro del zip: `WVS_Wave_7_Mexico_Stata_v5.1.dta` (único archivo, 1,932,469 bytes)
- Dimensiones (de metadatos, `metadataonly=True`): **1,741 filas × 403 columnas**

## 2. DISEÑO

Variables de diseño encontradas en el .dta:

| Variable | Etiqueta Stata | Etiquetas de valor |
|---|---|---|
| `W_WEIGHT` | Weight | (continua, sin etiquetas de valor) |
| `S018` | Equilibration weight-1000 | (continua, sin etiquetas de valor) |
| `PWGHT` | Population size weight | (continua, sin etiquetas de valor) |
| `I_PSU` | Primary Sampling Unit ID | (identificador, sin etiquetas de valor) |
| `N_REGION_ISO` | Region ISO 3166-2 | 32 entidades federativas (códigos `484001`–`484032`, p.ej. `484001 = MX-CMX Ciudad de Mexico`) |
| `N_REGION_WVS` | Region country specific | 32 entidades, codificación específica del país (`484101`–`484132`) |
| `G_TOWNSIZE` | Settlement size_8 groups | 8 tramos, de "Under 2,000" a "500,000 and more" |
| `G_TOWNSIZE2` | Settlement size_5 groups | 5 tramos, de "Under 5,000" a "500000 and more" |
| `S_INTLANGUAGE` | Language in which interview was conducted | único valor observado en la etiqueta: `1270 = Spanish; Castilian` |

**No existe ninguna variable de estrato de diseño (`STRATUM`/similar) en el .dta.** Se buscó explícitamente con patrones `strat|psu|upm` sobre las 403 etiquetas de columna y solo aparece `I_PSU` (identificador de unidad primaria de muestreo, sin etiquetas de valor — es un ID, no una etiqueta de estrato). No hay variable de UPM/PSU con etiquetas adicionales, ni variable de estrato geográfico/socioeconómico explícita más allá de `N_REGION_ISO`/`N_REGION_WVS` (entidad) y `G_TOWNSIZE`/`G_TOWNSIZE2` (tamaño de localidad), que son las candidatas más próximas a un post-estrato.

Lo que dice el PDF de diseño muestral (`F00010701-WVS7_Sample_Design_Mexico_2018.pdf`, texto extraído con `pdftotext`):

> "The Mexico 2018 WVS was based on a national representative sample of 1,741 adults (18 years or older). It conducted with face-to-face interviews in households from January 18 to May 2, 2018 in 496 polling points in the 32 federal entities of Mexico."
>
> "A multi-stage probability sampling was employed using the National Elections Institute (INE) list of electoral sections updated for the 2018 presidential elections and stratified by urban-rural-mixed categories by INE. The sample design also took into account the population proportion of the 32 federal entities in the country."
>
> "A total of 496 electoral sections were selected from the list of 68,364... The corresponding address to each electoral section... was then used as a starting point for a systematic selection of blocks and households in each polling point. In each household a single respondent was selected. In each polling point the number of interviews conducted ranged from 2 to 6..."
>
> "The dataset included a weight variable based on population distributions by sex, age, and education."
>
> Nota de campo: tasa de rechazo 58%; margen de error estimado ±2.6% (95% de confianza); 209 entrevistadores/supervisores bajo dirección de Alejandro Moreno (Moreno & Sotnikova Social Research and Consulting S.C.), con apoyo de El Financiero-Marketing.

Es decir: el diseño **es** multietápico (secciones electorales → manzanas → hogares → un respondiente), estratificado urbano-rural-mixto por el INE a nivel de sección electoral, con ponderación final por sexo/edad/educación (`W_WEIGHT`, con variantes `S018` de equilibración y `PWGHT` poblacional) — pero **el .dta liberado NO trae la variable de estrato ni el identificador de sección electoral/punto de levantamiento**; solo trae `I_PSU` (un ID sin decodificar) y las variables de entidad/tamaño de localidad como aproximación geográfica.

## 3. SEGMENTACIÓN

| Variable | Etiqueta Stata | Esquema / etiquetas de valor |
|---|---|---|
| `Q260` | Sex | `1=Male, 2=Female` |
| `Q262` | Age | continua (años); solo etiqueta de código faltante `b='No answer'` |
| `X003R` | Age recoded (6 intervals) | `1=16-24, 2=25-34, 3=35-44, 4=45-54, 5=55-64, 6=65 and more years` |
| `X003R2` | Age recoded (3 intervals) | (no inspeccionada en detalle; recodificación de `X003R`) |
| `Q275` | Highest educational level: Respondent [ISCED 2011] | esquema **ISCED 2011**, códigos `0`–`8`: Early childhood/no education … Doctoral or equivalent |
| `Q275R` | Highest educational level: Respondent (recoded into 3 groups) | `1=Lower, 2=Middle, 3=Higher` |
| `Q279` | Employment status | `1=Full time, 2=Part time, 3=Self employed, 4=Retired/pensioned, 5=Homemaker, 6=Student, 7=Unemployed` |
| `Q284` | Sector of employment | `1=Government/public, 2=Private business, 3=Private non-profit` |
| `Q285` | Are you the chief wage earner in your house | `1=Yes, 2=No` |
| `Q287` | Social class (subjective) | `1=Upper class ... 5=Lower class` (5 niveles) |
| `Q288` | Scale of incomes | escala de 10 pasos ("Lower step" … "Tenth step") |
| `Q288R` | Income level (Recoded) | `1=Low, 2=Medium, 3=High` |
| `G_TOWNSIZE` / `G_TOWNSIZE2` | tamaño de localidad | ver sección 2 (8 y 5 tramos respectivamente) |
| `N_REGION_ISO` / `N_REGION_WVS` | región/entidad | ver sección 2 |

La edad es **continua** (`Q262`, en años) con recodificaciones en tramos (`X003R` de 6 intervalos, `X003R2` de 3). No hay variable de "urbano-rural" binaria explícita; la proxy es `G_TOWNSIZE`/`G_TOWNSIZE2` (tamaño de asentamiento). La escolaridad usa el esquema internacional **ISCED 2011** (no un esquema nacional SEP), con recodificación a 3 grupos. No hay variable de ingreso monetario directa: `Q288` es una escala subjetiva de 10 peldaños de ingreso del hogar, con recodificación a 3 niveles (`Q288R`); `Q287` es clase subjetiva (5 niveles).

## 4. Reactivos candidatos

Fuente del texto de pregunta: `F00006635-WVS7_Questionnaire_Mexico_2018_Spanish.pdf` (extraído con `pdftotext -layout`), verbatim salvo saltos de línea del PDF. Todos los ítems de escala Likert/confianza comparten además los códigos negativos estándar del cuestionario: `-1=No sabe; -2=No contestó; -3=No aplica (filtro); -5=Valor perdido, no aplica, otras razones` (impresos una sola vez al inicio del cuestionario, "CÓDIGOS PARA TODO EL CUESTIONARIO").

### Confianza interpersonal

| Variable | Etiqueta Stata | Pregunta (verbatim, cuestionario ES) | Etiquetas de valor |
|---|---|---|---|
| Q57 | Most people can be trusted | Q57. "En términos generales, ¿diría usted que se puede confiar en la mayoría de las personas o que se tiene que ser muy cuidadoso al tratar con la gente?" | `1=Se puede confiar en la mayoría de la gente (Stata: Most people can be trusted), 2=Se tiene que ser muy cuidadoso (Need to be very careful), a=Don't know` |
| Q58 | Trust: Your family | Q58 (lista bajo "¿Podría decirme, para cada uno, si usted confía completamente..."). "Su familia" | `1=Trust completely, 2=Trust somewhat, 3=Do not trust very much, 4=Do not trust at all` |
| Q59 | Trust: Your neighborhood | Q59 "Sus vecinos" | `1..4` igual esquema, más `a=Don't know` |
| Q60 | Trust: People you know personally | Q60 "Sus conocidos" | `1..4`, `a=Don't know` |
| Q61 | Trust: People you meet for the first time | Q61 "Gente a la que conoce por primera vez" | `1..4`, `a=Don't know` |
| Q62 | Trust: People of another religion | Q62 "Gente de otra religión" | `1..4`, `a=Don't know`, `b=No answer` |
| Q63 | Trust: People of another nationality | Q63 "Gente de otra nacionalidad" | `1..4`, `a=Don't know`, `b=No answer` |

### Confianza en instituciones (muestra representativa; el bloque completo Q64–Q89 sigue el mismo esquema de valores)

| Variable | Etiqueta Stata | Pregunta (verbatim) | Etiquetas de valor |
|---|---|---|---|
| Q64 | Confidence: Churches | Q64 "Las iglesias" (dentro de "¿Podría decirme cuánta confianza tiene usted en cada una de ellas: mucha, algo, poca o nada de confianza?") | `1=A great deal (Mucha), 2=Quite a lot (Algo), 3=Not very much (Poca), 4=None at all (Nada), a=Don't know, b=No answer` |
| Q65 | Confidence: Armed Forces | Q65 "El ejército" | mismo esquema |
| Q66 | Confidence: The Press | Q66 "La prensa" | mismo esquema |
| Q67 | Confidence: Television | Q67 "La televisión" | mismo esquema |
| Q68 | Confidence: Labor Unions | Q68 "Los sindicatos" | mismo esquema |
| Q69 | Confidence: The Police | Q69 "La policía" | `1..4`, `a=Don't know` (sin `b`) |
| Q70 | Confidence: Justice System/Courts | Q70 "Los tribunales y juzgados" | mismo esquema, con `b` |
| Q71 | Confidence: The Government | Q71 "El gobierno" | `1..4`, `a=Don't know` |
| Q72 | Confidence: The Political Parties | Q72 "Los partidos políticos" | `1..4`, `a=Don't know` |
| Q73 | Confidence: Parliament | Q73 "El Congreso" | `1..4`, `a=Don't know` |
| Q74 | Confidence: The Civil Services | Q74 "La burocracia pública" | mismo esquema |
| Q75 | Confidence: Universities | Q75 "Las universidades" | mismo esquema |
| Q76 | Confidence: Elections | Q76 "Las elecciones" | mismo esquema |
| Q77 | Confidence: Major Companies | Q77 "Las grandes empresas" | mismo esquema |
| Q78 | Confidence: Banks | Q78 "Los bancos" | mismo esquema |
| Q79 | Confidence: The Environmental Protection Movement | Q79 "Las organizaciones ambientalistas" | mismo esquema |
| Q80 | Confidence: The Women's Movement | Q80 "Las organizaciones de mujeres" | mismo esquema |
| Q81 | Confidence: Charitable or humanitarian organizations | Q81 "Las organizaciones de caridad o humanitarias" | mismo esquema |
| Q82 | Confidence: Major regional organization (combined) | Q82 "El Tratado de Libre Comercio de América del Norte, TLCAN" (variable específica de país, combinada en el archivo armonizado) | mismo esquema |
| Q83–Q89 | Confidence: UN, IMF, ICC, NATO, WB, WHO, WTO | Q83 "La ONU" … Q89 "La Organización Mundial del Comercio" | mismo esquema (`1..4`, `a`, `b`) |

Nota: el cuestionario mexicano además incluye el ítem de país «El Instituto Nacional Electoral, INE» (numeración del cuestionario con prefijo M) como ítem específico de país (no aparece como `Q` en la lista de columnas objetivo revisada; no se confirmó su nombre exacto de variable en el .dta, se reporta como hallazgo del cuestionario).

### Membresía en organizaciones (Q94–Q105)

| Variable | Etiqueta Stata | Pregunta (verbatim) | Etiquetas de valor |
|---|---|---|---|
| Q94 | Active/Inactive membership: Church or religious organization | Q94 "Iglesia u organización religiosa" (dentro de "¿podría decirme si usted es miembro activo, un miembro pero no activo, o no pertenece a este tipo de organización?") | `0=Don't belong, 1=Inactive member, 2=Active member, b=No answer` |
| Q95 | ...Sport or recreational organization | Q95 "Organización deportiva o de recreación" | mismo esquema |
| Q96 | ...Art, music or educational organization | Q96 "Organización artística, musical o educativa" | mismo esquema |
| Q97 | ...labor union | Q97 "Sindicato" | `0=Not a member, 1=Inactive member, 2=Active member, b=No answer` |
| Q98 | ...political party | Q98 "Partido político" | mismo esquema |
| Q99 | ...Environmental organization | Q99 "Organización ambientalista o ecológica" | mismo esquema |
| Q100 | ...Professional association | Q100 "Asociación profesional" | mismo esquema |
| Q101 | ...charitable/humanitarian organization | Q101 "Organización humanitaria o de caridad" | mismo esquema |
| Q102 | ...consumer organization | Q102 "Organización de consumidores" | mismo esquema |
| Q103 | ...self-help group | Q103 "Grupo de auto-ayuda o de ayuda mutua" | mismo esquema |
| Q104 | ...womens group | Q104 "Grupo de mujeres" | mismo esquema |
| Q105 | ...other organization | Q105 "Otra organización" | mismo esquema |

### Religiosidad

| Variable | Etiqueta Stata | Pregunta (verbatim) | Etiquetas de valor |
|---|---|---|---|
| Q6 | Important in life: Religion | Q6, dentro de la tarjeta 1: "Para cada uno de los siguientes aspectos, dígame qué tan importante es en su vida" → ítem 6 "La religión" | `1=Very important (Muy importante), 2=Rather important (Algo importante), 3=Not very important (Poco importante), 4=Not at all important (Nada importante), a=Don't know, b=No answer` |
| Q164 | Importance of God | Q164 (TARJETA 17). "¿Qué tan importante es Dios en su vida? Indique en esta tarjeta: el 10 significa muy importante y el 1 nada importante." | escala 1–10, `1=Not at all important...10=Very important`, `a=Don't know` |
| Q171 | How often do you attend religious services | Q171 (TARJETA 18). "Dejando aparte bodas, funerales, bautismos, etc. ¿Con qué frecuencia asiste usted a servicios religiosos?" | `1=More than once a week ... 7=Never, practically never`, `a`, `b` |
| Q172 | How often do you pray | Q172 (TARJETA 19). "Sin considerar bodas o funerales, ¿con qué frecuencia reza usted a Dios?" | `1=Several times a day ... 8=Never, practically never`, `a`, `b` |
| Q173 | Religious person | Q173. "Independientemente de si va o no a la iglesia, ¿diría que usted es...?" | `1=A religious person (Una persona religiosa), 2=Not a religious person, 3=An atheist (Es ateo), a, b` |
| Q289 | Religious denominations - major groups | Q289. "¿Pertenece usted a alguna religión o denominación religiosa? (SÍ) ¿A cuál?" | `0=Do not belong to a denomination, 1=Catholic, 2=Protestant, 3=Orthodox, 4=Jew, 5=Muslim, 6=Hindu, 7=Buddhist, a=Don't know, b=No answer/refused` (cuestionario ES añade opción `8) Otros (anotar)`, no visible en la etiqueta de valor de Stata revisada — ver sección 5) |

### Autoridad

| Variable | Etiqueta Stata | Pregunta (verbatim) | Etiquetas de valor |
|---|---|---|---|
| Q7 | Important child qualities: good manners | Q7 (TARJETA 2). "Aquí hay una lista de cualidades que pueden fomentarse en el hogar... ¿Cuál considera usted que es especialmente importante para enseñar a los niños?" → ítem 7 "Buenos modales" | `1=Important (Sí mencionó), 2=Not mentioned (No mencionó)` |
| Q17 | Important child qualities: obedience | Q17, mismo bloque. Ítem 17 "Obediencia" | `1=Important, 2=Not mentioned, b=No answer` |
| (Q8–Q16 mismo bloque: independencia, trabajar duro, responsabilidad, imaginación, tolerancia y respeto, ahorro, determinación, fe religiosa, altruismo — mismo esquema binario) | | | |
| Q45 | Future changes: Greater respect for authority | Q45. "Le voy a leer una lista de cambios a nuestro estilo de vida que podrían darse en un futuro próximo. Dígame... si sucediera, usted cree que sería bueno, sería malo, o le da igual" → ítem 45 "Mayor respeto por la autoridad" | `1=Good thing (Bueno), 2=Don't mind (Le da igual), 3=Bad thing (Malo), a=Don't know` |
| Q235 | Political system: strong leader | Q235. "Voy a describir varios tipos de sistemas políticos... ¿Dígame si es muy buena, algo buena, algo mala o muy mala forma de gobierno para México?" → ítem 235 "Tener un líder fuerte que no se moleste por el congreso y las elecciones" | `1=Very good, 2=Fairly good, 3=Fairly Bad, 4=Very bad, a=Don't know, b=No answer` |
| Q236 | Political system: experts decide | Q236 "Tener expertos, no un gobierno, que tomen decisiones de acuerdo con lo que consideren que es mejor para el país" | mismo esquema |
| Q237 | Political system: army rule | Q237 "Tener un gobierno militar" | mismo esquema |
| Q238 | Political system: democratic | Q238 "Tener un sistema político democrático" | mismo esquema |

### Tolerancia

| Variable | Etiqueta Stata | Pregunta (verbatim) | Etiquetas de valor |
|---|---|---|---|
| Q18–Q26 | Neighbors: [grupo] | Q18 (TARJETA 3). "En esta lista hay varios grupos de gente. ¿Podría indicar aquellos que usted preferiría NO tener como vecinos?" — ítems: 18 Drogadictos, 19 Personas de raza/etnia distinta, 20 Personas con SIDA, 21 Inmigrantes/trabajadores extranjeros, 22 Homosexuales, 23 Gente de religión distinta, 24 Bebedores empedernidos, 25 Parejas no casadas conviviendo, 26 Gente que habla idioma distinto | `1=Sí mencionó (Stata: no confirmado etiqueta exacta, ver Q19/Q26 que sí se listaron con label "Neighbors:..."), 2=No mencionó` — esquema binario mención/no mención |
| Q182 | Justifiable: Homosexuality | Q182 (TARJETA 20). "Por favor dígame para cada una de las siguientes acciones si cree usted que siempre puede justificarse, que nunca puede justificarse, o si su opinión está en algún punto intermedio" → ítem 182 "La homosexualidad" | escala 1–10: `1=Never justifiable ... 10=Always justifiable`, `a=Don't know`, `b=No answer` |

### Acción colectiva

| Variable | Etiqueta Stata | Pregunta (verbatim) | Etiquetas de valor |
|---|---|---|---|
| Q209 | Political action: Signing a petition | Q209 (TARJETA 21). "Le voy a leer algunas formas de acción política que lleva a cabo la gente, dígame para cada si la ha hecho, la podría hacer, o nunca la haría bajo ninguna circunstancia" → ítem 209 "Firmar una petición o iniciativa" | `1=Have done (La ha hecho), 2=Might do (La podría hacer), 3=Would never do (Nunca lo haría), a=Don't know, b=No answer` |
| Q210 | Political action: Joining in boycotts | Q210 "Unirse a boicots" | mismo esquema |
| Q211 | Political action: Attending lawful/peaceful demonstrations | Q211 "Asistir a manifestaciones pacíficas" | mismo esquema |
| Q212 | Political action: Joining unofficial strikes | Q212 "Unirse a huelgas" | mismo esquema |

## 5. Diferencias texto cuestionario MX (español) vs. etiqueta Stata (inglés)

- Q57: la etiqueta Stata es genérica ("Most people can be trusted") y colapsa a un rótulo binario; el texto ES es más extenso ("¿diría usted que se puede confiar en la mayoría de las personas o que se tiene que ser muy cuidadoso al tratar con la gente?"). Sin discrepancia de sentido.
- Q82: la etiqueta Stata dice "Confidence: Major regional organization (combined from country-specific)" — es una variable armonizada entre países; el ítem específico de México detrás de esa etiqueta es el TLCAN ("El Tratado de Libre Comercio de América del Norte, TLCAN"), que no es obvio desde el rótulo inglés genérico. Riesgo de lectura errónea si no se coteja con el cuestionario nacional.
- Q289: el cuestionario ES incluye una octava opción "8) Otros (anotar)" que no aparece en las etiquetas de valor Stata revisadas (`0`–`7`, `a`, `b`); no se pudo confirmar si existe un código `8` en la variable sin leer valores — se reporta como discrepancia potencial a verificar en fase de codificación, no en esta fase de estructura.
- Q18–Q26 (vecinos no deseados): no se extrajeron las etiquetas de valor Stata exactas para cada ítem individual (solo se confirmó el esquema general "Sí mencionó/No mencionó" desde el texto del cuestionario y por analogía con Q7/Q17 que comparten el mismo bloque de tarjeta). Se recomienda verificación puntual antes de operacionalizar.
- Los ítems de país del INE y de protesta ("Asistir a una protesta o evento político convocado por...") son ítems específicos de México visibles en el cuestionario que no se buscaron por nombre de variable exacto en el .dta (prefijo `M` en vez de `Q`); quedan fuera de la tabla de reactivos por no confirmarse su nombre de columna.

## Nota metodológica

No se leyó, contó ni imprimió ningún valor de microdato del .dta en ningún momento de este ejercicio. Todas las llamadas a `pyreadstat.read_dta` se hicieron con `metadataonly=True`. El único cómputo realizado sobre datos fue el número de filas y columnas reportado por los metadatos del archivo (1,741 × 403), no derivado de leer contenido.
