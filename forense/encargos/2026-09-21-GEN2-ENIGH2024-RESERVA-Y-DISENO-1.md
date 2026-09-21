# ENCARGO · ACTO GEN2-ENIGH2024-RESERVA-Y-DISENO-1 · ENIGH 2024 ENTRA AL CORPUS RESERVADA, Y QUEDA ESCRITO —ANTES DE QUE NADIE LA ABRA— QUÉ SE VA A PREDECIR DE ELLA, CON QUÉ CONTENDIENTES Y QUÉ LO REFUTARÍA

> ENTORNO: **NUBE, entorno `milpa-inegi`** (egreso a INEGI permitido; se reconoce por la sonda de red, no por la variable). Lee documentos —cuestionario, descriptor, nota metodológica—, **nunca microdato ni tabulados de 2024**. Si la sonda sale DENEGADA: haz P0, P1 y P3 con lo que hay en el repo, deja P2 con NC y dilo. NO es CAJA.
> **Trampa conocida:** si un payload cae en `data/raw`, `ENTORNO-DERIVADO` se voltea solo a CAJA; no es PARO ni cambio de entorno.

CABECERA · SHA de redacción `55c8d57c`; re-deriva al abrir · una sola sesión, rama `acto/gen2-enigh2024-reserva-y-diseno-1` · MODELO: Opus · MODO: **ABIERTO**; nada se congela aquí · CONTADOR: ninguno · FP/ADR/NC: raíz de acto.
**Si al fusionar `main` choca la línea L0 de `canon/estado-programa-v1_14.md`: NO conserves los dos lados; toma la de `main` y re-inserta solo tu anotación** (27 MB por duplicaciones; TUBERÍA la repara). Si `canon/L0/` ya existe al cerrar, tu anotación va ahí.

## 1 · OBJETIVO
ENIGH 2024 está en la cola de descarga y va a entrar al corpus en horas. Es una ola que nadie del programa ha abierto, de una encuesta con seis olas de historia en el manifiesto (2012–2022): es la tercera oportunidad de prueba prospectiva, después de ENVIPE 2026 y del lote ENIF 2024, y la única del dominio hogar-ingreso-cuidado. Una ola se vuelve inservible como prueba en el momento en que alguien la abre «para ver»: por eso la reserva se asienta **antes** de que el payload llegue, y el diseño se escribe antes de que exista tentación.
«Hecho» significa: la reserva asentada · inventario de qué estimandos de ENIGH tienen serie sellada en GEN2 y cuáles no · comparabilidad por texto 2022→2024 de esos estimandos · un diseño para firma de mesa, con la forma del duelo ENVIPE 2026.

## 2 · FIRMAS DE MESA — verbatim
Precedente (21/sep): «ENVIPE 2026 queda RESERVADA desde hoy, entera: nacional, marginales por eje y cruces. Bajar el payload está permitido; abrirlo, derivar de él o leer sus tabulados, no, fuera del código que se congele para ello. Rige E.6.»
**Propuesta de dirección — el lanzamiento es el sello:** «ENIGH 2024 queda RESERVADA desde hoy, entera, en los mismos términos que ENVIPE 2026. Y como regla: toda ola nueva de una encuesta con historia en el corpus nace RESERVADA al entrar al manifiesto; la levanta solo el código congelado de una prueba pre-registrada, o mesa por escrito.»

## 3 · LO QUE DIRECCIÓN SABE (contra `55c8d57c`)
- `[EJECUTADO sobre el manifiesto]` `enigh2012_nc_csv` … `enigh2022_nc_csv` (seis olas), `enigh2022_descripcion_base_pdf`, `enigh2022_nota_tecnica_pdf`. ENIGH 2024: 0 entradas; fila `residual:ENIGH_2024_NC` en la cola, prioridad 2 `[LEÍDO: nota de #960]`.
- `[EXISTE]` sellados que leen ENIGH: `CALC-B-0001` (línea base temporal; sus inputs son ENIGH 2016, 2018, 2020 y 2022 `[LEÍDO: forense/replay-evidencia.tsv:29]`), `CALC-B-MARCO-ENIGH-0001`, `CALC-ENIGH-0001`, `CALC-ENIGH2022-PERFIL-ESTRUCTURAL-0001…0003`, `CALC-ENIGH2022-INTENSIDAD-REMESAS-0001`, `CALC-ENIGH2022-REMESAS-CONTEXTO-0001`. `[SUPUESTO]` que alguno trae el mismo estimando medido en ≥ 3 olas: es lo que P1 averigua.
- `[LEÍDO]` el molde: `forense/prereg-caja/DISENO-duelo-prospectivo-ENVIPE2026-v1_0.md` y su enmienda, si ya están archivados (los archiva el acto del duelo, en vuelo); si no, el texto de la firma F7 en `FP-260921-GEN2-TRAMITE-FIRMAS-4-8a1f-07`. Lecciones ya firmadas: a nivel nacional el punto nuevo no adjudica solo y se acompaña de validación de origen móvil; todas las variantes de tendencia entran juntas; a nivel cruce, la regla es la diferencia de error medio con IC (lote ENIF v0.3).
- `[LEÍDO: nota de cierre del piloto 3]` la interacción cruda erró 10.6 pp, la encogida 1.9, el piso 3.4: el contendiente de cruces que importa es el encogido.

## 4 · YA HECHO
Por objeto («ENIGH 2024», «ENIGH2024», «reserva») en encargos, `decisiones.tsv`, firmas y ramas: la fila de cola existe; no hay reserva ni diseño. **Repítela tú.**

## 5 · PIEZAS
**P0 · Reserva.** Asienta la firma de §2 (A.12) y pon la regla de reserva en la fila de cola de ENIGH 2024, como la tiene la de ENVIPE 2026. Semilla `PARA-v2.16` con la regla general.
**P1 · Inventario.** Por cada estimando sellado que lea ENIGH: qué mide, unidad (hogar / persona / peso), universo, ponderador, en qué olas está sellado y con qué `RESULT`. Regla de entrada del duelo: R sellado en ≥ 3 olas con universo idéntico. Lo que no la cumpla: qué acto de caja haría falta para que la cumpla (medir olas abiertas: no gasta nada).
**P2 · Comparabilidad 2022→2024 por texto**, de lo que pase P1: cuestionario y descriptor de 2024 bajados de INEGI y registrados en el manifiesto; forma de `data/credito-comparabilidad-texto-v1_0.tsv`. ENIGH cambió de serie en 2016 («nueva serie»): dilo donde toque.
**P3 · Diseño para firma.** Primera línea: universo, unidad, escala. Contendientes mecánicos declarados juntos (persistencia, tendencias de 2, 3 y serie completa en la escala que corresponda al estimando —logit para proporciones, log para montos—, C2 y la familia encogida en cruces, sobre pares cuya historia ya esté abierta). Regla de adjudicación por nivel. B-bis completo. Qué NO prueba. Fecha límite propuesta para el COMMIT-2 y por qué.

## 6 · LATITUD
Decides tú: forma, orden, herramientas. Si P1 muestra que ningún estimando cumple la regla de entrada, el diseño dice eso y propone el acto de caja que construye la serie primero: **ése es un entregable válido.**

## 7 · PAROS — lista cerrada
a) bajar, abrir o listar microdato de ENIGH 2024, o leer sus tabulados, comunicados o presentaciones de resultados · b) lo mismo con ENVIPE 2026 · c) declarar algo congelado · d) editar un sello.

## 8 · COMPUERTAS
Ninguna.

## 9 · PERÍMETRO
Propio: fila de firma y fila de cola · entradas de manifiesto de los documentos de 2024 · tabla de comparabilidad de ENIGH y su test · el diseño en `forense/prereg-caja/` · semilla · nota · cascada. Ajeno: todo CALC · `milpa/` · celdas-D. Si te encuentras escribiendo fuera de esta lista, PARA.

## 10 · NO HACE · SUCESORES · AUDITORÍA · CIERRE
No mide · no congela. Sucesor: COMMIT-1 del duelo ENIGH 2024, en caja, con el módulo genérico que deja el duelo ENVIPE. Auditoría (el diseño afirma sobre México): ingreso, gasto y remesas son estructura económica antes que conducta: el diseño dice, por estimando, qué parte es decisión del hogar y qué parte es precio, empleo o transferencia pública; ENIGH sub-capta el ingreso alto y las remesas informales: se declara; unidad hogar, no persona: no se cruza contra ENIF o ENVIPE sin enlace. `## NO-CORRIDO / RESERVAS` · `## CONSUMIDO`.

## NO-CORRIDO / RESERVAS

**P2 · Comparabilidad 2022→2024 por texto** — `NC-260921-GEN2-ENIGH2024-RESERVA-Y-DISENO-1-b7ae-01`

- **Qué** (verbatim del encargo §5): «**P2 · Comparabilidad 2022→2024 por texto**, de lo que pase P1: cuestionario y descriptor de 2024 bajados de INEGI y registrados en el manifiesto; forma de `data/credito-comparabilidad-texto-v1_0.tsv`. ENIGH cambió de serie en 2016 («nueva serie»): dilo donde toque.» **Corrido en parte:** la última frase SÍ se cumplió — el corte de serie de 2016 está dicho donde toca (diseño §2.3, `L0`, gobernanza, esta nota), derivado del metadato sellado `identifier=MEX-INEGI.40.202.03-ENIGH-2014-NCV` y del salto de `n` 19 479 → 70 311, no de memoria. **No corrido:** todo lo que exige red — cero documentos de 2024 bajados, cero entradas de manifiesto creadas, cero filas escritas en la tabla de comparabilidad.
- **Por qué:** `PARO-ENTORNO` — el encargo asigna NUBE `milpa-inegi` y dice que el entorno «se reconoce por la sonda de red, no por la variable». La sonda salió **DENEGADA** (`http_code=000`, `http_connect=403`, `via_proxy=SI`), confirmada en **2 intentos** contra la URL real del cuestionario 2024 (`curl: (56) CONNECT tunnel failed, response 403`). A.5: **NO OBTENIDO POR ESTE AGENTE EN 2 INTENTOS**; no se concluye nada sobre el portal de INEGI. El propio encargo previó esta rama y la ordenó: «Si la sonda sale DENEGADA: haz P0, P1 y P3 con lo que hay en el repo, deja P2 con NC y dilo». **No fue PARO del acto**: P0, P1 y P3 se entregaron completos.
- **Impacto:** **ningún contador se mueve por esto** — este acto no sella corrida (`cuenta_gen2 = NO`). La firma del diseño (P3) **no queda gateada**: la comparabilidad por texto no gatea la firma de mesa, gatea el **COMMIT-1**. El riesgo concreto que queda abierto, dicho sin suavizar: si el cuestionario de 2024 movió la pregunta de remesas dentro del concentrado, el punto de 2024 no sería comparable con la serie 2016–2022 y el duelo mediría otra cosa. Ese riesgo **se cierra antes del COMMIT-1, no después**, y el diseño lo declara como dependencia.
- **Sucesor:** acto en entorno con egreso a INEGI **verificado por sonda** (`milpa-inegi` o caja), consumiendo la forma ya existente de `data/credito-comparabilidad-texto-v1_0.tsv`; **`SIN-ASIGNAR`** de dueño. Debe correr **antes** del COMMIT-1 del duelo ENIGH 2024.

**Ninguna otra pieza quedó sin correr.** P0 (reserva), P1 (inventario) y P3 (diseño para firma) se entregaron completos. Nada de lo que este acto sí hizo quedó parcial ni sustituido.

## CONSUMIDO

Ejecutado por **ACTO GEN2-ENIGH2024-RESERVA-Y-DISENO-1**, rama `acto/gen2-enigh2024-reserva-y-diseno-1`, **PR #964** (https://github.com/Josanoforo/Modelado-Mexicano/pull/964), `ADR-260921-GEN2-ENIGH2024-RESERVA-Y-DISENO-1-b7ae-01`. 0-bis en `b7ae01e`, sello de cuerpo `e165564d6a03e743` (no regenerado en el cierre).

P0, P1 y P3 completos; P2 en `## NO-CORRIDO / RESERVAS` arriba. Cierre: `forense/notas/2026-09-21-GEN2-ENIGH2024-RESERVA-Y-DISENO-1-cierre.md`.
