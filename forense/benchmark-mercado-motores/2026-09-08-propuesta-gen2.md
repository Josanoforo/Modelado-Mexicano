# Gen2 frente a los benchmarks: demostrar valor sobre una tasa base

**Corte:** redactada contra `main = 7a958b06940b6c36e416859d7cd79879a8370e5a` (PR #613);
premisas materiales re-verificadas y actualizadas contra `main = 6f1500e2`
(PR #614, GEN2-PRE-E5 fusionado, ADR-400) el 8/sep/2026 — el parche aplica
limpio sobre ese corte y la suite queda LÍNEA BASE VERDE (3 FAIL · 186 WARN
heredados, ninguna entrada nueva).
**Estado:** propuesta de dirección y componente técnico optativo; no adopción de parámetros.
**Mandato:** revisar el transfer, los benchmarks acumulados y los PR recientes;
integrar una mejora acotada si aporta al modelo actual.

## Decisión recomendada

**Integrar el selector temporal de B y usarlo en la siguiente evaluación de
valor incremental de M.** La pregunta decisiva es si el motor mejora una
predicción trivial con la misma información disponible. Ganarle a un LLM
sin ese comparador no responde esta pregunta.

Mantener la secuencia operativa vigente: **GEN2-T9 (en vuelo, rama
`claude/motor-matricial-d11-demanda-2188aw`) → GEN2-E5-0 → GEN2-E5**.
GEN2-PRE-E5 ya fusionó como PR #614 (ADR-400): `estado_calc`, el firewall
no circular de T35, la separación medición/adopción y el despacho
sincronizado están en `main`. Este cambio se revisa aparte: no añade una
compuerta a esa secuencia, no reabre el runner ni modifica CALC-0001…0003,
y no bloquea ni es bloqueado por la re-derivación de la demanda de T9
(archivos disjuntos, verificado por diff contra su rama).

La siguiente prueba sustantiva de M es **la dimensión de segmento que el
ejecutable sellado ya trae**: el motor es matricial por sello de mesa
(ADR-91, `gobernanza:1821`, «M1 cómputo matricial como definición del
ejecutable») y evaluado en `x = ∅` se reduce a la `p` base — encender
`x ≠ ∅` en **una sola regla** (diseño T9 P3(b), corre en C0-D) y compararlo
contra la `p` base y contra B, fuera del dato de calibración. La dimensión temporal sirve para ordenar esa prueba; buscar la
tasa de la misma ola evaluada no demuestra capacidad predictiva.

## Qué cambió realmente con Gen2

| Frente | Evidencia vigente | Consecuencia |
|---|---|---|
| Motor M | El ejecutable sellado es matricial (ADR-91): `motor.py`/`matriz.py` con `g(B, θ(x))`; el corredor evaluado hasta hoy pasa por el **emisor** (`milpa/src/emisor.py::emitir_binaria`), que devuelve la `p` base de la regla — la matriz evaluada en `x = ∅` | La constancia observada es el punto-origen de la matriz, no ausencia de estructura; el efecto de ola/segmento existe en el ejecutable y se enciende por celda (T9/C0-D), no se «añade» un modelo |
| Runner | [#601](https://github.com/Josanoforo/Modelado-Mexicano/pull/601), [#608](https://github.com/Josanoforo/Modelado-Mexicano/pull/608), [#610](https://github.com/Josanoforo/Modelado-Mexicano/pull/610): spec, snapshot, contrato, run, sello y replay | Cambió cómo nace y se reproduce un resultado; eso permite medir con confianza en su procedencia |
| Demanda y consumo | [#600](https://github.com/Josanoforo/Modelado-Mexicano/pull/600), [#603](https://github.com/Josanoforo/Modelado-Mexicano/pull/603), [#611](https://github.com/Josanoforo/Modelado-Mexicano/pull/611) | La demanda y las dependencias se derivan; medir y adoptar deben seguir separados |
| Marcador | [#613](https://github.com/Josanoforo/Modelado-Mexicano/pull/613): M y agregado envueltos, R/L pendientes | Hay dos CALC sellados de preparación, con `cuenta_gen2: PENDIENTE-DE-MESA`; no una victoria comparativa nueva |
| Caja | [#612](https://github.com/Josanoforo/Modelado-Mexicano/pull/612) | Cierra la pieza de infraestructura del encargo; las corridas reales de R siguen necesitando corpus |

`python3 tools/corrida0.py status`, re-ejecutado sobre `6f1500e2` (#614), devuelve:

```text
N_corridas_requeridas=79
N_corridas_selladas=0
N_resultados_activos=162
N_resultados_sellados=0
N_resultados_pendientes=162
dependencias_numericas_legacy_activas=162
N_resultados_gen2_sellados=0
N_resultados_gen2_pendientes_adopcion=0
N_resultados_gen2_adoptados_activos=0
resultados_con_validacion_independiente=0
diferencias_materiales=0
no_corrido_abiertas=10
replays_legacy_sellados=2
```

(Los tres contadores `gen2_*` los añadió PRE-E5 (#614) y arrancan en cero,
como esta propuesta exige: medir no adopta.)

Estos son los contadores de demanda/adopción de la CLI en este corte. El cero
no niega la existencia de los dos CALC de preparación de #613. Sus etiquetas
y el contador responden preguntas distintas. El agregado actual tiene
`N-CON-R=0`, `N-CON-L=0`; ambos ejes comparativos son `NO-ESTIMABLE`.

## Qué conservar de los cuatro documentos y qué corregir

| Documento compartido | Aporte que sigue sirviendo | Ajuste para decidir hoy |
|---|---|---|
| Mercado 25/ago, v1.0 | Separar afirmaciones comerciales de una comparación sobre las mismas celdas | No sostener exclusividad mundial ni superioridad por número de ADR, commits o hashes |
| Mercado 1/sep, v1.1 | La falta de cobertura de M en el piloto era un hallazgo útil | Sus cifras pertenecen a aquella versión y población; no son contadores Gen2 |
| Mercado 6/sep, v1.2 | Detectó la poca información del indicador «en banda» y propuso error en pp | La secundaria en pp ya entró en [#592](https://github.com/Josanoforo/Modelado-Mexicano/pull/592); no implementarla otra vez. La constancia de M era temporal, no evidencia directa de falta de segmentación |
| Revisión 7/sep | B, heterogeneidad, holdout y diagnóstico del corpus son prioridades útiles | Reordenar: B y evaluación fuera de muestra antes de adoptar M por ola, ampliar dominios o entrenar confianza |

El resultado favorable del 7/sep sí está en el JSON histórico:
`agregado-v1_3-resultado.json`. La diferencia pareada de MAE en pp favorece
a M frente a L-solo en **7.23 pp [0.68, 16.92]**, y frente a L+corpus en
**15.10 pp [5.92, 25.71]**. La primaria L-solo–M continúa
`INDETERMINADO`. Se verificaron esas claves, no se recalculó el marcador.
**Son resultados GEN1, leídos como historia; no se usan como inputs GEN2.**

### Corrección material a P1: la ola exacta puede contener la respuesta

La propuesta del 7/sep sugiere que M consulte `serie_olas` para emitir la tasa
de la ola que el árbitro evalúa. El código y los insumos muestran un riesgo
concreto: `tramite.yaml` ya contiene tasas ENCIG cuya procedencia es
literalmente `R-json (TRA-M-03, ya público)` y `R-json (TRA-M-07, ya público)`.
Usarlas para predecir esas mismas celdas reutilizaría el árbitro como respuesta.
Puede servir como reconstrucción o verificación, con ese rótulo, pero no como
éxito fuera de muestra. El filtro F-DD existente también distingue
`P0 VERIFICACION` de `P1 PUNTUA`.

T9 (en vuelo) ya adopta leave-one-out para la modulación por ola (P3(c):
«ola más cercana **distinta** a la del árbitro; empate → anterior»). Dos
filos que este selector cierra y que suben a T9 como adenda de mesa:
(1) «más cercana» admite una ola **posterior** cuando la serie no trae
anterior — caso concreto en el marco: remesas ENIGH, celda objetivo 2016
con serie que arranca en 2016, elegiría 2018; la regla operable es *última
ola anterior al periodo del árbitro y disponible al corte; sin anterior →
`modela_ola: SIN-PREVIA`, la celda no modula*. (2) Las entradas de serie
con `metodo: R-json (TRA-M-…)` se rotulan `ORIGEN-ARBITRO`: F-DD cubre el
par misma-encuesta-misma-ola, no la reutilización cruzada de un valor que
ya pasó por el árbitro; una celda que las consuma queda
`VERIFICACION-NO-PUNTUA`, no `P1`.

La revisión del 7/sep además llama 2017 a TRA-M-03: el **marco vigente dice
2013**, y TRA-M-07 dice 2021. Se sigue el marco, sin modificar el documento
histórico compartido.

Medición descriptiva sobre el marco y las calibraciones actuales:

| Conducta / grupo | Celdas | Ola objetivo | Calibración que M consulta |
|---|---:|---|---|
| Denuncia con miedo/desconfianza | 6 | ENVIPE 2012, 2013, 2015, 2021, 2023, 2024 | ENVIPE 2025 |
| Tiene ahorros | 1 | ENNViH 2002 | Declaración compuesta: ENNViH 2005–06 y ENIF 2024 |
| Apoyo familiar para vejez | 1 | ENIF 2018 | ENIF 2024 |
| Remesas | 3 | ENIGH 2016, 2018, 2020 | ENIGH 2022 |
| Mordida | 3 | ENCUCI 2020; ENCIG 2013, 2021 | ENCIG 2025 |

**Las 14 celdas usan una calibración posterior al periodo objetivo; ninguna
demuestra pronóstico hacia adelante con corte histórico.** Una también
transfiere explícitamente entre ENCUCI y ENCIG. Esto no invalida la prueba
retrospectiva autorizada: delimita lo que demuestra. Tampoco prueba que todo
el error se deba a la ola; universo, reactivo y traslado entre instrumentos
pueden contribuir.

Hay 14 emisiones y 5 valores distintos. CIV ocupa 6/14 filas: **42.9%** del
marco. No deben confundirse 14 filas con 14 mecanismos independientes; tampoco
puede inferirse que el tamaño efectivo sea exactamente cinco. Mantener el
marcador histórico y proponer una sensibilidad por grupo es preferible a
colapsarlo o escoger la agregación que salga favorable.

Receta de la tabla: leer las filas elegibles de
`forense/prereg-duelo-v2/marco-M-sorteado-v1_3.tsv`, agrupar por
`(regla, conducta)`, llamar a `tools.emite_m.cita_ola_calibracion` con ese par
y las líneas de `milpa/tramite.yaml`, y contrastar con los RESULT-M del CALC
sellado. Es metadato de la emisión, no una nueva estimación de conducta.

### Precedente de B en el piloto, citado para no reabrirlo a ciegas (A.10)

En el duelo GEN1, B salió `SIN_BASELINE` en las 15 celdas y mesa **declinó**
adquirir tasas base para el piloto, con razón medida: las 9 arbitrables
tenían `publicada=NO` por diseño del sorteo (FP-166, FIRMADA; ADR-207/208),
y B quedó **opcional** en el contrato re-sellado, con las casillas de skill
«no evaluable» cuando B no exista. Esta propuesta no reabre ese cierre: su
universo era el marco sorteado del piloto bajo GEN1. El B de aquí es otro
territorio — RESULT GEN2 recomputados, con disponibilidad documentada al
corte — y por eso se propone de nuevo, no se hereda.

## Frente al mercado: qué merece copiarse

La comprobación externa se limitó a fuentes primarias que podían cambiar la
priorización. No es un nuevo censo de proveedores ni una prueba de sus productos.

| Referencia | Evidencia pública revisada | Aplicación razonable a MILPA |
|---|---|---|
| Simile | Su artículo [Building confidence in Simile](https://www.simile.com/blog/confidence) describe predicción del error TVD, unos 8,600 ítems retenidos, validación cruzada agrupando pregunta y muestra, y comparación con baselines | Estimar dónde se equivoca M con predicciones retenidas; no convertir el tier o el IC muestral de R en «probabilidad de que M acierte» |
| Aaru | Su [descripción de simulación](https://aaru.com/simulation) explica ajuste de distribuciones conjuntas, validación fuera del entrenamiento y criterios por caso de uso | Probar una interacción observable y una decisión concreta, preservando población y estimando; no saltar a una población sintética completa |
| Evaluación temporal | La [documentación de scikit-learn sobre fuga de información](https://scikit-learn.org/stable/common_pitfalls.html) explica por qué usar información no disponible al predecir infla el rendimiento | Fijar corte y versión de los insumos; separar reconstrucción retrospectiva, validación retenida y pronóstico |

Las dos primeras son descripciones de los proveedores, no validaciones
independientes contra México. Pero contradicen la caracterización acumulada
de «punto y adjetivo, sin método publicado». No hay aquí evidencia de que
MILPA supere a Simile/Aaru; tampoco la hay de que esos productos superen a
MILPA en las celdas mexicanas. «Nadie mide México» y «único marcador del mundo»
no son conclusiones defendibles a partir del barrido realizado.

## Cambio implementado en esta propuesta

`tools/baseline_temporal.py` añade un selector ejecutable para B:

- Exige periodo objetivo y fecha de corte; excluye la misma ola, periodos
  superpuestos y versiones que aún no estaban disponibles.
- Compara exactamente encuesta, reactivo, universo, codificación, segmento y
  unidad. No deduce equivalencia entre instrumentos o códigos.
- Mantiene la precedencia ya descrita para B: última ola pública admisible;
  después persistencia de una medición previa disponible; después `SIN_BASELINE`.
- Devuelve el RESULT y la fuente seleccionados y el motivo de exclusión de
  observaciones. `null` sigue siendo no estimable; un cero real sigue siendo cero.
- Rechaza porcentajes como proporciones, NaN, valores fuera de rango y
  alternativas ambiguas en la última ola. No promedia para resolverlas.

El B anterior elegía `max(historial, key=ola)`, dando por hecho que el llamador
había filtrado correctamente; su interfaz no conocía el objetivo. El sucesor
hace explícito ese corte. No se altera el archivo sellado ni se activa el
sucesor dentro de ningún CALC existente.

**Límite:** es un componente de selección, no un productor GEN2 terminado.
Un ID escrito en el JSON no demuestra su procedencia. El medidor consumidor
deberá resolver los RESULT auténticos y sus metadatos dentro del snapshot
declarado de `corrida0`; este módulo no sustituye esa validación. No se
inventaron fechas de publicación ni se migraron las tasas `serie_olas`.
Todavía no hay una cifra B real ni una mejora medida del error de M.

Interfaz Python: `seleccionar_baseline(Objetivo(...), [Observacion(...)])`.
CLI: `python3 tools/baseline_temporal.py entrada.json`; los campos son los de
las dataclasses del módulo, con fechas ISO y objetos `serie` anidados. El
adaptador `desde_documento` acepta el mismo documento ya parseado desde los
bytes de un snapshot. `disponible_desde` corresponde a **la versión utilizada**;
una revisión de 2026 de una ola 2019 no estaba disponible para pronosticar 2021.

## Orden de integración y criterio de éxito

| Orden | Trabajo | Qué permite decidir / cuándo parar |
|---|---|---|
| Ahora | PRE-E5 completado (#614). Cerrar T9 (en vuelo) y correr GEN2-E5-0 y GEN2-E5; revisar este selector por separado | Producir RESULT nuevos. El benchmark no bloquea esas corridas |
| 1 | En una familia, recomputar B y R en GEN2, fijar el mismo corte informativo para M y B; reportar error en pp y cobertura sobre pares comunes | Saber si M mejora la tasa base. Si M sólo emite esa misma tasa, declarar equivalencia del algoritmo; no vender estructura adicional |
| 2 | Encender la matriz en **una** regla (`x ≠ ∅`, motor sellado, diseño T9 P3(b)/C0-D) con conjunto retenido; comparar M matricial contra M base (`x = ∅`) y B | Emitir por segmento sólo si el error fuera de muestra o la decisión objetivo mejora sin perder cobertura material; si no, la celda conserva `x = ∅` / `modela_segmento: NO` — no hay modelo nuevo que adoptar ni retirar |
| 3 | Calcular E cuando existan L-solo, L+corpus y M GEN2 compatibles | Su definición por mediana ya está firmada, pero la intersección de 14 del histórico no sustituye capturas nuevas; no entrenar pesos con el mismo benchmark |
| 4 | Diagnóstico de error/confianza, por grupos y casos de uso | Sólo entrenar confianza cuando haya suficientes errores retenidos y variación para evaluarla; «20 celdas» por sí solo no acredita suficiencia |
| Después | Ampliar dominios, L+tasas diagnóstico y productos externos | Hacerlo cuando cambie una decisión o permita medir una hipótesis concreta, con alcance y coste explícitos |

Primer ensayo temporal sugerido: **remesas, ENIGH Nueva Serie**, comenzando
por 2016→2018→2020→2022. Tiene unidad de hogar y desenlace explícitos. Antes
de puntuar hay que confirmar comparabilidad y fechas de disponibilidad de las
versiones usadas. Las olas 2012/2014 no se añaden automáticamente. No copiar
sus valores actuales: recomputar en GEN2. Tres transiciones servirían como
ensayo descriptivo, no como demostración general sobre México.

Para el paso 2, ahorro en ENIF es candidato por sus ejes ya inventariados.
La elección final depende de qué RESULT y códigos deje listos la medición;
no se firman aquí un cruce de segmentos, un umbral de ganancia o una nueva
adopción. El grupo de entrenamiento y el retenido deben fijarse antes de ver
los nuevos errores. El marco de 14 celdas históricas permanece como tal.

## Validación y pendientes

`python3 tests/test_baseline_temporal.py`: **9 pruebas pasan**, con datos
ficticios. Cubren corte, revisiones posteriores, identidad del estimando,
abstención, precedencia, ambigüedad, valores inválidos, solapamiento y CLI.
La prueba entra al workflow existente. No se llamaron LLM ni servicios pagos,
ni se abrió microdato para producir cifras nuevas.

Pendiente material para usar B en el marcador: historial de RESULT GEN2,
metadatos comparables y disponibilidad documentada; spec de un CALC consumidor
sucesor y su ejecución normal. R/L (NC-0018/0019) conservan su estado; NC-0020 la cierra T9 en vuelo con
la unidad de celda `regla × segmento × ola × instrumento`. Este cambio no
cierra ninguna.

**Avance:** queda implementada una selección temporal utilizable, se descarta
un camino que reutilizaría la respuesta del árbitro y queda definido el
experimento que puede demostrar el aporte incremental del modelo.

## Alcance de lectura

Se leyeron los cuatro benchmarks compartidos, su manifiesto y el transfer
(los dos TXT son idénticos). Los ZIP del 7/ago se inspeccionaron como contexto
histórico; no se derivaron de ellos cifras actuales. Se consultaron los 35 PR
más recientes y se concentró la lectura de implementación en #592/#597 y la
transición #600–#613. No se realizó una auditoría general de cada diff.
Las propuestas de mercado siguen siendo documentos de dirección. Este archivo
usa un nombre propio para no confundirlas con el benchmark interno de L/M/R.
