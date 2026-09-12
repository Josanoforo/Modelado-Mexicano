# GEN2-38 · continuación CAJA de investigación NC-0122 / NC-0126

Fecha de exploración: 2026-09-11. Entorno: CAJA (Ubuntu/WSL2), con
`data/raw -> /home/pc0/mm-corpus/raw` y red real confirmada contra
`https://www.inegi.org.mx/` (HTTP 200). Mandato: GEN2-38. Este documento
registra descubrimiento y fronteras; no adopta científicamente una fuente.

## NC-0122 · producto fintech exacto y canal del mismo producto

Versión: `2026-09-10-producto-fintech-exacto-v1`.

Definición: «medir el canal de alta DEL PRODUCTO FINTECH en sí, no del último
producto contratado».

Estado de entrada: ENIF 2021/2024 identifica tenencia fintech y canal del
último producto, sin identidad producto↔canal y sin «referido» como categoría.
La exploración previa ya cubría ENIF, cuatro sondeos regulatorios/locales,
openICPSR 202904 y una declaración agregada de Baubap.

Modos ejecutados: CONSTRUCTO y HERMANAS.

Consultas web reales:

- Buscador web: `Mexico fintech survey exact lender product acquisition channel referral questionnaire dataset`.
  Recuperó ENIF 2024, ENAFIN y `COFINFAD`; ENIF es universo ya examinado,
  ENAFIN observa empresas y COFINFAD observa clientes de una fintech colombiana.
- Buscador web: `site:dataverse.harvard.edu Mexico fintech consumer survey lender referral channel`.
  No produjo un paquete mexicano pertinente en los resultados examinados.
- Buscador web: `site:openicpsr.org Mexico fintech borrower survey acquisition channel`.
  No añadió un paquete pertinente distinto del openICPSR 202904 ya descartado
  por unidad.
- Buscador web: `México encuesta usuarios fintech canal de contratación referido producto prestamista microdatos`.
  Predominaron ENIF y materiales divulgativos/comerciales sin microdato
  persona-producto con diseño.
- Control local: `python3 tools/busca_reactivos.py --palabra fintech --limite 20`
  examinó 241,591 filas (178,246 v1_2 + 63,345 ext) y arrojó 0 candidatas.
- Control local: `python3 tools/busca_reactivos.py --palabra referido --limite 20`
  arrojó dos reactivos de elección de centro en EHH 2002/2005, incompatibles
  con producto financiero.

Candidata examinada: `COFINFAD_COLOMBIA_FINTECH_2023`,
https://pmc.ncbi.nlm.nih.gov/articles/PMC12950484/ . El artículo y su depósito
público describen 48,723 clientes de una única fintech colombiana, una fila por
cliente, y la variable `acquisition_channel` con valores como organic/referral,
además de indicadores de productos. Es evidencia de que el enlace técnico
existe en datos operativos, pero no acredita población mexicana ni una muestra
de adultos de México; tampoco identifica varios lenders/productos comparables.
Clasificación: EXISTE-NO-SATISFACE. No se crea residual ni se descarga.

Resultado: `sin_hallazgo_acotado`. Suficiencia permanece: identidad PARCIAL,
concepto PARCIAL, población ACREDITADA para el proxy ENIF, selección/no
respuesta ACREDITADA, unidad PARCIAL, temporalidad ACREDITADA, diseño
ACREDITADA, identificación NO_APLICA; uso habilitado APTA_ALCANCE_MENOR y
pregunta ABIERTA.

Frontera no examinada: instrumentos internos no publicados de lenders,
login/compra/contacto, tesis y repositorios no indexados, y depósitos nuevos
que no afloraron con estas consultas. Cursor: buscar paquetes mexicanos de
datos operativos o encuestas de una fintech identificable que publiquen a la
vez lender/producto y adquisición/referral; no repetir ENIF, openICPSR 202904
ni COFINFAD Colombia. Próxima revisión: 2026-10-11.

## NC-0126 · tenencia separada de horizonte de ahorro

Versión: `2026-09-09-horizonte-ahorro-descolapsado-v1`.

Definición: «P4_10 = 1 es una categoría colapsada y el descriptor no permite
descolapsarla».

Estado de entrada: ENIF P4_10 mezcla menos de una semana y ausencia de ahorros.
La exploración previa verificó Banxico EACF 2024 y ENSAFI 2023: la primera no
ofrece «no tiene ahorros» separado en SF12 y la segunda mide tenencia y monto,
no duración.

Modos ejecutados: CONSTRUCTO y HERMANAS.

Consultas web reales:

- Buscador web: `Mexico survey savings duration how long savings would last separate no savings questionnaire microdata`.
  Recuperó ENFIH 2019, Findex 2025, ENIF y ENSAFI; ninguna ficha mostró la
  secuencia exacta tenencia→duración entre quienes sí ahorran.
- Buscador web: `México encuesta cuánto tiempo durarían sus ahorros no tiene ahorros cuestionario`.
  Recuperó el mismo reactivo colapsado de ENIF y materiales Banxico ya
  examinados.
- Buscador web: `site:inegi.org.mx encuesta ahorro "menos de una semana" "no tiene ahorros"`.
  Confirmó ENIF y ENSAFI; no apareció otra operación con el objeto exacto.
- Buscador web: `site:banxico.org.mx encuesta ahorro duración ahorros SF12 microdatos`.
  Confirmó EACF: SF12 usa seis categorías (cinco duraciones y no sabe), sin
  categoría separada de ausencia de ahorro.
- Control local: `python3 tools/busca_reactivos.py --palabra ahorros --limite 30`
  examinó 241,591 filas; los primeros 30 resultados contienen tenencia/monto
  y usos de ahorro, no duración condicionada a tenencia.

Candidata examinada: `GLOBAL_FINDEX_2025_MEXICO_FIN17D`,
https://microdata.worldbank.org/catalog/7945/variable/F1/V65?name=fin17d . La
ficha pública acredita 1,050 casos México 2024 y `fin17d`, frecuencia de ahorro
formal (semanal/mensual/menos de mensual) con 161 respuestas válidas y 889
faltantes estructurales. El corpus ya contiene el CSV México 2025 como
`gen2_universo_c_findex2025_csv`. Mide frecuencia, no cuántos días/meses
cubrirían los ahorros; es evidencia existente e incompatible con el concepto.

Resultado: `evidencia_existente`, sin candidata pública nueva adquirible.
Suficiencia permanece: identidad ACREDITADA, concepto NO_ACREDITADA, población
ACREDITADA, selección/no respuesta ACREDITADA, unidad ACREDITADA, temporalidad
ACREDITADA, diseño ACREDITADA, identificación NO_APLICA; uso INCOMPATIBLE y
pregunta ABIERTA.

Frontera no examinada: cuestionarios subnacionales, módulos privados, otras
ediciones no indexadas y variables internas de ENFIH no anunciadas como
duración. Cursor: buscar un instrumento público de adultos en México que mida
tenencia de ahorro y, sólo entre quienes sí ahorran, duración de cobertura;
no repetir ENIF, EACF, ENSAFI ni Findex 2025. Próxima revisión: 2026-10-11.

## Segunda pasada crítica

Se examinó el objeto exacto, no sólo ahorro o adopción fintech en general. Los
HTTP 200 y las fichas se contrastaron con población, unidad, variable y corpus.
COFINFAD se descarta por Colombia/un prestador; Findex por frecuencia en vez de
duración y por estar ya en corpus. No se observó una vía pública pendiente que
justifique residual GEN2-38. Los negativos son acotados a las consultas y
repositorios declarados y conservan la frontera anterior ampliada.
