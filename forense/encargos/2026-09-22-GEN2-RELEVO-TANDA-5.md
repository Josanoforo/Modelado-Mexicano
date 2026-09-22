# ENCARGO · ACTO GEN2-RELEVO-TANDA-5 · DIECIOCHO LECTURAS DEL LLM Y OCHO CORRIDAS DE CAMPO SALEN DE LEGACY POR LAS DOS PUERTAS QUE MESA ABRIÓ

> ENTORNO: **NUBE** (cualquiera): no abre microdato; todo está en el repo. Instala numpy/pandas si `verify` los pide (logística). NO es CAJA.

CABECERA · SHA de redacción `6901853c`; re-deriva al abrir · una sola sesión, rama `acto/gen2-relevo-tanda-5` · MODO: **ABIERTO** · CONTADOR: `dependencias_numericas_legacy_activas` baja en **exactamente** las lecturas pineadas (hoy 146; re-deriva el punto de partida); `adoptados_activos` antes y después, el número sale del comando · FP/ADR/NC: raíz de acto. **MODELO: Sonnet por mandato de mesa (presupuesto del 21/sep).** D-13 pide Opus para actos que miden; mesa lo baja a Sonnet a sabiendas. Mitigación: el procedimiento ya está congelado, tu latitud es solo logística, y toda bifurcación que no esté en LATITUD se pregunta a mesa con opciones en vez de resolverse. Si en algún paso dudas entre dos interpretaciones del procedimiento, PARA y pregunta: ése es el riesgo que mesa acepta.
**Si al fusionar `main` choca la línea L0 de `canon/estado-programa-v1_14.md`: NO conserves los dos lados; toma la de `main` y re-inserta solo tu anotación.** `canon/L0/` existe: tu anotación va ahí como fragmento.

## 1 · OBJETIVO
Cerrar las dos decisiones que el trámite 5 dejó fuera a propósito (A.12: viajan en su encargo). «Hecho»: los pines escritos y `ACEPTADO` por `valida_pin`; las dos firmas de §2 `FIRMADA` con este PR; la guarda (a) leyendo el eje RESULTADO también en la vía (i), con tests; `tests/test_pines_mesa.py` verde; el contador bajó en exactamente lo pineado.

## 2 · FIRMAS DE MESA — verbatim; el lanzamiento con este archivo es el sello
**F-L (pines de L):** «Se pinean por la vía (i) las 18 lecturas L con cobertura completa (8 de 8 réplicas válidas): las seis CIV (M-01, 02, 04, 10, 12, 13) y las tres FAM (M-05, 06, 07), en sus dos variantes (L-solo y L+corpus), al RESULT de `CALC-L-DESDE-CAPTURAS-v1_0`. Las siete con abstención (DIN-M-01, FAM-M-01, TRA-M-02, TRA-M-03, TRA-M-07) quedan en propuesta con reserva y no se pinean: un IC degenerado por una sola réplica no adjudica. `CALC-TRIADA-0001/0002` no se tocan.»
**F-R (vía (i), eje RESULTADO):** «La lectura del eje RESULTADO del replay vale igual para la vía (i); el CONTEXTO se declara en la nota de cada pin. Se aplica a las ocho corridas de la nota de TANDA-4 §3: CALC-R-DIN-M-01, -FAM-M-01, -FAM-M-05, -FAM-M-06, -FAM-M-07, -TRA-M-02, -TRA-M-03, -TRA-M-07.»
Ya vigentes, cítalas del repo: 4.1 (21/sep, TANDA-3 `:8`); 7bf5-01 (eje RESULTADO en vía (ii), FIRMADA por `#959`); los 9 L (7bf5-03, FIRMADA).

## 3 · LO QUE DIRECCIÓN SABE (contra `6901853c`)
- `[EJECUTADO]` `forense/analisis/gen2-l-desde-capturas-1/lista-pineables-v1_0.md`: 18 slots «cobertura completa» (8/8), los de F-L; 7 con abstención. `CALC-L-DESDE-CAPTURAS-v1_0` sellado en `main` (`#973`).
- `[EJECUTADO]` `forense/replay-evidencia.tsv`: exactamente 8 `CALC-R-*` con `REPLICA-RESULTADO · CONTEXTO-DISTINTO`; son los de F-R. `pines-de-mesa.tsv` trae 14 pines `CALC-R-` ya escritos (las lecturas `::R` que sí tenían REPRODUCE): busca por objeto qué lecturas de esas ocho corridas siguen legacy antes de escribir nada.
- `[LEÍDO]` `tools/pines_mesa.py:287-290`: la guarda (a) para la vía (i) exige `REPRODUCE`; TANDA-4 dejó la vía (ii) leyendo el eje RESULTADO con tokens derivados del vocabulario de `corrida0`. **Extiende, no dupliques:** el mismo derivador de tokens afirmativos sirve para (i).
- `[LEÍDO: nota de TANDA-4]` la vía (i) siguió estricta a propósito «mientras mesa no firme otra cosa»: F-R es esa firma.

## 4 · YA HECHO
Por objeto («TANDA-5», «L-solo», «CALC-R-DIN-M-01», «vía (i)») en encargos, `pines-de-mesa.tsv` y ramas vivas: los 14 pines `::R` de TANDA-3; ningún pin L; ninguna extensión de (i). **Repítela tú.**

## 5 · PIEZAS
**P1 · Guarda (a), vía (i).** Acepta los tokens afirmativos en RESULTADO; rechaza `NO-REPRODUCE*` y `NO-EJECUTABLE`; el mensaje dice por qué; un test por token del vocabulario real, y uno que pruebe que `NO-VERIFICABLE` en CONTEXTO no basta solo.
**P2 · Pines de L (F-L).** 18 pines, vía (i), al RESULT correspondiente de `CALC-L-DESDE-CAPTURAS-v1_0`, con la nota «mediana sobre 8/8 capturas selladas». `valida_pin` → `ACEPTADO`. Contador −18 (si alguna lectura ya no estaba en legacy, reporta el número real y por qué).
**P3 · Pines de las ocho CALC-R (F-R).** Para cada lectura legacy que cite una de las ocho corridas: pin vía (i) con el CONTEXTO declarado en `nota` (qué input cambió, en qué commit). Contador baja en las que existan; reporta cuántas.
**P4 · Cierre.** Las dos FP `FIRMADA`; NC-0425 y NC-…-7bf5-03 cerradas con cita a `#973` (el trámite 5 no pudo porque `#973` aún no estaba en main); vista y tablero por comando; nota: cuántas salieron de legacy, por qué puerta, y las 7 de L que quedan con reserva.

## 6 · LATITUD
Decides tú: orden, nombres, cómo derivas los tokens. Replantea y sigue ante main movido o ids renombrados. Pregunta a mesa, siguiendo: si alguna de las 18 lecturas L cita un RESULT que no existe con ese nombre.

## 7 · PAROS — lista cerrada
a) el contador baja en más lecturas que las pineadas · b) pinear una de las 7 L con reserva, o cualquier lectura no cubierta por F-L/F-R · c) admitir `NO-REPRODUCE` o `NO-EJECUTABLE` en cualquier vía · d) editar un sello, un `resultados.json` o `lista-pineables-v1_0.md` · e) `DIN-M-01:M` deja de ser legacy (vetado).

## 8 · COMPUERTAS
«Tests de P1 en verde antes de escribir un pin» protege: **adoptar**.

## 9 · PERÍMETRO
Propio: `tools/pines_mesa.py` · `data/corrida0/pines-de-mesa.tsv` · `tests/test_pines_mesa.py` · las dos filas FP y las dos NC · derivados por comando · nota · cascada. Ajeno: todo lo demás; en especial `tests/check.py`, `tools/cierre_acto.py`, `tools/tablero_programa.py` (TUBERÍA en vuelo). Si te encuentras escribiendo fuera de esta lista, PARA.

## 10 · NO HACE · SUCESORES · CIERRE
No mide · no re-sella · no toca las 7 L con reserva. Sucesor: firma de mesa sobre las 7 cuando haya más capturas. `## NO-CORRIDO / RESERVAS` · `## CONSUMIDO`.

## NO-CORRIDO / RESERVAS

- **qué**: P2 · los 18 pines de L (F-L) vía (i) al RESULT de `CALC-L-DESDE-CAPTURAS-v1_0`. **por qué**: `PARO-PREMISA` — la guarda (a) rechaza los 18 porque el registro deriva `resultado_replay = NO-VERIFICADO` para ese CALC (no el `REPRODUCE`/`IDENTICO` que `forense/replay-evidencia.tsv:175` asienta). Causa raíz: `tools/corrida0.py::_evidencia_vigente` compara `input_sha256_efectivos` como cadena ordenada; el asiento se escribió con el orden de declaración de `spec.yaml` y hoy se deriva con `sorted()` — mismo conjunto de pares `id=hash` (verificado como `set` en Python), orden distinto, falsa discrepancia. `tools/corrida0.py` es perímetro ajeno a este acto (§9); no se toca. **impacto**: 18 lecturas L (`marco-M::{CIV-M-01,02,04,10,12,13; FAM-M-05,06,07}::{L-solo,L+corpus}`) siguen legacy; `dependencias_numericas_legacy_activas` se queda en 146 en vez de bajar a 128. **sucesor**: `DIFERIDO-A: NC-260922-GEN2-RELEVO-TANDA-5-f54e-01` (acto que corrija `_evidencia_vigente` para comparar por conjunto, no por cadena ordenada; task sugerida `task_8d287fca`).
- **qué**: P3 · pines vía (i) para lecturas legacy que citen las ocho corridas de F-R (`CALC-R-DIN-M-01, -FAM-M-01, -FAM-M-05, -FAM-M-06, -FAM-M-07, -TRA-M-02, -TRA-M-03, -TRA-M-07`). **por qué**: `SUSTITUIDO-POR:GEN2-RELEVO-TANDA-3` — búsqueda por objeto contra el registro derivado (`corrida0._filas_registro`) confirma que los 8 usos `::R` de estas corridas ya son `GEN2` desde TANDA-3, pineados vía (i) citando los sucesores `-v2/-v3/-v4` de cada CALC (que `REPRODUCEN` estricto), no la base que F-R nombra. Ningún uso activo cita hoy el CALC base sin sufijo, y ningún downstream ingiere su `resultados.json`. Absorbido por: los 8 pines `::R` ya vigentes en `data/corrida0/pines-de-mesa.tsv` (vía TANDA-3). Huérfano: ninguno — F-R queda `FIRMADA` como habilitación general de la vía (i) por eje, disponible para el día en que un consumidor cite el CALC base. **impacto**: ninguno sobre el contador; cero pines nuevos. **sucesor**: `SIN-ASIGNAR` (nada pendiente salvo que un futuro consumidor cite el CALC base directamente).
- **qué**: las 7 lecturas L con reserva (`DIN-M-01`, `FAM-M-01`, `TRA-M-02`, `TRA-M-03`, `TRA-M-07`). **por qué**: `FUERA-DE-PERÍMETRO` — el encargo lo veda explícitamente (§10, "no toca las 7 L con reserva") y F-L las deja fuera por diseño (IC degenerado por una sola réplica no adjudica). **impacto**: ninguno — siguen en propuesta con reserva, como F-L declara. **sucesor**: firma de mesa sobre las 7 cuando haya más capturas (§10 del encargo).
