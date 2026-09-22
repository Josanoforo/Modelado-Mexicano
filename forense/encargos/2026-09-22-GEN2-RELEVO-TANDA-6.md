# ENCARGO · ACTO GEN2-RELEVO-TANDA-6 · EL REPLAY DEL CALC DE L SE ASIENTA (E.7) Y ENTONCES SÍ ENTRAN LOS DIECIOCHO PINES DE L

> ENTORNO: **NUBE** (cualquiera). Instala numpy/pandas si `verify` los pide. NO es CAJA.
CABECERA · SHA de redacción `99a43faf`; una sesión, rama `acto/gen2-relevo-tanda-6` · MODO ABIERTO · CONTADOR: legacy baja en exactamente lo pineado (hoy 146); `adoptados_activos` antes/después por comando. **L0 de `canon/estado-programa-v1_14.md`: si choca al fusionar, toma la de `main` y re-inserta solo tu anotación; `canon/L0/` existe.**
**MODELO: Sonnet por mandato de mesa (presupuesto).** El procedimiento está congelado o es receta; tu latitud es logística. Toda duda entre dos interpretaciones del procedimiento se pregunta a mesa en una línea, con opciones; no se resuelve.
NO tocar (TUBERÍA): `tests/check.py`, `tools/cierre_acto.py`, `tools/tablero_programa.py`, `.github/workflows/`, `.claude/commands/`. Cierre: `tests/check.py --rapido` antes de empujar; la suite completa la corre el CI (firma 21/sep). Derivados («DERIVADO — NO EDITAR») no se commitean: los re-deriva el job de main (`#984`).

## 1 · OBJETIVO
TANDA-5 (`#983`) paró en P2 por una premisa mía falsa: la guarda (a) rechazó los 18 pines porque `CALC-L-DESDE-CAPTURAS-v1_0` tiene `resultado_replay = NO-VERIFICADO` — el acto que lo selló (`#973`) no dejó asiento en `forense/replay-evidencia.tsv`, y E.7 dice que sin asiento no hay veredicto. «Hecho»: asiento de replay del CALC con veredicto en los dos ejes; los 18 pines `ACEPTADO`; FP F-L de TANDA-5 `FIRMADA`; el contador bajó exactamente en lo pineado; NC de TANDA-5 P2 cerrada.

## 2 · FIRMAS — verbatim, ya en el repo
F-L (TANDA-5, `forense/encargos/2026-09-22-GEN2-RELEVO-TANDA-5.md` §2): «Se pinean por la vía (i) las 18 lecturas L con cobertura completa (8 de 8 réplicas válidas): las seis CIV (M-01, 02, 04, 10, 12, 13) y las tres FAM (M-05, 06, 07), en sus dos variantes (L-solo y L+corpus), al RESULT de `CALC-L-DESDE-CAPTURAS-v1_0`. Las siete con abstención […] no se pinean.» E.7 (v2.16): «ningún veredicto de replay se publica sin asiento en `forense/replay-evidencia.tsv`». Vía (i) con eje RESULTADO: FIRMADA por `#983`.

## 3 · LO QUE DIRECCIÓN SABE (contra `99a43faf`)
- `[LEÍDO: encargo archivado de TANDA-5, ## NO-CORRIDO]` P2 `PARO-PREMISA`: «la guarda (a) rechaza los 18 porque el registro deriva `resultado_replay = NO-VERIFICADO` para ese CALC». P3 `SUSTITUIDO-POR TANDA-3`: las ocho `CALC-R` ya estaban pineadas; **no hay P3 aquí**.
- `[EXISTE]` `CALC-L-DESDE-CAPTURAS-v1_0` sellado (`#973`), inputs = 224 capturas con hash en `forense/prereg-duelo-v2/corridas-L-completa-v1_0/` (en el repo: replay posible en nube). `[LEÍDO]` E.7(3): una vista bloqueada se destraba asentando evidencia corrida por corrida en procesos aislados (`tools/asienta_replay_aislado.py`; ojo: escribe incluso con `--help`, no lo invoques a ciegas).
- `[LEÍDO: lista-pineables-v1_0.md]` los 18 slots y sus RESULT.

## 4 · YA HECHO
Por objeto («TANDA-6», «CALC-L-DESDE-CAPTURAS» en replay-evidencia): 0 asientos, 0 pines L. Repítela tú.

## 5 · PIEZAS
**P1 · Replay.** `python3 tools/corrida0.py verify CALC-L-DESDE-CAPTURAS-v1_0`; asiento en `replay-evidencia.tsv` con los dos ejes. Si RESULTADO no es afirmativo (`REPRODUCE` o `REPLICA-RESULTADO`), **PARA**: no se pinea contra un sello que no replica; NC con el diagnóstico.
**P2 · Los 18 pines** (F-L), vía (i), nota «mediana sobre 8/8 capturas selladas; replay <veredicto>». `valida_pin` → `ACEPTADO`. Contador −18 o el número real con su razón.
**P3 · Cierre.** FP F-L `FIRMADA`; NC de TANDA-5 P2 cerrada; nota de media página.

## 6 · LATITUD · 7 · PAROS · 8 · COMPUERTAS · 9 · PERÍMETRO
Latitud: logística, orden. PAROS: a) P1 no afirmativo · b) pinear una de las 7 L con reserva o cualquier otra lectura · c) el contador baja en más de lo pineado · d) editar un sello · e) `DIN-M-01:M` sale de legacy (vetado). Compuerta: «asiento de replay afirmativo» protege **adoptar**. Perímetro propio: `replay-evidencia.tsv` (filas propias), `pines-de-mesa.tsv`, FP/NC propias, nota, cascada. Ajeno: todo lo demás. Si escribes fuera, PARA.

## 10 · NO HACE · CIERRE
No mide · no toca las 7 con reserva · no re-sella. `## NO-CORRIDO / RESERVAS` · `## CONSUMIDO`.

## NO-CORRIDO / RESERVAS

- **qué**: P2 · los 18 pines de L (F-L) vía (i) al RESULT de `CALC-L-DESDE-CAPTURAS-v1_0`. **por qué**: `PARO-PREMISA` — verificado por mutación directa contra `pines_mesa.valida_pin` (no por lectura): con la guarda (a) ya en verde (P1 de este acto), las 18 filas construidas según F-L son `RECHAZADO-SIN-INSUMO-CRUDO` por la guarda (b) (`_tiene_crudo`): `CALC-L-DESDE-CAPTURAS-v1_0/spec.yaml` declara sus 7 inputs con `origen: repo` (código y metadatos), ninguno `origen: manifiesto` ni con `manifiesto-capturas` en la ruta, y `dependencias_materiales: []` está vacío. Las 224 capturas que el CALC lee de verdad (vía `IN-F5C-PLAN`, un JSON de rutas) no están declaradas como insumo crudo individual en el spec congelado (`#973`, COMMIT-1). No se tocó `spec.yaml` (congelado, PARO (d)) ni `tools/pines_mesa.py` (TUBERÍA de 4.1). **impacto**: 18 lecturas L (`marco-M::{CIV-M-01,02,04,10,12,13; FAM-M-05,06,07}::{L-solo,L+corpus}`) siguen legacy; `dependencias_numericas_legacy_activas` se queda en 146 (no baja a 128 como preveía la cabecera). **sucesor**: `NC-260922-GEN2-RELEVO-TANDA-6-7510-01`, `DECISION-DE-MESA-PENDIENTE`: si el spec debe enmendarse (D-18, enmienda de cableado) para declarar el manifiesto de capturas como insumo `origen: manifiesto`, o si la guarda (b) debe reconocer un `origen: repo` cuya ruta cita el plan de capturas como insumo crudo indirecto.
