# `GEN2-R-COMPLETA-MARCO` — cierre

**Fecha:** 9/sep/2026 · **Entorno:** CAJA, Ubuntu/WSL, Opus · **Compuerta:** contrato TRIADA de `ENCARGO 2/5` presente en la base fusionada · **Motor:** intacto · **L/M:** no leídos durante la medición.

## Resultado

El árbol determinó 6 árbitros R ya sellados y 8 faltantes ejecutables. Los ocho pasaron `spec-check → preflight VERDE → run → verify REPRODUCE/CONTEXTO=IDENTICO`. Al aplicar la corrección puramente registral de estado/fecha exigida por FP-370, la guardia de inmutabilidad impidió re-sellar los mismos IDs; por eso nacieron ocho sucesores `-v2` ligados por `repite_de`. La revisión adversarial de PR #680 conserva esos sellos históricos intactos y añade siete sucesores técnicos `-v3` y `CALC-R-DIN-M-01-v4` sólo para completar las dependencias materiales del replay; el intento sellado `CALC-R-DIN-M-01-v3` también se preserva y queda superado. No hubo celda bloqueada ni sin spec. `UR` permanece congelado en **14/14** mediante `universo-triada-v1_3.tsv`; esto habilita el panel para el `ENCARGO 5/5`, pero no decide `U3` ni adjudica contendiente alguno.

`codificacion-R-v1_1.tsv` fue el primer sello registral. La revisión adversarial de PR #680 detectó que esa redacción hacía parecer que FP-370 autorizaba epistemológicamente el diseño aproximado de `DIN-M-01b`. La sucesora `codificacion-R-v1_2.tsv` conserva sin cambio el estimando y el punto: separa el punto descriptivo disponible del EE/IC bajo diseño aproximado. FP-370 no autoriza esa inferencia; `FP-371` queda ABIERTA y sin firma exclusivamente para aceptar o rechazar estrato constante + `folio` como aproximación de diseño.

La fila `FP-370` queda `FIRMADA -- EJECUTADA` por la firma de mesa de este encargo y remite a la sucesora sellada; v1.0 permanece intacta.

## Las 14 celdas

| celda | estado R final | UR | punto R | n | masa ponderada | excluidos | estratos / UPM | IC95 / reserva |
|---|---|---:|---:|---:|---:|---:|---:|---|
| CIV-M-01 | R-YA-SELLADO | SI | control positivo, no re-medido | — | — | — | — | CALC histórico |
| CIV-M-02 | R-YA-SELLADO | SI | control positivo, no re-medido | — | — | — | — | CALC histórico |
| CIV-M-04 | R-YA-SELLADO | SI | control positivo, no re-medido | — | — | — | — | CALC histórico |
| CIV-M-10 | R-YA-SELLADO | SI | control positivo, no re-medido | — | — | — | — | CALC histórico |
| CIV-M-12 | R-YA-SELLADO | SI | control positivo, no re-medido | — | — | — | — | CALC histórico |
| CIV-M-13 | R-YA-SELLADO | SI | control positivo, no re-medido | — | — | — | — | CALC histórico |
| DIN-M-01 | R-YA-SELLADO | SI | 0.15558094338412926 | 19,739 | 68,002,840 | 63 | 1 / 8,050 | [0.1461309873, 0.1650308994]; DISEÑO APROXIMADO / NO AUTORIZADO COMO GROUND TRUTH INFERENCIAL DE TRIADA SIN FIRMA DE MESA |
| FAM-M-01 | R-YA-SELLADO | SI | 0.5571925669683186 | 12,054 | 76,430,133 | 392 | 182 / 1,908 | [0.5439300566, 0.5704550773] |
| FAM-M-05 | R-YA-SELLADO | SI | 0.04745859252351374 | 70,311 | 32,974,661 | 0 | 536 / 7,891 | [0.0449844107, 0.0499327743] |
| FAM-M-06 | R-YA-SELLADO | SI | 0.04728548395278385 | 74,647 | 34,400,515 | 0 | 543 / 8,377 | [0.0449423946, 0.0496285733] |
| FAM-M-07 | R-YA-SELLADO | SI | 0.04377543852935772 | 89,006 | 35,749,659 | 0 | 558 / 10,118 | [0.0417927636, 0.0457581134] |
| TRA-M-02 | R-YA-SELLADO | SI | 0.12602486953090247 | 13,412 | 61,126,927 | 8,107 | 281 / 3,003 | [0.1161074373, 0.1359423018]; 1 estrato con UPM única |
| TRA-M-03 | R-YA-SELLADO | SI | 0.04453797671500066 | 22,081 | 32,965,687 | 10,919 | 180 / 6,510 | [0.0389693871, 0.0501065663]; 1 estrato con UPM única |
| TRA-M-07 | R-YA-SELLADO | SI | 0.07181522879909936 | 39,763 | 51,117,793 | 167 | 353 / 9,190 | [0.0671184263, 0.0765120313] |

Cada medición nueva quedó contada una sola vez por su `-v2` (`cuenta_gen2=SI` y `FP-370; OBJETO=CALC-R-…:<id_celda>`). Los sucesores puramente técnicos heredan ese contador y la vista canónica los marca `cuenta_gen2=NO`, evitando contar dos veces el mismo objeto. Los conteos de faltantes se desagregan en cada `resultados.json`; en estas ocho corridas `N-FALTANTES-EXCLUIDOS` coincide con código excluido y `N-FUERA-UNIVERSO=N-SIN-PONDERADOR=0`.

## Independencia y controles

Los ocho CALC activos sólo declaran payload, `codificacion-R-v1_2.tsv`, marco v1.3 y el aparato estadístico R existente. No declaran ni abren `corridas-L/`, `corridas-M/`, extractor L, CALC TRIADA ni errores de contendientes. Los seis controles positivos coinciden literalmente en variable, universo, códigos, ponderador, estrato y UPM con la sucesora; no se volvieron a medir. Sólo después del sello se compararon los ocho puntos con sus `-v2`: ocho deltas exactamente cero. Evidencia tabular: `2026-09-09-GEN2-R-COMPLETA-MARCO-P4-control.tsv`.

## Frontera, NC y sucesor

Ningún target R requiere una fuente nueva: **0 bloqueados, 0 sin spec, 0 NC nuevas**. Se mantienen las reservas estadísticas nombradas arriba. `NC-0143` sigue abierta porque cerrar `U3` requiere los puntos válidos de L y el snapshot M; su habilitador se actualiza para consumir el `UR=14` congelado aquí. Este acto no amplía el panel después de observar quién gana y no realiza comparación triádica.

**Reserva de suite:** `tests/test_corrida0.py` pasa 83/83. `python3 tests/check.py --baseline` da **LÍNEA BASE VERDE**, con los 3 FAIL heredados y 1,959 WARN, sin entradas nuevas. T22 reconoce `codificacion-R-v1_1.tsv` porque la FP-371 abierta lo cita como antecedente sellado de la reserva; no se mutó el sello v1.1, no se modificó `tests/` y `tests/baseline.json` permanece intacto. T02, T15, T22 y T32 quedan sin FAIL nuevos.

## Cascada

- Sucesoras vigentes tras la corrección adversarial: `codificacion-R-v1_2.tsv` y `universo-triada-v1_3.tsv`, ambas con hash. La segunda actualiza sólo el estado factual: extractor L v1.3 y snapshot M v1.0 ya están disponibles en `main`; U3 sigue sin derivar y UR permanece congelado en 14/14.
- Siete CALC-R activos `-v3` con `repite_de` a su `-v2`, y `CALC-R-DIN-M-01-v4` con `repite_de` al intento sellado `-v3`. Los `-v2` permanecen intactos y superados; `DIN-M-01-v3` también permanece intacto y superado por `-v4`. Los sucesores reparan únicamente el replay: ligan `tools/arbitra.py` (`d668829386db9fba8ca6a7c2ed2955cb391e540e0e5ae54c839def3580446cdf`), `forense/prereg-duelo-v2/corridas-R/correr-R.py` (`02896f92aa075b2039eaab5554502779851cb047da6adffc779d33283808514a`), `tests/dbfmini.py` (`a14952e7f754b6921c78312cf1f5c2156b73d4b82f12fa6f9dad72740160335b`) y `tests/svystat.py` (`5d97b1362dbf31845bb2080f479ac3022921579546a7b327cbd7e1204e4959de`) por SHA256. El contador vigente conserva ocho mediciones, no suma sucesores técnicos.
- `ADR-452`, L0 y rótulo `GEN2-R-COMPLETA-MARCO` registran el acto.
- `ENCARGO 5/5` debe usar este `UR=14` congelado y aplicar, sin ampliarlo, la intersección U3 de la spec TRIADA.
