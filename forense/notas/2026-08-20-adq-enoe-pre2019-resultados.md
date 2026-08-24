# ADQ-ENOE-PRE2019 · COMMIT B — resultados del barrido

*20 de agosto de 2026 · `ACTO ADQ-ENOE-PRE2019`, T2 · especificación en `bbis-adq-enoe-pre2019` (COMMIT A, congelado antes de bajar nada)*

---

## VEREDICTO

> **Desenlace 2 de `bbis-adq-enoe-pre2019` §6: las 14 filas salen `EXISTE-NO-SATISFACE` o `NO-ENCONTRADO`. Cero `EXISTE-SATISFACE`.** La Razón 1 de `FP-64` se extiende del instrumento moderno al pre-2019 completo, y esta vez con una evidencia que `FP-64` no tenía: **de las 553 variables que las olas pre-2019 traen, cero faltan en las 29 olas post-2019 que ya estaban en disco.** No es que el barrido no las encontrara — es que **no existen**: la ENOE sólo ganó variables entre eras, nunca perdió ninguna.

**La hipótesis del encargo, contestada por conjunto y no por muestreo.** El encargo dice *«puede que las olas viejas sí traigan lo que las nuevas no»*. Esa frase es una afirmación de **diferencia de conjuntos**, y se contesta con la diferencia de conjuntos, no con un léxico. Corrida sobre el inventario **completo** de variables de seis olas-sonda que cubren toda la vida de la encuesta y sus dos eras de instrumento:

| ola-sonda | era de instrumento | variables (5 tablas) | ausentes de las 29 olas post-2019 |
|---|---|---:|---:|
| `2005T1` | `14ymas` | 466 | **0** |
| `2008T1` | `14ymas` | 394 | **0** |
| `2012T1` | `14ymas` | 466 | **0** |
| `2014T1` | `15ymas` | 466 | **0** |
| `2016T1` | `15ymas` | 466 | **0** |
| `2018T4` | `15ymas` | 394 | **0** |

*(Derivado: `python3 tools/barrido_enoe_constructos.py` → `data/barrido-enoe-sonda-eras.tsv`. Las olas de 466 son las de cuestionario **ampliado** (T1 de cada año) y las de 394 las de **básico**; la unión de las 12 olas adquiridas da 553 variables, y `SOLO_PRE = 0` contra la unión de las 29 post.)*

---

## 1 · Universo A · los cuestionarios y descriptores — `A.13` con la cardinalidad al frente

**16 PDF · 5,021,037 caracteres examinados · dos extractores independientes.**

| bloque | archivos | qué es |
|---|---|---|
| los 6 cuestionarios ya en disco | `c_amp_v5`, `c_amp_v6a`, `c_bas_v5`, `c_bas_v7`, `c_sdem_v4`, `c_sdem_v5a` | el universo que `CAL-ENOE Fase A` leyó el 31/jul/2026 |
| 7 descriptores era `14ymas` | `fd_c_amp_v1`…`v4`, `fd_c_bas_v1`, `fd_c_bas_v2`, `fd_c_bas_amp_conapo` | **nunca abiertos por ningún acto anterior**; `fd_c_amp_v1` cubre los trimestres 105-206, `fd_c_bas_v1` los 306-107 |
| 3 descriptores era `15ymas` | `fd_c_bas_amp_15ymas`, `enoe_123_fd_c_bas_amp`, `enoe_325_fd_c_bas_amp` | estructura de la base de datos de la era moderna |

**El método reproduce el anterior, verificado y no supuesto.** `data/coef-universo-v1_0.tsv:14` declara que el barrido moderno extrajo *«6408 a 35733 caracteres cada uno»* con `pypdf`. Corrido `pypdf` aquí sobre esos mismos 6 PDF: `c_sdem_v4` = **6,408**, `c_amp_v5` = **35,733**. Los dos extremos coinciden al carácter, así que este barrido corre sobre el mismo método y no sobre uno más flojo.

**Y lo mejora, con una consecuencia que hay que decir.** `pdftotext -layout` ve ~3× más texto que `pypdf` en los mismos archivos (111,288 vs 35,733 en `c_amp_v5`). Este barrido usa la **unión** de los dos. **Consecuencia sobre el hallazgo anterior:** el `NO-ENCONTRADO` de `coef-universo` se produjo sobre aproximadamente un tercio del texto que su propio PDF contenía. No lo refuta —este barrido, con el triple de texto, llega al mismo sitio— pero un negativo derivado de un extractor que ve un tercio del documento no era, en el momento en que se escribió, un negativo tan fuerte como parecía.

**118 términos pre-registrados; 76 con CERO aciertos en los 16 PDF.** Los que nombran el constructo de frente están todos en el grupo de cero: `confia`, `confianza`, `planea`, `planific`, `prevision`, `proyecto de vida`, `estatus`, `posicion social`, `prestigio`, `clase social`, `nivel socioeconomico`, `obedec`, `jerarqui`, `acatar`, `sumis`, `incertidumbre`, `apost`, `azar`, `loteria`, `garantizado`, `preferiria`, `victima`, `amenaza`, `denuncia`, `manutencion`, `red de apoyo`. Una fila entera —`confianza_institucional[justicia-policía]`— sale con **6 de 6 términos en cero**.

### 1.1 · Adjudicación de las 14 filas, cada acierto contra el reactivo en que vive

| # | fila | veredicto `A.4` | el acierto, y por qué no es exposición |
|---|---|---|---|
| 1 | `aversion_riesgo` | `EXISTE-NO-SATISFACE` | `riesgo` sólo vive en *«04 el trabajo era riesgoso y/o insalubre»* — motivo de dejar un empleo. `seguro de` es *«seguro de vida / de desempleo / de separación individual»*, la batería `P3M` de **prestaciones que otorga el patrón** |
| 2 | `ci[seguridad]` | `EXISTE-NO-SATISFACE` | `seguridad publica` sólo dentro de `inseguridad publica`, como *«problemas de inseguridad pública»* que dificultan un negocio. `policia`, `ejercito`, `marina`, `guardia nacional`: **cero** |
| 3 | `ci[educacion]` | `EXISTE-NO-SATISFACE` | `escuela` es tipo de **empleador** (*«escuela, hospital, clínica o institución asistencial»*). `sep` es `septiembre`/`separado`/`separarse` — falso positivo de subcadena |
| 4 | `ci[salud]` | `EXISTE-NO-SATISFACE` | `imss`/`issste`/`hospital`/`clinica` son **a qué institución está afiliado** o **tipo de empleador**; nunca *«¿qué tanto confía en…?»* |
| 5 | `ci[electoral]` | `EXISTE-NO-SATISFACE` | `ine` es `INEGI` y `eleccion` es `seleccionada` — los 1,181 y 202 aciertos son subcadena, cero sustantivos. `voto`, `campana electoral`: **cero** |
| 6 | `ci[justicia-policia]` | `NO-ENCONTRADO` | **6 de 6 términos en cero** sobre 16 PDF y 5,021,037 caracteres |
| 7 | `ci[financiera]` | `EXISTE-NO-SATISFACE` | `banca` es *«cadena comercial, bancaria o de servicios»*, tipo de unidad económica. `afore`/`caja de ahorro` son opciones `P3M4`/`P3M7`, prestaciones |
| 8 | `deferencia` | `EXISTE-NO-SATISFACE` | `jefe` es *«¿en su trabajo tiene un jefe(a) o superior?»* (estructura de supervisión) y *«conflicto con su jefe»* (motivo de renuncia). `autoridad` es boilerplate del Art. 45 de la Ley del SNIEG más *«problemas con las autoridades (extorsión, multa)»* |
| 9 | `exposicion_violencia` | `EXISTE-NO-SATISFACE` | el único acierto sustantivo es *«07 por violencia (entre vecinos, comunidad, intrafamiliar)»* — **categoría dentro del motivo de migración**, universo restringido a quien se mudó. Reproduce exacto lo que `coef-universo` ya había adjudicado |
| 10 | `familismo_apoyo` | `EXISTE-NO-SATISFACE` | `familiar` es *«pidió a conocidos o familiares»* (método de búsqueda de empleo), *«no lo(a) deja un familiar»* (motivo de no trabajar) y *«de un familiar o de otra persona»* (quién lo sostuvo). `presta` es `prestaciones`. `remesa`, `red de apoyo`, `pariente`: **cero** |
| 11 | `familismo_obligacion` | `EXISTE-NO-SATISFACE` | `obligacion` sólo en *«sin interés por trabajar por atender otras obligaciones»* — una **clase de la población no económicamente activa**, no una batería de deber familiar |
| 12 | `horizonte_temporal` | `EXISTE-NO-SATISFACE` | **los 16 aciertos de `ahorr`, en los 16 PDF y en las dos eras, son el mismo reactivo**: `P3M7`, *«opción 7: préstamos personales y/o caja de ahorro?»*. `afore`/`retiro` son `P3M4`, *«fondo de retiro (SAR o AFORE)?»*. `futuro` es *«Jóvenes Construyendo el Futuro»*, nombre de programa. `plazo`, `planea`, `planific`, `prevision`, `meta`: **cero** |
| 13 | `radio_confianza` | `EXISTE-NO-SATISFACE` | `comunidad` es *«prestar servicios gratuitos a su comunidad?»* — trabajo no remunerado, conducta, no radio de confianza. `vecino` es la misma categoría de motivo de migración de la fila 9. **`confia` y `confianza`: cero aciertos en 5,021,037 caracteres** |
| 14 | `sens_estatus` | `EXISTE-NO-SATISFACE` | `pena` es `desempeña`/`empeñar` — subcadena. `empeñar sus bienes` es real pero es **conducta de sostenimiento**, un desenlace. Los 9 términos restantes: **cero** |

---

## 2 · Universo B · el inventario de variables — la evidencia que `FP-64` no corrió

**553 variables pre-2019 (12 olas, 5 tablas) contra 628 post-2019 (29 olas).** `SOLO_PRE = 0` · `SOLO_POST = 75` · `AMBAS = 553`.

Las 75 que la era post **añade** son casi todas de diseño y administración: `CVEGEO`, `CVE_ENT`, `CVE_MUN`, `CVE_AGEB`, `CVE_LOC`, `FAC_MEN`, `FAC_TRI`, `EST_D_MEN`, `EST_D_TRI`, `MES_CAL`, `TIPO`, `TIPOLEV`, `T_LOC_MEN`, `T_LOC_TRI`, `CA`. Las sustantivas son `P6E`…`P6I` en `COE2` y `CS_P20A`/`CS_P20B`/`CS_P20C`/`CS_P21_DES`/`CS_P23_DES` en `SDEM` — ocupación y escolaridad, ninguna de los 9 constructos.

### 2.1 · Y la parte útil: el antes/después **sí** se puede construir

El barrido cierra la puerta de la exposición θ, pero la adquisición no fue en balde y esto es lo que la sostiene. Las claves que un DiD por franja fronteriza necesita están **en las dos eras**:

| lo que hace falta | variable | pre-2019 | post-2019 |
|---|---|---|---|
| asignar tratamiento (municipio fronterizo) | `ENT` + `MUN` (en `HOG`/`SDEM`/`VIV`) | **sí** | **sí** |
| ponderar | `FAC` | **sí** | **sí** |
| varianza con diseño complejo | `UPM`, `EST_D` | **sí** | **sí** |
| estrato urbano/rural | `T_LOC` | **sí** | **sí** |

⚠️ **Dos advertencias para quien escriba el diseño, medidas aquí:** (1) `MUN` **no** está en `COE1`/`COE2` — hay que traerlo por la llave de hogar desde `SDEM`/`HOG`. (2) el post-2019 añade `FAC_TRI` y `FAC_MEN` **junto a** `FAC`; usar el mismo nombre de ponderador en las dos eras no garantiza que sea el mismo objeto, y eso se verifica antes de estimar, no después.

---

## 3 · El puente de distribución — la costura, medida

`bbis-adq-enoe-pre2019` §2 prometió medir la comparabilidad pre↔post en vez de afirmarla, bajando `2018T4` por las **dos** rutas de INEGI. Resultado sobre la misma ola:

| tabla | variables | filas | contenido (`sha256` del CSV) |
|---|---|---|---|
| `COE1` | 169 = 169 | 309,051 = 309,051 | **byte-idéntico** |
| `COE2` | 70 = 70 | 309,051 = 309,051 | **byte-idéntico** |
| `HOG` | 31 = 31 | 123,292 = 123,292 | **byte-idéntico** |
| `SDEM` | 104 = 104 | 390,612 = 390,612 | **DIFIERE** |
| `VIV` | 20 = 20 | 122,578 = 122,578 | **byte-idéntico** |

**El `DIFIERE` de `SDEM` no es formato — es dato que falta.** Diagnosticado campo por campo tras normalizar BOM y espacios:

- **`cs_p14_c` (*«Pregunta 14 Clave de la carrera»*, catálogo de carreras): `/microdatos/` trae 71,516 valores no vacíos, `/datosabiertos/` trae 70,188.** `/datosabiertos/` **pierde 1,328**, todos del bloque `N12x` (`N120`×700, `N122`×560, `N121`×53, `N123`×12, `N126`×3), y **no gana ninguno** en la otra dirección.
- **3 campos de texto libre truncados** en `/datosabiertos/` (`cs_p20_des`, `cs_nr_ori`), un carácter menos cada uno.

**Las dos rutas de INEGI para la misma ola de la ENOE no son intercambiables.** Vindica, por medición y no por corazonada, la decisión de `bbis-adq-enoe-pre2019` §2 de adquirir el período pre **uniformemente por una sola ruta**; y deja escrito que mezclarlas en un panel de olas mete una discontinuidad en `cs_p14_c` que ningún test del proyecto vigila hoy.

---

## 4 · Lo que este acto NO concluye — los cuatro límites de `bbis-adq-enoe-pre2019` §7, contestados

1. **El `NO-ENCONTRADO` no prueba que la ENOE nunca lo midió.** Sigue en pie, y ahora está **acotado**: la ENOE ha tenido módulos temáticos anexos que no viajan en el ZIP trimestral, y este barrido no los cubre. Hueco nombrado, no cerrado.
2. **Adquirir no es diseñar.** Ninguna fila del registro de llaves nace en este acto. El contador queda `2 de 3`.
3. **El decreto no se verificó aquí.** No se leyó el `DOF`, no se derivaron los municipios de la franja, no se fijó el grupo de tratamiento (§2.1 dice sólo que las **claves** para hacerlo existen).
4. **El barrido no midió potencia.** Nada dice sobre si el `n` por municipio fronterizo sostiene un DiD.
