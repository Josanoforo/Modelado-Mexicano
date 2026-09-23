# REGION-ENCIG2025-CONSUMIDORES · spec humana v1.0

El primer resultado que produzca este procedimiento es el que se reporta. Esta pieza mide por **entidad de residencia del informante** cuatro conductas activas de ENCIG 2025, con códigos heredados de `CALC-ENCIG-0001`/`forense/prereg-caja/ENCIG-MORDIDA-spec-v1_0.md`. No interpreta entidad como ubicación del trámite. El marco ENCIG cubre población de 18+ en localidades de 100 mil habitantes o más; los resultados no describen población rural ni ciudades menores. Solo se abre el manifiesto `encig25_base_datos_csv`, ZIP ya existente y no reservado.

| Conducta consumidor | Tabla y unidad del denominador | Denominador | Numerador | Factor |
|---|---|---|---|---|
| `paga_mordida_encig2025` | `encig2025_01_sec1_A_3_4_5_8_9_10.csv`, persona 18+ | `P8_3_1∈{1,2}` | `P8_3_1=1` | `FAC_P18` |
| `adopta_encig2025_luz` | `encig2025_04_sec_7.csv`, trámite de luz | `N_TRA=01` y `P7_3∈{1,2,4,5,6}` | `P7_3∈{4,5}` | `FAC_TRA` |
| `paga_mordida_encig2025_presencial_r2` | SEC7 enlazada a `encig2025_05_sec_8.csv` por `ID_TRA`, registro de trámite **sin deduplicar** | `P7_3=1` y `P8_4∈{0,1}` | `P8_4=1` | `FAC_TRA` |
| `paga_mordida_encig2025_digital_r2` | mismo enlace y unidad | `P7_3∈{3,4,5}` y `P8_4∈{0,1}` | `P8_4=1` | `FAC_TRA` |

La fila de SEC8 por `ID_TRA` debe ser única y no vacía; SEC7 puede repetir `ID_TRA` y los brazos `_r2` **no deduplican**. Falta de pareja deja fuera del denominador B, no se imputa. `P8_3_1=1` y `P8_4=1` miden **solicitud** de pago informal; el nombre heredado `paga_mordida` no prueba pago consumado. Las cuatro unidades no se suman ni promedian. `CVE_ENT` de cada tabla es entidad de residencia según el descriptor público `encig25_estructura_base_datos.pdf`. Se excluyen registros sin factor positivo, estrato o UPM válidos **antes** de formar el plan de réplicas y se cuenta cuántos salen; dentro de ese marco elegible se forma el diseño completo antes de aplicar conducta/entidad.

Factor por tabla arriba; estrato `EST_DIS`, UPM `UPM_DIS`. Punto como razón de masas ponderadas por código `CVE_ENT=01..32`, nunca media de porcentajes. 1 000 réplicas UPM estratificadas compartidas entre los 32 dominios de cada conducta; mismo orden/semilla PCG64(20260923) en los brazos SEC7, que preserva su covarianza. Módulo `tools/celda_d/marginales_reproduccion.py::replicas_compartidas` fijado SHA256 `4df2c630179c194345594d959d012b7dd18d94ac93fab3f48b8f6683753dafd6`; UPM única, extremos y réplicas inválidas siguen el protocolo congelado en la spec regional base. R1/R2 de mesa del 23/sep/2026: solo entidades admitidas; punto e IC95 percentil únicamente con n no ponderado ≥200, varianza estimable y regla oficial más estricta. Todas las filas permanecen con estado y cifras nulas si se suprimen. `n` es persona, trámite o registro según fila, no número de UPM independientes.

Cada `-JSON` guarda las réplicas conjuntas, diagnóstico y unidad, sin identificadores ni pesos individuales. Scalar RESULT por conducta y entidad cita punto, límites, n, Kish y estado. `cuenta_gen2: SI`, `origen_numerico: NUEVO`, `adopta: NO`, **RETROSPECTIVA**. No se abre NSE ni región×clase. Esta corrida no hereda calibración de persistencia; `≥3` olas es solo elegibilidad documental.

## Auditoría de rigor extremo

`P8_3_1` es el primer inciso, no todas las solicitudes; `_r2` preserva filas de SEC7 sin deduplicar y no equivale a personas. Canal digital puede depender de oferta y acceso, no de preferencia cultural. Las celdas estatales de ENCIG describen un marco urbano selectivo; n≥200 no garantiza precisión ni da inferencia rural. No hay variable de clase AMAI exacta ni de pertenencia indígena en estas filas.
