# Expediente 02 · OECD Trust Survey PUM 2021/2023/2025

Estado: **FORMULARIO TÉCNICO COMPLETO; LISTO-PARA-TITULAR; NO ENVIADO**.
Canal y formulario comprobados el 11 de septiembre de 2026.

## Formulario vigente y canal

- Página oficial: [OECD Trust Survey Data](https://www.oecd.org/en/data/datasets/oecd-trust-survey-data.html).
- Formulario técnico preparado:
  [`02-OECD-TRUST-PUM-TECHNICAL-DRAFT.docx`](02-OECD-TRUST-PUM-TECHNICAL-DRAFT.docx).
- Destinatario publicado: **`govtrustinfo@oecd.org`**.
- Asunto: `Request for OECD Trust Survey Public Use Microdata — Mexico`
- Elegibilidad publicada: investigación académica o de políticas públicas no
  comercial. La OECD revisa que la pregunta pueda responderse con la encuesta y
  que necesite microdatos en vez de indicadores/StatLinks.

El DOCX deriva del formulario ya registrado
`tc_oecd_trust_survey_pum_2021_2023_2025` y conserva su estructura. Están
completos `Intended use` y `Planned outputs`. Permanecen vacíos, deliberadamente,
la fecha esperada de conclusión, nombre, afiliación, país, firma y fecha.

## Alcance técnico que contiene el DOCX

Pregunta: para México, relacionar confianza interpersonal e institucional con
integridad, confiabilidad, capacidad de respuesta, apertura y equidad, y evaluar
heterogeneidad por conexiones sociales u organizacionales. México se pide en
cada ola en que realmente esté presente entre 2021/2023/2025. Chile, Colombia y
Costa Rica son los únicos comparadores mínimos y sólo entran en variables/olas
armonizadas con México.

Variables mínimas: identificador PUM, país/ola, ponderadores y variables de
diseño o réplica publicadas; Q1; Q2; Q5 o equivalente de integridad/soborno;
Q8-Q22 o impulsores armonizados; Q33-Q34 o equivalentes de participación,
voluntariado, asociación y redes; B14 o experiencia armonizada; modo y controles
demográficos/económicos liberados. La numeración se valida contra cada
cuestionario entregado antes de comparar olas.

Los indicadores públicos ya obtenidos no permiten distribuciones conjuntas,
ajuste por covariables, tamaños de subgrupo, faltantes ni equivalencia
individual. Por eso la solicitud no repite esos indicadores. El resultado se
usa como robustez de N30 y **no** reemplaza WVS7/R8.3 sin demostrar comparación
de constructo y población.

Tratamiento: acceso sólo por firmantes aprobados en el entorno real que declaren
fuera del repo; sin redistribución ni reidentificación; únicamente agregados,
supresión de celdas pequeñas conforme a términos, cita y disclaimer OECD. La
retención y destrucción se ajustan al acuerdo firmado; este borrador no inventa
fecha ni infraestructura.

## Correo final para copiar

> Dear OECD Trust Survey team,  
> Please find attached my completed Terms of Use for access to the OECD Trust
> Survey Public Use Microdata. The proposed non-commercial research concerns
> respondent-level associations among institutional trust, perceived integrity
> and other trust drivers, and social or organisational connections in Mexico.
> Public indicators are insufficient because the project requires joint
> distributions, subgroup sample sizes, missingness checks and harmonised
> multivariable analysis. The form limits any comparison to Mexico and the
> minimum harmonised Latin American comparators actually available in the PUM.
> Please let me know if a different form or additional truthful information is
> required.  
> Kind regards,  
> [REAL NAME — complete only in the private copy]

Adjunto exacto: la copia **privada** del DOCX de este directorio después de
completar y firmar sus seis campos pendientes. No enviar la copia versionada sin
firma.

## Dato del titular

| dato faltante del titular | por qué se exige | dónde se escribe |
|---|---|---|
| fecha esperada real del proyecto | campo del formulario; no puede inferirse | `Expected completion date` |
| nombre real | identifica al solicitante | `Name` |
| afiliación real, si existe | elegibilidad y contacto | `Affiliation`; no inventar una |
| país real | campo del formulario | `Country` |
| firma y fecha reales | aceptación de términos | `Signature` y `Date` |

## Recepción y continuación

Conservar fuera de Git el correo enviado, Message-ID, adjunto firmado y
respuesta. Registrar olas y países concedidos, versión de PUM, condiciones y
vencimiento. Al recibir bytes: guardar fuera de Git; calcular SHA-256, tamaño,
formato, filas/columnas; cotejar cuestionario/diccionario, pesos y presencia
real de México. Un correo favorable sin archivo o enlace usable es `CONCEDIDO`,
no `OBTENIDO`.

El sucesor congela primero la correspondencia de variables/olas y los umbrales
de divulgación. Sólo después ejecuta N30; si Q33/Q34 o equivalentes no miden la
conexión requerida, se registra `EXISTE-NO-SATISFACE` sin sustituir el constructo.
