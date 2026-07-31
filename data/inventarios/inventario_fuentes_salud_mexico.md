# Inventario de fuentes de datos — Salud, cuerpo y consumo de sustancias (México)

**Dominio:** estado de salud, acceso a servicios de salud, nutrición, alcohol y tabaco (y otras sustancias psicoactivas cuando el instrumento las incluye).
**Naturaleza del documento:** catálogo. No contiene resultados, nombres de variables, reactivos de cuestionario, juicios de calidad ni recomendaciones de uso.
**Fecha de compilación:** 30 de julio de 2026.
**Convención de marcado:**
- `[verificado]` = confirmado por consulta web en esta sesión.
- `[no verificado]` = la fuente existe, pero el dato específico no se confirmó aquí.

Orden: de mayor a menor cobertura poblacional.

---

## 1. Censo de Población y Vivienda

- **Nombre / siglas:** Censo de Población y Vivienda (Censo). Antecedentes en la serie: Conteo de Población y Vivienda (1995, 2005), Encuesta Intercensal (2015).
- **Institución:** Instituto Nacional de Estadística y Geografía (INEGI).
- **Periodicidad y ediciones:** decenal. Ediciones modernas: 1990, 2000, 2010, 2020. Levantamientos intermedios: 1995, 2005, 2015. Próxima edición decenal prevista para 2030 `[no verificado]`.
- **Cobertura:** nacional, con desagregación estatal, municipal y por localidad / AGEB. Enumeración universal (no muestral) con un cuestionario ampliado aplicado a una muestra probabilística. Transversal.
- **Tamaño de muestra:** universo poblacional completo; el cuestionario ampliado se aplica a una submuestra de viviendas `[no verificado — magnitud exacta no confirmada aquí]`.
- **Microdatos:** sí, muestra censal y archivos agregados descargables. Formatos habituales: CSV / DBF y archivos para paquetes estadísticos `[no verificado por edición]`.
- **Acceso:** descarga directa, sin registro `[no verificado para todos los productos]`.
- **URL:** https://www.inegi.org.mx/programas/ccpv/2020/
- **Licencia / términos:** Términos de Libre Uso de la Información del INEGI (uso libre con obligación de citar la fuente).
- **Relación con el dominio:** afiliación y derechohabiencia a servicios de salud; discapacidad. No mide consumo de sustancias ni nutrición.

---

## 2. Estadísticas de Defunciones Registradas (EDR)

- **Nombre / siglas:** Estadísticas de Defunciones Registradas (EDR). Anteriormente difundidas como Estadísticas Vitales — Mortalidad.
- **Institución:** INEGI, a partir de certificados de defunción del Registro Civil y Servicios Médicos Forenses, con confronta con la Secretaría de Salud `[verificado]`.
- **Periodicidad y ediciones:** anual. Serie disponible desde 1990; última edición localizada: datos 2024 `[verificado]`.
- **Cobertura:** nacional; desagregación por entidad, municipio y localidad, en tres ámbitos de referencia (registro, ocurrencia, residencia habitual) `[verificado]`. Registro administrativo censal, transversal por año.
- **Tamaño de muestra:** no aplica (registro exhaustivo).
- **Microdatos:** sí, descarga gratuita de archivos de microdatos `[verificado]`. Formatos habituales: CSV / DBF `[no verificado por año]`.
- **Acceso:** descarga directa gratuita, sin registro `[verificado]`.
- **URL:** https://www.inegi.org.mx/programas/edr/ — metadatos en https://www.inegi.org.mx/rnm/index.php/catalog/1140
- **Licencia / términos:** Términos de Libre Uso de la Información del INEGI.
- **Relación con el dominio:** causa de muerte codificada en CIE-10; incluye defunciones accidentales y violentas.

---

## 3. Estadísticas de Natalidad / Nacimientos registrados

- **Nombre / siglas:** Estadísticas de Natalidad (registros de nacimiento). Serie complementaria: Estadísticas de Nacimientos Registrados.
- **Institución:** INEGI (con base en Registro Civil); la Secretaría de Salud opera además su propio subsistema de nacimientos (SINAC) `[no verificado en detalle]`.
- **Periodicidad y ediciones:** anual; serie larga desde los años noventa `[no verificado en su extensión exacta]`.
- **Cobertura:** nacional, estatal y municipal. Registro administrativo, transversal.
- **Tamaño de muestra:** no aplica (registro).
- **Microdatos:** sí `[no verificado en esta sesión]`.
- **Acceso:** descarga directa `[no verificado]`.
- **URL:** https://www.inegi.org.mx/programas/natalidad/ `[no verificado — URL construida por analogía, confirmar]`
- **Licencia / términos:** Términos de Libre Uso de la Información del INEGI.
- **Relación con el dominio:** atención del parto, características de la madre y del recién nacido.

---

## 4. Sistema Nacional de Vigilancia Epidemiológica — Anuarios de Morbilidad

- **Nombre / siglas:** Anuarios de Morbilidad, derivados del Sistema Nacional de Vigilancia Epidemiológica (SINAVE) y de la Red Nacional de Vigilancia Epidemiológica (RENAVE); el componente de notificación semanal se conoce como SUIVE.
- **Institución:** Dirección General de Epidemiología (DGE), Secretaría de Salud `[verificado]`.
- **Periodicidad y ediciones:** anual; serie 1984–2024 en el portal de consulta `[verificado]`.
- **Cobertura:** nacional y estatal, con desagregación por grupo de edad, sexo, semana epidemiológica y fuente de notificación `[verificado]`. Registro administrativo agregado, transversal.
- **Tamaño de muestra:** no aplica (notificación de casos).
- **Microdatos:** el portal difunde tabulados; existen bases en datos abiertos para los anuarios 2015–2017 y para eventos específicos (influenza, COVID-19, virus respiratorios) `[verificado]`. Microdatos caso a caso para toda la serie: `[no verificado]`.
- **Acceso:** consulta y descarga abiertas, sin registro `[verificado]`.
- **URL:** https://epidemiologia.salud.gob.mx/anuario/html/index.html y https://www.gob.mx/salud/acciones-y-programas/anuarios-de-morbilidad-1984-a-2024
- **Licencia / términos:** Términos de Libre Uso de Datos Abiertos de la DGE `[verificado — existencia del documento de términos]`.
- **Relación con el dominio:** incidencia de padecimientos sujetos a vigilancia.

---

## 5. Subsistema Automatizado de Egresos Hospitalarios (SAEH)

- **Nombre / siglas:** Subsistema Automatizado de Egresos Hospitalarios (SAEH), integrado al Sistema de Información de la Secretaría de Salud / SINBA.
- **Institución:** Dirección General de Información en Salud (DGIS), Secretaría de Salud `[verificado]`.
- **Periodicidad y ediciones:** cortes mensuales preliminares y cierre definitivo anual `[verificado]`. Series publicadas desde 2000 en cubos dinámicos; bases de datos abiertos anuales localizadas desde 2008 `[verificado]`. Cifras de años recientes marcadas como preliminares o definitivas según el año `[verificado]`.
- **Cobertura:** unidades hospitalarias del sector; desagregación por entidad y por unidad médica (clave CLUES) `[verificado]`. Registro administrativo, transversal por egreso.
- **Tamaño de muestra:** no aplica (registro de egresos).
- **Microdatos:** sí, bases anuales de datos abiertos, además de cubos dinámicos para consulta agregada `[verificado]`. Formatos habituales: CSV comprimido y bases para consulta OLAP `[no verificado por año]`.
- **Acceso:** descarga abierta sin registro `[verificado]`.
- **URL:** http://www.dgis.salud.gob.mx/contenidos/basesdedatos/da_egresoshosp_gobmx.html · cubos: https://sinba.salud.gob.mx/CubosDinamicos · réplica en https://www.datos.gob.mx/dataset/datos_egresos_hospitalarios
- **Licencia / términos:** Términos de Libre Uso de Datos Abiertos de la DGIS; en datos.gob.mx, Libre Uso MX con obligación de citar fuente y liga `[verificado en cuanto a la existencia de esas condiciones]`.
- **Relación con el dominio:** afecciones tratadas, procedimientos, lesiones, atención obstétrica, defunción hospitalaria.

---

## 6. Otros subsistemas de la DGIS (cubos dinámicos y datos abiertos)

- **Nombre / siglas:** Sistema de Información de la Secretaría de Salud / SINBA. Componentes difundidos: Servicios Otorgados, Urgencias, Lesiones, Establecimientos de Salud (CLUES), Recursos (base del Boletín Estadístico de Información en Salud, BEIS), Defunciones, Nacimientos, Población.
- **Institución:** DGIS, Secretaría de Salud `[verificado — listado de componentes]`.
- **Periodicidad y ediciones:** anual, con cortes preliminares; series desde inicios de los 2000 según componente `[no verificado por componente]`.
- **Cobertura:** nacional, estatal, por unidad médica. Registros administrativos, transversales.
- **Tamaño de muestra:** no aplica.
- **Microdatos:** varía por componente; algunos como bases descargables, otros solo como cubo de consulta `[no verificado por componente]`.
- **Acceso:** abierto, sin registro `[no verificado por componente]`.
- **URL:** https://sinba.salud.gob.mx/CubosDinamicos · http://www.dgis.salud.gob.mx/
- **Licencia / términos:** Términos de Libre Uso de Datos Abiertos de la DGIS `[no verificado por componente]`.
- **Relación con el dominio:** oferta de servicios, infraestructura, recursos humanos, atención de urgencias y lesiones.

---

## 7. Encuesta Nacional de Ingresos y Gastos de los Hogares (ENIGH)

- **Nombre / siglas:** Encuesta Nacional de Ingresos y Gastos de los Hogares (ENIGH). La edición 2024 se difunde como "Nueva serie" `[verificado]`.
- **Institución:** INEGI.
- **Periodicidad y ediciones:** bienal en la serie reciente (2016, 2018, 2020, 2022, 2024); serie histórica desde 1984 con periodicidad irregular `[no verificado en su totalidad]`. La ENIGH 2024 se publicó el 30 de julio de 2025 `[verificado]`.
- **Cobertura:** nacional, con desagregación por entidad federativa y por ámbito urbano/rural. Transversal (no panel).
- **Tamaño de muestra:** del orden de 10⁵ viviendas en las ediciones recientes `[no verificado — magnitud exacta de 2024 no confirmada aquí]`.
- **Microdatos:** sí, bases descargables por tabla (viviendas, hogares, personas, gastos, ingresos). Formatos: CSV y bases para paquetes estadísticos `[no verificado por edición]`.
- **Acceso:** descarga directa gratuita, sin registro `[no verificado para 2024]`.
- **URL:** https://www.inegi.org.mx/programas/enigh/nc/2024/ — metadatos en https://www.inegi.org.mx/rnm/index.php/catalog/1116
- **Licencia / términos:** Términos de Libre Uso de la Información del INEGI.
- **Relación con el dominio:** gasto de los hogares en salud; gasto en alimentos, bebidas y tabaco; acceso a la alimentación; derechohabiencia; discapacidad `[verificado en cuanto a la existencia de estos temas en el diseño conceptual]`.

---

## 8. Encuesta Nacional de Salud y Nutrición (ENSANUT) y ENSANUT Continua

- **Nombre / siglas:** Encuesta Nacional de Salud y Nutrición (ENSANUT); modalidad anual vigente: ENSANUT Continua. Variantes con nombre propio: ENSANUT-MC 2016 (Medio Camino), ENSANUT-100K 2018 (localidades de menos de 100 mil habitantes), ENSANUT Continua COVID-19 (2020), sobremuestras estatales (p. ej. Guanajuato, Nuevo León) y sobremuestra de población derechohabiente del ISSSTE en 2021–2025 `[verificado]`.
- **Institución:** Instituto Nacional de Salud Pública (INSP), en el marco del Sistema Nacional de Encuestas de Salud, con la Secretaría de Salud `[verificado]`. Antecedentes de la familia de encuestas de salud desde 1986 `[verificado]`.
- **Periodicidad y ediciones:** ediciones mayores en 2000, 2006, 2012, 2016 (MC), 2018–2019 y 2018 (100K); modalidad continua anual 2020, 2021, 2022, 2023, 2024 y 2025 `[verificado]`. La edición 2024 fue descrita como la quinta continua y 2023 como la cuarta de cinco `[verificado]`.
- **Cobertura:** nacional, con representatividad de las 32 entidades federativas mediante acumulación de las rondas continuas 2020–2024 `[verificado]`; ámbito urbano y rural. Transversal repetida; no es panel.
- **Tamaño de muestra:** varía por edición. ENSANUT 2018, componente de salud: 50 000 viviendas distribuidas en las 32 entidades `[verificado]`. Rondas continuas anuales: menor magnitud, diseñadas para acumularse `[no verificado — cifras por año no confirmadas aquí]`.
- **Microdatos:** sí. El sitio ofrece descarga de bases de datos y cuestionarios por edición y por módulo `[verificado]`. Formatos habituales: bases para paquetes estadísticos y CSV `[no verificado por edición]`. Existe además catalogación tipo DDI para algunas ediciones `[verificado]`.
- **Acceso:** descarga directa desde la página de descargas de cada edición, sin registro aparente `[verificado en cuanto al mecanismo de descarga]`.
- **URL:** https://ensanut.insp.mx/ · descargas por edición, p. ej. https://ensanut.insp.mx/encuestas/ensanutcontinua2024/index.php · tablero IDEAS-ENSANUT en el mismo dominio.
- **Licencia / términos:** condiciones de datos abiertos federales (Libre Uso MX): citar el nombre del conjunto de datos, la dependencia, la liga y la fecha de consulta; no alterar el sentido de la información; no aparentar respaldo oficial `[verificado para ediciones publicadas en el catálogo federal]`.
- **Relación con el dominio:** estado de salud, enfermedades crónicas, mediciones antropométricas y de presión arterial, muestras biológicas (anemia, micronutrimentos, plomo, serología vacunal), nutrición y consumo de alimentos, utilización y cobertura de servicios de salud, y módulos sobre consumo de tabaco y alcohol `[verificado en cuanto a la presencia de estos temas]`.

---

## 9. Encuesta Nacional de la Dinámica Demográfica (ENADID)

- **Nombre / siglas:** Encuesta Nacional de la Dinámica Demográfica (ENADID).
- **Institución:** INEGI. Referentes metodológicos: programa de Encuestas de Salud Reproductiva (RHS) y uso por USAID `[verificado]`.
- **Periodicidad y ediciones:** aproximadamente quinquenal: 1992, 1997, 2006, 2009, 2014, 2018, 2023 `[verificado para 2018 y 2023; ediciones previas no verificadas en esta sesión]`.
- **Cobertura:** nacional con desagregación por entidad federativa; ámbito urbano y rural. Transversal.
- **Tamaño de muestra:** del orden de 10⁴–10⁵ viviendas `[no verificado]`.
- **Microdatos:** sí `[no verificado en esta sesión para 2023]`. Formatos habituales: CSV y bases para paquetes estadísticos.
- **Acceso:** descarga directa `[no verificado]`.
- **URL:** https://www.inegi.org.mx/programas/enadid/2023/ — metadatos en https://www.inegi.org.mx/rnm/index.php/catalog/981
- **Licencia / términos:** Términos de Libre Uso de la Información del INEGI.
- **Relación con el dominio:** salud materno-infantil, atención prenatal, uso de métodos anticonceptivos, infecciones de transmisión sexual, discapacidad `[verificado en cuanto a la presencia de estos temas]`.

---

## 10. Encuesta Nacional de Consumo de Drogas, Alcohol y Tabaco (ENCODAT) y la serie ENA

- **Nombre / siglas:** Encuesta Nacional de Consumo de Drogas, Alcohol y Tabaco (ENCODAT). Serie predecesora: Encuesta Nacional de Adicciones (ENA).
- **Institución:** en 2025, esfuerzo conjunto de la Comisión Nacional de Salud Mental y Adicciones (CONASAMA), el Instituto Nacional de Psiquiatría "Ramón de la Fuente Muñiz" (INPRFM) y el INSP, bajo la Secretaría de Salud `[verificado]`. Las primeras ediciones fueron dirigidas por la Dirección General de Epidemiología y el entonces Instituto Mexicano de Psiquiatría `[verificado]`.
- **Periodicidad y ediciones:** irregular. Serie: 1988, 1993, 1998, 2002, 2008, 2011, 2016(–2017) y 2025 `[verificado]`. Levantamiento de la edición 2025: del 2 de julio al 10 de octubre de 2025 `[verificado]`; difusión de resultados en enero de 2026 `[verificado]`.
- **Cobertura:** nacional y regional, población de 12 a 65 años en hogares. Las tres primeras ediciones fueron solo urbanas; desde 2002 incluyen zonas rurales `[verificado]`. La edición 2016 tuvo además representatividad estatal `[no verificado]`. Transversal repetida; no es panel.
- **Tamaño de muestra:** ENCODAT 2025 — diseño previsto de 23 950 viviendas; muestra efectiva reportada de 3 847 personas de 12 a 17 años y 15 353 de 18 a 65 años `[verificado]`. Ediciones anteriores: `[no verificado]`.
- **Microdatos:** `[no verificado]`. La difusión localizada de la edición 2025 consiste en informe completo y resumen ejecutivo en PDF; no se confirmó aquí la existencia de bases descargables. Para ediciones previas, la distribución histórica se ha hecho por los sitios del INPRFM y de CONADIC/CONASAMA `[no verificado]`.
- **Acceso:** informes de acceso abierto; para microdatos, mecanismo `[no verificado — podría requerir solicitud institucional]`.
- **URL:** https://encuestas.insp.mx/repositorio/encuestas/ENCODAT2025/ · https://portal.insp.mx/control-tabaco/epidemiologia/encuesta-nacional-de-consumo-de-drogas-alcohol-y-tabaco-2025 · informe en https://www.gob.mx/cms/uploads/attachment/file/1044513/ENCODAT_-_COMPLETO.pdf
- **Licencia / términos:** `[no verificado]`. Publicaciones bajo términos de la Secretaría de Salud / INSP.
- **Relación con el dominio:** consumo de tabaco fumado y de cigarro electrónico, alcohol, drogas médicas fuera de prescripción y drogas ilegales; salud mental; comportamiento de juego con apuestas; uso problemático de videojuegos `[verificado en cuanto a la presencia de estas secciones en 2025]`.

---

## 11. Encuesta Nacional sobre Salud y Envejecimiento en México (ENASEM / MHAS)

- **Nombre / siglas:** Encuesta Nacional sobre Salud y Envejecimiento en México (ENASEM); en inglés, Mexican Health and Aging Study (MHAS). Submuestra especializada: Mex-Cog (protocolo armonizado HCAP) `[verificado]`.
- **Institución:** INEGI en colaboración con la Universidad de Texas (UTMB y, en la ronda 2024, el Centro de Ciencias de la Salud en San Antonio), Universidad de Wisconsin, UCLA, el Instituto Nacional de Geriatría (INGER) y el INSP; financiamiento parcial del National Institute on Aging `[verificado]`.
- **Periodicidad y ediciones:** longitudinal con rondas en 2001, 2003, 2012, 2015, 2018, 2021 y 2024; octava ronda prevista para 2027 `[verificado]`. Incorpora cohortes de reemplazo en varias rondas `[verificado]`.
- **Cobertura:** nacional, con representación urbana y rural, población de 50 años y más `[verificado]`. **Panel** (único estudio longitudinal nacional de este tipo en el país según el propio INEGI) `[verificado]`. Incluye entrevistas con informantes sustitutos y entrevistas post-mortem con familiares `[verificado]`.
- **Tamaño de muestra:** ronda 2024 — 23 044 personas, de las cuales 17 043 de seguimiento y 6 001 de reemplazo `[verificado]`.
- **Microdatos:** sí, tanto en el sitio del proyecto (mhasweb.org) como en el sitio del INEGI `[no verificado para todas las rondas]`. Formatos habituales: bases para paquetes estadísticos y archivos delimitados `[no verificado]`.
- **Acceso:** el sitio del proyecto opera con registro de usuario para descarga de archivos `[no verificado en esta sesión]`. La vía INEGI es de descarga directa `[no verificado]`.
- **URL:** https://www.mhasweb.org/ · https://www.inegi.org.mx/programas/enasem/2024/ · metadatos de 2021 en https://www.inegi.org.mx/rnm/index.php/catalog/861
- **Licencia / términos:** por la vía INEGI, Términos de Libre Uso de la Información del INEGI; por la vía del proyecto, términos propios de uso de datos con requisito de citación `[no verificado]`.
- **Relación con el dominio:** salud autorreportada, enfermedades crónicas, síntomas, funcionalidad, depresión, cognición, medidas preventivas, atención médica, estilo de vida `[verificado en cuanto a la presencia de estos dominios]`.

---

## 12. Encuesta Global de Tabaquismo en Adultos (GATS)

- **Nombre / siglas:** Encuesta Global de Tabaquismo en Adultos — Global Adult Tobacco Survey (GATS), México.
- **Institución:** INSP, con coordinación de CONASAMA (en 2015, CONADIC) y asistencia técnica de OPS/OMS y de los CDC de Estados Unidos; financiamiento de la Iniciativa Bloomberg en las primeras ediciones `[verificado]`.
- **Periodicidad y ediciones:** 2009, 2015 y 2023 `[verificado]`.
- **Cobertura:** nacional, población de 15 años y más en hogares, con estratos urbano, semiurbano y rural; diseño por conglomerados estratificado y polietápico `[verificado]`. Transversal repetida.
- **Tamaño de muestra:** 2009 — 13 617 entrevistas; 2015 — 14 664 entrevistas `[verificado]`. 2023 — `[no verificado]`.
- **Microdatos:** `[no verificado]`. El protocolo GATS forma parte del Global Tobacco Surveillance System, cuyos datos se difunden por los CDC; la modalidad de acceso para México no se confirmó aquí.
- **Acceso:** informes de acceso abierto; microdatos posiblemente por solicitud o registro en el repositorio del GTSS `[no verificado]`.
- **URL:** https://portal.insp.mx/control-tabaco/proyecto/encuesta-global-de-tabaquismo-en-adultos-gats-mexico-2023 · hoja comparativa en https://www.gob.mx/cms/uploads/attachment/file/874574/Encuesta_Global_de_Tabaquismo_en_adultos_GATS_Hoja_de_Comparacion.pdf
- **Licencia / términos:** `[no verificado]`.
- **Relación con el dominio:** consumo de tabaco, cesación, exposición a humo de tabaco ajeno, advertencias sanitarias, publicidad, indicadores MPOWER.

---

## 13. Sistema de Vigilancia Epidemiológica de las Adicciones (SISVEA)

- **Nombre / siglas:** Sistema de Vigilancia Epidemiológica de las Adicciones (SISVEA).
- **Institución:** Dirección General de Epidemiología (DGE) / Dirección de Investigación Epidemiológica (DIE), Secretaría de Salud `[verificado]`. Información complementaria concentrada por CONASAMA `[verificado]`.
- **Periodicidad y ediciones:** informes anuales; serie desde 1994 en el componente de centros de tratamiento no gubernamentales `[verificado]`. Informe más reciente localizado: SISVEA 2024, publicado el 29 de enero de 2026 `[verificado]`.
- **Cobertura:** nacional con desagregación por entidad federativa `[verificado]`. Registro administrativo de población usuaria que acude a fuentes centinela (centros de tratamiento y rehabilitación gubernamentales y no gubernamentales, y otras fuentes) — **no es una muestra probabilística de población general**. Transversal por año.
- **Tamaño de muestra:** no aplica en sentido muestral; el volumen corresponde a solicitudes de atención registradas `[verificado en cuanto al tipo de conteo]`.
- **Microdatos:** `[no verificado]`. La difusión localizada es por informes anuales en PDF.
- **Acceso:** informes de acceso abierto sin registro `[verificado]`.
- **URL:** https://www.gob.mx/salud/documentos/informes-anuales-del-sistema-de-vigilancia-epidemiologica-de-las-adicciones
- **Licencia / términos:** Términos de Libre Uso de Datos Abiertos de la DGE `[no verificado para este componente]`.
- **Relación con el dominio:** droga de inicio y droga de impacto, perfil sociodemográfico de la población en tratamiento.

---

## 14. Encuesta Nacional de Consumo de Drogas en Estudiantes (ENCODE)

- **Nombre / siglas:** Encuesta Nacional de Consumo de Drogas en Estudiantes (ENCODE). Antecedentes y encuestas afines de cobertura subnacional: encuesta en estudiantes de la Ciudad de México (2012), Estado de México (2009), Jalisco (2009) `[verificado en cuanto a su existencia]`.
- **Institución:** INPRFM, con CONADIC (hoy CONASAMA), Secretaría de Salud y SEP `[verificado]`.
- **Periodicidad y ediciones:** irregular. Edición nacional confirmada: 2014 (publicada en 2015) `[verificado]`. Ediciones posteriores: `[no verificado]`.
- **Cobertura:** las 32 entidades federativas; estudiantes de 5.º y 6.º de primaria, secundaria y bachillerato `[verificado]`. Transversal, con base en muestra escolar.
- **Tamaño de muestra:** 166 535 estudiantes en 2014 `[verificado]`.
- **Microdatos:** `[no verificado]`. La difusión localizada consiste en reportes nacionales y estatales en PDF (reportes separados de tabaco, alcohol y drogas).
- **Acceso:** reportes de acceso abierto; microdatos `[no verificado — posiblemente por solicitud al INPRFM]`.
- **URL:** http://omextad.salud.gob.mx/contenidos/encuestas/encode2014/index.html · reporte en https://www.gob.mx/cms/uploads/attachment/file/239256/ENCODE_DROGAS_2014.pdf
- **Licencia / términos:** `[no verificado]`.
- **Relación con el dominio:** consumo de tabaco, alcohol y drogas ilegales en población escolar.

---

## 15. Encuesta Nacional de Niños, Niñas y Mujeres (ENIM / MICS México)

- **Nombre / siglas:** Encuesta Nacional de Niños, Niñas y Mujeres (ENIM), aplicación mexicana de las Multiple Indicator Cluster Surveys (MICS) de UNICEF.
- **Institución:** INSP con UNICEF México `[no verificado en esta sesión]`.
- **Periodicidad y ediciones:** edición 2015 `[no verificado]`. Ediciones posteriores: `[no verificado]`.
- **Cobertura:** nacional `[no verificado]`. Transversal.
- **Tamaño de muestra:** `[no verificado]`.
- **Microdatos:** las MICS suelen distribuir microdatos mediante solicitud registrada en el portal global de UNICEF `[no verificado para México]`.
- **Acceso:** `[no verificado — probable registro/solicitud]`.
- **URL:** `[no verificado]` — punto de partida sugerido: portal MICS de UNICEF y sitio del INSP.
- **Licencia / términos:** `[no verificado]`.
- **Relación con el dominio:** nutrición infantil, lactancia, atención a la salud materno-infantil, vacunación.

---

## 16. Encuesta Nacional sobre Niveles de Vida de los Hogares (ENNViH / MxFLS)

- **Nombre / siglas:** Encuesta Nacional sobre Niveles de Vida de los Hogares (ENNViH); Mexican Family Life Survey (MxFLS).
- **Institución:** Universidad Iberoamericana y Centro de Investigación y Docencia Económicas (CIDE), con colaboraciones internacionales `[no verificado en esta sesión]`.
- **Periodicidad y ediciones:** longitudinal; rondas en 2002, 2005–2006 y 2009–2012 `[no verificado]`. Rondas posteriores: `[no verificado]`.
- **Cobertura:** nacional, urbano y rural. **Panel** de hogares e individuos, con seguimiento de migrantes `[no verificado en detalle]`.
- **Tamaño de muestra:** `[no verificado]`.
- **Microdatos:** sí, con registro de usuario en el sitio del proyecto `[no verificado en esta sesión]`.
- **Acceso:** requiere registro / aceptación de términos `[no verificado]`.
- **URL:** `[no verificado]` — sitio histórico del proyecto: ennvih-mxfls.org
- **Licencia / términos:** `[no verificado]`.
- **Relación con el dominio:** estado de salud autorreportado, mediciones antropométricas, uso de servicios de salud, consumo de tabaco y alcohol `[no verificado en detalle]`.

---

## 17. Módulos y encuestas complementarias del INEGI con contenido parcial del dominio

Se listan agrupados porque su contenido sobre el dominio es modular, no central.

| Instrumento | Institución | Ediciones | Cobertura | Microdatos | Contenido pertinente |
|---|---|---|---|---|---|
| Encuesta Nacional de Bienestar Autorreportado (ENBIARE) | INEGI | 2021 `[no verificado si hay ediciones posteriores]` | Nacional, transversal | `[no verificado]` | Bienestar subjetivo, salud mental autorreportada |
| Módulo de Práctica Deportiva y Ejercicio Físico (MOPRADEF) | INEGI | Serie semestral/anual `[no verificado]` | Nacional urbano (áreas de 32 ciudades) `[no verificado]` | `[no verificado]` | Actividad física |
| Encuesta Nacional de Calidad e Impacto Gubernamental (ENCIG) | INEGI | Bienal `[no verificado]` | Nacional, transversal | `[no verificado]` | Experiencia y satisfacción con servicios públicos de salud |
| Encuesta Nacional sobre la Dinámica de las Relaciones en los Hogares (ENDIREH) | INEGI | 2003, 2006, 2011, 2016, 2021 `[no verificado]` | Nacional y estatal, transversal | `[no verificado]` | Consecuencias en salud física y emocional de la violencia |
| Encuesta Nacional de Ocupación y Empleo (ENOE) | INEGI | Trimestral continua | Nacional y estatal; panel rotatorio de viviendas | `[no verificado]` | Acceso a instituciones de salud por condición laboral |
| Cuenta Satélite del Sector Salud de México | INEGI | Anual `[no verificado]` | Nacional, series macro | No aplica (series agregadas) | Gasto en salud por función y agente |

Punto de entrada común: https://www.inegi.org.mx/datos/ y la Red Nacional de Metadatos, https://www.inegi.org.mx/rnm/
Licencia común: Términos de Libre Uso de la Información del INEGI.

---

## 18. Series derivadas y compilaciones de terceros

- **Bases estandarizadas de la Unidad de Inteligencia en Salud Pública (UISP), INSP.** Compilaciones armonizadas de series largas construidas sobre fuentes oficiales: defunciones registradas INEGI 1990–2024 y egresos hospitalarios de la Secretaría de Salud 2008–2024 `[verificado]`. Catálogo con metadatos y descarga: https://riisp.insp.mx/nada/ `[verificado]`. Términos: se solicita citar la fuente en forma específica `[verificado]`. No son fuentes primarias.
- **Medición multidimensional de la pobreza (CONEVAL).** Serie bienal derivada de la ENIGH que incluye una carencia por acceso a servicios de salud y otra por acceso a la alimentación nutritiva y de calidad. Institución: Consejo Nacional de Evaluación de la Política de Desarrollo Social. Microdatos: bases de cálculo y programas de replicación descargables `[no verificado]`. URL: https://www.coneval.org.mx/ `[no verificado]`.
- **Plataforma Nacional de Datos Abiertos.** Agregador federal donde se replican varios de los conjuntos anteriores. URL: https://www.datos.gob.mx/ `[verificado]`. Términos: Libre Uso MX `[verificado]`.
- **Repositorios internacionales** (OMS Global Health Observatory, OPS, Banco Mundial, IHME/GBD, OCDE Health Statistics): series agregadas para México derivadas o modeladas a partir de fuentes nacionales. No son fuentes primarias mexicanas. `[no verificado en esta sesión]`.

---

# Fuentes que probablemente existen pero no pudieron confirmarse

Se listan como pistas de verificación, no como hallazgos.

1. **Encuesta Nacional de Salud en Escolares (ENSE).** Se tiene noticia de una edición alrededor de 2008 a cargo del INSP. No confirmada aquí; no se localizó una serie continua.
2. **Encuesta Mundial de Tabaquismo en Jóvenes (GYTS / EMTA Jóvenes).** Componente escolar del Global Tobacco Surveillance System. Es plausible que México haya participado en varias rondas, pero no se confirmaron ediciones, cobertura ni difusión de datos.
3. **Global School-based Student Health Survey (GSHS).** Participación de México no confirmada.
4. **Encuesta Nacional de Epidemiología Psiquiátrica (ENEP, ~2003) y posibles sucesoras de salud mental.** El informe de ENCODAT 2025 indica que en esa edición se incorporó un bloque amplio de salud mental, lo que sugiere que no ha existido una serie nacional independiente y periódica de salud mental. No verificado.
5. **Ediciones de ENCODE posteriores a 2014.** No se localizaron. Podría existir una edición escolar reciente vinculada a CONASAMA o a la SEP.
6. **Registro Nacional de Cáncer.** Existe un mandato legal para su creación. Estado operativo actual, cobertura y difusión de datos: no verificados.
7. **Sistema de Vigilancia Epidemiológica de Patologías Bucales (SIVEPAB).** Se tiene noticia de informes anuales de la Secretaría de Salud. No verificado.
8. **Sistema de Cuentas en Salud a Nivel Federal y Estatal (SICUENTAS) y Boletín Estadístico de Información en Salud (BEIS), DGIS.** Muy probablemente vigentes como productos de la DGIS, pero no se confirmaron ediciones ni formato de difusión.
9. **Subsistema de Información sobre Nacimientos (SINAC), Secretaría de Salud.** Distinto de la estadística de natalidad del INEGI. Existencia probable; cobertura y acceso no verificados.
10. **Registros administrativos propios del IMSS y del ISSSTE** (derechohabiencia, morbilidad atendida, consultas). Los institutos publican anuarios y memorias estadísticas; la disponibilidad de microdatos no fue verificada.
11. **Encuestas estatales de adicciones y de salud.** Existen levantamientos estatales y sobremuestras (algunas de ellas asociadas a ENSANUT Continua, confirmadas para Guanajuato, Nuevo León y Sonora). Un inventario estatal completo no se intentó aquí.
12. **Encuestas nacionales de consumo de alimentos independientes de ENSANUT.** No se localizó ninguna. Es posible que el consumo alimentario se capte únicamente dentro de ENSANUT y de la ENIGH.
13. **Encuestas de salud y nutrición focalizadas en población indígena o afromexicana.** Posible existencia de estudios específicos del INSP o del INPI. No verificado.
14. **Observatorio Mexicano de Salud Mental y Consumo de Drogas** (sucesor del Observatorio Mexicano de Tabaco, Alcohol y otras Drogas, OMEXTAD). El dominio omextad.salud.gob.mx aloja materiales históricos; el estado actual del observatorio y qué series propias publica no fueron verificados.
15. **Encuesta Nacional de Consumo de Sustancias en Población Privada de la Libertad.** La Encuesta Nacional de Población Privada de la Libertad (ENPOL, INEGI) probablemente incluye contenido de salud y consumo. No verificado en esta sesión.
16. **Cédulas de supervisión y directorio de establecimientos de tratamiento de adicciones (CONASAMA).** Existe un directorio de establecimientos especializados reconocido por CONASAMA. Formato de publicación y disponibilidad como base de datos: no verificados.

---

## Notas de método

- Las URL se transcriben tal como aparecieron en resultados de búsqueda o en los propios sitios institucionales. Varias del dominio `dgis.salud.gob.mx` aparecen bajo `http`, no `https`.
- Cuando una fuente tiene dos vías de acceso (por ejemplo ENASEM, disponible vía INEGI y vía el sitio del proyecto), los términos de uso y el requisito de registro pueden diferir según la vía.
- Los términos de uso de los conjuntos publicados en el catálogo federal siguen la fórmula "Libre Uso MX", que impone obligación de citación con liga y fecha de consulta, prohibición de alterar el sentido de la información y prohibición de aparentar respaldo oficial.
- No se verificó, para ninguna fuente, la estructura interna de los archivos ni el contenido de los cuestionarios.
