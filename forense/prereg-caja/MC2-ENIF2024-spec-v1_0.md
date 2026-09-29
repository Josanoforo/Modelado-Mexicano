# MC2 · ENIF 2024 · pisos por segmento de inclusión financiera, previsión y razones · spec v1.0

ACTO GEN2-MEDICION-CARRILES-2, hija ENIF 2024, entorno CAJA, rama
`acto/gen2-medicion-carriles-2--enif2024`. CALC: `data/corrida0/CALC-MC2-ENIF2024-0001`
(medidor `medidor.py`; prueba sintética `tests/test_mc2_enif2024.py`). Encargo:
`forense/encargos/2026-09-28-GEN2-MEDICION-CARRILES-2.md` (sello de cuerpo `c791b192…`).
Todo es **RETROSPECTIVA** (ENIF 2024 es ola vista; ver §0). No adopta; no hay retador ni θ.

## 0 · Premisas, reserva y lectura previa

- `[EJECUTADO]` Payload `enif_2024_enif_2024_bd_csv` (manifiesto), sha256 del zip
  `00e4b0b42775276b…` COINCIDE con el manifiesto. Miembro leído: `TMODULO.csv` (398 columnas).
- `[EJECUTADO]` Reserva E.6. `tools/corpus_loader.motivo_reserva` devuelve para este id
  «h→firmada R06 RESERVADA: ENIF 2024 (reservas por módulo; módulo 7)». La reserva de **ola** de
  ENIF 2024 ya se consumió (lote de 14 cruces, `FP-260921-GEN2-TRAMITE-FIRMAS-4-8a1f-01`;
  `forense/analisis/familias-2027/EXPEDIENTE-v1_1.md:34`: «La reserva sin decidir de ENIF 2024 es
  el módulo 7 (pagos)»), y R06 la firmó **RESERVADA** (`2026-09-28-GEN2-TRAMITE-FIRMAS-21-ADENDA-1.md:11`).
  Los módulos 3, 4, 5, 6 y 9 ya los leyeron CALC sellados (`CALC-AMAI-NSE-ENIF-2024-0001`: P3_8,
  P3_13, P4_10, P5_4_*, P9_9_4; `CALC-DIN-CREDITO-PREDICCION-2024-ADJUDICACION-0001`: P6_2_*,
  P6_14, P6_17_*). El módulo 8 (seguros) no lo leyó ningún CALC sellado; no tiene reserva
  declarada en el manifiesto, en `RESERVA_FUERA_DEL_MANIFIESTO`, en la memoria operativa ni en
  la hoja de FIRMAS-21, y la ola no es nueva: se lee como parte de una ola vista (decisión del
  ejecutor, reversible, declarada). **Ninguna columna `P7_*` es input**; el medidor revienta
  (`ReservaRota`) si su lista la pide, con prueba en el sintético.
- HOLDOUT (R01 (b)): el único momento del catálogo sobre ENIF 2024 es `M23`
  `dinero.ahorro.via_informal`, marcado GASTABLE-COMO-PISO. `TANDA` es un componente de la vía
  informal: esta spec **declara** que lo consume como piso RETROSPECTIVO. Ningún momento
  HOLDOUT no gastable se toca.
- Lectura de estructura antes del COMMIT-1 (permitida, declarada): FD `enif2024_fd_xlsx`
  (hoja TMODULO), cuestionario `enif2024_cuestionario_pdf` (texto por `pdftotext`, secciones 4,
  5, 6, 8, 9 y el flujo de pases), `enif2024_diseno_muestral_pdf` (población objetivo) y la
  **cabecera** de `TMODULO.csv`. Ningún registro leído, contado ni tabulado.
- E.5 (lo sellado se cita, no se re-mide): el catálogo v1.3 ya trae de ENIF 2024 el portafolio
  de ahorro (vías formal/informal, `tiene_ahorros`, horizonte condicional, desconfianza, recibe
  dinero de familiares para la vejez) por NSE, región y ejes. Ninguno mide tenencia de afore,
  aportación voluntaria, seguro, tarjeta departamental/bancaria, crédito formal agregado, crédito
  de vivienda, tanda sola, metas de largo plazo, cobertura de un mes sin ingresos (P4_10 en toda
  la población), expectativas de vejez P9_9_1/P9_9_5 ni las razones P6_14, P6_17_4, P9_2 y P5_13.
  `CTA-APP` (P5_4_8) sí tiene cifra nacional en `CALC-ENIF-FINTECH-0001` (control 2024): aquí se
  mide sólo por el cruce de segmentos, y la nacional se cita de ese CALC para APUEST-011.

## 1 · Variables por texto (A.15), códigos y construcción

ENIF 2024, `TMODULO.csv`, una fila por persona elegida (18+). Códigos por el FD; cero a la
izquierda normalizado; «b» (blanco por secuencia), «8» (no responde) y «9» (no sabe/no
especificado) salen del denominador y se cuentan donde el DIAG lo nombra, nunca se imputan.

| indicador | reactivo (texto verbatim del FD/cuestionario) | 1 = | denominador |
|---|---|---|---|
| CUENTA | 5.4 «¿Usted tiene…» nómina, pensión, apoyos de gobierno, ahorro, cheques, plazo fijo, fondo de inversión, cuenta por internet o aplicación, otro (`P5_4_1..9`) | algún ítem = 1 | los nueve ítems en {1,2} |
| CTA-AHORRO | 5.4 «¿Usted tiene cuenta de ahorro?» (`P5_4_4`) | 1 | {1,2} |
| CTA-APP | 5.4 «¿Usted tiene cuenta contratada por internet o aplicación (no bancaria) como Mercado Pago, Nu o Spin de Oxxo?» (`P5_4_8`) | 1 | {1,2} |
| CRED-FORMAL | 6.2 «¿Usted tiene…» departamental, bancaria, nómina, personal, automotriz, vivienda, grupal, por internet, otro (`P6_2_1..9`) | algún ítem = 1 | los nueve en {1,2} |
| TC-DEPTO | 6.2 «¿Usted tiene tarjeta de crédito departamental o de tienda de autoservicio?» (`P6_2_1`) | 1 | {1,2} |
| TC-BANC | 6.2 «¿Usted tiene tarjeta de crédito bancaria u otra institución financiera?» (`P6_2_2`) | 1 | {1,2} |
| CRED-VIV | 6.2 «¿Usted tiene crédito de vivienda como Infonavit, Fovissste, banco u otra institución?» (`P6_2_6`) | 1 | {1,2} |
| SEGURO | 8.1 «¿Usted tiene algún seguro de auto, de casa, de vida, de gastos médicos u otro (sin considerar el IMSS-Bienestar, Seguro Popular, INSABI, IMSS o ISSSTE)?» (`P8_1`) | 1 | {1,2} |
| AFORE | 9.1 «¿Usted tiene una cuenta de ahorro para el retiro o AFORE?» (`P9_1`) | 1 | {1,2} |
| AFORE-VOL | 9.3 «¿Usted realiza aportaciones voluntarias a su cuenta de ahorro para el retiro o AFORE?» (`P9_3`), sólo con `P9_1 = 1` (pase del cuestionario) | 1 | {1,2} y `P9_1 = 1` |
| PRODUCTO-FORMAL | CUENTA = 1 o CRED-FORMAL = 1 o `P8_1 = 1` o `P9_1 = 1` | alguno | CUENTA y CRED-FORMAL válidos |
| TANDA | 5.1 «En los últimos 12 meses, de junio de 2023 a la fecha, ¿usted participó en una tanda?» (`P5_1_5`) | 1 | {1,2} |
| METAS-SIEMPRE | 4.6.4 «Generalmente, ¿se pone metas económicas a largo plazo y se esfuerza por alcanzarlas…?» (`P4_6_4`) | 1 Siempre | {1,2,3} |
| CUBRE-MES | 4.10 «Si usted dejará de recibir ingresos, ¿por cuánto tiempo podría cubrir sus gastos con sus ahorros?» (`P4_10`) | 3, 4 o 5 (un mes o más) | {1..5} |
| VEJEZ-GOB | 9.9 «En su vejez, ¿piensa cubrir sus gastos con lo que reciba de los apoyos del gobierno para personas adultas mayores?» (`P9_9_1`; se pregunta a 18–70, FILTRO 1 de §9) | 1 | {1,2} |
| VEJEZ-TRAB | 9.9 «… de seguir trabajando?» (`P9_9_5`) | 1 | {1,2} |

Distribuciones de razón principal (proporción de cada código entre los códigos válidos):
`NUNCACRED-RAZON` = 6.14 «¿Cuál es la razón principal por la que nunca ha tenido un préstamo,
crédito o tarjeta de crédito?» (`P6_14`, códigos 1–9; 7 = «No le gusta endeudarse»);
`NOAFORE-RAZON` = 9.2 «¿Cuál es la razón principal por la que no ha tenido AFORE o SAR?»
(`P9_2`, 1–9; se pregunta a quien no tiene afore y nunca cotizó), más dos grupos fijados aquí:
`G-SINTRAB-INGRESO` = {1 No trabaja o nunca ha trabajado, 3 No tiene dinero o es insuficiente}
y `G-VEHICULO` = {2 No sabe qué es, 4 No sabe cómo tramitarla, 6 Las Afores le dan desconfianza,
8 Trabaja por su cuenta y no sabía que podía tramitarla}; `EFECTIVO-RAZON` = 5.13 «¿Cuál es la
razón principal por la que prefiere pagar sus compras en efectivo?» (`P5_13`, 1–7; 9 fuera).
`RECHAZO-SINHISTORIAL` = 6.17 «¿Cuáles son las razones por las que le negaron el crédito? No
tenía historial crediticio» (`P6_17_4`, 1 Sí se mencionó / 0 No se mencionó; «b» fuera).

Segmentos (§3, México no es bloque): NAC; SEXO (`SEXO` 1 hombre, 2 mujer); EDAD (`EDAD_V`,
cortes de `FP-384`: 18-29, 30-44, 45-59, 60+; 98 fuera); ESCOLARIDAD (`NIV` 3.1: HASTA-PRIMARIA
00–02, SECUNDARIA 03–05, MEDIA-SUPERIOR 06–07, SUPERIOR 08–11; 99 fuera); LOCALIDAD (`TLOC`:
15 000 y más = 1–2, menos de 15 000 = 3–4, los mismos cortes que `ENIFPIC-D9`); REGIÓN (`REGION`
1–6, FD TMODULO); FORMALIDAD (`P3_13`: CON-SS = derecho a servicios médicos por su trabajo,
códigos 1–6; SIN-SS = 7; quien no trabaja, «b», y 9 quedan fuera del eje). **Clase** (NSE AMAI)
no se cruza aquí: exige el módulo de regla AMAI como input (`CALC-AMAI-NSE-ENIF-2024-0001`), y
la escolaridad no se rotula como clase. Las razones se cortan sólo NAC y SEXO. Ningún cruce
doble (sexo × edad, etc.).

## 2 · Universo, unidad, ponderador, diseño, IC, agregador

- Unidad: **persona elegida de 18 años y más** residente de vivienda particular (población
  objetivo del diseño muestral 2024: «población de 18 años y más»). Escala: proporción [0,1];
  diferencias en [−1,1].
- Ponderador `FAC_PER` («Factor de expansión a nivel persona»). Diseño: estrato `EST_DIS`, UPM
  `UPM_DIS` (llaves opacas de texto). Fila sin ponderador positivo o sin diseño sale de todo,
  contada (`DIAG-N-SIN-PONDERADOR`).
- Agregador (E.1): razón ponderada Σw·y/Σw por celda. Brechas: MUJER − HOMBRE para CUENTA,
  CTA-AHORRO, CRED-FORMAL, SEGURO, AFORE, PRODUCTO-FORMAL y TANDA; CON-SS − SIN-SS para AFORE,
  SEGURO, CRED-VIV, CUENTA y CRED-FORMAL; `NOAFORE-RAZON-DIF-VEHICULO-SINTRAB-NAC` =
  G-VEHICULO − G-SINTRAB-INGRESO. Toda diferencia se calcula en la misma réplica.
- IC95: bootstrap de UPM con reemplazo dentro de estrato, **2 000 réplicas**, `PCG64(42)`,
  bloques de 50; estrato de UPM única se remuestrea a sí mismo (contado en
  `DIAG-N-ESTRATOS-UPM-UNICA`); percentiles 2.5/97.5. Celda vacía → P/IC null
  (`permite_no_estimable`), N se conserva.
- Salida: sólo RESULT escalares, ids `RESULT-MC2-ENIF2024-…` con sufijos `-P`, `-IC95-INF`,
  `-IC95-SUP`, `-N` (n no ponderado), y `-DIAG-*` enteros.

## 3 · Pre-registro de falsación B-bis (fijado antes del dato)

Reglas generales, fijadas aquí para toda afirmación de esta pieza:
- **Nivel** (el report da una proporción `c`): CONFIRMA si `c` ∈ IC95; MATIZA si `c` ∉ IC95 y
  |punto − c| ≤ 0.10; ROMPE si |punto − c| > 0.10. Si el report da un rango `[a,b]`: CONFIRMA si
  el punto ∈ `[a,b]`; si no, la misma regla contra el extremo más cercano.
- **Signo/orden**: ROMPE si la brecha u orden que el report afirma sale con signo contrario
  (punto ≤ 0 donde afirma > 0).
- Afirmación con varios componentes: dictamen = el **peor** (ROMPE > MATIZA > CONFIRMA).
  Componente no medible aquí: se nombra y el dictamen se rotula `PARCIAL` (cubre sólo lo medido).
- Mecanismo, motivo o causa que el report añada («aversión al riesgo», «crisis de 1994»,
  «estabilidad permite horizonte») **no es observable** en ENIF; el dictamen es sobre la conducta.

| afirmación | estimando que manda y regla |
|---|---|
| FIN-003 | CUENTA-MUJER vs 0.586 y CUENTA-HOMBRE vs 0.680 («cuenta de ahorro formal»: se lee como tenencia de alguna cuenta 5.4, el agregado que el report llama 63.0 %; CTA-AHORRO se reporta, no manda); AFORE-MUJER vs 0.342 y AFORE-HOMBRE vs 0.514 (nivel); ROMPE si CUENTA- o AFORE-BRECHA-MUJER-HOMBRE ≥ 0 |
| FIN-004 | AFORE-NAC vs 0.422; AFORE-VOL-NAC vs 0.079 (nivel) |
| FIN-005 | SEGURO-NAC vs 0.229 (nivel); «producto más rezagado»: ROMPE si SEGURO-NAC no es el menor de {CUENTA, CRED-FORMAL, SEGURO, AFORE}-NAC |
| FIN-006 | VEJEZ-GOB-NAC vs 0.682; VEJEZ-TRAB-NAC vs 0.673 (nivel; universo 18–70 por el pase) |
| FIN-009 | NUNCACRED-RAZON-7-NAC vs 0.384 (nivel) |
| FIN-010 | CUENTA-NAC vs 0.630 (nivel); la ola 2015 (44.1 %) no es input: `PARCIAL` |
| FIN-034 | CUENTA 0.630, CRED-FORMAL 0.373, SEGURO 0.229, AFORE 0.422, TC-DEPTO 0.226, TC-BANC 0.157 (nivel, NAC); ROMPE si TC-DEPTO-NAC ≤ TC-BANC-NAC |
| CONS-039 | PRODUCTO-FORMAL-MUJER vs 0.728, -HOMBRE vs 0.809 (nivel); ROMPE si PRODUCTO-FORMAL-BRECHA-MUJER-HOMBRE ≥ 0 |
| CONS-011 | TC-BANC-NAC vs el rango [0.10, 0.15] |
| FAM-017 | componente medible aquí: «Solo el 24 % tiene cuenta bancaria» → CUENTA-NAC vs 0.24 (nivel). «36.6 % ahorra exclusivamente de manera informal» y «la mitad» se citan del catálogo (E.5, `ahorra_solo_informal`), no se re-miden: `PARCIAL` |
| FIN-002 | sin cifra: «infraestructura financiera masiva». TANDA-NAC: CONFIRMA si IC95-INF ≥ 0.10 (una de cada diez personas adultas; umbral fijado aquí); ROMPE si punto < 0.05; MATIZA en otro caso |
| CRPOP-056 | TANDA-NAC vs 0.30 (nivel). El report cita ENIF 2012/2015; ENIF 2024 es otra ola: el dictamen no sube de MATIZA |
| APUEST-015 | «~49.5 % de adultos sin acceso a crédito formal» → 1 − CRED-FORMAL-NAC vs 0.495 (nivel, se usa el punto e IC de CRED-FORMAL-NAC reflejados); las cifras Kueski/Aplazo no son de ENIF: `PARCIAL`. RECHAZO-SINHISTORIAL se reporta (sin cifra en el report) |
| TIME-001 | METAS-SIEMPRE-NAC vs 0.40 («cerca de cuatro de cada diez», nivel) |
| TIME-006 | AFORE-, SEGURO- y CRED-VIV-DIF-CONSS-SINSS: CONFIRMA si los tres IC95-INF > 0; ROMPE si algún punto ≤ 0; MATIZA en otro caso |
| TIME-014 | NOAFORE-RAZON-DIF-VEHICULO-SINTRAB-NAC: CONFIRMA si IC95-INF > 0; ROMPE si NOAFORE-RAZON-G-SINTRAB-INGRESO-NAC ≥ 0.5; MATIZA en otro caso |
| TIME-032 | CUBRE-MES-NAC vs 0.43 (nivel) |
| TRUST-019 | EFECTIVO-RAZON-4-NAC («Le dan desconfianza las tarjetas de débito»): CONFIRMA si es la moda (punto mayor que el de cada otro código 1–7); ROMPE si punto < 0.10; MATIZA en otro caso. La parte P7_9 (módulo 7) queda DIFERIDA por R06 |

Fuera de esta pieza, con su razón (vocabulario A.4): APUEST-030, APUEST-032 y CONS-010 miden
P7_1/P7_2/P7_3 → **DIFERIDO-A apertura de R06** (módulo 7 RESERVADO). APUEST-011 → nacional
**citada** de `CALC-ENIF-FINTECH-0001` (E.5); aquí sólo segmentos. CLIENT-014 (padrón de la
pensión, 5.1 → 12.1 millones) → **NO-CONSTRUIBLE**: es un conteo de registro administrativo;
ninguna encuesta del corpus lo mide. ASPIR-005 (ENIF 2015, uso de tarjeta de crédito en
comercios) → otra ola, fuera de esta pieza: queda en la tabla de apertura como pendiente.

Reglas del motor con ENIF como instrumento (`reglas-contrastadas-v1_1.tsv`): las doce son
NO-CONSTRUIBLE por texto (prescriptivas o metodológicas) en v1.0/v1.1 y esta pieza no trae
motivo nuevo para ninguna (RG-34a21bc6a2 pide el tipo de organizador de la tanda; ENIF no lo
pregunta). Esta pieza no dictamina reglas.

## 4 · Módulo de auditoría v2.16

- Unidad: persona elegida 18+; nunca hogar; escala proporción.
- RETROSPECTIVA: ENIF 2024 es ola vista; nada es predicción.
- Segmentación: sexo, edad, escolaridad, tamaño de localidad, región, formalidad; cada brecha se
  lee dentro de su segmento, sin cruces dobles.
- ¿Incentivo o psicología? Tenencia de afore, seguro y crédito de vivienda siguen primero a la
  formalidad laboral (el afore y el Infonavit vienen con el empleo formal): una brecha CON-SS −
  SIN-SS es **oferta institucional**, no «previsión» como rasgo. Las razones de no tener afore o
  de preferir efectivo se reportan como declaradas; no se leen como psicología profunda.
- Oferta antes que preferencia: donde hay mercado (crédito, seguro, pagos), la razón «no le
  interesa» se reporta junto a las de acceso (requisitos, sucursal, comisiones, no la aceptan).
- ¿Clase media urbana? Ninguna cifra se atribuye a «la clase media»; clase no se cruza aquí.
- Firewall genético: ninguna variable de ascendencia; nada de ascendencia → conducta.

El primer resultado que produzca este procedimiento es el que se reporta.
