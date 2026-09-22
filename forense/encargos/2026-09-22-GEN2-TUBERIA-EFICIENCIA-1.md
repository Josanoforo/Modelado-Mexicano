# ENCARGO · ACTO GEN2-TUBERIA-EFICIENCIA-1 · CERRAR UN ACTO CUESTA MINUTOS: SUBCONJUNTO RÁPIDO EN LOCAL, EL CI COMO ÚNICO JUEZ, LOS DERIVADOS FUERA DE LOS PR, T16 Y EL CANAL DE WARN FUERA, SUITE ESTRICTA

> ENTORNO: **NUBE** con `gh` si lo hay (una sonda, ver P0); si no, NUBE igual. NO necesita CAJA.

CABECERA · SHA de redacción `6901853c`; re-deriva al abrir · LOTE (D-11): hasta cuatro piezas por PR; **puede ser más de un PR si el lote no cabe**, en este orden: A (P1–P3), B (P4–P6), C (P7) · MODO: **ABIERTO** · CONTADOR: ninguno numérico; **ningún contador de medición debe moverse** · FP/ADR/NC: raíz de acto. **MODELO: Sonnet por mandato de mesa (presupuesto del 21/sep).** D-13 pide Opus para actos que miden; mesa lo baja a Sonnet a sabiendas. Mitigación: el procedimiento ya está congelado, tu latitud es solo logística, y toda bifurcación que no esté en LATITUD se pregunta a mesa con opciones en vez de resolverse. Si en algún paso dudas entre dos interpretaciones del procedimiento, PARA y pregunta: ése es el riesgo que mesa acepta.
**Si al fusionar `main` choca la línea L0 de `canon/estado-programa-v1_14.md`: NO conserves los dos lados; toma la de `main` y re-inserta solo tu anotación.** `canon/L0/` existe: tu anotación va ahí como fragmento.

## 1 · OBJETIVO
Con la data de TUBERÍA (`EVALUACION-TUBERIA-PR-y-verificacion-2026-09-21`, `#955`): una corrida de CI tarda 198 s de mediana; la cascada corre la suite tres veces por cierre y una más por cada re-fusión; después de `#962` las renumeraciones son cero pero las re-fusiones siguen en 1–4 por PR, ahora por los archivos derivados; la suite emite 24 381 WARN que nadie lee; el baseline acepta 12 FAIL que ya no ocurren; T16 relanza la suite entera para comparar cero afirmaciones. Mesa vivió cierres de 40 minutos. «Hecho», **verificable por comando** sobre los 20 PR siguientes al merge de este lote: CONSUMIDO → merge ≤ 10 min de mediana · ≤ 1 re-fusión por PR · suite local antes de empujar ≤ 15 s · CI completo ≤ 90 s de mediana · 0 WARN en la salida de la suite · baseline sin FAIL aceptados. Los comandos de medición son los de `#955`, re-corridos por este acto al cerrar (P7).

## 2 · FIRMAS DE MESA — verbatim (mesa, 21/sep, sobre la evaluación de TUBERÍA)
«(1) Antes de empujar, un acto corre solo el subconjunto rápido de la suite; la suite completa la corre el CI una vez en el push y ése es el juez. (2) Los archivos derivados no viajan en los PR: un job del push a main los re-deriva y commitea. (3) T16 se retira; una sola derivación compartida por T32, T32-quater, T45 y el marcador, con salida idéntica; la cascada corre la suite una vez. (4) Los reports GEN1 de T06/T08 se declaran históricos; el baseline se re-congela con lo que ocurre hoy y la suite pasa a estricta. (5) El canal de WARN se retira. Cada familia pasa a FAIL acotado a los archivos que el PR toca, o a un contador del tablero derivado por comando; lo que no sea ninguna de las dos se borra. T10 pasa a FAIL acotado. El baseline deja de guardar WARN. Meta verificable: CONSUMIDO → merge ≤ 10 min de mediana, ≤ 1 re-fusión por PR, suite local ≤ 15 s.»
Y del trámite 5 (`#981`, hallazgo P3): «adoptar una celda-D debe mover `celdas_validadas` y `adoptados_activos` en el mismo commit; hoy el marcador no la cuenta hasta un mecanismo de `tools/` que no existe (NC-…-3619-01).»

## 3 · LO QUE DIRECCIÓN SABE (contra `6901853c`)
- `[EJECUTADO]` `tests/check.py`: `def t16` sigue; `acto.md:349,401,473` mandan la suite tres veces (`#980` tocó `acto.md` y `check.py`: re-lee). `tests/baseline.json`: 15 FAIL, 142 WARN aceptados. Suite en main hoy: 3 FAIL (T06 ×2, T08 ×1), 24 381 WARN, 235 s en un núcleo.
- `[EJECUTADO]` los 10 PR fusionados tras `#962` (`#963`…`#977`): 0 renumeraciones, re-fusiones 1–4 (mediana 3). `[LEÍDO: notas]` la causa que repiten: «re-deriva `usos.tsv` / marcador tras fusionar main».
- `[LEÍDO: evaluación §5]` tests con capturas propias: T02 (48), T22 (7), T30 (4), T15, T27, T34; guardias huérfanas (13). Los tres caros (T32 36 s, T32-quater 32 s, T35 7 s) nunca fueron los únicos en atrapar. `[LEÍDO: §3]` marcador llama `deriva()` 11 veces (12 s cada una, mismo resultado); T-PINES 5 derivaciones; T-CORRIDA0 `status` 7 veces y 283 subprocesos de git; T45 relanza `status`.
- `[EJECUTADO]` en `forense/hallazgos.md` y NC: 0 acciones originadas por un WARN. Familias: T35 13 845+ (replay), T34 177, T03 165, T22 69, T10 65.
- `[EJECUTADO]` `.gitattributes` con `merge=union` en gobierno (`#962`); `canon/L0/` por fragmentos.
- `[SUPUESTO]` si `main` exige ramas al día (protección de rama). P0 lo decide; cambia el diseño de P4.

## 4 · YA HECHO
`#962` (ids, L0, union), `#965` (enrutamiento), `#966`, `#980` (cierre rápido: qué cubre lo dices tú en la nota, línea por línea contra §2 — lo que ya esté, no se rehace). **Repítela tú.**

## 5 · PIEZAS
**P0 · Sonda.** `gh api repos/:owner/:repo/branches/main/protection` (o el equivalente): ¿`required_status_checks.strict`? Si no hay `gh`: pregunta a mesa en una línea y sigue con lo demás (P4 se diseña para las dos respuestas y elige al final).
**P1 · Subconjunto rápido.** `tests/check.py --rapido`: T02, T22, T25, T15, T27, T30, T34, T46–T52, sidecars y guardias huérfanas; ≤ 15 s medido; es lo que `acto.md` manda correr antes de empujar. La cascada corre **solo eso**; la suite completa la corre el CI.
**P2 · T16 fuera y una sola derivación.** Retirar T16. Una derivación del árbol real por corrida —`corrida0 status`/registro— compartida por T32, T32-quater, T45 y `test_marcador_segmento.py`, con copia por caso. Criterio: la salida de cada test es **byte a byte** la de hoy sobre `main`; ninguna aserción cambia. Medición antes/después.
**P3 · Baseline estricto y WARN fuera.** Declarar históricos los reports GEN1 de T06/T08 (regla E.1; lista por comando; un rótulo en `registro-rotulos.tsv`, no un edit de los reports); re-congelar con 0 FAIL; retirar del baseline los WARN. Cada familia de WARN: FAIL acotado a archivos tocados por el PR (T03, T10, T22 nuevos) o contador del tablero (T35, T34); lo demás se borra. La suite imprime FAIL/VERDE y nada más.
**P4 · Derivados fuera de los PR.** Lista por comando de los archivos «DERIVADO — NO EDITAR» (`corridas.tsv`, `resultados.tsv`, `usos.tsv`, demanda, marcador, tablero, …). Guarda en CI: un PR que los toque falla, salvo el job derivador. Job en push a `main` que los re-deriva por comando y commitea (`[deriva]` en el mensaje; sin loop). Si `main` exige ramas al día (P0): el job derivador debe poder empujar sin esa exigencia, o el diseño pasa a cola de merge; dilo y elige. `acto.md`: los actos ya no los re-derivan ni los commitean.
**P5 · Contador de celdas-D adoptadas.** Adoptar una celda-D (fila en `decisiones.tsv` + `champion_actual`) mueve `celdas_validadas` y `adoptados_activos` en la misma derivación. Test con una celda-D sintética adoptada. Cierra NC-…-3619-01. **No cambia ningún número ya sellado**; el piloto 3 (`GOB…edad_x_escolaridad`, `champion_actual: C2`) es el caso real: reporta el antes/después.
**P6 · Cascada.** `acto.md` y `cierre_acto.py`: una sola corrida (`--rapido`) antes de empujar; fusionar main **una vez**, al final; nada de re-derivar derivados. Plantilla v2.1: la línea de perímetro de cierre acorde.
**P7 · Medición de cierre.** Re-correr los comandos de `#955` sobre los PR fusionados desde este lote (o los 20 siguientes, si aún no hay): las seis cifras de «Hecho», antes/después. Si alguna no se cumple, se dice cuál y por qué, sin aflojar aserciones.

## 6 · LATITUD
Decides tú: implementación, nombres, cuántos PR, orden dentro del lote. Replantea y sigue ante main movido. Pregunta a mesa, siguiendo: el resultado de P0; y si alguna familia de WARN no cabe en «FAIL acotado» ni en «contador» y crees que sí debe conservarse (di cuál y qué defecto atrapa).

## 7 · PAROS — lista cerrada
a) aflojar, quitar o cambiar una aserción de un test que atrapa (T02, T22, T25, T15, T27, T30, T34, guardias, sidecars, T-REPRO, verificación de sellos) para ganar tiempo · b) tocar lo que protege abrir dato, congelar spec, adoptar o borrar (`corrida0 run/preflight/_valida_outputs`, guardián, reservas) · c) mover un contador de medición a mano · d) construir infraestructura nueva fuera de lo listado (D-14) · e) el job derivador crea un loop de commits.

## 8 · COMPUERTAS
«Salida byte a byte idéntica en P2» protege: nada de las cuatro — es criterio, no compuerta. No hay compuertas.

## 9 · PERÍMETRO
Propio: `tests/check.py`, `tests/baseline.json`, `tests/test_marcador_segmento.py`, `tools/tablero_programa.py`, `tools/cierre_acto.py`, `tools/estado_comun.py`, `.github/workflows/*.yml`, `.claude/commands/acto.md`, `forense/encargos/PLANTILLA-ENCARGO-v2_1.md` (una línea), `canon/registro-rotulos.tsv` (rótulo histórico), `tools/ci_guardias.py`, nota, cascada. Ajeno: `data/corrida0/CALC-*` · `milpa/` · celdas-D · reports GEN1 (no se editan: se rotulan). Si te encuentras escribiendo fuera de esta lista, PARA. **Actos en vuelo que tocan `tools/pines_mesa.py` y `tests/test_pines_mesa.py`: TANDA-5. No los toques.**

## 10 · NO HACE · SUCESORES · CIERRE
No mide · no re-adjudica · no borra historia de git (los blobs de L0 se quedan). Sucesor: `EFICIENCIA-2` con la medición de P7 si alguna meta no se cumplió. Auditoría §5: no aplica. Falsador a tres meses: si en diciembre CONSUMIDO → merge sigue > 10 min, este lote no sirvió y se anota. `## NO-CORRIDO / RESERVAS` · `## CONSUMIDO`.

## NO-CORRIDO / RESERVAS

- **qué**: P7 — re-correr los comandos de `#955` sobre los 20 PR siguientes al merge de este lote (las seis cifras de "Hecho" antes/después).
  **por qué**: `DIFERIDO-A:EFICIENCIA-2` — la meta verificable del lote (merge ≤10 min mediana, ≤1 re-fusión, CI ≤90s, 0 WARN, baseline sin FAIL) solo se puede medir después de que este PR se fusione y corran los 20 PR posteriores.
  **impacto**: la meta de "Hecho" del §1 del encargo no queda verificada por este acto.
  **sucesor**: `EFICIENCIA-2`. Fila: `NC-260922-GEN2-TUBERIA-EFICIENCIA-1-0d1b-01`.

- **qué**: `NC-260921-GEN2-CELDA-D-PILOTO-3-COMMIT-2-3-v1_3-3619-01` — levantar la reserva del par `CRUCE-GRUPO::tramite.gobierno_digital.util_sin_coercion_ejes_encig2025::edadxescolaridad` en `marcador-segmento.tsv`. A.8 (`python3 tools/ya_medido.py "tramite.gobierno_digital.util_sin_coercion_ejes_encig2025"`) -> MEDIDA-EN: tramite-ola5-propuesta-v0.yaml:1600 (tier SELLADA, p=0.681276, [NO-DISCRIMINA]) — cita ilustrativa del par ya conocido, no una clasificación nueva de este acto.
  **por qué**: `FUERA-DE-PERÍMETRO` — de `tools/marcador_segmento.py`, ajeno a este acto (§9 del encargo).
  **impacto**: el par sigue `RESERVADA`; el contador nuevo `celdas_d_adoptadas_activas` (P5) no depende de ese re-derivado y ya cuenta la celda-D adoptada por otra vía.
  **sucesor**: acto de aparato sobre `tools/marcador_segmento.py`. Fila: `NC-260922-GEN2-TUBERIA-EFICIENCIA-1-0d1b-02`.

## CONSUMIDO

PR #984. ADR-260922-GEN2-TUBERIA-EFICIENCIA-1-0d1b-01. `tests/check.py --rapido`: VERDE, 0 FAIL. `tests/check.py --baseline --parallel`: VERDE, exit 0, sin FAIL. El PR queda propuesto contra `main`; mesa central fusiona.
