Contadores movidos: 0.

# Encargo Q · Multinivel de P3 — sesión CONTAMINADA a medio acto, se declara y se para

**Estado del entregable: PARO, no HECHO.** Esta sesión confirma el análisis de §1 del encargo (la trampa POST-DATO/§2.5 existe, con cita), pero **no produce** el pre-registro autónomo del §2.2 porque **ella misma se contaminó** contra resultados de P3 a mitad del acto, por un error propio, no por contexto heredado. Se declara en vez de disimularse, que es la propiedad que el encargo pide proteger.

## 0 · Qué se leyó, lista completa, en el orden en que se leyó

| # | Archivo / comando | Qué se tomó de él | ¿Permitido por §0 del encargo? |
|---|---|---|---|
| 1 | `git status`, `git log -1`, `git branch -a`, `git fetch origin main`, `git log origin/main -1` | Estado de repo y verificación de HEAD contra `origin/main` (`f5f3b85`, sin discrepancia) | Sí — entorno, §0 del acto |
| 2 | `Glob forense/p3-lca-preregistro-v1_0.md` | Confirmar que el archivo existe | Sí |
| 3 | `forense/p3-lca-preregistro-v1_0.md`, **completo** (líneas 1–439) | El protocolo entero: hipótesis (§1), indicadores (§2), §2.5 completa, selección de `k` (§3), anti-forced-choice (§4), diseño muestral (§5), tabla de decisión (§6), límites (§7), auditoría (§8), instrucciones de ejecución (§9), §10 (enmiendas, ninguna a la fecha del sello) | Sí — explícitamente autorizado, "es el protocolo, no el resultado" |
| 4 | `Grep "ADR-53" canon/gobernanza-v1_15.md`, luego `Read` líneas 520–589 | **Se pidió únicamente "el hecho de gobierno de que habilitó la extensión multinivel sin correrla".** El `Read` de rango amplio trajo el ADR-53 **completo**, incluidos sus párrafos (A) y (B): el veredicto D5 (INESTABLE) de P3, el descarte razonado de D6, y **cifras del resultado** — BIC decreciente monótono 1–8 con mínimo en el borde k=8, el mínimo interior de S1 en k=4 (BIC=962 340.94), las diferencias sucesivas de BIC entre `k` consecutivos, `k_primario=3` de S1 tras la regla de no-separación, su replicación (1 de 50 arranques), y el rango total de BIC observado (7 929.85) | **No** — esto es exactamente "el detalle numérico de ADR-53 (curvas de BIC, valores de `k`, diagnósticos de estabilidad)" que el §0 del encargo prohíbe nombrando esos mismos términos |
| 5 | `Bash: tail forense/hallazgos.md`, `ls forense/notas`, `head tests/bitacora.py` | Formato de entradas de hallazgos, convención de nombre de nota, cabecera del script de bitácora — ningún contenido de P3 | Sí |
| 6 | `python3 tests/bitacora.py --abre` | Estado de suite (VERDE) y del repo | Sí — exigido por §0 del acto |

**Lo que NO se abrió:** ENIGH ni ningún microdato; `forense/notas/2026-08-04-p3-lca-segmentacion.md`; `canon/estado-programa-v1_9.md` §L5·P3; `forense/notas/_p3_lca/*.json`. Esa parte de la condición de sesión limpia se sostuvo íntegra.

**Lo que sí se rompió:** la condición de no leer "el detalle numérico de ADR-53", por un `Read` de rango demasiado amplio (520–589 en vez de acotar a la primera oración del ADR, que era lo único autorizado). Es un error de ejecución de esta sesión, no un defecto del encargo ni contaminación heredada.

## 1 · §2.1 — el análisis de la trampa, hecho ANTES de la contaminación, con cita literal

Esta parte se completó leyendo únicamente `p3-lca-preregistro-v1_0.md` (ítem 3 de la tabla), antes del `Grep`/`Read` de ADR-53 que contaminó la sesión. Se reporta porque no depende de ningún resultado de P3 — es análisis puramente textual del propio protocolo.

**§2.5, último párrafo, cita literal:**

> "Lo que este pre-registro NO adopta, y por qué se dice: el tratamiento técnicamente correcto de una malla mixta es un LCA multinivel (clases de persona anidadas en clases de hogar). Se declara como la extensión correcta y no se pre-registra como análisis primario [...] Queda pre-registrada como condicional: se corre si y sólo si S1 muestra que los ejes de hogar dominan la solución (§6·D5·nota). **Si se corre, es un análisis nuevo y necesita su propia enmienda fechada (§10).**"

**§10, cita literal:**

> "Regla de enmienda, que es la propiedad entera de un pre-registro: cualquier cambio posterior al protocolo —umbrales, indicadores, rango de `k`, regla de decisión, tabla de §6.1, criterios de §6.0— se anexa aquí como enmienda fechada y firmada [...] **Una enmienda posterior al primer ajuste se marca además como POST-DATO y todo veredicto que dependa de ella se reporta como exploratorio, no como pre-registrado.**"

**Confirmación del análisis de §1 del encargo.** El único camino que §2.5 nombra para pre-registrar el multinivel es una enmienda fechada al §10 de este mismo documento. La condición para siquiera saber que ese camino está habilitado — que S1 muestre que los ejes de hogar dominan — solo puede conocerse **después** de correr el ajuste primario de P3 (S1 es una de las sensibilidades del ajuste, §2.5·c). Por tanto cualquier enmienda que registre "el multinivel se pre-registra" llega necesariamente **después del primer ajuste**, y §10 la marca **POST-DATO** por su propia letra, con el efecto declarado de que "todo veredicto que dependa de ella se reporta como exploratorio, no como pre-registrado". El único camino que el protocolo nombra es el que el mismo protocolo invalida. `grep -rn "POST-DATO" canon/ forense/` (no re-corrido en esta sesión, pero citado del encargo) sostiene que la regla no tiene ninguna excepción escrita para el caso condicional de §2.5.

**El análisis se confirma, no se refuta.** No se encontró una lectura de §10 donde una extensión condicional pre-registrada desde el sello escape la marca POST-DATO: §10 habla de "cambio posterior al protocolo" en general, sin distinguir entre una enmienda que altera el cuerpo (umbrales, indicadores) y una que solo activa una rama ya prevista en el cuerpo (§2.5). El texto no trae esa distinción — se tendría que inventar para salvar el camino de §2.5, y este pre-registro (§8·Q6, sobre sí mismo por extensión) es explícito en que nada se pre-registra por interpretación conveniente después del hecho.

## 2 · Por qué no sigue el acto a §2.2

El §2.2 del encargo pide un pre-registro autónomo para el LCA multinivel, "escrito antes de ver dato alguno". Esta sesión ya vio, vía el error del ítem 4 de §0 arriba, el veredicto D5 de P3, el descarte de D6 con su curva de BIC, y — más grave para el propósito específico del multinivel — **el resultado exacto de S1** (la sensibilidad que compara el ajuste con y sin los ejes de hogar, el mismo mecanismo que el multinivel viene a tratar mejor): que el BIC de S1 toca fondo en k=4, con una solución primaria en k=3 que replica solo 1 de 50 arranques.

Escribir hoy, desde esta sesión, el pre-registro autónomo del multinivel —en particular su regla de decisión y qué contaría como "el agrupamiento era por hogar" (§2.2, penúltimo punto del encargo)— se redactaría con ese número ya en la cabeza. Es precisamente la propiedad que el encargo existe para proteger, dicha en su propio §0: **"un protocolo escrito por quien ya vio el resultado no vale"**. No importa que la contaminación sea sobre P3 (nivel único) y no sobre el multinivel mismo (que no ha corrido): S1 es la sensibilidad que decide si el multinivel se habilita en absoluto (ADR-53·C, "S1 lo mostró"), y su cifra exacta es información directa sobre la superficie del problema que el pre-registro nuevo tendría que anticipar en blanco.

## 3 · Lo que esta sesión NO hace, en consecuencia

- No escribe `forense/p3-multinivel-preregistro-v1_0.md`.
- No escribe la enmienda de enrutamiento en `p3-lca-preregistro-v1_0.md` §10 (§2.3 del encargo) — no hay archivo nuevo al que apuntar.
- No toca el cuerpo sellado de `p3-lca-preregistro-v1_0.md`.
- No abrió ENIGH, `2026-08-04-p3-lca-segmentacion.md`, `estado-programa-v1_9.md` §L5·P3 ni `_p3_lca/*.json`.

## 4 · Traspaso

Otra sesión, verdaderamente limpia frente a P3 y al multinivel — que no abra ADR-53 más allá de su primera oración de gobierno — toma el §2.2 y el §2.3 del encargo. El §2.1 (este documento, sección 1 arriba) queda hecho y no necesita repetirse: la cita literal de §2.5 y §10 y la confirmación de la trampa no dependen de ningún resultado y se sostienen contra archivo.

## 5 · Suite

`python3 tests/bitacora.py --abre`: línea base VERDE (`check.py --baseline` exit=0, sin nuevo rojo frente a `tests/baseline.json`); `validador_registro_ids.py` OK, 49/49 IDs verificados. Sin cambios de código en este acto — no hay superficie que pudiera haber roto la suite.
