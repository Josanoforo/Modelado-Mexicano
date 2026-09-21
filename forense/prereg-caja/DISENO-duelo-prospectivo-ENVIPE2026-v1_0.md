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
