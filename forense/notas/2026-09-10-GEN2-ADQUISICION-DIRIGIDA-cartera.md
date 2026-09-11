# GEN2-ADQUISICION-DIRIGIDA-Y-DIN · cartera por objeto

Fecha de comprobación: 10 de septiembre de 2026. Universo: `NC-0151`,
`FP-286/314/343`, las demandas vigentes de los lotes GEN2 y las 139 filas del
registro canónico de adquisición. Se verificaron físicamente los payloads
citados; un borrador, una cuenta o un acceso no se registran como envío,
recepción o adopción.

## Resultado ejecutivo

La receta FP-314 mezclaba objetos ya obtenidos con accesos personales. WBES
México 2023 ya está adquirido, ENAFIN ya satisface el cruce N19 con tabulados
públicos y las ocho olas ENVIPE que `ENCARGO-E08` necesita están presentes. No se vuelven
a descargar. La única adquisición pública nueva de este acto es una versión de
autor de 2012 del estudio de Bauchet; cubre el contenido académico asociado a
SSRN 2474620, pero no se finge que sea el artefacto SSRN 2014. ICPSR, OECD,
Reuters y ENJUVE quedan como acciones personales/institucionales concretas.

## Matriz de utilidad e identidad

| objeto | pregunta / consumidor | identificador y ola | ya disponible | barrera / siguiente acción |
|---|---|---|---|---|
| WBES México 2023 | rechazo de crédito por segmento, N19 | `WORLD_BANK_ENTERPRISE_SURVEY_MEXICO_2023`; `wbes_mexico_2023_microdato_dta_zip` | microdato 1 322 × 357, panel 2010–2023, DDI y documentos; hash y tamaño coinciden | no hay barrera de adquisición. `k20a1` identifica rechazo y el diseño permite segmentar, pero no hay motivo institucional “sin historial”; retirar la receta de descarga, conservar `EXISTE-SATISFACE-PARCIAL` |
| ENAFIN 2024 | historial crediticio por segmento, N19 | `adq15_enafin_conjunto_de_datos_enafin_2024_csv`; bloques `K_51/X_51/AK_51`, 43/44 | `EXISTE-SATISFACE`: once dominios (total, tamaño, sector y localidad), bytes verificados | el microdato individual requiere Laboratorio de Microdatos INEGI, pero no bloquea N19; no tramitarlo sin un nuevo consumidor exacto |
| Global Findex 2025 | control paralelo de N19 | `gen2_universo_c_findex2025_csv`, 438 columnas | archivo país público y glosario | `EXISTE-NO-SATISFACE`: no contiene razón de rechazo ni historial; el microdato con cuenta no se persigue sin demanda nueva |
| F5 | cobertura documental de las 14 celdas del lote 01 | paquete F5 v2.0 y `CALC-TRIADA-0002` | la actualización con `origin/main` incorporó PR #687: corpus determinista 14/14 y captura completa | cerrado por ensamblado/ejecución del lote 01, no por una adquisición de `ENCARGO-E09`; no abrir una descarga adicional |
| corrupción general | D08 / NC-0153 | ENCUCI 2020 `AP5_17/AP5_18`, `CALC-ENCUCI-0001`; UNAM-IIJ 2015 `p4_1..p4_4` | ENCUCI separa solicitud/entrega/unión entre personas con contacto; UNAM aporta cuatro tasas generales por trámite, pero ninguna fuente cruza el evento con su canal | demanda exacta ya inscrita como `TASA_GENERAL_SOLICITUD_PAGO_INFORMAL_POR_CANAL_TRAMITES_MEXICO`, fila canónica `PENDIENTE` y seleccionable por SONDA; ENCIG `B-COVERAGE=0.200895` sigue condicionado y no se extrapola |
| ENVIPE serie | `ENCARGO-E08` / `NC-0087/0093/0101` | ocho olas pendientes, 2011/2014/2016–2020/2022 | todos los payloads están presentes y coinciden con manifiesto | falta medición y comparabilidad, no adquisición; `ENCARGO-E08` produce specs y serie |
| OECD Trust PUM | N30; R8.3 ya tiene WVS7 | formulario `tc_oecd_trust_survey_pum_2021_2023_2025` | indicadores públicos sí; PUM no. El DOCX de términos está sin datos del solicitante ni firma | titular completa identidad, afiliación, proyecto, productos y fecha, firma y envía a `govtrustinfo@oecd.org`; no se registró envío |
| ICPSR 35024 | N26/N27; R7.3/R7.6/list experiment | `35024-0001-Data.dta`, esperado 1 555 × 374, MD5 `3f717dfcd8f3ba136c5d5ac0f571990c` | documentación, tabulados y subconjunto Harvard; no el DTA completo | requiere Restricted Data Use Agreement; la cuenta y términos de descarga documental no bastan. Titular somete DUA y, si se concede, verifica MD5/dimensiones y registra fuera de Git |
| Reuters DNR individual | cartera FP-314; falta fijar consumidor | microdato respondent-level México, año/reactivo aún no fijado | informe, cuestionario y tablas topline 2025 | antes de enviar, fijar año, reactivo y uso; luego pedir datos individuales para investigación no comercial a Reuters Institute |
| ENJUVE | cartera exploratoria FP-314 | microdatos 2000/2005/2010 | cuestionario/presentación 2010 y cuatro tabulados 2005; no microdatos | hosts históricos muertos y Wayback no archivó binarios. Titular presenta solicitud PNT a IMJUVE, enumerando olas y formatos; INMUJERES queda como segunda vía |
| Bauchet / SSRN 2474620 | N21/R1.4, comparador de marca | SSRN `abstract_id=2474620` | hermanas 2589578/2689238 y, desde este acto, versión de autor 2012 del mismo estudio | SSRN sigue detrás de sesión/Cloudflare y la versión 2012 no es el binario 2014. Ninguna versión trae el comparador de marca que cerraría R1.4; no bloquea el modelo |
| tandas comerciales | R8.2/N29 | `REGISTRO_DE_TANDAS_Y_REPUTACION` y `REGISTRO_OPERATIVO_DE_TANDAS_DIGITALES` | sólo prosa y solicitud preparada | D18 difiere la vía comercial hasta propuesta concreta; no enviar ni negociar en este acto. La ruta académica se documenta en informe separado |

## Recibo de adquisición pública

| campo | valor |
|---|---|
| objeto | versión de autor 2012 de *Price and Information in Life Microinsurance Demand: Experimental Evidence from Mexico*, Jonathan Bauchet |
| origen | `https://www.dartmouth.edu/neudc2012/docs/paper_208.pdf` |
| fecha | 2026-09-10 |
| hash / tamaño | sha256 `4d252d1938f42b30e34947de3737fae8e4d84099768c54d6056c75188869b8d5`; 1 335 782 bytes; 47 páginas |
| ruta configurada | `data_raw:milk_rct_microseguro/Bauchet-Price-and-Information-Life-Microinsurance-Mexico-author-version-2012.pdf` |
| legibilidad | PDF 1.5, no cifrado; portada/autor/contenido abiertos; dos descargas (`curl`/`wget`) idénticas |
| condición | PDF público alojado por Dartmouth/NEUDC; copyright y redistribución no determinados, payload fuera de Git y uso de investigación |
| manifiesto | `bauchet_price_information_mexico_author_version_2012_pdf` |
| responsable siguiente | nadie para uso bibliográfico; titular sólo si necesita además el binario SSRN 2014. No cierra R1.4 |

## Cierre por objeto

`FP-286/FP-343` ya no tienen una pregunta de clasificación: ENAFIN está
resuelta para N19 y las dos tandas comerciales quedaron diferidas por D18. Sus
residuales sustantivos sobreviven en `NC-0151` (accesos) y `NC-0037`
(ausencia de ledger público de tandas), no en una repetición de las 28 filas. `FP-314`
queda parcialmente ejecutada. `NC-0151` permanece abierta por ICPSR, OECD,
Reuters, ENJUVE y el artefacto SSRN exacto; WBES y ENVIPE salen de su lista de
adquisición.
