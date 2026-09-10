# ENCARGO · ACTO GEN2-F5-TRIADA-CALC

Recibido en mesa 10/sep/2026 (despacho 5/5 y último de la batería que la
firma de mesa pidió el 9/sep — "necesito que midas al menos 5 encargos a
correr en claude code... dame 5 completos"). Texto verbatim del
lanzamiento:

> ENCARGO 5/5 · ACTO GEN2-F5-TRIADA-CALC
>
> LLM SOLO vs LLM CON CORPUS vs MOTOR
>
> OBJETIVO: adjudicar la pregunta central del programa sobre una generación común de evidencia:
> ¿qué rinde mejor en el panel sellado: L_SOLO, L_CORPUS o M?
>
> CABECERA: NUBE, Opus. Cero microdato. Cero llamadas nuevas a Claude. Consume exclusivamente productos sellados de 1/5, 2/5, 3/5 y 4/5.
>
> COMPUERTA, POR PRODUCTO:
> Deben existir y verificarse:
>
> 1. extractor L v1.3 + manifiesto de extracción;
> 2. spec TRIADA sellada;
> 3. `UR` congelado y árbitros R sellados;
> 4. snapshot M congelado y firewall por celda.
>
> Si falta cualquiera, PARO. No improvisar sustituto.
>
> FIRMA DE CONTADOR CON OBJETO:
> `cuenta_gen2 = SI para el CALC-TRIADA que este acto selle`.
> El merge perfecciona la firma.
>
> FIRMA DE ADJUDICACIÓN:
> Mesa autoriza aplicar exactamente la escala de la spec TRIADA. La firma autoriza aceptar como salida válida tanto un ganador como `SIN-GANADOR-UNICO` o `NO-ADJUDICABLE-POR-CONTROL`. No existe obligación de coronar a nadie.
>
> P1 · ESPEJO DEL CONTRATO, COMMIT-1
> Crear `CALC-TRIADA-*`.
> Su `spec.yaml` copia por hash, sin reinterpretar:
>
> * `U0`;
> * `UR`;
> * regla para `U3`;
> * 3 contendientes;
> * regla de agregación L;
> * snapshot M;
> * árbitros;
> * MAE;
> * Δ pareados;
> * bootstrap;
> * δ=0.5 pp;
> * cobertura;
> * escala pareada;
> * escala global;
> * secundaria TRANSFERENCIA;
> * rol diagnóstico de B.
>
> Declarar todos los RESULT antes de calcular.
> Como mínimo:
> Cobertura
>
> * `RESULT-TRIADA-U0-N`
> * `RESULT-TRIADA-UR-N`
> * `RESULT-TRIADA-U3-N`
> * cobertura L_SOLO
> * cobertura L_CORPUS
> * cobertura M
> * exclusiones por contaminación/identidad
>
> Primarios
>
> * `MAE-L-SOLO`
> * `MAE-L-CORPUS`
> * `MAE-M`
>
> Pareadas
>
> * Δ L_CORPUS - L_SOLO + IC95 + veredicto
> * Δ M - L_SOLO + IC95 + veredicto
> * Δ M - L_CORPUS + IC95 + veredicto
>
> Global
>
> * ranking puntual 1/2/3
> * `VEREDICTO-TRIADA`
>
> Secundaria
>
> * resultados de TRANSFERENCIA bajo el universo donde sus cortes sean comparables.
>
> Cierra P1 con:
> «El primer resultado producido por este procedimiento es el reportado. No se amplía universo, no se cambia agregación, no se recalibra M y no se vuelve a capturar L después de observar el ranking.»
>
> P2 · CÓMPUTO, COMMIT-2
> Ejecutar:
> `preflight → run → verify`.
> Por cada celda de `U3`, producir una fila durable:
> `id · R · L_SOLO · error_L_SOLO · L_CORPUS · error_L_CORPUS · M · error_M · cobertura/réplicas · firewall · notas de corte`.
> Usar exactamente el mismo conjunto de celdas para los tres MAE.
> Los bootstrap pareados usan los mismos índices de celda en los tres contendientes.
> Prohibido:
>
> * quitar outliers;
> * cambiar a mediana porque la media no gustó;
> * dar más peso a una familia;
> * contar las 8 réplicas como 8 tareas independientes;
> * elegir la mejor réplica;
> * volver a correr un brazo;
> * calibrar M;
> * completar R;
> * modificar extractor;
> * reinterpretar B como cuarto contendiente.
>
> Un defecto material descubierto produce PARO/INCONCLUSO, no una reparación dentro del mismo cómputo.
>
> P3 · VEREDICTO
> La nota de cierre abre con una frase inequívoca:
> RESULTADO PRIMARIO: [GANADOR-TRIADA-L_SOLO / GANADOR-TRIADA-L_CORPUS / GANADOR-TRIADA-M / SIN-GANADOR-UNICO / NO-ADJUDICABLE-POR-CONTROL], sobre `U3 = n` celdas del marco de 14.
> Después:
>
> 1. tabla MAE y ranking puntual;
> 2. tres comparaciones pareadas con IC95 y veredicto;
> 3. cobertura sobre todo `U0`;
> 4. tabla por celda;
> 5. secundaria TRANSFERENCIA;
> 6. B, sólo como diagnóstico si aporta información;
> 7. sensibilidad pertinente ya pre-registrada;
> 8. límites.
>
> P4 · LECTURAS PERMITIDAS
> Si gana L_SOLO:
> En este panel, añadir el corpus no produjo mejor desempeño operacional que usar el LLM solo y el motor tampoco lo superó bajo la regla fijada.
> Si gana L_CORPUS:
> En este panel, el LLM con corpus superó tanto al mismo LLM sin corpus como al motor bajo la regla fijada.
> Si gana M:
> En este panel, el motor superó tanto al LLM solo como al LLM con corpus bajo la regla fijada.
> Si no hay ganador:
> El panel no permite identificar un ganador único bajo la magnitud, incertidumbre y cobertura pre-registradas.
> Ninguna salida autoriza por sí sola:
>
> * causalidad;
> * «todos los mexicanos»;
> * «todos los LLM»;
> * cualquier modelo/versionado futuro;
> * cualquier tarea fuera del marco;
> * declarar que corpus «explica» la diferencia sólo porque L_CORPUS gane;
> * declarar que el motor es universalmente mejor porque gane 14 tareas.
>
> P5 · QUÉ SIGUE SEGÚN EL RESULTADO
> El sucesor no se decide por preferencia por un contendiente, sino por el diagnóstico:
>
> * Si hay ganador único con cobertura suficiente: F6 · COSECHA, informe central con cadena citable.
> * Si L_CORPUS > L_SOLO pero M no se distingue de L_CORPUS: siguiente experimento debe discriminar arquitectura, no hacer más corpus por inercia.
> * Si M > ambos L: siguiente paso es validación prospectiva/holdout, no recalibración retrospectiva.
> * Si L_SOLO ≈ L_CORPUS: investigar utilidad real del acceso documental antes de ampliar corpus.
> * Si `SIN-GANADOR-UNICO`: estudiar la fuente dominante de incertidumbre o ampliar prospectivamente el marco bajo una spec nueva. No añadir celdas a este CALC.
> * Si control/identidad bloquea: sucesor mínimo al defecto concreto.
>
> PERÍMETRO Y CONCURRENCIA
> Toca:
>
> * `data/corrida0/CALC-TRIADA-*/`
> * vistas corrida0 derivadas;
> * `forense/notas/` resultado;
> * `forense/no-corrido.tsv`;
> * `data/corrida0/decisiones.tsv` por firma de contador;
> * 0-bis;
> * cascada.
>
> NO toca:
>
> * capturas;
> * extractor;
> * spec TRIADA;
> * R sellados;
> * snapshot M;
> * `milpa/`;
> * marcador histórico;
> * F5 v1.0;
> * B;
> * corpus.
>
> Si al correr se necesita editar cualquiera de esos inputs, PARO. El contrato estaba incompleto y saberlo es el resultado correcto.
>
> CIERRE
> Orden obligatorio:
>
> 1. resultado primario;
> 2. cifras y universo;
> 3. cobertura;
> 4. pareadas;
> 5. secundaria;
> 6. límites;
> 7. contadores antes/después;
> 8. cascada;
> 9. `## NO-CORRIDO / RESERVAS`;
> 10. `## CONSUMIDO` con PR.
>
> Éste es el acto que debe contestar la pregunta del proyecto. No termina cuando alguien gana. Termina cuando sabemos, con una regla fijada antes del resultado, si L_SOLO, L_CORPUS o M rindió mejor en el panel que decidimos usar.

---

## Compuerta verificada (por producto, contra `origin/main = c439065`)

10/sep/2026, antes de cualquier edición sustantiva. Los cuatro productos
que el encargo exige existen en `origin/main` y se citan por hash:

| # | Producto exigido | Ruta | `sha256` en `origin/main` |
|---|---|---|---|
| 1 | extractor L v1.3 | `tools/extrae_l_v1_3.py` | `ecfbd8491f9b353d9eebdb25f0afa6eddf4f0d3082cff50c3db7d8f5ddd8ff5e` |
| 1 | manifiesto de extracción | `forense/prereg-duelo-v2/manifiesto-extraccion-L-v1_3.json` | `a1e5d609fe0044eef44d3365b308004daeaa8d511f4692464b422e1296e75809` |
| 2 | spec TRIADA sellada | `forense/prereg-duelo-v2/F5-contrato-triada-spec-v1_1.md` | `db6b24c579e72dc705c772200ca2c4066bd9708cc6c06c85c5101d56b081b4f5` (coincide con su `.sha256` sellado) |
| 3 | `UR` congelado (14/14) | `forense/prereg-duelo-v2/universo-triada-v1_4.tsv` | `840fc68ce7261686426221effbf9df313ef17e2876fa6345b3c00589bab80f80` (coincide con su `.sha256` sellado) |
| 3 | árbitros R sellados | 14 `CALC-R-*` citados por el sidecar | 14/14 con `resultados.json` + `sello.json` + `sello.sha256` + `spec.yaml` en `origin/main` |
| 4 | snapshot M congelado + firewall por celda | `forense/prereg-duelo-v2/snapshot-M-triada-v1_0.json` | `b53ac6d51d1b50ce929fdf1b3e14b124c11db39fb216a15d7073a287ed3f065c` (14/14 celdas con `estado_firewall` y `razon_firewall`) |

Comandos: `git cat-file -e origin/main:<ruta>` + `git show origin/main:<ruta> | sha256sum`
para cada fila; para los 14 `CALC-R`, `git cat-file -e` sobre los cuatro
archivos de cada directorio nombrado en la columna `fuente_R` de
`universo-triada-v1_4.tsv`. **COMPUERTA CUMPLIDA — 4/4.**

---

## Cierre — orden obligatorio del encargo

### 1 · Resultado primario

**`SIN-GANADOR-UNICO`, sobre `U3 = 3` celdas del marco de 14.** Ningún
contendiente gana sus dos comparaciones pareadas bajo la banda `δ = 0.5 pp`
pre-registrada. **No** es `NO-ADJUDICABLE-POR-CONTROL`: los controles
salieron limpios. Lectura permitida, la única (P4, verbatim): *"El panel no
permite identificar un ganador único bajo la magnitud, incertidumbre y
cobertura pre-registradas."*

### 2 · Cifras y universo

`U0 = 14` · `UR = 14` · `U3 = 3` (`FAM-M-05`, `FAM-M-06`, `FAM-M-07`),
derivadas por la intersección congelada de `F5-contrato-triada-spec-v1_1.md`
§1.3 sin ampliar ni reducir `UR` y sin observar errores antes de fijarla.

| Contendiente | `MAE` (pp) | Ranking puntual |
|---|---:|:--:|
| `M` | 0.1758 | 1 |
| `L_SOLO` | 0.1990 | 2 |
| `L_CORPUS` | 0.3466 | 3 |

Ranking **descriptivo**, reportado por separado de la banda como manda §4:
las tres distancias caben dentro de `δ`.

### 3 · Cobertura

Sobre `UR = 14`: `M` 14/14 · `L_SOLO` 6/14 · `L_CORPUS` **3/14**. Réplicas
(de 112 por brazo): `L_SOLO` 33 `EXTRAIBLE` / 75 `NO-EXTRAIBLE` / 4
`AMBIGUA`; `L_CORPUS` 23 / 89 / 0. 224/224 capturas examinadas. Las
`NO-EXTRAIBLE`/`AMBIGUA` cuentan en cobertura; ninguna se sustituyó por cero.
Las 8 réplicas de una celda no se contaron como 8 tareas independientes.

### 4 · Pareadas

| Comparación | Δ (pp) | IC95 (pp) | Veredicto |
|---|---:|---|---|
| `Δ(L_CORPUS, L_SOLO)` | +0.1476 | `[−0.1000, +0.5000]` | `INCONCLUSO` |
| `Δ(M, L_SOLO)` | −0.0231 | `[−0.0694, +0.0694]` | `EMPATE-PRACTICO` |
| `Δ(M, L_CORPUS)` | −0.1708 | `[−0.4306, +0.0306]` | `EMPATE-PRACTICO` |

Mismo `U3` y **mismo vector de índices de bootstrap por réplica** para los
tres contendientes; `seed = 42` heredada, 10,000 réplicas, IC95.

### 5 · Secundaria

TRANSFERENCIA: **`SIN-UNIVERSO`**. Las 14 celdas de `UR` quedan
`M-NO-COMPARABLE-EN-TRANSFERENCIA` bajo el criterio mecánico de §6 (cita con
año ≥ ola de la celda, o sin año determinable, excluye). No veta ni
reemplaza la primaria.

### 6 · Límites

`U3 = 3/14` de **una sola familia** (ENIGH `recibe_remesas`) y **una sola
escala**; `L` se abstuvo en 11/14 celdas para `L_CORPUS` y 8/14 para
`L_SOLO` —dato de desempeño que el `MAE` no captura—; `M` en `U3` reproduce
la tasa base ENIGH 2022; `B` no es piso independiente (sus cifras sobre este
panel **son** el propio `R`). Ninguna salida autoriza causalidad, «todos los
mexicanos», «todos los LLM», modelo/versionado futuro, tarea fuera del
marco, ni que el corpus «explique» diferencia alguna. El `IC-HI` de la
primera pareada cae exactamente en `+0.5 pp` y el veredicto global es
**invariante** a esa frontera (`NC-0147`). Detalle completo en la nota de
veredicto §9.

### 7 · Contadores antes/después

| Contador | Antes (`origin/main = c439065`) | Después |
|---|---:|---:|
| ADR | 452 | **453** |
| Corridas derivadas en vivo (`corrida0 status`) | 138 | **139** |
| `RESULT` derivados en vivo | 2630 | **2889** (+259) |
| `corredores_envueltos_legacy` | 20 | **21** |
| `N_corridas_selladas` (vista TSV) | 34 | 34 — **no se movió**, ver `NC-0145` |
| `N_resultados_gen2_sellados` (vista TSV) | 1294 | 1294 — **no se movió**, ver `NC-0145` |
| `NC` abiertas | 82 | 84 (`−2` cerradas, `+4` abiertas) |
| Adopciones al motor | — | **cero**: este acto no adopta nada |

### 8 · Cascada

`ADR-453` (`canon/gobernanza-v1_15.md`) · `L0` recifrado
(`canon/estado-programa-v1_12.md`, con reparación del ancla duplicada
heredada, `NC-0148`) · rótulo `GEN2-F5-TRIADA-CALC` censado
(`canon/registro-rotulos.tsv`) · firma de contador con OBJETO
(`data/corrida0/decisiones.tsv`) · nota de veredicto
(`forense/notas/2026-09-10-GEN2-F5-TRIADA-CALC-veredicto.md`) ·
`python3 tools/cierre_acto.py --aplica` → `APLICADO: gobernanza 452→453 ·
tabla estado 452→453` · `python3 tests/check.py --baseline` → **VERDE**
(3 `FAIL` preexistentes: `T06`×2, `T08`; nada nuevo frente a
`tests/baseline.json`).

## NO-CORRIDO / RESERVAS

| qué (pieza citada del encargo) | por qué | impacto | sucesor |
|---|---|---|---|
| **`PERÍMETRO · «vistas corrida0 derivadas»`** — reescribir `data/corrida0/corridas.tsv` y `resultados.tsv` con la corrida sellada | `NO-VERIFICABLE-AQUÍ` | `registro --escribe` PARA (no existe `--force`) porque degradaría a `NO-VERIFICADO` el veredicto de replay de 29 corridas ajenas, entre ellas los 14 `CALC-R`. Medido: esta sesión es NUBE sin `data/raw` (`acceso_corpus.montado=NO`, `archivos_examinados=0`) y `verify CALC-R-FAM-M-05-v3` devuelve `NO-REPRODUCE · CONTEXTO-DISTINTO` con todos los `RESULT` en `hoy=None`, así que `--verifica` tampoco puede llenarlas. `N_corridas_selladas` (34) y `N_resultados_gen2_sellados` (1294) no se mueven en la vista; **ninguna cifra de este veredicto depende de esa escritura**. | `NC-0145` — acto de cascada en CAJA/Ubuntu con `data/raw` montada |
| **`P3 · «RESULTADO PRIMARIO: [GANADOR-TRIADA-…]»`** — coronar un ganador con cobertura suficiente | `DIFERIDO-A:` acto sucesor **bajo spec nueva** | `SIN-GANADOR-UNICO` sobre `U3 = 3/14`, una sola familia y una sola escala. Fuente dominante de incertidumbre medida y nombrada: **abstención de `L`** (11/14 sin punto de `L_CORPUS`, 8/14 sin `L_SOLO`), no varianza del árbitro ni del motor. **`F6 · COSECHA` NO procede.** | `NC-0146` — P5 del encargo, verbatim: *"estudiar la fuente dominante de incertidumbre o ampliar prospectivamente el marco bajo una spec nueva. No añadir celdas a este CALC."* |
| **`P2 · escala pareada de la spec TRIADA §4`** — resolver la escala cuando un límite del IC95 cae **exactamente** en `±δ` | `DECISIÓN-DE-MESA-PENDIENTE` | `Δ(L_CORPUS,L_SOLO)` selló `IC-HI = +0.5000000000000004 pp`; el valor exacto es `+0.5 pp` (residuo de coma flotante por calcular `|L−R|` dos veces con el mismo `R`). Sobre el número sellado la escala da `INCONCLUSO`; sobre el exacto daría `EMPATE-PRACTICO`. **Impacto nulo aquí, verificado:** el veredicto global es `SIN-GANADOR-UNICO` en ambos casos. Se reporta lo que el procedimiento sellado produjo, sin editarlo. | `NC-0147` — spec sucesora que declare tolerancia numérica en los límites de la banda |
| **`CASCADA · recifrado L0`** — impedir que se repita el ancla `L0` duplicada | `FUERA-DE-PERÍMETRO` | Defecto **heredado** de `ADR-452`, latente mientras `452 == 452` y detonado al subir a 453 (`APLICACION_ABORTADA · L0: 2 ancla(s)`, suite ROJO con dos `T15`). Reparado aquí sin reescribir prosa ajena: la anotación de `ADR-451` se restituyó verbatim en la cadena viva (612 anotaciones, orden 453-452-451-450-449) y la línea duplicada se borró sólo tras comprobar que su cola era byte-idéntica. Lo que no se corrió: **ningún test atrapa la duplicación**, así que puede repetirse; `tests/` no está en el perímetro. | `NC-0148` — acto de infraestructura con `tests/` en perímetro |

Todo lo demás que el encargo pidió **se corrió**: `P1` (espejo del contrato
por hash, 259 `RESULT` declarados antes de calcular, frase de cierre
verbatim), `P2` (`preflight → run → verify`, fila durable por celda, mismo
conjunto de celdas para los tres `MAE`, mismos índices de bootstrap), `P3`
(nota de veredicto en el orden pedido, con la tabla por celda, la secundaria,
`B` como diagnóstico y los límites), `P4` (lectura permitida, sin
extralimitaciones), `P5` (sucesor decidido por diagnóstico, no por
preferencia) y el perímetro, sin tocar ninguno de los inputs prohibidos.

## CONSUMIDO

Ejecutado por **[PR #681](https://github.com/Josanoforo/Modelado-Mexicano/pull/681)**
— `ACTO GEN2-F5-TRIADA-CALC · LLM SOLO vs LLM CON CORPUS vs MOTOR`, rama
`claude/calc-triada-gen2-adjudicacion-s40h3r`, base `origin/main = c439065`,
10/sep/2026, NUBE/Opus, cero microdato / cero red / cero llamadas nuevas a
ningún modelo.

**Compuerta 4/4 cumplida por producto** antes de cualquier edición
sustantiva (tabla de hashes arriba). **P1** congeló el espejo del contrato
en `COMMIT-1` (`data/corrida0/CALC-TRIADA-0001/spec.md` + `spec.yaml` con
248 inputs por hash y **los 259 `RESULT` declarados antes de calcular**, más
el medidor escrito y **no ejecutado**). **P2** corrió en `COMMIT-2`:
`preflight VERDE → run exit=0 → verify REPRODUCE` (`CONTEXTO=IDENTICO`,
sello `b5826272…`), con fila durable por celda para las 14 y el mismo
conjunto de celdas y los mismos índices de bootstrap para los tres
contendientes. **P3**:
`forense/notas/2026-09-10-GEN2-F5-TRIADA-CALC-veredicto.md`.

**`RESULTADO PRIMARIO: SIN-GANADOR-UNICO`, sobre `U3 = 3` celdas del marco
de 14.** `MAE` (pp): `M` 0.1758 < `L_SOLO` 0.1990 < `L_CORPUS` 0.3466 —
ranking puntual descriptivo, con las tres distancias dentro de `δ = 0.5 pp`.
Pareadas: `Δ(L_CORPUS,L_SOLO)` `INCONCLUSO`, `Δ(M,L_SOLO)` y
`Δ(M,L_CORPUS)` `EMPATE-PRACTICO`. Secundaria TRANSFERENCIA `SIN-UNIVERSO`.
`B` sólo diagnóstico: sus únicas cifras sobre este panel **son** el propio
`R`. Controles limpios (224/224 identidad, 0 discordancias de
re-derivación, 0 contaminadas) — por eso no es
`NO-ADJUDICABLE-POR-CONTROL`: lo que falta es cobertura.

Cascada: `ADR-453` (`canon/gobernanza-v1_15.md`), `L0`
(`canon/estado-programa-v1_12.md`, con la reparación del ancla duplicada
heredada de `ADR-452`, `NC-0148`), rótulo `GEN2-F5-TRIADA-CALC` censado
(`canon/registro-rotulos.tsv`), firma de contador con OBJETO
(`data/corrida0/decisiones.tsv`). `NC-0143` y `NC-0144` **CIERRAN** (la
segunda por hallazgo, no por ejecución); abren `NC-0145`, `NC-0146`,
`NC-0147` y `NC-0148`. `python3 tests/check.py --baseline` **VERDE**
(3 `FAIL` preexistentes: `T06`×2, `T08`).

**Sucesor:** **`F6 · COSECHA` NO procede** — exige ganador único con
cobertura suficiente, y no hay ninguna de las dos cosas. Por `P5`, y por
diagnóstico y no por preferencia: la fuente dominante de incertidumbre es la
**abstención de `L`** (11/14 celdas de `UR` sin punto de `L_CORPUS`, 8/14
sin `L_SOLO`), y el sucesor la estudia o amplía prospectivamente el marco
**bajo una spec nueva** — sin añadir celdas a este CALC (`NC-0146`).
