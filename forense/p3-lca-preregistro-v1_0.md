# P3 · Pre-registro del LCA de segmentación

### `p3-lca-preregistro` · **v1.0** · 3 de agosto de 2026 · **PRE-REGISTRO SELLADO**

> | | |
> |---|---|
> | **ARCHIVO** | `p3-lca-preregistro-v1_0.md` |
> | **NOMBRE ESTABLE** | **`p3-lca-preregistro`** — cítalo así, nunca por nombre de archivo |
> | **QUÉ ES** | El protocolo completo de la prueba **P3** de `revision-programa-2026-07-31.md` §5. **No la ejecuta.** La ejecuta otra sesión, en Fase B |
> | **VERIFICAS ASÍ** | §1 trae **dos hipótesis rivales** con su falsador cada una · §3 fija el rango de `k` y la regla de desempate **antes** del dato · §6 es una tabla de decisión con **seis desenlaces** · §8 es el módulo de auditoría de nueve preguntas |
> | **ESTADO** | **SELLADO.** Cualquier cambio posterior va como **enmienda fechada y visible** al final de este archivo (§10), nunca como edición silenciosa del cuerpo |

---

## 0 · Declaración de sesión limpia — léela antes que el protocolo

**Esta sesión escribió el protocolo antes de ver el dato. Es la propiedad entera del artefacto y por eso va primero.**

**Lo que se leyó, todo del repo en esta sesión (procedencia tipo (1), `instrucciones` Bloque A):**

| Archivo | Qué se tomó de él |
|---|---|
| `canon/modelo-decision-v4_0.md` | §0.2, §1.1 completa (A–F), §1.2, §1.3, §1.5, §1.6, §2.1, §2.2, §5, módulo de auditoría |
| `canon/gobernanza-v1_15.md` | §4, **ADR-51** completo (a)–(e); cabecera `VERIFICAS ASÍ`; ADR-28.a; ADR-50 §(5) |
| `canon/protocolo-sesion-v1_0.md` | §1–§3 (apertura, R0, traspaso) |
| `forense/notas/2026-08-01-p2-momentos-atributos.md` | §2.b (criterio **C1–C4**), §2.c, §2.d (tabla parámetro × estatus), §1.b, §1.d, §3.a, §3.b, §5 |
| `forense/notas/2026-07-31-identificabilidad-perfiles.md` (**INV-SEG p3**) | §3.A (correspondencia perfil→observable, las 4 celdas), §3.B (Pruebas 1–3), §3.C (veredicto) |
| `forense/metodologia-identificacion-vs-ajuste-v0_1.md` | §1–§4 (identificación ≠ ajuste; las cinco rutas; la condición de "declarar antes de ver los datos") |
| `revision-programa-2026-07-31.md` | §5 (P1–P4), §6 (decisiones de mesa), §7 (auditoría) |
| `forense/hitoD-preregistro-v2_0.md` | Solo la **convención de forma** de un pre-registro del programa (cabecera, sello, "escrito antes de buscar nada") |
| `instrucciones-proyecto-v2.md` | Bloque A completo; las nueve preguntas del módulo de auditoría del Bloque B |
| `milpa/` | Existencia y rol de `procedencia.yaml`, `refutations.yaml`, `tramite.yaml` (citados por ADR-51 y por P2, no re-derivados aquí) |

**Lo que NO se abrió, y es la condición que habilita este artefacto:**

> **Ninguna fuente de datos fue abierta, descargada, listada ni inspeccionada.** Ni microdato, ni diccionario, ni cuestionario, ni catálogo de valores, ni descriptor — de ENIGH ni de ninguna otra de las ocho fuentes del inventario, ni de WVS, LAPOP, Latinobarómetro o ENCUP. **No se consultó ningún host de datos** (INEGI ni ningún otro). No se corrió ningún modelo. El árbol `data/` no se abrió.
>
> Todo nombre de variable, catálogo, módulo y llave que aparece abajo está **citado textualmente de `modelo` §1.1.A** —que a su vez los cita de P1— o de **INV-SEG p3 §3.A**. **Ninguno se escribió de memoria.** Donde el canon no trae el nombre, este pre-registro **declara el hueco y ordena que el ejecutor lo derive y lo reporte**, en vez de teclear una cifra o un identificador esperado (`instrucciones` v2.1, *"ninguna cifra esperada se teclea de memoria"*).

**Contaminación heredada, declarada.** `revision §5·P3` exige que el pre-registro lo escriba una sesión limpia *"porque INV-SEG contaminó a las de Ubuntu contra las ocho fuentes"*. Esta sesión no tocó ninguna de las ocho. Lo que sí heredó es **lectura de INV-SEG p3 y de P2**, que sí las tocaron: los veredictos de identificabilidad y las cuatro celdas de §3.A entran aquí como **premisa citada**, no como observación propia. Eso no es contaminación de dato —ninguno de esos artefactos reporta una distribución, una frecuencia ni un cruce de ENIGH— pero se declara porque un lector tiene derecho a saber por dónde entró cada cosa.

**Verificación de premisas del encargo (ADR-39, `instrucciones` v2.1).** Las cuatro premisas se verificaron contra archivo antes de obedecerlas, y las cuatro se sostienen:

| Premisa del encargo | Verificada contra | Resultado |
|---|---|---|
| El canon vigente es **v4.0**, con §1.1 por síntesis sobre atributos y perfiles como DESCRIPTORES | `canon/modelo-decision-v4_0.md` §1.1, §1.1.D | ✔ Sostenida. El v3.4 no se cita en ninguna parte de este documento salvo donde el propio v4.0 lo cita como historia |
| Los seis ejes con variable, módulo y llave; tres de nivel hogar | `modelo` §1.1.A, tabla e ⚠️ de restricción de nivel hogar | ✔ Sostenida. Citados verbatim en §2 de este documento |
| P2 declaró **C1–C4** (incluido C3 de circularidad) y una tabla parámetro × estatus | `forense/notas/2026-08-01-p2-momentos-atributos.md` §2.b y §2.d | ✔ Sostenida |
| **ADR-51** corrigió los g.l. reales a **22** y registró **M2/M3** | `canon/gobernanza-v1_15.md` §4, ADR-51 (b) y (c) | ✔ Sostenida. 22 = 7 probabilidades + 15 coeficientes, dos derivaciones computadas coincidentes |

---

## 1 · Hipótesis, escritas antes

**Qué decide esta prueba, en una línea:** si la heterogeneidad que el corpus lleva un año describiendo con seis perfiles existe como estructura en la conjunta de los seis ejes observables, o si esos ejes sostienen bastante menos estructura de la que el corpus les colgó encima. *Por primera vez la segmentación sería falsable en vez de asumida* (`revision §5·P3`).

Las hipótesis se enuncian sobre **el modelo ajustado**, no sobre México: una clase latente es un objeto de un modelo estadístico con un conjunto de indicadores elegido, no una población que ande por ahí. Ver §7 y §8·Q1.

### H-A · Hipótesis del programa — los seis descriptores nombran regiones reales

> La conjunta de los siete indicadores de §2 tiene **estructura latente múltiple**: el criterio de §3 selecciona **k ≥ 5**, y al menos **cuatro** de las clases seleccionadas tienen perfil modal compatible con una de las regiones de `modelo` §1.1.D bajo el criterio de correspondencia de §6.0.

**Por qué se espera, derivado del corpus y no de intuición:** §1.1.D define cada descriptor como una conjunción explícita de cortes sobre esos mismos ejes (`segsoc`=1 ∧ `tam_loc`=1 ∧ `est_socio`=3, etc.). Si esas conjunciones concentran masa —si la gente se apila en las esquinas del espacio y no se reparte uniforme por él—, un LCA sobre los ejes tiene que verlo.

**Techo aritmético de H-A, declarado antes de correr nada y no negociable:** **el máximo recuperable es 4 de 6, no 6 de 6.** El descriptor **3 (Vulnerable en ascenso)** no es una región sino una **trayectoria** (§1.1.D, `revision §3`) y no puede emerger de un transversal ni por accidente; el descriptor **4 (Élite A/B)** es **región declarada NO OBSERVADA** (límite (i) de §1.1.C: *"si las encuestas de hogar no capturan a la élite A/B, la población sintética tampoco"*). **Cualquier lectura futura de un resultado k=6 como "emergieron los seis perfiles" es un error de lectura, y queda pre-registrado como error antes de que alguien pueda cometerlo.**

**Qué falsa H-A:** que el criterio de §3 seleccione **k ≤ 2**; o que seleccione k ≥ 5 pero **menos de cuatro** clases satisfagan el criterio de correspondencia de §6.0. Cualquiera de las dos la falsa por separado.

### H-B · Hipótesis rival — el dato sostiene ~2 clases y el corpus sobre-segmentó

> El criterio de §3 selecciona **k = 2**, y la separación entre las dos clases está dominada por **formalidad** (`segsoc`) y/o **nivel socioeconómico** (`est_socio`) bajo el criterio de dominancia de §6.0.

**Por qué es la rival seria y no un espantapájaros —tres apoyos, todos citados:**

1. **INV-SEG p3 §3.A ya lo midió con lo que tenía y le salió peor que seis.** De los seis perfiles: 1 y 4 no se separan (`{1∪4}`, unión forzada), 2 y 3 no se separan (`{2∪3}`), el 5 se identifica pero **solapa** con ambos y el 6 se parte en tres poblaciones distintas. *"Lo que sobrevive: 4 celdas, no 6 perfiles"* — y de esas cuatro, dos son uniones forzadas y una no es disjunta. El escenario **PESIMISTA** de su tabla de momentos es literalmente *"sólo formal/informal (2 celdas)"*: la rival ya está escrita en el corpus como escenario contemplado.
2. **Las dos uniones forzadas caen justo sobre el eje de formalidad e ingreso.** `{1∪4}` es formal-urbano-ingreso alto; `{2∪3}` es informal-ingreso bajo. Si el corpus no pudo separar dentro de cada una con ninguna combinación de variables del inventario, la lectura parsimoniosa es que la estructura real **es** ese contraste y lo demás era vocabulario.
3. **La malla es de estructura económica, no de cultura** (`modelo` §8·Q1: *"los seis ejes son de estructura y de exposición; ninguno pregunta por valores, creencias ni preferencias"*). Formalidad, ingreso, urbanización y acceso digital covarían fuerte entre sí en cualquier economía desigual. Un LCA sobre variables que miden en gran medida la misma posición socioeconómica **tiene motivos para devolver un gradiente, no un mosaico**.

**Qué falsa H-B:** que el criterio de §3 seleccione **k ≥ 3** de forma estable (§3.5); o que seleccione k=2 pero la separación esté dominada por un eje **distinto** de formalidad e ingreso —urbanización, edad, migración o acceso digital—, lo cual falsaría la *forma* de H-B aunque acertara el número.

### H-C · Segunda rival, la que casi nadie escribe — no hay clases, hay un gradiente

> El criterio de §3 selecciona **k = 1** (ninguna heterogeneidad latente por encima de la independencia local), **o bien** el BIC decrece monótonamente en todo el rango 1–8 sin mínimo interior.

**Por qué se pre-registra:** son los dos resultados que un analista con una hipótesis favorita tiende a no escribir en el menú, y por eso hay que ponerlos antes. k=1 dice que la conjunta de los siete indicadores no tiene más estructura que sus marginales. BIC monótono decreciente dice algo distinto y más incómodo: **que lo que hay es un continuo y el modelo de clases le está poniendo cortes arbitrarios a un gradiente**, añadiendo clases indefinidamente para aproximarlo. Con siete indicadores de estructura socioeconómica correlacionada, ese desenlace es plausible y no marginal.

**Qué falsa H-C:** cualquier mínimo interior de BIC en el rango con solución estable.

**Ninguna de las tres hipótesis puede ganar por defecto.** H-A pierde con k≤2 o con correspondencia insuficiente; H-B pierde con k≥3 estable o con eje separador equivocado; H-C pierde con mínimo interior estable. Y el desenlace **INESTABLE** (§6·D5) no cuenta como victoria de ninguna — está pre-registrado como *"la prueba no decidió"*, explícitamente **no** como apoyo al statu quo.

---

## 2 · Indicadores, covariables y auxiliares

### 2.0 · El principio que ordena la lista

**Entran como indicadores los seis ejes del vector de atributos de `modelo` §1.1.A, y nada más.** La razón no es comodidad: la pregunta que esta prueba responde es *"¿la segmentación que el corpus declara tiene sustento en la estructura observada?"*, y esa segmentación está definida en §1.1.D **sobre esos seis ejes y ningún otro**. Meter sexo, escolaridad o región cambiaría la pregunta a *"¿cuál es la mejor segmentación de México?"* — una pregunta más grande, legítima, y **fuera del perímetro de este pre-registro**. Se declara para que nadie la añada después presentándola como la misma prueba.

### 2.1 · Los siete indicadores — variables citadas, no reescritas

Todas las variables, catálogos, módulos y llaves de esta tabla se citan de `modelo` §1.1.A, que las cita de P1 §1–§2 (ENIGH 2022 nueva serie, `enigh2022_nc_csv`, sha256 verificado contra `data/manifiesto.yaml`). **Esta sesión no abrió el paquete.**

| # | Indicador | Variable · valores (citados de §1.1.A) | Módulo | Nivel real | Categorías que entran al LCA |
|---|---|---|---|---|---|
| **I1** | Formalidad laboral | `segsoc` — 1 Sí / 2 No (derechohabiencia) | `poblacion` | **persona** | 2 |
| **I2** | Edad, en tramos | `edad` — entero, años | `poblacion` | **persona** | 4 · ver §2.2 |
| **I3** | Condición migratoria | `residencia` — 32 entidades + "Estados Unidos de América" + "Otro país" (catálogo `residencia.csv`, 34 categorías) | `poblacion` | **persona** | 3 · ver §2.3 |
| **I4** | Urbanización | `tam_loc` — 1 · 100 000+ / 2 · 15 000–99 999 / 3 · 2 500–14 999 / 4 · <2 500 (catálogo `tam_loc.csv`) | `concentradohogar` | **hogar**, heredado | 4 |
| **I5** | Nivel socioeconómico | `est_socio` (catálogo `est_socio.csv`: 1 Bajo / 2 Medio bajo / 3 Medio alto / 4 Alto) | `concentradohogar` | **hogar**, heredado | 4 |
| **I6** | Tenencia de celular | `celular` (SERV_2) — 1 Sí / 2 No | `hogares` | **hogar**, heredado | 2 |
| **I7** | Conexión a internet | `conex_inte` (SERV_4) — 1 Sí / 2 No | `hogares` | **hogar**, heredado | 2 |

**Unidad de análisis:** la **persona**, base `poblacion`, llave PERSONA `folioviv`+`foliohog`+`numren` (§1.1.A). Los indicadores I4–I7 se heredan del hogar a cada persona.

**Universo:** personas de **18 años o más**. Decisión declarada, no heredada: por debajo de 18 la formalidad laboral no es un atributo interpretable y el modelo de decisión describe decisores. El ejecutor **reporta el `n` resultante**; este pre-registro no lo predice (`instrucciones` v2.1).

**Por qué `acceso digital` entra como dos indicadores binarios y no como un índice.** Construir un índice —"acceso bajo/medio/alto"— sería imponer una estructura antes de medirla, que es exactamente el vicio que esta prueba existe para no cometer. Los dos binarios entran separados y el LCA decide si covarían. Se hereda el límite declarado por P1 y repetido en §1.1.A: es **tenencia binaria del hogar**, sin distinguir celular básico de *smartphone*, sin uso individual ni banca en línea. **El eje 5 es el más débil de los seis y su debilidad viaja con el resultado.**

**Por qué `acceso_digital` puede ser indicador sin violar C3.** Porque el v4.0 ya lo sacó de la lista de parámetros: X-03 de §1.1.E lo reclasifica de parámetro a **eje del vector de atributos**, precisamente citando el criterio C3 (*"una condicional sobre sí misma es circular"*). Aquí opera como atributo, que es lo que el canon dice que es. **Corolario pre-registrado:** ningún análisis posterior puede condicionar un θ_k simultáneamente sobre la clase latente y sobre `acceso_digital` como si fueran informaciones independientes — el segundo está dentro de la primera.

### 2.2 · El corte de edad — el punto más delicado del protocolo

`modelo` §1.1.A y §1.1.F declaran que **la edad no tiene partición canónica**: el corte de "joven" está marcado **PENDIENTE** en los siete sitios donde el canon lo usa (H-02, H-06, H-07, `R1.4`, `R2.4`, `R5.4`, descriptor 5), y §1.1.B prohíbe inventar forma funcional donde no hay evidencia.

**Se pre-registra el corte, con procedencia y con marca:**

> **I2 = {18–29 · 30–44 · 45–59 · 60+}.**
> - El corte **18–29** se toma de **INV-SEG p3 §3.A**, fila del perfil 5: *"edad (`EDAD_V` 18-29)"*. Tiene procedencia en el corpus; **no lo inventó esta sesión**.
> - Los cortes **44/59** son **ARBITRARIOS**, se declaran como tales, y su única defensa es que están escritos **antes** del dato y por tanto no se pueden afinar para que salga la clase que a alguien le guste.

**Por qué la edad entra como indicador y no como covariable, aun con el corte sin canonizar.** Si saliera del bloque de indicadores, el descriptor 5 (*Joven Gen Z urbano conectado*) **no podría emerger como clase por construcción**, y H-A quedaría amputada de uno de sus cuatro recuperables antes de empezar. Una prueba diseñada para que una hipótesis no pueda ganar es tan mala como una diseñada para que no pueda perder.

**Sensibilidad obligatoria S2 (§5.4):** re-ajuste del `k` seleccionado con una partición distinta de la edad, declarada aquí: **{18–24 · 25–39 · 40–59 · 60+}**. Si la solución cambia de `k` o si la congruencia de perfiles cae por debajo del umbral de §3.5, se reporta que **el eje de edad no sostiene estructura estable** y el resultado se lee con esa advertencia pegada. La sensibilidad no es opcional ni queda a criterio del ejecutor.

**Subproducto pre-registrado, y solo eso.** Si emerge una solución estable, la **distribución empírica de edad por clase** es un insumo candidato para el corte de "joven" que el canon tiene PENDIENTE. Se reporta **como subproducto descriptivo**, no como canonización: fijar el corte es acto de mesa, no salida de este protocolo.

### 2.3 · Migración — recodificación declarada y su límite

`residencia` (34 categorías) se recodifica a **3**: `misma entidad` / `otra entidad de México` / `extranjero` (unión de "Estados Unidos de América" y "Otro país"). La unión de las dos categorías extranjeras es decisión declarada: §1.1.D define el descriptor 6 exactamente sobre esa unión.

⚠️ **Límite heredado, no resuelto:** §1.1.A declara que *"ni el diccionario ni `metadatos_enigh_2022_ns.txt` traen el texto literal de la pregunta, así que no se puede confirmar la referencia temporal de `residencia`"*. **Este pre-registro no lo resuelve y prohíbe resolverlo por suposición.** El ejecutor de Fase B **reporta** qué referencia temporal encontró, si la encontró, y si no la encontró lo dice con esas palabras — *"no pude confirmarlo"* y *"la fuente no lo trae"* son hallazgos distintos y no se colapsan (`instrucciones` v2.2).

⚠️ **Segundo límite, de INV-SEG p3 §3.A:** el eje de migración *"se parte en tres poblaciones que no son la misma: quien migró y volvió · el hogar que se quedó y recibe remesas · el hogar con integrante ausente"*. Por eso **`remesas` NO entra como indicador** (§2.4): mezclarla con `residencia` metería tres poblaciones distintas en un mismo eje binario.

### 2.4 · Lo que queda FUERA de los indicadores, con su razón

| Variable | Rol asignado | Por qué no es indicador |
|---|---|---|
| `ing_cor` (monto trimestral, continuo) | **Auxiliar descriptivo** | Es continua; meterla en un LCA categórico exigiría categorizarla —otro corte inventado— y **puede ser redundante con `est_socio`**, cuya regla de construcción **no está verificada por P1**. Entra como auxiliar para *describir* las clases (mediana ponderada por clase, vía §4), nunca para definirlas. ⚠️ Si el ejecutor encuentra que `est_socio` es función determinista de `ing_cor`, lo **reporta**; no lo asume ni ahora ni entonces |
| `remesas` (Σ `ingresos.ing_tri`, clave P041) | **Auxiliar** | §1.1.A la marca *"complementaria, no necesaria"*; INV-SEG p3 la señala como una de tres poblaciones distintas del eje 6. Es de **hogar** |
| `contrato`, `tipocontr`, `pres_1..20` (incl. `pres_8` SAR/AFORE), `medtrab_1..7` (módulo `trabajos`) | **Sensibilidad S3** (§5.4) | Es la **segunda operacionalización de la formalidad** que §1.1.F declara (*"la formalidad admite al menos dos operacionalizaciones"*). No se promedia con `segsoc`: se corre aparte y se comparan las soluciones. ⚠️ El módulo **no tiene fila para quien no trabajó** (§1.1.A): eso es **ausencia estructural**, no dato faltante — tratamiento en §5.3 |
| `poblacion.parentesco` (composición de hogar) | **Fuera. Declarado, no usado** | §1.6 lo declara **PENDIENTE DE VERIFICACIÓN**: *"P1 inventarió seis ejes y la composición de hogar no es ninguno de ellos"*. Un pre-registro no promueve a indicador una variable que el canon marca sin verificar |
| Sexo, escolaridad, entidad/región | **Fuera de indicadores; admisibles como auxiliares descriptivos** | No están en el vector de §1.1.A. Incluirlos cambia la pregunta (§2.0). ⚠️ Nota: `R2.1` conserva *"sur"* como modificador literal porque **la región geográfica no está en el vector de seis ejes** (§1.6) — este pre-registro respeta esa frontera |
| **`gastotarjetas`** y todo desenlace de regla del motor | **PROHIBIDO como indicador** | Es la trampa C3, aplicada. INV-SEG p3 §3.B·Prueba 1 lo nombra como el desenlace observable de `dinero.consumo.estatus_mediado_por_credito` (G2). Si entrara como indicador y después se relacionara la clase con ese desenlace, sería **regresar el desenlace sobre sí mismo** |
| **Todo reactivo de un θ_k** (ENCUCI `AP5_1_*`, ENIF `P9_9_*`, ENIF `P4_10`, ENVIPE `BP1_20/23/28`, ENCIG batería XI, ENUT 6.11/6.11a) | **PROHIBIDO como indicador** | Misma trampa, del otro lado: son los reactivos sobre los que el programa quiere **condicionar** después. Además ninguno vive en ENIGH, así que la prohibición es hoy también una imposibilidad — se escribe igual, porque la prohibición debe sobrevivir a que alguien cambie de fuente |

### 2.5 · La restricción de nivel hogar — qué se hace con ella, decidido antes

**Tres de los siete indicadores (I4, I5, I6, I7 — cuatro columnas sobre tres ejes) son de nivel hogar.** P1 §3, citado por §1.1.A: *"todas las personas del mismo hogar comparten el mismo valor en esas columnas tras el join [...] esa varianza no existe en ENIGH — es indistinguible de una persona a otra del mismo hogar por diseño del instrumento, no por un hueco de esta sesión."*

Esto no es un detalle de estimación. Es una **restricción de diseño con tres consecuencias, todas pre-registradas**:

**(a) Ninguna clase latente podrá separar a dos personas del mismo hogar por urbanización, ingreso o acceso digital.** Si dos hermanos caen en clases distintas, sólo puede ser por I1, I2 o I3. Esto es **una propiedad del instrumento, no un hallazgo del LCA**, y queda prohibido reportarlo como hallazgo.

**(b) Hay dependencia intra-hogar por construcción.** Cuatro de siete indicadores son constantes dentro del hogar, así que las personas del mismo hogar **no son observaciones independientes**. Tratamiento pre-registrado: errores estándar robustos con conglomerado en la **UPM** del diseño (§5.1), que anida al hogar. ⚠️ **Se declara explícitamente que el LCA de un nivel asume independencia local condicional a la clase y que ese supuesto está violado aquí por diseño.** El efecto conocido de esa violación es **sobreestimar el número de clases**: parte de la "estructura" puede ser agrupamiento por hogar. Esto sesga el resultado **a favor de H-A y en contra de H-B** — y por eso se dice aquí, no en un anexo. Un resultado k alto es, en parte, sospechoso por esta vía; un resultado k=2 lo es mucho menos.

**(c) Especificación de control obligatoria, S1 (§5.4):** re-ajuste del rango completo de `k` usando **sólo los tres indicadores de persona** (I1, I2, I3). Es la prueba directa de (b): si la solución de personas colapsa a un `k` menor cuando salen los ejes de hogar, buena parte de la estructura era agrupamiento de hogar; si se sostiene, no lo era. **Los dos resultados se reportan juntos, siempre.**

**Lo que este pre-registro NO adopta, y por qué se dice:** el tratamiento técnicamente correcto de una malla mixta es un **LCA multinivel** (clases de persona anidadas en clases de hogar). Se declara como la extensión correcta y **no se pre-registra como análisis primario**: multiplica supuestos y decisiones antes de que exista un resultado de un nivel con el que compararla. Queda **pre-registrada como condicional**: se corre si y sólo si S1 muestra que los ejes de hogar dominan la solución (§6·D5·nota). Si se corre, es un análisis nuevo y necesita su propia enmienda fechada (§10).

---

## 3 · Selección del número de clases — fijada antes de ver el dato

> ⚠️ **Toda esta sección es marco importado, marcado (c)** (`instrucciones` Bloque A). BIC, aBIC, entropía, arranques múltiples y replicación en mitades son práctica estándar de la literatura de mixturas (Nylund-Gilmore-Muthén; Vermunt; Wedel & Kamakura, ya citado por el v4.0 §1). **Se importa con crítica declarada, no ingenuamente:** los tres puntos donde la práctica estándar **no** aplica limpio a este caso están nombrados en §3.6, y ninguno se resuelve fingiendo que no existe.

### 3.1 · Rango de `k` que se prueba: **1 a 8**

- **`k=1` entra** porque es H-C y porque un rango que empieza en 2 asume la conclusión.
- **`k=2` entra** porque es H-B.
- **`k` llega a 8, no a 6**, para que la hipótesis del programa no tenga el techo puesto a su favor: si el máximo probado fuera 6 y saliera 6, el resultado sería un artefacto del rango. **Dos de holgura por encima de 6** es la justificación completa.
- **No se extiende el rango después de ver el dato.** Si el BIC sigue decreciendo en `k=8`, eso **es un resultado** (§6·D6), no una invitación a probar 9. Cualquier ajuste fuera de 1–8 se marca **EXPLORATORIO** y queda **fuera de este pre-registro**.

### 3.2 · Índices que se computan y se reportan **siempre**, para los ocho ajustes

Log-verosimilitud · número de parámetros libres · **BIC** · **aBIC** (BIC ajustado por tamaño de muestra) · **AIC** · **entropía** · prevalencia ponderada de cada clase · número de arranques que replican la mejor log-verosimilitud · señalización de fronteras (probabilidades en 0/1).

**La tabla completa de los ocho ajustes se publica**, gane quien gane. Un pre-registro que sólo publica la solución elegida no permite auditar la elección.

### 3.3 · Regla de decisión — escrita antes, en este orden y sin discreción

1. **Primario: BIC mínimo.** El `k` con menor BIC.
2. **aBIC se reporta siempre** y no manda.
3. **Si BIC y aBIC discrepan** (señalan `k` distintos): **se reportan ambas soluciones completas y se elige como primaria la de `k` MENOR.** *Por qué el desempate va hacia la parsimonia, escrito antes: el modo de falla documentado de este programa es la **sobre-segmentación** (`revision §0`, INV-SEG p3 §3.C). Cuando la regla de desempate tiene que apuntar a algún lado, apunta **contra la hipótesis del propio programa**. Un desempate que favorece a quien lo escribe no es un desempate.*
4. **Regla de "sin separación":** si la diferencia de BIC entre el mínimo y una solución de `k` menor es **inferior al 2 % del rango total de BIC observado en 1–8**, se declara que los dos modelos **no están separados por el criterio** y gana **el `k` menor**. Evita que una diferencia de tercera cifra decida un veredicto de canon.
5. **La entropía NUNCA selecciona `k`.** Se reporta siempre y no entra en la decisión. *Por qué se prohíbe explícitamente: la entropía mide **qué tan nítida es la clasificación**, no qué tan bien ajusta el modelo. Elegir `k` por entropía alta selecciona la solución que más se parece a una asignación dura — es decir, empuja hacia el forced choice justo por la puerta que §4 cierra.* La entropía se usa **sólo** para calificar la calidad de clasificación del resultado y para justificar la corrección de §4.
6. **Se reportan siempre las soluciones `k−1`, `k` y `k+1`** con sus perfiles completos de probabilidades condicionales por indicador. *Un veredicto que depende de un solo corte no es un veredicto.*

### 3.4 · Máximos locales

Mínimo **500 arranques aleatorios** por valor de `k`, con las 50 mejores soluciones iniciales llevadas a convergencia final. Se reporta cuántos arranques replican la mejor log-verosimilitud. **Una solución cuya mejor log-verosimilitud se replique en menos de 5 arranques se declara NO REPLICADA** y arrastra al desenlace **INESTABLE** (§6·D5).

### 3.5 · Estabilidad — el criterio que decide D5, fijado antes

Tres condiciones. **Basta que falle una** para que el resultado sea INESTABLE:

- **(E1) Replicación de log-verosimilitud** ≥ 5 arranques (§3.4).
- **(E2) Replicación en mitades.** La muestra se parte en dos mitades aleatorias **por UPM** (no por persona: partir por persona rompería el conglomerado y fabricaría estabilidad). Se re-ajusta el `k` seleccionado en cada mitad. Criterio de congruencia: **cada clase de la solución completa debe emparejarse con una clase de cada mitad cuyo perfil de probabilidades condicionales tenga correlación ≥ 0.90**, con el emparejamiento resuelto por máxima congruencia. El **0.90** es un umbral **ARBITRARIO declarado antes** — su defensa es que está escrito aquí y no después.
- **(E3) Sin clases degeneradas.** Ninguna clase con prevalencia ponderada **< 5 %**, y ninguna con probabilidades condicionales pegadas a 0/1 en frontera. Si aparece una, se reporta y la solución se marca degenerada.

### 3.6 · Los tres puntos donde el marco importado no aplica limpio — declarados, no disimulados

1. **Las pruebas de razón de verosimilitud (VLMR, BLRT) no se pre-registran como criterio.** Su distribución de referencia se obtiene por *bootstrap* bajo muestreo simple, y aquí hay **pesos de expansión, estratos y conglomerados**. Se corren **sólo** si el software ofrece una versión que respete el diseño; si no, se reporta **"no corridas por incompatibilidad con el diseño complejo"** y no se corren mal. *Correr un test inválido y reportar su p-valor es peor que no correrlo.*
2. **El BIC depende de `n`, y con pesos de expansión `n` es una elección, no un dato.** Tratamiento pre-registrado en §5.2 — es probablemente el grado de libertad más peligroso de todo el protocolo y por eso tiene sección propia.
3. **La independencia local está violada por diseño** (§2.5·b), lo que sesga la selección hacia `k` mayores. Se declara junto al resultado, siempre, y es la razón de que S1 sea obligatoria.

---

## 4 · Anti-*forced-choice* — prohibición explícita

> ### 🚫 **PROHIBIDA la asignación modal para relacionar clases con desenlaces.**
>
> Ningún análisis derivado de este protocolo puede asignar a cada persona su clase más probable y usar esa etiqueta como variable en un análisis posterior.

**Por qué, en una línea, para que se vea el vínculo con el hallazgo del 31/jul:** la asignación modal convierte un vector de probabilidades en una etiqueta única y tira el error de clasificación — **reintroduce exactamente el *forced choice* de segmentación a priori que `revision-programa-2026-07-31.md` §0/§2 identificó como el defecto del v3.4 y que §1.1 del v4.0 acaba de eliminar al sacar la tabla 6×15**, sólo que ahora con una etiqueta estimada en vez de asignada, lo que la hace más difícil de ver y no menos dañina.

**Enfoque pre-registrado si hay relación clase→desenlace:** **método de tres pasos con corrección — BCH como primera opción, ML (Vermunt) como alternativa declarada**, con la matriz de error de clasificación estimada del propio modelo. Se declara cuál se usó y por qué. Sin corrección, no hay relación clase→desenlace: se reporta que no se hizo.

**Tres corolarios operativos, todos pre-registrados:**

- **(a) El entregable de Fase B son los parámetros de medición y las probabilidades posteriores completas, nunca una columna de etiqueta dura.** No se escribe al repo un archivo con una variable `clase`.
- **(b) La prohibición de `modelo` §1.1.D se extiende a las clases latentes por analogía directa.** Su texto —*"ni una regla de §3, ni un generador de §2, ni un disparador, ni una salida, ni un archivo de `rules/*.yaml` puede tomar como entrada 'el agente es del perfil N'"*— **aplica igual a "el agente es de la clase latente N"**. Un número de clase estimado no es más dato del agente de lo que era un número de perfil asignado. **Se pre-registra que el check de compilación de §1.1.D debe extenderse a identificadores de clase latente**; ejecutar esa extensión es acto de mesa y no lo hace este documento.
- **(c) La prohibición sobrevive al resultado.** Vale igual si emergen 2 clases que si emergen 6. No es una salvaguarda contra un desenlace: es una propiedad del método.

---

## 5 · Diseño muestral, pesos y casos incompletos — decidido antes, no cuando estorbe

### 5.1 · Diseño complejo

**Se respetan los factores de expansión y el diseño muestral de ENIGH.** Estimación por **máxima pseudo-verosimilitud** con pesos; errores estándar con **estratos y conglomerados (UPM)** del diseño; el conglomerado anida al hogar, que es donde vive la dependencia de §2.5·b.

⚠️ **HUECO DECLARADO, y se declara en vez de rellenarse.** **P1 no inventarió el factor de expansión ni las variables de diseño de ENIGH** — no aparecen en `modelo` §1.1.A ni en ninguna otra parte del canon leída por esta sesión. **Este pre-registro NO teclea sus nombres**, porque hacerlo sería escribir de memoria un identificador esperado, que es el defecto que la regla v2.1 existe para atrapar.

> **Instrucción al ejecutor de Fase B:** localiza en el descriptor del paquete el factor de expansión de persona (o el de hogar y su regla de traslado a persona) y las variables de estrato y UPM; **repórtalos con su nombre exacto y su ubicación antes de ajustar nada**. Si el paquete no trae variables de diseño, **dilo con esas palabras**, ajusta sólo con pesos, y declara los errores estándar como **no válidos para inferencia**, no como aproximados. *"No las encontré"* y *"el paquete no las trae"* son hallazgos distintos y no se colapsan (`instrucciones` v2.2).

### 5.2 · Escalamiento de pesos — el grado de libertad más peligroso

Los factores de expansión de ENIGH suman población nacional. **Un BIC computado sobre esa suma es un BIC de decenas de millones de observaciones: penalizaría tan poco en términos relativos que seleccionaría el `k` máximo del rango casi con independencia del dato.** Es un modo de falla que decide el veredicto sin que nadie lo note.

> **Se pre-registra: los pesos se reescalan para sumar el tamaño de muestra efectivo (no expandido), y BIC/aBIC se computan sobre ese `n`.** El ejecutor reporta ambas cifras —suma cruda de pesos y `n` de muestra— y la constante de escalamiento.
>
> **Sensibilidad S4 obligatoria:** reportar la tabla de BIC **sin pesos**. Si la selección de `k` cambia entre ponderado-reescalado y no ponderado, **se reporta como resultado de primer orden**, no como nota al pie: significaría que la estructura latente depende de a quién se le da peso, que es información sustantiva sobre quién está sub-representado en la solución.

### 5.3 · Casos incompletos

- **(a) Ausencia estructural ≠ dato faltante.** El módulo `trabajos` *"no tiene fila para quien no trabajó"* (§1.1.A). En la sensibilidad S3, la formalidad entra con **tres categorías: `formal` / `informal ocupado` / `no ocupado`** — la tercera es una categoría legítima, **no un faltante que imputar**. Confundirlas sería inventar ocupación donde el instrumento dice ausencia.
- **(b) No respuesta de reactivo en los indicadores:** **FIML** bajo MAR condicional a los indicadores, sin borrado por lista. El supuesto MAR se declara como supuesto y no se defiende como hecho.
- **(c) Se reporta la proporción faltante por indicador ANTES de ajustar.** Si algún indicador supera **10 %** de faltantes, se corre además la solución en **casos completos** y se reportan las dos. El 10 % es umbral **ARBITRARIO declarado antes**.
- **(d) Personas con los siete indicadores faltantes:** se excluyen y **se cuenta cuántas fueron**.
- **(e) No se imputa ningún indicador con un modelo externo.** Imputar es meter estructura ajena antes de medir estructura.

---

## 6 · Traducción del veredicto al canon — la tabla de decisión, escrita antes

### 6.0 · Los dos criterios que la tabla usa, definidos antes de tener resultados

**Criterio de CORRESPONDENCIA (¿una clase "es" un descriptor?).** Una clase recupera un descriptor de `modelo` §1.1.D si su **perfil modal** —la categoría de mayor probabilidad condicional en cada uno de los siete indicadores— **satisface la definición de región de la tabla de §1.1.D**, en las variables que esa fila nombra y sólo en ésas. El emparejamiento es **inyectivo**: dos clases no pueden recuperar el mismo descriptor, y una clase no recupera dos.
- **Techo aritmético: 4 de 6** (§1). El descriptor **3** es trayectoria y el **4** es región no observada; **ninguno de los dos puede recuperarse, y su no-recuperación NO cuenta como evidencia en contra de H-A.**
- **Correspondencia SUFICIENTE = 4 de 4 recuperables** (descriptores 1, 2, 5, 6). **PARCIAL = 2 o 3.** **NULA = 0 o 1.**

**Criterio de DOMINANCIA (¿qué eje separa las clases?).** Un eje domina la separación si es el indicador con **mayor distancia entre clases en sus probabilidades condicionales**, medida como la máxima diferencia absoluta entre clases, y esa distancia es **≥ 1.5 veces** la del siguiente eje. Si ningún eje alcanza ese margen, se reporta **"sin eje dominante"** y no se nombra uno. El **1.5** es **ARBITRARIO declarado antes**.

### 6.1 · La tabla

| # | Desenlace del LCA | Qué se concluye | Qué pasa con los seis descriptores de §1.1.D / §1.1.E |
|---|---|---|---|
| **D1** | **k = 1** seleccionado y estable | **No hay heterogeneidad latente en los seis ejes.** La conjunta no tiene más estructura que sus marginales. H-A y H-B falsadas; **H-C sostenida** | Los descriptores pierden su base empírica **como regiones**. §1.1.D pasa a declarar que las seis regiones son **cortes definidos, no concentraciones observadas**: siguen siendo cortes bien definidos sobre variables reales, pero nada indica que la población se apile en ellos. **Vocabulario, sin sustento estructural.** Requiere ADR |
| **D2** | **k = 2** estable, **dominado por formalidad y/o `est_socio`** | **H-B sostenida: el corpus sobre-segmentó, y queda dicho con dato.** La estructura que los seis ejes sostienen es esencialmente **un contraste socioeconómico**. Confirma con dato lo que INV-SEG p3 §3.A derivó del inventario (`{1∪4}` vs `{2∪3}`) | Descriptores **1 y 2** sobreviven como los polos del contraste. Descriptores **3, 4, 5 y 6** quedan **sin sustento en la estructura observada** y se marcan así en §1.1.D — no se borran (el árbol es append-only) sino que llevan la marca. **Las hipótesis H-02, H-06, H-07 y H-10 de §1.1.E pierden su región condicionante** y bajan a hipótesis sobre ejes continuos, no sobre regiones. Requiere ADR |
| **D3** | **k ≥ 5** estable **con correspondencia SUFICIENTE** (4/4) | **H-A sostenida en lo que puede sostenerse.** Los descriptores nombran concentraciones reales de masa en el espacio de atributos | §1.1.D se conserva **íntegra**, con una nota nueva: los descriptores 1, 2, 5 y 6 tienen **respaldo estructural medido**; el 3 y el 4 siguen **explícitamente sin respaldo posible** con este dato, y eso queda escrito para que nunca se lea "los seis quedaron validados". **Ninguna hipótesis de §1.1.E se promueve de tier por este resultado** — ver §7 |
| **D4** | **k = 3 o 4** estable, **o k ≥ 5 con correspondencia PARCIAL/NULA** | **El dato sostiene segmentación, pero no ésta.** Los ejes que dominan la separación (criterio de dominancia) **son la segmentación que los datos sí sostienen** (`revision §5·P3`, literal) | Los descriptores bajan a **vocabulario histórico**: se conservan como resumen del corpus (§1.1.D dice ya que son *"la forma en que este programa lleva un año hablando de heterogeneidad"*) y **dejan de presentarse como regiones con respaldo**. La sustitución de §1.1.D por regiones derivadas del resultado es **un acto nuevo, de mesa, con su propio encargo** — este pre-registro **prohíbe** que el ejecutor de Fase B reescriba §1.1.D con las clases que le salieron. Requiere ADR |
| **D5** | **INESTABLE** — falla E1, E2 o E3 (§3.5); o S1/S2 cambian la solución | **La prueba no decidió.** Ninguna hipótesis gana | **Nada cambia en el canon.** ⚠️ Y lo importante: **INESTABLE no es apoyo a los seis descriptores.** El statu quo no gana por empate. Se registra como prueba corrida sin veredicto, con el diagnóstico de qué falló. Si S1 muestra que los ejes de hogar dominan, se habilita el **LCA multinivel** de §2.5 como extensión, con enmienda fechada |
| **D6** | **BIC monótono decreciente** en todo 1–8, sin mínimo interior | **Lo que hay es un gradiente, no clases.** El modelo está aproximando un continuo con cortes arbitrarios. **H-C sostenida en su segunda forma** | Mismo efecto que **D1** sobre los descriptores, con un matiz que cambia la lectura: no es que no haya variación —hay mucha—, es que **no está agrupada**. Un espacio de atributos continuo es, de hecho, **exactamente lo que el v4.0 §1.1.B ya afirma** al hacer de los parámetros condicionales sobre un vector en vez de valores por casilla: D6 sería **confirmación del reencuadre y refutación del vocabulario de regiones**. Requiere ADR |

### 6.2 · Lo que NO cambia — bajo ninguno de los seis desenlaces

Esta lista es tan vinculante como la tabla. Se escribe antes para que nadie derive de un resultado de segmentación una conclusión que la segmentación no toca.

1. **Los generadores son agnósticos a la partición.** Los siete generadores de §2.1 y sus quince coeficientes de §2.2 operan sobre **parámetros**, no sobre clases ni perfiles. Ya está establecido y **este resultado no lo toca**. Ninguna cláusula falsable de §2.1 se modifica, ni en ninguno de los seis desenlaces.
2. **El estado de falsación de los generadores no se mueve:** uno probado y sobrevive (G3), uno contradicho (G1b), uno contestado (G2), cuatro sin falsar (G1a, G4, G5, G6).
3. **Los 22 g.l. reales del ajuste (7 + 15) siguen siendo 22** (ADR-51 (b)). Un LCA no añade ni quita grados de libertad al ajuste.
4. **"0 de 14 condicionales medidas" sigue siendo 0.** El LCA **no estima ningún θ_k**: sus indicadores son atributos, no reactivos de parámetros — es la propia condición C3 la que lo garantiza (§2.4). Ningún desenlace de §6.1 mueve ese contador.
5. **El veredicto de identificabilidad de P2/ADR-51 no se toca.** La subidentificación bajo atributos persiste, con su causa en la **medición** y no en la segmentación (ADR-51 (a)). Un resultado favorable de este LCA **no** la alivia: aunque emergieran clases nítidas, seguirían faltando los reactivos co-observados que exige C1–C4. Los 5 inidentificables y los 8 no determinables siguen donde están.
6. **`4 de 144` no se mueve.** Sigue congelado por decisión de mesa (`forense/hallazgos.md`, 31/jul/2026).
7. **La prohibición de §1.1.D sigue vigente**, extendida a clases latentes por §4·b.
8. **La cola alta A/B sigue sin observarse** bajo los seis desenlaces. Ningún `k` la hace aparecer.
9. **Los dos hallazgos que P2 declaró PERSISTENTES persisten:** G3/G5 justo identificados con cero grados de libertad (§3.a) y el check de ADR-30 sin contraste apoyo/obligación dentro del hogar (§3.b). Son problemas del **modelo**, no de la segmentación — el propio `revision §5·P2` lo anticipó y P2 lo confirmó.

---

## 7 · Qué NO decide esta prueba — acotado aquí, no por quien lea el resultado

1. **No valida la maquinaria causal.** Un LCA describe covariación entre siete variables observadas. No dice nada sobre generadores, mecanismos, ni sobre por qué la gente hace lo que hace.
2. **No mide ningún parámetro del modelo.** Cero de las 14 condicionales. Ni una.
3. **No canoniza el corte de edad.** Lo devuelve como subproducto descriptivo (§2.2); fijarlo es acto de mesa.
4. **No mide "cuántos tipos de mexicano hay".** Mide en cuántas clases un modelo de mixtura, con **este** conjunto de indicadores, **estas** categorizaciones, **esta** fuente y **este** criterio, particiona mejor una conjunta. Cambiar cualquiera de los cuatro puede cambiar el número. **El número de clases es una propiedad del modelo ajustado, no un hecho sobre el país.**
5. **Hereda todos los límites del dato**, y ninguno se alivia: la **cola alta A/B no se observa** (§1.1.C límite (i)); tres ejes son de **nivel hogar** y no separan personas del mismo hogar; el **acceso digital** es tenencia binaria de hogar; la **referencia temporal de `residencia`** no está confirmada; el **extremo rural** sigue submuestreado (§1.1.D, descriptor 2); el **sistema indígena-comunal está fuera por diseño** (ADR-10) y ningún `k` lo mete.
6. **Es una fuente, una edición, un año.** ENIGH 2022 nueva serie. No es "el dato mexicano": es un transversal. Un resultado distinto en otra edición sería información, no contradicción.
7. **No cierra ni abre ningún hallazgo del registro congelado**, y no propone hacerlo.
8. **No autoriza a nadie a reescribir `modelo` §1.1.D.** Bajo D2, D4 y D6 el canon cambia — y cambia **por acto de mesa con su propio encargo**, no por la mano del ejecutor de Fase B.

---

## 8 · Módulo de auditoría de rigor extremo

*Módulo completo, las nueve preguntas del Bloque B de `instrucciones-proyecto-v2.md`. **Este artefacto sí afirma sobre México** —pre-dice su estructura social y fija de antemano cómo se leerá el resultado—, así que el módulo aplica entero.*

### 1 · ¿Qué parte confunde pobreza, desigualdad, violencia o informalidad con "cultura"?

**El riesgo central de este protocolo, y hay que decirlo con todas sus letras: una clase latente separada por formalidad e ingreso es ESTRUCTURA ECONÓMICA, NO CULTURA.**

Los siete indicadores son derechohabiencia, edad, lugar de residencia, tamaño de localidad, índice socioeconómico y dos tenencias del hogar. **Ninguno pregunta por valores, creencias, preferencias ni carácter.** Una clase que agrupe a personas sin seguridad social, de localidad pequeña e índice socioeconómico bajo describe **una posición en la estructura económica mexicana** — describe **a qué está expuesta** esa gente, no **cómo es**.

El peligro no está en correr el modelo: está en **cómo se nombra el resultado**. Una clase con prevalencia del 40 % bautizada *"el mexicano popular"* es un estereotipo con cita y tabla de respaldo — y la tabla es real, que es lo que lo hace peligroso. **El protocolo lo impide de antemano con cuatro reglas vinculantes, no con una advertencia:**

> **(R1) Regla de nombre.** Las clases se nombran **exclusivamente por sus coordenadas estructurales modales** — p. ej. *"clase con `segsoc`=2, `tam_loc` ∈ {3,4}, `est_socio` ∈ {1,2}"*. **PROHIBIDO** nombrarlas con adjetivos psicológicos, de carácter o de identidad (*tradicional*, *aspiracional*, *desconfiado*, *conservador*, *precarizado*, *emprendedor*). Un nombre no es una etiqueta cosmética: es la forma en que un resultado sale del documento y entra en la conversación.
>
> **(R2) Regla de prioridad.** **PROHIBIDO** usar los nombres de los seis descriptores para las clases **antes** de que el criterio de correspondencia de §6.0 resuelva, y prohibido usarlos **nunca** para las clases que no recuperen su descriptor. Nombrar la clase 3 *"los Gen Z"* antes de la prueba **es** la prueba, mal hecha.
>
> **(R3) Regla de sujeto.** **PROHIBIDO** reportar prevalencias como *"el X % de los mexicanos son [clase]"*. La forma admitida es *"el X % de la población de 18+ tiene probabilidad posterior modal en una clase caracterizada por [coordenadas]"* — larga a propósito. La forma corta es la que produce el error.
>
> **(R4) Regla de mecanismo, heredada de §1.5.** Si alguna vez se estima un θ_k con nombre psicológico condicionado a estas clases, **rige §1.5 completa**: mecanismo estructural declarado con fuente **más** condición de dominancia. Sin las dos, el diferencial es un rasgo y se rechaza en compilación.

**Y el límite que ninguna de las cuatro elimina, dicho igual que lo dice el v4.0:** el diseño hace la correlación medible sin hacer el mecanismo identificable. Si emergen clases y después se les cuelgan parámetros con nombre psicológico, *"la gente de la clase 2 defiere más"* y *"en un mercado laboral sin salida deferir es lo que conviene"* seguirán siendo indistinguibles con este dato. Las cuatro reglas contienen el daño en el nombre y en la sintaxis del reporte; **no** lo resuelven en la inferencia. Nada en este protocolo lo resuelve.

### 2 · ¿Qué sobregeneraliza desde clases medias urbanas?

**El sesgo de ADR-13 entra aquí por la puerta del peso, y el protocolo lo hace visible en vez de corregirlo.** ENIGH es probabilística y ponderada, así que el sesgo de sobre-muestreo *del corpus* (literatura sobre clasemediero urbano formal) **no** se traslada mecánicamente al dato. Pero sí hay tres vías reales:

- **La cola alta A/B no está**, así que cualquier clase "de arriba" que emerja será **clase media alta, no élite** — y `est_socio`=4 se leerá como "élite" si nadie lo impide. INV-SEG p3 lo dice sin ambigüedad: *"el decil superior de ENIGH **no** es A/B"*. Queda pre-registrado: **prohibido leer `est_socio`=4 como descriptor 4.**
- **El extremo rural sigue submuestreado** (§1.1.D, descriptor 2): una clase rural pequeña puede caer bajo el umbral de prevalencia de E3 y ser descartada como degenerada **por escasez de muestra, no por inexistencia**. Pre-registrado: si una clase cae por E3 y su perfil modal es `tam_loc`=4, **se reporta esa coincidencia explícitamente** en vez de descartarla en silencio.
- **La sensibilidad S4** (ponderado vs. no ponderado, §5.2) es precisamente el diagnóstico de quién está sostenido por el peso y quién por la muestra.

### 3 · ¿Qué está sesgado por marcos o muestras extranjeras?

**Marco (c), y es el único de este artefacto pero es grande:** **todo el aparato de selección de clases es literatura importada** — mixturas finitas, BIC/aBIC, entropía, replicación, tres pasos BCH/ML, la distinción bases/descriptores de Wedel & Kamakura que el v4.0 ya adopta. Se importa **con crítica declarada** (§3.6 nombra los tres puntos donde no aplica limpio: LRT inválido bajo diseño complejo, BIC dependiente del `n` elegido, independencia local violada por construcción). **Ningún veredicto de §6 depende de que este marco sea el correcto**; depende de que se haya declarado antes de ver el dato, que es una propiedad distinta y más barata de garantizar.

**Muestras (b): ninguna.** Este protocolo no toca `familismo_apoyo` ni `familismo_obligacion` ni ningún constructo con procedencia de diáspora — no estima parámetros. **La deuda (b) del programa no se salda ni se agrava aquí; sigue exactamente donde estaba.**

**Y una advertencia sobre importación silenciosa:** la palabra *"clase"* en "clase latente" no es la palabra *"clase"* de "clase social". La coincidencia léxica es una vía de contrabando conceptual y queda señalada.

### 4 · ¿Qué cambiaría con foco rural, indígena o popular?

- **El eje de urbanización se vuelve el eje crítico y es de nivel hogar.** Para un foco rural eso muerde más, *"porque los hogares rurales son más heterogéneos internamente en ocupación"* (§1.1.A/§8·Q4 del v4.0): personas con ocupaciones muy distintas comparten `tam_loc`, `est_socio` y `conex_inte`. La estructura latente que el modelo vea en el México rural estará **comprimida por el instrumento**.
- **`conex_inte` como binario de hogar es más ciego en rural que en urbano.** La diferencia entre tener conexión y usarla es mayor donde la conexión es escasa y compartida; el indicador más débil de los siete es el que peor mide justo donde más importaría.
- **El sistema indígena-comunal sigue fuera por diseño** (ADR-10). Los siete indicadores son de la economía monetaria y del Estado nacional: `segsoc` mide relación con el IMSS, `est_socio` mide ingreso monetizado. **Una clase latente construida con ellos no puede representar un orden institucional distinto — puede, como mucho, representar su ausencia de los registros.** Queda prohibido leer cualquier clase de baja formalidad y baja monetización como "el México indígena".
- **Y sigue en pie lo de siempre:** `ref.A.02` (esfuerzo) y `ref.B.04` (colorismo) siguen entre las ocho refutaciones sin objeto. Este protocolo no añade esas variables ni podría: no están en el vector de §1.1.A.

### 5 · ¿Qué parece psicológico y es un incentivo racional?

**El resultado entero, si se lee mal.** Una partición de la población por derechohabiencia, ingreso y localidad es un mapa de **a quién le tocó qué arreglo institucional**. Si después alguien observa que las clases difieren en conducta, la explicación por defecto disponible —y correcta más veces que la alternativa— es **el arreglo, no el carácter**.

El caso concreto ya nombrado por el canon: **H-01** (horizonte más corto bajo informalidad) es la hipótesis mejor sostenida del conjunto y la que más fácil se lee como impaciencia cultural. *No lo es: quien no sabe cuánto va a ingresar el mes que viene descuenta más el futuro, y eso es aritmética de la volatilidad.* Si este LCA devuelve una clase informal, esa clase **es** el conjunto de gente expuesta a esa aritmética. La regla **R1** de Q1 existe para que el nombre de la clase no diga otra cosa.

### 6 · ¿Dónde hay evidencia débil e intuición fuerte?

Tres lugares, nombrados:

- **El corte de edad.** La intuición de una cohorte joven divergente es fuerte en el corpus (descriptor 5, H-02, H-06, H-07, `R1.4`, `R2.4`, `R5.4`) y **el corte que la operacionaliza no existe en ningún inventario**. Este protocolo usa 18–29 **con procedencia de INV-SEG p3** y declara arbitrarios los otros dos cortes, con sensibilidad obligatoria S2. Es contención, no solución.
- **Que las regiones de §1.1.D sean las regiones correctas.** El propio v4.0 lo pone en su lista de "escrito a mano, sin receta": *"nadie verificó que `est_socio`=3 sea 'clasemediero', y no hay corte publicado que lo sostenga"*. **El criterio de correspondencia de §6.0 hereda ese defecto entero**: mide si las clases caen en regiones **cuya definición es interpretación**. Una correspondencia SUFICIENTE sería evidencia de que las clases caen donde el corpus dijo que caerían, no de que el corpus haya nombrado bien esas regiones.
- **Que los seis ejes sean los ejes que importan.** Son los seis que P1 verificó en una fuente. Que sean **los** ejes de la heterogeneidad mexicana es intuición del corpus, no resultado. §2.0 lo acota declarando fuera de perímetro la pregunta más grande.

### 7 · ¿Qué conclusión sería peligrosa mal usada?

Cuatro, y dos son opuestas entre sí:

- **"El LCA encontró que hay N tipos de mexicano."** La más peligrosa y la más probable. Falsa por §7·4: el número es una propiedad del modelo ajustado con este conjunto de indicadores, esta fuente y este criterio. Las reglas R1–R3 de Q1 existen para que la frase no se pueda formar con el vocabulario del reporte.
- **"Salieron 6 clases, los seis perfiles quedaron validados."** Imposible por construcción y pre-registrada como error **antes** de que exista el resultado: **el techo de recuperación es 4 de 6** (§1, §6.0), porque el descriptor 3 es trayectoria y el 4 es región no observada.
- **"Salieron 2 clases, los perfiles estaban mal."** Tampoco — es la lectura que `revision §7` ya anticipó y que el v4.0 §8·Q7 repite: los perfiles fallan como **bases de asignación exclusiva**; como **descriptores** siguen siendo el resumen del corpus. D2 retira respaldo estructural a cuatro descriptores; **no** convierte un año de síntesis en error.
- **"Ahora la segmentación es empírica, ya no hay que declarar límites."** No. La segmentación sigue heredando la fuente, la unidad, los cortes declarados y la cola alta que no se observa. Un resultado medido es **un supuesto mejor documentado**, no una fotografía.

### 8 · ¿Qué afirmación sobre el estado del corpus no fue derivada, sino escrita a mano?

| Afirmación | Receta · fuente | ¿Derivada? |
|---|---|---|
| El canon vigente es **v4.0** y §1.1 va por atributos | Lectura de `canon/modelo-decision-v4_0.md` en esta sesión | **Sí, leída** |
| **Los seis ejes** con variable, módulo, llave y nivel | **NO derivada aquí — citada** de `modelo` §1.1.A, que la cita de P1 §1–§2. **Esta sesión no abrió el paquete ni ningún descriptor** | **No — citada con su fuente** |
| El corte **18–29** para "joven" | **NO derivada aquí — citada** de INV-SEG p3 §3.A, fila del perfil 5 (`EDAD_V` 18-29) | **No — citada con su fuente** |
| Las **4 celdas** `{1∪4}`, `{2∪3}`, `{5}`, `{6}` y sus debilidades | **NO derivada aquí — citada** de INV-SEG p3 §3.A | **No — citada con su fuente** |
| **C1–C4** y la tabla parámetro × estatus | **NO derivada aquí — citada** de P2 §2.b y §2.d | **No — citada con su fuente** |
| **22 g.l. reales** (7 + 15) y M2/M3 | **NO derivada aquí — citada** de ADR-51 (b) y (c). Este documento **no** re-corrió ningún script sobre `milpa/procedencia.yaml` | **No — citada con su fuente** |
| **0 de 14 condicionales medidas** | **NO derivada aquí — citada** de `modelo` §1.1.F, paso 5 | **No — citada con su fuente** |
| El techo de recuperación es **4 de 6** | **Sí, derivado en esta sesión**: 6 descriptores − descriptor 3 (trayectoria, §1.1.D) − descriptor 4 (región no observada, §1.1.C límite (i)) = 4 | **Sí** |
| Los siete indicadores son **7** (I1–I7) | **Sí, derivado**: 6 ejes de §1.1.A, con el eje 5 desdoblado en `celular` y `conex_inte` porque §1.1.A los nombra como dos variables y §2.1 rechaza construir un índice | **Sí** |
| **Cero contadores movidos** por este artefacto | **Sí, por construcción**: es un pre-registro; no ajusta, no mide, no cierra hallazgos | **Sí** |

⚠️ **Lo escrito a mano en este documento, sin receta, y por tanto lo que hay que vigilar:** **(i)** los cinco umbrales numéricos —2 % de rango de BIC (§3.3.4), 5 arranques (§3.4), correlación 0.90 (§3.5·E2), prevalencia 5 % (§3.5·E3), margen 1.5 (§6.0), 10 % de faltantes (§5.3·c)— son **ARBITRARIOS**; su única defensa es estar escritos antes, y se declaran uno por uno donde aparecen; **(ii)** los cortes de edad 44/59 son arbitrarios (§2.2); **(iii)** el universo de **18+** es decisión declarada de esta sesión, no criterio heredado; **(iv)** el criterio de correspondencia de §6.0 es **interpretación** de la tabla de §1.1.D, cuya propia definición el v4.0 ya declaró escrita a mano. Ninguno de los cuatro se presenta como derivado.

### 9 · ¿Qué restricción o deuda hereda este artefacto sin verificar?

**Contadores movidos por este artefacto: cero.** Es un pre-registro: no mide, no ajusta, no cierra hallazgos, no toca `4 de 144`, no toca `0 de 14`, no toca los 22 g.l. Lo único que produce es un compromiso.

Cuatro deudas heredadas, nombradas:

- **P1 no se re-verificó**, igual que en el v4.0. Todo nombre de variable, catálogo y llave viene de §1.1.A, que viene de P1. **Si P1 se equivocó en un nombre de campo, este protocolo hereda el error** y el ejecutor de Fase B será el primero en topárselo — se le pide expresamente que **lo reporte como hallazgo**, no que lo corrija en silencio.
- **El factor de expansión y las variables de diseño no están inventariadas por nadie** (§5.1). Es la deuda más operativa: el protocolo depende de ellas y el canon no las trae. **Se declara como hueco y se ordena derivarlas antes de ajustar** — no se teclean aquí.
- **La regla de construcción de `est_socio` no está verificada** (§2.4). Si es función determinista de `ing_cor`, el indicador I5 es ingreso con otro nombre y la lectura del resultado cambia. **Se ordena reportarlo; no se asume en ninguna dirección.**
- **La restricción "sesión limpia" se hereda parcialmente verificada.** Esta sesión verificó que **ella** no abrió fuentes (§0). No pudo verificar —ni le corresponde— el estado de contaminación de la sesión que ejecute Fase B. **ADR-46 fija que la unidad de contaminación es la SESIÓN, no la máquina**: por tanto la sesión ejecutora **puede** abrir el microdato sin invalidar este pre-registro, precisamente porque el protocolo ya está sellado y fechado antes que ella. **Esa es la propiedad entera del artefacto y el motivo de que el sello vaya en la cabecera.**

---

## 9 · Instrucciones de ejecución para Fase B — el contrato, en una lista

1. **Verifica las premisas de este pre-registro antes de obedecerlo** (ADR-39). Si alguna no se sostiene contra el archivo, **detente y repórtalo**: encontrar que un pre-registro estaba mal fundado es un entregable.
2. **Deriva y reporta antes de ajustar:** `n` del universo 18+, factor de expansión y variables de diseño (§5.1), suma cruda de pesos y constante de reescalamiento (§5.2), proporción de faltantes por indicador (§5.3·c), y si `est_socio` es función de `ing_cor` (§2.4).
3. **Ajusta k = 1…8** con ≥500 arranques (§3.4) y **publica la tabla completa de los ocho**, no sólo la elegida (§3.2).
4. **Aplica la regla de decisión de §3.3 en su orden, sin discreción.** Reporta k−1, k, k+1 con perfiles completos.
5. **Corre las cuatro sensibilidades obligatorias:** **S1** sólo indicadores de persona (§2.5·c) · **S2** partición de edad alternativa (§2.2) · **S3** formalidad por módulo `trabajos` con tres categorías (§2.4, §5.3·a) · **S4** sin pesos (§5.2).
6. **Evalúa E1/E2/E3** (§3.5) y **el criterio de correspondencia y de dominancia** (§6.0) **antes** de escribir una sola línea de conclusión.
7. **Lee el veredicto en la tabla de §6.1.** No inventes un desenlace que no esté ahí; si el resultado no cae en ninguno de los seis, **eso es una enmienda** (§10), no una interpretación libre.
8. **Respeta §4 completo:** sin asignación modal, sin columna de etiqueta dura, tres pasos con corrección si hay desenlace.
9. **Respeta R1–R4 de §8·Q1** al nombrar y reportar las clases. Es vinculante, no estilístico.
10. **No reescribas `modelo` §1.1.D.** Ninguno de los seis desenlaces te autoriza a hacerlo (§7·8).

---

## 10 · Enmiendas

**Ninguna a la fecha del sello.**

> **Regla de enmienda, que es la propiedad entera de un pre-registro:** cualquier cambio posterior al protocolo —umbrales, indicadores, rango de `k`, regla de decisión, tabla de §6.1, criterios de §6.0— **se anexa aquí como enmienda fechada y firmada, con el texto viejo visible y la razón del cambio**. **Nunca como edición silenciosa del cuerpo.** Una enmienda posterior al primer ajuste **se marca además como POST-DATO** y todo veredicto que dependa de ella se reporta como **exploratorio**, no como pre-registrado.
>
> El cuerpo de este documento queda **sellado el 3 de agosto de 2026**, antes de que ninguna fuente fuera abierta.

---

*Escrito por una sesión que no abrió un solo dato. Ese es el único mérito que reclama, y es el que lo hace utilizable.*
