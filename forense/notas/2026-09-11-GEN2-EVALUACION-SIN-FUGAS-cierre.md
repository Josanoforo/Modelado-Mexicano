# ACTO GEN2-EVALUACION-SIN-FUGAS · cierre

Fecha: 11/sep/2026  
Entorno: NUBE/WSL2; repo y agregados, cero microdatos, cero llamadas a modelos
y cero solicitudes a terceros.  
Encargo: `forense/encargos/2026-09-11-GEN2-EVALUACION-SIN-FUGAS.md`.

## Resultado útil

`CALC-F5-REANALISIS-0001` aplica controles fail-closed al panel F5 conocido.
Su spec enumera 245 inputs directos y únicos: 224 respuestas L, 14 resultados
R y siete piezas de contrato/código. Cada miembro tiene ruta, rol y SHA-256;
el runner resuelve sus bytes una vez y el núcleo no abre el árbol.

El calculador rechaza IDs o roles ambiguos, hash cambiado, coordenadas de
captura distintas, R con spec/ruta/punto discordante, parámetros no soportados
y conjuntos no correspondientes. Una celda contaminada, con identidad no
confirmada, punto M inválido, estimando/corte no acreditado o linaje no apto se
conserva en cobertura y exclusiones, pero nunca se puntúa. Si el control cambia
el U3 congelado, la única salida global es
`NO-ADJUDICABLE-POR-CONTROL`.

El medidor consume desde los bytes fijados `milpa/src/linaje.py` del acto 17 y
su función `aptitud_para_uso`; no mantiene un segundo resolver. El snapshot M
histórico carece de `origen_numerico`, `camino_linaje`,
`dependencia_objetivo`, `validacion_independiente` y `rol_evaluacion`, por lo
que las 14 celdas quedan correctamente `INDETERMINADO`, sin inferir limpieza.
La dependencia 18 quedó integrada, pero su snapshot sucesor no es input de
esta corrida: sus 16 salidas directas declaran origen `NUEVO` y aptitud de
linaje, pero las 16 conservan `validacion_independiente=NO-HECHA` y sus roles
son `medicion_directa` (14) o `proxy_descriptivo` (2), no
`HOLDOUT`/`EVALUACION-RETENIDA`. Por ello no habilita confirmación
independiente ni se evaluó un M renovado.

## Historia y reanálisis lado a lado

| salida | histórica `CALC-TRIADA-0002` | protegida `CALC-F5-REANALISIS-0001` |
|---|---:|---:|
| naturaleza | comparación publicada | reanálisis diagnóstico del panel conocido |
| marco | 14 | 14 |
| posiciones L | 224 | 224: 171 válidas, 53 abstenciones, 0 malformadas/técnicas/identidad |
| cobertura L_SOLO / L_CORPUS | 14 / 12 | 14 / 12 |
| puntos M / M elegible | 14 / no separado | 14 / 0 |
| puntos R | 14 | 14 |
| U3 | 12 | 0; conjunto congelado comprometido |
| MAE L_SOLO (pp) | 3.9573621816025666 | no estimable |
| MAE L_CORPUS (pp) | 3.889025747112979 | no estimable |
| MAE M (pp) | 4.9866732397828875 | no estimable |
| veredicto | `SIN-GANADOR-UNICO` | `NO-ADJUDICABLE-POR-CONTROL` |

La segunda columna no sustituye ni corrige la primera. La diferencia nace de
un contrato distinto, posterior a la inspección: exige comparabilidad, corte y
linaje que la corrida histórica no acreditaba. No “rescata” un ganador y no es
evidencia de transferencia.

## Decisión de elegibilidad por celda

Fuente común **A**:
`forense/notas/2026-09-10-GEN2-F5-APRENDIZAJES-Y-SUCESOR-diagnostico.md §2`.
Fuente **B**:
`forense/prereg-duelo-v2/F5-aprendizajes-sucesor-v1_0/traza-motor.tsv` y
`forense/notas/BENCHMARK-WEB-CUATRO-DECISIONES-GEN2-2026-09-11.md §3`.
El detalle canónico completo, incluidos puntos, brazos y razones, está en
`RESULT-F5SF-DETALLE-CELDAS-JSON` del resultado sellado.

| celda | criterio fijado | fuente | decisión | efecto en cobertura |
|---|---|---|---|---|
| CIV-M-01 | unidad, recorte, códigos y ola difieren | A | no elegible: estimando/corte no acreditados; linaje/dependencia indeterminados | conserva L/L/M/R; no entra a U3 |
| CIV-M-02 | unidad, recorte, códigos y ola difieren | A | no elegible: estimando/corte no acreditados; linaje/dependencia indeterminados | conserva L/L/M/R; no entra a U3 |
| CIV-M-04 | unidad, recorte, códigos y ola difieren | A | no elegible: estimando/corte no acreditados; linaje/dependencia indeterminados | conserva L/L/M/R; no entra a U3 |
| CIV-M-10 | unidad, recorte, códigos y ola difieren | A | no elegible: estimando/corte no acreditados; linaje/dependencia indeterminados | conserva L/L/M/R; no entra a U3 |
| CIV-M-12 | unidad, recorte, códigos y ola difieren | A | no elegible: estimando/corte no acreditados; linaje/dependencia indeterminados | conserva L/L/M/R; no entra a U3 |
| CIV-M-13 | unidad, recorte, códigos y ola difieren | A | no elegible: estimando/corte no acreditados; linaje/dependencia indeterminados | conserva L/L/M/R; no entra a U3 |
| DIN-M-01 | población entre olas y diseño de varianza no acreditados; R=15.56% permanece descriptivo | B | no elegible: comparabilidad/estimando/corte y linaje indeterminados | conserva L_SOLO/M/R; L_CORPUS sin punto; no entra a U3 |
| FAM-M-01 | coincide el inciso, no la elegibilidad poblacional entre versiones | A | no elegible: comparabilidad/estimando/corte y linaje indeterminados | conserva L/L/M/R; no entra a U3 |
| FAM-M-05 | unidad/evento/ponderación alinean, pero M usa una ola posterior a R | A | no elegible: corte no acreditado; linaje/dependencia indeterminados | conserva L/L/M/R; no entra a U3 |
| FAM-M-06 | unidad/evento/ponderación alinean, pero M usa una ola posterior a R | A | no elegible: corte no acreditado; linaje/dependencia indeterminados | conserva L/L/M/R; no entra a U3 |
| FAM-M-07 | unidad/evento/ponderación alinean, pero M usa una ola posterior a R | A | no elegible: corte no acreditado; linaje/dependencia indeterminados | conserva L/L/M/R; no entra a U3 |
| TRA-M-02 | encuesta, edad, exposición y evento difieren | A | no elegible: estimando/corte no acreditados; linaje/dependencia indeterminados | conserva L/L/M/R; no entra a U3 |
| TRA-M-03 | evento general alinea, pero M 2025 es posterior al objetivo 2013 | A | no elegible: corte no acreditado; linaje/dependencia indeterminados | conserva L/L/M/R; no entra a U3 |
| TRA-M-07 | evento alinea, pero M 2025 es posterior al objetivo 2021 | A | no elegible: corte no acreditado; linaje/dependencia indeterminados | conserva L_SOLO/M/R; L_CORPUS sin punto; no entra a U3 |

Que una cadena de payload sea distinta evita afirmar contaminación directa;
no acredita por sí sola comparabilidad ni independencia. La cercanía numérica
tampoco resuelve unidad o corte.

## Ajustes consumidos del benchmark web

La versión ya archivada por otro acto se consumió desde su ruta versionada;
no se duplicó su carga. Se aplicaron cuatro separaciones:

- punto R, incertidumbre de encuesta, variación L y dependencia entre
  celdas/familias aparecen como capas distintas;
- `DIN-M-01` conserva 15.56% como punto descriptivo; SRS y
  constante+folio son sensibilidades, no diseño oficial ni verdad terreno;
- los intervalos de S6 por localidad sólo son sensibilidad y no habilitan una
  promoción científica;
- las recomendaciones del benchmark informan specs y tarjetas, pero no son
  firmas de adopción.

## Dos decisiones científicas separadas

`F5-documental-dirigida-spec-v1_0.md` propone DIN/TRA en dos celdas, dos
brazos y ocho réplicas: 32 llamadas. Mide recuperación/verificación de una
fuente permitida, no generalización. Exige al menos 6/8 puntos dirigidos
trazables por celda y mejora de cobertura de 4/8; permite como máximo dos
reintentos técnicos.

`F5-transferencia-reservada-spec-v1_0.md` propone familias realmente no vistas.
Un piloto disjunto usa 6 familias × 2 celdas × 2 brazos × 8 réplicas = 192
llamadas. La confirmación fija entre 12 y 30 familias mediante la fórmula de
precisión predeclarada: 24–60 celdas y 384–960 llamadas. El máximo total es
72 celdas, 144 brazos, 1,152 llamadas L, 72 emisiones M y 72 R. Éxito exige
mejora de al menos 2 pp frente a L_SOLO, cobertura M ≥90% y no más de 5 pp
inferior, al menos 12 familias analizables y cero contaminación.

Ambas propuestas siguen pendientes de decisión y autorización de coste. No se
abrió F6, no se cambió el competidor por Codex y un plan Pro no se interpretó
como permiso de API.

## Verificación

- `tests.test_f5_sin_fugas`: 23/23, incluidos controles adversariales,
  clausura, parámetros, baseline histórico y la interfaz real de 17.
- `corrida0 preflight`: verde; 245/245 inputs coinciden.
- `corrida0 verify`: `CONTEXTO=IDENTICO · RESULTADO=REPRODUCE`.
- Sello: `data/corrida0/CALC-F5-REANALISIS-0001/sello.sha256`.
- Suite global: `LÍNEA BASE: VERDE`; conserva sólo tres fallos heredados
  (`T06`×2 y `T08`×1), sin entradas nuevas ni recifrado de `baseline.json`.

## Obligaciones y residuales

| obligación | evidencia | consumidor/alcance | cierre o residual |
|---|---|---|---|
| Impedir puntuación contaminada o sin identidad | calculador y pruebas adversariales | toda celda F5 sucesora | CERRADA |
| Cerrar inputs realmente leídos | spec de 245 miembros, preflight y prueba sin lecturas extra | reanálisis 0001 | CERRADA |
| Reutilizar linaje de 17 | input hash del módulo común, medidor y prueba de interfaz real | 17→19 | CERRADA |
| Mantener historia | comparación lado a lado; cero cambio a TRIADA-0002 | panel conocido | CERRADA |
| Acreditar comparabilidad por celda | tarjetas y resultado detallado | 14 celdas | CERRADA como diagnóstico; 0 elegibles |
| Ejecutar producto documental | spec con 32 llamadas | DIN/TRA | PENDIENTE de decisión de mesa y fuentes |
| Ejecutar transferencia reservada | spec con 192+384–960 llamadas | M renovado | PENDIENTE de decisión de mesa, familias y snapshot elegible de 18 |
| Evaluar un M renovado | contrato de campos definido | evaluación futura | DIFERIDA; no se usa el snapshot histórico |
