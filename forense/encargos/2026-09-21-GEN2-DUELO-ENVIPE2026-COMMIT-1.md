# ENCARGO · ACTO GEN2-DUELO-ENVIPE2026-COMMIT-1 · EL DUELO PROSPECTIVO NACIONAL QUEDA CONSTRUIDO, ENSAYADO DE PUNTA A PUNTA SOBRE OLAS ABIERTAS Y CONGELADO — SIN TOCAR ENVIPE 2026

> ENTORNO: **CAJA** (corpus montado: necesita ENVIPE 2018-2025). El hook imprime ENTORNO-DERIVADO; si no dice CAJA, PARA en una línea. `data/raw` ausente en worktree nuevo: se enlaza, no es PARO. NO es NUBE.

CABECERA · SHA de redacción `55c8d57c`; re-deriva al abrir · una sola sesión, rama `acto/gen2-duelo-envipe2026-commit-1` · MODELO: Opus · MODO: **ABIERTO** mientras construyes; lo que declares congelado queda RÍGIDO para quien ejecute · **F3:** quien congela aquí NO ejecuta el COMMIT-2/3 · CONTADOR: no sella corridas de 2026; los ensayos sobre olas abiertas que selles cuentan según su spec; `adoptados_activos` no se mueve · FP/ADR/NC: raíz de acto.
**Si al fusionar `main` choca la línea L0 de `canon/estado-programa-v1_14.md`: NO conserves los dos lados; toma la de `main` y re-inserta solo tu anotación** (27 MB por duplicaciones; TUBERÍA la repara). Si `canon/L0/` ya existe al cerrar, tu anotación va ahí.

## 1 · OBJETIVO
El duelo de tres que tiene el programa (motor, LLM solo, LLM con corpus) es retrospectivo para sus tres contendientes: por eso empata y no prueba nada. ENVIPE 2026 es la única ola anual que nadie del programa ha abierto. Este acto deja listo —y probado con el validador que sella— el procedimiento que la abrirá **una vez**, con todos los contendientes mecánicos declarados juntos. Fecha límite del COMMIT-2: 31/oct/2026; lo que se degrada con el tiempo es la ceguera. Además, su módulo de cruces es la **implementación de referencia** que el lote ENIF 2024 reutilizará: escríbelo genérico sobre (instrumento, par).
«Hecho» significa: diseño y enmienda archivados · spec humana con sidecar · CALC de emisiones encadenado a CALC de adjudicación, con su COMMIT-3a previsto en el propio `spec.yaml` · «congelado» según D-22 ampliada, **demostrado** · la validación de origen móvil corrida y reportada · nota de una página.

## 2 · FIRMAS DE MESA — verbatim
Reserva (21/sep): «ENVIPE 2026 queda RESERVADA desde hoy, entera: nacional, marginales por eje y cruces. Bajar el payload está permitido; abrirlo, derivar de él o leer sus tabulados, no, fuera del código que se congele para ello. Rige E.6.»
Diseño con tres enmiendas (21/sep; en el repo como `FP-260921-GEN2-TRAMITE-FIRMAS-4-8a1f-07` `[EJECUTADO: grep]`): «(A) A nivel nacional hay una o dos celdas por ola: el punto de 2026 **no adjudica solo**. El COMMIT-1 corre, como ensayo de punta a punta, la validación de origen móvil de K, T3, T5 y TC sobre la serie sellada (cada ola predicha solo con las anteriores), rotulada RETROSPECTIVA-MECÁNICA; el veredicto nacional se lee con las dos cosas a la vista. (B) A nivel cruce entra la misma familia del lote ENIF —C2, persistencia, interacción cruda, interacción encogida, ajuste proporcional— sobre los dos pares cuyo cruce de 2025 ya está abierto (`escolaridad × dominio`, piloto 2; `edad × dominio`, consumido sin piloto, NC-0328), para que esta ola pueda informar la regla de salida de θ; los 4 cruces reservados de ENVIPE 2025 no se tocan. (C) "Congelado" es D-22 ampliada. Fecha límite del COMMIT-2: 31/oct/2026. Dueño: dirección.»
D-22 ampliada (21/sep, `…-8a1f-05`): «Congelado exige: `preflight` VERDE sobre el commit final con main fusionado; que `_valida_outputs` acepte la salida de cada rama terminal del procedimiento, incluida la de celda rara, sobre sintético y sobre oro; que todo id que el código pueda emitir nulo por lectura estática esté declarado; y ningún input con hash sobre un archivo vivo.»
**Propuesta de dirección — el lanzamiento es el sello:** «La adjudicación a nivel cruce usa la regla del lote ENIF v0.3: diferencia de error medio entre C2 y la interacción encogida sobre las celdas puntuadas, con IC95 por réplica; vence si despeja 0.5 pp; propuesta con reserva si despeja 0 y no 0.5; nadie vence si incluye 0. `cuenta_gen2 = SI` para las corridas del duelo, sea cual sea el veredicto.»

## 3 · LO QUE DIRECCIÓN SABE (contra `55c8d57c`, sin corpus)
- `[EJECUTADO]` `data/corrida0/envipe-serie-denuncia-v1_0.tsv`: 15 olas, columnas `anio_hecho · ola_encuesta · p_c1_u1 · ic95_boot_lo/hi · n_u1 · unidad · ponderador · reactivo · formato · comparabilidad · calc_id · result_id_punto`. Es el estimando **delito no denunciado**.
- `[EXISTE]` `CALC-ENVIPE-SERIE-2011…2022`, `CALC-ENVIPE-U4-2012/2013/2015`, `CALC-EVASION-NORMA-0001-v1_1`, `CALC-TRA-EVADE-NORMA-SXD-EMISIONES-0001` y `…-ARBITRO-CRUCE-0001` (piloto 2), `CALC-PISOS-ENVIPE2024-EJES-0002`, `CALC-C2-COMPUESTO-IC-ENVIPE2025-0001`; specs en `forense/prereg-caja/` (`TRA-evade-norma-sxd12-spec-v1_0.md`, `ENVIPE-SERIE-COMPLETA-spec-v1_0.md`, `PISOS-ENVIPE2024-ejes-spec-v2_0.md`); medidores en `tools/medidor_envipe_serie_completa.py`, `tools/medidor_evasion_norma_envipe25.py`. **Reutiliza; no reescribas lo que ya mide bien.**
- `[EJECUTADO]` manifiesto: `envipe2018_csv` … `envipe2025_csv` presentes. **`envipe2026_csv` NO está todavía**: está en la cola de adquisición (prioridad 1) y lo baja el agente en caja. → P0.
- `[REPORTADO por MOTOR, EJECUTADO allá]` para `evade_norma` la constante del motor (`milpa/tramite.yaml`, 0.562774) y el nacional sellado de la ola 2025 son el mismo número: K es **un** contendiente, no dos. Para `evade_norma` hay 3 puntos nacionales sellados: T5 y TC son `NO-CONSTRUIBLE` y así se asientan. La ola 2011 trae `comparabilidad = INSTRUMENTACION-NOMINAL-Y-RESIDUALES`. Compruébalo por comando.
- `[EXISTE]` celda-D del piloto 2: `data/curacion-registro/celdas-d/TRA.evade_norma.envipe2025.escolaridad_x_dominio.yaml`. `[LEÍDO: instrucciones HISTORIA, E.6]` el cruce `edad × dominio` de ENVIPE 2025 quedó `CONSUMIDA-SIN-PILOTO` (NC-0328). Son los dos pares del nivel cruce. Re-verifica el estado de ambos (A.17).
- `[LEÍDO: nota de cierre del piloto 3]` lo que costó aprender: `preflight` relativo al CALC, sha de inputs, `dependencias_materiales`, nulos por réplica vacía (`medidor.py:290-291` de ese piloto), puntos sin guardia de finitud. Tu ensayo cubre las dos cosas: `None` **y** `NaN`.

## 4 · YA HECHO
Por objeto («ENVIPE2026», «duelo prospectivo», «origen móvil», «rolling») en encargos, `prereg-caja`, `data/corrida0/` y ramas remotas (1 viva, de TUBERÍA): existe la reserva firmada y la fila de cola; no hay spec, CALC ni rama del duelo. **Repítela tú.**

## 5 · PIEZAS
**P0 · Archivo y payload.** Extrae el Anexo A a `forense/prereg-caja/DISENO-duelo-prospectivo-ENVIPE2026-v1_0.md` (el contenido entre marcadores debe dar sha256 `e88d3192268167a37e5c96e75a8c73421eb1926a9f621e46da29a10ce2dabca3`) y su `…-enmienda-v1_1.md` con F7 verbatim. ¿Está `envipe2026_csv` en el manifiesto con sha? Si no: **no es PARO** — construye y ensaya todo, NO declares congelado (el `spec.yaml` no puede fijar un input sin sha), y deja NC con sucesor «congelar cuando el payload entre». Jamás lo bajes tú a mano ni lo abras.
**P1 · Spec humana.** Primera línea: universo, unidad (DELITO, `FAC_DEL`) y escala. Qué estimandos entran, por la regla del diseño (R sellado en ≥ 3 olas y universo idéntico). Los contendientes nacionales K, T3, T5, TC y E+ en logit, con fórmula cerrada, **todas las variantes a la vez**. El nivel cruce de F7(B) con la regla de §2. Regla del LLM del diseño §3. B-bis del diseño §6, íntegro. Lo que NO significa.
**P2 · Código y contrato.** Emisiones → adjudicación, con guardia de **una sola variable de agrupación** sobre 2026 en emisiones. Módulo de cruces genérico sobre (instrumento, par), sin nada de ENVIPE cableado dentro. Códigos y ponderadores desde el descriptor, no adivinados (E.5).
**P3 · Ensayo de punta a punta sobre lo abierto (E.5: declarado en la spec antes de correrlo).** (i) Con `corrida0 run`, el procedimiento corrido «como si 2025 fuera la ola nueva» reproduce lo sellado —nacional `G-M25-P-NACIONAL`, marginales y C2 del piloto 2— dentro de la tolerancia del tipo. (ii) Validación de origen móvil de K, T3, T5, TC sobre la serie sellada: cada ola predicha solo con las anteriores; error por contendiente y por ola; rotulada RETROSPECTIVA-MECÁNICA; **no selecciona variante**. (iii) Ensayo de sellabilidad: `_valida_outputs` sin problemas en cada rama terminal, celda rara incluida, cero no finitos.
**P4 · Congelar, o decir por qué no.** Los cuatro requisitos de D-22 ampliada, con salida cruda. Nota para mesa: qué quedó congelado, qué dijo el origen móvil, qué falta para el COMMIT-2.

## 6 · LATITUD
Decides tú: cuántos CALC, nombres, qué medidores existentes reutilizas, cómo representas E+ por variante. Replantea y sigue ante main movido, ids renombrados o un sello viejo con contexto distinto (decláralo). Una pieza que no sale no tumba las otras. Pregunta a mesa, siguiendo con lo demás: si un estimando que el diseño daba por entrante no cumple la regla de entrada.

## 7 · PAROS — lista cerrada
a) abrir, listar, descomprimir o derivar de `envipe2026*`, o leer tabulados o comunicados con cifras de ENVIPE 2026 · b) abrir alguno de los 4 cruces reservados de ENVIPE 2025 · c) elegir, quitar o reajustar una variante de tendencia después de ver el origen móvil · d) declarar congelado sin los cuatro requisitos · e) editar un sello o una spec sellada · f) entorno equivocado.

## 8 · COMPUERTAS
«P3 completo en verde» protege: **congelar spec**. Ninguna más.

## 9 · PERÍMETRO
Propio: diseño y enmienda · spec y sidecar del duelo · los CALC nuevos del duelo y sus ensayos · el módulo genérico de cruces (archivo nuevo en `tools/`) y sus tests, cableados en CI · nota · cascada. Ajeno: todo CALC existente · `milpa/` · celdas-D · marcador (lo re-deriva quien ejecute). Si te encuentras escribiendo fuera de esta lista, PARA.

## 10 · NO HACE · SUCESORES · AUDITORÍA · CIERRE
No abre 2026 · no corre LLM · no adjudica. Sucesores: COMMIT-2/3a/3 en otra sesión, antes del 31/oct · COMMIT-1 del lote ENIF reutiliza el módulo de cruces. Auditoría (la spec afirma sobre México): denunciar o no responde a confianza institucional, costo del trámite y tipo de delito —estructura e instituciones— antes que a disposición; unidad delito: no se lee como «proporción de personas»; el promedio nacional esconde dónde se concentra el error, por eso el desglose por eje es obligatorio antes de cualquier frase de producto; si todos los contendientes yerran en el mismo sentido, es cambio de nivel del instrumento o del mundo, no veredicto. `## NO-CORRIDO / RESERVAS` · `## CONSUMIDO`.

---
## ANEXO A · diseño v1.0 de MOTOR, verbatim · sha256 `e88d3192268167a37e5c96e75a8c73421eb1926a9f621e46da29a10ce2dabca3` · el contenido es lo que está ENTRE las dos líneas marcadoras
<<<ANEXO-A-INICIO>>>
# DISEÑO · DUELO PROSPECTIVO NACIONAL · ENVIPE 2026
**Dirección MOTOR · 21/sep/2026 · contra `main = d4494952` · propuesta, NO ejecutada**

> **Primera línea, como pide mesa: UNIVERSO, UNIDAD, ESCALA.**
> Unidad de análisis: **DELITO**, no persona. Ponderador `FAC_DEL`. Universo por estimando,
> declarado abajo pieza por pieza. Escala de emisión: proporción en [0,1]; todo error se
> reporta en **puntos porcentuales (pp)**; toda combinación de niveles se hace en **logit** y
> se devuelve a proporción antes de comparar. Ninguna cantidad de unidad DELITO se compara
> contra ninguna de unidad PERSONA sin función de enlace declarada; en este duelo no hay
> ninguna, así que **no se mezclan**.

## 0 · Estado de la reserva y exposición

FIRMA DE MESA, verbatim, 21/sep/2026: «ENVIPE 2026 queda RESERVADA desde hoy, entera:
nacional, marginales por eje y cruces. Bajar el payload está permitido; abrirlo, derivar de él
o leer sus tabulados, no, fuera del código que se congele para ello. Rige E.6.»

Exposición declarada, categoría nunca contenido:
- **Dirección**: cifras titulares NACIONALES de denuncia, del comunicado de prensa. No
  marginales, no cruces, no el estimando por delito con universo BP1_20 ∈ {1,2} [REPORTADO].
- **MOTOR (esta conversación)**: columnas de calendario de difusión (programa, tipo de cifras,
  periodicidad, fecha, periodo de referencia) y títulos de notas sobre calendarios. **Ninguna
  cifra de ENVIPE de ningún año, a ningún nivel** [EJECUTADO].

Consecuencia de diseño que esto impone: **ningún contendiente tiene un parámetro que alguien
elija después de esta fecha.** Por eso todos los contendientes de §2 son mecánicos y se
declaran juntos, y por eso las variantes de tendencia entran **todas a la vez** o no entra
ninguna. No hay "la mejor variante": hay las que había.

## 1 · Qué prueba este duelo, y qué no

Prueba **transferencia prospectiva a una ola que nadie del programa ha abierto**, a nivel
nacional, en la única serie anual con R sellado por ola que tenemos. Es lo que la jornada 1
mostró que no existe: el duelo de tres es RETROSPECTIVO para sus tres contendientes.

No prueba: que el motor "entienda" nada. Si una tendencia gana, dice que una regularidad se
transporta entre olas — no dice por qué existe. Y el error nacional promedio esconde dónde se
concentra: por eso §5 exige el desglose antes de cualquier frase de producto.

## 2 · Contendientes — mecánicos, declarados todos juntos, sin selección posterior

**Hallazgo que cambia el conteo [EJECUTADO].** Para `evade_norma` la constante del motor en
`milpa/tramite.yaml:497` es `0.562774`, y el nacional de la ola 2025 sellado en
`CALC-TRA-EVADE-NORMA-SXD-EMISIONES-0001` (`G-M25-P-NACIONAL`) es `0.5627744787844097`.
**Son el mismo número.** La constante del motor y la persistencia t−1 no son dos contendientes
en este estimando: son uno. Se emite **una sola vez**, rotulada
`K = constante-del-motor ≡ persistencia-t−1 (coinciden en este estimando)`, y se dice en el
marcador. Para cualquier otro estimando que entre al duelo, la coincidencia **se comprueba por
comando antes de congelar**, no se supone.

| id | contendiente | de dónde sale | nivel |
|---|---|---|---|
| K | constante del motor ≡ persistencia t−1 | `tramite.yaml` / nacional ola 2025 sellado | nacional |
| T3 | tendencia lineal, últimas 3 olas | serie nacional sellada | nacional |
| T5 | tendencia lineal, últimas 5 olas | serie nacional sellada | nacional |
| TC | tendencia lineal, serie completa | serie nacional sellada | nacional |
| E+ | persistencia por eje + desplazamiento nacional predicho por la tendencia, **en logit** | marginales sellados ola t−1 + T* | marginal por eje |
| C2 | marginales de la misma ola, sin interacción, réplica por réplica con guardián | como el piloto 2 | cruce |
| L | LLM — solo si cumple §3 | — | nacional |

**Restricción de construibilidad, declarada, no rellenada [EJECUTADO].** La serie nacional
sellada de 15 olas (`data/corrida0/envipe-serie-denuncia-v1_0.tsv`, olas 2011–2025) es del
estimando **delito personal no denunciado** (`p_c1_u1`), no de `evade_norma`. Para
`evade_norma` solo hay tres puntos nacionales sellados (olas 2023, 2024, 2025:
0.521540, 0.538725, 0.562774). Por tanto:
- estimando **no-denunciado**: T3, T5 y TC son todos construibles (15 puntos);
- estimando **evade_norma**: T3 construible; **T5 y TC = NO-CONSTRUIBLE por serie insuficiente**,
  y así se asientan. No se sustituyen por T3, no se rellenan, no se omiten del marcador.

Un estimando entra al duelo solo si tiene R sellado por ola en al menos tres olas y un universo
idéntico a lo largo de ellas. La comparabilidad por ola se lee de la columna del archivo
(`comparabilidad`), no se asume: la ola 2011 está marcada
`INSTRUMENTACION-NOMINAL-Y-RESIDUALES` y no entra a una serie que se trate como homogénea sin
que la spec lo diga.

**E+ en logit, explícito.** `logit(p_eje,2026) = logit(p_eje,2025) + [logit(T*_nac,2026) −
logit(p_nac,2025)]`, con T* la variante de tendencia que corresponda; se emite una fila por
variante. El desplazamiento es nacional y común a todos los ejes: eso es la hipótesis, y es
falsable — si el desplazamiento real difiere por eje, E+ pierde contra la persistencia por eje
en los ejes que se movieron distinto, y eso es un hallazgo sobre México, no sobre el motor.

## 3 · Regla del LLM

Cuenta como PROSPECTIVO **solo** un modelo sin acceso web y con corte de entrenamiento
anterior al 10/sep/2026. Con web, o con corte posterior, es RETROSPECTIVO: se rotula así en su
propia fila y **nunca se promedia con los mecánicos**, o se excluye. El corte se documenta con
la cita del proveedor, no con la respuesta del modelo sobre sí mismo. Si no se puede acreditar,
la fila es `NO-ACREDITABLE` y no entra. Ausencia de L no invalida el duelo: los mecánicos son
la prueba.

## 4 · Procedimiento — tres commits (E.6), guardia, D-22

- **COMMIT-1 · spec congelada, sin microdato 2026.** Estimandos, universos, unidad, ponderador,
  los siete contendientes con su fórmula cerrada, la regla de adjudicación, el B-bis de §6, y
  el medidor completo. Guardia de **una sola variable de agrupación**. Nada en scratch.
  **D-22**: antes de congelar, el punto de entrada corre **de punta a punta sobre ENVIPE 2025,
  ya abierta**, y reproduce lo sellado (`G-M25-P-NACIONAL` y los marginales del piloto 2) dentro
  de la tolerancia del tipo. Un medidor cuyas pruebas solo ejercitan guardias y constantes no
  es COMMIT-1.
- **COMMIT-2 · emisiones selladas.** Las siete emisiones con su IC95, ciegas a R. El orden del
  diff es el sello. Un R derivado antes de este commit degrada el ejercicio a factibilidad y se
  declara.
- **COMMIT-3 · R y adjudicación.** Se abre ENVIPE 2026 solo con el código congelado en
  COMMIT-1. Un cruce visto se declara consumido y no se relanza sobre él.

Descarga del payload: permitida desde hoy (firma), y **conviene hacerla ya** para que la
disponibilidad del microdato no sea la excusa que retrase el sello. Descargar no es abrir: el
payload queda en el corpus compartido, con su sha256, y nadie lo lee.

**Fecha límite de sello de COMMIT-2: 31/oct/2026.** No por el calendario del INEGI —la ola ya
está publicada— sino por la exposición: cada semana que pasa aumenta la probabilidad de que
alguien del programa vea una cifra de 2026 y contamine la ceguera. La reserva es lo que hace
prospectivo a este duelo, y se degrada con el tiempo, no con el calendario.

## 5 · Qué se reporta

Por contendiente: MAE en pp, **cobertura de IC95 (R dentro del IC del candidato)** con su
intervalo binomial, y el punto dentro del IC de R — las tres, sin colapsarlas, como en la
jornada 1. Y el desglose: dónde se concentra el error por eje. Un contendiente que acierta en
el agregado nacional y falla en rural o en escolaridad baja no es un buen contendiente para
México; el promedio lo esconde.

## 6 · B-bis · Pre-registro de falsación (escrito antes de ver nada)

| si ocurre | se concluye | rótulo |
|---|---|---|
| K gana a las tres tendencias, con IC que despejan | la serie no tiene pendiente aprovechable a un año; la persistencia es el estimador adjudicado y la tendencia se retira como retador | corroborada |
| alguna T* gana a K con IC que despeja | la pendiente se transporta una ola; el retador entra a piloto por dominio, y **solo esa variante**, sin reajustar ventana | corroborada |
| T* gana en punto pero el IC no despeja | **falsador débil**: no adjudica. K sigue siendo el adjudicado (A-bis: un piso no vencido se adopta) | falsador débil |
| ningún contendiente se distingue de otro | la ola 2026 no discrimina entre estos candidatos a este n; se declara y **no se relanza sobre la misma ola** | acotada |
| E+ pierde contra persistencia por eje | el desplazamiento nacional no es común a los ejes; se acota E+ a los ejes donde ganó y se dice cuáles | acotada |
| todos los contendientes yerran en el mismo sentido y por magnitud similar | hubo un cambio de nivel en la ola (instrumento, muestra o mundo); **no es un veredicto entre candidatos** y se investiga antes de adjudicar nada | acotada |

Si dos filas pueden satisfacerse a la vez, manda la de arriba. Se sella con la spec.

## 7 · Lo que este diseño NO hace

No toca cruces reservados de otros dominios. No abre ENIF ni ENCIG. No propone cambiar el
emisor. No adjudica ninguna celda-D: produce evidencia para que el dueño de cada dominio la
adjudique bajo su contrato.
<<<ANEXO-A-FIN>>>

## NO-CORRIDO / RESERVAS

- **qué:** «P4 · Congelar, o decir por qué no» para `CALC-DUELO-ENVIPE2026-EMISIONES-0001` y `CALC-DUELO-ENVIPE2026-ADJUDICACION-0001` (y, por tanto, «congelado según D-22 ampliada, demostrado» para el COMMIT-1 de 2026). · **por qué:** `DIFERIDO-A:` acto de caja que registre `envipe2026_csv` en `data/manifiesto.yaml` con sha (cola `data/cola-adquisicion-v1_0.tsv:158`, prioridad 1; bajar y hashear SOLO, sin descomprimir ni listar) y corra `python3 tools/corrida0.py preflight CALC-DUELO-ENVIPE2026-EMISIONES-0001` → VERDE; el requisito 1 de D-22 ampliada falla hoy por `input_manifiesto_AUSENTE=envipe2026_csv` (los requisitos 2–4 se cumplen). Ninguna otra edición está autorizada al congelar; si `preflight` bloquea por otra causa (sufijo de miembro o columna renombrada en 2026), abre v1.1 por otra sesión. · **impacto:** el COMMIT-2 (fecha límite 31/oct/2026) no puede arrancar; la ceguera se degrada con el tiempo. · **sucesor:** «congelar cuando el payload entre» — acto de adquisición en caja + sesión del COMMIT-2 (F3, otra sesión).
- **qué:** «P3 (i) … reproduce lo sellado —nacional `G-M25-P-NACIONAL`, marginales y C2 del piloto 2— dentro de la tolerancia del tipo», en la parte `S1` (= `C7` del piloto 2) y `MAE(C2)`. · **por qué:** `NO-VERIFICABLE-AQUÍ` a `1e-10`: el piloto 2 construyó `C7` y su `MAE(C2)` sobre el `C2` de los marginales sellados **a seis decimales** (`tramite-ola5-propuesta-v0.yaml`), no sobre el re-derivado; `S1` difiere `1.1e-6` y `MAE(C2)` `2.2e-5` pp, y con ese `C2` redondeado y mi `Ī` la diferencia es `0` en las 12 celdas (atribución exacta, `hallazgos.md`). `C2` re-derivado (`1.1e-16`), `P = C1` (`0.0`), `R` (12 celdas, p e IC95, `0.0`) y el nacional sí reproducen. · **impacto:** ninguno sobre contadores; el control `RESULT-DUELO25E-EM-CTRL-SXD-S1-REPRODUCE` queda `NO` en el sello con su delta, y el módulo genérico queda validado por la atribución. · **sucesor:** SIN-ASIGNAR (no requiere acto: atribuido y declarado en la spec §9 vía esta fila).
- **qué:** E+ (§3 de la spec) ejercitado sobre oro. · **por qué:** `DIFERIDO-A:` COMMIT-2 — en el ensayo «como si 2025 fuera la ola nueva» `T3` para `evade_norma` es NO-CONSTRUIBLE (solo 2023 y 2024 anteriores) y E+ sale `null` declarado en sus 13 celdas × 3 variantes; para `no-denunciado` E+ es NO-CONSTRUIBLE por diseño (sin marginal por eje sellado; el guardián mide un solo desenlace). E+ solo está probado sobre sintético (`test_e_mas_formula_y_replicas`) y por `_valida_outputs`. · **impacto:** la fila 5 del B-bis (E+ vs persistencia por eje) no tiene ensayo sobre oro antes del COMMIT-3. · **sucesor:** COMMIT-2/3 del duelo (otra sesión).
- **qué:** Regla del LLM (diseño §3): fila `L`. · **por qué:** `DECISIÓN-DE-MESA-PENDIENTE` — este acto no corre LLM (encargo §10); `L` entra al COMMIT-2 solo con firma de mesa que acredite modelo sin web y corte anterior al 10/sep/2026 por cita del proveedor; si no, `NO-ACREDITABLE`/`NO-ENTRA`. · **impacto:** ninguno: los mecánicos son la prueba (diseño §3). · **sucesor:** mesa, antes del COMMIT-2.
- **qué:** `origen_numerico` / `envuelto_legacy` de los tres CALC sellados en `data/corrida0/corridas.tsv` (= `INDETERMINADO`). · **por qué:** `FUERA-DE-PERÍMETRO`: `tools/corrida0.py registro` (TUBERÍA) — `_funcion_de_dependencia` no clasifica el input `serie_nd` (`data/corrida0/envipe-serie-denuncia-v1_0.tsv`) y `_referencias_numericas_de_intermediario` solo reconoce rutas, no `calc_id` en celdas; la cadena real es GEN2 (15 `calc_id` en la propia tabla). Los `spec.yaml` están sellados y no se editan (PARO e). · **impacto:** la columna de linaje de tres filas propias dice `INDETERMINADO` en vez de `NUEVO`; `cuenta_gen2 = SI` no se afecta. · **sucesor:** GEN2-TUBERIA (registrador: reconocer `calc_id` en intermediarios TSV o `funcion: DATO` explícita); los dos CALC de 2026 pueden declarar `funcion: DATO` al congelarse si TUBERÍA lo sella antes.
- **qué:** `tests/test_duelo_prospectivo.py` cableado en CI. · **por qué:** `DIFERIDO-A:` FP-398 (a) — censado en `forense/analisis/ci-guardias/censo-tests.tsv` (fila propia; `--ejecuta-huerfanos` lo reconoce: `SKIP … NECESITA-DEPENDENCIA(pytest)`); corre en CAJA (25/25) y se salta en CI hasta que mesa instale `pytest`/`numpy` en el runner. · **impacto:** ninguno hoy; el job `guardias` solo exige la fila. · **sucesor:** FP-398 (a).
