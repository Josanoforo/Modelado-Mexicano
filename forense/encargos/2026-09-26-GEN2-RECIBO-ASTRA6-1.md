# ENCARGO · ACTO GEN2-RECIBO-ASTRA6-1 · Recibo post-merge del lote 1 de validación ciega (PR #1184, C1, nueve paquetes ENDIREH): qué significan 685 cifras distintas de 2 561, 11 discrepancias de publicabilidad y 799 specs insuficientes, qué rótulo lleva la ceguera, y qué se sostiene, se acota o se propone suspender en el catálogo

> ENTORNO: **NUBE** — lee `main`, los paquetes archivados, las comparaciones congeladas y los RESULT sellados; cero microdato. Hook imprime ENTORNO-DERIVADO; si dice CAJA, PARA.
> Instancia 1 de `GEN2-RECIBO-ASTRA6-N` (`108b720e993417a3`). PR `#1184` · carril C1 · rama `codex/astra6-c1-validacion-lote1-1` (en `main`, `2af4f29c`) · recibo **post-merge** (R(a) se rompió: se recibe igual y se dice). **Alcance ampliado:** también recibe el lote 2 (`#1185`, `codex/astra6-c1-paquetes-2`, en `main` `57a3f2a4`, once copias verificadas) y la revisión de tanda 2 (`#1189`, `codex/astra6-revision-tanda2`), fusionados ya sin recibo: mismas cinco preguntas, tabla por lote.

CABECERA · SHA de redacción `57a3f2a4` (re-deriva al abrir) · una sesión, rama propia (la que fije la plataforma; se declara) · MODELO: Opus · MODO: **AUTÓNOMO** (cláusula v1.0) · ids con raíz de acto (D-24) · D-21 aplica · cierre por /acto: `## NO-CORRIDO / RESERVAS` y `## CONSUMIDO` con esas palabras.
CONTADOR: cero mediciones; no adopta; no cambia sellos ni `decisiones.tsv`; asienta `validacion_independiente` por RESULT en `replay-evidencia.tsv` según lo que el dictamen dé.

## 1 · OBJETIVO
Contestar por comando, sobre `forense/validacion-independiente/catalogo-1-ejecucion-lote1/` (`informe-lote1.md`, `entregas.json`, `*--comparacion.json` por paquete, constancias de sesiones, `astra6-c1-lote1-recibo-para-claude.md`):
1. **Ceguera.** Por paquete: ¿el archivo con sha se commiteó **antes** del primer commit de la sesión ciega (orden por historial)? ¿Contiene solo spec humana, cuestionario, descriptor e insumos autorizados? Astra pide dictamen sobre la **separación exterior con Bubblewrap** frente al rótulo conservador `NO-CIEGA` que algunos validadores conservaron: el recibo dictamina por paquete `CIEGA-POR-SEPARACIÓN` o `REIMPLEMENTACIÓN-INDEPENDIENTE-NO-CIEGA`, con la evidencia (constancia de sesión, contenido del paquete). El **materializador no ciego** que leyó los esperados para la comparación: ¿estaba separado de la sesión que recalculó? Si no, el lote entero es NO-CIEGA y se dice sin drama.
2. **Las 685 cifras distintas.** No son un número: son una distribución. Por paquete y por causa (tolerancia declarada vs. diferencia observada; redondeo; universo; ponderador; NS/NR; normalización), cuántas caen dentro de la tolerancia preexistente del RESULT (entonces COINCIDE), cuántas son DISCREPA con efecto (cifra · incertidumbre · alcance · conclusión · ninguno), y cuántas son artefacto del comparador. Astra menciona «normalización»: si el comparador normalizó algo después de ver esperados, eso invalida esa comparación y se rotula.
3. **Las 11 discrepancias de publicabilidad.** Lista con RESULT, valor sellado, valor recalculado, efecto y **qué fila del catálogo v1.2 y de la tabla de piso v1.1 las cita**. Recomendación por fila: SOSTENER · ACOTAR (rótulo) · PROPONER-SUSPENDER (fuera de la tabla de piso hasta corregir; el sello no se toca; el sucesor es un CALC nuevo).
4. **Las 799 specs insuficientes** (D-15: «una spec humana debe bastar para recalcular sin leer el código; si no basta, ese es el hallazgo»). Por spec: qué faltó (denominador, ponderador, recorte, tratamiento de NS/NR, módulo/ola). Una NC por spec agrupada por causa; propuesta de sucesor de spec (versión nueva sellada, no edición).
5. **Recomendación a mesa:** `RECIBIDO-POST-MERGE-CON-NC` (lo esperable) o `PROPONER-REVERTIR` solo si el lote escribió en sellos, catálogo o `decisiones.tsv` (no debería: verificar `git diff --stat 2af4f29c^..2af4f29c`). Y la frase de producto honesta para el informe v1.5: «En el primer lote de validación ciega (ENDIREH, N paquetes, N identidades), M cifras coinciden dentro de tolerancia, K discrepan con efecto en [cifra/alcance/conclusión], y J specs no bastan para recalcular; ceguera: [rótulo por paquete]».
«Hecho»: nota con las cinco respuestas por comando · tabla RESULT × estado × efecto (0 filas sin estado) · rótulo de ceguera por paquete · `replay-evidencia.tsv` con `validacion_independiente` asentada por RESULT dictaminado · NC por spec insuficiente (agrupadas) y por DISCREPA · fila FP con la recomendación y la lista de filas del catálogo a acotar o suspender · `check.py --baseline` VERDE.

## 2 · FIRMAS DE MESA — dadas
MISION-ASTRA-6 + ADENDA-1 (acordado): estados `COINCIDE · DISCREPA · NO-RECALCULABLE-DESDE-SPEC · BLOQUEADO-POR-ACCESO · NO-EVALUADO`; efecto por discrepancia; tolerancias preexistentes; ceguera por separación y paquete archivado. FIRMAS-20 D (no revertir por forma; regla de recibo antes de fusionar `codex/*`). E.2 (tres preguntas), D-15, E.3 (sellos no se tocan).

## 3 · LO QUE DIRECCIÓN SABE
`[LEÍDO]` `astra6-c1-lote1-recibo-para-claude.md`: «SOLICITADO, no recibido»; nueve sesiones nuevas separadas del clon; 3 371 identidades; 2 561 cifras: 1 876 coincidentes, 685 distintas; 11 discrepancias de publicabilidad; 799 specs insuficientes; tabla paquete × commit congelado × sha de salida (9 paquetes ENDIREH 2011/2021); pide dictamen sobre Bubblewrap vs NO-CIEGA, sobre el materializador no ciego y sobre normalización; propone abrir sucesores de spec/método y **no** fusionar ni adoptar por ese acto. `[EJECUTADO]` #1184 (`2af4f29c`), #1185 (`57a3f2a4`) y #1189 (`0304bf21`) fusionados el 26/sep sin recibo previo; FIRMAS-20 (#1190) firmada y fusionada, con la regla de recibo antes de fusionar `codex/*` ya asentada — este acto es el último recibo post-merge que debería existir. Catálogo v1.2 (#1168) y tabla de piso v1.1 citan ENDIREH 2011/2016/2021 adoptados por FIRMAS-15 T. `[SUPUESTO]` que las comparaciones congeladas (`*--comparacion.json`) traen valor esperado, recalculado y tolerancia por RESULT: si no traen tolerancia, la carencia es de la spec del CALC (NC) y no se inventa.

## 4 · YA HECHO / YA DECIDIDO
`ls forense/encargos | grep -c 'RECIBO-ASTRA6-1'` → 0. `grep -c 'validacion_independiente' forense/replay-evidencia.tsv` → reporta (las de #970 y lote ENIF; ninguna de ENDIREH).

## 5 · PIEZAS
Ceguera → distribución de las 685 → las 11 → las 799 → recomendación y FP. Un script en `tools/recibo/` que lea los `comparacion.json` y produzca la tabla, reutilizable en los lotes siguientes.

## 6 · LATITUD — CLÁUSULA DE AUTONOMÍA v1.0
1–7 verbatim. Si `comparacion.json` no permite reconstruir la causa de una diferencia, se rotula `CAUSA-NO-DETERMINABLE` y va a NC; no se adivina. Pregunta a mesa prevista: **ninguna**.

## 7 · PAROS — lista cerrada (D-19 estricta)
a) abrir microdato · b) editar sellos, catálogo, `decisiones.tsv` o los paquetes archivados · c) adoptar; asentar `validacion_independiente` = COINCIDE sin tolerancia citada · d) no aplica · e) CAJA.

## 8 · COMPUERTAS
«Estado por RESULT solo con tolerancia preexistente citada» protege **adoptar** (E.2). «Rótulo de ceguera por evidencia de separación, no por declaración» protege **congelar**. «Suspensión solo por FP; el sello no se toca» protege **borrar/reescribir**.

## 9 · PERÍMETRO Y CONCURRENCIA
Propio: nota, `tools/recibo/comparaciones.py` + test, `forense/replay-evidencia.tsv` (append), TSV de gobierno (append), L0, cascada. Ajeno: los paquetes y comparaciones (se leen), catálogo, sellos, la rama de C1 lote 2. En vuelo: FIRMAS-20 (#1190), Astra C1 lote 2 (`astra6-c1-paquetes-2`), CI-TIEMPO-1 si se lanzó.

## 10 · LO QUE NO HACE · SUCESORES
No corrige specs ni cifras. Sucesores: CATALOGO-V1-3-1 aplica las filas a acotar/suspender que mesa firme; sucesores de spec por causa; RECIBO-ASTRA6-2 para el siguiente PR de Astra **antes** de fusionarlo.

## NO-CORRIDO / RESERVAS

| qué | por qué | impacto | sucesor |
|---|---|---|---|
| §1.4 «Una NC por spec agrupada por causa; propuesta de sucesor de spec» — 767 de las 799 | DIFERIDO-A:ASTRA6-C1-REEMPAQUETA-VENTANA-1 — no son D-15: la ventana está en el RESULT sellado y en el catálogo; faltó en `estimandos.tsv` (NC-260927-GEN2-RECIBO-ASTRA6-1-beee-01) | 767 identidades sin validación; COM/ESC/LAB quedan NO-HECHA | ASTRA6-C1-REEMPAQUETA-VENTANA-1 |
| §1.4 — 32 D-15 genuinas (recodificación NIV 31, identidad contradictoria 1) | DIFERIDO-A:GEN2-SPEC-ENDIREH2021-ESCOLARIDAD-1 / GEN2-SPEC-ENDIREH2021-AYUDA-2 — el acto no corrige specs (§10) (NC-…-02, -03) | 32 celdas sin corroboración | GEN2-SPEC-ENDIREH2021-ESCOLARIDAD-1 · GEN2-SPEC-ENDIREH2021-AYUDA-2 |
| §1.2 «por causa» de las 685 | DIFERIDO-A:GEN2-CONTRAFACTUAL-ENDIREH2011-1 — `comparacion.json` no trae causa; hipótesis del ejecutor sin contrafactual → CAUSA-NO-DETERMINABLE (NC-…-04) | causas reportadas como hipótesis | GEN2-CONTRAFACTUAL-ENDIREH2011-1 |
| §1.2 estado de los 1 873 IC con efecto | DIFERIDO-A:GEN2-METODO-COMPARACION-INFERENCIAL-1 — la única tolerancia preexistente es de replay; no se inventa otra (NC-…-06, -07) | ningún IC corroborado ni refutado | GEN2-METODO-COMPARACION-INFERENCIAL-1 |
| §1.3 aplicar SOSTENER/ACOTAR/SUSPENDER al catálogo | DECISIÓN-DE-MESA-PENDIENTE — FP-260927-GEN2-RECIBO-ASTRA6-1-beee-02; catálogo ajeno (NC-…-05) | 7 cifras siguen publicadas sin rótulo | CATALOGO-V1-3-1 |
| §1.1 contenido de `/raw` y red del sandbox | NO-VERIFICABLE-AQUÍ — requiere la caja de Astra (NC-…-08) | el rótulo de ceguera descansa en el transcript para la red | RECIBO-ASTRA6-2 |
| «Hecho»: `replay-evidencia.tsv` con `validacion_independiente` | SUSTITUIDO-POR:GEN2-RECIBO-ASTRA6-1 — asentado en `data/corrida0/validaciones-independientes.tsv` (el TSV citado no tiene esa columna); absorbe los 6 RESULT con cifra; quedan sin asiento COM/ESC/LAB (NO-HECHA, por NC-…-01) | ninguno sobre la vista | ninguno |
| «Hecho»: `check.py --baseline` VERDE | NO-VERIFICABLE-AQUÍ — la sesión corre `--rapido` (P-A); el CI del PR es el juez de la suite completa | ver CI del PR | CI del PR |
