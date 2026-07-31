# CAL-ENOE · Fase A — ¿puede la ENOE calibrar `horizonte_temporal`?

*31 de julio de 2026 · Fase A, solo documentación · ningún microdato abierto*

---

## VEREDICTO

> **ENOE NO puede calibrar `horizonte_temporal`: el instrumento no contiene desenlace.** Los **nueve** cuestionarios que cubren sin hueco los 28 trimestres no traen una sola pregunta sobre ahorro, crédito, deuda, planeación o expectativas del informante; lo más cercano —la batería `3m` del cuestionario ampliado— mide **prestaciones que otorga el patrón** ("¿a … le dan, **aunque no utilice**…?"), no conducta del sujeto, y además es casi colineal con la exposición. La compuerta 1 no pasa, y las compuertas 2, 3 y 4 no se evalúan porque son condicionales a ella.

**Consecuencia, con una precisión que importa.** `milpa/procedencia.yaml:282-288` (`asignados_coeficiente.unico_calibrable_hoy`) contiene dos afirmaciones, y **no corren la misma suerte**:

1. *"El panel rotativo trimestral de la ENOE sigue al mismo hogar cinco trimestres"* — **VERIFICADA**. `enoe_n_manual_entrevistador.pdf` p. 15: *"El diseño de la encuesta es de panel rotatorio, la muestra está dividida en cinco paneles y cada uno permanece en la muestra durante cinco trimestres… La quinta parte de la muestra que ya cumplió con su ciclo de cinco visitas se reemplaza cada tres meses."*
2. *"…y estimar el cambio de **conducta financiera** asociado"* — **FALSA a nivel de reactivo**. Es la que muere aquí, y es la que sostenía la calificación de "única elasticidad calibrable con dato público".

`procedencia.yaml` NO se toca en esta nota: la corrección y su cascada son decisión de mesa.

**Esto no es CAL-G3.** CAL-G3 (`forense/hitoD-preregistro-v2_0.md` Nota 7, Adenda 1, Notas 8-10) está sellada, su alcance era ENNViH olas 2-3 y su resultado está en la Nota 10. No se enmienda, no se reabre, no se vuelve a correr. Por **ADR-47** (`canon/gobernanza-v1_15.md:388`) CAL-ENOE es **calibración, no falsación**: no emite `CAL-A/B/C/X` y no entra al conteo de corridas archivadas del Hito D.

---

## 1 · ¿Existe el desenlace? — **NO. La compuerta mata el ejercicio.**

### Qué se leyó

**Nueve cuestionarios, 103 páginas de instrumento, que cubren SIN HUECO los 28 trimestres** (2019T1-2026T1, sin 2020T2), con `sha256` verificado uno por uno antes de leerlos — **9/9 coinciden**:

| archivo | tipo | pág | cobertura | procedencia |
|---|---|---:|---|---|
| `c_bas_v5` | básico | 12 | trim. 2-3-4 de 2016-2019 | manifiesto |
| `c_bas_v7` | básico | 11 | trim. 2-3-4 de 2023-2025 | manifiesto |
| `c_amp_v5` | ampliado | 15 | trim. 1 de cada año 2016-2020 | manifiesto |
| `c_amp_v6a` | ampliado | 14 | trim. 1 de cada año 2023-2026 | manifiesto |
| `c_sdem_v4` | sociodemográfico | 2 | trim. 2 de 2016 a trim. 1 de 2020 | manifiesto |
| `c_sdem_v5a` | sociodemográfico | 10 | a partir de trim. 1 de 2023 | manifiesto |
| `c_bas_v6` | básico | 13 | **ENOEN** · trim. 3-4 de 2021 y 2-3-4 de 2022 | dentro del ZIP |
| `c_amp_v6` | ampliado | 15 | **ENOEN** · trim. 1 de 2022 | dentro del ZIP |
| `c_sdem_v5` | sociodemográfico | 11 | **ENOEN** · trim. 3 de 2021 al 4 de 2022 | dentro del ZIP |

Los seis primeros están registrados individualmente en `data/manifiesto.yaml`. Los tres últimos viajan dentro de `enoe_n_trim3_2020-trim4_2022.zip`, cuyo `sha256` sí está registrado (`enoen_trim3_2020_trim4_2022_documentacion_zip`) y se verificó también. **Ese ZIP resultó ser 100 % documental** —101 PDF, cero microdatos, cero `conjunto_de_datos_*`— y trae seis cuestionarios; tres de ellos (`c_amp_v5`, `c_bas_v5`, `c_sdem_v4`) son **byte-idénticos** a los ya bajados sueltos, mismo `sha256`. Por eso la era ENOEN aporta exactamente tres instrumentos nuevos y ninguno más.

### El censo de secciones — ninguna es de finanzas del hogar

Encabezados en romanos, transcritos del instrumento:

- **Básico** (v5, v6, v7) — I. Condición de ocupación · II. No ocupados · III. Contexto laboral · IV. Características de la unidad económica · V. Jornada y regularidad laboral · VI. Ingresos y atención médica · VII. Trabajo secundario · VIII. Búsqueda de otro trabajo · IX. Otras actividades.
- **Ampliado** (v5, v6, v6a) — las mismas, más **IX. Antecedentes laborales · X. Apoyos económicos · XI. Otras actividades**.
- **Sociodemográfico** (v4, v5, v5a) — identificación geográfica · resultado de la entrevista · datos del personal operativo · supervisión · residentes de la vivienda · **VI. Características sociodemográficas** · ausentes definitivos · nuevos residentes · observaciones.

Los instrumentos ENOEN llevan un encabezado **II. No ocupados** explícito que las versiones clásicas no rotulan aparte. Es la única diferencia de estructura entre eras, y no introduce ninguna sección nueva.

La sección que más se acerca, **X. Apoyos económicos** (`c_amp_v5` p. 12), resultó ser: pregunta 10, recepción de programas de gobierno en los últimos tres meses (beca de capacitación; "apoyo para realizar una actividad por su cuenta *(Procampo, microcréditos)*"; otro programa); pregunta 10a, recepción de apoyo de alguien que vive o trabaja en el extranjero / otro estado / el mismo estado; pregunta 10b, Seguro Popular. Es un catálogo de **fuentes de ingreso**, no de conducta financiera.

La sección **VI. Características sociodemográficas** del sociodemográfico es lista de personas, condición de residencia, parentesco, sexo, edad, fecha y lugar de nacimiento, alfabetismo y nivel de instrucción (`c_sdem_v5a`:160-255). Nada financiero.

### El barrido léxico, y su adjudicación

Se corrió un léxico de **45 términos** sobre el texto completo de los nueve cuestionarios, cubriendo las cuatro familias con las que se operacionaliza preferencia temporal en encuesta de hogar —(i) acervo y vehículo de ahorro, (ii) crédito y deuda, (iii) horizonte de planeación, (iv) expectativas— más los nombres propios de las instituciones mexicanas de cada familia. **Todo acierto se adjudicó, uno por uno, contra el reactivo en que vive.**

**29 de los 45 términos tienen CERO aciertos en los nueve cuestionarios**, y son justamente los que nombran el constructo de frente:

> `tanda` · `alcanci` · `cooperativa` · `caja popular` · `invers` · `invert` · `patrimoni` · `herenc` · `endeud` · `hipotec` · `tarjeta de credito` · `mensualidad` · `abono` · `plazos` · `agiotist` · `fiado` · `banco` · `aseguradora` · `remesa` · `planea` · `planific` · `previs` · `largo plazo` · `corto plazo` · `posterga` · `impacien` · `paciencia` · `presupuest` · `expectativ`

**Los tres cuestionarios sociodemográficos no registran un solo acierto de los 45 términos.**

Los tres instrumentos ENOEN producen un perfil de aciertos **idéntico** al de sus pares de las otras dos eras, término por término: `c_bas_v6` calca a `c_bas_v5`/`c_bas_v7`, `c_amp_v6` calca a `c_amp_v5`/`c_amp_v6a`, y `c_sdem_v5` da cero como los otros dos sociodemográficos. **Ni un solo término nuevo en toda la era ENOEN.** El instrumento no cambió en esta dimensión entre 2016 y 2026.

Los 16 términos con acierto caen, sin excepción, en nueve clases y **ninguna es horizonte temporal**:

| clase | qué es | ejemplo de reactivo |
|---|---|---|
| **A** | prestación que otorga el **patrón** | `3m` · crédito de vivienda, fondo de retiro, seguro de vida, préstamos personales y/o caja de ahorro |
| **B** | acceso a institución de salud por el trabajo | `6d`/`7d`/`9k` · IMSS, ISSSTE, Pemex/naval/militar; `10b` · Seguro Popular |
| **C** | condición de actividad / motivo de separación | `2e` · "pensionado o jubilado"; `9d`-4 · "se pensionó, jubiló o se retiró de su negocio" |
| **D** | fuente de ingreso de un trabajo anterior | "pensión o jubilación"; "seguro de desempleo"; "seguro de separación individual" |
| **E** | motivo de cierre o paro de la **unidad económica** | `9b`-01 · "exceso de deudas o se declaró en quiebra"; `9c` · "falta de crédito para seguir operando" |
| **F** | apoyo de gobierno recibido | `10`-2 · "*(Procampo, microcréditos)*" |
| **G** | instrucción al entrevistador | recuadro ATENCIÓN tras la pregunta 3 · "Vender o empeñar sus bienes → corrige la secuencia" |
| **H** | descriptor de la unidad económica | `4c` · "cadena comercial, **bancaria** o de servicios" |
| **I** | nombre propio de programa | `10`-1 · "*Jóvenes Construyendo el Futuro*" — único acierto de `futuro` en los nueve cuestionarios |

La clase **E** merece el señalamiento explícito porque es lo más cercano a *deuda* en toda la ENOE: `9b` opción 01, "Exceso de deudas o se declaró en quiebra". Es un **motivo declarado retrospectivamente sobre un negocio ya cerrado**, dentro de la sección de antecedentes laborales. No es una medida de endeudamiento del hogar ni de nadie.

### Por qué la batería `3m` no rescata el ejercicio — tres razones, cada una suficiente

`c_amp_v5` p. 5 y `c_amp_v6a`, enunciado literal:

> **3m. En este trabajo, ¿a … le dan, *aunque no utilice*,**
> 1 crédito para vivienda *(Infonavit, Fovissste)*? · 2 guardería? · 3 tiempo para cuidados maternos o paternos? · **4 fondo de retiro *(SAR o Afore)*?** · **5 seguro de vida?** · 6 seguro privado para gastos médicos? · **7 préstamos personales y/o caja de ahorro?**

1. **Mide al patrón, no al sujeto.** El "*aunque no utilice*" excluye la conducta **por diseño del instrumento**: la respuesta es idéntica para quien ahorra en su Afore voluntariamente y para quien nunca la ha mirado. No hay conducta que observar.
2. **Es casi colineal con la exposición.** La prestación laboral es ingrediente de la definición operativa de formalidad —el propio codebook documenta `PRE_ASA` ("prestaciones laborales: 1 Con, 2 Sin") como variable precodificada de la clasificación (`con_basedatos_proy2010.pdf` p. 24)—. Usar `3m` de desenlace y formalidad de exposición sería **regresar formalidad sobre sí misma**.
3. **No interroga a quien importa.** Verificado contra los saltos de la p. 4 de `c_amp_v5`: `3a` ("¿tiene un jefe o superior?") con **Sí → pasa a 3h**; con No, `3b` ("¿se dedica a un negocio por su cuenta?") con **Sí → 3c…3g → pasa a 3r**. En `3h`, las opciones **2 "trabajador no familiar sin pago"** y **3 "trabajador familiar sin pago" → pasan a 3q**. Es decir: **`3l`/`3m` solo las contesta el subordinado con pago.** El trabajador por cuenta propia, el empleador y el trabajador sin pago **nunca ven la batería** — y son precisamente donde se concentra la ocupación informal que la elasticidad quiere contrastar (`TUE2=5` "sector informal", 16.4 M de personas en 4T2022, `con_basedatos_proy2010.pdf` p. 23). El manual del entrevistador de ENOEN lo dice sin rodeos al fijar el objetivo de la batería (p. 247): *"Conocer qué otro tipo de prestaciones laborales les otorga a los **trabajadores subordinados remunerados** la unidad económica para la que trabajan"*.

**Y la restricción temporal es peor de lo que parece.** El básico **no tiene `3m` en absoluto** — confirmado no solo en el cuestionario sino en el *layout* de captura: `enoe_n_manual_critico.pdf` A.6 (COE versión básica, p. 109) lista `P3k1…P3k9`, luego `P3l` y salta a `P4`; **no existen campos `P3m*`**. En A.5 (COE versión ampliada, p. 98) sí están `P3m1…P3m9`. Como el ampliado se levanta **solo en el trimestre I de cada año** desde 2009 (`con_basedatos_proy2010.pdf` p. 2), la batería existe en **un trimestre por año**. En toda la era ENOEN, en solo dos: **2021T1 y 2022T1**. Una ventana de cinco trimestres contiene, en el mejor caso, dos mediciones de `3m` — y eso si el hogar sobrevive las cinco visitas.

La razón 3 es la **lección de la Nota 10 (d) repitiéndose textualmente**: allá fueron los 730 jefes de `tb32p` códigos 1 y 2 a quienes `TB33` nunca interroga; aquí es el cuenta propia, el empleador y el trabajador sin pago a quienes `3m` nunca interroga. La diferencia es que esta vez **se detectó antes de estimar**, que es exactamente lo que el encargo pedía.

### Lo que NO se hizo: estirar el constructo

Lo más cercano a "conducta financiera" en ENOE es un catálogo de **prestaciones** y un catálogo de **fuentes de ingreso**. Ninguna de las dos es horizonte temporal. Declararlas equivalentes sería la asignación disfrazada de medición que el punto (2) de CAL-G3 existe para no repetir. **No hay desenlace, y la variable de ingreso no lo sustituye.**

### Relación con el hallazgo previo — esto lo CIERRA, no lo repite

El "Segundo entregable" de la Nota 7 (29/jul/2026) ya registró esta misma dirección, pero declaró su propia evidencia como débil y lo dijo con todas sus letras:

> *"hallazgo 'no lo encontré', con cobertura a nivel de **título de grupo**, no de variable individual — el listado variable-por-variable del portal devolvió vacío para todos los grupos probados"*

Esta nota sustituye esa cobertura de título por **lectura de reactivo sobre el instrumento completo, con procedencia verificada por hash y re-derivable por script**. El hallazgo pasa de *ausencia de evidencia* a *evidencia de ausencia*.

---

## 2, 3 y 4 · NO EVALUADAS

Las compuertas 2 (enlace del panel a cinco trimestres), 3 (poder) y 4 (población interrogada) **son condicionales a que exista desenlace**. No existe. Conforme al encargo —"si una falla, ese es el resultado: para, escribe la nota, y no sigas"— **no se evalúan y esta nota no emite juicio sobre ellas**.

Se registra abajo, **explícitamente marcado como incidental y NO como veredicto de compuerta**, lo que se leyó en paralelo antes de que la compuerta 1 cerrara. Se deja para que una sesión futura no lo re-derive, no para sustituir un chequeo que no se hizo.

### Incidental, sobre la compuerta 2

Se leyó completo `con_basedatos_proy2010.pdf` (40 pág.) y se extrajo y barrió el paquete de documentación de ENOEN (101 PDF), leyendo en detalle los cuestionarios, los dos manuales, el diseño conceptual, el diseño muestral, la estrategia operativa y las notas técnicas. Resultados que la mesa debería conocer:

- **El panel de cinco trimestres SÍ está documentado, y la afirmación de `procedencia.yaml` queda verificada** — pero *no* en el descriptor que el repo tenía identificado. `enoe_n_manual_entrevistador.pdf` p. 15: *"El diseño de la encuesta es de panel rotatorio, la muestra está dividida en cinco paneles y cada uno permanece en la muestra durante cinco trimestres…"*, con ficha `Tamaño de la muestra: 132 mil viviendas cada trimestre`. La nota metodológica trimestral lo repite y hasta nombra el uso: *"permite a las y los investigadores especializados rastrear los cambios que han tenido los hogares que permanecieron en la muestra a lo largo del tiempo (estudios longitudinales)"*.
- **En cambio `con_basedatos_proy2010.pdf` no dice una palabra del panel.** Cero coincidencias de `panel`, `rotativo`, `rotación`, `quinto`, `cinco trimestres`, `longitudinal`, `seguimiento`, `diseño muestral`. La llave que sí documenta (p. 6) es **intra-trimestral** —vincular VIV→HOG→SDEM→COE1→COE2 dentro de un mismo trimestre— y **no hay receta de enlace longitudinal en él**. Curiosamente, `enoe_n_diseno_muestral.pdf` —donde uno esperaría el tratamiento del panel— tampoco menciona ni una vez "panel", "rotación", "visita" ni "longitudinal".
- **`N_ENT` sí existe y sí va de 1 a 5**, pero eso solo aparece en el anexo A del manual del crítico de ENOEN (`N_ENT`, 1 carácter, 1-5, "Número de entrevista"), no en el descriptor. `H_MUD` queda definido ahí también (`enoe_n_manual_entrevistador.pdf` p. 95): *"identificar, en cada entrevista de la segunda a la quinta, si el o los hogares detectados la primera vez… son los mismos o alguno o todos fueron reemplazados"*.
- **La llave cambia de composición en la frontera ENOEN**: `TIPO` y `MES_CAL` entran desde 3T2020 y `CA` existe solo entre 3T2020 y 2T2021; las tablas llevan prefijo `ENOEN`. La llave publicada para ENOEN **no incluye `UPM` ni `N_ENT`**, y los tres campos nuevos **no están definidos en ninguno de los 101 PDF** — el propio paquete remite a un `enoe_n_fd_c_bas_amp.pdf` que **no viene en el ZIP y no está en el manifiesto**.
- **No existe ponderador longitudinal, en ninguna de las dos eras.** Solo `FAC` (2005T1-2020T1), `FAC_TRI` y `FAC_MEN` (desde 2020T3), los tres transversales. `enoe_n_diseno_muestral.pdf` §6 enumera exactamente tres ajustes —colapsamiento de estratos, no respuesta, proyecciones de población— todos transversales. **Cero menciones de pesos de panel o ajuste por attrition.** La frase promocional sobre "estudios longitudinales" no viene acompañada de ningún instrumento de ponderación.
- **El panel NO se reinició tras el hueco de 2020T2.** `enoe_n_estrategia_operativa.pdf` p. 14: *"La muestra es la que se tiene definida para la ENOE N… **y se mantiene el esquema de rotación por panel**"*; `enoe_n_nota_tecnica_trim3_2020.pdf` p. 28: la ENOEN *"toma como referencia la muestra de viviendas de la ENOE del tercer trimestre 2020"*. **Pero en ningún lugar se afirma explícitamente** que el contador de visita se preserve a través de 2020T2, ni hay una sola frase sobre continuidad o ruptura del enlace en el retorno a ENOE de 2023T1.
- **No hay cifras de attrition por visita del panel, en ninguna de las dos eras.** Cero tablas de pérdida 1ª→2ª→…→5ª, cero tasas de emparejamiento longitudinal. Cobertura publicada solo para tres trimestres (2020T3: 84 556 de 132 325 viviendas, 63.9 %; 2020T4: 76.4 %; 2021T1: 74.8 %); a partir de 2021T2 el INEGI dejó de publicar el conteo.
- Dato confirmado (`con_basedatos_proy2010.pdf` p. 2): desde **2009, el ampliado se levanta en el trimestre I y el básico en II-IV**. Es lo que confina la batería `3m` a un trimestre por año.

**Lectura honesta de esto:** la compuerta 2 probablemente **habría pasado** —el panel existe, la llave existe, `N_ENT` existe— aunque con dos problemas serios que una Fase B habría tenido que declarar: no hay ponderador longitudinal publicado, y la continuidad del contador de visitas a través de 2020T2 no está afirmada por INEGI en ninguna parte. **Nada de esto se evalúa como veredicto aquí.** Es material para quien retome el expediente con otra fuente.

### Incidental, sobre la compuerta 4

La observación de ruteo de `3m` (razón 3 de arriba) es material de Bloque A y quedó verificada contra la p. 4 de `c_amp_v5`. Se reporta ahí, en su sitio, porque sostiene el veredicto de la compuerta 1 — no como evaluación de la compuerta 4.

---

## EL SCRIPT

`tests/cal_enoe_fasea.py` — reproduce la compuerta 1 entera.

- **Modo transcripción** (`python3 tests/cal_enoe_fasea.py`): no necesita los PDF; imprime el instrumento leído, las secciones, el léxico de 45 términos, el inventario adjudicado y el veredicto. Verifica la consistencia interna del inventario.
- **Modo verificación** (`--docs <dir>`): re-deriva todo desde los PDF, buscándolos recursivamente — comprueba los nueve `sha256`, re-extrae con `pdftotext -layout` y vuelve a correr el léxico. **Corrido en esta sesión: 9/9 hashes OK, inventario re-derivado idéntico al transcrito, exit 0.**

Está construido para **fallar si alguien lo contradice**: si aparece un acierto que no está en el inventario adjudicado, sale con código 1 y lo nombra, en vez de dejarlo pasar. Probado con dos controles negativos —un término del léxico sin adjudicar, y ese mismo término apareciendo en los PDF— y **ambos fallos se reportan juntos, exit 1**.

Las constantes (los nueve `sha256`, los conteos por término y cuestionario, la adjudicación reactivo por reactivo) están transcritas en el cuerpo del script con su fuente citada, igual que `tests/calx_g3.py`.

**Un defecto propio, encontrado por el control negativo y corregido en la misma sesión:** la primera versión abortaba la verificación contra PDF si el chequeo de inventario ya había fallado, de modo que un fallo enmascaraba al otro. Ahora solo un problema de **lectura** (PDF ausente o hash malo) aborta la comparación; una inconsistencia de inventario ya no la silencia.

---

## SIN FICHA CAL-ENOE

El encargo pedía el borrador de ficha **"si puede"**. No puede: no hay desenlace, luego no hay exposición que contrastar contra nada, ni ventana, ni muestra analítica, ni ponderador que declarar. **Pre-registrar una ficha aquí sería pre-registrar la estimación de una elasticidad cuyo lado izquierdo no existe.** No se redacta.

---

## HASTA DÓNDE LEYÓ ESTA SESIÓN

**Leído completo, línea por línea:** los **nueve** cuestionarios de ENOE/ENOEN (103 pág., hash verificado 9/9) y `con_basedatos_proy2010.pdf` (40 pág.). De `forense/hitoD-preregistro-v2_0.md`: Notas 7 a 10, la Adenda 1 y el bloque de veredictos. ADR-47 en `canon/gobernanza-v1_15.md`. Las entradas de ENOE/ENOEN de `data/manifiesto.yaml` y el bloque `asignados_coeficiente` de `milpa/procedencia.yaml`.

**Extraído y barrido íntegro, leído en detalle solo en parte:** los **101 PDF** de `enoe_n_trim3_2020-trim4_2022.zip`. El barrido léxico corrió sobre los 101; se leyeron en detalle los seis cuestionarios, el manual del entrevistador, el manual del crítico, el diseño conceptual, el diseño muestral, la estrategia operativa y las notas técnicas trimestrales. Las 40 presentaciones ejecutivas y los instructivos de codificación se barrieron pero no se leyeron en detalle — no tocan ni desenlace ni panel.

**Leído parcialmente:** `forense/hitoE-campana-medicion-v2_0.md` — solo §11 y la adenda del 31/jul, lo suficiente para constatar que `unico_calibrable_hoy` es lo que pone a ENOE en el puesto 1 de la cola priorizada (ver `forense/hallazgos.md`).

**NO leído / NO abierto:**
- **Ningún microdato.** Los 28 ZIP trimestrales de ENOE/ENOEN siguen sin descomprimir y sin inspeccionar por esta sesión. Ni un `.csv`, ni un `.dta`, ni un `conjunto_de_datos_*`. (El ZIP que sí se abrió, `enoe_n_trim3_2020-trim4_2022.zip`, resultó ser 100 % documental: 101 PDF, cero microdatos — verificado enumerando el índice antes de extraer nada.)
- **`enoe_n_fd_c_bas_amp.pdf`** — el *Descriptor de Archivos* de los microdatos de ENOEN. Es el único documento que definiría `TIPO`, `MES_CAL`, `CA`, `fac_tri`, `fac_men` y las variables derivadas de SDEM/COE (`emp_ppal`, `pos_ocu`, `seg_soc`, `tue_ppal`, `clase1`/`clase2`). Está referenciado por URL desde dentro del paquete, **no viene en el ZIP y no está en `data/manifiesto.yaml`**. Es el descriptor de ENOE que el manifiesto ya declara pendiente.
- La *Metodología* y el *Diseño muestral* de la ENOE clásica, y los documentos *Estructura de la base de datos* y *Reconstrucción de variables*, que `con_basedatos_proy2010.pdf` referencia y que **no están en el manifiesto**.

### LÍMITE DEL VEREDICTO

**Ninguno por cobertura de instrumento.** Los nueve cuestionarios cubren las tres eras —clásica (2016-2020), ENOEN (2020T3-2022T4) y post-2023— sin hueco sobre los 28 trimestres bajados. El hueco que esta nota declaraba en su primera redacción quedó cerrado dentro de la misma sesión.

El límite que queda es de otro tipo, y es de alcance: el veredicto es sobre **el instrumento de captación**. Si alguien sostuviera que existe conducta financiera en una variable *derivada* que no se capta en el cuestionario, tendría que exhibirla en el descriptor de archivos — que es justo el documento ausente. Dicho esto, una variable derivada no puede medir algo que ninguna pregunta levantó.

---

## LO QUE ESTA SESIÓN NO HIZO, POR ENCARGO

No tocó `milpa/procedencia.yaml`. No tocó CAL-G3 ni el modelo. No abrió ADR. No pre-registró nada — el pre-registro era Fase B, y ya no procede. No estimó nada. No emitió `CAL-A/B/C/X`.

**Lo que la mesa tiene que decidir**, y esta nota solo enuncia: `unico_calibrable_hoy` afirma que ENOE permite estimar conducta financiera, y no. La declaración se repite en `modelo §2.2`, `glosario §13`, `estado §4` y `gobernanza §5` (cascada ya identificada en la Nota 7), y además **ordena la cola priorizada del Hito E**: `forense/hitoE-campana-medicion-v2_0.md` pone a ENOE en el puesto 1 explícitamente por ser "la única con ruta de calibración ya declarada en `procedencia.yaml`", y una corrección de revisión del 31/jul movió `horizonte_temporal` de SIN CANDIDATA a CANDIDATA sobre esa misma base. Con la compuerta 1 cerrada, **ese puesto 1 y esa reclasificación se apoyan en una premisa que ya no se sostiene**. Ni la cola ni la clasificación se editan aquí.
