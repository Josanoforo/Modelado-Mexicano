# MAESTRA38-A1 · Paquete de recetas — cuenta/solicitud (Lote 3)

Tres candidatas de las 12 exigen cuenta o solicitud, verificado por sonda
directa (no supuesto): CSES, Reuters DNR, Pew (microdato completo — el
topline ya está `OBTENIDO`). Firma de mesa aplicable: **FP-291 "mesa
ejecuta recetas de cuenta/solicitud"** (vence 7 días desde el cierre de
este acto). Cada receta es ≤1 minuto de trabajo humano, verificado por su
propia brevedad — ninguna pide más de un formulario o una casilla.

## 1 · CSES (Comparative Study of Electoral Systems)

**Qué falta.** Registro gratuito en `cses.org` — verificado: la página
`cses.org/data-download/` no trae ningún enlace `.zip/.dta/.sav` en el HTML
servido, sólo el texto "Register".

**Receta.**
1. Ir a `https://cses.org/data-download/` y crear cuenta (correo +
   contraseña, sin aprobación manual — es un formulario de auto-registro).
2. Descargar el dataset integrado (Module 3, incluye México 2006/2009; y/o
   Module 5 si México aparece — verificar en la página de módulos) en
   formato Stata o SPSS.
3. Depositar en `descargas_mx/UNIVERSO-2026-09/CSES/` y anotar aquí el
   nombre exacto del archivo bajado.

## 2 · Reuters DNR (Digital News Report)

**Qué falta.** Solicitud a investigador — verificado por fuente pública
(no de la propia página, que no lista un formulario de solicitud
directo): "underlying data tables are available to academic or industry
researchers **on request**"; sólo gráficas/tablas agregadas son de
descarga libre.

**Receta.**
1. Ir a `https://reutersinstitute.politics.ox.ac.uk/digital-news-report/`
   y ubicar el contacto de solicitud de datos (o escribir a
   `info@digitalnewsreport.org` / el contacto que la página de recursos
   declare).
2. Solicitar el dataset de encuesta con desagregación México (no las
   gráficas agregadas, que no traen microdato).
3. Depositar la respuesta en `descargas_mx/UNIVERSO-2026-09/REUTERS-DNR/`
   cuando llegue — no tiene plazo de 1 minuto (la respuesta del Instituto
   no la controla mesa), pero el *pedirla* sí.

## 3 · Pew Research — Global Attitudes Survey, microdato completo

**Qué falta.** El topline (`pewresearch.org`, PDF agregado) ya está
`OBTENIDO` desde antes de este acto (`pew_gas2025_social_trust_topline`,
FP-29) — lo que falta es el **microdato** (.sav/.dta con respuesta
individual por país, incluye México). Verificado: "You need to log in or
create a free account to download datasets from Pew Research."

**Receta.**
1. Ir a `https://www.pewresearch.org/profile/registration/` y crear cuenta
   gratuita (correo + contraseña).
2. Ir a `https://www.pewresearch.org/dataset/spring-2025-survey-data/` y
   descargar el dataset (.sav o .dta), país México incluido.
3. Depositar en `descargas_mx/UNIVERSO-2026-09/PEW/` — el topline ya
   depositado (`FP29_PEW_2025/`) no se mueve ni se duplica.

## Fila PENDIENTE-DE-MESA

Las tres filas correspondientes viven en
`data/curacion-registro/cola-adquisicion-registro.tsv` (`estado_A4A5:
PENDIENTE` las tres; la fila de Pew declara en su nota que el topline ya
está `OBTENIDO` bajo otro id, sólo el microdato queda pendiente), citando
este archivo como `origen`. `[CENSO]` de N6
(`forense/notas/2026-09-03-MAESTRA37-N6-...`) las verá al correr sobre
`descargas_mx` después de que mesa deposite.
