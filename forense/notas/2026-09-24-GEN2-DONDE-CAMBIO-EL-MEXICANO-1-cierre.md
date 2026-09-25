# Nota de cierre · ACTO GEN2-DONDE-CAMBIO-EL-MEXICANO-1

24/sep/2026 · CAJA (`tools/entorno.py --sonda-red`: corpus=SI(examinados=511), raices data_raw:SI descargas_mx:SI; red=000 desde el sandbox, sin microdato en este acto) · Opus 5.5 · MODO AUTÓNOMO · ADR-260924-GEN2-DONDE-CAMBIO-EL-MEXICANO-1-96ee-01.

**Resumen.** 7872 series: 583 ESTABLE · 8 CAMBIO-SOSTENIDO · 0 SALTO-DE-INSTRUMENTO · 81 SALTO-SIN-EXPLICAR · 7200 SIN-SERIE (suma de RESULT-DC-<INST>-N-* de los nueve CALC-<INST>-SERIE-DICTAMEN-0001). Todo RETROSPECTIVA; `cuenta_gen2: SI`, `adopta: NO`.

## 1 · Recuperación de sesión

La computadora se apagó tras COMMIT-1a (`9aea5a09`). La sesión siguiente encontró sin commitear el esquema del mapa, el motor `tools/series/` y el sintético; los selló en `24958c0e` antes de leer valores. Ningún valor se había leído antes de la caída.

## 2 · Commits en orden (B-bis, D-22)

- `96ee84fd` 0-bis · `9aea5a09` COMMIT-1a spec (vocabulario, umbrales, desempate) · `24958c0e` motor y sintético.
- `625f98af` COMMIT-1b: mapa de series congelado (31 063 filas, sólo ids; `forense/analisis/donde-cambio/mapa/CONGELADO.md`).
- COMMIT-1c: nueve `spec.yaml` derivados del mapa sin valores + prueba sintética del conducto (`tools/series/sintetico_conducto.py`, tres escenarios, `_fallas_run` limpio); preflight VERDE en los nueve sobre base = origin/main.
- COMMIT-2: un commit por CALC sellado (`corrida0 run`); `verify` REPRODUCE · IDENTICO en los nueve, y de nuevo en proceso aislado (`tools/verifica_aislada.py`) con asiento E.7 en `forense/replay-evidencia.tsv`.
- P4 `7ab748d1`: `forense/analisis/donde-cambio/tabla-dictamen-v1_0.tsv` (una fila por serie, 0 sin dictamen) y `canon/donde-cambio-el-mexicano-v1_0.md` (`tests/test_donde_cambio_documento.py`: regeneración byte a byte y 0 cifras sin RESULT).

## 3 · Interpretaciones declaradas (PROPUESTO-POR-EJECUTOR)

1. Quinta palabra `SALTO-SIN-EXPLICAR` (spec §4; término de #972): sin ella un único par fuera sin cita quedaría sin dictamen.
2. Celdas de `RESULT-*-TABLA` sellados (ENOE, ENDIREH, MOCIBA) direccionadas `<RESULT>#k=v&…/<campo>`, resueltas por (CALC, RESULT): sin esto tres instrumentos del encargo quedaban fuera.
3. Conductas fuera de escala (0,1) entran al mapa y salen SIN-SERIE; ENOE sólo dentro de era (cruce = NO-COMPARABLE); ENDIREH sin fuente de comparabilidad → NO-DOCUMENTADO.
4. Instrumentos menores en un solo CALC-OTROS (NC 96ee-04).

Detalle en `mapa/CONGELADO.md`.

## 4 · Exposición declarada

Dos subagentes de construcción del mapa vieron cifras incrustadas como texto en columnas permitidas (`unidad_escala` del catálogo; prosa §0 de `R-ENVIPE-SERIE-DBF-spec`). No las transmitieron; los scripts las recortan. La sesión ejecutora no vio ningún valor de serie antes del COMMIT-2.

## 5 · Lectura (sin causa, v2.16 §3)

- Los ocho CAMBIO-SOSTENIDO son ENOE, con acumulado entre −1.1 y −0.0 pp y pares fuera en ambas direcciones: artefacto de IC estrecho y τ² pequeño bajo una regla sellada que no se reinterpreta (PARO d). No se leen como cambio de conducta.
- ENVIPE no denuncia (C1/U1, 15 olas): SALTO-SIN-EXPLICAR sólo en 2019→2020 (−3.9 pp); candidato a crisis, no cultura. Serie R (6 olas): salto 2015→2021.
- ENCIG C-LUZ-DIGITAL: 9 ESTABLE, 2 SALTO-SIN-EXPLICAR (18–29 en 2019→2021; hasta primaria en 2021→2023). No coincide con el 2017→2019 de #972, que era la serie nacional con 2025.
- SIN-SERIE domina por corpus (una o dos olas por celda en ENIF, ENDIREH, MOCIBA), no por dato.

Cifras: `canon/donde-cambio-el-mexicano-v1_0.md`, cada una con su RESULT.

## 6 · Contadores

Nueve corridas selladas (README 246 → 255, RESULT GEN2 66 582 → 71 614, ajuste declarado D-21). `celdas_validadas` 219 → 219. Ninguna adopción.
