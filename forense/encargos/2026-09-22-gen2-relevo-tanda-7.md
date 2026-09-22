# ENCARGO · ACTO GEN2-RELEVO-TANDA-7 · LA GUARDA (b) RECONOCE LAS CAPTURAS SELLADAS COMO INSUMO CRUDO, Y ENTONCES ENTRAN LOS DIECIOCHO PINES DE L

> ENTORNO: **NUBE**. NO es CAJA.
CABECERA · SHA de redacción `bda6b60c`; una sesión, rama `acto/gen2-relevo-tanda-7` · MODO ABIERTO · CONTADOR: legacy baja en exactamente lo pineado (hoy 146); `adoptados_activos` antes/después por comando. **L0 de `canon/estado-programa-v1_14.md`: si choca, toma la de `main` y re-inserta solo tu anotación; `canon/L0/` existe.**
**MODELO: Sonnet por mandato de mesa.** Procedimiento congelado o receta; latitud logística; toda duda de procedimiento se pregunta a mesa en una línea con opciones.
NO tocar (TUBERÍA): `tests/check.py`, `tools/cierre_acto.py`, `tools/tablero_programa.py`, `.github/workflows/`, `.claude/commands/`. Cierre: `tests/check.py --rapido` antes de empujar; el CI corre la suite completa. Derivados («DERIVADO — NO EDITAR») no se commitean: los re-deriva el job de main.

## 1 · OBJETIVO
Tercer intento sobre los mismos 18 pines, y el diagnóstico ya es exacto: TANDA-6 (`#985`) probó por mutación que la guarda (b) los rechaza con `RECHAZADO-SIN-INSUMO-CRUDO` porque `_tiene_crudo` (`tools/pines_mesa.py:316-327`) solo reconoce `origen: manifiesto` o una ruta que contenga `manifiesto-capturas`, y `CALC-L-DESDE-CAPTURAS-v1_0` declara sus 224 capturas a través de un plan JSON con hash (`IN-F5C-PLAN`). La regla 4.1 dice «insumo crudo con hash — microdato o capturas selladas»: el CALC lo cumple; la guarda mecánica no lo ve. «Hecho»: la guarda (b) reconoce el caso por regla declarada (no por excepción nombrada); tests por mutación; los 18 pines `ACEPTADO`; F-L `FIRMADA`; el contador bajó en exactamente lo pineado; NC-…-7510-01 cerrada.

## 2 · FIRMAS — verbatim; el lanzamiento es el sello
4.1 (21/sep, TANDA-3 `:8`): «(i) su cifra la produce código GEN2 desde un insumo crudo con hash —microdato o capturas selladas—». F-L (TANDA-5 §2, en el repo): los 18 slots. **Precisión de dirección:** «Un input `origen: repo` cuya ruta apunte a un manifiesto o plan de capturas selladas con hash por captura (hoy `forense/prereg-duelo-v2/F5-completa-plan-v1_0.json` y los `manifiesto-capturas-*.json`) es insumo crudo a efectos de la guarda (b). La guarda lo reconoce leyendo el archivo —que enumere capturas con sha— y no por nombre. El `spec.yaml` congelado de `#973` no se toca.»

## 3 · LO QUE DIRECCIÓN SABE (contra `bda6b60c`)
- `[LEÍDO: nota de TANDA-6]` `verify` → `REPRODUCE / IDENTICO`; asiento existente; la guarda (a) ya en verde; las 18 filas construidas (`marco-M::…::{L-solo,L+corpus}`, `result_gen2=RESULT-LDESC-TABLA-JSON`, `via=i-CRUDO`) caen solo en (b). `[EJECUTADO]` `forense/prereg-duelo-v2/manifiesto-capturas-P3-v1_0.json` existe; el plan `F5-completa-plan-v1_0.json` está declarado en el spec con sha. `[SUPUESTO]` que el plan enumera las 224 rutas con hash por captura: verifícalo; si solo enumera rutas, el hash está en el sello del CALC (`input_sha256_efectivos`) y la guarda puede leerlo de ahí — dilo cuál.

## 4 · YA HECHO
`#983` (vía (i) eje RESULTADO), `#985` (replay asentado). 0 pines L. Repítela tú.

## 5 · PIEZAS
**P1 · Guarda (b).** `_tiene_crudo` acepta un input `origen: repo` cuyo archivo sea un manifiesto/plan de capturas con hash por captura; test por mutación: acepta el plan real; rechaza un JSON sin hashes; rechaza `origen: repo` a secas. Mensaje de rechazo sigue diciendo por qué.
**P2 · Los 18 pines** (F-L). `valida_pin` → `ACEPTADO`. Contador −18 o el real con razón.
**P3 · Cierre.** F-L `FIRMADA`; NC de TANDA-5 y TANDA-6 cerradas; nota: qué cambió en la guarda y por qué no es una excepción.

## 6 · LATITUD · 7 · PAROS · 8 · COMPUERTAS · 9 · PERÍMETRO
Latitud: implementación, orden. PAROS: a) editar `CALC-L-DESDE-CAPTURAS-v1_0/spec.yaml` o cualquier sello · b) relajar (b) para `origen: repo` sin hashes de captura · c) pinear las 7 L con reserva u otra lectura · d) el contador baja en más de lo pineado · e) `DIN-M-01:M` sale de legacy. Compuerta: «tests de P1 en verde antes de escribir un pin» protege adoptar. Perímetro: `tools/pines_mesa.py`, `tests/test_pines_mesa.py`, `pines-de-mesa.tsv`, FP/NC propias, nota, cascada. Fuera, PARA.

## 10 · CIERRE
No mide · no re-sella. `## NO-CORRIDO / RESERVAS` · `## CONSUMIDO`.
