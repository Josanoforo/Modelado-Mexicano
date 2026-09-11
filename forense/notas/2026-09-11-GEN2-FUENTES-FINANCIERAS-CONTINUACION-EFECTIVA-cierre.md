# ACTO GEN2-FUENTES-FINANCIERAS-CONTINUACION-EFECTIVA · cierre

Fecha de ejecución: 11/sep/2026. Entorno: CAJA, Ubuntu/WSL2, Python
3.14.4, corpus local y red pública. Worktree propio:
`/home/pc0/mm-gen2-fuentes-financieras-continuacion`; rama:
`acto/gen2-fuentes-financieras-continuacion-efectiva`. Partió de
`origin/main=70c64d9ead92384ece0eaf18cbfb53372bb88a74`, que contiene el merge de
#717. El árbol inicial estaba limpio. La configuración local excluida de Git
quedó resuelta con `data/raices.local.yaml` y `data/raw` enlazado al corpus
compartido `/home/pc0/mm-corpus/raw`; la sonda acreditó red HTTP 200,
`data_raw=SI`, `descargas_mx=SI` y corpus resoluble antes de extraer.

Alcance: adquisición pública y extracción descriptiva. No se repite el
inventario de 29 CSV ni la identificación de ENCRIGE. Cero cambios al motor,
cron o evaluación; cero CALC, RESULT, parámetro o adopción.

## 1 · Resultado ejecutivo

- **A, satisfecha mediante equivalente oficial.** Banco de México publica
  una serie mensual de IMOR de banca comercial con cinco productos de consumo,
  123 meses continuos de 2016-01 a 2026-03. Es una publicación oficial
  equivalente y queda rotulada como tal: no es la exportación R16 CNBV ni se
  mezcla con la foto R16 de 2021-12. `NC-0163` cierra por la alternativa que su
  propio sucesor admitía.
- **B, satisfecha para descripción poblacional; residual causal abierto.** La
  ENSAFI 2023 observa hogares y personas consumidoras/deudoras. Entrega atraso
  por cuatro clases amplias de deuda con denominador de expuestos y estrategias
  ante insuficiencia de ingreso con denominador poblacional. No enlaza en una
  sola observación producto exacto, CAT/BNPL/baja fricción o usura y daño; por
  eso `NC-0164` sigue abierta con alcance reducido y no se adopta N34/R1.7.

## 2 · Tarjetas fijadas antes de descargar

### A · IMOR

| atributo | objeto requerido |
|---|---|
| institución/universo | sistema bancario oficial; cada publicación debe declarar inclusiones y exclusiones |
| producto | consumo total y clases separadas, no sólo agregado |
| frecuencia/periodo | mensual, historia continua y fechas explícitas |
| numerador | saldo vencido; desde IFRS9, saldo clasificado en etapa 3 si así lo define la fuente |
| denominador | saldo de cartera total del mismo producto y universo |
| escala | porcentaje de saldos, no probabilidad individual de mora |
| cambios relevantes | ruptura de definición en 2022-01, composición institucional y alcance de ABCD |

### B · N34

| atributo | objeto requerido |
|---|---|
| actor | consumidor-deudor, no empresa acreedora ni unidad administrativa |
| daño/causa | atraso, cobranza o venta/empeño de activos; distinguir respuesta ante insuficiencia de causa causal |
| producto | clase de crédito/deuda; idealmente producto exacto, CAT y canal BNPL/digital |
| población/periodo | población observada y referencia temporal explícitas |
| denominador | tenedores/expuestos con respuesta válida para prevalencia; no número de quejas |
| uso | separar contexto, conteos administrativos, prevalencia descriptiva y efecto causal |

La tarjeta orientó la adquisición; no constituye spec, medición sellada ni
autorización de adopción. El experimento Compartamos ya registrado conserva su
evidencia causal local y estrecha; ENSAFI añade prevalencia/contexto nacional,
no lo sustituye.

## 3 · A: serie oficial equivalente de IMOR

### 3.1 Procedencia y objeto

Publicación oficial: `Índices de morosidad del crédito al sector privado no
financiero`, tabla de Banco de México del Informe trimestral enero-marzo 2026:

`https://www.banxico.org.mx/TablasWeb/informes-trimestrales/enero-marzo-2026/B133C3DC-462F-40C1-B2BA-04086A1CFAB1.html`

| consulta | tamaño | SHA-256 | corpus fuera de Git |
|---|---:|---|---|
| 11/sep/2026 | 223,734 B | `c9691762bb6e086a08b4487f3d121ace04d74b31cfdc7e7a6c4c2512aa96c4b2` | `data/raw/GEN2_FUENTES_FINANCIERAS_CONTINUACION/banxico_imor_producto_2026T1.html` |

`curl` y `wget` produjeron bytes idénticos. El manifiesto usa la identidad
`gen2_banxico_imor_consumo_producto_mensual_2026t1_html`.

La tabla contiene banca comercial y señala que incluye Sofomes ER subsidiarias
de instituciones bancarias y grupos financieros. Excluye CI Banco. ABCD agrupa
adquisición de bienes de consumo duradero, incluidos muebles y automotriz. A
partir de enero de 2022 aplica IFRS9 y define IMOR como cartera etapa 3 entre
cartera total; antes se conserva el rótulo de cartera vencida. Este corte es
una ruptura metodológica: no se interpreta el salto 2021-12→2022-01 como cambio
económico limpio.

### 3.2 Extracción y controles

`data/fuentes-financieras-20/banxico-imor-consumo-mensual.csv` contiene 615
filas: 123 meses × consumo total, tarjeta de crédito, ABCD, nómina y personales.
Llave `fecha×producto`: 615 únicas, cero duplicados. Secuencia mensual esperada
2016-01..2026-03: 123/123, cero huecos y cero valores faltantes; no se interpoló
ni se convirtió vacío en cero.

El último mes disponible, 2026-03, registra 3.26% en consumo total, 3.35% en
tarjeta, 1.88% en ABCD, 2.77% en nómina y 5.29% en personales. El archivo
conserva por fila numerador, denominador, escala, frecuencia, universo y régimen
de definición. La foto CNBV 2021-12 permanece en
`cnbv-imor-consumo.csv`, separada y sin hacerse pasar por historia.

## 4 · B: consumidor-deudor en ENSAFI 2023

### 4.1 Datos y documentación

Ya estaban manifestados y coinciden con el corpus:

| objeto | tamaño | SHA-256 | archivo lógico |
|---|---:|---|---|
| base CSV | 5,027,338 B | `c0594079ddf4733d4f574d00f5e84290c62c5330eab0567dd867c26d42fafacd` | `ensafi2023/ensafi_2023_bd_csv.zip` |
| descriptor XLSX | 1,108,577 B | `37bd0cb6dd54ddb8d8962114971e60e06d2628e97eeb8b4e32269129d556ff4b` | `ensafi2023/ensafi_2023_fd_xlsx.zip` |
| cuestionario | 1,182,405 B | `d86c69f26d8b77de1d00b94d794b1e2ac01bd26aa101d3fca9e17287380c85fb` | `ensafi2023/ensafi_2023_cuestionario.pdf` |

Se incorporaron los dos documentos oficiales faltantes para fijar población,
diseño y contraste:

| objeto | consulta | tamaño | SHA-256 | corpus fuera de Git |
|---|---|---:|---|---|
| diseño muestral | 11/sep/2026 | 1,540,078 B | `80a097b28f55cf5b8282f8d0a656d52e0d9b21693663c4f52803f55985a0fb31` | `GEN2_FUENTES_FINANCIERAS_CONTINUACION/ensafi_2023_diseno_muestral.pdf` |
| presentación de resultados | 11/sep/2026 | 1,545,505 B | `4ad641dff0c90b389044d85efb975ced2dc21fd6a820bab6903b560a32d802ef` | `GEN2_FUENTES_FINANCIERAS_CONTINUACION/ensafi_2023_presentacion_resultados.pdf` |

URLs oficiales:

- diseño: `https://www.inegi.org.mx/contenidos/productos/prod_serv/contenidos/espanol/bvinegi/productos/nueva_estruc/889463916840.pdf`;
- resultados: `https://www.inegi.org.mx/contenidos/programas/ensafi/2023/doc/ensafi_2023_presentacion_resultados.pdf`;
- cuestionario: `https://www.inegi.org.mx/contenidos/programas/ensafi/2023/doc/ensafi_2023_cuestionario.pdf`.

Las dobles descargas de los dos documentos nuevos coincidieron. ENSAFI tiene
diseño probabilístico, multietápico, estratificado y por conglomerados; la
unidad última es la persona de 18 años y más. `FAC_HOG` y `FAC_ELE` son los
factores de expansión apropiados para las dos tablas; el corpus también expone
`EST_DIS` y `UPM_DIS` para una futura spec inferencial.

### 4.2 Variables contrastadas contra cuestionario y descriptor

- Hogar: `P4_7_1..4` identifica tenencia de cuatro clases de deuda y
  `P4_8_1..4` atraso durante el último mes en la misma clase. La primera clase
  agrega tarjeta o crédito bancario, financiero o de tienda; las otras son
  caja/familia/amistades, casa de empeño y prestamista/agiotista.
- Persona: `P6_7` pregunta si se ha atrasado en alguno de sus préstamos o
  créditos; `P6_8` identifica personas con deuda, pero `P6_7` no liga el atraso
  a uno de los productos de `P6_6` ni explicita ventana temporal.
- `P6_9=2` identifica ingreso insuficiente en el último mes y `P6_10_1..8`
  las respuestas múltiples, entre ellas vender/empeñar, usar crédito y atrasar
  otro pago. La condición describe contexto y afrontamiento; no demuestra que
  un producto crediticio causó la insuficiencia.

### 4.3 Resultados descriptivos y denominadores

`ensafi2023-atraso-deuda-producto-hogar.csv` conserva expuestos, respuestas
desconocidas, denominador válido y masas ponderadas:

| clase de deuda | n expuestos | desconocido | n denominador | masa denominador | masa atraso | porcentaje |
|---|---:|---:|---:|---:|---:|---:|
| formal agregada | 4,897 | 42 | 4,855 | 8,841,713 | 2,460,369 | 27.8268% |
| caja/familia/amistades | 922 | 1 | 921 | 1,618,454 | 486,892 | 30.0838% |
| casa de empeño | 399 | 2 | 397 | 637,557 | 176,344 | 27.6593% |
| prestamista/agiotista | 354 | 3 | 351 | 601,995 | 197,577 | 32.8204% |

Las clases no son mutuamente excluyentes; no se suman como personas únicas.

`ensafi2023-deuda-y-afrontamiento-persona.csv` reproduce el 27.3% oficial: de
7,894 personas muestrales con deuda, masa expandida 33,603,460, 2,295 reportan
atraso, masa 9,161,224, estimación 27.2627%. Entre personas cuyo ingreso no
alcanzó para cubrir gastos sin endeudarse (`n=6,224`, masa 28,288,447), 10.2793%
usó tarjeta o pidió crédito formal/de tienda, 10.0741% atrasó un crédito o
préstamo y 9.7363% vendió o empeñó un bien. Las ocho estrategias completas se
publican, sin forzar una partición.

Estos son estimandos descriptivos ponderados, no un CALC sellado con errores
estándar. No hay tasa de BNPL, CAT/usura, cobranza abusiva ni efecto causal.

## 5 · Tabla de uso

| objeto | variable/estimando | consumidor | uso permitido | limitación | siguiente cálculo posible |
|---|---|---|---|---|---|
| Banxico IMOR mensual | IMOR de saldos por mes×producto | R1.6 / `dinero.credito.scoring_alternativo` | contexto temporal y comparación dentro de régimen | banca comercial, no R16 ni riesgo individual; ruptura 2022-01 | spec de tendencia/volatilidad separada por régimen, sin cruzar IFRS9 como serie homogénea |
| ENSAFI hogar | `P4_8_j=1` entre `P4_7_j=1` y respuesta válida | N34/R1.7 | prevalencia nacional descriptiva por clase amplia de deuda | clase formal agregada; no CAT, BNPL o causalidad | spec con `FAC_HOG`, `EST_DIS`, `UPM_DIS`, dominios y varianza de encuesta si mesa acepta las clases |
| ENSAFI persona | `P6_7=1` entre `P6_8=1..4` | N34/R1.7 | prevalencia general de atraso entre personas con deuda | atraso no ligado a producto y sin ventana explícita | estimación con diseño completo, sólo como contexto general |
| ENSAFI afrontamiento | `P6_10_k=1` entre `P6_9=2` y respuesta válida | N34/R1.7 | respuestas múltiples ante insuficiencia de ingreso | asociación/contexto, no mecanismo causal por producto | tabulación de dominios preespecificados; no mediación causal sin diseño nuevo |
| Compartamos preexistente | ITT de atraso en crédito grupal, Nogales | N34/R1.7 | dirección causal en población y producto estrechos | no prevalencia nacional, CAT o BNPL | síntesis explícita de transportabilidad; no combinar numéricamente sin decisión |

## 6 · Incorporación canónica y reproducibilidad

El manifiesto añadió sólo los tres payloads nuevos. El registro de adquisición
se actualiza mediante `tools/curador_registro/tsv_crudo.py::upsert_fila`, por
`fuente_canonica`, y la proyección se regenera con
`tools/vista_cola_adquisicion.py`. Se añadieron las identidades estables
`BANXICO_IMOR_CONSUMO_POR_PRODUCTO_MENSUAL` y
`ENSAFI_2023_N34_CONSUMIDOR_DEUDOR`; las filas históricas CNBV/ENCRIGE conservan
su identidad y alcance. `NC-0163/0164` se concilian por `id` mediante el mismo
escritor canónico.

El extractor ahora produce nueve tablas, incluidas las tres nuevas, y
`--verifica` las reconstruye byte a byte:

```bash
python3 tools/extrae_fuentes_financieras.py
python3 tools/extrae_fuentes_financieras.py --verifica
python3 tools/extrae_fuentes_financieras.py --actualiza-registro
python3 tools/vista_cola_adquisicion.py
python3 tests/test_fuentes_financieras.py
```

## 7 · Obligaciones y residual

| capa | A · IMOR | B · N34 |
|---|---|---|
| documentación obtenida | HTML Banxico con notas metodológicas | diseño y presentación ENSAFI; cuestionario/descriptor verificados |
| datos obtenidos/reutilizados | 123 meses×5 productos | THOGAR y TMODULO del paquete ya manifestado |
| extracción ejecutada | 615 filas, continuidad/duplicados/faltantes controlados | 4 prevalencias hogar + 9 estimandos persona, denominadores y desconocidos explícitos |
| necesidad científica | satisfecha por publicación oficial equivalente; R16 exacto no se afirma | satisfecha para descripción poblacional consumidor-deudor; mecanismo causal completo no |
| parámetro adoptado | ninguno | ninguno |

No persiste un acceso externo indispensable para entregar A ni el componente
descriptivo de B, así que no se repiten los expedientes de #715. Como mejora
opcional —no condición de este cierre—, una solicitud CNBV exacta pediría el
reporte 040-1A-R16 para Total Banca Múltiple, meses 2016-presente, con periodo,
institución, producto, cartera vencida/etapa 3, cartera total, IMOR, diccionario
y puente IFRS9, en CSV/XLSX; el titular tendría que presentar la solicitud por
el canal oficial con su identidad real.

El residual `NC-0164` es científico, no un URL fallido: hace falta una fuente o
instrumento que enlace en la misma unidad producto exacto —incluido BNPL o
crédito digital—, exposición/costo/CAT o fricción, atraso/cobranza/venta de
activos, periodo, negativos, pesos y diseño. La acción siguiente concreta es
que mesa decida si los estimandos amplios de ENSAFI ameritan una spec de
encuesta; sólo después se calcularían incertidumbre y dominios con
`FAC_HOG/FAC_ELE`, `EST_DIS` y `UPM_DIS`. Esa spec no puede convertir la
asociación en causalidad ni unir variables que ENSAFI no enlaza.

**Contador científico:** cero. **Adopciones:** cero.
