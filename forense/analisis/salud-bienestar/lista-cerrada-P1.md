# Lista cerrada P1 · ACTO GEN2-SALUD-Y-BIENESTAR-PISOS-1

Congelada en el COMMIT-1 (24/sep/2026), **antes** de abrir un solo valor de microdato de
ENSANUT, ENCODAT o ENBIARE. Fuente de cada reactivo: el texto de la pregunta (A.15), leído
de las etiquetas de variable y de valor (`pyreadstat`, `metadataonly=True`) y del FD de
ENBIARE; informes de estructura en esta carpeta (`estructura-ensanut.md`,
`estructura-encodat.md`, `estructura-enbiare.md`). Cambiar esta lista después del
COMMIT-1 es PARO (d).

## 1 · Olas abiertas y reservadas (E.6)

| instrumento | olas en corpus (microdato) | reservada | se abre aquí |
|---|---|---|---|
| ENSANUT | 2006, 2012, 2016, 2018, 2020, 2021, 2022, 2023, 2024, 2025 | **2025** (`RESERVADA-NO-ABIERTA-NO-INDEXAR-L`, 24 payloads) | 2021, 2022, 2023, 2024 |
| ENCODAT | 2016–17, 2025 | **2025** (3 payloads) | 2016–17 |
| ENBIARE | 2021 | — (una sola ola: no hay historia que reservar; se abre y se declara) | 2021 |

**ENSANUT 2018 queda fuera de la serie (declarado):** cambia de esquema (`P#_#_#`, llaves
`UPM`+folio sin nombre estándar), la necesidad de salud es de «último mes» (no «últimos 3
meses»), la hipertensión no trae la categoría de embarazo y el alcohol no trae el ítem
binario de 5+/4+ copas; su muestra regular no tiene archivo de utilizadores. La serie
2021→2024 (cuatro olas, mismo esquema `FOLIO_I`/`FOLIO_INT`/`ponde_f`/`est_sel`/`upm`,
textos IDÉNTICOS salvo lo anotado) basta para el IC calibrado de persistencia (≥ 3 olas).
ENSANUT 2020 no se incluye: su cuestionario de adultos es el de la ola COVID (declarado,
no verificado ítem por ítem en este acto) — va a NO-CORRIDO.

## 2 · Conductas, por instrumento

### ENSANUT 2021–2024 → `CALC-ENSANUT-PISOS-SALUD-0001`

Diseño: `ponde_f` (persona), estrato `est_sel`, UPM `upm`. Ejes, uno a la vez: SEXO,
EDAD, ESTRATO (`estrato`: rural < 2 500 / urbano / metropolitano ≥ 100 mil), ESCOLARIDAD
(`h0317a` de integrantes, por llave `FOLIO_I`+`FOLIO_INT` m:1, sólo 20+). Sin entidad
(declarado: 32 celdas por ola con n de 1.9–13 mil adultos no sostienen IC; región U5 queda
como referencia en la nota).

| conducta | archivo | texto (A.15) | 1 | 0 | fuera (NaN) |
|---|---|---|---|---|---|
| DEPRESION-CESD7 | adultos 20+ | a0211–a0217 «Durante la última semana…» (CESD-7) | puntaje ≥ 9 (20–59) / ≥ 5 (60+) | debajo | algún ítem fuera de 1–4 |
| IDEACION-SUICIDA-ADULTOS | adultos 20+ | a1211 «¿Alguna vez ha pensado en suicidarse?» | 1 | 2 | 9 |
| DX-DIABETES | adultos 20+ | a0301 «¿Algún médico le ha dicho que tiene diabetes…?» | 1 | 2 (gestacional), 3 | otro |
| DX-HIPERTENSION | adultos 20+ | a0401 «¿…tiene la presión alta?» | 1 | 2 (embarazo), 3 | otro |
| FUMA-ACTUAL | adultos 20+ | a1301 «Actualmente, ¿fuma tabaco…» | 1, 2 | 3 | 9 |
| ALCOHOL-12M | adultos 20+ | a1308 «En los últimos 12 meses, ¿con qué frecuencia tomó al menos una copa…» | 1–4 | 5, 6 | 9 |
| ALCOHOL-EXCESIVO-30D | adultos 20+ | a1311 (hombres, 5+ copas) / a1312 (mujeres, 4+ copas) «En los últimos 30 días…» | 1 | 2; y a1308 ∈ {5, 6} (salto) | 9 |
| NECESIDAD-SALUD-3M | integrantes, todas las edades | h0401 «En los últimos 3 meses… alguna necesidad de salud» | 1 | 2 | — |
| BUSCO-ATENCION | integrantes con h0401 = 1 | h0404 «¿buscó atención por esa necesidad de salud?» | 1 | 2 | resto |
| FUE-ATENDIDO | integrantes con h0404 = 1 | h0406 «¿fue atendido por esa necesidad de salud…?» | 1 | 2 | resto |
| ATENCION-CONSULTORIO-FARMACIA | utilizadores | u0201 «¿En qué institución de salud se atendió?» | 12 «Consultorios pertenecientes a farmacias» | otra categoría 1–26 | fuera de 1–26 |
| ATENCION-CURANDERO-HIERBERO | utilizadores | u0201 | 20 «Curandero(a), hierbero(a), naturista» | otra 1–26 | fuera de 1–26 |
| IDEACION-SUICIDA-ADOLESCENTES | adolescentes 10–19 | d0817 «¿Alguna vez has pensado en suicidarte?» | 1 | 2 | 8 |

Comparabilidad (texto contra 2024): IDÉNTICO 2021–2024 en todas, con dos notas. (i) u0201
amplía su catálogo (23 → 25 → 26 categorías: consultorio psicológico, CESAME, IMSS-BIENESTAR
separado); los códigos 12 y 20 no cambian de texto, pero el denominador reparte distinto:
se declara como cambio de instrumento y cuenta en τ². (ii) El código «No responde» pasa de
8 a 9 en algunos ítems: ambos quedan fuera.

### ENCODAT 2016–17 → `CALC-ENCODAT-PISOS-SUSTANCIAS-0001`

Diseño: `ponde_ss` (individual); `est_var`, `code_upm`, `estrato` del hogar por la llave
declarada `id_pers[:20] == id_hogar` (no documentada por el catálogo; el medidor cuenta los
no pareados en `G-JOIN-SIN-HOGAR`). Universo 12–65 (`ds3`). Ejes: SEXO (`ds2`), EDAD (12–17,
18–34, 35–65), ESTRATO, ESCOLARIDAD (`ds9`, sólo 18+). Sin región: la variable no existe en
ningún archivo (búsqueda en el informe de estructura); sin entidad (mismo motivo que
ENSANUT).

| conducta | texto (A.15) | regla |
|---|---|---|
| ALCOHOL-12M | al4 «En los últimos 12 meses, ¿tomó alguna bebida que contenga alcohol?» | 1 → 1; 2 → 0; al1 = 2 (nunca) → 0 |
| ALCOHOL-30D | al9 «En los últimos 30 días…» | 1 → 1; 2 → 0; al1 = 2 o al4 = 2 → 0 |
| ALCOHOL-EXCESIVO-12M | al11 «mayor número de copas en un solo día (12 meses)» | hombres 5+ copas (códigos 1–4), mujeres 4+ (1–5) → 1; resto → 0; no bebió 12 m → 0; 9 fuera |
| FUMA-ACTUAL | tb02 «¿Actualmente fuma tabaco todos los días, algunos días o no fuma?» | 1, 2 → 1; 3 → 0; sin dato y tb05 = 2 (nunca) → 0 |
| CIGARRO-ELECTRONICO-ALGUNA-VEZ | tb50 «¿Alguna vez… usó un cigarro electrónico?» | 1 / 2 |
| DROGA-ILEGAL-ALGUNA-VEZ | di1a–di1i «¿ha tomado, usado, probado…?» (9 sustancias) | alguna = 1 → 1; todas = 2 → 0 |
| MARIGUANA-ALGUNA-VEZ | di1a | 1 / 2 |
| DROGA-MEDICA-SIN-RECETA-ALGUNA-VEZ | dm1a–dm1d | alguna = 1 → 1; todas = 2 → 0 |
| OPIACEOS-SIN-RECETA-ALGUNA-VEZ | dm1a «Opiáceos…» (sin tramadol en el texto 2016) | 1 / 2 |
| CONSULTO-PROFESIONAL-POR-CONSUMO | tp1 «¿Alguna vez… ha consultado a algún profesional de la salud por su uso de alcohol o drogas…?» | 1 / 2 (universo = a quien el cuestionario se lo preguntó; N se reporta) |

### ENBIARE 2021 → `CALC-ENBIARE-PISOS-BIENESTAR-0001`

Diseño: `FAC_ELE`, `EST_DIS`, `UPM_DIS` (llaves opacas). Persona elegida 18+ (TENBIARE) con
SEXO, EDAD, NIVEL de TSDEM por `FOLIO`+`VIV_SEL`+`HOGAR`+`N_REN`. Ejes: SEXO, EDAD (18–29,
30–44, 45–59, 60+), ESCOLARIDAD (`NIVEL`), TLOC (4 tamaños de localidad).

| conducta | texto (FD) | regla |
|---|---|---|
| SATISFACCION-VIDA | PA1 «qué tan satisfecho(a) se encuentra actualmente con su vida» 0–10 | media |
| ESCALERA-CANTRIL | PA5 «¿En qué escalón siente que su vida se ubica actualmente?» 0–10 | media |
| DEPRESION-CESD7 | PD2_1–PD2_7 (0–3), PD2_6 invertido | ≥ 9 (18–59) / ≥ 5 (60+) → 1 |
| ANSIEDAD-GAD2 | PD3_1, PD3_2 (0–3) | suma ≥ 3 → 1 |
| CONFIANZA-MAYORIA-GENTE | PB1_01 «¿cuánto confía en la mayoría de la gente?» 0–10 | media |
| CONFIANZA-GENTE-CONOCIDA | PB1_02 | media |
| CONFIANZA-POLICIA-MUNICIPAL | PB1_04 | media |
| CONFIANZA-PARTIDOS | PB1_11 | media |
| CUENTA-APOYO-FAMILIA | PB2_1 «¿…siempre contará con la ayuda de personas de su familia?» | 1 → 1; 2, 3 («no tiene familia») → 0 |
| CUENTA-APOYO-AMISTADES | PB2_2 | ídem |
| TIENE-RELIGION | PG6 «¿Usted tiene una religión?» | 1 / 2 |
| ASISTE-SERVICIO-RELIGIOSO | PG7 «¿Acostumbra asistir a su iglesia, templo o servicio religioso?» | 1 → 1; 2 → 0; PG6 = 2 (blanco por secuencia) → 0 |

Cortes CESD-7 (≥ 9 en adultos, ≥ 5 en 60+): los de la validación del CESD-7 que usa el
INSP para ENSANUT (Salinas-Rodríguez et al., Salud Pública Mex 2013/2014), fijados aquí,
antes del dato, e idénticos en ENSANUT y ENBIARE. GAD-2 ≥ 3: corte de Kroenke et al.
(2007). Ninguno se ajusta con el resultado.

## 3 · Cruce con las 29 afirmaciones MEDIBLE del mapa que nombran ENSANUT/ENCODAT/ENBIARE

| afirmación | conducta que la mide aquí | estado |
|---|---|---|
| SALMEN-013 (depresión 2022, 16.7 %) · SALMEN-014 (brecha por sexo) | ENSANUT DEPRESION-CESD7 × SEXO/EDAD | MIDE |
| JUV-009 (ideación 7.6 % adol / 7.7 % adultos; intento) | IDEACION-SUICIDA-ADOLESCENTES / -ADULTOS | MIDE ideación; «intento» NO-CONSTRUIBLE por texto en 2021–23 (a1213 es autolesión, no intento) |
| SALUD-006 (17.7 % en farmacia, 2022) · SALUD-030 | ATENCION-CONSULTORIO-FARMACIA × ESCOLARIDAD/ESTRATO | MIDE (la condición «informal, sin IMSS» no es eje aquí) |
| SALUD-009 (necesidad 21.6 % H / 27.4 % M, 2022) | NECESIDAD-SALUD-3M × SEXO | MIDE |
| SALUD-036 (hombre pospone) | BUSCO-ATENCION × SEXO | MIDE la conducta; «machismo» es mecanismo, no se mide |
| RURAL-021 (curandería) | ATENCION-CURANDERO-HIERBERO × ESTRATO | MIDE uso, no «lógica interna» |
| SALUD-007 (alcohol mujeres 62.6 % 2016 → 69.3 % 2025) | ENCODAT ALCOHOL-12M × SEXO | MIDE el lado 2016; 2025 RESERVADA |
| SALUD-008 (binge adolescente 8.3 % 2016) | ALCOHOL-EXCESIVO-12M × EDAD 12–17 | MIDE 2016 (definición de ENCODAT 2016 no verificada contra el report) |
| SALUD-019 (cigarro electrónico 1.1 % 2016) | CIGARRO-ELECTRONICO-ALGUNA-VEZ | MIDE 2016 («alguna vez», el report no dice la ventana) |
| SALUD-039 (opioides 0.1 % → 1.4 %, tramadol) | OPIACEOS-SIN-RECETA-ALGUNA-VEZ | MIDE 2016 |
| SALUD-017 (droga ilegal por región, 2025) | DROGA-ILEGAL-ALGUNA-VEZ (total) | 2025 RESERVADA; región NO-CONSTRUIBLE en 2016 |
| EMOC-028 (satisfacción alta, depresión baja) | ENBIARE SATISFACCION-VIDA, DEPRESION-CESD7 | MIDE nivel; la comparación entre países no |
| CLASE-040 (facilidad para cubrir gastos) | — | NO-CONSTRUIBLE: el ítem no está en ENBIARE 2021 (FD completo) |
| SALUD-018 (fentanilo) · JUV-010 (malestar psicológico ENCODAT 2025) | — | RESERVADA (2025); ENCODAT 2016 no trae escala de malestar |
| APUEST-024/025 (etiquetado) · APUEST-037, CONOC-010 (vacunación) · SALUD-014 (HbA1c) · SALUD-016 (obesidad regional) · SALUD-024/025 (actividad física) · SALUD-031/032/037 · CONOC-018 (CAF 2012) | — | NO-CORRIDO: módulo fuera de esta lista (etiquetado, menores, sangre, antropometría, actividad física, motivos) → sucesor `-2` |

Capital social y confianza (reports *Non-Family Social Capital* y *Confianza y
desconfianza*) se citan por dominio: ENBIARE CONFIANZA-*, CUENTA-APOYO-* son su medida;
*Religiosidad*: TIENE-RELIGION y ASISTE-SERVICIO-RELIGIOSO.
