# Investigación dirigida · tasa general de solicitud de pago informal por canal

Fecha de ejecución: 10 de septiembre de 2026. Objeto: `NC-0153` /
`TASA_GENERAL_SOLICITUD_PAGO_INFORMAL_POR_CANAL_TRAMITES_MEXICO`. Esta nota
continúa el mismo encargo y el PR #695; no reemplaza la reconstrucción previa
de la unidad de ENCIG ni convierte candidatos parciales en parámetros.

## Resultado

La Fase 3 sí se ejecutó con red real, navegador/buscador, `curl`, `wget`, APIs,
catálogos, archivos históricos y corpus. No se localizó una fuente pública que
observe a la vez, con cobertura nacional de México: (a) cada evento elegible de
trámite, (b) solicitud o insinuación de pago informal ligada a ese evento y
(c) canal del mismo evento. El resultado no es “cero fuentes”: se obtuvieron
diez payloads pertinentes y se identificaron numerosos productos parciales.

El hallazgo más cercano es **ENEAC 2021**. Su microdato sí enlaza canal y
solicitud en la misma unidad trámite, pero representa sólo microempresas de dos
sectores en Aguascalientes. Por ello es `EXISTE-SATISFACE-PARCIAL` por
geografía y universo, no satisfacción del estimando nacional.[^1]

## 1. Por qué la primera sonda devolvió HTTP 000

`000` no fue una respuesta del servidor. Dentro de la caja, `curl` terminó con
`Could not resolve host` y `wget` con `Temporary failure in name resolution`:
el fallo ocurrió en DNS, antes de TCP/TLS/HTTP. La misma sonda fuera del
aislamiento resolvió `www.inegi.org.mx` a `200.23.8.5`; `curl` y `wget`
recibieron `HTTP/1.1 200 OK`. El buscador web también abrió el programa
oficial.[^2] Por tanto, el `000` anterior era una limitación del entorno, no
evidencia de ausencia de fuente.

Se probaron mecanismos alternativos. Para `amij.org.mx`, `curl` y `wget`
fallaron por DNS y DNS-over-HTTPS no devolvió un registro A; el texto indexado
del informe se pudo inspeccionar, pero no se fingió una descarga. Para INEGI,
la URL correcta del cuestionario respondió como PDF; dos nombres plausibles
respondieron `200 text/html` con 2,263 bytes, la firma de *soft 404*. También se
probaron endpoints de la aplicación dinámica: el endpoint antiguo de
`archivoscompaginacion` quedó vacío/no JSON y el nuevo redirigió a la página de
mantenimiento `/500.html`. La página, el RNM y las rutas estáticas siguieron
siendo utilizables.[^3]

Comprobación ejecutada:

```text
sandbox: curl (6) Could not resolve host -> http=000
sandbox: wget: Temporary failure in name resolution
fuera de sandbox: curl http=200 remote=200.23.8.5
fuera de sandbox: wget HTTP/1.1 200 OK
```

## 2. Criterio de satisfacción

Una fuente exacta debe permitir, por canal `c`,

```text
eventos elegibles con solicitud/insinuación de pago informal y canal=c
-----------------------------------------------------------------------
             todos los eventos elegibles con canal=c
```

La unidad debe ser el evento, no la persona, el hogar, la empresa, una queja o
el subconjunto que ya declaró corrupción. El periodo, ponderador y diseño
muestral deben estar disponibles. “Canal” significa cómo se realizó ese mismo
trámite (por ejemplo presencial/en línea), no el modo de entrevista ni el canal
por el cual se presentó una denuncia.

## 3. Candidatos examinados

### 3.1 ENCIG 2025, INEGI — nacional, pero el enlace evento-corrupción no es unívoco

- **Reactivo exacto.** 8.3: “Durante 2025, para agilizar, realizar, evitar
  procedimientos o multas…”; inciso 1: “¿Un (una) servidor(a) público(a) o
  empleado(a) de gobierno intentó apropiarse o le solicitó de forma directa
  algún beneficio (dinero, regalos o favores) que usted pudiera otorgarle?”.
  Los incisos 2 y 3 captan tercero/coyote e insinuación. 8.4 identifica el tipo
  de trámite y 8.5 pregunta en cuántas realizaciones ocurrió.[^4]
- **Unidad / numerador / denominador.** 8.4–8.5 permiten conteos por tipo de
  trámite; `P7_3` registra el canal de cada evento `(ID_TRA,NT_TIPO)`, mientras
  `P8_4` vive en `ID_TRA`. En 501 `ID_TRA` repetidos `P7_3` discrepa. No se
  puede atribuir el conteo de corrupción a uno de varios eventos/canales sin
  una regla inventada.
- **Periodo / diseño.** 2025; población de 18+ en áreas urbanas de 100 mil y
  más, diseño probabilístico trietápico, estratificado y por conglomerados;
  46 mil viviendas.[^2]
- **Archivo.** Cuestionario público descargado; microdato y estructura ya
  estaban en el corpus. **Parcial:** nacional y con canal, pero no identifica
  la solicitud en el evento cuando una persona repite el tipo de trámite.

### 3.2 ENEAC 2021, SESEA Aguascalientes — cruce exacto, cobertura parcial

- **Reactivos exactos.** P13: “¿Cómo se realizó el trámite?”: (1) la empresa
  acudió a instalaciones de gobierno, (2) “en línea, por medio de internet y
  computadora”, (3) personal de gobierno acudió al negocio. P16: “¿Recuerda si
  algún servidor público le insinuó o le pidió a Usted o a esta empresa,
  dinero, regalos o favores a cambio de agilizar, autorizar o evitar este
  trámite o pago?”. P17 cubre tercero/coyote y P18 insinuación/condiciones.[^5]
- **Unidad / numerador / denominador.** Registro de trámite. Numerador
  descriptivo: unión `P16=1 ∪ P17=1 ∪ P18=1`; denominador: registros con P13
  válido. Hay 894 trámites, 869 con canal válido y 25 `NS/NC`. Sin ponderador
  en los archivos descargados, el cálculo no ponderado da: instalaciones
  32/710 = 0.045070; en línea 3/49 = 0.061224; personal en negocio 8/110 =
  0.072727. Son resultados exploratorios, no adopción.
- **Periodo / diseño.** 1–7 de diciembre de 2021; 706 entrevistas cara a cara,
  selección probabilística con marco DENUE, margen teórico estatal ±3.6% al
  95%.[^6]
- **Cobertura.** Establecimientos fijos de 0–10 empleados, SCIAN 46 y 72, que
  realizaron o intentaron trámites estatales/municipales en Aguascalientes.
  **Parcial fuerte:** satisface unidad, conducta y canal, pero no México
  nacional ni población general.

La reproducción está en `tools/diagnostico_fuente_general_corrupcion.py` y
queda marcada `EXPLORATORIO-NO-ADOPTAR`.

### 3.3 MCCI 2019–2024 — tasa general por persona, sin canal

- **Reactivo exacto.** “En los últimos 12 meses, ¿para realizar algún trámite
  o recibir algún servicio o apoyo gratuito del gobierno le solicitaron una
  mordida, propina o un favor?”.[^7]
- **Unidad / numerador / denominador.** Persona encuestada; `Sí` a
  `mordida_encuestado` sobre respuestas válidas, ponderado por
  `indice_ponderador`. No hay variable de canal entre 235 columnas.
- **Periodo / diseño.** Encuestas nacionales anuales; 1,500 registros en cada
  año 2019–2023 y 1,000 en 2024. Productores de campo: Datología Reforma
  (2019–2023) y Lorena Becerra y Asociados (2024). El archivo no documenta un
  diseño por evento.
- **Resultado parcial.** Tasas ponderadas: 2019 .135155; 2020 .099541; 2021
  .097855; 2022 .143309; 2023 .093758; 2024 .100469. Es solicitud general por
  persona, no por evento/canal.

### 3.4 INCBG 2010, Transparencia Mexicana — tasa por ocasión, sin canal

- **Reactivo.** No se localizó el cuestionario/microdato para transcribir el
  reactivo exacto. El informe primario define operacionalmente “servicio
  obtenido con mordida”.
- **Unidad / numerador / denominador.** Numerador: veces que se dio mordida en
  35 servicios; denominador: veces que se usaron esos 35 servicios; 10.3 por
  100 ocasiones en 2010.[^8]
- **Diseño.** 15,326 hogares, muestra estrictamente probabilística, 32
  encuestas estatales, estructura urbano-rural del Censo 2010, error nacional
  menor a 1%; respondieron jefes de hogar usuarios de cada servicio.
- **Archivo.** Informe ejecutivo público descargado. El informe anunció base
  íntegra “en unos días” y una nota contemporánea indicó consulta en CIDE; no
  apareció un microdato público en CIDE, búsquedas dirigidas ni CDX/Wayback.
  **Parcial:** unidad ocasión y tasa general, pero sin canal y sin microdato
  localizado.

### 3.5 ENCUCI 2020, INEGI — solicitud/entrega por persona con contacto

- **Reactivos exactos.** AP5_17: “¿hubo alguna ocasión en la que un funcionario
  o servidor público le haya pedido dar una dádiva, un favor o dinero extra por
  un asunto o trámite relacionado con sus funciones?”. AP5_18 pregunta si
  “tuvo que darle… una dádiva, un favor o dinero extra (que no sea la tarifa
  oficial)”.[^9]
- **Unidad / numerador / denominador.** Persona seleccionada de 15+ con al
  menos un contacto y respuesta válida; numeradores `AP5_17=1`, `AP5_18=1` o
  su unión; denominador 13,411; `FAC_SEL`. Resultados ya reproducidos:
  .106319, .073640 y .126006.
- **Periodo / archivo.** Últimos 12 meses, ENCUCI 2020; microdato DBF y
  descriptor públicos ya estaban en el corpus. **Parcial:** no identifica
  evento ni canal.

### 3.6 UNAM-IIJ 2015 — cuatro trámites, sin canal

- **Reactivo disponible.** Para reconexión de luz, licencia de conducir,
  incapacidad médica y licencia de construcción, `p4_j` distingue a quienes
  realizaron el trámite en el último año y si “le solicitaron dinero extra”.
- **Unidad / numerador / denominador.** Persona; `p4_j=2` sobre
  `p4_j∈{1,2}`, con `Pondi2`, separado por trámite. Tasas ponderadas: .334828,
  .279622, .194481 y .212140. No deben promediarse.
- **Archivo.** Microdatos/etiquetas del proyecto *Los mexicanos vistos por sí
  mismos* ya estaban en el corpus y el host HTTP del IIJ respondió en una
  adquisición anterior.[^10] **Parcial:** cuatro servicios, sin canal ni
  denominador conjunto de eventos.

### 3.7 ENCRIGE 2020, INEGI — empresa por tipo de trámite, sin canal comparable

- **Reactivo exacto.** 9.3 pregunta, para agilizar/realizar/evitar
  procedimientos o multas, si un servidor público “intentó apropiarse o le
  solicitó de forma directa algún beneficio (dinero, regalos o favores) que
  usted o esta empresa pudiera otorgarle”; incisos posteriores cubren coyote e
  insinuación.[^11]
- **Unidad / numerador / denominador.** Empresa y tipo de trámite/inspección;
  9.4–9.5 registran tipo y número de ocasiones. La sección 8 identifica quién
  hizo el trámite, no un medio transversal presencial/digital enlazable a cada
  conteo corrupto.
- **Periodo / diseño.** 2020; 34,919 unidades económicas, muestra
  probabilística estratificada con dominios nacional, estatal, tamaño, sector
  y 42 municipios.[^12]
- **Archivo.** Cuestionario y microdato ya estaban en el corpus. **Parcial:**
  empresas y ocasiones, sin canal de entrega equivalente.

### 3.8 World Bank Enterprise Survey México 2023 — soborno por tipo, sin canal

- **Reactivos.** El DDI etiqueta, entre otros: `c5` “Informal Gift/Payment
  Expected or Requested For An Electrical Connection?”, `g4` para permiso de
  construcción y `j15` para licencia de operación.[^13]
- **Unidad / denominador.** Establecimiento que solicitó/tuvo el contacto de
  cada tipo; numerador solicitud/expectativa de pago informal. Los indicadores
  agregan seis transacciones. No existe canal de realización del mismo evento.
- **Periodo / diseño.** Marzo–octubre 2023; 1,322 establecimientos; muestreo
  aleatorio estratificado por industria, tamaño y región; entrevista cara a
  cara y ponderadores publicados.[^14]
- **Archivo.** DDI y microdatos ya obtenidos bajo condiciones del repositorio.
  **Parcial:** universo empresarial y tipos de transacción, sin canal.

### 3.9 Institucionales y académicos adicionales

- **PROFEDET/ASF 2024.** Reactivo reportado: si “el servidor público solicitó
  dinero para agilizar su trámite”. Unidad: usuario de PROFEDET; numerador 38;
  denominador 15,812 cédulas aplicadas aleatoriamente; 2024; canal no
  registrado. El propio informe advierte que base, preguntas y reportes no se
  correspondían. PDF descargado. Parcial institucional.[^15]
- **Usuarios de servicios de justicia, UNAM-IIJ/AMIJ 2009.** Reactivo exacto:
  “¿alguien le pidió dinero o algún otro tipo de bien o servicio para agilizar
  alguno de los trámites?”. Encuesta nacional de salida en 100 tribunales,
  1,500 usuarios de 18+, septiembre de 2009; 2.2% sí; sin canal. El host no
  resolvió en `curl`, `wget` ni DoH al corte, así que no se registró un archivo
  vacío ni un mirror no autorizado.[^16]
- **SAT, encuesta telefónica 2025.** Informa 26 entrevistados (3.3% de la
  muestra analizada) que entregaron dinero a personal del SAT, entre
  contribuyentes con interacción reciente; CATI, muestra de 2,000, error
  ±2.2%, 95%. El “canal remoto” es el modo de levantamiento, no el canal del
  trámite corrupto. Parcial institucional.[^17]
- **LAPOP/ICPSR 36562.** Batería de soborno por servicios públicos, adultos en
  edad de votar, diseño probabilístico multietápico nacional; México está
  incluido en 2004–2014. No registra el canal del evento; archivos de uso
  restringido requieren DUA y no se intentó eludirlo.[^18]
- **Global Corruption Barometer, Transparencia Internacional.** Reporta pago
  de soborno entre usuarios de servicios y categorías institucionales para
  México, no canal del servicio. Parcial por persona/servicio.[^19]
- **OCDE Trust Survey 2023.** Para México pregunta la expectativa de que un
  empleado público rechace un soborno para acelerar un servicio: percepción
  hipotética, no experiencia/evento/canal.[^20]
- **BID User Survey on Government Transactions and Equity 2023–2024.** Tiene
  usuarios y canales de transacción, pero su lista de países no incluye
  México. `EXISTE-NO-SATISFACE` por geografía.[^21]
- **datos.gob.mx.** La encuesta de satisfacción de la Ventanilla Única tiene
  canal fijo en línea y un CSV de año/homoclave/pregunta/respuesta/frecuencia,
  pero no reactivo de soborno. SIDEC y buzones registran denuncias/canal de
  recepción, no el denominador de trámites elegibles. No satisfacen.[^22]
- **UNODC/INEGI.** El manual de encuestas de corrupción ofrece el patrón
  normativo de contacto y soborno para ODS 16.5.1, pero no observaciones
  mexicanas por canal.[^23]

## 4. Universo de búsqueda y respuestas observadas

| ruta | consulta/objeto | respuesta y decisión |
|---|---|---|
| INEGI ENCIG, RNM y estáticos | 2013–2025; cuestionario, estructura, microdato, tabulados; variantes `encig25_*` | fuente nacional; PDF correcto obtenido; dos variantes fueron *soft 404*; enlace evento-canal no unívoco |
| INEGI ENCRIGE / ENCUCI | cuestionarios, diccionarios, microdatos y páginas de programa | parciales sin canal de evento; payloads ya existentes |
| UNAM-IIJ | corrupción/cultura de legalidad y usuarios de justicia; HTTP/HTTPS | microdatos 2015 existentes; informe 2009 indexado, host AMIJ sin DNS al corte |
| SESEA Aguascalientes | ENEAC: base códigos/etiquetas/SAV, cuestionario, marco, método, reporte | seis payloads obtenidos; cruce evento×canal×solicitud, cobertura estatal/empresarial |
| datos.gob.mx / CKAN | `mordida`, `solicitaron dinero`, `corrupción trámite`, satisfacción en línea, SIDEC | índice web accesible; API `package_show` devolvió Access Denied; metadatos muestran satisfacción/quejas, no denominador exacto |
| Transparencia Mexicana / CIDE / Wayback | INCBG 2001–2010, “base de datos”, cuestionario, ZIP | informe 2010 obtenido; búsquedas CIDE sin depósito; CDX dirigido a ZIP devolvió `[]` |
| Banco Mundial | WBES México 2006/2010/2023, DDI y perfiles | soborno por seis transacciones; sin canal; archivos 2023 ya existentes |
| BID | Government Transactions and Equity, canales, México | producto pertinente, México ausente |
| OCDE | Trust Survey México 2023, corrupción/servicios | expectativa hipotética; no experiencia ni canal |
| ICPSR/LAPOP | México bribery/public services, 36562 | batería por servicios; sin canal; restricciones respetadas |
| Harvard Dataverse API | `Mexico bribery public services`, y búsquedas exactas por mordida/trámites | consulta amplia devolvió 105,424 resultados ruidosos; revisión dirigida no halló objeto exacto |
| Zenodo API | `"Mexico" AND (bribery OR mordida) AND "public services"` | total 0; resultados web cercanos eran compras públicas/artículos, no encuesta del objeto |
| OSF | API y búsqueda web con `Mexico bribery public services` | endpoint de búsqueda probado devolvió 404; búsqueda indexada no encontró candidato exacto |
| repositorios mexicanos / estatales / municipales | Aguascalientes, Baja California, Jalisco, Tabasco, Tijuana; soborno+agilizar trámite | ENEAC es el único cruce fuerte; demás son sondeos, indicadores o satisfacción institucional sin cobertura nacional/canal |
| buscadores secundarios | frases exactas, sinónimos `mordida`, `soborno`, `pago informal`, `agilizar`, `gestor/coyote`; inglés | sirvieron para descubrir ENEAC, MCCI, INCBG, PROFEDET y AMIJ; producto final verificado en productor cuando estuvo disponible |

También se inspeccionaron nombres/años alternativos, formatos CSV/XLSX/SAV/PDF,
endpoints de páginas dinámicas, catálogos y mirrors. No se usaron credenciales,
identidades, CAPTCHA, paywall o DUA ajenos.

## 5. Adquisiciones verificadas

Todos los archivos siguientes viven bajo
`data/raw/gen2_corrupcion_fuente_general/` y sus metadatos completos están en
`data/manifiesto.yaml`; el payload no se versiona en Git.

| id de manifiesto | bytes | SHA-256 | formato / origen / condición |
|---|---:|---|---|
| `encig25_cuestionario_pdf` | 2,060,955 | `807196d6aba5ee584fcc3710b6f01c6a43970b91c7f3c380f68109a4bd16bd33` | PDF, INEGI HTTPS, Términos de Libre Uso |
| `mcci_encuesta_corrupcion_impunidad_2019_2024_xlsx` | 4,109,327 | `ffa39bbb62e62a2dda0276f0120afbfeb37ad6c3c6b6e1f378a627642463372c` | XLSX, MCCI; página declara datos públicos/gratuitos |
| `incbg2010_informe_ejecutivo_pdf` | 1,213,893 | `68a00a843d0b837326fd1b5c4503689da0b72e336aea2295b108fc871dcc2f38` | PDF, Transparencia Mexicana; disponibilidad pública, sin inferir licencia adicional |
| `asf_profedet_auditoria_2024_0282_pdf` | 447,934 | `dd7bd4a1ef59e22fd4336f3050685ea02c42538a63b4a1ce4fad44bd33b4cdbf` | PDF público ASF |
| `eneac2021_tramites_codigos_xlsx` | 1,587,917 | `7b66456fc5f4fa098a026cacc72d0bef84ebaea92f5a8b3b932a426871cb13d1` | XLSX, SESEA Aguascalientes |
| `eneac2021_tramites_etiquetas_xlsx` | 1,582,860 | `95e4e3d9ba17a24b27b22149b5cbd01f4c6c5d21bb1271c100eb25ad668a3d82` | XLSX, SESEA Aguascalientes |
| `eneac2021_tramites_sav` | 1,496,623 | `99b3fdb3c09eaae8b06278eda418cd018dcfd8928229a32a2451f013ff8b4af8` | SPSS SAV, SESEA Aguascalientes |
| `eneac2021_cuestionario_pdf` | 857,096 | `10a0ab1ed70c581d5276ffa1a17a0b9707f3f112afbdc487f98576d7081a0404` | PDF, SESEA Aguascalientes |
| `eneac2021_nota_metodologica_pdf` | 3,457,056 | `2608f85c79db54dc38234cf866eb94edb7dc7fe98d6d632c27c0f9588251240d` | PDF, SESEA Aguascalientes |
| `eneac2021_reporte_grafico_pdf` | 12,218,528 | `81560e686086f7ad04f4ee8e7fb9e10054cfc645781660b107dd859467bd5a2c` | PDF, SESEA Aguascalientes |

## 6. Conclusión y solicitud externa exacta

`NC-0153` permanece abierta. La fila de adquisición pasa de selección seca a
`OBTENIDO-PARCIAL`: hay archivos reales y un candidato con el cruce correcto,
pero no se obtuvo el objeto nacional. ENCIG no debe repararse asignando la
primera/última fila; ENEAC no debe extrapolarse de Aguascalientes y dos sectores
a México; MCCI/INCBG no deben presentarse por canal.

Si el productor posee una tabla de enlace no publicada, la solicitud precisa
es la siguiente (se prepara, **no se envía**):

> Solicito identificar y, si es públicamente liberable, proporcionar el
> microdato anonimizado, cuestionario, diccionario, diseño muestral y
> ponderadores de una encuesta representativa de México que conserve un
> identificador único por cada evento de trámite, pago o solicitud; el canal
> por el cual se realizó ese mismo evento; una variable que indique si un
> servidor público, tercero/coyote solicitó o insinuó dinero, regalo o favor
> respecto de ese evento; y todos los eventos elegibles necesarios para el
> denominador, incluidos los negativos. Para ENCIG 2025, solicito en particular
> la llave o tabla que vincule cada conteo de 8.5 con `NT_TIPO`/`P7_3` cuando
> un `ID_TRA` contiene más de un evento. Indiquen periodo, universo, exclusiones,
> estratos, UPM, factor y condiciones de acceso. Si sólo existe bajo licencia o
> DUA, agradeceré el catálogo y procedimiento oficial; no se solicita remover
> controles de confidencialidad.

## Fuentes

[^1]: SESEA Aguascalientes, [publicaciones y descargas ENEAC 2021](https://seaaguascalientes.org/publicaciones/).
[^2]: INEGI, [ENCIG 2025](https://www.inegi.org.mx/programas/encig/2025/).
[^3]: INEGI, [Red Nacional de Metadatos, ENCIG 2023](https://www.inegi.org.mx/rnm/index.php/catalog/945).
[^4]: INEGI, [Cuestionario general ENCIG 2025](https://www.inegi.org.mx/contenidos/programas/encig/2025/doc/encig25_cuestionario.pdf).
[^5]: SESEA Aguascalientes, [Cuestionario ENEAC 2021](https://seaaguascalientes.org/publicaciones/docs/eneac_2021/ENEAC2021-Cuestionario.pdf).
[^6]: SESEA Aguascalientes, [Nota metodológica ENEAC 2021](https://seaaguascalientes.org/publicaciones/docs/eneac_2021/ENEAC2021-Nota_Metodologica.pdf).
[^7]: MCCI, [Encuesta Nacional sobre Corrupción e Impunidad 2019–2024](https://contralacorrupcion.mx/encuesta-nacional-mcci-corrupcion-e-impunidad/).
[^8]: Transparencia Mexicana, [Informe ejecutivo INCBG 2010](https://www.tm.org.mx/wp-content/uploads/2013/05/01-INCBG-2010-Informe-Ejecutivo1.pdf).
[^9]: INEGI, [ENCUCI 2020](https://www.inegi.org.mx/programas/encuci/2020/).
[^10]: IIJ-UNAM, [Los mexicanos vistos por sí mismos](http://www.losmexicanos.unam.mx/).
[^11]: INEGI, [Cuestionario ENCRIGE 2020](https://www.inegi.org.mx/contenidos/programas/encrige/2020/doc/encrige2020_cuestionario.pdf).
[^12]: INEGI, [ENCRIGE 2020](https://www.inegi.org.mx/programas/encrige/2020/).
[^13]: Banco Mundial, [catálogo WBES México 2023](https://microdata.worldbank.org/catalog/6453).
[^14]: World Bank Enterprise Surveys, [Mexico 2023 country profile](https://www.enterprisesurveys.org/content/dam/enterprisesurveys/documents/country/Mexico-2023.pdf).
[^15]: ASF, [Auditoría 282 a PROFEDET, Cuenta Pública 2024](https://www.asf.gob.mx/Trans/Informes/IR2024b/Documentos/Auditorias/2024_0282_a.pdf).
[^16]: AMIJ/IIJ-UNAM, [Encuesta de satisfacción de usuarios de servicios de justicia](https://amij.org.mx/wp-content/uploads/2022/12/03-satisfaccion_de_los_usuarios.pdf).
[^17]: SAT, [Anticorrupción: Encuesta Telefónica Nacional de Indicadores B 2025](https://www.sat.gob.mx/minisitio/Anticorrupcion/mecanismos.html).
[^18]: ICPSR, [LAPOP 2004–2015, estudio 36562](https://doi.org/10.3886/ICPSR36562.v1).
[^19]: Transparency International, [Global Corruption Barometer: Latin America and the Caribbean](https://www.transparency.org/en/gcb/latin-america/corruption-on-the-rise-in-latin-america-and-the-caribbean).
[^20]: OCDE, [Encuesta sobre los motores de la confianza 2024: México](https://www.oecd.org/es/publications/encuesta-de-la-ocde-sobre-los-motores-de-la-confianza-2024_85bdcdc0-es/mexico_3172b4a5-es.html).
[^21]: BID, [User Survey on Government Transactions and Equity 2023–2024](https://data.iadb.org/es/dataset/user-survey-on-government-transactions-and-equity-2023-2024).
[^22]: datos.gob.mx, [Encuesta de satisfacción de trámites en línea](https://www.datos.gob.mx/dataset/resultados_encuesta_satisfaccion_tramites_linea_ventanilla_unica_nacional) y [SIDEC](https://www.datos.gob.mx/es/dataset/quejas_denuncias_ciudadanas_sidec).
[^23]: UNODC/INEGI, [Manual de encuestas de corrupción](https://www.cdeunodc.inegi.org.mx/unodc/wp-content/uploads/2019/03/Manual-Corrupcion.pdf).
