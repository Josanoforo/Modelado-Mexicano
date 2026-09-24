# Estructura ENBIARE 2021 — investigación de metadatos

Fuentes abiertas (solo metadatos/documentación; de la base solo se leyó la primera línea/encabezado):

| archivo | sha256 (manifiesto) | verificación |
|---|---|---|
| `enbiare2021/enbiare_2021_base_de_datos_csv.zip` | `afe9013a4cc26538dfe81da686f0d09e756a7d0e2fc407cd22f596fd53c0f354` | COINCIDE (recalculado con `sha256sum` sobre `/home/pc0/mm-corpus/raw/enbiare2021/enbiare_2021_base_de_datos_csv.zip`) |
| `enbiare2021/enbiare_2021_fd.pdf` | `8a79265d8c1f761d9f3043c2d4837a9366679314b97aaebd8d189c6bcbc716a9` | COINCIDE (recalculado con `sha256sum` sobre `/home/pc0/mm-corpus/raw/enbiare2021/enbiare_2021_fd.pdf`) |

Miembros del ZIP (solo listados con `zipfile.namelist()` y `getinfo().file_size`; NO hay `diccionario_de_datos` ni `catalogos` adjuntos, solo 4 CSV de base):
- `THOGAR.csv` (2,671,035 bytes)
- `TSDEM.csv` (11,473,757 bytes)
- `TVIVIENDA.csv` (3,450,823 bytes)
- `TENBIARE.csv` (37,222,592 bytes)

De cada uno se leyó únicamente la primera línea (encabezado de columnas), nunca datos. El FD (`enbiare_2021_fd.pdf`) se extrajo íntegro a texto con `pdftotext -layout` (2,326 líneas) y se leyó completo.

Inventario ya extraído `data/inventario-reactivos-v1_2.tsv` (178,246 filas totales; cabecera real en la línea 10 del archivo, tras 9 líneas de comentario `#`). Filtrando `instrumento` que contiene "enbiare" (case-insensitive) se obtienen **349 filas**, todas con `payload_id = enbiare2021/enbiare_2021_base_de_datos_csv.zip`, repartidas: TENBIARE.csv=284, TVIVIENDA.csv=24, TSDEM.csv=22, THOGAR.csv=19. Esto corrobora el número esperado (349) declarado en el encargo. No se corroboró columna por columna contra el diccionario porque el ZIP no trae diccionario_de_datos/catalogos separados — solo el FD PDF, que sí se usó como fuente de verdad de textos/códigos.

---

## A) Diseño muestral

Unidad de la encuesta: persona seleccionada de 18 años y más dentro del hogar (`N_REN` identifica el renglón de la persona seleccionada; TENBIARE es la tabla de persona).

Variables de diseño, **públicas en la base** (aparecen en el encabezado real del CSV y en el FD, apartado "VARIABLES DE DISEÑO" de cada una de las 4 tablas):

| variable | tabla(s) | tipo/tamaño | concepto (FD) |
|---|---|---|---|
| `FAC_VIV` | TVIVIENDA | Numérico, 4 | Factor de expansión de vivienda |
| `FAC_HOG` | THOGAR, TSDEM | Numérico, 4 | Factor de expansión de hogar |
| `FAC_ELE` | TENBIARE | Numérico, 5 | Factor de expansión del elegido (persona seleccionada) |
| `EST_DIS` | las 4 tablas | Alfanumérico, 3 (001…472) | Estrato de diseño muestral |
| `UPM_DIS` | las 4 tablas | Alfanumérico, 7 (0000001…0004716) | UPM de diseño muestral |

`EST_DIS`/`UPM_DIS` son llaves opacas (no traen nombre de estrato/UPM legible, solo código numérico), consistente con la memoria de proyecto sobre este patrón en otras encuestas INEGI.

## B) Segmentadores

| variable | tabla | concepto (FD) | códigos |
|---|---|---|---|
| `SEXO` | TSDEM | 4.3 sexo | 1 Hombre, 2 Mujer |
| `EDAD` | TSDEM | 4.4 años cumplidos | 00 <1 año, 01-95 años, 96 96+, 97/98/99 no especificado |
| `NIVEL` | TSDEM | 4.7 nivel/grado escolar aprobado | 00 Ninguno … 10 Maestría o doctorado, 99 No sabe, b Blanco |
| `GRADO` | TSDEM | 4.7 grado dentro del nivel | 0 Ninguno, 1-9 Año, b Blanco |
| `ENT` | las 4 tablas (variable derivada) | Entidad federativa | 01-32 |
| `TLOC` | las 4 tablas (variable derivada) | Tamaño de localidad | 1 100,000+ hab.; 2 15,000-99,999; 3 2,500-14,999; 4 <2,500 |
| `PAREN` | TSDEM | 4.2 parentesco con jefe(a) de hogar | 1 Jefe(a) … 8 Sin parentesco |

No se buscó/encontró un campo explícito "urbano/rural" binario distinto de `TLOC` (4 categorías).

## C) Conductas/estados

### C1. Satisfacción con la vida y satisfacción por dominio
Apartado A "BIENESTAR SUBJETIVO" del FD (líneas ~419-625), tabla TENBIARE.

| variable | texto literal | escala/códigos | universo/filtro |
|---|---|---|---|
| `PA1` | "¿Podría decirme, en esa escala de 0 a 10, qué tan satisfecho(a) se encuentra actualmente con su vida?" | 00-10 (0="totalmente insatisfecha(o)", 10="totalmente satisfecha(o)") | población 18+ seleccionada |
| `PA2` | "Y hace un año, ¿qué tan satisfecho se encontraba con su vida?" | 00-10, misma escala | ídem |
| `PA3_01`…`PA3_17` | satisfacción por dominio: nivel de vida, salud, logros en la vida, relaciones personales, vida social, vida familiar, vida afectiva/pareja, perspectivas a futuro, tiempo libre, libertad para tomar decisiones, seguridad, actividad principal (trabajo/hogar/estudio), vivienda, vecindario, ciudad, servicios públicos, país | 00-10, misma escala 0/10 | ídem |
| `PA5` | "¿En qué escalón siente que su vida se ubica actualmente?" (escalera de Cantril, 0="la peor vida posible", 10="la mejor vida posible") | 00-10 | ídem — candidata a C6 (eudemonía/evaluación global) |
| `PA6` | "Según su percepción, ¿en qué escalón diría usted que va a estar dentro de cinco años?" (misma escalera) | 00-10 | ídem |

No hay puntaje/índice construido en el archivo (solo ítems crudos; ni FD ni encabezados de CSV traen variable tipo "índice de satisfacción").

### C2. Facilidad/dificultad para cubrir gastos del hogar
**No se encontró** en ENBIARE 2021 un ítem que pregunte directamente "facilidad/dificultad para cubrir gastos del hogar" tipo el usado en otros reportes de bienestar.

Búsqueda realizada (grep case-insensitive sobre el texto completo del FD, 2326 líneas): `gasto`, `ingreso`, `alcanza`, `dificultad`, `facilidad`, `económic`, `cubrir`. Se revisaron manualmente todas las secciones: SECCIÓN I (vivienda), SECCIÓN II (identificación de hogares), SECCIÓN III (servicio doméstico), Apartados A-J de TENBIARE completos (~1900 líneas del FD), y las VARIABLES DERIVADAS/DE DISEÑO de las 4 tablas.

Hallazgos relacionados pero que NO son el ítem buscado:
- `P2_2`/`P2_3` (TVIVIENDA): "¿Todas las personas... comparten un mismo gasto para comer?" / "¿cuántos hogares... tienen gasto separado para comer?" — es sobre definición de hogar, no sobre suficiencia de ingreso.
- `PF2` (TENBIARE, Apartado F): "En su opinión, ¿de cuánto sería un ingreso suficiente para alcanzar a pagar todas las necesidades...?" (monto en pesos, 0000400-9999998) — es una pregunta de monto de ingreso mínimo suficiente, no una escala de facilidad/dificultad percibida para cubrir gastos actuales.
- `PD1_1`…`PD1_6` (Apartado D): son dificultades funcionales/discapacidad (ver, oír, caminar, etc.), no económicas.

Total de variables examinadas en el FD: las ~280 preguntas de TENBIARE más las de THOGAR/TSDEM/TVIVIENDA (349 filas del inventario). Ninguna corresponde a "facilidad percibida para cubrir gastos del hogar" tal como está formulado en otras encuestas (p. ej. ENIGH/BIARE módulo hogar).

### C3. Síntomas depresivos y ansiedad
Apartado D "SALUD" del FD (líneas ~872-990), tabla TENBIARE. Corresponde a una forma corta tipo CES-D (D2, 7 ítems) y tipo GAD-2 (D3, 2 ítems del GAD-7).

**D2 — síntomas depresivos (CES-D corta, 7 ítems), última semana, escala 0-3 (0="Rara vez o nunca <1 día", 1="Pocas o algunas veces 1-2 días", 2="Un número de veces considerable 3-4 días", 3="Todo el tiempo o la mayoría del tiempo 5-7 días"):**

| variable | texto literal |
|---|---|
| `PD2_1` | "¿usted sentía como si no pudiera quitarse la tristeza de encima?" |
| `PD2_2` | "¿le costaba concentrarse en lo que estaba haciendo?" |
| `PD2_3` | "¿usted se sintió deprimido(a)?" |
| `PD2_4` | "¿le parecía que todo lo que hacía era un esfuerzo?" |
| `PD2_5` | "¿usted no durmió bien?" |
| `PD2_6` | "¿usted disfrutó de la vida?" (ítem invertido) |
| `PD2_7` | "¿usted se sintió triste?" |

**D3 — ansiedad (2 ítems, tipo GAD-2/subconjunto de GAD-7), últimas dos semanas, escala 0-3 (0="Nunca <1 día", 1="Varios días", 2="Más de la mitad de los días", 3="Casi todos los días"):**

| variable | texto literal |
|---|---|
| `PD3_1` | "¿con qué frecuencia ha sentido molestias por Sentirse nervioso(a), intranquilo(a), con los nervios de punta...?" |
| `PD3_2` | "¿con qué frecuencia ha sentido molestias por No poder dejar de preocuparse o no poder controlar su preocupación...?" |

Universo/filtro: no se documenta filtro distinto al universo general (persona seleccionada 18+); no aparecen códigos "blanco por secuencia" en estos ítems del FD, sugiriendo que se preguntan a todos los seleccionados. No hay puntaje/índice construido (ni score CES-D ni GAD) en los encabezados del CSV ni en el FD — solo los ítems crudos.

### C4. Confianza interpersonal/institucional y capital social
Apartado B "CONFIANZA Y REDES DE APOYO" (líneas ~625-708) y Apartado C "USO DEL TIEMPO EN ACTIVIDADES Y REDES" (líneas ~708-872), tabla TENBIARE.

**B1 — confianza (12 ítems), escala 00-10 (0="nada en absoluto"…10 confianza máxima):**

| variable | texto literal |
|---|---|
| `PB1_01` | "¿cuánto confía en la mayoría de la [gente]...?" |
| `PB1_02` | "¿cuánto confía en la gente que usted [conoce]...?" |
| `PB1_03` | "¿cuánto confía en los medios de [comunicación]...?" |
| `PB1_04` | "¿cuánto confía en la policía municipal?" |
| `PB1_05` | "¿cuánto confía en la policía estatal?" |
| `PB1_06` | "¿cuánto confía en la Guardia Nacional?" |
| `PB1_07` | "¿cuánto confía en el Ejército y la [Marina]...?" |
| `PB1_08` | "¿cuánto confía en el ministerio público...?" |
| `PB1_09` | "¿cuánto confía en los juzgados y [tribunales]...?" |
| `PB1_10` | "¿cuánto confía en las cámaras de [diputados/senadores]...?" |
| `PB1_11` | "¿cuánto confía en los partidos [políticos]...?" |
| `PB1_12` | "¿cuánto confía en los funcionarios [públicos]...?" |

**B2 — apoyo/redes en urgencia:**

| variable | texto literal | códigos |
|---|---|---|
| `PB2_1` | "En caso de que se le presente una urgencia o necesidad, ¿considera usted que siempre contará con [apoyo]...?" (familia, según nota manifiesto) | 1 Sí, 2 No |
| `PB2_2` | continuación de B2 (otro tipo de apoyo/red) | 1 Sí, 2 No |

**C — cuidado, participación social y reuniones (capital social):**

| variable | texto literal (resumen) |
|---|---|
| `PC1_1`…`PC1_7` | "La semana pasada, ¿dedicó tiempo a cuidar o [ayudar]...?" (cuidado de personas, apoyo en tareas escolares, etc. de integrantes del hogar) |
| `PC2_1`…`PC2_5` | frecuencia de conductas de ayuda/apoyo en la semana pasada (escala Siempre/Algunas veces/Rara vez/Nunca aprox.) |
| `PC3_1`…`PC3_8` | "¿Con qué frecuencia acostumbra tener reuniones sociales con...?" — incluye personas de su iglesia o congregación religiosa (`PC3_2`), compañeros de escuela, personas con quien practica deporte, etc. |
| `PC4_1`, `PC4_2` | ítems finales de la sección C (no se leyó el texto completo, ver nota) |

Además, Apartado G "PARTICIPACIÓN SOCIAL Y COMUNITARIO" (THOGAR: `PG5_1_2/PG5_2_2/PG5_3_2` son mascotas, no capital social) y en TENBIARE `PG1`…`PG8` cubren participación cívica/asociativa (ver C5 para `PG6-PG8` religión).

Universo/filtro: no se observaron marcas de "Blanco por secuencia" en B1/B2; en PC1-PC4 sí puede haber filtros de secuencia (no se transcribieron todos los códigos "b" ítem por ítem).

### C5. Religiosidad
Apartado G del FD (TENBIARE, líneas ~1946-1958).

| variable | texto literal | códigos | notas |
|---|---|---|---|
| `PG6` | "¿Usted tiene una religión?" | (Sí/No, texto exacto de código truncado en extracción, revisar PDF pág. correspondiente si se requiere el detalle fino) | afiliación religiosa |
| `PG7` | "¿Acostumbra asistir a su iglesia, templo o servicio religioso?" | 1 Sí / 2 No (frecuencia no vista en el fragmento extraído — solo dicotómico en la vista obtenida) | asistencia |
| `PG8` | "...iglesia, en el que promueva activamente su fe o valores religiosos?" (participación activa/liderazgo religioso) | 1 Sí / 2 No | participación religiosa activa |

Además `PC3_2` (reuniones sociales con personas de su iglesia o congregación religiosa) es un ítem de capital social con anclaje religioso, ya listado en C4.

No se encontró un ítem de "importancia de la religión en su vida" (escala de importancia); solo afiliación/asistencia/participación.

### C6. Balance afectivo / eudemonía (propósito de vida)
**Balance afectivo — Apartado A, `PA4` (10 ítems), "día de ayer", escala 00-10 ("ningún momento del día" a "todo el día"):**

| variable | texto literal (resumen) |
|---|---|
| `PA4_01` | "¿Cuánta parte del día de ayer se sintió de buen [humor/ánimo]...?" |
| `PA4_02` | "...se sintió tranquilo(a)...?" |
| `PA4_03` | "...se sintió con energía...?" |
| `PA4_04`…`PA4_10` | continúan afectos positivos/negativos del día anterior (textos completos truncados en la extracción por columnas superpuestas del PDF; los nemónicos y escala 00-10 sí están confirmados) |

Esto es un balance afectivo tipo Day Reconstruction/PANAS abreviado (10 ítems de afecto del día anterior).

**Eudemonía/evaluación global — `PA5`/`PA6`** (escalera de Cantril, ya descritos en C1): evaluación de vida actual y proyección a 5 años. Son el candidato más cercano a "eudemonía" en el instrumento; no hay un ítem explícito de "propósito de vida" o "sentido de vida" tipo Ryff/PIL.

Búsqueda de "propósito"/"sentido de vida"/"vale la pena": sin resultados en el FD completo (grep sobre 2326 líneas).

---

## Resumen de cobertura de búsqueda
- Archivos abiertos íntegros: FD PDF (2326 líneas de texto vía `pdftotext -layout`) y encabezados de las 4 tablas del ZIP (solo primera línea de cada CSV, vía `zipfile`).
- El ZIP NO trae `diccionario_de_datos` ni `catalogos` separados (solo 4 CSV de base) — por tanto la corroboración de la etiqueta v1_2 del inventario se hizo contra el FD, no contra un diccionario adicional.
- Secciones del FD recorridas íntegramente: LLAVE + Sección I (vivienda), Sección II (hogares), Sección III (servicio doméstico), Apartados A-J de TENBIARE, más VARIABLES DERIVADAS y VARIABLES DE DISEÑO de las 4 tablas.
- 349 filas del inventario correspondientes a ENBIARE, correlacionadas contra las variables anteriores.
</content>
