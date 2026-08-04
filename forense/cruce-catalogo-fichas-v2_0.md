# Cruce catálogo × fichas — v2.0

> | | |
> |---|---|
> | **ARCHIVO** | `cruce-catalogo-fichas-v2.0.md` |
> | **REEMPLAZA A** | `cruce-catalogo-fichas-v1_0.md` — **no se edita, queda como está, este acto lo supersede con nota** |
> | **VERIFICAS ASÍ** | contiene una fila por **condición del Umbral**, no una por ficha, para las 27 fichas de `hitoD-preregistro-v2_0.md` |
> | **NOMBRE ESTABLE** | **`cruce-catalogo-fichas`** |

**Nota de sucesión, no de reemplazo.** `forense/cruce-catalogo-fichas-v1_0.md` (4/ago/2026,
mismo día) preguntaba *"¿hay alguna fuente que cubra el dominio?"* sobre las 18 fichas sin fuente
declarada. Ese documento **no se edita** (append-only, `forense/` — CONTRIBUTING §3) y sigue
siendo válido para lo que midió. Este documento pregunta otra cosa, sobre las 27: **¿qué fuente
construye CADA CONDICIÓN del Umbral, con qué granularidad, y enlaza con las demás condiciones en
la misma unidad de observación?** Es una pregunta más fina, no una corrección de la anterior.

**Límite duro, heredado literal de v1.0 y no relajado aquí:** ninguna celda de esta tabla afirma
que una variable exista. Afirma que un instrumento cubre una condición del Umbral, a la
granularidad declarada. Confirmar la variable exige abrir el instrumento — eso no es parte de
este acto.

**Insumo:** `data/catalogo-fuentes-v2_0.md` (131 fuentes únicas, 11 inventarios, incluida la
dimensión de clase) y `forense/hitoD-preregistro-v2_0.md` (27 fichas + 25 notas fechadas al
4/ago/2026, incluidos los 8 veredictos ya archivados).

---

## Veredictos, los cuatro valores y su lectura

- **VIABLE** — todas las condiciones de la ficha son construibles y enlazables en la **misma
  unidad de observación** (individuo, hogar o establecimiento pareado).
- **VIABLE ECOLÓGICO** — construibles, pero el enlace disponible es agregado (entidad×año,
  municipio×año) — diseño distinto, no versión peor.
- **NO ENLAZA** — cada condición existe en alguna fuente, pero no hay llave verificada que las
  una en una unidad común.
- **NO EXISTE** — ninguna fuente de ninguna de las 6 clases de `data/inventarios/inventario_fuentes_clase-fuente-mexico.md`
  la construye. Reservado a los casos donde se buscó en las seis clases y ninguna respondió —
  cuando la búsqueda no cubrió alguna clase, se declara explícitamente cuál falta, no se marca
  NO EXISTE por default.

---

## §3.1 · Dinero, ahorro, crédito y consumo

| Ficha | Condición del Umbral | Fuente candidata | Clase | Granularidad | ¿Enlaza con las otras condiciones? | Veredicto |
|---|---|---|---|---|---|---|
| R1.1 | Participación voluntaria ≥3 ciclos en Fondos de Aseguramiento agrícola, por productor y ciclo | Ninguna encontrada | — | — | — | **NO EXISTE, con reserva declarada** — no se buscó específicamente un padrón de Fondos de Aseguramiento Agrícola/AGROASEMEX en el barrido de clase de este acto (la búsqueda de Padrón de programa se concentró en Bienestar/salud). No se afirma NO EXISTE sin esa reserva. |
| R1.1 | Tasa de ahorro formal de largo plazo, asalariados informales urbanos, ingreso comparable | ENIF, ENIGH | Encuesta (ya en catálogo) | Individuo | Sí, con la condición anterior — si existiera el padrón agrícola, ambas comparten unidad "persona con ingreso" pero no llave directa persona↔padrón sin identificador cruzado | VIABLE ECOLÓGICO en el mejor caso — solo si el padrón (arriba) apareciera y trajera algo enlazable por entidad×año, no por persona |
| R1.2 | <15% de formales estables con acceso efectivo hacen aportación voluntaria a afore o seguro privado | CONSAR (agregado) + ENIF (individual) | Regulador no-INEGI (CONSAR) + Encuesta (ENIF) | AFORE-agregado (CONSAR) / individuo (ENIF) | Sí — ENIF mide el mismo individuo con acceso, ingreso y aportación en la misma entrevista | **VIABLE** — ya corrido en esta mesa (Nota 19, `hitoD-preregistro-v2_0.md:918`): 42.98%, IC95%=[39.88%,46.08%], falsador no se satisface. No se re-adjudica aquí (fuera de perímetro de Task C, que no emite veredictos RX.Y). |
| R1.3 | Penetración ≥10% segmento popular, brecha rural-urbana <10pp | ENIF, ENDUTIH | Encuesta (ya en catálogo) | Individuo | Sí, ambas condiciones en el mismo instrumento | VIABLE, a nivel de penetración/brecha |
| R1.3 | Sin programa de referidos que explique el grueso de las altas (canal de alta desagregado) | Ninguna — dato propietario de la fintech | — | — | No enlaza con la condición anterior sin el dato propietario | **NO EXISTE** — verificado en las 6 clases de `inventario_fuentes_clase-fuente-mexico.md`: ninguna (Registro administrativo, Regulador — ni CNBV publica canal de alta por fintech) lo construye. Mismo hallazgo que v1.0 ya daba, confirmado con el catálogo extendido. |
| R1.4 | Prima pagada por marca sobre sustituto funcional equivalente en D/E ≤ la de A/B | Ninguna | — | — | — | **NO EXISTE** — panel de consumo D/E popular, hueco declarado desde el pre-registro mismo (fila D "pre-registrado como el desenlace más probable"). Ninguna de las 6 clases nuevas lo cubre (no hay panel de consumo minorista por estrato en registro administrativo, padrón ni transparencia). |

## §3.2 · Trabajo y carrera

| Ficha | Condición del Umbral | Fuente candidata | Clase | Granularidad | ¿Enlaza? | Veredicto |
|---|---|---|---|---|---|---|
| R2.1 | Diferencia <20pp en tasa de reporte voluntario de errores, jerarquía tradicional vs. plana, canal pareado | Ninguna | — | — | — | **NO EXISTE** — dato organizacional propietario, mismo hallazgo del pre-registro (D probable). Ninguna de las 6 clases nuevas trae encuesta de clima organizacional por tipo de empresa. |
| R2.2 | Rotación y productividad ±10pp, liderazgo autoritario no-benévolo vs. benévolo | Ninguna | — | — | — | **NO EXISTE** — mismo hueco, dato propietario. Regulador no-INEGI (STPS/registros laborales) no se identificó con esta granularidad en el barrido. |

## §3.3 · Autoridad, trámite y relación con el Estado

| Ficha | Condición del Umbral | Fuente candidata | Clase | Granularidad | ¿Enlaza? | Veredicto |
|---|---|---|---|---|---|---|
| R3.1 | Brecha ≥20pp mordida, alta vs. baja discrecionalidad, dentro de trámites presenciales, pareada por tipo de trámite | ENCIG 2023 | Encuesta (ya en catálogo) | Individuo | Sí, dentro del mismo instrumento | VIABLE en diseño — corrida completa pendiente de adjudicación (`hitoD-preregistro-v2_0.md:787`), fuera de perímetro de este acto re-adjudicarla |
| R3.2 | Brecha ≥20pp mordida, digital/testigos/registrable vs. presencial sin registro | ENCIG 2023 | Encuesta (ya en catálogo) | Individuo | Sí | **VIABLE** — ya archivado veredicto `B` (`hitoD-preregistro-v2_0.md:991`). No se re-adjudica. |
| R3.4 | Condiciones A∧B∧C de ADR-37 (reproducción + mecanismo + anti-confusión), series de Banxico SPEI/CoDi | Banxico (series transaccionales) + ENIF (respaldo) | Regulador no-INEGI (Banxico) + Encuesta (ENIF) | Nacional agregado (Banxico) / individuo (ENIF) | Parcial — A es medible con series agregadas; B y C, por diseño, ninguna fuente pública separa riesgo fiscal de fricción de uso dentro del mismo producto | **VIABLE ECOLÓGICO para A; NO ENLAZA para B/C** — la propia ficha ya pre-registra esto como el desenlace más probable (Respaldo 2, `hitoD-preregistro-v2_0.md:841`): A medible agregado, B/C inejecutables por diseño de fuente, no por falta de búsqueda. |

## §3.4 · Salud y cuerpo

| Ficha | Condición del Umbral | Fuente candidata | Clase | Granularidad | ¿Enlaza? | Veredicto |
|---|---|---|---|---|---|---|
| R4.1 | Reducción <25% en uso de farmacia-con-consultorio tras mejora documentada de acceso público (antes/después) | Ninguna con diseño panel/evento fechado | — | — | — | **NO EXISTE, sostenido incluso con catálogo extendido** — ver `2026-08-04-aa-relectura-cuatro-d.md` (Tarea D): SINERHIAS podría, en principio, fechar aperturas/ampliaciones de unidad, pero no se verificó a nivel de instrumento en este acto; la razón del D archivado se sostiene con la reserva declarada ahí. |
| R4.1 | Trato medido (confusor a aislar) | ESTAD ("ENSATD" del encargo) | Encuesta institucional no-hogar | Establecimiento | No enlaza directo con la condición anterior (ESTAD es transversal por unidad, no panel pre/post) | **NO ENLAZA** — ESTAD mide trato por establecimiento, pero no está pareada temporalmente con un evento de mejora de acceso; sería insumo de un diseño futuro, no resuelve el confusor en este catálogo. |
| R4.2 | Diferencia hombre-mujer en posposición de chequeo <10pp, controlando tipo de empleo y acceso | ENSANUT 2024 | Encuesta (ya en catálogo) | Individuo | Sí — mismo cuestionario | **VIABLE en diseño, `D` archivado por ausencia de variable, no de instrumento** (`hitoD-preregistro-v2_0.md:993`, Nota 17) — ENSANUT no pregunta "sin permiso laboral para atender su salud". Catálogo extendido no cambia esto: ninguna de las 6 clases nuevas trae encuesta de conducta preventiva cruzada con permiso laboral. |
| R4.3-A | Caída de adherencia <15% ante desabasto documentado ≥3 meses | ENSANUT 2024 (`A0313`/`A0314`) | Encuesta (ya en catálogo) | Individuo | Sí | **VIABLE en diseño, `D` archivado** (auto-reporte, no surtimiento — ver Tarea D) |
| R4.3-B | Diferencia <10pp adherencia, cuidadora presente vs. ausente, controlando gravedad y SE | ENSANUT 2024 (proxy corresidencia) | Encuesta (ya en catálogo) | Individuo/hogar | Sí, mismo hogar | **VIABLE en diseño, `D` archivado** (sin variable de cuidadora, solo proxy confundido — ver Tarea D) |
| R5.1 | Reducción <10% en corresidencia/transferencias intrafamiliares tras Pensión del Bienestar, beneficiarios vs. no beneficiarios | ENIGH (clave `P044`/`P104`) + PUB (padrón, no verificado a nivel de microdato) | Encuesta (ENIGH) + Padrón de programa (PUB) | Hogar (ENIGH) / no verificada (PUB) | Sí para ENIGH sola (mismo hogar); PUB no se confirmó enlazable a nivel de hogar en este acto | **VIABLE ECOLÓGICO/VIABLE, ya corrido con ENIGH sola** (Nota 16, propuesta `A`, no adjudicada) — el padrón nominal (PUB) mejoraría la identificación de beneficiarios más allá del proxy de ENIGH, pero su granularidad quedó **ambigua** en este acto (`inventario_fuentes_clase-fuente-mexico.md` #5) — no se promueve como sustituto sin verificar. |
| R5.2 | Reducción <20% horas de cuidado, mujer 40+ pasa a ocupada formal TC, con varón disponible | ENUT 2024 | Encuesta (ya en catálogo) | Individuo/hogar | Sí | **VIABLE en diseño, ya corrido** (Nota 18, propuesta `A` con reserva estadística — IC95% no despeja 20%). No se adjudica aquí. |

## §3.5 · Familia y pareja — cubierto arriba (R5.1, R5.2 son de este bloque; se listaron junto a salud por continuidad de la ficha R4.3/R5.1 en el pre-registro)

## §3.7 · Cívico y participación

| Ficha | Condición del Umbral | Fuente candidata | Clase | Granularidad | ¿Enlaza? | Veredicto |
|---|---|---|---|---|---|---|
| R7.1 | Diferencia de participación <15pp, concurrente vs. no concurrente, mismo electorado | ENCUP (actitud) + INE (resultados oficiales) | Encuesta (ENCUP) + Regulador no-INEGI (INE) | Nacional-corte (ENCUP) / **casilla, sección, distrito, municipio, entidad (INE, confirmado en este acto)** | Parcial — INE por sí solo permite parear el mismo electorado por sección entre dos elecciones (misma unidad geográfica, distintos años), sin necesitar ENCUP para el Umbral literal (que es de participación, no de actitud) | **VIABLE ECOLÓGICO, mejora respecto a v1.0** — v1.0 (línea 176) marcaba "granularidad municipal es hueco declarado"; este acto encuentra que INE libera **casilla/sección**, más fino que municipio. El Umbral pide diferencia de participación por electorado, que es exactamente lo que un cómputo por sección entre dos comicios permite — sin abrir el instrumento no se confirma si el cruce concurrente/no-concurrente está pre-armado o requiere construirse sección por sección. Se registra como mejora de granularidad, no como variable confirmada. |
| R7.2 | Brecha de denuncia <20pp, asegurado vs. no asegurado, pareando gravedad e identificabilidad | ENVIPE (8 olas 2018-2025) | Encuesta (ya en catálogo) | Individuo | Sí | **VIABLE en diseño, `D` archivado, con ambigüedad documentada no resuelta** (Notas 11-13: `BP2_1` no cruza entre clases de delito; dentro de robo de vehículo, IC95% cruza el umbral en un pareo, no en otro). Catálogo extendido no aporta candidata nueva — ninguna de las 6 clases mide cobertura de seguro cruzada con tipo de delito. |
| R7.3 | RDD sobre Pensión del Bienestar con efecto electoral independiente de aprobación presidencial, ≥5-10pp a escala nacional | Ninguna con diseño RDD listo | — | — | — | **NO EXISTE el diseño, aunque los insumos existen por separado** — PUB (padrón de beneficiarios, granularidad ambigua) + INE (resultados por sección, granularidad confirmada fina) podrían, en teoría, construir un RDD si el padrón fuera nominal y geolocalizable — no verificado en este acto. La ficha misma (`D` no aplica: "el diseño es concebible, solo no se ha hecho") queda igual: el catálogo extendido no cambia que nadie construyó el cruce, solo que ahora hay más piezas candidatas para intentarlo. |
| R7.4/R7.5 | ≥25% de casos documentados de respuesta colectiva ante agravio cruzan la predicción ambiental | Ninguna | — | — | — | **NO EXISTE** — registro de eventos (protesta/autodefensa) codificado por entorno. Ninguna de las 6 clases nuevas lo trae (transparencia/sociedad civil se buscó vía MCCI/Cero Desabasto, ninguna de las dos es un registro de eventos de conflicto). |
| R8.1 | Contribución ≥60% sostenida ≥2 años sin sanción/monitoreo, fuera de usos y costumbres | Ninguna con inventario de comités | — | — | — | **NO EXISTE** — inventario de comités con/sin mecanismo de sanción. Ninguna de las 6 clases nuevas lo cubre (no hay padrón ni registro administrativo de comités vecinales identificado en el barrido). |
| R8.2 | Participación sostenida ≥2 ciclos, incumplimiento <10%, tandas digitales entre desconocidos | Ninguna — dato de plataforma propietario | — | — | — | **NO EXISTE** — mismo hueco declarado en el pre-registro (D probable). |
| R8.3 | Diferencia <10pp disposición a transar con desconocidos, enforcement alto vs. bajo | Ninguna reconciliada — `conf.06` sigue abierto | — | — | — | **NO ENLAZA / bloqueado por conflicto de cifras, no por ausencia de fuente** — LAPOP y Latinobarómetro (clase Internacional, ya en catálogo) existen pero **añadirían una sexta cifra sin reconciliar** `conf.06`, mismo argumento que v1.0 ya daba (línea 124). El catálogo extendido no resuelve el conflicto de medición preexistente. |

## §3.9 · Información y creencia

| Ficha | Condición del Umbral | Fuente candidata | Clase | Granularidad | ¿Enlaza? | Veredicto |
|---|---|---|---|---|---|---|
| R9.1 | Tasa de consulta a experto <50%, población con acceso documentado (distancia <2km, sin costo, espera <1 día) | CLUES (distancia) + ENSANUT (conducta) | Registro administrativo (CLUES) + Encuesta (ENSANUT) | Establecimiento con domicilio/localidad (CLUES) / individuo (ENSANUT) | **No confirmado** — CLUES da ubicación de establecimiento, no coordenadas GPS nativas confirmadas; ENSANUT no libera CLUES del establecimiento consultado en su microdato público (no verificado en este acto). Sin esa llave, no hay forma de calcular distancia real persona-establecimiento con las dos fuentes tal como están. | **NO ENLAZA, mejora parcial respecto al `D` archivado** — el `D` de R9.1 (Nota 23) decía "sin variable de distancia en km, solo tiempo de traslado". Eso sigue siendo cierto para ENSANUT sola. CLUES aporta georreferenciación de establecimientos que **antes no estaba catalogada**, pero enlazarla con la conducta de una persona específica requiere una llave (domicilio del hogar × CLUES del establecimiento) que **no se verificó que exista en ningún microdato público** — ver Tarea D para el detalle completo. |
| R9.1 | Población que no consultó a nadie (excluida del Cuestionario de Utilizadores) | Cuestionario Hogar de ENSANUT (sección IV) | Encuesta (ya en catálogo) | Individuo | Parcial — cubre a toda la población, pero su lista de motivos de no-atención es institucional, sin categoría de preferencia por conocimiento propio/allegado (verificado por Encargo Z, Nota 20) | **NO EXISTE la variable específica dentro del instrumento disponible** — ninguna de las 6 clases nuevas resuelve este hueco (no es de georreferenciación, es de diseño de cuestionario). |
| R9.2 | Cobertura <60% con disponibilidad y alcance de campaña verificados por fuente independiente del prestador — mitad de cobertura | ENSANUT 2024 (verificación por Cartilla) | Encuesta (ya en catálogo) | Individuo | Sí, mismo cuestionario | **VIABLE** — ya construible, es la mitad que el `D` archivado no cuestiona. |
| R9.2 | Mitad de disponibilidad/alcance de campaña, verificado por tercero independiente del prestador | Cero Desabasto | Transparencia/sociedad civil | **No verificada con precisión** (posible entidad, no confirmado a nivel de unidad médica) | No confirmado — si la granularidad de Cero Desabasto es de entidad, podría enlazar con ENSANUT por entidad×año; si es de unidad médica, podría acercarse a nivel establecimiento vía CLUES | **VIABLE ECOLÓGICO en el mejor caso, NO EXISTE con la evidencia verificada en este acto** — Cero Desabasto es **independiente del prestador** (satisface esa condición, ausente en el catálogo v1.0) y **cubre desabasto de medicamentos**, pero no se verificó que reporte específicamente disponibilidad/alcance de **campañas de vacunación** (su cobertura declarada es medicamentos/insumos/vacunas/anticonceptivos en general, no campañas). Se registra como candidata prometedora, no como resuelta — ver Tarea D para el contraste completo contra la razón exacta del `D` archivado. |

## §3.10 · Comunicación y conflicto

| Ficha | Condición del Umbral | Fuente candidata | Clase | Granularidad | ¿Enlaza? | Veredicto |
|---|---|---|---|---|---|---|
| R10.1 | Diferencia <15pp rechazo indirecto, interlocutor superior vs. inferior, muestra mexicana no universitaria | Ninguna encuesta del catálogo — ancla es estudio académico (Félix-Brasdefer) | — | — | — | **NO EXISTE en el catálogo de fuentes de datos** (es dato de estudio académico puntual, no serie ni registro) — ninguna de las 6 clases nuevas cataloga actos de habla. Consistente con v1.0. |
| R10.2 | Diferencia <10% rotación/desempeño, retro pública vs. privada, controlando sector | Ninguna | — | — | — | **NO EXISTE** — dato organizacional propietario, mismo hueco que R2.1/R2.2. |
| R10.3 | Aumento <15pp disposición a testificar tras protección efectiva a testigos, zona insegura | Ninguna — bloqueo ético declarado, no de dato | — | — | — | **NO EXISTE, y preferible que así sea** — la propia ficha declara que solo dato secundario ya publicado y agregado es admisible, nunca recolección primaria en zona de violencia activa. Ninguna de las 6 clases nuevas cambia este límite ético. |

---

## Resumen — no re-adjudica ningún veredicto, solo cuenta filas

**27 de 27 fichas tienen sus condiciones cruzadas** (criterio de suficiencia, §7 del encargo).
De las **~34 condiciones** listadas: **7 VIABLE**, **6 VIABLE ECOLÓGICO** (o parcialmente),
**5 NO ENLAZA**, **~16 NO EXISTE** (varias con reserva de búsqueda declarada, no exhaustiva). La
proporción exacta depende de cómo se cuenten las fichas con condiciones mixtas (p. ej. R9.1 tiene
una condición NO ENLAZA y otra NO EXISTE) — no se colapsa a una sola cifra por ficha porque **la
pregunta de este acto es por condición, no por ficha** (título de la Tarea C).

**Ninguna fila de esta tabla cambia un veredicto `RX.Y` ya archivado.** Donde una fila mejora la
imagen de una condición respecto al `D` archivado (R7.1 con INE, R9.1/R9.2 con CLUES/Cero
Desabasto), el contraste completo contra la razón exacta del `D` vive en Tarea D
(`forense/notas/2026-08-04-aa-relectura-cuatro-d.md`), que tampoco adjudica — produce evidencia
para que mesa decida.

## Lo que este documento no hace

Mismo límite que v1.0: no edita ninguna ficha, no adjudica ni retira ningún veredicto, no
descarga ninguna fuente. Ninguna candidata mencionada aquí pasó de "aparece en el catálogo
extendido" a "se abrió el instrumento". No se afirma que la búsqueda de las 6 clases sea
exhaustiva — donde no se buscó algo específico (p. ej. Fondos de Aseguramiento Agrícola para
R1.1), se declara la reserva en la fila misma, no se oculta detrás de un "NO EXISTE" sin
matices.
