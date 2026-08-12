# ACTO M-ADQ · Adquisición documental ENSAFI 2023 + ENFIH 2019 hasta el universo mínimo (ADR-69/70)

`ENCARGOS FINALES · PLAN DE DESCARGAS COMPLETO`, 12/ago/2026 (`forense/encargos/2026-08-12-encargos-finales-plan-descargas-completo.md`), §3. Worktree `/home/pc0/mm-m-adq-ensafi-enfih`, rama `acto-m-adq/ensafi-enfih`. Adquisición **documental**, no de microdato: ENFIH ya tiene descriptor (838 variables, 16 hojas) pero está por debajo del universo mínimo de ADR-69 (llegar a ficha RNM y cuestionario); ENSAFI está por debajo de ENFIH. Este acto no abre nada a nivel variable — eso es M-APERTURA (§6), gateado sobre el cierre de éste.

## 0 · ARRANQUE

1. **REPO.** Clon existente `/home/pc0/mm-m-adq-ensafi-enfih`. `git log -1`: `31c4ec3 forense/encargos: archiva ENCARGOS FINALES · PLAN DE DESCARGAS COMPLETO (A.3)`. `git status`: árbol limpio salvo `data/raw` (symlink esperado, gitignorado).
2. **SHA.** `origin/main = 11083af` (merge de PR #184, E4c Paso 3 corrida real R5.1-D2 — sin relación con este acto). `git rev-list --left-right --count origin/main...HEAD` → `0  1`: la rama es exactamente `origin/main` + el commit A.3 de este acto, sin deriva que re-derivar.
3. **data/raw.** Ya enlazado al abrir la sesión: `data/raw -> /home/pc0/mm-corpus/raw` (`readlink -f` confirma la ruta real). Este acto NO descarga microdato — no aplica la verificación PR#77 de corpus compartido.
4. **ENTORNO.** `CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE` sin definir → `sin_variable`. `curl -s -o /dev/null -w "%{http_code}\n" --max-time 10 https://www.inegi.org.mx/` → `200`, verificado en esta sesión. Firma de caja (`sin_variable` + sonda 200) — este acto acepta nube o caja; se declara **caja**, libre en esta sesión (P·Lote-1 ya reclamó `mm-p-lote1-adquisicion` en caja, pero ambos actos corren en paralelo por diseño del documento, perímetros disjuntos salvo el puntero de puertas).
5. **ESPEJO.** No se usó. Toda cifra de esta nota sale de comandos corridos en esta sesión (`curl`, `git`, `grep`, `python3`), con el comando a la vista donde importa.
5-bis. **CONCURRENCIA (regla de mesa para este acto, no del bloque ARRANQUE estándar).** `data/manifiesto.yaml` (reescritura completa vía `yaml.dump`) y `data/universo-puertas-2026-08-12.tsv` (puntero de puertas/activos documentales) son de un solo escritor a la vez entre este acto y P·Lote-1, que corre en paralelo. Este acto llega hasta clasificar cada pieza y **propone** las filas del conducto sin escribirlas — mesa secuencia la escritura real. Declarado explícitamente al cierre del Commit 2 (§2.3).

**Regla A.3 aplicada primero.** El texto completo del encargo (los ocho §, §0-§8) se archivó como *primer commit* de la sesión, antes de este acto (`31c4ec3`, ya en `HEAD` al abrir esta sesión).

**Verificado por comando, no de memoria (Commit 1(b)):**

```
$ awk -F'\t' '$3=="ENFIH" || $3=="ENSAFI"' data/curacion-registro/relaciones.tsv \
  | awk -F'\t' '{print $3" capa3="$11}' | sort -u
ENFIH capa3=EXISTE;COINCIDE;INTEGRO
ENSAFI capa3=EXISTE;COINCIDE;INTEGRO

$ ls data/raw/ensafi2023/
ensafi_2023_bd_csv.zip
$ ls data/raw/enfih2019/
enfih_2019_base_de_datos_csv.zip  enfih_2019_fd.xlsx

$ grep -n "^- id:.*ensafi\|^- id:.*enfih" data/manifiesto.yaml
3928:- id: ensafi2023_bd_csv_zip
3994:- id: enfih2019_bd_csv_zip
4014:- id: enfih2019_fd_xlsx

$ grep -in "ensafi\|enfih" data/universo-puertas-2026-08-12.tsv data/universo-puertas-2026-08-08.tsv
(sin resultados para ninguna fila real — el único hit es "ENFIH" citado de pasada dentro de la fila NO-ENCONTRADO
de ITAM_panel_household_finance, no una fila propia de ENSAFI/ENFIH)
```

Confirma el terreno que el encargo supone, con una corrección de detalle: **el nivel 1 ("el payload y su descriptor") NO está parejo entre las dos fuentes.** ENFIH tiene ambos (ZIP + `enfih_2019_fd.xlsx`, 16 hojas). ENSAFI **solo tiene el ZIP** — no hay ningún `*_fd.xlsx` ni equivalente en `data/raw/ensafi2023/`, y el propio `manifiesto.yaml` (entrada `ensafi2023_bd_csv_zip`, escrita 2026-08-04/05) ya documenta que ese hueco se investigó una vez, con un único patrón de URL (`.../ensafi/2023/microdatos/...`, soft-404 de 2263 B) y sin llegar a la RNM — exactamente el defecto que ADR-69 nombra (universo declarado incompleto, no falta de rigor dentro de él). Este acto retoma esa pieza.

## 1 · Commit 1 — Pre-registro

### 1.1 · Qué exige el universo mínimo (a) — leído de `data/UNIVERSO-MINIMO-FUENTE-v1_0.md`, no parafraseado

Seis niveles, costo creciente (archivo íntegro leído en esta sesión antes de escribir esta nota): **(1)** payload+descriptor en `data/raw`. **(2)** PDF "Conociendo la base de datos" de la edición, si existe. **(3)** ficha RNM (`/rnm/index.php/catalog/{id}`) — muestreo, recolección de datos (periodo de ejecución/levantamiento/referencia con fecha inicio/fin), factores de expansión por tabla con nombre exacto de columna, tasa de respuesta, cuestionarios por sección, política de acceso; exportable en `/rnm/index.php/metadata/export/{id}/json` y `/ddi`; el buscador interno del catálogo está roto (devuelve el catálogo completo sin filtrar) — el `{id}` se obtiene por navegación directa o enlace ya conocido, nunca por ese buscador. **(4)** indicadores de calidad publicados (CV/EE/IC), típicamente en `/rnm/index.php/catalog/{id}/download/{n}` — verificar `Content-Type`/`Content-Disposition` antes de registrar, un enlace catalogado no garantiza el documento correcto. **(5)** documentos de biblioteca que la ficha cite (Diseño muestral, Informe operativo, Diseño conceptual) en `https://www.inegi.org.mx/app/biblioteca/ficha.html?upc={id}`. **(6)** DOF, solo si la cifra buscada es un umbral/índice/regla de programa, no dato de encuesta.

La regla de cierre: un `NO-ENCONTRADO` sobre un campo material declara qué niveles se recorrieron y cuáles no, con mecanismo y fecha. Un nivel no recorrido es un pendiente, no un hallazgo negativo.

### 1.2 · ENSAFI 2023

**(b) Ya en el conducto:** payload (`ensafi2023_bd_csv_zip`, ZIP, en `data/raw` y `manifiesto.yaml`) — nivel 1 **parcial**, sin descriptor propio. Cero filas en `universo-puertas-*.tsv`. Ninguna nota previa del repo abrió una ficha RNM para esta fuente (verificado: `grep -rin "rnm.*ensafi\|ensafi.*rnm" forense/ data/ canon/` no trae ninguna apertura, solo una URL de metadatos citada sin abrir en `data/inventarios/inventario-fuentes-credito-ahorro-finanzas-hogar-mexico.md:111` y una fila `NO_INSPECCIONADO` en `data/curacion-universo/universo-declarado-t0.tsv:32889`).

**(c) Qué falta, pieza por pieza:** (i) descriptor/FD (resto del nivel 1); (ii) PDF "Conociendo la base de datos" (nivel 2); (iii) la ficha RNM misma (nivel 3, identidad sin confirmar en sesión); (iv) factores de expansión con nombre exacto de columna; (v) tasa de respuesta; (vi) cuestionario por sección; (vii) política de acceso; (viii) indicadores de calidad (nivel 4); (ix) documentos de biblioteca — Diseño muestral, Informe operativo, Diseño conceptual (nivel 5); (x) DOF (nivel 6, aplicabilidad por confirmar).

**(d) Dónde se buscará:** (iii)-(vii) en la ficha candidata `https://www.inegi.org.mx/rnm/index.php/catalog/992` — **SIN-FETCH hasta abrir (A.6)**: el id 992 viene de `inventario-fuentes-credito-ahorro-finanzas-hogar-mexico.md:111`, nunca abierto en este repo, se trata como candidata no confirmada hasta sondearla en esta sesión. (i)/(ii) en el portal del programa (`inegi.org.mx/programas/ensafi/2023/` y variantes `contenidos/programas/ensafi/2023/...`) y, si la ficha existe, en su pestaña de diccionario de datos. (viii) en los enlaces `/download/{n}` que la ficha declare. (ix) en la pestaña "Materiales de Referencia" de la ficha y en las citas `biblioteca/ficha.html?upc=...` que su prosa incluya. (x) no aplica salvo que alguna pieza resulte ser un umbral/índice — se declara explícitamente si no.

**(e) Criterio A.4 por pieza:** **EXISTE-SATISFACE** = documento localizado y abierto byte a byte en esta sesión, con `Content-Type`/portada confirmando que es el documento correcto (fuente+año+tipo), no solo el enlace catalogado. **EXISTE-NO-SATISFACE** = localizado pero incompleto o de identidad distinta a la buscada, declarando qué falta. **NO-ENCONTRADO** = los niveles pertinentes recorridos sin hallar la pieza, con términos y portales declarados. **NO-ACCESIBLE** = localizado pero detrás de pago o afiliación institucional (registro gratuito no cuenta como NO-ACCESIBLE).

### 1.3 · ENFIH 2019

**(b) Ya en el conducto:** payload + descriptor completos (`enfih2019_bd_csv_zip` + `enfih2019_fd_xlsx`, 16 hojas, en `data/raw` y `manifiesto.yaml`) — nivel 1 **satisfecho**. Cero filas en `universo-puertas-*.tsv`. Ninguna nota previa del repo abrió una ficha RNM para esta fuente (mismo grep que ENSAFI, sin resultados de apertura); URL de metadatos citada sin abrir en `inventario-fuentes-credito-ahorro-finanzas-hogar-mexico.md:123` y fila `NO_INSPECCIONADO` en `universo-declarado-t0.tsv:15084`.

**(c) Qué falta, pieza por pieza:** (i) PDF "Conociendo la base de datos" (nivel 2); (ii) la ficha RNM misma (nivel 3); (iii) factores de expansión con nombre exacto de columna; (iv) tasa de respuesta; (v) cuestionario por sección; (vi) política de acceso; (vii) indicadores de calidad (nivel 4); (viii) documentos de biblioteca (nivel 5); (ix) DOF (nivel 6, aplicabilidad por confirmar).

**(d) Dónde se buscará:** (ii)-(vi) en la ficha candidata `https://www.inegi.org.mx/rnm/index.php/catalog/709` — **SIN-FETCH hasta abrir (A.6)**, id de `inventario-fuentes-credito-ahorro-finanzas-hogar-mexico.md:123`, nunca abierto en este repo. (i) en el portal del programa (`inegi.org.mx/programas/enfih/2019/`, ya conocido como SPA por precedente de este repo para rutas `/programas/`) y su árbol `contenidos/programas/enfih/2019/...`. (vii) en los `/download/{n}` de la ficha. (viii) en "Materiales de Referencia" de la ficha, con fallback a `https://www.banxico.org.mx/enfih/` (espejo declarado en el inventario, INEGI+Banxico co-ejecutan esta encuesta) si el catálogo INEGI no da enlace directo. (ix) no aplica salvo hallazgo contrario, se declara.

**(e) Criterio A.4 por pieza:** idéntico a 1.2(e).

---

El primer resultado que produzca este procedimiento es el que se reporta.

## 2 · Commit 2 — Ejecución

Sonda A.5 en esta sesión sobre ambas fichas candidatas. Las dos existen y son las fuentes correctas — confirmado por `<title>`, no asumido del id:

```
$ curl -s -o /dev/null -w "%{http_code}\n" --max-time 15 https://www.inegi.org.mx/rnm/index.php/catalog/992
200
$ curl -s --max-time 20 https://www.inegi.org.mx/rnm/index.php/catalog/992 | grep -o "<title>[^<]*</title>"
<title>Mexico - Encuesta Nacional sobre Salud Financiera 2023</title>

$ curl -s -o /dev/null -w "%{http_code}\n" --max-time 15 https://www.inegi.org.mx/rnm/index.php/catalog/709
200
$ curl -s --max-time 20 https://www.inegi.org.mx/rnm/index.php/catalog/709 | grep -o "<title>[^<]*</title>"
<title>Mexico - Encuesta Nacional sobre las Finanzas de los Hogares (ENFIH) 2019</title>
```

Las candidatas SIN-FETCH de §1 quedan promovidas a EXISTE-SATISFACE para la pieza "ficha RNM misma" en ambas fuentes. Los HTML completos se guardaron para inspección estructurada (`BeautifulSoup`, secciones por `id` de la propia página: `metadata-sampling`, `metadata-data_collection`, `metadata-questionnaires`, `metadata-data_access`, `metadata-data_appraisal`, `related-materials`).

### 2.1 · ENSAFI 2023 — ficha RNM 992

**Muestreo — EXISTE-SATISFACE.** Sección "Muestreo" trae marco, procedimiento y estratificación en prosa completa (Comité de Aseguramiento de la Calidad del INEGI referenciado, deviación de muestreo declarada "Sin información" salvo el desglose de códigos de resultado — ver tasa de respuesta abajo).

**Recolección de datos — EXISTE-SATISFACE, con discrepancia interna declarada (mismo patrón que ficha 922/ENASIC, no resuelta aquí):**
- Tabla "Periodo de ejecución del proyecto estadístico", fila `Levantamiento`: **2023-08-14 / 2024-04-12**.
- La misma tabla, fila `Capacitación`: **2023-09-25 / 2023-11-17**.
- Prosa, §"1 Levantamiento de la información": *"El levantamiento de la ENSAFI 2023 se realizó a partir del 25 de septiembre y concluyó el 17 de noviembre"* — coincide exactamente con la fila `Capacitación` de la tabla, no con su propia fila `Levantamiento`.
- Las tres cifras se registran; no se elige una. Periodo de referencia: cuatro ventanas según bloque de preguntas — *"De octubre de 2022 a la fecha de la entrevista"* / *"Los últimos 3 meses"* / *"El mes pasado"* / *"La semana pasada"*. Modo de recolección: entrevista directa asistida por dispositivo de cómputo móvil (CAPI).

**Factores de expansión con nombre exacto de columna — EXISTE-SATISFACE.** No en la prosa de la ficha (menciona el *proceso* de cálculo, no los nombres) — hallado en el export DDI/JSON:

```
$ curl -s --max-time 20 https://www.inegi.org.mx/rnm/index.php/metadata/export/992/json -o export992.json   # HTTP 200, 121012 B
$ python3 -c "import json; d=json.load(open('export992.json'))['study_desc']['method']['data_collection']; print(d['weight'])"
FAC_VIV es el nemónico del campo utilizado para ponderar la muestra a nivel vivienda, y se
presenta en la tabla TVIVIENDA. FAC_HOG ... a nivel hogar ... THOGAR y TSDEM. FAC_ELE ...
a nivel de población de 18 años ... TMODULO. El factor de expansión se define como el
inverso de la probabilidad de selección.
```

Las tres tablas (TVIVIENDA/THOGAR·TSDEM/TMODULO) coinciden exactamente con las 4 tablas ya conocidas del payload (TSDEM/TVIVIENDA/THOGAR/TMODULO, únicas del ZIP).

**Tasa de respuesta — PARCIAL, declarado.** No hay una "tasa de respuesta" publicada como cifra única. Sí hay dos cifras distintas y no intercambiables: (a) la tasa de no-respuesta *asumida* en la fórmula de tamaño de muestra, 15% ("tnr = tasa de no respuesta máxima esperada... una tasa de no respuesta máxima esperada del 15%"); (b) la tabla real de resultados operativos, IKTAN web (SAM 01), diciembre 2023: **2,147 viviendas sin información = 9.34% del total de registros en muestra** (64.32% atribuible al marco de muestreo, 26.04% al informante, 9.64% otras situaciones). Ninguna de las dos se convierte aquí en una "tasa de respuesta" derivada — quedan como las cifras publicadas, a la vista de quien las necesite.

**Cuestionarios por sección — EXISTE-SATISFACE.** Ficha describe 10 secciones (1. Vivienda … 10. Conocimientos sobre CONDUSEF), con el detalle temático de cada una. Documento real localizado en la pestaña "Materiales de Referencia" y verificado byte a byte:

```
$ curl -s --max-time 20 -D - -o /dev/null https://www.inegi.org.mx/contenidos/programas/ensafi/2023/doc/ensafi_2023_cuestionario.pdf
HTTP/1.1 200 OK
Content-Type: application/pdf
Content-Length: 1182405
$ pdftotext -layout -f 1 -l 1 ensafi_2023_cuestionario.pdf -   # "...ENSAFI 2023 / CUESTIONARIO"
```

**Política de acceso — EXISTE-SATISFACE.** Uso Público; LSNIEG arts. 37/45/47/100; sin registro, contacto `atencion.usuarios@inegi.org.mx`.

**Indicadores de calidad (nivel 4) — EXISTE-SATISFACE.** Dos descargas en la ficha, verificadas por cabecera real (GET con `-D -`, nunca `-I`) y por apertura de contenido, no solo por el nombre declarado:

```
$ curl -s --max-time 20 -D - -o dl31624.bin https://www.inegi.org.mx/rnm/index.php/catalog/992/download/31624
Content-Disposition: attachment; filename="1_CV-EE-IC_IPE_Externos_Encuestas_2022_08_26.xlsx"   # 45,970 B, GENÉRICO multi-encuesta, no específico de ENSAFI
$ curl -s --max-time 20 -D - -o dl31625.bin https://www.inegi.org.mx/rnm/index.php/catalog/992/download/31625
Content-Disposition: attachment; filename="IPE_CV-EE-IC_ENSAFI_2023-00_Def_V1_180624.xlsx"      # 38,604 B, específico
```

`31625` abierto con `openpyxl` (hoja `INDICADORES`): **un solo indicador oficial publicado** — *"Población de 18 años y más según condición de tener dinero suficiente para cubrir sus gastos el último mes sin endeudarse"*, Estimación 69.52%, CV 0.923%, Error estándar 0.641, IC**90%** (68.46%, 70.57%). Nivel de confianza 90%, no 95% — declarado porque será relevante si algún acto posterior lo cruza contra un IC calculado con otra convención.

**Documentos de biblioteca (nivel 5) — EXISTE-SATISFACE, recuperado por la vía correcta tras un defecto de cita de INEGI declarado y no corregido:**

La prosa de la propia ficha (secciones "Muestreo" y "Recolección de Datos") cita dos documentos por `upc` como si fueran de ENSAFI:
- *"consultar el documento Encuesta Nacional sobre Salud Financiera (ENSAFI) 2023. Diseño muestral. https://www.inegi.org.mx/app/biblioteca/ficha.html?upc=889463903888"*
- *"consultar el documento Encuesta Nacional sobre Salud Financiera (ENSAFI) 2023. Informe operativo. https://www.inegi.org.mx/app/biblioteca/ficha.html?upc=889463903871"*

Esas páginas `biblioteca/ficha.html` son SPA (shell vacío, `id="titulo_producto"` sin contenido, poblado por JS — confirmado abriendo el HTML crudo, `inicializar()` en `onload`). Se derivó el patrón de descarga directa que este mismo repo ya usó con éxito para un documento de ENBIARE (`data/curacion-universo/activos-descubiertos-durante-ronda.tsv:2`, `.../bvinegi/productos/nueva_estruc/{upc}.pdf`) y se abrió byte a byte:

```
$ curl -s --max-time 20 -D - -o upc888.bin https://www.inegi.org.mx/contenidos/productos/prod_serv/contenidos/espanol/bvinegi/productos/nueva_estruc/889463903888.pdf
HTTP 200, Content-Type: application/pdf, 1,158,551 B
$ pdftotext -layout -f1 -l1 upc888.bin -
ENIF  Encuesta Nacional de Inclusión Financiera 2021 / Diseño muestral
```

**No es ENSAFI — es ENIF 2021.** Confirmado igual para `889463903871` (2,010,077 B): también ENIF 2021, "Informe operativo". **Defecto de cita del propio INEGI dentro de su ficha RNM 992, declarado aquí y no corregido en el catálogo** — exactamente la reserva que el nivel 4/5 del universo mínimo anticipa ("un enlace catalogado no garantiza que el recurso sea el documento buscado"), aplicada aquí a una cita en prosa, no solo a un `/download/{n}`.

Recuperado por la vía correcta: la pestaña **"Materiales de Referencia"** de la misma ficha (`/catalog/992/related-materials`) trae tres entradas con `upc` distintos, verificadas byte a byte:

| Documento (RNM) | upc | Bytes | Portada confirmada |
|---|---|---|---|
| Informe operativo y de procesamiento | 889463916277 | 2,689,964 | "2023 / Informe operativo y de procesamiento" |
| Documento conceptual | 889463918196 | 3,729,881 | "2023 / Documento conceptual" |
| Diseño muestral | 889463916840 | 1,540,078 | "2023 / Diseño muestral" |

Los tres, correctos.

**FD/descriptor (resto del nivel 1) — EXISTE-NO-SATISFACE, atenuado.** `/catalog/992/data-dictionary` (HTTP 200, navegable) lista las 4 tablas del payload con conteo de variables y descripción temática (`THOGAR` 55 vars/20,448 casos; `TSDEM` 25 vars/67,781 casos; `TMODULO`, `TVIVIENDA` con sus propios conteos) — es un diccionario de datos real, pero **no hay un archivo FD descargable** equivalente al `.xlsx` de ENFIH; el listado variable-por-variable completo (no solo el resumen por tabla) requiere renderizado JS que `curl` no ejecuta, o el export `/ddi` (no perseguido — fuera de las piezas nombradas por el universo mínimo, que no exige codebook completo). Qué falta declarado: exportación descargable variable-por-variable.

**"Conociendo la base de datos" (nivel 2) — NO-ENCONTRADO.** Ninguna de las cinco citas de biblioteca de la ficha 992 (las 2 mal citadas + las 3 correctas de la tabla de arriba) tiene ese título; tampoco aparece en `/catalog/992/data-dictionary` ni en la página principal de la ficha (`grep -il "conociendo la base"` sobre los 3 HTML de la ficha 992, sin resultados). Universo recorrido: los 3 tabs de la ficha (Información del proyecto / Diccionario de Datos / Materiales de Referencia) más el export JSON. No se intentó adivinar un id numérico de biblioteca sin cita — eso sería A.6 violado (candidata sin fundamento). Declarado NO-ENCONTRADO dentro de este universo, no "no existe".

**DOF (nivel 6) — no aplica.** Este acto no busca ninguna cifra de umbral, índice o regla de programa.

### 2.2 · ENFIH 2019 — ficha RNM 709

**Muestreo — EXISTE-SATISFACE**, más extenso que ENSAFI: Marco Nacional de Viviendas 2012 (INEGI, derivado del Censo 2010), Muestra Maestra de 240,912 UPM, formación de UPM por ámbito (urbano alto/complemento urbano/rural con rangos de vivienda por tipo), 683 estratos (geográfico × sociodemográfico, 34 indicadores multivariados), fórmula de tamaño de muestra con los mismos parámetros que ENSAFI (confianza 90%, DEFF 3.24, error relativo 15%, tnr 15%) → 22,931 viviendas calculadas, **ajustadas a 23,041** (nota menor: el inventario previo del repo, `inventario-fuentes-credito-ahorro-finanzas-hogar-mexico.md:120`, decía "ajustadas a 23 000" — la ficha RNM, fuente primaria, da 23,041; discrepancia de detalle declarada, no perseguida más).

**Recolección de datos — EXISTE-SATISFACE, con discrepancia interna declarada (mismo patrón que ENSAFI arriba y que la ficha 922/ENASIC ya documentada en `UNIVERSO-MINIMO-FUENTE-v1_0.md`):**
- Tabla "Periodo de ejecución del proyecto estadístico", fila `Levantamiento`: **2019-10-07 / 2019-11-19**.
- Tabla "Periodo de referencia", fila `La fecha de la entrevista`: **2019-10-07 / 2019-11-29**.
- Prosa, §"2.6 Levantamiento de la información": *"La etapa de recolección de información se llevó a cabo del 7 de octubre al 29 de noviembre de 2019"*.
- La prosa y el "Periodo de referencia" coinciden en la fecha de cierre (29 nov); la propia fila `Levantamiento` de "Periodo de ejecución" da 10 días menos (19 nov). Registradas las tres, sin resolver cuál se toma — igual que ENSAFI arriba, es material para quien selle `periodo_levantamiento` en un acto de cálculo, no para éste.

Modo de recolección: CAPI (mini laptop), igual que ENSAFI.

**Factores de expansión con nombre exacto de columna — EXISTE-SATISFACE**, vía export DDI/JSON (`/rnm/index.php/metadata/export/709/json`, HTTP 200, 93,964 B):

```
FAC_VIV ... ponderar las viviendas ... TViviendas. FAC_HOG ... ponderar los hogares ... THogares.
FACTOR ... ponderar los distintos universos de población total, de 3 a 29 años, de 3 años y
más, de 5 años o más, y de 12 años o más; en tabla TSDem. Asimismo, FACTOR es el ponderador
de los distintos activos y pasivos financieros ... en las tablas siguientes: TModulo,
TPropiedad, TComparte, TUnico, TAuto, TMoto, TDepar, TBanca, TNomina, TEduca, TPersonal
y TGrupal.
```

Tres nemónicos (`FAC_VIV`, `FAC_HOG`, `FACTOR`) cubriendo 14 tablas nombradas explícitamente.

**Tasa de respuesta — PARCIAL, mismo patrón que ENSAFI.** tnr asumida 15% (misma fórmula). Tabla real de resultados operativos, publicada dentro de `sampling_deviation` del export JSON: **3,405 viviendas "Sin información" = 14.78% del total de la muestra** (no respuesta atribuible al informante 6.56%, atribuible al marco 6.74%, otras situaciones 1.48%; desglose completo por código de resultado, 16 códigos). Mismo criterio: no se deriva aquí una "tasa de respuesta" — se deja el dato publicado.

**Cuestionarios por sección — EXISTE-SATISFACE.** Ficha describe 236 preguntas en 10 secciones + sección 4a (desglose exacto: 1. Residentes y hogares=3, 2. Sociodemográficas=10, 3. Vivienda=9, 4. Vivienda y deuda hipotecaria=55, 4a. Características personales=8, 5. Segundas propiedades=18, 6. Negocios=27, 7. Vehículos=23, 8. Deudas no hipotecarias=…). El catálogo (`related-materials`) cita el documento pero **sin enlace directo** — el `href` del botón "Descargar" apunta solo a `https://www.inegi.org.mx/programas/enfih/2019/`, confirmado SPA:

```
$ curl -s -o enfih_portal.html -w "%{http_code}\n" --max-time 15 https://www.inegi.org.mx/programas/enfih/2019/
200   # 3,952 B — shell React vacío (<menu-gen>, <presentacion-gen>, <pestanas-gen>, script src=".../react.inegi.min.js")
```

Confirma, para esta fuente y de primera mano, el hecho de mecanismo ya documentado del repo ("`/programas/` es SPA, no navegable por curl"). Se **derivó** la URL directa por analogía con el patrón ya confirmado de ENSAFI (`contenidos/programas/{acrónimo}/{año}/doc/{acrónimo}_{año}_{tipo}.pdf`) y se verificó byte a byte — candidata SIN-FETCH hasta este momento (A.6), promovida tras abrir:

```
$ curl -s --max-time 20 -D - -o enfih_cuestionario.bin https://www.inegi.org.mx/contenidos/programas/enfih/2019/doc/enfih_2019_cuestionario.pdf
HTTP 200, Content-Type: application/pdf, 1,262,902 B
$ pdftotext -layout -f1 -l1 enfih_cuestionario.bin -
Encuesta Nacional sobre las Finanzas de los Hogares (ENFIH) 2019 / CUESTIONARIO
```

Confirmado correcto. El propio export JSON de la ficha, en la sección de resultados operativos, cita esta misma URL derivada como fuente del "Informe operativo" (ver tabla de biblioteca abajo) — corroboración independiente de que el patrón derivado es el real, no una coincidencia de nomenclatura.

**Política de acceso — EXISTE-SATISFACE.** Mismo régimen que ENSAFI (LSNIEG arts. 37/45/47/100, Uso Público, sin registro).

**Indicadores de calidad (nivel 4) — EXISTE-SATISFACE, tras resolver una anomalía real de archivo:**

```
$ curl -s --max-time 20 -D - -o dl22877.bin https://www.inegi.org.mx/rnm/index.php/catalog/709/download/22877
Content-Disposition: attachment; filename="IndicadoresPrecisionEstadistica_CV_EE_IC_ENFIH_2019.xls"   # 62,976 B
$ file dl22877.bin
Composite Document File V2 ... Title: "ndice de confianza del consumidor. Componente 1" ...
```

El nombre de descarga declara ENFIH; el metadato interno del documento (propiedad "Título" de Office) declara un índice de una encuesta distinta (ICC). `strings` sobre el binario muestra tanto "ENFIH" (3 veces) como "Índice de Confianza del Consumidor" (varias veces) — no se resolvió por metadatos ni por texto plano. Se instaló `xlrd` (`pip install --target=... xlrd`, red permitida a `pypi.org` en este entorno) y se abrió la hoja de cálculo real:

```
$ python3 -c "import xlrd; wb=xlrd.open_workbook('dl22877.bin'); print(wb.sheet_names())"
['ENFIH', 'PE ICC 0818 (2)']
```

**Dos hojas: la primera (`ENFIH`) trae datos genuinos de ENFIH 2019**, dos indicadores oficiales completos —

| Variable | Parámetro | Estimador | CV | Error estándar | IC95% |
|---|---|---|---|---|---|
| Ingreso corriente efectivo anualizado (miles $) | Promedio | 162.71 | 1.248% | 2.031 | (158.73, 166.69) |
| Riqueza neta al momento de la entrevista (miles $) | Promedio | 759.02 | 4.752% | 36.07 | (688.33, 829.72) |

— la segunda hoja (`PE ICC 0818 (2)`) es un residuo de plantilla del Índice de Confianza del Consumidor, sin relación con ENFIH, que explica el metadato de título heredado y las cadenas de texto encontradas. **Anomalía explicada, no una fuente equivocada**: el archivo es genuinamente el indicador de ENFIH, contaminado por una hoja de plantilla no depurada — verificar solo `Content-Disposition` habría sido insuficiente (habría registrado el archivo correcto por casualidad); verificar solo el metadato de título habría sido un falso negativo (habría descartado un archivo correcto). Se registra el mecanismo completo, no solo el resultado.

`/download/22878` (144,475 B, `Metadatos_Indicadores_Encuestas_hog.pdf`) confirmado genérico — documento de 1 página que describe la estructura de columnas del formato estándar "pestaña Indicadores" usado en encuestas de hogares del INEGI en general, no datos de ENFIH.

**Documentos de biblioteca (nivel 5) — EXISTE-SATISFACE, por URL derivada (mismo patrón que el cuestionario):**

`related-materials` cita "Informe" e "Documento metodológico" ×2, los tres con el mismo `href` genérico (`https://www.inegi.org.mx/programas/enfih/2019/`, SPA confirmada arriba) — sin `upc` embebido a diferencia de ENSAFI. Se derivaron las tres URLs por el mismo patrón que resolvió el cuestionario, y se verificaron byte a byte:

| Documento (RNM) | URL derivada | Bytes | Portada confirmada |
|---|---|---|---|
| Informe operativo y de procesamiento | `.../enfih/2019/doc/enfih_2019_informe_operativo.pdf` | 3,924,195 | "ENFIH ... 2019 / Informe operativo" |
| Diseño muestral | `.../enfih/2019/doc/enfih_2019_diseno_muestral.pdf` | 3,631,468 | "ENFIH ... 2019 / Diseño muestral" |
| Diseño conceptual | `.../enfih/2019/doc/enfih_2019_diseno_conceptual.pdf` | 3,865,634 | "ENFIH ... 2019 / Diseño conceptual" |

Los tres, correctos. A diferencia de ENSAFI, aquí no hubo defecto de cita (la ficha nunca dio un `upc` equivocado) — solo un enlace roto/genérico que exigió derivación en vez de seguir un `href` directo.

**"Conociendo la base de datos" (nivel 2) — NO-ENCONTRADO.** Ninguna de las cuatro entradas de "Materiales de Referencia" tiene ese título; tampoco aparece en la página principal de la ficha ni en el export JSON (`grep -il "conociendo la base"` sobre los 3 HTML de la ficha 709, sin resultados). Universo recorrido: los tabs de la ficha, el portal SPA (shell sin contenido adicional) y el export JSON. No se probó el espejo de Banxico (`banxico.org.mx/enfih/`) para esta pieza específica — declarado como nivel no recorrido, no como hallazgo negativo adicional (la regla del universo mínimo: "un nivel no recorrido es un pendiente, no un hallazgo negativo").

**DOF (nivel 6) — no aplica.**

### 2.3 · Piezas listas para el conducto — PROPUESTAS, NO ESCRITAS

**Regla de concurrencia de mesa para este acto (§5-bis del ARRANQUE): `data/universo-puertas-2026-08-12.tsv` no se edita en esta sesión.** Ambas fichas quedan clasificadas `EXISTE-SATISFACE`, listas para pasar de FALTANTE a EN-CONDUCTO, pero la fila no se escribe — mesa secuencia el orden de escritura entre este acto y P·Lote-1, que toca el mismo puntero en paralelo. Filas propuestas, mismo formato y granularidad que el precedente ya sellado en esta tabla (`RNM_ENASIC_2022_ficha922`, `RNM_ENBIARE_2021_ficha730`, `RNM_ENCUCI_2020_ficha647` — una fila por ficha, no por sub-documento):

```
RNM_ENSAFI_2023_ficha992	catalogo_metadatos_inegi	INEGI (en colaboracion con CONDUSEF)	https://www.inegi.org.mx/rnm/index.php/catalog/992	ficha_metadatos_ddi	2023 (levantamiento declarado 25/sep-17/nov/2023 en prosa; tabla "Periodo de ejecucion" da 14/ago/2023-12/abr/2024 para su propia fila "Levantamiento" -- discrepancia interna, ver nota)	viviendas, hogares, persona elegida 18+; tablas TVIVIENDA/THOGAR/TSDEM/TMODULO	nacional y por entidad federativa	si, declarado en la ficha; fuente ya en corpus propio (ensafi2023_bd_csv_zip, manifiesto.yaml) pero sin FD descargable propio -- ver nota	publico, confidencialidad LSNIEG arts. 37/45/47/100; requiere citar fuente			EXISTE-SATISFACE	ficha de metadatos DDI de ENSAFI 2023; cuestionario (10 secciones) e indicadores de calidad (1, IC90%) verificados byte a byte; 3 documentos de biblioteca correctos via Materiales de Referencia (Informe operativo/Documento conceptual/Diseno muestral); DEFECTO declarado: 2 citas en prosa de la propia ficha (upc 889463903888/889463903871) resultaron ser documentos de ENIF 2021, no de ENSAFI, no corregido en el catalogo; ver forense/notas/2026-08-12-acto-m-adq-ensafi-enfih.md	2026-08-12
RNM_ENFIH_2019_ficha709	catalogo_metadatos_inegi	Banco de Mexico + INEGI (levantamiento INEGI)	https://www.inegi.org.mx/rnm/index.php/catalog/709	ficha_metadatos_ddi	2019 (levantamiento declarado 7/oct-29/nov/2019 en prosa y en tabla "Periodo de referencia"; tabla "Periodo de ejecucion" da 7/oct-19/nov/2019 para su propia fila "Levantamiento" -- discrepancia interna, ver nota)	viviendas, hogares; tablas TViviendas/THogares/TSDem/TModulo+11 tablas de activos-pasivos especificos	nacional	si, ya en corpus propio con descriptor completo (enfih2019_bd_csv_zip + enfih2019_fd_xlsx, 16 hojas, manifiesto.yaml)	publico, confidencialidad LSNIEG arts. 37/45/47/100; requiere citar fuente			EXISTE-SATISFACE	ficha de metadatos DDI de ENFIH 2019; cuestionario (236 preguntas, 10 secciones+4a) y 3 documentos de biblioteca (Informe operativo/Diseno muestral/Diseno conceptual) NO enlazados directo por el catalogo (Materiales de Referencia rebota a portal SPA) -- las 4 URLs derivadas por analogia con el patron de ENSAFI y verificadas byte a byte, portada correcta en las 4; indicador de calidad especifico con anomalia de archivo EXPLICADA (hoja residual de plantilla ICC ajena, hoja ENFIH con 2 indicadores geniunos confirmados abriendo el libro con xlrd); ver forense/notas/2026-08-12-acto-m-adq-ensafi-enfih.md	2026-08-12
```

(columnas `necesidad_que_sirve` y `llave_ADR57c_si_alguna` en blanco, mismo criterio que las tres fichas RNM ya selladas en esta tabla — no se inventa una asociación N-específica para un activo documental de fuente completa.)

### 2.4 · Cierre

**Contador: piezas del universo mínimo pasadas de FALTANTE a clasificadas (EN-CONDUCTO propuesto, pendiente de escritura secuenciada por mesa).** ENSAFI 2023: ficha RNM + muestreo + recolección (con discrepancia declarada) + factores de expansión + cuestionario + política de acceso + indicadores de calidad + documentos de biblioteca = **8 piezas EXISTE-SATISFACE**; FD/descriptor = 1 pieza EXISTE-NO-SATISFACE (atenuada, no cerrada); "Conociendo la base de datos" = 1 pieza NO-ENCONTRADO con universo agotado; DOF = no aplica, declarado. ENFIH 2019: mismas 8 categorías **EXISTE-SATISFACE** (el cuestionario y los 3 documentos de biblioteca vía URL derivada, no enlace directo); "Conociendo la base de datos" = 1 pieza NO-ENCONTRADO con universo agotado (Banxico no sondeado para esta pieza específica, declarado pendiente); DOF = no aplica.

Dos defectos de mecanismo reales, verificados de primera mano y no heredados de otra sesión: **(1)** dos citas en prosa dentro de la propia ficha RNM 992 de ENSAFI apuntan a documentos de ENIF 2021, no de ENSAFI — hallazgo propio de este acto, recuperado por la vía correcta (pestaña "Materiales de Referencia"). **(2)** el indicador de calidad específico de ENFIH (`download/22877`) es un archivo con una hoja residual de una plantilla ajena (Índice de Confianza del Consumidor) — no invalida el dato, exige abrir el libro completo para confirmarlo, no solo `Content-Disposition`.

Ninguna pieza queda `NO-ACCESIBLE` — todo lo localizado es de acceso público sin registro. Ninguna pieza requirió el nivel 6 (DOF). Este acto no abrió microdato a nivel variable en ningún momento — ni el cuestionario, ni los documentos de biblioteca, ni los indicadores de calidad se leyeron para extraer un valor de modelo; se abrieron para confirmar identidad y clasificar A.4, que es lo que el universo mínimo exige. El reporte que deja a M-APERTURA: las cuatro piezas nombradas por el propio acto (ficha RNM + cuestionario, para ambas fuentes) están **EN-CONDUCTO propuesto** — sin premisa floja sobre encabezados, que era el defecto que este acto existía para evitar.

Contador que NO se mueve: cero filas escritas en `data/universo-puertas-2026-08-12.tsv`, cero escrituras en `data/manifiesto.yaml` — perímetro respetado, concurrencia con P·Lote-1 resuelta por secuenciación de mesa, no por escritura simultánea.
