# ACTO GEN2-LINAJE-Y-ADOPCION · cierre

Fecha: 11/sep/2026  
Entorno: NUBE, repo y agregados; cero microdatos, cero red científica y cero llamadas a modelos.  
Encargo: `forense/encargos/2026-09-11-GEN2-LINAJE-Y-ADOPCION.md`.

## Resultado

El registro ya no confunde generación administrativa, permiso de conteo,
procedencia numérica y aptitud de adopción. La resolución se hace por RESULT:
`NUEVO`, `HEREDADO`, `MIXTO` o `INDETERMINADO`; cada input queda además
rotulado como `DATO`, `CODIGO`, `METADATO`, `CONTROL-HISTORICO` o
`INDETERMINADA`. Sólo `DATO` propaga procedencia.

`milpa/src/linaje.py` contiene la decisión pura compartida por registro y T35,
y es importable por los sucesores 18/19 sin acoplarlos a la CLI. Una adopción
`MEDICION-GEN2` exige origen `NUEVO`. Los usos `HISTORICO`, `BASELINE`,
`DESCRIPTIVO` y `CALIBRACION` admiten herencia sólo si se declaran; no la
borran. `CONFIRMACION-INDEPENDIENTE` exige además validación `PASA` y rol
`HOLDOUT`/`EVALUACION-RETENIDA`.

La salida `APTA-POR-LINAJE` certifica sólo procedencia. No certifica que
variable, unidad, población, transformación o estimando correspondan al
parámetro. Éste es el ajuste que corresponde al benchmark web de cuatro
decisiones: su investigación separa reproducibilidad de adecuación científica,
pero no constituye firma para adoptar sus propuestas sobre DIN, S6,
complementos o corrupción.

## Casos reales levantados

| caso | cuenta firmada | origen resuelto | resultado |
|---|---:|---|---|
| `CALC-SMOKE-0001/0002` | NO | HEREDADO | replay legacy visible; no medición GEN2 |
| wrapper M que consume `milpa/tramite.yaml`/`procedencia.yaml` | según spec | HEREDADO | el alias léxico o material no limpia la fuente |
| ocho árbitros R vigentes (`DIN-M-01-v4`, `FAM-M-01/05/06/07-v3`, `TRA-M-02/03/07-v3`) | SI | NUEVO | `correr-R.py` es código; el dato se reestima desde manifiesto |
| `CALC-B-0001` | SI | NUEVO | medición genuina; adopción vigente conserva aptitud |
| `CALC-TRIADA-0001` | SI | MIXTO | la firma de contador se conserva y la herencia queda separada |
| `CALC-TRIADA-0002` | SI | HEREDADO | el snapshot M propaga su origen; no se reescribe sello alguno |

Los caminos quedan publicados en `camino_linaje`, desde consumidor/RESULT
hasta CALC, snapshot o fuente. Rutas con `./`, `..`, separador invertido o
symlink convergen por identidad material; externos, enlaces rotos, padres
ausentes y ciclos terminan en `INDETERMINADO`. `tramite.yaml.otro` no coincide
con el archivo exacto.

## Auditoría de las 16 adopciones activas

Derivación sobre el corte integrado: 16/16 `MEDICION-GEN2`, 16/16 origen
`NUEVO`, 16/16 `APTA-POR-LINAJE`; ninguna pierde aptitud.

| RESULT | consumidor / impacto |
|---|---|
| `RESULT-ENCIG-MOR-A-P-SOL1` | `tramite.mordida.discrecional` |
| `RESULT-ENCUCI-A-P-CUALQUIERA` | `tramite.mordida.discrecional` |
| `RESULT-ENCIG-MOR-B-P-PRE-SD` | `tramite.mordida.con_registro` |
| `RESULT-ENCIG-MOR-B-P-DIG-SD` | `tramite.mordida.con_registro` |
| `RESULT-ENCIG-MOR-C-P-ADOPTA` | `tramite.gobierno_digital.util_sin_coercion` |
| `RESULT-ENVIPE-DEN-P-C2-U4` | `civico.denuncia.miedo_desconfianza` |
| `RESULT-B-ENIGH-2022-P` | `familia.seguro.volatilidad_ausencia_estado` |
| `RESULT-ENIF-AHO-A-P-CORTO-SIN-P` | `dinero.ahorro.horizonte_corto` |
| `RESULT-ENIF-AHO-A-P-CORTO-CON-P` | `dinero.ahorro.horizonte_no_corto_con_seguridad_social` |
| `RESULT-ENIF-AHO-B-P-FORMAL-P` | `dinero.ahorro.via_informal` |
| `RESULT-ENIF-AHO-B-P-INFORMAL-P` | `dinero.ahorro.via_informal` |
| `RESULT-ENIF-AHO-C-P-DESCONFIA-CONOCE-P` | `dinero.ahorro.seguro_deposito_enif2024` |
| `RESULT-ENIF-AHO-C-P-DESCONFIA-NOCONOCE-P` | `dinero.ahorro.seguro_deposito_enif2024` |
| `RESULT-ENCUCI-B-P-URB-AGR` | `civico.protesta.agravio_urbano_encuci2020` |
| `RESULT-ENCUCI-B-P-RUR-AGR` | `civico.protesta.agravio_urbano_encuci2020` |
| `RESULT-ENIF-POB-P-CORTO-NO-TRABAJA-P` | `dinero.ahorro.horizonte_no_trabajadores` |

## Verificación

- Contraejemplo: un consumidor GEN2 que cita un RESULT heredado, aun con
  `cuenta_gen2=SI` y sello, para con `USO-NO-APTO` e informa RESULT,
  consumidor, motivo e impacto.
- Aceptación: un RESULT nuevo desde manifiesto queda `APTA-POR-LINAJE`.
- Rutas, symlinks, snapshot, padre/hijo/nieto en orden inverso, código frente
  a tasa, ciclos, desconocidos, excepción de contador y separación por RESULT
  están cubiertos por fixtures temporales.
- `tests/test_corrida0.py`: 90/90.
- `tests/test_corredores_gen2.py`: 35/35.
- Las tres vistas se regeneraron desde evidencia vigente. No se ejecutó ningún
  medidor, no se re-selló historia y el guard de replay no observó transiciones.

## Obligaciones y residuales

| obligación | evidencia | consumidor/alcance | cierre o residual |
|---|---|---|---|
| Separar contador y origen | `origen_numerico`, tests de firma | registro completo | CERRADA |
| Propagar identidad y origen | normalizador, intermediarios y `camino_linaje` | por RESULT | CERRADA |
| Usar una sola aptitud | `milpa/src/linaje.py`, registro y T35 | adopción activa | CERRADA |
| No reclasificar código R como tasa | ocho CALC-R reales `NUEVO/SI` | árbitros vigentes | CERRADA |
| Auditar adopciones | tabla 16/16 | reglas de `milpa/tramite.yaml` | CERRADA; cero pérdida |
| Consultar el contrato desde el emisor | módulo puro disponible | ejecución del motor | DIFERIDO a `GEN2-MOTOR-Y-HERENCIA-EXPLICITA` |
| Completar roles de evaluación retenida | guard prospectivo implementado | confirmación independiente | DIFERIDO a `GEN2-EVALUACION-SIN-FUGAS` |

