# ENCARGO · ACTO GEN2-CONTADORES-CONSUMO-2 · El marcador entra al canal (P-A que CONTADORES-1 dejó por decisión de mesa): acredita `origen_numerico` de los dos CALC de gobierno digital, resuelve los FAIL de línea base uno por uno, y `adoptados_activos` deja el 72

> ENTORNO: **NUBE**. Hook imprime ENTORNO-DERIVADO; si dice CAJA, PARA.

CABECERA · SHA de redacción `6a2cd6c7` (re-deriva al abrir) · una sola sesión, rama propia `acto/gen2-contadores-consumo-2` (D-17) · MODELO: Opus · MODO: ABIERTO · ids con raíz de acto (D-24) · D-21 aplica · «Si te encuentras escribiendo fuera de la lista de §9, PARA.» · cierre por /acto: `## NO-CORRIDO / RESERVAS` («Ninguno.» obligatorio si aplica) y `## CONSUMIDO` al pie.
CONTADOR: cero mediciones; `adoptados_activos` se mueve solo por el derivador sobre adopciones ya firmadas (#1002 ENVIPE, #1009 ENIF con reserva, F3 gobierno digital); antes/después en la nota; nada a mano.

## 1 · OBJETIVO
Cerrar la mitad que CONTADORES-1 (#1078) no pudo: el marcador sigue sin publicarse (FP `…657c-04`) porque al entrar sus RESULT al registro, `CALC-GOB-DIGITAL-EXE-EMISIONES-0002` y `CALC-GOB-DIGITAL-EXE-ADJUDICACION-0001` caen en NO_APTA por no tener fila `origen_numerico` en `decisiones.tsv` (FP `…988c-01`). Con la firma de §2, se acreditan, se añade `marcador_segmento.py --escribe` al paso de derivados de `verify.yml` (quitando la exclusión de #1050), se resuelven los FAIL de línea base con cita uno por uno, y el siguiente PR `[deriva]` publica el marcador. Cierra también las tres filas RESERVADA fantasma de ENCIG 2025 en el TSV.
«Hecho» tras fusionar este PR y el siguiente `derivados/auto-*`: `status` en clon fresco con `adoptados_activos` > 72 (valor del derivador, citado) · `grep -c marcador_segmento .github/workflows/verify.yml` ≥ 1 en el paso de derivados · `grep -c RESERVADA` filtrado a ENCIG 2025 en `marcador-segmento.tsv` → 0 · `decisiones.tsv` con las dos filas nuevas · `check.py --baseline` VERDE sin `--force`.

## 2 · FIRMAS DE MESA (propuesta; mesa la da verbatim al lanzar; sin ella §7 f)
«Se acredita `origen_numerico` de `CALC-GOB-DIGITAL-EXE-EMISIONES-0002` y `CALC-GOB-DIGITAL-EXE-ADJUDICACION-0001` según sus inputs (manifiesto = NUEVO; otros CALC sellados = HEREDADO; constancia = HEREDADO), con fila en `decisiones.tsv` citando FP-260923-GEN2-CONTADORES-CONSUMO-1-988c-01. Los FAIL de línea base que describen el marcador viejo se actualizan con cita; uno que proteja una medición vuelve a mesa.»

## 3 · LO QUE DIRECCIÓN SABE
- `[LEÍDO]` NO-CORRIDO de #1078: P-A completa quedó DECISIÓN-DE-MESA-PENDIENTE tras verificar la premisa; P-B(2) parcial: el sufijo `-D-C2` fuera de ENCIG 2025 quedó FUERA-DE-PERÍMETRO (autorizado solo para #1060) — **aquí se autoriza** generalizarlo con la misma regla, declarándolo. `[LEÍDO]` FP `988c-01`: los inputs de los dos CALC son uno de manifiesto (NUEVO), varios de repo (HEREDADO) y uno de constancia.
- `[EJECUTADO]` `status` a `6a2cd6c7`: adoptados 72; `celdas_validadas` 219. FIRMAS-10 midió 87 en local con el derivador (23/sep).
- `[SUPUESTO]` que los «21 FAIL de línea base» (#1050) siguen siendo aserciones de estado; CONTADORES-1 los listó en su nota (**cítala**; si no los listó, los listas tú antes de tocar nada).
- ADJUNTOS: ninguno.

## 4 · YA HECHO / YA DECIDIDO
`grep -c 'GOB-DIGITAL-EXE-EMISIONES-0002' milpa/decisiones.tsv` → reporta (esperado 0). `grep -c marcador_segmento .github/workflows/verify.yml` → reporta (esperado 0).

## 5 · PIEZAS
- **P1 · Acreditación.** Dos filas en `decisiones.tsv` con la firma de §2 verbatim; `corrida0.py registro --verifica` en rama debe dejar de marcar NO_APTA (salida pegada).
- **P2 · FAIL de línea base.** En rama: `marcador_segmento.py --escribe`, `check.py --baseline`; tabla FAIL × causa; aserciones de estado actualizadas con cita al acto que las hizo verdad; una que proteja medición → PARA esa aserción y FP.
- **P3 · Canal.** `verify.yml`: `marcador_segmento.py --escribe` en el paso «Deriva vistas y abre PR automático»; quitar la exclusión de #1050; `derivados_protegidos.py` sigue impidiendo el commit manual.
- **P4 · Sufijo `-D-C2` general** (P-B(2) de CONTADORES-1) y cierre de `…657c-04`, `…988c-01`, NC de CONTADORES-1.

## 6 · LATITUD
Orden libre. ≤ 10 líneas adyacentes: sí. Pregunta a mesa (sigues): solo por un FAIL que proteja medición.

## 7 · PAROS — lista cerrada
a) no aplica · b) commitear el marcador a mano, `--force`, `--excluye`, editar `registro`, bajar una aserción que proteja medición · c) mover contadores a mano · d) no aplica · e) CAJA · f) mesa no dio la firma, o el marcador ya se publica por el canal.

## 8 · COMPUERTAS
«Acreditación solo con la firma verbatim en `decisiones.tsv`» protege: **adoptar**. «Marcador solo por el job» protege: **adoptar**. «FAIL que protege medición → mesa» protege: **borrar**.

## 9 · PERÍMETRO Y CONCURRENCIA
Propio: `milpa/decisiones.tsv` (dos filas), `.github/workflows/verify.yml` (paso de derivados), tests con aserciones de estado del marcador, `tools/celdas_validadas.py` + spec (solo P4), `firmas-pendientes.tsv`/`no-corrido.tsv`, nota, L0, cascada. Ajeno: `marcador_segmento.py`, `registro`, CALC, celdas-D. En vuelo: AUDITORIA-POST-HOC-ASTRA-1, MOTOR-DEUDA-LOTE-2, Astra (no tocan esto).

## 10 · LO QUE NO HACE · SUCESORES
No adopta estimadores nuevos; no toca `-D-C2` fuera de lo que P4 declara. Sucesor: ninguno si «Hecho»; FIRMAS-14 asienta el nuevo valor.
