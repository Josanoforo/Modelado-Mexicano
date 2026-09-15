# ACTO GEN2-LOTE-MEDICION-PENDIENTE-1 · LOTE D-11 DE MEDICIÓN PENDIENTE (NC-0184 · NC-0099 · NC-0125 · NC-0126)

**SHA de redacción:** no declarado en el texto (llegó como brief de despacho, ítem «2 · CAJA»); **re-derivado al abrir:** `a29d873b` (`origin/main`, PR #759 fusionado, 14/sep/2026)
**Entorno asignado:** CAJA (Ubuntu/WSL) — NO se lanza en NUBE
**Modelo:** Opus
**Rama:** `acto/gen2-lote-medicion-pendiente-1`
**Compuerta:** ninguna declarada (`GATED a` / `COMPUERTA:` ausentes). «corre detrás del RUN» se lee como carril: `ACTO GEN2-F5-DOCUMENTAL-RUN` (PR #756) `MERGED` 2026-09-14T19:11Z, `## CONSUMIDO` en su encargo archivado — la secuencia se cumple.
**Estado:** CONSUMIDO (PR #766)

## Texto del encargo, verbatim tal como se lanzó

2 · CAJA — ACTO GEN2-LOTE-MEDICION-PENDIENTE-1 (lote D-11, Opus, hasta 4 piezas afines de microdato; corre detrás del RUN)

P1 = NC-0184: correr el CALC de la spec EDER-CORRESIDENCIA-DISENO-spec-v1_0. Verificado: la spec quedó congelada en COMMIT-1 por #760 (0cbaba6c, 14/sep) y cero corridas la consumen (grep -i corresid en corridas.tsv: 0 coincidencias, 166 filas examinadas — A.13). Es puro COMMIT-2: el trabajo caro ya está hecho. Cierra la única regla EDER con IC de bootstrap simple.
P2 = NC-0099: la ruta U4 en ENVIPE 2012 vía join a tsdem por N_REN == R_SEL. Verificado: 0 filas U4/tsdem-2012 en corridas.tsv.
P3/P4 (opcionales) = NC-0125 + NC-0126: reconciliar la cobertura ENIF (fase 1 declaró 66.89%; la corrida mide 67.53/68.06) y adjudicar la categoría colapsada P4_10

## NO-CORRIDO / RESERVAS

| qué | por qué | impacto | sucesor |
|---|---|---|---|
| «P1 = NC-0184: correr el CALC de la spec EDER-CORRESIDENCIA-DISENO-spec-v1_0 … Es puro COMMIT-2: el trabajo caro ya está hecho» — **no se corrió esa spec** | `PARO-PREMISA` — la spec v1_0 ya tenía corrida sellada (`CALC-EDER-0001`, mismo PR #760; el `grep -i corresid` buscó la palabra donde `corridas.tsv` escribe el id del CALC) y `NC-0184` pide **otro estimando**. Lo que la fila pedía se ejecutó completo con COMMIT-1 nuevo: spec hermana `EDER-CORRESIDENCIA-ACTUAL-DISENO v1.0` + `CALC-EDER-0002` (absorbe la fila entera; nada queda huérfano) | ninguno: `NC-0184` cierra; el contador mueve una corrida más de lo previsto por el encargo (que suponía cero COMMIT-1) | — (ejecutado en este acto) |
| «P3/P4 (opcionales) = … **adjudicar** la categoría colapsada P4_10» — la adjudicación no se hizo | `DECISIÓN-DE-MESA-PENDIENTE` — el ejecutor no adjudica: produjo las cotas (`CALC-ENIF-0003` `D-*`: 63.6 % de `P4_10 = 1` sin ninguna vía de ahorro vs 37.7 % en el 2; 60.4 %/53.4 % del código 1 en `U_A_SIN`/`U_A_CON`) | `NC-0126` sigue ABIERTA; los cortes del lote ENIF-1 (`{1,2}` primario, `S1 = {1}`) no cambian | mesa, sobre `NC-0126`, con `CALC-ENIF-0003` a la vista |
| Contador: las cuatro corridas selladas (`CALC-EDER-0002`, `CALC-ENVIPE-U4-2012`, `-v1_1`, `CALC-ENIF-0003`) nacen `cuenta_gen2 = PENDIENTE-DE-MESA` | `DECISIÓN-DE-MESA-PENDIENTE` — el brief no trajo firma de mesa con OBJETO sobre el contador (FP-367/368) y no se inventa | `N_corridas_selladas`/`N_resultados_gen2_sellados` no cuentan las 4 corridas / 260 RESULT hasta la firma | `FP-375` |
| `U4` en ENVIPE 2013 y 2015 (`NC-0098`) | `FUERA-DE-PERÍMETRO` — la fila `NC-0099` acota a 2012; 2015 trae `ID_PER` y no necesita la ruta | `NC-0098` conserva 2013/2015 | `NC-0098` (SIN-ASIGNAR de acto puntual, como estaba) |
| Reserva: `CALC-ENVIPE-U4-2012` (v1.0) sigue `SELLADA` en `corridas.tsv` en vez de `SUPERADO→CALC-ENVIPE-U4-2012-v1_1` — `repite_de` quedó bajo `etiquetas` en el `spec.yaml` de v1.1 y `registro()` lo lee en la raíz de la spec; el `spec.yaml` está sellado y no se edita | `DECISIÓN-DE-MESA-PENDIENTE` — corregirlo exige una v1.2 re-sellada sólo para mover una clave; el punto es idéntico en ambas y el IC vigente es el de v1.1 (declarado en nota, ADR y L0) | ninguno sobre el punto; el registro muestra dos corridas SELLADA de la misma spec (v1.0 con IC de 4 estratos, v1.1 con 355) | mesa: aceptar la convivencia declarada, o pedir la v1.2 en un acto de mantenimiento |
| Reserva: `registro --verifica --escribe` pisó `fuente_replay` en 163 filas de 4 corridas ajenas (`CALC-0001`, `CALC-0001-v2`, `CALC-0002`, `CALC-MOTRAL2015-VALORACION-SS-0001`): `VERIFY-EN-ESTA-SESION` → `VERIFY-ESTRUCTURADO · ACTO GEN2-VERIFICACION-CAJA-2` (recibo de #761 ya en `main`) | Reserva (no es pieza no corrida): refresco hacia la fuente más autoritativa, cero transiciones de veredicto, `usos.tsv` idéntico | ninguno | — |

A.8 / ADR-340 (`tools/ya_medido.py`, `TZ=UTC`): `familia.corresidencia.adulto_familiar_actual` — `MEDIDA-EN: milpa/tramite-ola5-propuesta-v0.yaml:192` (SELLADA-SIN-CARGA, p=0.057531; **sucesor GEN2 con diseño: `CALC-EDER-0002`**, sin cita en `milpa/`, adopción de mesa).

## CONSUMIDO

Ejecutado en **PR #766** (`acto/gen2-lote-medicion-pendiente-1`, 14/sep/2026, CAJA Ubuntu/WSL2 con corpus compartido, Opus). Commits: `01dab9a` (0-bis) · `e99aa21` (COMMIT-1: tres specs + tres CALC congelados) · `059c6ae`/`6868630`/`84f38fc` (COMMIT-2 a/b/c: `CALC-EDER-0002`, `CALC-ENVIPE-U4-2012`, `CALC-ENIF-0003` sellados) · `eedceca`+`4481986` (COMMIT-3 de P2: spec v1.1 + `CALC-ENVIPE-U4-2012-v1_1`) · `d21840e` (registro) · `351b5fe` (cascada: `ADR-504`→`ADR-505` tras fusionar `main`, L0, rótulo, `NC-0184`/`NC-0099`/`NC-0125` CERRADAS, `NC-0189`, `FP-375`, hallazgo, nota de cierre, `## NO-CORRIDO / RESERVAS`) · `40b9df9` (merge de `main`, PR #762). El merge es de mesa.
