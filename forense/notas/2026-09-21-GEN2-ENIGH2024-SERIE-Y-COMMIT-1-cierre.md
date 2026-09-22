# Nota de cierre · ACTO GEN2-ENIGH2024-SERIE-Y-COMMIT-1 · 21/sep/2026

Encargo archivado (A.3): `forense/encargos/2026-09-21-GEN2-ENIGH2024-SERIE-Y-COMMIT-1.md`, 0-bis `74921d1a`, sello de cuerpo `f5913666…`, raíz de acto `7492`. Rama `acto/gen2-enigh2024-serie-y-commit-1`, una sola sesión, Sonnet 5 por mandato de mesa (presupuesto), 2 sub-agentes fork de solo lectura (verificación de premisas; reconocimiento de precedentes ENUT/ENCIG), MODO ABIERTO hasta cada COMMIT-1 y RÍGIDO después. Resumen compacto de todo lo de abajo: `canon/gobernanza-v1_15.md` ADR raíz de este acto.

## 0 · ARRANQUE

Guard 0.a-0.d: base `99a43faf` = SHA de redacción del encargo, 0 commits de diferencia al abrir; árbol limpio; rótulo sin duplicado (rama remota, worktree, PR — los tres verificados por comando); `limpia_arbol.py --reporta` sin bloqueo. `data/raw` enlazada a `/home/pc0/mm-corpus/raw`, `data/raices.local.yaml` copiada del clon padre. Entorno CAJA confirmado.

## 1 · Premisa del encargo corregida contra el árbol (A.8)

El encargo (§1) dice que los cuatro sellados de ENIGH 2022 (incluido `CALC-ENIGH-0001`) están "medidos en una sola ola". Verificado contra `data/corrida0/`: **falso para `CALC-ENIGH-0001`** — su estimando (`remesas>0`, hogar, tasa base) ya está sellado en **cinco olas** (2014/2016/2018/2020/2022) por `CALC-B-0001` y `CALC-B-MARCO-ENIGH-0001`, ajenos a este acto, con solapes verificados dígito a dígito. Esto es justo lo que el propio §1 del encargo adelanta como conclusión ("un solo estimando pasa: remesas>0") — el trabajo real de P1 son los otros tres CALC. Se declara aquí en vez de repetirlo en cada pieza.

## 2 · P1 · Series sobre olas abiertas

**Ventana**: 2016-2022 (no 2012-2022). Verificado por dos vías independientes de las ya existentes: `url_origen` del manifiesto (`_ncv_` en 2012/2014 contra `_nueva_serie_`/`_ns_` en 2016 en adelante) y `RESULT-BM-ENIGH-2014-METADATO-VERSION` (`identifier=...-ENIGH-2014-NCV`, sellado, ajeno). El encargo dejaba 2012 como posible ("si el corte de serie lo permite, declarado") — no lo permite, y queda declarado.

**Hallazgo de generalización, verificado antes de escribir código nuevo**: `poblacion.csv` de 2016/2018/2020 no trae `factor`/`est_dis`/`upm` como columnas (2022 y 2024 sí). Verificado que en 2022 estas tres columnas son **idénticas byte a byte** a las de `concentradohogar` de la misma llave hogar (muestra: 500 hogares, 1667 personas, 0 discordancias) — INEGI simplemente las copió a `poblacion.csv` desde esa ola, sin cambiar el diseño. Los tres medidores nuevos toman esas columnas de `concentradohogar` por `(folioviv, foliohog)` — matemáticamente la misma operación, no un cambio de método.

**Oro, verificado ANTES de sellar ninguna ola nueva**: el `medidor.py` que se congeló para cada ola nueva, reconfigurado (constantes de módulo, sin tocar la lógica) para leer 2022, reproduce byte a byte (`P1-MARGINALES-SHA256`/`P2-CONJUNTA-SHA256`/`P2-MARGINALES-COMPLETOS-SHA256` de PERFIL-ESTRUCTURAL) y bit a bit (bootstrap de 2000 réplicas de INTENSIDAD-REMESAS, misma semilla) los tres `resultados.json` ya sellados de 2022. `tests/test_enigh_serie_oro.py` lo deja como regresión permanente. No se selló un CALC-2022 nuevo (sería un duplicado byte-idéntico sin información nueva, D-14).

**Nueve CALC sellados** (3 medidores × 3 olas), cada uno vía `corrida0.py preflight` → `run` real (no simulado): `preflight` VERDE en los nueve, sello `COINCIDE` en los nueve. Serie de `remesas_media` entre receptores: 7249.08 (2016) → 8330.98 (2018) → 9507.28 (2020) → 14455.43 (2022, ya sellado) pesos por trimestre; prevalencia nacional 0.04746 → 0.04729 → 0.04378 → 0.04569 (coincide exacto, delta=0.0, con la serie ya sellada de `CALC-B-0001` en las tres olas nuevas — control de consistencia interno, no oro).

## 3 · P2 · Comparabilidad 2022→2024 por texto

`data/enigh-comparabilidad-texto-v1_0.tsv`, misma forma que `credito-comparabilidad-texto` (adaptada: unidad de fila `variable`, no `conducta`×`ola` — declarado en el `.tsv.meta` por qué). Leído `enigh2024_descripcion_base_pdf` (ya en el corpus por `#977`) con `pdftotext -layout`, comparado contra las citas ya selladas de `enigh2022_descripcion_base_pdf`. 14 variables: 13 `MISMO-INSTRUMENTO`, 1 `CAMBIO-MENOR` (`factor`: 2024 tampoco trae `factor`/`est_dis`/`upm` en `poblacion.csv` — mismo hallazgo que P1, mismo join sirve sin cambio si un acto futuro abre 2024). `remesas` (P041) confirma por texto — código y definición intactos — por qué `remesas>0` ya pasaba la regla de entrada. **Cero microdato de `enigh2024_ns_csv.zip` abierto**: sólo el diccionario y el listado de miembros del zip (A.7, listar no es abrir).

## 4 · P3 · Spec del duelo

`forense/prereg-caja/DUELO-PROSPECTIVO-ENIGH2024-spec-v1_0.md` formaliza `DISENO-duelo-prospectivo-ENIGH2024-v1_0.md` (propuesta de otro acto, `ACTO GEN2-ENIGH2024-RESERVA-Y-DISENO-1`) a contrato ejecutable, citando sus secciones en vez de repetirlas. Ningún contenido sustantivo del diseño cambia — lo que este acto añade es lo que una spec congelable exige y la prosa no traía: guardia de código (§7), preflight con salida cruda (§9), D-22 explícito (§8).

## 5 · P4 · Código, ensayo, guardia

**Por qué el código es propio y no importa `tools/duelo/`**: la cabecera del encargo declara `tools/duelo/` **ajeno** al perímetro de este acto. `tools/enigh_duelo_nacional.py` reimplementa el mismo diseño matemático (OLS en logit, delta method) que el molde de ENVIPE, con un conjunto de contendientes distinto (`C-T2`/`C-MEDIA` en vez de `T5`/`TC`, porque ENIGH nunca tiene más de 3 olas de historia en la ventana de este duelo).

**`CALC-ENIGH-DUELO-ORIGEN-MOVIL-0001` (sellado)**: RETROSPECTIVA-MECÁNICA sobre la serie sellada de `remesas>0`. Resultado medido, declarado tal cual es (ni inflado ni escondido): en la ventana de 3 olas retrospectivas, `C-MEDIA` (MAE 0.1406 pp) le gana numéricamente a `C-PISO` (MAE 0.1867 pp). **Esto no corrobora ni refuta B-bis-1 del diseño** — B-bis-1 es sobre el duelo real de 2024 (que exige ganar TAMBIÉN en el punto real, no solo en la retrospectiva), y con 3 puntos de historia el margen de error de esta comparación es enorme. Se declara para que quien corra COMMIT-2/3 no tenga que re-derivarlo, no como una conclusión.

**`tools/enigh_duelo_guardian.py`**: único código autorizado a leer `concentradohogar` de ENIGH 2024 antes de COMMIT-3 (E.6). Sin ejes (el diseño no los tiene, §3): la guardia es que sólo se leen 6 columnas, nunca otra cosa, y `nacional()` rechaza explícitamente un marco `reservada=True` — sólo `emite_bajo_reserva(autoriza=True)` puede calcular la celda sobre una ola reservada. Probado con 6 casos contra un zip **sintético** (`tests/test_enigh_duelo_guardian.py`): proporción correcta, bloqueo de `nacional()`, exigencia de los dos flags en `emite_bajo_reserva()`, detección de marco alterado por huella, columna ausente falla alto. Nunca contra el zip real.

**`CALC-ENIGH-DUELO-EMISIONES-0001` (COMMIT-2, PREVISTO)**: spec + medidor congelados, probados contra OTRO zip sintético (no commiteado como prueba, para no duplicar `test_enigh_duelo_guardian.py` — la única función que llama contra datos reales ya está cubierta ahí). `preflight` VERDE: el input real (`enigh2024_nc_csv`, sha256 completo) **COINCIDE** — identidad verificada sin abrir el archivo. **`run` nunca se invocó**: hacerlo abriría el zip reservado, PARO (a) explícito del encargo.

## 6 · Estado de "congelado" — lo que este acto NO decide

El diseño del duelo (`DISENO-duelo-prospectivo-ENIGH2024-v1_0.md`) trae en su cabecera: **"Estado: PROPUESTA, NO CONGELADA"**, y espera la firma `FP-260921-GEN2-ENIGH2024-RESERVA-Y-DISENO-1-b7ae-02` (adopción del diseño). Esa firma sigue **PENDIENTE** al cerrar este acto. El encargo actual pide llegar, en P4, a "congelado por D-22" — este acto interpreta eso como el nivel COMMIT-1 (spec + código + guardia + ensayo retrospectivo, todo lo que D-22 puede verificar sin abrir dato), no como la autorización de adoptar el diseño ni de correr COMMIT-2/3. Adoptar la firma pendiente por cuenta propia tocaría una firma de mesa — PARO por lista cerrada. Se pregunta explícitamente en `FP-260921-GEN2-ENIGH2024-SERIE-Y-COMMIT-1-7492-01`, y se sigue con lo demás (D-19: una pregunta no es un PARO).

## 7 · Qué NO significa lo de arriba (auditoría §5 de instrucciones)

- El resultado de `CALC-ENIGH-DUELO-ORIGEN-MOVIL-0001` (`C-MEDIA` < `C-PISO` en MAE) **no predice** quién gana el duelo real de 2024: es una ventana de 3 puntos, y B-bis-1 exige ganar también ahí.
- Que `remesas>0` esté sellado en 5 olas **no dice nada sobre remesas informales ni sobre hogares de ingreso alto**: ENIGH sub-capta ambos (heredado del diseño §7, no medido de nuevo aquí).
- Que la comparabilidad textual de 2022→2024 salga 13/14 `MISMO-INSTRUMENTO` **no es una medición de continuidad estadística** — es continuidad de definición en el diccionario; la serie real de 2024 puede diferir por razones ajenas al instrumento (composición muestral, coyuntura).
- El `CAMBIO-MENOR` de `factor` **no es un cambio de definición**: es dónde vive la columna, no qué significa.

## 8 · Verificación final

`tests/check.py --rapido`: VERDE, 0 FAIL, 297 WARN (los WARN nuevos son la propia fila FP pendiente y el `NC-HUÉRFANA` de T34 hasta el commit de `## NO-CORRIDO / RESERVAS`, que sigue a esta nota). `main` se movió 30 commits durante el acto (PR #987 y mantenimiento de CI); fusionado sin conflicto en `e9c00c9e`.

## 9 · Pendiente de mesa

`FP-260921-GEN2-ENIGH2024-SERIE-Y-COMMIT-1-7492-01`: ¿la firma `b7ae-02` (adopción del diseño del duelo, ya `ABIERTA` desde el acto anterior) se firma aparte, o el lanzamiento de este encargo — que pide explícitamente llegar a "congelado" — cuenta como esa adopción? Sin resolver esto, ningún acto puede correr `CALC-ENIGH-DUELO-EMISIONES-0001`/`-ADJUDICACION-0001`.
