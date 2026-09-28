# PDR1 · ENCUCI2020 · spec v1.0 · CALC-PDR1-ENCUCI2020-0001

ACTO GEN2-PISOS-DOMINIOS-Y-REGLAS-1, pieza P-ENCUCI2020 (P2/P3). Entorno CAJA.
Rótulo temporal: **RETROSPECTIVA** (ENCUCI 2020 es ola única ya vista; todo lo que
aquí se mide es piso descriptivo retrospectivo, no predicción). No adopta: adopción
por merge de mesa.

## 0 · Universo de la pieza y premisas

Universo exacto = filas `pieza=P-ENCUCI2020` de
`forense/analisis/pisos-dominios-1/tabla-apertura-v1_0.tsv`: afirmaciones
ASTRA5-U0-AUTOR-001, -002, -003, -010, -030, -031 (dominio AUTORIDAD; texto y
componente contrastable en `canon/mapa-dominios-v1_1.tsv`) y la regla
RG-67c84a2224 (dominio POLITICA; `canon/reglas-contrastadas-v1_0.tsv`). Nada más se mide.

- `[EJECUTADO]` reserva por id: `encuci2020_bd_dbf` → LIBRE (`corpus_loader.motivo_reserva`).
- `[EJECUTADO]` payload `data/raw/BD_ENCUCI2020_dbf.zip`, sha256
  `0414fd59e2afcc36294530687c721e8e86bd04e76ad95bfce4b7b2e70853f283` (manifiesto).
- `[LECTURA DE ESTRUCTURA, permitida antes del COMMIT-1]` (a) el descriptor
  `encuci2020_fd_pdf` (FD_ENCUCI2020.pdf, sha256 `6cd6f747…5638`) convertido a texto
  con `pdftotext -layout`; (b) la **cabecera de columnas** (descriptores de campo) de
  los DBF `ENCUCI_2020_SEC_4_5.dbf`, `ENCUCI_2020_SEC_6_7_8.dbf`, `ENCUCI_2020_SD.dbf`
  (nombres y tipos; ningún registro leído, ningún conteo). Resultado: SEC_4_5 trae
  `ID_PER, AP4_9_1(N), AP4_9_4(N), AP4_13(C), AP5_1_4(C), AP5_11(N), FAC_SEL, DOMINIO,
  UPM_DIS, EST_DIS`; SEC_6_7_8 trae `ID_PER, AP6_9, AP6_10, AP6_11, AP7_15, FAC_SEL,
  DOMINIO, UPM_DIS, EST_DIS`; SD trae `ID_PER, SEXO, EDAD`.
- `[LEÍDO]` Contaminación declarada: esta sesión leyó antes de congelar las cifras
  citadas por las afirmaciones (77.5 %, 88.7 %, 13.8 %, 62.1 %, 27.7 %/49.5 %, 33 %) y
  los RESULT sellados de CALC-ARBITRO-MARGINALES-2-ENCUCI2020-0001 (derecho entre
  beneficiarios 54.0 % [52.2, 55.8]; no-condicionados 54.1 % [52.2, 55.9]; brechas
  Morena por rama de secreto). No leyó ningún valor de AP4_9, AP4_13, AP5_1_4, AP5_11
  ni el cruce AP6_9×AP7_15.
- `[EJECUTADO]` E.5: ningún CALC sellado en `data/corrida0/*` ni spec en
  `forense/prereg-caja/*` contiene AP4_9_1, AP4_9_4, AP4_13, AP5_1_4 ni AP5_11
  (búsqueda de cadena en todos los archivos). CALC-ENCUCI-0001 mide AP5_16/17/18 y
  AP4_3_2, no AP5_1_4. AP5_1_2 (conocidos, 62.1 %) está en la nota C-06b/ADR-64, no en
  un CALC; AUTOR-003 sólo contrata AP5_1_4, así que no se re-mide AP5_1_2.
  `tools/ya_medido.py RG-67c84a2224` → NUNCA-MEDIDA.
- E.5 para la regla: CALC-ARBITRO-MARGINALES-2-ENCUCI2020-0001 selló
  `RESULT-ARB2-ENCUCI-ENTITLEMENT` (derecho = AP6_9=2 por beneficiario y, anidado, por
  AP6_11) y `RESULT-ARB2-ENCUCI-AGENCIA-SECRETO` (preferencia MORENA por beneficiario
  dentro de cada rama de AP7_15). Se **citan**, no se re-miden. Falta la pieza que la
  regla exige en su unidad: la proporción **conjunta** derecho × voto-secreto en la
  misma persona beneficiaria; ésa se mide aquí (con sus dos marginales en el MISMO
  universo sólo para que la conjunta sea interpretable; no sustituyen a lo sellado).

## 1 · Común a todas las celdas

- **Unidad**: persona seleccionada de 15 años o más, vivienda particular, nacional
  (ENCUCI 2020). Escala: nacional con segmentación.
- **Ponderador**: `FAC_SEL` «Ponderador que se utiliza para estimar resultados de las
  preguntas que se refieren al informante seleccionado» (FD pdf p.17 [impresa 14] y
  p.35 [impresa 32]); leído tal cual, sin normalizar; filas con FAC_SEL no finito o ≤0 salen.
- **Diseño**: `EST_DIS` (estrato de diseño, carácter 001-999) y `UPM_DIS` (UPM de
  diseño, carácter 7), FD pp.17 y 35; llaves de texto opacas, jamás convertidas a entero.
- **Estimando por celda**: proporción ponderada razón Σw·num / Σw·den.
- **Agregador (E.1)**: razón de sumas ponderadas sobre el marco completo de la tabla
  (no promedio de promedios de segmentos).
- **IC95**: bootstrap de UPM_DIS con reemplazo dentro de EST_DIS sobre el **marco
  completo** de cada tabla (SEC_4_5 para AUTOR, SEC_6_7_8 para la regla; dos
  instancias independientes con la misma semilla), **2000 réplicas**, semilla 42
  (numpy PCG64), percentiles 2.5/97.5; estrato con una sola UPM: autorremuestreo
  (varianza cero). Diferencias: percentiles de la serie réplica a réplica de la
  diferencia. Clase `Survey` copiada literal de la plantilla
  CALC-ARBITRO-MARGINALES-2-ENCUCI2020-0001.
- **Filtros**: 9 (No sabe/no responde), blanco y cualquier código fuera de rango
  salen del denominador; nunca se imputan.
- **Segmentación mínima (§3)**: cada celda se reporta además por (i) sexo (SD.SEXO,
  FD p.13 [impresa 10] «3.5 (NOMBRE) es hombre / es mujer», 1=Hombre 2=Mujer), (ii) grupo de
  edad (SD.EDAD «3.6 ¿Cuántos años cumplidos tiene?» 15-29, 30-44, 45-59, 60+; 97/98/99
  = edad no especificada → fuera del segmento, sigue en el total), (iii) DOMINIO de la
  tabla (FD p.17: U=Urbano, C=Complemento urbano, R=Rural — es el proxy de tamaño de
  localidad que el instrumento publica). Unión con SD por `ID_PER` (clave
  UPM+VIV_SEL+renglón, FD p.11); se reporta el número de filas unidas
  (`…-JOIN-SD-N`) como guardia: si fuera 0 los segmentos sexo/edad quedan vacíos y se
  dice, sin tocar el total.

## 2 · Celdas por afirmación y regla (códigos por texto del FD)

Páginas: «pdf p.N» = página del PDF; entre corchetes la impresa.

### AUTOR-001 — «77.5 % quiere un líder político fuerte»
Pregunta 4.9 «¿Qué tan de acuerdo o en desacuerdo está con las siguientes frases?
Para gobernar un país se necesita tener… 1. un gobierno encabezado por un líder
político fuerte» (pdf p.23 [20], `AP4_9_1`): 1 Muy de acuerdo, 2 Algo de acuerdo,
3 Algo en desacuerdo, 4 Muy en desacuerdo, 9 No sabe/no responde.
Denominador: código ∈ {1,2,3,4}. Numerador: {1,2}. Id `…-AUTOR001-LIDER-FUERTE-ACUERDO`.

### AUTOR-002 — «88.7 % dice que gobernar requiere participación de todos»
Misma pregunta 4.9, inciso «4. un gobierno donde todos participen en la toma de
decisiones» (pdf p.23 [20], `AP4_9_4`), mismos códigos. Den {1..4}, num {1,2}.
Id `…-AUTOR002-PARTICIPAN-TODOS-ACUERDO`.

### AUTOR-003 — «13.8 % confía en servidores públicos»
Pregunta 5.1 «En una escala de cero a diez, como en la escuela, donde cero es nada y
diez es completamente, en general ¿cuánto confía en… 4. los servidores públicos o
empleados de gobierno?» (pdf pp.24-25 [21-22], `AP5_1_4`, carácter de dos dígitos):
00 Nada … 10 Completamente, 99 No sabe/no responde. Den: texto ∈ {00..10}. Num:
{08,09,10} (corte alto ≥8 prerregistrado en el mapa, mismo que CAPSOC-003).
Id `…-AUTOR003-CONFIA-SERVIDORES-8A10`.

### AUTOR-010 — «doble discurso» simultáneo (cruce en la misma persona)
AP4_9_1 y AP4_9_4 (pdf p.23 [20]). Den: ambas ∈ {1..4}. (a) conjunta = ambas ∈ {1,2}
(`…-AUTOR010-CONJUNTA-LIDER-Y-PARTICIPACION`); (b) condicional = AP4_9_4 ∈ {1,2} entre
quienes AP4_9_1 ∈ {1,2} (`…-AUTOR010-PARTICIPACION-DADO-LIDER`). Manda (b): es el
falsador del mapa («<50 % de quienes marcan AP4_9_1=1/2 también marcan AP4_9_4=1/2»).

### AUTOR-030 — «27.7 % obedecer siempre leyes injustas; 49.5 % pedir cambio»
Pregunta 5.11 «En su opinión, ¿cuál de las siguientes frases se acerca más a lo que
usted piensa?» (pdf p.33 [30], `AP5_11`): 1 Las personas deben obedecer siempre las
leyes aunque sean injustas; 2 Las personas pueden pedir que cambien las leyes si
estas no les parecen; 3 Las personas pueden desobedecer la ley si esta es injusta;
4 Ninguna; 9 No sabe/no responde. Den {1,2,3,4}; se reporta la distribución completa
(`…-AUTOR030-AP5_11-{OBEDECER-SIEMPRE,PEDIR-CAMBIO,DESOBEDECER-INJUSTA,NINGUNA}`) y la
diferencia cat2−cat1 con IC (`…-AUTOR030-DIF-PEDIR-MENOS-OBEDECER`).

### AUTOR-031 — «33 % acepta formas más autoritarias de gobierno»
Pregunta 4.13 «En su opinión, ¿de las siguientes frases cuál es preferible para
gobernar al país?» (pdf p.24 [21], `AP4_13`): 1 La democracia es preferible a
cualquier otra forma de gobierno; 2 En algunas circunstancias, un gobierno no
democrático puede ser mejor; 3 Da lo mismo un régimen democrático que uno no
democrático; 4 Ninguna; 9 No sabe/no responde; b blanco (pase: no aplica). Den
{1,2,3,4}; num {2,3} (`…-AUTOR031-NO-DEMOCRATICO-O-INDIFERENTE`); además cat 1
(`…-AUTOR031-DEMOCRACIA-PREFERIBLE`) y diferencia cat1−(2+3) con IC.

### RG-67c84a2224 — transferencia universal no condicionada → derecho pero autonomía de voto
Unidad de la regla (fijada aquí; la tabla de reglas la deja «—»): **persona
beneficiaria de programa social a quien no se pidió nada a cambio**, es decir
- 6.10 «En los últimos doce meses… ¿usted es o ha sido beneficiario de algún
  programa de ayuda social del gobierno…?» (pdf p.41 [38], `AP6_10`) = 1 Sí, y
- 6.11 «¿A usted le pidieron algo, como dinero, documentos personales, favores o que
  votara por algún partido, a cambio de entrar o permanecer en algún programa de
  ayuda social?» (pdf p.41-42 [38], `AP6_11`) = 2 No (proxy de «no condicionada»;
  el instrumento no identifica si el programa es universal).
- Den adicional: 6.9 (pdf p.41 [38], `AP6_9`) ∈ {1 «Los programas sociales son una
  ayuda que da el gobierno», 2 «…son un derecho de los ciudadanos»} y 7.15 «¿Usted
  cree que su voto es secreto o se puede descubrir por quién ha votado?» (pdf p.48
  [45], `AP7_15`) ∈ {1 El voto es secreto, 2 Se puede descubrir}.
- Celdas: conjunta derecho(AP6_9=2) ∧ secreto(AP7_15=1)
  (`…-RG67C8-CONJUNTA-DERECHO-Y-SECRETO`) — **manda**; marginales en el mismo universo
  `…-RG67C8-DERECHO`, `…-RG67C8-SECRETO`.
- Declarado: «autonomía de voto» no se observa; AP7_15=1 (creer que el voto es
  secreto) es su condición necesaria observable, no la autonomía. «Gratitud al
  líder» no tiene reactivo; «ayuda» (AP6_9=1) no se trata como gratitud.

## 3 · Pre-registro de falsación B-bis (fijado antes del dato)

Orden de evaluación, idéntico en todas las filas: **ROMPE se evalúa primero; si no,
CONFIRMA; si no, MATIZA.** «IC» = IC95 de la celda que manda.

| id | valor a contrastar | CONFIRMA | MATIZA | ROMPE |
|---|---|---|---|---|
| AUTOR-001 | 0.775 | 0.775 ∈ IC | resto | IC_sup < 0.50 (el acuerdo no es mayoría: orden contrario) |
| AUTOR-002 | 0.887 | 0.887 ∈ IC | resto | IC_sup < 0.50 |
| AUTOR-003 | 0.138 | 0.138 ∈ IC | resto | IC_inf > 0.50 (confiar alto sería mayoría: orden contrario) |
| AUTOR-010 | condicional ≥ 0.50 (sin cifra; tesis de co-ocurrencia) | IC_inf ≥ 0.50 | IC contiene 0.50 | IC_sup < 0.50 |
| AUTOR-030 | 0.277 (cat1) y 0.495 (cat2) | 0.277 ∈ IC(cat1) **y** 0.495 ∈ IC(cat2) | resto | IC_sup de (cat2−cat1) < 0 (orden invertido: obedecer > pedir cambio) |
| AUTOR-031 | 0.33 (cat 2+3) | 0.33 ∈ IC | resto | IC_sup de (cat1−(2+3)) < 0 (no-democrático/indiferente supera a democracia: orden contrario) |
| RG-67c84a2224 | tesis: el beneficiario típico no condicionado vive el programa como derecho **y** cree su voto secreto | IC_inf(conjunta) ≥ 0.50 | resto (ninguna de las ramas de ROMPE ni CONFIRMA) | IC_sup(DERECHO) < 0.50 **o** IC_sup(SECRETO) < 0.50 (una de las dos patas no es mayoría) |

Para la regla, el dictamen se escribe en la unidad fijada en §2 (proporción de
personas beneficiarias no condicionadas). Si la conjunta sale NO-ESTIMABLE, el
dictamen es INCOMPARABLE. Para una afirmación con celda NO-ESTIMABLE: NO-CONSTRUIBLE.
Los segmentos son descriptivos; no deciden el dictamen (lo decide el total nacional),
pero se reportan y un segmento con signo contrario se anota en `detalle`.
Lo sellado en ARB2 se cita en `detalle` de la regla: derecho entre beneficiarios
54.0 % [52.2, 55.8]; brecha MORENA beneficiario−no dentro de rama SECRETO +6.4 pp
[3.9, 8.9] — asociación de preferencia, no prueba de pérdida de autonomía.

## 4 · RESULT declarados

Ids en `data/corrida0/CALC-PDR1-ENCUCI2020-0001/spec.yaml`, derivados de la salida
del medidor sobre una corrida sintética (`tests/test_pdr1_encuci2020.py`). Por cada
celda: punto, `-IC95-INF`, `-IC95-SUP` (flotantes, NO-ESTIMABLE permitido), `-N`
(entero, n no ponderado del denominador), `-SEGMENTOS` (JSON texto: sexo, edad,
dominio con n/masa/p/IC). Guardias: `SEC45-N-FILAS`, `SEC45-N-UPM`,
`SEC45-N-ESTRATOS`, `SEC45-JOIN-SD-N`, `SEC678-N-FILAS`, `SEC678-JOIN-SD-N`, `METODO-IC`.

## 5 · Módulo de auditoría v2.16

- **Unidad**: persona 15+ seleccionada; en la regla, persona beneficiaria no condicionada.
- **Escala**: nacional, con sexo × edad × U/C/R (no se trata a México como bloque).
- **RETROSPECTIVA**: sí; ola única 2020, ya vista (y año de pandemia: campo
  ago-2020). No se generaliza a 2024+.
- **¿Incentivo o psicología?**: AUTOR-001..031 son actitudes declaradas (psicología
  expresada), no conducta; la regla es de incentivo (ausencia de monitoreo) pero lo
  medido es percepción (derecho, secreto), no voto observado.
- **¿Clase media urbana?**: no; muestra probabilística nacional con dominio rural;
  el segmento R se reporta aparte.
- **¿Qué sería peligroso leído simplista?**: leer «77 % quiere un líder fuerte» como
  autoritarismo o apoyo a un personaje (el reactivo no lo dice); leer la coexistencia
  con «participación de todos» como incoherencia individual sin el cruce; leer la
  conjunta derecho×secreto como prueba de autonomía de voto (sólo es su condición
  necesaria declarada) o como ausencia de clientelismo.

el primer resultado que produzca este procedimiento es el que se reporta.
