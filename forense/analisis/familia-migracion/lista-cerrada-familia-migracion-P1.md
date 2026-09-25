# Lista cerrada P1 · ACTO GEN2-FAMILIA-CUIDADOS-Y-MIGRACION-PISOS-1

Congelada en el COMMIT-1 (25/sep/2026), **antes** de abrir un solo valor de microdato de
ENADID, ENASIC o Pew. Fuente de cada reactivo: el texto de la pregunta (A.15), leído del
descriptor (FD) de cada ola (ENADID 2009 PDF, 2014 y 2018 XLSX; ENASIC 2022 XLSX) y de las
etiquetas de variable y valor de los `.sav` de Pew (`pyreadstat`, `metadataonly=True`). De
las bases sólo se leyó la cabecera (nombres de columna) y, en DBF, el descriptor de campos.
Informe de estructura: `estructura-instrumentos.md` (esta carpeta). Cambiar esta lista
después del COMMIT-1 es PARO (d).

Afirmaciones del mapa que la motivan (`canon/mapa-dominios-v1_0.tsv`, dominios
FAMILIA_CUIDADOS, PAREJA, MIGRACION; VEJEZ no existe como dominio en el mapa: sus filas
viven en FAMILIA_CUIDADOS): FAM-025 (hogares ampliados/unipersonales), FAM-042 (salida del
hogar), VEJEZ-002 (peso de 60+), VEJEZ-005/006/037 (arreglos de residencia de 60+),
VEJEZ-008 (perfil del cuidador), FAM-007/008 (cuidado por sexo: ENUT, se cita),
PAREJA-032/041 (unión libre; migración y pareja), MIGR-009/011/013 (migración en ENADID).

## 1 · Olas abiertas y reservadas (E.6)

| instrumento | olas en corpus (microdato) | reservada | se abre aquí |
|---|---|---|---|
| ENADID | 1992, 1997, 2009, 2014, 2018, 2023 | **2023** para toda conducta de esta lista (ids `enadid2023_*`: no son input) | 2009, 2014, 2018 |
| ENASIC | 2022 | — (una sola ola: no hay historia que reservar; se abre y se declara) | 2022 |
| Pew GAS | Spring 2013, 2015, 2017, 2018, 2023, 2024, 2025 | **2025** (`pew_gas_spring2025`: no es input) | 2013, 2015, 2017, 2018, 2023 (2024 no trae ninguna pregunta de la lista) |
| EMIF | — | — | NO-OBTENIDO (ver §4) |

**ENADID 2023 ya fue abierta** por actos previos (`CALC-ENADID-0001`, `CALC-ENADID2023-UNION-SEXO-EDAD-0001..0004`):
lo que esos CALC derivaron se CITA, no se re-mide ni se reserva (un cruce visto no se
desve). Las conductas de esta lista no las derivó ninguno de ellos (unión por sexo y edad
no es «unida» por tamaño de hogar ni condición de hogar), y quedan reservadas en 2023 para
el sucesor que las evalúe prospectivamente (INTERPRETACIÓN-DECLARADA: E.6 pide reservar la
ola más reciente; la más reciente ya tuvo aperturas parciales; se reserva lo no derivado).

**ENADID 1992 y 1997 quedan fuera de la serie (declarado):** otro esquema de tablas
(`VIVIENDAS_HOGARES`, `DATOS_GRALES`; `E97VHO`, `E97DGE`), sin estrato/UPM de diseño con
nombre estándar en el descriptor de campos y sin variables derivadas de clase de hogar;
armonizarlas es un acto propio → NO-CORRIDO. 2009–2014–2018 comparten `CLS_HOG`,
`SEXO_JEFE`/`SEXO_JEF`, parentesco de un dígito y situación conyugal, y bastan para el IC
calibrado de persistencia (≥ 3 olas).

## 2 · Conductas, por instrumento

### ENADID 2009 / 2014 / 2018 → `CALC-ENADID-FAMILIA-HOGARES-0001`

Diseño: factor `FAC_VIV` (vivienda; el FD no trae factor de hogar ni de persona para la
tabla sociodemográfica), estrato `ESTDIS` (2009) / `EST_DIS`, UPM `UPM_DIS`. Personas:
diseño, tamaño y clase de hogar tomados de su hogar por llave (`LLAVE_HOG`; 2009:
`CONTROL`+`VIV_SEL`+`HOGAR`, la tabla de personas 2009 no trae diseño).

| conducta | unidad · universo | texto (A.15) | 1 | 0 | fuera |
|---|---|---|---|---|---|
| HOGAR-UNIPERSONAL | hogar | `CLS_HOG` «Clase de hogar» | 5 Unipersonal | 1,2,3,4,6 | 9 |
| HOGAR-NUCLEAR | hogar | `CLS_HOG` | 1 Nuclear | 2–6 | 9 |
| HOGAR-AMPLIADO | hogar | `CLS_HOG` | 2 Ampliado | 1,3–6 | 9 |
| HOGAR-JEFATURA-FEMENINA | hogar | «Sexo de la (el) jefa(e) del hogar» | 2 | 1 | otro |
| HOGAR-CON-MIGRANTE-INTERNACIONAL-5A | hogar | `MIG_HOG` (2014) / `MIGRA_HO` (2018) «Condición de migración internacional en el hogar» (P4.1: últimos cinco años) | 1 Con migrantes | 2 | 9. **2009 fuera:** `MIGRA_HO` 2009 es «migración a EUA», otro estimando |
| PERSONA-60MAS | persona residente | «¿Cuántos años cumplidos tiene…?» | ≥ 60 | 0–59 | 999 |
| AM60-VIVE-SOLO | persona 60+ | total de integrantes del hogar (`PERS_HOG` 2009, `TOT_PER` 2014, `P2_5` 2018) | = 1 | ≥ 2 | sin dato |
| AM60-EN-HOGAR-AMPLIADO | persona 60+ | `CLS_HOG` de su hogar | 2 | 1,3–6 | 9 |
| JOVEN-25-34-HIJO-DEL-JEFE | persona 25–34 | «¿Qué es (NOMBRE) de la (del) jefa(e)?» (`PAREN`; 2009 `PAR_AGRUP`) | 3 Hija(o) | 1,2,4–8 | 9 |
| PERSONA-15MAS-UNIDA | persona 15+ | situación conyugal (`P3_19` 2009, `P3_20` 2014, `P3_21` 2018) | unión libre o casada(o) | separada(o), divorciada(o), viuda(o), soltera(o) | 9, blanco |
| UNIDO-15MAS-EN-UNION-LIBRE | persona 15+ unida | misma | unión libre | casada(o) | los demás |

Códigos de situación conyugal: 2014/2018 1 UL, 2 separada UL, 3 separada matrimonio, 4
divorciada, 5 viuda, 6 casada, 7 soltera; 2009 1 UL, 2 separada, 3 divorciada, 4 viuda, 5
casada, 6 soltera.

### ENASIC 2022 → `CALC-ENASIC-CUIDADOS-VEJEZ-0001`

Diseño: `FAC_HOG`, `EST_DIS`, `UPM_DIS` (THOGAR); personas (TCSDEMPO) con el diseño de su
hogar por `LLAVEHOG`. ENASIC no publica tamaño de localidad en ninguna tabla (FD
recorrido: TVIVIENDA, THOGAR, TCSDemPO, TPOB_CUI, THOG_UNIP, TPER_ELE; sin `TLOC`/`TAM_LOC`/
«localidad» como variable) → eje TLOC NO-CONSTRUIBLE.

| conducta | unidad · universo | texto (A.15) | 1 | 0 | fuera |
|---|---|---|---|---|---|
| HOGAR-NECESITA-CUIDADOS | hogar | `HN_C` «Hogar que necesita cuidados» | 1 | 2 | otro |
| HOGAR-CON-60MAS-QUE-NECESITA-CUIDADOS | hogar | `HN_C60MA` | 1 | 2 | otro |
| AM60-CUIDADO-POR-ALGUIEN-DEL-HOGAR | persona 60+ | 4.42 «La semana pasada a (NOMBRE) ¿alguien del hogar le cuidó, ayudó, acompañó…?» | 1 | 2 | 3 hogar unipersonal, blanco |
| AM60-CUIDADOR-PRINCIPAL-MUJER | persona 60+ con cuidador principal en el hogar (4.44 = 01–07) | 4.44 «¿quién es la cuidadora o cuidador principal…?» → sexo del renglón | 2 Mujer | 1 Hombre | renglón sin pareo |
| AM60-CUIDADOR-PRINCIPAL-HIJA | ídem, con 4.44a 01–11 | 4.44a «El (la) cuidador(a) principal ¿qué es de (NOMBRE)?» | 04 Hija | 01–03, 05–11 | blanco |
| AM60-CUIDADOR-PRINCIPAL-CONYUGE | ídem | 4.44a | 01 Cónyuge o pareja | 02–11 | blanco |
| AM60-CUIDADO-POR-PERSONA-DE-OTRO-HOGAR | persona 60+ | 4.45 «¿la(o) cuidó alguna persona de otro hogar?» | 1 | 2 | blanco |

### Pew Global Attitudes, México → `CALC-PEW-MIGRACION-MEX-0001`

Universo: adultos 18+ entrevistados en México (código de país de cada ola por la etiqueta
«Mexico»: 2013 = 25, 2015 = 21, 2017 = 20, 2018 = 15, 2023 = 24). Evidencia **(a)**: son
residentes de México entrevistados en México, no diáspora — la cláusula (b) de la firma
§3 v2.16 no aplica. Peso `weight`; PSU/estrato de México donde existen (2015 `PSU`/
`STRATUM_MEX`; 2017 y 2018 `PSU_MEX`/`STRATUM_MEX`).

| conducta | texto (A.15), por ola | 1 | 0 | fuera |
|---|---|---|---|---|
| IRIA-A-VIVIR-A-EEUU | «If at this moment, you had the means and opportunity to go to live in the United States, would you go?» 2013 Q151, 2015 Q127, 2017 y 2018 `mex_live_US` | 1 Yes | 2 No | 8, 9 |
| IRIA-SIN-AUTORIZACION-ENTRE-QUIENES-IRIAN | «And would you be inclined to go work and live in the U.S. without authorization?» 2013 Q152, 2015 Q128, 2017 `mex_wo_auth`; universo: 1 en la anterior | 1 | 2 | 8, 9 |
| EN-EEUU-SE-VIVE-MEJOR | «…do people from our country who move to the U.S. have a better life there, a worse life there, or is life neither better nor worse there?» 2013 Q54, 2015 Q101, 2023 `us_better_life` | 1 Better | 2 Worse, 3 Neither | «no conoce a nadie» (4 en 2013/2015, 8 en 2023), DK, Ref |
| CONTACTO-REGULAR-CON-PARIENTES-O-AMIGOS-EN-EL-EXTRANJERO | «Do you have friends or relatives who live in another country that you write to, telephone or visit regularly?» 2013 Q167, 2015 Q147, 2017 `friends_abroad` (split A). 2018 `friends_abroad_intouch` («stay in touch») es otro texto → fuera | 1 | 2 | 8, 9 |
| RECIBE-DINERO-DE-PARIENTES-EN-EL-EXTRANJERO | «Do you receive money from relatives living in another country regularly, once in a while, or don't you…?» 2013 Q169, 2017 y 2018 `receive_money` | 1, 2 | 3 | 8, 9 |
| BUENO-PARA-MEXICO-QUE-VIVAN-EN-EEUU | «Overall, would you say it is good for (survey country) or bad… that many of its citizens live in the U.S.?» 2013 Q153, 2018 `good_live_us` (2 olas: sin IC calibrado) | 1 Good | 2 Bad | 8, 9 |

## 3 · Ejes (uno a la vez; nunca cruces)

- ENADID hogar: SEXO-JEFE · EDAD-JEFE (12–29/30–44/45–59/60+) · ESCOLARIDAD-JEFE · TLOC.
- ENADID persona: SEXO · EDAD (0–14/15–29/30–44/45–59/60–74/75+) · ESCOLARIDAD · TLOC ·
  TAMANO-HOGAR (1/2/3–4/5+) · CONDICION-PAREJA (unido / no unido).
- ENASIC hogar: SEXO-JEFE · EDAD-JEFE · TAMANO-HOGAR. ENASIC persona 60+: SEXO · EDAD
  (60–69/70–79/80+) · ESCOLARIDAD · TAMANO-HOGAR · CONDICION-PAREJA (pareja corresidente:
  cónyuge del jefe, o jefe con cónyuge en el hogar; los demás «sin» — cota inferior,
  declarada).
- Pew: SEXO · EDAD (18–29/30–44/45–59/60+). Escolaridad, región y urbanidad cambian de
  variable y códigos por ola (`d_educ_mexico_*`, `Q180MEX`, `Q163MEX`; región sólo 2013,
  2015, 2023) → fuera, declarado.
- Formalidad, región y NSE (encargo §0): ENADID/ENASIC no traen formalidad del empleo en las
  tablas usadas; NSE (A4) no está construido para estas encuestas → fuera, declarado.

## 4 · Lo que la lista NO trae, y por qué

- **Fecundidad deseada vs observada** (ENADID módulo de la mujer): el texto del ideal de
  hijos cambia de número y nemónico por ola; armonizarlo exige un informe de estructura del
  módulo de la mujer por ola → DIFERIDO (NC).
- **Unión y primera unión por cohorte**: ya medido — `CALC-EDER2017-PRIMERA-UNION-SEXO-COHORTE-0001/0002`
  y `CALC-ENADID2023-UNION-SEXO-EDAD-0001..0004`; se citan, no se repiten.
- **División de cuidados por sexo (ENUT)**: ya medido — `CALC-ENUT-*` (7: `CALC-ENUT-0001`,
  `-SERIE-2009-2014-NUCLEO-0001`, `-SERIE-DICTAMEN-0001`, `CALC-ENUT2019-NUCLEO-EJES-0001`,
  `CALC-ENUT2024-DISTRIBUCION-HORAS-0001/0002`, `-NUCLEO-EJES-0001`,
  `-PARTICIPACION-INTENSIDAD-0001`); se citan.
- **EMIF (COLEF)**: NO OBTENIDO POR ESTE AGENTE EN 1 INTENTO (25/sep/2026): `https://www.colef.mx/emif/`
  responde 200 pero su HTML estático no trae enlaces a bases (menú por include);
  `/emif/bases.php`, `/basesdatos.php`, `/resultados.php` → 404; datos.gob.mx `package_search?q=emif`
  sin JSON. Receta de un minuto: abrir `https://www.colef.mx/emif/` en navegador, menú
  «Bases de datos», registrar el formulario de solicitud y bajar EMIF Norte/Sur
  (`.sav`/`.dta`) por flujo; registrar con `/adquiere`.

El primer resultado que produzca este procedimiento es el que se reporta.
