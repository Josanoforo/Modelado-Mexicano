# ACTO GEN2-IMOR-CONTEXTO-TEMPORAL-POR-REGIMEN · cierre

Fecha: 11/sep/2026. Entorno: NUBE/WSL2, repo y datos agregados versionados;
cero descargas, microdatos o llamadas a modelos. Worktree:
`/home/pc0/mm-gen2-imor-contexto-temporal-por-regimen`; rama:
`acto/gen2-imor-contexto-temporal-por-regimen`. Partió de
`origin/main=a6d731db26a90b5b81eb6c5415c01e26c179aef9`, con árbol limpio, e
integró `origin/main=e37367581d5186ce4d4cf497377c83ebcd61cf93` antes del
cierre. PR revisable: #725; el merge pertenece a mesa.

## 1. Resultado útil

Se entrega el contexto temporal reproducible del IMOR mensual Banxico por
producto sin fabricar continuidad a través de IFRS9. La lectura sustantiva es:

- Personales tuvo el mayor nivel medio y la mayor dispersión temporal del
  nivel en ambos regímenes: 5.503% y 0.718 pp antes de IFRS9; 4.720% y
  0.412 pp desde IFRS9.
- Tarjetas fue segunda: media 5.139% y dispersión 0.697 pp antes de IFRS9;
  media 3.121% y dispersión 0.333 pp desde IFRS9.
- En el régimen 2022-01..2026-03, Tarjetas pasó de 2.51% a 3.35%
  (+0.84 pp; +33.47% relativo); ABCD pasó de 2.55% a 1.88% (−0.67 pp;
  −26.27% relativo). Son diferencias de extremos descriptivos, no efectos.
- En 2026-03 los niveles fueron: Consumo total 3.26%, Tarjetas 3.35%, ABCD
  1.88%, Nómina 2.77% y Personales 5.29%.

La lectura de dos páginas como máximo vive en
`data/analisis-imor-contexto-temporal/lectura-resultados.md`; la ficha de
consumo contextual está a su lado.

## 2. Definición, fuente y ruptura

Entrada versionada:
`data/fuentes-financieras-20/banxico-imor-consumo-mensual.csv`, SHA-256
`772f9d0b9da57b18ef9abdd5824b0824b6191e65668103e3a8329171d3df88e9`.
Contiene 615 llaves únicas, 123 meses continuos (2016-01..2026-03) y cinco
productos. Universo: banca comercial; incluye Sofomes ER subsidiarias de
instituciones bancarias y grupos financieros; excluye CI Banco. ABCD incluye
bienes muebles y automotriz.

Se consumieron el cierre y las notas de #723. Sólo acreditan una ruptura
metodológica dentro del corte:

| Régimen | Periodo | Numerador |
|---|---|---|
| `PRE_IFRS9_CARTERA_VENCIDA` | 2016-01..2021-12 | saldo de cartera vencida |
| `IFRS9_ETAPA_3` | 2022-01..2026-03 | saldo clasificado en etapa 3 |

No se encontró otra ruptura documentada en esos materiales. El salto
2021-12→2022-01 no se calcula ni se dibuja como movimiento homogéneo. La
publicación Banxico sigue rotulada como equivalente oficial, **no R16 CNBV**;
la foto R16 de diciembre de 2021 permanece separada.

## 3. Método y productos

La spec `CALC-IMOR-CONTEXTO-0001` se congeló en
`ae5153ab1e6bf8d6a8715f572d918f67734f9041` antes del primer run. Define
nivel mensual; cambios mensual e interanual sólo dentro de régimen; diferencias
en pp y porcentajes relativos en columnas distintas; media temporal uniforme,
mediana, extremos con fecha y desviación estándar poblacional (`ddof=0`) para
nivel y cambios.

Salidas propias:

| Archivo | Contenido |
|---|---|
| `niveles-mensuales.csv` | 615 niveles con unidad, universo, fuente y régimen |
| `cambios-mensuales-e-interanuales.csv` | 615 filas; 605 cambios mensuales y 495 interanuales calculables, pp y relativo separados |
| `resumen-producto-regimen.csv` | 10 filas, cinco productos×dos regímenes |
| `niveles-por-producto-y-regimen.svg` | niveles, paneles separados por régimen |
| `cambios-mensuales-por-producto-y-regimen.svg` | cambios mensuales en pp, paneles separados |
| `ficha-contextual.md` | unidad, universo, periodo, fuente y usos excluidos |
| `lectura-resultados.md` | síntesis sustantiva y dato faltante para calibración individual |

`materializa.py` fija `svg.hashsalt` y normaliza whitespace del SVG. Dos
materializaciones sucesivas produjeron hashes idénticos para las cinco salidas
generadas.

## 4. Corrida y validación

Corrida `CALC-IMOR-CONTEXTO-0001--ae5153ab1e6b`; `spec-check` 0/0 porque la
entrada es una tabla versionada sin reactivos; preflight VERDE; run exit 0;
`verify` **REPRODUCE · CONTEXTO=IDENTICO**, 11/11 RESULT. Sello completo:
`0c59cd4dc28edab30138ea0b599f1499da646730e6a76ae67b6cc5be3e5625df`.

El control independiente no importa el medidor: usa `csv` + `Decimal` y
reconstruye dimensiones, dos medias, un cambio mensual, un interanual, dos
extremos/fechas y los conteos calculables. Resultado:
`VALIDACION-INDEPENDIENTE-COINCIDE`. Las seis pruebas dirigidas cubren llaves,
continuidad, vacíos al inicio de régimen, referencias numéricas, unidades y
rótulos de los SVG.

La proyección de `tools/corrida0.py registro --lote
CALC-IMOR-CONTEXTO-0001` se verificó en modo seco y terminó sin error. No se
escribieron `data/corrida0/{corridas,resultados,usos}.tsv`: la proyección
canónica incorporaría también ofertas ya presentes de otros CALC, ajenas a
este encargo. El recibo pertinente y acotado de esta corrida queda en
`forense/replay-evidencia.tsv`; `usos.tsv` no cambia porque no hay adopción ni
consumidor activo.

## 5. Uso para R1.6 y límites

`python3 tools/ya_medido.py dinero.credito.scoring_alternativo` resolvió R1.6
y devolvió `NUNCA-MEDIDA`. Este acto no mide la probabilidad de R1.6. El uso
es `DESCRIPTIVO-NO-CALIBRA`: aporta contexto agregado de mora por producto,
sin sustituir una regla de scoring, convertir saldo en persona, medir CAT,
atribuir causalidad ni validar predicción.

Una calibración individual requiere datos enlazados a nivel crédito/persona:
originación, saldo/exposición, producto exacto, horizonte y definición de
default, cohorte, condiciones/CAT, covariables disponibles al decidir,
negativos y pérdidas, cobertura institucional, y evaluación temporal fuera de
muestra. Nada de eso se infiere de esta tabla agregada.

## 6. Obligaciones y residual

| Obligación | Evidencia | Estado | Siguiente acción |
|---|---|---|---|
| Analizar por régimen | tres tablas, dos SVG y `CALC-IMOR-CONTEXTO-0001` | CERRADA | mesa revisa PR #725 |
| Separar R16 | ficha, nota y figuras dicen “no R16 CNBV” | CERRADA | conservar la foto 2021-12 separada |
| Contexto R1.6 sin calibrar | ficha/lectura y RESULT de uso | CERRADA | cualquier calibración exige microdato longitudinal nuevo y decisión de mesa |
| `NC-0163` | #723 ya la cerró por alternativa oficial | PERMANECE CERRADA | ninguna por esta derivación |
| N34 / adopción R1.6 | fuera de autoridad | RESIDUAL SIN CAMBIO | acto científico específico, si mesa lo autoriza |
| Merge | PR #725 | PENDIENTE DE MESA | revisar y fusionar |

**Contador científico:** cero. El CALC usa el contrato canónico de identidad,
sello y replay, pero queda `NO-DERIVACION-CONTEXTUAL`: deriva una serie ya
publicada y no se presenta como medición independiente nueva.
