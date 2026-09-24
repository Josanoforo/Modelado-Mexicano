# ENSANUT — estructura de variables por ola (metadatos únicamente)

Metodología: se leyó SOLO metadata (`pyreadstat.read_dta(..., metadataonly=True)`): nombres de variable, etiquetas de variable, etiquetas de valor y `number_rows`. No se leyó ningún valor de microdato. Los `.dta` se extrajeron de sus `.zip` a `$TMPDIR` con `zipfile` de Python. RESERVA respetada: no se tocó ningún archivo con `2025` en el path/id (ENSANUT 2025 / ENCODAT 2025 / `reserva_respondentes`).

Verificación sha256: todos los 20 archivos abiertos (2018, 2021, 2022, 2023, 2024 × {adultos, adolescentes, integrantes/residentes, utilizadores} donde existen) **COINCIDEN** con `data/manifiesto.yaml`. Detalle al final del documento.

---

## Ola 2018 (ENSANUT 100k NO se usó salvo como alternativa señalada)

Archivos abiertos:
- Adultos: `ensanut_2018__cs_adultos_stata_stata_zip` (CS_ADULTOS.stata.zip), number_rows=43070
- Adolescentes: `ensanut_2018__cs_adolescentes_stata_stata_zip` (CS_ADOLESCENTES.stata.zip), number_rows=17925
- Hogares: `ensanut_2018__cs_hogares_stata_stata_zip` (CS_HOGARES.stata.zip), number_rows=44612
- Residentes (integrantes): `ensanut_2018__cs_residentes_stata_stata_zip` (CS_RESIDENTES.stata.zip), number_rows=158044
- **Utilizadores 2018 (muestra regular, NO 100k): NO EXISTE en el manifiesto/corpus.** Se buscó con patrón `ensanut_2018__cs*util*` y no hay coincidencias; el único id relacionado es `conf17_r9_1_ensanut_2018_cuestionario_utilizadores`, que es solo el CUESTIONARIO PDF, sin `.dta` asociado bajo ese id. La alternativa es la submuestra `ensanut_2018_100k__utilizadores_p_stata_stata_zip` (otra muestra, ENSANUT 100k/Prospera), que NO se abrió (fuera del alcance pedido; se reporta solo como referencia).

### A) Diseño (2018)
- Ponderador de persona: `F_20MAS` (Factor de Adultos, en cs_adultos), `F_10A19` (Factor de Adolescente, en cs_adolescentes), `FACTOR` (Factor de residentes, en cs_residentes), `FAC_HOGAR` (Factor del Hogar, en cs_hogares).
- Estrato de diseño: `EST_DIS` (presente en los 4 archivos). También existe `ESTRATO` ("Estrato sociodemográfico", distinto de diseño) y una var binaria `Urbano/Rural` sin nombre estándar propio (etiqueta de valor {1:'Urbano',2:'Rural'} asociada a `ENT`/zona, ver abajo).
- UPM: `UPM_DIS` (UPM de diseño) en los 4; también existe `UPM` (Unidad Primaria de Muestreo, cruda) en cs_adultos/adolescentes/hogares/residentes.
- Llaves de unión: `UPM` + folio de vivienda/hogar (visible como `P5_4`/folio titular en hogares) — no se leyeron nombres de llave estandarizados tipo FOLIO_I porque 2018 usa convención distinta (UPM + folio numérico de hogar/vivienda incluido en cs_hogares/cs_residentes); no se confirmó el nombre exacto de la llave persona-hogar sin leer más a fondo el archivo de residentes (limitación declarada).

### B) Segmentadores (2018)
- Sexo: `SEXO` (adultos, adolescentes, residentes: "(NOMBRE) es hombre/es mujer").
- Edad: `EDAD` (adultos, adolescentes, residentes).
- Escolaridad: `NIVEL` y `GRADO` ("¿Cuál es el último año y grado que aprobó (NOMBRE) en la escuela?") — SOLO en `cs_residentes` (no en cs_adultos/cs_adolescentes).
- Tamaño de localidad/rural-urbano: variable con VALLBL {1:'Urbano',2:'Rural'} presente en los 4 archivos (asociada a la zona geográfica, ligada a `ENT`).
- Entidad federativa: `ENT` (Clave de Entidad Federativa) en los 4 archivos.

### C) Conductas candidatas (2018)

**C1 — CESD-7 adultos** (`cs_adultos`): 7 reactivos, escala 1-4 idéntica en los 7:
`{1: 'Rara vez o nunca (menos de un día)', 2: 'Pocas veces o alguna vez (1-2 días)', 3: 'Un número de veces considerable (3-4 días)', 4: 'Todo el tiempo o la mayoría del tiempo (5-7 días)'}`
- `P2_1_1` "...¿sentía como si no pudiera quitarse de encima la tristeza...?"
- `P2_1_2` "...¿le costaba concentrarse en lo que estaba haciendo?"
- `P2_1_3` "...¿se sintió deprimido(a)?"
- `P2_1_4` "...¿le parecía que todo lo que hacía era un esfuerzo?"
- `P2_1_5` "...¿no durmió bien?"
- `P2_1_6` "...¿disfrutó de la vida?"
- `P2_1_7` "...¿se sintió triste?"
No se observó variable de puntaje/indicador CESD ya construido en el archivo (solo los 7 reactivos crudos).

CESD-7 adolescentes (`cs_adolescentes`), mismo patrón, escala idéntica:
`P5_1_1..P5_1_7` con el mismo texto en segunda persona ("...¿sentías...", "...¿te sentiste...", etc.)

**C2 — Ideación suicida** adultos: `P12_7` "¿Alguna vez ha pensado en suicidarse?" VALLBL {1:'Sí',2:'No',8:'No responde'}. Intento/autolesión: `P12_8` "¿Alguna vez a propósito se ha herido, cortado, intoxicado o hecho daño con el fin de...?" VALLBL {1:'Sí, una vez',2:'Sí, dos o más veces',3:'Nunca'} (es autolesión/intento, no exactamente "intento de suicidio" en el texto literal, pero es el ítem inmediato siguiente a ideación).
Adolescentes: `P7_16_1` "¿Alguna vez has pensado en suicidarte?" mismas etiquetas; `P7_17` mismo patrón de autolesión que P12_8.

**C3 — Necesidad de salud últimos 3 meses / atendido** — en `cs_residentes` (cuestionario de hogar/integrantes, todas las edades):
- `P4_3` "En el último mes ¿(NOMBRE), ha tenido algún problema de salud, por enfermedad, l[esión]...?" VALLBL {1:'Sí',2:'No',9:'No sabe'} — NOTA: el texto dice "último MES", no "últimos 3 meses" como en 2024 (CAMBIA la ventana temporal).
- `P4_5` "¿Está (NOMBRE) recibiendo o recibió atención por este padecimiento?" — es el equivalente funcional a H0405/H0406 2024 (atendido/no atendido).
- `P4_4` "¿Esto ocurrió en las últimas dos semanas?", `P4_6`-`P4_9` detallan medicamento/costo/quién atendió (incluye "Curandero"/"Yerbero"/"Partera"/"Dependiente de farmacia" como opciones de `P4_8_0x`).

**C4 — Utilizadores/institución**: AUSENTE en 2018 no-100k por falta de dataset (ver arriba). Se recorrió el manifiesto completo buscando patrones `ensanut_2018__*util*` y `ensanut_2018__cs*` (34 ids revisados) sin encontrar `.dta` de utilizadores para la muestra regular 2018.

**C5 — Diagnóstico diabetes/hipertensión** adultos:
- Diabetes: `P3_1` "¿Algún médico le ha dicho que tiene diabetes (o alta el azúcar en la sangre)?" VALLBL {1:'Sí',2:'Sí, durante el embarazo (solo mujeres, diabetes gestacional)',3:'No'}
- Hipertensión: `P4_1` "¿Algún médico le ha dicho que tiene la presión alta?" VALLBL {1:'Sí',2:'No'} (2018 NO tiene la categoría de embarazo que sí aparece en 2024 a0401).

**C6 — Tabaco/alcohol** adultos:
- Tabaco actual: `P13_2` "Actualmente ¿fuma tabaco...?" VALLBL {1:'todos los días?',2:'algunos días?',3:'no fuma actualmente?',8:'No responde'}
- Alcohol: `P13_12_1` "Aproximadamente, ¿cuántas copas toma (tomaba) y con qué frecuencia?" (formato distinto al binario 2024 de "5+/4+ copas últimos 30 días"; en 2018 no se localizó un ítem binario idéntico a a1311/a1312 — posible CAMBIA de formato, pendiente de revisar bloque P13 completo).

---

## Ola 2021

Archivos: `ensadul2021_entrega_w_15_12_2021` (n=13402), `ensadol2021_entrega_w_14_12_2021` (n=4152), `integrantes_ensanut2021_w_12_01_2022` (n=43724), `util2021_entrega_w_14_12_2021` (n=3027).

### A) Diseño (2021)
- Ponderador: `ponde_f` en los 4 archivos.
- Estrato: `estrato` ("Estrato urbanidad/ruralidad", VALLBL {1:'Rural (<2500 Hab)',2:'Urbano (2500-99,999 Hab)',3:'Metropolitano (100mil y + Hab)'}) y `est_sel` ("Estrato de seleccion") en los 4.
- UPM: `upm` ("Unidad primaria de muestreo") en los 4.
- Llaves de unión: `FOLIO_I` (Folio) + `FOLIO_INT` (Folio de integrante) en los 4 archivos — mismo esquema en adultos/adolescentes/integrantes/utilizadores.

### B) Segmentadores (2021)
- Sexo/edad: no confirmados por nombre exacto en adultos/adolescentes en este grep (candidatos `asexo`/`aedad` por analogía con 2024, no verificados línea por línea en 2021 — limitación declarada); en integrantes el bloque H03 trae edad/sexo por analogía con 2024, no verificado nombre exacto.
- Escolaridad: `h0317a` ("¿Cuál es el último año o grado que aprobó...?" VALLBL con niveles Preescolar..Doctorado) y `h0317g` en `integrantes_ensanut2021`.
- Tamaño de localidad: `estrato` (Rural/Urbano/Metropolitano) en los 4 archivos.
- Entidad: `entidad` en adultos/adolescentes/utilizadores; `entidad1` en integrantes.

### C) Conductas candidatas (2021)

**C1 — CESD-7 adultos** (`ensadul2021`): `a0211..a0217`, escala idéntica a 2024 (texto y etiquetas 1-4 con variantes tipográficas menores: "conside-rable" con guión, "tiempo    (5-7 días)" con espacios extra — IDÉNTICO en sustancia).
CESD-7 adolescentes (`ensadol2021`): `d0601a..d0601g`, mismo texto en segunda persona, escala idéntica.
No hay puntaje CESD precalculado en ninguno de los dos archivos.

**C2 — Ideación suicida**: adultos `a1211` "A1211 ¿Alguna vez ha pensado en suicidarse?" (mismo texto que 2024). Adolescentes `d0817` "D0817 ¿Alguna vez has pensado en suicidarte?" (idéntico a 2024). Intento/autolesión explícito NO se encontró como ítem propio en 2021 adultos/adolescentes (solo aparece "Intento de suicidio" como categoría 12 dentro de un catálogo de causas de lesión/violencia en el módulo de accidentes, no como pregunta dedicada de intento de suicidio propio).

**C3 — Necesidad de salud / atendido** (`integrantes_ensanut2021`): `h0401` "H0401 En los últimos 3 meses ¿(USTED/NOMBRE) ha tenido alguna necesidad de salud...?" (IDÉNTICO texto a 2024 h0401, misma ventana de 3 meses); `h0402` catálogo largo de causas (52 categorías, incluye códigos 47 Depresión, 48 Ansiedad, 49 Insomnio, 50 Estrés, 51 Otra condición mental); `h0404` buscó atención; `h0406` "fue atendido por esa necesidad de salud en alguna instituc[ión]..." — corresponde a H0406 del encargo.

**C4 — Utilizadores/institución** (`util2021`): `u0201` "U0201 ¿En qué institución de salud (USTED/NOMBRE) se atendió/recibió atención?" con 23 categorías; cat 12 = "Consultorios pertenecientes a farmacias / Farmacia con consu[ltorio]..." (equivalente a la de 2024); cat 20 = "Curandero, hierbero, naturista" (equivalente a la de 2024, sin coma en "hierbero" vs 2024 que usa "Curandero(a), hierbero(a), naturista"). 2021 tiene 23 categorías vs 26 en 2024 (2024 agrega 24 Consultorio psicológico, 25 Centro de salud mental CESAME, 26 IMSS-BIENESTAR como categoría propia — en 2021 "IMSS Bienestar" es cat 7, fusionado con Oportunidades). CAMBIA: catálogo se amplía de 2021→2024.

**C5 — Diagnóstico diabetes/hipertensión** adultos: `a0301` "¿Algún médico le ha dicho que tiene diabetes (o alta el azúcar en la sangre)?" VALLBL {1:'SÍ.',2:'Sí, durante el embarazo (solo mujeres, diabetes gestacional',3:'NO.'} — IDÉNTICO a 2024 (a0301) salvo mayúsculas/puntuación. `a0401` "¿Algún médico le ha dicho que tiene la presión alta?" VALLBL {1:'SÍ.',2:'SÍ, durante el embarazo.',3:'NO.'} — IDÉNTICO a 2024 (a0401).

**C6 — Tabaco/alcohol** adultos: `a1301` "A1301 Actualmente, ¿fuma tabaco…" (mismo inicio que 2024 a1301); alcohol `a1311`/`a1312` "En los últimos 30 días, ¿Tomó cinco/cuatro o más copas de alcohol en al menos una ocasión?" — IDÉNTICO patrón a 2024. Adolescentes: `d0101` tabaco actual, `d0111`/`d0112` mismas preguntas de 5+/4+ copas en 30 días — IDÉNTICO a 2024 (d0101/d0111/d0112).

---

## Ola 2022

Archivos: `ensadul2022_entrega_w` (n=11913), `ensadol2022_entrega_w` (n=3547), `integrantes_ensanut2022_w` (n=36483), `util2022_entrega_w` (n=4229).

### A) Diseño (2022)
- Ponderador: `ponde_f` en los 4 archivos.
- Estrato/UPM/llaves: mismo esquema que 2021 — `estrato` ("Estrato urbanidad/ruralidad"), `est_sel`, `upm` ("Unidad primaria de muestreo"), `FOLIO_I`+`FOLIO_INT` (verificados en adultos; por consistencia de diseño INSP se asume igual esquema en adolescentes/integrantes/utilizadores 2022, no releído línea por línea en los otros 3 — limitación declarada).

### B) Segmentadores (2022)
- Escolaridad: `h0317a` en `integrantes_ensanut2022`, IDÉNTICO catálogo a 2021/2024 (Preescolar..Doctorado).
- Resto (sexo/edad/entidad/tamaño de localidad): mismo patrón de nombres que 2021 por consistencia de diseño INSP, no releído variable por variable en 2022 (limitación declarada; `estrato` confirmado presente).

### C) Conductas candidatas (2022)

**C1 — CESD-7**: adultos `a0211..a0217` (`ensadul2022`) IDÉNTICO texto y escala a 2021/2024. Adolescentes `d0601a..d0601g` (`ensadol2022`) IDÉNTICO a 2021/2024.

**C2 — Ideación suicida**: adultos `a1211` "A1211 ¿Alguna vez ha pensado en suicidarse?" IDÉNTICO. Adolescentes `d0817` "D0817 ¿Alguna vez has pensado en suicidarte?" IDÉNTICO. Intento de suicidio dedicado: AUSENTE (en adolescentes 2022 la categoría de catálogo de violencia ahora dice "Intento de homicidio" en vez de "Intento de suicidio" como en 2021 — CAMBIA/desaparece esa mención lateral).

**C3 — Necesidad de salud / atendido** (`integrantes_ensanut2022`): `h0401` "H0401 En los últimos 3 meses ¿(USTED/NOMBRE) ha tenido alguna necesidad de salud..." IDÉNTICO a 2021/2024, pero VALLBL se simplifica a {1:'Sí',2:'No'} (en 2021/2024 no se leyó el VALLBL de h0401 directamente, solo se confirmó el texto; aquí en 2022 sí es binario simple). `h0406` "¿...fue atendido por esa necesidad de salud en alguna instituc[ión]...?" VALLBL {1:'Sí',2:'No'} — IDÉNTICO texto a 2021/2024.

**C4 — Utilizadores/institución** (`util2022`): `u0201` mismo texto, 23 categorías; cat 12 = "Consultorios pertenecientes a farmacias / Farmacias con cons[ultorio]..." (equivalente); cat 20 = "Curandero(a), hierbero(a), naturista" — esta vez con paréntesis de género, IDÉNTICO a la redacción de 2024. Sigue sin las 3 categorías nuevas de 2024 (24 Consultorio psicológico, 25 CESAME, 26 IMSS-BIENESTAR separado) — CAMBIA (se amplía) de 2022→2024, igual que de 2021→2024.

**C5 — Diagnóstico diabetes/hipertensión**: adultos `a0301`/`a0401` — texto y VALLBL IDÉNTICOS a 2021/2024. Adolescentes: aparece un bloque propio `d02o1a` "¿Algún médico te ha dicho que tienes diabetes o la azúcar alta en la sangre?" y `d02o1b` "...la presión alta o hipertensión?" (VALLBL {1:'Sí',2:'No',9:'No sabe'}) — este bloque en adolescentes no se verificó su presencia/ausencia en 2021/2024 con el mismo detalle (ver nota en 2021, donde sí aparece `d02o1a/b` también) — CONSISTENTE con 2021.

**C6 — Tabaco/alcohol**: adultos `a1301`/`a1311`/`a1312` IDÉNTICO texto a 2021/2024. Adolescentes `d0111`/`d0112` IDÉNTICO a 2021/2024 (5+/4+ copas en 30 días).

---

## Ola 2023

Archivos: `adultos_ensanut2023_w_n` (n=6772), `adolescentes_ensanut2023_w_n` (n=1924), `integrantes_ensanut2023_w_n` (n=20018), `utilizadores_ensanut2023_w_n` (n=2184).

### A) Diseño (2023)
- Ponderador: `ponde_f` en adultos e integrantes (verificado).
- Estrato: `estrato` ("Estrato urbanidad/ruralidad") y `est_sel` en adultos e integrantes.
- UPM: `upm` ("Unidad Primaria de Muestreo") en adultos e integrantes.
- Llaves de unión: `FOLIO_I` (Folio) + `FOLIO_INT` (Folio de integrante) en adultos e integrantes — mismo esquema que 2021/2022.

### B) Segmentadores (2023)
- Escolaridad: `h0317a` "¿Cuál es el último año o grado que aprobó (NOMBRE) en la escuela? NIVEL" en `integrantes_ensanut2023_w_n`.
- Resto (sexo/edad/entidad/tamaño de localidad): por consistencia de diseño con 2021/2022, se asume igual esquema (`estrato` confirmado); no se releyó variable por variable.

### C) Conductas candidatas (2023)

**C1 — CESD-7**: adultos `a0211..a0217` (número de rows más bajo, 6772 — muestra reducida 2023) IDÉNTICO texto y escala a 2021/2022/2024. Adolescentes `d0601a..d0601g` IDÉNTICO.

**C2 — Ideación suicida**: adultos `a1211` "¿Alguna vez ha pensado en suicidarse?" VALLBL {1:'Sí',2:'No',9:'No responde'} — mismo texto que 2021/2022/2024, código "No responde" pasa de 8/9 según ola (2018/2021/2022 code 8→9 en 2023, CAMBIA levemente el código pero no el texto). Adolescentes `d0817` "¿Alguna vez has pensado en suicidarte?" VALLBL {1:'Sí',2:'No',8:'No responde'} IDÉNTICO a 2024. Intento de suicidio dedicado: no localizado (mismo patrón AUSENTE que 2021/2022).

**C3 — Necesidad de salud / atendido** (`integrantes_ensanut2023_w_n`): `h0401` "En los últimos 3 meses ¿(USTED/NOMBRE) ha tenido alguna necesidad de salud..." VALLBL {1:'Sí',2:'No'} IDÉNTICO a 2022/2024. `h0406` "¿...fue atendido por esa necesidad de salud en alguna instituc[ión]...?" VALLBL {1:'Sí',2:'No'} IDÉNTICO a 2022/2024.

**C4 — Utilizadores/institución** (`utilizadores_ensanut2023_w_n`): `u0201` "U0201 ¿En qué institución de salud (USTED/NOMBRE) se/te atendió/atendiste o reci[bió]...?" (texto ahora incluye conjugación para adolescentes, "se/te"). 25 categorías: agrega respecto a 2021/2022 la cat 24 "Consultorio psicológico" y 25 "Centro de salud mental (CESAME)"; AÚN NO tiene la cat 26 "IMSS-BIENESTAR" separada de 2024 (sigue como cat 7 "IMSS Bienestar (antes Oportunidades)"). Cat 12 "Consultorios pertenecientes a farmacias / Farmacias con cons[ultorio]..." IDÉNTICO a 2022; cat 20 "Curandero(a), hierbero(a), naturista" IDÉNTICO a 2022/2024.

**C5 — Diagnóstico diabetes/hipertensión** adultos: `a0301`/`a0401` — texto y VALLBL IDÉNTICOS a 2021/2022/2024.

**C6 — Tabaco/alcohol** adultos: `a1301` IDÉNTICO texto (VALLBL con código "No responde"=9, igual que 2023 en a1211, vs 8 en 2021/2022 — CAMBIA levemente el código, no el texto); `a1311`/`a1312` IDÉNTICO texto ("En los últimos 30 días, ¿Tomó cinco/cuatro o más copas de alcohol en al menos una ocasión?").

---

## Ola 2024 (referencia de comparabilidad)

Archivos: `adultos_ensanut2024_w` (n=12924), `adolescentes_ensanut2024_w` (n=3730), `integrantes_ensanut2024_w_icb` (n=36021), `utilizadores_ensanut2024_w` (n=3223). Cuestionarios PDF en `/home/pc0/mm-corpus/descargas_mx_espejo/ENSANUT2024-v2026-09-01/` (ids `1_vfinal_..5_vfinal_..._cuestionarios`).

### A) Diseño (2024)
- Ponderador: `ponde_f` (adultos: "Ponderador"; integrantes: "ponderador de integrantes de hogar").
- Estrato: `estrato` "Estrato urbanidad/ruralidad" VALLBL {1:'Rural (<2500 Hab)',2:'Urbano (2500-99,999 Hab)',3:'Metropolitano (100mil y + Hab)'}; también `est_sel` "Estrato de seleccion".
- UPM: `upm` "Unidad primaria de muestreo".
- Llaves de unión adultos↔integrantes: `FOLIO_I` (Folio) + `FOLIO_INT` (Folio integrante/de integrante) — mismos nombres en los 4 archivos.

### B) Segmentadores (2024)
- Sexo: `sexo` ("Sexo del Seleccionado", adultos), `asexo` (bloque preliminar adultos), `dsexo` (adolescentes), `h0302` (integrantes, "Sexo").
- Edad: `edad` (adultos/adolescentes, "Edad del Seleccionado"), `aedad`/`dedad` (bloques preliminares), `h0303` (integrantes, "Edad").
- Escolaridad: `h0317a`/`h0317g` (integrantes) — VALLBL {1:'Preescolar',2:'Primaria',3:'Secundaria',4:'Preparatoria o Bachillerato',5:'Normal básica',6..8:'Estudios técnicos...',9:'Normal de licenciatura',10:'Licenciatura o profesional',11:'Maestría',12:'Doctorado'}. Solo en integrantes, no en adultos/adolescentes.
- Tamaño de localidad/rural-urbano: `estrato` (Rural/Urbano/Metropolitano) en los 4 archivos.
- Entidad: `entidad` (adultos), `entidad1`/`x_region` (integrantes).

### C) Conductas candidatas (2024)

**C1 — CESD-7 adultos** (`adultos_ensanut2024_w`): `a0211..a0217`, escala:
`{1: 'Rara vez o nunca (menos de un día).', 2: 'Pocas veces o alguna vez (1-2 días).', 3: 'Un número de veces considerable (3-4 días).', 4: 'Todo el tiempo o la mayoría del tiempo (5-7 días).'}`
- a0211 "...¿Sentía como si no pudiera quitarse de encima la tristeza...?"
- a0212 "...¿le costaba concentrarse en lo que estaba haciendo?"
- a0213 "...¿se sintió deprimido/a?"
- a0214 "...¿le parecía que todo lo que hacía era un esfuerzo?"
- a0215 "...¿no durmió bien?"
- a0216 "...¿disfruto de la vida?"
- a0217 "...¿se sintió triste?"
Sin puntaje CESD precalculado en el archivo (7 reactivos crudos únicamente). CESD-7 adolescentes (`adolescentes_ensanut2024_w`): `d0601a..d0601g`, mismo texto en segunda persona ("¿Sentías...", "¿Te sentiste...", etc.), escala idéntica.

**C2 — Ideación suicida**: adultos `a1211` "A1211 ¿Alguna vez ha pensado en suicidarse?" VALLBL {1:'Sí',2:'No',9:'No responde'}. Adolescentes `d0817` "D0817 ¿Alguna vez has pensado en suicidarte?" VALLBL {1:'Sí',2:'No',8:'No responde'}. Intento de suicidio dedicado: AUSENTE en ambos archivos de 2024 — se recorrió el bloque completo de factores de riesgo/salud mental (sección XIII en adultos, `nota005`..`a1314`, y sección equivalente en adolescentes `d0601`..`d0817`+siguientes) buscando "intent", "autolesion", "lastim", "herid", "cort" sin encontrar ítem propio de intento de suicidio en 2024 (270 variables examinadas en adultos, 250 aprox en adolescentes por conteo de líneas `VAR` en el archivo).

**C3 — Necesidad de salud últimos 3 meses / atendido** (`integrantes_ensanut2024_w_icb`): `h0401` "H0401 En los últimos 3 meses ¿(USTED/NOMBRE) ha tenido alguna necesidad de salud..." VALLBL {1:'Sí',2:'No'}. `h0404` "H0404 ¿(USTED/NOMBRE) buscó atención por esa necesidad de salud?" VALLBL {1:'Sí',2:'No'}. `h0406` "H0406 ¿(USTED/NOMBRE) fue atendido por esa necesidad de salud en alguna instituc[ión]...?" VALLBL {1:'Sí',2:'No'}. También existen `H0405A/B/C` (motivo de no buscar atención) y `H0407A/B/C` (motivo de no ser atendido).

**C4 — Lugar de atención (utilizadores)** (`utilizadores_ensanut2024_w`): `u0201` "U0201 ¿En qué institución de salud (USTED/NOMBRE) se atendió/recibió atención?" — 26 categorías. Cat 12 = "Consultorios pertenecientes a farmacias / Farmacias con consultorio médico". Cat 20 = "Curandero(a), hierbero(a), naturista". Cat 21 = "Homeópata, partera, acupunturista". Nuevas respecto a 2021-2023: cat 24 "Consultorio psicológico", cat 25 "Centro de salud mental (CESAME)", cat 26 "IMSS-BIENESTAR (que eran antes centros de salud de la Secretaría de Salud)" como categoría separada de IMSS/ISSSTE (en 2021-2023 estaba fusionada como cat 7 dentro de "IMSS Bienestar (antes Oportunidades)"). Universo del cuestionario de utilizadores: personas que en `h0406`/análogo de integrantes reportaron haber sido atendidas; n=3223 (submuestra de quienes usaron servicios).

**C5 — Diagnóstico diabetes/hipertensión** adultos: `a0301` "¿Algún médico le ha dicho que tiene diabetes (o alta el azúcar en la sangre)?" VALLBL {1:'SÍ.',2:'Sí, durante el embarazo (solo mujeres, diabetes gestacional).',3:'NO.'}. `a0401` "¿Algún médico le ha dicho que tiene la presión alta?" VALLBL {1:'SÍ.',2:'SÍ, durante el embarazo.',3:'NO.'}.

**C6 — Tabaco/alcohol** adultos: `a1301` "A1301 Actualmente, ¿fuma tabaco…" VALLBL {1:'todos los días?',2:'algunos días?',3:'no fuma actualmente?',9:'No responde'}. Alcohol: `a1311` "A1311 En los últimos 30 días, ¿Tomó cinco o más copas de alcohol en al menos una ocasión?" y `a1312` "A1312 ...cuatro o más copas..." VALLBL {1:'Sí',2:'No',9:'No responde'} en ambos. Adolescentes: `d0101` tabaco actual, `d0111`/`d0112` mismas preguntas de 5+/4+ copas en 30 días.

---

## Tabla-resumen de comparabilidad C1..C6 × olas (texto de pregunta contra 2024)

| Conducta | 2018 | 2021 | 2022 | 2023 | 2024 (referencia) |
|---|---|---|---|---|---|
| **C1 CESD-7 adultos** | IDÉNTICO (P2_1_1..7, misma escala 1-4) | IDÉNTICO (a0211-a0217) | IDÉNTICO (a0211-a0217) | IDÉNTICO (a0211-a0217) | a0211-a0217 |
| **C1 CESD-7 adolescentes** | IDÉNTICO (P5_1_1..7) | IDÉNTICO (d0601a-g) | IDÉNTICO (d0601a-g) | IDÉNTICO (d0601a-g) | d0601a-g |
| **C2 Ideación suicida adultos** | IDÉNTICO en fondo (P12_7, mismo texto salvo numeración) | IDÉNTICO (a1211) | IDÉNTICO (a1211) | IDÉNTICO (a1211, cod. NR 8→9) | a1211 |
| **C2 Ideación suicida adolescentes** | IDÉNTICO (P7_16_1) | IDÉNTICO (d0817) | IDÉNTICO (d0817) | IDÉNTICO (d0817) | d0817 |
| **C2 Intento de suicidio** | PRESENTE pero es AUTOLESIÓN (P12_8/P7_17), no "intento" literal | AUSENTE como ítem propio (solo mención lateral en catálogo de violencia) | AUSENTE (mención lateral cambia a "Intento de homicidio") | AUSENTE | AUSENTE (270+ vars adultos, ~250 adolescentes revisadas, sin ítem de intento) |
| **C3 Necesidad de salud (integrantes)** | CAMBIA ventana: "último MES" (P4_3) vs "últimos 3 meses" | IDÉNTICO texto y ventana (h0401, "últimos 3 meses") | IDÉNTICO (h0401) | IDÉNTICO (h0401) | h0401 "últimos 3 meses" |
| **C3 Atendido** | Equivalente funcional P4_5 (recibiendo/recibió atención) | h0406 IDÉNTICO texto | h0406 IDÉNTICO | h0406 IDÉNTICO | h0406/h0404 |
| **C4 Institución utilizadores (u0201)** | AUSENTE: no existe dataset de utilizadores para la muestra 2018 regular (solo 100k, otra muestra) | 23 categorías; cat 12 farmacias / cat 20 curandero presentes; SIN cat 24/25/26 de 2024 | 23 categorías; mismo patrón que 2021 | 25 categorías; agrega 24 psicológico y 25 CESAME; sin 26 IMSS-BIENESTAR separado | 26 categorías (agrega IMSS-BIENESTAR separado) |
| **C5 Diabetes** | Similar (P3_1) pero SIN "SÍ." en mayúsculas/puntuación de 2021+ | IDÉNTICO (a0301) | IDÉNTICO | IDÉNTICO | a0301 |
| **C5 Hipertensión** | CAMBIA: 2018 P4_1 solo {Sí,No}, sin categoría de embarazo | IDÉNTICO (a0401, con categoría embarazo) | IDÉNTICO | IDÉNTICO | a0401 (con categoría embarazo) |
| **C6 Tabaco actual** | IDÉNTICO en fondo (P13_2) | IDÉNTICO (a1301) | IDÉNTICO | IDÉNTICO | a1301 |
| **C6 Alcohol 5+/4+ copas 30 días** | CAMBIA: 2018 usa formato de frecuencia/cantidad continuo (P13_12_1), no ítem binario 5+/4+ | IDÉNTICO (a1311/a1312) | IDÉNTICO | IDÉNTICO | a1311/a1312 |

Nota general: de 2018 a 2021 hay una renumeración/estandarización de nombres de variable (de `P#_#_#` a `a0###`/`d0###`/`h0###`) que la comparación siguió por TEXTO literal de la pregunta, no por nombre, conforme al encargo. A partir de 2021 el esquema de nombres y en gran medida el texto se estabiliza; los cambios notables 2021→2024 son: ampliación del catálogo de instituciones en utilizadores (C4) y estabilidad casi total en CESD-7, diabetes, hipertensión y tabaco/alcohol.

---

## Archivos abiertos: id + sha256 + verificación

| id | sha256 (primeros 16) | Verificación |
|---|---|---|
| ensanut_2018__cs_adultos_stata_stata_zip | 1c89e2348d2fdf0e | COINCIDE |
| ensanut_2018__cs_adolescentes_stata_stata_zip | 562de091edf873df | COINCIDE |
| ensanut_2018__cs_hogares_stata_stata_zip | f0b9cb5561e3234d | COINCIDE |
| ensanut_2018__cs_residentes_stata_stata_zip | 720c6df363dfa24a | COINCIDE |
| ensanut_2021__ensadul2021_entrega_w_15_12_2021_stata_stata_zip | cfc2cd6d4e44b1bd | COINCIDE |
| ensanut_2021__integrantes_ensanut2021_w_12_01_2022_stata_stata_zip | 0239932685aa9803 | COINCIDE |
| ensanut_2021__util2021_entrega_w_14_12_2021_stata_stata_zip | a6d83c40694888d0 | COINCIDE |
| ensanut_2021__ensadol2021_entrega_w_14_12_2021_stata_stata_zip | 40135c1ce31751d0 | COINCIDE |
| ensanut_2022__ensadul2022_entrega_w_stata_stata_zip | bfdfdb82bcb31149 | COINCIDE |
| ensanut_2022__integrantes_ensanut2022_w_stata_stata_zip | b01e89fbd0b52663 | COINCIDE |
| ensanut_2022__util2022_entrega_w_stata_stata_zip | 5ff32de19cadaaec | COINCIDE |
| ensanut_2022__ensadol2022_entrega_w_stata_stata_zip | ebfbd04bea195a4c | COINCIDE |
| ensanut_2023__adultos_ensanut2023_w_n_stata_stata_zip | c6ccad40206aec82 | COINCIDE |
| ensanut_2023__integrantes_ensanut2023_w_n_stata_stata_zip | 139d967e11362b68 | COINCIDE |
| ensanut_2023__utilizadores_ensanut2023_w_n_stata_stata_zip | 8b3e0ad01caa13f6 | COINCIDE |
| ensanut_2023__adolescentes_ensanut2023_w_n_stata_stata_zip | 2cbae9b9f3c80655 | COINCIDE |
| adultos_ensanut2024_w_stata_stata__v2026_09_01 | 0fa8f4436fa427cc | COINCIDE |
| integrantes_ensanut2024_w_icb_stata_stata__v2026_09_01 | 20a9fae339da3fa3 | COINCIDE |
| utilizadores_ensanut2024_w_stata_stata__v2026_09_01 | b40a4dce264e6570 | COINCIDE |
| adolescentes_ensanut2024_w_stata_stata__v2026_09_01 | 47251c90bd411e6d | COINCIDE |

No se abrió ningún cuestionario PDF (los nombres/etiquetas de variable y valor ya venían en el .dta y bastaron para cubrir lo pedido en C1-C6); tampoco se abrió `ensanut_2018_100k__*` (fuera de alcance, solo referenciado). No se tocó ningún archivo `2025` (reserva respetada).
