# ENCARGO · ACTO GEN2-ENCIG-PISOS-GEN2-1 · El piso contra el que se adjudicó el cierre de ENCIG 2025 venía de una cifra legacy: primero se cuenta cuántos pisos del programa tienen ese origen, luego se re-mide el de ENCIG 2023 desde microdato y se re-adjudica el cierre con un CALC sucesor

> ENTORNO: **CAJA** — microdato de ENCIG 2023 (abierto) para el piso; ENCIG 2025 solo para reproducir la R ya sellada por #1060 (cruce visto). Hook imprime ENTORNO-DERIVADO; si dice NUBE, PARA.

CABECERA · SHA de redacción `3d138c66` (re-deriva al abrir) · una sola sesión, rama propia `acto/gen2-encig-pisos-gen2-1` (o la que la plataforma fije: se declara en el 0-bis, D-19) · MODELO: Opus (mide; no bajar) · MODO: RÍGIDO en la adjudicación (hereda el procedimiento del duelo por sha); ABIERTO en P1 (censo) y logística · ids con raíz de acto (D-24) · D-21 aplica · «Si te encuentras escribiendo fuera de la lista de §9, PARA.» · cierre por /acto: `## NO-CORRIDO / RESERVAS` («Ninguno.» obligatorio si aplica) y `## CONSUMIDO` al pie.
CONTADOR: sella dos CALC (piso 2023 · adjudicación -0002), `cuenta_gen2: SI`, `adopta: NO`; no reescribe el -0001 (E.3: sucesor); `celdas_validadas` no cambia de número (las dos celdas-D ya cuentan), cambia de champion citado.

## 1 · OBJETIVO
T-REPRO(g) encontró que los 16 RESULT `-C2-P` de `CALC-ENCIG-DUELO-2025-ADJUDICACION-0001` (edad×sexo, escolaridad×sexo) se copian en `medidor.py:639` de un CALC sellado cuya cadena sube a `milpa/tramite.yaml` (legacy): origen HEREDADO, no adoptable. Tres piezas: (P1) **censo**: cuántas celdas-D y cuántos RESULT que el marcador consume como C2/champion tienen cadena de origen que pase por un archivo legacy — número, lista por id, y si es más de estas dos celdas, hallazgo del programa para el informe v1.3; (P2) **piso ENCIG 2023 medido desde microdato** para edad×sexo y escolaridad×sexo de gobierno digital (misma definición de celda que el duelo, por texto de pregunta), con IC de diseño y réplicas, origen NUEVO; (P3) **adjudicación -0002**: mismo procedimiento del duelo por sha, mismos contendientes, mismo umbral, con C2 = el RESULT de P2 por id; dictamen B-bis; celdas-D actualizadas con `champion_actual` citando -0002; las 16 celdas vuelven al marcador como medición.
«Hecho»: nota con la tabla del censo (P1: N celdas-D · N RESULT · lista) · `CALC-ENCIG2023-PISOS-GOBDIGITAL-0001` y `CALC-ENCIG-DUELO-2025-ADJUDICACION-0002` con sello, asiento y `verify` REPRODUCE · `decisiones.tsv` con `origen_numerico = NUEVO` para el piso citando este acto · los dos YAML de celda-D con `champion_actual` → -0002 · `check.py --baseline` con el marcador re-derivado en el árbol: 0 FAIL de T-REPRO(g) para esas 16 · `check.py --baseline` VERDE sin `--force`.

## 2 · FIRMAS DE MESA — dadas («firmado», 24/sep/2026), verbatim; viajan aquí y las asienta este acto
- **Decisión 1 de ADOPCION-2 (S):** «Las 16 celdas -C2-P de CALC-ENCIG-DUELO-2025-ADJUDICACION-0001 salen del consumo del marcador como medición, rotuladas «piso de origen legacy, no adoptable», hasta que un acto en caja re-mida el piso ENCIG 2023 desde microdato y re-adjudique el cierre con un CALC sucesor -0002 que cite ese piso por id; el acto cuenta primero cuántos otros C2 de celdas-D tienen origen HEREDADO de legacy.» (opción (ii) de FIRMAS-15 + re-medición; sustituye a S; cierra `FP-…-749c-01` y `FP-…-e0db-01`)
- Vigentes que se citan: firma 17/sep (piso no vencido = estimador adjudicado); E.6 (cruce visto sirve para evaluar en retrospectiva, rotulado); regla 6 (sin retadores nuevos: los contendientes son los del -0001, ninguno más).

## 3 · LO QUE DIRECCIÓN SABE
- `[LEÍDO]` Cierre de ADOPCION-2 (`forense/notas/2026-09-24-GEN2-ADOPCION-BLOQUE-Y-PINES-2-cierre.md`): la firma S aplicada da HEREDADO; motivo del FAIL «una medición GEN2 no adopta origen HEREDADO»; `medidor.py:639` (`out[f"{base}-C2-P"] = cand["C2"][c]`, copiado de `e.get(f"{be}-C2-P")`, el CALC de emisiones); `spec.yaml` del -0001: inputs `origen: manifiesto` ×1, `origen: repo` ×6.
- `[EJECUTADO]` `data/corrida0/decisiones.tsv` (`objeto · decision · fuente · fecha`): 32 filas NUEVO, 0 HEREDADO — el censo de P1 no sale de ahí: sale de seguir la cadena de inputs de cada CALC que el marcador consume (`registro --verifica` clasifica aptitud; T-REPRO(g) es el detector). Celdas-D ENCIG 2025: tres YAML (`edad_x_escolaridad` del piloto 3, `edad_x_sexo`, `escolaridad_x_sexo`). ENCIG 2023: 4 payloads en manifiesto.
- `[LEÍDO]` Procedimiento del duelo: `forense/prereg-caja/ENCIG-DUELO-2025-*` (spec humana + `spec.yaml`), medidor congelado en #1060. Se hereda por sha; el único cambio es la fuente de C2 (RESULT de P2 por id).
- `[SUPUESTO]` que el piloto 3 (edad×escolaridad) y los pisos de ENVIPE/ENIF del árbitro tienen C2 medido desde microdato (origen NUEVO). **P1 lo verifica; no se asume.**
- ADJUNTOS: ninguno.

## 4 · YA HECHO / YA DECIDIDO
`ls data/corrida0 | grep -c 'ENCIG2023-PISOS\|ENCIG-DUELO-2025-ADJUDICACION-0002'` → 0. #1060 sellado (no se toca). ADOPCION-2 (rama `claude/new-session-uq2blk`, PR pendiente de mesa) asentó S como HEREDADO: se cita.

## 5 · PIEZAS
- **P1 · Censo de origen** (nube o caja, sin microdato): para cada celda-D y cada RESULT que `marcador_segmento.py` consume como C2/champion, seguir `ejecucion.json` → inputs → CALC → … hasta un archivo de `milpa/` o `data/raw`; clasificar NUEVO / HEREDADO-DE-GEN2 / HEREDADO-DE-LEGACY; tabla en la nota; si HEREDADO-DE-LEGACY > 2 celdas, NC con `DIFERIDO-A: GEN2-PISOS-GEN2-2` y una línea para el informe v1.3.
- **P2 · Piso 2023, COMMIT-1 antes de abrir microdato** (D-22): spec humana + `spec.yaml` (celdas por texto de pregunta del cuestionario 2023, unidad trámite/persona declarada, factor y estratos, réplicas por diseño), medidor; COMMIT-2 con RESULT.
- **P3 · Adjudicación -0002**: spec que hereda la del -0001 por sha, `C2 := RESULT de P2`; corre sobre la R ya sellada (reproducir el oro del -0001, E.5); dictamen; celdas-D con `champion_actual` → -0002 y `comparaciones_secundarias` intactas; `decisiones.tsv` NUEVO; marcador re-derivado en el árbol (sin commitear) para probar T-REPRO(g).

## 6 · LATITUD
Logística libre; enmienda de cableado (D-18) antes de `ejecucion.json`. Pregunta a mesa (sigues con P1/P2): solo si el censo revela que el piloto 3 o el árbitro también heredan de legacy — con la lista y una recomendación.

## 7 · PAROS — lista cerrada
a) abrir ENCIG 2025 fuera de reproducir la R sellada, o cualquier ola reservada · b) reescribir el -0001, sus celdas-D o cualquier sello · c) adoptar; poner NUEVO a algo cuya cadena pase por legacy · d) cambiar umbral, contendientes o agregador del duelo · e) NUBE (para P2/P3) · f) el -0002 ya existe.

## 8 · COMPUERTAS
«COMMIT-1 del piso antes de abrir 2023» protege: **abrir dato**. «Procedimiento del duelo por sha; solo cambia la fuente de C2» protege: **congelar**. «NUEVO solo con cadena que termina en manifiesto» protege: **adoptar**.

## 9 · PERÍMETRO Y CONCURRENCIA
Propio: `forense/prereg-caja/ENCIG2023-PISOS-*`, `forense/prereg-caja/ENCIG-DUELO-2025-ADJUDICACION-0002-*`, `data/corrida0/CALC-ENCIG2023-PISOS-*`, `data/corrida0/CALC-ENCIG-DUELO-2025-ADJUDICACION-0002/`, los dos YAML de celda-D (`champion_actual`, `comparaciones_secundarias` append), `data/corrida0/decisiones.tsv` (append), `replay-evidencia.tsv`, `firmas-pendientes.tsv`/`no-corrido.tsv`, nota, L0, cascada. Ajeno: -0001 y sus RESULT, `medidor.py` de -0001, marcador (derivado), `milpa/`. En CAJA: REPLAY-NO-VERIFICADOS-1 (no comparte olas ni archivos). En nube: ADOPCION-3, CATALOGO-CONTRATO-Y-TEST-1.

## 10 · LO QUE NO HACE · SUCESORES
No adopta, no toca el motor, no releva legacy en otros pisos (`GEN2-PISOS-GEN2-2` si el censo lo pide). Sucesor: FIRMAS-16 asienta el hallazgo del censo; informe v1.3 lo cita.
