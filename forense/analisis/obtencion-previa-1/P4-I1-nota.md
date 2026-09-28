# P4 · I1 · ENAPROCE 2015/2018 frente a R03 · nota de la pieza

Encargo: forense/encargos/2026-09-27-GEN2-OBTENCION-PREVIA-1.md, línea 14 (P4). NC: NC-260922-GEN2-ADQ-F6-DIRIGIDA-1-e7be-02. Cola: data/cola-adquisicion-v1_0.tsv, fila ENAPROCE_2015_2018_MICRODATO_COMPLETO (estado NO-ACCESIBLE). HEAD de lectura: d46f422b. Fecha: 2026-09-28. Entorno: nube con red (INEGI 200). No se abrió microdato. Contadores movidos: cero.

## (i) Qué necesita R03 (LEÍDO)

- forense/prereg-duelo-v2/F5-panel-candidatos-v1_3.tsv, línea 4: familia `R03-TRA-ENAPROCE-TRAMITES`; unidad «empresa micro/pequeña/mediana»; pregunta «Carga regulatoria y pago informal en trámites de la MIPYME»; regla M `tramite.mordida.discrecional`; faltante: «Microdato real (no la base cegada de ejemplo) y el FD de 2015 y 2018. Más la misma firma de unidad de R02». Estado RETENIDA-NO-EJECUTABLE.
- forense/prereg-duelo-v2/F6-falta-conseguir-v1_1.tsv, línea 8: verificación de llegada = «payload que no diga ejem_base ni ciega, con FD».
- forense/produccion/enaproce-instrumentos-acceso-1/CONTRATO-REACTIVOS.md (116 líneas): variables de carga por ola × instrumento: 2015 micro M61–M64, PyME P79–P82; 2018 micro M64_1..3, M65–M67, PyME P81_6, P82–P84; `FAC_EXPA`; universo empresas 0–100/250 por sector, sin grandes; periodos de referencia 2014 y 2017.
- forense/produccion/enaproce-instrumentos-acceso-1/NOTA-DECISION.md, líneas 13–18 y 36: **ningún reactivo mide solicitud o pago informal**, así que la mitad `mordida` de R03 no tiene desenlace en ENAPROCE con ninguna vía de acceso. Decisión previa recomendada: no tramitar el Laboratorio para la R03 actual; como mucho, un descriptivo de carga regulatoria con unidad empresa, sujeto a firma de mesa.

## (ii) Inventario y dictamen (EJECUTADO; detalle en P4-I1-enaproce.tsv, 14 filas)

- **Premisa del encargo corregida:** el manifiesto tiene **24** entradas que mencionan ENAPROCE (19 con «enaproce» en el id, más 5), no 75. Las 24 se agrupan en 10+4 bases de ejemplo cegadas, 6 cuestionarios, 2 fichas RNM, 1 informe de levantamiento y 1 CKAN vacío. Ninguna es microdato real. Conteo: python sobre data/manifiesto.yaml con el filtro `'enaproce' in str(e).lower()` (7035 entradas examinadas).
- Condición de acceso vigente en RNM 330 y 518 (fetch del 2026-09-28): «La información de la ENAPROCE a nivel microdato es confidencial; la descarga… es restringida al público en general… acceso indirecto: Laboratorio de análisis de datos». Veredicto: **NO-ACCESIBLE por descarga**.
- **Hallazgo nuevo:** Datos abiertos 2018 (`enaproce_2016_2018_micro_csv.zip`, sha 5e9bca09…). Contiene agregados nacionales de **microempresas**: C_66 gasto fiscal mensual total (2017), C_67 promedio de horas en trámites (2017), la serie _64 de principal problema (I_64 = exceso de trámites) y la serie _65 de trámite-obstáculo. Veredicto: **cubre R03 en parte**, porque solo trae micro, total nacional, 2017/2018, sin PyME, sin 2015, sin error estándar ni cortes, y nada de pago informal. No se abrió `conjunto_de_datos/`: solo se leyeron el diccionario, los metadatos y los rótulos del catálogo.
- Datos abiertos 2015: NO-ENCONTRADO (5 nombres de archivo probados en `2015/datosabiertos/`, todos soft-404).
- Tabulados 2015/2018: NO OBTENIDO POR ESTE AGENTE EN 2 INTENTOS (6 rutas probadas; el portal se renderiza con JS). Receta: navegador → https://www.inegi.org.mx/programas/enaproce/2018/#tabulados → módulo de regulación → descargar y registrar.
- Indicadores de precisión 2018: solo cubren número de empresas, personal ocupado e ingresos. Veredicto: EXISTE-NO-SATISFACE.
- **Dictamen global:** lo público **satisface R03 en parte**: carga regulatoria (horas, gasto fiscal formal, obstáculo) de microempresas 2017 a nivel nacional, sin error de diseño. **No satisface en nada** la parte `pago informal`, y el microdato del Laboratorio tampoco la satisface, porque el cuestionario no tiene la pregunta (LEÍDO, NOTA-DECISION). La NC tiene razón en la vía, pero la supera el problema de contenido.

## (iii) Microdato

El microdato es la única vía para PyME, 2015 y error estándar. No lo es para `mordida`, que ninguna vía da. La solicitud queda redactada en P4-I1-solicitud-LM.md, condicionada a que mesa redefina R03 como «carga regulatoria» con unidad empresa. Sin esa redefinición, la recomendación es la opción (b) de la hoja I1 (NO-ACCESIBLE declarado) más «NO-CONSTRUIBLE por contenido» para la parte mordida.

## NO-CORRIDO / reservas

- Reglas de operación del LM (sc.inegi.org.mx): el proxy de salida las bloquea. Plazo de respuesta NO-VERIFICABLE-AQUÍ.
- Tabulados: diferidos a la receta de navegador de arriba.
- El manifiesto no se editó. Los payloads nuevos los registra el hilo principal.
