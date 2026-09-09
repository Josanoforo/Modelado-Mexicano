# ¿Sobrevive "los pobres no pagan" a los datos auditados del crédito popular mexicano?

> **Nota de procedencia (19/ago/2026 · `FP-61`):** deep research corrido **fuera del proyecto** (herramienta externa; no sigue la disciplina Bloque A/B/C del programa), encargado por dirección bajo el prompt `PROMPT-DEEPSEARCH-CREDITO-POPULAR` como el gate de mesa que `FP-61` exigió el 19/ago/2026 para adjudicar `ref.A.04` (`milpa/refutations.yaml`) contra la frontera declarada de `ADR-35`. Evidencia de **clase mixta**: cada cifra trae su propia etiqueta `AUDITADA`/`AUTO-REPORTADA` tal como el informe la trae, en la tabla de §A y en el Anexo de fuentes (§C) — no se re-etiqueta ni se redondea en este acto. Archivado **verbatim**, sin edición de cuerpo, el 19/ago/2026 (`ACTO FP61-ADJUDICA`); a partir de este commit es base de evidencia fechada del corpus y no se retoca (doctrina `FP-57`/`ADR-114`). Archivo de origen (fuera del repo, no se re-sube con ese nombre): `compass_artifact_wf-e29a28d4-...-_text_markdown.md` {cita-ilustrativa}.

## TL;DR
- **No sobrevive como se enuncia, pero tampoco se rompe limpiamente: de 11 casos independientes analizados, la creencia se ROMPE o MATIZA en la mayoría, y en NINGUNO se CONFIRMA la versión conductual pura ("el segmento popular no paga").** Lo que los datos auditados (CNBV, BMV, SEC, reportes dictaminados) sostienen es más preciso: el segmento popular paga a tasas altas *cuando existe un mecanismo* —descuento en nómina, prenda en mano, cobranza semanal domiciliaria o presión grupal— y el modelo se hace rentable *precargando en el precio (CAT 63%–839%) una pérdida esperada de 6%–20%*.
- **Las tres quiebras "de contraste" (Famsa 2020, Crédito Real 2022, AlphaCredit 2021) NO cayeron por mora del pobre.** Las tres se adjudican a causas estructurales: partes relacionadas y falseo de capital (Famsa), interés capitalizado/portafolio inflado y muro de refinanciamiento en francos suizos (Crédito Real), y error/fraude contable en derivados (AlphaCredit). La variable conductual del deudor popular es marginal o CONFUNDIDA en todas.
- **Advertencia metodológica central:** el IMOR de las financieras populares está deprimido artificialmente por castigos rápidos. Medido con castigos (IMOR ajustado / cartera vencida ajustada), Banco Azteca ronda 10.7%, BanCoppel 15.7%, Financiera Independencia ~20% y CAME 34% — muy por encima del 2%–8% que sugiere el IMOR simple. La pregunta correcta nunca es "¿hay mora?", sino "¿paga peor que un segmento comparable, controlando producto y precio?".

## Key Findings

1. **El mito, en su forma fuerte, es falso.** Ninguna institución con datos auditados demuestra que el segmento popular *no pague*. Compartamos (microcrédito grupal sin garantía) opera con IMOR etapa-3 de 3.83%–3.88% y castigos anuales que en 2025 llegaron a Ps. 2,406 millones en un solo trimestre — cartera que sí se recupera mayoritariamente, pero a costa de reservar y castigar agresivamente.

2. **El mecanismo es el que paga, no la "confianza".** El caso que más desnuda el mito es el crédito de nómina: Crédito Real reportaba mora de su cartera de nómina en torno a 1.2%–1.5% precisamente porque el descuento ocurre *antes* de que el trabajador cobre. Eso no prueba que "el pobre pague"; prueba que cuando el cobro es involuntario, la conducta del deudor es irrelevante.

3. **Las casas de empeño no prueban nada sobre pago voluntario.** Nacional Monte de Piedad reporta ~90% de redención de prendas ("nueve de cada 10 clientes recuperan sus prendas", Expansión, 2019); FirstCash reporta inventario mayor a un año en apenas 1%–2% (reportes SEC). Pero la garantía prendaria *sustituye* a la confianza: si el cliente no paga, la casa vende la prenda y recupera capital + interés. La alta redención prueba que el cliente *valora su prenda*, no que "pague" en el sentido conductual.

4. **El pricing es una confesión.** Los CAT del sector precargan la pérdida: Compartamos ~100%+ (pérdida esperada Banxico 6.5%), Banco Azteca Credimax CAT 93.5% sin IVA, Provident CAT 343.7%–839.6%, FirstCash empeño ~69% CAT / 23% mensual. Un modelo con CAT de dos o tres dígitos que absorbe 10%–20% de castigos es un modelo que *tolera* que una fracción no pague — es rentabilidad, no virtud del deudor.

5. **Las quiebras confirman que el riesgo mortal del sector es estructural, no conductual.** Famsa, Crédito Real y AlphaCredit murieron por tesorería, gobierno corporativo, partes relacionadas y contabilidad — no por una ola de impago del segmento popular.

## A. Tabla por caso

| # | Institución | Segmento | Mecanismo de pago | Métrica clave (cifra · año · definición) | Fuente | Tesis | Veredicto | Confusores |
|---|---|---|---|---|---|---|---|---|
| 1 | **Banco Azteca / Elektra** | Consumo en tienda, personal popular (C/D) | Cobranza semanal, tarjeta Azteca, prenda parcial, buró | IMOR simple 5.35% (jun 2025); **IMOR ajustado ~10.7%** (2025); castigos 12m Ps. 17,390 M (mar 2024) | `AUDITADA` (CNBV vía HR Ratings / Whitepaper Intel) | DECLARADA (Valenzuela: "nació como institución popular", inclusión "como modelo de negocio") | **MATIZA** | Prenda parcial, venta cruzada |
| 2 | **BanCoppel / Coppel** | Consumo en tienda + banco popular | Cobranza en tienda, historial interno | IMOR 8.4% (3T24)→5.5% (3T25); castigos 12m Ps. 5,255 M (sep 2024); **IMOR ajustado 15.7%** (3T24) | `AUDITADA` (HR Ratings/CNBV; EEFF 2020–24 auditados KPMG sin salvedades) | INFERIDA/RETROSPECTIVA | **MATIZA** | Cartera empresarial/vivienda de menor mora diluye el indicador |
| 3a | **Nacional Monte de Piedad** | Empeño prendario | Garantía prendaria en mano | **~90% de redención** (2019); hasta 3 refrendos (~20 meses) | `AUTO-REPORTADA` (Expansión/institución) | INFERIDA | **ROMPE el marco** (colateral hace irrelevante el pago) | Redención ≠ pago conductual |
| 3b | **FirstCash** (cadena privada) | Empeño prendario, 30 días renovables, presta 30–70% valor | Garantía prendaria en mano; sin buró | Inventario >1 año 1%–2% (2024–25); rotación 2.8x LatAm; CAT ~69% / 23% mensual | `AUDITADA` (SEC 10-K / reportes) | INFERIDA | **ROMPE el marco** | Reporta forfeiture/inventario, no "tasa de redención" directa |
| 4 | **Compartamos (Gentera)** | Microcrédito grupal e individual | Presión grupal (garantía solidaria) + cobranza semanal | IMOR etapa-3 3.88% (4T24), 3.83% (4T25); castigos Ps. 542M (4T22)→1,130M (4T24)→2,406M (4T25); cobertura 207%; **pérdida esperada 6.5%** | `AUDITADA` (BMV/CNBV; Banxico RIB) | DECLARADA (fundada 1990 sobre premisa de microempresaria pobre como sujeto rentable; RCT de IPA 2009) | **MATIZA→CONFIRMA (versión débil)** | Venta de cartera castigada; migración a individual |
| 5 | **Financiera Independencia / Provident** | Crédito personal popular no bancario | Cobranza semanal/domiciliaria; sin garantía | Findep IMOR 6.1–6.3% (4T23–24); **IMOR ajustado ~20%** (4T24). Provident CAT 343.7%–839.6% | `AUDITADA` (Findep, HR/BMV) / `AUTO-REPORTADA` (CAT Provident) | DECLARADA parcial (Findep desde 1993 "privilegiar calidad y rentabilidad sobre tamaño") | **MATIZA** | Exposición EE.UU. (AFI); colocación conservadora reciente |
| 6 | **Banco Famsa** (quiebra 2020) | Banco popular + venta en tienda | — | Revocación 1-jul-2020; pasivos con partes relacionadas Ps. 8,589 M; ICAP bajo mínimo | `AUDITADA` (DOF/SHCP/CNBV; IPAB) | — | **ROMPE / CONFUNDIDO** (quebró por autopréstamo, no por impago del cliente) | 580,774 ahorradores cubiertos por IPAB |
| 7a | **Crédito Real** (default 2022) | Nómina (62.8%→69.2% cartera), pymes, autos | Descuento vía nómina en la fuente | Nómina reportada 1.2–1.5%; **~47% del portafolio = interés capitalizado**; revisión cartera mala +82% (abr 2021); default bono CHF 170 M → ~US$1.9 mil M | `AUDITADA` (Factsheets/BMV) + análisis forense (FGB/Bloomberg) | DECLARADA (inclusión de segmentos "desatendidos por la banca") | **ROMPE / CONFUNDIDO** | Sin EEFF auditados post-2020; descalce FX/duración |
| 7b | **AlphaCredit** (default 2021) | Consumo (nómina) + pymes, MX/Colombia | Descuento nómina | Reexpresión derivados 2018–19; deterioro ~Ps. 4,100 M (US$206 M) en otros activos/cuentas por cobrar | `AUDITADA` (comunicados BMV; Ch.11 Delaware) | INFERIDA | **ROMPE / CONFUNDIDO** | Detonante contable (derivados), no impago de cartera |
| 8a | **Tandas / cundinas (ROSCAs)** | Ahorro-crédito rotativo informal | Presión social (confianza/honor-vergüenza), sin garantía ni ley | ~30–31% de la población participa; tasa de default cuantitativa **NO ENCONTRADA** | `AUTO-REPORTADA` / cualitativa (SciELO, Sociológica UAM, Forbes) | INFERIDA | **MATIZA** (evidencia no auditada) | Sin microdato de incumplimiento |
| 8b | **CAME** (SOFIPO mediana, liquidada 2025) | Microcrédito popular | Cobranza; app digital | Castigos 2023 Ps. 1,138.4 M; **cartera vencida ajustada 34.0%** (2023) vs 24.8% (2022); pérdida Ps. 532 M | `AUDITADA` (PCR Verum/CNBV) | INFERIDA | **MATIZA / CONFUNDIDO** | Integración fallida + contabilidad "sospechosa" (venta de cartera oculta visibilidad) |
| — | **Comparación: banca múltiple** | Consumo/tarjeta clase media | Domiciliación, buró | Consumo IMOR ajustado 10.5% (dic 2023); **tarjeta IMOR ajustado 13.7%** (jun 2025); total 4.1% | `AUDITADA` (CNBV/HR Ratings) | — | Referencia de control | — |

## B. Síntesis

Once casos independientes, con calidad de dato muy dispar, apuntan en una sola dirección: **la creencia "los pobres no pagan" no sobrevive al contacto con los datos auditados de todo el sector.** No hay un solo caso que la CONFIRME en su forma fuerte (conductual). Lo que sí sostienen los datos —con fuente CNBV/BMV/SEC dictaminada en la mayoría— es que el segmento popular paga *a través de un mecanismo* que sustituye a la confianza, y que el modelo es rentable *aunque* una fracción no pague, porque el precio la precarga.

Los mecanismos revelan la creencia que opera de verdad. Donde el cobro es **involuntario en la fuente** (nómina: Crédito Real, AlphaCredit) o hay **colateral líquido** (empeño: Monte de Piedad ~90% redención, FirstCash 1–2% de inventario añejo), la conducta del deudor es *irrelevante*: la mora reportada es mínima porque la garantía o el descuento hacen el trabajo. Estos casos ROMPEN el marco de la pregunta más que confirmarla. Donde hay **presión social/grupal sin garantía física** (Compartamos, tandas), aparece la única evidencia de pago genuinamente voluntario —y aun ahí Compartamos castiga miles de millones al trimestre y cobra CAT de tres dígitos, señal de que también precarga incumplimiento.

El pricing es la confesión más honesta del sector: CAT de 63% (FirstCash) a 839% (Provident), con pérdidas esperadas de 6.5% (Compartamos) o cartera vencida ajustada de 15%–34% (BanCoppel, Findep, CAME). Un negocio que cobra tres dígitos y castiga dos dígitos no está diciendo "mi cliente paga"; está diciendo "mi cliente paga lo suficiente y yo cobro para cubrir a los que no". Y la prueba de control es demoledora: la **tarjeta de crédito de la banca múltiple —clase media— tiene IMOR ajustado de 13.7% (jun 2025)**, comparable o peor que Banco Azteca (10.7%) y no muy lejos de BanCoppel (15.7%). Controlando producto, el pobre no paga dramáticamente peor; la diferencia real está en el *precio*, no en el comportamiento.

Las tres quiebras obligatorias sellan el argumento por la vía negativa: ninguna murió por impago del segmento popular. Famsa cayó por créditos a partes relacionadas registrados como cuentas por cobrar para evadir reservas; Crédito Real por ~47% de portafolio en interés capitalizado y un muro de deuda en francos suizos; AlphaCredit por un agujero contable en derivados. Son riesgos del *emisor*, no del *acreditado*.

**La frase honesta final:** los datos SÍ sostienen que *"el segmento popular paga a tasas comparables o solo modestamente peores que el consumo bancario tradicional, siempre que exista un mecanismo —descuento en fuente, prenda, cobranza semanal o presión grupal— y a un costo (CAT de dos o tres dígitos) que precarga una pérdida esperada de 6%–20%."* Los datos NO sostienen ni que "los pobres no pagan" (falso: los modelos son rentables y persisten décadas), ni la versión romántica opuesta de que "pagan por virtud" sin necesidad de garantía o coerción de cobro (también falso: retirado el mecanismo, no hay dato que pruebe pago voluntario masivo).

## Recommendations

1. **Reformular la tesis antes de usarla.** Sustituir "los pobres no pagan" por la afirmación falsable que los datos sostienen (recuadro anterior). La original es indefendible con dato auditado; la reformulada es defendible.

2. **Nunca citar un IMOR simple del sector popular sin su castigo.** Regla operativa: exigir IMOR + castigos 12m (o IMOR ajustado / cartera vencida ajustada / pérdida esperada). **Umbral de alarma: si IMOR ajustado > 2.5× el IMOR simple, la institución sanea por castigo y el IMOR simple es cosmético** (Azteca, BanCoppel, Findep y CAME cumplen este patrón).

3. **Separar siempre garantía de conducta.** Para cualquier afirmación sobre "pago", clasificar el mecanismo: (a) cobro involuntario en fuente (nómina) → conducta irrelevante; (b) colateral líquido (empeño) → conducta irrelevante; (c) presión social/grupal sin garantía (Compartamos, tandas) → única evidencia de pago voluntario, y aun así con castigo precargado. No mezclar los tres bajo la palabra "pagan".

4. **Para due diligence de emisoras del sector:** las señales que precedieron a las tres quiebras NO fueron mora del cliente, sino partes relacionadas (Famsa, Crédito Real), interés capitalizado / portafolio sin efectivo (Crédito Real ~47%), reexpresiones contables (AlphaCredit), ausencia de estados auditados recientes y descalce FX/duración. Vigilar esos indicadores, no el IMOR del acreditado.

5. **Qué cambiaría el veredicto (benchmarks):** (a) un microdato auditado de cumplimiento de tandas que muestre default voluntario <5% sin garantía movería el caso hacia CONFIRMA (versión débil); (b) un estudio que aislara la mora conductual pura de la cartera popular —controlando cobro en fuente y colateral— por *encima* de la de tarjetas de clase media movería hacia CONFIRMA (versión fuerte). Ninguno existe hoy en fuente auditada, así que el veredicto agregado se mantiene en **ROMPE/MATIZA**.

## C. Anexo de fuentes

**Banco Azteca / Elektra**
- IMOR ajustado ~10.7% y castigos 12m Ps. 17,390 M (mar 2024): HR Ratings, "Banco Azteca — Reporte 2024" (5-jul-2024), hrratings.com/pdf/BancoAzteca_Reporte_2024.pdf; y La Política Online (datos Whitepaper Intel/CNBV), lapoliticaonline.com. `AUDITADA` (base CNBV).
- IMOR simple 5.35% (jun 2025): EL CEO, elceo.com/negocios/mexicanos-deben-193161-mdp... `AUDITADA` (CNBV).
- CAT Credimax 93.5% sin IVA / tasa 49.70% (2024): El Imparcial, elimparcial.com/dinero/2024/07/16/...; Elektra "Términos de promociones" (CAT Credimax 63.5%, tasa 40.53%, 2026), elektra.mx/terminos-de-promociones. `AUTO-REPORTADA`.
- Tesis Valenzuela ("nació como institución popular"): Wikipedia/Banco Azteca citando declaraciones del CEO. `AUTO-REPORTADA`.

**BanCoppel / Coppel**
- IMOR 8.4% (3T24), castigos 12m Ps. 5,255 M, IMOR ajustado 15.7%: HR Ratings, "BanCoppel — Reporte Revisión 2024" (16-dic-2024), hrratings.com/pdf/Bancoppel_ReporteRevisiAn_2024.pdf. `AUDITADA`.
- IMOR 5.5% (3T25): HR Ratings, "BanCoppel 2025" (15-dic-2025), hrratings.com/pdf/Bancoppel_ReporteRevisiAn_2025.pdf. `AUDITADA`.
- EEFF 2020–2024 auditados sin salvedades por KPMG: PCR Verum, "Reporte de Calificación BanCoppel" (7-ene-2026), pcrverum.mx. `AUDITADA`.
- Pérdida esperada BanCoppel 6.2%: Banxico, "Indicadores Básicos de Créditos Personales y Microcréditos, datos a feb 2024", banxico.org.mx. `AUDITADA`.

**Casas de empeño**
- NMP redención ~90% ("nueve de cada 10 recuperan sus prendas"), hasta 3 refrendos: Expansión, "Así se vive el negocio prendario de Nacional Monte de Piedad" (18-jul-2019), expansion.mx/finanzas-personales/2019/07/18/... `AUTO-REPORTADA`.
- FirstCash inventario >1 año 1%–2%, rotación 2.8x (LatAm) / 4.2–4.4x, márgenes 34–43%: FirstCash Holdings, comunicados de resultados 4T24 y 1T–2T25, ir.firstcash.com. `AUDITADA` (SEC).
- FirstCash CAT ~69% / ~23% mensual, presta 30–70% valor: sitios FirstCash México (firstcashtienda.com/faq). `AUTO-REPORTADA`.
- Marco legal empeño (NOM-179-SCFI-2016): firstcash.mx/empenos.

**Compartamos (Gentera)**
- IMOR etapa-3 3.88% (4T24), castigos Ps. 1,130 M (4T24), cobertura 207%: Banco Compartamos "Resumen 2024 y 4T24", compartamos.com.mx (Banco-PR-4T24.pdf). `AUDITADA` (BMV/CNBV).
- IMOR 3.83% y castigos Ps. 2,406 M (4T25): Gentera "Comentarios y Análisis 4T25", gentera.com.mx. `AUDITADA`.
- Castigos Ps. 542 M (4T22), política de castigo a 180 días: Banco Compartamos "Resumen 2022 y 4T22", compartamos.com.mx. `AUDITADA`.
- Castigos Ps. 928 M a sep-2024, crédito individual 34.7%: Moody's Local, "Banco Compartamos" (12-feb-2025), moodyslocal.com.mx. `AUDITADA` (base CNBV).
- Pérdida esperada 6.5% (segunda más alta tras Fin Útil 7.7%); tasa a microcrédito: Banxico, "Indicadores Básicos de Créditos Personales y Microcréditos, feb 2024", banxico.org.mx. `AUDITADA`.
- Tasa Crédito Mujer ~110% (2009), 16 pagos semanales, RCT: Innovations for Poverty Action, "Microcrédito para Mujeres en México", poverty-action.org. `AUDITADA` (estudio académico).
- Tasa comerciante ~100% anual, sin comisiones por atraso: compartamos.com.mx (costos y comisiones crédito grupal). `AUTO-REPORTADA`.

**Financiera Independencia / Provident**
- Cartera informal 23.4% (dic 2023), montos Ps. 500–300,000, pagos semanales/quincenales: Financiera Independencia, Reporte Anual 2023, findep.mx/documentos/anuales/2023ia.pdf. `AUDITADA`.
- IMOR 6.1–6.3% (4T23–4T24), IMOR ajustado ~20% (4T24): HR Ratings, "Financiera Independencia" (2024), hrratings.com/pdf/FINDEP_Reporte_2024.pdf. `AUDITADA`.
- Provident CAT 343.7% (51 sem), 455.0% (41 sem), 713.3% (31 sem); modelo domiciliario semanal: Provident México, providentest.wordpress.com y provident.com.mx. `AUTO-REPORTADA`.

**Banco Famsa (quiebra 2020)**
- Causas de revocación (partes relacionadas, registros indebidos, incumplimiento desde 2016): EL CEO, "Banco Ahorro Famsa quiebra por malas prácticas", elceo.com; El Financiero, "Liquidarán Banco Famsa y toma el control el IPAB", elfinanciero.com.mx. `AUDITADA` (SHCP/CNBV/DOF).
- 580,774 ahorradores cubiertos por IPAB: comunicado SHCP/CNBV, jul-2020 (El Financiero). `AUDITADA`.
- Pasivos con partes relacionadas Ps. 8,589 M; modus operandi Promobien/BAF: Excélsior, "Grupo Famsa, la crónica de una estafa anunciada", excelsior.com.mx; La Silla Rota, lasillarota.com. `AUTO-REPORTADA` (prensa sobre cifras de concurso).

**Crédito Real (default 2022)**
- Nómina 62.8%→69.2% de cartera (2016–18), NPL nómina 1.2–1.5%: Crédito Real Factsheets 3T16–3T18, creal.mx. `AUDITADA` (reportes trimestrales).
- ~47% del portafolio = interés capitalizado; revisión cartera mala +82% (abr 2021): FGB Law, "Case Highlights Reach of Transnational Insolvency", fgb.law; Bloomberg Línea, "Foreign Bondholders Lose $5 Billion..." (6-oct-2022), bloomberglinea.com. Análisis forense / prensa financiera (no hallado el documento del síndico subyacente).
- Default bono CHF 170 M; cross-default ~US$1.9 mil M; recuperación bancos locales US$615 M "con descuento significativo" primero, bonistas extranjeros ~23 centavos: La Jornada (10-feb-2022), jornada.com.mx; El Financiero/Bloomberg (20-jun-2023), elfinanciero.com.mx. `AUDITADA` (comunicado BMV) + prensa.
- Liquidación judicial jul-2022, concurso mercantil nov-2023, Ch.15 Delaware: Axis Negocios, axisnegocios.com; comunicado gob.mx No. 29.
- *Nota:* la mora de nómina 1.2–1.5% proviene de Factsheets de la propia emisora; no confirmada por auditor independiente post-2020 (la empresa no presentó EEFF auditados tras 2020).

**AlphaCredit (default 2021)**
- Reexpresión derivados 2018–19; deterioro ~Ps. 4,100 M (US$206 M): Forbes México, "AlphaCredit admite fallas en contabilidad", forbes.com.mx; Axis Negocios, axisnegocios.com; Bloomberg Línea, bloomberglinea.com. `AUDITADA` (comunicados BMV/Ch.11).

**Tandas / cundinas (ROSCAs)**
- ~30–31% de participación; mecanismo de confianza/honor: "Las tandas en México: un enfoque de acción colectiva", Sociológica México (UAM), sociologicamexico.azc.uam.mx; Wikipedia "Tanda (informal loan club)". `AUTO-REPORTADA`/académica cualitativa.
- Tasa de default cuantitativa auditada: **NO ENCONTRADO** en SciELO (scielo.org.mx), Sociológica México (UAM), Forbes México ni referencias a Banco Mundial consultadas.

**CAME (SOFIPO, liquidada 2025)**
- Castigos 2023 Ps. 1,138.4 M; cartera vencida ajustada 34.0% (2023) vs 24.8% (2022); pérdida Ps. 532 M: PCR Verum, "PCR Verum baja a 'B+/M' la calificación de CAME" (17-abr-2024), pcrverum.mx. `AUDITADA`.
- Revocación y liquidación (sep-2025): CAME, came.org.mx; La Política Online, lapoliticaonline.com. `AUDITADA` (DOF/CNBV).

**Comparación banca múltiple (control)**
- Banca total IMOR 2.1% / IMOR ajustado 4.1%; consumo 3.4% / 10.5% (dic 2023): HR Ratings, "Banca Múltiple en México — Análisis Sectorial" (16-abr-2024), hrratings.com/pdf/SectorialBancos_2024.pdf (base CNBV). `AUDITADA`.
- Tarjeta de crédito IMOR ajustado 13.7% (jun 2025): CNBV vía Yahoo Finanzas, es-us.finanzas.yahoo.com. `AUDITADA` (CNBV).
- Fuente primaria de indicadores: CNBV, Portafolio de Información — Banca Múltiple, portafolioinfo.cnbv.gob.mx; Información Estadística, cnbv.gob.mx.

---
*Notas de calidad de dato:* las cifras de IMOR simple del sector popular están sistemáticamente deprimidas por castigo rápido; se privilegió el IMOR ajustado / castigos donde existió. Casos marcados **CONFUNDIDO** (Famsa, Crédito Real, AlphaCredit, CAME) no permiten aislar la variable conductual y no se usan como evidencia del mito en ninguna dirección. Las comparaciones cruzan 2023–2025 por disponibilidad; cada cifra lleva su año. El monto exacto del default de Crédito Real varía por fuente y alcance (US$1.9 mil M en bonos dólar vs >US$2.5 mil M de deuda total) y por tipo de cambio.
