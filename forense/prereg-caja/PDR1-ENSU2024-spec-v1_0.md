# PDR1 · ENSU2024 · spec v1.0

ACTO GEN2-PISOS-DOMINIOS-Y-REGLAS-1, pieza P-ENSU2024 (CAJA). CALC: `CALC-PDR1-ENSU2024-0001`.
Universo de la pieza (tabla de apertura `forense/analisis/pisos-dominios-1/tabla-apertura-v1_0.tsv`,
`pieza` = P-ENSU2024): **una** afirmación, `ASTRA5-U0-SANC-007` (dominio SANCION_SOCIAL). Ninguna regla.
Todo es **RETROSPECTIVA**: ENSU 2024T1 ya fue abierta por GEN2-SEGURIDAD-ENSU-SERIE-1.

## 0 · Premisas verificadas y lectura de estructura (antes del COMMIT-1)

- `[EJECUTADO]` `ensu2024_bd_csv_zip` y `ensu2024_fd_pdf_zip`: `corpus_loader.motivo_reserva` → LIBRE.
  El payload trae los cuatro trimestres de 2024; **sólo** se lee `ensu_bd_marzo_2024_csv.zip!ENSU_CB_0324.csv`
  (2024T1, el trimestre que cita la afirmación). Ninguna ENSU 2025/2026 es input.
- `[EJECUTADO]` Lectura de **estructura** (no dato): cabecera de columnas de `ENSU_CB_0324.csv` (contiene
  `CD, SEXO, EDAD, BP1_5_1, FAC_SEL, UPM_DIS, EST_DIS`) y el descriptor de archivos
  `ensu_fd_2024/ensu_fd_2024_marzo.pdf` (dentro de `ensu2024_fd_pdf_zip`). No se contó ni tabuló ninguna fila.
- `[LEÍDO]` Afirmación (`canon/mapa-dominios-v1_1.tsv`, fila ASTRA5-U0-SANC-007, `texto_vigente`): «según la ENSU
  del primer trimestre de 2024 (INEGI), 47.4% de la población de 18 años y más manifestó evitar llevar cosas de
  valor —joyas, dinero o tarjetas de crédito— por temor a sufrir algún delito».
- `[LEÍDO]` E.5 — **ya sellado, se cita**: `CALC-ENSU-PISOS-0001` (y `CALC-ENSU-SERIE-0001`, idéntico) midió
  `C09-HABITO-OBJETOS-VALOR` 2024T1 con numerador código 1 y **denominador 1,2,3,9** (incluye «No aplica» y
  NS/NR; `lista-cerrada-P1.md` §3), ids `RESULT-ENSU-PISOS-C09-HABITO-OBJETOS-VALOR-2024T1-TOTAL-TODOS-{P,IC-LO,IC-HI,N}`
  y sus segmentos SEXO/EDAD; la nota de cierre de ese acto lo dictaminó MATIZA contra 47.4 y dejó la NC
  `NC-260926-GEN2-SEGURIDAD-ENSU-SERIE-1-5916-03` (ABIERTA, SIN-ASIGNAR): «hábitos C09–C12 con el denominador
  del comunicado (sin "No aplica")… re-medir es spec nueva». **Este CALC es esa spec nueva para C09 2024T1**: el
  estimando principal (denominador sin «No aplica» ni NS/NR) no está sellado; el del universo 1,2,3,9 sí, y aquí
  sólo se recalcula como **oro** (debe reproducir el punto sellado), no como resultado nuevo.
- `[EJECUTADO]` `tools/ya_medido.py ASTRA5-U0-SANC-007` → NUNCA-MEDIDA (falso negativo conocido de la
  herramienta frente a la lista cerrada del acto ENSU; se declara).

## 1 · Reactivo, por texto (A.15)

Descriptor `ensu_fd_2024_marzo.pdf`, tabla CB (cuestionario de la persona seleccionada de 18+):

- **p. 24**, pregunta 1.5, variable 43: «1.5. En este mismo periodo de tres meses, por temor a sufrir algún delito
  (robo, asalto, secuestro, entre otros), ¿usted cambió sus hábitos respecto a … llevar cosas de valor como
  joyas, dinero o tarjetas de crédito?» Códigos: **1 Sí · 2 No · 3 No aplica · 9 No sabe / no responde**.
  (Nemónico en el archivo: `BP1_5_1`, sólo como localizador.)
- **p. 22**: SEXO (1 Hombre, 2 Mujer), EDAD (18,…,96 años).
- **p. 36**: `FAC_SEL` («ponderador que se utiliza» para la persona de 18+), `UPM_DIS` (unidad primaria de muestreo
  de diseño), `EST_DIS` (estrato de diseño). `CD` = ciudad (dominio de estudio).

Nota de contenido: el reactivo es «cambió sus hábitos respecto a llevar cosas de valor»; la afirmación dice
«evitar llevar». Se toma «Sí» = dejó de/evita llevar (lectura INEGI habitual del reactivo); se declara.

## 2 · Universo, unidad, escala, ponderador, diseño

- **Unidad:** persona seleccionada de 18+ años. **Escala:** proporción ponderada en [0,1].
- **Universo:** filas de `ENSU_CB_0324` con `FAC_SEL` > 0 y `EST_DIS`, `UPM_DIS` no vacíos (mismo marco que
  CALC-ENSU-PISOS-0001). Ciudades de interés ENSU (urbano), **no** México entero ni rural.
- **Ponderador:** `FAC_SEL`, sin normalizar. **Agregador (E.1):** razón de sumas ponderadas Σw·1{sí}/Σw·1{denominador}.
- **Diseño:** estrato = `CD`+`EST_DIS`; UPM = estrato+`UPM_DIS` (mismo que el CALC sellado).

## 3 · Estimandos

| sufijo | numerador | denominador | celdas |
|---|---|---|---|
| **PRINCIPAL** (manda) | código 1 | códigos 1,2 (NA y NS/NR fuera, regla del procedimiento) | TOTAL; SEXO (HOMBRE, MUJER); EDAD (18-29, 30-44, 45-59, 60-MAS) |
| CON-NSNR (sensibilidad) | 1 | 1,2,9 (sólo NA fuera) | TOTAL |
| ORO (control) | 1 | 1,2,3,9 | TOTAL — debe igualar el punto sellado `RESULT-ENSU-PISOS-C09-HABITO-OBJETOS-VALOR-2024T1-TOTAL-TODOS-P` (|Δ| ≤ 1e-10) |

Descriptivos: proporción ponderada de «No aplica» (3) y de NS/NR (9) sobre 1,2,3,9; n de códigos fuera de lista.
Segmentación mínima (§3): sexo y edad. Tamaño de localidad / rural-urbano: **NO-CONSTRUIBLE** en ENSU (sólo
ciudades); escolaridad, NSE: no están en CB. Un eje a la vez, sin cruces.

## 4 · IC

Bootstrap de UPM con reposición dentro de estrato (n_h de n_h), **2000** réplicas, semilla **42**
(`numpy.PCG64`); estrato con una sola UPM se remuestrea a sí mismo (varianza cero; se cuenta y se reporta).
Percentiles 2.5/97.5. Sin IC si alguna réplica deja denominador cero en la celda (contrato conservador: null).

## 5 · Pre-registro de falsación B-bis (afirmación ASTRA5-U0-SANC-007, cifra 47.4 % = 0.474)

Sobre el estimando **PRINCIPAL**, TOTAL:
- **CONFIRMA**: 0.474 ∈ [IC-LO, IC-HI].
- **MATIZA**: 0.474 fuera del IC y |p − 0.474| ≤ **0.03** (3 pp; mismo umbral que ENSU-SERIE §8.3, fijado antes).
- **ROMPE**: 0.474 fuera del IC y |p − 0.474| > 0.03.
- **NO-CONSTRUIBLE**: punto o IC null.
Las tres filas son excluyentes. **Manda PRINCIPAL**; CON-NSNR y ORO llevan el mismo dictamen mecánico sólo como
sensibilidad (se reportan, no deciden). El medidor emite el dictamen (`RESULT-PDR1-ENSU2024-SANC007-DICTAMEN`).
Lo que no cambia con ningún resultado: el reactivo mide conducta defensiva ante el **delito**, no ocultamiento de
riqueza por **envidia** (límite inferencial del mapa); un CONFIRMA no respalda el mecanismo de nivelación.

## 6 · Controles

Sintético (`tests/test_pdr1_ensu2024.py`): payload con zip externo + zips trimestrales, CB con BOM, comillas y
fin de línea `\r` solo, miembro de junio basura que no debe leerse; ids exactos por `corrida0._valida_outputs`;
rama degenerada (sin «No»); dictamen mecánico. Oro: estimando ORO contra el punto sellado (se contrasta en el
fragmento de dictámenes). No hay ejecución diagnóstica sobre el dato real.

## 7 · Módulo de auditoría v2.16

Contadores que mueve: ninguno por sí mismo (no adopta; propone piso del dominio SANCION_SOCIAL). **Unidad:**
persona 18+ (no hogar ni delito). **Escala:** proporción. **RETROSPECTIVA** (ola vista); ninguna cifra PROSPECTIVA.
**Segmentación:** sexo, edad; urbano-sólo. **¿Incentivo o psicología?** Cambiar hábitos por miedo al delito es
adaptación racional a la violencia (estructura), no rasgo cultural; tampoco es «sanción social horizontal».
**¿Clase media urbana?** Sí: ENSU cubre ciudades; no dice nada del México rural/indígena, y sin NSE no separa
clase. **Peligroso leído simplista:** «la mitad de los mexicanos esconde su riqueza por envidia» — el reactivo no
mide envidia ni ocultamiento de riqueza; y el denominador (con/sin «No aplica») mueve la cifra: se reportan los
tres. Ninguna cifra de esta spec está escrita a mano salvo la de la afirmación (0.474, citada del mapa) y el umbral.

el primer resultado que produzca este procedimiento es el que se reporta.
