# ACTO GEN2-MOTOR-Y-HERENCIA-EXPLICITA · cierre

Fecha: 11/sep/2026  
Entorno: NUBE, repo y agregados; cero microdatos, cero red científica y cero
llamadas nuevas a modelos.  
Encargo:
`forense/encargos/2026-09-11-GEN2-MOTOR-Y-HERENCIA-EXPLICITA.md`.

## Resultado

El emisor probabilístico conserva su API histórica y añade un contrato
explícito para presentarse como GEN2. `emitir_binaria_contrato` exige propósito,
dominio, consumidor activo, RESULT sellado, generación GEN2, origen numérico
apto según el contrato de 17 e identidad entre el valor materializado y el
RESULT. Toda ausencia termina en `NO_COVERAGE`: no usa el `p` viejo, cero ni el
árbitro como sustituto.

La ruta `HISTORICO` sigue accesible y expone las dependencias de regla,
palancas, generadores, tier y números sin RESULT. La ruta GEN2 emite el valor
completo del RESULT, no el redondeo de seis decimales, y conserva
`resultado_id`, generación, origen, aptitud y camino de linaje.

17 se integró como dependencia por `d19c92d` y su cierre remoto `3e68220`, PR
#710. Este acto sólo consume `milpa/src/linaje.py` y las vistas derivadas; no
duplica el resolvedor de rutas, registro ni T35.

## Cobertura observada

El snapshot sucesor
`forense/prereg-duelo-v2/snapshot-M-gen2-explicito-v1_0.json` se re-deriva con
`tools/snapshot_motor_gen2.py` y guarda hash del emisor, contrato de linaje y
selector temporal.

| alcance | antes | resultado explícito |
|---|---:|---:|
| registro activo | 207 usos: 16 GEN2 directos, 191 legacy | los 16 directos se evaluaron y los 16 emitieron |
| `milpa/tramite.yaml` | 66 consumidores: 16 GEN2, 50 legacy | CIV 3, TRA 5, FAM 1, DIN 7 |

Los conteos no son oráculo de prueba: el test los compara contra la vista que
acaba de cargar. Los 191 legacy quedan agrupados por causa en la nota de Fase
1; no se convirtieron en 191 supuestas mediciones faltantes.

La transferencia operativa ENIGH-NS para 2022 selecciona la última ola
estrictamente anterior disponible al corte `2021-12-31`:
`RESULT-B-ENIGH-2020-P`. Usa igualdad exacta de encuesta, reactivo, universo,
codificación, segmento y unidad. Queda rotulada
`NO-EVALUACION-INDEPENDIENTE`; la misma operación con rol `ARBITRO` falla
cerrada.

## Ajustes de la adenda y benchmark

- S6 recibió en `milpa/tramite-ola5-propuesta-v0.yaml` la enmienda de alcance
  y el rótulo `IC-SENSIBILIDAD-LOCALIDAD-NO-DISENO-OFICIAL`. No cambian los
  veredictos históricos ni R4.4 MEDIA; FP-372 y NC-0156 continúan.
- Fintech D10 llegó al contexto R1.6 en `milpa/procedencia.yaml` como
  `DESCRIPTIVO-NO-CALIBRA`. 2018 sigue no estimable; 2021/2024 se presentan
  lado a lado y el proxy no sustituye la probabilidad R1.6. NC-0122 continúa.
- La identidad ENCIG2023 ya había sido corregida por el payload incorporado
  en #700; se verificó y no se repitió. El escenario académico de tandas no
  fue adoptado como parámetro.
- El benchmark cargado por otra sesión y fusionado en #708 se consumió como
  propuesta, no firma. r2 de ENCIG sólo emite para uso descriptivo; una
  probabilidad por evento falla cerrada.
- El complemento ENCUCI ya adoptado deriva `1-p` del mismo RESULT y no suma
  una observación. La propuesta ENVIPE conserva el contrato de persona/U1-U4,
  pero devuelve `NO_COVERAGE` hasta firma; una persona con razones del padre y
  del resto mantiene padre=1 y complemento=0.
- DIN y S6 conservan sus puntos descriptivos y limitaciones; no se promueven
  los IC aproximados ni se infiere decisión de FP-371/372.

## Pruebas

- `tests/test_motor_gen2_explicito.py`: 10/10 casos obligatorios.
- `tests/test_motor_usos_complementos.py`: 16/16.
- `tests/test_corrida0.py`: 90/90.
- `tests/test_emisor_fidelidad.py` y `tests/test_emisor_m2.py`: pasan.
- `tools/corrida0.py demanda`, `registro` seco y `status --json`: 207 usos,
  16 adopciones GEN2 activas, 191 dependencias legacy y cero diferencia en
  `corridas.tsv`, `resultados.tsv` y `usos.tsv`.
- `tools/snapshot_motor_gen2.py --verifica`: reproducción exacta.
- `python3 tools/ya_medido.py salud.atencion.grave_ennvih2002`: salida final
  cruda `MEDIDA-EN: tramite-ola5-propuesta-v0.yaml`.
- `tests/check.py --baseline`: línea base VERDE; conserva únicamente 3 FAIL
  históricos (T06/T08) y sus WARN ya congelados.
- `git diff --check`: pasa.

Los congelados históricos siguen byte a byte:

| artefacto | sha256 |
|---|---|
| `snapshot-M-triada-v1_0.json` | `b53ac6d51d1b50ce929fdf1b3e14b124c11db39fb216a15d7073a287ed3f065c` |
| `CALC-TRIADA-0002/resultados.json` | `e2d0adc2a9fb9722d50a9479916129b3524cb87ce9021359ebfe755ec0e9e22a` |
| `F5-completa-resultado-v1_0.json` | `e1ec8765f769f76c7f649958f46b72b34fcef786bcc113f5c3cbc997c4ed0079` |

## Obligaciones y residuales

| obligación | evidencia | consumidor/alcance | cierre o residual |
|---|---|---|---|
| Consumir el linaje de 17 | `milpa/src/linaje.py`; vistas; PR #710 | emisor GEN2 | CERRADA; NC-0157 cierra |
| Fallar cerrado sin fuente apta | `emitir_binaria_contrato`; casos 02, 04, 07 y 09 | toda emisión GEN2 | CERRADA |
| Conservar baseline histórico | modo `HISTORICO`; hashes F5 | comandos y artefactos anteriores | CERRADA |
| Selección temporal exacta | `baseline_temporal.py`; caso 06; transferencia ENIGH | FAM operativo | CERRADA para la serie implementada |
| No usar árbitro | guard de rol; caso 08 | transferencia GEN2 | CERRADA |
| Complementos dependientes | ENCUCI emite con padre; ENVIPE sin firma no emite | TRA/CIV | CERRADA técnicamente; NC-0085 permanece por decisión de adopción |
| Corrupción por evento | r2 `proxy_descriptivo`; pruebas de propósito/dominio | TRA r2 | CERRADA la protección; NC-0107/0153 permanecen por fuente/regla |
| DIN/S6 inferenciales | límites trasladados y snapshot | DIN/SALUD | FP-371, FP-372 y NC-0156 permanecen |
| Fintech por producto exacto | D10 descriptiva | R1.6 | NC-0122 permanece |
| Confirmación independiente | fuera de este acto | evaluación retenida | NC-0158 / GEN2-EVALUACION-SIN-FUGAS |

**CONTADOR: cero.** Este acto consume mediciones ya selladas, no crea ni
adopta una nueva medición científica. No firma opciones del benchmark ni
fusiona PR alguno.
