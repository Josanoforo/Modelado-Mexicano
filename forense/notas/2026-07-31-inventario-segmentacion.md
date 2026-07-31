# Inventario de segmentación · INV-SEG partes 1 y 2

*31 de julio de 2026. Responde al ENCARGO INV-SEG. Ocho fuentes en disco:
ENIGH, ENIF, ENVIPE, ENOE, ENCUCI, ENCIG, ENSANUT, ENUT.*

**Firewall respetado.** Se abrieron descriptores/diccionarios de variables,
catálogos código→etiqueta y cuestionarios (nombres de variable, etiquetas
de pregunta, códigos de valor, estructura de tablas/hojas). No se abrió
ninguna carpeta `conjunto_de_datos/` (microdato real) de ningún ZIP, ningún
`.dbf`/`.csv.csv.zip`/`.stata.zip` de datos, ni fila, frecuencia,
distribución o cruce. Extracción vía `pdftotext -layout` (PDF), `zipfile`
estándar de Python sobre `diccionario_de_datos/`/`catalogos/` (CSV dentro
de ZIP), y un volcador propio de XML crudo para `.xlsx` (sin librerías
externas — `openpyxl`/`pandas` no están instalados en este entorno). Los
`.txt` derivados viven en el scratchpad de la sesión, no en el repo.

⚠️ **Declaración de contaminación (ADR-46).** Esta sesión abrió descriptores
de las ocho fuentes del encargo. Queda contaminada de forma permanente para
pre-registrar contra cualquiera de las ocho. Esperado, no defecto.

**Método de trabajo.** Ocho subagentes en paralelo, uno por fuente, cada
uno con el mismo firewall y el mismo catálogo de 49 reglas/6 ejes. Se
detectaron y cerraron en la misma sesión dos huecos de encargo incompleto
(ver `forense/hallazgos.md`, línea del 31/jul sobre este archivo): ENOE no
recibió los ids exactos de `familia.cuidado`/`familia.union`/`familia.cortejo`,
`tiempo.compromiso`/`tiempo.bomberazo`/`tiempo.cumplimiento`, ni ningún id
de `cooperacion.*`/`comunicacion.*`; ENUT no recibió los ids de
`trabajo.jerarquia`/`trabajo.liderazgo`/`trabajo.rotacion`. Se completaron
directamente en esta sesión con `grep`/`pdftotext` sobre los mismos
archivos ya identificados por los subagentes — resultados integrados abajo,
sin marca especial salvo donde se cita explícitamente.

⚠️ **No se estima cobertura de perfiles.** ADR-50(5) declara la
correspondencia perfil↔demografía un riesgo declarado y no resuelto, fuera
del alcance de esta sesión. Ninguna fila de abajo asigna casos a perfiles.

---

## TABLA A — Ejes de segmentación (eje × fuente × variable × página)

### 1. Formalidad laboral (acceso a seguridad social por el trabajo)

| fuente | sí/no/parcial | variable(s) | página/hoja | nota |
|---|---|---|---|---|
| ENIGH | Sí | `segsoc` (poblacion); `contrato`, `tipocontr`, `pres_1..20` (prestaciones, incl. `pres_8` SAR/AFORE), `medtrab_1..7` (servicio médico por trabajo) | `diccionario_datos_poblacion_enigh2022_ns.csv`; `diccionario_datos_trabajos_enigh2022_ns.csv` | Directo y desagregado: derechohabiencia general + contrato + batería completa de prestaciones |
| ENIF | Sí | `P3_13` "¿tiene derecho a los servicios médicos... del Seguro Social (IMSS)?" (7 categorías + carece) | TMODULO Sección 3, cuestionario p.7 | Verificado de nuevo (ya conocido de CAL-CONF Fase A); confirmado literal |
| ENVIPE | Parcial | `AP3_8` (condición de actividad), `AP3_10` (posición en la ocupación: jornalero/empleado/cuenta propia/patrón/sin pago) | Cuest. principal Sección III, preg. 3.8/3.10, p.3 | Sin pregunta de afiliación IMSS/ISSSTE/prestaciones — `grep -i "seguridad social\|IMSS\|ISSSTE\|prestaciones"` sin resultados en los 3 PDF |
| ENOE | Sí | `SEG_SOC` (acceso a institución de salud por trabajo), `EMP_PPAL`/`TUE_PPAL` (formal/informal, sector informal) | `con_basedatos_proy2010.pdf` p.22-23; `c_bas_v7.pdf` p.9 pregunta 6d | Variable de referencia nacional de informalidad, construida exactamente sobre acceso a IMSS/ISSSTE/otra institución |
| ENCUCI | Sí | `AP3_15_4` "¿...derecho a servicios públicos de salud (IMSS, ISSSTE u otro)?" | Tabla CS, pregunta 3.15, **p.12** | **Corrección de página** frente a CAL-CONF Fase A, que citó p.15 — verificado contando folios impresos del PDF; ver `forense/hallazgos.md` |
| ENCIG | Parcial | `POS` (posición ocupacional: jornalero/empleado/cuenta propia/patrón/sin pago) | Pregunta 2.10, p.39 (edición 2023) | Proxy débil, no mide formalidad contractual/afiliación; sin módulo de prestaciones (`grep -i "afiliac\|IMSS\|ISSSTE\|prestaciones"` solo halla IMSS/ISSSTE como prestador de salud evaluado en sección de confianza, no como afiliación laboral). CAL-CONF Fase A había marcado este eje "NO" con criterio más estricto (exige prestación/afiliación, no solo posición ocupacional) — ambos criterios son defendibles, se deja "parcial" con el límite explícito |
| ENSANUT | Parcial | `H0310A/B/C` (derechohabiencia: IMSS/ISSSTE/PEMEX-Defensa-Marina/seguro privado/IMSS-BIENESTAR/ninguno) | Cuest. Hogar Sección III, preg. 3.10, p.8 | Es derechohabiencia, puede heredarse de otro cotizante del hogar, no necesariamente del empleo propio actual; sin módulo de ocupación/condición de actividad |
| ENUT | Parcial | `P5_6_1..8` (derecho a licencia/vacaciones/jubilación/AFORE/guardería/servicio médico IMSS-ISSSTE/crédito vivienda) + `P5_5` (posición ocupacional) | TMODULO Sección V | Capta los insumos de formalidad pero no hay variable derivada "formal/informal" en `TVAR_CREA` (hoja revisada completa, no aparece) |

### 2. Edad

| fuente | sí/no/parcial | variable(s) | página/hoja |
|---|---|---|---|
| ENIGH | Sí | `edad` (poblacion), `edad_jefe` (concentradohogar) | `diccionario_datos_poblacion_enigh2022_ns.csv` |
| ENIF | Sí | `EDAD` (TSDEM, todo el hogar), `EDAD_V` (TMODULO, persona elegida) | TSDEM p.3; TMODULO p.5 |
| ENVIPE | Sí | `EDAD` | Cuest. principal Sección III, preg. 3.5, p.3 |
| ENOE | Sí | `EDA` + derivadas `EDA5C`/`EDA7C`/`EDA12C`/`EDA19C` | `c_sdem_v5a.pdf` p.4 |
| ENCUCI | Sí | `EDAD` | Tabla CS, pregunta 3.6, p.10 |
| ENCIG | Sí | `EDAD` | Pregunta 2.5, p.38 (2023) |
| ENSANUT | Sí | `h0303` | Cuest. Hogar Sección III, preg. 3.3, p.5 |
| ENUT | Sí | `EDAD` | Pregunta 3.5, TSDEM/TVAR_CREA |

### 3. Urbanización / tamaño de localidad

| fuente | sí/no/parcial | variable(s) | página/hoja | nota |
|---|---|---|---|---|
| ENIGH | Sí | `tam_loc` (4 categorías, 100k+ a &lt;2,500 hab.) | `diccionario_datos_concentradohogar_enigh2022_ns.csv` + catálogo `tam_loc.csv` | — |
| ENIF | Sí | `TLOC` (4 categorías) | TVIVIENDA/TSDEM/TMODULO | Variable de diseño muestral, no reactivo del cuestionario |
| ENVIPE | Sí | `DOMINIO` (U/C/R: Urbano/Complemento urbano/Rural) | Variable de diseño muestral, tabla `tsdem` | — |
| ENOE | Sí | `T_LOC`/`T_LOC_TRI`/`T_LOC_MEN` (4 tramos) + `UR` (binario) | `con_basedatos_proy2010.pdf` p.32 | — |
| ENCUCI | Parcial | `DOMINIO` (U/C/R, etiquetado) + `ESTRATO` (1-4, sin etiqueta de tamaño en el diccionario) | Tabla VIV, p.8 | `ESTRATO` no se puede interpretar sin documentación externa |
| ENCIG | Parcial | `AREAM`/`NOM_AREAM` (área metropolitana vs. resto de ciudades ≥100k) | Campo 12, p.5-6 (2023) | **Límite de diseño, no de instrumento**: el universo de ENCIG excluye localidades &lt;100,000 hab. — no hay variable tipo ENOE/ENIGH de tramo rural-urbano completo |
| ENSANUT | Sí | `estrato` (Rural &lt;2,500 / Urbano 2,500-99,999 / Metropolitano 100mil+) | `hogar_ensanut2024_w_ICB.Catlogo.xlsx` pos.199 | — |
| ENUT | Sí | `TLOC` (4 categorías) + `MENOR10` (binaria) | Variables derivadas, THOGAR/TSDEM/TVAR_CREA | — |

### 4. Ingreso / proxy de nivel socioeconómico

| fuente | sí/no/parcial | variable(s) | página/hoja | nota |
|---|---|---|---|---|
| ENIGH | Sí | `ing_cor` (ingreso corriente del hogar, continuo) + `est_socio` (índice NSE 4 categorías, ya construido) | `diccionario_datos_concentradohogar_enigh2022_ns.csv` + catálogo `est_socio.csv` | Única fuente del corpus con ambas: ingreso monetario continuo e índice NSE categórico |
| ENIF | Sí (parcial como NSE) | `P3_11A`/`P3_11B` (monto y periodicidad de ingreso individual), `P3_12` (fijo/variable) | TMODULO Sección 3, p.7 | Ingreso individual autorreportado, no índice compuesto de NSE |
| ENVIPE | Parcial | `ESTRATO` (1-4, estrato sociodemográfico de diseño muestral por AGEB) | Tablas `tper_vic1`/`tmod_vic` | Estrato del área, no ingreso declarado por el entrevistado; sin pregunta de ingreso (`grep -i "ingreso"` solo aparece en batería de prioridades de política pública) |
| ENOE | Sí | `INGOCUP` (ingreso mensual), `ING7C` (categorías por salario mínimo), `ING_X_HRS` | `con_basedatos_proy2010.pdf` p.22 | — |
| ENCUCI | Sí | `AP10_14` (6 rangos de ingreso mensual, incluye remesas en el enunciado sin separarlas) | Pregunta 10.14, tabla SEC_9_10, p.55 | — |
| ENCIG | No | ninguna variable de ingreso/gasto/NSE | — | `grep -i "ingreso\|NSE\|nivel socioecon\|bienestar\|pobreza"` sobre diccionario 2023 completo (4,462 líneas): solo "Pobreza"/"Bienestar" como ítems de opinión/nombres de programa, ninguno mide ingreso u NSE del hogar. Único proxy disponible: escolaridad (`NIV`/`GRA`) |
| ENSANUT | Sí | `indice1`/`nseF`/`nse5F` (índice de bienestar y NSE por terciles/quintiles) + `h0327` (ingreso mensual del hogar, abierto) | Catálogos `NSE_Hogar`/`NSE_Integrantes`; Cuest. Hogar p.12 | Doble evidencia: índice compuesto + pregunta directa |
| ENUT | Parcial | `P5_10` (ingreso laboral individual, solo aplica a quien trabajó) + `P2_4_01..14` (bienes del hogar, proxy AMAI) | TMODULO Sección V; THOGAR Sección II | Sin ingreso total del hogar |

### 5. Acceso digital (internet, smartphone, banca en línea)

| fuente | sí/no/parcial | variable(s) | página/hoja | nota |
|---|---|---|---|---|
| ENIGH | Parcial | `conex_inte`/`celular` (SERV_4/SERV_2, tenencia a nivel hogar) | `diccionario_datos_hogares_enigh2022_ns.csv` | Sin distinción smartphone vs. celular básico; sin banca en línea |
| ENIF | Sí (fuerte) | `P3_14` (smartphone), `P0_4_2` (internet vivienda), `P5_17_2`/`P7_7` (transferencias por app/internet), `P7_2/3_1` (CoDi), `P7_2/3_2` (DiMo), `P9_6_2` (AforeMóvil/Web) | Secciones 0, 3, 5, 7, 9 | Única fuente con tenencia de smartphone Y uso efectivo de canales digitales de pago/cuenta |
| ENVIPE | No | — | — | Único uso de "internet" es como modalidad del delito sufrido o canal de denuncia (`grep -i "internet\|celular\|smartphone\|banca"` en los 3 PDF); sin variable de tenencia/uso propio |
| ENOE | No | — | — | `grep -i "internet\|celular\|smartphone\|banco\|digital"` sin resultados temáticos en `sdem`/`amp`/`bas`/`con_basedatos`; único hit es "internet" como canal de búsqueda de empleo |
| ENCUCI | Parcial | `AP1_4_11` (internet en vivienda, hogar) + `AP4_4_03/08`, `AP4_6_03/08` (uso de redes/internet como fuente de información) | Tabla VIV p.7; Sección 4.4/4.6, pp.17-18 | Solo tenencia hogar + uso como fuente de información, no exposición/frecuencia individual; sin smartphone propio ni banca en línea |
| ENCIG | Parcial | `P7_3` (modalidad de trámite=Internet, es conducta no acceso) + `P10_1_1..6` (uso de gobierno electrónico) | Pregunta 7.3 pp.49-50; pregunta 10.1 p.34 (2023) | Sin variable de tenencia de internet/dispositivo per se — todo es uso/conducta digital |
| ENSANUT | Parcial | `h0501f`/`h0501g` (celular/internet, binario, nivel hogar) | Cuest. Hogar Sección V, p.16 | Sin uso individual, smartphone específico, ni banca en línea |
| ENUT | Sí (con distinción) | `P2_4_11/12/13` (tenencia hogar: computadora, celular/smartphone, internet) | THOGAR Sección II | Distinto del tiempo dedicado a uso (`P6_22`, `P7_1_8`, otra variable); sin banca en línea |

### 6. Migración (propia, de integrante del hogar, o remesas)

| fuente | sí/no/parcial | variable(s) | página/hoja | nota |
|---|---|---|---|---|
| ENIGH | Parcial | `residencia` (catálogo incl. EUA/otro país) + `remesas` (agregado de clave P041, concentradohogar) | `diccionario_datos_poblacion_enigh2022_ns.csv`; `diccionario_datos_concentradohogar_enigh2022_ns.csv` | El diccionario no trae el texto literal de la pregunta de `residencia`, solo nombre+catálogo — no se pudo confirmar la referencia temporal exacta |
| ENIF | Sí | `P3_15`/`P3_16` (migración propia a 5 años, incl. deportación) + `P7_5`/`P7_6` (remesas, canal) | Sección 3 p.7; Sección 7 p.20 | Dos variables independientes, la más completa del corpus para este eje |
| ENVIPE | No | — | — | `grep -i "migra\|remesa\|extranjero\|otro país\|nació en"` sin resultados; único proxy débil es antigüedad residencial (`AP4_1`), insuficiente |
| ENOE | Sí (parcial en remesas) | Migración propia: `CS_P20A/B/C` (entidad/país/causa hace un año); de integrante: `CS_AD_MOT/DES` (ausente definitivo), `CS_NR_MOT/ORI` (nuevo residente) | `c_sdem_v5a.pdf` preguntas 20a-24, pp.6-9 | **Sin remesas**: `grep -i "remesa"` sin resultados en los 4 archivos ENOE revisados |
| ENCUCI | Parcial | `AP10_2` (vivienda anterior en EUA/otro país) | Pregunta 10.2, pp.52-53 | Solo migración de **retorno propia reciente**, condicionada a mudanza; remesas solo embebidas en el texto de `AP10_14` (eje 4), sin variable propia |
| ENCIG | No | — | — | `grep -i "migra\|remesa\|extranjero\|otro país\|Estados Unidos"` sin resultados en diccionario 2023 (4,462 líneas) ni en cuestionario/estructura 2021 (verificación cruzada) |
| ENSANUT | Parcial | `h0306`/`h0306e/p` (lugar de nacimiento, incl. EUA/otro país) | Cuest. Hogar Sección III, preg. 3.6, p.6 | Solo lugar de nacimiento, no estatus migratorio actual ni remesas (`grep -i "remesa\|migrante\|extranjero"` vacío en 5 cuestionarios + 7 catálogos) |
| ENUT | Parcial | `P3_20_3`/`P3_20_4` (dinero de familiares/amistades en el extranjero / en el país) | THOGAR Sección III, preg. 3.20 | Solo remesas, mezcladas con "amistades"; sin lugar de nacimiento/migración propia ni de integrante ausente |

---

## TABLA B — Reglas del motor (dominio × regla × fuente × variable × página × sí/no/parcial)

*49 reglas, ids de `canon/modelo-decision-v3_4.md` §3.B. Dominios prioritarios
(cobertura CERO en `forense/cobertura-motor.md`) marcados con ⚠️
**PRIORITARIO**, cubiertos con las 8 fuentes completas. El resto,
solo filas con sí/parcial (instrucción del encargo: no inflar la tabla con
"no" en dominios secundarios).*

### ⚠️ PRIORITARIO — §3.2 Trabajo y carrera

| regla (id) | fuente | sí/no/parcial | variable(s) | página | nota |
|---|---|---|---|---|---|
| `trabajo.jerarquia.deferencia_iniciativa_suprimida` | ENIGH | No | — | (poblacion, trabajos revisados) | Sin batería actitudinal de deferencia/jerarquía |
| | ENIF | No | — | Sección 3 completa | Sin reactivo de iniciativa/deferencia laboral |
| | ENVIPE | No | — | — | Sin variable de estilo de liderazgo/jerarquía |
| | ENOE | Parcial (solo predictor) | `P3A` (¿tiene jefe/superior?), `POS_OCU` | `c_amp_v6a.pdf` p.5 | Solo proxy estructural binario, sin deferencia/supresión de iniciativa medida — cuenta como No de desenlace |
| | ENCUCI | No | — | (búsqueda por sección, sin id individual) | ENCUCI no es encuesta laboral |
| | ENCIG | No | — | — | ENCIG no es encuesta laboral |
| | ENSANUT | No | — | — | Sin módulo de empleo/jerarquía |
| | ENUT | No | — | (`grep -in "jefe\|jerarqu\|liderazgo\|supervisor\|deferencia"` sobre `enut2024_fd.txt`, 0 resultados) | Cerrado en esta sesión (hueco de encargo original) |
| `trabajo.liderazgo.benevolencia_legitima` | ENIGH | No | — | trabajos completo | Sin pregunta de satisfacción/percepción del jefe |
| | ENIF | No | — | Sección 3 | — |
| | ENVIPE | No | — | — | — |
| | ENOE | No | — | (`grep -in "satisfec\|liderazgo\|conforme"`, 0 resultados) | — |
| | ENCUCI | No | — | — | — |
| | ENCIG | No | — | — | — |
| | ENSANUT | No | — | — | — |
| | ENUT | No | — | (mismo grep que arriba, 0 resultados) | Cerrado en esta sesión |
| `trabajo.prestaciones.formalidad_pesa_mas_que_salario` | ENIGH | Parcial | `contrato`/`tipocontr`/`pres_1..20` + `sueldos`/`ing_cor` | trabajos + concentradohogar | Ambas variables predictoras existen y son cruzables; sin juicio explícito "pesa más" |
| | ENIF | Parcial | `P3_13` (formalidad) + `P3_11A`/`P3_12` (salario) | Sección 3 p.7 | Mismo límite: predictores sí, trade-off actitudinal no |
| | ENVIPE | No | — | — | Confirmada ausencia de IMSS/Infonavit/prestaciones (eje 1) |
| | ENOE | Parcial | `SEG_SOC`/`EMP_PPAL` + `INGOCUP`/`ING7C` | `con_basedatos_proy2010.pdf` p.22-23 | De las más sólidas del corpus para predictores; sin desenlace de valoración |
| | ENCUCI | No | `POS`/`AP3_14` | pp.11-12 | Solo condición de actividad/prestaciones, sin desenlace de valoración |
| | ENCIG | No | `POS` (proxy indirecto) | p.39 | Sin prestaciones/salario — no permite operacionalizar |
| | ENSANUT | No | `H0310` | p.8 | Sin pregunta de valoración prestaciones-vs-salario |
| | ENUT | No | `P5_6_1..8` + `P5_10` | Sección V | Registra estado actual, no preferencia/trade-off |
| `trabajo.rotacion.joven_urbano_sin_culpa` | ENIGH | No | — | trabajos, poblacion | Sin antigüedad/historial de rotación |
| | ENIF | No | `P3_8`/`P3_9` | Sección 3 | Mide ocupación actual, no rotación |
| | ENVIPE | No | — | — | — |
| | ENOE | Parcial | `P9D` (motivo de separación del trabajo anterior), `P9F_ANIO/MES` | `c_amp_v6a.pdf` p.13 | Permite ver rotación cruzada con edad/urbanización; componente "sin culpa" (actitudinal) no medido |
| | ENCUCI | No | — | — | — |
| | ENCIG | No | — | — | — |
| | ENSANUT | No | — | — | — |
| | ENUT | No | — | (`grep -in "antigüedad\|rotaci\|cambió de trabajo\|cambio de empleo"`, 0 resultados) | Cerrado en esta sesión |

### ⚠️ PRIORITARIO — §3.5 Familia y pareja

| regla (id) | fuente | sí/no/parcial | variable(s) | página | nota |
|---|---|---|---|---|---|
| `familia.seguro.volatilidad_ausencia_estado` | ENIGH | Parcial | `clase_hog` (corresidencia) + `remesas` + `redsoc_1..6` (ambiguo, sin etiqueta clara en diccionario) | concentradohogar, poblacion | Corresidencia y flujo de remesas sí; `redsoc` no confirmable |
| | ENIF | **Sí** | `P9_9_1..6` ("¿con qué piensa cubrir su vejez?": gobierno/pensión/venta de bienes/**familia**/trabajo/otro) + `P7_5`/`P7_6` (remesas) + `P4_4_1`/`P4_9_4` (préstamo de familiares) | Sección 9 p.26; Sección 7 p.20; Sección 4 pp.8-9 | Mejor candidato del corpus: distingue explícitamente familia vs. Estado vs. mercado como fuente de seguridad económica |
| | ENVIPE | No | — | — | — |
| | ENOE | Parcial | `PAR_C` (parentesco) + roster de hogar | `c_sdem_v5a.pdf` pp.3-4 | Estructura/corresidencia estática; sin remesas ni pooling medido |
| | ENCUCI | No | — | — | — |
| | ENCIG | No | — | — | — |
| | ENSANUT | No | — | (roster + `h0327` revisados) | Sin reactivo directo del mecanismo de aseguramiento familiar |
| | ENUT | Parcial (débil) | `P3_20_3`/`P3_20_4` | THOGAR Sección III | Solo flujo monetario, mezclado con amistades; no volatilidad ni ausencia estatal |
| `familia.cuidado.recae_mujeres_40mas` | ENIGH | No | (`hor_1..8` sin etiqueta de actividad en diccionario) | poblacion | No sostenible sin etiqueta |
| | ENIF | No | — | — | ENIF no cubre cuidado de dependientes |
| | ENVIPE | No | — | — | — |
| | ENOE | No | — | (`grep -in "cuidado\|dependiente\|quehacer"`; único hit es prestación laboral "tiempo para cuidados maternos/paternos" del empleador, no variable de cuidado en el hogar) | Cerrado en esta sesión |
| | ENCUCI | No | — | — | — |
| | ENCIG | No | — | — | — |
| | ENSANUT | Parcial | `M0101_id`/`M0103_id` (fila del cuidador/a) cruzable con `h0302`/`h0303` (sexo/edad) del roster | Cuest. Niños 0-9, Sección 1, p.2 | Requiere cruzar dos archivos, no es un reactivo etiquetado único |
| | ENUT | **Sí** | `P6_11_01..14`/`P6_12_01..12`/`P6_13_1..9` (tiempo de cuidado por tramo etario del receptor) + derivadas `CUID_INT_*`, cruzables con `SEXO`/`EDAD` | TMODULO Sección VI; TVAR_CREA | Fuente estándar para esta regla; todos los insumos existen aunque la variable "recae en mujeres 40+" no está pre-construida |
| `familia.union.baja_garantia_institucional` | ENIGH | Parcial/Sí | `edo_conyug` (unión libre / casado / separado / divorciado / viudo / soltero) | poblacion + catálogo | Distingue estructura; el "baja garantía institucional" es interpretación |
| | ENIF | No | — | (`P2_3` parentesco revisado) | Sin estado civil |
| | ENVIPE | No | — | — | Sin estado civil en `tsdem` |
| | ENOE | **Sí** | Pregunta 19 "Situación conyugal": 1 unión libre / 2 separado / 3 divorciado / 4 viudo / 5 casado / 6 soltero | `c_sdem_v5a.pdf` Sección VI, p.4 | Cerrado en esta sesión (hueco de encargo original); distingue explícitamente unión libre de matrimonio |
| | ENCUCI | No | (`AP10_4` estado conyugal, estructural) | p.53 | Solo estructura, no "garantía institucional" |
| | ENCIG | No | — | — | Matrimonio/divorcio solo aparece como tipo de trámite del Registro Civil, no estado civil |
| | ENSANUT | **Sí** | `H0319`: 1 unión libre / 2 separada unión libre / 3 separada matrimonio / 4 divorciado / 5 viudo / 6 casado civil o religiosamente / 7 soltero | Sección III, preg. 3.19, p.10 | Coincide directamente con el constructo |
| | ENUT | **Sí** | `P4_5` (unión libre/separada/divorciada/viuda/casada/soltera) | TMODULO Sección IV, preg. 4.5 | — |
| `familia.cortejo.urbano_joven_apps` | ENIGH | No | — | — | — |
| | ENIF | No | — | — | — |
| | ENVIPE | No | — | — | — |
| | ENOE | No | — | (`grep -in "pareja\|noviazgo\|cortejo"`; único hit es "vive con su pareja" como opción de estado conyugal, no cortejo) | Cerrado en esta sesión |
| | ENCUCI | No | — | — | — |
| | ENCIG | No | — | — | — |
| | ENSANUT | No | — | (`grep -i "app\|red social\|tinder"` en Adolescentes/Adultos, vacío) | — |
| | ENUT | No | — | (Secciones III-VII completas revisadas) | — |

### ⚠️ PRIORITARIO — §3.6 Tiempo y compromiso

| regla (id) | fuente | sí/no/parcial | variable(s) | página | nota |
|---|---|---|---|---|---|
| `tiempo.puntualidad.formal_vs_social` | ENIGH | No | — | poblacion, hogares, trabajos | Solo `htrab` (horas trabajadas), sin puntualidad |
| | ENIF | No | — | Secciones 0-13 | ENIF no tiene módulo de uso del tiempo |
| | ENVIPE | No | — | — | — |
| | ENOE | No | `HRSOCUP`/`P5C`/`P5E` (horario regular sí/no) | dic. `sdem`/`coe1`; `c_bas_v7.pdf` p.8 | Mide horario regular/irregular, no puntualidad ni norma formal/social |
| | ENCUCI | No | — | — | ENCUCI no tiene módulo de uso del tiempo |
| | ENCIG | No | `P7_5A-D` (tiempo de trámite, distinto) | p.51 | Tiempo de procesamiento administrativo, no puntualidad — mantenido estrictamente separado |
| | ENSANUT | No | — | — | — |
| | ENUT | No | (Secc. VI-VII, todo tiempo DEDICADO o percepción de suficiencia, ninguna sobre llegar a tiempo) | — | Distinción explícita: mide tiempo dedicado, no puntualidad |
| `tiempo.compromiso.si_voy_incierto` | ENIGH | No | — | — | — |
| | ENIF | No | — | Secciones 0-13 | — |
| | ENVIPE | No | — | — | — |
| | ENOE | No | — | (`grep -in "compromiso\|asistir\|invitaci"`, 0 resultados) | Cerrado en esta sesión |
| | ENCUCI | No | — | — | — |
| | ENCIG | No | — | — | — |
| | ENSANUT | No | — | — | — |
| | ENUT | No | — | Secc. VII (única actitudinal) | — |
| `tiempo.bomberazo.recursos_escasos_urgencias` | ENIGH | No | — | — | — |
| | ENIF | No | — | — | — |
| | ENVIPE | No | — | — | — |
| | ENOE | No | — | (`grep -in "urgenc\|imprevist\|bomberazo"`, 0 resultados) | Cerrado en esta sesión |
| | ENCUCI | No | — | — | — |
| | ENCIG | No | (`N_TRA`=08 "urgencia médica" solo como categoría de trámite) | p.40 | No es conducta de improvisación/urgencia |
| | ENSANUT | No | — | (`H0409` "urgencias" es tipo de servicio de salud usado, no gestión del tiempo) | — |
| | ENUT | No | — | Secc. VI-VII | — |
| `tiempo.cumplimiento.recordatorio_baja_barrera` | ENIGH | No | — | — | — |
| | ENIF | No | — | — | — |
| | ENVIPE | No | — | — | — |
| | ENOE | No | — | (`grep -in "recordator\|cita medic"`, 0 resultados) | Cerrado en esta sesión |
| | ENCUCI | No | — | — | — |
| | ENCIG | No | — | — | — |
| | ENSANUT | No | — | — | — |
| | ENUT | No | — | — | — |

### ⚠️ PRIORITARIO — §3.8 Cooperación y bienes públicos

| regla (id) | fuente | sí/no/parcial | variable(s) | página | nota |
|---|---|---|---|---|---|
| `cooperacion.comite.monitoreo_sancion_visible` | ENIGH | No | — | — | — |
| | ENIF | No | — | Secciones 5-6 | Sin monitoreo/sanción en cajas/tandas |
| | ENVIPE | No (tangencial) | `AP4_9_1..6` ("¿se organizaron los vecinos para resolver...?") | preg. 4.9 | Percepción binaria de organización vecinal, sin monitoreo/sanción propios ni participación del entrevistado |
| | ENOE | No | — | (`grep -in "comité\|vecinal\|faena\|cooperativa\|voluntari"`, sin resultados temáticos) | Cerrado en esta sesión |
| | ENCUCI | Parcial | `AP6_2_12`/`AP6_3_12` (organización vecinal), `AP7_2_3/4` (frecuencia de reunión para servicios/vigilancia), `AP7_7_5/6` (motivos de no participación: desconfianza, "no son efectivos") | pp.36-39, 43 | Hay participación y razones de no-participación, pero ninguna distingue monitoreo/sanción visible del comité |
| | ENCIG | No | — | — | Sin módulo de participación vecinal |
| | ENSANUT | No | — | — | Único acercamiento es receptor pasivo de programas sociales |
| | ENUT | Parcial (débil) | `P6_17_2` (voluntariado institucional: Cruz Roja, DIF, iglesias, partidos) | Secc. VI, preg. 6.17 | Tiempo en voluntariado formal, sin componente de monitoreo/sanción |
| `cooperacion.tanda.conoce_organizadora` | ENIGH | No | `Q001` (tanda mezclada con depósitos bancarios/cajas de ahorro, sin aislar) | catálogo `producto.csv` | — |
| | ENIF | Parcial | `P5_1_5` (participó en tanda, sí/no) | Sección 5, p.11 | Existe participación; sin seguimiento sobre conocer a la organizadora |
| | ENVIPE | No | — | — | — |
| | ENOE | No | — | — | — |
| | ENCUCI | No | (`AP6_9`/`AP6_10` "tandas para el bienestar" = programa social gubernamental, no tanda financiera) | pp.37-38 | Falso amigo terminológico |
| | ENCIG | No | — | — | — |
| | ENSANUT | No | — | — | — |
| | ENUT | No | — | — | — |
| `cooperacion.confianza.puente_personal` | ENIGH | No | — | — | — |
| | ENIF | Parcial | `P6_1A_3/4/5` (cobro de interés entre familiares/amistades/otro, proxy indirecto) + `P5_1_3/4` (caja de ahorro/guardado con conocidos) | Sección 6, p.16; Sección 5, p.11 | Proxy indirecto vía cobro/no cobro de interés; sin confianza declarada directa |
| | ENVIPE | No (no equivalente) | `AP5_2_1..4` (confianza en vecinos/compañeros/familiares/amigos) | Sección 5.2 | Confianza generalizada por vínculo, no el mecanismo de puente hacia un desconocido |
| | ENOE | No | — | — | — |
| | ENCUCI | **Sí** | `AP5_1_1` (confianza en la mayoría de las personas) / `AP5_1_2` (personas que conoce personalmente — puente) / `AP5_1_3` (vecinos/localidad) | Sección 5.1, pp.21-22 | Distingue explícitamente confianza generalizada de confianza con vínculo personal conocido |
| | ENCIG | No (no equivalente) | (batería XI de confianza institucional, distinta) | Sección XI, p.62 | Confianza en instituciones formales, no confianza personal entre pares |
| | ENSANUT | No | — | — | — |
| | ENUT | No | — | — | — |
| `cooperacion.faena.sancion_social_pueblo_mestizo` | ENIGH | No | — | — | — |
| | ENIF | No | — | — | — |
| | ENVIPE | No | — | — | — |
| | ENOE | No | — | — | — |
| | ENCUCI | No (no equivalente) | `AP7_1` (trabajo voluntario/comunidad, explícitamente sin retribución) | p.38 | Sin norma de faena obligatoria ni sanción social; `grep "faena\|tequio"` sin resultados |
| | ENCIG | No | — | — | — |
| | ENSANUT | No | — | — | — |
| | ENUT | Parcial | `P6_17_3` ("tequio, faena, mano vuelta, mayordomía...") + derivada `TRAB_NO_REM_NO_FAM` | Secc. VI, preg. 6.17 | Mide tiempo dedicado al catálogo exacto de actividad tradicional; sin componente de sanción social |

### ⚠️ PRIORITARIO — §3.10 Comunicación y conflicto

| regla (id) | fuente | sí/no/parcial | variable(s) | página | nota |
|---|---|---|---|---|---|
| `comunicacion.rechazo.indirecto_face` | ENIGH | No | — | — | — |
| | ENIF | No | — | Secciones 0-13 | — |
| | ENVIPE | No | — | — | — |
| | ENOE | No | — | (`grep -in "rechaz\|retroaliment\|conflicto\|desacuerdo"`, sin resultados temáticos) | Cerrado en esta sesión |
| | ENCUCI | No | — | — | — |
| | ENCIG | No | — | — | — |
| | ENSANUT | No | — | — | — |
| | ENUT | No | — | — | — |
| `comunicacion.retroalimentacion.privada_publica_capital_social` | ENIGH | No | — | — | — |
| | ENIF | No | — | — | — |
| | ENVIPE | No (no equivalente) | `P10_1_4` (uso de redes sociales para queja/denuncia a gobierno) | preg. 10.1 | Canal de queja hacia el gobierno, no retroalimentación interpersonal/capital social |
| | ENOE | No (tangencial) | (`08 "Conflicto con su jefe o superior"` como motivo de separación del trabajo) | `c_amp_v6a.pdf` | Código de motivo, no constructo de retroalimentación |
| | ENCUCI | No | — | — | — |
| | ENCIG | No (no equivalente) | `P10_1_4` (redes sociales para queja a gobierno) | p.34 | Mismo límite que ENVIPE |
| | ENSANUT | No | — | — | — |
| | ENUT | No | (`P6_21_1` tiempo platicando con integrantes del hogar — tiempo, no desenlace) | Secc. VI | — |
| `comunicacion.inseguridad.ver_oir_callar` | ENIGH | No | — | — | — |
| | ENIF | No | — | — | — |
| | ENVIPE | Parcial | `BP1_23` códigos 01 "miedo al agresor" y 06 "desconfianza en la autoridad" (razón de no denunciar) | Cuest. módulo, preg. 1.23, p.4 | Cubre "callar" como no-denuncia tras ser víctima directa; no cubre silencio ante delito ajeno presenciado |
| | ENOE | No | — | — | — |
| | ENCUCI | No | — | — | — |
| | ENCIG | No | — | — | — |
| | ENSANUT | No | — | (módulo de violencia en Adolescentes revisado, sin norma de "ver/oír/callar") | — |
| | ENUT | No | — | — | — |
| `comunicacion.directividad.regional_generacional` | ENIGH | No | — | — | — |
| | ENIF | No | — | — | — |
| | ENVIPE | No | — | — | — |
| | ENOE | No | — | — | — |
| | ENCUCI | No | — | — | — |
| | ENCIG | No | — | — | — |
| | ENSANUT | No | — | — | — |
| | ENUT | No | — | — | — |

### Resto de dominios (§3.1, §3.3, §3.4, §3.7, §3.9) — solo sí/parcial

**§3.1 Dinero, ahorro, crédito y consumo**

| regla (id) | fuente | sí/no/parcial | variable(s) | página |
|---|---|---|---|---|
| `dinero.ahorro.volatilidad_horizonte_corto` | ENIF | Sí | `P4_10` (¿por cuánto tiempo cubriría gastos con ahorros si dejara de recibir ingreso?) | Sección 4, p.9 |
| `dinero.planeacion.formal_estable` | ENIGH | Parcial | `pres_8` (AFORE/SAR), `segvol_1`, `N008`/`N009` (seguros) | trabajos, poblacion |
| | ENIF | Sí | `P9_1`/`P9_1A` (Afore/SAR) + `P8_5_1..8` (tenencia de seguros) | Sección 9 pp.22-24; Sección 8 |
| `dinero.ahorro.informal_sin_puente` + `con_puente_y_respaldo` | ENIGH | Parcial | `Q001`/`P051` (tanda/caja mezclada con depósitos bancarios) | erogaciones, ingresos |
| | ENIF | Parcial | `P5_1_3/4/5` (canal informal) + `P6_1A_3/4/5` (cobro de interés, proxy de "puente") | Sección 5 p.11; Sección 6 p.16 |
| `dinero.consumo.estatus_mediado_por_credito` | ENIGH | Sí | `tarjeta`/`pagotarjet` + módulo `gastotarjetas` (TB/TR por categoría) | `diccionario_datos_gastotarjetas_enigh2022_ns.csv` |
| `dinero.ahorro.seguro_deposito_atenua_aversion` | ENIF | Sí | `P5_23`/`P5_24_1..6` (conocimiento de protección de ahorros/IPAB) | Sección 5, pp.15-16 |
| `dinero.credito.baja_friccion_usura_dano_downstream` | ENIF | Sí | `P6_3_1..9` (atraso de pago por tipo de crédito) | Sección 6, p.17 |

**§3.3 Autoridad, trámite y relación con el Estado**

| regla (id) | fuente | sí/no/parcial | variable(s) | página |
|---|---|---|---|---|
| `tramite.mordida.discrecional` | ENCUCI | Sí | `AP5_17`/`AP5_18` (¿le pidieron / tuvo que dar dádiva/favor/dinero extra en un trámite?), contextualizado por `AP5_16_1..10` | Sección 5.16-5.18, pp.30-32 |
| | ENCIG | Sí | `P8_3_1/2/3` (apropiación directa, insinuación de tercero, funcionario genera condición) | Pregunta 8.3, p.32 (2023) |
| | ENVIPE | No | `AP5_5_01..11` (percepción de corrupción "a su juicio", no experiencia) | preg. 5.5 |
| `tramite.mordida.con_registro` | ENCIG | Sí (estructural) | `P7_3` (modalidad del trámite) cruzable con `P8_4-P8_7` (apropiación en ese trámite) vía llave `N_TRA` | pp.49-50, 57-58 (2023) |
| `tramite.gobierno_digital.coercitivo` + `util_sin_coercion` | ENIF | Parcial | `P7_2/3_1` (CoDi), `P7_2/3_2` (DiMo) — conocimiento/uso, sin distinguir coerción/utilidad | Sección 7, p.20 |
| | ENCIG | Sí (adopción) / falta motivo | `P7_3`=Internet + `P10_1_2/3/5` (llenó/pagó/completó trámite en línea) | pp.49-50, 34 (2023) |

**§3.4 Salud y cuerpo**

| regla (id) | fuente | sí/no/parcial | variable(s) | página |
|---|---|---|---|---|
| `salud.atencion.leve_sin_imss` | ENSANUT | Parcial | `H0310` (derechohabiencia) + `H0408` (institución) + `H0409A-D` (tipo de servicio=consulta externa) | Sección IV, pp.8, 15 |
| `salud.atencion.grave` | ENSANUT | Parcial | `H0409A-D` (código 2 hospitalización / 3 urgencias) | Sección IV, p.15 |
| `salud.adherencia.desabasto_vs_cuidadora` | ENIGH | Parcial | `noatenc_9` ("no le dan el medicamento que necesita") | catálogo `noatenc.csv` |
| | ENSANUT | Parcial | `A0314` código 05 ("no le surtieron los medicamentos") — específico del módulo diabetes | Sección III, preg. 3.14, p.6 |

**§3.7 Cívico y participación**

| regla (id) | fuente | sí/no/parcial | variable(s) | página |
|---|---|---|---|---|
| `civico.denuncia.sin_seguro` + `con_seguro` | ENVIPE | **Sí** | `BP1_20` (¿denunció?) + `BP1_23` (razón de no denunciar, incl. miedo/desconfianza) + `BP2_1` (vehículo asegurado) + `BP1_28` (razón de sí denunciar, incl. "por el seguro") | preg. 1.20/1.23/1.28/2.1, pp.4-6 |
| `civico.participacion.contingente` | ENCUCI | Sí | `AP7_9` (votó 2018), `AP7_8` (credencial vigente), `AP7_11` (funcionario de casilla) | Sección 6-7, p.44 |
| `civico.voto.agencia_con_secreto` | ENCUCI | Sí | `AP7_13`/`AP7_13A`/`AP7_14`/`AP7_15` (simpatía partidista, secrecía del voto) | pp.44-45 |
| `civico.voto.clientelar_si_observable` | ENCUCI | Sí | `AP7_13`/`AP7_13A`/`AP7_14`/`AP7_15` (simpatía partidista, secrecía del voto) | pp.44-45 |
| `civico.protesta.agravio_urbano` | ENCUCI | Parcial | `AP7_3_5/6`/`AP7_4_5/6` (protesta, bloqueo de vías) | pp.40-41 |
| `civico.transferencia.entitlement_derecho` | ENIGH | Parcial | `bene_gob` (agregado de claves de programas: Beca Benito Juárez, Pensión Bienestar, etc.) | concentradohogar |
| | ENIF | Parcial | `P3_4` (recibe apoyo/programa de gobierno) + `P9_9_1` (piensa cubrir vejez con apoyo de gobierno) | Sección 3 p.5; Sección 9 p.26 |
| `civico.transferencia.atribucion_lider` | ENIGH | Parcial | `bene_gob` (agregado de claves de programas: Beca Benito Juárez, Pensión Bienestar, etc.) | concentradohogar |
| | ENIF | Parcial | `P3_4` (recibe apoyo/programa de gobierno) + `P9_9_1` (piensa cubrir vejez con apoyo de gobierno) | Sección 3 p.5; Sección 9 p.26 |

**§3.9 Información y creencia**

| regla (id) | fuente | sí/no/parcial | variable(s) | página |
|---|---|---|---|---|
| `informacion.deferencia.costo_acceso_experto` | ENIF | Sí | `P5_15_5`/`P6_11_5`/`P8_12_5` (comparó producto con "recomendación de especialistas/analistas", dentro de batería con recomendación de conocidos, publicidad, comparadores) | Secciones 5, 6, 8 |
| `salud.vacunacion.disponible` ⚠️ *id con dominio equivocado, ver `forense/hallazgos.md`* | ENSANUT | Sí | Esquema de vacunación (`m0511-m0526`, `D05xx`, preg. 9.1-9.13) + motivo de indisponibilidad (`m0535a_1`) | Niños 0-9 Secc. 5 p.14+; Adolescentes Secc. 5 p.19; Adultos Secc. IX p.18 |

---

## Límite declarado

- **ENCIG 2023 sin cuestionario en papel independiente**: la edición 2023
  reemplaza el cuestionario impreso por un diccionario de datos por tabla
  con columna "Pregunta" (texto literal inline) — se usó como fuente
  principal; 2021 solo para verificación cruzada de ausencias
  (migración, prestaciones laborales), confirmando el mismo resultado.
- **ENOE y ENUT — huecos de encargo cerrados en esta misma sesión** (ver
  arriba, filas marcadas "Cerrado en esta sesión" y línea de
  `forense/hallazgos.md`): los subagentes de estas dos fuentes no
  recibieron inicialmente los ids exactos de un subconjunto de reglas
  prioritarias. Se completó con `grep`/`pdftotext` directo sobre los
  mismos archivos ya localizados, no con una segunda ronda de subagentes.
- **ENIGH 2022 es la edición más reciente en disco** — no hay ENIGH 2024
  en `data/raw`.
- **ENCUCI 2020 es la única edición existente** en disco y, según el
  catálogo de fuentes, la única edición realizada hasta la fecha.
- Todas las afirmaciones de ausencia ("No") citan el comando/lectura
  literal que las sostiene (ADR-38), reportado por cada subagente o por
  esta sesión en el cierre de huecos — no se listó el comando exacto en
  cada celda de la tabla por espacio, pero está documentado en el reporte
  de cada subagente (transcripciones no incluidas en el repo).
