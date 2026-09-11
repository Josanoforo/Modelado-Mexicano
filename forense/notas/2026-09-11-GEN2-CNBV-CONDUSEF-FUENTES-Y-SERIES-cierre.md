# ACTO GEN2-CNBV-CONDUSEF-FUENTES-Y-SERIES · cierre

Fecha de ejecución: 11/sep/2026. Entorno: CAJA, Ubuntu/WSL2, Python 3.14.4,
corpus compartido montado en `data/raw` mediante la configuración local excluida
de Git. Worktree absoluto:
`/home/pc0/mm-gen2-encola-post707`; rama:
`acto/gen2-fuentes-financieras-20`; el archivo del encargo quedó archivado en el
commit A.3 `76d11d99f998247d556200525a5fb82346867a2a`. La rama partió del `main`
disponible `a37837a0df69240e35c160a53c5c1de209f9be01`, que ya contiene el corte
#708 requerido. No había rama ni PR abierto del mismo objeto. Estado inicial
limpio; corpus con 403 payloads resolubles desde `data_raw+descargas_mx`.
Antes de cerrar se integró `origin/main=f6c93326048c7219181bd903a2fd41857265831e`
(PR #714, que contiene #712) y se conciliaron sus cambios compartidos. Ese
merge tomó ADR-474; por la regla de la casa, este acto renumeró provisionalmente
a ADR-475. La sincronización posterior con `origin/main=36e6b3f` incorporó el
PR #713, que ya ocupaba ADR-475 y NC-0160/0161/0162; el cierre final queda en
ADR-476 y sus reservas en NC-0163/0164.

Alcance: adquisición y extracción descriptiva. Cero llamadas a modelos, cero
cambio a motor, `milpa/`, capturas, R, sellos históricos, cron o métodos
pendientes de firma. No se crea CALC ni se adopta parámetro.

## 1 · Resultado ejecutivo

- **CNBV: `OBTENIDO-PARCIAL`.** Se obtuvo, registró y extrajo el XLS oficial
  `040-01A-R16 Balance: IMOR por tipo de cartera`, pero el archivo público sólo
  contiene una foto cacheada de diciembre de 2021. La macro que produciría la
  historia depende de una conexión interna de CNBV. La serie mensual pública
  solicitada queda en barrera externa demostrada; no se fabricó continuidad.
- **CONDUSEF: 29/29 CSV verificados y explotados.** Se entregan inventario y
  tres agregados reproducibles. Los conteos administrativos se conservan por
  canal/sistema/edición; nunca se transforman en prevalencia entre clientes.
- **ENCRIGE 2020: identidad y alcance resueltos.** El paquete tabulado y el
  cuestionario ya estaban manifestados; la ficha de diseño oficial sí era el
  documento faltante y se adquirió. El reactivo 4.2 observa a la empresa
  acreedora/contratante frente a contrapartes privadas, no daño al consumidor
  deudor. La adquisición queda `OBTENIDO`; la demanda científica N34 no.

## 2 · CNBV: objeto obtenido y barrera exacta

### 2.1 Ruta oficial e identidad

El flujo vigente parte del portal oficial
`https://portafolioinfo.cnbv.gob.mx/Paginas/Reporte.aspx?s=40&t=26&st=0&ti=0&sti=0&n=0&tp=0`.
El HTML carga
`https://picomponentebi.cnbv.gob.mx/ReportViwer/index?...`; ese componente hace
un GET a `/ReportViwer/Agrupados` con `Sector=40`, `Tema=26`, los subtemas en
cero y `TipoPortafolio=0`. La respuesta oficial lista directamente:

`https://portafolioinfdoctos.cnbv.gob.mx/Documentacion/minfo/XLS/40/040_1a_R16.xls`

La cadena del servidor no aportó el intermedio. Se descargó el certificado
oficial `GlobalSign RSA OV SSL CA 2018` desde
`http://secure.globalsign.com/cacert/gsrsaovsslca2018.crt`, se convirtió DER a
PEM y se añadió sólo al bundle temporal de la ejecución. No se usó `-k` ni se
desactivó la validación TLS. Dos clientes independientes (`curl` y `wget`)
produjeron bytes idénticos:

| objeto | tamaño | SHA-256 | ubicación fuera de Git |
|---|---:|---|---|
| `040_1a_R16.xls` | 5,491,712 B | `3b6ac444df102a4b6cecf0a24469471940bb9cc838e82b3c304e17bc56491629` | `data/raw/GEN2_FUENTES_FINANCIERAS_20/040_1a_R16.xls` |

El manifiesto lo registra como
`gen2_cnbv_040_1a_r16_imor_tipo_cartera`.

### 2.2 Unidad, punto disponible y faltantes

El indicador se fijó antes de extraer como **IMOR = cartera vencida / cartera
total del segmento**, unidad porcentaje de saldos, universo `Total Banca
Múltiple`, periodicidad nominal mensual y producto separado. No es probabilidad
individual de impago. El único periodo contenido es `2021-12`: consumo total
3.3494%; tarjeta 3.6436%; personales 5.2126%; nómina 2.3573%; ABCD 2.8536%;
automotriz 2.1309%; adquisición de bienes muebles 6.0811%; otros créditos de
consumo 2.7356%. Operaciones de arrendamiento capitalizable está vacío en el
original y permanece vacío: la hoja de notas dice que vacío es no reportado,
no cero.

Principio, medio y final no pueden contrastarse como tres periodos: hay una sola
fecha única. El control correcto fue contrastar las nueve filas del corte con
la hoja `MINFO`, comprobar fecha/universo/producto y exigir unicidad
`fecha×producto`. La salida se denomina explícitamente foto, no serie.

### 2.3 Exportación manual exacta y punto de bloqueo

La receta reproducible para una persona autorizada es:

1. Abrir la URL del reporte anterior en navegador con TLS estricto.
2. En la lista de reportes abrir `040-01A-R16 Balance: IMOR por tipo de
   cartera` y guardar el XLS original.
3. Abrirlo en Excel de escritorio, inspeccionar la firma/código de macro y sólo
   entonces habilitar contenido; en **Datos → Actualizar todo**, elegir los
   meses e instituciones y exportar la hoja `MINFO` como XLSX/CSV sin alterar
   porcentajes ni vacíos.
4. Si la actualización falla, documentar el error de conexión: `lee()` intenta
   leer `\\sector5\DGAIN\MINFO\dgaex.txt`; después abre `ADODB.Connection` y la
   consulta del libro ejecuta `sp_obtiene_reporte '040_1a_R16'`. Esa ruta UNC y
   la base no son públicas ni se resuelven desde el navegador/CLI externo.

Se intentaron las dos rutas razonables. La plantilla R16 directa entrega sólo
202112 y su actualización exige infraestructura interna. La sección oficial
`4.-Series Históricas` de la misma respuesta `Agrupados` sólo lista R1, R2 y
R8A-R2, no R16/IMOR por producto. La sección de indicadores ofrece reportes
relacionados, pero no la historia del mismo objeto. Por ello el residual es una
barrera externa específica y comprobable, no otra lista de URLs.

## 3 · CONDUSEF: 29 archivos, unidades y agregados

El extractor resuelve contra manifiesto exactamente 29 identidades: 26 bajo
`A6_CONDUSEF_DATOS_ABIERTOS/` y tres bajo `condusef_redeco_reune/`. Verifica
SHA-256, tamaño, codificación, ancho de cada fila y encabezados antes de
agregar. No había diccionario adjunto entre esos 29 payloads. Los catálogos
oficiales de datos abiertos describen las colecciones anuales de acciones e
instituciones y las ediciones del Buró, pero no definen una correspondencia que
permita colapsar `GO`, `GE`, `REDECO`, `CO`, `DT`, `SDLG`, `DLG`, `AJP` o `CM`;
se conservaron las etiquetas literales y nunca se sumaron canales como casos
únicos.

Resultados descriptivos auditables:

- Acciones 2024: 1,290,853 asesorías; 168,166 `GE`; 41,922 `REDECO`; 28,243
  `CO`; 9,149 `DT`. En 2025: 1,082,663; 161,582; 48,448; 27,744; 8,793,
  respectivamente. Es comparación de canales homónimos publicados, no conteo
  de personas ni expedientes deduplicados.
- Reclamaciones por sistema: en 2024, CONDUSEF 195,153 y REUNE 7,263,310; en
  2025, 137,562 y 7,212,426. Banca múltiple concentra 60.386% y 71.891% dentro
  de CONDUSEF, y 88.872% y 93.843% dentro de REUNE. Los archivos de
  instituciones de 2024 y 2025 tienen 766 y 80 filas, respectivamente: la
  cobertura cambió y las diferencias no se presentan como tendencia causal.
- Las dos ediciones `evaluacion_producto_BEF` suman 2,447,339 y 582,304
  reclamaciones; tarjeta de crédito representa 83.166% y 79.863% dentro de cada
  edición. Ningún CSV incluye periodo para esas ediciones; se rotulan
  `NO_INCLUIDO_EN_CSV` y no se calcula cambio temporal.

Los CSV REDECO/REUNE aquí disponibles son directorios de despachos/unidades, no
tablas de quejas con causa. Los archivos de reclamaciones tienen institución,
clase y conteo, sin causa ni denominador de clientes. Ninguno identifica BNPL o
usura. Por tanto estos objetos describen actividad administrativa, pero no
estiman prevalencia de daño ni satisfacen por sí solos N34.

## 4 · ENCRIGE 2020: identidad, diseño y lado observado

El censo del 11/sep mostró que `conjunto_de_datos_encrige_2020_csv`
(ZIP, 392 miembros, SHA-256 `068649…`) y `encrige2020_cuestionario` (SHA-256
`f410…`) ya estaban manifestados: la ausencia declarada por la receta anterior
era obsoleta. Se adquirió el diseño muestral oficial, edición 2021:

| objeto | tamaño | SHA-256 | ubicación fuera de Git |
|---|---:|---|---|
| diseño muestral ENCRIGE 2020 | 1,185,888 B | `3f314258dc4ad0ddc5a4b94b327c763f3ff8c2abacf0bcac0a171519ce479961` | `data/raw/GEN2_FUENTES_FINANCIERAS_20/encrige2020_diseno_muestral.pdf` |

URL oficial:
`https://www.inegi.org.mx/contenidos/productos/prod_serv/contenidos/espanol/bvinegi/productos/nueva_estruc/889463901969.pdf`;
ID de manifiesto: `gen2_encrige2020_diseno_muestral`. `curl` y `wget`
coincidieron byte a byte.

Población objetivo: unidades económicas privadas con instalaciones fijas de
industria, comercio y servicios; excluye agricultura y gobierno. Marco RENEM de
4,129,983 unidades a partir de CE2019; muestra probabilística estratificada de
34,919 y 29,482 recuperadas. El factor de expansión es el inverso de la
probabilidad de selección, ajustado por no respuesta en dominio-estrato; las
tablas publicadas son estimaciones expandidas, no microdato crudo.

El reactivo 4.2 pregunta si **la empresa encuestada** tuvo problemas de cobranza
o incumplimiento con inversionistas, proveedores, compradores, arrendatarios u
otras contrapartes. 4.3 pregunta el mecanismo de solución y 4.4 el proceso
judicial. Resultados publicados: 439,456.4445 de 4,129,982.9109 unidades
expandidas, 10.6406%, reportan el problema; 394,571.6545 de 439,456.4445,
89.7863%, reportan acuerdo entre particulares. Sin micro, 70,604.2058 de
587,028.9146, 12.0274%, reportan el problema, y 18,461.4213 de 70,604.2058,
26.1478%, acudieron a tribunales. Juicio (89.6912%) y conciliación (15.4598%)
son respuesta múltiple y no forman una partición.

Esto identifica el lado empresa acreedora/contratante y sus mecanismos; no
identifica consumidor deudor, crédito al consumo, BNPL ni usura. Es evidencia
contextual posible para N34, no sustituto de quejas de consumidores ni permiso
de adopción.

## 5 · Mapa de uso

| fuente | unidad / periodo | hallazgo descriptivo | consumidor posible | qué no identifica | siguiente uso |
|---|---|---|---|---|---|
| CNBV R16 | porcentaje de saldos, Total Banca Múltiple, 2021-12 | IMOR total consumo 3.3494%, ocho productos y un faltante explícito | R1.6 / `dinero.credito.scoring_alternativo` | probabilidad individual, segmento popular, historia pública | obtener exportación histórica mediante acceso CNBV o una publicación oficial estática equivalente; después fijar una spec antes de cualquier CALC/adopción |
| CONDUSEF acciones/reclamaciones | conteos administrativos, 2024/2025 o corte rotulado | distribución por canal, sistema, sector/clase y producto | N34 / `dinero.credito.baja_friccion_usura_dano_downstream` | clientes expuestos, causa en estas tablas, BNPL/usura, expedientes únicos | buscar tabla oficial con causa y denominador compatible; mantener REUNE/CONDUSEF separados |
| ENCRIGE 2020 | unidades económicas expandidas, nacional 2020 | problemas contractuales y mecanismos desde el lado de la empresa | contexto de N34 | consumidor deudor y producto de crédito | no adoptar para N34; usar sólo si una spec futura necesita el lado empresa |

## 6 · Productos reproducibles y registro

`tools/extrae_fuentes_financieras.py` escribe seis tablas y `--verifica` exige
igualdad byte a byte:

| tabla | filas de datos | función |
|---|---:|---|
| `cnbv-imor-consumo.csv` | 9 | corte CNBV, unidad y faltante explícito |
| `condusef-inventario.csv` | 29 | identidad, estructura, periodo/corte y límites de cada payload |
| `condusef-acciones-defensa.csv` | 531 | agregados por periodo×sector×clase×canal |
| `condusef-reclamaciones-clase.csv` | 58 | CONDUSEF y REUNE separados por periodo×sector×clase |
| `condusef-reclamaciones-producto.csv` | 150 | agregados por edición×sector×producto, sin periodo inventado |
| `encrige2020-cumplimiento-contratos.csv` | 6 | indicadores publicados con denominador, diseño y actor |

`--actualiza-registro` usa el escritor canónico de
`tools/curador_registro/tsv_crudo.py` por `fuente_canonica`, no por
`fila_origen`: ambas filas afectadas comparten históricamente `fila_origen` y
esa no es una llave. Se regeneró sólo `data/cola-adquisicion-v1_0.tsv`.
`CNBV_PORTAFOLIO_INFORMACION_IMOR_CONSUMO` queda `OBTENIDO-PARCIAL` y
`ENCRIGE_2020_FD_COMPLETO_MAS_CONDUSEF`, `OBTENIDO` en adquisición. Estado de
archivo, utilidad científica y adopción permanecen separados.

Comandos:

```bash
python3 tools/extrae_fuentes_financieras.py
python3 tools/extrae_fuentes_financieras.py --verifica
python3 tools/extrae_fuentes_financieras.py --actualiza-registro
python3 tests/manifiesto.py --verifica --id gen2_cnbv_040_1a_r16_imor_tipo_cartera
python3 tests/manifiesto.py --verifica --id gen2_encrige2020_diseno_muestral
python3 tests/test_fuentes_financieras.py
```

## 7 · Obligaciones, satisfacción y residual

| obligación | evidencia | alcance satisfecho | residual |
|---|---|---|---|
| serie CNBV o barrera externa con exportación exacta | XLS oficial registrado, corte reproducible, inspección de hojas/VBA y §2.3 | corte 2021-12 utilizable y barrera demostrada | historia mensual R16 requiere conexión interna CNBV o publicación estática oficial |
| agregados efectivos de 29 CSV | inventario 29/29 y tres tablas CONDUSEF | identidad, unidad, granularidad y agregación reproducibles | no hay causa/BNPL ni denominador de clientes; cortes no siempre comparables |
| identidad/alcance ENCRIGE | paquete, cuestionario, diseño y tabla de seis resultados | ola 2020 y actor/diseño resueltos | no satisface daño de consumidor-deudor N34 |
| incorporación canónica | dos altas de manifiesto, dos filas de registro y proyección regenerada | adquisición trazable sin reescribir corpus ajeno | ninguna cifra queda adoptada |
| pruebas de unidad/duplicación/faltantes | prueba dirigida y `--verifica` | porcentaje≠fracción, conteos enteros, denominadores, vacíos y llaves controlados | suite integral se reporta en el cierre mecánico |
| FP-324 / recetas 3 y 4 | esta nota y filas registrales | receta CNBV ejecutada hasta barrera; receta ENCRIGE+CONDUSEF ejecutada | recetas 1 (RUPC) y 5 (OECD PUM) permanecen abiertas; N34 y la serie CNBV siguen científicamente pendientes |

## 8 · A.8 y contadores

El censo se ejecutó antes de fijar estados: ENCRIGE y su cuestionario ya
existían en manifiesto; no se contabilizan como adquisiciones nuevas. Se
añadieron sólo el XLS CNBV y la ficha de diseño ENCRIGE. No se usaron como
fuentes empíricas documentos de encargos del censo #707. No hay medición GEN2,
`RESULT`, parámetro ni adopción nuevos: **contador científico = cero**.

`A.8` también se ejerció sobre los dos consumidores nombrados en el encargo.
Salida terminal de `python3 tools/ya_medido.py dinero.credito.scoring_alternativo`:

```text
resuelto por canon: dinero.credito.scoring_alternativo -> R1.6
milpa/tramite.yaml: sin apariciones
milpa/tramite-ola5-propuesta-v0.yaml: sin apariciones
data/corrida0: sin apariciones
canon/modelo-decision-v4_0.md §7: R1.6, tier [MEDIA], medido No
NUNCA-MEDIDA
```

Salida terminal de
`python3 tools/ya_medido.py dinero.credito.baja_friccion_usura_dano_downstream`:

```text
resuelto por canon: dinero.credito.baja_friccion_usura_dano_downstream -> R1.7
milpa/tramite.yaml: sin apariciones
milpa/tramite-ola5-propuesta-v0.yaml: sin apariciones
data/corrida0: sin apariciones
canon/modelo-decision-v4_0.md §7: R1.7, tier [MEDIA], medido No
NUNCA-MEDIDA
```

Son negativos de medición, no ausencias de fuente: este acto sólo entrega
insumos descriptivos y mantiene cualquier definición futura antes del cálculo.
