# GEN2 · expedientes de acceso listos para el titular

Fecha de comprobación de canales: **11 de septiembre de 2026**. Estado del
paquete: **LISTO-PARA-TITULAR; cero envíos, cero accesos concedidos y cero
archivos obtenidos por este acto**.

Este directorio termina las partes técnicas de cinco solicitudes ya existentes.
No sustituye identidad, firma, declaraciones institucionales ni aceptación de
términos. La copia privada que el titular firme o envíe, los acuses con datos
personales y cualquier dato restringido permanecen fuera de Git.

| expediente | artefacto listo | dato o acto mínimo del titular | qué desbloquea si la respuesta es útil |
|---|---|---|---|
| ICPSR 35024 | [`01-ICPSR-35024-RDUA.md`](01-ICPSR-35024-RDUA.md) | confirmar en la pantalla autenticada si DS0001 es acceso público financiado por miembros o si la versión necesaria es restringida; para esta última, PI/institución, IRB, plan real y firmas | `35024-0001-Data.dta`; análisis individual ponderado de N26/N27 y R7.3/R7.6 sólo dentro del alcance que el archivo confirme |
| OECD Trust PUM | [`02-OECD-TRUST-PUM.md`](02-OECD-TRUST-PUM.md) + [`02-OECD-TRUST-PUM-TECHNICAL-DRAFT.docx`](02-OECD-TRUST-PUM-TECHNICAL-DRAFT.docx) | completar fuera de Git nombre, afiliación, país, fecha esperada, firma y fecha; enviar | N30 mediante distribuciones conjuntas; no sustituye automáticamente WVS7/R8.3 |
| ENNViH DIN + S6 | [`03-ENNVIH-DIN-S6.md`](03-ENNVIH-DIN-S6.md) | identidad/correo real y envío | varianza oficial de DIN y C1/C3/C4 de S6; no cambia puntos ni firma FP-371/372 |
| ENCIG / NC-0153 | [`04-INEGI-ENCIG-NC-0153.md`](04-INEGI-ENCIG-NC-0153.md) | datos mínimos del formulario y envío | tasa nacional evento × canal con negativos y diseño, si INEGI entrega enlace, microdato o tabulado válido |
| ENJUVE 2000/2005/2010 | [`05-IMJUVE-ENJUVE.md`](05-IMJUVE-ENJUVE.md) | cuenta/medio de notificación de PNT y presentación | microdatos y documentación por ola reconocida |
| Reuters DNR individual | [`06-REUTERS-DNR-DIFERIDO.md`](06-REUTERS-DNR-DIFERIDO.md) | primero fijar consumidor/reactivo/año; hoy no enviar | nada vigente; alcance mínimo propuesto para una eventual reapertura |

## Secuencia del titular

1. Abrir el expediente elegido y completar **únicamente** su tabla «Dato del
   titular». No llenar un dato supuesto para hacer pasar elegibilidad.
2. Guardar fuera de Git una copia privada del formulario o correo definitivo.
   Para OECD, partir del DOCX técnico de este directorio; para ICPSR, copiar la
   descripción en el formulario vigente que abre el botón `Access Restricted
   Data` del estudio.
3. Presentar por el canal comprobado en cada expediente. No combinar solicitudes
   de productores distintos.
4. Registrar en `REGISTRO-RECEPCION.tsv` sólo metadatos no personales. Un folio
   puede abreviarse si revelara identidad; el comprobante íntegro queda privado.
5. Clasificar el avance sin saltos: `LISTO-PARA-TITULAR` → `ENVIADO` →
   `CONCEDIDO` → `OBTENIDO-Y-VERIFICADO`. Una respuesta negativa queda
   `NEGADO-O-NO-ELEGIBLE`, no `NO-ENCONTRADO`.

## Criterio común de recepción

- **Acuse:** productor, expediente, canal, fecha/hora, folio o Message-ID y ruta
  privada del comprobante.
- **Respuesta:** fecha, alcance exacto, condiciones y vencimientos; separar lo
  entregado de lo negado o no reconocido.
- **Archivo:** conservar fuera de Git; registrar nombre, tamaño, SHA-256, formato,
  dimensiones y diccionario. En ICPSR se cotejan además `1 555 × 374` y el MD5
  esperado; una carpeta de documentación no cuenta como DTA.
- **Diseño o servicio:** documentar método, pesos, escalas, grados de libertad,
  UPM únicas/FPC, universo y versión del instrumento. Un número sin contrato de
  diseño no levanta NC-0156.
- **Continuidad:** quien reciba verifica primero identidad, cobertura, códigos,
  ponderadores y restricciones; después congela la spec sucesora correspondiente.
  No se calcula primero para decidir luego qué respuesta aceptar.

## Insumos que no se persiguen en este paquete

El binario SSRN de 2014 no se solicita: existe la versión de autor de 2012 y
ninguna de las dos resuelve por sí sola el comparador pendiente. D18 mantiene
diferidas las fuentes comerciales de tandas. La eventual ficha ENCRIGE del
encargo 20 no había llegado al corte; no se creó una solicitud rival.
