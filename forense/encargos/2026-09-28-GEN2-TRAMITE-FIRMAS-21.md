# ENCARGO · ACTO GEN2-TRAMITE-FIRMAS-21 · Asienta en el repo todo lo que mesa firmó en el chat de dirección el 28/sep sobre la hoja consolidada (21 renglones ya FIRMADA-EN-CHAT + los 57 que pedían firma), aplica los estados de reserva firmados en el manifiesto, cierra por objeto las 19 NC-pregunta de PENDIENTES-2 **decidiendo él mismo la opción reversible** bajo la delegación firmada, y ejecuta lo de forma (R52, R53) — sin abrir una NC nueva por nada que la cláusula de autonomía le permita resolver

> ENTORNO: **NUBE** — TSV de gobierno, manifiesto (campo `reserva`), catálogo de momentos (campo `rol_calibracion`), notas. Cero microdato. Hook imprime ENTORNO-DERIVADO; si dice CAJA, PARA.

CABECERA · SHA de redacción `3c55bfc5` (re-deriva al abrir) · una sesión, rama propia; PR por bloque (apertura · adopción/veto · contratos · NC-pregunta · forma) · MODELO: **Opus** (las 19 NC exigen leer el objeto y decidir) · MODO: **AUTÓNOMO-AMPLIO** (cláusula v1.0) · ids con raíz de acto · D-21 aplica.
CONTADOR: cero mediciones; no adopta cifras (las firmas de adopción/veto de esta hoja reciben reglas y fijan contratos: ninguna mueve `adoptados`). Mueve `firmas_pendientes_abiertas` hacia abajo y `no_corrido_abiertas` hacia abajo por cierres con cita; declara antes/después. **Prohibido abrir NC por bifurcación reversible**: se decide y se declara en la nota (cláusula §1–§4); NC solo por D-19.

## 1 · OBJETIVO
(P1) **Asiento.** Cada renglón de `forense/analisis/hoja-firmas-21/decisiones-21.tsv` con estado FIRMADA-EN-CHAT o PIDE-FIRMA queda FIRMADA en `forense/firmas-pendientes.tsv` (todos los `ids_fundidos`) con este PR y el texto de firma de §2 como firma; los `YA-CUBIERTA` y `SUPERADA` se cierran con su cita. Lo que otro acto ejecuta (CALC-ALTERNOS-LOTE-1, C1-SUCESORES-Y-LOTE-3) **no se asienta aquí**: se marca `VIAJA-EN <encargo>` (A.12) y lo asienta ese acto.
(P2) **Estados de reserva y HOLDOUT.** En `data/manifiesto.yaml`, campo `reserva` de las olas firmadas: ENCRIGE 2020 y ENVE 2024 → `ABIERTA-COMO-VISTA (firma R02/R03, este PR)`; CSES M5, ENDUTIH 2025, ENIF 2024 m7 → `RESERVADA`; CAAS 2015, ENGPEE 2010, MSM 2002 → reserva levantada por escrito (R09); ENCRIGE 2016 → vista. En `milpa/catalogo-momentos-v0_1.tsv`: columna nueva `holdout_decision` con `GASTABLE-COMO-PISO` / `RESERVADO-PARA-FAMILIA-2027 (familia)` según el expediente C2 (R01 (b)); la spec que consuma un HOLDOUT lo declara. Nada más del catálogo cambia.
(P3) **Las 19 NC-pregunta** (R16, R29, R30, R34–R45, R54–R57; ids en la tabla): abrir el objeto de cada una, redactar las opciones que faltaban, y **decidir**: reversible → se aplica, se cierra con cita y la nota lista «decidido por delegación: <opción> porque <razón>»; irreversible (D-19: sellos, reservas, contadores vedados, procedimientos congelados) → una sola hoja al cierre con opciones, no NC nuevas. Precedente que manda: R56/R57 (c6d9-01/02) son cerrables con cita según la hoja.
(P4) **Forma.** R52: nota en `corpus/reports-v2/INDICE.md` (por su productor) de que genómica va en inglés en v2 y se traduce en v3; R53: la cifra L8 del report de duelo marcada «pendiente de cotejo de fuente y corte» y los ROMPE clínicos rotulados como dice el texto de firma. R50: los 598 payloads residuales de licencias → sucesor CORPUS-LICENCIAS-2 registrado, no ejecutado aquí.

«Hecho», por comando sobre el commit final con `origin/main` fusionado: 0 renglones de `decisiones-21.tsv` con estado PIDE-FIRMA o FIRMADA-EN-CHAT sin asiento (cruce con `firmas-pendientes.tsv` por id) · las 9 olas con el campo `reserva` que la firma dice (lector YAML) · `holdout_decision` no vacío en M09–M23 · las 19 NC con `estado` CERRADA (cita) o en la hoja de cierre (ninguna «sigue abierta por falta de opciones») · `check.py --baseline` VERDE.

## 2 · FIRMAS DE MESA
Mesa, 28/sep/2026, chat de dirección (maestra 54), en respuesta al bloque de decisiones de dirección sobre la hoja consolidada: **«firmado»** — con INTERPRETACIÓN-DECLARADA en `ADENDA-1` (adjunta al lanzar): las opciones recomendadas renglón por renglón (R01 b · R02/R03 ABIERTA-COMO-VISTA · R04/R05/R06 RESERVADA · R07 b · R08 b · R09 a · R10 d · R11 2 · R12 a2/b1 · R13 1 · R14 etapa 1 · R15 1 · R17 2 · R18 1 · R19 1 · R20 2 · R21 2 · R22 1 · R23 2 · R24 2 · R25 1 · R26 2 · R27 2 · R28 1 · R31 firmar por sha · R32 A · R33 1 · R52 1 · R53 1 · R50 a · **delegación de las 19 NC-pregunta al trámite** · acceso de C1 a ENBIARE 2021 y ENCODAT 2016-17 delimitado como `ee49`), más las fechas que mesa dé para R46, R47, R49 y R51. Los textos de firma de cada renglón son los de `decisiones-21.tsv`, columna `texto_de_firma`, con la letra sustituida. Firmas previas ya en el repo: ADENDA-1 de HOJA-FIRMAS-21-1 (22 letras), ADENDA-1 de RECIBO-ASTRA6-2 (7 FP de Codex), beee-01/02.

## 3 · LO QUE DIRECCIÓN SABE
- [EJECUTADO] `3c55bfc5` · `decisiones-21.tsv`: 86 renglones — PIDE-FIRMA 57, FIRMADA-EN-CHAT 21, YA-CUBIERTA 7, SUPERADA 1; columnas `ids_fundidos`, `opciones`, `recomendacion`, `texto_de_firma`. FP ABIERTA 41; NC ABIERTA 509.
- [LEÍDO] `forense/encargos/2026-09-28-GEN2-ASTRA6-C1-LOTE-3.md` §NO-CORRIDO: las 312 residuales son ENBIARE 180, ENCODAT 130, ENCUCI 1, ENIGH 1 — no ENDIREH; PARO-PREMISA de entorno; reserva de aislamiento de red NO-VERIFICABLE-AQUÍ.
- [LEÍDO] Hoja consolidada: R56/R57 «forma, cerrables con cita»; R16, R29, R30, R34–R45, R54, R55: «el acto de origen dejó pregunta, no opciones».
- [EXISTE] `tools/consulta.py`, escritor de FP de TRAMITE-FIRMAS-20 (modelo), regenerador de `INDICE.md` (C3-1).

## 4 · YA HECHO / YA DECIDIDO — por objeto
`git ls-tree -r --name-only origin/main forense/encargos | grep -c 'TRAMITE-FIRMAS-21'` → 0 (HOJA-FIRMAS-21-1 produjo la hoja; no asentó). Consumidos: TRAMITE-FIRMAS-11…-20 (formato de asiento), PENDIENTES-2 (dejó las 19 preguntas), C1-LOTE-3, C2-EJECUCION-1, DEMANDA-DICTAMEN-1 (sus dictámenes se citan en las NC que toquen la demanda). En vuelo: CALC-ALTERNOS-LOTE-1 y C1-SUCESORES-Y-LOTE-3 (caja; asientan sus propias firmas; no tocar sus filas), el `[deriva]`.

## 5 · PIEZAS
P2 → P1 → P4 → P3 (las NC al final, con todo lo demás asentado). Rama prevista: renglón cuyo objeto ya cerró otro acto (A.17) → SUPERADA con cita; NC cuyo objeto ya no existe → CERRADA-POR-DISEÑO con el commit que lo retiró.

## 6 · LATITUD — amplia por firma
Todo lo reversible se decide aquí y se declara; orden, PR, formato: tuyos. PREGUNTA A MESA: una hoja al cierre con lo irreversible, si lo hay. NO DECIDES: nada de §7.

## 7 · PAROS — lista cerrada (D-19 estricta)
a) abrir dato · b) editar sellos, RESULT, emisiones, o un texto de firma · c) adoptar cifras; cambiar una opción firmada · d) no aplica · e) CAJA · f) objetivo inalcanzable.

## 8 · COMPUERTAS
«Un objeto, una fila; firma verbatim de la adenda» protege **adoptar** (A.12) · «Reservas solo como la firma dice» protege **abrir dato** · «Decidir lo reversible, no abrir NC» protege **borrar** (deuda que se multiplica).

## 9 · PERÍMETRO Y CONCURRENCIA
Propio: `forense/firmas-pendientes.tsv`, `forense/no-corrido.tsv` (las 19 + cierres con cita), `data/manifiesto.yaml` (solo campo `reserva` de las 9 olas), `milpa/catalogo-momentos-v0_1.tsv` (solo columna nueva), `corpus/reports-v2/INDICE.md` (por productor) y el report de duelo (solo L8 y rótulos ROMPE), `forense/analisis/hoja-firmas-21/` (estado), nota, L0, cascada. Ajeno: sellos, specs, `prereg-*`, vistas. «Si te encuentras escribiendo fuera de esta lista, PARA.»

## 10 · LO QUE NO HACE · SUCESORES · CIERRE
No mide, no adopta cifras, no ejecuta CALC ni C1 (los dos actos de caja), no envía solicitudes ni publica (mesa). Sucesores: CORPUS-LICENCIAS-2; FIRMAS-22 solo si queda algo irreversible. Sin módulo de auditoría. El cuerpo no lleva campos para rellenar; `## NO-CORRIDO / RESERVAS` («Ninguno.» obligatorio) y `## CONSUMIDO` las añade /acto. Adendas: `2026-09-28-GEN2-TRAMITE-FIRMAS-21-ADENDA-N.md`, selladas al recibirse.
