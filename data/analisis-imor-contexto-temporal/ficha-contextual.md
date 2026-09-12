# Ficha contextual · IMOR de consumo por producto

| Campo | Definición |
|---|---|
| Indicador | IMOR mensual: porcentaje de saldos de cartera en el numerador de mora respecto de la cartera total del mismo producto. |
| Unidad | Porcentaje de saldos; no porcentaje de personas, probabilidad individual ni error estándar de encuesta. |
| Agregado institucional | Banca comercial; incluye Sofomes ER subsidiarias de instituciones bancarias y grupos financieros; excluye CI Banco. |
| Productos | Consumo total publicado, tarjetas de crédito, ABCD, nómina y personales. ABCD incluye adquisición de bienes de consumo duradero, incluidos bienes muebles y automotriz. |
| Periodo | 2016-01..2026-03, 123 meses continuos. |
| Regímenes comparables | `PRE_IFRS9_CARTERA_VENCIDA` (2016-01..2021-12) e `IFRS9_ETAPA_3` (2022-01..2026-03). No se calcula el salto entre ambos. |
| Fuente | Banco de México, *Índices de morosidad del crédito al sector privado no financiero*, Informe trimestral enero-marzo 2026; identidad manifestada `gen2_banxico_imor_consumo_producto_mensual_2026t1_html`. |
| Artefacto analizado | `data/fuentes-financieras-20/banxico-imor-consumo-mensual.csv`, SHA-256 `772f9d0b9da57b18ef9abdd5824b0824b6191e65668103e3a8329171d3df88e9`. |
| Relación con CNBV | Publicación oficial equivalente para la historia mensual; **no** es R16 CNBV. La foto R16 de 2021-12 permanece separada. |
| Uso permitido | Contexto temporal descriptivo para `dinero.credito.scoring_alternativo` (`R1.6`), comparando sólo dentro de régimen. |
| Usos excluidos | Calibración individual, consumidor Bernoulli de persona, sustitución de una regla de scoring, causalidad, validación predictiva o adopción automática de parámetros. |

La media temporal pondera meses uniformemente. No equivale al cociente de
saldos acumulados porque no se dispone de los denominadores monetarios por
mes. La dispersión reportada es desviación estándar poblacional entre meses
observados (`ddof=0`), no incertidumbre de muestreo.
