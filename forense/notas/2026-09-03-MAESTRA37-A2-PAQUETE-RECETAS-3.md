# PAQUETE-RECETAS-3 — 2026-09-03

Producido por `ACTO MAESTRA37-A2 · REVISA-COLA-A-DETALLE` sobre `data/curacion-registro/cola-adquisicion-registro.tsv`. A diferencia de los paquetes `2026-09-01`/`2026-09-02` (producidos por `/adquiere`, que cierran filas en `NO-OBTENIDO-POR-ESTE-AGENTE`), este acto NO descarga ni cierra ninguna fila — el criterio de selección es distinto: aquí van las **6 de 28** filas de la revisión a detalle cuya recomendación fue `BAJAR` (receta ejecutable en ≤1 minuto, verificada hoy). Las otras 22 (`MESA-DECIDE`: 12 · `NO-BAJAR-PORQUE`: 10) no traen receta porque, o dependen de un criterio de mesa (costo, prioridad), o no hay URL/instrumento que un navegador pueda abrir — ver el detalle completo de las 28 en `forense/notas/2026-09-03-MAESTRA37-A2-revision-cola.md` §2.

Ninguna receta de abajo, ejecutada, cierra la fila por sí sola: es mesa quien decide y quien, al ejecutar y registrar el payload, mueve `estado_A4A5` (mismo criterio que la firma de mesa citada en §0 del acto: ninguna fila se cierra por veredicto de agente).

---

## Tablero

| # | fuente_canonica | estado_A4A5 actual | qué trae |
|---:|---|---|---|
| 1 | `EARTHQUAKE_TRUST_LAPOP_2017` | PENDIENTE | receta abajo |
| 2 | `IMSS_BIENESTAR_ACCIONES_DE_INFRAESTRUCTURA` | PENDIENTE | receta abajo |
| 3 | `EXT_OF_11_REUNE_REDECO` | NO-OBTENIDO-POR-ESTE-AGENTE(1 intento) | receta abajo |
| 4 | `ENVIPE_EXTRACCION_TEXTO_REACTIVO` | PENDIENTE | receta abajo |
| 5 | `TEPJF_ELECCIONES_CONCURRENTES_1991_2018` | NO-OBTENIDO-POR-ESTE-AGENTE(1 intentos) | receta abajo |
| 6 | `IETAM_TAMAULIPAS_SERIE_MUNICIPAL` | NO-OBTENIDO-POR-ESTE-AGENTE(5 intentos) | receta abajo |

---

## 1. `EARTHQUAKE_TRUST_LAPOP_2017`

Receta de navegador, ≤1 minuto, verbatim: (1) Pega en la barra de direcciones y da Enter: https://dataverse.harvard.edu/api/access/datafile/10123574?format=original -- el navegador descarga "Final_dataset_Mexico_Earthquake.dta" (Stata 14, 674621 B; confirmado con curl: 303 con Location firmado a S3, sin login/clickwrap). Alternativa en tab-delimitado sin conversión: la misma URL sin "?format=original" descarga "Final_dataset_Mexico_Earthquake.tab" (389401 B). (2) Pega y da Enter: https://dataverse.harvard.edu/api/access/datafile/10123575 -- descarga "Final_do_file_Mex_quake.do" (44712 B, código de réplica Stata, confirma mapeo de variables a las cifras del paper). Fin -- dos archivos, licencia CC0 1.0 (dominio público), sin cuenta ni formulario. Vía UI alterna si se prefiere clic: abrir https://dataverse.harvard.edu/dataset.xhtml?persistentId=doi:10.7910/DVN/JGYZ7T , marcar ambos archivos, botón "Access File"→"Download". Nota para quien ejecute (MAESTRA38-A1/mesa): al registrar en manifiesto.yaml, dar de alta esta fuente como hermana propia (no fusionar con la fila 52 LAPOP genérica) -- son instrumentos distintos por diseño, muestra y repositorio; y confirmar en aliases-fuentes.tsv si el nombre "LAPOP" de esta fila se conserva o se corrige, ya que el dataset no se publica bajo esa marca aunque su coautora dirige LAPOP.

---

## 2. `IMSS_BIENESTAR_ACCIONES_DE_INFRAESTRUCTURA`

Receta ejecutable por un humano en <=1 minuto, verbatim (URLs verificadas hoy por HEAD, 200, tipo/tamaño reales):

1. Abrir en el navegador: https://imssbienestar.gob.mx/assets/doc/transparencia/05_datosabiertos/04_uinfraestructura/SEGUIM_ACCIONES_INFRA_FISICA_OBRA_CONS_MANT_1Y2TRIM24.xlsx
   → descarga automática. Archivo esperado: SEGUIM_ACCIONES_INFRA_FISICA_OBRA_CONS_MANT_1Y2TRIM24.xlsx (~246 KB / 251823 B, cubre 1°-2° trimestre 2024).

2. Abrir en el navegador: https://imssbienestar.gob.mx/assets/doc/transparencia/05_datosabiertos/04_uinfraestructura/Seguimiento%20de%20Acciones%20de%20Infraestructura%201%C2%B0%20Trimestre%202025.xlsx
   → descarga automática. Archivo esperado: "Seguimiento de Acciones de Infraestructura 1° Trimestre 2025.xlsx" (~1.22 MB / 1278564 B, cubre 1er trimestre 2025).

Opcional/alterno (mismo trimestre 2025, formato CSV, mucho más chico -- posiblemente un extracto reducido, no el reemplazo del XLSX #2): https://repodatos.atdt.gob.mx/api_update/imss-bienestar/acciones_infraestructura_fisica_obra_conservacion_mantenimiento/seguimiento_acciones_infraestructura_1er_trimestre_2025.csv → archivo esperado seguimiento_acciones_infraestructura_1er_trimestre_2025.csv (8795 B).

Si el enlace directo cambiara: imssbienestar.gob.mx → menú "Transparencia" (07_transparencia.html) → sección "Banco de Datos - Unidad de Infraestructura" → subsección "Proceso de Seguimiento de Acciones de Infraestructura Física de Obra, Conservación y Mantenimiento" → clic en cada archivo EXCEL listado.

Nota para quien baje: ningún criterio de mesa depende hoy de esta fuente (ninguna necesidad de relaciones.tsv la cita) -- BAJAR se recomienda porque la receta es barata y confiable (candidata real localizada por fin, tras dos actos previos sin sondear red), no porque haya urgencia de consumo.

---

## 3. `EXT_OF_11_REUNE_REDECO`

Dos archivos, cada uno bajable en <=1 minuto por descarga directa sin cuenta ni JS (verificado con curl: HTTP 200, Content-Type text/csv, Content-Length real, sin redirección a login):

1) REDECO -- abrir en el navegador: https://repodatos.atdt.gob.mx/api_update/condusef/registro_despachos_cobranza_contratados_entidades_financieras/redeco_datosabiertos1ertrim_2026.csv
   El navegador descarga el archivo directamente (Content-Type text/csv fuerza la descarga o la muestra como texto, según el navegador -- si se muestra como texto, Ctrl+S / Guardar como). Archivo esperado: redeco_datosabiertos1ertrim_2026.csv (~663 KB, ~678,710 B).

2) REUNE -- abrir en el navegador: https://repodatos.atdt.gob.mx/api_update/condusef/unidades_especializadas/datosabiertos_310326.csv
   Mismo comportamiento. Archivo esperado: datosabiertos_310326.csv (~4.3 MB, ~4,482,648 B).

Ruta alterna equivalente (un clic más, vía el portal en vez del enlace directo, útil si el enlace directo cambia de nombre en el próximo trimestre): ir a https://www.datos.gob.mx/dataset/registro_despachos_cobranza_contratados_entidades_financieras (o .../dataset/unidades_especializadas), clic en "Descargar" sobre el recurso CSV con la fecha "Última actualización" más reciente.

Nota para quien baje: ambos son registros trimestrales -- si mesa quiere la serie histórica completa, cada dataset ya trae también el recurso del trimestre anterior (30/09/2025) en la misma página, con el mismo patrón de URL.

---

## 4. `ENVIPE_EXTRACCION_TEXTO_REACTIVO`

Esta fila se llama "EXTRACCIÓN" pero el hallazgo de hoy la reencuadra: lo que hace falta no es abrir/analizar semánticamente un PDF (eso sigue fuera de perímetro), sino ADQUIRIR un archivo pequeño, ya transcrito por el propio INEGI, machine-readable, con el texto literal de cada reactivo -- una adquisición normal, no una extracción semántica. Receta ejecutable ≤1 min, dos pasos, mismo patrón para ambos instrumentos: (A) ENVIPE -- abrir en el navegador la URL exacta `https://www.inegi.org.mx/rnm/index.php/metadata/export/1130/ddi` (o el `/json` equivalente); el navegador descarga/muestra el XML DDI del catálogo ENVIPE 2025 sin login ni clics adicionales; guardar como `envipe2025_rnm_ddi.xml` (~2.2 MB). Repetible por año cambiando el id de catálogo (2018=384, 2021=698, 2022=803, 2023=913, 2024=1027, 2025=1130). (B) ENSU (hermana) -- misma receta con `https://www.inegi.org.mx/rnm/index.php/metadata/export/1100/ddi` (2025; otros años: 2018=400, 2020=584, 2021=654, 2022=754, 2023=859, 2024=969); guardar como `ensu2025_rnm_ddi.xml`. Tras la descarga (trabajo de un acto de adquisición, no de este A2): registrar en manifiesto.yaml y correr un parser de XML sobre los nodos `<qstnLit>` -- mecánico, no semántico, por lo que ya no calza con la exclusión que MAESTRA33-A3 declaró para el PDF. Nota para mesa: como ninguna regla de relaciones.tsv cita hoy esta fila, la urgencia de bajarlo es baja -- pero el costo es mínimo (2 clics, <5MB) y elimina de un golpe el hueco 0%-texto-de-reactivo que motivó FP-190/CIV-08, además de traer una candidata (ENSU) más específica que la que el mapeo original había encontrado.

---

## 5. `TEPJF_ELECCIONES_CONCURRENTES_1991_2018`

Receta de navegador, ejecutable en menos de 1 minuto: abrir directamente https://www.te.gob.mx/editorial_service/media/pdf/JEA_Elecciones_concurrentes.pdf en el navegador (no hace falta pasar por el catálogo JS de /publicaciones/ ni por el buscador -- es la URL directa del archivo, confirmada hoy). El navegador mostrará o descargará el PDF automáticamente; si no descarga solo, clic derecho sobre la página → "Guardar como". Nombre de archivo esperado: JEA_Elecciones_concurrentes.pdf, ~1.4 MB (1441115 B exactos, confirmado por curl -A navegador con Content-Type: application/pdf y Last-Modified: 22-dic-2020, coincide con la publicación de 2020 que la nota de MAESTRA34-L6 ya identificaba). Esto reemplaza la receta anterior (que pedía navegar el catálogo JS y buscar el libro a mano) por una más corta y verificada: la URL exacta ya se conoce y responde con el archivo real, no con el soft-404 de 2102 B que dieron las rutas adivinadas anteriormente. Nota para quien ejecute la descarga (MAESTRA38-A1/mesa): al no haber FD público, documentar manualmente en el registro qué tablas/variables trae el anexo una vez abierto, para que futuras necesidades (p.ej. si se redacta un sucesor tipo N25) puedan decidir si esta fuente aporta algo que SICEE/PREP no dan.

---

## 6. `IETAM_TAMAULIPAS_SERIE_MUNICIPAL`

Receta de navegador ejecutable en menos de 1 minuto -- 4 URLs directas, cada una ya verificada hoy con curl -I (HTTP 200, content-type y Content-Length reales, no soft-404): pegar cada una en la barra de direcciones y guardar el archivo que el navegador ofrezca (nombre esperado entre paréntesis). (1) 2016: https://ietam.org.mx/PortalN/documentos/PE2015/Resultados/Concentrado_Ayuntamientos_2016.pdf (Concentrado_Ayuntamientos_2016.pdf, 556 374 B). (2) 2018: https://ietam.org.mx/PortalN/documentos/Municipios_2017-2018/Abasolo.xlsx como ejemplo de los 43 -- para el resto, sustituir "Abasolo" por cada uno de los 43 nombres de municipio que ya lista la página https://ietam.org.mx/PortalN/Paginas/EstadisticaEl/Estadistica_Electoral.aspx bajo "2017-2018" (Abasolo.xlsx, 58 881 B). (3) 2021: https://ietam.org.mx/PortalN/documentos/PE2020/Computos_electorales/Ayuntamiento.xlsx (Ayuntamiento.xlsx, consolidado 43 municipios en una hoja, 77 251 B). (4) 2024: https://ietam.org.mx/PortalN/documentos/PE2023/Computos_Finales/CONCENTRADO_DE_COMPUTOS_MUNICIPALES.xlsx (CONCENTRADO_DE_COMPUTOS_MUNICIPALES.xlsx, 171 703 B). Con (1)+(3)+(4) más los 43 de (2) se cubre VOTOS por municipio para los 4 años exactos de la cohorte g2018. Nota para quien ejecute: esto NO trae lista nominal (denominador) -- eso necesita, aparte, que mesa decida sobre las dos hermanas de la sección anterior (SICEE vía navegador para 2016-2024, o el ZIP de Zenodo/Larreguy para 2016-2018 solamente); esa segunda decisión es MESA-DECIDE, no bloquea el BAJAR de esta fila.

---

## Contador

Payloads `OBTENIDO` antes de este acto → después: **sin cambio** (0). Este acto no descarga (perímetro explícito del encargo); las 6 recetas de arriba son candidatas para que mesa ejecute, no adquisiciones consumadas. El contador que sí se mueve es el del encargo: filas con informe 0 → **28**.

