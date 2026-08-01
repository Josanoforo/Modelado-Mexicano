<!-- PROCEDENCIA — leer antes que el cuerpo.

Este archivo responde a un ENCARGO recibido de chat (tipo (3) en su origen:
el encargo mismo, con su vocabulario — "M2/M3", "P2", "PERSISTE", "la mesa",
"ADR-51" — no proviene de ningún archivo de este repo; se buscó "PERSISTE",
"ADR-51" y "\bP2\b" en todo `canon/` y `forense/` y no hay coincidencias.
Se trata como instrucción de encargo, no como hecho ya sentado, y este
documento declara en cada sección qué se derivó de archivo (tipo (1)) y qué
se toma tal cual del encargo sin verificación posible en este repo.

Sesión: sesión dedicada, rama `sesion/familismo-deferencia-reactivo`, base
`origin/main` = `ba44c25`. Régimen declarado por el encargo: **Fase A —
diccionarios, catálogos, cuestionarios; ningún microdato.** Por ADR-46, esta
sesión abre diccionarios y cuestionarios a propósito (es su objeto), y por
tanto queda **inhabilitada para pre-registrar** contra cualquier fuente cuyo
diccionario o cuestionario leyó abajo — ENUT, ENCUCI, ENCIG.

**Este documento no rige.** No sella ADR-51 — no existe ADR-51 en
`canon/gobernanza-v1_15.md` (el más reciente registrado ahí y en el log de
`git` es ADR-50, "motor ABM ajuste"). La sección 4 (enmienda) es una
**propuesta sin sello**, misma disciplina que `forense/hitoE-campana-medicion-v2_0.md`:
"no rige sin ADR". La mesa decide si se sella.
-->

# ENCARGO · C — ¿Existe reactivo para `familismo_obligacion` y/o `deferencia`?

## 0 · Veredictos (arriba, por instrucción del encargo)

| Parámetro | Candidata | Veredicto candidata | Veredicto global del parámetro |
|---|---|---|---|
| **`familismo_obligacion`** | **ENUT** (2019, 2024 — en disco) | **PROXY CON SUPUESTO DECLARADO** — persona, carga de cuidado, series `6.11`/`6.11a` | **PROXY CON SUPUESTO DECLARADO.** El parámetro pasa de "sin reactivo" a "medible, pendiente de medición". El hueco es de **cobertura** (fuentes ya inventariadas, no bajadas), no un límite permanente |
| | ENDIREH (inventario, no en disco) | NO DETERMINABLE — descriptor no disponible en disco | |
| | ENASIC (inventario, no en disco) | NO DETERMINABLE — descriptor no disponible en disco | |
| | ENBIARE (inventario, no en disco) | NO DETERMINABLE — descriptor no disponible en disco | |
| | ENASEM (inventario, no en disco) | NO DETERMINABLE — descriptor no disponible en disco | |
| **`deferencia`** | ENCUCI (2020 — en disco, FD completo leído) | **SIN REACTIVO** — el único ítem adyacente (`AP5_11`) mide legitimidad de la ley, no deferencia jerárquica | **NO DETERMINABLE — no colapsable a límite permanente.** 2 candidatas en disco dan SIN REACTIVO; las 4 candidatas temáticamente más fuertes (LAPOP, WVS, Latinobarómetro, ENCUP) **no están en disco** y no se pudieron inspeccionar |
| | ENCIG (en disco, estructura de BD completa leída) | SIN REACTIVO — la única mención de jefe/subordinado es una batería de frecuencia de corrupción, no de deferencia | |
| | LAPOP / AmericasBarometer (inventario, no en disco) | NO DETERMINABLE — descriptor no disponible en disco | |
| | World Values Survey (inventario, no en disco) | NO DETERMINABLE — descriptor no disponible en disco | |
| | Latinobarómetro (inventario, no en disco) | NO DETERMINABLE — descriptor no disponible en disco | |
| | ENCUP (inventario, no en disco; portal INEGI con JS, intento de descarga directa no resuelto en esta sesión) | NO DETERMINABLE — descriptor no disponible en disco | |

**La distinción que el encargo pide no colapsar, aplicada:** para `familismo_obligacion` el veredicto es un **hallazgo de cobertura que sí se resolvió** — hay reactivo, en una fuente ya en disco. Para `deferencia`, el veredicto **no llega a "sin reactivo en el dato público mexicano"** (límite permanente) porque el corpus completo no se agotó: 4 de las 6 candidatas derivadas del inventario nunca se abrieron. Declarar aquí "deferencia no tiene reactivo" sería exactamente el colapso que el encargo prohíbe. Lo único que se sostiene con lo que hay en disco es que **las dos candidatas inspeccionables no lo tienen**.

---

## 1 · Procedencia y punto de partida

Candidatas derivadas de tres inventarios de `data/inventarios/` — no asumidos por nombre, localizados en el repo:

- `inventario_fuentes_uso_del_tiempo_cuidados_hogar_mexico.md`
- `inventario_fuentes_capital_social_mexico.md`
- `inventario_fuentes_cultura_valores_opinion_mexico.md`

y contra `data/catalogo-fuentes-v1_0.md` (119 fuentes) para confirmar qué candidatas ya están en `mm-corpus/raw/` (el directorio de descargas de esta línea de sesiones) antes de abrir nada.

Trabajo previo ya existente y verificado antes de empezar (no se repitió): `forense/hitoE-campana-medicion-v2_0.md` §11 (adenda 31/jul/2026) ya cruzó `deferencia` y `familismo_obligacion` contra las 119 fuentes **al nivel de alcance temático declarado** (sin abrir cuestionario, por firewall ADR-46 de esa sesión). Resultado de esa sesión: `deferencia` SIN CANDIDATA en los diez inventarios; `familismo_obligacion` con candidatas (`ENASEM`, `ENDIREH`, `ENASIC`, `ENBIARE`) pero "ninguna es la escala de familismo — son proxies conductuales de cuidado/obligación". Esta sesión **no repite ese cruce**: lo hereda, y añade exactamente lo que esa sesión tenía prohibido hacer — abrir el diccionario/cuestionario — para las candidatas que sí están en disco, y deriva un candidato nuevo (ENUT) que esa adenda no había propuesto para `familismo_obligacion` con este código específico.

---

## 2 · `familismo_obligacion`

### 2.1 Candidatas (derivadas del inventario de uso del tiempo/cuidados, ítems 4, 6, 9, 10, 17)

| # | Candidata | ¿En disco? | Acción esta sesión |
|---|---|---|---|
| 1 | **ENUT** | Sí — `enut2019_fd.xlsx`, `enut2019_diccionario_variables.html`, `enut2024_fd.xlsx`, `enut2024_diccionario_variables.html`, más 2002/2009/2014 | Diccionario leído completo (reactivo por reactivo, vía `sharedStrings.xml` del `.xlsx`) |
| 2 | ENDIREH | No | Sin acción — NO DETERMINABLE |
| 3 | ENASIC | No | Sin acción — NO DETERMINABLE |
| 4 | ENBIARE | No | Sin acción — NO DETERMINABLE |
| 5 | ENASEM | No | Sin acción — NO DETERMINABLE |

### 2.2 Descriptor — ENUT

El contraste que pide el encargo es "apoyo vs. obligación intra-hogar, vía estructural: un reactivo de carga/deber de cuidado a nivel PERSONA, no de transferencias a nivel hogar". `familismo_apoyo` ya está asignado en `procedencia.yaml` con justificación "trabajo no remunerado al hogar" (`hitoE §11`, cola priorizada, fila `ENUT`). Esa asignación es un agregado amplio de trabajo doméstico. Lo que esta sesión encontró es una franja **más específica y no usada previamente**: la Sección VI del cuestionario ENUT, preguntas `6.11`–`6.11a` (2019 y 2024; numeración estable entre ediciones), capta **por persona informante**, para cada integrante del hogar que necesitó cuidados por discapacidad o enfermedad crónica/temporal:

- si el informante realizó cada una de 11 tareas de cuidado (dar de comer, bañar/vestir, cargar/acostar, dar medicamentos, llevar a citas médicas, ayudar en tareas escolares, "estar al pendiente", etc.) — variables `P6_11_01`…`P6_11_11` (2019), mismo patrón en 2024
- **cuánto tiempo le dedicó**, en horas y minutos, desglosado lunes-a-viernes vs. sábado-y-domingo — variables `P6_11A_XX_1`…`P6_11A_XX_4`

Es decir: no es una pregunta de actitud ("¿cree que debe cuidar a su familia?") sino una **medición de carga real, a nivel persona, con tiempo declarado** — exactamente la "vía estructural" que el encargo pide distinguir de una escala de creencia. Existe un contraste paralelo dentro de la misma fuente que refuerza por qué esta franja es la candidata correcta y no la ya asignada: la pregunta `6.16` ("¿usted ayudó de manera gratuita a **otro hogar**...?") capta ayuda **inter-hogar** — la dimensión de red/reciprocidad más cercana a `familismo_apoyo` — mientras que `6.11`/`6.12`/`6.13`/`6.14`/`6.15` captan cuidado **intra-hogar**, a los propios dependientes — la dimensión de carga/obligación que el encargo busca. Esta distinción (intra vs. inter-hogar) no estaba explícita en la justificación previa de `familismo_apoyo`, y es la misma distinción que el glosario ya advierte no colapsar (`canon/modelo-decision-v3_4.md:525`: "el riesgo mayor entra por `familismo_obligacion`... si el parámetro se lee como 'estas familias son más familieras', el modelo reproduce el esencialismo que combate").

Verificado que el ítem **persiste entre ediciones** (no es un accidente de una sola ola): confirmado en `enut2019_fd.xlsx` (preguntas `6.11`/`6.11a`, filtro `FP6_11`, condicionado a `3.11=1`) y en `enut2024_fd.xlsx` (mismas preguntas `6.11`/`6.11a`, filtro condicionado a `3.7=1` o `3.8∈{1,2}` — el filtro cambió de número de pregunta de origen entre ediciones, el contenido y la estructura de la pregunta 6.11 no).

### 2.3 Veredicto — ENUT: PROXY CON SUPUESTO DECLARADO

**Supuesto que no se puede evitar declarar:** el glosario (`canon/glosario-v5_6.md:120`) define `familismo_obligacion` como "creencia **internalizada** de que uno debe sacrificarse por la familia" (base Zeiders 2013, Fuligni 1999, Calzada 2012 — escalas psicométricas de actitud). Las horas de cuidado de ENUT **no miden la creencia**; miden la **conducta de carga resultante**, que puede coexistir con la creencia, sustituirla (carga impuesta por ausencia de alternativas, no por convicción) o mezclarse con `familismo_apoyo` en el mismo dato. El supuesto que convierte esto en proxy válido para la vía estructural: **una carga de cuidado intra-hogar alta y asimétrica, no explicada por ingreso o composición del hogar, es conducta consistente con obligación internalizada** — no la prueba, pero tampoco es una transferencia monetaria a nivel hogar (lo que el encargo pide excluir explícitamente). No resuelve la ambigüedad que `hitoE §11.3` ya señaló para ENDIREH/ENASIC/ENBIARE/ENASEM ("proxies conductuales, no la escala de familismo, y las dos marcas (b) de contexto migratorio siguen sin resolverse") — **la comparte**: es un proxy conductual más, con la ventaja operativa de estar ya en disco y de reportar tiempo (no solo sí/no), y la desventaja de no distinguir motivo (obligación vs. cariño vs. falta de alternativa).

### 2.4 Las cuatro candidatas sin disco

ENDIREH, ENASIC, ENBIARE y ENASEM son las candidatas que `hitoE §11.3` ya identificó por alcance temático declarado, y ninguna de las cuatro está en `mm-corpus/raw/`. Por la regla del encargo, esto **no es "sin reactivo"**: es hallazgo de cola de descarga. Las cuatro son de acceso directo en el portal del INEGI salvo ENASEM, que tiene una segunda vía (`mhasweb.org`) con registro previo — la vía INEGI no lo requiere. Ninguna se bajó en esta sesión (Fase A no autoriza microdato ni implica autorización de descarga nueva; el mecanismo de descarga masiva del portal INEGI, documentado en `forense/notas/2026-07-31-enut-descarga.md`, es transferible a estas cuatro fuentes por una sesión dedicada a descarga).

---

## 3 · `deferencia`

### 3.1 Candidatas (derivadas de los inventarios de cultura/valores y capital social)

| # | Candidata | Dominio(s) donde aparece | ¿En disco? | Acción esta sesión |
|---|---|---|---|---|
| 1 | **ENCUCI 2020** | cultura/valores (#3), capital social (#3) | Sí — `FD_ENCUCI2020.pdf` (552 variables) | Leído completo, buscado por `autoridad`, `jerarqu`, `obedien`, `superior`, `jefe`, `iniciativa`, `mandan`, `orden(a/es)`, `sumis`, `acatar`, `cuestionar`, `desafi` |
| 2 | **ENCIG** | cultura/valores (#5), capital social (#8) | Sí — `encig23_estructura_base_datos.pdf` (y ediciones 2015-2023) | Leído (edición 2023), mismo barrido de términos |
| 3 | LAPOP / AmericasBarometer | cultura/valores (#12), capital social (#9) | No | Sin acción — NO DETERMINABLE |
| 4 | World Values Survey | cultura/valores (#14), capital social (#11) | No | Sin acción — NO DETERMINABLE |
| 5 | Latinobarómetro | cultura/valores (#13), capital social (#10) | No | Sin acción — NO DETERMINABLE |
| 6 | ENCUP | cultura/valores (#4), capital social (#4) | No | Se intentó acceso directo al portal INEGI (`https://www.inegi.org.mx/programas/encup/2012/`); la página es una cáscara renderizada por JS sin enlaces de documento estáticos — no resuelto dentro del alcance de esta sesión. NO DETERMINABLE |

No se persiguió `ENNVIH` (en disco, panel MxFLS) porque no aparece nombrada en ninguno de los tres inventarios que el encargo señala como punto de partida — perseguirla habría sido "abrir por lo que hay en disco", exactamente lo que el encargo pide no hacer ("primero el inventario, no la descarga"). Queda anotado por si una sesión futura decide ampliar el inventario de partida.

### 3.2 Descriptor y veredicto — ENCUCI: SIN REACTIVO

El único ítem que el barrido de términos encontró es `AP5_11` (sección 5, "cultura de la legalidad"):

> *5.11 En su opinión, ¿cuál de las siguientes frases se acerca más a lo que usted piensa? (1) Las personas deben obedecer siempre las leyes aunque sean injustas · (2) Las personas pueden pedir que cambien las leyes si estas no les parecen · (3) Las personas pueden desobedecer la ley si esta es injusta*

**Por qué no califica ni como proxy.** El constructo que el motor necesita (`canon/modelo-decision-v3_4.md:234`, regla `R2.1`) es deferencia **ante jerarquía interpersonal** — tradición organizacional o familiar, con el efecto conductual específico de "iniciativa suprimida" y el "sí que significa probablemente". `AP5_11` mide **legitimidad percibida de la ley como institución abstracta** frente al Estado — un objeto de actitud distinto (autoridad legal-política, no jerarquía personal/laboral/familiar) y sin el componente conductual (no pregunta si el respondiente calla, evita iniciativa o disiente en una relación jerárquica concreta). Tratarlo como proxy sería el mismo colapso que el encargo pide evitar, solo que entre dos objetos de actitud en vez de entre estructura y cultura. El resto de menciones de "autoridad(es)" en `ENCUCI` (32 ocurrencias revisadas) son ítems de participación cívica conductual ("¿se ha reunido con las autoridades?"), integridad electoral ("¿las autoridades electorales son justas?") o identificación del jefe(a) de hogar para el listado de integrantes — ninguno mide deferencia.

### 3.3 Descriptor y veredicto — ENCIG: SIN REACTIVO

La única mención de "Jefes[as] o subordinados[as])" (`P3_3_07`, y su equivalente en otras ediciones) aparece dentro de una batería de **frecuencia percibida de corrupción** ("¿con qué frecuencia diría que actos como el soborno son parte de la cultura de...?"), con "compañeros de trabajo (jefes o subordinados)" como una de varias categorías de actor (junto a policías, hospitales públicos, empresarios, gobernadores). Jefe/subordinado aparece como etiqueta de relación dentro de una pregunta de corrupción, no como objeto de un ítem de deferencia. El resto de las 19 menciones de "autoridades" en las estructuras de base de datos revisadas (2023 y verificación cruzada en años anteriores) son de la misma familia: contacto con autoridad para trámites, denuncia ante autoridad. Nada mide obediencia, supresión de iniciativa o jerarquía interpersonal.

### 3.4 Las cuatro candidatas sin disco

LAPOP, WVS y Latinobarómetro son las tres fuentes con mayor probabilidad *a priori* de contener el reactivo — las tres son baterías de valores/actitudes con módulos históricos de autoritarismo, tolerancia política o valores de crianza (p. ej., WVS incluye en varias olas un ítem de crianza "obediencia" entre las cualidades deseables en un niño, y baterías de valores tipo Schwartz con el componente "conformidad/tradición" en algunas olas — **no verificado aquí**: es conocimiento externo al corpus, no una lectura de diccionario, y por eso no se usa como veredicto, solo como razón para priorizar la descarga). Ninguna de las tres está en `mm-corpus/raw/`, y las tres requieren aceptar una licencia o registro antes de descargar (LAPOP: "click license"; WVS: formulario; Latinobarómetro: acuerdo de usuario) — ninguno es un bloqueo técnico, son fricciones de una sesión de descarga, no de esta. ENCUP es INEGI y de descarga directa en principio, pero el portal usa el mismo componente `descargaMasivaV2` documentado en `forense/notas/2026-07-31-enut-descarga.md` (JS, sin enlaces estáticos) — replicar ese mecanismo para ENCUP es tarea de una sesión de descarga dedicada, no de esta lectura de diccionario.

**Ninguna de las cuatro se marca "sin reactivo".** Se marcan NO DETERMINABLE por regla explícita del encargo: "'No está en disco' jamás se reporta como 'no existe'".

---

## 4 · Propuesta de enmienda a ADR-51 (sin sellar)

> No rige. No hay ADR-51 en `canon/gobernanza-v1_15.md` (el registro más reciente es ADR-50). Esta sección es material para que la mesa decida, exactamente como `forense/hitoE-campana-medicion-v2_0.md` presentó E0–E4 sin sellar nada.

**Aplica solo a `familismo_obligacion`** (`deferencia` no cambia de estado — sigue sin candidata inspeccionada, ver §3).

Cambio propuesto en `milpa/procedencia.yaml` (fila `familismo_obligacion`, hoy `ASIGNADO` y "sin magnitud"): **no tocar el peso asignado** (`G5`, "signo negativo o no monotónico" — misma disciplina que `hitoE §5`, "los pesos siguen ASIGNADO"). Lo que cambia es el estado de operacionalización: de `SIN INSTRUMENTO` (registrado en `hitoE-campana-medicion-v2_0.md:416`) a **`CANDIDATA CON DICCIONARIO VERIFICADO`**, con:

- **Fuente:** ENUT (2019, 2024 — y probablemente 2009/2014, no verificado en esta sesión)
- **Reactivo:** preguntas `6.11`/`6.11a` (2019) y equivalentes 2024 — carga de cuidado intra-hogar por persona informante, en horas/minutos, desglosada entre semana y fin de semana
- **Unidad:** persona (informante de 12 años y más)
- **Operacionalización propuesta:** horas semanales de cuidado a integrantes dependientes del propio hogar, como proxy conductual de `familismo_obligacion` (vía estructural, no de creencia)
- **Supuesto declarado:** carga de cuidado alta y asimétrica ≈ conducta consistente con obligación internalizada; no distingue motivo (obligación / afecto / ausencia de alternativa) — la misma limitación de marca (b) que ya cargan ENDIREH/ENASIC/ENBIARE/ENASEM en `procedencia.yaml:278-280` (nadie ha medido este parámetro en población residente en México con una escala validada; esto tampoco lo es, es proxy conductual)
- **Lo que esto NO decide:** si el proxy conductual sustituye la escala psicométrica que el glosario cita (Zeiders/Fuligni/Calzada), o si haría falta declarar el mecanismo por separado antes de estimar (misma regla que `hitoE §5`: "ninguna entrada de la capa medida se escribe en la casilla de un peso del generador... por separado y en mesa")

Si la mesa sella esto, `familismo_obligacion` pasa de 0 a al menos 1 fuente instrumentable con dato ya en disco — sin esperar la descarga de las otras cuatro candidatas.

---

## 5 · Límite de lectura declarado (ADR-46)

Esta sesión leyó: los tres inventarios de dominio nombrados en §1 completos; `data/catalogo-fuentes-v1_0.md` (confirmación de qué candidatas están en disco, no releído línea por línea — ya lo hizo `hitoE §11`); `forense/hitoE-campana-medicion-v2_0.md` completo; `forense/notas/2026-07-31-enut-descarga.md` completo; `enut2019_fd.xlsx`, `enut2024_fd.xlsx` (diccionarios completos, vía `sharedStrings.xml`), `enut2019_diccionario_variables.html`, `enut2024_diccionario_variables.html` (páginas RNM); `FD_ENCUCI2020.pdf` completo (4005 líneas de texto extraído); `encig23_estructura_base_datos.pdf` completo y verificación cruzada de "jefe/subordinado" contra ediciones 2015/2017/2019/2021 de ENCIG por el mismo patrón de pregunta. Un intento de acceso HTTP a `inegi.org.mx/programas/encup/2012/` (200 OK, cáscara JS sin contenido de documento — no es apertura de cuestionario, es una página vacía). **Cero microdato abierto o extraído** (ningún `.zip`/`.dbf`/`.csv` de base de datos). Por ADR-46, esta sesión queda **inhabilitada para pre-registrar** contra ENUT, ENCUCI o ENCIG.

## 6 · Fuera de perímetro, y por qué no se tocó

No se bajó ninguna fuente nueva. No se modificó `milpa/procedencia.yaml`. No se selló ningún ADR. No se tocó `canon/gobernanza-v1_15.md`. No se registró entrada en `canon/cola.yaml` ni en `forense/hallazgos.md` — el encargo pidió una nota vía PR, no un hallazgo formal; si la mesa quiere una entrada de cola para "ENCUP/ENDIREH/ENASIC/ENBIARE/ENASEM/LAPOP/WVS/Latinobarómetro pendientes de descarga", eso es una decisión posterior a este documento, no de esta sesión.
