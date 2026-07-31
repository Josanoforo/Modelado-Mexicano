# Inventario de fuentes de datos — Crédito, ahorro y finanzas del hogar en México

**Dominio:** crédito, ahorro y finanzas del hogar — inclusión financiera, uso de crédito formal e informal, ahorro, morosidad, medios de pago.

**Alcance de este documento:** catalogación de instrumentos. No contiene nombres ni claves de variable, no cita reactivos de cuestionario, no reporta cifras de resultados, no afirma posibilidades de cruce o análisis, y no clasifica las fuentes por calidad ni recomienda ninguna.

**Criterio de orden:** amplitud del universo cubierto. Primero registros de cobertura censal del sistema financiero; luego encuestas en hogares según universo y desagregación geográfica declarada; al final universos restringidos.

**Estado de verificación:** verificado por búsqueda web salvo donde se indique "no verificado".

**Fecha de compilación:** 30 de julio de 2026.

---

## A. Registros administrativos y series oficiales (cobertura censal del universo regulado)

### 1. Bases de Datos de Inclusión Financiera (BDIF)

- **Institución responsable:** Comisión Nacional Bancaria y de Valores (CNBV), Dirección General para el Acceso a Servicios Financieros.
- **Periodicidad y ediciones:** trimestral. Series desde 2009; última edición verificada con cierre de 2024.
- **Cobertura:** nacional, estatal y municipal. Incluye banca múltiple y de desarrollo, sociedades cooperativas de ahorro y préstamo y sociedades financieras populares. Serie transversal repetida; no es panel de personas.
- **Contenido temático:** infraestructura (sucursales, cajeros automáticos, terminales punto de venta), tenencia de productos de captación y de crédito, cuentas ligadas a teléfono celular y transacciones. En el cuarto trimestre se agrega información de seguros, ahorro para el retiro y protección al consumidor.
- **Tamaño de muestra:** no aplica (registro regulatorio, no muestreo).
- **Microdatos:** no publica microdatos a nivel persona. Publica bases agregadas descargables en hoja de cálculo.
- **Acceso:** abierto, sin registro ni solicitud.
- **URL:** https://www.gob.mx/cnbv/acciones-y-programas/bases-de-datos-de-inclusion-financiera · https://www.cnbv.gob.mx/Inclusión/Paginas/Bases-de-Datos.aspx
- **Licencia:** no declarada de forma explícita en la página; se distribuye dentro del marco de datos abiertos del Gobierno de México (Libre Uso MX) — **no verificado**.

### 2. Portafolio de Información (PI)

- **Institución responsable:** CNBV.
- **Periodicidad y ediciones:** periódica, mensual o trimestral según reporte. Cartera comercial bajo IFRS9 a partir de 2022; metodología de pérdida esperada de enero 2016 a diciembre 2021.
- **Cobertura:** nacional, por sector y por entidad supervisada. Series de cartera de crédito (incluidas consumo y vivienda) e información de situación financiera. Transversal repetido.
- **Tamaño de muestra:** no aplica.
- **Microdatos:** no a nivel persona; sí descarga de tablas por entidad y periodo. Desde diciembre de 2023 los portafolios de consulta y de exportación se consolidaron en un solo sitio.
- **Acceso:** abierto, sin registro.
- **URL:** https://portafolioinfo.cnbv.gob.mx/Paginas/Inicio.aspx
- **Licencia:** no verificada. La CNBV advierte que la información está sujeta a revisión continua por reenvíos de las entidades supervisadas.

### 3. Ahorro Financiero y Financiamiento en México (reportes y bases)

- **Institución responsable:** CNBV.
- **Periodicidad y ediciones:** trimestral. Ediciones recientes verificadas: cifras a marzo, junio, septiembre y diciembre de 2025.
- **Cobertura:** nacional, con reportes adicionales a nivel municipal y metodologías publicadas para las bases nacional y municipal. Transversal repetido.
- **Contenido temático:** componentes del ahorro financiero (captación de intermediarios, tenencia de valores de renta fija y certificados bursátiles fiduciarios, ahorro externo) y del financiamiento (cartera de crédito, emisión de deuda, financiamiento externo).
- **Tamaño de muestra:** no aplica.
- **Microdatos:** no; bases agregadas.
- **Acceso:** abierto.
- **URL:** https://www.gob.mx/cnbv/documentos/reportes-de-analisis
- **Licencia:** no verificada.

### 4. Sistema de Información Económica (SIE)

- **Institución responsable:** Banco de México.
- **Periodicidad y ediciones:** variable por serie, de diaria a anual; series históricas largas.
- **Cobertura:** nacional, agregados. Incluye estadísticas del SPEI publicadas en la sección de Estadísticas / SIE, además de series de crédito, tasas de interés y agregados monetarios.
- **Tamaño de muestra:** no aplica.
- **Microdatos:** no. Descarga de series de tiempo; existe API REST con catálogo de series documentado.
- **Acceso:** consulta web abierta. La API requiere solicitar un token.
- **URL:** https://www.banxico.org.mx/SieInternet/ · API: https://www.banxico.org.mx/SieAPIRest/service/v1/doc/catalogoSeries
- **Licencia:** términos de uso del sitio de Banco de México — **no verificados**.

### 5. Estadísticas del Sistema de Ahorro para el Retiro (SAR)

- **Institución responsable:** Comisión Nacional del Sistema de Ahorro para el Retiro (CONSAR).
- **Periodicidad y ediciones:** mensual. El portal SISET publica fecha de publicación de estadísticas y secciones de información financiera, operativa y contable, con apartados de cuentas administradas, registro de trabajadores y traspasos.
- **Cobertura:** nacional, universo de cuentas individuales. Transversal repetido.
- **Contenido temático:** número de cuentas por tipo, saldo de recursos administrados, entradas y salidas de recursos, traspasos entre administradoras, comisiones e indicadores de desempeño de SIEFORE.
- **Tamaño de muestra:** no aplica.
- **Microdatos:** no a nivel persona. Conjuntos agregados en datos.gob.mx en formato XLSX.
- **Acceso:** abierto, sin registro.
- **URL:** https://www.gob.mx/consar/articulos/informacion-estadistica-61314 · https://www.consar.gob.mx/gobmx/aplicativo/siset/Enlace.aspx?md=2 · https://www.datos.gob.mx/organization/consar
- **Licencia:** marco de datos abiertos del Gobierno de México — no verificada de forma expresa.

### 6. REDECO, REUNE y Buró de Entidades Financieras

- **Institución responsable:** Comisión Nacional para la Protección y Defensa de los Usuarios de Servicios Financieros (CONDUSEF).
- **Periodicidad y ediciones:** registro continuo; publicaciones trimestrales en el Buró de Entidades Financieras.
- **Cobertura:** nacional, por institución financiera. REDECO es el Registro de Despachos de Cobranza que administra la CONDUSEF y por el cual las personas pueden presentar reclamación contra la entidad financiera. El total de reclamaciones del Buró suma las registradas en CONDUSEF y las reportadas por la propia institución en REUNE. Universo de quejas; no es muestra probabilística.
- **Tamaño de muestra:** no aplica.
- **Microdatos:** existe base abierta de despachos de cobranza contratados en datos.gob.mx; la ficha advierte que las bases pueden incluir actualizaciones retroactivas y que la información histórica puede cambiar. Formato no verificado. Microdato de queja individual: **no verificado**.
- **Acceso:** consulta abierta. Presentar una queja requiere registro y folio.
- **URL:** https://eduweb.condusef.gob.mx/redeco/redeco.aspx · https://www.buro.gob.mx/ · https://www.datos.gob.mx/dataset/registro_despachos_cobranza_contratados_entidades_financieras
- **Licencia:** no verificada.

---

## B. Encuestas en hogares con representatividad nacional

### 7. Encuesta Nacional de Ingresos y Gastos de los Hogares (ENIGH)

- **Institución responsable:** Instituto Nacional de Estadística y Geografía (INEGI).
- **Periodicidad y ediciones:** bienal; nueva serie con edición 2024. Ediciones históricas desde 1984 — **listado completo no verificado**.
- **Cobertura:** nacional y por entidad federativa, con cortes urbano y rural. Transversal (submuestra probabilística); no panel de hogares.
- **Tamaño de muestra:** 105 718 viviendas en 2024.
- **Contenido temático pertinente:** percepciones y erogaciones financieras, y flujos relativos a activos y pasivos, sin desglose por instrumento financiero.
- **Microdatos:** sí, descargables. Formatos CSV y DBF con descriptores; se acompaña documentación de cálculo de indicadores en R.
- **Acceso:** descarga directa, sin registro.
- **URL:** https://www.inegi.org.mx/programas/enigh/nc/2024/ · microdatos: https://www.inegi.org.mx/contenidos/programas/enigh/nc/2024/microdatos/
- **Licencia:** Términos de Libre Uso de la Información del INEGI (copia, difusión, adaptación, extracción y explotación comercial, con atribución obligatoria).

### 8. Encuesta Nacional sobre Salud Financiera (ENSAFI)

- **Institución responsable:** INEGI en colaboración con CONDUSEF.
- **Periodicidad y ediciones:** sin periodicidad establecida; una sola edición verificada, 2023, con resultados presentados el 25 de junio de 2024.
- **Cobertura:** nacional y por entidad federativa, en localidades urbanas y rurales; población de 18 años y más. Transversal.
- **Tamaño de muestra:** tamaño mínimo calculado de 22 513 viviendas, ajustado a 22 982.
- **Contenido temático:** deuda, ahorro y gasto individual, con subtemas de ahorro formal e informal y de crédito formal e informal; comportamientos y percepciones de bienestar financiero; estrés financiero; metas financieras.
- **Microdatos:** sí. Base de usuario final en CSV (UTF-8) y en formato de datos abiertos, con descriptor de archivos y modelo entidad–relación.
- **Acceso:** uso público mediante sitio de descarga directa; sin registro.
- **URL:** https://www.inegi.org.mx/programas/ensafi/2023/ · metadatos: https://www.inegi.org.mx/rnm/index.php/catalog/992 · micrositio CONDUSEF: https://ensafi.condusef.gob.mx/
- **Licencia:** Términos de Libre Uso del INEGI, con crédito obligatorio y prohibición de alterar el sentido original de la información.

### 9. Encuesta Nacional sobre las Finanzas de los Hogares (ENFIH)

- **Institución responsable:** Banco de México en conjunto con INEGI; levantamiento a cargo del INEGI.
- **Periodicidad y ediciones:** edición única. 2019 es el único levantamiento realizado.
- **Cobertura:** representatividad nacional; muestra distribuida conforme a criterios del INEGI en cada entidad federativa. Transversal.
- **Tamaño de muestra:** 22 931 viviendas calculadas, ajustadas a 23 000.
- **Contenido temático:** pasivos y activos financieros y no financieros de los hogares, medidos en acervos y en flujos; riqueza neta; ingresos; y uso de financiamiento por canales de crédito formales e informales.
- **Microdatos:** sí. Base de datos en ZIP, acompañada de diseño muestral, informe operativo y diseño conceptual en PDF, más tabulados. Formato interno del ZIP no verificado.
- **Acceso:** descarga directa desde Banco de México e INEGI; sin registro.
- **URL:** https://www.banxico.org.mx/enfih/ · metadatos: https://www.inegi.org.mx/rnm/index.php/catalog/709
- **Licencia:** Términos de Libre Uso del INEGI por ser proyecto INEGI. Términos del espejo en Banco de México **no verificados**.

### 10. Encuesta Nacional de Inclusión Financiera (ENIF)

- **Institución responsable:** INEGI en convenio con CNBV.
- **Periodicidad y ediciones:** aproximadamente trienal. Ediciones 2012, 2015, 2018, 2021 y 2024; la de 2024 es el quinto levantamiento.
- **Cobertura:** nacional, por tamaño de localidad y por sexo, con resultados también por región; población de 18 a 70 años. Transversal. Levantamiento 2024 del 24 de junio al 16 de agosto.
- **Tamaño de muestra:** 15 161 viviendas calculadas, ajustadas a 15 263 en 2024.
- **Contenido temático:** tenencia de productos de ahorro y cuentas de captación, financiamiento, seguros, ahorro para el retiro, uso y disponibilidad de infraestructura financiera, educación y bienestar financieros, y conocimiento y uso de herramientas de pago digitales.
- **Microdatos:** sí, programa INEGI con base de datos publicada. Formato específico de la edición 2024 **no verificado**; en programas equivalentes del INEGI es CSV más formato de datos abiertos.
- **Acceso:** descarga directa, sin registro.
- **URL:** metadatos https://www.inegi.org.mx/rnm/index.php/catalog/1081 · CNBV: https://www.gob.mx/cnbv/acciones-y-programas/medicion-de-inclusion-financiera
- **Licencia:** Términos de Libre Uso del INEGI.

### 11. Encuesta Nacional de Vivienda (ENVI)

- **Institución responsable:** INEGI, en colaboración con CONAVI, INFONAVIT, FOVISSSTE y Sociedad Hipotecaria Federal.
- **Periodicidad y ediciones:** irregular. Ediciones 2014 (primera) y 2020.
- **Cobertura:** nacional; la nota técnica menciona desagregación por entidad federativa. Transversal.
- **Tamaño de muestra:** **no verificado**.
- **Contenido temático pertinente:** financiamiento de las viviendas, distinguiendo créditos de institución financiera privada, créditos de instituciones públicas y préstamos de familiares o conocidos; además gastos en construcción, reparación y mejora.
- **Microdatos:** programa INEGI con microdatos publicados — **formato no verificado**.
- **Acceso:** presumiblemente descarga directa sin registro conforme al patrón INEGI — **no verificado para esta encuesta**.
- **URL:** metadatos https://www.inegi.org.mx/rnm/index.php/catalog/695
- **Licencia:** Términos de Libre Uso del INEGI.

### 12. Encuesta Nacional sobre Salud y Envejecimiento en México (ENASEM / MHAS)

- **Institución responsable:** esfuerzo conjunto de la Universidad de Texas (UTMB), Universidad de Wisconsin, Instituto Nacional de Geriatría, Instituto Nacional de Salud Pública, UCLA e INEGI, con apoyo del National Institute on Aging. La edición 2024 se presentó con UT Health San Antonio.
- **Periodicidad y ediciones:** rondas irregulares. Ediciones 2001, 2003, 2012, 2015, 2018, 2021 y 2024; octava ronda prevista para 2027.
- **Cobertura:** nacional, con representación urbana y rural; población de 50 años y más. **Panel** (estudio longitudinal con refresco de cohortes: nueva muestra de nacidos entre 1952 y 1962 en 2012, entre 1963 y 1968 en 2018, y entre 1969 y 1974 en 2024).
- **Tamaño de muestra:** 23 044 personas en 2024, de las cuales 17 043 de seguimiento y 6 001 de reemplazo.
- **Contenido temático pertinente:** situación económica y pensiones, dentro del contenido común de la familia de encuestas HRS. Alcance exacto en ahorro y deuda del hogar: **no verificado a detalle**.
- **Microdatos:** sí, por dos vías: portal INEGI y portal MHAS.
- **Acceso:** el portal MHAS opera con usuario y contraseña, es decir **requiere registro**. La vía INEGI sigue el esquema de descarga directa.
- **URL:** https://www.inegi.org.mx/programas/enasem/2024/ · https://www.mhasweb.org/
- **Licencia:** Términos de Libre Uso del INEGI para la vía INEGI; términos de MHAS **no verificados**.

### 13. Encuesta Nacional sobre Niveles de Vida de los Hogares (ENNViH / MxFLS)

- **Institución responsable:** Universidad Iberoamericana y CIDE, en colaboración con investigadores de la Universidad de Duke.
- **Periodicidad y ediciones:** tres levantamientos: 2002, 2005-2006 y 2009-2012.
- **Cobertura:** nacional, urbano, rural y regional, con cinco regiones de interés en cada ronda. **Panel** — da seguimiento a los individuos de la línea basal, incluso si migraron dentro del país o a Estados Unidos.
- **Tamaño de muestra:** aproximadamente 35 mil individuos en 8 400 hogares en el levantamiento basal de 2002.
- **Contenido temático pertinente:** ingresos, programas sociales, empleo, propiedad de la tierra y negocios familiares, entre otros temas. Módulos específicos de crédito y ahorro: **no verificados**.
- **Microdatos:** sí. Declarados de dominio público, con datos y documentación descargables sin costo. Formato **no verificado**. Se han emitido correcciones a ponderadores longitudinales con instrucción de reemplazar descargas previas.
- **Acceso:** gratuito **previo registro**.
- **URL:** https://www.ennvih-mxfls.org/
- **Licencia:** declarada como dominio público en el sitio del proyecto; texto formal de licencia **no verificado**.

### 14. Global Findex Database (México como país incluido)

- **Institución responsable:** Banco Mundial; levantamiento por Gallup.
- **Periodicidad y ediciones:** aproximadamente trienal. Ediciones 2011, 2014, 2017, 2021 y 2025; la edición 2025 se levantó a lo largo de 2024.
- **Cobertura:** nacional, población adulta. Transversal. Encuestas representativas a nivel nacional de unos 148 000 adultos en 141 economías.
- **Tamaño de muestra:** submuestra de México **no verificada** (en ediciones anteriores del programa suele rondar el millar de casos — no verificado).
- **Contenido temático:** acceso y uso de servicios financieros formales e informales para ahorrar, pedir prestado, hacer pagos y gestionar riesgo financiero; en 2025 se añaden series de propiedad de teléfono móvil, uso de internet y seguridad digital.
- **Microdatos:** sí, en dos niveles. Datos por país en XLSX, CSV, Stata (.dta) y World Bank Databank; datos a nivel individual en la Microdata Library.
- **Acceso:** datos por país sin registro. La Microdata Library normalmente requiere cuenta y aceptación de términos — **no verificado para esta colección**.
- **URL:** https://www.worldbank.org/en/publication/globalfindex/download-data · ficha de México 2025: https://microdata.worldbank.org/index.php/catalog/7945
- **Licencia:** **no verificada**.

---

## C. Universo de empresas, incluidos micronegocios de hogares (adyacente al dominio)

### 15. Encuesta Nacional de Financiamiento de las Empresas (ENAFIN)

- **Institución responsable:** CNBV en coordinación con INEGI.
- **Periodicidad y ediciones:** aproximadamente trienal. Ediciones 2015, 2018, 2021 y 2024.
- **Cobertura:** nacional, por tamaño de empresa (micro de seis a diez personas ocupadas, pequeña, mediana y grande), por sector de actividad (construcción, manufacturas, comercio y servicios privados no financieros incluidos transportes) y por tamaño de localidad (50 000 a 499 999 habitantes, y 500 000 y más). Transversal. Unidad de observación: la empresa con 6 o más personas ocupadas.
- **Tamaño de muestra:** **no verificado**.
- **Contenido temático:** características de la empresa, recursos propios y aportaciones de capital, financiamiento y solicitudes de crédito, y servicios bancarios y financieros. Cuestionario electrónico respondido principalmente a través del sitio del INEGI.
- **Microdatos:** programa INEGI con microdatos publicados — **formato no verificado**.
- **Acceso:** descarga directa conforme al patrón INEGI.
- **URL:** https://www.inegi.org.mx/programas/enafin/2021/ · https://www.gob.mx/cnbv/acciones-y-programas/encuesta-nacional-de-financiamiento-de-las-empresas · metadatos 2024: https://www.inegi.org.mx/rnm/index.php/catalog/1106
- **Licencia:** Términos de Libre Uso del INEGI.

---

## D. Fuentes que probablemente existen pero no pudieron confirmarse

Para ninguna de las siguientes se verificó existencia actual, ediciones, disponibilidad de microdatos, condiciones de acceso ni licencia.

- **Encuesta Nacional de Mercados Financieros Rurales (ENAMFIR), 2002.** Referida en documentación oficial de la ENFIH como levantamiento del Banco Mundial con INEGI, FIRA y SHCP sobre uso de servicios financieros en hogares, micronegocios y empresas de áreas rurales, con edición única en 2002. No se localizó página de datos ni microdatos.
- **Encuesta Nacional sobre Confianza del Consumidor (ENCO)**, INEGI y Banco de México, mensual. Presumible cobertura de percepción sobre la situación económica del hogar y capacidad de compra de bienes duraderos. Sin verificar si capta ahorro o crédito, ni si publica microdatos.
- **Censo de Población y Vivienda 2020, cuestionario ampliado**, INEGI. Presumible captación de forma de adquisición de la vivienda y financiamiento asociado, además de remesas. Sin verificar.
- **Encuesta Nacional sobre Disponibilidad y Uso de TIC en los Hogares (ENDUTIH)**, INEGI e IFT. Presumible cobertura de compras y pagos por internet y de banca en línea. Sin verificar.
- **Encuesta sobre Condiciones Generales y/o Estándares en el Mercado de Crédito Bancario** y **Encuesta de Evaluación Coyuntural del Mercado Crediticio (EECMC)**, Banco de México, trimestrales. Miden oferta y acceso al crédito desde bancos y empresas. Sin verificar ediciones, microdatos ni URL de datos.
- **Encuesta Nacional Agropecuaria (ENA)**, INEGI y SADER. Presumible sección de crédito y seguro para unidades de producción. Sin verificar.
- **Encuesta Nacional sobre Productividad y Competitividad de las MIPYME (ENAPROCE)**, INEGI. Presumible sección de financiamiento. Sin verificar.
- **Datos abiertos de INFONAVIT y FOVISSSTE** (créditos otorgados, cartera, originación). Presumibles portales con series descargables. Sin verificar.
- **Encuesta de Satisfacción Residencial (ESR)**, Sociedad Hipotecaria Federal, aplicada desde 2006 en conjuntos habitacionales con al menos un hogar con crédito de vivienda de Sofomes, bancos, INFONAVIT o FOVISSSTE. Sin verificar vigencia, microdatos ni URL de datos.
- **Encuesta ESRU de Movilidad Social (ESRU-EMOVI)**, Centro de Estudios Espinosa Yglesias. Presumibles módulos de activos y patrimonio del hogar. Sin verificar.
- **Buró de Crédito y Círculo de Crédito** (sociedades de información crediticia). Datos de historial y morosidad a nivel persona; presumiblemente sin microdato público. Sin verificar.
- **Comisión Nacional de Seguros y Fianzas (CNSF)**, series del sector asegurador. Fuera del núcleo de crédito y ahorro solicitado. Sin verificar.
- **Reportes regulatorios de instituciones de tecnología financiera (ITF) ante la CNBV.** Presumibles agregados publicados desde la entrada en vigor de la Ley Fintech. Sin verificar.
- **ENIGH Estacional (ENIGH-A)**, ediciones 2020 y 2022 según el listado de programas del INEGI. Sin verificar contenido financiero, muestra ni microdatos.
