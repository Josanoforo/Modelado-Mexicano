# F5 · panel viable, fuentes y presupuesto · propuesta v1.0

Estado: **PROPUESTA PARA MESA; NO AUTORIZA LLAMADAS, CAPTURAS L, EMISIONES M NI APERTURA/ESTIMACION R**.

Esta spec convierte `FP-373` y `FP-374` en decisiones separadas. Sucede en
preparación a las dos specs de #713; no reabre `TRIADA-0002`,
`CALC-F5-REANALISIS-0001` ni `NC-0160/0161/0162`.

## 1. Decisión corta

**Recomendación:** autorizar, en un acto posterior, **FP-373 documental** de
32 posiciones, condicionado a que CAJA materialice y verifique los dos paquetes
fuente-nativos y a que Jonás firme llamadas/modelo. **No autorizar FP-374 como
piloto de transferencia:** el panel acreditado tiene **0 familias retenidas
ejecutables**.

El snapshot explícito de #712 sí permite inspeccionar capacidad técnica: 16
salidas directas, agrupadas en 10 familias fuente-estimando. Pero las diez
fueron conocidas durante desarrollo, ninguna tiene rol retenido, y sólo cinco
tienen al menos dos celdas. Incluso ignorando exposición, faltaría una familia
pareada para el piloto; respetando independencia faltan las 18 familias
disjuntas completas (6 piloto + 12 confirmatorias mínimas).

Hay tres líneas de ampliación nominales (`A01`–`A03`): **una candidata
potencialmente reservable** (OECD Trust PUM), **una conocida durante desarrollo**
(Mexico Panel Study 2012) y **una indeterminada** (ENJUVE); las tres tienen
**cero familias disponibles** hoy. No se suman al máximo acreditado porque
faltan acceso, consumidor M, dos celdas exactas y split previo. `X01`–`X04`
son exclusiones por unidad, evento o consumidor, no una reserva oculta.

Fuente nominal completa: `F5-panel-candidatos-v1_0.tsv`.

## 2. Unidad familiar y conteos

Una familia de evaluación es la llave indivisible:

`(regla/constructo, fuente/instrumento, muestra/ola, población, unidad, evento, codificación, transformación)`.

Dos celdas pueden pertenecer a una familia sólo si fueron declaradas juntas
antes de R y comparten fuente/muestra sin ser copias, traducciones o
complementos algebraicos. Se agregan dentro de familia; no elevan `n`.

| ámbito | familias | celdas | familias con >=2 celdas | retenidas ejecutables |
|---|---:|---:|---:|---:|
| snapshot #712 (`S01`–`S10`) | 10 | 16 | 5 | 0 |
| FP-373 documental (`D01`–`D02`) | 2 | 2 | no aplica | no pretende reserva |
| ampliación (`A01`–`A03`) | 3 indeterminadas | 0 congeladas | 0 | 0 |
| exclusiones (`X01`–`X04`) | 4 renglones | 0 | 0 | 0 |

La reserva acreditable es del entorno experimental controlado. No se certifica
ausencia de exposición en el preentrenamiento del LLM.

Fuentes institucionales reabiertas sólo para comprobar disponibilidad y
diseño el 11/sep/2026: [ENNViH-1 2002](https://www.ennvih-mxfls.org/english/ennvih-1.html),
[ENCIG 2021](https://www.inegi.org.mx/programas/encig/2021/),
[estructura ENCIG 2021](https://www.inegi.org.mx/contenidos/programas/encig/2021/doc/encig21_estructura_base_datos.pdf),
[OECD Trust Survey Data](https://www.oecd.org/en/data/datasets/oecd-trust-survey-data.html)
e [ICPSR 35024](https://www.icpsr.umich.edu/web/RCMD/studies/35024).

## 3. Capacidad M y contrato de fuentes

### 3.1 Ruta vigente y límite

Para los consumidores exactos de `S01`–`S10`, la ruta estática es
`emitir_binaria_contrato` → `cargar_indice_linaje_emision` → RESULT/uso
sellado → `PrediccionM`. `milpa/src/linaje.py` separa origen numérico, uso y rol;
`tools/baseline_temporal.py` exige serie exacta, precedencia y disponibilidad.
Esto acredita transporte numérico para esos consumidores, no comparabilidad ni
independencia.

Los candidatos `A01`–`A03` y `X01`–`X04` no tienen consumidor activo en el
snapshot: el comportamiento correcto hoy es `NO_COVERAGE`. Este encargo no
modifica el emisor para hacerlos caber.

### 3.2 Coordinación con encargo 23

Al cierre de esta propuesta, el encargo 23 está publicado pero **no fusionado**
en [PR #720](https://github.com/Josanoforo/Modelado-Mexicano/pull/720), cabeza
`67aa13d73e9300acd14c4b593e3bcfb6bc945712`. La inspección estática de ese
commit introduce:

- `SELECCION-TEMPORAL-v1` y `seleccionar_transferencia`;
- `seleccion_transferencia` estructurada en `emitir_binaria_contrato`;
- rol derivado `OBSERVACION-SERIE-PREVIA`;
- snapshot sucesor `snapshot-M-gen2-explicito-v1_1.json`.

Estos nombres y el SHA de cabeza **no son todavía autoridad**. Antes de
cualquier ejecución, el acto sucesor debe comprobar que #720 fue fusionado,
registrar el commit efectivo en `main`, verificar que contiene la interfaz y
adaptar esta referencia si cambió. Una observación previa seleccionada sirve
para M; nunca se convierte por ello en R objetivo o en rol retenido.

### 3.3 Cuatro ejes que no se colapsan

| eje | evidencia mínima | qué no demuestra |
|---|---|---|
| origen numérico | camino de linaje por RESULT y fuente | validez del reactivo |
| validez de medición | cuestionario, códigos, universo, ponderador y diseño | compatibilidad con el consumidor |
| compatibilidad del estimando | misma tarjeta población/unidad/evento/transformación | independencia |
| independencia de evaluación | split previo, rol retenido, objetivo fuera de ajuste y contexto | que M acertará |

No se necesita conocer el error futuro para declarar elegible una predicción;
se necesita haber congelado identidad y separación antes de abrir R.

## 4. FP-373 · ficha ejecutable de recuperación documental

### 4.1 Pregunta y fuentes concretas

Pregunta: **¿el acceso a archivos fuente-nativos del estimando aumenta la
cobertura de puntos trazables para `DIN-M-01` y `TRA-M-07`, frente al contexto
contemporáneo, sin sustitución semántica?** Si el archivo permite derivar el
objetivo, el resultado mide recuperación/análisis documental, no
generalización.

| celda | fuente nativa dirigida disponible | campos mínimos | reserva |
|---|---|---|---|
| `DIN-M-01` | manifiesto `ennvih1_2002_hogar_q`, `ennvih1_2002_hogar_cb`, `ennvih1_2002_hogar_dta`, `ennvih1_2002_ponderador`, `ennvih1_muestra_diseno`; página oficial ENNViH-1/Book 3B | `cr27`, respuesta válida sí/no, `fac_3b`, población libro 3B, fecha | punto descriptivo verificable; varianza oficial sigue pendiente en FP-371 y no se inventa con constante+folio |
| `TRA-M-07` | `encig2021_cuestionario_pdf`, `encig2021_estructura_base_datos_pdf`, `encig_2021_encig21_base_datos_csv`; tabla `encig2021_01_sec1_A_3_4_5_8_9_10.csv` | `P8_3_1`, `FAC_P18`, `EST_DIS`, `UPM_DIS`, población 18+ urbana | no sustituir por tasa general, P8_4, otra ola o tabla derivada del R del repo |

Ambas fuentes están registradas y hasheadas en el corpus compartido. NUBE no
tiene `data/raw`; por eso el estado es **FUENTES IDENTIFICADAS, TRANSPORTE POR
MATERIALIZAR EN CAJA**, no “archivos ausentes”.

### 4.2 Información de cada brazo

- `CONTEXTUAL-v2`: tarjeta de la celda + el paquete contextual de #698 fijado
  por `paquete-corpus-F5-v2_0/manifiesto-F5-v2_0.json`. No recibe fuente nativa,
  M, R, resultado derivado de R ni archivos de la otra celda.
- `FUENTE-DIRIGIDA-v1`: exactamente lo anterior + cuestionario, codebook/
  estructura, archivo fuente nativo y ponderador de **esa** celda. Puede usar la
  capacidad de análisis de archivos que se congele con el cliente. No recibe
  `CALC-R-*`, tabulación del repo, valor R ni transcripción del objetivo.

CAJA debe producir antes de llamar un manifiesto de miembros con ruta lógica,
SHA-256, bytes, licencia, orden y prueba de transporte. Una serialización de
filas permitida debe ser mecánica y completa para los campos congelados; no
puede incluir una tabulación o estadístico calculado con el objetivo.

### 4.3 Diseño, éxito, faltantes y parada

- 2 celdas × 2 brazos × 8 réplicas = **32 llamadas lógicas**.
- Éxito por celda: dirigido con >=6/8 puntos válidos y trazables, cero
  sustituciones y mejora de cobertura >=4/8 contra su control contemporáneo.
- Una respuesta sin punto se rotula `ABSTENCION`, `MALFORMADA` o
  `ERROR_TECNICO`; nunca cero.
- Si falta un archivo fuente-nativo, campo o ponderador, la celda queda
  `FUENTE-AUSENTE` y **no se llama ningún brazo**. No se sustituye encuesta,
  ola, evento, tabla publicada ni estimando.
- Si el cliente no puede leer el tipo de archivo o trunca el paquete, queda
  `TRANSPORTE-NO-VALIDADO` y no se llama.
- No hay ampliación por resultado. Se para en 32 posiciones, por identidad rota,
  contaminación, o dos fallos sistémicos consecutivos de autenticación/cuota.

### 4.4 Identidad y coste

Antes de llamar se congelan: proveedor, modelo/versión exacta, endpoint,
cuenta/proyecto sin secretos, cliente y versión, mensajes system/user, plantilla
y hashes, herramientas habilitadas, temperatura/top_p/seed si existen, ventana,
límite de salida, política de truncación, paquete y orden de archivos, orden de
posiciones, ventana horaria y parser.

Cada llamada lógica admite máximo **dos reintentos sólo técnicos**. Por tanto:

| concepto | previsto | techo con reintentos |
|---|---:|---:|
| llamadas lógicas | 32 | 32 |
| solicitudes facturables | 32 | 96 |
| emisiones M | 0 | 0 |
| estimaciones R nuevas | 0 | 0 |

Sea `I[c,b]` el input tokenizado y `O` el máximo de salida por posición:

`T_previsto = 8 * sum(I[c,b], cuatro combinaciones celda-brazo) + 32*O`.

`T_techo <= 3*T_previsto` si todo intento técnico consume el máximo. El coste
monetario será `sum(tokens_input*precio_input_modelo + tokens_output*precio_output_modelo)`
con la tarifa oficial vigente capturada al congelar la identidad. No se publica
una cifra monetaria sin modelo, modalidad de caché/batch y conteo del cliente.

## 5. FP-374 · ficha coherente, hoy NO ejecutable

### 5.1 Hipótesis, margen y efecto de planeación

Para la familia `f`, sea `d_f = error_M,f - error_L_SOLO,f`, después de agregar
sus dos celdas predeclaradas. El margen sustantivo es 2 puntos porcentuales:

- `H0: E[d_f] >= -0.02`;
- `H1: E[d_f] < -0.02`;
- éxito: límite superior del IC95 bilateral de `E[d_f]` **< -0.02**.

El efecto esperado de planeación debe ser más exigente que el margen. Se fija
`Delta_plan=-0.04`; la distancia al borde nulo es `g=0.02`. Con potencia 80% y
alfa unilateral 2.5%:

`n = ceil(((z_0.975 + z_0.80) * sigma_plan / g)^2)`, mínimo 12, máximo 30.

Así el denominador de 2 pp corresponde a la separación entre efecto esperado
(-4 pp) y criterio de éxito (-2 pp), no a probar “cualquier mejora”.
`sigma_plan` es el límite superior unilateral 80% de la DE entre familias del
piloto. Se fija `n` antes de abrir R confirmatorios. Si `n>30`, se declara
inviable; no se rebaja el margen ni se selecciona otro estimador.

### 5.2 Piloto, confirmación y dependencia

- Piloto: 6 familias retenidas × 2 celdas × 2 brazos L × 8 réplicas = 192
  llamadas. Estima varianza/operación; no entra al análisis confirmatorio.
- Confirmación disjunta: `n=12..30` familias × 2 celdas × 2 brazos × 8 =
  384..960 llamadas.
- Unidad inferencial: familia, no celda ni réplica. Las dos celdas se promedian
  dentro de familia; réplicas L producen una mediana por celda/brazo y su IQR.
- IC primario: procedimiento por familia congelado antes de confirmación
  (t de Student sobre `d_f`, con bootstrap de familias sólo como sensibilidad,
  o el inverso; no se elige tras R).

### 5.3 Abstención, cobertura, faltantes y varianza R

- Celda L analizable por brazo: >=4/8 respuestas válidas; las demás conservan
  causa. Mediana e IQR usan sólo válidas.
- Abstención M es `NO_COVERAGE`, nunca cero ni error numérico imputado.
- Cobertura usa como denominador todas las celdas elegibles congeladas: M >=90%
  y no más de 5 pp menor que L_SOLO.
- Error pareado de una celda requiere punto M, mediana L_SOLO y R; la pérdida
  sale del error pero cuenta contra cobertura. Familia primaria requiere sus
  dos celdas completas.
- Menos de 12 familias confirmatorias analizables:
  `NO-ADJUDICABLE-POR-COBERTURA`.
- Contaminación, cambio de snapshot/interfaz o identidad:
  `NO-ADJUDICABLE-POR-CONTROL`.
- R debe tener estimando y diseño acreditados. Con réplicas oficiales, se
  propaga su incertidumbre al contraste; sin varianza defendible, la celda se
  reporta descriptiva y no vuelve inferencial usando varianza cero. La
  incertidumbre R, variación L y variación entre familias se publican separadas.

No hay parada temprana por victoria o derrota. Se para por control roto, dos
fallos sistémicos consecutivos, alcanzar `n`, o `n>30`.

### 5.4 Identidades y coste

Además de las identidades de §4.4 se congelan: repo HEAD, commit/hash de la
interfaz fusionada del encargo 23, snapshot M elegible, registro de familias y
asignación piloto/confirmación, tarjetas M/R, códigos de análisis, semilla de
agregación/bootstrap y política de revelación R. El modelo que ejecuta Codex no
sustituye al competidor firmado.

| tramo | llamadas lógicas previstas | solicitudes máximas con 2 reintentos por posición | M | R |
|---|---:|---:|---:|---:|
| piloto | 192 | 576 | 12 | 12 |
| confirmación mínima | 384 | 1,152 | 24 | 24 |
| confirmación máxima | 960 | 2,880 | 60 | 60 |
| total mínimo | 576 | 1,728 | 36 | 36 |
| total máximo | 1,152 | 3,456 | 72 | 72 |

Para cada celda `j`, `T_j=8*(I_j,L_SOLO+I_j,L_CORPUS)+16*O`; el total previsto
es la suma sobre 36..72 celdas y el techo técnico es hasta tres veces ese total.
El precio monetario se calcula sólo tras congelar modelo/cliente/modalidad y
medir tokens aceptados por el proveedor.

## 6. Opciones para Jonás

1. **Recomendada — firmar FP-373:** ejecutar el acto en cola después de
   materializar y validar fuentes en CAJA. Pregunta recuperación documental;
   coste 32 llamadas lógicas, techo 96 solicitudes.
2. **No firmar FP-374 hoy:** hay 0/18 familias retenidas ejecutables. El déficit
   exacto es 18 familias bajo independencia; aun contando material conocido,
   sólo 5/6 familias tienen dos celdas para el piloto y ninguna es retenida.
3. **Rediseño acotado:** si la mesa quiere aprender antes de reunir 18 familias,
   congelar `A01`–`A03` antes del acceso y ejecutar, cuando existan, un estudio
   de factibilidad de hasta 3 familias sin hipótesis confirmatoria ni lenguaje
   de transferencia. Termina al resolver esas tres fuentes; no abre búsqueda
   indefinida.
4. **Mantener la pregunta confirmatoria:** abrir un encargo de ampliación sólo
   cuando exista una lista nominal previa de 18 familias × 2 celdas y un
   consumidor M para cada una. Hasta entonces no hay piloto FP-374.

Preparación no cierra `FP-373/374`, `NC-0160/0161/0162`, no autoriza F6 y no
firma DIN, S6, complementos ni deduplicación ENCIG.
