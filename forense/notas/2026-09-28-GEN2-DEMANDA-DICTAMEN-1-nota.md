# Nota de cierre · ACTO GEN2-DEMANDA-DICTAMEN-1 · 28/sep/2026

**Contadores movidos: cero mediciones; no adopta.** `corrida0 demanda`: `N_corridas_requeridas` 105 → **0** y `N_resultados_pendientes` 236 → **63**, las dos bajas por dictamen citado en `data/corrida0/demanda-dictamen-v1_0.tsv`; ninguna fila borrada (`N_resultados_activos` sigue en 236).

ENTORNO: NUBE (hook: `ENTORNO-DERIVADO = NUBE`, corpus montado NO, archivos examinados 0; red DENEGADA-POR-POLITICA). Cero microdato. Base: `16ba3d02` = origin/main al abrir (0 detrás); SHA de redacción `723b62c1`, ancestro. 0-bis `c13359b5`. MODO AUTÓNOMO-AMPLIO (cláusula v1.0).

## Demanda de apertura (EJECUTADO, `python3 tools/corrida0.py demanda` sobre 16ba3d02)

`N_resultados_activos = 236 · N_corridas_requeridas = 105 · N_resultados_pendientes = 236 · clausura_activa_de_payloads = 22`: coincide con §3 del encargo. Las copias de `demanda-{corridas,resultados}.tsv` de esa corrida son la entrada del constructor (el comando reescribe esos derivados; se restauraron: no son de este perímetro).

## Vocabulario (declarado antes de usarlo; §6 latitud)

Del encargo: `DECIDIBLE`, `SIN-PAYLOAD-EN-CORPUS`, `SIN-ESTIMANDO-RECONSTRUIBLE`, `NO-RELEVAR-POR-REGLA-6`, `RELEVAR-COMO-PISO-DESCRIPTIVO`, `DIFERIDO-A-FAMILIAS-2027`, `NO-RELEVAR-θ`, `RELEVAR-DESDE-RESULT`, `SIN-BASE-GEN2`, `ESPERA-FIRMA-HOLDOUT`, `EN-CURSO`. Añadidos: `YA-RELEVADO-GEN2` (el consumidor ya lee un RESULT GEN2), `NO-RELEVAR-POR-FIRMA` (firma de mesa HISTÓRICO/fuera del contador), `NO-RELEVAR-GENERADOR` (β̂ de `matriz.g`, misma lógica que θ por §4), `ESPERA-FIRMA-MESA` (firma no HOLDOUT), `CELDA-D-ADJUDICADA` / `CELDA-D-SIN-CHAMPION` (estado del contrato celda-D por archivo), y a nivel corrida `CORRIDA-NO-REQUERIDA` / `CORRIDA-REQUERIDA:<tokens>`. Qué cierra cada uno: `VOCAB` en `forense/analisis/demanda-dictamen-1/construye_dictamen.py`. Cierran el RESULT sólo `YA-RELEVADO-GEN2`, `NO-RELEVAR-*`, `SIN-ESTIMANDO-RECONSTRUIBLE` y `DIFERIDO-A-FAMILIAS-2027`.

## Resultado por pieza (EJECUTADO)

| pieza | universo | dictamen |
|---|---|---|
| P2 duelo v2 | 70 | L 28 + AGREGADO 14 → `NO-RELEVAR-POR-REGLA-6` (+ firma H3, e760-03); M 13 `YA-RELEVADO-GEN2` + 1 (DIN-M-01) `NO-RELEVAR-POR-REGLA-6`; R 14 `YA-RELEVADO-GEN2` (RESULT-R-*-PUNTO ya adoptados en `canon/catalogo-del-mexicano-v1_3.tsv`) |
| P3 procedencia + celdas-D | 40 + 21 | θ 12 `NO-RELEVAR-θ` (nadie ocupó la fila de emisión); β̂ 7 `NO-RELEVAR-GENERADOR`; coeficientes asignados 8 `NO-RELEVAR-POR-FIRMA` (H1); asignados de probabilidad 13 → 11 `SIN-BASE-GEN2` (ASIGNADO-CONSERVADO-H1) + 2 `RELEVAR-DESDE-RESULT` (util_sin_coercion, denuncia con seguro); celdas-D 21 → 17 `CELDA-D-ADJUDICADA` + 4 `CELDA-D-SIN-CHAMPION` (evasión de norma) |
| P1 conductas y cortes | 76 + 6 | 59 `YA-RELEVADO-GEN2` (tramite.yaml con `corrida0_resultado_id` GEN2 o usos.tsv GEN2); 4 `NO-RELEVAR-POR-FIRMA` (rol_uso historico, B2); 6 cortes π `NO-RELEVAR-POR-FIRMA` (B3); 6 `SIN-BASE-GEN2` (asignados de mordida y coercitivo); 3 `RELEVAR-DESDE-RESULT` (CALC-L8-CONVERSION-0001, listado para mesa); 4 `ESPERA-FIRMA-MESA` (evasión de norma → A1; ENNViH → B1) |
| P4 momentos | 23 | 15 `ESPERA-FIRMA-HOLDOUT` (M09–M22 letra A2, M23 letra A1); AJUSTE 8: M04, M08 `YA-RELEVADO-GEN2`; M01, M02, M06, M07 `NO-RELEVAR-POR-FIRMA` (H2); M05 `ESPERA-FIRMA-MESA` (A1); M03 `SIN-ESTIMANDO-RECONSTRUIBLE` |

Corridas: 105 de 105 `CORRIDA-NO-REQUERIDA`. Ningún RESULT quedó `DECIDIBLE`, `EN-CURSO` ni `SIN-PAYLOAD-EN-CORPUS`.

«Hecho» (EJECUTADO en el commit de cierre): ids sin fila 0 (236 RESULT + 105 corridas = 341 filas); dictámenes sin cita 0 (el constructor lo aserta); `grep -c "no existe"` en la vista = 0; `corrida0 demanda` reporta 0 corridas requeridas (de apertura 105; no requeridas por dictamen 105) y 63 pendientes (cerrados por dictamen 173). Cuadre por token: 88 + 43 + 22 + 12 + 7 + 1 = 173.

## Premisas que cayeron (logística; el objetivo siguió alcanzable)

- «10 `celda_D`» (§1 P3): son **21** en la demanda (`data/curacion-registro/celdas-d/`, 21 archivos). Se dictaminaron las 21.
- «33 de procedencia.yaml»: son **40** con los 7 `coeficiente_ejecutable`. Se dictaminaron los 40.
- «61 indecidibles»: los rótulos del encargo se solapan; al dictaminar, ninguno resultó `DECIDIBLE`: la indecidibilidad venía de que la demanda no lee lo ya relevado (ver hallazgo).
- «RELEVO-TRAMITE-CAJA-1 mide las 10 de orden 1: cítalas como EN-CURSO» [REPORTADO]: NO-ENCONTRADO por este agente en `forense/encargos/` de origin/main ni en las 7 ramas remotas (`git ls-remote --heads origin`, 28/sep). Además, ninguna fila de orden 1 quedó pendiente: sus RESULT ya son GEN2 o `rol_uso: historico`. No se usó `EN-CURSO`; NC-…-c133-01.
- P4 «AJUSTE sin RESULT → DECIDIBLE»: M03 no tiene instrumento ni estimando reconstruible → `SIN-ESTIMANDO-RECONSTRUIBLE` (INTERPRETACIÓN-DECLARADA), a mesa como B2.

## Hallazgos

1. `corrida0 demanda` no descuenta lo ya relevado: ni `corrida0_resultado_id` GEN2 de `tramite.yaml`, ni `usos.tsv`, ni las firmas B2/B3/H1–H3 (el contador `status` sí aplica algunas). Eso convertía la demanda en inventario. Cableado mínimo en `tools/corrida0.py` (8 líneas en `cmd_demanda`, coordinado por archivo con TUBERIA-Y-CURACION-1, que toca `status`, no `cmd_demanda`); arreglo de raíz: NC-…-c133-02.
2. `corrida0 demanda` reescribe `data/corrida0/demanda-*.tsv` al leer (D-23: un comando que deriva no escribe estado). Anotado en `forense/hallazgos.md`.
3. Seis RESULT derivados (`RESULT-ENCIGDER-*`, `RESULT-ENCUCIDER-A-Q`) viven en sus `CALC-*-COMPLEMENTO(S)-DERIVADO-0001/resultados.json` y no tienen fila en `data/corrida0/resultados.tsv`. Anotado.
4. La vista es foto de la demanda de apertura: si la demanda cambia, se regenera con `construye_dictamen.py --entrada <copias> --escribe`; una fila nueva de la demanda sin dictamen no se descuenta (falla hacia contar de más, no de menos).

## Firmas

A1 y A2 ya están en mesa (f2e5-01/-02): se citan, no se duplican. Nuevas: FP-260928-GEN2-DEMANDA-DICTAMEN-1-c133-01 (B1, ENNViH) y -02 (B2, M03). Hoja: `forense/analisis/demanda-dictamen-1/hoja-para-mesa-demanda-dictamen-1.md`, para FIRMAS-21/22.

## Sucesores

RELEVO-CONSUMIDORES-4 (pins de 22 RESULT/celdas-D y 17 SIN-BASE-GEN2), FIRMAS-21/22 (A1, A2, B1, B2), RELEVO-TRAMITE-CAJA-2 y CALC-ALTERNOS-LOTE-1 (consumen la vista: hoy sin corridas de demanda), GEN2-DEMANDA-DICTAMEN-2 (demanda que derive estado por sí misma).
