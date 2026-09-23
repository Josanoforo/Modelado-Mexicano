# ENCARGO · ACTO GEN2-TRAMITE-FIRMAS-9 · Tres asientos que la máquina no hace sola: el CONSUMIDO que #1026 no dejó, la celda-D adjudicada que el marcador sigue mostrando RESERVADA, y la fila de mesa que falta para las tres líneas de 8e53-04

> ENTORNO: **NUBE** — cero microdato, cero corridas. Hook imprime ENTORNO-DERIVADO; si dice CAJA, PARA en una línea.

CABECERA · SHA de redacción `619748f5` (re-deriva al abrir; main movido no es PARO) · una sola sesión, rama propia `acto/gen2-tramite-firmas-9` (D-17) · MODELO: Sonnet · MODO: **ABIERTO** · CONTADOR: cero mediciones; **no adopta**; no toca `cuenta_gen2`; el único derivado que puede moverse es `marcador-segmento.tsv` por su propio derivador (P2) · ids con raíz de acto (D-24).

## 1 · OBJETIVO
Que `origin/main` deje de contradecirse en tres sitios que hoy se leen a mano: (P1) el encargo de SECUNDARIA-1 fusionado en #1026 sin `## CONSUMIDO`; (P2) la celda-D `GOB.gobierno_digital.encig2025.edad_x_escolaridad` con `champion_actual: C2` y reserva levantada en su yaml, mientras `marcador-segmento.tsv:208` la publica `RESERVADA · EMITIDA-SIN-EVALUAR · SIN-PISO`; (P3) las tres líneas de 8e53-04 (protección de `main`, merge queue, quién fusiona) pendientes de mesa sin fila en `firmas-pendientes.tsv` (A.12). Habilita: que el piloto 5 y el recibo de Astra lean el estado de ENCIG del marcador y no del yaml, y que mesa vea 8e53-04 en su tablero.
«Hecho» = sobre el commit final con `origin/main` fusionado: `grep -c '^## CONSUMIDO' forense/encargos/2026-09-22-GEN2-DIN-LOTE-ENIF2024-SECUNDARIA-1.md` → 1 · la fila `CRUCE-GRUPO::tramite.gobierno_digital.util_sin_coercion_ejes_encig2025::edadxescolaridad` de `data/corrida0/marcador-segmento.tsv` ya no dice `RESERVADA` en su columna de estado, **o** la nota explica por qué el derivador no puede leer la adjudicación y la NC nombra el sucesor · `awk -F'\t' '$1 ~ /8e53-04/ && $6 ~ /^ABIERTA/' forense/firmas-pendientes.tsv` → 1 fila.

## 2 · FIRMAS DE MESA
Ya selladas, se citan: F3 21/sep (cuaderno §2.2, `forense/encargos/CUADERNO-DE-MESA-2026-09-21.md`, #963: adopta el piso C2 de `gobierno_digital` como champion; asentado por `GEN2-TRAMITE-FIRMAS-5`) — está en el yaml de la celda-D, línea 86. Ninguna nueva. **P3 no firma nada: registra que falta la firma.**

## 3 · LO QUE DIRECCIÓN SABE
- `[EJECUTADO]` `grep -c CONSUMIDO forense/encargos/2026-09-22-GEN2-DIN-LOTE-ENIF2024-SECUNDARIA-1.md` → 0; `git log --oneline --grep SECUNDARIA` → `d34b70e1 Merge pull request #1026 …secundaria-1`. Cola del archivo: termina en `## 10 · NO HACE · SUCESORES · CIERRE`. **No sé** si tiene `## NO-CORRIDO / RESERVAS` (A.14 exige los dos bloques; si falta, va también, con «Ninguno.» si procede — lee la nota de cierre de #1026 antes de escribirlo).
- `[LEÍDO]` `data/curacion-registro/celdas-d/GOB.gobierno_digital.encig2025.edad_x_escolaridad.yaml`: l.84 «la reserva se LEVANTÓ en el COMMIT-3 … el par edad×escolaridad de marcador-segmento.tsv deja de estar RESERVADA (re-derivado por comando)»; l.86 `champion_actual: C2` con la firma F3. `[EJECUTADO]` `marcador-segmento.tsv:208` columnas 9–11: `RESERVADA · EMITIDA-SIN-EVALUAR · SIN-PISO`. Contradicción en main, no en una rama.
- `[LEÍDO]` `tools/marcador_segmento.py`: l.16 dice que lee `celdas-d/*.yaml` con `champion_actual: C2`; l.969–972 y l.1081 (`assert f["estado"] == "RESERVADA"`) vienen de `GEN2-C2-COMPUESTO-RESERVADAS-1` («un cruce emitido sigue RESERVADA para evaluación»). Hipótesis de dirección, `[SUPUESTO]`: `GEN2-MARCADOR-CONSUMO-Y-ADOPCION-2` (#1025) cableó el consumo de adjudicaciones para ENIF y ENUT y no incluyó esta celda-D de ENCIG, o el assert de l.1081 gana sobre la adjudicación. Si es otra cosa, el hallazgo es tuyo.
- `[EJECUTADO]` `grep 8e53 forense/firmas-pendientes.tsv` → 3 filas, todas FIRMADA, ninguna es 8e53-04; `forense/encargos/2026-09-22-GEN2-TUBERIA-RUTINAS-AUTOMERGE-1.md:19` cita «NC TUBERIA-CIERRE-SIN-CHOQUE-2-8e53-04 (protección de rama) ABIERTA». Es un pendiente de mesa que vive como NC y no como FP.
- `[EXISTE]` `forense/encargos/2026-09-22-GEN2-TRAMITE-FIRMAS-8.md` y `-ADENDA-1.md` (#1027, #1029): el trámite anterior; patrón de asiento.
- ADJUNTOS: ninguno.

## 4 · YA HECHO / YA DECIDIDO
`git log --oneline e5b424c4..619748f5` → solo #1028 (lote estricto) y un dedup de CI; ninguno toca los tres objetos. `git grep -n 'gobierno_digital' origin/main -- forense/encargos/2026-09-22-GEN2-MARCADOR-CONSUMO-Y-ADOPCION-2.md` → reporta (dirección no lo leyó: **léelo tú antes de P2**, es el acto que debió consumir esta adjudicación). Ramas vivas: piloto 4 (caja, no toca ENCIG), dos de Astra (no tocan marcador). **Repítelo tú.**

## 5 · PIEZAS
- **P1 · CONSUMIDO de SECUNDARIA-1.** Append al pie del encargo archivado: `## NO-CORRIDO / RESERVAS` (si falta; contenido derivado de la nota de cierre de #1026, con sus NC citadas por id) y `## CONSUMIDO` citando PR #1026 y su ADR de raíz. Nunca se edita nada arriba de la línea de append (A.3: el sello de cuerpo no se regenera). Hallazgo en `hallazgos.md`: acto fusionado sin marcador; una línea.
- **P2 · El marcador consume la adjudicación de `gobierno_digital`.** Primero lee el encargo y la nota de #1025 (qué cableó y para qué instrumentos). Luego una de tres ramas, y dices cuál: (i) es configuración (una entrada en el yaml de consumo que #1025 instaló) → la añades, regeneras `marcador-segmento.tsv` por su comando, y la fila 208 cambia; (ii) es el assert de l.1081 (el compuesto exige RESERVADA aunque exista champion) → defecto adyacente: si cabe en ≤ 10 líneas, se arregla y se declara; si no, NC `DIFERIDO-A` con sucesor nombrado `GEN2-MARCADOR-CONSUMO-Y-ADOPCION-3` y la nota dice qué cambiaría; (iii) el yaml de la celda-D es el que está mal (la reserva no se levantó de verdad) → PARA esa pieza (§7 b: no se edita un yaml adjudicado) y va a mesa con cita. Sea cual sea la rama: `adoptados_activos` puede moverse solo si el derivador lo hace por sí mismo con `champion_actual` ya firmado — se reporta antes/después; **no se toca a mano**.
- **P3 · Fila FP para 8e53-04.** Una fila ABIERTA en `firmas-pendientes.tsv` con id de raíz de este acto, `qué_se_firma` = las tres líneas verbatim del NC 8e53-04 (léelas en `no-corrido.tsv`, cita fila), `gatea` = «AUTOMERGE-1 (#1022) instalado y apagado; e889-01 ya FIRMADA no basta sin ellas», `encargo` = este. La NC 8e53-04 sigue ABIERTA y cita la FP nueva en su campo de sucesor (append, no edición).

## 6 · LATITUD
DECIDES TÚ: orden, si P2 va primero por ser la que puede mover contador, formato de la nota. Obstáculos reversibles: `pyyaml`, regenerar derivados por comando, corregir una cita rota. ≤ 10 líneas adyacentes: sí, declarado.
PREGUNTAS A MESA (sigues con lo demás): solo si P2 cae en (iii). Recomendación de dirección si ocurre: mesa confirma o borra la línea 84 del yaml por escrito; nada se edita mientras tanto.
NO DECIDES: nada de §7.

## 7 · PAROS — lista cerrada
a) no aplica (cero microdato) · b) editar un yaml de celda-D adjudicado, un `spec.yaml` sellado o cualquier cosa arriba de la línea de append de un encargo archivado · c) adoptar, o mover `adoptados_activos` / `cuenta_gen2` a mano · d) no aplica · e) CAJA · f) los tres objetos ya están asentados en `origin/main` → PARO, y decirlo es el entregable.

## 8 · COMPUERTAS
«P2 no edita `marcador-segmento.tsv` a mano: solo su derivador lo escribe» protege: **adoptar** (una fila escrita a mano sería una adopción sin decisión). «P3 no marca FIRMADA nada» protege: **adoptar** (la firma no existe todavía). Lo demás es orden sugerido: P2 → P1 → P3.

## 9 · PERÍMETRO Y CONCURRENCIA
Propio: `forense/encargos/2026-09-22-GEN2-DIN-LOTE-ENIF2024-SECUNDARIA-1.md` (append al pie únicamente) · el yaml/config de consumo que #1025 instaló (P2 rama i) · `tools/marcador_segmento.py` solo bajo rama (ii) ≤ 10 líneas · `data/corrida0/marcador-segmento.tsv` por derivador · `forense/firmas-pendientes.tsv` y `forense/no-corrido.tsv` (append) · `hallazgos.md` · nota · `canon/L0/<ADR-raíz>.md` · cascada. Ajeno: celdas-D · CALC · `tramite.yaml` · `verify.yml`/`check.py` (D-21: test propio como huérfano).
Archivos que OTRO ACTO EN VUELO está tocando: piloto 4 (caja) hace append en `firmas-pendientes.tsv`; `GEN2-RECIBO-ASTRA-1` (nube, en paralelo) hace append en `firmas-pendientes.tsv`, `no-corrido.tsv`, `hallazgos.md`. Todos son union: si choca, `git merge-file --union` local, nunca el editor web.
«Si te encuentras escribiendo fuera de esta lista, PARA.» Perímetro de cierre permanente (D-21) aplica.

## 10 · LO QUE NO HACE · SUCESORES · CIERRE
No mide, no adopta, no firma, no relanza AUTOMERGE-1, no toca el piloto 4 ni a Astra. Sucesores: `GEN2-TUBERIA-RUTINAS-AUTOMERGE-1` relanzado cuando mesa firme la FP de P3; `GEN2-MARCADOR-CONSUMO-Y-ADOPCION-3` si P2 cae en (ii) grande; `GEN2-CELDA-D-PILOTO-5-ENCOGIDA-ENCIG-1` lee el marcador ya consistente. Auditoría de rigor extremo: no carga (papeleo). Cierre por /acto: `## NO-CORRIDO / RESERVAS` y `## CONSUMIDO` al pie; adendas como `<este-encargo>-ADENDA-N.md`.

## NO-CORRIDO / RESERVAS

- Ninguno.

## CONSUMIDO

Ejecutado por PR [#1032](https://github.com/Josanoforo/Modelado-Mexicano/pull/1032), ACTO GEN2-TRAMITE-FIRMAS-9, 23/sep/2026. `ADENDA-1` (P4/P5, `forense/encargos/2026-09-22-GEN2-TRAMITE-FIRMAS-9-ADENDA-1.md`) recibida con el acto ya cerrado; ejecutada sobre el mismo PR #1032, `ADR-260923-GEN2-TRAMITE-FIRMAS-9-97dc-02`.
