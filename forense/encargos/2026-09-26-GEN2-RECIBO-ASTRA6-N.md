# ENCARGO · ACTO GEN2-RECIBO-ASTRA6-N · Recibo de un PR de MISION-ASTRA-6 (C1 validación ciega · C2 familias 2027 · C3 reports v2): lo que cada carril prometió en la ADENDA-1 se verifica por comando, y mesa recibe FUSIONAR / FUSIONAR-CON-NC / DEVOLVER con la razón

> ENTORNO: **NUBE** — lee la rama del PR, RESULT sellados, paquetes archivados; cero microdato. Hook imprime ENTORNO-DERIVADO; si dice CAJA, PARA.
> Plantilla: una instancia por PR (N consecutivo desde 1). Sustituir `<PR>`, `<carril>`, `<rama>`; SHA de la rama fijado al abrir. Hereda de `GEN2-RECIBO-ASTRA-PRODUCTO-N` (`6773bbcdf2ada478`) los seis criterios comunes (cifras con RESULT, etiquetas y sellos, perímetro, olas, §3 México, recomendación) y añade los propios de cada carril.

CABECERA · SHA de redacción `4f125e70` (re-deriva al abrir) · una sesión, rama propia (la que fije la plataforma; se declara) · MODELO: Opus (C1 y C2); Sonnet (C3) · MODO: **AUTÓNOMO** (cláusula v1.0) · ids con raíz de acto (D-24) · D-21 aplica · cierre por /acto: `## NO-CORRIDO / RESERVAS` y `## CONSUMIDO` con esas palabras.
CONTADOR: cero mediciones; no adopta; no mueve `cuenta_gen2`. PR: `<PR>` · carril: `<carril>` · rama: `<rama>` · SHA: `<git rev-parse origin/<rama>>`.

## 1 · OBJETIVO
Un veredicto por PR con los seis criterios comunes más los del carril:

**C1 · Validación ciega (ADENDA-1 §C1).**
- **Paquete archivado antes de entregarse**: `forense/validacion-independiente/catalogo-1/paquetes/<lote>/` con `.sha256`, y su commit anterior al primer commit de la sesión ciega (orden por historial: aquí sí sirve, porque es orden, no ausencia de lecturas). Contenido del paquete = spec humana + cuestionario + descriptor + insumos autorizados; **si contiene `medidor.py`, `resultados.json`, reports que revelen valores o el repo completo, el lote es `REIMPLEMENTACIÓN-INDEPENDIENTE-NO-CIEGA`** y así se rotula; no es DEVOLVER, es rótulo.
- **Números congelados antes de comparar**: commit de los recálculos anterior al commit del comparador/tabla; tolerancias preexistentes citadas (o declaradas antes de revelar, con commit).
- **Estados y efectos**: cada fila con uno de `COINCIDE · DISCREPA · NO-RECALCULABLE-DESDE-SPEC · BLOQUEADO-POR-ACCESO · NO-EVALUADO`, y cada DISCREPA con efecto (cifra · incertidumbre · alcance · conclusión · ninguno). Un lote que presente `NO-EVALUADO` o bloqueos como validación = DEVOLVER.
- **Sin cambios a sellos ni adopciones** desde el carril (solo NC y propuestas); `replay-evidencia.tsv` con asiento `validacion_independiente` por RESULT tocado.
- **Sesión de diseño ≠ sesión ciega** declarado en la nota.

**C2 · Familias 2027 (ADENDA-1 §C2).**
- COMMIT-1 completo (D-22: `spec.yaml`, medidor congelado con guardia de una variable, auditoría del código, prueba por mutación, preflight sobre sintético y sobre oro histórico, ids nulos declarados, ningún hash sobre archivo vivo) **antes** de COMMIT-2 (orden por historial).
- **Ninguna ola reservada leída** (inputs por id contra `manifiesto.yaml`; futuras inexistentes; ENVIPE 2026, ENCO, último periodo de ENOE/ENSU, ENIGH 2024 fuera de AMAI).
- Familia ≠ ola: conteos y dependencia declarados; calendario con fecha oficial o ventana con fuente; potencia con escenarios rotulados; estados `SELLADO-INTERNAMENTE · ENVIADO-A-ATESTACIÓN · ATESTIGUADO-EXTERNAMENTE` sin colapsar; retador externo ≤ 1 por familia y solo si estructural (regla 6: nada sobre olas vistas); familias nuevas como propuesta, no como CALC.
- Frase de producto con N/M/K derivados.

**C3 · Reports v2 (ADENDA-1 §C3).**
- `corpus/reports/` (v1) sin diff; v2 en `corpus/reports-v2/` con índice derivado.
- Tabla afirmación × dictamen (`CONFIRMA · MATIZA · ROMPE · SIN-CIFRA` con razón diferenciada) × RESULT/CALC/fila; **trazabilidad de afirmaciones cuantitativas** (no de dígitos: años, n bibliográficos y cifras de literatura con fuente primaria, separadas de los RESULT propios); sellados no adoptados rotulados como evidencia provisional.
- §3: evidencia (a)/(b)/(c), marcos importados con crítica, sin confundir estructura con cultura, firewall genético; sin apartados vacíos; tier de frecuencia ≠ tier de mecanismo; módulo de auditoría completo con [v2.16]; sin texto reproducido de fuentes (paráfrasis; una cita corta por fuente).
- Muestra de 10 afirmaciones al azar (semilla declarada) verificadas contra su RESULT o fuente.

«Hecho»: nota con la tabla criterio × veredicto por comando · recomendación FUSIONAR / FUSIONAR-CON-NC / DEVOLVER con la lista exacta · fila FP para mesa · NC por defecto que Astra no abrió · `check.py --baseline` VERDE sobre la rama fusionada localmente.

## 2 · FIRMAS DE MESA — dadas
MISION-ASTRA-6 y su ADENDA-1 (acuerdo; mesa: «acordado»), R(a) de FIRMAS-15 (recibo obligatorio), regla 6, E.2, E.6, D-22.

## 3 · LO QUE DIRECCIÓN SABE
`[EJECUTADO]` (`4f125e70`) Astra empujó `codex/astra6-c1-paquetes-1` con seis encargos propios archivados (C1-PAQUETES-1, C2-ENCIG-1, C2-ENIF-1, C2-ENVIPE-1, C3-CONSUMO-FAMILIA-1, C3-SOCIAL-1): **Astra se organizó por lotes con encargo por lote, como la ADENDA-1 pedía**; cada uno abre su PR y recibe su recibo. Plantilla base: `RECIBO-ASTRA-PRODUCTO-N`; precedente de auditoría post hoc: cero REVERTIR en 14 unidades, 12 sin recibo (eso ya no puede pasar: R(a)).

## 4 · YA HECHO / YA DECIDIDO
`ls forense/encargos | grep -c "RECIBO-ASTRA6-<N>"` → 0.

## 5 · PIEZAS
Comunes → propios del carril → recomendación → FP/NC.

## 6 · LATITUD — CLÁUSULA DE AUTONOMÍA v1.0
1–7 verbatim. Un PR que mezcle carriles se recibe por carril y se dice. Pregunta a mesa prevista: **ninguna**.

## 7 · PAROS — lista cerrada (D-19 estricta)
a) abrir dato reservado · b) editar la rama de Astra o un sello · c) adoptar; poner `cuenta_gen2` · d) no aplica · e) CAJA.

## 8 · COMPUERTAS
«El recibo lee; no corrige» protege **borrar/reescribir**. «Un lote sin paquete archivado antes de la sesión ciega no es validación ciega» protege **adoptar** (E.2 segunda pregunta). «Ninguna ola reservada en C2» protege **abrir dato**.

## 9 · PERÍMETRO Y CONCURRENCIA
Propio: nota, `tools/recibo/` (scripts reutilizables), TSV de gobierno (append), L0, cascada. Ajeno: la rama de Astra, todo lo demás. En vuelo: los siete actos de hoy (no chocan).

## 10 · LO QUE NO HACE · SUCESORES
No fusiona, no adopta, no corrige a Astra. Sucesor: el siguiente N.

## NO-CORRIDO / RESERVAS

| qué | por qué | impacto | sucesor |
|---|---|---|---|
| «check.py --baseline VERDE sobre la rama fusionada localmente» para #1170, #1172 y #1173 | NO-VERIFICABLE-AQUÍ: los tres chocan con origin/main. #1172 y #1173 se resolvieron por union en local (#1173: VERDE). #1170 y #1172 se midieron sobre su HEAD (#1170 ROJO, #1172 VERDE). Resolver un conflicto de la rama de Astra es editarla (PARO b). | El VERDE de #1172 es sobre el HEAD, no sobre el merge. | Astra, al resolver el conflicto |
| Replay de oro y firma CAJA de los CALC de #1170, #1172 y #1174 | NO-VERIFICABLE-AQUÍ: NUBE sin microdato. `verify` da INPUT AUSENTE o NO-EJECUTABLE. | El oro se LEYÓ de `ejecucion.json`/`oro.json`, no se re-ejecutó. | sesión CAJA post-merge (NC-…-996b-03) |
| Citas externas de los reports de #1173 | NO-VERIFICABLE-AQUÍ: red denegada por política (EGRESS_BLOCKED). | La trazabilidad de literatura se verificó por forma, no por contenido de la fuente. | siguiente recibo C3 |
| Plantilla GEN2-RECIBO-ASTRA-PRODUCTO-N | SUSTITUIDO-POR:criterios K1–K6 PROPUESTO-POR-EJECUTOR (absorbe los seis criterios comunes nombrados en el encargo; queda huérfano cualquier criterio de la plantilla que no esté en esa lista) | Si la plantilla aparece, la diferencia se declara. | mesa / dirección |
| Recibo de #1166 y #1171 (N=1, N=2) | DIFERIDO-A:GEN2-RECIBO-ASTRA6-N (siguiente instancia; D-11 limita el lote a cuatro piezas) | #1171 sigue en main sin recibo (R(a)). | NC-…-996b-07 |
