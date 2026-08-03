<!-- PROCEDENCIA — leer antes que el cuerpo.

Este archivo responde a un ENCARGO recibido de chat (tipo (3) en su origen).
Se verificó contra archivo lo verificable: "C-bis" SÍ es vocabulario del
repo — `canon/gobernanza-v1_15.md`, ADR-51 §(c) M2/M3, declara literalmente
"el veredicto que registra este ADR es 'indeterminado, con cola de
verificación declarada (C-bis)'" y "No corre C-bis ni agota las 4
candidatas pendientes de `deferencia` — la cola de verificación queda
declarada, no ejecutada." Este documento ES esa cola, ejecutada. El resto
del vocabulario del encargo ("Paso 0", "Al volver", la escala de veredicto)
se toma tal cual, sin verificación posible en este repo más allá de la
escala misma, que sí es de `forense/notas/2026-07-31-encargo-c-familismo-
deferencia-reactivo.md` (Encargo C, precedente directo, mismo autor).

Sesión: sesión dedicada, rama `sesion/cbis-deferencia-externas`, base
`origin/main` = `ad08900` (post-ADR-51, post-renombre `modelo-decision-v3_4`
→ `v4_0`). La rama `sesion/familismo-deferencia-reactivo` de Encargo C ya
se fusionó (PR #42) y no se reutiliza aquí.

**Perímetro de red, ya corrido antes de esta sesión (Paso 0 del encargo,
no se repite):** los cuatro hosts —`vanderbilt.edu`, `worldvaluessurvey.org`,
`latinobarometro.org`, `inegi.org.mx`— responden 200 vía el proxy de egreso
de este entorno. Esta sesión sí verificó, de forma adicional y con
propósito distinto (diagnóstico de UNA URL específica, no todo el
perímetro), que el espejo `fomentocivico.segob.gob.mx` de ENCUP **no**
completa el handshake TLS a través del mismo proxy (`curl -v`: el túnel
CONNECT se establece con HTTP 200, pero el ClientHello TLS nunca recibe
respuesta y expira a los 15s) — ver §4.4.

**Régimen y contaminación (ADR-46).** Esta sesión abrió a propósito:
`forense/notas/2026-07-31-enut-descarga.md` completo (referencia de
mecanismo, no cuestionario), el cuestionario México 2023 de LAPOP/
AmericasBarometer (PDF completo, 77 páginas), el cuestionario regional 2024
de Latinobarómetro (PDF completo) y su ficha técnica 2024 (PDF completo).
Por tanto queda **inhabilitada para pre-registrar contra LAPOP/
AmericasBarometer 2023 y contra Latinobarómetro 2024**. Para **WVS Ola 7**
y **ENCUP**, esta sesión hizo **exploración de estructura** del portal
(páginas de navegación, endpoints AJAX, catálogo RNM) sin llegar a leer el
contenido del instrumento — por la distinción de dos niveles que ADR-46
fija, esto **contamina parcialmente**: la sesión queda inhabilitada para
pre-registrar contra la *estructura de acceso* de WVS Ola 7 y del portal
ENCUP de INEGI, aunque no leyó el cuestionario de ninguna de las dos. Se
declara hasta dónde en §4.2 y §4.4.

**Este documento no rige sobre ADR-51.** No lo reescribe ni lo sella de
nuevo. La §5 (enmienda) es una **propuesta sin sello**, misma disciplina
que Encargo C §4 y que `forense/hitoE-campana-medicion-v2_0.md`: "no rige
sin ADR". La mesa decide si se sella.
-->

# ENCARGO · C-bis — Cuatro candidatas externas de `deferencia`: LAPOP, WVS, Latinobarómetro, ENCUP

## 0 · Veredictos (arriba, por instrucción del encargo)

**Perímetro de red (Paso 0, dado por el encargo, no re-corrido):**

| Candidata | URL sondeada | Código |
|---|---|---|
| LAPOP | `https://www.vanderbilt.edu/lapop/` | 200 |
| World Values Survey | `https://www.worldvaluessurvey.org` | 200 |
| Latinobarómetro | `https://www.latinobarometro.org` | 200 |
| ENCUP | `https://www.inegi.org.mx/programas/encup/2012/` | 200 |

**Veredictos por candidata:**

| Candidata | Instrumento localizado | Veredicto |
|---|---|---|
| **LAPOP / AmericasBarometer** | Cuestionario México 2023 (`ABMex2023-Mexico-Questionnaire-V9.2.3.0-Spa-230511-W.pdf`, 77 pp., leído completo) | **SIN REACTIVO** |
| **World Values Survey (Ola 7)** | `WVS7 Questionnaire Mexico 2018 Spanish.pdf` (identificado con precisión: título exacto, país-año, id de documento) — **no se pudo extraer su contenido** | **NO DETERMINABLE — documento localizado pero ilegible** (dentro del alcance de esta sesión) |
| **Latinobarómetro** | Cuestionario regional 2024 (`latinobarometro-2024-cuestionario-esp.pdf`, aplicado en México, n=1200, leído completo) | **PROXY CON SUPUESTO DECLARADO** — ítem `P4NOIJ`, "Obediencia" entre las cualidades a inculcar en los niños |
| **ENCUP** | Portal INEGI (`inegi.org.mx/programas/encup/2012/`) confirmado como SPA sin tabla de Microdatos/Tabulados y sin instrumento estático localizable; catálogo RNM de INEGI (el mismo mecanismo que sí dio el diccionario de ENUT en Encargo C) **no tiene ninguna entrada para ENCUP** | **NO DETERMINABLE — espejo fuera del sandbox** (ruta de recuperación: `fomentocivico.segob.gob.mx`, fuera de los hosts permitidos de este entorno, o descarga manual del autor) |

**Veredicto global de `deferencia`:** **PROXY CON SUPUESTO DECLARADO (parcial).** La cola C-bis pasa de "6 candidatas, 0 con instrumento leído fuera de disco" a: 2 candidatas cerradas (ENCUCI, ENCIG de Encargo C: SIN REACTIVO; LAPOP de esta sesión: SIN REACTIVO — **3 en total, SIN REACTIVO**), 1 candidata con **hallazgo positivo** (Latinobarómetro: PROXY), 2 candidatas que **siguen sin agotarse** por razones distintas y declaradas (WVS: documento identificado pero no legible con las herramientas de esta sesión; ENCUP: portal confirmado sin instrumento estático, ruta de recuperación fuera del sandbox). **No se colapsa a "sin reactivo en el corpus alcanzable"**: hay un reactivo, con supuesto declarado, en una fuente ya leída completa. Tampoco se colapsa a "límite permanente": WVS es la candidata que la literatura señala como más probable de tener el reactivo mejor formulado (histórico ítem de obediencia en la misma batería de cualidades para niños que aquí sí dio positivo en Latinobarómetro) y queda sin cerrar, no descartada.

---

## 1 · Procedencia y punto de partida

Esta sesión no repite el cruce de candidatas: lo hereda de Encargo C (`forense/notas/2026-07-31-encargo-c-familismo-deferencia-reactivo.md` §3.1, PR #42 fusionado), que ya derivó las 6 candidatas de `deferencia` de los inventarios de dominio y dejó 4 sin inspeccionar por no estar en `mm-corpus/raw/`. Esta sesión ejecuta exactamente esa cola declarada en ADR-51 §(c) como "C-bis": las 4 candidatas sin disco — LAPOP, WVS, Latinobarómetro, ENCUP —, ahora que el Paso 0 (perímetro de red) confirmó que los cuatro hosts son alcanzables desde este entorno.

**El constructo que se busca, sin relajar el criterio** (`canon/modelo-decision-v4_0.md` §3.2, regla `R2.1`, `id: trabajo.jerarquia.deferencia_iniciativa_suprimida`): *"SI hay jerarquía tradicional/empresa familiar (`segsoc`=2 ∧ `tam_loc` ∈ {3,4}) ENTONCES deferencia hacia arriba, iniciativa suprimida, el 'sí' que significa 'probablemente' — PORQUE G6 + G1."* Es deferencia ante **jerarquía interpersonal, laboral o familiar concreta**, con un efecto conductual específico (iniciativa suprimida). Encargo C ya estableció, contra ENCUCI `AP5_11`, que un ítem sobre legitimidad de la ley como institución abstracta **no** califica ni como proxy porque el objeto de actitud es distinto (autoridad legal-política, no jerarquía personal). Ese mismo criterio se aplica aquí sin relajarlo: un ítem que mencione "autoridad" o "obediencia" en un objeto distinto (régimen político, ley, elección de autoridades) no es deferencia jerárquica interpersonal, aunque use vocabulario parecido.

---

## 2 · LAPOP / AmericasBarometer

### 2.1 Localización

`https://www.vanderbilt.edu/lapop/mexico.php` enlaza el cuestionario específico de México de la ronda más reciente (2023): `https://www.vanderbilt.edu/lapop/mexico/ABMex2023-Mexico-Questionnaire-V9.2.3.0-Spa-230511-W.pdf`. No es el "Core Questionnaire" genérico (que también existe, regional): es la versión con numeración y adaptaciones de México, la relevante por la advertencia de Bloque A del encargo (muestra = población en México, clase (a); marco del instrumento sigue siendo regional/importado, se declara). Descargado y leído completo vía `pdftotext -layout` (77 páginas, 3543 líneas de texto). No se registró en manifiesto como archivo permanente del corpus — **corrección: sí se registró**, ver §6 (se leyó completo como payload y se guardó en `data/raw/`, por la regla del encargo "si se descarga para leerse, se registra").

### 2.2 Barrido de términos y veredicto: SIN REACTIVO

Barrido por `autoridad`, `obedien`, `jerarqu`, `superior`, `jefe`, `patrón`, `empleador`, `iniciativa`, `mand(a/ar/ó)`, `orden(a/es)`, `sumis`, `acatar`, `cuestionar`, `desafi`, `crianza`, `hijos`, `golpe de estado`, `mano dura`. Resultado:

- **`CHM1BN`/`CHM2BN`** (split-sample): elegir entre un sistema que garantice ingreso básico sin voto vs. votar sin garantía de ingreso — mide **preferencia de régimen político** (legitimidad de un tipo de sistema), no jerarquía interpersonal.
- **Apoyo a golpe de Estado militar** (línea 332 y siguientes): mide **tolerancia al autoritarismo de régimen** — el mismo tipo de objeto distinto que ya excluyó `AP5_11` en Encargo C (autoridad político-legal abstracta, no jerarquía laboral/familiar concreta con efecto de iniciativa suprimida).
- **`FORMAL`** ("¿usted o su empleador hacen aportaciones a su AFORE?"): pregunta de **formalidad laboral/previsión social**, "empleador" es solo la etiqueta de quién aporta, no hay pregunta de conducta ante jerarquía.
- **Cero coincidencias** para `jefe`, `patrón`, `jerarqu`, `sumis`, `acatar`, `obedien` (ninguna), `crianza`/`hijos` (ninguna batería de cualidades a inculcar en los niños en este instrumento).

No hay ningún ítem, ni siquiera candidato a falso positivo, sobre deferencia ante un jefe, patrón o cabeza de familia. **SIN REACTIVO**, con lectura completa del instrumento — mismo tratamiento que ENCUCI/ENCIG en Encargo C.

---

## 3 · World Values Survey (Ola 7)

### 3.1 Localización — reconstruida sin ejecutar JS

`https://www.worldvaluessurvey.org` es una SPA basada en `javaScript:SetContent(...)`, pero varias páginas internas responden como JSP reales fuera de esa SPA. Cadena reconstruida por prueba directa de endpoints (sin navegador):

1. `WVSDocumentationWV7.jsp` → contiene un `<iframe>` a `AJDocumentation.jsp?CndWAVE=7&COUNTRY=`.
2. `AJDocumentation.jsp?CndWAVE=7&COUNTRY=` → tabla de 100+ países-año de la Ola 7; fila `Mexico 2018`, atributo `id="3203"` (identificador de muestra, `SAID`).
3. `AJDocumentationSmpl.jsp` (POST, `SAID=3203`) → ficha de México 2018 con lista de documentos, cada uno con un id de descarga (`DOID`) invocado por `DocDownload(doid)`:
   - `WVS7 Questionnaire Mexico 2018 Spanish.pdf` — **DOID 6635**
   - `WVS7 Methodology Report Mexico 2018.pdf` — DOID 8602
   - `WVS7 Sample Design Mexico 2018.pdf` — DOID 10701
   - `WVS7 Information about the team Mexico 2018.pdf` — DOID 10700
   - más el dataset (Excel/SPSS/Stata/CSV — no perseguido, es microdato, fuera del alcance del encargo)

Esto **localiza el documento con precisión total**: título exacto, edición (2018), país (México), identificador interno (`DOID 6635`, `SAID 3203`). No es "no está en disco" ni "portal sin enlaces" (el caso de ENCUP) — es un documento nombrado y direccionado con exactitud.

### 3.2 Por qué no se pudo leer: mecanismo de descarga no replicable sin navegador

`DocDownload(doid)` postea un formulario (`name=Datos`) a `AJDownload.jsp` con los campos ocultos vigentes en ese momento (`ulthost`, `CMSID`, `CndWAVE`, `SAID`, `DOID`, `AJArchive`, `EdFunction`, `DOP`, `XU`, `PUB`). Se replicó esa cadena completa —incluida la persistencia de `JSESSIONID` entre pasos— y se probaron, en orden, sin éxito:

1. POST solo con `DOID`.
2. POST con `DOID` + `SAID` + `AJArchive`.
3. POST con los diez campos ocultos exactos de la página, en el orden que aparecen.
4. Las tres variantes anteriores repitiendo la cabecera `X-Requested-With: XMLHttpRequest`.
5. Las tres variantes con cabecera `Referer` apuntando a `AJDocumentationSmpl.jsp`.
6. GET equivalente (mismos parámetros por query string) en vez de POST.
7. Con `User-Agent` de navegador real (Chrome/124) en vez del de `curl`.
8. Reiniciando la sesión completa (`wvs.jsp` → `WVSDocumentationWV7.jsp` → `AJDocumentation.jsp` → `AJDocumentationSmpl.jsp` → `AJDownload.jsp`) para asegurar que `JSESSIONID` fuera el mismo en las cuatro paradas.

**Las ocho variantes devolvieron el mismo resultado**: `HTTP/2 200`, `content-length: 1`, cuerpo = un solo carácter espacio (`0x20`). El servidor responde (no es un host inalcanzable, no es un 404, no es un timeout de red) pero no entrega el archivo — el estado que valida qué `DOID` es descargable para una sesión dada vive en el servidor de una forma que esta sesión no pudo reconstruir sin ejecutar el JavaScript real del cliente (posiblemente un paso intermedio disparado por eventos DOM, no solo por los valores de formulario).

**Veredicto: NO DETERMINABLE — documento localizado pero ilegible dentro del alcance de esta sesión.** No es "sin reactivo" (no se leyó el instrumento) ni "host fuera de perímetro" (el host respondió 200 en todos los pasos, con sesión válida). El dato que el encargo cita como conocido por fama —WVS incluye históricamente un ítem de "cualidades deseables en los niños" con la opción "Obediencia"— **no se verifica aquí contra el instrumento real de México 2018**: es exactamente el tipo de afirmación que Encargo C ya señaló no usar como veredicto ("es conocimiento externo al corpus, no una lectura de diccionario"). Se declara como razón para no cerrar esta candidata como agotada, no como hallazgo.

**Ruta de recuperación anotada:** un navegador real (o una sesión con herramienta de automatización de navegador) resolvería esto en un paso; el archivo existe y está nombrado con precisión (`DOID 6635`).

---

## 4 · Latinobarómetro

### 4.1 Localización

`https://www.latinobarometro.org` → `documentacion-datos` → `agregados` → `latinobarometro-2024` (última ola completa; 2025 está en licitación según el propio sitio, sin instrumento aún). Esta ruta **no** usa el mecanismo AJAX con sesión de WVS ni el shell JS de ENCUP: son enlaces `href` directos a PDF estático. Dos documentos descargados y leídos completos:

- `latinobarometro-2024-cuestionario-esp.pdf` (cuestionario regional 2024, aplicado en los 17 países de la ola, incluido México)
- `latinobarometro-2024-fichas-tecnicas.pdf` (ficha técnica: empresa, método, muestra y fechas por país)

### 4.2 País-año-n de la muestra mexicana (exigido por el encargo para las tres internacionales)

De la ficha técnica: **México — Moreno & Sotnikova Social Research and Consulting — muestra en 4 etapas, probabilística en 3 etapas y por cuota en la etapa final — n=1200 — levantamiento del 27 de agosto al 8 de septiembre de 2024 — error muestral ±2.8% — representatividad 100%.** El estudio completo: 19,214 entrevistas cara a cara en 17 países, del 23 de agosto al 9 de octubre de 2024. El cuestionario es el mismo instrumento regional para los 10 países sudamericanos y México (1200 casos c/u); no hay anotación en el propio cuestionario ni en la ficha técnica de que el ítem relevante (`P4NOIJ`, §4.3) se excluya de algún país — no se encontró ningún marcador "SOLO PARA [país]" adyacente a esa pregunta en el barrido de términos completo del PDF.

### 4.3 El ítem: `P4NOIJ`

> *P4NOIJ. (MOSTRAR TARJETA 24) Pensando en las cualidades que se pueden alentar en los niños en el hogar, si tuviera que escoger, ¿cuáles considera usted que es especialmente importante de enseñar a un niño? Por favor escoja hasta cinco alternativas.*
> Opciones incluyen: Buenos modales, Independencia, Trabajo duro/dedicación al trabajo, Sentido de responsabilidad, Imaginación, Tolerancia y respeto a los demás, Ser ahorrativo con el dinero, Determinación y perseverancia, Fe religiosa, Generosidad, **Obediencia**, Respeto al medio ambiente, Sentido de justicia-equidad, Diversidad sexual, Respeto a los animales.

Es exactamente el tipo de ítem que el encargo cita por fama de WVS ("cualidades deseables en niños"), pero aquí **sí se verificó contra el instrumento real** (no contra su fama): existe, en el cuestionario 2024, aplicado en México con n=1200.

### 4.4 Veredicto: PROXY CON SUPUESTO DECLARADO

**Por qué no es REACTIVO DIRECTO.** El constructo que el motor necesita (`R2.1`) es deferencia **ante una jerarquía concreta** (jefe, patrón, cabeza de familia), con efecto conductual (iniciativa suprimida, el "sí" que significa "probablemente"). `P4NOIJ` no pregunta sobre ninguna relación jerárquica concreta ni sobre la conducta del propio respondiente: pregunta qué valor debería **inculcarse a un niño**. Es un ítem de **orientación de valores** (la familia clásica de escalas de "autonomía vs. obediencia" en la crianza — Inglehart/Alwin, usada extensamente en WVS/Latinobarómetro como marcador de valores autoritarios vs. libertarios), no una medición directa de conducta ante jerarquía.

**El supuesto que convierte esto en proxy válido, declarado sin evitarlo:** valorar la obediencia como cualidad a enseñar a los propios hijos es una **orientación general hacia la deferencia/sumisión a la autoridad como principio**, que la literatura de valores trata como covariante — no como sinónimo — de la conducta de deferencia ante una jerarquía laboral o familiar concreta. El ítem no distingue: (a) si quien valora la obediencia en sus hijos también la practica él mismo ante su propio jefe o patriarca; (b) si el valor se sostiene por convicción o por adaptación a un entorno donde la desobediencia tiene costo (la misma ambigüedad que ya cargan los proxies conductuales de `familismo_obligacion` en Encargo C — obligación/afecto/falta de alternativa); (c) si "obediencia" en este contexto (crianza) se transmite igual al dominio laboral que `R2.1` describe. **No resuelve estas tres ambigüedades — las declara.**

**Contraste con `AP5_11` de ENCUCI (Encargo C), para no relajar el criterio:** `AP5_11` fue descartado *sin ni siquiera calificar como proxy* porque su objeto de actitud (legitimidad de la ley) es una categoría distinta de la jerarquía interpersonal — no hay forma de leerlo como "el mismo constructo con un supuesto de por medio". `P4NOIJ` sí comparte objeto de actitud con `R2.1` (deferencia/obediencia a la autoridad como disposición), solo que a un nivel de generalidad distinto (valor normativo sobre crianza vs. conducta en una relación jerárquica específica) — por eso aquí sí calza como **proxy con supuesto declarado**, y no como descarte total.

---

## 5 · ENCUP

### 5.1 El portal INEGI: confirmado como SPA sin instrumento estático, con más profundidad que Encargo C

Encargo C reportó "página cáscara renderizada por JS, no resuelto". Esta sesión fue más allá:

- El HTML crudo de `https://www.inegi.org.mx/programas/encup/2012/` (2828 bytes) confirma que todo el contenido —incluida la sección de documentación— se renderiza vía componentes web personalizados (`<presentacion-gen>`, `<menu-gen>`, `<pestanas-gen>`) sin contenido estático.
- El archivo de configuración de pestañas (`/programas/encup/2012/data/pestana/pestanadata.js`, mismo patrón usado para ENUT en `forense/notas/2026-07-31-enut-descarga.md`) muestra que **ENCUP solo tiene dos pestañas: "Documentación" y "Publicaciones" — no tiene pestaña de Microdatos ni de Tabulados**, a diferencia de ENUT (que sí las tiene, y de ahí salió su diccionario). La pestaña "Documentación" usa el componente `ldocumentos-inegi`, que no expone su endpoint de datos vía `urlComp` (viene embebido en el framework general del sitio, `sitioinegi.com.js`) — a diferencia de `descargaMasivaV2` (el componente de Microdatos/Tabulados), cuyo mecanismo sí quedó documentado en la sesión de ENUT. Se intentaron 7 rutas de endpoint por analogía de nombre (`listadoDocs1.js`/`.json` bajo variantes de ruta) — las 7 devolvieron la página de error 404 propia del sitio.
- **Evidencia adicional, no disponible en Encargo C:** el catálogo de metadatos oficial de INEGI (Red Nacional de Metadatos, RNM — el mismo mecanismo que en Encargo C dio el diccionario de variables de ENUT) se consultó vía su API de búsqueda (`/rnm/index.php/api/catalog/search`). Búsquedas por "Cultura Política", "Encuesta Nacional sobre Cultura Política" y "Practicas Ciudadanas" sí devuelven resultados (23, 14 y 7 respectivamente) — pero **ninguno de esos resultados es ENCUP**: aparecen ENCUCI, ENUT, censos de gobierno, etc., encuestas del mismo dominio temático, pero ninguna entrada de catálogo bajo el nombre "ENCUP" en ninguna de las tres búsquedas. **ENCUP no está indexado en el catálogo de metadatos de INEGI**, a diferencia de sus encuestas hermanas.

### 5.2 El espejo SEGOB: fuera del sandbox, con evidencia de red (no solo de lista de hosts)

`https://fomentocivico.segob.gob.mx/es/FomentoCivico/ENCUP` (citado en `data/inventarios/inventario_fuentes_cultura_valores_opinion_mexico.md:67`) se probó a través del mismo proxy que sí alcanza los otros cuatro hosts. El túnel `CONNECT` se establece (`HTTP/1.1 200 Connection Established`, autenticación de proxy aceptada), pero el `ClientHello` TLS hacia el destino nunca recibe respuesta: `curl -v` expira a los 15 segundos exactos del `--max-time`, con el mensaje `Connection timed out after 15002 milliseconds`, inmediatamente después de `TLS handshake, Client hello (1)`. Esto es distinto de un bloqueo inmediato del proxy (que habría devuelto un código de error HTTP en el propio `CONNECT`) — es consistente con un firewall de salida que acepta la conexión pero descarta el tráfico hacia ese destino específico en silencio.

### 5.3 Veredicto: NO DETERMINABLE — espejo fuera del sandbox

Por regla explícita del encargo: el portal INEGI de ENCUP **sí** resultó ser una SPA sin instrumento descargable (confirmado con más profundidad que en Encargo C: sin pestaña de Microdatos/Tabulados, sin entrada en el catálogo RNM). El cierre correspondiente, por instrucción textual del encargo, es **NO DETERMINABLE — espejo fuera del sandbox**, no SIN REACTIVO. Ruta de recuperación anotada: (a) descarga manual del archivo por el autor desde `fomentocivico.segob.gob.mx`, fuera de este entorno; (b) una sesión futura con ese host agregado a la lista de hosts permitidos del sandbox.

---

## 6 · Manifiesto — payload descargado y leído esta sesión

Tres archivos se guardaron en `data/raw/` (symlink a `/home/pc0/mm-corpus/raw/`, gitignorado) y se registraron con `tests/manifiesto.py --registra`, luego verificados con `--verifica` (los tres: `COINCIDE`, sha256 y tamaño contra `data/manifiesto.yaml`):

| id | Archivo | Origen | Uso |
|---|---|---|---|
| `lapop_abmex2023_cuestionario_mexico` | `lapop_abmex2023_cuestionario.pdf` (627 114 bytes) | `vanderbilt.edu/lapop/mexico/ABMex2023-Mexico-Questionnaire-V9.2.3.0-Spa-230511-W.pdf` | Barrido completo de términos, §2 |
| `latinobarometro2024_cuestionario_esp` | `latinobarometro2024_cuestionario_esp.pdf` (430 128 bytes) | `latinobarometro.org/documents/LAT-2024/latinobarometro-2024-cuestionario-esp.pdf` | Localización de `P4NOIJ`, §4.3 |
| `latinobarometro2024_fichas_tecnicas` | `latinobarometro2024_fichas_tecnicas.pdf` (16 325 bytes) | `latinobarometro.org/documents/LAT-2024/latinobarometro-2024-fichas-tecnicas.pdf` | País-año-n de México, §4.2 |

WVS: ningún archivo persistente se obtuvo (la descarga devolvió un cuerpo de 1 byte, no un documento) — no hay payload que registrar. ENCUP: ningún archivo de instrumento existe para descargar (portal sin instrumento estático) — no hay payload que registrar. El informe completo de Latinobarómetro 2024 (`latinobarometro-informe-2024.pdf`, 8.9 MB) se descargó a un directorio temporal de esta sesión para evaluar su tamaño, pero **no se leyó ni se movió a `data/raw/`** — no se registra en el manifiesto porque no fue usado como evidencia.

---

## 7 · Propuesta de enmienda a ADR-51 (sin sellar)

> No rige. Es material para que la mesa decida, exactamente como Encargo C §4 y `forense/hitoE-campana-medicion-v2_0.md` presentaron sin sellar nada.

**Aplica a `deferencia` (G6).** Estado hoy en ADR-51 §(c): "NO DETERMINABLE — no colapsable a límite permanente... cola de verificación declarada (C-bis)". Con esta sesión:

- **Fuente:** Latinobarómetro (ola 2024, cuestionario regional aplicado en México n=1200, 27 ago–8 sep 2024)
- **Reactivo:** `P4NOIJ` — "Obediencia" entre 15 cualidades a inculcar en los niños (escoger hasta 5)
- **Unidad:** persona entrevistada de 18 años y más (16 en Brasil, no aplica a México)
- **Operacionalización propuesta:** indicador binario o de frecuencia — el respondiente incluyó "Obediencia" entre las cualidades escogidas — como proxy de orientación de valor hacia la deferencia/sumisión a la autoridad, vía crianza declarada
- **Supuesto declarado, no resuelto:** valorar la obediencia en la crianza ≈ orientación general hacia la deferencia a la autoridad, que covaría con —pero no mide directamente— la conducta de iniciativa suprimida ante una jerarquía laboral o familiar concreta que `R2.1` describe. No distingue automáticamente convicción de adaptación al entorno, ni transferencia del dominio de crianza al dominio laboral
- **Lo que esto NO decide:** si el proxy sustituye a un reactivo directo si WVS o ENCUP eventualmente se abren (ambos quedan como candidatas activas, no cerradas — §3, §5); ni si el nivel de generalidad (valor normativo vs. conducta) es aceptable para el uso que el motor le dará a `deferencia`, decisión de mesa separada (misma regla que Encargo C §4: "ninguna entrada de la capa medida se escribe en la casilla de un peso del generador... por separado y en mesa")

Si la mesa sella esto, `deferencia` pasa de 0 a 1 fuente instrumentable con dato públicamente accesible (el cuestionario ya está leído; el microdato de Latinobarómetro 2024 no se descargó en esta sesión — Fase A, solo instrumento). La cola C-bis **no se cierra**: WVS y ENCUP quedan como candidatas abiertas con razones declaradas, no agotadas.

---

## 8 · Fuera de perímetro, y por qué no se tocó

No se descargó microdato de ninguna fuente (ningún `.zip`/`.sav`/`.dta`/`.csv` de base de datos — se verificó que los enlaces de dataset de WVS y Latinobarómetro existen pero no se persiguieron). No se modificó `milpa/procedencia.yaml`. No se selló ningún ADR. No se tocó `canon/`. No se registró entrada en `forense/hallazgos.md` — el encargo pidió una nota vía PR, no un hallazgo formal de instrumento (protocolo §5: eso solo aplicaría si algo impidiera medir, y aquí sí se pudo medir/reportar). El intento fallido de descarga de WVS y la ruta de recuperación de ENCUP quedan documentados en §3 y §5 respectivamente, no como hallazgo de proceso separado, por instrucción del propio encargo ("el fallo se reporta con su error textual y su URL").
