# ENCARGO · ACTO GEN2-DIN-CREDITO-CELDAS-D-1 · Las 36 adjudicaciones selladas de crédito (4 celdas × 9 conductas, ENIF 2024) entran a `celdas_validadas` como celdas-D registradas por su acto, sin escribir el marcador a mano

> ENTORNO: **NUBE** — solo RESULT sellados y yaml de registro; cero microdato. Hook imprime ENTORNO-DERIVADO; si dice CAJA, PARA.

CABECERA · SHA de redacción `f28d1038` (re-deriva al abrir; main movido no es PARO) · una sola sesión, rama propia `acto/gen2-din-credito-celdas-d-1` (D-17) · MODELO: Sonnet · MODO: ABIERTO · ids con raíz de acto (D-24) · perímetro de cierre permanente (D-21) aplica sin enumerarlo · «Si te encuentras escribiendo fuera de la lista de §9, PARA.» · cierre por /acto: `## NO-CORRIDO / RESERVAS` («Ninguno.» obligatorio si aplica) y `## CONSUMIDO` al pie; adendas como `<este-encargo>-ADENDA-N.md`.
CONTADOR: cero corridas; `celdas_validadas` sube por derivación (`_celdas_validadas` lee celdas-D) — se reporta antes/después; nada se adopta (los veredictos ya están sellados; el champion de cada celda es el que el CALC adjudicó).

## 1 · OBJETIVO
Que cada adjudicación sellada en `CALC-DIN-CREDITO-PREDICCION-2024-ADJUDICACION-0001` exista como celda-D en `data/curacion-registro/celdas-d/`, con el contrato celda-D (ADR-68) completo: emisión sellada antes (COMMIT-1/2 del acto de predicción), R después (ENIF 2024), veredicto con vocabulario cerrado, marcador PROSPECTIVA o RETROSPECTIVA según el orden de sellos, y `champion_actual` = el que el CALC adjudicó. Habilita: que la métrica rectora cuente el producto de dinero (firma D3).
«Hecho» sobre el commit final: `ls data/curacion-registro/celdas-d/ | grep -c '^DIN\.'` = número de celdas-D nuevas declarado en la nota (≤ 36; las que no se registren llevan NC con razón) · `python3 tools/corrida0.py status | grep celdas_validadas` mayor que el valor de arranque en exactamente ese número · cada yaml cita el RESULT del CALC por id y hash · `check.py --baseline` VERDE.

## 2 · FIRMAS DE MESA (23/sep/2026, verbatim del chat de dirección; entran al repo por GEN2-TRAMITE-FIRMAS-11 — este encargo las cita, no las asienta)
- **D1** «Integrar los dos, nada es fuera de plazo, todo se utiliza.» (#1030 y #1031 se fusionan; las cuatro emisiones ENVIPE de Astra se adjudican contra la R del piloto 4.)
- **D3** «Que cuenten.» (las adjudicaciones de crédito entran a celdas_validadas vía celda-D)
- **D4** «A, desde ya.» (main exige check.py VERDE; merge queue; el token de Actions fusiona solo PR de rutina: `claude/encola-*`, `acto/gen2-tramite-*`, `[deriva]`; lo que mide lo fusiona mesa)
- **D5** «Ya tengo un disco duro, necesito reformatearlo para dejarlo listo, no ahora, esta semana sí; vence el domingo de esta semana.» (27/sep/2026)
- **D6** «A.» (la vía (i) de relevo lee el eje RESULTADO; CONTEXTO en la nota del pin)
- **D7** «A.» (acto de MOTOR autorizado a editar `milpa/src/motor.py` en las líneas de NC …e8fa-01; los sellos afectados se suceden por CALC nuevos)
- **D8** «A, pero que se explique claramente qué significa.» (INDETERMINADO es valor válido; se define por escrito)
- **D2** no es firma: es una pregunta de mesa («¿por qué seguimos haciendo piloto del piloto?») que contesta el encargo DUELO-ENCIG2025-CIERRE-1 con su firma §2 propuesta.

## 3 · LO QUE DIRECCIÓN SABE
- `[LEÍDO]` NC `…DIN-CREDITO-ESCOLARIDAD-2-0af9-02`: «ADJ16 selló 4 celdas × 9 conductas con veredicto; `_celdas_validadas` sólo lee marcador y celdas-D» — decisión de mesa pendiente; D3 la da.
- `[EXISTE]` `data/corrida0/CALC-DIN-CREDITO-PREDICCION-2024-ADJUDICACION-0001/` (sello, resultados). `[EXISTE]` 6 yaml en `celdas-d/` como patrón de formato (p. ej. `GOB.gobierno_digital.encig2025.edad_x_escolaridad.yaml`, con `champion_actual`, `estado_operativo`, bloque de reserva). `[LEÍDO]` `tools/tablero_programa.py` `_celdas_validadas`: lee esos yaml (grep de la función al redactar; **cita las líneas tú**).
- `[SUPUESTO]` que el orden de sellos del acto de predicción (COMMIT-1 `2026-09-21-GEN2-DIN-CREDITO-PREDICCION-2024-COMMIT-1.md`, COMMIT-2-3 del 22/sep) demuestra emisión antes de abrir ENIF 2024 → PROSPECTIVA. Si el diff muestra que ENIF 2024 se leyó antes del sello de emisión, RETROSPECTIVA-MECÁNICA y se dice. No se colapsan.
- `[SUPUESTO]` cuál es la unidad de celda: 4 «celdas» de la NC son cruces (p. ej. escolaridad × formalidad) y 9 «conductas» son estimandos; una celda-D por (cruce, conducta) = 36, o por cruce = 4 con 9 estimandos cada una. **Léelo del contrato celda-D (ADR-68) y de cómo cuentan las celdas-D de ENVIPE del piloto 4; declara cuál y por qué antes de escribir el primer yaml.** Contar 36 donde el contrato dice 4 sería inflar la métrica.
- ADJUNTOS: ninguno.

## 4 · YA HECHO / YA DECIDIDO
`ls data/curacion-registro/celdas-d/ | grep -ci 'DIN\|credito'` → 0. `git grep -l 'PREDICCION-2024-ADJUDICACION' origin/main -- data/curacion-registro` → reporta.

## 5 · PIEZAS
- **P1 · Unidad y orden.** Decide la unidad (§3, cuarto punto) leyendo ADR-68 y las celdas-D del piloto 4; verifica el orden de sellos por diff; escribe en la nota la tabla RESULT → celda-D antes de crear archivos.
- **P2 · Yaml por celda-D.** Mismo esquema que las existentes; campos: estimando, universo (persona 18–70, recorte ff56-01 (a)), emisión (CALC, RESULT id, hash), R (CALC, RESULT id, hash), veredicto (vocabulario del CALC), marcador PROSPECTIVA/RETROSPECTIVA, `champion_actual` (el del CALC), `estado_operativo` según contrato, `registrado_por: GEN2-DIN-CREDITO-CELDAS-D-1`. Ningún número tecleado: todos por id y hash.
- **P3 · Derivación y prueba.** `status` antes/después; test huérfano que falle si un yaml cita un RESULT inexistente; NC por cada celda no registrable con razón (NO-CONSTRUIBLE, unidad discordante, veredicto ausente).

## 6 · LATITUD
Formato libre dentro del esquema existente. Pregunta a mesa (sigues): si el contrato celda-D no admite un estimando de unidad «crédito» o «persona-conducta» sin cambio de esquema.

## 7 · PAROS — lista cerrada
a) no aplica · b) editar un CALC sellado o un yaml de celda-D ajeno · c) escribir `marcador-segmento.tsv` a mano o cambiar `champion_actual` respecto al CALC · d) no aplica · e) CAJA · f) las celdas-D ya existen.

## 8 · COMPUERTAS
«Unidad declarada en la nota antes del primer yaml» protege: **adoptar** (la métrica rectora). «Todo número por id y hash» protege: **congelar** (E.2).

## 9 · PERÍMETRO Y CONCURRENCIA
Propio: `data/curacion-registro/celdas-d/DIN.*.yaml` (nuevos), test propio, `no-corrido.tsv` (append), nota, L0, cascada. Ajeno: CALC, marcador, `tablero_programa.py` (si `_celdas_validadas` necesita cambio, es NC a TUBERÍA, no edición). En vuelo: FIRMAS-11, ASTRA-ENVIPE-ADJUDICACION-1 (toca celdas-D del piloto 4, no las tuyas), AUTOMERGE-2; union en TSV.

## 10 · LO QUE NO HACE · SUCESORES
No re-mide, no adopta, no toca la serie de crédito. Sucesor: `GEN2-DIN-CREDITO-SERIE-LECTURA-1` cita estas celdas-D. Auditoría de rigor extremo: no carga (registro), pero cada yaml lleva unidad y escala.

## NO-CORRIDO / RESERVAS

- **P1/P2/P3 (unidad, yaml por celda-D, derivación/prueba) — el encargo entero.** `PARO-PREMISA`. Verificado por comando antes de escribir ningún yaml: `CALC-DIN-CREDITO-PREDICCION-2024-ADJUDICACION-0001` (la fuente que §1/§3 citan para las 36 adjudicaciones) tiene 882 `RESULT` y **cero** terminan en `VEREDICTO` — no adjudica nada, `python3 -c "import json; d=json.load(open('data/corrida0/CALC-DIN-CREDITO-PREDICCION-2024-ADJUDICACION-0001/resultados.json')); print(len([k for k in d['resultados'] if k.endswith('VEREDICTO')]))"` → `0`. Las adjudicaciones reales de crédito 2024 viven en `CALC-DIN-CREDITO-PREDICCION-2024-ESCOLARIDAD-0002` (bloque `ADJ16`, 28 `VEREDICTO`, citado en `NC-260922-GEN2-DIN-CREDITO-ESCOLARIDAD-2-0af9-02`) — cuyo propio `spec.yaml` declara que sucede **solo el eje escolaridad** del `-0001` — y esos 28 veredictos están agregados por (conducta × candidato) sobre las celdas puntuadas del bloque, con 7 tags de conducta (`K1, K2, K3, K4A, K4B, K5, K6`; no hay `K7`/`K8`/`K9`) y **sin desagregación por celda de escolaridad**. No hay 36 adjudicaciones de las que derivar 36 celdas-D bajo ningún CALC sellado hoy. Impacto: 0 de ≤36 celdas-D registradas; `celdas_validadas` sin cambio (92 → 92); la métrica rectora (firma D3) sigue sin ver crédito 2024. Sucesor: `DECISION-DE-MESA-PENDIENTE` — mesa declara (a) la unidad correcta de celda-D para crédito 2024 (por conducta agregada sobre las 16 celdas del bloque `ADJ16`, que es lo que el veredicto sellado realmente produce, o una desagregación más fina que exigiría re-medir) y (b) cuál CALC es la fuente vigente para las 12 celdas no-escolaridad del `-0001`, que tampoco tienen veredicto propio hoy. Fila `NC-260923-GEN2-DIN-CREDITO-CELDAS-D-1-e6b2-01`.

## CONSUMIDO
PR (pendiente) — `ACTO GEN2-DIN-CREDITO-CELDAS-D-1`. PARO-PREMISA, cero celdas-D registradas, cero adopción. Ver `NC-260923-GEN2-DIN-CREDITO-CELDAS-D-1-e6b2-01`, `canon/gobernanza-v1_15.md` `ADR-260923-GEN2-DIN-CREDITO-CELDAS-D-1-e6b2-01`, `canon/L0/ADR-260923-GEN2-DIN-CREDITO-CELDAS-D-1-e6b2-01.md`.
