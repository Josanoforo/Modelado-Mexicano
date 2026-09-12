# ACTO GEN2-N34-DATOS-PRODUCTO-Y-DANO · cierre

Fecha de ejecución: 11/sep/2026. Entorno: CAJA, Ubuntu/WSL2, Python 3.14.4,
corpus compartido y red pública. Worktree propio:
`/home/pc0/mm-gen2-n34-datos-producto-dano`; rama:
`acto/gen2-n34-datos-producto-y-dano`; base inicial efectiva:
`origin/main=d9c251954bce1c08abba6f47696adde9d7a2913a`, que ya contiene el merge
de #726/#732. El árbol inicial estaba limpio. El worktree principal ajeno
tenía un `error.log` sin seguimiento y no se tocó.

Al arrancar estaban abiertos #727–731. #730 es la medición ENSAFI con diseño:
este acto no repite sus 13 estimandos ni toca sus CALC/RESULT. Tampoco repite
IMOR, el inventario CONDUSEF ni ENCRIGE de #717/#723. Se enlazó `data/raw` al
corpus compartido `/home/pc0/mm-corpus/raw` y se creó el staging exclusivo
`GEN2_N34_PRODUCTO_DANO`. La sonda de entorno verificó Python, dependencias,
las dos raíces lógicas y 406 archivos del corpus; su prueba HTTP a INEGI dio
`000`, pero las descargas directas por TLS funcionaron y cada objeto se obtuvo
dos veces con bytes idénticos.

Alcance: adquisición, lectura de estructura y preparación de insumos. Cero
parámetros, CALC, RESULT, adopciones o inferencias causales nuevas; cero cambios
al motor, F5, cron, selector o `tools/adq_*`.

## 1 · Resultado ejecutivo

- **México, asociación utilizable.** Banco de México publica un XLSX de 12,408
  filas persona-ola y 142 columnas para 2019–2024, con ponderador. En una misma
  fila observa la categoría inequívoca de cinco productos de crédito, la
  percepción de intereses/comisiones y facilidad de contratación, el
  comportamiento de pago —incluido atraso o imposibilidad de pago—, problemas,
  reclamación y vulnerabilidad. Es la primera fuente mexicana de este residual
  que permite enlazar producto, condición de costo y daño en la misma unidad.
  No identifica institución, CAT contractual ni una asignación exógena: habilita
  descripción y asociación, no causalidad.
- **BNPL, mecanismo extranjero utilizable.** SHED 2025 aporta microdato público
  de 12,934 personas en Estados Unidos y co-observa uso de BNPL, atraso, cargo
  extra por atraso, sobregiro/NSF disparado por el pago y si BNPL fue la única
  forma de poder comprar. Trae `weight` y `weight_pop`. Sirve para estructura y
  mecanismo BNPL; nunca como tasa mexicana ni efecto causal.
- **BNPL, corroboración agregada.** El informe CFPB 2025 permite reproducir su
  Table 3: 892,668 originaciones pay-in-four de seis firmas emparejadas con
  registro crediticio, con participación y default a 120 días por categoría
  FICO. Sólo se adquirió el PDF: los datos subyacentes no son públicos.
- **Causalidad mexicana ya existente.** El paquete Compartamos AEJ
  `116334_v1` ya estaba adquirido y ejercido. Su RCT enlaza oferta aleatoria de
  crédito grupal y mora administrativa en 16,560 mujeres de Nogales; se
  reutiliza, no se vuelve a descargar. Sigue sin medir CAT ni BNPL y su
  transportabilidad es estrecha.

`NC-0164` **permanece abierta**. El acto cubre la capa asociativa mexicana y
añade medición posible del mecanismo BNPL extranjero, pero no satisface el
alcance conjunto de producto BNPL/digital o CAT en México más identificación
causal de daño.

## 2 · Pregunta y campos fijados antes de adquirir

| campo | mínimo deseado | criterio aplicado |
|---|---|---|
| unidad | persona/hogar deudor | se excluye como fuente principal toda tabla sólo de institución o cartera |
| país/periodo | México y fecha; otro país sólo como mecanismo | fuentes estadounidenses llevan rótulo explícito de no transporte |
| producto/exposición | lender o categoría inequívoca | Banxico fija cinco categorías; SHED/CFPB fijan BNPL; Compartamos fija lender y crédito grupal |
| costo/condición/fricción | CAT, tasa, comisiones, baja fricción o condición de acceso | percepción de interés no se llama CAT; asequibilidad/autopago no se llama tasa |
| daño | atraso, impago, cargo, sobregiro, cobranza o venta de activos | satisfacción sola no cuenta como daño; problema/reclamación es fricción, rotulada |
| denominador | tenedores/expuestos y negativos, con ponderador/diseño si existe | las tablas conservan n válido y masa; no convierten quejas en prevalencia |

Ninguna fuente tenía que llenar simultáneamente las seis columnas para
conservar valor. El nivel de uso se asignó por lo que sí observa, no por el
título de la publicación.

## 3 · Primera pasada: seis conjuntos candidatos

La búsqueda se separó entre BNPL, crédito digital/aplicaciones, costo del
crédito y consecuencias del sobreendeudamiento en México. La tabla completa y
legible por máquina es `data/n34-producto-dano/candidatos-n34.csv`.

| candidato | bytes/datos | nivel alcanzado | decisión |
|---|---|---|---|
| Banxico, satisfacción de personas usuarias 2019–2024 | XLSX + manual + informe públicos | asociación potencial México | priorizado y adquirido |
| Federal Reserve SHED 2025 | CSV + codebook públicos | descripción/asociación BNPL, EE. UU. | priorizado y adquirido |
| CFPB, BNPL y deuda no garantizada 2025 | sólo informe/tablas; fuente administrativa no publicada | asociación agregada, EE. UU. | adquirido como corroboración |
| Compartamos AEJ RCT | paquete público ya en corpus | causal estrecho, México | reutilizado sin duplicar bytes |
| CFPB Making Ends Meet public-use file | exige aceptar un acuerdo de uso al acceder | asociación BNPL+buró | no adquirido: el encargo prohíbe aceptar compromisos |
| Di Maggio, Williams y Katz, NBER w30508 | panel transaccional propietario; no se localizó réplica pública | causal en paper, desenlace de gasto | descartado para adquisición reproducible |

Una landing page no se contó como dato. Las dos barreras se registran por
objeto: CFPB MEM exige aceptación expresa de términos; w30508 no ofrece los
bytes del panel ni un repositorio público de replicación localizable.

## 4 · Bytes obtenidos e integridad

| id de manifiesto | archivo fuera de Git | bytes | SHA-256 |
|---|---|---:|---|
| `gen2_banxico_satisfaccion_usuarios_2019_2024_microdatos` | `GEN2_N34_PRODUCTO_DANO/banxico_satisfaccion_usuarios_2019_2024.xlsx` | 5,794,893 | `67d4a97b86e635252803a89848dc90b3815a32dd30266f7a7f8511a4f21207c6` |
| `gen2_banxico_satisfaccion_usuarios_2019_2024_manual` | `GEN2_N34_PRODUCTO_DANO/banxico_satisfaccion_usuarios_manual_2024.pdf` | 281,206 | `07926aca1a9fc7caadafcde7b4399fa1d91452355997ac58a7bb8d8ef1d36b5d` |
| `gen2_banxico_satisfaccion_usuarios_2024_informe` | `GEN2_N34_PRODUCTO_DANO/banxico_satisfaccion_usuarios_informe_2024.pdf` | 1,369,127 | `a2ef944695e9c9568fb9debaa32740e668da23f36ffb6b913c86d9641ca050db` |
| `gen2_federal_reserve_shed_2025_public_csv` | `GEN2_N34_PRODUCTO_DANO/shed_2025_public_csv.zip` | 4,676,794 | `a4ab3f7d042f16d63626b1af9aeb6f0b8a0b39e412fa94b87265bc67fe26de14` |
| `gen2_federal_reserve_shed_2025_codebook` | `GEN2_N34_PRODUCTO_DANO/shed_2025_codebook.pdf` | 849,070 | `3094d147be4fe60214b1c2550537d1b9d931559d3f804be7976b24e43e27311e` |
| `gen2_cfpb_bnpl_unsecured_debt_2025_report` | `GEN2_N34_PRODUCTO_DANO/cfpb_bnpl_unsecured_debt_2025.pdf` | 2,673,179 | `785d4f37e98eaacdf79d65de292112c6aa5cb7d827d94eb96fa40ea564e800d2` |

Los seis objetos pasaron `file`; los PDF declaran 16, 49, 119 y 35 páginas,
el XLSX es Excel 2007+ y el ZIP contiene únicamente `public2025.csv`
(47,807,284 bytes descomprimidos). Una segunda descarga independiente en
`/tmp/gen2-n34-verify.pKp24u` dio los mismos seis hashes. Banxico rotula manual
e informe como «Uso Público / Información de acceso público». SHED se publica
como public-use dataset por la Junta de Gobernadores con DOI
`10.17016/datasets.002`.

URLs primarias:

- Banxico, página de la encuesta:
  `https://www.banxico.org.mx/publicaciones-y-prensa/indicadores-de-satisfaccion-de-los-usuarios-de-ser/servicios-financieros-satis.html`;
- Federal Reserve, datos SHED:
  `https://www.federalreserve.gov/consumerscommunities/shed_data.htm`;
- CFPB, informe:
  `https://www.consumerfinance.gov/data-research/research-reports/consumer-use-of-buy-now-pay-later-and-other-unsecured-debt/`.

## 5 · Banco de México: estructura y cobertura

El informe 2024 documenta entrevistas en hogar, personas mexicanas de 18–70
años con al menos un producto y representatividad nacional para localidades de
50 mil habitantes o más. Las seis olas contienen 2,072, 2,075, 2,071, 2,060,
2,070 y 2,060 filas, respectivamente. El universo no es todo México rural ni
personas sin productos. Las categorías de producto no son excluyentes.

El lector stdlib verifica las 142 columnas y produce 30 filas
`ola×producto` en
`data/n34-producto-dano/banxico-cobertura-producto-ola.csv`. Para 2024, los
denominadores muestrales de tenedores y sus masas coinciden con el Cuadro 1
oficial:

| producto | n tenedores | masa ponderada | n costo y pago válidos | n costo+pago+problema válidos |
|---|---:|---:|---:|---:|
| tarjeta de crédito | 562 | 9,852,061.856285 | 548 | 548 |
| hipotecario | 428 | 5,496,821.773289 | 421 | 421 |
| personal | 421 | 2,390,314.081292 | 419 | 419 |
| nómina | 415 | 1,804,287.005152 | 407 | 407 |
| automotriz | 128 | 1,718,380.437775 | 128 | 128 |

El archivo conserva además, por ola y producto, n válido de costo, pago,
problema, reclamación y vulnerabilidad. En 2019, el comportamiento de pago no
está disponible para hipotecario, nómina o automotriz; se publica como n=0, no
como ausencia de atraso. La escala de interés es una calificación subjetiva
0–10; no se reetiqueta como tasa ni CAT.

Estimando **propuesto, no corrido**: para cada producto y ola, proporción
ponderada que reporta atraso o imposibilidad de pago entre tenedores con pago
válido, y tabla descriptiva conjunta por bandas predeclaradas de percepción de
interés, pago y problema. Una diferencia por costo sería asociación; sin
asignación exógena o estrategia de identificación no es efecto del interés.

## 6 · SHED 2025: BNPL en la misma persona

El codebook fija una encuesta web sobre KnowledgePanel probabilístico; el CSV
tiene 12,934 ids únicos, 815 columnas y ponderadores transversales. La lectura
reproducible está en `data/n34-producto-dano/shed-bnpl-cobertura.csv`:

| variable | concepto | n válido | sí | no |
|---|---|---:|---:|---:|
| `BNPL1` | usó BNPL en el último año | 12,934 | 2,004 | 10,930 |
| `BNPL3` | atraso en pago BNPL | 2,004 | 487 | 1,517 |
| `BNPL3A` | cargo extra por atraso | 487 | 302 | 185 |
| `BNPL1A` | sobregiro/NSF disparado por pago BNPL | 542 | 206 | 336 |
| `BNPL4_e` | BNPL era la única forma de poder comprar | 2,004 | 1,161 | 843 |

La tabla conserva también las masas con `weight`. `BNPL1A` se rotula como
subuniverso del cuestionario porque sólo 542 respuestas son observadas; este
acto no inventa su filtro a partir del patrón de faltantes.

Estimandos **propuestos, no corridos**: prevalencia ponderada de atraso entre
usuarios BNPL; cargo extra entre usuarios atrasados; sobregiro en el
subuniverso documentado; y asociación entre motivo de asequibilidad y cada
daño. Todos son estadounidenses y no causales.

## 7 · CFPB y evidencia causal preexistente

`data/n34-producto-dano/cfpb-bnpl-default-tabla3.csv` se extrae con
`pdftotext -layout` de Table 3, página impresa 14. Conserva seis categorías
FICO, su participación de originaciones, su default y el denominador 892,668.
Los defaults van de 0.7% a 4.1%; la fuente define default como falta de pago a
120 días y advierte que no contiene pagos tardíos. Son estadísticas agregadas
de 2021–2022, no microdato adquirido ni tasa mexicana.

Compartamos permanece como la única pieza causal acreditada mexicana del
conjunto: oferta aleatoria por 238 conglomerados; daño primario de mora
administrativa, ITT +1.1009 pp, IC95 [+0.6423, +1.5595], sobre 144 eventos.
Viajan sus reservas ya registradas: venta de activos con signo contrario,
atrición de 37.43%, una geografía/producto y ausencia de CAT y reporte al buró.
Este acto cita el resultado vigente; no lo reestima ni adopta.

## 8 · Niveles de uso y residual

| objeto | descriptivo | asociativo | causal acreditado | límite material |
|---|---|---|---|---|
| Banxico 2019–2024 | sí | posible en misma persona, no estimado aquí | no | categoría, no lender/CAT; población urbana 50 mil+ |
| SHED 2025 | sí | posible en misma persona, no estimado aquí | no | Estados Unidos; no transporte a México |
| CFPB Table 3 | sí | sí, agregado por FICO | no | sin microdato público; Estados Unidos |
| Compartamos AEJ | sí | sí | sí, RCT estrecho | no BNPL/CAT; Nogales; reservas de desenlace/atrición |
| ENSAFI de #723/#730 | sí | clase amplia | no | ya cubierto; no producto exacto |

Avance real: producto/costo subjetivo/daño ya son co-observables por cinco
categorías en México, y producto BNPL/daño son co-observables en una encuesta
pública extranjera. Residual exacto: obtener en México un producto BNPL o
crédito digital/lender identificable con CAT/tasa o fricción objetiva, daño y
negativos, y una estrategia que identifique efecto; alternativamente, un
experimento mexicano que mida las condiciones estructurales que Compartamos no
observa. No se cierra `NC-0164` ni se abre una necesidad duplicada.

## 9 · Reproducción y controles

```bash
python3 tools/extrae_n34_producto_dano.py
python3 tools/extrae_n34_producto_dano.py --verifica
python3 tests/test_n34_producto_dano.py
python3 tests/manifiesto.py --verifica \
  --id gen2_banxico_satisfaccion_usuarios_2019_2024_microdatos \
  --id gen2_banxico_satisfaccion_usuarios_2019_2024_manual \
  --id gen2_banxico_satisfaccion_usuarios_2024_informe \
  --id gen2_federal_reserve_shed_2025_public_csv \
  --id gen2_federal_reserve_shed_2025_codebook \
  --id gen2_cfpb_bnpl_unsecured_debt_2025_report
```

El extractor sólo requiere la biblioteca estándar y `pdftotext`, ya disponible
en CAJA. `--verifica` reconstruye cuatro tablas en memoria y exige identidad
byte a byte. Los tests unitarios ejercen la lectura de columnas XLSX, la
exclusión de no-aplica/no-respuesta, la tabla de candidatos y la transcripción
del denominador CFPB sin corpus ni red.

**Contador científico:** cero. **Parámetros/adopciones:** cero.

Antes del cierre se integró `origin/main=7a59c0eb84923e50dcb1a373a9c7d6fd34a34f04`,
que ya contiene #730/#731. La medición ENSAFI de #730 se conserva intacta:
este acto sólo añade evidencia distinta por identidad y mantiene su residual.
