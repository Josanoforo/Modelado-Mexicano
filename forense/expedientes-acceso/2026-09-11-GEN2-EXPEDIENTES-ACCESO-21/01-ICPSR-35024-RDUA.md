# Expediente 01 · ICPSR 35024 / `35024-0001-Data.dta`

Estado: **LISTO-PARA-TITULAR; NO ENVIADO; ACCESO NO CONCEDIDO**. Canal y
requisitos comprobados el 11 de septiembre de 2026.

## Canal vigente e identidad del objeto

- Estudio oficial: [Mexico Panel Study, 2012 — ICPSR 35024](https://www.icpsr.umich.edu/web/RCMD/studies/35024).
- Ruta: iniciar sesión y abrir `Data & Documentation`. La pantalla autenticada
  debe resolver primero si el DS0001 pedido es descarga pública financiada por
  miembros o si la versión necesaria se ofrece bajo **Access Restricted Data**.
  Para esta última, el formulario se tramita en el sistema en línea de ICPSR;
  no se adjunta un acuerdo antiguo guardado localmente.
- Archivo pedido: **DS0001 completo en Stata,
  `35024-0001-Data.dta`**, esperado `1 555` registros × `374` variables, MD5
  `3f717dfcd8f3ba136c5d5ac0f571990c` según el manifiesto ya adquirido.
- Ayuda legítima si la elegibilidad no está confirmada:
  `restricteddata@icpsr.umich.edu`. Tener Researcher Passport/MyData y haber
  aceptado términos para documentación no equivale a acceso restringido.

La página del estudio declara versiones pública y restringida y que los datos
financiados por membresía son gratuitos para instituciones miembro. A la vez,
el manifiesto local rotula `35024-0001-Data.dta` bajo `DS0001 Public Use Data
(Spanish Language)`. La página pública actual no expone la correspondencia de
archivos de la versión restringida. Por tanto, **no se afirma que el RDUA sea la
puerta de DS0001**: el titular debe leer la etiqueta de acceso del archivo en la
pantalla autenticada. Si es `member-funded public`, la vía correcta es acceso
por institución miembro o consulta de no-miembro; si la versión necesaria se
rotula `restricted`, se usa el dossier RDUA siguiente.

ICPSR confirma que el acceso restringido requiere solicitud; para descarga segura suele exigir
PI con grado terminal y afiliación de investigación, personal de la misma
institución, descripción, plan de seguridad, RDUA firmado por investigador y
representante legal institucional, y aprobación o exención IRB. Estudiantes
normalmente necesitan patrocinador académico como PI. No se afirma que Jonás o
su institución satisfagan esos requisitos.

## Texto técnico para `Research description`

**Project title**

> Electoral monitoring, programme conditionality and vote autonomy in Mexico's
> 2012 panel election study

**Research question and purpose**

> This non-commercial research examines whether perceived ballot secrecy and
> exposure to electoral inducements or conditioned public benefits are
> associated with turnout and vote choice in Mexico's 2012 election panel. It
> also compares direct self-reports of vote-buying offers with the study's list
> experiments to assess under-reporting and construct differences. The purpose
> is to evaluate mechanisms linking monitoring, programme exposure and voter
> autonomy; all estimates will be reported as associational unless the original
> randomized list-experiment assignment supports the narrower experimental
> contrast.

**Why this exact file is required**

> We request access to the complete DS0001 Stata file
> `35024-0001-Data.dta`, or to the corresponding restricted version only if
> ICPSR confirms that it is the version required to provide those complete
> respondent-level fields. The material
> already available to us consists of questionnaires, codebooks, unweighted
> online crosstabs and a partial public replication subset. Those alternatives
> do not contain the full respondent-level joint distributions, the complete
> 374-variable panel, study population weights, item nonresponse patterns and
> panel indicators required to estimate weighted multivariable relationships
> and reproduce the list-versus-direct comparison. Published crosstabs cannot
> be recombined into individual records and therefore cannot answer this
> research question.

**Variables and analytic use**

> The minimum variables are the wave-one list experiment `P35A/P35B`, the
> wave-two list experiment `W2_P35A/W2_P35B`, perceived ballot secrecy
> `P36C/W2_P36C`, public-programme receipt/exposure variables including
> `P38A/P38B/P38C` and `W2_P39A/W2_P39B/W2_P39C`, programme conditionality
> `P39/W2_P40`, direct offer of a favour, gift or service for a vote
> `P40/W2_P41`, turnout and vote choice including `P7/P8`, `W2_P7/W2_P8`,
> `VOTOPRESW1/VOTOPRESW2` and `VOTODIPW1/VOTODIPW2`, plus the study-supplied
> population weight(s), panel/response indicators and non-identifying design and
> demographic controls released in DS0001. We will first verify names, labels,
> universes and coding against the delivered codebook; a listed variable will
> not be treated as present or comparable until that verification succeeds.

**Methods and outputs**

> Analyses will include weighted distributions, missingness and panel attrition
> checks; the pre-specified difference in list counts between treatment and
> control forms by wave; and weighted regressions or stratified contrasts of
> turnout and vote choice by programme exposure, reported conditionality,
> direct offers and ballot-secrecy perception. Small cells and unstable models
> will be reported as such. Outputs are aggregate tables, coefficients,
> uncertainty intervals and a technical methods appendix. No respondent-level
> row, small identifying cell or restricted geography will be published or
> redistributed.

The internal labels N26/N27 and R7.3/R7.6 are tracking destinations, not claims
to ICPSR. N27 or R7.6 advances only if the full file actually contains the
needed variables and universe; obtaining DS0001 does not prejudge that check.

## Custodia si la ruta aplicable es restringida

In the current ICPSR process, the applicant chooses and truthfully documents one
permitted security configuration for the relevant dissemination method. For
secure download, ICPSR lists an external drive, a non-networked computer, or a
local isolated virtual/physical enclave. The private application must identify
the real device/location and every authorised person; backups and transfers
must follow the selected plan. Access logs, updates, renewal and a destruction
affidavit may be required. This dossier does **not** select a device, assert an
access site or invent a destruction date.

## Dato del titular

| dato faltante del titular | por qué se exige | dónde se escribe |
|---|---|---|
| PI real, grado y afiliación; o patrocinador académico si aplica | elegibilidad de acceso restringido | Investigator information de IDARS |
| contacto y afiliación de cada persona con acceso | el acuerdo limita quién puede usar los datos | Research staff information |
| aprobación o exención IRB auténtica | requisito de la solicitud | documento privado adjunto |
| plan y equipo/ubicación de seguridad reales | custodia y control de acceso | Confidential Data Security Plan |
| representante legal institucional | el RDUA es entre Michigan y la institución | firma institucional del RDUA vigente |
| firmas y fechas verdaderas | aceptación contractual | RDUA generado por el sistema |

Si DS0001 aparece como `member-funded public`, estos campos RDUA no se inventan:
se usa acceso de institución miembro o se pregunta a ICPSR por acceso de
no-miembro. Si la versión aplicable es restringida y falta PI/institución/IRB,
no declarar elegibilidad. La alternativa legítima es consultar a ICPSR sobre el
caso real, conseguir un patrocinador/institución que asuma el acuerdo, o
continuar con documentación/tabulados públicos rotulados de segunda mano; no
usar la identidad de otra persona ni tratar el archivo parcial como el DTA
completo.

## Adjuntos, presentación y recepción

Si aplica RDUA, adjuntar exclusivamente lo que muestre la solicitud vigente:
acuerdo generado por IDARS, IRB/exención y documentos de personal/seguridad
requeridos. Pegar el texto técnico anterior en `Research description`; no
adjuntar datos locales. Si la pantalla clasifica DS0001 como público para
miembros, conservar captura/acuse de esa clasificación y no presentar un RDUA
para un objeto distinto.

Registrar el acuse privado y el identificador de acuerdo. Si se aprueba y llega
un archivo, mantenerlo fuera de Git, verificar nombre, MD5, SHA-256, `1 555 ×
374`, etiquetas y presencia de pesos. Una descarga de sólo PDF/TXT/HTML queda
`DOCUMENTACION`, no `OBTENIDO`. El receptor técnico prepara una spec sucesora
antes de analizar el DTA y conserva las restricciones de acceso en todo
producto.
