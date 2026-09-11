# GEN2-EXPEDIENTES-ACCESO-21 · cierre técnico

Fecha: 11 de septiembre de 2026. Base efectiva:
`a37837a0df69240e35c160a53c5c1de209f9be01` (`origin/main`, incorpora #709).
El corte del encargo quedó superado sólo por la integración de la cola post-707;
no apareció un envío ni una respuesta posterior de los objetos de este acto.

## Resultado

Se terminó la parte técnica de ICPSR 35024, OECD Trust PUM, una sola solicitud
ENNViH para DIN+S6, ENCIG/NC-0153 y ENJUVE 2000/2005/2010. Reuters DNR queda
diferido por demanda no definida después de cruzar el cuestionario con los
consumidores actuales. Todo vive en el índice
`forense/expedientes-acceso/2026-09-11-GEN2-EXPEDIENTES-ACCESO-21/INDICE-EXPEDIENTES-ACCESO-21.md`.

| expediente | estado al cierre | producto |
|---|---|---|
| ICPSR 35024 | listo para que el titular confirme la puerta exacta y, si aplica, tramite RDUA; no enviado | descripción de investigación, variables, alternativas insuficientes, requisitos de elegibilidad/custodia y recepción |
| OECD Trust PUM | formulario técnico completo; no firmado ni enviado | DOCX vigente derivado, correo final, faltantes personales mínimos y recepción |
| ENNViH DIN + S6 | borrador final; no enviado | cuatro estimandos ejecutables, dos vías confidenciales de respuesta y contrato de varianza requerido |
| ENCIG / NC-0153 | borrador final; no enviado | llave 8.5↔`NT_TIPO/P7_3`, microdato evento con negativos o tabulado nacional como salidas equivalentes delimitadas |
| ENJUVE | borrador PNT final; no enviado | pedido separado por ola, formatos históricos, documentación/diseño/pesos y tratamiento de ola no reconocida |
| Reuters DNR | diferido por demanda no definida | cruce negativo de consumidores, candidato mínimo y criterio de reapertura |

## Comprobaciones públicas acotadas

- ICPSR mantiene el estudio 35024, declara versiones pública y restringida y
  remite el acceso restringido al botón de la página. Su guía vigente exige para
  descarga segura descripción, plan de seguridad, RDUA institucional e
  IRB/exención, con requisitos reales de PI/personal. El manifiesto local pone
  `35024-0001-Data.dta` bajo `DS0001 Public Use Data (Spanish Language)`, mientras
  la página pública no expone qué archivo pertenece a la versión restringida.
  Por eso el dossier obliga a comprobar la etiqueta autenticada: membresía para
  DS0001 público o RDUA para la versión restringida que ICPSR identifique.
- OECD publica el formulario general/estudiante, elegibilidad no comercial y
  envío a `govtrustinfo@oecd.org`; evalúa necesidad de microdato frente a
  StatLinks. El original registrado y el formulario oficial descargado hoy son
  idénticos: SHA-256
  `4a3ac6d704caa67e1a4dfc702b5a38747a56eb48e086d3aae4c14814601af915`.
- ENNViH publica `support@ennvih-mxfls.org`; su FAQ confirma que UPM/localidad
  no se hacen públicas por confidencialidad. Se pidió réplica no geográfica o
  servicio, no identificación territorial.
- INEGI mantiene ENCIG 2025, el formulario de información estadística y el
  esquema nacional para personas de 18 años o más en ciudades de 100 mil y más.
- IMJUVE mantiene su Unidad de Transparencia y enlaza la Plataforma Nacional de
  Transparencia como canal para solicitudes.

No se hizo otra búsqueda general sobre NC-0153. El encargo hermano 20 sólo había
archivado su instrucción al corte y no entregó ficha ENCRIGE; no se redactó una
solicitud rival.

## DOCX y reproducibilidad

`tools/prepara_oecd_pum_docx.py` valida el hash del original, conserva los
miembros/metadatos ZIP y añade texto únicamente a párrafos técnicos vacíos. El
resultado pasa `ZipFile.testzip()` y conserva `Expected completion date`,
`Name`, `Affiliation`, `Country`, `Signature` y `Date`. SHA-256 del derivado:
`6b342e948cb086ee4e31a06ac009fb71fd0f1a7b623385508afd3c1697371fe0`.

## Seguimiento canónico

`tools/actualiza_expedientes_acceso_21.py` modificó sólo:

- `NC-0151`, `NC-0153`, `NC-0156`;
- `FP-314`, `FP-371`, `FP-372`, sin cerrar ni firmar ninguna;
- seis filas de adquisición: `MEXICO_PANEL_STUDY_2012`, `OECD`,
  `ENNVIH_DIN_M_01_DISENO_INFERENCIAL`,
  `TASA_GENERAL_SOLICITUD_PAGO_INFORMAL_POR_CANAL_TRAMITES_MEXICO`, `ENJUVE` y
  `REUTERS_DNR`.

La vista `data/cola-adquisicion-v1_0.tsv` se regeneró desde el registro canónico.
Los estados se conservaron: listo no significa enviado, concedido ni obtenido.
El registro de recepción diferencia esas etapas y mantiene cualquier archivo
restringido fuera de Git.

## Límites

Cero llamadas a modelos, cero mensajes externos y cero microdatos adquiridos.
No se tocó motor, CALC, cron ni evaluación. El binario SSRN 2014 no se persiguió
y no se abrió vía comercial de tandas. Las reservas ejecutivas quedan en el
encargo archivado y en las tres NC vigentes.
