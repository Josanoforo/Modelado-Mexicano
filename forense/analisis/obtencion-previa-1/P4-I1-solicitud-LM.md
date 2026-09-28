# Solicitud al Laboratorio de Microdatos del INEGI · ENAPROCE 2015 y 2018 · borrador listo para firmar

Estado: PREPARADA, NO ENVIADA. Se envía solo si mesa firma dos cosas: (1) R03 queda redefinida como «carga regulatoria de la MIPYME», sin pago informal, porque el cuestionario no lo mide (NOTA-DECISION.md, líneas 13–18); (2) mesa acepta la unidad empresa.

Formulario vigente (LEÍDO 2026-09-28): https://www.inegi.org.mx/contenidos/app/microdatos/laboratoriodatos/doc/Solicitud_Uso.pdf. Copia en data/raw/obtencion-previa-1/enaproce/inegi_lm_solicitud_uso_formato.pdf, sha256 5a5d041da5edbe1d17ef608c9eb4d072f34a0b7811c20c368c223cf08bb15c19. Tiene 4 páginas: datos del solicitante, institución, supervisor, proyecto, modalidad (Laboratorio con sede o Procesamiento remoto), software (Stata, SPSS, R, ArcGIS) y autorización de publicar.

## Receta de un minuto para mesa

1. Designar un titular con identidad real y acreditable: becario SECIHTI o investigador SNII, o personal de una institución con convenio con el INEGI, o servidor público del SNIEG (requisito de acreditación citado en el resultado de búsqueda del portal de microdatos; texto normativo NO-VERIFICABLE-AQUÍ).
2. Descargar el PDF de arriba y copiar en él los campos del proyecto (sección siguiente). Llenar los datos personales, de la institución y del supervisor.
3. Preparar dos adjuntos: CV del titular y, si la institución no tiene convenio, el convenio o constancia de acreditación.
4. Enviar por la sección Microdatos del sitio del INEGI (https://www.inegi.org.mx/datos/?ps=microdatos). Marcar «Procesamiento remoto» (no exige viajar a una sede).
5. Plazo: NO-VERIFICABLE-AQUÍ. Las reglas de operación (https://sc.inegi.org.mx/repositorioNormateca/Or_24Mar20.pdf) no se pudieron abrir desde la nube (proxy). Mesa las abre en navegador y anota el plazo al presentar.

## Campos del proyecto (texto para pegar)

- **Nombre del proyecto:** Carga regulatoria de las micro, pequeñas y medianas empresas en México, 2014 y 2017.
- **Objetivo:** Estimar, por ola, tamaño (micro / pequeña / mediana) y sector, las horas mensuales que las empresas dedican a trámites gubernamentales, el gasto mensual en cumplimiento fiscal federal (sin impuestos) y la distribución del trámite que consideran principal obstáculo, con error estándar de diseño.
- **Beneficio para la sociedad:** Medición comparable de la carga administrativa sobre la MIPYME para evaluar la política de mejora regulatoria.
- **Programas, años y cobertura:** ENAPROCE 2015 (referencia 2014) y ENAPROCE 2018 (referencia 2017). Cuestionarios micro y PyME (manufactura, comercio y servicios). Nacional; sin geografía fina.
- **Variables:** 2015 micro M61–M64 y PyME P79–P82; 2018 micro M64_1–M64_3, M65–M67 y PyME P81_6, P82–P84. Además tamaño, sector SCIAN, indicador de panel/ola, FAC_EXPA, estrato, UPM (o réplicas) y códigos de faltante/imputación. No se requieren identificadores.
- **Metodología:** medias, medianas y cuantiles ponderados; proporciones por categoría; varianza por linealización de Taylor con estrato/UPM; las grandes empresas quedan excluidas; los montos se reportan en pesos nominales por periodo.
- **Justificación del microdato:** los datos abiertos solo publican totales nacionales de microempresas de 2017/2018 sin error estándar, y no hay publicación equivalente para PyME ni para 2015.
- **Resultados esperados:** tabla ola × tamaño × sector con estimación, n no ponderado, EE e IC95.
- **Difusión:** repositorio de investigación del proyecto, solo con cifras agregadas que pasen el control de confidencialidad del INEGI.
- **Terminación estimada:** a llenar por mesa.
- **Modalidad:** Procesamiento remoto. **Software:** R o Stata.
- **Autoriza publicar:** a decidir por el titular.

Alternativa sin identidad: pedir una salida agregada calculada por el INEGI (tabulado a la medida) con esta misma tabla. Vía y costo NO-VERIFICABLE-AQUÍ.
