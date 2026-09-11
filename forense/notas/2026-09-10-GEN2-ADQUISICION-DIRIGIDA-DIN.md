# GEN2-ADQUISICION-DIRIGIDA-Y-DIN · diseño de DIN-M-01

Fecha de comprobación: 10 de septiembre de 2026. Objeto: aplicación del
benchmark D16 a `CALC-R-DIN-M-01-v4`, sin modificar ni reemplazar ese cálculo
congelado.

## Resultado

No existe en el corpus ni en la publicación oficial una UPM, un estrato de
selección o pesos replicados que permitan construir hoy un diseño ejecutable y
acreditado para DIN-M-01. La documentación oficial sí acredita que ENNViH-1 fue
una muestra probabilística, polietápica, estratificada y por conglomerados, y
prescribe estimación de varianza por conglomerados últimos y series de Taylor.
La FAQ del productor confirma además que la UPM no es pública por
confidencialidad. Por ello no se crea `CALC-R-DIN-M-01-v5`.

El punto ponderado vigente, `0.15558094338412926`, queda disponible como
descriptivo. El EE `0.004821494748362768` y el IC95
`[0.1461309873234716, 0.1650308994447869]` de v4 son una sensibilidad bajo
estrato constante + `folio`; el EE SRS heredado `0.0040186269` es otra
sensibilidad. Ninguna tiene orden conocido respecto del EE del diseño real y
ninguna se denomina conservadora o cota inferior.

## Identidad, universo y enlace verificados

- `iiib_cr.dta`: 19 802 filas; llave `folio+ls` única. `cr27` contiene 2 665
  códigos `1`, 17 074 códigos `3`, 60 códigos `7` y 3 nulos. El manual rotula
  esos 60 casos como código `8`; la discrepancia no cambia el estimando porque
  la spec excluye ambos códigos.
- `ehh02w_b3b.dta`: 35 677 filas; llave `folio+ls` única; `fac_3b` está
  etiquetado `FACTOR DE EXPANSIÓN LIBRO 3B`.
- El enlace normalizando `folio` y usando `folio+ls` es 1:1: 19 802 de 19 802
  filas, cero huérfanos y cero pesos no positivos. Enlazar sólo por `folio`
  produciría 96 638 pares y expandiría accidentalmente la tabla.
- El universo efectivo es `n=19 739` y la masa ponderada `68 002 840`, iguales
  a v4. La guía oficial confirma que los libros individuales se unen a su
  ponderador mediante `folio+ls`; `ls` identifica persona.
- `c_portad.estrato` clasifica tamaño de localidad, no el estrato de selección.
  `id_loc` tiene 150 comunidades, mientras el diseño documenta 180 UPM; tampoco
  es una UPM sustituta. `iiib_portad.ent` aporta entidad pero no estrato de
  diseño.
- Los once archivos públicos de ponderadores contienen `fac_*` y cero pesos
  replicados.

Fuentes ya registradas y verificadas: `ennvih1_muestra_diseno`, sha256
`9f90df10338c7749cf46f86edc0664fc300c913e4fc4b1eee5e360d2970e91f0`, y
`ennvih3_2009_factores_exp`, sha256
`cc297561caa5e963fd5a7cd88a8ab0a45726b997015eafbcdac7bcf088fe214d`.
Referencias oficiales: `https://www.ennvih-mxfls.org/assets/ennvih-1_muestra.pdf`,
`https://www.ennvih-mxfls.org/ponderadores1.html` y
`https://ennvih-mxfls.org/faq.html`.

## Recomendación concreta para FP-371

Rechazar el uso de estrato constante + `folio` como *ground truth* inferencial
de TRIADA. Conservar el punto descriptivo y, si se muestran intervalos antes de
obtener una vía oficial, etiquetar separadamente SRS y constante+folio como
sensibilidades sin dirección garantizada. FP-371 permanece `ABIERTA`: esta nota
formula el uso concreto que mesa debe aceptar o rechazar, no sustituye su firma.

## Solicitud preparada, no enviada

Destinatario oficial: `support@ennvih-mxfls.org` (página de contacto en inglés).
La FAQ en español también publica `ennvih.soporte@ennvih-mxfls.org`; se usa el
primero como ruta primaria y el segundo sólo como alternativa si rebota.

Texto propuesto:

> Estimado equipo ENNViH: para estimar la varianza de una proporción ponderada
> de ENNViH-1 (2002), Libro 3B, con `fac_3b`, solicitamos una vía compatible con
> la confidencialidad: (a) pesos replicados oficiales y su método, `scale`,
> `rscales`, convención MSE y grados de libertad; o (b) un servicio/tabulado que
> devuelva el EE de la estimación bajo el diseño. Entendemos por su FAQ que la
> UPM no es pública y no solicitamos geografía identificable. Agradeceríamos
> también la regla para UPM únicas y cualquier FPC aplicable.

No se registró envío ni acceso concedido. Responsable de la siguiente acción:
titular de mesa, quien aporta identidad y decide enviar. Si llega una respuesta
operativa, el sucesor congela `CALC-R-DIN-M-01-v5` antes del primer resultado,
verifica cobertura y unidades por estrato, reproduce el punto y coteja el EE con
una implementación de referencia del mismo diseño.
