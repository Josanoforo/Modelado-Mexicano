# ASTRA-2 · localización dirigida de visitas y seguro basal (2026-09-23)

**Estado:** no se recuperaron las tablas fuente del desenlace de
`RES-0087`. El mapa y el diagnóstico permanecen válidos; la primera
medición sigue `NO-ESTIMABLE`, sin CALC/RESULT ni adopción de θ.

## Inventario local y depósito primario

1. `corpus/`, `data/raw/seguro_popular_rct/`, el corpus compartido
   `/home/pc0/mm-corpus/raw/seguro_popular_rct/` y los seis registros
   `astra_sp_rct_*` de `data/manifiesto.yaml` contienen `ALL.tab`, lista
   de pares, dos codebooks, README y archivo de réplica. No contienen
   `tbl_seccion11_vis.dta`, `tbl_seccion11_vis.RData`, tabla homóloga final
   ni tabla fuente de personas/seguro. El tar de réplica incluye scripts,
   índices y resultados derivados, pero ninguno de esos archivos fuente.
2. La [API del depósito primario](https://dataverse.harvard.edu/api/datasets/:persistentId/?persistentId=doi:10.7910/DVN/P6NC0M)
   enumera 17 objetos en la versión 6.2. Además de los seis registrados,
   publica cuestionarios, tablas geográficas/de conglomerados y dos
   planillas de validación. No enumera las tablas de visitas ni de personas.
   Se descargaron **solo para inspeccionar encabezados**
   `combined6statesfinal.tab` (117 columnas, unidad de conglomerado) y
   `DATABASERURALALL3km.tab` (161 columnas, geografía rural); ninguno
   contiene los cuatro reactivos de motivo/lugar, los códigos de seguro
   basal o llaves de persona/hogar requeridos. No se leyeron filas de
   desenlace ni se eligió una variable sustituta.
3. El código primario del propio depósito,
   `Eval/utilization.formerge.R`, intenta leer
   `tbl_seccion11_vis.RData` (y comenta el origen
   `tbl_seccion11_vis.dta`); usa `P11D0501` como lugar de visita. Su
   `Eval/Insurance.formerge.R` exige `tbl.personas` ya cargada y extrae
   `P01D12`, `P01D1301` y `P01D1501` del entrevistado seleccionado.
   Estas rutas explican el faltante concreto; un índice `.dta` de
   variables dentro del tar no contiene la tabla de visitas.

La [página de réplica de King y coautores](https://gking.harvard.edu/publications/replication-data-public-policy-poor-randomised-assessment-mexican-universal-healt/)
remite a ese depósito. La [DGED de la Secretaría de Salud](https://salud.gob.mx/unidades/evaluacion/seguropopular/seguropopular.htm)
identifica al INSP como recolector de información primaria y a DGED como
colaborador de la evaluación. La siguiente solicitud dirigida es al equipo
de réplica y a DGED/INSP por: (a) visitas basal y seguimiento al nivel de
persona×visita, (b) seguro basal individual y diccionario de códigos,
(c) llaves originales de persona, hogar, conglomerado y par, (d) marco y
motivo de exclusión de los 24 pares entre los 74 iniciales y los 50
observados, y (e) condiciones de uso. La fila de
`solicitud-adquisicion.tsv` fija el criterio de aceptación; no se ha
enviado una petición a terceros desde esta rama.

## Regla antes de estimar

Si llegan las tablas y sus términos permiten usarlas, registrarlas con
id/hash/tamaño y cotejar códigos y uniones sin duplicados. **Antes de abrir
resultados**, añadir una enmienda prospectiva a la spec que distinga 74
pares inicialmente aleatorizados de 50 observados, defina la población
del ITT y fije cómo se tratará la pérdida de 24 pares (motivos, balance
basal, atrición por brazo y análisis de sensibilidad). Conservar intacto
el preregistro `c529cdf0` y `diagnostico-salud-oferta.json`.

## Siguiente ruta del mapa

Si no se obtienen esos archivos, la siguiente ruta es `AT-25` /
`RES-0091`, exposición a trámite digital registrable y solicitud/entrega
de mordida. El consumidor preciso es
`milpa/procedencia.yaml:asignados_probabilidad:tramite.mordida.con_registro`
(`asignados_probabilidad[9]`). ENCIG 2021/2023 ya está adquirida; el
insumo faltante es el calendario **efectivo** por entidad×servicio×fecha,
incluidas suspensiones, obligatoriedad y cobertura del código `05`. Solo
si permite aislar servicios tratados y controles comparables se podrá
preregistrar un DiD. Un ITT de utilización ambulatoria total disponible
en `ALL.tab` no responde al desenlace congelado ni actualiza `RES-0087`.
