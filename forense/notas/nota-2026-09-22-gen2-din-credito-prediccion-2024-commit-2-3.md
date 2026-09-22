# Nota de cierre · ACTO GEN2-DIN-CREDITO-PREDICCION-2024-COMMIT-2-3

22/sep/2026, CAJA. Encargo:
`forense/encargos/2026-09-22-GEN2-DIN-CREDITO-PREDICCION-2024-COMMIT-2-3.md`
(sha256 cuerpo `9eef778c565e7746ccd73c9b1e0bcf450ce2196c2bb1ad4cddfbdfb50bba7901`).
Rama `acto/gen2-din-credito-prediccion-2024-commit-2-3`. Sucesor de
`#987`/COMMIT-1 (`forense/notas/nota-2026-09-21-gen2-din-credito-prediccion-2024-commit-1.md`).

## 0 · Desvío de premisa declarado (v2.16 §2)

El encargo pedía "P1 · COMMIT-2: `corrida0 run` …-EMISIONES-0001" — pero
`-EMISIONES-0001` **ya estaba corrido y sellado** desde `#987` (merged en
`origin/main` antes de que este acto empezara); su propia premisa §4 ("los
dos CALC sin `ejecucion.json`") estaba basada en un estado intermedio de
COMMIT-1, no en el final. Re-correrlo habría sido PARO f) del propio
encargo ("repetir una corrida") y E.3 lo niega mecánicamente. Replanteado
(logística/estado del repo, objetivo intacto): se saltó ese paso y se
siguió la secuencia real que `-ADJUDICACION-0001/spec.yaml` ya declaraba
(`commit_3a` **antes** de abrir el dato, luego `commit_2` = abrir 2024 y
extraer R, luego `commit_3` = adjudicar) — confirmado con el usuario antes
de abrir ningún dato real.

## 1 · Qué predijo el programa — antes de ver 2024

`#987` congeló, sin abrir ningún dato de 2024, cuatro contendientes por
`(conducta, celda)` en escala logit (`PERSISTENCIA`, `TENDENCIA-2/3/SERIE`)
para nueve conductas de crédito, y midió que `PERSISTENCIA` ganaba el
*backtest* histórico (2012→2021) en 7 de 9. Este acto (`commit_3a`) fijó,
**antes de abrir 2024**, la regla exacta para comparar esas predicciones
contra la realidad: como ninguno de los dos lados expone réplicas
bootstrap (R sólo trae punto+IC percentil; las emisiones sólo punto+IC
analítico en logit), se fabricaron 10 000 réplicas SINTÉTICAS por
cantidad (semilla `PCG64(20260922)`, orden de consumo declarado) y se
alimentaron al comparador de referencia del proyecto
(`tools/duelo/cruces_familia.py::adjudica()`) con `umbral_vence_pp=∞` —
**sin umbral de materialidad inventado**, heredando la postura de
`-EMISIONES-0001`. Eso hace que `VENCE-RETADOR` sea
INALCANZABLE-POR-DISEÑO en este acto: sólo `NADIE-VENCE` y
`PROPUESTA-CON-RESERVA` son alcanzables.

## 2 · Qué salió — 2024 ya abierto (`commit_2`)

Primera apertura real de la sección de crédito de ENIF 2024 (guardia de
una variable, `abre_conducta_2024`; 9 conductas autorizadas; el par
«crédito por app», K7, fuera de la lista blanca — PARO b) intacto).
n=12 379 personas 18-70. Veredicto por conducta (piso=`PERSISTENCIA`,
retador=mejor `TENDENCIA-X` habilitada por MAE puntual, sobre 12 de 16
celdas — ver §3):

| conducta | retador | veredicto | ΔMAE (pp) | IC95 | cobertura (R en IC del candidato) |
|---|---|---|---|---|---|
| K1 (tenencia, cualquier producto) | TENDENCIA-SERIE | **PROPUESTA-CON-RESERVA** | +1.90 | [+0.62, +2.65] | 0.56 (5/9) |
| K2-DEPARTAMENTAL | TENDENCIA-2 | NADIE-VENCE | +0.30 | [−1.25, +1.21] | 1.00 (9/9) |
| K2-NOMINA | TENDENCIA-3 | NADIE-VENCE | −0.12 | [−0.48, +0.15] | 0.33 (3/9) |
| K2-AUTOMOTRIZ | TENDENCIA-3 | NADIE-VENCE | +0.00 | [−0.39, +0.13] | 0.89 (8/9) |
| K3 (informal, algún tipo) | TENDENCIA-3 | NADIE-VENCE | +0.43 | [−1.00, +1.12] | 0.89 (8/9) |
| K4A-AUTOEXCLUSION | — | **NO-CONSTRUIBLE-SIN-RETADOR** (sólo 2 olas previas) | — | — | — |
| K4B-OFERTA | — | **NO-CONSTRUIBLE-SIN-RETADOR** (sólo 2 olas previas) | — | — | — |
| K5 (rechazo de solicitud) | TENDENCIA-SERIE | NADIE-VENCE | +0.75 | [−0.54, +1.40] | 0.89 (8/9) |
| K6-P-TENEDORES (atraso entre tenedores) | TENDENCIA-SERIE | **PROPUESTA-CON-RESERVA** | +2.62 | [+0.45, +3.50] | 1.00 (9/9) |

ΔMAE positivo = el retador (tendencia) tuvo MENOR error que persistencia.
`K1`/`K6` son las dos únicas conductas donde el IC95 completo de ΔMAE
queda por encima de 0 — la señal más fuerte que este diseño (sin umbral)
puede producir a favor de una tendencia. Las otras cinco comparables
(`K2-*`, `K3`, `K5`) no despejan 0: persistencia se sostiene.

**Contexto oferta-antes-que-preferencia (v2.16 §3):** K4B-OFERTA y K5,
reales de 2024, junto a cada celda de K1/K2-*/K3 en
`data/corrida0/duelo-credito-prediccion-2024.json` (`contexto_oferta`) —
no entran al cómputo de ΔMAE de esas conductas.

## 3 · Defecto heredado encontrado y declarado (no reparado — código sellado)

El eje **escolaridad completo** (4 de 16 celdas × 9 conductas) sale del
ajuste: `medidor.py` de `-ADJUDICACION-0001` (sellado en COMMIT-1) reusa
`_code()` de `-EJES-0003` (recorta el cero inicial) sobre `niv`, un código
2024 de DOS dígitos — "00".."09" caen a `None` (seguro, declarado) pero
"10"/"11" SÍ calzan bajo la etiqueta "superior", excluyendo silenciosamente
"08"/"09" (que también son "superior"): la celda ESCOLARIDAD-SUPERIOR de
este CALC mide sólo maestría/doctorado (N=283 de 12 379 en K1), no
educación superior completa. El código ya está sellado (E.3): no se edita.
Declarado en `NC-260922-GEN2-DIN-CREDITO-PREDICCION-2024-COMMIT-2-3-95ec-01`
y `FP-260922-…-95ec-01` (pide a mesa vía de corrección). `hallazgos.md`
tiene la línea.

## 4 · Lo que esto NO significa

**No tener crédito formal no es preferir el informal**: K1/K2-*/K3 miden
tenencia, no preferencia; el rechazo (K5) y la autoexclusión por oferta
(K4B) — reportados al lado — son parte de por qué alguien no tiene un
producto (requisitos, buró, oferta), no una elección revelada de
informalidad. Unidad **persona** (adulto elegido 18-70), no hogar ni
trámite. `PROPUESTA-CON-RESERVA` no es "tendencia gana": es "el IC excluye
0, pero este acto no fijó un umbral de materialidad para declarar
victoria" — la pregunta de si 1.9-2.6 pp es un cambio que importa
sustantivamente queda para mesa. Cobertura es descriptiva y con `n=9`
celdas que comparten la MISMA muestra de 2024 (no son 9 ensayos
independientes).

## 5 · Una línea

**¿Alguna tendencia venció a la persistencia en 2024? Estrictamente no
(`VENCE-RETADOR` es inalcanzable por diseño en este acto) — pero en 2 de 7
conductas comparables (K1, K6-P-TENEDORES) la tendencia tuvo un error
menor que persistencia con el IC95 completo por encima de cero
(`PROPUESTA-CON-RESERVA`); en las otras 5, persistencia se sostiene.**

## CONTADOR

`cuenta_gen2 = SI` para `CALC-DIN-CREDITO-PREDICCION-2024-ADJUDICACION-0001`
(decisiones.tsv, la etiqueta sellada de la spec ya decía `NO` y no se
edita — E.3; se asienta en decisiones.tsv, E.2); **no adopta** nada. Una
corrida real sellada en este acto (commit_2); replay `REPRODUCE`/`IDENTICO`
(`forense/replay-evidencia.tsv`).

`tests/check.py --rapido`: VERDE, 0 FAIL. **Pendiente de mesa:**
`FP-260922-GEN2-DIN-CREDITO-PREDICCION-2024-COMMIT-2-3-95ec-01` (vía de
corrección del defecto de escolaridad). `FP-…-7866-02` (regla de
adjudicación) queda FIRMADA por este acto. `FP-…-7866-01` (K6-P-TENEDORES
vs K6-PR) sigue ABIERTA, ajena a este acto.

## NO-CORRIDO / RESERVAS

`NC-260922-GEN2-DIN-CREDITO-PREDICCION-2024-COMMIT-2-3-95ec-01`: marginal
correcto de escolaridad, DECISIÓN-DE-MESA-PENDIENTE (§3 de aquí arriba).

## CONSUMIDO

Encargo archivado (0-bis, A.3); PR abierto por este acto, mesa fusiona.
