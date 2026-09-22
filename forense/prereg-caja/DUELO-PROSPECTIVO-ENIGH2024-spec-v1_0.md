# DUELO PROSPECTIVO ENIGH 2024 · especificación congelable v1.0

`ACTO GEN2-ENIGH2024-SERIE-Y-COMMIT-1`, P3. Formaliza
`forense/prereg-caja/DISENO-duelo-prospectivo-ENIGH2024-v1_0.md` (PROPUESTA
de `ACTO GEN2-ENIGH2024-RESERVA-Y-DISENO-1`, sección de firma
`FP-260921-GEN2-ENIGH2024-RESERVA-Y-DISENO-1-b7ae-02`) a un contrato
ejecutable. **No repite la prosa del diseño** — cita su sección cuando la
decisión ya está tomada ahí; solo añade lo que el diseño dejó en prosa y
una spec congelable exige como campo.

**Este documento congela la spec ANTES de abrir ningún microdato de ENIGH
2024.** El primer resultado que produzca el procedimiento de abajo, sobre
la ola nueva, es el que se reporta — no se ajusta después de verlo (D-24,
patrón de dos/tres commits). Estado de la firma de adopción del diseño
(`b7ae-02`) al momento de este commit: **PENDIENTE**. Esta spec puede
congelarse (COMMIT-1: el procedimiento, no el resultado) sin esa firma —
es la firma la que autoriza declarar el duelo **CONGELADO** en el sentido
fuerte que abre la puerta a COMMIT-2/3; hasta entonces, el estado de este
documento es `RÍGIDO-SIN-ADOPCIÓN`, y se declara así en `## NO-CORRIDO /
RESERVAS` del encargo.

## 1 · Estimando, universo, escala

Verbatim `DISEÑO §1`: proporción de hogares con remesas > 0, ponderador
`factor` de hogar sin normalizar, escala logit para el ajuste, error
reportado de vuelta en puntos de proporción. Una sola celda nacional.

## 2 · Ventana de la serie

**2016, 2018, 2020, 2022** (4 olas de "nueva serie"; 2012/2014 fuera por
corte de metodología NCV — verificado en este acto, ver
`CALC-ENIGH2016-PERFIL-ESTRUCTURAL-0001/spec.md §2` — el DISEÑO ya lo
anticipaba por el salto de `n`, este acto añade la confirmación
independiente por `url_origen`). Los cuatro puntos: `CALC-B-0001`,
sellado antes de este acto, ajeno a su perímetro, citado con hash.

## 3 · Contendientes (DISEÑO §4, código en `tools/enigh_duelo_nacional.py`)

`C-PISO`, `C-T2`, `C-T3`, `C-TS`, `C-MEDIA` — los cinco, siempre, sin
selección tras ver el dato (F7 heredado del molde ENVIPE). Congelados y
verificados por comando (oro de reproducción de 2022 y coincidencias
exactas C-T2≡C-TS / C-T3≡C-TS) en `CALC-ENIGH-DUELO-ORIGEN-MOVIL-0001`,
sellado en este mismo acto — **ese resultado ES la validación de origen
móvil de esta spec**, no un ensayo aparte que haya que repetir.

## 4 · Nivel cruce y marginal: NO-CONSTRUIBLE (DISEÑO §3, verbatim)

Sin cambio: ningún par de ENIGH tiene historia de cruce abierta
(`CALC-ENIGH{2016,2018,2020,2022}-REMESAS-CONTEXTO-0001` están sellados en
4 olas cada uno **por este mismo acto**, pero eso es marginal por eje
dentro de UNA ola, no historia de UN cruce a través de olas — el §3 del
diseño exige la segunda cosa, y sigue sin existir). Se declara **no
construible**, no perdedor: nadie corrió el mecanismo (regla de salida de
θ, verbatim citada en DISEÑO §3).

## 5 · Regla de adjudicación (DISEÑO §5, verbatim, sin cambio)

Nivel nacional único. Un retador vence al piso solo si gana en (a) el
punto de 2024 Y (b) la validación de origen móvil (§3 de este documento).
Solo (a): `PROPUESTA CON RESERVA`. Ninguno gana: se adopta `C-PISO`.

**Nota de este acto sobre el resultado de origen móvil ya medido**
(`CALC-ENIGH-DUELO-ORIGEN-MOVIL-0001`, sellado): en la ventana retrospectiva
de 3 olas, `C-MEDIA` tiene MAE más bajo (0.1406 pp) que `C-PISO`
(0.1867 pp). **Esto no adjudica nada por sí solo** — la condición (b) de
esta sección exige TAMBIÉN ganar en el punto real de 2024, que este acto no
abre. Se declara aquí para que quien ejecute COMMIT-2/3 lo tenga presente
sin tener que releer el CALC.

## 6 · B-bis (DISEÑO §6, verbatim, sin cambio)

Las cuatro filas del pre-registro de falsación quedan igual — B-bis-1 a
B-bis-4, con la prioridad B-bis-1 > B-bis-3 si ambas se satisfacen a la
vez, declarada antes de ver 2024.

## 7 · Guardia de una variable (E.6, este acto)

`tools/enigh_duelo_guardian.py` (nuevo, propio de este acto, congelado en
este commit): única superficie de código autorizada a leer
`concentradohogar` de ENIGH 2024 antes de COMMIT-3. Lee solo
`folioviv, foliohog, factor, remesas, est_dis, upm` — ninguna otra columna,
ningún otro miembro del zip. `nacional()` rechaza un marco cargado con
`reservada=True`; `emite_bajo_reserva()` exige `reservada=True` Y
`autoriza=True` explícito. Probado contra zip sintético
(`tests/test_enigh_duelo_guardian.py`), nunca contra el zip real.

## 8 · D-22, salida cruda

1. **Preflight VERDE con `origin/main` fusionado, payload COINCIDE en
   caja.** `CALC-ENIGH-DUELO-EMISIONES-0001` (COMMIT-2, previsto, este
   acto) declara `enigh2024_ns_csv` como input `origen: manifiesto`;
   `tools/corrida0.py preflight CALC-ENIGH-DUELO-EMISIONES-0001` da
   `[COINCIDE]` sobre el hash del zip (identidad, no contenido — bajar y
   hashear no es abrir, E.6) sin llamar a `run` (que sí abriría el zip: PARO
   (a) de este encargo). Salida cruda en `## 9` de este documento.
2. **`_valida_outputs` acepta cada rama terminal, sobre sintético y sobre
   oro.** Sintético: los 6 tests de `tests/test_enigh_duelo_guardian.py`
   ejercitan `REPORTADO`, `NO-ESTIMABLE-SIN-HOGARES-VALIDOS` (marco vacío
   tras filtrar inválidos), `ReservaRota` (dos vías) y columna ausente.
   Oro: `CALC-ENIGH-DUELO-ORIGEN-MOVIL-0001` reproduce sus 27 RESULT sin
   `NO-VÁLIDO` alguno sobre la serie real.
3. **Todo nulo posible declarado.** Los `permite_no_estimable: true` de
   `CALC-ENIGH-DUELO-ORIGEN-MOVIL-0001/spec.yaml` cubren cada
   `MAE-PP`/`SESGO-PP`/`COBERTURA` que puede salir `None` con serie corta.
   Ningún `NaN`: `tools/enigh_duelo_nacional.py` y
   `tools/enigh_duelo_guardian.py` convierten todo no-finito a `None` antes
   de canonizar.
4. **Ningún input sobre archivo vivo.** `CALC-B-0001/resultados.json` (ya
   sellado, ajeno) y los tres `spec.md` de 2022 (ya sellados, ajenos) entran
   con sha256 declarado; ninguno se re-sellará contra su estado futuro.

## 9 · Preflight previsto — salida cruda

(Se pega literal el `preflight` de `CALC-ENIGH-DUELO-EMISIONES-0001`
inmediatamente después de escribir ese `spec.yaml`, en el mismo commit —
ver ese archivo.)

## 10 · Qué NO hace este acto (DISEÑO §7, heredado + restricción propia)

No abre, lista ni deriva nada de `enigh2024*` (PARO (a)). No corre
COMMIT-2 ni COMMIT-3 — quedan `PREVISTOS` (D-18 enmienda de cableado):
spec + medidor escritos y congelados, `preflight` verificado por hash,
`run` nunca invocado. El acto que los ejecute es otro, posterior a la firma
`b7ae-02` y a que mesa decida el régimen de universo (si aplica) igual que
`GEN2-DIN-LOTE-ENIF2024-COMMIT-1` lo dejó pendiente para su propio dominio.
