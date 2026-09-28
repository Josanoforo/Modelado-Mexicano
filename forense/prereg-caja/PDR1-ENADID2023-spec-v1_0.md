# PDR1-ENADID2023 · spec v1.0 (pieza P-ENADID2023 del acto GEN2-PISOS-DOMINIOS-Y-REGLAS-1)

**RETROSPECTIVA** (ENADID 2023 ya abierta por CALC-ENADID2023-UNION-SEXO-EDAD-0002..0004, sellados).
CALC: `data/corrida0/CALC-PDR1-ENADID2023-0001`. Entorno: CAJA. No adopta; adopción por merge de mesa.

## 0 · Reserva (E.6) y lectura previa declarada
- `motivo_reserva('enadid2023_base_datos_csv')` = LIBRE; P1 (`tabla-apertura-v1_0.tsv`) = LIBRE/MEDIR.
- No hay en el manifiesto ola ENADID posterior a 2023. Sí es la más reciente, pero **ya fue abierta**:
  `enadid2023_base_datos_csv` figura en `data/corrida0/CALC-ENADID2023-UNION-SEXO-EDAD-000{1..4}/spec.yaml`,
  con `sello.json` en 0002, 0003 y 0004. Las specs COLA-ENADID-PISOS y FAMILIA-ENADID-PISOS la declararon
  reservada «para estas conductas» (alcance acotado a esos actos, anterior a los UNION sellados).
- Lectura de estructura antes del COMMIT-1 (permitida): FD `fd_enadid23.xlsx` hoja TSDEM; cuestionario
  `hogar_enadid23.pdf`; cabecera de columnas y fin de línea de `TSDEM.csv` (CRLF, sin BOM, cabecera en
  minúsculas entre comillas). No se contó, tabuló ni calculó nada sobre el microdato.

## 1 · Afirmación (ASTRA5-U0-TEC-010, dominio RURAL_INDIGENA)
«El analfabetismo indígena es 19% frente a 2.8% de población no indígena y 24.2% entre mujeres indígenas,
atribuido a ENADID 2023.» Componente contrastable (canon/mapa-dominios-v1_1.tsv): proporción ponderada
P3_23=2 entre residentes habituales de 15+ por P3_12=1 frente a P3_12=2 y, entre autoadscritas, SEXO=2.
`tools/ya_medido.py ASTRA5-U0-TEC-010` → NUNCA-MEDIDA (nada que citar por E.5).

## 2 · Reactivos por texto (A.15)
- **P3.12** (cuestionario hogar p.5, sección 3; FD TSDEM filas 153–154): «¿(NOMBRE) se considera indígena
  de acuerdo con sus tradiciones o costumbres?» 1 Sí · 2 No. Indígena = 1; no indígena = 2; cualquier otro
  valor/blanco fuera del denominador.
- **P3.23** (cuestionario p.6, bloque «PARA PERSONAS DE 5 AÑOS CUMPLIDOS O MÁS»; FD filas 323–325):
  «¿(NOMBRE) sabe leer y escribir un recado?» 1 Sí · 2 No · 9 No especificado. Numerador = 2; denominador
  = {1,2}; 9 fuera.
- **EDAD** (FD fila 60): «¿Cuántos años cumplidos tiene (NOMBRE)?» 000…109,120; 999 no especificada (fuera).
- **SEXO** (FD fila 58): 1 Hombre · 2 Mujer.
- **T_LOC_UR** (FD fila 412–413): 1 urbana (2 500+ hab.) · 2 rural (<2 500).
- **FAC_VIV** (FD fila 410): factor de expansión (se asigna a cada residente). **EST_DIS** (fila 502) estrato
  de diseño; **UPM_DIS** (fila 503) UPM de diseño. Mismos ponderador y diseño que los CALC ENADID2023 sellados.

## 3 · Estimando, universo, unidad, escala
- Unidad: persona residente habitual (registro de TSDEM). Escala: proporción en [0,1] (se lee ×100 = %).
- Universo: EDAD 15–120, SEXO∈{1,2}, P3_12∈{1,2}, P3_23∈{1,2}, FAC_VIV>0, EST_DIS/UPM_DIS no vacíos.
- Estimando por celda: p = Σ w·1[P3_23=2] / Σ w, w=FAC_VIV sin normalizar (razón de totales), dentro de
  cada grupo P3_12 × dominio. Brecha = p(indígena) − p(no indígena).
- Dominios (segmentación mínima §3): TOTAL; sexo H/M; edad 15_29, 30_44, 45_59, 60M (60+); URB/RUR; sexo×edad
  (8). Tamaño de localidad con valor fuera de {1,2} entra al total pero a ningún corte URB/RUR.
- Agregador (E.1): razón de totales ponderados; ningún promedio de proporciones.

## 4 · Inferencia
Bootstrap de diseño: 2000 réplicas; en cada estrato EST_DIS con m UPM se sortean m UPM con reemplazo
(multinomial), sobre el **marco completo** (todas las UPM con FAC_VIV>0, no sólo las del universo); estrato
con una sola UPM se autorremuestrea (varianza cero, se cuenta en N-ESTRATOS-SINGLETON). RNG numpy PCG64
semilla 42. IC95 = percentiles 2.5/97.5 de las réplicas (proporción y brecha, esta con réplicas pareadas).
Denominador nulo → null (NO-ESTIMABLE, `permite_no_estimable`).

## 5 · Salidas
167 RESULT escalares `RESULT-PDR1-ENADID2023-*` (ids derivados del medidor sobre corrida sintética):
N-MARCO, N-UNIVERSO, N-IND, N-NOIND, N-IND-M, N-ESTRATOS, N-UPM, N-ESTRATOS-SINGLETON, REPLICAS, SEMILLA;
por dominio D: P-IND-D, P-NOIND-D, BRECHA-D con -IC95INF/-IC95SUP; CIFRA19-EN-IC, CIFRA2_8-EN-IC,
CIFRA24_2-EN-IC (SI/NO/NA) y DICTAMEN-BBIS. Ningún texto >1024 bytes.

## 6 · Pre-registro de falsación B-bis (fijado antes del dato)
Unidad: proporción. Cifras de la afirmación: 0.19 (indígena 15+), 0.028 (no indígena 15+), 0.242 (mujeres
indígenas 15+).
- **ROMPE**: BRECHA-TOTAL ≤ 0 (orden contrario a la predicción indígena > no indígena).
- **CONFIRMA**: BRECHA-TOTAL > 0 **y** 0.19 ∈ IC95(P-IND-TOTAL) **y** 0.028 ∈ IC95(P-NOIND-TOTAL) **y**
  0.242 ∈ IC95(P-IND-M).
- **MATIZA**: BRECHA-TOTAL > 0 y al menos una de las tres cifras fuera de su IC95 (o IC no disponible).
- **NO-CONSTRUIBLE**: BRECHA-TOTAL no estimable.
- Precedencia: ROMPE manda sobre las demás; luego CONFIRMA; si no, MATIZA. El medidor aplica esta regla
  mecánicamente y emite DICTAMEN-BBIS. Los cortes por sexo, edad y localidad son descriptivos (no deciden).

## 7 · Módulo de auditoría v2.16
- Unidad: persona residente 15+; escala: proporción ponderada. RETROSPECTIVA.
- Segmentación: sexo, cuatro grupos de edad, urbano/rural, sexo×edad; no trata a México como bloque.
- ¿Incentivo o psicología? Ninguno: es un indicador de capital educativo acumulado, no de conducta.
- ¿Clase media urbana? No; el corte rural/urbano está explícito y la población indígena se concentra en rural.
- Peligroso leído simplista: autoadscripción P3_12 no es habla de lengua indígena (P3_19); la brecha es
  sobre todo generacional/geográfica (composición por edad y localidad), no un atributo étnico; «sabe
  escribir un recado» es autodeclarado por el informante del hogar; alfabetismo no mide uso de internet.

el primer resultado que produzca este procedimiento es el que se reporta.
