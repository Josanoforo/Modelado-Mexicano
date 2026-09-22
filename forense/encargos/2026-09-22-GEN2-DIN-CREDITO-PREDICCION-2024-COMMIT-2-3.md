# ENCARGO · ACTO GEN2-DIN-CREDITO-PREDICCION-2024-COMMIT-2-3 · LA SECCIÓN DE CRÉDITO DE ENIF 2024 SE ABRE UNA VEZ, CONTRA LA PREDICCIÓN CONGELADA

> ENTORNO: **CAJA**. NO es NUBE. **F3:** no la sesión de `#987` (congeló).
CABECERA · SHA de redacción `bda6b60c`; una sesión, rama `acto/gen2-din-credito-prediccion-2024-commit-2-3` · MODO **RÍGIDO** · CONTADOR: sella dos corridas; `cuenta_gen2 = SI`; no adopta; el marcador levanta la reserva de crédito por comando. **L0 de `canon/estado-programa-v1_14.md`: si choca, toma la de `main` y re-inserta solo tu anotación; `canon/L0/` existe.**
**MODELO: Sonnet por mandato de mesa.** Procedimiento congelado o receta; latitud logística; toda duda de procedimiento se pregunta a mesa en una línea con opciones.
NO tocar (TUBERÍA): `tests/check.py`, `tools/cierre_acto.py`, `tools/tablero_programa.py`, `.github/workflows/`, `.claude/commands/`. Cierre: `tests/check.py --rapido` antes de empujar; el CI corre la suite completa. Derivados («DERIVADO — NO EDITAR») no se commitean: los re-deriva el job de main.

## 1 · OBJETIVO
Paso 5 del orden de mesa para crédito: abrir 2024 después de predecir. `#987` congeló la predicción: nueve conductas (K1, K2 no bancaria por familia, K3, K4a, K4b, K5, K6), contendientes mecánicos sellados, y un backtest sobre las cuatro olas reales donde **persistencia ganó en 7 de 9**. Este acto mide la realidad de 2024 y adjudica. «Hecho»: EMISIONES y ADJUDICACION selladas, cada una en `origin` antes de la siguiente; veredicto con la regla de la spec (diferencia de error medio con IC) por conducta y por nivel; cada marginal de K1–K3 publicado **con K4(b) y K5 al lado**; B-bis palabra por palabra; vista, replay, marcador; nota de una página.

## 2 · FIRMAS — verbatim, en el repo
Reserva de crédito (`decisiones.tsv:186`): «La sección de crédito de ENIF 2024 queda RESERVADA desde hoy, con el hueco declarado: el par "crédito por app" (n=200) está visto y consumido; no se relanza sobre él.» FP-404. Alcance v0 (20/sep). Las de `#987` (ff56-01/-02 en (a); «las corridas cuentan»), selladas por lanzamiento. D-22 ampliada (v2.16): preflight VERDE con main fusionado · `_valida_outputs` en cada rama terminal, celda rara incluida · nulos y NaN declarados · ningún input sobre archivo vivo.

## 3 · LO QUE DIRECCIÓN SABE (contra `bda6b60c`)
- `[EJECUTADO]` `CALC-DIN-CREDITO-PREDICCION-2024-EMISIONES-0001` y `…-ADJUDICACION-0001` congelados (`1960c5fe`, «congelado sin correr»); `ADJUDICACION/spec.yaml:33` trae `commit_3a` («misma sesión del COMMIT-2, commit aparte, ANTES de derivar cualquier R»); input `enif2024_csv, origen: manifiesto` con nota «presente y hasheado; bajar y hashear no es abrir».
- `[LEÍDO: nota de #987 :27-40]` backtest: persistencia mejor en 7/9; K1 y K6-tenedores favorecen T3 por márgenes de centésimas; no se fijó umbral de materialidad a propósito (la regla es la de la spec: IC).
- `[LEÍDO]` K4 mide «nunca ha tenido»; K3 no colapsa empeño y gota a gota; unidad persona; universo 18+ (2021 referencia) con el recorte 18-70 sellado aparte para conmensurar.

## 4 · YA HECHO
Los dos CALC sin `ejecucion.json`; ninguna rama COMMIT-2. Repítela tú.

## 5 · PIEZAS — orden estricto
**P0.** `preflight` EMISIONES VERDE con `enif2024_csv` COINCIDE; `pytest` de los ensayos de `#987`; censo: `data/raw/enif2024_csv.zip` nunca leído por sección de crédito (rastro → PARO); el par «crédito por app» excluido en la spec.
**P1 · COMMIT-2.** `corrida0 run …-EMISIONES-0001`. Sella; nulos por familia. Push; `ls-remote`.
**P2 · Compuerta.** Puntos de los contendientes no nulos donde hay soporte; nulo → PARO antes de R.
**P3 · COMMIT-3a.** Lo que `spec.yaml:33` dice. `preflight` ADJUDICACION → VERDE. Commit propio, push.
**P4 · COMMIT-3.** `corrida0 run …-ADJUDICACION-0001`. Reporta por conducta: MAE de cada contendiente; ΔMAE con IC y su salida; cobertura del IC (R dentro del IC del candidato) con intervalo binomial; K4(b) y K5 junto a cada marginal de tenencia; B-bis. `EXPLORATORIO — NO ADJUDICA` después.
**P5 · Cierre.** Marcador y tablero por comando; nota: qué predijo el programa, qué salió, con qué certeza, qué NO significa (**no tener crédito formal no es preferir el informal**: rechazo, requisitos, buró; adulto elegido; unidad persona) y una línea: ¿alguna tendencia venció a la persistencia en 2024, sí o no?

## 6 · LATITUD (solo logística) · 7 · PAROS
PAROS: a) leer crédito de ENIF 2024 fuera de `corrida0 run` de estos CALC · b) tocar el par «crédito por app» · c) editar spec, `spec.yaml` fuera de P3, o `.py` · d) `run` no sella → no se parcha · e) P2 halla un nulo · f) repetir una corrida · g) sesión/entorno equivocados · h) adoptar. Compuertas: P0 y «emisiones en origin» protegen abrir dato. Perímetro: `ejecucion/resultados/sello` de los dos CALC, la línea de P3, filas propias, marcador/tablero por comando, nota, cascada. Fuera, PARA. `## NO-CORRIDO / RESERVAS` · `## CONSUMIDO`.

## NO-CORRIDO / RESERVAS

P1 tal como el encargo la escribió ("`corrida0 run` …-EMISIONES-0001") NO
se corrió: esa pieza ya estaba sellada desde `#987` (premisa §4 estaba
basada en un estado intermedio de COMMIT-1, no en el final; verificado
contra el árbol antes de obedecer, v2.16 §2). PARO-PREMISA declarado y
replanteado como logística — no bloqueó el objetivo: se ejecutó la
secuencia real de `-ADJUDICACION-0001/spec.yaml` (`commit_3a` → `commit_2`
→ `commit_3`), confirmada con dirección antes de abrir el dato.

El eje escolaridad completo (4 de 16 celdas × 9 conductas) no entró a
ninguna comparación cuantitativa: defecto heredado en el código SELLADO de
`-ADJUDICACION-0001` (COMMIT-1, `#987`) — `_code()` (importado de
`-EJES-0003`) quita el cero inicial de `niv`, incompatible con los códigos
2024 de dos dígitos. Código ya sellado (E.3): no se repara en este acto.
`NC-260922-GEN2-DIN-CREDITO-PREDICCION-2024-COMMIT-2-3-95ec-01`
(DECISIÓN-DE-MESA-PENDIENTE); `FP-260922-…-95ec-01` pide a mesa la vía de
corrección. El resto del CALC (12 de 16 celdas por conducta) no está
afectado.

`FP-260921-GEN2-DIN-CREDITO-PREDICCION-2024-COMMIT-1-7866-01` (¿ratifica
mesa K6-P-TENEDORES, no K6-PR?) sigue ABIERTA — ajena a este acto, no
gatea nada de él.

## CONSUMIDO

PR #997. ADR de raíz `ADR-260922-GEN2-DIN-CREDITO-PREDICCION-2024-COMMIT-2-3-95ec-01`.
`CALC-DIN-CREDITO-PREDICCION-2024-ADJUDICACION-0001` corrido y sellado
(commit_2), adjudicado por conducta (commit_3): `PROPUESTA-CON-RESERVA` en
K1 y K6-P-TENEDORES, `NADIE-VENCE` en K2-*/K3/K5, sin retador en K4A/K4B.
`tests/check.py --rapido`: VERDE, 0 FAIL, 299 WARN; `--baseline`: LÍNEA
BASE VERDE. El PR no se fusiona en este acto: queda propuesto, mesa
fusiona.
