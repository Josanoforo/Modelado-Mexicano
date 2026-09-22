# ENCARGO · ACTO GEN2-MARGINALES-ADOPCION-1 · Los pisos t−1 de 57 celdas marginales, adoptados o vetados por instrumento según su cobertura medida: el yaml de estimadores por segmento deja de tener solo cruces

> ENTORNO: **NUBE** — cero microdato: todo está sellado. Hook; si no coincide, PARA.

CABECERA · SHA `ccd7c0eb` · una sola sesión · MODELO: Opus · MODO: **ABIERTO** · CONTADOR: cero mediciones; mueve `adoptados_activos` (72 → N, derivado) y `n_celdas` de `milpa/estimadores-por-segmento.yaml` (20 → N); **no** mueve `celdas_validadas` · ids raíz de acto.

## 1 · OBJETIVO
Que la decisión de `FP-260921-GEN2-ARBITRO-MARGINALES-1-ed7d-02` quede ejecutada por el único que puede escribirla —el marcador— y que cada celda marginal evaluada tenga en el yaml su estimador adoptado **o** su veto con la cobertura que lo justifica. «Hecho» = `python3 tools/marcador_segmento.py` re-derivado sin editar a mano; `awk` sobre el yaml: N celdas `MARGINAL` con `champion = PERSISTENCIA(t−1)` y cobertura citada, M con `veto: <instrumento, cobertura>`; `status` → `adoptados_activos` movido; FP `…ed7d-02` FIRMADA con cita.

## 2 · FIRMAS DE MESA
- *Propuesta de dirección (recomendación del ejecutor de ARBITRO-MARGINALES-1), mesa sella o edita:* «Piso t−1 en marginales: **ENVIPE 2025 se adopta** (cobertura 8/15 = 0.53 [0.30, 0.75]); **ENIF 2024 se difiere** (6/32 = 0.19 [0.09, 0.35]: el IC de tres años no cubre el cambio real; se re-evalúa con IC de persistencia calibrado); **ENCIG 2025 se veta en nivel** (0/10: persiste el orden, no el nivel) y queda como piso de orden. A-bis 6 «salvo veto»: este es el veto, con dato.» Sin texto → PARA (nada que ejecutar).
- Ya en el repo: A-bis 6 (v2.16 §4), FP-383, `adopcion:piso-C2-20-celdas` (`decisiones.tsv`).

## 3 · LO QUE DIRECCIÓN SABE
- `[LEÍDO]` FP `…ed7d-02`: 57 marginales `EVALUADA`, ninguna con retador, coberturas por instrumento (arriba); «milpa/estimadores-por-segmento.yaml sólo lo escribe el marcador tras firma».
- `[EJECUTADO]` `milpa/estimadores-por-segmento.yaml`: `# DERIVADO — NO EDITAR (tools/marcador_segmento.py, ACTO GEN2-MARCADOR-REDISENO-1)`, `n_celdas: 20`, `n_emitidas_sin_evaluar: 206`, `n_emitidas_con_ic_sellado: 174`, `decision_ref: adopcion:piso-C2-20-celdas`.
- `[EXISTE]` `CALC-ARBITRO-PERSISTENCIA-ERROR-0001`, `CALC-PISO-PERSISTENCIA-ERROR-0001`. No sé cuál trae la cobertura por celda: el acto lo lee.
- `[SUPUESTO]` `tools/marcador_segmento.py` acepta una `decision_ref` de adopción de marginales o la lee de `decisiones.tsv`. Si resulta falso —solo sabe de cruces—, rama prevista: se extiende el tool (≤ el mínimo para leer la decisión por instrumento; declarado; test), nunca se edita el yaml a mano.
- ADJUNTOS: ninguno.

## 4 · YA HECHO / YA DECIDIDO
`grep -c "adopcion:piso-t1\|marginales" data/corrida0/decisiones.tsv` → reporta (al redactar, solo la fila de cruces); yaml sin celdas `MARGINAL` (n_celdas 20). Ramas vivas: ninguna.

## 5 · PIEZAS
- **P1 · Fila de decisión** en `decisiones.tsv` (objeto `adopcion:piso-t1-marginales-por-instrumento`, verbatim de §2) y FP `…ed7d-02` → FIRMADA.
- **P2 · Re-derivación del yaml** por el tool con la decisión: ENVIPE adoptadas (champion, punto, IC, cobertura citada), ENIF `DIFERIDA` (con la cobertura y el sucesor: IC calibrado), ENCIG `VETADA-EN-NIVEL` con `piso_de_orden: SI`. Guardias existentes del marcador en verde (T-RESERVA, T-EMISOR-NO-COMPARA, T-PISO-NO-CIRCULAR).
- **P3 · Consumo:** `ADOPTADO_ACTIVO` en `status` movido por el mecanismo de la casa (`corrida0.py:4256`: sellado citado por consumidor activo); si el mecanismo no admite adopción por celda marginal, PARO c) **no**: es pregunta a mesa con propuesta, y P1/P2 valen igual.
- **P4 · Sucesor escrito:** para ENIF, qué haría falta para re-evaluar (IC de persistencia con varianza del cambio entre olas, no solo muestral) — una NC con sucesor nombrado, sin diseñarlo aquí.

## 6 · LATITUD
DECIDES TÚ: extensión mínima del tool, orden, regenerar derivados. PREGUNTAS A MESA: si ENVIPE tiene celdas individuales con cobertura fuera del IC del instrumento (p. ej. una celda muy desviada), ¿adopción por instrumento igual (recomendado: la firma es por instrumento) o por celda? NO DECIDES: §7.

## 7 · PAROS
a) no aplica · b) editar el yaml a mano o forzar · c) adoptar **fuera** de lo que la firma dice (p. ej. ENIF) · d) no aplica · e) caja · f) inalcanzable.

## 8 · COMPUERTAS
«Firma de §2 presente — protege: adoptar.» Ninguna otra.

## 9 · PERÍMETRO
Propio: `milpa/estimadores-por-segmento.yaml` (por tool) · `tools/marcador_segmento.py` (extensión mínima si hace falta) + su test (huérfano en CI) · `data/corrida0/decisiones.tsv` · `forense/firmas-pendientes.tsv` · derivados por comando · nota · tablero · `canon/L0/<raíz>.md`. Ajeno: los CALC de error (lectura), `tramite.yaml`, celdas-D. Otro acto en vuelo: ninguno verificado; `MARCO-M-CONSUMIDOR-1` lee el mismo yaml sin escribirlo. «Si te encuentras escribiendo fuera de esta lista, PARA.»

## 10 · NO HACE · SUCESORES · CIERRE
No mide, no re-evalúa ENIF, no toca los CALC. Sucesor: el IC calibrado de persistencia para ENIF (diseño de dirección). Auditoría: no aplica (no afirma sobre México: adopta números ya sellados con su cobertura). Cierre por /acto.

## NO-CORRIDO / RESERVAS
- **P3 (parcial) · adoptados_activos.** `NC-260922-GEN2-MARGINALES-ADOPCION-1-c45c-01` — `DECISIÓN-DE-MESA-PENDIENTE`: el mecanismo (`tools/corrida0.py::_estimadores_segmento_para_status`, extendido por este acto) proyecta las 15 celdas ENVIPE `ADOPTADO-POR-FIRMA` como uso activo, pero `aptitud_para_uso` las marca `NO-APTA` porque `origen_numerico` de los `RESULT-PISOS-*` que consumen es `INDETERMINADO` — propiedad de esos CALC, ajena a este acto. Impacto: `N_resultados_gen2_adoptados_activos` se queda en 72 (no sube a 87); `milpa/estimadores-por-segmento.yaml` sí queda con las 15 `ADOPTADO-POR-FIRMA`. Sucesor: `FP-260922-GEN2-MARGINALES-ADOPCION-1-c45c-01` (pregunta a mesa, con recomendación de acreditar el origen_numerico).
- **P4 · sucesor de ENIF, sin diseñar.** `NC-260922-GEN2-MARGINALES-ADOPCION-1-c45c-02` — `DIFERIDO-A:GEN2-ENIF-IC-CALIBRADO-1`: el IC de persistencia calibrado (varianza del cambio entre olas) que permitiría re-evaluar la cobertura 6/32=0.19 de ENIF 2024 no se diseña en este acto, por mandato explícito del encargo (§10). Impacto: ENIF 2024 permanece `DIFERIDA` (32 celdas) hasta que exista ese IC. Sucesor: `GEN2-ENIF-IC-CALIBRADO-1` (sin lanzar).

## CONSUMIDO
Ejecutado por PR [#1002](https://github.com/Josanoforo/Modelado-Mexicano/pull/1002) (rama `claude/gen2-marginales-adopcion-1`). P1: `data/corrida0/decisiones.tsv#adopcion:piso-t1-marginales-por-instrumento`; `FP-260921-GEN2-ARBITRO-MARGINALES-1-ed7d-02` FIRMADA; `NC-260921-GEN2-ARBITRO-MARGINALES-1-ed7d-02` CERRADA. P2: `milpa/estimadores-por-segmento.yaml` clave `marginales` (15 adoptadas / 42 vetadas-diferidas), `tools/marcador_segmento.py` extendido, test nuevo `t_marginales_adopcion_por_instrumento` en `tests/test_marcador_segmento.py`, guardias existentes en verde. P3: `tools/corrida0.py::_estimadores_segmento_para_status` extendido; `adoptados_activos` no se mueve (causa ajena, ver `## NO-CORRIDO / RESERVAS`). P4: sucesor declarado sin diseñar. ADR de raíz: `ADR-260922-GEN2-MARGINALES-ADOPCION-1-c45c-01` (`canon/gobernanza-v1_15.md`, `canon/L0/`). Rótulo censado en `canon/registro-rotulos.tsv`. `tests/check.py --rapido`: VERDE, 0 FAIL. El PR no se fusiona en este acto: queda propuesto, mesa fusiona.

**Post-sello (P4 §2(2), firma de mesa 21/sep/2026): `data/corrida0/marcador-segmento.tsv` y `milpa/estimadores-por-segmento.yaml` NO viajan committeados en este PR** — se revirtieron a la versión de `origin/main` (`tools/derivados_protegidos.py --toca` los marcaba como tocados, guardia bloqueante en `verify.yml`); el job del push a `main` los re-deriva con `tools/marcador_segmento.py --escribe`. Las 57 celdas `marginales` (15 `ADOPTADO-POR-FIRMA` / 42 `DIFERIDA`-`VETADA-EN-NIVEL`) descritas arriba y en el ADR son el resultado PROYECTADO localmente (`python3 tools/marcador_segmento.py --json`, verificado con `t_marginales_adopcion_por_instrumento`); se materializan en el yaml/tsv reales cuando este PR se fusione, mismo patrón que `PR #993` (`ACTO GEN2-LECTURAS-DE-MESA-Y-ROTULOS-1`).

**Post-sello · resolución de `NC-260922-…-c45c-01` (no reescribe la fila de arriba, la cierra).** Mesa respondió `FP-…-c45c-01`, verbatim: «Se acredita origen_numerico de los CALC-PISOS-*-EJES-000x citados por las 15 celdas ENVIPE por fila de decisión 3D caso por caso en decisiones.tsv, tras leer la spec de cada uno (son marginales sobre microdato con cadena; el INDETERMINADO es hueco de etiqueta, no de procedencia), sin editar ningún CALC — precedente FP ed7d-01.» Verificado leyendo `data/corrida0/CALC-PISOS-ENVIPE2024-EJES-0002/spec.yaml` (único CALC que las 15 consumen como piso): input `envipe2024_csv` con `origen: manifiesto` (microdato real) da `ORIGEN-NUEVO`; el `INDETERMINADO` venía del segundo input, `PISOS-REJILLA-METADATOS` (tabla de identidad, sin cifra propia), clasificado `FUNCION-INDETERMINADA` porque `tools/corrida0.py::_funcion_de_dependencia` no reconoce el token `METADATO` — confirma el diagnóstico de mesa. Quince filas nuevas en `decisiones.tsv` (objeto `origen:CALC-PISOS-ENVIPE2024-EJES-0002:<RESULT>`, `origen_numerico=NUEVO`, sin tocar el CALC sellado); `tools/corrida0.py::_origen_numerico_decisiones()` nuevo, mismo patrón de precedencia por RESULT que `_validacion_independiente_resuelta`. Verificado: `N_resultados_gen2_adoptados_activos` **72 → 87**. `FP-…-c45c-01` FIRMADA, `NC-…-c45c-01` CERRADA — la fila de arriba queda como registro histórico de lo que se preguntó, no se edita (A.3).
