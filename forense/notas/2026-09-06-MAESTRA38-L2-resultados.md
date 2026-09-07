# ACTO MAESTRA38-L2 · MPS-2012 — resultados (rama TEXTO)

Rama elegida: **TEXTO** (ver `forense/notas/2026-09-06-MAESTRA38-L2-spec-rama.md`:
`find` sobre las tres raíces declaradas, 2051 archivos examinados, `35024-0001-Data.dta`
NO-ENCONTRADO). El `.dta` restringido sigue sin descargarse (FP-314/FP-316).

## P0 · universo

- `data/l2-mps2012-cuestionario-v1_0.txt` — texto completo del cuestionario en
  español (`35024-Questionnaire-spanish.pdf`, raíz `descargas_mx`,
  `ICPSR_35024/35024-Questionnaire-spanish.pdf`, `pdftotext`, 3908 líneas).
- `data/l2-mps2012-items-v1_0.tsv` — 11 filas: wording verbatim de las
  variables citadas por FP-263, T9b y la serie de ronda 1, con línea de origen
  en el cuestionario.
- Insumos ya en manifiesto verificados presentes en `descargas_mx`:
  `ICPSR35024-ds1-w2-tabulados-T5-T9-derivados-2026-09-02.csv` (647 filas,
  once tablas T5-T13 pese al nombre), su LEEME de procedencia (9 adendas de
  re-sello por crecimiento de universo, todas SIN-FETCH clase (3)), LEEME
  general, `35024-Questionnaire-spanish.pdf`, paquete v1 (14.6 MB, 0 datos),
  codebook, DATS json, parcial `.tab`.

## P1 · FP-263 se adjudica

`FP-263` (`forense/firmas-pendientes.tsv:255`) pedía tres cosas para cerrar
MPS-2012 sin el `.dta`:

1. **T9b** (`W2_P38A x W2_P38B`, control `P46`, 45 celdas) — **PRESENTE**. Está
   en el CSV desde la Adenda 4 del LEEME (`N=876`, 5 paneles de `P46`:
   6/95/367/182/226). Medido con `csv.DictReader` en la Adenda misma del
   depósito de mesa, no supuesto por este acto.
2. **Serie de ronda 1 completa** (`P40 x P7`, `P40 x P8`, `P38B_oportunidades x
   P8` con control `P36C`, `P39 x P8`) — **PRESENTE**, las cuatro: T10
   (`P40xP7`, N=1284), T11 (`P40xP8`, N=1268), T12
   (`P38B_oportunidades x P8`, control `P36C`, N=1268), T13 (`P39xP8`, N=696,
   universo = inscritos en programa, no poblacional — ver Adenda 8-C del
   LEEME). Añadidas por las Adendas 5-8 del mismo LEEME.
3. **El texto de los ítems de P35A/P35B/W2_P35A/W2_P35B** — **OBTENIDO EN ESTE
   ACTO**. `ADR-350` (`L2-LISTA`) ya había verificado el wording por una vía
   distinta (el paquete R `list::mexico`, en inglés). Este acto lee el
   cuestionario ORIGINAL en español y confirma, verbatim, líneas 1192-1230
   (ronda 1) y 3057-3124 (ronda 2): Lista B = Lista A + un ítem, y ese ítem es
   "c. Recibir un regalo, favor o acceso a un servicio a cambio de su voto" —
   venta del voto — en las dos olas, wording idéntico entre ronda 1 y ronda 2.

Con las tres condiciones satisfechas, **`FP-263` → EJECUTADA** (ver
`forense/firmas-pendientes.tsv`, columna de estado). Lo que NO cambia: el
instrumento sigue siendo de segunda mano para T5-T13 (tabulador en línea, SIN
PONDERAR), el `.dta` de ICPSR 35024 sigue sin obtenerse, y ninguna cifra de
este paquete entra al canon como verificada hasta que un acto con acceso al
microdato reproduzca las celdas (así lo declara el propio LEEME, clase de
procedencia (3), marca SIN-FETCH). Cerrar FP-263 es cerrar la PREGUNTA DE
INSUMO ("¿hay suficiente para adjudicar P2/P3 sin el .dta?"), no sellar los
resultados de segunda mano.

## P2 · R7.3 / R7.6 con el texto

`ya_medido.py` (A.8, salida completa en el commit): `R7.3` →
`civico.voto.agencia_con_secreto` (`ADR-329`: MEDIA, `se_mueve_si` = medición
de primera mano en el `.dta`; L9/L11 `CONTRARIA-REPLICADA`; L12 P2
`REPLICA-DE-SEGUNDA-MANO-NO-SELLADA`). `R7.6` →
`civico.voto.clientelar_si_observable` (`ADR-349`, LOTE-LAPOP: tercera
`CONTRARIA` en el otro brazo — no se reabre, se compara).

Con el texto de los ítems ya leído, la tabla relevante para R7.3
(clientelismo condicionado al secreto del voto) sigue siendo **T12**
(`P38B_oportunidades x P8`, control `P36C` = creencia en secreto del voto).
El hallazgo (LEEME Adenda 7-D) va en la dirección CONTRARIA al mecanismo de
sanción creíble: la ventaja priista del beneficiario de Oportunidades
aparece SOLO donde el votante SÍ cree que su voto es secreto, y se invierte
al perderse esa creencia — lo opuesto de lo que predice un mecanismo de
sanción por vigilancia.

**Veredicto de este acto: `NO-SELLADA` para R7.3 y R7.6 bajo este
instrumento.** El texto de los ítems (P1) resuelve la procedencia de las
preguntas pero no resuelve lo que ya impedía sellar antes: conteos SIN
PONDERAR, sin diseño muestral, sin acceso al `.dta`, celdas pequeñas en varios
paneles (n=20, n=13, n=30 en distintos cortes de T12). No se re-declara
CONTRARIA ni RECHAZADA: se mantiene la lectura de `ADR-329`/L12
(`REPLICA-DE-SEGUNDA-MANO-NO-SELLADA`), ahora con el ítem confirmado en
español y no solo en inglés. `R7.6` no se reabre (`ADR-349` sigue firme); esta
nota solo compara: la dirección de T12 (sanción por secreto invertida, no
confirmada) es consistente con — no idéntica a — la tercera `CONTRARIA` del
otro brazo.

## P3 · lista: ¿el ítem sensible es venta de voto?

**`CORROBORADA-EN-TEXTO`.** Confirmado arriba (P1, punto 3): el cuestionario
en español de ICPSR 35024 dice, verbatim, que el ítem añadido en la Lista B es
"recibir un regalo, favor o acceso a un servicio a cambio de su voto", en las
dos olas. Esto es más fuerte que la vía de `ADR-350` (inglés de
`list::mexico`, un paquete R distinto con su propio subconjunto de
encuestados) porque lee el idioma y el instrumento original directamente. No
se declara `VENCIDA EN ALCANCE`: el texto en español confirma exactamente lo
que el texto en inglés ya decía, sin contradicción y sin ítems adicionales
sorpresa. Sucesor declarado en `ADR-350` (L2-bis rama MEDICIÓN cuando el
`.dta` llegue) no cambia: sigue pendiente, y esta corroboración de texto no
sustituye la medición de primera mano sobre el panel completo.

## Fila B-bis (qué significa que el falsador no refute)

`R7.7`/`R7.3` no tienen aquí un falsador nuevo que corra — este acto no abrió
el `.dta` ni recalculó ninguna celda de T9b/ronda-1 (ya vienen medidas y
verificadas por el LEEME del depósito de mesa). Lo que este acto aporta es
procedencia textual, no un contraste falsable nuevo. Declarado explícitamente
para que no se lea como una fila B-bis silenciosa: **no hay falsador corrido
en esta pieza; NO-APLICA**.

## Enmiendas append

Dos entradas de `civico.clientelismo.*_mps2012` en
`milpa/tramite-ola5-propuesta-v0.yaml` reciben un campo
`enmienda_maestra38_l2` (append puro, sin editar ningún campo existente):
`vote_change_mps2012` (contexto de instrumento, no cambia p ni
`r7_7_estado`) y `prevalencia_lista_mps2012` (el
`supuesto_no_verificado_que_la_gobierna` queda `CORROBORADO-EN-TEXTO`, no se
re-mide `p`). `situacion` de ambas la cambia un acto siguiente con firma —
este acto no la toca.

## Contador

Rama TEXTO: piezas de L12 adjudicadas +2 (R7.3, R7.6 con veredicto
`NO-SELLADA` explícito bajo este instrumento; antes quedaban implícitas en la
prosa de `ADR-329`), FP-263 cerrada (EJECUTADA), medición: cero (ninguna
cifra nueva; todo lo citado ya estaba medido en el depósito de mesa del
2/sep, este acto solo lee procedencia textual y adjudica la pregunta de
insumo).
