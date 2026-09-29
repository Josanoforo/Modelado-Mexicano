# Hoja de recetas de mesa · GEN2-PENDIENTES-4

Acciones con identidad real (correos, solicitudes, registros, un disco, una función de GitHub, un `.ots`): un ejecutor no las puede hacer. Están **deduplicadas por acción física** (varias NC pedían el mismo envío) y contrastadas contra R46–R49 y las seis solicitudes (a)–(f) de `GEN2-OBTENCION-EXTERNA-1`. Cada NC de esta hoja lleva `MESA-ACCION (<fecha>)` como dueño; la fecha es la que mesa ya fijó (R46, R47, R49 y R51 difieridas al 29/sep) o el corte semanal (5/oct). El acuse de cada solicitud entra por adenda del acto que la registra, no por un trámite aparte (A.12). Generada por `arma_hoja_recetas_pendientes_4.py`.

## A01 · Generar el sello externo (.ots) del manifiesto de sellos

**Cierra (5):** `NC-260926-GEN2-ASTRA6-C2-CIERRE-MATERIAL-1-ad01-02`, `NC-260926-GEN2-ASTRA6-C2-ENCIG-1-fde0-01`, `NC-260926-GEN2-ASTRA6-C2-ENVIPE-1-7045-01`, `NC-260926-GEN2-RECIBO-ASTRA6-N-996b-03`, `NC-260923-GEN2-TUBERIA-SELLO-EXTERNO-1-cfce-01`
**Fecha:** 2026-10-05 · **Deduplicada contra:** FP fde0-02 FIRMADA («mesa genera el .ots»)

**Receta de un minuto.**

- En máquina con red y clon con historia: (1) python3 tools/familias-2027/cierre-material-1/verifica_cierre_material.py --verifica --hoja --pruebas --evidencia; (2) python3 tools/sello_externo.py stamp --desde forense/sellos/manifiesto-sellos-2026-09-23.tsv --fecha <hoy> (escribe el manifiesto delta con los sellos nuevos de familias 2027); (3) pip install opentimestamps-client && ots stamp <manifiesto delta>; (4) commitear el .ots junto al manifiesto; horas después, ots upgrade + ots verify → «Success! Bitcoin block…».
- La misma receta que ad01-02: python3 tools/sello_externo.py stamp --desde forense/sellos/manifiesto-sellos-2026-09-23.tsv --fecha <hoy>; comprobar que el delta trae los COMMIT-1/2 de ENCIG listados en forense/analisis/familias-2027/astra6-encig/inventario-sellos.json; ots stamp <delta>; commitear el .ots; ots upgrade + ots verify.
- La misma receta que ad01-02. El delta de tools/sello_externo.py stamp debe traer los dos sello.json de CALC-FAMILIA-2027-ENVIPE-* (229a4f0b…, 4ba2cbcb…); ots stamp <delta>; commitear el .ots; ots upgrade + ots verify.
- Antes (sesión CAJA, lote RELEVO-TRAMITE-CAJA-2): `python3 tools/familias-2027/encig/cierre.py --verifica` sobre el commit de merge, añadir el hash de cierre.py/evaluar.py/enmienda-verificacion.json al inventario y escribir el manifiesto nuevo con `python3 tools/sello_externo.py manifiesto --escribe`. Luego mesa, en su máquina: `pip install opentimestamps-client`, `ots stamp forense/sellos/manifiesto-sellos-<fecha>.tsv`, sube el .ots junto al manifiesto y, horas después, confirma con `ots upgrade` y `ots verify` (docs/sello-externo.md:24-37).
- En un clon de main, desde una máquina con red abierta: pip install opentimestamps-client && ots stamp forense/sellos/manifiesto-sellos-2026-09-23.tsv ; openssl ts -query -data forense/sellos/manifiesto-sellos-2026-09-23.tsv -sha256 -cert -out forense/sellos/manifiesto-sellos-2026-09-23.tsv.tsq && curl -sS -H 'Content-Type: application/timestamp-query' --data-binary @forense/sellos/manifiesto-sellos-2026-09-23.tsv.tsq https://freetsa.org/tsr -o forense/sellos/manifiesto-sellos-2026-09-23.tsv.tsr ; commit de .ots/.tsq/.tsr en una rama y PR; verificación según docs/sello-externo.md (ots verify / openssl ts -verify).

**Destino / acuse.** forense/sellos/ (.ots junto al manifiesto delta; receta docs/sello-externo.md §Mecanismo (a)); estado ENVIADO-A-ATESTACIÓN hasta el comprobante · forense/sellos/ (.ots junto al manifiesto delta); inventario de origen: forense/analisis/familias-2027/astra6-encig/inventario-sellos.json · forense/sellos/ (.ots junto al manifiesto delta); inventario de origen: forense/analisis/familias-2027/astra6-envipe/inventario-atestacion.json · forense/sellos/manifiesto-sellos-<fecha>.tsv.ots (receta en docs/sello-externo.md; generador tools/sello_externo.py) · forense/sellos/ (PR que fusiona mesa) · hoja de recetas de GEN2-PENDIENTES-4

## A02 · Activar GitHub Pages desde main/docs y comprobar que sirve

**Cierra (3):** `NC-260926-GEN2-PRODUCTO-CONSULTA-1-dcde-01`, `NC-260923-GEN2-TRAMITE-FIRMAS-14-9556-05`, `NC-260924-GEN2-TUBERIA-TABLERO-EN-CANAL-1-3726-02`
**Fecha:** 2026-09-29 · **Deduplicada contra:** R49

**Receta de un minuto.**

- Después de activar Pages (receta R49-PAGES: Settings > Pages > Deploy from branch: main, /docs), esperar a que termine el build 'pages build and deployment' en Actions. Abrir https://josanoforo.github.io/Modelado-Mexicano/consultar.html en un navegador normal, hacer una consulta y confirmar que responde sin el aviso de file://. Pegar URL, fecha y «carga/no carga» en la hoja.
- En github.com/Josanoforo/Modelado-Mexicano ir a Settings > Pages > Build and deployment > Source: Deploy from a branch > main, /docs > Save. Esperar el build y abrir https://josanoforo.github.io/Modelado-Mexicano/. DOI, después (R49 opción c): Releases > Draft new release con tag v2026.09 y conectar el repo en zenodo.org > GitHub. Anotar URL, fecha y DOI en la hoja.
- Abrir github.com/Josanoforo/Modelado-Mexicano/settings/pages → Source: «Deploy from a branch» → rama main, carpeta /docs → Save. Esperar ~1 min, abrir https://josanoforo.github.io/Modelado-Mexicano/tablero y .../PROTOCOLO-TABLERO y contestar «Pages activo <fecha>» (R49 opción (c)). El DOI puede ir después.

**Destino / acuse.** https://josanoforo.github.io/Modelado-Mexicano/consultar.html (fuente docs/consultar.md; baseurl /Modelado-Mexicano en docs/_config.yml:3) · GitHub Settings > Pages (repo Josanoforo/Modelado-Mexicano, carpeta docs/ con docs/_config.yml); zenodo.org > GitHub · https://github.com/Josanoforo/Modelado-Mexicano/settings/pages (receta en forense/notas/2026-09-23-GEN2-FRONT-1-cierre.md:64-66; firma en forense/analisis/hoja-firmas-21/decisiones-21.tsv R49)

## A03 · Poner los metadatos del repo (About y vista previa social)

**Cierra (1):** `NC-260927-GEN2-TRAMITE-FIRMAS-20-96f9-02`
**Fecha:** 2026-09-29 · **Deduplicada contra:** R49

**Receta de un minuto.**

- En la portada del repo, abrir el engrane de About. Description: la de docs/_config.yml:2. Website: https://josanoforo.github.io/Modelado-Mexicano/ (solo después de R49-PAGES). Topics: mexico inegi benchmark survey-data reproducible-research behavioral-science spanish. Luego Settings > General > Social preview > Edit > subir docs/assets/social-preview.png.

**Destino / acuse.** GitHub repo About + Settings > General > Social preview · archivo docs/assets/social-preview.png · texto en docs/_config.yml:2 y forense/notas/2026-09-26-GEN2-FRONT-3-PORTADA-1-cierre.md:11

## A04 · Registrarse con la identidad de mesa en las fuentes de R46 (EMOVI/CEEY, WVS, IFPS, MCPS, LAPOP)

**Cierra (2):** `NC-260924-GEN2-ASTRA5-U5-ADQUISICION-1-43d6-01`, `NC-260925-GEN2-CORPUS-COMPLETO-1-7813-02`
**Fecha:** 2026-09-29 · **Deduplicada contra:** R46

**Receta de un minuto.**

- Con la opción (1) recomendada de R46: en un navegador normal, registrarse con el correo institucional de mesa en https://ceey.org.mx/emovi/ (EMOVI 2011/2023; 2011 también en ICPSR 35333), https://www.worldvaluessurvey.org/WVSEVStrend.jsp (longitudinal) y https://www.worldvaluessurvey.org/WVSDocumentationWV7.jsp (ola 7 EE.UU./Japón); aceptar los términos académicos y descargar a Descargas MX. IFPS y MCPS esperan a que una afirmación los exija.
- Navegador normal, correo institucional de mesa: registrarse y aceptar términos académicos en (1) https://ceey.org.mx/emovi/ (EMOVI 2011/2017/2023), (2) https://www.worldvaluessurvey.org/WVSEVStrend.jsp (WVS/EVS longitudinal: olas 1–6 de México), (3) https://www.vanderbilt.edu/cgd/data-access/ (rondas LAPOP México que faltan), (4) https://www.latinobarometro.org/latContents.jsp (olas 1995–2022), (5) https://www.pewresearch.org/religion/dataset/religion-in-latin-america-2014-dataset/ (Pew 2014). Descargar a Descargas MX, avisar y firmar R46 con fecha. Mínimo de R46 opción (1): EMOVI + WVS.

**Destino / acuse.** Descargas MX → registro por /adquiere a cargo del sucesor GEN2-OBTENCION-EXTERNA-2; URLs verificadas el 27/sep en forense/analisis/obtencion-externa-1/solicitudes/registros-con-identidad.md · Descargas MX → registro por /adquiere con sha y licencia a cargo de GEN2-OBTENCION-EXTERNA-2 (encargo NO-ENCONTRADO en origin/main: 0 de 1219 rutas bajo forense/encargos con 'OBTENCION-EXTERNA-2') · firma en forense/analisis/hoja-firmas-21/decisiones-21.tsv R46

## A05 · Montar el disco externo (o el remoto cifrado) y dar la ruta del respaldo del corpus

**Cierra (2):** `NC-260921-GEN2-CORPUS-INTEGRIDAD-Y-RESPALDO-1-3d56-01`, `NC-260923-GEN2-CORPUS-RESPALDO-EJECUCION-1-a307-01`
**Fecha:** 2026-09-29 · **Deduplicada contra:** R47

**Receta de un minuto.**

- Conectar el disco externo reformateado (o crear el remoto cifrado de mesa) y anotar su ruta de montaje. Firmar R47: «Respaldo del corpus: opción (a|b) con fecha ____». Con esa ruta, un acto CAJA (GEN2-CORPUS-RESPALDO-EJECUCION-2) corre los cuatro pasos de INSTRUCCION-RESPALDO.md: --indexa, --copia, --verifica y --restaura 20. Luego asienta 3d56-01, f2e5-20 y f2e5-26 juntas.
- Es la misma que en 3d56-01: montar el disco o el remoto cifrado, dar la ruta y firmar R47 con opción y fecha. El acto CAJA sucesor corre los cuatro comandos con --destino, verifica 1914/1914 por sha256 en destino y aplica en el mismo acto las 4 propuestas de propuestas-manifiesto-2026-09-21.tsv.

**Destino / acuse.** $DEST de forense/analisis/corpus-integridad-1/INSTRUCCION-RESPALDO.md (la ruta que mesa nombre) · firma en forense/analisis/hoja-firmas-21/decisiones-21.tsv R47 · $DEST de forense/analisis/corpus-integridad-1/INSTRUCCION-RESPALDO.md · forense/analisis/corpus-integridad-1/propuestas-manifiesto-2026-09-21.tsv · firma R47 (decisiones-21.tsv)

## A06 · Pegar la v2.17 de las instrucciones en el proyecto de Claude y subir la PLANTILLA v2.2

**Cierra (1):** `NC-260928-GEN2-TRAMITE-INSTRUCCIONES-V217-1-3e59-01`
**Fecha:** 2026-09-29 · **Deduplicada contra:** R51

**Receta de un minuto.**

- En el proyecto de Claude, sustituir el bloque de instrucciones por el contenido de gobierno/PEGAR-EN-PROYECTO-v2_17.md y subir PLANTILLA-ENCARGO v2.2 al conocimiento. Después contestar en chat: «pegado <fecha>: instrucciones v2.17 y PLANTILLA-ENCARGO v2.2 en el proyecto de Claude.» Con esa línea corre GEN2-TRAMITE-INSTRUCCIONES-V217-2 (commit 2 de A.9).

**Destino / acuse.** Proyecto de Claude (instrucciones + conocimiento) · fuente gobierno/PEGAR-EN-PROYECTO-v2_17.md (+ .sha256)

## A07 · Enviar las solicitudes (a)–(f) de OBTENCION-EXTERNA-1 (Banxico, IECM y Segob por PNT; correos; Delaney)

**Cierra (3):** `NC-260928-GEN2-OBTENCION-EXTERNA-1-81e1-07`, `NC-260928-GEN2-OBTENCION-EXTERNA-1-81e1-01`, `NC-260928-GEN2-OBTENCION-EXTERNA-1-81e1-04`
**Fecha:** 2026-10-05 · **Deduplicada contra:** R48 = solicitudes (a)–(f) de OBTENCION-EXTERNA-1; la NC 81e1-04 añade una línea a la (c)

**Receta de un minuto.**

- Con identidad de mesa y en navegador normal: (a) Banxico, (b) IECM y (c) Segob por https://www.plataformadetransparencia.org.mx/, pegando a-/b-/c-*.md. (d) Correo a cfelixbr@iu.edu con d-felix-brasdefer-role-plays.md. (e) Delaney, vía https://digitalcommons.fiu.edu/etd/4710/, con e-fiu-delaney-microdato.md. (f) Formulario de https://worldpanelbynumerator.com/latin-america/mexico con f-worldpanel-convenio.md. Guardar el folio o acuse de cada una y pasarlo al chat.
- Entrar a https://www.plataformadetransparencia.org.mx con la cuenta de mesa → sujeto obligado IECM (CDMX) → pegar forense/analisis/obtencion-externa-1/solicitudes/b-iecm-copaco-sepcopp.md con los corchetes llenos → enviar y guardar el acuse.
- Al presentar por PNT (sujeto obligado Segob) forense/analisis/obtencion-externa-1/solicitudes/c-segob-mecanismo-incorporaciones.md, añadir la línea: «y los Informes Estadísticos Mensuales del Mecanismo de diciembre de 2018 y de marzo a diciembre de 2019, no enlazados en gob.mx/defensorasyperiodistas». Guardar el acuse.

**Destino / acuse.** forense/analisis/obtencion-externa-1/solicitudes/ (textos a–f) · acuses por adenda de GEN2-OBTENCION-EXTERNA-2 (FP-260928-GEN2-TRAMITE-FIRMAS-21-8560-01; encargo NO-ENCONTRADO en origin/main) · Acuse por adenda de GEN2-OBTENCION-EXTERNA-2 (FP-…-8560-01); la respuesta se registra en la cola L936-937 · Acuse por adenda de GEN2-OBTENCION-EXTERNA-2 (FP-…-8560-01); los PDF recibidos se registran en la cola L939

## A08 · Pedir por acceso institucional los dos papers de pago de OBTENCION-EXTERNA-1 P3

**Cierra (1):** `NC-260928-GEN2-OBTENCION-EXTERNA-1-81e1-06`
**Fecha:** 2026-10-05 · **Deduplicada contra:** distinta de las (a)–(f): son dos PDF de pago

**Receta de un minuto.**

- Abrir https://doi.org/10.1111/lamp.70057 y confirmar que es «The Power of the Older Vote in Culiacan in 2021» (Sandoval, Latin American Policy). Pedir ese PDF y el de https://doi.org/10.1177/0149206308316063 (Pellegrini & Scandura 2008) por la biblioteca institucional o el préstamo interbibliotecario de mesa. Si no hay acceso: decidir en una línea entre compra y dejarlos SIN-FETCH con DOI. Dejar los PDF en Descargas MX.

**Destino / acuse.** Descargas MX → registro por /adquiere con sha y licencia a cargo de GEN2-OBTENCION-EXTERNA-2 (encargo NO-ENCONTRADO en origin/main); filas SANDOVAL_2026_LATIN_AMERICAN_POLICY y Pellegrini de data/cola-adquisicion-v1_0.tsv

## A09 · Presentar a INEGI la solicitud ENCIG evento × canal (y, en la misma visita, el listado de UPM de ENVIPE)

**Cierra (3):** `NC-0153`, `NC-0111`, `NC-0159`
**Fecha:** 2026-10-05 · **Deduplicada contra:** expediente 04 de EXPEDIENTES-ACCESO-21; no es ninguna de (a)–(f)

**Receta de un minuto.**

- Con identidad de mesa, abrir https://www.inegi.org.mx/inegi/contacto.html (o escribir a atencion.usuarios@inegi.org.mx). Pegar forense/expedientes-acceso/2026-09-11-GEN2-EXPEDIENTES-ACCESO-21/04-INEGI-ENCIG-NC-0153.md y añadir una línea que pida la tasa general evento × canal (NC-0111). Enviar y pasar al chat el folio de atención.
- Abrir https://www.inegi.org.mx/inegi/contacto.html (o escribir a atencion.usuarios@inegi.org.mx) → pegar forense/expedientes-acceso/2026-09-11-GEN2-EXPEDIENTES-ACCESO-21/04-INEGI-ENCIG-NC-0153.md, que ya pide evento × canal → enviar con la identidad de mesa → anotar fecha y acuse en REGISTRO-RECEPCION.tsv, fila ENCIG-NC-0153.
- Abrir https://www.inegi.org.mx/inegi/contacto.html (o escribir a atencion.usuarios@inegi.org.mx), si se puede en la misma sesión del envío de NC-0153. Pegar: «Para ENVIPE 2021, 2023 y 2024 solicitamos el listado completo de UPM seleccionadas por estrato, incluidas las que no aportaron viviendas, o en su defecto los errores estándar oficiales de los dominios validados; no pedimos geografía identificable.» Adjuntar la sección de diseño de forense/notas/2026-09-11-GEN2-VALIDACION-R-ENVIPE-CSV-cierre.md y pegar el folio en el chat.

**Destino / acuse.** REGISTRO-RECEPCION.tsv fila ENCIG-NC-0153 (fecha_presentacion, acuse_no_personal), asentado por el acto que reciba el folio; cierra NC-0153 y alimenta NC-0111 (ADQUISICION) · REGISTRO-RECEPCION.tsv (ENCIG-NC-0153) → acto receptor que re-deriva el denominador de la familia B; cubre NC-0153 y NC-0111 · https://www.inegi.org.mx/inegi/contacto.html (data/cola-adquisicion-v1_0.tsv, fila ENVIPE_ROSTER_UPM_O_SERVICIO_VARIANZA)

## A10 · Pedir a INEGI la regla oficial de varianza de los 39 estratos singleton de ENOE 2024T4

**Cierra (1):** `NC-260923-ASTRA5-U1-TRABAJO-ENOE-e422-04`
**Fecha:** 2026-10-05 · **Deduplicada contra:** distinta de A09

**Receta de un minuto.**

- Abrir forense/analisis/familias-2027-enoe-inferencia-1/enoe-hoja-decision.md §«Insumo específico para decidir» (l.15-23); copiar la solicitud (regla oficial de varianza para los 39 EST_D_TRI con una UPM en ENOE 2024T4, lista en diagnostico/enoe-auditoria.json; crosswalk de unidad de selección, certeza o pesos de réplica); enviarla por el canal de atención a usuarios de INEGI desde la cuenta de mesa; guardar el acuse y asentarlo por adenda (regla FP-260928-GEN2-TRAMITE-FIRMAS-21-8560-01).

**Destino / acuse.** INEGI · atención a usuarios / área ENOE

## A11 · Pedir a INEGI la llave LLAVE→UPM/estrato (o pesos replicados) de ENDIREH 2003

**Cierra (1):** `NC-260923-ASTRA5-U2-ENDIREH-6a2c-01`
**Fecha:** 2026-10-05 · **Deduplicada contra:** acuse por adenda de OBTENCION-EXTERNA-2

**Receta de un minuto.**

- Por el canal oficial de Atención a Usuarios de INEGI (inegi.org.mx → Contacto), pedir para ENDIREH 2003 la asignación LLAVE→UPM y estrato de diseño, o pesos replicados, y la documentación del factor actualizado. Citar que el ZIP público solo trae FAC_PER y enlazar forense/analisis/dominios/genero/endireh-2003-dictamen-documental.md. Guardar el acuse.

**Destino / acuse.** El acuse lo registra GEN2-OBTENCION-EXTERNA-2 (FP-260928-GEN2-TRAMITE-FIRMAS-21-8560-01). El archivo que entregue INEGI va a Descargas MX y se registra en data/manifiesto.yaml desde caja. Con él se abre un CALC nuevo de ENDIREH 2003.

## A12 · Presentar los expedientes de acceso ICPSR 35024, OECD Trust PUM y ENJUVE

**Cierra (2):** `NC-0151`, `NC-0061`
**Fecha:** 2026-10-05 · **Deduplicada contra:** el correo OECD de NC-0061 es el mismo envío que el de NC-0151

**Receta de un minuto.**

- Tres envíos de un minuto cada uno, llenando solo datos personales verdaderos. (1) ICPSR: iniciar sesión en icpsr.umich.edu, estudio 35024, y pedir el RDUA según 01-ICPSR-35024-RDUA.md. (2) OCDE: correo a govtrustinfo@oecd.org con 02-OECD-TRUST-PUM.md y el .docx adjunto; este envío cierra también NC-0061 [a]. (3) IMJUVE: solicitud en la PNT según 05-IMJUVE-ENJUVE.md. Pegar en el chat fecha y acuse de cada uno.
- (a) OCDE: desde tu cuenta, escribir a govtrustinfo@oecd.org adjuntando 02-OECD-TRUST-PUM.md y 02-OECD-TRUST-PUM-TECHNICAL-DRAFT.docx; es el mismo envío que NC-0151. Completar solo datos verdaderos y anotar fecha y acuse en la fila OECD-TRUST-PUM de REGISTRO-RECEPCION.tsv. (b) Tandas (equipo@tandamas.mx): no enviar; asentar «vía comercial diferida por D18» en la fila REGISTRO_OPERATIVO_DE_TANDAS_DIGITALES del registro de la cola.

**Destino / acuse.** forense/expedientes-acceso/2026-09-11-GEN2-EXPEDIENTES-ACCESO-21/ (01-ICPSR-35024-RDUA.md, 02-OECD-TRUST-PUM.md + .docx, 05-IMJUVE-ENJUVE.md); acuse en REGISTRO-RECEPCION.tsv · govtrustinfo@oecd.org · adjuntos en forense/expedientes-acceso/2026-09-11-GEN2-EXPEDIENTES-ACCESO-21/02-OECD-TRUST-PUM{.md,-TECHNICAL-DRAFT.docx} · acuse en …/REGISTRO-RECEPCION.tsv

## A13 · Enviar la solicitud combinada ENNViH DIN+S6 (pesos replicados o servicio de varianza)

**Cierra (1):** `NC-0156`
**Fecha:** 2026-10-05 · **Deduplicada contra:** expediente 03 de EXPEDIENTES-ACCESO-21

**Receta de un minuto.**

- Enviar desde tu cuenta, a support@ennvih-mxfls.org (o por el formulario de contacto MxFLS/ENNViH), el texto de 03-ENNVIH-DIN-S6.md: solicitud combinada DIN+S6 de pesos replicados con contrato completo o de un servicio oficial de varianza para los cuatro estimandos. Completar solo datos personales verdaderos. Luego anotar fecha_presentacion y acuse en la fila ENNVIH-DIN-S6 de REGISTRO-RECEPCION.tsv.

**Destino / acuse.** support@ennvih-mxfls.org · texto: forense/expedientes-acceso/2026-09-11-GEN2-EXPEDIENTES-ACCESO-21/03-ENNVIH-DIN-S6.md · acuse: …/REGISTRO-RECEPCION.tsv

## A14 · Escribir al CEEY por el cuadro y el denominador de la cifra de movilidad desde pobreza

**Cierra (1):** `NC-260926-GEN2-ASTRA6-C3-TRABAJO-MOVILIDAD-1-ed83-03`
**Fecha:** 2026-10-05 · **Deduplicada contra:** misma institución que R46 pero otra acción (no es un registro)

**Receta de un minuto.**

- Desde el correo institucional de mesa, escribir al CEEY (contacto en https://ceey.org.mx/) pidiendo el cuadro y el denominador exactos de la cifra de movilidad desde pobreza citada por el report de movilidad (ola EMOVI, condicionamiento origen→destino, universo). Archivar la respuesta tal cual y avisar para que un recibo decida el tratamiento editorial. Si R46 trae el microdato EMOVI, CAJA puede recalcularla y el correo sobra.

**Destino / acuse.** forense/analisis/reports-v2/trabajo-movilidad-1/ (respuesta archivada con sha); cierra NC-…-ed83-03

## A15 · Escribir al autor de «Do Workers Value Formal Jobs?» por el Appendix C y los datos

**Cierra (1):** `NC-0166`
**Fecha:** 2026-10-05 · **Deduplicada contra:** el correo sale del PDF del payload (corpus de caja)

**Receta de un minuto.**

- Abrir el PDF do_workers_value_formal_jobs_mexico_20260316.pdf (versión de marzo de 2026, 48 pp.) y copiar el correo del autor de correspondencia (no verificado aquí: el PDF vive en el corpus de caja). Escribirle con identidad de mesa, con la cita completa, y pedirle el Appendix C/cuestionario, la asignación de los 64 bloques, el microdato anonimizado y el código de las tablas 2–5, para reproducir antes de proponer una regla DCE. Pasar el acuse al chat.

**Destino / acuse.** correo del autor de correspondencia (dato en el PDF del payload do_workers_value_formal_jobs_mexico_20260316) · acuse asentado por un acto de trámite; cierra NC-0166 (BANDEJA-TITULAR entrada 2)

## A16 · Registrarse y bajar Pew «Religion in Latin America» 2014

**Cierra (1):** `NC-260925-GEN2-CONFIANZA-RELIGIOSIDAD-CAPITAL-SOCIAL-PISOS-1-ac7b-03`
**Fecha:** 2026-10-05 · **Deduplicada contra:** no está en R46

**Receta de un minuto.**

- En un navegador normal, abrir https://www.pewresearch.org/religion/dataset/religion-in-latin-america/, crear la cuenta gratuita con el correo de mesa, aceptar los términos y descargar el dataset (SAV/CSV + cuestionario). Dejarlo en Descargas MX/UNIVERSO-2026-09/PEW/ y avisar.

**Destino / acuse.** Descargas MX/UNIVERSO-2026-09/PEW/ (convención de data/cache/universo-p1.tsv) → registro por /adquiere a cargo del sucesor GEN2-OBTENCION-EXTERNA-2 (su encargo: NO-ENCONTRADO en forense/encargos/ de origin/main); desbloquea RELIG-017/023

## A17 · Solicitar EMIF Norte/Sur al COLEF (formulario con identidad)

**Cierra (1):** `NC-260925-GEN2-FAMILIA-CUIDADOS-Y-MIGRACION-PISOS-1-2a0e-02`
**Fecha:** 2026-10-05 · **Deduplicada contra:** no está en R46

**Receta de un minuto.**

- Abrir https://www.colef.mx/emif/ en un navegador → menú «Bases de datos» → llenar el formulario de solicitud con la identidad de mesa → bajar EMIF Norte y EMIF Sur (.sav/.dta) a Descargas MX y avisar la ruta.

**Destino / acuse.** Descargas MX → /adquiere en CAJA (registro en data/manifiesto.yaml con sha y alta de la fila EMIF en la cola; cierra NC-…-2a0e-02)

## A18 · Bajar desde una red doméstica los cortes REDECO previos a 2025

**Cierra (1):** `NC-260924-GEN2-ASTRA5-U5-ADQUISICION-1-43d6-03`
**Fecha:** 2026-10-05 · **Deduplicada contra:** necesita red que la caja no tiene

**Receta de un minuto.**

- Desde una red doméstica (no la caja), abrir https://www.datos.gob.mx/dataset/registro_despachos_cobranza_contratados_entidades_financieras y los recursos que apunten a repodatos.atdt.gob.mx. Bajar a Descargas MX todo corte REDECO anterior a 30/09/2025. Si solo existen los dos cortes ya obtenidos, anotarlo con la fecha.

**Destino / acuse.** Descargas MX; se registra en data/manifiesto.yaml desde caja y se abre la fila residual REDECO (cortes < 30/09/2025) en la cola con esa evidencia.

## A19 · Buscar la metodología 2012 de ENCUP en el portal de Segob

**Cierra (1):** `NC-260923-ASTRA5-U3-POLITICA-COMPLETAR-d459-01`
**Fecha:** 2026-10-05 · **Deduplicada contra:** acción de navegador

**Receta de un minuto.**

- Abrir https://fomentocivico.segob.gob.mx/es/FomentoCivico/ENCUP en un navegador y buscar «metodología 2012» o «nota técnica» (encup-diseno-dictamen-v1_0.md:58-60). Si aparece, bajar el PDF a Descargas MX. Si no aparece, anotar NO-ENCONTRADO con la fecha y los términos usados.

**Destino / acuse.** Descargas MX; el PDF se registra en data/manifiesto.yaml (convención R46: lo registra GEN2-OBTENCION-EXTERNA-2). Con él se reabre la inferencia ENCUP que FP df0d-02 deja en espera.

## A20 · Abrir el DOI de Benjamini–Hochberg 1995 y copiar la frase que distingue FDR de FWER

**Cierra (1):** `NC-0278`
**Fecha:** 2026-10-05 · **Deduplicada contra:** acceso institucional

**Receta de un minuto.**

- En un navegador normal (con acceso institucional si lo pide), abrir https://doi.org/10.1111/j.2517-6161.1995.tb02031.x (redirige a academic.oup.com, JRSS-B), copiar la frase del resumen que distingue FDR de FWER y pegarla con la URL final y la fecha. Las otras dos fuentes ya están abiertas (#1004).

**Destino / acuse.** forense/notas/2026-09-17-GEN2-CELDA-D-CAREO-1.md (§1.2 del careo, por adenda de un acto; no se edita la nota sellada), citado desde el cierre de NC-0278

## A21 · Adjuntar al chat de un acto de trámite los tres archivos fuente (transfer de Astra, plan de visibilización, informe y revisión del mapa)

**Cierra (3):** `NC-260928-GEN2-ASTRA-CONTINUIDAD-C3-1-26bb-01`, `NC-260923-GEN2-FRONT-1-4296-02`, `NC-260927-GEN2-MAPA-INSTRUMENTOS-ALTERNOS-1-4b11-01`
**Fecha:** 2026-10-05 · **Deduplicada contra:** un solo gesto; cada archivo con su sha256 (A.3)

**Receta de un minuto.**

- Adjuntar el zip del transfer de Astra del 27/sep (sha256 empieza 545600ae58fe4e54) a cualquier sesión de Claude con la instrucción: «extrae los 8 miembros y SHA256SUMS.txt en forense/encargos/fuentes/ASTRA-TRANSFER-20260927/, corre sha256sum -c SHA256SUMS.txt, deja un sidecar con el sha del zip y cierra NC-…-26bb-01 citando el commit».
- Adjuntar PLAN-VISIBILIZACION-2026-09-23.md al chat del próximo acto de trámite, junto con la salida de `sha256sum PLAN-VISIBILIZACION-2026-09-23.md`. El acto lo archiva verbatim con sidecar en forense/encargos/fuentes/. Si mesa no lo va a consumir, basta una línea («PLAN-VISIBILIZACION no se consume») y la fila cierra con esa firma.
- Adjuntar al chat del próximo acto de trámite los dos .md: el informe exportado del artefacto «Benchmark del Mexicano: fuentes alternas para 10 incógnitas» y REVISION-repo-y-fuentes-alternas-2026-09-27.md, cada uno con su `sha256sum`. El acto los archiva verbatim con sidecar en forense/analisis/mapa-instrumentos-alternos/adjuntos/. Si ya no existen del lado de mesa, basta decirlo en una línea y la fila cierra con esa firma.

**Destino / acuse.** forense/encargos/fuentes/ASTRA-TRANSFER-20260927/ (la ruta la fija el encargo C3-1:9; el directorio padre forense/encargos/fuentes/ existe) · forense/encargos/fuentes/ (FRONT-1.md:55; el directorio existe con 23 entradas) · forense/analisis/mapa-instrumentos-alternos/adjuntos/ (MAPA encargo:30; el directorio padre existe y adjuntos/ está NO-ENCONTRADO hoy)

## A22 · Aportar la evidencia de /raw y el launcher del lote 1 de C1 (rótulo CIEGA-POR-SEPARACIÓN)

**Cierra (1):** `NC-260927-GEN2-RECIBO-ASTRA6-1-beee-08`
**Fecha:** 2026-10-05 · **Deduplicada contra:** reserva declarada por el recibo de ASTRA6-1

**Receta de un minuto.**

- Escribir a Astra por su canal habitual: «Del lote 1 de C1 necesito (1) el log del materializador y un `ls -lR /raw` con sha256 por archivo de los lanzamientos ayuda, decisiones y laboral (los tres sin hashes de /raw en el repo), y (2) el SHA-256 del lanza.sh con que corrió el intento 2 de comunitaria. Pégalo tal cual, sin resumir.» Guardar la respuesta sin editar.

**Destino / acuse.** forense/validacion-independiente/catalogo-1-ejecucion-lote1/ (adenda con sha256, entrega por encargo CAJA/tramite); mientras no llegue, el rótulo CIEGA-POR-SEPARACIÓN del lote 1 conserva sus reservas declaradas.

## A23 · Convenios y credenciales personales de tandas (tanda.mx/tandamas.mx, Tanda+) y Findex individual

**Cierra (1):** `NC-0056`
**Fecha:** 2026-10-05 · **Deduplicada contra:** NC-0061 es el correo a tandas de la misma familia; FP-286 difiere lo comercial (D17/D18)

**Receta de un minuto.**

- Los tres son personales y no se negocian desde el repo: (1) convenio institucional con tanda.mx/tandamas.mx y con Tanda+ (equipo@tandamas.mx); (2) trámite presencial; (3) cuenta gratuita del Banco Mundial para Findex individual. Con identidad de mesa: escribir o presentarse; guardar el acuse en `forense/expedientes-acceso/` y avisar la ruta.

