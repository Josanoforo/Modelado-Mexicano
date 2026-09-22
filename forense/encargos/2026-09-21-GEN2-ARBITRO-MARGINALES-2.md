# ENCARGO · ACTO GEN2-ARBITRO-MARGINALES-2 · LO QUE QUEDA DEL ÁRBITRO GEN1 SE RE-MIDE EN GEN2 O SE DICTAMINA: ENCUCI, EDER, LAPOP, ENIGH, ENFIH, ENNViH Y LOS ELECTORALES

> ENTORNO: **CAJA**. NO es NUBE.
CABECERA · SHA de redacción `99a43faf`; una sesión, rama `acto/gen2-arbitro-marginales-2` · LOTE (D-11; más de un PR si hace falta) · MODO ABIERTO hasta cada COMMIT-1 · CONTADOR: sella corridas; `cuenta_gen2 = SI`; no adopta. **L0 de `canon/estado-programa-v1_14.md`: si choca al fusionar, toma la de `main` y re-inserta solo tu anotación; `canon/L0/` existe.**
**MODELO: Sonnet por mandato de mesa (presupuesto).** El procedimiento está congelado o es receta; tu latitud es logística. Toda duda entre dos interpretaciones del procedimiento se pregunta a mesa en una línea, con opciones; no se resuelve.
NO tocar (TUBERÍA): `tests/check.py`, `tools/cierre_acto.py`, `tools/tablero_programa.py`, `.github/workflows/`, `.claude/commands/`. Cierre: `tests/check.py --rapido` antes de empujar; la suite completa la corre el CI (firma 21/sep). Derivados («DERIVADO — NO EDITAR») no se commitean: los re-deriva el job de main (`#984`).

## 1 · OBJETIVO
`ARBITRO-MARGINALES-1` (`#971`) re-midió en GEN2 los 13 marginales del árbitro que dependían de ENIF 2024, ENVIPE 2025 y ENCIG 2025, y dejó 57 pisos evaluados. Quedan **40 reglas** en `milpa/tramite-ola5-propuesta-v0.yaml` (GEN1): 15 sin payload declarado, ENCUCI 2020 (4), EDER 2017 (3), LAPOP 2019 (3), ENNViH (1), ENIGH 2022 (1), ENFIH 2019 (1), y 3 electorales sobre cómputos por municipio. Mientras sigan GEN1, todo lo que el emisor copia de ahí es `IDENTICO` y cuenta como legacy (`legacy_activas_por_consumidor__procedencia = 40`). «Hecho»: cada regla con uno de tres destinos, por comando: `RE-MEDIDA` (CALC sellado GEN2 desde su payload, misma definición o `NO-CONSTRUIBLE` con texto), `SIN-PAYLOAD` (con la fila de adquisición que la traería), o `FUERA-DE-ALCANCE` (la regla no es un marginal de encuesta: electorales, LAPOP si su licencia no permite redistribuir); tabla de las 40; nota.

## 2 · FIRMAS — verbatim
3D (21/sep): «insumo-árbitro no impide contar (caso por caso) — «rec: a + b como demanda»»; «el insumo legacy es el árbitro, leído como control y como rejilla, no como fuente de la cifra». Piso adjudicado (17/sep). E.1 (v2.16): «GEN1 es historia, no autoridad […] un GEN1 que agregó de otro modo se re-mide desde el insumo crudo, no se reinterpreta.» D-22 ampliada (v2.16, ya vigente): preflight VERDE con main fusionado · `_valida_outputs` en cada rama terminal, celda rara incluida, sobre sintético y oro · todo nulo posible declarado, None y NaN · ningún input sobre archivo vivo. **«Las corridas de este acto cuentan» — el lanzamiento es el sello.**

## 3 · LO QUE DIRECCIÓN SABE (contra `99a43faf`)
- `[EJECUTADO]` conteo por `payload_manifiesto_id` de las 53 reglas: `None` 15 · `enif_2024…` 5 · `envipe2025_csv` 4 · `encuci2020_bd_dbf` 4 · `encig25…` 4 · `eder_2017…` 3 · `lapop…2019` 3 · un ENNViH con nota larga · `enigh2022_nc_csv` 1 · `enfih2019…` 1 · electorales 3. Las 13 de ENIF/ENVIPE/ENCIG las cubrió `#971`: cita, no re-midas.
- `[EJECUTADO: marcador]` EDER 2017: 4 `IDENTICO` + 4 `SIN-PISO`; ENUT 2024: 11 `SIN-PISO` con la definición sellada (la de `#976` mide un núcleo común: **no es este acto** — mesa decide el rótulo). `[EXISTE]` molde: `#971` (specs y medidores por encuesta), `tools/ejes_maestra35_l1.py`.
- `[LEÍDO: #971 nota]` lo aprendido: rejilla y conducta leídas del piso o del árbitro por objeto, no tecleadas; nemónicos por texto de pregunta (A.15); una variable de agrupación; oro = reproducir un sellado existente.

## 4 · YA HECHO
Por objeto («ARBITRO-MARGINALES-2», «ENCUCI», «EDER», «LAPOP» en `data/corrida0/`): `#971` y el CALC ENCUCI del relevo (`test_relevo_encuci_f2`): cita lo sellado. Repítela tú.

## 5 · PIEZAS
**P1 · Clasificación de las 40**, por comando, en la tabla de §1, con el payload que cada una nombra y su estado en el manifiesto por id (A.15).
**P2 · Re-medición, una pieza por encuesta con payload en el corpus** (ENCUCI 2020, EDER 2017, ENIGH 2022, ENFIH 2019, ENNViH si el payload está): COMMIT-1 (spec + medidor; congelado por D-22 con oro: reproduce un sellado existente de esa encuesta o, si no hay, el propio GEN1 se declara como referencia RETROSPECTIVA y **no** como oro) → COMMIT-2 (`corrida0 run`).
**P3 · Discrepancias.** Por regla: GEN1 vs GEN2 en pp; las que difieran más que la tolerancia del tipo son hallazgo sobre GEN1 (no se corrige el YAML).
**P4 · Cierre.** Marcador y tablero por comando; cuántos `IDENTICO` dejan de depender de GEN1 (el emisor sigue copiando: eso es del relevo, no de este acto — dilo).

## 6 · LATITUD · 7 · PAROS
Latitud: agrupación, orden, cuántos PR. Pregunta a mesa siguiendo: si una regla GEN1 no tiene texto de pregunta reconstruible. PAROS: a) agrupar por dos variables una ola con cruces reservados · b) abrir `envipe2026*`, `enigh2024*` o crédito de ENIF 2024 · c) editar el YAML GEN1 o un sello · d) cambiar procedimiento tras su COMMIT-1 · e) `run` no sella → no se parcha. Compuerta: «COMMIT-1 con oro en verde» protege abrir dato. Perímetro: CALC nuevos y specs, tabla, filas propias, nota, cascada; ajeno: `milpa/`, sellos, celdas-D. `## NO-CORRIDO / RESERVAS` · `## CONSUMIDO`.

## NO-CORRIDO / RESERVAS

Ninguno. Las cuatro piezas que el encargo pidió (P1 clasificación, P2
re-medición, P3 discrepancias, P4 cierre) corrieron completas: P1 clasifica
las 40 reglas por comando; P2 sella COMMIT-1→COMMIT-2 en las 6 reglas que
genuinamente lo necesitaban (las otras 18 `RE-MEDIDA` ya estaban selladas
bajo GEN2, verificado, no re-medidas — E.5 "lo ya sellado se cita, no se
re-mide"); P3 compara las 24 `RE-MEDIDA` contra GEN1; P4 deriva el marcador y
el tablero por comando. Ningún PARO se disparó. La adopción de las 24
`RE-MEDIDA` (A-bis 6) y los actos sucesores por encuesta (ENDUTIH2025,
ICPSR-MPS2012, `list::mexico`, CIDE-CSES2015, remanente de ENIF2024) no son
piezas de este encargo — son recomendaciones a mesa (§6 de la nota de
cierre), no trabajo pedido y dejado sin correr.
