# Cruce catálogo × fichas del Hito D — v1.0

**Clase: PROPUESTA. No es decisión y no autoriza ninguna medición.**

> **LÍMITE DURO.** Ninguna celda de esta tabla afirma que una variable exista. Afirma que un instrumento cubre un dominio. La viabilidad real solo se confirma abriendo el instrumento, y eso va después del pre-registro.

**Fecha:** 4 de agosto de 2026 · Mesa #19 · Encargo T
**Reemplaza (como insumo, no como cita):** `cruce-catalogo-fichas-2026-07-30.md`, documento vivido solo en el espejo del proyecto, sin sello de commit, tipo (2) — nunca entró al repo. `git log --all -- '*cruce-catalogo*'` no lo encuentra en ninguna rama ni commit borrado, verificado de nuevo en esta sesión.
**Entorno de esta sesión:** Nube, sin red a ningún host de datos, ningún instrumento abierto. Todo lo que sigue es lectura de `data/catalogo-fuentes-v1_0.md`, `data/inventarios/*.md` y `forense/hitoD-preregistro-v2_0.md` — los dos insumos que ya están en el repo.

---

## 0 · Qué hace este documento y qué no

Dos tablas:

- **§4 — Tabla A.** Reconstrucción del cruce original: las fichas del Hito D que **no** declaran fuente, cruzadas contra el catálogo, preguntando *"¿hay alguna candidata?"*.
- **§5 — Tabla B, el complemento.** Las fichas que **sí** declaran fuente, cruzadas contra el catálogo con la pregunta invertida: *"¿es la mejor que tenemos, y qué otras candidatas hay?"*. Éste es el punto de este encargo — el hueco que el §4 del documento del espejo declaró explícitamente sobre sí mismo: *"No cubre las 10 fichas que sí declaraban fuente."*

No edita ninguna ficha, no adjudica ni retira ningún veredicto, no descarga nada, no escribe un test, no toca `forense/hallazgos.md`. Ver §8.

---

## 1 · Procedencia

| Clase | Qué |
|---|---|
| (1) | `main` = `31fc671`. Contenido de `data/catalogo-fuentes-v1_0.md`, `data/inventarios/` (10 archivos), `forense/hitoD-preregistro-v2_0.md`. Ausencia del cruce anterior en el repo, verificada por `git log --all` sobre `*cruce*`. Ausencia de `catalogo-fuentes`, `catalogo_unico` e `inventarios` en `tests/check.py`, verificada por grep exacto de los tres términos (0 ocurrencias cada uno). |
| (2) | `cruce-catalogo-fichas-2026-07-30.md` (espejo, sin sello). Insumo a re-derivar, no fuente de cifras. Ninguna cifra suya se copia en este documento; donde una cifra re-derivada difiere de la que circulaba, se reporta como hallazgo (§7), no se ajusta. |
| (3) | Nada. |

---

## 2 · Receta de conteo — verificada, no asumida

```
grep -cE "^## R[0-9]" forense/hitoD-preregistro-v2_0.md
```

Da **27**. La receta ingenua `grep -c "^## R"` da **28** — cuenta también `## Registro de veredictos archivados`. Ambas cifras verificadas en esta sesión contra el archivo tal como está hoy (`c9e67bd`-y-posteriores en la rama que fusionó a `main`, HEAD real `31fc671`).

Las 27 fichas, listadas por posición en el archivo (no reordenadas):

`R1.1 · R1.2 · R1.3 · R1.4 · R2.1 · R2.2 · R4.1 · R4.2 · R4.3 · R5.1 · R5.2 · R7.1 · R7.2 · R7.3 · R7.4 · R7.5 · R8.1 · R8.2 · R8.3 · R9.1 · R9.2 · R10.1 · R10.2 · R10.3 · R3.2 · R3.1 · R3.4`

(Las últimas tres viven en Notas 4, 14 y 15 — append-only, no reordenan el cuerpo.)

**Nota aparte, no perímetro de este acto:** `CAL-G3` (Nota 7) no es una ficha `R` — pre-registra una estimación de coeficiente de generador, no un falsador de regla, y su propio texto declara que vive fuera del namespace `R`. No cuenta en los 27. Se usa en §6 como segundo caso de control porque el encargo lo pide explícitamente, no porque compita por un lugar en la tabla.

---

## 3 · Criterio de "declara fuente" — declarado antes de contar

**Cuenta como declarar fuente:** la ficha nombra, en su bloque `Serie/Año/Corte` (si lo tiene) o en cualquier fila de su escala A–D, un instrumento público identificable por sigla o institución (ENIGH, ENCIG, ENVIPE, ENUT, ENIF, CONSAR, Banxico/SPEI/CoDi, ENSANUT) como candidato para medir el falsador.

**No cuenta:**
- una población o universo nombrado sin instrumento (`R1.1`: "Fondos de Aseguramiento agrícola" es un *dónde*, no una fuente);
- un tipo de dato genérico ("dato propietario", "panel organizacional", "registro sistemático") sin instrumento nombrado;
- un estudio académico no instrumental, aunque tenga cita textual (`R10.1`: Félix-Brasdefer, muestra Tlaxcala — es un paper, no un instrumento del catálogo; se anota aparte);
- una referencia a un identificador interno del corpus sin fuente resuelta (`R8.3`: `conf.06`, que la propia ficha declara abierto y no usable).

Bajo este criterio: **8 de 27 declaran fuente, 19 no declaran.**

Esta cifra **no coincide** con el "10 declara / 15 no declara" que circulaba en el espejo (calculado sobre 25 fichas, con un criterio que ese documento no dejó escrito). La discrepancia es esperable y se reporta, no se concilia: distinto denominador (25 vs. 27) y distinto criterio (no escrito vs. escrito arriba).

---

## 4 · Tabla A — Fichas sin fuente declarada × catálogo

Búsqueda hecha contra los 10 inventarios de `data/inventarios/` y el resumen de `data/catalogo-fuentes-v1_0.md` (119 fuentes únicas, 38 operables). Para cada ficha: dominio del falsador, si el catálogo trae una candidata, y cuál. **"Candidata" = cubre el dominio. No implica que la variable exacta exista** — eso es lectura de instrumento, fuera de perímetro.

| Ficha | Dominio del falsador | ¿Candidata en catálogo? | Candidata(s) | Nota |
|---|---|---|---|---|
| `R1.1` | Seguro agrícola de productores de temporal, volatilidad máxima | **No** | — | Ninguno de los 10 inventarios cubre financiamiento/seguro agropecuario como dominio propio. El veredicto ya archivado (`D`, Nota 5) usó SADER/AMUCSS — fuentes fuera de los 10 inventarios, encontradas por búsqueda directa, no por este catálogo. El catálogo tiene un hueco de dominio aquí, no solo de dato. |
| `R1.3` | Penetración fintech 100% digital, brecha rural-urbana, referidos | **Sí** | `ENIF` (conocimiento/uso de herramientas de pago digitales, por tamaño de localidad) · `ENDUTIH` (uso de tecnología, urbano/rural, por entidad) | Ninguna mide "penetración de una fintech específica" ni aísla programas de referidos — dan proxy de adopción digital financiera general, no el instrumento exacto que el Umbral pide. |
| `R1.4` | Consumo compensatorio D/E, panel de consumo popular | **Parcial** | `ENIGH` (bienal, por decil) | La ficha exige panel; ENIGH es transversal repetido, no panel de las mismas unidades — no cumple la condición explícita del falsador (`C exigiría panel... — hueco declarado`). El catálogo confirma el hueco, no lo cierra. |
| `R2.1` | Empresa familiar mexicana, tasa de reporte voluntario de errores | **No** | — | Ningún inventario (trabajo-ingreso, capital social) cubre clima organizacional o disenso ascendente por tipo de empresa. Confirma el `D` pre-registrado. |
| `R2.2` | Clima organizacional, rotación por tipo de liderazgo | **No** | — | Mismo resultado que `R2.1`. `ENESTYC` (empleo/salarios/tecnología manufactura) está descontinuada y es a nivel establecimiento, no mide clima. |
| `R4.1` | Farmacia con consultorio vs. clínica pública, trato percibido | **Sí, no considerada por la ficha** | `ENSANUT` (utilización y cobertura de servicios de salud) | Ver §7 — ésta es una de las cuatro fichas de salud que el catálogo cubre sin que la ficha nombre la fuente. `ENSANUT` no tiene, hasta donde el catálogo declara, un ítem propio de "trato percibido" separable de uso — el propio confusor de la ficha queda sin resolver aunque exista candidata. |
| `R4.3` | Desabasto/adherencia (mitad A); familia cuidadora/adherencia (mitad B) | **Sí, no considerada** | Mitad A: `ENSANUT` (medicamento surtido, autorreporte). Mitad B: `ENASIC` (población cuidadora, 2022) | La ficha exige adherencia por surtimiento, no autorreporte (`D si solo hay adherencia auto-reportada`) — ninguna candidata del catálogo mide surtimiento farmacéutico a nivel persona; probable `D` se sostiene para la mitad A incluso con candidata de dominio. |
| `R7.1` | Participación en elecciones concurrentes vs. no concurrentes, mismo electorado | **Sí, no considerada** | Resultados electorales del INE (`Sistema de Consulta de la Estadística de las Elecciones`), registro administrativo por casilla/sección | Es dato agregado por casilla, no encuesta de individuos — permite el contraste de participación a nivel sección/municipio que el Umbral pide, pero la ficha no lo nombró. |
| `R7.3` | RDD sobre Pensión del Bienestar, efecto electoral independiente de aprobación | **Parcial** | `ENIGH` (identificación de hogares beneficiarios, mismo método que usó `R5.1`, Nota 16) + resultados electorales del INE (agregado por sección) | Ninguna combinación pública liga beneficiario individual con voto individual — el RDD que la ficha pide exige vinculación que estas dos fuentes, por separado, no dan. Confirma la fila `D` de la propia ficha ("el diseño es concebible, solo no se ha hecho"), con un poco más de precisión sobre por qué. |
| `R7.4`/`R7.5` | Registro de respuestas colectivas (protesta/autodefensa) por entorno | **No** | — | Ningún inventario de seguridad, capital social o cultura cubre un registro codificado de eventos de protesta/autodefensa. Confirma `D`. |
| `R8.1` | Comités con/sin mecanismo de sanción, contribución sostenida | **No** | — | `RFOSC/CLUNI` (registro de organizaciones civiles) no distingue mecanismo de sanción ni contribución. No es candidata útil. |
| `R8.2` | Tandas digitales, tasa de incumplimiento por plataforma | **No** | — | Dato de plataforma fintech, propietario por naturaleza. Ningún inventario lo cubre. Confirma `D`. |
| `R8.3` | Confianza en desconocidos según enforcement, `conf.06` | **No (mismas 5 ya conocidas rotas)** | `ENCUCI` · `LAPOP` · `Latinobarómetro` · `WVS` · `ENCUP` | Éstas son, con alta probabilidad, las mismas cinco cifras de confianza interpersonal que `conf.06` ya declara en conflicto entre sí (`10.3 puntos` de diferencia, dos que dicen ser la misma ENCUCI 2020). El catálogo no aporta una sexta candidata nueva — confirma que el problema es de reconciliación, no de ausencia. |
| `R9.1` | Consulta a experto vs. allegado, acceso objetivo documentado | **Parcial** | `ENSANUT` (utilización de servicios de salud) | Mide uso de servicios, no la comparación explícita "consultó al experto vs. prevaleció el allegado" que el Umbral pide. Candidata de dominio, no de variable. |
| `R9.2` | Cobertura vacunal/servicio, auditada por tercero | **Sí, no considerada** | `ENSANUT` (serología vacunal, cobertura) | La ficha exige métrica **auditada**, no autorreportada por el prestador — el catálogo no distingue esa propiedad sin abrir el instrumento; candidata de dominio con la misma reserva que `R4.1`/`R4.3`. |
| `R10.1` | Rechazo indirecto fuera de población universitaria | **No** | — | Ningún inventario cubre estudios de pragmática/comunicación con muestra nacional. El ancla sigue siendo el estudio académico de Tlaxcala citado en la propia ficha — no un instrumento del catálogo. |
| `R10.2` | Retroalimentación pública/privada, rotación por sector | **No** | — | Mismo resultado que `R2.1`/`R2.2`. |
| `R10.3` | Disposición a testificar, protección efectiva a testigos | **Parcial, con reserva ética ya declarada por la ficha** | `ENVIPE` / `ENSU` (percepción de seguridad, contacto con autoridades) | Ninguna mide "disposición a testificar tras protección efectiva" como contraste pre/post. La ficha ya declara que solo dato secundario publicado es admisible — ninguna candidata del catálogo cumple esa condición para este contraste específico; el `D` preferible que la ficha ya declara se sostiene. |

**Cifra derivada:** de las 19 fichas sin fuente declarada, **6 tienen candidata de dominio no considerada** (`R1.3`, `R4.1`, `R4.3`, `R7.1`, `R9.2`, y parcialmente `R9.1`/`R7.3`/`R10.3`/`R1.4`), y **9 no tienen ninguna** (`R1.1`, `R2.1`, `R2.2`, `R7.4`, `R7.5`, `R8.1`, `R8.2`, `R8.3`, `R10.1`, `R10.2` — diez, en realidad, contando `R7.4` y `R7.5` por separado). Esto **no reproduce** el "11 de 15" del espejo — denominador distinto (19 vs. 15), y el espejo no declaró su propio criterio de "candidata" con el detalle de arriba.

---

## 5 · Tabla B — El complemento: fichas con fuente declarada, pregunta invertida

Las 8 fichas que declaran fuente. Para cada una: la fuente declarada, las candidatas del catálogo que el falsador no consideró, y si alguna es mejor **para el umbral concreto de esa ficha** — no en abstracto.

### R1.2 · Estabilidad → planeación larga

| Fuente declarada | Candidatas no consideradas | ¿Mejor para este umbral? |
|---|---|---|
| CONSAR (aportación voluntaria, agregado) + ENIF (tenencia/uso, microdato) | `ENSAFI` (2023 — deuda, ahorro, crédito formal/informal, metas y estrés financiero, microdato) · `ENFIH` (2019, única edición — acervos y flujos de activos/pasivos financieros) | **No.** El Umbral pide `<15%` de formales estables con ingreso suficiente que hagan aportación voluntaria a AFORE **o** contraten seguro privado — ENIF es el único instrumento del catálogo diseñado explícitamente para esa tenencia cruzada con formalidad laboral, y es la edición más reciente (2024) de las tres. `ENSAFI` mide comportamiento y estrés financiero, no tenencia de instrumento por formalidad, y es de 2023. `ENFIH` es de 2019, edición única, sin actualización. Ninguna reemplaza a ENIF; `ENSAFI` es candidata razonable de **triangulación**, no de sustitución. |

### R3.1 · Trámite presencial discrecional sin registro → mordida

| Fuente declarada | Candidatas no consideradas | ¿Mejor para este umbral? |
|---|---|---|
| ENCIG 2023 (misma edición que R3.2) | `ENCOAP` (confianza en administración pública, urbano, bienal) · `CNARTyS` (catálogo de trámites, no de experiencia) | **No.** `ENCOAP` mide confianza y satisfacción, no incidencia de mordida por grado de discrecionalidad — no es sustituto. `CNARTyS` es un inventario de trámites (el universo de qué existe), no una medición de experiencia ciudadana; útil como denominador de tipos de trámite, inútil como fuente del falsador. ENCIG sigue siendo el único instrumento del dominio con incidencia de corrupción medida a nivel persona. |

### R3.2 · Digitalización/testigos/registrable → baja la mordida

| Fuente declarada | Candidatas no consideradas | ¿Mejor para este umbral? |
|---|---|---|
| ENCIG 2023 (veredicto `B` ya archivado, Nota 6) | Mismas dos de `R3.1` arriba | **No**, por la misma razón. Esta ficha ya corrió y archivó veredicto — el complemento aquí solo confirma que ninguna candidata alternativa habría cambiado la elección de fuente antes de correr. |

### R3.4 · CoDi rechazado vs. SPEI adoptado — el gate

| Fuente declarada | Candidatas no consideradas | ¿Mejor para este umbral? |
|---|---|---|
| Series transaccionales de Banxico (condición A) + ENIF como Respaldo 1 | `ENDUTIH` (tenencia de smartphone, acceso a internet, uso de apps, por nivel socioeconómico) | **No para la condición A** — nada sustituye a la serie transaccional de Banxico para medir adopción relativa CoDi/retail-efectivo. **Posiblemente útil, y no considerada, para el confundidor 2** (Bloque C de la propia ficha: *"coerción/riesgo fiscal y fricción de uso covarían por diseño del producto... no hay forma de aislarlo con las series agregadas fijadas"*). `ENDUTIH` no resuelve el gate, pero podría dar una medida independiente de **capacidad de fricción** (tenencia de smartphone, datos, familiaridad con apps por nivel socioeconómico) que la ficha, con las fuentes que fijó, declaró irresoluble. Esto **no cambia la fila de la escala** — el Respaldo 2 de la propia ficha ya pre-declara B/C como probablemente inejecutables con las fuentes fijadas, y ENDUTIH no estaba entre ellas — pero es la candidata más informativa de las ocho filas de esta tabla: apunta a una vía que la ficha no cerró por no buscar, no por no existir. Se reporta como hallazgo, no se reabre la ficha (sellada). |

### R4.2 · Hombre sin permiso laboral → pospone el chequeo

| Fuente declarada | Candidatas no consideradas | ¿Mejor para este umbral? |
|---|---|---|
| ENSANUT 2023 (desagregada por sexo × permiso laboral × posposición) | `ENOE` (acceso a instituciones de salud por condición laboral, módulo INEGI listado) | **No.** ENOE da condición laboral y derechohabiencia, no conducta de posposición del chequeo — le falta el desenlace conductual que el Umbral pide. ENSANUT sigue siendo la única fuente que podría, en principio, cruzar las tres dimensiones (sexo, permiso laboral, posposición) en el mismo instrumento. |

### R5.1 · Volatilidad + ausencia de Estado → familia como seguro

Caso de prueba del encargo — desarrollo completo en §6.

| Fuente declarada | Candidatas no consideradas | ¿Mejor para este umbral? |
|---|---|---|
| ENIGH (6 olas 2012–2022, veredicto propuesto `A`, Nota 16, no adjudicado) | `ENASEM/MHAS` (panel, 50+, olas 2018 y 2021 flanqueando la reforma) · `ENNViH/MxFLS` (panel, tres olas 2002–2012, ya declarada para `CAL-G3`) | **Depende de qué exige el falsador — ver §6.** El Umbral (línea 143) pide corte transversal beneficiario/no-beneficiario, que es exactamente lo que Nota 16 corrió con ENIGH. La fila `C` pide panel — condición distinta, no mejora del mismo desenlace. `ENASEM` es la única candidata que podría correr el contraste **tal como la fila C lo pide** (panel, mismas unidades, antes/después del choque). `ENNViH` no sirve para esta ficha — sus olas terminan en 2012, antes del choque de 2019. |

### R5.2 · Cuidado → mujeres 40+

| Fuente declarada | Candidatas no consideradas | ¿Mejor para este umbral? |
|---|---|---|
| ENUT (cruzada con ocupación y composición del hogar) | `ENASIC` (Encuesta Nacional para el Sistema de Cuidados, 2022, edición única — población cuidadora de 15+, población susceptible de recibir cuidados) | **No claramente, y por una razón específica al umbral.** El Umbral exige la reducción en horas de cuidado de la mujer 40+ **cuando ella misma pasa** de no ocupada a ocupada formal de tiempo completo, con varón adulto disponible — un contraste dentro del mismo instrumento entre horas de cuidado y ocupación de la misma persona. `ENASIC` está más especializada temáticamente en carga de cuidado que ENUT (que es un diario de tiempo general), pero el catálogo no confirma, sin abrir el instrumento, que mida ocupación formal de tiempo completo de la persona cuidadora con el detalle que el confundidor de disponibilidad del varón exige — y su muestra (7,021 viviendas, sin desagregación estatal, edición única) es menor que la de ENUT (~40,000 viviendas en 2019). ENUT sigue siendo el mejor ajuste porque mide horas y ocupación en el mismo instrumento; `ENASIC` es candidata de **triangulación futura**, no de sustitución. |

### R7.2 · Delito sin seguro → no denuncia

| Fuente declarada | Candidatas no consideradas | ¿Mejor para este umbral? |
|---|---|---|
| ENVIPE (veredicto `D` archivado; Notas 11–13 ya agruparon 8 olas 2018–2025) | `RNID` (Registro Nacional de Incidencia Delictiva, administrativo) · `ENVE` (victimización de empresas) | **No.** `RNID` es registro de denuncias — no observa a quien no denuncia, así que no puede medir la brecha que el Umbral pide por construcción. `ENVE` mide unidades económicas, no personas. ENVIPE sigue siendo la única fuente pública con el contraste denuncia × cobertura de seguro × tipo de delito a nivel persona, y ya fue explotada exhaustivamente (Notas 11–13) sin que ninguna candidata alternativa hubiera cambiado esa elección. |

---

## 6 · Casos de control — el punto que valida (o invalida) el procedimiento

### 6.1 · Caso positivo: `R5.1` y `ENASEM/MHAS`

**Por qué el procedimiento tiene que marcar esta fila, o está mal.**

La fila `C` de `R5.1` (línea 149) dice: *"exigiría panel de hogares pre/post con corresidencia observada"*. El catálogo trae, con marcas `[verificado]` propias (`data/inventarios/inventario_fuentes_salud_mexico.md:164-176` y duplicado en `inventario-fuentes-credito-ahorro-finanzas-hogar-mexico.md:150-160` y en `inventario_fuentes_uso_del_tiempo_cuidados_hogar_mexico.md:136-146`):

- `ENASEM/MHAS`: **panel** `[verificado]`, población 50 años y más, rondas 2001-2003-2012-2015-**2018**-**2021**-2024. Las rondas 2018 y 2021 flanquean exactamente la universalización de la Pensión del Bienestar (2019), el mismo choque exógeno que `R5.1` usa como disparador de vuelco.

Esto **satisface literalmente** lo que la fila `C` pide: hogares, panel, mismas unidades, antes y después del choque. Ninguna ficha de este perímetro lo había considerado — la propia Nota 16, que corre `R5.1` con ENIGH, no menciona ENASEM. El procedimiento de esta tabla lo marca en la fila de `R5.1` (§5, arriba). **Si no lo hubiera marcado, el procedimiento estaría mal, no el resultado** — exactamente la condición que el encargo puso por escrito.

**Lo que esto no dice.** Que ENASEM cubra el dominio no dice que el veredicto cambie. El Umbral de la ficha (línea 143) pide la comparación **transversal** beneficiario/no-beneficiario — la misma que Nota 16 ya corrió con ENIGH, con propuesta `A`. Un panel no mejora esa lectura: la responde de otra forma. Si mesa decidiera correr `R5.1` también contra ENASEM, produciría una prueba **distinta y adicional** (dentro-de-hogar, pre/post) — no una corrección de la que ya corrió. Y `ENASEM` limita la ficha a hogares con integrante de 50+, mientras `R5.1` no acota la regla por edad del hogar — correr contra ENASEM cambiaría también la población, no solo el diseño. Esto no está en la ficha ni se decide aquí (sellada); se reporta como hallazgo para que mesa lo pese.

### 6.2 · Caso negativo: `ENNViH/MxFLS`

**Por qué no sirve para `R5.1`, dicho con la misma cifra que ya está en el pre-registro.** `ENNViH` está declarada como fuente en `hitoD-preregistro-v2_0.md:484` (`CAL-G3`, no una ficha `R`), descrita ahí mismo como panel longitudinal de tres olas (2002 · 2005-06 · 2009-12). El límite de época que la propia ficha `CAL-G3` declara en su punto (9c) (línea 513) — *"el panel cierra en 2012... NO extrapolable al México de 2026"* — es exactamente por qué no sirve para `R5.1`: el choque que `R5.1` necesita (universalización de la Pensión del Bienestar, 2019) ocurre **siete años después** de que el panel terminó de levantar. No es un problema de variable (el roster de hogar de `ENNViH`, usado en `CAL-G3` vía el Libro C, sí traería corresidencia observable) — es un problema puramente temporal: no hay ola de `ENNViH` de ningún lado del choque.

**Por qué sí podría servir para otras reglas de §3.5.** `R5.2` (cuidado → mujeres 40+) no depende de un choque fechado — su mecanismo (estructura de oportunidad vs. guion normativo) no exige una ventana temporal específica, a diferencia de `R5.1`. La ventana 2002-2012 de `ENNViH` no sería una limitación temporal ahí como sí lo es para `R5.1`: podría servir como **línea base histórica de robustez** (¿el patrón de `R5.2` ya aparecía en 2002-2012, con la estructura ocupacional de esa época?), usando el mismo roster de hogar (`TB` para ocupación, composición del hogar para disponibilidad del varón) que `CAL-G3` ya validó como legible. **Esto no está verificado a nivel de variable** — el catálogo no confirma que `ENNViH` mida horas de cuidado explícitamente (§5, fila `R5.2`, ya señala que ningún módulo de cuidado propio aparece en la descripción del catálogo) — así que esta candidata queda como **hueco a explorar, no como hallazgo cerrado**.

---

## 7 · Corrección de rumbo: la cifra "cuatro fichas dependen de una fuente no nombrada"

Contra lo verificado en Tabla A: `R4.1`, `R4.3`, `R9.1` y `R9.2` son, en efecto, las cuatro fichas de salud cuyo dominio el catálogo cubre (`ENSANUT`) sin que la ficha nombre la fuente — exactamente la cifra que el encargo citaba. Se reporta aquí como confirmación derivada en esta sesión, no como cifra heredada del espejo: las cuatro se verificaron una por una en §4, con la misma reserva en las cuatro — `ENSANUT` da candidata de **dominio**, no de la variable exacta que cada Umbral pide (trato percibido, adherencia por surtimiento, consulta-vs-allegado, cobertura auditada por tercero). Ningún veredicto se infiere de esto; es un hallazgo de cobertura, no de viabilidad.

---

## 8 · Lo que este acto no hace

- No edita ninguna ficha de `hitoD-preregistro-v2_0.md`. El pre-registro está sellado (append-only); toda observación de arriba es hallazgo, no corrección de fuente.
- No adjudica ni retira ningún veredicto. `R5.1` sigue con propuesta `A` no adjudicada (Nota 16); `R3.2` y `R7.2` siguen con sus veredictos archivados intactos.
- No descarga nada. Ninguna URL de este documento se consultó como red — todo el contenido viene de los inventarios ya escritos en `data/inventarios/`.
- No escribe un test. El catálogo sigue sin vigilancia de `tests/check.py` — ver §0 del encargo. Se deja constancia, no se instrumenta aquí.
- No toca `forense/hallazgos.md` — perímetro del Encargo S (ENASEM), concurrente en un worktree separado.
- No toca `canon/`, el bloque append-only del pre-registro, ni `data/manifiesto.yaml`.

---

## 9 · Módulo de auditoría

**¿Qué parece propiedad de la regla y es propiedad de la búsqueda?** Las cuatro fichas de §7 no declaraban `ENSANUT` porque nadie cruzó el catálogo contra ellas antes de este acto — no porque la fuente no exista o no aplique. Es la misma clase de error que el propio encargo nombra en su §6: una ausencia registrada como atributo del falsador cuando era atributo del esfuerzo de búsqueda.

**¿Qué sería una conclusión peligrosa simplificada?** *"6 de 19 fichas sin fuente tienen candidata, y 1 de 8 con fuente tiene una candidata mejor (R3.4/ENDUTIH parcial) — luego el catálogo ya resolvió el Hito D."* No: cubrir un dominio no es medir un umbral, y `R3.2` ya demostró en este mismo pre-registro que tener fuente y tener candidata no evita que el gate salga aritméticamente inalcanzable. Las cifras de este documento son de **cobertura**, no de **viabilidad**.

**Deuda que caduca, heredada del encargo y no resuelta aquí:** (1) la ausencia de fuente en `R4.1`/`R4.3`/`R9.1`/`R9.2` como posible propiedad no registrada como decisión — sigue abierta; (2) el hallazgo de `R3.4`/`ENDUTIH` como vía no explorada para el confundidor de fricción — sigue abierto; (3) si mesa decide correr `R5.1` también contra `ENASEM`, eso es un acto de mesa aparte, no una instrucción de este documento.

**Contadores registrados movidos por este acto:** cero. Este documento es de cobertura de catálogo, no de medición — no corre ningún falsador, no abre ningún microdato, no cierra ninguna fila de escala. Congruente con §0 del encargo: el catálogo mismo, hasta que alguien lo cruce, no mueve contadores; cruzarlo tampoco los mueve — solo dice dónde buscar después.
