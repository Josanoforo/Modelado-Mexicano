# Nota de cierre · ACTO GEN2-ENIGH2024-DUELO-COMMIT-2-3 · 22/sep/2026

## 0 · ARRANQUE

Worktree `/home/pc0/mm-gen2-enigh2024-duelo-commit-2-3`, rama
`acto/gen2-enigh2024-duelo-commit-2-3`, sobre `origin/main = bda6b60c` (SHA de
redacción del encargo, coincide exacto). Guard de arranque (0.a-0.d): base al
día, árbol limpio, sin duplicado (rótulo ausente de remoto/worktrees/PR
abiertos), higiene reportada (`tools/limpia_arbol.py --reporta`). Entorno:
`python3 tools/entorno.py --arranque` → `ENTORNO-DERIVADO = CAJA` (coincide con
lo asignado), `data-raw-en-este-worktree: SI` tras enlazar `data/raw` y escribir
`data/raices.local.yaml`. `F3`: esta sesión no es la de `#988` (que congeló) —
`#988` está `MERGED` (verificado `gh pr list`).

## 1 · Premisa corregida contra el árbol (A.8)

El `[SUPUESTO]` de §3 del encargo aplicó: `#988` dejó únicamente
`CALC-ENIGH-DUELO-EMISIONES-0001` (preflight VERDE, sin correr) y
`CALC-ENIGH-DUELO-ORIGEN-MOVIL-0001` (sellado). No existía ningún
`CALC-ENIGH-DUELO-ADJUDICACION-0001`. Se construyó y se congeló en P0, sobre el
molde `CALC-DUELO-ENVIPE2026-ADJUDICACION-0001` (estructura), adaptado al
alcance real del diseño ENIGH 2024 (nacional único, sin ejes ni cruces —
`DISENO-duelo-prospectivo-ENIGH2024-v1_0.md §3`): 55 `RESULT` en vez de los
~3000 de la ENVIPE, porque no hay marginales ni cruces que enumerar.

## 2 · P0 · Firma, adopción, congelación de la adjudicación

- `FP-260921-GEN2-ENIGH2024-RESERVA-Y-DISENO-1-b7ae-02` → `FIRMADA` (mesa,
  verbatim en §2 del encargo). `FP-260921-GEN2-ENIGH2024-SERIE-Y-COMMIT-1-7492-01`
  (la pregunta de si el lanzamiento cuenta como adopción) queda `CERRADA`: la
  respuesta es la firma explícita, no la inferencia.
- Línea de adopción añadida a la cabecera de
  `DISENO-duelo-prospectivo-ENIGH2024-v1_0.md` (única edición, A.10 — el resto
  del documento permanece verbatim).
- `CALC-ENIGH-DUELO-ADJUDICACION-0001` construido, probado contra tres casos
  sintéticos (`VENCE-AL-PISO`, `C-PISO-ADOPTADO`, `NO-ESTIMABLE`; ninguno tocó
  ENIGH 2024) y congelado con `emisiones_selladas.sha256 = PENDIENTE-COMMIT-3a`.
  Preflight: `BLOQUEADO` solo por ese input pendiente (D-18, enmienda de
  cableado — no es PARO).
- Censo (A.15): `grep` sobre `tools/`/`tests/` confirma que ninguna superficie
  fuera de `enigh_duelo_guardian.py`/`enigh_duelo_nacional.py`/su test leyó
  `enigh2024*`.
- Preflight de `CALC-ENIGH-DUELO-EMISIONES-0001` re-verificado en este
  worktree: `VERDE`, `enigh2024_nc_csv` `[COINCIDE]` (mismo sha que `#988`
  verificó, corpus compartido vía `data/raw` → `/home/pc0/mm-corpus/raw`).

## 3 · P1 · COMMIT-2 — se abre el dato

`corrida0 run CALC-ENIGH-DUELO-EMISIONES-0001`, `exit_code=0`, sellado.
Primera y única apertura de `enigh2024_ns_csv.zip` de este acto, exclusivamente
vía `tools/enigh_duelo_guardian.py::emite_bajo_reserva`.

**R(remesas>0, nacional, 2024) = 0.039474 [0.037617, 0.041374], n=91 414
válidos, 0 inválidos.**

Las cinco predicciones, ciegas a este número (calculadas sobre 2016-2022):

| contendiente | p̂ | IC95 |
|---|---|---|
| C-PISO | 0.045694 | [0.043773, 0.047770] |
| C-T2 | 0.047693 | [0.043239, 0.052580] |
| C-T3 | 0.044027 | [0.041143, 0.047104] |
| C-TS | 0.043884 | [0.041535, 0.046359] |
| C-MEDIA | 0.046030 | [0.044987, 0.047097] |

**El punto real de 2024 cae por debajo de las cinco predicciones y fuera de
los cinco IC95.** No es un resultado que ningún contendiente mecánico
anticipara: la proporción de hogares con remesas cayó más de lo que persistir,
promediar o extrapolar la serie 2016-2022 hubiera sugerido.

## 4 · P2 · COMMIT-3a y COMMIT-3 — adjudicación

COMMIT-3a: única edición prevista (`inputs.emisiones_selladas.sha256`),
commit propio. `corrida0 run CALC-ENIGH-DUELO-ADJUDICACION-0001`,
`exit_code=0`, sellado.

| contendiente | error 2024 (pp) | MAE retrospectivo (pp) | condición (a) | condición (b) | veredicto |
|---|---|---|---|---|---|
| C-PISO | 0.622 | 0.187 | — | — | (piso) |
| C-T2 | 0.822 | 0.426 | NO | NO | NO-VENCE |
| C-T3 | 0.455 | 0.314 | SI | NO | PROPUESTA-CON-RESERVA |
| C-TS | 0.441 | 0.324 | SI | NO | PROPUESTA-CON-RESERVA |
| C-MEDIA | 0.656 | 0.141 | NO | SI | NO-VENCE |

**Veredicto general: `C-PISO-ADOPTADO`.** Ningún retador satisface las dos
condiciones de §5 del diseño a la vez. C-T3 y C-TS ganan el punto de 2024
(errores 0.455pp y 0.441pp contra 0.622pp del piso) pero pierden la validación
retrospectiva (MAE 0.314pp y 0.324pp contra 0.187pp del piso) → propuesta con
reserva, no adjudican. **C-MEDIA — el contendiente con el MAE retrospectivo
más bajo de los cinco (0.141pp) — pierde el punto real de 2024** (0.656pp,
peor que el piso): ganar en retrospectiva no bastó para ganar el duelo
prospectivo.

**B-bis, con vocabulario cerrado:**
- **B-bis-1 (el piso aguanta): `CORROBORADA`.** Tercera prueba prospectiva
  (junto con las de ENVIPE/ENIF ya corridas en el programa) en que ningún
  retador mecánico vence al piso de persistencia a nivel nacional.
- **B-bis-2 (tendencia legible): `ACOTADA`.** Ninguna de C-T2/C-T3/C-TS vence
  a C-MEDIA bajo la misma regla de dos condiciones — con cuatro puntos no se
  distingue tendencia de ruido (operacionalización propia, declarada en el
  docstring de `medidor.py`, congelada antes de abrir dato).
- **B-bis-3/4 (¿la retrospectiva predice el punto nuevo?): `FALSADOR-DÉBIL`.**
  El ganador retrospectivo es `C-MEDIA`; el ganador del punto de 2024 es
  `C-TS`. Distintos. Con una sola ola nueva no se puede separar "la
  retrospectiva no sirve" de "2024 fue atípico" (diseño §6, verbatim) — se
  declara y se espera a ENIGH 2026.
- Nivel cruce y marginal-por-eje: `NO-CONSTRUIBLE`, fijo (diseño §3/§4.3) —
  nadie corrió el mecanismo contra esta fuente, no es una derrota.

## 5 · P3 · Cierre — marcador, tablero, nota

`data/corrida0/decisiones.tsv:reserva:enigh2024-remesas-nacional-liberada`:
la reserva de `reserva:enigh2024` queda levantada **solo** para el estimando
`remesas>0` nacional, exactamente lo que los dos CALC sellados de este acto
emitieron. **Todo lo demás de ENIGH 2024 sigue RESERVADA** — ninguna otra
variable de `concentradohogar`, ningún corte, cruce, marginal, tabulado o
comunicado queda abierto por este acto. `tools/tablero_programa.py` corrido
por comando (TUBERÍA, no editado): sus indicadores son de programa general
(ramas, motor, propuesta) y no traen una fila granular por CALC — no hay
salida derivada que commitear (CLAUDE.md: derivados no se commitean, los
re-deriva el job de main).

## 6 · Qué NO significa lo de arriba (auditoría §5 de instrucciones)

Heredado y ratificado del diseño (§8), con la cifra real de 2024 a la vista:

- **No dice nada sobre disposición al envío, solidaridad familiar o
  reciprocidad.** Que el piso de persistencia gane no significa que los
  hogares receptores sean "inerciales": la incidencia de remesas depende, en
  orden de peso, de que el hogar tenga un migrante (decisión tomada años
  antes, casi siempre por otra persona), del mercado laboral
  **estadounidense**, del tipo de cambio y del costo de envío — estructura
  económica transnacional, no conducta del hogar receptor.
- **La caída de 2024 no se lee como "las familias dejaron de ayudarse".** Es
  exactamente el tipo de movimiento que este duelo mide sin explicar: ningún
  contendiente mecánico lo anticipó, lo que es consistente con un choque de
  origen económico/cambiario/migratorio, no con un cambio gradual de
  conducta (que sí hubiera favorecido a la persistencia o a la tendencia).
- **No prueba nada sobre montos de remesas**, solo sobre incidencia
  (recibe/no recibe). El estimando de intensidad (monto) existe en una sola
  ola (2022, pesos corrientes sin deflactor) y no se compara aquí (escala
  distinta, §4.3 de instrucciones).
- **ENIGH sub-capta el ingreso alto y las remesas informales.** Este duelo
  mide la capacidad de predecir la **propia serie** de ENIGH, no la validez
  de esa serie contra la remesa real recibida en México.
- **Unidad hogar, no persona.** Un hogar con remesas puede tener uno o varios
  migrantes; esta cifra no cuenta personas ni migrantes.
- **No adopta nada al motor.** `cuenta_gen2 = SI` en las dos etiquetas, `no
  adopta` — mide, no mueve ninguna regla `SI-ENTONCES`.
- **¿Cuántos contadores movió este acto?** Dos corridas selladas
  (`cuenta_gen2 = SI` en ambas), cero adopciones al motor. La reserva de
  ENIGH 2024 baja de "entera" a "entera salvo una celda nacional ya medida".

## 7 · Verificación final

`python3 tests/check.py --rapido`: `0 FAIL · 298 WARN` (deuda pre-existente,
ninguna nueva de este acto — la única que este acto introdujo, un T22 roto al
cerrar `FP-...-7492-01`, se corrigió en el mismo commit trasladando la cita a
`b7ae-02`, sin tocar `tests/check.py`).

## 8 · Sucesores

- Fecha límite ya cumplida (encargo original proponía 31/oct/2026 para
  COMMIT-2; este acto llegó el 22/sep/2026).
- La comparación C-MEDIA-gana-retrospectiva-pero-pierde-2024 es un dato para
  la regla de salida de θ del programa (misma familia que ENVIPE/ENIF): se
  deja declarado aquí, no se decide en este acto (fuera de perímetro —
  pertenece a un acto de síntesis de las tres pruebas prospectivas).
- ENIGH 2026 (próxima ola) podría resolver B-bis-3/4 (falsador débil):
  sucesor sin dueño, `SIN-ASIGNAR`.
